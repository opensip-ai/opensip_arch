import json, pathlib
V4 = pathlib.Path('/private/tmp/opensip-design-corrections/bv6-corrections-author.v4')
delta = json.load(open(V4 / 'out/evidence/delta.json'))
prop = json.load(open(V4 / 'root-input/proposal.json'))
EDITS = {
 'docs/coop/design-corrections/workflows/check_workflows.v1.py': [
   'root patch 00: the prose-substring control workflow.native-preparation-lookup-is-not-replay-and-import-is-delivery-only REMOVED and replaced by a comment stating that lookup meanings are normative prose reviewed with the owning authorization/recovery contracts and that the key computations execute no delivery or preparation'],
 'docs/coop/design-corrections/workflows/schemas/imported-evidence.schema.json': [
   'root patch 01: deterministicProjection step 3 no longer says kind together with qualifiedName is the symbol granularity; it states that the projection reads logicalPath and qualifiedName and does not classify by the open kind vocabulary',
   'root patch 01: granularityIsReportedNotClassified gains the uniform limitation - neither imported format distinguishes subjectKey.language, kind or discriminator, distinct findings may project to one observation, and answerGranularity=symbol is not an exact match of the whole subject key'],
 'docs/coop/design-corrections/workflows/schemas/repair.schema.json': [
   'root patch 02: the ImportResult citation corrected from "workflow.mutation-receipt is the one receipt domain" to "the owning mutation receipt domain"'],
 'docs/coop/design-corrections/workflows/workflows_model.v1.py': [
   'root patch 03: project_targets_to_imported_subjects docstring gains the uniform path-and-name-only limitation; the widening comment generalised from history to either kind. Executable AST unchanged after stripping docstrings (verified independently).'],
 'docs/v2/contracts/product-v1/workflows-and-surfaces.md': [
   'root patch 04 section 1: the ExecutionId rationale corrected - the receipt key is operational and already carries RequestId, so ExecutionId is out because the key is scoped to one admitted invocation and step, with each attempt keeping its own; plus an explicit no-execution/no-retry-authority sentence',
   'root patch 04 section 1: "Among the generic mutation rows, four commands" corrected to "Across these step kinds, four ... Three use generic mutation steps", matching renamedRowsNote (three mutation-class plus the execution-class native-prepare)',
   'root patch 04 section 4: the HistoryPayloadV1 only-fields claim corrected to bounds fields, noting it also carries subjects and has no runtime window/population/observability fields',
   'root patch 04 section 4: the projection paragraph no longer classifies by kind and states the uniform path-and-name-only limitation and its bounded-observation consequence'],
}
for c in delta:
    c['edits'] = EDITS[c['path']] if c['changedThisTurn'] else ['unchanged this turn; carried from final v3']

