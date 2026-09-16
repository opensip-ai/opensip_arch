import json, hashlib, os, difflib
S = '/private/tmp/opensip-design-corrections/application-stage.v46'
R = '/Users/sb/code/opensip-ai/opensip_arch'
C = S + '/support/root-application46-corrections.v1/before'
m46 = json.load(open(S + '/application-subject.v46.json'))
m45 = json.load(open(R + '/docs/coop/design-corrections/reviews/application-subject.v45.json'))
out = {}
for k in ['files', 'beforeImages', 'support']:
    a = {e['path']: e for e in m45[k]}; b = {e['path']: e for e in m46[k]}
    changed = sorted(p for p in a if p in b and (a[p]['sha256'] != b[p]['sha256'] or a[p].get('beforeSha256') != b[p].get('beforeSha256')))
    out[k] = {'v45': len(a), 'v46': len(b), 'identical': sum(1 for p in a if p in b and a[p] == b[p]), 'changed': [(p, a[p]['sha256'][:8], b[p]['sha256'][:8]) for p in changed], 'added': sorted(set(b) - set(a)), 'removed': sorted(set(a) - set(b))}
out['topLevelKeys45'] = {k: (v if not isinstance(v, list) else len(v)) for k, v in m45.items()}
out['topLevelDiff'] = {k: [m45.get(k), m46.get(k)] for k in set(m45) | set(m46) if not isinstance(m46.get(k), list) and m45.get(k) != m46.get(k)}
# delta.json vs manifests
d = json.load(open(R + '/docs/coop/design-corrections/reviews/root-application46-delta.v1/delta.json'))
a = {e['path']: e['sha256'] for e in m45['files']}; b = {e['path']: e['sha256'] for e in m46['files']}
out['deltaJsonAgrees'] = all(a[c['path']] == c['beforeSha256'] and b[c['path']] == c['afterSha256'] for c in d['changed']) and len(d['changed']) == len(out['files']['changed'])
# corrections before images == v45 files
cb = {}
for r, dd, f in os.walk(C):
    for x in f:
        p = os.path.join(r, x); rel = os.path.relpath(p, C)
        cb[rel] = hashlib.sha256(open(p, 'rb').read()).hexdigest() == a.get(rel)
out['correctionBeforeEqualsV45'] = cb
print(json.dumps(out, indent=1))
