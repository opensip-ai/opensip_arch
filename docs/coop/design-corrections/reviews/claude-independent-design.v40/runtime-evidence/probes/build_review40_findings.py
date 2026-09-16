# Executed by build_review40.py in its own globals (exec). Findings, advisories, observations, item dispositions, F rows and
# the 30 evaluation-residual rows.

VDOBS = VDB['reference-attribution-of-the-two-producer-and-universe-matched-views']['observed']
VDFOUR = VDB['a-manifest-attributing-every-view-of-this-cell-program-U-producer']['observed']
VDRET = VDC['host-records-V_decl-as-returned-in-receipt-and-selectedRefs-on-no-row']['observed']
S40_01_DEMONSTRATED = (VDOBS == {'attributedRows': {'V_file': [[0, 'inventory']], 'V_decl': []}, 'inSelectedRefs': {'V_file': True, 'V_decl': False}}
                       and VDFOUR.get('result') == 'REFUSE' and 'EXECUTION_INPUTS_VIEW_TOTALITY' in (VDFOUR.get('refusals') or [])
                       and VDRET.get('result') == 'ADMIT' and VDRET.get('differsFromReferenceEncoding') is True and VDRET.get('storePointers') == 'promised_pointers'
                       and VDB['reference-rebuild-admits']['observed']['result'] == 'ADMIT' and VDC['control-reference-rebuild-admits']['observed']['result'] == 'ADMIT')
if not S40_01_DEMONSTRATED:
    GAPS.append('S40-01 measurements are not as recorded in the finding text')
if not EI_OWNER_UNCHANGED:
    GAPS.append('execution-inputs owner changed 39->40; S40-01 pre-existing statement is wrong')

SHOULD = [{
    'id': 'S40-01', 'severity': 'SHOULD',
    'title': 'Which returned views a cell/program row attributes (CellProgramOutcomeV1.viewDigests), and therefore stage-receipt outputRefs and selectedRefs, has no published recipe; the reference applies an unpublished capability-relation criterion, and two conforming encodings of the same stage returns both admit with different ExecutionInputsV1 digests',
    'selectors': [
        'docs/coop/design-corrections/foundation/execution-inputs.schema.v1.json:621 (viewDigests: "Must equal captured receipt views attributed to this cell/program/U/producer"; the only statement of the attribution, and "attributed" is not defined)',
        'docs/coop/design-corrections/foundation/execution-inputs-contract.v1.md:12-19 (section 1: the record is a host TCB observation of stage returns; stage-produced selectedRefs = union of complete receipt outputRefs; coverage = coverageIds of "those captured returned views")',
        'execution-inputs-contract.v1.md:51 (section 3 joins: enumerator closure, stage producerClosure, view planId, named scope sourceUniverse, receipt outputDomains; no relation or capability criterion)',
        'execution-inputs-contract.v1.md:114 and :219-231 (section 5 derives accounts from "this cell/program\'s returned views" and resolves "the views THAT cell/program returned, restricted to the binding\'s own enumerator/provider closure": it presupposes the attribution rather than defining it)',
        'execution-inputs-contract.v1.md:141-144 (a competing internally consistent rule is "exactly why the normative one is published here instead of living only in the reference implementation") and :152-158 (precedent: two admissible encodings gave conforming hosts different ExecutionInputsV1 digests, proofs and Run ids, and were closed)',
        'execution-inputs-contract.v1.md:294 (build_manifest: "selectedRefs = attributed views + ...", again undefined)',
        'docs/coop/design-corrections/foundation/execution_inputs_model.v1.py:1129-1159 (admission: a view is attributed to a row iff same producer, same Plan, some scope at binding U, and some scope relation in the cell capability matrix relations, or any such view for a capability without matrix relations; exact equality else EXECUTION_INPUTS_VIEW_TOTALITY)',
        'docs/coop/design-corrections/foundation/execution_inputs_fixture.v3.py:226-244 and :342-388 (the host-capture builder applies its own copy of the relation criterion and derives stage-receipt outputRefs from the attributed views)',
        'docs/coop/design-corrections/foundation/enumeration-contract.v1.md:17 (one cell per requested capability tuple, so a program of one language mode and workspace carries several capability cells bound to the same provider and universe; seen in search output) and native-capability-matrix.v2.json (inventory relations file/package/vcs-change; syntax declares/literal/control-flow; script-extracted)',
    ],
    'measured': {
        'executionInputsOwnerBytesUnchanged39to40': EI_OWNER_UNCHANGED,
        'maintainedOwnerGraphRows (cellOrdinal, programOrdinal, capabilityId)': {k: [(r['cell'], r['program'], r['capability']) for r in VD[k]['observed'].get('rows', [])] for k in ('one-universe-owner-admits', 'missing-package-owner-admits', 'two-universes-owner-admits')},
        'contractTextNamesViewDigests': VD['source-text-execution-inputs-contract-names-viewDigests']['observed'],
        'referenceAttributionOfMintedViews': VDOBS,
        'manifestAttributingEveryViewOfThisCellProgramUProducer': VDFOUR,
        'hostRecordingTheReturnedViewInReceiptAndSelectedRefsOnNoRow': VDRET,
    },
    'detail': ('Into the maintained one-universe owner graph (one inventory cell) the probe minted two views returned by the binding\'s own producer for its own Plan, each with one subject-scope at the binding universe: V_file (relation file, an inventory relation) and V_decl (relation declares, not one). '
               'Rebuilt through the maintained host-capture builder, the reference attributes V_file to the inventory row and V_decl to no row, leaves V_decl out of the stage receipt and selectedRefs, and admits. '
               'A manifest naming every view of this cell/program/U/producer on the row, which is the literal schema sentence, is refused EXECUTION_INPUTS_VIEW_TOTALITY. '
               'A manifest recording V_decl as what the stage returned (receipt outputRefs and selectedRefs, per section 1) on no row, with store pointers recomputed by promised_pointers as section 2 requires, also admits, and its raw digest differs from the reference encoding. '
               'So for identical stage returns two admissible ExecutionInputsV1 records exist, giving different executionInputsDigest values and therefore different Run identities; section 5 closed exactly this class for targetUniverse. '
               'No contract or schema text states the deciding criterion (a scope relation among the cell capability\'s matrix relations), whether a view may be attributed to several rows, what a returned view that matches no requested cell does to the receipt and selectedRefs, or the rule for capabilities without matrix relations. '
               'Lawful plans reach the case: a program carries one cell per requested capability, all bound to the same provider and universe, so returned views must be divided among rows by some rule. No maintained control has more than one capability cell per program, so the passing suites cannot expose it. '
               'The execution-inputs owner bytes are unchanged 39->40, so this is a pre-existing gap. This origin\'s source39 review read the contract completely and did not find it; the charter\'s narrow question and a reviewer-minted graph found it now.'),
    'consequence': 'An implementation written from the published law alone can mint a manifest that a conforming verifier refuses, or one that is admitted under a different RunId than another conforming host\'s for the same analysis. Retained Run identity is therefore not reproducible from published law.',
    'requiredChange': ('Publish the attribution law in execution-inputs contract sections 1, 3 and 5 and align the schema description: '
                       '(1) the predicate attributing a returned view to a cell/program row, including the capability-relation criterion; (2) whether one view may be attributed to several rows; '
                       '(3) the treatment of a returned view matching no requested cell, and whether stage-receipt outputRefs are the observed returns or only attributed views; (4) the rule for capabilities without matrix relations. '
                       'Make builder and admission implement that single stated predicate so exactly one encoding admits, and add controls with two capability cells on one program, a view shared by both, and a returned view matching neither.'),
    'owner': 'foundation execution-inputs owner (execution-inputs-contract.v1.md, execution-inputs.schema.v1.json, execution_inputs_model.v1.py, execution_inputs_fixture.v3.py, check-execution-inputs.v1.py); planned host capture module crates/host/src/analysis.rs (inventory path, not present in the snapshot)',
    'receipts': ['receipts/probes/viewdigests-v40b.json', 'receipts/probes/viewdigests-v40c.json', 'receipts/probes/viewdigests-v40.json']}]

