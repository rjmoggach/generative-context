# Generative Model Context File - Regeneration Process

**Objective**: To provide a standardized process for creating and updating generative model context files, ensuring they remain consistent, comprehensive, and concise for use as cached context by a custom GPT for artist teams.

---

## Step 1: Model Identification and Scoping

1.  **Identify Target Model**: Clearly define the generative model and its specific version that requires documentation (e.g., `Midjourney v7.1`, `Seedance 2.0`).
2.  **Define Scope**: Determine the primary function (e.g., Text-to-Image, Image-to-Video, Image Editing). If a model has multiple functions, create a separate document for each.
3.  **File Naming**: Name the file using lowercase kebab-case: `[model-name]-[version/type].md` (e.g., `midjourney-v7.md`, `flux-kontext.md`).

## Step 2: Deep Research and Information Gathering

1.  **Prioritize Official Sources**: Begin research at the model developer’s official website, technical reports, API documentation, and official blog posts or release notes.
2.  **Consult Secondary Sources**: Expand research to include reputable third-party sources such as AI research blogs, community forums (e.g., Reddit), and platform-specific documentation (e.g., Replicate, Fal.ai) for practical implementation details.
3.  **Gather Key Information**: Collect data points that align with the Unified Documentation Pattern. Focus on:
    *   Model version, resolution, cost, and speed.
    *   Core prompting structure and syntax.
    *   A complete list of parameters and their functions.
    *   Advanced features and unique capabilities.
    *   Common issues and effective workarounds.
    *   API endpoints and integration examples.

## Step 3: Content Synthesis and Drafting

1.  **Adhere to the Unified Documentation Pattern**: Structure the new Markdown file using the standard template. This ensures consistency across all context files.
2.  **Write for Conciseness**: Remember that this document will be used as cached context. Use tables for parameters and troubleshooting. Keep descriptions brief and to the point.
3.  **Use Standard Markdown**: Do not use emojis, em/en dashes, or non-standard characters. Use simple hyphens and straight quotes. All syntax, parameters, and technical terms must be in `code` formatting.
4.  **Use Structured Callouts**: Use blockquotes with prefixes for emphasis:
    *   `> **Note:**` for helpful information.
    *   `> **Tip:**` for best practices.
    *   `> **Warning:**` for critical limitations.

## Step 4: Review and Finalization

1.  **Quality Checklist**: Before finalizing, perform a quality check:
    *   [ ] Is the Quick Reference table complete and accurate?
    *   [ ] Are all sections of the Unified Documentation Pattern present?
    *   [ ] Is the content concise and free of redundancy?
    *   [ ] Are all parameters documented in a table?
    *   [ ] Are troubleshooting steps clear and actionable?
    *   [ ] Does the file name follow the `kebab-case.md` convention?
    *   [ ] Is the formatting clean and consistent?
2.  **Final Save**: Save the completed file in the appropriate directory (`/models/image`, `/models/video`, etc.).

---

## Unified Documentation Pattern (Template)

```markdown
# [Model Name] - [Version/Type]

---

## Quick Reference

| Attribute | Value |
|---|---|
| **Current Version** | ... |
| **Model Type** | ... |
| **Primary Use** | ... |
| **Max Resolution** | ... |
| **Speed** | ... |
| **Cost** | ... |
| **API Endpoint** | ... |

---

## Overview

(Brief paragraph on core strengths, differentiators, and limitations. Include a version history subsection if applicable.)

---

## When to Use This Model

(Comparison with alternatives, clear strengths/weaknesses to guide model selection.)

---

## Prompting Structure

(Core framework with a visual breakdown or diagram.)

---

## Parameters

(Complete table of all parameters, their syntax, values, defaults, and purpose.)

---

## Techniques

(Organized by skill level: Basic, Intermediate, Advanced. Include "Before/After" prompt examples.)

---

## Common Workflows

(1-2 step-by-step scenarios for typical use cases.)

---

## Troubleshooting

(Table of common issues, their causes, and solutions.)

---

## Integration

(API examples, workflow position, and complementary tools.)
```
