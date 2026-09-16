"""Focused discriminating probes of the root corrections overlay (verified overlay copy) against verified source37.

S3  S37-03 advisory law: full 20-operation x advisory matrix, base vs overlay schema; consumer scan of
    query-response-shaped JSON objects.
A5  A37-05 availability observation: vocabulary matrix; precedence; public host-invariant route representability.
A6  A37-06 semantic replay refusal: root mutant + independent false-result mutants + structural/missing/host-bug
    controls; owner-route comparison with the evaluator fault registry.
R12 R1/R2 StepTermination: definition equality, exhaustive class x faultCause x reasonCodes x errorCode admission
    difference, producer/fixture revalidation, D9 hostTerminationUnion field comparison.
ID  registered payload identity/closure consequence and Run identity stability against prior public receipts.
Reference evidence only; no suite, no pin regeneration.
"""
import copy, hashlib, importlib.util, itertools, json, os, re, sys, traceback

RT = '/private/tmp/opensip-design-corrections/claude-source37-root-corrections-review.v1'
OV = RT + '/work/source37-overlay'
BASE = '/tmp/opensip-design-corrections/candidate-subject.v37'
DC = OV + '/docs/coop/design-corrections'
OUT = RT + '/receipts/probe-overlay-semantics.json'
MAN37 = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v37.json'
res = {'standing': 'independent focused probe over verified overlay copy; reference evidence only'}


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def rows(o):
    if isinstance(o, list) and o and isinstance(o[0], dict) and 'path' in o[0] and 'sha256' in o[0]:
        return o
    if isinstance(o, dict):
        for v in o.values():
            x = rows(v)
            if x:
                return x


MAN = {r['path']: r['sha256'] for r in rows(json.load(open(MAN37)))}
OVM = {f['path']: f for f in json.load(open(RT + '/subject-manifest.json'))['files']}


def verified_base(rel):
    p = BASE + '/' + rel
    assert sha(p) == MAN[rel], 'base source bytes changed: ' + rel
    return p


def verified_overlay(rel):
    p = OV + '/' + rel
    want = OVM[rel]['sha256'] if rel in OVM else MAN[rel]
    assert sha(p) == want, 'overlay copy bytes changed: ' + rel
    return p


def load(name, path):
    s = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(s)
    sys.modules[name] = m
    s.loader.exec_module(m)
    return m


for rel in ('docs/coop/design-corrections/workflows/query_projection_model.v3.py',
            'docs/coop/design-corrections/workflows/schemas/common.schema.json',
            'docs/coop/design-corrections/workflows/schemas/evaluator3/common.schema.json',
            'docs/coop/design-corrections/workflows/schemas/evaluator3/graph-query.schema.json',
            'docs/coop/design-corrections/foundation/check-semantic-replay.v3.py',
            'docs/coop/design-corrections/foundation/check-replay.v3.py',
            'docs/coop/design-corrections/foundation/identity-model.v3.py',
            'docs/coop/design-corrections/foundation/evaluator-fault-observation.schema.v3.json',
            'docs/coop/design-corrections/native/native_evidence_model.v2.py',
            'docs/coop/design-corrections/workflows/workflows_model.v1.py',
            'docs/coop/artifacts/d9-exit-contract.v1.14.json'):
    verified_overlay(rel)

sys.path.insert(0, DC + '/foundation')
import canonical  # noqa: E402
from referencing import Registry, Resource  # noqa: E402
from referencing.jsonschema import DRAFT202012  # noqa: E402

Q = load('ov_query', DC + '/workflows/query_projection_model.v3.py')


def registry(root):
    docs = {}
    for d in (root + '/docs/coop/design-corrections/workflows/schemas', root + '/docs/coop/design-corrections/workflows/schemas/evaluator3'):
        for f in sorted(os.listdir(d)):
            if f.endswith('.json'):
                rel = os.path.relpath(os.path.join(d, f), root)
                if root == BASE:
                    verified_base(rel)
                doc = json.load(open(os.path.join(d, f)))
                if '$id' in doc:
                    docs[doc['$id']] = doc
    return Registry().with_resources([(k, Resource(contents=v, specification=DRAFT202012)) for k, v in docs.items()]), docs


