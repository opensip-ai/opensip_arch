"""Scratch-only: run the product checkout's real verify_design over a scratch lock, the real
lock with one appended D1 contract binding whose review and assent are synthetic in-memory
documents (SCRATCH-D1/ paths). Nothing is written to either repository. This proves only that
everything except the missing independent review and root assent passes. It also checks that
each override's effective text is what verify_design binds and that the inheritance projection
is unchanged (the overrides are direct overrides on the final selected inventory)."""
import hashlib, importlib.util, json, sys
from pathlib import Path
W = Path(sys.argv[1] if len(sys.argv) > 1 else '/Users/sb/code/opensip-ai/opensip')
A = Path('/Users/sb/code/opensip-ai/opensip_arch')
spec = importlib.util.spec_from_file_location('vd', W / 'tools/verify_design.py'); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
D = 'docs/implementation/m2/description-batch-d1'
def pin(p): b = (A / p).read_bytes(); return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
subject, record = pin(D + '-subject.json'), pin(D + '/successor.json')
review = json.dumps({'verdict': 'ACCEPT-DESIGN-UNIT', 'requiredFindings': [], 'subjectManifestSha256': subject['sha256']}).encode()
rpin = {'path': 'SCRATCH-D1/review.json', 'bytes': len(review), 'sha256': hashlib.sha256(review).hexdigest()}
assent = json.dumps({'status': 'ACCEPTED-DESIGN-UNIT', 'rootSubstantiveAssent': True, 'requiredUnitFindings': [], 'subjectManifest': subject, 'independentReview': rpin, 'acceptedSuccessor': record}).encode()
apin = {'path': 'SCRATCH-D1/assent.json', 'bytes': len(assent), 'sha256': hashlib.sha256(assent).hexdigest()}
synthetic = {rpin['path']: review, apin['path']: assent}
real = m.pinned_bytes
def pinned_bytes(root, row):
    if isinstance(row, dict) and row.get('path') in synthetic:
        raw = synthetic[row['path']]; assert hashlib.sha256(raw).hexdigest() == row['sha256']; return raw
    return real(root, row)
m.pinned_bytes = pinned_bytes
real_lock = json.loads((W / 'design-lock.json').read_text())
lock = json.loads((W / 'design-lock.json').read_text())
lock['contractSuccessors'].append({'record': record, 'subjectManifest': subject, 'review': rpin, 'assent': apin})
result = m.verify(A, lock, W)
mine = result['contractSuccessors'][-1]
assert result['passed'] is True
assert result['inventoryPassageInheritance'] == real_lock['inventoryPassageInheritance']
assert result['selectedInventory'] == real_lock['inventorySuccessors'][-1]['candidate']
assert all(o['parent'] == result['selectedInventory'] for o in mine['passageOverrides'])
print(json.dumps({'passed': result.get('passed'), 'selectedInventory': result['selectedInventory']['path'],
                  'contractSuccessors': len(result['contractSuccessors']), 'inventoryPassageInheritance': len(result['inventoryPassageInheritance']),
                  'd1': {'selected': mine['selected'], 'passageOverrides': len(mine['passageOverrides'])},
                  'generationSources': result.get('generationSources'), 'admissionSources': result.get('admissionSources')}, indent=1))
