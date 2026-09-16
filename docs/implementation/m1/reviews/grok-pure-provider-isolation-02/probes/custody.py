"""Verify 36-member subject pins, copy export privately, compare live shared sources."""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import stat
import sys
from pathlib import Path

ARCH = Path("/Users/sb/code/opensip-ai/opensip_arch")
PRODUCT = Path("/Users/sb/code/opensip-ai/opensip")
REVIEW = Path("/tmp/opensip-implementation/m1-grok-pure-provider-isolation-02-review/review")
SUBJECT_REL = "docs/implementation/m1/trials/pure-provider-isolation-02/subject.json"
EXPECTED_SUBJECT_SHA = "3147a63a43825c4c9b1236d72f6b0afa36b507e3b518c13db4147f58c3479280"
EXPECTED_FILES = 36
SHARED_PREFIX = "docs/implementation/m1/trials/pure-provider-isolation-02/export/"
PYTHON = "/tmp/opensip-implementation/metadata-reference-env/bin/python"


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def file_row(path: Path) -> dict:
    raw = path.read_bytes()
    mode = path.stat().st_mode
    return {
        "bytes": len(raw),
        "sha256": sha256_bytes(raw),
        "mode": stat.S_IMODE(mode),
        "is_symlink": path.is_symlink(),
        "is_file": path.is_file(),
    }


