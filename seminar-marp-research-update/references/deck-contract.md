# Deck Contract

## Recommended sequence

| slide | purpose |
| --- | --- |
| 1 | literal research title, date, presenter |
| 2 | old framing versus new framing |
| 3 | one-sentence objective |
| 4 | causal chain and unavailable global information |
| 5 | formation/evaluation or intervention/measurement separation |
| 6--8 | geometry, physics, boundary conditions, controls |
| 9 | primary endpoint and validity gates |
| 10 | completed evidence and explicit claim boundary |
| 11 | method hierarchy or proposed contribution |
| 12 | current status with timestamps |
| 13 | next decisions |
| final | seminar questions |

## Evidence labels

- `complete`: a present artifact and its required checks passed.
- `running`: process is active; no result claim.
- `capability only`: execution path works, effectiveness is untested.
- `open`: required work has not started or a gate remains unresolved.
- `invalid`: a declared gate failed; do not repair or relabel the run.

## Visual QA

When a screenshot or rendered reference is supplied, first record its observable
layout features: top/bottom bands, content origin, outer margins, bullet glyphs,
indent depth, title weight, dominant colors, and approximate density. Reproduce
those features before adding decorative components of your own.

If the top band is the heading container, the heading text must render inside
the band on every ordinary slide. An empty band combined with a duplicate
bullet-style heading in the body fails the reference match.

For local MP4 evidence, use an HTML `<video>` element only with a valid poster.
The HTML build must retain the source path and controls; the PDF must show the
poster without clipping. MP4 playback is an HTML deliverable, not a PDF claim.

Reject the deck if any item is true:

- clipped text, equation, table, or image;
- body copy too small to read on the contact sheet;
- figure without an evidence status or source context;
- inconsistent colors or more than two dominant accent families;
- decorative layout that obscures the research decision;
- incomplete run displayed as a result;
- generated HTML/PDF missing a referenced local asset.

The contact sheet is a triage surface, not final proof. Open dense pages at original resolution before acceptance.
