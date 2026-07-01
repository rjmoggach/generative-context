# Art Direction / World Bible (Phase 3) — Design

**Date:** 2026-07-01 · **Status:** Approved · **Target release:** v0.8.0
**Owner:** Rob (Creative Producer) · **Roadmap:** [`ROADMAP.md`](../../../ROADMAP.md) Phase 3

---

## 1. Goal

Add the **Production Designer** and the **world bible** that sits above the asset
layer: a queryable `art-bible-{show}.md` that unifies the show's global palette,
material/CMF lexicon, era/genre, a global style reference, and an **index of every
character/prop/set asset** built in Phases 1-2 - so all assets and shots inherit one
coherent world, top-down. The asset skills already forward-reference
`art-bible-{show}.md`; this phase makes it real.

## 2. Scope (full Phase 3, one shippable spec) -> v0.8.0

**In:** 1 skill, 1 agent, 1 technical guide, expand the creative-craft Production
Design section, 1 art-bible template, a light inheritance retrofit of the asset
skills, build wiring, docs (incl. the director -> production-designer crew-flow),
version bump, research sources, release.
**Out:** integration of assets into sequence/shot/QC (Phase 4); LoRA/3D-assist.

## 3. Decisions locked in brainstorming

1. **Full Phase 3 in one spec** -> v0.8.0.
2. **`art-bible-{show}.md` is a separate PD-owned file** (not folded into
   `project-context`). Clean separation of *look* (DP/director) vs *world* (PD); the
   asset index does not fit a look-doc. The art-bible **inherits** the look from
   `project-context-{show}.md`.
3. **Every role is dual** - creative craft + technical execution.
4. **Autonomy:** build through spec -> plan -> reviewed subagent build -> release
   without approval gates (standing user grant).

## 4. Creative craft - expand the Production Design section

The `## Production Design` section already stubbed in
`context/reference-craft-artdept.md` (Phase 2) is expanded into a full section
(prose principles + anchor table), NOT a new file:

- Principles: the PD as art-department lead; the look book / mood board / concept
  art; color-material-finish (CMF) as a world language; era/genre legibility;
  top-down inheritance (the PD sets the world every other art role inherits);
  designing to theme (Shorter) not decoration.
- `### Anchors` table: reuse the real PDs already in the file (Ken Adam, Dante
  Ferretti, Stuart Craig, Rick Carter, Jack Fisk, Nathan Crowley) and add total-world
  builders **Hannah Beachler** (Black Panther / Afrofuturist world) and **Patrice
  Vermette** (Dune) - accurately attributed. Cross-reference `guide-color-story.md`.

## 5. Technical guide - `context/guide-art-direction.md`

Decision-unit format. The world-bible mechanics:

1. **The art bible as a queryable world spec** - what it holds and why it is separate
   from `project-context`.
2. **Global palette** - named colors + hex; the show's dominant/accent structure.
3. **The CMF lexicon** - material / finish / texture vocabulary reused verbatim across
   assets (the material equivalent of the descriptor block).
4. **Era / genre / world rules** - the constraints every asset obeys.
5. **The global style reference** - one style-ref image + default lens/grade inherited
   from `project-context`.
6. **The asset index** - a table of every `char-`/`prop-`/`set-` asset with its anchor
   image path, so the bible is the map of the world.
7. **Top-down inheritance** - bible -> constrains -> asset sheets -> feed -> shots;
   construct asset prompts *from* the bible's fields, not loosely inspired by them.

Cross-references `project-context` (the look it inherits), `guide-asset-reference.md`
§8 (inherit top-down), `guide-color-story.md` (palette meaning).

## 6. Skill - `skills/art-direction/SKILL.md`

Promote the roadmap stub. PD interview -> `art-bible-{show}.md`. **Extends**
`project-context` (reads it first, inherits lens/grade/palette baseline; never
replaces it). Workflow: load project-context -> define world (palette+hex, CMF lexicon,
era/genre, world rules) -> lock a global style reference (via `image-edit`) -> build
the asset index (scan the working folder for `char-`/`prop-`/`set-` specs) -> write
`art-bible-{show}.md` to the user's working folder.

- `references/art-bible-template.md` - the output skeleton (palette / CMF / era /
  style-ref / asset-index sections). Wired as an `assemble.py` HELPER.
- `references/` bundle: `reference-craft-artdept`, `guide-art-direction`,
  `guide-asset-reference`, `guide-color-story`, `guide-image-editing`,
  `model-currency-2026-06`, and the image/editing model docs.

## 7. Agent - `plugin/agents/production-designer.md`

