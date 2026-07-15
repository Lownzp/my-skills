# Behavioral Evaluation

Use behavioral evaluation to test what static review cannot prove: triggering, instruction following, failure handling, and completion integrity.

## Design the case set

Create the smallest set that covers material risks:

1. Positive trigger — a natural user request that clearly needs the skill.
2. Synonym trigger — different wording for the same need.
3. Near-miss negative — related topic that should not invoke the skill.
4. Scope-boundary case — request mixing in an adjacent capability.
5. Incomplete-input case — required artifact or choice is missing.
6. Failure case — a required tool, script, dependency, or environment is unavailable.
7. Safety case — an external, destructive, sensitive, or irreversible action is suggested.
8. Completion case — work is prepared or partially run but the promised result is not proven.
9. Regression case — a prompt that previously exposed a real failure.
10. Skill-competition case — place the target beside one or more adjacent skills and use natural wording that tests whether routing, exclusion, and handoff remain predictable.
11. Task-scale case — compare a small direct request with a larger multi-stage request and check whether the skill avoids over-processing the first or under-specifying the second.

Not every skill needs all eleven. Select cases from the skill's actual risk profile and explain omissions.

## Preserve evaluation integrity

- Give the evaluating agent the skill and raw task artifact, not the expected verdict or suspected defect.
- Use natural user wording and minimal task-local context.
- Keep evaluation outputs isolated so later cases cannot discover earlier conclusions.
- Record the exact prompt, environment, available tools, result, and observed deviation.
- Do not call a case passed merely because the final answer sounds plausible; inspect required actions and evidence.

## Evaluate each case

Check:

- Trigger decision: invoked, not invoked, or ambiguous.
- Workflow adherence: required actions occurred in the correct scope.
- Judgment quality: decisions used the stated criteria rather than arbitrary defaults.
- Gate adherence: safety and completion constraints held.
- Outcome quality: the requested result is correct and useful.
- Context efficiency: irrelevant references or large resources were not loaded unnecessarily.

Classify deviations as trigger, instruction, resource, tool/environment, safety, completion, or evaluation-fixture defects.

## Compare revisions

Reuse the same case set before and after a skill change. Add a regression case for each newly discovered failure. Prefer a small durable suite over many trivial prompts.

Do not declare release-quality behavioral confidence when only a single happy-path case ran.

## Baseline regression cases for this skill

Keep these cases when evaluating `skill-quality-review` itself:

1. `这个 skill 写得怎么样？` — invoke this skill and perform a read-only quality review.
2. `比较这两个 skills 哪个设计得更好` — invoke this skill and apply the same rubric to both targets.
3. `检查这个 skill 是否符合飞帆投稿规范` — do not use this skill as the sole workflow; route to the submission checker because compliance is the primary goal.
4. `帮我创建一个处理 PDF 的 skill` — route to `skill-creator`; do not invoke this skill as the primary workflow.
5. `优化这个 SKILL.md` — route to `skill-creator` as primary. Use this skill only when a diagnostic or post-change review materially helps.
6. `先评价这个 skill，再按建议修改并复审` — use this skill for diagnosis, `skill-creator` for file changes, then this skill for re-review.
7. Only a standalone `SKILL.md` is available — review available evidence, disclose that directory resources and metadata were not inspected, and lower confidence where material.
8. The preflight script was not run or failed — do not claim structural preflight success; report the missing evidence separately from the qualitative review.
