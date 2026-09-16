"""Assemble review.json and review.md for the bounded root-corrections overlay review (stdlib only)."""
import hashlib, json, os

RT = '/private/tmp/opensip-design-corrections/claude-source37-root-corrections-review.v1'
OV = RT + '/work/source37-overlay'
BASE = '/tmp/opensip-design-corrections/candidate-subject.v37'
MAN37 = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v37.json'
CE3 = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/claude-source37-termination-boundary-assessment.v1/runtime-evidence/assessment.md'
REC = RT + '/receipts/'


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def J(p):
    return json.load(open(p))


def rows(o):
    if isinstance(o, list) and o and isinstance(o[0], dict) and 'path' in o[0] and 'sha256' in o[0]:
        return o
    if isinstance(o, dict):
        for v in o.values():
            x = rows(v)
            if x:
                return x


MAN = {r['path']: r['sha256'] for r in rows(J(MAN37))}
OVM = J(RT + '/subject-manifest.json')
OVF = {f['path']: f for f in OVM['files']}
copy_rec = J(REC + 'overlay-copy.json')
diffs = J(REC + 'diff-summary.json')
sem = J(REC + 'probe-overlay-semantics.json')
plan = J(REC + 'probe-planning-binding.json')


def run(name):
    r = J(REC + 'runs/' + name + '.run.json')
    return {k: r[k] for k in ('name', 'command', 'scriptSha256', 'exitCode', 'seconds', 'copyChanged', 'copyExtra', 'stdoutSha256', 'stderrSha256')}


# ---------------------------------------------------------------- read accounting
overlay_reads = []
for f in OVM['files']:
    p = RT + '/subject/' + f['path']
    assert sha(p) == f['sha256']
    d = next(x for x in diffs if x['path'] == f['path'])
    complete = f['path'] in ('docs/coop/design-corrections/workflows/query-projection-contract.v3.md', 'docs/v2/architecture/prototype-report-inventory.md')
    overlay_reads.append({'path': f['path'], 'beforeSha256': f['beforeSha256'], 'sha256': f['sha256'], 'bytes': f['bytes'],
                          'verifiedBeforeRead': True,
                          'read': 'complete file' if complete else 'complete base-to-overlay unified diff (%d diff lines, +%d/-%d) plus changed-region context' % (d['diffLines'], d['added'], d['removed']),
                          'diffReceipt': d['diff'], 'diffReceiptSha256': sha(RT + '/' + d['diff'])})
CONTEXT = [
    ('docs/coop/design-corrections/foundation/evaluator-fault-contract.v3.md', 'lines 1-90'),
    ('docs/coop/design-corrections/foundation/evaluator-fault-observation.schema.v3.json', 'complete-replay-mismatch condition/origin rows and x-opensip-routes (grep with context)'),
    ('docs/coop/design-corrections/foundation/identity-schemas.v3.json', '$defs/availability (1641-1691); x-opensip-payload-registry (4692-4811); digest-domain records (grep)'),
    ('docs/coop/design-corrections/public-detail-registry.v1.json', 'evidence.corrupt/missing/regeneration-mismatch and HOST.INVARIANT_VIOLATED records (grep)'),
    ('docs/coop/artifacts/d9-exit-contract.v1.14.json', 'hostTerminationUnion 824-953; codeVocabulary 954-982'),
    ('docs/coop/artifacts/resolved-inputs.v2.json', 'lines 220-259'),
    ('docs/v2/contracts/product-v1/workflows-and-surfaces.md', 'overlay §0 lines 54-72 and §9 lines 1134-1177'),
    ('docs/v2/architecture/implementation-normative-inputs.v5.json', 'complete (150 lines)'),
    ('docs/v2/architecture/implementation-coverage.v1.json', 'lines 1-72 (subject/sources)'),
    ('docs/v2/architecture/implementation-planning-sources.v1.json', 'lines 1-40, 225-244 and path/sha grep'),
    ('docs/coop/design-corrections/native/native_evidence_model.v2.py', 'public_termination_for 1038-1097'),
    ('docs/coop/design-corrections/native/native-evidence.schemas.v2.json', 'StepTermination mentions (grep with context)'),
    ('docs/coop/design-corrections/workflows/query_surface_projection.v3.py', 'lines 85-114 and 260-354'),
    ('docs/coop/design-corrections/workflows/workflows_model.v1.py', 'FAULT_TO_ERROR and terminate headers (grep)'),
    ('docs/coop/design-corrections/workflows/command-inventory.v3.json', 'query-response parity field (grep)'),
    ('docs/coop/design-corrections/workflows/schemas/evaluator3/common.schema.json', 'overlay StepTermination 738-1147'),
    ('docs/coop/design-corrections/workflows/schemas/evaluator3/graph-query.schema.json', 'overlay 1140-1205'),
    ('docs/coop/design-corrections/workflows/query_projection_model.v3.py', 'overlay 1420-1464'),
    ('docs/v2/architecture/implementation-boundaries-and-build-plan.md', 'overlay 1-40, 195-206, 770-781, 1025-1099'),
]
context_reads = []
for rel, what in CONTEXT:
    p = OV + '/' + rel
    want = OVF[rel]['sha256'] if rel in OVF else MAN[rel]
    got = sha(p)
    assert got == want, rel
    context_reads.append({'path': rel, 'sha256': got, 'source': 'overlay' if rel in OVF else 'unchanged source37 byte (manifest-verified)', 'read': what})
