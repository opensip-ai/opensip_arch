"""Write J3a's inventory unit subject and unit records (untracked), from the
current bytes: the subject pins every file of the unit directory and the
candidate; the unit record's sourceBoundary pins every product file J3a adds
or changes (design-lock.json excluded, as in every inventory unit)."""
import hashlib, json, subprocess
from pathlib import Path
A = Path('/Users/sb/code/opensip-ai/opensip_arch'); W = Path('/Users/sb/code/opensip-ai/opensip-j3a')
M = 'docs/implementation/m2/'; U = M + 'durable-entry-j3a-inventory-v139'; C = M + 'repository-file-inventory.v139.json'
def pin(root, p):
    b = (root / p).read_bytes(); return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
files = sorted([C] + [str(p.relative_to(A)) for p in (A / U).rglob('*') if p.is_file() and '__pycache__' not in p.parts])
subject = {'schemaVersion': 1, 'files': [pin(A, p) for p in files]}
(A / (U + '-subject.json')).write_text(json.dumps(subject, indent=2) + '\n')
changed = subprocess.run(['git', '-C', str(W), 'diff', '--name-only', 'b7b87b7'], capture_output=True, text=True, check=True).stdout.split()
added = subprocess.run(['git', '-C', str(W), 'ls-files', '--others', '--exclude-standard'], capture_output=True, text=True, check=True).stdout.split()
paths = sorted(p for p in set(changed) | set(added) if p != 'design-lock.json')
unit = {
    'schemaVersion': 1, 'unit': 'durable-entry-j3a-inventory-v139', 'status': 'DRAFT-PENDING-REVIEW',
    'subjectManifest': pin(A, U + '-subject.json'),
    'independentReview': {'path': 'docs/implementation/m3/reviews/codex-j3a-r1/review.json', 'bytes': None, 'sha256': None},
    'rootSubstantiveAssent': False, 'requiredUnitFindings': None,
    'acceptedInventory': pin(A, C),
    'sourceBoundary': {'verdict': None, 'productBase': 'b7b87b7',
                       'paths': {p: hashlib.sha256((W / p).read_bytes()).hexdigest() for p in paths},
                       'integratedByThisSelector': False},
    'rootAssessment': 'DRAFT. The lead completes this record at integration: the accepted review pin, ACCEPTED-UNIT, root assent and the assessment text.',
    'fullM2Complete': False, 'productQualification': False,
}
(A / (U + '-unit.json')).write_text(json.dumps(unit, indent=2) + '\n')
print(json.dumps({'subjectFiles': len(files), 'subject': pin(A, U + '-subject.json'), 'sourcePaths': len(paths)}))
