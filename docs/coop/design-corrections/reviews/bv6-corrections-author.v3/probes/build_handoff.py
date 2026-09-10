import json, pathlib
D = pathlib.Path('/private/tmp/opensip-design-corrections/bv6-corrections-author.v3')
delta = json.load(open(D / 'evidence/delta.json'))
E = {
 'docs/coop/design-corrections/foundation/identity-model.py': [
   'note follow-up: the reported-subject ordering rationale corrected - for admitted Unicode scalar strings code-point and UTF-8 byte order AGREE, so the explicit UTF-8 ordering excludes a UTF-16 code-unit comparison and canonical-JSON order, not a Python default'],
 'docs/coop/design-corrections/foundation/check-identity.py': [
   'note follow-up: the two leftover partition comments reconciled with the corrected law (an invalid partition was ACCEPTED and claims CAN be ambiguous, not that every consumer double-counts; a no-Coverage scope BYPASSES the per-Coverage producer guard but still reaches the ladder guard)',
   'note follow-up: the builtin-plus-substring ordering check REMOVED and replaced by partition_run_pair - a full Run with TWO added scopes overlapping on two competing subjects, asserting which subject the actual guard reports, plus a disjoint counterpart'],
 'docs/coop/design-corrections/native/native-evidence.schemas.v2.json': [
   'BV6-V3-PRECISION: whatTheConsumerCarries no longer says causes/disclosures "stay with the retained Coverage" - they are producer result arrays and are fields of no retained record; what is retained is the evidence the evaluation read'],
 'docs/coop/design-corrections/workflows/schemas/imported-evidence.schema.json': [
   'BV6-V3-IMPORT-BINDING: NEW targetSubjectProjection - the deterministic seven-step fingerprint -> payload-subject join through the evidence Run finding and the retained finding-fingerprint subjectKey, with ambiguity refusal, unmatched handling and the reference projection named',
   'BV6-V3-IMPORT-BINDING: inputBinding.targets rewritten to name fingerprints and the projection; inputBinding.windowDemand now names the ADMITTED RECIPE CLOSURE (recipe.closureId) and records that RecipeRef has no such wire field and none is claimed',
   'BV6-V3-IMPORT-SEMANTICS: inputBinding.allVersusAny marked a SELECTED CLARIFICATION with its provenance, withdrawing the "already means exactly this" overclaim; requiredVersusOptional now states the typed-boolean boundary and withdraws the unknown-defaults-required claim',
   'note follow-up: NEW granularityIsReportedNotClassified - subjectKey.kind has no closed vocabulary so the projection does not classify the target; it reports the granularity of the ANSWER, and any coarsening the payload format forces is stated'],
 'docs/coop/design-corrections/workflows/schemas/common.schema.json': [
   'note follow-up: ImportedRequirementDeficiency no longer says revisionRange/collectionScope are the ONLY HistoryPayloadV1 fields - they are its BOUNDS fields',
   'BV6-V3-PRECISION: D9Deficiency gains an explicit provenance sentence - its ENUM is unchanged and no member moved, while the definition bytes did change when the description was added'],
 'docs/coop/design-corrections/workflows/schemas/repair.schema.json': [
   'BV6-V3-RECEIPT: receiptOperationIsRequiredNotOptional corrected - MutationReceiptV1 requires operation AND idempotencyKey, and workflow.mutation-receipt is named as the owning MUTATION receipt domain rather than the only receipt2 domain',
   'BV6-V3-RECEIPT: NEW receiptIdempotencyKeyByStepKind - the exact key recipe, preimage, binding and lookup/delivery meaning for all four step kinds, with import DELIVERY-ONLY and native-preparation explicitly NOT replay',
   'note follow-up: the native-preparation and import boundTo rationales corrected - these are OPERATIONAL keys that already carry RequestId, so ExecutionId is excluded because the key is per admitted invocation/step, not because operational identities are excluded',
   'note follow-up: the dangling MutationOperation.x-opensip-vocabulary.map pointer to the removed byCommand key repaired, and receipt/field-domain pointers added; the duplicated dedicatedStepOperations and outer whatIsNotClaimed keys removed so they cannot drift',
   'BV6-V3-PRECISION: the EvidenceRequirement.deficiency description drops the false "because relation is not an enum" rationale and states the deliberate choice to leave registry lookup to admission; the causes/disclosures carrier claim corrected'],
 'docs/coop/design-corrections/workflows/workflows_model.v1.py': [
   'BV6-V3-IMPORT-BINDING: NEW project_targets_to_imported_subjects implementing the published join over retained records, refusing an ambiguous target, a target outside the evidence Run and a missing fingerprint preimage',
   'BV6-V3-IMPORT-SEMANTICS: imported_requirement_outcome now takes the projection and a REQUIRED typed boolean; the support test depends on completeness and the not-observable / not-covered condition only names the cause when that test fails, so lawful partial-acceptable cases survive; bounds apply in both modes',
   'BV6-V3-IMPORT-CAUSE: admit_evidence_requirement now decides the PER-KIND applicability for the imported plane, not merely the broad plane',
   'note follow-up: a path-only runtime row is a FILE-level answer to a keyed subject - answerGranularity and granularityWidenedToFile are reported for both kinds so it never silently passes as symbol-level'],
 'docs/coop/design-corrections/workflows/workflow-cases.v1.json': [
   'note follow-up: the closed-world case note now says no imported requirement can BY ITSELF make a destructive repair applicable, and points at its sibling case for the additional-condition direction'],
 'docs/coop/design-corrections/workflows/check_workflows.v1.py': [
   'BV6-V3 controls: the projection join and its three refusals, symbol-versus-file granularity both ways, the corrected partial semantics for both kinds, bounds applying in both modes, the typed required boundary including None/0/1/"yes", and the per-kind consumer over six kind/cause pairs',
   'BV6-V3-RECEIPT controls: both required receiptIds, MutationReceiptV1 requiring both fields, a computable key per non-generic step kind, the three keys differing, and the authority pointers resolving',
   'note follow-up: the prose-substring controls removed and replaced by structural ones (published key sets, RecipeRef having no window field, the three vocabularies genuinely differing, citation lists non-empty); the two same-named runtime-outcome invocations given distinct ids'],
 'docs/coop/design-corrections/check-integration.py': [
   'BV6-V3-IMPORT-BINDING cross-unit controls: a target fingerprint projected through the retained finding-fingerprint subjectKey, and the foundation descriptor carrying the subjectKey the workflows projection reads under an h-identity representation',
   'BV6-V3-IMPORT-CAUSE cross-unit controls: a runtime relation cannot carry a history outcome and the reverse',
   'updated for the projection and typed-required signatures'],
 'docs/v2/contracts/product-v1/native-evidence.md': [
   'BV6-V3-PRECISION: section 4.6 no longer says causes/disclosures stay with the retained Coverage; it names them as producer result arrays and names what is actually retained'],
 'docs/v2/contracts/product-v1/workflows-and-surfaces.md': [
   'BV6-V3-RECEIPT: section 1 corrects the receipt-domain claim and publishes the per-step-kind key table with its separate lookup meanings',
   'BV6-V3-IMPORT-BINDING: section 4 publishes the fingerprint-versus-path distinction and the projection, including granularity and ambiguity',
   'BV6-V3-IMPORT-SEMANTICS: section 4 states the five limits, marks the completeness reading as selected here, separates bounds from support and states the typed evidenceUse boolean',
   'BV6-V3-PRECISION: section 6 removes the false schema rationale and states the deliberate choice; the recipe-closure ownership of the observation demand is named'],
}
for c in delta:
    c['edits'] = E[c['path']] if c['changedThisTurn'] else ['unchanged this turn; carried from final v2']

