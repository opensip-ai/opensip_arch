"""Probe 06 — verify the author evidence package completely and its binding to exact27."""
import hashlib, json, os

PKG = '/tmp/opensip-design-corrections/claude-author-package-successor.v4'
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v27/receipts'
os.makedirs(OUT, exist_ok=True)
res = {'packageRoot': PKG}

print('top-level entries:')
for n in sorted(os.listdir(PKG)):
    p = os.path.join(PKG, n)
    print('   %-52s %s' % (n, 'DIR' if os.path.isdir(p) else str(os.path.getsize(p))))

# locate the artifact manifest
cand = [n for n in os.listdir(PKG) if 'manifest' in n.lower() and n.endswith('.json')]
res['manifestCandidates'] = cand
mpath = None
for n in cand:
    p = os.path.join(PKG, n)
    h = hashlib.sha256(open(p, 'rb').read()).hexdigest()
    print('   manifest candidate %-40s %s' % (n, h))
    if h == '7d6ad55a3ed8eb1f16a4e1ac89076e6d05f547bd69810d5525f1d8b1d23e8c00':
        mpath = p
        res['artifactManifest'] = n
        res['artifactManifestSha256'] = h
res['artifactManifestMatchesDeclared'] = mpath is not None
if mpath is None:
    # search one level down
    for dp, dn, fn in os.walk(PKG):
        for n in fn:
            if n.endswith('.json') and 'manifest' in n.lower():
                p = os.path.join(dp, n)
                h = hashlib.sha256(open(p, 'rb').read()).hexdigest()
                if h == '7d6ad55a3ed8eb1f16a4e1ac89076e6d05f547bd69810d5525f1d8b1d23e8c00':
                    mpath = p
                    res['artifactManifest'] = os.path.relpath(p, PKG)
                    res['artifactManifestSha256'] = h
                    res['artifactManifestMatchesDeclared'] = True
print('\nartifact manifest resolved:', res.get('artifactManifest'), res['artifactManifestMatchesDeclared'])

if mpath:
    m = json.load(open(mpath, encoding='utf-8'))
    res['manifestTopKeys'] = list(m)
    rows = m.get('files') or m.get('artifacts') or []
    res['declaredFileCount'] = m.get('fileCount', len(rows))
    ok = bad = miss = 0
    detail = []
    for r in rows:
        rel = r.get('path')
        fp = os.path.join(PKG, rel)
        if not os.path.isfile(fp):
            miss += 1
            detail.append({'path': rel, 'issue': 'missing'})
            continue
        h = hashlib.sha256(open(fp, 'rb').read()).hexdigest()
        if h == r.get('sha256') and (r.get('bytes') is None or os.path.getsize(fp) == r['bytes']):
            ok += 1
        else:
            bad += 1
            detail.append({'path': rel, 'declared': r.get('sha256', '')[:16], 'actual': h[:16]})
    res.update({'rows': len(rows), 'verified': ok, 'mismatched': bad, 'missing': miss,
                'detail': detail[:15]})
    # extras on disk not in the manifest
    known = {r['path'] for r in rows}
    extra = []
    for dp, dn, fn in os.walk(PKG):
        for n in fn:
            rel = os.path.relpath(os.path.join(dp, n), PKG)
            if rel not in known:
                extra.append(rel)
    res['extraOnDisk'] = sorted(extra)[:25]
    res['extraOnDiskCount'] = len(extra)
    # source binding
    for k in ('sourceManifest', 'sourceManifestSha256', 'subjectManifestSha256',
              'sourceSubject', 'standing', 'boundSource'):
        if k in m:
            res['binding_' + k] = m[k]
    blob = json.dumps(m)
    res['mentionsExact27Manifest'] = 'a1ae88efc4198054b11cc2533582808a88dd25e5a5cc11c2966058ce1390227a' in blob
    res['mentionsSource26Manifest'] = 'c9a6c26a82dbe24acfbba423360be54e45f11325576b172d75a005ec35d0ffb2' in blob

json.dump(res, open(os.path.join(OUT, 'p06-package-verify.json'), 'w'), indent=1)
print('\n' + json.dumps({k: v for k, v in res.items() if k != 'detail'}, indent=1)[:3000])
if res.get('detail'):
    print('\nmismatch detail:', json.dumps(res['detail'], indent=1)[:1200])
