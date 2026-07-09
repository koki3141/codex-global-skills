---
name: proto-institution-swarm-workflow
description: Project workflow for /Users/koki/Documents/projects/proto-institution-swarm. Use when planning or implementing non-trivial C-PME, EIGI, IVP, simulation, analysis, paper, dashboard, literature, Oracle-review, or commit-by-commit research-software work in this repository, especially when protocol validity, TOML configs, C++/pybind11 bottleneck policy, claim boundaries, subagent orchestration, Zotero, or Google Drive evidence matter.
---

# Proto Institution Swarm Workflow

## Core Contract

Treat `AGENTS.md` as the source of truth. Before changing files, read it, the user's requested context file, `git status --short`, and the affected requirements, design, implementation-plan, paper, or report files. Preserve unrelated dirty work. Do not introduce submodules, global dependencies, API-engine Oracle, external storage, or source-code edits outside the requested scope.

Keep the theory boundary intact: robots store predictive memory atoms, prediction errors, exchange events, interventions, and analysis graphs. Terms such as institution, right-of-way, yield, rule, or priority belong only in post-hoc analysis, paper text, documentation, or dashboards.

## Planning Gate

For non-trivial implementation, protocol, metric, public API, directory-layout, or paper-claim changes, create or update `docs/implementation-plans/` from the repo template before coding. Make the plan commit-by-commit:

1. tooling or scaffold;
2. simulation core;
3. C-PME model logic;
4. EIGI / IVP analysis;
5. tests and fixtures;
6. paper or documentation;
7. reviewed small result summaries.

For each commit slice, state affected paths, architecture layer, protocol impact, data/artifact policy, validation commands, rollback notes, paper impact, and whether Oracle review is required. If a task is documentation-only or skill-only, explicitly mark code, protocol, paper, and raw experiment outputs unchanged.

## Implementation Defaults

Use Python 3.12, Nix, `uv`, `pytest`, `ruff`, NumPy/SciPy/Pandas, Torch, NetworkX, and TOML configs loaded into typed Python config objects unless the plan records a justified change. Prefer `configs/primary.toml` and `configs/ablations/` for experiment configs. Every run manifest should include commit SHA, config path, config hash, seed list, split, intervention replication count, command, start/end time, and output paths.

Add C++17 plus `pybind11` only after profiling shows a rollout or memory-lookup bottleneck, and keep a stable Python fallback. Add Parquet, Zarr, DVC, W&B, or object storage only after planning schema, locking, reproducibility, manifest, and storage impacts. Keep raw trajectories, checkpoints, videos, and repeated runs under ignored `experiments/`.

## EIGI / IVP Gates

Before treating an analysis result as evidence, check that the plan or report names the gate:

- fixed train/holdout or preregistered split;
- intervention labels and replication counts;
- paired or matched intervention comparisons where relevant;
- matched-null graph construction for EIGI claims;
- non-degradation or rejection criteria;
- manifest-backed provenance for every included run;
- equation traceability before paper-facing equations become strong claims.

If any gate is missing, label the result as a smoke run, diagnostic, implementation check, or hypothesis. Do not upgrade it to an institutional claim.

## Oracle Review

Use Oracle / ChatGPT Pro as advisory review when requirements, architecture, protocol validity, statistical claims, major design, analysis interpretation, or paper claims change. Always attach context files with `--file`; do not run prompt-only repo or research reviews. Store prompt, selected files, returned summary, adopted/rejected decisions, and follow-up actions under `docs/reviews/oracle/`.

Use `oracle-review-loop` only after a 100-point rubric has been fixed and approved by the user. It must use separate creator/evaluator sessions and stop at `FINAL_DECISION: PASS` or a concrete blocker. Treat Oracle output as advice and verify locally against files, tests, manifests, and run evidence.

## Subagent Orchestration

Use subagents only for separable, read-heavy or independently validatable work: one commit slice, module audit, literature pass, validation review, dashboard check, or paper-claim check per subagent. Pass raw files, commands, and acceptance criteria, not hidden conclusions. Require each subagent to report changed paths, validation output, unresolved risks, and unrelated dirty work it observed.

The parent agent owns final integration, writes that affect shared files, conflict resolution, validation commands, and acceptance decisions. If subagents are unavailable, perform the same checks serially and record that orchestration was local-only.

## Claims, Results, And Dashboards

Paper text, result summaries, and dashboards must distinguish:

- implementation status;
- smoke or diagnostic evidence;
- preregistered IVP evidence;
- matched-null EIGI evidence;
- reviewed paper-facing claims.

Put reviewed summaries and compact dashboards under `docs/reports/` or `paper/`; do not commit raw experiment data. A useful dashboard links the active implementation plan, requirements/design status, validation commands and results, run manifests, claim-to-evidence matrix, figures, equations, Oracle decisions, storage choices, performance notes, and unresolved risks.

## Literature Workflow

For literature or prior-work tasks, prefer source-backed retrieval over memory. Use Zotero first for the user's research library, then local `paper/refs.bib`, repo notes, and Google Drive docs/sheets/slides when the task depends on shared drafts or evidence tables. Preserve bibliographic provenance: cite item keys or document paths, distinguish direct source claims from synthesis, and update BibTeX or notes only when requested.

When literature evidence feeds Oracle, attach the actual source notes, PDFs, BibTeX, or Drive exports needed for review. Do not send secrets, credentials, cookies, or unnecessary private data.

## Closeout

Before final response or commit, run feasible validation from the plan, then inspect `git status --short` and `git diff --stat`. Report files changed, validation commands and outcomes, skipped checks, protocol/paper impact, raw artifact handling, and remaining risks.
