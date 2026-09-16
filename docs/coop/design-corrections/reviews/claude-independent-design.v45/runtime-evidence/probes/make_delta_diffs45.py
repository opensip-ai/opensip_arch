"""Exact unified diffs for every changed path of the 44->45 delta and complete creation diffs for every added path (both sides
hash-verified against their manifests)."""
import difflib, hashlib, json, os

RT = '/private/tmp/opensip-design-corrections/claude-independent-design.v45'
S = {v: '/tmp/opensip-design-corrections/candidate-subject.v' + v for v in ('44', '45')}
ver = json.load(open(RT + '/receipts/subject-verification.json'))
out = RT + '/receipts/delta-diffs-44to45'
os.makedirs(out, exist_ok=True)
rows = []
d = ver['delta']['44to45']
for kind, items in (('changed', d['changed']), ('added', d['added'])):
    for c in items:
        y = open(os.path.join(S['45'], c['path']), 'rb').read()
        assert hashlib.sha256(y).hexdigest() == c['shaB'], c['path']
        if kind == 'changed':
            x = open(os.path.join(S['44'], c['path']), 'rb').read()
            assert hashlib.sha256(x).hexdigest() == c['shaA'], c['path']
        else:
            x = b''
        try:
            xl, yl = x.decode('utf-8').splitlines(keepends=True), y.decode('utf-8').splitlines(keepends=True)
        except UnicodeDecodeError:
            rows.append({'path': c['path'], 'kind': kind, 'binary': True})
            continue
        diff = list(difflib.unified_diff(xl, yl, ('a44/' + c['path']) if kind == 'changed' else '/dev/null', 'b45/' + c['path'], n=3))
        name = c['path'].replace('/', '__') + '.diff'
        open(os.path.join(out, name), 'w').write(''.join(diff))
        rows.append({'path': c['path'], 'kind': kind, 'shaA': c.get('shaA'), 'shaB': c['shaB'], 'linesA': len(xl), 'linesB': len(yl),
                     'added': sum(1 for l in diff if l.startswith('+') and not l.startswith('+++')),
                     'removed': sum(1 for l in diff if l.startswith('-') and not l.startswith('---')), 'diffLines': len(diff),
                     'diff': 'receipts/delta-diffs-44to45/' + name})
json.dump({'44to45': rows}, open(RT + '/receipts/delta-diff-summary.json', 'w'), indent=1)
for r in rows:
    print(json.dumps({k: r[k] for k in r if k not in ('shaA', 'shaB', 'diff')}))
