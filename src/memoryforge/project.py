from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PROJECT_CONFIG = "memoryforge.toml"
PROJECT_DIRS = (
    "analysis",
    "cache",
    "logs",
    "output/reports",
    "output/preview",
    "output/timelines",
)


@dataclass(frozen=True)
class Project:
    root: Path

    @property
    def config_path(self) -> Path:
        return self.root / PROJECT_CONFIG

    def path(self, relative_path: str) -> Path:
        return self.root / relative_path

    def write_json(self, relative_path: str, payload: Any) -> Path:
        path = self.path(relative_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        return path

    def read_json(self, relative_path: str) -> Any:
        return json.loads(self.path(relative_path).read_text(encoding="utf-8"))


def create_project(root: Path) -> Project:
    root = root.expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)
    for relative_dir in PROJECT_DIRS:
        (root / relative_dir).mkdir(parents=True, exist_ok=True)

    config_path = root / PROJECT_CONFIG
    if not config_path.exists():
        config_path.write_text(_default_config(), encoding="utf-8")

    return Project(root=root)


def _default_config() -> str:
    created_at = datetime.now(tz=timezone.utc).isoformat().replace("+00:00", "Z")
    return (
        'schema_version = "0.1"\n'
        f'created_at_utc = "{created_at}"\n'
        "\n"
        "[providers]\n"
        'video_frame_labeler = "manual"\n'
        'photo_labeler = "manual"\n'
        'audio_analyzer = "local_ffmpeg"\n'
        'scene_group_summarizer = "manual"\n'
        'planning_llm = "manual"\n'
        'repair_llm = "manual"\n'
        'evaluation_llm = "manual"\n'
    )
