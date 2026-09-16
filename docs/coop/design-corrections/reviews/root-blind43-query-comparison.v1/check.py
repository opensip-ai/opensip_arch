"""Compare measured outputs and validate exact exported carriers, without executing consumer code.
Not whole-charter acceptance; opaque host cursors and diagnostic prose are not equality contracts.
"""
from pathlib import Path
import hashlib, importlib.util, json, re, shutil

B = Path('/tmp/opensip-design-corrections')
L = Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews')
O = Path(__file__).parent
S = B / 'candidate-subject.v43'
C = B / 'consumer-b.v24-source43.v1/output'
V = C / 'vectors/graph-query.json'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(V) == 'b26ead7f6a89d9deeb1de482052cf7d371dec213b1f46eb7a0f157be5852f2cd'
spec = importlib.util.spec_from_file_location('root_query_surface43', S / 'docs/coop/design-corrections/workflows/query_surface_projection.v3.py')
P = importlib.util.module_from_spec(spec)
spec.loader.exec_module(P)
v = json.loads(V.read_bytes())
assert len(v['vectors']) == 66
vectors = {r['vector']: r for r in v['vectors']}
command = {'parityFields': list(P.QUERY_PARITY_FIELDS)}

def differences(a, b, path=''):
    if type(a) != type(b):
        return [{'path': path, 'kind': 'type', 'owner': a, 'consumer': b}]
    if isinstance(a, dict):
        out = []
        for k in sorted(set(a) | set(b)):
            p = path + '/' + k
            if k not in a or k not in b:
                out.append({'path': p, 'kind': 'absent', 'ownerPresent': k in a, 'consumerPresent': k in b, 'owner': a.get(k), 'consumer': b.get(k)})
            else:
                out += differences(a[k], b[k], p)
        return out
    if isinstance(a, list):
        if len(a) != len(b):
            return [{'path': path, 'kind': 'length', 'owner': a, 'consumer': b}]
        return sum((differences(x, y, path + '/' + str(i)) for i, (x, y) in enumerate(zip(a, b))), [])
    return [{'path': path, 'kind': 'value', 'owner': a, 'consumer': b}] if a != b else []

carrier_rows = []
for r in v['vectors']:
    out = {'vector': r['vector'], 'passed': False}
    try:
        env = r.get('envelope', r.get('failureEnvelope'))
        P._admit(P.ENVELOPE_REF, env, 'EXPORTED_ENVELOPE')
        assert env['requestId'] == r['hostObservations']['requestId']
        if 'response' in r:
            projected = P.project_query_surface(r['response'], r['termination'], envelope=env, command=command)
            for fmt, text in r['renderings'].items():
                body = json.loads(text) if fmt in ('json', 'agent') else text
                recovered = P._parity_from_rendering({'format': fmt, 'body': body}, command)
                assert P._equal(recovered, projected['parity'])
            assert set(r['renderings']) == {'human', 'json', 'agent'}
            out['scope'] = 'exact response/envelope/summary joins and three exported renderer parities'
        else:
            assert env['kind'] == 'failure' and 'run' not in env
            assert env['termination']['domainDetail']['code'] == r['firstRefusal']
            out['scope'] = 'exact failure envelope schema and declared detail; not underlying negative store replay'
        out['passed'] = True
    except Exception as exc:
        out.update(exceptionType=type(exc).__name__, reason=str(exc))
    carrier_rows.append(out)

comparisons = []
for path in sorted((B / 'root-blind43-query-envelope-capture.v1').glob('*/report.json')):
    report = json.loads(path.read_bytes())
    assert report['semanticAdmission'] == 'ADMIT' and report['captureCompleted']
    for measured in report['cases']:
        r = vectors[measured['vector']]
        out = {'vector': r['vector'], 'captureSha256': sha(path), 'boundary': measured['boundary']}
        a, b = measured.get('ownerResponse'), r.get('response')
        if a is not None and b is not None:
            ds = differences(a, b)
            unexpected = []
            for d in ds:
                p = d['path']
                if p == '/termination' and d['owner'] == {'class': 'success'} and r['termination'] == d['owner']:
                    d['assessment'] = 'Optional response termination omitted; exact success termination is on the admitted envelope.'
                elif p == '/context/nextCursor':
                    d['assessment'] = 'Opaque host token; no cross-host byte equality or translation required.'
                elif re.fullmatch(r'/context/evidence/resolutionLimitations/\d+/note', p):
                    d['assessment'] = 'Optional bounded prose; exact consumer carrier and renderer parity independently admitted.'
                elif re.fullmatch(r'/context/evidence/deficiencyCitations/\d+/nativeCause', p):
                    d['assessment'] = 'Optional schema field; required exact source/cause/inputRefs remain equal.'
                else:
                    unexpected.append(d)
            out.update(responseDifferences=ds, unexpected=unexpected)
        elif a is None and b is not None:
            env = measured.get('ownerFailureEnvelope', {})
            opaque = r['vector'] in {'page2-after-newer-latest-bound-run', 'page2-with-host-cache-present'} and env.get('termination', {}).get('domainDetail', {}).get('code') == 'QUERY.CURSOR_MISMATCH'
            out.update(assessment='Consumer-issued opaque cursor presented to a different host. Same-host consumer execution is separate; no portability claim.', unexpected=[] if opaque else ['unaccounted return/refusal difference'])
        else:
            ae, be = measured.get('ownerFailureEnvelope'), r.get('failureEnvelope')
            def route(env):
                t = env['termination']
                return [env['kind'], env['requestId'], env.get('projectId'), env['exitCode'], t['class'], t['errorCode'], t.get('faultCause'), t['domainDetail']['code'], t.get('runId'), 'run' in env]
            equal = ae is not None and be is not None and route(ae) == route(be)
            out.update(structuredRouteEqual=equal, envelopeDifferences=differences(ae, be), unexpected=[] if equal else ['structured route mismatch'])
        comparisons.append(out)
assert len(comparisons) == 63
out = {'standing': 'Scoped root comparison only; no consumer imports, input repair, remint, token translation or whole-charter assent. Exact carriers independently checked; same-host cursor semantics remain consumer evidence. One tampered-verdict store was not exported and is not root replayed.', 'vectorsSha256': sha(V), 'carrierRows': carrier_rows, 'capturedComparisons': comparisons, 'carrierFailures': [r for r in carrier_rows if not r['passed']], 'unaccountedComparisons': [r for r in comparisons if r['unexpected']], 'rootBlindAssent': False}
(O / 'comparison.json').write_text(json.dumps(out, indent=2) + '\n')
shutil.copytree(O, L / O.name)
print(json.dumps({'carriers': len(carrier_rows), 'carrierFailures': out['carrierFailures'], 'comparisons': len(comparisons), 'unaccounted': out['unaccountedComparisons'], 'comparisonSha256': sha(O / 'comparison.json')}))
