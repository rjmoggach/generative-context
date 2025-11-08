# Cinematic Prompt Generation

A comprehensive, film grammar-based framework for generating professional AI video prompts. This toolset integrates classical cinematic principles from authoritative film grammar texts with modern AI video generation techniques.

**Designed for dual use:**
- **Manual prompting** - Reference guide for artists and cinematographers
- **Generative app development** - Structured data for building prompt generation tools

---

## Contents

1. **film_grammar.md** - Comprehensive film grammar principles from Arijon and Spottiswoode
2. **six_layer_framework.md** - Flexible six-layer framework with multiple prompt templates
3. **prompt_generation.json** - Structured JSON with CUSTOM/SELECT fields for both manual and programmatic use
4. **README.md** - This file

---

## Quick Start

### For Manual Prompting

1. **Start simple**: Use layers 1-2 only (Subject + Framing)
   - Example: "Close Up of a barista pouring latte art"

2. **Add complexity as needed**: Incorporate layers 3-4 (Movement + Lighting)
   - Example: "Medium Shot of a cyclist racing through a forest trail, tracking shot following from the side. Golden hour lighting, dappled sunlight through trees."

3. **Use all 6 layers for hero shots**: Maximum control for final deliverables
   - See `six_layer_framework.md` for 6 different template examples

### For App Developers

1. **CUSTOM fields** → Text input forms (subject, action, setting, narrative_intent)
2. **SELECT fields** → Dropdowns/checkboxes (shot distances, camera angles, lighting styles, etc.)
3. **REQUIRED/OPTIONAL** → Clearly marked for validation
4. **Model-specific templates** → Reference `model_specifics` section for platform optimization

See `prompt_generation.json` for complete structure.

---

## The Six-Layer Framework (v2.0)

**CRITICAL**: This framework is **descriptive, not prescriptive**. You do NOT need to use all six layers for every prompt.

### Layer 1: Subject, Action, and Narrative Intent

**What you provide (CUSTOM):**
- Subject: Who/what is in the shot
- Action: What is happening
- Setting: Where this takes place
- Narrative Intent: Emotional tone (optional)

**What you can select:**
- Dialogue staging techniques (if applicable)

### Layer 2: Shot Composition and Framing

