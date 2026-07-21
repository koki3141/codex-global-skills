# Improve One Harnessed Job

## Job contract

Freeze the comparison conditions before changing the harness.

```text
Target and revision:
Relevant external state:
Model and coding-agent configuration:
Representative job:
Accepted outcome:
Evidence that proves the outcome:
Authority and approval boundary:
Budget and stop conditions:
Suspected harness gap:
```

## Baseline

Prefer a fresh baseline when it is safe. Otherwise use a recent trajectory only
when its target state, worker, authority, and outcome are known. Record observable
evidence:

- accepted outcome and supplied proof;
- context that was available, retrieved, and relevant;
- capabilities discovered and invoked;
- human relay, retries, abandoned paths, latency, and review cycles;
- authority friction, unintended access, and recovery behavior.

## Earliest failed handoff

Trace the visible symptom upstream until one owner can shape future runs.

| Class | Question |
| --- | --- |
| Context | Was the needed fact absent, stale, overloaded, or unretrieved? |
| Capability | Was the operation missing or hard to discover, invoke, or verify? |
| Ownership | Did several representations compete for the same invariant? |
| Authority | Were capability and permission confused or missing a gate? |
| Proof | Did checks establish only an internal proxy instead of the outcome? |
| Feedback | Did an accepted lesson fail to survive into later runs? |
| Worker limit | Does the failure persist after other gaps are controlled? |

Do not label a worker limitation from one failed trajectory.

## Intervention hypothesis

```text
If <intervention> is added at <authoritative owner>, then the fixed worker will
<observable change> on <job>, because <mechanism>.

Evidence supporting the hypothesis:
Evidence weakening the hypothesis:
Expected carrying cost and owner:
```

Choose the smallest reversible intervention. Examples include a shorter route,
canonical example, typed boundary, actionable diagnostic, domain tool, approval
gate, real-system test, or recovery-aware runbook.

## Verification and rerun

Run both layers:

1. Target-native checks protecting internal contracts.
2. The user or operational journey proving the accepted outcome.

Then rerun with the same worker, authority envelope, and materially equivalent
state in a fresh session or isolated worktree. Confirm the intervention was
actually retrieved or invoked.

## Decision

- **Retain** when the bounded job closes and the gain justifies maintenance.
- **Revise** when the owner is correct but the interface remains hard to use.
- **Remove** when it adds noise, duplicates a better owner, or shows no repeatable
  benefit.
