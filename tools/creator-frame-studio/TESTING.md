# Testing notes

## Current GitHub edition

The GitHub edition splits the single-file beta into `index.html`, `styles.css` and `app.js` and replaces embedded personal demo photos with generated local demo artwork.

Static smoke checks live in `tests/smoke.mjs` and run in GitHub Actions.

They verify:
- the three-file app wiring,
- JavaScript syntax,
- the expected creator-tool surface,
- all current preset IDs,
- export/project functions,
- removal of embedded personal demo photos.

## What this does not prove

A static smoke test does not prove that every pointer gesture, browser download, ZIP export or mobile browser behaves correctly. Interaction testing belongs in the next CI step.

The earlier single-file v0.2 beta was exercised in a local browser-oriented test harness before this repository packaging step. Do not treat that earlier run as independent verification of this split GitHub build.

## Manual release checklist

1. Load the generated sample project.
2. Import at least one PNG, JPEG and WebP.
3. Drag, zoom and switch fit/cover.
4. Test 4:5, 3:4, 1:1, landscape and 9:16.
5. Add a text layer and deliberately move it outside the guide.
6. Run “fit text” and verify the warning clears.
7. Export PNG/JPEG/WebP.
8. Export a multi-format ZIP and inspect every image.
9. Save a project, reload the page and reopen it.
10. Repeat on desktop and mobile browsers before marking a release stable.
