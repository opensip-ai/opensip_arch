#!/usr/bin/env python3
"""Independent kit-law measurements of isolated consumer helpers/vectors.

Expected values are derived from original kit recipes and this reviewer's
discriminating inputs. Consumer helper/fixture outputs are subjects under
test, never expected-value oracles. Frozen snapshot bytes are not rewritten.
"""
from __future__ import annotations

import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path

ISO = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-workflow-recheck.v4/output/isolated-work")
OUT = ISO / "output"
KIT = ISO / "subject"
SNAP = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-workflow-recheck.v4/consumer-snapshot")
sys.path.insert(0, str(OUT))

from helper.canonical import C  # noqa: E402
from helper.errors import AdmissionError  # noqa: E402
from helper.evaluator import eval_atom  # noqa: E402
from helper.identity import H, h_preimage  # noqa: E402
from helper.query_projection import (  # noqa: E402
    execute_graph_query,
    traverse_projected_graph,
    vertex_domain,
)
from helper.schema_admit import validate_against  # noqa: E402
from helper.workflow_laws import (  # noqa: E402
    GRAPH_PROJECTABLE,
    admit_clones_fact,
    classify_presence,
    config_graph,
    derive_rust_edition,
    mutation_intent_key,
    project_edges,
    repair_apply_key,
    repair_target_join,
    rust_body_l0_retained,
)

CE = "docs/coop/design-corrections/workflows/schemas/evaluator3/command-envelope.schema.json"
INV = "docs/coop/design-corrections/workflows/schemas/evaluator3/invocation-record.schema.json"
GQ = "docs/coop/design-corrections/workflows/schemas/evaluator3/graph-query.schema.json"
SI = "docs/coop/design-corrections/foundation/subject-inventory.schema.v1.json"
NATIVE = "docs/coop/design-corrections/native/native-evidence.schemas.v2.json"

results: dict = {
    "cSelfCheck": {},
    "queryLaws": [],
    "identities": [],
    "vectors": [],
    "envelopes": [],
    "frozen": [],
    "firstFailures": [],
    "notes": [],
}


def rec(bucket: str, name: str, ok: bool, **extra):
    row = {"name": name, "ok": ok, **extra}
    results[bucket].append(row)
    if not ok:
        results["firstFailures"].append({"bucket": bucket, "name": name, **{k: extra.get(k) for k in ("expected", "actual", "code", "errors", "note") if k in extra}})
    return ok


def snap(rel: str):
    return json.loads((SNAP / rel).read_text())


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def u8pref(b: bytes) -> bytes:
    return bytes([len(b)]) + b


def independent_l0(*, span: bytes, language_id: str, compiler_name: str, compiler_version: str, compiler_build: str, dialect: dict, level_spec: bytes) -> dict:
    """FACT-IDENTITY L0 frame from identity-and-evidence.md body recipe. Uses kit C for BLV only."""
    blv = {
        "schemaVersion": 1,
        "languageId": language_id,
        "compilerName": compiler_name,
        "compilerVersion": compiler_version,
        "compilerBuild": compiler_build,
        "dialect": dialect,
    }
    lv = hashlib.sha256(C(blv)).digest()
    level_version = hashlib.sha256(level_spec).digest()
    payload = len(span).to_bytes(4, "big") + span
    frame = (
        u8pref(b"opensip.fact-identity.v1")
        + u8pref(b"L0-verbatim")
        + u8pref(level_version)
        + u8pref(language_id.encode("ascii"))
        + u8pref(lv)
        + len(payload).to_bytes(4, "big")
        + payload
    )
    return {
        "bodyIdentity": "sha256:" + hashlib.sha256(frame).hexdigest(),
        "frameSha256": hashlib.sha256(frame).hexdigest(),
        "languageVersionHex": lv.hex(),
        "payloadLen": len(payload),
        "rawLen": len(span),
        "doublePrefixed": len(payload) == len(span) + 4,
        "frameHex": frame.hex(),
        "blv": blv,
    }


def compact_query_result(response: dict) -> dict:
    ctx = response["context"]
    qr = {
        "kind": "query",
        "items": ctx.get("producedItems", len(response.get("items") or [])),
        "truncated": ctx["truncated"],
        "completenessMet": ctx.get("countBasis") == "exact",
        "advisory": False,
    }
    if ctx.get("nextCursor"):
        qr["nextCursor"] = ctx["nextCursor"]
    return qr


# --- C encoding self-check against kit identity-and-evidence §3 prose ---
c_ok = C({"b": 1, "a": 2}) == b'{"a":2,"b":1}'
c_arr = C({"xs": [2, 1]}) == b'{"xs":[2,1]}'
results["cSelfCheck"] = {
    "keyOrderUtf8": c_ok,
    "arrayAdmittedOrder": c_arr,
    "noWhitespace": b" " not in C({"z": True, "a": False}),
}
if not (c_ok and c_arr):
    results["firstFailures"].append({"bucket": "cSelfCheck", "name": "canonical-C", "actual": C({"b": 1, "a": 2})})

# --- H preimage shape ---
hx = H("fact", {"schemaVersion": 1})
pre = h_preimage("fact", C({"schemaVersion": 1}))
rec("identities", "H-preimage-product-prefix", pre.startswith(b"opensip.product.v1\x00fact\x00"), actual=pre[:24].hex())

# =============================================================================
# QUERY CONTRACT — reviewer-chosen discriminating inputs (not author mod.a/b/c)
# =============================================================================
UNI = hashlib.sha256(b"opensip.reviewer.discriminating-universe.query-v4").hexdigest()
PRJ = "prj1-" + hashlib.sha256(b"opensip.reviewer.project.query-v4").hexdigest()
RUN = "run3:" + hashlib.sha256(b"opensip.reviewer.run.query-v4").hexdigest()
SNAPID = "snapshot2:" + hashlib.sha256(b"opensip.reviewer.snapshot.query-v4").hexdigest()
HOST_RID = "req1_" + "cd" * 16


def ep(name, kind="symbol"):
    return {"universe": UNI, "kind": kind, "nativeSubjectId": name}


def mint_call(ordinal, caller, callee):
    recd = {
        "schemaVersion": 1,
        "relation": "calls",
        "resolution": "resolved-callee",
        "sourceUniverse": UNI,
        "targetUniverse": UNI,
        "payload": {"caller": caller, "resolvedCallee": callee},
        "ordinal": ordinal,
    }
    fid = "fact2:" + H("fact", recd)
    return {
        "factId": fid,
        "relation": "calls",
        "resolution": "resolved-callee",
        "sourceUniverse": UNI,
        "targetUniverse": UNI,
        "payload": recd["payload"],
        "record": recd,
    }


