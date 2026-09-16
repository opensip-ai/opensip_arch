"""Complete the declared record-adapter call with its exact request context.
Preserves the earlier lower-level owner captures; no consumer or source changes.
"""
from pathlib import Path
import json, hashlib, importlib.util, shutil
B = Path('/tmp/opensip-design-corrections')
L = Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews')
O = Path(__file__).parent
V = B / 'consumer-b.v24-source43.v1/output/vectors/graph-query.json'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(V) == 'b26ead7f6a89d9deeb1de482052cf7d371dec213b1f46eb7a0f157be5852f2cd'
sp = importlib.util.spec_from_file_location('root_record_context_query43', B / 'candidate-subject.v43/docs/coop/design-corrections/workflows/query_projection_model.v3.py')
Q = importlib.util.module_from_spec(sp)
sp.loader.exec_module(Q)
v = json.loads(V.read_bytes())
selected = {'retained-availability-record-other-run-corrupt', 'retained-availability-record-missing-state-corrupt', 'retained-availability-record-duplicate-key-bytes-corrupt'}
rows = []
for x in v['vectors']:
    if x['vector'] not in selected:
        continue
    host, req = x['hostObservations'], x['request']
    try:
        Q.observe_retained_availability(bytes.fromhex(host['availabilityRecord']['rawBytesHex']), v['runs']['cmp-code'])
        raise AssertionError('Expected record refusal')
    except Q.QueryRefusal as exc:
        env = Q.failure_envelope(exc, req, host)
    other = x['failureEnvelope']
    def route(e):
        t = e['termination']
        return [e['kind'], e['requestId'], e.get('projectId'), e['exitCode'], t['class'], t['errorCode'], t['faultCause'], t['domainDetail']['code'], 'run' in e]
    assert route(env) == route(other)
    rows.append({'vector': x['vector'], 'ownerEnvelopeWithExactRequest': env, 'consumerEnvelope': other, 'structuredRouteAndRequestContextEqual': True})
assert len(rows) == 3
out = {'standing': 'Three earlier comparison mismatches arose because the root collector invoked the low-level record refusal envelope without its request context, omitting optional projectId. The consumer complete adapter includes its admitted request projectId lawfully. Calling the frozen envelope owner with that exact request produces equal structured route and context. Earlier raw captures/comparison remain preserved; no new design defect, consumer repair or root full-charter assent.', 'vectorsSha256': sha(V), 'priorComparisonSha256': sha(B / 'root-blind43-query-comparison.v1/comparison.json'), 'rows': rows, 'remainingUnaccountedStructuredComparisons': 0, 'rootBlindAssent': False}
(O / 'assessment.json').write_text(json.dumps(out, indent=2) + '\n')
shutil.copytree(O, L / O.name)
print(json.dumps({'measured': len(rows), 'remainingUnaccounted': 0, 'assessmentSha256': sha(O / 'assessment.json')}))
