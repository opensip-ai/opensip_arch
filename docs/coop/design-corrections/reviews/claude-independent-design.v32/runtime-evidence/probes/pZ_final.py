"""Final integrity check: frozen source and package untouched, deliverables consistent."""
import hashlib, json, os

SRC = '/tmp/opensip-design-corrections/candidate-subject.v32'
PKG = '/tmp/opensip-design-corrections/claude-author-package-successor.v8'
BASE = '/tmp/opensip-design-corrections/claude-independent-design.v32'
MAN = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v32.json'

bad = 0
for f in json.load(open(MAN))['files']:
    p = os.path.join(SRC, f['path'])
    if (not os.path.isfile(p) or os.path.getsize(p) != f['bytes']
            or hashlib.sha256(open(p, 'rb').read()).hexdigest() != f['sha256']):
        bad += 1
print('frozen32 deviations after the whole review :', bad)
am = json.load(open(os.path.join(PKG, 'artifact-manifest.json')))
rows = am['files'] if isinstance(am, dict) else am
pbad = sum(1 for r in rows
           if hashlib.sha256(open(os.path.join(PKG, r['path']), 'rb').read()).hexdigest() != r['sha256'])
print('package8 deviations                        :', pbad, 'of', len(rows))

R = json.load(open(os.path.join(BASE, 'review.json')))
print('\nverdict            :', R['verdict'])
print('verifiedManifest   :', R['verifiedManifest'])
print('subject sha        :', R['subjectManifestSha256'][:24] + '…')
print('must/should/advis  :', len(R['newMustIssues']), '/', len(R['newShouldIssues']), '/',
      len(R['advisories']))
print('counts             :', json.dumps(R['dispositionCounts']))
print('TCB dependents     :', R['sharedAssumptionTCBSCOPE01']['dependentRowCount'])
print('condition5/gates/recovery/cond2 :', R['crossUnitStanding']['condition5'],
      R['crossUnitStanding']['qualificationGatesPerformed'],
      R['crossUnitStanding']['commitRecoveryCasesExecuted'],
      R['crossUnitStanding']['condition2ObligationsRetained'])
print('grants             :', json.dumps(R['grantsNothing'])[:150])
applied = [(m, k) for m in ('fDispositions', 'evaluationResidualDispositions', 'arDispositions',
                            'fwDispositions', 'inheritedResidualDispositions',
                            'scopedReviewOwnerDispositions')
           for k, v in R[m].items() if v['appliedByThisReview'] or v['finalApplicationOutcomeGranted']]
print('rows claiming applied/granted   :', applied)
emptyown = [k for k, v in R['inheritedResidualDispositions'].items() if not v['currentOwnerFiles']]
print('inherited rows with empty owners:', emptyown)
print('archive equals manifest         :', R['manifestVerification']['archiveEqualsManifest'])
print('parent is my v31                :', R['manifestVerification']['parentIsMyV31'])
print('record corrections applied      :', len(R['correctionsToMyOwnV31Record']))
print('\noutput tree:')
for n in sorted(os.listdir(BASE)):
    p = os.path.join(BASE, n)
    print('   %-20s %s' % (n, os.path.getsize(p) if os.path.isfile(p) else '<dir>'))
print('receipts: %d | probes: %d' % (len(os.listdir(os.path.join(BASE, 'receipts'))),
                                     len(os.listdir(os.path.join(BASE, 'probes')))))
