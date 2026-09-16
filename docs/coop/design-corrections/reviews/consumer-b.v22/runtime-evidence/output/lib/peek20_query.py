"""Read-only inspector for the evaluator3 graph-query owning schema."""
import json
import sys

S = '/tmp/opensip-design-corrections/consumer-b.v22/subject/'
P = S + 'docs/coop/design-corrections/workflows/schemas/evaluator3/graph-query.schema.json'
d = json.load(open(P))
what = sys.argv[1] if len(sys.argv) > 1 else 'top'
if what == 'top':
    print('$id:', d.get('$id'))
    print('x-keys:', [k for k in d if k.startswith('x-')])
    print('top keys:', [k for k in d if not k.startswith('x-')])
    print('defs:', sorted(d.get('$defs', {})))
    print()
    print('description:', (d.get('description') or '')[:1500])
elif what in d:
    print(json.dumps(d[what], indent=1)[:6000])
else:
    node = d['$defs'][what]
    print('required:', node.get('required'))
    print(json.dumps({k: v for k, v in node.items() if k != 'description'}, indent=1)[:5000])
    if node.get('description'):
        print('DESC:', node['description'][:2500])
