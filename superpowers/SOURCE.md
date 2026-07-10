# Source and local adaptation

## Upstream

- Repository: `obra/superpowers`
- Pinned commit: `d884ae04edebef577e82ff7c4e143debd0bbec99`
- Release represented by the pin: `v6.1.1`
- License: MIT. See `LICENSE`.

## Local profile

This directory is a Codex-global compatibility profile, not a byte-for-byte copy of the upstream plugin.

The upstream project provides a plugin, SessionStart behavior, and a library of separate skills. This local profile intentionally:

- collapses the core design-plan-TDD-review workflow into one global entrypoint;
- does not install or emulate upstream hooks;
- does not force skill invocation before every response;
- reuses existing local global skills such as `cost-aware-subagents`, `verification-loop`, and `code-review-excellence`;
- makes Agent Arena an explicit high-risk escalation instead of a default debate step;
- follows the closest project `AGENTS.md` before this profile.

The local behavior is therefore compatible with the upstream methodology but is not an official Superpowers distribution.

## Update procedure

1. Review the upstream release notes and changed skills.
2. Compare changes against the local invariants: design before consequential implementation, isolated work, TDD, specification review before quality review, and verification before completion.
3. Import only changes that improve the local profile without conflicting with existing global skills.
4. Update `metadata.upstream_commit` and this file.
5. Validate frontmatter and local references.
6. Re-run representative tasks before broadening automatic triggers.
