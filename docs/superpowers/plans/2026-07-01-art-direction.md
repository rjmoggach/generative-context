# Art Direction / World Bible (Phase 3) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship v0.8.0 - the Production Designer and world bible: the `art-direction` skill, the `production-designer` agent, `guide-art-direction.md`, the expanded Production Design creative section, and a light inheritance retrofit so Phase 1-2 assets inherit from `art-bible-{show}.md`.

**Architecture:** `context/` is the single source of truth; `skills/build.py` bundles context files into each skill's `references/` and zips `.skill`s; `plugin/assemble.py` regenerates `plugin/context/` + `plugin/skills/` (repointing `](references/...)` to `${CLAUDE_PLUGIN_ROOT}/context/`) and validates. No unit tests - the gate is `python plugin/assemble.py` printing `VALIDATE: OK` and `python skills/build.py` running clean. Mirrors the Phase 1-2 pipelines.

**Tech Stack:** Markdown (library + skills + agents), Python 3 stdlib build scripts, JSON manifests. Spec: `docs/superpowers/specs/2026-07-01-art-direction-design.md`.

## Global Constraints

- **Target version:** `0.8.0` - verbatim in `plugin/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` (both `metadata.version` and the plugin-entry `version`), and README banners.
- **Library format for `guide-*.md`:** heuristic decision-unit - `**Decision / Use when / Because / Prompt translation / Watch-outs / Anchors.**`
- **Library format for `reference-*.md`:** knowledge catalog with anchor tables.
- **House style:** match existing `context/guide-*.md` / `reference-*.md` - em-dashes (-) and rich prose ARE the house style; straight quotes; no emojis; technical terms in `` `code` ``. No `[PLACEHOLDER]` in shipped files.
- **World-bible naming:** the PD's world file is `art-bible-{show}.md` (a separate file that inherits from `project-context-{show}.md`). It holds an asset INDEX referencing the taxonomy paths `assets/char/{name}/`, `assets/prop/{name}/`, `assets/set/{name}/` (image files carry no `{show}`).
- **Agent frontmatter (strict YAML, required keys):** `name`, `description`, `model`, `color`, `tools`. Use `model: inherit`, `tools: ["Read", "Grep", "Glob"]`. No raw `<...>` tags in frontmatter. `production-designer` color: `magenta` (echoing `director` as the two leads; duplicate color allowed).
- **Commits:** OMIT the `Co-Authored-By` trailer. Branch: `feat/art-direction` (already created).
- **Build hygiene (Phase 1-2 lesson):** editing `context/guide-asset-reference.md` re-syncs EVERY skill that bundles it; editing an already-shipped skill's `SKILL.md` regenerates its `plugin/skills/` copy. After `build.py`/`assemble.py` run, commit ALL regenerated outputs so the tree is clean.

---

### Task 1: Expand the Production Design creative section + record sources

**Files:**
- Modify: `context/reference-craft-artdept.md` (expand the existing `## Production Design` stub section)
- Modify: `knowledge-base/Miscellaneous-Sources.md` (append three entries)

**Interfaces:**
- Produces: the expanded creative section read by the `production-designer` agent (Task 4) and the `art-direction` skill (Task 3).

- [ ] **Step 1: Read** the current `## Production Design` stub in `context/reference-craft-artdept.md` and the file's existing anchor-table format (columns Name | Signature | Known for | When to reference). Match it.

- [ ] **Step 2: Expand the section** into full craft. Keep the existing heading. Add 4-6 prose principles: the PD as art-department lead who sets the coherent world; the look book / mood board / concept art; color-material-finish (CMF) as a world language; era/genre legibility; top-down inheritance (the world every art role inherits); designing to theme not decoration. Then add or extend an `### Anchors` table with real production designers: reuse those already in the file (Ken Adam, Dante Ferretti, Stuart Craig, Rick Carter, Jack Fisk, Nathan Crowley) and add **Hannah Beachler** (*Black Panther* - first Black woman to win the Production Design Oscar; Afrofuturist world) and **Patrice Vermette** (*Dune*, *Arrival*, *Sicario*). Attribute every credit accurately - do not invent. Cross-reference `guide-color-story.md`.

