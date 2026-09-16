"""Shared StepTermination boundary probe over ONE disposable copy (baseline or edited).

Loads the copy's own models and schemas. Records observations only; the retained-law predicate below is the
assessor's transcription of d9-exit-contract.v1.14 codeDerivation / X1 / X3 / X4 / codeMaps with the successor
host-invariant member taken from workflows_model.FAULT_TO_ERROR, and it is reported beside, never instead of,
each actual boundary outcome.
"""
import hashlib, importlib.util, json, types
from pathlib import Path

BASE = Path('/tmp/opensip-design-corrections/claude-source37-termination-boundary-assessment.v1')
E3 = 'urn:opensip:product-v1:workflows:evaluator3:'
DETAIL = {'code': 'CONFIG.INVALID', 'remedy': 'probe detail'}


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def outcome(fn, returns=False):
    try:
        value = fn()
        row = {'observed': 'RETURNS' if returns else 'ADMIT'}
        if returns or value is not None:
            row['value'] = value
        return row
    except Exception as exc:
        row = {'observed': 'REFUSE', 'exception': type(exc).__name__, 'reason': (str(exc).splitlines() or [''])[0][:240]}
        if exc.__cause__ is not None:
            row['cause'] = type(exc.__cause__).__name__ + ': ' + (str(exc.__cause__).splitlines() or [''])[0][:240]
        return row


def modules(copy_name):
    root = BASE / 'disposable' / copy_name
    dc = root / 'docs/coop/design-corrections'
    m = types.SimpleNamespace(root=root, dc=dc)
    m.P = load(copy_name + '_projection3', dc / 'workflows/workflow_projection_model.v3.py')
    m.W = load(copy_name + '_workflows1', dc / 'workflows/workflows_model.v1.py')
    m.F = load(copy_name + '_fault3', dc / 'foundation/evaluator_fault_model.v3.py')
    m.H = load(copy_name + '_host', dc / 'integration-host-model.py')
    m.N = m.H.N
    m.D9 = json.loads((root / 'docs/coop/artifacts/d9-exit-contract.v1.14.json').read_text())
    m.CONST = json.loads((dc / 'workflows/workflow-cases.v1.json').read_text())['constants']
    return m


def legality(m, t):
    """(required, advisory) retained class/code violations of one termination-shaped value."""
    cls, required, advisory = t.get('class'), [], []
    if 'faultCause' in t and cls != 'operational-failed':
        required.append('X3/X4: faultCause present outside operational-failed')
    if 'reasonCodes' in t and cls != 'indeterminate':
        required.append('X1/codeDerivation: reasonCodes present outside indeterminate')
    if 'errorCode' in t and cls not in ('request-rejected', 'operational-failed'):
        required.append('codeDerivation: errorCode present on a class that carries no errorCode')
    if cls == 'operational-failed' and m.W.FAULT_TO_ERROR.get(t.get('faultCause')) != t.get('errorCode'):
        required.append('codeDerivation/codeMaps: operational-failed errorCode != map(faultCause)')
    if cls == 'request-rejected' and t.get('errorCode') not in set(m.D9['codeMaps']['rejectionCauseToErrorCode'].values()):
        advisory.append('codeDerivation/codeMaps: request-rejected errorCode outside rejectionCauseToErrorCode image')
    return required, advisory


