"""Assemble review.json and review.md for the independent source37 design review from verified receipts.
Stdlib only. Reads the frozen subject (hashes of completely read files) and this review's own receipts."""
import hashlib, json, os

BASE = '/tmp/opensip-design-corrections/claude-independent-design.v37'
SUBJ = '/tmp/opensip-design-corrections/candidate-subject.v37'
DC = SUBJ + '/docs/coop/design-corrections/'
REC = BASE + '/receipts/'
MANIFEST = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v37.json'
ROOT36 = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/root-independent36-completion-assessment.v1/verification.json'
PKG = '/tmp/opensip-design-corrections/claude-author-package-successor.v14'


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def J(p):
    return json.load(open(p))


READ_COMPLETELY = [
    'docs/v2/contracts/product-v1/README.md',
    'docs/v2/contracts/product-v1/identity-and-evidence.md',
    'docs/v2/contracts/product-v1/security-and-lifecycle.md',
    'docs/v2/contracts/product-v1/native-evidence.md',
    'docs/v2/contracts/product-v1/workflows-and-surfaces.md',
    'docs/v2/contracts/product-v1/admission-and-qualification.md',
    'docs/coop/design-corrections/foundation/enumeration-contract.v1.md',
    'docs/coop/design-corrections/foundation/atom-evaluation-contract.v1.md',
    'docs/coop/design-corrections/foundation/execution-inputs-contract.v1.md',
    'docs/coop/design-corrections/foundation/evaluator-composition-contract.v3.md',
    'docs/coop/design-corrections/foundation/evaluator-fault-contract.v3.md',
    'docs/coop/design-corrections/foundation/target-attribution.schema.v2.json',
    'docs/coop/design-corrections/foundation/provider-target-attribution-return.schema.v2.json',
    'docs/coop/design-corrections/workflows/workflow-projection-contract.v3.md',
    'docs/coop/design-corrections/workflows/query-projection-contract.v3.md',
    'docs/coop/design-corrections/workflows/schemas/evaluator3/graph-query.schema.json',
    'docs/coop/design-corrections/native/fact-batch.schema.v3.json',
    'docs/coop/design-corrections/native/occupancy-companion.schema.v1.json',
    'docs/coop/design-corrections/native/dispatch-binding.schema.v1.json',
    'docs/coop/design-corrections/hydradb-dispositions.proposed.md',
    'docs/coop/design-corrections/inherited-residuals.proposed.md',
    'docs/coop/design-corrections/current-source-map.proposed.md',
    'docs/v2/architecture/14-repository-and-module-layout.md',
    'docs/v2/architecture/implementation-boundaries-and-build-plan.md',
    'docs/v2/architecture/commit-recovery-plan.v1.json',
    'docs/v2/architecture/commit-recovery-readonly.v3.md',
    'docs/v2/architecture/store-instance-lineage.v1.json',
    'docs/v2/architecture/report-asset-binding.v1.json',
    'docs/v2/architecture/attempt-custody.schema.v1.json',
    'docs/v2/architecture/prototype-report-inventory.md',
    'docs/v2/architecture/implementation-normative-inputs.v5.json',
    'docs/v2/architecture/implementation-planning-sources.v1.json',
    'docs/v2/architecture/repository-file-inventory.v1.json',
    'docs/v2/architecture/implementation-coverage.v1.json',
    'docs/coop/design-corrections/security/carrier-format.v3.md',
    'docs/coop/design-corrections/security/carrier-migration.v1.md',
    'docs/coop/design-corrections/security/grant-journal.carrier.v3.sql',
    'docs/coop/design-corrections/security/carrier-highwater.schema.v1.json',
    'docs/coop/design-corrections/security/carrier-dispatch.v3.json',
    'docs/operations/check_implementation_planning.py',
    'docs/operations/check_repository_file_inventory.py',
]
missing = [p for p in READ_COMPLETELY if not os.path.isfile(SUBJ + '/' + p)]
assert not missing, missing
contracts = []
for p in READ_COMPLETELY:
    b = open(SUBJ + '/' + p, 'rb').read()
    contracts.append({'path': p, 'sha256': hashlib.sha256(b).hexdigest(), 'lines': b.count(b'\n'),
                      'coverage': 'complete, sequential chunks of about 120-345 lines; lines longer than the reader limit were printed in pieces'})

PARTIAL = [
    {'path': 'docs/coop/artifacts/d9-exit-contract.v1.14.json', 'read': 'lines 840-939, 2565-2764, plus causeModel, concurrentConditionReducer and codeMaps/deficiencyToReasonCode extracted in full'},
    {'path': 'docs/coop/design-corrections/workflows/schemas/evaluator3/common.schema.json', 'read': '$defs/StepTermination (lines 742-971)'},
    {'path': 'docs/coop/design-corrections/native/native_evidence_model.v2.py', 'read': 'lines 3625-3764 (native_deficiency_d9, stage_authority, run_termination), PRECEDENCE_V2, STAGE_TERMINAL_DEFICIENCY'},
    {'path': 'docs/coop/design-corrections/workflows/query_projection_model.v3.py', 'read': 'lines 1-669 and 1186-1565'},
    {'path': 'docs/coop/design-corrections/foundation/identity-model.v3.py', 'read': 'lines 600-779 (close_run, open_run_closure)'},
    {'path': 'docs/coop/design-corrections/foundation/evaluator_replay_model.v3.py', 'read': 'complete (96 lines)'},
    {'path': 'docs/coop/design-corrections/foundation/evaluator_composition_model.v3.py', 'read': 'lines 60-209 (compose, compare_complete_replay)'},
    {'path': 'docs/coop/design-corrections/foundation/atom_model.v1.py', 'read': 'lines 560-629 (occupancy reconciliation and conflicts)'},
    {'path': 'docs/coop/design-corrections/foundation/check-semantic-replay.v3.py', 'read': 'lines 1-479'},
    {'path': 'docs/coop/design-corrections/workflows/check-query-projection.v3.py', 'read': 'lines 100-189, 236-287, 418-597'},
    {'path': 'docs/coop/design-corrections/workflows/workflows_model.v1.py', 'read': 'lines 190-234 (analysis_termination)'},
    {'path': 'docs/coop/design-corrections/foundation/identity-schemas.v3.json', 'read': 'x-opensip-evaluator-deficiency-registry extracted'},
    {'path': 'docs/coop/design-corrections/security/security_lifecycle_model_v1.py', 'read': 'admit_analysis_seal (lines 1527-1552)'},
    {'path': 'docs/v2/architecture/08-decision-and-readiness-register.md', 'read': 'lines 40-41, 326-330, 380-421, 495, 530'},
    {'path': 'docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json', 'read': 'all 30 items, key fields'},
    {'path': 'docs/coop/design-corrections/correction-crosswalk.proposed.json', 'read': 'all 16 AR items, key fields'},
    {'path': 'docs/coop/design-corrections/qualification-gates.proposed.json', 'read': 'all 32 gate ids, standing and qualified fields'},
]

man = J(REC + 'manifest-verification.json')
arc = J(REC + 'archive-verification.json')
delta = J(REC + 'parent-delta.json')
groups = J(REC + 'reference/groups-report.json')
plan = J(REC + 'planning-checks.json')
pkgv = J(REC + 'package-verification/verification.json')
ddl = J(REC + 'probe-carrier-ddl.json')
sem = J(REC + 'probe-semantic-boundaries.json')
qb = J(REC + 'probe-query-boundary.json')
ca = J(REC + 'probe-cause-attribution.json')


