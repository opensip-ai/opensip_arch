"""Write, outside both repositories, the design lock inventory83's projection
is checked against: the live product lock (inventory81 selected) with X10b and
inventory82 applied as integration would apply them. X10b's review and
assent are placeholders; verify_projection.py reads only successor records
and inheritance rows, never reviews. Usage: scratch_lock.py PRODUCT OUT."""
import hashlib, json, sys
from pathlib import Path
A = Path(__file__).resolve().parents[5]
M = 'docs/implementation/m2/'
product, out = Path(sys.argv[1]), Path(sys.argv[2])
assert not str(out.resolve()).startswith((str(A), str(product.resolve()))), 'scratch output only'
def pin(p):
    b = (A / p).read_bytes(); return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
lock = json.loads((product / 'design-lock.json').read_text())
placeholder = {'path': 'SCRATCH/placeholder.json', 'bytes': 0, 'sha256': hashlib.sha256(b'').hexdigest()}
lock['contractSuccessors'].append({'record': pin(M + 'read-cli-x10b/successor.json'),
    'subjectManifest': pin(M + 'read-cli-x10b-subject.json'), 'review': placeholder, 'assent': placeholder})
parent, candidate = pin(M + 'repository-file-inventory.v81.json'), pin(M + 'repository-file-inventory.v82.json')
record = pin(M + 'read-cli-inventory-v82/successor.json')
lock['inventorySuccessors'].append({'parent': parent, 'candidate': candidate, 'record': record,
    'review': placeholder, 'assent': placeholder})
rows = json.loads((A / record['path']).read_text())['descriptionOverrideProjection']
lock['inventoryPassageInheritance'] = sorted(
    ({'parent': candidate, 'selector': r['candidateSelector'], 'before': r['before'], 'after': r['effectiveDescription']} for r in rows),
    key=lambda o: json.dumps(o['selector'], sort_keys=True))
out.write_text(json.dumps(lock, indent=2) + '\n')
print(json.dumps({'inventorySuccessors': len(lock['inventorySuccessors']), 'inheritance': len(lock['inventoryPassageInheritance'])}))
