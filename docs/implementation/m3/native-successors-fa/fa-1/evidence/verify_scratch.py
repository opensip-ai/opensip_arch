"""Scratch-only feasibility proof for FA-1 with the product's real verify_design. Synthetic reviews,
assents and probe records are held in memory under SCRATCH-* paths; nothing is written to either
repository. It proves only that everything except the missing independent review and root assent passes.

Usage: verify_scratch.py [PRODUCT_CHECKOUT] [--rev REV]
- Without --rev, the checkout's own tools/verify_design.py and design-lock.json are used, with the checkout
  as the implementation (generation and admission sources are checked).
- With --rev (for example cd5958b), both files are read from that commit with read-only git plumbing and
  verify runs design-only.

Runs:
1. FA-1 appended to the lock: must PASS, with exactly 3 passage overrides and no supersession, the selected
   inventory and the inheritance projection unchanged, and one more contract successor. No bound successor
   overrides any (parent, selector) pair FA-1 uses.
2. Binding order with FA-2 (in review with Codex): FA-2 then FA-1, and FA-1 then FA-2, must both PASS.
   Skipped, and reported, if FA-2's subject members do not verify at their pins.
3. Binding order with SD-5 (drafted beside FA-1; NE:3540): both orders must PASS. Skipped if absent.
4. Probe: after FA-1, a later record overriding NE:3849 again must REFUSE with
   "conflicting contract passage overrides"; the lines are FA-1's from then on."""
import copy, hashlib, importlib.util, json, subprocess, sys
from pathlib import Path

args = list(sys.argv[1:])
rev = None
if '--rev' in args:
    i = args.index('--rev')
    rev = args[i + 1]
    del args[i:i + 2]
W = Path(args[0] if args else '/Users/sb/code/opensip-ai/opensip')
A = Path('/Users/sb/code/opensip-ai/opensip_arch')
B = 'docs/implementation/m3/native-successors-fa/'
NE = 'docs/v2/contracts/product-v1/native-evidence.md'
OTHERS = {'FA-2': (B + 'fa-2/successor.json', B + 'fa-2-subject.json'),
          'SD-5': ('docs/implementation/m3/supervisor-d/sd-5/successor.json',
                   'docs/implementation/m3/supervisor-d/sd-5-subject.json')}


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
real = m.pinned_bytes


def pinned_bytes(root, row):
    if isinstance(row, dict) and row.get('path') in synthetic:
        raw = synthetic[row['path']]
        assert hashlib.sha256(raw).hexdigest() == row['sha256']
        return raw
    return real(root, row)


m.pinned_bytes = pinned_bytes


def serve(path, raw):
    synthetic[path] = raw
    return pin_bytes(path, raw)


def binding(record_pin, subject_pin, tag):
    review = json.dumps({'verdict': 'ACCEPT-DESIGN-UNIT', 'requiredFindings': [],
                         'subjectManifestSha256': subject_pin['sha256']}).encode()
    rpin = serve('SCRATCH-%s/review.json' % tag, review)
    assent = json.dumps({'status': 'ACCEPTED-DESIGN-UNIT', 'rootSubstantiveAssent': True, 'requiredUnitFindings': [],
                         'subjectManifest': subject_pin, 'independentReview': rpin,
                         'acceptedSuccessor': record_pin}).encode()
    apin = serve('SCRATCH-%s/assent.json' % tag, assent)
    return {'record': record_pin, 'subjectManifest': subject_pin, 'review': rpin, 'assent': apin}


def run(lock):
    try:
        return 'PASS', m.verify(A, lock, implementation)
    except m.DesignError as exc:
        return 'REFUSED: ' + str(exc), None


def subject_verifies(subject_path):
    try:
        subject = json.loads((A / subject_path).read_bytes())
        return all(pin(r['path']) == r for r in subject['files'])
    except (OSError, ValueError, KeyError):
        return False


base_status, base = run(base_lock)
assert base_status == 'PASS', base_status
out = {'mode': 'rev ' + rev if rev else 'checkout ' + str(W), 'baseContractSuccessors': len(base['contractSuccessors'])}

# 1. FA-1 appended.
record_pin, subject_pin = pin(B + 'fa-1/successor.json'), pin(B + 'fa-1-subject.json')
mine_record = json.loads((A / B / 'fa-1/successor.json').read_bytes())
assert 'passageSupersessions' not in mine_record
keys = {(o['parent']['path'], json.dumps(o['selector'], sort_keys=True)) for o in mine_record['passageOverrides']}
for other in base_lock['contractSuccessors']:
    rec = json.loads(m.pinned_bytes(A, other['record']))
    for entry in rec.get('passageOverrides', []) + rec.get('passageSupersessions', []):
        assert (entry['parent']['path'], json.dumps(entry['selector'], sort_keys=True)) not in keys, \
            other['record']['path']
fa1 = binding(record_pin, subject_pin, 'FA-1')
with_fa1 = copy.deepcopy(base_lock)
with_fa1['contractSuccessors'].append(fa1)
status, result = run(with_fa1)
assert status == 'PASS', status
mine = result['contractSuccessors'][-1]
assert mine['selected'] == record_pin['path'] and mine['passageSupersessions'] == []
assert [o['selector']['line'] for o in mine['passageOverrides']] == [3529, 3849, 3850]
assert result['selectedInventory'] == base['selectedInventory']
assert result['inventoryPassageInheritance'] == base['inventoryPassageInheritance']
out['fa-1'] = {'status': status, 'contractSuccessors': len(result['contractSuccessors']),
               'passageOverrides': len(mine['passageOverrides']), 'passageSupersessions': 0,
               'candidates': len(mine['inputs']), 'generationSources': result.get('generationSources')}

# 2 and 3. binding order with the other drafts.
orders = {}
for tag, (rec_path, subj_path) in OTHERS.items():
    if not (A / rec_path).exists() or not subject_verifies(subj_path):
        orders[tag] = 'SKIPPED: subject absent or not at its pins'
        continue
    other = binding(pin(rec_path), pin(subj_path), tag)
    results = {}
    for name, seq in (('%s-then-FA-1' % tag, [other, fa1]), ('FA-1-then-%s' % tag, [fa1, other])):
        lock = copy.deepcopy(base_lock)
        lock['contractSuccessors'].extend(seq)
        st, res = run(lock)
        assert st == 'PASS', (name, st)
        results[name] = '%s (%d)' % (st, len(res['contractSuccessors']))
    orders[tag] = results
out['bindingOrder'] = orders

# 4. a later conflicting override of NE:3849 refuses.
ne = pin(NE)
line = (A / NE).read_bytes().decode('utf-8').splitlines()[3848]
note = serve('SCRATCH-LATER/README.md', b'probe\n')
probe = {'schemaVersion': 1, 'standing': 'scratch probe', 'parents': [ne],
         'passageOverrides': [{'parent': ne, 'selector': {'line': 3849}, 'before': line, 'after': line + ' (probe)'}],
         'candidates': [note]}
ppin = serve('SCRATCH-LATER/successor.json', (json.dumps(probe, indent=2) + '\n').encode())
spin = serve('SCRATCH-LATER/subject.json', (json.dumps(
    {'schemaVersion': 1, 'files': sorted([note, ppin], key=lambda r: r['path'])}, indent=2) + '\n').encode())
lock = copy.deepcopy(with_fa1)
lock['contractSuccessors'].append(binding(ppin, spin, 'LATER'))
out['laterOverrideOfNE3849'] = run(lock)[0]
assert out['laterOverrideOfNE3849'] == 'REFUSED: conflicting contract passage overrides'
print(json.dumps(out, indent=1))
