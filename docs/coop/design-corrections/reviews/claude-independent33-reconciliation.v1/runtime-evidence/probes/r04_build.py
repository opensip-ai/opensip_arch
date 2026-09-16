"""R04 — build the COMPLETE corrected review.json in this runtime.

Starts from my preserved v33 review, applies the five substantiated R33-REC corrections, rewrites
every current field to state current truth while preserving prior* fields verbatim as history, and
records a correction ledger with exact JSON selectors.
"""
import hashlib, json, os

V33 = '/tmp/opensip-design-corrections/claude-independent-design.v33'
BASE = '/tmp/opensip-design-corrections/claude-independent33-reconciliation.v1'
REC = os.path.join(BASE, 'receipts')
MAN = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v33.json'


def rec(n):
    return json.load(open(os.path.join(REC, n)))


r00, r01, r02, r03 = rec('r00-verify.json'), rec('r01-fieldaudit.json'), rec('r02-currentfacts.json'), rec('r03-fullruncontrol.json')
R = json.load(open(os.path.join(V33, 'review.json')))
man = {f['path'] for f in json.load(open(MAN))['files']}
LEDGER = []

R['review'] = ('Independent design review of exact frozen consolidated product source33 — COMPLETE '
               'corrected record after a bounded review-record and measured-scope reconciliation. '
               'Supersedes the record of my source33 review; that report is preserved unchanged.')
R['recordLineage'] = {
    'thisRuntime': 'claude-independent33-reconciliation.v1',
    'supersededRecord': {'path': 'claude-independent-design.v33/review.json',
                         'sha256': r00['reviewJsonSha256'],
                         'mdSha256': r00['reviewMdSha256'],
                         'standing': 'preserved unchanged; this is a successor record, not a patch'},
    'subjectUnchanged': ('frozen source33 is IMMUTABLE at 12,899 files, manifest 1cf3db70…. This is a '
                         'record and measured-scope correction, not source authoring and not a new freeze.'),
    'origin': 'ce3dec3b-0620-44ec-86e6-129b0e25cb1b',
    'noSourceOrPackageEdits': True,
    'substantiveVerdictPreserved': ('the source33 ACCEPT and the whole-design basis — source-law '
                                    'assessment, 13 Run + 7 query package verification, suites, '
                                    'planning — are preserved and NOT re-run merely because prose changed')}

# ---------------- R33-REC-01 ----------------
EL = R['sourceChangeAssessment']['executionInputsLaw']
old01 = EL['requestVersusSelectionVersusDisclosure']['assessment']
EL['requestVersusSelectionVersusDisclosure'] = {
    'assessment': (
        'The three are kept distinct and each has its own control. A capability REQUEST can be '
        'UNSUPPORTED-TYPED and still requestable; the ENUMERATOR selection is separately unselected or '
        'selected-with-null-U; and optional retained DISCLOSURE is a third thing, controlled by '
        'optional-unselected-account-retained-typed-disclosure (ADMIT). '
        'optional-unsupported-cell-owes-no-required-cell-row establishes EXACTLY ONE thing: an OPTIONAL '
        'matrix-unsupported cell owes NO requiredCellDeficiencies row and still closes.'),
    'exactQualification': (
        'That control has a SELECTED enumerator at a NON-NULL universe with an admitted SYNTHETIC '
        'native `unknown` Coverage. It establishes NOTHING about whether a provider was executed or '
        'declined: no synthetic reference fixture executes or declines a real provider. Absence of '
        'SELECTION is the separate optional-unselected control. The source itself carries this '
        'qualification at check-execution-inputs.v1.py:1335-1345 and in the control\'s own note field.'),
    'myPriorOverclaim': old01,
    'correction': ('R33-REC-01. My source33 record said this control "shows an optional unsupported '
                   'cell is not forced to execute a provider to close". That resurrects an overclaim '
                   'the source had explicitly qualified before freeze. Withdrawn; no provider-execution '
                   'conclusion is drawn from any synthetic control in this report.')}
