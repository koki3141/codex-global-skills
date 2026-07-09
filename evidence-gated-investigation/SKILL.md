---
name: evidence-gated-investigation
description: Use this skill for any task that requires investigation, recovery, debugging, provenance tracing, root cause analysis, data verification, file comparison, log analysis, historical reconstruction, or claims about completeness, absence, origin, latestness, or causality.
---

# Evidence-Gated Investigation Skill

## Purpose

Prevent premature conclusions from partial evidence.

This skill ensures that the agent:
- Defines the claim being investigated
- Separates observation from inference
- Considers alternative hypotheses
- Checks output completeness
- Reports uncertainty honestly

## When to Use

Use this skill when the user asks:
- "なぜこうなった？"
- "原因を調べて"
- "復元して"
- "完全版を探して"
- "これは元々こうだった？"
- "存在する？"
- "消えた？"
- "最新版はどれ？"
- "このバグの原因は？"
- "このログから何が言える？"
- "このデータは正しい？"
- "このファイルは完全？"

## Key Principle

Do not answer the user's apparent question immediately.
First determine what kind of claim is being made.

## Claim Types

Classify the task into one or more of:
1. Existence
2. Non-existence
3. Completeness
4. Origin / provenance
5. Causality
6. Latestness
7. Consistency
8. User intent
9. Data correctness
10. Specification correctness

---

## Procedure

### Phase 1: Define the target claim

Write internally:
```text
Target claim:
Evidence required:
Search scope:
Known observations:
Unknowns:
```

### Phase 2: Generate alternative hypotheses

Always list at least 3 plausible hypotheses for non-trivial investigations.
Example:
- H1: The file was originally incomplete.
- H2: The file was complete in an earlier path but became truncated during migration.
- H3: The file was split into multiple files.
- H4: The missing content exists under another name.
- H5: The observed output is truncated, not the file itself.

Do not finalize until alternatives are checked or explicitly marked unresolved.

### Phase 3: Define evidence gates

For each hypothesis, define what would support or refute it.

| Hypothesis | Evidence that supports it | Evidence that refutes it | Status |
|---|---|---|---|
| H1 | Earliest complete history starts incomplete | Earlier complete version exists | Unchecked |
| H2 | Commit shows migration with content loss | No earlier complete version found | Unchecked |

### Phase 4: Collect evidence

Use the relevant tools.

**For files:**
- Read full file.
- Check beginning and end.
- Check line count and byte count.
- Check structural markers.

**For logs:**
- Preserve full log.
- Check timestamps.
- Check surrounding events.
- Avoid relying on the final error only.

**For Git:**
- Use path search and content search.
- Check renames, copies, deleted files, branches.
- Extract candidate versions fully.

**For tool / repository adoption:**
- Treat existence, official provenance, and safe adoption as separate claims.
- Verify exact org/repo candidates, claimed organization repository listings, official docs/blog links, license, and package metadata before calling a tool official.
- If official provenance is not confirmed, mark the item `watch_only` / `unverified`; do not install, create wrappers, or modify agent/MCP config.
- For MCP, agent, code-index, and context-compression tools, prefer version-pinned sandbox probes and avoid `install`, `wrap`, `proxy`, or `learn` commands until side effects are understood.
- Keep official provenance separate from repo existence. If a claimed organization/tool origin is unverified but a similarly named repo exists elsewhere, track them as separate candidates rather than merging the claims.
- For recurring tool evaluation, maintain a structured candidate DB with explicit `decision`, `adoption_status`, `risk`, `approved_usage`, and `reason` fields.
- See `references/tool-adoption-provenance.md` for the LifeOS AI tool radar pattern.
- See `references/lifeos-ai-tool-candidate-db.md` for the SQLite/JSON/CSV candidate database pattern and adoption-state vocabulary.

**For data:**
- Check schema.
- Check row counts.
- Check nulls, duplicates, ranges, and source consistency.

**For code:**
- Reproduce the issue when possible.
- Inspect stack traces fully.
- Check recent changes.
- Consider environment and dependency versions.

### Phase 5: Check output integrity

Before drawing conclusions, answer:
- Was any evidence truncated?
- Was any file only partially read?
- Was any command output summarized?
- Was any search scope limited?
- Was any tool result ambiguous?

If yes, do not make a strong claim.

### Phase 6: Report

Use:
```md
## 結論
## 確認済みの事実
## 推測
## 未確認・残リスク
## 代替仮説の扱い
## 信頼度
```

---

## Forbidden Final Statements

Do not write:
- "間違いなく"
- "完全に"
- "元々"
- "存在しません"
- "これが原因です"
- "これで確定です"
unless the evidence gate was passed.

Preferred alternatives:
- "確認できた範囲では"
- "現時点の証拠では"
- "有力な仮説は"
- "未確認の可能性として"
- "完全性はまだ保証できません"
- "この探索範囲では見つかっていません"
