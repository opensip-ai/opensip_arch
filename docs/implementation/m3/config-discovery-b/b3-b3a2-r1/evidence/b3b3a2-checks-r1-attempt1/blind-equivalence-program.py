import importlib.util, json, os, sys
from pathlib import Path
W, A, P, CACHE = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), sys.argv[4]
spec = importlib.util.spec_from_file_location('discovery_census', W / 'tools/security/discovery_census.py')
census = importlib.util.module_from_spec(spec); spec.loader.exec_module(census)
c = census.costs(W)
wv, ref, slm, rule = census.load_reference(W, A, P)
measure = census.blind_measure(c, census.load_member_model(W), rule, lambda tree: census.reference_population(wv, ref, slm, rule, tree))
manifest = json.loads((A / census.MANIFEST).read_bytes())
record = {e['id']: e for e in json.loads((W / census.OUTPUT_CENSUS).read_bytes())['entries']}
rows = []
for entry in manifest['repositories']:
    if entry['heldOut'] is not False:
        continue
    row = census.blind_row(dict(entry, heldOut=True), os.path.join(CACHE, 'store'), c, measure)
    full = record[entry['id']]['d15']['fullLedger']
    expected = dict(id=entry['id'], status='measured', integrity=True, population=True,
                    marginPermille=dict(objects=full['objectMarginPermille'], edges=full['edgeMarginPermille'],
                                        bytes=full['byteMarginPermilleAt'][str(census.ROOT_LENGTHS[-1])]), passes2x=full['passes2x'])
    rows.append(dict(id=entry['id'], equal=row == expected, row=row))
    print(entry['id'], row == expected, flush=True)
print(json.dumps(dict(rows=rows, allEqual=all(r['equal'] for r in rows) and len(rows) > 0)))
sys.exit(0 if rows and all(r['equal'] for r in rows) else 1)
