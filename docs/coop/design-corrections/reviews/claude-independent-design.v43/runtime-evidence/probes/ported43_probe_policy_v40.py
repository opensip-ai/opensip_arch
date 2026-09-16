"""Independent policy.test discrimination probe: source39 bytes versus source40 bytes, plus production composition controls.

Parent (no arguments): verifies the retained source39 copy against this origin's own source39 manifest index, runs one child
process per side with the pinned interpreter (-I -B) so no module is shared between the two byte sets, runs the production
composition side on source40, compares, and writes only receipts/probes/policy-v40-on43.json.
Child: python probe_policy_v40.py --side ROOT [--production]  -> JSON on stdout.
Expected values are this reviewer's reading of workflows-and-surfaces section 5 (source40 text), composition sections 2, 3, 5
and 9.5, and policy-test.schema.json x-opensip-fixture-representation; the authored suites' expected outcomes are author
oracles and are recorded as such, never used to decide a discrimination row."""
import copy, hashlib, importlib.util, json, os, subprocess, sys, traceback
from pathlib import Path

RT = Path('/private/tmp/opensip-design-corrections/claude-independent-design.v43')
NEW = RT / 'work/source43-pkg'
OLD = Path('/private/tmp/opensip-design-corrections/claude-independent-design.v39/work/source39-pkg')
OLD_INDEX = Path('/private/tmp/opensip-design-corrections/claude-independent-design.v39/receipts/manifest39-index.json')
NEW_INDEX = RT / 'receipts/manifest43-index.json'
OUT = RT / 'receipts/probes/policy-v40-on43.json'


