# Android Local-First MCP Checklist

## Architecture

- Keep Ktor/MCP routing thin: auth, request parsing, lifecycle, error envelopes, and delegation only.
- Keep assistant context construction separate from transport. Prefer service/DTO/codec boundaries when logic grows.
- Keep OpenAPI, REST, and MCP tool schemas aligned with actual JSON.
- Preserve `/api/history` and `/api/nutrition` array contracts unless the user explicitly approves a breaking change.
- Make future relay context explicit with small value types such as transport and disclosure profile.

## Room and Data Correctness

- Add foreign keys and indices with migration tests, not just entity annotations.
- During migrations, copy child rows only when valid parents exist; use JOINs or parent-first cleanup.
- Run or add `PRAGMA foreign_key_check` in instrumentation tests after migration.
- Normalize receipt dates with an explicit timezone policy.
- When date filters are provided, exclude rows whose dates cannot be normalized unless the API explicitly documents a diagnostic bucket.
- Keep SQL-level bounds where practical for `limit`, `offset`, and `sinceEpochMillis`; avoid unbounded full-table reads on common paths.

## MCP, REST, and Relay Security

- Bind development servers to loopback unless the user intentionally asks for external exposure.
- Use Bearer for local Actions/generic clients and OAuth-style auth for production ChatGPT Apps/relay paths.
- Treat query tokens as local-debug only; never document them as the tunnel/relay path.
- Bound request bodies and SSE channels.
- Do not log raw MCP/REST request bodies that may include receipt data or tokens.
- Return generic external error messages; keep stack traces in local logs only.
- Stop server coroutine jobs and close active channels on shutdown.

## External Data Disclosure

- Open Food Facts lookup by barcode or product name sends purchase-item-derived data to an external service.
- Make lookup user-initiated or clearly disclosed.
- Cache results locally and support cached/offline behavior where reasonable.
- Do not call purchase-history-derived signals medical diagnosis. Use recipe-planning language.

## ChatGPT and OpenAI

- For current ChatGPT Apps, Actions, MCP, or OpenAI API behavior, verify against official OpenAI docs.
- Distinguish Custom GPT Actions from ChatGPT Apps/MCP connectors:
  - Actions: OpenAPI plus API authentication.
  - Apps/MCP: HTTPS MCP endpoint, developer mode, and production-grade auth expectations.
- Keep relay docs clear: HTTPS/OAuth/request verification belongs in the relay; Room and images remain Android-local by default.

## Verification

Use the repo's real scripts. Common Android checks:

```bash
devbox run test
devbox run build
devbox run -- ./gradlew assembleDebugAndroidTest
python3 -m json.tool docs/chatgpt_actions_openapi.json
git diff --check
```

Run `connectedAndroidTest` only when an emulator/device is connected and the user expects runtime instrumentation, not just APK assembly.

## Git Hygiene

- Inspect `git status --short` before and after edits.
- Preserve unrelated user changes.
- Stage only after successful verification when the user asked for git整理 or staging.
- Commit/push only when explicitly asked.
