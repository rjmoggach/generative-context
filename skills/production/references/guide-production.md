# Production — The Manifest as the Show's Operational Memory

Decision rules for **building and maintaining `{show}_production.json`**, the
manifest that tracks what exists, what state it is in, what it cost, and what a
human has decided about it. `guide-art-direction.md` and `guide-asset-reference.md`
teach the craft of *making* the world and its assets; `guide-execution.md` teaches
the craft of *rendering* them and recording provenance in a `.recipe` sidecar next
to every file. This guide sits one level above all three: it is not a new source of
truth, it is the **index** over the truth those guides already produce.

The manifest is a **DERIVED index** — every block except one is rebuilt from a scan
of the working folder (asset specs, `assets/` folders, `.recipe` sidecars, shot
lists) and can always be regenerated. The one exception is the `human` block:
approvals, retake calls, and notes a person made, which no file scan can
reconstruct. A manifest that conflates the two — that lets a rebuild silently
overwrite an approval, or that asks a human to hand-maintain data the files already
carry — rots. This guide exists to keep that line sharp.

Each entry uses the library's decision-unit format:
**Decision / Use when / Because / Prompt translation / Watch-outs / Anchors.**

---

## 1. The manifest as derived index + persisted human status

- **Decision:** split every field in `{show}_production.json` into one of two
  categories — **derived** (rebuilt from a working-folder scan; always current,
  never edited by hand) or **persisted** (the `human` block; written by a person,
  never inferred, never overwritten).
- **Use when:** designing or reading any field in the manifest; deciding whether a
  new field belongs in a top-level block or inside `human`.
- **Because:** `assets`, `generations`, `sequences`, `cost`, and the rollup `status`
  counts can all be reconstructed from the files on disk — the asset spec files
  (`{show}_char_{name}.md`/`{show}_prop_{name}.md`/`{show}_set_{name}.md`), the anchor images under `assets/`, and
  the `.recipe` sidecars `guide-execution.md` §6 writes next to every render. Because
  they can always be rebuilt, they can never rot — a stale derived block is simply a
  manifest that hasn't been reconciled yet, and reconciling it (§3) fixes it for
  free. A human's approval or retake call is different in kind: no file on disk
  states "hero locked" or "reshoot the wide" — that judgment exists only in a
  person's head until it is written down, and once written down it must persist
  exactly as written, because there is no ground truth to re-derive it from.
- **Prompt translation:** when building or reconciling the manifest, populate
  `assets`, `generations`, `sequences`, `cost`, and `status` entirely from the scan
  — never ask the human for any of these values, and never invent them. Populate
  `human` entirely from what the human has told the coordinator directly (an
  approval, a note, a needs-retake call) — never infer a `human` entry from a file's
  existence or a render's completion. `rendered` is derived (a generation exists);
  `approved` is not (a human said so) — see §2.
- **Watch-outs:** the moment a derived value needs to be hand-edited to "fix" the
  manifest, something is wrong upstream (a missing spec file, a `.recipe` sidecar
  that never got written) — fix the source, then reconcile, don't patch the JSON.
  Conversely, never let a rebuild script write into `human` — that block only grows
  through explicit human input, per §3.
- **Anchors:** `guide-execution.md` §6 (the `.recipe` sidecar as provenance record —
  "the seed record the later production manifest will formalize"); §6 below (the
  worked manifest showing both blocks side by side).

## 2. The status vocabulary

- **Decision:** every asset and generation carries exactly one status from a fixed,
  ordered vocabulary: `specced` -> `built` -> `rendered` -> `approved`, with
  `needs-retake` and `missing` as off-ramps.
- **Use when:** computing an asset's `status` field during reconcile; reading the
  manifest's rollup `status` counts to answer "where are we."
- **Because:** an ungoverned status field drifts into synonyms ("done", "final",
  "ready") that mean different things to different agents and can't be counted
  reliably. A fixed vocabulary makes the rollup in `status` (§6) a trustworthy count,
  not a guess.
