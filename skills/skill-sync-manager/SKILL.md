---
name: skill-sync-manager
description: Selectively inventory, classify, validate, back up, export, and plan synchronization for Codex skills across machines. Use when the user asks to manage skills, sync only personal skills, avoid syncing work/client/company skills, create a skill allowlist, compare local skills to a repo, package skills for transfer, or set up Git-based skill synchronization.
---

# Skill Sync Manager

## Purpose

Manage Codex skills as selected assets, not as a bulk copy of everything. Default to inventory and dry-run plans. Never sync `.system`, work, company, client, secret-bearing, or unknown skills unless the user explicitly includes them.

## Safety Rules

- Default to no writes unless the user asks to create a config or export.
- Never sync `C:\Users\ADMIN\.codex\skills\.system`.
- Sync only skills in an explicit `include` allowlist.
- Treat `work-*`, `client-*`, `company-*`, and unknown business skills as excluded by default.
- Do not sync secrets, tokens, machine-specific private files, or unrelated plugin caches.
- Before overwriting any local skill, create a timestamped backup.
- Validate skills before and after sync when possible.
- Prefer Git for multi-machine sync, but generate a plan before push/pull/copy.

## Local Configuration

Use a local config file such as:

```text
C:\Users\ADMIN\.codex\skill-sync.json
```

Example:

```json
{
  "skills_root": "C:\\Users\\ADMIN\\.codex\\skills",
  "sync_repo": "D:\\codex-skills-sync",
  "include": [
    "flclash-proxy-rules",
    "skill-improvement-review"
  ],
  "exclude": [
    ".system",
    "work-*",
    "client-*",
    "company-*"
  ],
  "groups": {
    "personal": [
      "flclash-proxy-rules",
      "skill-improvement-review"
    ],
    "work": []
  }
}
```

## Workflow

1. Inventory local skills.
2. Classify each skill as `personal`, `work`, `experimental`, `private-local`, `system`, or `unknown`.
3. Build or update an explicit allowlist.
4. Run a dry-run sync plan.
5. Validate included skills.
6. Export or Git-sync only after the user confirms.

Use `scripts/skill_sync.py` for repeatable operations:

```powershell
python C:\Users\ADMIN\.codex\skills\skill-sync-manager\scripts\skill_sync.py inventory
python C:\Users\ADMIN\.codex\skills\skill-sync-manager\scripts\skill_sync.py init-config
python C:\Users\ADMIN\.codex\skills\skill-sync-manager\scripts\skill_sync.py plan-export --repo D:\codex-skills-sync
python C:\Users\ADMIN\.codex\skills\skill-sync-manager\scripts\skill_sync.py export --repo D:\codex-skills-sync
```

## Validation

Validate a skill with:

```powershell
python C:\Users\ADMIN\.codex\skills\.system\skill-creator\scripts\quick_validate.py C:\Users\ADMIN\.codex\skills\skill-name
```

If validation tooling is unavailable, still inspect `SKILL.md` frontmatter and required files before syncing.

## References

Read `references/sync-policy.md` when deciding what belongs in personal sync vs local-only/work groups.
