# Executed by build_review45.py in its own globals (exec). Issues, observations, current dispositions of every prior finding,
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


def cw(case):
    return pick(CW, case, 'closed-world45')


def cb(case):
    return pick(CB, case, 'checker-binding45')


MUST, SHOULD = [], []
V44ITEMS = {i['id']: i for i in V44['itemDispositions']}
V44ADV = {a['id']: a for a in V44['advisories']}

# ------------------------------------------------------------------------------------------------ advisories (both retained)
J1, J2, J3 = pickp(CJ, 'J1-', 'capture-joins-on45'), pickp(CJ, 'J2-', 'capture-joins-on45'), pickp(CJ, 'J3-', 'capture-joins-on45')
adv_measured_ok = (J1.get('admission', {}).get('refusals') == ['EXECUTION_INPUTS_PLAN_JOIN'] and J2.get('admission', {}).get('result') == 'ADMIT' and J3.get('admission', {}).get('result') == 'ADMIT'
                   and 'CLOSURE_FIELD_KIND' in str(J2.get('fullRun')) and 'CLOSURE_FIELD_KIND' in str(J3.get('fullRun'))
                   and not PORTED_EQUAL['P45-PORTED-CAPTURE-JOINS']['observedDifferFromSource44'])
adv_bytes = {k: U[k] for k in ('execution-inputs-contract.v1.md', 'execution_inputs_model.v1.py', 'execution-inputs.schema.v1.json', 'execution_inputs_fixture.v3.py', 'identity-model.v3.py', 'identity-schemas.v3.json')}
if not adv_measured_ok or not all(adv_bytes.values()):
    GAPS.append('ADV42-01 re-measurement or owner-byte identity not as recorded')
adv44_bytes = {k: U[k] for k in ('protocol3-transitions.v1.json', 'fact-batch.schema.v3.json')}
if any(PC['adv4401'].values()) or not all(adv44_bytes.values()):
    GAPS.append('ADV44-01 binding state or owner bytes differ from measurement')
A42, A44 = V44ADV['ADV42-01'], V44ADV['ADV44-01']
ADVISORIES = [
    {'id': 'ADV42-01', 'severity': 'ADVISORY', 'origin': 'source42 review (retained; not new in source45)', 'title': A42['title'], 'selectors': A42['selectors'],
     'selectorOwnerBytesUnchanged44to45': adv_bytes,
     'measuredOnSource45': {'sameProviderForeignPlanId': J1, 'foreignProducerSamePlan': J2, 'foreignProducerForeignPlan': J3,
                            'observedEqualToSource44Receipt': not PORTED_EQUAL['P45-PORTED-CAPTURE-JOINS']['observedDifferFromSource44']},
     'detail': A42['detail'],
     'currentStanding': 'RETAINED ADVISORY, NON-BLOCKING. The root implementation verification obligation for crates/host/src/analysis.rs remains correctly scoped; it is not a containment proof and no control was executed for it.',
     'standingAssessment': ('Every selector owner is byte-identical 44->45 (%s): source45 touches no execution-inputs, identity or capture byte. The ported measurement re-observes the source44 values exactly. J1 refuses EXECUTION_INPUTS_PLAN_JOIN. J2 and J3 admit at execution-inputs admission, and close_run refuses them with CLOSURE_FIELD_KIND:view.producerClosure:provider. '
                            'Receipt/view producer equality and the plan check before the row filter are still not enforced at execution-input admission. The two-provider shape remains unexercised, and the fixture keeps its recorded multi-provider construction limitation. '
                            'No measured world admits a contradictory Run. The source45 closed-world correction mints only host-derived provider-unavailable coverage and adds no view or receipt path, so it creates no contradiction with the advisory and no reason to reopen it.') % json.dumps(adv_bytes),
     'consequence': A42['consequence'], 'disposition': A42['disposition'], 'owner': A42['owner'],
     'receipts': ['receipts/probes/capture-joins-on45.json', 'claude-independent-design.v44/receipts/probes/capture-joins-on44.json (historical)']},
    {'id': 'ADV44-01', 'severity': 'ADVISORY', 'origin': 'source44 review (retained; not new in source45)', 'title': A44['title'], 'selectors': A44['selectors'],
     'measuredOnSource45': {'v13Inputs': PC['layerInputs']['13'], 'v13ChangedVsV12': PC['v13ChangedVsV12'], 'protocol3AndFactBatchV3BoundByV13': PC['adv4401'],
                            'protocol3AndFactBatchV3Unchanged44to45': adv44_bytes, 'changedSelfDeclaredNormativeDocumentsNotBoundByV13': UNBOUND_NORMATIVE},
     'detail': A44['detail'],
     'currentStanding': 'RETAINED ADVISORY, NON-BLOCKING. The optional direct planning-input coverage of the protocol3 table and fact-batch v3 is still not taken up; neither document changed in source45.',
     'standingAssessment': ('v13 correctly binds the two changed normative inputs, native-evidence.md and provider-startup.schemas.v1.json, and preserves v8-v12 byte-identically. The only changed self-declared normative documents it does not bind are the planning records themselves (%s), which the layer standing excludes to avoid a self-hash cycle. '
                            'protocol3-transitions.v1.json and fact-batch.schema.v3.json remain unbound and unchanged 44->45, so the source44 asymmetry persists without widening. No normative content is lost, because both restate law bound through native-evidence section 9.') % UNBOUND_NORMATIVE,
     'consequence': A44['consequence'], 'disposition': A44['disposition'], 'owner': A44['owner'], 'receipts': ['receipts/planning-checks.json']},
]

