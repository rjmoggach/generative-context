# Character Pipeline (Phase 1) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship v0.6.0 — a character-asset pipeline: the `character-sheet` skill, three art-department agents (casting-director, costume-designer, makeup-hair), and the craft library (creative + technical) they read, with typed asset naming and full build wiring.

**Architecture:** `context/` is the single source of truth; `skills/build.py` bundles context files into each skill's `references/` and zips `.skill`s; `plugin/assemble.py` regenerates `plugin/context/` + `plugin/skills/` (repointing links to `${CLAUDE_PLUGIN_ROOT}/context/`) and **validates** dead links + agent YAML. There is no unit-test framework — the verification gate is `python plugin/assemble.py` printing `VALIDATE: OK` and `python skills/build.py` running clean.

**Tech Stack:** Markdown (library + skills + agents), Python 3 stdlib build scripts, JSON manifests. Spec: `docs/superpowers/specs/2026-06-30-character-pipeline-design.md`.

## Global Constraints

- **Target version:** `0.6.0` — set verbatim in `plugin/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` (both the `metadata.version` and the plugin entry `version`), and README banners.
- **Library format for `guide-*.md`:** heuristic decision-unit — `**Decision / Use when / Because / Prompt translation / Watch-outs / Anchors.**`
- **Library format for `reference-*.md`:** knowledge catalog with anchor tables (sibling of `reference-visual-*.md`).
- **Formatting:** standard Markdown; no emojis; plain hyphens (no em/en dashes); straight quotes; technical terms in `` `code` ``. No `[PLACEHOLDER]` output in any shipped file.
- **Asset naming (canonical, defined in Task 1):** type codes `char · prop · set · veh · cam · light · style · fx`; spec file `{type}-{show}-{name}.md`; folder `assets/{type}/{name}/`; image `{type}-{name}-{facet}-{view}[-vNN].png`; facets `id · turn · fit · hmu`; views `front/back/side-l/side-r/3q-l/3q-r`; all lowercase kebab.
- **Asset binaries live in the user's working folder only** — never committed to the plugin repo.
- **LoRA = advise-only + record trigger word** — the plugin never trains.
- **Agent frontmatter (strict YAML, required keys):** `name`, `description`, `model`, `color`, `tools`. Use `model: inherit`, `tools: ["Read", "Grep", "Glob"]`. No raw `<example>` tags in frontmatter (assemble.py rejects them).
- **Branch:** `feat/character-pipeline` (already created). Commit after each task.

---

### Task 1: Naming & storage section in `guide-asset-reference.md`

**Files:**
- Modify: `context/guide-asset-reference.md` (append a new numbered section before "Quick application", and add one line to "Quick application")

**Interfaces:**
- Produces: the canonical asset naming taxonomy that Tasks 2, 5, 6, 9 reference by pointing at `guide-asset-reference.md`. No code symbols.

- [ ] **Step 1: Add the "Naming & storage" section.** Insert after the current `## 8. Inherit top-down` section and before `## Quick application`. Use this exact content:

```markdown
## 9. Naming & storage (the asset taxonomy)

- **Use when:** creating any asset spec or image so a human or a fresh agent can
  read `assets/` and know what everything is.
- **Because:** typed, coded, versioned names are self-describing and let new asset
  types slot in without redesign.
- **Prompt translation — the convention:**

  **Type codes** (reserved; `char` is built first): `char` (character) - `prop` -
  `set` (location/environment) - `veh` (vehicle) - `cam` - `light` - `style` - `fx`.

  ```
  Spec file     {type}-{show}-{name}.md          char-sbw-eli.md
  Asset folder  assets/{type}/{name}/            assets/char/eli/   (type-first, so
                                                  assets/char/ lists every character)
  Image files   {type}-{name}-{facet}-{view}[-vNN].png
    identity    char-eli-id-front.png   char-eli-id-3q-l.png
    turnaround  char-eli-turn-front.png  -side-l / -side-r / -back / -3q-l / -3q-r
    wardrobe    char-eli-fit-day1.png    char-eli-fit-day2-wet.png
    hmu         char-eli-hmu-clean.png   char-eli-hmu-wound-01.png
  ```

  Facets: `id` - `turn` - `fit` - `hmu`. Views: `front/back/side-l/side-r/3q-l/3q-r`.
  All lowercase kebab-case; `-vNN` version suffix optional.
- **Watch-outs:** everything the model writes goes to the **user's working folder**,
  never the plugin repo; keep names ASCII and kebab so paths stay portable.
- **Anchors:** VFX/game asset-management naming (type-first hierarchy, versioned).
```

