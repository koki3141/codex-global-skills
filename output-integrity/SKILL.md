---
name: output-integrity
description: Use this skill whenever tool output, logs, file content, diffs, search results, generated text, API responses, or dataset previews may be partial, truncated, summarized, paginated, sampled, or incomplete.
---

# Output Integrity Skill

## Purpose

Prevent false conclusions caused by partial output.

## Core Rule

Partial output cannot prove completeness, absence, origin, or correctness.

## Treat as incomplete if you see:
- truncated
- omitted
- summarized
- preview
- partial
- first N lines only
- last N lines only
- pagination
- ellipsis
- output too long
- no line numbers
- UI-rendered excerpt
- abrupt beginning
- abrupt ending
- missing sequence numbers
- missing headers
- missing closing sections

---

## Required Actions

### For files
Check:
- total line count
- total byte count
- first section
- last section
- structural markers
- expected sequence continuity

### For archives / generated project templates
When unpacking a ZIP/tarball into a project directory, verify the extraction as a bounded object, not just that the folder exists:
- inspect archive entry count, uncompressed byte total, and top-level roots before extraction
- reject unsafe paths (`..`, absolute paths) before writing files
- if the archive has one wrapper directory, strip it intentionally and state the chosen target directory
- after extraction, compare file count and byte total against the archive scope, allowing for later generated files if you ran setup/tests
- verify expected entry-point files exist (`README`, `START_HERE`, `pyproject.toml`, scripts, docs)
- run the project’s own smoke checks if available, then cite exact commands and pass/fail output
- if dependency setup rewrites a lockfile or generates artifacts, distinguish “archive extracted” from “working project verified”

Session note: see `references/zip-project-template-verification.md` for a concrete Python extraction/verification pattern.

### For logs
Check:
- time range
- first relevant event
- final relevant event
- surrounding context
- omitted middle section
- repeated errors

### For diffs
Check:
- full patch
- stat summary
- renamed files
- copied files
- deleted files
- binary files

### For data
Check:
- row count
- column count
- schema
- nulls
- duplicates
- min/max
- sample is not full data

### For API responses
Check:
- pagination
- next cursor
- total count
- rate limits
- filtered fields
- partial response parameters

---

## Completeness Claim Gate

Before saying "complete", verify:
- I inspected the full object, not only a preview.
- I know the expected structure.
- I checked the beginning and ending.
- I checked count/size/schema where applicable.
- I resolved pagination or truncation.

If not, say:
```text
完全性は未確認です。
```

## Non-existence Claim Gate

Before saying "not found" or "does not exist", verify:
- I defined the search scope.
- I searched likely alternate locations.
- I searched alternate names.
- I handled pagination/truncation.
- I can state the scope of the negative result.

If not, say:
```text
この探索範囲では見つかっていません。
```
