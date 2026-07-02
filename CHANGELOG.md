# Changelog

All notable changes to the Generative AI Context Library will be documented in this file.

## v1.3.1 - 2026-07-02

### Sequence taxonomy refinements (#6)

- **Flattened the sequence folder.** No `shots/` or `context/` subfolders — the shot list, per-sequence context, and renders all live directly in `sequences/{show}{###}/` (`{show}{###}_shotlist.md`, `{show}{###}_context.md`, `{show}{###}_{SSSS}_vNN.png`).
- **Configurable numbering.** `project-context` now asks for the sequence/shot zero-pad width and increment at setup and records the scheme in `{show}_project_context.md`; every skill reads it. Default: sequences 3-digit by tens (`sbw010`, `sbw020`; insert `sbw015`), shots 4-digit by tens (`sbw010_0010`; insert `_0015`).

## v1.3.0 - 2026-07-02

### Sequence entity taxonomy (#5)

Sequences are now a first-class entity mirroring assets — everything belonging to a sequence lives inside its own folder. (Supersedes v1.2.0's flat `{show}{NNNN}` by-10s numbering.)

- **Entity folder + id grammar.** A sequence is `sequences/{show}{###}/` — show code + zero-padded **three-digit** number, **concatenated** (`sbw002`), the one deliberate exception to the underscore rule. Inside: `{show}{###}_shotlist.md`, a per-sequence `context/{show}{###}_context.md`, and `shots/` for renders. Shot ids are `{show}{###}_{SSSS}` (4-digit by 10s → `sbw002_0010`) — the canonical handle in shot lists, `refs`, and render filenames.
- **Scaffold.** `project-context` scaffolds `sequences/` and `refs/` alongside `context/` + `assets/`; `sequence-design` creates each `sequences/{show}{###}/` on first touch and writes only inside it.
- **External source ingest.** Raw source (client briefs, decks, Drive exports) -> `refs/` verbatim; sequence context derived from a source is split **one file per sequence** into `sequences/{show}{###}/context/{show}{###}_context.md` with a provenance line. A compiled multi-sequence doc is never left whole.
- **Reconcile covers sequences.** The `production` skill's Step 1.5 relocates loose sequence files into the right entity folder, and a **fifth audit** flags any file under `sequences/` not inside a `{show}{###}/` folder.

## v1.2.0 - 2026-07-02

### Project scaffold + sequence numbering (#3, #4)

- **Up-front scaffold (#3).** `project-context` now lays down the working-folder skeleton at project start — a `context/` folder (holding `{show}_project_context.md` + `{show}_art_bible.md`) and the `assets/{char,prop,set,veh,cam,light,style,fx}/` type dirs. `sequences/` and `renders/` are created lazily when first needed. Asset specs now live inside their asset folder beside the images. The `production` skill's reconcile relocates loose legacy files into the scaffold (on top of the v1.1.0 rename/normalize), and its scan globs + the manifest schema follow the new paths.
- **Sequence/shot numbering (#4).** Sequences and shots use a VFX increment-by-10 convention: `sequences/{show}{NNNN}/{show}{NNNN}_{SSSS}.md`, numbered `0010, 0020, 0030…` so inserts drop in cleanly (`0015`). The shot stem `{show}{NNNN}_{SSSS}` is the canonical shot id in shot lists, `refs`, and render filenames (replacing ad-hoc `S2-03` labels). `sequence-design` emits on this numbering.
- Swept up naming stragglers the v1.1.0 pass missed (bare `char-`/`prop-` prefixes in `guide-production` and both READMEs, old suffix scan globs, old shot labels).

## v1.1.0 - 2026-07-02

### Asset naming overhaul + reconcile governance

- **New filename law (VFX-style).** The lowercase show code now **leads** every file the plugin writes to your working folder, and fields are **underscore-separated**: `sbw_project_context.md`, `sbw_art_bible.md`, `sbw_production.json`, `sbw_char_eli.md`, `sbw_char_eli_id_front.png`. (Previously: show code as a suffix, sometimes uppercase, hyphen-separated.) Underscores keep tokens from reading as a minus in a regex/expression. Ref ids in shot lines follow suit (`char_eli`); folders stay type-first (`assets/char/eli/`). The plugin's own internal files keep kebab-case (Claude Code requires it).
- **Legacy migration built in.** The `production` skill now **normalizes old-convention filenames on reconcile** — it renames suffix/uppercase/hyphen files (`project-context-SBW.md`, `char-sbw-eli.md`, `char-eli-id-front.png`) to the new `{show}_…` form and updates references, so existing projects self-heal.
- **Reconcile is plugin-governed, not a CLAUDE.md rule.** Every producing skill reconciles the manifest as a **close-out step**, and the `production-coordinator` + `guide-production` §7 now explicitly forbid writing standing workflow rules into a user's `CLAUDE.md` (and offer to remove one if found) — replacing agents improvising a "reconcile after every step" rule into project config.
- Updated the taxonomy (`guide-asset-reference.md` §9–10), the `production` skill's scan globs and schema, all producing skills, the coordinator, and the read-only dashboard (now matches `{show}_production.json`, still accepts legacy names).

## v1.0.4 - 2026-07-02

### Fix: model docs unreachable in the plugin; fal-hosted model defaults; audio as a cost choice

- **Bug: "no doc for uni-1" (and every per-model doc).** `shot-prompt` pointed at model docs via a bare `references/models/` **directory** link. In the assembled plugin the docs are flattened into the shared `context/` folder (no `models/` subdir), so that link resolved to the bare `context/` directory and the agent couldn't find a specific doc — even though the files ship in the package. Replaced it with **direct, resolvable links** to each model doc. Hardened `assemble.py` to fail on bare `context/` links and links to non-existent directories (validation previously skipped all directory links, which is how this shipped).
- **Model-selection defaults now lead with fal-hosted models.** Image: **Luma Uni-1 → Nano Banana / Nano Banana Pro → FLUX.2 → Seedream**. Video: **Seedance → Veo → Luma Ray → Kling**. Midjourney is flagged Discord-only (not on fal) and demoted to aesthetic-exploration-only, never a rendering default. Updated `shot-prompt`, `footage-transform`, and `model-currency-2026-06.md`.
- **Audio is now an explicit, opt-in cost choice.** Native-audio video models (Veo, Sora, Wan, Kling) roughly double per-clip cost, so audio defaults off and must be surfaced in the `FAL_AI_GET_PRICING` estimate before rendering. Noted in `footage-transform`, `model-currency`, and the `guide-execution` cost gate.

## v1.0.3 - 2026-07-02

### Fix: angle-bracket placeholders rejected as XML tags

- The plugin loader rejects any `<...>` tag in a SKILL.md. Converted every angle-bracket placeholder (`<show-code>`, `<place>`, `<id>`, sequence-template fields, etc.) to the project's existing `{...}` convention across all skills, and applied the same conversion to three agents (`cinematographer`, `first-ad`, `script-supervisor`) as a precaution.
- Extended the `assemble.py` gate to fail on any XML tag in a skill *or* agent body, alongside the 1024-char description check added in v1.0.2. Also audited every skill for name/dir match, kebab-case, and unexpected frontmatter keys — all clean.

## v1.0.2 - 2026-07-02

### Fix: skill description exceeded the loader's 1024-char cap

- Trimmed the `image-edit` skill's `description` frontmatter (1030 → 985 chars) by removing one redundant trigger example. The plugin loader rejects skill descriptions over 1024 characters, which blocked installation in v1.0.0/v1.0.1.
- Added a description-length check to `plugin/assemble.py` so any skill description over 1024 chars now fails the `VALIDATE` gate before release.

## v1.0.1 - 2026-07-02

### Repository rename

- Repo renamed to `claude-generative-wrangler`. Updated the marketplace-add slug, release/download URLs, and the plugin manifest `homepage`/`repository` to the new location. Added the Cowork desktop install path (Customize → Plugins → Add from a repository) alongside the Claude Code CLI commands. No changes to skills, agents, or context; the plugin name stays `generative-wrangler`.

## v1.0.0 - 2026-07-02

### Presentation layer - the make -> manage -> review loop is complete

- Added `dashboard/` - a self-contained, read-only production viewer. It renders a `production-{show}.json` as a board (assets, sequences and shots with thumbnails, budget, gaps) with a clean click-to-view lightbox. Loads via a File System Access folder picker, drag-drop, or a bundled sample; no build step, no server. An isolated sibling app, not part of the plugin package.
- Added `context/guide-presentation.md` - how the `production-coordinator` shows the board to the human: the dashboard, a contact sheet (ImageMagick), or an on-demand rendered board. Presentation is read-only; approvals still flow back through the manifest's `human` block.
- Wired presentation into the `production` skill and `production-coordinator` agent.
- **v1.0.0 milestone:** the v1.0 track (execution -> production office -> presentation) is complete. generative-wrangler now spans the full pipeline: define a project's look and world, build and store character/prop/set/style assets, plan coverage, write model-optimized prompts, actually render (single, batch, or video via Composio -> FAL), track the whole production in a manifest, and review it on a board.

## v0.11.0 - 2026-07-02

### New: Production office - coordinator + manifest (v1.0 track)

- Added the `production` skill and `production-coordinator` agent: build/reconcile `production-{show}.json` - the show's operational memory - and report where the production stands.
- The manifest is a derived index rebuilt from the working folder (asset specs + `.recipe` sidecars) plus a persisted `human` block (approvals / needs-retake / notes) that a rebuild merge-preserves, so it can always be rebuilt from the files and can't rot.
- Tracks assets (specced/built), generations (from recipes), cost rollups (by model/sequence), and gaps (specced-but-unrendered, orphans, missing refs, over-budget).
- Added `context/guide-production.md` (the production-office craft + manifest schema); sources: Eve Light Honthaner, The Complete Film Production Handbook.
- Second of the v1.0 track (execution -> production office -> presentation). Eleven skills / twelve agents.

## v0.10.0 - 2026-07-02

### New: Execution layer - closed render loop (v1.0 track)

- wrangler can now actually generate, not just prompt: `context/guide-execution.md` is the agent's playbook for driving the connected Composio -> FAL MCP (`FAL_AI_*` tools).
- Concurrent generation via fal's async queue - submit a set (coverage, turnaround views, variants, multiple clips) as a batch of `SUBMIT_ASYNC_JOB` calls, poll, and collect; video is always async.
- Each generative `model-*.md` gained a `fal_endpoint` for model routing; each generative skill gained a "generate" step pointing at `guide-execution.md`.
- Hard cost gate: confirm the `FAL_AI_GET_PRICING` estimate before any paid run; batches confirm the total and cap concurrency. Outputs save to the taxonomy path with a `.recipe` provenance sidecar.
- Agent-orchestrated (no render script, no key in the repo - auth is your Composio connection); needs an interactive session. First of the v1.0 track (execution -> production office -> presentation).

## v0.9.0 - 2026-07-01

### New: Asset integration & QC (art department, Phase 4 - roadmap complete)

- Added the `refs:` attachment notation (`context/guide-asset-reference.md` §10): each shot line names its assets by spec-stem (`char-{name}`, `prop-{name}`, `set-{name}`).
- `sequence-design` + `first-ad` now attach `refs:` to each shot line; `shot-prompt` + `cinematographer` consume them - loading each asset's anchor image and restating its identity block verbatim (identity = reference, change = prompt), inheriting the art-bible palette/CMF.
- `script-supervisor` now audits asset continuity: missing/wrong reference, costume/HMU/prop state drift, and location geometry mismatch, alongside its screen-direction/eyeline checks.
- Added per-model reference-count/strength caveats to `model-currency-2026-06.md` and a new end-to-end guide `docs/05-asset-pipeline.md`.
- Also in this release: the `model-image-luma-uni-1.md` doc (Luma Uni-1 unified image model). Sources: Pat P. Miller, Script Supervising and Film Continuity.

## v0.8.0 - 2026-07-01

### New: Production Designer / world bible (art department, Phase 3)

- Added the `art-direction` skill - a PD interview that produces `art-bible-{show}.md`: the show's global palette (named + hex), material/CMF lexicon, era/genre, a global style reference, and an index of every character/prop/set asset. Inherits the look from `project-context`; written to the user's working folder.
- Added the `production-designer` agent - the art-department counterpart to `director`: sets the world and delegates to casting, costume, makeup-hair, propmaster, and location-scout.
- Added the technical guide `context/guide-art-direction.md` and expanded the Production Design creative section in `reference-craft-artdept.md` (anchored to Ken Adam, Hannah Beachler, Patrice Vermette, and peers).
- Retrofitted the asset skills (`character-sheet`, `prop-turntable`, `location-pack`, `image-edit`) to inherit palette/CMF/style from `art-bible-{show}.md` when present.
- Wired into `skills/build.py` + `plugin/assemble.py`; docs updated to ten skills / eleven agents; crew flow now runs director -> production-designer -> art-dept sub-roles; sources added to `knowledge-base/Miscellaneous-Sources.md`.

## v0.7.0 - 2026-07-01

### New: Props & Locations (art department, Phase 2)

- Added the `prop-turntable` skill — build a persistent prop reference (hero anchor, orthographic ring, detail views, state variants/multiples) written to your working folder; uses `image-edit` as the derive engine.
- Added the `location-pack` skill — build a location/set reference (master establishing plate, coverage incl. the reverse angle, time-of-day/weather variants from locked geometry) with a continuity table.
- Added two art-department agents: `propmaster` (prop turntables) and `location-scout` (location packs).
- Added creative craft `context/reference-craft-artdept.md` (props + locations/sets artistry with real-master anchors) and technical guides `guide-prop-turntable.md` + `guide-location-pack.md`. 3D-assist (Blender) is noted as a deferred technique.
- Extended the asset naming taxonomy in `guide-asset-reference.md` §9 with prop facets (`hero`/`ortho`/`detail`/`360`), location facets (`plate`/`cov`/`tod`), and `top`/`bottom` views. Environment asset type is `set`.
- Wired into `skills/build.py` + `plugin/assemble.py`; docs updated to nine skills / ten agents; sources added to `knowledge-base/Miscellaneous-Sources.md`.

## v0.6.0 - 2026-06-30

### New: Character pipeline (art department, Phase 1)

- Added the `character-sheet` skill — build a persistent, re-attachable character reference (hero identity + descriptor block, turnaround/model sheet, wardrobe states, makeup/hair states) that downstream shots carry identity from. Anchor-then-fan-out; uses `image-edit` as the derive engine; output written to the user's working folder.
- Added three art-department agents: `casting-director` (identity), `costume-designer` (turnaround + wardrobe), `makeup-hair` (HMU states) — facets of one `char-{show}-{name}.md` asset.
- Added creative craft `context/reference-craft-character.md` (casting/costume/makeup-hair artistry with real-master anchors) and technical guides `guide-character-consistency.md` + `guide-turnaround-sheets.md`.
- Added the typed asset naming taxonomy to `guide-asset-reference.md` (`{type}-{show}-{name}.md`, `assets/{type}/{name}/`; codes char/prop/set/veh/cam/light/style/fx).
- Wired into `skills/build.py` + `plugin/assemble.py`; docs updated to seven skills; sources added to `knowledge-base/Miscellaneous-Sources.md`.

## v0.5.1 - 2026-06-30

### New skill: image-edit (image-to-image) — closes the i2i coverage gap

- Added `image-edit` skill — the still sibling of `footage-transform`: write/refine i2i prompts that preserve a real photo or generated still and change one thing (recolor/material, swap the background/crowd/world around a preserved subject, add or progress a wound, age a face, relight/regrade, remove/clean up, or compose locked references into a new scene). Trigger phrases include "change this image to X", "swap the crowd/background/wardrobe", "make these fans Moroccan instead of Dutch", "recolor this costume". Previously these requests had no home — `footage-transform` is v2v-only.
- Added foundation craft guide `context/guide-image-editing.md` (preserve-then-change, the four edit mechanisms, the denoise-strength dial, lighting integration, common edit types).
- Added foundation craft guide `context/guide-asset-reference.md` (anchor-then-fan-out, identity-block vs scene-block, reference-vs-LoRA decision gate, effective reference counts, multi-reference composition) — the shared spine for the upcoming art-department asset layer (v0.6+).
- Wired `image-edit` into `skills/build.py` and `plugin/assemble.py`; docs updated to six skills.
- Added `ROADMAP.md` (and staged stub crew/skills under `roadmap/`) planning the v0.6+ art department: Production Designer, casting, costume, makeup/hair, propmaster, location scout — character sheets, prop turntables, and location packs.

## v0.5.0 - 2026-06-30

### New skill: footage-transform (video-to-video)

- Added `footage-transform` skill — write/refine v2v prompts that preserve a real source clip and change one thing (add a VFX element, swap the environment, drop in a photoreal creature, sync a camera move to a spoken line, generate a transformed start frame).
- Added model-agnostic craft guide `context/guide-footage-transformation.md` (preserve-then-change, lighting/optics integration, timed moves with dual anchors, prepended-intro duration budget, first-frame workflow).
- Refreshed `context/model-video-seedance-pro.md` to Seedance 2.x: video-to-video `@source`/`@creature` input grammar, NON-IP guardrail, SFX-line convention, and 2.x input limits.
- Wired the new skill into `skills/build.py` and `plugin/assemble.py`; docs updated to five skills.

## v0.4.1 - 2026-06-30

### Distribution fix

- Ship a prebuilt `generative-cinema.plugin` at the repo root so Cowork users can install without building it.
- `plugin/assemble.py --package` now writes the artifact to the repo root (was a hardcoded session path).
- Un-ignored the committed root `generative-cinema.plugin` in `.gitignore`.
- README Cowork install now links the prebuilt file; maintenance note covers rebuilding/committing it on release.

## v0.2 - 2026-06-29

### Model currency refresh (June 2026)

- Added `context/model-currency-2026-06.md` as the single source of truth for current model versions.
- Added a currency callout to each of the 9 original model docs (FLUX.2, Nano Banana 2, Midjourney v8.1, Seedream 5, Seedance 2.5, Runway Gen-4.5, Veo 3.1, Luma Ray3.2).

### New model docs (12 models total)

- `model-video-kling-3.md` - Kling 3.0 (native 4K, fluid motion, Motion Control/Brush).
- `model-video-sora-2.md` - Sora 2 / 2 Pro (multi-shot storytelling, native dialogue; API sunset Sep 24 2026).
- `model-video-wan-2-6.md` - Wan 2.6 (open-weights, native audio/lip-sync, self-hostable).

### Cinematic craft guides (decision-support)

Heuristic-format guides (Decision / Use when / Because / Prompt translation / Watch-outs / Anchors):

- `guide-shot-selection.md`, `guide-lens-language.md`, `guide-continuity-rules.md`, `guide-sequence-construction.md` (P0).
- `guide-visual-structure.md`, `guide-color-story.md`, `guide-creative-approaches.md` (P1).
- `guide-ai-generation-strategy.md` (P2 - craft under current model limits).
- See `docs/history/CRAFT-EXPANSION-PROPOSAL.md` for the original roadmap.

### Agent skills (`skills/`)

Evolved the Custom GPT prompts into self-contained, progressively-disclosed skills:

- `project-context` (visual DNA interview), `sequence-design` (scene/coverage planning), `shot-prompt` (six-layer prompt generation), `model-docs` (document/refresh a model).
- `skills/build.py` syncs `context/` into each skill's bundled `references/` and packages installable `.skill` files to `skills/dist/` (git-ignored).
- Pipeline: project-context -> sequence-design -> shot-prompt -> prompts.

## v0.1 - 2025-11-07

### Initial Release

**9 Production-Ready Models:**
- Image Generation (4): FLUX.1 Pro, Gemini Flash, Midjourney v7, Seedream 4.0
- Video Generation (4): Seedance Pro, Runway Gen-4 Turbo, Google Veo 3.1, Luma Ray3
- Image Editing (1): FLUX.1 Kontext

**Show Context System:**
- Meta-generator for creating show context documents (20 essential questions)
- Template for manual creation
- Complete example: luxury automotive commercial

**Custom GPT Integration:**
- Meta-generator for system prompts
- Generic template for quick setup
- Complete deployment guide

**Documentation:**
- 9 model documentation files (consistent template structure)
- Setup guide for Custom GPT deployment
- Common workflow examples
- Model selection decision guide
- Universal prompting principles

**Process Tools:**
- Meta-generator for show contexts
- Meta-generator for system prompts
- Model documentation template
- All files follow `meta-generator-[TYPE]-[SUBTYPE].md` naming convention

**File Structure:**
- `context/` - 9 model documentation files
- `docs/` - Setup guides, workflows, model selection
- `prompts/` - 7 meta-generators and templates
