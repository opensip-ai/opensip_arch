"""Build review.json and review.md for the independent source38 design review.

Reads frozen source38/37 bytes, retained predecessor reviews, root/author evidence and this runtime's own
receipts. Writes only RT/review.json and RT/review.md. Every hash is recomputed here at build time.
"""
import glob
import hashlib
import json
import os
import re
import sys

RT = '/private/tmp/opensip-design-corrections/claude-independent-design.v38'
S38 = '/tmp/opensip-design-corrections/candidate-subject.v38'
S37 = '/tmp/opensip-design-corrections/candidate-subject.v37'
B = '/tmp/opensip-design-corrections'
REC = RT + '/receipts'
LIVE38 = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v38.json'
FALSE_FLAGS = {'appliedByThisReview': False, 'finalApplicationOutcomeGranted': False}
GAPS = []


def sha(p):
    try:
        with open(p, 'rb') as fh:
            return hashlib.sha256(fh.read()).hexdigest()
    except OSError:
        GAPS.append('missing: ' + p)
        return None


def nlines(p):
    try:
        with open(p, 'rb') as fh:
            b = fh.read()
    except OSError:
        return None
    return b.count(b'\n') + (0 if (not b or b.endswith(b'\n')) else 1)


def J(p):
    with open(p, encoding='utf-8') as fh:
        return json.load(fh)


def rel(p):
    return p.replace(RT + '/', '')


def src(p):
    return {'path': p, 'sha256': sha(S38 + '/' + p), 'lines': nlines(S38 + '/' + p)}


# ------------------------------------------------------------------------------------------------ subject
SV = J(REC + '/subject-verification.json')
delta = SV.get('delta', {})
delta_counts = {k: (len(v) if isinstance(v, list) else v) for k, v in delta.items() if k in ('changed', 'added', 'removed')}
archives = {rel(p): {'sha256': sha(p), 'content': J(p)} for p in sorted(glob.glob(REC + '/archive-verification*.json'))}
live_sha = sha(LIVE38)

# ------------------------------------------------------------------------------------------------ read scope
FRESH_COMPLETE = [
    ('docs/coop/design-corrections/foundation/run-termination-contract.v1.md', 'added in 38; complete'),
    ('docs/coop/design-corrections/foundation/run-termination-goldens.v1.json', 'added in 38; complete'),
    ('docs/coop/design-corrections/foundation/run_termination_model.v1.py', 'added in 38; complete'),
    ('docs/v2/architecture/implementation-normative-inputs.v6.json', 'added in 38; complete'),
    ('docs/v2/contracts/product-v1/workflows-and-surfaces.md', 'changed; complete sequential chunks'),
    ('docs/v2/contracts/product-v1/native-evidence.md', 'changed; complete sequential chunks (lines 3789 and 3791 verified by tail print)'),
    ('docs/v2/contracts/product-v1/security-and-lifecycle.md', 'changed; complete sequential chunks'),
    ('docs/coop/design-corrections/workflows/query-projection-contract.v3.md', 'changed; complete'),
    ('docs/coop/design-corrections/workflows/workflow-projection-contract.v3.md', 'changed; complete'),
    ('docs/coop/design-corrections/security/carrier-format.v3.md', 'changed; complete'),
    ('docs/coop/design-corrections/security/grant-journal.carrier.v3.sql', 'changed; complete'),
    ('docs/coop/design-corrections/security/carrier-migration.v1.md', 'changed; complete'),
    ('docs/coop/design-corrections/security/carrier-dispatch.v3.json', 'changed; complete'),
    ('docs/coop/design-corrections/security/check-carrier-v3.py', 'changed; complete in two ranges (440-1063 before context compaction, 1-440 after)'),
    ('docs/v2/architecture/commit-recovery-readonly.v3.md', 'changed; complete'),
    ('docs/v2/architecture/attempt-custody.schema.v1.json', 'changed; complete'),
    ('docs/v2/architecture/store-instance-lineage.v1.json', 'changed; complete'),
    ('docs/v2/architecture/14-repository-and-module-layout.md', 'changed; complete'),
    ('docs/v2/architecture/implementation-boundaries-and-build-plan.md', 'changed; complete'),
    ('docs/coop/design-corrections/foundation/evaluator_replay_model.v3.py', 'changed; complete'),
    ('docs/coop/design-corrections/foundation/check-evaluator-faults.v3.py', 'changed; complete'),
    ('docs/coop/design-corrections/security/check-analysis-seal-adapter.v1.py', 'changed; complete'),
    ('docs/coop/design-corrections/inherited-residuals.proposed.md', 'unchanged 37->38; freshly re-read complete'),
]
DELTA_READ = [
    ('docs/coop/design-corrections/foundation/identity-model.v3.py', 'complete 37->38 diff; ranges 1-70, 600-690, 1412-1439; grep context of every native_admission()/workflow_admission() call site'),
    ('docs/coop/design-corrections/foundation/evaluator_composition_model.v3.py', 'complete 37->38 diff'),
    ('docs/coop/design-corrections/security/security_lifecycle_model_v1.py', 'complete 37->38 diff; lines 175, 1527-1550 located by grep'),
    ('docs/coop/design-corrections/workflows/query_projection_model.v3.py', 'complete 37->38 diff; ranges 565-597, 1504-1546'),
    ('docs/coop/design-corrections/workflows/check-query-projection.v3.py', 'complete 37->38 diff (executed: 193 checks)'),
    ('docs/coop/design-corrections/foundation/check-semantic-replay.v3.py', 'complete 37->38 diff (executed in evaluator3 group)'),
    ('docs/coop/design-corrections/foundation/evaluator_semantic_fixture.v3.py', 'complete 37->38 diff'),
    ('docs/coop/design-corrections/workflows/schemas/common.schema.json', 'complete 37->38 diff; overlay bytes identical to 38 were reviewed in the bounded root-corrections review'),
    ('docs/coop/design-corrections/workflows/schemas/evaluator3/common.schema.json', 'complete 37->38 diff; overlay-identical'),
    ('docs/coop/design-corrections/workflows/schemas/evaluator3/graph-query.schema.json', 'complete 37->38 diff; overlay-identical'),
    ('docs/coop/design-corrections/workflows/workflow-cases.v1.json', 'complete 37->38 diff; overlay-identical'),
    ('docs/coop/design-corrections/workflows/check_workflows.v1.py', 'complete 37->38 diff; overlay-identical (executed in workflows group)'),
    ('docs/coop/design-corrections/workflows/check-workflow-projection.v3.py', 'complete 37->38 diff; overlay-identical (executed: 493 checks)'),
    ('docs/coop/design-corrections/workflows/workflows-report.v1.json', 'complete 37->38 diff'),
    ('docs/coop/design-corrections/foundation/source-pins.v1.json', 'complete 37->38 diff (pin gate executed by groups)'),
    ('docs/coop/design-corrections/foundation/evaluator3-source-pins.v1.json', 'complete 37->38 diff'),
    ('docs/coop/design-corrections/native/source-pins.v2.json', 'complete 37->38 diff'),
    ('docs/coop/design-corrections/security/source-pins.v1.json', 'complete 37->38 diff'),
    ('docs/coop/design-corrections/workflows/source-pins.v1.json', 'complete 37->38 diff'),
    ('docs/v2/architecture/implementation-coverage.v1.json', 'complete 37->38 diff (planning checker executed)'),
    ('docs/v2/architecture/implementation-planning-sources.v1.json', 'complete 37->38 diff'),
    ('docs/v2/architecture/repository-file-inventory.v1.json', 'complete 37->38 diff plus row-by-row JSON comparison (only finalization.rs and outcomes.rs rows changed)'),
    ('docs/v2/architecture/prototype-report-inventory.md', 'complete 37->38 diff; overlay bytes identical to 38 were read completely in the bounded review'),
]
delta_paths = set()
for kind in ('changed', 'added', 'removed'):
    for row in (delta.get(kind) or []):
        delta_paths.add(row['path'] if isinstance(row, dict) else row)

fresh = []
for p, note in FRESH_COMPLETE:
    e = src(p)
    e.update(read='complete', note=note, readClass='fresh38Read', inDelta37to38=p in delta_paths)
    fresh.append(e)
delta_reads = []
for p, note in DELTA_READ:
    e = src(p)
    d = REC + '/delta-diffs/' + p.replace('/', '__') + '.diff'
    e.update(read='delta-and-ranges (not a whole-file read)', note=note, readClass='fresh38DeltaRead',
             diffReceipt=rel(d), diffSha256=sha(d), inDelta37to38=p in delta_paths)
    delta_reads.append(e)

v37 = J(B + '/claude-independent-design.v37/review.json')
fresh_set = {p for p, _ in FRESH_COMPLETE} | {p for p, _ in DELTA_READ}
inherited, changed_not_fresh = [], []
for r in v37['contractsReadCompletely']:
    p = r['path']
    if p in fresh_set:
        continue
    a, b = sha(S37 + '/' + p), sha(S38 + '/' + p)
    if a == b:
        inherited.append({'path': p, 'sha256': b, 'lines': r['lines'], 'readClass': 'inheritedUnchanged37Read',
                          'basis': 'read completely by the source37 review; byte-identical in source38 (hash recomputed here)'})
    else:
        changed_not_fresh.append({'path': p, 'sha37': a, 'sha38': b})
for p, _ in FRESH_COMPLETE + DELTA_READ:
    if p not in delta_paths and 'unchanged' not in _:
        GAPS.append('read-scope entry not in 37->38 delta: ' + p)
uncovered_delta = sorted(delta_paths - fresh_set)

# ------------------------------------------------------------------------------------------------ receipts
def receipt(p):
    return {'path': rel(p), 'sha256': sha(p)}


G = J(REC + '/reference/groups-report.json')
P = J(REC + '/planning-checks.json')
PK = J(REC + '/package-verification/verification.json')
TERM = J(REC + '/probe-run-termination.json')
CAR = J(REC + '/probe-carrier-sql.json')
SQF = J(REC + '/probe-seal-query-fault.json')
STAT = J(REC + '/static-raise-reachability.json')

children = {}
for f in sorted(glob.glob(REC + '/reference/evaluator3/*.stdout')):
    name = os.path.basename(f)[:-7]
    try:
        d = J(f)
        children[name] = {k: d[k] for k in ('passed', 'count', 'checkCount', 'failed') if k in d and not isinstance(d[k], (dict, list)) or k == 'failed' and d.get(k) == []}
    except Exception:
        children[name] = {'parsed': False}
group_rows = [{'name': r['name'], 'exitCode': r['exitCode'], 'seconds': r.get('seconds'), 'scriptSha256': r.get('scriptSha256'),
               'scriptMatchesManifest': r.get('scriptMatchesManifest'), 'copyUnchangedAfter': r.get('copyAfter') == {'changed': [], 'missing': [], 'extra': []},
               'stdoutTail': (r.get('stdoutTail') or '')[-300:]} for r in G['rows']]

ind_equal = all(r.get('equal') is True for r in TERM['IND'])
# compact [variant, equal, owner termination, independent termination] rows for citation
TERM['IND'] = [[r.get('variant'), r.get('equal'), r.get('author'), r.get('independent')] for r in TERM['IND']]