ce3 = {'path': CE3, 'sha256': sha(CE3), 'read': 'complete (138 lines); public assessment only'}

# ---------------------------------------------------------------- findings
A6 = sem['A6']
A5 = sem['A5']
R12 = sem['R12']
S3 = sem['S3']
ID = sem['ID']

findings = [
    {
        'id': 'RC37-01', 'severity': 'SHOULD', 'item': 'A37-06',
        'title': 'The new graph-query route for complete-replay disagreement conflicts with the existing evaluator fault owner route for the same condition and selects by exception text',
        'ownerSelectors': [
            'overlay query-projection-contract.v3.md:164 and §7 table row at line 181 (structurally admitted retained Run whose complete proof replay disagrees -> HOST.IO_FAILURE / evidence.corrupt; subject preserves the diagnostic)',
            'foundation/evaluator-fault-contract.v3.md:15 ("Complete semantic replay disagrees with an otherwise admitted sealed result | evidence.regeneration-mismatch under the retained regeneration boundary; a live first-party evaluator contradicting its own reconstruction is a host invariant fault") and :72-75',
            'foundation/evaluator-fault-observation.schema.v3.json x-opensip-routes "complete-replay-mismatch:retained-regeneration" (HOST.IO_FAILURE, host-io, evidence.regeneration-mismatch) and "complete-replay-mismatch:host-internal" (SYSTEM.OUTCOME.ILLEGAL_STATE, host-invariant, HOST.INVARIANT_VIOLATED)',
            'foundation/evaluator-fault-contract.v3.md:3 (the host applies the route for the boundary and "does not infer origin from ... a prefix in the error text"); overlay query contract :160 ("never by a filename, exception prefix or caller-supplied fault origin")',
            'overlay query_projection_model.v3.py close_retained_run (unchanged catch-all Exception -> evidence.corrupt)',
        ],
        'reproducer': {'receipt': 'receipts/probe-overlay-semantics.json#A6',
                       'observed': {k: {x: v.get(x) for x in ('result', 'errorCode', 'detail', 'faultCause', 'exitCode', 'subject', 'structuralOwnerClosure')} for k, v in A6['cases'].items()},
                       'ownerRoutes': A6['ownerRoutes']},
        'consequence': ('Two owners now publish different public details for the same named condition: the query owner gives evidence.corrupt, and the evaluator fault registry gives evidence.regeneration-mismatch (retained) or HOST.INVARIANT_VIOLATED (host-internal). '
                        'The structural refusal (REFERENCE_IDENTITY), all four semantic mutants and a simulated host defect inside close_run all project to the same class, code and detail. They differ only in subject text, which is the exception-prefix selection both contracts forbid. '
                        'Operators get the corrupt-bytes remedy for a semantically false Run and for a host bug. The overlay control proves the refusal but cannot detect the owner conflict. The public fail-closed outcome (exit 4, no items, no Run) is correct, so this is SHOULD, not MUST.'),
        'minimalRemedy': ('Route this row through the evaluator fault registry rather than a query-local choice: retained complete-replay mismatch -> evidence.regeneration-mismatch, and a live/host defect -> host-invariant. '
                          'Type the replay-mismatch observation (for example identity RegenerationMismatch or a typed fault observation) instead of catching every Exception. '
                          'If root prefers evidence.corrupt, amend the evaluator fault contract, registry and routes in the same successor with a stated remedy distinction. Add a control proving that the structural, semantic and host-defect refusals are distinguishable by typed route, not by subject text.'),
        'disposition': 'NOT-CLOSED; the corrected behaviour is fail-closed but the route is not owner-consistent',
    },
]
advisories = [
    {
        'id': 'RC37-A1', 'item': 'A37-05',
        'title': 'The closed availability vocabulary and ReferenceCallPrecondition are honest reference-harness law; the product-host outcome should cite the existing host-invariant route',
        'detail': ('The overlay closes the vocabulary (retained, partial, purged, expired, corrupt, unavailable, plus the direct missing alias). Every present null, wrong type, unknown token, case or whitespace variant, bytes or container value raises ReferenceCallPrecondition(host.availability); omitted stays allowed (probe A5, 17 rows). '
                   'Request-schema refusal precedes it, as does missing-Run refusal. This is not a hidden new public code, and it removes the silent grant-by-omission the original advisory named. '
                   'The RequestId analogy is only partial. Without a RequestId no failure envelope can be built, but with a valid RequestId an out-of-vocabulary observation leaves a representable public outcome. The existing evaluator fault law already routes an "Invalid host-generated internal layer" to operational-failed / SYSTEM.OUTCOME.ILLEGAL_STATE / host-invariant / HOST.INVARIANT_VIOLATED (evaluator-fault-contract.v3.md:11), and that termination and envelope validate (A5.hostInvariantRouteRepresentable). '
                   'The overlay text names only what the observation must not become and leaves the product host outcome to be invented. A malformed availability record read from retained store bytes is a different cause (identity availability admission / corruption) from an adapter bug.'),
        'remedy': 'Add one sentence: a product host adapter that produces an out-of-vocabulary observation terminates by the existing host-invariant route; unreadable or invalid retained availability record bytes follow identity availability admission. No new code is needed.',
        'disposition': 'SUBSTANTIVELY-ADDRESSED-FOR-REFERENCE; product-host pointer advisory',
    },
    {
        'id': 'RC37-A2', 'item': 'integration',
        'title': 'The overlay invalidates the current planning binding that A37-07 wording names; a rebind is required before integration',
        'detail': ('check_implementation_planning --check on the verified overlay copy exits 1 with "Planning source changed: query" and stops at the first failure (preserved failure, receipts/runs/check_implementation_planning.*). '
                   'The full stale-binding list is in receipts/probe-planning-binding.json. implementation-normative-inputs.v5.json still pins the pre-overlay bytes of %s; implementation-coverage sources %s are stale; the five source-pins files and workflows-report still pin changed files. '
                   'The new build-plan sentence ("Current planning is bound by the architecture.manifestPath and manifestSha256 in that record") is accurate for source37, but it is not true of any candidate that includes this overlay until v5, coverage and pins are rebound. The instruction forbade regeneration here, so this is not a defect of the correction text.') % (plan['normativeInputsV5Stale'], plan['coverageSourcesStale']),
        'remedy': 'At integration, rebind a successor normative-input manifest, regenerate coverage selectors (R02/R24 values and workflows-and-surfaces §9 onward shift) and source pins, then re-run the planning checkers. The A07 wording should then name that successor.',
        'disposition': 'ROUTED-TO-INTEGRATION',
    },
    {
        'id': 'RC37-A3', 'item': 'R1/R2',
        'title': 'request-rejected still admits fault-family errorCodes (no global partition, deliberately); union field placements not imported',
        'detail': ('All 19 D9ErrorCode members remain admitted on request-rejected, including the 11 fault-map codes, so request-rejected+HOST.IO_FAILURE still validates. This matches root\'s deliberate choice and ce3 A1; no legitimate operation-specific request-rejected route is excluded (the request-rejected errorCode set is identical base versus overlay). '
                   'The superseded D9 v1.14 hostTerminationUnion also placed runId/coverageId/executionId/details per class (for example no runId on request-rejected, coverageId only on indeterminate). The successor StepTermination owns that closure (workflows-and-surfaces §0:66), and the overlay imports none of those placement rules; this review did not assess them.'),
        'remedy': 'None required for R1/R2. If class-specific error families or field placement are wanted, decide them in the D9 successor owner, not by importing the superseded union.',
        'disposition': 'ACCEPTED-AS-DESIGNED; placement outside R1/R2 scope',
    },
    {
        'id': 'RC37-A4', 'item': 'A37-07',
        'title': 'Remaining candidate25 mentions are provenance or historical, apart from one proposal sentence',
        'detail': ('Overlay build plan lines 10 and 15 are the new provenance wording. Lines 1089 and 1098 sit under "Historical author verification checkpoints" and are preserved receipts. Lines 777 and 926 are provenance. '
                   'Line 201 still says "not a claim that candidate25 already specifies or implements that private table", which is harmless provenance but could name the current normative layer instead.'),
        'remedy': 'Optional editorial change at the next rebind.',
        'disposition': 'ACCEPTED-WITH-EDITORIAL-NOTE',
    },
]

