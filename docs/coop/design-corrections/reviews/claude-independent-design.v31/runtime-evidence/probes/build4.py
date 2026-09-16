"""review.json part 4 — probes/receipts, issues, advisories, resolved-since-27, standing and verdict."""
import json, os

BASE = '/tmp/opensip-design-corrections/claude-independent-design.v31'
REC = os.path.join(BASE, 'receipts')


def rec(n):
    return json.load(open(os.path.join(REC, n)))


p06, p09c = rec('p06-replayorder.json'), rec('p09c-digestlaw.json')
p12, p14 = rec('p12-enumcontrols.json'), rec('p14-exports.json')
p15, p16 = rec('p15-portable31.json'), rec('p16-verifypkg.json')
p17, p19 = rec('p17-propmixed.json'), rec('p19-suites31.json')
p08, p22b = rec('p08-recordpointers.json'), rec('p22b-derivedrecompute.json')
O = {}

O['independentProbes'] = [
    {'id': 'P-00', 'what': 'manifest, archive, every row hash/size, extras, and the 31->30->29->28->27 ancestry',
     'result': '12895/12895 verified, 736,536,507 bytes, 0 missing/mismatched/extra; chain resolves to the exact v27 I graded'},
    {'id': 'P-01', 'what': 'my own 27->31 delta, per step and cumulative, compared with root\'s listing',
     'result': '2 added, 0 removed, 14 changed (16 touched); identical to root\'s 16 paths'},
    {'id': 'P-02', 'what': 'author package7 members and source binding',
     'result': '270/270 hash-match, source-manifest is byte-equal to the frozen31 manifest, native schema digest matches'},
    {'id': 'P-03/P-04', 'what': 'planning layer bindings and the 26/27 planning decisions on 31',
     'result': 'layer2 28/28 pins resolve; 198 paths / 20 packages / 320 mappings in 11 groups / M0-M6 / 54 cases / 32 gates, all unchanged'},
    {'id': 'P-05', 'what': 'every x-opensip-order annotation against the reference implementation',
     'result': '57 annotated properties; exactly 2 carry an explicit key order and BOTH are implemented; 0 left to the generic order'},
    {'id': 'P-06', 'what': 'ruleResults order: frozen run, then branch-omission in a disposable verified copy',
     'result': 'frozen passes; omission raises ORDER_OR_DUPLICATE while minting the proof bundle, so the branch is load-bearing',
     'failuresPreserved': '2 earlier runs failed on my own incomplete copies (discovery-defaults.py, then delivery.v4.json) and one wrongly reported load-bearing'},
    {'id': 'P-06b', 'what': 'the three ordering rows from the full frozen report',
     'result': 'correct-order wholeRun ADMIT; canonical-member order REFUSE; duplicate ruleId REFUSE'},
    {'id': 'P-07', 'what': 'native retention catalog measured structurally',
     'result': '76 sites (syntactic == structural), 0 undeclared, exactly 3 derived uses at the named SourceUnitOwnershipV1 positions'},
    {'id': 'P-08', 'what': 'every annotation record pointer resolved against frozen31',
     'result': 'all 3 resolve; the one legacy identity-schemas.v2 pointer binds a definition byte-identical to v3'},
    {'id': 'P-09/09b/09c', 'what': 'native digest-law enforcement',
     'result': "checker's own frozen report says PASS with annotationSites 76; the law is decidable and every mutation names its site",
     'failuresPreserved': 'two earlier runs read PIN-MISMATCH (rc=2) as enforcement; the pin gate fires first and was not bypassed'},
    {'id': 'P-12', 'what': 'the five enumeration root controls plus my own guard-omission mutation',
     'result': 'all five pass; omitting the guard makes the two project-root cases misattribute to ENUMERATION_BINDING_PROGRAM_ENTRY and the two member-root cases silently ADMIT',
     'failuresPreserved': 'my first invocation omitted --stdout/--receipt and parsed an empty report'},
    {'id': 'P-13', 'what': 'the AX6/AX9/MD5/RX2c originals, now frozen members',
     'result': 'both artifacts are members with matching digests; the original declares exactly those four as escapedEveryGuard out of 29 variants'},
    {'id': 'P-14', 'what': 'independent decode and replay of all 13 exports through both boundaries',
     'result': '7 positives ADMIT/ADMIT; 3 controls ADMIT then REFUSE EVALUATOR_COMPLETE_PROOF_REPLAY; invalid-default REFUSE ENUMERATION_BINDING_PROGRAM_ENTRY; lawful default and explicit ADMIT'},
    {'id': 'P-15', 'what': 'portable reconstruction against source31 in a fresh arbitrary directory',
     'result': 'all 5 builders succeed with no helper overlay; ALL 13 stores byte-identical to the preserved exports with identical runIds'},
    {'id': 'P-16', 'what': 'verify-package.py executed against frozen source31',
     'result': 'rc=0; 12895 source and 270 package files verified; 13 Run outcomes plus 7 query checks; my query outputs regenerate byte-identical'},
    {'id': 'P-17', 'what': 'the separate property and mixed-universe probes on 31',
     'result': 'properties pass with both effective-edition assertions; unmerged ADMIT and merged REFUSE EXECUTION_INPUTS_COVERAGE_DERIVE'},
    {'id': 'P-18/18b', 'what': 'RR27-01: where EXECUTION_INPUTS_COVERAGE_DERIVE is actually raised',
     'result': 'by AST enclosure: 1 site in load_coverage, 6 in the coverage-account loop of admit_execution_inputs, 0 in partitions_in_cell',
     'failuresPreserved': 'my indentation-extent pass mislabelled six sites as module level before I used the AST'},
    {'id': 'P-19', 'what': 'reference suites on 31 and rg availability',
     'result': 'evaluator3 launcher 1242 pins valid, 0 changed/missing, 16/16 children exit 0; 11 group checkers exit 0; 0 frozen deviations; rg 15.2.0 present and invocable'},
    {'id': 'P-20/21', 'what': 'the 30 residual rows bound to frozen31 and the TCB set re-decided by reading',
     'result': '30/30 ids, 0 selector or sha mismatches, all PENDING, none applied; declared 13 TCB dependents confirmed exactly'},
    {'id': 'P-22/22b', 'what': 'whether the new `derived` retention is actually recomputed',
     'result': 'source_unit_ownership_faults re-derives every unitId and enforces both membership positions; my end-to-end recompute is stable, injective, admits # in markerPath, and names tampering',
     'failuresPreserved': "my first fixture used targetKind 'ts-program' against the Rust target-kind enum"}]

