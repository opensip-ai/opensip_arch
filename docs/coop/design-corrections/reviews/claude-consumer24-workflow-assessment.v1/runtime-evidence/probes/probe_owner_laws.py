"""Discriminating probes for consumer24 items M4 M5 S5 S6 S7 A6 A8 A9 A11 A12 A13 A14 against one frozen tree.

usage: python -I -B probe_owner_laws.py TREE      (TREE = source37 | source38)
Read-only over /tmp/opensip-design-corrections/candidate-subject.v37|v38 and consumer-b.v24 exported vectors (diagnostic
inputs only, never an oracle). Every loaded file is hashed into the receipt. Each section is isolated; failures are
recorded, not hidden. Reference Python models are exercised as the owners' executable references; conclusions about
normative law come from the contract/schema text, not from model behaviour alone.
"""
import copy, hashlib, importlib.util, json, os, re, sys, traceback

RT = '/private/tmp/opensip-design-corrections/claude-consumer24-workflow-assessment.v1'
TREE = sys.argv[1]
ROOT = {'source37': '/tmp/opensip-design-corrections/candidate-subject.v37',
        'source38': '/tmp/opensip-design-corrections/candidate-subject.v38'}[TREE]
DC = ROOT + '/docs/coop/design-corrections'
CONSUMER = '/tmp/opensip-design-corrections/consumer-b.v24'
loaded = {}


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def track(p):
    loaded[os.path.relpath(p, '/tmp/opensip-design-corrections')] = sha(p)
    return p


def load(name, rel):
    p = track(DC + '/' + rel)
    s = importlib.util.spec_from_file_location(name, p)
    m = importlib.util.module_from_spec(s)
    sys.modules[name] = m
    s.loader.exec_module(m)
    return m


sys.path.insert(0, DC + '/foundation')
import canonical  # noqa: E402
track(DC + '/foundation/canonical.py')
from referencing import Registry, Resource  # noqa: E402
from referencing.jsonschema import DRAFT202012  # noqa: E402

docs = {}
for d in (DC + '/workflows/schemas', DC + '/workflows/schemas/evaluator3'):
    for f in sorted(os.listdir(d)):
        if f.endswith('.json'):
            doc = json.load(open(track(os.path.join(d, f))))
            if '$id' in doc:
                docs[doc['$id']] = doc
REG = Registry().with_resources([(k, Resource(contents=v, specification=DRAFT202012)) for k, v in docs.items()])
E3 = 'urn:opensip:product-v1:workflows:evaluator3:'


def validate(ref, value):
    try:
        canonical.typed(value)
        canonical.ExactValidator({'$ref': ref}, registry=REG).validate(value)
        return {'result': 'ADMIT'}
    except Exception as exc:
        return {'result': 'REFUSE', 'type': type(exc).__name__, 'message': str(exc).splitlines()[0][:220],
                'validator': getattr(exc, 'validator', None), 'path': list(getattr(exc, 'absolute_path', []) or [])}


def attempt(fn):
    try:
        v = fn()
        return {'result': 'OK', 'value': v}
    except Exception as exc:
        return {'result': 'RAISED', 'type': type(exc).__name__, 'message': str(exc).splitlines()[0][:220] if str(exc) else '',
                'errorCode': getattr(exc, 'error_code', None), 'detail': getattr(exc, 'detail', None)}


res = {'tree': TREE, 'sections': {}}


def section(name, fn):
    try:
        res['sections'][name] = fn()
    except Exception:
        res['sections'][name] = {'error': traceback.format_exc()[-2500:]}


REQ = 'req1_' + 'a' * 32
W = load('probe_wm1_' + TREE, 'workflows/workflows_model.v1.py')
P = load('probe_wpm3_' + TREE, 'workflows/workflow_projection_model.v3.py')
INV = json.load(open(track(DC + '/workflows/command-inventory.v3.json')))


