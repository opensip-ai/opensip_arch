"""B02 — completion builder for the bounded NONBLIND V23-S1/S2/S3 source-gap assessment. Supersedes the v1 b01 builder, which
was executed on completion and failed honestly because the interrupted p04 never wrote its summary receipt (receipt retained in
v1). Reads p01-p03 (v1 receipts) and s01-s04, p05 (completion receipts); gates on the measured facts; records rehearsal
outcomes as measured. Writes assessment.json into the original v1 runtime."""
import hashlib, json, os, time

V1 = '/tmp/opensip-design-corrections/claude-consumer23-gap-assessment.v1'
V2 = '/tmp/opensip-design-corrections/claude-consumer23-gap-assessment.v2'
RC1, RC2 = os.path.join(V1, 'receipts'), os.path.join(V2, 'receipts')
S36 = '/tmp/opensip-design-corrections/candidate-subject.v36'
REV = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews'
V36 = '/tmp/opensip-design-corrections/claude-independent-design.v36'
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
j = lambda d, n: json.load(open(os.path.join(d, n)))
p01, p02, p03 = j(RC1, 'p01-s1-endpoint.json'), j(RC1, 'p02-s2-d9.json'), j(RC1, 'p03-s3-availability.json')
s01, s02, s03, s04, p05 = (j(RC2, n) for n in ('s01-p04-status.json', 's02-poll-p04.json', 's03-digest-bearers.json', 's04-retained-schema-digests.json',
                                               'p05-successor-rehearsal2.json'))
b01cmd = j(os.path.join(RC1, 'b01_build'), 'command.json')
b01err = open(os.path.join(RC1, 'b01_build', 'stderr.txt')).read()
V36J = j(V36, 'review.json')
CONS = j(V1, 'consumer23-interim-review.json')
issues = {i['id']: i for i in CONS['newShouldIssues']}

# ------------------------------------------------------------------ gates on measured facts
assert sha(os.path.join(REV, 'candidate-subject.v36.json')) == 'a729406b9de0d865294884f7575ea943c0935437091389e2acebe8e5aedb4235'
assert sha(os.path.join(V1, 'consumer23-interim-review.json')) == '77cfab1f6f2cea89a9b8d301e725ec69314e6b94298b0707e565305fd9c66a66'
assert sha(os.path.join(V36, 'review.json')) == 'fa1b7f4843ac82e1ecbf6d4cacde42ad9922f7fb41edecac5d8464ac58bee921'
assert sorted(issues) == ['V23-S1', 'V23-S2', 'V23-S3']
o1 = p01['observations']
assert o1['wrapperDisagreesWithSection2'] and o1['wrapperDisagreesWithHelper'] and o1['step1ShapesAgreeEverywhere'] and o1['wrapperEnvelopeValid']
assert o1['publicWrapperForMissingCoordinate'] == ['REQUEST.PRECONDITION_FAILED', 'QUERY.PARAMS_MALFORMED'] and not p01['multiVertexClauseEverPopulated']
assert p02['section10DisagreesWithD9'] == ['confidence-floor-unmet', 'language-tier-unsupported', 'required-relation-missing']
assert p02['modelDisagreesWithD9'] == ['budget-exhausted', 'confidence-floor-unmet', 'language-tier-unsupported', 'required-relation-missing']
assert p02['modelDisagreesWithSection10'] == ['budget-exhausted']
assert all(v for v in p02['ownerSentences'].values() if isinstance(v, bool)) and p02['candidateRunTermination']['equalsD9OwnerForAll']
m3 = p03['observedMapping']
assert (m3['unavailable'], m3['purged'], m3['expired'], m3['corrupt']) == ('evidence.missing', 'evidence.purged', 'evidence.expired', 'evidence.corrupt')
assert not p03['contractNamesDetailForUnavailable'] and not p03['registryHasEvidenceUnavailable'] and not p03['existingControlsByState']['unavailable']
assert b01cmd['exit'] == 1 and 'p04-successor-rehearsal.json' in b01err
assert s01['completedFoundation']['passed'] is False and s01['kitNativeReport']['result'] == 'PASS' and s01['completedQueryControls']['passed']
assert s04['anyPackage13ExportCommitsChangedSchemaDigest']['native/native-evidence.schemas.v2.json'] is True
assert s04['anyPackage13ExportCommitsChangedSchemaDigest']['workflows/schemas/evaluator3/graph-query.schema.json'] is False
assert p05['v1KitReproducesV1Patch'] and p05['variantBOmitsSchemaEdit'] and p05['frozen36DriftAfter'] == 0
assert all(v['equal'] for v in p05['kitS2'].values()) and p05['kitS2DisclosurePresent'] and p05['kitS3ContractNamesUnavailableMapping']
ks1 = p05['kitS1']
# Without a Run the public wrapper stops at its Run-presence check (QUERY.VIEW_UNKNOWN), which proves the absent coordinate PASSED
# closed-schema admission; the ENDPOINT_AMBIGUOUS refusal itself is proved by the real-Run query control and the helper.
assert ks1['package-absent-coordinate'] == {'rawRequestSchemaAdmits': True, 'rawResponseEndpointAdmits': False,
                                            'wrapperWithoutRun': 'QUERY.VIEW_UNKNOWN', 'helper': 'QUERY.ENDPOINT_AMBIGUOUS'}
