---
model: llama3.2:3b
canonical_source:
  ollama_library: https://ollama.com/library/llama3.2
  official_docs: (NOT FOUND — all ai.meta.com URLs returned 400 errors during research)
provider: Meta AI
architecture: Llama-3.2 multilingual LLM (MoE architecture, 1B and 3B parameter sizes)
context_window_max: 131072 (128K tokens)
quantization: Q4_K_M
size_bytes: ~2.1 billion
capabilities: [completion, tools] — text-only; vision available in separate llama3.2-vision family
recommended_parameters:
  temperature: (NOT FOUND — not specified in accessible sources)
  top_p: (NOT FOUND — not specified in accessible sources)
  top_k: (NOT FOUND — not specified in accessible sources)
additional_notes: |
  Optimized for multilingual dialogue, agentic retrieval, and summarization.
  Apache 2.0 license. TikToken-based tokenizer. Supports English, German, French, Italian, Portuguese, Hindi, Spanish, Thai.
  NOTE: Recommended generation parameters not available from any accessible canonical source during research.
---
