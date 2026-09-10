#!/usr/bin/env python3
"""Execution-inputs join checks against owner-admitted fixture graphs where feasible.

Not a Run. Does not overwrite grok-execution-inputs.v1, v2, or v3.
Default: print JSON to stdout only. Optional --receipt PATH for an explicit new report.
Checker-only helpers mint package complete-empty Coverage and omitted-view/candidate
controls; root owns the fixture file.
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
    "grok-execution-inputs.v2", "grok-execution-inputs.v3",
)
CAND_SCHEMA = {"$defs": M.SCHEMA["$defs"], "allOf": [{"$ref": "#/$defs/CandidateProducerResultV1"}]}
GROUP_SCHEMA = {"$defs": M.NATIVE_SCHEMA["$defs"], "allOf": [{"$ref": "#/$defs/CloneCandidateGroupV2"}]}


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


def payload_of(objects, blobs, coverage_id):
    env = objects[coverage_id][1]
    return M.C.parse(blobs[env["payloadDigest"]])


def _blob(blobs, value):
    raw = value if type(value) is bytes else M.C.canonical(value)
    digest = hashlib.sha256(raw).hexdigest()
    blobs[digest] = raw
    return digest


def _mint(objects, domain, fields):
    rec = {"schemaVersion": 2, **fields}
    key = M.IM.identifier(domain, rec)
    objects[key] = (domain, rec)
    return key


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
    for ci, cell in enumerate(enum["cells"]):
        for b in cell["programBindings"]:
            po = b["ordinal"]
            uni = b.get("universe")
            kinds = cell["kinds"]
            inv_ds = M.canon_str_list(
                [d for d, inv in graph["inventoryResults"]
                 if inv["cellOrdinal"] == ci and inv["programOrdinal"] == po]
            )
            inv_recs = [
                {"digest": d, **inv} for d, inv in graph["inventoryResults"]
                if inv["cellOrdinal"] == ci and inv["programOrdinal"] == po
            ]
            cap_rels = {p[0] for p in M._matrix_pairs(cell["capabilityId"])}
            bound_views, bound_cov = [], []
            for vid in view_ids:
                view = objects[vid][1]
                matched_u = matched_rel = False
                for sid in view["scopeIds"]:
                    sc = objects[sid][1]
                    if sc.get("sourceUniverse") == uni:
                        matched_u = True
                    if sc.get("relation") in cap_rels or not cap_rels:
                        matched_rel = True
                if matched_u and matched_rel:
                    bound_views.append(hx(vid))
                    bound_cov.extend(hx(c) for c in view["coverageIds"])
            en = b.get("enumerator") or {}
            en_status = en.get("status")
            matrix_row = M.CELL_STATE.get((cell["capabilityId"], cell["languageMode"]))
            acc_summ = []
            for rel, rung in M._matrix_pairs(cell["capabilityId"]):
                app = M.derived_applicability(rel, uni, en_status, (matrix_row or {}).get("state"), vcs.get("kind"))
                matched = []
                if app == "supported-available":
                    for cid in bound_cov:
                        full = "coverage2:" + cid
                        if full not in objects:
                            continue
                        pay = payload_of(objects, blobs, full)
                        key = pay.get("key") or {}
                        if key.get("relation") == rel and key.get("resolution") == rung and key.get("sourceUniverse") == uni:
                            matched.append(cid)
                accounts.append({
                    "cellOrdinal": ci, "programOrdinal": po, "relation": rel, "resolution": rung,
                    "sourceUniverse": None if app in ("unavailable-unselected", "unavailable-null-universe") else uni,
                    "targetUniverse": None if app in ("unavailable-unselected", "unavailable-null-universe") else uni,
                    "applicability": app,
                    "coverageIds": M.canon_str_list(matched),
                })
                defic = ncause = None
                if app == "supported-available":
                    st = "complete" if matched and all(
                        payload_of(objects, blobs, "coverage2:" + c)["entry"].get("coverage") == "complete"
                        for c in matched
                    ) else "incomplete"
                    if st == "incomplete":
                        defs = [payload_of(objects, blobs, "coverage2:" + c)["entry"].get("deficiency") for c in matched]
                        causes = [payload_of(objects, blobs, "coverage2:" + c)["entry"].get("nativeCause") for c in matched]
                        defs = [d for d in defs if d]
                        causes = [c for c in causes if c]
                        defic = defs[0] if defs else "provider-unavailable"
                        ncause = causes[0] if causes else None
                elif app == "unsupported-typed":
                    st = "unsupported"
                elif app == "inapplicable-vcs":
                    st = "inapplicable"
                else:
                    st = "unavailable"
                acc_summ.append({
                    "accountState": st, "relation": rel, "resolution": rung,
                    "deficiency": defic, "nativeCause": ncause, "nativeCauses": [ncause] if ncause else [],
                })
            derived = M.derive_outcome(
                enumerator_status=en_status, universe=uni, required=cell["required"],
                inventories=inv_recs, account_summaries=acc_summ,
                candidate_rec=None, candidate_digest=None,
                candidate_cap=cell["capabilityId"] in M.CANDIDATE_CAPS,
            )
            d_state, d_reason = derived["state"], derived["stageOrdinalNullReason"]
            outcomes.append({
                "ordinal": ordinal, "cellOrdinal": ci, "programOrdinal": po,
                "capabilityId": cell["capabilityId"], "languageMode": cell["languageMode"],
                "workspaceRoot": cell["workspaceRoot"], "required": cell["required"],
                "kinds": kinds, "universe": uni, "enumeratorStatus": en_status,
                "enumeratorClosure": en.get("closureId"), "state": d_state,
                "deficiency": derived["deficiency"] if d_state != "complete" else None,
                "nativeCause": derived["nativeCause"] if d_state != "complete" else None,
                "stageOrdinal": None if d_state == "unavailable" else 0,
                "stageOrdinalNullReason": d_reason if d_state == "unavailable" else None,
                "inventoryDigests": inv_ds,
                "viewDigests": M.canon_str_list(bound_views), "candidateResultDigest": None,
            })
            ordinal += 1
    view_hexes = M.canon_str_list([h for row in outcomes for h in row["viewDigests"]])
    cov_hexes = []
    for h in view_hexes:
        view = objects["view2:" + h][1]
        cov_hexes.extend(hx(c) for c in view["coverageIds"])
    selected = []
    for h in view_hexes:
        selected.append({"domain": "view", "digest": h})
    for d, inv in graph["inventoryResults"]:
        selected.append({"domain": "subject-inventory", "digest": d})
    for c in M.canon_str_list(cov_hexes):
        selected.append({"domain": "coverage", "digest": c})
    for iid in plan.get("importIds") or []:
        selected.append({"domain": "import", "digest": hx(iid)})
    selected = canon_refs(selected)
    host_derived = canon_refs([{"domain": "subject-inventory", "digest": d} for d, _inv in graph["inventoryResults"]])
    output_refs = canon_refs([{"domain": "view", "digest": h} for h in view_hexes])
    receipts = [{
        "ordinal": 0, "stageSpecDigest": stage_d, "producerClosure": stage_spec["producerClosure"],
        "outputDomains": list(stage_spec["outputDomains"]),
        "outputRefs": output_refs, "state": "complete", "unavailableReason": None,
    }]
    manifest = {
        "schemaVersion": 1, "planId": plan_id, "executionPlanId": exec_id,
        "evaluatorClosure": graph["inputs"]["evaluatorClosure"],
        "enumerationPlanDigest": M.raw_digest(enum),
        "analysisSpecDigest": plan["analysisSpecDigest"],
        "hostCapture": {
            "custody": "host-tcb-evidence-store", "observation": "stage-return",
            "stageReceipts": receipts, "hostDerivedRefs": host_derived,
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


def rebuild_after_object_mutation(owner, objects, blobs, extra_view_ids=None):
    """Rebuild selectedRefs/receipts/accounts after checker-only object mints."""
    graphish = {
        "objects": objects, "blobs": blobs,
        "inputs": {"planId": owner["plan_id"], "executionPlanId": owner["execution_plan_id"],
                   "evaluatorClosure": owner["execution_inputs"]["evaluatorClosure"]},
        "snapshot": owner["objects"][owner["plan"]["snapshotId"]][1],
        "enumerationPlan": owner["enumeration_plan"],
        "inventoryResults": list(owner["inventories"].items()),
        "viewIds": [k for k, (dom, _) in objects.items() if dom == "view"],
    }
    if extra_view_ids:
        graphish["viewIds"] = M.canon_str_list(list(dict.fromkeys(graphish["viewIds"] + extra_view_ids)))
    rebuilt = manifest_from_owner(graphish)
    rebuilt["closures"] = owner["closures"]
    rebuilt["stage_specs"] = owner["stage_specs"]
    rebuilt["plan"] = owner["plan"]
    rebuilt["analysis_spec"] = owner["analysis_spec"]
    rebuilt["execution_plan"] = owner["execution_plan"]
    rebuilt["inventories"] = owner["inventories"]
    rebuilt["imports"] = owner["imports"]
    rebuilt["execution_inputs"]["evaluatorClosure"] = owner["execution_inputs"]["evaluatorClosure"]
    rebuilt["execution_inputs"]["analysisSpecDigest"] = owner["execution_inputs"]["analysisSpecDigest"]
    rebuilt["execution_inputs"]["enumerationPlanDigest"] = owner["execution_inputs"]["enumerationPlanDigest"]
    return rebuilt


def add_package_complete_empty_coverage(owner):
    """Checker-only helper. Root owns the fixture. Mint package@manifest-declared complete-empty Coverage."""
    H = F.fixture_helpers()
    objects = dict(owner["objects"])
    blobs = dict(owner["blobs"])
    plan_id = owner["plan_id"]
    snapshot_id = owner["plan"]["snapshotId"]
    enum = owner["enumeration_plan"]
    binding = enum["cells"][0]["programBindings"][0]
    uni = binding["universe"]
    provider = binding["enumerator"]["closureId"]
    existing_view = next(v for k, (d, v) in objects.items() if d == "view")
    rel_schema, cov_schema = existing_view["schemaDigests"]
    scope = {
        "snapshotId": snapshot_id, "sourceUniverse": uni, "targetUniverse": uni,
        "relation": "package", "resolution": "manifest-declared",
        "enumeratorClosure": provider, "subjects": [],
    }
    scope_id = _mint(objects, "subject-scope", scope)
    paths = [r["path"] for r in objects[snapshot_id][1]["sourceInventory"]]
    payload = H.coverage_result(objects[scope_id][1], uni, True, blobs, paths)
    admitted = H.N.admit_coverage_result_v3(payload, objects[scope_id][1], [], cov_schema)
    if admitted.get("result") != "ADMIT":
        raise RuntimeError("package complete-empty Coverage not admitted: " + str(admitted))
    pd = _blob(blobs, payload)
    cov_id = _mint(objects, "coverage", {
        "scopeId": scope_id, "payloadSchemaDigest": cov_schema, "payloadDigest": pd,
    })
    view_id = _mint(objects, "view", {
        "planId": plan_id, "scopeIds": [scope_id], "facts": [],
        "coverageIds": [cov_id], "producerClosure": provider,
        "schemaDigests": M.canon_str_list([rel_schema, cov_schema]),
    })
    return rebuild_after_object_mutation(owner, objects, blobs, extra_view_ids=[view_id])


def add_unknown_file_partition(owner):
    """Checker-only: second file@enumerated Coverage (unknown) on a new view of the same cell."""
    H = F.fixture_helpers()
    objects = dict(owner["objects"])
    blobs = dict(owner["blobs"])
    plan_id = owner["plan_id"]
    snapshot_id = owner["plan"]["snapshotId"]
    enum = owner["enumeration_plan"]
    binding = enum["cells"][0]["programBindings"][0]
    uni = binding["universe"]
    provider = binding["enumerator"]["closureId"]
    existing_view = next(v for k, (d, v) in objects.items() if d == "view")
    rel_schema, cov_schema = existing_view["schemaDigests"]
    file_scope = next(v for k, (d, v) in objects.items() if d == "subject-scope" and v.get("relation") == "file")
    subjects = list(file_scope["subjects"])
    scope = {
        "snapshotId": snapshot_id, "sourceUniverse": uni, "targetUniverse": uni,
        "relation": "file", "resolution": "enumerated",
        "enumeratorClosure": provider, "subjects": subjects,
    }
    # distinct scope: same subjects would mint the same identity; perturb by using a copy with same subjects
    # Identity includes all fields; identical fields collide. Use the existing scope's subjects as-is
    # but a second scope with the same fields is the same scope2. Add a sentinel subject? That
    # would change the partition. Keep identical subjects by reusing a NEW scope only if fields differ.
    # Use the same subjects — collision is OK if we attach a different payload? No, scope identity
    # is the fields. Build unknown coverage on a clone of subjects via a second enumerator? Can't.
    # Use a one-subject partition (README.md) as a second returned partition of file@enumerated.
    scope["subjects"] = M.canon_str_list([subjects[0]]) if subjects else []
    scope_id = _mint(objects, "subject-scope", scope)
    paths = [r["path"] for r in objects[snapshot_id][1]["sourceInventory"]]
    payload = H.coverage_result(objects[scope_id][1], uni, False, blobs, paths)
    admitted = H.N.admit_coverage_result_v3(payload, objects[scope_id][1], [], cov_schema)
    if admitted.get("result") != "ADMIT":
        raise RuntimeError("unknown file partition not admitted: " + str(admitted))
    pd = _blob(blobs, payload)
    cov_id = _mint(objects, "coverage", {
        "scopeId": scope_id, "payloadSchemaDigest": cov_schema, "payloadDigest": pd,
    })
    view_id = _mint(objects, "view", {
        "planId": plan_id, "scopeIds": [scope_id], "facts": [],
        "coverageIds": [cov_id], "producerClosure": provider,
        "schemaDigests": M.canon_str_list([rel_schema, cov_schema]),
    })
    return rebuild_after_object_mutation(owner, objects, blobs, extra_view_ids=[view_id]), hx(cov_id)


def replace_file_view_with_one_subject(owner):
    """Returned complete Coverage over one path while file inventory still names all paths."""
    H = F.fixture_helpers()
    objects = dict(owner["objects"])
    blobs = dict(owner["blobs"])
    plan_id = owner["plan_id"]
    snapshot_id = owner["plan"]["snapshotId"]
    enum = owner["enumeration_plan"]
    binding = enum["cells"][0]["programBindings"][0]
    uni = binding["universe"]
    provider = binding["enumerator"]["closureId"]
    existing_view = next(v for k, (d, v) in objects.items() if d == "view")
    rel_schema, cov_schema = existing_view["schemaDigests"]
    scope = {
        "snapshotId": snapshot_id, "sourceUniverse": uni, "targetUniverse": uni,
        "relation": "file", "resolution": "enumerated",
        "enumeratorClosure": provider, "subjects": ["README.md"],
    }
    scope_id = _mint(objects, "subject-scope", scope)
    paths = [r["path"] for r in objects[snapshot_id][1]["sourceInventory"]]
    payload = H.coverage_result(objects[scope_id][1], uni, True, blobs, paths)
    admitted = H.N.admit_coverage_result_v3(payload, objects[scope_id][1], [], cov_schema)
    if admitted.get("result") != "ADMIT":
        raise RuntimeError("subset file Coverage not admitted: " + str(admitted))
    pd = _blob(blobs, payload)
    cov_id = _mint(objects, "coverage", {
        "scopeId": scope_id, "payloadSchemaDigest": cov_schema, "payloadDigest": pd,
    })
    view_id = _mint(objects, "view", {
        "planId": plan_id, "scopeIds": [scope_id], "facts": [],
        "coverageIds": [cov_id], "producerClosure": provider,
        "schemaDigests": M.canon_str_list([rel_schema, cov_schema]),
    })
    rebuilt = copy.deepcopy(owner)
    rebuilt["objects"] = objects
    rebuilt["blobs"] = blobs
    rebuilt["store_pointers"] = pointers_of(objects, blobs)
    vh = hx(view_id)
    ch = hx(cov_id)
    for row in rebuilt["execution_inputs"]["cellOutcomes"]:
        row["viewDigests"] = [vh]
    recp = rebuilt["execution_inputs"]["hostCapture"]["stageReceipts"][0]
    recp["outputRefs"] = canon_refs([{"domain": "view", "digest": vh}])
    sel = [r for r in rebuilt["execution_inputs"]["selectedRefs"] if r["domain"] not in ("view", "coverage")]
    sel.extend([{"domain": "view", "digest": vh}, {"domain": "coverage", "digest": ch}])
    rebuilt["execution_inputs"]["selectedRefs"] = canon_refs(sel)
    for a in rebuilt["execution_inputs"]["nativeCoverageAccounts"]:
        if a["relation"] == "file":
            a["coverageIds"] = [ch]
    return rebuilt


def snapshot_row(owner, path):
    snap = owner["objects"][owner["plan"]["snapshotId"]][1]
    return next(r for r in snap["sourceInventory"] if r["path"] == path)


def source_body(owner, body_id, path, universe):
    row = snapshot_row(owner, path)
    return {
        "id": body_id, "path": path, "contentSha256": row["sha256"],
        "byteLength": row["bytes"], "universe": universe,
    }


def near_candidate_kw(owner, *, members, bodies, plan_paths, examined=None, groups_map=True,
                      extra_cand_ref=False, mutate_group_map=False, wrong_u=False, extra_binding=None):
    """Checker-only clones-near graph. Body coordinates are retained on the envelope."""
    uni = "c" * 64
    prov = next(k for k, v in owner["closures"].items() if v.get("kind") == "provider")
    near_spec = {"requestedCapabilities": [
        {"capabilityId": "clones-near", "languageMode": "syntax-only", "workspaceRoot": ".", "required": True}]}
    bindings = [{
        "ordinal": 0, "provenance": "default-unit",
        "enumerator": {"status": "selected", "closureId": prov},
        "nativeContextDigest": "b" * 64, "universe": uni, "programEntry": None, "extents": [],
        "candidateSourcePaths": M.canon_str_list(plan_paths),
    }]
    if extra_binding:
        bindings.append(extra_binding)
    near_enum = {
        "schemaVersion": 1, "snapshotId": owner["plan"]["snapshotId"],
        "scopeDigest": owner["plan"]["scopeDigest"], "membershipDigest": "1" * 64,
        "cells": [{"capabilityId": "clones-near", "languageMode": "syntax-only", "workspaceRoot": ".",
                   "required": True, "kinds": [], "programBindings": bindings}],
    }
    group = None
    gd = None
    if members:
        group = {
            "mode": "near", "evidenceLevel": "similar-candidate", "language": "typescript",
            "members": members, "authority": "candidate-only",
            "matchedEdges": [{"left": members[0], "right": members[-1], "similarityMillionths": 900000}],
            "grouping": "connected-component", "scoreMeaning": "minimum-member-best-neighbor",
            "semanticEquivalenceClaimed": False, "automaticDeletionEligible": False,
        }
        gd = M.raw_digest(group)
    src_bodies = list(bodies)
    if wrong_u and src_bodies:
        src_bodies = [dict(src_bodies[0], universe="d" * 64)] + src_bodies[1:]
    src_bodies = sorted(src_bodies, key=M.C.canonical)
    env = {
        "schemaVersion": 1, "planId": owner["plan_id"], "executionPlanId": owner["execution_plan_id"],
        "cellOrdinal": 0, "programOrdinal": 0, "capabilityId": "clones-near", "languageMode": "syntax-only",
        "universe": uni, "producerClosure": prov, "stageOrdinal": 0, "state": "complete",
        "deficiency": None, "nativeCause": None, "authority": "candidate-only",
        "semanticEquivalenceClaimed": False, "automaticDeletionEligible": False,
        "examinedPaths": M.canon_str_list(examined if examined is not None else plan_paths),
        "groupDigests": [gd] if gd else [],
        "sourceBodies": src_bodies,
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
    outcomes = [near_outcome]
    if extra_binding:
        outcomes.append({
            "ordinal": 1, "cellOrdinal": 0, "programOrdinal": extra_binding["ordinal"],
            "capabilityId": "clones-near", "languageMode": "syntax-only", "workspaceRoot": ".",
            "required": True, "kinds": [], "universe": extra_binding["universe"],
            "enumeratorStatus": "selected", "enumeratorClosure": prov, "state": "complete",
            "deficiency": None, "nativeCause": None, "stageOrdinal": 0, "stageOrdinalNullReason": None,
            "inventoryDigests": [], "viewDigests": [], "candidateResultDigest": None,
        })
    stage_d = owner["execution_plan"]["stages"][0]["stageSpecDigest"]
    cand_refs = M.canon_str_list([ed] + (["a" * 64] if extra_cand_ref else []))
    host_derived = canon_refs([{"domain": "candidate-producer-result", "digest": ed}])
    near_manifest = {
        "schemaVersion": 1, "planId": owner["plan_id"], "executionPlanId": owner["execution_plan_id"],
        "evaluatorClosure": owner["execution_inputs"]["evaluatorClosure"],
        "enumerationPlanDigest": M.raw_digest(near_enum), "analysisSpecDigest": near_plan["analysisSpecDigest"],
        "hostCapture": {
            "custody": "host-tcb-evidence-store", "observation": "stage-return",
            "stageReceipts": [{
                "ordinal": 0, "stageSpecDigest": stage_d,
                "producerClosure": owner["stage_specs"][stage_d]["producerClosure"],
                "outputDomains": list(owner["stage_specs"][stage_d]["outputDomains"]),
                "outputRefs": [], "state": "complete", "unavailableReason": None,
            }],
            "hostDerivedRefs": host_derived,
            "retainedObjectKeys": sorted(owner["objects"]),
            "retainedBlobDigests": M.canon_str_list(list(owner["blobs"]) + ([gd] if gd else []) + [ed]),
        },
        "selectedRefs": host_derived,
        "cellOutcomes": outcomes, "nativeCoverageAccounts": [], "candidateResultRefs": cand_refs,
    }
    near_blobs = dict(owner["blobs"])
    if gd:
        near_blobs[gd] = M.C.canonical(group)
    near_blobs[ed] = M.C.canonical(env)
    gmap = {gd: group} if gd else {}
    if mutate_group_map and members:
        gmap = {gd: dict(group, members=list(members) + ["unbound-extra"])}
    extra = "a" * 64
    if extra_cand_ref:
        near_blobs[extra] = b"{}"
    return {
        "plan_id": owner["plan_id"], "plan": near_plan, "execution_plan_id": owner["execution_plan_id"],
        "execution_plan": owner["execution_plan"], "enumeration_plan": near_enum, "analysis_spec": near_spec,
        "execution_inputs": near_manifest, "objects": owner["objects"], "blobs": near_blobs,
        "store_pointers": pointers_of(owner["objects"], near_blobs) + ([extra] if extra_cand_ref else []),
        "inventories": {}, "imports": {}, "target_attributions": {}, "incoming_searches": {},
        "candidate_results": {ed: env}, "groups": gmap if groups_map else {},
        "closures": owner["closures"], "stage_specs": owner["stage_specs"],
        "vcs_observation": owner["vcs_observation"],
    }


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
        derived_states = [d.get("state") for d in result.get("derivedOutcomes") or []]
        derived_acc = [d.get("accountState") for d in result.get("derivedAccounts") or []]
        cases.append({
            "case": name, "result": result.get("result"),
            "refusals": result.get("refusals"),
            "deficiencyCauses": [d.get("cause") for d in result.get("requiredCellDeficiencies") or []],
            "deficiencyRelations": [d.get("relation") for d in result.get("requiredCellDeficiencies") or []],
            "derivedOutcomeStates": derived_states,
            "derivedAccountStates": derived_acc,
            "rowComplete": derived_states == ["complete"] if derived_states else False,
        })

    graph = F.build_file_inputs()
    owner = manifest_from_owner(graph)
    rec("owner-graph-file-positive", admit(owner))

    two = manifest_from_owner(F.build_file_inputs(multiple_universes=True))
    rec("owner-graph-two-universes", admit(two))

    pkg = add_package_complete_empty_coverage(owner)
    rec("required-package-complete-empty-coverage", admit(pkg))

    mixed, extra_cov = add_unknown_file_partition(owner)
    rec("mixed-coverage-all-partitions-named", admit(mixed))
    subset = copy.deepcopy(mixed)
    for a in subset["execution_inputs"]["nativeCoverageAccounts"]:
        if a["relation"] == "file" and extra_cov in a["coverageIds"]:
            a["coverageIds"] = M.canon_str_list([c for c in a["coverageIds"] if c != extra_cov])
    rec("omitted-returned-partition-not-subset", admit(subset))

    drop = copy.deepcopy(owner)
    drop["execution_inputs"]["selectedRefs"] = [
        r for r in drop["execution_inputs"]["selectedRefs"] if r["domain"] != "view"
    ]
    rec("omitted-owner-view", admit(drop))

    m1 = copy.deepcopy(owner)
    m1["execution_inputs"]["selectedRefs"] = [
        r for r in m1["execution_inputs"]["selectedRefs"] if r["domain"] != "view"
    ]
    for row in m1["execution_inputs"]["cellOutcomes"]:
        row["viewDigests"] = []
    rec("receipt-view-omitted-from-selected-and-outcomes", admit(m1))

    complete_lie = copy.deepcopy(owner)
    for row in complete_lie["execution_inputs"]["cellOutcomes"]:
        row["state"] = "complete"
        row["deficiency"] = None
        row["nativeCause"] = None
        row["stageOrdinal"] = 0
        row["stageOrdinalNullReason"] = None
    rec("self-asserted-complete-with-incomplete-package", admit(complete_lie))

    omit_stage = copy.deepcopy(owner)
    for row in omit_stage["execution_inputs"]["cellOutcomes"]:
        row["state"] = "unavailable"
        row["deficiency"] = "provider-unavailable"
        row["stageOrdinal"] = None
        row["stageOrdinalNullReason"] = "unavailable-binding"
        row["viewDigests"] = []
    rec("unavailable-selected-u-omits-stage-and-views", admit(omit_stage))

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
            a["applicability"] = "supported-available"
            a["coverageIds"] = [hx(graph["coverageId"])]
    rec("vcs-none-not-applicable-alone", admit(vcs_lie))

    views_merge = copy.deepcopy(owner)
    rec("views-map-extra-merge", admit({**views_merge, "views": {"f" * 64: {"schemaVersion": 2}}}))

    no_eval = copy.deepcopy(owner)
    closures = {k: v for k, v in no_eval["closures"].items() if v.get("kind") != "evaluator"}
    rec("evaluator-closure-missing-from-map", admit({**no_eval, "closures": closures}))

    payload_gone = copy.deepcopy(owner)
    cov_id = graph["coverageId"]
    env = payload_gone["objects"][cov_id][1]
    blobs = dict(payload_gone["blobs"])
    blobs.pop(env["payloadDigest"], None)
    rec("coverage-payload-bytes-absent", admit({**payload_gone, "blobs": blobs}))

    # unsupported-typed wrong cause: references@syntax-only is UNSUPPORTED-TYPED / language-tier-unsupported
    ref_spec = {"requestedCapabilities": [
        {"capabilityId": "references", "languageMode": "syntax-only", "workspaceRoot": ".", "required": True}]}
    prov = next(k for k, v in owner["closures"].items() if v.get("kind") == "provider")
    uni = owner["enumeration_plan"]["cells"][0]["programBindings"][0]["universe"]
    ref_enum = {
        "schemaVersion": 1, "snapshotId": owner["plan"]["snapshotId"],
        "scopeDigest": owner["plan"]["scopeDigest"], "membershipDigest": owner["enumeration_plan"]["membershipDigest"],
        "cells": [{"capabilityId": "references", "languageMode": "syntax-only", "workspaceRoot": ".",
                   "required": True, "kinds": ["symbol"],
                   "programBindings": [{"ordinal": 0, "provenance": "default-unit",
                                        "enumerator": {"status": "selected", "closureId": prov},
                                        "nativeContextDigest": "b" * 64, "universe": uni,
                                        "programEntry": None, "extents": [{"kind": "symbol", "paths": ["src/index.ts"]}]}]}],
    }
    inv_sym = {
        "schemaVersion": 1, "planId": owner["plan_id"], "parameterDigest": M.raw_digest(ref_enum),
        "cellOrdinal": 0, "programOrdinal": 0, "kind": "symbol", "state": "complete",
        "deficiency": None, "nativeCause": None, "examinedPaths": ["src/index.ts"],
        "rows": [{"nativeSubjectId": "x", "kind": "symbol", "path": "src/index.ts", "qualifiedName": "x",
                  "subjectLanguage": "typescript", "signatureTokens": ["function", "x"], "projections": []}],
    }
    inv_d = M.raw_digest(inv_sym)
    ref_plan = dict(owner["plan"])
    ref_plan["analysisSpecDigest"] = M.raw_digest(ref_spec)
    stage_d = owner["execution_plan"]["stages"][0]["stageSpecDigest"]
    ref_outcome = {
        "ordinal": 0, "cellOrdinal": 0, "programOrdinal": 0, "capabilityId": "references",
        "languageMode": "syntax-only", "workspaceRoot": ".", "required": True, "kinds": ["symbol"],
        "universe": uni, "enumeratorStatus": "selected", "enumeratorClosure": prov, "state": "complete",
        "deficiency": None, "nativeCause": None,
        "stageOrdinal": 0, "stageOrdinalNullReason": None,
        "inventoryDigests": [inv_d], "viewDigests": [], "candidateResultDigest": None,
    }
    # matrix unsupported still owes a coverage account with empty ids
    ref_acc = {
        "cellOrdinal": 0, "programOrdinal": 0, "relation": "references", "resolution": "resolved-binding",
        "sourceUniverse": uni, "targetUniverse": uni, "applicability": "unsupported-typed", "coverageIds": [],
    }
    ref_manifest = {
        "schemaVersion": 1, "planId": owner["plan_id"], "executionPlanId": owner["execution_plan_id"],
        "evaluatorClosure": owner["execution_inputs"]["evaluatorClosure"],
        "enumerationPlanDigest": M.raw_digest(ref_enum), "analysisSpecDigest": ref_plan["analysisSpecDigest"],
        "hostCapture": {
            "custody": "host-tcb-evidence-store", "observation": "stage-return",
            "stageReceipts": [{
                "ordinal": 0, "stageSpecDigest": stage_d,
                "producerClosure": owner["stage_specs"][stage_d]["producerClosure"],
                "outputDomains": list(owner["stage_specs"][stage_d]["outputDomains"]),
                "outputRefs": [], "state": "complete", "unavailableReason": None,
            }],
            "hostDerivedRefs": canon_refs([{"domain": "subject-inventory", "digest": inv_d}]),
            "retainedObjectKeys": sorted(owner["objects"]),
            "retainedBlobDigests": M.canon_str_list(list(owner["blobs"]) + [inv_d]),
        },
        "selectedRefs": canon_refs([{"domain": "subject-inventory", "digest": inv_d}]),
        "cellOutcomes": [ref_outcome], "nativeCoverageAccounts": [ref_acc], "candidateResultRefs": [],
    }
    ref_blobs = dict(owner["blobs"]); ref_blobs[inv_d] = M.C.canonical(inv_sym)
    rec("unsupported-typed-matrix-cause", admit({
        "plan_id": owner["plan_id"], "plan": ref_plan, "execution_plan_id": owner["execution_plan_id"],
        "execution_plan": owner["execution_plan"], "enumeration_plan": ref_enum, "analysis_spec": ref_spec,
        "execution_inputs": ref_manifest, "objects": owner["objects"], "blobs": ref_blobs,
        "store_pointers": pointers_of(owner["objects"], ref_blobs), "inventories": {inv_d: inv_sym},
        "imports": {}, "target_attributions": {}, "incoming_searches": {},
        "candidate_results": {}, "groups": {}, "closures": owner["closures"],
        "stage_specs": owner["stage_specs"], "vcs_observation": owner["vcs_observation"],
    }))

    plan_paths = ["src/index.ts"]
    bodies = [
        source_body(owner, "body-a", "src/index.ts", "c" * 64),
        source_body(owner, "body-b", "src/index.ts", "c" * 64),
    ]
    rec("required-candidate-group-bytes-join", admit(near_candidate_kw(
        owner, members=["body-a", "body-b"], bodies=bodies, plan_paths=plan_paths)))
    rec("extra-candidate-ref-no-outcome", admit(near_candidate_kw(
        owner, members=["body-a", "body-b"], bodies=bodies, plan_paths=plan_paths, extra_cand_ref=True)))
    rec("groups-map-bypasses-blob", admit(near_candidate_kw(
        owner, members=["body-a", "body-b"], bodies=bodies, plan_paths=plan_paths, mutate_group_map=True)))
    rec("clone-member-opaque-id-no-custody", admit(near_candidate_kw(
        owner, members=["opaque-body-id"], bodies=bodies, plan_paths=plan_paths)))
    rec("complete-candidate-empty-examined-not-plan-extent", admit(near_candidate_kw(
        owner, members=["body-a", "body-b"], bodies=bodies, plan_paths=plan_paths, examined=[])))
    rec("candidate-wrong-universe-source-body", admit(near_candidate_kw(
        owner, members=["body-a", "body-b"], bodies=bodies, plan_paths=plan_paths, wrong_u=True)))
    rec("complete-empty-candidate-with-plan-extent", admit(near_candidate_kw(
        owner, members=[], bodies=[], plan_paths=plan_paths)))
    rec("complete-empty-candidate-without-plan-extent", admit(near_candidate_kw(
        owner, members=[], bodies=[], plan_paths=plan_paths, examined=[])))
    extra_b = {
        "ordinal": 1, "provenance": "explicit-plan-selection",
        "enumerator": {"status": "selected", "closureId": next(k for k, v in owner["closures"].items() if v.get("kind") == "provider")},
        "nativeContextDigest": "b" * 64, "universe": "d" * 64, "programEntry": None, "extents": [],
        "candidateSourcePaths": ["README.md"],
    }
    rec("candidate-examined-union-not-this-program-extent", admit(near_candidate_kw(
        owner, members=["body-a", "body-b"], bodies=bodies, plan_paths=plan_paths,
        examined=["src/index.ts", "README.md"], extra_binding=extra_b)))

    cand = {
        "schemaVersion": 1, "planId": owner["plan_id"], "executionPlanId": owner["execution_plan_id"],
        "cellOrdinal": 0, "programOrdinal": 0, "capabilityId": "clones-near",
        "languageMode": "syntax-only", "universe": None, "producerClosure": graph["inputs"]["evaluatorClosure"],
        "stageOrdinal": None, "state": "unavailable", "deficiency": "provider-unavailable",
        "nativeCause": None, "authority": "candidate-only", "semanticEquivalenceClaimed": False,
        "automaticDeletionEligible": False, "examinedPaths": [], "groupDigests": [], "sourceBodies": [],
    }
    try:
        M.C.validate(CAND_SCHEMA, cand)
        rec("candidate-unavailable-envelope-schema", {"result": "ADMIT", "refusals": []})
    except Exception as exc:
        rec("candidate-unavailable-envelope-schema", {"result": "REFUSE", "refusals": [str(exc)]})

    autofix = dict(cand, state="complete", deficiency=None, universe="c" * 64, stageOrdinal=0,
                   automaticDeletionEligible=True, examinedPaths=["src/index.ts"], sourceBodies=[])
    try:
        M.C.validate(CAND_SCHEMA, autofix)
        rec("schema-rejects-candidate-autofix", {"result": "ADMIT", "refusals": []})
    except Exception:
        rec("schema-rejects-candidate-autofix", {"result": "REFUSE", "refusals": ["EXECUTION_INPUTS_SCHEMA"]})

    group = {
        "mode": "near", "evidenceLevel": "similar-candidate", "language": "typescript",
        "members": ["body-a"], "authority": "candidate-only",
        "matchedEdges": [{"left": "body-a", "right": "body-a", "similarityMillionths": 900000}],
        "grouping": "connected-component", "scoreMeaning": "minimum-member-best-neighbor",
        "semanticEquivalenceClaimed": False, "automaticDeletionEligible": False,
    }
    try:
        M.C.validate(GROUP_SCHEMA, group)
        rec("clone-candidate-group-v2-schema", {"result": "ADMIT", "refusals": []})
    except Exception as exc:
        rec("clone-candidate-group-v2-schema", {"result": "REFUSE", "refusals": [str(exc)]})

    badm = copy.deepcopy(owner["execution_inputs"])
    badm["verdict"] = "pass"
    rec("schema-rejects-verdict-field", admit({**owner, "execution_inputs": badm}))

    try:
        partial_graph = F.build_file_inputs(symbol_rows=[{"nativeSubjectId": "x"}], symbol_state="partial")
        partial = manifest_from_owner(partial_graph)
        rec("partial-inventory-known-rows", admit(partial))
        swapped = copy.deepcopy(partial)
        for row in swapped["execution_inputs"]["cellOutcomes"]:
            if row["capabilityId"] == "syntax" and row["state"] == "partial":
                row["deficiency"] = "provider-unavailable"
                row["nativeCause"] = None
        rec("partial-inventory-budget-not-replaced-by-provider-unavailable", admit(swapped))
    except Exception as exc:
        rec("partial-inventory-known-rows", {"result": "REFUSE", "refusals": [type(exc).__name__ + ":" + str(exc)]})
        rec("partial-inventory-budget-not-replaced-by-provider-unavailable",
            {"result": "REFUSE", "refusals": [type(exc).__name__ + ":" + str(exc)]})

    rec("expected-source-census-uncovered-is-incomplete", admit(replace_file_view_with_one_subject(owner)))

    # Target sidecar: host-derived, not a view-stage output.
    fact_id = None
    for vid in graph["viewIds"]:
        facts = owner["objects"][vid][1].get("facts") or []
        if facts:
            fact_id = facts[0]
            break
    if fact_id:
        fact = owner["objects"][fact_id][1]
        tgt = {
            "schemaVersion": 1, "planId": owner["plan_id"], "sourceFactId": fact_id,
            "producerClosure": fact["producerClosure"], "targetUniverse": fact["targetUniverse"],
            "targetNativeId": "src/index.ts", "kind": "file", "occupancy": "first-party",
            "exported": None, "logicalPath": None, "packageManifestPath": None,
        }
        td = M.raw_digest(tgt)
        sidecar = copy.deepcopy(owner)
        blobs = dict(sidecar["blobs"]); blobs[td] = M.C.canonical(tgt)
        sidecar["blobs"] = blobs
        sidecar["store_pointers"] = pointers_of(sidecar["objects"], blobs)
        sidecar["target_attributions"] = {td: tgt}
        ref = {"domain": "target-attribution", "digest": td}
        sidecar["execution_inputs"]["hostCapture"]["hostDerivedRefs"] = canon_refs(
            list(sidecar["execution_inputs"]["hostCapture"]["hostDerivedRefs"]) + [ref])
        sidecar["execution_inputs"]["selectedRefs"] = canon_refs(
            list(sidecar["execution_inputs"]["selectedRefs"]) + [ref])
        rec("host-derived-target-sidecar-not-stage-output", admit(sidecar))
    else:
        rec("host-derived-target-sidecar-not-stage-output", {"result": "REFUSE", "refusals": ["NO_FACT"]})

    want = {
        "owner-graph-file-positive": "ADMIT",
        "owner-graph-two-universes": "ADMIT",
        "required-package-complete-empty-coverage": "ADMIT",
        "mixed-coverage-all-partitions-named": "ADMIT",
        "omitted-returned-partition-not-subset": "REFUSE",
        "omitted-owner-view": "REFUSE",
        "receipt-view-omitted-from-selected-and-outcomes": "REFUSE",
        "self-asserted-complete-with-incomplete-package": "REFUSE",
        "unavailable-selected-u-omits-stage-and-views": "REFUSE",
        "missing-inventory-pointer": "REFUSE",
        "lost-inventory-bytes": "REFUSE",
        "supplied-object-mismatch-not-pointer": "REFUSE",
        "invalid-blob-hash": "REFUSE",
        "duplicate-inventory-same-kind": "REFUSE",
        "wrong-view-producer-vs-stage": "REFUSE",
        "store-pointers-required": "REFUSE",
        "vcs-none-not-applicable-alone": "REFUSE",
        "views-map-extra-merge": "REFUSE",
        "evaluator-closure-missing-from-map": "REFUSE",
        "coverage-payload-bytes-absent": "REFUSE",
        "unsupported-typed-matrix-cause": "ADMIT",
        "required-candidate-group-bytes-join": "ADMIT",
        "extra-candidate-ref-no-outcome": "REFUSE",
        "groups-map-bypasses-blob": "REFUSE",
        "clone-member-opaque-id-no-custody": "REFUSE",
        "complete-candidate-empty-examined-not-plan-extent": "REFUSE",
        "candidate-wrong-universe-source-body": "REFUSE",
        "complete-empty-candidate-with-plan-extent": "ADMIT",
        "complete-empty-candidate-without-plan-extent": "REFUSE",
        "candidate-examined-union-not-this-program-extent": "REFUSE",
        "partial-inventory-budget-not-replaced-by-provider-unavailable": "REFUSE",
        "expected-source-census-uncovered-is-incomplete": "ADMIT",
        "host-derived-target-sidecar-not-stage-output": "ADMIT",
        "candidate-unavailable-envelope-schema": "ADMIT",
        "schema-rejects-candidate-autofix": "REFUSE",
        "clone-candidate-group-v2-schema": "ADMIT",
        "schema-rejects-verdict-field": "REFUSE",
        "partial-inventory-known-rows": "ADMIT",
    }
    mismatches = []
    for c in cases:
        exp = want.get(c["case"])
        if exp and c["result"] != exp:
            mismatches.append({"case": c["case"], "got": c["result"], "want": exp,
                               "refusals": c.get("refusals"), "deficiencies": c.get("deficiencyCauses")})
    owner0 = cases[0] if cases else {}
    oracles = []
    if owner0.get("result") == "ADMIT" and owner0.get("rowComplete"):
        oracles.append({"oracle": "owner-graph-file-positive-must-not-be-complete",
                        "got": owner0.get("derivedOutcomeStates")})
    pkg_case = next((c for c in cases if c["case"] == "required-package-complete-empty-coverage"), None)
    if pkg_case and pkg_case.get("result") == "ADMIT":
        if "incomplete" in (pkg_case.get("derivedAccountStates") or []):
            oracles.append({"oracle": "package-complete-empty-must-complete-package-account",
                            "got": pkg_case.get("derivedAccountStates")})
    mixed_case = next((c for c in cases if c["case"] == "mixed-coverage-all-partitions-named"), None)
    if mixed_case and mixed_case.get("result") == "ADMIT" and mixed_case.get("rowComplete"):
        oracles.append({"oracle": "mixed-complete-plus-unknown-must-not-be-complete",
                        "got": mixed_case.get("derivedAccountStates")})
    payload_case = next((c for c in cases if c["case"] == "coverage-payload-bytes-absent"), None)
    if payload_case and payload_case.get("result") == "REFUSE":
        if "EXECUTION_INPUTS_EVIDENCE_UNAVAILABLE" not in (payload_case.get("refusals") or []):
            oracles.append({"oracle": "absent-payload-must-be-evidence-unavailable",
                            "got": payload_case.get("refusals")})
    census = next((c for c in cases if c["case"] == "expected-source-census-uncovered-is-incomplete"), None)
    if census and census.get("result") == "ADMIT" and (census.get("derivedAccountStates") or [None])[0] == "complete":
        oracles.append({"oracle": "subset-complete-coverage-must-not-complete-file-account",
                        "got": census.get("derivedAccountStates")})
    partial_case = next((c for c in cases if c["case"] == "partial-inventory-known-rows"), None)
    if partial_case and partial_case.get("result") == "ADMIT":
        if "required-cell-unsatisfied" not in (partial_case.get("deficiencyCauses") or []):
            oracles.append({"oracle": "required-partial-inventory-must-emit-required-cell-deficiency",
                            "got": partial_case.get("deficiencyCauses")})
    mismatches.extend({"case": o["oracle"], "got": "ORACLE", "want": "HOLD", "refusals": [str(o["got"])]} for o in oracles)

    report = {
        "standing": "execution-inputs join checks; owner-graph from evaluator_graph_fixture.v3.py; not a Run; does not overwrite grok-execution-inputs.v1/v2/v3; does not relabel check-replay.v3.py.",
        "hostTcbHonesty": "sealed replay trusts host-captured stage-return inventory; cannot certify malicious host omissions",
        "causeRetention": "derivedAccounts retain ALL native causes; requiredCellDeficiencies one row per (cell, program, cause, relation)",
        "cases": cases, "expected": want, "mismatches": mismatches, "oracles": oracles,
        "ownedHashes": owned_hashes(), "internalFaults": list(M.INTERNAL_FAULTS),
        "neededRootInputs": list(M.NEEDED_ROOT),
        "ownerPositiveDeficiencies": owner0.get("deficiencyCauses"),
        "ownerPositiveRelations": owner0.get("deficiencyRelations"),
        "ownerPositiveDerivedStates": owner0.get("derivedOutcomeStates"),
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