h = {
 'artifact': 'bv6-corrections-author.v3 handoff',
 'role': 'Correction COAUTHOR working with Codex. Not an independent reviewer and not an accepting reviewer.',
 'supersedes': 'bv6-corrections-author.v2 (v1 and v2, their handoffs and all their evidence remain verbatim and unedited)',
 'standing': {'isProductQualification': False, 'isImplementationAuthorization': False,
   'isReadinessGrade': False, 'isIndependentAcceptance': False, 'isBlindReviewAcceptance': False,
   'isAgreementWithCodex': False,
   'note': 'Design-reference correction only. No product implementation, agents, subagents, commit, push or publication. EVERY v3 script, log, probe, report and temporary file is under /tmp/opensip-design-corrections/bv6-corrections-author.v3; nothing was written to bare /tmp this turn.'},
 'custody': {'writeScope': '/tmp/opensip-design-corrections/bv6-corrections-author.v3',
   'releasedWorkVerifiedAgainst': 'root-input/final-v2-source-inventory.json',
   'verifiedBeforeAnyEdit': {'declared': 6839, 'missing': 0, 'mismatched': 0, 'undeclared': 0},
   'verifiedAfterAllEdits': {'missing': 0, 'undeclared': 0, 'changedThisTurn': 12, 'aggregateVsFrozen16': 17},
   'frozenManifestSha256': 'ca5f36d421fb38d264f49fc6b2e1eeffee5bbe8182a7fe25bd50787244042ee9 (recomputed, matches)',
   'generatedReportsPinsReviewsTouched': 0,
   'codexPublicNote': 'root-input/final-v2-public-note.md read in full BEFORE edits, including the 22:54 and 22:57 UTC sections I had not seen at my v2 read. A further CODEX-PUBLIC-NOTE.md appeared in the v3 root and was read before this handoff; it added ten more precision items, all of which are dispositioned below.'},
 'technicalAssent': {'value': True,
   'scope': 'I substantively assent to the EXACT bytes at changedSource.files[].v3Sha256 as a correct, minimal and mutually consistent disposition of the five remaining root items and every point in the v3 CODEX-PUBLIC-NOTE.md, on top of the earlier corrections which are preserved.',
   'doesNotAssertAnyOf': ['independence from this correction pass', 'agreement by Codex or any independent reviewer',
     'readiness, acceptance or governance standing', 'product qualification or implementation authorization',
     'blind-review or application-review acceptance', 'correctness of any file outside changedSource',
     "that root's canonical six pass on the UNREFRESHED pins in the proposed tree",
     'that any control here is host enforcement, product emission, ledger or evaluator execution']},
}
h['rootPointDispositions'] = [
 {'id': 'BV6-V3-RECEIPT', 'parent': 'CX-BV6-04', 'severity': 'SHOULD', 'agreement': 'Full; both errors are mine.',
  'disposition': 'CORRECTED.',
  'whatWasWrong': ['MutationReceiptV1 requires idempotencyKey as well as operation, and my v2 law bound only the operation while saying the non-generic step kinds mint no H(workflow.mutation-intent) key - leaving a REQUIRED field underdetermined.',
    'My v2 text said exactly one receipt2 domain exists. Section 10 lists TWO: workflow.mutation-receipt and workflow.verification-link.'],
  'whatWasPublished': 'workflow.mutation-receipt named as the owning MUTATION receipt domain for those result branches, and receiptIdempotencyKeyByStepKind giving the exact recipe, preimage, binding and lookup meaning for all four step kinds.',
  'existingOwnerCited': 'No new H domain or record. MutationReplayScopeV1 is {schemaVersion, requestId, stepId, projectId, operation} and its operation domain ALREADY admits import and native-preparation - two of the 23 tokens - so the existing H("workflow.mutation-intent", scope) recipe is the owner. This is a further reason the 23-token domain must stay wider than the current generic emitters.',
  'semanticsHeldApart': ['mutation: delivery replay with no second effect',
    'repair-apply: its existing content-derived key',
    'import: DELIVERY ONLY within the same retained invocation; never a cross-request dedupe; custody, mandatory source correspondence and the staleness disposition unchanged and re-checked',
    'native-preparation: NOT replay - a fresh preparation is a new explicit authorized execution under its own AuthorizedExecutionV2 and grant set, with no automatic retry, and no completed receipt ever suppresses one'],
  'noteFollowUp': 'The boundTo rationale was corrected after the v3 note: these are OPERATIONAL keys that already carry RequestId, so ExecutionId is excluded because the scope is chosen per admitted invocation and step - not because operational identities are excluded, which would be false of such a preimage.',
  'referenceLimit': 'The reference model emits a receipt only for repair-apply. That is a stated qualification limit and is not a reason to omit a required field, which is exactly the distinction the correction makes.'},
 {'id': 'BV6-V3-IMPORT-BINDING', 'parent': 'CX-BV6-03', 'severity': 'MUST', 'agreement': 'Full.',
  'disposition': 'CORRECTED.',
  'whatWasWrong': 'RepairPlanDescriptor.targets are finding-key2 FINGERPRINTS; RuntimeSubject keys on {path, symbol?} and HistorySubject on {path}. My producer read the payload maps directly by the target string and my prose called the targets the payload subjects, silently equating a finding-key identity with a LogicalPath.',
  'theJoinPublished': ['target must be a finding of the evidence Run named by evidenceRunId - the binding repair preview already enforces',
    'the finding-key2 identity is the H identity of the retained finding-fingerprint descriptor, whose retention is preimage, so its bytes are retained and re-hashed at closure',
    'that descriptor carries subjectKey {language, kind, logicalPath, qualifiedName, discriminator}',
    'runtime matches on logicalPath and, where the row carries symbol, on qualifiedName; a symbol-keyed row for another symbol never matches',
    'history has no symbol field, so every history answer is file-level',
    'ambiguity REFUSES rather than choosing; an unmatched target is unsupported, never satisfied'],
  'granularity': 'After the v3 note, the classification was made explicit rather than assumed: subjectKey.kind has NO closed vocabulary here, so the projection does not classify the target by kind. It reports the granularity of the ANSWER - answerGranularity and granularityWidenedToFile - so a path-only runtime row is a FILE-level answer to a keyed subject and never silently passes as symbol-level, and any coarsening the payload format forces is stated on the outcome.',
  'windowDemand': 'RecipeRef has only contributionId, recipeId, recipeVersion and closureId. The demand is owned by the ADMITTED RECIPE CLOSURE named by recipe.closureId - content-addressed, admitted under current trust, revocation already invalidating apply - and projected by the host into a typed input. No nonexistent field is claimed.',
  'referenceIsJoinedToItsCaller': 'project_targets_to_imported_subjects implements the join over retained records and produces exactly what imported_requirement_outcome consumes, so the projection is exercised rather than only described.'},
 {'id': 'BV6-V3-IMPORT-CAUSE', 'parent': 'CX-BV6-03', 'severity': 'MUST', 'agreement': 'Full; root probe proves it.',
  'disposition': 'CORRECTED.',
  'whatWasWrong': 'admit_evidence_requirement admitted runtime-observation with history-range-insufficient and history-change with subject-not-observable, although the published perKindApplicability excludes both. The producer checked per-kind; the consumer checked only the broad imported plane.',
  'whatWasDone': 'The consumer now decides the PER-KIND law from the published perKindApplicability, refusing native.sufficiency-outcome-not-applicable-to-kind under CONFIG.INVALID with the typed presence law unchanged. Both lawful kind/cause pairs still admit, and the shared three outcomes still admit on both kinds.'},
 {'id': 'BV6-V3-IMPORT-SEMANTICS', 'parent': 'CX-BV6-03', 'severity': 'MUST', 'agreement': 'Full; three separate defects.',
  'disposition': 'CORRECTED.',
  'partialSemantics': 'The support test now depends on completeness, and the not-observable / not-covered condition only names the cause more precisely WHEN that test fails. Root partial fixtures with one supported and one unobservable or uncovered target now SATISFY, while complete still names the specific cause. Bounds - window and revision range - are a property of the observation rather than of the target count and therefore apply under both completeness values; that is stated.',
  'typedRequired': 'required must now be an actual bool; None, 0, 1 and "yes" all REFUSE with native.imported-required-declaration-not-boolean. The contradictory claim that unknown declarations are read as required is WITHDRAWN: there is no unknown state at this boundary, only a typed input from the owning evidenceUse declaration projection.',
  'provenanceCorrected': 'The completeness enum existed, but the imported ALL/ANY reading over plan targets is SELECTED HERE and is recorded as a selected clarification, not as a meaning the enum already published. The optional projection is related to the owning rule/recipe evidenceUse declaration and is explicitly NOT equated with policy predicate truth, whose own route keeps its own stated conditions.'},
 {'id': 'BV6-V3-PRECISION', 'parents': 'CX-BV6-07/CX-BV6-08', 'severity': 'SHOULD', 'agreement': 'Full; every item is a claim of mine.',
  'disposition': 'CORRECTED.',
  'items': ['the "because relation is not an enum" rationale is FALSE and is removed from both the schema description and section 6; the accurate statement is that this schema deliberately leaves the authoritative registry lookup to admission and cannot fetch registry rows, and that duplicating a registry as conditionals would create drift',
    'D9Deficiency: its ENUM is preserved and no member moved; its DEFINITION BYTES changed when the description was added. Stated in the definition itself and in this handoff.',
    'the v2 FULL RETAINED-RUN claim was FALSE for the repair_preview cases - those are synthetic workflow helper calls. Only the partition controls reach close_run, and even that is distinct from ledger or evaluator execution. Corrected in referenceControls below.',
    'the four renames are 3 generic mutation rows plus 1 dedicated native-preparation, not 4 generic rows',
    'v2 wrote /tmp/hb.log, /tmp/hd.py and /tmp/delta-table.md outside its output directory, so the all-writes-inside claim was repeated in error. In v3 every file is under the v3 root and this is verified below.',
    'the v2 public note was read once at 22:51 UTC; the 22:54 and 22:57 additions arrived during or after that handoff and were NOT substantively covered by it. No claim is made that every note point was agreed at v2.']}]