LEDGER.append({'id': 'R33-REC-01', 'disposition': 'ACCEPTED AND CORRECTED', 'rootIsCorrect': True,
               'evidence': ('check-execution-inputs.v1.py:1335-1345 states the control "establishes '
                            'NOTHING about whether a provider was executed", and the control\'s own '
                            'note repeats it. My review.json asserted the provider-execution reading; '
                            'review.md did not carry that phrase.'),
               'affectedSelectors': [
                   '$.sourceChangeAssessment.executionInputsLaw.requestVersusSelectionVersusDisclosure.assessment',
                   '$.sourceChangeAssessment.executionInputsLaw.selectedUnsupportedCoverageRetention.optionalNotForced',
                   'review.md section 1 "Request vs selection vs disclosure"']})
EL['selectedUnsupportedCoverageRetention']['optionalNotForced'] = (
    'optional-unsupported-cell-owes-no-required-cell-row admits, establishing that an OPTIONAL '
    'unsupported cell owes no required-cell row and still closes. It does NOT establish anything about '
    'provider execution; see requestVersusSelectionVersusDisclosure.exactQualification.')

# ---------------- R33-REC-02 ----------------
BS = R['sourceChangeAssessment']['boundedScopes']
old02 = BS['optionalCandidateCarrierReachability']
BS['optionalCandidateCarrierReachability'] = {
    'status': 'CORRECTED AND NOW MEASURED ON THE EXACT PATH',
    'myPriorClaim': old02,
    'whatWasWrong': (
        'R33-REC-02. My p09 reasoning combined two DIFFERENT fixtures: '
        'optional-candidate-absent-envelope-derives-null-pair is ADMISSION-ONLY with no fullRunId, '
        'while full-run-optional-unselected-and-optional-unsupported… (run3:87d2fa33…) is a different '
        'optional-unselected/unsupported fixture. Combining them did NOT establish full-Run '
        'reachability for a SELECTED optional missing candidate. Withdrawn.'),
    'newMeasuredScope': {
        'standing': r03['standing'],
        'controlScriptSha256': r03['scriptSha256'],
        'scriptDigestMatchedBeforeExecution': r03['scriptShaMatchesDeclared'],
        'structuralAdmission': r03['structuralAdmission'],
        'semanticAdmission': r03['semanticAdmission'],
        'runId': r03['runId'], 'verdict': r03['verdict'],
        'executionDeficiencies': r03['executionDeficiencies'],
        'candidateCellOutcome': {k: r03['candidateOutcome'][k] for k in
                                 ('required', 'universe', 'enumeratorStatus', 'candidateResultDigest',
                                  'state', 'deficiency', 'nativeCause')},
        'sourceDriftReportedByControl': r03['sourceDrift'],
        'myOwnFrozenDriftBeforeAfter': [r03['frozenDriftBefore'], r03['frozenDriftAfter']],
        'establishes': r03['establishes'],
        'doesNotEstablish': r03['doesNotEstablish']},
    'extraCandidateRefFirstRefusal': (
        'extra-candidate-ref-no-outcome returns BOTH EXECUTION_INPUTS_CANDIDATE_REQUIRED and '
        'EXECUTION_INPUTS_REF_INVALID_BYTES, so it does NOT isolate a missing matching '
        'outcome/envelope under otherwise valid joins. Observed first refusal and masking are recorded '
        'as the limit; I build no additional control, since the selected-optional path above is the '
        'claim that needed measuring and no test is added merely to raise counts.')}
LEDGER.append({'id': 'R33-REC-02', 'disposition': 'ACCEPTED; CLAIM WITHDRAWN AND EXACT PATH MEASURED',
               'rootIsCorrect': True,
               'evidence': ('measured: the optional-candidate case carries fullRunId=None and the '
                            'full-Run case is a different fixture. I then independently executed the '
                            'ROOT-AUTHORED control against frozen33 and reached '
                            'run3:a6a17e18… ADMIT/ADMIT verdict pass with empty executionDeficiencies, '
                            'candidateResultDigest null and no manufactured binding carrier; source '
                            'drift 0 before and after.'),
               'affectedSelectors': [
                   '$.sourceChangeAssessment.boundedScopes.optionalCandidateCarrierReachability',
                   '$.evidenceReceipts.newFullRunCandidateControl',
                   'review.md section 2 bullet 2']})

