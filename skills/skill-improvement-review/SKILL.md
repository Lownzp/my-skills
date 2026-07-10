---
name: skill-improvement-review
description: Review and improve Codex skills after meaningful skill usage. Use only when a skill run exposed reusable lessons, user corrections, safety issues, failed or risky workflows, repeated manual steps, missing validation, or the user explicitly asks to summarize lessons, evaluate a skill, or update a skill. Do not use after routine successful skill usage with no new learning.
---

# Skill Improvement Review

## Purpose

Evaluate a skill run as a source of reusable learning. Produce evidence-based improvement advice first; modify the skill only after the user explicitly asks to apply changes.

## Trigger Boundary

Use this skill when at least one is true:

- The user explicitly asks to optimize, review, evaluate, update, or write lessons into a skill.
- The user corrected the agent during skill use.
- A skill caused or nearly caused a safety issue, bad edit, data loss, broken workflow, or rollback.
- The same task pattern or command was repeated and should become a script or reference.
- A missing validation, backup, rollback, or boundary condition became clear.
- A new workflow was discovered that would reduce future risk.

Do not use this skill for routine successful skill usage, one-off environment quirks, or speculative improvements without evidence.

## Review Workflow

1. Identify the skill being reviewed and read its current `SKILL.md`.
2. Gather evidence from the conversation, tool outputs, file diffs, logs, user corrections, and validation results.
3. Separate durable lessons from one-off local accidents.
4. Produce a review using the format below.
5. Recommend whether to update now.
6. Only patch skill files if the user confirms.

If patching after confirmation:

- Read the target skill files first.
- Keep changes minimal and scoped.
- Prefer putting detailed examples in `references/`.
- Add scripts only for repeated, fragile, or deterministic operations.
- Run `quick_validate.py` after changes when available.

## Output Format

Use this concise structure:

```text
Skill Reviewed:
Trigger Fit:
What Happened:
Evidence:
Reusable Lessons:
Safety Notes:
Suggested Patch:
Should Update Now:
```

For `Should Update Now`, answer one of:

- `yes`: clear reusable lesson, safety fix, or repeated step.
- `not yet`: likely useful but needs another example or user confirmation.
- `no`: routine success or one-off issue.

## Rubric

Use `references/review-rubric.md` for the detailed scoring and decision checklist.