ADVISORIES = [{
    'id': 'ADV40-01', 'severity': 'EDITORIAL',
    'title': 'The added implementation-normative-inputs.v8.json is a superseded mid-integration layer that binds native-evidence.md bytes present in no frozen subject, under the same standing text as the current layer',
    'selectors': ['docs/v2/architecture/implementation-normative-inputs.v8.json (read complete; standing identical to v9)', 'docs/v2/architecture/implementation-planning-sources.v1.json (diff read; previous layer v8, current v9)'],
    'measured': {'v8Sha256': PC['v8Sha256'], 'v8InputsNotCurrent': PC['v8InputsNotCurrent'], 'v9Sha256': PC['v9Sha256'], 'v9Mismatched': PC['v9Mismatched']},
    'detail': ('v8 differs from v9 in run-termination-contract.v1.md (source39 bytes) and native-evidence.md (a digest matching neither the source39 nor the source40 bytes). Its standing still reads as exact normative inputs consumed by implementation planning. '
               'v9, coverage and planning sources bind current bytes and the planning checker passes, so planning is consistent; a reader of v8 alone could take an unfrozen integration state for a frozen input layer.'),
    'disposition': 'EDITORIAL at the next successor: mark v8 superseded (or name the unfrozen bytes it binds). Non-blocking.', 'receipt': 'receipts/planning-checks.json'}]

