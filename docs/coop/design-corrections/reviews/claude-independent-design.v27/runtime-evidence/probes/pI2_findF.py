import json, os, re

base = '/tmp/opensip-design-corrections/claude-author-package-review.v1'
for dp, dn, fn in os.walk(base):
    for n in sorted(fn):
        p = os.path.join(dp, n)
        print('%-70s %d' % (os.path.relpath(p, base), os.path.getsize(p)))

md = open(os.path.join(base, 'review.md'), encoding='utf-8').read()
print('\nreview.md first 1200 chars:\n', md[:1200])
pats = [r'\bF-\d\d\b', r'\bF\d\b', r'\bF0\d\b', r'\bF1\d\b', r'finding\s*0?\d+']
for pt in pats:
    got = sorted(set(re.findall(pt, md, re.I)))
    if got:
        print('pattern %-14s ->' % pt, got[:30])
heads = re.findall(r'^#{1,4} .*$', md, re.M)
print('\nheadings (%d):' % len(heads))
for h in heads[:60]:
    print('   ', h[:130])
