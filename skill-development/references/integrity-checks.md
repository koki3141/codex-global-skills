# Skill Integrity Checks

## Minimal local checks

```bash
# referenced files exist
rg -n "references/|examples/|scripts/|assets/" SKILL.md

# skill inventory
find . -maxdepth 2 -type f | sort

# obvious editor/cache noise
find . -type d -name "__pycache__" -o -name ".DS_Store"
```

## User-scoped global checks

```bash
# global skill directories without SKILL.md
find ~/.codex/skills ~/.agents/skills -mindepth 1 -maxdepth 1 -type d -exec sh -c 'for d do test -f "$d/SKILL.md" || echo "$d"; done' sh {} +

# stale labels when renaming a user-facing skill
rg -n "old-skill-name|Old Display Name|old default prompt" ~/.codex/skills ~/.agents/skills
```

## Common failure modes
- `SKILL.md` mentions references that were never created.
- A migrated skill still refers to old agent or plugin names.
- The directory contains logs or session artifacts.
- The frontmatter name and the directory slug drift apart.
- The skill promises a script-based path but ships no runnable script.
- A global user skill keeps a personal display name after the internal skill name was made neutral.
- A repository-local skill and a global skill share the same name and split the source of truth.