h['v3NoteFollowUps'] = [
 {'item': 'identity-model UTF-16/code-point ordering rationale', 'disposition': 'CORRECTED - code-point and UTF-8 byte order agree for admitted scalars; the explicit UTF-8 ordering excludes a UTF-16 code-unit comparison and canonical-JSON order. The chosen ordering is preserved.'},
 {'item': 'check-identity leftover partition comments', 'disposition': 'CORRECTED - both reconciled with the law.'},
 {'item': 'the builtin-plus-substring ordering control', 'disposition': 'REMOVED and REPLACED by a full Run with TWO added scopes overlapping on two competing subjects, which asserts which subject the actual guard reports, plus a disjoint counterpart. My first replacement attempt was wrong - the overlapping set had a single member - and is retained in evidence.'},
 {'item': 'workflow-cases closed-world note', 'disposition': 'CORRECTED - BY ITSELF added, with a pointer to the sibling case that shows the additional-condition direction.'},
 {'item': 'HistoryPayloadV1 "only fields"', 'disposition': 'CORRECTED - they are its BOUNDS fields; it has others, notably subjects.'},
 {'item': 'causes/disclosures "stay with the retained Coverage"', 'disposition': 'CORRECTED in all four places - they are producer RESULT ARRAYS and fields of no retained record; some could not be, since the confidence floor lives in RequirementV2 and required-relation-missing has no Coverage entry. What is retained is the evidence the evaluation read, so the projection drops nothing retained.'},
 {'item': 'remaining prose-substring controls in the workflow checker', 'disposition': 'REMOVED and replaced by structural checks - published key sets, RecipeRef genuinely lacking a window field, the three vocabularies genuinely differing by pattern and required members, and non-empty citation lists. No control now proves a join by matching prose.'},
 {'item': 'duplicate control id for the two runtime-outcome invocations', 'disposition': 'CORRECTED - distinct ids; counts below are reported as check ROWS, not distinct named properties.'},
 {'item': 'dangling MutationOperation map pointer to the removed byCommand key', 'disposition': 'CORRECTED, plus receipt and field-domain pointers added, a scan for other dangling selectors into that map (none remained), a new control that every such pointer resolves, and removal of the two duplicated keys that could drift.'},
 {'item': 'native-preparation boundTo rationale', 'disposition': 'CORRECTED - it is an operational key already carrying RequestId; ExecutionId is excluded because the scope is per admitted invocation and step, with attempt identity kept separate.'},
 {'item': 'runtime matching and intentional coarsening', 'disposition': 'CORRECTED in code and law - a path-only row is a file-level answer, reported as such for both kinds, and the projection does not invent a subjectKey.kind vocabulary.'}]
