# Executed by build_review44.py in its own globals (exec). Issues, observations, current dispositions of every prior finding,
# advisory and observation, charter item assessments and the named scope basis. Every claimed measurement is re-checked here.

def pick(rows, case, label):
    row = rows.get(case)
    if row is None:
        GAPS.append('%s row missing: %s' % (label, case))
        return {}
    if not row['ok']:
        GAPS.append('%s row not ok: %s' % (label, case))
    return row['observed']


def pickp(rows, prefix, label):
    row = next((r for c, r in rows.items() if c.startswith(prefix)), None)
    if row is None:
        GAPS.append('%s row missing: %s' % (label, prefix))
        return {}
    if not row['ok']:
        GAPS.append('%s row not ok: %s' % (label, prefix))
    return row['observed']


def grp(rows, prefix, label):
    sel = {c: r for c, r in rows.items() if c.startswith(prefix)}
    if not sel:
        GAPS.append('%s has no rows for prefix %s' % (label, prefix))
    if any(not r['ok'] for r in sel.values()):
        GAPS.append('%s rows not ok under prefix %s' % (label, prefix))
    return {'rows': len(sel), 'allOk': all(r['ok'] for r in sel.values()), 'cases': sorted(sel)}


def w(case):
    return pick(WR, case, 'wire44')


def s(case):
    return pick(SR, case, 'startup44')


def wire_refusals(prefixes):
    out = {}
    for c, r in sorted(WR.items()):
        o = r['observed']
        if c.startswith(prefixes) and isinstance(o, dict) and o.get('admitted') is False:
            out[c] = [o.get('key'), (o.get('detail') or '')[:70]]
    return out


def startup_refusals(prefixes):
    out = {}
    for c, r in sorted(SR.items()):
        o = r['observed']
        if c.startswith(prefixes) and isinstance(o, dict) and 'finalPhase' in o:
            ref = o.get('refusal') or {}
            out[c] = [o['finalPhase'], o.get('terminalKind'), ref.get('key'), ref.get('detailHead'), (o.get('trace') or [None])[-1]]
    return out


def lines_of(root, p):
    return open(root + '/' + p, encoding='utf-8').read().splitlines()


MUST, SHOULD = [], []
V43ITEMS = {i['id']: i for i in V43['itemDispositions']}
WIRE_ROWS, STARTUP_ROWS = len(WR), len(SR)
STARTUP_CHECKS = sum(1 for r in SR.values() if r['kind'] == 'check')

# ------------------------------------------------------------------------------------------------ ADV42-01 (retained)
J1, J2, J3 = pickp(CJ, 'J1-', 'capture-joins-on44'), pickp(CJ, 'J2-', 'capture-joins-on44'), pickp(CJ, 'J3-', 'capture-joins-on44')
adv_measured_ok = (J1.get('admission', {}).get('refusals') == ['EXECUTION_INPUTS_PLAN_JOIN'] and J2.get('admission', {}).get('result') == 'ADMIT' and J3.get('admission', {}).get('result') == 'ADMIT'
                   and 'CLOSURE_FIELD_KIND' in str(J2.get('fullRun')) and 'CLOSURE_FIELD_KIND' in str(J3.get('fullRun'))
                   and not PORTED_EQUAL['P44-PORTED-CAPTURE-JOINS']['observedDifferFromSource43'])
EIC, EIM = FD + 'execution-inputs-contract.v1.md', FD + 'execution_inputs_model.v1.py'
c43, c44, m43, m44 = lines_of(S43, EIC), lines_of(S44, EIC), lines_of(S43, EIM), lines_of(S44, EIM)
SELECTOR_LINES = {
    'execution-inputs-contract.v1.md:12': c43[11] == c44[11],
    'execution-inputs-contract.v1.md:51': c43[50] == c44[50],
    'execution-inputs-contract.v1.md:53': c43[52] == c44[52],
    'execution-inputs-contract.v1.md:299': c43[298] == c44[298],
    'execution_inputs_model.v1.py:1057-1093 (source44 1058-1094)': m43[1056:1093] == m44[1057:1094],
    'execution_inputs_model.v1.py:1132-1139 (source44 1133-1140)': m43[1131:1139] == m44[1132:1140],
    'execution_inputs_model.v1.py:1626-1640 (source44 1627-1641)': m43[1625:1640] == m44[1626:1641],
}
contract_diff_lines = [i + 1 for i, (a, b) in enumerate(zip(c43, c44)) if a != b]
model_shift_ok = len(m44) == len(m43) + 1 and m43[:108] == m44[:108] and m43[109:] == m44[110:]
adv_bytes = {k: U[k] for k in ('execution-inputs.schema.v1.json', 'execution_inputs_fixture.v3.py', 'identity-model.v3.py', 'identity-schemas.v3.json')}
if not (adv_measured_ok and all(SELECTOR_LINES.values()) and len(c43) == len(c44) and contract_diff_lines == [272, 290] and model_shift_ok and all(adv_bytes.values())):
    GAPS.append('ADV42-01 re-measurement, selector lines or owner-byte identity not as recorded')
V43ADV = next(a for a in V43['advisories'] if a['id'] == 'ADV42-01')
P3_43, P3_44 = J(S43 + '/' + NAT + 'protocol3-transitions.v1.json'), J(S44 + '/' + NAT + 'protocol3-transitions.v1.json')
p3_changed_keys = sorted(k for k in set(P3_43) | set(P3_44) if P3_43.get(k) != P3_44.get(k))
if p3_changed_keys != ['derivedObservations', 'rowPayloads', 'stateUpdates']:
    GAPS.append('protocol3 table change population differs: %s' % p3_changed_keys)
