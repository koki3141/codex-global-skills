# Evaluate a Harness

Use this reference when the desired conclusion is stronger than "this one job
closed after this intervention."

## Evaluation design

Define before running:

- representative task set and inclusion criteria;
- fixed model, agent version, reasoning effort, tools, permissions, and budget;
- clean or equivalently dirty starting state;
- accepted outcome and condition-blind grader where practical;
- proof completeness and authority-violation checks;
- number of repetitions and treatment order;
- retention, redaction, and privacy policy for trajectories.

## Metrics

Keep quality and cost separate.

```text
accepted_outcome
proof_complete
authority_violation
human_turns
assistant_turns
tool_calls
duplicate_tool_calls
input_tokens
output_tokens
elapsed_time
retries
```

Domain projects may add domain-specific misclassification metrics, but a generic
harness must not invent their meaning.

## Comparison rules

- Use equivalent revisions and external state.
- Randomize or counterbalance condition order when learning or cache effects are
  plausible.
- Grade outputs without revealing the condition when practical.
- Record whether the proposed intervention was actually used.
- Report run-level results, not only averages.
- Treat small samples as bounded evidence, not general treatment effects.
- Include new failure modes and maintenance cost in the decision.

## Minimum release gate

Retain a replacement only when it:

1. does not reduce accepted-outcome rate;
2. does not introduce authority violations;
3. preserves or improves claim-matched proof;
4. improves at least one predeclared efficiency or human-relay measure;
5. remains reversible and has a named owner.

When replacing an existing tool, preserve the old path until the comparison is
complete, then remove the losing implementation in a separate reviewable change.
