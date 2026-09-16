"""Custody and joins for inventory v10 and contracts-dependency-selection v1."""
from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path

ARCH = Path("/Users/sb/code/opensip-ai/opensip_arch")
PROD = Path("/Users/sb/code/opensip-ai/opensip")
REVIEW = Path("/tmp/opensip-implementation/m1-grok-contracts-dependency-selection-v1-review/review")
INV_MANIFEST = "docs/implementation/m1/tooling-inventory-v10-subject.json"
SEL_MANIFEST = "docs/implementation/m1/contracts-dependency-selection-v1-subject.json"
EXPECTED_INV = "7afbd34e564f6898ccc07fab63776eeaac6da59b7312fbfddd66d178caf7df6f"
EXPECTED_SEL = "d6404eb9e18bdb7f7f76d57545e0e327154041de881ad90625f0ae3520e5e7be"
EXPECTED_V9 = "ccfa6e348d24b3dbd631372e0bdab78b5db0893c2ce515e58775205194686c0e"
EXPECTED_V9_CAND = "75e5210ab15b7dae14b0c9c15838aeeb5f6c692f7cbf7fcb87f68e9385f958e2"
EXPECTED_V9_REVIEW = "b4d01781d1b81195dede3ba07aa01b3358f28c716d3fdfb7942221bd29a5e596"
FROZEN = Path("/tmp/opensip-implementation/m1-contracts-dependency-integration-subject-02")
FROZEN_MANIFEST = ARCH / "docs/implementation/m1/trials/contracts-dependency-integration-02/subject.json"
FROZEN_ARCHIVE = ARCH / "docs/implementation/m1/trials/contracts-dependency-integration-02/subject.tar.gz"
ADDED = [
    "tools/check_dependencies.py",
    "tools/contracts/dependency-policy.json",
    "tools/tests/test_dependency_policy.py",
]


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
    dest = REVIEW / "copy"
    dest.mkdir(parents=True, exist_ok=True)
    (dest / rel).parent.mkdir(parents=True, exist_ok=True)
    (dest / rel).write_bytes(raw)
    for row in man["files"]:
        dst = dest / row["path"]
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes((ARCH / row["path"]).read_bytes())
    return {
        "rel": rel, "outer": outer, "expected": expected, "match": outer == expected,
        "listed": len(man["files"]), "sorted": paths == sorted(set(paths)),
        "mismatches": mismatches[:10],
        "ok": outer == expected and not mismatches and len(man["files"]) == listed_n and paths == sorted(set(paths)),
    }


def frozen_custody():
    raw = FROZEN_MANIFEST.read_bytes()
    outer = hashlib.sha256(raw).hexdigest()
    man = json.loads(raw)
    mismatches = []
    files = dirs = links = 0
    for row in man["entries"]:
        p = FROZEN / row["path"]
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
    archive = pin(FROZEN_ARCHIVE)
    return {
        "outer": outer,
        "expected": "a5994024d4b9a784249d54b79e91cf707c64affeac67255f4146183e71957563",
        "match": outer == "a5994024d4b9a784249d54b79e91cf707c64affeac67255f4146183e71957563",
        "listed": len(man["entries"]), "files": files, "directories": dirs, "symlinks": links,
        "mismatchCount": len(mismatches), "archive": archive,
        "archiveMatches": archive == {"bytes": 1299182, "sha256": "dbc06f6551c460329b6b67dcfceab4516a701be9a1c15fb28ed0c8b4ddb9ded7"},
        "ok": outer == "a5994024d4b9a784249d54b79e91cf707c64affeac67255f4146183e71957563" and not mismatches and files == 192,
    }