def receipt(rel):
    return {'path': 'receipts/' + rel, 'sha256': sha(REC + rel)}


checkReceipts = [
    {'check': 'subject manifest and frozen source verification', **receipt('manifest-verification.json'), 'result': {k: man.get(k) for k in man if k in ('verified', 'fileCount', 'mismatches', 'missing', 'unlisted', 'manifestSha256')}},
    {'check': 'archive and every member verification plus disposable exact copies', **receipt('archive-verification.json'), 'result': {k: arc.get(k) for k in ('archiveSha256', 'archiveShaMatches', 'manifestFileCount', 'membersMatched', 'mismatches', 'missing', 'extraMembers', 'verified')}},
    {'check': 'parent36 snapshot verification and full delta', **receipt('parent-delta.json'), 'result': delta},
    {'check': 'six pinned reference groups (-I -B, verified copy)', **receipt('reference/groups-report.json'),
     'result': {'passed': groups['passed'], 'copyFilesChangedByCheckers': groups['copyFilesChangedByCheckers'], 'copyExtraFilesAfterRun': groups['copyExtraFilesAfterRun'],
                'rows': [{k: r[k] for k in ('name', 'script', 'scriptSha256', 'exitCode', 'seconds', 'stdoutSha256', 'stdoutTail')} for r in groups['rows']]}},
    {'check': 'current planning checks', **receipt('planning-checks.json'),
     'result': {'check_implementation_planning': {k: plan['check_implementation_planning'][k] for k in ('exitCode', 'stdout')},
                'check_repository_file_inventory': {k: plan['check_repository_file_inventory'][k] for k in ('exitCode', 'stdout')},
                'counts': plan['counts'], 'graphQuerySchemaLines': plan['graphQuerySchemaLines']}},
    {'check': 'nonblind author package v14 verifier on a second verified exact copy', **receipt('package-verification/verification.json'), 'result': pkgv},
]
for n in ('probe_semantic_boundaries', 'probe_query_boundary', 'probe_cause_attribution'):
    r = J(REC + 'probes/' + n + '.run.json')
    checkReceipts.append({'check': 'independent probe run ' + n, **receipt('probes/' + n + '.run.json'),
                          'result': {k: r[k] for k in ('probeSha256', 'exitCode', 'seconds', 'copyFileCount', 'copyChanged', 'copyExtra')}})

# ------------------------------------------------------------------------------------------ issues
cause = sem['P-CAUSE']
newShouldIssues = [
    {
        'id': 'S37-01',
        'title': 'Whole-Run primary/secondary cause order and coverageId attribution have no owner; the host termination is not a function of the sealed Run',
        'severity': 'SHOULD',
        'ownerSelectors': [
            'docs/v2/contracts/product-v1/native-evidence.md §10 "Native stage selection, and where it stops" lines 2946-2963 ("This section does not define how requirement, proof-cause, import or verdict outcomes are ordered in that reduction")',
            'docs/coop/artifacts/d9-exit-contract.v1.14.json#/concurrentConditionReducer (primary=deficiencies[0] in pre-reduction host input order) and #/causeModel/codeDerivation',
            'docs/coop/design-corrections/workflows/schemas/evaluator3/common.schema.json#/$defs/StepTermination (reasonCodes x-opensip-order sequence; coverageId optional, no selection law)',
            'docs/coop/design-corrections/workflows/workflow-projection-contract.v3.md line 138 (EVALUATION.WORK_BUDGET_EXHAUSTED: sealed Run "may reuse" budget-exhausted)',
            'docs/coop/design-corrections/foundation/evaluator-composition-contract.v3.md §5 / evaluator_composition_model.v3.py compose(): ruleResults[].deficiencies and executionDeficiencies retained only as canonical sets',
            'docs/v2/contracts/product-v1/workflows-and-surfaces.md §9 D9 goldens and typed detail (host finalizer owner, no ordering law)',
        ],
        'consequence': ('Two conforming host finalizers can emit different reasonCodes[0] (the remedy class a caller acts on first, D9 TO-7), different secondary order, '
                        'and a different or absent coverageId for byte-identical sealed Run evidence. The retained proof keeps deficiencies only as canonical sets, so no verifier can '
                        're-derive which termination was lawful, D9 goldens cannot pin it, and query/command parity of the enclosing termination is not reproducible across hosts. '
                        'Class and exit (indeterminate/3) and all identities are unaffected, hence SHOULD rather than MUST.'),
        'reproducer': {
            'receipts': ['receipts/probe-cause-attribution.json', 'receipts/probe-semantic-boundaries.json#P-CAUSE'],
            'actualRun': cause['run'],
            'A': 'Actual closed indeterminate Run %s carries %d deficient Coverage records (both resolution-incomplete); StepTermination with either coverageId, or none, is schema-valid (%s). Retained deficiency order is the canonical set order (%s). Native cause coverage-unknown has no D9 or native-bridge route.' % (
                cause['run']['runId'], ca['A-coverageId-candidates']['deficientCoverageRecords'], ca['A-coverageId-candidates']['allValid'], cause['retainedOrderIsCanonicalSet']),
            'B': 'Actual native run_termination over a clean budget-exhausted stage terminal and a resolution-incomplete entry returns stage primary %s while the typed detail names %s, so a coverageId naming that record carries a deficiency whose route differs from reasonCodes[0].' % (
                ca['B-stage-vs-entry'].get('stagePrimaryCode'), ca['B-stage-vs-entry'].get('entryTypedDetailDeficiency')),
            'C': 'D9 reducer applied to the same three concurrent conditions from different owners (requirement sufficiency required-relation-missing, native stage terminal budget-exhausted, verdict composition verdict-indeterminate) in the six lawful pre-reduction orders gives %d distinct schema-valid reasonCodes sequences and primary codes %s.' % (
                ca['C-reducer-orders']['distinctCodeSequences'], ca['C-reducer-orders']['distinctPrimaryCodes']),
        },
        'minimalRemedy': ('In one owner (the host finalizer section of workflows-and-surfaces §9, or a D9 successor row), define a total pre-reduction order across condition sources as a function of retained Run content '
                          '(for example native stage selections by §10 precedence, then requirement sufficiency, then required execution/import obligations, then verdict-indeterminate last, canonical tie-break); '
                          'make the evaluator-only cause bridge explicit (coverage-unknown, required-cell-unsatisfied, incomplete-inventory and import causes route through verdict-indeterminate; replace "may reuse" for work-budget-exhausted with MUST or MUST NOT); '
                          'and select coverageId deterministically (for example the canonically least coverage2 whose entry.deficiency equals the primary, omitted when the primary has no entry carrier). Add retained goldens for A, B and C.'),
        'relatedRows': ['AR-16', 'DR-007', 'DR-011-R08', 'FW-06', 'FW-08'],
    },
    {
        'id': 'S37-02',
        'title': 'Prototype report inventory selects executable "registered external report hooks" in a worker lane, contradicting the selected product boundary and without any owner',
        'severity': 'SHOULD',
        'ownerSelectors': [
            'docs/v2/architecture/prototype-report-inventory.md:37 (R02 "Registered external report hooks execute only in the supervised isolated worker lane; there is no in-host fallback")',
            'docs/v2/architecture/prototype-report-inventory.md:179 (R24 External tools "isolated registered report hooks")',
            'docs/v2/contracts/product-v1/admission-and-qualification.md §5 items 1, 3, 4 and 5 (lines 341-345: one first-party registry; only the host owns rendering; no untrusted native/WASM admission and no sandbox claim; imperative contributions/project hooks not admitted)',
            'docs/v2/architecture/implementation-coverage.v1.json groups.reportFeatures R02/R24 (owners apps/report/src/report-view.ts and crates/reporting/src/projection.rs only; no worker-lane owner, schema, D9 route or gate)',
        ],
        'consequence': ('The planning inventory, which chapter 14 and the file inventory ask reviewers to accept as R01-R24 dispositions, directs implementers toward an executable external rendering-hook lane '
                        'that the product boundary excludes. Accepting R02/R24 as written would silently widen scope and the trusted-code account (TCB-SCOPE-01) without admission contract, isolation claim, failure route or qualification gate; '
                        'rejecting it leaves no stated replacement for external-tool presentation.'),
        'reproducer': 'Text comparison of the cited selectors; searching all non-review snapshot docs for "report hook" or "external report" finds only prototype-report-inventory.md lines 37 and 179.',
        'minimalRemedy': 'Replace the hook language in R02 and R24 with versioned host-approved data projections only (no executable report hooks), or route an explicit reviewed scope change through admission §5 with an owner, admission schema, D9 routes and gate.',
        'relatedRows': ['DR-010', 'DR-011-R16', 'DR-205', 'AR-15'],
    },
    {
        'id': 'S37-03',
        'title': 'GraphQueryResponseV1 admits advisory=true for non-advisory non-graph operations although the contract and schema description say advisory is true exactly for four operations',
        'severity': 'SHOULD',
        'ownerSelectors': [
            'docs/coop/design-corrections/workflows/schemas/evaluator3/graph-query.schema.json#/$defs/GraphQueryResponseV1/allOf[4] (AdvisoryOperation then advisory const true; no else branch), lines 1164-1190',
            'graph-query.schema.json#/$defs/GraphQueryResponseContext/properties/advisory (type boolean), lines 947-950, versus the schema description at line 5 ("false for graph.* and the remaining non-advisory operations")',
            'docs/v2/contracts/product-v1/workflows-and-surfaces.md:1050-1066 ("advisory is true exactly for comparison.diff, candidate.list, inspection.show and review.brief"; query-response is the complete owner-admitted GraphQueryResponseV1)',
        ],
        'consequence': ('A finding.list or run.show response labelled advisory passes owner schema admission, and so does the query-response parity field built from it. Renderers and agent consumers '
                        'that rely on admission for the Control versus Map authority distinction can present authoritative findings as advisory. The half-enforced "exactly" law is not caught by the existing controls, which only test the graph-true and advisory-diff-true branches.'),
        'reproducer': {'receipt': 'receipts/probe-query-boundary.json#Q4', 'results': qb['Q4']},
        'minimalRemedy': 'Add else: advisory const false for operations outside AdvisoryOperation (a schema successor with re-registration if these bytes are registered), plus negative controls for run.show and finding.list.',
        'relatedRows': ['AR-13', 'HYDRA-3'],
    },
]
newMustIssues = []

