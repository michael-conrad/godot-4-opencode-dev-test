---
model: gemma4:31b-256k
canonical_source:
  ollama_library: https://ollama.com/library/gemma4
  official_docs: https://ai.google.dev/gemma/docs/core/model_card_4
provider: Google DeepMind
architecture: Dense Transformer, gemma4 family (30.7B total params, 60 layers, sliding window 1024)
context_window_max: 262144
quantization: Q4_K_M
size_bytes: ~20.4 billion
capabilities: [completion, vision, tools, thinking]
recommended_parameters:
  temperature: 1.0
  top_p: 0.95
  top_k: 64
additional_notes: |
  Vision-capable (text + image input). Audio encoder NOT available on 31B variant.
  Supports configurable visual token budget (70, 140, 280, 560, 1120 tokens).
  Native thinking mode via <|think|> control token and reasoning mode.
  This is the -256k context variant: forces max 256K context window.
---

model: gemma4:31b
canonical_source:
  ollama_library: https://ollama.com/library/gemma4
  official_docs: https://ai.google.dev/gemma/docs/core/model_card_4
provider: Google DeepMind
architecture: Dense Transformer, gemma4 family (same weights as -256k variant)
context_window_max: 262144
quantization: Q4_K_M
size_bytes: ~20.4 billion
capabilities: [completion, vision, tools, thinking]
recommended_parameters:
  temperature: 1.0
  top_p: 0.95
  top_k: 64
additional_notes: |
  Same model weights as gemma4:31b-256k but may use different default context window in Ollama.
  The -256k suffix variant was created to force the max context window; this default variant should have equivalent specs.
---
