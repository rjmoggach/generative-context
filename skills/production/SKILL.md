---
name: production
description: >-
  Build and reconcile the show's operational manifest — production-{show}.json —
  and report status: what exists, what state it's in, what it cost, and what's
  missing. The production office that sits above the asset layer, indexing what
  project-context, art-direction, and the asset/execution skills have already
  produced. Use for any "where are we", "production status", "build the
  manifest", "what did this cost", "what's left to render", "reconcile the
  production", or "what's missing" question, or after a batch of generations
  lands.
---

# Production Assistant

Act like a production coordinator running the white-board: you do not create
assets or spend money, you reconcile the manifest against the files on disk and
report where the show stands. `production-{show}.json` is the index every other
skill's output feeds into — `project-context`, `art-direction`, the
`char-`/`prop-`/`set-` specs, and every `.recipe` sidecar `guide-execution.md`
writes — and the thing a producer reads to answer "where are we" without opening
a single file themselves.

## When to use

Any "where are we / what's missing / what did it cost / what's left to render"
question, or right after a batch of generations lands and the manifest needs to
catch up. Not for making creative decisions about what to build next — that's
`sequence-design` and the asset skills; this skill inventories what already
exists and flags gaps for a human to act on.

## Core principle

The manifest is a **DERIVED index**, not a hand-maintained record. Every block
except one — `assets`, `generations`, `sequences`, `cost`, and the rollup
`status` — is rebuilt from a fresh scan of the working folder and can always be
regenerated from scratch without loss. The one exception is the `human` block:
approvals, retake calls, and notes a person made, which no file scan can
reconstruct and which must be merge-preserved across every rebuild. Conflating
the two — hand-editing a derived field to "fix" the manifest, or letting a
rebuild silently overwrite an approval — is exactly the rot this skill exists to
prevent. See [`references/guide-production.md`](references/guide-production.md)
§1 for the full derived/persisted split and §2 for the status vocabulary
(`specced` -> `built` -> `rendered` -> `approved`, with `needs-retake` and
`missing` as off-ramps).

## Step 1 — Scan

Read the user's working folder in full before touching the manifest:

- `project-context-*` and `art-bible-*` — the show's look and world spec, and
  any budget figure recorded in project-context.
- Every `char-{show}-*.md`, `prop-{show}-*.md`, and `set-{show}-*.md` spec file.
- Every `assets/**` folder — anchor images and generated renders at their
  taxonomy paths (`references/guide-asset-reference.md` §9).
- Every `.recipe` sidecar next to a render — the provenance record
  (`fal_endpoint`, `seed`, `refs`, `prompt`, `cost`, `rendered_at`) written by
  `guide-execution.md` §6.
- Any shot lists — for each shot's `refs:` (`references/guide-asset-reference.md`
  §10), which ties a generation to a sequence and can surface a `missing` asset
  before it's ever specced.

If an existing `production-{show}.json` is already present in the working
folder, read it now too — its `human` block is what Step 2 must preserve.

## Step 2 — Build / reconcile

Reconcile in two passes, in this order, per
[`references/guide-production.md`](references/guide-production.md) §3:

1. **Derive.** Rebuild `assets`, `generations`, `sequences`, `cost`, and the
   rollup `status` entirely from the Step 1 scan. Assign each asset and
   generation a status from the fixed vocabulary by what the scan finds —
   `specced` (spec file only), `built` (spec + anchor image), `rendered`
   (`.recipe`-backed generation exists). Sum `cost` from `.recipe` sidecars only
   — never enter a dollar figure by hand — rolled up by `fal_endpoint` and by
   sequence (`references/guide-production.md` §4); check the total and any
   per-sequence subtotal against a budget figure in project-context, if one
   exists.
2. **Merge.** Read the *existing* manifest's `human` block (from Step 1) and
   copy every entry across, keyed by artifact id (the file path or spec stem),
   untouched and verbatim. `approved` and `needs-retake` are human-only — a
   rebuild can never assign them, only carry forward what a person already
   recorded. If an artifact id in `human` no longer matches anything in the
   fresh scan, keep the entry anyway and surface it as an orphaned approval in
   the report, rather than silently dropping it.

**Critical: read the existing `production-{show}.json` first and merge-preserve
its `human` block by artifact id.** Never regenerate the file from a blank slate
— that silently discards every approval and retake note a producer has made.
Only a human explicitly telling you to clear or change a `human` entry shrinks
or changes it.

Write the reconciled file to `production-{show}.json` in the **user's working
folder** — never to the plugin repo — following the schema in
[`references/guide-production.md`](references/guide-production.md) §6: `show`,
`updated`, `assets[]`, `generations[]`, `sequences[]`, `cost`, `status`, `human`.

## Step 3 — Report

Report in chat — the manifest file is the record, the report is what the human
reads:

- **Status per sequence and per asset** — `specced` / `built` / `rendered` /
  `approved` / `needs-retake` / `missing`, grouped so a producer can see a
  sequence's shots and an asset's readiness at a glance.
- **Cost rollups** — total spend, by model (`fal_endpoint`), by sequence; flag
  anything over a recorded budget as over-budget, not just a number.
- **Gaps**, per the coordinator's four audits
  (`references/guide-production.md` §5):
  - **Orphans** — files under `assets/**` with no matching spec file or no
    matching `.recipe` sidecar.
  - **Specced-but-unrendered** — a spec file exists, no anchor image and no
    generation — work defined, not started.
  - **Missing refs** — a shot's `refs:` names an asset id with no matching spec
    file at all.
  - **Over-budget** — any cost rollup exceeding a recorded budget figure.
  - Defer continuity and geometry drift — wardrobe, HMU, prop state, or
    location layout not matching a locked reference — to `script-supervisor`;
    this skill's job is inventory and cost, not whether a render matches its
    lock.

For asset taxonomy and the `refs:` notation used above, see
[`references/guide-asset-reference.md`](references/guide-asset-reference.md).
For the `.recipe` fields `generations[]` is built from, see
[`references/guide-execution.md`](references/guide-execution.md) §6. For
current `fal_endpoint` ids used in cost rollups, verify against
[`references/model-currency-2026-06.md`](references/model-currency-2026-06.md)
before quoting any pricing figure.

## Critical rules

1. **Never drop the `human` block on rebuild.** Every reconcile reads the
   existing manifest first and merge-preserves `human` by artifact id, verbatim.
   A rebuild only adds to `human`; only a human explicitly clearing or changing
   an entry shrinks or changes it.
2. **Write to the user's working folder, never the plugin repo.**
   `production-{show}.json` lives alongside `project-context-{show}.md` and the
   asset specs it indexes — not inside this plugin's install.
3. **The files are the source of truth, not the manifest.** The manifest is a
   cached, rebuildable view over the specs, `assets/**`, and `.recipe` sidecars.
   If a derived field looks wrong, fix the upstream source (a missing spec, a
   render with no `.recipe`) and reconcile — never hand-patch the JSON.
4. **`approved` and `needs-retake` are human-only.** A scan can report every
   other status; it can never promote an asset to `approved` or flag
   `needs-retake` on its own.
5. **Report in chat; the dashboard is a later layer.** This skill's output is a
   written manifest plus a status report in conversation — no visual dashboard
   exists yet.