advisories = [
    {'id': 'A37-01', 'title': 'carrierFormat 3 DDL grammar CHECKs verify only the first character after the prefix',
     'detail': 'GLOB patterns "op-[0-9a-f]*", "run3:[0-9a-f]*" and "[0-9a-f]*" with a length check admit uppercase or non-hex tails; body_sha256/prev_sha256 and attempt_custody execution_id have length-only checks. Probe admitted op-a+Z*31, run3:c+Q*63, non-hex body_sha256, project_key_digest and migration_op_ref, and a non-hex execution_id. The inherited carrierFormat 2 DDL has the same pattern. carrier-format.v3.md:158 states the grammar as a preserved law.',
     'selectors': ['docs/coop/design-corrections/security/grant-journal.carrier.v3.sql:21-22,30-32,48-49,56-60', 'docs/v2/architecture/attempt-custody.schema.v1.json#/proposedPrivateDDL', 'docs/coop/design-corrections/security/carrier-format.v3.md:158'],
     'receipt': 'receipts/probe-carrier-ddl.json', 'disposition': 'ROUTE-TO-IMPLEMENTATION-DDL: add a "NOT GLOB \'*[^0-9a-f]*\'" tail test or state that host record admission alone owns grammar and the DDL is defence in depth only.'},
    {'id': 'A37-02', 'title': 'first_generation law is not DDL-enforced in the {A,B} footprint',
     'detail': 'With the v3 objects present and no carrier_format row, an append at grantGeneration 1 is admitted, and the row is then published with first_generation=5 while v3 holds generation 1. The carrier-migration {A,B} resume procedure verifies definitions, not rows.',
     'selectors': ['docs/coop/design-corrections/security/grant-journal.carrier.v3.sql', 'docs/coop/design-corrections/security/carrier-migration.v1.md:159', 'docs/coop/design-corrections/security/carrier-dispatch.v3.json:322'],
     'receipt': 'receipts/probe-carrier-ddl.json', 'disposition': 'ROUTE-TO-CARRIER-OWNER: at act C require grant_journal_v3 to be empty, or add a publication-time check that no v3 row precedes first_generation.'},
    {'id': 'A37-03', 'title': 'MIGRATION.CORRUPT carries a projectKeyDigest mismatch that may be a swapped carrier',
     'detail': 'carrier-dispatch.v3.json:212 and carrier-format.v3.md:274 route a published carrierFormat 3 projectKeyDigest mismatch to MIGRATION.CORRUPT (LEDGER.CORRUPT). S12:1306 routes a foreign or swapped carrier on read-only recovery to EXTENSION.ADMISSION_REJECTED/RECOVERY.REFUSED, and S12:1308 explicitly keeps MIGRATION.CORRUPT to one remedy. Partial-object and definition failures of the migration itself are coherent uses.',
     'selectors': ['docs/coop/design-corrections/security/carrier-dispatch.v3.json:212', 'docs/coop/design-corrections/security/carrier-format.v3.md:274', 'docs/v2/contracts/product-v1/security-and-lifecycle.md:1300,1306,1308'],
     'disposition': 'ROUTE-TO-SECURITY-OWNER: state whether a digest mismatch is migration corruption or foreign binding on each path.'},
    {'id': 'A37-04', 'title': 'F46 unknown-carrier-incompatible and F51 split-brain-custody-condition have no public projection row',
     'detail': 'The build plan and commit-recovery plan define these conclusions, but neither S12 nor commit-recovery-readonly.v3 gives a class, exit or code for them.',
     'selectors': ['docs/v2/architecture/implementation-boundaries-and-build-plan.md:578,583', 'docs/v2/architecture/commit-recovery-plan.v1.json:562,612', 'docs/v2/contracts/product-v1/security-and-lifecycle.md §S12', 'docs/v2/architecture/commit-recovery-readonly.v3.md §1'],
     'disposition': 'ROUTE-TO-SECURITY-OWNER: add the two rows before F46/F51 implementation.'},
    {'id': 'A37-05', 'title': 'Unknown graph availability observation value is silently ignored',
     'detail': 'The reference treats host availability "not-a-state" like an omitted observation (ADMIT; close_run still decides). Query §7 names only purged/expired/corrupt/unavailable, retained/partial and omitted; "missing" is also accepted as a direct host report.',
     'selectors': ['docs/coop/design-corrections/workflows/query-projection-contract.v3.md:160', 'docs/coop/design-corrections/workflows/query_projection_model.v3.py:1425-1450'],
     'receipt': 'receipts/probe-query-boundary.json#Q3', 'disposition': 'ROUTE-TO-QUERY-OWNER: state that an out-of-vocabulary observation is a host invariant violation, or that it is ignored.'},
    {'id': 'A37-06', 'title': 'Complete-replay disagreement on the graph query path collapses into the corrupt-retained-bytes row',
     'detail': 'Fully reminted false-result Runs are refused by the query with HOST.IO_FAILURE/evidence.corrupt, subject EVALUATOR_COMPLETE_PROOF_REPLAY. Identity §4 (lines 1465-1467) keeps complete replay disagreement a distinct typed boundary observation, but query §7 has no row for it.',
     'selectors': ['docs/coop/design-corrections/workflows/query-projection-contract.v3.md:162-177', 'docs/v2/contracts/product-v1/identity-and-evidence.md:1465-1467'],
     'receipt': 'receipts/probe-semantic-boundaries.json#P-REMINT', 'disposition': 'ROUTE-TO-QUERY-OWNER: add an explicit row; evidence.corrupt is acceptable if chosen deliberately.'},
    {'id': 'A37-07', 'title': 'Stale standing prose after the v5 normative-input binding',
     'detail': 'The build plan still says the planning checker verifies candidate25 (lines 10, 19, 1041, 1045, 1085), but the executed checker binds implementation-normative-inputs.v5 (29 files, all hashes ok). carrier-format.v3.md:4 and commit-recovery-readonly.v3.md:5 say "authored against Source25"; store-instance-lineage.v1.json:469,506 cites an "F00-F37" matrix while the plan has F00-F53.',
     'selectors': ['docs/v2/architecture/implementation-boundaries-and-build-plan.md:10,19,1041,1045,1085', 'docs/coop/design-corrections/security/carrier-format.v3.md:4', 'docs/v2/architecture/commit-recovery-readonly.v3.md:5', 'docs/v2/architecture/store-instance-lineage.v1.json:469,506'],
     'disposition': 'EDITORIAL: add current-standing notes in the next successor. No semantic effect found.'},
    {'id': 'A37-08', 'title': 'Registered native schema annotation still states a superseded three-code list',
     'detail': 'The native §10 supersession law (lines 2933-2944) is coherent: editing the annotation would change payloadSchemaDigest and every coverage2 identity. Readers of the schema alone still see the stale list.',
     'selectors': ['docs/v2/contracts/product-v1/native-evidence.md:2933-2944', 'native-evidence.schemas.v2.json#/x-opensip-deficiency-cause-registry/perRequirementConsumerBoundary/threeDistinctThingsNotToConflate/publicD9Termination'],
     'disposition': 'ACCEPTED-AS-DESIGNED; fold the correction into the next registered schema successor.'},
]

