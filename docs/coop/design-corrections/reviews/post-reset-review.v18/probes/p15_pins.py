"""p15: verify every transitive source pin in the v18 snapshot resolves to the actual file bytes,
and that the v17->v18 pin deltas are ONLY the corrected checker."""
import hashlib, json, os

FROZEN = '/tmp/opensip-design-corrections/candidate-subject.v18'
R = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/'
PIN_FILES = ['docs/coop/design-corrections/foundation/source-pins.v1.json',
             'docs/coop/design-corrections/native/source-pins.v2.json',
             'docs/coop/design-corrections/security/source-pins.v1.json',
             'docs/coop/design-corrections/workflows/source-pins.v1.json']


def collect(obj, path=''):
    """yield (jsonpath, dict) for every dict carrying both a path-like and a sha256"""
    if isinstance(obj, dict):
        if 'sha256' in obj and isinstance(obj.get('sha256'), str):
            yield path, obj
        for k, v in obj.items():
            yield from collect(v, path + '/' + str(k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from collect(v, path + '/%d' % i)


total, verified, bad, unresolved = 0, 0, [], []
per_file = {}
for pf in PIN_FILES:
    doc = json.load(open(os.path.join(FROZEN, pf)))
    n = 0
    for jp, d in collect(doc):
        total += 1
        n += 1
        p = d.get('path') or d.get('file') or d.get('source')
        if not p:
            unresolved.append((pf, jp, 'no path key', sorted(d.keys())[:6]))
            continue
        cand = os.path.join(FROZEN, p)
        if not os.path.isfile(cand):
            unresolved.append((pf, jp, 'missing file', p))
            continue
        h = hashlib.sha256(open(cand, 'rb').read()).hexdigest()
        if h == d['sha256']:
            verified += 1
        else:
            bad.append((pf, p, d['sha256'], h))
    per_file[pf] = n

print('pinFiles=%d  totalPinEntries=%d  verifiedAgainstActualBytes=%d  mismatched=%d  unresolved=%d'
      % (len(PIN_FILES), total, verified, len(bad), len(unresolved)))
for k, v in per_file.items():
    print('   %-70s %d' % (k.split('design-corrections/')[1], v))
for b in bad[:20]:
    print('  MISMATCH', b)
for u in unresolved[:20]:
    print('  UNRESOLVED', u)

# ---- v17 -> v18 pin delta: which pinned entries changed?
print('\n--- v17 vs v18 pin deltas ---')
import tarfile
v17man = {e['path']: e['sha256'] for e in json.load(open(R + 'candidate-subject.v17.json'))['files']}
# the v17 pin file bytes are not on disk; recover them from the v17 tarball
tar = tarfile.open(R + 'candidate-source.v17.tar.gz')
names = {n.lstrip('./') for n in tar.getnames()}
for pf in PIN_FILES:
    member = None
    for cand in (pf, './' + pf):
        try:
            member = tar.extractfile(cand)
            if member:
                break
        except KeyError:
            continue
    if member is None:
        print('  %s : v17 copy not found in tarball' % pf)
        continue
    old_doc = json.loads(member.read())
    new_doc = json.load(open(os.path.join(FROZEN, pf)))
    old_map = {d.get('path'): d['sha256'] for _, d in collect(old_doc) if d.get('path')}
    new_map = {d.get('path'): d['sha256'] for _, d in collect(new_doc) if d.get('path')}
    ch = sorted(p for p in set(old_map) & set(new_map) if old_map[p] != new_map[p])
    ad = sorted(set(new_map) - set(old_map))
    rm = sorted(set(old_map) - set(new_map))
    print('  %-28s entries=%d changed=%d added=%d removed=%d'
          % (pf.split('/')[-2], len(new_map), len(ch), len(ad), len(rm)))
    for p in ch:
        print('       CHANGED %s' % p)
    for p in ad + rm:
        print('       ADD/REM %s' % p)
