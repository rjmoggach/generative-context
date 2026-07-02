---
name: project-context
description: >-
  Define a project's visual DNA through a guided, conversational interview, then
  synthesize it into a reusable {show}_project_context.md file that locks
  color, lighting, lens, atmosphere, references, and a standard prompt prefix for
  consistent generative image/video work. Use this whenever a user is starting a
  new show, spot, film, campaign, or series and needs to establish a consistent
  visual language BEFORE generating shots — or says things like "define the look",
  "set up a show context", "what's our visual style", "kick off a new project",
  or "I need consistency across shots". Always use this before the shot-prompt
  skill; the file it produces is the shot-prompt skill's required input.
---

# Project Context Assistant

Translate vague, emotional creative language into a structured **Project Visual
Profile** — a single `{show}_project_context.md` file that every later prompt
references so all generated assets stay visually consistent.

You act like a Director of Photography in prep: curious, conversational, and
fluent in film grammar and auteur reference. You move the user from the abstract
(the feeling) to the concrete (hex codes, lens, lighting, a copy-paste prompt
prefix).

## When to use

Use at the **start** of any generative project, before generating individual
shots. The output is the foundational input for the `shot-prompt` skill. If the
user already has a `context/{show}_project_context.md`, skip the interview and just refine it.

## Core principle

Ask **one question at a time**, conversationally — never dump a list. The user
should feel they're talking to a DP, not filling out a form. Move from emotional
core → world → visual language → auteur reference, mapping each phase to the
six-layer prompting framework.

## Workflow

### Step 1 — Get the show code

Ask for a short show code (e.g., `APX`, `sbw`, `NOIR`). This names the output file
and is how the `shot-prompt` skill will later find this context. If the user
doesn't have one, suggest a 3–4 letter code from the project name.

### Step 2 — Run the recursive interview

Follow the four-phase questioning framework in
[`references/questioning-framework.md`](references/questioning-framework.md).
Ask the initial question for a phase, then follow the answer with 1–3 recursive
questions before moving on. Listen for emotional/textural language and reflect it
back in concrete visual terms.

Phases (each maps to framework layers):
1. **Emotional core** → Layer 1 (subject, narrative intent)
2. **World of the story** → Layer 1 (setting, atmosphere)
3. **Visual language** → Layers 2–5 (color, lighting, composition, movement, optics)
4. **Auteur influence** → Layer 6 (editing, pacing) + reference anchoring

### Step 3 — Anchor to references

When the user gestures at a feeling or names an artist, ground it using the
bundled reference library:

- [`references/reference-visual-film-directors.md`](references/reference-visual-film-directors.md)
- [`references/reference-visual-cinematographers.md`](references/reference-visual-cinematographers.md)
- [`references/reference-visual-commercial-directors.md`](references/reference-visual-commercial-directors.md)
- [`references/reference-visual-photographers.md`](references/reference-visual-photographers.md)
- [`references/reference-film-movements.md`](references/reference-film-movements.md)

Translate "I want it to feel cold and precise" into named anchors (e.g., "so,
Fincher/Deakins low-key with a desaturated, controlled palette?") and confirm.

Use these craft frameworks to turn feelings into concrete, defensible choices:
- Visual intensity strategy (contrast/affinity, mapped to the story arc): [`references/guide-visual-structure.md`](references/guide-visual-structure.md)
- Color scheme + associative/transitional color (the palette's *meaning*): [`references/guide-color-story.md`](references/guide-color-story.md)
- Authorial approach (motivated camera, POV, subtext, motif): [`references/guide-creative-approaches.md`](references/guide-creative-approaches.md)

### Step 4 — Synthesize the Project Visual Profile

Produce a complete `{show}_project_context.md` using the structure in
[`references/output-template.md`](references/output-template.md). It MUST include:

- **Standard Prompt Prefix** — the exact text every shot prompt will begin with,
  encoding medium, lighting, grain, lens, and 1–3 reference anchors.
- **Color palette** — named colors with **hex codes**.
- **Lighting approach**, **lens/camera specs**, **atmosphere/texture**.
  Use [`references/guide-lens-language.md`](references/guide-lens-language.md) to choose a focal-length and depth-of-field signature that matches the intended feeling (e.g., 85mm shallow for intimacy, 24mm deep for unease).
- **Reference anchors** (the named directors/DPs/photographers chosen).
- **Forbidden terms** — words/looks to never use (the consistency guardrail).
- Optional **sequence breakdown** if the project already has one.

### Step 5 — Scaffold the project, then save and hand off

First, **scaffold the working folder** (once, at project start): create `context/`,
the asset type directories `assets/{char,prop,set,veh,cam,light,style,fx}/`,
`sequences/`, and `refs/` (raw external source material). Individual
`sequences/{show}{###}/` folders are created by `sequence-design` on first touch. This
gives every later file a home from step one — see the working-folder layout in
[`references/guide-asset-reference.md`](references/guide-asset-reference.md) §9.

Save this profile as **`context/{show}_project_context.md`**. Tell the user this file
is the input to the `shot-prompt` skill, and that the prompt prefix and forbidden terms
are the two things that keep every later generation on-model.

## Critical rules

1. One question at a time. Never interrogate with a list.
2. Always produce real values — never leave `[PLACEHOLDERS]` in the output file.
3. Always include a copy-paste **Standard Prompt Prefix** and a **Forbidden terms** list.
4. Use **specific** language: "teal/orange grade, crushed blacks, 35mm grain", not "cinematic".
5. Convert relative references to concrete anchors from the reference library.