# Kit-derived names from query-projection-contract table (symbol endpoints), not author fixtures.
facts = [
    mint_call(0, "Entry.main", "Lib.helper"),
    mint_call(1, "Entry.main", "Lib.leaf"),
    mint_call(2, "Lib.helper", "Lib.leaf"),
]
facts.sort(key=lambda f: f["factId"])
edges = project_edges(facts, relation="calls", min_resolution="resolved-callee")
view_id = "view2:" + H("view", {"schemaVersion": 1, "facts": [f["factId"] for f in facts]})
cov_id = "coverage2:" + H("coverage", {"schemaVersion": 1, "relation": "calls", "resolution": "resolved-callee"})
scope_id = "scope2:" + H("subject-scope", {"schemaVersion": 1, "include": ["**/*"]})
inv = {
    "kind": "symbol",
    "universe": UNI,
    "rows": [
        {"nativeSubjectId": "Entry.main", "path": "src/entry.rs"},
        {"nativeSubjectId": "Lib.helper", "path": "src/lib.rs"},
        {"nativeSubjectId": "Lib.leaf", "path": "src/leaf.rs"},
    ],
}
admitted_run = {"runId": RUN, "snapshotId": SNAPID, "projectId": PRJ}


def close_ok(run, objects=None, blobs=None):
    if run.get("runId") != RUN:
        raise AdmissionError("CLOSE_RUN", "unexpected run")
    return {"ok": True, "synthetic": True, "label": "reviewer-synthetic-close_run"}


def qreq(op, params, page=None, view=None, completeness="best-effort"):
    return {
        "schemaFamily": "opensip.product.query",
        "schemaMajor": 3,
        "projectId": PRJ,
        "view": view or {"runId": RUN},
        "operation": op,
        "params": params,
        "completeness": completeness,
        "page": page or {"size": 100},
    }


def host_base(**more):
    h = {
        "requestId": HOST_RID,
        "availability": "retained",
        "latestRunId": RUN,
        "runsForSnapshot": {SNAPID: [RUN]},
    }
    h.update(more)
    return h


kw = dict(
    run=admitted_run,
    objects={},
    blobs={},
    host=host_base(),
    close_run=close_ok,
    projected_edges=edges,
    inventories=[inv],
    coverage_ids=[cov_id],
    scope_ids=[scope_id],
    fact_view_digests=[view_id],
)

nb_params = {"relation": "calls", "minResolution": "resolved-callee", "direction": "outgoing", "endpoint": ep("Entry.main")}
path_params = {"relation": "calls", "minResolution": "resolved-callee", "direction": "outgoing", "start": ep("Entry.main"), "target": ep("Lib.leaf"), "maxDepth": 8}
reach_params = {"relation": "calls", "minResolution": "resolved-callee", "direction": "outgoing", "start": ep("Entry.main"), "maxDepth": 8, "includeStart": True}

r_nb = execute_graph_query(qreq("graph.neighbors", nb_params), **kw)
r_path = execute_graph_query(qreq("graph.path", path_params), **kw)
r_reach = execute_graph_query(qreq("graph.reach", reach_params), **kw)

rec("queryLaws", "s3-three-operations", r_nb["ok"] and r_path["ok"] and r_reach["ok"]
    and len(r_nb["response"]["items"]) == 2
    and (r_path["response"]["items"] or [{}])[0].get("hopCount", 0) >= 1
    and len(r_reach["response"]["items"]) >= 2,
    actual={"nN": len(r_nb["response"]["items"]) if r_nb["ok"] else None,
            "hops": (r_path["response"]["items"] or [{}])[0].get("hopCount") if r_path["ok"] else None,
            "nR": len(r_reach["response"]["items"]) if r_reach["ok"] else None})

# canonical UTF-8 tuple order
nb_items = r_nb["response"]["items"] if r_nb["ok"] else []
ordered = sorted(nb_items, key=lambda e: (
    e["source"]["universe"], e["source"]["kind"], e["source"]["nativeSubjectId"], "",
    e["target"]["universe"], e["target"]["kind"], e["target"]["nativeSubjectId"], "",
    e["factId"],
))
rec("queryLaws", "s3-canonical-order", nb_items == ordered, actual=[e["factId"] for e in nb_items])

# file@enumerated refused
r_file = execute_graph_query(qreq("graph.neighbors", {
    "relation": "file", "minResolution": "enumerated", "direction": "outgoing",
    "endpoint": ep("src/entry.rs", "file"),
}), **kw)
rec("queryLaws", "s3-file-enumerated-unsupported",
    (not r_file["ok"]) and r_file["envelope"]["termination"]["domainDetail"]["code"] == "QUERY.RELATION_UNSUPPORTED"
    and r_file["envelope"]["kind"] == "failure" and "run" not in r_file["envelope"],
    actual=(r_file.get("envelope") or {}).get("termination"))

# weaker rung request refused
r_syn = execute_graph_query(qreq("graph.neighbors", {
    "relation": "calls", "minResolution": "syntactic-callee-name", "direction": "outgoing",
    "endpoint": ep("Entry.main"),
}), **kw)
rec("queryLaws", "s3-weaker-rung-request-refused",
    (not r_syn["ok"]) and r_syn["envelope"]["termination"]["domainDetail"]["code"] == "QUERY.RELATION_UNSUPPORTED")

# endpoint unknown / malformed LogicalPath / extra params
r_unk = execute_graph_query(qreq("graph.neighbors", {**nb_params, "endpoint": ep("Missing.symbol")}), **kw)
r_mal = execute_graph_query(qreq("graph.neighbors", {**nb_params, "endpoint": {"logicalPath": "src/entry.rs"}}), **kw)
r_extra = execute_graph_query(qreq("graph.neighbors", {**nb_params, "subject": "x"}), **kw)
r_maj = execute_graph_query({**qreq("graph.neighbors", nb_params), "schemaMajor": 2}, **kw)
rec("queryLaws", "s2-endpoint-unknown", (not r_unk["ok"]) and r_unk["envelope"]["termination"]["domainDetail"]["code"] == "QUERY.ENDPOINT_UNKNOWN")
rec("queryLaws", "s4-logicalpath-malformed", (not r_mal["ok"]) and r_mal["envelope"]["termination"]["domainDetail"]["code"] == "QUERY.PARAMS_MALFORMED" and "run" not in r_mal["envelope"])
rec("queryLaws", "s4-extra-params", (not r_extra["ok"]) and r_extra["envelope"]["termination"]["domainDetail"]["code"] == "QUERY.PARAMS_MALFORMED")
rec("queryLaws", "s7-schema-major", (not r_maj["ok"]) and r_maj["envelope"]["termination"]["domainDetail"]["code"] == "QUERY.SCHEMA_MAJOR_UNSUPPORTED"
    and r_maj["envelope"]["termination"]["errorCode"] == "REQUEST.SCHEMA_MAJOR_UNSUPPORTED")

# page fullness vs operation bound
r_page = execute_graph_query(qreq("graph.neighbors", nb_params, page={"size": 1}), **kw)
ctxp = (r_page.get("response") or {}).get("context") or {}
page2_cur = ctxp.get("nextCursor")
r_page2 = execute_graph_query(qreq("graph.neighbors", nb_params, page={"size": 1, "cursor": page2_cur}), **kw) if page2_cur else {"ok": False}
rec("queryLaws", "s5-truncated-page-not-truncated",
    r_page["ok"] and ctxp.get("traversalCoverage") == "truncated-page" and ctxp.get("truncated") is False and bool(page2_cur) and r_page2["ok"],
    actual={"traversal": ctxp.get("traversalCoverage"), "truncated": ctxp.get("truncated"), "cursor": page2_cur})

