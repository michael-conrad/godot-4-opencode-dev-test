---
card: 4
status: unresolved
topic: split-blob vision bug
affects: qwen35moe architecture with separate projector
bugs:
  - https://github.com/ollama/ollama/issues/14730
  - https://github.com/ollama/ollama/issues/14575
fix_pr: https://github.com/ollama/ollama/pull/14517
---

# Card 4: Split-Blob Vision Bug — qwen35moe + clip

## Bug
When a `qwen35moe` architecture GGUF is loaded with a **separate vision projector blob** (second FROM line), Ollama's multimodal runner fails.

## Reproduction
1. Download community Qwen 3.5/3.6 GGUF + separate mmproj file
2. Modelfile: two FROM lines (weights + projector)
3. `ollama create` → succeeds
4. `ollama run` → `500 Internal Server Error: unable to load model`

## Root Cause
PR #14517 fixed text-only `qwen35moe` loading in the LLM loader, but the **multimodal clip runner** was not updated. When a projector blob is present, Ollama routes through the clip runner, which encounters `qwen35moe` and cannot handle it.

Error state: `families: ['qwen35moe', 'clip']` → clip runner fails.

## Scope
ALL community GGUFs of Qwen 3.5-35B-A3B and 3.6-35B-A3B with separate projector blobs.

Official models work because vision tensors are embedded in the main GGUF.

## Affected Models (confirmed)
- `hf.co/unsloth/Qwen3.6-35B-A3B-GGUF:*` (any variant with mmproj)
- `hf.co/lmstudio-community/Qwen3.5-35B-A3B-GGUF:*`
- Any community quant with separate projector

## Workaround
Re-quantize the official single-blob model (see Card 2). Single blob → no clip runner path → bug not triggered.