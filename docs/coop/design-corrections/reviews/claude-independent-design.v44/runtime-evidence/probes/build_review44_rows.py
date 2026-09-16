# Executed by build_review44.py in its own globals (exec). The 107 individually reasoned rows with current owners and
# consequences, the single TCB-SCOPE-01 object, retained obligations, authority and limitations. Flags are always false.

N, I = 'new-44', 'unchanged-43-basis'
BASIS_RULE = ('unchanged-43-basis: the named governing owner bytes (unchanged43GoverningOwners) are byte-identical 43->44, and the conclusion rests on that identity plus this origin\'s named source43 row assessment, quoted in unchanged43Basis. '
              'Re-executed suites and ported probes are corroboration only. new-44: the conclusion rests on a source44 read, diff, probe or measurement newly performed under this charter, including rows whose executable owners are unchanged but whose governing text, planning record or provider protocol owner changed. '
              'Every row carries its own current text, current owner and consequence. No row is carried forward in bulk, and no grade is assigned.')
V43ROWS = {r['id']: r for k in ('fDispositions', 'evaluationResidualDispositions', 'arDispositions', 'fwDispositions', 'inheritedResidualDispositions', 'scopedReviewOwnerDispositions') for r in V43[k]}
TCB_DEPS = ['RES-EP13-02', 'RES-EP13-04', 'RES-EP13-12', 'RES-EP13-13', 'RES-EP13-16', 'RES-EP13-18', 'IR-EP13-NB-01', 'IR-EP13-NB-03', 'IR-EP13-NB-04', 'AX6', 'AX9', 'MD5', 'RX2c']


def base_row(rid, basis, disposition, assessment, owner, consequence, owners=None, **extra):
    prior = V43ROWS.get(rid)
    if prior is None:
        GAPS.append('no source43 row for ' + rid)
    if basis == I:
        if not owners:
            GAPS.append('unchanged basis without named governing owners: ' + rid)
        elif owners != 'outside-snapshot' and not all(U.get(o) for o in owners):
            GAPS.append('unchanged basis claimed for a changed owner: %s %s' % (rid, {o: U.get(o) for o in owners}))
    r = {'id': rid, 'prior43Disposition': prior['disposition'] if prior else None, 'prior43AssessmentBasis': prior['assessmentBasis'] if prior else None,
         'disposition': disposition, 'assessmentBasis': basis, 'unchanged43Basis': (prior['currentAssessment'] if (prior and basis == I) else None),
         'unchanged43GoverningOwners': (owners if basis == I else None), 'currentAssessment': assessment, 'currentOwner': owner, 'consequence': consequence}
    r.update(extra)
    r.update(appliedByThisReview=False, finalApplicationOutcomeGranted=False)
    return r


RESOWN = 'evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review'
F_ROWS = []
for i in range(1, 15):
    rid = 'F-%02d' % i
    st = V43ROWS[rid]['priorRootStanding']
    F_ROWS.append(base_row(rid, I, 'CARRIED-NOT-REGRADED',
                           '%s: prior root standing %s (root-independent36-completion-assessment.v1) carried without regrade. The F record lives outside the frozen snapshot, and none of the 30 source43->44 delta files is an F record.' % (rid, st),
                           'root custody of the F record (outside the frozen snapshot)', 'No source44 change; remains carried without regrade and is not source44 acceptance.', owners='outside-snapshot', priorRootStanding=st))

