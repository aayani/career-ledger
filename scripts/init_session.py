#!/usr/bin/env python3
"""Create an isolated workspace for a new agent session."""

from __future__ import annotations

import shutil
from datetime import datetime, timezone
from pathlib import Path


def init_session(repo_root: Path, now: datetime | None = None) -> Path:
    repo_root = repo_root.resolve()
    current = now or datetime.now(timezone.utc)
    timestamp = current.astimezone(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    session_dir = repo_root / ".sessions" / f"session-{timestamp}"

    session_dir.mkdir(parents=True)
    (session_dir / "artifacts").mkdir()
    shutil.copy2(
        repo_root / ".agents" / "skills" / "career-ledger" / "references" / "checklist.md",
        session_dir / "checklist.md",
    )

    return session_dir


def main() -> None:
    repo_root = Path(__file__).resolve().parent.parent
    session_dir = init_session(repo_root)
    print(session_dir.relative_to(repo_root))


if __name__ == "__main__":
    main()