def m4():
    out = {}
    bschema = docs[E3 + 'baseline:2']['$defs']
    out['DetectorClosureEntry.detectorId'] = bschema['DetectorClosureEntry']['properties']['detectorId']
    out['BaselineEntry.detectorId'] = bschema['BaselineEntry']['properties']['detectorId']
    art = json.load(open(track(CONSUMER + '/output/vectors/baseline-audit.json')))['baselineArtifact']
    d = art['descriptor']
    out['consumerDetectorRows'] = [{'detectorId': x['detectorId'], 'contributionId': x['contributionId']} for x in d['detectorClosure']]
    out['originalVerify'] = attempt(lambda: P.verify_baseline_artifact_v3(art))
    rename = {x['detectorId']: x['detectorId'] + '-alt' for x in d['detectorClosure']}
    var = copy.deepcopy(art)
    for x in var['descriptor']['detectorClosure']:
        x['detectorId'] = rename[x['detectorId']]
    for x in var['descriptor']['entries']:
        x['detectorId'] = rename.get(x['detectorId'], x['detectorId'])
    var['baselineId'] = 'baseline2:' + canonical.identity('workflow.baseline', var['descriptor'])
    out['variant'] = {'detectorIdDiffersFromContributionId': all(x['detectorId'] != x['contributionId'] for x in var['descriptor']['detectorClosure']),
                      'schema': validate(E3 + 'baseline:2', var),
                      'ownerVerify': attempt(lambda: P.verify_baseline_artifact_v3(var)),
                      'baselineIdOriginal': art['baselineId'], 'baselineIdVariant': var['baselineId'],
                      'baselineIdsDiffer': art['baselineId'] != var['baselineId']}
    out['e0JoinSameMap'] = attempt(lambda: P.require_exact_detector_map(d['detectorClosure'], d['detectorClosure'], 'E0'))
    out['e0JoinVariantVsOriginal'] = attempt(lambda: P.require_exact_detector_map(var['descriptor']['detectorClosure'], d['detectorClosure'], 'E0'))
    src = open(DC + '/workflows/workflow_projection_model.v3.py').read()
    out['referenceModelDerivation'] = {'detectorIdFromContributionIdLines': len(re.findall(r'"detectorId":\s*(binding\["contributionId"\]|did)', src)),
                                       'pivotDetectorDocstring': 'One detector row per contributionId' in src}
    kit = [os.path.join(dp, f) for dp, _, fs in os.walk(CONSUMER + '/subject/docs') for f in fs]
    out['kitFilesMentioningDetectorId'] = sorted(os.path.relpath(p, CONSUMER + '/subject') for p in kit if 'detectorId' in open(p, errors='replace').read())
    return out


def m5():
    out = {}
    env_schema = docs[E3 + 'command-envelope:3']
    out['envelopeAdditionalProperties'] = env_schema.get('additionalProperties')
    out['envelopeProperties'] = sorted(env_schema['properties'])
    out['anyEnvelopeRefToGraphQueryResponse'] = 'GraphQueryResponseV1' in json.dumps(env_schema)
    qr = {'kind': 'query', 'items': 0, 'truncated': False, 'completenessMet': True, 'advisory': False}
    base = {'schemaFamily': 'opensip.product.envelope', 'schemaMajor': 3, 'kind': 'query', 'requestId': REQ,
            'termination': {'class': 'success'}, 'exitCode': 0, 'projectId': 'prj1-' + 'b' * 64, 'query': qr}
    out['baseQueryEnvelope'] = validate(E3 + 'command-envelope:3', base)
    out['envelopePlusQueryResponse'] = validate(E3 + 'command-envelope:3', dict(base, queryResponse={'schemaFamily': 'opensip.product.query'}))
    qcmd = next(c for c in INV['commands'] if 'query-response' in c.get('parityFields', []))
    out['queryCommandParityFields'] = qcmd['parityFields']
    out['jsonRendererParityRule'] = next(r['parityRule'] for r in INV['renderers'] if r['format'] == 'json')
    parity = {k: None for k in qcmd['parityFields']}
    rendering = attempt(lambda: sorted(W.render({'parity': parity, 'envelope': base}, 'json', qcmd)))
    out['referenceJsonRenderingTopLevelKeys'] = rendering
    missing = dict(parity)
    missing.pop('query-response')
    out['referenceRenderMissingQueryResponse'] = attempt(lambda: W.render({'parity': missing, 'envelope': base}, 'json', qcmd))
    return out


FAULT = {'HOST.IO_FAILURE': 'host-io', 'DELIVERY.REQUIRED_FAILED': 'delivery-required'}


