"""P14 — the root input transitioned to READY during this review and I verified package10, so the
package portion is now COMPLETE. Update review.json accordingly: F rows, advisory A-11 and verdict."""
import hashlib, json, os

BASE = '/tmp/opensip-design-corrections/claude-independent-design.v33'
REC = os.path.join(BASE, 'receipts')
RJ = os.path.join(BASE, 'review.json')
p11 = json.load(open(os.path.join(REC, 'p11-package.json')))
p12 = json.load(open(os.path.join(REC, 'p12-package10.json')))
p13 = json.load(open(os.path.join(REC, 'p13-queries.json')))
UPD = os.path.join(BASE, 'author-package-update.json')
upd = json.load(open(UPD))
updsha = hashlib.sha256(open(UPD, 'rb').read()).hexdigest()
R = json.load(open(RJ))

R['authorPackageReview'] = {
    'status': 'COMPLETE — INDEPENDENTLY VERIFIED ON SOURCE33',
    'transitionDuringReview': (
        'The root-owned author-package-update.json was PENDING when I began and had changed to '
        'READY_FOR_INDEPENDENT_REVIEW by my final pre-finalization re-read. I therefore performed the '
        'package verification rather than finalizing an incomplete package review. Both exact versions '
        'are recorded.'),
    'rootInputConsumed': {'file': 'author-package-update.json',
                          'pendingVersionSha256': p11['updateFileSha256'],
                          'readyVersionSha256': updsha,
                          'status': upd['status'],
                          'namedPackageManifestSha256': upd['packageManifestSha256'],
                          'namedPackageFiles': upd['packageFiles']},
    'myVerification': {
        'artifactManifestSha256': p12['artifactManifestSha256'],
        'matchesRootNamedManifest': p12['matchesRootNamedManifest'],
        'declaredMembers': p12['declaredMembers'], 'verified': p12['verified'],
        'mismatched': p12['mismatched'], 'missing': p12['missing'],
        'sourceManifestByteEqualToFrozen33': p12['sourceManifestEqualsFrozen33'],
        'ownerSha256': p12['ownerSha256'],
        'thirteenCases': p12['counts'],
        'positivesAdmitBothBoundaries': p12['positivesAdmitBoth'],
        'negativesAdmitThenReplayRefuse': p12['negativesAdmitThenRefuse'],
        'bindingInvalidDefaultRefused': p12['bindingInvalidRefused'],
        'bindingLawfulAdmitted': p12['bindingLawfulAdmitted'],
        'allThirteenAsExpected': p12['allThirteenAsExpected'],
        'verifierReturncode': p13['returncode'],
        'verificationJsonEmitted': p13['verificationJsonEmitted'],
        'sourceFilesVerified': (p13.get('verification') or {}).get('sourceFilesVerified'),
        'packageFilesVerified': (p13.get('verification') or {}).get('packageFilesVerified'),
        'queryChecks': p13.get('queryChecks'),
        'queryAssessment': p13.get('queryAssessment'),
        'allGroupsPassed': p13.get('allGroupsPassed')},
    'rootVerificationAssessed': {
        'digestMatchesTheNamedOne': p13.get('rootVerificationMatchesNamedDigest'),
        'myGroupOutcomesIdentical': p13.get('myGroupsMatchRoot'),
        'standing': ('agreement with root is corroboration only; my basis is my own decoder and my own '
                     'execution against the snapshot33 owner')},
    'package9Assessed': {
        'standing': 'assessed from preserved receipts; NOT rerun',
        'genuineFailures': p11['genuineFailures'],
        'expectedRefusalsNotFailures': p11['expectedRefusalsNotFailures'],
        'assessment': p11['assessmentOfPackage9'],
        'rootExplanationOfTheMasking': upd.get('historicalFailure'),
        'myReading': ('Root records that package9\'s old semantic negative-group expectation passed '
                      'while the base proof had already refused — the negative group was MASKED rather '
                      'than being independent tamper evidence. That is consistent with what I measured '
                      'from the receipts, and it is the right reason to treat the package9 outcome as '
                      'a rebinding artifact rather than as evidence about source33.')},
    'retainedLimits': {
        'A10': ('TS checkpoint is helper-versus-owner only; the other six positives are owner-derived '
                'self-consistency; exists/none only with other operator limitations; the two-binding '
                'construction is incomplete with a single explicit binding; no compiler, provider or '
                'OS qualification.'),
        'A9': 'the repair controls retain their exact admitted-versus-unit limitations.',
        'residualGrades': 'all 30 author residual proposals remain PENDING independent grading.'}}