assert p05['queryControls']['passed'] and all(p05['queryControls']['new'].values())
assert ks1['package-empty-coordinate']['wrapperWithoutRun'] == ks1['package-empty-coordinate']['helper'] == 'QUERY.PARAMS_MALFORMED'
assert p05['allSuitesExitZero'] and p05['variantB']['sameOutcomesAsFrozen36'] and p05['variantA']['sameOutcomesAsFrozen36'] is False
planning_err = open(os.path.join(RC2, 'p05-kit-planning-check_implementation_planning.stderr')).read().strip().splitlines()[-1]
assert p05['planningExitCodes']['planning-check_implementation_planning'] == 1 and planning_err == 'ValueError: Planning source changed: query'

starts = {}
for root in (RC1, RC2):
    for d in sorted(os.listdir(root)):
        cj = os.path.join(root, d, 'command.json')
        if os.path.isfile(cj):
            c = json.load(open(cj))
            starts[os.path.relpath(os.path.join(root, d), '/tmp/opensip-design-corrections')] = {'startedUtc': c['startedUtc'], 'exit': c['exit']}
exp = os.path.join(V1, 'expected-before-probes.json')
exp_written = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(os.path.getmtime(exp)))
first_probe = min(v['startedUtc'] for k, v in starts.items() if 'v1/receipts/p0' in k)
assert exp_written <= first_probe

touched = set(p05['patchV2']['files'])
rows36 = []
for mp in ('fDispositions', 'evaluationResidualDispositions', 'arDispositions', 'fwDispositions', 'inheritedResidualDispositions', 'scopedReviewOwnerDispositions'):
    for rid, row in V36J[mp].items():
        own = row.get('currentOwnerFiles') or row.get('currentOwnerSelectors') or []
        paths = {o.split('#')[0].split(' ')[0] for o in own if isinstance(o, str)}
        hit = sorted(paths & touched)
        if hit:
            rows36.append({'map': mp, 'row': rid, 'ownersTouched': hit, 'statusChangeOn36': row.get('statusChangeOn36')})

suitesB = {x['name']: x['returncode'] for x in p05['suites']}
A = {}
A['assessment'] = 'Bounded NONBLIND source gap assessment of V23-S1, V23-S2 and V23-S3 on frozen candidate36'
A['standing'] = ('Actual Claude, source-review origin ce3dec3b-0620-44ec-86e6-129b0e25cb1b. NOT blind consumer B, NOT the final application '
                 'review, NOT fresh-blind standing, NOT acceptance of any successor. My candidate36 technical ACCEPT (review.json fa1b7f48...) is '
                 'historical evidence of that review, not a resolution of these findings. Grants no application outcome, architecture readiness, '
                 'activation or implementation authority.')