h['earlierFindingsPreserved'] = {
 'note': 'Not re-opened this turn; carried unchanged unless a v3 item touched them.',
 'rootPointsV2': ['CX-BV6-01 partition law and controls - preserved; only the two leftover comments and the ordering control were corrected',
   'CX-BV6-02 typed presence law and CONFIG.INVALID routing - preserved and extended by the per-kind check',
   'CX-BV6-03 plane split and disjoint vocabularies - preserved; binding, cause and semantics corrected',
   'CX-BV6-04 step-kind operation law - preserved; the key law and the dangling pointer added',
   'CX-BV6-05, CX-BV6-06 - unchanged', 'CX-BV6-07, CX-BV6-08 - the remaining precision items corrected here'],
 'originalBlind': ['CB6-MUST-1', 'CB6-MUST-2', 'CB6-SHOULD-1', 'CB6-SHOULD-2', 'CB6-ADV-1', 'CB6-ADV-2', 'CB6-ADV-3'],
 'ownNew': ['CB6-NEW-1 retained', 'CB6-NEW-2 retained as corrected in v2 - only config-write is unbound',
   'CB6-NEW-3 remains WITHDRAWN', 'CB6-NEW-4 retained - editing a registered schema document moves fixture Run identities'],
 'severitiesPreserved': True,
 'invariantsPreserved': ['both imported relations still supported', 'symbol versus file granularity preserved and now reported',
   'native safety and recipe authority unchanged - the unsafe-repair gate remains the evidence Run ClosedWorldV2',
   'all 23 generic operation tokens retained and repair-apply still excluded from both generic fields',
   'no D9 widening; the D9 enum is unchanged', 'partial cases preserved and now actually admitted']}
