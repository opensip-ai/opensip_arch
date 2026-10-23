#!/usr/bin/env python3
"""Install or verify global discovery links for the OpenSIP agent bootstrap."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import sys


LINKS = (
    (Path(".codex/AGENTS.md"), Path("AGENTS.md")),
    (Path(".claude/CLAUDE.md"), Path("CLAUDE.md")),
)


def link_state(target: Path, source: Path) -> str:
    if not os.path.lexists(target):
        return "missing"
    if not target.is_symlink():
        return "occupied"
    return "current" if target.resolve() == source.resolve() else "different"


def run(action: str, home: Path, repository: Path) -> int:
    failed = False
    for relative_target, relative_source in LINKS:
        target = home / relative_target
        source = repository / relative_source
        state = link_state(target, source)
        if action == "install" and state == "missing":
            target.parent.mkdir(parents=True, exist_ok=True)
            target.symlink_to(source)
            state = "current"
        print(f"{target}: {state} -> {source}")
        failed |= state != "current"
    return 1 if failed else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("install", "check"))
    parser.add_argument("--home", type=Path, default=Path.home(), help=argparse.SUPPRESS)
    args = parser.parse_args()
    repository = Path(__file__).resolve().parent.parent
    return run(args.action, args.home.expanduser().resolve(), repository)


if __name__ == "__main__":
    sys.exit(main())
