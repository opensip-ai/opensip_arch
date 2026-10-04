"""Stage unit J2a's lock change in a product worktree, as P0 staged
inventory137: append the inventory137 entry to HEAD's design-lock.json and
replace the inheritance with the one hundred and three rows re-parented to
inventory137. The record, candidate and parent pins are real; the review and
assent pins are the SCRATCH-J2A/ placeholders whose bytes and sha256 are those
of evidence/verify_scratch.py's synthetic overlay. At integration the lead
replaces exactly those two pins with the accepted review and the completed
unit record. The lock has no separate selected-inventory field: selection is
the last inventory successor.

It writes only the worktree's design-lock.json, in the lock's canonical
formatting, and refuses unless that file is HEAD's lock or already this
exact staged lock. Rerunning reproduces the same bytes.
Usage: stage_lock_j2a.py [WORKTREE]."""
import importlib.util, json, sys
from pathlib import Path
spec = importlib.util.spec_from_file_location('scratch', Path(__file__).resolve().parent / 'verify_scratch.py')
s = importlib.util.module_from_spec(spec); spec.loader.exec_module(s)
W = Path(sys.argv[1] if len(sys.argv) > 1 else '/Users/sb/code/opensip-ai/opensip-j2a').resolve(strict=True)
path = W / 'design-lock.json'
base = s.head_lock(W)
assert path.read_text() == s.canonical(base) or path.read_text() == s.canonical(s.staged(base)), 'the worktree lock is neither HEAD nor the staged inventory137 lock'
lock = s.staged(base)
path.write_text(s.canonical(lock))
entry = lock['inventorySuccessors'][-1]
print(json.dumps({'inventorySuccessors': len(lock['inventorySuccessors']), 'inventoryPassageInheritance': len(lock['inventoryPassageInheritance']),
                  'review': entry['review'], 'assent': entry['assent']}, indent=1))
