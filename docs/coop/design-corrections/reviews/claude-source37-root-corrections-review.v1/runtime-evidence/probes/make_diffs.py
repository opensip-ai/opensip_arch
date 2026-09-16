"""Unified diffs base(source37, beforeSha256-verified) -> overlay(subject/, sha256-verified) for all overlay rows."""
import difflib, hashlib, json, os

RT = '/private/tmp/opensip-design-corrections/claude-source37-root-corrections-review.v1'
SRC = '/tmp/opensip-design-corrections/candidate-subject.v37'
OUTD = RT + '/receipts/diffs'
os.makedirs(OUTD, exist_ok=True)
ov = json.load(open(RT + '/subject-manifest.json'))
summary = []
for f in ov['files']:
    a = open(os.path.join(SRC, f['path']), 'rb').read()
    b = open(os.path.join(RT, 'subject', f['path']), 'rb').read()
    assert hashlib.sha256(a).hexdigest() == f['beforeSha256'], f['path']
    assert hashlib.sha256(b).hexdigest() == f['sha256'], f['path']
    al = a.decode('utf-8').splitlines(keepends=True)
    bl = b.decode('utf-8').splitlines(keepends=True)
    diff = list(difflib.unified_diff(al, bl, 'a/' + f['path'], 'b/' + f['path'], n=3))
    name = f['path'].replace('/', '__') + '.diff'
    open(os.path.join(OUTD, name), 'w').write(''.join(diff))
    added = sum(1 for x in diff if x.startswith('+') and not x.startswith('+++'))
    removed = sum(1 for x in diff if x.startswith('-') and not x.startswith('---'))
    summary.append({'path': f['path'], 'diff': 'receipts/diffs/' + name, 'diffLines': len(diff), 'added': added, 'removed': removed,
                    'baseLines': len(al), 'overlayLines': len(bl), 'maxDiffLineLen': max([len(x) for x in diff] or [0])})
json.dump(summary, open(RT + '/receipts/diff-summary.json', 'w'), indent=1)
for s in summary:
    print(s)
