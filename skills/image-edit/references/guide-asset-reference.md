# Asset Reference (Building Reusable Visual Anchors)

Decision rules for **building and using persistent reference assets** — a locked
character, prop, or location that holds consistent across many shots. This is the
spine of the art department: it turns the principle in
`guide-ai-generation-strategy.md` ("reference images beat text bibles") into a
repeatable method for *making* those references and *composing* them into new shots.
Used by the asset skills (`character-sheet`, `prop-turntable`, `location-pack`), by
`image-edit` (the engine that derives views/states), and by `shot-prompt` (which
attaches the finished references). Pair with `guide-image-editing.md`.

Each entry uses the library's decision-unit format:
**Decision / Use when / Because / Prompt translation / Watch-outs / Anchors.**

---

## 1. Anchor, then fan out

- **Use when:** building any reusable asset (character, prop, location).
- **Because:** generating each view/state independently produces siblings, not the
  same subject. A single clean **anchor** gives every later view a fixed thing to
  reconstruct from.
- **Prompt translation:** generate one clean, frame-filling anchor on a neutral
  background with even lighting *first* (front portrait for a character; hero view for
  a prop; master establishing plate for a location). Then derive all other
  views/states *from it* via the model's reference feature and `image-edit`.
- **Watch-outs:** a weak anchor (angled, expressive, low-res, cluttered) poisons
  everything downstream — get it right before fanning out.
- **Anchors:** VFX asset pipeline ("lock the asset early; every department uses the
  same dataset").

## 2. Two-block prompting: identity vs change

- **Use when:** every prompt that uses an asset.
- **Because:** scene complexity bleeds into identity unless they're kept separate.
- **Prompt translation:** split every prompt into a constant **identity block**
  (50–80 words: face, hair, body, locked wardrobe, accessories, HMU state, marks —
  for a prop: form, material, finish, marks; for a location: geometry, key features,
  light logic) reused **verbatim**, plus a variable **scene block** (location, camera,
  light, action). Identity lives in the reference; change lives in the prompt.
- **Watch-outs:** vague language is the #1 drift source — pin **hex colors**, garment
  names, silhouette, wound position+side+size, material names.
- **Anchors:** continuity script (the same descriptor every shot).

## 3. Reference for speed, LoRA for scale

- **Use when:** deciding how hard to lock a given subject.
- **Because:** reference images are fast but cap out around perceptual consistency; a
  trained LoRA reaches near-identity but costs setup and images.
- **Prompt translation — the decision gate:**
  - **≤ ~1 scene / quick turnaround → reference image only** (~65–75% consistency).
  - **Recurring hero across many shots/episodes → reference + trained LoRA + fixed
    descriptor block** (~85–92%); record the LoRA trigger word in the asset file.
  - **Background / one-off → reference only.**
- **Watch-outs:** don't train a LoRA for a subject that appears once; don't rely on a
  bare reference for a lead who carries the show.
- **Anchors:** cost-aware production (match the lock to the subject's screen life).

## 4. Effective reference counts

- **Use when:** feeding multiple references for one asset.
- **Because:** too few starves the model of angle/light info; too many gives
  diminishing returns and muddies identity.
- **Prompt translation:** ~**4–6** reference images is the sweet spot; reference
  strength ~**0.7** (workable 0.6–0.8). Below 3, the model lacks angle/lighting
  coverage; above ~8, returns diminish.
- **Watch-outs:** these numbers are **version-sensitive** — current per-model limits
  (e.g. how many objects/characters a model holds, max references) live in the model
  docs and `model-currency`. Verify before hard-coding; flag the `researcher` /
  `model-docs` loop to keep them current.
- **Anchors:** model docs are the source of truth for counts.

## 5. Multi-reference composition

- **Use when:** placing a locked subject into a new location wearing a locked
  costume/prop — the core art-department shot.
- **Because:** each reference can carry one locked element; the prompt directs how
  they combine.
- **Prompt translation:** assign every reference an explicit **role** — "Image 1 =
  this exact person, keep face and features; Image 2 = the background/location; Image 3
  = the costume/prop" — and map characters spatially for multi-subject scenes
  ("Character A on the left, B center"). Keep the identity block verbatim even though a
  reference carries the face. When the model won't honor staging from text, fall back
  to **composite-then-blend**: assemble the elements, then a low-denoise (~0.1–0.2)
  pass to unify light.
- **Watch-outs:** mismatched light across the source references reads as pasted-in —
  prefer references shot/generated under compatible light, or relight in the blend pass.
- **Anchors:** background-plate compositing; reference-image lock.

## 6. Hold the light; don't depend on micro-detail

- **Hold one dominant light-key direction per scene** — the cheapest, most-overlooked
  identity lever; flipping the key flips identity.
- **Don't depend on micro-detail** (freckles, logos, insignia, tiny patterns) for
  identity — models drop these first. Keep them simple, carry them in a dedicated
  detail reference, or composite them in.

## 7. Edit, don't regenerate, for progressions

For any state that evolves (wound stages, aging, wear, weather on a location), **edit
from the previous state** at low denoise rather than regenerating from scratch — it
preserves the fingerprint and keeps the progression continuous. See
`guide-image-editing.md` §4, §6.

## 8. Inherit top-down

Assets are not islands. The world bible (`art-bible-{show}.md`) sets the global style,
palette, material lexicon, and grade; every character/prop/location asset **inherits**
it so the world coheres. Construct asset prompts *from* the bible's fields, not loosely
inspired by them. See `guide-art-direction.md`.

---

## Quick application

1. Build the **anchor** first (front portrait / hero view / master plate) — clean,
   neutral, evenly lit, high-res.
2. **Fan out** views and states from it with the asset skill + `image-edit`.
3. Write the **identity block** (verbatim, hex-pinned) and store it with the asset.
4. Set the **reference-vs-LoRA** lock to the subject's screen life.
5. **Compose** into shots by reference role; keep identity constant, scene variable.
6. Hold the **light-key**; edit (don't regenerate) for progressions.
