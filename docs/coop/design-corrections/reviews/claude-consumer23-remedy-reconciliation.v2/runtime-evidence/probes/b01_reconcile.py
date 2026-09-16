"""B01 — reconciliation builder. Remedy assistance only: NOT independent acceptance, NOT successor acceptance.
Gates on the captured author inputs and the p01 targeted probe; verifies that every recommended edit anchors exactly once in
the captured author after-image; applies the edits to disposable copies (model compiled, nothing executed); writes
reconciliation.json and a reviewable diff against the author images. No frozen, live or author byte is written."""
import difflib, hashlib, json, os, shutil

BASE = '/tmp/opensip-design-corrections/claude-consumer23-remedy-reconciliation.v2'
IMG = os.path.join(BASE, 'observed-author-source')
RC = os.path.join(BASE, 'receipts')
WORK = os.path.join(BASE, 'disposable/recommended')
PREV = '/tmp/opensip-design-corrections/claude-consumer23-gap-assessment.v2/receipts'
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
man = json.load(open(os.path.join(BASE, 'after-manifest.json')))
p01 = json.load(open(os.path.join(RC, 'p01-targeted.json')))
AR = json.load(open(os.path.join(BASE, 'author-report.json')))
QC = 'docs/coop/design-corrections/workflows/query-projection-contract.v3.md'
NAT = 'docs/v2/contracts/product-v1/native-evidence.md'
NM = 'docs/coop/design-corrections/native/native_evidence_model.v2.py'
NS = 'docs/coop/design-corrections/native/native-evidence.schemas.v2.json'

# ------------------------------------------------------------------ gates
for f in man['files']:
    assert sha(os.path.join(IMG, f['path'])) == f['sha256'], f['path']
assert [f for f in man['files'] if f['path'] == NS][0]['equalsFrozen36'] is True
s1 = p01['S1']
for k in ('package-absent-coordinate', 'package-empty-coordinate'):
    assert all(s1[k][r] == 'REQUEST.PRECONDITION_FAILED / QUERY.PARAMS_MALFORMED' for r in ('wrapperNoRun', 'wrapperNoRunPurgedObservation', 'wrapperDummyRunPurgedObservation', 'helper'))
    assert s1[k]['rawRequestSchemaAdmits'] is False
assert s1['package-with-coordinate']['wrapperDummyRunPurgedObservation'] == 'HOST.IO_FAILURE / evidence.purged' and p01['graphQuerySchemaUnchanged']
assert p01['S1ambiguityHelperOnly']['admit_vertices_with_marked_key'] == 'REQUEST.PRECONDITION_FAILED / QUERY.ENDPOINT_AMBIGUOUS'
assert p01['nativeRouteDrift'] == [] and p01['nativeRouteRefusesNonMember'] and len(p01['nativeRouteTotal']) == 9
ob = p01['observations']
assert ob['requirementRelativeDeficiencyReachesHelperOnlyIfAnEntryDeclaresIt'] and ob['stageImpliedPrimaryCanDifferFromTypedDetail'] and ob['faultedStageKeepsOwnTermination']
assert ob['helperInputsAreOnlyStageAndEntries'] is False and p01['helperSignature'] == "(stage: 'dict', coverage_entries: 'list[dict]') -> 'dict'"
assert p01['imagesUnchangedAfter'] and p01['frozen36OverlaySourcesUnchanged']

