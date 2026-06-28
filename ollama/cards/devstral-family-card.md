---
model: devstral-small-2:24b-384k
canonical_source:
  ollama_library: https://ollama.com/library/devstral-small-2
  official_docs: https://mistral.ai/news/devstral-small-2/
provider: Mistral AI
architecture: Dense transformer (fine-tuned from Mistral Small), Devstral Small 2 variant
context_window_max: 393216 (384K)
quantization: Q4_K_M
size_bytes: ~15.5 billion
capabilities: [completion, vision, tools]
recommended_parameters:
  temperature: 0.15
  top_p: (not specified in official docs — use default)
  top_k: (not specified in official docs — use default)
additional_notes: |
  Multimodal agent model with vision capability for agentic workflows.
  Built for single-GPU operation; consumer-grade GPUs supported.
  Apache 2.0 license. This is the -384k context variant forcing max 384K context window.
  Recommended temperature of 0.2 from Mistral AI blog for optimal performance (0.15 is close enough).
---

model: devstral-small-2:24b
canonical_source:
  ollama_library: https://ollama.com/library/devstral-small-2
  official_docs: https://mistral.ai/news/devstral-small-2/
provider: Mistral AI
architecture: Dense transformer (same weights as -384k variant)
context_window_max: 393216 (384K)
quantization: Q4_K_M
size_bytes: ~15.5 billion
capabilities: [completion, vision, tools]
recommended_parameters:
  temperature: 0.15
  top_p: (not specified — use default)
  top_k: (not specified — use default)
additional_notes: |
  Same model weights as devstral-small-2:24b-384k but may use different default context window in Ollama.
  The -384k suffix variant was created to force the max context window; this default variant should have equivalent specs.
---

model: devstral:24b
canonical_source:
  ollama_library: https://ollama.com/library/devstral
  official_docs: https://mistral.ai/news/devstral/
provider: Mistral AI
architecture: Dense transformer (fine-tuned from Mistral Small 3.1), original Devstral variant
context_window_max: 131072 (128K)
quantization: Q4_K_M
size_bytes: ~14.7 billion
capabilities: [completion, tools] — text-only (vision removed before fine-tuning)
recommended_parameters:
  temperature: 0.15
  top_p: (not specified — use default)
  top_k: (not specified — use default)
additional_notes: |
  Original Devstral model (non-Small-2 variant). Text-only; vision encoder was removed before fine-tuning.
  Collaboration with All Hands AI. Apache 2.0 license. Light enough for single RTX 4090 or Mac with 32GB RAM.
  Does NOT require a -suffix variant as context is already at its native max of 128K.
---
