---
name: prop-turntable
description: >-
  Build or refresh a prop reference asset — prop-{show}-{name}.md plus a multi-view /
  360 turntable of locked images — that keeps an object consistent across every shot.
  Use when the user says "build a prop turntable", "make an object reference sheet",
  "lock this prop", "I need this object from every angle", "hero prop reference", or
  "keep this object consistent". Produces front/back/side/top/three-quarter/detail
  views (optional 360) from one locked hero view; optionally uses 3D-assist (Blender)
  for geometry that must survive many angles or destruction.
---

DRAFT — STUB. Flesh out before promoting to skills/.

# Prop-Turntable Assistant

Lock an object into a reusable, multi-angle specification sheet that every shot
references.

## When to use
Whenever a prop must read as the same object across shots, or the user wants an object
reference sheet / turntable. Refine in place if the file exists.

## Core principle: anchor, then fan out
Generate one clean, frame-filling hero view on a neutral background with even lighting
first; derive all other views *from it*. Make the object the star — push in, keep it
dominant; pick portrait/landscape by the object's proportions and hold it across views.

## Workflow
1. **Hero view** — one clean anchor.
2. **Orthographic ring** — front · back · L/R side · top (and bottom if relevant) · ¾
   hero, derived from the anchor via reference conditioning.
3. **Detail/macro** views for signature features (engraving, seam, material).
4. **Optional 360** — 8–12 evenly-spaced angles.
5. **3D-assist (optional, recommended for hard cases):** for props that must survive
   destruction/handling/many angles or have reflective/transparent materials, lock the
   geometry in Blender (MCP) and render orthographic + depth views; skin via the image
   model. See `guide-3d-assist.md`.

## References
- [`references/guide-prop-turntable.md`](references/guide-prop-turntable.md)
- [`references/guide-asset-reference.md`](references/guide-asset-reference.md)
- [`references/guide-3d-assist.md`](references/guide-3d-assist.md)

## Reference counts
~4–6 reference images is the sweet spot; below 3 the model lacks angle/light info, above
~8 is diminishing returns. Verify per-model limits against `model-currency`.

## Output
`prop-{show}-{name}.md`: prop ID/class (hero/dressing/action), description,
dimensions/scale cue, material/finish, state variants (pristine/aged/damaged), anchor
path, model + reference-strength used, scene appearances — plus the view set in
`/assets/prop-{name}/` (assembled as a contact-sheet composite for re-use as one ref).
