# Executed by build_review40.py in its own globals (exec). AR, FW, DR and scoped-owner rows, the single TCB-SCOPE-01 object,
# retained obligations, authority and limitations. Every row is individually reasoned; flags are always false.

BASIS_RULE = ('inherited-unchanged-39: the governing owner bytes are byte-identical 39->40, and the conclusion rests on that identity plus this origin\'s source39 assessment; '
              'any re-executed suite named in the row is corroboration only. new-40: the conclusion rests on a source40 read, diff, probe or measurement newly performed '
              'under this charter. No row is carried forward without its own text, and no grade is assigned.')

AR_TEXT = {
    'AR-01': (N, 'NO-NEW-ISSUE', 'Admission section 1 is byte-identical 39->40. The ported query-carrier probe re-confirms both runId delivery directions of the StepTermination law on source40.'),
    'AR-02': (I, 'NO-NEW-ISSUE', 'Admission sections 2-4 and the qualification gates are byte-identical 39->40 (%d gates, qualified=true %d); all gates stay unperformed.' % (len(GATES), gates_true)),
    'AR-03': (N, 'NO-NEW-ISSUE', 'The security contract is byte-identical 39->40. The ported custody probe passes, and U-4b.2 nested project boundaries exclude nested workspace markers (P40-NATIVE C5).'),
    'AR-04': (I, 'NO-NEW-ISSUE', 'The security contract is byte-identical 39->40 and no delta touches trust time. No probe.'),
    'AR-05': (I, 'NO-NEW-ISSUE', 'The security contract is byte-identical 39->40 and no delta touches root chain or revocation. No probe.'),
    'AR-06': (N, 'NO-NEW-ISSUE', 'The platform admission text and carrier DDL are unchanged 39->40, and the security group passes on this review\'s source40 copy.'),
    'AR-07': (N, 'NO-NEW-ISSUE', 'native-evidence.md changed and was read complete. U-1 effective allowJs, U-4b.2 nested folding and the unit-kind projection were probed against source39 baselines and with full-Run closure; the native group passes 388/388 (source39: 380).'),
    'AR-08': (N, 'NO-NEW-ISSUE', 'workflows-and-surfaces.md changed and was read complete, but the invocation and repair text is outside the 39->40 diff. The ported repair:2 probe passes on source40; argvDigest is unchanged and not independently probed.'),
    'AR-09': (N, 'CHANGES-REQUIRED (S40-01)', 'identity-and-evidence.md is byte-identical 39->40 and incorporates the execution-inputs contract (identity section 4). S40-01: which returned views a cell row attributes has no published recipe, and two conforming encodings of the same stage returns admit with different ExecutionInputsV1 digests. The foundation group passes, and the commit-inventory recipe was recomputed independently.'),
    'AR-10': (N, 'NO-NEW-ISSUE', 'Baseline and comparison text changed (first-applicable indeterminateReason order, workflows-and-surfaces.md:403; the conservative evidence axis) and was read complete. The ported comparison-knowledge probe and child pass, and no contradiction was demonstrated.'),
    'AR-11': (N, 'NO-NEW-ISSUE', 'Comparison and import: the single H import identity (workflows-and-surfaces.md:475) and exact-snapshot correspondence (:508) were read, and the policy-test imported row now joins subject and universe (S39-02). The execution-inputs child passes. No independent import probe.'),
    'AR-12': (N, 'NO-NEW-ISSUE', 'Native section 4 atom semantics are unchanged in substance, and the atoms child passes (%s units). S39-01 is closed: the policy-test verifier now keeps known findings under missing required evidence, as fail dominance requires.' % children['atoms'].get('passed')),
    'AR-13': (N, 'NO-NEW-ISSUE', 'Native sections 1 and 2 changed (U-1 effective allowJs, the mode table) and were probed. The U-9 fallback and its security S3 counterpart were re-run by the ported custody probe. OBS40-04 and OBS40-05 are stated trusted-host scope, not defects.'),
    'AR-14': (N, 'NO-NEW-ISSUE', 'ADV38-02 and ADV38-03 remain closed: carrier-dispatch and commit-recovery bytes are unchanged 39->40, and the ported read-only carrier probe passes on source40.'),
    'AR-15': (I, 'NO-NEW-ISSUE', 'The contract index README is byte-identical 39->40.'),
    'AR-16': (N, 'NO-NEW-ISSUE', 'S39-01 and S39-02 are closed at source level, and the run-termination clarifications are confirmed against the unchanged model. ADV38-01 remains closed and the D9 successor stays carried. The only addition in this row is observation OBS40-03 (policy show).'),
}
AR_ROWS = []
for i in range(1, 17):
    rid = 'AR-%02d' % i
    basis, disp, text = AR_TEXT[rid]
    p = V39ROWS[rid]
    c = p['contract']
    AR_ROWS.append(base_row(rid, basis, disp, text, contract=c, selector=p['selector'], statusRecorded=p['statusRecorded'],
                            contractSha256=sha(S40 + '/' + c), contractUnchanged39to40=same39(c)))
    if basis == I and not same39(c):
        GAPS.append('inherited basis claimed for a changed contract: ' + rid)

