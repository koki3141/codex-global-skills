# Evaluation protocol

Evaluate the skill against a single-agent baseline before broad rollout and after material changes.

## 1. Build a representative task set

Use real or replayable tasks stratified by shape:

- small negative-trigger tasks;
- parallel read-heavy exploration;
- sequential debugging;
- orthogonal review;
- homogeneous batch work;
- limited isolated-write work;
- high-risk specialist plus verifier work.

Include both tasks where delegation should trigger and tasks where it should not.

## 2. Compare control and treatment

- Control: same Codex environment and task, no orchestration skill, one agent.
- Treatment: this skill enabled and explicitly invoked.
- Hold the repository commit, permissions, tools, and quality rubric constant.
- Randomize or alternate order when practical to reduce learning and temporal effects.
- Capture the full run trace and artifacts.

## 3. Score four dimensions

### Quality

- task acceptance or merge readiness;
- deterministic test, lint, type, build, or schema checks;
- reviewer rubric score;
- critical defects, false positives, and missed requirements;
- nonfunctional requirements such as compatibility, docs, observability, and rollout safety.

### Time

- end-to-end wall-clock p50 and p95;
- parent active time and straggler wait time;
- human review minutes;
- time to first useful evidence.

### Cost

- input, output, cached, and reasoning tokens when available;
- model or credit spend;
- tool/API/GPU cost;
- number of agents, retries, and repeated context reconstruction.

### Coordination and rework

- duplicate work rate;
- write-conflict rate;
- verifier rejection rate;
- rework or fix minutes;
- malformed result rate;
- skill trigger precision and recall.

## 4. Use explicit rollout gates

Set thresholds before examining results. A reasonable policy is:

- quality must be non-inferior to the single-agent baseline within a declared tolerance;
- at least one primary efficiency objective must improve materially;
- no unacceptable increase in p95 cost, human review, conflicts, or severe defects;
- negative-trigger precision must be high enough that small or sequential tasks remain single-agent.

Do not optimize a single benchmark score. Review trace behavior, final artifacts, and human acceptance together.

## 5. Improve one variable at a time

Tune in this order:

1. trigger description and delegation gate;
2. task decomposition and ownership;
3. output schema and verification;
4. model tier and reasoning effort;
5. concurrency cap;
6. optional scripts or batch facilities.

Keep a reviewed change log outside the skill package or in version control. Do not let the skill rewrite its own policy based only on its self-evaluation.