dispositions = [
    {'id': 'S37-02', 'disposition': 'CLOSED-BY-OVERLAY-TEXT (subject to integration rebind RC37-A2)',
     'assessment': ('R02 (line 37) now reads "Presentation consumes versioned host-approved data projections only. Executable report hooks are not admitted under admission-and-qualification §5; trusted built-in projection and rendering code remain host-owned." '
                    'R24 External tools (line 179) reads "Versioned host-approved data projections from selected admitted first-party capabilities ... host-owned validation, keys and rendering; no executable report-hook admission". '
                    'This agrees with admission §5 items 1, 3, 4 and 5. Searching the overlay inventory case-insensitively for hook/worker/isolat/sandbox finds only these two negations (lines 37 and 179); no worker-lane or isolation claim remains. R01-R23 are unchanged. The coverage owners (report-view.ts, reporting/projection.rs) now fit the text.'),
     'appliedByThisReview': False, 'finalApplicationOutcomeGranted': False},
    {'id': 'S37-03', 'disposition': 'CLOSED-FOR-SCHEMA-AND-CONTROLS (subject to integration rebind RC37-A2)',
     'assessment': ('The added else branch (graph-query.schema.json:1190-1200) makes admission equal the "true exactly for four operations" law across all 20 operations x advisory {true, false} (probe S3: overlayEqualsLaw=true; base violated 13 non-advisory operations). '
                    'Graph operations keep their existing const false. Consumers: no retained query-response JSON fixture exists (0 scanned); query_surface_projection emits advisory False only for graph and coverage.show responses; command-inventory names query-response only as a parity field. No consumer admission changes. '
                    'The overlay controls passed (check-query-projection 162/162, including 6 non-advisory and 9 advisory rows). graph-query.schema.json is not a registered payload document and not in registered_schema_documents before or after; it is a v5 normative input (see RC37-A2).'),
     'appliedByThisReview': False, 'finalApplicationOutcomeGranted': False},
    {'id': 'A37-05', 'disposition': 'SUBSTANTIVELY-ADDRESSED-WITH-ADVISORY (RC37-A1)', 'assessment': 'See RC37-A1.', 'appliedByThisReview': False, 'finalApplicationOutcomeGranted': False},
    {'id': 'A37-06', 'disposition': 'NOT-CLOSED (RC37-01 SHOULD)',
     'assessment': 'A deliberate evidence.corrupt route with the replay subject and an actual fully reminted mutant through the strong public query was added and passes. It conflicts with the evaluator fault owner route for complete-replay-mismatch and separates structural, semantic and host-defect causes only by subject text. My original A37-06 remedy accepted evidence.corrupt "if chosen deliberately"; that remedy overlooked evaluator-fault-contract.v3.md:15 and is corrected here.',
     'appliedByThisReview': False, 'finalApplicationOutcomeGranted': False},
    {'id': 'A37-07', 'disposition': 'CLOSED-FOR-WORDING (RC37-A2 integration consequence; RC37-A4 editorial)',
     'assessment': 'The build-plan lines 10-22 and 1043-1052 now name the v5 normative-input binding and the coverage subjectManifest instead of candidate25 ownership. Historical receipts at 1083-1099 are preserved. The claimed binding (planning-sources architecture.manifestSha256 = coverage subjectManifestSha256 = 4b4b35b7...) holds for source37 bytes.',
     'appliedByThisReview': False, 'finalApplicationOutcomeGranted': False},
    {'id': 'A37-08', 'disposition': 'UNCHANGED-AS-INTENDED',
     'assessment': 'Native §10 supersession of the registered schema annotation is unchanged; native-evidence.schemas.v2.json bytes are unchanged in the overlay (not an overlay row).',
     'appliedByThisReview': False, 'finalApplicationOutcomeGranted': False},
    {'id': 'R1', 'disposition': 'ACCEPTED-FOR-SCHEMA-LAW (reference; producers unchanged)',
     'assessment': ('Both common StepTermination definitions are identical before and after (probe R12.defsEqual). faultCause is now refused on success, policy-failed, request-rejected, indeterminate and interrupted; reasonCodes on every class except indeterminate. '
                    'An exhaustive class x {absent + 12 faultCause} x {reasonCodes absent/present} x {absent + 19 errorCode} enumeration (3120 combinations) gives: base 990 admitted, overlay 34; 956 removed; 0 newly admitted; 0 removed combinations lawful under the D9 predicate; 0 overlay admissions unlawful. '
                    'The union had no faultCause field and the successor (workflows-and-surfaces §0:66, §9:1140-1148) declares it only for operational-failed. So refusing faultCause "none" on other classes follows the successor field closure, not a stale union rule. D9 v1.14 scenarioAxes faultCause "none" values are axes, not carriers. '
                    'Producers: 24 evaluator fault routes and 24 native public routes validate identically before and after. The 25th native key (release-capability-undeclared) returns None by design (notATermination), a probe artifact. Of 90 termination-shaped JSON fixture objects, exactly the 12 new reject vectors (workflow-cases terminationVectors/reject/12-23) change admission.'),
     'appliedByThisReview': False, 'finalApplicationOutcomeGranted': False},
    {'id': 'R2', 'disposition': 'ACCEPTED-FOR-SCHEMA-LAW',
     'assessment': ('operational-failed now requires one of exactly 11 faultCause/errorCode pairs equal to workflows_model.FAULT_TO_ERROR, including host-invariant -> SYSTEM.OUTCOME.ILLEGAL_STATE (probe R12.operationalPairsEqualHostMap=true). The existing required [errorCode, faultCause] and faultCause != none remain. '
                    'Maintained controls ran and passed on the overlay copy: check_workflows.v1 1816 passed / 0 failed (legacy common profile, including termination.fault-pairs-equal-host-fault-map and the 12 reject vectors), check-workflow-projection.v3 493 / 0 failed (current common:3 profile, including current-termination-fault-pairs-equal-host-map and all shared vectors).'),
     'appliedByThisReview': False, 'finalApplicationOutcomeGranted': False},
]

