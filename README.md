# Generative AI Context Library

**Version**: 0.1
**Released**: 2025-11-07

Production-ready knowledge base for generative AI workflows. Designed for Custom GPT integration and artist teams.

---

## Quick Start

### For Artists

1. Find your model: `context/model-[type]-[name].md`
2. Read the prompting guide: `docs/prompting.md`
3. See workflow examples: `docs/example-*.md`

### For Custom GPT Setup

**CRITICAL FIRST STEP:** Create a show context document
1. Use `process/meta-generator-show-context.md` to create your show's visual specification
2. Save as `show-context-[YOUR-PROJECT].md`

**Then:**
1. Upload all `context/model-*.md` files to knowledge base (9 models)
2. Upload `docs/prompting.md` to knowledge base
3. Upload your `show-context-[YOUR-PROJECT].md` to knowledge base
4. Choose a system prompt:
   - Quick start: `process/meta-generator-system-prompt-template.md`
   - Custom: Use `process/meta-generator-system-prompt.md`
5. See `docs/01-setup-custom-gpt.md` for detailed steps

### For Pickaxe No-Code Apps

Pickaxe is a no-code platform for creating custom AI apps with strict formatting constraints.

1. Use `pickaxe/generate-pickaxe.md` for standard conversational Pickaxe apps
2. Use `pickaxe/generate-pickaxe-multiquestion.md` for multi-question sequential Q&A apps
3. These meta-prompts generate system prompts optimized for Pickaxe's lightweight interface

### For Video/Cinematic Prompting

For advanced video generation with film grammar principles:

1. See `cinematic_prompting/` for the complete framework
2. Includes classical film grammar (Arijon, Spottiswoode)
3. 27 cinematographic references (Kubrick, Fincher, Romanek, etc.)
4. Structured CUSTOM/SELECT fields for both manual prompting and app development
5. Quick reference: `docs/04-six-layer-framework.md`

---

## Documentation Structure

```
context/
├── model-image-*.md      # Image generation models (4 models)
├── model-video-*.md      # Video generation models (4 models)
└── model-editing-*.md    # Image editing models (1 model)

docs/
├── 01-setup-custom-gpt.md     # Custom GPT deployment guide
├── 02-workflow-basics.md      # Common production workflows
├── 03-model-selection.md      # Choosing the right model
├── 04-six-layer-framework.md  # Quick video prompting reference
└── prompting.md               # Universal prompting principles

process/
├── README.md                                          # Process workflow guide
├── meta-generator-show-context.md                     # Generate show contexts (20 questions)
├── meta-generator-show-context-template.md            # Show context template
├── meta-generator-show-context-example-automotive.md  # Show context example
├── meta-generator-system-prompt.md                    # Generate GPT prompts
├── meta-generator-system-prompt-template.md           # GPT prompt template
└── meta-generator-model-context.md                    # Model documentation template

cinematic_prompting/
├── README.md               # Framework overview and guide
├── film_grammar.md         # Comprehensive film grammar principles
├── prompt_structure.md     # Flexible framework with 6 templates
└── prompt_structure.json   # Structured CUSTOM/SELECT data

pickaxe/
├── generate-pickaxe.md                # Meta-prompt for standard Pickaxe apps
└── generate-pickaxe-multiquestion.md  # Meta-prompt for multi-question apps
```

---

## Available Models

### Image Generation (4 models)
- **FLUX.1 Pro** - Fast, high-res (4MP), commercial assets
- **Gemini Flash** - Conversational editing, text rendering
- **Midjourney v7** - Artistic, stylized, concept art
- **Seedream 4.0** - Ultra high-res (4K native), print quality

### Video Generation (4 models)
- **Seedance Pro** - Cinematic, multi-shot narratives (1080p, 10s)
- **Runway Gen-4 Turbo** - Fast iteration, character consistency (720p, 10s)
- **Google Veo 3.1** - Audio+video generation (1080p, 8s)
- **Luma Ray3** - HDR video, advanced physics (4K upscale, 10s)

### Image Editing (1 model)
- **FLUX.1 Kontext** - Iterative editing, character consistency

**Total: 9 production-ready models**

---

## Production Workflow

### Complete Project Flow

