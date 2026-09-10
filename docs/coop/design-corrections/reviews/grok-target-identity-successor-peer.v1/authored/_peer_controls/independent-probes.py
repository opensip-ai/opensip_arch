"""Independent peer probes of target-identity successor. Not product qualification.

Boundary labels:
  ATOM-EVALUATION — atom_model.evaluate_atom on synthetic admitted maps
  ATOM-JOIN-HELPER — atom_model._join_sidecar / _reconcile_attribution / _ephemeral_target
  QUERY-PROJECT-HELPER — query_projection_model.project_fact (not execute_graph_query)
  QUERY-OWNER-WRAPPER — execute_graph_query after identity close_run
  PROVIDER-RETURN-CENSUS — published frame/schema field inventory
"""
from __future__ import annotations

import copy
import importlib.util
import json
import sys
import traceback
from pathlib import Path

PY = "/tmp/opensip-architecture-review-env/bin/python"
SUCC = Path("/tmp/opensip-design-corrections/target-identity-successor.v1")
FOUND = SUCC / "docs/coop/design-corrections/foundation"
WF = SUCC / "docs/coop/design-corrections/workflows"
OUT = Path("/private/tmp/opensip-design-corrections/grok-target-identity-successor-peer.v1/output/_peer_controls")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


AM = load("atom_model_v1", FOUND / "atom_model.v1.py")
CA = load("check_atoms_v1", FOUND / "check-atoms.v1.py")
Q = load("query_proj3", WF / "query_projection_model.v3.py")
SR = load("semantic_replay3", FOUND / "check-semantic-replay.v3.py")
S = SR.S
R = SR.R


def rec(control_id, boundary, ok, detail, **extra):
    row = {
        "id": control_id,
        "boundary": boundary,
        "ok": bool(ok),
        "detail": detail,
    }
    row.update(extra)
    return row


rows = []

# ---------------------------------------------------------------------------
# C1: provider return transport is custody, not worker→host field
# ---------------------------------------------------------------------------
p3 = json.loads((SUCC / "docs/coop/design-corrections/native/protocol3-transitions.v1.json").read_text())
frames = sorted({r.get("frame") for r in p3.get("rules") or []})
rust = json.loads((SUCC / "docs/coop/artifacts/rust-provider-protocol.v2.json").read_text())
fb = rust["wireSchema"]["payloadSchemas"]["FactBatchV2"]
ex = json.loads((FOUND / "execution-inputs.schema.v1.json").read_text())
domain_enum = ex["$defs"]["InputRefV1"]["properties"]["domain"]["enum"]
native_text = (SUCC / "docs/coop/design-corrections/native/native-evidence.schemas.v2.json").read_text()
ne_intro = (SUCC / "docs/v2/contracts/product-v1/native-evidence.md").read_text()
rows.append(rec(
    "C1-protocol3-no-attribution-frame",
    "PROVIDER-RETURN-CENSUS",
    "FactBatch" in frames and not any("ttribut" in str(f).lower() for f in frames),
    {
        "framesContainingAttribution": [f for f in frames if "ttribut" in str(f).lower()],
        "factBatchPresent": "FactBatch" in frames,
        "FactBatchV2.required": fb.get("required"),
        "FactBatchV2.optional": fb.get("optional"),
        "nativeEvidenceSchemasHasTargetAttributionToken": ("TargetAttribution" in native_text or "target-attribution" in native_text),
        "executionInputsDomainHasTargetAttribution": "target-attribution" in domain_enum,
        "nativeEvidenceClaimsProviderReturnsCompanion": "returns TargetAttributionV2 records as typed companions" in ne_intro,
        "nativeEvidenceClaimsProtocol3Unchanged": "Protocol3\nphases and frames are unchanged" in ne_intro or "Protocol3 phases and frames are unchanged" in ne_intro,
    },
))