- [ ] **Step 3: Append three sources to `knowledge-base/Miscellaneous-Sources.md`** in the file's `## Author, _Title_` + note + URL-bullet format. Use verifiable publisher/Goodreads URLs; if unsure of an exact URL, use a Goodreads or publisher search-result URL rather than inventing one:

```markdown
## Peter Ettedgui, _Screencraft: Production Design & Art Direction_

sixteen leading production designers on world-building, drawings, models, and storytelling through space.

- https://www.goodreads.com/book/show/1662436.Production_Design_Art_Direction

## Georgina Shorter, _Designing for Screen: Production Design and Art Direction Explained_

designing to story and theme through colour, texture, and space; the art-department workflow.

- https://www.crowood.com/products/designing-for-screen-by-georgina-shorter

## Christopher Frayling, _Ken Adam: The Art of Production Design_

the monograph on Ken Adam's world-building (Bond, Dr. Strangelove, Barry Lyndon).

- https://www.goodreads.com/book/show/1857890.Ken_Adam
```

- [ ] **Step 4: Verify.** `grep -n "Hannah Beachler\|Patrice Vermette" context/reference-craft-artdept.md` finds the new anchors; `grep -n "Ettedgui" knowledge-base/Miscellaneous-Sources.md` finds the source; no `[PLACEHOLDER]`; house style clean.

- [ ] **Step 5: Commit.**

```bash
git add context/reference-craft-artdept.md knowledge-base/Miscellaneous-Sources.md
git commit -m "feat(context): expand Production Design creative section + sources"
```

---

### Task 2: `guide-art-direction.md` (technical craft)

**Files:**
- Create: `context/guide-art-direction.md`

**Interfaces:**
- Produces: `context/guide-art-direction.md` (bundled by Tasks 3, 6; read by `production-designer` in Task 4).

- [ ] **Step 1: Study** `context/guide-asset-reference.md` (the spine, esp. §8 inherit top-down), `context/guide-color-story.md` (palette), and `context/reference-craft-character.md` for the decision-unit format and cross-referencing voice.

- [ ] **Step 2: Write the guide.** Decision-unit format. Intro: the world bible mechanics - how to build and maintain `art-bible-{show}.md`, the *technical* companion to the Production Design creative section, inheriting the look from `project-context`. Sections:
  1. **The art bible as a queryable world spec** - what it holds; why it is separate from `project-context` (look vs world); it inherits lens/grade/palette baseline from project-context.
  2. **Global palette** - named colors + hex; dominant/accent structure; cross-ref `guide-color-story.md`.
  3. **The CMF lexicon** - material / finish / texture vocabulary reused verbatim across assets (the material equivalent of the character descriptor block).
  4. **Era / genre / world rules** - the constraints every asset obeys.
  5. **The global style reference** - one style-ref image (derive/lock via `image-edit`) + default lens/grade from `project-context`.
  6. **The asset index** - a table mapping every `char-`/`prop-`/`set-` asset to its anchor image path (taxonomy paths); the bible is the map of the world.
  7. **Top-down inheritance** - bible -> constrains -> asset sheets -> feed -> shots; construct asset prompts FROM the bible's fields.
  - Close with `## Quick application` + companion-guides line (`project-context`, `guide-asset-reference.md` §8, `guide-color-story.md`, `reference-craft-artdept.md`).

- [ ] **Step 3: Verify.** `grep -n "art-bible-{show}.md\|CMF\|asset index" context/guide-art-direction.md` finds the key concepts; decision-unit format present; no `[PLACEHOLDER]`.

- [ ] **Step 4: Commit.**

```bash
git add context/guide-art-direction.md
git commit -m "feat(context): add guide-art-direction (world-bible mechanics)"
```

---

### Task 3: `art-direction` skill + art-bible template

