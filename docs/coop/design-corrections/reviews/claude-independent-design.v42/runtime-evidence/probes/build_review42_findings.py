# Executed by build_review42.py in its own globals (exec). Findings, advisories, observations, current dispositions of every
# source40 finding/advisory/observation, and charter item assessments. Every claimed measurement is re-checked here.

def vx(prefix):
    row = next((r for c, r in VAX.items() if c.startswith(prefix)), None)
    if row is None:
        GAPS.append('three-tree row missing: ' + prefix)
        return {}
    if not row['ok']:
        GAPS.append('three-tree row not ok: ' + prefix)
    return row['observed']


def cj(prefix):
    row = next((r for c, r in CJ.items() if c.startswith(prefix)), None)
    if row is None:
        GAPS.append('capture-join row missing: ' + prefix)
        return {}
    return row['observed']


MUST, SHOULD = [], []
J2, J3, FW10, FW11 = cj('J2-'), cj('J3-'), vx('FW10-'), vx('FW11-')
adv_measured_ok = (J2.get('admission', {}).get('result') == 'ADMIT' and J3.get('admission', {}).get('result') == 'ADMIT'
                   and 'CLOSURE_FIELD_KIND' in str(J2.get('fullRun')) and 'CLOSURE_FIELD_KIND' in str(J3.get('fullRun'))
                   and all(FW11[t]['admission']['result'] == 'ADMIT' for t in FW11) and all(FW10[t]['admission']['refusals'] == ['EXECUTION_INPUTS_PLAN_JOIN'] for t in FW10))
if not adv_measured_ok:
    GAPS.append('ADV42-01 measurements are not as recorded')
ADVISORIES = [{
    'id': 'ADV42-01', 'severity': 'ADVISORY',
    'title': 'Execution-inputs admission neither states nor checks that a complete receipt\'s view outputRefs carry that receipt\'s producerClosure, and raises the section 3 PLAN_JOIN only for candidate views whose producer matches some row; Run closure is the backstop',
    'selectors': ['docs/coop/design-corrections/foundation/execution-inputs-contract.v1.md:12 (section 1: receipts rooted in producer obligations; outputRefs constrained by domain only)',
                  'execution-inputs-contract.v1.md:51 and :53 (section 3: stage-spec producerClosure and view planId checks; "a candidate view whose planId is not the Plan\'s refuses EXECUTION_INPUTS_PLAN_JOIN")',
                  'execution-inputs-contract.v1.md:299 (section 8: the builder places each explicit returned view on the view stage whose producerClosure it carries)',
                  'docs/coop/design-corrections/foundation/execution_inputs_model.v1.py:1057-1093 (receipt checks compare receipt and stage spec, never an outputRef view producer)',
                  'execution_inputs_model.v1.py:1132-1139 (the per-row producer filter precedes the planId check)',
                  'execution_inputs_model.v1.py:1626-1640 (an attributed view is compared with the producer of its ROW\'s receipt, not of the receipt that lists it)',
                  'docs/coop/design-corrections/foundation/identity-model.v3.py:1842-1851 and identity-schemas.v3.json byField view.producerClosure=provider (Run closure: VIEW_PLAN_JOIN, UNSELECTED_PRODUCER, closure kind)'],
    'measured': {'sameProviderForeignPlanId': cj('J1-'), 'foreignProducerSamePlan': J2, 'foreignProducerForeignPlan': J3, 'threeTreesForeignPlanId': FW10, 'threeTreesForeignProducer': FW11},
    'detail': ('A captured, unattributed view whose producerClosure is not the receipt\'s producer admits at execution-inputs admission on source40, source41 and source42, even with a foreign planId, and the complete Run refuses it only at closure (CLOSURE_FIELD_KIND:view.producerClosure:provider). '
               'A foreign-planId view from the stage\'s own provider refuses EXECUTION_INPUTS_PLAN_JOIN as section 3 says, because it passes a row\'s producer filter first. '
               'By reading, the model never compares a complete receipt\'s outputRef views with that receipt\'s producerClosure, and it checks attributed views against their own row\'s receipt. '
               'In a Plan with two view stages of two Plan-selected providers, a view of provider P2 listed on P1\'s complete receipt would therefore pass admission and the closure checks measured here. No maintained multi-provider graph exists, so that shape was not exercised.'),
    'consequence': ('No Run closes with the measured shapes; for them the contract\'s named refusal and the refusing owner differ. The unexercised multi-provider shape would be a self-contradictory stage-return record, a detectable host capture error rather than an omission. '
                    'It is not attribution nondeterminism for one captured observation, and it is pre-existing since source40.'),
    'disposition': ('ADVISORY, non-blocking. Owners may state in sections 1/3 that every complete-receipt view outputRef carries that receipt\'s producerClosure (existing EXECUTION_INPUTS_STAGE_PRODUCER), apply the planId check to every candidate view before the row filter, and add a two-stage two-provider control. '
                    'Not a SHOULD: no contradiction reaches an admitted Run in any measured world, the refusal chain is closed by the Run owner, and the TCB boundary is unchanged.'),
    'owner': 'foundation execution-inputs owner (contract sections 1/3, execution_inputs_model.v1.py); planned host capture crates/host/src/analysis.rs',
    'receipts': ['receipts/probes/capture-joins-42.json', 'receipts/probes/view-attribution-x.json']}]

