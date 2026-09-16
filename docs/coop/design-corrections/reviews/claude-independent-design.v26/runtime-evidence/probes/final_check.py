"""Final: re-index receipts, hash the deliverables, and re-verify the frozen snapshot."""
import hashlib, json, os, subprocess, sys

B = '/tmp/opensip-design-corrections/claude-independent-design.v26'
subprocess.run([sys.executable, os.path.join(B, 'probes', 'pZ_receipts_index.py')],
               capture_output=True)

for n in ['review.md', 'review.json', 'dispositions.json', 'review.body.json', 'PROGRESS.md']:
    p = os.path.join(B, n)
    b = open(p, 'rb').read()
    print('%-22s %8d  %s' % (n, len(b), hashlib.sha256(b).hexdigest()))

d = json.load(open(os.path.join(B, 'review.json')))
req = d['requiredReviewActions']
print()
print('requiredReviewActions all true:', all(req.values()), '(%d items)' % len(req))
print('verdict:', d['verdict'], '| verifiedManifest:', d['verifiedManifest'])
print('subjectManifestSha256 ok:',
      d['subjectManifestSha256'] == 'c9a6c26a82dbe24acfbba423360be54e45f11325576b172d75a005ec35d0ffb2')
print('grantsNothing:', json.dumps(d['grantsNothing']))
print('dispositionCounts:', json.dumps(d['dispositionCounts']))
print('MUST/SHOULD/ADV:', len(d['newMustIssues']), len(d['newShouldIssues']), len(d['advisories']))

man = {r['path']: r for r in json.load(open(
    '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v26.json'))['files']}
R = '/tmp/opensip-design-corrections/candidate-subject.v26'
bad = n = 0
for rel, rec in man.items():
    p = os.path.join(R, rel)
    if not os.path.isfile(p) or os.path.getsize(p) != rec['bytes']:
        bad += 1
        continue
    if hashlib.sha256(open(p, 'rb').read()).hexdigest() != rec['sha256']:
        bad += 1
    n += 1
print()
print('FINAL frozen snapshot re-verification: %d files checked, %d deviations' % (n, bad))
