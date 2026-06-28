# Multi-Agent Orchestration System Architecture

## Overview

A specialized multi-agent dispatch system for Godot 4 game development that routes tasks to 12 different LLM agents based on capability profiles.

## Core Concepts

### Agents

12 LLM models with different strengths:

| Agent | Model | Best For | Context |
|-------|-------|----------|----------|
| Qwen 3.6 Orchestrator | 35B | Coordination, design, planning | 256K |
| Qwen 3-Coder | 30B | Code generation, implementation | 256K |
| Devstral Small | 24B | Fast prototyping, long context | 384K |
| Nemotron 3 | 33B | Verification, balanced tasks | 256K |
| Laguna-XS | Q4 Quant | Lightweight, resource-constrained | 256K |
| GPT-OSS | 20B | General purpose, quick tasks | 128K |
| Gemma 4 | 31B | Instruction following | 256K |
| Mistral Small 3.2 | 24B | Ultra-fast responses | 32K |
| Granite 4.1 | 30B | Code-focused reasoning | 128K |
| Qwen 3.5 | 35B | Fallback general purpose | 256K |
| Nemotron Cascade-2 | 30B | Multi-step reasoning | 256K |

### Utilities (Non-Agents)

**Qwen 3-Embedding:40K** - NOT an agent
- Ollama API-only service
- Used for semantic search and embeddings
- Called on-demand by agents
- Accessed via `/api/embeddings` endpoint

## Architecture Components

```
┌─────────────────────────────────────────────────────────────┐
│                     User Input (OpenCode)                    │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                Orchestrator (Dispatcher)                     │
│  - Loads agent cards                                        │
│  - Parses task description                                  │
│  - Matches against dispatch rules                           │
│  - Selects best agent                                       │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│           Dispatch Rules Engine                             │
│  - Keyword-based routing                                    │
│  - Type-based dispatch                                      │
│  - Fallback chains                                          │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│           Agent Selection & Invocation                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Qwen3-Coder  │  │  Nemotron3   │  │  Dev Small   │ ... │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              Ollama HTTP API                                │
│  (local LLM inference server)                               │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│         Agent Model Processing + Optional Embedding         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  If semantic search needed:                          │  │
│  │  → Call Qwen3-Embedding:40K via /api/embeddings     │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Return Result                            │
│                  (to User / OpenCode)                       │
└─────────────────────────────────────────────────────────────┘
```

## Dispatch Logic

### Deterministic Routing

1. **Keyword Matching** (first pass)
   - "write", "implement", "code" → Qwen 3-Coder
   - "design", "spec", "architecture" → Qwen 3.6 Orchestrator
   - "review", "verify", "check" → Nemotron 3
   - "fast", "quick", "rapid" → Devstral Small

2. **Type-Based Routing** (if no keyword match)
   - Code generation → Qwen 3-Coder
   - Game design → Qwen 3.6 Orchestrator
   - Verification → Nemotron 3
   - Planning → Qwen 3.6 Orchestrator

3. **Fallback Chain**
   - Primary agent unavailable?
   - Try fallback agents in order
   - Hard failure if all unavailable

### Uncertainty Handling

When task doesn't match any rule:
1. Use **Nemotron 3** (balanced agent)
2. Falls back to **Qwen 3.6 Orchestrator**
3. Logs reasoning for manual review

## Agent Card Format

Each agent has a YAML profile:

```yaml
name: "Model Name"
model: "ollama/model-id"
role: "Primary responsibility"
context_window: 262144

strengths:
  - "What it's good at"
  - "Another strength"

capabilities:
  can_generate_code: true
  can_reason: true
  can_verify: true

weaknesses:
  - "What it struggles with"

best_for:
  - "Use case 1"
  - "Use case 2"

worst_for:
  - "Avoid this"

dispatch_criteria:
  - "When to select this agent"

fallback_chain:
  - "primary-fallback"
  - "secondary-fallback"
```

## Using the Embedding Service

Agents can call the embedding service for semantic operations:

```python
from ollama_client import OllamaClient

client = OllamaClient()
vector = client.embed(
    model="qwen3-embedding:40k",
    text="Code snippet to embed"
)
```

Use cases:
- Finding similar code patterns
- Compressing conversation history
- Semantic search over documentation
- Context retrieval

## Configuration

### Ollama

Ensure Ollama is running:
```bash
ollama serve
```

All models must be available:
```bash
ollama list  # Verify all models are loaded
```

### Orchestrator

Modify `dispatch-rules.yaml` to add new routing rules or adjust fallback chains.

## Error Handling

- **Timeout**: Retry up to 3 times with 2-second delays
- **Connection Error**: Retry with backoff
- **Model Unavailable**: Use fallback chain
- **All Fallbacks Exhausted**: Hard failure with error message

## Performance Considerations

### Context Window Selection

- **Long-context code review**: Devstral Small (384K)
- **General tasks**: Qwen 3.6 / Nemotron (256K)
- **Quick operations**: Mistral Small (32K) or GPT-OSS (128K)
- **Embeddings**: Qwen 3-Embedding (40K, API-only)

### Inference Speed

1. **Fastest**: Mistral Small (24B, 32K context)
2. **Fast**: Devstral Small (24B, 384K context)
3. **Medium**: Qwen 3-Coder, Nemotron (30-33B)
4. **Full-featured**: Qwen 3.6 (35B, comprehensive)

### Quality vs. Speed Tradeoff

- **Speed-critical**: Use smaller models (Devstral, Mistral)
- **Quality-critical**: Use larger models (Qwen 3.6, Nemotron)
- **Balanced**: Use Nemotron 3

## Future Enhancements

- [ ] Agent performance tracking (latency, accuracy, cost)
- [ ] Dynamic routing based on historical performance
- [ ] Multi-agent collaboration for complex tasks
- [ ] Rate limiting and quota management
- [ ] Caching of embeddings and common responses
- [ ] Agent health monitoring and self-healing
