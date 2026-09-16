"""Identity tests, Clippy, and independent schema/oracle comparison."""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

CARGO = "/opt/homebrew/Cellar/rust/1.95.0/bin/cargo"
REVIEW = Path("/tmp/opensip-implementation/m2-grok-logical-path-selection-v1-review/review")
COPY = REVIEW / "copy" / "frozen-subject"
PRODUCT = COPY / "product"
SAFE_PATH = "/opt/homebrew/Cellar/rust/1.95.0/bin:/usr/bin:/bin:/usr/sbin:/sbin"


def env_for(target: Path) -> dict[str, str]:
    env = {
        "HOME": os.environ["HOME"],
        "PATH": SAFE_PATH,
        "CARGO_TARGET_DIR": str(target),
        "CARGO_TERM_COLOR": "never",
        "CARGO_HOME": os.environ.get("CARGO_HOME", str(Path(os.environ["HOME"]) / ".cargo")),
        "TMPDIR": str(REVIEW / "probes" / "tmp"),
        "TERM": "dumb",
    }
    try:
        env["SDKROOT"] = subprocess.check_output(
            ["/usr/bin/xcrun", "--sdk", "macosx", "--show-sdk-path"], text=True
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        pass
    return env


def run(cmd, env, cwd, timeout=180):
    proc = subprocess.run(cmd, env=env, cwd=cwd, capture_output=True, timeout=timeout)
    return proc


def main() -> None:
    if not sys.flags.isolated or sys.flags.optimize:
        raise SystemExit("isolated Python without optimization required")
    logs = REVIEW / "results" / "logs"
    logs.mkdir(parents=True, exist_ok=True)
    (REVIEW / "probes" / "tmp").mkdir(parents=True, exist_ok=True)
    target = REVIEW / "probes" / "identity-target"
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True)
    env = env_for(target)
    lock_before = hashlib.sha256((PRODUCT / "Cargo.lock").read_bytes()).hexdigest()

    tests = run(
        [CARGO, "test", "--locked", "--offline", "-p", "opensip-identity", "--all-targets"],
        env, PRODUCT,
    )
    (logs / "tests.stdout").write_bytes(tests.stdout)
    (logs / "tests.stderr").write_bytes(tests.stderr)
    clippy = run(
        [CARGO, "clippy", "--locked", "--offline", "-p", "opensip-identity", "--all-targets", "--", "-D", "warnings"],
        env, PRODUCT,
    )
    (logs / "clippy.stdout").write_bytes(clippy.stdout)
    (logs / "clippy.stderr").write_bytes(clippy.stderr)
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
        "lockUnchanged": lock_before == lock_after,
        "nodeOnPath": subprocess.run(["/usr/bin/which", "node"], env=env, capture_output=True).returncode == 0,
        "testsTail": tests.stdout.decode()[-800:],
        "clippyTail": clippy.stderr.decode()[-400:],
    }
    (REVIEW / "results" / "identity-tests.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
