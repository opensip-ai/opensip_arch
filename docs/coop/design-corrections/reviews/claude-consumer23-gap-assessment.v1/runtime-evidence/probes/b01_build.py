"""B01 — build assessment.json for the bounded nonblind V23-S1/S2/S3 gap assessment from this runtime's receipts. Every gating
claim is asserted against the receipt that measured it before anything is written."""
import hashlib, json, os, time

BASE = '/tmp/opensip-design-corrections/claude-consumer23-gap-assessment.v1'
RC = os.path.join(BASE, 'receipts')
S36 = '/tmp/opensip-design-corrections/candidate-subject.v36'
REV = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews'
V36 = '/tmp/opensip-design-corrections/claude-independent-design.v36'
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
rc = lambda n: json.load(open(os.path.join(RC, n)))
p01, p02, p03, p04 = rc('p01-s1-endpoint.json'), rc('p02-s2-d9.json'), rc('p03-s3-availability.json'), rc('p04-successor-rehearsal.json')
V36J = json.load(open(os.path.join(V36, 'review.json')))
CONS = json.load(open(os.path.join(BASE, 'consumer23-interim-review.json')))
issues = {i['id']: i for i in CONS['newShouldIssues']}

# ------------------------------------------------------------------ gates
assert sha(os.path.join(REV, 'candidate-subject.v36.json')) == 'a729406b9de0d865294884f7575ea943c0935437091389e2acebe8e5aedb4235'
assert sha(os.path.join(BASE, 'consumer23-interim-review.json')) == '77cfab1f6f2cea89a9b8d301e725ec69314e6b94298b0707e565305fd9c66a66'
assert sha(os.path.join(V36, 'review.json')) == 'fa1b7f4843ac82e1ecbf6d4cacde42ad9922f7fb41edecac5d8464ac58bee921'
o1 = p01['observations']
assert o1['wrapperDisagreesWithSection2'] and o1['wrapperDisagreesWithHelper'] and o1['step1ShapesAgreeEverywhere'] and o1['wrapperEnvelopeValid']
assert o1['publicWrapperForMissingCoordinate'] == ['REQUEST.PRECONDITION_FAILED', 'QUERY.PARAMS_MALFORMED'] and not p01['multiVertexClauseEverPopulated'] and p01['ownersUnchangedAfter']
assert p02['section10DisagreesWithD9'] == ['confidence-floor-unmet', 'language-tier-unsupported', 'required-relation-missing']
assert p02['modelDisagreesWithD9'] == ['budget-exhausted', 'confidence-floor-unmet', 'language-tier-unsupported', 'required-relation-missing']
assert all(v for v in p02['ownerSentences'].values() if isinstance(v, bool)) and p02['candidateRunTermination']['equalsD9OwnerForAll'] and p02['ownersUnchangedAfter']
assert all(not r['failuresUnderCandidate'] for r in p02['existingNativeRunTerminationCasesUnderCandidate']) and p02['checkIdentityProjectionControlUnderCandidate']['stillSatisfied']
m3 = p03['observedMapping']
assert m3['unavailable'] == 'evidence.missing' and m3['purged'] == 'evidence.purged' and m3['expired'] == 'evidence.expired' and m3['corrupt'] == 'evidence.corrupt'
assert not p03['contractNamesDetailForUnavailable'] and not p03['registryHasEvidenceUnavailable'] and not p03['existingControlsByState']['unavailable'] and p03['ownersUnchangedAfter']
assert all(p03['publicWrapperByAvailability'][s]['envelopeValid'] for s in ('purged', 'expired', 'corrupt', 'unavailable'))
assert p04['allKitSuitesExitZero'] and p04['kitQueryControls']['passed'] and all(p04['kitQueryControls']['new'].values()) and p04['frozen36DriftAfter'] == 0
assert all(v['equal'] for v in p04['kitS2'].values())
ks1 = p04['kitS1']
assert ks1['package-absent-coordinate']['wrapperWithoutRun'] == 'QUERY.ENDPOINT_AMBIGUOUS' and ks1['package-absent-coordinate']['rawRequestSchemaAdmits'] and not ks1['package-absent-coordinate']['rawResponseEndpointAdmits']
assert ks1['package-empty-coordinate']['wrapperWithoutRun'] == ks1['package-empty-coordinate']['helper'] == 'QUERY.PARAMS_MALFORMED'
starts = {}
for d in sorted(os.listdir(RC)):
    cj = os.path.join(RC, d, 'command.json')
    if os.path.isfile(cj):
        starts[d] = json.load(open(cj))['startedUtc']
