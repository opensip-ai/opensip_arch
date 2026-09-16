"""Independent adapter-path discrimination, source42 versus source43, each tree's own query model, identity model, semantic fixture
and replay driver in its own process (verified copies work/base42 and work/source43-pkg).

The product adapter reads a RETAINED identity availability record (observe_retained_availability), supplies its admitted state as
the observation to execute_graph_query, and handles its own out-of-vocabulary observation with host_adapter_refusal. On a lawful
closed Run this measures: record state -> observation -> response context.availability (partial must be disclosed on source43 and
was upgraded on source42); a partial record with nonempty missingRefs still grants nothing when retained bytes are corrupt or
missing; refusing record states route unchanged; failing records are evidence.corrupt; adapter invalid observation routes to
SYSTEM.OUTCOME.ILLEGAL_STATE / HOST.INVARIANT_VIOLATED / host-invariant / exit 4 with subject host.availability and no run; a
RequestId precondition is never projected. Expectations are this reviewer's reading of contract section 7 (:162-166).
usage: probe_query_adapter43_x.py  |  --child ROOT LABEL OUT"""
import contextlib, copy, importlib.util, io, json, subprocess, sys
from pathlib import Path

RT = Path('/private/tmp/opensip-design-corrections/claude-independent-design.v43')
TREES = [('source42', RT / 'work/base42'), ('source43', RT / 'work/source43-pkg')]
PY = '/tmp/opensip-architecture-review-env/bin/python'
OUT = RT / 'receipts/probes/query-adapter43-x.json'
RID = 'req1_' + 'c' * 32


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(mod)
    return mod


