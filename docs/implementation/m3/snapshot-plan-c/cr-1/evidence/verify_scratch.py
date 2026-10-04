"""Scratch-only: run the product's real verify_design over a lock that appends CR-1, with a
synthetic review and assent held in memory (SCRATCH-CR-1/ paths). Nothing is written to either
repository. It proves only that everything except the missing independent review and root
assent passes.

Usage: verify_scratch.py [PRODUCT_CHECKOUT] [--rev REV] [--after-crc-1 | --before-crc-1]
- Without --rev, the checkout's own tools/verify_design.py and design-lock.json are used, with
  the checkout as the implementation (generation and admission sources are checked).
- With --rev (for example cd5958b), both files are read from that commit with read-only git
  plumbing and verify runs design-only.
- With --after-crc-1, CRC-1 (docs/implementation/m3/snapshot-plan-c/crc-1/) is appended first,
  also with a synthetic review and assent, and CR-1 after it. With --before-crc-1 (r2), CR-1 is
  appended first and CRC-1 after it. The two units bind together in either order because they
  share no parent.

It asserts that the base lock passes; that the lock with CR-1 appended passes; that the selected
inventory and the inheritance projection are unchanged; that the record has four passage
overrides (r2) and no supersession; and that no bound successor already overrides any of CR-1's
(parent, selector) pairs."""
import copy, hashlib, importlib.util, json, subprocess, sys
from pathlib import Path

args = list(sys.argv[1:])
rev = None
if '--rev' in args:
    i = args.index('--rev')
    rev = args[i + 1]
    del args[i:i + 2]
after_crc = '--after-crc-1' in args
before_crc = '--before-crc-1' in args
assert not (after_crc and before_crc)
args = [a for a in args if a not in ('--after-crc-1', '--before-crc-1')]
W = Path(args[0] if args else '/Users/sb/code/opensip-ai/opensip')
A = Path('/Users/sb/code/opensip-ai/opensip_arch')
M = 'docs/implementation/m3/snapshot-plan-c/'


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

synthetic = {}


def pin_bytes(path, b):
    return {'path': path, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}


def pin(p):
    return pin_bytes(p, (A / p).read_bytes())


def scratch(path, raw):
    synthetic[path] = raw
    return pin_bytes(path, raw)


def binding(name, subject, record):
    review = json.dumps({'verdict': 'ACCEPT-DESIGN-UNIT', 'requiredFindings': [],
                         'subjectManifestSha256': subject['sha256']}).encode()
    rpin = scratch('SCRATCH-%s/review.json' % name, review)
    assent = json.dumps({'status': 'ACCEPTED-DESIGN-UNIT', 'rootSubstantiveAssent': True, 'requiredUnitFindings': [],
                         'subjectManifest': subject, 'independentReview': rpin, 'acceptedSuccessor': record}).encode()
    apin = scratch('SCRATCH-%s/assent.json' % name, assent)
    return {'record': record, 'subjectManifest': subject, 'review': rpin, 'assent': apin}


real = m.pinned_bytes


def pinned_bytes(root, row):
    if isinstance(row, dict) and row.get('path') in synthetic:
        raw = synthetic[row['path']]
        assert hashlib.sha256(raw).hexdigest() == row['sha256']
        return raw
    return real(root, row)


m.pinned_bytes = pinned_bytes
mine_record = json.loads((A / M / 'cr-1/successor.json').read_bytes())
assert 'passageSupersessions' not in mine_record
keys = {(o['parent']['path'], json.dumps(o['selector'], sort_keys=True)) for o in mine_record['passageOverrides']}
for other in base_lock['contractSuccessors']:
    rec = json.loads(m.pinned_bytes(A, other['record']))
    for entry in rec.get('passageOverrides', []) + rec.get('passageSupersessions', []):
        assert (entry['parent']['path'], json.dumps(entry['selector'], sort_keys=True)) not in keys, \
            other['record']['path']
base = m.verify(A, base_lock, implementation)
lock = copy.deepcopy(base_lock)
if after_crc:
    lock['contractSuccessors'].append(binding('CRC-1', pin(M + 'crc-1-subject.json'), pin(M + 'crc-1/successor.json')))
lock['contractSuccessors'].append(binding('CR-1', pin(M + 'cr-1-subject.json'), pin(M + 'cr-1/successor.json')))
if before_crc:
    lock['contractSuccessors'].append(binding('CRC-1', pin(M + 'crc-1-subject.json'), pin(M + 'crc-1/successor.json')))
result = m.verify(A, lock, implementation)
mine = result['contractSuccessors'][-2 if before_crc else -1]
assert base['passed'] is True and result['passed'] is True and mine['selected'] == M + 'cr-1/successor.json'
assert result['selectedInventory'] == base['selectedInventory']
assert result['inventoryPassageInheritance'] == base['inventoryPassageInheritance']
assert len(mine['passageOverrides']) == 4 and mine['passageSupersessions'] == []
assert len(result['contractSuccessors']) == len(base['contractSuccessors']) + (2 if after_crc or before_crc else 1)
print(json.dumps({'mode': ('rev ' + rev if rev else 'checkout ' + str(W)) + (', after CRC-1' if after_crc else '')
                  + (', before CRC-1' if before_crc else ''),
                  'passed': True, 'baseContractSuccessors': len(base['contractSuccessors']),
                  'contractSuccessors': len(result['contractSuccessors']),
                  'cr-1': {'selected': mine['selected'], 'passageOverrides': len(mine['passageOverrides']),
                           'passageSupersessions': 0, 'candidates': len(mine['inputs'])},
                  'selectedInventory': result['selectedInventory']['path'],
                  'inventoryPassageInheritance': len(result['inventoryPassageInheritance']),
                  'generationSources': result.get('generationSources'),
                  'admissionSources': result.get('admissionSources')}, indent=1))