SM_INV = U['current-source-map.proposed.md'] and U['repository-file-inventory.v1.json']
FW_TEXT = {
    'FW-01': 'discovery.rs must implement U-4b.2 nested Cargo folding (the deepest surviving workspace, decided shallowest first), the closed unit-kind projection, the U-1 effective allowJs marker observation (including a checkJs-derived value, OBS40-05) and pruned-tree custody; all were confirmed at owner level and with full Runs.',
    'FW-02': 'review.rs carries review-brief through query carriers; the ported query probe re-confirms the lawful control, the truncated variant and the another-run refusal.',
    'FW-03': 'analysis.rs hands the host observation to run-termination section 7 (ported TERM7 passes) and captures stage returns into ExecutionInputsV1. S40-01 routes here too: the capture cannot be implemented deterministically from published text until the attribution law is published.',
    'FW-04': 'imports.rs implements the typed-null targetUniverse account, the single H import identity and exact-snapshot correspondence; the policy-test imported-row subject-and-universe join is confirmed (P40-POLICY). Read and child evidence only.',
    'FW-05': 'comparison.rs implements presence knowledge (ported probe passes) and the first-applicable indeterminateReason order, which was read; no independent probe of the order.',
    'FW-06': 'finalization.rs projects the delivery laws (ported query probe) and the run-termination section 6 and 7.3 commit-inventory recipe, recomputed independently over a closed Run (P40-RUNTERM-ADV).',
    'FW-07': 'invocation.rs computes argvDigest over C(argv); the text is unchanged 39->40, read-confirmed and covered by an executed author control, not independently probed.',
    'FW-08': 'outcomes.rs implements the section 7 detail allowlist (ported TERM7) and the closed candidate comparison: errorCode, faultCause and signal reach NOT_DERIVED, and an unknown member refuses first (P40-RUNTERM-ADV).',
    'FW-09': 'review.rs candidates/inspect carriers are re-confirmed by the ported query probe; the suppressedCount observation (OBS40-09) still means the host derives the count from the producing step.',
    'FW-10': 'repair.rs is the repair:2 constructor owner; the ported probe re-confirms refusal before the descriptor and exact-class unavailability.',
    'FW-11': 'comparison.rs baseline.show carriers and pivot closure availability are re-confirmed by the ported query controls.',
    'FW-12': 'review.rs review.produce-brief stays a host-only query operation (ported query probe).',
    'FW-13': 'configuration.rs routes policy-test admission: an unregistered fact universe token is CONFIG.INVALID on source40 (P40-POLICY); the recommend config2 joins are re-confirmed by the ported probe.',
    'FW-14': 'discovery.rs recommend discovery units now follow U-1 effective allowJs and U-4b.2 folding (P40-NATIVE); NATIVE_DEFAULT_SELECTION_WITHOUT_UNIT is re-confirmed by the ported probes.',
    'FW-15': 'policy.rs owns policy show/test: S39-01 and S39-02 are closed at source level (P40-POLICY); policy show accepting an unregistered token is inspection, not analysis admission (OBS40-03).',
}
FW_ROWS = []
for i in range(1, 16):
    rid = 'FW-%02d' % i
    p = V39ROWS[rid]
    FW_ROWS.append(base_row(rid, N, 'OWNER-ROUTING-ASSESSED-NOT-EXECUTED',
                            FW_TEXT[rid] + ' Owner module and milestone match the current-source-map and repository-file-inventory rows (both byte-identical 39->40: %s); implementation not executed.' % SM_INV,
                            owners=p['owners'], milestone=p['milestone'], verificationStanding=p['verificationStanding']))

