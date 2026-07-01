---
name: spec-review
description: Reviews implementation against spec documents and research cards for compliance, correctness, and completeness without modifying code.
license: MIT
compatibility: opencode
metadata:
  workflow: review
  agent-type: subagent
---

## What I do
- Load the relevant spec document from docs/specs/ or docs/systems/
- Cross-reference against research cards in docs/cards/catalogue.md
- Verify implementation matches each requirement (REQ-XXX) exactly
- Report findings as verified/passed/failed per requirement

## When to use me
Use this when asked to review, verify, or audit implementation against a spec.

## Rules
- Never modify code — only read and report
- Be specific about which REQ failed and the exact gap
- Check docs/cards/catalogue.md for architectural decisions affecting the spec