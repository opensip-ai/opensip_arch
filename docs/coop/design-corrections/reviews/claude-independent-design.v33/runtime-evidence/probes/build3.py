"""review.json part 3 — issues, advisories, TCB, standing, verdict."""
import json, os

BASE = '/tmp/opensip-design-corrections/claude-independent-design.v33'
REC = os.path.join(BASE, 'receipts')
B = json.load(open('/tmp/opensip-design-corrections/claude-independent32-reconciliation.v2/review.json'))


def rec(n):
    return json.load(open(os.path.join(REC, n)))


p03, p04, p05 = rec('p03-suites.json'), rec('p04-newlawcontrols.json'), rec('p05-fullrun.json')
p10, p11 = rec('p10-pins-planning.json'), rec('p11-package.json')
O = {}

O['newMustIssues'] = []
O['newShouldIssues'] = []
adv = [dict(a) for a in B['advisories']]
for a in adv:
    a['statusOn33'] = ('Carried unchanged: nothing in my derived 32->33 delta touches this advisory\'s '
                       'subject.')
adv.append({
    'id': 'A-11',
    'title': 'No source33-bound author package exists yet, so nine F rows cannot be evidenced on these bytes',
    'selectors': ['author-package-update.json (root-owned, status PENDING)',
                  'claude-author-package-successor.v9 (rebound from 8, current verification failed)',
                  'author-package-final33-verification.v1 (preserved receipts)'],
    'measured': ('The root input names no package10 manifest and no root verification. Package9 was '
                 'rebound from package8 rather than constructed on source33; under actual current '
                 'verification checkpoint3/author-ts, binding ts-lawful-default and binding '
                 'ts-lawful-explicit-selection structurally ADMIT then REFUSE '
                 'EVALUATOR_COMPLETE_PROOF_REPLAY, the expected invalid-program-entry refusal still '
                 'holds, normalized-examples6 and rust-selection-examples1 pass, the three '
                 'semantic-controls1 negatives refuse exactly as designed, query assessment then '
                 'failed and no final verification.json was emitted.'),
    'why_not_a_should': ('This is not a source defect. A historical source30 construction does not '
                         'become a new execution by rebinding, so a rebound package failing complete '
                         'proof replay under changed law is the CORRECT outcome and is evidence the '
                         'replay boundary works. It is an evidence-availability gap in my review '
                         'inputs, and the source itself carries no unresolved MUST or SHOULD.'),
    'consequence': ('F-01, F-02, F-03, F-05, F-06, F-08, F-10, F-11 and F-12 are recorded '
                    'PACKAGE-EVIDENCE-REVIEW-INCOMPLETE-ON-33 rather than carried forward as if '
                    'current. No package acceptance is inferred.'),
    'statusOn33': 'NEW in this review'})
O['advisories'] = adv

O['resolvedSinceV32'] = {
    'executionLawTwoOwnerContradiction': {
        'whatWasWrong': ('composition §9.6 explicitly prescribed a provider-unavailable fallback that '
                         'execution-inputs §4/§5 forbade — a contradiction between two normative '
                         'owners, so a host obeying one could not obey the other'),
        'status': 'RESOLVED IN THESE BYTES, WITH BOTH OWNERS CORRECTED TOGETHER',
        'howIVerified': ('read both changed owners; measured that the composition table now routes "no '
                         'Coverage records" to the account\'s derived primary pair (null/null) and that '
                         'execution-inputs forbids manufacturing a carrier; and confirmed four REFUSE '
                         'controls enforce it in the model'),
        'noteOnTheRecord': ('the contract also corrects the earlier diagnosis that called this a '
                            'reference-side invention, saying that reading was too narrow. I agree '
                            'with the correction and with recording it rather than quietly fixing it.')},
    'applicabilityPrecedenceNowPublishedAndControlled': {
        'status': 'RESOLVED',
        'evidence': ('five-token FIRST-MATCH order published as normative with an '
                     'x-opensip-applicability-precedence annotation; my exhaustive 108-cell grid '
                     'reaches all five tokens and the checker carries a 10-case precedence control '
                     'where every want equals got')},
    'externalUniverseJoinNowNormative': {
        'status': 'RESOLVED',
        'evidence': ('sourceUniverse equals the binding universe for every applicability, published '
                     'as x-opensip-external-joins because JSON Schema cannot compare another document; '
                     'four negative controls refuse EXECUTION_INPUTS_COVERAGE_DERIVE and two positive '
                     'controls admit')}}

