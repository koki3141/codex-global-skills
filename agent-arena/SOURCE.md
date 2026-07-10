# Source and local adaptation

## Upstream

- Repository: `zhjai/agent-arena`
- Pinned commit: `a9b4f262bddb4efd9b25c2b14c82ba3bb5570751`
- Protocol version observed at the pin: `0.2.3`
- License: MIT. See `LICENSE`.

## Local profile

This directory is a compact Codex-global adaptation rather than a byte-for-byte vendor copy.

Preserved upstream principles:

- independent heterogeneous agents first;
- evidence before consensus;
- deterministic checks before model judgment;
- dissent preservation;
- honest degraded-mode reporting;
- privacy and permission boundaries;
- explicit handling of mechanical orchestration failures;
- external-call and parent-context budget controls.

Local changes:

- reduced the trigger surface to consequential and contested or verifiable work;
- aligned orchestration with the existing `cost-aware-subagents` skill;
- aligned investigations with `evidence-gated-investigation`;
- integrated the workflow with the local `superpowers` compatibility profile;
- moved detailed protocol and CLI handling into `references/`;
- omitted host-specific UI metadata and companion skills that are not required locally;
- avoided pinning a concrete model identifier.

This is not affiliated with the upstream author, Anthropic, or OpenAI.

## Update procedure

1. Review upstream changes after the pinned commit.
2. Import changes that affect evidence handling, privacy, failure recovery, context budgeting, or Codex/Claude interoperability.
3. Do not broaden automatic triggering without task-local evaluation.
4. Confirm sibling skill names still exist.
5. Validate frontmatter and local references.
6. Test at least one bounded review, one open design review, and one unavailable-counterpart degraded run.
