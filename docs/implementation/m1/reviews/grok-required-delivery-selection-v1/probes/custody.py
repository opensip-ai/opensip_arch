"""Verify required-delivery-selection v1 pins, map, parents; copy privately."""
from __future__ import annotations

import hashlib
import json
import shutil
import stat
import sys
from pathlib import Path

ARCH = Path("/Users/sb/code/opensip-ai/opensip_arch")
PRODUCT = Path("/Users/sb/code/opensip-ai/opensip")
REVIEW = Path("/tmp/opensip-implementation/m1-grok-required-delivery-selection-v1-review/review")
SEL = "docs/implementation/m1/required-delivery-selection-v1-subject.json"
SEL_SHA = "62bc0033f1c7817e492fcad2e37202aaec978a199b02f33671db25da047ebc14"
FROZEN = Path("/tmp/opensip-implementation/m1-required-delivery-subject-01")
FMAN = ARCH / "docs/implementation/m1/trials/required-delivery-01/subject.json"
FSHA = "3320546737eda04874b349ea3c5b4e2824a0003a1546731a50cd2347bf9a5761"
ARCHIVE = ARCH / "docs/implementation/m1/trials/required-delivery-01/subject.tar.gz"


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


def verify_manifest(manifest: Path, root: Path, expected_sha: str) -> dict:
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
        "membersMatch": not mismatches,
        "mismatches": mismatches,
    }


def main() -> None:
    if not sys.flags.isolated or sys.flags.optimize:
        raise SystemExit("isolated Python without optimization required")
    (REVIEW / "results").mkdir(parents=True, exist_ok=True)
    sel = verify_manifest(ARCH / SEL, ARCH, SEL_SHA)
    frozen = verify_manifest(FMAN, FROZEN, FSHA)
    successor = json.loads((ARCH / "docs/implementation/m1/required-delivery-selection-v1/successor.json").read_bytes())
    subject = json.loads((ARCH / SEL).read_bytes())
    record = "docs/implementation/m1/required-delivery-selection-v1/successor.json"
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
    mmap = json.loads((ARCH / "docs/implementation/m1/required-delivery-selection-v1/materialization-map.json").read_bytes())
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
    pin = json.loads((ARCH / "docs/implementation/m1/required-delivery-selection-v1/evidence/archive-pin.json").read_bytes())
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
        "crates/host/src/outcomes.rs",
        "crates/host/src/request.rs",
        "apps/cli/src/arguments.rs",
        "apps/cli/src/main.rs",
        "crates/identity/src/lib.rs",
        "crates/identity/src/digests.rs",
        "Cargo.lock",
    ]:
        live = PRODUCT / rel
        fr = dest / "product" / rel
        inherited.append({
            "path": rel,
            "liveExists": live.exists(),
            "equal": live.exists() and info(live)["sha256"] == info(fr)["sha256"],
        })
    live_delivery = (PRODUCT / "crates/host/src/delivery.rs").exists()
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
        "inherited": inherited,
        "liveHasDeliveryRs": live_delivery,
        "frozenHasDescriptors": (dest / "product/crates/identity/src/descriptors.rs").exists(),
        "privateCopy": str(dest),
        "executedAgainstFrozenTmp": False,
    }
    (REVIEW / "results" / "custody-before.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "sel": {k: sel[k] for k in ("shaMatch", "count", "membersMatch", "mismatches")},
        "frozen": {k: frozen[k] for k in ("shaMatch", "count", "membersMatch", "mismatches")},
        "candidates": cand_paths == minus,
        "parentsMatch": out["parentsMatch"],
        "mapAllMatch": out["mapAllMatch"],
        "archiveOk": out["archiveMatchesPin"],
        "invPackages": out["inventoryPackageCount"],
        "liveHasDeliveryRs": live_delivery,
        "frozenHasDescriptors": out["frozenHasDescriptors"],
        "inherited": inherited,
        "mapRoles": {r["productPath"]: r["inventoryRole"] for r in map_rows},
    }, indent=2))


if __name__ == "__main__":
    main()
