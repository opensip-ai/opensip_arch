"""Measure the actual exception type identity escaping identity-model.v3 close_run and the graph-query route.

usage: python -I -B probe_exception_identity.py LABEL   (LABEL = before | after)
Runs over the coauthor copy only. Records, per case, the escaping class, its module-load identity against the
query's identity copy, the replay stack copy that close_run loaded, the atom/enumeration owners, jsonschema and the
query's own canonical import, and the public graph-query route. Reference evidence only.
The semantic false-result reminting follows the completed review probe (probe_overlay_semantics.py A6).
"""
import copy, hashlib, importlib.util, json, sys, traceback

RT = '/private/tmp/opensip-design-corrections/claude-source37-query-fault-author.v1'
DC = RT + '/work/source37-coauthor/docs/coop/design-corrections'
LABEL = sys.argv[1]
OUT = RT + '/receipts/probe-exception-identity.' + LABEL + '.json'
sys.path.insert(0, DC + '/foundation')
import canonical  # noqa: E402
from jsonschema import ValidationError  # noqa: E402


def load(name, path):
    s = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(s)
    sys.modules[name] = m
    s.loader.exec_module(m)
    return m


Q = load('probe_query3', DC + '/workflows/query_projection_model.v3.py')
SR = load('probe_semrep3', DC + '/foundation/check-semantic-replay.v3.py')
CR = load('probe_replaymut3', DC + '/foundation/check-replay.v3.py')
MQ = Q.identity3()
MS = SR.M
REQ = 'req1_' + '5' * 32


def ident(exc):
    R = getattr(MQ, '_COMPLETE_REPLAY', None)
    t = type(exc)
    row = {'type': t.__name__, 'classModule': t.__module__, 'mro': [c.__name__ for c in t.__mro__], 'str': str(exc)[:200],
           'queryIdentity.C.AdmissionError': isinstance(exc, MQ.C.AdmissionError),
           'queryIdentity.EvidenceUnavailable': isinstance(exc, MQ.EvidenceUnavailable),
           'queryIdentity.CompleteReplayMismatch': isinstance(exc, getattr(MQ, 'CompleteReplayMismatch', ())),
           'queryCanonical.AdmissionError': isinstance(exc, canonical.AdmissionError),
           'jsonschema.ValidationError': isinstance(exc, ValidationError), 'builtin.ValueError': isinstance(exc, ValueError),
           'cause': type(exc.__cause__).__name__ if exc.__cause__ is not None else None}
    if R is not None:
        row.update({'replayStack.M.C.AdmissionError': isinstance(exc, R.M.C.AdmissionError),
                    'replayStack.M.EvidenceUnavailable': isinstance(exc, R.M.EvidenceUnavailable),
                    'replayStack.A.AtomAdmissionError': isinstance(exc, R.A.AtomAdmissionError),
                    'replayStack.ENUM.AdmissionError': isinstance(exc, R.I.ENUM.AdmissionError)})
    if hasattr(MQ, 'replay_refusals'):
        row['queryIdentity.replay_refusals()'] = isinstance(exc, MQ.replay_refusals())
    return row


def identity_close(run, objects, blobs):
    try:
        return {'close_run': 'ADMIT', 'runId': MQ.close_run(run, objects, blobs)}
    except Exception as exc:
        return {'close_run': 'REFUSE', 'exception': ident(exc)}


def route_of(fn):
    try:
        v = fn()
        return {'result': 'ADMIT', 'value': v if isinstance(v, str) else None}
    except Q.QueryRefusal as e:
        term = e.termination()
        try:
            env = e.envelope(host={'requestId': REQ})
            ex = env['exitCode']
        except Exception as ee:
            ex = 'envelope-error:' + type(ee).__name__ + ':' + str(ee)[:80]
        return {'result': 'REFUSE', 'termination': term, 'exitCode': ex, 'diagnostic': getattr(e, 'diagnostic', None),
                'cause': type(e.__cause__).__name__ if e.__cause__ is not None else None}
    except Exception as e:
        return {'result': 'UNCAUGHT', 'type': type(e).__name__, 'error': str(e)[:200]}


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
    pid = MS.identifier('proof-bundle', proof)
    objects_[pid] = ('proof-bundle', proof)
    evidence['findingIds'] = []
    evidence['proofBundleId'] = pid
    eid = MS.identifier('semantic-evidence', evidence)
    objects_[eid] = ('semantic-evidence', evidence)
    seal['proofBundleId'] = pid
    seal['evidenceId'] = eid
    seal['verdict'] = 'pass'
    sid = MS.identifier('evaluation-seal', seal)
    objects_[sid] = ('evaluation-seal', seal)
    run_['evidenceId'] = eid
    run_['evaluationSealId'] = sid
    return run_, objects_, blobs_


