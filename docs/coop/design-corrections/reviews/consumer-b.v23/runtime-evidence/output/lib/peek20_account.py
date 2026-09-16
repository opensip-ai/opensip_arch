"""Read-only inspector for the generation-20 execution-inputs schema annotations."""
import json
import sys

S = '/tmp/opensip-design-corrections/consumer-b.v23/subject/'
d = json.load(open(S + 'docs/coop/design-corrections/foundation/execution-inputs.schema.v1.json'))
which = sys.argv[1] if len(sys.argv) > 1 else 'NativeCoverageAccountV1'
node = d['$defs'][which]
print('== %s x-keys: %s' % (which, [k for k in node if k.startswith('x-')]))
for k in node:
    if k.startswith('x-'):
        print('-- %s' % k)
        print(json.dumps(node[k], indent=1)[:3000])
if node.get('description'):
    print('-- description')
    print(node['description'][:2000])
for p, v in (node.get('properties') or {}).items():
    if v.get('description'):
        print('-- properties/%s DESC' % p)
        print(v['description'][:1200])
