---
name: obsidian-project-bootstrap
description: This skill should be used when the user asks to start a new research project, import an existing code-plus-Markdown repository into Obsidian, or bind the current repository to a compact research knowledge base for future syncing.
---

# Obsidian Project Bootstrap

Bootstrap a project knowledge base for the current repository.

## Role in the workflow

This is a **supporting skill**.

Use `obsidian-project-memory` as the main workflow authority. Use this skill only when a repository still needs its initial binding or rebuild.

## When to use

- The user says “start a new research project”.
- The user has an existing repo with code plus Markdown and wants an Obsidian knowledge base generated automatically.
- `obsidian-project-memory` detects a research-project candidate but no existing binding.

## Required input

Resolve the vault path from one of:
1. explicit user input,
2. `OBSIDIAN_VAULT_PATH`.

## Codex-native script path rule

Codex does **not** provide `${CLAUDE_PLUGIN_ROOT}`.

Resolve `project_kb.py` from one of these locations instead:

1. installed Codex skill tree:
   ```bash
   ${CODEX_HOME:-$HOME/.codex}/skills/obsidian-project-memory/scripts/project_kb.py
   ```
2. a checked-out Claude Scholar repository:
   ```bash
   <claude-scholar-repo>/skills/obsidian-project-memory/scripts/project_kb.py
   ```

If you are running inside a normal research repo rather than inside the Claude Scholar repo itself, prefer the installed Codex path.

## Procedure

1. Identify the repository root.
2. Run a preflight detect step first:
   ```bash
   PROJECT_KB_SCRIPT="${CODEX_HOME:-$HOME/.codex}/skills/obsidian-project-memory/scripts/project_kb.py"
   python3 "$PROJECT_KB_SCRIPT" detect --cwd "$PWD"
   ```
3. Only if the repo is unbound and should be imported, run bootstrap:
   ```bash
   PROJECT_KB_SCRIPT="${CODEX_HOME:-$HOME/.codex}/skills/obsidian-project-memory/scripts/project_kb.py"
   python3 "$PROJECT_KB_SCRIPT" bootstrap --cwd "$PWD" --vault-path "$OBSIDIAN_VAULT_PATH"
   ```
4. Verify that bootstrap created at least:
   - `.codex/project-memory/registry.yaml`
   - `.codex/project-memory/<project_id>.md`
   - `Research/{project-slug}/00-Hub.md`
   - `Research/{project-slug}/01-Plan.md`
   - `Research/{project-slug}/Knowledge/Source-Inventory.md`
   - `Research/{project-slug}/Knowledge/Codebase-Overview.md`
5. If the imported project still lacks real background or experiment context, switch to an agent-first pass:
   - read the most informative repo docs and code entry points,
   - synthesize durable notes into `Knowledge/`, `Papers/`, `Experiments/`, `Results/`, or `Writing/`,
   - avoid placeholder notes.
6. Summarize the created knowledge base and the next recommended canonical notes to fill in.

## Notes

- The bootstrap process imports **structure and summaries**, not raw datasets, caches, checkpoints, or the whole code tree.
- Ignore `.git`, `.venv`, `node_modules`, caches, checkpoints, binaries, and other heavy artifacts.
- The default vault is compact: `00-Hub.md`, `01-Plan.md`, `Knowledge/`, `Papers/`, `Experiments/`, `Results/`, `Writing/`, `Daily/`, `Archive/`.
- If `python3` is unavailable in the current shell, use the system Python interpreter that can run `project_kb.py` and say so explicitly.
- If the installed Codex path does not exist, point `PROJECT_KB_SCRIPT` at the checked-out Claude Scholar repo explicitly rather than using `${CLAUDE_PLUGIN_ROOT}`.

## References

- `references/BOOTSTRAP-RUNBOOK.md` - preflight decisions, failure modes, and post-bootstrap verification