**Select from:**
- 9 shot distances (BCU to ELS)
- 6 camera angles (eye level to worm's eye)
- Composition principles (rule of thirds, symmetry, etc.)
- Framing precision (cutting heights, headroom)

### Layer 3: Camera Dynamics and Movement

**Select from:**
- 10 basic movements (static, tracking, dolly, crane, etc.)
- 5 combination movements (dolly zoom, arc shot, etc.)
- Focus manipulation (rack focus, deep focus, shallow focus)
- Movement quality (slow/deliberate, chaotic, smooth)

### Layer 4: Lighting, Color, and Atmosphere

**Select from:**
- 12 lighting styles (High Key, Low Key, Rembrandt, etc.)
- 9 time of day options (golden hour, blue hour, etc.)
- 12 color theory approaches (monochromatic, teal/orange, etc.)
- 19 atmospheric effects (fog, rain, film grain, etc.)

### Layer 5: Technical Specifications and Lens Choice

**Select from:**
- 12 lens types (14mm fisheye to anamorphic)
- 11 optical characteristics (shallow DOF, bokeh, flares)
- 15 film stock formats (35mm, IMAX, Arri Alexa, etc.)
- 10 resolution/quality markers

### Layer 6: Editing, Pacing, and Transitions

**Select from (multi-shot sequences only):**
- 10 pacing/rhythm options (slow motion, time lapse, etc.)
- 12 editing techniques (match cut, jump cut, montage)
- 14 transitions (dissolve, fade, L-cut, etc.)
- 7 montage theory approaches (rhythmical, implicational, etc.)

---

## Framework Flexibility

### Complexity Levels

**Minimal (Layers 1-2)**: Quick tests, simple shots
- "A chef preparing sushi, Medium Close Up"

**Moderate (Layers 1-4)**: 80% of production work
- "Medium Shot of a cyclist racing through a forest trail, tracking shot following from the side. Golden hour lighting, dappled sunlight through trees."

**Complex (All 6 Layers)**: Hero shots, final deliverables
- See `six_layer_framework.md` Template 4

### Model-Specific Recommendations

| Model | Essential Layers | Use Case |
|-------|-----------------|----------|
| **Kling 2.5** | 1, 2, 3 | Athletic movement, character animation |
| **Sora 2 Pro** | 1, 2, 6 | Multi-shot storytelling, sequences |
| **Veo 3.1** | All 6 | Premium production, exact control |
| **Wan 2.5** | 1, 2, 4 | Dialogue, lip sync, character narratives |

---

## Style Reference Stacking

Combine visual references from multiple films for unique aesthetics. The JSON includes 27 comprehensive cinematographic references:

**Classic Masters:**
- Kubrick: 2001, The Shining, Barry Lyndon
- Lawrence of Arabia - epic 70mm grandeur

**Auteur Precision:**
- Fincher: Seven, Zodiac, Gone Girl, The Social Network
- Gattaca, Inception

**Natural Realism:**
- Roma, The Revenant, Moonlight, Nomadland, Children of Men

**Glossy Commercial:**
- Top Gun Maverick, Mission Impossible Fallout

**Stylized:**
- Blade Runner 2049, Drive, Mad Max Fury Road, The Grand Budapest Hotel

**Music Videos (Romanek):**
- Johnny Cash 'Hurt', Nine Inch Nails 'Closer', Jay-Z '99 Problems'

**Example Usage:**
```
"Medium Shot of a detective in rain-soaked streets, aesthetic combining Seven (Fincher) color grading + Blade Runner 2049 atmosphere + Children of Men handheld movement, using 35mm lens with shallow focus."
```

---

## Film Grammar Reference

### Shot Distances (Arijon)

| Shot Type | Abbreviation | Description |
|---|---|---|
| Big Close Up | BCU | Head only |
| Close Up | CU | Head and shoulders |
| Close Shot | CS | Head, shoulders, chest |
| Medium Close Up | MCU | Chest to head |
| Medium Shot | MS | Waist and up |
| Medium Full Shot | MFS | Knees and up |
| Full Shot | FS | Entire figure with feet |
| Long Shot | LS | Figure with ample background |
| Extreme Long Shot | ELS | Vast landscape, small or absent figure |

### Lighting Styles

| Style | Description | Use Case |
|---|---|---|
| High Key | Bright, even, low contrast | Comedy, commercials, optimism |
| Low Key | Dark, high contrast, dramatic shadows | Noir, mystery, drama |
| Chiaroscuro | Extreme light/dark contrast | Artistic, dramatic |
| Rembrandt | Triangle of light on cheek | Portraits, character studies |
| Butterfly | Light above and in front | Beauty, glamour |
| Three-Point | Key, fill, back lights | Standard professional setup |
| Natural | Ambient, realistic | Documentary, realism |
| Practical | Visible light sources in scene | Motivated lighting |

### Montage Types (Spottiswoode)

| Type | Description | Use Case |
|---|---|---|
| Primary | Conceptual effect from successive shots | Basic narrative construction |
| Rhythmical | Emotional effect from editing tempo | Building tension or energy |
| Implicational | Symbolic meaning between shots | Complex thematic development |
| Intellectual | Combine shots to form new idea | Metaphorical storytelling |

---

## Integration with Main Context Library

This cinematic framework complements the main generative AI context library:

- **FLUX.1 Pro**: Use layers 1-2-4 (subject, framing, lighting)
- **Midjourney v7**: Apply shot distances, camera angles, film references
- **Seedance Pro**: Leverage layer 6 for multi-shot narrative sequences
- **Runway Gen-4 Turbo**: Focus on layers 1-3 (subject, framing, movement)
- **Veo 3.1**: Use complete JSON structure with all 6 layers
- **Luma Ray3**: Emphasize layer 5 (technical specs for HDR/4K)

---

## Workflow Recommendations

### Manual Prompting Process

1. **Start with CUSTOM fields** - Define your subject, action, setting
2. **SELECT shot distance and angle** from Layer 2
3. **Add camera movement** from Layer 3 if needed
4. **SELECT lighting and atmosphere** from Layer 4
5. **Add technical specs** from Layer 5 for final shots
6. **Use Layer 6** only for multi-shot sequences

### Generative App Development

1. **Input collection** - Use CUSTOM fields as text input forms
2. **Option selection** - Present SELECT options as dropdowns/multi-select
3. **Template assembly** - Programmatically combine inputs with selected techniques
4. **Model adaptation** - Reference `model_specifics` to customize per platform
5. **Validation** - Ensure REQUIRED fields populated before generation

---

## Advanced Techniques

### Arijon's Triangle Principle

When staging multi-character scenes, use triangular relationships between performers. Head positioning is critical for directing viewer attention. The "line of interest" should form dynamic triangles.

### Spottiswoode's Cutting Rhythm

Vary editing tempo to control emotional tone. Fast cuts increase energy but risk fatigue. Rhythmic variation maintains engagement.

### Negative Prompting

Model-specific approaches:
- **Veo 3.1**: Use dedicated `negative_prompt` field in JSON
- **Kling**: Add "avoid", "without", or "do not use" phrasing
- **Sora**: Focus on positive descriptors (e.g., "crisp and sharp" vs "not blurry")

---

## Sources and References

1. **Daniel Arijon** - "Grammar of the Film Language" (1976)
   - Practical staging, camera placement, editing techniques
   - Dialogue staging for 2-player, 3-player, multi-player scenes
   - Triangle principle, cutting heights, spatial continuity

2. **Raymond Spottiswoode** - "A Grammar of the Film" (1965)
   - Montage theory and conceptual effects
   - Theoretical approach to film as artistic medium
   - Primary, rhythmical, implicational, ideological montage

3. **Modern AI Video Generation**
   - Model-specific optimization for Kling, Sora, Veo, Wan, Seedance, Runway, Luma

---

## File Structure

```
cinematic_prompt_generation/
├── README.md (this file)
├── film_grammar.md (312 lines - comprehensive reference)
├── six_layer_framework.md (192 lines - flexible framework with 6 templates)
└── prompt_generation.json (466 lines - structured CUSTOM/SELECT data)
```

---

## Version History

**v2.0** - Framework Flexibility Update
- Added CUSTOM/SELECT field structure for dual use (manual + programmatic)
- 6 prompt templates from minimal to complex
- 27 film style references (Kubrick, Fincher, Romanek, etc.)
- Model-specific layer recommendations
- Expanded from 9 to 100+ selectable options per layer
- Clear REQUIRED/OPTIONAL field markers

**v1.0** - Initial Release
- Classical film grammar integration (Arijon + Spottiswoode)
- Six-layer framework foundation
- Basic JSON structure
