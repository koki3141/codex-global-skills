# LifeOS AI Tool Candidate DB Pattern

Use this reference when the user asks to evaluate, adopt, or keep track of AI/dev tools, especially from GitHub, t.co links, social posts, or trending lists.

## Core principle

Separate these claims before deciding adoption:

1. **Existence** — does the repo/package/page exist?
2. **Official provenance** — is it actually from the claimed organization or author?
3. **Function** — what class of tool is it: agent runtime, MCP/code graph, context compression, web extraction, observability, forecasting, Obsidian system, etc.?
4. **Side effects** — does it install wrappers, alter MCP/agent config, edit `AGENTS.md`/`CLAUDE.md`, start proxies, or send data externally?
5. **Adoption state** — adopted, sandbox_probe, sandbox_candidate, watch, candidate, reference_only, research_source, domain_candidate, infra_candidate, or rejected.

Do not merge an unverified provenance claim with a verified repo. Example: if the user says “Netflix Headroom” but the URL is `chopratejas/headroom`, keep `netflix-headroom` as an unverified watch item and add `headroom-ai` as the actual verified repo.

## Recommended LifeOS DB shape

For `$HOME/Documents/projects/lifeos-tools`, maintain all three formats:

- `data/ai-tool-candidates.sqlite` — queryable SSOT for agents/scripts
- `data/ai-tool-candidates.json` — editable structured copy
- `data/ai-tool-candidates.csv` — spreadsheet-friendly export
- `docs/ai-tool-candidates.md` — human-readable summary

Suggested table/JSON fields:

```text
id
name
url
category
source
evidence_status
adoption_status
decision
reason
risk
approved_usage
artifact
next_action
verified_at
notes
```

## Safety classifications

Prefer conservative states until side effects are understood:

- `adopted`: low-risk wrapper/reference already verified and used.
- `sandbox_probe`: a version-pinned probe exists and avoids install/config mutation.
- `sandbox_candidate`: promising, but no wrapper yet; evaluate only on public sample data.
- `watch`: provenance or usefulness unconfirmed.
- `reference_only`: useful design/example, but no code/template import yet.
- `research_source`: source of ideas/instructions only.
- `domain_candidate`: useful only when the relevant dataset/project exists.
- `infra_candidate`: useful for server/lab infra, too heavy for local LifeOS.

## High-risk commands to forbid by default

For agent/MCP/context-compression tools, do not run these without explicit approval and rollback plan:

```bash
<tool> install
<tool> wrap claude
<tool> wrap codex
<tool> proxy --port ...
<tool> learn
```

Reason: these may alter agent configs, route model traffic through a proxy, or write to `AGENTS.md` / `CLAUDE.md`.

## Evidence collection checklist

- Resolve short URLs with HEAD/GET and record the final URL.
- Query GitHub repo metadata: owner, license, stars, pushed_at, archived, homepage.
- Read README enough to identify modes and side effects.
- Check PyPI/npm metadata for package names and versions if the README advertises packages.
- Search for claimed organization provenance separately from repo existence.
- If license is missing or unclear, use `reference_only_no_direct_code_import_until_license_confirmed`.

## Report wording

Use calibrated wording:

- “確認できた範囲では…”
- “公式出自は未確認”
- “実体としての `<repo>` は別エントリで扱う”
- “sandbox限定候補”

Avoid saying a tool is official, safe, or adopted until the evidence gates pass.
