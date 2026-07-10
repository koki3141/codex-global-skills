# Orchestrator Preferences

## User Preferences

- Prefer a single Codex agent first.
- Prefer native Codex subagents for same-provider, read-heavy parallel work.
- Use Orchestrator only for cross-provider, durable background, resume, interrupt, or persistent task-state requirements.
- Initial allowed runtimes: `codex`, `claude-code`.
- Do not use `shell`, `copilot`, `grok`, `pi`, or custom runtimes unless the current user request explicitly permits them.
- Read-only tasks are the default.
- Do not delegate deployment, deletion, credential changes, external writes, or production mutations.
- Use at most three concurrent child tasks, and use fewer whenever sufficient.
- Do not send private repository content to another provider without explicit approval for the exact provider and scope.
- Do not install, update, or globally reconfigure the Orchestrator CLI automatically.
- Do not silently substitute another model or provider when the requested one is unavailable.
- Pause and report when all permitted runtimes are unavailable, usage-limited, or fail preflight.
- Keep raw outputs on disk; return only compact structured summaries to the parent context.
