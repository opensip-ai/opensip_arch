"""Dump the query Params/View/ResolvedView/CountBasis defs and the non-graph allOf joins."""
import json

S = '/tmp/opensip-design-corrections/consumer-b.v22/subject/'
P = S + 'docs/coop/design-corrections/workflows/schemas/evaluator3/graph-query.schema.json'
d = json.load(open(P))
for name in ('Params', 'View', 'ResolvedView', 'CountBasis', 'AdvisoryOperation',
             'GraphOperation', 'GraphNeighborsParams', 'GraphNeighborRow', 'GraphEndpoint'):
    node = d['$defs'][name]
    print('===== %s required=%s' % (name, node.get('required')))
    print(json.dumps({k: v for k, v in node.items() if k != 'description'}, indent=1)[:2200])
    if node.get('description'):
        print('DESC:', node['description'][:700])
    print()
req = d['$defs']['GraphQueryRequestV1']
print('===== request allOf branch count:', len(req.get('allOf') or []))
for i, br in enumerate(req.get('allOf') or []):
    cond = json.dumps(br.get('if'))[:150]
    then = json.dumps(br.get('then'))[:200]
    print('  [%d] if %s then %s' % (i, cond, then))