def C(x):
    return json.dumps(x, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')


def H(domain, x):
    b = C(x)
    return hashlib.sha256(b'opensip.product.v1\x00' + domain.encode('ascii') + b'\x00' + len(b).to_bytes(8, 'big') + b).hexdigest()


def ref(rule_id):
    return {'contributionId': 'core.rules', 'ruleStableId': rule_id, 'semanticsMajor': 1, 'programDigest': '0' * 64}


FILE_EXISTS = {'op': 'exists', 'relation': 'file', 'minResolution': 'enumerated', 'filters': []}
TEST_EXISTS = {'op': 'exists', 'relation': 'test-execution', 'minResolution': 'observed', 'filters': [], 'evidence': 'test'}
RUNTIME_HIT = {'op': 'exists', 'relation': 'runtime-observation', 'minResolution': 'observed',
               'filters': [{'field': 'observability', 'cmp': 'eq', 'value': 'observed-hit'}], 'evidence': 'runtime'}
NO_WAIVERS = {'schemaFamily': 'opensip.product.waivers', 'schemaMajor': 1, 'waivers': []}


def rule(rule_id, emit, evidence_use, universe='typescript', gate=True, severity='error', enabled=True):
    return {'ruleId': rule_id, 'ruleProgramRef': ref(rule_id), 'enabled': enabled, 'severity': severity, 'gate': gate,
            'subjectEnumeration': {'universe': universe, 'subjectKind': 'file'}, 'emitWhen': emit, 'evidenceUse': evidence_use}


def fact(relation, universe='typescript', subject='src/a.ts', resolution='enumerated', **extra):
    f = {'relation': relation, 'subject': subject, 'target': subject, 'resolution': resolution, 'universe': universe, 'confidenceMillionths': 1000000}
    f.update(extra)
    return f


def suite(rules, subjects=('src/a.ts',), facts=(), available=(), coverage='complete', waivers=NO_WAIVERS, expectations=None):
    policy = {'schemaFamily': 'opensip.product.policy', 'schemaMajor': 2, 'gateSeverityAtLeast': 'warning', 'rules': sorted(rules, key=lambda r: r['ruleId'].encode())}
    case = {'id': 'c', 'subject': {'kind': 'facts', 'subjects': list(subjects), 'facts': list(facts), 'coverage': coverage, 'evidenceAvailable': list(available)},
            'expectations': expectations or [{'kind': 'verdict', 'verdict': 'fail'}]}
    return {'schemaFamily': 'opensip.product.policy-test', 'schemaMajor': 2, 'candidatePolicy': policy, 'waivers': waivers, 'asOfDate': '2026-09-05', 'cases': [case]}


WAIVE_A = {'schemaFamily': 'opensip.product.waivers', 'schemaMajor': 1,
           'waivers': [{'waiverId': 'w-a', 'target': {'ruleId': 'r', 'subjectPath': 'src/a.ts'}, 'reason': 'accepted', 'expires': None}]}


def fixture_cases():
    OR = {'op': 'or', 'operands': [FILE_EXISTS, TEST_EXISTS]}
    AND = {'op': 'and', 'operands': [FILE_EXISTS, TEST_EXISTS]}
    REQ, OPT = [{'kind': 'test', 'requirement': 'required'}], [{'kind': 'test', 'requirement': 'optional'}]
    RT_OPT = [{'kind': 'runtime', 'requirement': 'optional'}]
    return {
        'A1-or-known-hit-required-missing': suite([rule('r', OR, REQ)], facts=[fact('file')]),
        'A2-or-known-hit-optional-missing': suite([rule('r', OR, OPT)], facts=[fact('file')]),
        'A3-or-known-hit-required-present': suite([rule('r', OR, REQ)], facts=[fact('file')], available=['test']),
        'A4-and-known-false-required-missing': suite([rule('r', AND, REQ)], facts=[]),
        'A5-advisory-known-hit-required-missing': suite([rule('r', OR, REQ, gate=False, severity='note')], facts=[fact('file')]),
        'A6-waived-known-hit-required-missing': suite([rule('r', OR, REQ)], facts=[fact('file')], waivers=WAIVE_A),
        'A7-no-subjects-required-missing': suite([rule('r', OR, REQ)], subjects=[], facts=[]),
        'B1-rule-token-typescript-v2-fact-typescript': suite([rule('r', FILE_EXISTS, [], universe='typescript-v2')], facts=[fact('file')]),
        'B2-disabled-rule-arbitrary-token': suite([rule('r', FILE_EXISTS, [], universe='no-such-universe', enabled=False),
                                                   rule('s', FILE_EXISTS, [])], facts=[fact('file')]),
        'B3-fact-token-typescript-v2': suite([rule('r', FILE_EXISTS, [])], facts=[fact('file', universe='typescript-v2')]),
        'B4-registered-typescript': suite([rule('r', FILE_EXISTS, [], universe='typescript')], facts=[fact('file', universe='typescript')]),
        'B4-registered-rust': suite([rule('r', FILE_EXISTS, [], universe='rust')], facts=[fact('file', universe='rust')]),
        'B4-registered-syntax': suite([rule('r', FILE_EXISTS, [], universe='syntax')], facts=[fact('file', universe='syntax')]),
        'C1-foreign-universe-imported-runtime-hit': suite([rule('r', RUNTIME_HIT, RT_OPT)], available=['runtime'],
                                                          facts=[fact('runtime-observation', universe='rust', resolution='observed', observability='observed-hit')]),
        'C2-same-universe-imported-runtime-hit': suite([rule('r', RUNTIME_HIT, RT_OPT)], available=['runtime'],
                                                       facts=[fact('runtime-observation', universe='typescript', resolution='observed', observability='observed-hit')]),
        'C3-foreign-universe-native-file-fact': suite([rule('r', FILE_EXISTS, [])], facts=[fact('file', universe='rust')]),
        'G1-optional-imported-available-no-row': suite([rule('r', RUNTIME_HIT, RT_OPT)], available=['runtime'], facts=[]),
        'G2-optional-imported-absent': suite([rule('r', RUNTIME_HIT, RT_OPT)], available=[], facts=[]),
    }


# ------------------------------------------------------------------------------------------------ child side
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def child(root, production):
    DC = Path(root) / 'docs/coop/design-corrections'
    W = load('pv40_workflows_v3', DC / 'workflows/workflows_model.v3.py')
    out = {'root': root, 'cases': {}}

    def run(s):
        try:
            res, refusal = W.run_admitted_policy_test(copy.deepcopy(s))
        except W.Refusal as exc:
            t = exc.termination()
            return {'route': 'ADMISSION-REFUSED', 'errorCode': t.get('errorCode'), 'detail': (t.get('domainDetail') or {}).get('code'), 'remedy': exc.remedy}
        except Exception as exc:  # noqa: BLE001
            return {'route': 'EXCEPTION', 'error': type(exc).__name__ + ':' + str(exc)[:300]}
        if refusal is not None:
            t = refusal.termination()
            return {'route': 'RESOLVER-REFUSED', 'errorCode': t.get('errorCode'), 'detail': (t.get('domainDetail') or {}).get('code'), 'remedy': refusal.remedy,
                    'resolverAccepted': res['resolverAccepted']}
        c = res['results'][0]
        return {'route': 'ADMITTED', 'observedVerdict': c['observedVerdict'], 'findings': c['findings'], 'indeterminateRules': c['indeterminateRules'],
                'expectationOutcomes': c['expectationOutcomes'], 'outcome': c['outcome'], 'result': res}

    for name, s in fixture_cases().items():
        r = run(s)
        r.pop('result', None)
        out['cases'][name] = r
    # policy.show path: the inspection resolver over a policy carrying an unregistered universe token
    try:
        pol = fixture_cases()['B1-rule-token-typescript-v2-fact-typescript']['candidatePolicy']
        resolved = W.resolve_policy(copy.deepcopy(pol))
        effective, resolution = W.resolve_waivers(NO_WAIVERS, '2026-09-12')
        digest = getattr(W, 'doc_digest', lambda x: hashlib.sha256(C(x)).hexdigest())
        env_id = json.loads((DC / 'workflows/schemas/evaluator3/command-envelope.schema.json').read_text())['$id']
        record = {'surface': 'effective-policy', 'policyDigest': digest(resolved), 'policy': resolved, 'waiverSetDigest': digest(effective),
                  'effectiveWaivers': effective, 'waiverResolution': resolution}
        try:
            W.projection_owner().validate_profile(env_id + '#/$defs/EffectivePolicyRecordV1', record)
            valid = True
        except Exception as exc:  # noqa: BLE001
            valid = type(exc).__name__ + ':' + str(exc).split('\n')[0][:200]
        out['policyShow'] = {'resolverAccepted': True, 'effectivePolicyRecordSchemaValid': valid}
    except Exception as exc:  # noqa: BLE001
        out['policyShow'] = {'resolverAccepted': False, 'error': type(exc).__name__ + ':' + str(exc)[:300]}
    eim = (DC / 'foundation/evaluator_input_model.v3.py').read_text()
    out['evaluatorInputAdmissionRefusesUnregisteredToken'] = "raise C.AdmissionError('EVALUATOR_POLICY_UNIVERSE_UNREGISTERED')" in eim
    cases_doc = json.loads((DC / 'workflows/policy-test-cases.v3.json').read_text())
    ids = {}
    for key in ('currentSuite', 'requiredEvidenceSuite', 'importedUniverseSuite'):
        if key not in cases_doc:
            continue
        s = cases_doc[key]
        r1, r2 = run(s), run(s)
        if r1['route'] != 'ADMITTED':
            ids[key] = {'route': r1}
            continue
        res = r1['result']
        body = {k: v for k, v in res.items() if k != 'policyTestResultId'}
        valid = True
        try:
            W.projection_owner().validate_profile('urn:opensip:product-v1:workflows:policy-test#/$defs/PolicyTestResultV1', res)
        except Exception as exc:  # noqa: BLE001
            valid = type(exc).__name__
        expect = cases_doc.get(key + 'Expect') or {}
        ids[key] = {'suiteDigestIsH': res['suiteDigest'] == H('workflow.policy-test-suite', s),
                    'resultIdIsPolicytest2H': res['policyTestResultId'] == 'policytest2:' + H('workflow.policy-test-result', body),
                    'candidateDigestIsRawSha': res['candidatePolicyDigest'] == hashlib.sha256(C(s['candidatePolicy'])).hexdigest(),
                    'sameSuiteSameBytes': C(r1['result']) == C(r2['result']), 'resultSchemaValid': valid,
                    'summary': res['summary'], 'authorExpectedSummary': expect.get('summary'),
                    'authorOracleSummaryEqual (author oracle, not independent)': res['summary'] == expect.get('summary') if expect else None}
    out['identity'] = ids
    if production:
        out['production'] = production_side(DC)
    return out


def production_side(DC):
    E = load('pv40_composition_v3', DC / 'foundation/evaluator_composition_model.v3.py')

    def token(text):
        return hashlib.sha256(text.encode()).hexdigest()

    def compose(atom, requirement, missing, values, gate=True, waivers=NO_WAIVERS, subjects=True, evidence_kind='test'):
        r = {'ruleId': 'r', 'ruleProgramRef': {'contributionId': 'fixture', 'ruleStableId': 'r', 'semanticsMajor': 2, 'programDigest': E.sha(atom)},
             'enabled': True, 'severity': 'error' if gate else 'note', 'gate': gate, 'subjectEnumeration': {'universe': 'syntax', 'subjectKind': 'file'},
             'emitWhen': atom, 'evidenceUse': [{'kind': evidence_kind, 'requirement': requirement}]}
        policy = {'schemaFamily': 'opensip.product.policy', 'schemaMajor': 2, 'gateSeverityAtLeast': 'error', 'rules': [r]}
        detector = 'closure2:' + token('fixture-detector')
        universe = token('one')
        population = {}
        if subjects:
            sid = E.M.identifier('evaluation-subject', {'schemaVersion': 3, 'universe': universe, 'kind': 'file', 'nativeSubjectId': 'src/a.ts'})
            population[sid] = {'subjectId': sid, 'universe': universe, 'kind': 'file', 'collisionPopulationComplete': True,
                               'row': {'nativeSubjectId': 'src/a.ts', 'kind': 'file', 'path': 'src/a.ts', 'qualifiedName': 'src/a.ts',
                                       'subjectLanguage': 'typescript', 'signatureTokens': [], 'projections': []}}
        plan = {'policyDigest': E.sha(policy), 'waiverDigest': E.sha(waivers), 'semanticClosures': [detector], 'budget': {'unit': 'work-units', 'limit': 100000}}
        missing_rows = [{'source': 'import', 'cause': 'evidence-kind-unavailable', 'subjectId': None, 'predicateId': None, 'inputRefs': [],
                         'evidenceKind': evidence_kind, 'nativeCause': None, 'universe': None}] if missing else []
        inputs = {'plan': plan, 'planId': 'plan2:' + token('plan'), 'executionPlanId': 'exec-plan2:' + token('exec'), 'evaluatorClosure': 'closure2:' + token('eval'),
                  'policy': policy, 'effectiveWaivers': waivers,
                  'emissionPlan': {'schemaVersion': 1, 'policyDigest': plan['policyDigest'], 'rules': [{'ruleId': 'r', 'contributionId': 'fixture', 'ruleStableId': 'r',
                                   'semanticsMajor': 2, 'detectorClosure': detector, 'stabilityClass': 'path-stable', 'emissionProfile': 'declarative-subject-v1'}]},
                  'population': population,
                  'enumerations': {'r': {'state': 'complete', 'inventoryRefs': [], 'selectedSubjectIds': E.cset(population), 'unresolvedSubjectIds': [], 'incompleteInventoryRefs': []}},
                  'enumerationDeficiencies': {'r': []}, 'requiredEvidenceDeficiencies': {'r': missing_rows}, 'executionDeficiencies': [],
                  'executionInputsDigest': 'e' * 64, 'evaluationInputRefs': [{'domain': 'execution-inputs', 'digest': 'e' * 64}],
                  'inventoryRowCount': len(population), 'inventoryLocatorCount': len(population), 'factCount': 0, 'observationCount': 0, 'coverageCount': 0,
                  'importKinds': {}, 'closures': {detector: {'kind': 'detector'}}}

        def scan(rule_, subject, node, pid):
            value, source = values[node['relation']]
            ds = [] if value != 'indeterminate' else [{'source': source, 'cause': 'evidence-kind-unavailable' if source == 'import' else 'required-relation-missing',
                                                      'subjectId': subject['subjectId'], 'predicateId': pid, 'inputRefs': [],
                                                      'evidenceKind': node.get('evidence') if source == 'import' else None, 'nativeCause': None, 'universe': None}]
            return {'kind': 'imported-atom' if source == 'import' else 'native-atom', 'value': value, 'matchingFactIds': [], 'uncertainFactIds': [],
                    'matchingImportRows': [], 'uncertainImportRows': [], 'coverageIds': [], 'scopeIds': [], 'inputRefs': [], 'deficiencies': ds}
        proof = E.compose(inputs, scan)['proof']
        return {'verdict': proof['verdict'], 'ruleOutcome': proof['ruleResults'][0]['outcome'], 'findings': len(proof['findingIds']),
                'waived': len(proof['waivedFindingIds'])}
    OR = {'op': 'or', 'operands': [FILE_EXISTS, TEST_EXISTS]}
    AND = {'op': 'and', 'operands': [FILE_EXISTS, TEST_EXISTS]}
    TRUE_UNKNOWN = {'file': ('true', 'native'), 'test-execution': ('indeterminate', 'import')}
    FALSE_UNKNOWN = {'file': ('false', 'native'), 'test-execution': ('indeterminate', 'import')}
    RT_WAIVE = {'schemaFamily': 'opensip.product.waivers', 'schemaMajor': 1,
                'waivers': [{'waiverId': 'w', 'target': {'ruleId': 'r', 'subjectPath': 'src/a.ts'}, 'reason': 'accepted', 'expires': None}]}
    return {
        'A1-or-known-hit-required-missing': compose(OR, 'required', True, TRUE_UNKNOWN),
        'A2-or-known-hit-optional-missing': compose(OR, 'optional', False, TRUE_UNKNOWN),
        'A3-or-known-hit-required-present': compose(OR, 'required', False, {'file': ('true', 'native'), 'test-execution': ('false', 'import')}),
        'A4-and-known-false-required-missing': compose(AND, 'required', True, FALSE_UNKNOWN),
        'A5-advisory-known-hit-required-missing': compose(OR, 'required', True, TRUE_UNKNOWN, gate=False),
        'A6-waived-known-hit-required-missing': compose(OR, 'required', True, TRUE_UNKNOWN, waivers=RT_WAIVE),
        'A7-no-subjects-required-missing': compose(OR, 'required', True, TRUE_UNKNOWN, subjects=False),
        'G1-optional-imported-unknown-gating': compose(RUNTIME_HIT, 'optional', False, {'runtime-observation': ('indeterminate', 'import')}, evidence_kind='runtime'),
    }


# ------------------------------------------------------------------------------------------------ parent
def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(1 << 20), b''):
            h.update(c)
    return h.hexdigest()