def failure_env(term, exit_code, errors=None):
    env = {'schemaFamily': 'opensip.product.envelope', 'schemaMajor': 3, 'kind': 'failure', 'requestId': REQ, 'termination': term, 'exitCode': exit_code}
    if errors is not None:
        env['errors'] = errors
    return env


def s6():
    out = {'goldenSchemaRequired': docs[E3 + 'command-inventory:3']['$defs']['Golden']['required']}
    codes = docs[E3 + 'common:3']['$defs']['DomainDetailCode']['enum']
    out['candidateDetailCodes'] = sorted(c for c in codes if c.startswith(('DOCTOR.', 'ENVELOPE.', 'QUERY.VIEW', 'OUTPUT.')) or 'SCHEMA_MAJOR' in c)
    goldens = {g['id']: g for g in INV['goldens']}
    for gid in ('doctor-report-not-producible', 'query-latest-empty', 'envelope-major-unsupported'):
        g = goldens[gid]
        term = {'class': g['class'], 'errorCode': g['errorCode']}
        if g['class'] == 'operational-failed':
            term['faultCause'] = FAULT[g['errorCode']]
        row = {'golden': g, 'failureEnvelopeWithoutErrors': validate(E3 + 'command-envelope:3', failure_env(term, g['exitCode']))}
        if gid == 'query-latest-empty':
            det = {'code': 'QUERY.VIEW_UNKNOWN', 'remedy': g['remedy']}
            row['withOwnerDetailQueryViewUnknown'] = validate(E3 + 'command-envelope:3', failure_env(dict(term, domainDetail=det), g['exitCode'], [det]))
        out[gid] = row
    out['doctorKindWithoutReport'] = validate(E3 + 'command-envelope:3', {'schemaFamily': 'opensip.product.envelope', 'schemaMajor': 3, 'kind': 'doctor', 'requestId': REQ,
                                                                          'termination': {'class': 'operational-failed', 'errorCode': 'HOST.IO_FAILURE', 'faultCause': 'host-io'}, 'exitCode': 4})
    wf = open(track(ROOT + '/docs/v2/contracts/product-v1/workflows-and-surfaces.md')).read()
    out['workflowsSaysGoldensIncludeDetails'] = 'Goldens include actual security,\nnative and evidence-availability details, rather than leaving the detail absent.' in wf
    qc = open(track(DC + '/workflows/query-projection-contract.v3.md')).read()
    out['queryContractEmptyLatestRow'] = [l for l in qc.splitlines() if 'latest' in l and 'QUERY.VIEW_UNKNOWN' in l][:3]
    return out


def a13():
    out = {}
    term = {'class': 'operational-failed', 'errorCode': 'DELIVERY.REQUIRED_FAILED', 'faultCause': 'delivery-required'}
    out['requiredDeliveryNoRunNoErrors'] = validate(E3 + 'command-envelope:3', failure_env(term, 4))
    det = {'code': 'DELIVERY.RENDERER_FAILED_AFTER_COMMIT', 'remedy': 'x'}
    out['requiredDeliveryNoRunWithAfterCommitDetail'] = validate(E3 + 'command-envelope:3', failure_env(dict(term, domainDetail=det), 4, [det]))
    codes = docs[E3 + 'common:3']['$defs']['DomainDetailCode']['enum']
    out['deliveryDetailCodes'] = sorted(c for c in codes if c.startswith('DELIVERY.'))
    return out


