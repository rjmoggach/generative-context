# Production Office — Coordinator + Manifest (v1.0-b) — Design

**Date:** 2026-07-02 · **Status:** Approved · **Target release:** v0.11.0
**Owner:** Rob (Creative Producer) · **Track:** toward v1.0 (make -> manage -> review)

---

## 1. Goal

Turn the growing pile of artifacts (context docs, asset specs, and the images/video
the v0.10.0 render loop now produces) into a **managed production**. Add the
operational deputy every real production has - a production coordinator / UPM - and
the **manifest** that is the show's operational memory: what exists, its status, its
provenance, and what it cost. This is the second v1.0 layer (execution -> **production
office** -> presentation).

## 2. Scope (v1.0-b) -> v0.11.0

**In:** the `production-{show}.json` manifest, a `production` skill (build/reconcile +
report), a `production-coordinator` agent, `guide-production.md`, build wiring, docs,
version bump, one research source.
**Out:** contact sheets + the rendered dashboard (the *presentation* of the manifest) -
that is v1.0-c. The coordinator reports in chat for now.

## 3. Decisions

1. **Manifest = a derived index the coordinator rebuilds from ground truth** (asset
   specs + the `.recipe` sidecars v0.10.0 writes) **plus persisted human status**
   (approved / needs-retake / notes) that cannot be re-derived. It can always be
   rebuilt from the files, so it cannot rot; producing skills carry no manifest-writing
   burden. (Defaulted to the recommended option while the user was away - revisit if
   they disagree.)
2. **Format: JSON canonical** (`production-{show}.json`) - it is operational data the
   coordinator mutates, so a structured store keeps machine round-trips honest. The
   human view (a rendered dashboard) is generated in v1.0-c; for now the coordinator
   reports in chat. One source of truth, never two masters.
3. **Skill + agent + guide**, mirroring the established pattern (like art-direction ->
   art-bible + production-designer + guide-art-direction). Version **v0.11.0**.

## 4. The manifest - `production-{show}.json`

Written to the user's working folder (beside `project-context-*`, `art-bible-*`, and
the asset specs). Structure (documented with a worked example in `guide-production.md`):

- `show`, `updated` - the show code and last-reconcile timestamp.
- `assets[]` - derived from scanning `char-`/`prop-`/`set-` spec files + `assets/`
  folders: `{ type, name, spec_file, anchor_image, status }` where `status` is
  `specced` | `built` (has anchor image) | `missing`.
- `generations[]` - derived from `.recipe` sidecars: `{ file, fal_endpoint, seed,
  refs, prompt, cost, rendered_at }`.
- `sequences[]` / `shots[]` - derived from shot lists when present: `{ label, refs,
  generated, ... }`.
- `cost` - rollups: `{ total, by_model, by_sequence }` summed from the recipes.
- `status` - rollups: counts of specced / built / rendered / approved / missing.
- `human` - the **persisted, non-derivable** block: per-artifact `{ status:
  draft|approved|needs-retake, note }`, keyed by artifact id. This is what a rebuild
  MUST preserve.

## 5. Skill - `skills/production/SKILL.md`

The counterpart to how `art-direction` builds the art-bible. Workflow:
1. **Scan** the working folder - `project-context-*`, `art-bible-*`, `char-`/`prop-`/
   `set-` specs, `assets/**`, `.recipe` sidecars, shot lists.
2. **Build/reconcile** `production-{show}.json` - regenerate the derived blocks from
   the scan; **preserve the existing `human` block** (merge by artifact id; never drop
   an approval on rebuild).
3. **Report** in chat: where we are (specced/built/rendered/approved/missing per
   sequence + asset), cost rollups, and gaps (specced-but-unrendered, orphan files not
   in any spec, missing refs, over-budget).
- `references/` bundle: `guide-production`, `guide-asset-reference`, `guide-execution`,
  `model-currency-2026-06`.

## 6. Agent - `plugin/agents/production-coordinator.md`

