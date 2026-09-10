"""Synthetic host-capture builder for ExecutionInputsV1.

Reference design, not a host runtime and not a Run. Root calls attach_host_capture
BEFORE seed seal so the manifest is the pre-output input closure. Later proof/seal
objects must not be folded back into the hashed manifest.

Does not import the checker. Does not invent native Coverage to make cases pass.
Missing required work is described by admission requiredCellDeficiencies.

Compatible with M3 canonical-record registration of execution-inputs and
candidate-producer-result (blob preimage, not an H prefix) and with a later
proof.executionInputsDigest equal to inputs.executionInputsDigest.
"""
from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


M = _load("exec_in_fixture_model", HERE / "execution_inputs_model.v1.py")
C = M.C

SELECTED_DOMAINS = frozenset({
    "view", "import", "coverage", "subject-inventory",
    "target-attribution", "incoming-search", "candidate-producer-result",
})
HOST_DERIVED_DOMAINS = frozenset({
    "subject-inventory", "candidate-producer-result",
    "target-attribution", "incoming-search",
})


def hx(prefixed: str) -> str:
    return prefixed.split(":", 1)[1] if isinstance(prefixed, str) and ":" in prefixed else prefixed


def canon_refs(refs):
    return sorted({C.canonical(x): x for x in refs}.values(), key=C.canonical)


def pointers_of(objects, blobs):
    return list(objects.keys()) + list(blobs.keys())


def payload_of(objects, blobs, coverage_id):
    if isinstance(coverage_id, str) and not coverage_id.startswith("coverage2:"):
        coverage_id = "coverage2:" + coverage_id
    env = objects[coverage_id][1]
    raw = blobs[env["payloadDigest"]]
    return C.parse(raw) if type(raw) is bytes else raw


def _parse_store(blobs, digest):
    raw = blobs.get(digest)
    if raw is None:
        return None
    if type(raw) is bytes:
        return C.parse(raw)
    return raw


def _inventory_pairs(raw) -> list[tuple]:
    if raw is None:
        return []
    if isinstance(raw, dict):
        return list(raw.items())
    out = []
    for item in raw:
        if isinstance(item, (tuple, list)) and len(item) >= 2:
            out.append((item[0], item[1]))
        elif isinstance(item, dict) and isinstance(item.get("digest"), str):
            inv = item.get("inventory") or item.get("record") or {
                k: v for k, v in item.items() if k != "digest"
            }
            out.append((item["digest"], inv))
    return out


def normalize_graph(graph: dict) -> dict:
    """Accept evaluator_graph_fixture.v3 and evaluator_semantic_fixture.v3 shapes."""
    if not isinstance(graph, dict) or "objects" not in graph or "blobs" not in graph:
        raise C.AdmissionError("EXECUTION_INPUTS_FIXTURE_GRAPH")
    inputs = graph.get("inputs") or {}
    if not isinstance(inputs, dict):
        inputs = {}
    objects, blobs = graph["objects"], graph["blobs"]
    plan_id = (
        inputs.get("planId") or graph.get("planId") or graph.get("plan_id")
        or (inputs.get("plan") or {}).get("id")
    )
    exec_id = (
        inputs.get("executionPlanId") or graph.get("executionPlanId")
        or graph.get("execution_plan_id")
    )
    if not plan_id or plan_id not in objects:
        raise C.AdmissionError("EXECUTION_INPUTS_FIXTURE_PLAN")
    if not exec_id or exec_id not in objects:
        raise C.AdmissionError("EXECUTION_INPUTS_FIXTURE_EXECUTION_PLAN")
    enum = graph.get("enumerationPlan") or graph.get("enumeration_plan") or inputs.get("enumerationPlan")
    if not isinstance(enum, dict):
        raise C.AdmissionError("EXECUTION_INPUTS_FIXTURE_ENUM")
    snapshot = graph.get("snapshot")
    if snapshot is None:
        sid = objects[plan_id][1].get("snapshotId")
        rec = objects.get(sid)
        snapshot = rec[1] if rec else None
    view_ids = list(graph.get("viewIds") or graph.get("view_ids") or [])
    if not view_ids and graph.get("viewId"):
        view_ids = [graph["viewId"]]
    coverage_ids = list(graph.get("coverageIds") or graph.get("coverage_ids") or [])
    if not coverage_ids and graph.get("coverageId"):
        coverage_ids = [graph["coverageId"]]
    inventory_results = _inventory_pairs(
        graph.get("inventoryResults") or graph.get("inventory_results") or graph.get("inventories")
    )
    existing_refs = list(
        inputs.get("evaluationInputRefs") or inputs.get("evaluation_input_refs") or []
    )
    evaluator_closure = (
        inputs.get("evaluatorClosure") or graph.get("evaluatorClosure")
        or inputs.get("evaluator_closure")
    )
    return {
        "graph": graph, "objects": objects, "blobs": blobs, "inputs": inputs,
        "plan_id": plan_id, "execution_plan_id": exec_id, "enumeration_plan": enum,
        "snapshot": snapshot, "view_ids": view_ids, "coverage_ids": coverage_ids,
        "inventory_results": inventory_results, "evaluation_input_refs": existing_refs,
        "evaluator_closure": evaluator_closure,
    }


