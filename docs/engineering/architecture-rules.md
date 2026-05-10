# Architecture Rules

## Command Shape

Every pipeline command follows the same shape:

```text
read previous artifacts
  -> do bounded work
  -> write this step's artifact
  -> return a clear status
```

Commands should be safe to rerun. If a command cannot continue, it should leave
existing artifacts intact and report the missing prerequisite.

## Dependency Direction

- Domain helpers must not depend on CLI parsing.
- Provider integrations must not leak provider-specific response shapes into
  core artifacts.
- Exporters should consume validated `TimelinePlan`, not raw LLM output.

## Source Media Safety

Source media files are read-only inputs. Generated thumbnails, keyframes,
proxies, reports, and previews belong under the MemoryForge project directory.

## Agent Readability

Prefer boring, explicit, inspectable code. When a convention matters for future
agent work, encode it in tests, schemas, or docs instead of relying on chat
history.