# ------------------------------------------------------------------------------------------------ observations
consumer_display = ('`RepairPlanDescriptor.closedWorld` (workflows 937-968) reduces each member to the least-closed value among the selected records. The display sentinel with nothing selected uses `nonliteralLoading: present`, the least-closed pole, to stand for absence.')
OBSERVATIONS = [
    {'id': 'OBS45-01', 'text': ('Against root-source45-final-reference.v1 and codex final-reference.v45, all six group stdouts are byte-equal (%s), and %d of %d child stdouts are byte-equal to root. Enumeration and execution-inputs differ from root only in path fields. '
                                'Against this origin\'s source44 receipts, all six group stdouts are byte-equal and the same two children differ only in path fields; the native checker still reports 477/477. The codex runner-original equals the root reference-checks (%s), and codex adds the formal subject binding (%s).')
     % (all(v['stdoutFileEqualRoot'] and v['stdoutFileEqualCodex'] and v['stdoutEqualHistoricalMine44'] for v in RC['groups'].values()), RC['childrenEqualRoot'], RC['childCount'], RC['codexRunnerOriginalEqualsRoot'], RC['codexMinusRootTopLevelKeys']),
     'receipt': 'receipts/reference-comparison.json'},
    {'id': 'OBS45-02', 'text': ('The root reference and the root companion checks v2 were executed from a pre-freeze working tree (%s), not the frozen archive; companion v1 lacked the planning --source argument and is retained. The recorded script shas equal the frozen source45 bytes, all six group stdouts are byte-equal to this review\'s own runs, and the companion stdout text equals this review\'s planning and inventory output (%s). This review\'s own executions are the acceptance input.')
     % (RC['rootExecutionSourceRoots'], planning_stdout_equal_companion), 'receipt': 'receipts/reference-comparison.json; receipts/planning-checks.json'},
    {'id': 'OBS45-03', 'text': ('Ten ported scope probes re-observe every value of this origin\'s source44 receipts on source45 (%s). The re-executed 162-row source44 startup discriminator is row-for-row identical (%d rows, %d differing). This is corroboration, not fresh assessment.')
     % (', '.join('%s %d' % (k.replace('P45-PORTED-', '').lower(), v['rows']) for k, v in PORTED_EQUAL.items()), REEXEC_EQUAL['rows'], len(REEXEC_EQUAL['observedDifferFromSource44'])),
     'receipt': 'receipts/ported45-vs44.json; receipts/probes/startup44-reexec-on45.json'},
    {'id': 'OBS45-04', 'text': ('Consumer effect of the fixed record. The workflows repair gate is the conjunction of deadCodeRepairEligible over the selected records (workflows 815-819), so a relevant universe whose only records are pre-analysis conversions stays ineligible. ' + consumer_display +
                                ' A summary whose selected records are all pre-analysis conversions therefore displays nonliteralLoading none and entryPointsRecognized none while exportsClosed is unknown and the boolean is false. That summary is non-authoritative (workflows 970-972), and section 9.7 (3259-3261) states that the fixed value proves no absence of dynamic loading or dispatch. This is display semantics, not a contradiction, and it predates source45: the source44 helper produced the same record.'),
     'receipt': 'workflows-and-surfaces.md 800-974 (read); receipts/probes/closed-world45.json'},
    {'id': 'OBS45-05', 'text': 'Editorial only: provider-target-attribution-return.schema.v2.json x-opensip-return-law.missingAndIncomplete.missingToken now reads "Historical the historical per-language payload (...)", a duplicated word in an annotation. Meaning is clear, and no $defs, property or registered shape changed (P45-CLOSED-WORLD shape rows).',
     'receipt': 'receipts/delta-diffs-44to45/docs__coop__design-corrections__foundation__provider-target-attribution-return.schema.v2.json.diff'},
    {'id': 'OBS45-06', 'text': ('native-cases.v2.json was reindented: the text diff is %d lines, but the parsed structures differ only in the two pre-analysis conversion cases, which each add closedWorld expectations (TS 2, Rust 1). All 125 fixtures, the other 475 cases, case order and top-level members are equal. '
                                'Neither source44 nor source45 bytes equal a stock json.dumps re-serialisation at indent none/1/2/4, so the whitespace layout is an author formatting choice; semantic identity is established structurally.')
     % next(r['diffLines'] for r in DIFFSUM['44to45'] if r['path'].endswith('native-cases.v2.json')), 'receipt': 'receipts/probes/cases-structure45.json'},
    {'id': 'OBS45-07', 'text': ('Law derivation boundary. Section 4.5 forces exportsClosed unknown, entryPointsRecognized none and deadCodeRepairEligible false for a conversion that observes no manifest and no recognizer. nonliteralLoading none, dynamicDispatch not-applicable, externalConsumers unknown and reasons ["no-manifest"] are not forced by 4.5; they are the published section 9.7 choice. '
                                'ClosedWorldV2 has no unknown member for nonliteralLoading or dynamicDispatch, consistent with workflows 963-968. The disclaimer is text-only, and the value cannot enable closed exports or dead-code repair.'),
     'receipt': 'receipts/probes/closed-world45.json'},
    {'id': 'OBS45-08', 'text': ('Checker binding scope. check_native_evidence compares the law member, the helper\'s no-observation result and the first JSON fence of section 9.7 by parsed equality. Section 9.7 contains exactly one fence today, so a later fence placed before it would change which block is checked. '
                                'The case expectations pin the minted entries independently of the checker, and all three mutation variants were refused with their exact faults.'),
     'receipt': 'receipts/probes/checker-binding45.json'},
    {'id': 'OBS45-09', 'text': ('Committed bytes. The published record\'s canonical JSON is %s with SHA-256 %s. The pre-analysis entries minted by the source45 exchange are byte-identical to those minted by the source44 exchange, and their coverage identities are equal (TS %s; Rust %s). Package RunIds are unchanged, so the correction publishes law without changing any retained or derived identity.')
     % (cw('section-9.7-publishes-exactly-one-json-record-equal-to-the-startup-law-member-by-parse-and-canonical-bytes').get('canonical'),
        cw('section-9.7-publishes-exactly-one-json-record-equal-to-the-startup-law-member-by-parse-and-canonical-bytes').get('canonicalSha256'),
        cw('typescript-semantic-source44-exchange-yields-byte-identical-entries-and-coverage-ids').get('coverageIds45'),
        cw('rust-semantic-source44-exchange-yields-byte-identical-entries-and-coverage-ids').get('coverageIds45')),
     'receipt': 'receipts/probes/closed-world45.json'},
    {'id': 'OBS45-10', 'text': ('The source44 reference-scope limits remain material and unchanged by source45. The reference takes planned stages, verified descriptors and the Plan identity row as trusted host inputs (OBS44-05, re-observed). It does not validate every provider-authored descriptor member, every Cancel/Cancelled correlation or Rust Cancelled phase, recomputes no stream or coverage commitment (OBS44-06/07), and exercises no framing, process or compiler. '
                                'The closed-world discriminator is a measured subset of reference host-conversion behaviour over fixture inputs, not executed proof of the normative requirement in a product.'),
     'receipt': 'receipts/probes/startup44-reexec-on45.json; native-evidence.md 3304-3313 (read)'},
]

