"""Independent query discrimination: source42 versus source43, each tree's OWN query_projection_model, semantic fixture,
semantic replay driver (close_positive) and query surface projection, in separate processes (verified copies work/base42 and
work/source43-pkg).

A lawful retained Run (TypeScript semantic fixture, references@resolved-binding with incomplete resolution and incoming search,
closed through identity close_run by the maintained driver) is queried through the public execute_graph_query entry with:
availability omitted / retained / partial on neighbors, path and reach; every refusing availability state; invalid observations;
missing and corrupt retained bytes under partial/retained/purged; public refusal routes with a partial observation present;
same-host cursor continuation, cache loss/poison, historical re-selection and bound admission; path hop orientation on the Run and
tie/order/zero-hop goldens through traverse_projected_graph; and the graph-query-response surface parity and renderers.
Expected values are this reviewer's reading of each tree's contract.
usage: probe_query43_x.py  |  probe_query43_x.py --child ROOT LABEL OUT"""
import contextlib, copy, hashlib, importlib.util, io, json, subprocess, sys, traceback
from pathlib import Path

RT = Path('/private/tmp/opensip-design-corrections/claude-independent-design.v43')
TREES = [('source42', RT / 'work/base42'), ('source43', RT / 'work/source43-pkg')]
PY = '/tmp/opensip-architecture-review-env/bin/python'
OUT = RT / 'receipts/probes/query43-x.json'
RID = 'req1_' + 'a' * 32


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(mod)
    return mod


def ep(u, kind, nid):
    return {'universe': u, 'kind': kind, 'nativeSubjectId': nid}