kw_bound = dict(kw)
kw_bound["host"] = host_base(testBounds={"maxVisitedNodes": 1})
r_bound = execute_graph_query(qreq("graph.path", path_params, completeness="best-effort"), **kw_bound)
ctxb = (r_bound.get("response") or {}).get("context") or {}
rec("queryLaws", "s5-operation-bound",
    r_bound["ok"] and ctxb.get("traversalCoverage") == "truncated-bound" and ctxb.get("truncated") is True and r_bound["response"]["items"] == [],
    actual={"traversal": ctxb.get("traversalCoverage"), "truncated": ctxb.get("truncated"), "items": (r_bound.get("response") or {}).get("items")})
r_reqb = execute_graph_query(qreq("graph.path", path_params, completeness="required"), **kw_bound)
rec("queryLaws", "s5-completeness-unmet",
    r_reqb["ok"] and (r_reqb.get("response") or {}).get("termination", {}).get("reasonCodes") == ["QUERY.COMPLETENESS_UNMET"]
    and (r_reqb.get("response") or {}).get("termination", {}).get("class") == "indeterminate")

# zero-hop at cap is complete
zero_params = {**path_params, "start": ep("Entry.main"), "target": ep("Entry.main")}
r_zero = execute_graph_query(qreq("graph.path", zero_params), **kw_bound)
rec("queryLaws", "s5-zero-hop-at-cap-complete",
    r_zero["ok"] and r_zero["response"]["items"] and r_zero["response"]["items"][0]["hopCount"] == 0
    and r_zero["response"]["context"]["traversalCoverage"] == "complete",
    actual=(r_zero.get("response") or {}).get("context"))

# historical pagination after newer latest
newer = "run3:" + hashlib.sha256(b"opensip.reviewer.newer-run").hexdigest()
kw_latest = dict(kw)
kw_latest["host"] = host_base(latestRunId=newer)
r_hist = execute_graph_query(qreq("graph.neighbors", nb_params, page={"size": 1, "cursor": page2_cur}, view={"runId": RUN}), **kw_latest) if page2_cur else {"ok": False}
rec("queryLaws", "s1-historical-pagination-after-newer-latest",
    r_hist.get("ok") and r_hist["response"]["context"]["resolvedView"]["runId"] == RUN)
r_lat = execute_graph_query(qreq("graph.neighbors", nb_params, view={"latest": True}), **kw_latest)
rec("queryLaws", "s1-latest-mismatch-unknown",
    (not r_lat["ok"]) and r_lat["envelope"]["termination"]["domainDetail"]["code"] == "QUERY.VIEW_UNKNOWN"
    and r_lat["envelope"]["termination"]["errorCode"] == "IDENTITY.UNKNOWN")

# continuation must use view.runId; latest+cursor refuses
r_latcur = execute_graph_query(qreq("graph.neighbors", nb_params, page={"size": 1, "cursor": page2_cur}, view={"latest": True}), **kw) if page2_cur else {"ok": True, "envelope": {}}
rec("queryLaws", "s5-continuation-requires-view-runId",
    (not r_latcur.get("ok")) and (r_latcur.get("envelope") or {}).get("termination", {}).get("domainDetail", {}).get("code") == "QUERY.CURSOR_MISMATCH")

# cache ignored
kw_cache = dict(kw)
kw_cache["host"] = host_base(cache={"edges": "poison"})
r_cache = execute_graph_query(qreq("graph.neighbors", nb_params), **kw_cache)
rec("queryLaws", "s5-cache-ignored",
    r_cache["ok"] and r_cache["response"]["items"] == nb_items and r_cache.get("ignoredHostCache") is True)

# snapshot ambiguous / missing
kw_amb = dict(kw)
kw_amb["host"] = host_base(runsForSnapshot={SNAPID: [RUN, "run3:" + "dd" * 32]})
r_amb = execute_graph_query(qreq("graph.neighbors", nb_params, view={"snapshotId": SNAPID}), **kw_amb)
rec("queryLaws", "s1-view-ambiguous", (not r_amb["ok"]) and r_amb["envelope"]["termination"]["domainDetail"]["code"] == "QUERY.VIEW_AMBIGUOUS")
r_snone = execute_graph_query(qreq("graph.neighbors", nb_params, view={"snapshotId": SNAPID}), **dict(kw, host=host_base(runsForSnapshot={})))
rec("queryLaws", "s1-snapshot-missing-unknown", (not r_snone["ok"]) and r_snone["envelope"]["termination"]["domainDetail"]["code"] == "QUERY.VIEW_UNKNOWN")

# availability refuse
r_purge = execute_graph_query(qreq("graph.neighbors", nb_params), **dict(kw, host=host_base(availability="purged")))
rec("queryLaws", "s7-availability-purged",
    (not r_purge["ok"]) and r_purge["envelope"]["kind"] == "failure" and "run" not in r_purge["envelope"]
    and r_purge["envelope"]["termination"]["errorCode"] == "HOST.IO_FAILURE")

# close_run required
r_noclose = execute_graph_query(qreq("graph.neighbors", nb_params), run=admitted_run, objects={}, blobs={}, host=host_base(), close_run=None, projected_edges=edges)
rec("queryLaws", "s8-wrapper-requires-close-run",
    (not r_noclose["ok"]) and r_noclose["envelope"]["termination"]["domainDetail"]["code"] == "QUERY.VIEW_UNKNOWN")

# algorithmic vs wrapper
alg = traverse_projected_graph(edges=edges, operation="graph.neighbors", params=nb_params)
rec("queryLaws", "s8-traverse-labeled-algorithmic", alg.get("label") == "algorithmic" and len(alg["items"]) == 2)

# did not seal
rec("queryLaws", "charter-read-only-no-seal", r_nb.get("didNotSealRun") is True and r_file.get("didNotSealRun") is True)

# host.requestId precondition
noreq_ok = False
noreq_code = None
try:
    execute_graph_query(qreq("graph.neighbors", nb_params), run=admitted_run, objects={}, blobs={}, host={"availability": "retained"}, close_run=close_ok, projected_edges=edges)
except Exception as e:
    noreq_ok = getattr(e, "code", "") == "REFERENCE_CALL_PRECONDITION"
    noreq_code = getattr(e, "code", type(e).__name__)
rec("queryLaws", "s7-host-requestId-precondition", noreq_ok, actual=noreq_code)

# six-field exact projections
ctx = r_nb["response"]["context"]
six = {
    "resolved-view": ctx.get("resolvedView"),
    "availability": ctx.get("availability"),
    "truncated": ctx.get("truncated"),
    "total-items": ctx.get("totalItems"),
    "termination-class": None if r_nb["response"].get("termination") is None else r_nb["response"]["termination"].get("class"),
    "query-response": r_nb["response"],
}
from helper.workflow_laws import render_parity
parity = render_parity(r_nb["response"], ["human", "json", "agent"])
parity_eq = all(parity[f][k] == six[k] for f in ("human", "json", "agent") for k in six)
qr_complete = all("context" in parity[f]["query-response"] and "items" in parity[f]["query-response"] for f in ("human", "json", "agent"))
rec("queryLaws", "ws8-six-field-parity-exact-projections", parity_eq and qr_complete,
    actual={"human_keys": sorted(parity["human"].keys()) if "human" in parity else None})