The operational deputy (UPM / line producer / coordinator) - the human Creative
Producer's operations partner. Reads `${CLAUDE_PLUGIN_ROOT}/context/guide-production.md`
+ `guide-asset-reference.md` + `guide-execution.md`; runs the `production` skill's
scan/reconcile; **reports and audits** (status, cost, orphans, missing/over-budget). It
writes ONLY the manifest (the index), never the assets. Strict-YAML frontmatter
(`name`/`description`/`model`/`color`/`tools`), `model: inherit`,
`tools: ["Read", "Grep", "Glob"]`, `color: green` (operational kinship with `first-ad`;
duplicate color is allowed by the loader).

## 7. Guide - `context/guide-production.md`

Decision-unit format. The production-office craft:
- The manifest as **derived index + persisted human status** - what is re-derived
  (assets/generations/cost from specs + recipes) vs what must persist (approvals/notes).
- The **status vocabulary** - specced / built / rendered / approved / needs-retake /
  missing.
- **Reconcile discipline** - rebuild the derived blocks from the files; merge-preserve
  the `human` block by id; the files are the source of truth, the manifest is the index.
- **Cost tracking** - sum from `.recipe` sidecars; rollups by model/sequence; flag
  over-budget.
- **The coordinator's audits** - orphans, specced-but-unrendered, missing refs,
  geometry/state drift (defer detail to `script-supervisor`), budget.
- A worked example `production-{show}.json`.
- Close with `## Quick application` + companion-guides line.
Grounded in a real production-management source (§11).

## 8. Build wiring

- `skills/build.py`: add a `production` MANIFEST entry (the §5 bundle).
- `plugin/assemble.py`: add `"production"` to `SKILLS`. (No new HELPER - the manifest
  schema lives in `guide-production.md`, not a template file.)
- `python plugin/assemble.py` must end `VALIDATE: OK`; commit all regenerated bundles.

## 9. Docs + release

- `README.md` + `plugin/README.md`: add the `production` skill row + `production-
  coordinator` agent row; note the production office (manifest + coordinator); counts ->
  **twelve skills / twelve agents**; banner 0.11.0.
- `CHANGELOG.md` v0.11.0 entry; `ROADMAP.md`: v1.0-track note (production office shipped;
  presentation next). Versions 0.11.0 in `plugin/.claude-plugin/plugin.json` +
  `.claude-plugin/marketplace.json` (both).
- Record the Honthaner source in `knowledge-base/Miscellaneous-Sources.md`.
- **Release:** final review -> merge -> tag `v0.11.0` -> package -> `gh release create`.

## 10. Verification

- `python plugin/assemble.py` -> `VALIDATE: OK`; `python skills/build.py` clean.
- Every `](references/...)` in `production/SKILL.md` resolves (bundled).
- `production-coordinator` frontmatter parses as strict YAML with the required keys.
- The manifest schema in `guide-production.md` names the `human` (persisted) block and
  states the merge-preserve-on-rebuild rule (the anti-rot guarantee).
- No `[PLACEHOLDER]`; project name stays `generative-wrangler`.

## 11. Research - source (added to `knowledge-base/Miscellaneous-Sources.md`)

- Eve Light Honthaner, *The Complete Film Production Handbook* - the standard reference
  for line producers, production managers, and coordinators (forms, checklists, tracking,
  budgeting); grounds the production-office craft.
  <https://www.routledge.com/The-Complete-Film-Production-Handbook/Honthaner/p/book/9780240811505>

## 12. Approach considered & rejected

- **Every producing step writes the manifest:** rejected - in a no-code, agent-driven
  system that discipline is fragile and drifts silently (rot). Rebuild-from-ground-truth
  is robust.
- **Markdown-canonical manifest:** rejected - it is machine-mutated operational data;
  JSON keeps round-trips honest. The human-readable view is generated (v1.0-c).
- **Fold the coordinator into an existing agent (e.g. first-ad):** rejected - the
  production office is a distinct operational role; conflating it with coverage muddies
  both.
