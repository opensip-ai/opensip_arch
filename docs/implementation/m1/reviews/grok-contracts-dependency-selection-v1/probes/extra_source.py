"""Independent extra-source / false-negative probes. Private copy only."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import tomllib
from pathlib import Path

CARGO = "/opt/homebrew/Cellar/rust/1.95.0/bin/cargo"
TARGET = "aarch64-apple-darwin"
SRC = Path("/tmp/opensip-implementation/m1-grok-contracts-dependency-selection-v1-review/review/copy/frozen-product")
OUT = Path("/tmp/opensip-implementation/m1-grok-contracts-dependency-selection-v1-review/review/results/extra-source.json")
TOOL = SRC / "tools/check_dependencies.py"


def main():
    if not sys.flags.isolated or sys.flags.optimize:
        raise SystemExit("isolated Python without optimization required")
    spec = importlib.util.spec_from_file_location("dependency_check", TOOL)
    checker = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(checker)
    temp = tempfile.mkdtemp(prefix="opensip-dep-extra-")
    root = Path(temp) / "product"
    shutil.copytree(SRC, root, ignore=shutil.ignore_patterns(".git", "target", "node_modules", "python-packages", "__pycache__", "dist"))
    env = dict(os.environ, CARGO_TARGET_DIR=str(Path(temp) / "target"))
    policy = json.loads((root / "tools/contracts/dependency-policy.json").read_bytes())

    def run_check(pol=None):
        r = subprocess.run(
            [CARGO, "metadata", "--locked", "--offline", "--format-version", "1",
             "--filter-platform", TARGET, "--manifest-path", str(root / "Cargo.toml")],
            env=env, capture_output=True, timeout=120,
        )
        if r.returncode != 0:
            raise RuntimeError(r.stderr.decode())
        return checker.check(json.loads(r.stdout), tomllib.loads((root / "Cargo.lock").read_text()), pol or policy)

    rows = []

    def case(name, fn):
        try:
            outcome = fn()
            rows.append({"name": name, **outcome})
        except Exception as exc:
            rows.append({"name": name, "error": f"{type(exc).__name__}: {exc}"})
        print(name, rows[-1].get("passed", rows[-1].get("error")))

    def baseline():
        r = run_check()
        return {"passed": r["passed"], "deps": r["dependencyCount"], "sources": r["localSourceFilesVerified"]}

    def extra_outside_src():
        p = root / "crates/contracts/unselected_root.rs"
        p.write_text("pub const EXTRA: bool = true;\n")
        try:
            r = run_check()
            return {"passed": r["passed"], "falseNegativeIfPassed": r["passed"]}
        except checker.DependencyError as exc:
            return {"passed": False, "reason": str(exc), "falseNegativeIfPassed": False}
        finally:
            p.unlink()

    def extra_tests_dir():
        d = root / "crates/contracts/tests"
        d.mkdir(exist_ok=True)
        p = d / "probe.rs"
        p.write_text("#[test] fn x() {}\n")
        try:
            r = run_check()
            return {"passed": r["passed"], "falseNegativeIfPassed": r["passed"]}
        except checker.DependencyError as exc:
            return {"passed": False, "reason": str(exc), "falseNegativeIfPassed": False}
        finally:
            p.unlink()
            d.rmdir()

    def v1_policy_refuses():
        pol = {k: v for k, v in policy.items() if k != "localSources"}
        pol["schemaVersion"] = 1
        try:
            run_check(pol)
            return {"passed": True, "unexpectedPass": True}
        except checker.DependencyError as exc:
            return {"passed": False, "reason": str(exc), "unexpectedPass": False}

    case("baseline", baseline)
    case("extra-outside-src", extra_outside_src)
    case("extra-tests-dir", extra_tests_dir)
    case("schemaversion-1-refuses", v1_policy_refuses)
    shutil.rmtree(temp, ignore_errors=True)
    OUT.write_text(json.dumps({"cases": rows}, indent=2) + "\n")
    print(json.dumps({"cases": [{k: c[k] for k in c if k != "deps"} for c in rows]}, indent=2))


if __name__ == "__main__":
    main()