A['provenance'] = {
    'originalDispatch': {'runtime': V1, 'label': 'bounded nonblind gap assessment of an interim captured consumer report (label preserved as historical dispatch)',
                         'process': 'ended with a progress-only response while the p04 rehearsal ran in the background; no assessment artifact was written by it'},
    'completion': {'runtime': V2, 'standing': 'continuation of the same origin to complete the original assessment; not a new independent origin; the previous CLI process had ended',
                   'dispatchSha256': sha(os.path.join(V2, 'dispatch.json'))},
    'consumerReport': {'path': os.path.join(V1, 'consumer23-interim-review.json'), 'sha256': sha(os.path.join(V1, 'consumer23-interim-review.json')),
                       'currentStanding': ('root states these bytes equal the completed original blind consumer23 final report and that its final three '
                                           'SHOULD equal this captured input; I verified only the digest of my copy and did not access the consumer or its outputs'),
                       'verdictField': CONS['verdict'], 'scope': ['V23-S1', 'V23-S2', 'V23-S3']},
    'subject': {'manifest': os.path.join(REV, 'candidate-subject.v36.json'), 'sha256': 'a729406b9de0d865294884f7575ea943c0935437091389e2acebe8e5aedb4235', 'snapshot': S36},
    'myPriorReview': {'path': os.path.join(V36, 'review.json'), 'sha256': sha(os.path.join(V36, 'review.json')), 'verdict': V36J['verdict']}}
A['boundaries'] = {'noContactWithConsumerOrItsOutputs': True, 'noAuthorAssemblyOrFinalSourceAuthorFiles': True, 'noPrivateSessionLogs': True,
                   'consumerHelpersNotRepaired': True, 'consumerExportedRunsNotClaimedRootAdmitted': True, 'frozenSourceLiveReadOnly': True,
                   'writes': 'v1 assessment artifacts, v1 builder receipt, and the v2 completion runtime only', 'noCommitPushAgentsOrProductWork': True,
                   'modelCodeStanding': 'model behaviour was measured as evidence only, never used to supply a consumer-visible recipe'}
A['expectedLawBeforeProbes'] = {'file': os.path.join(V1, 'expected-before-probes.json'), 'sha256': sha(exp), 'writtenUtc': exp_written, 'firstProbeStartedUtc': first_probe,
                                'writtenBeforeAnyProbe': True, 'heldFor': ['S1', 'S2', 'S3'],
                                'notAnticipated': ['the fixture-drift and retained-Run consequences of editing native-evidence.schemas.v2.json (found by rehearsal, s03/s04/p05)']}
