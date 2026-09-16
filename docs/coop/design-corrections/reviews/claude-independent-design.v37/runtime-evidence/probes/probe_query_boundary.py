"""Independent retained graph-query boundary probes over the actual source37 query owner (verified exact copy).

Q1 schema-first endpoint admission precedes Run presence, availability and vertex lookup.
Q2 package endpoints: complete tuples for two same-named packages are distinct; no ENDPOINT_AMBIGUOUS path.
Q3 availability mapping: purged/expired/corrupt/unavailable -> operational-failed HOST.IO_FAILURE exit 4 with
   the named detail; retained/partial/omitted neither refuse nor grant (corrupt bytes still refuse).
Q4 response parity: GraphQueryResponseV1 advisory cross-join for non-graph, non-advisory operations.
Q5 cursor binding and effective params; Q6 visit cap exactly-at-cap vs owed work.
Reference evidence only.
"""
import copy, importlib.util, json, sys, traceback

BASE = '/tmp/opensip-design-corrections/claude-independent-design.v37'
SRC = BASE + '/work/source37'
DC = SRC + '/docs/coop/design-corrections'
OUT = BASE + '/receipts/probe-query-boundary.json'


def load(name, path):
    s = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(s)
    sys.modules[name] = m
    s.loader.exec_module(m)
    return m


SR = load('q37_semantic_replay', DC + '/foundation/check-semantic-replay.v3.py')
S = SR.S
Q = load('q37_query', DC + '/workflows/query_projection_model.v3.py')
REQ_ID = 'req1_' + '9' * 32
res = {'standing': 'independent reviewer probe; reference evidence only; not qualification'}


def host(**kw):
    h = {'requestId': REQ_ID}
    h.update(kw)
    return h


def ep(universe, kind, nid, manifest=None):
    e = {'universe': universe, 'kind': kind, 'nativeSubjectId': nid}
    if manifest is not None:
        e['packageManifestPath'] = manifest
    return e


def req(op, project, view, params, completeness='required', size=100, cursor=None):
    r = {'schemaFamily': 'opensip.product.query', 'schemaMajor': 3, 'projectId': project, 'view': view,
         'operation': op, 'params': params, 'completeness': completeness, 'page': {'size': size}}
    if cursor:
        r['page']['cursor'] = cursor
    return r


def attempt(fn):
    try:
        v = fn()
        c = v['context']
        return {'result': 'ADMIT', 'items': len(v['items']), 'traversal': c['traversalCoverage'], 'countBasis': c['countBasis'],
                'visited': c['visitedNodes'], 'produced': c['producedItems'], 'nextCursor': c.get('nextCursor'),
                'termination': v['termination'], '_v': v}
    except Q.QueryRefusal as e:
        env = e.envelope()
        return {'result': 'REFUSE', 'errorCode': e.error_code, 'detail': e.detail, 'class': e.klass, 'exitCode': env['exitCode']}
    except Exception as e:
        return {'result': 'ERROR', 'type': type(e).__name__, 'error': str(e).split('\n')[0][:300]}


def strip(x):
    return {k: v for k, v in x.items() if k != '_v'}


# owner graph (two universes, target sidecar, incomplete incoming) as a retained Run
atom = {'op': 'none', 'relation': 'references', 'minResolution': 'resolved-binding', 'endpoint': 'target', 'filters': []}
g = S.build_ts_semantic_graph(atom=atom, has_declares=False, has_references_fact=True, second_partition=True,
                              references_resolved=False, incoming_search=True, incoming_complete=False,
                              target_sidecar=True, second_universe=True)
run, objects, blobs, actual = SR.close_positive(g)
rid, project = actual['runId'], run['projectId']
foo = ep(g['u1'], 'symbol', g['foo'])
REL = {'relation': 'references', 'minResolution': 'resolved-binding'}

