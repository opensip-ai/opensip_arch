"""Custody and joins for inventory v9 and platform-backend-selection v1."""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import sys
from pathlib import Path

ARCH = Path("/Users/sb/code/opensip-ai/opensip_arch")
PROD = Path("/Users/sb/code/opensip-ai/opensip")
REVIEW = Path("/tmp/opensip-implementation/m1-grok-platform-backend-selection-v1-review/review")
INV_MANIFEST = "docs/implementation/m1/tooling-inventory-v9-subject.json"
SEL_MANIFEST = "docs/implementation/m1/platform-backend-selection-v1-subject.json"
EXPECTED_INV = "ccfa6e348d24b3dbd631372e0bdab78b5db0893c2ce515e58775205194686c0e"
EXPECTED_SEL = "3ad044c637d3d6b5c8010957bdd8337dce696c89c6d8f8cc79812555e2240134"
EXPECTED_V8 = "68c3855e6e12e0b5a02e734d8b9775a99d5e51ca8c9dc5f8199544d98e507b7c"
EXPECTED_V8_CAND = "c4a1242cb1ea15b260927abd4b844bce4d134be465a6b7e4930992229dda2611"
EXPECTED_V8_REVIEW = "ca5afc203984e52df7caa33de033d59a6408f33c0e1a21e60a60813805ea6032"
GUARD = Path("/tmp/opensip-implementation/m1-platform-backend-guard-subject-01")
GUARD_MANIFEST = Path("/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m1/trials/platform-backend-guard-01/subject.json")
GUARD_ARCHIVE = Path("/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m1/trials/platform-backend-guard-01/subject.tar.gz")
ADDED = ["crates/platform/build.rs", "tools/tests/test_entropy_backend.py"]


def pin(path: Path) -> dict:
    raw = path.read_bytes()
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def pin_rows(value, label):
    if not isinstance(value, list) or not value:
        raise ValueError(label)
    paths = [row.get("path") for row in value]
    if any(not isinstance(p, str) for p in paths) or paths != sorted(set(paths)):
        raise ValueError(label + " unsorted")
    return value


def most_specific(packages, path):
    best, best_len = None, -1
    for pkg in packages:
        prefix = pkg.get("path") or ""
        ok = True if prefix == "" else (path == prefix or path.startswith(prefix + "/"))
        plen = 0 if prefix == "" else len(prefix)
        if ok and plen >= best_len:
            best, best_len = pkg["id"], plen
    return best


def custody_contract(rel, expected, listed_n):
    raw = (ARCH / rel).read_bytes()
    outer = hashlib.sha256(raw).hexdigest()
    man = json.loads(raw)
    mismatches = []
    for row in man["files"]:
        actual = pin(ARCH / row["path"])
        if actual["bytes"] != row["bytes"] or actual["sha256"] != row["sha256"]:
            mismatches.append(row["path"])
    paths = [r["path"] for r in man["files"]]
    return {
        "rel": rel,
        "outer": outer,
        "expected": expected,
        "match": outer == expected,
        "listed": len(man["files"]),
        "sorted": paths == sorted(set(paths)),
        "mismatches": mismatches[:10],
        "ok": outer == expected and not mismatches and len(man["files"]) == listed_n and paths == sorted(set(paths)),
    }


def copy_listed(rel):
    man = json.loads((ARCH / rel).read_text())
    dest = REVIEW / "copy"
    dest.mkdir(parents=True, exist_ok=True)
    (dest / rel).parent.mkdir(parents=True, exist_ok=True)
    (dest / rel).write_bytes((ARCH / rel).read_bytes())
    for row in man["files"]:
        dst = dest / row["path"]
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes((ARCH / row["path"]).read_bytes())


def guard_custody():
    raw = GUARD_MANIFEST.read_bytes()
    outer = hashlib.sha256(raw).hexdigest()
    man = json.loads(raw)
    mismatches = []
    files = dirs = links = 0
    for row in man["entries"]:
        p = GUARD / row["path"]
        st = p.lstat()
        mode = st.st_mode & 0o777
        if row["type"] == "file":
            files += 1
            actual = pin(p)
            if actual["bytes"] != row["bytes"] or actual["sha256"] != row["sha256"] or mode != row["mode"]:
                mismatches.append(row["path"])
        elif row["type"] == "directory":
            dirs += 1
            if not p.is_dir() or mode != row["mode"]:
                mismatches.append(row["path"])
        else:
            links += 1
            if os.readlink(p) != row.get("target") or mode != row["mode"]:
                mismatches.append(row["path"])
    archive = pin(GUARD_ARCHIVE)
    return {
        "outer": outer,
        "expected": "442df270bf12916d6a11925f0579e91d8380d158c48be647a2986f8c76029c3d",
        "match": outer == "442df270bf12916d6a11925f0579e91d8380d158c48be647a2986f8c76029c3d",
        "listed": len(man["entries"]),
        "files": files,
        "directories": dirs,
        "symlinks": links,
        "mismatchCount": len(mismatches),
        "archive": archive,
        "archiveMatches": archive == {"bytes": 1160782, "sha256": "e299f86e581715336f1df21aadc983bb0fbd34718f2ab118c6341b4d828903ef"},
        "ok": outer == "442df270bf12916d6a11925f0579e91d8380d158c48be647a2986f8c76029c3d" and not mismatches and files == 142 and archive["bytes"] == 1160782,
    }