RP = ['COVERAGE.PROVIDER_UNAVAILABLE']
CASES = [
    # root-observed combinations
    ('root', 'success-plus-faultCause', {'class': 'success', 'faultCause': 'host-io'}),
    ('root', 'fault-plus-deficiency', {'class': 'operational-failed', 'errorCode': 'HOST.IO_FAILURE', 'faultCause': 'host-io', 'reasonCodes': RP}),
    ('root', 'indeterminate-plus-faultCause', {'class': 'indeterminate', 'reasonCodes': RP, 'faultCause': 'host-io'}),
    ('root', 'policy-plus-reasonCodes', {'class': 'policy-failed', 'authority': 'ephemeral', 'reasonCodes': RP}),
    # same retained law, other classes
    ('extra', 'success-plus-faultCause-none', {'class': 'success', 'faultCause': 'none'}),
    ('extra', 'policy-plus-faultCause', {'class': 'policy-failed', 'authority': 'ephemeral', 'faultCause': 'host-io'}),
    ('extra', 'rejected-plus-faultCause', {'class': 'request-rejected', 'errorCode': 'CONFIG.INVALID', 'faultCause': 'host-io'}),
    ('extra', 'rejected-plus-reasonCodes', {'class': 'request-rejected', 'errorCode': 'CONFIG.INVALID', 'reasonCodes': RP}),
    ('extra', 'interrupted-plus-faultCause', {'class': 'interrupted', 'signal': 'SIGINT', 'faultCause': 'host-io'}),
    ('extra', 'interrupted-plus-reasonCodes', {'class': 'interrupted', 'signal': 'SIGINT', 'reasonCodes': RP}),
    # pairing
    ('pairing', 'fault-pair-mismatch', {'class': 'operational-failed', 'errorCode': 'HOST.IO_FAILURE', 'faultCause': 'ledger-busy'}),
    ('pairing', 'fault-with-rejection-code', {'class': 'operational-failed', 'errorCode': 'CONFIG.INVALID', 'faultCause': 'host-io'}),
    ('pairing', 'fault-with-unmapped-illegal-state-borrowing-host-io', {'class': 'operational-failed', 'errorCode': 'SYSTEM.OUTCOME.ILLEGAL_STATE', 'faultCause': 'host-io'}),
    ('advisory', 'rejected-with-fault-code', {'class': 'request-rejected', 'errorCode': 'HOST.IO_FAILURE'}),
    # lawful controls
    ('lawful', 'fault-only', {'class': 'operational-failed', 'errorCode': 'HOST.IO_FAILURE', 'faultCause': 'host-io'}),
    ('lawful', 'host-invariant', {'class': 'operational-failed', 'errorCode': 'SYSTEM.OUTCOME.ILLEGAL_STATE', 'faultCause': 'host-invariant'}),
    ('lawful', 'success-bare', {'class': 'success'}),
    ('lawful', 'success-with-detail', {'class': 'success', 'domainDetail': {'code': 'DOCTOR.DEFECTS_FOUND', 'remedy': 'inspect'}}),
    ('lawful', 'policy-ephemeral', {'class': 'policy-failed', 'authority': 'ephemeral'}),
    ('lawful', 'rejected-config', {'class': 'request-rejected', 'errorCode': 'CONFIG.INVALID'}),
    ('lawful', 'indeterminate-two-reasons', {'class': 'indeterminate', 'reasonCodes': ['COVERAGE.PROVIDER_UNAVAILABLE', 'COVERAGE.BUDGET_EXHAUSTED']}),
    ('lawful', 'interrupted-sigint', {'class': 'interrupted', 'signal': 'SIGINT'}),
    # already-refused controls (the validators are live)
    ('existing-refusal', 'fault-plus-unknown-extra', {'class': 'operational-failed', 'errorCode': 'HOST.IO_FAILURE', 'faultCause': 'host-io', 'unknown': True}),
    ('existing-refusal', 'success-plus-errorCode', {'class': 'success', 'errorCode': 'HOST.IO_FAILURE'}),
    ('existing-refusal', 'fault-cause-none', {'class': 'operational-failed', 'errorCode': 'HOST.IO_FAILURE', 'faultCause': 'none'}),
]
for cause, error in [('host-io', 'HOST.IO_FAILURE'), ('ledger-busy', 'LEDGER.BUSY_TIMEOUT'), ('ledger-corrupt', 'LEDGER.CORRUPT'),
                     ('cas-link', 'CAS.LINK_FAILED'), ('provider-protocol', 'PROVIDER.PROTOCOL_VIOLATION'),
                     ('durability-commit', 'DURABILITY.COMMIT_FAILED'), ('delivery-required', 'DELIVERY.REQUIRED_FAILED'),
                     ('output-serialization', 'OUTPUT.SERIALIZATION_FAILED'), ('extension-install-io', 'EXTENSION.INSTALL_IO_FAILED'),
                     ('serve-protocol', 'SERVE.PROTOCOL_FAULT'), ('host-invariant', 'SYSTEM.OUTCOME.ILLEGAL_STATE')]:
    CASES.append(('lawful', 'fault-pair.' + cause, {'class': 'operational-failed', 'errorCode': error, 'faultCause': cause}))


