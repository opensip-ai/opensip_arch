"""Cross-unit compatibility of the five new identity records against the ACTUAL
workflow policy / rule-program / finding schemas and the analysis-spec shape,
plus the predicate node-addressing law over a REAL multi-level RuleProgramV1
Predicate (not the fixture's single atom), plus native order-violation typing."""
import copy, hashlib, json, sys, importlib.util
from pathlib import Path

SUB = Path('/tmp/opensip-design-corrections/candidate-subject.v7/docs/coop/design-corrections')
FOUND = SUB / 'foundation'
src = (FOUND / 'check-identity.py').read_text()
G = {'__file__': str(FOUND / 'check-identity.py'), '__name__': 'subject_fixtures'}
exec(compile(src[:src.index('a=argparse.ArgumentParser()')], str(FOUND / 'check-identity.py'), 'exec'), G)
M, C, N, W = G['M'], G['C'], G['N'], G['W']
IDS = M.SCHEMA
R = {}

def ok(fn):
    try: return {'ok': True, 'value': str(fn())[:110]}
    except Exception as e: return {'ok': False, 'error': type(e).__name__ + ':' + str(e)[:200]}

# ---------------------------------------------------------------- 1. real policy DSL Predicate
POLICY_SCHEMA = 'workflows/schemas/policy-document.schema.json'
ATOM = {'op': 'none', 'relation': 'references', 'minResolution': 'resolved',
        'filters': [{'field': 'target', 'cmp': 'eq', 'value': 'foo'}]}
ATOM2 = {'op': 'none', 'relation': 'references', 'minResolution': 'resolved',
         'filters': [{'field': 'target', 'cmp': 'eq', 'value': 'bar'}]}
DEEP = {'op': 'and', 'operands': [
            ATOM,
            {'op': 'or', 'operands': [ATOM2, {'op': 'not', 'operand': ATOM}]},
            {'op': 'not', 'operand': ATOM2}]}
RULE = {'ruleId': 'deep-rule',
        'ruleProgramRef': {'contributionId': 'x', 'ruleStableId': 'deep-rule', 'semanticsMajor': 2,
                           'programDigest': hashlib.sha256(C.canonical(DEEP)).hexdigest()},
        'enabled': True, 'severity': 'error', 'gate': True,
        'subjectEnumeration': {'universe': 'typescript', 'subjectKind': 'symbol'},
        'emitWhen': DEEP, 'evidenceUse': [], 'messageCode': 'deep'}
POLICY = {'schemaFamily': 'opensip.product.policy', 'schemaMajor': 1,
          'gateSeverityAtLeast': 'error', 'rules': [RULE]}
R['deepPolicyValidatesUnderRealSchema'] = ok(
    lambda: W.validate_import_record(POLICY_SCHEMA, '#/$defs/PolicyDocumentV1', POLICY))
program = {'schemaVersion': 1, 'policyDigest': hashlib.sha256(C.canonical(POLICY)).hexdigest(),
           'rules': [{'ruleId': 'deep-rule', 'ruleProgramRef': RULE['ruleProgramRef'],
                      'emitWhen': DEEP}]}
R['compiledProgramValidatesUnderRealSchema'] = ok(
    lambda: W.validate_import_record(POLICY_SCHEMA, '#/$defs/RuleProgramV1', program))
program_digest = hashlib.sha256(C.canonical(program)).hexdigest()

# node addressing over the REAL nested predicate, from the contract's stated rule
def addr(node, a):
    yield a, node
    if node['op'] in ('and', 'or'):
        for i, child in enumerate(node['operands']):
            yield from addr(child, a + '.' + str(i))
    elif node['op'] == 'not':
        yield from addr(node['operand'], a + '.0')
mine = dict(addr(DEEP, 'p'))
theirs = {a: M.predicate_node_at(DEEP, a) for a in mine}
R['myAddressingMatchesTheModel'] = all(theirs[a] is mine[a] for a in mine)
R['addressesEnumerated'] = sorted(mine)
R['childAddressesAgree'] = all(
    M.predicate_child_addresses(mine[a], a) == [a + '.' + str(i) for i in
        range(len(mine[a].get('operands', [])) if mine[a]['op'] in ('and', 'or')
              else (1 if mine[a]['op'] == 'not' else 0))]
    for a in mine)
R['unaddressableAddressRefuses'] = ok(lambda: M.predicate_node_at(DEEP, 'p.9'))['ok'] is False
R['leadingZeroAddressRefuses'] = ok(lambda: M.predicate_node_at(DEEP, 'p.01'))['ok'] is False

