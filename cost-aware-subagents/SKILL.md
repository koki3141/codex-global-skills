---
name: cost-aware-subagents
description: Orchestrate Codex subagents to reduce wall-clock time while bounding model/token cost, coordination overhead, and human review or rework. Use for tasks with at least two independent nontrivial workstreams, broad read-heavy exploration, orthogonal reviews, dependency-aware waves, or homogeneous batch items. Do not use for small tasks, tightly sequential work, overlapping writes, shared mutable state, or work without a credible verification method.
license: MIT
metadata:
  version: "0.1.0"
---

# Cost-aware subagent orchestration

## Objective

Minimize the combined cost of wall-clock time, model and tool usage, human review, and rework while meeting the required quality floor.

Treat a single agent as the default and control condition. Subagents are an optimization, not a default behavior. Parallelism primarily reduces elapsed time; it does not automatically reduce tokens or total cost.

## Operating defaults

Unless the task states otherwise:

- Use the `balanced` profile.
- Keep delegation depth at one. Instruct children not to spawn children.
- Use read-only workers for exploration, research, testing analysis, and review.
- Assign one writer to each file or ownership area. Never allow overlapping writes.
- Keep planning, merge decisions, and final verification in the parent thread.
- Pass only task-relevant context; never copy the full conversation or complete plan to every worker.
- Require compact structured results with evidence; do not return raw logs or long transcripts.
- Close completed or no-longer-needed agent threads.

## 1. Establish the optimization profile

Infer the profile from the request. If unspecified, use `balanced`.

- `economy`: minimize model and tool cost; use at most two concurrent children; cheap-first routing; no redundant review unless risk requires it.
- `balanced`: optimize total cost and elapsed time; use at most three concurrent children; cheap read-only workers plus one strong coordinator or verifier.
- `fast`: prioritize wall-clock time; use all genuinely independent ready tasks up to the configured thread cap; retain ownership and verification rules.
- `critical`: prioritize correctness and risk reduction; use focused specialists and a fresh independent verifier; do not increase agent count merely for consensus.

These concurrency values are starting limits, not universal optima. Change them only after task-specific evals show a better trade-off.

## 2. Build a dependency and ownership plan

Before spawning, create a compact table with:

`task_id | objective | dependencies | read_or_write | owned_paths_or_resources | expected_result | verification | model_tier`

Classify every node as one of:

- `ready-independent`: may run concurrently.
- `blocked`: wait for dependencies.
- `shared-write`: keep sequential or isolate in a separate worktree with disjoint ownership.
- `tiny`: keep in the parent; dispatch overhead is not justified.

## 3. Apply the delegation gate

Use subagents only when all applicable conditions hold:

1. There are at least two bounded, nontrivial workstreams that are ready and independent.
2. The workers do not need shared mutable state or overlapping file ownership.
3. Each task has explicit scope, non-goals, definition of done, and a compact return format.
4. The work is large enough to amortize dispatch and merge overhead.
5. The result can be verified by source evidence, deterministic checks, tests, a schema, or an independent reviewer.
6. The expected reduction in elapsed time or context pollution is greater than the expected coordination and review cost.

If these conditions fail, use one agent or a sequential pipeline. Record the selected mode internally; do not spawn agents merely because the skill was invoked.

## 4. Select one orchestration pattern

Use the smallest adequate pattern:

- `single`: small, sequential, tightly coupled, write-heavy, or weakly verifiable work.
- `parallel-read`: independent exploration, documentation research, log analysis, test-gap analysis, or orthogonal review lenses. This is the preferred subagent pattern.
- `dag-waves`: run only dependency-ready nodes in parallel, merge their structured outputs, then release the next wave.
- `specialist-verifier`: one specialist produces a result and a fresh independent agent attempts to falsify it. Use for security, migrations, public APIs, data loss, or other high-risk work.
- `batch-map`: homogeneous rows such as one file, package, service, incident, or PR per item. Use a fixed output schema, concurrency cap, and runtime cap. Prefer Codex batch subagent facilities when available.
- `isolated-writes`: parallel implementation only in separate worktrees or strictly disjoint paths and interfaces. Integrate and test centrally. Otherwise keep implementation sequential.

