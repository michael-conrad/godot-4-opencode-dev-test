# Changelog

All notable changes to this project are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) conventions with AI agent workflow extensions.

## Unreleased

### Planned / In Progress
- CARD-XXX: <Title> — `<status>` (draft/approved/in-progress)
- CARD-YYY: <Title> — `<status>` (draft/approved/in-progress)

---

## [YYYY-MM-DD] — CARD-XXX: <Title>

**Subsystem**: `<subsystem-name>`  
**Branch**: `feature/<short-descriptive-name>` → squash-merged to main  
**Commit**: `<sha>` (`<type>(<scope>): <what changed>`)  
**GitHub Issue(s)**: #<issue_number> (if filed)  

### Summary
[2-3 sentence description of what was built]

### What Changed
- Added/Modified/Removed: `<specific changes>`
- Files touched: `path/to/file`, `another/path`

### Verification
- **HEADLESS_TEST**: <test_command> — passed ✓ / failed ✗
- **Godot Verification**: <visual_check_or_screenshot_result> — passed ✓ / failed ✗
- **CHANGELOG.md Updated**: YYYY-MM-DD HH:MM UTC

### Notes
- [Any relevant context, decisions made during implementation]
- [If reverted, explain why and link to revert commit]

---

## Format Reference

When adding a new CHANGELOG entry, copy this structure:

```markdown
## [YYYY-MM-DD] — CARD-XXX: <Title>

**Subsystem**: `<subsystem-name>`  
**Branch**: `feature/<short-descriptive-name>` → squash-merged to main  
**Commit**: `<sha>` (`<type>(<scope>): <what changed>`)  
**GitHub Issue(s)**: #<issue_number> (if filed)  

### Summary
[2-3 sentence description of what was built]

### What Changed
- Added/Modified/Removed: `<specific changes>`
- Files touched: `path/to/file`, `another/path`

### Verification
- **HEADLESS_TEST**: <test_command> — passed ✓ / failed ✗
- **Godot Verification**: <visual_check_or_screenshot_result> — passed ✓ / failed ✗
- **CHANGELOG.md Updated**: YYYY-MM-DD HH:MM UTC

### Notes
- [Any relevant context, decisions made during implementation]
```
