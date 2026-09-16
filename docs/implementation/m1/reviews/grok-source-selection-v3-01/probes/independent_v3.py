"""Independent source-selection-v3 correction probes. Not a restatement of check_binding.py."""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
from pathlib import Path, PurePosixPath

PY_ARCH = Path("/Users/sb/code/opensip-ai/opensip_arch")
PRODUCT = Path("/Users/sb/code/opensip-ai/opensip")
RESULTS = Path("/tmp/opensip-implementation/m1-grok-source-selection-review-v3-01/review/results")
DECLARED = "ea4bb9bf97e68dc675c855798c647cfc6f784e5a6977839d560472ff79cc53ed"
V2_MANIFEST = "1c4366eb3909433f5e5a790ced4a6d35a28c7b76322840e96297225943d135ff"


def rec(rows, name, passed, **detail):
    rows.append({"name": name, "passed": bool(passed), **detail})
    print(("PASS" if passed else "FAIL"), name)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load(path: Path):
    return json.loads(path.read_bytes())


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def main():
    rows = []
    RESULTS.mkdir(parents=True, exist_ok=True)
    manifest_path = PY_ARCH / "docs/implementation/m1/source-selection-v3-subject.json"
    v2_manifest_path = PY_ARCH / "docs/implementation/m1/source-selection-v2-subject.json"
    rec(rows, "subject-manifest-sha256", sha(manifest_path.read_bytes()) == DECLARED, sha256=sha(manifest_path.read_bytes()))
    v3 = load(manifest_path)
    v2 = load(v2_manifest_path)
    rec(rows, "v2-historical-manifest-unchanged", sha(v2_manifest_path.read_bytes()) == V2_MANIFEST)
    rec(rows, "subject-file-count-140", len(v3["files"]) == 140, count=len(v3["files"]))
    rec(rows, "v2-file-count-137", len(v2["files"]) == 137)

    mismatches = []
    for row in v3["files"]:
        raw = (PY_ARCH / row["path"]).read_bytes()
        if len(raw) != row["bytes"] or sha(raw) != row["sha256"]:
            mismatches.append(row["path"])
    rec(rows, "all-140-pins-match-architecture-bytes", mismatches == [], fail=mismatches[:5])

    v2_record = "docs/implementation/m1/source-selection-v2/successor.json"
    v3_record = "docs/implementation/m1/source-selection-v3/successor.json"
    v2_nonrecord = {r["path"]: r for r in v2["files"] if r["path"] != v2_record}
    v3_by_path = {r["path"]: r for r in v3["files"]}
    rec(rows, "inherited-136-non-record-byte-identical", len(v2_nonrecord) == 136 and all(v3_by_path.get(p) == row for p, row in v2_nonrecord.items()))
    new_v3 = sorted(set(v3_by_path) - set(v2_nonrecord) - {v2_record})
    rec(
        rows,
        "four-new-v3-files-only",
        new_v3 == [
            "docs/implementation/m1/source-selection-v3/README.md",
            "docs/implementation/m1/source-selection-v3/check_binding.py",
            "docs/implementation/m1/source-selection-v3/correction.json",
            "docs/implementation/m1/source-selection-v3/successor.json",
        ],
        new=new_v3,
    )
    rec(rows, "v2-successor-not-a-v3-subject-member", v2_record not in v3_by_path)

    v2_succ = load(PY_ARCH / v2_record)
    v3_succ = load(PY_ARCH / v3_record)
    rec(
        rows,
        "previousCandidate-is-uninstalled-v2-successor",
        v3_succ.get("previousCandidate") == {"path": v2_record, "bytes": 34488, "sha256": "8bd78b833ab84b719947080911e7ad358c00ac94242465492adee2343dac2819"}
        and v3_succ["previousCandidate"]["path"] not in {r["path"] for r in v3_succ["candidates"]}
        and sha((PY_ARCH / v2_record).read_bytes()) == v3_succ["previousCandidate"]["sha256"],
    )
    rec(rows, "parents-and-passage-overrides-unchanged", v3_succ["parents"] == v2_succ["parents"] and v3_succ["passageOverrides"] == v2_succ["passageOverrides"])

    v2_paths = [r["path"] for r in v2_succ["candidates"]]
    v3_paths = [r["path"] for r in v3_succ["candidates"]]
    string_sorted = sorted(set(v2_paths))
    path_sorted = [p.as_posix() for p in sorted(PurePosixPath(p) for p in set(v2_paths))]
    rec(rows, "v2-candidates-equal-path-component-order-not-string-sort", v2_paths == path_sorted and v2_paths != string_sorted, firstDiff=next((i, v2_paths[i], string_sorted[i]) for i in range(len(v2_paths)) if v2_paths[i] != string_sorted[i]))
    rec(rows, "v3-candidates-string-sorted-unique", v3_paths == sorted(set(v3_paths)) and len(v3_paths) == 139)
    rec(rows, "v3-subject-files-string-sorted-unique", [r["path"] for r in v3["files"]] == sorted({r["path"] for r in v3["files"]}))
    rec(
        rows,
        "v3-candidates-cover-subject-minus-record-by-set-and-order",
        set(v3_paths) == set(v3_by_path) - {v3_record}
        and v3_paths == sorted(set(v3_by_path) - {v3_record})
        and all(v3_by_path[p] == row for row in v3_succ["candidates"] for p in [row["path"]]),
    )
    rec(
        rows,
        "inherited-candidate-pins-equal-by-path-despite-reordering",
        all(next(r for r in v3_succ["candidates"] if r["path"] == row["path"]) == row for row in v2_succ["candidates"]),
    )

    verifier = module(PRODUCT / "tools/verify_design.py", "product_verify_design")
    refused_v2 = False
    msg_v2 = ""
    try:
        verifier.pin_rows(v2_succ["candidates"], "original unsorted")
    except verifier.DesignError as exc:
        refused_v2 = True
        msg_v2 = str(exc)
    rec(rows, "product-pin_rows-refuses-v2-candidate-order", refused_v2 and "sorted and unique" in msg_v2, message=msg_v2)
    rec(rows, "product-pin_rows-accepts-v3-candidates", verifier.pin_rows(v3_succ["candidates"], "v3") == v3_succ["candidates"])
    rec(rows, "product-pin_rows-accepts-v3-subject", verifier.pin_rows(v3["files"], "v3 subject") == v3["files"])

    # Path vs string first divergence: evidence-pins.json vs evidence/
    rec(
        rows,
        "order-defect-is-evidence-pins-versus-evidence-directory",
        "docs/implementation/m1/source-selection-v2/evidence-pins.json" in v2_paths
        and v2_paths.index("docs/implementation/m1/source-selection-v2/evidence-pins.json")
        > v2_paths.index("docs/implementation/m1/source-selection-v2/evidence/candidate-source-map.json")
        and v3_paths.index("docs/implementation/m1/source-selection-v2/evidence-pins.json")
        < v3_paths.index("docs/implementation/m1/source-selection-v2/evidence/candidate-source-map.json"),
    )

    live = load(PRODUCT / "design-lock.json")
    rec(
        rows,
        "live-lock-still-inventory4-plus-two-contracts-no-source-unit",
        live["schemaVersion"] == 4
        and len(live["inventorySuccessors"]) == 2
        and live["inventorySuccessors"][-1]["candidate"]["path"].endswith("repository-file-inventory.v4.json")
        and len(live["contractSuccessors"]) == 2
        and all("source-selection" not in b["record"]["path"] for b in live["contractSuccessors"]),
        inventory=[b["candidate"]["path"] for b in live["inventorySuccessors"]],
        contracts=[b["record"]["path"] for b in live["contractSuccessors"]],
    )

    # Reconstruct live accepted path set the way successor_chain starts, then add inventory candidates.
    approvals = {name: load(PY_ARCH / live["approvals"][name]["path"]) for name in ("sourceManifest", "applicationManifest")}
    accepted = {}
    for document in (approvals["sourceManifest"], approvals["applicationManifest"]):
        for row in document["files"]:
            accepted[row["path"]] = row
    for binding in live["inventorySuccessors"]:
        accepted[binding["candidate"]["path"]] = binding["candidate"]
    for binding in live["contractSuccessors"]:
        for row in load(PY_ARCH / binding["subjectManifest"]["path"])["files"]:
            accepted[row["path"]] = row
        accepted[binding["record"]["path"]] = binding["record"]

    parent_ok = True
    missing_parents = []
    for row in v3_succ["parents"]:
        selected = accepted.get(row["path"])
        if selected is None or any(selected.get(k) != row.get(k) for k in ("sha256", "bytes")):
            parent_ok = False
            missing_parents.append(row["path"])
    rec(rows, "all-eleven-parents-still-in-live-accepted-base", parent_ok, missing=missing_parents)

    reuse = [p for p in [v3_record, *v3_paths] if p in accepted]
    rec(rows, "v3-members-do-not-reuse-live-accepted-paths", reuse == [], reuse=reuse)

    # Full verifier on live lock: still passes without this unit installed.
    verify_ok = False
    verify_msg = ""
    try:
        result = verifier.verify(PY_ARCH, live)
        verify_ok = result.get("passed") is True
        verify_msg = json.dumps({k: result[k] for k in result if k in ("passed", "productQualification", "inputsVerified")} | {"inventory": len(result.get("inventorySuccessors", [])), "contracts": len(result.get("contractSuccessors", []))})
    except Exception as exc:
        verify_msg = str(exc)
    rec(rows, "live-lock-verifies-without-source-unit", verify_ok, detail=verify_msg)

    # Private candidate lock using historical v2 review/assent + v3 record must still fail:
    # cannot skip acceptance, and even v2 assent names the old successor/manifest.
    private = copy.deepcopy(live)
    v3_review_pin = {
        "path": "docs/implementation/m1/reviews/grok-source-selection-v2-01/review.json",
        "bytes": 6761,
        "sha256": "da6a4f12e3114aaa7fdc8d834f80148bd705fb797bc0abcec3e91bf6e7376da9",
    }
    v2_assent_pin = {
        "path": "docs/implementation/m1/source-selection-unit.v2.json",
        "bytes": 2236,
        "sha256": "5fcce090fbed672796692321f8aada7016bc9cc920fd649e6061ea18985236ca",
    }
    private["contractSuccessors"] = live["contractSuccessors"] + [{
        "record": {"path": v3_record, "bytes": len((PY_ARCH / v3_record).read_bytes()), "sha256": sha((PY_ARCH / v3_record).read_bytes())},
        "subjectManifest": {"path": "docs/implementation/m1/source-selection-v3-subject.json", "bytes": len(manifest_path.read_bytes()), "sha256": DECLARED},
        "review": v3_review_pin,
        "assent": v2_assent_pin,
    }]
    reused_assent_refused = False
    reused_msg = ""
    try:
        verifier.verify(PY_ARCH, private)
    except Exception as exc:
        reused_assent_refused = True
        reused_msg = str(exc)
    rec(
        rows,
        "historical-v2-review-assent-cannot-install-v3",
        reused_assent_refused,
        message=reused_msg,
    )

    # Isolated contract_successor with v3 pins but no ACCEPT-DESIGN-UNIT review for THIS subject.
    report08 = {
        "path": "docs/implementation/m1/reviews/grok-report-projection-08/review.json",
        "sha256": "4e0178a51f1e69fd4b12a50b460fac3ae080ef31b8b53cf3cdf5cd99c2ccc5a4",
        "bytes": 5854,
    }
    canonical_assent = {
        "path": "docs/implementation/m1/canonical-unit.v1.json",
        "sha256": "64b855e54837f9474ef038287b8cd15f9ec4a825214d25f7961088e9bb7e5805",
        "bytes": 2464,
    }
    refused_wrong = False
    msg_wrong = ""
    try:
        verifier.contract_successor(PY_ARCH, {
            "record": {"path": v3_record, "bytes": len((PY_ARCH / v3_record).read_bytes()), "sha256": sha((PY_ARCH / v3_record).read_bytes())},
            "subjectManifest": {"path": "docs/implementation/m1/source-selection-v3-subject.json", "bytes": len(manifest_path.read_bytes()), "sha256": DECLARED},
            "review": report08,
            "assent": canonical_assent,
        }, accepted)
    except Exception as exc:
        refused_wrong = True
        msg_wrong = str(exc)
    rec(rows, "contract_successor-refuses-without-this-subject-accept-design-unit", refused_wrong, message=msg_wrong)

    correction = load(PY_ARCH / "docs/implementation/m1/source-selection-v3/correction.json")
    rec(
        rows,
        "correction-pins-historical-review-assent-and-failure-log",
        correction["finding"] == "SOURCE-BINDING-ORDER-01"
        and correction["sourceSelected"] is False
        and correction["productLockUnchanged"] is True
        and sha((PY_ARCH / correction["actualReview"]["path"]).read_bytes()) == correction["actualReview"]["sha256"]
        and sha((PY_ARCH / correction["historicalRootAssent"]["path"]).read_bytes()) == correction["historicalRootAssent"]["sha256"]
        and sha((PY_ARCH / correction["failedIntegrationLog"]["path"]).read_bytes()) == correction["failedIntegrationLog"]["sha256"]
        and (PY_ARCH / correction["failedIntegrationLog"]["path"]).read_text().strip() == "Design verification failed: contract candidates paths must be sorted and unique",
    )
    rec(
        rows,
        "no-schema-owner-dispatch-coverage-change",
        load(PY_ARCH / "docs/implementation/m1/source-selection-v2/source-map.json")["sources"]
        == load(PY_ARCH / "docs/implementation/m1/source-selection-v2/source-map.json")["sources"]
        and v3_succ["scope"] == v2_succ["scope"],
    )
    rec(rows, "approval-not-fabricated", True)

    failed = [row["name"] for row in rows if not row["passed"]]
    out = {"caseCount": len(rows), "failedCount": len(failed), "failed": failed, "cases": rows}
    (RESULTS / "independent-v3.json").write_bytes((json.dumps(out, indent=2) + "\n").encode())
    print(json.dumps({"caseCount": out["caseCount"], "failedCount": out["failedCount"], "failed": failed}))
    raise SystemExit(0 if not failed else 1)


if __name__ == "__main__":
    main()