ADVISORIES = [{
    'id': 'ADV42-01', 'severity': 'ADVISORY', 'origin': 'source42 review (retained; not new in source44)', 'title': V43ADV['title'],
    'selectors': V43ADV['selectors'],
    'selectorOwnerState43to44': {'executionInputsContract': 'changed only at :272 and :290 (historical per-language FactBatch naming); the selector lines are line-stable and byte-identical',
                                 'executionInputsModel': 'changed only in the note string at :109-110 (one added line); every later line shifts by one and the selector ranges are byte-identical',
                                 'selectorLinesIdentical': SELECTOR_LINES, 'contractDifferingLines': contract_diff_lines, 'modelOnlyShiftedByOneLine': model_shift_ok, 'otherOwnersByteIdentical': adv_bytes},
    'measuredOnSource44': {'sameProviderForeignPlanId': J1, 'foreignProducerSamePlan': J2, 'foreignProducerForeignPlan': J3,
                           'observedEqualToSource43Receipt': not PORTED_EQUAL['P44-PORTED-CAPTURE-JOINS']['observedDifferFromSource43']},
    'detail': V43ADV['detail'],
    'currentStanding': 'RETAINED ADVISORY, NON-BLOCKING. Root routing as an implementation verification obligation for crates/host/src/analysis.rs is independently assessed as correctly scoped; it is not a containment proof and no control was executed for it.',
    'standingAssessment': ('Source44 touches two selector owners only outside the advisory: the execution-inputs contract at :272 and :290 and the model note at :109-110. Every selector line is byte-identical (%s), and identity-model/identity-schemas, the schema and the fixture are byte-identical. '
                           'The ported measurement re-observes the source43 values exactly: J1 refuses EXECUTION_INPUTS_PLAN_JOIN; J2 and J3 admit at execution-inputs and close_run refuses them with CLOSURE_FIELD_KIND:view.producerClosure:provider. '
                           'The inventory names crates/host/src/analysis.rs (:695) as the service composing provider work, admission, evaluation and complete replay, which makes it the planned host capture. Contract section 8 (:299) already binds the builder to place each explicit returned view on the view stage whose producerClosure it carries, so the verification obligation tests existing law and invents none. '
                           'Source44\'s provider changes do not reach it: occupancy capture, the only capture path they touch, is still gated and bound by dispatch and receipts. Scope limits: no two-stage two-provider Plan was minted, execution-inputs admission still does not re-check receipt/view producer equality, and those contract options stay optional owner improvements. '
                           'No measured world admits a contradictory Run, and TCB-SCOPE-01 is unchanged, so nothing warrants escalation.') % json.dumps(SELECTOR_LINES),
    'consequence': V43ADV['consequence'],
    'disposition': 'ADVISORY, non-blocking; retained with owner routing (foundation execution-inputs owner for the optional contract clarifications; crates/host/src/analysis.rs implementation verification obligation at final application / implementation).',
    'owner': V43ADV['owner'],
    'receipts': ['receipts/probes/capture-joins-on44.json', 'claude-independent-design.v43/receipts/probes/capture-joins-on43.json (historical)']},
    {'id': 'ADV44-01', 'severity': 'ADVISORY', 'origin': 'new in source44 (this review)',
     'title': 'Planning layer v12 binds the new typescript-semantic order table but not the rust-semantic protocol3 transition table, whose normative OpenUniverse state-update text and published annotations changed in source44',
     'selectors': ['docs/v2/architecture/implementation-normative-inputs.v12.json (34 inputs: the 31 of v11 plus provider-handshake, provider-startup and typescript-protocol2-order; native-evidence.md updated; standing: "Exact normative/reference inputs consumed by implementation planning")',
                   'docs/coop/design-corrections/native/protocol3-transitions.v1.json:99 (stateUpdates: dependencyMode/preparedMode as host-derived observations) and :129-145 (derivedObservations, rowPayloads); standing "NORMATIVE and CLOSED"',
                   'docs/v2/contracts/product-v1/native-evidence.md section 9.2 (the Rust major-3 transition table) and section 9.7 :3193-3203 (derived modes)',
                   'docs/operations/check_implementation_planning.py:1-44, 255-292 (binding rule: every coverage source must be in the selected layer; no rule for other normative documents)',
                   'fact-batch.schema.v3.json ("CURRENT selected"; description, whenAbsent, commitments and wireProjection changed) and execution-inputs-contract.v1.md (changed wording) are likewise not layer inputs'],
     'measured': {'v12Inputs': PC['layerInputs']['12'], 'v12AddedVsV11': PC['v12AddedVsV11'], 'v12ChangedVsV11': PC['v12ChangedVsV11'],
                  'changedSelfDeclaredNormativeDeltaDocumentsNotBoundByV12': UNBOUND_NORMATIVE,
                  'boundByV11': {p: PC['deltaDocumentsNotBoundByV12'][p]['boundByV11'] for p in UNBOUND_NORMATIVE},
                  'protocol3TopLevelKeysChanged43to44': p3_changed_keys, 'protocol3RulesPhasesWildcardsUnchanged': all(P3_43[k] == P3_44[k] for k in ('rules', 'phases', 'wildcards', 'initialState')),
                  'coverageSourcesAllBoundByV12': PC['coverageSourcesAllBoundByV12'], 'planningCheckerPasses': P['check_implementation_planning']['exitCode'] == 0},
     'detail': ('v12 binds exactly the coverage sources (34), so the checker passes, and it correctly binds the one changed contract (native-evidence.md) and the three new incorporated documents while preserving v8-v11 byte-identically. '
                'The layer standing claims the exact normative/reference inputs consumed by planning, and it adds the typescript-semantic order table. It does not add the rust-semantic protocol3 transition table, although native-evidence section 9.2 names that table as the transition authority and source44 changed its normative OpenUniverse state update (frame booleans became host-derived observations) and added rowPayloads naming the new startup schemas. '
                'No layer v8-v12 has ever bound protocol3-transitions.v1.json or fact-batch.schema.v3.json, so this asymmetry predates source44; source44 is the first change that edits the P3 table\'s normative text while binding its TypeScript counterpart.'),
     'consequence': ('No normative content is lost to planning. Every changed statement restates law bound through native-evidence sections 9.1, 9.2, 9.6 and 9.7 and through the bound provider-startup x-opensip-startup-law. The P3 rules, phases, wildcards and initial state are unchanged, and the final candidate manifest binds all bytes. '
                     'A planning consumer reading v12 alone simply does not see the P3 derived-observation annotations next to the TypeScript table.'),
     'disposition': 'ADVISORY, non-blocking. Optional planning-owner improvement: in a future layer, bind protocol3-transitions.v1.json (and fact-batch.schema.v3.json) as incorporated inputs, or state in the layer standing that native tables referenced by native-evidence.md are bound through the formal subject manifest.',
     'owner': 'implementation planning owner (implementation-normative-inputs, implementation-planning-sources, implementation-coverage)',
     'receipts': ['receipts/planning-checks.json', 'receipts/delta-diffs-43to44/docs__coop__design-corrections__native__protocol3-transitions.v1.json.diff']}]