REG_B, DOCS_B = registry(BASE)
REG_O, DOCS_O = registry(OV)
URN = 'urn:opensip:product-v1:workflows:'
IDS = {'wf': [k for k in DOCS_O if k.endswith(':common') or k.endswith('workflows:common:2') or k == URN + 'common'],
       'e3': URN + 'evaluator3:common:3', 'gq': URN + 'evaluator3:graph-query:3'}
res['schemaIds'] = sorted(DOCS_O)


def ok(reg, ref, value):
    try:
        canonical.ExactValidator({'$ref': ref}, registry=reg).validate(value)
        return True
    except Exception:
        return False


# ------------------------------------------------------------------------------------------ S3
try:
    ops = DOCS_O[IDS['gq']]['$defs']['Operation']['enum']
    adv = set(DOCS_O[IDS['gq']]['$defs']['AdvisoryOperation']['enum'])
    graph = set(DOCS_O[IDS['gq']]['$defs']['GraphOperation']['enum'])
    project = 'prj1-' + 'a' * 64
    run_id = 'run3:' + 'b' * 64
    ng = {'projectId': project, 'resolvedView': {'runId': run_id}, 'coverage': 'complete', 'availability': 'retained', 'truncated': False, 'totalItems': 0}
    gctx = {'advisory': False, 'availability': 'retained', 'countBasis': 'exact',
            'evidence': {'coverageIds': [], 'deficiencyCitations': [], 'resolutionLimitations': [], 'scopeIds': []},
            'factViewDigests': [], 'producedItems': 0, 'projectId': project, 'resolvedView': {'runId': run_id},
            'totalItems': 0, 'traversalCoverage': 'complete', 'truncated': False, 'visitedNodes': 0}
    matrix = []
    for op in ops:
        for a in (True, False):
            ctx = dict(gctx if op in graph else ng, advisory=a)
            rsp = {'schemaFamily': 'opensip.product.query', 'schemaMajor': 3, 'operation': op, 'context': ctx}
            if op in graph:
                rsp['items'] = []
            ref = IDS['gq'] + '#/$defs/GraphQueryResponseV1'
            matrix.append({'operation': op, 'advisory': a, 'base': ok(REG_B, ref, rsp), 'overlay': ok(REG_O, ref, rsp),
                           'law': a == (op in adv)})
    s3 = {'operations': len(ops), 'advisorySet': sorted(adv),
          'overlayEqualsLaw': all(r['overlay'] == r['law'] for r in matrix),
          'baseViolations': [(r['operation'], r['advisory']) for r in matrix if r['base'] != r['law']],
          'overlayViolations': [(r['operation'], r['advisory']) for r in matrix if r['overlay'] != r['law']]}
    # consumer scan: every query-response-shaped object in non-review JSON documents
    changed, scanned = [], 0
    for rel in sorted(MAN):
        if '/reviews/' in rel or not rel.endswith('.json') or not rel.startswith('docs/'):
            continue
        try:
            doc = json.load(open(verified_overlay(rel)))
        except (ValueError, UnicodeDecodeError, AssertionError):
            continue
        stack = [(doc, '')]
        while stack:
            o, ptr = stack.pop()
            if isinstance(o, dict):
                if o.get('schemaFamily') == 'opensip.product.query' and 'operation' in o and 'context' in o:
                    scanned += 1
                    ref = IDS['gq'] + '#/$defs/GraphQueryResponseV1'
                    b, v = ok(REG_B, ref, o), ok(REG_O, ref, o)
                    if b != v:
                        changed.append({'file': rel, 'pointer': ptr, 'base': b, 'overlay': v})
                for k, v in o.items():
                    stack.append((v, ptr + '/' + str(k)))
            elif isinstance(o, list):
                for i, v in enumerate(o):
                    stack.append((v, ptr + '/%d' % i))
    s3['consumerObjectsScanned'] = scanned
    s3['consumerAdmissionChanged'] = changed
    # producer: query_surface_projection advisory emissions
    src = open(verified_overlay('docs/coop/design-corrections/workflows/query_surface_projection.v3.py')).read()
    s3['surfaceProjectionAdvisoryLiterals'] = sorted(set(re.findall(r'"advisory":\s*(True|False|[a-z_]+)', src)))
    res['S3'] = s3