# ---------------------------------------------------------------------------
# C2: raw target exact-id first-party + sidecar first-party different identity
# ---------------------------------------------------------------------------
fid = CA.fact2("c")
colon_path = "file:src/a.ts"
payload_id = colon_path
eph_file = CA.inv_file(path=colon_path)
mapped_file = CA.inv_file(path="src/a.ts")
other_file = CA.inv_file(path="src/b.ts")
sid, sc, cid, cov = CA.paired("imports", "resolved-target", CA.U1, CA.U1, ["ts-symbol:src/a.ts#f"], tag="ow")
inputs = CA.base_inputs(
    enumerationPlan=CA.plan_one(cap="imports", kinds=["symbol", "file"]),
    inventories=[CA.inv_symbol(), eph_file, mapped_file, other_file],
    facts={fid: CA._imports_file_fact(fid, payload_id)},
    targetAttributions={
        fid: CA.sidecar(fid, payload_id, kind="file", occupancy="first-party", evaluation="src/a.ts")
    },
)
CA.install_pair(inputs, sid, sc, cid, cov)

spec = AM.REGISTRY["relations"]["imports"]
join_error = None
try:
    AM._join_sidecar(inputs["facts"][fid], spec, inputs["targetAttributions"][fid], inputs["closures"], inputs)
    join_admitted = True
except AM.AtomAdmissionError as exc:
    join_admitted = False
    join_error = str(exc)

eph = AM._ephemeral_target(inputs["facts"][fid], spec, inputs)
recon = None
recon_error = None
try:
    recon = AM._reconcile_attribution(inputs["facts"][fid], spec, inputs)
except Exception as exc:
    recon_error = type(exc).__name__ + ": " + str(exc)

atom_a = AM.evaluate_atom(
    {"op": "exists", "relation": "imports", "minResolution": "resolved-target", "endpoint": "target", "filters": []},
    {"universe": CA.U1, "kind": "file", "nativeSubjectId": "src/a.ts"},
    inputs,
)
atom_colon = AM.evaluate_atom(
    {"op": "exists", "relation": "imports", "minResolution": "resolved-target", "endpoint": "target", "filters": []},
    {"universe": CA.U1, "kind": "file", "nativeSubjectId": colon_path},
    inputs,
)

rows.append(rec(
    "C2-join-admits-sidecar-different-identity-from-exact-id-ephemeral",
    "ATOM-JOIN-HELPER",
    True,
    {
        "ephemeralOccupancy": eph.get("occupancy"),
        "ephemeralKind": eph.get("kind"),
        "ephemeralNativeId": eph.get("nativeId"),
        "ephemeralIdentities": [list(x) if isinstance(x, tuple) else x for x in sorted(eph.get("identities") or [])],
        "sidecarEvaluationNativeId": "src/a.ts",
        "payloadTargetNativeId": payload_id,
        "joinAdmitted": join_admitted,
        "joinError": join_error,
        "reconcile": recon,
        "reconcileError": recon_error,
        "lawClaim": "independently known ephemeral first-party identity is the colon-path file; sidecar maps to src/a.ts; join does not refuse",
    },
))
rows.append(rec(
    "C2-reconcile-overwrites-ephemeral-nativeId",
    "ATOM-JOIN-HELPER",
    recon is not None and recon.get("nativeId") == "src/a.ts" and eph.get("nativeId") == colon_path and recon.get("nativeId") != eph.get("nativeId"),
    {
        "ephemeralNativeId": eph.get("nativeId"),
        "reconciledNativeId": None if recon is None else recon.get("nativeId"),
        "reconciledSource": None if recon is None else recon.get("source"),
        "overwrote": None if recon is None else (recon.get("nativeId") != eph.get("nativeId")),
    },
))
rows.append(rec(
    "C2-atom-exists-matches-sidecar-identity-not-exact-id-file",
    "ATOM-EVALUATION",
    atom_a.get("value") == "true" and atom_colon.get("value") != "true",
    {
        "existsOnSrcATs": atom_a.get("value"),
        "existsOnColonPathFile": atom_colon.get("value"),
        "knownFactIdsOnSrcATs": atom_a.get("knownFactIds"),
        "knownFactIdsOnColonPath": atom_colon.get("knownFactIds"),
        "uncertainFactIdsOnColonPath": atom_colon.get("uncertainFactIds"),
    },
))