- [ ] **Step 2: Add one bullet to "Quick application".** In the existing `## Quick application` numbered list, add a final item:

```markdown
7. Name and store per the **asset taxonomy** (§9): `{type}-{show}-{name}.md` +
   `assets/{type}/{name}/`, in the user's working folder.
```

- [ ] **Step 3: Verify.** Confirm the section reads cleanly, no em-dashes/emojis, code fences balanced. `grep -n "assets/{type}" context/guide-asset-reference.md` returns the new lines.

- [ ] **Step 4: Commit.**

```bash
git add context/guide-asset-reference.md
git commit -m "feat(context): add asset naming & storage taxonomy to guide-asset-reference

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 2: `reference-craft-character.md` (creative craft) + record sources

**Files:**
- Create: `context/reference-craft-character.md`
- Modify: `knowledge-base/Miscellaneous-Sources.md` (append three entries)

**Interfaces:**
- Produces: `context/reference-craft-character.md` (bundled by Tasks 5 & 7; read by agents in Task 6).

- [ ] **Step 1: Write `context/reference-craft-character.md`.** Knowledge-catalog format (like `reference-visual-*.md`). Required structure:
  - H1 `# Character Craft — Casting, Costume, Makeup & Hair` + a 2-3 sentence intro stating this is the *creative* companion to the technical `guide-character-consistency.md` / `guide-turnaround-sheets.md`, and that each role is dual (art + tool).
  - `## Casting — presence, typage, chemistry` — 4-6 prose principles: (1) the face tells a story before a line is spoken; (2) typage vs casting-against-type; (3) presence/watchability over conventional looks; (4) ensemble chemistry and contrast; (5) what a casting director reads for in an audition. Then a `### Anchors` table (columns: Casting director | Signature | Known for | When to reference) with real names: **Marion Dougherty**, **Juliet Taylor**, **Janet Hirshenson & Jane Jenkins**, **Ellen Lewis**, **Nina Gold**.
  - `## Costume — wardrobe as character` — principles: (1) silhouette first; (2) colour-as-character (tie to `guide-color-story.md`); (3) status/period/era legibility; (4) the costume *arc* across a story; (5) distressing/aging as narrative; (6) costume vs fashion. Then `### Anchors` table with: **Edith Head**, **Colleen Atwood**, **Sandy Powell**, **Ruth E. Carter**, **Milena Canonero**, **Jacqueline Durran**.
  - `## Makeup & Hair — the invisible craft` — principles: (1) the "no-makeup" naturalistic look; (2) aging and its tells; (3) wounds/SFX/prosthetics as storytelling; (4) hair as silhouette and era marker; (5) continuity as discipline (reproduce identically regardless of shoot order). Then `### Anchors` table with: **Rick Baker**, **Ve Neill**, **Greg Cannom**, **Kazu Hiro**.
  - `## How this feeds the pipeline` — 3-5 lines connecting each department's art to what the `character-sheet` skill locks (identity descriptor, wardrobe/HMU states) so creative intent survives into the reference asset.
  - Format rules per Global Constraints (no emojis/em-dashes; straight quotes).

- [ ] **Step 2: Append sources to `knowledge-base/Miscellaneous-Sources.md`.** Match the file's existing `## Author, _Title_` + note + URL-bullet format. Append:

