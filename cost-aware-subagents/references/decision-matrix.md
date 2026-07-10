# Decision matrix and patterns

## Recommended optimization objective

Treat the workflow as a constrained optimization problem:

`minimize J = model_and_tool_cost + wt*wall_clock + wh*human_review_time + wr*rework_cost`

subject to `quality >= required_quality_floor` and all safety or ownership constraints.

The weights are task-specific:

- `economy`: increase the model/tool-cost weight.
- `fast`: increase the wall-clock weight.
- `critical`: increase the quality floor and rework/risk weight.
- `balanced`: account for all four terms.

## Delegation matrix

| Task shape | Default mode | Reason |
|---|---|---|
| One small change or one narrow question | single | Dispatch and merge overhead dominates. |
| Sequential debugging where each step depends on the previous result | single or dag-waves | Full fan-out guesses before evidence exists. |
| Broad codebase/document exploration with separable areas | parallel-read | Independent contexts reduce elapsed time and main-context pollution. |
| Security, correctness, tests, and maintainability review of the same diff | orthogonal parallel-read | Lenses are independent and mergeable; avoid duplicate generic reviewers. |
| Many similar files/packages/incidents | batch-map | Fixed schema and bounded concurrency provide predictable aggregation. |
| Multiple agents editing overlapping files | sequential | Shared writes create conflict and coordination cost. |
| Disjoint modules with stable interfaces and isolated worktrees | isolated-writes, cautiously | Parallel writes are acceptable only with strict ownership and central integration. |
| High-risk finding or patch | specialist-verifier | Independent falsification reduces correlated error. |

## Break-even proxy

Do not attempt false precision. Use these observable proxies before dispatch:

- Each child requires multiple nontrivial reads, searches, commands, or checks.
- The parent would otherwise load a large amount of low-value intermediate context.
- Independent work can overlap in time.
- The return is substantially smaller than the input examined.
- Verification is cheaper than reproducing the entire child investigation.

A task that can be completed in one or two direct actions should normally remain in the parent.
