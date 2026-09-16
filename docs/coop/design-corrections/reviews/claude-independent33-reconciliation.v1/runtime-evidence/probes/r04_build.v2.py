"""R04 (v2, final) — build the COMPLETE corrected review.json in this runtime.

Starts from my preserved source33 review, applies the five substantiated R33-REC corrections, rewrites
every current field so it states current source33 truth while preserving prior* fields verbatim as
explicit history, and records a correction ledger with exact JSON selectors.

No source, package or old-review bytes are written. Frozen source33 stays immutable.
(r04_build.py is the earlier draft of this script, kept for the record.)
"""
import hashlib, json, os

V33 = '/tmp/opensip-design-corrections/claude-independent-design.v33'
BASE = '/tmp/opensip-design-corrections/claude-independent33-reconciliation.v1'
REC = os.path.join(BASE, 'receipts')
MAN = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v33.json'

r00 = json.load(open(os.path.join(REC, 'r00-verify.json')))
r03 = json.load(open(os.path.join(REC, 'r03-fullruncontrol.json')))
R = json.load(open(os.path.join(V33, 'review.json')))
p01 = json.load(open(os.path.join(V33, 'receipts', 'p01-delta.json')))
DELTA = sorted([c['path'] for c in p01['changed']] + [a['path'] for a in p01['added']])
LEDGER = []

R['review'] = ('Independent design review of exact frozen consolidated product source33 — COMPLETE '
               'corrected record after a bounded review-record and measured-scope reconciliation. '
               'Supersedes the record of my source33 review, which is preserved unchanged.')
R['recordLineage'] = {
    'thisRuntime': 'claude-independent33-reconciliation.v1',
    'supersededRecord': {'path': 'claude-independent-design.v33/review.json',
                         'sha256': r00['reviewJsonSha256'], 'mdSha256': r00['reviewMdSha256'],
                         'standing': 'preserved unchanged on disk; this is a successor record, not a patch'},
    'subjectUnchanged': ('frozen source33 is IMMUTABLE at 12,899 files, manifest 1cf3db70d4b73b0c42f13'
                         '93331e6a874ee26f7ddf67aa05c6ac15a5753069299. This pass is a record and '
                         'measured-scope correction: not source authoring and not a new source freeze.'),
    'origin': 'ce3dec3b-0620-44ec-86e6-129b0e25cb1b',
    'substantiveVerdictPreserved': ('the source33 ACCEPT and its basis — source-law assessment, the six '
                                    'changed-input suites, the 13-case + 7-query package verification, '
                                    'planning layer4 — are preserved and were NOT re-run merely because '
                                    'prose changed. Only the newly measured control below is new.'),
    'writesConfinedTo': 'claude-independent33-reconciliation.v1'}

# ---------------------------------------------------------------- R33-REC-01
EL = R['sourceChangeAssessment']['executionInputsLaw']
old01 = EL['requestVersusSelectionVersusDisclosure']['assessment']
EL['requestVersusSelectionVersusDisclosure'] = {
    'assessment': (
        'The three stay distinct and each has its own control. A capability REQUEST can be '
        'UNSUPPORTED-TYPED and still requestable; ENUMERATOR selection is separately unselected or '
        'selected-at-null-U; optional retained DISCLOSURE is a third thing, controlled by '
        'optional-unselected-account-retained-typed-disclosure. '
        'optional-unsupported-cell-owes-no-required-cell-row establishes EXACTLY ONE thing: an OPTIONAL '
        'matrix-unsupported cell owes NO requiredCellDeficiencies row and still closes.'),
    'exactQualification': (
        'That control has a SELECTED enumerator at a NON-NULL universe with an admitted SYNTHETIC '
        'native `unknown` Coverage. It establishes NOTHING about whether a provider was executed or '
        'declined to execute: no synthetic reference fixture executes or declines a real provider. '
        'Absence of SELECTION is the separate optional-unselected control. The source carries this '
        'qualification itself at check-execution-inputs.v1.py:1335-1345 and repeats it in the '
        "control's own note field."),
    'correctionR33REC01': (
        'My source33 record said this control shows an optional unsupported cell "is not forced to '
        'execute a provider to close". That resurrects an overclaim the source had explicitly '
        'qualified before freeze. WITHDRAWN. No provider-execution conclusion is drawn anywhere in '
        'this report from any synthetic control.'),
    'priorTextPreserved': old01}
