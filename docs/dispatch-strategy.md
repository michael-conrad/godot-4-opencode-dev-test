# Dispatch Strategy Guide

How the orchestrator selects agents and routes tasks.

## Task Classification

Every task falls into one of these categories:

### 1. Code Generation
- "Write a GDScript script for..."
- "Implement the player movement..."
- "Create a UI component..."
- **Primary**: Qwen 3-Coder
- **Reasoning**: Specialized for code generation

### 2. Game Design
- "Design the combat system..."
- "Write a spec for..."
- "Define the architecture..."
- **Primary**: Qwen 3.6 Orchestrator
- **Reasoning**: Needs cross-domain coordination

### 3. Code Review & Verification
- "Review this code for..."
- "Check if this implementation..."
- "Verify that the design..."
- **Primary**: Nemotron 3
- **Reasoning**: Strong verification capabilities

### 4. Fast Prototyping
- "Quickly mock up a UI screen..."
- "Rapid prototype a game mechanic..."
- **Primary**: Devstral Small
- **Reasoning**: 384K context + fast inference

### 5. Planning & Decomposition
- "Break down this feature..."
- "Plan the implementation..."
- "Coordinate the following tasks..."
- **Primary**: Qwen 3.6 Orchestrator
- **Reasoning**: Excels at multi-step reasoning

### 6. Debugging
- "Fix this bug in..."
- "Why is this code failing..."
- "Debug the following error..."
- **Primary**: Qwen 3-Coder
- **Reasoning**: Code-specialized debugging

## Keyword Detection

The dispatcher uses keyword matching for quick routing:

```
Keywords → Primary Agent
─────────────────────────
write → qwen3-coder
implement → qwen3-coder
code → qwen3-coder
script → qwen3-coder

design → qwen3.6-orchestrator
spec → qwen3.6-orchestrator
architecture → qwen3.6-orchestrator
system → qwen3.6-orchestrator

review → nemotron3
verify → nemotron3
check → nemotron3
validate → nemotron3

quick → devstral-small
fast → devstral-small
rapid → devstral-small
prototype → devstral-small

plan → qwen3.6-orchestrator
decompose → qwen3.6-orchestrator
organize → qwen3.6-orchestrator

debug → qwen3-coder
fix → qwen3-coder
bug → qwen3-coder
error → qwen3-coder
```

## Routing Decision Tree

```
Incoming Task
    ↓
[Match Keywords?]
    ├─ YES → Use matched agent
    └─ NO → Continue
        ↓
    [Match Type-based Rules?]
        ├─ YES → Use type agent
        └─ NO → Continue
            ↓
        [Uncertainty]
            └─ Use Nemotron 3 (fallback)
```

## Context Size Considerations

### When to Use High Context Models

**Devstral Small (384K)**:
- Full codebase review (>256K tokens)
- Complete file history review
- Long conversation threads

**Qwen/Nemotron (256K)**:
- Most general tasks
- Medium-large code reviews
- Long-form documentation

**GPT-OSS/Mistral (32K-128K)**:
- Quick operations
- Small code snippets
- Brief documentation

## Temperature & Sampling

### Low Temperature (0.3-0.4) - Deterministic
Used for:
- Code generation (correctness critical)
- Debugging (precise solutions needed)
- Verification (factual accuracy needed)

**Agents**: Qwen 3-Coder (0.3), Granite 4.1 (0.4)

### Medium Temperature (0.5-0.6) - Balanced
Used for:
- General purpose tasks
- Balanced reasoning + creativity
- Design discussions

**Agents**: Nemotron 3 (0.6), Gemma 4 (0.5), GPT-OSS (0.5)

### High Temperature (0.7) - Creative
Used for:
- Brainstorming
- Creative writing
- Exploratory design

**Agents**: Qwen 3.6 (0.7), Qwen 3.5 (0.6)

## Fallback Chains

If the primary agent is unavailable:

1. **Code Generation**:
   - Primary: Qwen 3-Coder
   - Fallback: Devstral Small → Qwen 3.6

2. **Design/Planning**:
   - Primary: Qwen 3.6 Orchestrator
   - Fallback: Nemotron 3 → Nemotron Cascade

3. **Verification**:
   - Primary: Nemotron 3
   - Fallback: Qwen 3.6 → Qwen 3.5

4. **Fast Prototyping**:
   - Primary: Devstral Small
   - Fallback: Mistral Small → Qwen 3-Coder

5. **General (Uncertain)**:
   - Primary: Nemotron 3
   - Fallback: Qwen 3.6 → Qwen 3-Coder

## Performance Metrics by Agent

| Agent | Speed | Quality | Versatility | Context |
|-------|-------|---------|-------------|----------|
| Qwen 3-Coder | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | 256K |
| Devstral Small | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | 384K |
| Nemotron 3 | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 256K |
| Qwen 3.6 | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 256K |
| Mistral Small | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐ | 32K |
| Laguna-XS | ⭐⭐⭐⭐ | ⭐⭐ | ⭐ | 256K |

## Custom Routing Examples

### Example 1: Write Player Movement Script
```
Task: "Write a GDScript script for player movement with WASD controls"
Keywords: "Write" + "script" + "GDScript"
Route: qwen3-coder
Reason: Code generation + GDScript specialization
```

### Example 2: Design Combat System
```
Task: "Design a combat system for a top-down ARPG with 3 classes"
Keywords: "Design"
Route: qwen3.6-orchestrator
Reason: Design coordination + multi-domain reasoning
```

### Example 3: Fast UI Prototype
```
Task: "Quickly prototype a pause menu UI for Godot 4"
Keywords: "Quickly" + "prototype"
Route: devstral-small
Reason: Speed + 384K context for full game context
```

### Example 4: Code Review Full Codebase
```
Task: "Review this entire player.gd file (25KB) for performance"
Context: > 256K tokens needed
Route: devstral-small
Reason: Only model with 384K context window
Fallback: qwen3-coder (truncate context)
```

## Adding New Dispatch Rules

1. Edit `orchestration/dispatch-rules.yaml`
2. Add rule to `keyword_routing` section:
   ```yaml
   - keywords: ["your", "keywords"]
     primary: "target-agent"
   ```
3. Or add to `dispatch_rules` section for complex logic
4. Restart orchestrator

## Monitoring & Debugging

Enable verbose logging:
```bash
python3 orchestration/orchestrator.py --task "..." --verbose
```

Check dispatch decision:
- Logs show matched keyword
- Logs show selected agent
- Logs show fallback chain if needed

List all agents:
```bash
python3 orchestration/orchestrator.py --list-agents
```

Force specific agent:
```bash
python3 orchestration/orchestrator.py --task "..." --agent qwen3-coder
```
