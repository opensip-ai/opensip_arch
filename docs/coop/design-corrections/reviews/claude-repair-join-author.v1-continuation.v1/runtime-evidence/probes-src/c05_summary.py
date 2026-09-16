"""c05 [final]: continuation delta, custody and command account.

- continuation work/source against the captured baseline hashes: only owned files changed, none added/removed; minimal
  unified diff against root's captured source (delta-vs-captured-source.diff) with before/after hashes; the diff bytes
  equal the carried original delta and the tree equals the original authored work/source;
- root probe inputs unchanged against p00; root captured source still equal to capture.json; prior completed reviews unchanged;
- the original runtime unchanged since c00 (full manifest);
- this continuation's command receipts (exit, times) and every receipt digest; with 'final', review.md/review.json digests.
Output: receipts/c05-summary[.final].json.
"""
import difflib, hashlib, json, os, sys
from pathlib import Path

ORIG = Path('/tmp/opensip-design-corrections/claude-repair-join-author.v1')
BASE = Path('/tmp/opensip-design-corrections/claude-repair-join-author.v1-continuation.v1')
ROOT = Path('/tmp/opensip-design-corrections/root-repair-owner-probe.v2')
W = BASE / 'work' / 'source'
R = BASE / 'receipts'
final = len(sys.argv) > 1 and sys.argv[1] == 'final'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()


def manifest(root):
    files, links = {}, {}
    for dirpath, dirnames, filenames in os.walk(root):
        for n in dirnames + filenames:
            p = Path(dirpath) / n
            if p.is_symlink(): links[str(p.relative_to(root))] = os.readlink(p)
        for n in filenames:
            p = Path(dirpath) / n
            if not p.is_symlink(): files[str(p.relative_to(root))] = sha(p)
    return {'files': files, 'symlinks': links}


baseline = json.loads((R / 'baseline-file-hashes.json').read_text())
p00 = json.loads((R / 'p00-copy.json').read_text())
current = manifest(W)['files']
changed = sorted(p for p in current if p in baseline and baseline[p] != current[p])
added, removed = sorted(set(current) - set(baseline)), sorted(set(baseline) - set(current))
diff, rows = '', []
for p in changed:
    a, b = (ROOT / 'source' / p).read_bytes(), (W / p).read_bytes()
    diff += ''.join(difflib.unified_diff(a.decode().splitlines(True), b.decode().splitlines(True), 'captured-source/' + p, 'author/' + p))
    rows.append({'path': p, 'before': baseline[p], 'after': current[p], 'rootCapturedStillBefore': sha(ROOT / 'source' / p) == baseline[p]})
(BASE / 'delta-vs-captured-source.diff').write_text(diff, encoding='utf-8')
capture = json.loads((ROOT / 'capture.json').read_text())
c00_manifest = json.loads((R / 'c00-original-manifest.json').read_text())
now_orig = manifest(ORIG)
out = {'changedFiles': rows, 'added': added, 'removed': removed,
       'onlyOwnedFilesChanged': set(changed) <= set(p00['ownedBaseline']) and not added and not removed,
       'delta': {'path': 'delta-vs-captured-source.diff', 'sha256': hashlib.sha256(diff.encode()).hexdigest(), 'lines': diff.count('\n'),
                 'equalsCarriedOriginalDelta': diff.encode() == (BASE / 'carried/delta-vs-captured-source.diff').read_bytes()},
       'treeEqualsOriginalAuthoredSource': manifest(ORIG / 'work/source')['files'] == current,
       'rootInputsUnchanged': all(sha(ROOT / n) == h for n, h in p00['rootInputs'].items()),
       'rootCapturedSourceStillCapture': all(sha(ROOT / 'source' / f['path']) == f['sha256'] for f in capture['files']),
       'originalRuntimeUnchangedSinceCarry': now_orig == c00_manifest,
       'originalRuntimeDrift': sorted(set(now_orig['files'].items()) ^ set(c00_manifest['files'].items()))[:20]}
PRIOR = {'/tmp/opensip-design-corrections/claude-readset-package-boundary-author.v1/review.md': '7d73425deb2d6000268c91c83da13e9743f4996206b78811b31b1b76f1a33907',
         '/tmp/opensip-design-corrections/claude-readset-package-boundary-author.v1/review.json': '214655dc36f9ea0ca0bc53f07d210cfd763b05f61dde1c2feac87bd1dba5ca77',
         '/tmp/opensip-design-corrections/claude-readset-nesting-review.v1/review.md': 'd86b9980682ff37ec85acca143d1663d66db46e5ca622287e438c5e6add6b05e',
         '/tmp/opensip-design-corrections/claude-readset-nesting-review.v1/review.json': '308a729f22ee7f7503337055f44fab305d915fa950e455157475dfa38ee3da32'}
out['priorReviewsUnchanged'] = all(sha(Path(p)) == h for p, h in PRIOR.items())
carried = {r['to'].split('/')[-1] for r in json.loads((R / 'c00-carry.json').read_text())['receipts']}
out['commands'] = {p.name: {k: json.loads(p.read_text())[k] for k in ('args', 'started', 'finished', 'exit')} | {'execution': 'original (carried)' if p.name in carried else 'continuation'}
                   for p in sorted(R.glob('*.receipt.json'))}
out['receiptDigests'] = {p.name: sha(p) for p in sorted(R.iterdir()) if p.is_file()}
if final:
    json.loads((BASE / 'review.json').read_text())
    out['review'] = {n: sha(BASE / n) for n in ('review.md', 'review.json')}
(R / ('c05-summary.final.json' if final else 'c05-summary.json')).write_text(json.dumps(out, indent=1) + '\n')
print(json.dumps({k: v for k, v in out.items() if k != 'receiptDigests'}, indent=1))
ok = all(out[k] for k in ('onlyOwnedFilesChanged', 'treeEqualsOriginalAuthoredSource', 'rootInputsUnchanged', 'rootCapturedSourceStillCapture',
                          'originalRuntimeUnchangedSinceCarry', 'priorReviewsUnchanged')) and out['delta']['equalsCarriedOriginalDelta']
sys.exit(0 if ok else 1)
