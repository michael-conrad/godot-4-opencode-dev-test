---
name: card-mgmt
description: Manages the research card system — creating, updating status, and archiving cards in docs/cards/ with catalogue updates.
license: MIT
compatibility: opencode
metadata:
  workflow: documentation
  agent-type: subagent
---

## What I do
- Create new numbered cards (CARD-XXX) under docs/cards/
- Update card status in both the card file and docs/cards/catalogue.md
- Archive superseded cards by changing status, never deleting files
- Cross-reference related cards using "Related Cards" section at bottom of each

## When to use me
Use this when making architectural decisions, evaluating tools/libraries, or recording user design decisions that affect implementation.

## Rules
- Never delete old card files — archive them with status change instead
- Update docs/cards/catalogue.md whenever creating/updating/archiving a card
- Each card must have: ID, topic, status, created date, related cards