"""Independent query-carrier probe (workflows-and-surfaces section 8) over the verified disposable copy.

Reuses the owner-built positive envelopes of check-workflow-projection.v3 (module globals, loaded with stdout captured and
its final sys.exit caught) and applies reviewer-authored, lawfully reminted mutations the checker does not apply. Also
checks the nine-command inventory census, the 20 public / 5 host operation split and the required-delivery detail law
against the actual StepTermination schema. Writes only receipts/probes/query-carriers.json."""
import contextlib, copy, hashlib, importlib.util, io, json, sys, traceback
from pathlib import Path

RT = Path('/private/tmp/opensip-design-corrections/claude-independent-design.v43')
WF = RT / 'work/source43-pkg/docs/coop/design-corrections/workflows'
OUT = RT / 'receipts/probes/query-carriers.json'
ROWS = []


def row(case, ok, observed=None, expected=None):
    r = {'case': case, 'ok': bool(ok), 'observed': observed}
    if expected is not None:
        r['expected'] = expected
    ROWS.append(r)


spec = importlib.util.spec_from_file_location('p40_cwp', WF / 'check-workflow-projection.v3.py')
K = importlib.util.module_from_spec(spec)
sys.modules['p40_cwp'] = K
saved_argv, sys.argv = sys.argv, [str(WF / 'check-workflow-projection.v3.py')]
buf, exit_code = io.StringIO(), None
try:
    with contextlib.redirect_stdout(buf):
        spec.loader.exec_module(K)
except SystemExit as exc:
    exit_code = exc.code
finally:
    sys.argv = saved_argv
try:
    checker = json.loads(buf.getvalue())
    row('owner-checker-import', exit_code == 0 and checker['passed'], {'exit': exit_code, 'count': checker['count'], 'failed': len(checker['failed'])})
except Exception as exc:  # noqa: BLE001
    row('owner-checker-import', False, {'exit': exit_code, 'error': str(exc)[:200]})

QS = K.QS
ENVS, CMD_OF, CMD, ENV_REF, INV = K._R2_ENVS, K._R2_COMMAND_OF, K._R2_CMD, K._R2_ENV, K._R2_INV


def schema_ok(env):
    ok, why = K.valid(ENV_REF, env)
    return ok, (None if ok else str(why)[:160])


def project(env, name):
    try:
        QS.project_command_surface(env, CMD[name])
        return 'ADMIT'
    except QS.QuerySurfaceProjectionError as exc:
        return exc.code
    except Exception as exc:  # noqa: BLE001
        return 'EXCEPTION:' + type(exc).__name__


def outcome(env, name):
    ok, why = schema_ok(env)
    return {'schemaValid': ok, 'projection': project(env, name) if ok else 'not-reached', 'why': why}


def wid(prefix, domain, desc):
    return QS.Wlegacy.wid(prefix, domain, desc)


