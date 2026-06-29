# AGENTS.md — Spec-Driven AI Agent Development Setup

## Project Context

This project uses OpenCode as the AI agent framework for spec-driven development. LLM inference runs via Ollama (model configurable per section below). The goal is to build a game / application through autonomous agent workflows with full traceability from user intent → spec → implementation → verification.

### Primary Workflow

1. **Read this file** on every session start
2. **Read docs/cards/catalogue.md** to understand active research context
3. **Follow the spec-driven development loop**: user intent → spec proposal → approval → implementation → verification → review
4. Never skip tests before implementing code
5. Always verify in the editor (headless or visual) before claiming work is done

### Project Structure

```
<PROJECT_NAME>/                 ← repo root
├── AGENTS.md                   ← you are reading this file
├── CHANGELOG.md                ← progress tracking, updated after every merge
├── opencode.jsonc              ← OpenCode config: models, MCP servers
├── docs/
│   ├── cards/                  ← research card system (ALWAYS read catalogue first)
│   │   └── catalogue.md        ← active cards index with cross-references
│   ├── templates/              ← CARD.md, CHANGELOG-template.md, etc.
│   ├── AGENTS.md               ← docs-level agent instructions
│   └── specs/                  ← game design specifications (generated during development)
├── .opencode/
│   ├── agents/                 ← per-model agent cards — orchestrator delegates to specialist
│   ├── skills/                 ← on-demand skill definitions
│   └── commands/               ← custom opencode commands
├── <GAME_DIR>/                 ← application root (language-specific structure)
│   ├── scenes/                 ← scene files
│   ├── scripts/                ← source code
│   └── assets/                 ← textures, audio, fonts
└── ollama/                     ← Ollama Modelfile configs for available models
```

## Agent Architecture — Orchestrator Pattern

The orchestrator (primary model) is the single entry point. It delegates to specialist subagents based on task type. Each model has its own agent card describing what it's genuinely good at:

| Model | Native Context | Verified Capability | Agent Card |
|-------|---------------|--------------------|------------|
| `<ORCHESTRATOR_MODEL>` | `<context_window>` | General-purpose reasoning (orchestrator) | `build.md` |
| `<MODEL_2>` | `<context_window>` | <capability> | `<agent-card-2>.md` |
| `<MODEL_3>` | `<context_window>` | <capability> | `<agent-card-3>.md` |

The orchestrator assesses each incoming task and routes to the best-fit model. If no specialist clearly fits, it handles the task itself. Agent cards describe capabilities — they are not personas or fixed roles.

See `.opencode/agents/*.md` for full agent card contents. Switch agents with Tab in TUI or @mention them.

## MCP Integration

### <MCP_SERVER_NAME> Plugin

The `<MCP_SERVER_NAME>` plugin exposes `<N>+` MCP tools over **<transport>** at `<server_url>`. To use it:

1. Install the plugin into your application project as `<install_path>`
2. Open the application in `<editor>` → enable the plugin in Project Settings → Plugins
3. The editor starts a server on `<port>` automatically
4. Configure OpenCode's MCP config to connect to that URL (type: `"<http|stdio>"`)

When implementing features with agents, they use these tools:

1. `<TOOL_1>` — verify existing structure
2. `<TOOL_2>` / `<TOOL_3>` — build scenes/objects programmatically  
3. `<TOOL_4>` — visual verification
4. `<TOOL_5>` — catch syntax errors before running
5. `<TOOL_6>` — logic verification

See CARD-XXX for full tool list and setup details.

<!-- END OF MCP INTEGRATION SECTION -->

## Git Workflow

Branching follows GitHub Flow style: one `feature/xxx` branch per spec, squash-merged to `main`. No tags at this stage — progress tracked via CHANGELOG.md and conventional commits.

**Branch naming**: `feature/<short-descriptive-name>` (e.g., `feature/card-system`, `feature/script-validator`)

**Merge method**: Squash merge one commit per feature onto `main`. One spec = one branch = one commit on main. Revert becomes trivial — `git revert <commit-sha>`.

**Commit format** (applies to squash-merged commits on main):
```
<type>(<subsystem>): <what changed> [Refs: CARD-XXX]

Verified: <test method> — <result>
```

Types: `feat`, `fix`, `test`, `docs`. Scopes map to code subsystems (`card-system`, `tooling`, `<SUBSYSTEM_A>`), not spec names. Inline `[Refs: CARD-XXX]` keeps traceability to the source of truth without body bloat. Verification line is always present — it's a requirement, not optional.

**Documentation discipline**: CHANGELOG.md and dev-journal.md must be updated with every change. AGENTS.md itself must stay current as workflows evolve. If a workflow decision changes, update this file before implementing the new behavior.