IR_UNCH = U['inherited-residuals.proposed.md']
DR_TEXT = {
    'DR-001': (I, 'current-source-map and the residual ledgers are byte-identical 39->40, and the reading path was refreshed on source40.'),
    'DR-002': (N, 'The identity/evidence/proof chain holds: the commit-inventory recipe was recomputed over a closed Run. S40-01 is an identity-determinism gap in ExecutionInputsV1 attribution, routed to the execution-inputs owner, and it keeps this obligation open.'),
    'DR-003': (N, 'Read-only carrier routes are re-confirmed by the ported probe. The 54 recovery cases remain unexecuted, and real platform demonstration remains a release requirement.'),
    'DR-004': (N, 'The native contract changed (U-1 effective allowJs, U-4b.2 nested folding and unit kinds, ADV39-01 account) and was read complete. The native group passes 388/388 and unit kinds are enforced at full-Run closure.'),
    'DR-005': (N, 'Executable custody groups pass on source40, the ported custody probe passes, and nested project boundaries exclude nested workspace markers. Native product carrier qualification is still required.'),
    'DR-006': (N, 'The descriptor graph is unchanged: the ported query probe re-checks graph-query-3 bytes, and the full-replay child passes.'),
    'DR-007': (N, 'The D9 published successor artifact remains a carried implementation-unit obligation, not a new blocker. The run-termination clarifications add no D9 code or public detail (the registry is unchanged at 315 codes).'),
    'DR-008': (I, 'The applied retention posture is unchanged.'),
    'DR-009': (N, 'The run-termination section 3, 6 and 7.3 clarifications keep the host observation outside the sealed Run; the commit inventory is a separate record over a closed Run, preserving lifetime neutrality.'),
    'DR-010': (N, 'Bounded first-party composition is unchanged (prototype-report-inventory byte-identical: %s). The policy-test verifier now agrees with bounded composition on the six discriminating cases; it remains reference evidence, not composition authority.' % U['prototype-report-inventory.md']),
    'DR-011': (I, 'Individual dispositions exist; the blind implementer litmus follows final integration and is not closed here.'),
    'DR-011-R01': (N, 'The fact-plane successor schemas are unchanged 39->40 (identity-schemas byte-identical: %s); policy test now consumes their policyUniverseMap as the closed token set.' % U['identity-schemas.v3.json']),
    'DR-011-R02': (N, 'Imperative plugins stay outside D-371. PolicyTestSuiteV2 admission is closed, and rule and fact universe tokens now refuse typed (P40-POLICY).'),
    'DR-011-R03': (N, 'The plan2/exec-plan2 membership law gains the unit-kind projection check (enumeration_model diff read). The enumeration child passes and full Runs refuse reminted kinds.'),
    'DR-011-R04': (I, 'The carrierFormat axis mapping is unchanged (carrier-dispatch byte-identical: %s).' % U.get('carrier-dispatch.v3.json')),
    'DR-011-R05': (I, 'The Rust protocol major 3 is unchanged, and the native group passes.'),
    'DR-011-R06': (N, 'identity-model is byte-identical 39->40 (%s); the analysis-seal and query-projection children re-exercise the typed close_run outcomes on source40.' % U['identity-model.v3.py']),
    'DR-011-R07': (I, 'Query retained availability routes are unchanged, and the query-projection child passes (%s checks).' % children['query-projection'].get('count')),
    'DR-011-R08': (N, 'The D9 published successor artifact remains carried (DR-007); nothing in source40 claims to discharge LIVE D9 (native-evidence.md:3018).'),
    'DR-011-R09': (N, 'Semantic IDs still exclude attempt identity, and policytest2 identity is a function of the suite alone (P40-POLICY identity preimages). S40-01 is a capture-encoding ambiguity, not attempt identity leaking into semantics.'),
    'DR-011-R10': (I, 'OPEN: this nonblind review cannot close the fresh blind implementer litmus.'),
    'DR-011-R11': (N, 'ADV38-02 and ADV38-03 remain closed. Real platform durability is unmeasured and the 54 cases are not executed.'),
    'DR-011-R12': (N, 'Depends on TCB-SCOPE-01, assessed once on source40.'),
    'DR-011-R13': (N, 'Source40 changes discovery outcomes without relabelling record majors (the jsconfig allowJs:false membershipDigest differs 39->40). The composition profile states that a changed value changes ancestor identity normally and an unchanged record shape needs no relabel; PolicyTestSuiteV2 and repair:2 still refuse major 1.'),
    'DR-011-R14': (I, 'CFG-6/TM is unchanged.'),
    'DR-011-R15': (N, 'The trusted request context stays host-only: the ported query probe re-confirms that HostQueryParams operations are not public.'),
    'DR-011-R16': (I, 'No executable report-hook admission: prototype-report-inventory (%s) and admission section 5 (%s) are byte-identical 39->40.' % (U['prototype-report-inventory.md'], U['admission-and-qualification.md'])),
}
DR_ROWS = []
for rid in ['DR-%03d' % i for i in range(1, 12)] + ['DR-011-R%02d' % i for i in range(1, 17)]:
    basis, text = DR_TEXT[rid]
    DR_ROWS.append(base_row(rid, basis, 'CONDITION-1-OBLIGATION-RETAINED-ASSESSED',
                            text + ' The successor routing in inherited-residuals.proposed.md (byte-identical 39->40: %s) is consistent with source40; original custody and standing preserved.' % IR_UNCH))

