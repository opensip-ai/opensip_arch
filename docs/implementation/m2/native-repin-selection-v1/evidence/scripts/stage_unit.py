"""Stage native-repin-selection-v1 into an architecture checkout (creates new files only).

Copies the 8 regenerated scratch product files, the evidence and the scripts, then writes
materialization-map.json, successor.json and the subject manifest beside the unit.
Refuses if any target path already exists. Before pins come from product HEAD 0a3af77;
each parent is an already selected architecture path with those exact bytes.
"""
from pathlib import Path
import hashlib, json, shutil, subprocess, sys

ARCH = Path(sys.argv[1]).resolve()
NAME = 'native-repin-selection-v1'
REL = 'docs/implementation/m2/' + NAME
UNIT = ARCH / REL
SUBJECT = ARCH / 'docs/implementation/m2' / (NAME + '-subject.json')
BASE = Path('/Users/sb/opensip-deps/native-repin-01')
PRODUCT = BASE / 'product'
REPROBE = Path('/Users/sb/opensip-deps/confinement-reprobe-01')
REBUILD = Path('/Users/sb/opensip-deps/contracts-generator-rebuild-01')
PAD = Path('/Users/sb/opensip-deps/native-repin-01/evidence-inputs')
HEAD = '0a3af770903699d7672acc4a1f2ffa3c1cb82cd3'
FILES = ['apps/report/src/generated/report.ts', 'schemas/registry.json',
         'tools/contracts/build-receipt.json', 'tools/contracts/confinement-profile.json',
         'tools/contracts/generator-closure.json', 'tools/contracts/native-python-profile.json',
         'tools/contracts/python-profile.json', 'tools/contracts/toolchain.json']
PARENTS = {
    'tools/contracts/confinement-profile.json': 'docs/implementation/m1/generator-selection-v2/product/tools/contracts/confinement-profile.json',
    'tools/contracts/native-python-profile.json': 'docs/implementation/m1/generator-selection-v2/product/tools/contracts/native-python-profile.json',
    'tools/contracts/python-profile.json': 'docs/implementation/m1/generator-selection-v2/product/tools/contracts/python-profile.json',
}
for f in FILES:
    PARENTS.setdefault(f, 'docs/implementation/m2/initial-root-binding-owner-selection-v1/product/' + f)
if UNIT.exists() or SUBJECT.exists():
    sys.exit('refuse: unit already staged')


def pin(raw, path=None):
    row = {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}
    return {'path': path, **row} if path else row


def dump(value):
    return (json.dumps(value, indent=2) + '\n').encode()


copies = {'README.md': BASE / 'unit-src/README.md'}
for f in FILES:
    copies['product/' + f] = PRODUCT / f
E = 'evidence/'
copies[E + 'sigequiv.json'] = PAD / 'sigequiv.json'
for s in ('sigequiv.py', 'getformula.py', 'checkpins.py'):
    copies[E + 'scripts/sigequiv/' + s] = PAD / s
for s in ('results.json', 'new-pins.json', 'repin-output.json'):
    copies[E + 'reprobe/' + s] = REPROBE / s
copies[E + 'reprobe/scratch-vs-real.diff'] = REPROBE / 'diffs/scratch-vs-real.diff'
for n in ('1', '2'):
    for ext in ('stdout', 'stderr'):
        copies[E + f'reprobe/runs/positive-{n}.{ext}'] = REPROBE / f'runs/positive-{n}.{ext}'
        copies[E + f'reprobe/runs/negative-{n}.{ext}'] = REPROBE / f'negative-{n}.{ext}'
    copies[E + f'reprobe/runs/positive-{n}-result.json'] = REPROBE / f'runs/positive-{n}/result.json'
    copies[E + f'reprobe/runs/positive-{n}-selection-result.json'] = REPROBE / f'runs/positive-{n}/selection-result.json'
    copies[E + f'reprobe/runs/bypass-log-{n}.json'] = REPROBE / f'runs/bypass-log-{n}.json'
    copies[E + f'reprobe/runs/negative-{n}-results.json'] = REPROBE / f'negative-{n}/results.json'
