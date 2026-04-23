from __future__ import annotations

from ..models import ResearchRun


def render_markdown_report(run: ResearchRun) -> str:
    lines = [
        f"# Research Report: {run.topic}",
        "",
        f"- Público: {run.audience}",
        f"- Objetivo: {run.goal}",
        f"- Plataformas: {', '.join(run.platforms)}",
        "",
        "## Keywords",
        "",
    ]
    lines.extend([f"- {keyword}" for keyword in run.keywords])
    lines.extend(["", "## Sources", ""])

    for idx, source in enumerate(run.sources, start=1):
        lines.extend(
            [
                f"### {idx}. {source.title}",
                f"- Canal: {source.channel}",
                f"- URL: {source.url}",
                f"- Score: {source.score}",
                f"- Transcript disponível: {'sim' if source.transcript_available else 'não'}",
                f"- Uso sugerido: {', '.join(source.use_cases)}",
                f"- Descrição: {source.description}",
                "- Notas:",
                *[f"  - {note}" for note in source.notes],
                "- Ângulos editoriais:",
                *[f"  - {angle}" for angle in source.editorial_angles],
                "",
            ]
        )
        if source.transcript_excerpt:
            lines.extend(["**Trecho inicial do transcript**", "", source.transcript_excerpt, ""])
    return "\n".join(lines)
