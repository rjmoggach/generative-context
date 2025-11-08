# Video Prompt Engineering Framework Analysis

**COMPREHENSIVE VERSION**: For the complete framework with film grammar principles, 27 cinematographic references, and structured CUSTOM/SELECT fields for app development, see `../cinematic_prompt_generation/`

**This document**: Quick reference for practical video prompting across AI models.

---

## Six-Layer Framework (Universal for All Models)

### Layer 1: Subject and Action
- **Who/What**: The focus of the shot
- **Action/Movement**: What is happening
- **Emotional State/Energy**: The essence to capture

**Example**: "A woman in a flowing red dress walking through a sunlit Victorian garden with a contemplative expression"

### Layer 2: Shot Type and Framing
- **Wide Shot**: Full environment and context
- **Medium Shot**: Waist up, balances subject and setting
- **Close-Up**: Face or detail, intimate portrayal

**Framing Angles**:
- Eye Level: Neutral, natural
- Low Angle: Powerful, dramatic
- High Angle: Vulnerability

### Layer 3: Camera Movement
- **Static Shot**: Camera remains still
- **Tracking Shot**: Camera maintains connection with subject
- **Panning**: Camera rotates horizontally, revealing environment
- **Dolly/Push-in/Push-out**: Camera moves closer or farther, creating intensity

**Pro Tip**: Slow and deliberate movements create cinematic effect (e.g., "slow dolly forward", "gentle tracking shot")

### Layer 4: Lighting and Atmosphere
- **Golden Hour**: Warm, soft, romantic, cinematic (sunrise/sunset)
- **Blue Hour**: Twilight, mysterious, atmospheric
- **Studio Lighting**: Precise, controlled, dramatic, professional

**Considerations**:
- Color Temperature: Warm, cool, red, alarming
- Light Quality: Soft or hard, diffused or direct
- Environment Effects: Rain, fog, particles
- Contrast and Shadow Depth: Strong lights vs shadows

### Layer 5: Technical Specs
**Lens Types**:
- 35mm: Wide angle
- 50mm: Natural perspective
- 85mm: Portrait
- Macro: Extreme detail, extreme close-up

**Depth of Field**:
- Shallow: Blurred background
- Deep: Everything in focus
- Bokeh: Aesthetic blur quality
- Rack Focus: Focus shifts between subjects

**Film Aesthetics**:
- 35mm film grain
- Anamorphic lens flares
- Kodak Portra color palette
- IMAX quality
- Vintage 1970s film stock

### Layer 6: Duration and Pacing
- **Duration**: 3-10 seconds (often set as parameter, not in prompt)
- **Speed**: Slow motion (0.5x), fast motion, time lapse (2-10x speed)
- **Rhythm**: Slow paced, energetic, fast
- **Transitions**: Smooth fade out, hard cut

**Pro Tip**: 120fps for slow motion, specify exact speed like "0.5 speed"

## Universal Prompt Template

```
[Shot Type] of [Subject] doing [Action] in/at [Setting], [Camera Movement], [Lens], [Camera], [Lighting], [Atmosphere], [Technical Details]
```

**Example**:
"Medium shot of a female athlete in vibrant athletic wear performing a dynamic leap dance move between buildings in a city's downtown, smooth dolly camera movement visible through motion blur trails, dramatic golden hour lighting with volumetric rays streaming through urban architecture, shot with 85 millimeter lens creating beautiful bokeh depth of field, composed with dynamic pacing and rhythm, ultra high quality, 8k resolution, professional cinematography, award-winning composition"

## Model-Specific Optimizations

### Kling 2.5
**Best For**: Athletic movement, character animation, motion fluidity, action rendering

**Prompt Structure**:
1. Detailed visual description
2. Camera movement
3. Professional cinematography
4. Specific style reference
5. Lighting conditions
6. High quality markers

**Pro Tip**: Don't give it more time than needed. If action takes 5 seconds, use 5 seconds, not 10.

### Sora 2 / Sora 2 Pro
**Best For**: Multi-shot storytelling, seamless multi-angle sequences, spatial consistency

**Capabilities**:
- Creates establishing shot, action, detail, and reaction in one sequence
- Maintains spatial relationships
- Responds well to professional camera language

**Prompt Structure**:
"Start as [establishing shot description], [transition] to [medium shot description], then [transition] to [close-up description], [additional camera techniques]. [Technical specs], [transitions note]"