def leaf_counts(node, out):
    if isinstance(node, str):
        for tag in ('ADMIT', 'REFUSE', 'HARNESS'):
            if node.startswith(tag):
                out[tag] = out.get(tag, 0) + 1
    elif isinstance(node, dict):
        for v in node.values():
            leaf_counts(v, out)
    elif isinstance(node, list):
        for v in node:
            leaf_counts(v, out)
    return out


carrier_sections = {'sqlite': CAR.get('sqlite')}
for enc, node in (CAR.get('HOSTILE') or {}).items():
    carrier_sections['HOSTILE/' + enc] = leaf_counts(node, {})
carrier_sections['ORDER'] = leaf_counts(CAR.get('ORDER') or {}, {})
CAR['DISPATCH'] = dict(CAR.get('DISPATCH') or {}, routeSchemaValidity=CAR.get('ROUTES'))

preserved = sorted(rel(p) for p in glob.glob(REC + '/**/*attempt*', recursive=True))
inventory = []
for root, dirs, files in os.walk(RT):
    if '/work' in root[len(RT):]:
        continue
    for f in files:
        p = os.path.join(root, f)
        if p in (RT + '/review.json', RT + '/review.md'):
            continue
        inventory.append({'path': rel(p), 'bytes': os.path.getsize(p), 'sha256': sha(p)})
inventory.sort(key=lambda x: x['path'])

PROBES = [
    {'id': 'P38-SUBJECT', 'script': 'probes/verify_subject.py', 'receipts': ['receipts/subject-verification.json', 'receipts/manifest38-index.json'],
     'claim': 'LIVE candidate-subject.v38.json and snapshot verified member by member; parent37 manifest and 37->38 delta measured.'},
    {'id': 'P38-ARCHIVE', 'script': 'probes/verify_archive_extract.py', 'receipts': sorted(archives),
     'claim': 'Archive 571aad4d... hashed; every member extracted into the two disposable copies and compared by hash and length.'},
    {'id': 'P38-DELTA', 'script': 'probes/make_delta_diffs.py', 'receipts': ['receipts/delta-diffs/'],
     'claim': 'Unified 37->38 diffs for all changed files (reading aid; diffs are not whole-file reads).'},
    {'id': 'P38-GROUPS', 'script': 'probes/run_reference_groups.py', 'receipts': ['receipts/reference/groups-report.json'],
     'claim': 'Six pinned reference groups with /tmp/opensip-architecture-review-env/bin/python -I -B on a verified disposable exact copy; copy re-verified before and after.'},
    {'id': 'P38-PLAN', 'script': 'probes/run_planning_checks.py', 'receipts': ['receipts/planning-checks.json'],
     'claim': 'check_implementation_planning --check and check_repository_file_inventory --check on the exact copy, plus independent v6/coverage/planning-source binding counts.'},
    {'id': 'P38-PKG', 'script': 'claude-author-package-successor.v15/verify-package.py (author verifier, executed on the verified copy)', 'receipts': ['receipts/package-verification/verification.json'],
     'claim': 'Package15 13 Run/control structural and full-replay checks plus 7 query checks against source38.'},
    {'id': 'P38-TERM', 'script': 'probes/probe_run_termination.py', 'receipts': ['receipts/probe-run-termination.json'],
     'claim': 'Independent derivation of the whole-Run termination over 11 actual closed Runs versus the owner model; native stage helper; semantically false Run; projection boundary; 47-cause bridge; mixed-owner cases.', 'discriminating': True},
    {'id': 'P38-CARRIER', 'script': 'probes/probe_carrier_sql.py', 'receipts': ['receipts/probe-carrier-sql.json'],
     'claim': 'Hostile TEXT/hex/NUL/BLOB grammar in three encodings, publication/first_generation/superseded/TERMINAL order laws, and open-dispatch phase routes over real SQLite carriers.', 'discriminating': True},
    {'id': 'P38-SEALQ', 'script': 'probes/probe_seal_query_fault.py', 'receipts': ['receipts/probe-seal-query-fault.json'],
     'claim': 'SEAL adapter over lawful, reminted false, structural and foreign same-name exceptions; replay-stack exception-class coverage walk; graph query missing/corrupt/reminted/host-defect/foreign-class routes and retained availability records; fault pair schema-versus-parity discrimination; StepTermination admission enumeration.', 'discriminating': True},
    {'id': 'P38-STATIC', 'script': 'probes/static_raise_reachability.py', 'receipts': ['receipts/static-raise-reachability.json'],
     'claim': 'Syntactic escape analysis of owner exceptions from identity-model.v3 call sites that are not locally wrapped (attempt 2 accounts for call-site try blocks).', 'discriminating': False},
]
for pr in PROBES:
    s = pr['script']
    pr['scriptSha256'] = sha(RT + '/' + s) if s.startswith('probes/') else None
    pr['receiptSha256'] = {r: (sha(RT + '/' + r) if not r.endswith('/') else None) for r in pr['receipts']}

# ------------------------------------------------------------------------------------------------ root / author evidence
def ev(p, note):
    full = B + '/' + p
    d = {'path': full, 'sha256': sha(full), 'note': note}
    try:
        j = J(full)
        for k in ('standing', 'passed', 'outcome'):
            if k in j and not isinstance(j[k], (dict, list)):
                d[k] = j[k]
    except Exception:
        pass
    return d


EVIDENCE = [
    ev('root-final38-reference.v1/reference-checks.json', 'FAILED root reference run (passed=false; evaluator3 analysis-seal child exit 1). Preserved as a failure; not relabelled.'),
    ev('root-final38-reference.v1/evaluator3.stdout', 'child list of the failed run'),
    ev('root-final38-reference.v1/evaluator3/analysis-seal.stderr', 'failing child stderr (name-based SEAL catch let CompleteReplayMismatch escape)'),
    ev('root-final38-reference.v2/reference-checks.json', 'root rerun after the SEAL correction (original runner); evidence only'),
    ev('root-final38-reference-binding.v1/reference-checks.bound.json', 'final-reference bound to the frozen source38 subject; evidence only'),
    ev('root-final38-prefreeze.v2/verification.json', 'root declared delta and pin verification before freeze'),
    ev('root-final38-custody.v1/verification.json', 'root custody verification of the frozen snapshot'),
    ev('root-source38-dispositions.v4/dispositions.json', 'root disposition ledger; predates the completed SEAL integration assessment and the final bindings'),
    ev('root-source38-host-integration.v1/integration.json', 'root integration of host-finalizer v2 (NONBLIND)'),
    ev('root-source38-host-planning.v1/assessment.json', 'root planning ownership clarification'),
    ev('root-source38-carrier-integration.v1/integration.json', 'root integration of carrier v3'),
    ev('root-source38-query-integration.v1/integration.json', 'root integration of query-fault v2'),
    ev('root-source38-fault-check-correction.v1/assessment.json', 'root QF-I1 checker correction'),
    ev('root-final38-seal-correction.v1/proposal.json', 'root two-file SEAL adapter correction'),
    ev('root-final38-seal-correction.v1/check.json', 'root SEAL correction check'),
    ev('root-final38-seal-acceptance.v1/assessment.json', 'root SEAL acceptance assessment'),
    ev('claude-source38-seal-integration-assessment.v1/review.json', 'actual Claude SEAL/fault integration assessment (NONBLIND coauthor; SI-1..5, SI-A1, QF-1, v2 qualification)'),
    ev('claude-source38-seal-integration-assessment.v1/process.json', 'process record of that assessment'),
    ev('claude-source37-host-finalizer-author.v2/review.json', 'host-finalizer author v2 (NONBLIND author)'),
    ev('claude-source37-carrier-owner-author.v3/review.json', 'carrier owner author v3 (NONBLIND author)'),
    ev('claude-source37-query-fault-author.v2/review.json', 'query-fault author v2 (NONBLIND author)'),
    ev('claude-source37-root-corrections-review.v1/review.json', 'bounded root-corrections review (PARTIAL); preserved unchanged'),
    ev('claude-independent-design.v37/review.json', 'source37 independent review (CHANGES_REQUIRED); preserved unchanged'),
    ev('claude-independent-design.v37/review.md', 'source37 independent review markdown; preserved unchanged'),
]
proc = {}
try:
    proc = J(B + '/claude-source38-seal-integration-assessment.v1/process.json')
except Exception:
    pass
seal_origin = [str(v) for v in proc.values() if isinstance(v, str) and 'f561' in v]
qf_v2_sha = sha(B + '/claude-source37-query-fault-author.v2/review.json')
qf_v2_expected = J(B + '/root-source38-query-integration.v1/integration.json').get('reviewSha256')
bounded_sha = sha(B + '/claude-source37-root-corrections-review.v1/review.json')
bounded_expected = J(B + '/root-source38-dispositions.v4/dispositions.json').get('boundedRootReview', {}).get('sha256')
registry_text = open(S38 + '/docs/coop/design-corrections/public-detail-registry.v1.json', encoding='utf-8').read()
seal_key_registered = 'SEAL_CLOSE_RUN_REFUSED' in registry_text
native_schema_same = sha(S37 + '/docs/coop/design-corrections/native/native-evidence.schemas.v2.json') == sha(S38 + '/docs/coop/design-corrections/native/native-evidence.schemas.v2.json')
map_sources = {}
for p in ('docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json', 'docs/coop/design-corrections/correction-crosswalk.proposed.json',
          'docs/coop/design-corrections/inherited-residuals.proposed.md', 'docs/coop/design-corrections/current-source-map.proposed.md',
          'docs/v2/architecture/08-decision-and-readiness-register.md', 'docs/coop/design-corrections/qualification-gates.proposed.json',
          'docs/v2/contracts/product-v1/admission-and-qualification.md', 'docs/v2/contracts/product-v1/identity-and-evidence.md'):
    a, b = sha(S37 + '/' + p), sha(S38 + '/' + p)
    map_sources[p] = {'sha256': b, 'unchanged37to38': a == b}
gates = J(S38 + '/docs/coop/design-corrections/qualification-gates.proposed.json')
gate_rows = gates.get('gates') or gates.get('items') or []
gates_qualified_true = sum(1 for g in gate_rows if isinstance(g, dict) and g.get('qualified') is True)
pkg_manifest_sha = sha('/tmp/opensip-design-corrections/claude-author-package-successor.v15/artifact-manifest.json')
pkg_binding = J('/tmp/opensip-design-corrections/claude-author-package-successor.v15/source-binding.v38.json')

# ------------------------------------------------------------------------------------------------ items
QS = SQF.get('QUERY', {})
SS = SQF.get('SEAL', {})
FS = SQF.get('FAULT', {})
SCH = SQF.get('SCHEMA', {})
ORDER = CAR.get('ORDER', {})
DISP = CAR.get('DISPATCH', {})

