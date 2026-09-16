"""Verify array-order-selection v1 pins, map, parent LogicalPath, copy privately."""
from __future__ import annotations

import hashlib
import json
import shutil
import stat
import sys
from pathlib import Path

ARCH = Path("/Users/sb/code/opensip-ai/opensip_arch")
PRODUCT = Path("/Users/sb/code/opensip-ai/opensip")
REVIEW = Path("/tmp/opensip-implementation/m2-grok-array-order-selection-v1-review/review")
SEL = "docs/implementation/m2/array-order-selection-v1-subject.json"
SEL_SHA = "db9194adb6cac4b755545c197916e22b921ba0e056d4fab1ae6eb48964c6500f"
FROZEN = Path("/tmp/opensip-implementation/m2-array-order-subject-01")
FMAN = ARCH / "docs/implementation/m2/trials/array-order-01/subject.json"
FSHA = "3fd8620abb1d45bb3ead8746f95484e8e945f104e9f77faa1628124e04eaba10"
ARCHIVE = ARCH / "docs/implementation/m2/trials/array-order-01/subject.tar.gz"
PARENT_DESC = ARCH / "docs/implementation/m2/logical-path-selection-v1/product/crates/identity/src/descriptors.rs"
PARENT_LIB = ARCH / "docs/implementation/m2/logical-path-selection-v1/product/crates/identity/src/lib.rs"
CANON = ARCH / "docs/coop/design-corrections/foundation/canonical.py"
CANON_SHA = "d47f25db0fb09ceb84282a89fdf74055cb81ccb9de26f85a5a70b032b9a6b442"


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
        "sha256": sha,
        "shaMatch": sha == expected_sha,
        "count": len(data["files"]),
        "countMatch": len(data["files"]) == expected_count,
        "membersMatch": not mismatches,
        "mismatches": mismatches,
    }


def logical_path_body(text: str) -> str:
    """Strip the two-line module doc so remaining LogicalPath source can be compared."""
    lines = text.splitlines(True)
    # Keep from `use alloc` through the LogicalPath tests module, before ArrayOrder docs.
    start = None
    end = None
    for i, line in enumerate(lines):
        if start is None and line.startswith("use alloc::string::String"):
            start = i
        if line.startswith("/// A selected `x-opensip-order`"):
            end = i
            break
    if start is None:
        raise SystemExit("LogicalPath body start not found")
    if end is None:
        return "".join(lines[start:])
    return "".join(lines[start:end])


