"""Independent SEAL adapter, query typed replay boundary, fault-pair and schema probes over frozen source38 bytes.

SEAL   lawful full Run admitted; independently reminted false results (predicate flip, evidence-level) refused with the
       exact identity CompleteReplayMismatch cause and its chained origin-free replay-stack condition; REAL owner classes
       from another loaded identity copy and real replay-stack defects propagate (not Reject).
COVER  every Exception subclass defined by modules the replay stack loads is classified against UNAVAILABLE/MISMATCHES/REFUSALS.
QUERY  missing blob vs missing object, corrupt bytes, evidence-level remint (non-proof comparison key), declared jsonschema
       error inside the stack, undeclared host defect, outer-copy class raised inside the stack (bypass observation),
       retained availability record variants (valid, extra member, wrong schemaVersion, str input).
FAULT  all 24 evaluator fault routes: illegal errorCode/faultCause pair refuses at schema; every lawful-but-different pair
       refuses at owner parity.
SCHEMA R1/R2 exhaustive admission on both frozen common schemas, advisory exact-four law on graph-query, and query-operation
       terminations (finding.show purged exit 2, completeness indeterminate) stay admissible.
Reference evidence only.
"""
import copy, hashlib, importlib.util, inspect, json, sys, traceback

RT = '/private/tmp/opensip-design-corrections/claude-independent-design.v38'
SRC = RT + '/work/source38-pkg'
DC = SRC + '/docs/coop/design-corrections'
OUT = RT + '/receipts/probe-seal-query-fault.json'
res = {'standing': 'independent reviewer probe; reference evidence only',
       'attempt1': 'receipts/runs/probe_seal_query_fault.attempt1-probe-bug.* (unguarded structural call and NameError; preserved)'}


def load(name, path):
    s = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(s)
    sys.modules[name] = m
    s.loader.exec_module(m)
    return m


def raise_(e):
    raise e


def flip_remint(M, C, run, objects, blobs, mode):
    run, objects, blobs = copy.deepcopy(run), copy.deepcopy(objects), copy.deepcopy(blobs)
    seal = copy.deepcopy(objects[run['evaluationSealId']][1])
    proof = copy.deepcopy(objects[seal['proofBundleId']][1])
    ev = copy.deepcopy(objects[run['evidenceId']][1])
    if mode == 'predicate-flip':
        for p in proof['predicateProofs']:
            if p['value'] == 'true':
                w = C.parse(blobs[p['witnessDigest']])
                w.update(matchingFactIds=[], uncertainFactIds=[], deficiencies=[])
                raw = C.canonical(w)
                d = hashlib.sha256(raw).hexdigest()
                blobs[d] = raw
                p.update(witnessDigest=d, value='false')
        proof.update(findingIds=[], waivedFindingIds=[], verdict='pass')
        for rr in proof['ruleResults']:
            rr.update(findingIds=[], outcome='pass' if rr['outcome'] == 'fail' else rr['outcome'])
        pid = M.identifier('proof-bundle', proof)
        objects[pid] = ('proof-bundle', proof)
        ev.update(findingIds=[], proofBundleId=pid)
        seal.update(proofBundleId=pid, verdict='pass')
    elif mode == 'evidence-coverage-dropped':
        if not ev['coverageIds']:
            return None
        ev['coverageIds'] = ev['coverageIds'][1:]
    eid = M.identifier('semantic-evidence', ev)
    objects[eid] = ('semantic-evidence', ev)
    seal['evidenceId'] = eid
    sid = M.identifier('evaluation-seal', seal)
    objects[sid] = ('evaluation-seal', seal)
    run.update(evidenceId=eid, evaluationSealId=sid)
    return run, objects, blobs


