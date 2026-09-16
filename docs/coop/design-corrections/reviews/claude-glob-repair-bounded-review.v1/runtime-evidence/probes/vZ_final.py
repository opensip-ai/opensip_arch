"""Final integrity check: inputs untouched, deliverables consistent, commands retained."""
import hashlib, json, os

G = '/tmp/opensip-design-corrections/glob-semantics-successor.v1'
RR = '/tmp/opensip-design-corrections/root-repair-selection-author-review.v1'
SNAP = '/tmp/opensip-design-corrections/candidate-subject.v31'
BASE = '/tmp/opensip-design-corrections/claude-glob-repair-bounded-review.v1'
v00 = json.load(open(os.path.join(BASE, 'receipts/v00-verify.json')))


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


bad = 0
for r in v00['globChanges']:
    p = os.path.join(G, 'source', r['path'])
    if sha(p) != r['declaredSha256']:
        bad += 1
print('glob input deviations after the review  :', bad)
rbad = sum(1 for x in v00['repairReviewFiles'] if sha(os.path.join(RR, x['path'])) != x['sha256'])
print('repair input deviations after the review:', rbad, 'of', len(v00['repairReviewFiles']))

R = json.load(open(os.path.join(BASE, 'review.json')))
print('\nglob verdict      :', R['globDisposition']['verdict'])
print('RRS-A1            :', R['repairOwnershipDisposition']['RRS_A1']['answer'])
print('RRS-A2 unmet/partial:',
      [k for k, v in R['repairOwnershipDisposition']['RRS_A2'].items()
       if isinstance(v, dict) and v.get('status')])
print('grants            :', json.dumps(R['grantsNothing']))
print('differential pairs :', R['globDisposition']['reconstructabilityTest']['pairsTested'],
      '| mismatches:', R['globDisposition']['reconstructabilityTest']['mismatches'])
print('\noutput tree:')
for n in sorted(os.listdir(BASE)):
    p = os.path.join(BASE, n)
    print('   %-18s %s' % (n, os.path.getsize(p) if os.path.isfile(p) else '<dir>'))
print('receipts: %d | probes: %d' % (len(os.listdir(os.path.join(BASE, 'receipts'))),
                                     len(os.listdir(os.path.join(BASE, 'probes')))))