exp = os.path.join(BASE, 'expected-before-probes.json')
exp_written = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(os.path.getmtime(exp)))
first_probe = min(starts.values())
assert exp_written <= first_probe

rows36 = []
touched = set(p04['changedSourceFiles'])
for mp in ('fDispositions', 'evaluationResidualDispositions', 'arDispositions', 'fwDispositions', 'inheritedResidualDispositions', 'scopedReviewOwnerDispositions'):
    for rid, row in V36J[mp].items():
        own = row.get('currentOwnerFiles') or row.get('currentOwnerSelectors') or []
        paths = {o.split('#')[0].split(' ')[0] for o in own if isinstance(o, str)}
        hit = sorted(paths & touched)
        if hit:
            rows36.append({'map': mp, 'row': rid, 'ownersTouched': hit, 'statusChangeOn36': row.get('statusChangeOn36')})

A = {}
A['assessment'] = 'Bounded NONBLIND source gap assessment of consumer23 interim findings V23-S1, V23-S2, V23-S3 on frozen candidate36'
A['standing'] = ('Actual Claude, continuing completed source-review origin ce3dec3b-0620-44ec-86e6-129b0e25cb1b. NOT blind consumer B, NOT the final '
                 'application review, NOT acceptance of any successor. The candidate36 technical ACCEPT (review.json fa1b7f48...) is historical evidence '
                 'of that review, not a resolution of these findings. Grants no application outcome, readiness, activation or implementation authority.')
A['inputs'] = {
    'subjectManifest': {'path': os.path.join(REV, 'candidate-subject.v36.json'), 'sha256': 'a729406b9de0d865294884f7575ea943c0935437091389e2acebe8e5aedb4235',
                        'snapshot': S36},
    'consumerReport': {'path': os.path.join(BASE, 'consumer23-interim-review.json'), 'sha256': sha(os.path.join(BASE, 'consumer23-interim-review.json')),
                       'standing': 'exact captured interim report of the still-completing original independent consumer; provisional, not a completed consumer verdict',
                       'capturedVerdictField': CONS['verdict'], 'scope': ['V23-S1', 'V23-S2', 'V23-S3']},
    'myPriorReview': {'path': os.path.join(V36, 'review.json'), 'sha256': sha(os.path.join(V36, 'review.json')), 'verdict': V36J['verdict']}}
A['boundaries'] = {'noContactWithRunningConsumer': True, 'noPrivateSessionLogs': True, 'consumerHelpersNotRepaired': True,
                   'consumerExportedRunsNotClaimedRootAdmitted': True, 'writesConfinedToThisRuntime': True, 'noCommitPushAgentsOrProductWork': True,
                   'modelCodeStanding': 'model behaviour was measured as evidence; it was never used as a normative input to fill a consumer-visible recipe'}
A['expectedLawBeforeProbes'] = {'file': 'expected-before-probes.json', 'sha256': sha(exp), 'writtenUtc': exp_written, 'firstProbeStartedUtc': first_probe,
                                'writtenBeforeAnyProbe': exp_written <= first_probe, 'allExpectationsHeld': True}

