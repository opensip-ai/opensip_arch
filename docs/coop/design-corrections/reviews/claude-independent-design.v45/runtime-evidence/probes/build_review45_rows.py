# Executed by build_review45.py in its own globals (exec). The 107 individually reasoned rows with current owners and
# consequences, the single TCB-SCOPE-01 object, retained obligations, authority and limitations. Flags are always false.

N, I = 'new-45', 'unchanged-44-basis'
BASIS_RULE = ('unchanged-44-basis: the named governing owner bytes (unchanged44GoverningOwners) are byte-identical 44->45, and the conclusion rests on that identity plus this origin\'s named source44 row assessment, quoted in unchanged44Basis. '
              'Re-executed suites and ported probes are corroboration only. new-45: the conclusion rests on a source45 read, diff, probe or measurement newly performed under this charter, including rows whose owners are unchanged but whose governing law, closed-world consumer or trust account is touched by the source45 correction. '
              'Every row carries its own current text, current owner and consequence. No row is carried forward in bulk, and no grade is assigned.')
V44ROWS = {r['id']: r for k in ('fDispositions', 'evaluationResidualDispositions', 'arDispositions', 'fwDispositions', 'inheritedResidualDispositions', 'scopedReviewOwnerDispositions') for r in V44[k]}
TCB_DEPS = ['RES-EP13-02', 'RES-EP13-04', 'RES-EP13-12', 'RES-EP13-13', 'RES-EP13-16', 'RES-EP13-18', 'IR-EP13-NB-01', 'IR-EP13-NB-03', 'IR-EP13-NB-04', 'AX6', 'AX9', 'MD5', 'RX2c']


def base_row(rid, basis, disposition, assessment, owner, consequence, owners=None, **extra):
    prior = V44ROWS.get(rid)
    if prior is None:
        GAPS.append('no source44 row for ' + rid)
    if basis == I:
        if not owners:
            GAPS.append('unchanged basis without named governing owners: ' + rid)
        elif owners != 'outside-snapshot' and not all(U.get(o) for o in owners):
            GAPS.append('unchanged basis claimed for a changed owner: %s %s' % (rid, {o: U.get(o) for o in owners}))
    r = {'id': rid, 'prior44Disposition': prior['disposition'] if prior else None, 'prior44AssessmentBasis': prior['assessmentBasis'] if prior else None,
         'disposition': disposition, 'assessmentBasis': basis, 'unchanged44Basis': (prior['currentAssessment'] if (prior and basis == I) else None),
         'unchanged44GoverningOwners': (owners if basis == I else None), 'currentAssessment': assessment, 'currentOwner': owner, 'consequence': consequence}
    r.update(extra)
    r.update(appliedByThisReview=False, finalApplicationOutcomeGranted=False)
    return r


RESOWN = 'evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review'
F_ROWS = []
for i in range(1, 15):
    rid = 'F-%02d' % i
    st = V44ROWS[rid]['priorRootStanding']
    F_ROWS.append(base_row(rid, I, 'CARRIED-NOT-REGRADED',
                           '%s: prior root standing %s (root-independent36-completion-assessment.v1) carried without regrade on source45. The F record lives outside the frozen snapshot, and none of the 15 source44->45 delta files is an F record.' % (rid, st),
                           'root custody of the F record (outside the frozen snapshot)', 'No source45 change; remains carried without regrade and is not source45 acceptance.', owners='outside-snapshot', priorRootStanding=st))

