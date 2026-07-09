---
name: oracle
description: "This skill should be used when running Oracle second-model reviews with bundled prompts and files, including browser-mode diagnosis, debugging, refactoring, and design checks."
---

# Oracle (CLI) — best use

Oracle bundles the prompt + selected files into one “one-shot” request so another model can answer with real repo context (API or browser automation). Treat outputs as advisory: verify against the codebase + tests.

## Mandatory context-file rule

For any Oracle prompt, attach the file(s) that define the task context with `--file`. Do not send a prompt-only Oracle request when the answer depends on a note, source file, transcript, or prior artifact; include the target file itself and any referenced context files needed to understand the request.

## Main use case (browser, GPT‑5.5 Pro)

Default workflow here: `--engine browser` with GPT‑5.5 Pro in ChatGPT. This is the “human in the loop” path: it can take ~10 minutes to ~1 hour; expect a stored session for later reattachment.

Recommended defaults:

- Engine: browser (`--engine browser`)
- Model: GPT‑5.5 Pro (either `--model gpt-5.5-pro` or a ChatGPT picker label like `--model "5.5 Pro"`)
- Attachments: directories/globs + excludes; avoid secrets.

## Local invocation rule

In this environment, use the installed `oracle` command when it is available:

```bash
command -v oracle
oracle --version
```

If `oracle` is not on `PATH`, use the absolute path:

```bash
$HOME/Library/pnpm/oracle --version
```

Expected version: `0.15.0` or newer. Use the same binary for dry-run and the real run. Do not fall back to `npx -y @steipete/oracle` just because `oracle` is missing from `PATH`; `npx` can resolve an older package version and change browser/login/model-picker behavior.

Known-good browser invocation:

```bash
oracle --engine browser --browser-manual-login --browser-keep-browser --browser-input-timeout 120000 -p "<task>" --file "src/**"
```

If `oracle` is unavailable, replace `oracle` in the command above with `$HOME/Library/pnpm/oracle`.

## Browser Login Recovery

Use this path when browser mode fails with either of these errors:

- `ChatGPT session not detected. Login button detected on page`
- `No ChatGPT cookies were applied`

Do not keep retrying the same normal browser command. If `--copy-profile` reports that no cookies were applied, the copied Chrome profile did not provide a usable ChatGPT session for Oracle.

First confirm the failure and stage:

```bash
oracle status --hours 24
oracle session <slug> --render
```

Then run a manual-login smoke test in the Oracle-controlled browser:

```bash
oracle --engine browser --browser-manual-login --browser-input-timeout 120000 --model gpt-5.5-pro --timeout 10m --wait --no-notify --slug oracle-manual-login-smoke --write-output /private/tmp/oracle-manual-login-smoke.md --prompt "Reply only: OK"
```

If the visible browser asks for ChatGPT login, complete it there. A successful run should return only `OK`.

After this error class is observed, keep `--browser-manual-login --browser-input-timeout 120000` on real browser runs instead of switching back to normal mode:

```bash
oracle --engine browser --browser-manual-login --browser-input-timeout 120000 --model gpt-5.5-pro --timeout 60m --wait --no-notify --slug "<slug>" -p "<task>" --file "<context-file-or-glob>"
```

On Oracle 0.15.0 these manual-login flags are accepted even when they are not shown in the normal `--help --verbose` option list.

## Golden path (fast + reliable)

1. Pick a tight file set (fewest files that still contain the truth).
2. Preview the outgoing bundle (`--dry-run` + `--files-report` when needed).
3. Run in browser mode for the usual GPT‑5.5 Pro ChatGPT workflow; use API only when explicitly requested.
4. If the run detaches/timeouts: reattach to the stored session (don’t re-run).

## Commands (preferred)

- Show help (once/session):
  - `oracle --help`

- Preview (no tokens):
  - `oracle --dry-run summary -p "<task>" --file "src/**" --file "!**/*.test.*"`
  - `oracle --dry-run full -p "<task>" --file "src/**"`

- Token/cost sanity:
  - `oracle --dry-run summary --files-report -p "<task>" --file "src/**"`

- Startup/perf trace:
  - `oracle --perf-trace --perf-trace-path /tmp/oracle-perf.json --dry-run summary -p "<task>" --file "src/**"`
  - Use when CLI startup or time-to-first-output feels slow; inspect `first-output` and `exit`.

- Browser run (main path; long-running is normal):
  - `oracle --engine browser --model gpt-5.5-pro -p "<task>" --file "src/**"`

- Manual paste fallback (assemble bundle, copy to clipboard):
  - `oracle --render --copy -p "<task>" --file "src/**"`
  - Note: `--copy` is a hidden alias for `--copy-markdown`.

## Attaching files (`--file`)

`--file` accepts files, directories, and globs. Pass it multiple times when useful; entries can be comma-separated.

- Include:
  - `--file "src/**"` (directory glob)
  - `--file src/index.ts` (literal file)
  - `--file docs --file README.md` (literal directory + file)

- Exclude (prefix with `!`):
  - `--file "src/**" --file "!src/**/*.test.ts" --file "!**/*.snap"`

- Defaults (important behavior from the implementation):
  - Default-ignored dirs: `node_modules`, `dist`, `coverage`, `.git`, `.turbo`, `.next`, `build`, `tmp` (skipped unless explicitly passed as literal dirs/files).
  - Honors `.gitignore` when expanding globs.
  - Does not follow symlinks (glob expansion uses `followSymbolicLinks: false`).
  - Dotfiles are filtered unless explicitly included with a pattern that includes a dot-segment (e.g. `--file ".github/**"`).
  - Default cap: files > 1 MB are rejected unless `ORACLE_MAX_FILE_SIZE_BYTES` or `maxFileSizeBytes` in `~/.oracle/config.json` is raised.