EL['selectedUnsupportedCoverageRetention']['optionalNotForced'] = (
    'optional-unsupported-cell-owes-no-required-cell-row ADMITS, establishing that an OPTIONAL '
    'unsupported cell owes no required-cell row and still closes. It establishes nothing about '
    'provider execution — see requestVersusSelectionVersusDisclosure.exactQualification.')
LEDGER.append({
    'id': 'R33-REC-01', 'disposition': 'ACCEPTED AND CORRECTED', 'rootIsCorrect': True,
    'evidence': ('check-execution-inputs.v1.py:1335-1345 states in the source itself that the control '
                 '"establishes NOTHING about whether a provider was executed", and the recorded control '
                 'note repeats it. Measured: my review.json carried the provider-execution reading; my '
                 'review.md did not carry that phrase.'),
    'affectedSelectors': [
        '$.sourceChangeAssessment.executionInputsLaw.requestVersusSelectionVersusDisclosure.assessment',
        '$.sourceChangeAssessment.executionInputsLaw.requestVersusSelectionVersusDisclosure.exactQualification',
        '$.sourceChangeAssessment.executionInputsLaw.selectedUnsupportedCoverageRetention.optionalNotForced',
        'review.md §1 "Request versus selection versus disclosure"']})

# ---------------------------------------------------------------- R33-REC-02
BS = R['sourceChangeAssessment']['boundedScopes']
old02 = BS['optionalCandidateCarrierReachability']
BS['optionalCandidateCarrierReachability'] = {
    'status': 'CLAIM WITHDRAWN AND THE EXACT PATH NOW MEASURED',
    'whatWasWrong': (
        'R33-REC-02. My p09 reasoning combined two DIFFERENT fixtures. '
        'optional-candidate-absent-envelope-derives-null-pair is ADMISSION-ONLY and carries '
        'fullRunId null; the only full-Run case in that probe is '
        'full-run-optional-unselected-and-optional-unsupported (run3:87d2fa33…), a different '
        'optional-unselected + unsupported fixture. Combining them did NOT establish full-Run '
        'reachability for a SELECTED optional cell with a missing candidate. Withdrawn.'),
    'priorClaimPreserved': old02,
    'newMeasuredScope': {
        'standing': r03['standing'],
        'controlScriptSha256': r03['scriptSha256'],
        'digestMatchedRootDeclaredBeforeExecution': r03['scriptShaMatchesDeclared'],
        'structuralAdmission': r03['structuralAdmission'],
        'semanticAdmission': r03['semanticAdmission'],
        'runId': r03['runId'],
        'verdict': r03['verdict'],
        'executionDeficiencies': r03['executionDeficiencies'],
        'candidateCellOutcome': r03['candidateOutcome'],
        'sourceDriftReportedByControl': r03['sourceDrift'],
        'myOwnFrozen33DriftBeforeAfter': [r03['frozenDriftBefore'], r03['frozenDriftAfter']],
        'establishes': r03['establishes'],
        'doesNotEstablish': r03['doesNotEstablish']},
    'extraCandidateRefFirstRefusalLimit': (
        'extra-candidate-ref-no-outcome returns BOTH EXECUTION_INPUTS_CANDIDATE_REQUIRED and '
        'EXECUTION_INPUTS_REF_INVALID_BYTES, so it does NOT isolate a missing matching outcome or '
        'envelope under otherwise valid joins: the first refusal masks the second condition. That '
        'observed masking is recorded as the limit. I add no further control, because the '
        'selected-optional full-Run path was the claim that needed measuring and no test is written '
        'merely to raise a count.')}
LEDGER.append({
    'id': 'R33-REC-02', 'disposition': 'ACCEPTED; CLAIM WITHDRAWN AND THE EXACT PATH MEASURED',
    'rootIsCorrect': True,
    'evidence': ('measured from my own preserved p09 receipt: the optional-candidate case carries '
                 'fullRunId null and the full-Run case is a different fixture. I then independently '
                 'executed the ROOT-AUTHORED control (sha e32d15f0…, digest verified before running) '
                 'against frozen33 and reached run3:a6a17e18de4555538b55defc75925113ff96946403316e322e'
                 'eeeb5a3c1de189a: structural ADMIT, semantic ADMIT, verdict pass, executionDeficiencies '
                 'empty, the candidate cell required false at a non-null universe with enumeratorStatus '
                 'selected, candidateResultDigest null, deficiency null and nativeCause null. '
                 'Frozen33 drift 0 before and 0 after.'),
    'standingOfThatControl': ('root-authored control independently executed and verified by me; NOT a '
                              'new independent consumer implementation and not my own construction'),
    'affectedSelectors': [
        '$.sourceChangeAssessment.boundedScopes.optionalCandidateCarrierReachability',
        '$.sourceChangeAssessment.boundedScopes.optionalCandidateCarrierReachability.newMeasuredScope',
        '$.evidenceReceipts.newFullRunCandidateControl',
        'review.md §2 optional-candidate bullet']})

