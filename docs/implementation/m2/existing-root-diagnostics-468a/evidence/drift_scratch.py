"""Scratch-only drift check through the worktree's real generate_contracts.generate, with
verify_design patched exactly as verify_scratch.py (synthetic in-memory 468a review/assent)."""
import argparse, hashlib, importlib.util, json, sys
from pathlib import Path
W = Path('/Users/sb/code/opensip-ai/opensip-468a'); A = Path('/Users/sb/code/opensip-ai/opensip_arch'); S = Path(sys.argv[1])
spec = importlib.util.spec_from_file_location('gc', W / 'tools/generate_contracts.py'); gc = importlib.util.module_from_spec(spec); spec.loader.exec_module(gc)
D = 'docs/implementation/m2/existing-root-diagnostics-468a'
def pin(p): b = (A / p).read_bytes(); return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
orig = gc.module
def patched(path, name):
    m = orig(path, name)
    if name != 'design_preflight': return m
    subject, record = pin(D + '-subject.json'), pin(D + '/successor.json')
    review = json.dumps({'verdict': 'ACCEPT-DESIGN-UNIT', 'requiredFindings': [], 'subjectManifestSha256': subject['sha256']}).encode()
    rpin = {'path': 'SCRATCH-468A/review.json', 'bytes': len(review), 'sha256': hashlib.sha256(review).hexdigest()}
    assent = json.dumps({'status': 'ACCEPTED-DESIGN-UNIT', 'rootSubstantiveAssent': True, 'requiredUnitFindings': [], 'subjectManifest': subject, 'independentReview': rpin, 'acceptedSuccessor': record}).encode()
    apin = {'path': 'SCRATCH-468A/assent.json', 'bytes': len(assent), 'sha256': hashlib.sha256(assent).hexdigest()}
    synthetic = {rpin['path']: review, apin['path']: assent}; real = m.pinned_bytes; real_verify = m.verify
    def pinned_bytes(root, row):
        if isinstance(row, dict) and row.get('path') in synthetic: return synthetic[row['path']]
        return real(root, row)
    def verify(architecture, lock, implementation=None):
        lock = dict(lock); lock['contractSuccessors'] = [*lock['contractSuccessors'], {'record': record, 'subjectManifest': subject, 'review': rpin, 'assent': apin}]
        return real_verify(architecture, lock, implementation)
    m.pinned_bytes, m.verify = pinned_bytes, verify
    return m
gc.module = patched
args = argparse.Namespace(root=W, architecture=A, output=S / 'gen-drift', node=Path('/Users/sb/.nvm/versions/node/v24.16.0/bin/node'),
    generator=Path('/Users/sb/opensip-deps/contracts-generator-rebuild-01/opensip-contract-generator'),
    python=Path('/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/Resources/Python.app/Contents/MacOS/Python'), write=False)
print(json.dumps(gc.generate(args)))