# ------------------------------------------------------------------------------------------ probes
probes = [
    {'id': 'P-CROSS', 'claim': 'cross-unit claim: evaluator proof and public graph query project the same retained references facts per subject across two native universes',
     'script': 'probes/probe_semantic_boundaries.py', 'scriptSha256': sha(BASE + '/probes/probe_semantic_boundaries.py'), 'receipt': 'receipts/probe-semantic-boundaries.json#P-CROSS',
     'result': {'passed': sem['P-CROSS']['passed'], 'runId': sem['P-CROSS']['runId'], 'mismatches': sem['P-CROSS']['mismatches'], 'rows': len(sem['P-CROSS']['rows']),
                'crossUniverseEdges': any(r.get('cross_universe_edge') for r in sem['P-CROSS']['rows'])},
     'discriminating': 'yes: a per-subject fact-set equality in both universes would fail under any union, universe conflation or occupancy divergence between atom and query'},
    {'id': 'P-TARGET', 'claim': 'target/proof boundary: target-side predicate values versus the incoming graph result; an empty or complete traversal is never proof',
     'script': 'probes/probe_semantic_boundaries.py', 'receipt': 'receipts/probe-semantic-boundaries.json#P-TARGET-complete,P-TARGET-incomplete',
     'result': {'complete': sem['P-TARGET-complete']['passed'], 'incomplete': sem['P-TARGET-incomplete']['passed'],
                'incompleteRows': [{k: r.get(k) for k in ('nativeSubjectId', 'predicateValue', 'queryFactIds', 'queryTraversal', 'queryLimitationKinds')} for r in sem['P-TARGET-incomplete']['rows']]},
     'discriminating': 'yes: foo is indeterminate in proof while the query returns zero rows with traversal complete, and must disclose incoming-search-incomplete/resolution-not-attempted'},
    {'id': 'P-QUERY', 'claim': 'retained graph query boundary: schema-first endpoint admission, package tuple identity, availability mapping, response parity, cursor binding, visit caps',
     'script': 'probes/probe_query_boundary.py', 'scriptSha256': sha(BASE + '/probes/probe_query_boundary.py'), 'receipt': 'receipts/probe-query-boundary.json',
     'result': {'Q1-schemaFirst': qb['Q1']['passed'], 'Q2-ambiguousReachable': qb['Q2'].get('ambiguousReachable'), 'Q3-availabilityMapping': qb['Q3']['mappingPassed'],
                'Q3-unknownState': qb['Q3']['unknownStateObservation'], 'Q4-parity': qb['Q4'],
                'Q5': {k: (v.get('result'), v.get('detail')) if isinstance(v, dict) else v for k, v in qb['Q5'].items()},
                'Q6': {k: (v.get('result'), v.get('traversal')) for k, v in qb['Q6'].items()}},
     'discriminating': 'yes for Q1 (malformed package endpoint with no Run and with a purged observation), Q3 and Q4; Q4 found S37-03'},
    {'id': 'P-REMINT', 'claim': 'fully reminted false-result graphs (witness blobs, proof, evidence, seal, Run) pass structural owner admission but fail complete replay and every public boundary',
     'script': 'probes/probe_semantic_boundaries.py', 'receipt': 'receipts/probe-semantic-boundaries.json#P-REMINT',
     'result': [{k: r.get(k) for k in ('label', 'original', 'predicatesFlipped', 'structuralOwnerClosure', 'completeReplay', 'close_run', 'publicGraphQuery', 'discriminates')} for r in sem['P-REMINT']],
     'discriminating': 'yes: all three mutants (fail to pass, indeterminate laundered to false, execution deficiency erased) get new valid identities and ADMIT at open_run_closure; close_run and execute_graph_query refuse. These differ from the checker\'s same-count metadata mutants. The SEAL adapter delegates to close_run by source reading and was not executed.'},
    {'id': 'P-CAUSE', 'claim': 'whole-Run cause order and coverageId attribution',
     'script': 'probes/probe_semantic_boundaries.py + probes/probe_cause_attribution.py', 'scriptSha256': sha(BASE + '/probes/probe_cause_attribution.py'),
     'receipt': 'receipts/probe-semantic-boundaries.json#P-CAUSE, receipts/probe-cause-attribution.json',
     'result': {'actualRun': cause['run'], 'deficientCoverageRecords': cause['deficientCoverageRecords'], 'causesWithoutAnyOwnerRoute': cause['causesWithoutAnyOwnerRoute'],
                'A': ca['A-coverageId-candidates'], 'B': {k: ca['B-stage-vs-entry'].get(k) for k in ('stagePrimaryCode', 'entryTypedDetailDeficiency', 'differs')},
                'C': {k: ca['C-reducer-orders'][k] for k in ('distinctPrimaryCodes', 'distinctCodeSequences', 'allValid')},
                'workflowsModelAnalysisTermination': cause['workflowsModelAnalysisTermination']},
     'discriminating': 'yes: several schema-valid terminations for one sealed Run; found S37-01. Part C drives the D9 reducer text over constructed condition lists because no product host finalizer exists; A and B use actual owners'},
    {'id': 'P-CARRIER', 'claim': 'carrierFormat 3 DDL enforcement of its stated grammar and first_generation law',
     'script': 'probes/probe_carrier_ddl.py', 'scriptSha256': sha(BASE + '/probes/probe_carrier_ddl.py'), 'receipt': 'receipts/probe-carrier-ddl.json',
     'result': {k: v for k, v in ddl.items() if k != 'v2_columns'}, 'discriminating': 'yes; found A37-01 and A37-02'},
]

