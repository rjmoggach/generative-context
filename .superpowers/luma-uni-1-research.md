# Research Report: Luma Uni-1 Model Doc

## Proposed Filename

`model-image-luma-uni-1.md`

Type prefix `image` because Uni-1 is an image-only model (text-to-image + image editing). Luma's video models retain the `video` prefix (Ray3, etc.).

---

## Official Name

The official name is **Luma Uni-1** (hyphenated, no space). The API version is **Uni-1.1** (announced May 5, 2026). The original prompt named it "Luma Uni 1" (with a space and no hyphen) -- the correct form is `Uni-1`.

---

## Sources

### Primary (Official Luma)
- Luma AI - UNI-1 Product Page: https://lumalabs.ai/uni-1
- Luma AI - UNI-1 Tech Specs: https://lumalabs.ai/uni-1/tech-specs
- Luma AI - Introducing the Uni-1.1 API: https://lumalabs.ai/news/uni-1-1-api
- Luma AI - Uni-1 Field Guide: https://lumalabs.ai/learning-center/articles/luma-uni-1-field-guide
- Luma AI - Uni-1 Model Start Guide: https://lumalabs.ai/learning-hub/luma-uni-1-model
- Luma AI - Agents Quickstart Docs: https://docs.agents.lumalabs.ai/
- Luma AI Freshdesk - What Is the Uni-1 API: https://lumaai-help.freshdesk.com/support/solutions/articles/151000230412-what-is-the-uni-1-api-

### Reputable Secondary
- TechCrunch - Luma Launches Creative AI Agents: https://techcrunch.com/2026/03/05/exclusive-luma-launches-creative-ai-agents-powered-by-its-new-unified-intelligence-models/
- VentureBeat - Luma AI Launches Uni-1: https://venturebeat.com/technology/luma-ai-launches-uni-1-a-model-that-outscores-google-and-openai-while
- MarkTechPost - Luma Labs Launches Uni-1: https://www.marktechpost.com/2026/03/23/luma-labs-launches-uni-1-the-autoregressive-transformer-model-that-reasons-through-intentions-before-generating-images/
- The Decoder - Luma Uni-1.1 Image API: https://the-decoder.com/luma-opens-uni-1-1-image-model-api-at-prices-and-quality-matching-openai-and-google/
- i-SCOOP - Uni-1 from Luma AI: https://www.i-scoop.eu/uni-1-luma-ai/
- MindStudio - What Is Luma Uni-1: https://www.mindstudio.ai/blog/what-is-luma-uni1-thinking-image-model

### Developer/Integration
- fal.ai - Uni-1 Model Page: https://fal.ai/uni-1
- Runware - UNI-1 Max API Docs: https://runware.ai/docs/models/luma-uni-1-max
- digen.ai - Luma Uni API 2026 Integration Guide: https://resource.digen.ai/luma-uni-api-for-developers-2026-guide/
- emelia.io - Luma Uni-1 Review Full Breakdown: https://emelia.io/hub/luma-uni-1-review
- mer.vin - Uni-1.1 API Pricing Explained: https://mer.vin/2026/05/luma-uni-1-1-api-explained-faster-image-generation-built-in-prompt-intelligence-and-production-pricing/

---

## Confidence Assessment

### High Confidence (confirmed across multiple independent sources)
- Official name: Uni-1 (hyphenated); API version Uni-1.1
- Release dates: Announced March 5, 2026; public web March 23, 2026; API May 5, 2026
- Architecture: Decoder-only autoregressive transformer, unified text+image tokens
- Max resolution: 2048px
- Aspect ratios: 3:1, 2:1, 16:9, 3:2, 1:1, 2:3, 9:16, 1:2, 1:3 (9 options)
- Generation time: ~31 seconds per image
- Pricing: uni-1 = $0.04/img, uni-1-max = $0.10/img, references = $0.003 each
- Reference images: up to 9 per request
- Prompt length: up to 6,000 characters
- Reference role system (STYLE, CHARACTER, COMPOSITION, etc.)
- Output formats: JPG, PNG, WEBP
- Two API endpoints: create_image, modify_image
- Benchmarks: #1 Human Preference Elo (Overall, Style & Editing, Reference-Based)
- API docs at docs.agents.lumalabs.ai
- Python and JS/TS SDKs available

### Medium Confidence (found in developer/secondary sources; not directly verified against official API reference)
- `intent_weight` parameter (found in a developer integration guide; not confirmed in official Luma API docs page)
- `seed` parameter (standard for image models, mentioned in field guide, but exact parameter name not confirmed from API schema)
- Exact Python SDK method names (`client.generations.image.create`) -- pattern is consistent with Luma's existing SDK conventions but SDK docs were not directly read

### Low Confidence / Unconfirmed
- Whether `intent_weight` is currently in production API (marked [UNCONFIRMED] in draft)
- Provisioned throughput pricing ($2,100-$3,800/unit/month) -- from a developer guide, not official Luma pricing page; omitted from draft to avoid confusion
- Exact latency SLA for provisioned throughput

### Not Found / Missing
- Official benchmark comparison table (tech-specs page exists but content was from search summaries, not direct page read)
- Complete API request/response schema (available at docs.agents.lumalabs.ai but not directly fetched)
- Whether `lumaai` Python package (PyPI) was updated post-May 2026 to include `generations.image` methods or if a separate `lumaagents` package is required

---

## Proposed model-currency Row Addition

Add to the **Image Generation** section of `model-currency-2026-06.md`:

```
| `model-image-luma-uni-1.md` | Uni-1 (Mar 2026) | **Uni-1.1 API** (May 5 2026, now GA) | GA REST API: `create_image` + `modify_image`; 9-reference input; `uni-1` ($0.04/img) + `uni-1-max` ($0.10/img) tiers; 2048px max. |
```

---

## Notes for Reviewer

1. Fetch `https://lumalabs.ai/uni-1/tech-specs` directly to confirm 2048px max resolution and benchmark data.
2. Fetch `https://docs.agents.lumalabs.ai/` to verify exact API parameter names before publishing the doc -- specifically `intent_weight` and the method path for the Python SDK.
3. The `lumaai` vs `lumaagents` SDK split needs clarification. The existing Ray3 doc uses `requests` directly; consider doing the same here to avoid SDK naming ambiguity.
4. The doc correctly uses `model-image-` prefix (not `model-video-`) since Uni-1 is image-only.
