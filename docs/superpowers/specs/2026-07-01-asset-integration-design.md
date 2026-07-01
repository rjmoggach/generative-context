# Asset Integration & QC (Phase 4) — Design

**Date:** 2026-07-01 · **Status:** Approved · **Target release:** v0.9.0
**Owner:** Rob (Creative Producer) · **Roadmap:** [`ROADMAP.md`](../../../ROADMAP.md) Phase 4 (final)

---

## 1. Goal

Close the loop: wire the persistent assets (characters/props/sets from Phases 1-2
and the art-bible from Phase 3) into the shot pipeline. Teach the scene/coverage
layer to **attach the right asset references** to each shot, teach the shot layer to
**consume them** (identity = reference, change = prompt), and teach QC to **audit
asset continuity**. Completes the roadmap.

## 2. Scope (full Phase 4, one shippable spec) -> v0.9.0

**In:** the `refs:` attachment notation; edits to `sequence-design` + `first-ad`
(attach), `shot-prompt` + `cinematographer` (consume), `script-supervisor` (audit);
per-model reference-count/strength caveats in `model-currency`; a new
`docs/05-asset-pipeline.md`; build re-wire for the two skills that now bundle
`guide-asset-reference.md`; docs; version bump; one research source; release.
**Out:** no new skills or agents. This is integration only.

## 3. Decisions locked in brainstorming

1. **Full Phase 4 in one spec** -> v0.9.0 (final roadmap phase).
2. **Attachment notation:** a per-shot **`refs:`** field on the shot line listing
   asset ids by their spec-file stem, e.g. `refs: char-eli, prop-revolver,
   set-livingroom`. This is the contract every layer reads.
3. **Autonomy:** build through spec -> plan -> reviewed subagent build -> release
   without approval gates (standing user grant).

## 4. The `refs:` attachment notation

Documented in a new short section of `context/guide-asset-reference.md`
("Attaching references to shots"). Rules:

- Each shot line may end with `refs: <id>[, <id>...]` where each id is an asset's
  spec-file stem: `char-{name}`, `prop-{name}`, `set-{name}` (no `{show}`, no
  extension - the show is implied by the loaded project).
- A shot with no assets omits `refs:`.
- The id resolves to the asset spec (`char-{show}-{name}.md`) and its anchor image
  (`assets/char/{name}/char-{name}-id-front.png`, etc.) via the taxonomy.

## 5. Attach - `sequence-design` + `first-ad`

- `skills/sequence-design/SKILL.md`: add a step "attach asset references" - scan the
  working folder for `char-`/`prop-`/`set-` spec files, and append `refs:` to each
  shot line naming the assets that beat needs. Update the output-format example to
  show `refs:`. Bundle `guide-asset-reference.md` (see §9).
- `plugin/agents/first-ad.md`: add the attach step to its method + output.

## 6. Consume - `shot-prompt` + `cinematographer`

- `skills/shot-prompt/SKILL.md`: add a step "consume attached references" - for each
  id in a shot's `refs:`, read the asset spec, restate its **identity/descriptor
  block verbatim**, attach its **anchor image path** as the model reference, apply
  *identity = reference, change = prompt*, and inherit the `art-bible` palette/CMF.
  Bundle `guide-asset-reference.md` + `guide-image-editing.md` (see §9).
- `plugin/agents/cinematographer.md`: add the consume step to its method.

## 7. Audit - `script-supervisor`

`plugin/agents/script-supervisor.md`: add an **asset-continuity** audit alongside the
existing screen-direction/eyeline/180/look checks:
- **Missing/wrong reference:** a shot that needs an asset but has no `refs:`, or names
  an id with no matching spec.
- **State drift:** costume/HMU/prop **state** changing across a cut without motivation
  (wrong `-fit-`/`-hmu-`/`-hero-<state>` variant).
- **Geometry mismatch:** a location's reverse/coverage that breaks the master plate's
  geometry or light logic.
Report grouped by severity as it already does.

