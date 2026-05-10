from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .ingest import ingest_media
from .project import create_project


RESERVED_COMMANDS = ("segment", "summarize", "brief", "plan", "validate", "export", "evaluate")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="memoryforge",
        description="MemoryForge local media understanding and rough-cut CLI.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Create a MemoryForge project directory.")
    init_parser.add_argument("project", type=Path)
    init_parser.set_defaults(func=_cmd_init)

    ingest_parser = subparsers.add_parser("ingest", help="Scan local media into analysis/assets.json.")
    ingest_parser.add_argument("media", type=Path)
    ingest_parser.add_argument("--project", required=True, type=Path)
    ingest_parser.set_defaults(func=_cmd_ingest)

    for command in RESERVED_COMMANDS:
        reserved = subparsers.add_parser(command, help=f"Reserved Phase 1 command: {command}.")
        reserved.add_argument("--project", required=True, type=Path)
        reserved.set_defaults(func=_cmd_reserved)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except FileNotFoundError as exc:
        print(f"memoryforge: {exc}", file=sys.stderr)
        return 1
    except ValueError as exc:
        print(f"memoryforge: {exc}", file=sys.stderr)
        return 1


def _cmd_init(args: argparse.Namespace) -> int:
    project = create_project(args.project)
    print(f"Initialized MemoryForge project at {project.root}")
    return 0


def _cmd_ingest(args: argparse.Namespace) -> int:
    manifest = ingest_media(args.media, args.project)
    print(
        "Ingested "
        f"{manifest['counts']['total']} assets "
        f"({manifest['counts']['photos']} photos, {manifest['counts']['videos']} videos) "
        f"into {Path(args.project).resolve() / 'analysis' / 'assets.json'}"
    )
    return 0


def _cmd_reserved(args: argparse.Namespace) -> int:
    print(
        f"memoryforge: '{args.command}' is reserved for Phase 1 and is not implemented yet.",
        file=sys.stderr,
    )
    return 2