def child(root, label, outfile):
    WF = Path(root) / 'docs/coop/design-corrections/workflows'
    FD = Path(root) / 'docs/coop/design-corrections/foundation'
    sys.path.insert(0, str(FD))
    Q = load('q43x_q_' + label, WF / 'query_projection_model.v3.py')
    S = load('q43x_s_' + label, FD / 'evaluator_semantic_fixture.v3.py')
    RP = load('q43x_r_' + label, FD / 'check-semantic-replay.v3.py')
    QS = load('q43x_qs_' + label, WF / 'query_surface_projection.v3.py')
    command = next(c for c in json.loads((WF / 'command-inventory.v3.json').read_text())['commands'] if c['name'] == 'query')
    out = {}
    atom = {'op': 'none', 'relation': 'references', 'minResolution': 'resolved-binding', 'endpoint': 'target', 'filters': []}
    g = S.build_ts_semantic_graph(atom=atom, has_declares=False, has_references_fact=True, second_partition=True, references_resolved=False,
                                  incoming_search=True, incoming_complete=False, target_sidecar=True, second_universe=True)
    run, objects, blobs, actual = RP.close_positive(g)
    run_key, project = actual['runId'], run['projectId']
    foo, bar = ep(g['u1'], 'symbol', g['foo']), ep(g['u1'], 'symbol', g['bar'])
    out['_run'] = {'runId': run_key, 'projectId': project}

    def host(**kw):
        d = {'requestId': RID}
        d.update(kw)
        return d

    def req(op, params, view=None, size=100, cursor=None, completeness='required', major=3, project_id=None):
        page = {'size': size}
        if cursor is not None:
            page['cursor'] = cursor
        return {'completeness': completeness, 'operation': op, 'page': page, 'params': params, 'projectId': project_id or project,
                'schemaFamily': 'opensip.product.query', 'schemaMajor': major, 'view': view or {'runId': run_key}}

    def q(name, rq, h, r=None, o=None, b=None):
        try:
            resp = Q.execute_graph_query(rq, run if r is None else r, objects if o is None else o, blobs if b is None else b, host=h)
            out[name] = {'ok': True, 'response': resp}
        except Q.QueryRefusal as exc:
            rec = {'ok': False, 'errorCode': exc.error_code, 'detail': exc.detail}
            try:
                env = exc.envelope()
                rec.update(exitCode=env['exitCode'], klass=env['termination']['class'], errors=[e['code'] for e in env['errors']], hasRun='run' in env)
            except Exception as e2:  # noqa: BLE001
                rec['envelopeError'] = type(e2).__name__ + ':' + str(e2)[:200]
            out[name] = rec
        except Q.ReferenceCallPrecondition as exc:
            out[name] = {'ok': False, 'precondition': exc.missing}
        except Exception as exc:  # noqa: BLE001
            out[name] = {'ok': False, 'exception': type(exc).__name__ + ':' + str(exc)[:400]}

    NB = {'relation': 'references', 'minResolution': 'resolved-binding', 'direction': 'outgoing', 'endpoint': foo}
    PATH = {'relation': 'references', 'minResolution': 'resolved-binding', 'direction': 'outgoing', 'start': foo, 'target': bar, 'maxDepth': 4}
    REACH = {'relation': 'references', 'minResolution': 'resolved-binding', 'direction': 'outgoing', 'start': foo, 'maxDepth': 4, 'includeStart': True}
    for opname, op, params in (('neighbors', 'graph.neighbors', NB), ('path', 'graph.path', PATH), ('reach', 'graph.reach', REACH)):
        for obs in ('omitted', 'retained', 'partial'):
            q('avail-%s-%s' % (opname, obs), req(op, params), host() if obs == 'omitted' else host(availability=obs))
    for state in ('purged', 'expired', 'corrupt', 'unavailable', 'missing'):
        q('avail-refuse-' + state, req('graph.neighbors', NB), host(availability=state))
    for lab, val in (('null', None), ('unknown', 'not-a-state'), ('number', 1)):
        q('avail-precondition-' + lab, req('graph.neighbors', NB), host(availability=val))

    victim = None
    for vid in objects[run['evidenceId']][1]['viewIds']:
        if objects[vid][1].get('facts'):
            victim = objects[vid][1]['facts'][0]
            break
    out['_victim'] = victim
    if victim is not None:
        digest = objects[victim][1]['payloadDigest']
        corrupt_b = copy.deepcopy(blobs)
        corrupt_b[digest] = b'not-the-retained-payload'
        missing_b = copy.deepcopy(blobs)
        del missing_b[digest]
        for obs in ('omitted', 'retained', 'partial'):
            h = host() if obs == 'omitted' else host(availability=obs)
            q('bytes-corrupt-' + obs, req('graph.neighbors', NB), h, run, objects, corrupt_b)
            q('bytes-missing-' + obs, req('graph.neighbors', NB), h, run, objects, missing_b)
        q('bytes-missing-purged', req('graph.neighbors', NB), host(availability='purged'), run, objects, missing_b)

    other_run = 'run3:' + '1' * 64
    q('route-major2-partial', req('graph.neighbors', NB, major=2), host(availability='partial'))
    q('route-malformed-partial', {'schemaMajor': 3, 'bad': True}, host(availability='partial'))
    q('route-malformed-purged', {'schemaMajor': 3, 'bad': True}, host(availability='purged'))
    q('route-project-mismatch-partial', req('graph.neighbors', NB, project_id='prj1-' + hashlib.sha256(b'elsewhere').hexdigest()), host(availability='partial'))
    q('route-relation-unsupported-partial', req('graph.neighbors', dict(NB, relation='calls', minResolution='syntactic-callee-name')), host(availability='partial'))
    q('route-runid-mismatch-partial', req('graph.neighbors', NB, view={'runId': other_run}), host(availability='partial'))
    q('route-latest-missing-partial', req('graph.neighbors', NB, view={'latest': True}), host(availability='partial'))
    q('route-latest-ok-partial', req('graph.neighbors', NB, view={'latest': True}), host(availability='partial', latestRunId=run_key))
    q('route-snapshot-ambiguous-partial', req('graph.neighbors', NB, view={'snapshotId': run['snapshotId']}),
      host(availability='partial', runsForSnapshot={run['snapshotId']: [run_key, other_run]}))
    q('route-view-unavailable-partial', req('graph.neighbors', dict(NB, factViewDigests=['view2:' + '2' * 64])), host(availability='partial'))
    q('route-endpoint-unknown-partial', req('graph.neighbors', dict(NB, endpoint=ep(g['u1'], 'symbol', 'symbol:missing'))), host(availability='partial'))
    q('route-purged-before-view-join', req('graph.neighbors', NB, view={'runId': other_run}), host(availability='purged'))
    try:
        resp = Q.execute_graph_query(req('graph.neighbors', NB), None, None, None, host=host(availability='partial', standing='x'))
        out['route-no-retained-run-partial'] = {'ok': True, 'response': resp}
    except Q.QueryRefusal as exc:
        out['route-no-retained-run-partial'] = {'ok': False, 'errorCode': exc.error_code, 'detail': exc.detail}

    q('cursor-page1-retained', req('graph.reach', REACH, size=1), host())
    tok = (out['cursor-page1-retained'].get('response') or {}).get('context', {}).get('nextCursor')
    out['_cursor'] = tok
    if tok:
        q('cursor-page2-retained', req('graph.reach', REACH, size=1, cursor=tok), host())
        q('cursor-page2-partial', req('graph.reach', REACH, size=1, cursor=tok), host(availability='partial'))
        q('cursor-page2-cache-loss', req('graph.reach', REACH, size=1, cursor=tok), host(cache={}))
        q('cursor-page2-cache-poison', req('graph.reach', REACH, size=1, cursor=tok), host(cache={'k': {'edges': []}}))
        q('cursor-latest-reresolve', req('graph.reach', REACH, size=1, cursor=tok, view={'latest': True}), host(latestRunId=run_key))
        q('cursor-other-run', req('graph.reach', REACH, size=1, cursor=tok, view={'runId': other_run}), host())
        q('cursor-params-changed', req('graph.reach', dict(REACH, maxDepth=3), size=1, cursor=tok), host())
        q('cursor-position-past-prefix', req('graph.reach', REACH, size=1, cursor=tok[:tok.rfind('.') + 1] + '99'), host())
        q('cursor-malformed', req('graph.reach', REACH, size=1, cursor='not-a-token'), host())
    q('bound-raise-refused', req('graph.reach', REACH), host(testBounds={'maxVisitedNodes': 2000000}))
    q('bound-lower-admitted', req('graph.reach', REACH, completeness='best-effort'), host(testBounds={'maxVisitedNodes': 1}))

    q('orient-path-outgoing-foo-bar', req('graph.path', PATH), host())
    q('orient-path-incoming-bar-foo', req('graph.path', dict(PATH, direction='incoming', start=bar, target=foo)), host())
    q('orient-path-both-bar-foo', req('graph.path', dict(PATH, direction='both', start=bar, target=foo)), host())
    q('orient-path-incoming-foo-bar-none', req('graph.path', dict(PATH, direction='incoming')), host())
    q('orient-path-zero-hop', req('graph.path', dict(PATH, target=foo)), host())
    q('orient-neighbors-incoming-bar', req('graph.neighbors', dict(NB, direction='incoming', endpoint=bar)), host())
    q('orient-neighbors-both-bar', req('graph.neighbors', dict(NB, direction='both', endpoint=bar)), host())
    q('orient-reach-incoming-bar', req('graph.reach', dict(REACH, direction='incoming', start=bar)), host())

    u = 'c' * 64
    s, x, y, t = ep(u, 'symbol', 'symbol:s'), ep(u, 'symbol', 'symbol:x'), ep(u, 'symbol', 'symbol:y'), ep(u, 'symbol', 'symbol:t')

    def e(n, src, dst):
        return {'confidenceMillionths': 1000000, 'factId': 'fact2:' + (n * 64), 'producerClosure': 'closure2:' + 'd' * 64,
                'relation': 'references', 'resolution': 'resolved-binding', 'source': src, 'target': dst}
    golden = [e('1', x, s), e('2', s, y), e('3', t, x), e('4', y, t)]
    gp = {'relation': 'references', 'minResolution': 'resolved-binding', 'maxDepth': 4}
    prj, rid = 'prj1-' + 'e' * 64, 'run3:' + 'f' * 64
    for name, params in (('golden-both-s-t', dict(gp, direction='both', start=s, target=t)),
                         ('golden-incoming-t-s', dict(gp, direction='incoming', start=t, target=s)),
                         ('golden-outgoing-s-t', dict(gp, direction='outgoing', start=s, target=t)),
                         ('golden-both-zero-hop', dict(gp, direction='both', start=s, target=s)),
                         ('golden-both-depth1-no-path', dict(gp, direction='both', start=s, target=t, maxDepth=1))):
        try:
            out[name] = {'ok': True, 'response': Q.traverse_projected_graph('graph.path', params, golden, project_id=prj, run_id=rid)}
        except Exception as exc:  # noqa: BLE001
            out[name] = {'ok': False, 'exception': type(exc).__name__ + ':' + str(exc)[:300]}

    def parity(name):
        resp = (out.get(name) or {}).get('response')
        if not resp:
            return {'missing': True}
        try:
            term = copy.deepcopy(resp.get('termination') or {'class': 'success'})
            env = {'schemaFamily': 'opensip.product.envelope', 'schemaMajor': 3, 'kind': 'query', 'requestId': RID, 'projectId': project,
                   'termination': term, 'exitCode': QS.Wlegacy.EXIT[term['class']], 'query': QS.graph_query_result_summary(resp),
                   'querySurface': 'graph-query-response', 'queryResponse': copy.deepcopy(resp)}
            proj = QS.project_query_surface(resp, term, envelope=env, command=command)
            rnd = QS.render_query_formats(proj['parity'], env, command, hints=['hint'])
            return {'parityAvailability': proj['parity'].get('availability'), 'queryResponseEqual': proj['parity'].get('query-response') == resp,
                    'renderOk': rnd.get('ok'), 'parityHolds': rnd.get('parityHolds'), 'formats': sorted(r['format'] for r in rnd['renderings'])}
        except Exception as exc:  # noqa: BLE001
            return {'exception': type(exc).__name__ + ':' + str(exc)[:300]}
    out['parity-neighbors-partial'] = parity('avail-neighbors-partial')
    out['parity-neighbors-retained'] = parity('avail-neighbors-retained')
    Path(outfile).write_text(json.dumps(out, indent=1, default=str))