O['evidenceReceipts'] = {
    'interpreter': '/tmp/opensip-architecture-review-env/bin/python -I -B, launched via standard-library subprocess',
    'wrongInvocationsNotReadAsSourceFailure': True,
    'referenceSuites': {'evaluator3PinnedFiles': p19['pinnedFiles'],
                        'sourcePinsValid': p19['launcherReport']['sourcePinsValid'],
                        'children': p19['launcherReport']['checks'],
                        'allChildrenExitZero': p19['launcherReport']['allExitZero'],
                        'groupCheckers': len(p19['groups']),
                        'allGroupsExitZero': p19['allGroupsExitZero'],
                        'frozenDeviationsAfterRuns': p19['frozenDeviationsAfterRuns'],
                        'pinGateBypassed': False,
                        'reportWritersRanInVerifiedDisposableCopy': True},
    'exportReplay': {'positives': p14['counts']['positives'],
                     'falseResultControls': p14['counts']['falseResultControls'],
                     'bindingControls': p14['counts']['bindingControls'],
                     'ownerSha256': p14['ownerSha256'],
                     'positivesAdmitBoth': p14['positivesAllAdmitBoth'],
                     'negativesAdmitThenReplayRefuse': p14['negativesAdmitStructurallyThenReplayRefuse'],
                     'bindingInvalidDefaultRefused': p14['bindingInvalidDefaultRefused'],
                     'expectedOutputsTreatedAsCorrectnessEvidence': False},
    'portableReconstruction': {'allBuildsSucceeded': p15['allBuildsSucceeded'],
                               'storeFilesCompared': p15['storeFilesCompared'],
                               'storeFilesByteIdentical': p15['storeFilesByteIdentical'],
                               'runIdsIdentical': p15['claimRunIdsIdenticalEverywhere'],
                               'helperOverlayRequired': False},
    'packageVerifier': {'returncode': p16['returncode'],
                        'passed': (p16.get('verification') or {}).get('passed'),
                        'sourceFilesVerified': (p16.get('verification') or {}).get('sourceFilesVerified'),
                        'packageFilesVerified': (p16.get('verification') or {}).get('packageFilesVerified'),
                        'queryChecks': p16.get('queryChecks'),
                        'queryOutputsRegeneratedIdentical': p16['queryOutputsRegeneratedIdentical'],
                        'matchesRootRetainedReceipts': p16.get('myGroupsMatchRootGroups'),
                        'note': 'agreement with root receipts is corroboration; my basis is my own execution'}}