# ------------------------------------------------------------------------------------------- SEAL
Q = load('sq38_query', DC + '/workflows/query_projection_model.v3.py')
try:
    AD = load('sq38_seal_adapter_check', DC + '/security/check-analysis-seal-adapter.v1.py')
    S = AD.S
    IM = S._identity_model_v3()
    run, objects, blobs, run_id, _ = AD.full_admitted_graph()
    rec = AD.journal_seal(run_id)
    seal = {'lawful': S.admit_analysis_seal(rec, run, objects, blobs)['result']}
    for mode in ('predicate-flip', 'evidence-coverage-dropped'):
        m = flip_remint(AD.M, AD.C, run, objects, blobs, mode)
        if m is None:
            seal[mode] = 'NOT-APPLICABLE'
            continue
        try:
            mid = IM.open_run_closure(*m)[0]
            structural = 'ADMIT'
        except IM.C.AdmissionError as e:
            mid, structural = IM.identifier('run', m[0]), 'STRUCTURAL-REFUSE:' + str(e)[:60]
        try:
            S.admit_analysis_seal(AD.journal_seal(mid), *m)
            seal[mode] = {'structural': structural, 'seal': 'ADMITTED-FALSE'}
        except S.Reject as e:
            cause = e.__cause__
            seal[mode] = {'structural': structural, 'seal': str(e)[:90], 'causeIsIM.CompleteReplayMismatch': type(cause) is IM.CompleteReplayMismatch,
                          'causeIsIM.AdmissionErrorSubclass': isinstance(cause, IM.C.AdmissionError), 'causeType': type(cause).__name__,
                          'chainedOriginalType': type(cause.__cause__).__name__ if cause is not None and cause.__cause__ is not None else None,
                          'chainedOriginalIsReplayStackClass': cause is not None and cause.__cause__ is not None and type(cause.__cause__) is IM.complete_replay().M.CompleteReplayMismatch}
        except Exception as e:
            seal[mode] = {'structural': 'ADMIT', 'seal': 'PROPAGATED ' + type(e).__name__}
    foreign = {
        'query-identity-copy AdmissionError': Q.identity3().C.AdmissionError('REFERENCE_IDENTITY'),
        'query-identity-copy CompleteReplayMismatch': Q.identity3().CompleteReplayMismatch('EVALUATOR_COMPLETE_PROOF_REPLAY'),
        'replay-stack identity copy CompleteReplayMismatch': IM.complete_replay().M.CompleteReplayMismatch('EVALUATOR_COMPLETE_PROOF_REPLAY'),
        'replay-stack canonical AdmissionError': IM.complete_replay().C.AdmissionError('X'),
    }
    orig = IM.close_run
    for label, exc in foreign.items():
        IM.close_run = lambda *a, _e=exc, **k: raise_(_e)
        try:
            S.admit_analysis_seal(rec, run, objects, blobs)
            seal['foreign:' + label] = 'ADMITTED'
        except S.Reject as e:
            seal['foreign:' + label] = 'REJECT(misrouted as owner refusal)'
        except Exception as e:
            seal['foreign:' + label] = 'PROPAGATED' if e is exc else 'OTHER ' + type(e).__name__
        finally:
            IM.close_run = orig
    stack = IM.complete_replay()
    oc = stack.E.compare_complete_replay
    stack.E.compare_complete_replay = lambda *a, **k: raise_(KeyError('simulated comparison defect'))
    try:
        S.admit_analysis_seal(rec, run, objects, blobs)
        seal['replay-stack KeyError'] = 'ADMITTED'
    except S.Reject:
        seal['replay-stack KeyError'] = 'REJECT(misrouted)'
    except KeyError:
        seal['replay-stack KeyError'] = 'PROPAGATED KeyError'
    finally:
        stack.E.compare_complete_replay = oc
    seal['lawful-after-restore'] = S.admit_analysis_seal(rec, run, objects, blobs)['result']
    res['SEAL'] = seal
except Exception as exc:
    res['SEAL'] = {'error': repr(exc), 'tb': traceback.format_exc()[-2000:]}

