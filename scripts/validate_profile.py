#!/usr/bin/env python3
"""Validate the canonical YAML profile."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

try:
    from scripts.profile_document import ProfileDocumentError, load_profile
    from scripts.profile_schema import PROFILE_VALIDATOR
except ModuleNotFoundError:  # Direct execution from the scripts directory.
    from profile_document import ProfileDocumentError, load_profile
    from profile_schema import PROFILE_VALIDATOR


@dataclass(frozen=True)
class Finding:
    level: str
    path: str
    message: str

    @property
    def line(self) -> int:
        """Compatibility shim for callers of the former Markdown validator."""
        return 1


def _json_path(parts: Iterable[object]) -> str:
    path = "$"
    for part in parts:
        if isinstance(part, int):
            path += f"[{part}]"
        elif isinstance(part, str) and re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", part):
            path += f".{part}"
        else:
            path += f"[{part!r}]"
    return path


def validate_profile(path: Path) -> list[Finding]:
    """Return schema findings for a profile YAML file."""
    try:
        document = load_profile(path)
    except ProfileDocumentError as error:
        return [Finding("ERROR", "$", str(error))]

    findings = [
        Finding("ERROR", _json_path(error.absolute_path), error.message)
        for error in PROFILE_VALIDATOR.iter_errors(document)
    ]
    unique = {(item.level, item.path, item.message): item for item in findings}
    return sorted(unique.values(), key=lambda item: (item.path, item.level, item.message))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", default="data/profile.yaml", type=Path)
    parser.add_argument("--warnings-as-errors", action="store_true")
    args = parser.parse_args()
    if not args.path.is_file():
        print(f"Validation skipped: {args.path} does not exist")
        return 0
    findings = validate_profile(args.path)
    for finding in findings:
        print(f"{finding.level} {args.path}:{finding.path}: {finding.message}")
    errors = sum(item.level == "ERROR" for item in findings)
    warnings = sum(item.level == "WARNING" for item in findings)
    print(f"Validation complete: {errors} error(s), {warnings} warning(s)")
    return 1 if errors or (args.warnings_as_errors and warnings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