h = {
 'artifact': 'bv6-corrections-author.v4 bounded final-source review',
 'role': 'Correction COAUTHOR review of a root-authored patch. Not an independent reviewer, not an accepting reviewer, and NOT an implementation pass - I made no source edit.',
 'standing': {'isProductQualification': False, 'isImplementationAuthorization': False,
   'isReadinessGrade': False, 'isIndependentAcceptance': False, 'isBlindReviewAcceptance': False,
   'note': 'Source under work/ was treated as READ-ONLY. Every file I wrote is under '
           '/tmp/opensip-design-corrections/bv6-corrections-author.v4/out. No source edit, no report '
           'or pin mutation, no product implementation, commit, push, publication or subagent.'},
 'custody': {'writeScope': '/tmp/opensip-design-corrections/bv6-corrections-author.v4/out',
   'inventoryVerified': {'declared': 6839, 'present': 6839, 'missing': 0, 'mismatched': 0, 'undeclared': 0,
     'against': 'root-input/proposed-source-inventory.json'},
   'aggregateChangedFiles': 17, 'changedThisTurn': 5, 'unchangedFromV3': 12,
   'hashChainVerified': ['all five proposal afterSha256 equal the supplied work bytes',
     'all five proposal beforeSha256 equal the prior-handoff finalV3Sha256 for those paths',
     'the other twelve declared files still equal their finalV3Sha256',
     'all five supplied diff files match their declared diffSha256'],
   'noHashesGuessed': 'Every value in changedSource.files was recomputed from the actual files; base '
                      'values come from root-input/prior-handoff.json and were checked against the '
                      'proposal before-hashes.'},
 'technicalAssent': {
   'value': False,
   'verdict': 'CHANGES_REQUIRED',
   'whatIAssentTo': 'All five proposed changes are correct, minimal and consistent with the '
                    'authorization, receipt-lookup, original-evidence-Run, closed-world and '
                    'bounded-observation laws. I would assent to each of them individually and I '
                    'have no disagreement with any of them.',
   'whyNotTheAggregate': 'Assent was requested to the EXACT aggregate 17-file hash set. One of those '
                         'files - check_workflows.v1.py, which this patch already modifies - still '
                         'carries the false "because relation is not an enum" rationale that root '
                         'itself declared false and that the corrected schema description and '
                         'section 6 prose in this same patch now contradict. Assenting to the '
                         'aggregate would assent to a statement I have verified to be wrong, so the '
                         'aggregate assent is withheld pending that one edit.',
   'doesNotAssertAnyOf': ['independence from this correction series', 'acceptance or readiness',
     'product qualification or implementation authorization',
     'that any control here is host enforcement, product emission, or full-Run closure evidence',
     'that the leftover-copy scan proves consistency - absence of a pattern match is not proof']},
}
h['changesRequired'] = [{
 'id': 'BV6-V4-CR-1', 'severity': 'SHOULD', 'parent': 'BV6-V3-PRECISION (root) / CX-BV6-08',
 'file': 'docs/coop/design-corrections/workflows/check_workflows.v1.py',
 'fileSha256': '98adcb93314e527f8182b67df68d56ab1c88faaf0e74c8ed4468feb80fa58875',
 'lines': '711-716',
 'finding': 'A leftover copy of the rationale root declared false. The comment reads "because the '
            'SCHEMA CANNOT DECIDE THEM. `relation` is a CanonicalIdentifier, not an enum, so no '
            'keyword in this document can look up which registry that relation belongs to". Two '
            'things are wrong. (1) It reproduces the false causal claim that a broader string type '
            'prevents conditional constraints - JSON Schema can branch on a property const/enum '
            'regardless of base type, which is exactly what root established. (2) "cannot decide" '
            'is itself too strong: the schema could enumerate the two imported relation names as '
            'consts; what it cannot do is dereference a registry, and the design DELIBERATELY leaves '
            'the authoritative lookup to admission to avoid duplicating a registry.',
 'whyItMatters': 'It now contradicts, in the same patch, the corrected wording of '
                 'repair.schema.json EvidenceRequirement.deficiency ("THIS SCHEMA DELIBERATELY '
                 'LEAVES THE AUTHORITATIVE REGISTRY LOOKUP TO ADMISSION ... not a limitation of '
                 'JSON Schema") and of workflows section 6. Leftover copies in a second document are '
                 'the defect class that has recurred through v1-v3, and this one is inside a file '
                 'the patch already touches.',
 'precisRemedy': 'Restate the comment as the deliberate choice, mirroring the corrected schema '
                 'description: the cross-plane rows are held separately because this schema '
                 'deliberately leaves the authoritative registry lookup to admission and cannot '
                 'dereference a registry - not because a broad string type prevents conditionals. No '
                 'control change is needed; the two cross-plane controls themselves are correct and '
                 'should stay.',
 'notBlockingTheFiveItems': True,
 'evidence': 'out/evidence/changes-required-leftover.json, out/evidence/leftover_scan.json'}]