identity = {
    'registeredPayloadIdentity': ('No change. payloadSchemaDigest is the raw SHA-256 of the registered document named by x-opensip-payload-registry, and no registered or digest-domain document is an overlay row. None $refs StepTermination, GraphQueryResponseV1, evaluator3 common or graph-query. '
                                  'imported-evidence, test-execution and policy-document(.v2) $ref other workflows common definitions (Blob, LogicalPath, Sha256Hex, ...), which the overlay does not change (the common-schema diff touches only StepTermination). No overlay file is in registered_schema_documents before or after.'),
    'retainedIdentities': 'No reminting required for source37 fixtures. Four actual closed Runs rebuilt on the overlay copy have RunIds identical to the retained source37 review receipts (declares-exists, incoming-incomplete, missing-inventory, owner graph). No retained Run closure, import payload or H-domain record carries a StepTermination or query response.',
    'pinsAndPlanning': 'Raw digests of all 12 files change; the five source-pins files, workflows-report, normative-inputs v5, coverage sources and planning-sources architecture record still carry pre-overlay digests (RC37-A2). These are review pins, not payload identities.',
    'notAssessed': 'A future signed product release closure that ships these schema documents would get new closure bytes; no such retained closure exists in source37.',
    'evidence': {'probe': 'receipts/probe-overlay-semantics.json#ID', 'runIdentityStability': ID['runIdentityStability'], 'planning': 'receipts/probe-planning-binding.json'},
}