ITEMS = [
    {'id': 'S37-01', 'origin': 'claude-independent-design.v37 (SHOULD)', 'disposition': 'CLOSED-AT-SOURCE-LEVEL',
     'finalOwnerSelectors': ['docs/coop/design-corrections/foundation/run-termination-contract.v1.md:61-84 (§3 condition population), :85-135 (§4 conditions, evaluator-only bridge and total order), :136-163 (§5 coverageId), :164-199 (§6 checking and goldens)',
                             'docs/coop/design-corrections/foundation/run_termination_model.v1.py; run-termination-goldens.v1.json',
                             'docs/v2/contracts/product-v1/workflows-and-surfaces.md:1135-1189 (§9 selects the owner)',
                             'docs/v2/contracts/product-v1/native-evidence.md:2946-2966 (native stage selection stops; the Run termination owner is named)',
                             'docs/coop/design-corrections/workflows/workflow-projection-contract.v3.md:138 (EVALUATION.WORK_BUDGET_EXHAUSTED positioned by run-termination-contract §4)',
                             'docs/v2/architecture/implementation-normative-inputs.v6.json and implementation-coverage.v1.json workflows-and-surfaces:10 (incorporated owner pinned)'],
     'evidence': {'P38-TERM': {'closedRunVariants': len(TERM['IND']), 'independentDerivationEqualsOwnerForAll': ind_equal,
                               'nativeStageRecords': TERM.get('NAT'), 'falseRun': TERM.get('FALSE'), 'bridge': {k: TERM['BRIDGE'][k] for k in ('registered', 'routeMismatchVsIndependent', 'routeDrift', 'unregistered')}},
                  'evaluator3 native-replay child': children.get('native-replay')},
     'consequence': 'The analysis projection (class, runId, ordered reasonCodes, coverageId, absence of errorCode/faultCause/signal) is now a deterministic function of the sealed Run. Independent derivation matched the owner on every variant, including foo-budget+bar-unavailable, work budget with native stage carriers, provider-fault/cancelled/complete stage terminals and the complete-empty and policy-failed controls, and was invariant to discovery and object order. Delegated executionId/domainDetail/authority remain owner-validation-required (ADV38-01).'},
    {'id': 'S37-02', 'origin': 'claude-independent-design.v37 (SHOULD); bounded review CLOSED-BY-OVERLAY-TEXT', 'disposition': 'CLOSED-AT-SOURCE-LEVEL',
     'finalOwnerSelectors': ['docs/v2/architecture/prototype-report-inventory.md:37 (R02: versioned host-approved data projections only; executable report hooks not admitted under admission §5)',
                             'docs/v2/architecture/prototype-report-inventory.md:179 (External tools row: no executable report-hook admission)',
                             'docs/v2/contracts/product-v1/admission-and-qualification.md:344-345 (§5 items 4-5: no untrusted native/WASM admission; no imperative contributions or project hooks)',
                             'docs/v2/architecture/implementation-coverage.v1.json R02 and R24 valueSha256 rebound'],
     'evidence': {'P38-PLAN': P.get('check_implementation_planning', {}).get('stdout')},
     'consequence': 'The planning layer no longer selects executable report hooks, so TCB-SCOPE-01 has no report-rendering exception.'},
    {'id': 'S37-03', 'origin': 'claude-independent-design.v37 (SHOULD); bounded review CLOSED-FOR-SCHEMA-AND-CONTROLS', 'disposition': 'CLOSED-AT-SOURCE-LEVEL',
     'finalOwnerSelectors': ['docs/coop/design-corrections/workflows/schemas/evaluator3/graph-query.schema.json:908-1022, 1180-1194 (advisory law)',
                             'docs/coop/design-corrections/workflows/query-projection-contract.v3.md:152 (advisory is schema-const false for graph.*)'],
     'evidence': {'P38-SEALQ.SCHEMA.advisoryViolations': SCH.get('advisoryViolations'), 'evaluator3 query-projection child': children.get('query-projection')},
     'consequence': 'Advisory is admitted exactly where the schema law permits; no advisory violation was produced by the enumeration.'},
    {'id': 'A37-01', 'origin': 'claude-independent-design.v37 (advisory)', 'disposition': 'CLOSED-AT-SOURCE-LEVEL',
     'finalOwnerSelectors': ['docs/coop/design-corrections/security/grant-journal.carrier.v3.sql:33, 49-50, 63-65, 89-114 (typeof + length + instr(col, char(0)) = 0 + prefix GLOB + NOT GLOB \'*[^0-9a-f]*\')',
                             'docs/coop/design-corrections/security/carrier-format.v3.md:168-227 (§5.1 exact storage class and whole-value grammar)',
                             'docs/v2/architecture/attempt-custody.schema.v1.json:153-155 (proposedPrivateDDL and ddlGrammarCorrection)'],
     'evidence': {'P38-CARRIER.sectionCounts': carrier_sections},
     'consequence': 'Every hostile hex/prefix/NUL/BLOB/zero-width/fullwidth variant was refused in UTF-8, UTF-16le and UTF-16be carriers. The free-text body column admits an embedded NUL, and documented SQLite affinity conversions are admitted; carrier-format §5.1 leaves closed-record admission to the host, and this review treats that as the stated boundary, not a defect.'},
    {'id': 'A37-02', 'origin': 'claude-independent-design.v37 (advisory)', 'disposition': 'CLOSED-AT-SOURCE-LEVEL',
     'finalOwnerSelectors': ['docs/coop/design-corrections/security/grant-journal.carrier.v3.sql:58-70 (migrated_from/migration_op_ref/first_generation CHECKs), :73-75 (format row immutable), :137-151 (no append before the format row; below first_generation; superseded generation)',
                             'docs/coop/design-corrections/security/carrier-format.v3.md:168-227 (publication law)', 'docs/coop/design-corrections/security/carrier-migration.v1.md'],
     'evidence': {'P38-CARRIER.ORDER': ORDER},
     'consequence': 'The publication and first_generation laws are DDL-enforced in the footprint that 37 found unenforced. The superseded-generation law was isolated after attempt 2 showed contiguity firing first.'},
    {'id': 'A37-03', 'origin': 'claude-independent-design.v37 (advisory)', 'disposition': 'CLOSED-AT-SOURCE-LEVEL (editorial residual ADV38-03)',
     'finalOwnerSelectors': ['docs/v2/contracts/product-v1/security-and-lifecycle.md:1300-1301 (MIGRATION.CORRUPT scope; carrier project binding mismatch with domainDetail omitted), :1310-1312',
                             'docs/coop/design-corrections/security/carrier-dispatch.v3.json:568-580 and :597-609 (carrier-project-binding-mismatch routes)',
                             'docs/v2/architecture/commit-recovery-readonly.v3.md:58-69'],
     'evidence': {'P38-CARRIER.DISPATCH.keys': sorted(DISP)},
     'consequence': 'A foreign project binding is no longer carried by MIGRATION.CORRUPT on any path.'},
    {'id': 'A37-04', 'origin': 'claude-independent-design.v37 (advisory)', 'disposition': 'CLOSED-AT-SOURCE-LEVEL (residual ADV38-02)',
     'finalOwnerSelectors': ['docs/v2/contracts/product-v1/security-and-lifecycle.md:1300 (writer F51), :1305 (read-only quarantine incl. F51), :1307 (F46 unknown-carrier-incompatible)',
                             'docs/coop/design-corrections/security/carrier-format.v3.md:361-402 (§8.1 phase-specific routes)',
                             'docs/coop/design-corrections/security/carrier-dispatch.v3.json:611-674 (publicProjectionByPhase.readOnlyRecovery and readOnlyStandingOfDispatchResult)'],
     'evidence': {'P38-CARRIER.DISPATCH': DISP},
     'consequence': 'F46 and F51 have public projections that validate against both StepTermination schemas. Format-1 rows after TERMINAL and a UTF-16 F51 carrier are detected as split-brain (writer MIGRATION.CORRUPT; read-only quarantine with stable observations).'},
    {'id': 'A37-05', 'origin': 'claude-independent-design.v37 (advisory); bounded RC37-A1', 'disposition': 'CLOSED-AT-SOURCE-LEVEL (see RC37-A1)',
     'finalOwnerSelectors': ['docs/coop/design-corrections/workflows/query-projection-contract.v3.md:160-164', 'query_projection_model.v3.py:1504-1519 host_adapter_refusal, :1522-1546 observe_retained_availability'],
     'evidence': {'P38-SEALQ.QUERY.retainedAvailability': QS.get('retained availability')}, 'consequence': 'An out-of-vocabulary observation is a reference precondition, a product adapter defect with a valid RequestId is host-invariant, and a malformed retained record is evidence.corrupt.'},
    {'id': 'A37-06', 'origin': 'claude-independent-design.v37 (advisory); bounded RC37-01 SHOULD', 'disposition': 'CLOSED-AT-SOURCE-LEVEL (see RC37-01)',
     'finalOwnerSelectors': ['docs/coop/design-corrections/workflows/query-projection-contract.v3.md:166-173, 186-191'], 'evidence': {'see': 'RC37-01'}, 'consequence': 'Complete-replay disagreement is no longer collapsed into corrupt bytes.'},
    {'id': 'A37-07', 'origin': 'claude-independent-design.v37 (editorial); bounded CLOSED-FOR-WORDING', 'disposition': 'CLOSED-AT-SOURCE-LEVEL (RC37-A4 editorial retained)',
     'finalOwnerSelectors': ['docs/v2/architecture/implementation-boundaries-and-build-plan.md:10-22, 1039-1052, 1103-1111 (current v6 binding; historical checkpoints 1083-1101 preserved)',
                             'docs/v2/architecture/store-instance-lineage.v1.json:470 and :508 (currentStandingNote F00-F53)', 'docs/v2/architecture/14-repository-and-module-layout.md:719-731'],
     'evidence': {'P38-PLAN.counts': {k: P.get('counts', {}).get(k) for k in ('v6Sha256', 'v6Inputs', 'coverageSubjectMatchesV6', 'planningSourcesArchitectureSha256MatchesV6', 'inventoryPaths', 'inventoryPackages', 'coverageMappings')}},
     'consequence': 'Standing prose names the current v6 layer and preserves dated counts as history.'},
    {'id': 'A37-08', 'origin': 'claude-independent-design.v37 (advisory)', 'disposition': 'ACCEPTED-AS-DESIGNED-UNCHANGED',
     'finalOwnerSelectors': ['docs/v2/contracts/product-v1/native-evidence.md:2933-2944 (explicit annotation supersession)', 'docs/coop/design-corrections/native/native-evidence.schemas.v2.json (registered payload schema bytes)'],
     'evidence': {'nativeSchemaBytesUnchanged37to38': native_schema_same},
     'consequence': 'The registered payload schema bytes and every coverage2 identity minted against them stay unchanged. The superseded annotation remains readable in the schema, and native §10 governs it.'},
    {'id': 'R1', 'origin': 'root termination-boundary assessment; bounded ACCEPTED-FOR-SCHEMA-LAW', 'disposition': 'CLOSED-FOR-SCHEMA-LAW',
     'finalOwnerSelectors': ['docs/coop/design-corrections/workflows/schemas/evaluator3/common.schema.json:739-1140 ($defs/StepTermination branches)', 'docs/coop/design-corrections/workflows/schemas/common.schema.json (retained predecessor, identical branch law)', 'docs/v2/contracts/product-v1/workflows-and-surfaces.md:1135-1189'],
     'evidence': {'P38-SEALQ.SCHEMA': SCH, 'evaluator3 workflow-projection child': children.get('workflow-projection')},
     'consequence': 'faultCause appears only on operational-failed, and reasonCodes only on indeterminate. Evaluator3 common admits exactly the 34 lawful combinations; the historical common admits 33 because its RunId pattern differs. No unlawful combination is admitted, and the query operation exception terminations remain admissible.'},
    {'id': 'R2', 'origin': 'root termination-boundary assessment; bounded ACCEPTED-FOR-SCHEMA-LAW', 'disposition': 'CLOSED-FOR-SCHEMA-LAW',
     'finalOwnerSelectors': ['docs/coop/design-corrections/workflows/schemas/evaluator3/common.schema.json:945-1060 (11 exact faultCause/errorCode pairs incl. host-invariant)', 'docs/coop/design-corrections/foundation/check-evaluator-faults.v3.py (separate schema and parity controls)'],
     'evidence': {'P38-SEALQ.FAULT': FS, 'evaluator3 faults child': children.get('faults')},
     'consequence': 'Across the 24 routes, an illegal pair is refused at schema admission (132 of 132) and a structurally lawful but owner-inconsistent pair is refused at owner parity (120 of 120). Zero outcomes were unexpected.'},
    {'id': 'RC37-01', 'origin': 'claude-source37-root-corrections-review.v1 (SHOULD)', 'disposition': 'CLOSED-AT-SOURCE-LEVEL',
     'finalOwnerSelectors': ['docs/coop/design-corrections/workflows/query-projection-contract.v3.md:166-173 (four typed close_run outcomes) and :186-191 (table rows)',
                             'docs/coop/design-corrections/workflows/query_projection_model.v3.py:565-597 (close_retained_run)',
                             'docs/coop/design-corrections/foundation/identity-model.v3.py:613-635 (EvidenceUnavailable, RegenerationMismatch, CompleteReplayMismatch), :654-681 (close_run normalization by exact class object), :1927 (restore maps to RegenerationMismatch)',
                             'docs/coop/design-corrections/foundation/evaluator_replay_model.v3.py:18-27 (declared UNAVAILABLE/MISMATCHES/REFUSALS)',
                             'docs/coop/design-corrections/foundation/evaluator-fault-contract.v3.md:3, 11, 15'],
     'evidence': {'P38-SEALQ.QUERY': QS},
     'consequence': 'Missing bytes route to evidence.missing, corrupt structural bytes (including an evidence-level remint refused structurally) to evidence.corrupt, and a fully reminted semantically false Run to evidence.regeneration-mismatch with the refused RunId as subject. An undeclared host exception inside the replay stack routes to SYSTEM.OUTCOME.ILLEGAL_STATE / host-invariant / HOST.INVARIANT_VIOLATED. The route is selected by class object, not text: a KeyError, and the query identity copy\'s own classes raised inside the stack, route by type, and a lawful Run admits again after restore.'},
    {'id': 'RC37-A1', 'origin': 'claude-source37-root-corrections-review.v1 (advisory)', 'disposition': 'CLOSED-AT-SOURCE-LEVEL',
     'finalOwnerSelectors': ['docs/coop/design-corrections/workflows/query-projection-contract.v3.md:162-164', 'query_projection_model.v3.py:1504-1519, 1522-1546'],
     'evidence': {'P38-SEALQ.QUERY.retainedAvailability': QS.get('retained availability'), 'maintainedControls': children.get('query-projection')},
     'consequence': 'A product adapter\'s own invalid observation with a valid RequestId terminates host-invariant, and a retained availability record failing identity availability admission is evidence.corrupt. No public code is added.'},
    {'id': 'RC37-A2', 'origin': 'claude-source37-root-corrections-review.v1 (routed to integration)', 'disposition': 'CLOSED-AT-SOURCE-LEVEL',
     'finalOwnerSelectors': ['docs/v2/architecture/implementation-normative-inputs.v6.json (30 inputs incl. run-termination-contract.v1.md)', 'implementation-coverage.v1.json subjectManifestSha256', 'implementation-planning-sources.v1.json architecture.manifestSha256', 'five source-pins ledgers'],
     'evidence': {'P38-PLAN': {'planning': P.get('check_implementation_planning', {}).get('stdout'), 'inventory': P.get('check_repository_file_inventory', {}).get('stdout'), 'counts': P.get('counts')}},
     'consequence': 'Planning and pins bind current source38 bytes; the pin gates of all six groups pass.'},
    {'id': 'RC37-A3', 'origin': 'claude-source37-root-corrections-review.v1 (advisory)', 'disposition': 'ACCEPTED-AS-DESIGNED',
     'finalOwnerSelectors': ['docs/coop/design-corrections/workflows/schemas/evaluator3/common.schema.json StepTermination request-rejected branch'],
     'evidence': {'P38-SEALQ.SCHEMA.requestRejectedCodes': SCH.get('requestRejectedCodes')},
     'consequence': 'request-rejected still admits all 19 D9ErrorCode members, which is deliberate. Class-specific error families belong to the D9 successor owner.'},
    {'id': 'RC37-A4', 'origin': 'claude-source37-root-corrections-review.v1 (editorial)', 'disposition': 'RETAINED-OPTIONAL-EDITORIAL',
     'finalOwnerSelectors': ['docs/v2/architecture/implementation-boundaries-and-build-plan.md:201 ("not a claim that candidate25 already specifies or implements that private table")'],
     'evidence': {'freshRead': 'implementation-boundaries-and-build-plan.md complete'},
     'consequence': 'This is harmless provenance wording. It could name the current normative layer at the next successor, and has no semantic effect.'},
    {'id': 'SI-1', 'origin': 'claude-source38-seal-integration-assessment.v1', 'disposition': 'CONFIRMED-RESOLVED',
     'finalOwnerSelectors': ['docs/coop/design-corrections/security/security_lifecycle_model_v1.py:1547-1550 (except IM.C.AdmissionError -> Reject(SEAL_CLOSE_RUN_REFUSED:...) from e)', 'docs/coop/design-corrections/security/check-analysis-seal-adapter.v1.py'],
     'evidence': {'rootFailedRunPreserved': 'root-final38-reference.v1 passed=false, analysis-seal child exit 1 (not relabelled)', 'evaluator3 analysis-seal child (this review)': children.get('analysis-seal')},
     'consequence': 'The typed replay mismatch no longer escapes the SEAL adapter as a host exception.'},
    {'id': 'SI-2', 'origin': 'claude-source38-seal-integration-assessment.v1', 'disposition': 'CONFIRMED-INDEPENDENTLY',
     'finalOwnerSelectors': ['security_lifecycle_model_v1.py:1527-1550', 'identity-model.v3.py:654-681'],
     'evidence': {'P38-SEALQ.SEAL': SS},
     'consequence': 'The lawful Run admits. The fully reminted false Run is refused with cause type exactly IM.CompleteReplayMismatch, chained to the replay stack\'s origin-free CompleteReplayMismatch. A structurally refused remint is refused with cause IM.C.AdmissionError. Foreign same-name classes raised by close_run propagate, as does a KeyError inside the comparison, and the lawful Run admits after restore.'},
    {'id': 'SI-3', 'origin': 'claude-source38-seal-integration-assessment.v1', 'disposition': 'CONFIRMED',
     'finalOwnerSelectors': ['security_lifecycle_model_v1.py:175 (Reject carries no termination)', 'docs/coop/design-corrections/public-detail-registry.v1.json'],
     'evidence': {'SEAL_CLOSE_RUN_REFUSED_inPublicDetailRegistry': seal_key_registered},
     'consequence': 'The security-local Reject key establishes no public origin; the outer host decides origin.'},
    {'id': 'SI-A1', 'origin': 'claude-source38-seal-integration-assessment.v1 (advisory)', 'disposition': 'CARRIED-IMPLEMENTATION-BOUNDARY-UNDER-EXISTING-FAULT-OWNER',
     'finalOwnerSelectors': ['docs/coop/design-corrections/foundation/evaluator-fault-contract.v3.md:3 (no origin from a prefix in the error text), :15 (retained regeneration versus live host-internal)',
                             'docs/v2/architecture/repository-file-inventory.v1.json crates/host/src/finalization.rs and outcomes.rs rows'],
     'evidence': {'outerLiveHostProjectionExistsInSource': False},
     'consequence': 'A product outer host must route SEAL refusals by the Reject __cause__ type, not by the embedded diagnostic text. The existing fault owner already forbids text inference, so this is an implementation obligation, not a source defect.'},
    {'id': 'SI-4', 'origin': 'claude-source38-seal-integration-assessment.v1', 'disposition': 'CONFIRMED-INDEPENDENTLY',
     'finalOwnerSelectors': ['foundation/atom_model.v1.py:897 and security/security_lifecycle_model_v1.py:1481 (the only non-test class-name matches; neither wraps close_run)', 'workflows/query_projection_model.v3.py:596 (type name used only in host-invariant diagnostic text after typed routing)'],
     'evidence': {'grep': 'type(...).__name__ comparisons across foundation/security/workflows/native *.py', 'P38-STATIC': STAT.get('results')},
     'consequence': 'No current caller depends on the changed close_run class names.'},
    {'id': 'SI-5', 'origin': 'claude-source38-seal-integration-assessment.v1 (limitation)', 'disposition': 'SUPERSEDED-BY-REBIND',
     'finalOwnerSelectors': ['docs/coop/design-corrections/security/source-pins.v1.json (rebound)'],
     'evidence': {'securityGroup (this review)': [r for r in group_rows if r['name'] == 'security']},
     'consequence': 'The pin-gated security owner suite runs and passes on source38.'},
    {'id': 'QF-1', 'origin': 'claude-source38-seal-integration-assessment.v1', 'disposition': 'CONFIRMED-INDEPENDENTLY',
     'finalOwnerSelectors': ['docs/coop/design-corrections/foundation/check-evaluator-faults.v3.py (read complete)'],
     'evidence': {'P38-SEALQ.FAULT': FS, 'faultsChild': children.get('faults')},
     'consequence': 'Both protections are retained and discriminated. The earlier failing expectation (root-final38 source37 overlay exit 1) is preserved as history, not reclassified.'},
    {'id': 'AUTHOR-V2-QUALIFICATION', 'origin': 'claude-source38-seal-integration-assessment.v1 v2Qualification', 'disposition': 'CONFIRMED-ACCURATE; v2 REPORT PRESERVED UNEDITED',
     'finalOwnerSelectors': ['identity-model.v3.py:627-635, 678-681, 1927', 'query-projection-contract.v3.md:169'],
     'evidence': {'queryFaultV2ReviewSha256': qf_v2_sha, 'rootIntegrationRecordedReviewSha256': qf_v2_expected, 'equal': qf_v2_sha == qf_v2_expected},
     'consequence': 'The v2 sentence that class names were unchanged is overbroad for replay disagreement, caller-copy classes, the query route and restore. The qualification is correct and does not rewrite the v2 record.'},
    {'id': 'ROOT38-CARRIER-GRAMMAR', 'origin': 'root-source38-dispositions.v4 rootFollowups', 'disposition': 'CLOSED-AT-SOURCE-LEVEL', 'finalOwnerSelectors': ['see A37-01'], 'evidence': {'see': 'A37-01'}, 'consequence': 'The NUL suffix and ASCII-hex BLOB holes are closed in all three encodings.'},
    {'id': 'ROOT38-HOST-PROJECTION-SCOPE', 'origin': 'root-source38-dispositions.v4 rootFollowups', 'disposition': 'CLOSED-AT-SOURCE-LEVEL (residual ADV38-01)',
     'finalOwnerSelectors': ['run-termination-contract.v1.md:23-38 (derived versus delegated members), :136-163 (carrier chosen from every condition at the primary rank)', 'crates/host/src/outcomes.rs and finalization.rs inventory rows'],
     'evidence': {'P38-TERM.workBudgetRows': [r for r in TERM['IND'] if r[0].startswith('work-budget')], 'P38-TERM.PROJ': TERM.get('PROJ')},
     'consequence': 'A combined work-budget Run with native stage carriers now names the stage carrier. Arbitrary schema-valid extras are owner-validation-required, never lawful.'},
    {'id': 'ROOT38-FAULT-CHECK-ORDER', 'origin': 'root-source38-dispositions.v4 rootFollowups', 'disposition': 'CLOSED (see QF-1)', 'finalOwnerSelectors': ['check-evaluator-faults.v3.py'], 'evidence': {'see': 'QF-1'}, 'consequence': 'None beyond QF-1.'},
    {'id': 'QF-I1', 'origin': 'claude-source37-query-fault-author.v2', 'disposition': 'CLOSED (see QF-1)', 'finalOwnerSelectors': ['check-evaluator-faults.v3.py'], 'evidence': {'see': 'QF-1'}, 'consequence': 'None beyond QF-1.'},
    {'id': 'QF-I2', 'origin': 'claude-source37-query-fault-author.v2', 'disposition': 'CLOSED (see RC37-A2)', 'finalOwnerSelectors': ['five source-pins ledgers'], 'evidence': {'see': 'RC37-A2'}, 'consequence': 'Pins are rebound.'},
]

