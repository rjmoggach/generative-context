# Execution Layer — Closed Render Loop (v1.0-a) — Design

**Date:** 2026-07-02 · **Status:** Approved · **Target release:** v0.10.0
**Owner:** Rob (Creative Producer) · **Track:** toward v1.0 (make -> manage -> review)

---

## 1. Goal

Close the render loop: give wrangler a way to **actually generate** images and
video (not just author prompts) by driving the **Composio -> FAL** MCP tools the
user has connected, and to do it **concurrently** (fan out N generations at once).
wrangler stays pure-text; the agent orchestrates the MCP. This is the first of the
three v1.0 layers (execution -> production office -> presentation).

## 2. Scope (v1.0-a) -> v0.10.0

**In:** `guide-execution.md` (the agent playbook incl. batch/concurrent generation),
a `fal_endpoint` field on each generative `model-*.md`, a "generate" step in the
generative skills, an output/provenance convention (`.recipe` sidecar + light
in-flight batch tracking), build wiring, docs, version bump, and one paid smoke-test.
**Out:** the production-coordinator + manifest (v1.0-b) and the presentation layer
(v1.0-c). No render script, no local key (agent-orchestrated via the Composio
connection). No new creative-craft source (this is plumbing, not craft).

## 3. Decisions locked in brainstorming

1. **Agent-orchestrated + guide**, not a script — auth is the user's Composio
   connection; nothing secret lives in the repo. Works in an interactive session
   (Cowork); does not work headless/cron (Composio MCP must be connected).
2. **Concurrency = fal's async queue**, not subagents. Fan out `SUBMIT_ASYNC_JOB`
   x N (each returns a `request_id` immediately, non-blocking), fal runs them in
   parallel, then poll/collect. Subagents/Workflows are reserved for later, only
   when each item needs *reasoning* around the render (variant->judge, render->QC).
3. **Version v0.10.0** for the execution layer; **1.0.0 reserved** for the complete
   make->manage->review loop (a + b + c).

## 4. `context/guide-execution.md` (the agent playbook)

Decision-unit format. The one place that teaches the agent how to drive Composio->FAL.

- **Single quick render (images):** `FAL_AI_GET_MODELS` (confirm the endpoint +
  input schema) -> `FAL_AI_RUN_MODEL_SYNC` (`model_id` = the model's `fal_endpoint`,
  `input` = `{prompt, image_size/aspect, ...}`) -> read `data.images[0].url` -> save
  to the taxonomy path.
- **Batch / concurrent generation (first-class):** for any SET - coverage, a
  turnaround's views, variant grids, multiple shots - **submit all as async jobs**
  (`FAL_AI_SUBMIT_ASYNC_JOB` x N), collect the `request_id`s, then poll
  (`QUEUE_GET_STATUS`) and collect (`GET_QUEUE_REQUEST_RESULT`) each. Never loop
  one-at-a-time. fal parallelizes the compute.
- **Video (always async):** always `SUBMIT_ASYNC_JOB` + poll (video is long); same
  batch pattern for multiple clips.
- **i2i / i2v / v2v inputs:** `FAL_AI_UPLOAD_FILE` to host the local anchor/reference
  -> pass the returned `access_url` as the model's `image_url` / `video_url`. This is
  how anchor-then-fan-out becomes real.
- **Cost gate (hard rule):** before ANY paid run, call `FAL_AI_GET_PRICING` /
  `FAL_AI_ESTIMATE_PRICING`, show the estimate, and get human confirmation. For a
  **batch**, estimate and confirm the **batch total**, and **cap concurrency** (a
  sane default, e.g. warn/confirm above N jobs) so a fat-finger can't fire 100 jobs.
- **Output + provenance:** save each output to `assets/{type}/{name}/<taxonomy-name>`
  (images carry no `{show}`), and write a small **`.recipe`** sidecar next to it
  recording `fal_endpoint`, seed, `refs:`, the prompt, and cost. The recipe is the
  seed of the v1.0-b manifest.
- **In-flight batch tracking (light):** keep a simple list of the batch's
  `request_id`s with status (submitted / in-progress / completed / saved) so nothing
  is lost mid-batch. v1.0-b's manifest formalizes this into the render-queue tracker.
