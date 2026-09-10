"""Schema probes only: no graph engine, sealed Run, or product implementation.

These demonstrate admitted wire shapes, not that an authoritative query owner
accepts the corresponding semantics. Synthetic IDs are grammar-valid labels.
"""
import copy
import hashlib
import json
import sys
from pathlib import Path

from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

ROOT = Path('/tmp/opensip-design-corrections/candidate-subject.v23')
WF = ROOT / 'docs/coop/design-corrections/workflows/schemas'
sys.path.insert(0, str(ROOT / 'docs/coop/design-corrections/foundation'))
import canonical

docs = [json.loads(p.read_text()) for p in sorted((WF / 'evaluator3').glob('*.schema.json'))]
docs += [json.loads((WF / n).read_text()) for n in ['common.schema.json', 'imported-evidence.schema.json', 'policy-document.schema.json', 'policy-document.v2.schema.json', 'test-execution.schema.json']]
reg = Registry().with_resources((d['$id'], Resource(contents=d, specification=DRAFT202012)) for d in docs)
base = 'urn:opensip:product-v1:workflows:evaluator3:graph-query:2'
def admitted(selector, value):
    try:
        canonical.typed(value)
        canonical.ExactValidator({'$ref': base + '#/$defs/' + selector}, registry=reg).validate(value)
        return {'schemaAdmitted': True}
    except Exception as exc:
        return {'schemaAdmitted': False, 'error': str(exc).splitlines()[0]}

q = {'schemaFamily': 'opensip.product.query', 'schemaMajor': 2,
     'projectId': 'prj1-' + '1' * 64, 'view': {'runId': 'run3:' + '2' * 64},
     'operation': 'graph.path', 'params': {}, 'completeness': 'required', 'page': {'size': 1}}
cx = {'projectId': q['projectId'], 'resolvedView': {'latest': True}, 'coverage': 'complete',
      'availability': 'retained', 'truncated': False, 'totalItems': 0, 'advisory': False}
cases = [
    ('graph.path-without-endpoints', 'GraphQueryRequestV1', q),
    ('response-latest-still-unresolved', 'GraphQueryResponseContext', cx),
]
q2 = copy.deepcopy(q)
q2['operation'] = 'graph.neighbors'
q2['params'] = {'baselineId': 'baseline2:' + '3' * 64}
cases.append(('graph.neighbors-with-irrelevant-baseline-only', 'GraphQueryRequestV1', q2))
q3 = copy.deepcopy(q)
q3['params'] = {'relation': 'calls', 'subject': 'src/a.ts', 'target': 'src/b.ts', 'direction': 'both', 'maxDepth': 2}
cases.append(('file-path-only-calls-request', 'GraphQueryRequestV1', q3))
cx2 = copy.deepcopy(cx)
cx2['resolvedView'] = q['view']
cx2['advisory'] = True
cases.append(('graph-context-advisory-true-not-cross-joined', 'GraphQueryResponseContext', cx2))
result = {'standing': 'review-only schema observations; not actual query execution or Run admission',
          'subjectManifestSha256': '652c800166a8d3f37eacfbf273c9786bb84f6fd6b5c6ead57b5a254315859a25',
          'schemaSha256': hashlib.sha256((WF/'evaluator3/graph-query.schema.json').read_bytes()).hexdigest(),
          'probes': [{'name': n, 'selector': s, 'value': v, **admitted(s, v)} for n,s,v in cases]}
Path(__file__).with_name('query-schema-probe.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({r['name']: r['schemaAdmitted'] for r in result['probes']}, indent=2))