def a11():
    out = {}
    te = 'urn:opensip:product-v1:workflows:test-execution#/$defs/TestExecutionStepParams'
    base = {'kind': 'test-execution', 'argv': ['bin/test'], 'argv0Source': {'kind': 'snapshot-member', 'path': 'bin/test'}, 'cwdIsRoot': True,
            'principal': 'P-TRUSTED-REPO', 'executionClass': 'test-runner', 'platformId': 'linux-x86_64-gnu',
            'authorizationRef': 'security.repo-execution-grant.v2:' + 'a' * 64, 'consentSource': 'pre-existing-policy',
            'timeoutMilliseconds': 1000, 'maxOutputBytes': 1024, 'environmentAllowlist': [],
            'effects': {'network': 'DISCLOSURE-ONLY', 'subprocess': 'DISCLOSURE-ONLY', 'filesystemWrite': 'DISCLOSURE-ONLY', 'environment': 'ENFORCED-BY-CONSTRUCTION'}}
    chosen = None
    for step in ('analyze', 'analysis', 's1', 'step-1', 'a'):
        v = validate(te, dict(base, afterStep=step))
        if v['result'] == 'ADMIT':
            chosen = step
            break
    out['baseAfterStep'] = chosen
    b = dict(base, afterStep=chosen or 'analyze')
    out['baseParams'] = validate(te, b)
    out['platformPrimitiveEffect'] = validate(te, dict(b, effects=dict(b['effects'], network='ENFORCED-PLATFORM:seatbelt')))
    sec = json.load(open(track(DC + '/security/security-lifecycle.schemas.v1.json')))
    pat = None

    def find(o):
        nonlocal pat
        if isinstance(o, dict):
            if 'EnforcementV1' in o and isinstance(o['EnforcementV1'], dict):
                pat = o['EnforcementV1'].get('pattern')
            for v in o.values():
                find(v)
        elif isinstance(o, list):
            for v in o:
                find(v)
    find(sec)
    out['securityEnforcementV1Pattern'] = pat
    out['securityPatternAdmitsPlatformPrimitive'] = bool(pat and re.search(pat.replace('(?![\\s\\S])', '$'), 'ENFORCED-PLATFORM:seatbelt'))
    tt = open(track(ROOT + '/docs/coop/artifacts/permission-truth-tables.v9.json')).read()
    out['truthTablePlatformPrimitiveOccurrences'] = tt.count('ENFORCED-PLATFORM')
    return out


def a12():
    rule = {'enabled': True, 'gating': True, 'evidenceUse': []}
    fp = 'finding-key2:' + '1' * 64
    cases = {
        'detection-hidden-code-net-new': {'B': False, 'E0': True, 'E1': False, 'E2': False, 'E3': False, 'E4': False, 'waivedB': False, 'waivedC': False},
        'policy-hidden-code-net-new': {'B': False, 'E0': True, 'E1': True, 'E2': False, 'E3': False, 'E4': False, 'waivedB': False, 'waivedC': False},
    }
    out = {}
    for name, pres in cases.items():
        r = attempt(lambda pres=pres: W.classify(fp, 'r1', pres, rule, rule, {'imports': []}, {'imports': []},
                                                 {'detectorId': 'd1', 'method': 'three-way-pivot'}, W.AUDIT_PROFILES['code-regression']))
        if r['result'] == 'OK':
            e, sig = r['value']
            r = {k: e.get(k) for k in ('classification', 'subsequentDeltas', 'liveInCurrent', 'gates', 'gateReason')}
            r['verdictSignal'] = sig
        out[name] = r
    out['gateReasonEnum'] = docs[E3 + 'comparison:2']['$defs']['Entry']['properties']['gateReason']['enum']
    return out


def s7():
    rule = {'enabled': True, 'gating': True, 'evidenceUse': []}
    fp = 'finding-key2:' + '2' * 64
    pres = {'B': True, 'E0': False, 'E1': False, 'E2': False, 'E3': False, 'E4': False, 'waivedB': False, 'waivedC': False}
    out = {'note': 'current E4 unknown absence (rule root unknown / incomplete enumeration) has only boolean E4 in the owner presence model'}
    r = attempt(lambda: W.classify(fp, 'r1', pres, rule, rule, {'imports': []}, {'imports': []},
                                   {'detectorId': 'd1', 'method': 'identical-closure'}, W.AUDIT_PROFILES['code-regression']))
    if r['result'] == 'OK':
        e, sig = r['value']
        r = {k: e.get(k) for k in ('classification', 'direction', 'gates', 'indeterminateReason')}
        r['verdictSignal'] = sig
    out['ownerClassifyUnknownCurrentAbsenceAsFalse'] = r
    entry = {'fingerprint': fp, 'ruleId': 'r1', 'detectorId': 'd1', 'classification': 'INDETERMINATE', 'subsequentDeltas': [], 'liveInCurrent': False, 'gates': False,
             'presence': dict(pres, E4=None)}
    out['schemaEntryE4Null'] = validate(E3 + 'comparison:2#/$defs/Entry', dict(entry, indeterminateReason='pivot-reevaluation-unavailable'))
    out['schemaEntryE4FalseIndeterminateAnyReason'] = validate(E3 + 'comparison:2#/$defs/Entry', dict(entry, presence=pres, indeterminateReason='pivot-reevaluation-unavailable'))
    out['indeterminateReasonEnum'] = docs[E3 + 'comparison:2']['$defs']['IndeterminateReason']['enum']
    wf = open(ROOT + '/docs/v2/contracts/product-v1/workflows-and-surfaces.md').read()
    out['workflowsUnknownRootsNoNegative'] = 'Unknown\nroots, incomplete enumeration, disabled evaluation and exhausted budgets do\nnot establish a negative result.' in wf
    src = open(DC + '/workflows/workflow_projection_model.v3.py').read()
    out['modelE4DerivedAsBool'] = src.count('e4 = bool(')
    return out


