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

**CRITICAL FIRST STEP:** Deploy the Project Context Assistant
1. Use `prompts/system-prompt-project-context-assistant.md` for Custom GPT instructions
2. Have a conversation to generate `project-context-<show-code>.md`
3. Upload to knowledge base

**Then:**
1. Upload all `context/model-*.md` files to knowledge base (9 models)
2. Upload all `context/guide-*.md` and `context/reference-*.md` files
3. Deploy Shot Assistant: `prompts/system-prompt-shot-assistant.md`
4. Upload your `project-context-<show-code>.md` to Shot Assistant knowledge base
5. See `docs/01-setup-custom-gpt.md` for detailed steps

### For Pickaxe No-Code Apps

Pickaxe is a no-code platform for creating custom AI apps with strict formatting constraints.

1. Use `pickaxe/generate-pickaxe.md` for standard conversational Pickaxe apps
2. Use `pickaxe/generate-pickaxe-multiquestion.md` for multi-question sequential Q&A apps
3. These meta-prompts generate system prompts optimized for Pickaxe's lightweight interface

### For Video/Cinematic Prompting

For advanced video generation with film grammar principles:

1. **Core framework**: `context/guide-prompting-framework.md` - Six-layer framework with templates
2. **Structured data**: `context/guide-prompting-framework.json` - CUSTOM/SELECT fields for apps
3. **Film grammar**: `context/reference-film-grammar.md` - Arijon & Spottiswoode principles
4. **Visual references**: `context/reference-visual-*.md` - Directors, cinematographers, photographers
5. **Quick reference**: `docs/04-six-layer-framework.md` - Practical video prompting guide

---

## Documentation Structure

```
context/
├── model-image-*.md                   # Image generation models (4 models)
├── model-video-*.md                   # Video generation models (4 models)
├── model-editing-*.md                 # Image editing models (1 model)
├── guide-prompting-general.md         # Universal prompting principles
├── guide-prompting-framework.md       # Six-layer prompting framework
├── guide-prompting-framework.json     # Structured prompting data
├── guide-context-questioning.md        # Deep questioning for visual style
├── reference-film-grammar.md          # Comprehensive film grammar
├── reference-film-movements.md        # Cinema history and movements
├── reference-visual-cinematographers.md # Master cinematographers
├── reference-visual-film-directors.md  # Auteur film directors
├── reference-visual-commercial-directors.md # Commercial directors
└── reference-visual-photographers.md   # Still photography masters

docs/
├── 01-setup-custom-gpt.md     # Custom GPT deployment guide
├── 02-workflow-basics.md      # Common production workflows
├── 03-model-selection.md      # Choosing the right model
└── 04-six-layer-framework.md  # Quick video prompting reference

prompts/
├── README.md                                   # System prompt guide
├── system-prompt-project-context-assistant.md  # GPT: Generate project contexts
├── system-prompt-shot-assistant.md             # GPT: Generate shot prompts
├── system-prompt-model-context-generator.md    # GPT: Document new models
├── system-prompt-template.md                   # Template for new prompts
└── meta-generator-system-prompt.md             # Create new system prompts

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

- **Adding models**: Use Model Context Generator GPT (`prompts/system-prompt-model-context-generator.md`)
- **Updating docs**: Log changes in `CHANGELOG.md`
- **File naming**:
  - Models: `model-[type]-[name].md` (kebab-case)
  - System prompts: `system-prompt-[function].md`
  - Meta-generators: `meta-generator-[type].md`

---

## Version History

See `CHANGELOG.md` for version history and detailed changes.
