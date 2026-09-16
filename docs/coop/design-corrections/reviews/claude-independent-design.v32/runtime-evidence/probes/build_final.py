"""Merge parts into review.json and assert every required element."""
import json, os

BASE = '/tmp/opensip-design-corrections/claude-independent-design.v32'
R = {}
for n in ('part1.json', 'part2.json', 'part3.json'):
    for k, v in json.load(open(os.path.join(BASE, n))).items():
        assert k not in R, 'duplicate ' + k
        R[k] = v

ORDER = ['review', 'verdict', 'verdictBasis', 'sessionIdentity', 'subjectManifestSha256',
         'verifiedManifest', 'manifestVerification', 'delta31to32', 'verificationScopeOfInputs',
         'sourceChangeAssessment', 'correctionsToMyOwnV31Record', 'resolvedSinceV31',
         'newMustIssues', 'newShouldIssues', 'advisories', 'evidenceReceipts',
         'fDispositions', 'sharedAssumptionTCBSCOPE01', 'evaluationResidualStanding',
         'evaluationResidualDispositions', 'arDispositions', 'fwDispositions',
         'inheritedResidualDispositions', 'scopedReviewOwnerDispositions',
         'dispositionCounts', 'dispositionStandingForEveryRow', 'crossUnitStanding',
         'limitations', 'grantsNothing']
out = {k: R[k] for k in ORDER if k in R}
for k in R:
    out.setdefault(k, R[k])

assert out['subjectManifestSha256'] == '3897e8d1bb389f3d39669997d3078d5a44fa024f29d97bd17854a48916610bf2'
assert out['verifiedManifest'] is True
EXP = (['RES-EP13-%02d' % i for i in range(1, 20)]
       + ['IR-EP13-NB-%02d' % i for i in range(1, 8)] + ['AX6', 'AX9', 'MD5', 'RX2c'])
assert list(out['evaluationResidualDispositions']) == EXP
for name, n in (('fDispositions', 14), ('evaluationResidualDispositions', 30),
                ('arDispositions', 16), ('fwDispositions', 15),
                ('inheritedResidualDispositions', 27), ('scopedReviewOwnerDispositions', 5)):
    assert len(out[name]) == n, (name, len(out[name]))
    for rid, row in out[name].items():
        assert row['appliedByThisReview'] is False, (name, rid)
        assert row['finalApplicationOutcomeGranted'] is False, (name, rid)
assert sum(1 for v in out['evaluationResidualDispositions'].values() if v['sharedAssumption']) == 13
# RR31-01: every inherited row names real owners
empty = [k for k, v in out['inheritedResidualDispositions'].items() if not v['currentOwnerFiles']]
assert not empty, empty
for name in ('arDispositions', 'fwDispositions', 'inheritedResidualDispositions',
             'scopedReviewOwnerDispositions'):
    for rid, row in out[name].items():
        assert row['currentOwnerFiles'], (name, rid)
        assert row['currentStatusOn32'], (name, rid)
assert out['crossUnitStanding']['condition5'] == 'NOT MET'
assert out['crossUnitStanding']['qualificationGatesPerformed'] == 0
assert out['crossUnitStanding']['commitRecoveryCasesExecuted'] == 0
assert out['crossUnitStanding']['condition2ObligationsRetained'] == 28
assert out['grantsNothing']['grade'] is None
if out['verdict'] == 'ACCEPT':
    assert not out['newMustIssues'] and not out['newShouldIssues']

# no duplicated status prose within a map
for name in ('arDispositions', 'fwDispositions', 'inheritedResidualDispositions',
             'scopedReviewOwnerDispositions'):
    texts = [v['currentStatusOn32'] for v in out[name].values()]
    dup = len(texts) - len(set(texts))
    print('%-34s %d rows, %d duplicate status texts' % (name, len(texts), dup))
    assert dup == 0, name
rs = [v['currentStatusOn32'] for v in out['evaluationResidualDispositions'].values()]
print('evaluationResidualDispositions   %d rows, %d duplicate status texts' % (len(rs), len(rs) - len(set(rs))))
assert len(set(rs)) == 30

json.dump(out, open(os.path.join(BASE, 'review.json'), 'w'), indent=1, default=str)
print('\nwrote review.json keys=%d bytes=%d' % (len(out), os.path.getsize(os.path.join(BASE, 'review.json'))))
print('verdict:', out['verdict'], '| counts:', json.dumps(out['dispositionCounts']))
for n in ('part1.json', 'part2.json', 'part3.json'):
    os.remove(os.path.join(BASE, n))
print('removed intermediate parts')
