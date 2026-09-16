"""Private Cargo 1.95 build/run and metadata with Node excluded from PATH."""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

CARGO = "/opt/homebrew/Cellar/rust/1.95.0/bin/cargo"
RUSTC = "/opt/homebrew/Cellar/rust/1.95.0/bin/rustc"
RUST_BIN = "/opt/homebrew/Cellar/rust/1.95.0/bin"
SAFE_PATH = f"{RUST_BIN}:/usr/bin:/bin:/usr/sbin:/sbin"
CLEARED = [
    "RUSTFLAGS",
    "CARGO_ENCODED_RUSTFLAGS",
    "RUSTC_WRAPPER",
    "RUSTC_WORKSPACE_WRAPPER",
    "RUSTC_BOOTSTRAP",
    "RUSTUP_TOOLCHAIN",
]
REVIEW = Path("/tmp/opensip-implementation/m1-grok-pure-provider-isolation-02-review/review")
COPY = REVIEW / "copy" / "export"
PRODUCT = Path("/Users/sb/code/opensip-ai/opensip")
TARGET = "aarch64-apple-darwin"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def cargo_env(target_dir: Path) -> dict[str, str]:
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
            sdk = subprocess.check_output(["/usr/bin/xcrun", "--sdk", "macosx", "--show-sdk-path"], text=True).strip()
        except (OSError, subprocess.CalledProcessError):
            sdk = None
    if sdk:
        env["SDKROOT"] = sdk
    return env


def run(cmd: list[str], env: dict[str, str], cwd: Path | None = None, timeout: int = 180) -> dict:
    proc = subprocess.run(cmd, env=env, cwd=cwd, capture_output=True, timeout=timeout)
    return {
        "command": cmd,
        "cwd": None if cwd is None else str(cwd),
        "exitCode": proc.returncode,
        "stdoutBytes": len(proc.stdout),
        "stderrBytes": len(proc.stderr),
        "stdoutSha256": hashlib.sha256(proc.stdout).hexdigest(),
        "stderrSha256": hashlib.sha256(proc.stderr).hexdigest(),
        "stdout": proc.stdout.decode("utf-8", "replace"),
        "stderr": proc.stderr.decode("utf-8", "replace"),
    }


def which(name: str, env: dict[str, str]) -> dict:
    r = subprocess.run(["/usr/bin/which", name], env=env, capture_output=True, text=True)
    return {"name": name, "exitCode": r.returncode, "path": r.stdout.strip(), "stderr": r.stderr.strip()}