REG_UNCH = U['08-decision-and-readiness-register.md']
SCOPED_TEXT = {
    'DR-201': 'The semantic-correctness owner row (Run versus command finalization, post-commit output failure) is byte-identical. The source40 run-termination clarifications and the S40-01 capture-determinism gap fall in its area.',
    'DR-202': 'The delivery/operations owner row (recovery, repair, loader TCB) is byte-identical. Read-only carriers and repair:2 are re-confirmed by the ported probes.',
    'DR-203': 'The prototype-lessons owner row (PARTIAL-SCOPED) is byte-identical. No delta file is the prototype reference, and prototype-report-inventory is byte-identical (%s).' % U['prototype-report-inventory.md'],
    'DR-204': 'The V1/coop invariant owner row (exact selector/digest posture) is byte-identical. This review validated selectors and digests independently; ADV40-01 is an editorial digest-posture note in its spirit, and S40-01 is an identity-determinism gap.',
    'DR-205': 'The small-core/components owner row (core/TCB boundaries) is byte-identical. TCB-SCOPE-01 remains coherent on source40.',
}
SCOPED_ROWS = [base_row(rid, I if rid in ('DR-202', 'DR-203') else N, 'ROUTING-ASSESSED-ONLY-NOT-APPLIED',
                        SCOPED_TEXT[rid] + ' Register 08 is byte-identical 39->40 (%s). This review is an input to the integrated review and is not applied.' % REG_UNCH)
               for rid in ('DR-201', 'DR-202', 'DR-203', 'DR-204', 'DR-205')]

TCB = {
    'id': 'TCB-SCOPE-01', 'assessedOnceAsOneAssumption': True,
    'assumption': V39TCB['assumption'],
    'consequence': 'Rejecting or changing the assumption reopens all thirteen dependent rows together. It is a scope selection, not a containment guarantee, and repairs no historical attack. All thirteen author grades stay PENDING.',
    'dependentRows': TCB_DEPS, 'dependentRowCount': len(TCB_DEPS),
    'substantiveCurrentAssessment': [
        'It stays coherent as a scope selection on source40. Admission section 5 (no untrusted native/WASM, no imperative contributions or project hooks) is byte-identical 39->40: %s; prototype-report-inventory still admits no executable report hooks and is byte-identical: %s.' % (U['admission-and-qualification.md'], U['prototype-report-inventory.md']),
        'Source40 adds trust surfaces and states them as trust. The effective allowJs marker observation is trusted pre-Plan input: a consistent mode-and-kind remint closes a full Run with a different RunId (OBS40-04). Marker observations do not prove Cargo accepts a nested layout (OBS40-06). ExecutionInputsV1 remains a host TCB observation of stage returns (execution-inputs section 1).',
        'Untrusted inputs stay inert typed data and are more closed than in source39: policy-test rule and fact universe tokens refuse typed, an imported row must match subject and universe, and unit kinds are a closed projection enforced at closure (P40-POLICY, P40-NATIVE).',
        'S40-01 is a determinism defect in the published capture law: two conforming hosts encode the same returns differently. It is not a trust-boundary violation and does not change the assumption, although a product relying on the host observation needs the attribution law published. ADV40-01 is editorial.',
        'It remains unqualified. It rests on the authenticated closure/TCB inventory and provider process boundaries, and all %d gates are unperformed (qualified=true count %d).' % (len(GATES), gates_true),
    ],
    'reviewerPosition': 'NOT REJECTED',
    'standing': 'ASSESSED-COHERENT-UNQUALIFIED-ON-SOURCE40; final application adjudication not granted',
    'adjudicationOwner': 'The separate final application review, performed by a NEW other actual Claude origin: not this origin (%s) and not any author, design or blind origin. Not adjudicated here.' % ORIGIN,
    'prior39Standing': V39TCB['standing'],
}
for rid in TCB_DEPS:
    row = next(r for r in RES_ROWS if r['id'] == rid)
    if row['sharedDependency'] != 'TCB-SCOPE-01':
        GAPS.append('TCB dependent row lacks shared dependency: ' + rid)
