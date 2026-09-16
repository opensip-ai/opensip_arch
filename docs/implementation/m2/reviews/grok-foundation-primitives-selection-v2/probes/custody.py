"""Verify both subject manifests, copy frozen trees privately, record joins."""
from __future__ import annotations

import hashlib
import json
import shutil
import stat
import sys
from pathlib import Path

ARCH = Path("/Users/sb/code/opensip-ai/opensip_arch")
PRODUCT = Path("/Users/sb/code/opensip-ai/opensip")
REVIEW = Path("/tmp/opensip-implementation/m2-grok-foundation-v2-provider-workspace-v1-review/review")
INV10 = ARCH / "docs/implementation/m1/repository-file-inventory.v10.json"

A_SEL = "docs/implementation/m2/foundation-primitives-selection-v2-subject.json"
A_SHA = "b8328a23fbffb6c46f52af2f18595cc74f7b32dca76a30489adb4f871c37ac75"
A_FROZEN = Path("/tmp/opensip-implementation/m2-foundation-primitives-subject-02")
A_FMAN = ARCH / "docs/implementation/m2/trials/foundation-primitives-02/subject.json"
A_FSHA = "b76e18b97cdd86a646893e209f9b016c40d9e092fd44b80d7751dabbf776ed89"
A_ARCHIVE = ARCH / "docs/implementation/m2/trials/foundation-primitives-02/subject.tar.gz"
V1_PROD = ARCH / "docs/implementation/m2/foundation-primitives-selection-v1/product"
V2_PROD = ARCH / "docs/implementation/m2/foundation-primitives-selection-v2/product"
PRIOR_REVIEW = ARCH / "docs/implementation/m2/reviews/grok-foundation-primitives-selection-v1/review.json"

B_SEL = "docs/implementation/m1/rust-provider-workspace-selection-v1-subject.json"
B_SHA = "7621eedcee592785790ce46ff58c8c53e4d901cacbdbc74422844d115aff894e"
B_FROZEN = Path("/tmp/opensip-implementation/m1-rust-provider-workspace-subject-01")
B_FMAN = ARCH / "docs/implementation/m1/trials/rust-provider-workspace-01/subject.json"
B_FSHA = "94fa905cdafff165ee468cc8ae847d21f547f40fac142c4e0be0e68158677a49"
B_ARCHIVE = ARCH / "docs/implementation/m1/trials/rust-provider-workspace-01/subject.tar.gz"
PROBE_LOCK = "be35cf233ca1a09d5187d871936cff9554607040f5ce3e01e4ac4a0f012e5176"
PROBE_TOML = "cd818152d074c0f49405e6304dbab28a5ce9d3779c3e22b7bc26db50ab90fd67"


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def info(path: Path) -> dict:
    raw = path.read_bytes()
    return {
        "bytes": len(raw),
        "sha256": sha256_bytes(raw),
        "mode": stat.S_IMODE(path.stat().st_mode),
        "symlink": path.is_symlink(),
    }


def verify_manifest(manifest: Path, root: Path, expected_sha: str, expected_count: int) -> dict:
    raw = manifest.read_bytes()
    data = json.loads(raw)
    mismatches = []
    for row in data["files"]:
        path = root / row["path"]
        actual = info(path)
        if actual["bytes"] != row["bytes"] or actual["sha256"] != row["sha256"] or path.is_symlink():
            mismatches.append(row["path"])
    sha = sha256_bytes(raw)
    return {
        "path": str(manifest),
        "sha256": sha,
        "shaMatch": sha == expected_sha,
        "count": len(data["files"]),
        "countMatch": len(data["files"]) == expected_count,
        "membersMatch": not mismatches,
        "mismatches": mismatches,
    }


def candidates_minus_record(subject_path: Path, successor_path: Path, record_rel: str) -> dict:
    subject = json.loads(subject_path.read_bytes())
    successor = json.loads(successor_path.read_bytes())
    sub_paths = [r["path"] for r in subject["files"]]
    cand = successor["candidates"]
    minus = [p for p in sub_paths if p != record_rel]
    by = {r["path"]: r for r in cand}
    pin_mismatch = []
    for row in subject["files"]:
        if row["path"] == record_rel:
            continue
        c = by.get(row["path"])
        if c is None or c["bytes"] != row["bytes"] or c["sha256"] != row["sha256"]:
            pin_mismatch.append(row["path"])
    parents = []
    for parent in successor["parents"]:
        p = ARCH / parent["path"]
        actual = info(p)
        parents.append({
            **parent,
            "match": actual["sha256"] == parent["sha256"] and actual["bytes"] == parent["bytes"],
        })
    return {
        "candidatesEqualMinusRecord": [r["path"] for r in cand] == minus,
        "candidateCount": len(cand),
        "minusCount": len(minus),
        "pinMismatches": pin_mismatch,
        "passageOverrides": successor["passageOverrides"],
        "parents": parents,
        "parentsMatch": all(p["match"] for p in parents),
    }


def copy_tree(src: Path, dest: Path) -> None:
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(
        src,
        dest,
        ignore=shutil.ignore_patterns(".git", "target", "node_modules", "python-packages", "__pycache__", "dist"),
        symlinks=False,
    )