res = {'label': LABEL, 'cases': {}}


def case(name, packed, structural=True):
    run, objects, blobs = packed
    row = {}
    if structural:
        try:
            row['structural'] = 'ADMIT:' + MQ.open_run_closure(run, objects, blobs)[0]
        except Exception as exc:
            row['structural'] = 'REFUSE:' + type(exc).__name__ + ':' + str(exc)[:120]
    row.update(identity_close(run, objects, blobs))
    row['queryRoute'] = route_of(lambda: Q.close_retained_run(run, objects, blobs))
    res['cases'][name] = row


try:
    gd, posd, actd = SR.case_declares_exists()
    case('positive-declares-exists', posd)
    case('semantic-root-severity', CR.remint_finding(*posd, lambda f, _b: f.update(severity='warning')))
    case('semantic-fail-to-pass', remint_false(*posd, lambda p: 'false' if p['value'] == 'true' else None))
    gi, posi, acti = SR.case_incoming_incomplete_unknown()
    case('semantic-indeterminate-laundered', remint_false(*posi, lambda p: 'false' if p['value'] == 'indeterminate' else None))
    gm, posm, actm = SR.case_missing_inventory_execution()
    case('semantic-execution-deficiency-erased', remint_false(*posm, lambda p: None))
    r2, o2, b2 = copy.deepcopy(posd)
    dom, val = o2[r2['evidenceId']]
    val = dict(val)
    val['findingIds'] = list(val['findingIds'])[:-1]
    o2[r2['evidenceId']] = (dom, val)
    case('structural-reference-identity', (r2, o2, b2))
    r3, o3, b3 = copy.deepcopy(posd)
    del o3[o3[r3['evaluationSealId']][1]['proofBundleId']]
    case('missing-proof-object', (r3, o3, b3))
    r4, o4, b4 = copy.deepcopy(posd)
    victim = next(f for v in o4[r4['evidenceId']][1]['viewIds'] for f in o4[v][1].get('facts') or [])
    digest = o4[victim][1]['payloadDigest']
    b4[digest] = b'not-the-retained-payload'
    case('corrupt-fact-payload-bytes', (r4, o4, b4))
    del b4[digest]
    case('missing-fact-payload-bytes', (r4, o4, b4))
except Exception as exc:
    res['semanticError'] = traceback.format_exc()[-3000:]

try:
    F = load('probe_exec_fixture3', DC + '/foundation/evaluator_graph_fixture.v3.py')
    RX = load('probe_exec_replay3', DC + '/foundation/evaluator_replay_model.v3.py')
    SX = load('probe_exec_seal3', DC + '/foundation/evaluator_semantic_fixture.v3.py')
    XX = load('probe_exec_capture3', DC + '/foundation/execution_inputs_fixture.v3.py')
    MX, EX = RX.M, RX.E

    def fresh(**options):
        return F.build_file_inputs(atom_override={'op': 'none', 'relation': 'file', 'minResolution': 'enumerated', 'filters': []}, **options)

    def rewrite_manifest(g, change):
        XX.attach_host_capture(g)
        manifest = copy.deepcopy(g['executionInputs'])
        change(manifest)
        raw = MX.C.canonical(manifest)
        d = hashlib.sha256(raw).hexdigest()
        g['blobs'][d] = raw
        g['executionInputs'] = manifest
        g['executionInputsDigest'] = d
        g['inputs']['executionInputsDigest'] = d
        g['inputs']['evaluationInputRefs'] = EX.cset(manifest['selectedRefs'] + [{'domain': 'execution-inputs', 'digest': d}])

    def claim_complete(manifest):
        for row in manifest['cellOutcomes']:
            row.update(state='complete', deficiency=None, nativeCause=None)

    liar = fresh(complete_required_native=False)
    rewrite_manifest(liar, claim_complete)
    seed, objects, blobs, _ = F.seal_fixture(liar)
    case('execution-inputs-lying-completion', (seed, objects, blobs))

    def omit_coverage(manifest):
        manifest['selectedRefs'] = [r for r in manifest['selectedRefs'] if r['domain'] != 'coverage']
    omit = fresh()
    rewrite_manifest(omit, omit_coverage)
    seed, objects, blobs, _ = F.seal_fixture(omit)
    case('execution-inputs-selection-join', (seed, objects, blobs))

    base = fresh()
    seed, objects, blobs, _ = F.seal_fixture(base)
    _, owner = MX.open_run_closure(seed, objects, blobs)
    i = base['inputs']
    out = RX.derive(i['planId'], i['executionPlanId'], i['evaluatorClosure'], i['evaluationInputRefs'], objects, blobs, owner)
    run, objects, blobs = SX.seal_derived(base, out, objects, blobs)
    lost = copy.deepcopy(blobs)
    del lost[out['proof']['executionInputsDigest']]
    case('execution-inputs-manifest-lost', (run, objects, lost))
    bad = copy.deepcopy(blobs)
    bad[out['proof']['executionInputsDigest']] = b'{}'
    case('execution-inputs-manifest-invalid-bytes', (run, objects, bad))
