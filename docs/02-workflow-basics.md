# Common Generative AI Workflows

Production workflows for different asset types. Each workflow shows model selection and parameter guidance.

**IMPORTANT**: Before starting any workflow, create a show context document using `prompts/meta-generator-show-context.md`. This defines your visual language and ensures all prompts maintain consistency.

---

## Workflow 1: Static Character Concept Art

**Goal**: Create a consistent character across multiple poses/scenes

### Process

**Step 1: Initial Concept** (Midjourney v7)
```
Prompt: "Portrait of a cyberpunk hacker, neon-lit face, undercut hairstyle,
leather jacket with glowing circuitry, determined expression, cinematic lighting,
shot on 85mm lens, shallow depth of field --ar 4:5 --s 400 --v 7"
```

**Step 2: Variations** (Midjourney v7 with Omni Reference)
```
Prompt: "[URL of initial image] The same character, now in a full body shot,
standing in a rain-soaked alley, neon signs reflecting in puddles --ar 4:5 --s 400 --v 7"
```

**Step 3: Refinement** (FLUX.1 Kontext)
```
Prompt: "Change the jacket color to dark blue while preserving all facial features,
hairstyle, and expression exactly as shown"
```

**Step 4: High-Res Export** (Seedream 4.0)
- Use final approved image as reference
- Generate 4K version for print/final delivery

---

## Workflow 2: Product Photography

**Goal**: Create professional product shots with variations

### Process

**Step 1: Base Image** (FLUX.1 Pro - Ultra Mode)
```python
{
  "prompt": "Professional product shot of a sleek smartwatch on white background,
  studio softbox lighting, 85mm lens, f/2.8, clean shadows, photorealistic",
  "mode": "ultra",
  "resolution": "2048x2048"
}
```

**Step 2: Background Variations** (FLUX.1 Kontext)
```
Prompt 1: "Replace the white background with a dark wooden desk surface,
maintaining the watch position and lighting"

Prompt 2: "Change background to outdoor setting, blurred nature scene,
golden hour lighting, preserve product sharpness"
```

**Step 3: Color Variants** (FLUX.1 Kontext)
```
Prompt: "Change the watch band color to midnight blue while keeping all other
aspects identical"
```

---

## Workflow 3: Cinematic Video Sequence

**Goal**: Create a short narrative video clip

### Process

**Step 1: Keyframe Generation** (Midjourney v7)
```
Prompt: "Cinematic film still, wide shot of a lone astronaut standing on Mars,
red rocky landscape, two moons visible in pink sky, harsh directional lighting,
anamorphic lens flare, sense of isolation --ar 16:9 --s 400 --v 7"
```

**Step 2: Video Animation** (Seedance Pro)
```
Prompt: "The astronaut slowly turns their head to the right, looking towards
the horizon. Shot switch. Close-up of their helmet visor, reflecting a distant
light source. Shot switch. The camera slowly pushes in on the astronaut as they
raise their hand to shield their eyes. Cinematic, 1970s sci-fi aesthetic.
--dur 10 --rs 1080p --cf false"
```

**Step 3: Additional Clips** (Seedance Pro)
```
Prompt: "Camera positioned behind astronaut, over-the-shoulder shot looking
at the vast Martian landscape. A faint pulsing light appears on the horizon.
The astronaut takes one hesitant step forward. Slow zoom on the distant light.
--dur 5 --rs 1080p --cf false"
```

**Step 4: Post-Production**
- Concatenate clips in editing software
- Add sound design
- Color grade for consistency

---

## Workflow 4: Architectural Visualization

**Goal**: High-resolution architectural renders

### Process

**Step 1: Initial Render** (FLUX.1 Pro - Ultra Mode)
```
Prompt: "Ultra-realistic architectural render of modern glass house in forest,
evening light filtering through trees, interior lights warm and inviting,
reflections on glass surfaces, 4K photorealistic, architectural photography style"
```

