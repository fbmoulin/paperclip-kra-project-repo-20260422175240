from __future__ import annotations

from dataclasses import asdict, dataclass, field


@dataclass
class TopicConfig:
    topic: str
    audience: str
    goal: str
    language: str = "pt-BR"
    platforms: list[str] = field(default_factory=list)
    keywords: list[str] = field(default_factory=list)
    max_results: int = 10

    @classmethod
    def from_dict(cls, data: dict) -> "TopicConfig":
        return cls(**data)


@dataclass
class VideoSource:
    title: str
    channel: str
    url: str
    description: str = ""
    published_at: str | None = None
    duration: str | None = None
    views: int | None = None
    score: float = 0.0
    notes: list[str] = field(default_factory=list)
    use_cases: list[str] = field(default_factory=list)
    transcript_available: bool = False
    transcript_excerpt: str | None = None
    editorial_angles: list[str] = field(default_factory=list)


@dataclass
class ResearchRun:
    topic: str
    audience: str
    goal: str
    platforms: list[str]
    keywords: list[str]
    sources: list[VideoSource] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)