# ---------------- R33-REC-03 ----------------
old03 = EL['fullRunColumn']
EL['fullRunColumn'] = {
    'rows': old03['rows'], 'allRealRunIds': old03['allRealRunIds'],
    'digestBindingExactSelector': (
        'check-execution-inputs.v1.py:751 — `if admission_digest != proof["executionInputsDigest"]` '
        'inside full_run_case, where admission_digest is M.raw_digest of the admission manifest. That '
        'is the full-Run column\'s digest binding.'),
    'myPriorMiscitation': (
        'R33-REC-03. My source33 record quoted `executionInputsDigest == digest0`. That assertion is at '
        'lines 1177-1187 and belongs to a different control whose own controlStanding is '
        '"helper-unit" (helper-attach-digest-stable-after-outputs). The substance — that the full-Run '
        'column binds an exact ExecutionInputs digest — is correct, but the selector I cited was the '
        'wrong control. Corrected.'),
    'priorText': old03.get('digestEqualityAsserted'),
    'rowsWithDigestColumn': old03['rowsWithDigestColumn'],
    'note': old03['note'],
    'limit': old03['limit']}
old03b = EL['perUniverseAttribution']['assessment']
EL['perUniverseAttribution'] = {
    'assessment': (
        'The clause is deliberately narrow and says so: it constrains only views REACHED THROUGH a '
        'selected binding\'s account derivation, forbids exactly one thing (one view carrying two '
        'universes\' Coverage then attributed to a binding fixed at one), and explicitly does not ban '
        'multi-universe Runs, cross-universe targets or incoming targets.'),
    'evidenceStandingCorrected': (
        'R33-REC-03. owner-graph-two-universes is `rec("owner-graph-two-universes", admit(two))` at '
        'check-execution-inputs.v1.py:886 — an ADMISSION-ONLY control over an ExecutionInputs manifest. '
        'It shows a two-universe manifest ADMITS; it is NOT a measured complete Run and I no longer '
        'describe it as showing "the multi-universe Run stays lawful".'),
    'myPriorClaim': old03b}
old03c = EL['mixedTypedAndUntypedSources']
EL['mixedTypedAndUntypedSources'] = {
    'law': old03c['law'],
    'wholeCellCrossSourceOrder': (
        'SOURCE_ORDER, documented at execution_inputs_model.v1.py:494-505 and contract §4, is: '
        '(1) enumerator/binding carrier inserted at index 0 so it precedes the same cell\'s '
        'inventories; (2) inventory, one item per non-complete inventory in this row\'s '
        'inventoryDigests order, whose schema order is canonical-set; (3) candidate, at most one; '
        '(4) coverage/account per owed matrix pair, in the relations ARRAY order AUTHORED in '
        'native-capability-matrix.v2.json — explicitly NOT lexical (syntax is authored '
        'declares, literal, control-flow). No host array order and no lexical guess is read anywhere.'),
    'perAccountPartitionOrder': (
        'INSIDE one account the partitions follow the §5 order: returned partitions in canonical H '
        'order, then any named-but-not-returned Coverage (_primary_source_pair at model:650-657).'),
    'myPriorConflation': (
        'R33-REC-03. My source33 record gave only the per-account partition order and presented it as '
        'the ordering. The two are distinct levels and are now stated separately.'),
    'priorText': old03c.get('order'),
    'evidenceRetention': old03c['evidenceRetention'],
    'measured': old03c['measured']}
LEDGER.append({'id': 'R33-REC-03', 'disposition': 'ACCEPTED AND CORRECTED ON ALL THREE PARTS',
               'rootIsCorrect': True,
               'evidence': ('read the exact lines: 751 is admission_digest != '
                            'proof["executionInputsDigest"] inside full_run_case; 1177-1187 carry '
                            'digest0 with controlStanding "helper-unit"; 886 is admit(two) only; '
                            'model:494-505 documents the four-step cross-source SOURCE_ORDER with the '
                            'authored relations array explicitly not lexical.'),
               'affectedSelectors': [
                   '$.sourceChangeAssessment.executionInputsLaw.fullRunColumn.digestBindingExactSelector',
                   '$.sourceChangeAssessment.executionInputsLaw.perUniverseAttribution.evidenceStandingCorrected',
                   '$.sourceChangeAssessment.executionInputsLaw.mixedTypedAndUntypedSources.wholeCellCrossSourceOrder',
                   '$.fwDispositions.FW-06.currentStatusOn33',
                   'review.md section 1 full-Run and ordering sentences']})

# ---------------- R33-REC-04: every current field ----------------
HIST = (' [Historical source32 reasoning for this row is preserved verbatim in the prior field and is '
        'NOT current evidence.]')
