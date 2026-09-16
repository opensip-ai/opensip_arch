"""Exact unified diffs source39 -> source40 for every changed path (both sides hash-verified against their manifests),
plus line/length stats for changed and added files."""
import difflib, hashlib, json, os

RT = '/private/tmp/opensip-design-corrections/claude-independent-design.v40'
S39 = '/tmp/opensip-design-corrections/candidate-subject.v39'
S40 = '/tmp/opensip-design-corrections/candidate-subject.v40'
ver = json.load(open(RT + '/receipts/subject-verification.json'))
OUT = RT + '/receipts/delta-diffs'
os.makedirs(OUT, exist_ok=True)
rows = []
for c in ver['delta']['changed']:
    a = open(os.path.join(S39, c['path']), 'rb').read()
    b = open(os.path.join(S40, c['path']), 'rb').read()
    assert hashlib.sha256(a).hexdigest() == c['sha39'], c['path']
    assert hashlib.sha256(b).hexdigest() == c['sha40'], c['path']
    al = a.decode('utf-8').splitlines(keepends=True)
    bl = b.decode('utf-8').splitlines(keepends=True)
    d = list(difflib.unified_diff(al, bl, 'a39/' + c['path'], 'b40/' + c['path'], n=3))
    name = c['path'].replace('/', '__') + '.diff'
    open(os.path.join(OUT, name), 'w').write(''.join(d))
    rows.append({'path': c['path'], 'sha39': c['sha39'], 'sha40': c['sha40'], 'bytes40': c['bytes40'], 'lines39': len(al), 'lines40': len(bl),
                 'added': sum(1 for x in d if x.startswith('+') and not x.startswith('+++')),
                 'removed': sum(1 for x in d if x.startswith('-') and not x.startswith('---')),
                 'diffLines': len(d), 'maxDiffLineLen': max([len(x) for x in d] or [0]), 'maxLineLen40': max([len(x) for x in bl] or [0]),
                 'diff': 'receipts/delta-diffs/' + name})
for c in ver['delta']['added']:
    b = open(os.path.join(S40, c['path']), 'rb').read()
    assert hashlib.sha256(b).hexdigest() == c['sha40']
    try:
        bl = b.decode('utf-8').splitlines(keepends=True)
    except UnicodeDecodeError:
        bl = []
    rows.append({'path': c['path'], 'sha40': c['sha40'], 'bytes40': c['bytes40'], 'added-file': True, 'lines40': len(bl), 'maxLineLen40': max([len(x) for x in bl] or [0])})
for c in ver['delta']['removed']:
    rows.append({'path': c['path'], 'sha39': c['sha39'], 'removed-file': True})
json.dump(rows, open(RT + '/receipts/delta-diff-summary.json', 'w'), indent=1)
for r in rows:
    print(json.dumps({k: r[k] for k in r if k not in ('sha39', 'sha40', 'diff')}))
