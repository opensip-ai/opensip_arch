"""Source43 prose-law probe (verified copy work/source43-pkg, own modules): an optional limitation note and refusal diagnostic
prose obey schema, parity and route laws without any canonical wording. Writes only receipts/probes/query-prose43.json.
  - a limitation note may be any BoundedText: rewording it keeps GraphQueryResponseV1 admission and renderer parity (the
    note travels inside query-response parity unchanged); a note over 1024 characters is refused by schema admission.
  - a success StepTermination carries no errorCode/reasonCodes/signal/faultCause (schema branch).
  - QueryRefusal diagnostic text is private: two refusals differing only in diagnostic build identical envelopes; remedy prose
    changes only domainDetail.remedy, never the route (errorCode, detail, class, exit)."""
import contextlib, copy, importlib.util, io, json, sys
from pathlib import Path

RT = Path('/private/tmp/opensip-design-corrections/claude-independent-design.v43')
WF = RT / 'work/source43-pkg/docs/coop/design-corrections/workflows'
sys.path.insert(0, str(WF.parent / 'foundation'))
ROWS = []


def row(case, ok, observed=None):
    ROWS.append({'case': case, 'ok': bool(ok), 'observed': observed})


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(mod)
    return mod


Q = load('prose43_q', WF / 'query_projection_model.v3.py')
QS = load('prose43_qs', WF / 'query_surface_projection.v3.py')
command = next(c for c in json.loads((WF / 'command-inventory.v3.json').read_text())['commands'] if c['name'] == 'query')
RID = 'req1_' + 'b' * 32


def admits(ref, value):
    try:
        Q.validate_schema(ref, value)
        return True, ''
    except Exception as exc:  # noqa: BLE001
        return False, type(exc).__name__ + ':' + str(exc).splitlines()[0][:160]


def parity_render(resp):
    term = resp['termination']
    env = {'schemaFamily': 'opensip.product.envelope', 'schemaMajor': 3, 'kind': 'query', 'requestId': RID, 'projectId': resp['context']['projectId'],
           'termination': term, 'exitCode': QS.Wlegacy.EXIT[term['class']], 'query': QS.graph_query_result_summary(resp),
           'querySurface': 'graph-query-response', 'queryResponse': copy.deepcopy(resp)}
    proj = QS.project_query_surface(resp, term, envelope=env, command=command)
    rnd = QS.render_query_formats(proj['parity'], env, command, hints=[])
    bodies = {r['format']: r['body'] for r in rnd['renderings']}
    return proj, rnd, bodies


u = 'c' * 64
s, x, t = ({'universe': u, 'kind': 'symbol', 'nativeSubjectId': 'symbol:' + n} for n in ('s', 'x', 't'))


def e(n, src, dst):
    return {'confidenceMillionths': 1000000, 'factId': 'fact2:' + n * 64, 'producerClosure': 'closure2:' + 'd' * 64, 'relation': 'references',
            'resolution': 'resolved-binding', 'source': src, 'target': dst}


params = {'relation': 'references', 'minResolution': 'resolved-binding', 'direction': 'outgoing', 'start': s, 'maxDepth': 4, 'includeStart': True}
bounds = dict(Q.PUBLIC_BOUNDS, maxVisitedNodes=1)
resp = Q.traverse_projected_graph('graph.reach', params, [e('1', s, x), e('2', x, t)], bounds=bounds, completeness='best-effort',
                                  project_id='prj1-' + 'e' * 64, run_id='run3:' + 'f' * 64)
lims = resp['context']['evidence']['resolutionLimitations']
row('bounded reach yields a success response carrying the model limitation note', resp['termination'] == {'class': 'success'} and any('note' in l for l in lims), lims)
ref = Q.SCHEMA_ID + '#/$defs/GraphQueryResponseV1'
reworded = copy.deepcopy(resp)
for l in reworded['context']['evidence']['resolutionLimitations']:
    if 'note' in l:
        l['note'] = 'host-chosen wording: the visit cap stopped the walk before its frontier was exhausted'
ok_a, why_a = admits(ref, resp)
ok_b, why_b = admits(ref, reworded)
row('rewording the limitation note keeps schema admission (no canonical wording)', ok_a and ok_b, [why_a, why_b])
p1, r1, b1 = parity_render(resp)
p2, r2, b2 = parity_render(reworded)
row('each wording renders human/json/agent with parity holding; the note travels verbatim inside query-response parity',
    r1['ok'] and r1['parityHolds'] and r2['ok'] and r2['parityHolds'] and p2['parity']['query-response'] == reworded
    and b2['json']['queryResponse']['context']['evidence']['resolutionLimitations'] == reworded['context']['evidence']['resolutionLimitations'],
    {'formats': sorted(b1), 'scalarParityEqualAcrossWordings': {k: p1['parity'][k] == p2['parity'][k] for k in ('resolved-view', 'availability', 'truncated', 'total-items', 'termination-class')}})
row('scalar parity fields do not depend on the wording', all(p1['parity'][k] == p2['parity'][k] for k in ('resolved-view', 'availability', 'truncated', 'total-items', 'termination-class')))
too_long = copy.deepcopy(resp)
for l in too_long['context']['evidence']['resolutionLimitations']:
    if 'note' in l:
        l['note'] = 'n' * 1025
ok_c, why_c = admits(ref, too_long)
row('a limitation note over 1024 characters is refused by schema admission (BoundedText)', not ok_c, why_c)
term_ref = Q.COMMON_ID + '#/$defs/StepTermination'
row('success termination admits no errorCode/reasonCodes/signal/faultCause', not admits(term_ref, {'class': 'success', 'errorCode': 'HOST.IO_FAILURE'})[0]
    and not admits(term_ref, {'class': 'success', 'reasonCodes': ['QUERY.COMPLETENESS_UNMET']})[0] and admits(term_ref, {'class': 'success'})[0])
host = {'requestId': RID}


def refusal(diag, remedy='restore the exact retained closure bytes or report their unavailability'):
    r = Q.QueryRefusal('HOST.IO_FAILURE', 'evidence.corrupt', remedy, 'run3:' + 'f' * 64, klass='operational-failed', fault_cause='host-io', diagnostic=diag)
    return r.envelope(host)


env_a, env_b = refusal('AdmissionError: digest mismatch at object 17'), refusal('completely different private diagnostic prose')
row('refusal diagnostic prose is private: envelopes identical for different diagnostics', env_a == env_b and 'diagnostic' not in json.dumps(env_a), env_a)
env_c = refusal('x', remedy='another remedy wording')
route = lambda v: (v['termination']['class'], v['termination']['errorCode'], v['termination']['faultCause'], v['termination']['domainDetail']['code'], v['exitCode'])
row('remedy wording changes only domainDetail.remedy, never the route', route(env_a) == route(env_c) and env_a['termination']['domainDetail']['remedy'] != env_c['termination']['domainDetail']['remedy'],
    {'routeA': route(env_a), 'routeC': route(env_c)})
out = RT / 'receipts/probes/query-prose43.json'
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps({'standing': 'independent reviewer probe on the verified source43 copy; reference Python models; not product qualification',
                           'rows': ROWS, 'failed': [r for r in ROWS if not r['ok']]}, indent=1, default=str))
print(json.dumps({'total': len(ROWS), 'failed': [(r['case'], r['observed']) for r in ROWS if not r['ok']]}, indent=1, default=str))
