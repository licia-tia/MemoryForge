# MemoryForge

MemoryForge is a configurable-model AI media understanding and rough-cut
system. The first milestone builds the project harness: a CLI, artifact layout,
schemas, and a local media ingest manifest.

## Install For Development

```bash
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -e .
```

## CLI

```bash
memoryforge init ./mf-project
memoryforge ingest ./media --project ./mf-project
```

The remaining Phase 1 commands are reserved in the CLI and will return a clear
not-implemented error until their artifacts and validators land.

## Test

```bash
python3 -m unittest
```

## Current Scope

- `init` creates a MemoryForge project directory and artifact folders.
- `ingest` scans a local directory for photo and video files and writes
  `analysis/assets.json`.
- Schemas and docs define the intended contracts for later pipeline stages.
