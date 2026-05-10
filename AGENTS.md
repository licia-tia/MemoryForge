# MemoryForge Agent Map

This file is a short navigation map for coding agents. Keep durable project
knowledge in `docs/`, schemas, tests, and executable tools.

## Start Here

- Product architecture: `ARCHITECTURE.md`
- Original architecture source: `docs/product/memoryforge-architecture-v0.1.md`
- Phase 2 notes: `docs/product/phase2-plan.md`
- Documentation index: `docs/index.md`
- Active implementation plans: `docs/exec-plans/active/`
- JSON schemas: `docs/schemas/`

## Engineering Rules

- Keep the CLI first. Every pipeline step should read previous artifacts from a
  project directory and write its own artifacts back to disk.
- Do not mutate source media files.
- Prefer stable schemas and validators over model-specific behavior.
- Add tests for schema contracts, artifact layout, and any validator logic.
- Keep provider integrations behind explicit interfaces. Do not hard-code one
  AI provider into domain logic.

## Commands

```bash
PYTHONPATH=src python3 -m memoryforge --help
python3 -m unittest
```

When adding a new command, update `README.md`, `docs/product/phase1-mvp.md`, and
the relevant schema or artifact-layout documentation.