def child(root, label, outfile):
    WF = Path(root) / 'docs/coop/design-corrections/workflows'
    FD = Path(root) / 'docs/coop/design-corrections/foundation'
    sys.path.insert(0, str(FD))
    import canonical  # noqa: E402  (this tree's own copy)
    Q = load('qa43x_q_' + label, WF / 'query_projection_model.v3.py')
    S = load('qa43x_s_' + label, FD / 'evaluator_semantic_fixture.v3.py')
    RP = load('qa43x_r_' + label, FD / 'check-semantic-replay.v3.py')
    out = {}
    atom = {'op': 'none', 'relation': 'references', 'minResolution': 'resolved-binding', 'endpoint': 'target', 'filters': []}
    g = S.build_ts_semantic_graph(atom=atom, has_declares=False, has_references_fact=True, second_partition=True, references_resolved=False,
                                  incoming_search=True, incoming_complete=False, target_sidecar=True, second_universe=True)
    run, objects, blobs, actual = RP.close_positive(g)
    run_key, project = actual['runId'], run['projectId']
    out['_run'] = run_key
    foo = {'universe': g['u1'], 'kind': 'symbol', 'nativeSubjectId': g['foo']}
    req = {'completeness': 'required', 'operation': 'graph.neighbors', 'page': {'size': 100},
           'params': {'relation': 'references', 'minResolution': 'resolved-binding', 'direction': 'outgoing', 'endpoint': foo},
           'projectId': project, 'schemaFamily': 'opensip.product.query', 'schemaMajor': 3, 'view': {'runId': run_key}}
    victim = next((objects[v][1]['facts'][0] for v in objects[run['evidenceId']][1]['viewIds'] if objects[v][1].get('facts')), None)
    # identity-schemas.v3.json $defs/Ref: {domain, digest}; a fact reference carries the bare 64-hex digest of its fact2 id.
    missing_ref = {'domain': 'fact', 'digest': victim.split(':', 1)[1]} if victim else None

    def record(state, **kw):
        r = {'schemaVersion': 2, 'runId': run_key, 'generation': 3, 'state': state, 'missingRefs': [], 'reason': 'reviewer adapter probe'}
        r.update(kw)
        return canonical.canonical(r)

    def adapter_query(name, raw, o=None, b=None):
        """Reference adapter composition: read retained record, then query with its state as the observation."""
        try:
            state = Q.observe_retained_availability(raw, run_key)
        except Q.QueryRefusal as exc:
            out[name] = {'stage': 'record', 'ok': False, 'errorCode': exc.error_code, 'detail': exc.detail, 'klass': exc.klass}
            return
        try:
            resp = Q.execute_graph_query(req, run, objects if o is None else o, blobs if b is None else b, host={'requestId': RID, 'availability': state})
            out[name] = {'stage': 'query', 'ok': True, 'recordState': state, 'availability': resp['context']['availability'], 'items': resp['items'],
                         'contextMinusAvailability': {k: v for k, v in resp['context'].items() if k != 'availability'}, 'termination': resp['termination']}
        except Q.QueryRefusal as exc:
            env = exc.envelope()
            out[name] = {'stage': 'query', 'ok': False, 'recordState': state, 'errorCode': exc.error_code, 'detail': exc.detail, 'exitCode': env['exitCode'], 'hasRun': 'run' in env}

    adapter_query('record-retained', record('retained'))
    adapter_query('record-partial', record('partial'))
    adapter_query('record-partial-with-missing-ref', record('partial', missingRefs=[missing_ref]) if missing_ref else record('partial'))
    for st in ('purged', 'expired', 'corrupt', 'unavailable'):
        adapter_query('record-' + st, record(st))
    adapter_query('record-unparseable', b'{not-json')
    adapter_query('record-unknown-state', record('not-a-state'))
    adapter_query('record-other-run', record('partial', runId='run3:' + '1' * 64))
    adapter_query('record-missing-reason', canonical.canonical({'schemaVersion': 2, 'runId': run_key, 'generation': 0, 'state': 'partial', 'missingRefs': []}))
    if victim is not None:
        digest = objects[victim][1]['payloadDigest']
        cb = copy.deepcopy(blobs)
        cb[digest] = b'not-the-retained-payload'
        mb = copy.deepcopy(blobs)
        del mb[digest]
        adapter_query('record-partial-corrupt-bytes', record('partial', missingRefs=[missing_ref]), None, cb)
        adapter_query('record-partial-missing-bytes', record('partial', missingRefs=[missing_ref]), None, mb)
        adapter_query('record-retained-missing-bytes', record('retained'), None, mb)
    for lab, val in (('null', None), ('unknown', 'not-a-state')):
        try:
            Q.execute_graph_query(req, run, objects, blobs, host={'requestId': RID, 'availability': val})
            out['adapter-invalid-' + lab] = {'precondition': None}
        except Q.ReferenceCallPrecondition as pre:
            ref = Q.host_adapter_refusal(pre, req, {'requestId': RID})
            env = ref.envelope()
            t = env['termination']
            rec = {'precondition': pre.missing, 'errorCode': ref.error_code, 'detail': ref.detail, 'faultCause': t.get('faultCause'), 'klass': t['class'],
                   'exitCode': env['exitCode'], 'subject': t.get('domainDetail', {}).get('subject'), 'hasRun': 'run' in env, 'runIdOnTermination': 'runId' in t}
            try:
                Q.host_adapter_refusal(pre, req, {})
                rec['withoutRequestId'] = 'projected'
            except Q.ReferenceCallPrecondition as exc2:
                rec['withoutRequestId'] = 'precondition:' + exc2.missing
            out['adapter-invalid-' + lab] = rec
    try:
        Q.host_adapter_refusal(Q.ReferenceCallPrecondition('host.requestId'), req, {'requestId': RID})
        out['adapter-requestid-precondition'] = 'projected'
    except Q.ReferenceCallPrecondition as exc:
        out['adapter-requestid-precondition'] = 'precondition:' + exc.missing
    Path(outfile).parent.mkdir(parents=True, exist_ok=True)
    Path(outfile).write_text(json.dumps(out, indent=1, default=str))