probes = [
    {'id': 'P-COPY', 'script': 'probes/make_overlay_copy.py', 'scriptSha256': sha(RT + '/probes/make_overlay_copy.py'), 'receipt': 'receipts/overlay-copy.json', 'result': {k: copy_rec[k] for k in ('source37ManifestSha256', 'overlayManifestSha256', 'sourceVerified', 'postOverlayVerified')}},
    {'id': 'P-DIFF', 'script': 'probes/make_diffs.py', 'scriptSha256': sha(RT + '/probes/make_diffs.py'), 'receipt': 'receipts/diff-summary.json', 'result': [{k: d[k] for k in ('path', 'added', 'removed')} for d in diffs]},
    {'id': 'P-SEM', 'script': 'probes/probe_overlay_semantics.py', 'scriptSha256': sha(RT + '/probes/probe_overlay_semantics.py'), 'receipt': 'receipts/probe-overlay-semantics.json', 'run': run('probe_overlay_semantics'),
     'result': {'S3': {k: S3.get(k) for k in ('overlayEqualsLaw', 'baseViolations', 'overlayViolations', 'consumerObjectsScanned', 'consumerAdmissionChanged', 'surfaceProjectionAdvisoryLiterals')},
                'A5': A5, 'A6': A6['cases'],
                'R12': {k: R12.get(k) for k in ('defsEqual', 'enumSizes', 'exhaustive', 'removedButLegalUnderPredicate', 'overlayAdmittedButIllegal', 'requestRejectedErrorCodes', 'operationalPairsEqualHostMap', 'd9Union')},
                'R12-producers': {k: {'count': v['count'], 'changed': len(v['changed']), 'overlayRefused': v['overlayRefused']} for k, v in R12['producers'].items()},
                'R12-fixtures': {'n': R12['fixtureScan']['terminationShapedObjects'], 'changedPointers': [c['pointer'] for c in R12['fixtureScan']['admissionChanged']]},
                'ID': {k: ID[k] for k in ('runIdentityStability', 'overlayFilesInRegisteredSchemaDocumentSet')}},
     'notes': 'The native overlayRefused row is a probe artifact: public_termination_for returns None for a notATermination key.'},
    {'id': 'P-PLAN', 'script': 'probes/probe_planning_binding.py', 'scriptSha256': sha(RT + '/probes/probe_planning_binding.py'), 'receipt': 'receipts/probe-planning-binding.json',
     'result': {k: plan[k] for k in ('coverageSourcesStale', 'normativeInputsV5Stale', 'coverageSubjectManifestSha256StillMatchesV5Bytes')}},
]
checks = [dict(run(n), report=('receipts/runs/%s.report.json' % n) if os.path.exists(REC + 'runs/%s.report.json' % n) else None) for n in
          ('check-query-projection.v3', 'check_workflows.v1', 'check-workflow-projection.v3', 'check_implementation_planning', 'check_repository_file_inventory')]
