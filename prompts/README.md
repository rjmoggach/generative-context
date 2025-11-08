# Prompts Directory

This directory contains system prompts for Custom GPTs and meta-generators for creating new system prompts.

---

## File Guide

### System Prompts (Production-Ready Custom GPT Instructions)

**system-prompt-project-context-assistant.md**
- **What**: System prompt for generating project visual context documents
- **GPT Name**: "Project Context Assistant"
- **Purpose**: Guides users through recursive questioning to define visual language
- **Output**: `project-context-<show-code>.md` files
- **Use**: Upload to Custom GPT "Instructions" field

**system-prompt-shot-assistant.md**
- **What**: System prompt for generating shot-specific prompts
- **GPT Name**: "Shot Assistant"
- **Purpose**: Creates model-optimized prompts for individual shots
- **Workflow**: Establishing → Master → Coverage
- **Use**: Upload to Custom GPT "Instructions" field

**system-prompt-model-context-generator.md**
- **What**: System prompt for documenting new AI models
- **Purpose**: Creates structured model documentation for context library
- **Output**: `model-[type]-[name].md` files
- **Use**: Upload to Custom GPT "Instructions" field

**system-prompt-template.md**
- **What**: Generic template for creating new system prompts
- **When**: Starting point for custom GPT system prompts
- **Use**: Copy and customize for new use cases

### Meta-Generators (Create New System Prompts)

**meta-generator-system-prompt.md**
- **What**: Meta-prompt that generates new Custom GPT system prompts
- **When**: Creating a new specialized GPT
- **Process**: 20-question interview → complete system prompt
- **Use**: Copy → paste into ChatGPT/Claude → answer questions → get system prompt

---

## Workflow Overview

### Step 1: Define Project Visual Language

Use **Project Context Assistant** GPT to create `project-context-<show-code>.md`

1. Deploy `system-prompt-project-context-assistant.md` to a Custom GPT
2. Start conversation with the GPT
3. Answer recursive questions about visual style
4. GPT generates complete `project-context-<show-code>.md`
5. Save the output and add to GPT knowledge base

### Step 2: Generate Shot Prompts

Use **Shot Assistant** GPT to create model-specific prompts

1. Deploy `system-prompt-shot-assistant.md` to a Custom GPT
2. Upload `project-context-<show-code>.md` to GPT knowledge base
3. Start conversation with show code
4. Follow workflow: Establishing → Master → Coverage
5. GPT generates optimized prompts for each model

### Step 3: Create New GPTs (Optional)

Use **meta-generator-system-prompt.md** to create specialized system prompts

1. Copy meta-generator to ChatGPT/Claude
2. Answer 20 questions about your new GPT
3. Receive production-ready system prompt
4. Deploy to Custom GPT

---

## Quick Reference

| File | Purpose | Deploy To |
|------|---------|-----------|
| `system-prompt-project-context-assistant.md` | Generate project visual contexts | Custom GPT |
| `system-prompt-shot-assistant.md` | Generate shot-specific prompts | Custom GPT |
| `system-prompt-model-context-generator.md` | Document new AI models | Custom GPT |
| `system-prompt-template.md` | Starting template for new prompts | Customize |
| `meta-generator-system-prompt.md` | Create new system prompts | ChatGPT/Claude |

---

## File Naming Convention

**System Prompts (Production):**
- `system-prompt-[function].md` - Ready-to-deploy Custom GPT instructions

**Meta-Generators (Development):**
- `meta-generator-[type].md` - Generates new system prompts or templates

---

## Common Questions

**Q: Which GPT should I deploy first?**
A: Start with **Project Context Assistant** to define your visual language. Then deploy **Shot Assistant** to generate prompts.

**Q: How do I create a new specialized GPT?**
A: Use `meta-generator-system-prompt.md` - it will interview you and generate a complete system prompt.

**Q: Can I customize the existing system prompts?**
A: Yes. Copy any `system-prompt-*.md` file, modify it for your needs, and deploy to a Custom GPT.

**Q: How do I add a new AI model to the library?**
A: Use **Model Context Generator** GPT (deploy `system-prompt-model-context-generator.md`) to create structured documentation.

---

## Next Steps

1. **Deploy Project Context Assistant**: Use `system-prompt-project-context-assistant.md`
2. **Create your first project context**: Generate `project-context-<show-code>.md`
3. **Deploy Shot Assistant**: Use `system-prompt-shot-assistant.md`
4. **Upload project context**: Add to Shot Assistant's knowledge base
5. **Start generating prompts**: Follow Establishing → Master → Coverage workflow
