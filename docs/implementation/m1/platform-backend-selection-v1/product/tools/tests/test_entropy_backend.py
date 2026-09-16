"""Actual Cargo controls for the platform entropy backend build guard.

Run with the selected Cargo executable and explicitly provisioned crate cache.
This copies the developer checkout and never fetches archives or edits it.
"""
from pathlib import Path
import argparse
import json
import os
import shutil
import subprocess
import tempfile
import unittest


class EntropyBackendTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix="opensip-entropy-build-")
        cls.addClassCleanup(cls.temp.cleanup)
        cls.root = Path(cls.temp.name) / "product"
        repository = Path(__file__).resolve().parents[2]
        shutil.copytree(repository, cls.root, ignore=shutil.ignore_patterns(
            ".git", "target", "node_modules", "python-packages", "__pycache__", "dist"))
        cls.environment = dict(os.environ)
        for key in ("RUSTFLAGS", "CARGO_ENCODED_RUSTFLAGS"):
            cls.environment.pop(key, None)
        cls.environment["CARGO_TARGET_DIR"] = str(Path(cls.temp.name) / "target")
        cls.command = [CARGO, "check", "--locked", "--offline", "-p", "opensip-platform"]

    def cargo(self, extra=(), environment=None):
        return subprocess.run(
            [*self.command, *extra], cwd=self.root,
            env={**self.environment, **(environment or {})},
            capture_output=True, text=True, timeout=120)

    def assert_guard(self, result):
        self.assertNotEqual(result.returncode, 0, "explicit backend unexpectedly compiled")
        self.assertIn("OpenSIP refuses an explicit getrandom_backend override", result.stderr)

    def test_default_backend_builds(self):
        result = self.cargo()
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_environment_flags_refuse(self):
        self.assert_guard(self.cargo(environment={
            "RUSTFLAGS": '--cfg getrandom_backend="unsupported"'}))

    def test_encoded_flags_refuse(self):
        self.assert_guard(self.cargo(environment={
            "CARGO_ENCODED_RUSTFLAGS": '--cfg\x1fgetrandom_backend="unsupported"'}))

    def test_cargo_configuration_refuses(self):
        flags = ["--cfg", 'getrandom_backend="unsupported"']
        self.assert_guard(self.cargo(("--config", "build.rustflags=" + json.dumps(flags))))

    def test_ineffective_flags_do_not_change_backend(self):
        # Cargo gives encoded flags precedence, including an explicit empty set.
        # The guard follows effective cfg, not an ignored ambient string.
        result = self.cargo(environment={
            "RUSTFLAGS": '--cfg getrandom_backend="unsupported"',
            "CARGO_ENCODED_RUSTFLAGS": ""})
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cargo", required=True)
    args, remaining = parser.parse_known_args()
    CARGO = str(Path(args.cargo).resolve(strict=True))
    unittest.main(argv=[__file__, *remaining])
