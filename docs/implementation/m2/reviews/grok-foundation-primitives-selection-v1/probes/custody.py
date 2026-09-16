"""Verify selection + frozen subject pins, copy privately, record joins."""
from __future__ import annotations

import hashlib
import json
import shutil
import stat
import sys
from pathlib import Path

ARCH = Path("/Users/sb/code/opensip-ai/opensip_arch")
PRODUCT = Path("/Users/sb/code/opensip-ai/opensip")
REVIEW = Path("/tmp/opensip-implementation/m2-grok-foundation-primitives-selection-v1-review/review")
SEL_REL = "docs/implementation/m2/foundation-primitives-selection-v1-subject.json"
SEL_SHA = "87ec90665949e7a9dfe604f1bb3148039c1113d9a61c07bf0500b70b57f3162b"
FROZEN_MANIFEST = ARCH / "docs/implementation/m2/trials/foundation-primitives-01/subject.json"
FROZEN_SHA = "511eff69af377af48be171b0687823d21f97bbebfa9cb937e5fa13cf4bcba3d0"
FROZEN_TREE = Path("/tmp/opensip-implementation/m2-foundation-primitives-subject-01")
ARCHIVE = ARCH / "docs/implementation/m2/trials/foundation-primitives-01/subject.tar.gz"
OWNED = [
    "Cargo.lock",
    "crates/identity/src/canonical_tests.rs",
    "crates/identity/src/digests.rs",
    "crates/identity/src/lib.rs",
    "crates/platform/Cargo.toml",
    "crates/platform/src/filesystem.rs",
    "crates/platform/src/lib.rs",
]
ASSETS02 = ARCH / "docs/implementation/m1/trials/report-assets-02/subject/platform/src/lib.rs"
ASSETS02_SHA = "54bb15d968c9034a52a7fb5ae552d168995b3e49ed58e712cc012c5927f5cadf"


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def file_info(path: Path) -> dict:
    raw = path.read_bytes()
    return {
        "bytes": len(raw),
        "sha256": sha256_bytes(raw),
        "mode": stat.S_IMODE(path.stat().st_mode),
        "symlink": path.is_symlink(),
    }


def verify_manifest(manifest_path: Path, root: Path) -> dict:
    raw = manifest_path.read_bytes()
    data = json.loads(raw)
    mismatches = []
    members = []
    for row in data["files"]:
        path = root / row["path"]
        actual = file_info(path)
        ok = (
            actual["bytes"] == row["bytes"]
            and actual["sha256"] == row["sha256"]
            and path.is_file()
            and not path.is_symlink()
        )
        members.append({"path": row["path"], "match": ok, **actual})
        if not ok:
            mismatches.append(row["path"])
    return {
        "path": str(manifest_path),
        "sha256": sha256_bytes(raw),
        "bytes": len(raw),
        "count": len(data["files"]),
        "mismatches": mismatches,
        "membersMatch": not mismatches,
        "members": members,
    }


