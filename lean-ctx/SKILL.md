---
name: lean-ctx
description: Use LeanCTX to reduce context cost while reading files, searching code, exploring call graphs, or compressing shell output. Use when the user asks for LeanCTX, context compression, code-impact analysis, or verification of the installed LeanCTX integration.
---

# lean-ctx — Context Engineering for AI Agents

## Installed runtime

The managed user-scoped installation is pinned and must not be silently
replaced with the latest upstream revision:

```bash
/Users/koki/.local/bin/lean-ctx --version
/Users/koki/.local/bin/lean-ctx doctor
codex mcp list
```

Expected CLI release: `3.9.12`. See `SOURCE.md` for provenance. If the binary or
MCP registration is missing, report the mismatch and request an explicit
install or upgrade decision. Do not execute a remote installer from this Skill.

Do not run an agent-specific initializer inside a project unless the user asks
for project-local LeanCTX files. The user-scoped Codex MCP configuration is the
default integration.

## Core Tools (10 always visible)

| Tool | Purpose |
|------|---------|
| `ctx_read(path, mode)` | Read file with compression and caching |
| `ctx_search(pattern, path)` | Search code with compressed results |
| `ctx_shell(command)` | Run shell with compressed output |
| `ctx_tree(path, depth)` | Directory listing |
| `ctx_patch(path, ops)` | Anchored editing (line+hash, no old-text echo) |
| `ctx_session(action)` | Session state and persistence |
| `ctx_knowledge(action)` | Project knowledge across sessions |
| `ctx_overview(task)` | Task-relevant project map |
| `ctx_graph(action)` | Code relationships and impact |
| `ctx_call(name, args)` | Invoke any tool by name |

## Shell compression

```bash
lean-ctx -c "git status"
lean-ctx -c "cargo test"
lean-ctx -c "npm install"
lean-ctx ls src/
```

Use native raw commands or `LEAN_CTX_RAW=1` for authority documents, frozen
contracts, final experiment configuration, provenance, scientific output,
qualification decisions, and the final verification command. Compression is a
navigation aid, not an evidence source of truth.

## ctx_read Modes

| Mode | When |
|------|------|
| `anchored` | Files you will edit (full text + `N:hh\|` anchors for ctx_patch) |
| `full` | Verbatim cached read |
| `map` | Context-only (deps + exports) |
| `signatures` | API surface only |
| `diff` | After edits (changed lines) |
| `aggressive` | Large files, syntax-stripped; JSON arrays row-deduped (lossless) |
| `entropy` | Shannon filtering |
| `task` | Task-relevant lines |
| `lines:N-M` | Specific range |
| `auto` | System selects optimal |

Re-reads cost ~13 tokens. fresh=true bypasses cache.
Redundant JSON (arrays of like objects) is crushed losslessly into a compact
`_defaults` + per-row form; if a slice was dropped, recover it with
`ctx_expand(id, json_path=… | search=…)`.

## File Editing

Anchored editing saves output tokens: `ctx_read(mode="anchored")` → `ctx_patch(path, op, line, hash, new_text)`.
Never reproduce old text byte-for-byte; batch via `ops:[…]`; `op=create` writes new files.
Stale anchor → CONFLICT with fresh anchors (retry once). Native Edit/StrReplace stay fine;
`ctx_edit` (str_replace) is the legacy fallback via ctx_call/power profile.

## More Tools (via ctx_call or ctx_load_tools)

Architecture: ctx_symbol, ctx_callgraph, ctx_impact, ctx_architecture, ctx_routes, ctx_smells, ctx_quality
  ↳ "What breaks if I change this file/class/type?" → ctx_impact (file-level blast radius; resolves same-package/namespace type usage with no import for C#, Java, Go and Kotlin). "Who calls this function?" → ctx_callgraph (symbol-level). "How navigable / how much is complexity costing me?" → ctx_quality (navigability score + token quality tax).
Multi-agent: ctx_agent, ctx_share, ctx_task, ctx_handoff, ctx_workflow
Verify: ctx_benchmark, ctx_verify, ctx_proof, ctx_review
Batch: ctx_fill, ctx_execute, ctx_expand, ctx_pack

Full docs: https://leanctx.com/docs
