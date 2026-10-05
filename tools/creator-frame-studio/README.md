# Creator Frame Studio

**A browser-only framing, safe-area review and multi-format export workspace for creators.**

[Türkçe README](README_TR.md) · [Roadmap](ROADMAP.md) · [Testing](TESTING.md) · [Content pack](CONTENT-PACK.md)

> **Status:** v0.3.0 beta. The tool is useful today, but it is not presented as an official Instagram validator or an AI design judge.

## What it solves

A design can look good in the editor and still lose important text, faces or calls to action after it is reframed for another surface. Creator Frame Studio gives creators one local workspace to:

- place and reframe source images without regenerating them,
- preview multiple social-media canvases,
- add editable text layers,
- apply one-click Hook / Subtitle / CTA text styles,
- switch between Balanced / Hook-focus / CTA-focus editorial guide profiles,
- review a deterministic preflight readiness summary alongside detailed checks,
- review conservative inner-area guides,
- simulate common crop views,
- export single images or a multi-format ZIP,
- save and reopen local project files.

## Canvas presets

| Platform | Preset | Canvas |
| --- | --- | ---: |
| Instagram | Portrait / carousel | 1080 × 1350 · 4:5 |
| Instagram | Tall portrait | 1080 × 1440 · 3:4 |
| Instagram | Square | 1080 × 1080 · 1:1 |
| Instagram | Landscape | 1080 × 566 · ≈1.91:1 |
| Instagram | Story | 1080 × 1920 · 9:16 |
| Instagram | Reels cover canvas | 1080 × 1920 · 9:16 |
| Instagram | Profile / Highlight working canvas | 1080 × 1080 with circle preview |
| Pinterest | Standard Pin | 1000 × 1500 · 2:3 |
| YouTube | Video thumbnail | 3840 × 2160 · 16:9 |
| YouTube | Shorts thumbnail canvas | 2160 × 3840 · 9:16 |
| YouTube | Lightweight thumbnail canvas | 1280 × 720 · 16:9 |
| Any | Custom | 64–4096 px per side, within the tool limit |

The presets are **working canvases**, not a claim that every publishing route accepts every format. Platform UI and crops can change.

## Run locally

Clone the toolkit and open the tool:

```bash
git clone https://github.com/alptugharun/ai-social-media-toolkit.git
cd ai-social-media-toolkit/tools/creator-frame-studio
```

Open `index.html` in a modern browser. The application does not need an API key or account login.

## Privacy model

The app is intentionally local-first:

- no model/API call,
- no social login,
- no analytics request,
- no upload endpoint,
- no source-image regeneration.

The page Content Security Policy blocks network connections. Project and export files are created in the browser.

## Current limits

- Safe-area guides are editorial/conservative guides, **not official universal safe zones**.
- Rasterized text inside an uploaded image is not automatically detected or moved.
- There is no OCR, face detection, aesthetic score, virality score or publishing automation.
- Story/Reels UI overlays are simulations; verify the final publishing screen.
- Multi-format export reframes the composition; inspect each result before publishing.

## Source layout

```text
tools/creator-frame-studio/
├── index.html
├── styles.css
├── app.js
├── README.md
├── README_TR.md
├── ROADMAP.md
├── TESTING.md
├── CONTENT-PACK.md
└── tests/
    └── smoke.mjs
```

## Why it belongs in this toolkit

This repository is about practical, testable creator workflows. Creator Frame Studio is a concrete browser tool: it turns format and framing guidance into an inspectable workflow instead of another prompt card.

Built by **Alptuğ Harun**.

## v0.3 creator workflow upgrade

The v0.3 iteration adds faster creator-side decisions without pretending to be an AI design judge. Quick text styles, editorial guide profiles and the readiness card are deterministic layout helpers. They do not inspect aesthetic quality, faces, embedded raster text or platform ranking potential.