h['itemDispositions'] = [
 {'id': 'PATCH-00-remove-prose-lookup-control', 'diff': 'delta/00-check_workflows.v1.py.diff',
  'disposition': 'AGREE - and it corrects a false claim of mine.',
  'assessment': 'My v3 handoff asserted "No control in the v3 delta proves a claim by matching '
                'prose". That was FALSE: I added workflow.native-preparation-lookup-is-not-replay-'
                'and-import-is-delivery-only, which matched three substrings of the published '
                'lookupMeaning. Root is right to remove it and right that the claim must not be '
                'repeated.',
  'whatIsLostAndRetained': 'The substring matching is gone; the STRUCTURAL guarantee survives - I '
                           'verified that workflow.every-step-kind-has-a-published-key-recipe-and-'
                           'lookup-meaning still requires a non-empty key AND lookupMeaning for all '
                           'four step kinds, so deleting a lookup law would still be caught. Only '
                           'the pretence of proving its MEANING is dropped, which is correct: the '
                           'reference executes no receipt delivery and no native preparation.',
  'measuredEffect': 'MEASURED, not inferred: check_workflows.v1.py yields 1788 rows on the final-v3 '
                    'bytes and 1787 on the proposed bytes, both with 0 failures - exactly the one '
                    'row root predicted. Static AST inspection confirms exactly one check call '
                    'removed and none added.'},
 {'id': 'PATCH-01-projection-kind-and-uniform-limitation', 'diff': 'delta/01-imported-evidence.schema.json.diff',
  'disposition': 'AGREE.',
  'assessment': 'The v3 step 3 said "`kind` together with `qualifiedName` is the SYMBOL granularity", '
                'which contradicted BOTH the implemented projection - it reads only logicalPath and '
                'qualifiedName - and the granularityIsReportedNotClassified paragraph I added in the '
                'same v3 pass. The patch removes the contradiction.',
  'newClaimVerifiedBehaviourally': 'The newly published uniform limitation is TRUE of the code, not '
                                   'merely asserted: two DISTINCT fingerprints whose subjectKeys '
                                   'agree on path and name but differ on language, kind AND '
                                   'discriminator both match one observation row, at '
                                   'answerGranularity symbol.',
  'safetyAssessment': 'This coarsening cannot manufacture support - each target genuinely matched a '
                      'row at the format granularity - and it is a DISCLOSED coarsening rather than '
                      'the ambiguity refusal, which remains many-rows-for-one-target and still '
                      'refuses (verified). The new text explicitly denies that it establishes '
                      'execution or non-execution beyond the captured granularity, which preserves '
                      'the bounded-observation law and the no-universal-negative invariant. The '
                      'unsafe-repair gate remains the evidence Run native ClosedWorldV2, untouched.'},
 {'id': 'PATCH-02-receipt-domain-citation', 'diff': 'delta/02-repair.schema.json.diff',
  'disposition': 'AGREE.',
  'assessment': 'Verified that workflows section 10 lists TWO receipt2 domains, '
                'workflow.mutation-receipt and workflow.verification-link, so "the one receipt '
                'domain" was false. This was a leftover copy inside a citation string I authored in '
                'v3 while correcting the main statement. Naming it the OWNING MUTATION receipt '
                'domain is exact and changes no key recipe, no lookup meaning and no authority.'},
 {'id': 'PATCH-03-model-docstring-and-comment', 'diff': 'delta/03-workflows_model.v1.py.diff',
  'disposition': 'AGREE.',
  'assessment': 'The docstring addition states the same uniform limitation as the schema, and the '
                'widening comment is generalised from history to either kind - correct, because v3 '
                'already made a path-only RUNTIME row a file-level answer too, so the old '
                'history-only comment had become stale.',
  'behaviouralClaimVerified': 'I independently confirmed root behavioural claim for this file: the '
                              'executable AST is IDENTICAL after stripping docstrings (leading '
                              'string-literal Expr only, so any other literal change would still '
                              'show). The full AST including docstrings differs, as expected.'},
 {'id': 'PATCH-04-prose', 'diff': 'delta/04-workflows-and-surfaces.md.diff',
  'disposition': 'AGREE, all four changes.',
  'executionIdRationale': 'Correct and now matches the schema boundTo I fixed in v3. The preimage '
                          'does contain RequestId, so calling the key operational is right and the '
                          'content-identity rationale was wrong. The added sentence that these '
                          'bindings grant no execution or retry authority is consistent with the '
                          'no-automatic-retry law and the security admission boundary, and adds '
                          'nothing.',
  'fourCommands': 'Correct: three mutation-class renames plus the execution-class native-prepare. '
                  'Verified against renamedRowsNote in repair.schema.json, which already said three '
                  'mutation-class plus a fourth in request class execution.',
  'historyPayload': 'Correct: HistoryPayloadV1 requires payloadDomain, vcsSystem, revisionRange, '
                    'collectionScope and subjects, so the two are its BOUNDS fields, not its only '
                    'fields. The load-bearing half - that it carries no runtime window, population '
                    'or observability - is retained and is what the per-kind projection depends on.',
  'projectionParagraph': 'Correct and now agrees with the code and the schema. I verified the '
                         'precise claim that granularityWidenedToFile is disclosed "in the '
                         'projection and successful outcome": it appears on a satisfied outcome and '
                         'is absent from a failing one, where the deficiency names the cause instead.'}]
