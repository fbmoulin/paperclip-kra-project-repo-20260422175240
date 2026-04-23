from __future__ import annotations

from typing import Any


class TranscriptProvider:
    def fetch(self, video_id: str, languages: list[str] | None = None) -> dict:
        languages = languages or ["pt", "pt-BR", "en"]
        try:
            from youtube_transcript_api import YouTubeTranscriptApi
        except ImportError:
            return {
                "available": False,
                "reason": "youtube-transcript-api not installed",
                "segments": [],
                "excerpt": None,
            }

        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=languages)
        except Exception as exc:  # noqa: BLE001
            return {
                "available": False,
                "reason": type(exc).__name__,
                "segments": [],
                "excerpt": None,
            }

        excerpt = self._build_excerpt(transcript)
        return {
            "available": True,
            "reason": None,
            "segments": transcript,
            "excerpt": excerpt,
        }

    def _build_excerpt(self, transcript: list[dict[str, Any]], limit: int = 6) -> str | None:
        if not transcript:
            return None
        chunks = [segment.get("text", "").strip() for segment in transcript[:limit]]
        cleaned = [chunk for chunk in chunks if chunk]
        if not cleaned:
            return None
        return " ".join(cleaned)
