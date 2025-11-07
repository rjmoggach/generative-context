# Process Directory

This directory contains templates, examples, and tools for creating Custom GPTs and project-specific workflows.

---

## File Guide

All files follow the pattern: `meta-generator-[TYPE]-[SUBTYPE].md`

### Show Context (Visual Specification)

**meta-generator-show-context.md** (The Generator)
- **What**: Creates show context documents via 20 questions
- **When**: START of every project - defines visual language
- **Use**: Copy → paste into ChatGPT/Claude → answer questions → save output

**meta-generator-show-context-template.md** (Empty Template)
- **What**: Blank show context structure
- **When**: Manual creation without generator
- **Use**: Copy and fill all sections (<500 lines)

**meta-generator-show-context-example-automotive.md** (Complete Example)
- **What**: Finished show context for luxury automotive commercial
- **When**: Reference to understand structure and detail level
- **Use**: Study before creating your own

### System Prompt (Custom GPT Instructions)

**meta-generator-system-prompt.md** (The Generator)
- **What**: Creates Custom GPT system prompts
- **When**: After show context is created
- **Use**: Copy → paste into ChatGPT → describe project → get GPT instructions

**meta-generator-system-prompt-template.md** (Generic Template)
- **What**: Ready-to-use GPT system prompt
- **When**: Quick GPT setup without custom generation
- **Use**: Copy to GPT "Instructions" field, customize project context

### Model Documentation

**meta-generator-model-context.md** (Model Template)
- **What**: Template for documenting new generative AI models
- **When**: Adding new models to the library
- **Use**: Follow structure to create new `context/model-[type]-[name].md`

---

## Workflow: Creating a Show Context (Do This FIRST!)

**CRITICAL**: Before prompting ANY generative AI models, create a show context document. This defines your visual language and ensures consistency.

**Key Concept:**

- **Show Context** = Visual specification document (uploaded to GPT knowledge base)
- **GPT System Prompt** = Instructions that reference the show context

### Option A: Use the Meta-Generator (Recommended)

1. **Copy the generator**

   ```bash
   cat meta-generator-show-context.md | pbcopy  # macOS
   ```

2. **Paste into ChatGPT or Claude**
   - Answer 20 essential questions

3. **Receive your context**
   - AI generates concise markdown (<500 lines)
   - Save as `show-context-[YOUR-PROJECT].md`

4. **Upload to Custom GPT knowledge base**

### Option B: Manual Creation

1. **Copy the template**

   ```bash
   cp meta-generator-show-context-template.md ../show-context-[YOUR-PROJECT].md
   ```

2. **Fill in all sections** (reference `meta-generator-show-context-example-automotive.md`)

3. **Upload to Custom GPT knowledge base**

### Usage

The GPT system prompt will say: "Refer to show-context-[PROJECT].md for visual specifications"

---

## Workflow: Creating a Custom GPT for Your Project

### Option A: Manual Customization (Recommended)

1. **Start with the generic template**

   ```bash
   cp meta-generator-system-prompt-template.md ../my-project-prompt.md
   ```

2. **Customize for your project**
   - Update Role/Goal
   - Add project context (deadline, aesthetic, requirements)
   - Reference your show context file
   - Adjust workflow if needed

3. **Deploy to Custom GPT**
   - Follow steps in `docs/01-setup-custom-gpt.md`
   - Use your customized prompt in "Instructions" field

### Option B: Use the Meta-Generator

1. **Copy meta-generator contents**

   ```bash
   cat meta-generator-system-prompt.md | pbcopy  # macOS
   ```

2. **Paste into ChatGPT and provide requirements**

   ```
   Example prompt:
   "I need a Custom GPT for a fashion brand's Spring 2026 campaign.
   The project requires luxury aesthetic, 4K resolution minimum,
   deadline is March 2026. We're using FLUX.1 Pro and Midjourney v7
   primarily for still images."
   ```

3. **Save the generated prompt**
   - Copy the output to `example-YOUR-PROJECT-prompt.md`
   - Use in Custom GPT setup

4. **Deploy to Custom GPT**
   - Follow steps in `docs/01-setup-custom-gpt.md`

---

## Quick Reference

| File | Purpose | When to Use |
|------|---------|-------------|
| `meta-generator-show-context.md` | **Generate show contexts** | **FIRST - Define visual language** |
| `meta-generator-show-context-template.md` | Show context template | Manual creation |
| `meta-generator-show-context-example-automotive.md` | Show context example | Reference |
| `meta-generator-system-prompt.md` | Generate GPT prompts | After show context |
| `meta-generator-system-prompt-template.md` | GPT prompt template | Quick setup |
| `meta-generator-model-context.md` | Model doc template | Add new models |

---

## File Naming Convention

All files follow: **`meta-generator-[TYPE]-[SUBTYPE].md`**

**TYPE** categories:
- `show-context` - Visual specification documents
- `system-prompt` - Custom GPT instructions
- `model-context` - Model documentation

**SUBTYPE** clarifiers:
- *(no subtype)* - The generator/meta-prompt
- `template` - Empty structure to fill
- `example-[name]` - Complete filled example

**Examples:**
- `meta-generator-show-context.md` - Generates show contexts
- `meta-generator-show-context-template.md` - Empty template
- `meta-generator-show-context-example-automotive.md` - Automotive example

---

## Common Questions

**Q: Which system prompt should I use for my Custom GPT?**
A: If you have a specific project with requirements (deadline, aesthetic, etc.), customize `template-system-prompt-generic.md` or use the meta-generator. For testing or general use, use `template-system-prompt-generic.md` as-is.

**Q: What's the difference between the generic template and the example?**
A: The generic template is universal and works for any project. The example is customized for a specific project ("SBW - Super Bowl 2026") to show you what customization looks like.

**Q: Do I need to use the meta-generator?**
A: No. It's optional. You can manually customize `template-system-prompt-generic.md` instead. The meta-generator is helpful if you want AI assistance in creating project-specific prompts.

**Q: How do I add a new AI model to the library?**
A: Use `process-model-template.md` as your starting point. Follow the structure exactly, then save to `context/model-[type]-[name].md`.

---

## Next Steps

1. **To create a Custom GPT**: See `docs/01-setup-custom-gpt.md`
2. **To learn workflows**: See `docs/02-workflow-basics.md`
3. **To choose models**: See `docs/03-model-selection.md`
4. **To add a new model**: Use `process-model-template.md`