RP = lambda k: PBY[k]['result']['rows']
RES_TEXT = {
    'RES-EP13-01': (I, 'Plan and derivation joins stay inside complete replay on byte-identical owners (evaluator_replay_model, identity-model, identity-schemas); the full-replay child equals root and this origin\'s source43 receipt, and the 17 package RunIds are measured unchanged.',
                    'Grade PENDING; residual retained.', ['evaluator_replay_model.v3.py', 'identity-model.v3.py', 'identity-schemas.v3.json']),
    'RES-EP13-02': (N, 'Depends on TCB-SCOPE-01. Host capture and host-held startup inputs are trusted observations. The ported capture-join measurement on source44 still admits a non-provider-producer view and refuses it only at closure (ADV42-01). The startup reference takes the verified descriptors, Plan identity row, signed row and planned stages as host inputs, and an extra planned stage is converted verbatim (OBS44-05). Provider payloads are never trusted: every provider wire and startup record is admitted or refused before a source byte or coverage entry. No answer-provenance claim against the host is made.',
                    'Grade PENDING; reopens with TCB-SCOPE-01 only.', None),
    'RES-EP13-03': (I, 'The admission contract and residual ledger are byte-identical 43->44, and the finite historical measurement is unchanged.', 'Grade PENDING; finite historical measurement unchanged.',
                    ['admission-and-qualification.md', 'evaluation-residual-dispositions.proposed.json']),
    'RES-EP13-04': (N, 'Depends on TCB-SCOPE-01. Closed input admission is unchanged, and source44 closes the provider records it publishes. Every provider-handshake and provider-startup definition is closed, exact JSON typing refuses a float-typed identity version, and unknown members refuse at SCHEMA: payload protocolMajor on TS Hello, wire mode booleans, repositoryResolution on a TS OpenUniverse and analysisOrdinal on the pre-Analyze payload (P44-WIRE, P44-STARTUP).',
                    'Grade PENDING; reopens with TCB-SCOPE-01 only.', None),
    'RES-EP13-05': (N, 'The frozen subject was verified outside every author instrument: formal44 manifest e873c8db..., archive c21d0491..., all 12,919 members by hash and length (738,157,930 bytes), parent43 db43ee76... (12,913 members), the declared chain, the exact 24/6/0 delta and every entry of the five pin ledgers.', 'Grade PENDING.', None),
    'RES-EP13-06': (N, 'canonical.py stays outside the delta (%s). Source44 digests were recomputed with the reviewer\'s own oracles, and each equals the published value: TS descriptor digests (canonical JSON), the TS batch commitment (length-first CBOR), the contract digest (raw bytes) and the native semantic-universe identity (H recipe). The ported run-termination probe keeps every commit-inventory row identical to source43.' % U['canonical.py'], 'Grade PENDING.', None),
    'RES-EP13-07': (I, 'Seal and replay owners are byte-identical 43->44, and the analysis-seal child equals root and this origin\'s source43 receipt.', 'Grade PENDING.', ['evaluator_replay_model.v3.py', 'identity-model.v3.py']),
    'RES-EP13-08': (I, 'A bounded historical measurement. Source44 publishes field-level provider wire and startup successors and claims no proof over all PlanIntents or providers.', 'Grade PENDING.', ['evaluation-residual-dispositions.proposed.json']),
    'RES-EP13-09': (N, 'Provenance stays distinct from correctness on source44. Package v21 semantic-controls1 keeps owner ADMIT with semantic REFUSE, content-equal to the root rebuild verification, and a clean pre-Analyze Unavailable converts to indeterminate provider-unavailable coverage, never an answer or an operational fault.', 'Grade PENDING.', None),
    'RES-EP13-10': (N, 'Author self-counters did not decide this review. The native checker grows from 388 to 477 cases, which is reference self-consistency. The decisive evidence is the reviewer\'s own discriminators with source-bound expectations and independent oracles (P44-WIRE %d rows, P44-STARTUP %d rows) and the old-versus-new occupancy gate comparison.' % (RP('P44-WIRE'), RP('P44-STARTUP')), 'Grade PENDING.', None),
    'RES-EP13-11': (N, 'Failures stay recorded by cause. This review preserves three failed first attempts. Reference-comparison attempt 1 raised KeyError because evaluator3 check records carry no id key. Package-v21 probe attempt 1 expected only the package identity to differ, but the root verified the pre-binding package with fewer files. Wire probe attempt 1 expected byte-identical gate outputs, but source44 renamed the omitted-delivery label. Denied shell invocations produced no receipts and were replaced by tool reads.', 'Grade PENDING.', None),
    'RES-EP13-12': (N, 'Depends on TCB-SCOPE-01. No sole Python guard enters product authority. The wire and startup references refuse before admission, and only host fact admission and the Run owners grant facts or coverage. The exchange catches the three distinct AdmissionError classes (wire, startup, native) explicitly, and SELECTED_COVER still detects internal capture inconsistency, never malicious omission.', 'Grade PENDING; reopens with TCB-SCOPE-01 only.', None),
    'RES-EP13-13': (N, 'Depends on TCB-SCOPE-01. The discriminators loaded each owner module in its own process from verified copies (source44-pkg, plus base43 for the gate comparison), and the copies were re-verified unchanged afterwards (copy-verification-final.json).', 'Grade PENDING; reopens with TCB-SCOPE-01 only.', None),
    'RES-EP13-14': (I, 'The differential census is not used as an oracle, and no source44 delta file is a census owner.', 'Grade PENDING.', ['evaluation-residual-dispositions.proposed.json', 'current-source-map.proposed.md']),
    'RES-EP13-15': (I, 'The C-2 v4 self-census is not elevated. Enumeration owners are byte-identical 43->44, and their 54 checker cases equal this origin\'s source43 receipt after removing path fields only.', 'Grade PENDING.',
                    ['enumeration-contract.v1.md', 'enumeration_model.v1.py', 'enumeration-plan.schema.v1.json', 'check-enumeration.v1.py']),
    'RES-EP13-16': (N, 'Depends on TCB-SCOPE-01. Producer flags cannot bypass replay: row-attribution re-derivation and exact VIEW_TOTALITY are unchanged. The execution-inputs contract and model changed only in historical FactBatch naming (contract :272, :290; model note :109-110), and the 95 cases are unchanged modulo paths.', 'Grade PENDING; reopens with TCB-SCOPE-01 only.', None),
    'RES-EP13-17': (N, 'Text-only disclosures remain text-only. Source44\'s wire and startup prose is paired with closed schemas, a published order table and reference joins, and it was independently discriminated. The reference-scope limits (section 9.7 :3285-3294) remain explicit disclosures, not guarantees.', 'Grade PENDING.', None),
    'RES-EP13-18': (N, 'Depends on TCB-SCOPE-01. Native discovery and custody code is unchanged: the model delta is two appended regions, the wire loader and the startup section. Marker observations stay trusted, and ported native (%d rows) and custody (%d rows) observations are identical to source43. Empty dependency custody is now explicit and measured.' % (PORTED_EQUAL['P44-PORTED-NATIVE']['rows'], PORTED_EQUAL['P44-PORTED-CUSTODY']['rows']), 'Grade PENDING; reopens with TCB-SCOPE-01 only.', None),
    'RES-EP13-19': (N, 'Substantive review on source44: field-level wire and startup discriminators for both languages, cross-owner selector consistency and a planning-layer binding assessment (ADV44-01). The retained advisory was re-measured rather than carried, and all pinned groups pass.', 'Grade PENDING.', None),
    'IR-EP13-NB-01': (N, 'Depends on TCB-SCOPE-01. Every source44 probe ran in-process with owner modules. The provider references frame nothing and run no worker, so containment is not claimed.', 'Grade PENDING; reopens with TCB-SCOPE-01 only.', None),
    'IR-EP13-NB-02': (N, 'No name scan decides a provider route. Refusals carry typed keys, the exchange selects by typed exception class and key, the Unavailable payload class follows the phase and closed-schema members, and frame routing uses table rows over protocol frame vocabulary, not file names or messages.', 'Grade PENDING.', None),
    'IR-EP13-NB-03': (N, 'Depends on TCB-SCOPE-01. Loaded owner instances stay reachable in-process. The wire, startup and native modules each load their own canonical module, which is why the exchange names all three AdmissionError classes. Host-held startup inputs are trusted context that can only refuse or select.', 'Grade PENDING; reopens with TCB-SCOPE-01 only.', None),
    'IR-EP13-NB-04': (N, 'Depends on TCB-SCOPE-01. One TCB account, assessed once on source44, covers all thirteen rows.', 'Grade PENDING; reopens with TCB-SCOPE-01 only.', None),
    'IR-EP13-NB-05': (N, 'Contradictory prose still needed substantive review. Source43 texts named one generic historical FactBatchV2, although typescript-semantic historically carries delivery.v2 FactBatchV1, and the P3 state update described frame booleans. Source44 disambiguates both per owner, and readings made under the older bytes are not relabelled as reader errors.', 'Grade PENDING.', None),
    'IR-EP13-NB-06': (I, 'Historical attacker cost is preserved as history; no source44 file addresses it.', 'Grade PENDING.', ['evaluation-residual-dispositions.proposed.json']),
    'IR-EP13-NB-07': (I, 'The original environment is preserved. This review names its interpreter (/tmp/opensip-architecture-review-env/bin/python -I -B) and verifies every pin of the five ledgers on source44.', 'Grade PENDING.', ['evaluation-residual-dispositions.proposed.json']),
    'AX6': (N, 'Depends on TCB-SCOPE-01. None of the 24 changed or 6 added source44 files claims same-process route-region protection; all diffs and creation diffs were read.', 'Grade PENDING; reopens with TCB-SCOPE-01 only.', None),
    'AX9': (N, 'Depends on TCB-SCOPE-01. The source44 additions (closed provider records, handshake and startup joins, host coverage conversion) are typed admission law under a trusted host, not a protection mechanism.', 'Grade PENDING; reopens with TCB-SCOPE-01 only.', None),
    'MD5': (N, 'Depends on TCB-SCOPE-01. Source44 adds no Python-containment mechanism (delta read).', 'Grade PENDING; reopens with TCB-SCOPE-01 only.', None),
    'RX2c': (I, 'Depends on TCB-SCOPE-01. Complete replay and full-Run closure on the same manifest remain reproducibility evidence, not containment, and the replay owners are byte-identical 43->44.', 'Grade PENDING; reopens with TCB-SCOPE-01 only.',
             ['evaluator_replay_model.v3.py', 'identity-model.v3.py']),
}
RES_ROWS = []
for rid in ['RES-EP13-%02d' % i for i in range(1, 20)] + ['IR-EP13-NB-%02d' % i for i in range(1, 8)] + ['AX6', 'AX9', 'MD5', 'RX2c']:
    basis, text, cons, owners = RES_TEXT[rid]
    p = V43ROWS[rid]
    dep = 'TCB-SCOPE-01' if rid in TCB_DEPS else None
    if (p.get('sharedDependency') or None) != dep:
        GAPS.append('shared dependency differs from source43 for ' + rid)
    RES_ROWS.append(base_row(rid, basis, 'ASSESSED-CONSISTENT-GRADE-PENDING', text + ' Historical limitation preserved; no historical guard claimed repaired.', RESOWN, cons, owners=owners,
                             proposedDisposition=p['proposedDisposition'], authorGrade='PENDING', sharedDependency=dep, residualRetained=True))

