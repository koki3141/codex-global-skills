---
name: seminar-marp-research-update
description: Create or revise a Japanese research-seminar deck in Marp when the user needs to explain a changed research theme, proposal, experiment design, or evidence status. Use repository sources of truth, optional PowerPoint THMX styling, local figures, claim-boundary labels, speaker notes, Nix-based HTML/PDF rendering, and all-slide visual QA.
---

# Research Seminar Marp

## Workflow

1. Read the project governance file and the canonical research source before drafting.
2. Separate confirmed design, completed evidence, running work, and future work. Never present capability smoke or an active run as a scientific result.
3. Start from the thesis-seminar palette in `assets/default-seminar-theme.css`: near-black body text, white headings inside a dark-gray top band, and dark-gray secondary text. Copy the CSS into the deck's `style: |` block. If the user explicitly supplies a different `.thmx`, run `scripts/extract_thmx_theme.py` and translate its color/font scheme into Marp CSS. If a rendered screenshot is also supplied, inspect it directly and reproduce its band height, whitespace, heading hierarchy, bullet shape, and alignment; do not stop at color/font extraction. Treat both inputs as styling, not research evidence.
   - When the reference uses a top band as the slide heading region, place every slide heading inside that band. Do not duplicate it as a bullet-like heading in the body.
4. Build the argument in this order:
   - what changed and why;
   - research gap and objective;
   - causal chain;
   - operational definitions and experimental separation;
   - geometry, physics, controls, and primary endpoint;
   - evidence status and claim boundary;
   - next decision and discussion questions.
5. Use local figures that reveal the actual geometry, field, result, or workflow. Add a source/status caption. Do not use decorative stock images.
   - For Marp HTML, local MP4 evidence may be embedded with `<video controls playsinline>` when `html: true`. Always provide a local `poster` image because PDF export is static; verify the MP4 codec and the generated HTML source.
6. Verify every displayed constant, equation, condition, run state, and result against the current code, test, config, manifest, or reviewed report that owns it. Do not copy a value from an older slide when the executable contract has changed.
7. Add concise speaker notes in Marp HTML comments. Keep the visible slide usable without narration.
8. Run `scripts/render_marp_nix.sh DECK.md OUTPUT_DIR`. Treat the Markdown source as canonical and regenerate HTML, PDF, and contact sheet together. Inspect the contact sheet at full size, compare it with any supplied visual reference, then inspect every dense or suspicious page individually.
9. Fix overflow, missing media, low contrast, tiny text, source/render drift, and unsupported claims. Rebuild until the rendered PDF is clean. Preserve the last visually accepted artifacts if the renderer or host font stack fails.

## Content Rules

- Default text colors are body `#111111`, top-band heading `#ffffff`, and secondary text `#555555`; the top band is `#5b5b5b`. Table headers use white text on the same dark-gray family. Use status colors only for status meaning: complete `#176b4d`, running `#4f4f4f`, and open `#8b3f18`.
- One message per slide; normally 12--16 slides for a 10--15 minute seminar.
- Prefer a diagram, equation, table, or real result over paragraph-heavy prose.
- Keep body text at 20 px or larger unless a source note requires smaller text.
- Show equations only when the audience needs them for the decision being discussed.
- Label evidence as `complete`, `running`, `capability only`, `open`, or `invalid`.
- End with 2--3 concrete questions that the seminar can resolve.
- For a major theme change, make the old-to-new distinction explicit on slide 2.

Read `references/deck-contract.md` when choosing slide structure, evidence labels, and visual QA criteria.
Read `references/source-render-sync.md` when updating an existing deck or committing generated review artifacts.
Use `assets/default-seminar-theme.css` as the default CSS source when no different theme is explicitly requested.

## Commands

```bash
python3 scripts/extract_thmx_theme.py /path/to/theme.thmx
scripts/render_marp_nix.sh /absolute/path/deck.md /absolute/path/output
```

The renderer uses `nix run nixpkgs#marp-cli` and Nix-provided Poppler/ImageMagick. Do not silently fall back to host-global npm, Chromium, or PDF tools.
