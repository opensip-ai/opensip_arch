"""Exact unified diffs source38 -> source39 for every changed path (both sides hash-verified against their manifests),
plus line/length stats for changed and added files."""
import difflib, hashlib, json, os

RT = '/private/tmp/opensip-design-corrections/claude-independent-design.v39'
S38 = '/tmp/opensip-design-corrections/candidate-subject.v38'
S39 = '/tmp/opensip-design-corrections/candidate-subject.v39'
ver = json.load(open(RT + '/receipts/subject-verification.json'))
OUT = RT + '/receipts/delta-diffs'
os.makedirs(OUT, exist_ok=True)
rows = []
for c in ver['delta']['changed']:
    a = open(os.path.join(S38, c['path']), 'rb').read()
    b = open(os.path.join(S39, c['path']), 'rb').read()
    assert hashlib.sha256(a).hexdigest() == c['sha38'], c['path']
    assert hashlib.sha256(b).hexdigest() == c['sha39'], c['path']
    al = a.decode('utf-8').splitlines(keepends=True)
    bl = b.decode('utf-8').splitlines(keepends=True)
    d = list(difflib.unified_diff(al, bl, 'a38/' + c['path'], 'b39/' + c['path'], n=3))
    name = c['path'].replace('/', '__') + '.diff'
    open(os.path.join(OUT, name), 'w').write(''.join(d))
    rows.append({'path': c['path'], 'sha38': c['sha38'], 'sha39': c['sha39'], 'bytes39': c['bytes39'], 'lines38': len(al), 'lines39': len(bl),
                 'added': sum(1 for x in d if x.startswith('+') and not x.startswith('+++')),
                 'removed': sum(1 for x in d if x.startswith('-') and not x.startswith('---')),
                 'diffLines': len(d), 'maxDiffLineLen': max([len(x) for x in d] or [0]), 'maxLineLen39': max([len(x) for x in bl] or [0]),
                 'diff': 'receipts/delta-diffs/' + name})
for c in ver['delta']['added']:
    b = open(os.path.join(S39, c['path']), 'rb').read()
    assert hashlib.sha256(b).hexdigest() == c['sha39']
    try:
        bl = b.decode('utf-8').splitlines(keepends=True)
    except UnicodeDecodeError:
        bl = []
    rows.append({'path': c['path'], 'sha39': c['sha39'], 'bytes39': c['bytes39'], 'added-file': True, 'lines39': len(bl), 'maxLineLen39': max([len(x) for x in bl] or [0])})
for c in ver['delta']['removed']:
    rows.append({'path': c['path'], 'sha38': c['sha38'], 'removed-file': True})
json.dump(rows, open(RT + '/receipts/delta-diff-summary.json', 'w'), indent=1)
for r in rows:
    print(json.dumps({k: r[k] for k in r if k not in ('sha38', 'sha39', 'diff')}))
