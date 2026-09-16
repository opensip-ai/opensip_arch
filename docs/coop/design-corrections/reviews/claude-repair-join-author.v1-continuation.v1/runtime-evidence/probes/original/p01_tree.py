"""p01 <name> [owned-from=baseline|source]: make a disposable regular tree work/<name> from the baseline hashes.

Every file is copied from work/source when its bytes equal the captured baseline hash, otherwise from the root captured
source (whose bytes p00 verified against capture.json). With 'hybrid-checker', the edited checker is then copied from
work/source, so the tree is baseline owner files + edited checker. Refuses an existing target. Regular files only
(distinct inodes, st_nlink 1). Output: receipts/p01-<name>.json with every owned-file hash.
"""
import hashlib, json, os, shutil, sys
from pathlib import Path

BASE = Path('/tmp/opensip-design-corrections/claude-repair-join-author.v1')
ROOT_SRC = Path('/tmp/opensip-design-corrections/root-repair-owner-probe.v2/source')
W = BASE / 'work' / 'source'
R = BASE / 'receipts'
name = sys.argv[1]
mode = sys.argv[2] if len(sys.argv) > 2 else 'baseline'
T = BASE / 'work' / name
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
baseline = json.loads((R / 'baseline-file-hashes.json').read_text())
p00 = json.loads((R / 'p00-copy.json').read_text())
CHECKER = 'docs/coop/design-corrections/workflows/check-workflow-projection.v3.py'
if T.exists():
    print('target exists; refusing'); sys.exit(2)
bad = []
for rel, h in sorted(baseline.items()):
    src = W / rel if sha(W / rel) == h else ROOT_SRC / rel
    if sha(src) != h: bad.append(rel); continue
    (T / rel).parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, T / rel)
if mode == 'hybrid-checker':
    shutil.copyfile(W / CHECKER, T / CHECKER)
for rel in baseline:
    if (T / rel).stat().st_nlink != 1 or (T / rel).stat().st_ino in ((W / rel).stat().st_ino, (ROOT_SRC / rel).stat().st_ino): bad.append(rel)
files = sum(1 for _, _, fs in os.walk(T) for _ in fs)
out = {'tree': str(T), 'mode': mode, 'files': files, 'bad': bad,
       'owned': {rel: {'tree': sha(T / rel), 'baseline': h, 'source': sha(W / rel)} for rel, h in p00['ownedBaseline'].items()}}
out['ok'] = not bad and files == len(baseline)
(R / ('p01-%s.json' % name)).write_text(json.dumps(out, indent=1) + '\n')
print(json.dumps(out, indent=1))
sys.exit(0 if out['ok'] else 1)
