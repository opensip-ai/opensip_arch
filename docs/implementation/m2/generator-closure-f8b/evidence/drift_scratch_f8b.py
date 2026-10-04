"""F8b step 5 (admitted drift gate, scratch approval): run the checkout's real public
generate_contracts.generate with rebuild-02 and write=False.

Only the missing review and assent are synthetic. They are served in memory at SCRATCH-F8B/
paths by patching the design_preflight module that generate_contracts loads, as 468a's
drift_scratch.py did. In the bound worktree the lock already carries F8b's binding with
those placeholders; otherwise the binding is appended in memory. Every closure, toolchain,
receipt, options and tool-byte check runs unchanged. rebuild-01 is never passed here: after
F8b, pipeline.py:40-44 refuses it, as it should. Nothing is written to either repository.
Usage: drift_scratch_f8b.py CHECKOUT OUTPUT_DIR (must not exist; the pipeline creates it)"""
import argparse, hashlib, importlib.util, json, sys
from pathlib import Path
W = Path(sys.argv[1]).resolve(strict=True); A = Path('/Users/sb/code/opensip-ai/opensip_arch'); S = Path(sys.argv[2])
spec = importlib.util.spec_from_file_location('gc', W / 'tools/generate_contracts.py'); gc = importlib.util.module_from_spec(spec); spec.loader.exec_module(gc)
D = 'docs/implementation/m2/generator-closure-f8b'
def pin(p): b = (A / p).read_bytes(); return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
orig = gc.module
state = {}
def patched(path, name):
    m = orig(path, name)
    if name != 'design_preflight': return m
    subject, record = pin(D + '-subject.json'), pin(D + '/successor.json')
    review = json.dumps({'verdict': 'ACCEPT-DESIGN-UNIT', 'requiredFindings': [], 'subjectManifestSha256': subject['sha256']}).encode()
    rpin = {'path': 'SCRATCH-F8B/review.json', 'bytes': len(review), 'sha256': hashlib.sha256(review).hexdigest()}
    assent = json.dumps({'status': 'ACCEPTED-DESIGN-UNIT', 'rootSubstantiveAssent': True, 'requiredUnitFindings': [], 'subjectManifest': subject, 'independentReview': rpin, 'acceptedSuccessor': record}).encode()
    apin = {'path': 'SCRATCH-F8B/assent.json', 'bytes': len(assent), 'sha256': hashlib.sha256(assent).hexdigest()}
    synthetic = {rpin['path']: review, apin['path']: assent}; real = m.pinned_bytes; real_verify = m.verify
    binding = {'record': record, 'subjectManifest': subject, 'review': rpin, 'assent': apin}
    def pinned_bytes(root, row):
        if isinstance(row, dict) and row.get('path') in synthetic: return synthetic[row['path']]
        return real(root, row)
    def verify(architecture, lock, implementation=None):
        lock = dict(lock)
        if lock['contractSuccessors'][-1]['record']['path'] == record['path']:
            assert lock['contractSuccessors'][-1] == binding, 'bound F8b entry differs'; state['mode'] = 'bound'
        else:
            lock['contractSuccessors'] = [*lock['contractSuccessors'], binding]; state['mode'] = 'appended'
        return real_verify(architecture, lock, implementation)
    m.pinned_bytes, m.verify = pinned_bytes, verify
    return m
gc.module = patched
args = argparse.Namespace(root=W, architecture=A, output=S, node=Path('/Users/sb/.nvm/versions/node/v24.16.0/bin/node'),
    generator=Path('/Users/sb/opensip-deps/contracts-generator-rebuild-02/opensip-contract-generator'),
    python=Path('/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/Resources/Python.app/Contents/MacOS/Python'), write=False)
assert not S.exists(), 'the pipeline creates the output directory itself'
receipt = gc.generate(args)
receipt['scratchMode'] = state.get('mode')
print(json.dumps(receipt))
sys.exit(0 if receipt['passed'] and receipt['changed'] == [] else 1)