O['newMustIssues'] = []
O['newShouldIssues'] = []
O['advisories'] = [
    {'id': 'A-7', 'title': 'One native annotation record pointer still names identity-schemas.v2 as the owning document',
     'selectors': ['docs/coop/design-corrections/native/native-evidence.schemas.v2.json '
                   '$.$defs..ownerSourceDigest.x-opensip-digest.record.document',
                   'the bundle description naming foundation/identity-schemas.v2.json#/$defs/import'],
     'measured': ('All three record pointers resolve against frozen31. identity-schemas.v2.json is '
                  'still a frozen member, and its owner-source-set and import definitions are '
                  'BYTE-IDENTICAL to the v3 ones, so the legacy name binds the same record.'),
     'why_not_a_should': ('Nothing is dangling and nothing diverges: I compared the definitions and '
                          'they are equal. The digest-law standing already names v3 as current. This '
                          'is a document-name observation with no semantic consequence, and the file '
                          'is not in my 27->31 delta.'),
     'suggestion': 'Repoint the record document to identity-schemas.v3 if v2 is meant to be historical only.'},
    {'id': 'A-8', 'title': 'The preserved source29 failed receipt is not locatable among the inputs supplied to me',
     'selectors': ['claimed: source29 failed receipt preserved and not accepted',
                   'searched: frozen31 members, final31-independent-review-inputs.v1, '
                   'root-native-digest-catalog-correction.v1, root-rule-results-order-correction.v1, '
                   'root-independent27-advisory-corrections.v1, author-package-final31-verification.v1, '
                   'and every package7 historical preparation directory'],
     'measured': ('Zero matches. The source29 and source30 snapshots are also not inputs, so I could '
                  'not diff the 29->30 native-cases.v2.json edit directly.'),
     'why_not_a_should': ('This is an input-custody limit on MY evidence, not a defect in source31. '
                          'What I can verify I did verify: the same-byte-count digest-only shape of '
                          'the edit, and that every foundation drift guard and reference suite passes '
                          'on 31 with 1242 pins valid. I assess the current state as consistent and I '
                          'do not certify which single field moved or that the failed receipt was '
                          'preserved unaccepted.'),
     'suggestion': 'Supply the preserved source29 receipt, or the 29/30 manifests, if that sub-claim is to be independently checkable.'}]

O['resolvedSinceV27'] = {
    'A-4': {'status': 'RESOLVED',
            'basis': ('check-enumeration.v1.py now executes five internal-root controls on an '
                      'otherwise valid fixture with membershipDigest rebound so root admission is '
                      'reached. All five pass; the positive empty root admits; the four negatives '
                      'refuse with ONLY ENUMERATION_MEMBERSHIP_UNIT_ROOT plus the exact native '
                      'fault:location:selector prefix. My own guard-omission mutation makes all four '
                      'negatives fail, reproducing the original misattribution and silent-admit '
                      'failure modes. Token coverage moved from 0 of 27 checkers to 1 of 27 for each '
                      'of the four tokens.'),
            'shapeIAccept': ('JOIN controls, not a whole reminted Run. The guard runs at the '
                             'enumeration join, which precedes structural custody, so I do not insist '
                             'on the structural-ADMIT shape my v27 advisory suggested.')},
    'A-5': {'status': 'RESOLVED',
            'basis': ('evaluation-proof.v13.json and ep13.review-independent.json are now frozen31 '
                      'members with matching digests, so the proposal\'s source fields resolve where '
                      'they previously had zero occurrences. I read the AX6/AX9/MD5/RX2c statements '
                      'and the original declares exactly those four as escapedEveryGuard and '
                      'declaredBlindSpotVariants.'),
            'limit': ('Evidence restored, nothing repaired: no regrade, no rerun, no authentication '
                      'of the original measurements, and no historical file edited. The four rows '
                      'still carry no inline original of their own.')},
    'A-6': {'status': 'RESOLVED',
            'basis': ('verify-package.py now invokes check-author-query.py and assess-author-query.py '
                      'after the 13 Run/control outcomes and asserts all seven query checks. I '
                      'executed it against frozen source31: rc=0, 12895 source and 270 package files '
                      'verified, 13 outcomes plus 7 query checks, and my regenerated query outputs '
                      'are byte-identical to the retained copies. The README states that the property '
                      'and mixed-universe probes remain separate, with commands and receipts, and I '
                      'ran both separately.')},
    'note': ('All three advisories I recorded against source27 are addressed. No MUST or SHOULD was '
             'open against source27, so nothing of that kind carried forward.')}