# ---------------------------------------------------------------- R33-REC-03
old03 = dict(EL['fullRunColumn'])
EL['fullRunColumn'] = {
    'rows': old03['rows'], 'allRealRunIds': old03['allRealRunIds'],
    'rowsWithDigestColumn': old03['rowsWithDigestColumn'],
    'digestBindingExactSelector': (
        'check-execution-inputs.v1.py:751 — `if admission_digest != proof["executionInputsDigest"]` '
        'inside full_run_case, where admission_digest is M.raw_digest(admission_inputs'
        '["execution_inputs"]) computed at line 742 and the case records controlStanding "closed-run". '
        "That is the full-Run column's ExecutionInputs digest binding."),
    'correctionR33REC03': (
        'My source33 record quoted `attached["graph"]["inputs"]["executionInputsDigest"] == digest0`. '
        'That assertion is at lines 1177-1187 and belongs to a control whose own controlStanding is '
        '"helper-unit", not to the full-Run column. The substance — that the full-Run column binds an '
        'exact ExecutionInputs digest — survives; the selector I cited was the wrong control and is '
        'corrected.'),
    'priorTextPreserved': old03.get('digestEqualityAsserted'),
    'note': old03.get('note'), 'limit': old03.get('limit')}
old03b = EL['perUniverseAttribution']['assessment']
EL['perUniverseAttribution'] = {
    'assessment': (
        'The clause is deliberately narrow and says so. It constrains only views REACHED THROUGH a '
        "selected binding's account derivation, forbids exactly one thing — one view carrying two "
        "universes' Coverage then attributed to a binding fixed at one — and explicitly does not ban "
        'multi-universe Runs, cross-universe targets or incoming targets.'),
    'evidenceStandingCorrectedR33REC03': (
        'owner-graph-two-universes is `rec("owner-graph-two-universes", admit(two))` at '
        'check-execution-inputs.v1.py:886 — an ADMISSION-ONLY control over an ExecutionInputs manifest. '
        'It shows a two-universe manifest admits. It is NOT a measured complete Run, and I no longer '
        'describe it as showing that the multi-universe Run stays lawful end to end.'),
    'priorTextPreserved': old03b}
old03c = dict(EL['mixedTypedAndUntypedSources'])
EL['mixedTypedAndUntypedSources'] = {
    'law': old03c['law'],
    'wholeCellCrossSourceOrder': (
        'SOURCE_ORDER — contract §4, documented at execution_inputs_model.v1.py:494-505 — is: '
        "(1) the enumerator/binding carrier, inserted at index 0 so it precedes the same cell's "
        "inventories; (2) inventory, one item per non-complete inventory, in the order of this row's "
        'inventoryDigests, whose schema order is canonical-set; (3) candidate, at most one, for a '
        'candidate-only capability; (4) coverage/account per owed matrix pair, in the relations ARRAY '
        'order AUTHORED in native-capability-matrix.v2.json#/capabilities[id]/relations — explicitly '
        'NOT lexical, since syntax is authored declares, literal, control-flow. No host array order '
        'and no lexical guess is read anywhere in it.'),
    'perAccountPartitionOrder': (
        'INSIDE one account the partitions follow the §5 order: returned partitions in canonical H '
        'order, then any named-but-not-returned Coverage (_primary_source_pair, model:650-662). '
        '_outcome_from_items takes the pair WHOLE from the first source that actually carries a typed '
        'pair (model:617-628), which is what prevents an untyped source from masking a typed one.'),
    'correctionR33REC03': (
        'My source33 record gave only the per-account partition order and presented it as the ordering '
        'for the cell. Those are two different levels and are now stated separately: the per-account '
        'partition order is not the whole-cell cross-source order.'),
    'priorTextPreserved': old03c.get('order'),
    'evidenceRetention': old03c.get('evidenceRetention'), 'measured': old03c.get('measured')}
