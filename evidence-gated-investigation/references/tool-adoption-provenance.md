# Tool Adoption Provenance Checks

Use this reference when evaluating a newly-trending developer, AI, MCP, agent, or infra tool for inclusion in a user project.

## Goal

Separate three different claims before acting:

1. The tool exists.
2. The tool is official / from the claimed organization.
3. The tool is safe and appropriate to adopt in this environment.

Do not collapse these into one conclusion. A tool may be real but unofficial, official but too risky to install, or useful but only safe as a watch item.

## Evidence gates

### Official provenance

Check at least two of:

- Exact GitHub org/repo exists via GitHub API or GitHub page.
- The repo appears under the claimed organization's repository list/search.
- The official homepage, docs, blog, release note, or package registry links back to the repo.
- License and owner metadata match the claim.

If exact repo paths such as `Org/tool`, `org/tool`, or `Org-Skunkworks/tool` 404, do not say the tool is official yet. Mark it `unverified` or `watch_only`.

### Safety for local project inclusion

Before adding a tool to a project:

- Prefer metadata/documentation first; avoid running installers.
- Reject `curl | sh` and auto-installers unless the user explicitly approves.
- For MCP/agent/code-index tools, assume `install` may edit agent config until proven otherwise.
- Prefer version-pinned one-shot execution such as `npx -y package@version --help` or a sandbox probe.
- Refuse direct indexing of high-value stores such as the Hermes profile or Obsidian vault unless explicitly scoped.
- Record risk and approved usage: `adopted`, `sandbox_probe_only`, `watch_only`, or `rejected`.

## Recommended output shape

```md
## 結論
- Adopt / sandbox only / watch only / reject

## 確認済み
- repo/package metadata
- official source links
- license / update status

## 未確認
- official provenance gaps
- install/config side effects

## 反映
- files/scripts/config changed, if any

## 禁止
- commands not to run yet
```

## Pattern from LifeOS AI tool radar

When a user reports a new tool but official provenance is not confirmed:

1. Search exact repository candidates and organization repository filters.
2. Check package registries only for metadata, not installation.
3. Add the tool to an allowlist as `watch_only_until_official_repo_or_release_note_is_verified`.
4. Add a manual watch item to any recurring radar script.
5. Do not create wrappers, install MCP servers, or alter agent config until the official source is verified.