except Exception as e:
    res['S3'] = {'error': repr(e), 'tb': traceback.format_exc()[-2000:]}

# ------------------------------------------------------------------------------------------ fixtures
SR = load('ov_semrep', DC + '/foundation/check-semantic-replay.v3.py')
CR = load('ov_replaymut', DC + '/foundation/check-replay.v3.py')
M = SR.M
REQ = 'req1_' + '5' * 32


def host(**kw):
    h = {'requestId': REQ}
    h.update(kw)
    return h


def req(op, project, view, params, completeness='required', size=100):
    return {'schemaFamily': 'opensip.product.query', 'schemaMajor': 3, 'projectId': project, 'view': view,
            'operation': op, 'params': params, 'completeness': completeness, 'page': {'size': size}}


def outcome(fn):
    try:
        v = fn()
        return {'result': 'ADMIT', 'items': len(v['items']), 'termination': v['termination']}
    except Q.QueryRefusal as e:
        try:
            env = e.envelope()
            ex = env['exitCode']
        except Exception as ee:
            ex = 'envelope-error:' + type(ee).__name__
        return {'result': 'REFUSE', 'errorCode': e.error_code, 'detail': e.detail, 'class': e.klass,
                'faultCause': e.fault_cause, 'exitCode': ex, 'subject': (str(e.subject)[:240] if e.subject else None)}
    except Q.ReferenceCallPrecondition as e:
        return {'result': 'REFERENCE-CALL-PRECONDITION', 'missing': e.missing}
    except Exception as e:
        return {'result': 'UNCAUGHT', 'type': type(e).__name__, 'error': str(e)[:240]}


atom = {'op': 'none', 'relation': 'references', 'minResolution': 'resolved-binding', 'endpoint': 'target', 'filters': []}
g = SR.S.build_ts_semantic_graph(atom=atom, has_declares=False, has_references_fact=True, second_partition=True,
                                 references_resolved=False, incoming_search=True, incoming_complete=False,
                                 target_sidecar=True, second_universe=True)
run, objects, blobs, actual = SR.close_positive(g)
rid = actual['runId']
foo = {'universe': g['u1'], 'kind': 'symbol', 'nativeSubjectId': g['foo']}
PARAMS = {'relation': 'references', 'minResolution': 'resolved-binding', 'direction': 'outgoing', 'endpoint': foo}
okreq = req('graph.neighbors', run['projectId'], {'runId': rid}, PARAMS)

# ------------------------------------------------------------------------------------------ A5
try:
    a5 = {'matrix': {}}
    for label, val in (('omitted', None), ('retained', 'retained'), ('partial', 'partial'), ('purged', 'purged'), ('expired', 'expired'),
                       ('corrupt', 'corrupt'), ('unavailable', 'unavailable'), ('missing', 'missing'), ('unknown-token', 'not-a-state'),
                       ('case-variant', 'Purged'), ('trailing-space', 'purged '), ('null', 'NULL'), ('false', False), ('zero', 0),
                       ('list', []), ('dict', {}), ('bytes', b'purged')):
        h = host() if label == 'omitted' else host(availability=(None if val == 'NULL' else val))
        a5['matrix'][label] = outcome(lambda: Q.execute_graph_query(okreq, run, objects, blobs, host=h))
    bad = dict(okreq, schemaMajor=3, params={'relation': 'references'})
    a5['malformedRequest+invalidObservation'] = outcome(lambda: Q.execute_graph_query(bad, run, objects, blobs, host=host(availability='not-a-state')))
    a5['noRun+invalidObservation'] = outcome(lambda: Q.execute_graph_query(okreq, host=host(availability='not-a-state')))
    a5['missingRequestId+purged'] = outcome(lambda: Q.execute_graph_query(okreq, run, objects, blobs, host={'availability': 'purged'}))
    a5['invalidObservation+corruptBytes'] = None
    # representability of the existing public host-invariant route for a host-generated internal defect
    term = {'class': 'operational-failed', 'errorCode': 'SYSTEM.OUTCOME.ILLEGAL_STATE', 'faultCause': 'host-invariant',
            'domainDetail': {'code': 'HOST.INVARIANT_VIOLATED', 'remedy': 'host adapter supplied an out-of-vocabulary availability observation', 'subject': 'host.availability'}}
    env = {'schemaFamily': 'opensip.product.envelope', 'schemaMajor': 3, 'kind': 'failure', 'requestId': REQ, 'termination': term,
           'exitCode': 4, 'errors': [term['domainDetail']], 'projectId': run['projectId']}
    a5['hostInvariantRouteRepresentable'] = {'termination': ok(REG_O, IDS['e3'] + '#/$defs/StepTermination', term),
                                             'envelope': ok(REG_O, URN + 'evaluator3:command-envelope:3', env)}
    fault_doc = json.load(open(verified_overlay('docs/coop/design-corrections/foundation/evaluator-fault-observation.schema.v3.json')))
    routes = fault_doc.get('x-opensip-routes') or {}
    a5['ownerHostInternalRoutes'] = {k: v for k, v in routes.items() if k.endswith(':host-internal')}
    res['A5'] = a5
