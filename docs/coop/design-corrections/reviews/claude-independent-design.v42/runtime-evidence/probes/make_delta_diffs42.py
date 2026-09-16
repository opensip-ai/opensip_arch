"""Exact unified diffs for every changed path of the 41->42 and 40->42 deltas (both sides hash-verified against their
manifests), plus line statistics for changed and added files."""
import difflib, hashlib, json, os

RT = '/private/tmp/opensip-design-corrections/claude-independent-design.v42'
S = {v: '/tmp/opensip-design-corrections/candidate-subject.v' + v for v in ('40', '41', '42')}
ver = json.load(open(RT + '/receipts/subject-verification.json'))
summary = {}
for key, a, b in (('41to42', '41', '42'), ('40to42', '40', '42')):
    out = RT + '/receipts/delta-diffs-' + key
    os.makedirs(out, exist_ok=True)
    rows = []
    d = ver['delta'][key]
    for c in d['changed']:
        x = open(os.path.join(S[a], c['path']), 'rb').read()
        y = open(os.path.join(S[b], c['path']), 'rb').read()
        assert hashlib.sha256(x).hexdigest() == c['shaA'] and hashlib.sha256(y).hexdigest() == c['shaB'], c['path']
        try:
            xl, yl = x.decode('utf-8').splitlines(keepends=True), y.decode('utf-8').splitlines(keepends=True)
        except UnicodeDecodeError:
            rows.append({'path': c['path'], 'binary': True})
            continue
        diff = list(difflib.unified_diff(xl, yl, 'a%s/%s' % (a, c['path']), 'b%s/%s' % (b, c['path']), n=3))
        name = c['path'].replace('/', '__') + '.diff'
        open(os.path.join(out, name), 'w').write(''.join(diff))
        rows.append({'path': c['path'], 'shaA': c['shaA'], 'shaB': c['shaB'], 'linesA': len(xl), 'linesB': len(yl),
                     'added': sum(1 for l in diff if l.startswith('+') and not l.startswith('+++')),
                     'removed': sum(1 for l in diff if l.startswith('-') and not l.startswith('---')),
                     'diffLines': len(diff), 'diff': 'receipts/delta-diffs-%s/%s' % (key, name)})
    for c in d['added']:
        y = open(os.path.join(S[b], c['path']), 'rb').read()
        assert hashlib.sha256(y).hexdigest() == c['shaB']
        try:
            yl = y.decode('utf-8').splitlines(keepends=True)
        except UnicodeDecodeError:
            yl = []
        rows.append({'path': c['path'], 'shaB': c['shaB'], 'addedFile': True, 'linesB': len(yl)})
    for c in d['removed']:
        rows.append({'path': c['path'], 'shaA': c['shaA'], 'removedFile': True})
    summary[key] = rows
json.dump(summary, open(RT + '/receipts/delta-diff-summary.json', 'w'), indent=1)
for key, rows in summary.items():
    print('==', key)
    for r in rows:
        print(json.dumps({k: r[k] for k in r if k not in ('shaA', 'shaB', 'diff')}))