PKG_ROWS = ('F-01', 'F-02', 'F-03', 'F-05', 'F-06', 'F-08', 'F-10', 'F-11', 'F-12')
EV = ('Verified on a source33-bound package10: artifact manifest matches the root-named digest, '
      '305/305 members hash-verified, source-manifest byte-equal to the frozen33 manifest, all 13 '
      'Run/control cases replay as expected through BOTH open_run_closure and close_run with my own '
      'decoder, and verify-package.py exits 0 over 12,899 source files with 7/7 query checks. ')
for rid in PKG_ROWS:
    row = R['fDispositions'][rid]
    prior = row.get('priorBasisOn32') or ''
    row['dispositionOn33'] = row.get('v32Disposition') or 'RESOLVED-AND-STILL-HOLDS'
    row['currentBasisOn33'] = EV + prior
    row['packageEvidenceStandingOn33'] = 'confirmed on package10 (source33-bound)'
R['fDispositions']['F-06']['dispositionOn33'] = 'PARTIALLY-RESOLVED-REMAINDER-STILL-AN-EVIDENCE-LIMIT'
R['fDispositions']['F-06']['limits'] = ('The two-binding construction remains incomplete and the '
                                        'shipped control is single-explicit only. That stays an '
                                        'evidence limit, not a demonstrated owner defect.')

for a in R['advisories']:
    if a['id'] == 'A-11':
        a['statusOn33'] = 'RESOLVED DURING THIS REVIEW'
        a['resolution'] = (
            'The root input transitioned to READY_FOR_INDEPENDENT_REVIEW and named package10 '
            '(manifest 88c38b16…, 305 files). I verified it independently and all nine affected F rows '
            'are now evidenced on a source33-bound package. The package9 rebinding failure remains '
            'preserved and is explained by root as a masked negative-group expectation rather than '
            'independent tamper evidence, which matches my own reading of the receipts.')

R['limitations'] = [x for x in R['limitations']
                    if not x.startswith('The author package review is INCOMPLETE')]
R['limitations'].insert(2, ('The author package is author-assisted reference evidence verified on '
                            'source33; it is not blind reconstruction and grants no product '
                            'qualification. Package9 is known stale and was NOT rerun.'))
R['grantsNothing']['packageAcceptance'] = False
R['grantsNothing']['note'] = ('Verifying the package evidence is not accepting the package as a '
                              'product artifact, and grants no application outcome.')
R['grantsNothing']['stillRequired'] = ['final application review and activation',
                                       'successful original blind reconstruction',
                                       'product qualification of the 32 gates and 54 recovery cases']
R['verdict'] = 'ACCEPT'
R['verdictBasis'] = R['verdictBasis'].replace(
    'AUTHOR PACKAGE: INCOMPLETE, NOT ACCEPTED. The root-owned update is still PENDING and names no '
    'package10 manifest or verification, so no source33-bound package has been verified and nine F '
    'rows are recorded incomplete rather than presented as current. Package9 was rebound rather than '
    'constructed on 33 and its actual verification failed on three positive cases; I assessed those '
    'preserved receipts without rerunning them and treat the failure as the correct outcome for a '
    'rebound package under changed law, not a source defect. ',
    'AUTHOR PACKAGE: VERIFIED ON SOURCE33. The root input transitioned from PENDING to '
    'READY_FOR_INDEPENDENT_REVIEW during this review and my final pre-finalization re-read caught it, '
    'so I performed the verification rather than finalizing an incomplete package review. Package10 '
    'matches the root-named manifest digest with 305/305 members verified, its source-manifest is '
    'byte-equal to the frozen33 manifest, all 13 Run/control cases replay as expected through BOTH '
    'boundaries under my own decoder, and the verifier exits 0 with 7/7 query checks. Package9 remains '
    'preserved as a stale rebinding failure that I assessed without rerunning; root\'s explanation '
    'that its negative-group expectation was masked matches my reading. ')
json.dump(R, open(RJ, 'w'), indent=1, default=str)
print('verdict now:', R['verdict'])
print('package status:', R['authorPackageReview']['status'])
print('F rows updated:', PKG_ROWS)
print('review.json bytes:', os.path.getsize(RJ))