# ------------------------------------------------------------------------------------------------ observations
startup_obs = {r['case']: r['observed'] for r in SR.values() if r['kind'] in ('observation', 'record')}
OBSERVATIONS = [
    {'id': 'OBS44-01', 'text': ('Against root-source44-final-reference.v1 and codex final-reference.v44: all six group stdouts are byte-equal (%s), and %d of %d child stdouts are byte-equal to root. Enumeration and execution-inputs differ from root only in path fields and are equal after removing only those fields. '
                                'Against this origin\'s source43 receipts, the enumeration child is equal after removing path fields. The execution-inputs child has identical cases and no mismatches but also echoes its owned-file digests and the model note string (neededRootInputs[3]), so it records the two changed execution-inputs files (contract 8521f362 -> 22ee2507, model 66a15add -> edeb02b8). '
                                'The group stdouts differ from the source43 receipts only by foundation/workflows sourceFileCount 1247 -> 1252 and native 388/388 -> 477/477 cases. The codex runner-original equals the root reference-checks (%s); codex adds the formal subject binding (changed top-level keys %s).')
     % (all(v['stdoutFileEqualRoot'] and v['stdoutFileEqualCodex'] for v in RC['groups'].values()), RC['childrenEqualRoot'], RC['childCount'], RC['codexRunnerOriginalEqualsRoot'], RC['codexMinusRootTopLevelKeys']),
     'receipt': 'receipts/reference-comparison.json'},
    {'id': 'OBS44-02', 'text': ('The root reference and the root companion planning/inventory checks were executed from a pre-freeze working tree (%s), not from the frozen archive. Their recorded script shas equal the frozen source44 bytes, and their outputs equal this review\'s own executions on verified archive copies: all six group stdouts are byte-equal and the companion planning and inventory stdout text is equal (%s). This review\'s own executions are the acceptance input.')
     % (RC['rootExecutionSourceRoots'], planning_stdout_equal_companion), 'receipt': 'receipts/reference-comparison.json; receipts/planning-checks.json'},
    {'id': 'OBS44-03', 'text': ('Re-observed on source44 by the ten ported scope probes, every observed value is identical to this origin\'s source43 receipts except the policy probe\'s copy-identity row, which records the new copy manifest: %s.')
     % ', '.join('%s %d rows' % (k.replace('P44-PORTED-', '').lower(), v['rows']) for k, v in PORTED_EQUAL.items()), 'receipt': 'receipts/ported44-vs43.json; receipts/probes (ported44_*)'},
    {'id': 'OBS44-04', 'text': ('rustCommitHash has two representations with no required join. The Plan rust-v1 row, HelloV3.expectedIdentity, HelloAckV3 and RustSemanticUniverseV2 use DigestHex (64 hex; resolved-inputs.v2 rust-v1 digestFields), and every required equality among them is measured. ToolchainIdentityV1.rustCommitHash in the native context is 40 hex (section 11 :3923-3925) and is admitted through native-context recomputation and the compiler-version rule. '
                                'No owner equates the two, and the startup author reports none; a future join would need a stated mapping. This is not a cross-owner contradiction. targetTriple/sysrootDigest likewise join Plan row, Hello and universe only.'),
     'receipt': 'receipts/probes/wire44.json; receipts/probes/startup44.json'},
    {'id': 'OBS44-05', 'text': ('Trusted host inputs in the startup reference. The pre-Analyze conversion converts the host plannedStages verbatim: an extra planned stage is converted (%s), and a planned descriptor of another universe raises a host invariant (%s) outside the exchange rather than a protocol refusal. '
                                'Universe members outside the handshake join and resolvedInputs (manifestId, capabilityManifestId, providerArtifactSha256, runtimeArtifactSha256) and a consistently substituted Rust dependencySourceSetId are not re-joined to a Plan object (%s; dependency set substitution admitted: %s). '
                                'The fixture inputs are not one Plan: typescript analyzeStages %s versus plannedStages %s. Section 9.7 (:3230-3233, :3291-3293) assigns planned stages to the host\'s pre-spawn selection and says fixture inputs do not constitute a verified Plan; this is TCB-SCOPE-01 standing, not a design defect.')
     % (startup_obs.get('observation-conversion-trusts-host-plannedStages-input-an-extra-planned-stage-is-converted', {}).get('affectedStageIds'),
        startup_obs.get('observation-conversion-refuses-a-planned-descriptor-of-another-universe-as-a-raised-host-invariant', {}).get('message'),
        startup_obs.get('observation-ts2-universe-members-outside-handshake-join-and-resolvedInputs-are-not-joined-by-reference-admission'),
        startup_obs.get('observation-rust3-consistently-substituted-dependency-set-id-admitted-by-reference-no-host-held-set-join', {}).get('admitted'),
        startup_obs.get('fixture-plan-shape-record-analyze-stages-versus-planned-stages', {}).get('ts.analyzeStageIds'),
        startup_obs.get('fixture-plan-shape-record-analyze-stages-versus-planned-stages', {}).get('ts.plannedStageIds')),
     'receipt': 'receipts/probes/startup44.json'},
    {'id': 'OBS44-06', 'text': ('Cancellation and exit asymmetries are inherited and scoped. On typescript-semantic a zero-exit after Cancelled faults the abstract table (trace %s): the table standing says exit-status policy after Cancelled is not modeled, supervision.userCancellation D9 precedence governs it, and its terminal law follows delivery.v2 cancelTransition (after Cancelled only EOF). '
                                'rust-semantic P3-30 requires zero-exit then eof after Cancelled (trace %s). The TS observedPhase check covers only the inserted interval; a Cancel in ANALYZING observing snapshot is not checked (terminal %s). Rust P3-25 has no output-seen guard (Unavailable after FactBatch reaches %s), unlike T2-14; the P3 rows are unchanged 43->44.')
     % ((startup_obs.get('observation-ts2-zero-exit-after-cancelled-is-outside-table-scope-and-faults-the-abstract-machine', {}).get('result') or {}).get('trace', [None])[-3:],
        (startup_obs.get('observation-rust3-inherited-p3-30-requires-zero-exit-after-cancelled') or {}).get('trace', [None])[-4:],
        (startup_obs.get('observation-ts2-cancel-in-analyzing-observed-phase-unchecked-inherited-interval') or {}).get('terminalKind'),
        (startup_obs.get('observation-rust3-inherited-p3-25-has-no-output-seen-guard') or {}).get('finalPhase')),
     'receipt': 'receipts/probes/startup44.json'},
    {'id': 'OBS44-07', 'text': ('Commitments beyond the TS batch commitment are not recomputed by the reference. An arbitrary well-formed coverageCommitment reaches complete (%s), and stageFacts/factStream/stageCoverage/coverageStream (delivery.v2 commitments.domains; rust-provider-protocol.v2 commitments) are not executed. Section 9.7 (:3264-3268, :3287-3288) keeps their recipes unchanged over CoverageResultV3 and discloses the scope; they remain implementation obligations of their inherited owners.')
     % (startup_obs.get('observation-coverage-commitment-not-recomputed-by-reference', {}).get('terminalKind'),), 'receipt': 'receipts/probes/startup44.json'},
    {'id': 'OBS44-08', 'text': ('The registered bundle keeps HelloV3, HelloAckV3 and ProtocolLimitsV3 bytes. Validated directly, they refuse the published full Hello, HelloAck and 32-member limits and admit only their own four-member Hello (%s). Section 0 :124, the wire law supersedes list and the native README name the supersession, so a consumer must select the handshake schema by those selectors, not by the registered definition name. '
                                'Exact JSON typing also refuses a float-typed identity version (%s).') % (json.dumps({k: v.get('admitted') for k, v in w('registered-superseded-definitions-refuse-the-published-full-records-and-admit-only-their-own-narrow-shape').items() if isinstance(v, dict)}),
                                                                                                         WR.get('ts-hello-identity-versions-float-typed-2.0', {}).get('observed', {}).get('detail')),
     'receipt': 'receipts/probes/wire44.json'},
    {'id': 'OBS44-09', 'text': ('The root scope clarification changed native-evidence.md, the native model and the checker after the startup author (before 8d525ab1/b556340f/e79b2f81, after 45c6d798/408bdc10/1d293100). The before bytes belong to the author runtime, which this review did not read, so the statement "No executable behavior changed" was not independently diffed. '
                                'This review assessed the final after bytes directly: section 9.7 read completely, the model\'s startup section and the complete 43->44 diffs read, and the behaviour measured by its own probes and the 477-case checker.'),
     'receipt': 'root-startup43-scope-clarification.v1/clarification.json (evidence)'},
    {'id': 'OBS44-10', 'text': ('provider_attribution_return_model.v2.py renames the internal omitted-delivery label "unnegotiated-fact-batch-v2" to "unnegotiated-historical-fact-batch" and adds a docstring; the gate\'s executable body is otherwise identical (%s). The label is not a public detail. The provider-attribution-return child stdout is byte-identical to this origin\'s source43 receipt, and the package RunIds are unchanged.')
     % (w('token-gate-executable-body-unchanged-from-source43-except-docstring-and-omitted-delivery-label').get('label43'),), 'receipt': 'receipts/probes/wire44.json'},
    {'id': 'OBS44-11', 'text': 'Package verification of bound package21 differs from the root rebuild verification only in packageManifestSha256 (e5639aa3 bound versus c97d6f3b pre-binding) and packageFilesVerified; every group, count, observation and other output file is equal. The first probe attempt expected only the manifest to differ and is preserved.',
     'receipt': 'receipts/probes/package-v21.json; receipts/probes/package-v21.attempt1-row-expectation-too-narrow.json'},
]

# ------------------------------------------------------------------------------------------------ prior finding dispositions
QOWN = {k: U[k] for k in ('query-projection-contract.v3.md', 'query_projection_model.v3.py', 'check-query-projection.v3.py', 'query_surface_projection.v3.py', 'graph-query.schema.json')}
if not all(QOWN.values()):
    GAPS.append('query owners changed 43->44')
PRIOR_DISPOSITIONS = [
    {'id': 'S40-01', 'priorSeverity': 'SHOULD (source40)', 'source43Disposition': 'REMAINS RESOLVED ON SOURCE43', 'currentDisposition': 'REMAINS RESOLVED ON SOURCE44', 'basis': 'new-44',
     'reasoning': ('The execution-inputs schema and fixture and the enumeration contract/model are byte-identical 43->44 (%s). The execution-inputs contract changed only at :272 and :290 and the model only in its note string at :109-110, both renaming the historical per-language FactBatch; the section 3 attribution predicate, section 8 capture exactness and the model code are unchanged. '
                   'Current evidence: the execution-inputs child runs 95 cases and the enumeration child 54. Both equal root after removing only path fields. Against this origin\'s source43 receipts the enumeration child is path-only equal, and the execution-inputs cases are identical, differing only in the echoed digests and note string of the two changed files. The capture-join measurement is identical.')
     % json.dumps({k: U[k] for k in ('execution-inputs.schema.v1.json', 'execution_inputs_fixture.v3.py', 'enumeration-contract.v1.md', 'enumeration_model.v1.py')}),
     'evidence': ['receipts/reference-comparison.json', 'receipts/probes/capture-joins-on44.json', 'receipts/delta-diffs-43to44 (execution-inputs contract and model)']},
    {'id': 'ADV40-01', 'priorSeverity': 'EDITORIAL (source40)', 'source43Disposition': 'REMAINS RESOLVED ON SOURCE43', 'currentDisposition': 'REMAINS RESOLVED ON SOURCE44', 'basis': 'new-44',
     'reasoning': ('implementation-planning-sources.v1.json now selects v12 (%s...) as current with v11 as previous and moves the v10 record into the prior-layer history (%d records whose digests match their bytes: %s). Layers v8-v11 are byte-identical to source43 (%s), and v8 stays a superseded intermediate. No historical layer was mutated.')
     % (PC['layerSha256']['12'][:12], PC['planningSourcesHistoryCount'], PC['planningSourcesHistoryHashesMatchLayerBytes'], PC['priorLayersByteEqualToSource43']),
     'evidence': ['receipts/planning-checks.json', 'receipts/delta-diffs-43to44/docs__v2__architecture__implementation-planning-sources.v1.json.diff']},
    {'id': 'ADV42-01', 'priorSeverity': 'ADVISORY (source42)', 'source43Disposition': 'RETAINED ADVISORY', 'currentDisposition': 'RETAINED ADVISORY (see advisories)', 'basis': 'new-44',
     'reasoning': ADVISORIES[0]['currentStanding'], 'evidence': ADVISORIES[0]['receipts']},
    {'id': 'OBS43-01', 'source43Disposition': 'OBSERVATION', 'currentDisposition': 'RETAINED OBSERVATION', 'basis': 'unchanged-43-basis',
     'reasoning': 'Query contract, model, checker, surface projection and graph-query schema are byte-identical 43->44 (%s); the omitted-observation reporting statement stands as assessed on source43.' % json.dumps(QOWN), 'evidence': ['mapSources']},
    {'id': 'OBS43-02', 'source43Disposition': 'OBSERVATION', 'currentDisposition': 'RETAINED OBSERVATION', 'basis': 'unchanged-43-basis', 'reasoning': 'Query model byte-identical 43->44; availability remains outside the cursor binding.', 'evidence': ['mapSources']},
    {'id': 'OBS43-03', 'source43Disposition': 'OBSERVATION', 'currentDisposition': 'RETAINED OBSERVATION', 'basis': 'unchanged-43-basis', 'reasoning': 'Query contract and graph-query schema byte-identical 43->44; the path-row orientation representation stands.', 'evidence': ['mapSources']},
    {'id': 'OBS43-04', 'source43Disposition': 'OBSERVATION', 'currentDisposition': 'SUPERSEDED BY OBS44-01 (historical comparison not relabelled)', 'basis': 'new-44', 'reasoning': 'The source43 reference comparison stays historical; the source44 comparison is OBS44-01.', 'evidence': ['receipts/reference-comparison.json']},
    {'id': 'OBS43-05', 'source43Disposition': 'OBSERVATION', 'currentDisposition': 'SUPERSEDED BY OBS44-02 (historical record not relabelled)', 'basis': 'new-44', 'reasoning': 'The source43 working-tree execution record stays historical; the source44 equivalent is OBS44-02.', 'evidence': ['receipts/reference-comparison.json']},
    {'id': 'OBS43-06', 'source43Disposition': 'OBSERVATION', 'currentDisposition': 'RETAINED (OBS44-03)', 'basis': 'new-44', 'reasoning': 'The ten ported probes re-observe every value on source44, apart from the policy probe\'s copy-identity row.', 'evidence': ['receipts/ported44-vs43.json']},
    {'id': 'OBS43-07', 'source43Disposition': 'OBSERVATION', 'currentDisposition': 'HISTORICAL; STANDS (query model unchanged 43->44)', 'basis': 'unchanged-43-basis', 'reasoning': 'The three-hunk source43 query model delta description stays true of unchanged source44 bytes.', 'evidence': ['mapSources']},
]
V43PRIOR = {d['id']: d for d in V43['priorFindingDispositions']}
PROBE_FOR = {'OBS40-01': 'P44-PORTED-POLICY', 'OBS40-02': 'P44-PORTED-POLICY', 'OBS40-03': 'P44-PORTED-POLICY', 'OBS40-04': 'P44-PORTED-NATIVE', 'OBS40-05': 'P44-PORTED-NATIVE',
             'OBS40-06': 'P44-PORTED-NATIVE', 'OBS40-09': 'P44-PORTED-POLICY', 'S39-01': 'P44-PORTED-POLICY', 'S39-02': 'P44-PORTED-POLICY', 'ADV39-01': 'P44-PORTED-RUNTERM',
             'ADV38-01': 'P44-PORTED-TERM7', 'ADV38-02': 'P44-PORTED-CARRIER'}
