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
                "Notas de revisão:",
                *[f"- {note}" for note in source.notes],
                "",
            ]
        )
    return "\n".join(lines)
