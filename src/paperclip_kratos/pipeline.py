from __future__ import annotations

import json
from pathlib import Path

from .models import ResearchRun, TopicConfig
from .providers.youtube import YouTubeDiscoveryProvider
from .exporters.markdown import render_markdown_report
from .exporters.notebooklm import render_notebooklm_sources


class ResearchPipeline:
    def __init__(self) -> None:
        self.youtube = YouTubeDiscoveryProvider()

    def run(self, config: TopicConfig, output_dir: str | Path = "output") -> ResearchRun:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        sources = self.youtube.discover(config)
        run = ResearchRun(
            topic=config.topic,
            audience=config.audience,
            goal=config.goal,
            platforms=config.platforms,
            keywords=config.keywords,
            sources=sources,
        )

        (output_path / "research-report.json").write_text(
            json.dumps(run.to_dict(), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        (output_path / "research-report.md").write_text(
            render_markdown_report(run), encoding="utf-8"
        )
        (output_path / "notebooklm-sources.md").write_text(
            render_notebooklm_sources(run), encoding="utf-8"
        )
        return run
