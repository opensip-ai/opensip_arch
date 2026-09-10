#!/usr/bin/env python3
"""Execution-inputs join checks. Not full Run replay. Does not relabel check-replay.v3.py."""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("execution_inputs_v1", HERE / "execution_inputs_model.v1.py")
M = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(M)

HISTORICAL = (
    "grok-subject-assessment.v7", "grok-subject-assessment.v8",
    "grok-subject-assessment.v9", "grok-subject-assessment.v10",
    "grok-subject-assessment.v11",
)
DEFAULT_SCRATCH = Path("/tmp/opensip-execution-inputs-check-scratch")

HEX = "a" * 64
U1 = "c" * 64
U2 = "d" * 64
PLAN_ID = "plan2:" + "f" * 64
EXEC_ID = "exec-plan2:" + "e" * 64
EVAL = "closure2:" + "0" * 64
PROV = "closure2:" + "1" * 64
SNAP = "snapshot2:" + "b" * 64


def _refuse_historical(path: Path) -> None:
    if set(path.resolve().parts) & set(HISTORICAL):
        raise SystemExit("refusing historical review folder: " + str(path.resolve()))


def output_paths(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--receipt", default=None)
    p.add_argument("--hashes", default=None)
    ns = p.parse_args(argv)
    receipt = Path(ns.receipt) if ns.receipt else DEFAULT_SCRATCH / "check-receipt.json"
    hashes = Path(ns.hashes) if ns.hashes else receipt.with_name("hashes.json")
    _refuse_historical(receipt)
    _refuse_historical(hashes)
    return receipt, hashes


def dgst(obj) -> str:
    return M.raw_digest(obj)


def inv_rec(kind):
    return {"kind": kind, "schemaVersion": 1}


def view_rec(producer=PROV, plan=PLAN_ID):
    return {"planId": plan, "producerClosure": producer, "schemaVersion": 2}


def cov_key(rel, rung, uni=U1):
    return {
        "schemaVersion": 3,
        "key": {
            "relation": rel, "resolution": rung,
            "sourceUniverse": uni, "targetUniverse": uni,
            "subjectScopeCommitment": "sha256:" + "1" * 64,
        },
        "entry": {"coverage": "complete"},
    }


def accounts_for(ci, po, cap, uni, exhaustive=True, vcs_state="not-applicable"):
    pairs = M._matrix_pairs(cap)
    rows = []
    for rel, rung in pairs:
        payload = cov_key(rel, rung, uni)
        digest = dgst(payload)
        state = vcs_state if rel == "vcs-change" else "not-applicable"
        rows.append({
            "cellOrdinal": ci, "programOrdinal": po, "relation": rel, "resolution": rung,
            "sourceUniverse": uni, "targetUniverse": uni, "coverageDigest": digest,
            "coverage": "complete", "resolutionCompletenessState": state,
            "examinedExhaustive": exhaustive,
        })
    return rows, {r["coverageDigest"]: cov_key(r["relation"], r["resolution"], uni) for r in rows}


def candidate_result(*, state="complete", groups=None, examined=None, required_fields=True):
    rec = {
        "schemaVersion": 1, "planId": PLAN_ID, "executionPlanId": EXEC_ID,
        "cellOrdinal": 0, "programOrdinal": 0, "capabilityId": "clones-near",
        "universe": U1, "producerClosure": PROV, "state": state,
        "deficiency": None if state == "complete" else "provider-unavailable",
        "nativeCause": None, "authority": "candidate-only",
        "semanticEquivalenceClaimed": False, "automaticDeletionEligible": False,
        "examinedPaths": examined if examined is not None else ["src/a.ts"],
        "groupDigests": groups if groups is not None else [],
    }
    return rec


def base_inventory_graph(uni=U1, extra_cells=None):
    spec = {"requestedCapabilities": [
        {"capabilityId": "inventory", "languageMode": "syntax-only", "workspaceRoot": ".", "required": True}
    ]}
    kinds = M._cap_kinds("inventory")
    file_inv, pkg_inv = inv_rec("file"), inv_rec("package")
    fd, pd = dgst(file_inv), dgst(pkg_inv)
    view = view_rec()
    # locator key for view (H suffix stand-in; this unit does not re-hash view2)
    vd = "2" * 64
    acc, cov_map = accounts_for(0, 0, "inventory", uni)
    stage_spec = {"schemaVersion": 2, "planId": PLAN_ID, "producerClosure": PROV,
                  "operation": "derive-inventory-view", "parameters": [],
                  "outputDomains": ["view"], "outputSchemaDigest": HEX}
    sd = dgst(stage_spec)
    enum = {"schemaVersion": 1, "snapshotId": SNAP, "scopeDigest": HEX, "membershipDigest": HEX,
            "cells": [{"capabilityId": "inventory", "languageMode": "syntax-only", "workspaceRoot": ".",
                       "required": True, "kinds": kinds,
                       "programBindings": [{"ordinal": 0, "provenance": "default-unit",
                                            "enumerator": {"status": "selected", "closureId": PROV},
                                            "nativeContextDigest": HEX, "universe": uni,
                                            "programEntry": None, "extents": []}]}]}
    if extra_cells:
        spec["requestedCapabilities"].extend(extra_cells[0])
        enum["cells"].extend(extra_cells[1])
    exec_plan = {"schemaVersion": 2, "planId": PLAN_ID,
                 "stages": [{"ordinal": 0, "stageSpecDigest": sd, "requires": [], "outputDomains": ["view"]}]}
    outcome = {
        "ordinal": 0, "cellOrdinal": 0, "programOrdinal": 0, "capabilityId": "inventory",
        "languageMode": "syntax-only", "workspaceRoot": ".", "required": True, "kinds": kinds,
        "universe": uni, "enumeratorStatus": "selected", "state": "complete",
        "deficiency": None, "nativeCause": None, "stageOrdinal": 0,
        "inventoryDigests": M.canon_str_list([fd, pd]), "viewDigests": [vd],
        "candidateResultDigest": None,
    }
    selected = [
        {"domain": "view", "digest": vd},
        {"domain": "subject-inventory", "digest": fd},
        {"domain": "subject-inventory", "digest": pd},
    ]
    for a in acc:
        selected.append({"domain": "coverage", "digest": a["coverageDigest"]})
    selected = sorted({M.C.canonical(x): x for x in selected}.values(), key=M.C.canonical)
    retained = M.canon_str_list([r["digest"] for r in selected])
    plan = {"planId": PLAN_ID, "snapshotId": SNAP, "analysisSpecDigest": dgst(spec),
            "semanticClosures": [EVAL, PROV], "importIds": []}
    manifest = {
        "schemaVersion": 1, "planId": PLAN_ID, "executionPlanId": EXEC_ID,
        "evaluatorClosure": EVAL, "enumerationPlanDigest": dgst(enum),
        "analysisSpecDigest": dgst(spec),
        "hostCapture": {"custody": "host-tcb-evidence-store", "observation": "stage-return",
                        "retainedDigests": retained},
        "selectedRefs": selected, "cellOutcomes": [outcome],
        "nativeCoverageAccounts": acc, "candidateResultRefs": [],
    }
    blobs = {fd: M.C.canonical(file_inv), pd: M.C.canonical(pkg_inv)}
    for cdigest, payload in cov_map.items():
        blobs[cdigest] = M.C.canonical(payload)
    return {
        "plan": plan, "execution_plan": exec_plan, "execution_plan_id": EXEC_ID,
        "stage_specs": {sd: stage_spec}, "enumeration_plan": enum, "analysis_spec": spec,
        "execution_inputs": manifest, "inventories": {fd: file_inv, pd: pkg_inv},
        "views": {vd: view}, "coverages": cov_map, "candidate_results": {},
        "retained_blobs": blobs, "closures": {EVAL: {"kind": "evaluator"}, PROV: {"kind": "provider"}},
        "vcs_observation": {"kind": "none"},
    }


def admit(g, **over):
    kw = dict(g)
    kw.update(over)
    return M.admit_execution_inputs(**kw)


def owned_hashes():
    names = [
        "execution-inputs.schema.v1.json", "execution-inputs-contract.v1.md",
        "execution_inputs_model.v1.py", "check-execution-inputs.v1.py",
    ]
    rows = []
    for n in names:
        raw = (HERE / n).read_bytes()
        rows.append({"path": str(HERE / n), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()})
    return rows


def main(argv=None):
    OUT, HASHES = output_paths(argv)
    cases = []

    def rec(name, result):
        cases.append({"case": name, "result": result["result"], "refusals": result.get("refusals")})

    g = base_inventory_graph()
    rec("positive-required-inventory-complete-empty-vcs-none", admit(g))

    rec("all-rules-disabled-still-owes-native-coverage", admit(g))  # no policy document; native accounts remain

    missing = copy.deepcopy(g)
    missing["execution_inputs"]["nativeCoverageAccounts"] = [
        a for a in missing["execution_inputs"]["nativeCoverageAccounts"] if a["relation"] != "file"
    ]
    rec("missing-file-coverage-account-refused", admit(missing))

    # required clones-near without candidate envelope
    extra_spec = [{"capabilityId": "clones-near", "languageMode": "syntax-only", "workspaceRoot": ".", "required": True}]
    extra_cell = [{"capabilityId": "clones-near", "languageMode": "syntax-only", "workspaceRoot": ".",
                   "required": True, "kinds": [],
                   "programBindings": [{"ordinal": 0, "provenance": "default-unit",
                                        "enumerator": {"status": "selected", "closureId": PROV},
                                        "nativeContextDigest": HEX, "universe": U1,
                                        "programEntry": None, "extents": []}]}]
    # cell order: clones-near then inventory (utf8 cap id)
    g2spec = {"requestedCapabilities": extra_spec + g["analysis_spec"]["requestedCapabilities"]}
    g2enum = copy.deepcopy(g["enumeration_plan"])
    g2enum["cells"] = extra_cell + g2enum["cells"]
    g2 = copy.deepcopy(g)
    g2["analysis_spec"] = g2spec
    g2["enumeration_plan"] = g2enum
    g2["plan"]["analysisSpecDigest"] = dgst(g2spec)
    near_out = {
        "ordinal": 0, "cellOrdinal": 0, "programOrdinal": 0, "capabilityId": "clones-near",
        "languageMode": "syntax-only", "workspaceRoot": ".", "required": True, "kinds": [],
        "universe": U1, "enumeratorStatus": "selected", "state": "complete",
        "deficiency": None, "nativeCause": None, "stageOrdinal": None,
        "inventoryDigests": [], "viewDigests": [], "candidateResultDigest": None,
    }
    inv_out = copy.deepcopy(g["execution_inputs"]["cellOutcomes"][0])
    inv_out["ordinal"] = 1
    inv_out["cellOrdinal"] = 1
    g2["execution_inputs"]["cellOutcomes"] = [near_out, inv_out]
    for a in g2["execution_inputs"]["nativeCoverageAccounts"]:
        a["cellOrdinal"] = 1
    g2["execution_inputs"]["enumerationPlanDigest"] = dgst(g2enum)
    g2["execution_inputs"]["analysisSpecDigest"] = dgst(g2spec)
    rec("required-empty-kind-missing-candidate-refused", admit(g2))

    cand = candidate_result()
    cd = dgst(cand)
    g3 = copy.deepcopy(g2)
    g3["execution_inputs"]["cellOutcomes"][0]["candidateResultDigest"] = cd
    g3["execution_inputs"]["candidateResultRefs"] = [cd]
    g3["candidate_results"] = {cd: cand}
    g3["retained_blobs"] = dict(g3["retained_blobs"])
    g3["retained_blobs"][cd] = M.C.canonical(cand)
    g3["execution_inputs"]["hostCapture"]["retainedDigests"] = M.canon_str_list(
        g3["execution_inputs"]["hostCapture"]["retainedDigests"] + [cd])
    rec("required-empty-kind-zero-candidate-complete", admit(g3))

    g4 = copy.deepcopy(g3)
    g4["execution_inputs"]["cellOutcomes"][0]["candidateResultDigest"] = None
    g4["execution_inputs"]["candidateResultRefs"] = []
    rec("required-empty-kind-complete-without-envelope-refused", admit(g4))

    opt_spec = [{"capabilityId": "clones-near", "languageMode": "syntax-only", "workspaceRoot": ".", "required": False}]
    opt_cell = [dict(extra_cell[0], required=False,
                     programBindings=[dict(extra_cell[0]["programBindings"][0], universe=None,
                                           enumerator={"status": "unselected", "reason": "optional-unselected"})])]
    go = copy.deepcopy(g)
    go["analysis_spec"] = {"requestedCapabilities": opt_spec + go["analysis_spec"]["requestedCapabilities"]}
    go["enumeration_plan"] = copy.deepcopy(g["enumeration_plan"])
    go["enumeration_plan"]["cells"] = opt_cell + go["enumeration_plan"]["cells"]
    go["plan"]["analysisSpecDigest"] = dgst(go["analysis_spec"])
    opt_out = {
        "ordinal": 0, "cellOrdinal": 0, "programOrdinal": 0, "capabilityId": "clones-near",
        "languageMode": "syntax-only", "workspaceRoot": ".", "required": False, "kinds": [],
        "universe": None, "enumeratorStatus": "unselected", "state": "unavailable",
        "deficiency": "provider-unavailable", "nativeCause": None, "stageOrdinal": None,
        "inventoryDigests": [], "viewDigests": [], "candidateResultDigest": None,
    }
    inv_out = copy.deepcopy(g["execution_inputs"]["cellOutcomes"][0])
    inv_out["ordinal"] = 1
    inv_out["cellOrdinal"] = 1
    go["execution_inputs"]["cellOutcomes"] = [opt_out, inv_out]
    for a in go["execution_inputs"]["nativeCoverageAccounts"]:
        a["cellOrdinal"] = 1
    go["execution_inputs"]["enumerationPlanDigest"] = dgst(go["enumeration_plan"])
    go["execution_inputs"]["analysisSpecDigest"] = dgst(go["analysis_spec"])
    rec("optional-empty-kind-unselected-unavailable", admit(go))

    omit = copy.deepcopy(g)
    omit["execution_inputs"]["selectedRefs"] = [
        r for r in omit["execution_inputs"]["selectedRefs"] if r["domain"] != "view"
    ]
    rec("omitted-returned-view-refused", admit(omit))

    ptr = copy.deepcopy(g)
    ghost = "3" * 64
    ptr["execution_inputs"]["selectedRefs"] = sorted(
        {M.C.canonical(x): x for x in ptr["execution_inputs"]["selectedRefs"] + [
            {"domain": "view", "digest": ghost}
        ]}.values(), key=M.C.canonical)
    rec("missing-view-pointer-refused", admit(
        ptr, store_pointers=list(ptr["execution_inputs"]["hostCapture"]["retainedDigests"])))

    lost = copy.deepcopy(g)
    vd = next(r["digest"] for r in lost["execution_inputs"]["selectedRefs"] if r["domain"] == "view")
    rec("lost-view-bytes-refused", admit(lost, store_pointers=list(lost["execution_inputs"]["hostCapture"]["retainedDigests"]),
                                         retained_blobs={}))

    badb = copy.deepcopy(g)
    fd = next(r["digest"] for r in badb["execution_inputs"]["selectedRefs"] if r["domain"] == "subject-inventory")
    blobs = dict(badb["retained_blobs"])
    blobs[fd] = b"not-the-inventory-bytes"
    rec("invalid-supplied-inventory-bytes-refused", admit(badb, retained_blobs=blobs))

    two = copy.deepcopy(g)
    b1 = copy.deepcopy(two["enumeration_plan"]["cells"][0]["programBindings"][0])
    b1["ordinal"] = 1
    b1["provenance"] = "explicit-plan-selection"
    b1["universe"] = U2
    two["enumeration_plan"]["cells"][0]["programBindings"].append(b1)
    two["execution_inputs"]["enumerationPlanDigest"] = dgst(two["enumeration_plan"])
    acc2, cov2 = accounts_for(0, 1, "inventory", U2)
    two["coverages"].update(cov2)
    for cdigest, payload in cov2.items():
        two["retained_blobs"][cdigest] = M.C.canonical(payload)
    vd2 = "4" * 64
    two["views"][vd2] = view_rec()
    out1 = copy.deepcopy(two["execution_inputs"]["cellOutcomes"][0])
    out2 = copy.deepcopy(out1)
    out2["ordinal"] = 1
    out2["programOrdinal"] = 1
    out2["universe"] = U2
    out2["viewDigests"] = [vd2]
    acc1 = two["execution_inputs"]["nativeCoverageAccounts"]
    two["execution_inputs"]["cellOutcomes"] = [out1, out2]
    two["execution_inputs"]["nativeCoverageAccounts"] = acc1 + acc2
    extra_refs = [{"domain": "view", "digest": vd2}] + [{"domain": "coverage", "digest": a["coverageDigest"]} for a in acc2]
    two["execution_inputs"]["selectedRefs"] = sorted(
        {M.C.canonical(x): x for x in two["execution_inputs"]["selectedRefs"] + extra_refs}.values(),
        key=M.C.canonical)
    two["execution_inputs"]["hostCapture"]["retainedDigests"] = M.canon_str_list(
        [r["digest"] for r in two["execution_inputs"]["selectedRefs"]])
    rec("two-universes-two-outcomes", admit(two))

    wrong = copy.deepcopy(g)
    vd = next(iter(wrong["views"]))
    wrong["views"][vd] = view_rec(producer="closure2:" + "9" * 64)
    rec("stage-producer-wrong-join-refused", admit(wrong))

    badm = copy.deepcopy(g["execution_inputs"])
    badm["verdict"] = "pass"
    rec("schema-rejects-verdict-field", M.admit_execution_inputs(
        **{**g, "execution_inputs": badm}))

    autofix = candidate_result()
    autofix["automaticDeletionEligible"] = True
    try:
        M.C.validate({"$defs": M.SCHEMA["$defs"], "allOf": [{"$ref": "#/$defs/CandidateProducerResultV1"}]}, autofix)
        rec("schema-rejects-candidate-autofix", {"result": "ADMIT", "refusals": []})
    except Exception:
        rec("schema-rejects-candidate-autofix", {"result": "REFUSE", "refusals": ["EXECUTION_INPUTS_SCHEMA"]})

    unav = copy.deepcopy(g)
    unav["execution_inputs"]["cellOutcomes"][0]["state"] = "unavailable"
    unav["execution_inputs"]["cellOutcomes"][0]["deficiency"] = "provider-unavailable"
    unav["execution_inputs"]["cellOutcomes"][0]["universe"] = None
    unav["enumeration_plan"]["cells"][0]["programBindings"][0]["universe"] = None
    unav["execution_inputs"]["enumerationPlanDigest"] = dgst(unav["enumeration_plan"])
    for a in unav["execution_inputs"]["nativeCoverageAccounts"]:
        a["coverage"] = "unknown"
        a["sourceUniverse"] = None
        a["targetUniverse"] = None
        a["coverageDigest"] = None
    rec("unavailable-inventory-not-complete-empty", admit(unav))

    want = {
        "positive-required-inventory-complete-empty-vcs-none": "ADMIT",
        "all-rules-disabled-still-owes-native-coverage": "ADMIT",
        "missing-file-coverage-account-refused": "REFUSE",
        "required-empty-kind-missing-candidate-refused": "REFUSE",
        "required-empty-kind-zero-candidate-complete": "ADMIT",
        "required-empty-kind-complete-without-envelope-refused": "REFUSE",
        "optional-empty-kind-unselected-unavailable": "ADMIT",
        "omitted-returned-view-refused": "REFUSE",
        "missing-view-pointer-refused": "REFUSE",
        "lost-view-bytes-refused": "REFUSE",
        "invalid-supplied-inventory-bytes-refused": "REFUSE",
        "two-universes-two-outcomes": "ADMIT",
        "stage-producer-wrong-join-refused": "REFUSE",
        "schema-rejects-verdict-field": "REFUSE",
        "schema-rejects-candidate-autofix": "REFUSE",
        "unavailable-inventory-not-complete-empty": "ADMIT",
    }
    mismatches = []
    for c in cases:
        exp = want.get(c["case"])
        if exp and c["result"] != exp:
            mismatches.append({"case": c["case"], "got": c["result"], "want": exp, "refusals": c.get("refusals")})
    hashes = owned_hashes()
    report = {
        "standing": "execution-inputs join checks; not a Run; does not cover or replace check-replay.v3.py 25 checks.",
        "noCoveringProgramQualification": "unavailable inventory is already incomplete and cannot be complete-empty; incomplete-inventory instead of no-covering-program is not a false pass.",
        "cases": cases, "expected": want, "mismatches": mismatches, "ownedHashes": hashes,
        "internalFaults": list(M.INTERNAL_FAULTS),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2) + "\n")
    HASHES.write_text(json.dumps(hashes, indent=2) + "\n")
    print(json.dumps({"n": len(cases), "mismatches": mismatches, "receiptPath": str(OUT)}, indent=2))
    for c in cases:
        print(c["case"], c["result"], c.get("refusals"))
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