O['limitations'] = [
    'Design, architecture, schema and reference layers only. No product implementation exists to test.',
    'The author package is AUTHOR-assisted evidence, never a blind result. No row is graded from its '
    'self-assessment and no expected output is treated as correctness evidence.',
    'The seven positives are not seven independent agreements: only TS checkpoint3 is helper-versus-'
    'owner; the other six are owner-derived and owner-replayed self-consistency, and the three '
    'negatives derive from checkpoint3.',
    'exists and none only. and/or/not remain unexercised; count-at-most and all-covered remain '
    'unimplemented in the partial helper.',
    'The two-binding construction is incomplete and the shipped control is single-explicit only, so '
    'AR-01 Q3 cannot be answered from this package. That is an evidence limit, not a demonstrated '
    'owner defect.',
    'Nothing here grants provider, compiler, OS or process-isolation qualification. An authenticated '
    'pure host/evaluator consuming inert typed data is what the bytes describe.',
    'I could not diff the 29->30 native-cases edit or locate the preserved source29 failed receipt '
    'among my inputs; see advisory A-8.',
    'Mutation testing of the native digest-law vocabulary is impossible through the checker, because '
    'the schema and checker are both source-pinned and the pin gate answers first. I exercised the '
    'enforcement predicate in memory instead and did not bypass the gate.',
    'All 54 commit-recovery cases and all 32 qualification gates remain unperformed product '
    'obligations; condition 5 is NOT MET.',
    'The original fresh blind 123/8/3 charter remains a separate requirement. I did not read or touch '
    'any blind runtime, report or output, and I claim no blind acceptance.',
    'Reading of unchanged owner files is inherited from my v27 complete reading after exact-byte '
    'verification, and is labelled inherited rather than presented as fresh.']

O['crossUnitStanding'] = {
    'evaluationResidualsRetained': 30, 'evaluationResidualsClosedByThisReview': 0,
    'condition2Obligations': 28, 'condition2ObligationsRetained': 28,
    'condition2Standing': ('All 28 remain OPEN for full-product integration. Nothing in the 27->31 '
                           'delta discharges any of them.'),
    'qualificationGates': 32, 'qualificationGatesPerformed': 0, 'condition5': 'NOT MET',
    'qualificationGateMeasurement': ('Re-measured on frozen31: all 32 rows carry qualified=false, '
                                     'demonstrated=false, implementationHarnessAuthored=false and '
                                     'standing DESIGN-CONTRACT-PENDING-REVIEW.'),
    'commitRecoveryCases': 54, 'commitRecoveryCasesExecuted': 0,
    'd9SuccessorObligation': ('DR-007 and DR-011-R08: the successor D9 artifact carrying '
                              'host-invariant remains a disclosed, attributed implementation '
                              'obligation of the D9 unit, carried forward and not closed.'),
    'blindCharter': ('The original 123/8/3 blind charter is a separate, still-required reconstruction. '
                     'Untouched and uninfluenced by this review.')}
O['dispositionStandingForEveryRow'] = {
    'appliedByThisReview': False, 'finalApplicationOutcomeGranted': False,
    'independentApplicationGradeAwarded': None,
    'appliesTo': 'every evaluation, AR, FW, inherited and scoped-owner row without exception'}
O['dispositionCounts'] = {'fDispositions': 14, 'evaluationResidualDispositions': 30,
                          'arDispositions': 16, 'fwDispositions': 15,
                          'inheritedResidualDispositions': 27, 'scopedReviewOwnerDispositions': 5,
                          'total': 107}
O['grantsNothing'] = {
    'grade': None, 'activation': False, 'implementationAuthorized': False, 'blindAcceptance': False,
    'applicationActivation': False, 'commitOrPush': False,
    'note': ('Design review only. No product implementation, activation, commit or push. The final '
             'application review is separate and must still grade the 30 evaluation residuals and the '
             '28 condition-2 obligations.')}

O['verdict'] = 'ACCEPT'
O['verdictBasis'] = (
    'Every declared input verified before use, the 27->31 delta derived independently and matching '
    'root\'s 16 paths with no removals, and all five source-delta items assessed substantively on '
    'actual source rather than by restating the accounts. The source28 ordering correction is complete '
    'and load-bearing, and I reproduced the regression myself. The source29 catalog defines `derived` '
    'from the existing UnitIdentityV1 recipe, adds no unused retention, replaces a stale count with a '
    'measured one, and is genuinely enforced end to end. The source30 fixture refresh leaves the '
    'current state consistent across every suite. My own source27 advisories A-4, A-5 and A-6 are all '
    'resolved, and the A-4 remedy is load-bearing under my own guard-omission mutation. All 13 author '
    'exports replay through both boundaries, and all 13 stores now rebuild byte-identical from frozen '
    'source31. All five root review-record corrections are accepted and applied to this report; the '
    'source27 report is left unchanged. No unresolved required issue: zero new MUST, zero new SHOULD, '
    'two advisories, each stating why it is not a SHOULD. This grants no application grade, no '
    'activation, no blind acceptance and no implementation authorization.')

json.dump(O, open(os.path.join(BASE, 'part4.json'), 'w'), indent=1)
print('part4 keys:', len(O), '| verdict:', O['verdict'])