def main() -> None:
    if not sys.flags.isolated or sys.flags.optimize:
        raise SystemExit("isolated Python without optimization required")
    (REVIEW / "results").mkdir(parents=True, exist_ok=True)
    (REVIEW / "copy").mkdir(parents=True, exist_ok=True)
    inventory = json.loads(INV10.read_bytes())
    inv_files = {row["path"]: row for row in inventory["files"]}
    inv_packages = len(inventory["packages"])

    a_sel = verify_manifest(ARCH / A_SEL, ARCH, A_SHA, 29)
    a_frozen = verify_manifest(A_FMAN, A_FROZEN, A_FSHA, 208)
    a_joins = candidates_minus_record(
        ARCH / A_SEL,
        ARCH / "docs/implementation/m2/foundation-primitives-selection-v2/successor.json",
        "docs/implementation/m2/foundation-primitives-selection-v2/successor.json",
    )
    a_map = json.loads((ARCH / "docs/implementation/m2/foundation-primitives-selection-v2/materialization-map.json").read_bytes())
    a_map_rows = []
    for row in a_map["files"]:
        frozen = A_FROZEN / "product" / row["productPath"]
        cand = ARCH / row["candidatePath"]
        fi, ci = info(frozen), info(cand)
        a_map_rows.append({
            "productPath": row["productPath"],
            "inInventory10": row["productPath"] in inv_files,
            "frozenMatch": fi["sha256"] == row["sha256"] and fi["bytes"] == row["bytes"],
            "candidateMatch": ci["sha256"] == row["sha256"] and ci["bytes"] == row["bytes"],
        })
    owned = [
        "Cargo.lock",
        "crates/identity/src/canonical_tests.rs",
        "crates/identity/src/digests.rs",
        "crates/identity/src/lib.rs",
        "crates/platform/Cargo.toml",
        "crates/platform/src/filesystem.rs",
        "crates/platform/src/lib.rs",
    ]
    vs_v1 = []
    for rel in owned:
        v1 = info(V1_PROD / rel)
        v2 = info(V2_PROD / rel)
        vs_v1.append({"path": rel, "equalV1": v1["sha256"] == v2["sha256"], "v1": v1["sha256"], "v2": v2["sha256"]})
    v1_fs = (V1_PROD / "crates/platform/src/filesystem.rs").read_bytes()
    v2_fs = (V2_PROD / "crates/platform/src/filesystem.rs").read_bytes()
    marker = b"#[cfg(test)]"
    v1_prod = v1_fs.split(marker, 1)[0]
    v2_prod = v2_fs.split(marker, 1)[0]
    v2_tests = v2_fs.split(marker, 1)[1]
    prior = info(PRIOR_REVIEW)
    pin = json.loads((ARCH / "docs/implementation/m2/foundation-primitives-selection-v2/evidence/prior-review-pin.json").read_bytes())
    a_archive = info(A_ARCHIVE)
    a_archive_pin = json.loads((ARCH / "docs/implementation/m2/foundation-primitives-selection-v2/evidence/archive-pin.json").read_bytes())

    a_copy = REVIEW / "copy" / "foundation-v2"
    copy_tree(A_FROZEN, a_copy)

    b_sel = verify_manifest(ARCH / B_SEL, ARCH, B_SHA, 31)
    b_frozen = verify_manifest(B_FMAN, B_FROZEN, B_FSHA, 206)
    b_joins = candidates_minus_record(
        ARCH / B_SEL,
        ARCH / "docs/implementation/m1/rust-provider-workspace-selection-v1/successor.json",
        "docs/implementation/m1/rust-provider-workspace-selection-v1/successor.json",
    )
    b_map = json.loads((ARCH / "docs/implementation/m1/rust-provider-workspace-selection-v1/materialization-map.json").read_bytes())
    b_map_rows = []
    for row in b_map["files"]:
        frozen = B_FROZEN / "product" / row["productPath"]
        cand = ARCH / row["candidatePath"]
        fi, ci = info(frozen), info(cand)
        b_map_rows.append({
            "productPath": row["productPath"],
            "inInventory10": row["productPath"] in inv_files,
            "frozenMatch": fi["sha256"] == row["sha256"] and fi["bytes"] == row["bytes"],
            "candidateMatch": ci["sha256"] == row["sha256"] and ci["bytes"] == row["bytes"],
        })
    b_archive = info(B_ARCHIVE)
    b_archive_pin = json.loads((ARCH / "docs/implementation/m1/rust-provider-workspace-selection-v1/evidence/archive-pin.json").read_bytes())
    root_toml = (B_FROZEN / "product" / "Cargo.toml").read_text()
    live_toml = (PRODUCT / "Cargo.toml").read_text()
    b_copy = REVIEW / "copy" / "provider-v1"
    copy_tree(B_FROZEN, b_copy)

    identity_live = info(PRODUCT / "crates/identity/src/digests.rs")
    identity_export = info(B_FROZEN / "product" / "crates/identity/src/digests.rs")
    identity_foundation = info(V2_PROD / "crates/identity/src/digests.rs")

    out = {
        "inventoryPackageCount": inv_packages,
        "foundation": {
            **{k: a_sel[k] for k in ("shaMatch", "count", "countMatch", "membersMatch", "mismatches")},
            "frozen": {k: a_frozen[k] for k in ("shaMatch", "count", "countMatch", "membersMatch", "mismatches")},
            "joins": a_joins,
            "mapRows": a_map_rows,
            "mapAllMatch": all(r["frozenMatch"] and r["candidateMatch"] and r["inInventory10"] for r in a_map_rows),
            "vsV1": vs_v1,
            "fiveOfSevenEqualV1": sum(1 for r in vs_v1 if r["equalV1"]) == 5,
            "changedVsV1": [r["path"] for r in vs_v1 if not r["equalV1"]],
            "productionAdapterEqualV1": sha256_bytes(v1_prod) == sha256_bytes(v2_prod),
            "productionAdapterBytes": len(v2_prod),
            "socketUsesShortTmpOnly": b'Tree::new_in(Path::new("/tmp"))' in v2_tests,
            "otherTestsUseAmbientTempDir": b"Self::new_in(&std::env::temp_dir())" in v2_tests,
            "noSkipAttribute": b"#[ignore" not in v2_fs and b"skip(" not in v2_tests,
            "noCwdMutation": b"set_current_dir" not in v2_fs and b"current_dir" not in v2_fs,
            "priorReviewPinMatch": prior["sha256"] == pin["sha256"] and prior["bytes"] == pin["bytes"],
            "priorReviewSha256": prior["sha256"],
            "archiveMatchesPin": a_archive["sha256"] == a_archive_pin["sha256"],
            "privateCopy": str(a_copy),
        },
        "provider": {
            **{k: b_sel[k] for k in ("shaMatch", "count", "countMatch", "membersMatch", "mismatches")},
            "frozen": {k: b_frozen[k] for k in ("shaMatch", "count", "countMatch", "membersMatch", "mismatches")},
            "joins": b_joins,
            "mapRows": b_map_rows,
            "mapAllMatch": all(r["frozenMatch"] and r["candidateMatch"] and r["inInventory10"] for r in b_map_rows),
            "lockEqualsIsolation02Probe": info(B_FROZEN / "product/providers/rust/Cargo.lock")["sha256"] == PROBE_LOCK,
            "tomlEqualsIsolation02Probe": info(B_FROZEN / "product/providers/rust/Cargo.toml")["sha256"] == PROBE_TOML,
            "rootExcludeHasProvidersRust": 'exclude = ["providers/rust"' in root_toml and 'exclude = ["providers/rust"' in live_toml,
            "rootMembersOmitProvider": "providers/rust" not in root_toml.split("members", 1)[1].split("exclude", 1)[0],
            "identityExportEqualsLive": identity_export["sha256"] == identity_live["sha256"],
            "identityExportIsPriorToFoundationV2": identity_export["sha256"] != identity_foundation["sha256"],
            "archiveMatchesPin": b_archive["sha256"] == b_archive_pin["sha256"],
            "privateCopy": str(b_copy),
        },
        "executedAgainstFrozenTmp": False,
    }
    (REVIEW / "results" / "custody-before.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "aSel": {k: a_sel[k] for k in ("shaMatch", "countMatch", "membersMatch", "count", "mismatches")},
        "aFrozen": {k: a_frozen[k] for k in ("shaMatch", "countMatch", "membersMatch", "count", "mismatches")},
        "aJoins": {k: a_joins[k] for k in ("candidatesEqualMinusRecord", "candidateCount", "parentsMatch", "pinMismatches")},
        "aMap": out["foundation"]["mapAllMatch"],
        "fiveOfSeven": out["foundation"]["fiveOfSevenEqualV1"],
        "changed": out["foundation"]["changedVsV1"],
        "prodEqual": out["foundation"]["productionAdapterEqualV1"],
        "socket": out["foundation"]["socketUsesShortTmpOnly"],
        "ambient": out["foundation"]["otherTestsUseAmbientTempDir"],
        "priorPin": out["foundation"]["priorReviewPinMatch"],
        "bSel": {k: b_sel[k] for k in ("shaMatch", "countMatch", "membersMatch", "count", "mismatches")},
        "bFrozen": {k: b_frozen[k] for k in ("shaMatch", "countMatch", "membersMatch", "count", "mismatches")},
        "bJoins": {k: b_joins[k] for k in ("candidatesEqualMinusRecord", "candidateCount", "parentsMatch", "pinMismatches")},
        "bMap": out["provider"]["mapAllMatch"],
        "lockProbe": out["provider"]["lockEqualsIsolation02Probe"],
        "tomlProbe": out["provider"]["tomlEqualsIsolation02Probe"],
        "exclude": out["provider"]["rootExcludeHasProvidersRust"],
        "identityPrior": out["provider"]["identityExportIsPriorToFoundationV2"],
        "identityLive": out["provider"]["identityExportEqualsLive"],
        "invPackages": inv_packages,
    }, indent=2))


if __name__ == "__main__":
    main()
