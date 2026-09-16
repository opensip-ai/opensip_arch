"""S13 — record the invariant tests and their back-test in the report itself."""
import hashlib, json, os

V2 = '/tmp/opensip-design-corrections/claude-independent33-reconciliation.v2'
P = os.path.join(V2, 'review.json')
N = json.load(open(P))
s12 = json.load(open(os.path.join(V2, 'receipts', 's12-backtest.json')))
N['reportInvariantTests'] = {
    'standing': ('meaningful report invariants, not row counts. The v1 pass ran 59 checks and passed '
                 'them all while carrying every defect root then found, because counting rows cannot '
                 'detect a row that contradicts its own array, a current pointer that disagrees with '
                 'its own review status, or a prose rule that contradicts the measurement it cites.'),
    'families': [
        {'family': 'current assertions vs the row\'s own changed-owner array',
         'asserts': ('no row whose owner bytes changed may deny that change or stay silent about it; '
                     'the INHERITED standing may appear only where owners are byte-verified unchanged '
                     'and resolve in frozen33; no row carries both HISTORY and INHERITED')},
        {'family': 'current vs historical package receipt consistency',
         'asserts': ('evidenceReceipts.authorPackage must agree with authorPackageReview; the PENDING '
                     'root-input digest may appear only under the historical label; the current numbers '
                     'must equal the actual p12/p13 measurement; p11 must be preserved, not deleted')},
        {'family': 'required-cell bridge cause vs source rule AND retained measurement',
         'asserts': ('the matrix case must carry the MATRIX pair and not the fallback; pure '
                     'missing-work cases must carry required-cell-unsatisfied; the mixed case must '
                     'carry both in one Run; the JSON rule must match bridge_cause as frozen; and no MD '
                     'occurrence of the withdrawn sentence may appear outside a correction context')},
        {'family': 'structure carried forward',
         'asserts': ('107 rows, both authority flags false, prior fields identical to BOTH earlier '
                     'records, owner arrays consistent with the 18-file delta, 28/32-with-0/54-with-0 '
                     'and condition 5 NOT MET, D9 open on DR-007 and DR-011-R08, TCB-SCOPE-01 open over '
                     '13 rows, no residual graded, grantsNothing unchanged, verdict ACCEPT')}],
    'checksRun': 47, 'checksFailed': 0,
    'refinementsMadeAfterFirstRun': [
        {'check': 'MD must not assert the withdrawn bridge sentence',
         'firstDraft': 'forbade the string outright, so quoting it AS WITHDRAWN failed the test',
         'refined': 'every occurrence must sit inside a correction context; there is exactly one and it does'},
        {'check': 'changed-owner rows must account for their own change',
         'firstDraft': ('demanded that every such row repeat the owner filename, which flagged six rows '
                        'that accurately describe the change in prose'),
         'refined': ('fails on DENIAL or SILENCE, which is the defect class; the naming split is '
                     'censused at $.changedOwnerRowAudit instead of cosmetically rewritten')}],
    'backTest': {
        'why': 'a refinement that no longer catches the defect it was written for is a weakened test',
        'refinedInvariantAgainstTheV1Record': s12['v1FailureRows'],
        'catchesExactlyTheEightDefectiveRows': s12['catchesAllEightOnV1'],
        'cleanOnThisRecord': s12['cleanOnV2'],
        'dr007CorrectlyNotFlagged': s12['dr007NotFlagged'],
        'receipt': 'receipts/s12-backtest.json'}}
json.dump(N, open(P, 'w'), indent=1, default=str)
print('recorded. sha256:', hashlib.sha256(open(P, 'rb').read()).hexdigest())
