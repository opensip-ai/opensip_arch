"""Merge the three parts into review.json and sanity-check every required element."""
import json, os

BASE = '/tmp/opensip-design-corrections/claude-independent-design.v27'
R = {}
for n in ('review.part1.json', 'review.part2.json', 'review.part3.json'):
    part = json.load(open(os.path.join(BASE, n)))
    for k, v in part.items():
        assert k not in R, 'duplicate key %s' % k
        R[k] = v

ORDER = ['review', 'verdict', 'verdictBasis', 'origin', 'ancestry', 'subjectManifestSha256',
         'verifiedManifest', 'manifestVerification', 'delta26to27', 'readingStanding',
         'completedReadingThisReview', 'inheritedReadingFromV26', 'correctionsToMyOwnPriorReview',
         'requiredReviewActions', 'deltaAssessment', 'resolvedSinceV26', 'newMustIssues',
         'newShouldIssues', 'advisories', 'independentProbes', 'evidenceReceipts',
         'fDispositionSource', 'fDispositions', 'sharedAssumptionTCBSCOPE01',
         'evaluationResidualStanding', 'evaluationResidualDispositions', 'arDispositions',
         'fwDispositions', 'inheritedResidualDispositions', 'scopedReviewOwnerDispositions',
         'dispositionVocabulary', 'dispositionCounts', 'dispositionStandingForEveryRow',
         'crossUnitStanding', 'limitations', 'grantsNothing']
out = {k: R[k] for k in ORDER if k in R}
for k in R:
    if k not in out:
        out[k] = R[k]

# ---- assertions on the required shape ----
assert out['subjectManifestSha256'] == 'a1ae88efc4198054b11cc2533582808a88dd25e5a5cc11c2966058ce1390227a'
assert out['verifiedManifest'] is True
assert len(out['evaluationResidualDispositions']) == 30
assert len(out['arDispositions']) == 16
assert len(out['fwDispositions']) == 15
assert len(out['inheritedResidualDispositions']) == 27
assert len(out['scopedReviewOwnerDispositions']) == 5
assert len(out['fDispositions']) == 14
EXPECT = (['RES-EP13-%02d' % i for i in range(1, 20)] +
          ['IR-EP13-NB-%02d' % i for i in range(1, 8)] + ['AX6', 'AX9', 'MD5', 'RX2c'])
assert list(out['evaluationResidualDispositions']) == EXPECT, 'residual id mismatch'
for k, v in out['scopedReviewOwnerDispositions'].items():
    assert v['appliedByThisReview'] is False and v['finalApplicationOutcomeGranted'] is False, k
for k, v in out['evaluationResidualDispositions'].items():
    assert v['independentGradeAwardedHere'] is None, k
    assert v['basis'] and v['owningSelectors'] and v['scope'] and v['limits'], k
tcb = [k for k, v in out['evaluationResidualDispositions'].items() if v['sharedAssumption']]
assert len(tcb) == 13, tcb
assert out['crossUnitStanding']['condition5'] == 'NOT MET'
assert out['crossUnitStanding']['qualificationGatesPerformed'] == 0
assert out['crossUnitStanding']['commitRecoveryCasesExecuted'] == 0
assert out['crossUnitStanding']['condition2ObligationsRetained'] == 28
assert out['grantsNothing']['grade'] is None
if out['verdict'] == 'ACCEPT':
    assert not out['newMustIssues'] and not out['newShouldIssues']
    assert all(v is True for k, v in out['requiredReviewActions'].items())

# no generic copying: every disposition basis must be distinct
bases = [v['basis'] for v in out['evaluationResidualDispositions'].values()]
assert len(set(bases)) == 30, 'duplicate residual basis text'
reasons = [v['reassessmentFor27'] for v in out['arDispositions'].values()]
print('distinct AR reassessment texts:', len(set(reasons)), 'of 16')

json.dump(out, open(os.path.join(BASE, 'review.json'), 'w'), indent=1)
sz = os.path.getsize(os.path.join(BASE, 'review.json'))
print('wrote review.json  keys=%d  bytes=%d' % (len(out), sz))
print('verdict:', out['verdict'])
print('counts:', json.dumps(out['dispositionCounts']))
for n in ('review.part1.json', 'review.part2.json', 'review.part3.json'):
    os.remove(os.path.join(BASE, n))
print('removed intermediate parts')