def main():
    if not sys.flags.isolated or sys.flags.optimize:
        raise SystemExit("isolated Python without optimization required")
    results = REVIEW / "results"
    results.mkdir(parents=True, exist_ok=True)
    before = {"inventory": custody_contract(INV_MANIFEST, EXPECTED_INV, 3), "selection": custody_contract(SEL_MANIFEST, EXPECTED_SEL, 24)}
    (results / "custody-before.json").write_text(json.dumps(before, indent=2) + "\n")
    copy_listed(INV_MANIFEST)
    copy_listed(SEL_MANIFEST)

    v8 = json.loads((ARCH / "docs/implementation/m1/repository-file-inventory.v8.json").read_text())
    v9 = json.loads((ARCH / "docs/implementation/m1/repository-file-inventory.v9.json").read_text())
    unit8 = json.loads((ARCH / "docs/implementation/m1/tooling-inventory-v8-unit.json").read_text())
    lock = json.loads((PROD / "design-lock.json").read_text())
    m8 = {r["path"]: r for r in v8["files"]}
    m9 = {r["path"]: r for r in v9["files"]}
    inherited = sorted(set(m8) & set(m9))
    added = sorted(set(m9) - set(m8))
    other_keys = sorted((set(v8) | set(v9)) - {"standing", "files"})
    live_inv = [r["candidate"]["path"] for r in lock.get("inventorySuccessors", [])]
    live_con = [r["record"]["path"] for r in lock.get("contractSuccessors", [])]
    passages = lock.get("inventoryPassageInheritance", [])
    ownership = []
    for path in added:
        row = m9[path]
        ownership.append({
            "path": path, "package": row["package"], "role": row["role"],
            "mostSpecific": most_specific(v9["packages"], path),
            "mostSpecificMatch": most_specific(v9["packages"], path) == row["package"],
            "description": row["description"],
        })
    indices = {name: next(i for i, r in enumerate(v9["files"]) if r["path"] == name) for name in [
        "apps/cli/src/bootstrap.rs", "apps/report/package.json", "package.json"]}
    inventory = {
        "v8Files": len(v8["files"]), "v9Files": len(v9["files"]),
        "inherited": len(inherited),
        "inheritedEqual": all(m8[p] == m9[p] for p in inherited),
        "added": added, "removed": sorted(set(m8) - set(m9)),
        "packagesEqual": v8["packages"] == v9["packages"],
        "otherEqual": {k: v8.get(k) == v9.get(k) for k in other_keys},
        "files7Equal": v8["files"][7] == v9["files"][7],
        "files7Path": v9["files"][7]["path"],
        "remapIndices": indices,
        "parentPin": pin(ARCH / "docs/implementation/m1/repository-file-inventory.v8.json"),
        "candidatePin": pin(ARCH / "docs/implementation/m1/repository-file-inventory.v9.json"),
        "successorPin": pin(ARCH / "docs/implementation/m1/tooling-inventory-v9/successor.json"),
        "ownership": ownership,
        "unit8": {"status": unit8.get("status"), "assent": unit8.get("rootSubstantiveAssent"),
                  "reviewMatch": pin(ARCH / "docs/implementation/m1/reviews/grok-tooling-inventory-v8/review.json")["sha256"] == EXPECTED_V8_REVIEW,
                  "subjectMatch": unit8.get("subjectManifest", {}).get("sha256") == EXPECTED_V8},
        "liveInv": live_inv, "liveContracts": live_con,
        "inventory8InLiveLock": any(p.endswith("repository-file-inventory.v8.json") for p in live_inv),
        "inventory9InLiveLock": any(p.endswith("repository-file-inventory.v9.json") for p in live_inv),
        "livePassageParents": [p.get("parent", {}).get("path") for p in passages],
        "livePassageSelectors": [p.get("selector") for p in passages],
        "productPresence": {p: (PROD / p).is_file() for p in ADDED + ["crates/platform/Cargo.toml"]},
    }

    sel = json.loads((ARCH / SEL_MANIFEST).read_text())
    successor = json.loads((ARCH / "docs/implementation/m1/platform-backend-selection-v1/successor.json").read_text())
    mmap = json.loads((ARCH / "docs/implementation/m1/platform-backend-selection-v1/materialization-map.json").read_text())
    members = pin_rows(sel["files"], "subject")
    member_map = {r["path"]: r for r in members}
    record_path = "docs/implementation/m1/platform-backend-selection-v1/successor.json"
    candidates = pin_rows(successor["candidates"], "candidates")
    parents = pin_rows(successor["parents"], "parents")
    owned = []
    for row in mmap["files"]:
        actual = pin(ARCH / row["candidatePath"])
        owned.append({
            "productPath": row["productPath"],
            "pinMatch": actual == {"bytes": row["bytes"], "sha256": row["sha256"]},
            "inInventory9": row["productPath"] in m9,
        })
    three = ["crates/platform/Cargo.toml", "crates/platform/build.rs", "tools/tests/test_entropy_backend.py"]
    three_match = []
    for rel in three:
        selp = ARCH / "docs/implementation/m1/platform-backend-selection-v1/product" / rel
        guardp = GUARD / "product" / rel
        three_match.append({"path": rel, "match": selp.read_bytes() == guardp.read_bytes(), "sel": pin(selp), "guard": pin(guardp)})
    live_toml = pin(PROD / "crates/platform/Cargo.toml")
    sel_toml = pin(ARCH / "docs/implementation/m1/platform-backend-selection-v1/product/crates/platform/Cargo.toml")
    live_readme = pin(PROD / "tools/README.md")
    sel_readme = pin(ARCH / "docs/implementation/m1/platform-backend-selection-v1/product/tools/README.md")
    selection = {
        "subjectFiles": len(members),
        "cover": {r["path"] for r in candidates} == set(member_map) - {record_path},
        "candidatePinsEqual": all(member_map[r["path"]] == r for r in candidates),
        "passageOverrides": successor.get("passageOverrides"),
        "parents": [{"path": r["path"], "match": pin(ARCH / r["path"]) == {"bytes": r["bytes"], "sha256": r["sha256"]}} for r in parents],
        "owned": owned,
        "threeMatchGuard": three_match,
        "liveTomlEqualsSelection": live_toml == sel_toml,
        "liveToml": live_toml, "selToml": sel_toml,
        "liveReadmeEqualsSelection": live_readme == sel_readme,
        "readmeChanged": live_readme != sel_readme,
        "getrandomUnchanged": "=0.4.3" in (ARCH / "docs/implementation/m1/platform-backend-selection-v1/product/crates/platform/Cargo.toml").read_text()
            and "=0.4.3" in (PROD / "crates/platform/Cargo.toml").read_text(),
        "buildKeyAdded": 'build = "build.rs"' in (ARCH / "docs/implementation/m1/platform-backend-selection-v1/product/crates/platform/Cargo.toml").read_text()
            and "build =" not in (PROD / "crates/platform/Cargo.toml").read_text(),
        "bootstrapLive": any("bootstrap-selection-v1/successor.json" in p for p in live_con),
        "inventory9Live": any(p.endswith("repository-file-inventory.v9.json") for p in live_inv),
    }
    guard = guard_custody()
    (results / "inventory-comparison.json").write_text(json.dumps(inventory, indent=2) + "\n")
    (results / "selection-analysis.json").write_text(json.dumps(selection, indent=2) + "\n")
    (results / "guard-custody.json").write_text(json.dumps(guard, indent=2) + "\n")
    summary = {
        "invCustody": before["inventory"]["ok"],
        "selCustody": before["selection"]["ok"],
        "guardCustody": guard["ok"],
        "invLayout": inventory["inherited"] == 328 and inventory["inheritedEqual"] and inventory["added"] == ADDED
            and inventory["packagesEqual"] and all(inventory["otherEqual"].values())
            and inventory["inventory8InLiveLock"] and not inventory["inventory9InLiveLock"]
            and inventory["files7Path"] == "apps/cli/src/bootstrap.rs",
        "selJoins": selection["cover"] and selection["candidatePinsEqual"] and len(owned) == 4
            and all(r["pinMatch"] for r in owned) and all(r["match"] for r in three_match)
            and selection["passageOverrides"] == [] and selection["buildKeyAdded"] and selection["getrandomUnchanged"],
        "livePassagesOnlyCliOnV8": inventory["livePassageSelectors"] == [{"jsonPointer": "/files/7/description"}],
    }
    (results / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
