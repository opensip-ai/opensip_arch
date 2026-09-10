"""Candidate-only full-Run retained-input graphs.

Composes the public file fixture's owner-admitted syntax universe, snapshot, and
inventory views, then remints Plan / analysis-spec / enumeration cells / execution-plan
so clones-near is an actual required requestedCapabilities row. syntax-only is the
matrix SUPPORTED-DESIGN cell for clones-near; this does not bind a TypeScript universe
to a syntax-only request.

Not a compiler or host qualification. near_candidate_kw in the join checker is not a
full Run and is not used here.
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


F = _load("cand_graph_fix", HERE / "evaluator_graph_fixture.v3.py")
X = _load("cand_exec_fix", HERE / "execution_inputs_fixture.v3.py")
M = F.M
C = M.C
E = F.E


def _blob(blobs, value):
    raw = value if type(value) is bytes else C.canonical(value)
    digest = hashlib.sha256(raw).hexdigest()
    blobs[digest] = raw
    return digest


def _mint(objects, domain, fields):
    rec = {"schemaVersion": 2, **fields}
    key = M.identifier(domain, rec)
    objects[key] = (domain, rec)
    return key


def _sort_cells(cells):
    return sorted(cells, key=lambda c: (
        c["capabilityId"].encode("utf-8"),
        c["languageMode"].encode("utf-8"),
        c["workspaceRoot"].encode("utf-8"),
    ))


def _hx(prefixed):
    return prefixed.split(":", 1)[1] if isinstance(prefixed, str) and ":" in prefixed else prefixed


def build_candidate_graph(*, mode="complete-empty"):
    """mode: complete-empty | group-bearing | missing | forbidden-fact-authority."""
    graph = F.build_file_inputs(
        atom_override={"op": "none", "relation": "file", "minResolution": "enumerated", "filters": []},
        complete_required_native=True,
    )
    objects = copy.deepcopy(graph["objects"])
    blobs = copy.deepcopy(graph["blobs"])
    old_plan_id = graph["inputs"]["planId"]
    old_exec_id = graph["inputs"]["executionPlanId"]
    old_plan = objects[old_plan_id][1]
    old_exec = objects[old_exec_id][1]
    old_enum = copy.deepcopy(graph["enumerationPlan"])
    old_enum_digest = hashlib.sha256(C.canonical(old_enum)).hexdigest()
    spec = C.parse(blobs[old_plan["analysisSpecDigest"]])
    inv_cell = next(c for c in old_enum["cells"] if c["capabilityId"] == "inventory")
    binding0 = copy.deepcopy(inv_cell["programBindings"][0])
    provider = binding0["enumerator"]["closureId"]
    uni = binding0["universe"]
    if mode in ("complete-empty", "missing"):
        census = []
    else:
        census = ["src/index.ts"]
    cand_binding = {
        "ordinal": 0, "provenance": "default-unit",
        "enumerator": {"status": "selected", "closureId": provider},
        "nativeContextDigest": binding0["nativeContextDigest"],
        "universe": uni, "programEntry": None, "extents": [],
        "candidateSourcePaths": E.cset(census),
    }
    cand_cell = {
        "capabilityId": "clones-near", "languageMode": "syntax-only", "workspaceRoot": ".",
        "required": True, "kinds": [], "programBindings": [cand_binding],
    }
    cells = _sort_cells([copy.deepcopy(inv_cell), cand_cell])
    new_enum = {
        "schemaVersion": 1, "snapshotId": old_enum["snapshotId"],
        "scopeDigest": old_enum["scopeDigest"], "membershipDigest": old_enum["membershipDigest"],
        "cells": cells,
    }
    new_enum_digest = _blob(blobs, new_enum)
    requested = E.cset(list(spec["requestedCapabilities"]) + [{
        "capabilityId": "clones-near", "languageMode": "syntax-only",
        "workspaceRoot": ".", "required": True,
    }])
    params = []
    for p in spec["parameters"]:
        if p.get("payloadDigest") == old_enum_digest:
            params.append({"schemaDigest": p["schemaDigest"], "payloadDigest": new_enum_digest})
        else:
            params.append(p)
    spec = dict(spec, requestedCapabilities=requested, parameters=E.cset(params))
    spec_digest = _blob(blobs, spec)
    plan_fields = dict(old_plan, analysisSpecDigest=spec_digest)
    new_plan_id = _mint(objects, "plan", {k: v for k, v in plan_fields.items() if k != "schemaVersion"})
    new_plan = objects[new_plan_id][1]
    inv_ordinal = next(i for i, c in enumerate(cells) if c["capabilityId"] == "inventory")
    cand_ordinal = next(i for i, c in enumerate(cells) if c["capabilityId"] == "clones-near")
    new_inventory = []
    for _d, inv in graph["inventoryResults"]:
        rec = dict(inv, planId=new_plan_id, parameterDigest=new_enum_digest,
                   cellOrdinal=inv_ordinal if inv["cellOrdinal"] == 0 else inv["cellOrdinal"])
        new_inventory.append((_blob(blobs, rec), rec))
    new_view_ids = []
    new_coverage_ids = list(graph["coverageIds"])
    new_scope_ids = list(graph["scopeIds"])
    old_to_new_view = {}
    for vid in graph["viewIds"]:
        view = copy.deepcopy(objects[vid][1])
        view["planId"] = new_plan_id
        nid = _mint(objects, "view", {k: v for k, v in view.items() if k != "schemaVersion"})
        old_to_new_view[vid] = nid
        new_view_ids.append(nid)
    old_stage_d = old_exec["stages"][0]["stageSpecDigest"]
    stage = C.parse(blobs[old_stage_d])
    stage = dict(stage, planId=new_plan_id, parameters=spec["parameters"])
    new_stage_d = _blob(blobs, stage)
    new_exec_id = _mint(objects, "execution-plan", {
        "planId": new_plan_id,
        "stages": [{"ordinal": 0, "stageSpecDigest": new_stage_d, "requires": [], "outputDomains": ["view"]}],
    })
    snap = objects[new_plan["snapshotId"]][1]
    src_row = next(r for r in snap["sourceInventory"] if r["path"] == "src/index.ts")
    candidate_ref = None
    group = None
    gd = None
    bodies = []
    if mode in ("group-bearing", "forbidden-fact-authority"):
        bodies = [
            {"id": "body-a", "path": "src/index.ts", "contentSha256": src_row["sha256"],
             "byteLength": src_row["bytes"], "universe": uni},
            {"id": "body-b", "path": "src/index.ts", "contentSha256": src_row["sha256"],
             "byteLength": src_row["bytes"], "universe": uni},
        ]
        group = {
            "mode": "near", "evidenceLevel": "similar-candidate", "language": "typescript",
            "members": ["body-a", "body-b"],
            "authority": "fact" if mode == "forbidden-fact-authority" else "candidate-only",
            "matchedEdges": [{"left": "body-a", "right": "body-b", "similarityMillionths": 900000}],
            "grouping": "connected-component", "scoreMeaning": "minimum-member-best-neighbor",
            "semanticEquivalenceClaimed": False, "automaticDeletionEligible": False,
        }
        gd = _blob(blobs, group)
    if mode == "missing":
        env = {
            "schemaVersion": 1, "planId": new_plan_id, "executionPlanId": new_exec_id,
            "cellOrdinal": cand_ordinal, "programOrdinal": 0, "capabilityId": "clones-near",
            "languageMode": "syntax-only", "universe": uni, "producerClosure": provider,
            "stageOrdinal": 0, "state": "unavailable", "deficiency": "provider-unavailable",
            "nativeCause": None, "authority": "candidate-only",
            "semanticEquivalenceClaimed": False, "automaticDeletionEligible": False,
            "examinedPaths": [], "groupDigests": [], "sourceBodies": [],
        }
    else:
        env = {
            "schemaVersion": 1, "planId": new_plan_id, "executionPlanId": new_exec_id,
            "cellOrdinal": cand_ordinal, "programOrdinal": 0, "capabilityId": "clones-near",
            "languageMode": "syntax-only", "universe": uni, "producerClosure": provider,
            "stageOrdinal": 0, "state": "complete", "deficiency": None, "nativeCause": None,
            "authority": "candidate-only", "semanticEquivalenceClaimed": False,
            "automaticDeletionEligible": False,
            "examinedPaths": E.cset(census),
            "groupDigests": [gd] if gd else [],
            "sourceBodies": sorted(bodies, key=C.canonical),
        }
    ed = _blob(blobs, env)
    candidate_ref = {"domain": "candidate-producer-result", "digest": ed}
    refs = E.cset(
        [{"domain": "view", "digest": _hx(v)} for v in new_view_ids]
        + [{"domain": "subject-inventory", "digest": d} for d, _inv in new_inventory]
        + ([{"domain": "import", "digest": _hx(i)} for i in new_plan.get("importIds") or []])
        + ([candidate_ref] if candidate_ref else [])
    )
    inputs = dict(graph["inputs"])
    inputs.update({
        "plan": new_plan, "planId": new_plan_id, "executionPlanId": new_exec_id,
        "evaluationInputRefs": refs, "inventoryLocatorCount": len(new_inventory),
        "inventoryRowCount": sum(len(inv["rows"]) for _d, inv in new_inventory),
        "coverageCount": len(new_coverage_ids),
    })
    out = {
        "objects": objects, "blobs": blobs, "inputs": inputs, "native": graph["native"],
        "snapshot": snap, "membership": graph["membership"], "enumerationPlan": new_enum,
        "inventoryResults": new_inventory, "viewIds": E.cset(new_view_ids),
        "scopeIds": E.cset(new_scope_ids), "coverageIds": E.cset(new_coverage_ids),
        "viewId": old_to_new_view.get(graph["viewId"], new_view_ids[0]),
        "coverageId": graph["coverageId"], "scopeId": graph["scopeId"],
        "candidateMode": mode,
        "candidateOrdinal": cand_ordinal,
    }
    X.attach_host_capture(out)
    return out
