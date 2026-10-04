"""F8c step 5 (admitted drift gate, scratch approval): run the checkout's real public
generate_contracts.generate with the selected generator (rebuild-02) and write=False.

Only the missing review and assent are synthetic. They are served in memory at SCRATCH-F8C/
paths by patching the design_preflight module that generate_contracts loads (the checkout's
own tools/verify_design.py, VD2-a's bytes), as F8b's drift_scratch_f8b.py and I1-a's
drift_scratch_i1a.py did. In the staged worktree the lock already carries F8c's binding with
those placeholders, and it must equal verify_scratch_f8c.py's entry; otherwise the binding is
appended in memory. Every closure, toolchain, receipt, options and tool-byte check runs
unchanged, including "generator closure is not selected by an accepted design unit".
Nothing is written to either repository. It exits 0 only when the gate passes with
changed: [].
Usage: drift_scratch_f8c.py CHECKOUT OUTPUT_DIR (must not exist; the pipeline creates it)"""
import argparse, importlib.util, json, sys
from pathlib import Path
W = Path(sys.argv[1]).resolve(strict=True); A = Path('/Users/sb/code/opensip-ai/opensip_arch'); S = Path(sys.argv[2])
here = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('scratch', here / 'verify_scratch_f8c.py'); s = importlib.util.module_from_spec(spec); spec.loader.exec_module(s)
spec = importlib.util.spec_from_file_location('gc', W / 'tools/generate_contracts.py'); gc = importlib.util.module_from_spec(spec); spec.loader.exec_module(gc)
orig = gc.module
state = {}
def patched(path, name):
    m = orig(path, name)
    if name != 'design_preflight': return m
    entry, _ = s.binding(); s.overlay(m); real_verify = m.verify
    def verify(architecture, lock, implementation=None):
        lock = dict(lock)
        if lock['contractSuccessors'][-1]['record']['path'] == entry['record']['path']:
            assert lock['contractSuccessors'][-1] == entry, 'staged F8c entry differs'; state['mode'] = 'staged'
        else:
            lock['contractSuccessors'] = [*lock['contractSuccessors'], entry]; state['mode'] = 'appended'
        state['approval'] = real_verify(architecture, lock, implementation)
        return state['approval']
    m.verify = verify
    return m
gc.module = patched
args = argparse.Namespace(root=W, architecture=A, output=S, node=Path('/Users/sb/.nvm/versions/node/v24.16.0/bin/node'),
    generator=Path('/Users/sb/opensip-deps/contracts-generator-rebuild-02/opensip-contract-generator'),
    python=Path('/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/Resources/Python.app/Contents/MacOS/Python'), write=False)
assert not S.exists(), 'the pipeline creates the output directory itself'
receipt = gc.generate(args)
receipt['scratchMode'] = state.get('mode')
receipt['contractPassageSupersessions'] = state['approval'].get('contractPassageSupersessions')
print(json.dumps(receipt))
sys.exit(0 if receipt['passed'] and receipt['changed'] == [] else 1)