def parent():
    sides, runs = {}, {}
    for label, root in TREES:
        o = RT / ('receipts/probes/query-adapter43-x.side-' + label + '.json')
        p = subprocess.run([PY, '-I', '-B', __file__, '--child', str(root), label, str(o)], capture_output=True, text=True, timeout=3600)
        runs[label] = {'exitCode': p.returncode, 'stderrTail': p.stderr[-3000:]}
        sides[label] = json.loads(o.read_text()) if o.exists() else {}
    A, B = sides.get('source42', {}), sides.get('source43', {})
    rows = []

    def row(case, ok, observed=None):
        rows.append({'case': case, 'ok': bool(ok), 'observed': observed})

    def g(side, name):
        return side.get(name) or {}

    for lab, _ in TREES:
        row('child-%s-completed' % lab, runs[lab]['exitCode'] == 0 and bool(sides[lab]), runs[lab])
    row('same lawful closed Run on both trees', A.get('_run') == B.get('_run') and bool(A.get('_run')), A.get('_run'))
    row('retained record: admitted, response reports retained on both trees',
        all(g(s, 'record-retained').get('ok') and g(s, 'record-retained').get('availability') == 'retained' for s in (A, B)),
        {'source42': g(A, 'record-retained').get('availability'), 'source43': g(B, 'record-retained').get('availability')})
    for n in ('record-partial', 'record-partial-with-missing-ref'):
        row('%s: admitted record state partial reaches the query; source42 response reported retained, source43 reports partial' % n,
            g(A, n).get('recordState') == 'partial' == g(B, n).get('recordState') and g(A, n).get('availability') == 'retained' and g(B, n).get('availability') == 'partial',
            {'source42': g(A, n).get('availability'), 'source43': g(B, n).get('availability')})
        row('%s: same items, context and termination as the retained record on both trees (only availability differs)' % n,
            all(g(s, n).get('items') == g(s, 'record-retained').get('items') and g(s, n).get('contextMinusAvailability') == g(s, 'record-retained').get('contextMinusAvailability')
                and g(s, n).get('termination') == g(s, 'record-retained').get('termination') for s in (A, B)) and g(A, n).get('items') == g(B, n).get('items'), None)
    want = {'purged': 'evidence.purged', 'expired': 'evidence.expired', 'corrupt': 'evidence.corrupt', 'unavailable': 'evidence.missing'}
    for st, det in want.items():
        n = 'record-' + st
        row('%s: admitted state routes as the observation to HOST.IO_FAILURE / %s / exit 4, no run, identically' % (n, det),
            all(g(s, n).get('stage') == 'query' and g(s, n).get('ok') is False and g(s, n).get('errorCode') == 'HOST.IO_FAILURE' and g(s, n).get('detail') == det
                and g(s, n).get('exitCode') == 4 and g(s, n).get('hasRun') is False for s in (A, B)), {'source43': g(B, n)})
    for n in ('record-unparseable', 'record-unknown-state', 'record-other-run', 'record-missing-reason'):
        row('%s: record failing identity availability admission is evidence.corrupt at the record stage on both trees' % n,
            all(g(s, n).get('stage') == 'record' and g(s, n).get('errorCode') == 'HOST.IO_FAILURE' and g(s, n).get('detail') == 'evidence.corrupt' for s in (A, B)), {'source43': g(B, n)})
    for n, det in (('record-partial-corrupt-bytes', 'evidence.corrupt'), ('record-partial-missing-bytes', 'evidence.missing'), ('record-retained-missing-bytes', 'evidence.missing')):
        row('%s: the record observation grants nothing; close_run refuses %s on both trees' % (n, det),
            all(g(s, n).get('ok') is False and g(s, n).get('detail') == det and g(s, n).get('exitCode') == 4 for s in (A, B)), {'source42': g(A, n), 'source43': g(B, n)})
    for lab in ('null', 'unknown'):
        n = 'adapter-invalid-' + lab
        row('%s: adapter projects SYSTEM.OUTCOME.ILLEGAL_STATE / HOST.INVARIANT_VIOLATED / host-invariant / exit 4, subject host.availability, no run; without RequestId stays a precondition' % n,
            all(g(s, n).get('precondition') == 'host.availability' and g(s, n).get('errorCode') == 'SYSTEM.OUTCOME.ILLEGAL_STATE' and g(s, n).get('detail') == 'HOST.INVARIANT_VIOLATED'
                and g(s, n).get('faultCause') == 'host-invariant' and g(s, n).get('klass') == 'operational-failed' and g(s, n).get('exitCode') == 4
                and g(s, n).get('subject') == 'host.availability' and g(s, n).get('hasRun') is False and g(s, n).get('runIdOnTermination') is False
                and g(s, n).get('withoutRequestId') == 'precondition:host.requestId' for s in (A, B)), {'source43': g(B, n)})
    row('a RequestId precondition is never projected by the adapter on both trees', A.get('adapter-requestid-precondition') == B.get('adapter-requestid-precondition') == 'precondition:host.requestId',
        B.get('adapter-requestid-precondition'))
    OUT.write_text(json.dumps({'standing': 'independent reviewer adapter-path discrimination; each tree own modules in its own process; lawful closed Run; reference adapter laws only, no product host adapter or store',
                               'rows': rows, 'failed': [r for r in rows if not r['ok']], 'childRuns': runs}, indent=1, default=str))
    print(json.dumps({'total': len(rows), 'failed': [(r['case'], r['observed']) for r in rows if not r['ok']]}, indent=1, default=str)[:8000])


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--child':
        child(sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        parent()
