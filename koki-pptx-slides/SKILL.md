---
name: koki-pptx-slides
description: This skill should be used when creating, revising, or reviewing the user's personal PowerPoint/PPTX research slides, especially high-density Japanese lab-briefing, ROBOMECH-style, thesis, proposal, or source-backed technical decks.
---

# Koki PPTX Slides

## Purpose

Use this skill for the user's own slide style: dense, source-backed, editable
PowerPoint/PPTX slides for research explanation. This is not a generic
corporate slide style. It prioritizes argument density, evidence hierarchy,
native PowerPoint editability, and the user's preferred white / gray / dark-gray
visual language.

For detailed style rules, read `references/koki-pptx-style.md` before creating
or revising the deck.

## Workflow

1. Define the communication job in one sentence: who needs to understand what,
   and which evidence makes that conclusion credible.
2. Write a slide map before authoring. Each slide needs one role, one claim, a
   distinct evidence function, and one bottom conclusion. Merge or delete slides
   that answer the same question.
3. Build the deck around `claim -> evidence -> interpretation -> conclusion`.
   Use section labels such as `研究背景`, `研究目的`, and `実験方法`, but do not
   force the deck to have only three slides.
4. Preserve high-value density: numbers, constraints, cited figures, mechanisms,
   comparison conditions, equations, evaluation metrics, action rules, and saved
   artifacts. Remove duplicated definitions, repeated paraphrases, vague side
   notes, and hierarchy confusion.
5. Use source-backed images or editable native PowerPoint shapes. Do not use
   generated images as final factual evidence. Generated slide images may be
   used only as composition references.
6. Use PowerPoint-native text underlines for causality and emphasis. Do not draw
   separate underline shapes.
7. Keep body/evidence text at 16 pt or larger. Captions, source lines, page
   markers, and citations may be 8-10 pt.
8. Render and inspect the final deck. Fix overlap, clipping, small evidence
   text, orphan punctuation, unnatural line breaks, repeated slide roles, and
   weak source traceability before delivery.
9. When the deck is stored in a Vault or repository that excludes non-source
   binaries, keep the PPTX in Google Drive or another document store and commit
   only links, source notes, provenance, and editable support files.

## Personal Style Rules

- Use white, gray, and dark gray as the base system. The final conclusion bar is
  dark gray, darker than the title header, but not pure black.
- Reserve red/blue for temperature or result emphasis and brown for soil or
  domain-specific material. Do not use color as the primary logic system.
- Show causality with text hierarchy, position, arrows/down-cues, bold text, and
  native underlines.
- Use boxes only for substantial evidence groups, not for every causal phrase or
  small sub-conclusion.
- Prefer compact noun phrases for evidence blocks. Keep full sentences for the
  slide claim, major transition, or bottom conclusion.
- Use field-scale or repeated-use source photos for unfamiliar real-world
  techniques when scale matters. A single close-up is not enough when the
  audience needs to understand repeated deployment or field layout.
- Do not claim that prior experiments, simulations, or models are absent until
  the relevant primary literature or source documents have been searched. If a
  prior study covers part of the axis, show it as a positive existing result and
  narrow the remaining gap.

## Method And Simulation Slides

- Present the experimental contract before detail panels: domain, initial
  conditions, boundary conditions, agent/action constraints, comparison
  conditions, and evaluation metrics.
- Use one figure for one function. Full-domain figures are for environment,
  boundary, and initial conditions; local action rules should show only the
  local neighborhood needed for the action.
- Align grid lines to physical cell size when a grid represents computation.
  Label units such as `[mm]`, `[K]`, and `[-]`. If a table is only a compressed
  schematic, state that it is not the computation grid.
- Put numerical boundary values and equations near the boundary or object they
  define. Do not decorate equations with standalone boxes unless the box is a
  real table cell or method region.
- For Move / Pick / Drop or similar action rules, show valid executable
  candidates by default. Show rejection examples only when rejection is the
  slide's point.

## Handoff

Return the PPTX path or Drive link, the key files updated, and the verification
commands that passed. Mention remaining uncommitted or unrelated changes when
working inside a dirty repository.
