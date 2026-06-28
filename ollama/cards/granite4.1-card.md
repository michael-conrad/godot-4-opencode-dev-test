---
model: granite4.1:30b
canonical_source:
  ollama_library: https://ollama.com/library/granite4.1
  official_docs: https://www.ibm.com/granite/docs/
provider: IBM (Granite Team)
architecture: Dense decoder-only (non-MoE, non-Mamba); Granite-4.1 family
context_window_max: 131072 (128K operational default; training extended to 512K via long-context phase)
quantization: Q4_K_M
size_bytes: ~18.0 billion
capabilities: [completion, tools] — natively supports function-calling and tool usage
recommended_parameters:
  temperature: 0 (explicitly recommended by IBM Granite docs: "temperature set to 0 for most inferencing tasks")
  top_p: NOT specified in official IBM docs
  top_k: NOT specified in official IBM docs
additional_notes: |
  Granite-4.1 family includes three sizes (3B, 8B, 30B); all available as base and instruct variants.
  Apache 2.0 license. Tool-calling capability confirmed from both ollama.com library page and IBM GitHub README.
  NOTE: temperature=0 means deterministic output — use higher values only for creative/creative tasks.
---
