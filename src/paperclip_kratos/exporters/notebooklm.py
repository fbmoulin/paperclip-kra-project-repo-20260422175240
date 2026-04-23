from __future__ import annotations

from ..models import ResearchRun


def render_notebooklm_sources(run: ResearchRun) -> str:
    lines = [
        f"# NotebookLM Sources: {run.topic}",
        "",
        f"Objetivo: {run.goal}",
        "",
    ]
    for source in run.sources:
        lines.extend(
            [
                f"## {source.title}",
                f"URL: {source.url}",
                f"Canal: {source.channel}",
                f"Descrição: {source.description}",
                f"Transcript disponível: {'sim' if source.transcript_available else 'não'}",
                "Notas de revisão:",
                *[f"- {note}" for note in source.notes],
                "Ângulos editoriais:",
                *[f"- {angle}" for angle in source.editorial_angles],
            ]
        )
        if source.transcript_excerpt:
            lines.extend(["Trecho inicial:", source.transcript_excerpt])
        lines.append("")
    return "\n".join(lines)