except Exception as e:
    res['A5'] = {'error': repr(e), 'tb': traceback.format_exc()[-2000:]}

# ------------------------------------------------------------------------------------------ A6
try:
    a6 = {'ownerRoutes': {k: v for k, v in routes.items() if k.startswith('complete-replay-mismatch') or k.startswith('promised-bytes-lost')}}

    def remint_false(run_, objects_, blobs_, flip):
        run_, objects_, blobs_ = copy.deepcopy(run_), copy.deepcopy(objects_), copy.deepcopy(blobs_)
        seal = copy.deepcopy(objects_[run_['evaluationSealId']][1])
        proof = copy.deepcopy(objects_[seal['proofBundleId']][1])
        evidence = copy.deepcopy(objects_[run_['evidenceId']][1])
        for p in proof['predicateProofs']:
            new = flip(p)
            if new is None or new == p['value']:
                continue
            w = canonical.parse(blobs_[p['witnessDigest']])
            w['matchingFactIds'] = []
            w['uncertainFactIds'] = []
            w['deficiencies'] = []
            raw = canonical.canonical(w)
            d = hashlib.sha256(raw).hexdigest()
            blobs_[d] = raw
            p['witnessDigest'] = d
            p['value'] = new
        proof['findingIds'] = []
        proof['waivedFindingIds'] = []
        for rr in proof['ruleResults']:
            rr['findingIds'] = []
            rr['deficiencies'] = []
            if rr['outcome'] in ('fail', 'indeterminate'):
                rr['outcome'] = 'pass'
        proof['executionDeficiencies'] = []
        proof['verdict'] = 'pass'
        pid = M.identifier('proof-bundle', proof)
        objects_[pid] = ('proof-bundle', proof)
        evidence['findingIds'] = []
        evidence['proofBundleId'] = pid
        eid = M.identifier('semantic-evidence', evidence)
        objects_[eid] = ('semantic-evidence', evidence)
        seal['proofBundleId'] = pid
        seal['evidenceId'] = eid
        seal['verdict'] = 'pass'
        sid = M.identifier('evaluation-seal', seal)
        objects_[sid] = ('evaluation-seal', seal)
        run_['evidenceId'] = eid
        run_['evaluationSealId'] = sid
        return run_, objects_, blobs_

    def query_mutant(label, gr, mrun, mobj, mblob):
        try:
            rk, _ = Q.identity3().open_run_closure(mrun, mobj, mblob)
            structural = 'ADMIT'
        except Exception as e:
            rk, structural = 'run3:' + '0' * 64, 'REFUSE:' + str(e)[:120]
        sym = next(r for r in gr['inputs']['population'].values() if r['kind'] == 'symbol')
        rq = req('graph.neighbors', mrun['projectId'], {'runId': rk}, {'relation': 'references', 'minResolution': 'resolved-binding',
                                                                         'direction': 'outgoing', 'endpoint': {'universe': sym['universe'], 'kind': 'symbol', 'nativeSubjectId': sym['row']['nativeSubjectId']}})
        o = outcome(lambda: Q.execute_graph_query(rq, mrun, mobj, mblob, host=host()))
        o['structuralOwnerClosure'] = structural
        return label, o

    cases = {}
    gd, posd, actd = SR.case_declares_exists()
    cases.update([query_mutant('root-severity-mutant', gd, *CR.remint_finding(*posd, lambda f, _b: f.update(severity='warning')))])
    cases.update([query_mutant('fail-to-pass', gd, *remint_false(*posd, lambda p: 'false' if p['value'] == 'true' else None))])
    gi, posi, acti = SR.case_incoming_incomplete_unknown()
    cases.update([query_mutant('indeterminate-laundered', gi, *remint_false(*posi, lambda p: 'false' if p['value'] == 'indeterminate' else None))])
    gm, posm, actm = SR.case_missing_inventory_execution()
    cases.update([query_mutant('execution-deficiency-erased', gm, *remint_false(*posm, lambda p: None))])
    # structural corruption: an object whose key no longer matches its identity
    r2, o2, b2 = copy.deepcopy(posd)
    ek = r2['evidenceId']
    dom, val = o2[ek]
    val = dict(val, planId=val['planId'])
    val['findingIds'] = list(val['findingIds'])[:-1]
    o2[ek] = (dom, val)
    cases.update([query_mutant('structural-reference-identity', gd, r2, o2, b2)])
    # promised object missing
    r3, o3, b3 = copy.deepcopy(posd)
    del o3[o3[r3['evaluationSealId']][1]['proofBundleId']]
    cases.update([query_mutant('missing-proof-object', gd, r3, o3, b3)])
    # host defect inside the replay owner (not retained data): monkeypatched close_run raises
    orig = Q.identity3().close_run
    try:
        Q.identity3().close_run = lambda *a, **k: (_ for _ in ()).throw(TypeError('simulated host evaluator defect'))
        cases['host-defect-in-close_run'] = outcome(lambda: Q.execute_graph_query(okreq, run, objects, blobs, host=host()))
    finally:
        Q.identity3().close_run = orig
    cases['positive-control-after-restore'] = outcome(lambda: Q.execute_graph_query(okreq, run, objects, blobs, host=host()))
    a6['cases'] = cases
    res['A6'] = a6
