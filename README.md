# Codex Skills

Active user-maintained skills are top-level directories that contain `SKILL.md`.

This directory is managed as a local Git repository for reusable global Codex
skills. It is intentionally separate from project-local `.agents/skills` and
from plugin-managed or system-managed skills.

Public ChatGPT Web index:

- [ChatGPT Global Skill Index](https://github.com/koki3141/codex-global-skills/blob/main/chatgpt-global-skill-index.md)
- [raw Markdown](https://raw.githubusercontent.com/koki3141/codex-global-skills/main/chatgpt-global-skill-index.md)

## Official-first policy

Use capabilities in this order:

1. Codex built-in feature or system skill.
2. Plugin from the OpenAI Codex marketplace.
3. A thin, differently named user profile over official capabilities.
4. A custom global skill only when official capabilities cannot satisfy the
   user's durable contract.
5. A project-specific skill under the owning repository's `.agents/skills/`.

Do not vendor or recreate a current official plugin skill merely to change its
wording. Keep a custom skill only when it adds material user-specific routing,
privacy, evidence, cost, approval, rollback, deterministic tooling, or domain
rules that the official capability cannot express.

See:

- [`OFFICIAL_FIRST.md`](OFFICIAL_FIRST.md)
- [`official-first-audit-2026-07-10.md`](official-first-audit-2026-07-10.md)

## Repository scope

Track:

- active user-maintained global skills under top-level skill directories;
- small supporting files such as references, scripts, templates, non-secret
  examples, source pins, and licenses;
- official-overlap decisions and migration notes.

Do not track:

- `.system/` or plugin-managed skills;
- `backup/`, runtime logs, caches, generated task state, or plugin caches;
- environment files, credentials, tokens, secrets, private keys, or cookies;
- project-specific skills that belong in a repository `.agents/skills/`.

## Current conventions

- `koki-pptx-slides/` is the canonical personal PPTX research-slide skill.
- `engineering-review-stack/` is the user-specific, manual profile over the
  official Superpowers plugin, Codex `/review`, evidence, cost-aware delegation,
  Agent Arena, and final verification. It deliberately does not use the name
  `superpowers`.
- `agent-arena/` is the evidence-first heterogeneous review escalation for
  consequential, contested, falsifiable decisions. It is not a default step for
  routine changes.
- `orchestrator/` is the manual, read-only-first control profile for
  cross-provider, durable background agent execution. Native Codex subagents
  remain the default for same-provider work.
- `cost-aware-subagents/` decides whether delegation is economically and
  operationally justified; it does not replace native subagent mechanics.
- Adapted upstream skills keep a source pin, local-difference notes, and the
  applicable upstream license inside the skill directory.
- A current official marketplace skill is not copied here. A temporary fallback
  must be marked for migration and removed after the official plugin is
  installed and smoke-tested.
- `backup/` stores historical snapshots only. Backup entrypoints are named
  `SKILL.snapshot.md` so stale copies do not appear as callable skills.
- Extra frontmatter such as `version`, `tags`, `author`, and `dependencies`
  belongs under `metadata:`. Keep top-level YAML keys limited to the schema
  accepted by `quick_validate.py`.

## Validation and Git workflow

Before changing a skill, create a backup with:

```bash
skill-improver/scripts/backup-skill.sh
```

After changing a skill, run the available validation paths, including:

```bash
skill-improver/scripts/verify-update.sh
uv run --no-sync --with PyYAML \
  python ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  ~/.codex/skills/<skill-name>
```

Then:

1. inspect `git status --short --branch`;
2. inspect the focused diff;
3. stage only the related skill and governance files;
4. commit with an English prefix and Japanese message;
5. push unless the user explicitly requests otherwise.

After adding, removing, or renaming a skill, regenerate the public index:

```bash
python3 scripts/generate-chatgpt-global-skill-index.py
```

Official plugins are installed and updated through Codex `/plugins`; plugin
cache content must not be copied into this repository.