FW4, FW7 = vx('FW4-'), vx('FW7-')
P = {k: v['observed'] for k, v in PEX.items()}
OBSERVATIONS = [
    {'id': 'OBS42-01', 'text': 'Reference builder limitation: execution_inputs_fixture.v3.py:228-243 attributes a returned view by the same-scope universe+relation test alone, without the section 3 producer or planId filter that execution_inputs_model.v1.py:1135-1139 applies. In a multi-producer graph the builder would name views the model refuses (VIEW_TOTALITY). Maintained graphs have one producer; this is a construction defect of the reference fixture, not missing law.', 'receipt': 'source read'},
    {'id': 'OBS42-02', 'text': 'Binder shorthand: enumeration-contract.v1.md:24 says the universe is the owner admission of "this selected context + this programEntry + this extent (bind_typescript_universe / bind_rust_universe / bind_syntax_universe)". The binders take (universe, admission, context, retained, snapshot_inventory) and no programEntry (native_evidence_model.v2.py:2939, 2988, 3229, signatures seen in search output). For TS/JS the entry reaches the universe through the retained TypeScriptConfigGraphV1.entryConfigPath that enumeration_model.v1.py:809-817 compares. The construction rule immediately after (:26-35) states that for Rust and syntax-only the retained entry is the universe H itself. The shorthand is imprecise but disambiguated within the same section and invents no Rust/syntax input: not a material ambiguity.', 'receipt': 'source read; receipts/probes/program-entry-x.json'},
    {'id': 'OBS42-03', 'text': 'Refs-only returned view: on source42 the builder captures a view named only on evaluationInputRefs, so a Run whose semantic evidence omits it refuses EVALUATION_VIEW_ROOTS; source40/41 dropped it and closed without it (FW7: %s). This follows the section 8 builder inputs and the root refs-only decision.' % json.dumps({t: FW7[t].get('fullRun') for t in FW7}), 'receipt': 'receipts/probes/view-attribution-x.json'},
    {'id': 'OBS42-04', 'text': 'Re-encoding under the selected same-scope interpretation: a view whose binding universe and capability relation sit on different scopes was attributed and closed on source40 under ExecutionInputsV1 digest %s. Source42 captures it on no row and closes under digest %s. This is a published prerelease identity change for one capture, not two admissions of one observation.' % (FW4['source40']['executionInputsDigest'][:16], FW4['source42']['executionInputsDigest'][:16]), 'receipt': 'receipts/probes/view-attribution-x.json'},
    {'id': 'OBS42-05', 'text': 'Explicit js-synthesized available bindings are now never admissible: the null entry refuses on source42 (%s), and a non-null entry refuses on both trees because the retained entryConfigPath of a synthesized program is null (%s). This is consistent with native section 2.2 (synthesized exactly when the entry is null) and the construction table (explicit TS/JS names a config).' % (P['js-synthesized-explicit-null']['source42']['refusals'], P['js-synthesized-explicit-package-json-nonnull']['source42']['refusals']), 'receipt': 'receipts/probes/program-entry-x.json'},
    {'id': 'OBS42-06', 'text': 'Unavailable bindings keep programEntry freedom: default or explicit, null or non-null, all four variants admit on source41 and source42. No owner states a canonical encoding, and different values are different Plan inputs.', 'receipt': 'receipts/probes/program-entry-x.json'},
    {'id': 'OBS42-07', 'text': 'Against codex final-reference.v42 and root-source42-final-reference.v3, all six group stdouts are byte-equal (%s) and %d of 17 child stdouts are byte-equal; enumeration and execution-inputs differ only in ownedHashes/receiptPath. The codex runner-original equals root v3: %s.' % (all(v['stdoutFileEqualCodex'] and v['stdoutFileEqualRootV3'] for v in RC['groups'].values()), RC['childrenEqualRootV3'], RC['codexRunnerOriginalEqualsRootV3']), 'receipt': 'receipts/reference-comparison.json'},
    {'id': 'OBS42-08', 'text': 'Re-observed on unchanged bytes by the ported source40 probes on source42: the policy.show acceptance of an unregistered token, the fixture representation limit for available optional imported evidence without a row, the consistent mode-and-kind remint under trusted markers, the omitted-allowJs observation default, one broad installPath row, the case-variant segment, the suppressedCount join, a repair:2 declared unavailability class, and admit_repair_plan_v2 as identity admission.', 'receipt': 'receipts/probes (ported)'},
]

