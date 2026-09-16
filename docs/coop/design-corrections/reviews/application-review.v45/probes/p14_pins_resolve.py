import json, hashlib, os, collections
S = '/private/tmp/opensip-design-corrections/application-stage.v45.2/'
C = '/tmp/opensip-design-corrections/candidate-subject.v45/'
R = '/Users/sb/code/opensip-ai/opensip_arch/'
m = json.load(open(S + 'application-subject.v45.json'))
staged = {e['path']: e['sha256'] for e in m['files']}
cm = json.load(open(R + 'docs/coop/design-corrections/reviews/candidate-subject.v45.json'))
snap = {e['path']: e['sha256'] for e in cm['files']}
_c = {}
def livesha(p):
    if p in _c: return _c[p]
    fp = R + p
    v = hashlib.sha256(open(fp, 'rb').read()).hexdigest() if os.path.isfile(fp) else None
    _c[p] = v; return v
recs = ['application.v1.json', 'readiness-row-map.v1.json', 'review-owner-dispositions.v1.json', 'correction-crosswalk.applied.v1.json', 'inherited-residuals.applied.v1.json', 'evaluation-residual-dispositions.applied.v1.json', 'qualification-gates.applied.v1.json', 'accepted-review-advisories.v1.json', 'validation-summary.applied.v1.json']
stats = collections.Counter(); problems = []
def norm(p):
    if p.startswith('reviews/'): return 'docs/coop/design-corrections/' + p
    return p
def walk(o, rec, ptr):
    if isinstance(o, dict):
        p = o.get('path'); h = o.get('sha256') or o.get('sourceSha256')
        if isinstance(p, str) and isinstance(h, str) and len(h) == 64:
            p2 = norm(p)
            ra = o.get('resolveAgainst')
            where = []
            if snap.get(p2) == h: where.append('snapshot')
            if staged.get(p2) == h: where.append('staged')
            if livesha(p2) == h: where.append('live')
            if isinstance(ra, dict) and ra.get('sha256') != '8b4efbb04d9e25126ec7955931cf364f7013b3710a45c48bae8bc563a0c82155':
                # historical resolveAgainst (e.g. v13)
                stats['historical-resolveAgainst'] += 1
                hm = ra.get('path')
                try:
                    hman = json.load(open(R + hm)); hmap = {e['path']: e['sha256'] for e in hman['files']}
                    ok = hmap.get(p2) == h
                    if not ok: problems.append((rec, ptr, p2, h[:12], 'historical manifest mismatch'))
                    else: stats['historical-ok'] += 1
                except Exception as ex:
                    problems.append((rec, ptr, p2, 'historical manifest error', str(ex)))
            elif not where:
                problems.append((rec, ptr, p2, h[:12], 'UNRESOLVED'))
            else:
                stats['+'.join(where)] += 1
                if isinstance(ra, (dict, str)) and 'snapshot' not in where:
                    problems.append((rec, ptr, p2, h[:12], 'declares resolveAgainst snapshot but not in snapshot', where))
        for k, v in o.items(): walk(v, rec, ptr + '/' + str(k))
    elif isinstance(o, list):
        for i, v in enumerate(o): walk(v, rec, ptr + '/' + str(i))
for r in recs:
    walk(json.load(open(S + 'files/docs/coop/design-corrections/' + r)), r, '')
print(stats)
print('problems', len(problems))
for x in problems: print('  ', x)