g1 = POL['observation-optional-imported-evidence-available-without-a-row-is-a-blocking-fixture-unknown']['observed']
n3 = NAT['observation-full-run-N3-consistent-mode-and-kind-remint-over-a-jsconfig-false-marker']['observed']
n1 = NAT['full-run-source40-N1-jsconfig-false-published-closes']['observed']
OBSERVATIONS = [
    {'id': 'OBS40-01', 'text': 'policy test: a rule with missing required evidence is listed in indeterminateRules even when a known gating finding makes the verdict fail (production rule outcome fail). Section 5 now states this (workflows-and-surfaces.md:671-673); CaseResult.indeterminateRules names rules without a per-rule cause. An advisory rule with a known hit displays verdict advisory where production passes.', 'receipt': 'receipts/probes/policy-v40.json'},
    {'id': 'OBS40-02', 'text': 'policy test fixture representation limit: optional imported evidence that is available but has no matching row is a blocking fixture unknown (verdict %s), while the same rule with the evidence absent passes (%s) and bounded production composition of an optional-only unknown passes (%s). The ruleLaw names a representation limit as blocking, while composition section 5 lets optional-only unknowns pass, so the fixture is conservative and disclosed and never gives a false pass.' % (g1['fixtureAvailableNoRow'], g1['fixtureAbsent'], json.dumps(g1['productionOptionalOnlyUnknown'])), 'receipt': 'receipts/probes/policy-v40.json'},
    {'id': 'OBS40-03', 'text': 'policy show resolves and reports: it accepts a PolicyDocumentV2 carrying an unregistered universe token, and its EffectivePolicyRecordV1 is schema-valid on both byte sets, while policy test refuses POLICY.UNKNOWN_RULE. No stated law makes show perform test or analysis admission, so this is not a violation; showing a policy that analysis would refuse is a presentation limit.', 'receipt': 'receipts/probes/policy-v40.json'},
    {'id': 'OBS40-04', 'text': 'U-4b.2 trusted-host scope: remint BOTH languageMode and unitKind consistently over a jsconfig allowJs:false marker and the full Run still closes, with a different RunId (%s versus %s for the published unit). Closure checks kind against mode and re-derives membership from the supplied marker observations; the effective allowJs is the trusted pre-Plan marker observation (native section 1.2), not something closure re-derives from bytes. Measured on the syntax-universe fixture, which has no tsjs program cell.' % (n3['source40'].get('runId'), n1.get('runId')), 'receipt': 'receipts/probes/native-v40.json'},
    {'id': 'OBS40-05', 'text': 'U-1 omitted value: discover_units reads an omitted tsconfig allowJs observation as false, while typescript_mode derives true from checkJs. Native section 1.2 requires the marker observation to carry the effective value, so a host must supply allowJs=true for a checkJs-derived configuration; the model default is not a second law.', 'receipt': 'receipts/probes/native-v40.json'},
    {'id': 'OBS40-06', 'text': 'Nested Cargo: an explicitly named member root beside its explicit workspace root is folded (explicit a and a/b/c give one a workspace unit with members a/b and a/b/c), matching the retained explicit-root case. Marker observations do not prove that Cargo accepts a nested-workspace layout, as the native case note states.', 'receipt': 'receipts/probes/native-v40.json'},
    {'id': 'OBS40-07', 'text': 'execution-inputs reference: the scope-level enumeratorClosure test is the last statement of the attribution loop body, so its continue decides nothing (attribution already filters views by producer). Dead code with no behavioural effect.', 'receipt': 'receipts/probes/viewdigests-v40.json'},
    {'id': 'OBS40-08', 'text': 'Against the codex final-reference.v40 run: all six group stdouts byte-equal: %s; %d of 17 evaluator3 child stdouts byte-equal. enumeration and execution-inputs differ only in absolute copy paths inside ownedHashes and receiptPath.' % (all(v['stdoutEqual'] for v in RC['groups'].values()), RC['childrenEqual']), 'receipt': 'receipts/reference-comparison.json'},
    {'id': 'OBS40-09', 'text': 'Re-observed on unchanged bytes by the ported source39 probes: one broad installPath row authorizes every top-level package; a case-variant node_modules segment stays first-party; a hidden candidates suppressedCount cannot be joined from the query record; a trusted retained view may declare any unavailability class; admit_repair_plan_v2 is schema and identity admission.', 'receipt': 'receipts/probes (ported probe receipts)'},
    {'id': 'OBS40-10', 'text': 'Correction of this origin\'s source39 narrative. TOPIC-V7-PLANNING said the mapping population was preserved, but that review\'s own evidence recorded 320 in source38 and 322 in source39 (workflow goldens 43 to 45), so source39 changed the population. Source40 measures 322, equal to source39: 22 rows were rebound to changed selectors, none added or removed.', 'receipt': 'receipts/planning-checks.json'},
]


def pick(rows, *prefixes):
    return {k: v['observed'] for k, v in rows.items() if k.startswith(prefixes)}


