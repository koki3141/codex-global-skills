---
name: local-results-dashboard-packaging
description: Package local experiment results into inspectable Markdown or HTML dashboards with working PNG, SVG, and MP4 media. Use when local result media must render in VS Code Markdown Preview, when a video shows 0:00, or when a dashboard must preserve run provenance.
---

# Local Results Dashboard Packaging

## Goal

Turn local experiment outputs into reader-facing inspection artifacts while
preserving provenance. A dashboard or Markdown gallery is a derived inspection
layer, not the raw research-data source of truth.

## Output Rules

- Keep large raw experiment data in its run directory unless project policy
  says otherwise.
- Record the source run path, command, commit hash, and dirty status.
- Copy only reviewed preview media into a dashboard-owned media directory.
- Use relative paths inside the dashboard package so it remains movable.
- Verify every referenced local file instead of trusting rendered placeholders.

## VS Code Markdown Media

VS Code Markdown Preview runs in a restricted Webview. Media references that
leave the Markdown directory tree can fail even when the path exists.

1. Put the Markdown entrypoint and derived media under one tree, for example:
   `gallery/index.md` and `gallery/media/<case>/`.
2. Embed MP4 with HTML5 and a same-tree relative path:

   ```html
   <video controls loop muted playsinline preload="metadata" width="100%" src="media/case/trajectory.mp4">
     Video playback is unavailable. Open the MP4 link below.
   </video>
   ```

3. Add a normal Markdown link to the MP4 immediately after the element.
4. Embed PNG/SVG using relative Markdown image syntax.
5. Encode browser-compatible MP4 as H.264 with `yuv420p` and
   `-movflags +faststart`.
6. For an existing compatible MP4, move metadata without re-encoding:

   ```bash
   ffmpeg -i input.mp4 -codec copy -movflags +faststart output.mp4
   ```

7. Confirm the `moov` atom precedes `mdat`; a player that remains at `0:00`
   has not passed review.

## Dashboard Contents

Include the case name, model/configuration, stage, seed or run identifier,
commit provenance, metrics, selected figures/videos, and an explicit claim
boundary. Packaging does not upgrade a smoke run into publication evidence.

## Verification

- Check that all local Markdown/HTML media paths resolve inside the package.
- Use `ffprobe` to verify codec, pixel format, and positive duration.
- Check MP4 atom order or test metadata loading and seeking in the target
  preview surface.
- Open the actual Markdown Preview or dashboard and reject broken placeholders,
  `0:00` players, missing images, and non-seekable video.
- Report the entrypoint, source runs, copied media, tests, and remaining limits.