def verify_copy(root, index_path, prefixes):
    idx = json.load(open(index_path))
    bad = [p for p, s in idx.items() if p.startswith(prefixes) and (not (root / p).is_file() or sha(root / p) != s)]
    return {'checked': sum(1 for p in idx if p.startswith(prefixes)), 'mismatched': bad[:20]}


def side(root, production=False):
    cmd = [sys.executable, '-I', '-B', str(Path(__file__).resolve()), '--side', str(root)] + (['--production'] if production else [])
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=3000)
    if p.returncode != 0:
        return {'error': p.stderr[-3000:], 'exit': p.returncode}
    return json.loads(p.stdout.strip().splitlines()[-1])


def parent():
    rows = []

    def row(case, ok, observed, expected=None, kind=None):
        r = {'case': case, 'ok': bool(ok), 'observed': observed}
        if expected is not None:
            r['expected'] = expected
        if kind:
            r['kind'] = kind
        rows.append(r)
    prefixes = ('docs/coop/design-corrections/workflows/', 'docs/coop/design-corrections/foundation/', 'docs/coop/design-corrections/native/')
    row('old-copy-equals-source39-manifest', not (vo := verify_copy(OLD, OLD_INDEX, prefixes))['mismatched'], vo)
    row('new-copy-equals-source40-manifest', not (vn := verify_copy(NEW, NEW_INDEX, prefixes))['mismatched'], vn)
    old, new = side(OLD), side(NEW, production=True)
    if 'error' in old or 'error' in new:
        row('sides-completed', False, {'old': old.get('error'), 'new': new.get('error')})
        return rows, old, new
    O, N, P = old['cases'], new['cases'], new['production']

    def verdict(c):
        return c.get('observedVerdict') if c.get('route') == 'ADMITTED' else c.get('route')

    # S39-01 discrimination and composition agreement
    row('S39-01-source39-bytes-lose-the-known-hit (discriminating baseline)', verdict(O['A1-or-known-hit-required-missing']) == 'indeterminate'
        and O['A1-or-known-hit-required-missing'].get('findings') == [], O['A1-or-known-hit-required-missing'])
    for name in ('A1-or-known-hit-required-missing', 'A2-or-known-hit-optional-missing', 'A3-or-known-hit-required-present',
                 'A4-and-known-false-required-missing', 'A6-waived-known-hit-required-missing', 'A7-no-subjects-required-missing'):
        n, p = N[name], P[name]
        row('source40-fixture-verdict-and-finding-presence-equal-production-' + name,
            verdict(n) == p['verdict'] and bool(n.get('findings')) == (p['findings'] > 0), {'fixture': n, 'production': p})
    n5, p5 = N['A5-advisory-known-hit-required-missing'], P['A5-advisory-known-hit-required-missing']
    row('advisory-rule-fixture-advisory-display-over-production-pass-with-finding', verdict(n5) == 'advisory' and p5['verdict'] == 'pass' and p5['findings'] == 1,
        {'fixture': n5, 'production': p5}, 'workflows section 5 verdict vocabulary: advisory is the surface display of pass with live advisory findings (composition section 5)')
    row('required-missing-rule-listed-in-indeterminateRules-even-with-a-known-gating-fail (section 5 source40 sentence)',
        'r' in (N['A1-or-known-hit-required-missing'].get('indeterminateRules') or []) and P['A1-or-known-hit-required-missing']['ruleOutcome'] == 'fail',
        {'fixtureIndeterminateRules': N['A1-or-known-hit-required-missing'].get('indeterminateRules'), 'productionRuleOutcome': P['A1-or-known-hit-required-missing']['ruleOutcome']},
        None, 'observation')
    row('optional-missing-is-not-listed-and-required-missing-is (required versus optional distinguished)',
        'r' not in (N['A2-or-known-hit-optional-missing'].get('indeterminateRules') or []) and 'r' in (N['A1-or-known-hit-required-missing'].get('indeterminateRules') or []),
        {'optional': N['A2-or-known-hit-optional-missing'].get('indeterminateRules'), 'required': N['A1-or-known-hit-required-missing'].get('indeterminateRules')})
    # S39-02 discrimination
    b1o, b1n = O['B1-rule-token-typescript-v2-fact-typescript'], N['B1-rule-token-typescript-v2-fact-typescript']
    row('S39-02-source39-admits-typescript-v2-rule-token (discriminating baseline)', b1o.get('route') == 'ADMITTED', b1o)
    row('source40-typescript-v2-rule-token-is-resolver-refusal-POLICY.UNKNOWN_RULE',
        b1n.get('route') == 'RESOLVER-REFUSED' and (b1n.get('errorCode'), b1n.get('detail')) == ('CONFIG.INVALID', 'POLICY.UNKNOWN_RULE')
        and str(b1n.get('remedy')).startswith('EVALUATOR_POLICY_UNIVERSE_UNREGISTERED') and b1n.get('resolverAccepted') is False, b1n)
    b2o, b2n = O['B2-disabled-rule-arbitrary-token'], N['B2-disabled-rule-arbitrary-token']
    row('source40-disabled-rule-with-unregistered-token-still-refuses', b2n.get('route') == 'RESOLVER-REFUSED' and b2n.get('detail') == 'POLICY.UNKNOWN_RULE',
        {'source39': b2o, 'source40': b2n})
    b3o, b3n = O['B3-fact-token-typescript-v2'], N['B3-fact-token-typescript-v2']
    row('source40-fixture-fact-token-typescript-v2-is-admission-CONFIG.INVALID', b3n.get('route') == 'ADMISSION-REFUSED'
        and (b3n.get('errorCode'), b3n.get('detail')) == ('CONFIG.INVALID', 'CONFIG.INVALID'), {'source39': b3o, 'source40': b3n})
    reg = [N[k] for k in ('B4-registered-typescript', 'B4-registered-rust', 'B4-registered-syntax')]
    row('every-registered-token-admits-with-the-same-outcome', all(r.get('route') == 'ADMITTED' for r in reg)
        and len({json.dumps({k: r.get(k) for k in ('observedVerdict', 'findings', 'indeterminateRules')}) for r in reg}) == 1, reg)
    # imported fact universe
    c1o, c1n = O['C1-foreign-universe-imported-runtime-hit'], N['C1-foreign-universe-imported-runtime-hit']
    row('source39-foreign-universe-imported-row-created-a-known-hit (discriminating baseline)', bool(c1o.get('findings')) and verdict(c1o) == 'fail', c1o)
    row('source40-foreign-universe-imported-row-creates-no-known-hit', c1n.get('route') == 'ADMITTED' and not c1n.get('findings')
        and verdict(c1n) == 'indeterminate', c1n)
    c2o, c2n = O['C2-same-universe-imported-runtime-hit'], N['C2-same-universe-imported-runtime-hit']
    row('same-universe-imported-hit-control-fails-on-both-byte-sets', bool(c2o.get('findings')) and bool(c2n.get('findings'))
        and verdict(c2o) == verdict(c2n) == 'fail', {'source39': c2o, 'source40': c2n})
    c3o, c3n = O['C3-foreign-universe-native-file-fact'], N['C3-foreign-universe-native-file-fact']
    row('foreign-universe-native-fact-control-never-occupied-on-either-byte-set', not c3o.get('findings') and not c3n.get('findings'),
        {'source39': c3o, 'source40': c3n})
    # optional imported representation limit
    g1, g2, pg = N['G1-optional-imported-available-no-row'], N['G2-optional-imported-absent'], P['G1-optional-imported-unknown-gating']
    row('observation-optional-imported-evidence-available-without-a-row-is-a-blocking-fixture-unknown',
        True, {'fixtureAvailableNoRow': verdict(g1), 'fixtureAbsent': verdict(g2), 'productionOptionalOnlyUnknown': pg},
        'schema ruleLaw: a fixture representation limit is a blocking cause; composition section 5: optional-only root unknown stays pass', 'observation')
    # policy.show and identity
    row('policy-show-inspection-resolver-accepts-an-unregistered-token-and-the-record-is-schema-valid', True,
        {'source39': old.get('policyShow'), 'source40': new.get('policyShow'), 'evaluatorInputAdmissionRefuses': new.get('evaluatorInputAdmissionRefusesUnregisteredToken')},
        None, 'observation')
    for key, ident in new['identity'].items():
        ok = isinstance(ident, dict) and all(ident.get(k) is True for k in ('suiteDigestIsH', 'resultIdIsPolicytest2H', 'candidateDigestIsRawSha', 'sameSuiteSameBytes', 'resultSchemaValid'))
        row('source40-identity-preimages-' + key, ok, ident)
    return rows, old, new


if __name__ == '__main__':
    if '--side' in sys.argv:
        root = sys.argv[sys.argv.index('--side') + 1]
        try:
            result = child(root, '--production' in sys.argv)
        except Exception:  # noqa: BLE001
            result = {'crash': traceback.format_exc()[-3000:]}
        print(json.dumps(result, default=str))
    else:
        try:
            rows, old, new = parent()
        except Exception:  # noqa: BLE001
            rows, old, new = [{'case': 'probe-crashed', 'ok': False, 'observed': traceback.format_exc()[-3000:]}], None, None
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps({'standing': 'independent reviewer discrimination probe; fixture evaluator on source39 and source40 bytes in separate processes; bounded production composition on source40',
                                   'rows': rows, 'failed': [r for r in rows if not r['ok']], 'sides': {'source39': old, 'source40': new}}, indent=1, default=str))
        print(json.dumps({'total': len(rows), 'failed': [(r['case'], r['observed']) for r in rows if not r['ok']]}, indent=1, default=str)[:8000])