# ---- Q1 schema-first
pkg_no_path = ep(g['u1'], 'package', 'dup')
q1 = {}
bad = req('graph.neighbors', project, {'runId': rid}, dict(REL, direction='outgoing', endpoint=pkg_no_path))
q1['package-without-manifest-no-run'] = strip(attempt(lambda: Q.execute_graph_query(bad, host=host())))
q1['package-without-manifest-purged-observation'] = strip(attempt(lambda: Q.execute_graph_query(bad, run, objects, blobs, host=host(availability='purged'))))
q1['package-without-manifest-valid-run'] = strip(attempt(lambda: Q.execute_graph_query(bad, run, objects, blobs, host=host())))
sym_with_path = ep(g['u1'], 'symbol', g['foo'], 'package.json')
bad2 = req('graph.neighbors', project, {'runId': rid}, dict(REL, direction='outgoing', endpoint=sym_with_path))
q1['symbol-with-manifest-path'] = strip(attempt(lambda: Q.execute_graph_query(bad2, run, objects, blobs, host=host())))
logical = req('graph.neighbors', project, {'runId': rid}, dict(REL, direction='outgoing', subject='src/a.ts'))
q1['logicalpath-only-subject'] = strip(attempt(lambda: Q.execute_graph_query(logical, run, objects, blobs, host=host())))
q1['expected'] = 'every row REFUSE request-rejected REQUEST.PRECONDITION_FAILED QUERY.PARAMS_MALFORMED exit 2'
q1['passed'] = all(v.get('detail') == 'QUERY.PARAMS_MALFORMED' and v.get('exitCode') == 2 for k, v in q1.items() if isinstance(v, dict))
res['Q1'] = q1

# ---- Q2 package endpoint identity on an actual package Run
q2 = {}
try:
    pg = S.build_package_graph()
    prun, pobj, pblob, pact = SR.close_positive(pg)
    pk = [i for i in pg['inputs']['population'].values() if i['kind'] == 'package']
    q2['packages'] = sorted((i['row']['nativeSubjectId'], i['row']['path']) for i in pk)
    dup = [i for i in pk if i['row']['nativeSubjectId'] == 'dup']
    table_pkg = sorted(k for k, v in Q.projection_table().items() if v['sourceKind'] == 'package' or 'package' in v['targetKinds'])
    q2['packageProjectableRelations'] = table_pkg
    for i in dup:
        for relation, rung in table_pkg[:1] or [('references', 'resolved-binding')]:
            r = req('graph.neighbors', prun['projectId'], {'runId': pact['runId']},
                    {'relation': relation, 'minResolution': rung, 'direction': 'both',
                     'endpoint': ep(i['universe'], 'package', 'dup', i['row']['path'])})
            q2['dup@' + i['row']['path']] = strip(attempt(lambda: Q.execute_graph_query(r, prun, pobj, pblob, host=host())))
    if dup:
        i = dup[0]
        relation, rung = (table_pkg[:1] or [('references', 'resolved-binding')])[0]
        r = req('graph.neighbors', prun['projectId'], {'runId': pact['runId']},
                {'relation': relation, 'minResolution': rung, 'direction': 'both',
                 'endpoint': ep(i['universe'], 'package', 'dup', 'packages/absent/package.json')})
        q2['dup@unknown-manifest'] = strip(attempt(lambda: Q.execute_graph_query(r, prun, pobj, pblob, host=host())))
    q2['ambiguousReachable'] = any(v.get('detail') == 'QUERY.ENDPOINT_AMBIGUOUS' for v in q2.values() if isinstance(v, dict))
except Exception as e:
    q2['error'] = type(e).__name__ + ': ' + str(e)[:300]
    q2['tb'] = traceback.format_exc()[-1500:]
res['Q2'] = q2

# ---- Q3 availability mapping
ok = req('graph.neighbors', project, {'runId': rid}, dict(REL, direction='outgoing', endpoint=foo))
q3 = {}
for state in ('purged', 'expired', 'corrupt', 'unavailable', 'retained', 'partial', None, 'missing', 'not-a-state'):
    h = host() if state is None else host(availability=state)
    q3[str(state)] = strip(attempt(lambda: Q.execute_graph_query(ok, run, objects, blobs, host=h)))