ADVISORIES = [
    {'id': 'ADV38-01', 'severity': 'ADVISORY', 'title': 'Delegated domainDetail and attribution on an analysis termination have no closed admissibility rule in the read owners',
     'selectors': ['docs/coop/design-corrections/foundation/run-termination-contract.v1.md:23-38, 164-179', 'docs/v2/contracts/product-v1/workflows-and-surfaces.md:1135-1189',
                   'docs/v2/architecture/repository-file-inventory.v1.json crates/host/src/outcomes.rs, finalization.rs', 'implementation-coverage.v1.json workflows-and-surfaces:10 verification.method'],
     'detail': 'The termination owner admits a shape-valid but unrelated registered domainDetail on an analysis indeterminate projection (HOST.INVARIANT_VIOLATED, or a QUERY.* detail) and returns it as owner-validation-required, as its contract says. This review found no closed class-and-reason to detail admissibility table in the owners it read. The obligation is carried to host outcomes/finalization and to the §9 verification scenario.',
     'receipt': 'receipts/probe-run-termination.json#PROJ', 'disposition': 'ROUTE-TO-IMPLEMENTATION (host outcomes owner validates delegated detail and attribution); not a source defect because the owner never calls these lawful.'},
    {'id': 'ADV38-02', 'severity': 'ADVISORY', 'title': 'Read-only route for an association that names a carrier observed unmigrated (no published format row) is prose-only',
     'selectors': ['docs/coop/design-corrections/security/carrier-dispatch.v3.json:262 (readerLaws)', 'carrier-dispatch.v3.json:641-652 (unknown-carrier-incompatible observations name only grantGeneration below first_generation)', 'carrier-dispatch.v3.json:667-674 (readOnlyStandingOfDispatchResult has no carrierFormat1/carrierFormat2 entry)', 'docs/v2/contracts/product-v1/security-and-lifecycle.md:1307'],
     'detail': 'The open dispatch classifies an unmigrated carrier as carrierFormat1 or carrierFormat2. The reader law sends any association naming a format 1 or 2 generation to unknown-carrier-incompatible, but the machine observation list and dispatch-result map cover only the migrated below-first_generation case. An association naming a carrier that is unmigrated now points to lost migration, rollback or a swap, which could equally be read as custody or quarantine. Both candidate routes are non-confirming operational failures at exit 4, so fail-closed behaviour is preserved.',
     'receipt': 'receipts/probe-carrier-sql.json#DISPATCH.format2-with-association', 'disposition': 'ROUTE-TO-CARRIER-OWNER: state the route and add the observation or map entry before F46 implementation.'},
    {'id': 'ADV38-03', 'severity': 'EDITORIAL', 'title': 'commit-recovery-readonly.v3 keeps two stale scope phrases',
     'selectors': ['docs/v2/architecture/commit-recovery-readonly.v3.md:39 ("F00-F37")', 'commit-recovery-readonly.v3.md:73-75 (MIGRATION.CORRUPT "is the store transition\'s detail")', 'security-and-lifecycle.md:1300, 1310 (governing scope includes the carrierFormat 3 migration footprint at writer/maintenance open)'],
     'detail': 'The plan now holds F00-F53, and S12 extends MIGRATION.CORRUPT to the writer/maintenance carrier footprint. The read-only document\'s conclusion, that MIGRATION.CORRUPT is not used on a read-only path, is correct; only the scope description is stale.',
     'receipt': 'fresh read', 'disposition': 'EDITORIAL at the next successor; security S12 governs.'},
]
OBSERVATIONS = [
    'Replay-stack exception coverage: a module-graph walk found exception class objects outside the declared UNAVAILABLE/MISMATCHES/REFUSALS tuples (for example the identity copy\'s native load NativeRefusal/ScopeRefusal and discovery-defaults errors). Static escape analysis attempt 2 found escapes only from registry-selected inputs (NATIVE_CONTEXT_LANGUAGE), cve1_encode over already-admitted values and a Unicode case-data environment error. No retained-byte path to a misrouted owner refusal was demonstrated. Such an exception would fail closed as host-invariant.',
    'observe_retained_availability admits a schema-valid record with non-canonical key order. The query contract names identity availability schema admission, not canonical bytes, so this is recorded as an observation only.',
    'SQLite affinity conversions (integral text, boolean, 1.0 REAL) and an embedded NUL in the free-text body are admitted by the carrier DDL; carrier-format §5.1 assigns closed-record admission to the host.',
    'The historical workflows common schema admits 33 lawful termination combinations versus 34 for evaluator3 common; the difference is the retained RunId pattern, not the R1/R2 branch law.',
]

