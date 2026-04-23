from __future__ import annotations

import json
from pathlib import Path

from .models import TopicConfig


def load_topic_config(path: str | Path) -> TopicConfig:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return TopicConfig.from_dict(data)
