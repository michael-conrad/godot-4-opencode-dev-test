# docs/ AGENTS.md — Documentation Layer Agent Instructions

## Purpose

This file provides agent instructions specific to the `docs/` directory. It ensures agents always know how to work with documentation, specs, and research cards in this project.

### Rules for Working With Docs

1. **Always read docs/cards/catalogue.md first** when receiving a task that involves prior decisions
2. **Write new spec files under docs/specs/** — never inline-specify requirements in code comments
3. **Update the catalogue** whenever creating, updating, or archiving a research card
4. **Never delete old card files** — archive them with status change instead (card system preserves history)
5. **Cross-reference cards** using the "Related Cards" section at the bottom of each card

### Spec Document Conventions

Each spec in `docs/specs/` or `docs/systems/` must follow this structure:

```markdown
# [System Name]

## Overview
One paragraph describing what this system does.

## Requirements
- REQ-001: Specific, testable requirement
- REQ-002: ...

## Architecture
How the system fits into the broader game (autoloads, signals, node structure).

## Test Plan
What tests verify this spec and where they live.

## Status
DRAFT | APPROVED | IMPLEMENTED | SHIPPED
```

### Research Card Conventions

Each card in `docs/cards/` must follow this structure:

```markdown
# CARD-XXX: [Title]

**Status**: ACTIVE / RESEARCHING / DRAFTING / DECIDED / ARCHIVED  
**Created**: YYYY-MM-DD  
**References**: CARD-YYY, CARD-ZZZ

## Summary
What was decided or discovered.

## Details
Supporting information, comparisons, reasoning.

## Open Questions
Items that need follow-up (if any).

## Related Cards
CARD-YYY: [Title] — [one-line relationship description]
```

### When to Create New Cards

Create a new research card when:
- Making an architectural decision with long-term impact
- Evaluating tools/libraries/frameworks and recording the comparison
- Recording user design decisions that affect implementation
- Documenting failure modes or lessons learned during implementation

When NOT to create a card:
- Routine implementation details (put those in spec documents instead)
- Temporary context that will be resolved within one session
- Information already covered by an existing active card