**Files:**
- Create: `skills/art-direction/SKILL.md`
- Create: `skills/art-direction/references/art-bible-template.md`

**Interfaces:**
- Consumes (bundled by Task 6): `reference-craft-artdept.md`, `guide-art-direction.md`, `guide-asset-reference.md`, `guide-color-story.md`, `guide-image-editing.md`, `model-currency-2026-06.md`, image/editing model docs.
- Produces: `skills/art-direction/SKILL.md`; `art-bible-template.md` (assemble HELPER in Task 6).

- [ ] **Step 1: Study** `skills/character-sheet/SKILL.md` and `skills/project-context/SKILL.md` (the interview-style sibling) for frontmatter shape, structure, and the `](references/...)` link convention; read `roadmap/skills/art-direction/SKILL.md` (the stub).

- [ ] **Step 2: Write `skills/art-direction/SKILL.md`.** Frontmatter: `name: art-direction` + multiline `description: >-` with trigger phrases ("define the world", "build the art bible", "set the palette and materials", "create the world bible", "art-direct this show", "what's our CMF"). Body:
  - Purpose - build the queryable world spec above the asset layer; the PD's counterpart to project-context.
  - When to use - after `project-context` exists and before/alongside building assets; refine in place if `art-bible-{show}.md` exists.
  - Core principle - the bible inherits the look from `project-context` and constrains every asset top-down.
  - Step: Load - read `project-context-{show}.md` (inherit lens/grade/palette), and `](references/reference-craft-artdept.md)` (Production Design), `](references/guide-art-direction.md)`, `](references/guide-asset-reference.md)`, `](references/guide-color-story.md)`, `](references/guide-image-editing.md)`.
  - Step: Define the world - global palette (named + hex), CMF lexicon, era/genre, world rules.
  - Step: Lock the global style reference via `image-edit`; record default lens/grade inherited from project-context.
  - Step: Build the asset index - scan the working folder for `char-`/`prop-`/`set-` spec files and list each with its anchor image path.
  - Step: Output - write `art-bible-{show}.md` per `](references/art-bible-template.md)` to the USER'S WORKING FOLDER.
  - Critical rules - inherit from project-context (never replace it); pin palette hex + CMF names; the asset index uses taxonomy paths; binaries/outputs to the user folder; verify any model reference vs `](references/model-currency-2026-06.md)`.

- [ ] **Step 3: Write `skills/art-direction/references/art-bible-template.md`.** Output skeleton: H1 `# {SHOW} - Art Bible`; `## Inherits` (project-context link + inherited lens/grade); `## Global palette` (named + hex rows); `## CMF lexicon` (material/finish/texture terms); `## Era / genre / world rules`; `## Global style reference` (`assets/style/{show}-style.png` path); `## Asset index` (table: asset | type | spec file | anchor image - real taxonomy paths e.g. `char-{name}` -> `assets/char/{name}/char-{name}-id-front.png`, `prop-{name}` -> `assets/prop/{name}/prop-{name}-hero.png`, `set-{name}` -> `assets/set/{name}/set-{name}-plate.png`). No leftover placeholders in prose; template fill-in tokens (`{SHOW}`, `{name}`) are fine.

- [ ] **Step 4: Verify.** `grep -n "](references/" skills/art-direction/SKILL.md` lists the links; frontmatter has name+description, no tabs; template has the sections + taxonomy asset-index paths.

- [ ] **Step 5: Commit.**

```bash
git add skills/art-direction/SKILL.md skills/art-direction/references/art-bible-template.md
git commit -m "feat(skills): add art-direction skill + art-bible template"
```

---

### Task 4: `production-designer` agent

**Files:**
- Create: `plugin/agents/production-designer.md`

**Interfaces:**
- Consumes: `${CLAUDE_PLUGIN_ROOT}/context/reference-craft-artdept.md`, `guide-art-direction.md`, `guide-asset-reference.md` (in `plugin/context/` after Task 6).
- Produces: an agent file that passes assemble.py strict-YAML validation.

