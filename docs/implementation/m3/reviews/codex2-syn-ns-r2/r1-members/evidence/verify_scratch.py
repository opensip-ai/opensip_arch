"""Scratch-only: run the product's real verify_design over a lock that appends this unit (SYN-1, SYN-1F or
SYN-NS, from the directory this file sits in), with a synthetic review and assent held in memory
(SCRATCH-<UNIT>/ paths). Nothing is written to either repository. It proves only that everything except the
missing independent review and root assent passes.

Usage: verify_scratch.py [PRODUCT_CHECKOUT] [--rev REV] [--chain]
- Without --rev, the checkout's own tools/verify_design.py and design-lock.json are used, with the checkout as
  the implementation (generation and admission sources are checked).
- With --rev (for example 15c0779), both files are read from that commit with read-only git plumbing, and
  verify runs design-only.
- With --chain, SYN-1, SYN-1F and SYN-NS are appended in that order (each whose subject manifest exists),
  which is the binding order the units propose; without it, only this unit is appended.
- SYN-1F names CRC-1 (M3-C's closure-role successor, in review) as a parent and carries its overrides, so
  whenever SYN-1F is appended, CRC-1 is appended immediately before it, with its own synthetic review and
  assent, unless the lock already binds it.

It asserts that the lock passes; that the selected inventory and the inheritance projection are unchanged; that
each appended record is selected with its own override count and no supersession; and that no successor bound
before it overrides any (parent, selector) pair it overrides."""
import copy, hashlib, importlib.util, json, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
A = HERE.parents[5]
BASE = 'docs/implementation/m3/syntax-e/'
ORDER = ['syn-1', 'syn-1f', 'syn-ns']
ME = HERE.parent.name
assert ME in ORDER, ME

args = list(sys.argv[1:])
rev = None
chain = '--chain' in args
if chain:
    args.remove('--chain')
if '--rev' in args:
    i = args.index('--rev')
    rev = args[i + 1]
    del args[i:i + 2]
W = Path(args[0] if args else '/Users/sb/code/opensip-ai/opensip')


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


PREREQ = {'syn-1f': ('crc-1', 'docs/implementation/m3/snapshot-plan-c/crc-1-subject.json',
                     'docs/implementation/m3/snapshot-plan-c/crc-1/successor.json')}
units = [u for u in ORDER if (chain or u == ME) and (A / BASE / f'{u}-subject.json').exists()]
assert ME in units
bound_records = {b['record']['path'] for b in base_lock['contractSuccessors']}
plan = []
for unit in units:
    if unit in PREREQ and PREREQ[unit][2] not in bound_records:
        plan.append(PREREQ[unit])
    plan.append((unit, BASE + f'{unit}-subject.json', BASE + f'{unit}/successor.json'))
synthetic, bindings = {}, []
for unit, subject_path, record_path in plan:
    subject, record = pin(subject_path), pin(record_path)
    review = json.dumps({'verdict': 'ACCEPT-DESIGN-UNIT', 'requiredFindings': [],
                         'subjectManifestSha256': subject['sha256']}).encode()
    tag = 'SCRATCH-' + unit.upper()
    rpin = pin_bytes(f'{tag}/review.json', review)
    assent = json.dumps({'status': 'ACCEPTED-DESIGN-UNIT', 'rootSubstantiveAssent': True, 'requiredUnitFindings': [],
                         'subjectManifest': subject, 'independentReview': rpin, 'acceptedSuccessor': record}).encode()
    apin = pin_bytes(f'{tag}/assent.json', assent)
    synthetic[rpin['path']], synthetic[apin['path']] = review, assent
    bindings.append((unit, {'record': record, 'subjectManifest': subject, 'review': rpin, 'assent': apin}))
real = m.pinned_bytes


def pinned_bytes(root, row):
    if isinstance(row, dict) and row.get('path') in synthetic:
        raw = synthetic[row['path']]
        assert hashlib.sha256(raw).hexdigest() == row['sha256']
        return raw
    return real(root, row)


m.pinned_bytes = pinned_bytes
for unit, binding in bindings:
    mine = json.loads((A / binding['record']['path']).read_bytes())
    assert 'passageSupersessions' not in mine, unit
    keys = {(o['parent']['path'], json.dumps(o['selector'], sort_keys=True)) for o in mine['passageOverrides']}
    for other in base_lock['contractSuccessors']:
        rec = json.loads(m.pinned_bytes(A, other['record']))
        for entry in rec.get('passageOverrides', []) + rec.get('passageSupersessions', []):
            assert (entry['parent']['path'], json.dumps(entry['selector'], sort_keys=True)) not in keys, \
                (unit, other['record']['path'])
base = m.verify(A, base_lock, implementation)
lock = copy.deepcopy(base_lock)
lock['contractSuccessors'].extend(b for _, b in bindings)
result = m.verify(A, lock, implementation)
assert base['passed'] is True and result['passed'] is True
assert result['selectedInventory'] == base['selectedInventory']
assert result['inventoryPassageInheritance'] == base['inventoryPassageInheritance']
appended = result['contractSuccessors'][-len(bindings):]
report = {}
for (unit, binding), got in zip(bindings, appended):
    mine = json.loads((A / binding['record']['path']).read_bytes())
    assert got['selected'] == binding['record']['path']
    assert len(got['passageOverrides']) == len(mine['passageOverrides']) and got['passageSupersessions'] == []
    report[unit] = {'selected': got['selected'], 'record': binding['record'], 'subject': binding['subjectManifest'],
                    'passageOverrides': len(got['passageOverrides']), 'candidates': len(got['inputs'])}
print(json.dumps({'mode': 'rev ' + rev if rev else 'checkout ' + str(W), 'passed': True,
                  'baseContractSuccessors': len(base['contractSuccessors']),
                  'contractSuccessors': len(result['contractSuccessors']), 'units': report,
                  'generationSources': result.get('generationSources'),
                  'admissionSources': result.get('admissionSources')}, indent=1))
