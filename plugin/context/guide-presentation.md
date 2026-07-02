# Presentation — Showing the Production to the Human

The review surface. The `production` skill and `production-coordinator` build the
`production-{show}.json` manifest (see `guide-production.md`); this guide covers how to
put it in front of the human to review - a visual board, a contact sheet, or a one-off
rendered page - without turning the plugin into an app. Used by the `production-coordinator`
when the ask is "show me" rather than "tell me."

Format: **Decision / Use when / Because / Prompt translation / Watch-outs / Anchors.**

> Presentation is read-only. The human reviews and decides; approvals and retakes are set by
> telling the coordinator, which writes the manifest's `human` block (`guide-production.md`
> §3). No presentation surface writes assets or the manifest.

---

## 1. The dashboard (the standing review board)

- **Use when:** the human wants to see the whole show at a glance - assets, sequences and
  shots with thumbnails, status, cost, and the gaps to close.
- **Because:** a JSON manifest is not a review surface; a board is. The repo ships a
  self-contained, read-only viewer at `dashboard/index.html` that renders any
  `production-{show}.json` - no build step, no server, not part of the plugin package.
- **Prompt translation:** point the human at it - "open `dashboard/index.html`, click *Open
  production folder*, and pick your working folder (the one with `production-{show}.json` +
  `assets/`)." It resolves thumbnails read-only via the File System Access API (Chrome/Edge),
  or *Load sample* / drop-a-JSON for a quick look. Clicking any image opens it full-screen.
- **Watch-outs:** the folder picker needs a Chromium browser; the manifest and its `assets/`
  must sit in the same working folder so paths resolve. It reflects the manifest - reconcile
  first (`production` skill) so it is current.
- **Anchors:** the production report / call sheet a coordinator posts for the team.

## 2. Contact sheets (dailies)

- **Use when:** reviewing a sequence's renders as a set, or handing off a printable/archivable
  sheet.
- **Because:** a contact sheet is the film-native way to judge coverage together - the board's
  thumbnails, laid out for a focused pass.
- **Prompt translation:** assemble the sequence's stills into one image offline (zero API cost)
  with ImageMagick, e.g. `montage assets/**/S2-*.png -tile 3x -geometry +8+8 -background '#14161a'
  contact-S2.png`, then show it. Order by shot label; label each tile.
- **Watch-outs:** ImageMagick is a local dependency, not shipped by the plugin; skip if
  unavailable and use the dashboard instead. Keep the background neutral so frames read true.
- **Anchors:** photographic contact sheets; editorial dailies.

## 3. On-demand rendered board (no standing app)

- **Use when:** the human wants the visual board *right now* in the chat/agent surface and does
  not want to open the dashboard app - or is in a host (e.g. Cowork) that can render an HTML
  artifact inline.
- **Because:** the board is just the manifest rendered; the agent can produce a one-off,
  self-contained HTML view from `production-{show}.json` on request and throw it away after.
  The plugin stays pure-text; the presentation is an agent action, not a shipped surface.
- **Prompt translation:** read the manifest, render a single self-contained HTML board
  (mirroring `dashboard/index.html`'s layout) as an artifact, and hand it over. Do not commit
  it to the repo.
- **Watch-outs:** this is a snapshot, not the live viewer; regenerate it after a reconcile.
- **Anchors:** the dashboard's own design (dark, colour-neutral, thumbnails read true).

## 4. Choosing a surface

- Recurring, whole-show review with real thumbnails -> **the dashboard** (§1).
- Focused review of one sequence's coverage, or a hand-off artifact -> **contact sheet** (§2).
- A quick visual in the conversation, no app -> **on-demand rendered board** (§3).
- "Just the numbers / what's left" with no visuals needed -> the coordinator's **chat report**
  (`guide-production.md` §5) - no presentation surface required.

---

## Quick application

1. **Reconcile first** (`production` skill) so the manifest is current.
2. Pick the surface by the review need (§4).
3. For the dashboard, point the human at `dashboard/index.html` + *Open production folder*.
4. Keep it **read-only** - approvals/retakes go back through the coordinator to the manifest's
   `human` block, never through the presentation surface.

Companion guides: `guide-production.md` (the manifest this presents), `guide-asset-reference.md`
(the taxonomy paths the board reads), `guide-execution.md` (the `.recipe` provenance behind
each generation).