## Budget + observability

- Target: keep total input under ~196k tokens.
- Use `--files-report` (and/or `--dry-run json`) to spot the token hogs before spending.
- Use `--perf-trace` / `ORACLE_PERF_TRACE=1` for startup and first-output timing. Traces redact prompts, tokens, keys, cookies, and inline cookie payloads; detached API children write a session-suffixed sidecar trace.
- For hidden/advanced knobs: `oracle --help --verbose`.

## Engines (API vs browser)

- Auto-pick: uses `api` when `OPENAI_API_KEY` is set, otherwise `browser`.
- Browser engine supports GPT + Gemini only; use `--engine api` for Claude/Grok/Codex or multi-model runs.
- `--copy-profile <chrome-user-data-dir>`: reuse an **already signed-in** Chrome session with no manual login — copies the profile to a throwaway dir, launches with the real Keychain so its cookies decrypt, runs, then always deletes the copy. Failed/incomplete runs are deleted too, so they cannot be kept, reattached, or sent to an existing/remote browser. e.g. `oracle --engine browser --copy-profile "$HOME/Library/Application Support/Google/Chrome" -p "<task>"`. macOS/Linux; needs `rsync`.
- **API runs require explicit user consent** before starting because they incur usage costs.
- Browser attachments:
  - `--browser-attachments auto|never|always` (auto pastes inline up to ~60k chars then uploads).
  - Add `--browser-bundle-files --browser-bundle-format auto|zip` to upload many files as one bundle; ZIP bundles preserve original file bytes.
- Remote browser host (signed-in machine runs automation):
  - Host: `oracle serve --host 0.0.0.0 --port 9473 --token <secret>`
  - Client: `oracle --engine browser --remote-host <host:port> --remote-token <secret> -p "<task>" --file "src/**"`

## API preflight

- API runs require explicit user consent and cost money.
- Before API runs, check provider readiness without printing secrets:
  - `oracle doctor --providers --models gpt-5.4,claude-4.6-sonnet,gemini-3-pro`
  - `oracle --preflight --models gpt-5.4,gemini-3-pro`
  - `oracle --route --model gpt-5.4`
- If the user wants first-party OpenAI, pass `--provider openai` or `--no-azure`. This prevents exported Azure env/config from hijacking the route:
  - `oracle --provider openai --engine api --model gpt-5.5-pro ...`
- For advisory multi-model panels where partial success is useful, use `--allow-partial --write-output <path>` so successful model files and the `<stem>.oracle.json` manifest are easy to recover:
  - `oracle --models gpt-5.4,claude-4.6-sonnet,gemini-3-pro --allow-partial --write-output /tmp/panel.md -p "<task>"`
- `--timeout 10m` is the normal user-facing API deadline; Oracle derives the HTTP transport timeout unless `--http-timeout` is explicitly set.
- If the exported `OPENAI_API_KEY` is invalid and the user wants their personal OpenAI key, use `$one-password` in one persistent tmux session. Known item: `API Key - OpenAI - Personal`, field `api_key`. Inject only into the single Oracle command; never print the key:
  - `OPENAI_API_KEY="$(op item get 'API Key - OpenAI - Personal' --account my.1password.com --fields label=api_key --reveal)" oracle --provider openai --engine api --model gpt-5.5-pro ...`
- For debugging Oracle itself, prefer the local checkout after pulling `~/Projects/oracle`:
  - `pnpm -C ~/Projects/oracle run build`
  - `node ~/Projects/oracle/dist/scripts/run-cli.js ...`

## Sessions + slugs (don’t lose work)

- Stored under `~/.oracle/sessions` (override with `ORACLE_HOME_DIR`).
- Browser runs save durable files under `~/.oracle/sessions/<id>/artifacts/`, including `transcript.md`, Deep Research reports, and downloaded ChatGPT-generated images when available.
- Runs may detach or take a long time (browser/API + GPT‑5.5 Pro often does). If the CLI times out: don’t re-run; reattach.
  - List: `oracle status --hours 72`
  - Attach: `oracle session <id> --render`
- Use `--slug "<3-5 words>"` to keep session IDs readable.
- Duplicate prompt guard exists; use `--force` only when a fresh run is intentional.
- CLI guardrails: root runs without a prompt exit nonzero; `--dry-run` conflicts with `--render` / `--render-markdown`; Ctrl-C exits foreground API runs with code 130 while browser cleanup/reattach still runs.

## Prompt template (high signal)

Oracle starts with **zero** project knowledge. Assume the model cannot infer the stack, build tooling, conventions, or “obvious” paths. Include:

- Project briefing (stack + build/test commands + platform constraints).
- “Where things live” (key directories, entrypoints, config files, dependency boundaries).
- Exact question + prior attempts + the error text (verbatim).
- Constraints (“don’t change X”, “must keep public API”, “perf budget”, etc).
- Desired output (“return patch plan + tests”, “list risky assumptions”, “give 3 options with tradeoffs”).

### “Exhaustive prompt” pattern (for later restoration)

For a long investigation, write a prompt that can stand alone later:

- Top: 6–30 sentence project briefing + current goal.
- Middle: concrete repro steps + exact errors + prior attempts.
- Bottom: attach _all_ context files needed so a fresh model can fully understand (entrypoints, configs, key modules, docs).

To reproduce the same context later, re-run with the same prompt + `--file …` set (Oracle runs are one-shot; the model doesn’t remember prior runs).

## Safety

- Don’t attach secrets by default (`.env`, key files, auth tokens). Redact aggressively; share only what’s required.
- Prefer “just enough context”: fewer files + better prompt beats whole-repo dumps.