sh = p01['shapes']
A['findings'] = {
 'V23-S1': {
  'consumerClaim': issues['V23-S1'],
  'classification': 'REAL SOURCE INCONSISTENCY (confirmed); not consumer error',
  'severity': 'SHOULD - same class request-rejected, exit 2 and errorCode REQUEST.PRECONDITION_FAILED, different DomainDetail and remedy; no soundness effect',
  'exactSelectors': ['workflows/query-projection-contract.v3.md s2 "Fault precedence" steps 1-2 (lines 43-47)',
                     'workflows/query-projection-contract.v3.md s7 rows at lines 165 and 167; s8 steps 1 and 5 (lines 181, 185)',
                     'workflows/schemas/evaluator3/graph-query.schema.json#/$defs/GraphEndpoint allOf[0] (kind=package then required packageManifestPath); $ref from GraphNeighborsParams.endpoint, GraphPathParams.start/target, GraphReachParams.start and from response rows',
                     'public-detail-registry.v1.json QUERY.ENDPOINT_AMBIGUOUS and QUERY.PARAMS_MALFORMED (both select the contract and the schema)',
                     'workflows/query_projection_model.v3.py _validate_request (schema first, line 1219) -> effective_params (1454) -> parse_endpoint_syntax (404-412); inventory_vertices (690-719)'],
  'observedBehaviour': {'packageWithoutCoordinate': {k: sh['package-without-packageManifestPath'][k] for k in ('rawSchemaGraphEndpoint', 'rawSchemaGraphQueryRequestV1', 'publicWrapper', 'parseEndpointSyntaxHelper')},
                        'section2Predicts': 'QUERY.ENDPOINT_AMBIGUOUS', 'everyOtherStep1ShapeAgrees': o1['step1ShapesAgreeEverywhere'],
                        'multiVertexClauseEverPopulated': p01['multiVertexClauseEverPopulated'], 'receipt': 'v1/receipts/p01-s1-endpoint.json'},
  'assessmentOfConsumerReading': ('Conflict correctly found. Its reading I-Q4 (re-admit with a placeholder coordinate) is not published law and would '
                                  'itself be an invented recipe; both of its smallest fixes are lawful.'),
  'recommendedCorrection': {
   'choice': 'preserve the explicit s2 distinction (request-side endpoint $def); alternative recorded',
   'why': ('s2 is the specific endpoint law and deliberately separates malformed syntax from an absent package coordinate with its own registered '
           'detail and remedy; QUERY.ENDPOINT_AMBIGUOUS has no other reachable route in the reference (inventory_vertices cannot mark a tuple '
           'ambiguous); response rows must keep the strict GraphEndpoint.'),
   'edits': {'graph-query.schema.json': 'add $defs/GraphRequestEndpoint (kind=package may omit packageManifestPath; packageManifestPath forbidden on non-package); the four request params reference it',
             'query-projection-contract.v3.md': ['s2 step 1: present non-LogicalPath coordinate is malformed', 's2 step 2: "whose packageManifestPath is absent"',
                                                 's2: paragraph naming the request/response schema split', 's7 row label', 's8 step 1: absent coordinate passes closed admission and is refused by s2 step 2 before vertex lookup'],
             'query_projection_model.v3.py': 'parse_endpoint_syntax: absent -> ENDPOINT_AMBIGUOUS; present empty/non-string -> PARAMS_MALFORMED'},
   'regressionControls': list(p05['queryControls'].get('new', {}))[:5],
   'measuredOnRehearsal': {'kitS1': ks1, 'queryControls': p05['queryControls']},
   'alternative': ('Keep the schema and publish that an absent coordinate is a closed-schema refusal (PARAMS_MALFORMED): no schema or planning-input '
                   'change for S1, but QUERY.ENDPOINT_AMBIGUOUS then has no reachable graph route and s2 step 2 and the s7 row must be rewritten.')},
  'crossOwners': ['workflows query contract, graph-query schema, query model, query checker', 'graph-query.schema.json is a planning layer4 normative input (s03)',
                  'public detail registry, D9: unchanged', 'no retained Run commits the graph-query schema digest (s04)', 'no 107-row owner is a query file']},
 'V23-S2': {
  'consumerClaim': issues['V23-S2'],
  'classification': 'REAL SOURCE INCONSISTENCY (confirmed) inside the native owner against the D9 owner it states it inherits unchanged; NOT a lawful per-requirement/whole-Run scope distinction',
  'severity': 'SHOULD - whole-Run termination reasonCodes diverge for three deficiencies (class indeterminate and exit 3 unchanged); no D9 class, exit or vocabulary change',
  'exactSelectors': ['docs/v2/contracts/product-v1/native-evidence.md s10 rows language-tier-unsupported (2907), confidence-floor-unmet (2909), required-relation-missing (2910), column "Existing code"',
                     'native-evidence.md s10 "inherits d9-exit-contract.v1.14.json unchanged" (3051); s4.6 "public D9 termination ... still the s10 class/code columns" (2148-2153)',
                     'docs/coop/artifacts/d9-exit-contract.v1.14.json#/codeMaps/deficiencyToReasonCode; #/causeModel/codeDerivation; goldens analysis-required-coverage-missing, analysis-language-tier-unsupported, analysis-confidence-floor-unmet, repair-verification-indeterminate',
                     'workflows/schemas/evaluator3/common.schema.json#/$defs/D9Deficiency description; workflows-and-surfaces.md 783-796',
                     'native/native-evidence.schemas.v2.json publicD9Termination; native/native_evidence_model.v2.py run_termination (3668), D9_MAP, d9_map'],
  'observedBehaviour': {'perDeficiency': p02['perDeficiency'], 'section10DisagreesWithD9': p02['section10DisagreesWithD9'], 'modelDisagreesWithD9': p02['modelDisagreesWithD9'],
                        'ownerSentences': p02['ownerSentences'], 'receipt': 'v1/receipts/p02-s2-d9.json'},
  'whyNoPerRequirementDistinction': p02['publishedPerRequirementD9CodeReason'],
  'budgetMappingMismatch': {'finding': ('The native model is inconsistent with its own s10 row and D9 for budget-exhausted on the deficient-entry route: '
                                        'run_termination maps a deficient entry carrying budget-exhausted to VERDICT.INDETERMINATE, while s10, D9_MAP[budget-exhausted], '
                                        'stage_authority(budget-exhausted) and D9 codeMaps all give COVERAGE.BUDGET_EXHAUSTED. The published sources agree; the model does not.'),
                            'observed': p02['perDeficiency']['budget-exhausted'], 'correctedBy': 'the same run_termination change (D9_DEFICIENCY_REASON_CODE)'},
  'assessmentOfConsumerReading': ('Conflict correctly found and the right reading applied (the D9 exit contract governs whole-Run terminations). Its first '
                                  'fix option would invent a distinction the sources refute; its second (align the three codes) is correct.'),
  'recommendedCorrection': {
   'edits': {'native-evidence.md': ['s10 Existing code: language-tier-unsupported -> COVERAGE.LANGUAGE_TIER_UNSUPPORTED; confidence-floor-unmet -> COVERAGE.CONFIDENCE_FLOOR_UNMET; required-relation-missing -> COVERAGE.REQUIRED_RELATION_MISSING',
                                    's10: one paragraph stating the column IS the D9 codeMaps for D9Deficiency members and verdict-indeterminate for the four native-only outcomes (one mapping)',
                                    's10: disclosure that the publicD9Termination annotation in native-evidence.schemas.v2.json keeps an incomplete older parenthetical, that s10 governs, and why its bytes stay unchanged'],
             'native_evidence_model.v2.py': 'D9_DEFICIENCY_REASON_CODE mirrors the D9 map; run_termination uses it (also fixes budget-exhausted)',
             'native-cases.v2.json': 'case run-termination-derives-the-d9-exit-contract-reason-code-for-each-deficiency (five D9 members + one native-only)'},
   'notChanged': ['native-evidence.schemas.v2.json bytes (see correctionToMyOwnV1Patch)', 'D9 classes, exits, reason codes, D9Deficiency, DomainDetailCode, D9_MAP keys (check-integration requires D9_MAP keys to be registered details)'],
   'measuredOnRehearsal': {'kitS2': p05['kitS2'], 'section10Rows': p05['kitS2Section10Rows'], 'nativeReport': p05.get('nativeReport')}},
  'helperVersusFullD9Limitations': [
   'run_termination returns ONE reason code chosen by native PRECEDENCE_V2; the D9 cause model derives an ordered reasonCodes list [map(deficiency)] + secondaryDeficiencies (golden analysis-multiple-deficiencies gives two codes). The helper is not a full D9 derivation and is not corrected into one here.',
   'run_termination emits no runId or coverageId and performs no cross-family reduction (faultCause > rejectionCause > deficiency); those remain host/D9 derivation duties.',
   'd9_map is keyed by public detail (plus the provider-unavailable/capability-missing alias), not by deficiency: d9_map("provider-unavailable") and the three corrected deficiencies refuse; that is consistent with check-integration and is not a code-map.',
   'This assessment fixes only the deficiency-to-reason-code map. How an evaluator proof cause such as required-cell-unsatisfied selects a whole-Run D9Deficiency is not decided here.'],
  'correctionToMyOwnV1Patch': {'finding': ('My first proposed patch (v1 successor-v23-gaps.patch, 8222d978...) also rewrote the publicD9Termination text inside '
                                           'native-evidence.schemas.v2.json. Rehearsal showed that is not a text-only change: check-identity\'s fixture-drift guard '
                                           'failed (native-cases fixture declares the old document digest), and all 13 package13 retained Runs commit that registered '
                                           'schema document\'s digest, so the edit would strand retained evidence. The recommended v2 patch leaves those bytes unchanged '
                                           'and discloses the stale annotation in s10 instead.'),
                               'evidence': {'foundationFailure': s01['completedFoundation'], 'digestBearers': s03['nonLedgerBearers'].get('docs/coop/design-corrections/native/native-evidence.schemas.v2.json'),
                                            'package13CommitsDigest': s04['package13ExportOccurrences'], 'variantAReplay': {'sameOutcomesAsFrozen36': p05['variantA']['sameOutcomesAsFrozen36'], 'positiveRefusals': p05['variantA']['refusals']}}},
  'crossOwners': ['native contract s10, model, cases', 'D9 exit-contract artifact unchanged (the governing map)', 'workflows-and-surfaces unchanged',
                  'native-evidence.md is a planning layer4 normative input (s03)', '15 of the 107 rows own native-evidence.md; a successor review must re-read them']},
 'V23-S3': {
  'consumerClaim': issues['V23-S3'],
  'classification': 'REAL BUT NARROW NORMATIVE GAP (confirmed missing recipe); not an inconsistency and not consumer error',
  'severity': 'SHOULD (small) - one consumer-visible detail decided only by model code',
  'exactSelectors': ['workflows/query-projection-contract.v3.md s7 availability paragraph (160) and table (173-174)', 'identity-and-evidence.md s5 (1610-1614, 1642-1656)',
                     'foundation/identity-schemas.v3.json availability.state enum', 'public-detail-registry.v1.json evidence.* records',
                     'workflows/query_projection_model.v3.py AVAIL_REFUSE (1413-1419); foundation/identity-model.v3.py EvidenceUnavailable (616-619)'],
  'observedBehaviour': {'publicWrapperOverRealAdmittedRun': p03['publicWrapperByAvailability'], 'observedMapping': m3, 'identityOwnerTermination': p03['identityModelUnavailabilityTermination'],
                        'existingControlsByState': p03['existingControlsByState'], 'receipt': 'v1/receipts/p03-s3-availability.json'},
  'assessmentOfConsumerReading': 'Correct and conservative: it invented no detail.',
  'recommendedCorrection': {'edits': {'query-projection-contract.v3.md': ['s7 paragraph: purged/expired/corrupt/unavailable -> HOST.IO_FAILURE (host-io) with evidence.purged/expired/corrupt/missing; no evidence.unavailable member; retained and partial do not refuse by themselves',
                                                                          's7 table: one row per refusing availability state']},
                            'model': 'none', 'regressionControls': list(p05['queryControls'].get('new', {}))[5:], 'measuredOnRehearsal': p05['queryControls']},
  'crossOwners': ['workflows query contract and checker only', 'identity s5, registry: unchanged']}}
