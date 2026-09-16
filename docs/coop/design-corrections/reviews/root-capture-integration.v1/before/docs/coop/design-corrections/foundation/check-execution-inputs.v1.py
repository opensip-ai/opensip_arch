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
# Full retained-Run driver for the bridge controls. Same route check-execution-replay.v3.py uses;
# no new admission path is introduced here, and no consumer helper is imported.
_rspec = importlib.util.spec_from_file_location("exec_in_replay3", HERE / "evaluator_replay_model.v3.py")
R = importlib.util.module_from_spec(_rspec)
_rspec.loader.exec_module(R)
IDENTITY = R.M

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


def rebuild_after_object_mutation(owner, objects, blobs, extra_view_ids=None, view_ids=None):
    """Rebuild selectedRefs/receipts/accounts after checker-only object mints.

    `view_ids` REPLACES the default "every minted view object" set, for a control that must
    retire a view rather than add one.

    STANDING, stated correctly: the rebuild goes through the shared host-capture builder, and that
    builder is NOT independent of the admission model. `execution_inputs_fixture.v3.py` calls
    `M.derived_applicability`, `M._summarize_coverage_records` and `M.derive_outcome` to produce
    the very rows admission then re-derives. So an ADMIT here is REFERENCE SELF-CONSISTENCY plus
    the explicit oracles below, not an independent reconstruction of the host rows. The
    independent consumer reconstruction that a real acceptance needs is a separate obligation and
    is not what any control in this file provides.
    """
    if view_ids is None:
        view_ids = [k for k, (dom, _) in objects.items() if dom == "view"]
    if extra_view_ids:
        view_ids = M.canon_str_list(list(dict.fromkeys(view_ids + extra_view_ids)))
    snap_id = owner["plan"]["snapshotId"]
    snapshot = objects[snap_id][1] if snap_id in objects else owner["objects"][snap_id][1]
    # build_manifest re-adds any view named on the carried refs, so a retired view must be
    # dropped from them too or it walks straight back into the rebuilt manifest.
    keep_view_hexes = {hx(v) for v in view_ids}
    carried = [
        r for r in (owner["execution_inputs"].get("selectedRefs") or [])
        if r.get("domain") != "view" or r.get("digest") in keep_view_hexes
    ]
    graphish = {
        "objects": objects, "blobs": blobs,
        "inputs": {
            "planId": owner["plan_id"], "executionPlanId": owner["execution_plan_id"],
            "evaluatorClosure": owner["execution_inputs"]["evaluatorClosure"],
            "evaluationInputRefs": carried,
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
    # `schemaDigests` is x-opensip-order: canonical-set, so its ORDER IS CONTENT, never role.
    # Positional unpacking was only correct for the accidental digest values of one frozen
    # revision: any registered document whose digest re-sorts the pair silently swaps the two.
    # Select the coverage document by its registered identity instead of by position.
    cov_schema = H.N.schema_document_digest(H.N.NATIVE_SCHEMA_DOC)
    rel_schema = next(d for d in existing_view["schemaDigests"] if d != cov_schema)
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
    # `schemaDigests` is x-opensip-order: canonical-set, so its ORDER IS CONTENT, never role.
    # Positional unpacking was only correct for the accidental digest values of one frozen
    # revision: any registered document whose digest re-sorts the pair silently swaps the two.
    # Select the coverage document by its registered identity instead of by position.
    cov_schema = H.N.schema_document_digest(H.N.NATIVE_SCHEMA_DOC)
    rel_schema = next(d for d in existing_view["schemaDigests"] if d != cov_schema)
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


def replace_file_view_with_one_subject(owner, complete=True, rebuild=False):
    """Returned Coverage over one path while file inventory still names all paths.

    `complete=True` is the pure-census shape: the returned partition is honestly complete over
    what it committed to and carries NO pair, so the account's only incompleteness is the missing
    expected subjects. `complete=False` returns an `unknown` partition, so the SAME census failure
    now sits beside a real typed native carrier, which must survive as the primary pair.
    """
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
    # `schemaDigests` is x-opensip-order: canonical-set, so its ORDER IS CONTENT, never role.
    # Positional unpacking was only correct for the accidental digest values of one frozen
    # revision: any registered document whose digest re-sorts the pair silently swaps the two.
    # Select the coverage document by its registered identity instead of by position.
    cov_schema = H.N.schema_document_digest(H.N.NATIVE_SCHEMA_DOC)
    rel_schema = next(d for d in existing_view["schemaDigests"] if d != cov_schema)
    scope = {
        "snapshotId": snapshot_id, "sourceUniverse": uni, "targetUniverse": uni,
        "relation": "file", "resolution": "enumerated",
        "enumeratorClosure": provider, "subjects": ["README.md"],
    }
    scope_id = _mint(objects, "subject-scope", scope)
    paths = [r["path"] for r in objects[snapshot_id][1]["sourceInventory"]]
    payload = H.coverage_result(objects[scope_id][1], uni, complete, blobs, paths)
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
    if rebuild:
        # Retire every view built on the ORIGINAL full file scope and keep this subset one, then
        # let the shared builder derive the host rows for the mutated object graph.
        old_file_scopes = {
            k for k, (dom, v) in objects.items()
            if dom == "subject-scope" and v.get("relation") == "file" and k != scope_id
        }
        keep = [
            k for k, (dom, v) in objects.items()
            if dom == "view" and not (set(v.get("scopeIds") or []) & old_file_scopes)
        ]
        return rebuild_after_object_mutation(
            owner, objects, blobs, view_ids=M.canon_str_list(list(dict.fromkeys(keep + [view_id]))))
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
    # STANDING `helper-unit`: this calls `_summarize_coverage_records` directly. `derivedAccounts`
    # below are that helper's REAL output; the cell/Run columns are not applicable and stay null.
    return {"controlStanding": "helper-unit",
            "result": "ADMIT" if ok else "REFUSE",
            "refusals": [] if ok else ["RC3_OR_PAIRING"],
            "derivedAccounts": [summary, paired]}


def applicability_precedence_table():
    """Exhaustive FIRST-MATCH table, including the branch intersections.

    STANDING `helper-unit`: this calls `M.derived_applicability` and reads two published tables.
    It admits nothing and closes no Run, so the admission columns are NOT APPLICABLE and are
    reported as null rather than as an invented complete cell.

    Only LAWFUL binding shapes are exercised. `enumeration-contract.v1.md` §1 refuses a non-null
    universe on an unselected enumerator, so every `unselected` row here carries `universe=null`;
    no shape is invented to reach a branch. The intersections are the point: VCS-none over
    everything, matrix-unsupported over both unavailable tokens, and unselected over null-U.
    """
    U = "a" * 64
    rows = [
        # (name, rel, uni, enumerator, matrix, vcsKind, expected)
        ("vcs-none-over-unsupported-unselected-null", "vcs-change", None, "unselected", "UNSUPPORTED-TYPED", "none", "inapplicable-vcs"),
        ("vcs-none-over-supported-selected-u", "vcs-change", U, "selected", "SUPPORTED-DESIGN", "none", "inapplicable-vcs"),
        ("vcs-reported-is-supported", "vcs-change", U, "selected", "SUPPORTED-DESIGN", "git", "supported-available"),
        ("unsupported-over-unselected-and-null", "references", None, "unselected", "UNSUPPORTED-TYPED", "git", "unsupported-typed"),
        ("unsupported-over-null-universe", "references", None, "selected", "UNSUPPORTED-TYPED", "git", "unsupported-typed"),
        ("unsupported-at-selected-u", "references", U, "selected", "UNSUPPORTED-TYPED", "git", "unsupported-typed"),
        ("unselected-over-null-universe", "file", None, "unselected", "SUPPORTED-DESIGN", "git", "unavailable-unselected"),
        ("selected-null-universe", "file", None, "selected", "SUPPORTED-DESIGN", "git", "unavailable-null-universe"),
        ("selected-u-supported", "file", U, "selected", "SUPPORTED-DESIGN", "git", "supported-available"),
        # A non-vcs relation on a repository with no VCS is NOT inapplicable-vcs.
        ("vcs-none-does-not-touch-other-relations", "file", U, "selected", "SUPPORTED-DESIGN", "none", "supported-available"),
    ]
    got, bad = [], []
    for name, rel, uni, en, matrix, vcs, want in rows:
        token = M.derived_applicability(rel, uni, en, matrix, vcs)
        got.append({"case": name, "want": want, "got": token})
        if token != want:
            bad.append({"case": name, "want": want, "got": token})
    # The published order must be exactly what the reference walks.
    published = [t for t, _why in M.APPLICABILITY_PRECEDENCE]
    want_published = [
        "inapplicable-vcs", "unsupported-typed", "unavailable-unselected",
        "unavailable-null-universe", "supported-available",
    ]
    if published != want_published:
        bad.append({"case": "published-order", "want": want_published, "got": published})
    schema_order = [
        r["token"] for r in
        M.SCHEMA["$defs"]["NativeCoverageAccountV1"]["x-opensip-applicability-precedence"]["order"]
    ]
    if schema_order != want_published:
        bad.append({"case": "schema-annotation-order", "want": want_published, "got": schema_order})
    return {
        "controlStanding": "helper-unit",
        "result": "REFUSE" if bad else "ADMIT",
        "refusals": [str(b) for b in bad],
        "precedenceTable": got,
    }


def set_account_source_universe(owner, predicate, value):
    """Host-side mutation of one account's sourceUniverse; everything else stays lawful."""
    mutated = copy.deepcopy(owner)
    hit = False
    for a in mutated["execution_inputs"]["nativeCoverageAccounts"]:
        if predicate(a):
            a["sourceUniverse"] = value
            hit = True
    if not hit:
        raise RuntimeError("no account matched the source-universe mutation predicate")
    return mutated


def set_account_target_universe(owner, predicate, value):
    """Host-side mutation of one account's targetUniverse. §5 fixes it to null."""
    mutated = copy.deepcopy(owner)
    hit = False
    for a in mutated["execution_inputs"]["nativeCoverageAccounts"]:
        if predicate(a):
            a["targetUniverse"] = value
            hit = True
    if not hit:
        raise RuntimeError("no account matched the target-universe mutation predicate")
    return mutated


def candidate_cell_without_envelope(owner, required):
    """A candidate-only cell whose binding is SELECTED at a non-null universe and which retains
    NO CandidateProducerResultV1 at all.

    `AvailableProgramBindingV1` has no `deficiency`/`nativeCause` property (`additionalProperties:
    false`), so the binding declares no carrier; the candidate item therefore has no source pair
    of any kind and must derive (null, null). `required=True` is expected to refuse
    `EXECUTION_INPUTS_CANDIDATE_REQUIRED` before that matters.

    Bounded ExecutionInputs join fixture only: the changed Plan/analysis-spec is not reminted
    through structural closure here. This function is not a full-Run reachability control.
    """
    kw = copy.deepcopy(owner)
    prov = next(k for k, v in kw["closures"].items() if v.get("kind") == "provider")
    base_binding = kw["enumeration_plan"]["cells"][0]["programBindings"][0]
    uni = base_binding["universe"]
    enum = copy.deepcopy(kw["enumeration_plan"])
    enum["cells"] = [{
        "capabilityId": "clones-near", "languageMode": "syntax-only", "workspaceRoot": ".",
        "required": required, "kinds": [],
        "programBindings": [{
            "ordinal": 0, "provenance": "default-unit",
            "enumerator": {"status": "selected", "closureId": prov},
            "nativeContextDigest": base_binding["nativeContextDigest"],
            "universe": uni, "programEntry": None, "extents": [],
            "candidateSourcePaths": ["src/index.ts"],
        }],
    }]
    spec = {"requestedCapabilities": [{"capabilityId": "clones-near", "languageMode": "syntax-only",
                                       "workspaceRoot": ".", "required": required}]}
    plan = dict(kw["plan"])
    plan["analysisSpecDigest"] = M.raw_digest(spec)
    stage_d = kw["execution_plan"]["stages"][0]["stageSpecDigest"]
    row = {
        "ordinal": 0, "cellOrdinal": 0, "programOrdinal": 0, "capabilityId": "clones-near",
        "languageMode": "syntax-only", "workspaceRoot": ".", "required": required, "kinds": [],
        "universe": uni, "enumeratorStatus": "selected", "enumeratorClosure": prov,
        "state": "unavailable", "deficiency": None, "nativeCause": None,
        "stageOrdinal": 0, "stageOrdinalNullReason": None,
        "inventoryDigests": [], "viewDigests": [], "candidateResultDigest": None,
    }
    manifest = {
        "schemaVersion": 1, "planId": kw["plan_id"], "executionPlanId": kw["execution_plan_id"],
        "evaluatorClosure": kw["execution_inputs"]["evaluatorClosure"],
        "enumerationPlanDigest": M.raw_digest(enum), "analysisSpecDigest": plan["analysisSpecDigest"],
        "hostCapture": {
            "custody": "host-tcb-evidence-store", "observation": "stage-return",
            "stageReceipts": [{
                "ordinal": 0, "stageSpecDigest": stage_d,
                "producerClosure": kw["stage_specs"][stage_d]["producerClosure"],
                "outputDomains": list(kw["stage_specs"][stage_d]["outputDomains"]),
                "outputRefs": [], "state": "complete", "unavailableReason": None,
            }],
            "hostDerivedRefs": [],
        },
        "selectedRefs": [], "cellOutcomes": [row], "nativeCoverageAccounts": [],
        "candidateResultRefs": [],
    }
    return {
        "plan_id": kw["plan_id"], "plan": plan, "execution_plan_id": kw["execution_plan_id"],
        "execution_plan": kw["execution_plan"], "enumeration_plan": enum, "analysis_spec": spec,
        "execution_inputs": manifest, "objects": kw["objects"], "blobs": kw["blobs"],
        "store_pointers": pointers_of(kw["objects"], kw["blobs"]), "inventories": {},
        "imports": {}, "target_attributions": {}, "incoming_searches": {},
        "candidate_results": {}, "groups": {}, "closures": kw["closures"],
        "stage_specs": kw["stage_specs"], "vcs_observation": kw["vcs_observation"],
    }


def claim_row_pair(owner, deficiency, native_cause):
    """Host claims a carrier on every non-complete cell row. Used to prove that a manufactured
    `provider-unavailable` is REFUSED where the derivation carries null/null."""
    mutated = copy.deepcopy(owner)
    for row in mutated["execution_inputs"]["cellOutcomes"]:
        if row["state"] != "complete":
            row["deficiency"] = deficiency
            row["nativeCause"] = native_cause
    return mutated


def full_run(graph):
    """Owner ADMIT -> R.derive -> seal -> M.close_run, exactly as check-execution-replay.v3.py."""
    seed, objects, blobs, _ = F.seal_fixture(graph)
    _, owner = IDENTITY.open_run_closure(seed, objects, blobs)
    i = graph["inputs"]
    out = R.derive(i["planId"], i["executionPlanId"], i["evaluatorClosure"],
                   i["evaluationInputRefs"], objects, blobs, owner)
    run, objects, blobs = S.seal_derived(graph, out, objects, blobs)
    result = R.replay(run, objects, blobs)
    closed = IDENTITY.close_run(run, objects, blobs)
    if closed != result["runId"]:
        raise RuntimeError("close_run runId mismatch: " + str((closed, result["runId"])))
    return result, out["proof"]


NONE_ATOM = {"op": "none", "relation": "file", "minResolution": "enumerated", "filters": []}


def bridge_cause(deficiency):
    """Composition §9.6 step 3, as `evaluator_input_model.v3.py` implements it."""
    registered = IDENTITY.SCHEMA["x-opensip-evaluator-deficiency-registry"]["sources"]["execution"]
    if deficiency in registered:
        return deficiency
    if deficiency in (None, "source-syntax-invalid"):
        return "required-cell-unsatisfied"
    return "UNREGISTERED:" + str(deficiency)


def full_run_case(label, want_verdict, want_causes, **kwargs):
    """One closed Run, reported with REAL rows.

    STANDING `closed-run`. The proof columns are the actual closed Run's. The admission columns
    are the SAME graph's `admit_execution_inputs` result -- the very call the Run performs
    internally through `evaluator_input_model.execution_input_account`, re-run here only because
    `R.derive` does not return it. They are NOT a relabelling of proof success: an execution cell
    that is `partial` is reported as `partial`, and `requiredCellDeficiencies` are the real rows.
    The separately rebuilt reference fixture must produce the exact ExecutionInputs digest
    named by the closed proof. This byte binding identifies the admission columns with that
    Run; bridging their causes with §9.6 adds a separate projection check. Both builders reuse
    the reference model and this remains reference self-consistency, not a blind reconstruction.
    """
    try:
        graph = F.build_file_inputs(atom_override=NONE_ATOM, **kwargs)
        result, proof = full_run(graph)
        admission_inputs = manifest_from_owner(F.build_file_inputs(atom_override=NONE_ATOM, **kwargs))
        admission = admit(admission_inputs)
        admission_digest = M.raw_digest(admission_inputs["execution_inputs"])
    except Exception as exc:  # noqa: BLE001
        return {"controlStanding": "closed-run", "result": "REFUSE",
                "refusals": [type(exc).__name__ + ":" + str(exc)]}
    causes = sorted(d["cause"] for d in proof["executionDeficiencies"])
    pairs = sorted((d["cause"], d["nativeCause"]) for d in proof["executionDeficiencies"])
    bridged = sorted(bridge_cause(d.get("deficiency"))
                     for d in admission.get("requiredCellDeficiencies") or [])
    bad = []
    if admission_digest != proof["executionInputsDigest"]:
        bad.append({"executionInputsDigestMismatch": {"admission": admission_digest,
                    "proof": proof["executionInputsDigest"]}})
    if result["verdict"] != want_verdict:
        bad.append({"verdict": result["verdict"], "want": want_verdict})
    if causes != sorted(want_causes):
        bad.append({"causes": causes, "want": sorted(want_causes)})
    if any(d["cause"] == "provider-unavailable" for d in proof["executionDeficiencies"]):
        bad.append({"fabricatedCarrier": "provider-unavailable reached the proof"})
    if sorted(set(bridged)) != sorted(set(causes)):
        bad.append({"bridgedCausesEqualProof": False, "bridged": bridged, "proof": causes})
    if admission.get("result") != "ADMIT":
        bad.append({"sameGraphAdmission": admission.get("result"),
                    "refusals": admission.get("refusals")})
    return {
        "controlStanding": "closed-run",
        "result": "REFUSE" if bad else "ADMIT",
        "refusals": [str(b) for b in bad],
        # Real admission rows for the same graph, not invented ones.
        "requiredCellDeficiencies": admission.get("requiredCellDeficiencies") or [],
        "derivedOutcomes": admission.get("derivedOutcomes") or [],
        "derivedAccounts": admission.get("derivedAccounts") or [],
        "fullRun": {
            "case": label, "verdict": result["verdict"], "runId": result["runId"],
            "executionCausePairs": pairs,
            "executionInputRefs": [
                [(r["domain"], r["digest"]) for r in d["inputRefs"]]
                for d in proof["executionDeficiencies"]
            ],
            "sameGraphAdmissionResult": admission.get("result"),
            "sameGraphExecutionInputsDigest": admission_digest,
            "proofExecutionInputsDigest": proof["executionInputsDigest"],
            "sameGraphCellStates": [d.get("state") for d in admission.get("derivedOutcomes") or []],
            "bridgedCausesFromAdmission": bridged,
            "admissionColumnProvenance":
                "admit_execution_inputs on the same graph; the Run performs this same call via "
                "evaluator_input_model.execution_input_account but does not return it.",
        },
    }


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


_VA_NATIVE = []


def view_attribution_world(build_kwargs, mutate):
    """Checker-only world for contract §3 "View attribution".

    Starts from the maintained owner fixture with the full-run atom, then lets `mutate` mint
    subject-scopes, native-owner-admitted Coverage and views on the graph's OWN store and return
    `(retire, add)` view ids, which are applied to the graph's own view census and evaluation refs.
    Nothing about attribution is asserted here: the shared host-capture builder derives the rows
    and admission re-derives them. Symbol-row worlds are deliberately not used: their unmutated
    graphs do not close a Run (`PAYLOAD_RECORD:#/$defs/DeclaresPayloadV1`), which would leave every
    closed-run column blind.
    """
    if not _VA_NATIVE:
        _VA_NATIVE.append(F.fixture_helpers())
    NH = _VA_NATIVE[0]
    cov_schema = NH.N.schema_document_digest(NH.N.NATIVE_SCHEMA_DOC)
    graph = F.build_file_inputs(atom_override=NONE_ATOM, **build_kwargs)
    objects, blobs = graph["objects"], graph["blobs"]
    first = objects[graph["viewIds"][0]][1]
    provider = first["producerClosure"]
    rel_schema = next(d for d in first["schemaDigests"] if d != cov_schema)
    paths = [r["path"] for r in graph["snapshot"]["sourceInventory"]]

    def scope(relation, resolution, uni):
        return _mint(objects, "subject-scope", {
            "snapshotId": graph["inputs"]["plan"]["snapshotId"], "sourceUniverse": uni,
            "targetUniverse": uni, "relation": relation, "resolution": resolution,
            "enumeratorClosure": provider, "subjects": [],
        })

    def coverage(scope_id, uni):
        payload = NH.coverage_result(objects[scope_id][1], uni, True, blobs, paths)
        admitted = NH.N.admit_coverage_result_v3(payload, objects[scope_id][1], [], cov_schema)
        if admitted.get("result") != "ADMIT":
            raise RuntimeError("view-attribution coverage not admitted: " + str(admitted))
        return _mint(objects, "coverage", {"scopeId": scope_id, "payloadSchemaDigest": cov_schema,
                                           "payloadDigest": _blob(blobs, payload)})

    def view(scope_ids, facts=(), coverage_ids=()):
        return _mint(objects, "view", {
            "planId": graph["inputs"]["planId"], "scopeIds": M.canon_str_list(list(scope_ids)),
            "facts": M.canon_str_list(list(facts)), "coverageIds": M.canon_str_list(list(coverage_ids)),
            "producerClosure": provider, "schemaDigests": M.canon_str_list([rel_schema, cov_schema]),
        })

    def single(relation, uni):
        return next(k for k in graph["viewIds"]
                    if [(objects[s][1]["relation"], objects[s][1]["sourceUniverse"])
                        for s in objects[k][1]["scopeIds"]] == [(relation, uni)])

    universes = {}
    for cell in graph["enumerationPlan"]["cells"]:
        for b in cell["programBindings"]:
            universes.setdefault(cell["capabilityId"], []).append(b["universe"])
    retire, add = mutate({"scope": scope, "coverage": coverage, "view": view, "single": single,
                          "universes": universes, "objects": objects})
    retire, add = set(retire), list(add)
    graph["viewIds"] = M.canon_str_list([v for v in graph["viewIds"] if v not in retire] + add)
    refs = [r for r in graph["inputs"]["evaluationInputRefs"]
            if not (r["domain"] == "view" and "view2:" + r["digest"] in retire)]
    graph["inputs"]["evaluationInputRefs"] = canon_refs(refs + [{"domain": "view", "digest": hx(a)} for a in add])
    kept = [objects[v][1] for v in graph["viewIds"]]
    graph["coverageIds"] = M.canon_str_list([c for v in kept for c in v["coverageIds"]])
    graph["scopeIds"] = M.canon_str_list([s for v in kept for s in v["scopeIds"]])
    graph["inputs"]["coverageCount"] = len(graph["coverageIds"])
    if graph.get("viewId") in retire:
        graph["viewId"] = add[0]
    return graph, add


def view_attribution_case(graph, *, row_edit=None, capture=(), closed=True):
    """Admission over the shared builder's rows (optionally host-edited), plus the SAME manifest through
    the maintained `full_run` driver when `closed`.

    `capture` adds captured-but-unattributed views, with their Coverage, to the complete view
    receipt and selectedRefs; the shared builder never does that because it captures attributed
    views only. `row_edit` rewrites host `cellOutcomes` rows. An edited manifest is hashed into
    the Run graph exactly as `attach_host_capture` does, so the closed-run column is that manifest.
    """
    kw = manifest_from_owner(copy.deepcopy(graph))
    ei = kw["execution_inputs"]
    edited = bool(capture) or row_edit is not None
    for vid in capture:
        view = kw["objects"][vid][1]
        for rc in ei["hostCapture"]["stageReceipts"]:
            if "view" in rc["outputDomains"]:
                rc["outputRefs"] = canon_refs(rc["outputRefs"] + [{"domain": "view", "digest": hx(vid)}])
        ei["selectedRefs"] = canon_refs(ei["selectedRefs"] + [{"domain": "view", "digest": hx(vid)}]
                                        + [{"domain": "coverage", "digest": hx(c)} for c in view["coverageIds"]])
    if row_edit is not None:
        row_edit(ei["cellOutcomes"])
    if edited:
        kw["store_pointers"] = M.promised_pointers(
            ei, kw["plan"], kw["execution_plan"], kw["enumeration_plan"],
            objects=kw["objects"], blobs=kw["blobs"])["store_pointers"]
    result = dict(admit(kw))
    result["viewDigestsByRow"] = {r["capabilityId"] + "#" + str(r["programOrdinal"]): list(r["viewDigests"])
                                  for r in ei["cellOutcomes"]}
    if closed:
        run_graph = copy.deepcopy(graph)
        if edited:
            digest = M.raw_digest(ei)
            run_graph["blobs"][digest] = M.C.canonical(ei)
            run_graph["inputs"]["executionInputsDigest"] = digest
            run_graph["inputs"]["evaluationInputRefs"] = canon_refs(
                list(ei["selectedRefs"]) + [{"domain": "execution-inputs", "digest": digest}])
            run_graph["executionInputs"] = ei
            run_graph["executionInputsDigest"] = digest
        try:
            run_result, proof = full_run(run_graph)
            result["fullRun"] = {"verdict": run_result["verdict"], "runId": run_result["runId"],
                                 "sameManifest": proof["executionInputsDigest"] == M.raw_digest(ei)}
        except Exception as exc:  # noqa: BLE001
            result["fullRun"] = {"refused": type(exc).__name__ + ":" + str(exc)}
        result["controlStanding"] = "closed-run"
    return result


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
        # STANDING decides whether the admission columns MEAN anything for this control.
        #   admission  - a real admit_execution_inputs result; every derived* column is real.
        #   closed-run - a real M.close_run plus that same graph's real admission rows.
        #   helper-unit / schema-unit - a pure helper or schema check that admits nothing and
        #                closes no Run. Its admission columns are NOT APPLICABLE and are reported
        #                as null. They are never filled with an invented complete cell.
        # NOTE: the admission result carries its OWN `standing` string, so the control standing
        # uses a distinct key that cannot collide with it.
        standing = result.get("controlStanding") or "admission"
        bears_admission = standing in ("admission", "closed-run")
        derived_states = [d.get("state") for d in result.get("derivedOutcomes") or []]
        derived_acc = [d.get("accountState") for d in result.get("derivedAccounts") or []]
        defs = result.get("requiredCellDeficiencies") or []
        na = not bears_admission
        cases.append({
            "case": name, "controlStanding": standing, "result": result.get("result"),
            "refusals": result.get("refusals"),
            "deficiencyCauses": None if na else [d.get("cause") for d in defs],
            "deficiencyRelations": None if na else [d.get("relation") for d in defs],
            "deficiencyPairs": None if na else [(d.get("deficiency"), d.get("nativeCause")) for d in defs],
            "deficiencyInputRefs": None if na else [d.get("inputRefs") for d in defs],
            "derivedOutcomeStates": None if na else derived_states,
            "derivedAccountStates": None if na else derived_acc,
            "derivedOutcomeDeficiencies": None if na else [
                (d.get("deficiency"), d.get("nativeCause")) for d in result.get("derivedOutcomes") or []
            ],
            "derivedSources": None if na else [
                [(s.get("source"), s.get("deficiency"), s.get("nativeCause")) for s in (d.get("sources") or [])]
                for d in result.get("derivedOutcomes") or []
            ],
            # derivedAccounts may carry REAL helper output on a helper-unit control (the RC-3
            # summariser returns actual summaries), so this column is kept when present.
            "coverageRecordPairs": [
                [(r.get("deficiency"), r.get("nativeCause"), (r.get("inputRef") or {}).get("digest"))
                 for r in (a.get("coverageRecords") or [])]
                for a in result.get("derivedAccounts") or []
            ] or None,
            "rowComplete": None if na else (derived_states == ["complete"] if derived_states else False),
            "accountSourceUniverses": [
                (a.get("relation"), a.get("resolution"), a.get("applicability"), a.get("sourceUniverse"))
                for a in result.get("manifestAccounts") or []
            ],
            "fullRun": result.get("fullRun"),
            "precedenceTable": result.get("precedenceTable"),
            "note": result.get("note"),
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
        "sourceUniverse": uni, "targetUniverse": None, "applicability": "unsupported-typed", "coverageIds": [],
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
        rec("candidate-unavailable-envelope-schema", {"controlStanding": "schema-unit", "result": "ADMIT", "refusals": []})
    except Exception as exc:
        rec("candidate-unavailable-envelope-schema", {"controlStanding": "schema-unit", "result": "REFUSE", "refusals": [str(exc)]})

    autofix = dict(cand, state="complete", deficiency=None, universe="c" * 64, stageOrdinal=0,
                   automaticDeletionEligible=True, examinedPaths=["src/index.ts"], sourceBodies=[])
    try:
        M.C.validate(CAND_SCHEMA, autofix)
        rec("schema-rejects-candidate-autofix", {"controlStanding": "schema-unit", "result": "ADMIT", "refusals": []})
    except Exception:
        rec("schema-rejects-candidate-autofix", {"controlStanding": "schema-unit", "result": "REFUSE", "refusals": ["EXECUTION_INPUTS_SCHEMA"]})

    group = {
        "mode": "near", "evidenceLevel": "similar-candidate", "language": "typescript",
        "members": ["body-a"], "authority": "candidate-only",
        "matchedEdges": [{"left": "body-a", "right": "body-a", "similarityMillionths": 900000}],
        "grouping": "connected-component", "scoreMeaning": "minimum-member-best-neighbor",
        "semanticEquivalenceClaimed": False, "automaticDeletionEligible": False,
    }
    try:
        M.C.validate(GROUP_SCHEMA, group)
        rec("clone-candidate-group-v2-schema", {"controlStanding": "schema-unit", "result": "ADMIT", "refusals": []})
    except Exception as exc:
        rec("clone-candidate-group-v2-schema", {"controlStanding": "schema-unit", "result": "REFUSE", "refusals": [str(exc)]})

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
        unav_result = dict(admit(unav))
        unav_result["manifestAccounts"] = unav["execution_inputs"]["nativeCoverageAccounts"]
        rec("unavailable-binding-budget-keeps-inventory-causes", unav_result)
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
            "controlStanding": "helper-unit",
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
            "controlStanding": "helper-unit",
        })
        g_obj = copy.deepcopy(g_amb)
        g_obj["objects"]["finding3:" + "0" * 64] = ("finding", {"schemaVersion": 2})
        m3, d3 = H.build_manifest(g_obj)
        rec("ambient-object-does-not-change-digest", {
            "result": "ADMIT" if d1 == d3 and m1["selectedRefs"] == m3["selectedRefs"] else "REFUSE",
            "refusals": [] if d1 == d3 else ["AMBIENT_OBJECT_DIGEST"],
            "controlStanding": "helper-unit",
        })
        mutated = copy.deepcopy(m1)
        mutated["selectedRefs"] = [r for r in mutated["selectedRefs"] if r.get("domain") != "coverage"]
        rec("selected-refs-change-changes-digest", {
            "result": "ADMIT" if M.raw_digest(mutated) != d1 and mutated["selectedRefs"] != m1["selectedRefs"] else "REFUSE",
            "refusals": [] if M.raw_digest(mutated) != d1 else ["SELECTED_DIGEST_UNCHANGED"],
            "controlStanding": "helper-unit",
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
            "controlStanding": "helper-unit",
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
            "schemaVersion": 2, "planId": owner["plan_id"], "sourceFactId": fact_id,
            "producerClosure": fact["producerClosure"], "targetUniverse": fact["targetUniverse"],
            "targetNativeId": "file:src/index.ts", "kind": "unknown", "occupancy": "unknown",
            "exported": None, "logicalPath": None, "packageManifestPath": None,
            "evaluationNativeId": None,
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

    # ------------------------------------------------------------------
    # Execution-account corrections: applicability precedence, the account/binding universe
    # join, the selected-U unsupported disclosure, and the carrier for missing work.
    # ------------------------------------------------------------------
    rec("applicability-first-match-precedence", applicability_precedence_table())

    def with_accounts(kw, admitted, note=None):
        out = dict(admitted)
        out["manifestAccounts"] = kw["execution_inputs"]["nativeCoverageAccounts"]
        if note:
            out["note"] = note
        return out

    # sourceUniverse IS the binding U even where the account carries no Coverage. The owner
    # positive already owns an inapplicable-vcs account at a non-null binding U.
    vcs_acc = next(a for a in owner["execution_inputs"]["nativeCoverageAccounts"]
                   if a["relation"] == "vcs-change")
    rec("inapplicable-vcs-account-carries-binding-universe",
        with_accounts(owner, admit(owner),
                      note="binding U " + str(vcs_acc["sourceUniverse"])))
    rec("inapplicable-vcs-account-null-source-universe-refuses",
        admit(set_account_source_universe(owner, lambda a: a["relation"] == "vcs-change", None)))

    uns_graph = F.build_file_inputs(unsupported_cell="required")
    uns = manifest_from_owner(uns_graph)
    rec("unsupported-typed-account-carries-binding-universe", with_accounts(uns, admit(uns)))
    rec("unsupported-typed-account-null-source-universe-refuses",
        admit(set_account_source_universe(uns, lambda a: a["relation"] == "references", None)))

    # NOTE ON WHAT THIS SHOWS. This cell has a SELECTED enumerator at a NON-NULL universe with an
    # admitted synthetic native `unknown` Coverage. What the oracle establishes is that an
    # OPTIONAL matrix-unsupported cell owes NO requiredCellDeficiencies row and still closes. It
    # establishes NOTHING about whether a provider was executed: no synthetic reference fixture
    # executes or declines to execute a real provider, and absence of SELECTION is the separate
    # `optional-unselected-account-retained-typed-disclosure` control.
    uns_opt = manifest_from_owner(F.build_file_inputs(unsupported_cell="optional"))
    rec("optional-unsupported-cell-owes-no-required-cell-row", with_accounts(
        uns_opt, admit(uns_opt),
        note="selected enumerator, non-null U, admitted synthetic unknown Coverage; establishes "
             "the absence of a required-cell row only, not the absence of provider execution"))

    unsel = manifest_from_owner(F.build_file_inputs(optional_unselected_cell=True))
    rec("optional-unselected-account-retained-typed-disclosure", with_accounts(unsel, admit(unsel)))
    rec("null-binding-universe-account-must-stay-null",
        admit(set_account_source_universe(
            unsel, lambda a: a["applicability"] == "unavailable-unselected",
            owner["enumeration_plan"]["cells"][0]["programBindings"][0]["universe"])))

    two_u = manifest_from_owner(F.build_file_inputs(multiple_universes=True))
    u0 = two_u["enumeration_plan"]["cells"][0]["programBindings"][0]["universe"]
    u1 = two_u["enumeration_plan"]["cells"][0]["programBindings"][1]["universe"]
    rec("foreign-universe-account-source-universe-refuses",
        admit(set_account_source_universe(
            two_u, lambda a: a["programOrdinal"] == 0 and a["relation"] == "file", u1)))
    # §5: an account aggregates its binding's Coverage across target universes, so its own
    # targetUniverse has one canonical value, null. A cross-universe TARGET stays lawful on the
    # Coverage/fact records; only the account field is fixed.
    rec("account-target-universe-null-admits-in-a-two-universe-run", admit(two_u))
    rec("account-target-universe-non-null-refuses", admit(
        set_account_target_universe(two_u, lambda a: a["programOrdinal"] == 0, u1)))
    _ = u0

    # Census / empty-partition carrier.
    census = replace_file_view_with_one_subject(owner_missing)
    rec("census-missing-subjects-derive-null-pair", admit(census))
    rec("census-missing-subjects-host-may-not-claim-provider-unavailable", admit(
        claim_row_pair(census, "provider-unavailable", None)))
    rec("empty-returned-partitions-host-may-not-claim-provider-unavailable", admit(
        claim_row_pair(owner_missing, "provider-unavailable", None)))
    typed_census = replace_file_view_with_one_subject(owner_missing, complete=False, rebuild=True)
    rec("typed-native-carrier-survives-alongside-census-failure", admit(typed_census))
    try:
        inv_census = replace_file_view_with_one_subject(
            manifest_from_owner(graph_two_partial_inventories()), rebuild=True)
        rec("typed-inventory-carriers-survive-alongside-census-failure", admit(inv_census))
    except Exception as exc:  # noqa: BLE001
        rec("typed-inventory-carriers-survive-alongside-census-failure",
            {"result": "REFUSE", "refusals": [type(exc).__name__ + ":" + str(exc)]})

    # Cross-source primary pair: an earlier UNTYPED account must not mask a later typed one.
    # The file account is census-short with no typed record; the package account carries the
    # producer's own derived budget-exhausted. They are owed in the capability matrix's authored
    # relations order (file, package, vcs-change), so the untyped one comes FIRST.
    MIXED = {"file_coverage_subjects": ["README.md"], "package_coverage_unknown": True}
    mixed_acc = manifest_from_owner(F.build_file_inputs(**MIXED))
    rec("mixed-accounts-first-typed-pair-not-first-source", admit(mixed_acc))
    rec("full-run-mixed-accounts-first-typed-pair",
        full_run_case("mixed-accounts", "indeterminate",
                      ["budget-exhausted", "required-cell-unsatisfied"], **MIXED))

    # Candidate carrier is not manufactured either. An optional candidate cell with no retained
    # envelope ADMITS, so this path is reachable; the required one refuses first.
    try:
        rec("optional-candidate-absent-envelope-derives-null-pair",
            admit(candidate_cell_without_envelope(owner, required=False)))
        rec("required-candidate-absent-envelope-still-refuses",
            admit(candidate_cell_without_envelope(owner, required=True)))
    except Exception as exc:  # noqa: BLE001
        rec("optional-candidate-absent-envelope-derives-null-pair",
            {"result": "REFUSE", "refusals": [type(exc).__name__ + ":" + str(exc)]})
        rec("required-candidate-absent-envelope-still-refuses",
            {"result": "REFUSE", "refusals": [type(exc).__name__ + ":" + str(exc)]})

    # Full retained Runs through M.close_run.
    rec("full-run-empty-returned-partitions-bridge-required-cell-unsatisfied",
        full_run_case("empty-returned-partitions", "indeterminate",
                      ["required-cell-unsatisfied"], complete_required_native=False))
    rec("full-run-census-missing-subjects-bridge-keeps-originating-coverage",
        full_run_case("census-missing-subjects", "indeterminate",
                      ["required-cell-unsatisfied"], file_coverage_subjects=["README.md"]))
    rec("full-run-required-unsupported-matrix-pair-bridge",
        full_run_case("required-unsupported", "indeterminate",
                      ["language-tier-unsupported"], unsupported_cell="required"))
    rec("full-run-optional-unselected-and-optional-unsupported-close-without-execution-deficiency",
        full_run_case("optional-unselected+optional-unsupported", "pass", [],
                      optional_unselected_cell=True, unsupported_cell="optional"))

    # --- view attribution (contract §3 "View attribution") ---
    va = {}

    def va_rec(name, result):
        va[name] = result
        rec(name, result)

    def va_refs_universes(t):
        u0 = t["universes"]["references"][0]
        return u0, next(u for u in t["universes"]["inventory"] if u != u0)

    uns_world, _ = view_attribution_world({"unsupported_cell": "required"}, lambda t: ((), ()))
    uns_refs_view = hx(next(k for k in uns_world["viewIds"]
                            if [uns_world["objects"][s][1]["relation"] for s in uns_world["objects"][k][1]["scopeIds"]]
                            == ["references"]))
    va_rec("view-attribution-unsupported-row-names-its-returned-view", view_attribution_case(uns_world))

    def va_refs_row_names_nothing(rows):
        for r in rows:
            if r["capabilityId"] == "references":
                r["viewDigests"] = []

    va_rec("view-attribution-unsupported-row-naming-no-view-refuses",
           view_attribution_case(uns_world, row_edit=va_refs_row_names_nothing, closed=False))

    def va_shared_file_package(t):
        u0 = t["universes"]["inventory"][0]
        f, p = t["single"]("file", u0), t["single"]("package", u0)
        fv, pv = t["objects"][f][1], t["objects"][p][1]
        return (f, p), (t["view"](fv["scopeIds"] + pv["scopeIds"], fv["facts"] + pv["facts"],
                                  fv["coverageIds"] + pv["coverageIds"]),)

    shared_world, shared_add = view_attribution_world({}, va_shared_file_package)
    va_rec("view-attribution-one-view-several-relations-of-one-cell-admits", view_attribution_case(shared_world))

    va_um = {"unsupported_cell": "required", "multiple_universes": True}

    def va_refs_view_plus(relation, resolution, foreign, with_coverage):
        def mutate(t):
            u0, u1 = va_refs_universes(t)
            uni = u1 if foreign else u0
            r = t["single"]("references", u0)
            rv = t["objects"][r][1]
            extra = t["scope"](relation, resolution, uni)
            covs = [t["coverage"](extra, uni)] if with_coverage else []
            return (r,), (t["view"](rv["scopeIds"] + [extra], rv["facts"], rv["coverageIds"] + covs),)
        return mutate

    va_rec("view-attribution-unsupported-row-view-with-two-universes-coverage-refuses", view_attribution_case(
        view_attribution_world(va_um, va_refs_view_plus("references", "resolved-binding", True, True))[0]))
    va_rec("view-attribution-attributed-view-naming-coverage-less-foreign-scope-refuses", view_attribution_case(
        view_attribution_world(va_um, va_refs_view_plus("declares", "syntactic", True, False))[0]))
    va_rec("view-attribution-attributed-view-naming-coverage-less-same-universe-scope-admits", view_attribution_case(
        view_attribution_world(va_um, va_refs_view_plus("declares", "syntactic", False, False))[0]))

    def va_split_scopes(t):
        u0, u1 = va_refs_universes(t)
        return (), (t["view"]([t["scope"]("declares", "syntactic", u0),
                               t["scope"]("references", "resolved-binding", u1)]),)

    split_world, split_add = view_attribution_world(va_um, va_split_scopes)
    va_rec("view-attribution-universe-and-relation-on-different-scopes-attributes-nothing",
           view_attribution_case(split_world, capture=split_add))

    def va_refs_row_names_split(rows):
        for r in rows:
            if r["capabilityId"] == "references":
                r["viewDigests"] = M.canon_str_list(r["viewDigests"] + [hx(split_add[0])])

    va_rec("view-attribution-universe-and-relation-on-different-scopes-host-naming-it-refuses",
           view_attribution_case(split_world, capture=split_add, row_edit=va_refs_row_names_split, closed=False))

    def va_lawful_split(t):
        _u0, u1 = va_refs_universes(t)
        s = t["scope"]("references", "resolved-binding", u1)
        return (), (t["view"]([s], (), [t["coverage"](s, u1)]),)

    lawful_world, lawful_add = view_attribution_world(va_um, va_lawful_split)
    va_rec("view-attribution-lawful-one-view-per-universe-split-admits",
           view_attribution_case(lawful_world, capture=lawful_add))

    def va_two_universe_supported(t):
        u0, u1 = t["universes"]["inventory"][:2]
        a, b = t["single"]("file", u0), t["single"]("file", u1)
        av, bv = t["objects"][a][1], t["objects"][b][1]
        return (a, b), (t["view"](av["scopeIds"] + bv["scopeIds"], av["facts"] + bv["facts"],
                                  av["coverageIds"] + bv["coverageIds"]),)

    va_rec("view-attribution-supported-rows-view-with-two-universes-coverage-refuses", view_attribution_case(
        view_attribution_world({"multiple_universes": True}, va_two_universe_supported)[0], closed=False))

    want = {
        "applicability-first-match-precedence": "ADMIT",
        "inapplicable-vcs-account-carries-binding-universe": "ADMIT",
        "inapplicable-vcs-account-null-source-universe-refuses": "REFUSE",
        "unsupported-typed-account-carries-binding-universe": "ADMIT",
        "unsupported-typed-account-null-source-universe-refuses": "REFUSE",
        "optional-unsupported-cell-owes-no-required-cell-row": "ADMIT",
        "optional-unselected-account-retained-typed-disclosure": "ADMIT",
        "null-binding-universe-account-must-stay-null": "REFUSE",
        "foreign-universe-account-source-universe-refuses": "REFUSE",
        "account-target-universe-null-admits-in-a-two-universe-run": "ADMIT",
        "account-target-universe-non-null-refuses": "REFUSE",
        "census-missing-subjects-derive-null-pair": "ADMIT",
        "census-missing-subjects-host-may-not-claim-provider-unavailable": "REFUSE",
        "empty-returned-partitions-host-may-not-claim-provider-unavailable": "REFUSE",
        "typed-native-carrier-survives-alongside-census-failure": "ADMIT",
        "typed-inventory-carriers-survive-alongside-census-failure": "ADMIT",
        "mixed-accounts-first-typed-pair-not-first-source": "ADMIT",
        "full-run-mixed-accounts-first-typed-pair": "ADMIT",
        "optional-candidate-absent-envelope-derives-null-pair": "ADMIT",
        "required-candidate-absent-envelope-still-refuses": "REFUSE",
        "full-run-empty-returned-partitions-bridge-required-cell-unsatisfied": "ADMIT",
        "full-run-census-missing-subjects-bridge-keeps-originating-coverage": "ADMIT",
        "full-run-required-unsupported-matrix-pair-bridge": "ADMIT",
        "full-run-optional-unselected-and-optional-unsupported-close-without-execution-deficiency": "ADMIT",
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
        "view-attribution-unsupported-row-names-its-returned-view": "ADMIT",
        "view-attribution-unsupported-row-naming-no-view-refuses": "REFUSE",
        "view-attribution-one-view-several-relations-of-one-cell-admits": "ADMIT",
        "view-attribution-unsupported-row-view-with-two-universes-coverage-refuses": "REFUSE",
        "view-attribution-attributed-view-naming-coverage-less-foreign-scope-refuses": "REFUSE",
        "view-attribution-attributed-view-naming-coverage-less-same-universe-scope-admits": "ADMIT",
        "view-attribution-universe-and-relation-on-different-scopes-attributes-nothing": "ADMIT",
        "view-attribution-universe-and-relation-on-different-scopes-host-naming-it-refuses": "REFUSE",
        "view-attribution-lawful-one-view-per-universe-split-admits": "ADMIT",
        "view-attribution-supported-rows-view-with-two-universes-coverage-refuses": "REFUSE",
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
    by_case = {c["case"]: c for c in cases}

    def oracle(name, ok, got):
        if not ok:
            oracles.append({"oracle": name, "got": got})

    # --- account sourceUniverse IS the binding universe, for empty accounts too ---
    vcs_case = by_case.get("inapplicable-vcs-account-carries-binding-universe") or {}
    vcs_rows = [r for r in (vcs_case.get("accountSourceUniverses") or []) if r[0] == "vcs-change"]
    binding_u = owner["enumeration_plan"]["cells"][0]["programBindings"][0]["universe"]
    oracle("inapplicable-vcs-source-universe-equals-binding-u",
           bool(vcs_rows) and all(r[2] == "inapplicable-vcs" and r[3] == binding_u for r in vcs_rows),
           vcs_rows)
    uns_case = by_case.get("unsupported-typed-account-carries-binding-universe") or {}
    uns_rows = [r for r in (uns_case.get("accountSourceUniverses") or []) if r[0] == "references"]
    oracle("unsupported-typed-source-universe-equals-binding-u",
           bool(uns_rows) and all(r[2] == "unsupported-typed" and r[3] == binding_u for r in uns_rows),
           uns_rows)
    unsel_case = by_case.get("optional-unselected-account-retained-typed-disclosure") or {}
    unsel_rows = [r for r in (unsel_case.get("accountSourceUniverses") or [])
                  if r[2] == "unavailable-unselected"]
    oracle("optional-unselected-is-reachable-and-null-u",
           bool(unsel_rows) and all(r[3] is None for r in unsel_rows), unsel_rows)
    oracle("optional-unselected-keeps-typed-binding-pair-and-no-required-row",
           (unsel_case.get("derivedOutcomeStates") == ["complete", "unavailable"]
            and ("provider-unavailable", None) in [tuple(p) for p in (unsel_case.get("derivedOutcomeDeficiencies") or [])]
            and not (unsel_case.get("deficiencyCauses") or [])),
           {"states": unsel_case.get("derivedOutcomeStates"),
            "pairs": unsel_case.get("derivedOutcomeDeficiencies"),
            "required": unsel_case.get("deficiencyCauses")})

    # --- selected-U unsupported: Coverage retained and admitted, named by no account ---
    named = {c for a in uns["execution_inputs"]["nativeCoverageAccounts"] for c in a["coverageIds"]}
    selected_cov = {r["digest"] for r in uns["execution_inputs"]["selectedRefs"]
                    if r["domain"] == "coverage"}
    unaccounted = sorted(selected_cov - named)
    unaccounted_entries = [payload_of(uns["objects"], uns["blobs"], d).get("entry") or {}
                           for d in unaccounted]
    oracle("selected-u-unsupported-coverage-stays-selected-but-unaccounted",
           (len(unaccounted) == 1
            and unaccounted_entries[0].get("coverage") == "unknown"
            and unaccounted_entries[0].get("deficiency") == "language-tier-unsupported"
            and unaccounted_entries[0].get("nativeCause") == "capability-missing"),
           {"unaccounted": unaccounted, "entries": unaccounted_entries})
    uns_acc = next((a for a in (admit(uns).get("derivedAccounts") or [])
                    if a.get("relation") == "references"), {})
    oracle("unsupported-account-discloses-the-matrix-pair-not-only-the-token",
           (uns_acc.get("accountState") == "unsupported"
            and uns_acc.get("deficiency") == "language-tier-unsupported"
            and uns_acc.get("nativeCause") == "capability-missing"
            and uns_acc.get("coverageRecords") == []),
           uns_acc)
    oracle("required-unsupported-cell-outcome-complete-but-assessment-indeterminate",
           (uns_case.get("derivedOutcomeStates") == ["complete", "complete"]
            and ("language-tier-unsupported", "capability-missing")
            in [tuple(p) for p in (uns_case.get("deficiencyPairs") or [])]
            and uns_case.get("deficiencyCauses") == ["unsupported-typed"]),
           {"states": uns_case.get("derivedOutcomeStates"),
            "pairs": uns_case.get("deficiencyPairs"),
            "causes": uns_case.get("deficiencyCauses")})
    opt_uns = by_case.get("optional-unsupported-cell-owes-no-required-cell-row") or {}
    oracle("optional-unsupported-cell-needs-no-required-row",
           opt_uns.get("deficiencyCauses") == [], opt_uns.get("deficiencyCauses"))

    # --- no fabricated carrier for missing work; real carriers survive ---
    empty_part = by_case.get("owner-graph-file-missing-required-package") or {}
    oracle("empty-returned-partitions-derive-null-null",
           ([tuple(p) for p in (empty_part.get("deficiencyPairs") or [])] == [(None, None)]
            and [tuple(p) for p in (empty_part.get("derivedOutcomeDeficiencies") or [])] == [(None, None)]
            and empty_part.get("derivedOutcomeStates") == ["partial"]),
           {"pairs": empty_part.get("deficiencyPairs"),
            "row": empty_part.get("derivedOutcomeDeficiencies"),
            "states": empty_part.get("derivedOutcomeStates")})
    cen = by_case.get("census-missing-subjects-derive-null-pair") or {}
    cen_refs = [r for refs in (cen.get("deficiencyInputRefs") or []) for r in (refs or [])]
    oracle("census-missing-subjects-derive-null-null-and-keep-originating-coverage",
           (all(tuple(p) == (None, None) for p in (cen.get("deficiencyPairs") or []))
            and any(r.get("domain") == "coverage" for r in cen_refs)
            and cen.get("derivedOutcomeStates") == ["partial"]),
           {"pairs": cen.get("deficiencyPairs"), "refs": cen_refs,
            "states": cen.get("derivedOutcomeStates")})
    typed_cen = by_case.get("typed-native-carrier-survives-alongside-census-failure") or {}
    typed_pairs = [tuple(p) for p in (typed_cen.get("deficiencyPairs") or [])]
    typed_summary = next((a for a in (admit(typed_census).get("derivedAccounts") or [])
                          if a.get("relation") == "file"), {})
    oracle("real-typed-native-carrier-is-the-primary-pair-under-a-census-failure",
           (("budget-exhausted", None) in typed_pairs
            and typed_summary.get("deficiency") == "budget-exhausted"
            and bool(typed_summary.get("censusMissing"))
            and typed_summary.get("accountState") == "incomplete"),
           {"pairs": typed_pairs, "summary": {k: typed_summary.get(k) for k in
                                              ("accountState", "deficiency", "nativeCause", "censusMissing")}})
    inv_cen = by_case.get("typed-inventory-carriers-survive-alongside-census-failure") or {}
    inv_cen_pairs = [tuple(p) for p in (inv_cen.get("deficiencyPairs") or [])]
    oracle("typed-inventory-carriers-and-null-census-row-coexist",
           ({"budget-exhausted", "input-closure-incomplete"} <= {p[0] for p in inv_cen_pairs}
            and (None, None) in inv_cen_pairs
            and inv_cen.get("derivedOutcomeStates") == ["partial"]),
           {"pairs": inv_cen_pairs, "states": inv_cen.get("derivedOutcomeStates")})

    # --- the two unavailable tokens are reachable and MEAN different things ---
    sel_unav = by_case.get("unavailable-binding-budget-keeps-inventory-causes") or {}
    sel_tokens = {r[2] for r in (sel_unav.get("accountSourceUniverses") or [])}
    oracle("selected-unavailable-binding-is-unavailable-null-universe-not-unselected",
           "unavailable-null-universe" in sel_tokens and "unavailable-unselected" not in sel_tokens,
           sorted(sel_tokens))
    oracle("optional-unselected-and-selected-unavailable-are-distinct-reachable-tokens",
           ({r[2] for r in (unsel_case.get("accountSourceUniverses") or [])} & {"unavailable-unselected"}
            and sel_tokens & {"unavailable-null-universe"}),
           {"unselectedCase": sorted({r[2] for r in (unsel_case.get("accountSourceUniverses") or [])}),
            "selectedUnavailableCase": sorted(sel_tokens)})

    # --- cross-source primary pair: first source ACTUALLY carrying a typed pair ---
    mixed = by_case.get("mixed-accounts-first-typed-pair-not-first-source") or {}
    mixed_sources = [tuple(s) for group in (mixed.get("derivedSources") or []) for s in group]
    oracle("earlier-untyped-account-does-not-mask-a-later-typed-carrier",
           (mixed_sources[:2] == [("account", None, None), ("coverage", "budget-exhausted", None)]
            and [tuple(p) for p in (mixed.get("derivedOutcomeDeficiencies") or [])]
            == [("budget-exhausted", None)]
            and mixed.get("derivedOutcomeStates") == ["partial"]),
           {"sources": mixed_sources, "row": mixed.get("derivedOutcomeDeficiencies"),
            "states": mixed.get("derivedOutcomeStates")})
    oracle("masked-untyped-source-is-still-retained-with-its-own-refs",
           (("account", None, None) in mixed_sources
            and any(tuple(p) == (None, None) for p in (mixed.get("deficiencyPairs") or []))
            and sum(1 for refs in (mixed.get("deficiencyInputRefs") or [])
                    for r in (refs or []) if r.get("domain") == "coverage") >= 2),
           {"sources": mixed_sources, "pairs": mixed.get("deficiencyPairs"),
            "refs": mixed.get("deficiencyInputRefs")})
    # The published cross-source order must be the one the reference actually walks.
    oracle("published-source-order-matches-the-reference",
           [s for s, _why in M.SOURCE_ORDER]
           == ["enumerator-or-binding", "inventory", "candidate", "account"],
           [s for s, _why in M.SOURCE_ORDER])
    schema_cross = (M.SCHEMA["x-opensip-derived-carrier-law"]["crossSourceOrder"]["order"])
    oracle("schema-cross-source-annotation-matches-the-reference",
           [r["source"] for r in schema_cross]
           == ["enumerator-or-binding", "inventory", "candidate", "coverage-or-account"],
           [r["source"] for r in schema_cross])
    # The account leg's order is the matrix relations ARRAY as authored, not a lexical sort.
    oracle("account-leg-order-is-the-authored-matrix-array-not-lexical",
           (M._matrix_pairs("inventory") == [("file", "enumerated"),
                                             ("package", "manifest-declared"),
                                             ("vcs-change", "vcs-reported")]
            and M._matrix_pairs("syntax") == [("declares", "syntactic"), ("literal", "syntactic"),
                                              ("control-flow", "syntactic")]
            and M._matrix_pairs("syntax") != sorted(M._matrix_pairs("syntax"))),
           {"inventory": M._matrix_pairs("inventory"), "syntax": M._matrix_pairs("syntax")})

    # --- candidate carrier is not manufactured either ---
    cand_opt = by_case.get("optional-candidate-absent-envelope-derives-null-pair") or {}
    cand_sources = [tuple(s) for group in (cand_opt.get("derivedSources") or []) for s in group]
    oracle("absent-candidate-envelope-derives-null-null-and-keeps-unavailable",
           (cand_sources == [("candidate", None, None)]
            and cand_opt.get("derivedOutcomeStates") == ["unavailable"]
            and [tuple(p) for p in (cand_opt.get("derivedOutcomeDeficiencies") or [])]
            == [(None, None)]),
           {"sources": cand_sources, "states": cand_opt.get("derivedOutcomeStates"),
            "row": cand_opt.get("derivedOutcomeDeficiencies")})
    cand_req = by_case.get("required-candidate-absent-envelope-still-refuses") or {}
    oracle("required-candidate-absent-envelope-refuses-candidate-required",
           "EXECUTION_INPUTS_CANDIDATE_REQUIRED" in (cand_req.get("refusals") or []),
           cand_req.get("refusals"))

    # --- reporting standing: no control may invent an admission row ---
    bad_standing = [
        {"case": c["case"], "controlStanding": c.get("controlStanding"),
         "derivedOutcomeStates": c.get("derivedOutcomeStates")}
        for c in cases
        if c.get("controlStanding") not in ("admission", "closed-run")
        and c.get("derivedOutcomeStates") is not None
    ]
    oracle("non-admission-controls-report-no-invented-cell", not bad_standing, bad_standing)
    unknown_standing = sorted({c.get("controlStanding") for c in cases}
                              - {"admission", "closed-run", "helper-unit", "schema-unit"})
    oracle("every-control-declares-a-known-standing", not unknown_standing, unknown_standing)

    fabricated = []
    for c in cases:
        for pair in (c.get("deficiencyPairs") or []) + (c.get("derivedOutcomeDeficiencies") or []):
            if tuple(pair) == ("provider-unavailable", None) and c["case"] in (
                "owner-graph-file-missing-required-package",
                "census-missing-subjects-derive-null-pair",
                "expected-source-census-uncovered-is-incomplete",
            ):
                fabricated.append({"case": c["case"], "pair": pair})
    oracle("no-manufactured-provider-unavailable-on-missing-work", not fabricated, fabricated)

    # --- full retained Runs ---
    for name, want_pairs in [
        ("full-run-empty-returned-partitions-bridge-required-cell-unsatisfied",
         [["required-cell-unsatisfied", None]]),
        ("full-run-census-missing-subjects-bridge-keeps-originating-coverage",
         [["required-cell-unsatisfied", None]]),
        ("full-run-required-unsupported-matrix-pair-bridge",
         [["language-tier-unsupported", "capability-missing"]]),
        ("full-run-optional-unselected-and-optional-unsupported-close-without-execution-deficiency",
         []),
    ]:
        fr = (by_case.get(name) or {}).get("fullRun") or {}
        oracle(name + "::pairs",
               [list(p) for p in (fr.get("executionCausePairs") or [])] == want_pairs, fr)
    census_run = (by_case.get("full-run-census-missing-subjects-bridge-keeps-originating-coverage")
                  or {}).get("fullRun") or {}
    oracle("full-run-census-bridge-retains-execution-inputs-ref-plus-coverage-ref",
           any({d for d, _h in refs} == {"execution-inputs", "coverage"}
               for refs in (census_run.get("executionInputRefs") or [])),
           census_run.get("executionInputRefs"))

    # --- view attribution (contract §3 "View attribution") ---
    va_uns = va.get("view-attribution-unsupported-row-names-its-returned-view") or {}
    va_rows = va_uns.get("viewDigestsByRow") or {}
    oracle("view-attribution-unsupported-row-names-exactly-its-references-view",
           va_rows.get("references#0") == [uns_refs_view] and uns_refs_view not in (va_rows.get("inventory#0") or [])
           and (va_uns.get("fullRun") or {}).get("sameManifest") is True, {"rows": va_rows, "run": va_uns.get("fullRun")})
    for va_name in ("view-attribution-unsupported-row-naming-no-view-refuses",
                    "view-attribution-universe-and-relation-on-different-scopes-host-naming-it-refuses"):
        oracle(va_name + "::view-totality",
               "EXECUTION_INPUTS_VIEW_TOTALITY" in ((va.get(va_name) or {}).get("refusals") or []),
               (va.get(va_name) or {}).get("refusals"))
    va_shared = va.get("view-attribution-one-view-several-relations-of-one-cell-admits") or {}
    oracle("view-attribution-shared-view-named-once-and-run-closes",
           (va_shared.get("viewDigestsByRow") or {}).get("inventory#0") == [hx(shared_add[0])]
           and (va_shared.get("fullRun") or {}).get("verdict") == "pass"
           and (va_shared.get("fullRun") or {}).get("sameManifest") is True,
           {"rows": va_shared.get("viewDigestsByRow"), "run": va_shared.get("fullRun")})
    for va_name in ("view-attribution-unsupported-row-view-with-two-universes-coverage-refuses",
                    "view-attribution-attributed-view-naming-coverage-less-foreign-scope-refuses"):
        va_r = va.get(va_name) or {}
        oracle(va_name + "::coverage-derive-at-admission-and-in-the-run",
               "EXECUTION_INPUTS_COVERAGE_DERIVE" in (va_r.get("refusals") or [])
               and "EXECUTION_INPUTS_COVERAGE_DERIVE" in str((va_r.get("fullRun") or {}).get("refused")),
               {"refusals": va_r.get("refusals"), "run": va_r.get("fullRun")})
    for va_name in ("view-attribution-attributed-view-naming-coverage-less-same-universe-scope-admits",
                    "view-attribution-universe-and-relation-on-different-scopes-attributes-nothing",
                    "view-attribution-lawful-one-view-per-universe-split-admits"):
        va_run = (va.get(va_name) or {}).get("fullRun") or {}
        oracle(va_name + "::run-closes-on-the-same-manifest",
               va_run.get("verdict") == "indeterminate" and va_run.get("sameManifest") is True, va_run)
    va_split = va.get("view-attribution-universe-and-relation-on-different-scopes-attributes-nothing") or {}
    oracle("view-attribution-split-scope-view-is-on-no-row",
           all(hx(split_add[0]) not in v for v in (va_split.get("viewDigestsByRow") or {}).values()),
           va_split.get("viewDigestsByRow"))
    va_sup = va.get("view-attribution-supported-rows-view-with-two-universes-coverage-refuses") or {}
    oracle("view-attribution-supported-rows-two-universes-coverage-derive",
           "EXECUTION_INPUTS_COVERAGE_DERIVE" in (va_sup.get("refusals") or []), va_sup.get("refusals"))

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