```markdown
## Janet Hirshenson & Jane Jenkins, _A Star Is Found_

the casting director's craft: presence, chemistry, reading an audition, star-making.

- https://www.goodreads.com/book/show/398485.A_Star_Is_Found

## Deborah Nadoolman Landis, _FilmCraft: Costume Design_ / _Dressed_

wardrobe as character; sixteen designers on envisioning character through clothes; a century of Hollywood costume.

- https://books.google.com/books/about/FilmCraft_Costume_Design.html?id=3yCkCgAAQBAJ
- https://www.deborahlandis.com/publications

## Penny Delamar, _The Complete Make-Up Artist_ (with Richard Corson, _Stage Makeup_)

film/TV/theatre makeup craft: naturalistic looks, aging, SFX, and continuity discipline.

- https://www.amazon.com/Complete-Make-Up-Artist-Working-Television/dp/0810119692
```

- [ ] **Step 3: Verify.** `grep -c "^## " context/reference-craft-character.md` shows the expected section count (>= 4); every anchor table has a header row + separator; `grep -n "A Star Is Found" knowledge-base/Miscellaneous-Sources.md` finds the new entry.

- [ ] **Step 4: Commit.**

```bash
git add context/reference-craft-character.md knowledge-base/Miscellaneous-Sources.md
git commit -m "feat(context): add reference-craft-character (creative craft) + sources

Casting/costume/makeup-hair artistry with real-master anchor tables,
grounded in Hirshenson-Jenkins, Nadoolman Landis, Delamar/Corson.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 3: `guide-character-consistency.md` (technical craft)

**Files:**
- Create: `context/guide-character-consistency.md`

**Interfaces:**
- Produces: `context/guide-character-consistency.md` (bundled by Tasks 5 & 7; read by casting-director & makeup-hair agents in Task 6).

- [ ] **Step 1: Write the guide.** Heuristic decision-unit format. Open with a 2-3 line intro: this is the *character-specific technical* craft; the general spine is `guide-asset-reference.md`, the creative craft is `reference-craft-character.md`, and the derive engine is `guide-image-editing.md` — do not duplicate them. Required numbered sections (each a decision unit where applicable):
  1. **The hero identity reference** — the anchor portrait spec: front-facing, evenly lit, neutral expression, high-res, neutral background; why it's the single most load-bearing asset; watch-outs (angled/expressive/low-res anchors poison downstream).
  2. **The descriptor block (50-80 words, verbatim)** — how to write it: face, hair, body, locked wardrobe, accessories, HMU state, distinctive marks; pin hex colours, garment names, silhouette; reused verbatim as the identity block; example block (~60 words) for a sample character.
  3. **Drift failure modes + fixes** — table (Failure | Cause | Fix): face morphs across shots, wardrobe colour shifts, age/weight drift, micro-detail loss (freckles/logos), light-key flip changing identity; fixes tie to hold-the-key, edit-don't-regenerate, 30°+size change.
  4. **Wardrobe-state library** — lock garments by name + silhouette + hex; track states (clean/wet/damaged/day-1/day-2); each state independently lockable; progress by editing the prior state.
  5. **HMU-state library** — clean/aged/wounded/wet; pin injuries by position + side + size + hex; progress wounds by editing the previous state (fresh -> scabbed -> scarred), never regenerating.
  6. **Reference vs LoRA — for faces** — the decision gate: <= ~1 scene -> reference only (~65-75%); recurring hero -> reference + LoRA + fixed descriptor (~85-92%), **record the LoRA trigger word in the character file**; background/one-off -> reference only. Note the plugin advises but does not train.
  - Close with a `## Quick application` list and a companion-guides line pointing to `guide-asset-reference.md`, `reference-craft-character.md`, `guide-turnaround-sheets.md`, `guide-image-editing.md`.

- [ ] **Step 2: Verify.** `grep -n "Decision" context/guide-character-consistency.md` shows the decision-unit format is used; confirm the example descriptor block is 50-80 words; no `[PLACEHOLDER]`.

- [ ] **Step 3: Commit.**