def main():
    if not sys.flags.isolated or sys.flags.optimize:
        raise SystemExit("isolated Python without optimization required")
    results = REVIEW / "results"
    results.mkdir(parents=True, exist_ok=True)
    before = {"inventory": custody_contract(INV_MANIFEST, EXPECTED_INV, 3),
              "selection": custody_contract(SEL_MANIFEST, EXPECTED_SEL, 24)}
    (results / "custody-before.json").write_text(json.dumps(before, indent=2) + "\n")

    v9 = json.loads((ARCH / "docs/implementation/m1/repository-file-inventory.v9.json").read_text())
    v10 = json.loads((ARCH / "docs/implementation/m1/repository-file-inventory.v10.json").read_text())
    unit9 = json.loads((ARCH / "docs/implementation/m1/tooling-inventory-v9-unit.json").read_text())
    lock = json.loads((PROD / "design-lock.json").read_text())
    m9 = {r["path"]: r for r in v9["files"]}
    m10 = {r["path"]: r for r in v10["files"]}
    inherited = sorted(set(m9) & set(m10))
    added = sorted(set(m10) - set(m9))
    other_keys = sorted((set(v9) | set(v10)) - {"standing", "files"})
    live_inv = [r["candidate"]["path"] for r in lock.get("inventorySuccessors", [])]
    live_con = [r["record"]["path"] for r in lock.get("contractSuccessors", [])]
    ownership = []
    for path in added:
        row = m10[path]
        ownership.append({
            "path": path, "package": row["package"], "role": row["role"],
            "mostSpecific": most_specific(v10["packages"], path),
            "mostSpecificMatch": most_specific(v10["packages"], path) == row["package"],
        })
    indices = {name: next(i for i, r in enumerate(v10["files"]) if r["path"] == name)
               for name in ["apps/cli/src/bootstrap.rs", "apps/report/package.json", "package.json"]}
    inventory = {
        "v9Files": len(v9["files"]), "v10Files": len(v10["files"]),
        "inherited": len(inherited),
        "inheritedEqual": all(m9[p] == m10[p] for p in inherited),
        "added": added, "removed": sorted(set(m9) - set(m10)),
        "packagesEqual": v9["packages"] == v10["packages"],
        "otherEqual": {k: v9.get(k) == v10.get(k) for k in other_keys},
        "files7Path": v10["files"][7]["path"],
        "files7Equal": v9["files"][7] == v10["files"][7],
        "remapIndices": indices,
        "parentPin": pin(ARCH / "docs/implementation/m1/repository-file-inventory.v9.json"),
        "candidatePin": pin(ARCH / "docs/implementation/m1/repository-file-inventory.v10.json"),
        "successorPin": pin(ARCH / "docs/implementation/m1/tooling-inventory-v10/successor.json"),
        "ownership": ownership,
        "unit9": {"status": unit9.get("status"), "assent": unit9.get("rootSubstantiveAssent"),
                  "reviewMatch": pin(ARCH / "docs/implementation/m1/reviews/grok-tooling-inventory-v9/review.json")["sha256"] == EXPECTED_V9_REVIEW},
        "liveInvCount": len(live_inv), "liveConCount": len(live_con),
        "inventory9InLiveLock": any(p.endswith("repository-file-inventory.v9.json") for p in live_inv),
        "inventory10InLiveLock": any(p.endswith("repository-file-inventory.v10.json") for p in live_inv),
        "productPresence": {p: (PROD / p).is_file() for p in ADDED},
    }

    sel = json.loads((ARCH / SEL_MANIFEST).read_text())
    successor = json.loads((ARCH / "docs/implementation/m1/contracts-dependency-selection-v1/successor.json").read_text())
    mmap = json.loads((ARCH / "docs/implementation/m1/contracts-dependency-selection-v1/materialization-map.json").read_text())
    policy = json.loads((ARCH / "docs/implementation/m1/contracts-dependency-selection-v1/product/tools/contracts/dependency-policy.json").read_text())
    hist = json.loads((ARCH / "docs/implementation/m1/contracts-dependencies.v1.json").read_text())
    members = pin_rows(sel["files"], "subject")
    member_map = {r["path"]: r for r in members}
    record_path = "docs/implementation/m1/contracts-dependency-selection-v1/successor.json"
    candidates = pin_rows(successor["candidates"], "candidates")
    parents = pin_rows(successor["parents"], "parents")
    owned = []
    for row in mmap["files"]:
        actual = pin(ARCH / row["candidatePath"])
        owned.append({"productPath": row["productPath"],
                      "pinMatch": actual == {"bytes": row["bytes"], "sha256": row["sha256"]},
                      "inInventory10": row["productPath"] in m10})
    three = ["tools/check_dependencies.py", "tools/contracts/dependency-policy.json", "tools/tests/test_dependency_policy.py"]
    three_match = []
    for rel in three:
        selp = ARCH / "docs/implementation/m1/contracts-dependency-selection-v1/product" / rel
        frozenp = FROZEN / "product" / rel
        three_match.append({"path": rel, "match": selp.read_bytes() == frozenp.read_bytes(), "sel": pin(selp)})
    hist_deps = {(d["name"], d["version"], d["checksum"]) for d in hist["dependencies"]}
    pol_deps = {(d["name"], d["version"], d["checksum"]) for d in policy["dependencies"]}
    live_src = []
    for row in policy["localSources"]:
        live = PROD / "crates/contracts" / row["path"]
        actual = pin(live) if live.is_file() else None
        live_src.append({"path": row["path"], "match": actual == {"bytes": row["bytes"], "sha256": row["sha256"]}, "actual": actual})
    selection = {
        "subjectFiles": len(members),
        "cover": {r["path"] for r in candidates} == set(member_map) - {record_path},
        "candidatePinsEqual": all(member_map[r["path"]] == r for r in candidates),
        "passageOverrides": successor.get("passageOverrides"),
        "parents": [{"path": r["path"], "match": pin(ARCH / r["path"]) == {"bytes": r["bytes"], "sha256": r["sha256"]}} for r in parents],
        "owned": owned,
        "threeMatchFrozen": three_match,
        "policySchemaVersion": policy.get("schemaVersion"),
        "depCount": len(policy["dependencies"]),
        "sourceCount": len(policy["localSources"]),
        "histDepMatch": hist_deps == pol_deps,
        "histFeatureMatch": hist.get("resolvedFeatures") == policy.get("resolvedFeatures") if "resolvedFeatures" in hist else "hist-has-features",
        "liveSourcesMatch": all(r["match"] for r in live_src),
        "liveSources": live_src,
        "sourceOwner": policy.get("sourceOwner"),
        "platformLive": any("platform-backend-selection-v1/successor.json" in p for p in live_con),
        "inventory10Live": any(p.endswith("repository-file-inventory.v10.json") for p in live_inv),
    }
    # historical resolved features
    if "resolvedFeatures" in hist:
        selection["histFeatureMatch"] = hist["resolvedFeatures"] == policy["resolvedFeatures"]
    else:
        # compare per-dep features if present on historical rows
        hist_feat = {d["name"]: d.get("features") or d.get("resolvedFeatures") for d in hist["dependencies"]}
        selection["histFeatureKeys"] = {k: v for k, v in hist_feat.items() if v is not None}

    frozen = frozen_custody()
    (results / "inventory-comparison.json").write_text(json.dumps(inventory, indent=2) + "\n")
    (results / "selection-analysis.json").write_text(json.dumps(selection, indent=2) + "\n")
    (results / "frozen-custody.json").write_text(json.dumps(frozen, indent=2) + "\n")
    summary = {
        "invCustody": before["inventory"]["ok"],
        "selCustody": before["selection"]["ok"],
        "frozenCustody": frozen["ok"],
        "invLayout": inventory["inherited"] == 330 and inventory["inheritedEqual"] and inventory["added"] == ADDED
            and inventory["packagesEqual"] and all(inventory["otherEqual"].values())
            and inventory["inventory9InLiveLock"] and not inventory["inventory10InLiveLock"]
            and all(r["mostSpecificMatch"] and r["package"] == "tooling" for r in ownership),
        "selJoins": selection["cover"] and selection["candidatePinsEqual"] and len(owned) == 4
            and all(r["pinMatch"] for r in owned) and all(r["match"] for r in three_match)
            and selection["passageOverrides"] == [] and selection["histDepMatch"]
            and selection["liveSourcesMatch"] and selection["depCount"] == 11 and selection["sourceCount"] == 8,
    }
    (results / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