def main():
    nine = {'query', 'candidates', 'inspect', 'review-brief', 'recommend', 'baseline-show', 'policy-show', 'policy-test', 'repair-preview'}
    q_commands = {c['name']: c for c in INV['commands'] if c.get('queryDispatch')}
    row('inventory-query-dispatch-commands-are-exactly-the-nine', set(q_commands) == nine, sorted(q_commands))
    host_ops = {'baseline.inspect', 'discovery.recommend', 'policy.show', 'policy.test', 'review.produce-brief'}
    ops_by = {n: c['queryDispatch']['operations'] for n, c in q_commands.items()}
    want_ops = {'candidates': ['candidate.list'], 'inspect': ['inspection.show'], 'review-brief': ['review.produce-brief'],
                'recommend': ['discovery.recommend'], 'baseline-show': ['baseline.inspect'], 'policy-show': ['policy.show'],
                'policy-test': ['policy.test'], 'repair-preview': []}
    row('non-graph-command-operations-match-the-section-8-table', all(ops_by[n] == o for n, o in want_ops.items()), {n: ops_by[n] for n in want_ops})
    for n, c in q_commands.items():
        d = c['queryDispatch']
        row('parity-paths-equal-parity-fields-' + n, set(d['parityPaths']) == set(c['parityFields']) and d['parityPaths'].get('termination-class') == '/termination/class',
            sorted(d['parityPaths']))
    graph_doc = json.loads((WF / 'schemas/evaluator3/graph-query.schema.json').read_text())
    enums = []

    def walk(node):
        if isinstance(node, dict):
            if isinstance(node.get('enum'), list) and 'graph.neighbors' in node['enum']:
                enums.append(node['enum'])
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)
    walk(graph_doc)
    public = set(enums[0]) if enums else set()
    row('query-command-operations-are-the-20-public-graph-query-3-operations', len(public) == 20 and set(ops_by['query']) == public, sorted(public))
    row('host-operations-are-not-public-operations', not (host_ops & public), sorted(host_ops & public))
    row('seventeen-non-graph-public-operations', len(public - {'graph.neighbors', 'graph.path', 'graph.reach'}) == 17)
    b38 = Path('/tmp/opensip-design-corrections/candidate-subject.v38/docs/coop/design-corrections/workflows/schemas/evaluator3/graph-query.schema.json').read_bytes()
    b39 = (WF / 'schemas/evaluator3/graph-query.schema.json').read_bytes()
    row('graph-query-3-document-bytes-unchanged-from-source38 (17 non-graph owners preserved)', b38 == b39,
        {'sha38': hashlib.sha256(b38).hexdigest(), 'sha39': hashlib.sha256(b39).hexdigest()})

    for key, name in sorted(CMD_OF.items()):
        env = ENVS[key]
        row('lawful-control-' + key, outcome(env, name) == {'schemaValid': True, 'projection': 'ADMIT', 'why': None}, outcome(env, name))
        # recover every parity field from the human rendering independently and compare with the JSON pointer value
        rnd = QS.render_command_formats(env, CMD[name])
        human = next(r['body'] for r in rnd['renderings'] if r['format'] == 'human')
        recovered = QS.parity_from_human(human)
        pointers = CMD[name]['queryDispatch']['parityPaths']
        row('human-parity-equals-json-pointer-' + key,
            all(K.canonical.equal_typed(recovered[f], QS.json_pointer(env, p)) for f, p in pointers.items()), sorted(pointers))
        m = copy.deepcopy(env)
        m['queryResponse'] = {'context': {}}
        row('non-graph-envelope-with-queryResponse-refused-' + key, not schema_ok(m)[0], outcome(m, name))
        m = copy.deepcopy(env)
        m.update(kind='failure', termination={'class': 'request-rejected', 'errorCode': 'CONFIG.INVALID'}, exitCode=2,
                 errors=[{'code': 'CONFIG.INVALID', 'remedy': 'x'}])
        row('failure-envelope-carrying-a-query-carrier-refused-' + key, not schema_ok(m)[0], outcome(m, name))
        m = copy.deepcopy(env)
        m['querySurface'] = 'graph-query-response'
        row('graph-selector-over-a-query-record-refused-' + key, not schema_ok(m)[0], outcome(m, name))
        m = copy.deepcopy(env)
        m['exitCode'] = 3
        o = outcome(m, name)
        row('exit-code-not-the-class-exit-refused-' + key, (not o['schemaValid']) or o['projection'] == 'QUERY_SURFACE_EXIT_JOIN', o)

    # reminted semantic mutants not in the owner checker
    env = copy.deepcopy(ENVS['policy-test'])
    res = env['queryRecord']['result']
    res['resolverAccepted'] = False
    res['policyTestResultId'] = wid('policytest2', 'workflow.policy-test-result', {k: v for k, v in res.items() if k != 'policyTestResultId'})
    env['query'] = QS._summary(len(res['results']), False, False, False)
    row('policy-test-resolver-refused-result-reminted-is-never-a-carrier', not schema_ok(env)[0], outcome(env, 'policy-test'))
    env = copy.deepcopy(ENVS['policy-test'])
    res = env['queryRecord']['result']
    res['summary'] = dict(res['summary'], passed=res['summary']['passed'] + 1)
    res['policyTestResultId'] = wid('policytest2', 'workflow.policy-test-result', {k: v for k, v in res.items() if k != 'policyTestResultId'})
    o = outcome(env, 'policy-test')
    row('policy-test-summary-tamper-with-reminted-id-refused-by-the-summary-join', o['projection'] == 'QUERY_SURFACE_POLICY_TEST_SUMMARY_JOIN', o)

    env = copy.deepcopy(ENVS['candidates-hidden'])
    before = env['queryRecord']['suppressedCount']
    env['queryRecord']['suppressedCount'] = 0
    o = outcome(env, 'candidates')
    row('observation-hidden-listing-suppressedCount-is-not-joinable-from-the-record', True,
        {'originalSuppressedCount': before, 'mutatedTo': 0, 'outcome': o},
        'section 5: suppressedCount always counts the Run suppressed candidates; the carrier join table checks it only with includeSuppressed')

    env = copy.deepcopy(ENVS['recommend'])
    props = env['queryRecord']['config2Proposals']
    if props:
        p = props[0]
        dup = copy.deepcopy(env)
        dup['queryRecord']['config2Proposals'][0]['workspaceRoots'] = p['workspaceRoots'] + p['workspaceRoots'][:1]
        o = outcome(dup, 'recommend')
        row('recommend-duplicate-proposed-root-refused', (not o['schemaValid']) or o['projection'] == 'QUERY_SURFACE_CONFIG2_ROOT_NOT_DISCOVERED', o)
        ords = copy.deepcopy(env)
        ords['queryRecord']['config2Proposals'][0]['unitOrdinals'] = [x + 1000 for x in p['unitOrdinals']] or [1000]
        o = outcome(ords, 'recommend')
        row('recommend-unit-ordinals-not-the-proposed-units-refused', (not o['schemaValid']) or o['projection'] == 'QUERY_SURFACE_CONFIG2_UNIT_JOIN', o)
    else:
        row('recommend-fixture-has-a-proposal', False, 'no config2 proposal in the owner envelope')

    env = copy.deepcopy(ENVS['repair-preview'])
    plan, preview = env['queryRecord']['plan'], env['queryRecord']['preview']
    plan['descriptor']['projectId'] = 'prj1_' + '0' * 32 if not str(plan['descriptor']['projectId']).startswith('prj1_' + '0') else 'prj1_' + '1' * 32
    plan['repairPlanId'] = wid('repairplan2', 'workflow.repair-plan', plan['descriptor'])
    preview['repairPlanId'] = plan['repairPlanId']
    o = outcome(env, 'repair-preview')
    row('repair-preview-descriptor-of-another-project-reminted-refused', (not o['schemaValid']) or o['projection'] == 'QUERY_SURFACE_PROJECT_JOIN', o)

    env = copy.deepcopy(ENVS['review-brief'])
    env['queryRecord']['brief']['runId'] = 'run3:' + '1' * 64
    o = outcome(env, 'review-brief')
    row('review-brief-of-another-run-refused', (not o['schemaValid']) or o['projection'] == 'QUERY_SURFACE_CANDIDATE_RUN_JOIN', o)

    env = copy.deepcopy(ENVS['policy-show'])
    effective = [w['waiverId'] for w in env['queryRecord']['effectiveWaivers']['waivers']]
    if effective:
        env['queryRecord']['waiverResolution']['expired'] = sorted(set(env['queryRecord']['waiverResolution']['expired']) | {effective[0]})
        o = outcome(env, 'policy-show')
        row('policy-show-effective-waiver-listed-as-expired-refused', (not o['schemaValid']) or o['projection'] == 'QUERY_SURFACE_WAIVER_RESOLUTION_JOIN', o)

    env = copy.deepcopy(ENVS['inspect'])
    facts = env['queryRecord']['inspection']['facts']
    if len(facts) > 1:
        env['queryRecord']['inspection']['facts'] = list(reversed(facts))
        o = outcome(env, 'inspect')
        row('inspect-facts-not-byte-ordered-refused', (not o['schemaValid']) or o['projection'] == 'QUERY_SURFACE_INSPECTION_ORDER', o)
    else:
        row('inspect-fixture-fact-count', True, len(facts))

    # required-delivery detail law against the actual StepTermination schema
    def term_ok(t):
        try:
            QS._admit(QS.TERMINATION_REF, t, 'X')
            return True
        except Exception:  # noqa: BLE001
            return False
    base = {'class': 'operational-failed', 'errorCode': 'DELIVERY.REQUIRED_FAILED', 'faultCause': 'delivery-required'}
    run_id = 'run3:' + '2' * 64
    law = {
        'projection-failed-without-runId-valid': (dict(base, domainDetail={'code': 'DELIVERY.REQUIRED_PROJECTION_FAILED', 'remedy': 'x'}), True),
        'projection-failed-with-runId-invalid': (dict(base, runId=run_id, domainDetail={'code': 'DELIVERY.REQUIRED_PROJECTION_FAILED', 'remedy': 'x'}), False),
        'after-commit-with-runId-valid': (dict(base, runId=run_id, domainDetail={'code': 'DELIVERY.RENDERER_FAILED_AFTER_COMMIT', 'remedy': 'x'}), True),
        'after-commit-without-runId-invalid': (dict(base, domainDetail={'code': 'DELIVERY.RENDERER_FAILED_AFTER_COMMIT', 'remedy': 'x'}), False),
        'projection-failed-on-another-error-code-invalid': ({'class': 'operational-failed', 'errorCode': 'HOST.IO_FAILURE', 'faultCause': 'host-io',
                                                             'domainDetail': {'code': 'DELIVERY.REQUIRED_PROJECTION_FAILED', 'remedy': 'x'}}, False),
        'projection-failed-as-request-rejected-invalid': ({'class': 'request-rejected', 'errorCode': 'CONFIG.INVALID',
                                                           'domainDetail': {'code': 'DELIVERY.REQUIRED_PROJECTION_FAILED', 'remedy': 'x'}}, False),
    }
    for name, (t, want) in law.items():
        row('delivery-law-' + name, term_ok(t) is want, term_ok(t), want)
    pre = QS.delivery_required_termination(committed=False)
    row('owner-precommit-delivery-termination-is-schema-valid-without-runId', term_ok(pre) and 'runId' not in pre, pre)


try:
    main()
except Exception:  # noqa: BLE001
    row('probe-crashed', False, traceback.format_exc()[-2000:])
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps({'standing': 'independent reviewer probe over owner-built envelopes; reference projection, not Run admission or renderer conformance',
                           'rows': ROWS, 'failed': [r for r in ROWS if not r['ok']]}, indent=1, default=str))
print(json.dumps({'total': len(ROWS), 'failed': [(r['case'], r['observed']) for r in ROWS if not r['ok']]}, indent=1, default=str)[:6000])