# ------------------------------------------------------------------ recommended edits (exact anchors in the author images)
EDITS = [
 {'issue': 1, 'file': QC, 'kind': 'replace',
  'anchor': ('The reference vertex domain is keyed by the complete tuple, so one retained Run cannot yield two distinct vertices for one tuple '
             'and this step is not reachable through `execute_graph_query`; the detail remains the lawful answer for a vertex domain that could.'),
  'text': ('Because this section defines an endpoint, and so a vertex, by its complete tuple, a complete tuple names at most one vertex of an '
           'admitted domain: this step is not reachable through `execute_graph_query` and is kept only as a closed refusal. An implementation '
           'that nevertheless observes two distinct vertex records for one complete tuple must refuse with `QUERY.ENDPOINT_AMBIGUOUS` and must '
           'never choose one.')},
 {'issue': 2, 'file': NAT, 'kind': 'insert-after',
  'anchor': 'agrees with it. No D9 class, code, exit or vocabulary changes.\n',
  'text': ('\n**Superseded schema annotation (registered bytes kept).** The annotation\n'
           '`native-evidence.schemas.v2.json#/x-opensip-deficiency-cause-registry/perRequirementConsumerBoundary/threeDistinctThingsNotToConflate/publicD9Termination`\n'
           'still reads "the class/exit/errorCode of the Run or step that carries the requirement - unchanged, still the\n'
           'section 10 table columns (indeterminate (3) with VERDICT.INDETERMINATE, COVERAGE.PROVIDER_UNAVAILABLE or\n'
           'COVERAGE.BUDGET_EXHAUSTED)". Its reference to the section 10 class and code columns stands. Its parenthetical\n'
           'three-code list and its word `errorCode` are superseded by this section: an `indeterminate` termination carries\n'
           '`reasonCodes`, and the codes are the complete route in the table above, including\n'
           '`COVERAGE.LANGUAGE_TIER_UNSUPPORTED`, `COVERAGE.CONFIDENCE_FLOOR_UNMET` and `COVERAGE.REQUIRED_RELATION_MISSING`.\n'
           'Where the annotation and this section differ, this section governs. The annotation\'s bytes are deliberately\n'
           'unchanged: that document is a registered payload schema whose raw SHA-256 is the `payloadSchemaDigest` from\n'
           'which every `coverage2` minted against it is identified (§4.1a), so editing the annotation is a schema-document\n'
           'successor with its own re-registration, not a text correction.\n')},
 {'issue': 3, 'file': NAT, 'kind': 'replace',
  'anchor': ('The **primary** deficiency is chosen by the precedence above over every deficiency\n'
             'the Run\'s admitted Coverage entries declare and the one a clean typed stage\n'
             'terminal implies (`BudgetExhausted` → `budget-exhausted`, `Unavailable` →\n'
             '`provider-unavailable`). A faulted or cancelled stage mints nothing and keeps its\n'
             'own operational-failed or interrupted termination, so no deficiency accompanies\n'
             'it. The typed detail still names the most specific deficiency an entry actually\n'
             'carries and every `nativeCause` those entries carry. The reference\n'
             '`run_termination` returns the one primary code; the ordered `reasonCodes` list with\n'
             '`secondaryDeficiencies` (`causeModel.codeDerivation` of the D9 contract) is\n'
             'composed by the host termination and is **not** produced by that helper.'),
  'text': ('**Native stage selection, and where it stops.** Within one native stage, the precedence above selects that\n'
           'stage\'s **native primary deficiency** over the deficiencies its admitted Coverage entries declare and the one a\n'
           'clean typed stage terminal implies (`BudgetExhausted` → `budget-exhausted`, `Unavailable` →\n'
           '`provider-unavailable`). A faulted or cancelled stage mints nothing and keeps its own operational-failed or\n'
           'interrupted termination, so no deficiency accompanies it. The typed detail names the most specific deficiency an\n'
           'entry actually carries and every `nativeCause` those entries carry; it can differ from a stage-implied primary.\n'
           'The reference `run_termination` implements exactly this stage selection and returns its one code.\n\n'
           'That selection is the native contribution, not the Run\'s termination. Only the host finalizer constructs the\n'
           'Run\'s termination (`d9-exit-contract.v1.14.json` `invariant-one-mapper`). It reduces every concurrent condition\n'
           'the Run exhibits under `causeModel`: a fault cause, else a rejection cause, else deficiencies, whose primary and\n'
           'ordered `secondaryDeficiencies` come from that reduction (`concurrentConditionReducer`, `codeDerivation`). Besides\n'
           'native stage selections, those conditions include requirement sufficiency over `RequirementV2` (§4.6;\n'
           '`required-relation-missing` and `confidence-floor-unmet` have no entry carrier and are requirement-relative),\n'
           'required execution and imported-evidence obligations, and verdict composition\n'
           '(`evaluator-composition-contract.v3.md` §5). Whatever `DeficiencyV2` member that reduction names takes its class\n'
           'and code from the total route above. This section does not define how requirement, proof-cause, import or\n'
           'verdict outcomes are ordered in that reduction.')},
 {'issue': 3, 'file': NAT, 'kind': 'replace',
  'anchor': ('The termination code is the whole-Run route of the Run\'s primary deficiency (the\n'
             'class and code columns above): `VERDICT.INDETERMINATE` for the incomplete-input\n'
             'deficiencies named here, and `COVERAGE.BUDGET_EXHAUSTED` /\n'
             '`COVERAGE.PROVIDER_UNAVAILABLE` for those two terminals unless an entry declares a\n'
             'more specific deficiency (`run-termination-code-is-the-primary-deficiency-route`).'),
  'text': ('The stage\'s native termination code is the route above applied to its native primary\n'
           'deficiency: `VERDICT.INDETERMINATE` for the incomplete-input deficiencies named here, and\n'
           '`COVERAGE.BUDGET_EXHAUSTED` / `COVERAGE.PROVIDER_UNAVAILABLE` for those two terminals unless an entry\n'
           'declares a more specific deficiency (`run-termination-code-is-the-primary-deficiency-route`). The Run\'s\n'
           'termination is the host\'s D9 reduction over all its conditions (section 10, native stage selection).')},
 {'issue': 3, 'file': NM, 'kind': 'replace',
  'anchor': ('    A faulted or cancelled stage keeps its own D9 termination and mints nothing. Otherwise the Run\'s PRIMARY\n'
             '    deficiency is the most specific, by section 10 precedence, among the entries\' declared deficiencies and the one a\n'
             '    clean typed stage terminal implies (BudgetExhausted -> budget-exhausted, Unavailable -> provider-unavailable),\n'
             '    and its termination is `native_deficiency_d9` of it: indeterminate 3 under an existing D9 code, never a fault and\n'
             '    never exit 0.'),
  'text': ('    A faulted or cancelled stage keeps its own D9 termination and mints nothing. Otherwise the STAGE\'s native primary\n'
           '    deficiency is the most specific, by section 10 precedence, among the entries\' declared deficiencies and the one a\n'
           '    clean typed stage terminal implies (BudgetExhausted -> budget-exhausted, Unavailable -> provider-unavailable),\n'
           '    and the stage\'s native termination is `native_deficiency_d9` of it: indeterminate 3 under an existing D9 code,\n'
           '    never a fault and never exit 0. NATIVE CONTRIBUTION ONLY: the Run\'s HostTermination is the host finalizer\'s D9\n'
           '    reduction over every concurrent condition (native stages, requirement sufficiency, execution and import\n'
           '    obligations, verdict), which this helper does not see.')},
]
if os.path.isdir(WORK):
    shutil.rmtree(WORK)
