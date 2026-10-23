#!/usr/bin/env python3
"""Regression tests for global OpenSIP bootstrap discovery links."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest


MODULE_PATH = Path(__file__).with_name("install_agent_bootstrap.py")
SPEC = importlib.util.spec_from_file_location("install_agent_bootstrap", MODULE_PATH)
assert SPEC and SPEC.loader
INSTALLER = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = INSTALLER
SPEC.loader.exec_module(INSTALLER)


class InstallerTests(unittest.TestCase):
    def test_install_and_check(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            repository = MODULE_PATH.parent.parent
            self.assertEqual(INSTALLER.run("install", home, repository), 0)
            self.assertEqual(INSTALLER.run("check", home, repository), 0)
            self.assertEqual((home / ".codex/AGENTS.md").resolve(), repository / "AGENTS.md")
            self.assertEqual((home / ".claude/CLAUDE.md").resolve(), repository / "CLAUDE.md")

    def test_refuses_to_replace_existing_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            target = home / ".codex/AGENTS.md"
            target.parent.mkdir(parents=True)
            target.write_text("keep me", encoding="utf-8")
            self.assertEqual(INSTALLER.run("install", home, MODULE_PATH.parent.parent), 1)
            self.assertEqual(target.read_text(encoding="utf-8"), "keep me")


if __name__ == "__main__":
    unittest.main()