# ------------------------------------------------------------------------------------------------ prior finding dispositions
QOWN = {k: U[k] for k in ('query-projection-contract.v3.md', 'query_projection_model.v3.py', 'check-query-projection.v3.py', 'query_surface_projection.v3.py', 'graph-query.schema.json')}
if not all(QOWN.values()):
    GAPS.append('query owners changed 44->45')
PRIOR_DISPOSITIONS = [
    {'id': 'S40-01', 'priorSeverity': 'SHOULD (source40)', 'source44Disposition': 'REMAINS RESOLVED ON SOURCE44', 'currentDisposition': 'REMAINS RESOLVED ON SOURCE45', 'basis': 'unchanged-44-basis',
     'reasoning': ('The execution-inputs contract, schema, model and fixture and the enumeration contract/model are byte-identical 44->45 (%s), so the source44 assessment of the section 3 attribution predicate and section 8 capture exactness stands. '
                   'Corroboration: the execution-inputs (95 cases) and enumeration (54 cases) children equal root and this origin\'s source44 receipts after removing path fields only, and the capture-join measurement is identical.')
     % json.dumps({k: U[k] for k in ('execution-inputs-contract.v1.md', 'execution-inputs.schema.v1.json', 'execution_inputs_model.v1.py', 'execution_inputs_fixture.v3.py', 'enumeration-contract.v1.md', 'enumeration_model.v1.py')}),
     'evidence': ['mapSources', 'receipts/reference-comparison.json', 'receipts/probes/capture-joins-on45.json']},
    {'id': 'ADV40-01', 'priorSeverity': 'EDITORIAL (source40)', 'source44Disposition': 'REMAINS RESOLVED ON SOURCE44', 'currentDisposition': 'REMAINS RESOLVED ON SOURCE45', 'basis': 'new-45',
     'reasoning': ('implementation-planning-sources.v1.json now selects v13 (%s...) as current with v12 as previous and moves the v11 record into the prior-layer history (%d records, digests matching bytes: %s). Layers v8-v12 are byte-identical to source44 (%s). No historical layer was mutated.')
     % (PC['layerSha256']['13'][:12], PC['planningSourcesHistoryCount'], PC['planningSourcesHistoryHashesMatchLayerBytes'], PC['priorLayersByteEqualToSource44']),
     'evidence': ['receipts/planning-checks.json', 'receipts/delta-diffs-44to45/docs__v2__architecture__implementation-planning-sources.v1.json.diff']},
    {'id': 'ADV42-01', 'priorSeverity': 'ADVISORY (source42)', 'source44Disposition': 'RETAINED ADVISORY', 'currentDisposition': 'RETAINED ADVISORY (see advisories)', 'basis': 'unchanged-44-basis',
     'reasoning': ADVISORIES[0]['currentStanding'], 'evidence': ADVISORIES[0]['receipts']},
    {'id': 'ADV44-01', 'priorSeverity': 'ADVISORY (source44)', 'source44Disposition': 'ADVISORY, non-blocking', 'currentDisposition': 'RETAINED ADVISORY (see advisories)', 'basis': 'new-45',
     'reasoning': ADVISORIES[1]['currentStanding'], 'evidence': ADVISORIES[1]['receipts']},
    {'id': 'OBS44-01', 'source44Disposition': 'OBSERVATION', 'currentDisposition': 'SUPERSEDED BY OBS45-01 (historical comparison not relabelled)', 'basis': 'new-45', 'reasoning': 'The source44 comparison stays historical; the source45 comparison is OBS45-01.', 'evidence': ['receipts/reference-comparison.json']},
    {'id': 'OBS44-02', 'source44Disposition': 'OBSERVATION', 'currentDisposition': 'SUPERSEDED BY OBS45-02 (historical record not relabelled)', 'basis': 'new-45', 'reasoning': 'The source44 working-tree execution record stays historical; the source45 equivalent is OBS45-02.', 'evidence': ['receipts/reference-comparison.json']},
    {'id': 'OBS44-03', 'source44Disposition': 'OBSERVATION', 'currentDisposition': 'RETAINED (OBS45-03)', 'basis': 'new-45', 'reasoning': 'The ported probes re-observe every value on source45.', 'evidence': ['receipts/ported45-vs44.json']},
    {'id': 'OBS44-04', 'source44Disposition': 'OBSERVATION', 'currentDisposition': 'RETAINED OBSERVATION', 'basis': 'unchanged-44-basis',
     'reasoning': 'rustCommitHash owners unchanged: the handshake schema, wire model and registered bundle are byte-identical 44->45 (%s), and the startup schema $defs are unchanged (only its x-opensip-startup-law annotation changed).' % json.dumps({k: U[k] for k in ('provider-handshake.schemas.v1.json', 'provider_wire_model.v1.py', 'native-evidence.schemas.v2.json')}),
     'evidence': ['mapSources', 'receipts/probes/closed-world45.json']},
    {'id': 'OBS44-05', 'source44Disposition': 'OBSERVATION', 'currentDisposition': 'RETAINED OBSERVATION (OBS45-10)', 'basis': 'new-45', 'reasoning': 'The re-executed startup discriminator re-observes the trusted plannedStages, raised host invariant and unjoined universe members identically. Source45 changes only the closedWorld construction.', 'evidence': ['receipts/probes/startup44-reexec-on45.json']},
    {'id': 'OBS44-06', 'source44Disposition': 'OBSERVATION', 'currentDisposition': 'RETAINED OBSERVATION', 'basis': 'unchanged-44-basis', 'reasoning': 'TS order table, protocol3 table and startup model byte-identical 44->45 (%s); cancellation and exit asymmetries re-observed.' % json.dumps({k: U[k] for k in ('typescript-protocol2-order.v1.json', 'protocol3-transitions.v1.json', 'provider_startup_model.v1.py')}), 'evidence': ['mapSources', 'receipts/probes/startup44-reexec-on45.json']},
    {'id': 'OBS44-07', 'source44Disposition': 'OBSERVATION', 'currentDisposition': 'RETAINED OBSERVATION (OBS45-10)', 'basis': 'new-45', 'reasoning': 'The section 9.7 reference-scope paragraph (3304-3313, read) is unchanged in wording, and commitments are still not recomputed (re-observed).', 'evidence': ['receipts/probes/startup44-reexec-on45.json']},
    {'id': 'OBS44-08', 'source44Disposition': 'OBSERVATION', 'currentDisposition': 'RETAINED OBSERVATION', 'basis': 'unchanged-44-basis', 'reasoning': 'Registered bundle and handshake schema byte-identical 44->45 (%s, %s).' % (U['native-evidence.schemas.v2.json'], U['provider-handshake.schemas.v1.json']), 'evidence': ['mapSources']},
    {'id': 'OBS44-09', 'source44Disposition': 'OBSERVATION', 'currentDisposition': 'HISTORICAL; STANDS', 'basis': 'unchanged-44-basis', 'reasoning': 'It concerns the source44 root clarification\'s before-bytes; source45 does not revisit it.', 'evidence': ['source44 review (historical)']},
    {'id': 'OBS44-10', 'source44Disposition': 'OBSERVATION', 'currentDisposition': 'RETAINED OBSERVATION', 'basis': 'unchanged-44-basis', 'reasoning': 'provider_attribution_return_model.v2.py byte-identical 44->45 (%s); the attribution-return schema changed only annotation prose (OBS45-05).' % U['provider_attribution_return_model.v2.py'], 'evidence': ['mapSources']},
    {'id': 'OBS44-11', 'source44Disposition': 'OBSERVATION', 'currentDisposition': 'SUPERSEDED BY THE PACKAGE22 EQUIVALENT (packageAssessment)', 'basis': 'new-45', 'reasoning': 'The bound package22 verification again differs from the root pre-binding verification only in package identity and file count.', 'evidence': ['receipts/probes/package-v22.json']},
]
PROBE_FOR = {'OBS40-01': 'P45-PORTED-POLICY', 'OBS40-02': 'P45-PORTED-POLICY', 'OBS40-03': 'P45-PORTED-POLICY', 'OBS40-04': 'P45-PORTED-NATIVE', 'OBS40-05': 'P45-PORTED-NATIVE',
             'OBS40-06': 'P45-PORTED-NATIVE', 'OBS40-09': 'P45-PORTED-POLICY', 'S39-01': 'P45-PORTED-POLICY', 'S39-02': 'P45-PORTED-POLICY', 'ADV39-01': 'P45-PORTED-RUNTERM',
             'ADV38-01': 'P45-PORTED-TERM7', 'ADV38-02': 'P45-PORTED-CARRIER', 'OBS43-06': 'P45-PORTED-POLICY'}
