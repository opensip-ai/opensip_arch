"""PROBE C+D — my own discriminating probes, not the authors' case list.

D  A FULLY REMINTED FALSE-RESULT GRAPH: mutate a semantic output, then remint every
   enclosing identity so the graph is internally hash-consistent, and show that
     * structural owner admission (open_run_closure) ADMITS it, and
     * complete replay (close_run) REFUSES it,
     * and that the public graph-query entry refuses it too, because it calls close_run.
   This separates the structural API from semantic authority.

C  The newly specified retained GRAPH QUERY boundary, at the boundary actually claimed:
   C1 availability selector: purged/expired/corrupt/unavailable => operational-failed / exit 4
      for graph.*, and the contrasting workflow-owned finding.show exit-2 route is NOT reused.
   C2 endpoint membership: well-formed tuple outside the vertex domain => ENDPOINT_UNKNOWN;
      an isolated admitted vertex => lawful EMPTY neighbours that is NOT an absence claim.
   C3 cursor bound: a cursor minted for one Run refused against another selection.
   C4 visited-node law AT the cap: zero-hop at maxVisitedNodes=1 is exactly-at-cap COMPLETE;
      a one-edge path at the same cap does not enter the target and, under
      completeness=required, terminates indeterminate with QUERY.COMPLETENESS_UNMET.
   C5 renderer parity: completenessMet true exactly when countBasis == exact, and the
      compact QueryResult agrees with the complete owned response context.
"""
import copy, hashlib, importlib.util, json, os, sys

DC = '/tmp/opensip-design-corrections/candidate-subject.v26/docs/coop/design-corrections'
sys.path.insert(0, os.path.join(DC, 'foundation'))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    spec.loader.exec_module(m)
    return m


Q = load('qp3', os.path.join(DC, 'workflows/query_projection_model.v3.py'))
S = load('sf3', os.path.join(DC, 'foundation/evaluator_semantic_fixture.v3.py'))
RP = load('csr3', os.path.join(DC, 'foundation/check-semantic-replay.v3.py'))
M = RP.M
R = {}


def rec(k, v):
    R[k] = v
    print('%-58s %s' % (k, v))


atom = {"op": "none", "relation": "references", "minResolution": "resolved-binding",
        "endpoint": "target", "filters": []}
g = S.build_ts_semantic_graph(atom=atom, has_declares=False, has_references_fact=True,
                              second_partition=True, references_resolved=False,
                              incoming_search=True, incoming_complete=False,
                              target_sidecar=True, second_universe=True,
                              **({"emit": True} if 'emit' in
                                 S.build_ts_semantic_graph.__code__.co_varnames else {}))
run, objects, blobs, actual = RP.close_positive(g)
run_key = actual["runId"]
project = run["projectId"]
rec('D0_positive_run_closes_under_complete_replay', run_key == M.close_run(run, objects, blobs))


def ep(u, kind, nid, pkg=None):
    e = {"universe": u, "kind": kind, "nativeSubjectId": nid}
    if pkg:
        e["packageManifestPath"] = pkg
    return e


def request(op, project_id, view, params, page=None, completeness="best-effort"):
    pg = {"size": 100}
    if page:
        if "pageSize" in page:
            pg["size"] = page["pageSize"]
        if "cursor" in page:
            pg["cursor"] = page["cursor"]
    return {"completeness": completeness, "operation": op, "page": pg, "params": params,
            "projectId": project_id, "schemaFamily": "opensip.product.query",
            "schemaMajor": 3, "view": view}


HOST = {"requestId": "req1_" + "a" * 32, "latestRunId": run_key}
foo_ep = ep(g["u1"], "symbol", g["foo"])
bar_ep = ep(g["u1"], "symbol", g["bar"])

# ---------------- D: fully reminted false-result graph ----------------
seal = objects[run["evaluationSealId"]][1]
proof = objects[seal["proofBundleId"]][1]
fid0 = proof["findingIds"][0] if proof.get("findingIds") else None
rec('D1_positive_finding_count', len(proof.get("findingIds") or []))


def remint_full(mutate):
    """Apply `mutate` to the proof, then remint proof -> evidence -> seal -> run so every
    enclosing identity is recomputed. The result is internally hash-consistent."""
    o = copy.deepcopy(objects)
    b = dict(blobs)
    sl = copy.deepcopy(o[run["evaluationSealId"]][1])
    pf = copy.deepcopy(o[sl["proofBundleId"]][1])
    ev = copy.deepcopy(o[run["evidenceId"]][1])
    mutate(pf, ev, o, b)
    pid = M.identifier("proof-bundle", pf)
    o[pid] = ("proof-bundle", pf)
    ev["proofBundleId"] = pid
    eid = M.identifier("semantic-evidence", ev)
    o[eid] = ("semantic-evidence", ev)
    sl["proofBundleId"] = pid
    sl["evidenceId"] = eid
    sl["verdict"] = pf["verdict"]
    sid = M.identifier("evaluation-seal", sl)
    o[sid] = ("evaluation-seal", sl)
    r2 = copy.deepcopy(run)
    r2["evidenceId"] = eid
    r2["evaluationSealId"] = sid
    return r2, o, b