- [ ] **Step 1: Study** `plugin/agents/director.md` (the counterpart) and `plugin/agents/casting-director.md` for frontmatter shape and body structure; read `roadmap/agents/production-designer.md` (the stub).

- [ ] **Step 2: Write `plugin/agents/production-designer.md`.** Frontmatter verbatim:

```markdown
---
name: production-designer
description: >-
  The Production Designer: set the show's coherent visual world - global palette,
  materials/CMF, era, and a global style reference - and index every character, prop,
  and set asset into one art bible. Use when the user says "define the world", "build
  the art bible", "set the palette and materials", "art-direct this show", or "make
  the world coherent". The art-department counterpart to the director: the director
  sets story intent, you set the world and delegate to casting, costume, makeup-hair,
  propmaster, and location-scout.
model: inherit
color: magenta
tools: ["Read", "Grep", "Glob"]
---
```
  Body: persona (the art-dept lead who owns the coherent world - look book, CMF, world rules - per `reference-craft-artdept.md` Production Design); When this agent fires; Method (read `${CLAUDE_PLUGIN_ROOT}/context/reference-craft-artdept.md` + `guide-art-direction.md` + `guide-asset-reference.md`; inherit `project-context-{show}.md`; define palette/CMF/era; lock a global style ref; build the asset index; the art-direction skill writes `art-bible-{show}.md`); Output (a directed art-bible brief + delegation to the five sub-roles: casting-director, costume-designer, makeup-hair, propmaster, location-scout). Decide the world; hand execution to the sub-roles.

- [ ] **Step 3: Verify frontmatter.**

```bash
echo "== production-designer =="; sed -n '1,13p' plugin/agents/production-designer.md
```
Expected: the five keys, `color: magenta`, no `<` lines in frontmatter.

- [ ] **Step 4: Commit.**

```bash
git add plugin/agents/production-designer.md
git commit -m "feat(agents): add production-designer crew (art-dept lead)"
```

---

### Task 5: Inheritance retrofit (assets inherit from the art bible)

**Files:**
- Modify: `context/guide-asset-reference.md` (§8 Inherit top-down)
- Modify: `skills/character-sheet/SKILL.md`, `skills/prop-turntable/SKILL.md`, `skills/location-pack/SKILL.md`, `skills/image-edit/SKILL.md` (load-craft steps)

**Interfaces:**
- Produces: consistent `art-bible-{show}.md` inheritance references across the asset skills; §8 pointing at `guide-art-direction.md`.

- [ ] **Step 1: Update `context/guide-asset-reference.md` §8 "Inherit top-down."** Point it at the now-real bible: state that `art-bible-{show}.md` is built and maintained via `guide-art-direction.md` and the `art-direction` skill, and that assets construct their prompts FROM the bible's palette/CMF/style fields. Keep the existing §8 prose; add the `guide-art-direction.md` reference (do not duplicate that guide's content).

- [ ] **Step 2: Confirm/add the art-bible line in each asset skill's Load step.** For each of `skills/character-sheet/SKILL.md`, `skills/prop-turntable/SKILL.md`, `skills/location-pack/SKILL.md`, `skills/image-edit/SKILL.md`: read the "Load context/craft" step; ensure it contains a line equivalent to "If `art-bible-{show}.md` exists, inherit its global palette, CMF lexicon, and style reference; construct prompts from those fields." Add the one line where missing; if a skill already references the art-bible, leave it (do not duplicate). Do NOT restructure the skills - this is a one-line inheritance note per skill.

- [ ] **Step 3: Verify.** `grep -rn "art-bible" skills/character-sheet/SKILL.md skills/prop-turntable/SKILL.md skills/location-pack/SKILL.md skills/image-edit/SKILL.md context/guide-asset-reference.md` shows an art-bible reference in each of the five files. No other content changed (diff should be small, additive).

- [ ] **Step 4: Commit.**

