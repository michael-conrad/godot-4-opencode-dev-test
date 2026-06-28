---
card: 6
status: reference
topic: Qwen 3.6-35B-A3B sampling parameters
source: https://huggingface.co/Qwen/Qwen3.6-35B-A3B
---

# Card 6: Qwen 3.6-35B-A3B — Sampling Parameters

## Thinking Mode (General Tasks)
```
temperature=1.0, top_p=0.95, top_k=20, min_p=0.0
presence_penalty=1.5, repetition_penalty=1.0
```

## Thinking Mode (Precise Coding)
```
temperature=0.6, top_p=0.95, top_k=20, min_p=0.0
presence_penalty=0.0, repetition_penalty=1.0
```

## Instruct/Non-Thinking (General)
```
temperature=0.7, top_p=0.8, top_k=20, min_p=0.0
presence_penalty=1.5, repetition_penalty=1.0
```

## Instruct/Non-Thinking (Reasoning)
```
temperature=1.0, top_p=0.95, top_k=40, min_p=0.0
presence_penalty=2.0, repetition_penalty=1.0
```

## Thinking Preservation
Qwen 3.6 supports retaining reasoning context across multi-turn conversations:
```
extra_body: {"chat_template_kwargs": {"preserve_thinking": true}}
```

## Tool Calling
Uses `qwen3_coder` tool-call parser. Ollama's `qwen3.5` PARSER handles it.

## Recommended Output Length
- Most queries: 32,768 tokens
- Complex math/programming: 81,920 tokens