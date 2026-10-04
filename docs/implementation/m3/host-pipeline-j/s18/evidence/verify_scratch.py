"""Scratch-only: run the product's real verify_design over a lock that appends S18, with a synthetic review and
assent held in memory (SCRATCH-S18/ paths). Nothing is written to either repository. It proves only that
everything except the missing independent review and root assent passes.

Usage: verify_scratch.py [PRODUCT_CHECKOUT] [--rev REV]
- Without --rev, the checkout's own tools/verify_design.py and design-lock.json are used, with the checkout as
  the implementation (generation and admission sources are checked).
- With --rev (for example 392499e, the r2 base), both files are read from that commit with read-only git plumbing and
  verify runs design-only.

It asserts that the base lock passes; that the lock with S18 appended passes and selects S18's record; that the
selected inventory and the inheritance projection are unchanged; that the record has ten passage overrides and
no supersession; and that no bound successor already overrides or supersedes any of S18's (parent, selector)
pairs. Probe: a second, conflicting override of WS line 231 appended after S18 is refused ("conflicting contract
passage overrides"), so a later unit cannot silently replace S18's meaning by a line selector."""
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
J = 'docs/implementation/m3/host-pipeline-j/'


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


def binding(prefix, subject, record):
    review = json.dumps({'verdict': 'ACCEPT-DESIGN-UNIT', 'requiredFindings': [],
                         'subjectManifestSha256': subject['sha256']}).encode()
    rpin = pin_bytes(prefix + '/review.json', review)
    assent = json.dumps({'status': 'ACCEPTED-DESIGN-UNIT', 'rootSubstantiveAssent': True, 'requiredUnitFindings': [],
                         'subjectManifest': subject, 'independentReview': rpin, 'acceptedSuccessor': record}).encode()
    apin = pin_bytes(prefix + '/assent.json', assent)
    synthetic[rpin['path']] = review
    synthetic[apin['path']] = assent
    return {'record': record, 'subjectManifest': subject, 'review': rpin, 'assent': apin}


subject, record = pin(J + 's18-subject.json'), pin(J + 's18/successor.json')
mine_record = json.loads((A / record['path']).read_bytes())
assert 'passageSupersessions' not in mine_record
keys = {(o['parent']['path'], json.dumps(o['selector'], sort_keys=True)) for o in mine_record['passageOverrides']}
for other in base_lock['contractSuccessors']:
    rec = json.loads(m.pinned_bytes(A, other['record']))
    for entry in rec.get('passageOverrides', []) + rec.get('passageSupersessions', []):
        assert (entry['parent']['path'], json.dumps(entry['selector'], sort_keys=True)) not in keys, \
            other['record']['path']
base = m.verify(A, base_lock, implementation)
lock = copy.deepcopy(base_lock)
lock['contractSuccessors'].append(binding('SCRATCH-S18', subject, record))
result = m.verify(A, lock, implementation)
mine = result['contractSuccessors'][-1]
assert base['passed'] is True and result['passed'] is True and mine['selected'] == record['path']
assert result['selectedInventory'] == base['selectedInventory']
assert result['inventoryPassageInheritance'] == base['inventoryPassageInheritance']
assert len(mine['passageOverrides']) == 10 and mine['passageSupersessions'] == []

# Probe: a later record that overrides WS line 231 with another meaning is refused.
ws_231 = next(o for o in mine_record['passageOverrides'] if o['selector'] == {'line': 231}
              and o['parent']['path'].endswith('product-v1/workflows-and-surfaces.md'))
probe_record = {'schemaVersion': 1, 'standing': 'SCRATCH probe', 'parents': [ws_231['parent']],
                'passageOverrides': [{**ws_231, 'after': ws_231['before'] + ' (probe)'}],
                'candidates': [{'path': 'SCRATCH-PROBE/README.md', 'bytes': 6,
                                'sha256': hashlib.sha256(b'probe\n').hexdigest()}]}
probe_bytes = (json.dumps(probe_record, indent=2) + '\n').encode()
probe_pin = pin_bytes('SCRATCH-PROBE/successor.json', probe_bytes)
synthetic[probe_pin['path']] = probe_bytes
synthetic['SCRATCH-PROBE/README.md'] = b'probe\n'
probe_subject_bytes = (json.dumps({'schemaVersion': 1, 'files': sorted(
    [probe_record['candidates'][0], probe_pin], key=lambda r: r['path'])}, indent=2) + '\n').encode()
probe_subject = pin_bytes('SCRATCH-PROBE/subject.json', probe_subject_bytes)
synthetic[probe_subject['path']] = probe_subject_bytes
probe_lock = copy.deepcopy(lock)
probe_lock['contractSuccessors'].append(binding('SCRATCH-PROBE', probe_subject, probe_pin))
try:
    m.verify(A, probe_lock, implementation)
    probe = 'PASSED (unexpected)'
except m.DesignError as error:
    probe = 'REFUSED: %s' % error
assert probe == 'REFUSED: conflicting contract passage overrides', probe

print(json.dumps({'mode': 'rev ' + rev if rev else 'checkout ' + str(W), 'passed': True,
                  'baseContractSuccessors': len(base['contractSuccessors']),
                  'contractSuccessors': len(result['contractSuccessors']),
                  's18': {'selected': mine['selected'], 'passageOverrides': len(mine['passageOverrides']),
                          'passageSupersessions': 0, 'candidates': len(mine['inputs'])},
                  'selectedInventory': result['selectedInventory']['path'],
                  'inventoryPassageInheritance': len(result['inventoryPassageInheritance']),
                  'conflictingLaterOverrideProbe': probe,
                  'generationSources': result.get('generationSources')}, indent=1))