A['additionalObservations'] = [
    {'id': 'OBS-1', 'finding': 'The multi-vertex ENDPOINT_AMBIGUOUS clause is unreachable in the reference (inventory_vertices keys by the full tuple).', 'standing': 'advisory; model evidence (p01)'},
    {'id': 'OBS-2', 'finding': 'An unregistered availability value ("not-a-state") is ignored and the query succeeds, although identity availability is a closed enum.', 'standing': 'advisory; outside V23-S3 (p03)'},
    {'id': 'OBS-3', 'finding': 'traverse_projected_graph applies no endpoint syntax admission.', 'standing': 'documented internal algorithm helper; no public consequence (p01)'}]
A['rehearsal'] = {
    'p04Interrupted': {'status': s01['phaseOutputs'], 'lastWrite': s01['latestP04OutputWrite'], 'poll': {k: s02[k] for k in ('anyNewWriteDuringPoll', 'completedDuringPoll', 'conclusion')},
                       'completedPhases': {'queryControls': s01['completedQueryControls'], 'native': s01['kitNativeReport'].get('result'), 'foundation': s01['completedFoundation']},
                       'receipts': ['v2/receipts/s01-p04-status.json', 'v2/receipts/s02-poll-p04.json']},
    'b01': {'exit': b01cmd['exit'], 'reason': 'FileNotFoundError: p04-successor-rehearsal.json (never written by the interrupted p04)', 'receipt': 'v1/receipts/b01_build/'},
    'p05': {'variantA': {'sameOutcomesAsFrozen36': p05['variantA']['sameOutcomesAsFrozen36'], 'positiveRefusals': p05['variantA']['refusals']},
            'variantB': {'package13SameOutcomesAsFrozen36': p05['variantB']['sameOutcomesAsFrozen36'], 'suites': suitesB, 'allSuitesExitZero': p05['allSuitesExitZero'],
                         'reports': p05.get('reports'), 'launcher': p05.get('launcher'), 'planningExitCodes': p05['planningExitCodes'],
                         'planningFailure': {'check': 'check_implementation_planning.py', 'lastStderrLine': planning_err,
                                             'reading': ('expected successor consequence, not a patch defect: implementation-coverage.v1.json pins the query schema '
                                                         'source and native-evidence.md (s03); the checker stops at the first changed pinned source, so a successor '
                                                         'planning input layer is owed; check_repository_file_inventory passes')},
                         'pinsSealedAfterSuites': p05['pinsStillSealedAfterSuites'], 'generatedReportsChanged': p05['generatedAfterSuites']},
            'receipt': 'v2/receipts/p05-successor-rehearsal2.json'}}
