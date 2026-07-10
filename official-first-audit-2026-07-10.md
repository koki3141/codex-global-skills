# Global Codex skills official-first audit — 2026-07-10

## Scope

This audit reviewed the active skill index and performed source-level comparison for the highest-priority overlaps with current Codex built-ins and the `openai/plugins` marketplace.

Decision meanings:

```text
KEEP_CUSTOM            official capability cannot satisfy the user contract
KEEP_OFFICIAL_WRAPPER  keep a thin, differently named user profile over official features
MIGRATE_TO_OFFICIAL    install and validate the official plugin, then retire the local entrypoint
MOVE_PROJECT_LOCAL     move to the owning repository's .agents/skills
CONSOLIDATE            merge overlapping user skills before deleting any capability
RETIRE                  remove because a current official capability now supplies the job
REVIEW                  retain temporarily; deeper task-level comparison required
```

## Applied in this audit

### KEEP_CUSTOM — added

| Skill | Decision | Why official Codex is insufficient |
| --- | --- | --- |
| `orchestrator` | KEEP_CUSTOM | Native Codex subagents do not provide the same cross-provider CLI control plane, durable task store, background process supervision, provider-specific resume/interrupt, and persistent external-agent logs. The retained skill is manual-only and read-only-first. |

### KEEP_OFFICIAL_WRAPPER — renamed

| Previous | New | Decision | Reason |
| --- | --- | --- | --- |
| `superpowers` | `engineering-review-stack` | KEEP_OFFICIAL_WRAPPER | The official Superpowers plugin is the baseline. The user profile remains because it adds manual triggering, evidence-gated investigation, cost-aware delegation, Agent Arena escalation, claim calibration, and the user's review/verification boundaries. A distinct name prevents collision with the official plugin. |

### MOVE_PROJECT_LOCAL

| Skill | Destination | Reason |
| --- | --- | --- |
| `equation-traceability-workflow` | `Fujisawa-lab-inside/masters-thesis-shimohara-2027/.agents/skills/` | Hard-coded thesis workspace, submodules, EQ IDs, Sphinx paths, and build commands are repository-specific. |
| `proto-institution-swarm-workflow` | `koki3141/proto-institution-swarm/.agents/skills/` | Hard-coded C-PME/EIGI/IVP architecture, experiment manifest, artifact, paper, and claim-boundary rules are repository-specific. |

### RETIRE — replaced by a current Codex built-in

| Skill | Decision | Replacement |
| --- | --- | --- |
| `codex-hook-emulation` | RETIRE | Current Codex lifecycle hooks provide native `SessionStart`, `PreToolUse`, `PostToolUse`, `Stop`, and related event handling. The manual emulation entrypoint and its references/examples were removed. Any future Obsidian-specific behavior should be implemented as a native hook handler, not by restoring the emulator. |

### Generated index maintenance

The public index is now generated from top-level active `*/SKILL.md` files. A GitHub Actions workflow runs the generator after a skill entrypoint is added, changed, or deleted. This removed stale rows such as `codex-hook-emulation` and prevents future manual drift.

## Migrate to current official plugins

These local skills substantially overlap a current skill distributed through the OpenAI plugin marketplace. They are retained temporarily only to avoid a capability gap before local plugin installation is confirmed.

| Local skill | Official plugin / skill | Assessment | Migration rule |
| --- | --- | --- | --- |
| `chatgpt-apps` | `openai-developers` / `build-chatgpt-app` | Near byte-for-byte functional duplicate with a different name. | Install official plugin, run scaffold and review smoke tests, then retire local entrypoint. |
| `gh-address-comments` | `github` / `gh-address-comments` | Official version is newer and adds connector-plus-GraphQL thread handling and write safety. | Replace with official. Do not maintain the older local copy. |
| `gh-fix-ci` | `github` / `gh-fix-ci` | Official version includes current GitHub app integration and stronger residual-risk handling. | Replace with official. |
| `notion-research-documentation` | `notion` / same name | Official marketplace contains the same job. | Replace unless a concrete Obsidian/Notion-specific user delta is documented. |
| `notion-spec-to-implementation` | `notion` / same name | Official marketplace contains the same job. | Replace unless a concrete user workflow delta is documented. |
| `cloudflare-deploy` | `cloudflare` / `cloudflare` | Official plugin is broader and explicitly docs-first across Workers, Pages, storage, AI, networking, security, and IaC. | Install official plugin and retire the narrow local deployment copy after smoke testing. |

### No-gap migration sequence

Do not delete these entrypoints before local Codex confirms the official plugin is installed and usable.

```text
1. Open /plugins in Codex CLI.
2. Install openai-developers, github, notion, cloudflare, and superpowers as needed.
3. Restart Codex.
4. Run one representative task per replacement.
5. Remove the corresponding legacy global entrypoint.
6. Confirm the generated public index changed in the follow-up Actions commit.
```

## Keep because the user contract is materially stronger

