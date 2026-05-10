# MemoryForge Architecture

MemoryForge is a configurable-model AI media understanding and rough-cut
system. Phase 1 is CLI-first and focuses on turning messy local media into
structured, recoverable artifacts that an LLM can plan against.

## Phase 1 Pipeline

```text
ingest
  -> preprocess
  -> segment
  -> summarize
  -> group / compress
  -> brief
  -> plan
  -> validate / repair
  -> export
  -> evaluate
```

The first implementation milestone is intentionally narrower:

```text
repo harness
  -> project artifact layout
  -> schema contracts
  -> init command
  -> local media ingest manifest
```

## Core Contracts

The stable domain objects are:

- `Asset`
- `Segment`
- `MediaSummary`
- `SceneGroupSummary`
- `ProjectBrief`
- `TimelinePlan`
- `PlanValidationResult`
- `TimelineEvaluation`
- `AnalysisCache`

Schemas live in `docs/schemas/`. Runtime code should treat these contracts as
more stable than any specific model provider.

## Project Artifact Layout

Each MemoryForge run targets a project directory:

```text
memoryforge.toml
analysis/
  assets.json
  segments.json
  summaries.json
  scene_groups.json
  project_brief.json
  timeline_plan.json
  validation_result.json
cache/
logs/
output/
  reports/
  preview/
  timelines/
```

Every command should be restartable from artifacts already written to disk.

## Provider Boundary

AI-backed steps are represented as provider roles:

- `video_frame_labeler`
- `photo_labeler`
- `audio_analyzer`
- `scene_group_summarizer`
- `planning_llm`
- `repair_llm`
- `evaluation_llm`

Provider configuration belongs in the project config, not inside domain logic.

## Agent-Readable Engineering

The repository is the record system. `AGENTS.md` is only a map; durable
decisions belong in versioned docs, schemas, tests, and executable checks.
Architecture rules should become mechanical tests or linters when they start to
matter for correctness.
