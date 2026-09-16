"""Identity tests, Clippy, fmt on the private frozen product copy."""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

CARGO = "/opt/homebrew/Cellar/rust/1.95.0/bin/cargo"
REVIEW = Path("/tmp/opensip-implementation/m2-grok-array-order-selection-v1-review/review")
PRODUCT = REVIEW / "copy" / "frozen-subject" / "product"
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
    tests = subprocess.run(
        [CARGO, "test", "--locked", "--offline", "-p", "opensip-identity", "--all-targets"],
        env=env, cwd=PRODUCT, capture_output=True, timeout=180,
    )
    (logs / "identity-tests.stdout").write_bytes(tests.stdout)
    (logs / "identity-tests.stderr").write_bytes(tests.stderr)
    clippy = subprocess.run(
        [CARGO, "clippy", "--locked", "--offline", "-p", "opensip-identity", "--all-targets", "--", "-D", "warnings"],
        env=env, cwd=PRODUCT, capture_output=True, timeout=180,
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
        "testsTail": tests.stdout.decode()[-900:],
        "clippyTail": clippy.stderr.decode()[-300:],
        "fmtStderr": fmt.stderr.decode()[-300:],
    }
    (REVIEW / "results" / "identity-tests.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: out[k] for k in ("testsExit", "passed", "failed", "clippyExit", "fmtExit", "lockUnchanged", "nodeOnPath")}, indent=2))
    print(out["testsTail"][-500:])


if __name__ == "__main__":
    main()