ITEMS = [
    {'id': 'S39-01', 'origin': 'claude-independent-design.v39 SHOULD', 'prior39Disposition': 'OPEN-SHOULD', 'disposition': 'CLOSED-AT-SOURCE-LEVEL',
     'selectors': ['docs/coop/design-corrections/workflows/policy_test_model.v3.py:230-255 (every selected subject evaluated; required-absent is a rule-level blocking deficiency; a known true root still emits and fails)',
                   'docs/v2/contracts/product-v1/workflows-and-surfaces.md:644-647 and :671-673', 'docs/coop/design-corrections/workflows/schemas/evaluator3/policy-test.schema.json (ruleLaw; read complete)',
                   'docs/coop/design-corrections/foundation/evaluator-composition-contract.v3.md:36 and section 5 (optional-only root unknown passes)'],
     'evidence': pick(POL, 'S39-01', 'source40-fixture-verdict', 'optional-missing'),
     'assessment': ('Source39 bytes lose the known hit (verdict indeterminate, no finding). On source40 bytes the fixture equals bounded production composition on verdict and finding presence in all six discriminating cases: '
                    'the or-rule cases (required evidence missing, optional missing, required present) all fail, and the known-false-root case under missing required evidence, the waived hit and the no-subjects case are all indeterminate. '
                    'Required absence lists the rule in indeterminateRules and optional absence does not, so required and optional evidence are distinguished. Suite and result identities are H/policytest2 over the suite, and the same suite gives the same bytes.')},
    {'id': 'S39-02', 'origin': 'claude-independent-design.v39 SHOULD', 'prior39Disposition': 'OPEN-SHOULD', 'disposition': 'CLOSED-AT-SOURCE-LEVEL',
     'selectors': ['docs/coop/design-corrections/workflows/workflows_model.v3.py:279-289 (resolver refusal POLICY.UNKNOWN_RULE, remedy EVALUATOR_POLICY_UNIVERSE_UNREGISTERED)',
                   'docs/coop/design-corrections/workflows/policy_test_model.v3.py:37 (POLICY_UNIVERSES from identity-schemas policyUniverseMap), :71 (fact token), :76-79 (rule tokens), :132 (imported occupancy joins subject and universe)',
                   'docs/v2/contracts/product-v1/workflows-and-surfaces.md:660-671', 'docs/coop/design-corrections/workflows/policy-test-cases.v3.json (diff read; authored tokens registered)'],
     'evidence': pick(POL, 'S39-02', 'source40-typescript', 'source40-disabled', 'source40-fixture-fact', 'every-registered', 'source39-foreign', 'source40-foreign', 'same-universe', 'foreign-universe-native'),
     'assessment': ('Unregistered rule tokens, including one on a disabled rule, are resolver refusals POLICY.UNKNOWN_RULE; an unregistered fact token is admission CONFIG.INVALID; the three registered tokens admit with equal outcomes. '
                    'A foreign-universe imported row created a known hit on source39 bytes and creates none on source40. The same-universe control fails on both byte sets, and a foreign native fact occupied on neither. '
                    'The six-file correction is discriminated against the old bytes in separate processes. The policy show acceptance is OBS40-03, not a violation.')},
    {'id': 'ADV39-01', 'origin': 'claude-independent-design.v39 ADVISORY', 'prior39Disposition': 'ROUTE-TO-NATIVE-OWNER', 'disposition': 'CLOSED-BY-EXPLICIT-TRUTHFUL-ACCOUNT',
     'selectors': ['docs/v2/contracts/product-v1/native-evidence.md:3113-3124'],
     'evidence': pick(RTA, 'registered-native', 'source38-and', 'publicD9', 'only-Resolved', 'registry-registers', 'rebuilt-reference'),
     'assessment': ('Every factual statement of the new paragraph was measured. The annotation bytes are unchanged 38 to 40; the only JSON difference is the ResolvedNodeModulesLayoutV1 description; the digests are exactly 3e37c7b7... and 2d37b810...; '
                    'the registry registers only the latter and the rebuilt exports consume it; the registered bytes are unchanged 39 to 40. The paragraph calls this a prerelease document revision and re-registration and grants no cross-profile replay or migration acceptance, which is what the advisory asked for.')},
    {'id': 'ADV38-01', 'origin': 'claude-independent-design.v38 ADVISORY', 'prior39Disposition': 'CLOSED-AT-SOURCE-LEVEL', 'disposition': 'REMAINS CLOSED',
     'selectors': ['docs/coop/design-corrections/foundation/run-termination-contract.v1.md section 7 (read complete; 39->40 edits confined to sections 3, 6 and 7.3 prose)', 'run_termination_model.v1.py (unchanged 39->40: %s)' % U['run_termination_model.v1.py']],
     'evidence': PBY['P40-PORTED-TERM7'].get('result'), 'assessment': 'The section 7 composition admission and closed detail allowlist are unchanged in substance, and the ported probe passes over golden Runs on source40.'},
    {'id': 'ADV38-02', 'origin': 'claude-independent-design.v38 ADVISORY', 'prior39Disposition': 'CLOSED-AT-SOURCE-LEVEL', 'disposition': 'REMAINS CLOSED',
     'selectors': ['%s (unchanged 39->40: %s)' % (CD, U.get('carrier-dispatch.v3.json'))], 'evidence': PBY['P40-PORTED-CARRIER'].get('result'),
     'assessment': 'The read-only carrier route bytes are identical and every tabulated scenario still matches on source40.'},
    {'id': 'ADV38-03', 'origin': 'claude-independent-design.v38 ADVISORY', 'prior39Disposition': 'CLOSED-AT-SOURCE-LEVEL', 'disposition': 'REMAINS CLOSED (basis inherited, bytes unchanged)',
     'selectors': ['%s (unchanged 39->40: %s)' % (CR, U.get('commit-recovery-readonly.v3.md'))], 'evidence': {'unchanged39to40': U.get('commit-recovery-readonly.v3.md')},
     'assessment': 'The source39 whitespace-normalized measurement of the corrected phrases stands on byte-identical bytes; not re-measured.'},
    {'id': 'CHARTER-U4B-UNITKIND', 'origin': 'source40 charter', 'disposition': 'CONFIRMED WITH FULL RUN CLOSURE (trusted-host scope in OBS40-04)',
     'selectors': ['docs/v2/contracts/product-v1/native-evidence.md:733-804 (U-4b; unitKind at :755-760; enforcement U-4b.5)', 'docs/coop/design-corrections/native/native_evidence_model.v2.py:3764 (TSJS_UNIT_KIND), :3951-3957',
                   'docs/coop/design-corrections/foundation/enumeration_model.v1.py:536-559 (diff read)'],
     'evidence': pick(NAT, 'full-run', 'observation-full-run'),
     'assessment': ('Published kinds close full Runs. A digest-consistent reminted kind (N2), a rust unit carrying js-program (N4) and a tsjs unit carrying cargo-package (N5) each refuse at full closure with EVALUATOR_ENUMERATION_JOIN:ENUMERATION_MEMBERSHIP_ORDER, and all three close on source39 bytes. '
                    'Discovery and admission share one closed projection table. The one thing closure cannot check is the effective allowJs behind a consistent mode-and-kind remint (OBS40-04), which is the stated trusted marker observation.')},
    {'id': 'CHARTER-U1-ALLOWJS', 'origin': 'source40 charter', 'disposition': 'CONFIRMED (identity consequence measured)',
     'selectors': ['native-evidence.md:652-662 (U-1)', 'native-evidence.md:516-535 (section 1.2 effective allowJs)', 'native-evidence.md:162-163 (mode table)', 'native_evidence_model.v2.py:3951-3953 (discovery), :2207-2224 (typescript_mode)'],
     'evidence': pick(NAT, 'U-1', 'identity-consequence', 'section-1.2', 'observation-marker'),
     'assessment': ('jsconfig omitted or true selects js-allowjs, explicit false selects ts-tsconfig, tsconfig takes precedence, and package-only synthesizes; the source39 model read explicit jsconfig false as js-allowjs. '
                    'For a jsconfig allowJs:false project the membershipDigest (a PlanId input) differs between the models: a prerelease identity change, consistent with the corrected law. The omitted-value default is OBS40-05.')},
    {'id': 'CHARTER-NESTED-CARGO', 'origin': 'source40 charter', 'disposition': 'CONFIRMED (root and both coauthor edits carry controls, all executed)',
     'selectors': ['native-evidence.md:744-754 (U-4b.2 nested folding)', 'native_evidence_model.v2.py:3930-3941', 'check-enumeration.v1.py (diff read)', 'check-native-consumer24-corrections.v1.py (diff read; ranges 1-140 and 370-619 read)', 'native-cases.v2.json (diff read)'],
     'evidence': pick(NAT, 'U-4b.2', 'U-4a', 'U-4b.5', 'source39-baseline'),
     'assessment': ('Triple nesting, explicit outer, root plus inner, inner alone, a nested project boundary, a root package over a nested workspace, a package between workspaces and UTF-8 member order all match the source40 text. '
                    'Targets under folded member roots are pruned while src/target stays source, and dropping a folded member refuses row derivation. Source39 bytes raised StopIteration on triple nesting and on a package between workspaces. '
                    'The checker controls ran in this review\'s groups: enumeration %s cases with %s mismatches; native-consumer24 %s of %s; native group 388/388.' % (children['enumeration'].get('casesCount'), children['enumeration'].get('mismatchesCount'), children['native-consumer24-corrections'].get('passed'), children['native-consumer24-corrections'].get('total')))},
    {'id': 'CHARTER-RUN-TERMINATION', 'origin': 'source40 charter', 'disposition': 'CONFIRMED AGAINST THE UNCHANGED MODEL',
     'selectors': ['run-termination-contract.v1.md:83-87 (section 3), :170-180 (section 6), :246-256 (section 7.3)', 'run_termination_model.v1.py (unchanged 39->40: %s)' % U['run_termination_model.v1.py']],
     'evidence': pick(RTA, 'closed-candidate', 'delegated', 'check_projection', 'unexplained', 'run-termination-model', 'commit-inventory', 'a-non', 'an-extra'),
     'assessment': ('The named keys are the model\'s. errorCode, faultCause and signal are recognized fields that reach RUN_TERMINATION_NOT_DERIVED, and an unknown member refuses first. '
                    'The commit-inventory recipe, recomputed independently over a closed Run, equals the owner digest and canonical-set order and validates against the owning schema; a non-canonical order refuses and an extra object changes the digest. '
                    'Model, identity schemas and public registry are unchanged, so the clarifications add no public detail and no identity rule.')},
    {'id': 'CHARTER-ADVISORY-TOPICS', 'origin': 'source40 charter', 'disposition': 'ASSESSED; no contradiction demonstrated',
     'selectors': ['public-detail-registry.v1.json (unchanged; 315 codes)', 'native-evidence.md:3018 and :3031 (LIVE D9 not discharged; existing D9 codes only)', 'workflows-and-surfaces.md:403 (first-applicable indeterminateReason order)',
                   'workflows-and-surfaces.md:440, :475, :508 (evidence axis, single import identity, exact-snapshot correspondence)', 'native-evidence.md:166 and :172 (rust-cargo-prepared mode row), :1261-1263 (preparedResolution, preparedOutputSetId)'],
     'evidence': {'internalKeysNotPublic': RTA['internal-decision-keys-are-not-public-detail-codes']['observed']},
     'assessment': ('Private diagnostic spellings (EVALUATOR_POLICY_UNIVERSE_UNREGISTERED as remedy text under the registered POLICY.UNKNOWN_RULE, ENUMERATION_MEMBERSHIP_ORDER, RUN_TERMINATION_*) are not public codes. '
                    'The D9 successor remains the carried obligation (DR-007/DR-011-R08). An exact-snapshot import has one H identity over its wrapper, so a changed snapshot is a different import2 and an evidence-axis change, which comparison treats conservatively. '
                    'The first-applicable reason order publishes exactly one reason per entry and, by design, makes later reasons unreachable for that entry. '
                    'The prepared-Rust mode row still selects through an admitted PreparedOutputSetV3 with non-null preparedOutputSetId after U-1 yields a unit, which the source40 unit-kind change (cargo kinds for rust) does not touch.')},
    {'id': 'CHARTER-SCOPE-PRESERVATION', 'origin': 'source40 charter', 'disposition': 'RE-EXECUTED ON SOURCE40',
     'selectors': ['receipts/probe-port.json'], 'evidence': {p['id']: {'rows': p['result']['rows'], 'failed': len(p['result']['failedRows'])} for p in PROBES if p['id'].startswith('P40-PORTED')},
     'assessment': 'Six source39 probes were ported with their expectations unedited (query carriers, read-only carriers, comparison knowledge, repair:2, section 7 composition, custody and fallback), and all pass on source40. Their owner bytes are unchanged 39->40 except check-workflow-projection, whose added controls run in the workflow-projection child (%s checks).' % children['workflow-projection'].get('count')},
    {'id': 'CHARTER-V9-PLANNING', 'origin': 'source40 charter', 'disposition': 'CONFIRMED (population measured, not inherited)',
     'selectors': ['implementation-normative-inputs.v9.json (read complete)', 'implementation-coverage.v1.json (diff read)', 'implementation-planning-sources.v1.json (diff read)'],
     'evidence': {k: PC[k] for k in ('v9Sha256', 'v9Inputs', 'v9Mismatched', 'v9BindsItselfOrItsBindingRecords', 'coverageSubjectMatchesV9', 'planningSourcesArchitectureSha256MatchesV9', 'coverageMappings',
                                     'coverageMappingsSource39', 'coverageGroups', 'coverageRowIdsAdded40', 'coverageRowIdsRemoved40', 'coverageRowsChanged40', 'inventoryPaths', 'inventoryPackages', 'recoveryCases', 'milestoneOrder')},
     'assessment': 'v9 binds 31 current inputs with no mismatch and no self-binding, and coverage and planning sources name v9. There are 322 mappings (24 report features, 45 workflow goldens), equal to source39, with 22 rows rebound and none added or removed; 198 paths in 20 packages; M0-M6; 54 recovery cases, none executed. OBS40-10 records the source39 narrative correction.'},
    {'id': 'CHARTER-PACKAGE17', 'origin': 'source40 charter', 'disposition': 'VERIFIED AS AUTHOR EVIDENCE (package15 constructors plus native-v2 overlay; package16 preserved; no relabel)',
     'selectors': [PKG + '/artifact-manifest.json', PKG + '/source-binding.v40.json', REBUILD], 'evidence': {k: v['ok'] for k, v in PK.items()}, 'assessment': 'See packageAssessment.'},
    {'id': 'CHARTER-CURRENT-REFERENCE', 'origin': 'source40 charter', 'disposition': 'OWN EXECUTION PASSES; HEADER RUN IS CONSISTENT EVIDENCE',
     'selectors': [CODEX, ROOTREF2], 'evidence': {k: RC[k] for k in ('codexReferenceChecks', 'codexPassed', 'codexSubjectManifestSha256', 'codexRunnerOriginalEqualsRootOriginal', 'childrenEqual')},
     'assessment': 'The header-named codex final-reference.v40 report hashes to 019c3397..., binds the source40 subject and passed; its runner-original equals root-source40-final-reference.v2. This review\'s own six groups and 17 children pass on its own verified copy and agree with it apart from path-only fields. The preliminary root source40 reference v1 predates final integration and was not used.'},
    {'id': 'NARROW-Q1-VIEWDIGESTS', 'origin': 'source40 charter narrow question', 'disposition': 'MISSING RECIPE (S40-01)', 'selectors': ['see S40-01'], 'evidence': {'see': 'S40-01'},
     'assessment': ('Already owned: producer closure, Plan, binding universe (per-scope sourceUniverse and the section 5 single-universe restriction), receipt outputDomains, coverage equality per (cell, program, relation, resolution, U, producer), and UNSUPPORTED-TYPED coverage handling. '
                    'Missing: how the selected receipt relates to the returned views (are receipt outputRefs the observed returns or the attributed views), the capability-relation criterion, sharing a view across rows, unmatched returned views, and capabilities without matrix relations. Two admissible encodings with different digests demonstrate the consequence.')},
    {'id': 'NARROW-Q2-COMPOSITION-S7-CLOSURE', 'origin': 'source40 charter narrow question', 'disposition': 'NO GAP',
     'selectors': ['evaluator-composition-contract.v3.md:70 (input admission precedes replay), :74 (output typed-reference closure), :76 (complete comparison, exact reachable output set)', 'evaluator-composition-contract.v3.md:93-109, :271, :317 (section 9 owner-specific equality addresses)'],
     'evidence': {'read': 'composition contract read complete this charter'},
     'assessment': ('Section 7 closes OUTPUT references: a typed-prefix identity field resolves and admits its descriptor in the prefix-selected domain, and subset comparison is forbidden. '
                    'Output fields that name admitted inputs (planId, evaluatorClosure, EI-derived view/coverage/import ids, policyDigest) are fixed by section 9 equality to inputs already admitted, because input admission precedes replay. '
                    'Resolving an admitted input again is idempotent and section 9 equality is the stronger law, so the two layers compose without conflict and leave no implementer choice.')},
    {'id': 'NARROW-Q3-POLICY-DERIVATION3', 'origin': 'source40 charter narrow question', 'disposition': 'CONSISTENT',
     'selectors': ['evaluator-composition-contract.v3.md:288 and :317 (section 9.7)', 'evaluator_replay_model.v3.py:86-107 (range read to end of file)'], 'evidence': {'read': 'contract complete; replay model lines 86-107 of 107'},
     'assessment': ('policy-derivation3 is exactly {schemaVersion, planId, proofBundleId, policyDigest, waiverDigest, verdict}, derived from a completely replayed Run\'s admitted Plan and seal and its recomputed proof, and a claim is admitted only by equality to that derivation. '
                    'It carries no runId, so it is a derived and admitted projection keyed by Plan and proof, not a Run back-reference; a different policy or waiver set needs its own Plan and Run.')},
]

