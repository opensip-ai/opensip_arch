"""Scratch-only: run a product worktree's real verify_design with inventory96
(this unit) appended to its lock, with the re-projected inheritance and
synthetic in-memory reviews and assents (SCRATCH-X4TA/ paths). Nothing is
written to either repository. While the lock still selects inventory93 (X2b-1,
product 8452ab9), inventory94 (X3c-1, committed but not yet selected) is
appended first; once the lock selects inventory94, only inventory96 is
appended. Any other selection is refused. Proves only that everything except
the missing independent reviews and root assents passes.
Usage: verify_scratch.py [WORKTREE [LOCK]]; LOCK defaults to the worktree's
design-lock.json."""
import hashlib, importlib.util, json, sys
from pathlib import Path
W = Path(sys.argv[1] if len(sys.argv) > 1 else '/Users/sb/code/opensip-ai/opensip-x4ta')
L = Path(sys.argv[2]) if len(sys.argv) > 2 else W / 'design-lock.json'
A = Path('/Users/sb/code/opensip-ai/opensip_arch')
spec = importlib.util.spec_from_file_location('vd', W / 'tools/verify_design.py'); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
M = 'docs/implementation/m2/'
def pin(p): b = (A / p).read_bytes(); return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
synthetic = {}
def successor(parent, candidate, record, subject, tag):
    review = json.dumps({'verdict': 'ACCEPT-UNIT', 'requiredFindings': [], 'subjectManifestSha256': subject['sha256'],
        'inventoryCandidateAssessment': {'verdict': 'ACCEPT', 'requiredFindings': [], **candidate, 'parent': parent, 'successorRecord': record}}).encode()
    rpin = {'path': f'SCRATCH-X4TA/{tag}-review.json', 'bytes': len(review), 'sha256': hashlib.sha256(review).hexdigest()}
    assent = json.dumps({'status': 'ACCEPTED-UNIT', 'rootSubstantiveAssent': True, 'requiredUnitFindings': [], 'subjectManifest': subject,
        'independentReview': rpin, 'acceptedInventory': candidate}).encode()
    apin = {'path': f'SCRATCH-X4TA/{tag}-assent.json', 'bytes': len(assent), 'sha256': hashlib.sha256(assent).hexdigest()}
    synthetic.update({rpin['path']: review, apin['path']: assent})
    return {'parent': parent, 'candidate': candidate, 'record': record, 'review': rpin, 'assent': apin}
v93, v94, v96 = (pin(M + f'repository-file-inventory.v{n}.json') for n in (93, 94, 96))
chain = [(v93, v94, pin(M + 'ledger-creation-inventory-v94/successor.json'), pin(M + 'ledger-creation-inventory-v94-subject.json'), 'v94'),
         (v94, v96, pin(M + 'current-trust-inventory-v96/successor.json'), pin(M + 'current-trust-inventory-v96-subject.json'), 'v96')]
# Both rows are built (and their synthetic bytes registered) either way.
rows94, rows96 = (successor(*c) for c in chain)
real = m.pinned_bytes
def pinned_bytes(root, row):
    if isinstance(row, dict) and row.get('path') in synthetic:
        raw = synthetic[row['path']]; assert hashlib.sha256(raw).hexdigest() == row['sha256']; return raw
    return real(root, row)
m.pinned_bytes = pinned_bytes
lock = json.loads(L.read_text())
selected = lock['inventorySuccessors'][-1]['candidate']
assert selected in (v93, v94), 'the lock must select inventory93 or inventory94'
appended = chain if selected == v93 else chain[1:]
lock['inventorySuccessors'].extend([rows94, rows96] if selected == v93 else [rows96])
rows = json.loads((A / chain[-1][2]['path']).read_text())['descriptionOverrideProjection']
lock['inventoryPassageInheritance'] = sorted(
    ({'parent': v96, 'selector': r['candidateSelector'], 'before': r['before'], 'after': r['effectiveDescription']} for r in rows),
    key=lambda o: json.dumps(o['selector'], sort_keys=True))
result = m.verify(A, lock, W)
print(json.dumps({'passed': result.get('passed'), 'appended': [c[4] for c in appended], 'inventorySuccessors': len(result['inventorySuccessors']),
                  'contractSuccessors': len(result['contractSuccessors']), 'inventoryPassageInheritance': len(result['inventoryPassageInheritance']),
                  'selectedInventory': result['selectedInventory']['path']}, indent=1))
