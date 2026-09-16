"""Merge the four parts into review.json and assert every required element."""
import json, os

BASE = '/tmp/opensip-design-corrections/claude-independent-design.v31'
R = {}
for n in ('part1.json', 'part2.json', 'part3.json', 'part4.json'):
    for k, v in json.load(open(os.path.join(BASE, n))).items():
        assert k not in R, 'duplicate key ' + k
        R[k] = v

ORDER = ['review', 'verdict', 'verdictBasis', 'origin', 'sessionAncestry', 'subjectManifestSha256',
         'verifiedManifest', 'manifestVerification', 'delta27to31', 'authorPackageVerification',
         'sourceDeltaAssessment', 'correctionsToMyOwnV27Record', 'resolvedSinceV27',
         'newMustIssues', 'newShouldIssues', 'advisories', 'independentProbes', 'evidenceReceipts',
         'planningDecisions', 'fDispositions', 'sharedAssumptionTCBSCOPE01',
         'evaluationResidualStanding', 'evaluationResidualDispositions', 'arDispositions',
         'fwDispositions', 'inheritedResidualDispositions', 'scopedReviewOwnerDispositions',
         'dispositionCounts', 'dispositionStandingForEveryRow', 'crossUnitStanding',
         'limitations', 'grantsNothing']
out = {k: R[k] for k in ORDER if k in R}
for k in R:
    out.setdefault(k, R[k])

assert out['subjectManifestSha256'] == 'ca713db549f9337ae52a4bccc2ebbb84b136b8dc5d0545003bb3b2a24dfc95b5'
assert out['verifiedManifest'] is True
EXPECT = (['RES-EP13-%02d' % i for i in range(1, 20)]
          + ['IR-EP13-NB-%02d' % i for i in range(1, 8)] + ['AX6', 'AX9', 'MD5', 'RX2c'])
assert list(out['evaluationResidualDispositions']) == EXPECT
assert len(out['fDispositions']) == 14
assert len(out['arDispositions']) == 16
assert len(out['fwDispositions']) == 15
assert len(out['inheritedResidualDispositions']) == 27
assert len(out['scopedReviewOwnerDispositions']) == 5
assert sum(1 for v in out['evaluationResidualDispositions'].values() if v['sharedAssumption']) == 13
for name in ('evaluationResidualDispositions', 'arDispositions', 'fwDispositions',
             'inheritedResidualDispositions', 'scopedReviewOwnerDispositions'):
    for rid, row in out[name].items():
        assert row['appliedByThisReview'] is False, (name, rid)
        assert row['finalApplicationOutcomeGranted'] is False, (name, rid)
for rid, row in out['fDispositions'].items():
    assert row['appliedByThisReview'] is False
assert out['crossUnitStanding']['condition5'] == 'NOT MET'
assert out['crossUnitStanding']['qualificationGatesPerformed'] == 0
assert out['crossUnitStanding']['commitRecoveryCasesExecuted'] == 0
assert out['crossUnitStanding']['condition2ObligationsRetained'] == 28
assert out['grantsNothing']['grade'] is None
if out['verdict'] == 'ACCEPT':
    assert not out['newMustIssues'] and not out['newShouldIssues']

# no generic copying: current scope text must be distinct per row within each map
for name in ('arDispositions', 'fwDispositions', 'inheritedResidualDispositions',
             'scopedReviewOwnerDispositions'):
    texts = [v['currentScopeOn31'] for v in out[name].values()]
    dupes = len(texts) - len(set(texts))
    print('%-34s %d rows, %d duplicate scope texts' % (name, len(texts), dupes))
    assert dupes == 0, name
bases = [v['currentStatusOn31'] for v in out['evaluationResidualDispositions'].values()]
print('evaluationResidualDispositions  30 rows, %d duplicate status texts' % (len(bases) - len(set(bases))))
assert len(set(bases)) == 30

json.dump(out, open(os.path.join(BASE, 'review.json'), 'w'), indent=1)
print('\nwrote review.json  keys=%d  bytes=%d'
      % (len(out), os.path.getsize(os.path.join(BASE, 'review.json'))))
print('verdict:', out['verdict'], '| counts:', json.dumps(out['dispositionCounts']))
for n in ('part1.json', 'part2.json', 'part3.json', 'part4.json'):
    os.remove(os.path.join(BASE, n))
print('removed intermediate parts')
