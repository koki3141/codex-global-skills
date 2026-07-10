# Source and official boundary

## Official baseline

- Official marketplace repository: `openai/plugins`
- Official plugin: `superpowers`
- Upstream project: `obra/superpowers`
- Upstream commit reviewed when this profile was created: `d884ae04edebef577e82ff7c4e143debd0bbec99`
- Release represented by that upstream pin: `v6.1.1`
- License: MIT. See `LICENSE`.

## Why this profile remains

The official plugin supplies the development methodology and individual skills. This profile exists only to add user-specific composition and boundaries:

- manual, risk-gated activation rather than mandatory use on every request;
- `define-goal` for explicit acceptance and side-effect boundaries;
- `evidence-gated-investigation` before root-cause or provenance claims;
- `cost-aware-subagents` for delegation economics and ownership;
- `orchestrator` only for cross-provider durable execution;
- `agent-arena` only for consequential, contested, falsifiable decisions;
- `verification-loop` and `claim-calibration` before completion;
- the closest project `AGENTS.md` always takes precedence.

The profile must not use the name `superpowers`; that name belongs to the official plugin.

## Fallback boundary

`references/workflow.md` and `references/review-gates.md` preserve the user's quality floor when the official plugin is unavailable. They are not a full vendor copy and should not expand into one.

When the official plugin changes:

1. update the official plugin first;
2. use its current skills and hooks where they satisfy the job;
3. keep only the user-specific differences above;
4. remove local text that merely repeats official instructions;
5. re-run representative light, standard, and critical tasks.

## Retirement condition

Retire this profile when the official plugin can express all of the user's evidence, cost, privacy, Arena, verification, and completion policies without a separate entrypoint.