```bash
git add context/guide-asset-reference.md skills/character-sheet/SKILL.md skills/prop-turntable/SKILL.md skills/location-pack/SKILL.md skills/image-edit/SKILL.md
git commit -m "feat: retrofit asset skills to inherit from art-bible (guide-asset-reference §8 + load steps)"
```

---

### Task 6: Build wiring + integration validation (the gate)

**Files:**
- Modify: `skills/build.py` (add `art-direction` to `MANIFEST`)
- Modify: `plugin/assemble.py` (add `art-direction` to `SKILLS`; add `art-bible-template.md` to `HELPERS`)

**Interfaces:**
- Consumes: all files from Tasks 1-5.
- Produces: populated `skills/art-direction/references/`, regenerated `plugin/context/*` + `plugin/skills/*`, a passing `VALIDATE: OK`.

- [ ] **Step 1: Add the `art-direction` MANIFEST entry to `skills/build.py`** (after the `location-pack` entry):

```python
    "art-direction": [
        ("reference-craft-artdept.md", "references/reference-craft-artdept.md"),
        ("guide-art-direction.md", "references/guide-art-direction.md"),
        ("guide-asset-reference.md", "references/guide-asset-reference.md"),
        ("guide-color-story.md", "references/guide-color-story.md"),
        ("guide-image-editing.md", "references/guide-image-editing.md"),
        ("model-currency-2026-06.md", "references/model-currency-2026-06.md"),
        ("model-editing-flux-kontext.md", "references/models/model-editing-flux-kontext.md"),
        ("model-image-gemini-flash.md", "references/models/model-image-gemini-flash.md"),
        ("model-image-seedream-4.md", "references/models/model-image-seedream-4.md"),
        ("model-image-flux-pro.md", "references/models/model-image-flux-pro.md"),
    ],
```

- [ ] **Step 2: Register the skill + helper in `plugin/assemble.py`.** Add `"art-direction"` to the `SKILLS` list (after `"location-pack"`):

```python
SKILLS = ["project-context", "sequence-design", "shot-prompt", "model-docs", "footage-transform", "image-edit", "character-sheet", "prop-turntable", "location-pack", "art-direction"]
```
And append to `HELPERS`:

```python
    SKILLS_SRC / "art-direction/references/art-bible-template.md",
```

- [ ] **Step 3: Run the skill build.**

```bash
python skills/build.py
```
Expected: `sync art-direction: ...` lines and `zip ... art-direction.skill`. It also re-syncs every skill that bundles `guide-asset-reference.md` (image-edit, character-sheet, prop-turntable, location-pack) because Task 5 changed §8 - expected.

- [ ] **Step 4: Run assemble + validate (the gate).**

```bash
python plugin/assemble.py
```
Expected: `skill: art-direction` (among others) and final line `VALIDATE: OK`. If it prints `FAIL ...`, fix the named missing reference/agent and re-run. Paste the final line into your report.

- [ ] **Step 5: Commit build-script edits AND every regenerated output** (Phase 1-2 lesson - include the re-synced bundles and the regenerated `plugin/skills/*/SKILL.md` for the four retrofitted asset skills):

```bash
git add skills/build.py plugin/assemble.py skills/art-direction/references skills/image-edit/references skills/character-sheet/references skills/prop-turntable/references skills/location-pack/references plugin/context plugin/skills
git status --porcelain | grep -v .superpowers   # confirm nothing else pending
git commit -m "build: wire art-direction skill into build.py + assemble.py"
```

- [ ] **Step 6: Confirm tree clean** (excluding `.superpowers/`): `git status --porcelain | grep -v .superpowers` prints nothing. If a regenerated file remains, `git add` it and amend.

---

### Task 7: Docs, crew-flow, version bump, stub removal + final validate

**Files:**
- Modify: `README.md`, `plugin/README.md`, `CHANGELOG.md`, `ROADMAP.md`, `roadmap/README.md`
- Modify: `plugin/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`
- Delete: `roadmap/agents/production-designer.md`, `roadmap/skills/art-direction/`, `roadmap/skills/image-edit/`

