# Location Pack (Environment Master Plate & Coverage Craft)

This is the **location/set pack technical** guide — how to build a coverage-complete
environment reference set from a locked master plate via `image-edit`, hold geometry
and light logic constant across coverage angles and time-of-day variants, and manage
the hard cases of reverse angles and set extension. The **creative** framework — the
scouting packet, reverse-angle coherence, and set extension as production discipline —
lives in `reference-craft-artdept.md` (Locations & Sets); the **anchor-then-fan-out
discipline** — the spine of all asset building — lives in `guide-asset-reference.md`
§1; the **derive engine** (denoise dial, i2i mechanisms, relight progressions) is in
`guide-image-editing.md`. Do not duplicate those here — cross-reference them.

Each entry uses the library's decision-unit format:
**Decision / Use when / Because / Prompt translation / Watch-outs / Anchors.**

---

## 1. The master establishing plate (anchor)

- **Use when:** beginning a location/set pack — for any environment that must hold
  spatial identity across more than one shot.
- **Because:** the master plate is the load-bearing anchor of the entire pack. Every
  coverage angle and every time-of-day variant derives from it. The plate fixes three
  things simultaneously: the geometry of the space (spatial relationships, scale,
  architectural or landscape features that identify this location), the light logic
  (key direction, quality, colour temperature for the canonical production condition),
  and the persistent key features that every subsequent view must preserve — a doorway,
  a horizon line, a distinctive wall plane, a tree-line silhouette. A weak plate —
  framed too tight to read the geometry, lit in a condition that contradicts the logic
  of the space, or backed by a vague written identity block — poisons everything
  downstream. Get the plate right before fanning out. See `guide-asset-reference.md`
  §1 for the full treatment.
- **Prompt translation:** generate one wide establishing shot of the location — wide
  enough to read the full spatial relationships, dominant architecture or landscape
  features visible and legible, environment filling the frame with breathing room at
  the edges. Choose the production's canonical light condition for this anchor (the
  time of day and atmosphere the location will most often be seen in on screen). State
  explicitly: *"wide establishing shot, [environment descriptor: architecture /
  landscape / spatial geometry / key features], [canonical lighting condition: time of
  day, key direction, colour temperature], no characters, no props in frame."*
  Filename: `set-{name}-plate.png`. Store the identity block — geometry, key features,
  light logic — in the companion spec file (`set-{show}-{name}.md`); image files drop
  `{show}`.
- **Watch-outs:** the most common plate failure is a frame too tight to fix the
  geometry — an interesting close detail establishes atmosphere but not space, leaving
  coverage derivations with no spatial anchor to reconstruct from. The second failure
  is a plate shot in a dramatically lit condition (hard golden side-light, deep-night
  ambience) that forecloses tod variants: a plate already at a lighting extreme has
  nowhere to derive toward in that direction. Choose the canonical mid-range condition
  and let tod variants reach the extremes. The third failure is an insufficient written
  identity block — a plate backed by a vague descriptor cannot be reconstructed
  consistently in downstream prompts; pin the geometry the same way material finish
  is pinned for props (see `guide-asset-reference.md` §2).
- **Anchors:** `guide-asset-reference.md` §1 (anchor-then-fan-out; weak anchor poisons
  downstream); §2 (identity block for environments: geometry, key features, light
  logic).

---

## 2. Coverage angles

- **Use when:** any location needs multi-angle coverage — for continuity reference,
  downstream shot prompts, or multi-reference composition.
- **Because:** a single master plate cannot serve as a reference for off-axis shots —
  the reverse of a street, the view from the window seen in the establishing plate, the
  close view of a key threshold are all unknowns from the master angle. Coverage angles
  fill those gaps: each `cov` view adds a locked prior for a camera position the shot
  list will actually use. Without them, each off-axis shot is an independent guess at
  what this space looks like from that direction; with them, every derived shot
  reconstructs from a fixed geometry anchor. The **reverse angle** is the most critical
  coverage view — and the most commonly omitted. Its treatment as a hard case lives in
  §5; assign it a slot in the `cov` sequence here and lock it before proceeding.
- **Prompt translation:** derive each coverage angle from the master plate via
  `image-edit` mechanism C (full-frame i2i, denoise ~0.3–0.5) — camera direction and
  framing in the scene block; hold the geometry descriptor block and the canonical
  light condition verbatim. Number sequentially, with the reverse assigned its slot in
  the sequence:

  | View | Filename | What it shows |
  |---|---|---|
  | Master (= the plate) | `set-{name}-plate.png` | Wide establishing; full spatial geometry at canonical condition |
  | Coverage 01 | `set-{name}-cov-01.png` | First coverage angle per the shot list |
  | Coverage 02 | `set-{name}-cov-02.png` | Second coverage angle |
  | Reverse | `set-{name}-cov-reverse.png` | Looking back through the space; camera opposite the master plate |
  | Additional | `set-{name}-cov-03.png` | Any further angles required by the shot list |

  State the camera direction explicitly in each prompt: *"camera positioned [spatial
  description], looking [into / across / back through] the space; same geometry, same
  [canonical light condition]; no characters."* See `guide-asset-reference.md` §1 and
  `guide-image-editing.md` §3-C / §4.
