
import json, os, sys
from pathlib import Path
P = Path.cwd(); sys.path.insert(0, str(P / 'tools/security'))
import importlib.util
spec = importlib.util.spec_from_file_location('slc', P / 'tools/security/snapshot_ledger_census.py'); slc = importlib.util.module_from_spec(spec); spec.loader.exec_module(slc)
census = slc.Census(P, Path(sys.argv[1]), Path(sys.argv[2]))
record = json.loads((P / slc.OUTPUT).read_bytes()); rows = {r['id']: r for r in record['entries']}
manifest = json.loads((Path(sys.argv[1]) / census.dc.MANIFEST).read_bytes()); store = os.path.join(sys.argv[3], 'store')
out = []
for entry in manifest['repositories']:
    if entry['heldOut'] is not False:
        continue  # never a held-out store: only the lead-readable ones, each presented to the blind row as held out
    blind = census.blind_row(dict(entry, heldOut=True), store, census.dc._BLIND)
    row = rows[entry['id']]
    if row['status'] == 'over-item-5':
        ok = blind == dict(id=entry['id'], status='over-item-5', integrity=True, population=True)
    else:
        m = row['margins'][slc.PROFILE]
        ok = blind == dict(id=entry['id'], status='measured', integrity=True, population=True,
                           marginPermille={k: m[k]['marginPermille'] for k in slc.KEYS}, passes2x=m['passes2x'])
    out.append(dict(id=entry['id'], status=blind['status'], equal=ok))
    print(entry['id'], blind['status'], ok, flush=True)
json.dump(dict(rows=out, allEqual=all(r['equal'] for r in out), count=len(out)), open(sys.argv[4], 'w'), indent=2)
sys.exit(0 if out and all(r['equal'] for r in out) else 1)
