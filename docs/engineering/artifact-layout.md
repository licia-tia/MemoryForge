# Artifact Layout

`memoryforge init ./project` creates:

```text
project/
  memoryforge.toml
  analysis/
  cache/
  logs/
  output/
    reports/
    preview/
    timelines/
```

## Analysis Artifacts

- `analysis/assets.json` - media manifest produced by `ingest`.
- `analysis/segments.json` - video segments produced by `segment`.
- `analysis/summaries.json` - photo and segment summaries.
- `analysis/scene_groups.json` - grouped segment summaries.
- `analysis/project_brief.json` - planning context.
- `analysis/timeline_plan.json` - LLM rough-cut plan.
- `analysis/validation_result.json` - validator result.

## Output Artifacts

- `output/reports/` - human-readable reports and JSON evaluations.
- `output/preview/` - rendered preview videos.
- `output/timelines/` - OTIO, FCPXML, and EDL exports.
