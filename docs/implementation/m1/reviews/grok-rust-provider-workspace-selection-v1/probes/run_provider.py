"""Provider workspace: private export, vendor, empty CARGO_HOME, build, refusals."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tomllib
from pathlib import Path

CARGO = "/opt/homebrew/Cellar/rust/1.95.0/bin/cargo"
RUSTC = "/opt/homebrew/Cellar/rust/1.95.0/bin/rustc"
PYTHON = "/tmp/opensip-implementation/metadata-reference-env/bin/python"
REVIEW = Path("/tmp/opensip-implementation/m2-grok-foundation-v2-provider-workspace-v1-review/review")
FROZEN_PRODUCT = REVIEW / "copy" / "provider-v1" / "product"
ARCH = Path("/Users/sb/code/opensip-ai/opensip_arch")
INV10 = ARCH / "docs/implementation/m1/repository-file-inventory.v10.json"
ARCHIVES = Path("/Users/sb/.cargo/registry/cache/index.crates.io-1949cf8c6b5b557f")
MSG = b"opensip Rust provider: native analysis is not implemented in this development build\n"
PROBE_LOCK = "be35cf233ca1a09d5187d871936cff9554607040f5ce3e01e4ac4a0f012e5176"


def pin(raw: bytes) -> dict:
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def main() -> None:
    if not sys.flags.isolated or sys.flags.optimize:
        raise SystemExit("isolated Python without optimization required")
    logs = REVIEW / "results" / "provider-logs"
    logs.mkdir(parents=True, exist_ok=True)
    work = REVIEW / "probes" / "provider-work"
    if work.exists():
        shutil.rmtree(work)
    export = work / "export"
    vendor = work / "vendor"
    cargo_home = work / "cargo-home"
    empty_home = work / "empty-home"
    target = work / "target"
    host_target = work / "host-target"
    for p in (export, vendor, cargo_home, empty_home, target, host_target):
        p.mkdir(parents=True)

    source = []
    extra_names = []
    for name in ["crates/contracts", "crates/identity", "providers/rust"]:
        for path in sorted((FROZEN_PRODUCT / name).rglob("*")):
            if path.is_file():
                if not (path.name in ["Cargo.toml", "Cargo.lock", "rust-toolchain.toml"] or path.suffix == ".rs"):
                    extra_names.append(path.name)
                rel = path.relative_to(FROZEN_PRODUCT).as_posix()
                raw = path.read_bytes()
                out = export / rel
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_bytes(raw)
                out.chmod(0o444)
                source.append({"path": rel, **pin(raw)})
    for path in sorted(export.rglob("*"), reverse=True):
        if path.is_dir() and path.is_relative_to(export / "crates"):
            path.chmod(0o555)

    isolation = {
        "rootCargoToml": (export / "Cargo.toml").exists(),
        "apps": (export / "apps").exists(),
        "tools": (export / "tools").exists(),
        "packageJson": (export / "package.json").exists(),
        "nodeModules": any(p.name == "node_modules" for p in export.rglob("*")),
    }
    shared = [r for r in source if r["path"].startswith("crates/")]
    provider = [r for r in source if r["path"].startswith("providers/rust/")]

    spec = importlib.util.spec_from_file_location(
        "archive_helper", FROZEN_PRODUCT / "tools/build_contracts.py"
    )
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    deps = []
    lock_path = export / "providers/rust/Cargo.lock"
    lock_sha_before = hashlib.sha256(lock_path.read_bytes()).hexdigest()
    lock = tomllib.loads(lock_path.read_text())
    for row in lock["package"]:
        if "source" not in row:
            continue
        if row["source"] != "registry+https://github.com/rust-lang/crates.io-index":
            raise SystemExit("unexpected lock source " + row["source"])
        name = row["name"] + "-" + row["version"]
        raw = (ARCHIVES / (name + ".crate")).read_bytes()
        deps.append(helper.unpack_archive(raw, row["name"], row["version"], row["checksum"], vendor / name))

    (cargo_home / "config.toml").write_text(
        '[source.crates-io]\nreplace-with = "verified-vendor"\n[source.verified-vendor]\ndirectory = '
        + json.dumps(str(vendor))
        + "\n"
    )
    for parent in [export / "providers/rust", * (export / "providers/rust").parents]:
        for n in ("config", "config.toml"):
            if (parent / ".cargo" / n).exists():
                raise SystemExit("implicit cargo config " + str(parent / ".cargo" / n))

    env = {
        "PATH": "/usr/bin:/bin",
        "HOME": str(empty_home),
        "CARGO_HOME": str(cargo_home),
        "RUSTC": RUSTC,
        "CARGO_TARGET_DIR": str(target),
        "LANG": "C",
        "LC_ALL": "C",
        "TZ": "UTC",
        "CARGO_INCREMENTAL": "0",
        "CARGO_TERM_COLOR": "never",
        "TERM": "dumb",
    }
    try:
        env["SDKROOT"] = subprocess.check_output(
            ["/usr/bin/xcrun", "--sdk", "macosx", "--show-sdk-path"], text=True
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        pass

    commands = []

    def run(name: str, cmd: list[str], expected: int = 0, **kwargs) -> subprocess.CompletedProcess:
        r = subprocess.run(
            cmd, cwd=export / "providers/rust", env=env, capture_output=True, timeout=300, **kwargs
        )
        (logs / f"{name}.stdout").write_bytes(r.stdout)
        (logs / f"{name}.stderr").write_bytes(r.stderr)
        commands.append({"name": name, "command": cmd, "exitCode": r.returncode, "expected": expected})
        if r.returncode != expected:
            raise SystemExit(f"{name} exit {r.returncode} expected {expected}: {r.stderr[-800:]}")
        return r

    run("cargo-version", [CARGO, "-vV"])
    run("rustc-version", [RUSTC, "-vV"])
    run("build", [CARGO, "build", "--locked", "--offline", "--target", "aarch64-apple-darwin"])
    run(
        "metadata",
        [CARGO, "metadata", "--locked", "--offline", "--format-version", "1",
         "--filter-platform", "aarch64-apple-darwin"],
    )
    run(
        "dependencies",
        [PYTHON, "-I", "-B", str(FROZEN_PRODUCT / "tools/check_dependencies.py"),
         "--manifest", str(export / "providers/rust/Cargo.toml"),
         "--target", "aarch64-apple-darwin", "--cargo", CARGO],
    )
    run(
        "edges",
        [PYTHON, "-I", "-B", str(FROZEN_PRODUCT / "tools/check_package_edges.py"),
         "--repository", str(export),
         "--metadata", str(logs / "metadata.stdout"),
         "--inventory", str(INV10), "--lane", "rust-provider"],
    )
    exe = target / "aarch64-apple-darwin" / "debug" / "opensip-rust-provider"
    refusals = []
    for i, data in enumerate([b"", b'{"kind":"hello"}\n', b"not a protocol frame\x00"]):
        r = run("unavailable-" + str(i), [str(exe)], 1, input=data)
        ok = r.stdout == b"" and r.stderr == MSG
        refusals.append({
            "name": "unavailable-" + str(i),
            "exitCode": r.returncode,
            "stdoutEmpty": r.stdout == b"",
            "stderrExact": r.stderr == MSG,
            "ok": ok,
        })
        if not ok:
            raise SystemExit("refusal mismatch " + str(i) + repr(r.stderr))

    lock_sha_after = hashlib.sha256(lock_path.read_bytes()).hexdigest()
    host_env = dict(env)
    host_env["CARGO_TARGET_DIR"] = str(host_target)
    host_env["CARGO_HOME"] = os.environ.get("CARGO_HOME", str(Path(os.environ["HOME"]) / ".cargo"))
    host_env["PATH"] = "/opt/homebrew/Cellar/rust/1.95.0/bin:/usr/bin:/bin:/usr/sbin:/sbin"
    host_meta = subprocess.run(
        [CARGO, "metadata", "--locked", "--offline", "--format-version", "1",
         "--filter-platform", "aarch64-apple-darwin",
         "--manifest-path", str(FROZEN_PRODUCT / "Cargo.toml")],
        env=host_env, capture_output=True, timeout=180,
    )
    (logs / "host-workspace-metadata.stdout").write_bytes(host_meta.stdout)
    (logs / "host-workspace-metadata.stderr").write_bytes(host_meta.stderr)
    host_names = []
    if host_meta.returncode == 0:
        host_json = json.loads(host_meta.stdout)
        host_names = sorted({row["name"] for row in host_json["packages"] if row.get("source") is None})
    provider_meta = json.loads((logs / "metadata.stdout").read_bytes())
    provider_local = sorted({row["name"] for row in provider_meta["packages"] if row.get("source") is None})
    provider_workspace = [row.split(" ")[0] if " " in row else row for row in provider_meta.get("workspace_members", [])]
    # workspace_members are ids like opensip-rust-provider 0.1.0
    workspace_names = sorted({pid.split(" ", 1)[0] for pid in provider_meta.get("workspace_members", [])})

    which_node = subprocess.run(["/usr/bin/which", "node"], env=env, capture_output=True)
    deps_out = (logs / "dependencies.stdout").read_text()
    edges_out = (logs / "edges.stdout").read_text()

    out = {
        "sourceCount": len(source),
        "sharedOwnerFiles": len(shared),
        "providerOwnedFiles": len(provider),
        "extraNonRsNames": extra_names,
        "archiveCount": len(deps),
        "isolation": isolation,
        "exportIsolated": not any(isolation.values()),
        "lockSha256Before": lock_sha_before,
        "lockSha256After": lock_sha_after,
        "lockUnchanged": lock_sha_before == lock_sha_after == PROBE_LOCK,
        "commands": commands,
        "refusals": refusals,
        "allRefusalsOk": all(r["ok"] for r in refusals),
        "executableExists": exe.is_file(),
        "hostWorkspaceLocalPackages": host_names,
        "hostIncludesRustProvider": "opensip-rust-provider" in host_names,
        "providerLocalPackages": provider_local,
        "providerWorkspaceNames": workspace_names,
        "hostMetadataExit": host_meta.returncode,
        "nodeOnEmptyPath": which_node.returncode == 0,
        "dependenciesStdout": deps_out,
        "edgesStdout": edges_out,
        "cargoHomeWasEmptyExceptVendorConfig": sorted(p.name for p in cargo_home.iterdir() if p.name != "config.toml"),
    }
    (REVIEW / "results" / "provider-reproduction.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "sources": len(source),
        "shared": len(shared),
        "provider": len(provider),
        "archives": len(deps),
        "exportIsolated": out["exportIsolated"],
        "lockUnchanged": out["lockUnchanged"],
        "buildExit": next(c["exitCode"] for c in commands if c["name"] == "build"),
        "depsExit": next(c["exitCode"] for c in commands if c["name"] == "dependencies"),
        "edgesExit": next(c["exitCode"] for c in commands if c["name"] == "edges"),
        "refusals": refusals,
        "hostIncludesProvider": out["hostIncludesRustProvider"],
        "hostLocal": host_names,
        "providerLocal": provider_local,
        "workspace": workspace_names,
        "node": out["nodeOnEmptyPath"],
        "extra": extra_names,
    }, indent=2))


if __name__ == "__main__":
    main()