AR_TEXT = {
    'AR-01': (I, 'NO-NEW-ISSUE', 'Admission section 1 is byte-identical 43->44, and the ported query carriers (%d rows) are identical to source43.' % PORTED_EQUAL['P44-PORTED-QUERY']['rows'], 'No change required.', ['admission-and-qualification.md']),
    'AR-02': (I, 'NO-NEW-ISSUE', 'Admission sections 2-4 and the gate ledger are byte-identical 43->44: %d gates, none qualified, and no delta file is a gate owner.' % len(GATES), 'All gates stay unperformed.', ['admission-and-qualification.md', 'qualification-gates.proposed.json']),
    'AR-03': (I, 'NO-NEW-ISSUE', 'The security discovery text is byte-identical 43->44, and the ported custody rows are identical to source43.', 'No change required.', ['security-and-lifecycle.md']),
    'AR-04': (I, 'NO-NEW-ISSUE', 'The security trust-time text is byte-identical 43->44, and the security group stdout equals root and this origin\'s source43 receipt.', 'No change required.', ['security-and-lifecycle.md']),
    'AR-05': (I, 'NO-NEW-ISSUE', 'The security root chain and revocation text is byte-identical 43->44; no delta file touches it.', 'No change required.', ['security-and-lifecycle.md']),
    'AR-06': (I, 'NO-NEW-ISSUE', 'Platform admission and the carrier DDL are byte-identical 43->44, and the ported read-only carrier rows (%d) are identical to source43.' % PORTED_EQUAL['P44-PORTED-CARRIER']['rows'], 'No change required.', ['security-and-lifecycle.md', 'carrier-dispatch.v3.json']),
    'AR-07': (N, 'NO-NEW-ISSUE (ADVISORY ADV44-01 ON PLANNING BINDING)', 'Native section 9 changed: field-level provider handshakes (9.1, 9.4), limits (9.3), FactBatch (9.6) and startup successors (9.7). It was read completely (:2781-3297) with the complete diff and discriminated per language (CH44-WIRE-HANDSHAKE, CH44-FACTBATCH-AND-OCCUPANCY, CH44-STARTUP-OPEN-UNIVERSE, CH44-PRE-ANALYZE-UNAVAILABLE, CH44-COVERAGE-AND-CANCELLATION). Sections 3 and 5 lie outside every hunk; empty dependency custody and the prepared authorization joins now reach the startup payload. The native group passes 477/477.', 'No change required; the planning advisory is optional.', None),
    'AR-08': (I, 'NO-NEW-ISSUE', 'The invocation and repair text is byte-identical 43->44, and the ported repair:2 rows are identical.', 'No change required.', ['workflows-and-surfaces.md', 'repair_closed_world_selection.v1.py']),
    'AR-09': (N, 'NO-NEW-ISSUE (ADVISORY ADV42-01 RETAINED)', 'identity-and-evidence is byte-identical 43->44. The wire universe coordinate is the native semantic-universe identity under the foundation H recipe, recomputed independently and joined to universeKey, CoverageKeyV2 suffixes and subject scopes; snapshot2 and plan2 texts are schema-bound. S40-01 remains resolved, and ADV42-01 is retained on re-measured values.', 'No change required; the advisory is optional.', None),
    'AR-10': (I, 'NO-NEW-ISSUE', 'The baseline and comparison text is byte-identical 43->44, and the ported comparison-knowledge rows are identical.', 'No change required.', ['workflows-and-surfaces.md']),
    'AR-11': (I, 'NO-NEW-ISSUE', 'The comparison and import text is byte-identical 43->44, and the execution-inputs child equals root after removing path fields only.', 'No change required.', ['workflows-and-surfaces.md']),
    'AR-12': (N, 'NO-NEW-ISSUE', 'Native section 4 lies outside every source44 hunk (complete diff read). CoverageResultV3 and CoverageKeyV2 are reused unchanged as the Coverage entry type, the host conversion admits its entries through admit_coverage_result_v3, and the atoms child equals root and source43.', 'No change required.', None),
    'AR-13': (N, 'NO-NEW-ISSUE', 'Native sections 1, 2, 6 and 8 lie outside every source44 hunk; the section intro sentence at :78-85 only renames provider frame names per language. Enumeration cases equal source43 after removing path fields only, and the nine native-v2 membership probes equal root.', 'No change required.', None),
    'AR-14': (I, 'NO-NEW-ISSUE', 'The stage transition and lease bytes are unchanged 43->44; no delta file is a lifecycle owner.', 'No change required.', ['security-and-lifecycle.md']),
    'AR-15': (I, 'NO-NEW-ISSUE', 'The contract index README and its D-372 application text are byte-identical 43->44.', 'No change required.', ['README.md']),
    'AR-16': (N, 'NO-NEW-ISSUE', 'workflows-and-surfaces is byte-identical, and source44 adds no D9 code. Provider wire and startup refusals map to the existing PROVIDER.PROTOCOL_VIOLATION (operational-failed, exit 4), and a clean pre-Analyze Unavailable maps to the existing COVERAGE.PROVIDER_UNAVAILABLE (indeterminate); both were measured. The D9 successor stays carried.', 'No change required.', None),
}
AR_ROWS = []
for i in range(1, 17):
    rid = 'AR-%02d' % i
    basis, disp, text, cons, owners = AR_TEXT[rid]
    p = V43ROWS[rid]
    c = p['contract']
    unchanged = same(S43, S44, c)
    if basis == I and not unchanged:
        GAPS.append('unchanged basis claimed for a changed contract: ' + rid)
    AR_ROWS.append(base_row(rid, basis, disp, text, c + ' (' + p['selector'] + ')', cons, owners=owners, contract=c, selector=p['selector'], statusRecorded=p['statusRecorded'],
                            contractSha256=sha(S44 + '/' + c), contractUnchanged43to44=unchanged))

