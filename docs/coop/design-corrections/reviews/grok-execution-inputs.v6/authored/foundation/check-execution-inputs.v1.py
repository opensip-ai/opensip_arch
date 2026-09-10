#!/usr/bin/env python3
"""Execution-inputs join checks against owner-admitted fixture graphs where feasible.

Not a Run. Does not overwrite grok-execution-inputs.v1, v2, v3, v4, or v5.
Default: print JSON to stdout only. Optional --receipt PATH for an explicit new report.
Builder is execution_inputs_fixture.v3.py (not inlined here). Checker-only helpers mint
package complete-empty Coverage and omitted-view/candidate controls; root owns the fixture file.
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
_hspec = importlib.util.spec_from_file_location("exec_in_host_capture", HERE / "execution_inputs_fixture.v3.py")
H = importlib.util.module_from_spec(_hspec)
_hspec.loader.exec_module(H)
_sspec = importlib.util.spec_from_file_location("exec_in_sem_fix", HERE / "evaluator_semantic_fixture.v3.py")
S = importlib.util.module_from_spec(_sspec)
_sspec.loader.exec_module(S)

PINNED_V1 = "grok-execution-inputs.v1"
HISTORICAL = (
    "grok-subject-assessment.v7", "grok-subject-assessment.v8",
    "grok-subject-assessment.v9", "grok-subject-assessment.v10",
    "grok-subject-assessment.v11", PINNED_V1,
    "grok-execution-inputs.v2", "grok-execution-inputs.v3",
    "grok-execution-inputs.v4", "grok-execution-inputs.v5",
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
    return H.hx(prefixed)


def canon_refs(refs):
    return H.canon_refs(refs)


def pointers_of(objects, blobs):
    return H.pointers_of(objects, blobs)


def payload_of(objects, blobs, coverage_id):
    return H.payload_of(objects, blobs, coverage_id)


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
    """Shared builder. Does not import production reference from this checker."""
    return H.admission_kwargs(graph)


def admit(kw):
    return M.admit_execution_inputs(**kw)


def rebuild_after_object_mutation(owner, objects, blobs, extra_view_ids=None):
    """Rebuild selectedRefs/receipts/accounts after checker-only object mints."""
    view_ids = [k for k, (dom, _) in objects.items() if dom == "view"]
    if extra_view_ids:
        view_ids = M.canon_str_list(list(dict.fromkeys(view_ids + extra_view_ids)))
    snap_id = owner["plan"]["snapshotId"]
    snapshot = objects[snap_id][1] if snap_id in objects else owner["objects"][snap_id][1]
    graphish = {
        "objects": objects, "blobs": blobs,
        "inputs": {
            "planId": owner["plan_id"], "executionPlanId": owner["execution_plan_id"],
            "evaluatorClosure": owner["execution_inputs"]["evaluatorClosure"],
            "evaluationInputRefs": list(owner["execution_inputs"].get("selectedRefs") or []),
        },
        "snapshot": snapshot,
        "enumerationPlan": owner["enumeration_plan"],
        "inventoryResults": list(owner["inventories"].items()),
        "viewIds": view_ids,
        "coverageIds": [k for k, (dom, _) in objects.items() if dom == "coverage"],
        "planId": owner["plan_id"], "executionPlanId": owner["execution_plan_id"],
    }
    rebuilt = H.admission_kwargs(graphish)
    rebuilt["closures"] = owner["closures"]
    rebuilt["stage_specs"] = owner["stage_specs"]
    rebuilt["plan"] = owner["plan"]
    rebuilt["analysis_spec"] = owner["analysis_spec"]
    rebuilt["execution_plan"] = owner["execution_plan"]
    rebuilt["inventories"] = owner["inventories"]
    rebuilt["imports"] = owner["imports"]
    rebuilt["target_attributions"] = owner.get("target_attributions") or {}
    rebuilt["incoming_searches"] = owner.get("incoming_searches") or {}
    rebuilt["candidate_results"] = owner.get("candidate_results") or {}
    rebuilt["groups"] = owner.get("groups") or {}
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


def graph_two_partial_inventories():
    """Same cell, two inventories, distinct deficiency+inputRef pairs."""
    graph = copy.deepcopy(F.build_file_inputs())
    new = []
    for _d, inv in graph["inventoryResults"]:
        inv = copy.deepcopy(inv)
        if inv["kind"] == "file":
            inv["state"] = "partial"
            inv["deficiency"] = "budget-exhausted"
            inv["nativeCause"] = None
        elif inv["kind"] == "package":
            inv["state"] = "partial"
            inv["deficiency"] = "input-closure-incomplete"
            inv["nativeCause"] = "lockfile-missing"
        raw = M.C.canonical(inv)
        nd = hashlib.sha256(raw).hexdigest()
        graph["blobs"][nd] = raw
        new.append((nd, inv))
    graph["inventoryResults"] = new
    keep = [r for r in graph["inputs"]["evaluationInputRefs"] if r.get("domain") != "subject-inventory"]
    keep.extend({"domain": "subject-inventory", "digest": d} for d, _inv in new)
    graph["inputs"]["evaluationInputRefs"] = canon_refs(keep)
    return graph


def graph_unavailable_binding_keeps_inventory():
    """Selected unavailable binding (universe=null) with typed carrier plus partial inventory."""
    graph = copy.deepcopy(F.build_file_inputs(symbol_rows=[{"nativeSubjectId": "x"}], symbol_state="partial"))
    cell = graph["enumerationPlan"]["cells"][1]
    b = cell["programBindings"][0]
    b["universe"] = None
    b["deficiency"] = "input-closure-incomplete"
    b["nativeCause"] = "lockfile-missing"
    b["nativeContextDigest"] = None
    return graph


def rc3_summarize_unit():
    """Complete extraction + RC-3 resolution-incomplete must not manufacture a carrier."""
    recs = [{
        "id": "a" * 64,
        "entry": {
            "coverage": "complete", "deficiency": None, "nativeCause": None,
            "resolutionCompleteness": {"state": "incomplete", "examinedExhaustive": True},
        },
    }]
    summary = M._summarize_coverage_records(recs, {"src/index.ts"}, {"src/index.ts"})
    paired = M._summarize_coverage_records(
        [
            {"id": "a" * 64, "entry": {
                "coverage": "unknown", "deficiency": "budget-exhausted", "nativeCause": None,
                "resolutionCompleteness": {"state": "not-applicable", "examinedExhaustive": False},
            }},
            {"id": "b" * 64, "entry": {
                "coverage": "unknown", "deficiency": "input-closure-incomplete",
                "nativeCause": "lockfile-missing",
                "resolutionCompleteness": {"state": "not-applicable", "examinedExhaustive": False},
            }},
        ],
        set(), set(),
    )
    ok = (
        summary["accountState"] == "complete"
        and summary.get("deficiency") is None
        and summary.get("nativeCause") is None
        and (summary.get("coverageRecords") or [{}])[0].get("resolutionCompletenessState") == "incomplete"
        and (paired.get("coverageRecords") or [{}, {}])[0].get("deficiency") == "budget-exhausted"
        and (paired.get("coverageRecords") or [{}, {}])[0].get("nativeCause") is None
        and (paired.get("coverageRecords") or [{}, {}])[1].get("deficiency") == "input-closure-incomplete"
        and (paired.get("coverageRecords") or [{}, {}])[1].get("nativeCause") == "lockfile-missing"
    )
    if ok:
        return {"result": "ADMIT", "refusals": [], "requiredCellDeficiencies": [],
                "derivedOutcomes": [{"state": "complete"}],
                "derivedAccounts": [summary, paired]}
    return {"result": "REFUSE", "refusals": ["RC3_OR_PAIRING"],
            "requiredCellDeficiencies": [], "derivedOutcomes": [],
            "derivedAccounts": [summary, paired]}


def attach_report(attached):
    adm = attached["admission"]
    refs = attached["evaluationInputRefs"]
    extra = [r for r in refs if r.get("domain") not in (
        "view", "import", "coverage", "subject-inventory",
        "target-attribution", "incoming-search", "candidate-producer-result",
        "execution-inputs",
    )]
    exec_refs = [r for r in refs if r.get("domain") == "execution-inputs"]
    selected = attached["manifest"]["selectedRefs"]
    want_refs = canon_refs(list(selected) + exec_refs)
    selection_ok = M.C.equal_typed(refs, want_refs) and len(exec_refs) == 1
    if extra or not selection_ok:
        return {
            "result": "REFUSE",
            "refusals": (["HELPER_OPAQUE_ROOTS"] if extra else []) + (["HELPER_SELECTION"] if not selection_ok else []),
            "requiredCellDeficiencies": adm.get("requiredCellDeficiencies") or [],
            "derivedOutcomes": adm.get("derivedOutcomes") or [],
            "derivedAccounts": adm.get("derivedAccounts") or [],
        }
    return adm


def owned_hashes():
    names = [
        "execution-inputs.schema.v1.json", "execution-inputs-contract.v1.md",
        "execution_inputs_model.v1.py", "check-execution-inputs.v1.py",
        "execution_inputs_fixture.v3.py",
    ]
    return [{"path": str(HERE / n), "bytes": len((HERE / n).read_bytes()),
             "sha256": hashlib.sha256((HERE / n).read_bytes()).hexdigest()} for n in names]


def main(argv=None):
    receipt_path, hashes_path = output_paths(argv)
    cases = []

    def rec(name, result):
        derived_states = [d.get("state") for d in result.get("derivedOutcomes") or []]
        derived_acc = [d.get("accountState") for d in result.get("derivedAccounts") or []]
        defs = result.get("requiredCellDeficiencies") or []
        cases.append({
            "case": name, "result": result.get("result"),
            "refusals": result.get("refusals"),
            "deficiencyCauses": [d.get("cause") for d in defs],
            "deficiencyRelations": [d.get("relation") for d in defs],
            "deficiencyPairs": [(d.get("deficiency"), d.get("nativeCause")) for d in defs],
            "deficiencyInputRefs": [d.get("inputRefs") for d in defs],
            "derivedOutcomeStates": derived_states,
            "derivedAccountStates": derived_acc,
            "derivedOutcomeDeficiencies": [
                (d.get("deficiency"), d.get("nativeCause")) for d in result.get("derivedOutcomes") or []
            ],
            "derivedSources": [
                [(s.get("source"), s.get("deficiency"), s.get("nativeCause")) for s in (d.get("sources") or [])]
                for d in result.get("derivedOutcomes") or []
            ],
            "coverageRecordPairs": [
                [(r.get("deficiency"), r.get("nativeCause"), (r.get("inputRef") or {}).get("digest"))
                 for r in (a.get("coverageRecords") or [])]
                for a in result.get("derivedAccounts") or []
            ],
            "rowComplete": derived_states == ["complete"] if derived_states else False,
        })

    graph = F.build_file_inputs()
    owner = manifest_from_owner(graph)
    rec("owner-graph-file-positive", admit(owner))

    graph_missing = F.build_file_inputs(complete_required_native=False)
    owner_missing = manifest_from_owner(graph_missing)
    rec("owner-graph-file-missing-required-package", admit(owner_missing))

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

    complete_lie = copy.deepcopy(owner_missing)
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

    rec("expected-source-census-uncovered-is-incomplete", admit(replace_file_view_with_one_subject(owner_missing)))

    rec("rc3-complete-extraction-keeps-native-resolution", rc3_summarize_unit())

    try:
        two_inv = manifest_from_owner(graph_two_partial_inventories())
        rec("two-partial-inventories-distinct-canonical-records", admit(two_inv))
    except Exception as exc:
        rec("two-partial-inventories-distinct-canonical-records",
            {"result": "REFUSE", "refusals": [type(exc).__name__ + ":" + str(exc)]})

    try:
        unav_graph = graph_unavailable_binding_keeps_inventory()
        unav = manifest_from_owner(unav_graph)
        rec("unavailable-binding-budget-keeps-inventory-causes", admit(unav))
        swapped_bind = copy.deepcopy(unav)
        for row in swapped_bind["execution_inputs"]["cellOutcomes"]:
            if row.get("universe") is None:
                row["deficiency"] = "provider-unavailable"
                row["nativeCause"] = None
        rec("unavailable-binding-cause-not-replaced-by-provider-unavailable", admit(swapped_bind))
    except Exception as exc:
        rec("unavailable-binding-budget-keeps-inventory-causes",
            {"result": "REFUSE", "refusals": [type(exc).__name__ + ":" + str(exc)]})
        rec("unavailable-binding-cause-not-replaced-by-provider-unavailable",
            {"result": "REFUSE", "refusals": [type(exc).__name__ + ":" + str(exc)]})

    try:
        attached = H.attach_host_capture(copy.deepcopy(F.build_file_inputs()))
        rec("helper-attach-graph-fixture", attach_report(attached))
        digest0 = attached["digest"]
        hc = attached["manifest"]["hostCapture"]
        attached["graph"]["objects"]["finding3:" + "f" * 64] = ("finding", {"schemaVersion": 2})
        rec("helper-attach-digest-stable-after-outputs", {
            "result": "ADMIT" if (
                attached["graph"]["inputs"]["executionInputsDigest"] == digest0
                and M.raw_digest(attached["manifest"]) == digest0
                and "retainedObjectKeys" not in hc
                and "retainedBlobDigests" not in hc
            ) else "REFUSE",
            "refusals": [] if M.raw_digest(attached["manifest"]) == digest0 else ["HELPER_DIGEST_DRIFT"],
            "requiredCellDeficiencies": [],
            "derivedOutcomes": [{"state": "complete"}] if M.raw_digest(attached["manifest"]) == digest0 else [],
            "derivedAccounts": [],
        })
        domains = {r.get("domain") for r in attached["evaluationInputRefs"]}
        rec("helper-no-policy-schema-roots", {
            "result": "ADMIT" if not ({"policy", "schema", "analysis-spec"} & domains) else "REFUSE",
            "refusals": [] if not ({"policy", "schema", "analysis-spec"} & domains) else ["HELPER_OPAQUE_ROOTS"],
            "requiredCellDeficiencies": attached["admission"].get("requiredCellDeficiencies") or [],
            "derivedOutcomes": attached["admission"].get("derivedOutcomes") or [],
            "derivedAccounts": attached["admission"].get("derivedAccounts") or [],
        })
    except Exception as exc:
        rec("helper-attach-graph-fixture", {"result": "REFUSE", "refusals": [type(exc).__name__ + ":" + str(exc)]})
        rec("helper-attach-digest-stable-after-outputs",
            {"result": "REFUSE", "refusals": [type(exc).__name__ + ":" + str(exc)]})
        rec("helper-no-policy-schema-roots",
            {"result": "REFUSE", "refusals": [type(exc).__name__ + ":" + str(exc)]})

    try:
        many = H.attach_host_capture(copy.deepcopy(F.build_file_inputs(
            multiple_universes=True, complete_required_native=True)))
        rec("helper-attach-three-views-full-required-package", attach_report(many))
    except Exception as exc:
        rec("helper-attach-three-views-full-required-package",
            {"result": "REFUSE", "refusals": [type(exc).__name__ + ":" + str(exc)]})

    try:
        sem = H.attach_host_capture(copy.deepcopy(S.build_ts_semantic_graph(
            atom={"op": "exists", "relation": "references", "minResolution": "resolved-binding", "filters": []},
            subject_kind="symbol", second_partition=True, second_universe=True,
            target_sidecar=True, incoming_search=True, incoming_complete=True,
        )))
        rec("helper-attach-semantic-fixture", attach_report(sem))
    except Exception as exc:
        rec("helper-attach-semantic-fixture",
            {"result": "REFUSE", "refusals": [type(exc).__name__ + ":" + str(exc)]})

    try:
        g_amb = F.build_file_inputs()
        m1, d1 = H.build_manifest(g_amb)
        g_blob = copy.deepcopy(g_amb)
        raw_amb = b"unrelated cached bytes, never selected"
        g_blob["blobs"][hashlib.sha256(raw_amb).hexdigest()] = raw_amb
        m2, d2 = H.build_manifest(g_blob)
        rec("ambient-blob-does-not-change-digest", {
            "result": "ADMIT" if d1 == d2 and m1["selectedRefs"] == m2["selectedRefs"] else "REFUSE",
            "refusals": [] if d1 == d2 else ["AMBIENT_BLOB_DIGEST"],
            "requiredCellDeficiencies": [],
            "derivedOutcomes": [{"state": "complete"}] if d1 == d2 else [],
            "derivedAccounts": [],
        })
        g_obj = copy.deepcopy(g_amb)
        g_obj["objects"]["finding3:" + "0" * 64] = ("finding", {"schemaVersion": 2})
        m3, d3 = H.build_manifest(g_obj)
        rec("ambient-object-does-not-change-digest", {
            "result": "ADMIT" if d1 == d3 and m1["selectedRefs"] == m3["selectedRefs"] else "REFUSE",
            "refusals": [] if d1 == d3 else ["AMBIENT_OBJECT_DIGEST"],
            "requiredCellDeficiencies": [],
            "derivedOutcomes": [{"state": "complete"}] if d1 == d3 else [],
            "derivedAccounts": [],
        })
        mutated = copy.deepcopy(m1)
        mutated["selectedRefs"] = [r for r in mutated["selectedRefs"] if r.get("domain") != "coverage"]
        rec("selected-refs-change-changes-digest", {
            "result": "ADMIT" if M.raw_digest(mutated) != d1 and mutated["selectedRefs"] != m1["selectedRefs"] else "REFUSE",
            "refusals": [] if M.raw_digest(mutated) != d1 else ["SELECTED_DIGEST_UNCHANGED"],
            "requiredCellDeficiencies": [],
            "derivedOutcomes": [{"state": "complete"}] if M.raw_digest(mutated) != d1 else [],
            "derivedAccounts": [],
        })
        att = H.attach_host_capture(copy.deepcopy(g_amb))
        op1 = att["operationalCapture"]
        att["graph"]["blobs"][hashlib.sha256(raw_amb).hexdigest()] = raw_amb
        op2 = H.operational_capture(att["graph"], att["manifest"], exclude_blob=att["digest"])
        rec("operational-receipt-may-vary-without-run-identity", {
            "result": "ADMIT" if (
                att["digest"] == d1
                and M.raw_digest(att["manifest"]) == d1
                and op1["availableBlobDigests"] != op2["availableBlobDigests"]
                and "retainedObjectKeys" not in att["manifest"]["hostCapture"]
            ) else "REFUSE",
            "refusals": [] if att["digest"] == d1 else ["OPERATIONAL_COUPLED"],
            "requiredCellDeficiencies": [],
            "derivedOutcomes": [{"state": "complete"}] if att["digest"] == d1 else [],
            "derivedAccounts": [],
        })
    except Exception as exc:
        rec("ambient-blob-does-not-change-digest",
            {"result": "REFUSE", "refusals": [type(exc).__name__ + ":" + str(exc)]})
        rec("ambient-object-does-not-change-digest",
            {"result": "REFUSE", "refusals": [type(exc).__name__ + ":" + str(exc)]})
        rec("selected-refs-change-changes-digest",
            {"result": "REFUSE", "refusals": [type(exc).__name__ + ":" + str(exc)]})
        rec("operational-receipt-may-vary-without-run-identity",
            {"result": "REFUSE", "refusals": [type(exc).__name__ + ":" + str(exc)]})

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
        "owner-graph-file-missing-required-package": "ADMIT",
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
        "rc3-complete-extraction-keeps-native-resolution": "ADMIT",
        "two-partial-inventories-distinct-canonical-records": "ADMIT",
        "unavailable-binding-budget-keeps-inventory-causes": "ADMIT",
        "unavailable-binding-cause-not-replaced-by-provider-unavailable": "REFUSE",
        "helper-attach-graph-fixture": "ADMIT",
        "helper-attach-digest-stable-after-outputs": "ADMIT",
        "helper-no-policy-schema-roots": "ADMIT",
        "helper-attach-three-views-full-required-package": "ADMIT",
        "helper-attach-semantic-fixture": "ADMIT",
        "ambient-blob-does-not-change-digest": "ADMIT",
        "ambient-object-does-not-change-digest": "ADMIT",
        "selected-refs-change-changes-digest": "ADMIT",
        "operational-receipt-may-vary-without-run-identity": "ADMIT",
    }
    mismatches = []
    for c in cases:
        exp = want.get(c["case"])
        if exp and c["result"] != exp:
            mismatches.append({"case": c["case"], "got": c["result"], "want": exp,
                               "refusals": c.get("refusals"), "deficiencies": c.get("deficiencyCauses")})
    owner0 = cases[0] if cases else {}
    oracles = []
    missing_pkg = next((c for c in cases if c["case"] == "owner-graph-file-missing-required-package"), None)
    if missing_pkg and missing_pkg.get("result") == "ADMIT":
        if missing_pkg.get("rowComplete"):
            oracles.append({"oracle": "complete-required-native-false-must-not-be-complete",
                            "got": missing_pkg.get("derivedOutcomeStates")})
        if "native-work-incomplete" not in (missing_pkg.get("deficiencyCauses") or []):
            oracles.append({"oracle": "missing-package-work-must-be-described",
                            "got": missing_pkg.get("deficiencyCauses")})
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
    ptr_case = next((c for c in cases if c["case"] == "missing-inventory-pointer"), None)
    if ptr_case and ptr_case.get("result") == "REFUSE":
        if "EXECUTION_INPUTS_REF_POINTER" not in (ptr_case.get("refusals") or []):
            oracles.append({"oracle": "pointer-omission-must-be-ref-pointer",
                            "got": ptr_case.get("refusals")})
    lost_case = next((c for c in cases if c["case"] == "lost-inventory-bytes"), None)
    if lost_case and lost_case.get("result") == "REFUSE":
        if "EXECUTION_INPUTS_REF_LOST_BYTES" not in (lost_case.get("refusals") or []):
            oracles.append({"oracle": "promised-bytes-loss-must-be-lost-bytes",
                            "got": lost_case.get("refusals")})
    corrupt_case = next((c for c in cases if c["case"] == "invalid-blob-hash"), None)
    if corrupt_case and corrupt_case.get("result") == "REFUSE":
        if "EXECUTION_INPUTS_REF_INVALID_BYTES" not in (corrupt_case.get("refusals") or []):
            oracles.append({"oracle": "corrupt-supplied-bytes-must-be-invalid-bytes",
                            "got": corrupt_case.get("refusals")})
    census = next((c for c in cases if c["case"] == "expected-source-census-uncovered-is-incomplete"), None)
    if census and census.get("result") == "ADMIT" and (census.get("derivedAccountStates") or [None])[0] == "complete":
        oracles.append({"oracle": "subset-complete-coverage-must-not-complete-file-account",
                        "got": census.get("derivedAccountStates")})
    partial_case = next((c for c in cases if c["case"] == "partial-inventory-known-rows"), None)
    if partial_case and partial_case.get("result") == "ADMIT":
        if "required-cell-unsatisfied" not in (partial_case.get("deficiencyCauses") or []):
            oracles.append({"oracle": "required-partial-inventory-must-emit-required-cell-deficiency",
                            "got": partial_case.get("deficiencyCauses")})
    mixed_pairs = mixed_case.get("coverageRecordPairs") if mixed_case else None
    if mixed_case and mixed_case.get("result") == "ADMIT":
        file_recs = [pair for group in (mixed_pairs or []) for pair in group]
        file_ids = {p[2] for p in file_recs if p[2]}
        if len(file_ids) < 2:
            oracles.append({"oracle": "two-coverage-same-relation-must-retain-both-coordinates",
                            "got": mixed_pairs})
    two_inv_case = next((c for c in cases if c["case"] == "two-partial-inventories-distinct-canonical-records"), None)
    if two_inv_case and two_inv_case.get("result") == "ADMIT":
        inv_refs = []
        for refs in two_inv_case.get("deficiencyInputRefs") or []:
            for r in refs or []:
                if r.get("domain") == "subject-inventory":
                    inv_refs.append((r.get("digest"),))
        pairs = two_inv_case.get("deficiencyPairs") or []
        defs = {p[0] for p in pairs if p[0]}
        if len({r[0] for r in inv_refs}) < 2 or not (
            "budget-exhausted" in defs and "input-closure-incomplete" in defs
        ):
            oracles.append({"oracle": "two-partial-inventories-must-retain-both-causes-and-coordinates",
                            "got": {"pairs": pairs, "invRefs": inv_refs}})
    unav_case = next((c for c in cases if c["case"] == "unavailable-binding-budget-keeps-inventory-causes"), None)
    if unav_case and unav_case.get("result") == "ADMIT":
        sources = [s for group in (unav_case.get("derivedSources") or []) for s in group]
        has_inv = any(s[0] == "inventory" for s in sources)
        has_bind = any(s[0] in ("binding", "enumerator") and s[1] == "input-closure-incomplete" for s in sources)
        host_pairs = unav_case.get("derivedOutcomeDeficiencies") or []
        if any(p[0] == "provider-unavailable" and p[1] is None for p in host_pairs if p[0]) and not has_bind:
            oracles.append({"oracle": "null-universe-must-not-wipe-to-provider-unavailable",
                            "got": {"sources": sources, "host": host_pairs}})
        if not has_inv or not has_bind:
            oracles.append({"oracle": "null-universe-must-retain-binding-and-inventory-causes",
                            "got": sources})
    mismatches.extend({"case": o["oracle"], "got": "ORACLE", "want": "HOLD", "refusals": [str(o["got"])]} for o in oracles)

    report = {
        "standing": "execution-inputs join checks; owner-graph from evaluator_graph_fixture.v3.py plus execution_inputs_fixture.v3.py; not a Run; does not overwrite grok-execution-inputs.v1/v2/v3/v4/v5; does not relabel check-replay.v3.py.",
        "hostTcbHonesty": "sealed replay trusts host-captured stage-return inventory; cannot certify malicious host omissions",
        "causeRetention": "derivedAccounts[].coverageRecords retain each Coverage deficiency+nativeCause+inputRef together; requiredCellDeficiencies is canonical-record unique",
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
