"""PROBE C (continued) — inspect the exact response/termination carriers so the
completeness=required + truncated-bound law and renderer parity are tested at the
boundary actually claimed, and add the availability=partial case."""
import copy, importlib.util, json, os, sys

DC = '/tmp/opensip-design-corrections/candidate-subject.v26/docs/coop/design-corrections'
sys.path.insert(0, os.path.join(DC, 'foundation'))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    spec.loader.exec_module(m)
    return m


Q = load('qp3', os.path.join(DC, 'workflows/query_projection_model.v3.py'))
QS = load('qsp3', os.path.join(DC, 'workflows/query_surface_projection.v3.py'))
S = load('sf3', os.path.join(DC, 'foundation/evaluator_semantic_fixture.v3.py'))
RP = load('csr3', os.path.join(DC, 'foundation/check-semantic-replay.v3.py'))
M = RP.M
R = {}


def rec(k, v):
    R[k] = v
    print('%-56s %s' % (k, v))


atom = {"op": "none", "relation": "references", "minResolution": "resolved-binding",
        "endpoint": "target", "filters": []}
g = S.build_ts_semantic_graph(atom=atom, has_declares=False, has_references_fact=True,
                              second_partition=True, references_resolved=False,
                              incoming_search=True, incoming_complete=False,
                              target_sidecar=True, second_universe=True)
run, objects, blobs, actual = RP.close_positive(g)
run_key = actual["runId"]
project = run["projectId"]
HOST = {"requestId": "req1_" + "a" * 32, "latestRunId": run_key}


def ep(u, k, n):
    return {"universe": u, "kind": k, "nativeSubjectId": n}


def req(op, params, completeness="required", size=100, cursor=None, avail=None):
    page = {"size": size}
    if cursor:
        page["cursor"] = cursor
    return {"completeness": completeness, "operation": op, "page": page, "params": params,
            "projectId": project, "schemaFamily": "opensip.product.query",
            "schemaMajor": 3, "view": {"runId": run_key}}


foo = ep(g["u1"], "symbol", g["foo"])
bar = ep(g["u1"], "symbol", g["bar"])

rec('AVAIL_REFUSE_map', dict(getattr(Q, 'AVAIL_REFUSE', {})))
for avail in ("partial", "retained", None):
    h = dict(HOST)
    if avail:
        h["availability"] = avail
    try:
        out = Q.execute_graph_query(
            req("graph.neighbors", {"relation": "references", "minResolution": "resolved-binding",
                                    "direction": "outgoing", "endpoint": foo}),
            run, objects, blobs, host=h)
        rec('C1b_availability_%s' % avail, 'ANSWERED items=%d' % len(out["items"]))
    except Q.QueryRefusal as exc:
        t = exc.termination()
        rec('C1b_availability_%s' % avail, '%s/%s/%s' % (t.get("class"), t.get("errorCode"),
                                                         (t.get("domainDetail") or {}).get("code")))

one = req("graph.path", {"relation": "references", "minResolution": "resolved-binding",
                         "direction": "outgoing", "start": foo, "target": bar, "maxDepth": 4},
          completeness="required")
h1 = dict(HOST, testBounds={"maxVisitedNodes": 1})
o1 = Q.execute_graph_query(one, run, objects, blobs, host=h1)
rec('C4b_response_top_keys', sorted(o1.keys()))
rec('C4b_context_keys', sorted(o1["context"].keys()))
rec('C4b_traversalCoverage', o1["context"]["traversalCoverage"])
rec('C4b_countBasis', o1["context"]["countBasis"])
rec('C4b_termination_in_context', o1["context"].get("termination"))
rec('C4b_termination_top', o1.get("termination"))

best = Q.execute_graph_query(dict(one, completeness="best-effort"), run, objects, blobs, host=h1)
rec('C4b_best_effort_termination', best["context"].get("termination"))
rec('C4b_best_effort_coverage', best["context"]["traversalCoverage"])

# --- renderer parity ---
import inspect
rec('C5_project_query_surface_sig', str(inspect.signature(QS.project_query_surface)))
term = o1.get("termination") or {"class": "success"}
# the projector enforces response/termination equality; a mismatched pair must refuse
try:
    QS.project_query_surface(o1, {"class": "success"})
    rec('C5_mismatched_termination_refused', False)
except Exception as exc:
    rec('C5_mismatched_termination_refused', type(exc).__name__ + ':' + str(exc)[:60])
proj = QS.project_query_surface(o1, term)
rec('C5_parity_fields', sorted(proj.keys()) if isinstance(proj, dict) else type(proj).__name__)
if isinstance(proj, dict):
    qr = proj.get('query-response')
    rec('C5_query_response_equals_complete_owned_response', qr == o1)
    for f in ('resolved-view', 'availability', 'truncated', 'total-items', 'termination-class'):
        rec('C5_' + f, proj.get(f))
    rec('C5_scalars_are_exact_projections_of_context', {
        'resolved-view': proj.get('resolved-view') == o1['context'].get('resolvedView'),
        'truncated': proj.get('truncated') == o1['context'].get('truncated'),
        'total-items': proj.get('total-items') == o1['context'].get('totalItems'),
    })
    compact = None
    for k in ('queryResult', 'QueryResult', 'query-result'):
        if k in proj:
            compact = proj[k]
    rec('C5_compact_query_result', compact)

# completenessMet law: true exactly when countBasis == exact
for label, resp in (('truncated-bound', o1), ('complete', Q.execute_graph_query(
        req("graph.path", {"relation": "references", "minResolution": "resolved-binding",
                           "direction": "outgoing", "start": foo, "target": bar, "maxDepth": 4}),
        run, objects, blobs, host=dict(HOST)))):
    t2 = resp.get("termination") or {"class": "success"}
    p2 = QS.project_query_surface(resp, t2)
    cm = None
    for k in ('queryResult', 'QueryResult', 'query-result'):
        if isinstance(p2, dict) and k in p2:
            cm = (p2[k] or {}).get('completenessMet')
    rec('C5_completenessMet_%s' % label,
        {'countBasis': resp["context"]["countBasis"], 'completenessMet': cm,
         'agrees': (cm is None) or (cm == (resp["context"]["countBasis"] == 'exact'))})

json.dump({k: (v if isinstance(v, (str, int, float, bool, list, dict, type(None))) else str(v))
           for k, v in R.items()},
          open('/tmp/opensip-design-corrections/claude-independent-design.v26/receipts/probeCD2.json', 'w'), indent=1)