O['evidenceReceipts'] = {
    'interpreter': '/tmp/opensip-architecture-review-env/bin/python -I -B',
    'changedInputSuites': {'jobs': [{'checker': j['checker'], 'rc': j.get('returncode'),
                                     'seconds': j.get('seconds'),
                                     'justification': j.get('justification')} for j in p03['jobs']],
                           'allExitZero': p03['allExitZero'],
                           'disposableCopyVerified': p03['disposableVerified']},
    'executionInputsControlSet': {'cases': p04['totalCases'], 'mismatches': len(p04['mismatches']),
                                  'admitting': p04['summary']['admittingControls'],
                                  'refusing': p04['summary']['refusingControls'],
                                  'fullRunRows': p04['summary']['fullRunRows'],
                                  'nullNullCarrierCases': p04['summary']['nullNullCarrierCases'],
                                  'externalUniverseJoinRows': p04['summary']['casesWithExternalUniverseJoin']},
    'fullRunRows': [{'case': x['case'], 'runId': x['runId'], 'verdict': x['verdict'],
                     'causePairs': x['executionCausePairs'],
                     'sameGraphDigest': x['sameGraphExecutionInputsDigest']}
                    for x in p05['fullRunRows']],
    'pinnedLauncher': p10.get('launcherReport'),
    'planningGroups': [{'checker': x['checker'], 'rc': x.get('returncode'),
                        'lastLine': x.get('lastLine')} for x in p10['planningGroups']],
    'frozenDeviationsAfterAllRuns': p10['frozenDeviationsAfterRuns'],
    'authorPackage': {'status': 'INCOMPLETE', 'rootInputSha256': p11['updateFileSha256']},
    'failedOrImpreciseProbesPreserved': [
        'p02 checked contract table order with a document-wide index() and reported False because the '
        'tokens appear in prose before the table; the table itself is in published order',
        'p05 allHaveProofRefDigest reads False only because the clean PASS row has no execution '
        'deficiency and so no refs',
        'p06 keyword heuristic flagged four provider-unavailable mentions as prescriptive; on reading, '
        'one is the quoted old prescription inside the correction-of-record and three are the LAWFUL '
        'carrier for a genuinely unavailable binding or receipt',
        'p07 envelope probe invented a record shape and refused on a missing required property; p08 '
        'redid it with root\'s own recorded instances',
        'p11 first read semantic-controls1 report.json passed=False as a failure; it is the designed '
        'outcome for false-result negatives and that field reports whether every check admitted']}

O['sharedAssumptionTCBSCOPE01'] = dict(B['sharedAssumptionTCBSCOPE01'])
O['sharedAssumptionTCBSCOPE01']['statusOn33'] = (
    'Unchanged on 33: admission-and-qualification.md is not in my derived 32->33 delta. Assessed once '
    'as ONE shared assumption over its 13 dependent rows, with the joint-reopening consequence intact.')
O['crossUnitStanding'] = dict(B['crossUnitStanding'])
O['crossUnitStanding']['statusOn33'] = (
    'All obligations carried forward unchanged: 28 condition-2 obligations retained, 32 product '
    'qualification gates unperformed with condition 5 NOT MET, 54 recovery cases unexecuted, and the '
    'D9 implementation obligation on DR-007 / DR-011-R08 persists.')
O['dispositionStandingForEveryRow'] = {
    'appliedByThisReview': False, 'finalApplicationOutcomeGranted': False,
    'independentApplicationGradeAwarded': None,
    'appliesTo': 'all 107 rows without exception'}
O['dispositionCounts'] = {'fDispositions': 14, 'evaluationResidualDispositions': 30,
                          'arDispositions': 16, 'fwDispositions': 15,
                          'inheritedResidualDispositions': 27, 'scopedReviewOwnerDispositions': 5,
                          'total': 107}
