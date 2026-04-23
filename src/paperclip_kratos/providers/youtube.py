from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from urllib.parse import quote_plus, urlencode
from urllib.request import urlopen

from ..models import TopicConfig, VideoSource
from .transcript import TranscriptProvider


class YouTubeDiscoveryProvider:
    """Provider de descoberta com integração real no YouTube Data API v3.

    Se ``YOUTUBE_API_KEY`` não estiver configurada, cai no modo placeholder.
    """

    SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
    VIDEOS_URL = "https://www.googleapis.com/youtube/v3/videos"

    def __init__(self) -> None:
        self.transcripts = TranscriptProvider()

    def discover(self, config: TopicConfig) -> list[VideoSource]:
        api_key = os.getenv("YOUTUBE_API_KEY", "").strip()
        if not api_key:
            return self._placeholder_results(config)

        sources: list[VideoSource] = []
        for keyword in config.keywords[: config.max_results]:
            search_items = self._search(keyword, config.max_results, api_key)
            video_ids = [item["id"]["videoId"] for item in search_items if item.get("id", {}).get("videoId")]
            details_map = self._video_details(video_ids, api_key) if video_ids else {}

            for item in search_items:
                video_id = item.get("id", {}).get("videoId")
                if not video_id:
                    continue
                snippet = item.get("snippet", {})
                details = details_map.get(video_id, {})
                transcript = self.transcripts.fetch(video_id)
                score = self._score_result(snippet, details, keyword, transcript["available"])
                sources.append(
                    VideoSource(
                        title=snippet.get("title", "Sem título"),
                        channel=snippet.get("channelTitle", "Canal desconhecido"),
                        url=f"https://www.youtube.com/watch?v={video_id}",
                        description=snippet.get("description", ""),
                        published_at=snippet.get("publishedAt"),
                        duration=details.get("contentDetails", {}).get("duration"),
                        views=self._safe_int(details.get("statistics", {}).get("viewCount")),
                        score=score,
                        notes=self._build_notes(snippet, details, keyword, transcript),
                        use_cases=self._suggest_use_cases(config, score),
                        transcript_available=transcript["available"],
                        transcript_excerpt=transcript["excerpt"],
                        editorial_angles=self._editorial_angles(snippet, keyword, transcript["excerpt"]),
                    )
                )

        deduped: dict[str, VideoSource] = {}
        for source in sorted(sources, key=lambda item: item.score, reverse=True):
            deduped.setdefault(source.url, source)
        return list(deduped.values())[: config.max_results]

    def _search(self, keyword: str, max_results: int, api_key: str) -> list[dict]:
        params = {
            "part": "snippet",
            "q": keyword,
            "type": "video",
            "maxResults": min(max_results, 10),
            "safeSearch": "moderate",
            "order": "relevance",
            "key": api_key,
        }
        with urlopen(f"{self.SEARCH_URL}?{urlencode(params)}") as response:
            payload = json.loads(response.read().decode("utf-8"))
        return payload.get("items", [])

    def _video_details(self, video_ids: list[str], api_key: str) -> dict[str, dict]:
        params = {
            "part": "contentDetails,statistics",
            "id": ",".join(video_ids),
            "key": api_key,
        }
        with urlopen(f"{self.VIDEOS_URL}?{urlencode(params)}") as response:
            payload = json.loads(response.read().decode("utf-8"))
        return {item["id"]: item for item in payload.get("items", [])}

    def _score_result(self, snippet: dict, details: dict, keyword: str, has_transcript: bool) -> float:
        score = 0.3
        title = (snippet.get("title") or "").lower()
        description = (snippet.get("description") or "").lower()
        if keyword.lower() in title:
            score += 0.3
        elif any(token in title for token in keyword.lower().split()):
            score += 0.15

        if any(token in description for token in keyword.lower().split()[:3]):
            score += 0.1

        views = self._safe_int(details.get("statistics", {}).get("viewCount")) or 0
        if views >= 100000:
            score += 0.2
        elif views >= 10000:
            score += 0.12
        elif views >= 1000:
            score += 0.06

        published_at = snippet.get("publishedAt")
        if published_at:
            published_dt = datetime.fromisoformat(published_at.replace("Z", "+00:00"))
            age_days = max(1, (datetime.now(timezone.utc) - published_dt).days)
            if age_days <= 30:
                score += 0.1
            elif age_days <= 180:
                score += 0.05

        if has_transcript:
            score += 0.08

        return round(min(score, 1.0), 2)

    def _build_notes(self, snippet: dict, details: dict, keyword: str, transcript: dict) -> list[str]:
        notes = [f"Encontrado pela keyword: {keyword}"]
        views = self._safe_int(details.get("statistics", {}).get("viewCount"))
        if views is not None:
            notes.append(f"Views observadas: {views}")
        duration = details.get("contentDetails", {}).get("duration")
        if duration:
            notes.append(f"Duração ISO-8601: {duration}")
        if transcript["available"]:
            notes.append("Transcript disponível para extração de insights")
        else:
            notes.append(f"Transcript indisponível: {transcript['reason']}")
        notes.append("Validar narrativa, autoridade do canal e timestamps antes de uso final")
        return notes

    def _editorial_angles(self, snippet: dict, keyword: str, transcript_excerpt: str | None) -> list[str]:
        title = snippet.get("title", "")
        angles = [
            f"Resumo prático sobre {keyword}",
            f"Comentário crítico a partir do vídeo '{title}'",
        ]
        if transcript_excerpt:
            angles.append("Carrossel com 3 aprendizados extraídos do transcript")
            angles.append("Post com insight acionável + fonte citada")
        return angles

    def _suggest_use_cases(self, config: TopicConfig, score: float) -> list[str]:
        use_cases = ["NotebookLM"]
        if "instagram" in [item.lower() for item in config.platforms]:
            use_cases.append("Instagram")
        if "linkding" in [item.lower() for item in config.platforms]:
            use_cases.append("Linkding")
        if score >= 0.7:
            use_cases.append("Artigo")
        if score >= 0.8:
            use_cases.append("Tutorial")
        return use_cases

    def _placeholder_results(self, config: TopicConfig) -> list[VideoSource]:
        sources: list[VideoSource] = []
        for idx, keyword in enumerate(config.keywords[: config.max_results], start=1):
            score = max(0.1, 1.0 - (idx * 0.05))
            sources.append(
                VideoSource(
                    title=f"Pesquisa inicial: {keyword}",
                    channel="A validar",
                    url=f"https://www.youtube.com/results?search_query={quote_plus(keyword)}",
                    description=(
                        "Resultado placeholder para descoberta inicial. "
                        "Configure YOUTUBE_API_KEY para busca real."
                    ),
                    score=round(score, 2),
                    notes=[
                        "YOUTUBE_API_KEY não configurada",
                        "Verificar autoridade do canal",
                        "Extrair timestamps relevantes",
                    ],
                    use_cases=["NotebookLM", "Instagram", "Linkding", "Artigo"],
                    transcript_available=False,
                    transcript_excerpt=None,
                    editorial_angles=[
                        f"Resumo introdutório sobre {keyword}",
                        "Carrossel educativo com conceitos básicos",
                    ],
                )
            )
        return sources

    @staticmethod
    def _safe_int(value: str | int | None) -> int | None:
        try:
            return int(value) if value is not None else None
        except (TypeError, ValueError):
            return None