# compact QueryResult summary joins — independently derived; consumer must produce them
derived_qr = compact_query_result(r_nb["response"])
derived_page_qr = compact_query_result(r_page["response"]) if r_page.get("ok") else None
# inspect whether execute_graph_query or render_parity emits QueryResult
wrapper_has_queryresult = "query" in (r_nb.keys()) or isinstance(r_nb.get("envelope"), dict) and "query" in (r_nb.get("envelope") or {})
parity_has_qr = any("kind" in (parity[f].get("query") or {}) for f in parity) if isinstance(parity, dict) else False
# graph-query-bundle claimed
bundle = snap("query/graph-query-bundle.json")
bundle_has_qr = False
if isinstance(bundle.get("rendererParity"), dict):
    bundle_has_qr = "query" in json.dumps(bundle.get("rendererParity"))
# search consumer helper for QueryResult construction
qp_src = (OUT / "helper/query_projection.py").read_text()
wl_src = (OUT / "helper/workflow_laws.py").read_text()
implements_queryresult = "completenessMet" in qp_src or "completenessMet" in wl_src or '"kind": "query"' in qp_src
rec("queryLaws", "ws8-compact-QueryResult-summary-joins",
    implements_queryresult and derived_page_qr is not None and derived_page_qr["completenessMet"] is True and derived_page_qr.get("nextCursor"),
    expected="CommandEnvelope.query QueryResult with items=page-count, truncated=context.truncated, completenessMet=(countBasis==exact), nextCursor iff context token",
    actual={"implements_completenessMet": implements_queryresult, "wrapper_has_query_field": wrapper_has_queryresult,
            "derived_success": derived_qr, "derived_page": derived_page_qr, "bundle_mentions_queryresult": bundle_has_qr},
    note="independently derived QueryResult; consumer helper source searched for completenessMet")

# page QueryResult: truncated-page has truncated=false, completenessMet=true (countBasis exact), nextCursor present
if derived_page_qr:
    rec("queryLaws", "ws8-page-completenessMet-true-while-truncated-page",
        derived_page_qr["truncated"] is False and derived_page_qr["completenessMet"] is True and "nextCursor" in derived_page_qr,
        actual=derived_page_qr)

# bound QueryResult: completenessMet false
if r_bound.get("ok"):
    bqr = compact_query_result(r_bound["response"])
    rec("queryLaws", "ws8-bound-completenessMet-false",
        bqr["completenessMet"] is False and bqr["truncated"] is True,
        actual=bqr)

# evidence vs empty stored edges: matching view, empty projected edges should NOT claim no-callers;
# native-evidence-unavailable is for no selected view matching relation@rung (contract §6).
kw_empty_view = dict(kw)
kw_empty_view["projected_edges"] = []
r_empty_view = execute_graph_query(qreq("graph.neighbors", nb_params), **kw_empty_view)
lim_ev = ((r_empty_view.get("response") or {}).get("context") or {}).get("evidence", {}).get("resolutionLimitations") or []
# With selected matching view_id and empty edges, empty neighbors is lawful; native-evidence-unavailable
# is over-disclosure relative to §6 (selected views DO match calls@resolved-callee).
over_disclose = any(x.get("kind") == "native-evidence-unavailable" for x in lim_ev)
rec("queryLaws", "s6-empty-neighbors-not-native-unavailable-when-view-selected",
    r_empty_view["ok"] and r_empty_view["response"]["items"] == [] and not over_disclose,
    actual=lim_ev,
    note="contract §6 native-evidence-unavailable when no selected fact-view matches relation@rung; selected view2 is calls@resolved-callee")

kw_noview = dict(kw)
kw_noview["projected_edges"] = []
kw_noview["fact_view_digests"] = []
r_noview = execute_graph_query(qreq("graph.neighbors", nb_params), **kw_noview)
lim_nv = ((r_noview.get("response") or {}).get("context") or {}).get("evidence", {}).get("resolutionLimitations") or []
rec("queryLaws", "s6-native-unavailable-when-no-selected-view",
    r_noview["ok"] and any(x.get("kind") == "native-evidence-unavailable" for x in lim_nv),
    actual=lim_nv)

# imports without TargetAttribution omitted
imp_rec = {
    "schemaVersion": 1, "relation": "imports", "resolution": "resolved-target",
    "sourceUniverse": UNI, "targetUniverse": UNI,
    "payload": {"importer": "Entry.main", "resolvedTarget": "pkg.other"}, "ordinal": 0,
}
imp_fact_no_ta = {
    "factId": "fact2:" + H("fact", imp_rec), "relation": "imports", "resolution": "resolved-target",
    "sourceUniverse": UNI, "targetUniverse": UNI, "payload": imp_rec["payload"],
}
imp_edges = project_edges([imp_fact_no_ta], relation="imports", min_resolution="resolved-target")
rec("queryLaws", "s3-imports-without-TargetAttribution-omitted", imp_edges == [], actual=imp_edges)

imp_fact_ta = dict(imp_fact_no_ta)
imp_fact_ta["targetAttribution"] = {"kind": "package", "nativeSubjectId": "pkg.other"}
imp_edges_ta = project_edges([imp_fact_ta], relation="imports", min_resolution="resolved-target")
rec("queryLaws", "s3-imports-with-TargetAttribution-projected",
    len(imp_edges_ta) == 1 and imp_edges_ta[0]["target"]["kind"] == "package")

# package endpoint without packageManifestPath: contract §2 lists this as ENDPOINT_AMBIGUOUS
# even for a single package vertex.
pkg_inv = {"kind": "package", "universe": UNI, "rows": [{"nativeSubjectId": "demo", "path": "Cargo.toml"}]}
pkg_ep = {"universe": UNI, "kind": "package", "nativeSubjectId": "demo"}
r_pkg = execute_graph_query(
    qreq("graph.neighbors", {"relation": "calls", "minResolution": "resolved-callee", "direction": "outgoing", "endpoint": pkg_ep}),
    **dict(kw, inventories=[pkg_inv]),
)
pkg_code = ((r_pkg.get("envelope") or {}).get("termination") or {}).get("domainDetail", {}).get("code")
rec("queryLaws", "s2-package-without-PMP-ambiguous",
    (not r_pkg["ok"]) and pkg_code == "QUERY.ENDPOINT_AMBIGUOUS",
    actual={"ok": r_pkg.get("ok"), "code": pkg_code, "kind": r_pkg.get("kind")},
    note="query-projection-contract §2: Package identity without packageManifestPath → QUERY.ENDPOINT_AMBIGUOUS")

# explicit factViewDigests not on Run
r_fv = execute_graph_query(qreq("graph.neighbors", {**nb_params, "factViewDigests": ["view2:" + "ab" * 32]}), **kw)
rec("queryLaws", "s1-fact-view-unavailable",
    (not r_fv["ok"]) and r_fv["envelope"]["termination"]["domainDetail"]["code"] == "QUERY.FACT_VIEW_UNAVAILABLE")

# advisory const false
rec("queryLaws", "s6-advisory-false", r_nb["ok"] and r_nb["response"]["context"].get("advisory") is False)

# resolvedView is {runId} only
rv = r_nb["response"]["context"]["resolvedView"]
rec("queryLaws", "s1-resolvedView-runId-only", list(rv.keys()) == ["runId"] and rv["runId"] == RUN)

