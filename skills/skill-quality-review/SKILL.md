---
name: skill-quality-review
description: Evaluate, audit, score, or compare the design quality, trigger accuracy, execution reliability, safety, context efficiency, verifiability, and maintainability of an Agent Skill directory or SKILL.md, and provide prioritized improvement recommendations. Use when asked whether a skill is good, to review skill quality, compare skills, assess a skill before adoption, verify whether a revision improved quality, or respond to phrases such as "这是一个好 skill 吗", "skill 好不好", "评价 skill", or "审查 skill 质量". Use skill-creator as the primary workflow when the user asks to create, modify, optimize, complete, or refactor skill files. Do not use as a submission-format or marketplace-packaging checker when compliance alone is the goal.
---

# Skill Quality Review

Evaluate whether a skill can trigger at the right time, complete its claimed task reliably, and prove the result without wasting context or creating unacceptable risk.

## Review workflow

1. Establish the review target and requested depth: one `SKILL.md`, a complete skill directory, a comparison, or a post-change re-review. Treat review as read-only unless the user explicitly asks for edits.
2. Inventory the complete skill directory when available. Run `python scripts/inspect_skill.py <skill-dir>` as a fast deterministic preflight, then use the platform's official skill validator when available. The preflight does not fully parse YAML, validate every product-specific metadata constraint, inspect every transitive reference, or prove behavioral quality. Read `SKILL.md`, `agents/openai.yaml`, directly referenced resources, and executable scripts that affect behavior. Do not infer missing content.
3. Read `references/quality-rubric.md` completely. Evaluate every applicable dimension using artifact evidence. Mark dimensions `N/A` only with a reason.
4. Separate three instruction types:
   - Require concrete, observable workflow actions.
   - Preserve professional judgment by specifying decision criteria rather than forcing one result.
   - Apply hard gates to safety, authorization, truthfulness, irreversible side effects, and completion claims.
5. Identify interaction defects: contradictory rules, duplicated guidance, unreachable references, scope overlap with other skills, hidden prerequisites, brittle environment assumptions, and rules that should be scripts or validators. When adjacent skills are available, inspect their routing contracts rather than judging trigger quality only in isolation.
6. When the user requests behavioral confidence, comparisons, or a release-quality verdict, read `references/behavior-evaluation.md` and design or run representative trigger and execution cases. Do not claim behavioral validation from static inspection alone.
7. Produce an evidence-backed verdict. Prioritize changes; do not rewrite the skill unless explicitly asked.

When the user asks to modify skill files, use this skill to establish the diagnosis and acceptance criteria, use `skill-creator` as the primary implementation workflow, then use this skill again for post-change review. Do not duplicate skill creation, metadata generation, or editing procedures here.

## Evidence rules

- Cite file paths and tight line references for material findings when files are available.
- Distinguish observed facts, reasoned risks, and untested hypotheses.
- Do not award quality for length, strict wording, number of files, or nominal coverage alone.
- Do not treat valid YAML or directory structure as proof that the skill works.
- Do not penalize a skill merely for allowing judgment; penalize missing decision criteria or missing safety boundaries.
- Treat a blocker as verdict-capping even when the numeric score is high.

## Verdicts

- `优秀`: No blocker; reliable design with only minor optional improvements.
- `可用但需优化`: No blocker; useful now, with one or more material weaknesses.
- `不稳定`: Important behavior depends on ambiguity, missing validation, brittle assumptions, or conflicting instructions.
- `不适合作为 Skill`: The scope belongs in one-off instructions, durable project guidance, a deterministic workflow/hook, or another capability surface.

Cap the verdict at `不稳定` for any unresolved blocker involving trigger ambiguity, unsafe side effects, false completion, unusable dependencies, or an inability to verify the claimed outcome.

## Output format

Lead with the verdict and one-sentence rationale, then provide:

1. `阻断问题`: Only verdict-capping issues; omit when none.
2. `主要发现`: Evidence-backed findings ordered by impact.
3. `维度评价`: Scores with concise reasons; do not use a Markdown table unless the destination document benefits from one.
4. `改进顺序`: Minimal prioritized actions: keep, simplify, split, add a reference, script a repeated action, add a gate, or add behavioral evaluation.
5. `验证边界`: State whether the conclusion is static-only or includes behavioral evaluation.

Keep the report proportional. For a strong small skill, a short review is better than manufactured findings.

## Resources

- Read `references/quality-rubric.md` for every review.
- Read `references/behavior-evaluation.md` for behavioral validation, comparisons, release-quality verdicts, or when static evidence cannot resolve a material concern.
- Run `scripts/inspect_skill.py` on a local skill directory before manual review when Python is available.
- Treat `scripts/inspect_skill.py` as a fast preflight only; do not present it as a complete skill validator or quality verdict.