def boundary_calls(m, t):
    req = m.CONST['REQ']
    env3 = {'schemaFamily': 'opensip.product.envelope', 'schemaMajor': 3, 'kind': 'failure', 'requestId': req,
            'termination': t, 'exitCode': m.W.EXIT.get(t.get('class'), 4), 'errors': [DETAIL]}
    env2 = dict(env3, schemaMajor=2)
    return {
        'evaluator3.common:3#StepTermination (validate_profile)':
            lambda: m.P.validate_profile(E3 + 'common:3#/$defs/StepTermination', t),
        'workflows.common#StepTermination (validate_import_record)':
            lambda: m.W.validate_import_record('workflows/schemas/common.schema.json', '#/$defs/StepTermination', t),
        'evaluator3.command-envelope:3 kind=failure (validate_profile)':
            lambda: m.P.validate_profile(E3 + 'command-envelope:3', env3),
        'workflows.command-envelope major2 kind=failure (validate_import_record)':
            lambda: m.W.validate_import_record('workflows/schemas/command-envelope.schema.json', '', env2),
        'evaluator3.graph-query:3 GraphQueryResponseV1.termination (validate_profile)':
            lambda: m.P.validate_profile(E3 + 'graph-query:3#/$defs/GraphQueryResponseV1/properties/termination', t),
        'evaluator3.invocation:3 StepResult.termination (validate_profile)':
            lambda: m.P.validate_profile(E3 + 'invocation:3#/$defs/StepResult/properties/termination', t),
        'workflows.invocation-record StepResult.termination (validate_import_record)':
            lambda: m.W.validate_import_record('workflows/schemas/invocation-record.schema.json', '#/$defs/StepResult/properties/termination', t),
    }


def case_rows(m):
    rows = []
    for group, name, t in CASES:
        required, advisory = legality(m, t)
        results = {k: outcome(fn) for k, fn in boundary_calls(m, t).items()}
        results['workflows_model.exit_code (class-only table)'] = outcome(lambda: m.W.exit_code(t), returns=True)
        rows.append({'group': group, 'name': name, 'input': t, 'retainedLawRequired': required,
                     'retainedLawAdvisory': advisory, 'boundaries': results})
    return rows