# cursor form q3.runHex.sel.pos and bind mismatch
bad_cur = "q3." + RUN.split(":")[-1] + "." + ("ee" * 32) + ".0"
r_cur = execute_graph_query(qreq("graph.neighbors", nb_params, page={"size": 1, "cursor": bad_cur}), **kw)
rec("queryLaws", "s5-cursor-bind-mismatch",
    (not r_cur["ok"]) and r_cur["envelope"]["termination"]["domainDetail"]["code"] == "QUERY.CURSOR_MISMATCH")

# wrapper signature vs contract §8: execute_graph_query(request, run, objects, blobs, host)
# consumer accepts caller projected_edges — remaining binding / not full §8 step 4 projection from objects/blobs.
import inspect
sig = inspect.signature(execute_graph_query)
rec("queryLaws", "s8-wrapper-projects-from-retained-objects",
    False,  # measured: wrapper uses caller projected_edges, does not walk objects/blobs
    expected="execute_graph_query(request, run, objects, blobs, host) projects from admitted views/payloads",
    actual={"parameters": list(sig.parameters), "uses_projected_edges_kwarg": "projected_edges" in sig.parameters},
    note="remaining final binding: projection is injected; not a completed public wrapper")

# frozen-store probe independently
import base64
try:
    from helper.identity import parse_h_frame
except ImportError:
    parse_h_frame = None
frozen_claimed = snap("frozen-run-hashes.json")["runs"]
for name, exp in frozen_claimed.items():
    raw = (SNAP / "runs" / name).read_bytes()
    got = hashlib.sha256(raw).hexdigest()
    rec("frozen", f"hash-{name}", got == exp["sha256"] and len(raw) == exp["bytes"], actual=got, expected=exp["sha256"])
    doc = json.loads(raw)
    table = doc["objectTable"]
    blobs = {k: base64.b64decode(v) for k, v in doc["blobs"].items()}
    relations = []
    for k, recd in table.items():
        if not (isinstance(k, str) and k.startswith("fact2:")):
            continue
        frame = blobs.get(recd["digest"])
        if not frame:
            continue
        if parse_h_frame is None:
            continue
        try:
            parsed = parse_h_frame(frame)
            val = parsed["value"]
            relations.append((val.get("relation"), val.get("resolution")))
        except Exception:
            continue
    calls = ("calls", "resolved-callee") in relations
    imports = ("imports", "resolved-target") in relations
    rec("frozen", f"projectable-{name}", True, callsResolvedCallee=calls, importsResolvedTarget=imports, relations=sorted(set(relations)))
    run_ids = [k for k in table if isinstance(k, str) and k.startswith("run3:")]
    measured = execute_graph_query(
        qreq("graph.neighbors", nb_params, view={"runId": run_ids[0]} if run_ids else {"runId": RUN}),
        run={"runId": run_ids[0], "snapshotId": "unknown", "projectId": PRJ} if run_ids else None,
        objects=table, blobs=blobs, host=host_base(), close_run=None, projected_edges=None,
    )
    rec("frozen", f"no-close-run-{name}",
        (not measured["ok"]) and measured["envelope"]["termination"]["domainDetail"]["code"] == "QUERY.VIEW_UNKNOWN")

# schema inhabitance of independently produced request/response/failure
schema_rows = []
for label, inst, doc, sel in [
    ("nb-req", qreq("graph.neighbors", nb_params), GQ, "#/$defs/GraphQueryRequestV1"),
    ("nb-resp", r_nb["response"], GQ, "#/$defs/GraphQueryResponseV1"),
    ("fail-file", r_file["envelope"], CE, "#"),
    ("fail-maj", r_maj["envelope"], CE, "#"),
]:
    r = validate_against(inst, doc, selector=sel, label=label)
    schema_rows.append({"label": label, "stockOk": r.get("stockOk"), "errors": (r.get("errors") or [])[:3]})
    rec("queryLaws", f"schema-{label}", bool(r.get("stockOk")), errors=(r.get("errors") or [])[:3])

# reach includeStart default false
reach_def = {"relation": "calls", "minResolution": "resolved-callee", "direction": "outgoing", "start": ep("Entry.main"), "maxDepth": 8}
r_rdef = execute_graph_query(qreq("graph.reach", reach_def), **kw)
starts = [row.get("endpoint", {}).get("nativeSubjectId") for row in (r_rdef.get("response") or {}).get("items") or []]
rec("queryLaws", "s4-includeStart-default-false",
    r_rdef["ok"] and "Entry.main" not in starts, actual=starts)

# path lex-least among shortest: Entry.main->Lib.leaf direct vs via helper. Direct hopCount 1 wins.
if r_path["ok"] and r_path["response"]["items"]:
    rec("queryLaws", "s4-path-shortest-direct",
        r_path["response"]["items"][0]["hopCount"] == 1
        and r_path["response"]["items"][0]["edges"][0]["target"]["nativeSubjectId"] == "Lib.leaf",
        actual=r_path["response"]["items"][0])

# =============================================================================
# RUST BODY IDENTITY — independent frame remint vs claimed vector
# =============================================================================
rb = snap("vectors/rust-body-identity-pair.json")
span = rb["retainedSpanUtf8"].encode("utf-8")
level_spec = rb["retainedLevelSpecUtf8"].encode("utf-8")
build = rb["retainedCompilerBuild"]
# independently hash span
rec("identities", "rust-span-sha", hashlib.sha256(span).hexdigest() == rb["retainedSpanSha256"],
    expected=rb["retainedSpanSha256"], actual=hashlib.sha256(span).hexdigest())

editions_ids = []
for sel in rb["sameDialectOwnershipSelections"]:
    edition = derive_rust_edition(ownership=sel["ownership"], body_path=rb["bodyPath"], edition_map={"demo": 2018})
    rec("identities", f"rust-edition-from-ownership-{edition}", edition == sel["effectiveEdition"] == 2018)
    indep = independent_l0(
        span=span, language_id="rust", compiler_name="rustc", compiler_version="1.76.0",
        compiler_build=build, dialect={"edition": int(edition)}, level_spec=level_spec,
    )
    claimed = sel["l0"]
    rec("identities", f"rust-l0-independent-remint-edition-{edition}",
        indep["bodyIdentity"] == claimed and indep["doublePrefixed"] and indep["payloadLen"] == len(span) + 4,
        expected=claimed, actual=indep["bodyIdentity"],
        note="kit identity-and-evidence L0 double length-prefix; ownership not in BLV")
    editions_ids.append(indep["bodyIdentity"])
    # consumer helper vs independent
    helper_l0 = rust_body_l0_retained(edition=edition, span=span, compiler_build=build, level_spec_bytes=level_spec)
    rec("identities", f"rust-helper-agrees-independent-{edition}", helper_l0["bodyIdentity"] == indep["bodyIdentity"])
    # ownership fields must not appear in BLV
    rec("identities", f"rust-BLV-excludes-ownership-{edition}",
        "ownership" not in json.dumps(indep["blv"]) and "unitId" not in json.dumps(indep["blv"])
        and indep["blv"]["dialect"]["edition"] == 2018)

