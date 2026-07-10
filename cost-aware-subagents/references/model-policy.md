# Model and reasoning policy

This file contains concrete examples that can become stale. Recheck the current Codex model documentation before pinning names.

## Evidence hierarchy

Resolve routing decisions in this order:

1. Current local capabilities: selectable child models, reasoning controls, concurrency, permissions, and actual callable tools.
2. Official provider documentation: model identifiers, availability, supported features, API prices, plan limits, and deprecations.
3. Independent evaluations: relative intelligence, coding-agent performance, speed, latency, hallucination behavior, and measured Cost per Task.
4. Task-local evaluation: acceptance, deterministic checks, retries, rework, human-review time, and total cost for the actual workload.

Independent benchmarks inform comparative routing but do not establish official availability or subscription entitlements. A model that is attractive on a public Pareto frontier is a candidate, not an automatic default.

## Optimization target

Choose the lowest expected whole-run cost that satisfies the declared quality floor:

`E[whole_run_cost] = parent + workers + tools + retries + verification + expected_rework`

Do not route from model price alone. Prefer a lower-cost worker only when its expected first-pass acceptance, escalation, verification, and rework profile make the complete route preferable.

## Role policy

- Coordinator and merger: standard or strong general Codex model, medium reasoning by default. Use strong when decomposition, integration, architecture, security, or contradiction resolution is materially difficult, not merely because the agent is the parent.
- Read-only scout: fast lower-cost Codex model, low or medium reasoning.
- Routine text-only worker: near-instant text model when available and the task needs no image or rich UI handling.
- Bounded implementation worker: standard lower-cost model, medium reasoning, exclusive write ownership, and deterministic verification. Use a strong model for ambiguous, coupled, high-risk, or weakly verifiable implementation.
- Independent verifier: strong general Codex model, high reasoning for high-risk tasks; read-only unless a separately approved fix is requested.

Prefer one capable coordinator plus the smallest number of cheaper workers whose outputs are independent and verifiable. Do not use a fixed fan-out such as three to five agents. Homogeneous duplicate workers are justified only for a declared ensemble or falsification experiment.

## Resolving concrete models

Model names and availability change across Codex clients, plans, and local configurations. Resolve each tier from the current local model catalog or official documentation at execution time. Do not infer an unlisted alias from a related model family.

Prefer omitting a pinned model when Codex's automatic selection is adequate. If you pin models, treat this file as configuration data and review it when availability, pricing, or quality changes. A project-specific agent configuration may name concrete models, but the global skill must remain usable without those files.

If the subagent interface has no per-child model selector, do not emulate routing with an unsupported alias. Use the available model, preserve the task and ownership decomposition, and report that model-tier routing was unavailable.

## Keep cost measures separate

Never substitute one of these measures for another:

- API price per input, cached, reasoning, or output token;
- independent benchmark Cost per Task;
- subscription message or credit allowance within a shared window;
- end-to-end Cost per Accepted Result, including coordination, verification, retries, rework, and human review.

A fivefold token-price difference does not prove fivefold usable work. Prefer Cost per Accepted Result for task-local decisions and report the component measures when available.

## Evidence snapshot: GPT-5.6 Sol and Luna

Revalidate this dated snapshot before use. Artificial Analysis reported on 2026-07-10 that it supported OpenAI's pre-release evaluation of GPT-5.6 Sol, Terra, and Luna. At max reasoning, it reported Intelligence Index scores of 59 for Sol and 51 for Luna, Coding Agent Index scores of 80 and 75, and approximately USD 1.04 versus USD 0.21 per Intelligence Index task. Its xhigh model pages reported 58 versus 49 Intelligence, 70.8 versus 185.2 output tokens per second, and API token prices of USD 5/30 versus USD 1/6 per million input/output tokens.

This evidence supports using Sol as a candidate coordinator, integrator, or escalation model and Luna as a candidate for bounded, verifiable workers when both are actually selectable. It does not establish proportional productivity, independent quota per child, or that every implementation task should use Luna. Artificial Analysis also reported Sol and Luna on the intelligence-versus-cost Pareto frontier ahead of Terra across reasoning efforts; treat that as a dated prior and re-evaluate all candidates on the actual task distribution rather than permanently excluding Terra.

The reported output-token speed measures generation after output begins. It does not include dispatch, time to first token, tool use, integration, or verification, so do not convert it into an end-to-end workflow speedup.

Sources:

- [Artificial Analysis: GPT-5.6 benchmarks](https://artificialanalysis.ai/articles/gpt-5-6-has-landed)
- [Artificial Analysis: GPT-5.6 Sol xhigh](https://artificialanalysis.ai/models/gpt-5-6-sol-xhigh)
- [Artificial Analysis: GPT-5.6 Luna xhigh](https://artificialanalysis.ai/models/gpt-5-6-luna-xhigh)

## Research basis

The routing policy is consistent with the following literature, but their reported gains remain workload-specific:

- [FrugalGPT](https://arxiv.org/abs/2305.05176) supports cascades that begin with cheaper models and escalate when needed.
- [RouteLLM, ICLR 2025](https://openreview.net/pdf?id=8sSqNntaMr) supports learned routing between stronger and weaker models to improve the quality-cost trade-off.
- [Efficient Agents](https://arxiv.org/abs/2508.02694) motivates matching agent-system complexity to task requirements and measuring cost of successful completion.
- [Understanding Agent Scaling via Diversity](https://arxiv.org/abs/2602.03794), a 2026 preprint, reports diminishing returns from homogeneous agent scaling and greater value from complementary diversity.
- [More Agents Is All You Need](https://arxiv.org/abs/2402.05120) shows that intentional sampling-and-voting can improve some tasks; treat this as a bounded ensemble pattern, not a default fan-out rule.

## Escalation policy

1. Start at the lowest tier that can credibly complete and verify the bounded task.
2. Classify failure as `capability`, `contract`, `access`, `environment`, or `ownership`.
3. Escalate one tier only for capability failure, substantive contradiction, or failed semantic verification.
4. Repair or stop contract, access, environment, or ownership failures instead of selecting a stronger model.
5. Retry only after changing an identified causal factor. After two unsuccessful attempts, reduce scope, reformulate the task, change verification, or request a human decision.
6. Do not use high reasoning for routine extraction, grep, formatting, or schema validation.