RP = lambda k: PBY[k]['result']['rows']
REPLAY = ['evaluator_replay_model.v3.py', 'identity-model.v3.py']
RES_TEXT = {
    'RES-EP13-01': (I, 'Plan and derivation joins stay inside complete replay on byte-identical owners 44->45; the full-replay child equals root and this origin\'s source44 receipt, and the 17 package RunIds are unchanged.', 'Grade PENDING; residual retained.', REPLAY + ['identity-schemas.v3.json']),
    'RES-EP13-02': (N, 'Depends on TCB-SCOPE-01. The pre-analysis conversion still takes the host\'s planned stages as a trusted input, now with a published closedWorld record instead of a helper result (re-execution identical). Capture stays a host observation (ADV42-01 re-measured). No provider-authored field reaches the minted record.', 'Grade PENDING; reopens with TCB-SCOPE-01 only.', None),
    'RES-EP13-03': (I, 'Admission contract and residual ledger byte-identical 44->45; the finite historical measurement is unchanged on source45.', 'Grade PENDING; finite historical measurement unchanged.', ['admission-and-qualification.md', 'evaluation-residual-dispositions.proposed.json']),
    'RES-EP13-04': (N, 'Depends on TCB-SCOPE-01. Closed input admission is unchanged: the provider-startup $defs and registered bundle are unchanged, the host-minted closedWorld is a complete closed ClosedWorldV2 value admitted under the registered schema, and no open member is introduced.', 'Grade PENDING; reopens with TCB-SCOPE-01 only.', None),
    'RES-EP13-05': (N, 'The frozen subject was verified outside every author instrument: formal45 manifest 8b4efbb0..., archive 9536ebe3..., all 12,920 members by hash and length (738,157,930 -> 738,315,211 bytes), parent44 e873c8db... (12,919 members), the declared chain, the exact 14/1/0 delta and all 6,264 pin entries.', 'Grade PENDING.', None),
    'RES-EP13-06': (N, 'canonical.py stays outside the delta (%s). The published record\'s canonical bytes and the minted entries\' canonical bytes were recomputed with this review\'s own serializer, and they equal the foundation canonical form and the source44 entries.' % U['canonical.py'], 'Grade PENDING.', None),
    'RES-EP13-07': (I, 'Seal and replay owners byte-identical 44->45; the analysis-seal child equals root and this origin\'s source44 receipt on source45.', 'Grade PENDING.', REPLAY),
    'RES-EP13-08': (I, 'A bounded historical measurement. Source45 publishes one fixed conversion record and claims no proof over all PlanIntents, repositories or providers.', 'Grade PENDING.', ['evaluation-residual-dispositions.proposed.json']),
    'RES-EP13-09': (N, 'Provenance stays distinct from correctness: the published record keeps coverage unknown, exportsClosed unknown and deadCodeRepairEligible false, and the workflows repair gate cannot turn a pre-analysis conversion into repair eligibility (CH45-CONSUMER-IMPACT).', 'Grade PENDING.', None),
    'RES-EP13-10': (N, 'Author self-counters did not decide this review. The checker\'s three new bindings and the two case expectation additions are reference self-consistency. The decisive evidence is this review\'s derivation from section 4.5 and the registered schema, its byte and identity comparison against source44, and its mutation discriminators (P45-CLOSED-WORLD %d rows, P45-CHECKER-BINDING %d rows).' % (RP('P45-CLOSED-WORLD'), RP('P45-CHECKER-BINDING')), 'Grade PENDING.', None),
    'RES-EP13-11': (N, 'Failures stay recorded by cause: no probe attempt failed this charter. Two broad glob listings timed out and returned nothing, and one shell listing was denied by the harness; both were replaced by exact-path reads. Prior charters\' failed attempts stay in their own receipts.', 'Grade PENDING.', None),
    'RES-EP13-12': (N, 'Depends on TCB-SCOPE-01. No sole Python guard enters product authority. The checker\'s closed-world bindings are reference consistency checks, and the case expectations pin the minted entries; a product host must mint the published record as normative law, and nothing here executes that product obligation.', 'Grade PENDING; reopens with TCB-SCOPE-01 only.', None),
    'RES-EP13-13': (N, 'Depends on TCB-SCOPE-01. The discriminators loaded owner modules from the verified source45 and source44 copies in their own processes, and the checker mutations ran only on a disposable scratch copy; every verified copy was re-verified unchanged afterwards.', 'Grade PENDING; reopens with TCB-SCOPE-01 only.', None),
    'RES-EP13-14': (I, 'The differential census is not used as an oracle on source45; no delta file is a census owner.', 'Grade PENDING.', ['evaluation-residual-dispositions.proposed.json', 'current-source-map.proposed.md']),
    'RES-EP13-15': (I, 'The C-2 v4 self-census is not elevated; enumeration owners are byte-identical 44->45 and their 54 cases equal this origin\'s source44 receipt modulo paths.', 'Grade PENDING.', ['enumeration-contract.v1.md', 'enumeration_model.v1.py', 'enumeration-plan.schema.v1.json', 'check-enumeration.v1.py']),
    'RES-EP13-16': (I, 'Depends on TCB-SCOPE-01. Producer flags cannot bypass replay: execution-inputs owners are byte-identical 44->45 and the 95 cases equal this origin\'s source44 receipt modulo paths.', 'Grade PENDING; reopens with TCB-SCOPE-01 only.', ['execution-inputs-contract.v1.md', 'execution_inputs_model.v1.py', 'execution-inputs.schema.v1.json']),
    'RES-EP13-17': (N, 'Text-only disclosures remain text-only. The section 9.7 statement that the fixed record proves no absence of dynamic loading or dispatch is a disclosure paired with a non-enabling value, a checker binding and case pins; it is not a guarantee about repositories.', 'Grade PENDING.', None),
    'RES-EP13-18': (N, 'Depends on TCB-SCOPE-01. Native discovery and custody code is unchanged: the model delta is confined to the conversion closedWorld line and a comment. Marker observations stay trusted, and ported native (%d rows) and custody (%d rows) observations are identical to source44.' % (PORTED_EQUAL['P45-PORTED-NATIVE']['rows'], PORTED_EQUAL['P45-PORTED-CUSTODY']['rows']), 'Grade PENDING; reopens with TCB-SCOPE-01 only.', None),
    'RES-EP13-19': (N, 'Substantive review on source45: independent law derivation, scope and both-language challenge, committed-byte and identity comparison against source44, consumer impact, planning v13 binding, and both retained advisories reassessed with current reasoning.', 'Grade PENDING.', None),
    'IR-EP13-NB-01': (N, 'Depends on TCB-SCOPE-01. Every source45 probe ran in-process with owner modules; the in-process law-member mutation shows loaded law is mutable in-process, which is exactly the same-process boundary this assumption excludes. Containment is not claimed.', 'Grade PENDING; reopens with TCB-SCOPE-01 only.', None),
    'IR-EP13-NB-02': (N, 'No name scan decides a product route. The checker locates the section 9.7 record by heading and code fence in reference prose (OBS45-08), a documentation consistency check with no product route.', 'Grade PENDING.', None),
    'IR-EP13-NB-03': (N, 'Depends on TCB-SCOPE-01. Loaded owner instances stay reachable in-process: the conversion reads STARTUP.LAW by deep copy, so a same-process writer could alter a later conversion before copy, as the reviewer\'s mutation showed. That is outside the threat model, not a provider path.', 'Grade PENDING; reopens with TCB-SCOPE-01 only.', None),
    'IR-EP13-NB-04': (N, 'Depends on TCB-SCOPE-01; one TCB account, assessed once on source45, covers all thirteen rows.', 'Grade PENDING; reopens with TCB-SCOPE-01 only.', None),
    'IR-EP13-NB-05': (N, 'Contradictory or under-specified prose still needed substantive review. Source44 named an unpublished helper for a normative record; source45 publishes the record and binds prose, law and helper, and clarifies three generic historical-batch statements (one editorial duplication).', 'Grade PENDING.', None),
    'IR-EP13-NB-06': (I, 'Historical attacker cost preserved as history; no source45 file addresses it.', 'Grade PENDING.', ['evaluation-residual-dispositions.proposed.json']),
    'IR-EP13-NB-07': (I, 'The original environment is preserved; this review names /tmp/opensip-architecture-review-env/bin/python -I -B and verifies all 6,264 pins on source45.', 'Grade PENDING.', ['evaluation-residual-dispositions.proposed.json']),
    'AX6': (N, 'Depends on TCB-SCOPE-01. None of the 14 changed files or the added v13 layer claims same-process route-region protection (all diffs read; native-cases compared structurally).', 'Grade PENDING; reopens with TCB-SCOPE-01 only.', None),
    'AX9': (N, 'Depends on TCB-SCOPE-01. The fixed closedWorld record is typed host-minted data under a trusted host, not a protection mechanism.', 'Grade PENDING; reopens with TCB-SCOPE-01 only.', None),
    'MD5': (N, 'Depends on TCB-SCOPE-01. Source45 adds no Python-containment mechanism (delta read).', 'Grade PENDING; reopens with TCB-SCOPE-01 only.', None),
    'RX2c': (I, 'Depends on TCB-SCOPE-01. Complete replay and full-Run closure remain reproducibility evidence, not containment; replay owners byte-identical 44->45.', 'Grade PENDING; reopens with TCB-SCOPE-01 only.', REPLAY),
}
RES_ROWS = []
for rid in ['RES-EP13-%02d' % i for i in range(1, 20)] + ['IR-EP13-NB-%02d' % i for i in range(1, 8)] + ['AX6', 'AX9', 'MD5', 'RX2c']:
    basis, text, cons, owners = RES_TEXT[rid]
    p = V44ROWS[rid]
    dep = 'TCB-SCOPE-01' if rid in TCB_DEPS else None
    if (p.get('sharedDependency') or None) != dep:
        GAPS.append('shared dependency differs from source44 for ' + rid)
    RES_ROWS.append(base_row(rid, basis, 'ASSESSED-CONSISTENT-GRADE-PENDING', text + ' Historical limitation preserved; no historical guard claimed repaired.', RESOWN, cons, owners=owners,
                             proposedDisposition=p['proposedDisposition'], authorGrade='PENDING', sharedDependency=dep, residualRetained=True))

