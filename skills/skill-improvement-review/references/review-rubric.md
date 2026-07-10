# Skill Improvement Review Rubric

Use this rubric to keep reviews evidence-based and conservative.

## Trigger Fit

Ask:

- Was this skill actually relevant to the task?
- Did the skill trigger too early, too late, or not at all?
- Did the user explicitly ask to write down lessons?

## Workflow Fit

Ask:

- Did the skill provide the right order of operations?
- Were there missing prerequisites, backup steps, or validation steps?
- Did the agent invent unsafe steps outside the skill's intended path?

## Safety

Look for:

- Direct edits to generated or fragile files.
- Missing backups before configuration or data changes.
- Lack of rollback path.
- Commands that interrupted connectivity, services, or user work.
- Encoding, credential, or secret exposure risks.

## Completeness

Ask:

- Did the skill explain how to verify success?
- Did it distinguish diagnosis from remediation?
- Did it define when not to proceed?
- Did it cover how to recover if the change fails?

## User Friction

Treat these as strong evidence:

- The user interrupted or corrected the agent.
- The user reported "you broke it" or similar.
- The user had to point out the correct UI/path/mental model.
- The user asked for repeated clarification.

## Reusable Learning

Good skill updates include:

- A safer default workflow.
- A newly discovered correct entry point.
- A validation command.
- A rollback command.
- A script for repeated fragile edits.
- A reference table for common choices.

Avoid updates based only on:

- A single transient network failure.
- A user preference not likely to recur.
- A local path unless clearly marked as local setup.
- A speculative improvement with no observed failure.

## Suggested Patch Quality

A good suggested patch:

- Names exact files and sections.
- Adds only the smallest durable instruction.
- Moves long examples to references.
- Adds scripts only when they reduce repeated risk.
- Includes validation instructions.

## Decision

Use:

- `yes` when there is clear evidence and the patch is low-risk.
- `not yet` when evidence is plausible but thin.
- `no` when the run succeeded normally or the learning is not durable.