def producer_rows(m):
    rows = []

    def add(producer, key, res):
        row = {'producer': producer, 'key': key, 'outcome': res['observed']}
        if res['observed'] in ('ADMIT', 'RETURNS') and isinstance(res.get('value'), dict):
            row['termination'] = res['value']
            row['required'], row['advisory'] = legality(m, res['value'])
        elif res['observed'] == 'REFUSE':
            row['refusal'] = res.get('reason')
        rows.append(row)

    for key, route in m.F.ROUTES.items():
        add('evaluator_fault_model.ROUTES', key, {'observed': 'RETURNS', 'value': route['termination']})
    for key, row in m.N.PUBLIC_ROUTE_REGISTRY['keys'].items():
        if row.get('notATermination'):
            continue
        origins = list(row['byOriginatingBoundary']) if row['originDependent'] else [None]
        for origin in origins:
            add('native_evidence_model.public_termination_for', key + '@' + str(origin),
                outcome(lambda: m.N.public_termination_for(key, origin), returns=True))
    observations = [{'event': 'operational-fault', 'faultCause': c} for c in m.W.FAULT_TO_ERROR]
    observations += [{'event': 'completed-analysis', 'verdict': v} for v in ('fail', 'indeterminate', 'pass')]
    observations += [{'event': e} for e in ('provider-unavailable', 'baseline-unsupported', 'query-completeness-unmet', 'query-success', 'mutation-completed')]
    observations += [{'event': 'rejected', 'errorCode': 'CONFIG.INVALID'}, {'event': 'interrupted', 'signal': 'SIGINT'},
                     {'event': 'doctor-report', 'reportProduced': False}, {'event': 'doctor-report', 'reportProduced': True, 'defectsFound': 1}]
    for obs in observations:
        add('workflows_model.terminate', json.dumps(obs, sort_keys=True), outcome(lambda: m.W.terminate(obs), returns=True))
    vocab = m.D9['codeVocabulary']
    input_rows = []
    for cls, exit_code in m.W.EXIT.items():
        for code in [None] + vocab['errorCodes'] + vocab['reasonCodes']:
            d9 = {'class': cls, 'code': code, 'exit': exit_code}
            res = outcome(lambda: m.H.public_termination(d9, 'CONFIG.INVALID', 'probe'), returns=True)
            add('integration-host-model.public_termination', json.dumps(d9, sort_keys=True), res)
            if res['observed'] == 'RETURNS' and code is not None and cls in ('success', 'policy-failed', 'interrupted'):
                input_rows.append({'d9Input': d9, 'emitted': res['value']})
    return rows, input_rows


def fixture_scan(m):
    props = set(json.loads((m.dc / 'workflows/schemas/evaluator3/common.schema.json').read_text())['$defs']['StepTermination']['properties'])
    scanned, flagged = 0, []
    files = sorted(m.dc.rglob('*.json')) + [m.root / 'docs/coop/artifacts/d9-exit-contract.v1.14.json']
    for path in files:
        try:
            doc = json.loads(path.read_text())
        except Exception:
            continue

        def walk(o, ptr):
            nonlocal scanned
            if isinstance(o, dict):
                if (isinstance(o.get('class'), str) and o['class'] in m.W.EXIT and set(o) <= props | {'details'}
                        and set(o) & {'errorCode', 'faultCause', 'reasonCodes', 'signal', 'runId', 'authority'}):
                    scanned += 1
                    required, advisory = legality(m, o)
                    if required or advisory:
                        flagged.append({'file': str(path.relative_to(m.root)), 'pointer': ptr, 'value': o,
                                        'required': required, 'advisory': advisory,
                                        'negativeVector': '/reject' in ptr})
                for k, v in o.items():
                    walk(v, ptr + '/' + str(k))
            elif isinstance(o, list):
                for i, v in enumerate(o):
                    walk(v, ptr + '/' + str(i))

        walk(doc, '')
    return {'terminationShapedObjects': scanned, 'flagged': flagged}


def digest_consequence(m):
    targets = {'workflows/schemas/common.schema.json', 'workflows/schemas/evaluator3/common.schema.json'}
    ledgers = []
    for path in sorted(m.dc.rglob('*.json')):
        raw = path.read_bytes()
        if b'common.schema.json' not in raw:
            continue
        try:
            doc = json.loads(raw)
        except Exception:
            continue
        hits = []

        def walk(o, ptr):
            if isinstance(o, dict):
                p = o.get('path')
                if isinstance(p, str) and any(p.endswith(t) for t in targets) and isinstance(o.get('sha256'), str):
                    hits.append({'pointer': ptr, 'path': p, 'sha256': o['sha256']})
                for k, v in o.items():
                    if k in ('common.schema.json',) and isinstance(v, str) and len(v) == 64:
                        hits.append({'pointer': ptr + '/' + k, 'path': k, 'sha256': v})
                    walk(v, ptr + '/' + k)
            elif isinstance(o, list):
                for i, v in enumerate(o):
                    walk(v, ptr + '/' + str(i))

        walk(doc, '')
        if hits:
            ledgers.append({'file': str(path.relative_to(m.root)), 'hits': hits})
    registered = []
    for (kind, domain), row in m.W.PAYLOAD_REGISTRY.items():
        doc = json.loads((m.dc / row['schemaDocument']).read_text())
        refs = []

        def walk(o):
            if isinstance(o, dict):
                r = o.get('$ref')
                if isinstance(r, str) and 'StepTermination' in r:
                    refs.append(r)
                for v in o.values():
                    walk(v)
            elif isinstance(o, list):
                for v in o:
                    walk(v)

        walk(doc)
        registered.append({'kind': kind, 'payloadDomain': domain, 'schemaDocument': row['schemaDocument'],
                           'stepTerminationRefs': refs})
    return {'pinLedgers': ledgers, 'registeredPayloadDocuments': registered,
            'commonSchemaSha256': {t: hashlib.sha256((m.dc / t).read_bytes()).hexdigest() for t in sorted(targets)}}


