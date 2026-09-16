"""PROBE Z — final integrity check: the frozen snapshot and the author package are byte-unchanged
after everything I ran, my output is self-consistent, and nothing was written outside my own tree."""
import hashlib, json, os

SRC = '/tmp/opensip-design-corrections/candidate-subject.v27'
PKG = '/tmp/opensip-design-corrections/claude-author-package-successor.v4'
BASE = '/tmp/opensip-design-corrections/claude-independent-design.v27'
MAN = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v27.json'

man = json.load(open(MAN))['files']
bad = 0
for r in man:
    p = os.path.join(SRC, r['path'])
    if not os.path.isfile(p) or os.path.getsize(p) != r['bytes']:
        bad += 1
        continue
    if hashlib.sha256(open(p, 'rb').read()).hexdigest() != r['sha256']:
        bad += 1
print('snapshot27 deviations after the whole review :', bad)

am = json.load(open(os.path.join(PKG, 'artifact-manifest.json')))
rows = am['files'] if isinstance(am, dict) else am
pbad = 0
for r in rows:
    p = os.path.join(PKG, r['path'])
    if not os.path.isfile(p) or hashlib.sha256(open(p, 'rb').read()).hexdigest() != r['sha256']:
        pbad += 1
print('author package deviations                   :', pbad, 'of', len(rows))

R = json.load(open(os.path.join(BASE, 'review.json')))
print('\nreview.json verdict                          :', R['verdict'])
print('newMustIssues / newShouldIssues / advisories :',
      len(R['newMustIssues']), '/', len(R['newShouldIssues']), '/', len(R['advisories']))
print('dispositions                                 :', json.dumps(R['dispositionCounts']))
print('all requiredReviewActions true               :',
      all(v is True for v in R['requiredReviewActions'].values()))
print('subjectManifestSha256 / verifiedManifest     :', R['subjectManifestSha256'][:16] + '…',
      R['verifiedManifest'])
print('TCB dependents flagged                       :',
      sum(1 for v in R['evaluationResidualDispositions'].values() if v['sharedAssumption']))
print('owner routes all not-applied                 :',
      all(not v['appliedByThisReview'] and not v['finalApplicationOutcomeGranted']
          for v in R['scopedReviewOwnerDispositions'].values()))
print('condition5 / gates / recovery / condition2   :',
      R['crossUnitStanding']['condition5'],
      R['crossUnitStanding']['qualificationGatesPerformed'],
      R['crossUnitStanding']['commitRecoveryCasesExecuted'],
      R['crossUnitStanding']['condition2ObligationsRetained'])
print('grants                                       :',
      R['grantsNothing']['grade'], R['grantsNothing']['activation'],
      R['grantsNothing']['implementationAuthorized'], R['grantsNothing']['blindAcceptance'])

print('\noutput tree:')
for n in sorted(os.listdir(BASE)):
    p = os.path.join(BASE, n)
    print('   %-16s %s' % (n, os.path.getsize(p) if os.path.isfile(p) else '<dir>'))
print('receipts:', len(os.listdir(os.path.join(BASE, 'receipts'))),
      '| probes:', len(os.listdir(os.path.join(BASE, 'probes'))))