def main() -> None:
    if not sys.flags.isolated or sys.flags.optimize:
        raise SystemExit("isolated Python without optimization required")
    results = REVIEW / "results"
    logs = REVIEW / "results" / "logs"
    results.mkdir(parents=True, exist_ok=True)
    logs.mkdir(parents=True, exist_ok=True)
    (REVIEW / "probes" / "tmp").mkdir(parents=True, exist_ok=True)

    provider_target = REVIEW / "probes" / "provider-target"
    host_target = REVIEW / "probes" / "host-target"
    if provider_target.exists():
        shutil.rmtree(provider_target)
    if host_target.exists():
        shutil.rmtree(host_target)
    provider_target.mkdir(parents=True)
    host_target.mkdir(parents=True)

    env = cargo_env(provider_target)
    leaked = {name: os.environ.get(name) for name in CLEARED}
    present_in_env = [name for name in CLEARED if name in env]
    node_default = shutil.which("node")

    cargo_ver = run([CARGO, "--version", "--verbose"], env)
    rustc_ver = run([RUSTC, "-vV"], env)
    which_node = which("node", env)
    which_cargo = which("cargo", env)
    which_rustc = which("rustc", env)
    which_npm = which("npm", env)

    manifest = COPY / "providers/rust/Cargo.toml"
    lock_before = COPY / "providers/rust/Cargo.lock"
    lock_sha_before = sha256_file(lock_before)
    lock_bytes_before = lock_before.stat().st_size

    run_result = run(
        [CARGO, "run", "--locked", "--offline", "--manifest-path", str(manifest)],
        env,
        timeout=180,
    )
    (logs / "run.stdout").write_bytes(run_result["stdout"].encode())
    (logs / "run.stderr").write_bytes(run_result["stderr"].encode())

    metadata = run(
        [CARGO, "metadata", "--locked", "--offline", "--format-version", "1",
         "--filter-platform", TARGET, "--manifest-path", str(manifest)],
        env,
        timeout=120,
    )
    (logs / "provider-metadata.stdout").write_bytes(metadata["stdout"].encode())
    (logs / "provider-metadata.stderr").write_bytes(metadata["stderr"].encode())

    lock_sha_after = sha256_file(lock_before)
    shared_sources = []
    export_shared = [
        "crates/contracts/Cargo.toml",
        "crates/contracts/src/generated/evidence.rs",
        "crates/contracts/src/generated/identity.rs",
        "crates/contracts/src/generated/invocation.rs",
        "crates/contracts/src/generated/mod.rs",
        "crates/contracts/src/generated/output.rs",
        "crates/contracts/src/generated/protocol.rs",
        "crates/contracts/src/lib.rs",
        "crates/identity/Cargo.toml",
        "crates/identity/src/canonical.rs",
        "crates/identity/src/canonical_tests.rs",
        "crates/identity/src/digests.rs",
        "crates/identity/src/lib.rs",
    ]
    for rel in export_shared:
        p = COPY / rel
        shared_sources.append({
            "path": rel,
            "sha256": sha256_file(p),
            "mode": p.stat().st_mode & 0o777,
        })

    live_lock = PRODUCT / "Cargo.lock"
    live_lock_before = sha256_file(live_lock)
    host_env = cargo_env(host_target)
    host_meta = run(
        [CARGO, "metadata", "--locked", "--offline", "--format-version", "1",
         "--filter-platform", TARGET, "--manifest-path", str(PRODUCT / "Cargo.toml")],
        host_env,
        timeout=180,
    )
    (logs / "host-metadata.stdout").write_bytes(host_meta["stdout"].encode())
    (logs / "host-metadata.stderr").write_bytes(host_meta["stderr"].encode())
    live_lock_after = sha256_file(live_lock)

    binary = provider_target / "debug" / "opensip-rust-provider"
    binary_run = None
    if binary.is_file():
        binary_run = run([str(binary)], env, timeout=30)

    summary = {
        "cargoPath": CARGO,
        "rustcPath": RUSTC,
        "path": SAFE_PATH,
        "clearedCompilerEnvironment": CLEARED,
        "clearedVarsAbsentFromExecEnv": present_in_env == [],
        "clearedVarsInParentEnviron": {k: (v is not None) for k, v in leaked.items()},
        "nodeOnDefaultPath": node_default,
        "which": {
            "node": which_node,
            "cargo": which_cargo,
            "rustc": which_rustc,
            "npm": which_npm,
        },
        "cargoVersion": cargo_ver,
        "rustcVersion": rustc_ver,
        "manifest": str(manifest),
        "lockSha256Before": lock_sha_before,
        "lockBytesBefore": lock_bytes_before,
        "lockSha256After": lock_sha_after,
        "lockUnchanged": lock_sha_before == lock_sha_after,
        "run": {k: v for k, v in run_result.items() if k not in {"stdout"}},
        "runStdoutEmpty": run_result["stdout"] == "",
        "metadata": {k: v for k, v in metadata.items() if k not in {"stdout"}},
        "sharedSourcesAfterBuild": shared_sources,
        "sharedStillReadOnly": all(row["mode"] == 0o444 for row in shared_sources),
        "binaryExists": binary.is_file(),
        "binaryPath": str(binary),
        "binaryDirectRun": None if binary_run is None else {k: v for k, v in binary_run.items() if k not in {"stdout"}},
        "hostMetadata": {k: v for k, v in host_meta.items() if k not in {"stdout"}},
        "liveHostLockSha256Before": live_lock_before,
        "liveHostLockSha256After": live_lock_after,
        "liveHostLockUnchanged": live_lock_before == live_lock_after,
        "fullM1Complete": False,
        "compilerAttestation": False,
        "sandbox": False,
    }
    (results / "cargo-run.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    (logs / "cargo-version.stdout").write_text(cargo_ver["stdout"])
    (logs / "cargo-version.stderr").write_text(cargo_ver["stderr"])
    (logs / "rustc-version.stdout").write_text(rustc_ver["stdout"])
    (logs / "rustc-version.stderr").write_text(rustc_ver["stderr"])
    print(json.dumps({
        "cargoExit": cargo_ver["exitCode"],
        "rustcExit": rustc_ver["exitCode"],
        "nodeOnPath": which_node["exitCode"] == 0,
        "runExit": run_result["exitCode"],
        "metadataExit": metadata["exitCode"],
        "hostMetadataExit": host_meta["exitCode"],
        "lockUnchanged": summary["lockUnchanged"],
        "liveHostLockUnchanged": summary["liveHostLockUnchanged"],
        "sharedStillReadOnly": summary["sharedStillReadOnly"],
        "binaryExists": summary["binaryExists"],
        "binaryDirectExit": None if binary_run is None else binary_run["exitCode"],
        "runStderrTail": run_result["stderr"][-500:],
        "whichNode": which_node,
        "whichCargo": which_cargo,
        "cargoVersionHead": cargo_ver["stdout"].splitlines()[:1],
        "rustcVersionHead": rustc_ver["stdout"].splitlines()[:1],
    }, indent=2))


if __name__ == "__main__":
    main()