def summarize(rows):
    schema_keys = [k for k in rows[0]['boundaries'] if 'exit_code' not in k]
    out = {'illegalAdmittedAt': {}, 'lawfulRefusedAt': {}, 'existingRefusalAdmittedAt': {}}
    for r in rows:
        admitted = [k for k in schema_keys if r['boundaries'][k]['observed'] == 'ADMIT']
        refused = [k for k in schema_keys if r['boundaries'][k]['observed'] == 'REFUSE']
        if r['group'] == 'existing-refusal':
            if admitted:
                out['existingRefusalAdmittedAt'][r['name']] = admitted
        elif r['retainedLawRequired'] or r['retainedLawAdvisory']:
            out['illegalAdmittedAt'][r['name']] = {'required': bool(r['retainedLawRequired']), 'admittedAt': admitted}
        else:
            if refused:
                out['lawfulRefusedAt'][r['name']] = {k: r['boundaries'][k].get('reason') for k in refused}
    return out


def run(copy_name, out_name):
    m = modules(copy_name)
    rows = case_rows(m)
    producers, dropped_codes = producer_rows(m)
    record = {
        'copy': copy_name,
        'standing': 'Observation of one disposable copy. Not acceptance, not a global suite.',
        'loadedBytes': {rel: hashlib.sha256((m.root / rel).read_bytes()).hexdigest() for rel in (
            'docs/coop/design-corrections/workflows/schemas/common.schema.json',
            'docs/coop/design-corrections/workflows/schemas/evaluator3/common.schema.json',
            'docs/coop/design-corrections/workflows/workflow_projection_model.v3.py',
            'docs/coop/design-corrections/workflows/workflows_model.v1.py',
            'docs/coop/design-corrections/foundation/evaluator_fault_model.v3.py',
            'docs/coop/design-corrections/integration-host-model.py',
            'docs/coop/design-corrections/native/native_evidence_model.v2.py',
            'docs/coop/artifacts/d9-exit-contract.v1.14.json')},
        'summary': summarize(rows),
        'cases': rows,
        'producers': {
            'counts': {p: {'total': sum(1 for r in producers if r['producer'] == p),
                           'emitted': sum(1 for r in producers if r['producer'] == p and 'termination' in r),
                           'emittedRequiredIllegal': sum(1 for r in producers if r['producer'] == p and r.get('required')),
                           'emittedAdvisory': sum(1 for r in producers if r['producer'] == p and r.get('advisory'))}
                       for p in sorted({r['producer'] for r in producers})},
            'illegalOrAdvisoryEmissions': [r for r in producers if r.get('required') or r.get('advisory')],
            'publicTerminationDroppedInputCodes': dropped_codes,
            'rows': producers,
        },
        'fixtureScan': fixture_scan(m),
        'digestConsequence': digest_consequence(m),
    }
    (BASE / 'probes' / out_name).write_text(json.dumps(record, indent=2, sort_keys=False) + '\n')
    return record