def flip_verdict(pf, ev, o, b):
    pf["verdict"] = "pass" if pf["verdict"] != "pass" else "indeterminate"


def flip_predicate_value(pf, ev, o, b):
    """Same-count semantic mutation: flip one retained predicate proof value."""
    for p in pf.get("predicateProofs", []):
        if p.get("value") in ("true", "false", True, False):
            p["value"] = ("false" if p["value"] == "true" else
                          "true" if p["value"] == "false" else (not p["value"]))
            return
    raise AssertionError("no boolean-valued predicate proof to flip")


def drop_execution_deficiency(pf, ev, o, b):
    if pf.get("executionDeficiencies"):
        pf["executionDeficiencies"] = pf["executionDeficiencies"][1:]
    else:
        raise AssertionError("no execution deficiency to drop")


MUTATIONS = [("verdict-flipped", flip_verdict), ("predicate-value-flipped", flip_predicate_value)]
try:
    flip_predicate_value(copy.deepcopy(proof), None, None, None)
except AssertionError:
    MUTATIONS = [("verdict-flipped", flip_verdict)]
if proof.get("executionDeficiencies"):
    MUTATIONS.append(("execution-deficiency-dropped", drop_execution_deficiency))

for name, mut in MUTATIONS:
    r2, o2, b2 = remint_full(mut)
    try:
        M.open_run_closure(r2, o2, b2)
        structural = "ADMIT"
    except Exception as exc:
        structural = "REFUSE:" + str(exc)[:70]
    try:
        M.close_run(r2, o2, b2)
        semantic = "ADMIT"
    except Exception as exc:
        semantic = "REFUSE:" + type(exc).__name__ + ":" + str(exc)[:70]
    rec('D2_%s_reminted_runId_differs' % name, M.identifier("run", r2) != run_key)
    rec('D2_%s_structural_owner_admission' % name, structural)
    rec('D2_%s_complete_replay' % name, semantic)
    req = request("graph.neighbors", project, {"runId": M.identifier("run", r2)},
                  {"relation": "references", "minResolution": "resolved-binding",
                   "direction": "outgoing", "endpoint": foo_ep})
    try:
        Q.execute_graph_query(req, r2, o2, b2, host={"requestId": HOST["requestId"]})
        qres = "ANSWERED (graph boundary did NOT require complete replay)"
    except Q.QueryRefusal as exc:
        t = exc.termination()
        qres = "REFUSE %s/%s/%s exit=%s" % (t.get("class"), t.get("errorCode"),
                                            (t.get("domainDetail") or {}).get("code"), t.get("exitCode"))
    rec('D3_%s_graph_query_on_reminted_graph' % name, qres)

# ---------------- C1 availability selector ----------------
for avail in ("purged", "expired", "corrupt", "unavailable", "retained"):
    req = request("graph.neighbors", project, {"runId": run_key},
                  {"relation": "references", "minResolution": "resolved-binding",
                   "direction": "outgoing", "endpoint": foo_ep})
    h = dict(HOST, availability=avail)
    try:
        out = Q.execute_graph_query(req, run, objects, blobs, host=h)
        rec('C1_availability_%s' % avail, 'ANSWERED items=%d' % len(out["items"]))
    except Q.QueryRefusal as exc:
        t = exc.termination()
        rec('C1_availability_%s' % avail, '%s / %s / %s / exit %s' % (
            t.get("class"), t.get("errorCode"), (t.get("domainDetail") or {}).get("code"), t.get("exitCode")))

# ---------------- C2 endpoint membership ----------------
ghost = ep(g["u1"], "symbol", "sym:definitely-not-in-this-run")
req = request("graph.neighbors", project, {"runId": run_key},
              {"relation": "references", "minResolution": "resolved-binding",
               "direction": "outgoing", "endpoint": ghost})
try:
    Q.execute_graph_query(req, run, objects, blobs, host=HOST)
    rec('C2_unknown_endpoint', 'ANSWERED (no vertex-domain admission)')
except Q.QueryRefusal as exc:
    t = exc.termination()
    rec('C2_unknown_endpoint', '%s / %s / exit %s' % (t.get("errorCode"),
                                                      (t.get("domainDetail") or {}).get("code"), t.get("exitCode")))

req = request("graph.neighbors", project, {"runId": run_key},
              {"relation": "references", "minResolution": "resolved-binding",
               "direction": "incoming", "endpoint": foo_ep})