sh = p01['shapes']
A['findings'] = {
 'V23-S1': {
  'consumerClaim': issues['V23-S1'],
  'classification': 'REAL SOURCE INCONSISTENCY (confirmed). Two published owners assign different DomainDetails to one request; not consumer error.',
  'severity': 'SHOULD - consumer-visible conformance divergence (same class request-rejected, same exit 2, same errorCode REQUEST.PRECONDITION_FAILED; different DomainDetail and remedy); no soundness effect',
  'exactSelectors': ['docs/coop/design-corrections/workflows/query-projection-contract.v3.md section 2 "Fault precedence" steps 1-2 (lines 43-47)',
                     'docs/coop/design-corrections/workflows/query-projection-contract.v3.md section 7 rows "malformed graph params ..." and "malformed-complete but ambiguous endpoint" (lines 165, 167)',
                     'docs/coop/design-corrections/workflows/query-projection-contract.v3.md section 8 steps 1 and 5 (lines 181, 185)',
                     'docs/coop/design-corrections/workflows/schemas/evaluator3/graph-query.schema.json#/$defs/GraphEndpoint allOf[0] (if kind=package then required packageManifestPath); referenced by GraphNeighborsParams.endpoint, GraphPathParams.start/target, GraphReachParams.start AND by response rows',
                     'docs/coop/design-corrections/public-detail-registry.v1.json QUERY.ENDPOINT_AMBIGUOUS and QUERY.PARAMS_MALFORMED (both select the contract and the schema)',
                     'docs/coop/design-corrections/workflows/query_projection_model.v3.py _validate_request (schema first) -> effective_params -> parse_endpoint_syntax'],
  'observedBehaviour': {
   'packageWithoutCoordinate': {'rawGraphEndpointSchema': sh['package-without-packageManifestPath']['rawSchemaGraphEndpoint'],
                                'rawRequestSchema': sh['package-without-packageManifestPath']['rawSchemaGraphQueryRequestV1'],
                                'publicWrapper': sh['package-without-packageManifestPath']['publicWrapper'],
                                'parseHelper': sh['package-without-packageManifestPath']['parseEndpointSyntaxHelper'],
                                'section2Predicts': 'QUERY.ENDPOINT_AMBIGUOUS'},
   'everyOtherStep1ShapeAgreesOnSchemaWrapperAndHelper': o1['step1ShapesAgreeEverywhere'],
   'multiVertexAmbiguityClauseUnreachableInReference': {'everPopulated': p01['multiVertexClauseEverPopulated'], 'cases': p01['inventoryVerticesAmbiguity']},
   'receipt': 'receipts/p01-s1-endpoint.json'},
  'assessmentOfConsumerReading': ('The consumer correctly found the conflict. Its reading I-Q4 (section 2 decides; re-admit with a placeholder coordinate) is '
                                  'not published law and would itself be an invented recipe; its smallestFix options are both lawful. I recommend the one '
                                  'that preserves the explicitly published section 2 distinction.'),
  'whyPreserveTheSection2Distinction': ('Section 2 is the specific endpoint-admission law and deliberately separates malformed syntax (step 1) from an '
                                        'incomplete package identity (step 2) with its own registered detail and remedy; the model implements it; and '
                                        'QUERY.ENDPOINT_AMBIGUOUS has no other reachable route in the reference, because inventory_vertices keys vertices '
                                        'by the full tuple and cannot mark one ambiguous. The schema conditional is a generic shape rule written for the '
                                        'endpoint tuple in both directions; response rows must keep it. Relaxing it on the request side only is the smaller '
                                        'coherent change than deleting a documented, registered distinction.'),
  'correction': {
   'schema': 'graph-query.schema.json: add $defs/GraphRequestEndpoint (GraphEndpoint shape, kind=package may omit packageManifestPath; packageManifestPath on a non-package still refused); GraphNeighborsParams.endpoint, GraphPathParams.start/target and GraphReachParams.start reference it; response rows keep GraphEndpoint',
   'contract': ['s2 step 1: a present packageManifestPath that is not a LogicalPath is malformed', 's2 step 2: "whose packageManifestPath is absent"',
                's2: one paragraph naming the request/response schema split', 's7 row: "package endpoint without its coordinate, or well-formed but ambiguous endpoint"',
                's8 step 1: an absent package coordinate passes closed admission and is refused QUERY.ENDPOINT_AMBIGUOUS by endpoint syntax before any vertex lookup'],
   'model': 'parse_endpoint_syntax: absent coordinate -> ENDPOINT_AMBIGUOUS; present but empty/non-string -> PARAMS_MALFORMED (helper agrees with contract for every shape)',
   'regressionControls': ['closed-request-admission-leaves-absent-package-coordinate-to-section-2', 'response-graph-endpoint-still-requires-package-coordinate',
                          'package-endpoint-without-coordinate-is-endpoint-ambiguous (public wrapper, real admitted Run, envelope validated)',
                          'empty-package-coordinate-is-params-malformed', 'package-coordinate-on-file-endpoint-is-params-malformed'],
   'alternativeIfOwnersPreferIt': ('Keep the schema and state in s2 that an absent coordinate is a closed-schema refusal (PARAMS_MALFORMED); then '
                                   'QUERY.ENDPOINT_AMBIGUOUS has no reachable graph route and s2 step 2 and the s7 row must be rewritten accordingly.'),
   'rehearsed': {'kit': p04['kitS1'], 'controls': p04['kitQueryControls']}},
  'crossOwners': ['workflows (query contract, graph-query schema, query model, query checker)', 'public detail registry: no change',
                  'D9: no change', 'five pin ledgers: re-seal only', 'no 107-row owner is a query file']},
 'V23-S2': {
  'consumerClaim': issues['V23-S2'],
  'classification': 'REAL SOURCE INCONSISTENCY (confirmed), inside the native owner against the D9 owner it states it inherits unchanged; not a lawful per-requirement/whole-Run scope distinction.',
  'severity': 'SHOULD - consumer-visible divergence of whole-Run termination reasonCodes for three deficiencies (same class indeterminate and exit 3); no D9 class, exit or vocabulary change',
  'exactSelectors': ['docs/v2/contracts/product-v1/native-evidence.md section 10 table rows language-tier-unsupported, confidence-floor-unmet, required-relation-missing, column "Existing code" (lines 2907, 2909, 2910)',
                     'docs/v2/contracts/product-v1/native-evidence.md section 10 "inherits d9-exit-contract.v1.14.json unchanged" (line 3051) and section 4.6 "public D9 termination ... still the section 10 class/code columns" (lines 2148-2153)',
                     'docs/coop/design-corrections/native/native-evidence.schemas.v2.json publicD9Termination',
                     'docs/coop/artifacts/d9-exit-contract.v1.14.json#/codeMaps/deficiencyToReasonCode, #/causeModel/codeDerivation, goldens analysis-required-coverage-missing, analysis-language-tier-unsupported, analysis-confidence-floor-unmet, repair-verification-indeterminate',
                     'docs/coop/design-corrections/workflows/schemas/evaluator3/common.schema.json#/$defs/D9Deficiency description',
                     'docs/v2/contracts/product-v1/workflows-and-surfaces.md lines 783-796',
                     'docs/coop/design-corrections/native/native_evidence_model.v2.py run_termination (line 3668) and D9_MAP'],
  'observedBehaviour': {'perDeficiency': p02['perDeficiency'], 'section10DisagreesWithD9': p02['section10DisagreesWithD9'], 'modelDisagreesWithD9': p02['modelDisagreesWithD9'],
                        'modelDisagreesWithItsOwnSection10': p02['modelDisagreesWithSection10'], 'ownerSentences': p02['ownerSentences'], 'receipt': 'receipts/p02-s2-d9.json'},
  'whyNoPerRequirementDistinction': p02['publishedPerRequirementD9CodeReason'],
  'assessmentOfConsumerReading': ('The consumer correctly found the conflict and applied the right reading (the D9 exit contract governs whole-Run terminations). '
                                  'Its first smallestFix option ("the s10 column is the per-requirement route") would invent a distinction the sources '
                                  'refute: per-requirement outcomes carry DeficiencyV2 and no D9 code, and s4.6 names s10 as the Run/step termination. The '
                                  'second option (align the three codes) is the correct remedy.'),
  'correction': {
   'contract': ['native-evidence.md s10: Existing code for language-tier-unsupported -> COVERAGE.LANGUAGE_TIER_UNSUPPORTED, confidence-floor-unmet -> COVERAGE.CONFIDENCE_FLOOR_UNMET, required-relation-missing -> COVERAGE.REQUIRED_RELATION_MISSING',
                'native-evidence.md s10: one paragraph stating the column IS d9 codeMaps.deficiencyToReasonCode for D9Deficiency members and verdict-indeterminate for the four native-only outcomes; one mapping, no per-requirement D9 code'],
   'schemaText': 'native-evidence.schemas.v2.json publicD9Termination names the D9 map and all five COVERAGE codes',
   'model': 'native_evidence_model.v2.py: D9_DEFICIENCY_REASON_CODE mirrors the D9 map; run_termination uses it (also corrects budget-exhausted, which the model mapped to VERDICT.INDETERMINATE against its own s10 row)',
   'regressionControls': ['native-cases.v2.json run-termination-derives-the-d9-exit-contract-reason-code-for-each-deficiency (five D9 members + one native-only)',
                          'existing native run_termination cases and check-identity an-unsupported-source-variant-scope-projects-an-indeterminate-run unchanged'],
   'notChanged': 'no D9 class, exit, reason code, D9Deficiency member, public DomainDetailCode or D9_MAP key (check-integration requires D9_MAP keys to be registered details, which these deficiencies are not)',
   'rehearsed': {'kitS2': p04['kitS2'], 'nativeCase': p04.get('kitNativeNewCase')}},
  'crossOwners': ['native (contract s10, schema text, model, cases)', 'D9 exit-contract artifact: unchanged; it is the governing map',
                  'workflows-and-surfaces: unchanged (it already routes whole-Run terminations to native s10 and D9Deficiency)',
                  'AR-16 (exact outcomes) and the other native-evidence.md-owned rows: their owner changes, so a successor review must re-read them',
                  'planning layer4: native-evidence.md is %s one of the 29 normative inputs' % ('' if 'docs/v2/contracts/product-v1/native-evidence.md' in p04['layer4InputsTouched'] else 'NOT')]},
 'V23-S3': {
  'consumerClaim': issues['V23-S3'],
  'classification': 'REAL BUT NARROW NORMATIVE GAP (confirmed missing recipe), not an inconsistency and not consumer error.',
  'severity': 'SHOULD (small) - a consumer-visible detail for one availability state is decided only by model code',
  'exactSelectors': ['docs/coop/design-corrections/workflows/query-projection-contract.v3.md section 7 availability paragraph (line 160) and table (lines 173-174: only missing and corrupt retained bytes)',
                     'docs/v2/contracts/product-v1/identity-and-evidence.md section 5 (availability states; graph selector delegated to query s7, lines 1610-1614, 1642-1656)',
                     'docs/coop/design-corrections/foundation/identity-schemas.v3.json availability.state enum',
                     'docs/coop/design-corrections/public-detail-registry.v1.json evidence.* records (no meaning text; no evidence.unavailable)',
                     'docs/coop/design-corrections/workflows/query_projection_model.v3.py AVAIL_REFUSE; foundation/identity-model.v3.py EvidenceUnavailable'],
  'observedBehaviour': {'publicWrapperOverRealRun': p03['publicWrapperByAvailability'], 'observedMapping': m3,
                        'identityOwnerUnavailabilityTermination': p03['identityModelUnavailabilityTermination'],
                        'existingControlsByState': p03['existingControlsByState'], 'receipt': 'receipts/p03-s3-availability.json'},
  'assessmentOfConsumerReading': 'Correct and appropriately conservative: it invented no detail and treated unavailable as unexercised.',
  'whyEvidenceMissing': ('The only existing members are purged, expired, missing, corrupt, pinned, regeneration-mismatch. The identity owner\'s own '
                         'termination for required retained evidence that cannot be supplied is evidence.missing (remedy: "...or report their '
                         'unavailability"), and the reference already maps unavailable to it. Publishing that choice fills the recipe without a new code.'),
  'correction': {
   'contract': ['query s7 paragraph: purged/expired/corrupt/unavailable -> HOST.IO_FAILURE (host-io) with evidence.purged/expired/corrupt/missing respectively; no evidence.unavailable member; retained and partial do not refuse by themselves',
                'query s7 table: one row per refusing availability state'],
   'model': 'none (AVAIL_REFUSE already implements the published mapping)',
   'regressionControls': ['host-availability-unavailable-refuses-evidence-missing', 'host-availability-corrupt-refuses-evidence-corrupt', 'host-availability-partial-does-not-refuse-by-itself'],
   'rehearsed': p04['kitQueryControls']},
  'crossOwners': ['workflows query contract and checker only', 'identity s5 unchanged (already delegates the graph selector)', 'public detail registry unchanged']}}