h['priorDispositionsPreservedByReference'] = {
 'note': 'Not re-opened. This review is bounded to the supplied patch and its owning contexts; every '
         'earlier disposition stands with its original severity.',
 'v3RootItems': ['BV6-V3-RECEIPT (SHOULD)', 'BV6-V3-IMPORT-BINDING (MUST)', 'BV6-V3-IMPORT-CAUSE (MUST)',
   'BV6-V3-IMPORT-SEMANTICS (MUST)', 'BV6-V3-PRECISION (SHOULD)'],
 'v2RootItems': ['CX-BV6-01 (MUST)', 'CX-BV6-02 (SHOULD)', 'CX-BV6-03 (MUST)', 'CX-BV6-04 (SHOULD)',
   'CX-BV6-05 (SHOULD)', 'CX-BV6-06 (SHOULD)', 'CX-BV6-07 (SHOULD)', 'CX-BV6-08 (SHOULD)'],
 'originalBlindV6': ['CB6-MUST-1 (MUST)', 'CB6-MUST-2 (MUST)', 'CB6-SHOULD-1 (SHOULD)',
   'CB6-SHOULD-2 (SHOULD)', 'CB6-ADV-1', 'CB6-ADV-2', 'CB6-ADV-3'],
 'ownNew': ['CB6-NEW-1 retained', 'CB6-NEW-2 retained as narrowed in v2', 'CB6-NEW-3 WITHDRAWN',
   'CB6-NEW-4 retained'],
 'severitiesPreserved': True}
h['priorHandoffQualifications'] = [
 {'claim': 'v3 handoff: "No control in the v3 delta proves a claim by matching prose."',
  'status': 'FALSE and withdrawn. One such control existed and root removes it in patch 00.'},
 {'claim': 'v3 handoff: assent covering every point of the final note.',
  'status': 'OVERSTATED. My last actual Read of the note was 23:26 UTC; the 23:30 and 23:40 '
            'additions - which are the origin of these five items - were not covered by that assent '
            'and are dispositioned here for the first time.'},
 {'claim': 'v3 handoff comparative baselines: check-identity v2 = 1344, check-integration v2 = 378.',
  'status': 'WRONG, verified against the retained final-v2 reports: identity 1345 and integration '
            '388. 1344 was an intermediate failing v3 run and 378 was in fact the v1 value. The v2 '
            'handoff itself had recorded 1345 and 388 correctly. Historical comparative values are '
            'not current result evidence in any case.'},
 {'claim': 'v3 handoff FULL RETAINED-RUN scope.',
  'status': 'Already corrected in v3 and restated here: only the partition controls reach close_run; '
            'the imported path is exercised by pure helper calls.'}]
