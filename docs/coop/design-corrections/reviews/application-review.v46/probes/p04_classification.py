import json, hashlib, os
S46 = '/private/tmp/opensip-design-corrections/application-stage.v46/files/'
S45 = '/private/tmp/opensip-design-corrections/application-stage.v45.2/files/'
p = 'docs/operations/document-classification.v1.json'
a = json.load(open(S45 + p)); b = json.load(open(S46 + p))
print('top45', {k: (len(v) if isinstance(v, (list, dict)) else v) for k, v in a.items()})
print('top46', {k: (len(v) if isinstance(v, (list, dict)) else v) for k, v in b.items()})
for k in a:
    if a[k] == b.get(k): continue
    va, vb = a[k], b[k]
    if isinstance(va, list) and va and isinstance(va[0], dict):
        print('list key', k, 'sample keys', list(va[0].keys()))
        kk = 'path' if 'path' in va[0] else list(va[0].keys())[0]
        da = {x[kk]: x for x in va}; db = {x[kk]: x for x in vb}
        added = sorted(set(db) - set(da)); removed = sorted(set(da) - set(db))
        ch = [q for q in da if q in db and da[q] != db[q]]
        print(k, 'len', len(va), len(vb), 'added', len(added), 'removed', len(removed), 'changed', len(ch))
        fields = {}
        for q in ch:
            for f in set(da[q]) | set(db[q]):
                if da[q].get(f) != db[q].get(f): fields[f] = fields.get(f, 0) + 1
        print(' changed fields', fields)
        for q in ch[:3]:
            print('  ex', q, {f: (da[q].get(f), db[q].get(f)) for f in fields if da[q].get(f) != db[q].get(f)})
        print(' added sample', added[:10]); print(' removed sample', removed[:10])
        json.dump({'added': added, 'removed': removed, 'changed': {q: {f: [da[q].get(f), db[q].get(f)] for f in fields if da[q].get(f) != db[q].get(f)} for q in ch}}, open('/private/tmp/opensip-design-corrections/application-review.v46/probes/out/p04_class_' + k + '.json', 'w'), indent=1)
    elif isinstance(va, dict):
        ks = [x for x in set(va) | set(vb) if va.get(x) != vb.get(x)]
        print('dict key', k, 'changed subkeys', len(ks), ks[:20])
        for x in ks[:20]:
            print('  ', x, repr(va.get(x))[:300], '=>', repr(vb.get(x))[:300])
    else:
        print('scalar', k, repr(va)[:300], '=>', repr(vb)[:300])
