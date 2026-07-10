#!/usr/bin/env python3
"""Append rules to the currently bound FlClash overwrite script.

This edits shared_preferences.json only. It does not edit config.yaml or profile
YAML files. FlClash must reload/restart to regenerate config.yaml.
"""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime
from pathlib import Path


DEFAULT_PREF = Path(os.environ.get("APPDATA", "")) / "com.follow" / "clash" / "shared_preferences.json"


def load_config(pref_path: Path):
    outer = json.loads(pref_path.read_text(encoding="utf-8"))
    config = json.loads(outer["flutter.config"])
    return outer, config


def save_config(pref_path: Path, outer: dict, config: dict) -> None:
    outer["flutter.config"] = json.dumps(config, ensure_ascii=False, separators=(",", ":"))
    pref_path.write_text(json.dumps(outer, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")


def find_bound_script(config: dict):
    current_id = config.get("currentProfileId")
    profiles = config.get("profiles") or []
    profile = next((p for p in profiles if p.get("id") == current_id), None)
    if not profile:
        raise SystemExit(f"Current profile not found: {current_id}")

    script_id = (((profile.get("overwrite") or {}).get("scriptOverwrite") or {}).get("scriptId"))
    if not script_id:
        raise SystemExit("No overwrite script is bound to the current profile.")

    scripts = config.get("scripts") or []
    script = next((s for s in scripts if s.get("id") == script_id), None)
    if not script:
        raise SystemExit(f"Bound script not found: {script_id}")
    return profile, script


def append_rules_to_script(content: str, rules: list[str]) -> tuple[str, list[str]]:
    added: list[str] = []
    lines = content.splitlines()
    insert_at = None
    for i, line in enumerate(lines):
        if "];" in line:
            insert_at = i
            break
    if insert_at is None:
        raise SystemExit("Could not find the end of the rules array in the script.")

    for rule in rules:
        if rule in content:
            continue
        lines.insert(insert_at, f'    "{rule}",')
        insert_at += 1
        added.append(rule)
    return "\n".join(lines), added


def main() -> int:
    parser = argparse.ArgumentParser(description="Safely append FlClash overwrite-script rules.")
    parser.add_argument("rules", nargs="+", help="Rules such as DOMAIN,storage.googleapis.com,YKKCLOUD")
    parser.add_argument("--preferences", default=str(DEFAULT_PREF), help="Path to shared_preferences.json")
    args = parser.parse_args()

    pref_path = Path(args.preferences)
    if not pref_path.exists():
        raise SystemExit(f"Preferences file not found: {pref_path}")

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = pref_path.with_name(pref_path.name + f".bak-before-rule-{stamp}")
    backup.write_bytes(pref_path.read_bytes())

    outer, config = load_config(pref_path)
    _profile, script = find_bound_script(config)
    new_content, added = append_rules_to_script(script.get("content") or "", args.rules)
    script["content"] = new_content
    save_config(pref_path, outer, config)

    print(f"Backup: {backup}")
    if added:
        print("Added rules:")
        for rule in added:
            print(f"  {rule}")
    else:
        print("No new rules added; all requested rules already existed.")
    print("Reload or restart FlClash, then verify generated config.yaml.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