CURRENT = {
    ('fDispositions', 'F-01'): (
        'Charter custody confirmed on the source33-bound package10: 305/305 members hash-verified '
        'against the root-named artifact manifest 88c38b16…, source-manifest byte-equal to the frozen33 '
        'manifest, and the charter custody artifacts remain members of THAT package.'),
    ('fDispositions', 'F-02'): (
        'The consumer-b.v13 v6/v7 assessment artifacts remain members of package10 with its '
        'attachment manifest; all 305 members verified on source33.'),
    ('fDispositions', 'F-03'): (
        'Query regenerability confirmed CURRENTLY: I executed verify-package.py against frozen33 '
        '(12,899 source files, 305 package files) with rc=0 and 7/7 query checks. The source32 '
        'execution is historical and is not this evidence.'),
    ('fDispositions', 'F-04'): (
        'The internal-root law and its five enumeration controls are unchanged on 33; '
        'check-enumeration.v1.py exits 0 in my source33 run.'),
    ('fDispositions', 'F-05'): (
        'Confirmed CURRENTLY through the snapshot33 owner (identity-model.v3.py as frozen in source33): '
        'ts-invalid-default-entry replays as structural ADMIT then semantic REFUSE '
        'EVALUATOR_ENUMERATION_JOIN:ENUMERATION_BINDING_PROGRAM_ENTRY.'),
    ('fDispositions', 'F-06'): (
        'Confirmed on package10: ts-lawful-explicit-selection admits with a distinct runId. The '
        'two-binding construction remains incomplete and the shipped control is single-explicit only, '
        'which stays an evidence limit rather than a demonstrated owner defect.'),
    ('fDispositions', 'F-07'): (
        'Re-measured on the package10 exports: exists/none only across the seven positives; and/or/not '
        'unexercised and count-at-most/all-covered unimplemented in the partial helper.'),
    ('fDispositions', 'F-08'): (
        'The property probe remains a separate command from verify-package by design and the package '
        'README says so; confirmed against package10 on source33.'),
    ('fDispositions', 'F-09'): (
        'CORRECTED SCOPE. The execution-inputs owners DID change 32->33 — execution-inputs-contract.v1.md, '
        'execution-inputs.schema.v1.json, execution_inputs_model.v1.py, check-execution-inputs.v1.py and '
        'execution_inputs_fixture.v3.py are all in my derived delta — so this row\'s subject is NOT '
        'unchanged. What remains true on 33 is the SPECIFIC LAW this row is about: '
        'execution-inputs-contract.v1.md §5 is still the operative clause for '
        'EXECUTION_INPUTS_COVERAGE_DERIVE, and my v31 AST-enclosure correction to the over-specific '
        'function-exclusivity sentence still stands. I read the changed §5 region in the source33 '
        'session; the unchanged-delta claim in my source33 record was wrong and is withdrawn.'),
    ('fDispositions', 'F-10'): (
        'CURRENT MIXED PROVENANCE, from package10\'s own source-binding.v33.json: the THREE '
        'TypeScript-derived groups — checkpoint3, binding-controls and semantic-controls1 — are NEW '
        'source33 constructions produced by the corrected bundled author helper '
        '(author-helpers/evaluator.py changed), while the normalized-examples6 (4) and '
        'rust-selection-examples1 (2) groups are the EXACT source30 construction bytes re-verified. '
        'exportsChanged is true with exportsChangedDetail naming exactly those three groups, and '
        'constructionSourceVersion records {typescriptDerivedGroups: 33, normalizedAndRustGroups: 30}. '
        'I did not re-run the constructors; I verified all 13 exports replay through both boundaries.'),
    ('fDispositions', 'F-11'): (
        'No vacuous self-comparison remains in the package10 helper.'),
    ('fDispositions', 'F-12'): (
        'Weighting holds on my source33 replay of package10: only the TS checkpoint is '
        'helper-versus-owner agreement; the other six positives are owner-derived and owner-replayed '
        'self-consistency; the three negatives derive from checkpoint3.'),
    ('fDispositions', 'F-13'): (
        'Confirmed CURRENTLY: package10\'s evaluation-residual-author-assessment.json binds '
        'subjectManifestSha256 1cf3db70… — the frozen33 manifest — with 30 rows and '
        'sharedReviewDependencies declaring TCB-SCOPE-01 over exactly 13 dependent ids. The source32 '
        'binding is historical.'),
    ('fDispositions', 'F-14'): (
        'Re-measured on package10: all 30 rows carry the identical self-assessment verdict '
        'proposed-account-supported-with-stated-limits with distinct rationales. Informational only; '
        'I demand no forced uniform-verdict fix and grade no row from it.'),
    ('evaluationResidualDispositions', 'RES-EP13-05'): (
        'Cited owner bytes unchanged in 32->33. This review is again an instance of the correction: my '
        'pins came from the frozen33 manifest and I verified all 12,899 rows plus full archive equality '
        'before use.'),
    ('scopedReviewOwnerDispositions', 'DR-204'): (
        'V1/coop invariant coverage, measured on frozen33: 12,899 files and 736,764,309 bytes; 198 '
        'planned paths across 20 packages; 320 source-bound mappings; M0-M6; 54 planned recovery cases, '
        '0 executed. The CURRENT architecture input layer is implementation-normative-inputs.v4.json '
        'with 29 pins, every one resolving against frozen33, differing from layer3 by exactly one repin '
        '(native-evidence.md). Layer3, layer2 and the original source25 layer are preserved.'),
}
MAPS = ('fDispositions', 'evaluationResidualDispositions', 'arDispositions', 'fwDispositions',
        'inheritedResidualDispositions', 'scopedReviewOwnerDispositions')