h['referenceControls'] = {
 'interpreter': '/tmp/opensip-architecture-review-env/bin/python -I -B',
 'counts': {'check-foundation.py': {'v2': 231, 'v3': 231}, 'check-identity.py': {'v2': 1344, 'v3': 1346},
   'check-security-lifecycle.v1.py': {'v2': 456, 'v3': 456}, 'check_native_evidence.v2.py': {'v2': 355, 'v3': 355, 'unit': 'cases'},
   'check_workflows.v1.py': {'v2': 1761, 'v3': 1788}, 'check-integration.py': {'v2': 378, 'v3': 392}},
 'countScope': 'These are check ROWS, not distinct named properties and not exhaustive coverage. Several ids are parameterised over a vocabulary, so one property can contribute many rows.',
 'whatTheseControlsAre': 'SCHEMA-level jsonschema validation; HELPER-level direct calls into the reference models over synthetic already-admitted inputs; and FULL RETAINED-RUN close_run closure for the partition controls ONLY. The repair_preview cases are SYNTHETIC WORKFLOW HELPER calls and are NOT close_run cases - the v2 handoff said otherwise and that claim is withdrawn. Even close_run is distinct from ledger, evaluator or provider execution. HOST ENFORCEMENT: NONE.',
 'noProseSubstringOrSelfMirroring': 'No control in the v3 delta proves a claim by matching prose, and none asserts the model equals a second copy of itself. Parity controls compare a mirror against its OWNING authority document; behaviour controls call the changed admission.'}
