"""P02 — inventory ONLY the permitted live-review inputs and hash them.

Explicitly excluded and never opened: any consumer-b* runtime, which is blind consumer material.
"""
import hashlib, json, os

REV = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews'
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v32/receipts'
WANT = ['root-independent31-assessment.v1', 'independent31-advisory8-evidence.v1',
        'root-repair-scope-correction.v1', 'claude-repair-selection-author.v2',
        'root-repair-v2-interim-scope.v1', 'root-repair-selection-reproduction.v1',
        'final32-pin-binding.v1', 'root-repair-selection-author-review.v1']
FORBIDDEN = 'consumer-b'
R = {'excludedByPolicy': 'any consumer-b* runtime (blind consumer material) was never listed or opened'}


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


for d in WANT:
    base = os.path.join(REV, d)
    if not os.path.isdir(base):
        print('MISSING DIR:', d)
        R.setdefault('missingDirs', []).append(d)
        continue
    rows = []
    for dp, dn, fn in os.walk(base):
        if FORBIDDEN in dp:
            continue
        for n in sorted(fn):
            p = os.path.join(dp, n)
            rows.append({'path': os.path.relpath(p, base), 'bytes': os.path.getsize(p),
                         'sha256': sha(p)})
    R[d] = rows
    print('\n=== %s (%d files) ===' % (d, len(rows)))
    for x in rows[:22]:
        print('   %-64s %9d  %s' % (x['path'][-64:], x['bytes'], x['sha256'][:16]))
    if len(rows) > 22:
        print('   ... %d more' % (len(rows) - 22))

# root delta inventory anywhere under reviews (top level only)
hits = [n for n in os.listdir(REV) if 'delta31' in n or 'delta-31' in n]
R['rootDeltaCandidates'] = hits
print('\nroot delta inventory candidates at reviews top level:', hits)
for h in hits:
    p = os.path.join(REV, h)
    if os.path.isfile(p):
        R['rootDeltaSha256'] = sha(p)
        print('   %s sha=%s bytes=%d' % (h, R['rootDeltaSha256'][:16], os.path.getsize(p)))
json.dump(R, open(os.path.join(OUT, 'p02-inputs.json'), 'w'), indent=1)
print('\nwrote p02-inputs.json')
