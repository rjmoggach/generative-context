---
name: character-sheet
description: >-
  Build or refresh a persistent character reference asset — character-{show}-{name}.md
  plus a folder of locked reference images — that holds a character's face, body,
  wardrobe, and makeup/hair consistent across every shot. Use when the user says "build
  a character sheet", "lock this character", "make a turnaround / model sheet", "create
  the hero reference for X", "keep this person consistent across shots", or "design this
  character". Produces the identity (casting), turnaround + wardrobe (costume), and HMU
  states (makeup-hair) as one unified asset. The output is the reference the shot-prompt
  and image-edit skills attach to carry identity.
---

DRAFT — STUB. Flesh out before promoting to skills/.

# Character-Sheet Assistant

Build the single most load-bearing asset in the pipeline: a unified, persistent
character reference. Identity lives in this asset; downstream prompts carry only change.

## When to use
Whenever a character will recur across more than one shot, or when the user wants a
turnaround / model sheet / hero reference. Refine in place if the file exists.

## Core principle: anchor, then fan out
Generate one clean **hero identity reference** first (front-facing, evenly-lit, neutral,
high-res), then derive every other view and state *from it* via reference conditioning
and the `image-edit` skill — never generate views independently.

## Workflow (the three facets, one asset)
1. **Identity (casting):** hero portrait + multi-angle bundle; write the locked
   descriptor block (50–80 words, reused verbatim); call the reference-vs-LoRA gate.
2. **Turnaround + wardrobe (costume):** front (anchor) · side · back · ¾×2 aligned on
   eye/shoulder/waist/knee/foot lines; lock garments by name + silhouette + hex; track
   costume states. Add expression/pose companion sheets if useful.
3. **HMU states (makeup-hair):** a small state library (clean / aged / wounded / wet),
   each independently lockable; pin injuries by position+side+size+hex; progress by
   editing the previous state.

## References
- [`references/guide-character-consistency.md`](references/guide-character-consistency.md)
- [`references/guide-turnaround-sheets.md`](references/guide-turnaround-sheets.md)
- [`references/guide-asset-reference.md`](references/guide-asset-reference.md)
- [`references/guide-image-editing.md`](references/guide-image-editing.md)

## Reference counts
~4–6 reference images is the consistency sweet spot; reference strength ~0.7. Verify
per-model limits against `model-currency` (version-sensitive).

## Output
`character-{show}-{name}.md` with three sections (identity / wardrobe / HMU), each with
image paths, plus `/assets/character-{name}/` holding the locked images. State the
descriptor block prominently so other skills can paste it verbatim.
