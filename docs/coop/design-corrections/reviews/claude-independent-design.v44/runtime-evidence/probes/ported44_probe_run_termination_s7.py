"""Independent run-termination section 7 host-composition probe (ADV38-01) over actually closed Runs.

Builds the golden Runs through the maintained owner path (check-semantic-replay.v3 fixtures -> close_positive, i.e.
identity-model.v3.close_run), mints receipts through the reference commit path (identity-model.v3 EvidenceStore), and
calls run_termination_model.v1.admit_analysis_step_termination directly with observations the golden case vocabulary
cannot express. Writes only receipts/probes/run-termination-s7.json."""
import copy, json, sys, traceback
from pathlib import Path

RT = Path('/private/tmp/opensip-design-corrections/claude-independent-design.v44')
FOUND = RT / 'work/source44-pkg/docs/coop/design-corrections/foundation'
OUT = RT / 'receipts/probes/run-termination-s7.json'
sys.path.insert(0, str(FOUND))
import importlib.util


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


SR = load('p40_semantic_replay', FOUND / 'check-semantic-replay.v3.py')
M, R, C = SR.M, SR.R, SR.C
T = SR.load('p40_run_termination', 'run_termination_model.v1.py')
Q = SR.load('p40_step_schema', '../workflows/query_projection_model.v3.py')
DOC = json.loads((FOUND / 'run-termination-goldens.v1.json').read_text())
ATOMS = {'REFS_NONE_TGT': SR.REFS_NONE_TGT, 'DECLARES': SR.DECLARES}
ROWS = []


def row(case, ok, observed, expected=None):
    r = {'case': case, 'ok': bool(ok), 'observed': observed}
    if expected is not None:
        r['expected'] = expected
    ROWS.append(r)


def validate_shape(term):
    Q.validate_schema(Q.COMMON_ID + '#/$defs/StepTermination', term)


def validate_attempt(attempt):
    Q.validate_schema('urn:opensip:product-v1:workflows:evaluator3:invocation:3#/$defs/Attempt', attempt)


RECEIPT_SCHEMA = copy.deepcopy(M.SCHEMA)
RECEIPT_SCHEMA['$ref'] = '#/$defs/commit-receipt'


def validate_receipt(receipt):
    C.validate(RECEIPT_SCHEMA, receipt)


_EXPORTS = {}


def build(group_id):
    g = next(x for x in DOC['goldens'] if x['id'] == group_id)
    spec = g['build']
    if 'export' in spec:
        if spec['export'] not in _EXPORTS:
            fn = dict(SR.POSITIVES)[spec['export']]
            _EXPORTS[spec['export']] = fn()[1]
        return _EXPORTS[spec['export']]
    fixture = DOC['fixtures'][spec['fixture']]
    params = dict(fixture['params'], **spec['params'], atom=ATOMS[fixture['atom']])
    run, objects, blobs, _ = SR.close_positive(SR.S.build_ts_semantic_graph(**params))
    return run, objects, blobs


def receipt_for(run, objects, blobs, execution_id):
    seal = objects[run['evaluationSealId']][1]
    _, owner = M.open_run_closure(run, objects, blobs)

    def replay(plan, objs, bl, refs):
        return R.derive(run['planId'], seal['executionPlanId'], seal['evaluatorClosure'], refs, objs, bl, owner)['proof']
    store = M.EvidenceStore()
    store.prepare(run, objects, blobs, execution_id, replay)
    assert store.commit(execution_id) == 'committed'
    return dict(store.receipts[0])


def binding(run, objects):
    plan = objects[run['evaluationSealId']][1]['executionPlanId']
    stages = len(objects[plan][1]['stages'])
    return {'planId': run['planId'], 'executionPlanId': plan, 'stageCount': stages, 'stagesCompleted': stages}


DONE, OTHER, THIRD = 'exec1_' + 'd' * 32, 'exec1_' + 'e' * 32, 'exec1_' + 'c' * 32