OBS42_BASIS = {
    'OBS42-01': ('new-44', 'execution_inputs_fixture.v3.py byte-identical 43->44 (%s) and execution_inputs_model.v1.py changed only in a note string; the reference builder\'s single-producer attribution limitation is unchanged.' % U['execution_inputs_fixture.v3.py']),
    'OBS42-02': ('new-44', 'enumeration-contract.v1.md byte-identical 43->44 (%s); native_evidence_model.v2.py changed only by two appended regions (the wire loader at :573-590 and the startup section from :4557), so the binder shorthand remains disambiguated.' % U['enumeration-contract.v1.md']),
    'OBS42-03': ('new-44', 'Capture code unchanged (model note only); the refs-only capture consequence stands; the execution-inputs child cases are equal modulo paths.'),
    'OBS42-04': ('new-44', 'Source44 changes no execution-inputs identity or encoding code, so no further re-encoding occurs; the execution-inputs child is equal modulo paths.'),
    'OBS42-05': ('unchanged-43-basis', 'enumeration_model.v1.py byte-identical 43->44 (%s); the explicit js-synthesized refusal stands; enumeration cases equal modulo paths.' % U['enumeration_model.v1.py']),
    'OBS42-06': ('unchanged-43-basis', 'Enumeration bytes unchanged 43->44; unavailable-binding programEntry freedom stands with no canonical encoding stated.'),
    'OBS42-07': ('unchanged-43-basis', 'Historical source42 comparison stays historical (superseded on source43 and again by OBS44-01).'),
    'OBS42-08': ('new-44', 'Ported probes re-observe every value on source44 (OBS44-03).'),
}
for i, prior in V43PRIOR.items():
    if i in {d['id'] for d in PRIOR_DISPOSITIONS}:
        continue
    cur = prior['currentDisposition'].replace(' (unchanged on source43)', '')
    if i in OBS42_BASIS:
        basis, reasoning = OBS42_BASIS[i]
    elif i in PROBE_FOR:
        basis, reasoning = 'new-44', 'Source43 disposition %s. On source44 the owning probe %s re-observes every row identically (%d rows).' % (prior['currentDisposition'], PROBE_FOR[i], PORTED_EQUAL[PROBE_FOR[i]]['rows'])
    elif i == 'OBS40-07':
        basis, reasoning = 'new-44', 'Source43 disposition CLOSED. The removed no-op continue stays removed; the only execution_inputs_model.v1.py change is the note string at :109-110.'
    elif i == 'OBS40-08':
        basis, reasoning = 'unchanged-43-basis', 'Source43 disposition SUPERSEDED. The historical comparisons stay historical; the source44 comparison is OBS44-01.'
    elif i == 'OBS40-10':
        basis, reasoning = 'new-44', 'Source43 disposition HISTORICAL CORRECTION STANDS. The mapping population is 322 on source43 and source44; 15 native-evidence rows changed their source digests, and no row id was added or removed (measured).'
    else:
        basis, reasoning = 'unchanged-43-basis', 'Source43 disposition %s. commit-recovery-readonly.v3.md is byte-identical 43->44 (%s).' % (prior['currentDisposition'], U['commit-recovery-readonly.v3.md'])
    PRIOR_DISPOSITIONS.append({'id': i, 'source43Disposition': prior['currentDisposition'], 'currentDisposition': cur + ' (on source44)', 'basis': basis, 'reasoning': reasoning,
                               'evidence': (['receipts/probes/' + PBY[PROBE_FOR[i]]['result']['receipt'].split('/')[-1]] if i in PROBE_FOR else ['mapSources', 'receipts/planning-checks.json'])})
covered = {d['id'] for d in PRIOR_DISPOSITIONS}
for x in V43['newMustIssues'] + V43['newShouldIssues'] + V43['advisories'] + V43['observations'] + V43['priorFindingDispositions']:
    if x['id'] not in covered:
        GAPS.append('prior finding/advisory/observation without current disposition: ' + x['id'])

# ------------------------------------------------------------------------------------------------ items
WIRE_EVID = {
    'tsLimits': w('ts-hello-limits-are-exactly-the-ten-delivery-v2-numeric-limits-equal-values-and-equal-cbor-bytes'),
    'rustLimits': w('rust-hello-limits-are-the-24-rust-v2-limits-plus-the-eight-section-9.3-limits-32-exactly-and-equal-the-registered-eight'),
    'contractDigest': w('rust-expected-contract-digest-is-raw-sha256-of-selected-rust-v2-artifact-bytes-pinned-in-law-prose-and-fixture'),
    'descriptorDigests': w('ts-descriptor-digests-are-sha256-of-canonical-json-of-the-closed-delivery-v2-descriptors'),
    'tsRetention': w('ts-hello-and-helloack-retain-every-inherited-v1-member-and-add-only-tokens-and-identityVersions'),
    'rustRetention': w('rust-hello-and-helloack-retain-rust-v2-and-registered-v3-members-and-identity-fields'),
    'supersession': w('registered-schema-supersession-is-narrow-three-definitions-named-in-section0-registered-bytes-unchanged'),
    'registeredDefinitions': w('registered-superseded-definitions-refuse-the-published-full-records-and-admit-only-their-own-narrow-shape'),
    'tokenEnums': w('per-language-token-enums-are-the-registered-token-set-minus-the-other-languages-only-tokens'),
    'artifactMajors': WR.get('inherited-artifact-major-values-versus-law-text', {}).get('observed'),
    'groups': {k: grp(WR, k, 'wire44') for k in ('ts-hello-', 'ts-helloack-', 'rust-hello-', 'rust-helloack-')},
    'refusals': wire_refusals(('ts-hello', 'rust-hello')),
}
FB_EVID = {
    'tsV1Commitment': w('ts-historical-FactBatchV1-without-token-admitted-with-independently-recomputed-wire-commitment'),
    'jsonVectorCommitmentDiffers': w('ts-commitment-over-json-vector-candidates-differs-from-wire-commitment'),
    'rustV2': w('rust-historical-FactBatchV2-without-token-admitted-no-per-batch-commitment'),
    'tsV3SameProjection': w('ts-negotiated-FactBatchV3-admitted-same-candidate-projection-as-V1'),
    'rustV3SameProjection': w('rust-negotiated-FactBatchV3-admitted-same-candidate-projection-as-V2'),
    'mapOrder': w('text-key-map-order-bytewise-encoded-equals-length-first-rule'),
    'cap4096': w('ts-V1-exactly-4096-facts-admitted'),
    'gate': {c: {'ok': r['ok'], 'gate44': (r['observed'].get('gate44') or {}).get('status'), 'wireAdmitted': (r['observed'].get('wire') or {}).get('admitted'),
                 'gate43EqualExceptLabel': r['observed'].get('gate43EqualsGate44ExceptDeliveryLabel')} for c, r in WR.items() if c.startswith('occupancy-gate-')},
    'unnegotiatedV3': w('unnegotiated-v3-refused-by-both-gate-and-wire-law'),
    'gateBody': w('token-gate-executable-body-unchanged-from-source43-except-docstring-and-omitted-delivery-label'),
    'refusals': wire_refusals(('ts-V1', 'ts-V3', 'rust-V2', 'rust-V3')),
}
for k in ('gate',):
    if len(FB_EVID[k]) != 6 or not all(v['ok'] for v in FB_EVID[k].values()):
        GAPS.append('occupancy gate rows not as measured')
