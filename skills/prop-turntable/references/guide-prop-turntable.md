# Prop Turntable (Object Multi-View & State Craft)

This is the **prop-turntable technical** guide — how to build a geometry-true prop
turntable from the hero anchor via `image-edit`, hold scale and alignment constant
across the orthographic ring, and extend into detail views, state variants, and
multiples. The **creative** framework — hero prop classification, multiples strategy,
and state variants as storytelling — lives in `reference-craft-artdept.md` (Props);
the **anchor-then-fan-out discipline** — the spine of all asset building — lives in
`guide-asset-reference.md` §1; the **derive engine** (denoise dial, i2i mechanisms,
state progressions) is in `guide-image-editing.md`. Do not duplicate those here —
cross-reference them.

Each entry uses the library's decision-unit format:
**Decision / Use when / Because / Prompt translation / Watch-outs / Anchors.**

---

## 1. The hero view (anchor)

- **Use when:** beginning a prop reference set — for any prop that must hold identity
  across more than one shot.
- **Because:** the hero view is the load-bearing anchor of the entire turntable. Every
  ortho view, detail crop, and state variant derives from it via `image-edit`. A weak
  anchor — angled, dramatically lit, cluttered, or low-resolution — poisons everything
  downstream: ortho views that start from an impure anchor drift in form, finish, and
  material before the rotation instruction is even applied. Get the hero right before
  fanning out. See `guide-asset-reference.md` §1 for the full treatment.
- **Prompt translation:** generate one clean, frame-filling shot of the prop — front or
  front-3/4 angle showing the main face, dominant form, and key material character — on
  a neutral background with flat, even diffuse lighting. The object should fill 70–80%
  of the frame with breathing room on all sides. No directional key light, no cast
  shadow that competes with the form, no environment. State explicitly:
  *"hero view, [prop descriptor: form / material / finish / distinguishing marks],
  neutral grey background, flat even diffuse lighting, no cast shadow, object fills
  frame."* Filename: `{show}_prop_{name}_hero.png`.
- **Watch-outs:** the single most common anchor failure is directional lighting — a key
  light bakes shadow geometry into the hero that ortho derivations cannot hold
  consistently. A hero with a strong screen-left key will produce ortho views where the
  shadow falls on inconsistent faces, making the set unreadable as a measurement
  reference. Flat diffuse is non-negotiable for the anchor and all derived views. A
  weak prop descriptor block (vague material names, no hex for distinctive finishes)
  is the second failure mode — see `guide-asset-reference.md` §2 for the two-block
  method.
- **Anchors:** `guide-asset-reference.md` §1 (anchor-then-fan-out; weak anchor poisons
  downstream); §2 (identity block for props: form / material / finish / marks).

---

## 2. The orthographic ring

- **Use when:** any prop needs multi-angle coverage — as a continuity reference, for
  downstream shot prompts, or for multi-reference composition.
- **Because:** a single hero view cannot serve as a reference for off-axis shots — the
  prop's rear face, underside, and lateral profiles are all unknown from the hero angle.
  The ortho ring fills every gap: front, back, both sides, and top give downstream work
  a geometry-true picture of the object from every angle that will appear on screen.
  Without the ring, each off-axis shot is an independent guess at what the object looks
  like from that direction; with it, every off-axis shot derives from a locked prior.
- **Prompt translation:** the standard five views, mapped to their `ortho` facet
  filenames from the asset taxonomy (see `guide-asset-reference.md` §9):

  | View | Filename | What it shows |
  |---|---|---|
  | Front | `{show}_prop_{name}_ortho_front.png` | Primary face, dominant graphic, key material surface |
  | Back | `{show}_prop_{name}_ortho_back.png` | Rear surface, back markings, hardware or finish on the reverse |
  | Left side | `{show}_prop_{name}_ortho_side_l.png` | Left-profile silhouette and depth from this axis |
  | Right side | `{show}_prop_{name}_ortho_side_r.png` | Right-profile silhouette and depth from this axis |
  | Top | `{show}_prop_{name}_ortho_top.png` | Plan view; footprint and top-face detail |

  Add `{show}_prop_{name}_ortho_bottom.png` when the underside is visible on screen (a coin
  shown tails-up, a watch worn face-down, a book lying spine-visible). Derive each view
  from the hero anchor via `image-edit` mechanism C (full-frame i2i, denoise ~0.3–0.5)
  — rotation instruction in the scene block only; hold the prop descriptor block
  verbatim in every prompt. See `guide-asset-reference.md` §1 and
  `guide-image-editing.md` §3-C / §4. Keep alignment constant: consistent scale (object
  occupies the same frame proportion in every view), consistent background (same
  neutral), consistent lighting (same flat diffuse throughout).
