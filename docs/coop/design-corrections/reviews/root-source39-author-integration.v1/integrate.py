"""Guarded author integration into a mutable successor only; no acceptance or LIVE activation."""
from pathlib import Path
import hashlib, json, subprocess

RT = Path('/tmp/opensip-design-corrections')
OUT = Path(__file__).parent
BASE = RT / 'candidate-subject.v38'
DEST = RT / 'consumer24-corrections-successor.v1/source'
HOST = RT / 'claude-source38-advisory-author.v2'
NATIVE = RT / 'claude-consumer24-native-author.v2'
sha = lambda b: hashlib.sha256(b).hexdigest()
host = json.loads((HOST / 'review.json').read_bytes())['hashMap']
native = json.loads((NATIVE / 'output/changed-files.v1.json').read_bytes())['files']
assert not (OUT / 'integration.json').exists()
pending = {}
inputs = []
for row in host:
    path = row['path']
    before = (BASE / path).read_bytes()
    after = (HOST / 'work/edited' / path).read_bytes()
    assert sha(before) == row['source38'] and sha(after) == row['v2']
    assert (DEST / path).read_bytes() == before, path
    pending[path] = after
    inputs.append({'author':'host-v2', 'path':path, 'sha256':sha(after)})
for row in native:
    path = row['path']
    after = (NATIVE / 'source' / path).read_bytes()
    assert sha(after) == row['sha256'] and len(after) == row['bytes']
    if row['status'] == 'added':
        assert not (BASE / path).exists() and not (DEST / path).exists()
    else:
        before = (BASE / path).read_bytes()
        assert sha(before) == row['parentSha256']
        assert (DEST / path).read_bytes() == before, path
    inputs.append({'author':'native-v2', 'path':path, 'sha256':sha(after)})
    if path in pending:
        assert path.endswith('/run-termination-goldens.v1.json'), path
        merge = OUT / 'merge-inputs'
        merge.mkdir(exist_ok=True)
        (merge / 'host.json').write_bytes(pending[path])
        (merge / 'base.json').write_bytes(before)
        (merge / 'native.json').write_bytes(after)
        proc = subprocess.run(['git','merge-file','-p',str(merge/'host.json'),str(merge/'base.json'),str(merge/'native.json')],capture_output=True)
        (merge / 'stderr.txt').write_bytes(proc.stderr)
        assert proc.returncode == 0, proc.stderr
        json.loads(proc.stdout)
        pending[path] = proc.stdout
    else:
        pending[path] = after

rows = []
for path, after in pending.items():
    p = DEST / path
    before = p.read_bytes() if p.exists() else None
    if before is not None:
        backup = OUT / 'before' / path
        backup.parent.mkdir(parents=True, exist_ok=True)
        backup.write_bytes(before)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(after)
    assert p.read_bytes() == after
    rows.append({'path':path, 'beforeSha256':sha(before) if before is not None else None,
                 'sha256':sha(after), 'bytes':len(after)})
report = {'standing':'Mutable successor integration of completed actual Claude author batches. Not source acceptance, freeze, readiness or LIVE application.',
          'destination':str(DEST), 'inputs':inputs, 'files':rows,
          'rootClosureClarificationPreserved':True,
          'pending':['root cross-owner prose alignment','combined focused checks','workflow v2 batch','pins and planning','global checks','package rebuild','fresh source and blind reviews','application review']}
(OUT/'integration.json').write_text(json.dumps(report,indent=2)+'\n')
print('Integrated',len(rows),'paths; one conflict-free three-way golden merge. No acceptance.')
