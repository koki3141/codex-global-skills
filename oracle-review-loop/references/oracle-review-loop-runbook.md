# Oracle Review Loop Runbook

This runbook operates `/Users/koki/.codex/skills/oracle-review-loop/scripts/oracle_review_loop.py`.

The workflow has three separate artifacts:

- Skill: `/Users/koki/.codex/skills/oracle-review-loop/`
- Tool: `/Users/koki/.codex/skills/oracle-review-loop/scripts/oracle_review_loop.py`
- State/output: `.oracle-review-loop-state.json` and `.oracle-review-loop/`

## 0. Use This Only After the Preflight

Before starting any real Oracle run, follow `/Users/koki/.codex/skills/oracle-prompt-design/SKILL.md`.

Prepare a short preflight summary:

- Oracle question: the one-sentence question.
- Why Oracle: why an independent second-model pass is useful.
- Attach: each file/glob and its role.
- Exclude: each file/glob intentionally not sent and why.
- Missing: evidence that would help but is unavailable or intentionally omitted.
- Route: browser, API, or manual paste. API needs explicit user consent.

For broad or sensitive attachment sets, run an Oracle preview first:

```bash
oracle --dry-run summary --files-report \
  -p "<prompt>" \
  --file "<target-file-or-glob>"
```

Do not proceed if the preview includes secrets, credentials, cookies, private records, unrelated vault content, unrelated dirty-tree files, or files whose role is unclear.

### Research-updated rubric axes

Before deriving a 100-point rubric for AI, agent, knowledge-system, review, automation, or research-support work, update the evaluation axes from current sources.

Use this source order:

1. OpenAI official documentation, research posts, system cards, and policy/help pages relevant to the task.
2. Recent primary agent research papers, especially agent memory, agentic RAG, skill lifecycle, tool use, agent evaluation, and agent-as-a-judge work.
3. Secondary summaries only as pointers to primary sources.

Record the source set in the rubric or in the preflight summary. Separate source-backed requirements from local inferences. If current web or Deep Research access is unavailable, state that limitation and either pause or create a provisional rubric clearly marked as based only on attached files.

## 1. Choose the Entry Path

### Path A: Rubric is not decided yet

Generate a rubric and stop for user review.

```bash
python3 /Users/koki/.codex/skills/oracle-review-loop/scripts/oracle_review_loop.py \
  --derive-rubric \
  --goal "<deliverable goal>" \
  --file "<target-file-or-glob>"
```

Expected result:

- Oracle creates `.oracle-review-loop/<timestamp>/00-rubric.md`.
- The script writes `.oracle-review-loop-state.json`.
- The script stops before creating creator/evaluator review threads.

Show `00-rubric.md` to the user. Edit it if needed. Then continue with Path B.

### Path B: Reviewed rubric is ready

Start the fixed creator/evaluator loop using the same state file.

```bash
python3 /Users/koki/.codex/skills/oracle-review-loop/scripts/oracle_review_loop.py \
  --goal "<deliverable goal>" \
  --file "<target-file-or-glob>"
```

When `.oracle-review-loop-state.json` has `rubric_review_required: true`, the script reloads the edited `00-rubric.md` from `rubric_output` and freezes it before starting the loop.

### Path C: Rubric is supplied directly

Use this when the user already gave a stable 100-point criterion.

```bash
python3 /Users/koki/.codex/skills/oracle-review-loop/scripts/oracle_review_loop.py \
  --goal "<deliverable goal>" \
  --rubric "<100-point criterion>" \
  --file "<target-file-or-glob>"
```

For a longer rubric, prefer a file:

```bash
python3 /Users/koki/.codex/skills/oracle-review-loop/scripts/oracle_review_loop.py \
  --goal "<deliverable goal>" \
  --rubric-file "<rubric.md>" \
  --file "<target-file-or-glob>"
```

## 2. What the Loop Does

The first execution creates two fixed Oracle sessions:

- creator session: writes or revises the deliverable.
- evaluator session: scores the creator output against the frozen rubric.

After that, the script only uses `--followup` for those session IDs. It keeps the same creator chat thread and the same evaluator chat thread.

The script does not edit the target deliverable file directly. It writes Oracle outputs into `.oracle-review-loop/`. Apply accepted changes separately, then verify them locally.

## 3. Stop Condition

The evaluator prompt requires:

```text
Score: N/100
```

The loop stops only when the evaluator's last non-empty line is exactly:

```text
FINAL_DECISION: PASS
```

For 100-point approval, the evaluator is also instructed to include:

```text
100点満点です。合格です。終了してください
```

If the evaluator gives a high score but does not emit `FINAL_DECISION: PASS`, the loop continues until `--max-rounds` is reached.

## 4. State and Resume

Default state:

```text
.oracle-review-loop-state.json
```

Default output directory:

```text
.oracle-review-loop/<timestamp>/
```

Normal resume is the same command as before:

```bash
python3 /Users/koki/.codex/skills/oracle-review-loop/scripts/oracle_review_loop.py \
  --goal "<deliverable goal>" \
  --file "<target-file-or-glob>"
```

Manual resume from known Oracle sessions:

```bash
python3 /Users/koki/.codex/skills/oracle-review-loop/scripts/oracle_review_loop.py \
  --goal "<deliverable goal>" \
  --rubric-file "<fixed-rubric.md>" \
  --creator-session "<creator-session-id>" \
  --evaluator-session "<evaluator-session-id>" \
  --last-evaluator-output "<latest-evaluator-output.md>" \
  --file "<target-file-or-glob>"
```

If browser follow-up refuses to submit because the saved ChatGPT conversation did
not load stable prior turns, do not force a fresh chat. Read the saved session
metadata, copy the stored ChatGPT conversation URLs, and resume with explicit
browser tabs:

```bash
jq -r '.browser.runtime.tabUrl' ~/.oracle/sessions/<creator-session-id>/meta.json
jq -r '.browser.runtime.tabUrl' ~/.oracle/sessions/<evaluator-session-id>/meta.json

python3 /Users/koki/.codex/skills/oracle-review-loop/scripts/oracle_review_loop.py \
  --goal "<deliverable goal>" \
  --rubric-file "<fixed-rubric.md>" \
  --creator-session "<creator-session-id>" \
  --evaluator-session "<evaluator-session-id>" \
  --creator-browser-tab "<creator-chatgpt-url>" \
  --evaluator-browser-tab "<evaluator-chatgpt-url>" \
  --last-evaluator-output "<latest-evaluator-output.md>" \
  --file "<target-file-or-glob>"
```

This keeps the fixed creator/evaluator chat threads. Do not use `--force` to
work around this failure; `--force` is for duplicate prompt guards and can start
unwanted new work.

If browser attachment upload cannot reach a send-ready state, keep the same
ChatGPT URLs and retry with a reduced text-only context:

```bash
python3 /Users/koki/.codex/skills/oracle-review-loop/scripts/oracle_review_loop.py \
  --goal "<deliverable goal>" \
  --rubric-file "<fixed-rubric.md>" \
  --creator-session "<creator-session-id>" \
  --evaluator-session "<evaluator-session-id>" \
  --creator-browser-tab "<creator-chatgpt-url>" \
  --evaluator-browser-tab "<evaluator-chatgpt-url>" \
  --last-evaluator-output "<latest-evaluator-output.md>" \
  --browser-attachments never \
  --no-bundle-files \
  --file "<small-text-file>" \
  --file "<other-minimal-evidence>"
```

This is a same-thread fallback, not a reason to start new creator/evaluator
threads. If the returned output lacks a unique prompt marker or is byte-identical
to a previous answer, treat it as stale capture and rerun only after confirming
the active browser tab is the intended conversation.

Start a separate independent loop by using a different state file or `--force-new`:

```bash
python3 /Users/koki/.codex/skills/oracle-review-loop/scripts/oracle_review_loop.py \
  --force-new \
  --state ".oracle-review-loop-state-<name>.json" \
  --goal "<deliverable goal>" \
  --rubric-file "<fixed-rubric.md>" \
  --file "<target-file-or-glob>"
```

## 5. Wait and Rate Settings

Defaults:

- `--max-rounds 1000`
- `--delay-min-seconds 0`
- `--delay-max-seconds 600`
- `--delay-distribution power-law`

Disable waiting for local dry-runs or controlled tests:

```bash
--delay-distribution none
```

The wait is for load reduction and operational pacing. Do not frame it as detection evasion.

## 6. Dry-Run the Wrapper

Use wrapper dry-run to inspect generated Oracle commands without sending anything:

```bash
python3 /Users/koki/.codex/skills/oracle-review-loop/scripts/oracle_review_loop.py \
  --dry-run \
  --delay-distribution none \
  --goal "<deliverable goal>" \
  --rubric "<100-point criterion>" \
  --file "<target-file-or-glob>" \
  --max-rounds 1
```

This validates script wiring, not Oracle's file packing. Use Oracle's own `--dry-run summary --files-report` for attachment previews.

## 7. Common Failure Modes

### Rubric changed after loop start

The script rejects rubric changes after creator/evaluator sessions exist. Start a new loop with `--force-new` or a new `--state`.

### Wrong chat thread risk

Check `.oracle-review-loop-state.json` before continuing. The creator and evaluator session IDs must be the intended sessions.

### Browser or login failure

Follow `/Users/koki/.codex/skills/oracle/SKILL.md` browser login recovery. Do not repeatedly rerun the same failing command without checking `oracle status` and the stored session.

### Sensitive files in preview

Stop. Narrow `--file` globs or add excludes before any real browser/API transmission.

### Max rounds reached without PASS

Treat this as a review failure, not as near-success. Inspect the last evaluator output, then either revise the rubric, improve attachments, or stop and apply the best verified findings manually.

## 8. After PASS

1. Read the final creator output and final evaluator output.
2. Apply accepted edits to the real target files.
3. Run local verification commands appropriate to the target.
4. Commit only the target edits and relevant skill/runbook updates.
5. Do not commit `.oracle-review-loop/` or `.oracle-review-loop-state.json`.

If the loop revealed a reusable process improvement, update this skill through `/Users/koki/.codex/skills/skill-improver/SKILL.md` conversation-derived mode.

Capture only reusable lessons:

- recurring rubric design pattern
- attachment category that was missing
- repeated evaluator failure pattern
- script behavior that should be automated

Do not capture:

- full Oracle transcripts
- one-off scores
- private project content
- final deliverable prose
