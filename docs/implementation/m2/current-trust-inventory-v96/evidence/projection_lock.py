"""Scratch-only: write to OUT (outside both repositories) the product lock
that verify_projection.py checks inventory96 against. While the real lock
still selects inventory93, inventory94's successor row (with placeholder
review and assent pins, which verify_projection never reads) and its
re-projected inheritance are appended; once the real lock selects inventory94
it is copied unchanged. Usage: projection_lock.py LOCK OUT."""
import hashlib, json, sys
from pathlib import Path
A = Path('/Users/sb/code/opensip-ai/opensip_arch')
M = 'docs/implementation/m2/'
def pin(p): b = (A / p).read_bytes(); return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
lock_path, out = Path(sys.argv[1]), Path(sys.argv[2])
assert not out.resolve().is_relative_to(A), 'OUT must be outside the architecture repository'
lock = json.loads(lock_path.read_bytes())
v93, v94 = pin(M + 'repository-file-inventory.v93.json'), pin(M + 'repository-file-inventory.v94.json')
selected = lock['inventorySuccessors'][-1]['candidate']
assert selected in (v93, v94), 'the lock must select inventory93 or inventory94'
if selected == v93:
    record = pin(M + 'ledger-creation-inventory-v94/successor.json')
    placeholder = {'path': 'SCRATCH-X4TA/unread', 'bytes': 0, 'sha256': hashlib.sha256(b'').hexdigest()}
    lock['inventorySuccessors'].append({'parent': v93, 'candidate': v94, 'record': record, 'review': placeholder, 'assent': placeholder})
    rows = json.loads((A / record['path']).read_bytes())['descriptionOverrideProjection']
    lock['inventoryPassageInheritance'] = sorted(
        ({'parent': v94, 'selector': r['candidateSelector'], 'before': r['before'], 'after': r['effectiveDescription']} for r in rows),
        key=lambda o: json.dumps(o['selector'], sort_keys=True))
out.write_text(json.dumps(lock, indent=2) + '\n')
print(json.dumps({'appendedInventory94': selected == v93}))