```
STEP 1: Define Visual Language
↓
Create show context using meta-generator-show-context.md (20 questions)
Save as show-context-[PROJECT].md
↓
STEP 2: Set Up Custom GPT
↓
Upload: 9 model files + prompting.md + show-context-[PROJECT].md
Create system prompt (references show context)
↓
STEP 3: Generate Assets
↓
Use standard prompt prefix from show context
GPT references show context for consistency
Generate images/videos with recommended models
↓
STEP 4: Iterate & Refine
↓
Maintain consistency using show context guidelines
```

### Asset-Specific Workflows

**Still Image Production**
```
Concept → Midjourney v7 → Refinement → FLUX.1 Kontext → Final → Seedream 4.0 (4K)
```

**Video (Narrative)**
```
Keyframe → Midjourney v7 → Animation → Seedance Pro → Post → Edit & sound
```

**Video (With Audio)**
```
Keyframe → FLUX.1 Pro → Video+Audio → Veo 3.1 → Post → Color & mix
```

**Video (HDR/VFX)**
```
Concept → Luma Ray3 Draft → Final → Luma Ray3 HiFi (4K HDR) → Composite
```

**Product Photography**
```
Base → FLUX.1 Pro (ultra) → Variations → FLUX.1 Kontext
```

---

## Key Features

- **Consistent Structure**: All 9 model docs follow same template
- **LLM-Optimized**: Flat file structure, semantic prefixes
- **Production-Ready**: Real workflows, troubleshooting tables
- **No Emojis**: Clean, professional formatting
- **Version Controlled**: CHANGELOG.md tracks updates

---

## Model Selection Guide

| Need | Use | Alternative |
|------|-----|-------------|
| Speed + high-res | FLUX.1 Pro | Seedream 4.0 |
| Maximum resolution | Seedream 4.0 | FLUX.1 Pro |
| Artistic style | Midjourney v7 | FLUX.1 Pro |
| Text in images | Gemini Flash | FLUX.1 Pro |
| Character consistency (image) | Midjourney v7 + Kontext | - |
| Character consistency (video) | Runway Gen-4 | Seedance Pro |
| Cinematic video (multi-shot) | Seedance Pro | Runway Gen-4 |
| Video with audio | Veo 3.1 | Seedance + post audio |
| HDR video for VFX | Luma Ray3 | Veo 3.1 |
| Fast video iteration | Runway Gen-4 | Luma Ray3 Draft |
| Image editing | FLUX.1 Kontext | Gemini Flash |

---

## Universal Prompting Principles

1. **Front-load style**: `"Cinematic photo of..."` (not `"...cinematic style"`)
2. **Be specific**: `"1967 red Mustang convertible"` (not `"nice car"`)
3. **Positive phrasing**: Describe what you want, not what you don't
4. **Layer information**: Style → Subject → Technical → Context
5. **Iterate**: Start simple, refine one element at a time

See `docs/prompting.md` for complete guide.

---

## Video Model Comparison

| Feature | Seedance Pro | Runway Gen-4 | Veo 3.1 | Luma Ray3 |
|---------|-------------|--------------|---------|-----------|
| **Resolution** | 1080p | 720p (4K upscale) | 1080p | 4K (HiFi) |
| **Duration** | 10s | 10s | 8s | 10s |
| **Speed** | Medium | Fast (~30s) | Medium | 5x in Draft |
| **Audio** | ❌ | ❌ | ✅ Native | ❌ |
| **HDR** | ❌ | ❌ | ❌ | ✅ 16-bit |
| **Multi-shot** | ✅ Excellent | ❌ | ❌ | ❌ |
| **Character Lock** | Good | ✅ Excellent | Good | Good |
| **Best For** | Narratives | Rapid prototyping | Dialogue scenes | VFX elements |

---

## Maintenance

- **Adding models**: Follow `process/meta-generator-model-context.md`
- **Updating docs**: Log changes in `CHANGELOG.md`
- **File naming**:
  - Models: `model-[type]-[name].md` (kebab-case)
  - Process: `meta-generator-[TYPE]-[SUBTYPE].md`

---

## Version History

See `CHANGELOG.md` for version history and detailed changes.