def _stage_specs(exec_plan: dict, blobs: dict) -> dict:
    out = {}
    for st in exec_plan.get("stages") or []:
        d = st.get("stageSpecDigest")
        if d in blobs:
            raw = blobs[d]
            out[d] = raw if isinstance(raw, dict) else C.parse(raw)
    return out


def _sidecar_maps(objects: dict, blobs: dict, refs: list) -> dict:
    targets, incoming, candidates, imports = {}, {}, {}, {}
    for r in refs:
        if not isinstance(r, dict):
            continue
        dom, digest = r.get("domain"), r.get("digest")
        if not isinstance(digest, str):
            continue
        if dom == "target-attribution" and digest in blobs:
            targets[digest] = _parse_store(blobs, digest)
        elif dom == "incoming-search" and digest in blobs:
            incoming[digest] = _parse_store(blobs, digest)
        elif dom == "candidate-producer-result" and digest in blobs:
            candidates[digest] = _parse_store(blobs, digest)
        elif dom == "import":
            hit = objects.get("import2:" + digest)
            if hit:
                imports[digest] = hit[1]
    return {
        "target_attributions": targets, "incoming_searches": incoming,
        "candidate_results": candidates, "imports": imports,
    }


def _groups_from_candidates(blobs: dict, candidates: dict) -> dict:
    groups = {}
    for rec in candidates.values():
        if not isinstance(rec, dict):
            continue
        for gd in rec.get("groupDigests") or []:
            if gd in blobs and gd not in groups:
                parsed = _parse_store(blobs, gd)
                if parsed is not None:
                    groups[gd] = parsed
    return groups


