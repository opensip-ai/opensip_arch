"""Scratch-only: write a lock that selects inventory83 (unit X3a-1) over the
real product lock (which selects inventory82), with inventory83's re-projected
inheritance, so verify_projection.py can run before inventory83 is
integrated. It is written outside both repositories. The inventory83 review
and assent pins are placeholders that verify_projection.py never reads.
Usage: scratch_lock.py PRODUCT_LOCK OUT."""
import hashlib, json, sys
from pathlib import Path
A = Path('/Users/sb/code/opensip-ai/opensip_arch')
M = 'docs/implementation/m2/'
def pin(p): b = (A / p).read_bytes(); return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
lock = json.loads(Path(sys.argv[1]).read_text())
parent, candidate = pin(M + 'repository-file-inventory.v82.json'), pin(M + 'repository-file-inventory.v83.json')
assert lock['inventorySuccessors'][-1]['candidate'] == parent, 'the lock must select inventory82'
record = pin(M + 'store-endpoint-inventory-v83/successor.json')
placeholder = {'path': 'SCRATCH-X3A1/unread.json', 'bytes': 0, 'sha256': hashlib.sha256(b'').hexdigest()}
lock['inventorySuccessors'].append({'parent': parent, 'candidate': candidate, 'record': record, 'review': placeholder, 'assent': placeholder})
rows = json.loads((A / record['path']).read_text())['descriptionOverrideProjection']
lock['inventoryPassageInheritance'] = sorted(
    ({'parent': candidate, 'selector': r['candidateSelector'], 'before': r['before'], 'after': r['effectiveDescription']} for r in rows),
    key=lambda o: json.dumps(o['selector'], sort_keys=True))
Path(sys.argv[2]).write_text(json.dumps(lock, indent=2) + '\n')