**Branch divergence handling**: When `main` has moved forward while working on a feature branch, rebase the feature branch onto `main` first, then squash-merge. Conflicts are resolved by reading relevant spec documents and CHANGELOG.md for context — commit messages must transparently document what was merged and why.

**Post-merge cleanup**: Feature branches are deleted after a brief verification window (24-48 hours) where the stakeholder can review exec summaries and CHANGELOG updates before branches are removed. This gives visibility into completed work without cluttering the repository with stale branches.

## Upstream Spec Filing & Numbering Sync

<!-- OPTIONAL: Remove this entire section if you don't use upstream GitHub issues -->
When filing public-facing executive summaries via `gh`, claim upstream issue numbers at filing time (not creation). Check `gh issue list` for next available gap before creating each exec summary — GitHub never renumbers issues, so the mapping is stable once claimed.

**Numbering strategy**: Local CARD-XXX is source of truth; upstream issue number is claimed at filing moment. Bidirectional linking keeps both worlds connected without requiring sync.

**Per-card subfolder structure**: Each spec gets its own folder under `docs/cards/CARD-XXX/` for artifacts, research notes, and exec summary drafts:
```
docs/cards/CARD-001/
├── CARD-001.md                 ← main card doc (source of truth)
├── exec-summary.md             ← upstream filing draft with linked GitHub numbers
└── research-notes.md           ← agent's work-in-progress notes
```

**Many-to-one upstream**: When one spec maps to multiple GitHub issues, list all linked issue numbers in `exec-summary.md`. No dotted numbering — the subfolder workspace is where the mapping lives, not in commit messages or card names.

**Splitting work**: If a spec is complex enough to split into independent specs, create new CARD-XXX cards immediately as separate entities. Don't keep parent-child relationships — each becomes its own spec with its own upstream filing.

**Executive summary format** (machine-generatable from local spec):
```markdown
## [Local CARD-XXX]: <Title>

**Status**: Draft / In Review / Approved  
**Subsystem**: card-system  
**Estimated Effort**: 2-3 sessions  

### Summary
[2-3 sentence executive summary]

### Key Decisions
- Decision: rationale

### Open Questions (for stakeholders)
- Question?
```

**Monitoring workflow**: Check `gh issue list` at session start for stakeholder submissions. Periodic sync — not real-time loops.

<!-- END OF UPSTREAM FILING SECTION -->

## Spec Lifecycle & State Tracking

Spec lifecycle is managed autonomously by the agent. States: `draft` → `approved` → `in-progress` → `verified` → `done` / `reverted`. The "approved" state marks a spec ready to implement after research — no external sign-off required.

**State transitions**:
- `draft → approved`: CARD doc written with scope, verification plan, and upstream filing draft complete
- `approved → in-progress`: Feature branch created for implementation
- `in-progress → verified`: HEADLESS_TEST passes and editor verification completes
- `verified → done`: Squash merged to main + CHANGELOG.md/exec summary updated
- Any state → `reverted`: Work undone; CHANGELOG entry documents reasoning

**Catalogue.md tracks current state.** It's the source of truth for which cards are active vs completed. Updated alongside CHANGELOG.md as part of every change — same discipline, no exceptions.

## Spec Dependencies & Sequencing

**Hybrid approach**: Dependencies declared in card doc (source of truth for that spec) + tracked in catalogue.md (source of truth for workflow state and sequencing). When a card is verified, I check which cards depend on it → update their status from "Blocked" to "Ready". No manual bookkeeping — automatic state changes as blockers complete.

**Card doc declares dependencies explicitly**:
```markdown
## CARD-002: <Title>

**Status**: Draft  
**Depends On**: CARD-001 (Card System) — needs research notes before implementation  

### Summary
<What this does>
```

**Catalogue.md tracks workflow state and sequencing**:
```markdown
## Active Cards

| Card | Status | Depends On | Next Action |
|------|--------|------------|-------------|
| CARD-001 | In Progress | — | Complete implementation |
| CARD-002 | Blocked | CARD-001 | Wait for CARD-001 verification |
| CARD-003 | Draft | CARD-002 | Ready after CARD-002 done |
```

## Spec Overlap & Conflict Prevention

**Hybrid approach**: Quick overlap check before implementation + reactive resolution if new conflicts emerge during work.

1. **Before implementing CARD-XXX**, do quick scope check:
   - Search codebase for related work (`grep`, `srclight_search_symbols`)
   - Note which files/subsystems are touched by existing specs
   - Flag potential overlaps in research-notes.md

2. **If overlap detected**:
   - Small/contained → document resolution strategy, proceed
   - Significant → re-scope CARD-XXX to avoid conflict

3. **During implementation**, if new overlaps emerge:
   - Resolve based on spec priorities + CHANGELOG.md context
   - Document in commit message transparently

## Verification Standards

For a spec to transition from `in-progress` → `verified`, the following must complete:

