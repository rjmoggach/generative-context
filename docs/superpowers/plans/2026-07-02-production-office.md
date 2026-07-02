# Production Office — Coordinator + Manifest (v1.0-b) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship v0.11.0 - the production office: a `production` skill + `production-coordinator` agent that build/reconcile a `production-{show}.json` manifest (a derived index of assets/generations/cost from the working folder, plus persisted human status) and report production status.

**Architecture:** `context/` is the source of truth; `skills/build.py` bundles context into each skill's `references/`; `plugin/assemble.py` regenerates `plugin/context/` + `plugin/skills/` and validates. No unit tests - the gate is `python plugin/assemble.py` printing `VALIDATE: OK` + `python skills/build.py` clean. The manifest and coordinator are DOCUMENTATION the agent follows (scan the user's working folder, write `production-{show}.json` there) - no code ships in the plugin. Mirrors the art-direction pipeline (skill + agent + guide).

**Tech Stack:** Markdown (library + skill + agent), Python 3 stdlib build scripts, a JSON manifest the agent writes to the user's working folder. Spec: `docs/superpowers/specs/2026-07-02-production-office-design.md`.

## Global Constraints

- **Target version:** `0.11.0` - verbatim in `plugin/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` (both `metadata.version` and plugin-entry `version`), README banners.
- **Manifest model:** `production-{show}.json` is a DERIVED index the coordinator rebuilds from ground truth (asset specs + `.recipe` sidecars) PLUS a persisted `human` block (approved/needs-retake/notes) that a rebuild MUST merge-preserve by artifact id. Files are the source of truth; the manifest is the index; it can always be rebuilt (anti-rot).
- **Format:** JSON canonical, written to the USER'S WORKING FOLDER (never the plugin repo). Human-readable dashboard is deferred to v1.0-c; the coordinator reports in chat.
- **Pattern:** skill + agent + guide (like art-direction). No template file - the manifest schema lives in `guide-production.md`.
- **Agent frontmatter (strict YAML, required keys):** `name`, `description`, `model`, `color`, `tools`. `model: inherit`, `tools: ["Read", "Grep", "Glob"]`, `color: green`. No raw `<...>` tags in frontmatter.
- **House style:** `guide-*.md` decision-unit format, em-dashes, straight quotes, no emojis, technical terms in `code`. No `[PLACEHOLDER]` in shipped files. Project name stays `generative-wrangler`.
- **Commits:** OMIT the `Co-Authored-By` trailer. Branch: `feat/production-office` (already created).
- **Build hygiene:** adding a skill re-syncs bundles; commit ALL regenerated outputs, tree clean.

---

### Task 1: `context/guide-production.md` + source

**Files:**
- Create: `context/guide-production.md`
- Modify: `knowledge-base/Miscellaneous-Sources.md` (append one entry)

**Interfaces:**
- Produces: `context/guide-production.md` (bundled by Tasks 2, 4; read by the coordinator in Task 3). Defines the manifest schema every other piece references.

- [ ] **Step 1: Study** `context/guide-art-direction.md` and `context/guide-asset-reference.md` for the decision-unit format + cross-referencing voice; note `guide-execution.md`'s `.recipe` sidecar (endpoint, seed, refs, prompt, cost) - the manifest's `generations[]` derives from these.

- [ ] **Step 2: Write the guide.** Decision-unit format. Intro: the production office's craft - the manifest is the show's operational memory; it is a DERIVED index rebuilt from the files plus persisted human decisions. Sections:
  1. **The manifest as derived index + persisted status** - what is re-derived (assets/generations/cost from specs + `.recipe` sidecars) vs what MUST persist (the `human` block: approvals/notes). Because: derived data can always be rebuilt from the files (never rots); human decisions can't be, so they persist.
  2. **The status vocabulary** - `specced` (spec file exists) / `built` (has anchor image) / `rendered` (a generation exists) / `approved` / `needs-retake` / `missing`.
  3. **Reconcile discipline** - rebuild the derived blocks from a working-folder scan; **merge-preserve the `human` block by artifact id** (never drop an approval on rebuild); the files are the source of truth.
  4. **Cost tracking** - sum from `.recipe` sidecars; rollups by model and sequence; flag over-budget.
  5. **The coordinator's audits** - orphans (files not in any spec), specced-but-unrendered, missing refs, budget; defer state/geometry-drift detail to `script-supervisor`.
  6. **The worked manifest** - include this exact JSON example (schema reference):

