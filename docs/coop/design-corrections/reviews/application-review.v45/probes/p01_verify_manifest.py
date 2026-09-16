import json, hashlib, os, sys
S = '/private/tmp/opensip-design-corrections/application-stage.v45.2'
MP = S + '/application-subject.v45.json'
EXPECT = '948d9bdd50169ad54871b6816d7f970a2f203fd9b1e84b7bea87dcc5c9ca6757'
mb = open(MP, 'rb').read()
print('manifest sha', hashlib.sha256(mb).hexdigest(), hashlib.sha256(mb).hexdigest() == EXPECT, len(mb))
m = json.loads(mb)
base = {'files': S + '/files/', 'beforeImages': S + '/before/', 'support': S + '/'}
bad = 0; tot = 0
for k in ['files', 'beforeImages', 'support']:
    seen = set()
    for e in m[k]:
        tot += 1
        if e['path'] in seen: print('DUP', k, e['path'])
        seen.add(e['path'])
        if e['path'].startswith('/') or '..' in e['path'].split('/'): print('UNSAFE', k, e['path'])
        p = base[k] + e['path']
        if not os.path.isfile(p) or os.path.islink(p):
            print('MISSING/LINK', k, e['path']); bad += 1; continue
        b = open(p, 'rb').read()
        if hashlib.sha256(b).hexdigest() != e['sha256'] or len(b) != e['bytes']:
            print('MISMATCH', k, e['path']); bad += 1
print('entries', tot, 'bad', bad, {k: len(m[k]) for k in ['files', 'beforeImages', 'support']})
listed = set()
for k in ['files', 'beforeImages', 'support']:
    for e in m[k]:
        listed.add(os.path.normpath(base[k] + e['path']))
disk = set()
for r, ds, fs in os.walk(S):
    for f in fs:
        disk.add(os.path.normpath(os.path.join(r, f)))
unl = sorted(x[len(S):] for x in disk - listed)
print('disk files', len(disk), 'unlisted', len(unl), unl[:30])
# support entries that are under files/ or before/?
print('support under files/ or before/', [e['path'] for e in m['support'] if e['path'].startswith(('files/', 'before/'))][:5])
bset = {e['path']: e['sha256'] for e in m['beforeImages']}
fpaths = {e['path'] for e in m['files']}
print('files with beforeSha None', sum(1 for e in m['files'] if e.get('beforeSha256') is None))
print('files beforeSha != beforeImage', [e['path'] for e in m['files'] if e.get('beforeSha256') is not None and bset.get(e['path']) != e['beforeSha256']])
print('beforeImages not in files', [p for p in bset if p not in fpaths])
print('files with beforeSha but no beforeImage', [e['path'] for e in m['files'] if e.get('beforeSha256') and e['path'] not in bset])
print('unchanged files (sha==beforeSha)', [e['path'] for e in m['files'] if e['sha256'] == e.get('beforeSha256')])
for k in ['standing', 'implementationAuthorized', 'qualificationClaimed', 'pathConventions', 'retainedManifestPath', 'retainedReviewPath', 'postReviewBinding', 'designSubject', 'independentDesignReview', 'freshBlindConsumerReview']:
    print(k, '=', json.dumps(m[k]))