except Exception as e:
    res['A6'] = {'error': repr(e), 'tb': traceback.format_exc()[-2500:]}

# ------------------------------------------------------------------------------------------ R1/R2
try:
    r12 = {}
    wf_id = next(k for k in DOCS_O if DOCS_O[k].get('$defs', {}).get('StepTermination') and 'evaluator3' not in k)
    r12['workflowsCommonId'] = wf_id
    st_b_wf, st_b_e3 = DOCS_B[wf_id]['$defs']['StepTermination'], DOCS_B[IDS['e3']]['$defs']['StepTermination']
    st_o_wf, st_o_e3 = DOCS_O[wf_id]['$defs']['StepTermination'], DOCS_O[IDS['e3']]['$defs']['StepTermination']
    r12['defsEqual'] = {'base': st_b_wf == st_b_e3, 'overlay': st_o_wf == st_o_e3}
    e3 = DOCS_O[IDS['e3']]['$defs']
    fault_enum = e3.get('D9FaultCause', {}).get('enum') or st_o_e3['properties']['faultCause'].get('enum')
    if fault_enum is None:
        fref = st_o_e3['properties']['faultCause'].get('$ref', '').split('/')[-1]
        fault_enum = e3[fref]['enum']
    eref = st_o_e3['properties']['errorCode'].get('$ref', '').split('/')[-1]
    err_enum = e3[eref]['enum'] if eref else st_o_e3['properties']['errorCode']['enum']
    rref = st_o_e3['properties']['reasonCodes']['items']['$ref'].split('/')[-1]
    reason_enum = e3[rref]['enum']
    r12['enumSizes'] = {'faultCause': len(fault_enum), 'errorCode': len(err_enum), 'reasonCode': len(reason_enum)}
    W = load('ov_workflows_model', DC + '/workflows/workflows_model.v1.py')
    r12['hostFaultMap'] = W.FAULT_TO_ERROR
    CLASSES = ['success', 'policy-failed', 'request-rejected', 'indeterminate', 'operational-failed', 'interrupted']
    admitted = {'base': set(), 'overlay': set()}
    for cls in CLASSES:
        for fc in [None] + list(fault_enum):
            for rc in (False, True):
                for ec in [None] + list(err_enum):
                    t = {'class': cls}
                    if cls == 'policy-failed':
                        t['runId'] = 'run3:' + 'c' * 64
                    if cls == 'interrupted':
                        t['signal'] = 'SIGINT'
                    if fc is not None:
                        t['faultCause'] = fc
                    if rc:
                        t['reasonCodes'] = [reason_enum[0]]
                    if ec is not None:
                        t['errorCode'] = ec
                    key = (cls, fc, rc, ec)
                    for side, reg in (('base', REG_B), ('overlay', REG_O)):
                        if ok(reg, IDS['e3'] + '#/$defs/StepTermination', t):
                            admitted[side].add(key)
    removed = sorted(admitted['base'] - admitted['overlay'], key=str)
    added = sorted(admitted['overlay'] - admitted['base'], key=str)
    r12['exhaustive'] = {'combinations': len(CLASSES) * (len(fault_enum) + 1) * 2 * (len(err_enum) + 1),
                         'admittedBase': len(admitted['base']), 'admittedOverlay': len(admitted['overlay']),
                         'newlyAdmitted': [list(map(str, k)) for k in added][:20], 'newlyAdmittedCount': len(added),
                         'removedCount': len(removed)}

    def legal(k):
        cls, fc, rc, ec = k
        if fc is not None and cls != 'operational-failed':
            return False
        if rc and cls != 'indeterminate':
            return False
        if cls == 'operational-failed' and fc is not None and ec is not None and W.FAULT_TO_ERROR.get(fc) != ec:
            return False
        return True
    r12['removedButLegalUnderPredicate'] = [list(map(str, k)) for k in removed if legal(k)][:40]
    r12['overlayAdmittedButIllegal'] = [list(map(str, k)) for k in admitted['overlay'] if not legal(k)][:40]
    rr_b = sorted({k[3] for k in admitted['base'] if k[0] == 'request-rejected' and k[1] is None and not k[2]}, key=str)
    rr_o = sorted({k[3] for k in admitted['overlay'] if k[0] == 'request-rejected' and k[1] is None and not k[2]}, key=str)
    r12['requestRejectedErrorCodes'] = {'base': len(rr_b), 'overlay': len(rr_o), 'equal': rr_b == rr_o,
                                        'faultFamilyStillAdmitted': sorted(set(rr_o) & set(W.FAULT_TO_ERROR.values()))}
    op_pairs = sorted({(k[1], k[3]) for k in admitted['overlay'] if k[0] == 'operational-failed' and not k[2]}, key=str)
    r12['operationalPairsOverlay'] = op_pairs
    r12['operationalPairsEqualHostMap'] = dict(op_pairs) == W.FAULT_TO_ERROR and len(op_pairs) == len(W.FAULT_TO_ERROR)
    # producers: native public_termination_for over every registered key/origin; evaluator fault routes
    N = load('ov_native_model', DC + '/native/native_evidence_model.v2.py')
    nat = json.load(open(verified_overlay('docs/coop/design-corrections/native/native-evidence.schemas.v2.json')))
    reg_keys = nat['x-opensip-public-route-registry']['keys']
    prod = {'native': [], 'fault': []}
    for key, body in reg_keys.items():
        origins = body.get('possibleOrigins') or body.get('origins') or [None]
        for origin in origins:
            try:
                t = N.public_termination_for(key, origin)
            except Exception as e:
                prod['native'].append({'key': key, 'origin': origin, 'error': type(e).__name__ + ':' + str(e)[:100]})
                continue
            term = t.get('termination', t) if isinstance(t, dict) else t
            prod['native'].append({'key': key, 'origin': origin, 'base': ok(REG_B, IDS['e3'] + '#/$defs/StepTermination', term),
                                   'overlay': ok(REG_O, IDS['e3'] + '#/$defs/StepTermination', term)})
    for key, body in routes.items():
        term = dict(body['termination'])
        if body.get('detail'):
            term['domainDetail'] = {'code': body['detail'], 'remedy': body.get('remedy', 'x')[:1024]}
        if term.get('class') in ('indeterminate', 'policy-failed'):
            term.setdefault('runId', 'run3:' + 'd' * 64)
        prod['fault'].append({'key': key, 'base': ok(REG_B, IDS['e3'] + '#/$defs/StepTermination', term),
                              'overlay': ok(REG_O, IDS['e3'] + '#/$defs/StepTermination', term)})
    r12['producers'] = {k: {'count': len(v), 'errors': [x for x in v if 'error' in x][:10],
                            'changed': [x for x in v if 'error' not in x and x['base'] != x['overlay']],
                            'overlayRefused': [x for x in v if 'error' not in x and not x['overlay']]} for k, v in prod.items()}
    # fixture scan: termination-shaped objects in non-review JSON
    props = set(st_o_e3['properties'])
    changed_fix, n = [], 0
    for rel in sorted(MAN):
        if '/reviews/' in rel or not rel.endswith('.json') or not rel.startswith('docs/'):
            continue
        try:
            doc = json.load(open(verified_overlay(rel)))
        except (ValueError, UnicodeDecodeError, AssertionError):
            continue
        stack = [(doc, '')]
        while stack:
            o, ptr = stack.pop()
            if isinstance(o, dict):
                if o.get('class') in CLASSES and set(o) <= props and not any(isinstance(v, str) and v.startswith('$') for v in o.values()):
                    n += 1
                    b, v = ok(REG_B, IDS['e3'] + '#/$defs/StepTermination', o), ok(REG_O, IDS['e3'] + '#/$defs/StepTermination', o)
                    if b != v:
                        changed_fix.append({'file': rel, 'pointer': ptr, 'value': o, 'base': b, 'overlay': v})
                for k, v in o.items():
                    stack.append((v, ptr + '/' + str(k)))
            elif isinstance(o, list):
                for i, v in enumerate(o):
                    stack.append((v, ptr + '/%d' % i))
    r12['fixtureScan'] = {'terminationShapedObjects': n, 'admissionChanged': changed_fix}
    # D9 v1.14 hostTerminationUnion comparison (superseded union vs successor)
    d9 = json.load(open(verified_overlay('docs/coop/artifacts/d9-exit-contract.v1.14.json')))
    found = []

    def find(o, path=''):
        if isinstance(o, dict):
            for k, v in o.items():
                if k == 'hostTerminationUnion':
                    found.append((path + '/' + k, v))
                find(v, path + '/' + k)
        elif isinstance(o, list):
            for i, v in enumerate(o):
                find(v, path + '/%d' % i)
    find(d9)
    union_summary = []
    for path, u in found:
        txt = json.dumps(u)
        union_summary.append({'path': path, 'bytes': len(txt), 'mentionsFaultCause': 'faultCause' in txt,
                              'unknownFieldPolicy': u.get('unknownFieldPolicy') if isinstance(u, dict) else None,
                              'variantKeys': list(u.keys())[:20] if isinstance(u, dict) else None})
    r12['d9Union'] = union_summary
    r12['d9ScenarioAxesFaultCauseNoneAreAxesNotCarriers'] = sum(1 for _ in re.finditer(r'"faultCause": "none"', json.dumps(d9, indent=1)))
    res['R12'] = r12