```json
{
  "show": "SBW",
  "updated": "2026-07-02",
  "assets": [
    { "type": "char", "name": "eli", "spec_file": "char-sbw-eli.md", "anchor_image": "assets/char/eli/char-eli-id-front.png", "status": "built" },
    { "type": "set", "name": "livingroom", "spec_file": "set-sbw-livingroom.md", "anchor_image": null, "status": "specced" }
  ],
  "generations": [
    { "file": "assets/char/eli/char-eli-id-front.png", "fal_endpoint": "fal-ai/flux/schnell", "seed": 1278911897, "refs": [], "prompt": "...", "cost": 0.003, "rendered_at": "2026-07-02" }
  ],
  "sequences": [
    { "label": "S2", "shots": [ { "label": "S2-03", "refs": ["char-eli", "set-livingroom"], "generated": false } ] }
  ],
  "cost": { "total": 0.003, "by_model": { "fal-ai/flux/schnell": 0.003 }, "by_sequence": {} },
  "status": { "specced": 2, "built": 1, "rendered": 1, "approved": 0, "missing": 1 },
  "human": {
    "assets/char/eli/char-eli-id-front.png": { "status": "approved", "note": "hero locked" }
  }
}
```

  - Close with `## Quick application` + companion-guides line (`guide-asset-reference.md`, `guide-execution.md`, `model-currency-2026-06.md`, and `script-supervisor` for continuity audits).

- [ ] **Step 3: Append the source to `knowledge-base/Miscellaneous-Sources.md`:**

```markdown
## Eve Light Honthaner, _The Complete Film Production Handbook_

the line producer / production manager / coordinator's craft: tracking deliverables, forms, budgeting, the production office.

- https://www.routledge.com/The-Complete-Film-Production-Handbook/Honthaner/p/book/9780240811505
```

- [ ] **Step 4: Verify.** `grep -n "human\|derived\|merge-preserve\|status" context/guide-production.md` shows the anti-rot rule + status vocabulary; the JSON example parses (`python3 -c "import json,re,sys; t=open('context/guide-production.md').read(); b=t.split('```json')[1].split('```')[0]; json.loads(b); print('json ok')"`); `grep -n "Honthaner" knowledge-base/Miscellaneous-Sources.md` finds the source; no `[PLACEHOLDER]`.

- [ ] **Step 5: Commit.**

```bash
git add context/guide-production.md knowledge-base/Miscellaneous-Sources.md
git commit -m "feat(context): add guide-production (manifest as derived index + persisted status) + source"
```

---

### Task 2: `skills/production/SKILL.md`

**Files:**
- Create: `skills/production/SKILL.md`

**Interfaces:**
- Consumes (bundled by Task 4): `guide-production.md`, `guide-asset-reference.md`, `guide-execution.md`, `model-currency-2026-06.md`.
- Produces: `skills/production/SKILL.md`.

- [ ] **Step 1: Study** `skills/art-direction/SKILL.md` (the closest sibling - interview/scan -> doc) for frontmatter shape (`name` + multiline `description: >-` with trigger phrases) and the `](references/...)` link convention.

- [ ] **Step 2: Write `skills/production/SKILL.md`.** Frontmatter: `name: production` + `description: >-` with trigger phrases ("where are we", "production status", "build the manifest", "what did this cost", "what's left to render", "reconcile the production", "what's missing"). Body:
  - Purpose - build/reconcile the show's operational manifest and report status; the production office above the assets.
  - When to use - any "where are we / what's missing / what did it cost" question, or after a batch of generations.
  - Core principle - the manifest is a DERIVED index rebuilt from the files + a persisted `human` block; per `](references/guide-production.md)`.
  - Step: Scan - the working folder: `project-context-*`, `art-bible-*`, `char-`/`prop-`/`set-` specs, `assets/**`, `.recipe` sidecars, shot lists.
  - Step: Build/reconcile - regenerate the derived blocks (assets/generations/sequences/cost/status) per the schema in `guide-production.md`; **read the existing `production-{show}.json` first and merge-preserve its `human` block by artifact id.** Write `production-{show}.json` to the USER'S WORKING FOLDER.
  - Step: Report - status per sequence + asset (specced/built/rendered/approved/missing), cost rollups, and gaps (orphans, specced-but-unrendered, missing refs, over-budget). Reference `](references/guide-asset-reference.md)` for refs/taxonomy and `](references/guide-execution.md)` for the recipe fields.
  - Critical rules - never drop the `human` block on rebuild; write to the user's folder, never the plugin repo; the files are the source of truth (rebuildable); report in chat (the visual dashboard is a later layer).

