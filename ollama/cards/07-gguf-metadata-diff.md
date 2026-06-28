---
card: 7
status: reference
topic: GGUF metadata comparison
models:
  official: sha256-f5ee307a2982106a6eb82b62b2c00b575c9072145a759ae4660378acda8dcf2d
  iq4_nlx: sha256-071ee2a008ec51372f990d8efbea92ec9dd0137974110ef68fbfde429c8c6dd4
---

# Card 7: GGUF Metadata — Official vs IQ4_NL_XL Diff

## Tool Tokens Present in BOTH
```
<tool_call>  [496119]
</tool_call> [496121]
<tool_response> [496135]
</tool_response> [496137]
```
Identical indices, identical values.

## Present in Official, MISSING in IQ4_NL_XL

### Architecture
- `general.parameter_count`
- `qwen35moe.feed_forward_length`
- `qwen35moe.image_token_id`
- `qwen35moe.vision_start_token_id`
- `qwen35moe.vision_end_token_id`
- All `qwen35moe.vision.*` keys (embedded in official, separate projector in Unsloth)
- `qwen35moe.rope.mrope_interleaved` (redundant — `mrope_sections` exists in both)
- `qwen35moe.rope.mrope_section` (redundant — `mrope_sections` exists in both)

### Tokenizer
- `tokenizer.ggml.add_eos_token`
- `tokenizer.ggml.add_padding_token`
- `tokenizer.ggml.eos_token_ids` (plural — IQ4 has `bos_token_id` instead)
- `tokenizer.ggml.scores`

## Present in IQ4_NL_XL, MISSING in Official
- `general.base_model.*` (name, organization, repo_url)
- `general.license`, `general.license.link`
- `general.quantized_by`, `general.repo_url`
- `general.name`, `general.basename`, `general.size_label`, `general.type`
- `general.sampling.*` (temp, top_k, top_p)
- `general.tags`
- `quantize.imatrix.*` (chunks_count, dataset, entries_count, file)
- `tokenizer.ggml.add_bos_token`
- `tokenizer.ggml.bos_token_id`

## Token Type Array Difference
Official: 248,322 entries (half of 496,642 tokens)
IQ4_NL_XL: different size — confirms different quantization pipeline metadata handling

## Key Takeaway
Tool tokens are identical. Tokenizer vocab is identical. The `tools` capability gap is purely a Modelfile-level flag issue, compounded by the split-blob loading bug. No weights or tokenizer data differs in a way that affects tool calling capability.