except Exception:
    res['executionError'] = traceback.format_exc()[-3000:]

# Simulated host defects (process-local monkeypatches, always restored).
try:
    posd_run, posd_obj, posd_blob = posd
    orig = MQ.close_run

    def boom_prose(*a, **k):
        raise RuntimeError('EVALUATOR_COMPLETE_PROOF_REPLAY')
    MQ.close_run = boom_prose
    try:
        res['cases']['host-defect-close_run-runtimeerror-with-replay-prose'] = {'queryRoute': route_of(lambda: Q.close_retained_run(posd_run, posd_obj, posd_blob))}
    finally:
        MQ.close_run = orig

    def boom_missing(*a, **k):
        raise KeyError('EVIDENCE_UNAVAILABLE:proof3:' + '0' * 64)
    MQ.close_run = boom_missing
    try:
        res['cases']['host-defect-close_run-keyerror-with-missing-prose'] = {'queryRoute': route_of(lambda: Q.close_retained_run(posd_run, posd_obj, posd_blob))}
    finally:
        MQ.close_run = orig

    def foreign_mismatch(*a, **k):
        cls = getattr(MS, 'CompleteReplayMismatch', None)
        if cls is None:
            raise MS.C.AdmissionError('EVALUATOR_COMPLETE_PROOF_REPLAY')
        raise cls('EVALUATOR_COMPLETE_PROOF_REPLAY')
    MQ.close_run = foreign_mismatch
    try:
        res['cases']['host-defect-close_run-foreign-identity-copy-mismatch'] = {'queryRoute': route_of(lambda: Q.close_retained_run(posd_run, posd_obj, posd_blob))}
    finally:
        MQ.close_run = orig
    MQ.close_run(posd_run, posd_obj, posd_blob)
    R = MQ._COMPLETE_REPLAY
    orig_cmp = R.E.compare_complete_replay

    def inner_boom(*a, **k):
        raise TypeError('simulated evaluator comparison defect')
    R.E.compare_complete_replay = inner_boom
    try:
        res['cases']['host-defect-inside-replay-stack'] = {'identity': identity_close(posd_run, posd_obj, posd_blob),
                                                          'queryRoute': route_of(lambda: Q.close_retained_run(posd_run, posd_obj, posd_blob))}
    finally:
        R.E.compare_complete_replay = orig_cmp
    res['cases']['positive-after-restore'] = {'queryRoute': route_of(lambda: Q.close_retained_run(posd_run, posd_obj, posd_blob))}
except Exception:
    res['hostDefectError'] = traceback.format_exc()[-3000:]

res['runIds'] = {'declares-exists': actd['runId'], 'incoming-incomplete': acti['runId'], 'missing-inventory': actm['runId']}
json.dump(res, open(OUT, 'w'), indent=1, default=str)
summary = {}
for k, v in res['cases'].items():
    qr = v.get('queryRoute') or {}
    t = qr.get('termination') or {}
    exc = v.get('exception') or {}
    summary[k] = {'structural': (v.get('structural') or '')[:60], 'close_run': v.get('close_run'), 'excType': exc.get('type'),
                  'excModule': exc.get('classModule'), 'qC': exc.get('queryIdentity.C.AdmissionError'),
                  'qEU': exc.get('queryIdentity.EvidenceUnavailable'), 'rsC': exc.get('replayStack.M.C.AdmissionError'),
                  'refusals': exc.get('queryIdentity.replay_refusals()'),
                  'route': (qr.get('result'), t.get('errorCode'), t.get('faultCause'), (t.get('domainDetail') or {}).get('code'), qr.get('exitCode'))}
print(json.dumps({'label': LABEL, 'summary': summary, 'errors': {k: res.get(k) for k in ('semanticError', 'executionError', 'hostDefectError') if res.get(k)}, 'runIds': res['runIds']}, indent=1))