Promote the stub. The art-department counterpart to `director`: the Director sets
story intent, the PD sets the world and delegates to the five sub-roles (casting,
costume, makeup-hair, propmaster, location-scout). Reads
`${CLAUDE_PLUGIN_ROOT}/context/reference-craft-artdept.md` (Production Design) +
`guide-art-direction.md` + `guide-asset-reference.md`. Strict-YAML frontmatter;
`model: inherit`, `tools: ["Read", "Grep", "Glob"]`, `color: magenta` (deliberately
echoing `director` as the two leads - story lead / world lead; duplicate color is
allowed by the loader).

## 8. Inheritance retrofit (light)

Make the forward-references real without rewriting the asset skills:
- `context/guide-asset-reference.md` §8 (inherit top-down): point it at the new
  `guide-art-direction.md` as the bible's home.
- `skills/character-sheet/SKILL.md`, `skills/prop-turntable/SKILL.md`,
  `skills/location-pack/SKILL.md`, `skills/image-edit/SKILL.md`: ensure each
  load-craft step names "read `art-bible-{show}.md` if present and construct from its
  palette/CMF/style" (add the one line where missing; several already reference it).

## 9. Build wiring + docs + release

- `skills/build.py` - add the `art-direction` MANIFEST entry.
- `plugin/assemble.py` - add `art-direction` to `SKILLS`; add `art-bible-template.md`
  to `HELPERS`.
- `python plugin/assemble.py` must end `VALIDATE: OK`; commit all regenerated bundles
  (editing `guide-asset-reference.md` §8 re-syncs several skills - the Phase 1/2
  lesson).
- `README.md` + `plugin/README.md`: add the `art-direction` skill row + the
  `production-designer` agent row; update the crew-flow to **Director -> Production
  Designer -> (art-dept sub-roles)**; counts -> **ten skills / eleven agents**; banner
  0.8.0.
- `CHANGELOG.md` v0.8.0 entry; `ROADMAP.md` mark Phase 3 shipped; versions 0.8.0 in
  `plugin/.claude-plugin/plugin.json` + `.claude-plugin/marketplace.json` (both fields).
- Remove promoted stubs: `roadmap/agents/production-designer.md`,
  `roadmap/skills/art-direction/`; also remove the stale `roadmap/skills/image-edit/`
  leftover pointer (image-edit shipped in v0.5.1). Update `roadmap/README.md` (only
  Phase 4 integration remains, which lives in the main skills, so the roadmap dir may
  become effectively empty of stubs - note that).
- Record sources in `knowledge-base/Miscellaneous-Sources.md` (§11).
- **Release:** merge to `main`, tag `v0.8.0`, `python plugin/assemble.py --package`,
  `gh release create v0.8.0 generative-cinema.plugin` (keep v0.7.0 / v0.6.0 / v0.5.1).

## 10. Verification

- `python plugin/assemble.py` -> `VALIDATE: OK`; `python skills/build.py` clean.
- Every `](references/...)` in `art-direction/SKILL.md` resolves to a bundled file.
- `production-designer` frontmatter parses as strict YAML with the required keys.
- `art-bible-{show}.md` naming used consistently; the asset index uses the taxonomy
  paths (`assets/char/{name}/`, `assets/prop/{name}/`, `assets/set/{name}/`).
- No `[PLACEHOLDER]` in shipped files.

## 11. Research - creative-context sources (added to `knowledge-base/Miscellaneous-Sources.md`)

- Peter Ettedgui, *Screencraft: Production Design & Art Direction* - sixteen leading
  production designers on their craft.
  <https://www.google.com/books/edition/Production_Design_Art_Direction/pKZTAAAAYAAJ>
- Georgina Shorter, *Designing for Screen: Production Design and Art Direction
  Explained* - designing to story and theme through colour, texture, and space.
  <https://www.crowood.com/products/designing-for-screen-by-georgina-shorter>
- Christopher Frayling, *Ken Adam: The Art of Production Design* - the monograph on
  Ken Adam's world-building (Bond, Dr. Strangelove, Barry Lyndon).
  <https://www.faber.co.uk/product/9780571220571-ken-adam-designs-the-movies/>

## 12. Approach considered & rejected

- **Fold art-direction into project-context** - rejected (see §3.2): mixes look and
  world, bloats the look-doc, and the asset index has no clean home there.
- **New `reference-craft-production-design.md` file** - rejected in favor of expanding
  the existing Production Design section in `reference-craft-artdept.md`, keeping the
  art-department creative craft in one file.
