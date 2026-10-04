"""Stage unit X3a-2's lock change in a product worktree, as P0 staged
inventory135: append the inventory136 entry to HEAD's design-lock.json,
replace the inheritance with the one hundred rows re-parented to
inventory136, and append the description successor
(read-endpoint-x3a2-descriptions) as the last contract successor. The
record, candidate, subject and parent pins are real; the four review and
assent pins are the SCRATCH-X3A2/ placeholders whose bytes and sha256 are
those of evidence/verify_scratch.py's synthetic overlay. At integration the
lead replaces exactly those four pins with the accepted reviews and the
completed unit records. The lock has no separate selected-inventory field:
selection is the last inventory successor.

It writes only the worktree's design-lock.json, in the lock's canonical
formatting, and refuses unless that file is HEAD's lock or already this
exact staged lock. Rerunning reproduces the same bytes.
Usage: stage_lock_x3a2.py [WORKTREE]."""
import importlib.util, json, sys
from pathlib import Path
spec = importlib.util.spec_from_file_location('scratch', Path(__file__).resolve().parent / 'verify_scratch.py')
s = importlib.util.module_from_spec(spec); spec.loader.exec_module(s)
W = Path(sys.argv[1] if len(sys.argv) > 1 else '/Users/sb/code/opensip-ai/opensip-x3a2').resolve(strict=True)
path = W / 'design-lock.json'
base = s.head_lock(W)
assert path.read_text() == s.canonical(base) or path.read_text() == s.canonical(s.staged(base)), 'the worktree lock is neither HEAD nor the staged X3a-2 lock'
lock = s.staged(base)
path.write_text(s.canonical(lock))
inventory, descriptions = lock['inventorySuccessors'][-1], lock['contractSuccessors'][-1]
print(json.dumps({'inventorySuccessors': len(lock['inventorySuccessors']), 'contractSuccessors': len(lock['contractSuccessors']),
                  'inventoryPassageInheritance': len(lock['inventoryPassageInheritance']),
                  'inventory': {'review': inventory['review'], 'assent': inventory['assent']},
                  'descriptions': {'review': descriptions['review'], 'assent': descriptions['assent']}}, indent=1))
