---
card: 2
status: ready
model: qwen3.6:35b (official)
blob_main: sha256-f5ee307a2982106a6eb82b62b2c00b575c9072145a759ae4660378acda8dcf2d
quant: Q4_K_M
size: 23GB
capabilities: completion, tools, thinking, vision
---

# Card 2: Official qwen3.6:35b — Re-quantization Path

## GGUF Architecture

| Key | Value |
|-----|-------|
| Architecture | `qwen35moe` |
| Parameters | 36B (34.7B reported) |
| Context length | 262,144 |
| Embedding length | 2,048 |
| Expert count | 256 (8 routed + 1 shared) |
| Attention layers | 10 (3:1 DeltaNet:Attention ratio) |
| KV heads | 2, head dim 256 |
| Vision | Embedded (not split blob) |
| Tokenizer | 496,642 tokens |
| Quant | Q4_K_M (file_type=15) |

## Modelfile (from ollama show)

```
FROM /path/to/blob
TEMPLATE {{ .Prompt }}
RENDERER qwen3.5
PARSER qwen3.5
PARAMETER presence_penalty 1.5
PARAMETER repeat_penalty 1
PARAMETER temperature 1
PARAMETER top_k 20
PARAMETER top_p 0.95
PARAMETER min_p 0
```

## Re-quantization Options (via llama-quantize)

Requires `llama.cpp` build. System RAM: ~28GB needed.

KV cache at 256K: 10 layers × 2 heads × 256 dim × 2 bytes × 2 (K+V) × 262144 = ~5.1GB
Overhead: ~2GB (buffers, CLIP, scratch)
Available for weights: ~17GB

| Target Quant | Est. Weights | Total (256K ctx) | Fits 3090? |
|-------------|-------------|-------------------|-----------|
| Q4_K_M | 23GB | 30GB | ❌ |
| Q3_K_M | ~17GB | 24GB | ⚠️ Borderline |
| **Q3_K_S** | **~15GB** | **22GB** | **✅ Best** |
| IQ3_XXS | ~13GB | 20GB | ✅ Comfortable |
| IQ2_XXS | ~10GB | 17GB | ✅ Lots of room |

## Post-Quant Modelfile (single blob, no bug)

```
FROM /path/to/quantized-q3_k_s.gguf
TEMPLATE {{ .Prompt }}
RENDERER qwen3.5
PARSER qwen3.5
PARAMETER num_ctx 262144
PARAMETER presence_penalty 1.5
PARAMETER repeat_penalty 1
PARAMETER temperature 1
PARAMETER top_k 20
PARAMETER top_p 0.95
PARAMETER min_p 0
```

Single blob → clip runner never triggered → tools + thinking preserved.

## Official Sampling Parameters

| Mode | temp | top_p | top_k | min_p | presence_penalty | repeat_penalty |
|------|------|-------|-------|-------|-----------------|---------------|
| Thinking (general) | 1.0 | 0.95 | 20 | 0.0 | 1.5 | 1.0 |
| Thinking (coding) | 0.6 | 0.95 | 20 | 0.0 | 0.0 | 1.0 |
| Instruct (general) | 0.7 | 0.8 | 20 | 0.0 | 1.5 | 1.0 |
| Instruct (reasoning) | 1.0 | 0.95 | 40 | 0.0 | 2.0 | 1.0 |