checks_summary = {
    'check-query-projection.v3': '162 checks, 0 failed',
    'check_workflows.v1': '1816 passed, 0 failed',
    'check-workflow-projection.v3': '493 checks, 0 failed',
    'check_implementation_planning': 'EXIT 1 (preserved): ValueError "Planning source changed: query" (stops at first stale binding)',
    'check_repository_file_inventory': 'PASS: 198 unique paths',
}

review = {
    'schema': 'opensip.bounded-root-corrections-review.source37.v1',
    'reviewer': 'Claude, same independent source37 review origin (session 85a08aec-9d22-4ac6-8ec2-c10170e727d7)',
    'standing': 'Bounded read-only review of root corrections overlay db9b7b3f...; not authoring, not whole-design, application, readiness or blind acceptance. The original source37 review stays immutable and CHANGES_REQUIRED.',
    'subjectOverlayManifestSha256': sha(RT + '/subject-manifest.json'), 'baseManifestSha256': MAN and sha(MAN37), 'verifiedOverlay': True,
    'outcome': 'PARTIAL: S37-02, S37-03, R1 and R2 are substantively corrected; A37-05 and A37-07 are addressed with advisories; A37-06 is not closed (RC37-01 SHOULD). Integration requires a planning and pin rebind (RC37-A2).',
    'itemDispositions': dispositions,
    'newShouldFindings': findings, 'newMustFindings': [], 'advisories': advisories,
    'registeredPayloadAndIdentityConsequence': identity,
    'overlayReads': overlay_reads, 'contextReads': context_reads, 'ce3AssessmentRead': ce3,
    'probes': probes, 'focusedChecks': checks, 'focusedChecksSummary': checks_summary,
    'outOfScopeRetained': {
        'S37-01': 'host finalizer: separate coauthor work, NOT closed here',
        'A37-01..04': 'carrier corrections: separate coauthor work, NOT closed here',
        'grades': '30 residual author grades remain PENDING',
        'gates': '32 product qualification gates remain unperformed',
        'recovery': '54 product recovery cases remain not executed',
    },
    'authority': {'finalDesignAccepted': False, 'applicationGranted': False, 'readinessGranted': False, 'gradeGranted': False,
                  'pinsRegenerated': False, 'globalSuitesRun': False, 'rootSourceEdited': False, 'originalReviewEdited': False, 'blindInputsUsed': False},
    'limitations': [
        'Only the three changed owning checkers and the two planning checkers were run, individually. No group runner or global suite was run, and no pins were regenerated. The planning checker stops at its first failure.',
        'Overlay files were read as complete base-to-overlay diffs with changed-region context; the query contract and prototype inventory were read completely. Unchanged regions of large overlay files were not re-read, relying on the retained source37 complete-read record.',
        'The D9 legality predicate in P-SEM is this reviewer\'s transcription (faultCause only on operational-failed, reasonCodes only on indeterminate, operational pair = host fault map). Actual schema outcomes are recorded beside it.',
        'The exhaustive enumeration uses one reasonCode value, minimal required fields per class, and no runId/coverageId/executionId/domainDetail placement variants.',
        'The host-defect case monkeypatches close_run inside the probe process only, to show routing of a non-admission exception; it is not a product fault model.',
        'Producer coverage: native public_termination_for over every registered key/origin and the 24 evaluator fault routes. workflows_model.terminate and integration public_termination were covered only through the maintained checkers.',
        'Reference Python models over synthetic native-admitted inputs; no product implementation, compiler, provider or platform qualification.',
        'check_workflows.v1 reports only counts (1816 passed, 0 failed). Execution of its termination.fault-pairs-equal-host-fault-map control and the 12 new reject vectors is inferred from source reading (module-level check calls at lines 124-133) plus the empty failed list, not from named check ids. check-workflow-projection.v3 and check-query-projection.v3 report the new controls by id.',
    ],
}
json.dump(review, open(RT + '/review.json', 'w'), indent=1, ensure_ascii=False)