```bash
git add context/guide-character-consistency.md
git commit -m "feat(context): add guide-character-consistency (technical face/wardrobe/HMU craft)

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 4: `guide-turnaround-sheets.md` (technical craft)

**Files:**
- Create: `context/guide-turnaround-sheets.md`

**Interfaces:**
- Produces: `context/guide-turnaround-sheets.md` (bundled by Tasks 5 & 7; read by costume-designer agent in Task 6).

- [ ] **Step 1: Write the guide.** Heuristic format. Intro: model-sheet conventions for building a geometry-true turnaround from the hero anchor via `image-edit`. Required sections:
  1. **The view set** — front (the anchor) - side-l - side-r - back - 3q-l - 3q-r; why each view; map to the `turn` facet filenames from the taxonomy (`char-eli-turn-front.png`, etc.).
  2. **Alignment lines** — hold eye/shoulder/waist/knee/foot lines constant across views; consistent scale, neutral A-pose, even flat lighting, neutral background; why alignment makes the sheet usable as a multi-angle reference.
  3. **Derive from the anchor, never independently** — each view is an `image-edit` of the anchor at low-moderate denoise with the descriptor block held verbatim; rotate the subject, keep identity; cross-ref `guide-asset-reference.md` §1 (anchor-then-fan-out) and `guide-image-editing.md`.
  4. **Companion sheets** — expression sheet, pose sheet, palette/callout sheet; when each is worth building; keep them consistent with the turnaround's light and scale.
  5. **Reference counts** — ~4-6 views is the consistency sweet spot, strength ~0.7; verify per-model limits against `model-currency-2026-06.md`.
  - Close with `## Quick application` + companion-guides line.

- [ ] **Step 2: Verify.** `grep -n "char-eli-turn" context/guide-turnaround-sheets.md` finds the taxonomy-aligned filenames; decision-unit format present; no em-dashes/emojis.

- [ ] **Step 3: Commit.**

```bash
git add context/guide-turnaround-sheets.md
git commit -m "feat(context): add guide-turnaround-sheets (model-sheet view/alignment craft)

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 5: `character-sheet` skill + output template

**Files:**
- Create: `skills/character-sheet/SKILL.md`
- Create: `skills/character-sheet/references/character-template.md`

**Interfaces:**
- Consumes: `context/reference-craft-character.md`, `guide-character-consistency.md`, `guide-turnaround-sheets.md`, `guide-asset-reference.md`, `guide-image-editing.md`, `model-currency-2026-06.md`, and editing/image model docs (bundled into `references/` by Task 7's `build.py` run).
- Produces: `skills/character-sheet/SKILL.md` (repointed + validated in Task 7); `character-template.md` (registered as an assemble HELPER in Task 7).

- [ ] **Step 1: Write `skills/character-sheet/SKILL.md`.** Promote the roadmap stub (`roadmap/skills/character-sheet/SKILL.md`) into a real skill. Frontmatter: `name: character-sheet` + a `description:` (multi-line `>-`) with trigger phrases ("build a character sheet", "lock this character", "make a turnaround / model sheet", "create the hero reference for X", "keep this person consistent across shots", "design this character"). Body sections:
  - **Purpose** — build the single most load-bearing asset; identity lives in the asset, downstream prompts carry only change.
  - **When to use** — a character recurring across >1 shot, or any turnaround/model-sheet/hero-reference request; refine in place if the file exists.
  - **Core principle: anchor, then fan out** — hero identity ref first, derive all views/states via reference conditioning + `image-edit`.
  - **Step 1 — Load craft** — read `references/reference-craft-character.md` (creative), `references/guide-character-consistency.md`, `references/guide-turnaround-sheets.md`, `references/guide-asset-reference.md`, `references/guide-image-editing.md`. If a show is loaded, inherit `project-context-{show}.md` (prefix/palette/lens/forbidden terms).
  - **Step 2 — Identity (casting)** — hero portrait + multi-angle bundle; write the 50-80-word descriptor block; call the reference-vs-LoRA gate; record the trigger word if a LoRA is advised.
  - **Step 3 — Turnaround + wardrobe (costume)** — front-anchor turnaround on the alignment lines; lock garments by name + silhouette + hex; wardrobe states.
  - **Step 4 — HMU states (makeup-hair)** — clean/aged/wounded/wet state library; pin injuries position+side+size+hex; progress by editing the prior state.
  - **Step 5 — Model + references** — pick the i2i model; confirm reference-count/strength vs `references/model-currency-2026-06.md`; read the matching `references/models/model-*.md`.
  - **Step 6 — Output** — write `char-{show}-{name}.md` per `references/character-template.md` into the **user's working folder**; save images under `assets/char/{name}/` using the taxonomy filenames; state the descriptor block prominently so `shot-prompt`/`image-edit` can paste it verbatim.
  - **Critical rules** — anchor before fan-out; descriptor block verbatim; hex/garment/wound pinned; hold the light-key; edit don't regenerate for progressions; binaries to the user's folder only; verify counts vs currency.
  - Link references with `](references/...)` and `](references/models/...)` paths (assemble.py repoints these).

- [ ] **Step 2: Write `skills/character-sheet/references/character-template.md`.** The output skeleton the skill fills. Include: H1 `# {SHOW} - {Name} - Character Sheet`; `## Identity` (descriptor block callout; hero + turnaround image paths under `assets/char/{name}/`; the reference-vs-LoRA decision + `LoRA trigger word:` field); `## Wardrobe` (per-costume: name, silhouette, hex, state, image paths); `## Makeup & Hair` (per-state: name, injury/aging spec position+side+size+hex, image paths); `## Reference notes` (counts/strength used, model). Show the taxonomy paths as real examples (`assets/char/eli/char-eli-id-front.png`). Standard Markdown, no emojis/em-dashes.