AR_TEXT = {
    'AR-01': (I, 'NO-NEW-ISSUE', 'Admission section 1 byte-identical 44->45; ported query carriers (%d rows) identical to source44.' % PORTED_EQUAL['P45-PORTED-QUERY']['rows'], 'No change required.', ['admission-and-qualification.md']),
    'AR-02': (I, 'NO-NEW-ISSUE', 'Admission sections 2-4 and gate ledger byte-identical 44->45: %d gates, none qualified.' % len(GATES), 'All gates stay unperformed.', ['admission-and-qualification.md', 'qualification-gates.proposed.json']),
    'AR-03': (I, 'NO-NEW-ISSUE', 'Security discovery text byte-identical 44->45; ported custody rows identical to source44.', 'No change required.', ['security-and-lifecycle.md']),
    'AR-04': (I, 'NO-NEW-ISSUE', 'Security trust time byte-identical 44->45; the security group stdout equals root, codex and this origin\'s source44 receipt.', 'No change required.', ['security-and-lifecycle.md']),
    'AR-05': (I, 'NO-NEW-ISSUE', 'Security root chain and revocation byte-identical 44->45; untouched by the delta.', 'No change required.', ['security-and-lifecycle.md']),
    'AR-06': (I, 'NO-NEW-ISSUE', 'Platform admission and carrier DDL byte-identical 44->45; ported read-only carrier rows (%d) identical.' % PORTED_EQUAL['P45-PORTED-CARRIER']['rows'], 'No change required.', ['security-and-lifecycle.md', 'carrier-dispatch.v3.json']),
    'AR-07': (N, 'NO-NEW-ISSUE (ADVISORY ADV44-01 RETAINED)', 'Native section 9 changed only in 9.7: the pre-analysis host conversion now publishes its complete closedWorld record (3241-3261), with the machine owner in the startup law. Section 9.7 was read completely, and the record was derived from law, challenged for scope and both-language applicability, and shown byte-reproducible (CH45-CLOSED-WORLD-LAW, CH45-BOTH-LANGUAGES-AND-COMMITTED-BYTES). Sections 3 and 5 are unchanged; native group 477/477.', 'No change required; the planning advisory stays optional.', None),
    'AR-08': (I, 'NO-NEW-ISSUE', 'Invocation and repair text byte-identical 44->45; ported repair:2 rows identical.', 'No change required.', ['workflows-and-surfaces.md', 'repair_closed_world_selection.v1.py']),
    'AR-09': (I, 'NO-NEW-ISSUE (ADVISORY ADV42-01 RETAINED)', 'identity-and-evidence and identity owners byte-identical 44->45; coverage2 identities of the conversion entries equal source44; S40-01 remains resolved and ADV42-01 retained on re-measured values.', 'No change required; the advisory is optional.', ['identity-and-evidence.md', 'identity-model.v3.py', 'identity-schemas.v3.json']),
    'AR-10': (I, 'NO-NEW-ISSUE', 'Baseline and comparison text byte-identical 44->45; ported comparison-knowledge rows identical.', 'No change required.', ['workflows-and-surfaces.md']),
    'AR-11': (I, 'NO-NEW-ISSUE', 'Comparison and import text byte-identical 44->45; the execution-inputs child equals root after removing path fields only.', 'No change required.', ['workflows-and-surfaces.md']),
    'AR-12': (N, 'NO-NEW-ISSUE', 'Native section 4 text is unchanged (outside the only hunk), and section 4.5\'s ClosedWorldV2 law is now directly instantiated by the section 9.7 record. The derivation shows the record honours every 4.5 ingredient rule and cannot claim closed exports or repair eligibility; the atoms child equals root and source44.', 'No change required.', None),
    'AR-13': (N, 'NO-NEW-ISSUE', 'Native sections 1, 2, 6 and 8 lie outside the only source45 hunk (complete diff read); enumeration cases equal source44 modulo paths and the nine native-v2 membership probes equal root.', 'No change required.', None),
    'AR-14': (I, 'NO-NEW-ISSUE', 'Stage transition and lease bytes unchanged 44->45; no delta file is a lifecycle owner.', 'No change required.', ['security-and-lifecycle.md']),
    'AR-15': (I, 'NO-NEW-ISSUE', 'Contract index README and D-372 application text byte-identical 44->45.', 'No change required.', ['README.md']),
    'AR-16': (N, 'NO-NEW-ISSUE', 'workflows-and-surfaces is byte-identical, but its repair closed-world gate and display summary consume the record source45 publishes: the gate stays refused for conversion-only selections, and the non-authoritative summary may display nonliteralLoading none (OBS45-04). No D9 code is added, and the D9 successor stays carried.', 'No change required.', None),
}
AR_ROWS = []
for i in range(1, 17):
    rid = 'AR-%02d' % i
    basis, disp, text, cons, owners = AR_TEXT[rid]
    p = V44ROWS[rid]
    c = p['contract']
    unchanged = same(S44, S45, c)
    if basis == I and not unchanged:
        GAPS.append('unchanged basis claimed for a changed contract: ' + rid)
    AR_ROWS.append(base_row(rid, basis, disp, text, c + ' (' + p['selector'] + ')', cons, owners=owners, contract=c, selector=p['selector'], statusRecorded=p['statusRecorded'],
                            contractSha256=sha(S45 + '/' + c), contractUnchanged44to45=unchanged))