Do not run duplicate agents on the same scope unless the duplication is an intentional, bounded verification or ensemble experiment.

## 5. Route models and reasoning effort

Use capability tiers rather than hard-coding model names in task logic:

- `fast`: bounded read-only scans, extraction, classification, summarization, and routine checks.
- `standard`: implementation, planning, synthesis, and ambiguous multi-step work.
- `strong`: security, architecture, difficult debugging, contradiction resolution, and independent verification.

Start cheap and escalate at most once when a worker is blocked, low-confidence, contradicted by evidence, or fails verification. Do not launch a strong duplicate while a cheaper worker is still making adequate progress.

Read `references/model-policy.md` only when configuring concrete Codex agent models.

## 6. Dispatch with a strict contract

For every child, provide the fields in `references/delegation-contract.md`. At minimum include:

- task id and one-sentence objective;
- minimal background and exact inputs;
- scope, non-goals, and dependencies;
- allowed tools and sandbox expectations;
- read/write status and exclusive ownership;
- definition of done and verification requirement;
- output schema, evidence format, and confidence;
- budget or runtime cap and stop conditions;
- an explicit instruction not to spawn subagents unless authorized.

Do not ask a child to rediscover information the parent already has. Do not paste accumulated task history. Give it the task, relevant interfaces, and binding constraints only.

## 7. Execute in bounded waves

1. Spawn only `ready-independent` nodes, up to the profile cap and configured thread cap.
2. Keep the parent available for coordination; do not duplicate workers without a reason.
3. As results arrive, validate their shape and evidence. Reject malformed or unsupported findings.
4. Persist a small run ledger for multi-wave work so completed tasks are not redispatched after context compaction. Use a project-approved scratch path and do not commit it unless requested.
5. Close completed threads and stop workers whose result is no longer needed.
6. Release the next dependency-ready wave only after required inputs are accepted.
7. Merge in the parent. Resolve contradictions against primary evidence, not by majority vote alone.

For homogeneous batches, require each item to report exactly once and export status plus structured result fields.

## 8. Control writes and integration

- Explorers, researchers, and reviewers are read-only by default.
- One agent owns each file, directory, service, migration, or external resource at a time.
- Do not let multiple agents edit the same branch area concurrently.
- Cluster related fixes into one cohesive implementation task instead of launching one fixer per finding.
- Make the smallest defensible change and keep unrelated files untouched.
- Integrate sequentially, inspect the combined diff, and rerun the relevant checks after integration.

## 9. Verify before accepting

Use the cheapest credible verification first:

1. Validate structured output with `scripts/validate_result.py` when using the bundled schema.
2. Check cited files, symbols, commands, logs, or primary sources.
3. Run targeted format, lint, type, unit, integration, or build checks appropriate to the change.
4. Inspect the final diff and nonfunctional requirements such as compatibility, documentation, observability, and rollout behavior.
5. For high-risk work, dispatch a fresh verifier that did not create the finding or patch and ask it to falsify the result.
6. Separate `confirmed`, `rejected`, and `uncertain` findings. Do not convert uncertainty into a claim.

Do not accept self-reported success or a test pass as sufficient when important requirements are not algorithmically checked.

## 10. Stop and escalate deliberately

Stop spawning or running agents when any condition holds:

- the definition of done and quality floor are met;
- the remaining work is sequential or smaller than dispatch overhead;
- one additional wave produces no material new evidence;
- the configured token, tool-call, runtime, or agent budget is reached;
- expected marginal value is no greater than expected model, merge, and review cost;
- the same failure or uncertainty recurs twice.

After repeated uncertainty, escalate one model tier or request a human decision. Do not respond by recursively increasing agent count.

## 11. Report outcome and efficiency

Return a compact final report containing:

- selected mode and why it passed or failed the delegation gate;
- agents and waves used;
- result and material evidence;
- verification performed and failures encountered;
- elapsed time, token or credit usage, and tool cost when available;
- human-review or rework implications;
- stopped, skipped, or canceled work;
- remaining uncertainty and the next decision, if any.

For skill changes, follow `references/evaluation-protocol.md`. Do not enable broad implicit invocation until trigger precision, quality, cost, and latency have been compared with a single-agent baseline.