# ------------------------------------------------------------------------------------------------ 107 rows
TCB = ['RES-EP13-02', 'RES-EP13-04', 'RES-EP13-12', 'RES-EP13-13', 'RES-EP13-16', 'RES-EP13-18', 'IR-EP13-NB-01', 'IR-EP13-NB-03', 'IR-EP13-NB-04', 'AX6', 'AX9', 'MD5', 'RX2c']
RES_TEXT = {
    'RES-EP13-01': ('new-38', 'Plan/derivation joins are recomputed inside complete replay (evaluator_replay_model.v3.py:60-65, 67-89). On source38 a Plan-consistent reminted false Run passes owner closure and is refused only by replay (P38-SEALQ, P38-TERM FALSE; package semantic-controls1).'),
    'RES-EP13-02': ('new-38', 'Depends on TCB-SCOPE-01, assessed once on source38. No answer-provenance claim against adversarial in-process route regions is made.'),
    'RES-EP13-03': ('inherited-unchanged-37', 'The seven-vector measurement stays finite history. The correction text and admission §2-4 are byte-identical to source37, and no delta file changes it.'),
    'RES-EP13-04': ('new-38', 'Depends on TCB-SCOPE-01. Closed input schemas remain the product admission (StepTermination and query request enumerations in P38-SEALQ).'),
    'RES-EP13-05': ('new-38', 'This review verified the frozen subject outside every author instrument: live manifest, archive, 12,904 members and parent37 (P38-SUBJECT, P38-ARCHIVE).'),
    'RES-EP13-06': ('inherited-unchanged-37', 'canonical.py and identity §3 are unchanged. Exact typed admission still refuses float/exponent/negative-zero; carrier SQL affinity conversions are storage behaviour under host record admission, not canonical admission.'),
    'RES-EP13-07': ('new-38', 'Seal binds Plan, execution plan, evidence, proof and verdict: a predicate-flip remint with valid new identities is refused as EVALUATOR_COMPLETE_PROOF_REPLAY at SEAL and as evidence.regeneration-mismatch at query (P38-SEALQ).'),
    'RES-EP13-08': ('inherited-unchanged-37', 'Bounded historical measurement; no product proof over all PlanIntents is claimed in source38 either.'),
    'RES-EP13-09': ('new-38', 'Provenance stays distinct from correctness: reminted mutants carry valid identities and are refused only by replay (P38-SEALQ; package semantic-controls1 owner ADMIT / semantic REFUSE).'),
    'RES-EP13-10': ('new-38', 'Author self-counters did not decide this review: the six groups, planning and package were re-executed here and probes were independent.'),
    'RES-EP13-11': ('inherited-unchanged-37', 'Historical checker failures stay recorded by cause. Likewise the failed root-final38-reference.v1 run is preserved as failed and not relabelled.'),
    'RES-EP13-12': ('new-38', 'Depends on TCB-SCOPE-01. No sole Python answer-provenance guard is carried into product authority.'),
    'RES-EP13-13': ('new-38', 'Depends on TCB-SCOPE-01. This review\'s probes deep-copy fixtures before mutation (fixture isolation only).'),
    'RES-EP13-14': ('inherited-unchanged-37', 'The differential census is not used as an oracle; unchanged.'),
    'RES-EP13-15': ('inherited-unchanged-37', 'C-2 v4 self-census not elevated; plan/derivation schemas unchanged in 38.'),
    'RES-EP13-16': ('new-38', 'Depends on TCB-SCOPE-01. Producer flags cannot bypass replay (P38-SEALQ).'),
    'RES-EP13-17': ('inherited-unchanged-37', 'Text-only disclosures remain text-only.'),
    'RES-EP13-18': ('new-38', 'Depends on TCB-SCOPE-01.'),
    'RES-EP13-19': ('new-38', 'Substantive semantic review was performed on source38 with discriminating probes; pins and passing counts were not treated as acceptance.'),
    'IR-EP13-NB-01': ('new-38', 'Depends on TCB-SCOPE-01.'),
    'IR-EP13-NB-02': ('inherited-unchanged-37', 'No name/punctuation scan decides product scope; unchanged.'),
    'IR-EP13-NB-03': ('new-38', 'Depends on TCB-SCOPE-01. The replay-stack module walk confirms that loaded instances are reachable in-process, which is exactly why the boundary is trust rather than containment.'),
    'IR-EP13-NB-04': ('new-38', 'Depends on TCB-SCOPE-01; one TCB account is used.'),
    'IR-EP13-NB-05': ('inherited-unchanged-37', 'Contradictory prose requires substantive review; unchanged.'),
    'IR-EP13-NB-06': ('inherited-unchanged-37', 'Historical attacker cost preserved as history.'),
    'IR-EP13-NB-07': ('inherited-unchanged-37', 'Original environment preserved; this review names its own interpreter and pins.'),
    'AX6': ('new-38', 'Depends on TCB-SCOPE-01.'), 'AX9': ('new-38', 'Depends on TCB-SCOPE-01.'), 'MD5': ('new-38', 'Depends on TCB-SCOPE-01.'), 'RX2c': ('new-38', 'Depends on TCB-SCOPE-01.'),
}
AR_TEXT = {
    'AR-01': ('new-38', 'NO-NEW-ISSUE', 'Admission §1 is unchanged. The R1/R2 StepTermination closure was probed by exhaustive enumeration, with 34 lawful combinations admitted and none unlawful.'),
    'AR-02': ('inherited-unchanged-37', 'NO-NEW-ISSUE', 'Admission §§2-4 and qualification-gates are unchanged; all 32 gates remain unqualified.'),
    'AR-03': ('inherited-unchanged-37', 'NO-NEW-ISSUE', 'Security S3 discovery was re-read complete on source38; the security and integration groups pass.'),
    'AR-04': ('inherited-unchanged-37', 'NO-NEW-ISSUE', 'Security S4 trust time re-read complete on source38; no probe.'),
    'AR-05': ('inherited-unchanged-37', 'NO-NEW-ISSUE', 'Security S5/S6 re-read complete on source38; no probe.'),
    'AR-06': ('new-38', 'NO-NEW-ISSUE', 'The carrier DDL platform CHECK names the four S8 machine ids and refuses NUL-bearing platforms (P38-CARRIER); security group pass.'),
    'AR-07': ('inherited-unchanged-37', 'NO-NEW-ISSUE', 'Native §§3/5/9 re-read complete on source38 (the native delta is the §10 owner pointer); native group passes.'),
    'AR-08': ('inherited-unchanged-37', 'NO-NEW-ISSUE', 'The workflows-and-surfaces delta is confined to §9; repair per-requirement disclosure is unchanged.'),
    'AR-09': ('new-38', 'NO-NEW-ISSUE', 'identity-and-evidence.md is unchanged, and the reference close_run boundary now types its outcomes. A37-06 is closed by RC37-01 (P38-SEALQ).'),
    'AR-10': ('inherited-unchanged-37', 'NO-NEW-ISSUE', 'Baseline/comparison unchanged; comparison-knowledge child passes.'),
    'AR-11': ('inherited-unchanged-37', 'NO-NEW-ISSUE', 'Import wrapper and history/runtime limits unchanged; no independent import probe.'),
    'AR-12': ('inherited-unchanged-37', 'NO-NEW-ISSUE', 'Native §4 unchanged; atoms child passes.'),
    'AR-13': ('new-38', 'NO-NEW-ISSUE', 'Its 37 routing reason, S37-03, is closed at source level.'),
    'AR-14': ('new-38', 'ADVISORY-ONLY', 'A37-03 closed; ADV38-02 and ADV38-03 remain carrier/read-only advisories.'),
    'AR-15': ('new-38', 'NO-NEW-ISSUE', 'Its 37 routing reason, S37-02, is closed: report projections are data only.'),
    'AR-16': ('new-38', 'ADVISORY-ONLY', 'S37-01 closed by run-termination-contract.v1; ADV38-01 on delegated detail validation.'),
}
FW_TEXT = {
    'FW-06': ('new-38', 'The finalization row now routes the retained analysis projection through outcomes.rs and separately validates delegated attribution, detail and authority. S37-01 is closed; SI-A1 and ADV38-01 are carried to this owner.'),
    'FW-08': ('new-38', 'The outcomes row now names run-termination-contract.v1 as the derivation law. A37-05/06 are closed at the query owner (RC37-A1/RC37-01).'),
    'FW-13': ('new-38', 'S37-03 advisory registry/schema admission is closed.'),
    'FW-04': ('inherited-unchanged-37', 'Runtime/test/history stay non-Coverage per workflows §4 (re-read complete on source38); inventory row unchanged.'),
}
DR_TEXT = {
    'DR-001': ('inherited-unchanged-37', 'current-source-map and residual ledgers are unchanged; this review refreshed the reading path on source38.'),
    'DR-002': ('new-38', 'The identity/evidence/proof chain was re-probed: typed close_run outcomes and complete replay (P38-SEALQ; package 13 closures).'),
    'DR-003': ('new-38', 'The carrier v3 grammar/publication/route corrections were probed (P38-CARRIER). The 54 recovery cases remain not executed, and real platform demonstration remains a release requirement.'),
    'DR-004': ('inherited-unchanged-37', 'Native §4 and Phase-1A semantics unchanged.'),
    'DR-005': ('new-38', 'Executable custody reference groups pass on source38; native product carrier qualification is still required before release.'),
    'DR-006': ('inherited-unchanged-37', 'Descriptor graph unchanged; the full-replay child passes.'),
    'DR-007': ('new-38', 'S37-01 closed: the D9 cause reduction and coverageId join have one owner. The D9 published successor artifact remains a carried implementation-unit obligation (native §10:3133-3147; evaluator-fault-contract.v3.md:20), not a new blocker.'),
    'DR-008': ('inherited-unchanged-37', 'Applied retention posture unchanged.'),
    'DR-009': ('new-38', 'The termination projection keeps executionId delegated and outside the derived members, preserving lifetime neutrality.'),
    'DR-010': ('new-38', 'S37-02 closed: bounded first-party composition with no executable report hooks.'),
    'DR-011': ('inherited-unchanged-37', 'Individual dispositions exist; the blind implementer litmus follows final integration and is not closed here.'),
    'DR-011-R01': ('inherited-unchanged-37', 'Fact-plane successor schemas unchanged.'),
    'DR-011-R02': ('inherited-unchanged-37', 'Fact identity unchanged; arbitrary imperative plugins remain outside D-371 (admission §5 items 4-5 re-read).'),
    'DR-011-R03': ('inherited-unchanged-37', 'plan2/exec-plan2 unchanged.'),
    'DR-011-R04': ('new-38', 'The security carrierFormat axis and format-aware reader staging (S9:736-777) join the core bridge; the security group passes.'),
    'DR-011-R05': ('inherited-unchanged-37', 'Rust protocol major 3 unchanged; native group passes.'),
    'DR-011-R06': ('new-38', 'Proof mismatch is typed and restore maps it to RegenerationMismatch (identity-model.v3.py:1927).'),
    'DR-011-R07': ('new-38', 'Retained availability records and graph availability observations have typed routes (query §7:160-164; P38-SEALQ).'),
    'DR-011-R08': ('new-38', 'S37-01 closed. Branch-specific optional fields are closed by R1/R2, and the D9 published successor artifact remains carried (DR-007).'),
    'DR-011-R09': ('inherited-unchanged-37', 'Semantic IDs exclude attempt identity; unchanged.'),
    'DR-011-R10': ('inherited-unchanged-37', 'OPEN: this nonblind review cannot close the fresh blind implementer litmus.'),
    'DR-011-R11': ('new-38', 'Carrier advisories A37-01..04 are closed at source level, with ADV38-02 residual. Real platform durability is unmeasured, and the 54 cases are not executed.'),
    'DR-011-R12': ('new-38', 'Depends on TCB-SCOPE-01, assessed once on source38.'),
    'DR-011-R13': ('inherited-unchanged-37', 'Versioning successor unchanged.'),
    'DR-011-R14': ('inherited-unchanged-37', 'CFG-6/TM unchanged.'),
    'DR-011-R15': ('inherited-unchanged-37', 'Trusted request context unchanged.'),
    'DR-011-R16': ('new-38', 'S37-02 closed: no executable report-hook admission, so the bounded first-party product authority is preserved.'),
}


