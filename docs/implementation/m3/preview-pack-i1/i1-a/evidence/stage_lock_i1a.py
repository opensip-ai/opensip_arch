"""Stage I1-a's binding in a product worktree, as F8b and P0 staged theirs:
append the I1-a contractSuccessors entry to HEAD's design-lock.json. The record
and subject pins are real; the review and assent pins are the SCRATCH-I1A/
placeholders whose bytes and sha256 are those of verify_scratch_i1a.py's
synthetic overlay. At integration the lead replaces exactly those two pins with
the accepted review-contract.json and the completed unit record. There is no
inventory successor, so the inventory chain and inheritance are unchanged.

It writes only the worktree's design-lock.json, in the lock's canonical
formatting, and refuses unless that file is HEAD's lock or already this exact
staged lock. Rerunning reproduces the same bytes.
Usage: stage_lock_i1a.py [WORKTREE]"""
import importlib.util, json, sys
from pathlib import Path
spec = importlib.util.spec_from_file_location('scratch', Path(__file__).resolve().parent / 'verify_scratch_i1a.py')
s = importlib.util.module_from_spec(spec); spec.loader.exec_module(s)
W = Path(sys.argv[1] if len(sys.argv) > 1 else '/Users/sb/code/opensip-ai/opensip-i1a').resolve(strict=True)
path = W / 'design-lock.json'
base = s.head_lock(W)
lock = s.staged(base)
assert path.read_text() in (s.canonical(base), s.canonical(lock)), 'the worktree lock is neither HEAD nor the staged I1-a lock'
path.write_text(s.canonical(lock))
entry = lock['contractSuccessors'][-1]
print(json.dumps({'contractSuccessors': len(lock['contractSuccessors']), 'inventorySuccessors': len(lock['inventorySuccessors']),
                  'inventoryPassageInheritance': len(lock['inventoryPassageInheritance']), 'entry': entry}, indent=1))