A['additionalObservations'] = [
    {'id': 'OBS-1', 'finding': 'The second section 2 step-2 clause ("a well-formed tuple that matches more than one admitted vertex") is unreachable in the reference: inventory_vertices keys by the full tuple and compares a canonical endpoint derived from the same fields.',
     'standing': 'model evidence (p01); advisory only; not corrected here'},
    {'id': 'OBS-2', 'finding': 'An unregistered availability value (e.g. "not-a-state") on the trusted host observation is ignored and the query succeeds; identity availability is a closed enum.',
     'standing': 'advisory; trusted host input shape, outside V23-S3; a successor may refuse it as a reference-call precondition (p03)'},
    {'id': 'OBS-3', 'finding': 'native run_termination emits one reason code (native precedence worst), while the D9 cause model derives an ordered reasonCodes list including secondaryDeficiencies (golden analysis-multiple-deficiencies).',
     'standing': 'pre-existing helper limit, recorded not corrected (p02)'},
    {'id': 'OBS-4', 'finding': 'The internal traverse_projected_graph algorithm helper does not apply endpoint syntax admission at all.',
     'standing': 'documented internal helper ("Not close_run and not a public query"); no public consequence (p01)'}]
A['successor'] = {
    'recommendation': 'ONE coherent successor carrying the three corrections together',
    'patch': p04['patch'], 'changedSourceFiles': p04['changedSourceFiles'], 'edits': p04['edits'],
    'pinLedgersResealedInRehearsal': p04['repinned'], 'layer4InputsTouched': p04['layer4InputsTouched'],
    'planningConsequence': ('layer4 must be re-derived for the touched normative input(s); populations are unaffected by these edits'
                            if p04['layer4InputsTouched'] else 'no layer4 input touched; layer4 may be retained if its 29 inputs stay byte-identical'),
    'rehearsalSuites': p04['kitSuites'], 'rehearsalLauncher': p04.get('kitLauncher'), 'kitFilesRewrittenByCheckers': p04['kitFilesRewrittenByCheckers'],
    'standing': 'rehearsed only in a disposable hash-verified copy; frozen candidate36 drift 0; this is not a successor and not acceptance',
    'receipt': 'receipts/p04-successor-rehearsal.json'}
