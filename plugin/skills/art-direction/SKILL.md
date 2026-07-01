---
name: art-direction
description: >-
  Build the queryable world spec that sits above the asset layer — the Production
  Designer's counterpart to project-context. Synthesizes global palette (named +
  hex), a CMF material/finish/texture lexicon, era/genre rules, a locked global
  style-reference image, and an index of every asset into art-bible-{show}.md:
  the parent spec every character, prop, and set inherits from. Use after
  project-context exists and before (or alongside) building individual assets;
  if art-bible-{show}.md already exists, refine it in place. Trigger phrases:
  "define the world", "build the art bible", "set the palette and materials",
  "create the world bible", "art-direct this show", "what's our CMF".
---

# Art-Direction Assistant

Build the single most load-bearing world document in the pipeline: a unified,
queryable `art-bible-{show}.md` — the parent spec that every character, prop,
and set asset inherits from. You act like a Production Designer in prep: you lock
palette, materials, era, and a global style reference, then index every asset in
the world. Downstream asset skills (`character-sheet`, `prop-turntable`,
`location-pack`) construct their prompts directly from the bible's fields — not
loosely inspired by them.

## When to use

After `project-context` — which fixes the *look* (lens, grade, atmosphere, and
baseline palette) — and before building individual assets. Refine in place if
`art-bible-{show}.md` already exists: update only the changed section and re-audit
the asset index. The art bible is not a replacement for project-context; it is the
world spec that inherits from it.

## Core principle

The bible is a **hard dependency**, not a mood board. Every field must be defined
precisely enough to be *constructed from* directly: a palette entry is
`{name}, {hex}, {finish}`; a CMF entry is
`{short-name}: {material call}, {finish call}, {texture note}`; a world rule is a
checkable constraint, not a tonal description. Lock the global style reference
early — it anchors the visual register (light quality, surface feel, color
temperature, tonal contrast) in a form no prose can substitute. The bible tells
the pipeline *what world to build*; project-context tells it *how to work*.

## Step 1 — Load

Read these before writing any world spec:

- `project-context-{show}.md` — inherit the Standard Prompt Prefix, lens spec,
  grade, baseline palette, forbidden terms, and atmosphere. Do not restate these
  in the bible; cross-reference them.
- [`references/reference-craft-artdept.md`](${CLAUDE_PLUGIN_ROOT}/context/reference-craft-artdept.md) —
  Production Design creative foundation: world authorship, CMF as world language,
  top-down inheritance.
- [`references/guide-art-direction.md`](${CLAUDE_PLUGIN_ROOT}/context/guide-art-direction.md) —
  art-bible mechanics: palette structure, CMF lexicon, era/genre rules, asset
  index format, top-down inheritance.
- [`references/guide-asset-reference.md`](${CLAUDE_PLUGIN_ROOT}/context/guide-asset-reference.md) —
  anchor-then-fan-out, identity block discipline, the asset taxonomy (§9).
- [`references/guide-color-story.md`](${CLAUDE_PLUGIN_ROOT}/context/guide-color-story.md) —
  color scheme, associative/transitional color, temperature contrast.
- [`references/guide-image-editing.md`](${CLAUDE_PLUGIN_ROOT}/context/guide-image-editing.md) —
  i2i mechanics for generating and locking the global style reference.

## Step 2 — Define the world

Run a guided interview — one question at a time, conversationally — to lock the
world's hard constraints. Map answers directly to bible fields; never leave a
field in loose prose.

**Global palette.** Establish named colors with hex codes and explicit
dominant/accent roles. Every surface description in an asset prompt will take the
form `{name}, {hex}, {finish}` — set those names and pins now. Consult
[`references/guide-color-story.md`](${CLAUDE_PLUGIN_ROOT}/context/guide-color-story.md) for scheme
(complementary, analogous, monochromatic), temperature contrast, and associative
color. The palette block structure follows guide-art-direction §2:

| Role     | Name           | Hex     | Finish notes              |
|----------|----------------|---------|---------------------------|
| Dominant | {color-name}   | #{hex}  | matte / satin / gloss     |
| Accent   | {color-name}   | #{hex}  | {finish}                  |
| Skin ref | {color-name}   | #{hex}  | subsurface, not a surface |

**CMF lexicon.** Define the shared material/finish/texture vocabulary for every
surface class the world uses. Write each entry in the form
`{short-name}: {material call}, {finish call}, {texture note}` — for example:
`aged-brass: cast brass, verdigris patina, slight surface relief at seams` /
`raw-concrete: poured concrete, unsealed, fine aggregate visible, hairline cracks at joints`.
Do not invent new CMF terms per asset; add to the lexicon first, then apply it.