- **Troubleshooting:** the real pitfalls - async 405 (prefer explicit submit->poll->
  result over subscribe), poll to `COMPLETED` before fetching the result, validate
  `images` is non-empty before reading `[0].url`, `content_type` may mismatch the URL
  extension (trust the URL), 422 content-policy can occur post-complete (adjust +
  resubmit). Image fallback: `GEMINI_GENERATE_IMAGE` (Nano Banana, up to 14 refs, 4K)
  if fal is unavailable.

## 5. `fal_endpoint` field on generative `model-*.md`

Add a `fal_endpoint` line to the Quick Reference of each generative model doc,
mapping our model name to its fal id (namespace/name, e.g. `fal-ai/nano-banana-2/edit`,
`fal-ai/flux-pro`, `fal-ai/kling-video/...`). **Confirm each id via `FAL_AI_GET_MODELS`
(read-only, free) - do NOT guess.** Where a model is NOT on fal (e.g. Midjourney, Sora
if absent), state that explicitly and point at the native path / a fal alternative. Add
a one-line "fal endpoint" note to `model-currency-2026-06.md`. Applies to the
image/editing/video generative docs (not the currency file itself).

## 6. Per-skill "generate" step

A short, additive step in the generative skills - `image-edit`, `character-sheet`,
`prop-turntable`, `location-pack`, `art-direction`, `shot-prompt`, `footage-transform`
- reading: "To actually render, follow `](references/guide-execution.md)`: pick the
model's `fal_endpoint`, upload any reference, run (or **submit a batch** for a set -
coverage, turnaround views, variants), save to the taxonomy path, and record the
recipe. Always confirm the cost estimate first." DRY - each just points at the guide.
Add `](references/guide-execution.md)` links (bundled in build wiring).

## 7. Build wiring + docs

- `skills/build.py`: add `guide-execution.md` to the MANIFEST of each of the seven
  generative skills (so they bundle the execution craft). No new skills/agents/helpers
  -> no `assemble.py` `SKILLS`/`HELPERS` change.
- `python plugin/assemble.py` must end `VALIDATE: OK`; commit all regenerated bundles
  (editing model docs + adding the guide re-syncs bundles; the Phase 1-4 lesson).
- `README.md` + `plugin/README.md`: add a short **"Generating (closed loop)"** note -
  wrangler can now render via the connected Composio->FAL MCP, including batch/video;
  point at `guide-execution.md`; note it needs an interactive session with Composio
  connected. Banner 0.10.0.
- `CHANGELOG.md` v0.10.0 entry; `ROADMAP.md`: add a short "v1.0 track (execution ->
  production office -> presentation)" note with this as the first step. Versions 0.10.0
  in `plugin/.claude-plugin/plugin.json` + `.claude-plugin/marketplace.json` (both).

## 8. Smoke-test (end of build, in-session)

After the build validates, run ONE cheap image render end-to-end to prove the path:
`FAL_AI_GET_MODELS` -> `GET_PRICING` (show the estimate) -> **get the user's explicit
go-ahead for the ~few-cent spend** -> `RUN_MODEL_SYNC` on a cheap image endpoint ->
save the URL to a scratch/test path -> write the `.recipe`. Composio is already
connected, so no key handoff. Do NOT run video or batch in the smoke-test (cost).

## 9. Verification

- `python plugin/assemble.py` -> `VALIDATE: OK`; `python skills/build.py` clean.
- Every `](references/guide-execution.md)` link in the edited skills resolves
  (bundled).
- `fal_endpoint` present on each generative model doc, each confirmed via
  `FAL_AI_GET_MODELS` or explicitly marked not-on-fal (no guessed ids).
- `guide-execution.md` covers: single, batch, video, i2i inputs, cost gate + cap,
  provenance recipe, in-flight tracking, troubleshooting, fallback.
- No `[PLACEHOLDER]`; project name stays `generative-wrangler`.

## 10. Approach considered & rejected

- **A local `render.py` script:** rejected - can't use the Composio MCP (agent-facing);
  would need its own key/secret in a `.env`, reintroducing a dependency off the path
  the user set up.
- **Subagents per generation for concurrency:** rejected for raw fan-out - redundant
  with fal's async queue (fal already parallelizes; submission is non-blocking) and N x
  the agent overhead. Reserved for later, only when each item needs reasoning.
- **Building our own local queue:** rejected - fal's async queue is the queue.
