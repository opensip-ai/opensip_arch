"""Scratch-only: run the worktree's real verify_design with one appended 468a contract
binding whose review and assent are synthetic in-memory documents (SCRATCH-468A/ paths).
Nothing is written to either repository. This proves only that everything except the
missing independent review and root assent passes."""
import hashlib, importlib.util, json, sys
from pathlib import Path
W = Path('/Users/sb/code/opensip-ai/opensip-468a'); A = Path('/Users/sb/code/opensip-ai/opensip_arch')
spec = importlib.util.spec_from_file_location('vd', W / 'tools/verify_design.py'); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
D = 'docs/implementation/m2/existing-root-diagnostics-468a'
def pin(p): b = (A / p).read_bytes(); return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
subject, record = pin(D + '-subject.json'), pin(D + '/successor.json')
review = json.dumps({'verdict': 'ACCEPT-DESIGN-UNIT', 'requiredFindings': [], 'subjectManifestSha256': subject['sha256']}).encode()
rpin = {'path': 'SCRATCH-468A/review.json', 'bytes': len(review), 'sha256': hashlib.sha256(review).hexdigest()}
assent = json.dumps({'status': 'ACCEPTED-DESIGN-UNIT', 'rootSubstantiveAssent': True, 'requiredUnitFindings': [], 'subjectManifest': subject, 'independentReview': rpin, 'acceptedSuccessor': record}).encode()
apin = {'path': 'SCRATCH-468A/assent.json', 'bytes': len(assent), 'sha256': hashlib.sha256(assent).hexdigest()}
synthetic = {rpin['path']: review, apin['path']: assent}
real = m.pinned_bytes
def pinned_bytes(root, row):
    if isinstance(row, dict) and row.get('path') in synthetic:
        raw = synthetic[row['path']]; assert hashlib.sha256(raw).hexdigest() == row['sha256']; return raw
    return real(root, row)
m.pinned_bytes = pinned_bytes
lock = json.loads((W / 'design-lock.json').read_text())
lock['contractSuccessors'].append({'record': record, 'subjectManifest': subject, 'review': rpin, 'assent': apin})
result = m.verify(A, lock, W)
print(json.dumps({'passed': result.get('passed'), 'generationSources': result.get('generationSources'), 'admissionSources': result.get('admissionSources'),
                  'contractSuccessors': len(result['contractSuccessors']), 'inventoryPassageInheritance': len(result['inventoryPassageInheritance'])}, indent=1))
