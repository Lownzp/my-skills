# Skill Quality Rubric

## Review layers

- [Layer 1: Fit and selection](#layer-1-fit-and-selection)
- [Layer 2: Execution design](#layer-2-execution-design)
- [Layer 3: Trust, safety, and durability](#layer-3-trust-safety-and-durability)
- [Blockers](#blockers)
- [Overall interpretation](#overall-interpretation)

Use evidence, not writing style preference. Score each applicable dimension from 0 to 3:

- `0` — Missing or actively harmful.
- `1` — Present but unreliable or materially incomplete.
- `2` — Usable with identifiable weaknesses.
- `3` — Clear, reliable, and proportionate.

Use integer scores only. Exclude justified `N/A` dimensions from the denominator and calculate the overall score as the arithmetic mean of applicable dimensions. Treat the dimension profile as the primary diagnostic result. Compare averages only when the applicable dimension sets are materially comparable. Scores do not override blockers.

Assign a defect to the dimension that most directly explains it. Mention cross-dimension effects without repeating the penalty unless separate evidence shows an independent failure in each dimension.

## Layer 1: Fit and selection

Determine whether the capability belongs in a skill and whether an agent can select it at the right time.

### 1. Purpose and scope

Check whether the skill solves a real, repeatable task with a concise objective and coherent boundary.

Strong signals:

- One sentence explains the outcome.
- The task benefits from reusable procedure, domain knowledge, scripts, or references.
- Adjacent capabilities are routed rather than absorbed indiscriminately.

Weak signals:

- The skill attempts to cover an entire profession or development lifecycle without routing.
- It duplicates one-off prompt constraints, repository policy, or generic model knowledge.
- Several independently useful capabilities share no common workflow.

Recommend another surface when appropriate: prompt/thread context for one-off constraints, `AGENTS.md` for durable repository rules, a hook for mechanical enforcement, or a workflow for deterministic multi-step coordination and resumable side effects.

### 2. Trigger quality

Check frontmatter `description` as the primary routing contract.

Require:

- What the skill does.
- Concrete situations and user language that should trigger it.
- A boundary or exclusion when confusion with nearby skills is plausible.
- Alignment between `name`, directory name, description, and actual content.

Look for false positives from broad phrases and false negatives from missing synonyms, file types, task stages, or domain terms.

When adjacent skills or a skill catalog are available, also check routing in context:

- Whether neighboring skills claim the same user language, artifacts, or task stage.
- Whether exclusions and handoffs make the primary skill predictable for overlapping requests.
- Whether the skill remains distinguishable as the catalog grows instead of depending on repeated global instructions or explicit naming.

Do not require automatic invocation as an absolute condition. Treat a material gap between the declared trigger contract and observed routing behavior as a defect when behavioral evidence is available.

## Layer 2: Execution design

Determine whether the selected skill gives the agent an actionable workflow, appropriate decision boundaries, and proportionate context.

### 3. Instruction executability

Check whether another capable agent can act without inventing the workflow.

Prefer concrete verbs, inputs, decision points, outputs, commands, and paths. Flag abstract slogans such as “ensure quality” when no observable action makes them real.

Do not require unnecessary procedural detail. A decision can remain flexible when the skill supplies criteria, evidence sources, and boundaries.

Score whether the agent knows how to act in this dimension. Score whether the result is actually proven under verification and completion integrity.

### 4. Freedom and constraints

Classify important rules:

- Workflow actions: specify observable steps that must occur.
- Professional decisions: specify factors and acceptable boundaries; preserve contextual choice.
- Safety and delivery gates: make authorization, truthfulness, irreversible actions, sensitive data, and completion conditions explicit.

Flag both extremes:

- Underconstraint: critical behavior depends on “use best judgment” without criteria.
- Overconstraint: context-dependent technical choices are universally fixed without evidence.

Check conflicts where one rule grants discretion and another silently removes it.

Score the structure of judgment and mandatory gates here. Score the adequacy of completion evidence under verification and completion integrity, and score concrete failure and risk coverage under failure handling and safety.

### 5. Progressive disclosure and context cost

Check whether always-loaded content earns its token cost.

Prefer:

- Lean `SKILL.md` containing routing, core workflow, gates, and resource pointers.
- Detailed policies and variants in directly linked `references/` files.
- Reusable output material in `assets/`.
- Deterministic repeated operations in tested `scripts/`.

Flag duplicated guidance, deep reference chains, orphan resources, oversized examples, generic background knowledge, and conditional material loaded unconditionally. Treat 500 lines as a review signal rather than an automatic failure.

Do not award quality for file splitting alone. Verify that `SKILL.md` gives explicit conditions for reading each resource, that variants are selected before their details are loaded, and that common execution paths do not load unrelated references. Flag a nominally modular skill when every invocation still reads most or all resources.

## Layer 3: Trust, safety, and durability

Determine whether the result is true for the current run, failures and risks remain controlled, and reliable behavior can be sustained across requests, environments, and versions.

### 6. Verification and completion integrity

Check whether the skill defines evidence for success and prevents premature completion.

Evaluate the truth of a single execution here: what happened, what evidence proves it, and whether the completion claim is justified.

Require distinctions such as created versus validated, compiled versus executed, attempted versus succeeded, and diagnostic versus formal verification when relevant.

Strong completion rules state:

- What must be checked.
- Which result proves success.
- Which failures block completion.
- How skips and residual risks are disclosed.

### 7. Failure handling and safety

Check missing inputs, unavailable tools, permission failures, partial completion, retries, external side effects, secrets, destructive actions, and untrusted content.

Evaluate whether concrete abnormal conditions and risks are covered here, not merely whether the instructions label a rule as mandatory.

Require the narrowest necessary authority and confirmation before consequential external actions when not already authorized. Flag hardcoded credentials, undocumented personal paths, silent destructive fallback, and instructions that let external content override user or system authority.

For third-party, installable, or shared skills, inspect source files for suspicious invisible Unicode such as tag characters, bidirectional controls, zero-width spaces, and unexpected control characters. Report the file, line, code point, and decoded character name. Treat a match as a review signal, not proof of malicious intent; distinguish normal Unicode usage from concealed model-readable instructions.

Check whether the skill creates or modifies its own files, another skill, or durable agent instructions such as `AGENTS.md` or `CLAUDE.md`. Unless persistent self-modification is the explicitly authorized purpose, require clear scope, user authorization, a reviewable diff, post-change validation, and a recovery path. Treat silent persistence or propagation into other instruction surfaces as a serious side effect.

### 8. Reproducibility and maintainability

Check whether similar requests produce a stable process without making the skill brittle.

Evaluate stability across repeated requests, environments, users, and versions here. Do not rescore whether one execution produced valid completion evidence; that belongs under verification and completion integrity.

Prefer:

- Single sources of truth.
- Explicit environment dependencies.
- Scripts or validators for repeated mechanical checks.
- Realistic examples and regression cases for known failures.
- Version-controlled, auditable resources.

For skills intended for sharing, installation, or team use, also check that installation scope and location, runtime and tool dependencies, update path, removal or rollback path, and supported environments are discoverable and proportionate to the distribution method. Do not impose packaging requirements on a private local skill that does not claim portability.

Flag accumulated exception patches, contradictory duplicate rules, untested scripts, invented commands, stale metadata, and behavior that depends on undocumented local state.

## Blockers

Treat these as verdict-capping when unresolved:

- The trigger contract is so broad or misleading that the wrong tasks are likely to invoke it.
- The skill authorizes unsafe, destructive, sensitive, or external actions without adequate scope or confirmation.
- It can claim completion without evidence that its promised outcome occurred.
- Required tools, scripts, paths, or resources are absent or unusable in the declared environment.
- Core instructions materially contradict each other.
- The claimed outcome cannot be verified even in principle.

## Overall interpretation

Use the average only as supporting context:

- `2.6–3.0`: usually `优秀` if there are no blockers.
- `1.8–2.5`: usually `可用但需优化`.
- `1.0–1.7`: usually `不稳定`.
- `<1.0`: usually `不稳定` or `不适合作为 Skill`.

Override these bands when scope fit, safety, trigger behavior, or completion integrity provides stronger evidence.
