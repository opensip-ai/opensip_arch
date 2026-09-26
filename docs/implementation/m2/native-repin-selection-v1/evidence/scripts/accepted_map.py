"""Read-only: rebuild verify_design's 'accepted' path map from a lock (no hashing), and
find accepted arch paths whose pins equal given product files."""
import json, hashlib, sys
from pathlib import Path
ARCH = Path(sys.argv[1]); LOCK = Path(sys.argv[2]); PRODUCT = Path(sys.argv[3]); files = sys.argv[4:]
lock = json.loads(LOCK.read_bytes())
acc = {}
for name in ('sourceManifest', 'applicationManifest'):
    for row in json.loads((ARCH / lock['approvals'][name]['path']).read_bytes())['files']:
        acc[row['path']] = row
for b in lock['inventorySuccessors']:
    acc.setdefault(b['parent']['path'], b['parent']); acc[b['candidate']['path']] = b['candidate']
for b in lock['contractSuccessors']:
    rec = json.loads((ARCH / b['record']['path']).read_bytes())
    for row in [b['record'], *rec['candidates']]:
        acc[row['path']] = row
print('contractSuccessors', len(lock['contractSuccessors']), 'accepted', len(acc))
for f in files:
    raw = (PRODUCT / f).read_bytes(); s = hashlib.sha256(raw).hexdigest()
    hits = [p for p, r in acc.items() if r['sha256'] == s and r['bytes'] == len(raw)]
    print(f, len(raw), s[:12], hits)