FW_SUFFIX = (' Owner module and milestone match current-source-map (byte-identical 43->44: %s) and repository-file-inventory, whose only source44 change is the open-decision handshake sentence; its file and package rows are identical (%s).'
             % (U['current-source-map.proposed.md'], INV_ROWS_EQUAL))
FW_TEXT = {
    'FW-01': ('discovery.rs binding construction obligation is unchanged; enumeration owners are byte-identical 43->44.', 'Not executed.'),
    'FW-02': ('review.rs review-brief carriers are unchanged; the ported carriers are identical to source43.', 'Not executed.'),
    'FW-03': ('analysis.rs composes provider work, admission, evaluation and complete replay (inventory :695). It keeps the ADV42-01 verification obligation and now also composes the per-language provider exchange. The host must supply the verified descriptors, Plan identity row, signed row, universe expectations and pre-spawn planned stages that the reference takes as trusted inputs (OBS44-05). Wire dispatch sits in crates/components/src/provider_protocol.rs, and candidate/Coverage admission in crates/host/src/fact_admission.rs (:751).', 'Implementation obligations retained; not executed.'),
    'FW-04': ('imports.rs is unchanged; the typed-null targetUniverse account stands on source44.', 'Not executed.'),
    'FW-05': ('comparison.rs presence knowledge is unchanged; the ported comparison rows are identical.', 'Not executed.'),
    'FW-06': ('finalization.rs delivery laws are unchanged; the commit-inventory recipe is re-derived identically on source44.', 'Not executed.'),
    'FW-07': ('invocation.rs argvDigest is unchanged on source44.', 'Not executed.'),
    'FW-08': ('The outcomes.rs detail allowlist stays sufficient for source44. Provider refusals use PROVIDER.PROTOCOL_VIOLATION and the pre-Analyze conversion uses COVERAGE.PROVIDER_UNAVAILABLE, both existing; internal refusal keys never become public details, and no detail is added.', 'Not executed.'),
    'FW-09': ('review.rs candidates/inspect carriers are unchanged; the ported carriers are identical.', 'Not executed.'),
    'FW-10': ('The repair.rs repair:2 constructor is unchanged; the ported repair rows are identical.', 'Not executed.'),
    'FW-11': ('comparison.rs baseline.show is unchanged; no provider change reaches it.', 'Not executed.'),
    'FW-12': ('review.rs produce-brief stays host-only on source44.', 'Not executed.'),
    'FW-13': ('configuration.rs policy-test admission routes are unchanged; the ported policy rows are identical.', 'Not executed.'),
    'FW-14': ('discovery.rs recommend units is unchanged; the same binding construction rule applies on source44.', 'Not executed.'),
    'FW-15': ('policy.rs show/test is unchanged; the policy-derivation child equals source43.', 'Not executed.'),
}
FW_ROWS = []
for i in range(1, 16):
    rid = 'FW-%02d' % i
    text, cons = FW_TEXT[rid]
    p = V43ROWS[rid]
    FW_ROWS.append(base_row(rid, N, 'OWNER-ROUTING-ASSESSED-NOT-EXECUTED', text + FW_SUFFIX, ', '.join(p['owners']) + ' (' + p['milestone'] + ')', cons,
                            owners=p['owners'], milestone=p['milestone'], source43AssessmentStillApplies=p['currentAssessment']))