FWO = ['current-source-map.proposed.md', 'repository-file-inventory.v1.json']
FW_TEXT = {
    'FW-01': (I, 'discovery.rs binding construction obligation unchanged on source45; owner map and inventory byte-identical 44->45.', 'Not executed.'),
    'FW-02': (I, 'review.rs review-brief carriers unchanged on source45; ported carriers identical.', 'Not executed.'),
    'FW-03': (N, 'analysis.rs composes provider work, admission and evaluation (inventory :695). For the pre-analysis native-context mismatch its host conversion must now mint exactly the published hostConversionClosedWorld for both languages, not a locally computed record. It keeps the ADV42-01 verification obligation. Owner map and inventory byte-identical 44->45.', 'Implementation obligations retained; not executed.'),
    'FW-04': (I, 'imports.rs unchanged on source45; typed-null targetUniverse account stands.', 'Not executed.'),
    'FW-05': (I, 'comparison.rs presence knowledge unchanged on source45; ported comparison rows identical.', 'Not executed.'),
    'FW-06': (I, 'finalization.rs delivery laws unchanged on source45; commit-inventory recipe re-derived identically.', 'Not executed.'),
    'FW-07': (I, 'invocation.rs argvDigest unchanged on source45.', 'Not executed.'),
    'FW-08': (I, 'outcomes.rs detail allowlist unchanged and sufficient on source45; no detail added by the closed-world correction.', 'Not executed.'),
    'FW-09': (I, 'review.rs candidates/inspect carriers unchanged on source45; ported carriers identical.', 'Not executed.'),
    'FW-10': (I, 'repair.rs repair:2 constructor unchanged on source45; ported repair rows identical.', 'Not executed.'),
    'FW-11': (I, 'comparison.rs baseline.show unchanged on source45.', 'Not executed.'),
    'FW-12': (I, 'review.rs produce-brief host-only unchanged on source45.', 'Not executed.'),
    'FW-13': (I, 'configuration.rs policy-test admission routes unchanged on source45; ported policy rows identical.', 'Not executed.'),
    'FW-14': (I, 'discovery.rs recommend units unchanged on source45.', 'Not executed.'),
    'FW-15': (I, 'policy.rs show/test unchanged on source45; the policy-derivation child equals source44.', 'Not executed.'),
}
FW_ROWS = []
for i in range(1, 16):
    rid = 'FW-%02d' % i
    basis, text, cons = FW_TEXT[rid]
    p = V44ROWS[rid]
    # source44 FW rows carry the owner modules inside currentOwner ("module[, module] (milestone)"), not as a separate key
    FW_ROWS.append(base_row(rid, basis, 'OWNER-ROUTING-ASSESSED-NOT-EXECUTED', text, p['currentOwner'], cons, owners=FWO,
                            owner_modules=p['currentOwner'].rsplit(' (', 1)[0].split(', '), milestone=p['milestone']))