def row_out(r, basis, disposition, assessment, extra=None):
    o = {'id': r['id'], 'prior37Disposition': r['disposition'], 'disposition': disposition, 'assessmentBasis': basis, 'assessment': assessment}
    o.update(extra or {})
    o.update(FALSE_FLAGS)
    return o


fD = [row_out(r, 'inherited-unchanged-37', 'CARRIED-NOT-REGRADED',
              'Identifier and prior root standing ' + str(r.get('priorRootStanding')) + ' recorded from root-independent36-completion-assessment.v1, as in the source37 review. The F content lives outside the snapshot and was not re-derived, and no 37->38 delta file is an F record. The prior standing is not source38 acceptance.',
              {'priorRootStanding': r.get('priorRootStanding')}) for r in v37['fDispositions']]
eR = []
for r in v37['evaluationResidualDispositions']:
    basis, text = RES_TEXT[r['id']]
    eR.append(row_out(r, basis, 'ASSESSED-CONSISTENT-GRADE-PENDING', text + ' The historical limitation is preserved; no historical guard is claimed repaired.',
                      {'proposedDisposition': r['proposedDisposition'], 'authorGrade': 'PENDING', 'sharedDependency': 'TCB-SCOPE-01' if r['id'] in TCB else None, 'residualRetained': True}))
aR = []
for r in v37['arDispositions']:
    basis, disp, text = AR_TEXT[r['id']]
    aR.append(row_out(r, basis, disp, text, {'contract': r['contract'], 'selector': r['selector'], 'statusRecorded': r['statusRecorded'],
                                              'contractSha256': sha(S38 + '/' + r['contract'])}))
fwR = []
for r in v37['fwDispositions']:
    basis, text = FW_TEXT.get(r['id'], ('inherited-unchanged-37', 'Owner module and milestone match the unchanged current-source-map row and the unchanged inventory row; implementation not executed.'))
    fwR.append(row_out(r, basis, 'OWNER-ROUTING-ASSESSED-NOT-EXECUTED', text, {'owners': r['owners'], 'milestone': r['milestone'], 'verificationStanding': r['verificationStanding']}))
dR = []
for r in v37['inheritedResidualDispositions']:
    basis, text = DR_TEXT[r['id']]
    dR.append(row_out(r, basis, 'CONDITION-1-OBLIGATION-RETAINED-ASSESSED', text + ' The proposed successor routing in inherited-residuals.proposed.md (unchanged, re-read) is consistent with source38; original custody and standing preserved.'))
sR = [row_out(r, 'inherited-unchanged-37', 'ROUTING-ASSESSED-ONLY-NOT-APPLIED',
              'Register 08 is byte-identical to source37, so its scoped acceptance, full-product OPEN and condition-3 owner lines stand as recorded by the source37 review. The source37 issues this row related to (S37-01..03) are closed at source level on source38. This review is an input to the integrated review and is not applied.') for r in v37['scopedReviewOwnerDispositions']]
