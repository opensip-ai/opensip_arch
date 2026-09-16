"""Dump several evaluator3 graph-query defs at once (read-only)."""
import json

S = '/tmp/opensip-design-corrections/consumer-b.v22/subject/'
P = S + 'docs/coop/design-corrections/workflows/schemas/evaluator3/graph-query.schema.json'
d = json.load(open(P))
for name in ('GraphQueryRequestV1', 'GraphQueryResponseContext', 'GraphOperationResponseContext',
             'Page', 'Bounds', 'TraversalCoverage', 'GraphEvidenceDisclosure',
             'AdvisoryOperation', 'ResolvedView', 'View', 'Params', 'CountBasis',
             'GraphNeighborRow'):
    node = d['$defs'][name]
    print('===== %s  required=%s' % (name, node.get('required')))
    body = {k: v for k, v in node.items() if k != 'description'}
    print(json.dumps(body, indent=1)[:1900])
    if node.get('description'):
        print('DESC:', node['description'][:900])
    print()
