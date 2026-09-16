"""Independent policy.test probe over the verified disposable copy (PolicyTestSuiteV2, workflows-and-surfaces section 5).

P1 known-hit law: a gating rule whose root is decided by a known native hit while a REQUIRED evidence kind is absent.
   The fixture evaluator (policy_test_model.v3 via workflows_model.v3.run_admitted_policy_test) is compared with the
   evaluator composition owner (evaluator_composition_model.v3.compose) over the same logical rule. Bounded composition
   only on the production side (synthesized locators, no full retained Run), exactly as check-composition.v3 is.
P2 universe token: the retained authored suite names `typescript-v2`; the evaluator profile policyUniverseMap decides.
P3 admission precedence and public routes, with discriminating negatives.
P4 identity preimages recomputed with an independent H frame and canonical encoder.
Writes only receipts/probes/policy-test.json."""
import copy, hashlib, importlib.util, json, sys, traceback
from pathlib import Path

RT = Path('/private/tmp/opensip-design-corrections/claude-policy-test-known-hit-author.v1/work/repro-original')
SRC = Path('/private/tmp/opensip-design-corrections/claude-policy-test-known-hit-author.v1/work/source39')
DC = SRC / 'docs/coop/design-corrections'
OUT = RT / 'receipts/probes/policy-test.json'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


W = load('p39_workflows_v3', DC / 'workflows/workflows_model.v3.py')
E = load('p39_composition_v3', DC / 'foundation/evaluator_composition_model.v3.py')
CASES = json.loads((DC / 'workflows/policy-test-cases.v3.json').read_text())
BASE = CASES['currentSuite']
IDS = json.loads((DC / 'foundation/identity-schemas.v3.json').read_text())
ROWS = []


def row(probe, case, ok, observed, expected=None, note=None):
    r = {'probe': probe, 'case': case, 'ok': bool(ok), 'observed': observed}
    if expected is not None:
        r['expected'] = expected
    if note:
        r['note'] = note
    ROWS.append(r)


