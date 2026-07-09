# Local Cue Closed-Loop Research Design

Use this reference when a research idea involves artificial life, complex systems, multi-agent systems, behavioral ecology, cognitive science, distributed control, stigmergy, environmental memory, swarm robotics, termite mounds, flocking, fish schools, language acquisition, cell collectives, or agents that act from local cues without direct access to the target object or global objective.

## Core Contract

Do not start from "X is important." Start from the paradox:

```text
Normally, this function appears to require direct observation of the target object, a global map, a desired final shape, or a central controller. This study asks whether agents without those privileges can nevertheless produce the function through local cues and environmental feedback.
```

Treat the biological or collective phenomenon as a reference for a design question, not as a mechanism already explained. Do not claim that the study proves the real organism's mechanism.

## Input Normalization

Extract these fields and mark missing items as `未指定`.

| Field | Meaning |
|---|---|
| 研究の核 | Center question in the form "Can agents that do not directly know X realize Y using only local cue Z?" |
| 対象現象 | Termite mound, flock, fish school, language acquisition, cell collective, robot swarm, etc. |
| 主体 | Agent, individual, robot, model, cell, learner, etc. |
| 観測可能 cue | Temperature, humidity, structure, local density, pheromone-like field, neighbors, gradient, local history |
| 観測不能情報 | Target location/state, global map, final shape, global objective function, desired morphology |
| 行動 | Move, pick, drop, deposit, remove, speak, choose, imitate, divide, switch role |
| 環境設定 | Section, space, boundary conditions, external forcing, daily variation, disturbance, target/protected region |
| 目的機能 | Thermal stabilization, flock formation, language structure acquisition, homeostasis, tunnel formation |
| 既存システム・データ | Simulator, GitHub repo, logs, experimental data, CT data, physical model |

## Causal Redefinition

Always rewrite the target phenomenon into this closed loop.

```text
local cue
-> target selection / action selection
-> local action
-> environmental or structural change
-> physical or informational field change
-> target function
```

Clarify which links are implemented, which are measured, and which are boundary conditions. If the agent uses the target location, final shape, or global objective internally, the premise is broken.

## Output Contract

When the user asks for a full research concept, produce the following sections.

### 1. 面白さの核

State what would normally seem necessary: direct target observation, global map, central control, target-state feedback, or a final-shape plan. Then state the paradox: the subject lacks those privileges, yet local cue-driven action may still generate the target function.

Avoid generic openings such as `Xは重要である` or `Yが課題である`.

### 2. 研究対象の再定義

Do not frame the work as reproducing the target phenomenon. Define it as the closed loop:

```text
局所 cue -> 局所行動 -> 環境・構造の変化 -> 物理場・情報場の変化 -> 目的機能
```

Add target selection explicitly when the cue controls where or what the agent acts on.

### 3. 社会意義

Describe the significance as a basic design principle for distributed systems that do not rely on central control, global maps, or direct observation of the target object. Connect it cautiously to application areas such as swarm robotics, adaptive infrastructure, collective construction, environmental monitoring, distributed sensing, or self-organizing material systems. Do not overclaim immediate practical deployment.

### 4. 学術意義

Cover these points when they fit the input.

- The controller may be distributed across agents, environmental cues, structure, history, and physical fields rather than located only inside the agent.
- Stigmergy and environmental memory can be modeled as multiple cues with different time scales, not only as a single pheromone.
- `action selection` and `target selection` can be separated, so cues may determine both what to do and where/on what to act.
- Evaluation should test the causal chain from cue to action, structure, field, and function, not only the appearance of successful cases.

### 5. 研究目的

Use this form and instantiate it.

```text
本研究の目的は、[主体] が [目的対象] を直接観測せず、[全体情報・中央制御・最終形状] を持たない条件で、局所 cue に基づく [行動] が [目的機能] を生む条件を同定し、その成立過程を因果連鎖として解明することである。
```

Then split the objective into 3 to 5 sub-objectives. Each sub-objective must correspond to a later experiment or metric.

### 6. Research Questions

Use four RQ classes unless the user asks for fewer.

| RQ | Role | Required content |
|---|---|---|
| RQ1: 成立条件 | Sufficiency | Which cue combinations are sufficient to produce the structure, behavior, and function? |
| RQ2: 必要条件 | Necessity | What breaks when each cue is removed from the all-cue condition? |
| RQ3: 因果過程 | Process | Which cue induces which behavior, which structure, which field response, and which functional outcome? |
| RQ4: 環境依存性 | Boundary | Does the sufficient or necessary cue set change under different environmental conditions? |

### 7. 実験方法

Give environment and agent settings equal weight.

Environment settings must specify:

- section or spatial setup
- boundary conditions
- initial structure
- disturbance or forcing
- protected or target region
- environmental ablations
- initial-structure ablations
- target-region location sensitivity

Agent settings must specify:

- observable cues
- unobservable information
- actions
- action selection
- target selection
- environmental-memory or pheromone-like update equation, when used
- cue normalization
- single-cue, composite-cue, and leave-one-out conditions

### 8. 評価方法

Use four evaluation layers.

| Layer | Question |
|---|---|
| 機能評価 | Was the target function realized? |
| 行動評価 | Did cues induce the expected actions or target choices? |
| 構造評価 | What structure was formed by those actions? |
| 物理場・情報場評価 | How did structure or environmental memory change the physical or informational field? |

Appearance similarity is not a primary metric. It can be a diagnostic visualization only.

### 9. 提案方法

Summarize the proposed method as:

- proposed experimental environment
- proposed behavioral rule
- proposed treatment of environmental memory and cues
- proposed evaluation framework

### 10. 新規性と有用性

Make the difference from existing work explicit. Useful contrast axes are:

- single cue or appearance generation versus multi-cue causal-chain evaluation
- action selection only versus separated action selection and target selection
- direct target observation versus no direct access to target, map, final shape, or global objective
- function evaluation alone versus function plus causal-chain evaluation

Use `first`, `novel`, or `unprecedented` only when source verification supports it.

### 11. 学術的根拠

Attach papers claim by claim. For each paper, include author, year, title, and which claim it supports. Use only literature verified in the current task or supplied by the user. If a title, year, or claim relation is uncertain, write `要確認`.

Candidate search families:

- Boids, behavioral animation, collective behavior
- agent-based modeling
- synthetic ethology
- stigmergy and environmental memory
- termite mound construction
- termite mound ventilation and thermal regulation
- active porous media
- swarm robotics
- constrained model comparison such as BabyLM, when the target is language acquisition or cognitive modeling
- distributed cognition and extended cognition
- control without centralized controller

### 12. 研究説明文

Produce three versions.

1. 先生に説明する30秒版
2. 研究企画書に入れる正式版
3. 国際学会 abstract 風の英語版

## Prohibitions

- Do not use the template `X is important. However, Y is a problem. Therefore, we propose Z.` as the main logic.
- Do not make appearance similarity the main evaluation.
- Do not claim that the study explains the actual biological mechanism.
- Do not assume that agents directly observe the target object, target state, final shape, or global objective.
- Do not show only successful examples.
- Do not choose cues or metrics after seeing favorable outcomes.
- Do not turn social significance into an immediate deployment claim.
