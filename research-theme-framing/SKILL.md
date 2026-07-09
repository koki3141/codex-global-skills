---
name: research-theme-framing
description: This skill should be used when the user asks how to decide a research theme, whether a rough idea is a viable research topic, how to organize social significance, academic significance, objective, method, expected results, or how to turn an early research interest into a testable problem, failure mode, proposal mechanism, and center hypothesis before full experiment design.
---

# Research Theme Framing

Use this skill before full research design. Its job is to decide whether an idea has the structure of a research theme, not to write the whole proposal.

## Boundary

- Use this for pre-design framing: social significance, target phenomenon, academic gap, objective, mechanism, hypothesis, and next design question.
- Hand off to `research-design-generator` when the user needs formal comparison conditions, metrics, pilot experiments, parameter ledgers, or manuscript-level contributions.
- Invoke `evidence-gated-investigation` or `claim-calibration` when the user asks for source-backed novelty, literature-grounded gaps, or strong claims about prior work.
- Do not treat implementation knobs such as robot size, speed, communication range, seed count, model capacity, or task geometry as the theme. Treat them as later experimental factors unless they are the proposed mechanism itself.

## Input Normalization

Extract the user's rough idea into this table. Mark absent items as `未指定`.

| Field | Meaning |
|---|---|
| Application situation | Real situation where failure matters |
| Target phenomenon | Coordination, allocation, exploration, persistence, withdrawal, role formation, adaptation, etc. |
| Existing assumption | What current or intuitive approaches seem to assume |
| Failure mode | Which behavior fails, under what condition, and how it is observed |
| Proposed lever | The smallest decision, memory, signal, rule, or constraint that may control the failure |
| Evaluation object | What must change if the theme is real |

## Framing Order

Convert the idea in this order.

1. **Social significance**: State the real operation and the cost of failure. Avoid generic claims such as "society needs cooperation."
2. **Target phenomenon**: Name the phenomenon as an observable system behavior, not a value word. Prefer `探索継続/撤退`, `再割当`, `局所協調`, `役割形成`, `資源競合`, `通信制約下の適応`.
3. **Academic gap**: Express the gap as `existing assumption -> breakdown condition -> observable loss`. If literature is not checked, label it as a candidate gap.
4. **Objective**: Define the objective as controlling the failure mode. Do not define it as "use method X."
5. **Proposed mechanism**: Define the intervention point and target variable. Examples: withdrawal threshold, experience memory, local sharing, forgetting, priority signal, access right, role-switch condition.
6. **Center hypothesis**: Write one sentence in this form:

```text
Mechanism P changes [internal judgment or representation], suppresses/forms [failure mode or structure], and improves [target performance] under [boundary condition].
```

7. **Method placement**: Put environment, task difficulty, communication, robot size, speed, and observation range into experimental factors only after the hypothesis is stated.
8. **Result prediction**: Split expectations into internal change, structure change, performance change, and side effect.

## Theme Viability Gates

A theme is weak if any of these fail.

| Gate | Pass condition | Weak form |
|---|---|---|
| Failure gate | A measurable failure mode is named | "Coordination is important" |
| Mechanism gate | A minimal intervention changes an internal or interaction variable | "Try a new method" |
| Hypothesis gate | One sentence connects mechanism, structure, and performance | Separate background/method/result lists |
| Comparison gate | At least one baseline or simple heuristic can refute the claim | Only full proposal is tested |
| Parameter gate | Main knobs are later factors, not hidden theme definitions | Theme depends on arbitrary tuning |

If a gate fails, return the missing piece first. Do not continue into elaborate experiment design.

## Output Shape

Prefer this compact structure:

1. **Theme Diagnosis**: viable / under-specified / currently method-only.
2. **Compressed Theme**: one sentence.
3. **Causal Spine**: `application -> failure mode -> mechanism -> hypothesis -> observation`.
4. **What Belongs To Method Later**: list parameters and settings that should not decide the theme yet.
5. **Next Question**: the single missing decision needed before using `research-design-generator`.

## Style

- Use dense academic Japanese when the user writes in Japanese.
- Separate `確認済み`, `推測`, and `未確認` for literature or factual claims.
- Prefer conditional claims over vague hedging.
- Do not praise the idea. Diagnose structure and missing evidence.