def a6():
    E = load('probe_comp3_' + TREE, 'foundation/evaluator_composition_model.v3.py')
    clo = 'closure2:' + 'c' * 64
    rule = {'ruleProgramRef': {'ruleStableId': 'rs', 'semanticsMajor': 1}}
    binding = {'detectorClosure': clo}
    u = 'd' * 64

    def subj(sid, tokens, complete, name='f'):
        return {'subjectId': sid, 'universe': u, 'kind': 'symbol', 'collisionPopulationComplete': complete,
                'row': {'projections': [{'closureId': clo, 'signatureTokens': tokens}], 'subjectLanguage': 'typescript', 'path': 'a.ts', 'qualifiedName': name}}
    s1 = 'subject3:' + '1' * 64
    s2 = 'subject3:' + '2' * 64
    out = {}
    a = subj(s1, [], False)
    out['emptyTokensAndIncompletePopulation'] = attempt(lambda: list(E.correspondence(rule, binding, a, {s1: a})))
    b1, b2 = subj(s1, ['t'], False), subj(s2, ['t'], False)
    out['incompletePopulationAndSharedSignature'] = attempt(lambda: list(E.correspondence(rule, binding, b1, {s1: b1, s2: b2})))
    c1, c2 = subj(s1, ['t'], True), subj(s2, ['t'], True)
    out['completePopulationSharedSignature'] = attempt(lambda: list(E.correspondence(rule, binding, c1, {s1: c1, s2: c2})))

    def rec(cause):
        return {'source': 'correspondence', 'cause': cause, 'subjectId': s1, 'predicateId': 'p', 'inputRefs': [], 'evidenceKind': None, 'nativeCause': None, 'universe': None}
    first_only = E.cset([rec('population-incomplete')])
    all_rows = E.cset([rec('population-incomplete'), rec('signature-ambiguous')])
    out['deficiencyCsetDigest'] = {'firstApplicableOnly': hashlib.sha256(canonical.canonical(first_only)).hexdigest(),
                                   'everyApplicableRow': hashlib.sha256(canonical.canonical(all_rows)).hexdigest()}
    out['findingReasonCandidates'] = ['population-incomplete', 'signature-ambiguous']
    comp = open(track(DC + '/foundation/evaluator-composition-contract.v3.md')).read()
    out['contractPrecedenceStated'] = any(w in comp for w in ('precedence', 'first applicable', 'in table order', 'checked in order'))
    return out


def a9():
    comp = open(DC + '/foundation/evaluator-composition-contract.v3.md').read()
    src = open(DC + '/foundation/evaluator_composition_model.v3.py').read()
    return {'contractOutcomeSentence': [l for l in comp.splitlines() if l.startswith('A rule gates iff')][:1],
            'modelUnknownLine': [l.strip()[:220] for l in src.splitlines() if "requiredEvidenceDeficiencies'][rid])" in l][:2],
            'modelOutcomeLine': [l.strip() for l in src.splitlines() if l.strip().startswith("outcome='fail' if gating and live")][:1]}


