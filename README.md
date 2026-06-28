# Godot 4 + OpenCode + Qwen Multi-Agent Orchestration

A local-only multi-agent system for Godot 4 game development using OpenCode and Ollama.

## Architecture

- **Orchestrator**: Qwen 3.6:35B (256K context)
- **12 Specialized Agents**: Dispatched based on task type
- **Embedding Service**: Qwen 3-Embedding:40K (Ollama API only, not an agent)
- **LLM Server**: Ollama (local inference, running as system service)
- **Framework**: OpenCode (terminal-based AI assistant)
- **Package Manager**: `uv` (fast Python package manager)

## Requirements

- Python 3.10+
- `uv` - [Install from here](https://github.com/astral-sh/uv)
- Ollama running as a system service on `http://localhost:11434`
  - All 12 models + embedding model must be loaded

## Quick Start

### 1. Ensure Ollama is running

```bash
# Ollama should be running as a system service
# Verify it's accessible:
curl http://localhost:11434/api/tags
```

### 2. Load required models (if not already)

```bash
ollama pull qwen3.6:35b-256k
ollama pull qwen3-coder:30b-256k
ollama pull devstral-small-2:24b-384k
ollama pull nemotron3:33b-256k
ollama pull laguna-xs.2:q4_K_M-256k
ollama pull gpt-oss:20b-128k
ollama pull gemma4:31b-256k
ollama pull mistral-small3.2:24b-32k
ollama pull granite4.1:30b-128k
ollama pull qwen3.5:35b-256k
ollama pull nemotron-cascade-2:30b-256k
ollama pull qwen3-embedding:40k
```

### 3. Run the orchestrator

```bash
# List all available agents
uv run orchestration/orchestrator.py --list-agents

# Dispatch a task (auto-selects best agent)
uv run orchestration/orchestrator.py --task "Write a GDScript player movement script"

# Interactive mode
uv run orchestration/orchestrator.py --interactive

# Force specific agent
uv run orchestration/orchestrator.py --task "your task" --agent qwen3-coder --verbose
```

## Project Structure

```
godot-4-opencode-dev-test/
├── README.md
├── .gitignore
├── pyproject.toml              # Python project config
├── uv.lock                     # Locked dependencies
├── orchestration/
│   ├── __init__.py
│   ├── orchestrator.py         # Main dispatch engine (PEP 723 script)
│   ├── ollama_client.py        # Ollama HTTP client (PEP 723 script)
│   ├── dispatch-rules.yaml     # Routing rules
│   ├── agent-cards/            # 12 agent capability profiles
│   │   ├── qwen3.6-orchestrator.yaml
│   │   ├── qwen3-coder.yaml
│   │   ├── devstral-small.yaml
│   │   ├── nemotron3.yaml
│   │   ├── laguna-xs.yaml
│   │   ├── gpt-oss.yaml
│   │   ├── gemma4.yaml
│   │   ├── mistral-small3.yaml
│   │   ├── granite4.1.yaml
│   │   ├── qwen3.5.yaml
│   │   └── nemotron-cascade.yaml
│   └── utilities/
│       └── qwen3-embedding.yaml (non-agent service)
├── docs/
│   ├── agent-system-architecture.md
│   ├── dispatch-strategy.md
│   └── adding-new-agents.md
└── .opencode/commands/
    └── dispatch-task.md
```

## Usage Examples

### Example 1: Code Generation

```bash
uv run orchestration/orchestrator.py --task "Write a GDScript script for player movement with WASD controls and diagonal movement support"
```

Auto-routes to: **Qwen 3-Coder** (specialized for code generation)

### Example 2: Game Design

```bash
uv run orchestration/orchestrator.py --task "Design a combat system for a top-down Godot game with classes: Warrior, Ranger, Mage"
```

Auto-routes to: **Qwen 3.6 Orchestrator** (coordination + design)

### Example 3: Code Review

```bash
uv run orchestration/orchestrator.py --task "Review this GDScript code for performance issues: [code snippet]"
```

Auto-routes to: **Nemotron 3** (verification + quality)

### Example 4: Fast Prototype

```bash
uv run orchestration/orchestrator.py --task "Quickly prototype a pause menu UI for Godot 4"
```

Auto-routes to: **Devstral Small** (384K context + speed)

## Agent Selection

The system automatically selects the best agent based on your task keywords:

| Keywords | Agent | Reason |
|----------|-------|--------|
| write, implement, code, script | Qwen 3-Coder | Specialized code generation |
| design, spec, architecture | Qwen 3.6 Orchestrator | Planning & coordination |
| review, verify, check, validate | Nemotron 3 | Verification |
| quick, fast, rapid, prototype | Devstral Small | Speed + 384K context |
| plan, decompose, organize | Qwen 3.6 Orchestrator | Multi-step reasoning |
| debug, fix, bug, error | Qwen 3-Coder | Code debugging |

## Documentation

- **[Agent System Architecture](docs/agent-system-architecture.md)** - Detailed system design
- **[Dispatch Strategy](docs/dispatch-strategy.md)** - How routing works with examples
- **[Adding New Agents](docs/adding-new-agents.md)** - Onboarding guide for new models

## Models

### Main Orchestrator
- **Qwen 3.6:35B** (256K context) - Multi-step reasoning, planning, game design

### Agent Models (11 alternatives)
1. **Qwen 3-Coder:30B** (256K) - Code generation & optimization
2. **Devstral Small:24B** (384K) - Fast prototyping
3. **Nemotron 3:33B** (256K) - Balanced verification
4. **Laguna-XS** (256K) - Lightweight/quantized
5. **GPT-OSS:20B** (128K) - General purpose
6. **Gemma 4:31B** (256K) - Instruction following
7. **Mistral Small 3.2:24B** (32K) - Ultra-fast
8. **Granite 4.1:30B** (128K) - Code-focused
9. **Qwen 3.5:35B** (256K) - Fallback general
10. **Nemotron Cascade-2:30B** (256K) - Multi-step reasoning
11. **Qwen 3-Embedding:40K** (Utility API-only, not an agent)

## Python Environment

This project uses `uv` for fast, reliable Python dependency management:

```bash
# Install dependencies
uv sync

# Run scripts with uv
uv run orchestration/orchestrator.py --list-agents

# Run tests
uv run pytest

# Format code
uv run black .

# Lint
uv run ruff check .
```

## Architecture Diagram

```
User Input (OpenCode)
       ↓
[Orchestrator]
  - Load agent cards
  - Parse task
  - Match dispatch rules
  - Select best agent
       ↓
[Dispatch Decision]
  - Keyword-based routing
  - Type-based dispatch
  - Fallback chains
       ↓
[Agent Selection]
  ┌─────────────────┬──────────────────┬──────────────┐
  │ Qwen 3-Coder    │ Nemotron 3       │ Devstral     │ ...
  │ (code spec)     │ (verification)   │ (fast)       │
  └─────────────────┴──────────────────┴──────────────┘
       ↓
[Ollama HTTP API]
  (local LLM inference)
       ↓
[Agent Model Processing]
  (optionally calls embedding service)
       ↓
[Return Result]
  (to User / OpenCode)
```

## Error Handling

- **Connection Error**: Retries up to 3 times with 2-second delays
- **Timeout**: Automatic retry with backoff
- **Agent Unavailable**: Falls back to next in chain
- **All Fallbacks Exhausted**: Hard failure with error message

## Performance

### Context Windows
- **Longest**: Devstral Small (384K) - for full codebase review
- **Standard**: Most agents (256K) - for typical tasks
- **Quick**: Mistral Small (32K), GPT-OSS (128K) - for fast operations

### Inference Speed
1. **Fastest**: Mistral Small (24B, 32K context)
2. **Fast**: Devstral Small (24B, 384K context)
3. **Medium**: Qwen 3-Coder, Nemotron (30-33B)
4. **Full-featured**: Qwen 3.6 (35B, comprehensive)

## Contributing

To add new agents or modify dispatch rules:
1. See [Adding New Agents](docs/adding-new-agents.md)
2. Create agent card in `orchestration/agent-cards/`
3. Update `orchestration/dispatch-rules.yaml`
4. Test with `uv run orchestration/orchestrator.py --list-agents`

## License

MIT