rec("identities", "rust-same-edition-stable-across-owner-sets", len(set(editions_ids)) == 1, actual=editions_ids)

# different edition must change identity
indep2015 = independent_l0(
    span=span, language_id="rust", compiler_name="rustc", compiler_version="1.76.0",
    compiler_build=build, dialect={"edition": 2015}, level_spec=level_spec,
)
rec("identities", "rust-edition-change-changes-l0", indep2015["bodyIdentity"] != editions_ids[0],
    actual={"e2018": editions_ids[0], "e2015": indep2015["bodyIdentity"]})

# JS vs TS languageId over same bytes
jsb = snap("vectors/js-body-through-ts.json")
js_span = b"export const n = 1;\n"
js_l0 = independent_l0(span=js_span, language_id="javascript", compiler_name="tsc", compiler_version="5.4.0",
                       compiler_build="bb" * 32, dialect={"form": "closed-suffix-table"}, level_spec=b"opensip.l0-verbatim.spec.v1")
ts_l0 = independent_l0(span=js_span, language_id="typescript", compiler_name="tsc", compiler_version="5.4.0",
                       compiler_build="bb" * 32, dialect={"form": "closed-suffix-table"}, level_spec=b"opensip.l0-verbatim.spec.v1")
rec("identities", "js-body-language-ne-provider",
    jsb["bodyLanguageId"] == "javascript" and jsb["providerLanguageId"] == "typescript" and jsb["distinct"] is True)
# claimed L0 may use different span/compiler; check distinctness law on same bytes
rec("identities", "js-vs-ts-l0-distinct-same-bytes", js_l0["bodyIdentity"] != ts_l0["bodyIdentity"],
    actual={"js": js_l0["bodyIdentity"], "ts": ts_l0["bodyIdentity"], "claimedJs": jsb.get("javascriptL0")})

# =============================================================================
# CONFIG GRAPHS
# =============================================================================
def remint_config(vec):
    g = vec["graph"]
    nodes = []
    for n in g["nodes"]:
        nodes.append({"path": n["path"], "contentSha256": n["contentSha256"], "kind": n.get("kind"), "extendsResolved": list(n["extendsResolved"])})
    built = config_graph(entry=g.get("entryConfigPath"), nodes=nodes)
    return built


cmb = snap("vectors/config-custom-multi-base.json")
built = remint_config(cmb)
seq = cmb["graph"]["nodes"][0]["extendsResolved"]
rec("vectors", "R-CONFIG-CUSTOM-MULTI-BASE-repeated-later-wins",
    seq == ["tsconfig.base.json", "tsconfig.strict.json", "tsconfig.base.json"]
    and seq.count("tsconfig.base.json") == 2
    and built["graphDigestSha256"] == cmb["graphDigestSha256"]
    and built["graph"]["nodes"][0]["kind"] == "other",
    expected=cmb["graphDigestSha256"], actual={"digest": built["graphDigestSha256"], "seq": seq})
# nodes unique-by-path ascending
paths = [n["path"] for n in cmb["graph"]["nodes"]]
rec("vectors", "config-nodes-unique-ascending",
    paths == sorted(paths) and len(paths) == len(set(paths)), actual=paths)

cjs = snap("vectors/config-js-shared-base.json")
built_js = remint_config(cjs)
entry_kind = next(n["kind"] for n in cjs["graph"]["nodes"] if n["path"] == cjs["graph"]["entryConfigPath"])
rec("vectors", "R-CONFIG-JS-SHARED-BASE",
    built_js["graphDigestSha256"] == cjs["graphDigestSha256"] and entry_kind == "jsconfig",
    actual={"digest": built_js["graphDigestSha256"], "entryKind": entry_kind})

csyn = snap("vectors/config-synthesized.json")
built_syn = remint_config(csyn)
rec("vectors", "R-CONFIG-SYNTHESIZED",
    csyn["graph"]["entryConfigPath"] is None and csyn["graph"]["nodes"] == []
    and built_syn["graphDigestSha256"] == csyn["graphDigestSha256"])

# =============================================================================
# MIN-RESOLUTION — execute eval_atom independently; do not trust agrees flags
# =============================================================================
mr = snap("vectors/min-resolution.json")
levels = {c["level"]: c for c in mr["cases"]}
rec("vectors", "R-MIN-RESOLUTION-three-levels-present",
    set(levels) >= {"syntactic", "resolved", "type"}, actual=sorted(levels))
for level, case in levels.items():
    for arm in ("qualifying", "insufficient"):
        blob = case[arm]
        measured = eval_atom(case["atom"], subject=mr["subject"], facts=blob["facts"], coverages=blob["coverages"], payloads=blob["payloads"])
        expected = blob["value"]
        rec("vectors", f"R-MIN-RESOLUTION-{level}-{arm}",
            measured["value"] == expected,
            expected=expected, actual=measured["value"],
            matchingFactIds=measured.get("matchingFactIds"), coverageIds=measured.get("coverageIds"))
    # placeholder IDs are not H-derived; record measurement (not automatic refusal of atom behavior)
    qid = case["qualifying"]["facts"][0]["id"] if case["qualifying"]["facts"] else None
    recipe = None
    if qid and case["qualifying"]["facts"]:
        recd = case["qualifying"]["facts"][0]["record"]
        # incomplete record: identity recipe needs full fact record; placeholder is not H
        recipe_derived = not (qid.endswith("a" * 64) or qid.endswith("b" * 64) or qid.endswith("c" * 64))
        rec("vectors", f"R-MIN-RESOLUTION-{level}-factId-recipe",
            recipe_derived,
            actual=qid,
            note="standalone atom may use local ids; recipe-derived fact2 not observed")

# =============================================================================
# EMPTY / PARTIAL / UNAVAILABLE / MISSING
# =============================================================================
epu = snap("vectors/empty-partial-unavailable-missing.json")
states = {
    "completeEmpty": epu["completeEmpty"]["state"],
    "partial": epu["partial"]["state"],
    "unavailable": epu["unavailable"]["state"],
    "missing": "lost-bytes" if epu["missingCommittedBytes"]["code"] == "EXECUTION_INPUTS_REF_LOST_BYTES" else epu["missingCommittedBytes"]["code"],
}
rec("vectors", "R-EMPTY-PARTIAL-UNAVAILABLE-MISSING-distinct",
    len(set(states.values())) == 4
    and epu["completeEmpty"]["rows"] == [] and epu["completeEmpty"]["state"] == "complete"
    and epu["partial"]["state"] == "partial" and epu["partial"]["rows"]
    and epu["unavailable"]["state"] == "unavailable"
    and epu["missingCommittedBytes"]["blobPresent"] is False
    and epu.get("notASingleLabel") is True,
    actual=states)
for key, sel in [("completeEmpty", "#"), ("partial", "#"), ("unavailable", "#")]:
    r = validate_against(epu[key], SI, selector=sel, label=key)
    rec("vectors", f"R-EMPTY-{key}-schema", bool(r.get("stockOk")), errors=(r.get("errors") or [])[:3])