# ------------------------------------------------------------------------------------------- COVER
try:
    import types
    stack = IM.complete_replay()
    declared = stack.UNAVAILABLE + stack.MISMATCHES + stack.REFUSALS
    todo, visited, classes = [stack], set(), {}
    while todo:
        mod = todo.pop()
        if id(mod) in visited:
            continue
        visited.add(id(mod))
        for attr, obj in vars(mod).items():
            if isinstance(obj, types.ModuleType) and SRC in (getattr(obj, '__file__', '') or ''):
                todo.append(obj)
            elif inspect.isclass(obj) and issubclass(obj, BaseException) and getattr(obj, '__module__', None) == mod.__name__:
                classes[id(obj)] = {'file': mod.__file__.replace(SRC + '/', ''), 'loadName': mod.__name__, 'class': obj.__name__,
                                    'covered': issubclass(obj, declared),
                                    'coveredBy': 'UNAVAILABLE' if issubclass(obj, stack.UNAVAILABLE) else 'MISMATCHES' if issubclass(obj, stack.MISMATCHES) else 'REFUSALS' if issubclass(obj, stack.REFUSALS) else None}
    rows = sorted(classes.values(), key=lambda r: (r['file'], r['class'], r['loadName']))
    res['COVER'] = {'modulesInReplayStackGraph': len(visited), 'exceptionClassObjects': len(rows),
                    'uncovered': [r for r in rows if not r['covered']], 'covered': [r for r in rows if r['covered']]}
except Exception as exc:
    res['COVER'] = {'error': repr(exc), 'tb': traceback.format_exc()[-1500:]}

# ------------------------------------------------------------------------------------------- QUERY
try:
    SR = load('sq38_semrep', DC + '/foundation/check-semantic-replay.v3.py')
    M3 = Q.identity3()
    host = {'requestId': 'req1_' + '6' * 32}
    gd, (run, objects, blobs), act = SR.case_declares_exists()
    sym = next(r for r in gd['inputs']['population'].values() if r['kind'] == 'symbol')

    def q(r, o, b, rid=None):
        req = {'schemaFamily': 'opensip.product.query', 'schemaMajor': 3, 'projectId': r['projectId'], 'view': {'runId': rid or M3.identifier('run', r)},
               'operation': 'graph.neighbors', 'params': {'relation': 'references', 'minResolution': 'resolved-binding', 'direction': 'outgoing',
                                                          'endpoint': {'universe': sym['universe'], 'kind': 'symbol', 'nativeSubjectId': sym['row']['nativeSubjectId']}},
               'completeness': 'required', 'page': {'size': 100}}
        try:
            v = Q.execute_graph_query(req, r, o, b, host=host)
            return {'result': 'ADMIT', 'class': v['termination']['class']}
        except Q.QueryRefusal as e:
            return {'result': 'REFUSE', 'errorCode': e.error_code, 'faultCause': e.fault_cause, 'detail': e.detail, 'subject': str(e.subject)[:80],
                    'causeType': type(e.__cause__).__name__, 'exit': e.envelope()['exitCode']}
        except Exception as e:
            return {'result': 'UNCAUGHT', 'type': type(e).__name__, 'msg': str(e)[:120]}

    qr = {'lawful': q(run, objects, blobs, act['runId'])}
    o2, b2 = copy.deepcopy(objects), copy.deepcopy(blobs)
    wit = objects[objects[run['evaluationSealId']][1]['proofBundleId']][1]['predicateProofs'][0]['witnessDigest']
    del b2[wit]
    qr['missing witness blob'] = q(run, o2, b2, act['runId'])
    o2, b2 = copy.deepcopy(objects), copy.deepcopy(blobs)
    b2[wit] = b'{"tampered":true}'
    qr['corrupt witness blob bytes'] = q(run, o2, b2, act['runId'])
    m = flip_remint(M3, M3.C, run, objects, blobs, 'evidence-coverage-dropped')
    if m:
        try:
            structural = 'ADMIT ' + M3.open_run_closure(*m)[0][:20]
        except M3.C.AdmissionError as e:
            structural = 'STRUCTURAL-REFUSE:' + str(e)[:60]
        qr['evidence-level remint'] = dict(q(*m), structural=structural)
    m = flip_remint(M3, M3.C, run, objects, blobs, 'predicate-flip')
    qr['predicate-flip remint'] = q(*m)
    stack = M3.complete_replay()
    od = stack.derive
    for label, exc in (('declared jsonschema ValidationError', stack.C.ValidationError('probe')),
                       ('undeclared KeyError', KeyError('probe')),
                       ('outer query identity copy CompleteReplayMismatch raised inside stack', M3.CompleteReplayMismatch('EVALUATOR_COMPLETE_PROOF_REPLAY')),
                       ('outer query identity copy EvidenceUnavailable raised inside stack', M3.EvidenceUnavailable('retained:probe'))):
        stack.derive = lambda *a, _e=exc, **k: raise_(_e)
        try:
            qr['stack raises: ' + label] = q(run, objects, blobs, act['runId'])
        finally:
            stack.derive = od
    qr['lawful after restore'] = q(run, objects, blobs, act['runId'])
    rec_ok = {'schemaVersion': 2, 'runId': act['runId'], 'generation': 0, 'state': 'retained', 'missingRefs': [], 'reason': 'ok'}
    avail = {}
    for label, raw in (('valid retained', M3.C.canonical(rec_ok)), ('extra member', M3.C.canonical(dict(rec_ok, extra=1))),
                       ('schemaVersion 1', M3.C.canonical(dict(rec_ok, schemaVersion=1))), ('str input', M3.C.canonical(rec_ok).decode()),
                       ('non-canonical key order bytes', json.dumps(dict(reversed(list(rec_ok.items())))).encode())):
        try:
            avail[label] = Q.observe_retained_availability(raw, act['runId'])
        except Q.QueryRefusal as e:
            avail[label] = 'REFUSE ' + e.detail
        except Exception as e:
            avail[label] = 'UNCAUGHT ' + type(e).__name__ + ': ' + str(e)[:80]
    qr['retained availability'] = avail
    res['QUERY'] = qr