covered_now = {d['id'] for d in PRIOR_DISPOSITIONS}
for prior in V44['priorFindingDispositions']:
    i = prior['id']
    if i in covered_now:
        continue
    cur = re.sub(r' \(on source44\)$', '', prior['currentDisposition'])
    if i.startswith('OBS43-'):
        basis, reasoning = 'unchanged-44-basis', 'Source44 disposition %s. The query projection contract, model, checker, surface projection and graph-query schema are byte-identical 44->45 (%s).' % (prior['currentDisposition'], json.dumps(QOWN))
    elif i in PROBE_FOR:
        basis, reasoning = 'new-45', 'Source44 disposition %s. On source45 the owning probe %s re-observes every row identically (%d rows).' % (prior['currentDisposition'], PROBE_FOR[i], PORTED_EQUAL[PROBE_FOR[i]]['rows'])
    elif i == 'OBS42-02':
        basis, reasoning = 'new-45', 'Source44 disposition %s. enumeration-contract.v1.md is byte-identical 44->45 (%s); native_evidence_model.v2.py changed only in the pre-analysis closedWorld construction and a comment (complete diff read), so the binder shorthand is unchanged.' % (prior['currentDisposition'], U['enumeration-contract.v1.md'])
    elif i in ('OBS42-01', 'OBS42-03', 'OBS42-04', 'OBS40-07'):
        basis, reasoning = 'unchanged-44-basis', 'Source44 disposition %s. execution_inputs_model.v1.py and execution_inputs_fixture.v3.py are byte-identical 44->45 (%s, %s).' % (prior['currentDisposition'], U['execution_inputs_model.v1.py'], U['execution_inputs_fixture.v3.py'])
    elif i in ('OBS42-05', 'OBS42-06'):
        basis, reasoning = 'unchanged-44-basis', 'Source44 disposition %s. enumeration_model.v1.py byte-identical 44->45 (%s).' % (prior['currentDisposition'], U['enumeration_model.v1.py'])
    elif i == 'OBS40-10':
        basis, reasoning = 'new-45', 'Source44 disposition %s. The mapping population is 322 on source44 and source45; six native-evidence rows changed only selector lines and section digests, and no row id was added or removed (measured).' % prior['currentDisposition']
    elif i in ('OBS42-07', 'OBS42-08', 'OBS40-08'):
        basis, reasoning = 'unchanged-44-basis', 'Source44 disposition %s. Historical comparison records stay historical; the source45 comparison is OBS45-01 and the ported re-observation OBS45-03.' % prior['currentDisposition']
    else:
        basis, reasoning = 'unchanged-44-basis', 'Source44 disposition %s. commit-recovery-readonly.v3.md and carrier-dispatch.v3.json are byte-identical 44->45 (%s, %s).' % (prior['currentDisposition'], U['commit-recovery-readonly.v3.md'], U['carrier-dispatch.v3.json'])
    PRIOR_DISPOSITIONS.append({'id': i, 'source44Disposition': prior['currentDisposition'], 'currentDisposition': cur + ' (on source45)', 'basis': basis, 'reasoning': reasoning,
                               'evidence': (['receipts/probes/' + PBY[PROBE_FOR[i]]['result']['receipt'].split('/')[-1]] if i in PROBE_FOR else ['mapSources'])})