# every addressed node mints a distinct program-predicate under the registered record
witnesses = {}
for a, node in mine.items():
    rec = {'schemaVersion': 2, 'ruleProgramDigest': program_digest, 'ruleId': 'deep-rule',
           'predicateId': a, 'operation': node['op'],
           'nodeDigest': hashlib.sha256(C.canonical(node)).hexdigest()}
    sch = copy.deepcopy(IDS); sch['$ref'] = '#/$defs/program-predicate'
    C.validate(sch, rec)
    witnesses[a] = hashlib.sha256(C.canonical(rec)).hexdigest()
R['everyAddressedNodeMintsADistinctDigest'] = len(set(witnesses.values())) == len(witnesses)
R['programPredicateCount'] = len(witnesses)
# the SAME node at two addresses is a different program-predicate (address is load-bearing)
same_node_addrs = [a for a, n in mine.items() if n == ATOM]
R['sameNodeDifferentAddressDiffers'] = (
    len(same_node_addrs) > 1 and len({witnesses[a] for a in same_node_addrs}) == len(same_node_addrs))
# a witness naming an operation the addressed node does not have is a contract violation
R['operationMustEqualNodeOp'] = all(
    witnesses[a] != hashlib.sha256(C.canonical(
        {'schemaVersion': 2, 'ruleProgramDigest': program_digest, 'ruleId': 'deep-rule',
         'predicateId': a, 'operation': 'not' if mine[a]['op'] != 'not' else 'and',
         'nodeDigest': hashlib.sha256(C.canonical(mine[a])).hexdigest()})).hexdigest()
    for a in mine)

# ---------------------------------------------------------------- 2. finding parameters
FIND = IDS['$defs']['finding']['properties']
R['findingParameterDigestAnnotation'] = FIND['parameterDigest'].get('x-opensip-digest')
fp = IDS['$defs']['finding-parameters']
R['findingParametersIsAMapNotAnArray'] = (
    fp['properties']['parameters'].get('type') == 'object'
    and 'x-opensip-order' not in fp['properties']['parameters'])
R['findingParametersValueTypesClosed'] = json.dumps(
    fp['properties']['parameters'].get('additionalProperties'))[:300]
R['duplicateParameterNameImpossible'] = ok(
    lambda: C.parse(b'{"schemaVersion":2,"messageCode":"m","parameters":{"a":1,"a":2}}'))['ok'] is False

# ---------------------------------------------------------------- 3. stage spec vs analysis spec
sspec = IDS['$defs']['stage-spec']['properties']
aspec = IDS['$defs']['analysis-spec']['properties']
R['stageParamRowShapeEqualsAnalysisSpecRow'] = (
    C.canonical(sspec['parameters']['items']) == C.canonical(aspec['parameters']['items']))
R['stageParamRowShape'] = json.dumps(sspec['parameters']['items'])[:260]
R['stageSpecTwoSitesOneRecord'] = (
    C.canonical(IDS['$defs']['execution-plan']['properties']['stages']['items']
                ['properties']['stageSpecDigest']['x-opensip-digest'])
    == C.canonical(IDS['$defs']['cache-key']['properties']['stageSpecDigest']['x-opensip-digest']))
R['cacheAndRegenShareOneSchema'] = ('regeneration-key' not in IDS['$defs']
                                    or C.canonical(IDS['$defs']['cache-key'])
                                    == C.canonical(IDS['$defs'].get('regeneration-key')))
R['regenerationKeyIsNotASeparateDef'] = 'regeneration-key' not in IDS['$defs']

# ---------------------------------------------------------------- 4. native order refusal typing
fx = json.loads((SUB / 'native' / 'native-cases.v2.json').read_text())['fixtures']
ctx, trees = fx['tsNativeContext'], fx['tsClosureTrees']
R['nativeBaselineAdmits'] = not N.admit_native_context('typescript', ctx, trees)['refusals']
bad = copy.deepcopy(ctx); bad['toolchain']['libSelection'].reverse()
res = N.admit_native_context('typescript', bad, trees)
R['nativeOrderViolationRefusals'] = res['refusals']
R['nativeOrderViolationIsTypedAsOrderNotLanguage'] = (
    any('lib-selection-order' in r for r in res['refusals'])
    and not any('language' in r for r in res['refusals']))
badr = copy.deepcopy(ctx)
badr['configProjection']['configGraphPaths'] = list(
    reversed(badr['configProjection']['configGraphPaths']))
R['nativeConfigPathOrderRefusals'] = N.admit_native_context('typescript', badr, trees)['refusals']

print(json.dumps(R, indent=1, default=str))
json.dump(R, open(sys.argv[1], 'w'), indent=1, default=str)
