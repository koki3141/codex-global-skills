---
name: skillopt-sleep
description: This skill should be used when the user asks Codex to self-improve from past usage, run a nightly or offline sleep cycle, review archived sessions, replay recurring tasks, stage validated SkillOpt proposals, inspect sleep status, or adopt a reviewed proposal.
---

# SkillOpt-Sleep

## Goal

Drive a reviewable offline improvement cycle:

```text
harvest -> mine -> replay -> consolidate -> held-out gate -> stage -> adopt
```

The engine changes no model weights. Live skills or memory change only through
an explicit `adopt` action or a user-authorized `--auto-adopt` run.

## Installed runtime

```text
CLI: /Users/koki/.local/bin/skillopt-sleep
Version: 0.2.0
Pinned source: /Users/koki/.local/share/skillopt-v0.2.0
Codex runtime copy: /Users/koki/.agents/skills/skillopt-sleep/SKILL.md
```

Use the CLI directly for normal operation. The pinned repository runner remains
available through `$SKILLOPT_SLEEP_REPO/plugins/run-sleep.sh`.

## Default workflow

1. Run `status` for the target project.
2. Start with `dry-run --backend mock`.
3. If archived Codex sessions are unavailable, report zero harvested sessions;
   do not claim an optimization result.
4. For private or sensitive work, harvest to a task file, inspect and redact it,
   then set `reviewed` to `true` before any real backend run.
5. Bound real runs with `--max-sessions`, `--max-tasks`, and `--edit-budget`.
6. Read the generated report and show baseline, candidate, gate action, task
   count, session count, and exact edits.
7. Keep accepted proposals staged until the user reviews them.
8. Run `adopt` only after explicit approval.

## Commands

```bash
skillopt-sleep status --project "$(pwd)" --json

skillopt-sleep dry-run \
  --project "$(pwd)" \
  --source codex \
  --backend mock \
  --target-skill-path .agents/skills/example/SKILL.md \
  --max-sessions 5 \
  --max-tasks 3 \
  --json

skillopt-sleep harvest \
  --project "$(pwd)" \
  --source codex \
  --target-skill-path .agents/skills/example/SKILL.md \
  --max-sessions 5 \
  --max-tasks 3 \
  --output reviewed-tasks.json

skillopt-sleep dry-run \
  --project "$(pwd)" \
  --backend codex \
  --tasks-file reviewed-tasks.json \
  --progress \
  --json
```

## Data boundary

- Harvesting and the mock backend are local and make no provider calls.
- A real backend sends truncated transcript-derived or task-file content to the
  selected provider for mining, replay, judging, and reflection.
- Pattern-based secret redaction is defense in depth, not a guarantee.
- Do not run a real backend on private transcript content without explicit
  authorization for that egress.
- Keep raw transcripts, credentials, and unredacted task files out of commits
  and assistant messages.

## Hard rules

- Treat a held-out gain as run-specific evidence, not a general guarantee.
- Never edit archived sessions or raw transcripts.
- Never infer scientific, qualification, or claim status from a SkillOpt score.
- Do not optimize frozen contracts, authority rules, or generated skills.
- Do not use `--auto-adopt` unless the user explicitly requests it.
- Do not hand-edit the live target as a substitute for the engine's adopt path.
- Preserve the target's native validation and source-of-truth rules.

## Report

```text
Backend:
Transcript or task source:
Sessions and tasks:
Baseline -> candidate:
Gate action:
Accepted and rejected edits:
Staging directory:
Adopted:
Provider egress:
Known limits:
```

## Source

See `SOURCE.md` for provenance and the local compatibility adjustment.
