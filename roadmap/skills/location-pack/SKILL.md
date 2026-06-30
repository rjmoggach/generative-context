---
name: location-pack
description: >-
  Build or refresh a location reference asset — location-{show}-{name}.md plus a set of
  locked plates — that keeps a setting consistent across shots and across time-of-day
  and weather. Use when the user says "build a location pack", "lock this environment",
  "scout this setting", "establishing plate for X", "keep this place consistent", or
  "give me this location at night / in the rain". Produces a master establishing plate,
  multi-angle coverage, and time/weather variants derived from one locked geometry;
  optionally uses 3D-assist (Blender) for reverse angles and set extension.
---

DRAFT — STUB. Flesh out before promoting to skills/.

# Location-Pack Assistant

Lock a setting into a reusable plate set that holds its geometry as the camera moves and
the light changes.

## When to use
Whenever a location must read as the same place across shots, or the user wants
establishing plates / a location pack. Refine in place if the file exists.

## Core principle: master plate, then branch
Lock one strong establishing wide in base-state light (the geometry anchor); derive
coverage angles and all time-of-day / weather variants *from it*. Change one variable at
a time; avoid abrupt time/weather jumps within a sequence.

## Workflow
1. **Master plate** — establishing wide, base light.
2. **Coverage** — reverse angle + the key shot angles the scene needs, anchored to the
   master plate so geometry/dressing stay stable. Capture beyond the on-screen frame.
3. **Variants** — day / golden / night and clear / rain / fog, *same framing*, derived
   from the locked plate via `image-edit`.
4. **3D-assist (optional, recommended for hard cases):** for reverse-angle coherence and
   **set extension**, block the space in Blender (MCP) and render plates + depth (pure 2D
   extension seams). See `guide-3d-assist.md`.
5. **Continuity table** — lens, grade, light-key direction (sun-path), time, weather,
   camera motion — restated verbatim across shots.

## References
- [`references/guide-location-pack.md`](references/guide-location-pack.md)
- [`references/guide-asset-reference.md`](references/guide-asset-reference.md)
- [`references/guide-3d-assist.md`](references/guide-3d-assist.md)
- [`references/guide-color-story.md`](references/guide-color-story.md)

## Output
`location-{show}-{name}.md`: location ID, description/era, geometry anchor path,
lens/grade vocabulary, light-key direction, time/weather states, set-extension notes
(real vs extended), scene appearances — plus plates in `/assets/location-{name}/`.
