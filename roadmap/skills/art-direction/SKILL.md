---
name: art-direction
description: >-
  Define a show's coherent visual WORLD and synthesize it into a reusable
  art-bible-{show}.md — the queryable parent spec that unifies every character, prop,
  and location asset. Use after project-context (the look) when the user says "build
  the world bible", "define the art direction", "set the palette and materials", "what
  world are we in", or "make the assets cohere". Establishes global palette (named +
  hex), a material/CMF lexicon, era/genre, lighting logic, a global style-reference
  image, and an index of every asset. Inherits the LOOK from project-context; parents
  the character-sheet, prop-turntable, and location-pack skills.
---

DRAFT — STUB. Flesh out before promoting to skills/.

# Art-Direction Assistant (the world bible)

Translate the director's intent and the established look into a structured, queryable
**world bible** — `art-bible-{show}.md` — that every asset inherits from. You act like
a Production Designer in prep: you set palette, materials, era, and a global style
reference, then index the world's people, places, and things.

## When to use
After `project-context` (which fixes the *look* — lens, grade, atmosphere) and before
building individual assets. If an `art-bible-{show}.md` exists, refine it.

## Core principle
The bible is a **hard dependency**, not a mood board. Define attributes as fields that
asset prompts are *constructed from* — global palette, material lexicon, default lens &
grade (inherited from project-context), lighting logic, and one global style-reference
image. Lock the global style early; it controls how every model renders skin, fabric,
shadow, and texture.

## Workflow
1. **Inherit the look** from `project-context-{show}.md` (don't restate it).
2. **Interview** for the world: era/genre, palette (named + hex), key materials &
   finishes (CMF), lighting logic, signature environments.
3. **Generate concept-art / key-frame plates** for signature moments (via `shot-prompt`
   / `image-edit`); promote approved ones into the bible as canonical anchors.
4. **Index every asset** — characters, props, locations — with its anchor image path.
5. **Write `art-bible-{show}.md`** from
   [`references/output-template.md`](references/output-template.md).

## References
- [`references/guide-art-direction.md`](references/guide-art-direction.md)
- [`references/guide-asset-reference.md`](references/guide-asset-reference.md)
- [`references/guide-color-story.md`](references/guide-color-story.md)
- [`references/guide-visual-structure.md`](references/guide-visual-structure.md)

## Output
`art-bible-{show}.md`: world ID/logline, palette (hex + names), material lexicon,
default lens/grade/lighting logic, global style-reference path, and the asset index
(characters / props / locations with anchor images). Versioned; promote approved
generations back in so the canon never goes stale.