covered = {d['id'] for d in PRIOR_DISPOSITIONS}
for x in V44['newMustIssues'] + V44['newShouldIssues'] + V44['advisories'] + V44['observations'] + V44['priorFindingDispositions']:
    if x['id'] not in covered:
        GAPS.append('prior finding/advisory/observation without current disposition: ' + x['id'])

# ------------------------------------------------------------------------------------------------ items
DERIV = cw('derived-from-4.5-and-9.7-equals-the-published-value-forced-fields-and-fixed-fields-separated')
ITEMS = [
    {'id': 'CH45-CLOSED-WORLD-LAW', 'disposition': 'SUFFICIENT AND CONSISTENT; A MISSING NORMATIVE RECIPE IS NOW PUBLISHED; SCOPE CORRECT',
     'assessment': ('Source44 section 9.7 and the startup law named closed_world_v2 over "no manifest, no recognized entry points and no edges" without publishing its output, so the exact record was fixed only by the Python helper. '
                    'Source45 publishes the complete record in section 9.7 (3241-3261) and as provider-startup x-opensip-startup-law.preAnalyzeUnavailable.hostConversionClosedWorld; the hostConversion text now points to it "identically for both languages". Both copies equal the independently read value by parse and by this review\'s canonical bytes. '
                    'Derived from published law without the helper, using section 4.5 (2208-2258) and registered ClosedWorldV2 (bundle 1112-1180). exportsClosed must be unknown: closed needs ingredient 1, an observed manifest publishing nothing, and open needs an observed published entry. entryPointsRecognized is none because no recognizer or explicit origin exists before analysis. deadCodeRepairEligible is false because it needs closed, all and no nonliteral loading. '
                    'The other four members (nonliteralLoading none, dynamicDispatch not-applicable, externalConsumers unknown, reasons ["no-manifest"]) are lawful enum values fixed by the new publication rather than forced by 4.5. The derivation equals the published value, and the value cannot enable closed exports or repair (OBS45-07). '
                    'Scope: the text limits the value to this pre-analysis host conversion, records absent manifest and analysis observations, disclaims any proof that the repository has no dynamic loading or dispatch, and keeps coverage unknown and repair ineligible. No other ClosedWorldV2 producer is restricted, and the checker comment says so explicitly. '
                    'Registered bundle bytes are unchanged, and the startup and attribution-return schema $defs are unchanged; only x- annotations changed.'),
     'evidence': {'derivation': DERIV, 'publishedValue': cw('section-9.7-publishes-exactly-one-json-record-equal-to-the-startup-law-member-by-parse-and-canonical-bytes'),
                  'shapes': {k: CW[k]['observed'] for k in CW if k.startswith('shape-unchanged-')}}},
    {'id': 'CH45-BOTH-LANGUAGES-AND-COMMITTED-BYTES', 'disposition': 'CONFIRMED FOR BOTH LANGUAGES; NO IDENTITY CHANGE',
     'assessment': ('typescript-semantic (two planned stages) and rust-semantic (one) pre-analysis conversions on source45 reach DONE unavailable (T2-10/T2-20/T2-21 and P3-21/P3-31/P3-32). Every minted entry carries exactly the published record and admits through admit_coverage_result_v3, and all source45 case expectations hold. '
                    'The same exchanges on the verified source44 copy mint byte-identical CoverageResultV3 payloads with equal coverage2 identities, and the payload canonical bytes recomputed with this review\'s own serializer equal the foundation canonical form. '
                    'The correction therefore publishes law that source44 already produced: committed bytes are reproducible across versions and from the published record, and package RunIds are unchanged (OBS45-09). The value is language-independent by construction (no cargo or package manifest branch applies), and the prose says both languages.'),
     'evidence': {k: CW[k]['observed'] for k in CW if k.startswith(('typescript-semantic-', 'rust-semantic-'))}},
    {'id': 'CH45-CORRECTED-BOUNDARY', 'disposition': 'CONFIRMED: MODEL, CASES AND CHECKER NOW BIND THE PUBLISHED LAW',
     'assessment': ('Model: pre_analyze_unavailable_conversion now deep-copies STARTUP.LAW hostConversionClosedWorld instead of calling closed_world_v2 (complete model diff read; `import copy` present). '
                    'Positive reachability first, then a targeted discrimination. Mutating the in-process law member on source45 changes the minted closedWorld, and the source45 case expectations fail on it; restoring it passes again. The equivalent helper mutation on source44 changes the minted record, but the source44 cases do not detect it, because they carried no closedWorld expectation. That is the gap closed. '
                    'Checker (scratch copy, native pins regenerated inside scratch so the law checks are reached): unmutated passes 477/477. Mutating the law member alone is refused with "pre-analysis closedWorld differs from the exact section 9.7 record", and both conversion cases also fail. Mutating the section 9.7 record alone is refused with "section 9.7 does not publish the exact complete pre-analysis closedWorld record". '
                    'Mutating the retained helper alone is refused with "pre-analysis closedWorld differs from the retained helper\'s no-observation result", with cases still passing, which confirms the conversion no longer depends on the helper. The restored scratch passes, and its bytes equal the verified copy. '
                    'These are reference self-consistency controls; the decisive law assessment is CH45-CLOSED-WORLD-LAW (OBS45-08).'),
     'evidence': {'inProcess': {k: CW[k]['observed'] for k in CW if k.startswith(('source45-', 'source44-'))}, 'checker': {k: v['observed'] for k, v in CB.items()}}},
    {'id': 'CH45-CONSUMER-IMPACT', 'disposition': 'CONSISTENT; DISPLAY-ONLY OBSERVATION',
     'assessment': ('The only product consumer of ClosedWorldV2 members beyond the per-entry record is the workflows repair law, read at 800-974. Its selection is by relevant sourceUniverse, and its gate is the conjunction of deadCodeRepairEligible, so a pre-analysis conversion record cannot make repair eligible and yields REPAIR.CLOSED_WORLD_NOT_ESTABLISHED remedies carrying reasons ["no-manifest"]. '
                    'dynamicDispatch is not read by the gate. The five-field display summary may show nonliteralLoading none for conversion-only selections, but it is non-authoritative and disclaimed (OBS45-04). workflows-and-surfaces and the repair schema and selection model are byte-identical 44->45 (%s).')
     % json.dumps({k: U[k] for k in ('workflows-and-surfaces.md', 'repair_closed_world_selection.v1.py', 'evaluator3/repair.schema.json')}),
     'evidence': {'workflowsOwnersUnchanged': {k: U[k] for k in ('workflows-and-surfaces.md', 'repair_closed_world_selection.v1.py', 'evaluator3/repair.schema.json')}}},
    {'id': 'CH45-HISTORICAL-BATCH-PROSE', 'disposition': 'CONSISTENT; EDITORIAL DUPLICATION NOTED',
     'assessment': ('provider-target-attribution-return.schema.v2.json replaces three generic "Historical FactBatchV2" statements (standing, boundary.compilerWorkerTransport, missingAndIncomplete.missingToken) with the per-language historical payloads: delivery.v2 FactBatchV1 for typescript-semantic and rust-provider-protocol.v2 FactBatchV2 for rust-semantic. '
                    'This matches section 0, section 9.6 and fact-batch v3 as assessed on source44. Only x-opensip-return-law changed; there are no $defs or property changes, and the registered-schema shapes stay unchanged (measured). One editorial duplicated word remains (OBS45-05). '
                    'Earlier generic readings were ambiguous under those bytes and are not relabelled as reader errors.'),
     'evidence': {k: CW[k]['observed'] for k in CW if k.startswith('shape-unchanged-')}},
    {'id': 'CH45-NATIVE-CASES-REINDENT', 'disposition': 'CONFIRMED: TWO SEMANTIC EXPECTATION ADDITIONS; REST WHITESPACE',
     'assessment': OBSERVATIONS[5]['text'] + ' Both changed cases add only closedWorld expectations for every planned stage; no step, fixture or other expectation changed. The rationale\'s "two semantic case additions" are therefore additions inside two existing cases, not new case ids.',
     'evidence': {'cases': {k: v for k, v in CASES_STRUCT['cases'].items() if k != 'addedCases'}, 'fixtures': CASES_STRUCT['fixtures']}},
    {'id': 'CH45-PLANNING-V13', 'disposition': 'CONFIRMED (binds the actual changed normative inputs; predecessors preserved); ADV44-01 RETAINED',
     'assessment': ('v13 (%s...) binds %d inputs with no mismatch: v12 with native-evidence.md and provider-startup.schemas.v1.json updated, and nothing added or removed. All %d coverage sources are bound, and exactly those two changed. Layers v8-v12 are byte-identical to source44. The planning sources select v13, keep v12 as previous and record v11 in the history. '
                    'The planning checker reports 322 source-bound mappings and 54 planned failure cases, and the inventory checker 198 paths in 20 packages; stdout equals the companion v2 (%s). The six changed mapping rows (native-evidence sections 9-14) change only selector line numbers and section value digests. There are 24 report features, M0-M6, and 54 recovery cases, none executed. '
                    'The only architecture files changed are the three planning records. The unbound changed self-declared normative documents are the planning records themselves (excluded by standing).')
     % (PC['layerSha256']['13'][:12], PC['layerInputs']['13'], PC['coverageSourceKeys'], planning_stdout_equal_companion),
     'evidence': {k: PC[k] for k in ('layerSha256', 'layerInputs', 'priorLayersByteEqualToSource44', 'v13ChangedVsV12', 'coverageSourcesChangedVs44', 'coverageRowsChangedVs44', 'coverageRowsChangedOtherThanSelectorLinesAndValueDigest', 'coverageGroups', 'inventoryPaths', 'inventoryPackages', 'recoveryCasesNotExecuted', 'milestoneOrder', 'architectureDirFilesChangedVs44', 'adv4401')}},
    {'id': 'CH45-PINS-AND-REPORTS', 'disposition': 'CONFIRMED',
     'assessment': ('All %d entries of the five ledgers match the formal manifest (foundation %d, evaluator3 %d, native %d, security %d, workflows %d), with none added or removed. The union of changed pins is the attribution schema, checker, cases, model, startup schema, native-evidence.md and the sibling ledgers. '
                    'The delta files pinned by no ledger are the planning records, the workflows report and the evaluator3 ledger itself. The workflows report updates only the workflows source-pins digest. The generated native report bytes are unchanged 44->45 (%s): 477 cases, and its providerStartup summary carries no closedWorld count.')
     % tuple([PINS['totalPinEntries']] + [PINS['ledgers'][l]['entries'] for l in (FD + 'source-pins.v1.json', FD + 'evaluator3-source-pins.v1.json', NAT + 'source-pins.v2.json', DC + 'security/source-pins.v1.json', WFD + 'source-pins.v1.json')] + [U['native-evidence-report.v2.json']]),
     'evidence': {'changedPinUnion': PINS['changedPinUnion'], 'deltaFilesPinnedByNoLedger': PINS['deltaFilesPinnedByNoLedger']}},
    {'id': 'CH45-PACKAGE22', 'disposition': 'VERIFIED AS AUTHOR EVIDENCE; RUNIDS UNCHANGED (MEASURED)', 'assessment': 'See packageAssessment.', 'evidence': {k: v['ok'] for k, v in PK.items()}},
    {'id': 'CH45-CURRENT-REFERENCE', 'disposition': 'OWN EXECUTION PASSES; ROOT RECEIPTS CONSISTENT',
     'assessment': 'This review\'s six groups and 17 children pass on its own verified copy, unchanged before and after every group: native 477/477, query-projection 209 checks with 0 failed, execution-inputs 95, enumeration 54. The comparison is OBS45-01 and OBS45-02; historical source44 receipts are preserved and not relabelled.',
     'evidence': {k: RC[k] for k in ('codexReferenceChecks', 'codexPassed', 'codexSubjectManifestSha256', 'rootPassed', 'childrenEqualRoot', 'childrenDifferingFromHistoricalMine44')}},
]
WIRE_STARTUP_OWNERS = {k: U[k] for k in ('provider-handshake.schemas.v1.json', 'provider_wire_model.v1.py', 'provider_startup_model.v1.py', 'typescript-protocol2-order.v1.json', 'protocol3-transitions.v1.json',
                                         'fact-batch.schema.v3.json', 'occupancy-companion.schema.v1.json', 'provider_attribution_return_model.v2.py', 'delivery.v2.json', 'rust-provider-protocol.v2.json',
                                         'native-evidence.schemas.v2.json')}