O['limitations'] = [
    'Design and reference layers only. No product implementation exists and none is demanded.',
    'The execution-inputs controls are reference fixture self-consistency, including the five full-Run '
    'rows. They are not blind reconstruction and not provider, compiler or OS qualification.',
    'The author package review is INCOMPLETE: the root-owned update is PENDING and no source33-bound '
    'package has been verified. Nine F rows are recorded incomplete rather than carried forward.',
    'Package9 is known stale and was NOT rerun; its failure is assessed from preserved receipts.',
    'The candidate-envelope result is schema admission ONLY — not a retained join, not a full Run, and '
    'not a retroactive success for the original author q2 command, which carried an invalid '
    'execution2 prefix and whose refusal stands.',
    'Root suite receipts and root assessments were treated as evidence to assess, never as authority; '
    'every conclusion here rests on my own execution against frozen33.',
    'A-10 limits retained: TS checkpoint is helper-versus-owner only, six owner-derived '
    'self-consistency, exists/none with other operator limitations, incomplete two-binding '
    'construction with a single explicit binding.',
    'A-9 repair controls retain their exact admitted-versus-unit limitations.',
    'All 30 author residual proposals remain PENDING independent grading.',
    'Unchanged readings are inherited only after exact-byte verification and are labelled as such.',
    'No consumer output, runtime, report or blind replay file was read; no blind oracle is an input.']
O['grantsNothing'] = {
    'grade': None, 'architectureReady': False, 'activation': False, 'implementationAuthorized': False,
    'blindAcceptance': False, 'packageAcceptance': False, 'finalApplicationOutcomeGranted': False,
    'commitOrPush': False,
    'stillRequired': ['completion of the author package evidence review on a source33-bound package',
                      'final application review and activation',
                      'successful original blind reconstruction',
                      'product qualification of the 32 gates and 54 recovery cases']}
O['verdict'] = 'ACCEPT-SOURCE-DESIGN-WITH-AUTHOR-PACKAGE-REVIEW-INCOMPLETE'
O['verdictBasis'] = (
    'SOURCE33 DESIGN: ACCEPT. Full custody verified — manifest and archive digests match, all 12,899 '
    'rows verified by hash and size with zero extras, the archive is byte-equal to the manifest across '
    'every member, and the declared parent is exactly the source32 I graded. My independently derived '
    'delta is 1 added, 0 removed, 17 changed, agreeing with root\'s inventory on all 18 paths. The '
    'changed execution law is substantively correct and controlled in BOTH directions: the five-token '
    'FIRST-MATCH precedence is published as normative and my exhaustive 108-cell grid reaches every '
    'token with the row-3-before-row-4 reachability argument holding; the external '
    'sourceUniverse-to-binding join holds for every applicability with four refusing and two admitting '
    'controls; a selected-U unsupported cell keeps its Coverage outside the account while disclosing '
    'the matrix pair and, when required, bridging to an indeterminate Run; pure missing work carries '
    '(null, null) and four controls refuse any attempt to claim provider-unavailable instead; the '
    'derived pair is taken whole from the first record that actually carries one; and the parent '
    'composition contract\'s previously prescribed provider-unavailable fallback — a genuine '
    'contradiction between two normative owners — is corrected together with execution-inputs and '
    'recorded honestly on the record. The control set is 75 cases with 0 mismatches, 41 admitting and '
    '34 refusing, including five full-Run rows with real run3 ids that assert exact proof '
    'ExecutionInputs digest equality. All six changed-input suites, the pinned launcher (1,244 pins, '
    '16/16 children) and both planning groups exit 0 with zero frozen deviations. Planning is '
    'consistent: layer4 binds 29 inputs that all resolve with exactly one repin, layer3/2/original25 '
    'are preserved, no .py is a normative input, and 198/20/320/54 are unchanged. Zero new MUST and '
    'zero new SHOULD against the source. '
    'AUTHOR PACKAGE: INCOMPLETE, NOT ACCEPTED. The root-owned update is still PENDING and names no '
    'package10 manifest or verification, so no source33-bound package has been verified and nine F '
    'rows are recorded incomplete rather than presented as current. Package9 was rebound rather than '
    'constructed on 33 and its actual verification failed on three positive cases; I assessed those '
    'preserved receipts without rerunning them and treat the failure as the correct outcome for a '
    'rebound package under changed law, not a source defect. '
    'This design review grants no application grade, no activation, no blind acceptance, no package '
    'acceptance and no implementation authorization.')
json.dump(O, open(os.path.join(BASE, 'part3.json'), 'w'), indent=1, default=str)
print('part3 keys:', len(O), '| verdict:', O['verdict'])
print('advisories:', [a['id'] for a in O['advisories']])