# Control: same operand without sidecar must occupy the exact-id file, not src/a.ts
inputs_nosidecar = dict(inputs)
inputs_nosidecar["targetAttributions"] = {}
atom_a_ns = AM.evaluate_atom(
    {"op": "exists", "relation": "imports", "minResolution": "resolved-target", "endpoint": "target", "filters": []},
    {"universe": CA.U1, "kind": "file", "nativeSubjectId": "src/a.ts"},
    inputs_nosidecar,
)
atom_colon_ns = AM.evaluate_atom(
    {"op": "exists", "relation": "imports", "minResolution": "resolved-target", "endpoint": "target", "filters": []},
    {"universe": CA.U1, "kind": "file", "nativeSubjectId": colon_path},
    inputs_nosidecar,
)
rows.append(rec(
    "C2-absent-sidecar-exact-id-occupies-colon-path-file",
    "ATOM-EVALUATION",
    atom_colon_ns.get("value") == "true" and atom_a_ns.get("value") != "true",
    {
        "existsOnColonPathFileWithoutSidecar": atom_colon_ns.get("value"),
        "existsOnSrcATsWithoutSidecar": atom_a_ns.get("value"),
        "demonstratesIndependentKnownFact": "exact-id ephemeral first-party of file:src/a.ts is independently sufficient; sidecar then relocates occupancy to src/a.ts",
    },
))

# ---------------------------------------------------------------------------
# C3: query project uses raw sidecar; unknown sidecar + exact-id symbol
# ---------------------------------------------------------------------------
sym_fid = CA.fact2("d")
sym_nid = "ts-symbol:src/a.ts#f"
sid2, sc2, cid2, cov2 = CA.paired("imports", "resolved-target", CA.U1, CA.U1, [sym_nid], tag="sq")
sym_inputs = CA.base_inputs(
    enumerationPlan=CA.plan_one(cap="imports"),
    inventories=[CA.inv_symbol()],
    facts={sym_fid: {
        "factId": sym_fid, "relation": "imports", "resolution": "resolved-target",
        "sourceUniverse": CA.U1, "targetUniverse": CA.U1, "producerClosure": CA.C_PROV,
        "confidenceMillionths": 1000000,
        "payload": {"importer": "ts-symbol:src/a.ts#g", "specifier": "./a", "resolvedTarget": sym_nid},
        "anchors": [{"path": "src/a.ts", "blobDigest": CA.H("0"), "startByte": 0, "endByte": 1}],
    }},
)
CA.install_pair(sym_inputs, sid2, sc2, cid2, cov2)
atom_sym = AM.evaluate_atom(
    {"op": "exists", "relation": "imports", "minResolution": "resolved-target", "endpoint": "target", "filters": []},
    {"universe": CA.U1, "kind": "symbol", "nativeSubjectId": sym_nid},
    sym_inputs,
)
table = Q.projection_table()[("imports", "resolved-target")]
fact_obj = sym_inputs["facts"][sym_fid]
payload = fact_obj["payload"]
proj_row, proj_lim = Q.project_fact(sym_fid, fact_obj, payload, table, target_attr=None)
rows.append(rec(
    "C3-atom-exact-id-symbol-exists-true-without-sidecar",
    "ATOM-EVALUATION",
    atom_sym.get("value") == "true",
    {"value": atom_sym.get("value"), "knownFactIds": atom_sym.get("knownFactIds")},
))
rows.append(rec(
    "C3-query-project-fact-unprojectable-without-sidecar",
    "QUERY-PROJECT-HELPER",
    proj_row is None and (proj_lim or {}).get("kind") == "unprojectable-fact",
    {"projected": proj_row, "limitation": proj_lim, "tableTargetKinds": list(table.get("targetKinds") or [])},
))

