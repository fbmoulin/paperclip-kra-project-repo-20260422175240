from __future__ import annotations

from ..models import ResearchRun


def render_content_briefs(run: ResearchRun) -> str:
    lines = [
        f"# Content Briefs: {run.topic}",
        "",
        f"Público: {run.audience}",
        f"Objetivo: {run.goal}",
        "",
        "## Instagram",
        "",
    ]

    top_sources = run.sources[:3]
    for source in top_sources:
        lines.extend(
            [
                f"### Base: {source.title}",
                *[f"- {angle}" for angle in source.editorial_angles[:2]],
                "",
            ]
        )

    lines.extend(["## Linkding", ""])
    for source in top_sources:
        lines.extend(
            [
                f"- Salvar: {source.url}",
                f"- Motivo: usar como referência para {run.topic}",
                f"- Observação: score {source.score}",
                "",
            ]
        )

    lines.extend(["## Artigo", "", "- Tese central a partir das fontes coletadas", "- Comparar abordagens entre canais", "- Extrair exemplos práticos do transcript quando disponível", ""])
    return "\n".join(lines)
