---
model: qwen3-coder:30b
canonical_source:
  ollama_library: https://ollama.com/library/qwen3-coder
  official_docs: https://qwenlm.github.io/blog/qwen3/
provider: Qwen Team / Alibaba
architecture: Qwen3 MoE (30B total / ~3.3B active per token, 48 layers, 128 experts / 8 active)
context_window_max: 262144 (256K native; 1M with extrapolation)
quantization: Q4_K_M
size_bytes: ~19.2 billion
capabilities: [completion, tools] — text-only coding model
recommended_parameters:
  temperature: 0.7
  top_p: 0.8
  top_k: 20
additional_notes: |
  Qwen3-Coder variant specifically for code generation and agentic tasks.
  Apache 2.0 license. Uses stop tokens: </s>, """, and \n\n (as defined in Ollama modelfile).
  This is the text-only coding subset of the broader Qwen3 family.
---

model: qwen3.6:35b-256k
canonical_source:
  ollama_library: https://ollama.com/library/qwen3.6
  official_docs: https://qwenlm.github.io/blog/qwen3/
provider: Qwen Team / Alibaba
architecture: Qwen3 MoE (35B total / ~3.3B active, multimodal upgrade of Qwen3)
context_window_max: 262144 (256K native; 1M with extrapolation)
quantization: Q4_K_M
size_bytes: ~24.0 billion
capabilities: [completion, vision, tools, thinking]
recommended_parameters:
  temperature: 0.6
  top_p: 0.95
  top_k: 20
additional_notes: |
  Qwen3.6 multimodal variant — adds image input support to the Qwen3 text family.
  Vision-capable (Text + Image). This is the -256k context variant forcing max 256K window.
  Includes configurable thinking mode and reasoning capabilities.
---

model: qwen3.6:35b
canonical_source:
  ollama_library: https://ollama.com/library/qwen3.6
  official_docs: https://qwenlm.github.io/blog/qwen3/
provider: Qwen Team / Alibaba
architecture: Qwen3 MoE (same weights as -256k variant)
context_window_max: 262144 (256K native; 1M with extrapolation)
quantization: Q4_K_M
size_bytes: ~24.0 billion
capabilities: [completion, vision, tools, thinking]
recommended_parameters:
  temperature: 0.6
  top_p: 0.95
  top_k: 20
additional_notes: |
  Same model weights as qwen3.6:35b-256k but may use different default context window in Ollama.
  The -256k suffix variant was created to force the max context window; this default variant should have equivalent specs.
---

model: qwen3.5:35b
canonical_source:
  ollama_library: https://ollama.com/library/qwen3.5
  official_docs: https://qwenlm.github.io/blog/qwen3/
provider: Qwen Team / Alibaba
architecture: Qwen3 MoE (multimodal preview variant)
context_window_max: 262144 (256K native)
quantization: Q4_K_M
size_bytes: ~24.0 billion
capabilities: [completion, vision, tools, thinking]
recommended_parameters:
  temperature: 1.0
  top_p: 0.95
  top_k: 20
additional_notes: |
  Multimodal preview variant within the Qwen3 family lineage.
  Supports vision input and configurable thinking mode.
  Note: This model predates the finalized qwen3.6 release; use qwen3.6 for production where possible.
---