# ------------------------------------------------------------------------------------------------ rows: F and residuals
V39ROWS = {r['id']: r for k in ('fDispositions', 'evaluationResidualDispositions', 'arDispositions', 'fwDispositions', 'inheritedResidualDispositions', 'scopedReviewOwnerDispositions') for r in v39[k]}
TCB_DEPS = ['RES-EP13-02', 'RES-EP13-04', 'RES-EP13-12', 'RES-EP13-13', 'RES-EP13-16', 'RES-EP13-18', 'IR-EP13-NB-01', 'IR-EP13-NB-03', 'IR-EP13-NB-04', 'AX6', 'AX9', 'MD5', 'RX2c']
N, I = 'new-40', 'inherited-unchanged-39'


def base_row(rid, basis, disposition, assessment, **extra):
    prior = V39ROWS.get(rid)
    if prior is None:
        GAPS.append('no source39 row for ' + rid)
    r = {'id': rid, 'prior39Disposition': prior['disposition'] if prior else None, 'disposition': disposition, 'assessmentBasis': basis, 'assessment': assessment}
    r.update(extra)
    r.update(appliedByThisReview=False, finalApplicationOutcomeGranted=False)
    return r


F_ROWS = []
for i in range(1, 15):
    rid = 'F-%02d' % i
    st = V39ROWS[rid]['priorRootStanding']
    F_ROWS.append(base_row(rid, I, 'CARRIED-NOT-REGRADED',
                           '%s: identifier and prior root standing %s (root-independent36-completion-assessment.v1) carried. The F record lives outside the snapshot and is not re-derived; none of the 24 delta files is an F record. The prior standing is not source40 acceptance.' % (rid, st),
                           priorRootStanding=st))