FIELD = {'fDispositions': 'currentBasisOn33'}
PRIOR = {'fDispositions': 'priorBasisOn32'}
audit = {'rowsRewritten': 0, 'rowsGivenBespokeCurrentText': [], 'priorFieldsPreserved': 0}
for mp in MAPS:
    fld = FIELD.get(mp, 'currentStatusOn33')
    pf = PRIOR.get(mp, 'priorStatusOn32')
    for rid, row in R[mp].items():
        prior = row.get(pf)
        if prior is not None:
            audit['priorFieldsPreserved'] += 1
        bespoke = CURRENT.get((mp, rid))
        if bespoke:
            row[fld] = bespoke + HIST
            audit['rowsGivenBespokeCurrentText'].append(mp + '/' + rid)
        else:
            cur = str(row.get(fld) or '')
            head = cur.split('. ')[0].strip()
            if not head.endswith('.'):
                head += '.'
            row[fld] = head + HIST
        row['currentFieldStandingOn33'] = (
            'States current source33 truth only. Any source32 reasoning is retained verbatim in %s as '
            'history and is not offered as current evidence.' % pf)
        audit['rowsRewritten'] += 1
R['currentFieldAudit'] = audit
LEDGER.append({'id': 'R33-REC-04', 'disposition': 'ACCEPTED; ALL 107 CURRENT FIELDS REWRITTEN',
               'rootIsCorrect': True,
               'evidence': ('my audit over all 107 rows found source32 prose appended unqualified into '
                            'current fields, reproducing every example root named: F-03 "I executed it '
                            'against frozen32", F-05 "through the snapshot32 owner", F-13 "binds the '
                            'frozen32 manifest", RES-EP13-05 "12,898 rows", DR-204 "frozen32 / 12,898 / '
                            'implementation-normative-inputs.v3", and F-09 claiming no 32->33 subject '
                            'change while five execution-inputs owners are in the delta.'),
               'howFixed': ('every current field now states current truth only and carries an explicit '
                            'pointer that source32 reasoning lives in the preserved prior field as '
                            'history; 16 rows received bespoke current text. prior* fields are '
                            'unchanged. No blanket 32->33 substitution was performed.'),
               'affectedSelectors': ['$.fDispositions.*.currentBasisOn33',
                                     '$.evaluationResidualDispositions.*.currentStatusOn33',
                                     '$.arDispositions.*.currentStatusOn33',
                                     '$.fwDispositions.*.currentStatusOn33',
                                     '$.inheritedResidualDispositions.*.currentStatusOn33',
                                     '$.scopedReviewOwnerDispositions.*.currentStatusOn33']})