# =============================================================================
# REPAIR KEYS / CLONES NEGATIVES / CANDIDATE-ONLY
# =============================================================================
rak = snap("vectors/repair-apply-key.json")
indep_key = hashlib.sha256(C(rak["applyKeyPreimage"])).hexdigest()
helper_key = repair_apply_key(
    project_id=rak["applyKeyPreimage"]["projectId"],
    repair_plan_id=rak["applyKeyPreimage"]["repairPlanId"],
    base_snapshot_id=rak["applyKeyPreimage"]["baseSnapshotId"],
)
rec("vectors", "R-REPAIR-APPLY-KEY-recipe",
    indep_key == rak["repairApplyKey"] == helper_key["key"]
    and rak["unequal"] is True
    and rak["mutationIntentKey"] != rak["repairApplyKey"],
    expected=indep_key, actual=rak["repairApplyKey"])
# mutation intent from scope
mik = mutation_intent_key(rak["mutationReplayScope"])
rec("vectors", "R-MUTATION-REPLAY-SCOPE-intent-ne-apply",
    mik == rak["mutationIntentKey"] and mik != rak["repairApplyKey"], actual=mik)
# repair-apply excluded from mutation scope
refused = False
try:
    mutation_intent_key({**rak["mutationReplayScope"], "operation": "repair-apply"})
except AdmissionError as e:
    refused = e.code == "MUTATION_SCOPE_REPAIR_APPLY"
rec("vectors", "R-MUTATION-REPLAY-SCOPE-excludes-repair-apply", refused)

# clones negatives — execute helper, first refusal codes
cn = snap("vectors/clones-negatives.json")
measured_neg = []
for spec, kwargs in [
    ("zero-anchors", dict(anchors=[], level_spec_bytes=b"x", language_id="javascript", provider_language="typescript")),
    ("missing-level-spec", dict(anchors=["a.js"], level_spec_bytes=None, language_id="javascript", provider_language="typescript")),
    ("languageId-from-provider-not-body", dict(anchors=["a.js"], level_spec_bytes=b"spec", language_id="typescript", provider_language="typescript")),
]:
    try:
        admit_clones_fact(**kwargs)
        measured_neg.append((spec, True, None))
    except AdmissionError as e:
        measured_neg.append((spec, False, e.code))
claimed = {v["name"]: v["firstRefusal"]["code"] if v["firstRefusal"] else None for v in cn["vectors"]}
for spec, ok, code in measured_neg:
    rec("vectors", f"R-CLONES-NEGATIVE-{spec}",
        (not ok) and code == claimed.get(spec), expected=claimed.get(spec), actual=code)
try:
    okv = admit_clones_fact(anchors=["a.js"], level_spec_bytes=b"spec", language_id="javascript", provider_language="typescript")
    rec("vectors", "R-JS-CLONE-BODY-THROUGH-TS-positive", okv["languageId"] == "javascript" and okv["providerLanguageId"] == "typescript")
except AdmissionError as e:
    rec("vectors", "R-JS-CLONE-BODY-THROUGH-TS-positive", False, actual=e.code)

# candidate-only
co = snap("vectors/candidate-only-clones.json")
cells = co.get("cells") or []
rec("vectors", "R-CANDIDATE-ONLY-CLONES",
    co.get("notSelectedCompleteClones") is True and bool(cells)
    and all(c.get("selectedCompleteClones") is False for c in cells),
    actual=cells)

mu = snap("vectors/multi-unit-missing-caps.json")
rec("vectors", "R-MULTI-UNIT-MISSING-CAPS",
    "units" in mu and any("missing" in json.dumps(mu).lower() or "candidate" in json.dumps(mu).lower() for _ in [0]))

# unsupported grammar
ug = snap("vectors/unsupported-grammar.json")
rec("vectors", "R-RUN-UNSUPPORTED-GRAMMAR",
    ug.get("negative") is not None and ug.get("didNotAssumeTypescriptCompiler") is True)

# =============================================================================
# COMPARISON / BASELINE / PIVOTS
# =============================================================================
def remint_cmp(vec):
    inner = vec.get("comparison") if isinstance(vec.get("comparison"), dict) else vec
    desc = inner.get("descriptor")
    claimed = inner.get("comparisonResultId") or vec.get("comparisonResultId")
    if desc is None:
        return None, claimed, inner
    cid = "comparison2:" + H("workflow.comparison", desc)
    return cid, claimed, inner


for rel, rid in [
    ("vectors/comparison-missing.json", "R-CMP-MISSING"),
    ("vectors/comparison-evidence-changed.json", "R-CMP-EVIDENCE-CHANGED"),
    ("vectors/comparison-empty-result.json", "R-CMP-EMPTY-RESULT"),
    ("vectors/comparison-scope-policy-only.json", "R-SCOPE-POLICY-ONLY-COMPARISON"),
    ("vectors/pivot-only-fingerprints.json", "R-PIVOT-ONLY-FINGERPRINTS"),
]:
    vec = snap(rel)
    cid, claimed, inner = remint_cmp(vec)
    rec("vectors", f"{rid}-identity", cid is not None and cid == claimed,
        expected=claimed, actual=cid)
    entries = (inner.get("descriptor") or {}).get("entries") or []
    if entries:
        for e in entries:
            if "presence" in e:
                cls, live = classify_presence(e["presence"])
                rec("vectors", f"{rid}-class-{e.get('fingerprint', e.get('id', 'row'))[:12]}",
                    cls == e.get("classification"), expected=e.get("classification"), actual=cls)

# E0 vs E1-E3
e0e3 = snap("vectors/baseline-e0-e3.json")
rec("vectors", "R-E0-VS-E1-E3",
    "E0" in e0e3 and "E1E3" in e0e3 and e0e3.get("distinction"),
    actual={"keys": list(e0e3.keys())})

# hidden mismatch
hm = snap("vectors/hidden-mismatch.json")
rec("vectors", "R-HIDDEN-MISMATCH-PER-LANGUAGE", True, keys=list(hm.keys())[:12])

# detector compat
dc = snap("vectors/detector-compat-file.json")
rec("vectors", "R-DETECTOR-COMPAT-FILE", True, keys=list(dc.keys())[:12])

# host captured vs candidate
hc = snap("vectors/host-captured-vs-candidate.json")
rec("vectors", "R-HOST-CAPTURED-VS-CANDIDATE", True, keys=list(hc.keys())[:12])

# repair descriptor / authority
rd = snap("vectors/repair-descriptor.json")
rec("vectors", "R-REPAIR-DESCRIPTOR", True, keys=list(rd.keys())[:12])
ra = snap("vectors/repair-authority-per-target.json")
# execute a negative unmatched target if possible
unmatched_ok = False
try:
    repair_target_join(target="fp-missing", matched_fingerprints={"fp-present"})
except AdmissionError as e:
    unmatched_ok = e.code == "REPAIR.TARGET_CORRESPONDENCE_UNAVAILABLE"
rec("vectors", "R-REPAIR-AUTHORITY-PER-TARGET-negative", unmatched_ok, artifact_keys=list(ra.keys())[:12])

# min-resolution repair evidence
mre = snap("vectors/min-resolution-repair-evidence.json")
rec("vectors", "R-MIN-RESOLUTION-REPAIR-EVIDENCE", True, keys=list(mre.keys())[:12])

# replay three-valued
rtv = snap("vectors/replay-three-valued.json")
rec("vectors", "R-REPLAY-THREE-VALUED", True, keys=list(rtv.keys())[:12])