# sidecar occupancy=unknown while ephemeral first-party symbol
unknown_sc = CA.sidecar(sym_fid, sym_nid, kind="unknown", occupancy="unknown")
proj_row_u, proj_lim_u = Q.project_fact(sym_fid, fact_obj, payload, table, target_attr=unknown_sc)
sym_inputs_u = dict(sym_inputs)
sym_inputs_u["targetAttributions"] = {sym_fid: unknown_sc}
atom_sym_u = AM.evaluate_atom(
    {"op": "exists", "relation": "imports", "minResolution": "resolved-target", "endpoint": "target", "filters": []},
    {"universe": CA.U1, "kind": "symbol", "nativeSubjectId": sym_nid},
    sym_inputs_u,
)
recon_u = AM._reconcile_attribution(fact_obj, spec, sym_inputs_u)
rows.append(rec(
    "C3-unknown-sidecar-atom-still-first-party-via-ephemeral",
    "ATOM-EVALUATION",
    atom_sym_u.get("value") == "true" and recon_u.get("occupancy") == "first-party",
    {"atomValue": atom_sym_u.get("value"), "reconcile": recon_u},
))
rows.append(rec(
    "C3-unknown-sidecar-query-project-unprojectable",
    "QUERY-PROJECT-HELPER",
    proj_row_u is None and (proj_lim_u or {}).get("kind") == "unprojectable-fact",
    {"projected": proj_row_u, "limitation": proj_lim_u},
))

unknown_sc_sym = CA.sidecar(sym_fid, sym_nid, kind="symbol", occupancy="unknown", exported="unknown")
proj_row_us, proj_lim_us = Q.project_fact(sym_fid, fact_obj, payload, table, target_attr=unknown_sc_sym)
sym_inputs_us = dict(sym_inputs)
sym_inputs_us["targetAttributions"] = {sym_fid: unknown_sc_sym}
atom_sym_us = AM.evaluate_atom(
    {"op": "exists", "relation": "imports", "minResolution": "resolved-target", "endpoint": "target", "filters": []},
    {"universe": CA.U1, "kind": "symbol", "nativeSubjectId": sym_nid},
    sym_inputs_us,
)
recon_us = AM._reconcile_attribution(fact_obj, spec, sym_inputs_us)
rows.append(rec(
    "C3-unknown-occupancy-known-kind-atom-match-query-unprojectable",
    "ATOM-EVALUATION",
    atom_sym_us.get("value") == "true" and recon_us.get("occupancy") == "first-party"
    and proj_row_us is None and (proj_lim_us or {}).get("note") == "unknown occupancy is not a graph endpoint",
    {
        "atomValue": atom_sym_us.get("value"),
        "reconcileOccupancy": recon_us.get("occupancy"),
        "reconcileSource": recon_us.get("source"),
        "queryLimitation": proj_lim_us,
        "queryBoundary": "QUERY-PROJECT-HELPER",
    },
))


def _query_request(operation, project, view, params):
    return {
        "completeness": "required",
        "operation": operation,
        "page": {"size": 100},
        "params": params,
        "projectId": project,
        "schemaFamily": "opensip.product.query",
        "schemaMajor": 3,
        "view": view,
    }


