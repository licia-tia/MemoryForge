# Phase 1 MVP

Phase 1 turns a local media directory into structured artifacts that can later
be planned, validated, exported, and evaluated.

## Milestones

### v0.1 Local Ingest

- Create a project directory with a stable artifact layout.
- Scan local photos and videos.
- Write `analysis/assets.json`.
- Never modify source media.

### v0.2 Segment And Summaries

- Segment videos.
- Extract keyframes and lightweight audio features.
- Generate photo and segment summaries.
- Write `analysis/segments.json` and `analysis/summaries.json`.

### v0.3 Brief, Plan, Validate

- Generate scene groups and a project brief.
- Call a planning LLM through a provider boundary.
- Validate and repair `TimelinePlan`.

### v0.4 Preview And Evaluation

- Generate preview videos.
- Write selection and evaluation reports.

### v0.5 Editable Timeline

- Export OTIO.
- Export FCPXML for DaVinci Resolve Free.
- Export EDL as a fallback.