def a8():
    out = {}
    Q = load('probe_query3_' + TREE, 'workflows/query_projection_model.v3.py')
    SR = load('probe_semrep3_' + TREE, 'foundation/check-semantic-replay.v3.py')
    g, packed, actual = SR.case_declares_exists()
    run, objects, blobs = packed
    sym = next(r for r in g['inputs']['population'].values() if r['kind'] == 'symbol')
    req = {'schemaFamily': 'opensip.product.query', 'schemaMajor': 3, 'projectId': 'prj1-' + '0' * 64, 'view': {'runId': actual['runId']},
           'operation': 'graph.neighbors', 'completeness': 'required', 'page': {'size': 10},
           'params': {'relation': 'references', 'minResolution': 'resolved-binding', 'direction': 'outgoing',
                      'endpoint': {'universe': sym['universe'], 'kind': 'symbol', 'nativeSubjectId': sym['row']['nativeSubjectId']}}}
    out['runProjectIdDiffers'] = run['projectId'] != req['projectId']
    out['queryProjectIdMismatch'] = attempt(lambda: Q.execute_graph_query(req, run, objects, blobs, host={'requestId': 'req1_' + '5' * 32}))
    qc = open(DC + '/workflows/query-projection-contract.v3.md').read()
    out['queryContractSection7MentionsProjectMismatch'] = any('projectId' in l and '|' in l and ('mismatch' in l or 'does not' in l) for l in qc.splitlines())
    out['detectorListingPresentMissing'] = attempt(lambda: P.parse_detector_manifest_body({}, 'e' * 64, present=True))
    wf = open(ROOT + '/docs/v2/contracts/product-v1/workflows-and-surfaces.md').read()
    out['workflowsNamesListingRefusalDetail'] = 'present invalid, non-file or unavailable listing refuses' in wf and 'EVALUATION.PROJECTION_INPUT_INCOMPLETE' in wf[wf.find('detector-compatibility.json'):wf.find('detector-compatibility.json') + 1500]
    return out


def s5():
    argv = ['node_modules/.bin/vitest', 'run', '--reporter=json']
    recipes = {'rawSha256OfCanonicalJsonArray': hashlib.sha256(canonical.canonical(argv)).hexdigest(),
               'rawSha256OfNulJoined': hashlib.sha256('\0'.join(argv).encode()).hexdigest(),
               'hDomainWorkflowArgv': canonical.identity('workflow.argv', argv)}
    sites = {}
    for rel in ('workflows/workflows_model.v1.py', 'native/native_evidence_model.v2.py', 'workflows/check-workflow-projection.v3.py', 'security/security_lifecycle_model_v1.py'):
        txt = open(track(DC + '/' + rel)).read()
        sites[rel] = [l.strip()[:160] for l in txt.splitlines() if 'argv' in l and ('sha' in l or 'Digest' in l) and ('canonical' in l or 'hashlib' in l or '!=' in l)][:4]
    normative = {}
    for rel in ('docs/v2/contracts/product-v1/security-and-lifecycle.md', 'docs/v2/contracts/product-v1/workflows-and-surfaces.md'):
        txt = open(track(ROOT + '/' + rel)).read()
        normative[rel] = [l.strip() for l in txt.splitlines() if re.search(r'argv.?digest', l, re.I)]
    te = docs['urn:opensip:product-v1:workflows:test-execution']['$defs']['TestPayloadV1']['properties']['argvDigest']
    return {'recipesDiffer': len(set(recipes.values())) == 3, 'recipes': recipes, 'referenceSites': sites,
            'normativeMentions': normative, 'testPayloadArgvDigestSchema': te}


def a14():
    wf = open(ROOT + '/docs/v2/contracts/product-v1/workflows-and-surfaces.md').read()
    return {'disclosedConservativeEvidencePivot': 'Evidence-change attribution is deliberately conservative in this product' in wf,
            'futureSuccessorNamed': 'A future evidence-pivot recipe requires its own reviewed successor.' in wf}


for name, fn in (('M4', m4), ('M5', m5), ('S5', s5), ('S6', s6), ('S7', s7), ('A6', a6), ('A8', a8), ('A9', a9), ('A11', a11), ('A12', a12), ('A13', a13), ('A14', a14)):
    section(name, fn)
res['loadedFileSha256'] = dict(sorted(loaded.items()))
os.makedirs(RT + '/receipts', exist_ok=True)
json.dump(res, open(RT + '/receipts/probe-owner-laws.' + TREE + '.json', 'w'), indent=1, default=str)
print(json.dumps(res['sections'], indent=1, default=str)[:60000])
