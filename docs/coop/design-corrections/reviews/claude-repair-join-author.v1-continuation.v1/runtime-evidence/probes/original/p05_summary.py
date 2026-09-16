"""p05 [final]: delta and custody summary.

- every file of work/source against the captured baseline hashes: changed files must be owned; unified minimal diff
  (delta-vs-captured-source.diff) and before/after hashes;
- root probe inputs unchanged against p00; root captured source still equal to capture.json;
- prior completed review deliverables of this coauthor unchanged;
- receipt exits and digests; with 'final', review.md/review.json digests (review.json parsed).
Output: receipts/p05-summary[.final].json.
"""
import difflib, hashlib, json, os, sys
from pathlib import Path

BASE = Path('/tmp/opensip-design-corrections/claude-repair-join-author.v1')
ROOT = Path('/tmp/opensip-design-corrections/root-repair-owner-probe.v2')
W = BASE / 'work' / 'source'
R = BASE / 'receipts'
final = len(sys.argv) > 1 and sys.argv[1] == 'final'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
baseline = json.loads((R / 'baseline-file-hashes.json').read_text())
p00 = json.loads((R / 'p00-copy.json').read_text())
current = {}
for dirpath, _, files in os.walk(W):
    for n in files:
        p = Path(dirpath) / n
        current[str(p.relative_to(W))] = sha(p)
changed = sorted(p for p in current if p in baseline and baseline[p] != current[p])
added, removed = sorted(set(current) - set(baseline)), sorted(set(baseline) - set(current))
diff, rows = '', []
for p in changed:
    a, b = (ROOT / 'source' / p).read_bytes(), (W / p).read_bytes()
    diff += ''.join(difflib.unified_diff(a.decode().splitlines(True), b.decode().splitlines(True), 'captured-source/' + p, 'author/' + p))
    rows.append({'path': p, 'before': baseline[p], 'after': current[p], 'rootCapturedStillBefore': sha(ROOT / 'source' / p) == baseline[p]})
(BASE / 'delta-vs-captured-source.diff').write_text(diff, encoding='utf-8')
capture = json.loads((ROOT / 'capture.json').read_text())
out = {'changedFiles': rows, 'added': added, 'removed': removed,
       'onlyOwnedFilesChanged': set(changed) <= set(p00['ownedBaseline']) and not added and not removed,
       'delta': {'path': 'delta-vs-captured-source.diff', 'sha256': hashlib.sha256(diff.encode()).hexdigest(), 'lines': diff.count('\n')},
       'rootInputsUnchanged': all(sha(ROOT / n) == h for n, h in p00['rootInputs'].items()),
       'rootCapturedSourceStillCapture': all(sha(ROOT / 'source' / f['path']) == f['sha256'] for f in capture['files'])}
PRIOR = {'/tmp/opensip-design-corrections/claude-readset-package-boundary-author.v1/review.md': '7d73425deb2d6000268c91c83da13e9743f4996206b78811b31b1b76f1a33907',
         '/tmp/opensip-design-corrections/claude-readset-package-boundary-author.v1/review.json': '214655dc36f9ea0ca0bc53f07d210cfd763b05f61dde1c2feac87bd1dba5ca77',
         '/tmp/opensip-design-corrections/claude-readset-nesting-review.v1/review.md': 'd86b9980682ff37ec85acca143d1663d66db46e5ca622287e438c5e6add6b05e',
         '/tmp/opensip-design-corrections/claude-readset-nesting-review.v1/review.json': '308a729f22ee7f7503337055f44fab305d915fa950e455157475dfa38ee3da32'}
out['priorReviewsUnchanged'] = all(sha(Path(p)) == h for p, h in PRIOR.items())
out['receiptExits'] = {p.name: json.loads(p.read_text())['exit'] for p in sorted(R.glob('*.receipt.json'))}
out['receiptDigests'] = {p.name: sha(p) for p in sorted(R.iterdir()) if p.is_file()}
if final:
    json.loads((BASE / 'review.json').read_text())
    out['review'] = {n: sha(BASE / n) for n in ('review.md', 'review.json')}
(R / ('p05-summary.final.json' if final else 'p05-summary.json')).write_text(json.dumps(out, indent=1) + '\n')
print(json.dumps({k: v for k, v in out.items() if k != 'receiptDigests'}, indent=1))
print(diff)
sys.exit(0 if out['onlyOwnedFilesChanged'] and out['rootInputsUnchanged'] and out['rootCapturedSourceStillCapture'] and out['priorReviewsUnchanged'] else 1)
