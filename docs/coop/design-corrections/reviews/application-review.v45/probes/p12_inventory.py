import json, collections, hashlib
S = '/private/tmp/opensip-design-corrections/application-stage.v45.2/'
m = json.load(open(S + 'application-subject.v45.json'))
staged = {e['path']: e for e in m['files']}
for name in ['docs/operations/document-inventory.v1.json', 'docs/operations/document-classification.v1.json']:
    d = json.load(open(S + 'files/' + name))
    print('=====', name)
    for k, v in d.items():
        if isinstance(v, list):
            print(' ', k, 'list', len(v), 'row keys', sorted(v[0].keys()) if v and isinstance(v[0], dict) else '')
        elif isinstance(v, dict):
            print(' ', k, 'dict', len(v), json.dumps(v)[:1500])
        else:
            print(' ', k, '=', json.dumps(v)[:1500])
    rows = d.get('files') or []
    bypath = {r['path']: r for r in rows}
    cls = collections.Counter(r.get('classification') for r in rows)
    print('  classification counts', cls.most_common(30))
    for key in ['scope', 'scoped', 'inScope', 'status']:
        c = collections.Counter(str(r.get(key)) for r in rows)
        if len(c) > 1 or 'None' not in c: print('  field', key, c.most_common(10))
    # check staged paths recorded hashes
    mism = []
    for p, e in staged.items():
        r = bypath.get(p)
        if r is None: mism.append((p, 'ABSENT')); continue
        h = r.get('sha256')
        if h is not None and h != e['sha256']:
            mism.append((p, 'recorded', h[:12], 'before' if h == e['beforeSha256'] else 'other'))
    print('  staged paths not matching recorded sha', len(mism))
    for x in mism[:60]: print('    ', x)
    for p in ['docs/START-HERE.md', 'docs/v2/architecture/08-decision-and-readiness-register.md', 'docs/coop/design-corrections/application.v1.json', 'docs/operations/document-inventory.v1.json']:
        r = bypath.get(p)
        print('  ROW', p, json.dumps(r)[:1200] if r else None)