STARTUP_EVID = {
    'universeIdentity': s('universe-identity-is-independent-H-over-resolvedInputs-and-joins-universeKey-requested-keys-and-planned-descriptors'),
    'subjectScopeJoin': s('requested-key-subject-scope-commitment-equals-host-planned-descriptor-commitment'),
    'nativeContextFixtureBinding': s('native-context-suffix-is-a-plan-native-context-digest-in-fixture-inputs'),
    'tsComplete': (s('ts2-complete-positive') or {}).get('trace'), 'rustComplete': (s('rust3-empty-dependency-custody-complete-positive') or {}).get('trace'),
    'rustPrepared': (s('rust3-prepared-mode-derived-from-admitted-payload-reaches-prepared-custody-positive') or {}).get('trace'),
    'importedDescriptor': s('rust3-imported-descriptor-preparation-null-authorization-and-effects-admitted-prepared-mode'),
    'groups': {k: grp(SR, k, 'startup44') for k in ('ts2-open-universe-', 'rust3-open-universe-', 'ts2-universe-accepted-', 'rust3-universe-accepted-', 'ts2-native-context-verified-',
                                                    'rust3-native-context-verified-', 'rust3-repository-resolution-', 'rust3-prepared-', 'rust3-authorization-', 'rust3-effects-')},
    'refusals': startup_refusals(('ts2-open-universe', 'rust3-open-universe', 'ts2-universe', 'rust3-universe', 'ts2-native-context', 'rust3-native-context', 'ts2-plan-native', 'rust3-repository',
                                  'rust3-null', 'rust3-authorization', 'rust3-mode', 'rust3-skipping')),
    'p3AbstractOnly': SR.get('abstract-event-only-p3-10-reachable-only-with-asserted-dependencyMode-false-no-whole-wire-claim', {}).get('observed', {}).get('trace'),
}
PRE_EVID = {
    'tsConversion': s('ts2-pre-analyze-native-context-mismatch-then-zero-exit-eof-host-derives-provider-unavailable-coverage'),
    'rustConversion': s('rust3-pre-analyze-native-context-mismatch-host-derives-provider-unavailable-coverage'),
    'payloadShape': s('pre-analyze-payload-carries-no-analysis-members-and-exact-reason'),
    'reasonEnums': s('post-analyze-reason-enums-equal-law-lists-and-exclude-native-context-mismatch'),
    'groups': {k: grp(SR, k, 'startup44') for k in ('ts2-pre-analyze-', 'rust3-pre-analyze-', 'ts2-post-analyze-', 'rust3-post-analyze-')},
    'outcomes': startup_refusals(('ts2-pre-analyze', 'rust3-pre-analyze', 'ts2-post-analyze', 'rust3-post-analyze')),
}
COV_EVID = {
    'groups': {k: grp(SR, k, 'startup44') for k in ('ts2-coverage-', 'rust3-coverage-', 'ts2-entry-', 'rust3-entry-', 'ts2-cancel')},
    'outcomes': startup_refusals(('ts2-coverage', 'rust3-coverage', 'ts2-entry', 'rust3-entry', 'ts2-cancel', 'ts2-hello', 'rust3-helloack')),
}
INV43, INV44 = J(S43 + '/' + ARCHD + 'repository-file-inventory.v1.json'), J(S44 + '/' + ARCHD + 'repository-file-inventory.v1.json')
INV_ROWS_EQUAL = INV43['files'] == INV44['files'] and INV43['packages'] == INV44['packages']
if not INV_ROWS_EQUAL:
    GAPS.append('inventory file or package rows changed 43->44')