def compose(candidate, run, objects, blobs, observation, attempt_validator=validate_attempt, receipt_validator=validate_receipt):
    try:
        got = T.admit_analysis_step_termination(candidate, run, objects, blobs, observation, validate_shape, attempt_validator, receipt_validator)
        return 'ADMIT:' + str(got.get('domainDetailCode') or got['standing'])
    except T.RunTerminationError as exc:
        return str(exc).split(':', 1)[0]
    except Exception as exc:  # noqa: BLE001 - an owner admission refusal of a tampered Run is not a composition outcome
        return 'EXCEPTION:' + type(exc).__name__ + ':' + str(exc)[:160]


def main():
    wb = build('work-budget-is-d9-budget-exhausted')
    run, objects, blobs = wb
    derived = T.finalize(run, objects, blobs)['termination']
    detail = {'code': 'EVALUATION.WORK_BUDGET_EXHAUSTED', 'remedy': 'raise or narrow the admitted analysis work budget'}
    lawful = dict(derived, executionId=DONE, domainDetail=detail)
    rc = receipt_for(run, objects, blobs, DONE)
    b = binding(run, objects)

    def obs(attempts, receipt=rc, **over):
        o = {'stepId': 0, 'durability': 'authoritative', 'attempts': attempts, 'commitReceipt': receipt, 'requiredClosureNotInstalled': False}
        o.update(over)
        return o
    done = {'executionId': DONE, 'outcome': 'completed', 'derivation': dict(b)}
    busy = {'executionId': OTHER, 'outcome': 'failed', 'faultCause': 'ledger-busy', 'retried': True}
    cases = [
        ('lawful-control', lawful, obs([done]), 'ADMIT:EVALUATION.WORK_BUDGET_EXHAUSTED'),
        ('lawful-control-remedy-text-is-presentation', dict(lawful, domainDetail=dict(detail, remedy='any wording')), obs([done]), 'ADMIT:EVALUATION.WORK_BUDGET_EXHAUSTED'),
        ('attempt-id-reused', lawful, obs([dict(busy, executionId=DONE), done]), 'RUN_TERMINATION_ATTEMPT_ID_REUSED'),
        ('earlier-attempt-also-completed', lawful, obs([dict(done, executionId=OTHER), done]), 'RUN_TERMINATION_ATTEMPT_NOT_TERMINATING'),
        ('four-attempts-exceed-the-3-attempt-budget', lawful,
         obs([dict(busy, executionId='exec1_' + c * 32) for c in 'abc'] + [done]), 'RUN_TERMINATION_OBSERVATION_SHAPE'),
        ('observation-extra-member', lawful, dict(obs([done]), hostBlessed=True), 'RUN_TERMINATION_OBSERVATION_SHAPE'),
        ('observation-missing-member', lawful, {k: v for k, v in obs([done]).items() if k != 'requiredClosureNotInstalled'}, 'RUN_TERMINATION_OBSERVATION_SHAPE'),
        ('closure-observation-not-boolean', lawful, obs([done], requiredClosureNotInstalled='yes'), 'RUN_TERMINATION_OBSERVATION_SHAPE'),
        ('step-id-out-of-range', lawful, obs([done], stepId=64), 'RUN_TERMINATION_OBSERVATION_SHAPE'),
        ('step-id-boolean', lawful, obs([done], stepId=True), 'RUN_TERMINATION_OBSERVATION_SHAPE'),
        ('attempt-not-invocation-record-shape', lawful, obs([dict(done, outcome='done')]), 'RUN_TERMINATION_OBSERVATION_SHAPE'),
        ('receipt-not-commit-receipt-shape', lawful, obs([done], receipt=dict(rc, extra=1)), 'RUN_TERMINATION_OBSERVATION_SHAPE'),
        ('no-receipt-validator', lawful, obs([done]), 'RUN_TERMINATION_COMPOSITION_UNCHECKED'),
        ('ephemeral-observation-with-receipt', {'class': 'policy-failed', 'authority': 'ephemeral'}, obs([done], durability='ephemeral'),
         'RUN_TERMINATION_OBSERVATION_SHAPE'),
        ('ephemeral-execution-id-of-another-attempt', {'class': 'policy-failed', 'authority': 'ephemeral', 'executionId': OTHER},
         obs([done], receipt=None, durability='ephemeral'), 'RUN_TERMINATION_EXECUTION_ID_NOT_ATTEMPT'),
        ('ephemeral-lawful-control', {'class': 'policy-failed', 'authority': 'ephemeral', 'executionId': DONE},
         obs([done], receipt=None, durability='ephemeral'), 'ADMIT:ephemeral-attribution-admitted'),
    ]
    for name, candidate, observation, want in cases:
        receipt_validator = None if name == 'no-receipt-validator' else validate_receipt
        got = compose(copy.deepcopy(candidate), run, objects, blobs, copy.deepcopy(observation), receipt_validator=receipt_validator)
        row(name, got == want, got, want)

    # a registered native entry detail that is not the named carrier's own deficiency
    two = build('same-run-two-coverage-carriers')
    r2, o2, bl2 = two
    d2 = T.finalize(r2, o2, bl2)['termination']
    rc2 = receipt_for(r2, o2, bl2, DONE)
    done2 = {'executionId': DONE, 'outcome': 'completed', 'derivation': binding(r2, o2)}
    obs2 = {'stepId': 0, 'durability': 'authoritative', 'attempts': [done2], 'commitReceipt': rc2, 'requiredClosureNotInstalled': False}
    entry = C.parse(bl2[o2[d2['coverageId']][1]['payloadDigest']])['entry']
    row('native-carrier-entry-deficiency', True, {'coverageId': d2['coverageId'], 'deficiency': entry['deficiency'], 'reasonCodes': d2['reasonCodes']})
    for code in ('budget-exhausted', 'derivation-policy-unmet', 'external-consumers-unknown', 'input-closure-incomplete', 'resolution-incomplete'):
        want = 'ADMIT:' + code if code == entry['deficiency'] else 'RUN_TERMINATION_DETAIL_NOT_ADMITTED'
        got = compose(dict(d2, domainDetail={'code': code, 'remedy': 'x'}), r2, o2, bl2, copy.deepcopy(obs2))
        row('native-entry-detail-' + code, got == want, got, want)

    # composition over a tampered retained Run: mutate one retained finding/proof object without reminting
    tampered = copy.deepcopy(objects)
    target = next(k for k, (d, v) in tampered.items() if d == 'finding') if any(d == 'finding' for d, _ in tampered.values()) else None
    if target is None:
        target = run['evaluationSealId']
        tampered[target][1]['verdict'] = 'pass'
    else:
        tampered[target][1]['severity'] = 'note' if tampered[target][1]['severity'] != 'note' else 'error'
    got = compose(copy.deepcopy(lawful), run, tampered, blobs, obs([done]))
    row('tampered-retained-run-is-never-composed', got.startswith('EXCEPTION:'), got, 'owner admission refusal before any composition standing')
    # the host observation cannot change the derived projection: an attempt observation bound to this Run over another Run's derived fields
    got = compose(dict(lawful, reasonCodes=list(reversed(lawful['reasonCodes'])) if len(lawful['reasonCodes']) > 1 else ['VERDICT.INDETERMINATE']),
                  run, objects, blobs, obs([done]))
    row('observation-cannot-bless-a-non-derived-projection', got == 'RUN_TERMINATION_NOT_DERIVED', got, 'RUN_TERMINATION_NOT_DERIVED')


try:
    main()
except Exception:  # noqa: BLE001
    row('probe-crashed', False, traceback.format_exc()[-2000:])
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps({'standing': 'independent reviewer probe over actually closed golden Runs; synthetic host observations; not a product host',
                           'rows': ROWS, 'failed': [r for r in ROWS if not r['ok']]}, indent=1, default=str))
print(json.dumps({'total': len(ROWS), 'failed': [(r['case'], r['observed']) for r in ROWS if not r['ok']]}, indent=1))
