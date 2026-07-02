# Luma Uni-1 - Unified Reasoning Image Generation

> **Currency (Jul 2026):** Current API version is **Uni-1.1** (May 5, 2026 - full production API, two-endpoint REST interface, 9-reference support). See [`model-currency-2026-06.md`](model-currency-2026-06.md).

---

## Quick Reference

| Attribute | Value |
|---|---|
| **Current Version** | Uni-1 / Uni-1.1 API (May 2026) |
| **Model Type** | Text-to-Image, Image Editing (unified) |
| **Primary Use** | Reasoning-first image generation, multi-reference art direction, precise editing |
| **Max Resolution** | 2048px (longest edge; determined by aspect ratio) |
| **Max Duration** | N/A (image only) |
| **Speed** | ~31 seconds per image |
| **Cost** | `uni-1`: $0.04/image; `uni-1-max`: $0.10/image; reference images $0.003 each |
| **API Endpoint** | `docs.agents.lumalabs.ai` (Luma Agents REST API) |
| **Key Features** | Decoder-only autoregressive reasoning, 9 reference inputs, natural-language editing, 6000-char prompts |
| **fal endpoint** | `luma/agent/uni-1/v1/text-to-image` (edit: `luma/agent/uni-1/v1/edit`; max tier: `luma/agent/uni-1/v1/max`) |

---

## Overview

Luma Uni-1 (announced March 5, 2026; public API May 5, 2026 as Uni-1.1) is Luma's first Unified Intelligence model -- a decoder-only autoregressive transformer that represents text and image tokens in a single interleaved sequence. Unlike diffusion models, Uni-1 reasons through composition, constraints, and intent before rendering pixels.

The key architectural claim: learning to generate images makes the model measurably better at understanding them, and vice versa. Luma reports a 2.3-point Elo gain for the unified model over a variant trained for understanding only. The model ranks #1 on Human Preference Elo across Overall, Style & Editing, and Reference-Based Generation, and leads RISEBench on spatial reasoning.

**Version history:**
- March 5, 2026: Uni-1 announced alongside Luma Agents, web access only
- March 23, 2026: Public web access opens
- May 5, 2026: Uni-1.1 API launches (production REST, two endpoints, Python + JS/TS SDKs)

**Primary trade-off:** ~31 seconds per image versus ~3 seconds for FLUX.2 Pro. Reasoning depth comes at a latency cost.

---

## When to Use This Model

Uni-1 is the best choice when **prompt fidelity, reference-guided art direction, or complex spatial reasoning** are the priority.

- **Use Uni-1 for**: Multi-reference character/style consistency, precise instruction-following, complex spatial compositions, professional cinematographic framing, natural-language image editing.
- **Consider FLUX.2 Pro for**: Speed-critical pipelines (volume iterating 50+ images), maximum photorealism, open-source ComfyUI workflows.
- **Consider Midjourney v8 for**: Pure aesthetic quality and stylistic surprise without strict fidelity requirements, concept art, illustration.
- **Consider Gemini 3 Pro Image for**: Advanced reasoning with text rendering and high-fidelity typography tasks.

**Uni-1's Unique Strengths**: Only major production model built on autoregressive unified reasoning. Reference role system (up to 9 inputs with explicit roles) is the most structured multi-reference API available. Modify endpoint enables consistent natural-language editing without mask workflows.

---

## Prompting Structure

Uni-1 interprets intent, not just description. Prompts can be up to 6,000 characters. The model performs better with explicit compositional direction than with purely evocative language.

**Core Framework**: `[Subject + precise action] in [scene with specific spatial cues]. [Material/lighting properties]. [Camera/framing direction]. [Aesthetic register].`

```
+------------------------+----------------------+------------------------+--------------------+
| Subject & Action       | Scene & Spatial Cues | Material / Lighting    | Camera / Aesthetic |
+------------------------+----------------------+------------------------+--------------------+
| "A weathered           | "seated on a stool   | "harsh tungsten        | "tight 85mm        |
| ironworker"            | in a forge interior" | backlight, ash dust    | portrait, shallow  |
|                        |                      | catching light"        | DOF, editorial"    |
+------------------------+----------------------+------------------------+--------------------+
```

**Reference image syntax** (critical -- the model guesses when roles are omitted):

```
Use IMAGE1 ([brief description of the image]) as a [ROLE] reference.
```

Valid roles: `STYLE`, `CHARACTER`, `COMPOSITION`, `COLOR PALETTE`, `LIGHTING`, `TEXTURE`, `MOOD`

Example:
```
Use IMAGE1 (impressionist oil painting with loose brushwork, warm sunset palette)
as a STYLE reference. Create a portrait of an elderly man applying the color
palette and painterly texture.
```

---

## Parameters

### Uni-1.1 API - create_image endpoint