except Exception as exc:
    res['QUERY'] = {'error': repr(exc), 'tb': traceback.format_exc()[-2000:]}

# ------------------------------------------------------------------------------------------- FAULT
try:
    F = load('sq38_fault', DC + '/foundation/evaluator_fault_model.v3.py')
    W = load('sq38_wf', DC + '/workflows/workflows_model.v1.py')
    raw = b'{"owner":"probe"}'
    pairs = list(W.FAULT_TO_ERROR.items())
    rows = {'schemaRefusals': 0, 'parityRefusals': 0, 'unexpected': []}
    for key, route in F.ROUTES.items():
        condition, origin = key.split(':')
        o = {'schemaVersion': 3, 'condition': condition, 'origin': origin, 'diagnosticDigest': hashlib.sha256(raw).hexdigest(), 'reference': 'retained:probe',
             'limit': ({'field': 'selectedPrograms', 'observed': 65, 'maximum': 64} if condition == 'selection-limit-exceeded' else
                       {'field': 'proof.predicates', 'observed': 100001, 'maximum': 100000} if condition == 'output-bound-exceeded' else None)}
        r = F.route(o, raw)
        e = F.failure_envelope(o, raw, 'req1_' + '3' * 32)
        term = e['termination']
        if term['class'] == 'operational-failed':
            for fc, ec in pairs:
                if (fc, ec) == (term['faultCause'], term['errorCode']):
                    continue
                for label, mut in (('illegal', {'errorCode': ec}), ('lawful-other', {'errorCode': ec, 'faultCause': fc})):
                    bad = copy.deepcopy(e)
                    bad['termination'].update(mut)
                    try:
                        F.validate_envelope(bad, r)
                        rows['unexpected'].append((key, label, fc, 'ADMIT'))
                    except F.C.ValidationError:
                        rows['schemaRefusals'] += 1
                        if label != 'illegal':
                            rows['unexpected'].append((key, label, fc, 'schema'))
                    except Exception as ex:
                        if 'EVALUATOR_FAULT_ENVELOPE_PARITY' in str(ex):
                            rows['parityRefusals'] += 1
                            if label != 'lawful-other':
                                rows['unexpected'].append((key, label, fc, 'parity'))
                        else:
                            rows['unexpected'].append((key, label, fc, type(ex).__name__))
        else:
            for label, mut in (('faultCause-on-' + term['class'], {'faultCause': 'host-io'}),):
                bad = copy.deepcopy(e)
                bad['termination'].update(mut)
                try:
                    F.validate_envelope(bad, r)
                    rows['unexpected'].append((key, label, 'ADMIT'))
                except F.C.ValidationError:
                    rows['schemaRefusals'] += 1
                except Exception as ex:
                    rows['unexpected'].append((key, label, type(ex).__name__))
    rows['routes'] = len(F.ROUTES)
    res['FAULT'] = rows