for s in ('compare.py', 'probe.cjs', 'repin.py', 'run_confined.py', 'run_generation.py'):
    copies[E + 'reprobe/scripts/' + s] = REPROBE / 'scripts' / s
for s in ('system.sb.diff', 'dyld-support.sb.diff'):
    copies[E + 'sbdiff/' + s] = REPROBE / 'sbdiff' / s
for s in ('receipt.json', 'build.stdout.jsonl', 'build.stderr.log'):
    copies[E + 'generator-rebuild/' + s] = REBUILD / s
G = BASE / 'runs'
copies[E + 'generation/apply-pins.json'] = BASE / 'logs/apply-pins.json'
for run in ('write-1', 'check-1', 'check-2'):
    copies[E + f'generation/{run}.stdout'] = G / f'{run}.stdout'
    copies[E + f'generation/{run}.stderr'] = G / f'{run}.stderr'
    copies[E + f'generation/{run}-selection-result.json'] = G / run / 'selection-result.json'
    copies[E + f'generation/{run}-result.json'] = G / run / 'result.json'
    copies[E + f'generation/bypass-log-{run}.json'] = G / f'bypass-log-{run}.json'
copies[E + 'generation/product.diff'] = BASE / 'logs/product.diff'
for s in ('apply_pins.py', 'run_generation_b2.py', 'stage_unit.py', 'accepted_map.py'):
    copies[E + 'scripts/' + s] = BASE / 'scripts' / s
copies[E + 'scripts/accepted_map.py'] = BASE / 'accepted_map.py'

# Before pins from product HEAD; parents must carry exactly those bytes.
maps, parents = [], []
for f in FILES:
    before = subprocess.run(['git', '-C', str(PRODUCT), 'show', f'{HEAD}:{f}'], check=True, capture_output=True).stdout
    parent_raw = (ARCH / PARENTS[f]).read_bytes()
    assert parent_raw == before, f
    maps.append({'productPath': f, 'candidatePath': f'{REL}/product/{f}', 'before': pin(before), 'after': pin((PRODUCT / f).read_bytes())})
    parents.append(pin(parent_raw, PARENTS[f]))
parents.sort(key=lambda r: r['path'])

UNIT.mkdir(parents=True)
written = {}
for rel, src in sorted(copies.items()):
    target = UNIT / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    raw = Path(src).read_bytes()
    target.write_bytes(raw)
    written[rel] = raw
written['materialization-map.json'] = dump({
    'schemaVersion': 1,
    'standing': 'Exact prospective development materialization; independent review, root assent and a fresh no-bypass generation drift check are required before selection.',
    'baseProductHead': HEAD, 'files': maps})
(UNIT / 'materialization-map.json').write_bytes(written['materialization-map.json'])
candidates = sorted((pin(raw, f'{REL}/{rel}') for rel, raw in written.items()), key=lambda r: r['path'])
successor = dump({
    'schemaVersion': 1,
    'standing': 'PROPOSED macOS 27 native host re-pin of the contracts generator closure (same pinned tool versions; OS re-signing and OS-owned files only) with regenerated report.ts provenance; exact frozen candidate requires actual independent review and root assent.',
    'parents': parents, 'passageOverrides': [], 'candidates': candidates})
(UNIT / 'successor.json').write_bytes(successor)
record = pin(successor, f'{REL}/successor.json')
subject = dump({'schemaVersion': 1, 'files': sorted([*candidates, record], key=lambda r: r['path'])})
SUBJECT.write_bytes(subject)
print(json.dumps({'unit': str(UNIT), 'candidates': len(candidates), 'parents': len(parents),
                  'record': record, 'subject': pin(subject, str(SUBJECT.relative_to(ARCH)))}, indent=2))
