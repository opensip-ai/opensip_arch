"""Foundation v2: 30 tests with long TMPDIR, clippy/fmt/deps/edges, feature comparison."""
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
REVIEW = Path("/tmp/opensip-implementation/m2-grok-foundation-v2-provider-workspace-v1-review/review")
PRODUCT = REVIEW / "copy" / "foundation-v2" / "product"
LIVE = Path("/Users/sb/code/opensip-ai/opensip")
INV10 = Path("/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m1/repository-file-inventory.v10.json")
SAFE_PATH = "/opt/homebrew/Cellar/rust/1.95.0/bin:/usr/bin:/bin:/usr/sbin:/sbin"
TARGET = "aarch64-apple-darwin"
LONG_TMP = Path(
    "/tmp/osip-m2v2-long-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
)


def env_for(target_dir: Path) -> dict[str, str]:
    env = {
        "HOME": os.environ["HOME"],
        "PATH": SAFE_PATH,
        "CARGO_TARGET_DIR": str(target_dir),
        "CARGO_TERM_COLOR": "never",
        "CARGO_HOME": os.environ.get("CARGO_HOME", str(Path(os.environ["HOME"]) / ".cargo")),
        "TMPDIR": str(LONG_TMP),
        "TERM": "dumb",
    }
    try:
        env["SDKROOT"] = subprocess.check_output(
            ["/usr/bin/xcrun", "--sdk", "macosx", "--show-sdk-path"], text=True
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        pass
    return env


def run(cmd: list[str], env: dict[str, str], cwd: Path, timeout: int = 300) -> dict:
    proc = subprocess.run(cmd, env=env, cwd=cwd, capture_output=True, timeout=timeout)
    return {
        "command": cmd,
        "exitCode": proc.returncode,
        "stdout": proc.stdout.decode("utf-8", "replace"),
        "stderr": proc.stderr.decode("utf-8", "replace"),
    }


def count_tests(text: str) -> dict:
    passed = failed = 0
    for line in text.splitlines():
        if line.startswith("test result:"):
            parts = line.split()
            try:
                passed += int(parts[parts.index("passed;") - 1])
                failed += int(parts[parts.index("failed;") - 1])
            except (ValueError, IndexError):
                pass
    return {"passed": passed, "failed": failed}


def index(meta: dict) -> dict:
    packages = {row["id"]: row for row in meta["packages"]}
    nodes = {row["id"]: row for row in meta["resolve"]["nodes"]}
    by = {}
    for pid, pkg in packages.items():
        if pkg.get("source") is None:
            continue
        node = nodes[pid]
        by[pkg["name"]] = {
            "name": pkg["name"],
            "version": pkg["version"],
            "source": pkg.get("source"),
            "features": sorted(node.get("features") or []),
        }
    return by


def main() -> None:
    if not sys.flags.isolated or sys.flags.optimize:
        raise SystemExit("isolated Python without optimization required")
    logs = REVIEW / "results" / "foundation-logs"
    logs.mkdir(parents=True, exist_ok=True)
    LONG_TMP.mkdir(parents=True, exist_ok=True)
    sun_path = 104
    assert len(str(LONG_TMP)) > sun_path, (len(str(LONG_TMP)), str(LONG_TMP))
    target = REVIEW / "probes" / "foundation-target"
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

    tests = run([CARGO, "test", "--locked", "--offline", "--workspace", "--all-targets"], env, PRODUCT)
    (logs / "tests-long-tmpdir.stdout").write_text(tests["stdout"])
    (logs / "tests-long-tmpdir.stderr").write_text(tests["stderr"])
    clippy = run(
        [CARGO, "clippy", "--locked", "--offline", "--workspace", "--all-targets", "--", "-D", "warnings"],
        env, PRODUCT,
    )
    fmt = run([CARGO, "fmt", "--all", "--check"], env, PRODUCT, 60)
    deps = run(
        [PYTHON, "-I", "-B", str(PRODUCT / "tools/check_dependencies.py"),
         "--manifest", str(PRODUCT / "Cargo.toml"), "--target", TARGET, "--cargo", CARGO],
        env, PRODUCT, 120,
    )
    metadata = run(
        [CARGO, "metadata", "--locked", "--offline", "--format-version", "1", "--filter-platform", TARGET],
        env, PRODUCT, 120,
    )
    (logs / "metadata.stdout").write_text(metadata["stdout"])
    edges = run(
        [PYTHON, "-I", "-B", str(PRODUCT / "tools/check_package_edges.py"),
         "--repository", str(PRODUCT), "--metadata", str(logs / "metadata.stdout"),
         "--inventory", str(INV10), "--lane", "host"],
        env, PRODUCT, 30,
    )
    live_meta = run(
        [CARGO, "metadata", "--locked", "--offline", "--format-version", "1",
         "--filter-platform", TARGET, "--manifest-path", str(LIVE / "Cargo.toml")],
        live_env, LIVE, 120,
    )
    (logs / "live-metadata.stdout").write_text(live_meta["stdout"])

    cand = index(json.loads(metadata["stdout"])) if metadata["exitCode"] == 0 else {}
    live = index(json.loads(live_meta["stdout"])) if live_meta["exitCode"] == 0 else {}
    shared = sorted(set(cand) & set(live))
    unequal = []
    rows = []
    for name in shared:
        eq = cand[name] == live[name]
        rows.append({**cand[name], "equalLive": eq})
        if not eq:
            unequal.append(name)
    libc_features = cand.get("libc", {}).get("features")
    lock_after = hashlib.sha256((PRODUCT / "Cargo.lock").read_bytes()).hexdigest()
    live_lock_after = hashlib.sha256((LIVE / "Cargo.lock").read_bytes()).hexdigest()
    counts = count_tests(tests["stdout"])
    which_node = subprocess.run(["/usr/bin/which", "node"], env=env, capture_output=True)

    out = {
        "longTmpdir": str(LONG_TMP),
        "longTmpdirLen": len(str(LONG_TMP)),
        "longerThanSunPath": len(str(LONG_TMP)) > sun_path,
        "testsExit": tests["exitCode"],
        "testCounts": counts,
        "clippyExit": clippy["exitCode"],
        "fmtExit": fmt["exitCode"],
        "depsExit": deps["exitCode"],
        "depsStdout": deps["stdout"],
        "edgesExit": edges["exitCode"],
        "edgesStdout": edges["stdout"],
        "metadataExit": metadata["exitCode"],
        "liveMetadataExit": live_meta["exitCode"],
        "externalShared": len(shared),
        "allExternalEqualLive": not unequal,
        "unequal": unequal,
        "libcFeatures": libc_features,
        "rows": rows,
        "lockUnchanged": lock_before == lock_after,
        "liveLockUnchanged": live_lock_before == live_lock_after,
        "nodeOnPath": which_node.returncode == 0,
        "testsFailTail": tests["stdout"][-800:] if tests["exitCode"] else "",
        "clippyTail": clippy["stderr"][-400:],
    }
    (REVIEW / "results" / "foundation-reproduction.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "testsExit": tests["exitCode"],
        "counts": counts,
        "clippy": clippy["exitCode"],
        "fmt": fmt["exitCode"],
        "deps": deps["exitCode"],
        "edges": edges["exitCode"],
        "external": len(shared),
        "allEqual": not unequal,
        "unequal": unequal,
        "libcFeatures": libc_features,
        "lockUnchanged": out["lockUnchanged"],
        "tmpdirLen": len(str(LONG_TMP)),
        "node": out["nodeOnPath"],
        "failTail": out["testsFailTail"][-500:],
    }, indent=2))


if __name__ == "__main__":
    main()