row_count = len(fD) + len(eR) + len(aR) + len(fwR) + len(dR) + len(sR)

TCB_OBJ = {
    'id': 'TCB-SCOPE-01', 'assessedOnceAsOneAssumption': True,
    'assumption': v37['tcbScopeAccount']['assumption'],
    'consequence': 'Rejecting or changing the assumption reopens all thirteen dependent rows together. It is a scope selection, not a containment guarantee, and repairs no historical attack. All thirteen author grades stay PENDING.',
    'dependentRows': TCB, 'dependentRowCount': len(TCB),
    'substantiveCurrentAssessment': [
        'Coherent as a scope selection on source38. Admission §5 is byte-identical: item 4 admits no untrusted native/WASM and claims no sandbox; item 5 admits no imperative contributions or project hooks (admission-and-qualification.md:344-345).',
        'The source37 inconsistency is removed. prototype-report-inventory.md:37 and :179 now select versioned host-approved data projections with no executable report-hook admission, and coverage R02/R24 are rebound.',
        'What the assumption relies on was re-probed on source38. A fully reminted false Run passes owner closure and is refused only by complete replay (SEAL cause IM.CompleteReplayMismatch; query evidence.regeneration-mismatch; package semantic-controls1 owner ADMIT / semantic REFUSE).',
        'The typed boundary itself assumes trusted in-process code. close_run normalizes by exact class object, foreign same-name classes propagate, and undeclared exceptions fail closed as host-invariant. Adversarial code in the same process could raise identity classes directly, which is exactly what the assumption excludes.',
        'It remains unqualified. It rests on the authenticated closure/TCB inventory and provider process boundaries (DR-G29/G30 and related gates), and all 32 gates are unperformed.',
    ],
    'standing': 'ASSESSED-COHERENT-UNQUALIFIED-ON-SOURCE38; final application adjudication not granted',
    'adjudicationOwner': 'Separate final application review by a fresh other origin excluding all 11 author, design and blind origins; not adjudicated here.',
    'prior37Standing': v37['tcbScopeAccount']['standing'],
}
TCB_MAP = {
    'source37ReportUnchanged': True, 'source37ReviewJsonSha256': sha(B + '/claude-independent-design.v37/review.json'),
    'fieldMapping37to38': {'id': 'id', 'assessedOnce': 'assessedOnceAsOneAssumption', 'dependentResidualIds': 'dependentRows (+ dependentRowCount)', 'assumption': 'assumption (text carried verbatim)',
                           'assessment': 'substantiveCurrentAssessment (re-assessed on source38, not copied)', 'standing': 'standing (new) with the 37 value preserved in prior37Standing; consequence and adjudicationOwner made explicit'},
}

# ------------------------------------------------------------------------------------------------ build corrections
# (1) child summaries also carry case/mismatch counts (analysis-seal has 16 cases and no top-level count key)
for f in sorted(glob.glob(REC + '/reference/evaluator3/*.stdout')):
    name = os.path.basename(f)[:-7]
    try:
        d = J(f)
    except Exception:
        continue
    for lk in ('cases', 'mismatches'):
        if isinstance(d.get(lk), (list, dict)):
            children.setdefault(name, {})[lk] = len(d[lk])
# (2) the attempt glob also matched the attempt-custody delta diff, which is not a failure
preserved = [p for p in preserved if '/delta-diffs/' not in p]
# (3) exact per-encoding carrier accounting and the measured route claim
for it in ITEMS:
    if it['id'] == 'A37-01':
        it['consequence'] = ('In each of the UTF-8, UTF-16le and UTF-16be carriers the probe offered 26 values. All 16 hostile grammar values '
                             '(uppercase, zero-width, fullwidth, NUL-tail and leading-space hex and prefixes, BLOB, NaN and overflowing sequence, unknown record type) were refused. '
                             'The 10 admitted values are 2 lawful controls (REV, SEAL), 7 documented SQLite affinity conversions (integral or leading-space integral text sequence, '
                             'boolean grantGeneration, text record_schema, 1.0 REAL or text first_generation, 1.0 REAL chain_law) and 1 NUL-suffixed free-text body. '
                             'carrier-format §5.1 leaves closed-record admission of that body to the host; this review treats that as the stated boundary, not a defect.')
    if it['id'] == 'A37-04':
        it['consequence'] = ('F46 and F51 have public projections, and all 9 phase routes in publicProjectionByPhase are schema-valid StepTerminations in the probe (ROUTES 9/9 VALID). '
                             'Format-1 rows after TERMINAL and a UTF-16 F51 carrier are detected as split-brain (writer MIGRATION.CORRUPT; read-only quarantine requiring stable observations).')
        it['evidence']['P38-CARRIER.ROUTES'] = CAR.get('ROUTES')
# (4) the SEAL integration assessment origin is recorded in its review/process records, not as a bare process value
seal_text = open(B + '/claude-source38-seal-integration-assessment.v1/review.json', encoding='utf-8').read() + json.dumps(proc)
seal_origin = sorted(set(re.findall(r'f561[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', seal_text)))
for e in EVIDENCE:
    if e['path'].endswith('claude-source38-seal-integration-assessment.v1/review.json'):
        e['note'] = 'actual Claude SEAL/fault integration assessment by query-fault coauthor origin ' + ', '.join(seal_origin) + ' (NONBLIND coauthor; SI-1..5, SI-A1, QF-1, v2 qualification)'

# ------------------------------------------------------------------------------------------------ assemble
must, should = [], []
verdict = 'ACCEPT' if not must and not should and not uncovered_delta and not changed_not_fresh and not GAPS else 'CHANGES_REQUIRED'
review = {
    'schema': 'opensip.independent-design-review.source38.v1',
    'reviewer': 'Claude (independent design review origin 85a08aec-9d22-4ac6-8ec2-c10170e727d7; third charter; authored none of the reviewed bytes)',
    'standing': 'Substantive independent source-level review of frozen source38. Not inheritance of source37 acceptance, not blind reconstruction, not application, readiness, implementation authorization or product qualification.',
    'verdict': verdict,
    'verdictBasis': 'No MUST or SHOULD issue is unresolved. S37-01/02/03, A37-01..08, R1/R2, RC37-01 and RC37-A1..A3 are closed or accepted as designed on source38 by complete owner reads and independent discriminating probes; RC37-A4 stays optional editorial. Three advisories (ADV38-01..03) and SI-A1 are non-blocking and routed. Required actions ran to completion: subject/archive/member/parent/delta verification, six pinned groups, planning and inventory checks, package15 verification and probes. Source-level acceptance only.',
    'subjectManifestPath': LIVE38, 'subjectManifestSha256': SV.get('manifest38Sha256'),
    'verifiedManifest': bool(SV.get('manifest38Matches') and SV.get('snapshot', {}).get('verified') and live_sha == SV.get('manifest38Sha256')),
    'liveManifestSha256Measured': live_sha, 'subjectArchiveSha256': '571aad4d2038bcc02b13cfbab48d64ea1ce2255429badff5504432bb90175abd',
    'archiveVerification': archives, 'subjectFileCount': SV.get('fileCount38'), 'subjectTotalBytes': SV.get('totalBytes38'),
    'parentManifestSha256': SV.get('manifest37Sha256'), 'parentVerified': SV.get('manifest37Matches'), 'delta37to38': delta_counts,
    'predecessorsPreserved': {
        'source37Review': {'path': B + '/claude-independent-design.v37/review.json', 'sha256': sha(B + '/claude-independent-design.v37/review.json'), 'verdict': v37['verdict'], 'modifiedByThisReview': False},
        'boundedRootCorrectionsReview': {'path': B + '/claude-source37-root-corrections-review.v1/review.json', 'sha256': bounded_sha, 'rootRecordedSha256': bounded_expected, 'equal': bounded_sha == bounded_expected, 'outcome': 'PARTIAL', 'modifiedByThisReview': False},
    },
    'readScope': {'fresh38Read': fresh, 'fresh38DeltaRead': delta_reads, 'inheritedUnchanged37Read': inherited,
                  'changed37ReadNotFreshComplete': changed_not_fresh, 'deltaFilesWithoutReadEntry': uncovered_delta,
                  'rule': 'Whole-file claims are made only for fresh38Read and inheritedUnchanged37Read. fresh38DeltaRead is a complete 37->38 diff plus named ranges, not a whole-file read.'},
    'newMustIssues': must, 'newShouldIssues': should, 'advisories': ADVISORIES, 'observations': OBSERVATIONS,
    'itemDispositions': ITEMS,
    'probes': PROBES, 'preservedFailures': preserved,
    'commandReceipts': {'referenceGroups': group_rows, 'referenceGroupsPassed': G.get('passed'), 'evaluator3Children': children,
                        'planning': {k: P.get(k) for k in ('check_implementation_planning', 'check_repository_file_inventory')}, 'planningCounts': P.get('counts'),
                        'packageVerification': {'receipt': 'receipts/package-verification/verification.json', 'sha256': sha(REC + '/package-verification/verification.json'), 'passed': PK.get('passed'),
                                                'groups': [{k: g.get(k) for k in ('group', 'count', 'passed', 'negativeControls', 'exitCode', 'reportSha256')} for g in PK.get('groups', [])]}},
    'rootAndAuthorEvidence': {'standing': 'NONBLIND author/root evidence, not acceptance. The dispositions v4 ledger predates the completed SEAL integration assessment and the final bindings, so later receipts were assessed directly.',
                              'records': EVIDENCE, 'sealIntegrationOriginMentions': seal_origin},
    'planningLayer': {'normativeInputsV6Sha256': P.get('counts', {}).get('v6Sha256'), 'inputs': P.get('counts', {}).get('v6Inputs'), 'paths': P.get('counts', {}).get('inventoryPaths'),
                      'packages': P.get('counts', {}).get('inventoryPackages'), 'mappings': P.get('counts', {}).get('coverageMappings'), 'plannedRecoveryCasesUnexecuted': 54,
                      'milestones': 'M0-M6', 'runTerminationContractPinnedAsIncorporatedOwner': True},
    'mapSources': map_sources,
    'fDispositions': fD, 'evaluationResidualDispositions': eR, 'arDispositions': aR, 'fwDispositions': fwR,
    'inheritedResidualDispositions': dR, 'scopedReviewOwnerDispositions': sR, 'dispositionRowCount': row_count,
    'sharedAssumptionTCBSCOPE01': TCB_OBJ, 'tcbScopeAccountTransition': TCB_MAP,
    'packageAssessment': {'package': '/tmp/opensip-design-corrections/claude-author-package-successor.v15', 'artifactManifestSha256': pkg_manifest_sha,
                          'expectedManifestSha256': '6a8d4feca9db7ea48e91debf3a080415f769ac7271b8bf67df145263148b701e',
                          'verificationSha256': sha(REC + '/package-verification/verification.json'), 'expectedVerificationSha256': '204742347ae79a5f5d3bbe86a2f7f44e7eba9406b1a32d89f1c71870c334499c',
                          'constructionProvenance': pkg_binding.get('constructionSourceVersion'), 'exportsChanged': pkg_binding.get('exportsChanged'),
                          'result': 'All 13 Run/control structural and full-replay checks and all 7 query checks passed against source38 on a verified copy.',
                          'limits': ['Mixed construction provenance: TypeScript-derived groups are source33 constructions and normalized/Rust groups are source30 constructions, bound to source38 without remint.',
                                     'A9/A10 partial-helper limits (package README): only the TypeScript checkpoint compares a partial consumer helper with the owner; six positives are owner-derived/replayed self-consistency; the helper exercises exists/none, leaves and/or/not unexercised and count-at-most/all-covered unimplemented; two-binding construction is incomplete with a single explicit binding.',
                                     'No identity remint and no consumer artifact repair were performed. Binding alone proves nothing, and author proposals grant no grades.',
                                     'No compiler, provider, OS or process-isolation qualification.']},
    'retained': {'residuals': 30, 'authorGradesPending': 30, 'condition2Obligations': 28, 'condition2Source': 'docs/v2/architecture/08-decision-and-readiness-register.md:385-391 (unchanged 37->38)',
                 'qualificationGatesUnperformed': 32, 'qualificationGatesQualifiedTrue': gates_qualified_true, 'recoveryCasesNotExecuted': 54,
                 'd9PublishedSuccessor': 'Carried implementation-unit obligation (DR-007 / DR-011-R08); not a new blocker.',
                 'finalApplication': 'Must be a fresh other origin excluding all 11 author, design and blind origins.'},
    'authority': {'gradeGranted': False, 'activationGranted': False, 'implementationAuthorized': False, 'blindReconstructionClaimed': False,
                  'source37AcceptanceInherited': False, 'frozenInputsModified': False, 'applicationOrReadinessGranted': False},
    'limitations': [
        'Nonblind review. The reviewer read author packages, author and root receipts and prior reviews. No original or current blind consumer artifact, author blind diagnosis or root replay oracle was accessed.',
        'Reference Python models over synthetic native-admitted inputs; no product code exists. No compiler, provider, host, OS durability, process isolation or crypto is qualified. All 32 gates are unperformed and the 54 recovery cases are not executed.',
        'Large changed reference code and ledgers (identity-model.v3.py, security_lifecycle_model_v1.py, query_projection_model.v3.py, checkers, pins, coverage, planning sources, inventory) were read as complete 37->38 diffs plus named ranges, and several were executed. They are listed under fresh38DeltaRead and are not claimed as whole-file reads.',
        'Host-defect and foreign-class cases are in-process monkeypatches, always restored. Carrier probes ran on the reference interpreter\'s SQLite only.',
        'Static escape analysis is syntactic; the replay-stack coverage walk demonstrates class objects, not retained-byte reachability.',
        'Probe attempts with harness or probe defects are preserved beside the reruns (preservedFailures) and were not counted as results.',
        'F-01..F-14 content lives outside the snapshot and was not re-derived.',
        'No grade, activation, application, readiness or implementation authorization is granted. The 30 residuals, 28 condition-2 obligations and the D9 successor obligation are retained.',
    ],
    'buildGaps': GAPS,
    'receiptInventory': inventory,
}

