---
name: oracle-prompt-design
description: Design high-signal prompts and attachment plans for Oracle second-model review. Use when the user asks how to prompt Oracle, what files to send to Oracle, whether an Oracle run is worth doing, or wants a ready-to-run Oracle command for code review, debugging, design critique, refactoring, research validation, or claim checking.
---

# Oracle Prompt Design

Use this skill before invoking Oracle or when drafting a prompt for a human to paste into another model. The goal is not a long prompt; it is a self-contained question with enough verified context and file evidence that the other model can give a specific, checkable answer.

## Decision Gate

Use Oracle when the task benefits from an independent second-model pass over concrete files: risky code review, subtle debugging, architecture critique, refactor planning, paper/claim validation, or comparing alternatives with tradeoffs.

Do not use Oracle for a simple local lookup, a command output that can be checked directly, or a task where the user has not approved external transmission of sensitive content.

Before any real run, classify the route:

- Browser ChatGPT run: still external transmission; dry-run attachments first.
- API run: requires explicit user consent because it can incur cost.
- Manual paste: use `oracle --render --copy` after the same safety review.

Do not run Oracle yet if the prompt lacks any of these:

- Background: project, goal, current state, and why a second model is needed.
- Context attachments: at least one relevant file that grounds the prompt. If no context file can be attached, stop and get explicit user approval for a no-file Oracle run.
- File plan: attached files with roles, omitted files with reasons, and any missing files Oracle should request.
- Evidence boundary: verified facts separated from assumptions.
- Answer contract: requested output format and "say insufficient evidence if the files do not support a conclusion."

## Prompt Construction

Build the prompt in this order:

1. State the project and operating context: repo name, stack, runtime, target platform, relevant commands, branch/status if relevant, and where the important code lives.
2. State the background before the question: what the user wants, what local work has already happened, what failed or remains uncertain, and why Oracle is being asked now.
3. State the exact question: one primary question, then optional subquestions. Avoid vague requests like "review this"; say what risk, bug, design choice, or claim should be tested.
4. Separate verified facts from hypotheses: include what has been observed, exact errors or outputs, and what remains uncertain.
5. Name the attached files by role: entrypoint, implementation, tests, config, logs, docs, data sample, prior discussion, expected behavior, or local diff.
6. Name exclusions by reason: sensitive, generated, irrelevant, too large, duplicate, or intentionally out of scope.
7. Add constraints and non-goals: public API compatibility, performance budget, dependency limits, security/privacy boundaries, style constraints, or files that must not be changed.
8. Specify the desired answer format: findings with file/path references, confidence level, patch plan, test plan, alternatives with tradeoffs, or "say insufficient evidence if the files do not support a conclusion."

## Attachment Plan

Every Oracle prompt should include context-file attachments by default. Every `--file` item must have a reason. Prefer the smallest set that still contains the truth. If a file is needed to answer the question, attach it or explicitly mark it as missing evidence; do not rely on the other model guessing repository context.

Include:

- Entrypoints and call sites for the behavior under review.
- The implementation under question.
- Relevant tests, fixtures, schemas, configs, logs, and exact error output.
- Docs or notes only when they define intended behavior.
- The current diff or patch when asking whether local changes are correct.
- Prior instructions or user requirements when they materially constrain the answer.

Exclude by default:

- Secrets, `.env`, credentials, private keys, tokens, cookies, personal records, and unrelated private vault content.
- Generated output, dependency directories, build artifacts, coverage, large binaries, and broad archives.
- Files included only because they are nearby rather than evidentially relevant.

Before running Oracle, produce three explicit lists:

- **Attach**: file/glob and the role it plays.
- **Exclude**: file/glob and why it should not be sent.
- **Missing**: file or command output that would improve the review but is unavailable or intentionally omitted.

Use preview commands before transmission:

```bash
oracle --dry-run summary --files-report -p "<prompt>" --file "path/**" --file "!path/to/exclude/**"
oracle --render --copy -p "<prompt>" --file "path/**"
```

## Pre-send Evidence Check

Before any real external transmission, inspect the dry-run / files-report output and record a short evidence check in the prompt, working log, or user-facing preflight summary.

Record:

- route: Browser ChatGPT run, API run, or manual paste.
- dry-run command used.
- total files and estimated tokens.
- top token-heavy files, if reported.
- Attach list matched to the actual selected files.
- Exclude list confirmed absent from the selected files.
- unrelated dirty-tree files confirmed absent.
- secrets, credentials, tokens, cookies, personal records, and unrelated private vault content confirmed absent.
- missing evidence intentionally left out, with the reason.

Do not proceed to a real run if the files-report contains a sensitive file, an unrelated dirty-tree file, a file included only by proximity, or a file whose role is not stated in the prompt.

## Prompt Template

```text
Project/context:
- <repo or workspace name>
- <stack/runtime/platform>
- <relevant commands and current failure/success status>
- <where the important code lives>

Background:
- <what the user is trying to achieve>
- <what local work has already happened>
- <why this needs an independent second-model review>

Task:
<one precise question for Oracle to answer>

Verified facts:
- <fact with source path, command output, or observed behavior>
- <fact with source path, command output, or observed behavior>

Hypotheses / uncertainty:
- <what may be true but is not yet proven>
- <what the local agent wants checked independently>

Attached files and roles:
- <path>: <why this file is necessary>
- <path>: <why this file is necessary>

Excluded or intentionally omitted:
- <path or pattern>: <reason>

Missing evidence, if any:
- <file or command output>: <why it would matter>

Constraints / non-goals:
- <must preserve / must not do / privacy boundary / dependency limit>

Desired output:
- Give findings first, ordered by severity or importance.
- Cite concrete files, functions, commands, or quoted snippets where possible.
- Separate confirmed issues from risks and speculation.
- If evidence is insufficient, say what additional file or command is needed.
- Propose a focused patch/test plan, not a broad rewrite.
```

## User-Facing Output

When preparing an Oracle run for the user, return:

- `Oracle question`: the one-sentence core question.
- `Why Oracle`: why second-model review is useful here.
- `Prompt`: the final prompt text or a short path to it if saved.
- `Attachments`: each file/glob with its role.
- `Exclusions`: sensitive or irrelevant material intentionally excluded.
- `Missing evidence`: files or command outputs that would improve the review but are unavailable or intentionally omitted.
- `Preflight`: dry-run command plus a short evidence-check summary covering file count, token estimate, token-heavy files, excluded material, dirty-tree contamination, and missing evidence.
- `Run command`: browser/API/render command, with API consent called out when applicable.

## Quality Checks

Before finalizing, verify:

- The prompt can stand alone for a model with no prior project memory.
- The prompt begins with background, not only the final question.
- The attached files are sufficient to answer the question, or the prompt explicitly asks Oracle to identify missing evidence.
- No file is attached without a stated role, and no required file is silently omitted.
- The prompt does not smuggle the desired conclusion as an assumption.
- Sensitive material has been excluded or explicitly approved by the user.
- The requested output is concrete enough to verify against code, tests, or source files afterward.
