from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .media import classify_media_type
from .project import Project, create_project


def ingest_media(media_root: Path, project_root: Path) -> dict[str, Any]:
    media_root = media_root.expanduser().resolve()
    if not media_root.exists():
        raise FileNotFoundError(f"media directory does not exist: {media_root}")
    if not media_root.is_dir():
        raise ValueError(f"media path is not a directory: {media_root}")

    project = create_project(project_root)
    assets = [_asset_for_path(path, media_root) for path in _iter_media_files(media_root)]
    manifest = {
        "schema_version": "0.1",
        "generated_at_utc": _utc_now(),
        "source_root": str(media_root),
        "counts": {
            "total": len(assets),
            "photos": sum(1 for asset in assets if asset["media_type"] == "photo"),
            "videos": sum(1 for asset in assets if asset["media_type"] == "video"),
        },
        "assets": assets,
    }
    project.write_json("analysis/assets.json", manifest)
    return manifest


def _iter_media_files(media_root: Path) -> list[Path]:
    files: list[Path] = []
    for path in media_root.rglob("*"):
        if not path.is_file():
            continue
        if classify_media_type(path) is None:
            continue
        files.append(path)
    return sorted(files, key=lambda path: path.relative_to(media_root).as_posix().lower())


def _asset_for_path(path: Path, media_root: Path) -> dict[str, Any]:
    stat = path.stat()
    media_type = classify_media_type(path)
    if media_type is None:
        raise ValueError(f"unsupported media file: {path}")

    content_hash = _sha256_file(path)
    relative_path = path.relative_to(media_root).as_posix()
    asset_id = "asset_" + _sha256_text(f"{relative_path}:{content_hash}")[:16]

    return {
        "asset_id": asset_id,
        "media_type": media_type,
        "source_path": str(path.resolve()),
        "pair_id": None,
        "captured_at_utc": _datetime_utc(stat.st_mtime),
        "duration_sec": 0.0,
        "camera": None,
        "favorite": False,
        "content_hash": content_hash,
    }


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _datetime_utc(timestamp: float) -> str:
    return datetime.fromtimestamp(timestamp, tz=timezone.utc).isoformat().replace("+00:00", "Z")


def _utc_now() -> str:
    return datetime.now(tz=timezone.utc).isoformat().replace("+00:00", "Z")