LEDGER.append({
    'id': 'R33-REC-03', 'disposition': 'ACCEPTED AND CORRECTED ON ALL THREE PARTS', 'rootIsCorrect': True,
    'evidence': ('read at the exact lines in frozen33: 751 is `admission_digest != '
                 'proof["executionInputsDigest"]` inside full_run_case (controlStanding "closed-run"); '
                 '1177-1187 carry digest0 under controlStanding "helper-unit"; 886 is '
                 'rec("owner-graph-two-universes", admit(two)) with no Run; and '
                 'execution_inputs_model.v1.py:494-505 documents the four-step cross-source '
                 'SOURCE_ORDER whose account step follows the authored relations array, not lexical '
                 'order.'),
    'affectedSelectors': [
        '$.sourceChangeAssessment.executionInputsLaw.fullRunColumn.digestBindingExactSelector',
        '$.sourceChangeAssessment.executionInputsLaw.perUniverseAttribution.evidenceStandingCorrectedR33REC03',
        '$.sourceChangeAssessment.executionInputsLaw.mixedTypedAndUntypedSources.wholeCellCrossSourceOrder',
        '$.sourceChangeAssessment.executionInputsLaw.mixedTypedAndUntypedSources.perAccountPartitionOrder',
        '$.fwDispositions.FW-06.currentStatusOn33',
        'review.md §1 full-Run digest sentence and ordering sentence']})

# ---------------------------------------------------------------- R33-REC-04
HIST = (' [HISTORY: the source32 reasoning for this row is preserved verbatim in %s and is not offered '
        'as current evidence.]')
PKG10 = ('Verified on the source33-bound package10: artifact manifest matches the root-named digest '
         '88c38b16…, 305/305 members hash-verified, source-manifest byte-equal to the frozen33 '
         'manifest, all 13 Run/control cases replay as expected through BOTH open_run_closure and '
         'close_run with my own decoder, and verify-package.py exits 0 over 12,899 source files with '
         '7/7 query checks.')
