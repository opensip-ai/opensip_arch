"""Stage unit J3a's lock change in a product worktree, as E2a staged
inventory138: HEAD's design-lock.json (product b7b87b7, which selects
inventory138) plus the inventory139 entry, with the inheritance replaced by
the one hundred and three rows re-parented to inventory139. The record, candidate,
subject and parent pins are real; J3a's review and assent pins are the
SCRATCH-J3A/ placeholders whose bytes and sha256 are those of
evidence/verify_scratch.py's synthetic overlay. At integration the lead
replaces exactly J3a's two placeholder pins with the accepted review and the
completed unit record. The lock has no separate
selected-inventory field: selection is the last inventory successor.

It writes only the worktree's design-lock.json, in the lock's canonical
formatting, and refuses unless that file is HEAD's lock or already this
exact staged lock. Rerunning reproduces the same bytes.
Usage: stage_lock_j3a.py [WORKTREE]."""
import importlib.util, json, sys
from pathlib import Path
spec = importlib.util.spec_from_file_location('scratch', Path(__file__).resolve().parent / 'verify_scratch.py')
s = importlib.util.module_from_spec(spec); spec.loader.exec_module(s)
W = Path(sys.argv[1] if len(sys.argv) > 1 else '/Users/sb/code/opensip-ai/opensip-j3a').resolve(strict=True)
path = W / 'design-lock.json'
base = s.head_lock(W)
assert path.read_text() == s.canonical(base) or path.read_text() == s.canonical(s.staged(base)), 'the worktree lock is neither HEAD nor the staged J3a lock'
lock = s.staged(base)
path.write_text(s.canonical(lock))
print(json.dumps({'inventorySuccessors': len(lock['inventorySuccessors']), 'contractSuccessors': len(lock['contractSuccessors']),
                  'inventoryPassageInheritance': len(lock['inventoryPassageInheritance']),
                  'entries': [{'candidate': e['candidate']['path'], 'review': e['review'], 'assent': e['assent']}
                              for e in lock['inventorySuccessors'] if e['review']['path'].startswith('SCRATCH-')]}, indent=1))