h['executedCommands'] = {
 'where': '/tmp/opensip-design-corrections/bv6-corrections-author.v3/disposable/checker-run.v1, a separately inventoried disposable repinned copy. work/ was never repinned; its pins are stale by design.',
 'notTheCanonicalSix': 'run-suites.sh sets pipefail and is NOT the canonical final six. Root runs those after final source, records and pins. Verdicts are read from each suite report JSON.',
 'disposableCopyDeltas': ['excludes docs/coop/design-corrections/reviews/ except the three author-feedback files the pin manifests name',
   'repin.py refreshed 62 pin rows; those pins exist only in the disposable copy',
   'the suites rewrite their own reports there; a failing workflows report was preserved to evidence/ before being overwritten'],
 'suitesRunOnceAfterCoherentFinalSource': [
   {'suite': 'check-foundation.py', 'result': 'PASS 231/231'},
   {'suite': 'check-identity.py', 'result': '1346 passed, 0 failed'},
   {'suite': 'check-security-lifecycle.v1.py', 'result': '456/456, 10 sweeps true'},
   {'suite': 'check_native_evidence.v2.py', 'result': 'PASS 355/355 cases'},
   {'suite': 'run-reference-checks.py', 'result': 'pins valid, 1788/1788'},
   {'suite': 'check-integration.py', 'result': '392 passed, failed []'}],
 'rootProbesReRunAgainstV3': [
   {'probe': 'probe-bv6-scope-overlap-v3.py', 'result': 'unchanged and correct: overlap refuses, disjoint and different-relation admit', 'evidence': 'evidence/final-v3-probe-bv6-scope-overlap-v3.json'},
   {'probe': 'probe-bv6-scope-no-coverage-v1.py', 'result': 'unchanged and correct: overlapping no-Coverage refuses, disjoint admits', 'evidence': 'evidence/final-v3-probe-bv6-scope-no-coverage-v1.json'},
   {'probe': 'probe-bv6-requirement-draft.py', 'result': 'helper and owning schema agree on all five shapes', 'evidence': 'evidence/final-v3-probe-bv6-requirement-draft.json'},
   {'probe': 'probe-bv6-final-v2-imported.py', 'result': 'CANNOT RUN UNMODIFIED, and that is the correction landing: it passes plain strings as targets and omits `required`, which are exactly the two defects it exposed. Its unmodified failure is retained; probes/probe_v3_imported.py asks all of its questions against the corrected structure and matches on all 20 cases, including its four cross-kind consumer cases, its None/0 required cases and both partial fixtures.',
    'evidence': 'evidence/root-imported-probe-unmodified-fails-on-changed-signatures.txt, evidence/probe_v3_imported.result.json'}],
 'preservedFailures': [
   {'what': 'my first replacement for the ordering control', 'cause': 'the overlapping SET had a single member (foo), so the control asserted the wrong reported subject. Replaced by a two-scope overlap on two competing subjects.', 'retained': 'evidence/ and the probes directory'},
   {'what': 'workflows report with the stale symbolGranularity field', 'cause': 'my controls still read a projection field the granularity correction renamed.', 'retained': 'evidence/workflows-report.stale-symbolGranularity-failure.json'}]}