IRU = U['inherited-residuals.proposed.md']
DROWN = 'successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md'
RO = ['inherited-residuals.proposed.md', 'current-source-map.proposed.md']
DR_TEXT = {
    'DR-001': (I, 'current-source-map and residual ledgers byte-identical 44->45 on source45.', 'Condition-1 obligation retained.', RO + ['evaluation-residual-dispositions.proposed.json']),
    'DR-002': (I, 'ExecutionInputsV1 view attribution and exact selection remain published on byte-identical owners 44->45; S40-01 remains resolved.', 'Condition-1 obligation retained.', RO + ['execution-inputs-contract.v1.md', 'execution_inputs_model.v1.py']),
    'DR-003': (I, 'Read-only carrier routes unchanged 44->45; 54 recovery cases unexecuted on source45.', 'Condition-1 obligation retained; release demonstration still required.', RO + ['commit-recovery-readonly.v3.md', 'carrier-dispatch.v3.json']),
    'DR-004': (I, 'Native binding construction consumed by enumeration unchanged; enumeration owners byte-identical 44->45.', 'Condition-1 obligation retained.', RO + ['enumeration-contract.v1.md', 'enumeration_model.v1.py']),
    'DR-005': (N, 'Custody reference groups pass on source45; the native model change is confined to the conversion closedWorld, and ported custody rows are identical. Native carrier qualification is still required.', 'Condition-1 obligation retained.', None),
    'DR-006': (I, 'Descriptor graph unchanged 44->45; the full-replay child equals root and source44.', 'Condition-1 obligation retained.', RO + ['evaluator_replay_model.v3.py', 'identity-schemas.v3.json']),
    'DR-007': (I, 'The D9 published successor artifact remains a carried implementation-unit obligation; public-detail registry and workflows contract byte-identical 44->45.', 'Mandatory future implementation-unit obligation; not a new blocker.', RO + ['public-detail-registry.v1.json', 'workflows-and-surfaces.md']),
    'DR-008': (I, 'The applied retention posture is unchanged 44->45 on source45.', 'Condition-1 obligation retained.', RO + ['security-and-lifecycle.md', 'identity-and-evidence.md']),
    'DR-009': (I, 'The host capture stays outside the sealed Run; execution-inputs model and fixture byte-identical 44->45.', 'Condition-1 obligation retained.', RO + ['execution_inputs_model.v1.py', 'execution_inputs_fixture.v3.py']),
    'DR-010': (I, 'Bounded first-party composition unchanged 44->45 on source45.', 'Condition-1 obligation retained.', RO + ['evaluator-composition-contract.v3.md']),
    'DR-011': (I, 'The blind implementer litmus follows final integration and is not closed by this nonblind source45 review.', 'Condition-1 obligation retained.', RO),
    'DR-011-R01': (I, 'Fact-plane successor schemas unchanged: fact-batch v3 and occupancy companion byte-identical 44->45.', 'Retained.', RO + ['fact-batch.schema.v3.json', 'occupancy-companion.schema.v1.json']),
    'DR-011-R02': (I, 'Imperative plugins stay outside D-371 on source45.', 'Retained.', RO + ['admission-and-qualification.md']),
    'DR-011-R03': (I, 'plan2 EnumerationPlanV1 binding joins unchanged 44->45.', 'Retained.', RO + ['enumeration-plan.schema.v1.json', 'enumeration_model.v1.py']),
    'DR-011-R04': (I, 'carrierFormat mapping unchanged 44->45 on source45.', 'Retained.', RO + ['carrier-dispatch.v3.json']),
    'DR-011-R05': (N, 'Rust protocol major 3 and TypeScript major 2 unchanged; source45 changes only the startup law annotation for the pre-analysis conversion, with $defs unchanged (measured).', 'Retained.', None),
    'DR-011-R06': (I, 'Typed close_run outcomes through the graph query unchanged; query owners byte-identical 44->45.', 'Retained.', RO + ['query_projection_model.v3.py', 'query-projection-contract.v3.md']),
    'DR-011-R07': (I, 'Query retained-availability routes and partial disclosure unchanged; query owners byte-identical 44->45.', 'Retained.', RO + ['query_projection_model.v3.py', 'query-projection-contract.v3.md']),
    'DR-011-R08': (I, 'D9 successor remains carried on source45 (DR-007).', 'Mandatory future implementation-unit obligation.', RO + ['public-detail-registry.v1.json']),
    'DR-011-R09': (N, 'Semantic identity still excludes attempt identity: the conversion entries\' coverage2 identities equal source44, the 17 package export stores are byte-equal to package21, and the measured RunIds equal source44.', 'Retained.', None),
    'DR-011-R10': (I, 'OPEN: this nonblind source45 review cannot close the fresh blind implementer litmus.', 'Retained open.', RO),
    'DR-011-R11': (I, 'Real platform durability unmeasured on source45; 54 cases not executed.', 'Retained.', RO + ['commit-recovery-readonly.v3.md']),
    'DR-011-R12': (N, 'Depends on TCB-SCOPE-01, assessed once on source45.', 'Retained; reopens with TCB-SCOPE-01 only.', None),
    'DR-011-R13': (N, 'Source45 adds an annotation-level law member and changes no registered schema document, schema $defs, identity record or schema major; the registered bundle digest is unchanged, consistent with the composition profile.', 'Retained.', None),
    'DR-011-R14': (I, 'CFG-6/TM unchanged 44->45 on source45.', 'Retained.', RO),
    'DR-011-R15': (N, 'Trusted request context stays host-only: the conversion\'s planned stages and the published closedWorld are host inputs and host law, and none is provider-authored.', 'Retained.', None),
    'DR-011-R16': (I, 'No executable report-hook admission; prototype-report-inventory and admission section 5 unchanged 44->45.', 'Retained.', RO + ['prototype-report-inventory.md', 'admission-and-qualification.md']),
}
DR_ROWS = []
for rid in ['DR-%03d' % i for i in range(1, 12)] + ['DR-011-R%02d' % i for i in range(1, 17)]:
    basis, text, cons, owners = DR_TEXT[rid]
    DR_ROWS.append(base_row(rid, basis, 'CONDITION-1-OBLIGATION-RETAINED-ASSESSED',
                            text + ' Successor routing in inherited-residuals.proposed.md (byte-identical 44->45: %s) is consistent with source45.' % IRU, DROWN, cons, owners=owners))