S40ROWS = {x['id']: x for x in V40['newShouldIssues'] + V40['advisories'] + V40['observations'] + V40['itemDispositions']}
SOURCE40_DISPOSITIONS = [
    {'id': 'S40-01', 'source40Severity': 'SHOULD', 'currentDisposition': 'RESOLVED-ON-COMPLETE-SOURCE42-BYTES',
     'basis': ('Execution-inputs contract section 3 (:53) now publishes the attribution predicate:'
               ' candidate views are the complete-receipt view outputRefs, exactly the view members of selectedRefs (SELECTED_COVER);'
               ' same producer P; one and the same scope at U whose relation is the first element of a matrix [relation, resolution] pair; the matrix cell state plays no part; candidate-only capabilities attribute by U alone;'
               ' one view may sit on several rows; an unselected enumerator or null U attributes nothing; the canonical set is exact (VIEW_TOTALITY);'
               ' a captured unattributed view stays lawful and selected; and every named scope of an attributed view is at U (COVERAGE_DERIVE).'
               ' Section 8 (:299) makes receipts capture the explicit returned views and never the census, and the model enforces exact stage-produced totality (:1671-1690).'
               ' For one captured observation the attributed rows are now a deterministic published function. The source40 two-encoding demonstration (a returned view recorded or not recorded) is, as the charter notes, two different host observations; under source42 the builder records every explicit return, so only the observation itself stays host TCB.'),
     'evidence': ['receipts/probes/view-attribution-x.json (26/26)', 'receipts/case-populations.json', 'receipts/reference/evaluator3/execution-inputs.stdout (95 cases, 0 mismatches)']},
    {'id': 'ADV40-01', 'source40Severity': 'EDITORIAL', 'currentDisposition': 'RESOLVED',
     'basis': 'implementation-planning-sources.v1.json standing now selects architecture.manifestPath (v11) as current, marks previous layers historical, and names v8 a superseded intermediate whose native-evidence digest matches neither frozen39 nor frozen40. v8 bytes 99c8f876... are unchanged from source40 and listed in priorArchitectureInputLayers with their digest. No historical layer was mutated.',
     'evidence': ['receipts/planning-checks.json', '/tmp/opensip-design-corrections/root-planning-layer-history-clarification.v1 (after-image equals frozen bytes)']},
    {'id': 'OBS40-01', 'currentDisposition': 'RETAINED-OBSERVATION', 'basis': 'workflows-and-surfaces and policy_test_model bytes unchanged 40->42; the ported policy probe re-observes it.', 'evidence': ['receipts/probes/policy-v40-on42.json']},
    {'id': 'OBS40-02', 'currentDisposition': 'RETAINED-OBSERVATION', 'basis': 'Bytes unchanged; ported policy probe (26/26).', 'evidence': ['receipts/probes/policy-v40-on42.json']},
    {'id': 'OBS40-03', 'currentDisposition': 'RETAINED-OBSERVATION (OBS42-08)', 'basis': 'Bytes unchanged; policy.show remains inspection, not admission.', 'evidence': ['receipts/probes/policy-v40-on42.json']},
    {'id': 'OBS40-04', 'currentDisposition': 'RETAINED-OBSERVATION', 'basis': 'Native bytes unchanged; the ported native probe re-closes the consistent remint under trusted markers.', 'evidence': ['receipts/probes/native-v40-on42.json']},
    {'id': 'OBS40-05', 'currentDisposition': 'RETAINED-OBSERVATION', 'basis': 'Native bytes unchanged; re-observed.', 'evidence': ['receipts/probes/native-v40-on42.json']},
    {'id': 'OBS40-06', 'currentDisposition': 'RETAINED-OBSERVATION', 'basis': 'Native bytes unchanged; re-observed.', 'evidence': ['receipts/probes/native-v40-on42.json']},
    {'id': 'OBS40-07', 'currentDisposition': 'CLOSED', 'basis': 'The no-op scope-level enumeratorClosure continue was removed by the attribution correction (execution_inputs_model.v1.py 40->42 diff; the loop now tests one same-scope condition).', 'evidence': ['receipts/delta-diffs-40to42/docs__coop__design-corrections__foundation__execution_inputs_model.v1.py.diff']},
    {'id': 'OBS40-08', 'currentDisposition': 'SUPERSEDED (historical comparison not relabelled)', 'basis': 'The source42 reference comparison is OBS42-07.', 'evidence': ['receipts/reference-comparison.json']},
    {'id': 'OBS40-09', 'currentDisposition': 'RETAINED (OBS42-08)', 'basis': 'Ported probes re-observe it on unchanged owner bytes.', 'evidence': ['receipts/probes (ported)']},
    {'id': 'OBS40-10', 'currentDisposition': 'HISTORICAL CORRECTION STANDS', 'basis': 'The mapping population is 322 on source40, source41 and source42 (measured), with 0 rows changed.', 'evidence': ['receipts/planning-checks.json']},
] + [{'id': i, 'currentDisposition': 'REMAINS CLOSED', 'basis': b, 'evidence': e} for i, b, e in (
    ('S39-01', 'policy_test_model and section 5 bytes unchanged 40->42; the ported discrimination against source39 bytes passes on source42.', ['receipts/probes/policy-v40-on42.json']),
    ('S39-02', 'Bytes unchanged; the ported universe-token and imported-universe discrimination passes on source42.', ['receipts/probes/policy-v40-on42.json']),
    ('ADV39-01', 'Native section 10 account and registered bytes unchanged; the ported run-termination/registration probe passes (24/24).', ['receipts/probes/runterm-adv-v40-on42.json']),
    ('ADV38-01', 'Run-termination section 7 and model unchanged; ported section 7 probe passes (24/24).', ['receipts/probes/run-termination-s7.json']),
    ('ADV38-02', 'carrier-dispatch unchanged; ported read-only carrier probe passes (108 rows).', ['receipts/probes/carrier-readonly.json']),
    ('ADV38-03', 'commit-recovery-readonly unchanged 40->42; source39 measurement stands.', ['mapSources']))]