h['rootQualificationsAccepted'] = [
 'Root final eight projection/outcome rows omit observationWindow and observedPopulation in the '
 'outcome contexts, so those rows demonstrate selected helper MATCHING only, not admitted bounded '
 'observations. Accepted. My own verification probe supplies bounds where an outcome is computed, so '
 'its satisfied rows are bounded-observation rows - but they remain synthetic helper fixtures.',
 'All fixtures on both sides are synthetic helper fixtures, not closed-Run imports. No full-Run '
 'imported evidence admission is claimed by root or by me.',
 'Fingerprints in these fixtures are synthetically FORMATTED LABELS, not rehashed closure '
 'identities. No placeholder fingerprint is evidence of real closure admission.',
 'Structural presence, citation-list and key-set checks are presence only - they are not semantic '
 'proof and not host enforcement.',
 'run-suites is not the canonical six; final reports, custody and the canonical six after '
 'integration and pins remain root work.']
h['controlsRunByMe'] = {
 'interpreter': '/tmp/opensip-architecture-review-env/bin/python -I -B',
 'writtenTo': 'out/ only',
 'runs': [
  {'probe': 'out/probes/ast_equivalence.py',
   'result': 'workflows_model.v1.py executable AST identical after stripping docstrings; '
             'check_workflows.v1.py AST differs, as intended by the removed control. Both before and '
             'after hashes match the proposal.',
   'limit': 'AST equivalence over two .py files only; not a semantic or host proof and silent on the '
            'three non-.py files.'},
  {'probe': 'out/probes/checker_delta.py',
   'result': 'exactly one literal control id removed (the one root names), none added; 339 to 338 '
             'static call sites.',
   'limit': 'Static call sites are not runtime rows; several sites are inside loops.'},
  {'probe': 'check_workflows.v1.py executed on both byte sets in out/disposable',
   'result': 'MEASURED 1788 rows on final v3 and 1787 on the proposed bytes, 0 failures each.',
   'limit': 'One suite only, run directly rather than through the pinned launcher; not the canonical six.'},
  {'probe': 'out/probes/verify_published_claims.py',
   'result': 'all six newly published claims hold of the implemented code, including the uniform '
             'language/kind/discriminator limitation, the coarsening-versus-ambiguity distinction, '
             'and widening disclosed on a satisfied but not a failing outcome.',
   'limit': 'Pure helper calls over synthetic already-admitted inputs; synthetic fingerprint labels; '
            'no import, Run closure or host behaviour exercised.'},
  {'probe': 'out/probes/leftover_scan.py',
   'result': 'two pattern hits: one deliberate historical narration in repair.schema.json (correct to '
             'keep) and one genuine leftover in check_workflows.v1.py, raised as BV6-V4-CR-1.',
   'limit': 'Pattern matching over 203 non-review source files; absence of a match is not proof of '
            'consistency.'}]}
h['behaviouralScopeVerified'] = {
 'modelAstUnchangedAfterStrippingDocstrings': True,
 'checkerLosesExactlyOneControlAndGainsNone': True,
 'noEnumRequiredOrFieldChangeInTheTwoSchemas': 'The two schema diffs alter only description, citation '
   'and law prose strings; no $defs member, enum, required list or field was added, removed or '
   'retyped.',
 'noPayloadAuthorityPermissionRetryOrCapabilityAdded': True}
h['changedSource'] = {'aggregateVsFrozen16': 17, 'thisTurnVsFinalV3': 5, 'files': delta}
h['limitations'] = [
 'This is a bounded review of a supplied patch and its owning contexts, not a full source review.',
 'I made no source edit; the single remaining defect is returned as CHANGES_REQUIRED for root.',
 'Design reference evidence over synthetic inputs; nothing here is product qualification, host '
 'enforcement or closure admission.',
 'A fresh independent full review, a NEW blind consumer, an application review and the canonical six '
 'after integration and pins all remain owed.']
h['independentAcceptance'] = False
h['readinessChanged'] = False
h['implementationAuthorized'] = False
(V4 / 'out/handoff.json').write_text(json.dumps(h, indent=1, ensure_ascii=False) + '\n', encoding='utf-8')
print('written', len(json.dumps(h)))