**Step 2: Lighting Variations** (FLUX.1 Kontext)
```
Prompt 1: "Change to daytime lighting, bright sun casting shadows through trees,
preserve architecture exactly"

Prompt 2: "Night scene, stars visible through glass ceiling, interior warmly lit,
dramatic contrast"
```

**Step 3: 4K Final** (Seedream 4.0)
```
Prompt: "4K hyper-detailed architectural visualization of [describe approved design],
photorealistic materials, professional architectural photography"
```

---

## Workflow 5: Social Media Content Series

**Goal**: Fast iteration of consistent visual style

### Process

**Step 1: Style Reference** (Midjourney v7)
```
Prompt: "Flat design illustration of coffee cup on desk, warm color palette,
minimal shadows, vector style --ar 1:1 --s 200 --v 7"
```

**Step 2: Variations** (Midjourney v7)
```
Use --seed from first image to maintain style consistency

Prompt 1: "[Previous seed] Flat design illustration of laptop on desk,
same style --ar 1:1 --s 200 --v 7"

Prompt 2: "[Previous seed] Flat design illustration of notebook and pen,
same style --ar 1:1 --s 200 --v 7"
```

**Step 3: Rapid Edits** (FLUX.1 Kontext or Gemini Flash)
- Quick color adjustments
- Element additions/removals
- Text overlays (Gemini Flash better for text)

---

## Workflow 6: Animated Logo Reveal

**Goal**: Static logo to animated reveal

### Process

**Step 1: Logo Design** (FLUX.1 Pro or Gemini Flash)
```
Gemini Flash (better for text):
"Create a modern tech company logo with the text 'NOVA TECH' in clean sans-serif
font, geometric hexagon symbol, dark blue and silver color scheme, professional,
centered on white background"
```

**Step 2: Animation** (Seedance Pro)
```
[Using logo image as input]

Prompt: "The logo elements smoothly fade in from transparency. First the hexagon
materializes with a gentle glow, then the text 'NOVA TECH' appears letter by letter
from left to right. Subtle shimmer effect on the final composition. Modern, corporate
style. --dur 5 --rs 1080p"
```

---

## Workflow 7: Rapid Video Prototyping (Runway Gen-4)

**Goal**: Quickly iterate on video concepts for approval

### Process

**Step 1: Generate Test Concepts** (Runway Gen-4 Draft)
```python
{
  "model": "gen4_turbo",
  "prompt": "Close-up dolly zoom of detective discovering clue in dark alley, rain falling, neon signs reflecting. Cinematic film noir.",
  "duration_seconds": 5,
  "motion_strength": 6,
  "seed": 42
}
```

**Step 2: Iterate with Same Seed**
```python
# Keep seed=42, modify prompt
{
  "prompt": "Close-up dolly zoom of detective discovering clue in dark alley, rain falling, neon signs reflecting, lightning flash. Cinematic film noir.",
  "seed": 42
}
```

**Step 3: Final Version at Full Length**
```python
{
  "prompt": "[Best version from iterations]",
  "duration_seconds": 10,
  "seed": 42
}
```

**Step 4: Upscale (if needed)**
- Use Runway's upscaler for 4K delivery

---

## Workflow 8: Dialogue Scene with Audio (Veo 3.1)

**Goal**: Create video with synchronized dialogue and sound effects

### Process

**Step 1: Generate Keyframe** (FLUX.1 Pro)
```
Prompt: "Close-up of woman's face in dimly lit room, serious expression, looking directly at camera. Cinematic lighting, film noir style, shallow depth of field."
```

**Step 2: Animate with Dialogue** (Veo 3.1)
```python
{
  "prompt": "The woman says in a firm voice, 'We need to leave. Now.' Background sounds of distant sirens. Subtle head movement, eyes show concern. Cinematic, dramatic lighting.",
  "reference_images": ["[keyframe from Step 1]"],
  "duration_seconds": 8,
  "include_audio": true
}
```

**Step 3: Extend Scene** (Veo 3.1 Extend)
```
In Veo Flow UI, use Extend feature:
"She stands up quickly, chair scraping on floor. Footsteps as she walks toward door. Sirens growing louder."
```

