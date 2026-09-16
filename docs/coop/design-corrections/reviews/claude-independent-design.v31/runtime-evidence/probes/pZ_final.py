"""Final integrity check: frozen inputs untouched, deliverables consistent, failures preserved."""
import hashlib, json, os

SRC = '/tmp/opensip-design-corrections/candidate-subject.v31'
PKG = '/tmp/opensip-design-corrections/claude-author-package-successor.v7'
BASE = '/tmp/opensip-design-corrections/claude-independent-design.v31'
MAN = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v31.json'

bad = 0
for f in json.load(open(MAN))['files']:
    p = os.path.join(SRC, f['path'])
    if (not os.path.isfile(p) or os.path.getsize(p) != f['bytes']
            or hashlib.sha256(open(p, 'rb').read()).hexdigest() != f['sha256']):
        bad += 1
print('snapshot31 deviations after the whole review :', bad)

am = json.load(open(os.path.join(PKG, 'artifact-manifest.json')))
rows = am['files'] if isinstance(am, dict) else am
pbad = sum(1 for r in rows
           if hashlib.sha256(open(os.path.join(PKG, r['path']), 'rb').read()).hexdigest() != r['sha256'])
print('author package deviations                    :', pbad, 'of', len(rows))

R = json.load(open(os.path.join(BASE, 'review.json')))
print('\nverdict                          :', R['verdict'])
print('verifiedManifest                 :', R['verifiedManifest'])
print('subjectManifestSha256            :', R['subjectManifestSha256'][:24] + '…')
print('must / should / advisories       :', len(R['newMustIssues']), '/',
      len(R['newShouldIssues']), '/', len(R['advisories']))
print('disposition counts               :', json.dumps(R['dispositionCounts']))
print('TCB dependents                   :',
      sum(1 for v in R['evaluationResidualDispositions'].values() if v['sharedAssumption']))
print('condition5 / gates / recovery    :', R['crossUnitStanding']['condition5'],
      R['crossUnitStanding']['qualificationGatesPerformed'],
      R['crossUnitStanding']['commitRecoveryCasesExecuted'])
print('condition2 retained              :', R['crossUnitStanding']['condition2ObligationsRetained'])
print('grants                           : grade=%s activation=%s impl=%s blind=%s'
      % (R['grantsNothing']['grade'], R['grantsNothing']['activation'],
         R['grantsNothing']['implementationAuthorized'], R['grantsNothing']['blindAcceptance']))
applied = [(m, k) for m in ('evaluationResidualDispositions', 'arDispositions', 'fwDispositions',
                            'inheritedResidualDispositions', 'scopedReviewOwnerDispositions')
           for k, v in R[m].items() if v['appliedByThisReview'] or v['finalApplicationOutcomeGranted']]
print('rows claiming applied/granted    :', applied)
print('delta agrees with root listing   :', R['delta27to31']['agreesWithRootListing'])
print('ancestry chain verified          :', R['manifestVerification']['ancestryChainVerified'])

print('\noutput tree:')
for n in sorted(os.listdir(BASE)):
    p = os.path.join(BASE, n)
    print('   %-22s %s' % (n, os.path.getsize(p) if os.path.isfile(p) else '<dir>'))
print('receipts: %d | probes: %d' % (len(os.listdir(os.path.join(BASE, 'receipts'))),
                                     len(os.listdir(os.path.join(BASE, 'probes')))))
