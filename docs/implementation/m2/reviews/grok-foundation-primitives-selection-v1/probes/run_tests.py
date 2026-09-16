"""Reproduce workspace tests, clippy, fmt, dependency check and package edges."""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

CARGO = "/opt/homebrew/Cellar/rust/1.95.0/bin/cargo"
PYTHON = "/tmp/opensip-implementation/metadata-reference-env/bin/python"
REVIEW = Path("/tmp/opensip-implementation/m2-grok-foundation-primitives-selection-v1-review/review")
PRODUCT = REVIEW / "copy" / "frozen-subject" / "product"
LIVE = Path("/Users/sb/code/opensip-ai/opensip")
ARCH = Path("/Users/sb/code/opensip-ai/opensip_arch")
INV10 = ARCH / "docs/implementation/m1/repository-file-inventory.v10.json"
SAFE_PATH = "/opt/homebrew/Cellar/rust/1.95.0/bin:/usr/bin:/bin:/usr/sbin:/sbin"
CLEARED = [
    "RUSTFLAGS",
    "CARGO_ENCODED_RUSTFLAGS",
    "RUSTC_WRAPPER",
    "RUSTC_WORKSPACE_WRAPPER",
    "RUSTC_BOOTSTRAP",
    "RUSTUP_TOOLCHAIN",
]
TARGET = "aarch64-apple-darwin"


def env_for(target_dir: Path) -> dict[str, str]:
    env = {
        "HOME": os.environ["HOME"],
        "PATH": SAFE_PATH,
        "CARGO_TARGET_DIR": str(target_dir),
        "CARGO_TERM_COLOR": "never",
        "CARGO_HOME": os.environ.get("CARGO_HOME", str(Path(os.environ["HOME"]) / ".cargo")),
        "TMPDIR": str(REVIEW / "probes" / "tmp"),
        "TERM": "dumb",
    }
    sdk = os.environ.get("SDKROOT")
    if not sdk:
        try:
            sdk = subprocess.check_output(
                ["/usr/bin/xcrun", "--sdk", "macosx", "--show-sdk-path"], text=True
            ).strip()
        except (OSError, subprocess.CalledProcessError):
            sdk = None
    if sdk:
        env["SDKROOT"] = sdk
    return env


def run(cmd: list[str], env: dict[str, str], cwd: Path, timeout: int = 300) -> dict:
    proc = subprocess.run(cmd, env=env, cwd=cwd, capture_output=True, timeout=timeout)
    return {
        "command": cmd,
        "cwd": str(cwd),
        "exitCode": proc.returncode,
        "stdout": proc.stdout.decode("utf-8", "replace"),
        "stderr": proc.stderr.decode("utf-8", "replace"),
        "stdoutSha256": hashlib.sha256(proc.stdout).hexdigest(),
        "stderrSha256": hashlib.sha256(proc.stderr).hexdigest(),
        "stdoutBytes": len(proc.stdout),
        "stderrBytes": len(proc.stderr),
    }


def count_ok_tests(text: str) -> dict:
    passed = 0
    failed = 0
    suites = 0
    for line in text.splitlines():
        if line.startswith("test result:"):
            suites += 1
            parts = line.split()
            # test result: ok. N passed; M failed;
            try:
                p = parts.index("passed;")
                passed += int(parts[p - 1])
                f = parts.index("failed;")
                failed += int(parts[f - 1])
            except (ValueError, IndexError):
                continue
    return {"suites": suites, "passed": passed, "failed": failed}