files = sorted({e['file'] for e in EDITS})
for rel in files:
    os.makedirs(os.path.dirname(os.path.join(WORK, rel)), exist_ok=True)
    shutil.copyfile(os.path.join(IMG, rel), os.path.join(WORK, rel))
for e in EDITS:
    p = os.path.join(WORK, e['file'])
    t = open(p, encoding='utf-8').read()
    n = t.count(e['anchor'])
    e['anchorOccurrencesInAuthorImage'] = open(os.path.join(IMG, e['file']), encoding='utf-8').read().count(e['anchor'])
    assert n == 1 and e['anchorOccurrencesInAuthorImage'] == 1, (e['issue'], e['file'], n)
    t = t.replace(e['anchor'], e['text'] if e['kind'] == 'replace' else e['anchor'] + e['text'])
    open(p, 'w', encoding='utf-8').write(t)
compile(open(os.path.join(WORK, NM), encoding='utf-8').read(), NM, 'exec')
diff = []
for rel in files:
    a = open(os.path.join(IMG, rel), encoding='utf-8').read().splitlines(keepends=True)
    b = open(os.path.join(WORK, rel), encoding='utf-8').read().splitlines(keepends=True)
    diff.extend(difflib.unified_diff(a, b, 'author/' + rel, 'recommended/' + rel, n=2))
