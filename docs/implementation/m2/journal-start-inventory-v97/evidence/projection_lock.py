"""Scratch-only: write to OUT (outside both repositories) the product lock
that verify_projection.py checks inventory97 against: the real lock, which
selects inventory94, with inventory96's successor row (placeholder review and
assent pins, which verify_projection never reads) and its sixteen
inheritance rows re-projected onto inventory96. Once the real lock selects
inventory96 it is copied unchanged. Usage: projection_lock.py LOCK OUT."""
import hashlib, json, sys
from pathlib import Path
A = Path('/Users/sb/code/opensip-ai/opensip_arch')
M = 'docs/implementation/m2/'
def pin(p): b = (A / p).read_bytes(); return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
lock_path, out = Path(sys.argv[1]), Path(sys.argv[2])
assert not out.resolve().is_relative_to(A), 'OUT must be outside the architecture repository'
lock = json.loads(lock_path.read_bytes())
v94, v96 = pin(M + 'repository-file-inventory.v94.json'), pin(M + 'repository-file-inventory.v96.json')
selected = lock['inventorySuccessors'][-1]['candidate']
assert selected in (v94, v96), 'the lock must select inventory94 or inventory96'
if selected == v94:
    record = pin(M + 'current-trust-inventory-v96/successor.json')
    placeholder = {'path': 'SCRATCH-X3B1B/unread', 'bytes': 0, 'sha256': hashlib.sha256(b'').hexdigest()}
    lock['inventorySuccessors'].append({'parent': v94, 'candidate': v96, 'record': record, 'review': placeholder, 'assent': placeholder})
    rows = json.loads((A / record['path']).read_bytes())['descriptionOverrideProjection']
    lock['inventoryPassageInheritance'] = sorted(
        ({'parent': v96, 'selector': r['candidateSelector'], 'before': r['before'], 'after': r['effectiveDescription']} for r in rows),
        key=lambda o: json.dumps(o['selector'], sort_keys=True))
out.write_text(json.dumps(lock, indent=2) + '\n')
