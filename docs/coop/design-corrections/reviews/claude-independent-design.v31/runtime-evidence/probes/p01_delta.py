"""PROBE 01 (v31) — derive the 27->31 delta MYSELF from the frozen manifests, and also the
per-step deltas 27->28, 28->29, 29->30, 30->31, then compare with root's declared listing.
Root's listing is assessed, never adopted.
"""
import hashlib, json, os

REV = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews'
ROOTDELTA = '/tmp/opensip-design-corrections/final31-independent-review-inputs.v1/source27-to31-delta.json'
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v31/receipts'


def load(v):
    m = json.load(open(os.path.join(REV, 'candidate-subject.%s.json' % v)))
    return {f['path']: f for f in m['files']}, m


def diff(a, b):
    added = sorted(set(b) - set(a))
    removed = sorted(set(a) - set(b))
    changed = sorted(p for p in set(a) & set(b) if a[p]['sha256'] != b[p]['sha256'])
    return added, removed, changed


R = {}
steps = [('v27', 'v28'), ('v28', 'v29'), ('v29', 'v30'), ('v30', 'v31')]
maps = {v: load(v)[0] for v in ('v27', 'v28', 'v29', 'v30', 'v31')}
print('file counts:', {v: len(maps[v]) for v in maps})
R['fileCounts'] = {v: len(maps[v]) for v in maps}

for a, b in steps:
    ad, rm, ch = diff(maps[a], maps[b])
    R['step_%s_%s' % (a, b)] = {'added': ad, 'removed': rm, 'changed': ch,
                                'netBytes': sum(maps[b][p]['bytes'] for p in maps[b])
                                - sum(maps[a][p]['bytes'] for p in maps[a])}
    print('\n--- %s -> %s : +%d -%d ~%d ---' % (a, b, len(ad), len(rm), len(ch)))
    for p in ad:
        print('   ADD  %s (%d B)' % (p, maps[b][p]['bytes']))
    for p in rm:
        print('   DEL  %s' % p)
    for p in ch:
        print('   CHG  %-78s %d -> %d B' % (p, maps[a][p]['bytes'], maps[b][p]['bytes']))

ad, rm, ch = diff(maps['v27'], maps['v31'])
R['cumulative'] = {
    'added': [{'path': p, 'bytes': maps['v31'][p]['bytes'], 'sha256': maps['v31'][p]['sha256']} for p in ad],
    'removed': rm,
    'changed': [{'path': p, 'bytes27': maps['v27'][p]['bytes'], 'bytes31': maps['v31'][p]['bytes'],
                 'sha27': maps['v27'][p]['sha256'], 'sha31': maps['v31'][p]['sha256'],
                 'sameByteCount': maps['v27'][p]['bytes'] == maps['v31'][p]['bytes']} for p in ch],
    'addedCount': len(ad), 'removedCount': len(rm), 'changedCount': len(ch),
    'touchedTotal': len(ad) + len(ch),
    'netBytes': sum(f['bytes'] for f in maps['v31'].values()) - sum(f['bytes'] for f in maps['v27'].values())}
print('\n=== CUMULATIVE 27 -> 31 : +%d added, -%d removed, ~%d changed (%d touched) ===' %
      (len(ad), len(rm), len(ch), len(ad) + len(ch)))
for p in ad:
    print('   ADD  %s' % p)
for p in ch:
    same = maps['v27'][p]['bytes'] == maps['v31'][p]['bytes']
    print('   CHG  %-76s %s' % (p, 'SAME-BYTE-COUNT' if same else '%d->%d' % (
        maps['v27'][p]['bytes'], maps['v31'][p]['bytes'])))
print('net bytes:', R['cumulative']['netBytes'])

# ---- compare with root's declared listing ----
if os.path.isfile(ROOTDELTA):
    rd = json.load(open(ROOTDELTA))
    R['rootDeltaTopKeys'] = sorted(rd) if isinstance(rd, dict) else '<list>'
    txt = json.dumps(rd)
    mypaths = set(ad) | set(ch)
    rootpaths = set()
    def collect(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k in ('path', 'file') and isinstance(v, str):
                    rootpaths.add(v)
                collect(v)
        elif isinstance(o, list):
            for v in o:
                collect(v)
        elif isinstance(o, str) and o.startswith('docs/'):
            rootpaths.add(o)
    collect(rd)
    R['rootDeclaredPaths'] = sorted(rootpaths)
    R['rootDeclaredCount'] = len(rootpaths)
    R['inMineNotRoot'] = sorted(mypaths - rootpaths)
    R['inRootNotMine'] = sorted(rootpaths - mypaths)
    R['myTouchedCount'] = len(mypaths)
    R['agreesWithRoot'] = not (mypaths - rootpaths) and not (rootpaths - mypaths)
    print('\nroot declared paths: %d | mine: %d | agree: %s' %
          (len(rootpaths), len(mypaths), R['agreesWithRoot']))
    print('in mine not root :', R['inMineNotRoot'])
    print('in root not mine :', R['inRootNotMine'])
    R['rootClaimsNoRemoval'] = 'remov' in txt.lower()
else:
    R['rootDeltaPresent'] = False
    print('\nROOT DELTA LISTING NOT FOUND at', ROOTDELTA)

json.dump(R, open(os.path.join(OUT, 'p01-delta.json'), 'w'), indent=1)
print('\nwrote p01-delta.json')