**Era / genre / world rules.** Enumerate hard constraints: period, genre register,
technology level, entropy level (pristine / lived-in / decayed / ruined). Format
each as a checkable rule, not a tonal note. Every asset must pass this list before
being locked. Prepend the era/genre block to first-generation asset prompts as a
single orienting line: `World: {era}, {genre register}, {technology level}, {entropy level}.`

## Step 3 — Lock the global style reference

Generate one global style-reference image via `image-edit` using mood-board inputs
guided by the palette, CMF, and era/genre rules just locked. This image is not an
asset — it depicts no specific character, prop, or set. It anchors the visual
register of the world itself. Generate until one image captures the world's feel,
then lock it at `assets/style/style-{show}-global.png`.

Identify the target model for this i2i work (ask once if unstated; prefer the
model already in use for the project). Load the relevant model doc for
source/reference syntax and denoise/strength controls:

- FLUX.1 Kontext: [`references/models/model-editing-flux-kontext.md`](${CLAUDE_PLUGIN_ROOT}/context/model-editing-flux-kontext.md)
- Gemini Flash: [`references/models/model-image-gemini-flash.md`](${CLAUDE_PLUGIN_ROOT}/context/model-image-gemini-flash.md)
- Seedream 4: [`references/models/model-image-seedream-4.md`](${CLAUDE_PLUGIN_ROOT}/context/model-image-seedream-4.md)
- FLUX.1 Pro: [`references/models/model-image-flux-pro.md`](${CLAUDE_PLUGIN_ROOT}/context/model-image-flux-pro.md)

Before quoting any reference-count or strength values, verify against
[`references/model-currency-2026-06.md`](${CLAUDE_PLUGIN_ROOT}/context/model-currency-2026-06.md) —
per-model limits change monthly.

Record in the bible: the locked style-ref path and the inherited lens/grade from
`project-context-{show}.md` that the image implies. These must be stated explicitly
in the bible and cross-referenced from project-context, not left to be inferred
from the image alone.

## Step 4 — Build the asset index

Scan the user's working folder for existing `char-{show}-*`, `prop-{show}-*`, and
`set-{show}-*` spec files. For each locked asset — anchored and spec-filed — add
one row to the asset index. Do not list assets that are not yet locked; a partial
asset in the index implies it is safe to reference, which it is not.

Index table format (guide-art-direction §6; guide-asset-reference §9):

| Type   | Name     | Spec file               | Anchor image path                             |
|--------|----------|-------------------------|-----------------------------------------------|
| `char` | `{name}` | `char-{show}-{name}.md` | `assets/char/{name}/char-{name}-id-front.png` |
| `prop` | `{name}` | `prop-{show}-{name}.md` | `assets/prop/{name}/prop-{name}-hero.png`     |
| `set`  | `{name}` | `set-{show}-{name}.md`  | `assets/set/{name}/set-{name}-plate.png`      |

Spec-file names carry `{show}`; image-file names do not.

## Step 5 — Output

Write `art-bible-{show}.md` to the **user's working folder** — never to the plugin
repo — using the structure in [`references/art-bible-template.md`](${CLAUDE_PLUGIN_ROOT}/context/art-bible-template.md).
The bible must be queryable: every field labeled, every palette entry hex-pinned,
every CMF term explicitly defined, every world rule a checkable constraint, every
asset index row pointing to a real locked file.

Tell the user the art bible is the primary input to `character-sheet`,
`prop-turntable`, and `location-pack`; those skills inherit palette, CMF lexicon,
era/genre rules, and the global style-ref path from it.

## Critical rules

1. **Inherit, never replace.** The bible inherits lens, grade, and baseline palette
   from `project-context-{show}.md`. Cross-reference; do not duplicate. If
   project-context changes, update it first, then the bible.
2. **Pin palette hex and CMF names.** Named colors without hex drift across agents
   and sessions. CMF terms without a precise material/finish/texture call drift
   across models. Lock both before any asset is built.
3. **The asset index uses taxonomy paths exactly.** Spec-file names carry `{show}`;
   image filenames do not. Paths follow guide-asset-reference §9.
4. **Index only locked assets.** An unlocked asset in the index sends agents to a
   path that may not exist. Update the index when assets are locked; keep it live.
5. **Binaries to the user's working folder only.** The style-reference image and all
   asset images go to the user's folder; nothing writes to the plugin repo.
6. **Verify model references against currency.** Reference counts, strength values,
   and per-model limits are version-sensitive — always check
   [`references/model-currency-2026-06.md`](${CLAUDE_PLUGIN_ROOT}/context/model-currency-2026-06.md)
   before advising any specific value.
