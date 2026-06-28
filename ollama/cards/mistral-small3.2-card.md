---
model: mistral-small3.2:24b
canonical_source:
  ollama_library: https://ollama.com/library/mistral-small3.2
  official_docs: https://mistral.ai/models/mistral-small-3/
provider: Mistral AI
architecture: Dense transformer, mistral3 family (24B parameters)
context_window_max: 131072 (128K tokens)
quantization: Q4_K_M
size_bytes: ~15.7 billion
capabilities: [completion, vision, tools] — multimodal with image input support
recommended_parameters:
  temperature: 0.15 (explicitly recommended by Mistral AI in "Usage" section of HF model card)
  top_p: (not specified — use default)
  top_k: (not specified — use default)
additional_notes: |
  Mistral Small 3.2 is a compact multimodal model optimized for agentic and coding workflows.
  Apache 2.0 license. Requires vLLM for optimal deployment per Mistral docs.
  NOTE: Temperature of 0.15 is notably low — this model is optimized for deterministic, precise output rather than creative generation.
---
