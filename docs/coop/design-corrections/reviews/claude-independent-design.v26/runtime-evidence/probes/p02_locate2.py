import os, hashlib, re

ROOT = '/tmp/opensip-design-corrections/candidate-subject.v26'
pats = [
    r'14-.*\.md$', r'.*repository.*layout.*', r'.*module-layout.*', r'.*file-inventory.*',
    r'.*implementation-boundaries.*', r'.*build-plan.*', r'.*commit-recovery.*',
    r'.*implementation-coverage.*', r'.*planning.*', r'.*report-asset.*',
    r'.*store-instance.*', r'.*high-water.*', r'.*attempt-custody.*',
    r'.*hydradb.*',
]
rx = [re.compile(p, re.I) for p in pats]
seen = []
for dp, dn, fn in os.walk(ROOT):
    for f in fn:
        rel = os.path.relpath(os.path.join(dp, f), ROOT)
        if '/reviews/' in rel and 'design-corrections/reviews' in rel:
            continue
        for r in rx:
            if r.search(f) or r.search(rel):
                seen.append(rel)
                break
for s in sorted(set(seen)):
    p = os.path.join(ROOT, s)
    print('%-9d %s' % (os.path.getsize(p), s))
