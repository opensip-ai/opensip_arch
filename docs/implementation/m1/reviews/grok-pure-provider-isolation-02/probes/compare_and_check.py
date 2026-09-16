"""Compare host/provider resolved packages and run proposed checker plus package-edges."""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

CARGO = "/opt/homebrew/Cellar/rust/1.95.0/bin/cargo"
REVIEW = Path("/tmp/opensip-implementation/m1-grok-pure-provider-isolation-02-review/review")
COPY = REVIEW / "copy" / "export"
ARCH = Path("/Users/sb/code/opensip-ai/opensip_arch")
PRODUCT = Path("/Users/sb/code/opensip-ai/opensip")
PYTHON = "/tmp/opensip-implementation/metadata-reference-env/bin/python"
CHECKER = ARCH / "docs/implementation/m1/contracts-dependency-selection-v1/product/tools/check_dependencies.py"
POLICY = ARCH / "docs/implementation/m1/contracts-dependency-selection-v1/product/tools/contracts/dependency-policy.json"
EDGES = PRODUCT / "tools/check_package_edges.py"
INV10 = ARCH / "docs/implementation/m1/repository-file-inventory.v10.json"
INV9 = ARCH / "docs/implementation/m1/repository-file-inventory.v9.json"
TARGET = "aarch64-apple-darwin"
SAFE_PATH = "/opt/homebrew/Cellar/rust/1.95.0/bin:/usr/bin:/bin:/usr/sbin:/sbin"
CLEARED = [
    "RUSTFLAGS",
    "CARGO_ENCODED_RUSTFLAGS",
    "RUSTC_WRAPPER",
    "RUSTC_WORKSPACE_WRAPPER",
    "RUSTC_BOOTSTRAP",
    "RUSTUP_TOOLCHAIN",
]


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
    for name in CLEARED:
        env.pop(name, None)
    sdk = os.environ.get("SDKROOT")
    if sdk:
        env["SDKROOT"] = sdk
    return env


def index_metadata(data: dict) -> dict[str, dict]:
    packages = {row["id"]: row for row in data["packages"]}
    nodes = {row["id"]: row for row in data["resolve"]["nodes"]}
    by_name: dict[str, dict] = {}
    for pid, pkg in packages.items():
        node = nodes[pid]
        by_name[pkg["name"]] = {
            "id": pid,
            "name": pkg["name"],
            "version": pkg["version"],
            "source": pkg.get("source"),
            "features": sorted(node.get("features") or []),
            "manifest_path": pkg.get("manifest_path"),
        }
    return by_name


