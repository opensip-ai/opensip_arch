#!/usr/bin/env python3
"""Execution-inputs join checks against owner-admitted fixture graphs where feasible.

Not a Run. Does not overwrite grok-execution-inputs.v1 or historical review folders.
Default: print JSON to stdout. Optional --receipt PATH for a new report.
"""
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
_fspec = importlib.util.spec_from_file_location("exec_in_fixture3", HERE / "evaluator_graph_fixture.v3.py")
F = importlib.util.module_from_spec(_fspec)
_fspec.loader.exec_module(F)

PINNED_V1 = "grok-execution-inputs.v1"
HISTORICAL = (
    "grok-subject-assessment.v7", "grok-subject-assessment.v8",
    "grok-subject-assessment.v9", "grok-subject-assessment.v10",
    "grok-subject-assessment.v11", PINNED_V1,
)


def _refuse_historical(path: Path) -> None:
    if set(path.resolve().parts) & set(HISTORICAL):
        raise SystemExit("refusing historical/pinned review folder: " + str(path.resolve()))


def output_paths(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--receipt", default=None)
    p.add_argument("--hashes", default=None)
    ns = p.parse_args(argv)
    receipt = Path(ns.receipt) if ns.receipt else None
    hashes = Path(ns.hashes) if ns.hashes else (receipt.with_name("hashes.json") if receipt else None)
    if receipt:
        _refuse_historical(receipt)
    if hashes:
        _refuse_historical(hashes)
    return receipt, hashes


def hx(prefixed: str) -> str:
    return prefixed.split(":", 1)[1]


def canon_refs(refs):
    return sorted({M.C.canonical(x): x for x in refs}.values(), key=M.C.canonical)


def pointers_of(objects, blobs):
    return list(objects.keys()) + list(blobs.keys())


def payload_of(graph, coverage_id):
    env = graph["objects"][coverage_id][1]
    return M.C.parse(graph["blobs"][env["payloadDigest"]])


def manifest_from_owner(graph):
    objects, blobs = graph["objects"], graph["blobs"]
    plan_id = graph["inputs"]["planId"]
    plan = objects[plan_id][1]
    exec_id = graph["inputs"]["executionPlanId"]
    exec_plan = objects[exec_id][1]
    enum = graph["enumerationPlan"]
    spec = M.C.parse(blobs[plan["analysisSpecDigest"]])
    vcs = M.C.parse(blobs[graph["snapshot"]["vcsDigest"]])
    inventories = {d: inv for d, inv in graph["inventoryResults"]}
    closures = {k: v for k, (dom, v) in objects.items() if dom == "closure"}
    stage_d = exec_plan["stages"][0]["stageSpecDigest"]
    stage_spec = M.C.parse(blobs[stage_d])
    view_ids = list(graph["viewIds"])
    outcomes = []
    accounts = []
    ordinal = 0
    view_hexes_all = []
    cov_hexes_all = []
    for ci, cell in enumerate(enum["cells"]):
        for b in cell["programBindings"]:
            po = b["ordinal"]
            uni = b.get("universe")
            kinds = cell["kinds"]
            inv_ds = M.canon_str_list(
                [d for d, inv in graph["inventoryResults"]
                 if inv["cellOrdinal"] == ci and inv["programOrdinal"] == po]
            )
            bound_views, bound_cov, bound_scopes = [], [], []
            for vid in view_ids:
                view = objects[vid][1]
                for sid in view["scopeIds"]:
                    sc = objects[sid][1]
                    if sc.get("sourceUniverse") == uni:
                        bound_views.append(hx(vid))
                        bound_cov.extend(hx(c) for c in view["coverageIds"])
                        bound_scopes.append(sid)
                        break
            view_hexes_all.extend(bound_views)
            cov_hexes_all.extend(bound_cov)
            en = b.get("enumerator") or {}
            outcomes.append({
                "ordinal": ordinal, "cellOrdinal": ci, "programOrdinal": po,
                "capabilityId": cell["capabilityId"], "languageMode": cell["languageMode"],
                "workspaceRoot": cell["workspaceRoot"], "required": cell["required"],
                "kinds": kinds, "universe": uni, "enumeratorStatus": en.get("status"),
                "enumeratorClosure": en.get("closureId"), "state": "complete",
                "deficiency": None, "nativeCause": None, "stageOrdinal": 0,
                "stageOrdinalNullReason": None, "inventoryDigests": inv_ds,
                "viewDigests": M.canon_str_list(bound_views), "candidateResultDigest": None,
            })
            ordinal += 1
            for rel, rung in M._matrix_pairs(cell["capabilityId"]):
                if rel == "vcs-change" and vcs.get("kind") == "none":
                    accounts.append({
                        "cellOrdinal": ci, "programOrdinal": po, "relation": rel, "resolution": rung,
                        "sourceUniverse": uni, "targetUniverse": uni, "accountState": "inapplicable",
                        "deficiency": None, "nativeCause": None, "coverageIds": [], "scopeIds": [],
                        "coverage": None, "resolutionCompletenessState": None, "examinedExhaustive": None,
                    })
                    continue
                matched = []
                for cid in bound_cov:
                    full = "coverage2:" + cid
                    if full not in objects:
                        continue
                    pay = payload_of(graph, full)
                    key = pay.get("key") or {}
                    if key.get("relation") == rel and key.get("resolution") == rung and key.get("sourceUniverse") == uni:
                        matched.append((cid, objects[full][1], pay))
                if matched:
                    _cid, env, pay = matched[0]
                    entry = pay["entry"]
                    rc = entry.get("resolutionCompleteness") or {}
                    accounts.append({
                        "cellOrdinal": ci, "programOrdinal": po, "relation": rel, "resolution": rung,
                        "sourceUniverse": uni, "targetUniverse": uni, "accountState": "complete",
                        "deficiency": entry.get("deficiency"), "nativeCause": entry.get("nativeCause"),
                        "coverageIds": M.canon_str_list([m[0] for m in matched]),
                        "scopeIds": M.canon_str_list([m[1]["scopeId"] for m in matched]),
                        "coverage": entry.get("coverage"),
                        "resolutionCompletenessState": rc.get("state"),
                        "examinedExhaustive": rc.get("examinedExhaustive"),
                    })
                else:
                    accounts.append({
                        "cellOrdinal": ci, "programOrdinal": po, "relation": rel, "resolution": rung,
                        "sourceUniverse": uni, "targetUniverse": uni, "accountState": "incomplete",
                        "deficiency": "provider-unavailable", "nativeCause": None,
                        "coverageIds": [], "scopeIds": [], "coverage": "unknown",
                        "resolutionCompletenessState": None, "examinedExhaustive": None,
                    })
    selected = []
    for vid in view_ids:
        selected.append({"domain": "view", "digest": hx(vid)})
    for d, inv in graph["inventoryResults"]:
        selected.append({"domain": "subject-inventory", "digest": d})
    for cid in graph["coverageIds"]:
        selected.append({"domain": "coverage", "digest": hx(cid)})
    for iid in plan.get("importIds") or []:
        selected.append({"domain": "import", "digest": hx(iid)})
    selected = canon_refs(selected)
    output_refs = [r for r in selected if r["domain"] in ("view", "coverage", "import")]
    receipts = [{
        "ordinal": 0, "stageSpecDigest": stage_d, "producerClosure": stage_spec["producerClosure"],
        "outputRefs": canon_refs(output_refs),
    }]
    manifest = {
        "schemaVersion": 1, "planId": plan_id, "executionPlanId": exec_id,
        "evaluatorClosure": graph["inputs"]["evaluatorClosure"],
        "enumerationPlanDigest": M.raw_digest(enum),
        "analysisSpecDigest": plan["analysisSpecDigest"],
        "hostCapture": {
            "custody": "host-tcb-evidence-store", "observation": "stage-return",
            "stageReceipts": receipts,
            "retainedObjectKeys": sorted(objects),
            "retainedBlobDigests": M.canon_str_list(list(blobs)),
        },
        "selectedRefs": selected, "cellOutcomes": outcomes,
        "nativeCoverageAccounts": accounts, "candidateResultRefs": [],
    }
    return {
        "plan_id": plan_id, "plan": plan, "execution_plan_id": exec_id, "execution_plan": exec_plan,
        "enumeration_plan": enum, "analysis_spec": spec, "execution_inputs": manifest,
        "objects": objects, "blobs": blobs, "store_pointers": pointers_of(objects, blobs),
        "inventories": inventories, "imports": {hx(i): objects[i][1] for i in plan.get("importIds") or []},
        "target_attributions": {}, "incoming_searches": {}, "candidate_results": {}, "groups": {},
        "closures": closures, "stage_specs": {stage_d: stage_spec}, "vcs_observation": vcs,
    }


def admit(kw):
    return M.admit_execution_inputs(**kw)


def owned_hashes():
    names = [
        "execution-inputs.schema.v1.json", "execution-inputs-contract.v1.md",
        "execution_inputs_model.v1.py", "check-execution-inputs.v1.py",
    ]
    return [{"path": str(HERE / n), "bytes": len((HERE / n).read_bytes()),
             "sha256": hashlib.sha256((HERE / n).read_bytes()).hexdigest()} for n in names]


def main(argv=None):
    receipt_path, hashes_path = output_paths(argv)
    cases = []

    def rec(name, result):
        cases.append({
            "case": name, "result": result.get("result"),
            "refusals": result.get("refusals"),
            "deficiencyCauses": [d.get("cause") for d in result.get("requiredCellDeficiencies") or []],
            "deficiencyRelations": [d.get("relation") for d in result.get("requiredCellDeficiencies") or []],
        })

    graph = F.build_file_inputs()
    owner = manifest_from_owner(graph)
    rec("owner-graph-file-positive", admit(owner))

    two = manifest_from_owner(F.build_file_inputs(multiple_universes=True))
    rec("owner-graph-two-universes", admit(two))

    # false complete: package pair claimed complete with no envelopes
    fake = copy.deepcopy(owner)
    for a in fake["execution_inputs"]["nativeCoverageAccounts"]:
        if a["relation"] == "package":
            a["accountState"] = "complete"
            a["coverage"] = "complete"
            a["deficiency"] = None
            a["coverageIds"] = []
    rec("false-complete-without-coverage-envelope", admit(fake))

    derive = copy.deepcopy(owner)
    for a in derive["execution_inputs"]["nativeCoverageAccounts"]:
        if a["accountState"] == "complete":
            a["coverage"] = "unknown"
            break
    rec("self-asserted-coverage-mismatch-owner-entry", admit(derive))

    drop = copy.deepcopy(owner)
    drop["execution_inputs"]["selectedRefs"] = [
        r for r in drop["execution_inputs"]["selectedRefs"] if r["domain"] != "view"
    ]
    rec("omitted-owner-view", admit(drop))

    ptr = copy.deepcopy(owner)
    inv_d = next(iter(ptr["inventories"]))
    ptr["store_pointers"] = [p for p in ptr["store_pointers"] if p != inv_d]
    rec("missing-inventory-pointer", admit(ptr))

    lost = copy.deepcopy(owner)
    inv_d = next(iter(lost["inventories"]))
    blobs = dict(lost["blobs"])
    blobs.pop(inv_d, None)
    rec("lost-inventory-bytes", admit({**lost, "blobs": blobs}))

    mismatch = copy.deepcopy(owner)
    inv_d = next(iter(mismatch["inventories"]))
    invs = dict(mismatch["inventories"])
    invs[inv_d] = {**invs[inv_d], "kind": "symbol"}
    rec("supplied-object-mismatch-not-pointer", admit({**mismatch, "inventories": invs}))

    badhash = copy.deepcopy(owner)
    inv_d = next(iter(badhash["inventories"]))
    blobs = dict(badhash["blobs"])
    blobs[inv_d] = b'{"kind":"not-the-inventory"}'
    rec("invalid-blob-hash", admit({**badhash, "blobs": blobs}))

    exh = copy.deepcopy(owner)
    for a in exh["execution_inputs"]["nativeCoverageAccounts"]:
        if a["accountState"] == "complete":
            a["examinedExhaustive"] = (not a["examinedExhaustive"]) if a["examinedExhaustive"] is not None else True
            break
    rec("derived-examined-exhaustive-mismatch", admit(exh))

    dup = copy.deepcopy(owner)
    row = dup["execution_inputs"]["cellOutcomes"][0]
    if len(row["inventoryDigests"]) >= 1:
        row["inventoryDigests"] = [row["inventoryDigests"][0], row["inventoryDigests"][0]]
    rec("duplicate-inventory-same-kind", admit(dup))

    prod = copy.deepcopy(owner)
    vid = next(r["digest"] for r in prod["execution_inputs"]["selectedRefs"] if r["domain"] == "view")
    key = "view2:" + vid
    rec_view = copy.deepcopy(prod["objects"][key][1])
    rec_view["producerClosure"] = "closure2:" + "9" * 64
    objects = dict(prod["objects"])
    objects[key] = ("view", rec_view)
    rec("wrong-view-producer-vs-stage", admit({**prod, "objects": objects}))

    rec("store-pointers-required", M.admit_execution_inputs(
        **{k: v for k, v in owner.items() if k != "store_pointers"}, store_pointers=None))

    vcs_lie = copy.deepcopy(owner)
    for a in vcs_lie["execution_inputs"]["nativeCoverageAccounts"]:
        if a["relation"] == "vcs-change":
            a["accountState"] = "complete"
            a["coverage"] = "complete"
            a["coverageIds"] = [hx(graph["coverageId"])]
            a["resolutionCompletenessState"] = "not-applicable"
    rec("vcs-none-not-applicable-alone", admit(vcs_lie))

    # optional unselected candidate-only (synthetic bindings on a copies enum would break digest;
    # construct a clones-near-only graph using owner store plus extra enum is out of scope).
    # Required candidate pointer missing: add a clones-near cell would desync spec.
    # Exercise candidate schema + group join on a clones-near-only synthetic store.
    cand = {
        "schemaVersion": 1, "planId": owner["plan_id"], "executionPlanId": owner["execution_plan_id"],
        "cellOrdinal": 0, "programOrdinal": 0, "capabilityId": "clones-near",
        "languageMode": "syntax-only", "universe": None, "producerClosure": graph["inputs"]["evaluatorClosure"],
        "stageOrdinal": None, "state": "unavailable", "deficiency": "provider-unavailable",
        "nativeCause": None, "authority": "candidate-only", "semanticEquivalenceClaimed": False,
        "automaticDeletionEligible": False, "examinedPaths": [], "groupDigests": [],
    }
    try:
        M.C.validate({"$defs": M.SCHEMA["$defs"], "allOf": [{"$ref": "#/$defs/CandidateProducerResultV1"}]}, cand)
        rec("candidate-unavailable-envelope-schema", {"result": "ADMIT", "refusals": []})
    except Exception as exc:
        rec("candidate-unavailable-envelope-schema", {"result": "REFUSE", "refusals": [str(exc)]})

    autofix = dict(cand, state="complete", deficiency=None, universe="c" * 64, stageOrdinal=0,
                   automaticDeletionEligible=True, examinedPaths=["src/index.ts"])
    try:
        M.C.validate({"$defs": M.SCHEMA["$defs"], "allOf": [{"$ref": "#/$defs/CandidateProducerResultV1"}]}, autofix)
        rec("schema-rejects-candidate-autofix", {"result": "ADMIT", "refusals": []})
    except Exception:
        rec("schema-rejects-candidate-autofix", {"result": "REFUSE", "refusals": ["EXECUTION_INPUTS_SCHEMA"]})

    group = {
        "mode": "near", "evidenceLevel": "similar-candidate", "language": "typescript",
        "members": ["src/index.ts"], "authority": "candidate-only",
        "matchedEdges": [{"left": "src/index.ts", "right": "src/index.ts", "similarityMillionths": 900000}],
        "grouping": "connected-component", "scoreMeaning": "minimum-member-best-neighbor",
        "semanticEquivalenceClaimed": False, "automaticDeletionEligible": False,
    }
    gd = M.raw_digest(group)
    uni = "c" * 64
    prov = next(k for k, v in owner["closures"].items() if v.get("kind") == "provider")
    near_spec = {"requestedCapabilities": [
        {"capabilityId": "clones-near", "languageMode": "syntax-only", "workspaceRoot": ".", "required": True}]}
    near_enum = {"schemaVersion": 1, "snapshotId": owner["plan"]["snapshotId"],
                 "scopeDigest": owner["plan"]["scopeDigest"], "membershipDigest": "1" * 64,
                 "cells": [{"capabilityId": "clones-near", "languageMode": "syntax-only", "workspaceRoot": ".",
                            "required": True, "kinds": [],
                            "programBindings": [{"ordinal": 0, "provenance": "default-unit",
                                                 "enumerator": {"status": "selected", "closureId": prov},
                                                 "nativeContextDigest": "b" * 64, "universe": uni,
                                                 "programEntry": None, "extents": []}]}]}
    env = {
        "schemaVersion": 1, "planId": owner["plan_id"], "executionPlanId": owner["execution_plan_id"],
        "cellOrdinal": 0, "programOrdinal": 0, "capabilityId": "clones-near", "languageMode": "syntax-only",
        "universe": uni, "producerClosure": prov, "stageOrdinal": 0, "state": "complete",
        "deficiency": None, "nativeCause": None, "authority": "candidate-only",
        "semanticEquivalenceClaimed": False, "automaticDeletionEligible": False,
        "examinedPaths": ["src/index.ts"], "groupDigests": [gd],
    }
    ed = M.raw_digest(env)
    near_plan = dict(owner["plan"])
    near_plan["analysisSpecDigest"] = M.raw_digest(near_spec)
    near_outcome = {
        "ordinal": 0, "cellOrdinal": 0, "programOrdinal": 0, "capabilityId": "clones-near",
        "languageMode": "syntax-only", "workspaceRoot": ".", "required": True, "kinds": [],
        "universe": uni, "enumeratorStatus": "selected", "enumeratorClosure": prov, "state": "complete",
        "deficiency": None, "nativeCause": None, "stageOrdinal": 0, "stageOrdinalNullReason": None,
        "inventoryDigests": [], "viewDigests": [], "candidateResultDigest": ed,
    }
    stage_d = owner["execution_plan"]["stages"][0]["stageSpecDigest"]
    near_manifest = {
        "schemaVersion": 1, "planId": owner["plan_id"], "executionPlanId": owner["execution_plan_id"],
        "evaluatorClosure": owner["execution_inputs"]["evaluatorClosure"],
        "enumerationPlanDigest": M.raw_digest(near_enum), "analysisSpecDigest": near_plan["analysisSpecDigest"],
        "hostCapture": {
            "custody": "host-tcb-evidence-store", "observation": "stage-return",
            "stageReceipts": [{"ordinal": 0, "stageSpecDigest": stage_d,
                               "producerClosure": owner["stage_specs"][stage_d]["producerClosure"],
                               "outputRefs": []}],
            "retainedObjectKeys": sorted(owner["objects"]),
            "retainedBlobDigests": M.canon_str_list(list(owner["blobs"]) + [gd, ed]),
        },
        "selectedRefs": [{"domain": "candidate-producer-result", "digest": ed}],
        "cellOutcomes": [near_outcome], "nativeCoverageAccounts": [], "candidateResultRefs": [ed],
    }
    near_blobs = dict(owner["blobs"])
    near_blobs[gd] = M.C.canonical(group)
    near_blobs[ed] = M.C.canonical(env)
    rec("required-candidate-group-bytes-join", admit({
        "plan_id": owner["plan_id"], "plan": near_plan, "execution_plan_id": owner["execution_plan_id"],
        "execution_plan": owner["execution_plan"], "enumeration_plan": near_enum, "analysis_spec": near_spec,
        "execution_inputs": near_manifest, "objects": owner["objects"], "blobs": near_blobs,
        "store_pointers": pointers_of(owner["objects"], near_blobs), "inventories": {},
        "imports": {}, "target_attributions": {}, "incoming_searches": {},
        "candidate_results": {ed: env}, "groups": {gd: group}, "closures": owner["closures"],
        "stage_specs": owner["stage_specs"], "vcs_observation": owner["vcs_observation"],
    }))
    try:
        M.C.validate({"$defs": M.NATIVE_SCHEMA["$defs"], "allOf": [{"$ref": "#/$defs/CloneCandidateGroupV2"}]}, group)
        rec("clone-candidate-group-v2-schema", {"result": "ADMIT", "refusals": []})
    except Exception as exc:
        rec("clone-candidate-group-v2-schema", {"result": "REFUSE", "refusals": [str(exc)]})

    badm = copy.deepcopy(owner["execution_inputs"])
    badm["verdict"] = "pass"
    rec("schema-rejects-verdict-field", admit({**owner, "execution_inputs": badm}))

    want = {
        "owner-graph-file-positive": "ADMIT",
        "owner-graph-two-universes": "ADMIT",
        "false-complete-without-coverage-envelope": "REFUSE",
        "self-asserted-coverage-mismatch-owner-entry": "REFUSE",
        "omitted-owner-view": "REFUSE",
        "missing-inventory-pointer": "REFUSE",
        "lost-inventory-bytes": "REFUSE",
        "supplied-object-mismatch-not-pointer": "REFUSE",
        "invalid-blob-hash": "REFUSE",
        "derived-examined-exhaustive-mismatch": "REFUSE",
        "duplicate-inventory-same-kind": "REFUSE",
        "wrong-view-producer-vs-stage": "REFUSE",
        "store-pointers-required": "REFUSE",
        "vcs-none-not-applicable-alone": "REFUSE",
        "candidate-unavailable-envelope-schema": "ADMIT",
        "schema-rejects-candidate-autofix": "REFUSE",
        "clone-candidate-group-v2-schema": "ADMIT",
        "required-candidate-group-bytes-join": "ADMIT",
        "schema-rejects-verdict-field": "REFUSE",
    }
    mismatches = []
    for c in cases:
        exp = want.get(c["case"])
        if exp and c["result"] != exp:
            mismatches.append({"case": c["case"], "got": c["result"], "want": exp,
                               "refusals": c.get("refusals"), "deficiencies": c.get("deficiencyCauses")})
    report = {
        "standing": "execution-inputs join checks; owner-graph from evaluator_graph_fixture.v3.py; not a Run; does not overwrite grok-execution-inputs.v1; does not relabel check-replay.v3.py.",
        "hostTcbHonesty": "sealed replay trusts host-captured stage-return inventory; cannot certify malicious host omissions",
        "cases": cases, "expected": want, "mismatches": mismatches,
        "ownedHashes": owned_hashes(), "internalFaults": list(M.INTERNAL_FAULTS),
        "ownerPositiveDeficiencies": cases[0].get("deficiencyCauses") if cases else [],
        "ownerPositiveRelations": cases[0].get("deficiencyRelations") if cases else [],
    }
    text = json.dumps(report, indent=2) + "\n"
    print(text, end="")
    if receipt_path:
        receipt_path.parent.mkdir(parents=True, exist_ok=True)
        receipt_path.write_text(text)
        if hashes_path:
            hashes_path.write_text(json.dumps(report["ownedHashes"], indent=2) + "\n")
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
