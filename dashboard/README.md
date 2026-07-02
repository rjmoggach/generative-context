# dashboard — production viewer (v1.0-c)

A read-only, self-contained viewer for a generative-wrangler production. It renders a
`production-{show}.json` manifest (the file the `production` skill / `production-coordinator`
build) as a review board: assets, sequences and shots with thumbnails, status, cost, and the
gaps to close. Clicking any image opens it full-screen (clean, no chrome — Esc or click to
dismiss).

**It is not part of the plugin.** The plugin (`context/`, `skills/`, `plugin/`) stays pure-text;
this is an isolated sibling app. Nothing here is packaged into `generative-wrangler.plugin`.

## Use it

Open `index.html` in a browser, then:

- **Open production folder** — pick a working folder that contains a `production-{show}.json`
  and its `assets/`. Read-only via the File System Access API; resolves thumbnails and full
  images. Needs Chrome or Edge (Cowork's browser works).
- **Load sample** — renders the bundled `sample/` (the real v0.10.0 ironworker smoke-test),
  works in any browser and offline. Good for a first look.
- **Drop** a `production-{show}.json` anywhere on the window — renders the board (thumbnails
  resolve only when the images are reachable, e.g. via the folder picker).

No build step, no dependencies, no server. One HTML file + the sample.

## Scope

- **Read-only.** Approvals are set by telling the `production-coordinator`, which writes the
  manifest's `human` block; this viewer reflects it. (Write-back from the UI is a possible
  later step.)
- Design: dark, colour-neutral "edit-bay" treatment so thumbnails read true. Type: Archivo +
  IBM Plex Mono. Crafted with the `impeccable` skill.
