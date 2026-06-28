---
model: nemotron-cascade-2:30b
canonical_source:
  ollama_library: https://ollama.com/library/nemotron-cascade
  official_docs: https://developer.nvidia.com/blog/introducing-nemotron-3-super-an-open-hybrid-mamba-transformer-moe-for-agentic-reasoning/
provider: NVIDIA
architecture: Open MoE (MoE cascade), Nemotron-3-Nano variant; 30B total / ~3B active per token
context_window_max: 262144 (256K native)
quantization: Q4_K_M
size_bytes: ~25.2 billion
capabilities: [completion, tools, thinking] — text-only MoE model
recommended_parameters:
  temperature: (not specified by NVIDIA docs — use vLLM default: 1.0)
  top_p: (not specified by NVIDIA docs — commonly set to 0.95 for reasoning tasks per cookbook guidance)
  top_k: (not specified by NVIDIA docs — vLLM default: -1/unlimited)
additional_notes: |
  Configurable thinking budget via chat template flags (think/non-think).
  NVIDIA Open Model License Agreement. This model is text-only; vision/audio capabilities are available in the Nemotron3-33b "Nano Omni" variant.
  NVIDIA blog posts on Nemotron 3: https://developer.nvidia.com/blog/inside-nvidia-nemotron-3-techniques-tools-and-data-that-make-it-efficient-and-accurate/
---

model: nemotron3:33b
canonical_source:
  ollama_library: https://ollama.com/library/nemotron3
  official_docs: https://developer.nvidia.com/blog/nvidia-nemotron-3-nano-omni-powers-multimodal-agent-reasoning-in-a-single-efficient-open-model/
provider: NVIDIA
architecture: Hybrid Mamba-Transformer MoE (Mamba-2 + LatentMoE + Attention); Nemotron3-Nano-Omni variant
context_window_max: 131072 (128K) — also supports up to 1M tokens per official specs
quantization: Q4_K_M
size_bytes: ~29.3 billion
capabilities: [completion, vision, tools, thinking] — FULLY multimodal (images + audio/video reasoning + GUI understanding + OCR)
recommended_parameters:
  temperature: (not specified by NVIDIA docs — use vLLM default: 1.0)
  top_p: (not specified by NVIDIA docs — commonly set to 0.95 for reasoning tasks per cookbook guidance)
  top_k: (not specified by NVIDIA docs — vLLM default: -1/unlimited)
additional_notes: |
  The Nemotron3-Nano-Omni variant is the ONLY fully multimodal model in the Nemotron family (vision + audio + video + GUI/OCR).
  Configurable thinking budget via chat template flags. NVIDIA Open Model License Agreement.
---

model: nemotron3:33b-128k
canonical_source:
  ollama_library: https://ollama.com/library/nemotron3
  official_docs: https://developer.nvidia.com/blog/nvidia-nemotron-3-nano-omni-powers-multimodal-agent-reasoning-in-a-single-efficient-open-model/
provider: NVIDIA
architecture: Hybrid Mamba-Transformer MoE (same as nemotron3:33b)
context_window_max: 131072 (128K capped — variant explicitly caps context window)
quantization: Q4_K_M
size_bytes: ~29.3 billion
capabilities: [completion, vision, tools, thinking] — fully multimodal
recommended_parameters:
  temperature: (not specified by NVIDIA docs — use vLLM default: 1.0)
  top_p: (not specified by NVIDIA docs — commonly set to 0.95 for reasoning tasks per cookbook guidance)
  top_k: (not specified by NVIDIA docs — vLLM default: -1/unlimited)
additional_notes: |
  Explicit -128k suffix variant capping context window at 128K tokens (vs the native up-to-1M capability).
  Useful for constrained deployment scenarios where max context must be controlled.
---