RES_TEXT = {
    'RES-EP13-01': (N, 'Plan and derivation joins stay inside complete replay. On source40, full Runs built by the maintained fixture close with published unit kinds and refuse reminted ones at closure (P40-NATIVE N2/N4/N5), and the full-replay child passes %s checks.' % children['full-replay'].get('count')),
    'RES-EP13-02': (N, 'Depends on TCB-SCOPE-01. The effective allowJs marker observation is trusted pre-Plan input: a consistent mode-and-kind remint closes with a different RunId (OBS40-04), so no answer-provenance claim against the host is made.'),
    'RES-EP13-03': (I, 'The seven-vector measurement stays finite history; admission-and-qualification.md (unchanged 39->40: %s) and the residual ledger (unchanged: %s) are byte-identical.' % (U['admission-and-qualification.md'], U['evaluation-residual-dispositions.proposed.json'])),
    'RES-EP13-04': (N, 'Depends on TCB-SCOPE-01. Closed input admission now also covers policy-test rule and fact universe tokens: unregistered rule tokens refuse POLICY.UNKNOWN_RULE and fact tokens CONFIG.INVALID (P40-POLICY).'),
    'RES-EP13-05': (N, 'The frozen subject was verified outside every author instrument: formal manifest, archive, all 12,911 members, parent39 and the exact 22/2/0 delta (P40-SUBJECT, P40-ARCHIVE).'),
    'RES-EP13-06': (N, 'canonical.py is outside the delta. The reviewer\'s own C()/H() reproduced policy-test suite and result identities for three authored suites and the commit-inventory digest over a closed Run (P40-POLICY, P40-RUNTERM-ADV).'),
    'RES-EP13-07': (I, 'Seal and replay owners are outside the delta, and the analysis-seal child passes on source40.'),
    'RES-EP13-08': (I, 'A bounded historical measurement; source40 claims no product proof over all PlanIntents.'),
    'RES-EP13-09': (N, 'Provenance stays distinct from correctness. Package semantic-controls1 keeps owner ADMIT and semantic REFUSE (content-equal to the root run), and a digest-consistent unit-kind remint closed on source39 but refuses on source40.'),
    'RES-EP13-10': (N, 'Author self-counters did not decide this review. S40-01 came from reviewer-minted graphs outside the maintained controls, which have one capability cell per program.'),
    'RES-EP13-11': (N, 'Failures stay recorded by cause. This review keeps its own run-termination attempt 1 defect and its view-attribution attempt 1 harness defect, and it does not use the preliminary root source40 reference v1 as current evidence.'),
    'RES-EP13-12': (N, 'Depends on TCB-SCOPE-01. No sole Python guard enters product authority; host stage-return capture (execution-inputs section 1) stays a TCB observation, and S40-01 concerns its determinism, not containment.'),
    'RES-EP13-13': (N, 'Depends on TCB-SCOPE-01. The probes restore the patched fixture helper and checker globals, run source39 and source40 sides in separate processes, and re-verify the probe copy after every run.'),
    'RES-EP13-14': (I, 'The differential census is not used as an oracle; unchanged.'),
    'RES-EP13-15': (N, 'The C-2 v4 self-census is not elevated. The enumeration model change adds the unit-kind projection to the membership law, which the enumeration child (tsjs unit-kind controls) and full Runs exercise, not a census.'),
    'RES-EP13-16': (N, 'Depends on TCB-SCOPE-01. Producer flags cannot bypass replay; unit kinds are re-derived at every enumeration admission, and run-termination class and reasons are derived from the sealed Run.'),
    'RES-EP13-17': (I, 'Text-only disclosures remain text-only.'),
    'RES-EP13-18': (N, 'Depends on TCB-SCOPE-01. Nested Cargo marker observations are trusted and do not prove Cargo accepts a layout (OBS40-06), and pruned-tree custody remains a host observation.'),
    'RES-EP13-19': (N, 'Substantive review with discriminating probes on both byte sets. All six pinned groups passed and a SHOULD was still found.'),
    'IR-EP13-NB-01': (N, 'Depends on TCB-SCOPE-01. Every probe ran in-process with owner modules; containment is not claimed.'),
    'IR-EP13-NB-02': (N, 'No name scan decides scope. Unit kind and universe tokens are closed tables, and imported occupancy compares subject and universe values, not spellings.'),
    'IR-EP13-NB-03': (N, 'Depends on TCB-SCOPE-01. Loaded owner instances stay reachable in-process, and the trusted marker observation (OBS40-04) is exactly why the boundary is trust.'),
    'IR-EP13-NB-04': (N, 'Depends on TCB-SCOPE-01; one TCB account covers all thirteen rows.'),
    'IR-EP13-NB-05': (N, 'Incomplete prose still needs substantive review: S40-01 is a schema sentence whose literal reading the reference refuses and whose gap admits two encodings, and every suite passes.'),
    'IR-EP13-NB-06': (I, 'The historical attacker cost is preserved as history.'),
    'IR-EP13-NB-07': (I, 'The original environment is preserved; this review names its interpreter (-I -B) and pins.'),
    'AX6': (N, 'Depends on TCB-SCOPE-01. The AX6 escape stays history; no delta file claims same-process route-region protection.'),
    'AX9': (N, 'Depends on TCB-SCOPE-01. The AX9 escape stays history; the source40 additions (token maps, unit-kind projection, nested folding) are typed data admission under a trusted evaluator.'),
    'MD5': (N, 'Depends on TCB-SCOPE-01. The MD5 escape stays history; source40 adds no Python-containment mechanism.'),
    'RX2c': (N, 'Depends on TCB-SCOPE-01. The RX2c escape stays history; complete replay and full-Run closure are reproducibility evidence, not containment.'),
}
RES_ROWS = []
for rid in ['RES-EP13-%02d' % i for i in range(1, 20)] + ['IR-EP13-NB-%02d' % i for i in range(1, 8)] + ['AX6', 'AX9', 'MD5', 'RX2c']:
    basis, text = RES_TEXT[rid]
    p = V39ROWS[rid]
    dep = 'TCB-SCOPE-01' if rid in TCB_DEPS else None
    if (p.get('sharedDependency') or None) != dep:
        GAPS.append('shared dependency differs from source39 for ' + rid)
    RES_ROWS.append(base_row(rid, basis, 'ASSESSED-CONSISTENT-GRADE-PENDING', text + ' The historical limitation is preserved; no historical guard is claimed repaired.',
                             proposedDisposition=p['proposedDisposition'], authorGrade='PENDING', sharedDependency=dep, residualRetained=True))
