"""Verify checker-mode pins, 0755 bin, archive mode, map, parents; copy privately."""
from __future__ import annotations

import hashlib
import json
import shutil
import stat
import sys
import tarfile
from pathlib import Path

ARCH = Path("/Users/sb/code/opensip-ai/opensip_arch")
PRODUCT = Path("/Users/sb/code/opensip-ai/opensip")
REVIEW = Path("/tmp/opensip-implementation/m1-grok-checker-mode-selection-v1-review/review")
SEL = "docs/implementation/m1/checker-mode-selection-v1-subject.json"
SEL_SHA = "a7c5227fb5cf34af61ee2f7ff6f517ec561071ede8c11023413ddbd9d7dd4b88"
FROZEN = Path("/tmp/opensip-implementation/m1-checker-mode-subject-01")
FMAN = ARCH / "docs/implementation/m1/trials/checker-mode-01/subject.json"
FSHA = "e09689acdab6b4a65066c593131785004180df2468e21895b0d699ccb5df69b4"
ARCHIVE = ARCH / "docs/implementation/m1/trials/checker-mode-01/subject.tar.gz"
BIN_REL = "tools/typescript-boundary/bin/check-boundary.mjs"
BIN_SHA = "76e31fbe92ce1586dea6be365b6a3e77d61dbf7e48e2a72dae683d728eff10f1"


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def info(path: Path) -> dict:
    raw = path.read_bytes()
    return {
        "bytes": len(raw),
        "sha256": sha256_bytes(raw),
        "mode": stat.S_IMODE(path.stat().st_mode),
        "modeOctal": format(stat.S_IMODE(path.stat().st_mode), "04o"),
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
    successor = json.loads((ARCH / "docs/implementation/m1/checker-mode-selection-v1/successor.json").read_bytes())
    subject = json.loads((ARCH / SEL).read_bytes())
    record = "docs/implementation/m1/checker-mode-selection-v1/successor.json"
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
    mmap = json.loads((ARCH / "docs/implementation/m1/checker-mode-selection-v1/materialization-map.json").read_bytes())
    map_rows = []
    for row in mmap["files"]:
        frozen_p = FROZEN / "product" / row["productPath"]
        cand = ARCH / row["candidatePath"]
        fi, ci = info(frozen_p), info(cand)
        map_rows.append({
            "productPath": row["productPath"],
            "inInventory10": row["productPath"] in inv_files,
            "requiredModeOctal": row.get("requiredModeOctal"),
            "frozenMatch": fi["sha256"] == row["sha256"] and fi["bytes"] == row["bytes"],
            "candidateMatch": ci["sha256"] == row["sha256"] and ci["bytes"] == row["bytes"],
            "frozenMode": fi["modeOctal"],
            "candidateMode": ci["modeOctal"],
        })
    archive = info(ARCHIVE)
    pin = json.loads((ARCH / "docs/implementation/m1/checker-mode-selection-v1/evidence/archive-pin.json").read_bytes())
    tar_modes = []
    with tarfile.open(ARCHIVE) as tar:
        for member in tar.getmembers():
            if member.name.endswith("check-boundary.mjs"):
                tar_modes.append({"name": member.name, "modeOctal": format(member.mode, "04o"), "size": member.size})
    live_bin = info(PRODUCT / BIN_REL)
    cand_bin = info(ARCH / "docs/implementation/m1/checker-mode-selection-v1/product" / BIN_REL)
    frozen_bin = info(FROZEN / "product" / BIN_REL)
    old_map = json.loads((PRODUCT / "tools/typescript-boundary/tests/fixtures/staging-map.json").read_bytes())
    new_map = json.loads((ARCH / "docs/implementation/m1/checker-mode-selection-v1/product/tools/typescript-boundary/tests/fixtures/staging-map.json").read_bytes())
    changes = [(x, y) for x, y in zip(old_map["files"], new_map["files"]) if x != y]
    dest = REVIEW / "copy" / "frozen-subject"
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(FROZEN, dest, ignore=shutil.ignore_patterns(".git", "target", "node_modules", "__pycache__", "dist"), symlinks=False)
    copy_bin = info(dest / "product" / BIN_REL)
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
        "tarCheckerModes": tar_modes,
        "liveBin": live_bin,
        "candidateBin": cand_bin,
        "frozenBin": frozen_bin,
        "copyBin": copy_bin,
        "runtimeBytesUnchanged": live_bin["sha256"] == cand_bin["sha256"] == BIN_SHA,
        "liveMode0644": live_bin["modeOctal"] == "0644",
        "candidateMode0755": cand_bin["modeOctal"] == "0755",
        "frozenMode0755": frozen_bin["modeOctal"] == "0755",
        "copyMode0755": copy_bin["modeOctal"] == "0755",
        "tarMode0755": all(r["modeOctal"] == "0755" for r in tar_modes) and tar_modes,
        "stagingRowCount": len(old_map["files"]),
        "stagingRowsChanged": len(changes),
        "stagingChangedPath": None if not changes else changes[0][0]["path"],
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
        "bytesUnchanged": out["runtimeBytesUnchanged"],
        "liveMode": live_bin["modeOctal"],
        "candMode": cand_bin["modeOctal"],
        "frozenMode": frozen_bin["modeOctal"],
        "copyMode": copy_bin["modeOctal"],
        "tarModes": tar_modes,
        "stagingChanged": out["stagingRowsChanged"],
        "stagingPath": out["stagingChangedPath"],
        "invPackages": out["inventoryPackageCount"],
    }, indent=2))


if __name__ == "__main__":
    main()
