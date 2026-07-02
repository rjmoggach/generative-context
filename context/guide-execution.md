# Execution — Rendering via Composio -> FAL

Decision rules for turning an authored prompt into an actual file on disk. The
other guides teach the agent how to *write* a prompt — the six-layer framework
(`guide-prompting-framework.md`) plus references (`guide-asset-reference.md`); this
one teaches the agent how to *run* it: which MCP tool to call, in what order, how to
batch, what it costs, and where the output lands. It is the execution counterpart to
`guide-ai-generation-strategy.md` (that guide is about *what* to ask for given model
limits; this one is about *how to actually call the model*).

The runtime engine is the **Composio -> FAL** MCP the user has connected. This
requires an **interactive session with Composio connected** — it does not work
headless or from a cron job, because the tools are agent-facing (no local API key,
no secret in the repo; auth lives in the user's Composio connection).

Each entry uses the library's decision-unit format:
**Decision / Use when / Because / Prompt translation / Watch-outs / Anchors.**

---

## 1. Single quick render (images)

- **Use when:** rendering one image from an already-authored prompt — a single hero
  still, one turnaround view, a one-off test.
- **Because:** for a single fast render, the synchronous path is simplest and returns
  the result directly; no polling needed.
- **Prompt translation:** `FAL_AI_GET_MODELS` first to confirm the endpoint and its
  input schema (the model doc's `fal_endpoint` field names the id, but the schema —
  which fields it accepts, e.g. `prompt`, `image_size` or `aspect_ratio`, `seed` —
  should be confirmed, since it can drift between doc-writing and render time). Then
  `FAL_AI_RUN_MODEL_SYNC` with `model_id` = the model doc's `fal_endpoint` and `input`
  = the assembled fields (`{prompt, image_size/aspect_ratio, ...}`). Read the result's
  `data.images[0].url` — validate it's present and non-empty before using it (§8) —
  and save to the asset taxonomy path (§6).
- **Watch-outs:** don't skip `GET_MODELS` even for a "known" endpoint — schemas
  change; don't skip the cost gate (§5) just because it's "only one image."
- **Anchors:** a one-shot API call — request in, result out, no queue.

## 2. Batch / concurrent generation (first-class)

- **Use when:** rendering any **SET** — turnaround views, coverage angles, a variant
  grid, multiple shots in a sequence, a character/prop/location fan-out. This is not
  an edge case; most real work is a set, not a single image.
- **Because:** fal's queue **parallelizes** submitted jobs — looping `RUN_MODEL_SYNC`
  one item at a time serializes what the platform would otherwise run concurrently,
  wasting wall-clock time for no benefit. The async queue is the correct default for
  more than one render, not just a fallback for slow models.
- **Prompt translation:** submit every item in the set as its own async job —
  `FAL_AI_SUBMIT_ASYNC_JOB` **x N**, one call per item, back to back — and collect
  each returned `request_id` into a list immediately (don't wait between submits).
  Once all N are submitted, poll each with `FAL_AI_QUEUE_GET_STATUS` until it reports
  `COMPLETED` (§8), then fetch each with `FAL_AI_GET_QUEUE_REQUEST_RESULT` and save.
  Track the batch lightly while it's in flight (§7).
- **Watch-outs:** never structure a batch as submit -> poll -> result -> submit next
  — that collapses back to serial and defeats the point. Submit *all* jobs first,
  *then* poll. Respect the concurrency cap (§5) — a "batch" is still gated by cost.
- **Anchors:** a job queue, not a request/response call — submit work, come back for
  results.

## 3. Video (always async)

- **Use when:** any video render — i2v, t2v, v2v — regardless of clip count.
- **Because:** video renders take materially longer than stills; there is no fast
  synchronous path. Treat every video job as async by default.
- **Prompt translation:** `FAL_AI_SUBMIT_ASYNC_JOB` -> `FAL_AI_QUEUE_GET_STATUS` (poll
  to `COMPLETED`) -> `FAL_AI_GET_QUEUE_REQUEST_RESULT`, exactly like §1's image path
  but never the sync tool. For multiple clips, apply the same batch pattern as §2 —
  submit all clips' jobs first, then poll the set together.
- **Watch-outs:** don't reach for `FAL_AI_RUN_MODEL_SYNC` for video even for a short
  clip — see §8's 405 note. Video jobs cost more per unit than stills; the cost gate
  (§5) matters even more here.
- **Anchors:** render-farm submission — hand off the job, poll for completion, fetch
  when done.

## 4. i2i / i2v / v2v inputs

- **Use when:** the render needs a local reference or anchor as input — editing an
  existing still, animating a locked character, transforming existing footage.
- **Because:** fal models take a hosted URL for image/video inputs, not a local file
  path; the local asset has to be uploaded before it can be referenced.
- **Prompt translation:** `FAL_AI_UPLOAD_FILE` the local anchor or reference image
  (from `assets/{type}/{name}/...`, per `guide-asset-reference.md`'s taxonomy) or
  source clip, take the returned `access_url`, and pass it as the model's `image_url`
  (i2i, i2v) or `video_url` (v2v) input field. Then proceed via §1/§2 (image) or §3
  (video). This is how "anchor, then fan out"
  (`guide-asset-reference.md` §1) and the edit mechanisms in `guide-image-editing.md`
  become real calls rather than craft description.
- **Watch-outs:** upload each distinct reference once and reuse the `access_url`
  across a batch of jobs that share it — don't re-upload the same file per job. For
  multi-reference composition (`guide-asset-reference.md` §5), upload each reference
  separately and map each `access_url` to its role in the input.
- **Anchors:** the reference has to live somewhere fal can fetch it — upload is the
  hand-off from local disk to the model.

## 5. Cost gate + concurrency cap

- **Use when:** before **any** paid render — single, batch, or video. No exceptions.
- **Because:** fal renders cost real money per call, and a batch or an unbounded
  concurrency multiplies that instantly; the human, not the agent, decides whether a
  spend is worth it.
- **Prompt translation:** call `FAL_AI_GET_PRICING` or `FAL_AI_ESTIMATE_PRICING` for
  the model + input before rendering, show the estimate to the user, and get explicit
  confirmation before calling `RUN_MODEL_SYNC` or `SUBMIT_ASYNC_JOB`. For a batch,
  estimate and confirm the **batch total** (per-item cost x N), not just one item's
  cost, and **cap how many jobs fire without a fresh confirmation** — a sane default
  is to proceed freely under a small N and require explicit confirmation above it (a
  fat-finger shouldn't be able to fire 100 jobs on one "yes").
- **Watch-outs:** re-confirm if the input changes after the estimate (resolution,
  duration, model tier all move price); don't amortize a "the user said go earlier"
  confirmation across an unrelated new batch. **Audio is a price lever, not a free
  extra** — enabling native audio (Veo, Sora, Wan, Kling) roughly **doubles** the
  per-clip cost, so treat it as opt-in, state it explicitly in the estimate, and
  confirm the audio setting along with the price before rendering.
- **Anchors:** a budget approval before a purchase order — estimate, then sign-off,
  every time.

## 6. Output + provenance

- **Use when:** saving any completed render.
- **Because:** an image with no record of how it was made is unreproducible and
  un-auditable — the recipe is what lets a later shot, a QC pass, or the script
  supervisor trust or re-derive the asset.
- **Prompt translation:** save the file to `assets/{type}/{name}/<taxonomy-name>`
  per `guide-asset-reference.md` §9 (images carry **no** `{show}` in the filename —
  the show is implied by the folder, not encoded in the image name). Write a
  `.recipe` sidecar next to it (same stem, `.recipe` extension) recording: the
  `fal_endpoint` used, the `seed` (if the model returned or accepted one), the `refs:`
  consumed (asset ids, per `guide-asset-reference.md` §10), the full prompt sent, and
  the cost charged. The recipe is the seed record the later production manifest will
  formalize — write it now even though nothing downstream consumes it yet.
- **Watch-outs:** write the recipe *after* confirming the output saved correctly, not
  before — a recipe for a file that never landed is worse than no recipe. Keep the
  recipe plain text/YAML-ish, not another format to parse.
- **Anchors:** a camera report / take log — what stock, what settings, what take,
  filed with the footage.

## 7. In-flight batch tracking (light)

- **Use when:** any batch is submitted and not yet fully collected.
- **Because:** with N jobs in flight, losing track of even one `request_id` means a
  render that was paid for is silently dropped.
- **Prompt translation:** keep a simple running list — one line per job — of
  `request_id` + status (`submitted` -> `in-progress` -> `completed` -> `saved`).
  Update it as each job's `QUEUE_GET_STATUS` changes and again once its result is
  fetched and written to disk. This can be as light as a scratch note held for the
  duration of the batch — it doesn't need to be a persisted file.
- **Watch-outs:** don't consider a batch "done" until every tracked id reaches
  `saved`, not just `completed` (completed-but-unfetched is still an open job).
- **Anchors:** a call sheet's shot-status column — nothing wraps until every line is
  checked off.

## 8. Troubleshooting

- **Async 405 on the sync path:** if a model rejects synchronous calls (405), it only
  supports the async queue — switch to the explicit `SUBMIT_ASYNC_JOB` ->
  `QUEUE_GET_STATUS` -> `GET_QUEUE_REQUEST_RESULT` sequence rather than a subscribe/
  streaming variant; the explicit poll-and-fetch path is the reliable one.
- **Fetching before completion:** poll `QUEUE_GET_STATUS` until it reports
  `COMPLETED` before calling `GET_QUEUE_REQUEST_RESULT` — fetching earlier returns an
  incomplete or empty result, not an error, so it can look like a rendering failure
  when it's actually a timing issue.
- **Empty `images` array:** validate `data.images` is non-empty before reading
  `[0].url` — an empty array (content filtered, generation failed silently) will
  throw on the index instead of surfacing the real cause.
- **`content_type` mismatch:** the returned `content_type` may not match the URL's
  file extension (e.g. reports `image/png` for a `.jpg` URL) — trust the URL, not the
  declared content type, when deciding how to save or extension-match the file.
- **422 content-policy after COMPLETED:** a job can report complete and still fail
  content-policy review on fetch (422) — this is a valid rejection, not a bug; adjust
  the prompt (remove the flagged element) and resubmit as a new job rather than
  retrying the same one.
- **fal unavailable:** fall back to `GEMINI_GENERATE_IMAGE` (Nano Banana, up to 14
  reference images, 4K output) for image renders only — there is no video fallback;
  video renders simply wait for fal to come back.

---

## Quick application

1. Confirm the endpoint + schema with `FAL_AI_GET_MODELS`.
2. **Estimate and confirm cost** (`FAL_AI_GET_PRICING`/`ESTIMATE_PRICING`) before any
   paid call — batch total for a set, capped concurrency.
3. Single image -> `RUN_MODEL_SYNC`; **any set or video -> submit all async jobs
   first, then poll and collect** (never one-at-a-time).
4. i2i/i2v/v2v -> `FAL_AI_UPLOAD_FILE` the reference first, pass `access_url`.
5. Save to the taxonomy path, write the `.recipe` sidecar.
6. Track in-flight `request_id`s until every one reaches `saved`.
7. On failure, check §8 before assuming the render itself is broken.
8. **Close-out:** once renders are saved, reconcile the show manifest by running the
   `production` skill so `{show}_production.json` and the cost rollups stay current
   (`guide-production.md`). Do this as a step you perform — never install it as a rule
   in the user's `CLAUDE.md` (`guide-production.md` §7).

Companion: `guide-asset-reference.md`, `guide-image-editing.md`,
`guide-ai-generation-strategy.md`, `model-currency-2026-06.md`.
