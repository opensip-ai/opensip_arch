"""Q03 — inventory (names and sizes only) of package11, the root package verification, and the root
atom-cause retained reviews, so I can choose what to read. Blind replay / consumer files are not opened;
names matching those patterns are listed as SKIPPED."""
import hashlib, json, os, re

REV = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews'
DIRS = ['/tmp/opensip-design-corrections/claude-author-package-successor.v11',
        os.path.join(REV, 'author-package-final34-verification.v1'),
        os.path.join(REV, 'root-final-atom-cause-source-completion.v1'),
        os.path.join(REV, 'root-atom-cause-final2-assessment.v1'),
        os.path.join(REV, 'root-atom-cause-draft-review.v2'),
        '/tmp/opensip-design-corrections/root-final34-reference.v1',
        '/tmp/opensip-design-corrections/root-final34-planning-checks.v1']
BLIND = re.compile(r'blind|consumer|replay-oracle|oracle', re.I)
R = {}
for d in DIRS:
    ent = []
    if not os.path.isdir(d):
        print('\n### %s — MISSING' % d)
        R[d] = None
        continue
    for root, _, fs in os.walk(d):
        for f in sorted(fs):
            p = os.path.join(root, f)
            rel = os.path.relpath(p, d)
            ent.append({'rel': rel, 'bytes': os.path.getsize(p), 'skipped': bool(BLIND.search(rel))})
    R[d] = ent
    print('\n### %s (%d files)' % (d, len(ent)))
    shown = 0
    for e in ent:
        if shown >= 45 and '/' in e['rel']:
            continue
        print('   %9d  %s%s' % (e['bytes'], e['rel'], '   [SKIPPED: blind/consumer pattern]' if e['skipped'] else ''))
        shown += 1
    if len(ent) > shown:
        print('   ... %d more nested files' % (len(ent) - shown))
vf = os.path.join(REV, 'author-package-final34-verification.v1', 'verification.json')
if os.path.isfile(vf):
    R['rootVerificationSha256'] = hashlib.sha256(open(vf, 'rb').read()).hexdigest()
    print('\nroot package verification sha matches declared:',
          R['rootVerificationSha256'] == '58a78e56efb3f61819a9ad656fea41fea8aa158f0bd69c2c90aeb393365b50c4')
json.dump(R, open('/tmp/opensip-design-corrections/claude-independent-design.v34/receipts/q03-inventory.json', 'w'), indent=1)