inc = Q.execute_graph_query(req, run, objects, blobs, host=HOST)
rec('C2_admitted_vertex_zero_rows_is_not_absence',
    'items=%d traversalCoverage=%s limitations=%s' % (
        len(inc["items"]), inc["context"]["traversalCoverage"],
        sorted({x.get("kind") for x in inc["context"]["evidence"]["resolutionLimitations"]})))

# ---------------- C3 cursor bound to the Run ----------------
req = request("graph.neighbors", project, {"runId": run_key},
              {"relation": "references", "minResolution": "resolved-binding",
               "direction": "outgoing", "endpoint": foo_ep}, page={"pageSize": 1})
p1 = Q.execute_graph_query(req, run, objects, blobs, host=HOST)
cur = p1["context"].get("nextCursor")
rec('C3_first_page', 'items=%d cursor=%s' % (len(p1["items"]), bool(cur)))
forged = Q.encode_cursor("run3:" + "9" * 64, "0" * 64, 0)
req2 = request("graph.neighbors", project, {"runId": run_key},
               {"relation": "references", "minResolution": "resolved-binding",
                "direction": "outgoing", "endpoint": foo_ep}, page={"pageSize": 1, "cursor": forged})
try:
    Q.execute_graph_query(req2, run, objects, blobs, host=HOST)
    rec('C3_foreign_cursor', 'ACCEPTED (cursor not bound)')
except Q.QueryRefusal as exc:
    t = exc.termination()
    rec('C3_foreign_cursor', '%s / %s' % (t.get("errorCode"), (t.get("domainDetail") or {}).get("code")))

# ---------------- C4 visited-node law AT the cap ----------------
zero = request("graph.path", project, {"runId": run_key},
               {"relation": "references", "minResolution": "resolved-binding",
                "direction": "outgoing", "start": foo_ep, "target": foo_ep, "maxDepth": 4},
               completeness="required")
h1 = dict(HOST, testBounds={"maxVisitedNodes": 1})
z = Q.execute_graph_query(zero, run, objects, blobs, host=h1)
rec('C4_zero_hop_at_cap_1',
    'items=%d hop=%s coverage=%s visited=%s countBasis=%s' % (
        len(z["items"]), z["items"][0]["hopCount"] if z["items"] else None,
        z["context"]["traversalCoverage"], z["context"]["visitedNodes"],
        z["context"]["countBasis"]))

one = request("graph.path", project, {"runId": run_key},
              {"relation": "references", "minResolution": "resolved-binding",
               "direction": "outgoing", "start": foo_ep, "target": bar_ep, "maxDepth": 4},
              completeness="required")
o1 = Q.execute_graph_query(one, run, objects, blobs, host=h1)
term = o1["context"].get("termination")
rec('C4_one_edge_at_cap_1',
    'items=%d coverage=%s visited=%s termination=%s reasons=%s' % (
        len(o1["items"]), o1["context"]["traversalCoverage"], o1["context"]["visitedNodes"],
        (term or {}).get("class"), (term or {}).get("reasonCodes")))

o2 = Q.execute_graph_query(
    request("graph.path", project, {"runId": run_key},
            {"relation": "references", "minResolution": "resolved-binding",
             "direction": "outgoing", "start": foo_ep, "target": bar_ep, "maxDepth": 4}),
    run, objects, blobs, host=dict(HOST))
rec('C4_one_edge_unbounded', 'items=%d coverage=%s countBasis=%s' % (
    len(o2["items"]), o2["context"]["traversalCoverage"], o2["context"]["countBasis"]))

# ---------------- C5 renderer parity ----------------
QS = load('qsp3', os.path.join(DC, 'workflows/query_surface_projection.v3.py'))
pub = [n for n in dir(QS) if not n.startswith('_')]
R['C5_query_surface_public'] = pub
parity = None
for fn in ('project_query_surface', 'project_surface', 'surface_for'):
    if hasattr(QS, fn):
        parity = fn
rec('C5_projection_entry', parity)
if parity:
    proj = getattr(QS, parity)(o2)
    rec('C5_parity_fields', sorted(proj.keys()) if isinstance(proj, dict) else type(proj).__name__)
    if isinstance(proj, dict) and 'query-response' in proj:
        rec('C5_query_response_is_complete_owned_response',
            proj['query-response'] == o2)
        qr = proj.get('QueryResult') or proj.get('queryResult')
        rec('C5_compact_QueryResult', qr)

json.dump({k: (v if isinstance(v, (str, int, float, bool, list, dict, type(None))) else str(v))
           for k, v in R.items()},
          open('/tmp/opensip-design-corrections/claude-independent-design.v26/receipts/probeCD.json', 'w'), indent=1)