def main() -> None:
    if not sys.flags.isolated or sys.flags.optimize:
        raise SystemExit("isolated Python without optimization required")
    (REVIEW / "results").mkdir(parents=True, exist_ok=True)
    sel = verify_manifest(ARCH / SEL, ARCH, SEL_SHA, 26)
    frozen = verify_manifest(FMAN, FROZEN, FSHA, 205)
    successor = json.loads((ARCH / "docs/implementation/m2/array-order-selection-v1/successor.json").read_bytes())
    subject = json.loads((ARCH / SEL).read_bytes())
    record = "docs/implementation/m2/array-order-selection-v1/successor.json"
    minus = [r["path"] for r in subject["files"] if r["path"] != record]
    cand_paths = [r["path"] for r in successor["candidates"]]
    by = {r["path"]: r for r in successor["candidates"]}
    pin_mismatch = []
    for row in subject["files"]:
        if row["path"] == record:
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
    inventory = json.loads((ARCH / "docs/implementation/m1/repository-file-inventory.v10.json").read_bytes())
    inv_files = {row["path"]: row for row in inventory["files"]}
    mmap = json.loads((ARCH / "docs/implementation/m2/array-order-selection-v1/materialization-map.json").read_bytes())
    map_rows = []
    for row in mmap["files"]:
        frozen_p = FROZEN / "product" / row["productPath"]
        cand = ARCH / row["candidatePath"]
        fi, ci = info(frozen_p), info(cand)
        map_rows.append({
            "productPath": row["productPath"],
            "inInventory10": row["productPath"] in inv_files,
            "frozenMatch": fi["sha256"] == row["sha256"] and fi["bytes"] == row["bytes"],
            "candidateMatch": ci["sha256"] == row["sha256"] and ci["bytes"] == row["bytes"],
        })
    archive = info(ARCHIVE)
    pin = json.loads((ARCH / "docs/implementation/m2/array-order-selection-v1/evidence/archive-pin.json").read_bytes())
    canon = info(CANON)
    lock = json.loads((PRODUCT / "design-lock.json").read_bytes())
    src_manifest = json.loads((ARCH / lock["approvals"]["sourceManifest"]["path"]).read_bytes())
    rows = src_manifest.get("files", src_manifest.get("entries", []))
    canon_rows = [r for r in rows if r.get("path") == "docs/coop/design-corrections/foundation/canonical.py"]
    parent_desc = PARENT_DESC.read_text()
    new_desc = (ARCH / "docs/implementation/m2/array-order-selection-v1/product/crates/identity/src/descriptors.rs").read_text()
    parent_body = logical_path_body(parent_desc)
    new_body = logical_path_body(new_desc)
    parent_lib = PARENT_LIB.read_text()
    new_lib = (ARCH / "docs/implementation/m2/array-order-selection-v1/product/crates/identity/src/lib.rs").read_text()
    census = json.loads((ARCH / "docs/implementation/m2/array-order-selection-v1/evidence/selected-order-census.json").read_bytes())
    forms = []
    for row in census:
        forms.append(json.dumps(row["order"], sort_keys=True))
    dest = REVIEW / "copy" / "frozen-subject"
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(
        FROZEN,
        dest,
        ignore=shutil.ignore_patterns(".git", "target", "node_modules", "python-packages", "__pycache__", "dist"),
        symlinks=False,
    )
    inherited = []
    for rel in [
        "crates/identity/Cargo.toml",
        "crates/identity/src/canonical.rs",
        "crates/identity/src/canonical_tests.rs",
        "crates/identity/src/digests.rs",
    ]:
        live = info(PRODUCT / rel)
        fr = info(dest / "product" / rel)
        inherited.append({"path": rel, "liveEqualsFrozen": live["sha256"] == fr["sha256"]})
    out = {
        "selection": sel,
        "frozen": frozen,
        "candidatesEqualMinusRecord": cand_paths == minus,
        "candidateCount": len(cand_paths),
        "pinMismatches": pin_mismatch,
        "passageOverrides": successor["passageOverrides"],
        "parents": parents,
        "parentsMatch": all(p["match"] for p in parents),
        "mapRows": map_rows,
        "mapAllMatch": all(r["frozenMatch"] and r["candidateMatch"] and r["inInventory10"] for r in map_rows),
        "inventoryPackageCount": len(inventory["packages"]),
        "archiveMatchesPin": archive["sha256"] == pin["sha256"] and archive["bytes"] == pin["bytes"],
        "canonicalPy": canon,
        "canonicalPyMatchesOraclePin": canon["sha256"] == CANON_SHA and canon["bytes"] == 6465,
        "canonicalPyInSelectedBaseline": len(canon_rows) == 1 and canon_rows[0]["sha256"] == CANON_SHA,
        "logicalPathBodyEqualParent": parent_body == new_body,
        "moduleDocChanged": parent_desc.splitlines()[:3] != new_desc.splitlines()[:3],
        "libAddsArrayOrderOnly": (
            "ArrayOrder" in new_lib and "LogicalPath" in new_lib and parent_lib.count("pub use descriptors") == 1
        ),
        "censusForms": len(forms),
        "censusUniqueForms": len(set(forms)),
        "censusOccurrences": sum(len(row["occurrences"]) for row in census),
        "inherited": inherited,
        "liveHasDescriptors": (PRODUCT / "crates/identity/src/descriptors.rs").exists(),
        "privateCopy": str(dest),
        "executedAgainstFrozenTmp": False,
        "noDefaultOnArrayOrder": "Default" not in new_desc.split("pub struct ArrayOrder")[1][:200],
        "orderKindPrivate": "enum OrderKind" in new_desc and "pub enum OrderKind" not in new_desc,
    }
    (REVIEW / "results" / "custody-before.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "sel": {k: sel[k] for k in ("shaMatch", "countMatch", "membersMatch", "count", "mismatches")},
        "frozen": {k: frozen[k] for k in ("shaMatch", "countMatch", "membersMatch", "count", "mismatches")},
        "candidates": cand_paths == minus,
        "parentsMatch": out["parentsMatch"],
        "mapAllMatch": out["mapAllMatch"],
        "canonicalPin": out["canonicalPyMatchesOraclePin"],
        "canonicalBaseline": out["canonicalPyInSelectedBaseline"],
        "logicalPathBodyEqualParent": out["logicalPathBodyEqualParent"],
        "moduleDocChanged": out["moduleDocChanged"],
        "censusUnique": out["censusUniqueForms"],
        "censusOcc": out["censusOccurrences"],
        "inherited": inherited,
        "liveHasDescriptors": out["liveHasDescriptors"],
        "archiveOk": out["archiveMatchesPin"],
        "invPackages": out["inventoryPackageCount"],
        "opaque": {"noDefault": out["noDefaultOnArrayOrder"], "kindPrivate": out["orderKindPrivate"]},
    }, indent=2))


if __name__ == "__main__":
    main()
