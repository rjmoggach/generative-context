# Execution Layer — Closed Render Loop (v1.0-a) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship v0.10.0 - wrangler can actually render (images + video, concurrently) by driving the connected Composio -> FAL MCP, via a `guide-execution.md` playbook + per-skill generate steps + `fal_endpoint` model mapping. No script, no key.

**Architecture:** `context/` is the source of truth; `skills/build.py` bundles context into each skill's `references/`; `plugin/assemble.py` regenerates `plugin/context/` + `plugin/skills/` and validates. No unit tests - the gate is `python plugin/assemble.py` printing `VALIDATE: OK` + `python skills/build.py` clean. The execution layer is DOCUMENTATION the agent follows to call Composio->FAL tools - no code ships. Mirrors the Phase 1-4 pipelines.

**Tech Stack:** Markdown (library + skills), Python 3 stdlib build scripts. The runtime engine is the Composio MCP (`FAL_AI_*` tools) - agent-facing, not called by the build. Spec: `docs/superpowers/specs/2026-07-02-execution-layer-design.md`.

## Global Constraints

- **Target version:** `0.10.0` - verbatim in `plugin/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` (both `metadata.version` and plugin-entry `version`), README banners.
- **Execution model:** agent-orchestrated via the **Composio -> FAL** MCP; NO render script, NO key/`.env` in the repo. Needs an interactive session with Composio connected (not headless/cron).
- **Concurrency = fal's async queue:** batch = `FAL_AI_SUBMIT_ASYNC_JOB` x N -> collect `request_id`s -> poll (`QUEUE_GET_STATUS`) -> collect (`GET_QUEUE_REQUEST_RESULT`). Never loop one-at-a-time; never use subagents for raw fan-out.
- **Cost gate:** before ANY paid run, `FAL_AI_GET_PRICING`/`ESTIMATE_PRICING` + human confirmation; for a batch, confirm the batch total and cap concurrency.
- **MCP use during the BUILD is read-only only:** Task 2 may call `FAL_AI_GET_MODELS` (free) to confirm endpoint ids. NEVER call `RUN_MODEL_SYNC` / `SUBMIT_ASYNC_JOB` (paid) during implementation - the only paid call is the controller-run smoke-test at the end, with user consent.
- **House style:** `guide-*.md` decision-unit format, em-dashes, straight quotes, no emojis, technical terms in `code`. `model-*.md` docs: plain, no emojis/em-dashes. No `[PLACEHOLDER]`. Project name stays `generative-wrangler`.
- **Taxonomy:** outputs save to `assets/{type}/{name}/…` (images carry no `{show}`); each output gets a `.recipe` sidecar (endpoint, seed, refs, prompt, cost).
- **Commits:** OMIT the `Co-Authored-By` trailer. Branch: `feat/execution-layer` (already created).
- **Build hygiene:** editing model docs / adding `guide-execution.md` re-syncs bundles; commit ALL regenerated outputs, tree clean.

---

### Task 1: `context/guide-execution.md` (the agent playbook)

**Files:**
- Create: `context/guide-execution.md`

**Interfaces:**
- Produces: `context/guide-execution.md` (bundled by Task 4; linked from the generate-steps in Task 3).

- [ ] **Step 1: Study** `context/guide-image-editing.md` and `context/guide-asset-reference.md` for the decision-unit format and cross-referencing voice; skim `context/guide-ai-generation-strategy.md` (this guide is its execution counterpart).

