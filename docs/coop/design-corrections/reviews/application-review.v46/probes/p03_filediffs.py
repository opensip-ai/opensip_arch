import json, hashlib, os, difflib, sys
S46 = '/private/tmp/opensip-design-corrections/application-stage.v46'
S45 = '/private/tmp/opensip-design-corrections/application-stage.v45.2'
OUT = '/private/tmp/opensip-design-corrections/application-review.v46/probes/out'
os.makedirs(OUT, exist_ok=True)
m45 = json.load(open('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/application-subject.v45.json'))
f45 = {e['path']: e['sha256'] for e in m45['files']}

def get45(p):
    b = open(os.path.join(S45, 'files', p), 'rb').read()
    assert hashlib.sha256(b).hexdigest() == f45[p], p
    return b

def jdiff(a, b, path='', acc=None):
    if acc is None: acc = []
    if type(a) != type(b):
        acc.append((path, a, b)); return acc
    if isinstance(a, dict):
        for k in sorted(set(a) | set(b), key=str):
            if k not in a: acc.append((path + '/' + str(k), '<ABSENT>', b[k]))
            elif k not in b: acc.append((path + '/' + str(k), a[k], '<ABSENT>'))
            else: jdiff(a[k], b[k], path + '/' + str(k), acc)
    elif isinstance(a, list):
        if len(a) != len(b):
            # try element-wise for common prefix, then report tail
            for i in range(min(len(a), len(b))): jdiff(a[i], b[i], path + '/' + str(i), acc)
            acc.append((path + '/#len', len(a), len(b)))
            for i in range(min(len(a), len(b)), max(len(a), len(b))):
                acc.append((path + '/' + str(i), a[i] if i < len(a) else '<ABSENT>', b[i] if i < len(b) else '<ABSENT>'))
        else:
            for i in range(len(a)): jdiff(a[i], b[i], path + '/' + str(i), acc)
    elif a != b:
        acc.append((path, a, b))
    return acc

for p in ['docs/coop/design-corrections/readiness-row-map.v1.json', 'docs/coop/design-corrections/inherited-residuals.applied.v1.json', 'docs/coop/design-corrections/application.v1.json', 'docs/coop/design-corrections/accepted-review-advisories.v1.json', 'docs/coop/design-corrections/workflows/workflows-report.v1.json', 'docs/operations/document-classification.v1.json']:
    a = json.loads(get45(p)); b = json.load(open(os.path.join(S46, 'files', p)))
    d = jdiff(a, b)
    with open(os.path.join(OUT, 'p03_' + os.path.basename(p) + '.diff.json'), 'w') as fh:
        json.dump([{'ptr': x[0], 'v45': x[1], 'v46': x[2]} for x in d], fh, indent=1)
    print(p, 'diffLeaves', len(d))

for p in ['docs/v2/architecture/08-decision-and-readiness-register.md', 'docs/coop/COORDINATOR-DECISIONS.md', 'docs/catalog/current-design.md']:
    a = get45(p).decode().splitlines(); b = open(os.path.join(S46, 'files', p)).read().splitlines()
    ud = list(difflib.unified_diff(a, b, 'v45/' + p, 'v46/' + p, n=1, lineterm=''))
    with open(os.path.join(OUT, 'p03_' + os.path.basename(p) + '.diff'), 'w') as fh:
        fh.write('\n'.join(ud) + '\n')
    print(p, 'udiffLines', len(ud))

# inventory: structural
p = 'docs/operations/document-inventory.v1.json'
a = json.loads(get45(p)); b = json.load(open(os.path.join(S46, 'files', p)))
def summarize(o):
    return {k: (len(v) if isinstance(v, (list, dict)) else v) for k, v in o.items()} if isinstance(o, dict) else type(o).__name__
print('inv45', summarize(a)); print('inv46', summarize(b))
res = {}
for k in set(a) | set(b):
    if a.get(k) == b.get(k): continue
    if isinstance(a.get(k), list) and isinstance(b.get(k), list):
        la, lb = a[k], b[k]
        key = None
        if la and isinstance(la[0], dict) and 'path' in la[0]: key = 'path'
        if key:
            da = {x[key]: x for x in la}; db = {x[key]: x for x in lb}
            ch = [pp for pp in da if pp in db and da[pp] != db[pp]]
            det = []
            for pp in ch[:400]:
                det.append({'path': pp, 'diff': [(x[0], x[1], x[2]) for x in jdiff(da[pp], db[pp])]})
            res[k] = {'len45': len(la), 'len46': len(lb), 'added': sorted(set(db) - set(da))[:50], 'addedN': len(set(db) - set(da)), 'removed': sorted(set(da) - set(db))[:50], 'removedN': len(set(da) - set(db)), 'changedN': len(ch), 'changed': det, 'dupPaths46': len(lb) - len(db)}
        else:
            res[k] = {'len45': len(la), 'len46': len(lb)}
    else:
        res[k] = {'v45': a.get(k) if not isinstance(a.get(k), (list, dict)) else 'complex', 'v46': b.get(k) if not isinstance(b.get(k), (list, dict)) else 'complex', 'diff': jdiff(a.get(k), b.get(k))[:100] if isinstance(a.get(k), dict) else None}
with open(os.path.join(OUT, 'p03_inventory.diff.json'), 'w') as fh:
    json.dump(res, fh, indent=1, default=str)
print('inventory keys differing', list(res))

# references to removed root support files
hits = []
for base in [S46 + '/files', S46 + '/support']:
    for r, d, f in os.walk(base):
        for x in f:
            fp = os.path.join(r, x)
            if os.path.getsize(fp) > 5_000_000: continue
            try: t = open(fp, encoding='utf-8').read()
            except Exception: continue
            for name in ['accepted-source-application-delta.json', 'assembly-metadata.json', 'bound-review-receipt.json']:
                if name in t: hits.append((os.path.relpath(fp, S46), name))
print('removedNameHits', hits)
