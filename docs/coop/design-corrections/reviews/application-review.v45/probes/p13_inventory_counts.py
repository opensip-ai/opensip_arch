import json, collections
S = '/private/tmp/opensip-design-corrections/application-stage.v45.2/files/'
inv = json.load(open(S + 'docs/operations/document-inventory.v1.json'))
wd = inv['workingTreeDelta']
print('workingTreeDelta keys', list(wd.keys()))
for k, v in wd.items():
    print(' ', k, (len(v) if isinstance(v, list) else json.dumps(v)[:600]))
for h in inv['workingTreeDeltaHistory']:
    print(' history', h.get('date'), h.get('decision'), 'added', len(h.get('addedPaths') or []), 'refreshed', len(h.get('refreshedContentPaths') or []), (h.get('meaning') or '')[:300])
rows = inv['files']
scoped = [r for r in rows if 'referenceAccountingScope' in r]
print('rows', len(rows), 'rows with referenceAccountingScope', len(scoped), collections.Counter(r['referenceAccountingScope'][:60] for r in scoped).most_common(5))
print('rows with currentNavigationReferences', sum(1 for r in rows if 'currentNavigationReferences' in r))
print('rows without sha', sum(1 for r in rows if not r.get('sha256')))
print('keys union', sorted(set().union(*[set(r) for r in rows])))
# numbers 126015 / 135218
cands = {}
for k, v in inv.items():
    if isinstance(v, int): cands[k] = v
print('int fields', cands)
for r in rows:
    pass
cp = set(wd.get('contentPaths') or [])
print('contentPaths', len(cp), 'present in rows', sum(1 for r in rows if r['path'] in cp))
cls = json.load(open(S + 'docs/operations/document-classification.v1.json'))
print('classification counts sum', sum(cls['counts'].values()))
print('current/architecture rows', sorted(r['path'] for r in cls['files'] if r['classification'] == 'current/architecture'))
print('current/navigation rows', sorted(r['path'] for r in cls['files'] if r['classification'] == 'current/navigation'))
# find '126015' anywhere in support
import os
for root, ds, fs in os.walk('/private/tmp/opensip-design-corrections/application-stage.v45.2/support'):
    for f in fs:
        p = os.path.join(root, f)
        try:
            t = open(p, encoding='utf-8', errors='ignore').read()
        except Exception:
            continue
        if '126015' in t or '126,015' in t:
            i = t.find('126015')
            print('126015 in', p[len('/private/tmp/opensip-design-corrections/application-stage.v45.2/'):], t[max(0, i - 300): i + 200].replace('\n', ' '))
