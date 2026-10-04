"""Stage unit E2a's lock change in a product worktree, as X3a-2 staged
inventory136: HEAD's design-lock.json plus, while J2a is not integrated,
J2a's inventory137 entry exactly as its own stage_lock_j2a.py writes it
(SCRATCH-J2A placeholders), then the inventory138 entry, with the inheritance
replaced by the one hundred and three rows re-parented to inventory138. The
record, candidate, subject and parent pins are real; E2a's review and assent
pins are the SCRATCH-E2A/ placeholders whose bytes and sha256 are those of
evidence/verify_scratch.py's synthetic overlay. At integration, after J2a
is integrated, the lead re-stages on the real lock (which then adds only
E2a's entry) and replaces exactly E2a's two placeholder pins with the
accepted review and the completed unit record. The lock has no separate
selected-inventory field: selection is the last inventory successor.

It writes only the worktree's design-lock.json, in the lock's canonical
formatting, and refuses unless that file is HEAD's lock or already this
exact staged lock. Rerunning reproduces the same bytes.
Usage: stage_lock_e2a.py [WORKTREE]."""
import importlib.util, json, sys
from pathlib import Path
spec = importlib.util.spec_from_file_location('scratch', Path(__file__).resolve().parent / 'verify_scratch.py')
s = importlib.util.module_from_spec(spec); spec.loader.exec_module(s)
W = Path(sys.argv[1] if len(sys.argv) > 1 else '/Users/sb/code/opensip-ai/opensip-e2a').resolve(strict=True)
path = W / 'design-lock.json'
base = s.head_lock(W)
assert path.read_text() == s.canonical(base) or path.read_text() == s.canonical(s.staged(base)), 'the worktree lock is neither HEAD nor the staged E2a lock'
lock = s.staged(base)
path.write_text(s.canonical(lock))
print(json.dumps({'inventorySuccessors': len(lock['inventorySuccessors']), 'contractSuccessors': len(lock['contractSuccessors']),
                  'inventoryPassageInheritance': len(lock['inventoryPassageInheritance']),
                  'entries': [{'candidate': e['candidate']['path'], 'review': e['review'], 'assent': e['assent']}
                              for e in lock['inventorySuccessors'] if e['review']['path'].startswith('SCRATCH-')]}, indent=1))