IRU = U['inherited-residuals.proposed.md']
DROWN = 'successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md'
RO = ['inherited-residuals.proposed.md', 'current-source-map.proposed.md']
DR_TEXT = {
    'DR-001': (I, 'current-source-map and the residual ledgers are byte-identical 43->44.', 'Condition-1 obligation retained.', RO + ['evaluation-residual-dispositions.proposed.json']),
    'DR-002': (N, 'ExecutionInputsV1 view attribution and exact selection remain published. The execution-inputs contract and model changed only in historical FactBatch naming, and S40-01 remains resolved.', 'Condition-1 obligation retained.', None),
    'DR-003': (I, 'Read-only carrier routes are unchanged 43->44, and the 54 recovery cases remain unexecuted.', 'Condition-1 obligation retained; release demonstration still required.', RO + ['commit-recovery-readonly.v3.md', 'carrier-dispatch.v3.json']),
    'DR-004': (I, 'Native binding construction consumed by enumeration is unchanged, and the explicit TS/JS null refusal stands (enumeration owners byte-identical 43->44).', 'Condition-1 obligation retained.', RO + ['enumeration-contract.v1.md', 'enumeration_model.v1.py']),
    'DR-005': (N, 'Custody reference groups pass on source44, and empty dependency custody is now explicit: a null dependency set id refuses, and skipping DependencySourceManifest/Seal/Accepted faults. Native carrier qualification is still required.', 'Condition-1 obligation retained.', None),
    'DR-006': (I, 'The descriptor graph is unchanged 43->44, and the full-replay child equals root and source43.', 'Condition-1 obligation retained.', RO + ['evaluator_replay_model.v3.py', 'identity-schemas.v3.json']),
    'DR-007': (I, 'The D9 published successor artifact remains a carried implementation-unit obligation; the public-detail registry and workflows contract are byte-identical 43->44.', 'Mandatory future implementation-unit obligation; not a new blocker.', RO + ['public-detail-registry.v1.json', 'workflows-and-surfaces.md']),
    'DR-008': (I, 'The applied retention posture is unchanged 43->44, and no provider change reaches retention.', 'Condition-1 obligation retained.', RO + ['security-and-lifecycle.md', 'identity-and-evidence.md']),
    'DR-009': (N, 'The host capture stays outside the sealed Run. The execution-inputs model changed only in a note string, and census exclusion is unchanged.', 'Condition-1 obligation retained.', None),
    'DR-010': (I, 'Bounded first-party composition is unchanged 43->44.', 'Condition-1 obligation retained.', RO + ['evaluator-composition-contract.v3.md']),
    'DR-011': (I, 'The blind implementer litmus follows final integration and is not closed by this nonblind review.', 'Condition-1 obligation retained.', RO),
    'DR-011-R01': (N, 'Fact-plane successor schemas: fact-batch.schema.v3 changed only its description and its whenAbsent, helloLimits, commitments and wireProjection annotations (per-language historical payloads). The V3 required members and properties and FactCandidateV1 are unchanged.', 'Retained.', None),
    'DR-011-R02': (I, 'Imperative plugins stay outside D-371 on source44.', 'Retained.', RO + ['admission-and-qualification.md']),
    'DR-011-R03': (I, 'plan2 EnumerationPlanV1 binding joins are unchanged 43->44, and explicit TS/JS null entries still refuse.', 'Retained.', RO + ['enumeration-plan.schema.v1.json', 'enumeration_model.v1.py']),
    'DR-011-R04': (I, 'The carrierFormat mapping is unchanged 43->44.', 'Retained.', RO + ['carrier-dispatch.v3.json']),
    'DR-011-R05': (N, 'The Rust protocol major stays 3 and the TypeScript major 2. Source44 publishes their field-level handshakes and startup records without a new major (the registered HelloV3 bytes are superseded by name, not edited), as measured in P44-WIRE and P44-STARTUP.', 'Retained.', None),
    'DR-011-R06': (I, 'Typed close_run outcomes through the graph query are unchanged: the query owners are byte-identical 43->44.', 'Retained.', RO + ['query_projection_model.v3.py', 'query-projection-contract.v3.md']),
    'DR-011-R07': (I, 'Query retained-availability routes and partial disclosure are unchanged: the query owners are byte-identical 43->44.', 'Retained.', RO + ['query_projection_model.v3.py', 'query-projection-contract.v3.md']),
    'DR-011-R08': (I, 'The D9 successor remains carried on source44 (DR-007).', 'Mandatory future implementation-unit obligation.', RO + ['public-detail-registry.v1.json']),
    'DR-011-R09': (N, 'Semantic identity still excludes attempt identity: executionId is correlation only on the wire, the 17 package export stores are byte-equal to package20, and the measured RunIds equal source43.', 'Retained.', None),
    'DR-011-R10': (I, 'OPEN: this nonblind source44 review cannot close the fresh blind implementer litmus.', 'Retained open.', RO),
    'DR-011-R11': (I, 'Real platform durability remains unmeasured on source44; the 54 cases are not executed.', 'Retained.', RO + ['commit-recovery-readonly.v3.md']),
    'DR-011-R12': (N, 'Depends on TCB-SCOPE-01, assessed once on source44.', 'Retained; reopens with TCB-SCOPE-01 only.', None),
    'DR-011-R13': (N, 'Source44 adds closed field-level schema documents and supersedes three registered definitions by name without editing the registered bundle, whose raw SHA-256 remains the registered payloadSchemaDigest. No identity record or schema major changes, consistent with the composition profile.', 'Retained.', None),
    'DR-011-R14': (I, 'CFG-6/TM is unchanged 43->44.', 'Retained.', RO),
    'DR-011-R15': (N, 'Trusted request context stays host-only. The signed row, verified descriptors, Plan identity row, universe expectations and planned stages are host inputs the reference takes as arguments; none is provider-authored, and every provider-authored member is admitted against them.', 'Retained.', None),
    'DR-011-R16': (I, 'There is no executable report-hook admission; prototype-report-inventory and admission section 5 are unchanged 43->44.', 'Retained.', RO + ['prototype-report-inventory.md', 'admission-and-qualification.md']),
}
DR_ROWS = []
for rid in ['DR-%03d' % i for i in range(1, 12)] + ['DR-011-R%02d' % i for i in range(1, 17)]:
    basis, text, cons, owners = DR_TEXT[rid]
    DR_ROWS.append(base_row(rid, basis, 'CONDITION-1-OBLIGATION-RETAINED-ASSESSED',
                            text + ' Successor routing in inherited-residuals.proposed.md (byte-identical 43->44: %s) is consistent with source44.' % IRU, DROWN, cons, owners=owners))