if not all(WIRE_STARTUP_OWNERS.values()):
    GAPS.append('source44 wire/startup owners changed 44->45 beyond the recorded delta')
UNCH44_WIRE = []
for i, note in (('CH44-WIRE-HANDSHAKE', 'handshake schema, wire model, delivery.v2 and rust-provider-protocol.v2 byte-identical; not re-executed'),
                ('CH44-FACTBATCH-AND-OCCUPANCY', 'fact-batch v3, occupancy companion and attribution model byte-identical; the attribution-return schema changed annotation prose only (CH45-HISTORICAL-BATCH-PROSE); not re-executed'),
                ('CH44-STARTUP-OPEN-UNIVERSE', 'startup model byte-identical; startup schema $defs unchanged; the startup discriminator re-executed identically'),
                ('CH44-PRE-ANALYZE-UNAVAILABLE', 'payload, phase, correlation and process-fault law unchanged; the conversion closedWorld is now published (CH45 items); re-executed identically'),
                ('CH44-COVERAGE-AND-CANCELLATION', 'TS order table and protocol3 table byte-identical; re-executed identically'),
                ('CH44-RUST-COMMIT-REPRESENTATION', 'identity owners byte-identical'),
                ('CH44-CROSS-OWNER-CONSISTENCY', 'section 0 and the other cross-owner texts outside the section 9.7 closedWorld hunk unchanged')):
    if i not in V44ITEMS:
        GAPS.append('source44 item not found: ' + i)
        continue
    UNCH44_WIRE.append({'id': i, 'source44Disposition': V44ITEMS[i]['disposition'], 'standsOnSource45': True, 'basis': note})