CURRENT = {
    ('fDispositions', 'F-01'): PKG10 + (
        ' Row-specific on 33: the charter custody artifacts remain members of THAT package and are '
        'among the 305 verified members.'),
    ('fDispositions', 'F-02'): PKG10 + (
        ' Row-specific on 33: the consumer-b.v13 v6/v7 assessment artifacts remain frozen in package10 '
        'with their attachment manifest and verify among the 305 members.'),
    ('fDispositions', 'F-03'): PKG10 + (
        ' Row-specific on 33: verify-package.py again runs the query reproduction after the 13 outcomes '
        'and asserts all seven. I executed it MYSELF AGAINST FROZEN33 — rc 0, 12,899 source files, 305 '
        'package files, query count 7.'),
    ('fDispositions', 'F-04'): (
        "CORRECTED SCOPE on 33. This row's owner IS in my derived 32->33 delta: "
        'enumeration-contract.v1.md changed (+1844 bytes). I read the changed region this pass and '
        're-ran the owning suite: check-enumeration.v1.py exits 0 on frozen33. The internal-root law '
        'and its five enumeration controls are unchanged in substance; the previous "nothing in the '
        'delta touches this subject" phrasing was wrong for this row and is withdrawn.'),
    ('fDispositions', 'F-05'): PKG10 + (
        ' Row-specific on 33: ts-invalid-default-entry replays as structural ADMIT then semantic REFUSE '
        'EVALUATOR_ENUMERATION_JOIN:ENUMERATION_BINDING_PROGRAM_ENTRY through the SNAPSHOT33 owner — '
        'identity-model.v3.py as frozen in source33 — not through any earlier snapshot.'),
    ('fDispositions', 'F-06'): PKG10 + (
        ' Row-specific on 33: the dead parameter is gone and ts-lawful-explicit-selection admits with a '
        'distinct runId. The two-binding construction remains incomplete and the shipped control is '
        'single-explicit only, which stays an evidence limit rather than a demonstrated owner defect.'),
    ('fDispositions', 'F-07'): (
        "CORRECTED SCOPE on 33. The 32->33 delta is a SOURCE delta and does not touch this row's "
        "source owners, but this row's EVIDENCE is package-borne and the package was rebuilt: "
        "re-measured on package10's own exports, predicate coverage is exists/none only across the "
        'seven positives, with and/or/not unexercised and count-at-most and all-covered unimplemented '
        'in the partial helper. The disclosure remains accurate on 33.'),
    ('fDispositions', 'F-08'): PKG10 + (
        ' Row-specific on 33: the property probe remains a separate command from verify-package by '
        'design, the package README says so, and the effective-edition assertions are unchanged.'),
    ('fDispositions', 'F-09'): (
        'CORRECTED SCOPE on 33. The execution-inputs owners DID change in 32->33 — '
        'execution-inputs-contract.v1.md, execution-inputs.schema.v1.json, execution_inputs_model.v1.py, '
        'check-execution-inputs.v1.py and execution_inputs_fixture.v3.py are all in my derived 18-file '
        "delta — so this row's subject is NOT untouched and my previous \"nothing in my derived 32->33 "
        'delta touches this row\'s subject" was wrong. What remains true on 33 is the SPECIFIC claim '
        'this row is about: execution-inputs-contract.v1.md §5 is still the operative clause for '
        'EXECUTION_INPUTS_COVERAGE_DERIVE, and my v31 AST-enclosure correction to the over-specific '
        'function-exclusivity sentence still stands. I read the changed §5 region during the source33 '
        'review and check-execution-inputs.v1.py exits 0 on frozen33.'),
    ('fDispositions', 'F-10'): PKG10 + (
        " Row-specific on 33, with MIXED provenance taken from package10's own source-binding.v33.json: "
        'the THREE TypeScript-derived groups — checkpoint3, binding-controls and semantic-controls1 — '
        'are NEW source33 constructions produced by the corrected bundled author helper, with '
        'helperChanged naming author-helpers/evaluator.py and exportsChangedDetail naming exactly those '
        'three groups; the normalized-examples6 (4 cases) and rust-selection-examples1 (2 cases) groups '
        'are the EXACT source30 construction bytes, re-verified rather than rebuilt. The file records '
        'constructionSourceVersion {typescriptDerivedGroups: 33, normalizedAndRustGroups: 30} and '
        'currentVerificationSourceVersion 33. I did NOT re-run the constructors; I verified that all 13 '
        'exports replay through both boundaries.'),
    ('fDispositions', 'F-11'): PKG10 + (
        ' Row-specific on 33: no vacuous self-comparison remains in the package10 helper.'),
    ('fDispositions', 'F-12'): PKG10 + (
        ' Row-specific on 33, from my own replay: only checkpoint3/author-ts is helper-versus-owner '
        'agreement; the other six positives are owner-derived and owner-replayed self-consistency; the '
        'three negatives derive from checkpoint3. The weighting disclosure holds.'),
    ('fDispositions', 'F-13'): (
        "CORRECTED SCOPE on 33. This row's subject is a PACKAGE artifact, and it changed: package10's "
        'evaluation-residual-author-assessment.json now declares subjectManifestSha256 '
        '1cf3db70d4b73b0c42f1393331e6a874ee26f7ddf67aa05c6ac15a5753069299 — the FROZEN33 manifest — with '
        '30 rows and sharedReviewDependencies declaring TCB-SCOPE-01 over exactly 13 dependent ids. The '
        'earlier binding is historical; saying the subject was untouched was wrong and is withdrawn.'),
    ('fDispositions', 'F-14'): (
        'CORRECTED SCOPE on 33. The subject is the rebuilt package10 assessment, so it is not untouched: '
        're-measured there, all 30 rows carry the identical self-assessment verdict '
        'proposed-account-supported-with-stated-limits with distinct rationales and limits. F-14 asked '
        'for no correction, this remains informational, I demand no forced uniform-verdict fix, and I '
        'grade no residual row from it.'),
    ('evaluationResidualDispositions', 'RES-EP13-05'): (
        'Cited owner bytes unchanged in 32->33. This review is again an instance of the correction the '
        'row records: my pins came from the frozen33 manifest and I verified all 12,899 rows plus full '
        'archive equality before use.'),
    ('scopedReviewOwnerDispositions', 'DR-204'): (
        'Owner files partially in the 32->33 delta (implementation-coverage.v1.json and '
        'implementation-planning-sources.v1.json), and the current normative input layer is now layer4. '
        'V1/coop invariant coverage MEASURED ON FROZEN33: 12,899 files and 736,764,309 bytes; 198 '
        'planned paths across 20 packages; 320 source-bound mappings; M0-M6; 54 planned recovery cases '
        'with 0 executed. The current architecture input layer is '
        'implementation-normative-inputs.v4.json with 29 pins, every one resolving against frozen33, '
        'differing from layer3 by exactly one repin (docs/v2/contracts/product-v1/native-evidence.md) '
        'with no additions and no removals. Layer3, layer2 and the original layer remain in the source '
        'as preserved history.'),
}
MAPS = ('fDispositions', 'evaluationResidualDispositions', 'arDispositions', 'fwDispositions',
        'inheritedResidualDispositions', 'scopedReviewOwnerDispositions')