# ------------------------------------------------------------------------------------------ dispositions
FLAGS = {'appliedByThisReview': False, 'finalApplicationOutcomeGranted': False}
root36 = {r['id']: r for r in J(ROOT36)['rows'] if r.get('map') == 'fDispositions'}
fDispositions = []
for i in range(1, 15):
    fid = 'F-%02d' % i
    fDispositions.append({'id': fid, 'priorRootStanding': root36[fid]['disposition'],
                          'disposition': 'CARRIED-NOT-REGRADED',
                          'assessment': 'The identifier and prior root standing are recorded from root-independent36-completion-assessment.v1. The F row content is defined in earlier review records outside this snapshot; this review did not re-derive it, and source36 standing is not inherited as source37 acceptance. No source37 delta file is among its owners in that record.',
                          **FLAGS})

residuals = J(DC + 'evaluation-residual-dispositions.proposed.json')['items']
TCB = ['RES-EP13-02', 'RES-EP13-04', 'RES-EP13-12', 'RES-EP13-13', 'RES-EP13-16', 'RES-EP13-18',
       'IR-EP13-NB-01', 'IR-EP13-NB-03', 'IR-EP13-NB-04', 'AX6', 'AX9', 'MD5', 'RX2c']
NOTES = {
    'RES-EP13-01': 'Checked against evaluator3 execution-inputs and composition: Plan/derivation joins are recomputed in replay (evaluator_replay_model.v3.replay).',
    'RES-EP13-07': 'P-REMINT confirms the seal binds proof, evidence, verdict and Run: every reminted identity is new and complete replay refuses it.',
    'RES-EP13-09': 'Provenance and correctness stay separate: P-REMINT mutants have valid provenance-style identities and are refused only by replay.',
    'RES-EP13-10': 'Candidate self-counters are not admission: this review ran pinned groups and independent probes rather than relying on author counts.',
    'RES-EP13-13': 'This review\'s own probes deep-copy inputs before mutation (fixture isolation only; no sandbox claim).',
    'RES-EP13-19': 'Substantive semantic review was performed and found S37-01..03; pins and passing counts were not treated as acceptance.',
    'IR-EP13-NB-02': 'No name or punctuation scan decides scope in the source37 query/evaluator owners read.',
    'IR-EP13-NB-05': 'Contradictory prose still needs substantive review; S37-02 is an example found by reading, not by any checker.',
}
evaluationResidualDispositions = []
for it in residuals:
    rid = it['id']
    row = {'id': rid, 'proposedDisposition': it.get('proposedDisposition'), 'authorGrade': 'PENDING', 'reviewStatusRecorded': it.get('reviewStatus'),
           'disposition': 'ASSESSED-CONSISTENT-GRADE-PENDING',
           'assessment': 'The proposed prospective replacement is consistent with the source37 contracts read (identity §4 complete replay at close_run; admission §5 boundary). The historical limitation or observation is preserved unchanged, and no historical guard is claimed repaired. ' + NOTES.get(rid, ''),
           'sharedDependency': 'TCB-SCOPE-01' if rid in TCB else None, 'residualRetained': True, **FLAGS}
    evaluationResidualDispositions.append(row)
assert len(evaluationResidualDispositions) == 30

AR_NOTES = {
    'AR-01': ('NO-NEW-ISSUE', 'Numeric/schema admission read completely; probes observed exact schema admission on query requests and StepTermination.'),
    'AR-02': ('NO-NEW-ISSUE', 'Custody, semantic correctness and qualification remain separate; all 32 gates are DESIGN-CONTRACT-PENDING-REVIEW with qualified=false.'),
    'AR-03': ('NO-NEW-ISSUE', 'Discovery joins verified by the security reference group only.'),
    'AR-04': ('NO-NEW-ISSUE', 'Trust time read; no probe.'),
    'AR-05': ('NO-NEW-ISSUE', 'Root chain/revocation read; no probe.'),
    'AR-06': ('NO-NEW-ISSUE', 'Platform vocabulary joins pass in the security group; the carrier DDL platform enum matches the four machine ids.'),
    'AR-07': ('NO-NEW-ISSUE', 'Native §§3/5/9 read; native group 377/377.'),
    'AR-08': ('NO-NEW-ISSUE', 'Invocation and repair read; per-requirement repair disclosure stays a DeficiencyV2 member (native §10, lines 2965 onward).'),
    'AR-09': ('ADVISORY-ONLY', 'The close_run complete-replay boundary is confirmed by P-REMINT; see A37-06 for the query route of replay disagreement.'),
    'AR-10': ('NO-NEW-ISSUE', 'Baseline/comparison read; comparison-knowledge group passed.'),
    'AR-11': ('NO-NEW-ISSUE', 'Imported evidence wrapper and history/runtime limits read; no independent import probe.'),
    'AR-12': ('NO-NEW-ISSUE', 'Native §4 sufficiency read; dependency same-kind totality assessed by reading and the atoms group.'),
    'AR-13': ('CHANGES-REQUIRED-ROUTED', 'Workflow output parity: S37-03.'),
    'AR-14': ('ADVISORY-ONLY', 'Stage transition and lease model consistent with store lineage; A37-03 on MIGRATION.CORRUPT use.'),
    'AR-15': ('CHANGES-REQUIRED-ROUTED', 'The index/D-372 application is coherent; the planning layer contradicts the admission boundary on report hooks (S37-02).'),
    'AR-16': ('CHANGES-REQUIRED-ROUTED', 'The D9 native route is corrected and total, but the whole-Run reduction order and coverageId are unowned: S37-01.'),
}
cross = J(DC + 'correction-crosswalk.proposed.json')['items']
arDispositions = []
for it in cross:
    d, note = AR_NOTES[it['id']]
    arDispositions.append({'id': it['id'], 'contract': it['contract'], 'selector': it['selector'], 'statusRecorded': it['status'],
                           'disposition': d, 'assessment': note, **FLAGS})
assert len(arDispositions) == 16

cov = J(SUBJ + '/docs/v2/architecture/implementation-coverage.v1.json')
FW_NOTES = {'FW-06': 'S37-01: the typed termination projection is not yet a deterministic function of the sealed Run.',
            'FW-08': 'A37-05 and A37-06 on the query unavailable/operational-fault distinction.',
            'FW-04': 'Runtime/test/history stay non-Coverage per workflows §4 (read); no probe.',
            'FW-13': 'S37-03: typed registry/schema admission gap for the advisory cross-join.'}
fwDispositions = []
for r in cov['groups']['fallowConstraints']:
    fwDispositions.append({'id': r['id'], 'owners': r['owners'], 'milestone': r['milestone'], 'verificationStanding': r['verification']['standing'],
                           'disposition': 'OWNER-ROUTING-ASSESSED-NOT-EXECUTED',
                           'assessment': 'The source row and owner module match the current-source-map row and the chapter 14 inventory; implementation not executed. ' + FW_NOTES.get(r['id'], ''), **FLAGS})
