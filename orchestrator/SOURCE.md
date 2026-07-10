# Source and local adaptation

## Upstream

- Repository: `backnotprop/orchestrator`
- Pinned commit: `d841c7342061f81221d709bed041da79644c5067`
- CLI package represented by the pin: `@backnotprop/orchestrator-cli@0.1.0`
- Runtime requirement: Node.js 24 or newer
- License: Business Source License 1.1. See `LICENSE`.
- Change date: 2029-07-09
- Change license: Apache License 2.0

## Why this is a global skill

Codex native subagents cover same-harness parallel work. This skill is retained only for capabilities that are materially different:

- launching other provider CLIs;
- durable background task IDs and status;
- process supervision and heartbeat state;
- persistent logs and results outside the parent context;
- resume, steering where supported, and interrupt controls;
- runtime model discovery and provider-limit inspection.

For ordinary coding, exploration, or review, use Codex native features instead.

## Local hardening

This directory is not a byte-for-byte copy of the upstream skill. The local profile intentionally:

- requires explicit/manual use;
- never auto-installs or upgrades the CLI;
- prefers Codex native subagents and `/review` first;
- allows only `codex` and `claude-code` during the pilot;
- blocks shell, Copilot, Grok, Pi, and custom runtimes unless explicitly approved;
- defaults to read-only tasks and prohibits parallel writers;
- requires privacy approval before private material reaches another provider;
- checks repository config, environment-variable names, task-store permissions, output truncation, and terminal state;
- integrates with `cost-aware-subagents` for delegation economics and `agent-arena` for evidence-first cross-model review.

These restrictions are user policy. They do not change or sandbox the upstream runtime by themselves.

## License boundary

The upstream Additional Use Grant permits production and internal business use except offering a commercial hosted or managed agent-orchestration service to third parties. Review the full license before redistribution, external service operation, or commercial productization.

## Update procedure

1. Inspect upstream release notes and compare the pinned commit with the candidate version.
2. Review runtime command arguments, default isolation, environment inheritance, config loading, task-store schema, and license.
3. Keep automatic installation disabled.
4. Re-run a read-only Codex task, a read-only Claude task, timeout, interrupt, resume where supported, and output-truncation checks.
5. Update the pin, package version, metadata, this file, and the Obsidian audit note.
6. Do not broaden the runtime allowlist without a separate user decision.
