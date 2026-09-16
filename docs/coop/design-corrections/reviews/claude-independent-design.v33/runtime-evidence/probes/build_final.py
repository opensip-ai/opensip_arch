"""Merge and assert. Re-reads the root-owned package update immediately before finalizing."""
import hashlib, json, os

BASE = '/tmp/opensip-design-corrections/claude-independent-design.v33'
MAN = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v33.json'
man = {f['path'] for f in json.load(open(MAN))['files']}
R = {}
for n in ('part1.json', 'part2.json', 'part3.json'):
    for k, v in json.load(open(os.path.join(BASE, n))).items():
        assert k not in R, 'duplicate ' + k
        R[k] = v

# FINAL re-read of the root-owned package update
UPD = os.path.join(BASE, 'author-package-update.json')
cur = json.load(open(UPD))
cursha = hashlib.sha256(open(UPD, 'rb').read()).hexdigest()
R['authorPackageReview']['finalReReadBeforeFinalizing'] = {
    'sha256': cursha, 'status': cur['status'],
    'changedDuringReview': cursha != R['authorPackageReview']['rootInputConsumed']['sha256'],
    'note': 'root owns this file and may update it; the exact version consumed is recorded'}
if cur['status'] != 'PENDING':
    R['authorPackageReview']['ALERT'] = ('the root input changed to %s during the review; the package '
                                         'review remains recorded INCOMPLETE because no verification '
                                         'was performed against it in this pass' % cur['status'])
print('final re-read of author-package-update.json: status=%s changed=%s'
      % (cur['status'], R['authorPackageReview']['finalReReadBeforeFinalizing']['changedDuringReview']))

ORDER = ['review', 'verdict', 'verdictBasis', 'sessionIdentity', 'baselineRecord',
         'subjectManifestSha256', 'verifiedManifest', 'manifestVerification', 'delta32to33',
         'sourceChangeAssessment', 'authorPackageReview', 'resolvedSinceV32',
         'newMustIssues', 'newShouldIssues', 'advisories', 'evidenceReceipts',
         'fDispositions', 'sharedAssumptionTCBSCOPE01', 'evaluationResidualDispositions',
         'arDispositions', 'fwDispositions', 'inheritedResidualDispositions',
         'scopedReviewOwnerDispositions', 'dispositionCounts', 'dispositionStandingForEveryRow',
         'crossUnitStanding', 'limitations', 'grantsNothing', 'rowAudit']
out = {k: R[k] for k in ORDER if k in R}
for k in R:
    out.setdefault(k, R[k])

assert out['subjectManifestSha256'] == '1cf3db70d4b73b0c42f1393331e6a874ee26f7ddf67aa05c6ac15a5753069299'
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
assert out['sharedAssumptionTCBSCOPE01']['dependentRowCount'] == 13
cu = out['crossUnitStanding']
assert cu['condition2ObligationsRetained'] == 28 and cu['qualificationGatesPerformed'] == 0
assert cu['condition5'] == 'NOT MET' and cu['commitRecoveryCasesExecuted'] == 0
assert out['grantsNothing']['grade'] is None and out['grantsNothing']['packageAcceptance'] is False
assert not out['newMustIssues'] and not out['newShouldIssues']
# every owner path resolves on 33
bad = []
for mp in ('arDispositions', 'fwDispositions', 'inheritedResidualDispositions',
           'scopedReviewOwnerDispositions'):
    for rid, row in out[mp].items():
        for p in row['currentOwnerFiles']:
            if p not in man:
                bad.append(mp + '/' + rid + ':' + p)
        assert row['currentStatusOn33']
for rid, row in out['evaluationResidualDispositions'].items():
    for p in row.get('currentOwnerSelectors', []):
        if p not in man:
            bad.append('eval/' + rid + ':' + p)
assert not bad, bad
# no stale 32-era current fields
for mp in ('arDispositions', 'fwDispositions', 'inheritedResidualDispositions',
           'scopedReviewOwnerDispositions'):
    for rid, row in out[mp].items():
        assert 'currentStatusOn32' not in row, (mp, rid)
        assert 'ownerFilesChangedIn31to32' not in row, (mp, rid)
json.dump(out, open(os.path.join(BASE, 'review.json'), 'w'), indent=1, default=str)
sz = os.path.getsize(os.path.join(BASE, 'review.json'))
print('\nwrote review.json keys=%d bytes=%d' % (len(out), sz))
print('verdict:', out['verdict'])
print('counts :', json.dumps(out['dispositionCounts']))
print('owner paths absent from frozen33:', bad)
for n in ('part1.json', 'part2.json', 'part3.json'):
    os.remove(os.path.join(BASE, n))
print('removed intermediate parts')