def main() -> None:
    if not sys.flags.isolated or sys.flags.optimize:
        raise SystemExit("isolated Python without optimization required")
    (REVIEW / "results").mkdir(parents=True, exist_ok=True)
    (REVIEW / "copy").mkdir(parents=True, exist_ok=True)

    selection = verify_manifest(ARCH / SEL_REL, ARCH)
    selection["shaExpected"] = SEL_SHA
    selection["shaMatch"] = selection["sha256"] == SEL_SHA
    selection["countExpected"] = 25
    selection["countMatch"] = selection["count"] == 25

    frozen_manifest_info = verify_manifest(FROZEN_MANIFEST, FROZEN_TREE)
    frozen_manifest_info["shaExpected"] = FROZEN_SHA
    frozen_manifest_info["shaMatch"] = frozen_manifest_info["sha256"] == FROZEN_SHA
    frozen_manifest_info["countExpected"] = 196
    frozen_manifest_info["countMatch"] = frozen_manifest_info["count"] == 196

    evidence_impl = ARCH / "docs/implementation/m2/foundation-primitives-selection-v1/evidence/implementation-subject.json"
    evidence_impl_info = file_info(evidence_impl)

    archive = file_info(ARCHIVE)
    pin = json.loads((ARCH / "docs/implementation/m2/foundation-primitives-selection-v1/evidence/archive-pin.json").read_bytes())

    successor = json.loads((ARCH / "docs/implementation/m2/foundation-primitives-selection-v1/successor.json").read_bytes())
    subject = json.loads((ARCH / SEL_REL).read_bytes())
    subject_paths = [row["path"] for row in subject["files"]]
    candidate_paths = [row["path"] for row in successor["candidates"]]
    record_path = "docs/implementation/m2/foundation-primitives-selection-v1/successor.json"
    minus_record = [p for p in subject_paths if p != record_path]
    candidates_equal = candidate_paths == minus_record
    candidate_pin_mismatch = []
    by_cand = {row["path"]: row for row in successor["candidates"]}
    for row in subject["files"]:
        if row["path"] == record_path:
            continue
        c = by_cand.get(row["path"])
        if c is None or c["bytes"] != row["bytes"] or c["sha256"] != row["sha256"]:
            candidate_pin_mismatch.append(row["path"])

    mmap = json.loads((ARCH / "docs/implementation/m2/foundation-primitives-selection-v1/materialization-map.json").read_bytes())
    inventory = json.loads((ARCH / "docs/implementation/m1/repository-file-inventory.v10.json").read_bytes())
    inv_files = {row["path"]: row for row in inventory["files"]}
    map_rows = []
    for row in mmap["files"]:
        product = FROZEN_TREE / "product" / row["productPath"]
        candidate = ARCH / row["candidatePath"]
        pinfo = file_info(product)
        cinfo = file_info(candidate)
        inv = inv_files.get(row["productPath"])
        map_rows.append({
            "productPath": row["productPath"],
            "inInventory10": inv is not None,
            "inventoryPackage": None if inv is None else inv["package"],
            "inventoryRole": None if inv is None else inv["role"],
            "pinBytes": row["bytes"],
            "pinSha256": row["sha256"],
            "frozenMatch": pinfo["sha256"] == row["sha256"] and pinfo["bytes"] == row["bytes"],
            "candidateMatch": cinfo["sha256"] == row["sha256"] and cinfo["bytes"] == row["bytes"],
            "frozenEqualsCandidate": pinfo["sha256"] == cinfo["sha256"],
        })

    live_owned = []
    for rel in OWNED:
        live = PRODUCT / rel
        cand = ARCH / "docs/implementation/m2/foundation-primitives-selection-v1/product" / rel
        if live.exists():
            linfo = file_info(live)
            cinfo = file_info(cand)
            live_owned.append({
                "path": rel,
                "liveExists": True,
                "liveEqualsCandidate": linfo["sha256"] == cinfo["sha256"],
                "liveSha256": linfo["sha256"],
                "candidateSha256": cinfo["sha256"],
            })
        else:
            live_owned.append({"path": rel, "liveExists": False, "liveEqualsCandidate": False})

    assets02 = file_info(ASSETS02)
    dest = REVIEW / "copy" / "frozen-subject"
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(
        FROZEN_TREE,
        dest,
        ignore=shutil.ignore_patterns(".git", "target", "node_modules", "python-packages", "__pycache__", "dist"),
        symlinks=False,
    )

    parents = []
    for parent in successor["parents"]:
        path = ARCH / parent["path"]
        info = file_info(path)
        parents.append({
            **parent,
            "actualSha256": info["sha256"],
            "actualBytes": info["bytes"],
            "match": info["sha256"] == parent["sha256"] and info["bytes"] == parent["bytes"],
        })

    unchanged_identity_canonical = {
        "live": file_info(PRODUCT / "crates/identity/src/canonical.rs"),
        "frozen": file_info(dest / "product" / "crates/identity/src/canonical.rs"),
    }
    unchanged_identity_canonical["equal"] = (
        unchanged_identity_canonical["live"]["sha256"] == unchanged_identity_canonical["frozen"]["sha256"]
    )
    unchanged_build_rs = {
        "live": file_info(PRODUCT / "crates/platform/build.rs"),
        "frozen": file_info(dest / "product" / "crates/platform/build.rs"),
    }
    unchanged_build_rs["equal"] = unchanged_build_rs["live"]["sha256"] == unchanged_build_rs["frozen"]["sha256"]

    out = {
        "selection": {k: v for k, v in selection.items() if k != "members"},
        "selectionMismatches": selection["mismatches"],
        "frozenManifest": {k: v for k, v in frozen_manifest_info.items() if k != "members"},
        "frozenMismatches": frozen_manifest_info["mismatches"],
        "evidenceImplementationSubject": evidence_impl_info,
        "evidenceImplementationEqualsFrozenManifest": evidence_impl_info["sha256"] == FROZEN_SHA,
        "archive": archive,
        "archivePin": pin,
        "archiveMatchesPin": archive["sha256"] == pin["sha256"] and archive["bytes"] == pin["bytes"],
        "candidatesEqualManifestMinusRecord": candidates_equal,
        "candidateCount": len(candidate_paths),
        "subjectMinusRecordCount": len(minus_record),
        "candidatePinMismatches": candidate_pin_mismatch,
        "passageOverrides": successor["passageOverrides"],
        "parents": parents,
        "mapRows": map_rows,
        "mapAllMatchFrozenAndInventory": all(
            row["frozenMatch"] and row["candidateMatch"] and row["inInventory10"] for row in map_rows
        ),
        "liveOwnedVsCandidate": live_owned,
        "assets02": {"path": str(ASSETS02), **assets02, "shaMatch": assets02["sha256"] == ASSETS02_SHA, "bytesExpected": 2952},
        "privateCopy": str(dest),
        "executedAgainstFrozenTmp": False,
        "unchangedCanonicalRs": unchanged_identity_canonical,
        "unchangedBuildRs": unchanged_build_rs,
        "filesystemWasPlannedInInventory10": "crates/platform/src/filesystem.rs" in inv_files,
    }
    (REVIEW / "results" / "custody-before.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "selectionShaMatch": selection["shaMatch"],
        "selectionMembers": selection["membersMatch"],
        "selectionCount": selection["count"],
        "frozenShaMatch": frozen_manifest_info["shaMatch"],
        "frozenMembers": frozen_manifest_info["membersMatch"],
        "frozenCount": frozen_manifest_info["count"],
        "archiveMatchesPin": out["archiveMatchesPin"],
        "candidatesEqualManifestMinusRecord": candidates_equal,
        "candidatePinMismatches": candidate_pin_mismatch,
        "mapAllMatchFrozenAndInventory": out["mapAllMatchFrozenAndInventory"],
        "parentsMatch": all(p["match"] for p in parents),
        "assets02ShaMatch": out["assets02"]["shaMatch"],
        "canonicalUnchanged": unchanged_identity_canonical["equal"],
        "buildRsUnchanged": unchanged_build_rs["equal"],
        "liveEquals": {row["path"]: row.get("liveEqualsCandidate") for row in live_owned},
        "selectionMismatches": selection["mismatches"][:10],
        "frozenMismatches": frozen_manifest_info["mismatches"][:10],
    }, indent=2))


if __name__ == "__main__":
    main()