REGU = U['08-decision-and-readiness-register.md']
SCOPED_TEXT = {
    'DR-201': (N, 'Semantic-correctness owner row: the provider wire and startup successors, the retained ADV42-01 and the planning advisory ADV44-01 fall in its area.', None),
    'DR-202': (I, 'Delivery/operations owner row: recovery, repair and loader TCB are unchanged 43->44.', ['08-decision-and-readiness-register.md', 'commit-recovery-readonly.v3.md']),
    'DR-203': (I, 'Prototype-lessons owner row (PARTIAL-SCOPED): no source44 delta file is the prototype reference.', ['08-decision-and-readiness-register.md', 'prototype-report-inventory.md']),
    'DR-204': (N, 'V1/coop invariant owner row: every pin of the five ledgers was verified against the formal manifest (16 changed and 5 added pins). Layer v12 binds the changed coverage sources and preserves v8-v11 byte-identically, with ADV44-01 on the unbound P3 table.', None),
    'DR-205': (N, 'Small-core/components owner row: TCB-SCOPE-01 remains coherent on source44. Provider protocol dispatch stays a component (crates/components/src/provider_protocol.rs), and fact admission stays a host validator.', None),
}
SCOPED_ROWS = [base_row(rid, SCOPED_TEXT[rid][0], 'ROUTING-ASSESSED-ONLY-NOT-APPLIED', SCOPED_TEXT[rid][1] + ' Register 08 byte-identical 43->44 (%s).' % REGU,
                        'register 08 condition-3 review owner row ' + rid, 'Input to the integrated review; routing only, not applied.', owners=SCOPED_TEXT[rid][2])
               for rid in ('DR-201', 'DR-202', 'DR-203', 'DR-204', 'DR-205')]