c_objects, c_blobs = copy.deepcopy(objects), copy.deepcopy(blobs)
victim = None
for vid in c_objects[run['evidenceId']][1]['viewIds']:
    facts = c_objects[vid][1].get('facts') or []
    if facts:
        victim = facts[0]
        break
if victim:
    c_blobs[c_objects[victim][1]['payloadDigest']] = b'{"not":"retained"}'
    q3['partial+corrupt-bytes'] = strip(attempt(lambda: Q.execute_graph_query(ok, run, c_objects, c_blobs, host=host(availability='partial'))))
    q3['retained+corrupt-bytes'] = strip(attempt(lambda: Q.execute_graph_query(ok, run, c_objects, c_blobs, host=host(availability='retained'))))
expected = {'purged': 'evidence.purged', 'expired': 'evidence.expired', 'corrupt': 'evidence.corrupt', 'unavailable': 'evidence.missing'}
q3['mappingPassed'] = all(q3[k].get('detail') == v and q3[k].get('exitCode') == 4 and q3[k].get('errorCode') == 'HOST.IO_FAILURE'
                          for k, v in expected.items()) and all(q3[k]['result'] == 'ADMIT' for k in ('retained', 'partial', 'None'))
q3['unknownStateObservation'] = q3['not-a-state']['result']
res['Q3'] = q3

# ---- Q4 response parity (schema)
def valid(ref, value):
    try:
        Q.validate_schema(ref, value)
        return True
    except Exception as e:
        return 'INVALID:' + str(e).split('\n')[0][:160]


ctx = {'projectId': project, 'resolvedView': {'runId': rid}, 'coverage': 'complete', 'availability': 'retained',
       'truncated': False, 'totalItems': 0}
RESP = Q.SCHEMA_ID + '#/$defs/GraphQueryResponseV1'
q4 = {
    'run.show advisory=true (non-advisory op)': valid(RESP, {'schemaFamily': 'opensip.product.query', 'schemaMajor': 3, 'operation': 'run.show', 'context': dict(ctx, advisory=True)}),
    'finding.list advisory=true (non-advisory op)': valid(RESP, {'schemaFamily': 'opensip.product.query', 'schemaMajor': 3, 'operation': 'finding.list', 'context': dict(ctx, advisory=True), 'items': []}),
    'candidate.list advisory=false (advisory op)': valid(RESP, {'schemaFamily': 'opensip.product.query', 'schemaMajor': 3, 'operation': 'candidate.list', 'context': dict(ctx, advisory=False)}),
    'run.show advisory=false': valid(RESP, {'schemaFamily': 'opensip.product.query', 'schemaMajor': 3, 'operation': 'run.show', 'context': dict(ctx, advisory=False)}),
    'run.show context omitted advisory': valid(RESP, {'schemaFamily': 'opensip.product.query', 'schemaMajor': 3, 'operation': 'run.show', 'context': dict(ctx)}),
}
real = attempt(lambda: Q.execute_graph_query(ok, run, objects, blobs, host=host()))
if real['result'] == 'ADMIT':
    v = copy.deepcopy(real['_v'])
    v['context'].pop('evidence')
    q4['graph response without evidence'] = valid(RESP, v)
    v = copy.deepcopy(real['_v'])
    v['context']['resolvedView'] = {'latest': True}
    q4['graph response resolvedView latest'] = valid(RESP, v)
    v = copy.deepcopy(real['_v'])
    v['context']['advisory'] = True
    q4['graph response advisory true'] = valid(RESP, v)
res['Q4'] = q4

