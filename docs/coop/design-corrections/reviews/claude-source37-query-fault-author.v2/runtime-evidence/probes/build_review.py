"""Assemble review.json from this runtime's actual receipts (exact hashes/counts/exit codes) plus the authored dispositions."""
import glob, hashlib, json, os

RT = '/private/tmp/opensip-design-corrections/claude-source37-query-fault-author.v2'
R = RT + '/receipts'
V1 = '/private/tmp/opensip-design-corrections/claude-source37-query-fault-author.v1'


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def load(p):
    return json.load(open(p))


runs = []
for f in sorted(glob.glob(R + '/runs/*.run.json')):
    d = load(f)
    base = f[:-len('.run.json')]
    parsed = None
    try:
        j = json.loads(open(base + '.stdout').read())
        parsed = {k: (len(j[k]) if isinstance(j.get(k), list) else j[k]) for k in ('passed', 'failed', 'count', 'failedCount') if k in j}
    except ValueError:
        parsed = 'no JSON stdout (see stderr)'
    rep = None
    for cand in glob.glob(R + '/runs/' + d['name'] + '.' + d['tree'] + '.report.json'):
        rep = {'path': os.path.relpath(cand, RT), 'sha256': sha(cand)}
    runs.append({'name': d['name'], 'tree': d['tree'], 'exitCode': d['exitCode'], 'seconds': d['seconds'],
                 'command': d['command'], 'scriptSha256': d['scriptSha256'], 'treeFileCount': d['treeFileCount'],
                 'treeUnchanged': not (d['treeChanged'] or d['treeExtra'] or d['treeRemoved']),
                 'stdoutSha256': d['stdoutSha256'], 'stderrSha256': d['stderrSha256'], 'parsed': parsed, 'report': rep,
                 'receipt': os.path.relpath(f, RT)})

edit = load(R + '/edit-hashes.json')
setup = load(R + '/continue-setup.json')
comparison = load(R + '/comparison.json')
fault_rows = {t: {'count': load(R + '/probe-fault-owner-rows.' + t + '.json')['count'],
                  'notAsExpected': load(R + '/probe-fault-owner-rows.' + t + '.json')['notAsExpected']}
              for t in ('source37-frozen', 'source37-pristine', 'source37-coauthor')}
