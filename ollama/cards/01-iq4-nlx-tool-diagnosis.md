---
card: 1
status: unresolved
model: qwen3.6-35b-a3b-iq4_nlx:256k
source: unsloth/Qwen3.6-35B-A3B-GGUF:IQ4_NL_XL
blob_main: sha256-071ee2a008ec51372f990d8efbea92ec9dd0137974110ef68fbfde429c8c6dd4 (19G)
blob_projector: sha256-356dfaa3111376a4f7165e32e8749713378d1700b37cf52e0c50d9f23322334d (861M)
---

# Card 1: IQ4_NL_XL Tool Support Diagnosis

## Symptom
`ollama show` reports only `completion` + `vision`. No `tools` or `thinking` capabilities flagged, despite the model weights containing all tool tokens (`<tool_call>`, `</tool_call>`, etc.).

## Root Cause

Ollama detects capabilities via three signals. This model fails on two:

| Signal | Status |
|--------|--------|
| GGUF metadata (tool tokens) | ✅ Present at indices 496119-496137 |
| Template variables (.Tools/.Thinking) | ❌ Uses legacy `.Prompt`/`.Response` |
| PARSER/RENDERER directives | ❌ Not present in Modelfile |

## Attempted Fix

Added to Modelfile:
```
RENDERER qwen3.5
PARSER qwen3.5
TEMPLATE {{ .Prompt }}
```

`ollama show` then reported `tools` + `thinking`. But `ollama run` failed with:
```
500 Internal Server Error: unable to load model
```

## Why It Fails

Known Ollama bug [#14730](https://github.com/ollama/ollama/issues/14730): When a `qwen35moe` GGUF uses a **separate vision projector blob** (second `FROM` line), Ollama's multimodal clip runner cannot handle the `qwen35moe` architecture. Error in logs: `unknown model architecture: 'qwen35moe'`.

The official model works because vision tensors are **embedded in the main GGUF** — single blob, no clip runner path triggered.

## Status: UNRESOLVED

No fix available until Ollama patches the clip runner for `qwen35moe`. Workaround: re-quantize the official single-blob model (see Card 2).

## References
- https://github.com/ollama/ollama/issues/14730
- https://github.com/ollama/ollama/issues/14575
- https://github.com/ollama/ollama/pull/14517