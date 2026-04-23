from __future__ import annotations

from . import __name__  # noqa: F401
from ..models import TopicConfig, VideoSource


class YouTubeDiscoveryProvider:
    """Provider inicial de descoberta.

    No MVP atual, gera placeholders estruturados a partir das keywords.
    O próximo passo é trocar por integração real com YouTube Data API.
    """

    def discover(self, config: TopicConfig) -> list[VideoSource]:
        sources: list[VideoSource] = []
        for idx, keyword in enumerate(config.keywords[: config.max_results], start=1):
            score = max(0.1, 1.0 - (idx * 0.05))
            sources.append(
                VideoSource(
                    title=f"Pesquisa inicial: {keyword}",
                    channel="A validar",
                    url=f"https://www.youtube.com/results?search_query={keyword.replace(' ', '+')}",
                    description=(
                        "Resultado placeholder para descoberta inicial. "
                        "Substituir por busca real e metadados confiáveis."
                    ),
                    score=round(score, 2),
                    notes=[
                        "Verificar autoridade do canal",
                        "Extrair timestamps relevantes",
                        "Validar aderência ao objetivo editorial",
                    ],
                    use_cases=[
                        "NotebookLM",
                        "Instagram",
                        "Linkding",
                        "Artigo",
                    ],
                )
            )
        return sources