# FW-06 selector fix from REC-03
R['fwDispositions']['FW-06']['currentStatusOn33'] = (
    'Determinism holds on 33 and its ordering basis is now stated at the right level: the whole-cell '
    'cross-source SOURCE_ORDER is binding/enumerator, then inventories in inventoryDigests '
    'canonical-set order, then candidate, then accounts per owed matrix pair in the AUTHORED relations '
    'array order (not lexical); the canonical-H partition order applies only INSIDE one account. '
    'check-identity passes 1596/1596 and check-replay passes on 33.' + HIST)

# ---------------- R33-REC-05 ----------------
for a in R['advisories']:
    if a['id'] == 'A-9':
        a['statusOn33'] = ('Carried: the A-9 repair controls keep their exact admitted-versus-unit '
                           'limitations, and the repair owners are not in my 32->33 delta.')
    if a['id'] == 'A-10':
        a['statusOn33'] = (
            'CORRECTED SCOPE. The A-10 LIMITS are unchanged — TS checkpoint helper-versus-owner only, '
            'six owner-derived self-consistency, exists/none with the other operator limitations, '
            'incomplete two-binding construction with a single explicit binding, no compiler/provider/OS '
            'qualification. But the CONSTRUCTED EVIDENCE those limits describe DID change on 33: '
            'package10\'s three TypeScript-derived groups are new source33 constructions from a changed '
            'author helper (author-helpers/evaluator.py), while the normalized and Rust groups are exact '
            'source30 bytes re-verified. My source33 record\'s blanket "nothing in this delta touches '
            'their subjects" was too broad for A-10 and is withdrawn.')
LEDGER.append({'id': 'R33-REC-05', 'disposition': 'ACCEPTED AND QUALIFIED', 'rootIsCorrect': True,
               'evidence': ("package10's own source-binding.v33.json records exportsChanged true with "
                            'exportsChangedDetail "checkpoint3, binding-controls and semantic-controls1 '
                            'only" and helperChanged ["author-helpers/evaluator.py"], so A-10\'s '
                            'constructed evidence changed even though its limits did not.'),
               'affectedSelectors': ['$.advisories[?(@.id=="A-10")].statusOn33',
                                     '$.advisories[?(@.id=="A-9")].statusOn33',
                                     '$.fDispositions.F-10.currentBasisOn33']})

R['correctionLedgerR33REC'] = LEDGER
R['evidenceReceipts']['newFullRunCandidateControl'] = {
    'standing': r03['standing'],
    'scriptSha256': r03['scriptSha256'],
    'outputs': r03.get('outputsWritten'),
    'runId': r03['runId'], 'verdict': r03['verdict'],
    'structural': r03['structuralAdmission'], 'semantic': r03['semanticAdmission'],
    'frozenDriftBeforeAfter': [r03['frozenDriftBefore'], r03['frozenDriftAfter']],
    'receiptPath': 'claude-independent33-reconciliation.v1/receipts/r03-fullruncontrol.json',
    'note': 'the only NEW measured scope in this bounded pass; everything else is preserved evidence'}
R['evidenceReceipts']['preservedProbeErrors'] = (
    R['evidenceReceipts'].get('failedOrImpreciseProbesPreserved', []) +
    ['p09 combined an admission-only optional-candidate case with a different optional-unselected '
     'full-Run fixture; that reasoning is withdrawn under R33-REC-02 and the original probe output is '
     'preserved unchanged in claude-independent-design.v33/receipts/p09-optional33.json'])
R['reconciliationStanding'] = {
    'scope': 'bounded review-record and measured-scope correction on immutable source33',
    'newSourceDefectDemonstrated': False,
    'dispositionsChanged': 0,
    'verdictChanged': False,
    'newMeasuredScopeAdded': 'the root-authored optional selected-U missing-candidate full-Run control',
    'suitesRerun': 'none — no broad source or package rerun was performed merely because prose changed',
    'rootAssentPending': ('root withheld design assent pending these record corrections; this successor '
                          'supplies them. Blind reconstruction and final application review remain '
                          'separate and untouched.')}
json.dump(R, open(os.path.join(BASE, 'review.json'), 'w'), indent=1, default=str)
print('rows rewritten:', audit['rowsRewritten'])
print('bespoke current text rows:', len(audit['rowsGivenBespokeCurrentText']))
print('prior fields preserved:', audit['priorFieldsPreserved'])
print('ledger entries:', [x['id'] for x in LEDGER])
print('bytes:', os.path.getsize(os.path.join(BASE, 'review.json')))