def parent():
    sides, runs = {}, {}
    for label, root in TREES:
        o = RT / ('receipts/probes/query43-x.side-' + label + '.json')
        p = subprocess.run([PY, '-I', '-B', __file__, '--child', str(root), label, str(o)], capture_output=True, text=True, timeout=5400)
        runs[label] = {'exitCode': p.returncode, 'stderrTail': p.stderr[-3000:]}
        sides[label] = json.loads(o.read_text()) if o.exists() else {}
    A, B = sides.get('source42', {}), sides.get('source43', {})
    rows = []

    def row(case, ok, observed=None, kind=None):
        r = {'case': case, 'ok': bool(ok), 'observed': observed}
        if kind:
            r['kind'] = kind
        rows.append(r)

    def resp(side, name):
        return (side.get(name) or {}).get('response')

    def ctx(side, name):
        return (resp(side, name) or {}).get('context') or {}

    def brief(side, name):
        v = side.get(name) or {}
        if v.get('ok'):
            r = v['response']
            return {'ok': True, 'availability': r['context'].get('availability'), 'items': len(r['items']), 'traversalCoverage': r['context'].get('traversalCoverage'),
                    'termination': r.get('termination', {}).get('class')}
        return {k: v.get(k) for k in ('ok', 'errorCode', 'detail', 'exitCode', 'klass', 'errors', 'precondition', 'exception', 'envelopeError') if k in v}

    for lab, _ in TREES:
        row('child-' + lab + '-completed', runs[lab]['exitCode'] == 0 and bool(sides[lab]), runs[lab])
    row('same lawful closed Run on both trees', A.get('_run') == B.get('_run') and bool(A.get('_run')), {'source42': A.get('_run'), 'source43': B.get('_run')})
    for op in ('neighbors', 'path', 'reach'):
        names = ['avail-%s-%s' % (op, o) for o in ('omitted', 'retained', 'partial')]
        obs = {n: {'source42': brief(A, n), 'source43': brief(B, n)} for n in names}
        row('availability-%s: omitted and retained report retained on both trees; partial reports retained on source42 and partial on source43' % op,
            all(ctx(s, names[0]).get('availability') == 'retained' and ctx(s, names[1]).get('availability') == 'retained' for s in (A, B))
            and ctx(A, names[2]).get('availability') == 'retained' and ctx(B, names[2]).get('availability') == 'partial', obs)
        base = resp(A, names[1])
        same_items = all((resp(s, n) or {}).get('items') == (base or {}).get('items') for s in (A, B) for n in names)
        strip = lambda r: {k: v for k, v in (r or {}).get('context', {}).items() if k != 'availability'}
        same_ctx = all(strip(resp(s, n)) == strip(base) for s in (A, B) for n in names)
        same_term = all((resp(s, n) or {}).get('termination') == (base or {}).get('termination') for s in (A, B) for n in names)
        row('availability-%s: identical semantic items, termination and every other context field across trees and observations' % op,
            bool(base) and same_items and same_ctx and same_term, {'items': len((base or {}).get('items') or []), 'sameItems': same_items, 'sameContextBeyondAvailability': same_ctx, 'sameTermination': same_term})
        row('availability-%s: omitted and retained responses are byte-identical source42 versus source43' % op,
            json.dumps(resp(A, names[0]), sort_keys=True) == json.dumps(resp(B, names[0]), sort_keys=True)
            and json.dumps(resp(A, names[1]), sort_keys=True) == json.dumps(resp(B, names[1]), sort_keys=True), None)
    want = {'purged': 'evidence.purged', 'expired': 'evidence.expired', 'corrupt': 'evidence.corrupt', 'unavailable': 'evidence.missing', 'missing': 'evidence.missing'}
    for st, det in want.items():
        n = 'avail-refuse-' + st
        row('%s: HOST.IO_FAILURE / %s / operational-failed / exit 4 on both trees' % (n, det),
            all(not (s.get(n) or {}).get('ok') and (s.get(n) or {}).get('errorCode') == 'HOST.IO_FAILURE' and (s.get(n) or {}).get('detail') == det and (s.get(n) or {}).get('exitCode') == 4
                and (s.get(n) or {}).get('klass') == 'operational-failed' and (s.get(n) or {}).get('hasRun') is False for s in (A, B)), {'source42': brief(A, n), 'source43': brief(B, n)})
    for lab in ('null', 'unknown', 'number'):
        n = 'avail-precondition-' + lab
        row(n + ': ReferenceCallPrecondition host.availability on both trees', all((s.get(n) or {}).get('precondition') == 'host.availability' for s in (A, B)),
            {'source42': brief(A, n), 'source43': brief(B, n)})
    for kind, det in (('corrupt', 'evidence.corrupt'), ('missing', 'evidence.missing')):
        for obs in ('omitted', 'retained', 'partial'):
            n = 'bytes-%s-%s' % (kind, obs)
            row('%s: the observation grants nothing; close_run refuses %s on both trees' % (n, det),
                all(not (s.get(n) or {}).get('ok') and (s.get(n) or {}).get('detail') == det and (s.get(n) or {}).get('exitCode') == 4 for s in (A, B)), {'source42': brief(A, n), 'source43': brief(B, n)})
    n = 'bytes-missing-purged'
    row(n + ': the refusing observation routes before replay (evidence.purged) on both trees',
        all((s.get(n) or {}).get('detail') == 'evidence.purged' for s in (A, B)), {'source42': brief(A, n), 'source43': brief(B, n)})
    routes = {'route-major2-partial': 'QUERY.SCHEMA_MAJOR_UNSUPPORTED', 'route-malformed-partial': 'QUERY.PARAMS_MALFORMED', 'route-malformed-purged': 'QUERY.PARAMS_MALFORMED',
              'route-project-mismatch-partial': 'QUERY.PARAMS_MALFORMED', 'route-relation-unsupported-partial': 'QUERY.RELATION_UNSUPPORTED',
              'route-runid-mismatch-partial': 'QUERY.VIEW_UNKNOWN', 'route-latest-missing-partial': 'QUERY.VIEW_UNKNOWN',
              'route-snapshot-ambiguous-partial': 'QUERY.VIEW_AMBIGUOUS', 'route-view-unavailable-partial': 'QUERY.FACT_VIEW_UNAVAILABLE',
              'route-endpoint-unknown-partial': 'QUERY.ENDPOINT_UNKNOWN', 'route-purged-before-view-join': 'evidence.purged',
              'route-no-retained-run-partial': 'QUERY.VIEW_UNKNOWN'}
    for n, det in routes.items():
        row('%s: refuses %s identically on both trees (a partial or refusing observation does not change the public route)' % (n, det),
            all((s.get(n) or {}).get('ok') is False and (s.get(n) or {}).get('detail') == det for s in (A, B)) and brief(A, n) == brief(B, n), {'source42': brief(A, n), 'source43': brief(B, n)})
    n = 'route-latest-ok-partial'
    row(n + ': trusted latest join admits; source43 reports partial, source42 retained', ctx(A, n).get('availability') == 'retained' and ctx(B, n).get('availability') == 'partial'
        and resp(A, n)['items'] == resp(B, n)['items'], {'source42': brief(A, n), 'source43': brief(B, n)})
    row('cursor issued for a two-row reach page on both trees, identical token', bool(A.get('_cursor')) and A.get('_cursor') == B.get('_cursor'), {'source42': A.get('_cursor'), 'source43': B.get('_cursor')})
    if A.get('_cursor'):
        p2 = [resp(s, 'cursor-page2-retained') for s in (A, B)]
        row('cursor continuation (same host): page 2 items equal on both trees; cache loss and cache poison do not change the page',
            all(p and len(p['items']) == 1 for p in p2) and p2[0]['items'] == p2[1]['items']
            and all((resp(s, x) or {}).get('items') == (resp(s, 'cursor-page2-retained') or {}).get('items') for s in (A, B) for x in ('cursor-page2-cache-loss', 'cursor-page2-cache-poison')),
            {k: {'source42': brief(A, k), 'source43': brief(B, k)} for k in ('cursor-page2-retained', 'cursor-page2-cache-loss', 'cursor-page2-cache-poison')})
        row('cursor continuation with a partial observation: same page; source43 discloses partial, source42 retained',
            (resp(A, 'cursor-page2-partial') or {}).get('items') == (resp(B, 'cursor-page2-partial') or {}).get('items') == p2[0]['items']
            and ctx(A, 'cursor-page2-partial').get('availability') == 'retained' and ctx(B, 'cursor-page2-partial').get('availability') == 'partial',
            {'source42': brief(A, 'cursor-page2-partial'), 'source43': brief(B, 'cursor-page2-partial')})
        for n in ('cursor-latest-reresolve', 'cursor-other-run', 'cursor-params-changed', 'cursor-position-past-prefix', 'cursor-malformed'):
            row('%s: QUERY.CURSOR_MISMATCH on both trees' % n, all((s.get(n) or {}).get('detail') == 'QUERY.CURSOR_MISMATCH' for s in (A, B)), {'source42': brief(A, n), 'source43': brief(B, n)})
    row('bound-raise-refused: host.testBounds cannot raise a public cap (QUERY.PARAMS_MALFORMED) on both trees',
        all((s.get('bound-raise-refused') or {}).get('detail') == 'QUERY.PARAMS_MALFORMED' for s in (A, B)), {'source42': brief(A, 'bound-raise-refused'), 'source43': brief(B, 'bound-raise-refused')})
    row('bound-lower-admitted: a lowered visited cap truncates with lower-bound disclosure identically on both trees',
        json.dumps(resp(A, 'bound-lower-admitted'), sort_keys=True) == json.dumps(resp(B, 'bound-lower-admitted'), sort_keys=True)
        and ctx(B, 'bound-lower-admitted').get('traversalCoverage') == 'truncated-bound', {'source43': brief(B, 'bound-lower-admitted')})

    def hops_ok(r):
        if not r or not r.get('items'):
            return None
        it = r['items'][0]
        return all(it['edges'][i]['source'] == it['nodes'][i] and it['edges'][i]['target'] == it['nodes'][i + 1] for i in range(len(it['edges']))) and it['hopCount'] == len(it['edges'])
    run_facts = {}
    for n in ('orient-path-outgoing-foo-bar', 'orient-path-incoming-bar-foo', 'orient-path-both-bar-foo', 'orient-path-incoming-foo-bar-none', 'orient-path-zero-hop',
              'orient-neighbors-incoming-bar', 'orient-neighbors-both-bar', 'orient-reach-incoming-bar'):
        row('%s: byte-identical response on source42 and source43' % n, json.dumps(resp(A, n), sort_keys=True) == json.dumps(resp(B, n), sort_keys=True) and resp(B, n) is not None,
            brief(B, n))
    out_path, in_path, both_path = resp(B, 'orient-path-outgoing-foo-bar'), resp(B, 'orient-path-incoming-bar-foo'), resp(B, 'orient-path-both-bar-foo')
    nb_in = resp(B, 'orient-neighbors-incoming-bar')
    stored = (out_path or {}).get('items', [{}])[0].get('edges', [{}])[0] if out_path and out_path.get('items') else {}
    row('real-Run path under incoming and both: edges[i] is the hop nodes[i]->nodes[i+1] (bar->foo), the reverse of the stored fact, with the same stored factId',
        hops_ok(out_path) and hops_ok(in_path) and hops_ok(both_path)
        and in_path['items'][0]['edges'][0]['factId'] == stored.get('factId') == both_path['items'][0]['edges'][0]['factId']
        and in_path['items'][0]['edges'][0]['source'] == stored.get('target') and in_path['items'][0]['edges'][0]['target'] == stored.get('source'),
        {'outgoing': (out_path or {}).get('items'), 'incoming': (in_path or {}).get('items'), 'both': (both_path or {}).get('items')})
    row('real-Run neighbors under incoming keep the projected fact orientation (source foo, target bar)',
        bool(nb_in and nb_in['items']) and nb_in['items'][0]['factId'] == stored.get('factId') and nb_in['items'][0]['source'] == stored.get('source')
        and nb_in['items'][0]['target'] == stored.get('target'), (nb_in or {}).get('items'))
    row('real-Run incoming path from the fact source finds no hop; zero-hop path has nodes [start] and no edges',
        (resp(B, 'orient-path-incoming-foo-bar-none') or {}).get('items') == [] and (resp(B, 'orient-path-zero-hop') or {}).get('items', [{}])[0].get('edges') == []
        and (resp(B, 'orient-path-zero-hop') or {}).get('items', [{}])[0].get('hopCount') == 0, None)
    gb = resp(B, 'golden-both-s-t')
    gi = resp(B, 'golden-incoming-t-s')
    row('golden both s->t: shortest two-hop path, lex-least fact2 sequence (1,3), hops oriented along the walk against both stored facts',
        bool(gb and gb['items']) and [e['factId'][-1] for e in gb['items'][0]['edges']] == ['1', '3'] and hops_ok(gb)
        and [n['nativeSubjectId'] for n in gb['items'][0]['nodes']] == ['symbol:s', 'symbol:x', 'symbol:t'], (gb or {}).get('items'))
    row('golden incoming t->s: reverse traversal (4,2) with hops t->y and y->s',
        bool(gi and gi['items']) and [e['factId'][-1] for e in gi['items'][0]['edges']] == ['4', '2'] and hops_ok(gi), (gi or {}).get('items'))
    row('golden outgoing s->t: stored directions only (2,4); zero-hop and depth-bounded controls',
        [e['factId'][-1] for e in (resp(B, 'golden-outgoing-s-t') or {}).get('items', [{'edges': []}])[0]['edges']] == ['2', '4']
        and (resp(B, 'golden-both-zero-hop') or {}).get('items', [{}])[0].get('hopCount') == 0 and (resp(B, 'golden-both-depth1-no-path') or {}).get('items') == [], None)
    row('goldens identical on source42 and source43 (representation pin preserves model behavior)',
        all(json.dumps(resp(A, n), sort_keys=True) == json.dumps(resp(B, n), sort_keys=True) and resp(B, n) is not None
            for n in ('golden-both-s-t', 'golden-incoming-t-s', 'golden-outgoing-s-t', 'golden-both-zero-hop', 'golden-both-depth1-no-path')), None)
    pa, pb = A.get('parity-neighbors-partial', {}), B.get('parity-neighbors-partial', {})
    row('surface parity: graph-query-response availability parity is the context value (source42 retained, source43 partial); all renderers hold parity',
        pa.get('parityAvailability') == 'retained' and pb.get('parityAvailability') == 'partial' and all(p.get('renderOk') and p.get('parityHolds') and p.get('queryResponseEqual')
                                                                                                         and p.get('formats') == ['agent', 'human', 'json'] for p in (pa, pb)),
        {'source42': pa, 'source43': pb, 'retained43': B.get('parity-neighbors-retained')})
    OUT.write_text(json.dumps({'standing': 'independent reviewer discrimination probe; each tree own query/fixture/replay/surface modules in its own process; lawful closed Run; not product qualification',
                               'rows': rows, 'failed': [r for r in rows if not r['ok']], 'childRuns': runs}, indent=1, default=str))
    print(json.dumps({'total': len(rows), 'failed': [(r['case'], r['observed']) for r in rows if not r['ok']]}, indent=1, default=str)[:12000])


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--child':
        child(sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        parent()