- [ ] **Step 3: Verify.** `grep -n "](references/" skills/production/SKILL.md` lists the four links; frontmatter has `name` + `description`, no tabs; `grep -n "human\|merge-preserve\|production-{show}.json" skills/production/SKILL.md` shows the anti-rot rule; no `[PLACEHOLDER]`.

- [ ] **Step 4: Commit.**

```bash
git add skills/production/SKILL.md
git commit -m "feat(skills): add production skill (build/reconcile the manifest + report status)"
```

---

### Task 3: `plugin/agents/production-coordinator.md`

**Files:**
- Create: `plugin/agents/production-coordinator.md`

**Interfaces:**
- Consumes: `${CLAUDE_PLUGIN_ROOT}/context/guide-production.md` + `guide-asset-reference.md` + `guide-execution.md` (in `plugin/context/` after Task 4).
- Produces: an agent that passes assemble.py strict-YAML validation.

- [ ] **Step 1: Study** `plugin/agents/first-ad.md` and `plugin/agents/script-supervisor.md` for the persona -> fires -> method -> output structure and voice.

- [ ] **Step 2: Write `plugin/agents/production-coordinator.md`.** Frontmatter verbatim:

```markdown
---
name: production-coordinator
description: >-
  The Production Coordinator: the operational deputy who keeps the whole show
  tracked - which assets are built, which shots are rendered and approved, what is
  still missing, and what it all cost. Use when the user asks "where are we", "what's
  left", "what did this cost", "build/reconcile the production manifest", or "is
  anything missing". Maintains production-{show}.json (a derived index of assets,
  generations, and cost, plus persisted approvals) and reports status and gaps. Writes
  only the manifest, never the assets.
model: inherit
color: green
tools: ["Read", "Grep", "Glob"]
---
```
  Body: persona (the UPM / line producer / coordinator - the Creative Producer's operations partner - per `reference`/`guide-production.md`); When this agent fires; Method (read `${CLAUDE_PLUGIN_ROOT}/context/guide-production.md` + `guide-asset-reference.md` + `guide-execution.md`; run the `production` skill's scan/reconcile; merge-preserve the `human` block); Output (a status report - specced/built/rendered/approved/missing per sequence + asset, cost rollups, and the gaps to close; write only `production-{show}.json`). It reports and reconciles; it does not generate or edit assets.

- [ ] **Step 3: Verify frontmatter.** `sed -n '1,13p' plugin/agents/production-coordinator.md` shows the five keys, `color: green`, no `<` lines; the body names `production-{show}.json` and "writes only the manifest".

- [ ] **Step 4: Commit.**

```bash
git add plugin/agents/production-coordinator.md
git commit -m "feat(agents): add production-coordinator (operational deputy; manifest + status)"
```

---

### Task 4: Build wiring + integration validation (the gate)

**Files:**
- Modify: `skills/build.py` (add a `production` MANIFEST entry)
- Modify: `plugin/assemble.py` (add `production` to `SKILLS`)

**Interfaces:**
- Consumes: Tasks 1-3.
- Produces: bundled references for the production skill; a passing `VALIDATE: OK`.

- [ ] **Step 1: Add the `production` MANIFEST entry to `skills/build.py`** (after the `art-direction` entry):

```python
    "production": [
        ("guide-production.md", "references/guide-production.md"),
        ("guide-asset-reference.md", "references/guide-asset-reference.md"),
        ("guide-execution.md", "references/guide-execution.md"),
        ("model-currency-2026-06.md", "references/model-currency-2026-06.md"),
    ],
```

