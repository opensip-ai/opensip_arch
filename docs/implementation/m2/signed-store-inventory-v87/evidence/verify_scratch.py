"""Scratch-only: run a product worktree's real verify_design with inventory84
(unit X2a, committed, under review) and then inventory87 (this unit) appended
to its lock, which selects inventory83 at product 99f1c35, with the
re-projected inheritance and synthetic in-memory reviews and assents
(SCRATCH-X4T0/ paths). Nothing is written to either repository. Proves only
that everything except the missing independent reviews and root assents
passes. Usage: verify_scratch.py [WORKTREE] [--lock-out PATH]."""
import hashlib, importlib.util, json, sys
from pathlib import Path
args = [a for a in sys.argv[1:] if not a.startswith('--')]
W = Path(args[0] if args else '/Users/sb/code/opensip-ai/opensip-x4t0')
lock_out = sys.argv[sys.argv.index('--lock-out') + 1] if '--lock-out' in sys.argv else None
A = Path('/Users/sb/code/opensip-ai/opensip_arch')
spec = importlib.util.spec_from_file_location('vd', W / 'tools/verify_design.py'); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
M = 'docs/implementation/m2/'
def pin(p): b = (A / p).read_bytes(); return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
synthetic = {}
def unit(tag, parent_v, cand_v, record_path, subject_path):
    parent, candidate = pin(M + f'repository-file-inventory.v{parent_v}.json'), pin(M + f'repository-file-inventory.v{cand_v}.json')
    record, subject = pin(M + record_path), pin(M + subject_path)
    review = json.dumps({'verdict': 'ACCEPT-UNIT', 'requiredFindings': [], 'subjectManifestSha256': subject['sha256'],
        'inventoryCandidateAssessment': {'verdict': 'ACCEPT', 'requiredFindings': [], **candidate, 'parent': parent, 'successorRecord': record}}).encode()
    rpin = {'path': f'SCRATCH-X4T0/{tag}-review.json', 'bytes': len(review), 'sha256': hashlib.sha256(review).hexdigest()}
    assent = json.dumps({'status': 'ACCEPTED-UNIT', 'rootSubstantiveAssent': True, 'requiredUnitFindings': [], 'subjectManifest': subject,
        'independentReview': rpin, 'acceptedInventory': candidate}).encode()
    apin = {'path': f'SCRATCH-X4T0/{tag}-assent.json', 'bytes': len(assent), 'sha256': hashlib.sha256(assent).hexdigest()}
    synthetic[rpin['path']] = review; synthetic[apin['path']] = assent
    return {'parent': parent, 'candidate': candidate, 'record': record, 'review': rpin, 'assent': apin}
real = m.pinned_bytes
def pinned_bytes(root, row):
    if isinstance(row, dict) and row.get('path') in synthetic:
        raw = synthetic[row['path']]; assert hashlib.sha256(raw).hexdigest() == row['sha256']; return raw
    return real(root, row)
m.pinned_bytes = pinned_bytes
lock = json.loads((W / 'design-lock.json').read_text())
assert lock['inventorySuccessors'][-1]['candidate'] == pin(M + 'repository-file-inventory.v83.json'), 'the lock must select inventory83'
v84 = unit('v84', 83, 84, 'project-chain-inventory-v84/successor.json', 'project-chain-inventory-v84-subject.json')
lock['inventorySuccessors'].append(v84)
def project(entry):
    rows = json.loads((A / entry['record']['path']).read_text())['descriptionOverrideProjection']
    lock['inventoryPassageInheritance'] = sorted(
        ({'parent': entry['candidate'], 'selector': r['candidateSelector'], 'before': r['before'], 'after': r['effectiveDescription']} for r in rows),
        key=lambda o: json.dumps(o['selector'], sort_keys=True))
project(v84)
if lock_out:
    Path(lock_out).write_text(json.dumps(lock, indent=2) + '\n')
v87 = unit('v87', 84, 87, 'signed-store-inventory-v87/successor.json', 'signed-store-inventory-v87-subject.json')
lock['inventorySuccessors'].append(v87)
project(v87)
result = m.verify(A, lock, W)
print(json.dumps({'passed': result.get('passed'), 'inventorySuccessors': len(result['inventorySuccessors']),
                  'contractSuccessors': len(result['contractSuccessors']), 'inventoryPassageInheritance': len(result['inventoryPassageInheritance']),
                  'selectedInventory': result['selectedInventory']['path']}, indent=1))