if sum(1 for r in RES_ROWS if r['sharedDependency'] == 'TCB-SCOPE-01') != 13:
    GAPS.append('TCB dependent count is not 13')

RETAINED = {
    'residuals': len(RES_ROWS), 'authorGradesPending': sum(1 for r in RES_ROWS if r['authorGrade'] == 'PENDING'),
    'condition2Obligations': 28 if cond2_ok else None,
    'condition2Source': 'docs/v2/architecture/08-decision-and-readiness-register.md:385-391 (byte-identical 39->40: %s)' % REG_UNCH,
    'qualificationGatesUnperformed': len(GATES), 'qualificationGatesQualifiedTrue': gates_true,
    'recoveryCasesNotExecuted': PC['recoveryCasesNotExecuted'], 'condition5': 'NOT MET (not a design defect)',
    'd9PublishedSuccessor': 'Carried implementation-unit obligation (DR-007 / DR-011-R08); not a new blocker.',
    'finalApplication': 'Must be performed by a NEW other actual Claude origin, not this origin (%s) and not any author, design or blind origin.' % ORIGIN,
}
AUTHORITY = {'gradeGranted': False, 'activationGranted': False, 'implementationAuthorized': False, 'blindReconstructionClaimed': False,
             'source39ReviewConclusionInherited': False, 'frozenInputsModified': False, 'applicationOrReadinessGranted': False,
             'consumerArtifactsAccessedOrRepaired': False, 'historicalExportsRelabelled': False, 'productCommitPushOrActivation': False, 'subagentsOrWebUsed': False}
LIMITATIONS = [
    'Nonblind review. The reviewer read the author package, header-named root and codex evidence, and its own source39 review. No blind consumer artifact, its implementation, root replay results, private logs or the preliminary root source40 reference v1 were used.',
    'Reference Python models over synthetic inputs; no product code exists. No compiler, provider, host, OS durability, process isolation or cryptography is qualified. All 32 gates are unperformed and the 54 recovery cases are not executed (condition 5 NOT MET).',
    'Changed files that were not fresh-read were read as complete 39->40 diffs (delta40Read), not as whole files. This includes the five source-pins ledgers, whose pins are additionally exercised by the six executed pin-gated groups. Whole-file claims are made only for fresh40Read and inheritedUnchanged39Read; range reads and search-only sightings are listed separately.',
    'Several probes are not full Runs. Policy test compares the fixture with bounded production composition. Nested Cargo is at discover_units and enumeration-law level (full-Run closure was used for unit kinds). Comparison knowledge and custody are helper-level. The viewDigests probes use the maintained owner graph with reviewer-minted views and do not mint a multi-capability enumeration plan: reachability rests on enumeration-contract cell law and the capability matrix, seen via search and script output.',
    'OBS40-04 (consistent remint) was measured on the syntax-universe fixture, which has no tsjs program cell.',
    'Failed attempts are preserved and not counted. Run-termination attempt 1 (a probe defect: commit_inventory returns (record, digest)) is in receipts/probes/runterm-adv-v40.attempt1-probe-defect.json and receipts/runs/runterm-adv-v40.run.json. View-attribution attempt 1 (a harness defect: store pointers not recomputed after mutation, so the refusal was EXECUTION_INPUTS_REF_POINTER) is in receipts/runs/viewdigests-v40c.run.json and its stdout. Its probe receipt path was overwritten by attempt 2 because a separate copy was not permitted.',
    'In-process patches (the fixture helper assign_membership during full Runs, checker globals) were restored, and the probe copy was re-verified against the formal manifest after every run.',
    'The six ported source39 probes run with unedited expectations. Their owner bytes are unchanged 39->40 except check-workflow-projection, whose changed controls ran as a child, not as a ported probe.',
    'The package verifier and native probe are author tools re-executed on this review\'s copy. Content equality with the root verification and rebuild is evidence, not independent reconstruction. The 4 normalization-map negatives are exact recorded refusals and are not generalized.',
    'F-01..F-14 content lives outside the snapshot and was not re-derived.',
    'S40-01 predates source40 (execution-inputs owner bytes unchanged 39->40); this origin\'s source39 review missed it.',
    'No grade, activation, application, readiness or implementation authorization is granted. The 30 residuals, 28 condition-2 obligations and the D9 successor obligation are retained.',
]