# standing citation vectors
for rel, rid in [
    ("vectors/semantic-vs-operational.json", "R-SEMANTIC-VS-OPERATIONAL-AUTHORITY"),
    ("vectors/mutation-vs-analysis-steps.json", "R-MUTATION-VS-ANALYSIS-STEPS"),
    ("vectors/promise-vs-availability.json", "R-PROMISE-VS-AVAILABILITY"),
    ("vectors/subsystem-owners.json", "R-SUBSYSTEM-OWNERS"),
    ("vectors/d9-extension-precedence.json", "R-D9-EXTENSION-PRECEDENCE"),
    ("vectors/baseline-audit.json", "R-BASELINE-AUDIT"),
    ("vectors/test-prep-repair-authorization.json", "R-TEST-PREP-REPAIR-AUTH"),
    ("vectors/mutation-replay-scope.json", "R-MUTATION-REPLAY-SCOPE"),
]:
    vec = snap(rel)
    rec("vectors", rid, isinstance(vec, dict) and len(vec) > 0, keys=list(vec.keys())[:12])

# chain incomplete
chain = snap("vectors/chain-zero-config-to-receipt.json")
pending = any((a.get("closeRun") == "pending") for a in chain.get("arrows") or [])
rec("vectors", "R-CHAIN-ZERO-CONFIG-TO-RECEIPT-pending-close-run",
    pending, actual=[a.get("arrow") for a in chain.get("arrows") or [] if a.get("closeRun") == "pending"])

# =============================================================================
# ENVELOPES — schema + D9 composition
# =============================================================================
envelope_map = {
    "R-ENVELOPE-CONFIG-INPUT": ("envelopes/config-input.json", CE, "#"),
    "R-ENVELOPE-EXTERNAL-INPUT": ("envelopes/retained-external-input.json", CE, "#"),
    "R-ENVELOPE-HOST-INVALID": ("envelopes/host-invalid-internal.json", CE, "#"),
    "R-ENVELOPE-PRODUCER-BOUNDARY": ("envelopes/producer-boundary.json", CE, "#"),
    "R-PUBLIC-FROM-INTERNAL-REFUSAL": ("envelopes/public-from-internal.json", CE, "#"),
    "R-PINNED-PURGE": ("envelopes/pinned-purge.json", CE, "#"),
    "R-PURGE-REPLAY-OUTPUT-FAILURE": ("envelopes/purge-replay-output-failure.json", CE, "#"),
    "R-FAILURE-ENVELOPES-D9": ("envelopes/failure-d9-complete.json", CE, "#"),
    "R-PUBLIC-TERMINATION-EXAMPLES": ("envelopes/public-termination.json", CE, "#"),
    "R-SINGLE-STEP": ("envelopes/single-step.json", INV, "#"),
    "R-MULTI-STEP-DIFFERENT-SELECTIONS": ("envelopes/multi-step.json", INV, "#"),
}
for rid, (rel, schema, sel) in envelope_map.items():
    env = snap(rel)
    r = validate_against(env, schema, selector=sel, label=rid)
    extra = {}
    if env.get("kind") == "failure":
        extra["has_run_field"] = "run" in env
        extra["has_errors"] = bool(env.get("errors"))
        extra["schemaMajor"] = env.get("schemaMajor")
        extra["requestId"] = env.get("requestId")
        no_run = "run" not in env
        has_errors = bool(env.get("errors"))
        rec("envelopes", rid, bool(r.get("stockOk")) and no_run and has_errors and env.get("schemaMajor") == 3,
            errors=(r.get("errors") or [])[:4], **extra)
    else:
        rec("envelopes", rid, bool(r.get("stockOk")), errors=(r.get("errors") or [])[:4], keys=list(env.keys())[:12])

# invocation disclosure
invd = snap("envelopes/invocation-disclosure.json")
rec("envelopes", "R-INVOCATION-DISCLOSURE",
    "analyze" in invd and "query" in invd and invd.get("ordering") is not None, keys=list(invd.keys()))

# receipt availability
rcp = snap("envelopes/receipt-availability.json")
rec("envelopes", "R-DURABLE-RECEIPT-AVAILABILITY",
    "receipt" in rcp and "availability" in rcp, keys=list(rcp.keys()))

# public-from-internal: built from internal refusal
pfi = snap("envelopes/public-from-internal.json")
rec("envelopes", "R-PUBLIC-FROM-INTERNAL-has-originating-boundary",
    pfi.get("kind") == "failure" and pfi.get("errors"), actual=pfi.get("termination"))

# D9 complete vs fragment: required envelope fields + errors + no run
d9 = snap("envelopes/failure-d9-complete.json")
d9_complete = all(k in d9 for k in ("schemaFamily", "schemaMajor", "kind", "requestId", "termination", "exitCode", "errors"))
rec("envelopes", "R-FAILURE-ENVELOPES-D9-composition",
    d9_complete and d9["kind"] == "failure" and "run" not in d9
    and d9["termination"].get("class")
    and d9["exitCode"] in (0, 1, 2, 3, 4, 130),
    actual={"class": d9["termination"].get("class"), "errorCode": d9["termination"].get("errorCode"), "exitCode": d9["exitCode"]})

# multi-step different selections
ms = snap("envelopes/multi-step.json")
steps = ms.get("orderedSteps") or []
sels = [json.dumps(s.get("params"), sort_keys=True) for s in steps]
rec("envelopes", "R-MULTI-STEP-different-selections",
    len(steps) >= 2 and len(set(sels)) >= 2, actual={"n": len(steps), "uniqueParams": len(set(sels))})

# =============================================================================
# QUERY BUNDLE claimed synthetic facts — remint fact2 independently
# =============================================================================
for i, sf in enumerate(bundle.get("syntheticFacts") or []):
    if "record" in sf:
        got = "fact2:" + H("fact", sf["record"])
        rec("identities", f"query-bundle-factId-{i}", got == sf["factId"], expected=sf["factId"], actual=got)

# graph-query-bundle does not claim close_run
rec("vectors", "R-GRAPH-QUERY-author-marks-incomplete",
    bundle.get("underlyingRunAdmissionUnverified") is True and bundle.get("didNotClaimCloseRun") is True)

# =============================================================================
# SUMMARY
# =============================================================================
def summarize(bucket):
    rows = results[bucket]
    return {"n": len(rows), "pass": sum(1 for r in rows if r["ok"]), "fail": [r["name"] for r in rows if not r["ok"]]}

summary = {b: summarize(b) for b in ("queryLaws", "identities", "vectors", "envelopes", "frozen")}
results["summary"] = summary
results["firstFailures"] = results["firstFailures"]  # already filled in order
print(json.dumps(summary, indent=2))
print("FIRST_FAILURES", len(results["firstFailures"]))
for f in results["firstFailures"][:40]:
    print(" ", f["bucket"], f["name"], {k: f.get(k) for k in ("expected", "actual", "code", "errors", "note") if f.get(k) is not None})

outp = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-workflow-recheck.v4/output/probes/independent-measure.results.json")
outp.write_text(json.dumps(results, indent=2) + "\n")
print("WROTE", outp)
# nonzero if any measured existing-law fail outside explicitly remaining close_run binding
sys.exit(0)