| Parameter | Type | Values | Default | Purpose |
|---|---|---|---|---|
| `prompt` | string | up to 6,000 chars | (required) | Describes desired image; supports role syntax for references |
| `model` | string | `"uni-1"`, `"uni-1-max"` | `"uni-1"` | Standard vs. max-quality tier |
| `aspect_ratio` | string | `"3:1"`, `"2:1"`, `"16:9"`, `"3:2"`, `"1:1"`, `"2:3"`, `"9:16"`, `"1:2"`, `"1:3"` | `"16:9"` | Output proportions; model derives resolution |
| `format` | string | `"jpg"`, `"png"`, `"webp"` | `"jpg"` | `png` for lossless/transparency; `webp` for modern compression |
| `references` | array | up to 9 image URLs | null | Reference images; each billed at $0.003 |
| `intent_weight` | float | 0.0-1.0 | [UNCONFIRMED - default unclear] | Controls depth of reasoning pass before generation; higher = more deliberate composition |
| `seed` | integer | any | random | Reproducibility; save seed + prompt as a reusable recipe |

### Uni-1.1 API - modify_image endpoint

| Parameter | Type | Values | Default | Purpose |
|---|---|---|---|---|
| `image_url` | string | URL | (required) | Source image to modify |
| `prompt` | string | up to 6,000 chars | (required) | Natural-language edit instruction |
| `model` | string | `"uni-1"`, `"uni-1-max"` | `"uni-1"` | Standard vs. max-quality tier |
| `format` | string | `"jpg"`, `"png"`, `"webp"` | `"jpg"` | Output format |

> **Note:** The `intent_weight` parameter appeared in developer documentation. Treat as likely-confirmed but verify against current API reference at `docs.agents.lumalabs.ai` before relying on it.

---

## Techniques

### Basic: Spatial Reasoning via Explicit Direction

Uni-1's reasoning engine responds to spatial specificity that diffusion models typically misfire on.

- **Generic**: `"A man and a woman shaking hands in an office."`
- **Better**: `"Two executives shaking hands across a glass boardroom table. The woman stands on the left in a navy suit; the man is on the right in charcoal gray. Their clasped hands are centered in frame. Large window behind them, overcast daylight, slight lens flare. Corporate editorial, 35mm."`
- **Result**: Consistent spatial relationships, correct hand geometry, matching framing.

### Intermediate: Multi-Reference Art Direction

Use explicit roles to layer control across references without confusion.

**Setup (3 references)**:
```
Use IMAGE1 (moody 1970s analog photography, heavy grain, warm amber tones,
low contrast) as a STYLE reference.
Use IMAGE2 (young woman with a shaved head and angular jaw) as a CHARACTER reference.
Use IMAGE3 (cramped Tokyo alleyway at night, neon signs, wet pavement) as a
COMPOSITION reference.

Generate: the character from IMAGE2 in the setting from IMAGE3, rendered in
the photographic aesthetic of IMAGE1.
```

This is Uni-1's clearest competitive advantage. Diffusion models conflate reference roles; the explicit syntax keeps them separated.

### Advanced: Iterative Editing Workflow with Seed Locking

Combine `create_image` and `modify_image` for controlled iteration.

**Step 1** - Establish a base with a fixed seed:
- Run `create_image` with a detailed prompt and explicit `seed` value
- Save the prompt + seed pair as your recipe

**Step 2** - Edit without losing identity:
- Pass the output URL to `modify_image` with targeted instructions
- `"Change the jacket from navy to rust orange, keep everything else identical"`
- The model applies edits without cascading changes to unmentioned elements

**Step 3** - Converge on final:
- Repeat `modify_image` passes for fine adjustments
- Switch to `uni-1-max` tier only for the final deliverable image

---

## Common Workflows

### 1. Reference-Guided Character Consistency Across Scenes

Maintain a character across multiple settings without per-image fine-tuning.