for d in SOURCE40_DISPOSITIONS:
    if d['id'] not in S40ROWS:
        GAPS.append('source40 disposition id not found in the source40 review: ' + d['id'])
covered_ids = {d['id'] for d in SOURCE40_DISPOSITIONS}
for x in V40['newShouldIssues'] + V40['advisories'] + V40['observations']:
    if x['id'] not in covered_ids:
        GAPS.append('source40 finding/advisory/observation without current disposition: ' + x['id'])

FW = {k: vx(k) for k in ('FW0-', 'FW1-', 'FW1c-', 'FW2-', 'FW5-', 'FW5h-', 'FW6-', 'FW8-', 'FW9-', 'FW12-', 'FW13-', 'SW0-', 'SW1-', 'SW2-', 'SW3-', 'SW3h-', 'SW4-', 'SW5-')}


def cols(obs, keys=('admission', 'fullRun')):
    return {t: {k: obs[t].get(k) for k in keys if k in obs[t]} for t in obs}


ATTR_PROPERTIES = [
    ('same producer P and the Plan', 'EXISTING LAW ENFORCED', 'contract :51 and :53; model :1135-1139; closure identity-model :1842-1845',
     {'foreignPlanSameProvider': cols(FW10)}, 'Unchanged across trees; admission scope limit recorded in ADV42-01.'),
    ('universe and relation on ONE AND THE SAME scope', 'NEWLY SELECTED DETERMINISTIC INTERPRETATION (previously model-only separate booleans)', 'contract :53; model :1147-1155; fixture :232-243',
     {'splitScope': cols(FW4, ('admission', 'fullRun', 'marksOnRows', 'executionInputsDigest'))}, 'Re-encodes split-scope views (OBS42-04); consistent with section 5 :236-249.'),
    ('relation-column membership (first element of [relation, resolution])', 'PUBLISHED PIN OF EXISTING MODEL BEHAVIOUR', 'contract :53; model :1129',
     {'checkerCases': 'relation-column-membership-* on source42 (reference self-consistency, run in this review\'s evaluator3 group)'}, 'Not independently probed beyond the checker run; the model reading is unchanged since source40.'),
    ('matrix cell state plays no part (UNSUPPORTED-TYPED attributes like supported)', 'PUBLISHED EXISTING MODEL BEHAVIOUR', 'contract :53, section 5 :174-188',
     {'unsupportedControl': cols(FW['FW0-'], ('admission', 'fullRun', 'marksOnRows'))}, 'The references view sits on the references row on every tree.'),
    ('candidate-only capability attributes by U alone', 'PUBLISHED EXISTING MODEL BEHAVIOUR', 'contract :53; model :1152 (not cap_rels)',
     {'sharedCasesIdentical': CASEPOP['executionInputs']['compare40to42']['differingSharedCases'] == {}}, 'The any-scope-at-U and same-scope-at-U readings coincide when the relation set is empty; candidate cases are identical across trees.'),
    ('exact canonical set (VIEW_TOTALITY)', 'EXISTING LAW ENFORCED', 'contract :53; model :1165-1168', {'syntaxOmitsShared': cols(FW['SW2-']), 'inventoryNamesNeither': cols(FW['SW4-'])}, 'Identical on every tree.'),
    ('no view names on an unselected enumerator or null U', 'EXISTING LAW ENFORCED', 'contract :53; model :1140-1141', {'unselectedRow': cols(FW['FW12-'])}, 'Identical on every tree.'),
    ('every named scope of an attributed view at the binding U, for every applicability', 'EXISTING LAW NEWLY ENFORCED (unsupported and coverage-less scopes previously bypassed)', 'contract :51, :53, section 5 :236-249; model :1157-1164',
     {'coverageLessForeign': cols(FW['FW1-']), 'foreignCoverage': cols(FW['FW2-']), 'sameUniverseControl': cols(FW['FW1c-'])}, 'source40 admits and closes; source41/42 refuse at admission and in the Run.'),
    ('valid captured unattributed views', 'EXISTING CAPTURE LAW, BUILDER NOW FAITHFUL', 'contract :12-19, :53, :299; fixture :341-353',
     {'builder': cols(FW['FW5-'], ('admission', 'fullRun', 'marksCaptured', 'marksOnRows')), 'explicit': cols(FW['FW5h-'])}, 'source40/41 builders dropped them (EVALUATION_VIEW_ROOTS).'),
    ('cross-universe target relations', 'EXISTING LAW PRESERVED', 'section 5 :154-165, :236-239; model :1163 compares sourceUniverse only', {'crossTarget': cols(FW['FW13-'])}, 'Admits and closes on every tree.'),
    ('one view on several rows of one program/U', 'PUBLISHED EXISTING MODEL BEHAVIOUR', 'contract :53', {'twoCellShared': cols(FW['SW1-'], ('admission', 'fullRun', 'marksOnRows', 'executionInputsDigest'))}, 'Byte-identical manifest and RunId on every tree.'),
]

