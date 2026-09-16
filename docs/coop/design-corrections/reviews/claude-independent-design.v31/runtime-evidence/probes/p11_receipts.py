"""PROBE 11 (v31) — locate the preserved source29 FAILED receipt and the root source31
verification, and assess (not trust) what they claim."""
import json, os

OUT = '/tmp/opensip-design-corrections/claude-independent-design.v31/receipts'
PKG = '/tmp/opensip-design-corrections/claude-author-package-successor.v7'
R = {}

for base in ('/tmp/opensip-design-corrections/author-package-final31-verification.v1',
             '/tmp/opensip-design-corrections/root-independent27-advisory-corrections.v1',
             '/tmp/opensip-design-corrections/root-rule-results-order-correction.v1'):
    if not os.path.isdir(base):
        print('MISSING', base)
        continue
    names = []
    for dp, dn, fn in os.walk(base):
        for n in fn:
            p = os.path.join(dp, n)
            names.append((os.path.relpath(p, base), os.path.getsize(p)))
    R[os.path.basename(base)] = sorted(names)
    print('\n== %s (%d files)' % (os.path.basename(base), len(names)))
    for n, s in sorted(names)[:25]:
        print('   %-58s %d' % (n, s))

# package historical preparation dirs
print('\n== package historical preparation dirs')
for n in sorted(os.listdir(PKG)):
    p = os.path.join(PKG, n)
    if os.path.isdir(p) and n.startswith('historical-'):
        inner = sorted(os.listdir(p))
        R['pkg_' + n] = inner
        print('   %-42s %s' % (n, inner[:8]))

# hunt for a failed/source29 receipt anywhere in the package
hits = []
for dp, dn, fn in os.walk(PKG):
    for n in fn:
        rel = os.path.relpath(os.path.join(dp, n), PKG)
        if '29' in rel or 'fail' in rel.lower():
            hits.append(rel)
R['packagePathsMentioning29OrFail'] = sorted(hits)[:30]
print('\npackage paths naming 29 or fail:', sorted(hits)[:12])

json.dump(R, open(os.path.join(OUT, 'p11-receipts.json'), 'w'), indent=1, default=str)
print('\nwrote p11-receipts.json')
