# Context Routing

## Diagnose before adding context

Classify the failure:

- **Unavailable:** the needed fact did not exist in a reachable source.
- **Undiscoverable:** the source existed but no short route pointed to it.
- **Unretrieved:** the route existed but the worker did not use it.
- **Wrong fidelity:** summary was used where raw evidence was required, or full
  content overloaded a simple task.
- **Stale:** retrieved context no longer matched current state.
- **Competing:** multiple sources claimed the same authority.

## Owner-first routing

Keep the authoritative content at its natural owner. Add a compact route that
answers:

```text
When does this apply?
Where is the current source?
What must be read in full?
What can be summarized or indexed?
Which check detects drift?
When is the route retired?
```

Do not copy whole contracts into prompts or skills when a stable path and a
small trigger are sufficient.

## Fidelity policy

- Use maps, signatures, or summaries for initial discovery.
- Use targeted lines or definitions for implementation context.
- Use full raw content for authority documents, frozen contracts, final audits,
  provenance, and evidence-bearing status.
- Re-read after changes when a cache or summary may be stale.

## Evaluation

Measure whether the route was retrieved, whether the authoritative source was
opened, and whether the resulting decision matched the source. Token reduction
without decision accuracy is not an improvement.
