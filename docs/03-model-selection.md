# Model Selection Decision Guide

Choose the right generative AI model for your task. This guide provides decision trees and comparison data.

**PREREQUISITE**: Before selecting models, create a show context document (`prompts/meta-generator-show-context.md`). This defines your visual requirements and will guide model selection.

---

## Quick Decision Tree

### Image Generation

```
Need final asset with text/labels?
├─ YES → Gemini Flash
└─ NO → Continue

Need maximum resolution (4K+)?
├─ YES → Seedream 4.0
└─ NO → Continue

Need artistic/stylized output?
├─ YES → Midjourney v7
└─ NO → Continue

Need fast, clean, photorealistic?
└─ YES → FLUX.1 Pro
```

### Video Generation

```
Need synchronized audio (dialogue/SFX)?
├─ YES → Veo 3.1
└─ NO → Continue

Need HDR output for VFX compositing?
├─ YES → Luma Ray3
└─ NO → Continue

Need fastest iteration (rapid prototyping)?
├─ YES → Runway Gen-4 (30s generation)
└─ NO → Continue

Need multi-shot narrative sequence?
└─ YES → Seedance Pro
```

### Image Editing

```
Need conversational back-and-forth editing?
├─ YES → Gemini Flash
└─ NO → Continue

Need character consistency across scenes?
├─ YES → FLUX.1 Kontext
└─ NO → Continue

Need precise masked edits?
└─ YES → FLUX.1 Kontext
```

---

## Detailed Comparison

### Image Models

| Feature | FLUX.1 Pro | Gemini Flash | Midjourney v7 | Seedream 4.0 |
|---------|------------|--------------|---------------|--------------|
| **Max Resolution** | 2048x2048 | High (varies) | 4096x4096* | 4096x4096 |
| **Speed** | ~10s (4MP) | Fast | Medium | Medium |
| **Cost** | ~$0.06/image | Low | Subscription | Medium |
| **Text Rendering** | Good | **Excellent** | Poor | Good |
| **Photorealism** | **Excellent** | Very Good | Good | **Excellent** |
| **Artistic Style** | Good | Good | **Excellent** | Good |
| **Prompt Adherence** | Very Good | **Excellent** | Good | **Excellent** |
| **Best For** | Commercial assets | Text + images | Concept art | Print quality |
| **API Access** | ✅ Yes | ✅ Yes | Enterprise only | ✅ Yes (BytePlus) |

*Via upscalers

### Video Models

| Feature | Seedance Pro | Runway Gen-4 | Veo 3.1 | Luma Ray3 |
|---------|-------------|--------------|---------|-----------|
| **Max Resolution** | 1080p | 720p (4K upscale) | 1080p | 4K (HiFi) |
| **Max Duration** | 10s | 10s | 8s (+extend) | 10s |
| **Generation Speed** | Medium | **Fast (~30s)** | Medium | 5x (Draft) |
| **Multi-Shot** | ✅ **Excellent** | ❌ No | ❌ No | ❌ No |
| **Camera Control** | Via prompt | Via prompt | Via prompt | Via prompt |
| **Character Consistency** | Good | ✅ **Excellent** | Good | Good |
| **Audio Generation** | ❌ No | ❌ No | ✅ **Native** | ❌ No |
| **HDR Output** | ❌ No | ❌ No | ❌ No | ✅ **16-bit** |
| **Physics Simulation** | Good | Good | Good | ✅ **Reasoning** |
| **API Access** | ✅ Yes | ✅ Yes | ✅ Yes | ⚠️ Ray 2 only |
| **Cost** | Medium | $0.05/sec | Varies | Varies |
| **Best For** | Narratives | Rapid prototyping | Dialogue scenes | VFX elements |

### Editing Models

| Feature | FLUX.1 Kontext | Gemini Flash |
|---------|----------------|--------------|
| **Iterative Editing** | ✅ Excellent | ✅ Good |
| **Masked Editing** | ✅ Yes | ❌ No |
| **Character Consistency** | ✅ **Excellent** | Good |
| **Style Transfer** | ✅ Yes | ✅ Yes |
| **Multi-Image Composition** | Basic | ✅ **Excellent** |
| **Best For** | Precision edits | Conversational iteration |

---

## Use Case Matrix

### By Industry/Project Type

| Industry | Primary Model | Workflow |
|----------|---------------|----------|
| **Advertising** | FLUX.1 Pro | Fast product shots + Kontext for variations |
| **Film/TV Pre-vis** | Midjourney v7 + Runway Gen-4 | Fast concept frames → rapid iteration |
| **Architecture** | Seedream 4.0 | 4K renders for client presentations |
| **Social Media** | Midjourney v7 | Artistic style, character consistency |
| **E-commerce** | FLUX.1 Pro | Clean product photography |
| **VFX/Film Production** | Luma Ray3 | HDR elements for compositing |
| **Marketing Videos** | Veo 3.1 | Video with voiceover/dialogue |
| **Game Development** | Midjourney v7 | Concept art, character design |
| **Print/Publishing** | Seedream 4.0 | Maximum resolution requirements |
| **Education** | Gemini Flash | Diagrams, labels, illustrations |

### By Asset Type