except Exception as e:
    res['R12'] = {'error': repr(e), 'tb': traceback.format_exc()[-2500:]}

# ------------------------------------------------------------------------------------------ ID
try:
    ids = json.load(open(verified_overlay('docs/coop/design-corrections/foundation/identity-schemas.v3.json')))
    reg = ids['x-opensip-payload-registry']['classes']
    docs = set()
    for c in reg.values():
        if 'document' in c:
            docs.add(c['document'])
        for r in (c.get('rows') or {}).values():
            docs.add(r['document'])
    txt = json.dumps(ids['x-opensip-digest-domains'])
    docs |= set(re.findall(r'"document": "([^"]+)"', txt))
    changed_rel = {p.replace('docs/coop/design-corrections/', '') for p in OVM}
    refs = {}
    for d in sorted(docs):
        rel = 'docs/coop/design-corrections/' + d
        if rel not in MAN:
            refs[d] = 'NOT-IN-MANIFEST'
            continue
        body = open(verified_overlay(rel)).read()
        hits = sorted(set(re.findall(r'"\$ref":\s*"([^"]*(?:common|graph-query|StepTermination|GraphQuery)[^"]*)"', body)))
        refs[d] = {'inOverlay': d in changed_rel, 'refsToChangedSchemas': hits}
    M3 = Q.identity3()
    reg_docs = M3.registered_schema_documents()
    ov_hits = {f['path']: {'before': f['beforeSha256'] in reg_docs, 'after': f['sha256'] in reg_docs} for f in OVM.values()}
    idr = {'registeredAndDigestDomainDocuments': refs, 'overlayFilesInRegisteredSchemaDocumentSet': ov_hits}
    # Run identity stability: same fixtures as the retained source37 review receipts
    prior = {'declares-exists': 'run3:0cd01b29330dd5812b083946ea7a1684a91a602f0c6905c76bc4d81c417bd744',
             'incoming-incomplete': 'run3:f9b48563b2a7a96f9ee8637eb2db5c277ac2b466c424d2f9010825dad94d801b',
             'missing-inventory': 'run3:a3185cc797b2a01511a5c42573e795bb426b47e10a298504325440a52f791064',
             'owner-graph': 'run3:5f0c94d9673a053bd223654e63f18e7b6ab5369264f4eff323ac1494a8acaa45'}
    now = {'declares-exists': actd['runId'], 'incoming-incomplete': acti['runId'], 'missing-inventory': actm['runId'], 'owner-graph': rid}
    idr['runIdentityStability'] = {k: {'prior': prior[k], 'overlay': now[k], 'equal': prior[k] == now[k]} for k in prior}
    idr['closeRunOnOverlay'] = {k: 'ADMIT' for k in now}
    res['ID'] = idr