1. **HEADLESS_TEST passes** — core logic verified via `<test_command>`
2. **Editor verification completes** — visual/behavioral check via `<visual_check_method>` or headless render
3. **CHANGELOG.md updated** — documents what was tested and the result (`Verified: <test method> — <result>`)

Verification is documented in the card's CHANGELOG entry and reflected in the exec summary status if filed upstream. A spec cannot be marked `verified` until both HEADLESS_TEST and editor verification pass — logic correctness alone is insufficient.

## Documentation Update Timing & Discipline

Documentation follows a hybrid pattern — draft during work, finalize after verification:

**During implementation (on feature branch)**:
- Research notes in card subfolder kept current as decisions are made
- Exec-summary.md draft written early, refined with final details before merge
- CHANGELOG.md is NOT updated on the branch — it's a post-merge artifact

**After verification passes (`in-progress` → `verified`)**:
1. Finalize exec-summary.md in card subfolder (complete with upstream issue links)
2. Update CHANGELOG.md with final entry documenting what was built, verified, and merged
3. File/updated exec summary via `gh` referencing the CHANGELOG.md entry on main

**Workflow sequence**:
```
1. Draft CARD doc → draft exec-summary in card subfolder
2. Implement on feature branch → update research-notes.md as needed
3. Verify (HEADLESS_TEST + editor) → pass/fail determines next step
4. If verified: finalize CHANGELOG.md entry, file exec summary via gh
5. Squash-merge to main → delete feature branch after verification window
```

**Rationale**: Research notes capture decisions while fresh; CHANGELOG.md and exec summaries are finalized once — one authoritative record per spec, no scattered updates across multiple commits.

## Spec Creation & Extension Decision

**Default rule: extend existing card unless structural reasons demand a new one.**

Create new CARD-XXX when ANY of these apply:
1. **New subsystem touched** — current spec was `<subsystem_A>`, new work touches `<subsystem_B>` or another distinct area
2. **Different upstream filing needed** — extending would require separate GitHub issue
3. **Independent verification plan required** — can't verify both together; needs separate HEADLESS_TEST
4. **Significant scope expansion** — work is complex enough to warrant its own spec

Extend existing card when ALL of these apply:
- Small refinement to current scope
- No new subsystem impact
- Existing verification plan still applies
- No upstream filing changes needed

**How I apply this rule**: When receiving a request or discovering work during implementation, check the current active CARD. Ask whether it meets any of the four criteria above. If yes → create new card with reference to parent in research-notes.md. If no → extend existing card and update research-notes.md with findings.

## Execution Pattern — How Work Actually Starts

When a request arrives (user message or discovery during implementation), the following sequence applies before any CARD exists or branch is created:

1. **Receive and clarify intent** — confirm understanding of what's being requested; ask for clarification if scope is ambiguous
2. **Check active cards** — read `docs/cards/catalogue.md` to understand current state and whether work extends existing spec or creates new one
3. **Quick research phase**:
   - Search codebase for related work (`grep`, `srclight_search_symbols`)
   - Read existing CARD docs if extending prior work
   - Note constraints, dependencies, known issues in research-notes.md
4. **Draft CARD doc** with:
   - Scope (what this spec does)
   - Verification plan (what tests will pass)
   - Known constraints from research
   - State: `draft`
5. **Iterate on CARD** if needed — refine scope based on research findings; update research-notes.md as understanding evolves
6. **Mark approved** when verification plan is clear and scope is defined → state: `approved`
7. **Implementation begins** → state: `in-progress`

**Research notes live in card subfolder** — they're part of the spec workspace, not separate from it. When revisiting CARD-XXX weeks later, context is preserved.

**Verification plan written during draft phase** ensures I know what "done" looks like before implementation starts — prevents wasted effort on untestable or undefined scope.

## Development Rules

1. **Specs are source of truth** — if code conflicts with a spec document, the code is wrong
2. **Tests before implementation** — write verification tests that encode spec requirements first
3. **Verify in editor** — always run headless or visual test before claiming completion
4. **Update documentation** — CHANGELOG.md and dev-journal.md must be updated with every change; AGENTS.md must stay current as workflows evolve

## Template Reference

This project provides templates for consistent document creation:

| Document | Location | Purpose |
|----------|----------|---------|
| CARD doc | `docs/templates/CARD.md` | Spec document template |
| Catalogue | `docs/templates/catalogue-template.md` | Card index format |
| CHANGELOG entry | `docs/templates/CHANGELOG-template.md` | Post-merge changelog format |

Copy the relevant template, fill in placeholders, and save to the appropriate location. Never create documents from scratch — always start from a template for consistency.

### What This Repo Is

A spec-driven, AI-agent-led development setup using OpenCode + MCP tooling. The infrastructure is designed as a reusable template — clone it, customize the placeholders, and build your project through autonomous agent workflows with full traceability.