h['changedSource'] = {'aggregateVsFrozen16': 17, 'thisTurnVsFinalV2': 12, 'files': delta}
h['v2ScopeClaimsCorrectedHere'] = [
 'v2 said all writes were under its output directory; /tmp/hb.log, /tmp/hd.py and /tmp/delta-table.md were not.',
 'v2 claimed FULL RETAINED-RUN evidence for the repair_preview cases; they are synthetic workflow helper calls.',
 'v2 said D9Deficiency definition bytes were unchanged; only its enum is.',
 'v2 said exactly one receipt2 domain exists; there are two.',
 'v2 said the completeness enum already meant the imported ALL/ANY reading; that reading is selected now.',
 'v2 said the schema cannot decide the plane because relation is not an enum; that rationale is false.',
 'v2 described the four renames as four generic rows; they are three generic plus one dedicated.',
 'v2 did not cover the 22:54 and 22:57 public-note additions, which arrived during or after that handoff.']
h['limitations'] = {
 'evidenceClass': 'Design reference evidence over synthetic trusted inputs. No compiler, provider, renderer, ledger, evaluator or product emitter was executed.',
 'referenceModelVersusDesignLaw': 'The model emits a receipt only for repair-apply and does not exercise a production import or native-preparation emitter. Stated as a qualification limit, distinct from the design law, which is normative and complete for both required fields.',
 'importedProjectionIsPure': 'project_targets_to_imported_subjects and imported_requirement_outcome are pure reads over already-admitted inputs with stated preconditions. They admit no payload, no observation scope and no polarity, and they validate no opaque Run; an authenticated importer and the retained Run closure own those.',
 'noFullRunForImportedRepair': 'The imported requirement path is exercised through repair_preview and direct producer calls, not through a close_run closure. Only the partition controls reach close_run.',
 'stalePinsInProposedCopy': 'Expected; root refreshes pins after final source and records.',
 'successorStillOwed': 'Final full exact-byte root review, a fresh independent Claude review, a NEW blind consumer and an application review all remain owed. This is coauthor assent to exact bytes only.'}
h['independence'] = False
h['blindAcceptance'] = False
h['readinessChanged'] = False
h['productQualification'] = False
h['implementationAuthorized'] = False
h['codexAgreement'] = 'NOT CLAIMED. Root does not assent; this handoff exists so the final bytes can be checked.'
(D / 'handoff.json').write_text(json.dumps(h, indent=1, ensure_ascii=False) + '\n', encoding='utf-8')
print('written', len(json.dumps(h)))