- [ ] **Step 2: Write the guide.** Decision-unit format. Intro: the agent's playbook for actually rendering via the connected Composio -> FAL MCP; wrangler authors the prompt (six-layer + refs), this guide turns it into files. Note the hard requirement: an interactive session with Composio connected. Sections:
  1. **Single quick render (images)** - `FAL_AI_GET_MODELS` (confirm the endpoint + input schema) -> `FAL_AI_RUN_MODEL_SYNC` (`model_id` = the model doc's `fal_endpoint`, `input` = `{prompt, image_size/aspect_ratio, ...}`) -> read `data.images[0].url` -> save to the taxonomy path.
  2. **Batch / concurrent generation (first-class)** - for any SET (coverage, a turnaround's views, variant grids, multiple shots): submit ALL as async jobs (`FAL_AI_SUBMIT_ASYNC_JOB` x N), collect the `request_id`s, then poll (`QUEUE_GET_STATUS`) and collect (`GET_QUEUE_REQUEST_RESULT`) each. Never loop one-at-a-time - fal parallelizes.
  3. **Video (always async)** - always submit + poll (video is long); same batch pattern for multiple clips.
  4. **i2i / i2v / v2v inputs** - `FAL_AI_UPLOAD_FILE` to host the local anchor/reference -> pass the `access_url` as `image_url` / `video_url`; cross-ref `guide-asset-reference.md` (anchor-then-fan-out) and `guide-image-editing.md`.
  5. **Cost gate + concurrency cap** - before ANY paid run call `FAL_AI_GET_PRICING`/`FAL_AI_ESTIMATE_PRICING`, show the estimate, get human confirmation; for a batch confirm the batch total and cap how many fire at once (default: confirm above a small N).
  6. **Output + provenance** - save to `assets/{type}/{name}/<taxonomy-name>` (no `{show}` in image names) + a `.recipe` sidecar (endpoint, seed, refs, prompt, cost). Note the recipe is the seed of the (later) production manifest.
  7. **In-flight batch tracking (light)** - keep a simple list of the batch's `request_id`s + status (submitted/in-progress/completed/saved) so nothing is lost mid-batch.
  8. **Troubleshooting** - async 405 (prefer explicit submit->poll->result over subscribe); poll to `COMPLETED` before fetching; validate `images` non-empty before `[0].url`; `content_type` may mismatch the URL extension (trust the URL); 422 content-policy can occur post-complete (adjust + resubmit). Fallback: `GEMINI_GENERATE_IMAGE` (Nano Banana, up to 14 refs, 4K) if fal is unavailable.
  - Close with `## Quick application` + companion-guides line (`guide-asset-reference.md`, `guide-image-editing.md`, `guide-ai-generation-strategy.md`, `model-currency-2026-06.md`).

- [ ] **Step 3: Verify.** `grep -n "SUBMIT_ASYNC_JOB\|RUN_MODEL_SYNC\|fal_endpoint\|.recipe\|GET_PRICING" context/guide-execution.md` shows the key tools/concepts; decision-unit format; no `[PLACEHOLDER]`.

- [ ] **Step 4: Commit.**

```bash
git add context/guide-execution.md
git commit -m "feat(context): add guide-execution (agent playbook for Composio->FAL rendering + batch)"
```

---

### Task 2: `fal_endpoint` on generative model docs + currency note

**Files:**
- Modify: `context/model-image-flux-pro.md`, `context/model-image-gemini-flash.md`, `context/model-image-seedream-4.md`, `context/model-image-luma-uni-1.md`, `context/model-editing-flux-kontext.md`, `context/model-video-seedance-pro.md`, `context/model-video-runway-gen4-turbo.md`, `context/model-video-google-veo-3-1.md`, `context/model-video-luma-ray3.md`, `context/model-video-kling-3.md`, `context/model-video-wan-2-6.md`, `context/model-image-midjourney-v7.md`, `context/model-video-sora-2.md`
- Modify: `context/model-currency-2026-06.md`

**Interfaces:**
- Produces: a `fal_endpoint` field on each generative model doc that Task 1's guide and Task 3's skills reference when picking `model_id`.

- [ ] **Step 1: Confirm endpoint ids via read-only discovery.** Use the Composio MCP tool `FAL_AI_GET_MODELS` (free, read-only) - e.g. `category: "text-to-image"`, `"image-to-image"`, `"image-to-video"`, `"text-to-video"`, or `q:` search per model name - to find the real fal endpoint id for each model (namespace/name, e.g. `fal-ai/nano-banana-2/edit`, `fal-ai/flux-pro`). DO NOT call any paid tool (`RUN_MODEL_SYNC`/`SUBMIT_ASYNC_JOB`). If the connection is unavailable in your context, mark ids `verify via FAL_AI_GET_MODELS` rather than guessing.

- [ ] **Step 2: Add a `fal_endpoint` row** to each generative doc's Quick Reference table (or a `> **fal endpoint:** ...` line if no table row fits), e.g. `| **fal endpoint** | \`fal-ai/nano-banana-2/edit\` |`. For a model NOT available on fal (confirm via GET_MODELS - likely Midjourney and possibly Sora), state `not available via fal - use native API` and, where useful, name the closest fal alternative. Never invent an id.

- [ ] **Step 3: Add a one-line note to `context/model-currency-2026-06.md`** near the caveats subsection: "Each generative `model-*.md` carries a `fal_endpoint` for rendering via the Composio -> FAL MCP (see `guide-execution.md`); verify ids with `FAL_AI_GET_MODELS`."

- [ ] **Step 4: Verify.** `grep -l "fal_endpoint\|fal endpoint" context/model-*.md | wc -l` shows all 13 generative docs updated; no guessed ids (uncertain ones say `verify via FAL_AI_GET_MODELS`); `grep -n "fal_endpoint" context/model-currency-2026-06.md` shows the note.

- [ ] **Step 5: Commit.**

```bash
git add context/model-*.md
git commit -m "feat(context): add fal_endpoint mapping to generative model docs (confirmed via FAL_AI_GET_MODELS)"
```

---

### Task 3: Per-skill "generate" step

**Files:**
- Modify: `skills/image-edit/SKILL.md`, `skills/character-sheet/SKILL.md`, `skills/prop-turntable/SKILL.md`, `skills/location-pack/SKILL.md`, `skills/art-direction/SKILL.md`, `skills/shot-prompt/SKILL.md`, `skills/footage-transform/SKILL.md`

**Interfaces:**
- Consumes: `guide-execution.md` (Task 1) via a `](references/guide-execution.md)` link (bundled in Task 4).
- Produces: a generate step in each generative skill.

- [ ] **Step 1: Add a short "Generate (optional)" step** to each of the seven skills (after the skill's output/build step, before Critical rules), reading: "To actually render (not just hand off the prompt), follow `](references/guide-execution.md)`: pick the model's `fal_endpoint`, upload any reference image, run - or **submit a batch** for a set (coverage, turnaround views, variants) - save each output to its taxonomy path, and record the `.recipe`. Always confirm the cost estimate first." Keep it to a few lines; do NOT restate the guide (DRY). Do NOT change frontmatter.

- [ ] **Step 2: Add a Critical rule** to each skill: "Rendering spends money - always confirm the `FAL_AI_GET_PRICING` estimate before generating, and submit sets as a batch, not one at a time."

- [ ] **Step 3: Verify.** `grep -l "](references/guide-execution.md)" skills/*/SKILL.md | wc -l` shows 7; each edited skill has the generate step + rule; frontmatter unchanged; no `[PLACEHOLDER]`.

- [ ] **Step 4: Commit.**

```bash
git add skills/image-edit/SKILL.md skills/character-sheet/SKILL.md skills/prop-turntable/SKILL.md skills/location-pack/SKILL.md skills/art-direction/SKILL.md skills/shot-prompt/SKILL.md skills/footage-transform/SKILL.md
git commit -m "feat(skills): add generate step (render via guide-execution) to the seven generative skills"
```

---

### Task 4: Build wiring + integration validation (the gate)

**Files:**
- Modify: `skills/build.py` (add `guide-execution.md` to the MANIFEST of the seven generative skills)

**Interfaces:**
- Consumes: Tasks 1-3.
- Produces: `guide-execution.md` bundled into the seven skills; regenerated bundles; a passing `VALIDATE: OK`.

- [ ] **Step 1: Add the pair `("guide-execution.md", "references/guide-execution.md"),`** inside each of these seven MANIFEST entries in `skills/build.py`: `image-edit`, `character-sheet`, `prop-turntable`, `location-pack`, `art-direction`, `shot-prompt`, `footage-transform`. (Insert after the `guide-image-editing.md` pair where present, else after `guide-asset-reference.md`; match indentation.) Confirm valid Python: `python3 -c "import ast; ast.parse(open('skills/build.py').read())"`.

- [ ] **Step 2: Run the skill build.**

```bash
python skills/build.py
```
Expected: `sync <skill>: guide-execution.md -> references/guide-execution.md` for the seven skills; it also re-syncs every skill that bundles the edited model docs (Task 2) - expected. No traceback.

- [ ] **Step 3: Run assemble + validate (the gate).**

```bash
python plugin/assemble.py
```
Expected: final line `VALIDATE: OK`. If `FAIL ...`, the named `](references/guide-execution.md)` link isn't yet in that skill's MANIFEST - add it and re-run. Paste the final line into your report.

- [ ] **Step 4: Commit build.py edit AND every regenerated output.**

```bash
git add skills/build.py skills plugin/context plugin/skills
git status --porcelain | grep -v '.superpowers'   # confirm nothing else pending
git commit -m "build: bundle guide-execution into the seven generative skills; re-sync"
```

- [ ] **Step 5: Confirm tree clean** (excluding `.superpowers/`): `git status --porcelain | grep -v '.superpowers'` prints nothing. If a regenerated file remains, `git add` it and amend.

---

### Task 5: Docs, version bump + final validate

**Files:**
- Modify: `README.md`, `plugin/README.md`, `CHANGELOG.md`, `ROADMAP.md`, `plugin/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`

- [ ] **Step 1: Bump versions to `0.10.0`** in `plugin/.claude-plugin/plugin.json` (`"version"`), `.claude-plugin/marketplace.json` (BOTH `metadata.version` AND plugin-entry `version` - both currently 0.9.0), and README banners. Verify `grep -rn '0.9.0' plugin/.claude-plugin/plugin.json .claude-plugin/marketplace.json README.md` returns nothing (ignore filename/date strings).

- [ ] **Step 2: Add a "Generating (closed loop)" note to `README.md`** (a short subsection): wrangler can now render via the connected Composio -> FAL MCP - single images, i2i, and batch/video via fal's async queue - following `context/guide-execution.md`; note it needs an interactive session with Composio connected. Skill/agent counts unchanged (ten skills / eleven agents).

- [ ] **Step 3: Mirror the note in `plugin/README.md`.**

- [ ] **Step 4: Add the `CHANGELOG.md` v0.10.0 entry** at the top:

```markdown
## v0.10.0 - 2026-07-02

### New: Execution layer - closed render loop (v1.0 track)

- wrangler can now actually generate, not just prompt: `context/guide-execution.md` is the agent's playbook for driving the connected Composio -> FAL MCP (`FAL_AI_*` tools).
- Concurrent generation via fal's async queue - submit a set (coverage, turnaround views, variants, multiple clips) as a batch of `SUBMIT_ASYNC_JOB` calls, poll, and collect; video is always async.
- Each generative `model-*.md` gained a `fal_endpoint` for model routing; each generative skill gained a "generate" step pointing at `guide-execution.md`.
- Hard cost gate: confirm the `FAL_AI_GET_PRICING` estimate before any paid run; batches confirm the total and cap concurrency. Outputs save to the taxonomy path with a `.recipe` provenance sidecar.
- Agent-orchestrated (no render script, no key in the repo - auth is your Composio connection); needs an interactive session. First of the v1.0 track (execution -> production office -> presentation).
```

- [ ] **Step 5: Add a "v1.0 track" note to `ROADMAP.md`** (after the roadmap-complete line): the art-department roadmap (Phases 0-4) is complete; the **v1.0 track** adds the closed production loop - execution (v0.10.0, shipped), then the production-coordinator/manifest, then the presentation layer, reaching v1.0.0 when make -> manage -> review is complete.

- [ ] **Step 6: Final validate.**

```bash
python plugin/assemble.py
```
Expected: `VALIDATE: OK`.

- [ ] **Step 7: Commit.**

```bash
git add -A
git commit -m "docs: ship v0.10.0 execution layer (README/CHANGELOG/ROADMAP, version)"
```

---

## Post-plan notes

- **Final whole-branch review** (opus) then merge to `main`, tag `v0.10.0`, `python plugin/assemble.py --package`, `gh release create v0.10.0 generative-wrangler.plugin`.
- **Live smoke-test (controller-run, with user consent):** after merge (or before release), run ONE cheap image end-to-end in-session: `FAL_AI_GET_MODELS` -> `FAL_AI_GET_PRICING` (show estimate) -> **get the user's explicit go-ahead for the ~few-cent spend** -> `FAL_AI_RUN_MODEL_SYNC` on a cheap image endpoint -> save the URL to a scratch path -> write the `.recipe`. Do NOT run video/batch in the smoke-test. This proves the whole path live; it is not a subagent task (it spends money and needs the connected session).
- After all tasks: `git log --oneline feat/execution-layer` shows the spec + 5 task commits.
