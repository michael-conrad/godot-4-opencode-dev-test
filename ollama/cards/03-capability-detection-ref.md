---
card: 3
status: reference
topic: ollama capability detection
---

# Card 3: Ollama Capability Detection Reference

Source: [jonathanhecl/ollama-api-skill](https://github.com/jonathanhecl/ollama-api-skill/blob/main/ollama-api/references/modelfile-capability-unlock.md)

## Three Detection Signals

Ollama evaluates three independent signals at model load time:

| Signal | Method | Capability | How to Fix |
|--------|--------|-----------|-----------|
| GGUF metadata key | `vision.block_count > 0` | vision | Publisher-level GGUF injection |
| GGUF metadata key | `audio.block_count > 0` | audio | Publisher-level GGUF injection |
| GGUF metadata key | `pooling_type == "mean"` | embedding | Publisher-level GGUF injection |
| Template AST | `.Tools` field access node | tools | Rewrite Modelfile TEMPLATE |
| Template AST | `.Thinking` field access node | thinking | Rewrite Modelfile TEMPLATE |
| PARSER directive | Go parser `HasToolSupport()` | tools | Add `PARSER <arch>` to Modelfile |
| RENDERER directive | Go renderer handles formatting | tools (injection) | Add `RENDERER <arch>` to Modelfile |

## Known Parser/Renderer Families

| Architecture | Parser | Renderer | Tools | Thinking | Notes |
|-------------|--------|----------|-------|----------|-------|
| `qwen35moe`, `qwen35`, `qwen3.5` | `qwen3.5` | `qwen3.5` | Yes | Yes | Replace template with modern `.Messages` format for full API integration |
| `lfm2`, `lfm2moe` | `lfm2-thinking` | `lfm2-thinking` | Yes | Yes | Renderer handles all formatting internally |
| `gemma4` | `gemma4` | `gemma4` | Yes | Yes | Both required |
| `gemma3` | `gemma3` | — | Yes | No | Replace template |
| `gemma2` | `gemma2` | — | No | No | Basic chat |
| `gemma` | `gemma` | — | No | No | Basic chat |

## Template AST Rule

Ollama parses `TEMPLATE` as Go `text/template` and scans AST nodes. Detection is AST-level, NOT string-level. A comment containing `.Tools` does NOT trigger detection.

## Directives Quick Reference

| Directive | Purpose |
|-----------|---------|
| `PARSER <name>` | Selects built-in parser declaring tool/thinking support |
| `RENDERER <name>` | Selects built-in renderer handling prompt formatting and tool injection |
| `TEMPLATE` | Prompt template; modern format uses `.Messages`, `.Tools`, `.Thinking` |

## Known Bug: Modelfile Override (#14560)

When `FROM` references an existing Ollama model (tag name), children inherit the parent's `RENDERER`/`PARSER` and the new `TEMPLATE` is ignored.

**Workaround:** `FROM /path/to/blob/sha256-...` (raw blob path) instead of `FROM model:tag`.

Reference: https://github.com/ollama/ollama/issues/14560