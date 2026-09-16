"""Workspace tests/clippy/fmt on the private copy; skip original candidate path."""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

CARGO = "/opt/homebrew/Cellar/rust/1.95.0/bin/cargo"
REVIEW = Path("/tmp/opensip-implementation/m1-grok-required-delivery-selection-v1-review/review")
PRODUCT = REVIEW / "copy" / "frozen-subject" / "product"
SAFE_PATH = "/opt/homebrew/Cellar/rust/1.95.0/bin:/usr/bin:/bin:/usr/sbin:/sbin"


def env_for(target: Path) -> dict[str, str]:
    env = {
        "HOME": os.environ["HOME"],
        "PATH": SAFE_PATH,
        "CARGO_TARGET_DIR": str(target),
        "CARGO_TERM_COLOR": "never",
        "CARGO_HOME": os.environ.get("CARGO_HOME", str(Path(os.environ["HOME"]) / ".cargo")),
        "TMPDIR": "/tmp/osip-rdlv",
        "TERM": "dumb",
    }
    try:
        env["SDKROOT"] = subprocess.check_output(
            ["/usr/bin/xcrun", "--sdk", "macosx", "--show-sdk-path"], text=True
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        pass
    return env


def main() -> None:
    if not sys.flags.isolated or sys.flags.optimize:
        raise SystemExit("isolated Python without optimization required")
    Path("/tmp/osip-rdlv").mkdir(exist_ok=True)
    logs = REVIEW / "results" / "logs"
    logs.mkdir(parents=True, exist_ok=True)
    target = REVIEW / "probes" / "ws-target"
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True)
    env = env_for(target)
    lock_before = hashlib.sha256((PRODUCT / "Cargo.lock").read_bytes()).hexdigest()
    tests = subprocess.run(
        [CARGO, "test", "--locked", "--offline", "--workspace", "--all-targets"],
        env=env, cwd=PRODUCT, capture_output=True, timeout=300,
    )
    (logs / "tests.stdout").write_bytes(tests.stdout)
    (logs / "tests.stderr").write_bytes(tests.stderr)
    clippy = subprocess.run(
        [CARGO, "clippy", "--locked", "--offline", "--workspace", "--all-targets", "--", "-D", "warnings"],
        env=env, cwd=PRODUCT, capture_output=True, timeout=300,
    )
    fmt = subprocess.run(
        [CARGO, "fmt", "--all", "--check"],
        env=env, cwd=PRODUCT, capture_output=True, timeout=60,
    )
    lock_after = hashlib.sha256((PRODUCT / "Cargo.lock").read_bytes()).hexdigest()
    passed = failed = 0
    for line in tests.stdout.decode().splitlines():
        if line.startswith("test result:"):
            parts = line.split()
            try:
                passed += int(parts[parts.index("passed;") - 1])
                failed += int(parts[parts.index("failed;") - 1])
            except (ValueError, IndexError):
                pass
    out = {
        "testsExit": tests.returncode,
        "passed": passed,
        "failed": failed,
        "clippyExit": clippy.returncode,
        "fmtExit": fmt.returncode,
        "lockUnchanged": lock_before == lock_after,
        "nodeOnPath": subprocess.run(["/usr/bin/which", "node"], env=env, capture_output=True).returncode == 0,
        "testsTail": tests.stdout.decode()[-1200:],
        "clippyTail": clippy.stderr.decode()[-400:],
        "executedAgainstOriginalCandidate": False,
    }
    (REVIEW / "results" / "workspace-tests.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: out[k] for k in ("testsExit", "passed", "failed", "clippyExit", "fmtExit", "lockUnchanged", "nodeOnPath")}, indent=2))
    print(out["testsTail"][-600:])


if __name__ == "__main__":
    main()
