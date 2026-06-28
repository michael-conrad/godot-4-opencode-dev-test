---
model: laguna-xs.2:q4_K_M
canonical_source:
  ollama_library: https://ollama.com/library/laguna-xs.2
  official_docs: https://poolside.ai/blog/laguna-a-deeper-dive
provider: Poolside (Laguna family)
architecture: Laguna MoE (33B total / 3B activated per token, 40 layers — 10 global + 30 SWA, 256 experts + 1 shared expert, FP8 KV cache)
context_window_max: 262144 (262K per HF model card; Ollama pins at 128K operational default)
quantization: Q4_K_M
size_bytes: ~24.7 billion
capabilities: [completion, tools, thinking] — text-only MoE model
recommended_parameters:
  temperature: 0.7
  top_p: (not specified in official docs — use default)
  top_k: 20
additional_notes: |
  Open-source agent model from Poolside. Apache 2.0 license.
  This is the XS v2 variant — lightweight but powerful for agentic tasks on consumer hardware.
  NOTE: Official HF card states 262K context, but Ollama pins it at 128K operational default.
---
