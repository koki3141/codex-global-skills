---
name: skill-development
description: This skill should be used when the user asks to create a new skill, repair an existing skill, improve trigger descriptions, reorganize skill structure, maintain user-scoped global skills under ~/.codex/skills or ~/.agents/skills, or make a Codex/Claude skill more reusable and internally consistent.
---

# Skill Development

Use this skill to create or repair Codex/Claude skills in the **current local environment**, not in an abstract plugin template.

## Goal

Produce a skill that is:
- easy to trigger,
- lean at the `SKILL.md` layer,
- backed by real `references/`, `examples/`, and `scripts/` files when they are mentioned,
- free of dead local references.

## Core rules

- Keep **one skill = one durable job**.
- Treat the frontmatter description as the main trigger surface.
- Keep `SKILL.md` focused on workflow and boundaries.
- Move detailed catalogs, templates, and long explanations into `references/` or `examples/`.
- Do not mention files that do not exist.
- Do not inherit stale names, agents, or sibling skill references without verifying they exist locally.
- For user-scoped global skills, keep names and UI metadata neutral. Do not embed personal names, emails, private project names, or joke labels in `name`, `display_name`, `short_description`, or `default_prompt` unless the user explicitly wants that identity exposed.
- Keep the folder slug, frontmatter `name`, and any `$skill-name` invocation in `agents/openai.yaml` aligned.

## User-scoped global skill maintenance

When maintaining personal global skills in `~/.codex/skills` or `~/.agents/skills`:

1. Inventory real skill directories only. A directory without `SKILL.md` is not a valid skill; either remove it if empty or identify the owning runtime before preserving it.
2. Classify scope before moving or duplicating anything:
   - global: reusable across repositories and projects,
   - local: depends on vault paths, project structure, or private data,
   - plugin/runtime: supplied by an installed bundle and not hand-maintained here.
3. Prefer neutral, reusable names such as `user-custom-settings`, `oracle-prompt-design`, or `research-design-generator`. Avoid user-specific branding in visible labels.
4. Keep one source of truth and classify it before editing:
   - reusable global skill: `~/.codex/skills/<skill-name>/`, which is the Git-managed global source repository;
   - project-specific skill: `<project>/.agents/skills/<skill-name>/` in the owning Git repository;
   - installed runtime copy: `~/.agents/skills/<skill-name>/`, synchronized from its source of truth.
5. A source skill and an installed runtime copy may coexist only when ownership is documented and their managed files are byte-identical. Do not maintain two independently editable copies.
6. Validate every changed skill with `quick_validate.py`. If `PyYAML` is unavailable, use the existing `uv run --no-sync --with PyYAML ... quick_validate.py <skill-dir>` path.
7. After creating or changing a global or project-local skill, commit the validated source-of-truth files in their owning Git repository before finishing, unless the user explicitly says not to commit. Stage only the skill and directly related governance files; preserve unrelated worktree changes.
8. Use a Conventional Commits message for the skill commit. Do not push unless the user explicitly requests a push.
9. If a changed `~/.agents/skills/` copy has no identified source, stop treating it as canonical: classify its scope, copy it to the appropriate Git-managed source location, verify byte identity, and commit that source.

## Default workflow

### 1. Inspect the current environment first

Before writing anything:
- inspect the target skill directory,
- inspect neighboring skills that already solve a similar problem,
- verify which agents, commands, and sibling skills actually exist,
- identify stale references before adding new ones.

Use the local inventory as the authority. Do not write guidance against an imagined plugin layout.

### 2. Lock the skill contract

Define four things before editing:
1. what the skill does,
2. what triggers it,
3. what it explicitly does **not** do,
4. which bundled resources are actually needed.

If the skill only needs a short workflow, keep it short. Do not create `references/`, `examples/`, or `scripts/` just because the directories are conventional.

### 3. Write or repair the frontmatter

The frontmatter should:
- use the real skill identifier in `name`,
- use a third-person trigger description,
- include concrete phrases a user would naturally say,
- stay short enough to scan quickly.

Prefer descriptions of this form:

```yaml
---
name: skill-name
description: This skill should be used when the user asks to "...", "...", or needs help with ....
---
```

### 4. Keep the main file lean

A good `SKILL.md` should usually contain:
- a short goal section,
- role boundaries,
- a default workflow,
- safety or quality rules,
- a short list of additional resources.

Move these out of the main file when they get long:
- templates,
- exhaustive checklists,
- edge-case catalogs,
- sample outputs,
- long examples.

### 5. Add only real bundled resources

Use bundled resources deliberately:
- `references/` for detailed guidance that may be loaded selectively,
- `examples/` for real example outputs or scaffolds,
- `scripts/` for deterministic helper logic.

If a resource is mentioned in `SKILL.md`, it must exist.
If a resource exists but is never referenced or used, delete it.

### 6. Run integrity checks before closing

At minimum, verify:
- frontmatter parses,
- referenced local files exist,
- sibling skill or agent references are real,
- `SKILL.md` is not overloaded with material that belongs in references,
- temporary logs, caches, and editor artifacts are not left inside the skill directory.

### 7. Commit the skill source

After validation:

1. Resolve the source repository with `git -C <skill-source> rev-parse --show-toplevel`.
2. Inspect `git status` and `git diff` in that repository.
3. Confirm any installed copy is byte-identical to the source where applicable.
4. Stage only the skill source and directly related governance or handoff files.
5. Commit with a Conventional Commits message such as `chore(skills): track <workflow>` or `docs(skills): update <workflow>`.
6. Verify the commit and remaining worktree state. Leave the branch unpushed unless push was requested.

Do not finish with a newly created or modified global skill existing only under an untracked `~/.agents/skills/` directory.

## Typical repair patterns

### When the skill is too long
- keep the trigger and workflow in `SKILL.md`,
- move catalogs and deep detail into `references/`,
- keep a short read order so another model knows what to load first.

### When the skill is too thin
- add a default workflow,
- add at least one concrete example or checklist,
- make the boundaries explicit so the skill is not just a slogan.

### When the skill has stale references
- remove dead paths immediately,
- replace historical names with current local names,
- re-check neighboring agents/commands/skills against the live directory.

## Recommended output shape

When creating or repairing a skill, prefer ending with:
- what changed,
- which files were created or updated,
- what integrity checks were run,
- which source repository and commit contain the skill,
- what still needs manual follow-up, if anything.

## References

Load only what is needed:
- `references/checklist.md` - compact quality checklist before closing a skill edit
- `references/integrity-checks.md` - concrete local checks for missing files, dead references, and drift
- `references/skill-creator-original.md` - legacy background reference; use for context, not as the live source of truth
