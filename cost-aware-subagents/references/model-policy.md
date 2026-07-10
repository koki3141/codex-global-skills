# Model and reasoning policy

This file contains concrete examples that can become stale. Recheck the current Codex model documentation before pinning names.

## Role policy

- Coordinator and merger: strong general Codex model, medium reasoning by default; high only for complex architecture, security, or contradiction resolution.
- Read-only scout: fast lower-cost Codex model, low or medium reasoning.
- Routine text-only worker: near-instant text model when available and the task needs no image or rich UI handling.
- Implementation worker: strong general Codex model, medium reasoning, exclusive write ownership.
- Independent verifier: strong general Codex model, high reasoning for high-risk tasks; read-only unless a separately approved fix is requested.

## Resolving concrete models

Model names and availability change across Codex clients, plans, and local configurations. Resolve each tier from the current local model catalog or official documentation at execution time. Do not infer an unlisted alias from a related model family.

Prefer omitting a pinned model when Codex's automatic selection is adequate. If you pin models, treat this file as configuration data and review it when availability, pricing, or quality changes. A project-specific agent configuration may name concrete models, but the global skill must remain usable without those files.

## Escalation policy

1. Start at the lowest tier that can credibly complete and verify the bounded task.
2. Escalate one tier only after a concrete failure, contradiction, low-confidence result, or failed check.
3. Do not retry indefinitely. After two unsuccessful attempts, change the task formulation, reduce scope, or request a human decision.
4. Do not use high reasoning for routine extraction, grep, formatting, or schema validation.