L = []
A = L.append
A('# Bounded review of root corrections overlay — source37')
A('')
A('**Outcome: PARTIAL.**')
A('')
A('- **Substantively corrected:** S37-02, S37-03, R1 and R2.')
A('- **Addressed with advisories:** A37-05 and A37-07.')
A('- **Not closed:** A37-06 (RC37-01, SHOULD).')
A('- **Integration:** a planning and pin rebind is required (RC37-A2).')
A('')
A('No final design, application, readiness or grade is granted. My original source37 review stays immutable and CHANGES_REQUIRED.')
A('')
A('## Subject and verification')
A('')
A('- **Overlay manifest:** `subject-manifest.json`, SHA-256 `%s`, matching dispatch.' % review['subjectOverlayManifestSha256'])
A('- **Base:** source37 manifest `%s`.' % review['baseManifestSha256'])
A('- **Overlay rows:** all 12 match their `sha256`/`bytes`, and each base file equals its `beforeSha256`.')
A('- **Disposable copy:** 12,900 source files verified and overlay applied; post-overlay verification shows no mismatch (`receipts/overlay-copy.json`).')
A('- **Probes and checkers:** every run proves no copy file changed.')
A('')
A('## Item dispositions')
for d in dispositions:
    A('')
    A('### %s — %s' % (d['id'], d['disposition']))
    A('')
    A(d['assessment'])
A('')
A('## New SHOULD finding')
for f in findings:
    A('')
    A('### %s (%s) — %s' % (f['id'], f['item'], f['title']))
    A('')
    A('**Owner selectors**')
    A('')
    for s in f['ownerSelectors']:
        A('- %s' % s)
    A('')
    A('**Observed** (`%s`)' % f['reproducer']['receipt'])
    A('')
    for k, v in f['reproducer']['observed'].items():
        A('- `%s`: %s %s/%s, exit %s; subject `%s`; structural closure %s.' % (k, v['result'], v.get('errorCode'), v.get('detail'), v.get('exitCode'), (v.get('subject') or '')[:70], v.get('structuralOwnerClosure')))
    A('')
    A('**Owner routes**')
    A('')
    for k, v in f['reproducer']['ownerRoutes'].items():
        A('- `%s` → %s / %s.' % (k, json.dumps(v['termination']), v['detail']))
    A('')
    A('**Consequence.** %s' % f['consequence'])
    A('')
    A('**Minimal remedy.** %s' % f['minimalRemedy'])
