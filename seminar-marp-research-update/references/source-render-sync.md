# Source and render synchronization

## Ownership

- The Marp Markdown file is the editable source of truth.
- HTML is the interactive review artifact and may contain local video playback.
- PDF is the static presentation/export artifact.
- The contact sheet is the whole-deck triage artifact, not final visual proof.
- Figures, posters, and videos remain evidence assets owned by the project; generated slide files do not upgrade their claim status.

## Update sequence

1. Read the current source, the last accepted render, and the project files that own every changed claim or displayed value.
2. Update the source and its speaker notes.
3. Verify constants, units, equations, geometry labels, conditions, timestamps, and evidence labels against code, tests, configs, manifests, or reviewed reports.
4. Render HTML, PDF, and contact sheet as one artifact set with `scripts/render_marp_nix.sh`.
5. Inspect the contact sheet, then open dense pages at original resolution. Check video poster behavior in PDF and video source/controls in HTML.
6. Commit the source and intentionally retained generated review artifacts together when the repository tracks them. Do not commit a newer source with stale HTML/PDF/contact sheet while describing the deck as rebuilt.

## Failure handling

The renderer stages a complete artifact set before replacing files in the output directory. If Marp, Chromium, Fontconfig, Poppler, or ImageMagick fails, keep the last visually accepted artifacts and report the failed rebuild separately.

Non-empty output is not visual acceptance. Reject or quarantine a fresh render if fonts, equations, media, page count, clipping, or layout differ unexpectedly. Do not overwrite accepted evidence merely because the command exited zero.

## Claim synchronization

When a slide shows implementation-controlled values, prefer a test or generated table that asserts the same values. If source code, test fixtures, and slide disagree, resolve the owning executable contract first; do not choose the visually convenient value.

For active or superseded runs:

- show `running` only while the process is confirmed active;
- show `complete` only after the required manifest and checks close;
- label old diagnostic media as superseded or pre-alignment when retained for explanation;
- never silently replace a failed or incomplete run with capability evidence.