FIELD = {'fDispositions': ('currentBasisOn33', 'priorBasisOn32')}
audit = {'rowsProcessed': 0, 'appendedPriorSuffixStripped': 0, 'bespokeCurrentTextRows': [],
         'priorFieldsLeftByteIdentical': 0, 'method': (
             'the source33 builder had set current = current-prefix + prior-field-verbatim on 96 of 107 '
             'rows, which is exactly how source32 reasoning entered current fields unqualified. Each '
             'such suffix is removed (the text remains verbatim in the prior field), 16 rows receive '
             'bespoke current text measured on 33, and every row gains an explicit history pointer. No '
             'blanket 32->33 substitution was performed and no prior field was edited.')}
for mp in MAPS:
    fld, pf = FIELD.get(mp, ('currentStatusOn33', 'priorStatusOn32'))
    for rid, row in R[mp].items():
        audit['rowsProcessed'] += 1
        cur = str(row.get(fld) or '').strip()
        prior = str(row.get(pf) or '').strip()
        if prior and cur.endswith(prior):
            cur = cur[:len(cur) - len(prior)].strip()
            audit['appendedPriorSuffixStripped'] += 1
        bespoke = CURRENT.get((mp, rid))
        if bespoke:
            cur = bespoke
            audit['bespokeCurrentTextRows'].append(mp + '/' + rid)
        row[fld] = cur + (HIST % pf)
        row['currentFieldStandingOn33'] = (
            'States current source33 truth only. Any source32 reasoning is retained verbatim in %s as '
            'history and is not offered as current evidence.' % pf)
        if prior:
            audit['priorFieldsLeftByteIdentical'] += 1
R['currentFieldAudit'] = audit

# FW-06 ordering selector, per R33-REC-03
R['fwDispositions']['FW-06']['currentStatusOn33'] = (
    'Determinism is strengthened on 33 and its ordering basis is now stated at the right level. The '
    'composition contract changed to remove a prescribed provider-unavailable fallback that '
    'contradicted execution-inputs, and the derived carrier is a published deterministic selection. '
    "The WHOLE-CELL cross-source order is SOURCE_ORDER: binding/enumerator at index 0, then "
    "inventories in this row's inventoryDigests canonical-set order, then candidate, then accounts "
    'per owed matrix pair in the AUTHORED relations array order — not lexical. The canonical-H '
    'partition order (returned partitions first, then named-but-not-returned Coverage, pair taken '
    'WHOLE from the first record carrying one) applies only INSIDE a single account. check-identity '
    'passes 1596/1596 and check-replay passes on frozen33.' + (HIST % 'priorStatusOn32'))

# DR-204 current owner array: layer4 is the current normative input layer
dr204 = R['scopedReviewOwnerDispositions']['DR-204']
man_paths = {f['path'] for f in json.load(open(MAN))['files']}
L4 = 'docs/v2/architecture/implementation-normative-inputs.v4.json'
assert L4 in man_paths and 'docs/v2/architecture/implementation-normative-inputs.v3.json' in man_paths
if L4 not in dr204['currentOwnerFiles']:
    dr204['currentOwnerFiles'] = sorted(set(dr204['currentOwnerFiles']) | {L4})
    dr204['ownerFilesChangedIn32to33'] = sorted(set(dr204['ownerFilesChangedIn32to33']) | {L4})
    dr204['ownerFilesUnchangedIn32to33'] = sorted(
        p for p in dr204['currentOwnerFiles'] if p not in dr204['ownerFilesChangedIn32to33'])
    dr204['ownerArrayCorrectionR33REC04'] = (
        'The current owner array named implementation-normative-inputs.v3.json only. Layer4 is the '
        'CURRENT normative input layer on 33 and is the one ADDED file in my 18-file delta, so it is '
        'added here; v3 is retained because the source preserves the earlier layers and this row is '
        'about the layer lineage. Both paths resolve in the frozen33 manifest.')