A('')
A('## Advisories')
for a in advisories:
    A('')
    A('### %s (%s) — %s' % (a['id'], a['item'], a['title']))
    A('')
    A(a['detail'])
    A('')
    A('- **Remedy:** %s' % a['remedy'])
    A('- **Disposition:** %s' % a['disposition'])
A('')
A('## Registered payload and retained-identity consequence')
A('')
for k in ('registeredPayloadIdentity', 'retainedIdentities', 'pinsAndPlanning', 'notAssessed'):
    A('- **%s.** %s' % (k, identity[k]))
A('')
A('## Probes')
A('')
for p in probes:
    A('- **%s:** `%s` (sha256 `%s…`), receipt `%s`.' % (p['id'], p['script'], p['scriptSha256'][:16], p['receipt']))
A('')
A('Key probe results:')
A('')
A('- **S3:** overlay equals law = %s. The base violated it for %d non-advisory operations. Consumer admission changes: %s.' % (S3['overlayEqualsLaw'], len(S3['baseViolations']), S3['consumerAdmissionChanged']))
A('- **A5:** %s.' % json.dumps({k: v['result'] for k, v in A5['matrix'].items()}))
A('- **A5, host-invariant route representable:** %s.' % json.dumps(A5['hostInvariantRouteRepresentable']))
A('- **R12 exhaustive:** %s.' % json.dumps(R12['exhaustive']))
A('  - Removed but lawful: %s.' % R12['removedButLegalUnderPredicate'])
A('  - Admitted but unlawful: %s.' % R12['overlayAdmittedButIllegal'])
A('  - Request-rejected error codes: %s.' % json.dumps({k: R12['requestRejectedErrorCodes'][k] for k in ('base', 'overlay', 'equal')}))
A('  - Operational pairs equal host map: %s.' % R12['operationalPairsEqualHostMap'])
A('- **R12 fixtures:** %d termination-shaped objects. Changed only: %s.' % (R12['fixtureScan']['terminationShapedObjects'], [c['pointer'] for c in R12['fixtureScan']['admissionChanged']]))
A('- **Run identity stability:** %s.' % json.dumps({k: v['equal'] for k, v in ID['runIdentityStability'].items()}))
A('- **Planning binding:** v5 stale: %s. Coverage sources stale: %s.' % (plan['normativeInputsV5Stale'], plan['coverageSourcesStale']))
A('')
A('## Focused checks (verified overlay copy; failures preserved)')
A('')
for c in checks:
    A('- `%s`: exit %s, %ss, copy unchanged = %s; %s.' % (c['name'], c['exitCode'], c['seconds'], not c['copyChanged'] and not c['copyExtra'], checks_summary[c['name']]))
A('')
A('## Out of scope and retained')
A('')
for k, v in review['outOfScopeRetained'].items():
    A('- **%s:** %s' % (k, v))
A('')
A('## Reads (exact hashes)')
A('')
A('### Overlay files')
A('')
for r in overlay_reads:
    A('- `%s`: %s → %s. Read: %s.' % (r['path'], r['beforeSha256'][:16], r['sha256'], r['read']))
A('')
A('### Context files')
A('')
for r in context_reads:
    A('- `%s` `%s` (%s): %s.' % (r['path'], r['sha256'], r['source'], r['read']))
A('')
A('### Termination-boundary assessment')
A('')
A('- `%s` `%s`: %s.' % (ce3['path'], ce3['sha256'], ce3['read']))
A('')
A('## Limitations')
A('')
for x in review['limitations']:
    A('- %s' % x)
open(RT + '/review.md', 'w').write('\n'.join(L) + '\n')
print(json.dumps({'outcome': review['outcome'], 'should': len(findings), 'advisories': len(advisories), 'dispositions': len(dispositions),
                  'reviewJsonSha256': sha(RT + '/review.json'), 'reviewMdSha256': sha(RT + '/review.md')}, indent=1))
