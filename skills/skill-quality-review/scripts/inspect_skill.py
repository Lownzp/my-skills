#!/usr/bin/env python3
"""Fast deterministic preflight for an Agent Skill directory.

This does not replace an official validator or behavioral quality review.
"""

from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from pathlib import Path


LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
ABSOLUTE_PATH_RE = re.compile(r"(?:[A-Za-z]:\\|/Users/|/home/)")
FENCED_CODE_RE = re.compile(r"```.*?```", re.DOTALL)
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
TEXT_SUFFIXES = {
    ".md", ".markdown", ".txt", ".yaml", ".yml", ".json", ".toml",
    ".py", ".js", ".mjs", ".cjs", ".ts", ".tsx", ".jsx", ".sh",
    ".ps1", ".bat", ".cmd", ".xml", ".html", ".css", ".sql",
}
BIDI_CONTROLS = set(range(0x202A, 0x202F)) | set(range(0x2066, 0x206A))
TAG_CHARACTERS = set(range(0xE0000, 0xE0080))
ZERO_WIDTH_SIGNALS = {0x200B, 0x2060}


def suspicious_invisible_characters(text: str) -> list[tuple[int, int, str]]:
    """Return line, code point, and Unicode name for review-worthy characters."""
    findings: list[tuple[int, int, str]] = []
    line = 1
    for index, char in enumerate(text):
        code_point = ord(char)
        if char == "\n":
            line += 1
            continue
        suspicious = (
            code_point in TAG_CHARACTERS
            or code_point in BIDI_CONTROLS
            or code_point in ZERO_WIDTH_SIGNALS
            or (code_point < 0x20 and char not in "\r\t")
            or (code_point == 0x7F)
            or (code_point == 0xFEFF and index != 0)
        )
        if suspicious:
            name = unicodedata.name(char, "UNNAMED CONTROL")
            findings.append((line, code_point, name))
    return findings


def inspect(skill_dir: Path) -> tuple[list[str], list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    info: list[str] = []

    if not skill_dir.is_dir():
        return [f"Not a directory: {skill_dir}"], warnings, info

    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        return ["Missing SKILL.md"], warnings, info

    text = skill_md.read_text(encoding="utf-8")
    prose = INLINE_CODE_RE.sub("", FENCED_CODE_RE.sub("", text))
    lines = text.splitlines()
    info.append(f"SKILL.md lines: {len(lines)}")
    if len(lines) > 500:
        warnings.append("SKILL.md exceeds 500 lines; review progressive disclosure")

    if "TODO" in prose or "[TODO" in prose:
        errors.append("SKILL.md contains TODO placeholders")

    frontmatter = re.match(r"\A---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not frontmatter:
        errors.append("Missing or malformed YAML frontmatter")
    else:
        raw = frontmatter.group(1)
        name_match = re.search(r"^name:\s*(.+?)\s*$", raw, re.MULTILINE)
        desc_match = re.search(r"^description:\s*(.+?)\s*$", raw, re.MULTILINE)
        if not name_match:
            errors.append("Frontmatter missing name")
        else:
            name = name_match.group(1).strip('"\'')
            if name != skill_dir.name:
                errors.append(f"Skill name '{name}' does not match directory '{skill_dir.name}'")
            if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
                errors.append("Skill name is not lowercase hyphen-case")
        if not desc_match or len(desc_match.group(1).strip()) < 30:
            errors.append("Frontmatter description is missing or too short")

    if ABSOLUTE_PATH_RE.search(prose):
        warnings.append("SKILL.md contains an absolute local path; verify portability")

    for match in LINK_RE.finditer(prose):
        target = match.group(1).strip().split("#", 1)[0]
        if not target or "://" in target or target.startswith("#"):
            continue
        resolved = (skill_dir / target).resolve()
        if not resolved.exists():
            errors.append(f"Broken relative link: {target}")

    for folder_name in ("references", "scripts", "assets"):
        folder = skill_dir / folder_name
        if folder.is_dir() and not any(folder.iterdir()):
            warnings.append(f"Empty optional directory: {folder_name}/")

    openai_yaml = skill_dir / "agents" / "openai.yaml"
    if openai_yaml.is_file():
        metadata = openai_yaml.read_text(encoding="utf-8")
        if "$" + skill_dir.name not in metadata:
            warnings.append("agents/openai.yaml default_prompt may not mention the skill")
    else:
        warnings.append("Missing recommended agents/openai.yaml")

    unicode_findings = 0
    for path in skill_dir.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            candidate = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for line_number, code_point, name in suspicious_invisible_characters(candidate):
            unicode_findings += 1
            if unicode_findings <= 20:
                relative = path.relative_to(skill_dir)
                warnings.append(
                    f"Suspicious invisible Unicode: {relative}:{line_number} "
                    f"U+{code_point:04X} {name}; review context before judging intent"
                )
    if unicode_findings > 20:
        warnings.append(
            f"Suspicious invisible Unicode: {unicode_findings - 20} additional finding(s) omitted"
        )

    file_count = sum(1 for path in skill_dir.rglob("*") if path.is_file())
    info.append(f"Files: {file_count}")
    return errors, warnings, info


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill_dir", type=Path)
    args = parser.parse_args()

    errors, warnings, info = inspect(args.skill_dir.expanduser().resolve())
    for item in info:
        print(f"INFO: {item}")
    for item in warnings:
        print(f"WARN: {item}")
    for item in errors:
        print(f"ERROR: {item}")
    print(f"RESULT: {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