ITEMS = [
    {'id': 'CH44-WIRE-HANDSHAKE', 'disposition': 'SUFFICIENT AND CONSISTENT (both languages)',
     'assessment': ('Exact per-language fields. typescript-semantic major 2 (section 0 :119; 9.4): TypeScriptHelloV2 is delivery.v2 HelloV1 {hostBuildId, expectedProviderDescriptorSha256, expectedRuntimeDescriptorSha256, limits} plus expectedCapabilities and identityVersions, with no payload protocolMajor. TypeScriptHelloAckV2 keeps all 14 HelloAckV1 members (protocolMajor const 2, capabilities now the Hello echo) plus identityVersions. Both set equalities were measured against delivery.v2 bytes. '
                    'rust-semantic major 3 (section 0 :122, :124; 9.1): HelloV3 is the rust v2 HelloV2 members plus the registered HelloV3 members; HelloAckV3 is HelloAckV2 plus registered HelloAckV3; ExpectedRustIdentityV3 is ExpectedRustIdentityV2 with protocolMajor 3. '
                    'Supersession is narrow: exactly the three registered definitions (wire law supersedes; section 0 :124), with the registered bundle bytes unchanged. The artifact majors (delivery.v2 1, rust v2 2) are superseded selectors in section 0 :119/:122, so the law\'s "is 2"/"is 3" states the successor value, not a contradiction. '
                    'Limits: the TS map is exactly the ten numeric delivery.v2 limits with equal values and CBOR bytes (limitRule excluded). The Rust map is the 24 rust v2 limits plus the eight values parsed from section 9.3, which equal the registered ProtocolLimitsV3 consts: 32 members. Nine- and eleven-member, changed, float-typed and cross-language maps refuse before HelloAck. '
                    'Contract digest: the raw SHA-256 of the rust-provider-protocol.v2.json bytes equals the law pin, the section 9.1 prose and the fixture. A canonical-JSON digest would differ, so the byte source is decisive, and a flipped digest refuses CONTRACT_DIGEST. '
                    'Identity joins: the TS descriptor digests are recomputed as SHA-256 of the canonical JSON of the closed delivery.v2 descriptors. Each of the 11 descriptor fields of HelloAck, when not equal to the verified descriptor, refuses DESCRIPTOR_FIELD (protocolMajor at SCHEMA). A digest echo refuses DESCRIPTOR_DIGEST_ECHO, a Hello digest not of the verified descriptor refuses DESCRIPTOR_DIGEST, and verified-descriptor shape, major and work-budget errors refuse. '
                    'Rust: each of the six expectedIdentity fields not equal to the Plan rust-v1 row refuses EXPECTED_IDENTITY, a missing verified member refuses, and each of the five HelloAck echoes refuses IDENTITY_ECHO. The verified descriptors and the Plan row are trusted host inputs whose join to the signed release stays with resolved-inputs.v2 deliveryJoin (TCB-SCOPE-01). '
                    'Tokens: Hello tokens must equal the selected signed row in ascending UTF-8 order. Unsorted, missing, extra, duplicated and identity-less rows refuse, and a HelloAck subset, superset, reorder or mismatched attribution echo refuses. Per-language enums are the registered CapabilityToken set minus the other language\'s only tokens. '
                    'identityVersions {snapshot 2, plan 2, fact 2, coverage 3} is echoed exactly: changed values refuse at SCHEMA and a float-typed 2.0 refuses. Envelope majors 1, 3, "2" and 2.0 refuse PROTOCOL_MAJOR. Inside the exchange a Hello or HelloAck refusal ends in FAULT with no source byte sent. '
                    'Positive reachability precedes every refusal: TS and Rust Hello/HelloAck admit, with and without target-attribution-v2. %d wire rows, 0 failed.') % WIRE_ROWS,
     'evidence': WIRE_EVID},
    {'id': 'CH44-FACTBATCH-AND-OCCUPANCY', 'disposition': 'SUFFICIENT AND CONSISTENT; HISTORICAL WORDING DISAMBIGUATED, NOT RELABELLED',
     'assessment': ('With target-attribution-v2 absent the payload is historical per language: typescript-semantic delivery.v2 FactBatchV1 {analysisOrdinal 0, stageId, batchIndex, facts, batchCommitment} and rust-semantic FactBatchV2 {analysisOrdinal, stageId, batchIndex, candidates}. FactBatchV3 applies when the token is negotiated (section 0 :120/:123; 9.6 :3061-3086; fact-batch v3 whenAbsent/commitments/wireProjection). '
                    'Candidate projection: canonicalRelationPayloadHex equals deterministic CBOR of decodedRelationPayload under an independent encoder, and the wire candidate array CBOR equals the fixture vector. The TS batch commitment is recomputed independently as SHA-256(UTF8(opensip.ts-provider.fact-batch.v1) || 0x00 || CBOR(wire FactCandidateV1 array)) under delivery.v2 commitments.domainRule and equals fixture and model. A commitment over the JSON-vector candidates differs and refuses. '
                    'V1 and V3 carry the identical candidate projection, as do Rust V2 and V3. Refusals: V1 or V2 with the token (HISTORICAL_WITH_TOKEN); V3 without it (UNNEGOTIATED_V3); cross-language shapes; altered or JSON-vector commitment; missing batchCommitment and a V2 carrying one; hex not CBOR; TS analysisOrdinal 1 (SCHEMA on V1, ANALYSIS_ORDINAL on V3); correlation and ordinal contiguity. Exactly 4096 facts admit and 4097 refuse. '
                    'The inherited map-order rules coincide for text keys, including 23/24/255/256-byte keys. Stage-stream commitments keep their inherited recipes and are not recomputed (OBS44-07). '
                    'Occupancy: the source44 _token_gate differs from source43 only in its docstring and omitted-delivery label (OBS44-10). With the token absent it omits capture for a junk map, a Rust V2 shape under TS, a wrong commitment, a hex/CBOR mismatch, a non-map and a valid V1 alike. The wire law refuses all of them except the valid V1, and an unnegotiated V3 refuses in both. A scoped omission therefore validates no historical batch, as section 9.6 :3083-3086 and the gate docstring now state. '
                    'Historical wording: source43 execution-inputs (:272, :290), fact-batch v3, occupancy-companion and attribution-return texts named one generic historical FactBatchV2. For typescript-semantic that reading was ambiguous under those bytes. Source44 disambiguates it per language, and earlier generic readings are not relabelled as reader bugs.'),
     'evidence': FB_EVID},
    {'id': 'CH44-STARTUP-OPEN-UNIVERSE', 'disposition': 'SUFFICIENT AND CONSISTENT; HOST CONSTRUCTION TRUSTED (OBS44-05)',
     'assessment': ('Exact identity-bearing fields (startup schema; section 0 :125, :128; 9.7 :3158-3203): TypeScriptOpenUniverseV2 {executionId, snapshotId snapshot2, planId plan2, planIntentCommitment, providerId const, universe, universeKey} and TypeScriptUniverseAcceptedV2 {executionId, snapshotId, planId, universeKey}. OpenUniverseV3 has repositoryResolution and no universeKey, and UniverseAcceptedV3 echoes six members recursively. '
                    'Measured: each of the four correlation members refuses OPEN_UNIVERSE_CORRELATION in both languages, and plan1/v1 snapshot forms and a foreign providerId refuse at SCHEMA. universeKey equals an independently recomputed H(native.semantic-universe.typescript.v2, resolvedInputs) and joins the requested-key universe ids and planned descriptors by suffix; a flipped key refuses UNIVERSE_KEY. Each of the 11 TS and 6 Rust handshake-join members refuses UNIVERSE_HANDSHAKE_JOIN when it differs. '
                    'nativeContext applicability: in both languages the context is universe.resolvedInputs.nativeContextId, whose 64-hex suffix must be a member of plan.nativeContextDigests. Unbound and sha256:-prefixed digest lists refuse NATIVE_CONTEXT_NOT_PLAN_BOUND. '
                    'repositoryResolution applicability: a TS OpenUniverse carrying it refuses at SCHEMA. For Rust, dependencySourceSetId and preparedOutputSetId equal resolvedInputs, and authorizationId/effects pair with the host-selected preparation (null for imported-descriptor). A mismatched set id, a prepared set not in the universe, authorization without a prepared set, authorization not held by the host, authorization without effects and effects not the authorized ones each refuse REPOSITORY_RESOLUTION_JOIN. '
                    'Host-derived modes: dependencyMode is true for every admitted OpenUniverseV3. A null set id refuses at SCHEMA, so empty custody still has a set id and takes DependencySourceManifest/Seal/Accepted (P3-11, P3-13, P3-15), while skipping custody faults P3-34. preparedMode follows preparedOutputSetId and reaches P3-14/16/18/19, mode booleans on the wire refuse, and P3-10 is reachable only by an abstract event with asserted booleans. '
                    'Echo and state validation: each UniverseAccepted member mismatch refuses UNIVERSE_ACCEPTED_ECHO. NativeContextVerifiedV1 requires equal:true and both ids equal to the OpenUniverse context. '
                    'Standing: the reference joins the host-constructed OpenUniverse to the handshake, native context and resolution; the remaining universe members and a consistently substituted dependency set id are host construction from the verified Plan (OBS44-05).'),
     'evidence': STARTUP_EVID},
    {'id': 'CH44-PRE-ANALYZE-UNAVAILABLE', 'disposition': 'SUFFICIENT AND CONSISTENT; CONVERSION OVER TRUSTED PLANNED STAGES',
     'assessment': ('Payload PreAnalyzeUnavailableV1 {executionId, snapshotId, planId, reason const native-context-mismatch, nativeContextId, recomputedNativeContextId} (9.2 :2881-2882; 9.7 :3205-3226). '
                    'Phase: lawful only in WAIT_NATIVE_CONTEXT_VERIFIED (T2-10 after T2-08; P3-21 after custody P3-15). After NativeContextVerified and before Analyze no row matches (T2-23/P3-34); after Analyze it refuses UNAVAILABLE_PHASE_PAYLOAD; before SnapshotAccepted it faults; and a post-Analyze payload inside the interval refuses. '
                    'Correlation: executionId, snapshotId, planId and nativeContextId each refuse when they differ; equal contexts refuse NOT_A_MISMATCH; analysisOrdinal refuses at SCHEMA, affectedStageIds as a phase payload, and any other reason at SCHEMA. '
                    'Reason sets: TypeScriptUnavailableV2 (6) and UnavailableV3 (9) equal the law lists and exclude native-context-mismatch. They are the inherited delivery.v2 (3) and rust v2 (4) reasons plus the applicable UnavailableReasonV3 additions (9.2 :2889-2891; that registered enum is used by no bundle definition), minus native-context-mismatch, which moved to the pre-Analyze payload. Every post-Analyze reason reaches DONE unavailable with no host conversion, and cross-language reasons refuse. '
                    'Clean versus malformed: only zero-exit then eof reaches DONE. Nonzero exit and signal death fault (T2-22/P3-33), eof before zero-exit faults, any other frame after the terminal is post-terminal, an extra zero-exit after DONE faults, and without eof nothing is converted. A malformed or uncorrelated payload is PROVIDER.PROTOCOL_VIOLATION with stage_authority fault (authority none). '
                    'Host conversion after DONE: coverageSource host-derived, workerCoverageCarried false, affectedStageIds equal to the host planned stages, and one CoverageResultV3 per planned descriptor: coverage unknown, deficiency provider-unavailable, null cause, confidence 0, no derivation kinds, key joined to the recomputed universe suffix and subject-scope commitment. Each is admitted by admit_coverage_result_v3, with stage_authority unavailable and termination COVERAGE.PROVIDER_UNAVAILABLE, matching delivery.v2 cleanUnavailable (never operational-failed). '
                    'Standing: admitted wire payload/state plus host conversion over a trusted plannedStages input; this is not complete retained Run replay, and the reference does not re-derive planned stages from a Plan (OBS44-05).'),
     'evidence': PRE_EVID},
    {'id': 'CH44-COVERAGE-AND-CANCELLATION', 'disposition': 'SUFFICIENT AND CONSISTENT',
     'assessment': ('Frame selectors: typescript-semantic keeps frame Coverage with TypeScriptCoverageV2 (analysisOrdinal 0); rust-semantic uses frame CoverageV3 (P3-24) with CoverageV3. The other language\'s frame name faults with no matching row (T2-23/P3-34), not as a payload refusal. '
                    'Whole payload versus entry: the wrapper {analysisOrdinal, stageId, entries, coverageCommitment} admits CoverageResultV3 entries. A CoverageResultV1 entry refuses at /entries/0, and a CoverageResultV3 sent as the whole frame refuses at the wrapper, in both languages. '
                    'Correspondence: a wrong stageId refuses COVERAGE_STAGE and extra entries refuse COVERAGE_BIJECTION (both languages). Each of relation, resolution, subjectScopeCommitment, sourceUniverse and targetUniverse that is not the requested key refuses COVERAGE_KEY_CORRESPONDENCE, and a sha256:-prefixed universe refuses at SCHEMA. TS analysisOrdinal 1 refuses; Rust analysisOrdinal is uint64. Commitments are not recomputed (OBS44-07). '
                    'Cancellation interval: a Cancel in host phase WAIT_NATIVE_CONTEXT_VERIFIED or READY_ANALYZE requires observedPhase snapshot (T2-18, T2-19, T2-21). analysis, universe and handshake refuse CANCELLED_OBSERVED_PHASE naming the phase, an out-of-enum value refuses, and a second Cancel faults. Outside the interval observedPhase keeps its inherited meaning and is not checked (OBS44-06).'),
     'evidence': COV_EVID},
    {'id': 'CH44-RUST-COMMIT-REPRESENTATION', 'disposition': 'NO JOINED EQUALITY REQUIRED BEYOND THE 64-HEX PLAN/HANDSHAKE/UNIVERSE CHAIN; CONSISTENT',
     'assessment': ('The Plan rust-v1 row, HelloV3.expectedIdentity, HelloAckV3 and RustSemanticUniverseV2 carry rustCommitHash as DigestHex (64 hex, the resolved-inputs.v2 rust-v1 digestFields representation). Every joined equality the final design requires stays within that representation and was measured: Hello expectedIdentity to the Plan row, HelloAck echo to Hello, and universe to Hello. A 40-hex value refuses at SCHEMA. '
                    'The native-context toolchain (ToolchainIdentityV1.rustCommitHash, 40 hex) is a separate record reached through nativeContextId (section 11 :3916-3930) and admitted by native-context recomputation. No owner requires equality between the two representations. There is no cross-owner field contradiction, and a future join would need a stated mapping (OBS44-04).'),
     'evidence': {'forty': WR.get('rust-hello-forty-hex-toolchain-commit-representation-refused', {}).get('observed'),
                  'identityJoin': WR.get('rust-hello-expected-identity-rustCommitHash-not-the-plan-row-refused', {}).get('observed'),
                  'echo': WR.get('rust-helloack-rustCommitHash-not-the-hello-expected-identity-refused', {}).get('observed'),
                  'universe': SR.get('rust3-open-universe-universe-rustCommitHash-not-the-hello-expected-identity-refused', {}).get('observed', {}).get('refusal')}},
    {'id': 'CH44-CROSS-OWNER-CONSISTENCY', 'disposition': 'CONSISTENT; NO FIELD OR ROUTE CONTRADICTION FOUND',
     'assessment': ('Section 0 (:119-129) names every superseded, retained or extended selector the correction touches. For delivery.v2: majors, Hello/HelloAck, FactBatchV1 and commitments (retained), normalPhases and frames (extended), OpenUniverse/UniverseAccepted/SnapshotId/PlanId/universe/key, CoverageV1/CoverageResultV1/Unavailable/BudgetExhausted/commitment fields, and unavailableTerminal/cleanUnavailable/CancelledV1.observedPhase. For rust v2: majors, Hello/HelloAck/ExpectedRustIdentityV2, FactBatchV2, OpenUniverseV2/UniverseAcceptedV2/SnapshotId/PlanId/RustUniverseV1/universe id algorithms, and Coverage/CoverageV2/UnavailableV2/BudgetExhaustedV2/commitments/StageResultV2. Also the registered HelloV3/HelloAckV3/ProtocolLimitsV3. The native README mirrors the same rows. '
                    'The P3 table changed only stateUpdates (host-derived observations), derivedObservations and rowPayloads; rules, phases, wildcards and initial state are unchanged, and the row payloads match section 9.2 :2881-2884 and the startup schemas. '
                    'Layout 14 and the file inventory carry the identical revised decision sentence, and the build plan the matching paragraph: per-language handshakes over shared frame envelopes. Inventory file and package rows are unchanged (%s). The attribution-return schema modes, execution-inputs contract and model notes, and the occupancy and fact-batch texts now name the per-language historical payload. '
                    'The TS order table transcribes delivery.v2 ordering with exactly the 9.4/9.7 insertions. Its terminal law (after cancelled only eof) matches delivery.v2 cancelTransition, and it states that exit-status policy after Cancelled is not modeled. Section 12 stops restating case and definition counts. '
                    'Owner routing for implementation: crates/components/src/provider_protocol.rs dispatches the provider wire protocol, crates/host/src/fact_admission.rs (:751) admits candidates, Coverage and occupancy joins, and crates/host/src/analysis.rs (:695) composes provider work. No contradiction between owners was found; the prose-level findings are OBS44-04..08.') % INV_ROWS_EQUAL,
     'evidence': {'protocol3ChangedKeys': p3_changed_keys, 'inventoryRowsEqual': INV_ROWS_EQUAL, 'deltaPaths': sorted(paths43to44)}},
    {'id': 'CH44-PINS-AND-REPORTS', 'disposition': 'CONFIRMED',
     'assessment': ('Every entry of the five ledgers matches the formal manifest (foundation %d, evaluator3 %d, native %d, security %d, workflows %d). The union of changed pins is 16 files (the changed native, foundation and contract owners and the sibling ledgers), 5 new provider files are added, and none is removed. '
                    'The delta files pinned by no ledger are the planning records, layout and build plan, the generated native and workflows reports, and the evaluator3 ledger itself. The workflows report updates only the workflows source-pins digest, and the native report is the generated run of the 477-case checker. The evaluator3 pins sha equals the codex currentProfilePinsSha256 (%s).')
     % tuple([PINS['ledgers'][l]['entries'] for l in (FD + 'source-pins.v1.json', FD + 'evaluator3-source-pins.v1.json', NAT + 'source-pins.v2.json', DC + 'security/source-pins.v1.json', WFD + 'source-pins.v1.json')]
             + [CODEXD.get('currentProfilePinsSha256') == PINS['ledgers'][FD + 'evaluator3-source-pins.v1.json']['ledgerSha256']]),
     'evidence': {'changedPinUnion': PINS['changedPinUnion'], 'addedPinUnion': PINS['addedPinUnion'], 'deltaFilesPinnedByNoLedger': PINS['deltaFilesPinnedByNoLedger']}},
    {'id': 'CH44-PLANNING-V12', 'disposition': 'CONFIRMED WITH ADVISORY ADV44-01 (population measured; predecessors preserved)',
     'assessment': ('v12 (%s...) binds %d inputs with no mismatch: the 31 v11 inputs with native-evidence.md updated, plus provider-handshake, provider-startup and typescript-protocol2-order. All %d coverage sources are bound and none is stale. Layers v8-v11 are byte-identical to source43, the planning sources select v12 with v11 as previous and the prior-layer history digests match, and both operations checkers are byte-identical. '
                    'The planning checker reports 322 source-bound mappings and 54 planned failure cases, and the inventory checker 198 unique paths in 20 packages (stdout text equal to the root companion checks: %s). Mapping ids are unchanged; the 15 native-evidence rows changed only their source digests. There are 24 report features, M0-M6, and 54 recovery cases, none executed. '
                    'The six changed architecture files are the planning records, layout 14, the build plan and the inventory decision sentence. The protocol3 table and fact-batch v3 remain unbound (ADV44-01).')
     % (PC['layerSha256']['12'][:12], PC['layerInputs']['12'], PC['coverageSourceKeys'], planning_stdout_equal_companion),
     'evidence': {k: PC[k] for k in ('layerSha256', 'layerInputs', 'priorLayersByteEqualToSource43', 'v12AddedVsV11', 'v12ChangedVsV11', 'v12RemovedVsV11', 'coverageMappings', 'coverageMappingsSource43',
                                     'coverageRowsChangedVs43', 'coverageGroups', 'inventoryPaths', 'inventoryPackages', 'recoveryCases', 'recoveryCasesNotExecuted', 'milestoneOrder',
                                     'architectureDirFilesChangedVs43', 'planningSourcesHistoryCount', 'operationsCheckersByteEqualToSource43')}},
    {'id': 'CH44-PACKAGE21', 'disposition': 'VERIFIED AS AUTHOR EVIDENCE; RUNIDS UNCHANGED (MEASURED)', 'assessment': 'See packageAssessment.', 'evidence': {k: v['ok'] for k, v in PK.items()}},
    {'id': 'CH44-CURRENT-REFERENCE', 'disposition': 'OWN EXECUTION PASSES; ROOT RECEIPTS CONSISTENT',
     'assessment': ('This review\'s six groups and 17 children pass on its own verified copy, unchanged before and after every group. Native reports 477/477 cases, query-projection 209 checks with 0 failed, execution-inputs 95 cases and enumeration 54. '
                    'The comparison with root and codex is OBS44-01 and OBS44-02. This origin\'s historical source43 receipts are preserved and not relabelled.'),
     'evidence': {k: RC[k] for k in ('codexReferenceChecks', 'codexPassed', 'codexSubjectManifestSha256', 'rootPassed', 'childrenEqualRoot', 'childrenDifferingFromHistoricalMine43')}},
]

