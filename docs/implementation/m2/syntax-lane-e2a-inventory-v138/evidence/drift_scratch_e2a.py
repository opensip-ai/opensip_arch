"""E2a admitted drift gate, scratch approval: run the checkout's real public
generate_contracts.generate with the selected generator (rebuild-02) and
write=False.

Only the missing reviews and assents are synthetic: E2a's at SCRATCH-E2A/
and, while J2a (inventory137, E2a's parent) is not integrated, J2a's at
SCRATCH-J2A/. They are served in memory by patching the design_preflight
module that generate_contracts loads, as I1-a's drift_scratch_i1a.py did. In
the staged worktree the lock must equal verify_scratch.py's staged lock;
otherwise that lock is applied in memory. Every closure,
toolchain, receipt, options and tool-byte check runs unchanged. Nothing is
written to either repository. It exits 0 only when the gate passes with
changed: [].
Usage: drift_scratch_e2a.py CHECKOUT OUTPUT_DIR (must not exist; the pipeline creates it)"""
import argparse, hashlib, importlib.util, json, sys
from pathlib import Path
W = Path(sys.argv[1]).resolve(strict=True); A = Path('/Users/sb/code/opensip-ai/opensip_arch'); S = Path(sys.argv[2])
here = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('scratch', here / 'verify_scratch.py'); s = importlib.util.module_from_spec(spec); spec.loader.exec_module(s)
spec = importlib.util.spec_from_file_location('gc', W / 'tools/generate_contracts.py'); gc = importlib.util.module_from_spec(spec); spec.loader.exec_module(gc)
orig = gc.module
state = {}
def patched(path, name):
    m = orig(path, name)
    if name != 'design_preflight': return m
    real_verify, real_pinned = m.verify, m.pinned_bytes
    def verify(architecture, lock, implementation=None):
        base = s.head_lock(W)
        _, staged_lock, synthetic, _ = s.scenario(base)
        if lock['inventorySuccessors'][-1]['candidate']['path'] == s.CANDIDATE:
            assert lock == staged_lock, 'staged E2a lock differs'; state['mode'] = 'staged'
        else:
            assert lock == base, 'the lock is neither HEAD nor the staged E2a lock'; lock = staged_lock; state['mode'] = 'appended'
        def pinned_bytes(root, row):
            if isinstance(row, dict) and row.get('path') in synthetic:
                data = synthetic[row['path']]; assert hashlib.sha256(data).hexdigest() == row['sha256'] and len(data) == row['bytes']; return data
            return real_pinned(root, row)
        m.pinned_bytes = pinned_bytes
        return real_verify(architecture, lock, implementation)
    m.verify = verify
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
