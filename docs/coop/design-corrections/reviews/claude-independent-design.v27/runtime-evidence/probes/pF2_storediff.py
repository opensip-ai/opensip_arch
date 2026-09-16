"""PROBE F2 (v27) — audit WHY freshly built store files differ byte-wise from the shipped
ones even though every RunId reproduces exactly. A semantic difference would be serious;
a transport/meta difference is not. I decide it by measurement, not assumption."""
import base64, glob, hashlib, json, os

PKG = '/tmp/opensip-design-corrections/claude-author-package-successor.v4'
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v27/receipts'
arb = sorted(glob.glob('/tmp/indep27-arbitrary-*/deep/nested/elsewhere'))[-1]
res = {'arbitraryRoot': arb}

PAIRS = [
    (os.path.join(arb, 'a-checkpoint3/checkpoint3/ts.store.json'),
     os.path.join(PKG, 'checkpoint3/ts.store.json')),
    (os.path.join(arb, 'b-normalized/normalized-examples6/rust.store.json'),
     os.path.join(PKG, 'normalized-examples6/rust.store.json')),
    (os.path.join(arb, 'd-controls/semantic-controls1/severity.store.json'),
     os.path.join(PKG, 'semantic-controls1/severity.store.json')),
]
rows = []
for fresh, shipped in PAIRS:
    a = json.load(open(fresh))
    b = json.load(open(shipped))
    row = {'file': os.path.relpath(shipped, PKG),
           'topKeysFresh': sorted(a), 'topKeysShipped': sorted(b),
           'sameTopKeys': sorted(a) == sorted(b)}
    for k in sorted(set(a) | set(b)):
        same = a.get(k) == b.get(k)
        row['key_' + k + '_identical'] = same
        if not same and k == 'meta':
            row['metaFresh'] = a.get('meta')
            row['metaShipped'] = b.get('meta')
    # semantic content comparison independent of transport
    for k in ('objectTable', 'blobs', 'frames'):
        if k in a and k in b:
            row[k + '_countFresh'] = len(a[k])
            row[k + '_countShipped'] = len(b[k])
            row[k + '_keysIdentical'] = set(a[k]) == set(b[k])
            if k == 'blobs':
                row['blobs_bytesIdentical'] = all(
                    base64.b64decode(a[k][d]) == base64.b64decode(b[k][d])
                    for d in set(a[k]) & set(b[k]))
            else:
                row[k + '_valuesIdentical'] = all(a[k][x] == b[k][x] for x in set(a[k]) & set(b[k]))
    rows.append(row)
res['comparisons'] = rows
for r in rows:
    print('###', r['file'])
    for k, v in r.items():
        if k == 'file':
            continue
        print('    %-34s %s' % (k, json.dumps(v)[:200]))
    print()

# where do the binding-control stores live in the fresh tree?
bc = os.path.join(arb, 'e-binding-controls')
listing = []
for dp, dn, fn in os.walk(bc):
    for n in sorted(fn):
        listing.append(os.path.relpath(os.path.join(dp, n), bc))
res['freshBindingControlsListing'] = listing
print('fresh binding-controls files:', listing)

# compare binding-control stores explicitly
bcmp = []
for n in listing:
    fp = os.path.join(bc, n)
    sp = os.path.join(PKG, 'binding-controls', os.path.basename(n))
    if os.path.isfile(sp):
        fa = hashlib.sha256(open(fp, 'rb').read()).hexdigest()
        sb = hashlib.sha256(open(sp, 'rb').read()).hexdigest()
        bcmp.append({'file': os.path.basename(n), 'identical': fa == sb})
res['bindingControlComparison'] = bcmp
print('binding-control comparison:', json.dumps(bcmp))
json.dump(res, open(os.path.join(OUT, 'pF2-storediff.json'), 'w'), indent=1)
