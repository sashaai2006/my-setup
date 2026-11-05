#!/usr/bin/env python3
"""Perform deterministic sanity checks on a README.md file."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

PLACEHOLDER_RE = re.compile(
    r"\b(?:TODO|TBD|PLACEHOLDER|LOREM\s+IPSUM|COMING\s+SOON)\b", re.IGNORECASE
)
SECRET_RES = (
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
)
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")


def check_links(text: str, readme: Path) -> list[str]:
    errors: list[str] = []
    for match in LINK_RE.finditer(text):
        raw_target = match.group(1).strip()
        if not raw_target:
            continue
        angle_target = re.match(r"<([^>]+)>", raw_target)
        target = (
            angle_target.group(1)
            if angle_target
            else raw_target.split(maxsplit=1)[0].strip("<>")
        )
        parsed = urlsplit(target)
        if parsed.scheme or parsed.netloc or target.startswith(("#", "//")):
            continue
        path_text = unquote(parsed.path)
        if not path_text:
            continue
        if path_text.startswith("/"):
            errors.append(
                f"absolute local link is not portable: {target!r}"
            )
            continue
        resolved = (readme.parent / path_text).resolve()
        if not resolved.exists():
            line = text.count("\n", 0, match.start()) + 1
            errors.append(f"line {line}: missing local target: {target!r}")
    return errors


def check_fences(lines: list[str]) -> list[str]:
    errors: list[str] = []
    marker: str | None = None
    opening_line = 0
    for number, line in enumerate(lines, 1):
        match = FENCE_RE.match(line)
        if not match:
            continue
        current = match.group(1)
        if marker is None:
            marker = current
            opening_line = number
        elif current[0] == marker[0] and len(current) >= len(marker):
            marker = None
    if marker is not None:
        errors.append(f"line {opening_line}: unclosed code fence {marker!r}")
    return errors


def check_readme(readme: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if not readme.is_file():
        return [f"file not found: {readme}"], warnings
    try:
        text = readme.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        return [f"file is not valid UTF-8: {exc}"], warnings

    lines = text.splitlines()
    if not text.strip():
        return ["file is empty"], warnings

    first_content = next((line.strip() for line in lines if line.strip()), "")
    if not first_content.startswith("# "):
        warnings.append("first non-empty line is not an H1 title")

    h1_count = sum(bool(re.match(r"^#(?!#)\s+", line)) for line in lines)
    if h1_count == 0:
        errors.append("missing H1 title")
    elif h1_count > 1:
        warnings.append(f"multiple H1 titles found: {h1_count}")

    errors.extend(check_fences(lines))
    errors.extend(check_links(text, readme))

    for number, line in enumerate(lines, 1):
        if PLACEHOLDER_RE.search(line):
            errors.append(f"line {number}: unresolved placeholder")
        for secret_re in SECRET_RES:
            if secret_re.search(line):
                errors.append(f"line {number}: possible secret")
                break

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("readme", type=Path, help="path to README.md")
    args = parser.parse_args()
    errors, warnings = check_readme(args.readme)

    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")

    if errors:
        print(f"FAIL: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    print(f"PASS: 0 errors, {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