def build_manifest(graph: dict) -> tuple[dict, str]:
    """Construct ExecutionInputsV1 from an owner graph. Does not mutate the graph.

    Semantic record is lifetime-neutral: unselected ambient objects/blobs are not
    hashed. Physical availability lives on operational_capture_receipt metadata.
    """
    n = normalize_graph(graph)
    objects, blobs = n["objects"], n["blobs"]
    plan_id, exec_id = n["plan_id"], n["execution_plan_id"]
    plan = objects[plan_id][1]
    exec_plan = objects[exec_id][1]
    enum = n["enumeration_plan"]
    vcs_raw = blobs[n["snapshot"]["vcsDigest"]]
    vcs = C.parse(vcs_raw) if type(vcs_raw) is bytes else vcs_raw
    inventories = {d: inv for d, inv in n["inventory_results"]}
    view_ids = list(n["view_ids"])
    for r in n["evaluation_input_refs"]:
        if isinstance(r, dict) and r.get("domain") == "view":
            vid = "view2:" + r["digest"] if not str(r.get("digest", "")).startswith("view2:") else r["digest"]
            if vid in objects and vid not in view_ids:
                view_ids.append(vid)
    stage_specs = _stage_specs(exec_plan, blobs)
    maps = _sidecar_maps(objects, blobs, n["evaluation_input_refs"])
    outcomes = []
    accounts = []
    ordinal = 0
    bound_candidates: dict[tuple, str] = {}
    for ci, cell in enumerate(enum["cells"]):
        for b in cell["programBindings"]:
            po = b["ordinal"]
            uni = b.get("universe")
            inv_ds = M.canon_str_list(
                [d for d, inv in n["inventory_results"]
                 if inv.get("cellOrdinal") == ci and inv.get("programOrdinal") == po]
            )
            inv_by_d = {d: inv for d, inv in n["inventory_results"]}
            inv_recs = [{"digest": d, **inv_by_d[d]} for d in inv_ds if d in inv_by_d]
            cap_rels = {p[0] for p in M._matrix_pairs(cell["capabilityId"])}
            bound_views, bound_cov = [], []
            for vid in view_ids:
                if vid not in objects:
                    continue
                view = objects[vid][1]
                matched_u = matched_rel = False
                for sid in view.get("scopeIds") or []:
                    sc = objects.get(sid)
                    if not sc:
                        continue
                    scv = sc[1]
                    if scv.get("sourceUniverse") == uni:
                        matched_u = True
                    if scv.get("relation") in cap_rels or not cap_rels:
                        matched_rel = True
                if matched_u and matched_rel:
                    bound_views.append(hx(vid))
                    bound_cov.extend(hx(c) for c in view.get("coverageIds") or [])
            en = b.get("enumerator") or {}
            en_status = en.get("status")
            matrix_row = M.CELL_STATE.get((cell["capabilityId"], cell["languageMode"]))
            acc_summ = []
            cand_cap = cell["capabilityId"] in M.CANDIDATE_CAPS
            cand_rec = cand_digest = None
            if cand_cap:
                for digest, rec in maps["candidate_results"].items():
                    if not isinstance(rec, dict):
                        continue
                    if rec.get("cellOrdinal") == ci and rec.get("programOrdinal") == po:
                        cand_rec, cand_digest = rec, digest
                        bound_candidates[(ci, po)] = digest
                        break
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
                recs = []
                for cid in matched:
                    entry = payload_of(objects, blobs, "coverage2:" + cid).get("entry") or {}
                    recs.append({"id": cid, "entry": entry})
                expected = M.expected_source_census(rel, cell, b, inventories, inv_ds)
                covered = set()
                for cid in matched:
                    env = objects["coverage2:" + cid][1]
                    sc = objects.get(env["scopeId"])
                    if sc and sc[0] == "subject-scope":
                        covered.update(s for s in (sc[1].get("subjects") or []) if isinstance(s, str))
                if app == "supported-available":
                    summary = M._summarize_coverage_records(recs, expected, covered)
                elif app == "unsupported-typed":
                    want_def = (matrix_row or {}).get("deficiency")
                    want_cause = M._matrix_cause(want_def)
                    summary = {
                        "accountState": "unsupported", "coverageRecords": [],
                        "deficiency": want_def, "nativeCause": want_cause,
                        "nativeCauses": [want_cause] if want_cause else [],
                    }
                elif app == "inapplicable-vcs":
                    summary = {"accountState": "inapplicable", "coverageRecords": []}
                else:
                    bind_def, bind_cause = M._binding_carrier(b)
                    summary = {
                        "accountState": "unavailable", "coverageRecords": [],
                        "deficiency": bind_def, "nativeCause": bind_cause,
                        "nativeCauses": [bind_cause] if bind_cause else [],
                    }
                acc_summ.append({
                    "accountState": summary["accountState"], "relation": rel, "resolution": rung,
                    "deficiency": summary.get("deficiency"), "nativeCause": summary.get("nativeCause"),
                    "nativeCauses": list(summary.get("nativeCauses") or []),
                    "coverageRecords": summary.get("coverageRecords") or [],
                    "inputRefs": [{"domain": "coverage", "digest": c} for c in matched],
                })
            derived = M.derive_outcome(
                enumerator_status=en_status, universe=uni, required=cell["required"],
                inventories=inv_recs, account_summaries=acc_summ,
                candidate_rec=cand_rec, candidate_digest=cand_digest, candidate_cap=cand_cap, binding=b,
            )
            d_state, d_reason = derived["state"], derived["stageOrdinalNullReason"]
            outcomes.append({
                "ordinal": ordinal, "cellOrdinal": ci, "programOrdinal": po,
                "capabilityId": cell["capabilityId"], "languageMode": cell["languageMode"],
                "workspaceRoot": cell["workspaceRoot"], "required": cell["required"],
                "kinds": cell["kinds"], "universe": uni, "enumeratorStatus": en_status,
                "enumeratorClosure": en.get("closureId"), "state": d_state,
                "deficiency": derived["deficiency"] if d_state != "complete" else None,
                "nativeCause": derived["nativeCause"] if d_state != "complete" else None,
                "stageOrdinal": None if (d_state == "unavailable" and not (en_status == "selected" and uni is not None)) else 0,
                "stageOrdinalNullReason": d_reason if (d_state == "unavailable" and not (en_status == "selected" and uni is not None)) else None,
                "inventoryDigests": inv_ds,
                "viewDigests": M.canon_str_list(bound_views), "candidateResultDigest": cand_digest,
            })
            ordinal += 1
    view_hexes = M.canon_str_list([h for row in outcomes for h in row["viewDigests"]])
    cov_hexes = []
    for h in view_hexes:
        view = objects["view2:" + h][1]
        cov_hexes.extend(hx(c) for c in view.get("coverageIds") or [])
    selected = []
    for h in view_hexes:
        selected.append({"domain": "view", "digest": h})
    for d, _inv in n["inventory_results"]:
        selected.append({"domain": "subject-inventory", "digest": d})
    for c in M.canon_str_list(cov_hexes):
        selected.append({"domain": "coverage", "digest": c})
    for iid in plan.get("importIds") or []:
        selected.append({"domain": "import", "digest": hx(iid)})
    sidecar_refs = [
        r for r in n["evaluation_input_refs"]
        if isinstance(r, dict) and r.get("domain") in ("target-attribution", "incoming-search")
    ]
    for digest in bound_candidates.values():
        sidecar_refs.append({"domain": "candidate-producer-result", "digest": digest})
    sidecar_refs = canon_refs(sidecar_refs)
    selected.extend(sidecar_refs)
    selected = canon_refs([r for r in selected if r.get("domain") in SELECTED_DOMAINS])
    host_derived = canon_refs(
        [{"domain": "subject-inventory", "digest": d} for d, _inv in n["inventory_results"]]
        + sidecar_refs
    )
    host_derived = canon_refs([r for r in host_derived if r.get("domain") in HOST_DERIVED_DOMAINS])
    receipts = []
    for st in exec_plan.get("stages") or []:
        spec_d = st["stageSpecDigest"]
        st_spec = stage_specs.get(spec_d) or {}
        producer = st_spec.get("producerClosure")
        domains = list(st.get("outputDomains") or st_spec.get("outputDomains") or [])
        out_refs = []
        if "view" in domains:
            for h in view_hexes:
                view = objects["view2:" + h][1]
                if producer and view.get("producerClosure") != producer:
                    continue
                out_refs.append({"domain": "view", "digest": h})
        receipts.append({
            "ordinal": st.get("ordinal", len(receipts)),
            "stageSpecDigest": spec_d,
            "producerClosure": producer,
            "outputDomains": M.canon_str_list(domains) if domains else domains,
            "outputRefs": canon_refs(out_refs),
            "state": "complete", "unavailableReason": None,
        })
    if receipts and not C.equal_typed([r["ordinal"] for r in receipts], list(range(len(receipts)))):
        for i, r in enumerate(receipts):
            r["ordinal"] = i
    manifest = {
        "schemaVersion": 1, "planId": plan_id, "executionPlanId": exec_id,
        "evaluatorClosure": n["evaluator_closure"],
        "enumerationPlanDigest": M.raw_digest(enum),
        "analysisSpecDigest": plan["analysisSpecDigest"],
        "hostCapture": {
            "custody": "host-tcb-evidence-store", "observation": "stage-return",
            "stageReceipts": receipts, "hostDerivedRefs": host_derived,
        },
        "selectedRefs": selected, "cellOutcomes": outcomes,
        "nativeCoverageAccounts": accounts, "candidateResultRefs": M.canon_str_list(
            [d for d in bound_candidates.values()]
        ),
    }
    digest = M.raw_digest(manifest)
    return manifest, digest


