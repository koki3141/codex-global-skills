---
name: equation-traceability-workflow
description: Maintain equation traceability in the masters-thesis-shimohara-2027 workspace. Use when updating physical formulas, adding EQ_* IDs, connecting equations to C++ source and tests, generating LaTeX snippets, checking BibTeX references, or rendering the Sphinx equation registry with literalinclude code snippets.
---

# Equation Traceability Workflow

Use this skill for the parent workspace at:

`/Users/koki/Documents/projects/masters-thesis-shimohara-2027`

The durable policy is:

- Keep cross-repository equation metadata in the parent registry: `vault/equation-traceability.toml`.
- Keep generator/checker/docs tooling in `tools/equation-traceability/`.
- Keep simulator submodules buildable on their own; do not require Sphinx or thesis files for `termite-formula-sim` quality checks.
- Keep generated LaTeX snippets committed in the thesis submodule so thesis PDF builds remain self-contained.

## Before Editing

Read the relevant local rules before changing files:

- Parent: `AGENTS.md`
- Simulator: `termite-formula-sim/AGENTS.md`
- Thesis: `masters-thesis-pepper-shimohara-2027/AGENTS.md`

Check dirty state first:

```bash
git status --short
git -C termite-formula-sim status --short
git -C masters-thesis-pepper-shimohara-2027 status --short
```

Preserve unrelated dirty files. In this workspace, submodules are common and unrelated `heck2020a`, `test-termite-mound/`, or comparison-script changes should not be staged unless the user explicitly includes them.

## Add Or Repair An Equation

For each physical formula:

1. Add or update one `[[equations]]` entry in `vault/equation-traceability.toml`.
2. Use a stable `EQ_*_NNN` ID. Do not use LaTeX equation numbers as stable IDs.
3. Include `source_keys`, `latex_label`, `implemented_by`, `verified_by`, `latex_body`, `latex_intro_ja`, `sign_convention_ja`, and symbols.
4. Use only BibTeX keys that exist in `masters-thesis-pepper-shimohara-2027/refs/references.bib`.
5. Add `Traceability ID: EQ_*` comments to the relevant C++ physics function declarations or definitions.
6. Add the generated TeX input to `masters-thesis-pepper-shimohara-2027/src/03-method.tex`.
7. Generate the thesis TeX snippets.
8. Build or refresh the Sphinx page.

Prefer grouping tightly coupled formulas under one EQ entry when they form one physical relation in the implementation, for example conductance plus interface flux. Do not group unrelated subsystems just to reduce the number of IDs.

## Sphinx Code Display

The Sphinx page must display implementation and verification code with `literalinclude`, not copied code blocks.
Keep verification code collapsed by default. The reader-facing path is formula, implementation, and references; test code is evidence and should live inside a `Verification code` dropdown.
For references, show clickable `Reference links` before the raw BibTeX snippet. Derive DOI links as `https://doi.org/<doi>` from BibTeX `doi` fields, and show any BibTeX `url` field directly.

Expected page:

`http://127.0.0.1:8000/_generated/equations.html`

Expected generated Markdown:

`tools/equation-traceability/docs/_generated/equations.md`

Implementation details:

- Use line-range `literalinclude` directives for C++, tests, and BibTeX entries.
- Put test `literalinclude` blocks inside a Sphinx Design `{dropdown}` so they do not dominate the page.
- Resolve paths relative to `tools/equation-traceability/docs/_generated/`.
- Match C++ function names by exact function-call pattern, not substring, so `VaporDensity` does not match `SaturationVaporDensity`.
- Restrict implementation source discovery to `termite-formula-sim/src/physics`.

## Commands

From the parent workspace:

```bash
nix run ./tools/equation-traceability#generate
nix run ./tools/equation-traceability#check
nix run ./tools/equation-traceability#docs
nix run ./tools/equation-traceability#serve-docs
```

With uv:

```bash
cd tools/equation-traceability
UV_CACHE_DIR=/private/tmp/codex-uv-cache uv run equation-traceability generate --workspace ../..
UV_CACHE_DIR=/private/tmp/codex-uv-cache uv run equation-traceability check --workspace ../..
UV_CACHE_DIR=/private/tmp/codex-uv-cache uv run --group docs sphinx-build -b html docs docs/_build/html
UV_CACHE_DIR=/private/tmp/codex-uv-cache uv run pytest -q
```

For thesis validation:

```bash
cd masters-thesis-pepper-shimohara-2027
nix develop -c make pdf
```

If sandboxed Nix fails with daemon socket permission errors, rerun the same Nix command with the normal escalation flow. Treat Nix permission failure as an environment issue, not as failed research validation.

## Coverage Checks

The checker should fail when:

- a registry entry has a missing required field,
- a BibTeX key is missing,
- generated TeX is stale,
- `src/03-method.tex` does not input a generated equation snippet,
- source code does not mention the EQ ID,
- an `implemented_by` symbol is not found,
- an `implemented_by` symbol lacks an attached `Traceability ID: EQ_*` comment on its declaration or definition,
- a public `double` function under `termite-formula-sim/src/physics/*.h` is missing from the registry.

After building Sphinx, verify the page has multiple EQ headings and real code blocks. A browser DOM check should confirm at least:

- `EQ_HEAT_CONDUCTION_001`
- a non-heat equation such as `EQ_PSYCHROMETRICS_001`
- C++ implementation text such as `ConductiveHeatFluxIntoCell`
- BibTeX text such as `fourier1822theorie`

## Commit Boundaries

When the user asks for commits, keep the submodule settlement rule:

1. Commit simulator comment/source changes inside `termite-formula-sim`.
2. Commit generated TeX and `03-method.tex` inside `masters-thesis-pepper-shimohara-2027`.
3. Commit parent registry/tooling/handoff and updated submodule pointers in the parent repo.

Use the user's required commit-message style:

`{English prefix}: {Japanese message}`

Do not stage unrelated dirty files. Generated Sphinx HTML and generated Sphinx Markdown are build artifacts and should remain ignored unless the user explicitly requests committing them.