REGU = U['08-decision-and-readiness-register.md']
SCOPED_TEXT = {
    'DR-201': (N, 'Semantic-correctness owner row: the published pre-analysis closedWorld law, its consumer effect and both retained advisories fall in its area.', None),
    'DR-202': (I, 'Delivery/operations owner row: recovery, repair and loader TCB unchanged 44->45.', ['08-decision-and-readiness-register.md', 'commit-recovery-readonly.v3.md']),
    'DR-203': (I, 'Prototype-lessons owner row (PARTIAL-SCOPED): no source45 delta file is the prototype reference.', ['08-decision-and-readiness-register.md', 'prototype-report-inventory.md']),
    'DR-204': (N, 'V1/coop invariant owner row: all 6,264 pins verified; layer v13 binds the two changed normative inputs and preserves v8-v12 byte-identically; ADV44-01 retained.', None),
    'DR-205': (N, 'Small-core/components owner row: TCB-SCOPE-01 remains coherent on source45; the correction is host law, not a component or trust change.', None),
}
SCOPED_ROWS = [base_row(rid, SCOPED_TEXT[rid][0], 'ROUTING-ASSESSED-ONLY-NOT-APPLIED', SCOPED_TEXT[rid][1] + ' Register 08 byte-identical 44->45 (%s).' % REGU,
                        'register 08 condition-3 review owner row ' + rid, 'Input to the integrated review; routing only, not applied.', owners=SCOPED_TEXT[rid][2])
               for rid in ('DR-201', 'DR-202', 'DR-203', 'DR-204', 'DR-205')]

