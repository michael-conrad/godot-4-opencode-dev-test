---
model: gpt-oss:20b-128k
canonical_source:
  ollama_library: https://ollama.com/library/gpt-oss
  official_docs: https://openai.com/index/introducing-gpt-oss
provider: OpenAI (Ollama partnership)
architecture: Transformer MoE (NOT standard GPT architecture — uses grouped multi-query attention, alternating dense/sparse layers, Rotary Positional Embeddings; MxFP4 quantization of MoE weights at 4.25 bits/param)
context_window_max: 131072 (128K tokens) for BOTH variants
quantization: MXFP4 (post-training quantized)
size_bytes: ~13.6 billion
capabilities: [completion, tools, thinking] — text-only agentic model (no vision)
recommended_parameters:
  temperature: 0.8 to 1.0 (open-ended; vLLM guide uses 0.8-1.0 depending on use case)
  top_p: 0.95 (from NVIDIA TensorRT-LLM example in OpenAI Cookbook)
  top_k: NOT specified by OpenAI docs (not mentioned as a recommended parameter)
additional_notes: |
  CRITICAL: Requires Harmony response format — model will NOT work correctly without it.
  Reasoning effort controlled via system message: "Reasoning: high/medium(default)/low"
  Apache 2.0 license. Uses special tokens: <|return|>, <|call|>, <|channel|>, etc.
  This is the -128k context variant capping max window at 128K (same as default).
---

model: gpt-oss:20b
canonical_source:
  ollama_library: https://ollama.com/library/gpt-oss
  official_docs: https://openai.com/index/introducing-gpt-oss
provider: OpenAI (Ollama partnership)
architecture: Transformer MoE (same as -128k variant)
context_window_max: 131072 (128K tokens)
quantization: MXFP4 (post-training quantized)
size_bytes: ~13.6 billion
capabilities: [completion, tools, thinking] — text-only agentic model (no vision)
recommended_parameters:
  temperature: 0.8 to 1.0
  top_p: 0.95
  top_k: NOT specified by OpenAI docs
additional_notes: |
  Same model weights as gpt-oss:20b-128k; -128k suffix was used to force max context window.
  Requires Harmony response format for correct operation.
---