V43TCB = V43['sharedAssumptionTCBSCOPE01']
TCB = {
    'id': 'TCB-SCOPE-01', 'assessedOnceAsOneAssumption': True,
    'assumption': 'Authenticated selected in-process host/evaluator code is trusted; providers and inert inputs are untrusted; adversarial code sharing the process is outside the product threat model.',
    'consequence': 'Rejecting or changing the assumption reopens the thirteen dependent rows jointly, not as thirteen independent proofs. It repairs no historical attack and qualifies no containment. All thirteen author grades stay PENDING.',
    'dependentRows': TCB_DEPS, 'dependentRowCount': len(TCB_DEPS),
    'currentAssessment': 'NOT REJECTED: coherent as a scope selection on source44 and unqualified; the source44 changes add closed provider admission law, not trust.',
    'substantiveCurrentAssessment': [
        'Coherent as a scope selection on source44: admission section 5 (byte-identical 43->44: %s) and prototype-report-inventory (byte-identical: %s) still admit no untrusted native/WASM, imperative contributions or executable report hooks.' % (U['admission-and-qualification.md'], U['prototype-report-inventory.md']),
        'Providers stay untrusted. Every provider-authored Hello, HelloAck, UniverseAccepted, NativeContextVerified, Unavailable, Coverage and Cancelled member is checked against host-held values, and a refusal precedes any source byte or coverage entry (%d wire and %d startup checks).' % (RP('P44-WIRE'), STARTUP_CHECKS),
        'Host inputs stay TCB. The verified descriptors, Plan identity row, signed row, universe expectations and planned stages are trusted host inputs, and the reference joins do not re-derive them (OBS44-05). Capture remains a host observation: ADV42-01 is retained as an implementation verification obligation, not a trust-boundary violation.',
        'View producer closures must still be Plan-selected providers at Run closure (CLOSURE_FIELD_KIND re-measured on source44).',
        'Unqualified: the assumption rests on the authenticated closure/TCB inventory and provider process boundaries, and all %d gates are unperformed (qualified=true %d).' % (len(GATES), gates_true),
    ],
    'reviewerPosition': 'NOT REJECTED', 'standing': 'ASSESSED-COHERENT-UNQUALIFIED-ON-SOURCE44; final application adjudication not granted',
    'adjudicationOwner': 'separate final application review, by a NEW different actual Claude origin (not this origin %s and not any author, design or blind origin)' % ORIGIN,
    'prior43Standing': V43TCB['standing'],
}
for rid in TCB_DEPS:
    if next(r for r in RES_ROWS if r['id'] == rid)['sharedDependency'] != 'TCB-SCOPE-01':
        GAPS.append('TCB dependent row lacks shared dependency: ' + rid)

