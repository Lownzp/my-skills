# Skill Sync Policy

## Default Groups

- `personal`: safe to sync across personal machines.
- `experimental`: sync only if the user includes it.
- `private-local`: never sync by default; may contain machine-specific paths.
- `work`: never sync to personal machines by default.
- `system`: never sync; installed by Codex or plugins.
- `unknown`: do not sync until classified.

## Include Rules

Only sync skills listed in `include`.

Good personal candidates:

- General troubleshooting skills.
- Personal workflow automation.
- Reusable non-secret references.
- Skills intentionally created for personal Codex use.

Exclude by default:

- `.system`
- Work, company, client, or NDA-related skills.
- Skills containing secrets, tokens, customer data, internal URLs, or private repo details.
- Skills with absolute paths that only make sense on one machine, unless intentionally local.

## Git Sync Guidance

Use a private Git repository for multi-machine sync. Keep this config local unless the user wants it committed. Recommended repo structure:

```text
codex-skills-sync/
  skills/
    flclash-proxy-rules/
    skill-improvement-review/
  manifest.json
```

Before export:

- Inventory.
- Confirm allowlist.
- Validate included skills.
- Copy only included skill directories.

Before import:

- Compare source and destination.
- Back up any local skill that would be overwritten.
- Validate imported skills.

## Red Flags

Pause and ask before syncing if a skill contains:

- API keys, tokens, cookies, private URLs, or `.env` files.
- Customer names or company-internal process docs.
- Worktree-specific paths.
- Large generated artifacts.
- Plugin cache folders.