def main() -> None:
    if not sys.flags.isolated or sys.flags.optimize:
        raise SystemExit("isolated Python without optimization required")
    logs = REVIEW / "results" / "logs"
    logs.mkdir(parents=True, exist_ok=True)
    (REVIEW / "probes" / "tmp").mkdir(parents=True, exist_ok=True)
    target = REVIEW / "probes" / "candidate-target"
    live_target = REVIEW / "probes" / "live-target"
    if target.exists():
        shutil.rmtree(target)
    if live_target.exists():
        shutil.rmtree(live_target)
    target.mkdir(parents=True)
    live_target.mkdir(parents=True)
    env = env_for(target)
    live_env = env_for(live_target)

    lock_before = hashlib.sha256((PRODUCT / "Cargo.lock").read_bytes()).hexdigest()
    live_lock_before = hashlib.sha256((LIVE / "Cargo.lock").read_bytes()).hexdigest()

    cargo_ver = run([CARGO, "--version", "--verbose"], env, PRODUCT, 30)
    rustc_ver = run(["/opt/homebrew/Cellar/rust/1.95.0/bin/rustc", "-vV"], env, PRODUCT, 30)
    which_node = subprocess.run(["/usr/bin/which", "node"], env=env, capture_output=True, text=True)

    tests = run(
        [CARGO, "test", "--locked", "--offline", "--workspace", "--all-targets"],
        env, PRODUCT, 300,
    )
    (logs / "tests.stdout").write_text(tests["stdout"])
    (logs / "tests.stderr").write_text(tests["stderr"])

    clippy = run(
        [CARGO, "clippy", "--locked", "--offline", "--workspace", "--all-targets", "--", "-D", "warnings"],
        env, PRODUCT, 300,
    )
    (logs / "clippy.stdout").write_text(clippy["stdout"])
    (logs / "clippy.stderr").write_text(clippy["stderr"])

    fmt = run([CARGO, "fmt", "--all", "--check"], env, PRODUCT, 60)
    (logs / "fmt.stdout").write_text(fmt["stdout"])
    (logs / "fmt.stderr").write_text(fmt["stderr"])

    deps = run(
        [PYTHON, "-I", "-B", str(PRODUCT / "tools/check_dependencies.py"),
         "--manifest", str(PRODUCT / "Cargo.toml"),
         "--target", TARGET, "--cargo", CARGO],
        env, PRODUCT, 120,
    )
    (logs / "dependencies.stdout").write_text(deps["stdout"])
    (logs / "dependencies.stderr").write_text(deps["stderr"])

    metadata = run(
        [CARGO, "metadata", "--locked", "--offline", "--format-version", "1",
         "--filter-platform", TARGET],
        env, PRODUCT, 120,
    )
    (logs / "metadata.stdout").write_text(metadata["stdout"])
    (logs / "metadata.stderr").write_text(metadata["stderr"])
    meta_path = logs / "metadata.stdout"

    edges = run(
        [PYTHON, "-I", "-B", str(PRODUCT / "tools/check_package_edges.py"),
         "--repository", str(PRODUCT),
         "--metadata", str(meta_path),
         "--inventory", str(INV10),
         "--lane", "host"],
        env, PRODUCT, 30,
    )
    (logs / "edges.stdout").write_text(edges["stdout"])
    (logs / "edges.stderr").write_text(edges["stderr"])

    live_meta = run(
        [CARGO, "metadata", "--locked", "--offline", "--format-version", "1",
         "--filter-platform", TARGET, "--manifest-path", str(LIVE / "Cargo.toml")],
        live_env, LIVE, 120,
    )
    (logs / "live-metadata.stdout").write_text(live_meta["stdout"])
    (logs / "live-metadata.stderr").write_text(live_meta["stderr"])

    lock_after = hashlib.sha256((PRODUCT / "Cargo.lock").read_bytes()).hexdigest()
    live_lock_after = hashlib.sha256((LIVE / "Cargo.lock").read_bytes()).hexdigest()

    counts = count_ok_tests(tests["stdout"])
    out = {
        "cargoVersion": cargo_ver["stdout"],
        "rustcVersion": rustc_ver["stdout"],
        "nodeOnPath": which_node.returncode == 0,
        "path": SAFE_PATH,
        "clearedCompilerEnvironment": CLEARED,
        "tests": {k: v for k, v in tests.items() if k not in {"stdout", "stderr"}} | {"counts": counts, "exitCode": tests["exitCode"]},
        "clippyExit": clippy["exitCode"],
        "fmtExit": fmt["exitCode"],
        "dependenciesExit": deps["exitCode"],
        "dependenciesStdout": deps["stdout"],
        "edgesExit": edges["exitCode"],
        "edgesStdout": edges["stdout"],
        "metadataExit": metadata["exitCode"],
        "liveMetadataExit": live_meta["exitCode"],
        "lockSha256Before": lock_before,
        "lockSha256After": lock_after,
        "lockUnchanged": lock_before == lock_after,
        "liveLockUnchanged": live_lock_before == live_lock_after,
        "liveLockSha256": live_lock_before,
        "clippyStderrTail": clippy["stderr"][-400:],
        "fmtStderr": fmt["stderr"],
        "testsStderrTail": tests["stderr"][-400:],
    }
    (REVIEW / "results" / "reproduction.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "testsExit": tests["exitCode"],
        "testCounts": counts,
        "clippyExit": clippy["exitCode"],
        "fmtExit": fmt["exitCode"],
        "depsExit": deps["exitCode"],
        "depsPassed": "\"passed\": true" in deps["stdout"],
        "edgesExit": edges["exitCode"],
        "edgesPassed": "\"passed\": true" in edges["stdout"],
        "metadataExit": metadata["exitCode"],
        "liveMetadataExit": live_meta["exitCode"],
        "lockUnchanged": out["lockUnchanged"],
        "liveLockUnchanged": out["liveLockUnchanged"],
        "nodeOnPath": out["nodeOnPath"],
        "clippyTail": clippy["stderr"][-300:],
        "testsFailTail": tests["stdout"][-400:] if tests["exitCode"] else "",
    }, indent=2))


if __name__ == "__main__":
    main()
