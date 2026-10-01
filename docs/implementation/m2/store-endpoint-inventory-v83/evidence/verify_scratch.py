"""Scratch-only: run a product worktree's real verify_design with three
successors appended, each with synthetic in-memory review and assent
(SCRATCH-X3A1/ paths): the X10b contract successor and inventory82 (unit
X10a, committed in arch, under review), then inventory83 with its
re-projected inheritance. Nothing is written to either repository. Proves
only that everything except the missing independent reviews and root
assents passes. Usage: verify_scratch.py [WORKTREE]."""
import hashlib, importlib.util, json, sys
from pathlib import Path
W = Path(sys.argv[1] if len(sys.argv) > 1 else '/Users/sb/code/opensip-ai/opensip-x3a1')
A = Path('/Users/sb/code/opensip-ai/opensip_arch')
spec = importlib.util.spec_from_file_location('vd', W / 'tools/verify_design.py'); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
M = 'docs/implementation/m2/'
def pin(p): b = (A / p).read_bytes(); return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
synthetic = {}
def synth(name, document):
    raw = json.dumps(document).encode()
    row = {'path': f'SCRATCH-X3A1/{name}', 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}
    synthetic[row['path']] = raw
    return row
def inventory(parent_path, candidate_path, record_path, subject_path, tag):
    parent, candidate = pin(parent_path), pin(candidate_path)
    record, subject = pin(record_path), pin(subject_path)
    review = synth(f'{tag}-review.json', {'verdict': 'ACCEPT-UNIT', 'requiredFindings': [], 'subjectManifestSha256': subject['sha256'],
        'inventoryCandidateAssessment': {'verdict': 'ACCEPT', 'requiredFindings': [], **candidate, 'parent': parent, 'successorRecord': record}})
    assent = synth(f'{tag}-assent.json', {'status': 'ACCEPTED-UNIT', 'rootSubstantiveAssent': True, 'requiredUnitFindings': [],
        'subjectManifest': subject, 'independentReview': review, 'acceptedInventory': candidate})
    return {'parent': parent, 'candidate': candidate, 'record': record, 'review': review, 'assent': assent}
x10b_subject, x10b_record = pin(M + 'read-cli-x10b-subject.json'), pin(M + 'read-cli-x10b/successor.json')
x10b_review = synth('x10b-review.json', {'verdict': 'ACCEPT-DESIGN-UNIT', 'requiredFindings': [], 'subjectManifestSha256': x10b_subject['sha256']})
x10b_assent = synth('x10b-assent.json', {'status': 'ACCEPTED-DESIGN-UNIT', 'rootSubstantiveAssent': True, 'requiredUnitFindings': [],
    'subjectManifest': x10b_subject, 'independentReview': x10b_review, 'acceptedSuccessor': x10b_record})
v82 = inventory(M + 'repository-file-inventory.v81.json', M + 'repository-file-inventory.v82.json',
                M + 'read-cli-inventory-v82/successor.json', M + 'read-cli-inventory-v82-subject.json', 'v82')
v83 = inventory(M + 'repository-file-inventory.v82.json', M + 'repository-file-inventory.v83.json',
                M + 'store-endpoint-inventory-v83/successor.json', M + 'store-endpoint-inventory-v83-subject.json', 'v83')
real = m.pinned_bytes
def pinned_bytes(root, row):
    if isinstance(row, dict) and row.get('path') in synthetic:
        raw = synthetic[row['path']]; assert hashlib.sha256(raw).hexdigest() == row['sha256']; return raw
    return real(root, row)
m.pinned_bytes = pinned_bytes
lock = json.loads((W / 'design-lock.json').read_text())
lock['contractSuccessors'].append({'record': x10b_record, 'subjectManifest': x10b_subject, 'review': x10b_review, 'assent': x10b_assent})
lock['inventorySuccessors'] += [v82, v83]
rows = json.loads((A / v83['record']['path']).read_text())['descriptionOverrideProjection']
lock['inventoryPassageInheritance'] = sorted(
    ({'parent': v83['candidate'], 'selector': r['candidateSelector'], 'before': r['before'], 'after': r['effectiveDescription']} for r in rows),
    key=lambda o: json.dumps(o['selector'], sort_keys=True))
result = m.verify(A, lock, W)
print(json.dumps({'passed': result.get('passed'), 'inventorySuccessors': len(result['inventorySuccessors']),
                  'contractSuccessors': len(result['contractSuccessors']), 'inventoryPassageInheritance': len(result['inventoryPassageInheritance']),
                  'selectedInventory': result['selectedInventory']['path']}, indent=1))
