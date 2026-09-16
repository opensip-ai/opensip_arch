"""Exact unified diffs for every changed path of the 42->43 delta (both sides hash-verified against their manifests)."""
import difflib, hashlib, json, os

RT = '/private/tmp/opensip-design-corrections/claude-independent-design.v43'
S = {v: '/tmp/opensip-design-corrections/candidate-subject.v' + v for v in ('42', '43')}
ver = json.load(open(RT + '/receipts/subject-verification.json'))
out = RT + '/receipts/delta-diffs-42to43'
os.makedirs(out, exist_ok=True)
rows = []
d = ver['delta']['42to43']
for c in d['changed']:
    x = open(os.path.join(S['42'], c['path']), 'rb').read()
    y = open(os.path.join(S['43'], c['path']), 'rb').read()
    assert hashlib.sha256(x).hexdigest() == c['shaA'] and hashlib.sha256(y).hexdigest() == c['shaB'], c['path']
    xl, yl = x.decode('utf-8').splitlines(keepends=True), y.decode('utf-8').splitlines(keepends=True)
    diff = list(difflib.unified_diff(xl, yl, 'a42/' + c['path'], 'b43/' + c['path'], n=3))
    name = c['path'].replace('/', '__') + '.diff'
    open(os.path.join(out, name), 'w').write(''.join(diff))
    rows.append({'path': c['path'], 'shaA': c['shaA'], 'shaB': c['shaB'], 'linesA': len(xl), 'linesB': len(yl),
                 'added': sum(1 for l in diff if l.startswith('+') and not l.startswith('+++')),
                 'removed': sum(1 for l in diff if l.startswith('-') and not l.startswith('---')), 'diffLines': len(diff),
                 'diff': 'receipts/delta-diffs-42to43/' + name})
json.dump({'42to43': rows}, open(RT + '/receipts/delta-diff-summary.json', 'w'), indent=1)
for r in rows:
    print(json.dumps({k: r[k] for k in r if k not in ('shaA', 'shaB', 'diff')}))
