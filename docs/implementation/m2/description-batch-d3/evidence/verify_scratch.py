"""Scratch-only: run the product checkout's real verify_design over a lock that binds D3,
with a synthetic review and assent held in memory (SCRATCH-D3/ paths). Nothing is written to
either repository. This proves only that everything except the missing independent review
and root assent passes.

Two modes, chosen by the checkout's lock:
- the lock does not bind D3 (product main): the binding is appended in memory, as D1's and
  D2's scripts did;
- the lock's last contract successor is D3 (the uncommitted opensip-d3 worktree): its record
  and subject pins must equal this tree's bytes, and its review and assent pins must be the
  SCRATCH-D3 placeholders, which only this overlay serves. Plain verify_design refuses that
  lock until the lead replaces the two placeholders with the real review and unit pins.

It asserts that the lock passes; that the selected inventory and the inheritance projection
are those of the same lock without D3 (D3's entries are on the final inventory, so they are
checked, not projected); that supersessions grow by exactly D3's count; that every entry's
parent is the selected inventory; and that each before is the row's current text: the raw
description for an override, the inheritance entry's after for a supersession."""
import copy, hashlib, importlib.util, json, sys
from pathlib import Path
W = Path(sys.argv[1] if len(sys.argv) > 1 else '/Users/sb/code/opensip-ai/opensip')
A = Path('/Users/sb/code/opensip-ai/opensip_arch')
spec = importlib.util.spec_from_file_location('vd', W / 'tools/verify_design.py'); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
D = 'docs/implementation/m2/description-batch-d3'
def pin(p): b = (A / p).read_bytes(); return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
subject, record = pin(D + '-subject.json'), pin(D + '/successor.json')
review = json.dumps({'verdict': 'ACCEPT-DESIGN-UNIT', 'requiredFindings': [], 'subjectManifestSha256': subject['sha256']}).encode()
rpin = {'path': 'SCRATCH-D3/review.json', 'bytes': len(review), 'sha256': hashlib.sha256(review).hexdigest()}
assent = json.dumps({'status': 'ACCEPTED-DESIGN-UNIT', 'rootSubstantiveAssent': True, 'requiredUnitFindings': [], 'subjectManifest': subject, 'independentReview': rpin, 'acceptedSuccessor': record}).encode()
apin = {'path': 'SCRATCH-D3/assent.json', 'bytes': len(assent), 'sha256': hashlib.sha256(assent).hexdigest()}
synthetic = {rpin['path']: review, apin['path']: assent}
real = m.pinned_bytes
def pinned_bytes(root, row):
    if isinstance(row, dict) and row.get('path') in synthetic:
        raw = synthetic[row['path']]; assert hashlib.sha256(raw).hexdigest() == row['sha256']; return raw
    return real(root, row)
m.pinned_bytes = pinned_bytes
binding = {'record': record, 'subjectManifest': subject, 'review': rpin, 'assent': apin}
lock = json.loads((W / 'design-lock.json').read_text())
if lock['contractSuccessors'][-1]['record']['path'] == record['path']:
    mode = 'bound'
    assert lock['contractSuccessors'][-1] == binding, 'the bound D3 entry differs from this tree or its placeholders'
    without = copy.deepcopy(lock); without['contractSuccessors'].pop()
else:
    mode = 'appended'
    without = copy.deepcopy(lock); lock['contractSuccessors'].append(binding)
assert all(b['record']['path'] != record['path'] for b in without['contractSuccessors'])
base = m.verify(A, without, W)
result = m.verify(A, lock, W)
mine = result['contractSuccessors'][-1]
assert base['passed'] is True and result['passed'] is True
assert mine['selected'] == record['path']
assert result['selectedInventory'] == base['selectedInventory'] == without['inventorySuccessors'][-1]['candidate']
assert result['inventoryPassageInheritance'] == base['inventoryPassageInheritance'] == without['inventoryPassageInheritance']
assert result['inventoryPassageSupersessions'] == base['inventoryPassageSupersessions'] + len(mine['passageSupersessions'])
inventory = json.loads((A / result['selectedInventory']['path']).read_bytes())
current = {x['selector']['jsonPointer']: x['after'] for x in without['inventoryPassageInheritance']}
for o in mine['passageOverrides']:
    i = int(o['selector']['jsonPointer'].split('/')[2])
    assert o['parent'] == result['selectedInventory'] and o['selector']['jsonPointer'] not in current
    assert o['before'] == inventory['files'][i]['description']
for s in mine['passageSupersessions']:
    assert s['parent'] == result['selectedInventory'] and s['before'] == current[s['selector']['jsonPointer']]
print(json.dumps({'mode': mode, 'passed': result['passed'], 'selectedInventory': result['selectedInventory']['path'],
                  'inventorySuccessors': len(result['inventorySuccessors']), 'contractSuccessors': len(result['contractSuccessors']),
                  'inventoryPassageInheritance': len(result['inventoryPassageInheritance']),
                  'inventoryPassageSupersessions': {'before': base['inventoryPassageSupersessions'], 'after': result['inventoryPassageSupersessions']},
                  'd3': {'selected': mine['selected'], 'passageOverrides': len(mine['passageOverrides']),
                         'passageSupersessions': len(mine['passageSupersessions'])},
                  'generationSources': result.get('generationSources'), 'admissionSources': result.get('admissionSources')}, indent=1))
