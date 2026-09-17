"""Real Cargo metadata and exact-source controls; not approval fixtures."""
from pathlib import Path
import argparse
import importlib.util
import json
import os
import shutil
import subprocess
import tempfile
import tomllib
import unittest

TOOL = Path(__file__).resolve().parents[1] / 'check_dependencies.py'
SPEC = importlib.util.spec_from_file_location('dependency_check', TOOL)
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)


class DependencyPolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix='opensip-contracts-policy-')
        cls.addClassCleanup(cls.temp.cleanup)
        cls.root = Path(cls.temp.name) / 'product'
        shutil.copytree(Path(__file__).resolve().parents[2], cls.root,
                        ignore=shutil.ignore_patterns('.git', 'target', 'node_modules',
                                                      'python-packages', '__pycache__', 'dist'))
        cls.env = dict(os.environ, CARGO_TARGET_DIR=str(Path(cls.temp.name) / 'target'))
        cls.policy = json.loads((cls.root / 'tools/contracts/dependency-policy.json').read_bytes())
        cls.original_lock = (cls.root / 'Cargo.lock').read_bytes()

    def check(self, policy=None):
        result = subprocess.run(
            [CARGO, 'metadata', '--locked', '--offline', '--format-version', '1',
             '--filter-platform', TARGET, '--manifest-path', str(self.root / 'Cargo.toml')],
            env=self.env, capture_output=True, timeout=120)
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        raw = (self.root / 'Cargo.lock').read_bytes()
        self.assertEqual(raw, self.original_lock)
        return CHECKER.check(json.loads(result.stdout), tomllib.loads(raw.decode()),
                             self.policy if policy is None else policy)

    def test_selected_source_and_dependency_profile(self):
        result = self.check()
        self.assertTrue(result['passed'])
        self.assertEqual(result['dependencyCount'], 11)
        self.assertEqual(result['localSourceFilesVerified'], 8)

    def test_another_workspace_member_cannot_expand_features(self):
        file = self.root / 'crates/reporting/Cargo.toml'
        before = file.read_bytes()
        text = before.decode()
        self.assertEqual(text.count('serde_json = "=1.0.151"'), 1)
        try:
            file.write_text(text.replace('serde_json = "=1.0.151"',
                'serde_json = { version = "=1.0.151", features = ["raw_value"] }'))
            with self.assertRaisesRegex(CHECKER.DependencyError, 'unselected resolved features: serde_json'):
                self.check()
        finally:
            file.write_bytes(before)

    def test_added_effectful_code_refuses(self):
        file = self.root / 'crates/contracts/src/lib.rs'
        before = file.read_bytes()
        try:
            file.write_bytes(before + b'\npub fn effect() { let _ = std::fs::read("not-an-admitted-input"); }\n')
            with self.assertRaisesRegex(CHECKER.DependencyError, 'local contracts source bytes differ'):
                self.check()
        finally:
            file.write_bytes(before)

    def test_extra_source_refuses(self):
        file = self.root / 'crates/contracts/src/unselected.rs'
        self.assertFalse(file.exists())
        try:
            file.write_text('pub const EXTRA: bool = true;\n')
            with self.assertRaisesRegex(CHECKER.DependencyError, 'local contracts source set differs'):
                self.check()
        finally:
            file.unlink()

    def test_linked_source_refuses_even_with_same_bytes(self):
        file = self.root / 'crates/contracts/src/lib.rs'
        before = file.read_bytes()
        same = Path(self.temp.name) / 'same.rs'
        same.write_bytes(before)
        file.unlink()
        try:
            file.symlink_to(same)
            with self.assertRaisesRegex(CHECKER.DependencyError, 'linked contracts source refused'):
                self.check()
        finally:
            file.unlink()
            file.write_bytes(before)

    @unittest.skipUnless(hasattr(os, 'mkfifo'), 'Unix developer profile')
    def test_nonregular_extra_source_refuses_without_reading(self):
        file = self.root / 'crates/contracts/src/pipe.rs'
        os.mkfifo(file)
        try:
            with self.assertRaisesRegex(CHECKER.DependencyError, 'nonregular contracts source refused'):
                self.check()
        finally:
            file.unlink()

    def test_duplicate_source_pin_refuses(self):
        policy = {**self.policy, 'localSources': [*self.policy['localSources'], self.policy['localSources'][0]]}
        with self.assertRaisesRegex(CHECKER.DependencyError, 'sorted, unique'):
            self.check(policy)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cargo', required=True)
    parser.add_argument('--target', required=True)
    args, remaining = parser.parse_known_args()
    CARGO = str(Path(args.cargo).resolve(strict=True))
    TARGET = args.target
    unittest.main(argv=[__file__, *remaining])
