import json
S='/private/tmp/opensip-design-corrections/claude-root-binding-correction.v1/scratch'
def load(t):
    return json.load(open(S+'/'+t+'/docs/coop/design-corrections/foundation/identity-report.json'))['checks']
a={}; b={}
for r in load('baseline25'): a[r['id']]=r['passed']
for r in load('src25'): b[r['id']]=r['passed']
for k in sorted(set(a)|set(b)):
    if a.get(k)!=b.get(k): print('DIFFERS', k, '| baseline', a.get(k), '| src25', b.get(k))
print('src25 failing ids:', [k for k,v in b.items() if not v])