ITEMS.append({'id': 'CH45-UNCHANGED-WIRE-STARTUP-BASIS', 'disposition': 'SOURCE44 PROVIDER WIRE/STARTUP ASSESSMENTS STAND ON NAMED UNCHANGED OWNERS',
              'assessment': ('The source44 wire and startup items stand as individually named unchanged-44 basis, not relabelled fresh. Owner bytes: %s. The wire discriminator (130 rows) was not re-executed because none of its owners changed; the startup discriminator (162 rows) was re-executed because the native model changed, and it is identical.') % json.dumps(WIRE_STARTUP_OWNERS),
              'unchanged44Items': UNCH44_WIRE, 'reexecution': REEXEC_EQUAL})

UNCH44_QUERY = ['CH43-AVAILABILITY-REPORTING', 'CH43-OBSERVATION-GRANTS-NOTHING', 'CH43-PATH-EDGE-ORIENTATION', 'CH43-CURSOR-BOUNDS-AND-PROSE']
ch = lambda n: {'stdoutEqualRoot': RC['children'][n + '.stdout']['equalRoot'], 'stdoutEqualHistoricalMine44': RC['children'][n + '.stdout']['equalHistoricalMine44']}
SCOPE_BASIS = [
    {'scope': 'five product contracts and incorporated schemas', 'basis': 'new-45 (native 9.7) + unchanged-44-basis (others)',
     'current45': 'identity, security, workflows and admission contracts and the README index byte-identical (%s); native-evidence changed only in section 9.7 (complete diff read; section 9.7 read completely); provider-startup changed only its law annotation; all six groups pass' % json.dumps({k: U[k] for k in ('identity-and-evidence.md', 'security-and-lifecycle.md', 'workflows-and-surfaces.md', 'admission-and-qualification.md', 'README.md')}),
     'unchanged44': 'source44 AR row assessments for byte-identical contracts; inheritedUnchanged44Read whole-file reads'},
    {'scope': 'architecture, tool, layout and report decisions', 'basis': 'unchanged-44-basis + current execution', 'current45': '%d docs/v2/architecture files; only the three planning records changed; planning and inventory checks pass' % PC['architectureDirFileCount'], 'unchanged44': 'source44 layout, build-plan and inventory decisions on byte-identical bytes'},
    {'scope': '198 files in 20 packages; 322 mappings; M0-M6; 24 report features; 54 recovery cases', 'basis': 'current execution', 'current45': 'measured: %d paths, %d packages, %d mappings (6 rows with selector-line/digest updates only), %s, %d report features, %d recovery cases not executed' % (PC['inventoryPaths'], PC['inventoryPackages'], PC['coverageMappings'], '-'.join([PC['milestoneOrder'][0], PC['milestoneOrder'][-1]]), PC['coverageGroups']['reportFeatures'], PC['recoveryCasesNotExecuted']), 'unchanged44': None},
    {'scope': 'native discovery, config, unitKind, allowJs, nested Cargo, clone normalization, custody', 'basis': 'new-45 diff + current execution',
     'current45': 'the native model delta is confined to the pre-analysis conversion closedWorld line and a comment; native group 477/477; native-consumer24-corrections %s and native-replay %s; ported native (%d rows) and custody (%d rows) identical to source44; nine native-v2 membership probes content-equal to root' % (ch('native-consumer24-corrections'), ch('native-replay'), PORTED_EQUAL['P45-PORTED-NATIVE']['rows'], PORTED_EQUAL['P45-PORTED-CUSTODY']['rows']),
     'unchanged44': 'source44 native discovery/custody assessments on unchanged code'},
    {'scope': 'enumeration default-vs-explicit binding, attribution and capture', 'basis': 'unchanged-44-basis + current execution',
     'current45': 'enumeration and execution-inputs owners byte-identical; children equal root and own source44 after removing path fields only; capture-join measurement identical; package binding-controls content-equal to root',
     'unchanged44': 'source44 S40-01 and ADV42-01 assessments on byte-identical owners'},
    {'scope': 'policy.test known-hit, universe and import', 'basis': 'unchanged-44-basis + current execution', 'current45': 'ported policy probe %d rows identical; policy-derivation child %s' % (PORTED_EQUAL['P45-PORTED-POLICY']['rows'], ch('policy-derivation')), 'unchanged44': 'policy_test_model.v3.py unchanged (%s)' % U['policy_test_model.v3.py']},
    {'scope': 'comparison counterfactuals, knowledge and identities', 'basis': 'unchanged-44-basis + current execution', 'current45': 'ported comparison probe %d rows identical; comparison-knowledge child %s' % (PORTED_EQUAL['P45-PORTED-COMPARISON']['rows'], ch('comparison-knowledge')), 'unchanged44': 'source44 AR-10/AR-11'},
    {'scope': 'nine command carriers and twenty operations; query availability, path, cursor and diagnostic decisions', 'basis': 'unchanged-44-basis + current execution', 'current45': 'ported query carriers %d rows identical; query-projection 209 checks pass; query owners and command inventory byte-identical (%s)' % (PORTED_EQUAL['P45-PORTED-QUERY']['rows'], json.dumps(dict(QOWN, **{'command-inventory.v3.json': U['command-inventory.v3.json']}))), 'unchanged44': ', '.join(UNCH44_QUERY) + ' (source43 items carried through source44 on byte-identical query owners)'},
    {'scope': 'repair2', 'basis': 'unchanged-44-basis + current execution', 'current45': 'ported repair:2 probe %d rows identical' % PORTED_EQUAL['P45-PORTED-REPAIR2']['rows'], 'unchanged44': 'repair_closed_world_selection.v1.py unchanged (%s)' % U['repair_closed_world_selection.v1.py']},
    {'scope': 'security, discovery, commit, recovery and read-only carrier boundaries', 'basis': 'unchanged-44-basis + current execution',
     'current45': 'security group stdout equal root, codex and own source44; ported read-only carrier %d rows and run-termination/commit-inventory %d rows identical' % (PORTED_EQUAL['P45-PORTED-CARRIER']['rows'], PORTED_EQUAL['P45-PORTED-RUNTERM']['rows']),
     'unchanged44': 'carrier-dispatch.v3.json (%s) and commit-recovery-readonly.v3.md (%s) unchanged' % (U['carrier-dispatch.v3.json'], U['commit-recovery-readonly.v3.md'])},
    {'scope': 'evaluator, import and termination bridges', 'basis': 'unchanged-44-basis + current execution',
     'current45': 'children full-replay %s, execution-replay %s, candidate-replay %s, composition %s, analysis-seal %s, provider-attribution-return %s, faults %s, atoms %s; ported section 7 termination %d rows identical'
                  % (ch('full-replay'), ch('execution-replay'), ch('candidate-replay'), ch('composition'), ch('analysis-seal'), ch('provider-attribution-return'), ch('faults'), ch('atoms'), PORTED_EQUAL['P45-PORTED-TERM7']['rows']),
     'unchanged44': 'composition, replay and identity owners byte-identical (%s, %s, %s)' % (U['evaluator-composition-contract.v3.md'], U['evaluator_replay_model.v3.py'], U['identity-model.v3.py'])},
]
ITEMS.append({'id': 'CH45-SCOPE-PRESERVATION', 'disposition': 'SOURCE44 SCOPE RETAINED; NAMED BASIS',
              'assessment': 'Each retained scope names its current source45 execution and its individually named unchanged-44 basis. Passing suites are corroboration, not assessment. The source45 change reaches native section 9.7, the startup law, the native model conversion, the checker, two cases and the attribution-return annotations. Its consumer effect on the workflows repair owner, whose bytes are unchanged, is assessed in CH45-CONSUMER-IMPACT.',
              'scopeBasis': SCOPE_BASIS, 'portedProbes': PORTED_EQUAL})
