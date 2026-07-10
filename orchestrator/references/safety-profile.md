# Orchestrator safety profile

## 1. Trust boundary

Orchestrator launches local processes that inherit the authority of the current user and the selected provider CLI. Treat every runtime, model prompt, repo-local config, wrapper executable, and returned command array as code or control input.

Do not infer safety from a task being called a review. A reviewer can still have filesystem, network, credential, or shell access through its runtime defaults.

## 2. Runtime allowlist

Pilot allowlist:

```text
codex
claude-code
```

Blocked unless explicitly approved in the current request:

```text
shell
copilot
grok
pi
custom runtimes
repo-local runtimes
```

Reasons:

- `shell` executes an exact local command.
- some provider CLIs may use permissive non-interactive flags;
- custom runtimes can point to arbitrary executables;
- runtime defaults can change independently of this skill.

Run `orchestrator doctor --json --compact` and inspect the effective runtime contract before launch.

## 3. Repository configuration

Orchestrator may load configuration from user and repository paths. Before operating an unfamiliar repository, inspect at least:

```text
orchestrator.config.json
.orchestrator/config.json
```

Do not launch a custom runtime merely because it is present. Verify:

- executable and arguments;
- prompt transport;
- output adapter;
- environment additions;
- timeout and output cap;
- working directory policy;
- whether it can write or execute shell commands.

If the repository is untrusted or the config is ambiguous, disable the custom runtime or stop.

## 4. Environment variables and credentials

The upstream process executor inherits the parent process environment. Before launching another provider, inspect **variable names only**, not values:

```bash
env | cut -d= -f1 | rg -i '(token|secret|password|passwd|cookie|credential|private|api[_-]?key|aws_|gcp_|azure_)'
```

If sensitive variables are present:

1. do not print their values;
2. do not launch an unapproved provider;
3. use an audited wrapper with an explicit environment allowlist, or stop and request approval;
4. never put credentials in a task prompt, manifest, log, or committed config.

Provider CLIs may use credentials stored under the user's home directory even with a scrubbed process environment. Treat provider access itself as part of the privacy boundary.

## 5. Private source and external providers

Before sending private code, research data, manuscripts, logs, or unpublished results to another provider, state:

```text
provider:
files_or_paths:
purpose:
minimum_required_scope:
expected_local_logs:
retention_or_policy_unknowns:
```

Require explicit user approval. Approval for one provider or one file set does not authorize unrelated content.

Prefer a minimized evidence packet over repository-wide access. Exclude secrets, raw datasets, credentials, cookies, private logs, unrelated proprietary directories, and generated artifacts unless indispensable and approved.

## 6. Task store permissions and retention

Orchestrator stores task records, prompts, logs, transcripts, results, and provider metadata under `~/.orchestrator` by default. Before first use:

```bash
mkdir -p ~/.orchestrator
chmod 700 ~/.orchestrator
find ~/.orchestrator -type d -exec chmod 700 {} +
find ~/.orchestrator -type f -exec chmod 600 {} +
```

Do not commit the task store. Review retention periodically and delete expired tasks only after confirming they are no longer needed for audit, recovery, or reproducibility.

When a custom `--orchestrator-dir` is used, apply the same ownership and permission rules.

## 7. Read-only work

A read-only task packet must say explicitly:

```text
Do not modify files, git state, configuration, credentials, services, or external systems.
Do not install packages.
Do not run commands that mutate the repository or environment.
Return findings and evidence only.
```

This prompt is a policy instruction, not a sandbox guarantee. Verify the runtime's actual sandbox or permission settings before relying on it.

## 8. Writable work

Do not use parallel writers during the pilot. A future writable task requires:

- explicit approval;
- disjoint logical write sets;
- dedicated branches or worktrees;
- one owner for lockfiles, migrations, generated files, shared schemas, and shared configuration;
- no automatic merge;
- parent-owned integration and verification.

A worktree isolates checkout state but does not make overlapping logical changes independent.

## 9. Failure handling

Only `succeeded` is a successful task state. Treat the following as mechanical failure, not substantive output:

```text
failed
cancelled
timed_out
stale
orphaned
lost
```

Check output truncation fields before accepting a result. Do not convert a missing participant, authentication failure, timeout, empty output, or malformed JSON into consensus.

Retry only after changing an identified cause. Do not recursively increase agent count after repeated uncertainty.

## 10. Installation and updates

The skill must not install or upgrade the CLI automatically. Use a pinned version, review upstream changes, and update the pin deliberately.

Pilot install command:

```bash
npm install -g @backnotprop/orchestrator-cli@0.1.0
```

Before changing the version:

1. review release notes and diff;
2. recheck runtime arguments, sandbox defaults, environment handling, task-store format, and license;
3. run `doctor`, one dry read-only task, timeout handling, interrupt handling, and truncation checks;
4. update `SOURCE.md` and the skill metadata.