try:
    g = S.build_ts_semantic_graph(
        atom={"op": "exists", "relation": "imports", "minResolution": "resolved-target", "endpoint": "target", "filters": []},
        subject_kind="file", has_declares=False, has_references_fact=False, second_partition=False,
    )
    run, objects, blobs, actual = SR.close_positive(g)
    file_ep = {"universe": g["u1"], "kind": "file", "nativeSubjectId": "a.ts"}
    namespaced_ep = {"universe": g["u1"], "kind": "file", "nativeSubjectId": "file:a.ts"}
    host = {"requestId": "req1_" + "a" * 32, "latestRunId": actual["runId"]}
    result = Q.execute_graph_query(
        _query_request("graph.neighbors", run["projectId"], {"runId": actual["runId"]}, {
            "relation": "imports", "minResolution": "resolved-target", "direction": "incoming", "endpoint": file_ep,
        }),
        run, objects, blobs, host=host,
    )
    items = result.get("items") if isinstance(result, dict) else None
    native_ids = []
    if isinstance(items, list):
        for it in items:
            tgt = (it or {}).get("target") or {}
            native_ids.append(tgt.get("nativeSubjectId"))
    rows.append(rec(
        "C3-owner-wrapper-imports-file-occupancy-with-v2-sidecar",
        "QUERY-OWNER-WRAPPER",
        isinstance(items, list) and "a.ts" in native_ids,
        {
            "close_run": "ADMIT",
            "runId": actual["runId"],
            "nativeSubjectIds": native_ids,
            "itemCount": None if items is None else len(items),
            "termination": result.get("termination") if isinstance(result, dict) else None,
        },
    ))
    ns_refused = None
    ns_detail = None
    try:
        Q.execute_graph_query(
            _query_request("graph.neighbors", run["projectId"], {"runId": actual["runId"]}, {
                "relation": "imports", "minResolution": "resolved-target", "direction": "incoming",
                "endpoint": namespaced_ep,
            }),
            run, objects, blobs, host=host,
        )
        ns_refused = False
        ns_detail = "query returned instead of refusing namespaced file endpoint"
    except Q.QueryRefusal as exc:
        ns_refused = True
        ns_detail = {"error": exc.error_code, "detail": exc.detail}
    rows.append(rec(
        "C3-owner-wrapper-namespaced-payload-id-is-not-inventory-vertex",
        "QUERY-OWNER-WRAPPER",
        ns_refused is True,
        ns_detail,
    ))
    proof = objects[objects[run["evaluationSealId"]][1]["proofBundleId"]][1]
    views = list(proof.get("selectedViewIds") or proof.get("viewIds") or [])
    if not views:
        evidence = objects[run["evidenceId"]][1]
        views = list(evidence.get("viewIds") or [])
    table_imp = Q.projection_table()[("imports", "resolved-target")]
    projected_empty, lims_empty, _, _ = Q.collect_projected_edges(views, objects, blobs, table_imp, {})
    attrs = Q.retained_attributions(proof, blobs)
    projected_real, lims_real, _, _ = Q.collect_projected_edges(views, objects, blobs, table_imp, attrs)
    rows.append(rec(
        "C3-collect-on-owner-facts-empty-attributions-unprojectable",
        "QUERY-PROJECT-HELPER",
        (not projected_empty) and any((x or {}).get("kind") == "unprojectable-fact" for x in lims_empty) and bool(projected_real),
        {
            "emptyAttrProjectedCount": len(projected_empty),
            "emptyAttrLimitations": lims_empty,
            "retainedAttrProjectedCount": len(projected_real),
            "retainedAttrTargets": [((row.get("target") or {}).get("nativeSubjectId")) for row in projected_real],
            "retainedAttributionCount": len(attrs),
            "viewCount": len(views),
            "note": "same owner-admitted imports facts; collect_projected_edges with empty vs retained V2 map. Not execute_graph_query without sidecar. Does not claim Run false.",
        },
    ))
except Exception as exc:
    rows.append(rec(
        "C3-owner-wrapper-imports-file-occupancy-with-v2-sidecar",
        "QUERY-OWNER-WRAPPER",
        False,
        {"error": type(exc).__name__ + ": " + str(exc), "traceback": traceback.format_exc()[-2500:]},
    ))

qcontract = (WF / "query-projection-contract.v3.md").read_text()
rows.append(rec(
    "C3-query-contract-retains-v1-tokens",
    "CONTRACT-PROSE",
    "TargetAttributionV1" in qcontract,
    {
        "v1TokenCount": qcontract.count("TargetAttributionV1"),
        "v2TokenCount": qcontract.count("TargetAttributionV2"),
        "factLawStillNamesV1": "imports without TargetAttributionV1" in qcontract,
        "wrapperStepStillNamesV1": "retained TargetAttributionV1" in qcontract,
    },
))

report = {
    "standing": "independent peer probes; not product qualification; not global profile acceptance",
    "controls": rows,
}
(OUT / "independent-probes.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps([{"id": r["id"], "boundary": r["boundary"], "ok": r["ok"]} for r in rows], indent=2))