- **Watch-outs:**
  - Do not raise denoise above ~0.5 for ortho views — material and finish drift climbs
    sharply above that threshold. If the rotation did not take at ~0.4, sharpen the
    rotation instruction before raising denoise.
  - Always derive from the **hero anchor** — not from a previously derived ortho view.
    Chaining edits (hero → front → back) compounds form drift at each step.
  - Do not skip the back view. Rear surfaces and back hardware are the most common
    continuity gap in downstream shots.
- **Anchors:** `guide-asset-reference.md` §1 (anchor-then-fan-out); `guide-image-editing.md`
  §3-C and §4 (mechanism C; denoise dial).

---

## 3. Detail / macro views

- **Use when:** the prop has surface elements the hero and ortho views cannot show at
  usable resolution — engravings, hallmarks, mechanism components, wear patterns,
  inlays, inscriptions, labels, weave or texture.
- **Because:** hero props appear in close-up, and the camera will resolve surface detail
  that the full-frame ortho view cannot carry. Without dedicated detail references,
  close-up generation invents the micro-detail rather than reconstructing it — and
  invented detail drifts from shot to shot. A locked detail reference gives the model a
  fixed, inspectable surface to reconstruct from each time the prop enters close-up.
  See `guide-asset-reference.md` §6 on why micro-detail cannot be relied upon across
  the wider-angle reference set.
- **Prompt translation:** crop or inpaint the region of interest from the hero (or from
  a derived ortho view if the detail is on a non-hero face) via `image-edit` mechanism
  B (masked or cropped region) at low denoise (~0.2–0.3), preserving all surface
  characteristics. Name the surface explicitly:
  *"close-up of [engraving / hallmark / mechanism / wear patch], same material finish
  and surface character as source, no change to the object."* Number sequentially:
  `{show}_prop_{name}_detail_01.png`, `{show}_prop_{name}_detail_02.png`. Note which face each
  detail originates from in the companion spec file (`{show}_prop_{name}.md`).
- **Watch-outs:** hold the flat diffuse discipline in detail views — a detail lit
  differently from the hero creates integration problems when close-up shots must cut
  to wider frames. Micro-detail (fine text, insignia, hallmark stamps) is the first
  element i2i models drop under compression; verify each detail view against the hero
  after generation and re-derive at lower denoise if the element is lost.
- **Anchors:** `guide-asset-reference.md` §6 (don't depend on micro-detail for
  identity across wide-angle references); `guide-image-editing.md` §3-B (masked
  inpaint) and §4 (denoise dial).

---

## 4. State variants and multiples

- **Use when:** the prop changes condition across the story (pristine → worn → damaged
  → destroyed) or requires duplicate units for stunt work, continuity matching, or
  simultaneous shooting.
- **Because:** a prop's condition is itself a form of storytelling — and that
  progression must be locked and reproducible across a shooting schedule that may span
  weeks. Generating each state independently re-rolls material fingerprint, surface
  character, and form from shot to shot; editing from the prior state preserves the
  fingerprint and keeps the progression continuous. Multiples — the family of
  near-identical duplicate units a hero prop requires for coverage — must match each
  other within the same state; the state suffix makes the relationship explicit and
  traceable. See `reference-craft-artdept.md` (Props: "State variants as narrative"
  and "Multiples and the math of destruction") for the creative and production rationale.
- **Prompt translation:**
  - **State progression:** derive each new state from the previous one via `image-edit`
    mechanism A or B at low denoise (~0.2–0.3). Add the condition change in the edit
    instruction; hold the prop descriptor block verbatim. Never regenerate from scratch
    to reach a further state — always edit the immediately preceding state.
  - **State suffix convention:** append the state name to the base filename:
    `{show}_prop_{name}_hero_aged.png`, `{show}_prop_{name}_hero_bloodied.png`,
    `{show}_prop_{name}_hero_broken.png`. Ortho and detail views at the same state follow the
    same pattern: `{show}_prop_{name}_ortho_front_aged.png`,
    `{show}_prop_{name}_detail_01_bloodied.png`.
  - **Multiples:** generate the primary unit first; derive duplicate units from it at
    very low denoise (~0.1–0.2) with only minor permitted surface variation. Record the
    multiple count in the prop spec file.
- **Watch-outs:** progress by editing from the prior state, never by regenerating from
  zero — see `guide-asset-reference.md` §7 and `guide-image-editing.md` §6. Lock each
  recurrent state as its own reference if it appears across multiple shots. The state
  suffix is a narrative read signal, not a filing suffix — name it accurately
  (`-worn` ≠ `-aged` ≠ `-distressed`).
- **Anchors:** `guide-asset-reference.md` §7 (edit, don't regenerate, for
  progressions); `guide-image-editing.md` §6 (wound/blood/dirt progression); §8
  (iterate from the chosen result, not from scratch); `reference-craft-artdept.md`
  (Props: state variants and multiples).

---

## 5. Optional 360 turntable

- **Use when:** the prop must be resolved at arbitrary angles not covered by the ortho
  ring — circular reveal shots, continuous rotation sequences, or reference sets for a
  3D pipeline.