review = {
    'schema': 'opensip.bounded-coauthor.query-fault.source37.v2',
    'author': 'Claude (claude-opus-5), same query-fault coauthor session f5617310-c7c7-4d85-acdd-31370f220944, v2 continuation',
    'standing': 'Bounded design/reference coauthor proposal for RC37-01 and RC37-A1. Not independent acceptance, not whole-design, application, readiness or grade. All product qualification gates and recovery cases remain unperformed. No source-pin or planning rebind, freeze, product, activation, commit or push.',
    'v1IncompleteTermination': {
        'runtime': V1,
        'facts': [
            'v1 CLI exited 0 while its final response said it was waiting on two background checker batches (run_in_background). Those batches were stopped at session teardown; no batch summary exists.',
            'v1 public receipts that did complete: copy/copy-pristine verification, exception-identity probe before/after, check-query-projection on the edited tree (193/0), edit-hashes.json, proposed-edits.diff, and check-composition on both trees. No review.md/json was written.',
            'v2 did not reuse any v1 checker result as a pass; every focused check was rerun in the foreground in this runtime.',
        ],
        'v1PreservedUnchanged': load(R + '/v1-inventory.after-checks.json')['equalToBefore'],
        'v1InventoryFiles': load(R + '/v1-inventory.after-checks.json')['files'],
    },
    'inputs': {
        'immutableOverlayManifestSha256': setup['overlayManifestSha256'],
        'parentFrozen37ManifestSha256': setup['parentManifestSha256'],
        'immutableOverlayVerified': setup['immutableOverlayVerified'],
        'v1EditHashesVerified': setup['v1EditHashes'],
        'pristineCopy': setup['source37-pristine'],
        'coauthorCopy': setup['source37-coauthor'],
        'frozen37BaselineCopy': load(R + '/copy-frozen37.json'),
        'portedProbes': setup['portedProbes'],
        'probeScriptsFinalSha256': comparison['probeScripts'],
    },
    'proposal': {
        'files': edit['files'],
        'proposedEditsDiff': {'path': 'proposed-edits.diff', 'sha256': sha(RT + '/proposed-edits.diff'),
                              'equalsV1Diff': sha(RT + '/proposed-edits.diff') == sha(V1 + '/proposed-edits.diff')},
        'onlyTheseFilesDifferFromInput': setup['source37-coauthor']['differsFromInput'],
        'rootSuccessorOverlap': 'none: all six files still equal their input bytes in the root successor (rootSuccessorEqualsBefore)',
    },
    'dispositions': [
        {
            'id': 'RC37-01', 'item': 'A37-06', 'severity': 'SHOULD',
            'disposition': 'CORRECTED-IN-COAUTHOR-PROPOSAL (not independently accepted)',
            'problemMeasured': 'Before-probe on the verified input overlay: all four fully reminted semantic false-result Runs, the structural REFERENCE_IDENTITY refusal and four simulated host defects (RuntimeError/KeyError with owner-key text, a foreign identity-copy class, a TypeError inside the loaded replay comparison) all projected HOST.IO_FAILURE/host-io/evidence.corrupt. Every refusal escaping close_run was a class object of the separately loaded replay stack; none was an instance of the query identity copy classes, so isinstance(exc, M.EvidenceUnavailable) never held and the EVIDENCE_UNAVAILABLE message prefix was the load-bearing missing-bytes route.',
            'correction': [
                'identity-model.v3: new condition-only CompleteReplayMismatch(C.AdmissionError) with exact diagnostic (no termination, no origin). close_run normalizes the replay stack declared outcomes into this module classes by exact class object (EvidenceUnavailable, CompleteReplayMismatch, C.AdmissionError for declared owner refusals), preserving message and chaining the original; any other exception propagates unchanged. EvidenceStore.restore, a retained regeneration boundary, maps CompleteReplayMismatch to the existing RegenerationMismatch carrier.',
                'evaluator_composition_model.v3 compare_complete_replay and evaluator_replay_model.v3 proof-id/evidence/seal/Run comparisons raise CompleteReplayMismatch with the unchanged comparison key. evaluator_replay_model.v3 declares UNAVAILABLE, MISMATCHES and REFUSALS tuples of the exact class objects of its own loads (mirroring execution_inputs_model CATCH).',
                'query_projection_model.v3 close_retained_run: identity EvidenceUnavailable -> evidence.missing; CompleteReplayMismatch -> identity RegenerationMismatch carrier projected verbatim (complete-replay-mismatch:retained-regeneration, HOST.IO_FAILURE/host-io/evidence.regeneration-mismatch, subject refused RunId); other identity AdmissionError -> evidence.corrupt; anything else -> existing host-internal law SYSTEM.OUTCOME.ILLEGAL_STATE/host-invariant/HOST.INVARIANT_VIOLATED, subject close_run. QueryRefusal.diagnostic retains the exact owner text and never selects a route. No message prefix/split remains.',
                'query-projection-contract.v3 section 7: replaced the A06 paragraph that legitimized evidence.corrupt with the four typed outcomes; table rows updated; live first-party evaluator contradiction explicitly keeps complete-replay-mismatch:host-internal at its own boundary.',
            ],
            'typeIdentityAssessment': 'Each importlib load mints distinct class objects: the query identity copy, the replay stack identity copy (composition_identity3), enumeration identity/native copies, atom canonical copy, and the query sys.path canonical are pairwise distinct (maintained control replay-stack-is-a-separate-identity-load). Identity close_run is the one boundary that owns the replay-stack module objects, so it is where normalization happens; the query then routes only by its own identity copy. A same-named CompleteReplayMismatch from another identity copy reaching the query is treated as a host defect (control foreign-identity-copy-mismatch-is-host-invariant). The execution-inputs model loads per call but already converts its refusals into the stack canonical AdmissionError (measured).',
            'originLaw': 'Evaluator fault registry routes byte-identical in model and schema (untouched files). Row-isolated replica probe: all 24 condition/origin routes and details identical across frozen37, input overlay and edited tree; owner-carrier rows admit on the edited tree; a condition-only CompleteReplayMismatch is refused as an owner carrier (EVALUATOR_FAULT_OWNER_CARRIER), so the condition cannot bypass origin assignment. Query never produces provider-protocol or CONFIG.INVALID routes.',
            'after': comparison['exceptionProbeTable'],
            'runIdsStable': {'equal': comparison['runIdsEqual'], 'runIds': comparison['runIds']},
        },
        {
            'id': 'RC37-A1', 'item': 'A37-05', 'severity': 'advisory',
            'disposition': 'ADDRESSED-IN-COAUTHOR-PROPOSAL (not independently accepted)',
            'decision': 'ReferenceCallPrecondition remains the correct signal for the reference entry execute_graph_query, where the trusted observation is a call argument (unchanged: omitted allowed, request-schema and missing-Run precedence preserved, present null/wrong type/unknown token refused). A product host adapter produces the observation itself: its own out-of-vocabulary observation is an invalid host-generated internal layer and, with a valid reserved RequestId, terminates operational-failed/SYSTEM.OUTCOME.ILLEGAL_STATE/host-invariant/exit 4/HOST.INVARIANT_VIOLATED subject host.availability (reference host_adapter_refusal). Without a valid RequestId, or for the RequestId precondition itself, no envelope exists and the precondition is re-raised. A retained identity availability record read from the store that fails identity $defs/availability admission or names another Run is corrupt retained evidence (HOST.IO_FAILURE/evidence.corrupt, reference observe_retained_availability); an admitted record supplies its state as the observation. No new public code.',
        },
    ],
    'admittedBehaviorImpactOfFoundationTypedBoundaries': {
        'summary': 'Foundation changes alter exception classes, not decisions or messages: close_run refusal messages and class names are unchanged; comparison refusals remain AdmissionError subclasses with the same keys; restore now raises RegenerationMismatch (previously an unnormalized replay-stack AdmissionError) for a semantically disagreeing retained Run. Eleven maintained affected owners produce byte-identical stdout/stderr on input and edited trees (two only after normalizing the tree directory name in paths); only check-query-projection differs, by design (162 -> 193 checks, 0 failed).',
        'pristineVsEditedOutputs': comparison['pristineVsCoauthorOutputs'],
        'pathOnlyDifferences': load(R + '/output-difference-explanation.json'),
    },
    'newIntegrationFindings': [
        {
            'id': 'QF-I1', 'severity': 'SHOULD (root/evaluator-fault owner; outside this coauthor scope)',
            'title': 'Root overlay StepTermination pair law breaks maintained check-evaluator-faults.v3 (pre-existing, not caused by this proposal)',
            'evidence': 'check-evaluator-faults.v3 exits 0 (40 rows) on frozen37, exits 1 identically on the verified input overlay and on the edited tree. Control envelope-termination-origin mutates termination errorCode to HOST.IO_FAILURE with faultCause provider-protocol; the overlay common.schema operational pair law now refuses it by jsonschema ValidationError inside workflow_projection_model.validate_profile before evaluator_fault_model.validate_envelope reaches EVALUATOR_FAULT_ENVELOPE_PARITY, and the checker re-raises, aborting before the owner-carrier rows. The mutated envelope is still refused (fail-closed). Row-isolated replica: the only frozen37-vs-overlay difference is that row; all later rows pass.',
            'faultOwnerRowProbe': fault_rows,
            'remedy': 'Root/evaluator-fault owner decides whether that control expects the earlier schema refusal (e.g. accept the pair-law ValidationError as the parity refusal) or validate_envelope checks parity before profile validation; then rerun check-evaluator-faults.v3. Not edited here (not one of the owned files).',
        },
        {
            'id': 'QF-I2', 'severity': 'integration consequence',
            'title': 'Source pins stale for the six files (no rebind performed)',
            'evidence': 'All six files are pinned in foundation/source-pins.v1.json, foundation/evaluator3-source-pins.v1.json, workflows/source-pins.v1.json, security/source-pins.v1.json and native/source-pins.v2.json. The three foundation files become newly stale; the three query files were already stale from the root overlay (RC37-A2), as are workflows-report.v1.json rows for query_projection_model.v3.py and check-query-projection.v3.py. None is in implementation-normative-inputs.v5.json.',
        },
    ],
    'registeredIdentity': 'No registered payload/digest-domain schema document changed (all six files are .py/.md). identity-schemas.v3.json, evaluator-fault-observation.schema.v3.json, public-detail-registry and both common schemas untouched. Maintained lawful RunIds identical before/after; semantic, execution, candidate, provider-attribution and identity checker outputs byte-identical.',
    'focusedReceipts': runs,
    'notRun': ['global suites, pin/planning checkers, freeze', 'host-finalizer, security carrier, semantic fixture, new termination owners (other coauthor/root)', 'product qualification gates and recovery cases'],
    'limitations': [
        'Reference Python models over synthetic native-admitted fixtures; no product host adapter, evidence store, compiler, provider or platform qualification.',
        'REFUSALS is an explicit closed list of the replay stack owner refusal classes; an owner that later raises a new refusal class outside it will surface as a host-invariant fault until listed. The measured corpus (structural, missing, semantic, execution-input refusals) contained only listed classes; atom/enumeration/native refusal classes were not individually triggered through close_run.',
        'Host-defect controls monkeypatch close_run or the loaded replay comparison in-process; they model untyped failures, not real host faults.',
        'Live first-party evaluator boundary (complete-replay-mismatch:host-internal) is law in the contract but has no reference producer in these files; it belongs to the whole-Run host termination owner.',
        'check-evaluator-faults.v3 is a preserved failure on input and edited trees (QF-I1); its skipped rows were executed only by the row-isolated replica probe, which is not the maintained checker.',
        'Planning/pin staleness (RC37-A2, QF-I2) not rebound.',
    ],
}
json.dump(review, open(RT + '/review.json', 'w'), indent=1)
print(json.dumps({'reviewJsonSha256': sha(RT + '/review.json'), 'runs': len(runs), 'diffEqualsV1': review['proposal']['proposedEditsDiff']['equalsV1Diff'],
                  'v1Preserved': review['v1IncompleteTermination']['v1PreservedUnchanged']}, indent=1))