V44TCB = V44['sharedAssumptionTCBSCOPE01']
TCB = {
    'id': 'TCB-SCOPE-01', 'assessedOnceAsOneAssumption': True,
    'assumption': 'Authenticated selected in-process host/evaluator code is trusted; providers and inert inputs are untrusted; adversarial code sharing the process is outside the product threat model.',
    'consequence': 'Rejecting or changing the assumption reopens the thirteen dependent rows jointly, not as thirteen independent proofs. It repairs no historical attack and qualifies no containment. All thirteen author grades stay PENDING.',
    'dependentRows': TCB_DEPS, 'dependentRowCount': len(TCB_DEPS),
    'currentAssessment': 'NOT REJECTED: coherent as a scope selection on source45 and unqualified; the source45 correction publishes host law and adds no trust.',
    'substantiveCurrentAssessment': [
        'Coherent: admission section 5 (byte-identical 44->45: %s) and prototype-report-inventory (byte-identical: %s) still admit no untrusted native/WASM, imperative contributions or executable report hooks.' % (U['admission-and-qualification.md'], U['prototype-report-inventory.md']),
        'Providers stay untrusted: the pre-analysis closedWorld is host-minted from published law, and no provider-authored member reaches it; the provider-side startup admissions are unchanged (re-execution identical).',
        'Host inputs and loaded law stay TCB: planned stages remain trusted host inputs, and the in-process law member is mutable by same-process code (measured), which this assumption places outside the threat model.',
        'View producer closures must still be Plan-selected providers at Run closure (CLOSURE_FIELD_KIND re-measured on source45).',
        'Unqualified: it rests on the authenticated closure/TCB inventory and provider process boundaries; all %d gates are unperformed (qualified=true %d).' % (len(GATES), gates_true),
    ],
    'reviewerPosition': 'NOT REJECTED', 'standing': 'ASSESSED-COHERENT-UNQUALIFIED-ON-SOURCE45; final application adjudication not granted',
    'adjudicationOwner': 'separate final application review, by a NEW different actual Claude origin (not this origin %s and not any author, design or blind origin)' % ORIGIN,
    'prior44Standing': V44TCB['standing'],
}
for rid in TCB_DEPS:
    if next(r for r in RES_ROWS if r['id'] == rid)['sharedDependency'] != 'TCB-SCOPE-01':
        GAPS.append('TCB dependent row lacks shared dependency: ' + rid)

