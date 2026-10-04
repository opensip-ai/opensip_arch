"""Scratch-only: run the product's real verify_design over a lock that appends FA-2 and then RUST3-LIM, with
synthetic reviews and assents held in memory (SCRATCH-FA-2/ and SCRATCH-RUST3-LIM/ paths). Nothing is written to
either repository. It proves only that everything except the missing independent reviews and root assents passes.

Usage: verify_scratch.py [PRODUCT_CHECKOUT] [--rev REV]
- Without --rev, the checkout's own tools/verify_design.py and design-lock.json are used, with the checkout as the
  implementation (generation and admission sources are checked).
- With --rev (for example cd5958b), both files are read from that commit with read-only git plumbing and verify
  runs design-only.

It asserts that:
- the base lock passes;
- RUST3-LIM alone on the base lock is refused, because its handshake parents are FA-2's candidates (so it binds
  after FA-2);
- the lock with FA-2 appended passes, and the lock with FA-2 then RUST3-LIM appended passes;
- the selected inventory and the inheritance projection are unchanged;
- RUST3-LIM has six passage overrides and no supersessions;
- no bound successor, FA-2 included, already overrides any of RUST3-LIM's (parent, selector) pairs."""
import copy, hashlib, importlib.util, json, subprocess, sys
from pathlib import Path

args = list(sys.argv[1:])
rev = None
if '--rev' in args:
    i = args.index('--rev')
    rev = args[i + 1]
    del args[i:i + 2]
W = Path(args[0] if args else '/Users/sb/code/opensip-ai/opensip')
A = Path(__file__).resolve().parents[6]
B = 'docs/implementation/m3/native-successors-fa/'


def git_show(path):
    return subprocess.run(['git', '-C', str(W), 'show', '%s:%s' % (rev, path)], check=True,
                          capture_output=True).stdout


if rev:
    spec = importlib.util.spec_from_loader('vd', loader=None)
    m = importlib.util.module_from_spec(spec)
    exec(compile(git_show('tools/verify_design.py'), 'verify_design.py@' + rev, 'exec'), m.__dict__)
    base_lock = json.loads(git_show('design-lock.json'))
    implementation = None
else:
    spec = importlib.util.spec_from_file_location('vd', W / 'tools/verify_design.py')
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    base_lock = json.loads((W / 'design-lock.json').read_text())
    implementation = W


def pin_bytes(path, b):
    return {'path': path, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}


def pin(p):
    return pin_bytes(p, (A / p).read_bytes())


synthetic = {}


def binding(tag, subject_path, record_path):
    subject, record = pin(subject_path), pin(record_path)
    review = json.dumps({'verdict': 'ACCEPT-DESIGN-UNIT', 'requiredFindings': [],
                         'subjectManifestSha256': subject['sha256']}).encode()
    rpin = pin_bytes(f'SCRATCH-{tag}/review.json', review)
    assent = json.dumps({'status': 'ACCEPTED-DESIGN-UNIT', 'rootSubstantiveAssent': True, 'requiredUnitFindings': [],
                         'subjectManifest': subject, 'independentReview': rpin, 'acceptedSuccessor': record}).encode()
    apin = pin_bytes(f'SCRATCH-{tag}/assent.json', assent)
    synthetic[rpin['path']] = review
    synthetic[apin['path']] = assent
    return {'record': record, 'subjectManifest': subject, 'review': rpin, 'assent': apin}


real = m.pinned_bytes


def pinned_bytes(root, row):
    if isinstance(row, dict) and row.get('path') in synthetic:
        raw = synthetic[row['path']]
        assert hashlib.sha256(raw).hexdigest() == row['sha256']
        return raw
    return real(root, row)


m.pinned_bytes = pinned_bytes
fa2 = binding('FA-2', B + 'fa-2-subject.json', B + 'fa-2/successor.json')
mine = binding('RUST3-LIM', B + 'rust3-lim-subject.json', B + 'rust3-lim/successor.json')
mine_record = json.loads((A / mine['record']['path']).read_bytes())
assert 'passageSupersessions' not in mine_record
keys = {(o['parent']['path'], json.dumps(o['selector'], sort_keys=True)) for o in mine_record['passageOverrides']}
for other in base_lock['contractSuccessors'] + [fa2]:
    rec = json.loads(m.pinned_bytes(A, other['record']))
    for entry in rec.get('passageOverrides', []) + rec.get('passageSupersessions', []):
        assert (entry['parent']['path'], json.dumps(entry['selector'], sort_keys=True)) not in keys, \
            other['record']['path']

base = m.verify(A, base_lock, implementation)
assert base['passed'] is True

alone = copy.deepcopy(base_lock)
alone['contractSuccessors'].append(mine)
try:
    m.verify(A, alone, implementation)
except m.DesignError as exc:
    alone_refusal = str(exc)
else:
    raise AssertionError('RUST3-LIM bound without FA-2 was not refused')
assert 'contract parent is not an accepted base' in alone_refusal, alone_refusal

with_fa2 = copy.deepcopy(base_lock)
with_fa2['contractSuccessors'].append(fa2)
after_fa2 = m.verify(A, with_fa2, implementation)
assert after_fa2['passed'] is True

lock = copy.deepcopy(with_fa2)
lock['contractSuccessors'].append(mine)
result = m.verify(A, lock, implementation)
ours = result['contractSuccessors'][-1]
assert result['passed'] is True and ours['selected'] == mine['record']['path']
assert result['selectedInventory'] == base['selectedInventory']
assert result['inventoryPassageInheritance'] == base['inventoryPassageInheritance']
assert len(ours['passageOverrides']) == 6 and ours['passageSupersessions'] == []
print(json.dumps({'mode': 'rev ' + rev if rev else 'checkout ' + str(W), 'passed': True,
                  'baseContractSuccessors': len(base['contractSuccessors']),
                  'rust3LimWithoutFa2': 'refused: ' + alone_refusal,
                  'withFa2ContractSuccessors': len(after_fa2['contractSuccessors']),
                  'contractSuccessors': len(result['contractSuccessors']),
                  'rust3-lim': {'selected': ours['selected'], 'passageOverrides': len(ours['passageOverrides']),
                                'passageSupersessions': 0, 'candidates': len(ours['inputs'])},
                  'generationSources': result.get('generationSources')}, indent=1))
