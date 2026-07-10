#!/usr/bin/env python3
"""Selective Codex skill inventory and export helper."""

from __future__ import annotations

import argparse
import fnmatch
import json
import os
import shutil
from datetime import datetime
from pathlib import Path


DEFAULT_SKILLS_ROOT = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")) / "skills"
DEFAULT_CONFIG = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")) / "skill-sync.json"


DEFAULT_EXCLUDE = [".system", "work-*", "client-*", "company-*"]


def is_skill_dir(path: Path) -> bool:
    return path.is_dir() and (path / "SKILL.md").exists()


def load_config(path: Path) -> dict:
    if not path.exists():
        return {
            "skills_root": str(DEFAULT_SKILLS_ROOT),
            "sync_repo": "",
            "include": [],
            "exclude": DEFAULT_EXCLUDE,
            "groups": {"personal": [], "work": []},
        }
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save_config(path: Path, config: dict) -> None:
    path.write_text(json.dumps(config, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def excluded(name: str, patterns: list[str]) -> bool:
    return any(fnmatch.fnmatchcase(name, pat) for pat in patterns)


def inventory(config: dict) -> list[dict]:
    root = Path(config.get("skills_root") or DEFAULT_SKILLS_ROOT)
    include = set(config.get("include") or [])
    exclude = config.get("exclude") or DEFAULT_EXCLUDE
    group_by_name = {}
    for group, names in (config.get("groups") or {}).items():
        for name in names or []:
            group_by_name[name] = group
    rows = []
    if not root.exists():
        return rows
    for child in sorted(root.iterdir(), key=lambda p: p.name.lower()):
        if not is_skill_dir(child):
            continue
        name = child.name
        if name == ".system":
            group = "system"
        elif excluded(name, exclude):
            group = "excluded"
        elif name in include:
            group = "included"
        elif name in group_by_name:
            group = group_by_name[name]
        else:
            group = "unknown"
        rows.append({"name": name, "group": group, "path": str(child)})
    return rows


def print_inventory(config: dict) -> None:
    rows = inventory(config)
    if not rows:
        print("No skills found.")
        return
    width = max(len(r["name"]) for r in rows)
    for row in rows:
        print(f"{row['name']:<{width}}  {row['group']:<9}  {row['path']}")


def plan_export(config: dict, repo: Path) -> list[tuple[Path, Path]]:
    root = Path(config.get("skills_root") or DEFAULT_SKILLS_ROOT)
    include = config.get("include") or []
    pairs = []
    for name in include:
        src = root / name
        if not is_skill_dir(src):
            print(f"SKIP missing or invalid skill: {name}")
            continue
        dst = repo / "skills" / name
        pairs.append((src, dst))
    return pairs


def export(config: dict, repo: Path, dry_run: bool) -> None:
    pairs = plan_export(config, repo)
    if not pairs:
        print("Nothing to export. Add skill names to include first.")
        return
    for src, dst in pairs:
        print(f"{'WOULD COPY' if dry_run else 'COPY'} {src} -> {dst}")
        if dry_run:
            continue
        if dst.exists():
            backup_root = repo / ".backups" / datetime.now().strftime("%Y%m%d-%H%M%S")
            backup_dst = backup_root / dst.name
            backup_dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(dst, backup_dst)
            shutil.rmtree(dst)
        dst.parent.mkdir(parents=True, exist_ok=True)
        ignore = shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store")
        shutil.copytree(src, dst, ignore=ignore)
    manifest = {
        "exported_at": datetime.now().isoformat(timespec="seconds"),
        "include": config.get("include") or [],
    }
    if not dry_run:
        (repo / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Selective Codex skill inventory/export helper.")
    parser.add_argument("command", choices=["inventory", "init-config", "plan-export", "export"])
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    parser.add_argument("--repo", default="")
    args = parser.parse_args()

    config_path = Path(args.config)
    config = load_config(config_path)

    if args.command == "init-config":
        if config_path.exists():
            print(f"Config already exists: {config_path}")
        else:
            save_config(config_path, config)
            print(f"Created config: {config_path}")
        return 0

    if args.command == "inventory":
        print_inventory(config)
        return 0

    repo = Path(args.repo or config.get("sync_repo") or "")
    if not str(repo):
        raise SystemExit("A repo path is required via --repo or sync_repo in config.")

    if args.command == "plan-export":
        export(config, repo, dry_run=True)
        return 0

    if args.command == "export":
        export(config, repo, dry_run=False)
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