def C(x):
    return json.dumps(x, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')


def H(domain, x):
    b = C(x)
    return hashlib.sha256(b'opensip.product.v1\x00' + domain.encode('ascii') + b'\x00' + len(b).to_bytes(8, 'big') + b).hexdigest()


def run(suite):
    try:
        res, refusal = W.run_admitted_policy_test(copy.deepcopy(suite))
    except W.Refusal as exc:
        t = exc.termination()
        return {'admission': 'REFUSED', 'class': t['class'], 'errorCode': t['errorCode'],
                'detail': (t.get('domainDetail') or {}).get('code')}
    except Exception as exc:  # noqa: BLE001 - recorded, never read as a lawful refusal
        return {'admission': 'EXCEPTION', 'error': type(exc).__name__ + ':' + str(exc)[:300]}
    out = {'admission': 'ADMITTED', 'resolverAccepted': res['resolverAccepted'], 'result': res}
    if refusal is not None:
        t = refusal.termination()
        out.update(refusalClass=t['class'], refusalErrorCode=t['errorCode'], refusalDetail=(t.get('domainDetail') or {}).get('code'))
    return out


def route(o):
    if o['admission'] == 'REFUSED':
        return ['REFUSED', o['class'], o['errorCode'], o['detail']]
    if o['admission'] == 'ADMITTED' and not o['resolverAccepted']:
        return ['RESOLVER-REFUSED', o['refusalClass'], o['refusalErrorCode'], o['refusalDetail']]
    return [o['admission'], o.get('resolverAccepted'), o.get('error')]


def ref(rule_id):
    return {'contributionId': 'core.rules', 'ruleStableId': rule_id, 'semanticsMajor': 1, 'programDigest': '0' * 64}


NATIVE_NONE_TARGET = {'op': 'none', 'relation': 'imports', 'minResolution': 'resolved-target', 'endpoint': 'target', 'filters': []}
TEST_EXISTS = {'op': 'exists', 'relation': 'test-execution', 'minResolution': 'observed', 'filters': [], 'evidence': 'test'}
WAIVERS = {'schemaFamily': 'opensip.product.waivers', 'schemaMajor': 1, 'waivers': []}


def suite_with(emit_when, requirement, available, facts=(), universe='typescript', expectations=None):
    rule = {'ruleId': 'known-hit-rule', 'ruleProgramRef': ref('known-hit-rule'), 'enabled': True, 'severity': 'error', 'gate': True,
            'subjectEnumeration': {'universe': universe, 'subjectKind': 'file', 'include': ['src/**']},
            'emitWhen': emit_when, 'evidenceUse': [{'kind': 'test', 'requirement': requirement}]}
    policy = {'schemaFamily': 'opensip.product.policy', 'schemaMajor': 2, 'gateSeverityAtLeast': 'warning', 'rules': [rule]}
    case = {'id': 'c', 'subject': {'kind': 'facts', 'subjects': ['src/a.ts'], 'facts': list(facts), 'coverage': 'complete',
                                   'evidenceAvailable': list(available)},
            'expectations': expectations or [{'kind': 'finding', 'ruleId': 'known-hit-rule', 'minCount': 1, 'subjects': ['src/a.ts']},
                                             {'kind': 'verdict', 'verdict': 'fail'}]}
    return {'schemaFamily': 'opensip.product.policy-test', 'schemaMajor': 2, 'candidatePolicy': policy, 'waivers': WAIVERS,
            'asOfDate': '2026-09-05', 'cases': [case]}


def fixture_case(o):
    if o['admission'] != 'ADMITTED' or not o['resolverAccepted']:
        return route(o)
    c = o['result']['results'][0]
    return {'outcome': c['outcome'], 'observedVerdict': c['observedVerdict'], 'findings': c['findings'],
            'indeterminateRules': c['indeterminateRules'], 'expectationOutcomes': c['expectationOutcomes']}


# ---------------------------------------------------------------------------------------------- production composition
def token(text):
    return hashlib.sha256(text.encode()).hexdigest()


def compose(atom, requirement, missing, native_value):
    """check-composition.v3 `make` harness (bounded composition, one file subject), with an evidence kind of `test`."""
    rule = {'ruleId': 'r', 'ruleProgramRef': {'contributionId': 'fixture', 'ruleStableId': 'r', 'semanticsMajor': 2, 'programDigest': E.sha(atom)},
            'enabled': True, 'severity': 'error', 'gate': True, 'subjectEnumeration': {'universe': 'syntax', 'subjectKind': 'file'},
            'emitWhen': atom, 'evidenceUse': [{'kind': 'test', 'requirement': requirement}]}
    policy = {'schemaFamily': 'opensip.product.policy', 'schemaMajor': 2, 'gateSeverityAtLeast': 'error', 'rules': [rule]}
    detector = 'closure2:' + token('fixture-detector')
    universe = token('one')
    sid = E.M.identifier('evaluation-subject', {'schemaVersion': 3, 'universe': universe, 'kind': 'file', 'nativeSubjectId': 'src/a.ts'})
    population = {sid: {'subjectId': sid, 'universe': universe, 'kind': 'file', 'collisionPopulationComplete': True,
                        'row': {'nativeSubjectId': 'src/a.ts', 'kind': 'file', 'path': 'src/a.ts', 'qualifiedName': 'src/a.ts',
                                'subjectLanguage': 'typescript', 'signatureTokens': [], 'projections': []}}}
    plan = {'policyDigest': E.sha(policy), 'waiverDigest': E.sha(WAIVERS), 'semanticClosures': [detector], 'budget': {'unit': 'work-units', 'limit': 100000}}
    missing_rows = [{'source': 'import', 'cause': 'evidence-kind-unavailable', 'subjectId': None, 'predicateId': None, 'inputRefs': [],
                     'evidenceKind': 'test', 'nativeCause': None, 'universe': None}] if missing else []
    inputs = {'plan': plan, 'planId': 'plan2:' + token('plan'), 'executionPlanId': 'exec-plan2:' + token('exec'), 'evaluatorClosure': 'closure2:' + token('eval'),
              'policy': policy, 'effectiveWaivers': WAIVERS,
              'emissionPlan': {'schemaVersion': 1, 'policyDigest': plan['policyDigest'], 'rules': [{'ruleId': 'r', 'contributionId': 'fixture', 'ruleStableId': 'r',
                               'semanticsMajor': 2, 'detectorClosure': detector, 'stabilityClass': 'path-stable', 'emissionProfile': 'declarative-subject-v1'}]},
              'population': population,
              'enumerations': {'r': {'state': 'complete', 'inventoryRefs': [], 'selectedSubjectIds': E.cset(population), 'unresolvedSubjectIds': [], 'incompleteInventoryRefs': []}},
              'enumerationDeficiencies': {'r': []}, 'requiredEvidenceDeficiencies': {'r': missing_rows}, 'executionDeficiencies': [],
              'executionInputsDigest': 'e' * 64, 'evaluationInputRefs': [{'domain': 'execution-inputs', 'digest': 'e' * 64}],
              'inventoryRowCount': 1, 'inventoryLocatorCount': 1, 'factCount': 0, 'observationCount': 0, 'coverageCount': 0, 'importKinds': {},
              'closures': {detector: {'kind': 'detector'}}}

    def scan(rule, subject, node, pid):
        if node['relation'] == 'test-execution':
            value = 'indeterminate'
            ds = [{'source': 'import', 'cause': 'evidence-kind-unavailable', 'subjectId': subject['subjectId'], 'predicateId': pid, 'inputRefs': [],
                   'evidenceKind': 'test', 'nativeCause': None, 'universe': None}]
            kind = 'imported-atom'
        else:
            value, ds, kind = native_value, [], 'native-atom'
        return {'kind': kind, 'value': value, 'matchingFactIds': [], 'uncertainFactIds': [], 'matchingImportRows': [], 'uncertainImportRows': [],
                'coverageIds': [], 'scopeIds': [], 'inputRefs': [], 'deficiencies': ds}
    out = E.compose(inputs, scan)
    proof = out['proof']
    root = [p for p in proof['predicateProofs'] if p['predicateId'] == 'p']
    return {'verdict': proof['verdict'], 'ruleOutcome': proof['ruleResults'][0]['outcome'], 'findings': len(proof['findingIds']),
            'rootValue': root[0]['value'] if root else None}


def p1():
    OR = {'op': 'or', 'operands': [NATIVE_NONE_TARGET, TEST_EXISTS]}
    AND_FALSE = {'op': 'and', 'operands': [NATIVE_NONE_TARGET, TEST_EXISTS]}
    importer = {'relation': 'imports', 'subject': 'src/b.ts', 'target': 'src/a.ts', 'resolution': 'resolved-target', 'universe': 'typescript',
                'confidenceMillionths': 1000000, 'targetKind': 'file'}
    # production composition over the same logical rule (native `none` known true; test atom unknown)
    prod = {'or-required-missing': compose(OR, 'required', True, 'true'),
            'or-required-present': compose(OR, 'required', False, 'true'),
            'or-optional-missing': compose(OR, 'optional', False, 'true'),
            'and-false-required-missing': compose({'op': 'and', 'operands': [NATIVE_NONE_TARGET, TEST_EXISTS]}, 'required', True, 'false')}
    fixture = {'or-required-missing': fixture_case(run(suite_with(OR, 'required', []))),
               'or-required-present': fixture_case(run(suite_with(OR, 'required', ['test']))),
               'or-optional-missing': fixture_case(run(suite_with(OR, 'optional', []))),
               'and-false-required-missing': fixture_case(run(suite_with(AND_FALSE, 'required', [], facts=[importer],
                                                    expectations=[{'kind': 'no-finding', 'ruleId': 'known-hit-rule'},
                                                                  {'kind': 'verdict', 'verdict': 'indeterminate'}])))}
    for name in prod:
        row('P1', 'production-composition-' + name, True, prod[name])
        row('P1', 'fixture-' + name, True, fixture[name])
    pr, fx = prod['or-required-missing'], fixture['or-required-missing']
    row('P1', 'known-native-hit-under-missing-required-evidence-agrees-with-composition',
        isinstance(fx, dict) and pr['verdict'] == fx.get('observedVerdict') and (pr['findings'] > 0) == bool(fx.get('findings')),
        {'composition': pr, 'fixture': fx},
        expected='composition section 5 / 9.5 (check-composition a9-known-live-failure-dominates-missing-required-import): a live unwaived '
                 'gating finding makes the outcome fail even when a required import kind is unavailable; workflows section 5: known '
                 'findings, strong Kleene and gating are unchanged')
    for name in ('or-required-present', 'or-optional-missing'):
        pr, fx = prod[name], fixture[name]
        row('P1', 'control-' + name + '-agrees', isinstance(fx, dict) and pr['verdict'] == fx.get('observedVerdict')
            and (pr['findings'] > 0) == bool(fx.get('findings')), {'composition': pr, 'fixture': fx})


def p2():
    umap = IDS['x-opensip-evaluator-profile']['policyUniverseMap']
    tokens = sorted({r['subjectEnumeration']['universe'] for r in BASE['candidatePolicy']['rules']})
    row('P2', 'evaluator-profile-policy-universe-map', True, umap)
    row('P2', 'authored-suite-universe-tokens', True, tokens)
    o = run(BASE)
    row('P2', 'authored-suite-with-unregistered-token-is-resolver-accepted', True,
        {'route': route(o), 'tokensRegistered': {t: t in umap for t in tokens}, 'summary': o.get('result', {}).get('summary')},
        note='observation: the policy test resolver does not apply the evaluator profile universe-token admission')
    bogus = copy.deepcopy(BASE)
    for r in bogus['candidatePolicy']['rules']:
        r['subjectEnumeration']['universe'] = 'no-such-universe'
    for c in bogus['cases']:
        for f in c['subject'].get('facts', []):
            f['universe'] = 'no-such-universe'
    ob = run(bogus)
    row('P2', 'arbitrary-token-no-such-universe', True, {'route': route(ob), 'summary': ob.get('result', {}).get('summary')})
    lawful = copy.deepcopy(BASE)
    for r in lawful['candidatePolicy']['rules']:
        r['subjectEnumeration']['universe'] = 'typescript'
    for c in lawful['cases']:
        for f in c['subject'].get('facts', []):
            f['universe'] = 'typescript'
    ol = run(lawful)
    row('P2', 'registered-token-control-yields-the-same-summary',
        o.get('result', {}).get('summary') == ol.get('result', {}).get('summary'),
        {'route': route(ol), 'summary': ol.get('result', {}).get('summary')})


def p3():
    MAJOR = ['REFUSED', 'request-rejected', 'REQUEST.SCHEMA_MAJOR_UNSUPPORTED', 'EVALUATION.MIXED_OUTPUT_MAJOR']
    IMPERATIVE = ['REFUSED', 'request-rejected', 'CONFIG.INVALID', 'POLICY.IMPERATIVE_KEY_REFUSED']
    SHARED = ['REFUSED', 'request-rejected', 'CONFIG.INVALID', 'CONFIG.INVALID']

    def mutate(fn):
        s = copy.deepcopy(BASE)
        fn(s)
        return s
    rules = lambda s: s['candidatePolicy']['rules']  # noqa: E731
    cases = [
        ('suite-major-1', lambda s: s.update(schemaMajor=1), MAJOR),
        ('candidate-major-1', lambda s: s['candidatePolicy'].update(schemaMajor=1), MAJOR),
        ('historical-v1-shaped-suite-and-candidate', lambda s: (s.update(schemaMajor=1), s['candidatePolicy'].update(schemaMajor=1)), MAJOR),
        ('suite-major-1-beats-imperative-key', lambda s: (s.update(schemaMajor=1), rules(s)[0].update(hook='rm -rf')), MAJOR),
        ('candidate-major-1-beats-imperative-key', lambda s: (s['candidatePolicy'].update(schemaMajor=1), rules(s)[0].update(hook='x')), MAJOR),
        ('undeclared-rule-member', lambda s: rules(s)[0].update(hook='x'), IMPERATIVE),
        ('undeclared-atom-member-nested', lambda s: rules(s)[1]['emitWhen'].update(exec='x'), IMPERATIVE),
        ('string-expression-emitWhen', lambda s: rules(s)[1].update(emitWhen="imports.none()"), IMPERATIVE),
        ('undeclared-top-level-policy-member', lambda s: s['candidatePolicy'].update(include='other.json'), IMPERATIVE),
        ('imperative-key-precedes-other-suite-schema-failure', lambda s: (s.pop('cases'), rules(s)[0].update(exec='x')), IMPERATIVE),
        ('imperative-key-precedes-fixture-fault', lambda s: (rules(s)[0].update(exec='x'), s['cases'][0]['subject']['facts'][0].update(resolution='observed')), IMPERATIVE),
        ('wrong-severity-enum-is-not-imperative', lambda s: rules(s)[0].update(severity='critical'), SHARED),
        ('malformed-rule-id-string-is-not-imperative', lambda s: (rules(s)[0].update(ruleId='bad id')), SHARED),
        ('suite-missing-cases', lambda s: s.pop('cases'), SHARED),
        ('suite-major-boolean', lambda s: s.update(schemaMajor=True), SHARED),
        ('fact-rung-not-of-relation', lambda s: s['cases'][0]['subject']['facts'][0].update(resolution='observed'), SHARED),
        ('fact-relation-unregistered', lambda s: s['cases'][0]['subject']['facts'][0].update(relation='imports-maybe'), SHARED),
        ('override-of-non-candidate-rule', lambda s: s.update(overrides=[{'ruleId': 'not-a-rule', 'field': 'enabled', 'value': False}]), SHARED),
        ('override-severity-with-boolean', lambda s: s.update(overrides=[{'ruleId': 'unimported-file', 'field': 'severity', 'value': True}]), SHARED),
        ('override-enabled-with-severity', lambda s: s.update(overrides=[{'ruleId': 'unimported-file', 'field': 'enabled', 'value': 'error'}]), SHARED),
        # reminted lawfully: waiverId order is strictly ascending, so the duplicate TARGET carries a later waiverId
        ('duplicate-waiver-is-resolver-refusal', lambda s: s['waivers']['waivers'].append(dict(s['waivers']['waivers'][1], waiverId='w-zdup')),
         ['RESOLVER-REFUSED', 'request-rejected', 'CONFIG.INVALID', 'POLICY.DUPLICATE_WAIVER']),
        ('unregistered-atom-relation-is-resolver-refusal', lambda s: rules(s)[1]['emitWhen'].update(relation='no-such-relation'),
         ['RESOLVER-REFUSED', 'request-rejected', 'CONFIG.INVALID', 'POLICY.UNKNOWN_RULE']),
        ('undeclared-evidence-is-resolver-refusal', lambda s: rules(s)[2].update(evidenceUse=[]),
         ['RESOLVER-REFUSED', 'request-rejected', 'CONFIG.INVALID', 'IMPORT.ABSENT_FOR_PREDICATE']),
    ]
    for name, fn, want in cases:
        try:
            got = route(run(mutate(fn)))
        except Exception as exc:  # noqa: BLE001
            got = ['PROBE-ERROR', type(exc).__name__ + ':' + str(exc)[:200]]
        row('P3', name, got == want, got, want)
    ok = run(BASE)
    row('P3', 'authored-suite-admits', route(ok) == ['ADMITTED', True, None], route(ok))
    # a candidate-policy major refusal must not require the family string to be exactly right? recorded as observation
    s = copy.deepcopy(BASE)
    s['candidatePolicy']['schemaMajor'] = 1
    s['candidatePolicy'].pop('schemaFamily')
    row('P3', 'observation-candidate-major-1-without-family', True, route(run(s)),
        note='schema precedence 2 names "a policy document candidatePolicy whose integer schemaMajor is not 2"')


def p4():
    o = run(BASE)
    res = o['result']
    row('P4', 'independent-canonical-equals-owner-canonical', C(BASE) == W.canonical.canonical(BASE), len(C(BASE)))
    row('P4', 'suite-digest-is-H-workflow-policy-test-suite-over-the-whole-suite', res['suiteDigest'] == H('workflow.policy-test-suite', BASE),
        res['suiteDigest'])
    row('P4', 'suite-digest-is-not-raw-sha256-of-suite-bytes', res['suiteDigest'] != hashlib.sha256(C(BASE)).hexdigest(), res['suiteDigest'])
    body = {k: v for k, v in res.items() if k != 'policyTestResultId'}
    row('P4', 'result-id-is-policytest2-H-over-the-result-without-its-id', res['policyTestResultId'] == 'policytest2:' + H('workflow.policy-test-result', body),
        res['policyTestResultId'])
    row('P4', 'candidate-digest-is-raw-sha256-of-candidate-bytes', res['candidatePolicyDigest'] == hashlib.sha256(C(BASE['candidatePolicy'])).hexdigest(),
        res['candidatePolicyDigest'])
    again = run(BASE)['result']
    row('P4', 'same-suite-same-result-bytes', C(again) == C(res), res['policyTestResultId'])
    try:
        W.projection_owner().validate_profile('urn:opensip:product-v1:workflows:policy-test#/$defs/PolicyTestResultV1', res)
        valid = True
    except Exception as exc:  # noqa: BLE001
        valid = type(exc).__name__ + ':' + str(exc).split('\n')[0][:200]
    row('P4', 'result-validates-as-PolicyTestResultV1', valid is True, valid)
    over = copy.deepcopy(BASE)
    over['overrides'] = [{'ruleId': 'unimported-file', 'field': 'gate', 'value': False}]
    ro = run(over)['result']
    row('P4', 'override-changes-suite-and-effective-digests-not-candidate-digest',
        ro['suiteDigest'] != res['suiteDigest'] and ro['effectivePolicyDigest'] != res['effectivePolicyDigest']
        and ro['candidatePolicyDigest'] == res['candidatePolicyDigest'],
        {'suite': ro['suiteDigest'], 'effective': ro['effectivePolicyDigest']})
    expect = CASES['currentSuiteExpect']
    row('P4', 'authored-expectation-summary-reproduced (author oracle, not independent)', res['summary'] == expect['summary'], res['summary'])


for fn in (p1, p2, p3, p4):
    try:
        fn()
    except Exception:  # noqa: BLE001
        row(fn.__name__.upper(), 'section-crashed', False, traceback.format_exc()[-1500:])
OUT.parent.mkdir(parents=True, exist_ok=True)
report = {'standing': 'author path-only rerun of the retained independent probe against my verified frozen39 capture (pre-correction); not an independent probe',
          'rows': ROWS, 'failed': [r for r in ROWS if not r['ok']]}
OUT.write_text(json.dumps(report, indent=1, default=str))
print(json.dumps({'total': len(ROWS), 'failed': [(r['probe'], r['case']) for r in ROWS if not r['ok']]}, indent=1))