- [ ] **Step 3: Verify.** `grep -n "](references/" skills/character-sheet/SKILL.md` lists the reference links; confirm the frontmatter has `name` + `description` and parses (no tabs); template contains the three sections + LoRA trigger field.

- [ ] **Step 4: Commit.**

```bash
git add skills/character-sheet/SKILL.md skills/character-sheet/references/character-template.md
git commit -m "feat(skills): add character-sheet skill + character output template

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 6: Three art-department agents

**Files:**
- Create: `plugin/agents/casting-director.md`
- Create: `plugin/agents/costume-designer.md`
- Create: `plugin/agents/makeup-hair.md`

**Interfaces:**
- Consumes: `${CLAUDE_PLUGIN_ROOT}/context/reference-craft-character.md`, `guide-character-consistency.md`, `guide-turnaround-sheets.md` (present in `plugin/context/` after Task 7's assemble run).
- Produces: three agent files that pass `assemble.py`'s strict-YAML frontmatter validation.

- [ ] **Step 1: Write `plugin/agents/casting-director.md`.** Frontmatter (verbatim keys):

```markdown
---
name: casting-director
description: >-
  The Casting Director. Lock a character's identity — the hero reference and the
  50-80 word descriptor block — so every later shot carries the same face. Use when
  the user says "cast this character", "lock this identity", "create the hero
  reference for X", or "who is this person". Owns typage, presence, and chemistry;
  applies the character-sheet identity craft. Reads the creative craft and the
  technical consistency guide; hands the locked identity to the costume-designer and
  makeup-hair.
model: inherit
color: red
tools: ["Read", "Grep", "Glob"]
---
```
  Body: persona (a casting director who reads for presence/typage/chemistry, per `reference-craft-character.md` Casting); when it fires; method (read `${CLAUDE_PLUGIN_ROOT}/context/reference-craft-character.md` + `guide-character-consistency.md` + `guide-asset-reference.md`; build the hero identity anchor + descriptor block + reference-vs-LoRA call); output (the Identity section of `char-{show}-{name}.md` + hero/identity image paths). Decide identity; hand off wardrobe/HMU to the sibling agents.

- [ ] **Step 2: Write `plugin/agents/costume-designer.md`.** Same frontmatter shape, `name: costume-designer`, `color: orange`. Body: persona (wardrobe as character — silhouette, colour, status, arc, distressing, per `reference-craft-character.md` Costume); also owns model-sheet/turnaround craft; method (read Costume craft + `guide-turnaround-sheets.md` + `guide-character-consistency.md`; build the turnaround on the alignment lines; lock garments by name+silhouette+hex; wardrobe states); output (the Turnaround + Wardrobe sections + `assets/char/{name}/char-{name}-turn-*.png` and `-fit-*.png`).

- [ ] **Step 3: Write `plugin/agents/makeup-hair.md`.** Same shape, `name: makeup-hair`, `color: purple`. Body: persona (HMU continuity, aging, wounds/SFX as story, per `reference-craft-character.md` Makeup & Hair); method (read Makeup craft + `guide-character-consistency.md`; build the HMU state library clean/aged/wounded/wet; pin injuries position+side+size+hex; progress by editing prior state); output (the Makeup & Hair section + `char-{name}-hmu-*.png`).

- [ ] **Step 4: Verify frontmatter keys.** For each file:

```bash
for a in casting-director costume-designer makeup-hair; do
  echo "== $a =="; sed -n '1,12p' plugin/agents/$a.md