assert len(fwDispositions) == 15

DR_NOTES = {
    'DR-003': 'G19 and native carrier custody remain release obligations; the 54 recovery cases are not executed; A37-01, A37-02 and A37-04.',
    'DR-005': 'Executable custody reference groups pass; native product carrier qualification is still required.',
    'DR-007': 'S37-01: the cause reduction order and coverageId join are not closed.',
    'DR-010': 'S37-02: report hooks conflict with bounded first-party scope.',
    'DR-011': 'Individual dispositions exist; the blind implementer litmus follows final integration and was not performed here.',
    'DR-011-R08': 'S37-01 affects the closed host-owned outcome for concurrent deficiencies.',
    'DR-011-R10': 'Remains OPEN: this nonblind review cannot close the fresh blind implementer litmus.',
    'DR-011-R11': 'Real platform durability is still unmeasured; carrier advisories A37-01..04.',
    'DR-011-R12': 'Depends on TCB-SCOPE-01 (assessed once below).',
    'DR-011-R16': 'S37-02.',
}
ids = ['DR-%03d' % i for i in range(1, 12)] + ['DR-011-R%02d' % i for i in range(1, 17)]
inheritedResidualDispositions = [{'id': x, 'disposition': 'CONDITION-1-OBLIGATION-RETAINED-ASSESSED',
                                  'assessment': 'The proposed successor routing in inherited-residuals.proposed.md is consistent with the source37 contracts read; the original custody and standing are preserved. ' + DR_NOTES.get(x, ''),
                                  **FLAGS} for x in ids]
assert len(inheritedResidualDispositions) == 27

scopedReviewOwnerDispositions = [{'id': 'DR-%d' % i, 'disposition': 'ROUTING-ASSESSED-ONLY-NOT-APPLIED',
                                  'assessment': 'Register 08 records ACCEPTED 2026-08-13 for the earlier scope (line %d) and OPEN for full-product integration (line 412). DR-201..205 remain the condition-3 owners (line 391). This review is an input to that integrated review and is not applied.' % (325 + i - 200)
                                  + (' Related: S37-01.' if i == 201 else ' Related: S37-02.' if i == 205 else ' Related: A37-01..04.' if i == 202 else ''),
                                  **FLAGS} for i in range(201, 206)]

allRows = fDispositions + evaluationResidualDispositions + arDispositions + fwDispositions + inheritedResidualDispositions + scopedReviewOwnerDispositions
assert len(allRows) == 107 and all(r['appliedByThisReview'] is False and r['finalApplicationOutcomeGranted'] is False for r in allRows)
assert all(r['authorGrade'] == 'PENDING' for r in evaluationResidualDispositions)

tcb = {
    'id': 'TCB-SCOPE-01', 'assessedOnce': True, 'dependentResidualIds': TCB,
    'assumption': 'Selected authenticated in-process host/evaluator code is trusted; adversarial code sharing that process is outside this product threat model. Untrusted inputs are inert typed data and provider process boundaries still require real qualification.',
    'assessment': [
        'COHERENT AS A SCOPE SELECTION, NOT A CONTAINMENT CLAIM. It agrees with admission §5 items 3-5: only the host constructs findings, verdicts and rendering; no untrusted native/WASM admission; no sandbox claim; no imperative contributions. It also agrees with identity §4, where open_run_closure grants no correctness.',
        'What it relies on is visible and was probed. Fully reminted false-result graphs with valid new identities pass structural admission and are refused only by complete replay (P-REMINT). Outside the trusted process, correctness therefore rests on the replaying evaluator code and retained inputs, not on identity checks. If that code is adversarial, nothing in the design detects it, which is exactly what the assumption excludes.',
        'One planning text is inconsistent with it. S37-02 selects executable external report hooks in a worker lane, which would put non-host rendering code outside this account. Resolving S37-02 as recommended keeps the assumption intact.',
        'The assumption rests on an exact authenticated closure/TCB inventory and on provider process boundaries (DR-G29/G30 and related gates). All 32 gates remain unperformed, so it is design-coherent and unqualified.',
        'Consequence retained: rejecting or changing it reopens all thirteen dependent accounts together. It does not repair the historical attacks or establish containment. No grade is assigned, all thirteen author grades stay PENDING, and final application adjudication is still required and is not granted here.',
    ],
    'standing': 'ASSESSED-COHERENT-UNQUALIFIED; final application adjudication required; not granted',
}

pkg_assessment = {
    'package': PKG, 'manifestSha256Expected': 'a4704b3a...', 'artifactManifestSha256': sha(PKG + '/artifact-manifest.json'),
    'verifier': 'verify-package.py --source <second verified exact copy> --out receipts/package-verification',
    'result': pkgv,
    'independentObservations': [
        'On a verified exact copy of source37 (12900 source files, 329 package files verified), every verifier group passed. There are seven valid synthetic Runs (checkpoint3 1, normalized-examples6 4, rust-selection-examples1 2), each owner ADMIT and semantic ADMIT. The three reminted semantic negative controls (severity, unrelated-scope, collapsed-deficiencies) are owner ADMIT and complete-replay REFUSE with EVALUATOR_COMPLETE_PROOF_REPLAY. Of the three binding controls, two are lawful ADMIT and ts-invalid-default-entry is REFUSE with EVALUATOR_ENUMERATION_JOIN:ENUMERATION_BINDING_PROGRAM_ENTRY. There are seven query checks. The group exitCode 1 for semantic-controls1 and binding-controls is the expected refusal signal, with passed=true.',
        'semantic-controls1/construction-provenance.json: "AUTHOR-assisted construction. Not independent reconstruction, not blind acceptance, not product qualification". It was built against the source33 kit with package-v10 author helpers and transported by check-export.v4.py. This mixed construction provenance is preserved and is not upgraded by passing on source37.',
        'The A9/A10 limitations named by the charter are preserved as stated there. The literal tokens "A9"/"A10"/"A-9"/"A-10" do not appear in the current top-level v14 package files searched (historical subdirectories excluded), so their wording was not re-read here.',
        'This review\'s own discriminating mutants (P-REMINT, P-CAUSE, P-QUERY) were designed independently of the package controls and do not reuse its stores.',
    ],
    'standing': 'NONBLIND AUTHOR PACKAGE VERIFIED AS REFERENCE EVIDENCE; no blind reconstruction claimed; no grade or acceptance conferred',
}