def _promised(graph: dict, manifest: dict) -> dict:
    n = normalize_graph(graph)
    objects = n["objects"]
    return M.promised_pointers(
        manifest, objects[n["plan_id"]][1], objects[n["execution_plan_id"]][1],
        n["enumeration_plan"], objects=objects, blobs=n["blobs"],
    )


def operational_capture(graph: dict, manifest: dict, *, exclude_blob: str | None = None) -> dict:
    n = normalize_graph(graph)
    return M.operational_capture_receipt(
        _promised(graph, manifest), n["objects"], n["blobs"], exclude_blob=exclude_blob,
    )


def admission_kwargs(graph: dict) -> dict:
    """Keyword arguments for admit_execution_inputs. Does not mutate graph.

    store_pointers is the promised logical closure, not the ambient store census.
    If attach_host_capture already stored executionInputs, reuse that hashed record.
    """
    n = normalize_graph(graph)
    objects, blobs = n["objects"], n["blobs"]
    plan = objects[n["plan_id"]][1]
    exec_plan = objects[n["execution_plan_id"]][1]
    spec_raw = blobs[plan["analysisSpecDigest"]]
    spec = C.parse(spec_raw) if type(spec_raw) is bytes else spec_raw
    vcs_raw = blobs[n["snapshot"]["vcsDigest"]]
    vcs = C.parse(vcs_raw) if type(vcs_raw) is bytes else vcs_raw
    closures = {k: v for k, (dom, v) in objects.items() if dom == "closure"}
    existing = graph.get("executionInputs")
    existing_digest = graph.get("executionInputsDigest") or n["inputs"].get("executionInputsDigest")
    if isinstance(existing, dict) and existing_digest == M.raw_digest(existing):
        manifest = existing
    else:
        manifest, _digest = build_manifest(graph)
    maps = _sidecar_maps(objects, blobs, n["evaluation_input_refs"] + list(manifest.get("selectedRefs") or []))
    if not maps["imports"]:
        maps["imports"] = {hx(i): objects[i][1] for i in plan.get("importIds") or [] if i in objects}
    inventories = {d: inv for d, inv in n["inventory_results"]}
    groups = _groups_from_candidates(blobs, maps["candidate_results"])
    promised = M.promised_pointers(
        manifest, plan, exec_plan, n["enumeration_plan"], objects=objects, blobs=blobs,
    )
    return {
        "plan_id": n["plan_id"], "plan": plan, "execution_plan_id": n["execution_plan_id"],
        "execution_plan": exec_plan, "enumeration_plan": n["enumeration_plan"],
        "analysis_spec": spec, "execution_inputs": manifest,
        "objects": objects, "blobs": blobs, "store_pointers": promised["store_pointers"],
        "inventories": inventories, "imports": maps["imports"],
        "target_attributions": maps["target_attributions"],
        "incoming_searches": maps["incoming_searches"],
        "candidate_results": maps["candidate_results"], "groups": groups,
        "closures": closures, "stage_specs": _stage_specs(exec_plan, blobs),
        "vcs_observation": vcs,
    }


def attach_host_capture(graph: dict) -> dict:
    """Mutate graph: store C(manifest) in blobs, set inputs.executionInputsDigest,
    replace evaluationInputRefs with selectedRefs + execution-inputs ref.

    Call BEFORE seed seal. Adding later outputs or unselected ambient blobs does
    not rewrite the already-hashed manifest. operationalCapture is metadata, not
    a Run preimage. Does not invent Coverage.
    """
    manifest, digest = build_manifest(graph)
    graph["blobs"][digest] = C.canonical(manifest)
    inputs = graph.setdefault("inputs", {})
    inputs["executionInputsDigest"] = digest
    exec_ref = {"domain": "execution-inputs", "digest": digest}
    inputs["evaluationInputRefs"] = canon_refs(list(manifest["selectedRefs"]) + [exec_ref])
    graph["executionInputs"] = manifest
    graph["executionInputsDigest"] = digest
    op = operational_capture(graph, manifest, exclude_blob=digest)
    admitted = M.admit_execution_inputs(**admission_kwargs(graph))
    return {
        "graph": graph, "manifest": manifest, "digest": digest,
        "admission": admitted,
        "evaluationInputRefs": inputs["evaluationInputRefs"],
        "operationalCapture": op,
    }