| Asset Type | Model Choice | Rationale |
|------------|--------------|-----------|
| **Character Portrait** | Midjourney v7 | Best artistic quality + Omni Reference |
| **Product on White** | FLUX.1 Pro | Clean, fast, professional |
| **Infographic** | Gemini Flash | Superior text rendering |
| **Landscape/Environment** | Seedream 4.0 or Midjourney v7 | Resolution vs artistic style |
| **Logo Design** | Gemini Flash | Text handling |
| **Texture/Pattern** | Midjourney v7 (--tile) | Seamless patterns |
| **Video Storyboard** | Runway Gen-4 or Seedance Pro | Fast iteration vs multi-shot |
| **Architectural Render** | FLUX.1 Pro (ultra) or Seedream 4.0 | Photorealism + resolution |
| **VFX Elements** | Luma Ray3 | HDR, advanced physics |
| **Dialogue/Narration Video** | Veo 3.1 | Synchronized audio |

### By Constraint

| Constraint | Recommended Model | Notes |
|------------|-------------------|-------|
| **Budget: Low** | Gemini Flash or FLUX.1 Dev | Free tier or lower cost |
| **Time: Urgent** | FLUX.1 Pro | Fastest generation |
| **Quality: Maximum** | Seedream 4.0 | Native 4K, high detail |
| **Control: Precise** | FLUX.1 Kontext | Masked editing, preservation |
| **Consistency: Critical (image)** | Midjourney v7 + Kontext | Omni Reference + editing |
| **Consistency: Critical (video)** | Runway Gen-4 | Character locking |
| **Text: Required** | Gemini Flash | Best text rendering |
| **Audio: Required** | Veo 3.1 | Only model with native audio |
| **HDR: Required** | Luma Ray3 | Only 16-bit HDR output |

---

## Decision Factors

### When Resolution Matters

**Need 4K+ for print?**
- Use: Seedream 4.0 (native 4K)
- Alternative: FLUX.1 Pro ultra → upscaler

**Web/social only (1080p)?**
- Use: FLUX.1 Pro or Midjourney v7
- Faster, more cost-effective

### When Speed Matters

**Fastest to final (image):**
1. FLUX.1 Pro (~10s for 4MP)
2. Gemini Flash (fast)
3. Midjourney v7 (medium)
4. Seedream 4.0 (medium)

**Fastest to final (video):**
1. Runway Gen-4 (~30s for 10s video)
2. Luma Ray3 Draft Mode (~20s)
3. Seedance Pro (medium)
4. Veo 3.1 (medium)

### When Style Matters

**Photorealistic:**
1. FLUX.1 Pro (raw mode)
2. Seedream 4.0
3. Gemini Flash

**Artistic/Stylized:**
1. Midjourney v7 (highest stylize)
2. FLUX.1 Pro (style prompts)
3. Seedream 4.0

**Specific Art Style:**
- Midjourney v7 (best at mimicking styles)
- Use style references in prompt

### When Text Matters

**Text overlays, labels, signage:**
- **Primary**: Gemini Flash (best text rendering)
- **Backup**: FLUX.1 Pro (good but not perfect)
- **Avoid**: Midjourney v7 (poor text handling)

### When Consistency Matters

**Same character across multiple images:**
1. Generate base with Midjourney v7
2. Use Omni Reference for variations
3. Refine with FLUX.1 Kontext
4. Use --seed parameter (Midjourney)

**Same style across asset series:**
1. Generate style reference
2. Use --seed (Midjourney) or reference image
3. Document exact prompts
4. Iterate one variable at a time

---

## Cost Optimization

### By Budget Tier

**Shoestring ($0-50/month):**
- Use: Gemini Flash (free tier), FLUX.1 Dev (open weights)
- Strategy: Fewer iterations, accept good-enough results

**Standard ($50-500/month):**
- Use: FLUX.1 Pro for bulk, Midjourney subscription
- Strategy: Draft in cheaper model, finalize in premium

**Premium ($500+/month):**
- Use: All models, optimize for quality
- Strategy: Right tool for each job, less iteration needed

### Cost per Asset Estimates

| Model | Single Image | 100 Images | Notes |
|-------|-------------|------------|-------|
| FLUX.1 Pro | $0.06 | $6 | 4MP ultra mode |
| Gemini Flash | Low/Free | $2-5 | API pricing varies |
| Midjourney v7 | $10-60/mo | Unlimited* | Subscription tiers |
| Seedream 4.0 | $0.10-0.15 | $10-15 | 4K native |

*Subject to fair use limits

---

## Common Selection Mistakes

**Mistake 1**: Using Midjourney for product photography
- **Issue**: Too artistic, inconsistent
- **Fix**: Use FLUX.1 Pro for clean commercial shots

**Mistake 2**: Using FLUX for text-heavy designs
- **Issue**: Poor text rendering
- **Fix**: Use Gemini Flash for anything with text

**Mistake 3**: Not using reference images for consistency
- **Issue**: Characters/styles vary wildly
- **Fix**: Always use image-to-image or Omni Reference

**Mistake 4**: Choosing based on hype, not needs
- **Issue**: Overpaying for features you don't need
- **Fix**: Match tool to specific requirements

**Mistake 5**: Not testing before committing to workflow
- **Issue**: Discover limitations mid-project
- **Fix**: Run small test before full production

---

## Testing Protocol

Before committing to a model for a project:

1. **Define success criteria**
   - Resolution requirements
   - Style/aesthetic
   - Text needs
   - Budget constraints
   - Turnaround time

2. **Run 5-10 test prompts** in top 2 candidate models

3. **Compare results** on:
   - Quality match to vision
   - Consistency across iterations
   - Time per generation
   - Cost per acceptable result
   - Ease of iteration

4. **Document findings** for future projects

---

## Getting Help

Can't decide? Ask the Custom GPT:

"I need to create [describe asset] for [use case].
Requirements: [resolution, style, budget, timeline].
Which model should I use?"

The GPT will:
1. Identify your constraints
2. Recommend primary and alternative models
3. Suggest a workflow
4. Provide starting prompts
