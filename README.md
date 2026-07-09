# Codex Skills

Active skills are top-level directories that contain `SKILL.md`.

This directory is managed as a local Git repository for user-maintained global
Codex skills. It is intentionally separate from any project-local `.agents/skills`
directory.

Repository scope:

- Track active user-maintained global skills under top-level skill directories.
- Track small supporting files such as `README.md`, validation scripts,
  references, templates, and non-secret examples.
- Do not track `.system/`, `backup/`, runtime logs, caches, environment files,
  credentials, tokens, or generated review-loop state.
- Do not track plugin caches under `$CODEX_HOME/plugins/cache`; those are
  managed by plugin installation and should not be treated as source.

Current conventions:

- `koki-pptx-slides/` is the canonical personal PPTX research-slide skill.
- `backup/` stores historical snapshots only. Backup entrypoints are named
  `SKILL.snapshot.md` so stale copies do not appear as callable skills.
- Extra frontmatter such as `version`, `tags`, `author`, and `dependencies`
  belongs under `metadata:`. Keep top-level YAML keys limited to the schema
  accepted by `quick_validate.py`.
- Before changing a skill, create a backup with
  `skill-improver/scripts/backup-skill.sh`.
- After changing a skill, run `skill-improver/scripts/verify-update.sh` and
  `skill-creator/scripts/quick_validate.py`.

Suggested Git workflow:

1. Edit the active skill under `~/.codex/skills/<skill-name>/`.
2. Validate the changed skill.
3. Review `git status --short` and stage only related files.
4. Commit with a focused message.