done
```
Expected: each shows `---` fences with `name/description/model/color/tools` and no raw `<` lines in frontmatter.

- [ ] **Step 5: Commit.**

```bash
git add plugin/agents/casting-director.md plugin/agents/costume-designer.md plugin/agents/makeup-hair.md
git commit -m "feat(agents): add casting-director, costume-designer, makeup-hair crew

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 7: Build wiring + integration validation (the gate)

**Files:**
- Modify: `skills/build.py` (add `character-sheet` to `MANIFEST`)
- Modify: `plugin/assemble.py` (add `character-sheet` to `SKILLS`; add `character-template.md` to `HELPERS`)

**Interfaces:**
- Consumes: all files from Tasks 1-6.
- Produces: populated `skills/character-sheet/references/`, `plugin/context/*`, `plugin/skills/character-sheet/SKILL.md`; a passing `VALIDATE: OK`.

- [ ] **Step 1: Add the `character-sheet` MANIFEST entry to `skills/build.py`.** Insert into the `MANIFEST` dict (after the `image-edit` entry):

```python
    "character-sheet": [
        ("reference-craft-character.md", "references/reference-craft-character.md"),
        ("guide-character-consistency.md", "references/guide-character-consistency.md"),
        ("guide-turnaround-sheets.md", "references/guide-turnaround-sheets.md"),
        ("guide-asset-reference.md", "references/guide-asset-reference.md"),
        ("guide-image-editing.md", "references/guide-image-editing.md"),
        ("model-currency-2026-06.md", "references/model-currency-2026-06.md"),
        ("model-editing-flux-kontext.md", "references/models/model-editing-flux-kontext.md"),
        ("model-image-gemini-flash.md", "references/models/model-image-gemini-flash.md"),
        ("model-image-seedream-4.md", "references/models/model-image-seedream-4.md"),
        ("model-image-flux-pro.md", "references/models/model-image-flux-pro.md"),
    ],
```

- [ ] **Step 2: Register the skill + helper in `plugin/assemble.py`.** Add `"character-sheet"` to the `SKILLS` list:

```python
SKILLS = ["project-context", "sequence-design", "shot-prompt", "model-docs", "footage-transform", "image-edit", "character-sheet"]
```
And append to the `HELPERS` list:

```python
    SKILLS_SRC / "character-sheet/references/character-template.md",
```

- [ ] **Step 3: Run the skill build (syncs bundled references + zips).**

```bash
python skills/build.py
```
Expected: `sync  character-sheet: ...` lines for each manifest pair, then `zip   skills/dist/character-sheet.skill  (... bytes)`. No traceback.

- [ ] **Step 4: Run assemble + validate (the integration gate).**

```bash
python plugin/assemble.py
```
Expected: `context/: N files`, `skill: character-sheet` (among others), and final line `VALIDATE: OK`. If it prints `FAIL ...`, fix the named missing reference/agent and re-run before committing.

- [ ] **Step 5: Commit** (include the generated `skills/character-sheet/references/` and `plugin/` outputs the scripts produced).