- [ ] **Step 2: Add `"production"` to `SKILLS` in `plugin/assemble.py`** (append after `"art-direction"`):

```python
SKILLS = ["project-context", "sequence-design", "shot-prompt", "model-docs", "footage-transform", "image-edit", "character-sheet", "prop-turntable", "location-pack", "art-direction", "production"]
```

- [ ] **Step 3: Run the skill build.**

```bash
python skills/build.py
```
Expected: `sync production: ...` lines for the four references + `zip ... production.skill`. No traceback.

- [ ] **Step 4: Run assemble + validate (the gate).**

```bash
python plugin/assemble.py
```
Expected: `skill: production` (among others) and final line `VALIDATE: OK`. If `FAIL ...`, fix the named missing reference/agent and re-run. Paste the final line into your report.

- [ ] **Step 5: Commit build-script edits AND every regenerated output.**

```bash
git add skills/build.py plugin/assemble.py skills/production plugin/context plugin/skills
git status --porcelain | grep -v '.superpowers'   # confirm nothing else pending
git commit -m "build: wire production skill into build.py + assemble.py"
```

- [ ] **Step 6: Confirm tree clean** (excluding `.superpowers/`): `git status --porcelain | grep -v '.superpowers'` prints nothing.

---

### Task 5: Docs, version bump + final validate

**Files:**
- Modify: `README.md`, `plugin/README.md`, `CHANGELOG.md`, `ROADMAP.md`, `plugin/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`

- [ ] **Step 1: Bump versions to `0.11.0`** in `plugin/.claude-plugin/plugin.json` (`"version"`), `.claude-plugin/marketplace.json` (BOTH `metadata.version` AND plugin-entry `version` - both currently 0.10.0), and README banners. Verify `grep -rn '0.10.0' plugin/.claude-plugin/plugin.json .claude-plugin/marketplace.json README.md` returns nothing (ignore filename/date strings).

- [ ] **Step 2: Update `README.md`** - add a `production` skill row (Level: Production office) and a `production-coordinator` agent row (Role: Production office); note the production office (manifest + coordinator that tracks status/cost/gaps). Update repo-layout counts to `skills/ (12) agents/ (12)`. Model list unchanged.

- [ ] **Step 3: Update `plugin/README.md`** - mirror the skill row + agent row; skill count language -> twelve skills.

- [ ] **Step 4: Add the `CHANGELOG.md` v0.11.0 entry** at the top:

```markdown
## v0.11.0 - 2026-07-02

### New: Production office - coordinator + manifest (v1.0 track)

- Added the `production` skill and `production-coordinator` agent: build/reconcile `production-{show}.json` - the show's operational memory - and report where the production stands.
- The manifest is a derived index rebuilt from the working folder (asset specs + `.recipe` sidecars) plus a persisted `human` block (approvals / needs-retake / notes) that a rebuild merge-preserves, so it can always be rebuilt from the files and can't rot.
- Tracks assets (specced/built), generations (from recipes), cost rollups (by model/sequence), and gaps (specced-but-unrendered, orphans, missing refs, over-budget).
- Added `context/guide-production.md` (the production-office craft + manifest schema); sources: Eve Light Honthaner, The Complete Film Production Handbook.
- Second of the v1.0 track (execution -> production office -> presentation). Twelve skills / twelve agents.
```

- [ ] **Step 5: Update `ROADMAP.md`** - in the v1.0-track note, mark the production office shipped (v0.11.0); presentation (contact sheets + dashboard) is the remaining step to v1.0.0.

- [ ] **Step 6: Final validate.**

```bash
python plugin/assemble.py
```
Expected: `VALIDATE: OK`.

- [ ] **Step 7: Commit.**

```bash
git add -A
git commit -m "docs: ship v0.11.0 production office (README/CHANGELOG/ROADMAP, version)"
```

---

## Post-plan notes

- **Final whole-branch review** (opus) then merge to `main`, tag `v0.11.0`, `python plugin/assemble.py --package`, `gh release create v0.11.0 generative-wrangler.plugin`.
- After all tasks: `git log --oneline feat/production-office` shows the spec + 5 task commits. Next: v1.0-c (presentation) -> v1.0.0.