assessments = {
    'wholeRunCauseOrderAndCoverageId': 'CHANGES REQUIRED (S37-01). Native §10 now correctly delegates the Run termination to the host finalizer and D9 reducer, but no owner fixes the pre-reduction order or coverageId; a stage-implied primary can differ from the entry detail named by coverageId (probe B).',
    'nativeDeficiencyToD9Routing': 'ACCEPTABLE. The nine-row route equals the D9 map (five self-mapped members; the four bridge members go to verdict-indeterminate, i.e. VERDICT.INDETERMINATE). The source37 correction of LANGUAGE_TIER/CONFIDENCE_FLOOR/REQUIRED_RELATION to their COVERAGE.* codes agrees with D9 v1.14. The native group passes, including route drift.',
    'strictPackageEndpointAdmission': 'ACCEPTABLE. Schema-first QUERY.PARAMS_MALFORMED precedes Run presence, availability observation and vertex lookup; same-name packages with distinct manifests are distinct vertices; an unknown manifest is ENDPOINT_UNKNOWN; ENDPOINT_AMBIGUOUS is unreachable from one retained Run (P-QUERY Q1/Q2).',
    'graphEvidenceAvailabilityMapping': 'ACCEPTABLE with advisories A37-05/06. purged, expired, corrupt and unavailable route to HOST.IO_FAILURE exit 4 with evidence.purged/expired/corrupt/missing; retained, partial and omitted neither refuse nor grant; corrupt bytes still refuse under a retained or partial observation (Q3).',
    'dependencySameKindTotality': 'ASSESSED BY READING AND REFERENCE GROUP ONLY. The atom contract\'s evaluate-with-and-without-gap-positions law, required-relation-missing for removed positions, vacuous empty owed set and whole-source different-kind are coherent with composition §9. The atoms group passed. No independent probe.',
    'partialEvidenceCitationsBooleanScopeUnion': 'ACCEPTABLE. Boolean nodes union child scopeIds/inputRefs/deficiencies while witness coverageIds stay narrower. Finding evidenceRefs cite witness, facts, coverage and imports from descendants. P-TARGET-incomplete shows retained witness deficiencies with matching query disclosure.',
    'importedHistoryRuntimeAndWireVersionTokens': 'ASSESSED BY READING. Runtime/test/history do not become Coverage; negotiated FactBatchV3 token target-attribution-v2 and occupancy companion/dispatch binding are coherent. No independent probe.',
    'repairPerRequirementDisclosures': 'ACCEPTABLE BY READING. One requirement\'s outcome stays its DeficiencyV2 member and is not a per-requirement D9 code (native §10).',
    'fullQueryResponseParity': 'CHANGES REQUIRED (S37-03). The parity law (workflows §8) is otherwise coherent: graph context requires evidence, run-only resolvedView and advisory const false (Q4 negatives confirmed).',
    'nativeSchemaAnnotationSupersession': 'ACCEPTABLE (A37-08). Bytes are kept because payloadSchemaDigest identifies coverage2; §10 governs.',
    'packageDependencyDirections': 'ACCEPTABLE. The 20-package graph is acyclic: contracts <- identity <- evaluator/syntax pure layers; security depends on evaluator; storage on evaluator and security. apps/cli is Cargo package opensip-cli with binary opensip.',
    'reportDispositions': 'CHANGES REQUIRED (S37-02) for R02/R24 hook language; the other rows are coherent with offline host-projection ownership.',
    'milestonesM0toM6': 'CONSISTENT. Checker PASS on 320 mappings; moduleFirstMilestone and milestoneOrder are coherent; all verification standings not-executed.',
    'phaseSensitiveRecovery': 'CONSISTENT across identity §5, S12, read-only v3, attempt custody, store lineage phase markers and plan F52/F53; 54/54 cases not executed. Advisories A37-01..04.',
}

limitations = [
    'Nonblind review: the reviewer read the author package, its verifier and prior root receipts. No blind reconstruction is claimed, and no blind consumer artifact, root blind diagnosis or replay oracle was read.',
    'Source36 acceptance is not treated as covering source37. The parent36 delta (1 added, 15 changed) was verified, and the whole design was re-read under this charter.',
    'Reference models are Python design references over synthetic native-admitted inputs. No product code exists. Nothing here qualifies a compiler, provider, host, OS durability or platform; all 32 qualification gates remain unperformed (qualified=false), and the 54 recovery cases are not executed.',
    'Partially read files are listed under partiallyRead. Many checker scripts were executed rather than read.',
    'P-CAUSE part C applies the D9 reducer algorithm text to constructed condition lists because no product host finalizer exists. Parts A and B use actual owners and an actual closed Run.',
    'The SEAL adapter (admit_analysis_seal) was not executed; its delegation to close_run is from source reading.',
    'Dependency same-kind totality, imported history/runtime evidence, wire version tokens and repair disclosures were assessed by reading plus reference groups, without independent probes.',
    'F-01..F-14 content lives in earlier review records outside the snapshot and was not re-derived. Issue novelty is judged against the snapshot documents; an item may duplicate a finding in earlier review rounds this reviewer did not read.',
    'No grade, activation, application or implementation authorization is granted. The 30 residuals and 28 condition-2 obligations are retained unchanged.',
]

review = {
    'schema': 'opensip.independent-design-review.source37.v1',
    'reviewer': 'Claude (independent design review origin 85a08aec-9d22-4ac6-8ec2-c10170e727d7)',
    'verdict': 'CHANGES_REQUIRED',
    'verdictBasis': 'No MUST issue was found. Three new SHOULD issues (S37-01 whole-Run cause order/coverageId, S37-02 report hooks versus product boundary, S37-03 query advisory cross-join) need owner corrections before ACCEPT. The reference groups, planning checks and author package verification all pass on verified exact copies.',
    'subjectManifestPath': MANIFEST, 'subjectManifestSha256': sha(MANIFEST), 'verifiedManifest': True,
    'subjectArchiveSha256': arc['archiveSha256'], 'subjectFileCount': arc['manifestFileCount'],
    'contractsReadCompletely': contracts, 'partiallyRead': PARTIAL,
    'newMustIssues': newMustIssues, 'newShouldIssues': newShouldIssues, 'advisories': advisories,
    'probes': probes, 'checkReceipts': checkReceipts, 'assessments': assessments,
    'fDispositions': fDispositions, 'evaluationResidualDispositions': evaluationResidualDispositions,
    'arDispositions': arDispositions, 'fwDispositions': fwDispositions,
    'inheritedResidualDispositions': inheritedResidualDispositions, 'scopedReviewOwnerDispositions': scopedReviewOwnerDispositions,
    'dispositionRowCount': len(allRows),
    'tcbScopeAccount': tcb, 'packageAssessment': pkg_assessment,
    'retained': {'residuals': 30, 'condition2Obligations': 28, 'condition2Source': 'docs/v2/architecture/08-decision-and-readiness-register.md:385-391 (DR-101-107, DR-109-115, DR-117-127, DR-130/131/133)',
                 'qualificationGatesUnperformed': 32, 'recoveryCasesNotExecuted': plan['counts']['recoveryCasesNotExecuted']},
    'authority': {'gradeGranted': False, 'activationGranted': False, 'implementationAuthorized': False, 'blindReconstructionClaimed': False,
                  'source36AcceptanceCoversSource37': False, 'frozenInputsModified': False},
    'limitations': limitations,
}
json.dump(review, open(BASE + '/review.json', 'w'), indent=1, ensure_ascii=False)

# ------------------------------------------------------------------------------------------ markdown
L = []
A = L.append
A('# Independent design review — OpenSIP source37')
A('')
A('**Verdict: CHANGES_REQUIRED.** %s' % review['verdictBasis'])
A('')
A('- Subject manifest: `%s`, SHA-256 `%s` (verified).' % (MANIFEST, review['subjectManifestSha256']))
A('- Archive: SHA-256 `%s`, %d members, every member verified.' % (arc['archiveSha256'], arc['membersMatched']))
A('- Parent36: snapshot verified. Delta: 1 added, 15 changed files (`receipts/parent-delta.json`).')
A('- No grade, activation, application or implementation authorization is granted.')
A('- This is not a blind reconstruction, and source36 acceptance does not cover source37.')
A('')
A('## New MUST issues')
A('')
A('None found.')
A('')
A('## New SHOULD issues')
for s in newShouldIssues:
    A('')
    A('### %s — %s' % (s['id'], s['title']))
    A('')
    A('**Owner selectors**')
    A('')
    for o in s['ownerSelectors']:
        A('- %s' % o)
    A('')
    A('**Consequence.** %s' % s['consequence'])
    A('')
    A('**Reproducer**')
    A('')
    rp = s['reproducer']
    if isinstance(rp, dict):
        for k, v in rp.items():
            if k in ('receipt', 'receipts', 'actualRun'):
                continue
            A('- **%s.** %s' % (k, v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)))
        refs = rp.get('receipts') or [rp.get('receipt')]
        A('- Receipts: %s.' % ', '.join('`%s`' % r for r in refs if r))
    else:
        A(rp)
    A('')
    A('**Minimal remedy.** %s' % s['minimalRemedy'])
    A('')
    A('Related rows: %s.' % ', '.join(s['relatedRows']))
