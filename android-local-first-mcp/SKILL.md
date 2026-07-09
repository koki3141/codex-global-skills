---
name: android-local-first-mcp
description: This skill should be used when the user asks to build, review, harden, or refactor a Kotlin Android local-first app that exposes device-local data through MCP, ChatGPT Actions, REST/OpenAPI, Open Food Facts, Room, Health Connect/Google health integrations, or a future HTTPS/Cloudflare relay. Use for requests like "clean architecture", "super engineer code", "MCP/ChatGPT integration", "Cloudflare relay readiness", "Room migration safety", or "official OpenAI docs check" in Android app development.
---

# Android Local-First MCP

## Goal

Keep Kotlin Android work local-first, contract-stable, and relay-ready while preserving clean architecture boundaries. Treat public HTTPS, OAuth, and tunnel concerns as transport/auth layers unless the user explicitly asks for cloud sync.

## Default Workflow

1. Inspect before editing: `git status --short`, app architecture, DI, Room entities/DAOs/migrations, API docs, and tests.
2. Identify the contract surface: Android UI, Room schema, REST/OpenAPI, MCP tools, JSON response shape, and any external data disclosure.
3. Keep source of truth local: Room and private app files stay on device by default; relay code must not become an unplanned cloud database.
4. Separate boundaries:
   - UI/ViewModel for interaction state.
   - Repository/DAO for persistence and network fetches.
   - Assistant/query service for bounded context construction.
   - JSON/OpenAPI/MCP codecs for wire shape.
   - Ktor/MCP manager for auth, routing, SSE/HTTP lifecycle, and transport only.
5. Use official docs for OpenAI or ChatGPT behavior. Trigger `openai-docs` when current OpenAI product details affect the answer or code.
6. If the user asks for Oracle/Pro review, trigger `$oracle` and `$oracle-prompt-design`; attach relevant files and apply only concrete, scope-safe findings.
7. Validate with the repo's actual commands. Prefer existing `devbox`/Gradle scripts over invented tooling.

## Non-Negotiables

- Do not break existing ChatGPT Actions top-level response shapes without explicit approval.
- Do not expose receipt images, image bytes, or private local paths to assistant-safe contexts by default.
- Do not publish token-in-query flows for HTTPS tunnels or relays; keep Bearer/OAuth as the production path.
- Do not claim Health Connect, Google Fit, OpenAI, or ChatGPT capabilities from memory when official docs are needed.
- Do not rename application IDs or database filenames casually; treat them as migration/backup-affecting.
- Do not commit generated local DBs, APKs, tunnel URLs, API keys, or personal receipt exports.

## Detailed Checklist

Load `references/checklist.md` when doing a substantial implementation, review, or architecture cleanup.
