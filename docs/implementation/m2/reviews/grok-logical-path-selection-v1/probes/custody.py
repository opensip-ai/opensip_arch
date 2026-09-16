"""Verify logical-path-selection v1 pins, map, inheritance; copy frozen privately."""
from __future__ import annotations

import hashlib
import json
import shutil
import stat
import sys
from pathlib import Path

ARCH = Path("/Users/sb/code/opensip-ai/opensip_arch")
PRODUCT = Path("/Users/sb/code/opensip-ai/opensip")
REVIEW = Path("/tmp/opensip-implementation/m2-grok-logical-path-selection-v1-review/review")
SEL = "docs/implementation/m2/logical-path-selection-v1-subject.json"
SEL_SHA = "81b43104e418925acaaa44f8e27eb6826b4bb49c2a9db5a816c7a6a105a27632"
FROZEN = Path("/tmp/opensip-implementation/m2-logical-path-subject-01")
FMAN = ARCH / "docs/implementation/m2/trials/logical-path-01/subject.json"
FSHA = "81aa152b14db7184fea036cb480121df86d8f4da5b683748b4b1bc5473ee651c"
ARCHIVE = ARCH / "docs/implementation/m2/trials/logical-path-01/subject.tar.gz"
SCHEMA_SRC = ARCH / "docs/implementation/m1/source-selection-v2/schemas/sources/identity.v3.schema.json"
SCHEMA_SHA = "311c1feb09ff8cd0b207233d2ec0d7440bb1c72fc0470de277ee1891c24bb68f"
V2_LIB = ARCH / "docs/implementation/m2/foundation-primitives-selection-v2/product/crates/identity/src/lib.rs"


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


def main() -> None:
    if not sys.flags.isolated or sys.flags.optimize:
        raise SystemExit("isolated Python without optimization required")
    (REVIEW / "results").mkdir(parents=True, exist_ok=True)
    (REVIEW / "copy").mkdir(parents=True, exist_ok=True)
    sel = verify_manifest(ARCH / SEL, ARCH, SEL_SHA, 23)
    frozen = verify_manifest(FMAN, FROZEN, FSHA, 197)
    successor = json.loads((ARCH / "docs/implementation/m2/logical-path-selection-v1/successor.json").read_bytes())
    subject = json.loads((ARCH / SEL).read_bytes())
    record = "docs/implementation/m2/logical-path-selection-v1/successor.json"
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
    mmap = json.loads((ARCH / "docs/implementation/m2/logical-path-selection-v1/materialization-map.json").read_bytes())
    map_rows = []
    for row in mmap["files"]:
        frozen_p = FROZEN / "product" / row["productPath"]
        cand = ARCH / row["candidatePath"]
        fi, ci = info(frozen_p), info(cand)
        map_rows.append({
            "productPath": row["productPath"],
            "inInventory10": row["productPath"] in inv_files,
            "inventoryRole": None if row["productPath"] not in inv_files else inv_files[row["productPath"]]["role"],
            "frozenMatch": fi["sha256"] == row["sha256"] and fi["bytes"] == row["bytes"],
            "candidateMatch": ci["sha256"] == row["sha256"] and ci["bytes"] == row["bytes"],
        })
    archive = info(ARCHIVE)
    pin = json.loads((ARCH / "docs/implementation/m2/logical-path-selection-v1/evidence/archive-pin.json").read_bytes())
    schema_src = info(SCHEMA_SRC)
    schema_copy = info(FROZEN / "product/schemas/sources/identity-v3.schema.json")
    owner = json.loads((ARCH / "docs/implementation/m2/logical-path-selection-v1/evidence/schema-owner.json").read_bytes())
    inherited = []
    for rel in [
        "crates/identity/Cargo.toml",
        "crates/identity/src/canonical.rs",
        "crates/identity/src/canonical_tests.rs",
        "crates/identity/src/digests.rs",
    ]:
        live = info(PRODUCT / rel)
        fr = info(FROZEN / "product" / rel)
        inherited.append({
            "path": rel,
            "liveEqualsFrozen": live["sha256"] == fr["sha256"],
            "sha256": live["sha256"],
        })
    v2_lib = info(V2_LIB)
    live_lib = info(PRODUCT / "crates/identity/src/lib.rs")
    frozen_lib = info(FROZEN / "product/crates/identity/src/lib.rs")
    dest = REVIEW / "copy" / "frozen-subject"
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(
        FROZEN,
        dest,
        ignore=shutil.ignore_patterns(".git", "target", "node_modules", "python-packages", "__pycache__", "dist"),
        symlinks=False,
    )
    desc_src = (ARCH / "docs/implementation/m2/logical-path-selection-v1/product/crates/identity/src/descriptors.rs").read_text()
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
        "schemaSource": schema_src,
        "schemaSourceMatch": schema_src["sha256"] == SCHEMA_SHA and schema_src["bytes"] == owner["source"]["bytes"],
        "schemaCopyEqualsSource": schema_copy["sha256"] == schema_src["sha256"],
        "schemaSelector": owner["selector"],
        "inheritedUnchangedVsLive": inherited,
        "allInheritedEqualLive": all(r["liveEqualsFrozen"] for r in inherited),
        "liveLibEqualsFoundationV2": live_lib["sha256"] == v2_lib["sha256"],
        "frozenLibDiffersFromFoundationV2": frozen_lib["sha256"] != v2_lib["sha256"],
        "liveHasDescriptors": (PRODUCT / "crates/identity/src/descriptors.rs").exists(),
        "noDefaultDerive": "Default" not in desc_src,
        "noDeserialize": "Deserialize" not in desc_src and "serde" not in desc_src,
        "privateTupleField": "pub struct LogicalPath(String)" in desc_src,
        "privateCopy": str(dest),
        "executedAgainstFrozenTmp": False,
    }
    (REVIEW / "results" / "custody-before.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "sel": {k: sel[k] for k in ("shaMatch", "countMatch", "membersMatch", "count", "mismatches")},
        "frozen": {k: frozen[k] for k in ("shaMatch", "countMatch", "membersMatch", "count", "mismatches")},
        "candidates": cand_paths == minus,
        "parentsMatch": out["parentsMatch"],
        "mapAllMatch": out["mapAllMatch"],
        "schemaSourceMatch": out["schemaSourceMatch"],
        "schemaCopyEqualsSource": out["schemaCopyEqualsSource"],
        "inherited": inherited,
        "liveLibEqualsV2": out["liveLibEqualsFoundationV2"],
        "frozenLibDiffers": out["frozenLibDiffersFromFoundationV2"],
        "liveHasDescriptors": out["liveHasDescriptors"],
        "encapsulation": {
            "noDefaultDerive": out["noDefaultDerive"],
            "noDeserialize": out["noDeserialize"],
            "privateTupleField": out["privateTupleField"],
        },
        "invPackages": out["inventoryPackageCount"],
        "archiveOk": out["archiveMatchesPin"],
    }, indent=2))


if __name__ == "__main__":
    main()
