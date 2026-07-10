# Delegation contract

Use this template for every subagent. Delete irrelevant fields rather than adding generic prose.

```text
TASK_ID: <stable id>
OBJECTIVE: <one sentence; one deliverable>
WHY_THIS_TASK: <minimal context needed to make correct decisions>
INPUTS: <exact files, URLs, commands, artifacts, or parent-provided facts>
SCOPE: <included paths, components, questions, or records>
NON_GOALS: <explicit exclusions>
DEPENDENCIES: <accepted upstream results or none>
ACCESS: <read-only | workspace-write | external side effects prohibited/allowed>
OWNERSHIP: <exclusive files/resources; "none" for read-only work>
TOOLS: <allowed and disallowed tools>
MODEL_TIER: <fast | standard | strong>
BUDGET: <runtime/tool-call/token proxy cap when available>
DEFINITION_OF_DONE: <observable completion conditions>
VERIFICATION: <tests, schema, source evidence, or reviewer expected>
STOP_OR_ESCALATE: <conditions for blocked/uncertain status>
RETURN_FORMAT: <JSON schema below or a task-specific compact schema>
CHILD_AGENTS: Do not spawn subagents unless the parent explicitly authorizes it.
```

## Default result schema

```json
{
  "task_id": "string",
  "status": "done | blocked | uncertain",
  "summary": "string",
  "findings": [
    {
      "claim": "string",
      "evidence": ["file:line, command result, artifact path, or primary-source reference"],
      "severity": "critical | high | medium | low | info",
      "confidence": 0.0
    }
  ],
  "artifacts": ["path or identifier"],
  "tests": [
    {
      "command": "string",
      "result": "pass | fail | not_run",
      "evidence": "concise output or artifact path"
    }
  ],
  "open_questions": ["string"],
  "recommended_next_action": "string"
}
```

Rules:

- Return one result only.
- Keep summaries concise; do not include private reasoning or raw transcripts.
- Every material claim needs evidence or must be marked uncertain.
- Use `blocked` when required access or input is missing; do not guess.
- Use `uncertain` when evidence is conflicting or insufficient.
