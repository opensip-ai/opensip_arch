"""Scratch-only: run the worktree's real verify_design with the inventory81
successor appended and the re-projected inheritance, whose review and assent
are synthetic in-memory documents (SCRATCH-X1A/ paths). Nothing is written to
either repository. Proves only that everything except the missing independent
review and root assent passes. Prints the lock's expected inheritance rows."""
import hashlib, importlib.util, json, sys
from pathlib import Path
W = Path(sys.argv[1] if len(sys.argv) > 1 else '/Users/sb/code/opensip-ai/opensip-x1a')
A = Path('/Users/sb/code/opensip-ai/opensip_arch')
spec = importlib.util.spec_from_file_location('vd', W / 'tools/verify_design.py'); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
M = 'docs/implementation/m2/'
def pin(p): b = (A / p).read_bytes(); return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
parent, candidate = pin(M + 'repository-file-inventory.v80.json'), pin(M + 'repository-file-inventory.v81.json')
record, subject = pin(M + 'ordinary-writer-inventory-v81/successor.json'), pin(M + 'ordinary-writer-inventory-v81-subject.json')
review = json.dumps({'verdict': 'ACCEPT-UNIT', 'requiredFindings': [], 'subjectManifestSha256': subject['sha256'],
    'inventoryCandidateAssessment': {'verdict': 'ACCEPT', 'requiredFindings': [], **candidate, 'parent': parent, 'successorRecord': record}}).encode()
rpin = {'path': 'SCRATCH-X1A/review.json', 'bytes': len(review), 'sha256': hashlib.sha256(review).hexdigest()}
assent = json.dumps({'status': 'ACCEPTED-UNIT', 'rootSubstantiveAssent': True, 'requiredUnitFindings': [], 'subjectManifest': subject,
    'independentReview': rpin, 'acceptedInventory': candidate}).encode()
apin = {'path': 'SCRATCH-X1A/assent.json', 'bytes': len(assent), 'sha256': hashlib.sha256(assent).hexdigest()}
synthetic = {rpin['path']: review, apin['path']: assent}
real = m.pinned_bytes
def pinned_bytes(root, row):
    if isinstance(row, dict) and row.get('path') in synthetic:
        raw = synthetic[row['path']]; assert hashlib.sha256(raw).hexdigest() == row['sha256']; return raw
    return real(root, row)
m.pinned_bytes = pinned_bytes
lock = json.loads((W / 'design-lock.json').read_text())
lock['inventorySuccessors'].append({'parent': parent, 'candidate': candidate, 'record': record, 'review': rpin, 'assent': apin})
rows = json.loads((A / record['path']).read_text())['descriptionOverrideProjection']
lock['inventoryPassageInheritance'] = sorted(
    ({'parent': candidate, 'selector': r['candidateSelector'], 'before': r['before'], 'after': r['effectiveDescription']} for r in rows),
    key=lambda o: json.dumps(o['selector'], sort_keys=True))
result = m.verify(A, lock, W)
print(json.dumps({'passed': result.get('passed'), 'inventorySuccessors': len(result['inventorySuccessors']),
                  'contractSuccessors': len(result['contractSuccessors']), 'inventoryPassageInheritance': len(result['inventoryPassageInheritance']),
                  'selectedInventory': result['selectedInventory']['path']}, indent=1))