A['recommendedSuccessor'] = {
    'patch': p05['patchV2'], 'supersedes': {'path': 'v1/successor-patch/successor-v23-gaps.patch', 'sha256': p05['v1Patch']['sha256'], 'reason': 'contained the native schema byte edit'},
    'alsoOwedOutsideThePatch': ['re-seal the five pin ledgers for the changed files and each other', 'commit the regenerated workflows-report.v1.json (and native report if its bytes changed)',
                                'a successor planning input layer: native-evidence.md and graph-query.schema.json are pinned by implementation-normative-inputs.v4.json, implementation-coverage.v1.json and implementation-planning-sources.v1.json (layer4 cannot be retained)',
                                'a fresh review of the exact successor bytes'],
    'layer4InputsTouched': p05['layer4InputsTouched'],
    'standing': 'rehearsed only in disposable copies; frozen candidate36 drift 0; not a successor and not acceptance'}
A['doesSource36AcceptanceReopen'] = {
    'answer': 'YES',
    'explanation': ('My source36 ACCEPT stated no new MUST or SHOULD. Three confirmed consumer-visible defects in published candidate36 law are '
                    'SHOULD-level issues that review did not find, so it cannot stand as final design acceptance of the affected surfaces. The record '
                    'stays historical and unedited. No MUST: class, exit, errorCode, soundness and D9 vocabulary are unaffected. A successor carrying '
                    'the recommended patch, re-sealed pins, regenerated reports, a successor planning input layer and a fresh review of its bytes is '
                    'needed before design acceptance can be claimed again.'),
    'myPriorReviewMadeNoContraryClaim': True, 'rowsOwningTouchedFiles': rows36}
