"""p00: captured input custody and a regular copy.

- root probe inputs (probe.py, report.json, capture.json, checker stdout/stderr) hashed;
- root captured source verified against capture.json (every path, sha256, bytes; no extra files, no symlinks) and against
  the report's before/after hashes of the three probed files;
- regular per-file copy into work/source (no hardlinks: distinct inodes, st_nlink 1, byte-equal), refusing an existing tree;
- baseline hashes of the copy (receipts/baseline-file-hashes.json) and of the owned files.
Output: receipts/p00-copy.json.
"""
import hashlib, json, os, shutil, sys
from pathlib import Path

BASE = Path('/tmp/opensip-design-corrections/claude-repair-join-author.v1')
ROOT = Path('/tmp/opensip-design-corrections/root-repair-owner-probe.v2')
SRC = ROOT / 'source'
W = BASE / 'work' / 'source'
R = BASE / 'receipts'
R.mkdir(exist_ok=True)
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
OWNED = ['docs/coop/design-corrections/workflows/workflows_model.v3.py',
         'docs/coop/design-corrections/workflows/repair_closed_world_selection.v1.py',
         'docs/coop/design-corrections/workflows/check-workflow-projection.v3.py',
         'docs/coop/design-corrections/workflows/workflow-projection-contract.v3.md',
         'docs/v2/contracts/product-v1/workflows-and-surfaces.md']
out = {'rootInputs': {n: sha(ROOT / n) for n in ('probe.py', 'report.json', 'capture.json', 'checker-stdout.json', 'checker-stderr.txt')}}
capture = json.loads((ROOT / 'capture.json').read_text())
report = json.loads((ROOT / 'report.json').read_text())
listed = {f['path']: f for f in capture['files']}
walk, links = [], []
for dirpath, dirnames, filenames in os.walk(SRC, followlinks=False):
    for name in dirnames + filenames:
        p = Path(dirpath) / name
        if p.is_symlink(): links.append(str(p.relative_to(SRC)))
    walk += [str((Path(dirpath) / f).relative_to(SRC)) for f in filenames]
mism = [p for p in listed if not (SRC / p).is_file() or sha(SRC / p) != listed[p]['sha256'] or (SRC / p).stat().st_size != listed[p]['bytes']]
out['capture'] = {'captureOrigin': capture['source'], 'listed': len(listed), 'walked': len(walk), 'symlinks': links,
                  'extra': sorted(set(walk) - set(listed)), 'missingOrMismatched': mism}
out['reportProbedFiles'] = {k: {'before': v, 'after': report['after'][k], 'now': sha(Path(k))} for k, v in report['before'].items()}
out['reportStable'] = all(r['before'] == r['after'] == r['now'] for r in out['reportProbedFiles'].values())
ok_capture = not links and not out['capture']['extra'] and not mism and len(walk) == len(listed)
if W.exists():
    print('work/source exists; refusing to overwrite'); sys.exit(2)
if not (ok_capture and out['reportStable']):
    (R / 'p00-copy.json').write_text(json.dumps(out, indent=1) + '\n'); print(json.dumps(out, indent=1)[:4000]); sys.exit(1)
for rel in sorted(walk):
    dst = W / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SRC / rel, dst)
bad = []
for rel in sorted(walk):
    a, b = (SRC / rel).stat(), (W / rel).stat()
    if a.st_ino == b.st_ino or b.st_nlink != 1 or (SRC / rel).read_bytes() != (W / rel).read_bytes(): bad.append(rel)
copied = sum(1 for _, _, fs in os.walk(W) for _ in fs)
out['copy'] = {'files': copied, 'bad': bad, 'ok': not bad and copied == len(walk)}
baseline = {rel: listed[rel]['sha256'] for rel in sorted(walk)}
(R / 'baseline-file-hashes.json').write_text(json.dumps(baseline, indent=1) + '\n')
out['ownedBaseline'] = {rel: baseline.get(rel) for rel in OWNED}
(R / 'p00-copy.json').write_text(json.dumps(out, indent=1) + '\n')
print(json.dumps(out, indent=1))
sys.exit(0 if out['copy']['ok'] else 1)