- **Watch-outs:**
  - Do not skip the reverse. A pack without a locked reverse forces the reverse to be
    generated independently inside the shot prompt — an independent generation with no
    geometry anchor, which will drift from the plate.
  - Do not raise denoise above ~0.5 for coverage derivations — spatial drift climbs
    sharply above that threshold. Sharpen the camera direction instruction before
    raising denoise.
  - Always derive from the **master plate** — not from a previously derived coverage
    angle. Chaining edits (plate → cov-01 → cov-02) compounds spatial drift at each
    step.
- **Anchors:** `guide-asset-reference.md` §1 (anchor-then-fan-out); `guide-image-editing.md`
  §3-C and §4 (mechanism C; denoise dial).

---

## 3. Time-of-day and weather variants

- **Use when:** the location appears under more than one lighting or atmospheric
  condition across the story.
- **Because:** a location's identity is partly geometric (fixed) and partly atmospheric
  (variable). Generating each lighting condition independently re-rolls the geometry —
  windows shift, the horizon line moves, spatial relationships change — so each
  independently generated tod image is a sibling location, not the same place. Deriving
  tod variants from the locked master geometry preserves the spatial fingerprint and
  changes only what the light and atmosphere change: colour temperature, shadow
  direction and length, sky quality, and ambient moisture. The discipline is one
  variable at a time — do not simultaneously shift the time of day AND the weather in
  a single derive step; two-variable changes compound drift and make the variant
  unrecoverable as a geometry anchor.
- **Prompt translation:** derive each tod variant from the master plate via `image-edit`
  mechanism C at low-to-moderate denoise (~0.3–0.5 for dawn/dusk/rain; allow ~0.5–0.6
  for night). Relight instruction in the scene block only; hold the geometry descriptor
  block verbatim. Standard tod set:

  | Variant | Filename | What changes |
  |---|---|---|
  | Dawn | `set-{name}-tod-dawn.png` | Low warm-orange key, long horizontal shadows, sky graduating dark to pale |
  | Dusk | `set-{name}-tod-dusk.png` | Low warm-red key, shadows stretching opposite dawn, late-colour sky |
  | Night | `set-{name}-tod-night.png` | Ambient or practical-source key (streetlights, windows), deep shadow, reduced ambient |
  | Rain | `set-{name}-tod-rain.png` | Overcast diffuse key, wet surfaces, atmospheric haze; derive from the canonical plate |

  Always branch from the master plate — not in series. Do not chain dawn → day →
  dusk → night; each tod variant derives independently from the anchor. The canonical
  plate is the day reference if day is the production condition; it does not need a
  separate named tod image for day.
- **Watch-outs:** night is the highest-risk tod variant — full-frame relighting requires
  higher denoise (~0.5–0.6), which puts geometry at drift risk. List the key landmarks
  explicitly in the night prompt; accept some ambient detail loss; what must survive is
  the spatial skeleton. Rain changes surface properties (wet reflections, overcast sky,
  haze) but must not change geometry; derive rain from the canonical plate, not from a
  partially-lit tod variant already in progress. One variable per derive step: a
  rain-at-night variant requires two steps — anchor → rain (day-locked, wet surfaces) →
  night from that rain base.