- **Prompt translation:** assign status by what the scan finds, in this order:
  - `specced` — the asset's spec file (`{show}_char_{name}.md`/`{show}_prop_{name}.md`/`{show}_set_{name}.md`)
    exists, nothing else does yet.
  - `built` — the spec exists **and** its anchor image exists at the taxonomy path
    (`guide-asset-reference.md` §9).
  - `rendered` — a `.recipe`-backed generation exists for the artifact (an image or
    shot beyond the anchor, or the anchor itself if that's the only render so far).
  - `approved` — a human has recorded this in the `human` block (§1); a rebuild
    cannot promote anything to `approved` on its own.
  - `needs-retake` — a human has recorded this in `human`, overriding whatever the
    derived status would otherwise be.
  - `missing` — referenced (by a shot's `refs:`, per `guide-asset-reference.md` §10,
    or by an expected deliverable) but no spec file exists at all.
- **Watch-outs:** `approved` and `needs-retake` are **human-only** — a scan can never
  assign them, only report what a human already recorded in `human`. Don't collapse
  `specced` and `missing` into one bucket; a spec that exists but has no anchor is a
  real, trackable state (work started, not yet built), while `missing` means nothing
  exists to point to at all.
- **Anchors:** `guide-asset-reference.md` §9 (the taxonomy that defines what "has an
  anchor image" means) and §10 (`refs:` — the mechanism that can surface a `missing`
  asset before it's ever specced).

## 3. Reconcile discipline

- **Decision:** every reconcile rebuilds all derived blocks from a fresh
  working-folder scan, then **merge-preserves the existing `human` block by artifact
  id** — never regenerates or drops it.
- **Use when:** running the `production` skill's build/reconcile step; any time new
  assets, renders, or shot lists have landed since the manifest was last built.
- **Because:** the files are the source of truth, not the manifest — the manifest is
  a cached view over them. Treating it as anything else (hand-editing derived
  fields, trusting a stale manifest over a fresh scan) reintroduces exactly the rot
  this design is meant to prevent. But a naive rebuild that regenerates the whole
  JSON from scratch would wipe `human` along with the derived blocks, silently
  discarding every approval and retake note a producer has made — the single failure
  mode this guide exists to rule out.
- **Prompt translation:** reconcile in two passes. First, **derive**: scan
  `context/*_project_context.md`, `context/*_art_bible.md`, every `{show}_char_{name}.md`/`{show}_prop_{name}.md`/`{show}_set_{name}.md`
  spec, every `assets/**` folder, every `.recipe` sidecar, and any shot lists; rebuild
  `assets`, `generations`, `sequences`, `cost`, and rollup `status` from what's found.
  Second, **merge**: read the manifest's *existing* `human` block before writing the
  new file, and copy every entry across keyed by artifact id (the file path or spec
  stem) — untouched, verbatim. Only add to `human`; never subtract from it during a
  derive pass. A human explicitly telling the coordinator to clear or change an entry
  is the only way `human` shrinks or changes.
- **Watch-outs:** reconcile order matters — derive first, merge second, so the merge
  step can't be skipped by an early return. If an artifact id in `human` no longer
  matches anything in the fresh `assets`/`generations` scan (the file was renamed or
  deleted), keep the `human` entry anyway and surface it as an orphaned approval in
  the audit (§5) rather than silently dropping it — a human should decide whether
  that entry is stale, not the rebuild.
- **Anchors:** the art bible's asset index (`guide-art-direction.md` §6) — "the index
  is live; an out-of-date index is more dangerous than no index" — the same
  discipline applies here, except the manifest's live-ness is enforced by rebuild
  rather than by hand-maintenance.

## 4. Cost tracking

- **Decision:** every dollar in `cost` is summed from `.recipe` sidecars, never
  entered by hand; roll it up by model and by sequence, and flag anything over
  budget.
- **Use when:** reconciling the manifest; answering "what did this cost" or "are we
  over budget"; before authorizing another render batch (`guide-execution.md` §5).
- **Because:** the `.recipe` sidecar already records the `cost` charged for every
  render (`guide-execution.md` §6) — re-entering it by hand would duplicate a number
  that already exists on disk and drift the moment the two copies disagree. Rollups
  by model and sequence turn a flat list of per-file costs into an answer a producer
  can act on: which model is burning the budget, which sequence is the expensive
  one.
- **Prompt translation:** during the derive pass, read the `cost` field out of every
  `.recipe` sidecar found in the scan and sum three ways: `cost.total` (every
  recipe), `cost.by_model` (grouped by each recipe's `fal_endpoint`), `cost.by_sequence`
  (grouped by the sequence a generation's file belongs to, where determinable from
  the shot lists' `refs:`). Compare `cost.total` — and any per-sequence subtotal —
  against a budget figure if one is recorded in `{show}_project_context.md`; if a
  budget exists and is exceeded, surface it in the audit report (§5) as
  over-budget, don't just log the number silently.
- **Watch-outs:** a generation with no `.recipe` sidecar (a render that landed
  without provenance, per `guide-execution.md` §6's watch-out) is invisible to cost
  tracking — it under-counts spend rather than erroring, which is worse than a loud
  failure. Flag files under `assets/**` or shot output paths that have no matching
  `.recipe` as an audit finding (an orphan, §5), not just a cost gap. `by_sequence`
  can be empty (`{}`) when no shot list ties generations to sequences yet — that's a
  valid state, not a bug, matching §6's worked example.
- **Anchors:** `guide-execution.md` §5 (the cost gate — estimate and confirm *before*
  spending) and §6 (the `.recipe` sidecar — the per-render record this rollup sums).

## 5. The coordinator's audits

- **Decision:** on every reconcile, the `production-coordinator` runs a fixed set of
  audits over the derived blocks — orphans, specced-but-unrendered, missing refs,
  and budget — and reports gaps, not just status.
- **Use when:** reconciling the manifest; any "what's left" or "is anything missing"
  question from the human.
- **Because:** a status rollup alone tells a producer *where things stand*; it takes
  an audit to tell them *what needs a decision*. The manifest's value is as much in
  what it flags as in what it counts.
- **Prompt translation:** run these four checks against the fresh scan:
  - **Orphans** — files under `assets/**` (or rendered output) with no matching spec
    file or no matching `.recipe` sidecar; a file the manifest can't explain.
  - **Specced-but-unrendered** — an asset with a spec file and `specced` status but
    no anchor image and no generation — work defined but not started.
  - **Missing refs** — a shot's `refs:` (`guide-asset-reference.md` §10) names an
    asset id with no matching spec file at all — a broken reference, reported as
    `missing` per §2.
  - **Budget** — any `cost` rollup (§4) that exceeds a recorded budget figure.
  - **Loose sequence files** — any file under `sequences/` that is not inside a
    `{show}{###}/` entity folder (`guide-asset-reference.md` §9); a shot list, per-sequence
    context, or render that landed loose. Flag it and normalize it into the correct
    `sequences/{show}{###}/` on reconcile — the same relocate discipline as legacy asset/context files.
  - Defer **state drift and geometry mismatch** — a character's wardrobe or a
    location's layout not matching its locked reference across shots — to
    `script-supervisor`, which audits asset continuity in that depth
    (missing/wrong reference, costume/HMU/prop state drift, location geometry).
    The coordinator's job is inventory and cost; `script-supervisor`'s job is
    whether what got rendered actually matches what was locked.
- **Watch-outs:** don't let the coordinator's audit duplicate `script-supervisor`'s
  continuity work — reporting "this shot has no `refs:` for a locked asset" is the
  coordinator's job (a manifest-completeness question); reporting "this shot's
  wardrobe doesn't match the locked reference" is `script-supervisor`'s job (a
  content-correctness question). Keep the boundary at *does the data exist* versus
  *is the data right*.
- **Anchors:** `guide-asset-reference.md` §10 (`refs:` and the broken-reference case
  it names as `script-supervisor`'s to audit); `script-supervisor` (continuity —
  screen direction, eyelines, and asset-continuity: missing/wrong reference,
  costume/HMU/prop state drift, location geometry).

## 6. The worked manifest

- **Decision:** `{show}_production.json` follows one fixed schema — `show`,
  `updated`, `assets[]`, `generations[]`, `sequences[]`, `cost`, `status`, `human` —
  written to the user's working folder, never the plugin repo.
- **Use when:** implementing or reading a `{show}_production.json` file; the schema
  reference for §1-§5.
- **Because:** a worked example makes the derived/persisted split (§1) and the
  status vocabulary (§2) concrete rather than abstract — every field below traces to
  a rule above it.
- **Prompt translation:** the schema, populated for a two-asset, one-shot show:

```json
{
  "show": "sbw",
  "updated": "2026-07-02",
  "assets": [
    { "type": "char", "name": "eli", "spec_file": "assets/char/eli/sbw_char_eli.md", "anchor_image": "assets/char/eli/sbw_char_eli_id_front.png", "status": "built" },
    { "type": "set", "name": "livingroom", "spec_file": "assets/set/livingroom/sbw_set_livingroom.md", "anchor_image": null, "status": "specced" }
  ],
  "generations": [
    { "file": "assets/char/eli/sbw_char_eli_id_front.png", "fal_endpoint": "fal-ai/flux/schnell", "seed": 1278911897, "refs": [], "prompt": "...", "cost": 0.003, "rendered_at": "2026-07-02" }
  ],
  "sequences": [
    { "label": "S2", "shots": [ { "label": "sbw002_0030", "refs": ["char_eli", "set_livingroom"], "generated": false } ] }
  ],
  "cost": { "total": 0.003, "by_model": { "fal-ai/flux/schnell": 0.003 }, "by_sequence": {} },
  "status": { "specced": 2, "built": 1, "rendered": 1, "approved": 0, "missing": 0 },
  "human": {
    "assets/char/eli/sbw_char_eli_id_front.png": { "status": "approved", "note": "hero locked" }
  }
}
```

- **Watch-outs:** note what this example demonstrates about §1-§5: `eli` is `built`
  in `assets` (derived — spec + anchor both exist) but `approved` only inside `human`
  (persisted — a person locked it; the derived `assets` entry never says
  `"status": "approved"` on its own). `livingroom` has `anchor_image: null` and
  `status: "specced"` — work defined, not built (§5's specced-but-unrendered case).
  `sbw002_0030` names both refs but `"generated": false` — a shot the coordinator should
  flag as not yet rendered. `cost.by_sequence` is empty because no generation yet
  ties to `S2` — a valid state (§4), not an error. The rollup `status` counts (2
  specced, 1 built, 1 rendered, 0 approved-at-the-rollup-level, 0 missing - both of
  `sbw002_0030`'s refs resolve to specs) are derived sums; the one `approved` fact in the
  file lives only in `human`.
- **Anchors:** §1 (the split this example demonstrates); `guide-execution.md` §6
  (the `.recipe` fields — `fal_endpoint`, `seed`, `refs`, `prompt`, `cost`,
  `rendered_at` — that `generations[]` is built from, one entry per sidecar).

---

## Quick application

1. Scan the working folder — asset specs, `assets/**`, `.recipe` sidecars, shot
   lists — and rebuild `assets`, `generations`, `sequences`, `cost`, and rollup
   `status` from scratch every reconcile (§1, §3).
2. Assign status from the fixed vocabulary — `specced` / `built` / `rendered` /
   `approved` / `needs-retake` / `missing` — never a synonym (§2).
3. Read the existing manifest's `human` block first and merge it into the new file
   by artifact id before writing anything — never let a rebuild drop an approval
   (§3).
4. Sum `cost` from `.recipe` sidecars only; roll up by model and sequence; flag
   anything over budget (§4).
5. Run the coordinator's four audits — orphans, specced-but-unrendered, missing
   refs, budget — and defer state/geometry drift to `script-supervisor` (§5).
6. Write `{show}_production.json` to the user's working folder using the schema in
   §6 — derived blocks plus the persisted `human` block, never conflated.

## 7. Governance — reconcile is a plugin action, not a standing rule

- **Decision:** the reconcile discipline lives in the plugin's skills and this guide,
  **never** in the user's `CLAUDE.md` or any config file.
- **Use when:** an agent is tempted to "make reconcile automatic," or a user asks how
  to keep the manifest current.
- **Because:** a drifting manifest is a tooling problem, solved by *running* the
  `production` skill — not by installing a "the coordinator must run after every step"
  rule into a project's `CLAUDE.md`. An agent that writes such a rule is overreaching:
  it edits the user's standing configuration to compensate for a step it should simply
  perform. Reconciliation happens two ways, both inside the plugin: a producing skill's
  **close-out step** (it reconciles before finishing), or the user invoking the
  `production` skill / `production-coordinator` directly.
- **Prompt translation:** after producing assets/specs/generations, run the reconcile
  yourself as the close-out. **Never** propose or write a workflow rule into `CLAUDE.md`
  (or `.cursorrules`, settings, etc.); if a project's `CLAUDE.md` already carries one,
  offer to remove it — the plugin governs this. Normalizing legacy filenames (§9 of
  `guide-asset-reference.md`) is part of reconcile, not a config change.
- **Anchors:** tools own their own discipline; standing configuration is the user's,
  not the agent's to rewrite.

Companion guides: `guide-asset-reference.md` (the taxonomy and `refs:` notation the
manifest indexes), `guide-execution.md` (the `.recipe` sidecar `generations[]`
derives from), `model-currency-2026-06.md` (current `fal_endpoint` ids and pricing
for the cost rollup), and `script-supervisor` (continuity audits — state and
geometry drift — that the coordinator defers rather than duplicates).