RETAINED = {
    'residuals': len(RES_ROWS), 'authorGradesPending': sum(1 for r in RES_ROWS if r['authorGrade'] == 'PENDING'),
    'condition2Obligations': 28 if cond2_ok else None,
    'condition2Source': 'docs/v2/architecture/08-decision-and-readiness-register.md:385-391 (byte-identical 44->45: %s)' % REGU,
    'productQualificationGates': {'count': len(GATES), 'qualifiedTrue': gates_true, 'standing': 'UNPERFORMED'},
    'plannedRecoveryCases': {'count': PC['recoveryCases'], 'notExecuted': PC['recoveryCasesNotExecuted'], 'standing': 'UNPERFORMED'},
    'condition5': 'NOT MET (not a design defect)',
    'd9PublishedSuccessor': 'Mandatory future implementation-unit obligation (DR-007 / DR-011-R08); not a newly invented design blocker.',
    'adv4201ImplementationVerification': 'crates/host/src/analysis.rs verification that no returned view is listed on another producer\'s complete receipt (root routing; not executed).',
    'adv4401PlanningBinding': 'Optional planning-owner improvement: bind protocol3-transitions.v1.json and fact-batch.schema.v3.json in a future layer, or state their binding through the formal manifest (non-blocking).',
    'closedWorldHostImplementation': 'A product host must mint exactly the published hostConversionClosedWorld for pre-analysis provider-unavailable coverage in both languages (FW-03; not executed).',
    'providerImplementationObligations': 'Framing, worker processes, compilers, descriptor members beyond the reference joins, Cancel/Cancelled correlation and Rust Cancelled phase, stream and coverage commitments, and host user-interruption reduction remain owned by their inherited laws and are unqualified (section 9.7 reference scope; OBS45-10).',
    'gradeAndConditionOwner': 'All 30 evaluation grades and 28 condition-2 obligations belong to final application adjudication.',
    'finalApplication': 'Requires a NEW different actual Claude origin, not this origin (%s) and not any author, design or blind origin.' % ORIGIN,
    'acceptanceStanding': 'Source-level acceptance only; distinct from final application, readiness and product qualification.',
}
AUTHORITY = {'gradeGranted': False, 'activationGranted': False, 'implementationAuthorized': False, 'blindReconstructionClaimed': False,
             'freshOriginIndependenceClaimed': False, 'source44ReviewConclusionInherited': False, 'frozenInputsModified': False,
             'applicationOrReadinessGranted': False, 'productQualificationGranted': False, 'blindConsumerArtifactsOrOutcomesAccessed': False,
             'authorRuntimeHistoriesRead': False, 'historicalExportsRelabelled': False, 'runIdsReminted': False, 'productCommitPushOrActivation': False,
             'subagentsWebOrPrivateLogsUsed': False}
LIMITATIONS = [
    'Nonblind successor review by the origin that completed the source40, 42, 43 and 44 reviews; not fresh-origin independence. No author report was header-bound for source45; the charter\'s source-only correction rationale was treated as author statement and re-measured. No author runtime history, blind consumer artifact, export, helper, report or root blind outcome was read; review directories named for blind consumers or root corrections that were not header-bound were not opened.',
    'The law derivation separates members forced by section 4.5 from members fixed by the new section 9.7 publication; the latter are assessed for lawfulness, scope and non-enabling effect, not derived as unique.',
    'Reference Python models over fixtures; no product code. The closed-world discriminator exercises the reference host conversion over trusted fixture host inputs; it is not complete retained Run replay and not a product host. No framing, worker, process or compiler is exercised. 32 gates and 54 recovery cases remain unperformed (condition 5 NOT MET).',
    'Whole-file claims are limited to fresh45Read and inheritedUnchanged44Read. native-evidence.md was read by range (4.3, 4.5, complete 9.7) plus its complete diff; the startup law object was read by range plus complete diff; native-cases was compared structurally, not read as a 57,096-line text diff.',
    'The source44 wire discriminator was not re-executed because its owners are byte-identical; its conclusions stand as named unchanged-44 basis. The startup discriminator was re-executed as corroboration only.',
    'The checker mutation probe regenerated the native pin ledger inside a disposable scratch copy so the targeted law checks could be reached; that scratch ledger is not a source artifact and no verified or frozen copy was modified.',
    'Ported probes keep their historical labels; only runtime paths changed, and the current side is the verified source45 copy.',
    'The package verifier and native probe are author tools re-executed on this review\'s copy; content equality with root evidence is not independent reconstruction. Four TS normalization-map negatives are executed; the Rust map negative and the partial and/or/not helper are unexercised; count/all are unimplemented; two-binding qualification is incomplete.',
    'Byte-identical owners outside the correction (query projection, composition, policy derivation, enumeration, identity, wire handshake) rely on this origin\'s named source44 assessments and were not re-read this charter.',
    'No grade, activation, application, readiness, implementation authorization or product qualification is granted.',
]