ITEMS = [
    {'id': 'CH42-ATTRIBUTION-LAW', 'disposition': 'SUFFICIENT AND CONSISTENT',
     'assessment': 'Each required property is stated in contract section 3 and implemented by the model; the table separates existing-law enforcement from the newly selected deterministic interpretation. Section 5 (:221-249) now refers to section 3 for which views are reached, and the schema description at execution-inputs.schema.v1.json:621 ("captured receipt views attributed to this cell/program/U/producer") agrees with the published candidate set. The remaining admission-scope note is ADV42-01. Joins verified at their owners: stage/receipt (model :1042-1093), row receipt producer (:1618-1640), plan (:883-894), selection (evaluator_input_model :26-45), Run closure (identity-model :1797-1851).',
     'properties': [{'property': a, 'classification': b, 'selectors': c, 'evidence': d, 'note': e} for a, b, c, d, e in ATTR_PROPERTIES]},
    {'id': 'CH42-CAPTURE', 'disposition': 'SUFFICIENT AND CONSISTENT',
     'assessment': 'Receipts capture the explicit returned views (viewIds/viewId and view refs on evaluationInputRefs) and never the ambient census: a census-only view is never captured and leaves the digest equal to the control on every tree. A captured unattributed view is selected and on no row, and closes on source42. Stage-produced selectedRefs equals the union of complete receipts exactly: a reminted receipt that omits a selected attributed view admitted and closed on source40/41 and refuses SELECTED_COVER on source42 in both worlds, and a receipt view missing from selectedRefs refuses on every tree. A refs-only view is captured, so evidence omitting it refuses (OBS42-03). Capture detects internal inconsistency, not malicious omission; the TCB limitation of section 1 :24 stands.',
     'evidence': {'censusOnly': cols(FW['FW6-'], ('marksCaptured', 'executionInputsDigest')), 'remintedReceiptFile': cols(FW['FW8-']), 'remintedReceiptTwoCell': cols(FW['SW5-']),
                  'receiptNotSelected': cols(FW['FW9-']), 'neitherViewBuilder': cols(FW['SW3-'], ('admission', 'fullRun', 'marksCaptured', 'marksOnRows')), 'neitherViewExplicit': cols(FW['SW3h-'])}},
    {'id': 'CH42-HISTORICAL-POPULATIONS', 'disposition': 'ACCOUNTED',
     'assessment': ('Each tree\'s own execution-inputs checker ran on its verified copy: source40 %d cases, source41 %d, source42 %d, 0 mismatches each. All shared cases are field-identical (path fields excluded) 40->41 (%d shared), 41->42 (%d) and 40->42 (%d), and the shared full-run RunIds are equal. '
                    'The 10 cases added by the attribution correction include 7 closed-run cases (closed=False on naming-no-view, host-naming split scope and supported two-universe rows), and the 9 capture cases include 6 closed-run cases (closed=False on census-only, its control and the pair-reading encoding); both counts are read from the checker diff. '
                    'Enumeration: source41 %d cases, source42 %d, %d shared cases field-identical, unit-kind and unit-root controls identical. These are reference self-consistency counts, not independent proof; the independent discrimination is CH42-ATTRIBUTION-LAW and CH42-CAPTURE.')
     % (CASEPOP['executionInputs']['source40']['cases'], CASEPOP['executionInputs']['source41']['cases'], CASEPOP['executionInputs']['source42']['cases'],
        CASEPOP['executionInputs']['compare40to41']['shared'], CASEPOP['executionInputs']['compare41to42']['shared'], CASEPOP['executionInputs']['compare40to42']['shared'],
        ENUMPOP['source41']['cases'], ENUMPOP['source42']['cases'], ENUMPOP['compare41to42']['shared']),
     'evidence': {'executionInputs': {k: v for k, v in CASEPOP['executionInputs'].items() if k.startswith('compare')}, 'enumeration': ENUMPOP['compare41to42']}},
    {'id': 'CH42-PROGRAM-ENTRY-CLARIFICATION', 'disposition': 'CONSISTENT; NO SEMANTIC CHANGE',
     'assessment': 'Enumeration contract section 1 (:21-47) restates AvailableProgramBindingV1.programEntry (schema :380-390). A default available binding is null; for tsconfig/jsconfig markers the admission-derived entry is the U-1 marker, for js-synthesized a null entry with no nodes. An explicit TS/JS binding names the selected config and equals the retained entryConfigPath. Rust and syntax-only are keyed by the universe H. The syntax-only sentence (:21) now correctly cites the U-9 fallback unit. The WRONG example (:46) is exactly what admission refuses (ts-default-marker-nonnull refuses on both trees), and the explicit marker selection it keeps lawful admits on both. Unavailable bindings get no rule (OBS42-06).',
     'evidence': {k: P[k] for k in ('ts-default-null', 'ts-default-marker-nonnull', 'ts-explicit-marker-nonnull', 'ts-default-null-plus-explicit-build-config', 'rust-explicit-null', 'syntax-explicit-null')}},
    {'id': 'CH42-PROGRAM-ENTRY-ENFORCEMENT', 'disposition': 'CONFIRMED',
     'assessment': 'enumeration_model.v1.py:803-807 now refuses ENUMERATION_BINDING_PROGRAM_ENTRY for an available explicit-plan-selection binding with a null entry in every TS/JS mode, enforcing the schema\'s non-null TS/JS extra-program law that source41 admitted when the null happened to equal the U-1 derivation. Independently discriminated at the enumeration owner: ts-tsconfig, js-allowjs and js-synthesized explicit null admit on source41 and refuse exactly on source42; defaults, explicit marker and build-config selections, Rust and syntax (null or non-null) and every unavailable variant are unchanged. Complete Run closure consumes the same owner admission (evaluator_input_model.v3.py:103-104), so the refusal reaches the Run as EVALUATOR_ENUMERATION_JOIN. The checker adds 8 cases; the 46 shared cases are identical. Standalone atom and workflow fragments with explicit null TS bindings never call admit_enumeration and are not complete Runs, so they are not an admission regression.',
     'evidence': {k: v for k, v in PEX.items()}},
    {'id': 'CH42-IDENTITY-DIGEST-SCOPE', 'disposition': 'SUFFICIENTLY EXPLICIT; NO CLARIFICATION REQUIRED',
     'assessment': 'identity-and-evidence.md:407-418 scopes the closing digest law to identity-schemas.v3. :420-433 extends the same law, with a named sweep refusal, to every foundation record document the closure walks through a {document, selector} record, lists them, and says identity-schemas and the relation payload document carry their own sweeps. :920-934 states that the native contract extends the law to its own bundle and that relation-payload-schemas.v2.json carries its own x-opensip-digest-law. Each vocabulary\'s owner is named, and an unannotated position refuses mechanically in each scope, so a reader cannot mistake which law governs a document.',
     'evidence': {'read': 'identity-and-evidence.md 400-474 and 912-966 this charter'}},
    {'id': 'CH42-COMPOSITION7-AND-POLICY-DERIVATION3', 'disposition': 'SOURCE40 NO-GAP FINDINGS PRESERVED',
     'assessment': 'evaluator-composition-contract.v3.md and evaluator_replay_model.v3.py are byte-identical 40->42 (%s, %s). This origin\'s source40 assessment stands on unchanged bytes. Section 7 closes OUTPUT typed-prefix references in their prefix-selected domains. Input identities named by outputs are fixed by the section 9 equality addresses to inputs admitted before replay. policy-derivation3 is a derived projection admitted by equality under section 9.7, carrying no runId. Not re-read this charter.' % (U['evaluator-composition-contract.v3.md'], U['evaluator_replay_model.v3.py']),
     'evidence': {'source40Items': [S40ROWS['NARROW-Q2-COMPOSITION-S7-CLOSURE']['disposition'], S40ROWS['NARROW-Q3-POLICY-DERIVATION3']['disposition']]}},
    {'id': 'CH42-PLANNING-V11', 'disposition': 'CONFIRMED (population measured)',
     'assessment': 'v11 binds 31 current inputs with no mismatch and no self-binding. v11, v10 and v9 are byte-identical (75ea6065...); coverage subject and planning architecture name v11, and v10 is the previous layer. priorArchitectureInputLayers lists v1-v9 with digests matching their bytes. There are 322 mappings on source40, source41 and source42 with 0 rows changed; 24 report features; 198 paths in 20 packages; M0-M6; 54 recovery cases, none executed.',
     'evidence': {k: PC[k] for k in ('layerSha256', 'layerMismatchedAgainstSource42', 'v9v10v11ByteIdentical', 'coverageSubjectMatchesV11', 'planningSourcesArchitectureSha256MatchesV11', 'planningSourcesPrevious',
                                     'planningSourcesHistoryHashesMatchLayerBytes', 'coverageMappings', 'coverageMappingsSource41', 'coverageMappingsSource40', 'coverageRowsChangedVs40',
                                     'coverageGroups', 'inventoryPaths', 'inventoryPackages', 'recoveryCases', 'recoveryCasesNotExecuted', 'milestoneOrder')}},
    {'id': 'CH42-PACKAGE19', 'disposition': 'VERIFIED AS AUTHOR EVIDENCE', 'assessment': 'See packageAssessment.', 'evidence': {k: v['ok'] for k, v in PK.items()}},
    {'id': 'CH42-CURRENT-REFERENCE', 'disposition': 'OWN EXECUTION PASSES; HEADER RECEIPTS CONSISTENT',
     'assessment': 'This review\'s six groups and 17 children pass on its own verified copy, with 95 execution-inputs and 54 enumeration cases at 0 mismatches. The header-named codex final-reference.v42 report hashes to d46d0bf2..., binds f602fc7e... and passed; its runner-original equals root-source42-final-reference.v3. Root v1 and v2 were not used, and no source40 result is relabelled.',
     'evidence': {k: RC[k] for k in ('codexReferenceChecks', 'codexPassed', 'codexSubjectManifestSha256', 'codexRunnerOriginalEqualsRootV3', 'childrenEqualCodex', 'childrenEqualRootV3')}},
    {'id': 'CH42-SCOPE-PRESERVATION', 'disposition': 'RE-EXECUTED ON SOURCE42',
     'assessment': 'The source40 scope probes were ported with only runtime paths changed (receipts/probe-port.json) and pass on source42: policy.test, native discovery/unitKind/allowJs/nested Cargo, run-termination and registration, nine command carriers and twenty operations, read-only carriers, comparison knowledge, repair:2, section 7 termination, custody and fallback. Their owner bytes are unchanged 40->42.',
     'evidence': {p['id']: {'rows': p['result']['rows'], 'failed': len(p['result']['failedRows'])} for p in PROBES if p['id'].startswith('P42-PORTED')}},
]
