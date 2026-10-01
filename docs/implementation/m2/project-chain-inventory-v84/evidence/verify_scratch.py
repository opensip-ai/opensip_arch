"""Scratch-only: run a product worktree's real verify_design with inventory83
(unit X3a-1) and then inventory84 (unit X2a) appended to its lock, which
selects inventory82 and the X10b contract successor, and with the inheritance
re-projected onto inventory84. Every review and assent is a synthetic
in-memory document (SCRATCH-X3A1/ and SCRATCH-X2A/ paths). Nothing is written
to either repository. Proves only that everything except the missing
independent reviews and root assents passes. Usage: verify_scratch.py
[WORKTREE]."""
import hashlib, importlib.util, json, sys
from pathlib import Path
W = Path(sys.argv[1] if len(sys.argv) > 1 else '/Users/sb/code/opensip-ai/opensip-x2a')
A = Path('/Users/sb/code/opensip-ai/opensip_arch')
spec = importlib.util.spec_from_file_location('vd', W / 'tools/verify_design.py'); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
M = 'docs/implementation/m2/'
def pin(p): b = (A / p).read_bytes(); return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
synthetic = {}
def successor(tag, parent_version, version, unit):
    parent, candidate = pin(f'{M}repository-file-inventory.v{parent_version}.json'), pin(f'{M}repository-file-inventory.v{version}.json')
    record, subject = pin(f'{M}{unit}/successor.json'), pin(f'{M}{unit}-subject.json')
    review = json.dumps({'verdict': 'ACCEPT-UNIT', 'requiredFindings': [], 'subjectManifestSha256': subject['sha256'],
        'inventoryCandidateAssessment': {'verdict': 'ACCEPT', 'requiredFindings': [], **candidate, 'parent': parent, 'successorRecord': record}}).encode()
    rpin = {'path': f'SCRATCH-{tag}/review.json', 'bytes': len(review), 'sha256': hashlib.sha256(review).hexdigest()}
    assent = json.dumps({'status': 'ACCEPTED-UNIT', 'rootSubstantiveAssent': True, 'requiredUnitFindings': [], 'subjectManifest': subject,
        'independentReview': rpin, 'acceptedInventory': candidate}).encode()
    apin = {'path': f'SCRATCH-{tag}/assent.json', 'bytes': len(assent), 'sha256': hashlib.sha256(assent).hexdigest()}
    synthetic[rpin['path']] = review; synthetic[apin['path']] = assent
    return {'parent': parent, 'candidate': candidate, 'record': record, 'review': rpin, 'assent': apin}
real = m.pinned_bytes
def pinned_bytes(root, row):
    if isinstance(row, dict) and row.get('path') in synthetic:
        raw = synthetic[row['path']]; assert hashlib.sha256(raw).hexdigest() == row['sha256']; return raw
    return real(root, row)
m.pinned_bytes = pinned_bytes
lock = json.loads((W / 'design-lock.json').read_text())
v83 = successor('X3A1', 82, 83, 'store-endpoint-inventory-v83')
assert lock['inventorySuccessors'][-1]['candidate'] == v83['parent'], 'the lock must select inventory82'
v84 = successor('X2A', 83, 84, 'project-chain-inventory-v84')
lock['inventorySuccessors'] += [v83, v84]
rows = json.loads((A / v84['record']['path']).read_text())['descriptionOverrideProjection']
lock['inventoryPassageInheritance'] = sorted(
    ({'parent': v84['candidate'], 'selector': r['candidateSelector'], 'before': r['before'], 'after': r['effectiveDescription']} for r in rows),
    key=lambda o: json.dumps(o['selector'], sort_keys=True))
result = m.verify(A, lock, W)
print(json.dumps({'passed': result.get('passed'), 'inventorySuccessors': len(result['inventorySuccessors']),
                  'contractSuccessors': len(result['contractSuccessors']), 'inventoryPassageInheritance': len(result['inventoryPassageInheritance']),
                  'selectedInventory': result['selectedInventory']['path']}, indent=1))