- [ ] **Step 1: Bump versions to `0.8.0`** in `plugin/.claude-plugin/plugin.json` (`"version"`), `.claude-plugin/marketplace.json` (BOTH `metadata.version` AND the plugin-entry `version` - both currently 0.7.0), and README banners. Verify `grep -rn '0.7.0' plugin/.claude-plugin/plugin.json .claude-plugin/marketplace.json README.md` returns nothing.

- [ ] **Step 2: Update `README.md`** - add an `art-direction` row to the Skills table (Level: World bible / Project), a `production-designer` row to the Agents table (Role: Art dept lead). Update the crew-flow text so it reads Director -> Production Designer -> the art-dept sub-roles (casting/costume/makeup-hair/propmaster/location-scout) -> DP/coverage. Mention `guide-art-direction` + the art-bible in the craft paragraph. Update repo-layout counts to `skills/ (10) agents/ (11)`. Model list unchanged.

- [ ] **Step 3: Update `plugin/README.md`** - mirror the skill row + agent row + crew-flow; skill count language -> ten skills.

- [ ] **Step 4: Add the `CHANGELOG.md` v0.8.0 entry** at the top:

```markdown
## v0.8.0 - 2026-07-01

### New: Production Designer / world bible (art department, Phase 3)

- Added the `art-direction` skill - a PD interview that produces `art-bible-{show}.md`: the show's global palette (named + hex), material/CMF lexicon, era/genre, a global style reference, and an index of every character/prop/set asset. Inherits the look from `project-context`; written to the user's working folder.
- Added the `production-designer` agent - the art-department counterpart to `director`: sets the world and delegates to casting, costume, makeup-hair, propmaster, and location-scout.
- Added the technical guide `context/guide-art-direction.md` and expanded the Production Design creative section in `reference-craft-artdept.md` (anchored to Ken Adam, Hannah Beachler, Patrice Vermette, and peers).
- Retrofitted the asset skills (`character-sheet`, `prop-turntable`, `location-pack`, `image-edit`) to inherit palette/CMF/style from `art-bible-{show}.md` when present.
- Wired into `skills/build.py` + `plugin/assemble.py`; docs updated to ten skills / eleven agents; crew flow now runs director -> production-designer -> art-dept sub-roles; sources added to `knowledge-base/Miscellaneous-Sources.md`.
```

- [ ] **Step 5: Update `ROADMAP.md`** - mark `### Phase 3 - Production Designer / world bible ✅ *shipped in v0.8.0*` and check off its bullets. Resolve open question §9.1 (art-bible kept as a separate file).

- [ ] **Step 6: Remove promoted + stale stubs.**

```bash
git rm -r roadmap/agents/production-designer.md roadmap/skills/art-direction roadmap/skills/image-edit
```
Then edit `roadmap/README.md`: all Phase 1-3 stubs are now shipped; note that the remaining roadmap work (Phase 4 integration) lives in the existing skills/agents, not stubs. If `roadmap/agents/` or `roadmap/skills/` is now empty, say so in `roadmap/README.md`.

- [ ] **Step 7: Final validate.**

```bash
python plugin/assemble.py
```
Expected: `VALIDATE: OK`.

- [ ] **Step 8: Commit.**

```bash
git add -A
git commit -m "docs: ship v0.8.0 production designer / world bible (README/CHANGELOG/ROADMAP, crew-flow, version, stubs)"
```

---

## Post-plan notes

- **Release (after final whole-branch review + merge):** merge `feat/art-direction` -> `main`; `git tag -a v0.8.0`; `python plugin/assemble.py --package`; `gh release create v0.8.0 generative-cinema.plugin` (keep v0.7.0 / v0.6.0 / v0.5.1). The `.plugin` is gitignored - do not commit it.
- **Then Phase 4 (v0.9.0 - integration & QC)** begins its own spec -> plan -> build -> release cycle.
- After all tasks: `git log --oneline feat/art-direction` should show the spec + 7 task commits.
