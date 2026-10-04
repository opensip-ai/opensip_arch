"""F8b step 9 (scratch only): run the checkout's real verify_design over a lock that binds F8b,
with a synthetic review and assent held in memory (SCRATCH-F8B/ paths). Nothing is written to
either repository. It proves only that everything except the missing independent review and
root assent passes.

Two modes, chosen by the checkout's lock (as D3's verify_scratch.py):
- appended: the lock does not bind F8b, so the binding is appended in memory;
- bound: the lock's last contract successor is F8b (the uncommitted opensip-f8b worktree).
  Its record and subject pins must equal this tree's bytes, and its review and assent pins
  must be the SCRATCH-F8B placeholders, which only this overlay serves. Plain verify_design
  refuses that lock until the lead replaces the two placeholders.

It asserts that both locks pass and that F8b adds exactly one contract successor. The selected
inventory, the inheritance projection and the supersession count must equal those of the lock
without F8b. It also asserts that F8b's frozen closure and lane-registry copies are F8b inputs,
and that the lane registry is selected exactly once across all units (check_typescript.py's
rule). In bound mode the checkout must carry exactly those bytes.
Usage: verify_scratch_f8b.py [CHECKOUT]"""
import copy, hashlib, importlib.util, json, sys
from pathlib import Path
W = Path(sys.argv[1] if len(sys.argv) > 1 else '/Users/sb/code/opensip-ai/opensip').resolve(strict=True)
A = Path('/Users/sb/code/opensip-ai/opensip_arch')
spec = importlib.util.spec_from_file_location('vd', W / 'tools/verify_design.py'); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
D = 'docs/implementation/m2/generator-closure-f8b'
def pin(p): b = (A / p).read_bytes(); return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
subject, record = pin(D + '-subject.json'), pin(D + '/successor.json')
review = json.dumps({'verdict': 'ACCEPT-DESIGN-UNIT', 'requiredFindings': [], 'subjectManifestSha256': subject['sha256']}).encode()
rpin = {'path': 'SCRATCH-F8B/review.json', 'bytes': len(review), 'sha256': hashlib.sha256(review).hexdigest()}
assent = json.dumps({'status': 'ACCEPTED-DESIGN-UNIT', 'rootSubstantiveAssent': True, 'requiredUnitFindings': [], 'subjectManifest': subject, 'independentReview': rpin, 'acceptedSuccessor': record}).encode()
apin = {'path': 'SCRATCH-F8B/assent.json', 'bytes': len(assent), 'sha256': hashlib.sha256(assent).hexdigest()}
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
    assert lock['contractSuccessors'][-1] == binding, 'the bound F8b entry differs from this tree or its placeholders'
    without = copy.deepcopy(lock); without['contractSuccessors'].pop()
else:
    mode = 'appended'
    without = copy.deepcopy(lock); lock['contractSuccessors'].append(binding)
assert all(b['record']['path'] != record['path'] for b in without['contractSuccessors'])
base = m.verify(A, without, W)
result = m.verify(A, lock, W)
mine = result['contractSuccessors'][-1]
assert base['passed'] is True and result['passed'] is True
assert len(result['contractSuccessors']) == len(base['contractSuccessors']) + 1
assert mine['selected'] == record['path'] and mine['passageOverrides'] == [] and mine['passageSupersessions'] == []
assert result['selectedInventory'] == base['selectedInventory']
assert result['inventoryPassageInheritance'] == base['inventoryPassageInheritance']
assert result['inventoryPassageSupersessions'] == base['inventoryPassageSupersessions']
inputs = [row for unit in result['contractSuccessors'] for row in unit['inputs']]
def selected(raw):
    d = hashlib.sha256(raw).hexdigest()
    return sum(1 for row in inputs if row['sha256'] == d and row['bytes'] == len(raw)), sum(1 for row in mine['inputs'] if row['sha256'] == d and row['bytes'] == len(raw))
# Selection is judged for F8b's frozen product copies. The checkout carries those bytes only
# where F8b is materialized (the bound worktree); main still carries the base bytes.
closure, lanes = ((A / D / 'product' / p).read_bytes() for p in ('tools/contracts/generator-closure.json', 'tools/typescript-lanes.json'))
closure_all, closure_f8b = selected(closure)
lanes_all, lanes_f8b = selected(lanes)
assert closure_f8b == 1 and lanes_f8b == 1 and lanes_all == 1
materialized = (W / 'tools/contracts/generator-closure.json').read_bytes() == closure and (W / 'tools/typescript-lanes.json').read_bytes() == lanes
assert materialized or mode == 'appended', 'bound checkout does not carry F8b materialization'
print(json.dumps({'mode': mode, 'checkoutCarriesF8b': materialized, 'passed': result['passed'], 'selectedInventory': result['selectedInventory']['path'],
                  'inventorySuccessors': len(result['inventorySuccessors']),
                  'contractSuccessors': {'without': len(base['contractSuccessors']), 'with': len(result['contractSuccessors'])},
                  'inventoryPassageInheritance': len(result['inventoryPassageInheritance']),
                  'inventoryPassageSupersessions': result['inventoryPassageSupersessions'],
                  'f8b': {'selected': mine['selected'], 'inputs': len(mine['inputs']), 'passageOverrides': 0, 'passageSupersessions': 0},
                  'generatorClosureSelected': {'byF8b': closure_f8b, 'byAll': closure_all},
                  'laneRegistrySelected': {'byF8b': lanes_f8b, 'byAll': lanes_all},
                  'generationSources': result.get('generationSources'), 'admissionSources': result.get('admissionSources'),
                  'inputsVerified': result.get('inputsVerified')}, indent=1))