A['doesSource36AcceptanceReopen'] = {
    'answer': 'YES',
    'explanation': ('My source36 technical ACCEPT stated no new MUST or SHOULD. These three confirmed consumer-visible defects in published candidate36 '
                    'law are SHOULD-level issues that review did not find, so that ACCEPT cannot stand as final acceptance of the affected surfaces. '
                    'The record stays historical and unedited. No MUST is raised: class, exit, errorCode, soundness and D9 vocabulary are unaffected. '
                    'A successor carrying the patch, re-sealed pins and a layer4 re-derivation if required, and a fresh review of its exact bytes, are '
                    'needed before design acceptance can be claimed again.'),
    'myPriorReviewMadeNoContraryClaim': 'review.json fa1b7f48... contains no statement about package-endpoint admission, native s10 D9 codes or query availability details',
    'rowsOwningTouchedFiles': rows36}
A['carriedObligations'] = {
    'TCB-SCOPE-01': 'one shared assumption over 13 dependent rows, not closed, no qualification', 'condition2Obligations': 28,
    'productGates': {'count': 32, 'performed': 0, 'condition5': 'NOT MET'}, 'plannedRecoveryCases': {'count': 54, 'executed': 0},
    'residualProposals': '30 PENDING', 'd9': 'DR-007 / DR-011-R08 implementation obligation persists',
    'authority': 'no final application, architecture-readiness, activation or implementation authority'}