- **Anchors:** `guide-asset-reference.md` §7 (edit, don't regenerate, for progressions);
  `guide-image-editing.md` §3-C and §4 (mechanism C; denoise dial); §5 (lighting
  integration; key direction and atmosphere matching).

---

## 4. The continuity table

- **Use when:** the pack has more than two variants — coverage angles or tod conditions —
  that must cut together in the edit.
- **Because:** a location pack is only as consistent as its worst-recorded variant.
  Without a written record, light direction drifts between shots (screen-left key in
  the plate, screen-right in cov-02), colour temperature is inconsistent between tod
  variants, and shadow logic contradicts the time of day stated in the script. These
  are the same continuity problems a script supervisor photographs against — the
  continuity table is the written equivalent for the generated reference set. What is
  recorded here is what gets restated verbatim in every downstream shot prompt that
  uses this location.
- **Prompt translation:** maintain one continuity table per location pack, stored in the
  spec file (`set-{show}-{name}.md`). Minimum fields per variant:

  | Variant | Key direction | Key colour / temp | Sky / atmosphere | Notes for downstream prompts |
  |---|---|---|---|---|
  | `plate` | Screen-left, 3/4 front | Warm white, ~5600K | Clear, light cloud | State explicitly in every shot prompt |
  | `cov-01` | Match plate | Match plate | Same sky condition | Looking back toward plate camera position |
  | `tod-dawn` | Low, screen-right | Orange, ~2800K | Pale sky, ground mist | Shadow length: long horizontal |
  | `tod-night` | Practical (streetlight / window) | Amber / cool moonlight | Dark, minimal cloud | Deep shadow zones: list landmark areas |
  | `tod-rain` | Diffuse, no direction | Flat grey-white, ~7000K | Heavy overcast, haze | Wet surfaces: list which are in frame |

  The Notes column records what must be stated explicitly in downstream shot prompts —
  the guardrail that prevents per-shot light drift. See `guide-asset-reference.md` §6
  (hold the light-key direction per scene) and §2 (restate the identity block verbatim
  per shot).
- **Watch-outs:** a continuity entry that says only "similar to plate" is not useful —
  name the specific key direction, temperature, and atmosphere in each cell. Imprecise
  entries produce imprecise prompts, which produce shots that fail to cut together. If
  a tod variant required a specific denoise value or was produced from a specific
  intermediate step, record that too — it is the fastest path back to a matching result
  if a re-derive is needed later.
- **Anchors:** `guide-asset-reference.md` §2 (identity block; verbatim reuse per shot)
  and §6 (hold the light-key direction).

---

## 5. Reverse-angle and set-extension coherence

- **Use when:** the shot list calls for the reverse angle of the master plate, or for
  views that extend beyond what the plate frame shows.
- **Because:** the reverse angle and set extension are the two cases where the plate
  anchor cannot be directly derived — the camera is pointing in the opposite direction
  from the plate, or is positioned in a zone the plate does not show. Without
  discipline, the reverse becomes a different location and the extension becomes an
  invented attachment with no spatial relationship to the anchor. The production
  rationale is in `reference-craft-artdept.md` (Locations & Sets: "a location approved
  on the basis of a single hero angle that ignores the reverse is a mistake"). The
  technical answer is: enumerate the landmarks that must persist through the direction
  change, derive the reverse from those, and lock the result as its own anchor that
  all further reverse-angle shots derive from.
- **Prompt translation:**
  - **Reverse angle:** identify the persistent landmarks visible from both directions —
    features that span the full depth of the space (a floor pattern, a distinctive wall
    plane, a ceiling, a tree-line that reads from both ends, a practical light source).
    List these explicitly in the reverse prompt as geometry guardrails: *"reverse angle
    looking back through the space; preserving [landmark A, landmark B, landmark C];
    same [canonical light condition]; no characters."* Lock the result as the next `cov`
    slot in the sequence. Treat it as its own anchor — all further shots from the
    reverse direction derive from this locked `cov` view, not from the master plate.
  - **Set extension:** when the shot requires seeing beyond what the plate frame shows —
    above, to the side, or behind the primary camera position — derive the extension as
    an additional `cov` view from the master plate via mechanism C, stating the spatial
    continuation explicitly: *"continuing the space [above / to the left / behind
    camera]; geometry consistent with [key features of the plate]; same [canonical
    light condition]."*
- **Watch-outs:** the reverse angle is most likely to expose what was not designed —
  the missing wall, the undressed background zone, the light source implied by the
  plate's key direction that cannot plausibly exist from the opposite angle. In
  generated reference sets, the answer is to be explicit about what the reverse MUST
  show before generating it. Inventory mismatches — a doorway on the wrong wall, a
  shadow falling in the wrong direction — are the most common coherence failure; catch
  them by comparing key features explicitly across plate and reverse before committing
  either to the pack. When a mismatch is found, correct the reverse, not the plate:
  the plate is the fixed anchor.
- **Anchors:** `guide-asset-reference.md` §1 (anchor-then-fan-out; the reverse derives
  from a locked prior, not from scratch); `reference-craft-artdept.md` (Locations &
  Sets: reverse-angle coherence and set extension); `guide-image-editing.md` §3-C
  (mechanism C for derived views).

---

**3D-assist forward pointer:** blocking the location in 3D for geometry-locked reverse
angles and set extensions is a known technique — deferred to a later phase.

---

## Quick application

1. Generate the **master establishing plate** (`set-{name}-plate.png`) — wide enough to
   fix the geometry, in the production's canonical light condition. Store the identity
   block (geometry, key features, light logic) in the companion spec file
   (`set-{show}-{name}.md`).
2. Derive **coverage angles** from the master plate via `image-edit` (mechanism C,
   denoise ~0.3–0.5) — never from each other. Always include the reverse angle, locked
   as the next slot in sequence: `set-{name}-cov-01.png`, `set-{name}-cov-02.png`, …
3. Derive **tod variants** from the master plate one variable at a time — branch each
   from the anchor independently, never chain in series: `set-{name}-tod-dawn.png`,
   `set-{name}-tod-dusk.png`, `set-{name}-tod-night.png`, `set-{name}-tod-rain.png`.
4. Record the **continuity table** in the spec file — light direction, key colour, and
   atmosphere per variant. Restate these values verbatim in every downstream shot
   prompt that uses this location.
5. Handle **reverse angles and set extensions** by enumerating the persistent landmarks
   first, deriving the reverse as its own locked `cov` view, and locking all further
   reverse-direction shots to that derived anchor rather than to the master plate.

**Companion guides:** `guide-asset-reference.md` (anchor-then-fan-out §1; identity
block §2; light-key §6; asset taxonomy §9) · `reference-craft-artdept.md` (Locations
& Sets: creative and scouting rationale) · `guide-image-editing.md` (i2i mechanisms
§3; denoise dial §4; lighting integration §5).
