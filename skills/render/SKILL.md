---
name: render
description: >-
  Render a batch of prompts or a sequence's shot list into actual images or video via
  the Composio -> FAL MCP, then file the results and update the manifest. Use whenever
  the user wants to generate, not just write prompts — "render sbw020", "fire these
  prompts", "generate the shot list", "make the images", "run the batch". This skill
  finds the Composio->fal connection, confirms the cost estimate, submits the async
  batch, polls to completion, saves each output to its sequence or asset folder with a
  .recipe sidecar and a v001 version, and reconciles the production manifest. It honors
  the cost gate: no paid render without an estimate and an explicit human go-ahead.
---

# Render (execute prompts via Composio -> FAL)

Turn authored prompts into files on disk and keep the manifest current. This is the
execution counterpart to the prompt-writing skills: `shot-prompt`, `image-edit`,
`footage-transform`, and the asset skills hand you prompts; you fire them, file the
outputs with provenance, and hand the tally to the `production` skill. The full tool
sequence, batch pattern, and cost gate live in
[`references/guide-execution.md`](references/guide-execution.md) — read it first.

## When to use

Any "generate / render / fire / run the batch" request once prompts exist. Not for
writing prompts (that's `shot-prompt` and its siblings) and not for status (`production`).

## Step 1 — Find the connection

There is **no native fal MCP**. The models are reached through the **Composio** MCP
(composio.dev). Confirm the Composio connection and its `FAL_AI_*` tools (discover with
`COMPOSIO_SEARCH_TOOLS`, execute via `mcp__composio__COMPOSIO_MULTI_EXECUTE_TOOL`). If
Composio is not connected, say so and stop — this skill needs an interactive session
with Composio connected (`references/guide-execution.md`).

## Step 2 — Resolve inputs

Collect what to render: a sequence's `{show}{###}_shotlist.md`, a set of prompt files,
or an asset fan-out. For each item confirm the target model's `fal_endpoint`
(`FAL_AI_GET_MODELS`; `references/model-currency-2026-06.md` for the current id) and its
input schema. For i2i/i2v/v2v, `FAL_AI_UPLOAD_FILE` each local anchor/reference once and
reuse the `access_url` (`references/guide-execution.md` §4).

## Step 3 — Cost gate (mandatory)

Before any paid call, `FAL_AI_GET_PRICING`/`FAL_AI_ESTIMATE_PRICING` the model + input,
show the **batch total** (per-item cost x N), and get an explicit go-ahead. Flag audio as
a price lever (~2x on native-audio video). Never fire without sign-off
(`references/guide-execution.md` §5).

## Step 4 — Fire the batch

Submit every item as its own async job — `FAL_AI_SUBMIT_ASYNC_JOB` x N, back to back —
collect the `request_id`s, then poll each with `FAL_AI_QUEUE_GET_STATUS` to `COMPLETED`
and fetch with `FAL_AI_GET_QUEUE_REQUEST_RESULT`. Submit all first, then poll — never
submit -> poll -> submit (`references/guide-execution.md` §2-3). Use
`FAL_AI_RUN_MODEL_SYNC` only for a single quick still.

## Step 5 — File the outputs

Save each result to its taxonomy path with a version and a provenance sidecar
(`references/guide-asset-reference.md` §9):
- Shots -> `sequences/{show}{###}/{show}{###}_{SSSS}_v001.png` (increment `_v002`… on a
  re-render — never overwrite a version).
- Asset images -> `assets/{type}/{name}/{show}_{type}_{name}_{facet}_{view}_v001.png`.
- Write a `.recipe` sidecar next to each (`fal_endpoint`, `seed`, `refs`, `prompt`,
  `cost`, `rendered_at`) — the provenance the manifest derives from
  (`references/guide-execution.md` §6).

## Step 6 — Reconcile and hand off

Run the `production` skill so the new generations, cost rollups, and status land in
`{show}_production.json` (`references/guide-production.md`). Then hand off to `dailies`
for the render-vs-spec review.

## Critical rules

1. Composio is the connection — never assume a native fal MCP.
2. Cost gate before every paid render; confirm the batch total, not one item.
3. Submit all async jobs first, then poll — never serialize a batch.
4. Every saved render gets a `v001` version and a `.recipe` sidecar; never overwrite a version.
5. Reconcile the manifest as the close-out — never write a rule into CLAUDE.md
   (`references/guide-production.md` §7).