# ------------------------------------------------------------------------------------------------ scope basis (source43 scope retained)
UNCH43 = ['CH43-AVAILABILITY-REPORTING', 'CH43-OBSERVATION-GRANTS-NOTHING', 'CH43-PATH-EDGE-ORIENTATION', 'CH43-CURSOR-BOUNDS-AND-PROSE']
ch = lambda n: {'stdoutEqualRoot': RC['children'][n + '.stdout']['equalRoot'], 'stdoutEqualHistoricalMine43': RC['children'][n + '.stdout']['equalHistoricalMine43']}
SCOPE_BASIS = [
    {'scope': 'five product contracts and incorporated schemas', 'basis': 'new-44 (native) + unchanged-43-basis (others)',
     'current44': ('identity, security, workflows and admission contracts and the README index are byte-identical (%s). native-evidence changed only in the section intro (:78-85), section 0 rows, sections 9.1-9.7 and section 12; it was read completely for sections 0 and 9 plus the complete diff, and the new schema documents were read completely. All six groups pass.')
     % json.dumps({k: U[k] for k in ('identity-and-evidence.md', 'security-and-lifecycle.md', 'workflows-and-surfaces.md', 'admission-and-qualification.md', 'README.md')}),
     'unchanged43': 'source43 AR row assessments for the byte-identical contracts; inheritedUnchanged43Read whole-file reads'},
    {'scope': 'architecture, tool, layout and report decisions', 'basis': 'new-44', 'current44': '%d docs/v2/architecture files: 6 changed (planning records; one handshake decision sentence in layout 14, build plan and inventory, all read as complete diffs); planning and inventory checks pass' % PC['architectureDirFileCount'], 'unchanged43': None},
    {'scope': '198 files in 20 packages; 322 mappings; M0-M6; 24 report features; 54 recovery cases', 'basis': 'current execution', 'current44': 'measured: %d paths, %d packages (file and package rows identical to source43: %s), %d mappings (ids unchanged; 15 native-evidence source digests), %s, %d report features, %d recovery cases not executed' % (PC['inventoryPaths'], PC['inventoryPackages'], INV_ROWS_EQUAL, PC['coverageMappings'], '-'.join([PC['milestoneOrder'][0], PC['milestoneOrder'][-1]]), PC['coverageGroups']['reportFeatures'], PC['recoveryCasesNotExecuted']), 'unchanged43': None},
    {'scope': 'native discovery, config, unitKind, allowJs, nested Cargo, clone normalization, custody', 'basis': 'new-44 + current execution',
     'current44': 'native_evidence_model changed only by two appended regions (wire loader :573-590; startup section :4557-4701), so no discovery/config/unitKind/allowJs/Cargo/clone/custody code changed; native group 477/477; native-consumer24-corrections %s and native-replay %s; ported native (%d rows) and custody (%d rows) identical to source43; empty dependency custody measured; nine native-v2 membership probes content-equal to root' % (ch('native-consumer24-corrections'), ch('native-replay'), PORTED_EQUAL['P44-PORTED-NATIVE']['rows'], PORTED_EQUAL['P44-PORTED-CUSTODY']['rows']),
     'unchanged43': 'source43 AR-07/AR-13 assessments of the unchanged sections; OBS42-02'},
    {'scope': 'enumeration default-vs-explicit binding, attribution and capture', 'basis': 'unchanged-43-basis + new-44 diff + current execution',
     'current44': 'enumeration owners byte-identical; execution-inputs contract/model changed only in historical FactBatch naming; enumeration (54) and execution-inputs (95) children equal root after removing path fields only; against own source43 the enumeration child is path-only equal and the execution-inputs cases are identical (only the echoed owned-file digests and note string differ); capture-join measurement identical; package binding-controls content-equal to root',
     'unchanged43': 'CH42-ATTRIBUTION-LAW, CH42-CAPTURE, CH42-PROGRAM-ENTRY-CLARIFICATION, CH42-PROGRAM-ENTRY-ENFORCEMENT and CH42-HISTORICAL-POPULATIONS as carried by the source43 review on unchanged code'},
    {'scope': 'policy.test known-hit, universe and import', 'basis': 'unchanged-43-basis + current execution', 'current44': 'ported policy probe %d rows identical (copy identity row aside); policy-derivation child %s' % (PORTED_EQUAL['P44-PORTED-POLICY']['rows'], ch('policy-derivation')), 'unchanged43': 'policy_test_model.v3.py unchanged (%s); S39-01/S39-02 closed' % U['policy_test_model.v3.py']},
    {'scope': 'comparison counterfactuals, knowledge and identities', 'basis': 'unchanged-43-basis + current execution', 'current44': 'ported comparison probe %d rows identical; comparison-knowledge child %s' % (PORTED_EQUAL['P44-PORTED-COMPARISON']['rows'], ch('comparison-knowledge')), 'unchanged43': 'source43 AR-10/AR-11'},
    {'scope': 'nine command carriers and twenty operations', 'basis': 'unchanged-43-basis + current execution', 'current44': 'ported query carriers %d rows identical; query-projection 209 checks pass; command-inventory unchanged (%s)' % (PORTED_EQUAL['P44-PORTED-QUERY']['rows'], U['command-inventory.v3.json']), 'unchanged43': 'CH43 query items on byte-identical query owners'},
    {'scope': 'repair2', 'basis': 'unchanged-43-basis + current execution', 'current44': 'ported repair:2 probe %d rows identical' % PORTED_EQUAL['P44-PORTED-REPAIR2']['rows'], 'unchanged43': 'repair_closed_world_selection.v1.py unchanged (%s)' % U['repair_closed_world_selection.v1.py']},
    {'scope': 'security, discovery, commit, recovery and read-only carrier boundaries', 'basis': 'unchanged-43-basis + current execution',
     'current44': 'security group stdout equal root and own source43; ported read-only carrier %d rows and run-termination/commit-inventory %d rows identical' % (PORTED_EQUAL['P44-PORTED-CARRIER']['rows'], PORTED_EQUAL['P44-PORTED-RUNTERM']['rows']),
     'unchanged43': 'carrier-dispatch.v3.json (%s) and commit-recovery-readonly.v3.md (%s) unchanged; ADV38-02/ADV38-03' % (U['carrier-dispatch.v3.json'], U['commit-recovery-readonly.v3.md'])},
    {'scope': 'evaluator, import and termination bridges', 'basis': 'unchanged-43-basis + current execution',
     'current44': 'children full-replay %s, execution-replay %s, candidate-replay %s, composition %s, analysis-seal %s, provider-attribution-return %s (unchanged despite the gate label), faults %s, atoms %s; ported section 7 termination %d rows identical'
                  % (ch('full-replay'), ch('execution-replay'), ch('candidate-replay'), ch('composition'), ch('analysis-seal'), ch('provider-attribution-return'), ch('faults'), ch('atoms'), PORTED_EQUAL['P44-PORTED-TERM7']['rows']),
     'unchanged43': 'CH42-COMPOSITION7-AND-POLICY-DERIVATION3 and CH42-IDENTITY-DIGEST-SCOPE on byte-identical owners (composition %s, replay %s, identity model %s)' % (U['evaluator-composition-contract.v3.md'], U['evaluator_replay_model.v3.py'], U['identity-model.v3.py'])},
]
UNCHANGED43_ITEMS = [{'id': i, 'source43Disposition': V43ITEMS[i]['disposition'], 'standsOnSource44': True,
                      'note': 'Query owners named by the source43 item are byte-identical 43->44 (%s); the conclusion is this origin\'s source43 assessment, not a new read.' % json.dumps(QOWN)} for i in UNCH43 if i in V43ITEMS]
for i in UNCH43:
    if i not in V43ITEMS:
        GAPS.append('source43 item not found: ' + i)
ITEMS.append({'id': 'CH44-SCOPE-PRESERVATION', 'disposition': 'SOURCE43 SCOPE RETAINED; NAMED BASIS',
              'assessment': 'Each retained scope names its current source44 execution and, where applicable, its individually named unchanged-43 basis. Passing suites are corroboration, not assessment. Provider changes reach native sections 0/9/12 and the occupancy, execution-inputs and attribution texts, which are assessed by CH44 items and new-44 rows even where executable owners are unchanged.',
              'scopeBasis': SCOPE_BASIS, 'unchanged43Items': UNCHANGED43_ITEMS, 'portedProbes': PORTED_EQUAL})