def main() -> None:
    if not sys.flags.isolated or sys.flags.optimize:
        raise SystemExit("isolated Python without optimization required")
    (REVIEW / "results").mkdir(parents=True, exist_ok=True)
    (REVIEW / "copy").mkdir(parents=True, exist_ok=True)

    subject_path = ARCH / SUBJECT_REL
    subject_raw = subject_path.read_bytes()
    subject_sha = sha256_bytes(subject_raw)
    subject = json.loads(subject_raw)
    rows = subject["files"]
    members = []
    mismatches = []
    for row in rows:
        path = ARCH / row["path"]
        actual = file_row(path)
        ok = (
            actual["bytes"] == row["bytes"]
            and actual["sha256"] == row["sha256"]
            and actual["is_file"]
            and not actual["is_symlink"]
        )
        members.append({
            "path": row["path"],
            "expectedBytes": row["bytes"],
            "expectedSha256": row["sha256"],
            **actual,
            "match": ok,
        })
        if not ok:
            mismatches.append(row["path"])

    pins = json.loads((ARCH / "docs/implementation/m1/trials/pure-provider-isolation-02/source-pins.json").read_bytes())
    shared_live = []
    shared_mismatches = []
    for pin in pins["files"]:
        export_path = ARCH / SHARED_PREFIX / pin["path"] if False else ARCH / f"docs/implementation/m1/trials/pure-provider-isolation-02/export/{pin['path']}"
        live_path = PRODUCT / pin["path"]
        export = file_row(export_path)
        live = file_row(live_path)
        equal_live = export["sha256"] == live["sha256"] and export["bytes"] == live["bytes"]
        equal_pin = (
            export["sha256"] == pin["sha256"]
            and export["bytes"] == pin["bytes"]
            and export["mode"] == pin["mode"]
        )
        shared_live.append({
            "path": pin["path"],
            "pin": pin,
            "export": export,
            "live": live,
            "exportEqualsPin": equal_pin,
            "exportEqualsLive": equal_live,
            "exportReadOnly": export["mode"] == 0o444,
        })
        if not (equal_pin and equal_live and export["mode"] == 0o444):
            shared_mismatches.append(pin["path"])

    export_root = ARCH / "docs/implementation/m1/trials/pure-provider-isolation-02/export"
    export_files = sorted(
        p.relative_to(export_root).as_posix()
        for p in export_root.rglob("*")
        if p.is_file()
    )
    forbidden = {
        "rootCargoToml": (export_root / "Cargo.toml").exists(),
        "apps": (export_root / "apps").exists(),
        "tools": (export_root / "tools").exists(),
        "packageJson": (export_root / "package.json").exists(),
        "nodeModules": any(p.name == "node_modules" for p in export_root.rglob("*")),
        "rustToolchain": (export_root / "providers/rust/rust-toolchain.toml").exists(),
        "platform": (export_root / "crates/platform").exists(),
        "host": (export_root / "crates/host").exists(),
        "rootNode": any(p.suffix in {".js", ".mjs", ".cjs", ".ts"} for p in export_root.rglob("*") if p.is_file()),
    }

    dest = REVIEW / "copy" / "export"
    if dest.exists():
        def _onerror(func, path, _exc):
            os.chmod(path, 0o700)
            func(path)
        shutil.rmtree(dest, onerror=_onerror)
    shutil.copytree(export_root, dest, symlinks=False, copy_function=shutil.copy2)

    copy_files = []
    for p in sorted(dest.rglob("*")):
        if p.is_file():
            rel = p.relative_to(dest).as_posix()
            copy_files.append({"path": rel, **file_row(p)})

    provider_lock_selected = file_row(ARCH / "docs/implementation/m1/trials/pure-provider-isolation-02/provider-lock.selected")
    export_lock = file_row(export_root / "providers/rust/Cargo.lock")
    copy_lock = file_row(dest / "providers/rust/Cargo.lock")

    checker = ARCH / "docs/implementation/m1/contracts-dependency-selection-v1/product/tools/check_dependencies.py"
    policy = ARCH / "docs/implementation/m1/contracts-dependency-selection-v1/product/tools/contracts/dependency-policy.json"
    live_checker = PRODUCT / "tools/check_dependencies.py"
    live_policy = PRODUCT / "tools/contracts/dependency-policy.json"
    edges = PRODUCT / "tools/check_package_edges.py"
    inv10 = ARCH / "docs/implementation/m1/repository-file-inventory.v10.json"
    inv9 = ARCH / "docs/implementation/m1/repository-file-inventory.v9.json"

    tools = {
        "proposedChecker": {"path": str(checker), **file_row(checker)},
        "proposedPolicy": {"path": str(policy), **file_row(policy)},
        "liveChecker": {"path": str(live_checker), **file_row(live_checker)},
        "livePolicy": {"path": str(live_policy), **file_row(live_policy)},
        "installedPackageEdges": {"path": str(edges), **file_row(edges)},
        "inventory10": {"path": str(inv10), **file_row(inv10)},
        "inventory9": {"path": str(inv9), **file_row(inv9)},
    }
    tools["checkerMatchesReviewedPin"] = (
        tools["proposedChecker"]["sha256"] == "d00f6d6f867b0db2d97b4acfcb628e26f890d9c3948d6402da960d37cf041b34"
        and tools["proposedChecker"]["bytes"] == 6684
    )
    tools["policyMatchesReviewedPin"] = (
        tools["proposedPolicy"]["sha256"] == "7e34a6a0fd92e3a42e92ee3ca2d0d32fdf2eac0cc8d27c4e4d8ca5c11f0dd6df"
        and tools["proposedPolicy"]["bytes"] == 3771
    )
    tools["proposedCheckerEqualsLive"] = tools["proposedChecker"]["sha256"] == tools["liveChecker"]["sha256"]
    tools["proposedPolicyEqualsLive"] = tools["proposedPolicy"]["sha256"] == tools["livePolicy"]["sha256"]
    tools["inventory10MatchesAccepted"] = (
        tools["inventory10"]["sha256"] == "6608fabd31f1fb89feb565ad5b930c4be49f096a30dd92ecdc21466251fd8bc9"
        and tools["inventory10"]["bytes"] == 121810
    )

    live_provider = PRODUCT / "providers/rust"
    result = {
        "python": PYTHON,
        "sysVersion": sys.version,
        "isolated": bool(sys.flags.isolated),
        "subjectPath": str(subject_path),
        "subjectSha256": subject_sha,
        "subjectShaExpected": EXPECTED_SUBJECT_SHA,
        "subjectShaMatch": subject_sha == EXPECTED_SUBJECT_SHA,
        "expectedFiles": EXPECTED_FILES,
        "actualFiles": len(rows),
        "memberCountMatch": len(rows) == EXPECTED_FILES,
        "membersMatch": not mismatches,
        "mismatches": mismatches,
        "members": members,
        "sharedSourceCount": len(pins["files"]),
        "sharedAllEqualLiveAndPins": not shared_mismatches,
        "sharedMismatches": shared_mismatches,
        "shared": shared_live,
        "exportFileCount": len(export_files),
        "exportFiles": export_files,
        "exportForbiddenPresent": forbidden,
        "exportIsolated": not any(forbidden.values()),
        "providerLockEqualsExportLock": provider_lock_selected["sha256"] == export_lock["sha256"],
        "copyLockEqualsExportLock": copy_lock["sha256"] == export_lock["sha256"],
        "copyRoot": str(dest),
        "copyFileCount": len(copy_files),
        "copyFiles": copy_files,
        "liveProvidersRustExists": live_provider.exists(),
        "tools": tools,
        "frozenOriginalExportNotUsed": True,
    }
    out = REVIEW / "results" / "custody-before.json"
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "subjectShaMatch": result["subjectShaMatch"],
        "membersMatch": result["membersMatch"],
        "sharedAllEqualLiveAndPins": result["sharedAllEqualLiveAndPins"],
        "exportIsolated": result["exportIsolated"],
        "exportFileCount": result["exportFileCount"],
        "copyFileCount": result["copyFileCount"],
        "checkerMatchesReviewedPin": tools["checkerMatchesReviewedPin"],
        "policyMatchesReviewedPin": tools["policyMatchesReviewedPin"],
        "proposedCheckerEqualsLive": tools["proposedCheckerEqualsLive"],
        "inventory10MatchesAccepted": tools["inventory10MatchesAccepted"],
        "liveProvidersRustExists": result["liveProvidersRustExists"],
        "mismatches": mismatches,
        "sharedMismatches": shared_mismatches,
        "forbidden": forbidden,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
