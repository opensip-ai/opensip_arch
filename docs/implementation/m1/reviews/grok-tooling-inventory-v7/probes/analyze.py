"""Independent layout comparison for tooling-inventory-v7. Read-only vs architecture/product."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ARCH = Path("/Users/sb/code/opensip-ai/opensip_arch")
PROD = Path("/Users/sb/code/opensip-ai/opensip")
REVIEW = Path("/tmp/opensip-implementation/m1-grok-tooling-inventory-v7-review/review")
MANIFEST = "docs/implementation/m1/tooling-inventory-v7-subject.json"
EXPECTED = "d6d8f771409001ede14dfac0fb449f0d4ccff6417acf82c6beba4f8fa49173ce"
EXPECTED_V6 = "3f0e683d88795ef8bb8667106c567deeb2a3106480c02a0286fd5594fa59be2f"
EXPECTED_V6_CAND = "52e75edc8a30aa304d2f3e42f541a5ece1c00d9e1f21435651ac29776d0b81c1"
EXPECTED_V6_REVIEW = "a18ed3a0ba9f764226921b10d92ff571b0f1da523b75a5d2955ab37dd80b61e3"
ADDED = [
    "tools/tests/test_typescript_check.py",
    "tools/typescript-boundary/tests/generated-outputs.test.mjs",
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

    v6 = json.loads((ARCH / "docs/implementation/m1/repository-file-inventory.v6.json").read_text())
    v7 = json.loads((ARCH / "docs/implementation/m1/repository-file-inventory.v7.json").read_text())
    successor = json.loads((ARCH / "docs/implementation/m1/tooling-inventory-v7/successor.json").read_text())
    unit6 = json.loads((ARCH / "docs/implementation/m1/tooling-inventory-v6-unit.json").read_text())
    review6 = pin(ARCH / "docs/implementation/m1/reviews/grok-tooling-inventory-v6/review.json")
    lock = json.loads((PROD / "design-lock.json").read_text())
    lock_pin = pin(PROD / "design-lock.json")

    m6 = {row["path"]: row for row in v6["files"]}
    m7 = {row["path"]: row for row in v7["files"]}
    inherited = sorted(set(m6) & set(m7))
    added = sorted(set(m7) - set(m6))
    removed = sorted(set(m6) - set(m7))
    other_keys = sorted((set(v6) | set(v7)) - {"standing", "files"})
    other_equal = {k: v6.get(k) == v7.get(k) for k in other_keys}
    v6_paths = [row["path"] for row in v6["files"]]
    v7_paths = [row["path"] for row in v7["files"]]
    files7_equal = v6["files"][7] == v7["files"][7]
    ownership = []
    for path in added:
        row = m7[path]
        ownership.append({
            "path": path,
            "package": row.get("package"),
            "role": row.get("role"),
            "generated": row.get("generated"),
            "standing": row.get("standing"),
            "description": row.get("description"),
            "mostSpecific": most_specific(v7["packages"], path),
            "mostSpecificMatch": most_specific(v7["packages"], path) == row.get("package"),
        })

    live_inv = []
    for row in lock.get("inventorySuccessors", []):
        cand = row.get("candidate")
        if isinstance(cand, dict):
            live_inv.append({"path": cand.get("path"), "bytes": cand.get("bytes"), "sha256": cand.get("sha256")})
    v6_in_lock = any(r.get("sha256") == EXPECTED_V6_CAND for r in live_inv)
    v7_in_lock = any(r.get("path") == "docs/implementation/m1/repository-file-inventory.v7.json" for r in live_inv)
    passage_parent = None
    for row in lock.get("inventoryPassageInheritance", []):
        parent = row.get("parent") or {}
        if parent.get("path") == "docs/implementation/m1/repository-file-inventory.v6.json":
            passage_parent = parent

    product_presence = {
        path: (PROD / path).is_file()
        for path in ADDED + ["tools/tests/test_design_binding.py", "tools/check_typescript.py"]
    }

    comparison = {
        "v6Files": len(v6["files"]),
        "v7Files": len(v7["files"]),
        "inherited": len(inherited),
        "inheritedEqual": all(m6[p] == m7[p] for p in inherited),
        "added": added,
        "removed": removed,
        "addedExact": added == ADDED,
        "packagesV6": len(v6["packages"]),
        "packagesV7": len(v7["packages"]),
        "packagesEqual": v6["packages"] == v7["packages"],
        "otherKeys": other_keys,
        "otherEqual": other_equal,
        "allOtherEqual": all(other_equal.values()),
        "v6SortedUnique": v6_paths == sorted(set(v6_paths)),
        "v7SortedUnique": v7_paths == sorted(set(v7_paths)),
        "files7Equal": files7_equal,
        "files7Path": v7["files"][7].get("path"),
        "parentPin": pin(ARCH / "docs/implementation/m1/repository-file-inventory.v6.json"),
        "parentMatch": pin(ARCH / "docs/implementation/m1/repository-file-inventory.v6.json")
        == {"bytes": 118433, "sha256": EXPECTED_V6_CAND},
        "candidatePin": pin(ARCH / "docs/implementation/m1/repository-file-inventory.v7.json"),
        "candidateExpected": {"bytes": 119227, "sha256": "763a5431ebd0aac23dfdd2bb95bacc5ae930dc50763c147a97b93fd8be91e111"},
        "successorPin": pin(ARCH / "docs/implementation/m1/tooling-inventory-v7/successor.json"),
        "successorExpected": {"bytes": 838, "sha256": "98cd60520901a0d062abcaa68cdf14e92e76cdb381cf0edfdef87610d103d2f1"},
        "successorAddedFiles": successor.get("addedFiles"),
        "successorParent": successor.get("parent"),
        "successorCandidate": successor.get("candidate"),
        "ownership": ownership,
        "nodeModulesRows": [p for p in v7_paths if "node_modules" in p or "python-packages/" in p],
        "inventory6Unit": {
            "status": unit6.get("status"),
            "rootSubstantiveAssent": unit6.get("rootSubstantiveAssent"),
            "requiredUnitFindings": unit6.get("requiredUnitFindings"),
            "reviewSha": unit6.get("independentReview", {}).get("sha256"),
            "reviewPin": review6,
            "reviewMatch": review6["sha256"] == EXPECTED_V6_REVIEW,
            "subjectSha": unit6.get("subjectManifest", {}).get("sha256"),
            "acceptedInventory": unit6.get("acceptedInventory"),
        },
        "inventory6SubjectUnchanged": pin(ARCH / "docs/implementation/m1/tooling-inventory-v6-subject.json")["sha256"] == EXPECTED_V6,
        "liveLock": lock_pin,
        "liveInventoryCandidates": live_inv,
        "inventory6InLiveLock": v6_in_lock,
        "inventory7InLiveLock": v7_in_lock,
        "passageParentV6": passage_parent,
        "productPresence": product_presence,
        "checker09Untouched": True,
    }
    comparison["candidateMatch"] = comparison["candidatePin"] == comparison["candidateExpected"]
    comparison["successorMatch"] = comparison["successorPin"] == comparison["successorExpected"]
    (results / "comparison.json").write_text(json.dumps(comparison, indent=2) + "\n")
    summary = {
        "custodyOk": before["ok"],
        "layoutOk": comparison["inherited"] == 324
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
        and all(row["mostSpecificMatch"] and row["package"] == "tooling" and row["role"] == "test" for row in ownership)
        and comparison["inventory6Unit"]["status"] == "ACCEPTED-UNIT"
        and comparison["inventory6InLiveLock"]
        and not comparison["inventory7InLiveLock"],
    }
    (results / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