```bash
git add skills/build.py plugin/assemble.py skills/character-sheet/references plugin/context plugin/skills
git commit -m "build: wire character-sheet skill into build.py + assemble.py

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 8: Docs, version bump, stub removal + final validate

**Files:**
- Modify: `README.md`, `plugin/README.md`, `CHANGELOG.md`, `ROADMAP.md`
- Modify: `plugin/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`
- Delete: `roadmap/skills/character-sheet/` (and its `SKILL.md`), `roadmap/agents/casting-director.md`, `roadmap/agents/costume-designer.md`, `roadmap/agents/makeup-hair.md`
- Modify: `roadmap/README.md` (drop the removed stubs from the listing)

**Interfaces:**
- Consumes: the shipped skill/agents/guides from Tasks 1-7.

- [ ] **Step 1: Bump versions to `0.6.0`.** In `plugin/.claude-plugin/plugin.json` set `"version": "0.6.0"`. In `.claude-plugin/marketplace.json` set both `metadata.version` and the plugin entry `version` to `"0.6.0"`. Update the README banners: `README.md` line ~3 `**Version**: 0.6.0` and any version string in `plugin/README.md`.

- [ ] **Step 2: Update `README.md`.** Add a `character-sheet` row to the Skills table (Level: Asset - "Build a persistent character reference: hero identity, turnaround, wardrobe + HMU states"); add three rows to the Agents table (casting-director / costume-designer / makeup-hair with their one-line asks); add `reference-craft-character`, `guide-character-consistency`, `guide-turnaround-sheets` to the craft-guides paragraph; note the `assets/{type}/{name}/` convention. Keep the model list unchanged.

- [ ] **Step 3: Update `plugin/README.md`.** Mirror the skill row + 3 agent rows + shared-library mention. Skill count language updated to seven skills.

- [ ] **Step 4: Add the `CHANGELOG.md` entry** at the top:

```markdown
## v0.6.0 - 2026-06-30

### New: Character pipeline (art department, Phase 1)

- Added the `character-sheet` skill — build a persistent, re-attachable character reference (hero identity + descriptor block, turnaround/model sheet, wardrobe states, makeup/hair states) that downstream shots carry identity from. Anchor-then-fan-out; uses `image-edit` as the derive engine; output written to the user's working folder.
- Added three art-department agents: `casting-director` (identity), `costume-designer` (turnaround + wardrobe), `makeup-hair` (HMU states) — facets of one `char-{show}-{name}.md` asset.
- Added creative craft `context/reference-craft-character.md` (casting/costume/makeup-hair artistry with real-master anchors) and technical guides `guide-character-consistency.md` + `guide-turnaround-sheets.md`.
- Added the typed asset naming taxonomy to `guide-asset-reference.md` (`{type}-{show}-{name}.md`, `assets/{type}/{name}/`; codes char/prop/set/veh/cam/light/style/fx).
- Wired into `skills/build.py` + `plugin/assemble.py`; docs updated to seven skills; sources added to `knowledge-base/Miscellaneous-Sources.md`.
```

- [ ] **Step 5: Update `ROADMAP.md`.** Change the Phase 1 heading to `### Phase 1 - Character pipeline ✅ *shipped in v0.6.0*`, check off its bullets, and update any `character-{show}-{name}.md` / `/assets/character-{name}/` references to the taxonomy in `guide-asset-reference.md` §9.

- [ ] **Step 6: Remove promoted stubs.**

```bash
git rm -r roadmap/skills/character-sheet roadmap/agents/casting-director.md roadmap/agents/costume-designer.md roadmap/agents/makeup-hair.md
```
Then edit `roadmap/README.md` to drop `character-sheet`, `casting-director`, `costume-designer`, `makeup-hair` from the "What's here" listing (leave the remaining Phase 2/3 stubs).

- [ ] **Step 7: Final validate** (docs don't affect the build, but confirm nothing regressed).

```bash
python plugin/assemble.py
```
Expected: `VALIDATE: OK`.

- [ ] **Step 8: Commit.**

```bash
git add -A
git commit -m "docs: ship v0.6.0 character pipeline (README/CHANGELOG/ROADMAP, version, stubs)

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Post-plan notes

- **`.plugin` release is a maintainer step** — run `python plugin/assemble.py --package` and attach `generative-cinema.plugin` to a GitHub Release `v0.6.0` (or use the `claude-mem:version-bump` skill). Not performed by this plan.
- After all tasks: `git log --oneline feat/character-pipeline` should show the spec + 8 task commits; open a PR against `main` when ready.