RETAINED = {
    'residuals': len(RES_ROWS), 'authorGradesPending': sum(1 for r in RES_ROWS if r['authorGrade'] == 'PENDING'),
    'condition2Obligations': 28 if cond2_ok else None,
    'condition2Source': 'docs/v2/architecture/08-decision-and-readiness-register.md:385-391 (byte-identical 43->44: %s)' % REGU,
    'productQualificationGates': {'count': len(GATES), 'qualifiedTrue': gates_true, 'standing': 'UNPERFORMED'},
    'plannedRecoveryCases': {'count': PC['recoveryCases'], 'notExecuted': PC['recoveryCasesNotExecuted'], 'standing': 'UNPERFORMED'},
    'condition5': 'NOT MET (not a design defect)',
    'd9PublishedSuccessor': 'Mandatory future implementation-unit obligation (DR-007 / DR-011-R08); not a newly invented design blocker.',
    'adv4201ImplementationVerification': 'crates/host/src/analysis.rs verification that no returned view is listed on another producer\'s complete receipt (root routing; not executed).',
    'adv4401PlanningBinding': 'Optional planning-owner improvement: bind protocol3-transitions.v1.json (and fact-batch.schema.v3.json) in a future layer or state their binding through the formal manifest (non-blocking).',
    'providerImplementationObligations': 'Framing, worker processes, compilers, stage-stream and coverage commitments, Rust Cancelled payload validation and host user-interruption reduction remain owned by their inherited laws and are unqualified (section 9.7 reference scope).',
    'gradeAndConditionOwner': 'All 30 evaluation grades and 28 condition-2 obligations belong to final application adjudication.',
    'finalApplication': 'Requires a NEW different actual Claude origin, not this origin (%s) and not any author, design or blind origin.' % ORIGIN,
    'acceptanceStanding': 'Source-level acceptance only; distinct from final application, readiness and product qualification.',
}
AUTHORITY = {'gradeGranted': False, 'activationGranted': False, 'implementationAuthorized': False, 'blindReconstructionClaimed': False,
             'freshOriginIndependenceClaimed': False, 'source43ReviewConclusionInherited': False, 'frozenInputsModified': False,
             'applicationOrReadinessGranted': False, 'productQualificationGranted': False, 'blindConsumerArtifactsOrOutcomesAccessed': False,
             'authorRuntimeHistoriesRead': False, 'historicalExportsRelabelled': False, 'runIdsReminted': False, 'productCommitPushOrActivation': False,
             'subagentsWebOrPrivateLogsUsed': False}
LIMITATIONS = [
    'Nonblind successor review by the origin that completed the source40, source42 and source43 reviews; not fresh-origin independence. Evidence read: the four source-only author reports, the root clarification and companion checks, root reference/package records and codex receipts. No author runtime history, blind consumer artifact, export, helper, report or root blind outcome was read.',
    'One content search whose glob named two model files under docs/coop/design-corrections did not exclude reviews/**. It surfaced file names and one signature line each from snapshot-internal historical review copies, including a directory named blind-corrections-author.v1. The overflow file was never opened, nothing from those copies was read or used, and every later search named exact current paths (readScope.searchOnlySightings).',
    'Reference Python models over fixtures; no product code. The provider references frame no bytes and run no worker, host process or compiler. Snapshot, dependency-source, prepared, Analyze and FactBatch frames are abstract events in the exchange, fixture host inputs are not a verified Plan, and nothing here is complete retained Run replay. Stage-stream and coverage commitments, the Rust Cancelled payload and host user-interruption reduction are not exercised.',
    'Whole-file claims are limited to fresh44Read and inheritedUnchanged43Read. native-evidence.md was read by complete ranges for section 0 and section 9 plus its complete diff. The new schema documents, order table and both provider models were read completely. The native model and checker were read in named ranges plus complete diffs, and the generated native report as a complete diff. native-cases.v2.json (+6274 lines) was read only by named fixture and case ranges plus a structured listing of its startup-exchange cases; its complete diff was not read, and all 477 cases were executed by the native group. Other changed files were read as complete diffs.',
    'The root scope clarification\'s before bytes belong to the author runtime and were not read, so "No executable behavior changed" was not independently diffed; the final bytes were assessed directly (OBS44-09).',
    'Failed attempts preserved and not counted: reference-comparison-v44 attempt 1 (KeyError on evaluator3 check records), probe-package-v21 attempt 1 (one row expected only the package manifest to differ; receipt kept as package-v21.attempt1-row-expectation-too-narrow.json), probe-wire44 attempt 1 (seven rows expected byte-identical gate outputs across the renamed delivery label; receipt kept as wire44.attempt1-gate-label-expectation-too-narrow.json), and copies-final attempt 1, which was superseded by a re-verification after the last probe run. Several shell invocations (cp, a cat loop, a shell loop of probes) were denied by the harness and replaced by tool reads or individual runs.',
    'Ported source43 probes keep their original labels ("source40"/"source42"/"source43") as historical text; only runtime paths changed, and the current side is the verified source44 copy.',
    'The package verifier and native probe are author tools re-executed on this review\'s copy; content equality with root evidence is not independent reconstruction. Four TS normalization-map negatives are executed; the Rust map negative and the partial and/or/not helper are unexercised; count/all are unimplemented; two-binding qualification is incomplete.',
    'Byte-identical owners outside the provider change (query projection, composition section 7, policy-derivation3, enumeration, identity digest scope) rely on this origin\'s named source43 assessments and were not re-read this charter.',
    'No grade, activation, application, readiness, implementation authorization or product qualification is granted.',
]