def main() -> None:
    if not sys.flags.isolated or sys.flags.optimize:
        raise SystemExit("isolated Python without optimization required")
    results = REVIEW / "results"
    provider_meta = json.loads((results / "logs" / "provider-metadata.stdout").read_bytes())
    host_meta = json.loads((results / "logs" / "host-metadata.stdout").read_bytes())
    claimed = json.loads((ARCH / "docs/implementation/m1/trials/pure-provider-isolation-02/comparison.json").read_bytes())

    provider = index_metadata(provider_meta)
    host = index_metadata(host_meta)
    provider_only = sorted(set(provider) - set(host))
    host_only = sorted(set(host) - set(provider))
    shared_names = sorted(set(provider) & set(host))
    shared_rows = []
    unequal = []
    for name in shared_names:
        a, b = provider[name], host[name]
        equal = a["version"] == b["version"] and a["source"] == b["source"] and a["features"] == b["features"]
        row = {
            "name": name,
            "providerVersion": a["version"],
            "hostVersion": b["version"],
            "providerSource": a["source"],
            "hostSource": b["source"],
            "providerFeatures": a["features"],
            "hostFeatures": b["features"],
            "equal": equal,
        }
        shared_rows.append(row)
        if not equal:
            unequal.append(name)

    claimed_by_name = {row["name"]: row for row in claimed["packages"]}
    claimed_mismatch = []
    for row in shared_rows:
        c = claimed_by_name.get(row["name"])
        if c is None:
            claimed_mismatch.append(row["name"] + ": missing from claimed comparison")
            continue
        if (
            c["version"] != row["providerVersion"]
            or c["source"] != row["providerSource"]
            or sorted(c["features"]) != row["providerFeatures"]
        ):
            claimed_mismatch.append(row["name"])

    policy = json.loads(POLICY.read_bytes())
    lock_text = (COPY / "providers/rust/Cargo.lock").read_text()
    import tomllib
    lock = tomllib.loads(lock_text)
    lock_rows = {(row["name"], row["version"]): row for row in lock["package"]}
    checksum_rows = []
    checksum_fail = []
    for dep in policy["dependencies"]:
        key = (dep["name"], dep["version"])
        pinned = lock_rows.get(key, {})
        ok = pinned.get("checksum") == dep["checksum"] and pinned.get("source") == "registry+https://github.com/rust-lang/crates.io-index"
        checksum_rows.append({"name": dep["name"], "version": dep["version"], "ok": ok, "lockChecksum": pinned.get("checksum")})
        if not ok:
            checksum_fail.append(dep["name"])

    sha2 = lock_rows.get(("sha2-const-stable", "0.1.0"), {})
    identity_lock = {
        "present": ("sha2-const-stable", "0.1.0") in lock_rows,
        "checksum": sha2.get("checksum"),
        "source": sha2.get("source"),
        "expectedChecksum": "5f179d4e11094a893b82fff208f74d448a7512f99f5a0acbd5c679b705f83ed9",
    }
    identity_lock["checksumMatch"] = identity_lock["checksum"] == identity_lock["expectedChecksum"]

    env = cargo_env(REVIEW / "probes" / "provider-target")
    checker_cmd = [
        PYTHON, "-I", "-B", str(CHECKER),
        "--manifest", str(COPY / "providers/rust/Cargo.toml"),
        "--target", TARGET,
        "--cargo", CARGO,
        "--policy", str(POLICY),
    ]
    checker = subprocess.run(checker_cmd, env=env, capture_output=True, timeout=120)
    (results / "logs" / "dependency-check.stdout").write_bytes(checker.stdout)
    (results / "logs" / "dependency-check.stderr").write_bytes(checker.stderr)
    checker_json = None
    if checker.returncode == 0 and checker.stdout:
        checker_json = json.loads(checker.stdout)

    edges_cmd = [
        PYTHON, "-I", "-B", str(EDGES),
        "--repository", str(COPY),
        "--metadata", str(results / "logs" / "provider-metadata.stdout"),
        "--inventory", str(INV10),
        "--lane", "rust-provider",
    ]
    edges = subprocess.run(edges_cmd, capture_output=True, timeout=30)
    (results / "logs" / "package-edges.stdout").write_bytes(edges.stdout)
    (results / "logs" / "package-edges.stderr").write_bytes(edges.stderr)
    edges_json = None
    if edges.returncode == 0 and edges.stdout:
        edges_json = json.loads(edges.stdout)

    edges_host = subprocess.run(
        [
            PYTHON, "-I", "-B", str(EDGES),
            "--repository", str(COPY),
            "--metadata", str(results / "logs" / "provider-metadata.stdout"),
            "--inventory", str(INV10),
            "--lane", "host",
        ],
        capture_output=True, timeout=30,
    )
    (results / "logs" / "package-edges-host-lane.stdout").write_bytes(edges_host.stdout)
    (results / "logs" / "package-edges-host-lane.stderr").write_bytes(edges_host.stderr)

    edges_v9 = subprocess.run(
        [
            PYTHON, "-I", "-B", str(EDGES),
            "--repository", str(COPY),
            "--metadata", str(results / "logs" / "provider-metadata.stdout"),
            "--inventory", str(INV9),
            "--lane", "rust-provider",
        ],
        capture_output=True, timeout=30,
    )

    fixture_checker = json.loads((ARCH / "docs/implementation/m1/trials/pure-provider-isolation-02/dependency-check.stdout").read_bytes())
    fixture_edges = json.loads((ARCH / "docs/implementation/m1/trials/pure-provider-isolation-02/package-edges.stdout").read_bytes())

    comparable_checker = None
    if checker_json:
        comparable_checker = {
            k: checker_json[k]
            for k in ("dependencyCount", "features", "localSourceFilesVerified", "package", "passed", "productQualification", "target")
        }
        fixture_cmp = {k: fixture_checker[k] for k in comparable_checker}
        checker_matches_fixture_except_workspace = comparable_checker == fixture_cmp

    comparable_edges = None
    edges_matches_fixture = None
    if edges_json:
        skip = set()
        comparable_edges = {k: edges_json[k] for k in edges_json if k not in skip}
        edges_matches_fixture = comparable_edges == fixture_edges

    provider_packages = sorted(provider)
    out = {
        "providerPackageCount": len(provider),
        "providerPackages": provider_packages,
        "providerOnly": provider_only,
        "sharedCount": len(shared_names),
        "sharedNames": shared_names,
        "allSharedVersionsSourcesFeaturesEqualHost": not unequal,
        "unequalShared": unequal,
        "shared": shared_rows,
        "claimedSharedCount": claimed["sharedPackages"],
        "claimedAllEqual": claimed["allSharedVersionsSourcesFeaturesEqualHost"],
        "independentMatchesClaimedRows": not claimed_mismatch,
        "claimedRowMismatches": claimed_mismatch,
        "policyLockChecksumsOk": not checksum_fail,
        "policyLockChecksums": checksum_rows,
        "sha2ConstStable": identity_lock,
        "checker": {
            "command": checker_cmd,
            "exitCode": checker.returncode,
            "stdout": checker.stdout.decode(),
            "stderr": checker.stderr.decode(),
            "parsed": checker_json,
            "matchesFixtureExceptWorkspace": checker_json is not None and checker_matches_fixture_except_workspace,
        },
        "packageEdgesV10": {
            "command": edges_cmd,
            "exitCode": edges.returncode,
            "stdout": edges.stdout.decode(),
            "stderr": edges.stderr.decode(),
            "parsed": edges_json,
            "matchesFixture": edges_matches_fixture,
        },
        "packageEdgesHostLaneRefuses": {
            "exitCode": edges_host.returncode,
            "stderr": edges_host.stderr.decode(),
            "stdout": edges_host.stdout.decode(),
        },
        "packageEdgesV9": {
            "exitCode": edges_v9.returncode,
            "stdout": edges_v9.stdout.decode(),
            "stderr": edges_v9.stderr.decode(),
        },
        "workspaceRoot": provider_meta.get("workspace_root"),
        "workspaceMembers": provider_meta.get("workspace_members"),
        "hostWorkspaceRoot": host_meta.get("workspace_root"),
    }
    (results / "comparison.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "sharedCount": out["sharedCount"],
        "allEqual": out["allSharedVersionsSourcesFeaturesEqualHost"],
        "providerOnly": provider_only,
        "unequalShared": unequal,
        "claimedRowMismatches": claimed_mismatch,
        "policyLockChecksumsOk": out["policyLockChecksumsOk"],
        "sha2Ok": identity_lock["checksumMatch"],
        "checkerExit": checker.returncode,
        "checkerPassed": None if checker_json is None else checker_json.get("passed"),
        "checkerMatchesFixtureExceptWorkspace": out["checker"]["matchesFixtureExceptWorkspace"],
        "edgesV10Exit": edges.returncode,
        "edgesPassed": None if edges_json is None else edges_json.get("passed"),
        "edgesMatchesFixture": edges_matches_fixture,
        "hostLaneExit": edges_host.returncode,
        "hostLaneStderr": edges_host.stderr.decode(),
        "edgesV9Exit": edges_v9.returncode,
        "checkerStderr": checker.stderr.decode(),
        "edgesStderr": edges.stderr.decode(),
        "checkerStdout": checker.stdout.decode(),
        "edgesStdout": edges.stdout.decode(),
    }, indent=2))


if __name__ == "__main__":
    main()