with open(RT + '/review.json', 'w', encoding='utf-8') as fh:
    json.dump(review, fh, indent=1, ensure_ascii=False)
    fh.write('\n')

# ------------------------------------------------------------------------------------------------ markdown
L = []
A = L.append
A('# Independent design review: frozen source38')
A('')
A('**Verdict: ' + verdict + '** (source level only; not blind reconstruction, application, readiness or product qualification).')
A('')
A(review['verdictBasis'])
A('')
A('## Subject')
A('')
A('- Manifest: `' + LIVE38 + '`, SHA-256 `' + str(review['subjectManifestSha256']) + '`; measured live SHA `' + str(live_sha) + '`; verifiedManifest=' + str(review['verifiedManifest']) + '.')
A('- Archive `571aad4d...`; ' + str(review['subjectFileCount']) + ' files, ' + str(review['subjectTotalBytes']) + ' bytes; parent37 `245ef613...` verified=' + str(review['parentVerified']) + '; delta ' + json.dumps(delta_counts) + '.')
A('- The source37 review (CHANGES_REQUIRED) and the bounded root-corrections review (PARTIAL, SHA equal to the root-recorded value: ' + str(bounded_sha == bounded_expected) + ') are preserved unchanged.')
A('')
A('## Issues')
A('')
A('No new MUST or SHOULD issue.')
A('')
for adv in ADVISORIES:
    A('### ' + adv['id'] + ' (' + adv['severity'] + '): ' + adv['title'])
    A('')
    A(adv['detail'])
    A('')
    A('- Selectors: ' + '; '.join('`' + s + '`' for s in adv['selectors']))
    A('- Receipt: `' + adv['receipt'] + '`')
    A('- Disposition: ' + adv['disposition'])
    A('')
A('### Observations (not issues)')
A('')
for o in OBSERVATIONS:
    A('- ' + o)
A('')
A('## Item dispositions')
A('')
for it in ITEMS:
    A('### ' + it['id'] + ': ' + it['disposition'])
    A('')
    A('Origin: ' + it['origin'] + '.')
    A('')
    A(it['consequence'])
    A('')
    A('Owner selectors:')
    for s in it['finalOwnerSelectors']:
        A('- `' + s + '`')
    A('')
A('## Probes and command receipts')
A('')
for pr in PROBES:
    A('- **' + pr['id'] + '** `' + pr['script'] + '`: ' + pr['claim'] + ' Receipts: ' + ', '.join('`' + r + '`' for r in pr['receipts']))
A('')
A('Reference groups (reference interpreter `-I -B`, verified disposable copy):')
A('')
A('| Group | Exit | Seconds | Copy unchanged |')
A('|---|---|---|---|')
for r in group_rows:
    A('| ' + r['name'] + ' | ' + str(r['exitCode']) + ' | ' + str(r['seconds']) + ' | ' + str(r['copyUnchangedAfter']) + ' |')
A('')
A('Evaluator3 children: ' + ', '.join(k + ' ' + json.dumps(v) for k, v in children.items()))
A('')
A('Planning: `' + str(P.get('check_implementation_planning', {}).get('stdout', '')).strip() + '`; inventory: `' + str(P.get('check_repository_file_inventory', {}).get('stdout', '')).strip() + '`.')
A('')
A('Preserved failed probe attempts: ' + ', '.join('`' + p + '`' for p in preserved) + '.')
A('')
A('Root reference `root-final38-reference.v1` failed (analysis-seal child exit 1) and stays a failure; `root-final38-reference.v2` and the bound report `94b54adc...` are evidence only.')
A('')
A('## Package15')
A('')
pa = review['packageAssessment']
A('- Manifest `' + str(pa['artifactManifestSha256']) + '` (expected equal: ' + str(pa['artifactManifestSha256'] == pa['expectedManifestSha256']) + '); verification `' + str(pa['verificationSha256']) + '` (expected equal: ' + str(pa['verificationSha256'] == pa['expectedVerificationSha256']) + ').')
A('- ' + pa['result'])
for lim in pa['limits']:
    A('- ' + lim)
A('')
A('## TCB-SCOPE-01 (one shared assumption, ' + str(TCB_OBJ['dependentRowCount']) + ' dependent rows)')
A('')
A('Assumption: ' + TCB_OBJ['assumption'])
A('')
for s in TCB_OBJ['substantiveCurrentAssessment']:
    A('- ' + s)
A('')
A('Consequence: ' + TCB_OBJ['consequence'] + ' Adjudication owner: ' + TCB_OBJ['adjudicationOwner'])
A('')
A('Dependent rows: ' + ', '.join(TCB) + '. The source37 `tcbScopeAccount` is unchanged; field mapping 37->38: ' + json.dumps(TCB_MAP['fieldMapping37to38']) + '.')
A('')
A('## Disposition rows (' + str(row_count) + ')')
A('')
for title, rows in (('F', fD), ('Evaluation residuals', eR), ('AR', aR), ('FW', fwR), ('Inherited residuals', dR), ('Scoped review owners', sR)):
    A('### ' + title)
    A('')
    for r in rows:
        extra = (' [author grade PENDING]' if r.get('authorGrade') else '') + (' [depends on TCB-SCOPE-01]' if r.get('sharedDependency') else '')
        A('- **' + r['id'] + '** ' + r['disposition'] + ' (' + r['assessmentBasis'] + ')' + extra + ': ' + r['assessment'])
    A('')
A('Every row: appliedByThisReview=false, finalApplicationOutcomeGranted=false.')
A('')
A('## Read scope')
A('')
A('Fresh complete reads (source38):')
for e in fresh:
    A('- `' + e['path'] + '` ' + str(e['sha256'])[:16] + ' (' + str(e['lines']) + ' lines): ' + e['note'])
A('')
A('Fresh delta reads (complete 37->38 diff plus ranges; not whole-file):')
for e in delta_reads:
    A('- `' + e['path'] + '` ' + str(e['sha256'])[:16] + ': ' + e['note'])
A('')
A('Inherited unchanged from the source37 complete read (hash recomputed):')
for e in inherited:
    A('- `' + e['path'] + '` ' + str(e['sha256'])[:16])
if changed_not_fresh or uncovered_delta:
    A('')
    A('Scope gaps: ' + json.dumps({'changed37ReadNotFreshComplete': changed_not_fresh, 'deltaFilesWithoutReadEntry': uncovered_delta}))
A('')
A('## Retained obligations and authority')
A('')
for k, v in review['retained'].items():
    A('- ' + k + ': ' + str(v))
A('- Authority: ' + json.dumps(review['authority']))
A('')
A('## Limitations')
A('')
for lim in review['limitations']:
    A('- ' + lim)
if GAPS:
    A('')
    A('Build gaps: ' + json.dumps(GAPS))
with open(RT + '/review.md', 'w', encoding='utf-8') as fh:
    fh.write('\n'.join(L) + '\n')

print(json.dumps({'verdict': verdict, 'rows': row_count, 'gaps': GAPS, 'uncoveredDelta': uncovered_delta, 'changedNotFresh': changed_not_fresh,
                  'verifiedManifest': review['verifiedManifest'], 'liveSha': live_sha, 'pkgManifestEqual': pkg_manifest_sha == review['packageAssessment']['expectedManifestSha256'],
                  'pkgVerificationEqual': review['packageAssessment']['verificationSha256'] == review['packageAssessment']['expectedVerificationSha256'],
                  'boundedEqual': bounded_sha == bounded_expected, 'qfV2Equal': qf_v2_sha == qf_v2_expected, 'sealKeyRegistered': seal_key_registered,
                  'nativeSchemaSame': native_schema_same, 'gatesQualifiedTrue': gates_qualified_true, 'gateRows': len(gate_rows), 'children': children,
                  'groupsPassed': G.get('passed'), 'indEqual': ind_equal, 'mapSources': map_sources, 'sealOrigin': seal_origin,
                  'reviewJsonSha256': sha(RT + '/review.json'), 'reviewMdSha256': sha(RT + '/review.md')}, indent=1))