A['limits'] = [
    'Source/reference assessment only; no product implementation, qualification or readiness.',
    'S1 and S3 public-wrapper behaviour was measured on the reference model with a synthetic admitted Run (the query checker\'s own fixture); S2 was measured on the native reference model helpers and the D9 artifact; no retained product Run, blind reconstruction or consumer helper was used.',
    'The consumer report is an interim capture; its other findings, advisories and verdict are outside this scope and were not assessed.',
    'The successor was rehearsed in a disposable copy with pins re-sealed there only; root owns real re-sealing, layer4 re-derivation if required, freezing and review.',
    'Choosing to preserve the section 2 distinction (S1) is a normative judgement between two lawful corrections; the alternative is recorded.']
A['probeErrorsAndSlips'] = [
    'In a progress message I first described the captured report verdict as ACCEPT before reading the field; it is CHANGES_REQUIRED. No artifact relied on the slip.']
A['receipts'] = {f: sha(os.path.join(RC, f)) for f in sorted(os.listdir(RC)) if f.endswith('.json') and not f.startswith('i01')}
A['commandReceipts'] = {d: {'startedUtc': v, 'exit': json.load(open(os.path.join(RC, d, 'command.json')))['exit']} for d, v in starts.items()}
A['patchSha256'] = p04['patch']['sha256']
out = os.path.join(BASE, 'assessment.json')
json.dump(A, open(out, 'w'), indent=1, default=str)
print('findings', {k: v['classification'][:40] for k, v in A['findings'].items()}, '| reopen', A['doesSource36AcceptanceReopen']['answer'])
print('layer4 touched', p04['layer4InputsTouched'], '| rows owning touched files', len(rows36))
print('assessment.json', sha(out))