# ---- Q5 cursor binding / effective params
q5 = {}
reach_p = dict(REL, direction='both', start=foo, maxDepth=8, includeStart=True)
first = attempt(lambda: Q.execute_graph_query(req('graph.reach', project, {'runId': rid}, reach_p, size=1), run, objects, blobs, host=host()))
q5['first-page'] = strip(first)
cur = first.get('nextCursor')
if cur:
    q5['continue-identical'] = strip(attempt(lambda: Q.execute_graph_query(req('graph.reach', project, {'runId': rid}, reach_p, size=1, cursor=cur), run, objects, blobs, host=host())))
    p2 = dict(reach_p)
    p2.pop('includeStart')
    q5['continue-includeStart-omitted(effective false)'] = strip(attempt(lambda: Q.execute_graph_query(req('graph.reach', project, {'runId': rid}, p2, size=1, cursor=cur), run, objects, blobs, host=host())))
    q5['continue-latest-selector'] = strip(attempt(lambda: Q.execute_graph_query(req('graph.reach', project, {'latest': True}, reach_p, size=1, cursor=cur), run, objects, blobs, host=host(latestRunId=rid))))
    q5['continue-different-page-size'] = strip(attempt(lambda: Q.execute_graph_query(req('graph.reach', project, {'runId': rid}, reach_p, size=5, cursor=cur), run, objects, blobs, host=host())))
p_false = dict(reach_p, includeStart=False)
p_omit = dict(reach_p)
p_omit.pop('includeStart')
f1 = attempt(lambda: Q.execute_graph_query(req('graph.reach', project, {'runId': rid}, p_false, size=1), run, objects, blobs, host=host()))
f2 = attempt(lambda: Q.execute_graph_query(req('graph.reach', project, {'runId': rid}, p_omit, size=1), run, objects, blobs, host=host()))
q5['includeStart-false-vs-omitted-same-selection'] = (f1.get('nextCursor') == f2.get('nextCursor'), f1.get('items'), f2.get('items'))
res['Q5'] = q5

# ---- Q6 visit cap
q6 = {}
full = attempt(lambda: Q.execute_graph_query(req('graph.reach', project, {'runId': rid}, reach_p), run, objects, blobs, host=host()))
q6['uncapped'] = strip(full)
if full['result'] == 'ADMIT':
    n = full['visited']
    q6['cap=visited'] = strip(attempt(lambda: Q.execute_graph_query(req('graph.reach', project, {'runId': rid}, reach_p), run, objects, blobs, host=host(testBounds={'maxVisitedNodes': n}))))
    if n > 1:
        q6['cap=visited-1 required'] = strip(attempt(lambda: Q.execute_graph_query(req('graph.reach', project, {'runId': rid}, reach_p), run, objects, blobs, host=host(testBounds={'maxVisitedNodes': n - 1}))))
        q6['cap=visited-1 best-effort'] = strip(attempt(lambda: Q.execute_graph_query(req('graph.reach', project, {'runId': rid}, reach_p, completeness='best-effort'), run, objects, blobs, host=host(testBounds={'maxVisitedNodes': n - 1}))))
    q6['testBounds raise refused'] = strip(attempt(lambda: Q.execute_graph_query(req('graph.reach', project, {'runId': rid}, reach_p), run, objects, blobs, host=host(testBounds={'maxVisitedNodes': 2000000}))))
res['Q6'] = q6

json.dump(res, open(OUT, 'w'), indent=1, default=str)
print(json.dumps({'Q1': res['Q1']['passed'], 'Q2-ambiguousReachable': res['Q2'].get('ambiguousReachable'), 'Q2-error': res['Q2'].get('error'),
                  'Q3': res['Q3']['mappingPassed'], 'Q3-unknownState': res['Q3']['unknownStateObservation'], 'Q4': res['Q4'],
                  'Q5': {k: (v.get('result'), v.get('detail')) if isinstance(v, dict) else v for k, v in res['Q5'].items()},
                  'Q6': {k: (v.get('result'), v.get('traversal'), v.get('termination', v.get('detail'))) for k, v in res['Q6'].items()}},
                 indent=1, default=str))