| Skill or family | Decision | Distinct contract |
| --- | --- | --- |
| `agent-arena` | KEEP_CUSTOM | Heterogeneous independent generation, atomic-claim extraction, evidence gate, cross-critique, dissent-preserving synthesis, and degraded-mode disclosure. |
| `cost-aware-subagents` | KEEP_CUSTOM | Delegation economics, model-tier routing, ownership, bounded waves, verification cost, and stop conditions beyond native subagent mechanics. |
| `engineering-review-stack` | KEEP_OFFICIAL_WRAPPER | User-specific composition of official Superpowers, `/review`, evidence, cost, claim, and Arena rules. |
| `evidence-gated-investigation`, `claim-calibration`, `output-integrity` | KEEP_CUSTOM | User-wide epistemic and completeness contracts not supplied as one official workflow. |
| `code-review-excellence`, `verification-loop` | KEEP_OFFICIAL_WRAPPER | Keep only for custom rubric, verification bundle, and user reporting requirements; use `/review` as the default reviewer. |
| `oracle`, `oracle-prompt-design`, `oracle-review-loop` | KEEP_CUSTOM | External second-model browser/CLI workflow, attachment planning, fixed rubric, and persistent review loop. |
| `user-custom-settings`, `koki-pptx-slides` | KEEP_CUSTOM | Explicit personal output, citation, calculation, and slide-density requirements. |
| Obsidian skill family | KEEP_CUSTOM | Vault-specific Markdown, Bases, knowledge graph, research log, lifecycle, and project-memory contracts. |
| Research and paper skill family | KEEP_CUSTOM | Domain-specific experimental, statistical, literature, paper, rebuttal, and journal-review workflows. |
| `orchestrator` | KEEP_CUSTOM | Cross-provider durable execution unavailable from native subagents alone. |

## Keep as official-origin fallback pending current replacement

The following appear to derive from the deprecated official `openai/skills` catalog or otherwise match earlier curated capabilities. A current one-to-one marketplace replacement was not confirmed in this audit, so they are not removed:

```text
pdf
jupyter-notebook
playwright
transcribe
security-best-practices
security-threat-model
```

Policy:

- do not fork them further without checking current official plugins;
- record provenance and upstream revision when editing;
- migrate when a current official plugin provides the same complete job;
- keep user-specific safety or artifact requirements as a separately named thin profile, not an official-name copy.

## Consolidate next

### Claude Code extension authoring cluster

```text
agent-identifier
command-development
hook-development
mcp-integration
memory-updater
plugin-structure
```

These jobs are related and several descriptions are Claude-specific while living in the Codex global list. Consolidate them into one `claude-code-extension-authoring` entrypoint with selective references, unless task-level evaluation shows materially different triggers are needed.

### Skill governance cluster

```text
skill-development
skill-improver
skill-quality-reviewer
```

Codex already supplies system skill creation support, and the official marketplace includes plugin evaluation tooling. Preserve only the user's Git source-of-truth, backup, byte-identity, validation, commit, and push rules. Prefer one maintenance entrypoint with subcommands or references.

### Browser and frontend verification cluster

```text
frontend-design
ui-ux-pro-max
web-design-reviewer
webapp-testing
playwright
```

The official `build-web-apps` plugin overlaps some implementation and browser-testing work. Retain personal visual-quality requirements, but evaluate whether five global triggers are necessary. Likely target: official build plugin plus one personal UI profile and one browser-test profile.

### Git workflow cluster

```text
git-commit
git-push
git-workflow
checkpoint-manager
```

These remain because they encode different side-effect boundaries, but their trigger descriptions should be tested for overlap. A future consolidation must preserve the user's English-prefix/Japanese-message rule and the distinction between local commit and remote push.

## Retention rule for everything not listed

All other active skills remain `KEEP_CUSTOM` or `REVIEW` for now. This is not a blanket quality endorsement. They are retained because no current official one-to-one replacement was established in the priority audit, or because their descriptions clearly encode a niche user/research/domain job.

Before materially editing any retained skill, re-run the official-first check from `OFFICIAL_FIRST.md`.

## Completed follow-up

```text
- removed the obsolete codex-hook-emulation entrypoint and supporting files;
- regenerated chatgpt-global-skill-index.md without stale rows;
- added automatic index refresh through GitHub Actions;
- updated the Obsidian official-first audit and engineering review stack notes;
- retained official-plugin duplicates only as no-gap fallbacks pending local smoke tests.
```

## Local actions still required

GitHub is the source repository, but plugin and CLI installation occur on the user's machine.

```text
- pull the global skill repository into ~/.codex/skills;
- install and smoke-test official plugins through /plugins;
- install the pinned Orchestrator CLI only after reviewing its package and Node/Nix impact;
- run quick_validate.py for changed skills;
- remove legacy official-duplicate entrypoints only after replacement tests pass.
```

## Review date

Re-audit after either condition:

- the next material Codex/plugin marketplace update;
- 2026-08-10, whichever comes first.