**Example**:
"Establishing wide shot of a bustling Parisian cafe at golden hour, slowly pushing into a medium shot of a woman reading at a corner table, then cutting to close-up of an espresso cup, rack focus to her contemplative expression as she looks up toward the window. 35mm lens, warm cinematic lighting, shallow depth of field, seamless transitions, maintaining spatial consistency"

### Alibaba WAN 2.5
**Best For**: Lip sync, dialogue, multilingual content, character narratives

**Advantages**:
- Open source (cheaper: ~165 credits for 10s 1080p vs ~330+ for Sora 2 Pro)
- Uncensored and anonymized on Venice AI
- Excellent lip sync capabilities

**Prompt Structure for Dialogue**:
"[Visual description]. The character says '[dialogue]' with [tone/emotion]. [Lip sync details], [gestures], [expressions]."

**Example**:
"Medium shot of a visionary figure in Renaissance Venice, standing on a grand marble balcony overlooking the Grand Canal at golden hour. The character says 'Don't sleep on Venice AI' with a commanding and visionary tone, emphasis on 'don't' and 'Venice AI'. Perfect lip sync with mouth movements, theatrical hand gesture on 'don't sleep', proud sweeping gesture toward Venice skyline on 'Venice AI', eyes gleaming with conviction."

### Google Veo 3 / Veo 3.1
**Best For**: Premium production, exact creative vision, commercial/art projects, fine-tuned control

**Unique Feature**: JSON prompting for more consistent results and precise control

**JSON Structure**:
```json
{
  "scene": "Description of environment and subject",
  "movement": "Camera movement type",
  "angle": "Camera angle",
  "lens": "Lens specification",
  "speed": "Playback speed multiplier",
  "lighting": "Lighting description",
  "atmosphere": "Atmospheric effects",
  "color_grading": "Color palette",
  "style": "Overall aesthetic",
  "duration": "Length in seconds",
  "negative_prompt": "Things to avoid"
}
```

**Example JSON**:
```json
{
  "scene": "A cyberpunk street market at night with neon signs",
  "movement": "Slow dolly forward",
  "angle": "Eye level",
  "lens": "35 millimeter lens",
  "speed": "0.5x speed",
  "lighting": "Neon lights, volumetric fog",
  "atmosphere": "High contrast",
  "color_grading": "Teal and orange color grading",
  "style": "Cinematic feel",
  "duration": "8 seconds"
}
```

## Advanced Techniques

### 1. The 5-10-1 Rule (Cost-Efficient Iteration)
1. Make 5 variations on a cheaper model (Kling or WAN) at 40-60 credits each
2. Select the best from the initial batch
3. Do 10 more iterations on the best one
4. Take that prompt and do a final render on premium model (Veo 3 or Sora 2 Pro)

**Cost Savings**: ~1,000 credits vs potentially thousands by iterating only on premium models

### 2. Negative Prompting
Specify what you DON'T want to see.

**Common Negative Prompts**:
- Blurry, low quality
- Distorted faces, warped hands
- Anatomical issues (e.g., "arms in the back of the body")
- Text artifacts, watermark
- Consistency problems

**Model-Specific Implementation**:
- **Veo 3 (JSON)**: Built-in `negative_prompt` field
- **Kling**: Add to main prompt with "avoid", "without", "don't use"
- **Sora**: Be explicit about what you want (e.g., instead of "not blurry", say "very focused and crisp")

### 3. Style Reference Stacking
Combine multiple film references for unique aesthetic.

**Example**:
"Shot of a detective walking through rain-soaked streets, aesthetic combining Blade Runner 2049 color grading + Seven atmosphere and mood + Heat camera movement, using anamorphic lens and cinematic bokeh"

**Pro Tip**: Stack 2-3 references for great results. More references = more diluted aesthetics, but can create unique styles.

## Key Principles

1. **Think like a director**: Give instructions to a camera operator, not everyday descriptions
2. **Use cinematography language**: AI models are trained on professional film and video data
3. **Be specific**: More detail = more control = better results = fewer iterations = money saved
4. **Match duration to action**: Don't give 10 seconds if the action only needs 5
5. **Order matters somewhat**: Put shot type and subject/action first
6. **Iterate strategically**: Use cheaper models for experimentation, premium for final renders