LEDGER.append({
    'id': 'R33-REC-04', 'disposition': 'ACCEPTED; ALL 107 CURRENT FIELDS REWRITTEN', 'rootIsCorrect': True,
    'evidence': ('my audit over all 107 rows found the mechanical cause: on 96 rows the current field '
                 'was literally the current prefix followed by the prior field verbatim, which '
                 'reproduced every example root named — F-03 "I executed it against frozen32", F-05 '
                 '"through the snapshot32 owner", F-13 "the author assessment binds the frozen32 '
                 'manifest", RES-EP13-05 "12,898 rows", DR-204 "frozen32: 12,898 files" with '
                 'implementation-normative-inputs.v3, and F-01 "all 277 members verify". Separately, '
                 'F-09 asserted no 32->33 subject change while five execution-inputs owners are in the '
                 'delta; auditing that same phrasing across the F rows, which carry no owner arrays and '
                 'so were not covered by the mechanical pass, found the same false claim on F-04 '
                 '(enumeration-contract.v1.md is in the delta) and an imprecise one on F-07, F-13 and '
                 'F-14, whose subjects are package artifacts that were rebuilt.'),
    'howFixed': ('the appended prior suffix is removed from those 96 fields and remains verbatim in the '
                 'prior field; 16 rows received bespoke current text measured on 33 from records I had '
                 'already taken rather than from a rerun; every current field now carries an explicit '
                 "HISTORY pointer naming the prior field; DR-204's current owner array now names "
                 'layer4. No prior field was modified and no blanket 32->33 substitution was made.'),
    'noRerunJustification': ('all current facts used here come from records already measured this '
                             'session or in the source33 pass — package10 305/305, 12,899 files, layer4 '
                             'pins, suite exit codes, the residual assessment binding. Unchanged suites '
                             'were not re-run merely to restate them.'),
    'affectedSelectors': ['$.fDispositions.*.currentBasisOn33',
                          '$.evaluationResidualDispositions.*.currentStatusOn33',
                          '$.arDispositions.*.currentStatusOn33',
                          '$.fwDispositions.*.currentStatusOn33',
                          '$.inheritedResidualDispositions.*.currentStatusOn33',
                          '$.scopedReviewOwnerDispositions.*.currentStatusOn33',
                          '$.*.*.currentFieldStandingOn33',
                          '$.scopedReviewOwnerDispositions.DR-204.currentOwnerFiles',
                          '$.scopedReviewOwnerDispositions.DR-204.ownerFilesChangedIn32to33',
                          '$.scopedReviewOwnerDispositions.DR-204.ownerFilesUnchangedIn32to33',
                          '$.currentFieldAudit']})

# ---------------------------------------------------------------- R33-REC-05
for a in R['advisories']:
    if a['id'] == 'A-9':
        a['statusOn33'] = (
            'Carried with its limits intact: the repair owners — repair_closed_world_selection.v1.py '
            'and workflows-and-surfaces.md — are NOT in my derived 32->33 delta, and the '
            'reference-level-only limitation is unchanged. Scope note: this advisory is about source '
            'surfaces, and no package evidence is claimed for it.')
    if a['id'] == 'A-10':
        a['selectors'] = ['claude-author-package-successor.v10 binding-controls/',
                          'author-helpers/evaluator.py',
                          'claude-author-package-successor.v8 binding-controls/ (historical selector '
                          'from the source31/32 record)']
        a['statusOn33'] = (
            'CORRECTED SCOPE. The A-10 LIMITS are unchanged on 33 — exists/none only, and/or/not '
            'unexercised, count-at-most and all-covered unimplemented in the partial helper, and the '
            'two-binding construction still incomplete with a single-explicit control. But the '
            "CONSTRUCTED EVIDENCE those limits describe DID change: package10's source-binding.v33.json "
            'records exportsChanged true with exportsChangedDetail "checkpoint3, binding-controls and '
            'semantic-controls1 only" and helperChanged ["author-helpers/evaluator.py"], so the '
            'binding-controls group and the helper this advisory points at are NEW source33 '
            'constructions, while the normalized and Rust groups are exact source30 bytes re-verified. '
            'My blanket "nothing in my derived 32->33 delta touches this advisory\'s subject" was too '
            'broad for A-10 — the source delta indeed does not, but the package rebuild does — and it '
            'is withdrawn. The limits still hold as measured on the new construction.')
        a['whyStillNotAShould'] = (
            'Still an evidence limit rather than a demonstrated owner defect, and nothing in this design '
            'layer depends on closing it. Re-measured on package10, not carried on the earlier package.')
