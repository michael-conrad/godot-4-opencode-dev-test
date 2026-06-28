# Godot 4 + OpenCode + Qwen Multi-Agent Orchestration

A local-only multi-agent system for Godot 4 game development using OpenCode and Ollama.

## Architecture

- **Orchestrator**: Qwen 3.6:35B (256K context)
- **12 Specialized Agents**: Dispatched based on task type
- **Embedding Service**: Qwen 3-Embedding:40K (Ollama API only, not an agent)
- **LLM Server**: Ollama (local inference)
- **Framework**: OpenCode (terminal-based AI assistant)

## Structure

```
ordestration/
├── agent-cards/          # 12 LLM agent capability profiles
├── utilities/            # Non-agent services (embeddings)
├── dispatch-rules.yaml   # Routing logic
├── orchestrator.py       # Main dispatch engine
└── ollama-client.py      # Ollama HTTP client

docs/
├── agent-system-architecture.md
├── dispatch-strategy.md
└── adding-new-agents.md

.opencode/commands/       # OpenCode custom commands
```

## Quick Start

1. Ensure Ollama is running locally on `http://localhost:11434`
2. All 12 models + embedding model are loaded
3. Run: `python3 orchestration/orchestrator.py --task "your task"`

## Models

**Main Orchestrator**:
- `ollama/qwen3.6:35b-256k`

**Agent Models**:
1. `ollama/qwen3-coder:30b-256k`
2. `ollama/devstral-small-2:24b-384k`
3. `ollama/nemotron3:33b-256k`
4. `ollama/laguna-xs.2:q4_K_M-256k`
5. `ollama/gpt-oss:20b-128k`
6. `ollama/gemma4:31b-256k`
7. `ollama/mistral-small3.2:24b-32k`
8. `ollama/granite4.1:30b-128k`
9. `ollama/qwen3.5:35b-256k`
10. `ollama/nemotron-cascade-2:30b-256k`
11. `ollama/qwen3.6:35b-256k` (alternate orchestrator)
12. (Additional model per your setup)

**Utility Services**:
- `ollama/qwen3-embedding:40k` (Ollama API only for semantic search)

## Documentation

- See `docs/agent-system-architecture.md` for detailed system design
- See `docs/dispatch-strategy.md` for routing logic
- See `docs/adding-new-agents.md` for onboarding new models
