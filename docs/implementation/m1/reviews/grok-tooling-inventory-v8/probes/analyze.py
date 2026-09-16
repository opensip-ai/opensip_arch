"""Independent layout comparison for tooling-inventory-v8. Read-only vs architecture/product."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ARCH = Path("/Users/sb/code/opensip-ai/opensip_arch")
PROD = Path("/Users/sb/code/opensip-ai/opensip")
REVIEW = Path("/tmp/opensip-implementation/m1-grok-tooling-inventory-v8-review/review")
MANIFEST = "docs/implementation/m1/tooling-inventory-v8-subject.json"
EXPECTED = "68c3855e6e12e0b5a02e734d8b9775a99d5e51ca8c9dc5f8199544d98e507b7c"
EXPECTED_V7 = "d6d8f771409001ede14dfac0fb449f0d4ccff6417acf82c6beba4f8fa49173ce"
EXPECTED_V7_CAND = "763a5431ebd0aac23dfdd2bb95bacc5ae930dc50763c147a97b93fd8be91e111"
EXPECTED_V7_REVIEW = "4b9bd97745fc4bc60fd960ee9ebeaec7c75123e0b7a154e383cedbf12a853bb2"
ADDED = [
    "tools/check_package_edges.py",
    "tools/tests/test_package_edges.py",
]


def pin(path: Path) -> dict:
    raw = path.read_bytes()
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def custody(label: str) -> dict:
    raw = (ARCH / MANIFEST).read_bytes()
    outer = hashlib.sha256(raw).hexdigest()
    manifest = json.loads(raw)
    listed = manifest["files"]
    paths = [row["path"] for row in listed]
    mismatches = []
    for row in listed:
        actual = pin(ARCH / row["path"])
        if actual["bytes"] != row["bytes"] or actual["sha256"] != row["sha256"]:
            mismatches.append({"path": row["path"], "actual": actual, "pin": row})
    copy_root = REVIEW / "copy"
    copy_root.mkdir(parents=True, exist_ok=True)
    dest = copy_root / MANIFEST
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(raw)
    for row in listed:
        dst = copy_root / row["path"]
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes((ARCH / row["path"]).read_bytes())
    return {
        "label": label,
        "outerSha256": outer,
        "expected": EXPECTED,
        "match": outer == EXPECTED,
        "listed": len(listed),
        "sorted": paths == sorted(set(paths)),
        "mismatches": mismatches,
        "ok": outer == EXPECTED and not mismatches and len(listed) == 3 and paths == sorted(set(paths)),
    }


def most_specific(packages: list, path: str) -> str | None:
    best = None
    best_len = -1
    for pkg in packages:
        prefix = pkg.get("path") or ""
        if prefix == "":
            candidate_ok = True
            plen = 0
        else:
            candidate_ok = path == prefix or path.startswith(prefix + "/")
            plen = len(prefix)
        if candidate_ok and plen >= best_len:
            best = pkg["id"]
            best_len = plen
    return best


def main() -> None:
    if not sys.flags.isolated or sys.flags.optimize:
        raise SystemExit("isolated Python without optimization required")
    results = REVIEW / "results"
    results.mkdir(parents=True, exist_ok=True)
    before = custody("before")
    (results / "custody-before.json").write_text(json.dumps(before, indent=2) + "\n")

    v7 = json.loads((ARCH / "docs/implementation/m1/repository-file-inventory.v7.json").read_text())
    v8 = json.loads((ARCH / "docs/implementation/m1/repository-file-inventory.v8.json").read_text())
    successor = json.loads((ARCH / "docs/implementation/m1/tooling-inventory-v8/successor.json").read_text())
    unit7 = json.loads((ARCH / "docs/implementation/m1/tooling-inventory-v7-unit.json").read_text())
    review7 = pin(ARCH / "docs/implementation/m1/reviews/grok-tooling-inventory-v7/review.json")
    cargo = json.loads((ARCH / "docs/implementation/m1/package-boundaries-unit.v1.json").read_text())
    lock = json.loads((PROD / "design-lock.json").read_text())
    lock_pin = pin(PROD / "design-lock.json")

    m7 = {row["path"]: row for row in v7["files"]}
    m8 = {row["path"]: row for row in v8["files"]}
    inherited = sorted(set(m7) & set(m8))
    added = sorted(set(m8) - set(m7))
    removed = sorted(set(m7) - set(m8))
    other_keys = sorted((set(v7) | set(v8)) - {"standing", "files"})
    other_equal = {k: v7.get(k) == v8.get(k) for k in other_keys}
    v7_paths = [row["path"] for row in v7["files"]]
    v8_paths = [row["path"] for row in v8["files"]]
    files7_equal = v7["files"][7] == v8["files"][7]
    ownership = []
    for path in added:
        row = m8[path]
        ownership.append({
            "path": path,
            "package": row.get("package"),
            "role": row.get("role"),
            "generated": row.get("generated"),
            "standing": row.get("standing"),
            "description": row.get("description"),
            "mostSpecific": most_specific(v8["packages"], path),
            "mostSpecificMatch": most_specific(v8["packages"], path) == row.get("package"),
        })

    live_inv = []
    for row in lock.get("inventorySuccessors", []):
        cand = row.get("candidate")
        if isinstance(cand, dict):
            live_inv.append({"path": cand.get("path"), "bytes": cand.get("bytes"), "sha256": cand.get("sha256")})

    comparison = {
        "v7Files": len(v7["files"]),
        "v8Files": len(v8["files"]),
        "inherited": len(inherited),
        "inheritedEqual": all(m7[p] == m8[p] for p in inherited),
        "added": added,
        "removed": removed,
        "addedExact": added == ADDED,
        "packagesV7": len(v7["packages"]),
        "packagesV8": len(v8["packages"]),
        "packagesEqual": v7["packages"] == v8["packages"],
        "otherKeys": other_keys,
        "otherEqual": other_equal,
        "allOtherEqual": all(other_equal.values()),
        "v7SortedUnique": v7_paths == sorted(set(v7_paths)),
        "v8SortedUnique": v8_paths == sorted(set(v8_paths)),
        "files7Equal": files7_equal,
        "files7Path": v8["files"][7].get("path"),
        "parentPin": pin(ARCH / "docs/implementation/m1/repository-file-inventory.v7.json"),
        "parentMatch": pin(ARCH / "docs/implementation/m1/repository-file-inventory.v7.json")
        == {"bytes": 119227, "sha256": EXPECTED_V7_CAND},
        "candidatePin": pin(ARCH / "docs/implementation/m1/repository-file-inventory.v8.json"),
        "candidateExpected": {"bytes": 119982, "sha256": "c4a1242cb1ea15b260927abd4b844bce4d134be465a6b7e4930992229dda2611"},
        "successorPin": pin(ARCH / "docs/implementation/m1/tooling-inventory-v8/successor.json"),
        "successorExpected": {"bytes": 868, "sha256": "f55f82d1f75a25d47058d667e70fd94cf130b4889c2cdb23754b0ecf157a84ff"},
        "successorAddedFiles": successor.get("addedFiles"),
        "successorParent": successor.get("parent"),
        "successorCandidate": successor.get("candidate"),
        "ownership": ownership,
        "nodeModulesRows": [p for p in v8_paths if "node_modules" in p or "python-packages/" in p],
        "inventory7Unit": {
            "status": unit7.get("status"),
            "rootSubstantiveAssent": unit7.get("rootSubstantiveAssent"),
            "requiredUnitFindings": unit7.get("requiredUnitFindings"),
            "reviewSha": unit7.get("independentReview", {}).get("sha256"),
            "reviewPin": review7,
            "reviewMatch": review7["sha256"] == EXPECTED_V7_REVIEW,
            "subjectSha": unit7.get("subjectManifest", {}).get("sha256"),
            "acceptedInventory": unit7.get("acceptedInventory"),
        },
        "inventory7SubjectUnchanged": pin(ARCH / "docs/implementation/m1/tooling-inventory-v7-subject.json")["sha256"] == EXPECTED_V7,
        "liveLock": lock_pin,
        "liveInventoryCandidates": live_inv,
        "inventory7InLiveLock": any(r.get("sha256") == EXPECTED_V7_CAND for r in live_inv),
        "inventory8InLiveLock": any(r.get("path") == "docs/implementation/m1/repository-file-inventory.v8.json" for r in live_inv),
        "inventory6InLiveLock": any(r.get("path") == "docs/implementation/m1/repository-file-inventory.v6.json" for r in live_inv),
        "productPresence": {path: (PROD / path).is_file() for path in ADDED + [
            "tools/check_typescript.py",
            "tools/tests/test_typescript_check.py",
            "tools/tests/test_design_binding.py",
        ]},
        "cargoChecker02Unit": {
            "status": cargo.get("status"),
            "rootSubstantiveAssent": cargo.get("rootSubstantiveAssent"),
            "integrationApproved": cargo.get("integrationApproved"),
            "requiredUnitFindings": cargo.get("requiredUnitFindings"),
        },
    }
    comparison["candidateMatch"] = comparison["candidatePin"] == comparison["candidateExpected"]
    comparison["successorMatch"] = comparison["successorPin"] == comparison["successorExpected"]
    (results / "comparison.json").write_text(json.dumps(comparison, indent=2) + "\n")
    summary = {
        "custodyOk": before["ok"],
        "layoutOk": comparison["inherited"] == 326
        and comparison["inheritedEqual"]
        and comparison["addedExact"]
        and comparison["removed"] == []
        and comparison["packagesEqual"]
        and comparison["allOtherEqual"]
        and comparison["parentMatch"]
        and comparison["candidateMatch"]
        and comparison["successorMatch"]
        and comparison["files7Path"] == "apps/cli/src/bootstrap.rs"
        and comparison["files7Equal"]
        and all(row["mostSpecificMatch"] and row["package"] == "tooling" for row in ownership)
        and {row["path"]: row["role"] for row in ownership} == {
            "tools/check_package_edges.py": "entrypoint",
            "tools/tests/test_package_edges.py": "test",
        }
        and comparison["inventory7Unit"]["status"] == "ACCEPTED-UNIT"
        and comparison["inventory7Unit"]["rootSubstantiveAssent"] is True
        and not comparison["inventory7InLiveLock"]
        and not comparison["inventory8InLiveLock"],
    }
    (results / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