except Exception as exc:
    res['FAULT'] = {'error': repr(exc), 'tb': traceback.format_exc()[-2000:]}

# ------------------------------------------------------------------------------------------- SCHEMA
try:
    sys.path.insert(0, DC + '/foundation')
    import canonical
    from referencing import Registry, Resource
    from referencing.jsonschema import DRAFT202012
    docs = {}
    import os
    for d in (DC + '/workflows/schemas', DC + '/workflows/schemas/evaluator3'):
        for f in sorted(os.listdir(d)):
            if f.endswith('.json'):
                doc = json.load(open(os.path.join(d, f)))
                if '$id' in doc:
                    docs[doc['$id']] = doc
    reg = Registry().with_resources([(k, Resource(contents=v, specification=DRAFT202012)) for k, v in docs.items()])

    def ok(ref, v):
        try:
            canonical.ExactValidator({'$ref': ref}, registry=reg).validate(v)
            return True
        except Exception:
            return False
    e3 = 'urn:opensip:product-v1:workflows:evaluator3:common:3'
    wf = next(k for k in docs if 'evaluator3' not in k and docs[k].get('$defs', {}).get('StepTermination'))
    st = docs[e3]['$defs']['StepTermination']
    fenum = docs[e3]['$defs'][st['properties']['faultCause']['$ref'].split('/')[-1]]['enum']
    eenum = docs[e3]['$defs'][st['properties']['errorCode']['$ref'].split('/')[-1]]['enum']
    renum = docs[e3]['$defs'][st['properties']['reasonCodes']['items']['$ref'].split('/')[-1]]['enum']
    W = load('sq38_wf2', DC + '/workflows/workflows_model.v1.py')
    admitted = {e3: set(), wf: set()}
    for cls in ('success', 'policy-failed', 'request-rejected', 'indeterminate', 'operational-failed', 'interrupted'):
        for fc in [None] + fenum:
            for rc in (False, True):
                for ec in [None] + eenum:
                    t = {'class': cls}
                    if cls == 'policy-failed':
                        t['runId'] = 'run3:' + 'c' * 64
                    if cls == 'interrupted':
                        t['signal'] = 'SIGINT'
                    if fc:
                        t['faultCause'] = fc
                    if rc:
                        t['reasonCodes'] = [renum[0]]
                    if ec:
                        t['errorCode'] = ec
                    for sid in admitted:
                        if ok(sid + '#/$defs/StepTermination', t):
                            admitted[sid].add((cls, fc, rc, ec))

    def lawful(k):
        cls, fc, rc, ec = k
        if fc is not None and cls != 'operational-failed':
            return False
        if rc and cls != 'indeterminate':
            return False
        if cls == 'operational-failed' and W.FAULT_TO_ERROR.get(fc) != ec:
            return False
        return True
    sch = {'defsEqual': docs[e3]['$defs']['StepTermination'] == docs[wf]['$defs']['StepTermination'],
           'admitted': {k: len(v) for k, v in admitted.items()}, 'sameAdmission': admitted[e3] == admitted[wf],
           'unlawfulAdmitted': [list(map(str, k)) for k in admitted[e3] if not lawful(k)][:20],
           'requestRejectedCodes': sorted({k[3] for k in admitted[e3] if k[0] == 'request-rejected'})}
    gq = 'urn:opensip:product-v1:workflows:evaluator3:graph-query:3'
    ops = docs[gq]['$defs']['Operation']['enum']
    adv = set(docs[gq]['$defs']['AdvisoryOperation']['enum'])
    graph = set(docs[gq]['$defs']['GraphOperation']['enum'])
    viol = []
    ctx = {'projectId': 'prj1-' + 'a' * 64, 'resolvedView': {'runId': 'run3:' + 'b' * 64}, 'coverage': 'complete', 'availability': 'retained', 'truncated': False, 'totalItems': 0}
    gctx = {'availability': 'retained', 'countBasis': 'exact', 'evidence': {'coverageIds': [], 'deficiencyCitations': [], 'resolutionLimitations': [], 'scopeIds': []},
            'factViewDigests': [], 'producedItems': 0, 'projectId': 'prj1-' + 'a' * 64, 'resolvedView': {'runId': 'run3:' + 'b' * 64}, 'totalItems': 0,
            'traversalCoverage': 'complete', 'truncated': False, 'visitedNodes': 0}
    for op in ops:
        for a in (True, False):
            body = {'schemaFamily': 'opensip.product.query', 'schemaMajor': 3, 'operation': op, 'context': dict(gctx if op in graph else ctx, advisory=a)}
            if op in graph:
                body['items'] = []
            if ok(gq + '#/$defs/GraphQueryResponseV1', body) != (a == (op in adv)):
                viol.append((op, a))
    sch['advisoryViolations'] = viol
    sch['queryOperationTerminations'] = {
        'finding.show purged request-rejected exit2': ok(e3 + '#/$defs/StepTermination', {'class': 'request-rejected', 'errorCode': 'REQUEST.PRECONDITION_FAILED', 'domainDetail': {'code': 'evidence.purged', 'remedy': 'x'}}),
        'graph availability purged operational host-io': ok(e3 + '#/$defs/StepTermination', {'class': 'operational-failed', 'errorCode': 'HOST.IO_FAILURE', 'faultCause': 'host-io', 'domainDetail': {'code': 'evidence.purged', 'remedy': 'x'}}),
        'query completeness indeterminate with runId': ok(e3 + '#/$defs/StepTermination', {'class': 'indeterminate', 'reasonCodes': ['QUERY.COMPLETENESS_UNMET'], 'runId': 'run3:' + 'b' * 64}),
        'view unknown IDENTITY.UNKNOWN request-rejected': ok(e3 + '#/$defs/StepTermination', {'class': 'request-rejected', 'errorCode': 'IDENTITY.UNKNOWN', 'domainDetail': {'code': 'QUERY.VIEW_UNKNOWN', 'remedy': 'x'}}),
        'regeneration mismatch': ok(e3 + '#/$defs/StepTermination', {'class': 'operational-failed', 'errorCode': 'HOST.IO_FAILURE', 'faultCause': 'host-io', 'domainDetail': {'code': 'evidence.regeneration-mismatch', 'remedy': 'x', 'subject': 'run3:' + 'b' * 64}}),
        'host invariant': ok(e3 + '#/$defs/StepTermination', {'class': 'operational-failed', 'errorCode': 'SYSTEM.OUTCOME.ILLEGAL_STATE', 'faultCause': 'host-invariant', 'domainDetail': {'code': 'HOST.INVARIANT_VIOLATED', 'remedy': 'x'}}),
    }
    res['SCHEMA'] = sch
except Exception as exc:
    res['SCHEMA'] = {'error': repr(exc), 'tb': traceback.format_exc()[-2000:]}

json.dump(res, open(OUT, 'w'), indent=1, default=str)
print(json.dumps(res, indent=1, default=str)[:14000])