open(os.path.join(BASE, 'recommended-edits.diff'), 'w', encoding='utf-8').write(''.join(diff))

J = {
 'reconciliation': 'Remedy reconciliation for consumer23 V23-S1/S2 author remedy: S1 schema-first coherence, native schema annotation supersession, native section 10 scope boundary',
 'standing': ('Remedy assistance by origin ce3dec3b-0620-44ec-86e6-129b0e25cb1b. NOT independent acceptance, NOT successor acceptance, NOT blind '
              'consumer standing. Author assistance before a NEW fresh source acceptance and a NEW fresh blind consumer, each in a separate new '
              'origin. Grants no application outcome, readiness, activation or implementation authority.'),
 'inputs': {'authorReportMd': sha(os.path.join(BASE, 'author-report.md')), 'authorReportJson': sha(os.path.join(BASE, 'author-report.json')),
            'afterManifest': sha(os.path.join(BASE, 'after-manifest.json')), 'authorOrigin': AR['authorOrigin'],
            'capturedImagesVerifiedAgainstAfterManifest': True, 'nativeSchemaImageEqualsFrozen36': True,
            'frozen36': '/tmp/opensip-design-corrections/candidate-subject.v36 (owning contracts, read-only)',
            'notRead': 'live source assembly, original blind artifacts, root consumer diagnostics'},
 'priorOwnRecords': {'gapAssessment': '/tmp/opensip-design-corrections/claude-consumer23-gap-assessment.v1/assessment.json (historical, unedited)',
                     'completionReceipts': PREV},
 'issues': {
  '1-S1-schema-first': {
   'verdict': 'COHERENT, with one precision edit recommended',
   'assessment': ('The author adopted the lawful alternative recorded in my gap assessment: closed-schema admission decides, so a package endpoint '
                  'without a non-empty packageManifestPath is QUERY.PARAMS_MALFORMED; graph-query.schema.json is unchanged; section 2, the section 7 '
                  'rows and the model helper now agree. Measured on the captured images over frozen36: absent and empty coordinates are refused '
                  'PARAMS_MALFORMED by the public wrapper with no Run, with a purged availability observation, and with a dummy Run, before Run '
                  'presence, view and availability, while a well-formed coordinate reaches the Run check and then the purged refusal; the helper '
                  'agrees. QUERY.ENDPOINT_AMBIGUOUS is produced only by admit_vertices when handed a pre-marked key. My earlier preference to preserve '
                  'the old section 2 distinction with a request-side schema is withdrawn for this successor: the author\'s choice needs no schema or '
                  'planning-input change for S1, and it discharges the conditions I attached to the alternative (step 2 and the section 7 row rewritten).'),
   'precision': ('Section 2 defines an endpoint, and therefore a vertex, by its complete tuple (line 36), so a complete tuple cannot name two vertices '
                 'under the contract itself, not merely under the reference implementation. The author\'s closing clause "the detail remains the lawful '
                 'answer for a vertex domain that could" implies a lawful domain the contract does not admit.'),
   'ownerCitations': ['query-projection-contract.v3.md section 2 (tuple identity, line 36; fault precedence), section 7 rows, section 8 step 1',
                      'graph-query.schema.json#/$defs/GraphEndpoint allOf[0] (unchanged)', 'query_projection_model.v3.py _validate_request, parse_endpoint_syntax, inventory_vertices, admit_vertices'],
   'measured': {'S1': s1, 'ambiguityHelperOnly': p01['S1ambiguityHelperOnly'], 'graphQuerySchemaUnchanged': p01['graphQuerySchemaUnchanged']},
   'modelIssue': 'none required',
   'recommendedEdits': [e for e in EDITS if e['issue'] == 1]},
  '2-native-schema-annotation': {
   'verdict': 'KEEP EXACT REGISTERED BYTES; ADD AN EXPLICIT NORMATIVE SUPERSESSION NOTE IN SECTION 10',
   'assessment': ('The author correctly reverted the schema document to frozen36 bytes but left the stale annotation only in the author report. The '
                  'annotation still enumerates three codes and says errorCode, which after the corrected table is an incomplete and misleading public '
                  'statement; a consumer reading the schema needs the owning contract to say that section 10 governs. The registered bytes must not '
                  'change here: coverage2 is minted from payloadSchemaDigest, the raw SHA-256 of the exact registered schema document (native-evidence.md '
                  'section 4.1a lines 1759-1760), and changing those bytes made check-identity v20-native-view-fixture-declares-current-registered-schemas '
                  'fail and every positive retained package13 Run refuse PAYLOAD_SCHEMA_NOT_THE_REGISTERED_DOCUMENT in my earlier rehearsal (variant A).'),
   'ownerCitations': ['native-evidence.schemas.v2.json#/x-opensip-deficiency-cause-registry/perRequirementConsumerBoundary/threeDistinctThingsNotToConflate/publicD9Termination',
                      'native-evidence.md section 4.1a (coverage2 minted from payloadSchemaDigest), section 4.6, section 10',
                      'foundation/identity-schemas.v3.json payloadSchemaDigest ("raw SHA-256 of the EXACT FULL schema DOCUMENT file bytes named by the row")',
                      'author-report.json#/decisions/V23-S2/schemaAnnotationNotChanged'],
   'priorEvidence': {'variantAReplay': PREV + '/p05-successor-rehearsal2.json', 'retainedRunsCommitDigest': PREV + '/s04-retained-schema-digests.json',
                     'fixtureGuardFailure': PREV + '/s01-p04-status.json'},
   'noRegistrationOrRemintHere': True,
   'recommendedEdits': [e for e in EDITS if e['issue'] == 2]},
  '3-section10-scope': {
   'verdict': 'REAL SCOPE CONFLATION IN THE AUTHOR WORDING; minimal boundary text and one model docstring recommended; no behaviour change',
   'assessment': ('The author paragraph says the PRIMARY deficiency is chosen over the Run\'s admitted Coverage entry deficiencies and the clean stage '
                  'terminal. That is exactly the native helper\'s input (run_termination(stage, coverage_entries)), but it is worded as the Run\'s primary '
                  'deficiency. The owners place Run termination above native: only the host finalizer constructs HostTermination (D9 invariant-one-mapper); '
                  'the host reduces concurrent faults, rejections and deficiencies, taking primary and secondaries from its own ordered set '
                  '(concurrentConditionReducer, causeModel.codeDerivation); required-relation-missing and confidence-floor-unmet have no entry carrier and '
                  'are requirement-relative (cause registry rows; native section 4.6; D9 goldens analysis-required-coverage-missing and '
                  'analysis-confidence-floor-unmet are requirement scenarios); required execution deficiencies and gating-rule indeterminacy make the '
                  'sealed verdict indeterminate (evaluator-composition-contract section 5). Measured: the helper derives those two codes only when an entry '
                  'declares them, and a stage-implied primary can differ from the typed-detail entry deficiency.'),
   'preserved': ['the total native DeficiencyV2 -> D9 route (nine rows, drift-free, refuses non-members)', 'native stage/entry precedence and nativeCauses',
                 'faulted/cancelled stages keep their own termination', 'host secondaryDeficiencies composition', 'no per-requirement D9 code',
                 'no new proof-cause, requirement or import ordering recipe'],
   'ownerCitations': ['docs/coop/artifacts/d9-exit-contract.v1.14.json invariants[invariant-one-mapper], concurrentConditionReducer, causeModel (precedence, codeDerivation, theOneException), crossAxisInvariants X1/X4/X10, goldenCases analysis-required-coverage-missing / analysis-confidence-floor-unmet / analysis-multiple-deficiencies',
                      'native-evidence.schemas.v2.json#/x-opensip-deficiency-cause-registry/deficiencies (confidence-floor-unmet and required-relation-missing: carrier none-in-entry)',
                      'native-evidence.md section 4.6 (per-requirement outcome), section 10 rows, line 70 (D9 class assignment is host-owned)',
                      'evaluator-composition-contract.v3.md section 5 (lines 56, 58) and line 315',
                      'workflows-and-surfaces.md lines 783-796 (D9Deficiency carries whole-Run terminations), 1137-1147 (termination branch contract), 1386-1388 (host projects D9 class/code)'],
   'measured': {'runTermination': p01['runTermination'], 'observations': ob, 'helperSignature': p01['helperSignature'], 'nativeRoute': p01['nativeRouteTotal']},
   'modelIssue': 'docstring only: run_termination says "the Run\'s PRIMARY deficiency"; recommended wording scopes it to the stage and names the host reduction. No behaviour change.',
   'advisory': ('A stage-implied primary (for example BudgetExhausted with a resolution-incomplete entry, or Unavailable with a budget-exhausted entry) '
                'yields a code that differs from the typed-detail deficiency; the author text publishes that the typed detail names the entry. How a host '
                'pairs a coverageId with such a termination is host/D9 territory and is not decided here.'),
   'recommendedEdits': [e for e in EDITS if e['issue'] == 3]}},
 'recommendedEditsRehearsal': {'files': files, 'allAnchorsExactlyOnceInAuthorImages': all(e['anchorOccurrencesInAuthorImage'] == 1 for e in EDITS),
                               'editedModelCompiles': True, 'diff': 'recommended-edits.diff', 'diffSha256': sha(os.path.join(BASE, 'recommended-edits.diff')),
                               'notRun': 'no suite or checker was rerun; the edits are prose and one docstring'},
 'limits': ['Targeted helper/wrapper probe only; no global suite, pin, planning or generated-report run.',
            'The recommended texts were anchored and applied only to disposable copies of the captured images; the author owns applying them.',
            'The scope boundary names the host reduction but deliberately does not define how requirement, proof-cause, import or verdict outcomes are ordered in it.',
            'coverageId pairing for stage-implied primaries is left to host/D9.',
            'The author assembly itself and its receipts were not read beyond the captured report, manifest and images.'],
 'carried': {'TCB-SCOPE-01': 'one shared assumption over 13 dependent rows, not closed', 'productGates': '32, 0 performed, condition 5 NOT MET',
             'plannedRecoveryCases': '54, 0 executed', 'source36Acceptance': 'reopened; nothing granted here', 'authority': 'no final application or readiness authority'},
 'probeErrors': ['p01 predicate helperInputsAreOnlyStageAndEntries was False only because the module uses postponed annotations, so the signature string is '
                 "(stage: 'dict', coverage_entries: 'list[dict]') -> 'dict'; the helper's inputs are exactly its stage and entries."],
 'receipts': {f: sha(os.path.join(RC, f)) for f in sorted(os.listdir(RC)) if f.endswith('.json') and not f.startswith('i0')},
 'grantsNothing': True}
json.dump(J, open(os.path.join(BASE, 'reconciliation.json'), 'w'), indent=1, ensure_ascii=False)
print('edits', [(e['issue'], e['file'].split('/')[-1], e['kind']) for e in EDITS], '| model compiles | diff', J['recommendedEditsRehearsal']['diffSha256'][:12])
print('reconciliation.json', sha(os.path.join(BASE, 'reconciliation.json')))