**Step 4: Post Production**
- Export video+audio
- Mix audio levels
- Color grade for final look

---

## Workflow 9: HDR VFX Element (Luma Ray3)

**Goal**: Create professional-grade HDR element for compositing

### Process

**Step 1: Draft Iterations** (Luma Ray3 Draft Mode)
Generate 5-10 variations quickly:
- Draft 1: `"Explosion with fire and smoke"`
- Draft 2: `"Explosion with fire, volumetric smoke, debris"`
- Draft 3: `"Massive explosion with intense fire, thick volumetric smoke, concrete debris flying outward. Slow motion."`
- Draft 4: `"Massive explosion with intense fire, thick volumetric smoke, concrete debris flying outward, shockwave visible. Ultra slow motion, cinematic."`

**Step 2: Select Best Draft**
- Choose draft with best composition and motion

**Step 3: HiFi 4K HDR Upscale** (Web UI)
- Upscale selected draft to 4K
- Enable 16-bit HDR output
- Export as EXR sequence

**Step 4: Composite** (Nuke/After Effects)
```
Import EXR sequence
Composite over live action
Color grade with HDR tools
Add additional particle effects if needed
```

---

## Model Selection Quick Reference

| Asset Type | Primary Model | Alternative | Final Output |
|------------|---------------|-------------|--------------|
| Character concept | Midjourney v7 | FLUX.1 Pro | Seedream 4.0 (4K) |
| Product photo | FLUX.1 Pro | Seedream 4.0 | FLUX.1 Pro (ultra) |
| Video narrative | Seedance Pro | - | Editing software |
| Architecture | FLUX.1 Pro | Seedream 4.0 | Seedream 4.0 (4K) |
| Social graphics | Midjourney v7 | FLUX.1 Pro | Kontext (edits) |
| Logo/text | Gemini Flash | FLUX.1 Pro | As generated |

---

## Time Estimates

| Workflow | Steps | Est. Time | Iterations |
|----------|-------|-----------|------------|
| Character concept | 4 | 20-30 min | 3-5 per step |
| Product photo | 3 | 15-20 min | 2-3 per step |
| Video sequence (Seedance) | 4 | 45-60 min | 2-4 per clip |
| Architecture | 3 | 25-35 min | 3-4 per step |
| Social series | 3 | 30-40 min | 4-6 images |
| Logo animation | 2 | 15-20 min | 2-3 iterations |
| Rapid video prototyping (Runway) | 4 | 15-25 min | 5-10 iterations |
| Dialogue scene (Veo) | 4 | 30-40 min | 2-3 takes |
| HDR VFX element (Luma) | 4 | 40-60 min | 5-10 drafts |

Times assume familiarity with tools and prompting techniques.

---

## Best Practices

1. **Create show context FIRST** - Define visual language before generating (use `prompts/meta-generator-show-context.md`)
2. **Use standard prompt prefix** - Start every prompt with prefix from your show context
3. **Always save prompts** - Document what works for reuse
4. **Use seeds for consistency** - When model supports it (Midjourney)
5. **Iterate one variable** - Change lighting OR composition, not both
6. **Reference previous work** - Image-to-image for consistency
7. **Archive raw outputs** - Before edits, in case of rollback
8. **Test on small resolution** - Verify concept before expensive 4K renders

---

## Common Pitfalls

**Pitfall 1**: Changing too many parameters at once
- **Solution**: Iterate one element per generation

**Pitfall 2**: Not documenting successful prompts
- **Solution**: Keep a prompt library organized by project

**Pitfall 3**: Starting to prompt without a show context
- **Solution**: Always create show context first to define visual language

**Pitfall 4**: Using wrong model for the task
- **Solution**: Consult model selection guide (README.md) and show context recommendations

**Pitfall 5**: Skipping reference images for consistency
- **Solution**: Always use image-to-image for character/style consistency

**Pitfall 6**: Not accounting for model limitations
- **Solution**: Review model docs before starting (Seedance: no negative prompts, etc.)
