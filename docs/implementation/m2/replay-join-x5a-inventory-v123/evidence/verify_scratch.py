"""Scratch-only: run a product worktree's real verify_design with the
inventory123 successor appended to its lock (which selects the parent,
inventory122 for unit X3d-2, at product 933e78b, D2 bound) and the re-projected
inheritance (fifty-five rows), with a synthetic in-memory review and assent (SCRATCH-X5A/
paths). Nothing is written to either repository. Proves only that everything
except the missing independent review and root assent passes. Usage: verify_scratch.py [WORKTREE]."""
import hashlib, importlib.util, json, sys
from pathlib import Path
W = Path(sys.argv[1] if len(sys.argv) > 1 else '/Users/sb/code/opensip-ai/opensip-x5a')
A = Path('/Users/sb/code/opensip-ai/opensip_arch')
spec = importlib.util.spec_from_file_location('vd', W / 'tools/verify_design.py'); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
M = 'docs/implementation/m2/'
def pin(p): b = (A / p).read_bytes(); return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
lock = json.loads((W / 'design-lock.json').read_text())
parent, candidate = lock['inventorySuccessors'][-1]['candidate'], pin(M + 'repository-file-inventory.v123.json')
assert pin(parent['path']) == parent and json.loads((A / M / 'replay-join-x5a-inventory-v123/successor.json').read_bytes())['parent'] == parent, 'inventory123 must be built on the selected inventory'
record, subject = pin(M + 'replay-join-x5a-inventory-v123/successor.json'), pin(M + 'replay-join-x5a-inventory-v123-subject.json')
review = json.dumps({'verdict': 'ACCEPT-UNIT', 'requiredFindings': [], 'subjectManifestSha256': subject['sha256'],
    'inventoryCandidateAssessment': {'verdict': 'ACCEPT', 'requiredFindings': [], **candidate, 'parent': parent, 'successorRecord': record}}).encode()
rpin = {'path': 'SCRATCH-X5A/review.json', 'bytes': len(review), 'sha256': hashlib.sha256(review).hexdigest()}
assent = json.dumps({'status': 'ACCEPTED-UNIT', 'rootSubstantiveAssent': True, 'requiredUnitFindings': [], 'subjectManifest': subject,
    'independentReview': rpin, 'acceptedInventory': candidate}).encode()
apin = {'path': 'SCRATCH-X5A/assent.json', 'bytes': len(assent), 'sha256': hashlib.sha256(assent).hexdigest()}
synthetic = {rpin['path']: review, apin['path']: assent}
real = m.pinned_bytes
def pinned_bytes(root, row):
    if isinstance(row, dict) and row.get('path') in synthetic:
        raw = synthetic[row['path']]; assert hashlib.sha256(raw).hexdigest() == row['sha256']; return raw
    return real(root, row)
m.pinned_bytes = pinned_bytes
lock['inventorySuccessors'].append({'parent': parent, 'candidate': candidate, 'record': record, 'review': rpin, 'assent': apin})
rows = json.loads((A / record['path']).read_text())['descriptionOverrideProjection']
lock['inventoryPassageInheritance'] = sorted(
    ({'parent': candidate, 'selector': r['candidateSelector'], 'before': r['before'], 'after': r['effectiveDescription']} for r in rows),
    key=lambda o: json.dumps(o['selector'], sort_keys=True))
result = m.verify(A, lock, W)
print(json.dumps({'passed': result.get('passed'), 'inventorySuccessors': len(result['inventorySuccessors']),
                  'contractSuccessors': len(result['contractSuccessors']), 'inventoryPassageInheritance': len(result['inventoryPassageInheritance']),
                  'selectedInventory': result['selectedInventory']['path']}, indent=1))
