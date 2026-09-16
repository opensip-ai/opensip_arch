"""PZ — final consistency check of the complete reports."""
import hashlib, json, os

BASE = '/tmp/opensip-design-corrections/claude-independent-design.v33'
SRC = '/tmp/opensip-design-corrections/candidate-subject.v33'
PKG = '/tmp/opensip-design-corrections/claude-author-package-successor.v10'
MAN = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v33.json'
man = {f['path']: f for f in json.load(open(MAN))['files']}
R = json.load(open(os.path.join(BASE, 'review.json')))
md = open(os.path.join(BASE, 'review.md'), encoding='utf-8').read()
C = {}


def chk(n, ok, d=''):
    C[n] = bool(ok)
    print('%-56s %s %s' % (n, 'OK ' if ok else 'FAIL', d if not ok else ''))


bad = sum(1 for p, f in man.items()
          if not os.path.isfile(os.path.join(SRC, p))
          or hashlib.sha256(open(os.path.join(SRC, p), 'rb').read()).hexdigest() != f['sha256'])
chk('frozen33 unchanged after the whole review', bad == 0, str(bad))
am = json.load(open(os.path.join(PKG, 'artifact-manifest.json')))
rows = am['files'] if isinstance(am, dict) else am
pbad = sum(1 for r in rows
           if hashlib.sha256(open(os.path.join(PKG, r['path']), 'rb').read()).hexdigest() != r['sha256'])
chk('package10 unchanged after verification', pbad == 0, str(pbad))

for k, n in (('fDispositions', 14), ('evaluationResidualDispositions', 30), ('arDispositions', 16),
             ('fwDispositions', 15), ('inheritedResidualDispositions', 27),
             ('scopedReviewOwnerDispositions', 5)):
    chk('map %s has %d rows' % (k, n), len(R[k]) == n, str(len(R[k])))
chk('107 total', sum(len(R[k]) for k in ('fDispositions', 'evaluationResidualDispositions',
                                         'arDispositions', 'fwDispositions',
                                         'inheritedResidualDispositions',
                                         'scopedReviewOwnerDispositions')) == 107)
chk('verdict ACCEPT', R['verdict'] == 'ACCEPT', R['verdict'])
chk('manifest sha is source33',
    R['subjectManifestSha256'] == '1cf3db70d4b73b0c42f1393331e6a874ee26f7ddf67aa05c6ac15a5753069299')
chk('verifiedManifest true', R['verifiedManifest'] is True)
chk('no new MUST/SHOULD', not R['newMustIssues'] and not R['newShouldIssues'])
chk('three advisories', len(R['advisories']) == 3)
chk('A-11 resolved', any(a['id'] == 'A-11' and 'RESOLVED' in str(a.get('statusOn33'))
                         for a in R['advisories']))
applied = [(m, k) for m in ('fDispositions', 'evaluationResidualDispositions', 'arDispositions',
                            'fwDispositions', 'inheritedResidualDispositions',
                            'scopedReviewOwnerDispositions')
           for k, v in R[m].items() if v['appliedByThisReview'] or v['finalApplicationOutcomeGranted']]
chk('every row applied=false and no outcome granted', not applied, str(applied)[:140])
chk('TCB once with 13 dependents',
    R['sharedAssumptionTCBSCOPE01']['dependentRowCount'] == 13
    and sum(1 for v in R['evaluationResidualDispositions'].values() if v['sharedAssumption']) == 13)
cu = R['crossUnitStanding']
chk('28/32-unperformed/54/condition5 intact',
    cu['condition2ObligationsRetained'] == 28 and cu['qualificationGatesPerformed'] == 0
    and cu['commitRecoveryCasesExecuted'] == 0 and cu['condition5'] == 'NOT MET')
chk('D9 obligation persists', 'ASSIGNED' in cu['d9SuccessorObligation'].upper())
chk('30 residuals PENDING',
    all(v['reviewStatus'] == 'PENDING' and v['independentGradeAwardedHere'] is None
        for v in R['evaluationResidualDispositions'].values()))
ownbad = []
for mp in ('arDispositions', 'fwDispositions', 'inheritedResidualDispositions',
           'scopedReviewOwnerDispositions'):
    for rid, row in R[mp].items():
        ownbad += [p for p in row['currentOwnerFiles'] if p not in man]
        if not row.get('currentStatusOn33'):
            ownbad.append(mp + '/' + rid + ':no-status')
chk('every owner path resolves and every row has a 33 status', not ownbad, str(ownbad)[:160])
chk('no stale 32-era current fields',
    not any('currentStatusOn32' in v or 'ownerFilesChangedIn31to32' in v
            for mp in ('arDispositions', 'fwDispositions', 'inheritedResidualDispositions',
                       'scopedReviewOwnerDispositions') for v in R[mp].values()))
chk('package review COMPLETE and verified',
    R['authorPackageReview']['status'].startswith('COMPLETE')
    and R['authorPackageReview']['myVerification']['allThirteenAsExpected'] is True
    and R['authorPackageReview']['myVerification']['queryChecks'] == 7)
chk('both package-update versions recorded',
    R['authorPackageReview']['rootInputConsumed']['pendingVersionSha256']
    != R['authorPackageReview']['rootInputConsumed']['readyVersionSha256'])
chk('grantsNothing design-only',
    R['grantsNothing']['grade'] is None and not R['grantsNothing']['activation']
    and not R['grantsNothing']['blindAcceptance'] and not R['grantsNothing']['packageAcceptance']
    and not R['grantsNothing']['architectureReady'])
chk('md verdict matches json', '**Verdict: ACCEPT.**' in md)
chk('md records the mid-review status change', 'PENDING' in md and 'READY_FOR_INDEPENDENT_REVIEW' in md)
chk('md declares no consumer/blind read', 'no blind oracle is an input' in md)
chk('md states 28/32/54 and condition 5', all(x in md for x in ('**28**', '**32**', '**54**', 'condition 5 NOT MET')))

fails = [k for k, v in C.items() if not v]
print('\n%d checks, %d failures %s' % (len(C), len(fails), fails))
final = hashlib.sha256(open(os.path.join(BASE, 'review.json'), 'rb').read()).hexdigest()
print('review.json sha256:', final)
print('review.md   sha256:', hashlib.sha256(open(os.path.join(BASE, 'review.md'), 'rb').read()).hexdigest())
print('\noutput tree:', sorted(os.listdir(BASE)))
print('receipts: %d | probes: %d' % (len(os.listdir(os.path.join(BASE, 'receipts'))),
                                     len(os.listdir(os.path.join(BASE, 'probes')))))
json.dump({'checks': C, 'failures': fails, 'reviewJsonSha256': final},
          open(os.path.join(BASE, 'receipts', 'pZ-final.json'), 'w'), indent=1)