A['carriedObligations'] = {'TCB-SCOPE-01': 'one shared assumption over 13 dependent rows; not closed; no qualification', 'condition2Obligations': 28,
                           'productGates': {'count': 32, 'performed': 0, 'condition5': 'NOT MET'}, 'plannedRecoveryCases': {'count': 54, 'executed': 0},
                           'residualProposals': '30 PENDING', 'd9': 'DR-007 / DR-011-R08 implementation obligation persists',
                           'authority': 'no final application, architecture-readiness, activation or implementation authority'}
A['limits'] = [
    'Source/reference assessment only; no product implementation, qualification or readiness.',
    'S1 and S3 were measured on the reference query model (S3 over the query checker\'s own synthetic admitted Run); S2 on native reference helpers and the D9 artifact. No retained product Run, blind reconstruction or consumer helper was used.',
    'Only V23-S1/S2/S3 were assessed; the consumer report\'s other content was not.',
    'Successor edits were rehearsed only in disposable copies; root owns real sealing, report regeneration, the planning layer and freezing.',
    'The S1 choice between two lawful corrections is a normative judgement; the alternative is recorded.',
    'The helper-versus-full-D9 limitations above remain open.']
A['probeErrorsAndSlips'] = [
    'A progress message first described the captured report verdict as ACCEPT before reading the field; it is CHANGES_REQUIRED. No artifact relied on it.',
    'My v1 proposed patch included the native schema annotation edit; rehearsal exposed its fixture and retained-Run consequences and it is superseded by the v2 patch.',
    'The v1 process ended while p04 was running; p04 was stopped during the evaluator3 launcher and never wrote its summary; b01 then failed on that missing receipt. Both are retained.',
    'My first b02 run failed its own S1 gate: it expected QUERY.ENDPOINT_AMBIGUOUS from a public-wrapper call WITHOUT a Run, but that call is refused QUERY.VIEW_UNKNOWN at the Run-presence check after closed admission. The gate now asserts the measured values; the ENDPOINT_AMBIGUOUS refusal is proved by the real-Run query control (receipt v2/receipts/b02_build/ retained).']
A['receipts'] = {os.path.relpath(os.path.join(root, f), '/tmp/opensip-design-corrections'): sha(os.path.join(root, f))
                 for root in (RC1, RC2) for f in sorted(os.listdir(root)) if f.endswith('.json') and not f.startswith('i0')}
A['commandReceipts'] = starts
out = os.path.join(V1, 'assessment.json')
json.dump(A, open(out, 'w'), indent=1, default=str)
print('findings', {k: v['classification'][:48] for k, v in A['findings'].items()}, '| reopen', A['doesSource36AcceptanceReopen']['answer'])
print('variantA same', p05['variantA']['sameOutcomesAsFrozen36'], '| variantB same', p05['variantB']['sameOutcomesAsFrozen36'], '| suites', suitesB, '| planning', p05['planningExitCodes'])
print('assessment.json', sha(out))
