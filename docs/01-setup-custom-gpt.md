# Custom GPT Setup Guide

Step-by-step deployment of the generative AI knowledge base as a Custom GPT.

---

## Prerequisites

- ChatGPT Plus or Enterprise account
- All model documentation files from this repository
- **CRITICAL**: A show context document for your project (see Step 0 below)

---

## Step 0: Create Show Context Document (REQUIRED)

**Before uploading anything to Custom GPT**, create your show's visual specification:

1. Open `process/meta-generator-show-context.md`
2. Copy entire contents and paste into ChatGPT or Claude
3. Answer 20 essential questions about your project
4. Save output as `show-context-[YOUR-PROJECT].md`
5. This defines your visual language and ensures consistency

**Example:** See `process/meta-generator-show-context-example-automotive.md`

---

## Step 1: Upload Knowledge Base Files

Upload these files to the Custom GPT knowledge base:

**Required Files** (9 models):

*Image Generation (4):*
- `context/model-image-flux-pro.md`
- `context/model-image-gemini-flash.md`
- `context/model-image-midjourney-v7.md`
- `context/model-image-seedream-4.md`

*Video Generation (4):*
- `context/model-video-seedance-pro.md`
- `context/model-video-runway-gen4-turbo.md`
- `context/model-video-google-veo-3-1.md`
- `context/model-video-luma-ray3.md`

*Image Editing (1):*
- `context/model-editing-flux-kontext.md`

**Required Files (guides):**
- `docs/prompting.md`
- `show-context-[YOUR-PROJECT].md` (created in Step 0)

---

## Step 2: Configure System Prompt

**Option A - Use Generic Template (Quick Start):**
1. Open `process/meta-generator-system-prompt-template.md`
2. Copy the entire contents
3. Paste into Custom GPT "Instructions" field
4. Customize project context section

**Option B - Create Custom Prompt (Recommended for Production):**
1. See `process/README.md` for detailed workflow
2. Use `process/meta-generator-system-prompt.md` to generate custom instructions

### Key Customizations

Update these sections for your project:

**Project Context** (lines 29-33):
```markdown
## Project Context

The project is codenamed **[YOUR PROJECT NAME]**. The final delivery is in
[DEADLINE], meaning production deadlines are [tight/flexible]. The required
aesthetic is [YOUR AESTHETIC], with a minimum technical specification of
[RESOLUTION/QUALITY].
```

**Role Name** (line 5):
```markdown
You are the **[Your Project Name] Production Assistant**, an expert AI...
```

---

## Step 3: Test the Custom GPT

Run these test queries to verify setup:

### Test 1: Show Context Awareness
**Query**: "What's our show's color palette?"
**Expected**: Should reference your show-context-[PROJECT].md and cite the specific colors

### Test 2: Model Selection
**Query**: "Which model should I use for a cinematic video?"
**Expected**: Should recommend based on show context + model capabilities

### Test 3: Prompt Generation
**Query**: "Create a prompt for the hero product shot"
**Expected**: Should use standard prompt prefix from show context + model-specific params

### Test 4: Consistency Enforcement
**Query**: "How do I keep our main character consistent?"
**Expected**: Should reference character details from show context + technical workflow

---

## Step 4: Configure Advanced Settings

### Conversation Starters (Optional)

Add these quick-start prompts:

1. "Help me choose the right model for my task"
2. "Create a prompt for [describe your need]"
3. "What's the workflow for [type of asset]?"
4. "Troubleshoot my failed generation"

### Capabilities

Enable/disable as needed:
- ✅ Web Browsing: OFF (rely on knowledge base only)
- ✅ DALL-E: OFF (we're documenting external models)
- ✅ Code Interpreter: OFF (not needed for prompting)

---

## Step 5: Share and Deploy

### For Team Use

1. Click "Save" on Custom GPT
2. Set sharing to "Anyone with the link" or "Only people in my workspace"
3. Share link with artist team
4. Provide quick reference guide (this doc)

### For Enterprise Deployment

1. Request admin to add to organization GPTs
2. Provide training session for team
3. Collect feedback for improvements

---

## Troubleshooting

### GPT is hallucinating model features

**Cause**: Relying on pre-trained knowledge instead of knowledge base

**Solution**: Add this to system prompt after line 110:
```markdown
- **Critical Constraint**: If a model feature, parameter, or technique is not
  explicitly documented in the provided files, you MUST state:
  "That information is not available in my knowledge base." Never extrapolate
  or guess based on your general knowledge.
```

### GPT provides prompts without citing sources

**Cause**: Missing citation instruction

**Solution**: Already included in line 113 of system prompt. Verify it's present:
```markdown
- **Cite Your Sources**: When providing technical advice, you must cite the
  specific document you are referencing...
```

### Responses are too long or conversational

**Cause**: Tone instruction not strong enough

**Solution**: Emphasize in system prompt (line 99-102):
```markdown
Your tone is that of a busy, expert production tool.
Be **technical, direct, and concise**.
Avoid conversational filler, apologies, or subjective creative opinions.
```

---

## Updating the Knowledge Base

When new models are added:

1. Add new `model-*.md` file to knowledge base
2. Update system prompt if needed (new model categories)
3. Test with queries about the new model
4. Update this deployment guide

---

## Success Checklist

- [ ] **Show context created** (Step 0)
- [ ] All 9 model files uploaded (4 image + 4 video + 1 editing)
- [ ] Prompting guide uploaded (docs/prompting.md)
- [ ] **Show context uploaded** (show-context-[PROJECT].md)
- [ ] System prompt configured and customized
- [ ] All 4 test queries pass
- [ ] Conversation starters added
- [ ] Team has access link
- [ ] Feedback collection process established

---

**Deployment time**: ~30 minutes (includes show context creation)
**Maintenance**: Update show context when visual direction changes; update models as new ones added