except Exception as e:
    res['ID'] = {'error': repr(e), 'tb': traceback.format_exc()[-2500:]}

json.dump(res, open(OUT, 'w'), indent=1, default=str)
summary = {
    'S3': {k: res['S3'].get(k) for k in ('overlayEqualsLaw', 'baseViolations', 'overlayViolations', 'consumerObjectsScanned', 'consumerAdmissionChanged', 'error')},
    'A5': {k: (v if not isinstance(v, dict) or 'result' not in v else (v['result'], v.get('detail'), v.get('missing'))) for k, v in (res['A5'].get('matrix') or {}).items()},
    'A5-extra': {k: res['A5'].get(k) for k in ('malformedRequest+invalidObservation', 'noRun+invalidObservation', 'missingRequestId+purged', 'hostInvariantRouteRepresentable', 'error')},
    'A6': {k: (v.get('result'), v.get('detail'), v.get('errorCode'), (v.get('subject') or '')[:60], v.get('structuralOwnerClosure')) for k, v in (res['A6'].get('cases') or {}).items()},
    'A6-ownerRoutes': res['A6'].get('ownerRoutes'),
    'R12': {k: res['R12'].get(k) for k in ('defsEqual', 'enumSizes', 'exhaustive', 'removedButLegalUnderPredicate', 'overlayAdmittedButIllegal', 'requestRejectedErrorCodes', 'operationalPairsEqualHostMap', 'error')},
    'R12-producers': {k: {kk: (vv if kk != 'changed' else len(vv)) for kk, vv in v.items()} for k, v in (res['R12'].get('producers') or {}).items()},
    'R12-fixtures': {'n': (res['R12'].get('fixtureScan') or {}).get('terminationShapedObjects'), 'changed': len((res['R12'].get('fixtureScan') or {}).get('admissionChanged') or [])},
    'R12-d9Union': res['R12'].get('d9Union'),
    'ID': {'refs': res['ID'].get('registeredAndDigestDomainDocuments'), 'regDocs': res['ID'].get('overlayFilesInRegisteredSchemaDocumentSet'), 'runs': res['ID'].get('runIdentityStability'), 'error': res['ID'].get('error')},
}
print(json.dumps(summary, indent=1, default=str))
