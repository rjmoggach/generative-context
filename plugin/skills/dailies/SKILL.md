---
name: dailies
description: >-
  Review a batch of rendered shots against their specs before a human approves them —
  the dailies pass. Use after renders land — "review sbw020", "run dailies", "check the
  renders", "do these match the specs", "dailies for the sequence". For each rendered
  shot it compares the image against its identity block, screen direction and eyeline,
  palette and grade, and the attached refs, and produces a per-shot pass or flag with
  concrete notes. It is read-only: it recommends, and routes approve or needs-retake
  calls to the production-coordinator, which records the human's decision in the
  manifest. It does not render or edit — that is the render and image-edit skills.
---

# Dailies (review renders against their specs)

The near-set review pass: judge what actually rendered against what was locked, and tee
up the human's approve / needs-retake call. Runs after `render`; feeds the
`production-coordinator`. Read-only — you assess and recommend, you do not change files.

## When to use

After a batch of renders lands, before approval. Not for continuity of the *plan* (that
is `sequence-design` plus `script-supervisor`'s screen-direction audit) — dailies is
about whether each rendered frame matches its own spec.

## Step 1 — Gather the batch

For the sequence or set under review, pair each rendered file with its source of truth:
the shot line in `{show}{###}_shotlist.md` (size, lens, refs, intensity), the asset specs
its `refs:` name (`assets/{type}/{name}/{show}_{type}_{name}.md`), and the project look
(`context/{show}_project_context.md`, `context/{show}_art_bible.md`).

## Step 2 — Compare each shot

**Open the render** and check it against the spec on four axes
(`references/guide-asset-reference.md`, `references/guide-continuity-rules.md`):
- **Identity** — does each referenced asset match its identity block (face/wardrobe/HMU
  for a character; form/material for a prop; geometry for a set)?
- **Screen direction / eyeline** — does it hold the line and eyelines the shot list set,
  so it cuts with its neighbors?
- **Palette / grade** — is it on the project's hex palette and grade, not drifted?
- **Refs present** — did every locked asset the shot needed actually make it into frame?

## Step 3 — Report pass / flag

Produce a per-shot list: **pass**, or **flag** with a concrete, fixable note ("Eli's
jacket reads navy, spec is #1A2B3C oxblood"; "eyeline screen-right, should be left to
match the reverse"). Group by sequence; lead with the flags.

## Step 4 — Route the decision

The human decides. Hand the pass/flag list to the `production-coordinator`, which writes
the approve / needs-retake call into the manifest's `human` block
(`references/guide-production.md`). To *show* the renders as a board, use the
presentation surfaces (`references/guide-presentation.md`). A `needs-retake` goes back to
`render` (re-fire, new version) or `image-edit` (fix in place).

## Critical rules

1. Compare against the spec, not taste — cite the field that's off (hex, side, ref id).
2. Read-only: recommend, never approve — the human's call lands via the coordinator.
3. Don't duplicate `script-supervisor` — dailies is render-vs-spec, not plan continuity.
4. A flag names the fix path: re-render (`render`) or edit-in-place (`image-edit`).
