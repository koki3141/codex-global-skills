---
name: harness-engineering
description: This skill should be used when the user asks to "improve the agent harness", "evaluate agent effectiveness", "reduce repeated agent failures", "compare an agent workflow before and after a change", or needs a bounded evidence-based improvement to agent context, tools, authority, proof, or feedback loops.
---

# Harness Engineering

## Goal

Improve one bounded agent job by changing the environment around a fixed worker,
then verify the effect with a fresh comparable trajectory.

## Boundary

This skill owns the general improvement loop. It does not:

- redefine the target repository's acceptance criteria;
- grant mutation, deployment, data-access, or external-message authority;
- replace repository-native tests or domain-specific gates;
- treat one successful rerun as proof of general improvement;
- import another repository's private rules into the target.

The user's request, the closest `AGENTS.md`, and target-native contracts remain
authoritative.

## Default workflow

1. Select one representative job that is safe and cheap enough to rerun.
2. Record its revision, worker configuration, authority envelope, accepted
   outcome, proof requirement, budget, and stop conditions.
3. Observe a baseline trajectory or inspect a recent trajectory with reliable
   source evidence.
4. Locate the earliest failed handoff and classify it as context, capability,
   ownership, authority, proof, feedback, or a still-unconfirmed worker limit.
5. State one smallest reversible intervention and its expected mechanism.
6. Change the authoritative owner through the target's normal workflow.
7. Run target-native verification.
8. Rerun the same job in a fresh, materially equivalent trajectory.
9. Compare outcome, proof, human relay, retries, latency, authority behavior,
   and carrying cost.
10. Retain, revise, or remove the intervention.

## Required evidence record

```text
Job and accepted outcome:
Target revision and external state:
Fixed worker and authority envelope:
Baseline evidence:
Earliest failed handoff and owner:
Intervention and expected mechanism:
Native verification:
Fresh-rerun evidence:
Outcome and proof comparison:
Human-relay and latency comparison:
Risk and carrying-cost comparison:
Decision: retain | revise | remove
Known limits:
```

## Routing

- Read `references/improve-one-job.md` for the operational loop.
- Read `references/evaluate-harness.md` before causal, comparative, or
  longitudinal claims.
- Read `references/context-routing.md` when the suspected gap is context
  availability, retrieval, fidelity, or source ownership.

## Hard rules

- Preserve the fixed worker and materially equivalent task conditions during a
  before/after comparison.
- Do not weaken a grader, gate, policy, or acceptance criterion to create a win.
- Do not call a tool or instruction effective unless the rerun actually used it.
- Separate missing capability from poor discovery and missing context from poor
  routing.
- Keep target truth at its authoritative owner; the harness may route to it but
  must not create a competing source of truth.
- Prefer removal when an intervention adds noise, duplicates a better owner, or
  repeatedly fails to improve the job.

## Source

See `SOURCE.md` for upstream provenance and license.