LEDGER.append({
    'id': 'R33-REC-05', 'disposition': 'ACCEPTED AND QUALIFIED', 'rootIsCorrect': True,
    'evidence': ("package10's own source-binding.v33.json records exportsChanged true, "
                 'exportsChangedDetail "checkpoint3, binding-controls and semantic-controls1 only", '
                 'helperChanged ["author-helpers/evaluator.py"] and constructionSourceVersion '
                 '{typescriptDerivedGroups: 33, normalizedAndRustGroups: 30}. A-10 therefore had '
                 "changed construction evidence even though its limits did not change. A-9's source "
                 'owners are genuinely absent from the delta, so only the over-broad phrasing was '
                 'tightened there.'),
    'affectedSelectors': ['$.advisories[?(@.id=="A-10")].statusOn33',
                          '$.advisories[?(@.id=="A-10")].selectors',
                          '$.advisories[?(@.id=="A-10")].whyStillNotAShould',
                          '$.advisories[?(@.id=="A-9")].statusOn33',
                          '$.fDispositions.F-10.currentBasisOn33']})

# ---------------------------------------------------------------- ledger + receipts
R['correctionLedgerR33REC'] = {
    'standing': ('each item is assessed on measured evidence, not accepted on authority. All five are '
                 'substantiated; none is refused, and I found no counter-evidence against any of them.'),
    'items': LEDGER, 'itemsAccepted': len(LEDGER), 'itemsRefuted': 0}
R['evidenceReceipts']['newFullRunCandidateControl'] = {
    'standing': r03['standing'], 'scriptSha256': r03['scriptSha256'],
    'runId': r03['runId'], 'verdict': r03['verdict'],
    'structuralAdmission': r03['structuralAdmission'], 'semanticAdmission': r03['semanticAdmission'],
    'outputsWritten': r03.get('outputsWritten'),
    'frozen33DriftBeforeAfter': [r03['frozenDriftBefore'], r03['frozenDriftAfter']],
    'receiptPath': 'claude-independent33-reconciliation.v1/receipts/r03-fullruncontrol.json',
    'note': 'the ONLY new measured scope in this bounded pass; every other datum is preserved evidence'}
R['evidenceReceipts']['reconciliationReceipts'] = [
    'receipts/r00-verify.json — input digests, manifest, and the exact cited checker lines',
    'receipts/r01-fieldaudit.json — the 107-row current-field audit',
    'receipts/r02-currentfacts.json — package10 membership, residual binding, F-10 provenance',
    'receipts/r03-fullruncontrol.json — the root-authored full-Run control execution',
    'receipts/r05-consistency.json — final consistency check of this record']
R['evidenceReceipts']['failedOrImpreciseProbesPreserved'] = (
    R['evidenceReceipts'].get('failedOrImpreciseProbesPreserved', []) + [
        'p09 (source33 pass) combined an admission-only optional-candidate case with a DIFFERENT '
        'optional-unselected full-Run fixture. That reasoning is withdrawn under R33-REC-02; the '
        'original probe and its receipt are preserved unchanged in '
        'claude-independent-design.v33/receipts/p09-optional33.json.'])
R['reconciliationStanding'] = {
    'scope': 'bounded review-record and measured-scope correction on immutable source33',
    'newSourceDefectDemonstrated': False,
    'dispositionsChanged': 0, 'verdictChanged': False,
    'newMeasuredScopeAdded': ('one: the root-authored optional selected-U missing-candidate full-Run '
                              'control, independently executed'),
    'suitesRerun': 'none — no source or package suite was re-run merely because prose changed',
    'whatThisStillDoesNotDo': ('no source or package implementation, no product qualification, no blind '
                               'reconstruction, no application grade, no activation, no commit or push, '
                               'and no consumer/runtime/root blind record was read'),
    'rootAssentPending': ('root withheld design assent pending these record corrections. This successor '
                          'record supplies all five. Blind reconstruction and the final application '
                          'review remain separate and untouched.')}
out = os.path.join(BASE, 'review.json')
json.dump(R, open(out, 'w'), indent=1, default=str)
print('rows processed           :', audit['rowsProcessed'])
print('prior suffixes stripped  :', audit['appendedPriorSuffixStripped'])
print('bespoke current rows     :', len(audit['bespokeCurrentTextRows']))
print('prior fields untouched   :', audit['priorFieldsLeftByteIdentical'])
print('ledger items             :', [x['id'] for x in LEDGER])
print('delta files              :', len(DELTA))
print('bytes                    :', os.path.getsize(out))
print('sha256                   :', hashlib.sha256(open(out, 'rb').read()).hexdigest())