- **Reference setup**: One CHARACTER image per generation (the subject's face/features, with description)
- **Prompt pattern**: `"Use IMAGE1 ([character description]) as a CHARACTER reference. [New scene description]. Same character, same features, different environment."`
- **Output**: Consistent identity across scenes without LoRA or fine-tuning
- **Caveat**: Works best with clear frontal reference images; unusual angles degrade consistency

### 2. Art-Directed Style Transfer at Scale

Apply a visual language from references to new subjects.

- **Use case**: Brand-consistent imagery -- apply a defined visual style to product photography or editorial content
- **Approach**: STYLE + COLOR PALETTE reference (can be the same image); distinct subject prompt
- **Prompt**: `"Use IMAGE1 (Bauhaus geometric poster, primary colors, strong horizontal rule, sans-serif typography) as a STYLE reference and COLOR PALETTE reference. Generate a product shot of a glass water bottle. Apply the geometric aesthetic and limited palette. Clean white background, centered composition."`

### 3. Iterative Concept Development

Generate a strong base, then edit to final using natural-language modification.

1. `create_image`: Detailed directorial prompt, save seed
2. `modify_image`: Lighting edit - `"Shift from overcast daylight to late golden hour; add soft lens flare from upper left"`
3. `modify_image`: Color edit - `"Desaturate background 40%, keep subject colors intact"`
4. Upgrade to `uni-1-max` for final output

---

## Troubleshooting

| Issue | Cause | Solution |
|---|---|---|
| **References bleed into each other** | Role syntax omitted or unclear | Always specify explicit roles per image: `"as a STYLE reference"`, `"as a CHARACTER reference"`. Describe the reference image briefly in parentheses so the model parses it correctly. |
| **Generation time too slow for volume work** | Autoregressive architecture; ~31s is inherent | Use `uni-1` (not `uni-1-max`) for drafts. For high-volume iteration (50+ images), consider FLUX.2 Flash instead -- reasoning depth is not always the bottleneck. |
| **Complex text rendering fails** | Multilingual or dense layout can produce minor defects | Uni-1 handles English and Chinese well; other scripts and complex multi-line layouts are less reliable. Render final typography in post. |
| **Editing changes spread beyond the target area** | Prompt too broad or vague | Anchor instructions: name unchanged elements explicitly - `"keep the background, subject position, and clothing identical; only change [X]"`. |
| **`modify_image` loses character identity** | Source image is low-res or partially occluded | Use clean, well-lit source images. For character consistency across new scenes, prefer `create_image` with a CHARACTER reference over chained `modify_image` calls. |
| **Unexpected creative composition** | High `intent_weight` interprets ambiguous prompts liberally | Lower `intent_weight` for more literal execution; add explicit spatial anchors to the prompt. |

---

## Integration

- **API Example (Python - Luma AI SDK)**:
    ```python
    import lumaai
    import time

    client = lumaai.LumaAI()  # reads LUMAAI_API_KEY from environment

    # Text-to-image generation
    generation = client.generations.image.create(
        model="uni-1",
        prompt=(
            "Use IMAGE1 (a woman with short copper-red hair, sharp cheekbones, "
            "pale complexion) as a CHARACTER reference. "
            "She stands in a rain-soaked Tokyo alleyway at night, neon reflections "
            "on wet pavement, low-angle shot, cinematic, moody."
        ),
        aspect_ratio="9:16",
        references=[{"url": "https://example.com/character-ref.jpg"}]
    )

    # Poll for completion
    while generation.state != "completed":
        time.sleep(5)
        generation = client.generations.image.get(generation.id)

    print(generation.assets.image)
    ```

    > **Note:** SDK method names (`client.generations.image.create`) reflect the documented pattern but should be verified against the latest `lumaai` Python package on PyPI. The Luma Agents SDK (`lumaagents`) is a separate package used internally by Luma Agents workflows.

- **Natural-language editing**:
    ```python
    modified = client.generations.image.modify(
        image_url=generation.assets.image,
        prompt="Change her jacket from black to burnt orange. Keep everything else identical.",
        model="uni-1",
        format="png"
    )
    ```

- **Workflow Position**: Ideal for final hero frames and art-directed deliverables requiring reference consistency. Use `uni-1` tier for draft iteration, `uni-1-max` for finals. Pair with Ray3.2 or Seedance 2.5 for downstream video generation using Uni-1 outputs as keyframes.
- **Complementary Tools**: Uni-1 outputs work as `image_url` inputs to Luma Ray3.2 (I2V). FLUX.2 is faster for volume drafting. Midjourney v8 for aesthetic exploration where fidelity is secondary.

---

## References

- Luma AI. (2026, March 5). *Luma Launches Creative AI Agents Powered by Unified Intelligence Models*. TechCrunch. https://techcrunch.com/2026/03/05/exclusive-luma-launches-creative-ai-agents-powered-by-its-new-unified-intelligence-models/
- Luma AI. (2026). *UNI-1 - Less Artificial. More Intelligent.* https://lumalabs.ai/uni-1
- Luma AI. (2026). *UNI-1 Tech Specs*. https://lumalabs.ai/uni-1/tech-specs
- Luma AI. (2026, May 5). *Introducing the Uni-1.1 API*. https://lumalabs.ai/news/uni-1-1-api
- Luma AI. (2026). *Uni-1 Field Guide*. https://lumalabs.ai/learning-center/articles/luma-uni-1-field-guide
- Luma AI. (2026). *Luma Agents Quickstart*. https://docs.agents.lumalabs.ai/
- MarkTechPost. (2026, March 23). *Luma Labs Launches Uni-1: The Autoregressive Transformer Model*. https://www.marktechpost.com/2026/03/23/luma-labs-launches-uni-1-the-autoregressive-transformer-model-that-reasons-through-intentions-before-generating-images/
- VentureBeat. (2026). *Luma AI Launches Uni-1, a Model That Outscores Google and OpenAI at 30% Lower Cost*. https://venturebeat.com/technology/luma-ai-launches-uni-1-a-model-that-outscores-google-and-openai-while
