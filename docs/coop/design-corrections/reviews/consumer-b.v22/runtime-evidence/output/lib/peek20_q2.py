"""Dump the graph params, evidence disclosure and row defs exactly."""
import json

S = '/tmp/opensip-design-corrections/consumer-b.v22/subject/'
P = S + 'docs/coop/design-corrections/workflows/schemas/evaluator3/graph-query.schema.json'
d = json.load(open(P))
for name in ('GraphPathParams', 'GraphReachParams', 'GraphEvidenceDisclosure', 'ScopeId',
             'FactId', 'ViewDigest', 'GraphPathRow', 'GraphReachRow', 'GraphPathEdge',
             'NativeSubjectId', 'StoredKind', 'FactViewDigests'):
    node = d['$defs'].get(name)
    print('===== %s' % name)
    print(json.dumps(node, indent=1)[:2000])
    print()