- **Because:** the five-view ortho ring covers the canonical camera positions but leaves
  gaps between them. An 8–12 step 360 fills those gaps with interpolated positions,
  giving the model a continuous geometry read around the full circumference. This is
  warranted only when the shot list or pipeline explicitly requires it — for most props,
  the ortho ring is sufficient.
- **Prompt translation:** generate 8–12 evenly spaced views at 30°–45° intervals
  (8 steps = 45°; 12 steps = 30°) from the hero anchor via `image-edit` mechanism C.
  All framing-the-asset rules apply (§6): consistent scale, neutral background, flat
  diffuse. File as `{show}_prop_{name}_360_01.png` through `{show}_prop_{name}_360_08.png` (or
  `-12.png`). Record the step count and starting angle in the prop spec file.
- **Watch-outs:** diminishing returns set in quickly. Beyond ~12 steps, generation
  drift across the set compounds and frames stop reading as a single coherent object.
  The 360 facet is warranted only when the shot list or 3D pipeline explicitly requires
  it. When consuming a 360 set as references, the same effective-reference-count logic
  applies — see `guide-asset-reference.md` §4.
- **Anchors:** `guide-asset-reference.md` §4 (effective reference counts; the same
  ceiling applies to 360-set consumption in downstream prompts).

---

## 6. Framing-the-asset rules

- **Use when:** generating or reviewing any image in the prop reference set — hero,
  ortho, detail, state variant, or 360.
- **Because:** a reference set is only as consistent as its most inconsistent frame.
  Scale mismatch between views makes proportions unreadable across the set; varied
  backgrounds compete with edge definition; directional lighting bakes inconsistent
  shadow geometry into different views; focal-length variation introduces perspective
  distortion that reads as a form change. These failures are systematic — they compound
  across every derived view — so they must be established at the hero anchor and held
  without exception.
- **Prompt translation:** four non-negotiable requirements, stated explicitly in every
  view prompt:
  1. **Fill the frame** — the object occupies 70–80% of the frame with breathing room
     on all sides. State: *"object fills frame, slight margin on all sides."*
  2. **Neutral background** — low-contrast neutral grey or white; no environment, no
     texture, no cast shadow extending into the background. State: *"plain neutral grey
     background, no environment."*
  3. **Even, flat diffuse lighting** — no directional key light, no asymmetric specular
     hot-spots (unless the material is genuinely specular and the highlight falls
     symmetrically with the object's axis). State: *"flat even diffuse lighting, no
     cast shadows."*
  4. **Consistent lens character** — use an equivalent of 50–85mm focal length
     (moderate telephoto) for all views; avoid wide-angle distortion that deforms the
     object's proportions. Do not vary this between views. State: *"neutral lens,
     no distortion, consistent with prior views."*
- **Watch-outs:** background tone sets edge definition for every downstream matte or
  composite — pure white risks haloing on light objects; very dark grey risks edge-fill
  on dark objects. A low-contrast mid-grey (#808080 range) is the safe default. If the
  production uses a specific matte-key color in post, match it across the entire set.
- **Anchors:** product and studio photography convention (consistent axis, lens, and
  background for multi-view reference sets); `guide-turnaround-sheets.md` §2 (alignment
  discipline — the same principle applied to character views).

---

**3D-assist forward pointer:** for props that must survive arbitrary angles, destruction sequences, or LoRA training at production scale, a 3D geometry-lock and depth-pass approach is a known technique — deferred to a later phase.

---

## Quick application

1. Generate the **hero anchor** (`{show}_prop_{name}_hero.png`) — frame-filling, flat diffuse,
   neutral background; apply §6 framing rules.
2. Derive the **orthographic ring** from the hero anchor via `image-edit` (mechanism C,
   denoise ~0.3–0.5) — never from each other:
   `{show}_prop_{name}_ortho_front.png` / `-back` / `-side_l` / `-side_r` / `-top`
   (add `-bottom` when the underside is on screen).
3. Add **detail views** for any surface element the camera will resolve in close-up:
   `{show}_prop_{name}_detail_01.png`, `{show}_prop_{name}_detail_02.png`.
4. Build **state variants** by editing from the prior state at low denoise (~0.2–0.3) —
   never regenerate from scratch. Apply state suffix across all affected filenames:
   `{show}_prop_{name}_hero_aged.png`, `{show}_prop_{name}_ortho_front_aged.png`.
5. Add a **360 turntable** (`{show}_prop_{name}_360_01.png` through `-08.png` or `-12.png`)
   only when the shot list or 3D pipeline explicitly requires it.
6. Hold **framing-the-asset rules** (§6) across every image in the set: fill the frame,
   neutral background, flat diffuse, consistent lens.

**Companion guides:** `guide-asset-reference.md` (anchor-then-fan-out §1; reference
counts §4; asset taxonomy §9) · `reference-craft-artdept.md` (Props: hero
classification, multiples, state variants) · `guide-image-editing.md` (i2i mechanisms
§3; denoise dial §4).
