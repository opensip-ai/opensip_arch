"""Stage unit I1-c's lock change in a product worktree, as E2a staged
inventory138: HEAD's design-lock.json plus, while J3a is not integrated,
J3a's inventory139 entry exactly as its own stage_lock_j3a.py writes it
(SCRATCH-J3A placeholders), then the inventory140 entry, with the inheritance
replaced by the one hundred and three rows re-parented to inventory140. The
record, candidate, subject and parent pins are real; I1-c's review and assent
pins are the SCRATCH-I1C/ placeholders whose bytes and sha256 are those of
evidence/verify_scratch.py's synthetic overlay. At integration, after J3a
is integrated, the lead re-stages on the real lock (which then adds only
I1-c's entry) and replaces exactly I1-c's two placeholder pins with the
accepted review and the completed unit record. The lock has no separate
selected-inventory field: selection is the last inventory successor.

It writes only the worktree's design-lock.json, in the lock's canonical
formatting, and refuses unless that file is HEAD's lock or already this
exact staged lock. Rerunning reproduces the same bytes.
Usage: stage_lock_i1c.py [WORKTREE]."""
import importlib.util, json, sys
from pathlib import Path
spec = importlib.util.spec_from_file_location('scratch', Path(__file__).resolve().parent / 'verify_scratch.py')
s = importlib.util.module_from_spec(spec); spec.loader.exec_module(s)
W = Path(sys.argv[1] if len(sys.argv) > 1 else '/Users/sb/code/opensip-ai/opensip-i1c').resolve(strict=True)
path = W / 'design-lock.json'
base = s.head_lock(W)
assert path.read_text() == s.canonical(base) or path.read_text() == s.canonical(s.staged(base)), 'the worktree lock is neither HEAD nor the staged I1-c lock'
lock = s.staged(base)
path.write_text(s.canonical(lock))
print(json.dumps({'inventorySuccessors': len(lock['inventorySuccessors']), 'contractSuccessors': len(lock['contractSuccessors']),
                  'inventoryPassageInheritance': len(lock['inventoryPassageInheritance']),
                  'entries': [{'candidate': e['candidate']['path'], 'review': e['review'], 'assent': e['assent']}
                              for e in lock['inventorySuccessors'] if e['review']['path'].startswith('SCRATCH-')]}, indent=1))