## 8. Currency caveats - `model-currency`

`context/model-currency-2026-06.md`: add a short "Reference-count & strength caveats
(per model)" subsection with the version-anchored numbers the asset layer depends on:
e.g. Nano Banana Pro ~14 objects / ~5 characters; FLUX.2 & Seedream ~10 references;
sweet spot ~4-6 refs; reference strength ~0.7 (0.6-0.8). Note these are
version-sensitive and the `researcher`/`model-docs` loop keeps them current.

## 9. Build re-wire (no new skills)

- `skills/build.py`: add `guide-asset-reference.md` to the `sequence-design` MANIFEST,
  and `guide-asset-reference.md` + `guide-image-editing.md` to the `shot-prompt`
  MANIFEST (so those skills bundle the asset craft they now consume). No `SKILLS`/
  `HELPERS` changes in `assemble.py` (no new skills/agents/helpers).
- `python plugin/assemble.py` must end `VALIDATE: OK`; commit all regenerated bundles
  (editing `guide-asset-reference.md` §10 + `model-currency` re-syncs many skills; the
  Phase 1-3 lesson).

## 10. New doc - `docs/05-asset-pipeline.md`

The end-to-end asset pipeline, mirroring the existing `docs/0X-*.md` style:
project-context (look) -> art-bible (world) -> assets (character-sheet /
prop-turntable / location-pack) -> attach (`refs:` in sequence-design) -> consume
(shot-prompt) -> QC (script-supervisor). Show a worked shot line with `refs:` and how
shot-prompt renders it.

## 11. Docs + release

- `README.md` + `plugin/README.md`: refresh the crew/skill tables + flow to show the
  integrated pipeline (attach -> consume -> audit); mention `docs/05-asset-pipeline.md`;
  banner 0.9.0. Skill/agent counts unchanged (ten skills / eleven agents).
- `CHANGELOG.md` v0.9.0 entry; `ROADMAP.md` mark **Phase 4 shipped and the roadmap
  complete**; versions 0.9.0 in `plugin/.claude-plugin/plugin.json` +
  `.claude-plugin/marketplace.json` (both fields).
- Record the Miller source in `knowledge-base/Miscellaneous-Sources.md` (§13).
- **Release:** merge to `main`, tag `v0.9.0`, `python plugin/assemble.py --package`,
  `gh release create v0.9.0 generative-wrangler.plugin` (keep prior releases). The
  v0.9.0 package also carries the Luma Uni-1 doc already on `main`.

## 12. Verification

- `python plugin/assemble.py` -> `VALIDATE: OK`; `python skills/build.py` clean.
- Every `](references/...)` in the edited `sequence-design`/`shot-prompt` SKILL.md
  resolves (guide-asset-reference / guide-image-editing now bundled).
- `refs:` notation used consistently across guide, sequence-design, first-ad,
  shot-prompt, cinematographer, script-supervisor, and `docs/05-asset-pipeline.md`
  (ids are `char-`/`prop-`/`set-` stems, no `{show}`, no extension).
- Agent frontmatters still parse (first-ad, cinematographer, script-supervisor edited
  in body only - no frontmatter change).
- No `[PLACEHOLDER]` in shipped files.

## 13. Research - source (added to `knowledge-base/Miscellaneous-Sources.md`)

- Pat P. Miller, *Script Supervising and Film Continuity* - the industry-standard
  handbook on continuity, matching, screen direction, and the script supervisor's
  craft; grounds the asset-continuity audit.
  <https://www.routledge.com/Script-Supervising-and-Film-Continuity/Miller/p/book/9780240802947>

## 14. Approach considered & rejected

- **A separate attachment table** (shot -> assets) instead of an inline `refs:` field:
  rejected - it duplicates the shot list and drifts; an inline `refs:` per shot line
  keeps the attachment where the shot is defined and is trivial to author and audit.
- **A new `asset-attach` skill:** rejected (YAGNI) - attachment is a step of
  sequence-design, not a separate deliverable.