A('')
A('## Advisories (separate from issues)')
for a in advisories:
    A('')
    A('### %s — %s' % (a['id'], a['title']))
    A('')
    A(a['detail'])
    A('')
    A('- Selectors: %s.' % '; '.join('`%s`' % x for x in a['selectors']))
    if a.get('receipt'):
        A('- Receipt: `%s`.' % a['receipt'])
    A('- Disposition: %s' % a['disposition'])
A('')
A('## Independent probes')
for p in probes:
    A('')
    A('### %s — %s' % (p['id'], p['claim']))
    A('')
    A('- Script: `%s`.' % p['script'])
    A('- Receipt: `%s`.' % p['receipt'])
    A('- Discriminating: %s.' % p['discriminating'])
    if p['id'] == 'P-REMINT':
        A('')
        for r in p['result']:
            A('- **%s.**' % r['label'])
            A('  - structural `open_run_closure`: %s (new RunId).' % r['structuralOwnerClosure']['result'])
            A('  - complete replay: %s `%s`.' % (r['completeReplay']['result'], r['completeReplay'].get('error')))
            A('  - `close_run`: %s.' % r['close_run']['result'])
            A('  - graph query: %s %s/%s, exit %s.' % (r['publicGraphQuery']['result'], r['publicGraphQuery'].get('errorCode'), r['publicGraphQuery'].get('detail'), r['publicGraphQuery'].get('exitCode')))
    elif p['id'] == 'P-QUERY':
        A('')
        A('- Q1 schema-first: %s.' % p['result']['Q1-schemaFirst'])
        A('- Q2 ambiguous reachable: %s.' % p['result']['Q2-ambiguousReachable'])
        A('- Q3 availability mapping: %s (unknown state: %s).' % (p['result']['Q3-availabilityMapping'], p['result']['Q3-unknownState']))
        A('- Q4 parity: %s.' % json.dumps(p['result']['Q4-parity'], ensure_ascii=False))
        A('- Q5 cursor: %s.' % json.dumps(p['result']['Q5'], ensure_ascii=False))
        A('- Q6 caps: %s.' % json.dumps(p['result']['Q6'], ensure_ascii=False))
    elif p['id'] == 'P-CAUSE':
        A('')
        A('- Actual run: `%s`.' % json.dumps(p['result']['actualRun']))
        A('- Deficient coverage records: %s.' % p['result']['deficientCoverageRecords'])
        A('- Causes with no route: %s.' % p['result']['causesWithoutAnyOwnerRoute'])
        A('- A: %s.' % json.dumps({k: v for k, v in p['result']['A'].items() if k != 'candidates'}))
        A('- B: %s.' % json.dumps(p['result']['B']))
        A('- C: %s.' % json.dumps(p['result']['C']))
    else:
        A('- Result: `%s`.' % json.dumps(p['result'], ensure_ascii=False)[:1500])
A('')
A('## Check receipts')
A('')
for c in checkReceipts:
    ok = c['result'].get('exitCode', c['result'].get('passed', c['result'].get('verified', '')))
    A('- %s: `%s` (`%s…`); result key: %s.' % (c['check'], c['path'], c['sha256'][:16], ok))
A('')
A('Six groups ran (exit, seconds):')
A('')
for r in groups['rows']:
    A('- %s: %d, %.1f.' % (r['name'], r['exitCode'], r['seconds']))
A('')
A('The checkers changed no copy files.')
A('')
A('**Planning checks**')
A('')
A('- `check_implementation_planning`: `%s`.' % plan['check_implementation_planning']['stdout'].strip()[:200])
A('- `check_repository_file_inventory`: `%s`.' % plan['check_repository_file_inventory']['stdout'].strip()[:200])
A('')
A('## Assessments')
A('')
for k, v in assessments.items():
    A('- **%s.** %s' % (k, v))
A('')
A('## TCB-SCOPE-01 (one shared assumption, 13 dependent accounts)')
A('')
A('**Dependent accounts:** %s.' % ', '.join(TCB))
A('')
A('**Assumption.** %s' % tcb['assumption'])
A('')
for x in tcb['assessment']:
    A('- %s' % x)
A('')
A('**Standing.** %s' % tcb['standing'])
A('')
A('## Author package v14 (nonblind)')
A('')
for x in pkg_assessment['independentObservations']:
    A('- %s' % x)
A('')
A('**Standing.** %s' % pkg_assessment['standing'])
A('')
A('## Disposition rows (%d)' % len(allRows))
A('')
A('Every row has `appliedByThisReview=false` and `finalApplicationOutcomeGranted=false`. Full text is in review.json.')
for name, rows in (('fDispositions', fDispositions), ('evaluationResidualDispositions', evaluationResidualDispositions), ('arDispositions', arDispositions),
                   ('fwDispositions', fwDispositions), ('inheritedResidualDispositions', inheritedResidualDispositions), ('scopedReviewOwnerDispositions', scopedReviewOwnerDispositions)):
    A('')
    A('### %s (%d)' % (name, len(rows)))
    A('')
    A('| id | disposition | note |')
    A('|---|---|---|')
    for r in rows:
        extra = (' [author grade PENDING]' if 'authorGrade' in r else '') + (' [depends on TCB-SCOPE-01]' if r.get('sharedDependency') else '')
        A('| %s | %s%s | %s |' % (r['id'], r['disposition'], extra, r['assessment'].replace('|', '/')[-260:]))
A('')
A('## Retained')
A('')
A('- 30 evaluation residuals (all author grades PENDING).')
A('- 28 condition-2 obligations (%s).' % review['retained']['condition2Source'])
A('- 32 qualification gates unperformed.')
A('- %d recovery cases not executed.' % review['retained']['recoveryCasesNotExecuted'])
A('')
A('## Contracts read completely (%d)' % len(contracts))
A('')
A('| path | sha256 | lines |')
A('|---|---|---|')
for c in contracts:
    A('| %s | `%s` | %d |' % (c['path'], c['sha256'], c['lines']))
A('')
A('### Partially read')
A('')
for p in PARTIAL:
    A('- %s: %s' % (p['path'], p['read']))
A('')
A('## Limitations')
A('')
for x in limitations:
    A('- %s' % x)
open(BASE + '/review.md', 'w').write('\n'.join(L) + '\n')
print(json.dumps({'verdict': review['verdict'], 'rows': len(allRows), 'must': len(newMustIssues), 'should': len(newShouldIssues),
                  'advisories': len(advisories), 'contracts': len(contracts), 'reviewJsonSha256': sha(BASE + '/review.json'),
                  'reviewMdSha256': sha(BASE + '/review.md')}, indent=1))
