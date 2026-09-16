"""RESUMED INDEPENDENT DELTA REVIEW 04 probes (reference only, no host/runtime claim)."""
import ast
import copy
import hashlib
import json
import sys
import types
from pathlib import Path
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

S = Path(__file__).resolve().parent / 'subject'
pins = json.loads((S / 'input-pins.json').read_bytes())['inputs']
B = {}
for p in pins:
    b = (S / p['path']).read_bytes()
    assert len(b) == p['bytes'] and hashlib.sha256(b).hexdigest() == p['sha256'], p['path']
    B[p['path']] = b
ref = types.ModuleType('ref'); exec(compile(B['inputs/canonical.py'], 'canonical.py', 'exec'), ref.__dict__)
docs = {}
for path in sorted((S / 'inputs/schemas').glob('*.json')):
    d = ref.parse(path.read_bytes()); docs[d['$id']] = d
V6 = ref.parse((S / 'command-envelope.v6.schema.json').read_bytes()); docs[V6['$id']] = V6
REG = Registry().with_resources((k, Resource(contents={a: v for a, v in d.items() if a != '$schema'}, specification=DRAFT202012)) for k, d in docs.items())
INV_ID = 'urn:opensip:product-v1:workflows:evaluator3:invocation:3'
ENV_ID = V6['$id']
INV = docs[INV_ID]

join = types.ModuleType('join'); exec(compile((S / 'ledger_join.py').read_bytes(), 'ledger_join.py', 'exec'), join.__dict__)

# owner model: my own extraction; successor applied by me from model-successor.json
succ = json.loads((S / 'model-successor.json').read_bytes())
src = B['inputs/workflows_model.v1.py']
assert hashlib.sha256(src).hexdigest() == succ['ownerSha256']
text = src.decode()
assert text.splitlines()[succ['selector']['startLine'] - 1] == succ['before'] and text.count(succ['before']) == 1
WANT = {'Refusal', 'terminate', 'analysis_termination', 'comparison_termination', 'exit_code', 'validate_dag',
        'raw_sha', 'synthetic_execution_id', '_exec_id', 'run_invocation'}


def load(t):
    nodes = []
    for n in ast.parse(t).body:
        if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name in WANT:
            nodes.append(n)
        elif isinstance(n, ast.Assign):
            names = {x.id for x in n.targets if isinstance(x, ast.Name)}
            if names & WANT or (names and all(x.isupper() for x in names) and not any(isinstance(c, ast.Call) for c in ast.walk(n.value))):
                nodes.append(n)
    m = types.ModuleType('owner'); m.__dict__.update(hashlib=hashlib, json=json, canonical=ref)
    exec(compile(ast.Module(body=nodes, type_ignores=[]), 'workflows_model.v1.py#extract', 'exec'), m.__dict__)
    return m


PARENT, SUCC = load(text), load(text.replace(succ['before'], succ['after']))

fx = json.loads((S / 'inputs/report-fixtures04.json').read_bytes())
gold = fx['deliveryGoldens'][24]['envelope']
ANALYSIS, RID, PID = gold['run'], gold['requestId'], gold['projectId']
rows, fails = [], []


def shape(v, sid):
    try:
        ref.validate({'$ref': sid}, v, REG); return True
    except Exception as e:
        if type(e).__name__ not in ('ValidationError', 'AdmissionError'): raise
        return False


def J(rec, env, fn=None):
    try:
        (fn or join.validate_interruption_join)(rec, env); return 'accepted'
    except join.JoinRefusal as e:
        return str(e)
    except Exception as e:
        return 'UNTYPED:' + type(e).__name__


def row(name, got, want=None, **kw):
    r = {'case': name, 'got': got, **kw}
    if want is not None:
        r['want'] = want; r['ok'] = got == want
        if got != want: fails.append(name)
    else:
        r['observation'] = True
    rows.append(r)


def params(i, kind, reqs):
    p = {'kind': kind}
    if kind == 'analysis':
        p.update(profile='default', role='primary', durability='authoritative', snapshotSource='live-worktree')
    elif kind == 'render':
        p.update(format='json', destination='stdout', sourceSteps=[j for j in range(i) if reqs[j] == 'required'], required=True)
    elif kind == 'query':
        rq = copy.deepcopy(gold['advisoryReport']['request'])
        p.update(operation=rq['operation'], completeness=rq['completeness'], page=rq['page'], request=rq)
    return p


def base(kinds, reqs=None):
    reqs = reqs or ['required'] * len(kinds)
    steps = [{'stepId': i, 'kind': k, 'requirement': reqs[i], 'dependsOn': [j for j in range(i) if reqs[j] == 'required' or reqs[i] == 'optional'],
              'dependencyGate': 'terminal' if k == 'render' else 'completed', 'retryPolicy': 'none', 'params': params(i, k, reqs)} for i, k in enumerate(kinds)]
    wf = {'kind': 'builtin', 'name': 'analyze'} if kinds.count('analysis') <= 1 and 'optional' not in reqs else \
        {'kind': 'profile', 'contributionId': 'org.example.workflow', 'activationId': 'review', 'profileVersion': '1.0.0'}
    return {'schemaFamily': 'opensip.product.invocation', 'schemaMajor': 3, 'requestId': RID, 'projectId': PID,
            'workflow': wf, 'mode': {'interactive': False, 'ci': True, 'ephemeral': False}, 'orderedSteps': steps}


def script(kinds, cut=None, sig='SIGINT', over=None):
    sc = {}
    for i, k in enumerate(kinds):
        if k == 'analysis':
            r = copy.deepcopy(ANALYSIS); r['runId'] = 'run3:' + format(i + 1, 'x') * 64
            sc[str(i)] = [{'event': 'completed', 'result': r}]
        elif k == 'render':
            sc[str(i)] = [{'event': 'completed', 'result': {'kind': 'render', 'format': 'json', 'rendererVersion': 1, 'bytes': 1, 'truncation': False, 'written': True}}]
        elif k == 'query':
            sc[str(i)] = [{'event': 'completed', 'result': {'kind': 'query', 'items': 1, 'truncated': False, 'completenessMet': True, 'advisory': True}}]
    sc.update(over or {})
    if cut is not None:
        sc['cancelAt'] = {'stepId': cut, 'signal': sig}
    return sc


def gen(model, kinds, reqs=None, cut=None, sig='SIGINT', over=None):
    return model.run_invocation(base(kinds, reqs), script(kinds, cut, sig, over))


def env_for(rec, kind=None, errors=None):
    t = rec['termination']
    e = {'schemaFamily': 'opensip.product.envelope', 'schemaMajor': 6, 'requestId': rec['requestId'], 'projectId': rec['projectId'],
         'termination': copy.deepcopy(t), 'exitCode': 130 if t['class'] == 'interrupted' else PARENT.exit_code(t)}
    kind = kind or ('run' if t.get('runId') else 'failure')
    e['kind'] = kind
    if kind == 'run':
        e['run'] = copy.deepcopy(next(r['result'] for r in reversed(rec['stepResults']) if r.get('result', {}).get('runId') == t.get('runId')))
    elif kind == 'invocation':
        e['invocation'] = copy.deepcopy(rec)
    if errors is not None:
        e['errors'] = errors
    elif kind == 'failure':
        e['errors'] = []
    return e


# ================= A. optional-Run successor: legitimacy and scope
opt_kinds, opt_reqs = ['analysis', 'render'], ['optional', 'required']
p_rec, p_code = gen(PARENT, opt_kinds, opt_reqs, 1)
s_rec, s_code = gen(SUCC, opt_kinds, opt_reqs, 1)
row('A1-parent-vs-successor-optional-commit', {'parent': p_rec['termination'], 'successor': s_rec['termination'], 'exit': [p_code, s_code],
    'stepResultsEqual': p_rec['stepResults'] == s_rec['stepResults'], 'successorRecordShape': shape(s_rec, INV_ID)},
    {'parent': {'class': 'interrupted', 'signal': 'SIGINT'}, 'successor': {'class': 'interrupted', 'signal': 'SIGINT', 'runId': 'run3:' + '1' * 64},
     'exit': [130, 130], 'stepResultsEqual': True, 'successorRecordShape': True})
row('A2-parent-model-record-refused-by-successor-join', (J(p_rec, env_for(p_rec)), shape(env_for(p_rec), ENV_ID)), ('J-INTERRUPTION-AGGREGATE', True),
    note='host records produced under the parent required-only law are refused; report aggregate must be rebased together')
er = env_for(s_rec); er.pop('run'); er['kind'] = 'failure'; er['errors'] = []; er['termination'].pop('runId')
row('A3-valid-shape-optional-run-erasure-envelope-only', (shape(er, ENV_ID), J(s_rec, er)), (True, 'J-INTERRUPTION-AGGREGATE'))
er_rec = copy.deepcopy(s_rec); er_rec['termination'].pop('runId')
row('A4-optional-run-erasure-record-and-envelope', (shape(er_rec, INV_ID), J(er_rec, er)), (True, 'J-INTERRUPTION-AGGREGATE'))
lo_kinds, lo_reqs = ['analysis', 'analysis', 'render'], ['required', 'optional', 'required']
lo, _ = gen(SUCC, lo_kinds, lo_reqs, 2)
wrong = env_for(lo); first = lo['stepResults'][0]['result']; wrong['run'] = copy.deepcopy(first); wrong['termination']['runId'] = first['runId']
row('A5-later-optional-run-wrong-last-run', (lo['termination'].get('runId'), shape(wrong, ENV_ID), J(lo, wrong)), ('run3:' + '2' * 64, True, 'J-INTERRUPTION-AGGREGATE'))
# after-settle asymmetry: settled aggregate (required-only) never names the optional Run
as_kinds, as_reqs = ['query', 'analysis', 'render'], ['required', 'optional', 'required']
full, _ = gen(SUCC, as_kinds, as_reqs, None)
cut_opt_committed, _ = gen(SUCC, as_kinds, as_reqs, 2)
row('A6-settled-vs-interrupted-run-identity', {'noSignal': full['termination'], 'signalBeforeRender': cut_opt_committed['termination']},
    note='with the successor an interrupted aggregate names the optional Run while the uninterrupted settled aggregate of the same ledger does not; owner prose must state this asymmetry')
# ephemeral optional analysis never commits
eph = script(opt_kinds, 1)
r0 = copy.deepcopy(next(o for o in [fx['bases'][k].get('envelope', {}).get('run') for k in fx['bases']] if o and o.get('authority') == 'ephemeral')) \
    if any((fx['bases'][k].get('envelope', {}).get('run') or {}).get('authority') == 'ephemeral' for k in fx['bases']) else None
if r0 is None:
    def _find(o):
        if isinstance(o, dict):
            if o.get('authority') == 'ephemeral' and o.get('kind') == 'analysis' and 'evidenceId' in o: return o
            for v in o.values():
                f = _find(v)
                if f: return f
        elif isinstance(o, list):
            for v in o:
                f = _find(v)
                if f: return f
    r0 = copy.deepcopy(_find(fx))
eb = base(opt_kinds, opt_reqs); eb['orderedSteps'][0]['params']['durability'] = 'ephemeral'
eph['0'] = [{'event': 'completed', 'result': r0}]
try:
    e_rec, _ = SUCC.run_invocation(eb, eph)
    row('A7-ephemeral-optional-analysis-not-commit', ('runId' in e_rec['termination'], J(e_rec, env_for(e_rec))), (False, 'accepted'), recordShape=shape(e_rec, INV_ID))
except Exception as ex:
    row('A7-ephemeral-optional-analysis-not-commit', 'model-script-refused:' + repr(ex)[:120])
# differential: successor-join accepts every successor-model ledger with its canonical carrier
diffs = []
for label, kinds, reqs in [('default', ['analysis', 'render'], None), ('fit', ['analysis', 'query', 'render'], None),
                           ('candidates', ['query', 'render'], None), ('opt', opt_kinds, opt_reqs), ('later-opt', lo_kinds, lo_reqs),
                           ('query-opt-analysis-render', as_kinds, as_reqs), ('opt-query-only', ['analysis', 'query'], ['optional', 'required'])]:
    for cut in [None] + list(range(len(kinds) + 1)):
        for sig in ('SIGINT', 'SIGTERM', 'SIGHUP'):
            if cut is None and sig != 'SIGINT': continue
            rec, code = gen(SUCC, kinds, reqs, cut, sig)
            if rec['termination']['class'] == 'interrupted':
                carriers = [env_for(rec), env_for(rec, 'invocation')]
            else:
                carriers = [env_for(rec, 'invocation')]
            res = [(c['kind'], shape(c, ENV_ID), J(rec, c)) for c in carriers]
            diffs.append({'wf': label, 'cut': cut, 'sig': sig, 'phase': rec.get('cancellation', {}).get('phase', 'none'), 'term': rec['termination'], 'recShape': shape(rec, INV_ID), 'carriers': res})
            if not shape(rec, INV_ID) or any(not s or j != 'accepted' for _, s, j in res):
                fails.append('A8-diff:%s@%s/%s' % (label, cut, sig))
row('A8-successor-model-differential', {'ledgers': len(diffs), 'carrierChecks': sum(len(d['carriers']) for d in diffs)}, detail=diffs)

# ================= B. verify steps and result kinds
ar = INV['$defs']['AnalysisResult']
ar_kind = json.dumps(ar.get('properties', {}).get('kind', ar))[:300]
vres = copy.deepcopy(ANALYSIS); vres['kind'] = 'verify'
row('B1-AnalysisResult-kind-schema', {'kindSchema': ar_kind, 'verifyKindShapeValid': shape(vres, INV_ID + '#/$defs/AnalysisResult'),
    'analysisKindShapeValid': shape(ANALYSIS, INV_ID + '#/$defs/AnalysisResult')})
SNAP = 'snapshot2:' + 'a' * 64
VERIFICATION = {'appliedSnapshotId': SNAP, 'verifiedSnapshotId': SNAP, 'snapshotMatched': True, 'targetsRemaining': 0, 'netNewFindings': 0}
vres['verification'] = VERIFICATION
row('B1b-authoritative-verify-result-shape', shape(vres, INV_ID + '#/$defs/AnalysisResult'), True,
    note='AnalysisResult authoritative branch: kind enum [analysis, verify]; kind=verify requires verification')
vb = base(['verify', 'render']); vb['workflow'] = {'kind': 'builtin', 'name': 'repair-verify'}
vb['orderedSteps'][0]['params'] = {'kind': 'verify', 'afterStep': 0, 'profile': 'default'}
for cut, label in [(1, 'before-settle-during-render'), (2, 'after-settle'), (None, 'no-signal')]:
    vsc = script(['verify', 'render'], cut)
    vsc['0'] = [{'event': 'completed', 'result': copy.deepcopy(vres)}]
    vrec, _ = SUCC.run_invocation(copy.deepcopy(vb), vsc)
    carrier = env_for(vrec) if vrec['termination'].get('runId') else env_for(vrec, 'invocation')
    row('B2-owner-valid-verify-ledger-' + label, {'recordShape': shape(vrec, INV_ID), 'envShape': shape(carrier, ENV_ID), 'join': J(vrec, carrier)},
        {'recordShape': True, 'envShape': True, 'join': 'J-INTERRUPTION-RESULT-KIND'},
        note='DEFECT: join maps verify steps to expected kind "analysis" but owner AnalysisResult uses kind=verify (schema enum; workflows_model.v1.py:1913). Every shape-valid ledger with a completed verify step is refused, including settled ones.')
wrongv = copy.deepcopy(vres); wrongv['kind'] = 'analysis'; wrongv.pop('verification')
vsc = script(['verify', 'render'], 1); vsc['0'] = [{'event': 'completed', 'result': wrongv}]
wv, _ = SUCC.run_invocation(copy.deepcopy(vb), vsc)
row('B3-verify-step-carrying-analysis-kind', {'recordShape': shape(wv, INV_ID), 'join': J(wv, env_for(wv))}, {'recordShape': True, 'join': 'accepted'},
    note='the join admits the wrong kind on a verify step (no verification outcome) that the owner would never emit')

# ================= C. prior errors: real vs invented, determinism
CFG = {'code': 'CONFIG.INVALID', 'remedy': 'Correct the invalid configuration.'}
# optional analysis step rejected with recorded detail, then required analysis cancelled
# (analysis params are owner-valid; import params would need invented evidence paths)
k3, rq3 = ['analysis', 'analysis', 'render'], ['optional', 'required', 'required']
b3 = base(k3, rq3)
b3['orderedSteps'][1]['dependsOn'] = []; b3['orderedSteps'][2]['dependsOn'] = [1]; b3['orderedSteps'][2]['params']['sourceSteps'] = [1]
sc3 = script(k3, 1, over={'0': [{'event': 'rejected', 'errorCode': 'CONFIG.INVALID', 'detail': 'CONFIG.INVALID', 'remedy': CFG['remedy']}]})
rec3, _ = SUCC.run_invocation(b3, sc3)
row('C0-model-optional-rejected-then-cancel', {'recordShape': shape(rec3, INV_ID), 'step0': rec3['stepResults'][0]['termination'], 'agg': rec3['termination']})
for name, errors, want in [('C1-empty-while-real-detail-recorded', [], 'accepted'),
                           ('C2-exact-real-detail', [CFG], 'accepted'),
                           ('C3-changed-remedy', [{**CFG, 'remedy': 'x'}], 'J-INTERRUPTION-INVENTED-DETAIL'),
                           ('C4-unrelated-code', [{'code': 'QUERY.VIEW_UNKNOWN', 'remedy': CFG['remedy']}], 'J-INTERRUPTION-INVENTED-DETAIL'),
                           ('C5-duplicate', [CFG, CFG], 'J-INTERRUPTION-INVENTED-DETAIL')]:
    e = env_for(rec3, errors=errors)
    row(name, (shape(e, ENV_ID), J(rec3, e)), (True, want), note='C2 detail comes from an OPTIONAL step; settled D9 would never surface it' if name.startswith('C2') else '')
# two recorded details: order / omission
k4, rq4 = ['analysis', 'analysis', 'analysis', 'render'], ['optional', 'optional', 'required', 'required']
b4 = base(k4, rq4)
for i in (0, 1): b4['orderedSteps'][i]['dependsOn'] = []
b4['orderedSteps'][2]['dependsOn'] = []; b4['orderedSteps'][3]['dependsOn'] = [2]; b4['orderedSteps'][3]['params']['sourceSteps'] = [2]
D2 = {'code': 'IMPORT.ARTIFACT_CORRUPT', 'remedy': 're-import'}
sc4 = script(k4, 2, over={'0': [{'event': 'rejected', 'errorCode': 'CONFIG.INVALID', 'detail': 'CONFIG.INVALID', 'remedy': CFG['remedy']}],
                          '1': [{'event': 'rejected', 'errorCode': 'CONFIG.INVALID', 'detail': 'IMPORT.ARTIFACT_CORRUPT', 'remedy': 're-import'}]})
rec4, _ = SUCC.run_invocation(b4, sc4)
for name, errors, want in [('C6-two-in-order', [CFG, D2], 'accepted'), ('C7-reordered', [D2, CFG], 'J-INTERRUPTION-INVENTED-DETAIL'),
                           ('C8-omission', [D2], 'J-INTERRUPTION-INVENTED-DETAIL')]:
    e = env_for(rec4, errors=errors)
    row(name, (shape(rec4, INV_ID), shape(e, ENV_ID), J(rec4, e)), (True, True, want))
# rejected step without recorded detail (route composition would supply one at projection)
sc5 = script(k3, 1, over={'0': [{'event': 'rejected', 'errorCode': 'CONFIG.INVALID'}]})
rec5, _ = SUCC.run_invocation(copy.deepcopy(b3), sc5)
row('C9-real-rejection-without-recorded-detail', {'step0': rec5['stepResults'][0]['termination'], 'emptyJoin': J(rec5, env_for(rec5)),
    'composedDetailJoin': J(rec5, env_for(rec5, errors=[CFG]))}, {'step0': {'class': 'request-rejected', 'errorCode': 'CONFIG.INVALID'}, 'emptyJoin': 'accepted',
    'composedDetailJoin': 'J-INTERRUPTION-INVENTED-DETAIL'}, note='host persistence duty is unverifiable by the join: absence of domainDetail silently selects the empty form')
# committed Run + genuine earlier error
k6, rq6 = k3, rq3
sc6 = script(k6, 2, over={'0': [{'event': 'rejected', 'errorCode': 'CONFIG.INVALID', 'detail': 'CONFIG.INVALID', 'remedy': CFG['remedy']}]})
rec6, _ = SUCC.run_invocation(copy.deepcopy(b3), sc6)
e6 = env_for(rec6, errors=[CFG])
row('C10-run-carrier-with-real-earlier-error', {'shape': shape(e6, ENV_ID), 'join': J(rec6, e6), 'withoutErrors': J(rec6, env_for(rec6))},
    note='committed branch admits errors on kind=run both with and without the recorded detail')
e7 = env_for(rec3, 'invocation'); e7['errors'] = [CFG]
row('C11-invocation-carrier-with-errors', {'shape': shape(e7, ENV_ID), 'join': J(rec3, e7)})
# failure + real details + run-bearing extras
e8 = env_for(rec3, errors=[CFG]); e8['findings'] = gold['findings']
row('C12-failure-with-real-error-plus-findings', (shape(e8, ENV_ID), J(rec3, e8)), note='findings are outside result_fields; a no-commit failure could carry findings of no Run')
e9 = env_for(rec3, errors=[CFG]); e9['advisoryReport'] = gold['advisoryReport']
row('C13-failure-with-real-error-plus-advisoryReport', (shape(e9, ENV_ID), J(rec3, e9)))

# ================= D. phase / signal / result / correlation extras
pre, _ = gen(SUCC, ['analysis', 'render'], None, 0)
for name, mut, want in [
    ('D1-cancelled-step-with-result', lambda r, e: r['stepResults'][1].update(result={'kind': 'render', 'format': 'json', 'rendererVersion': 1, 'bytes': 1, 'truncation': False, 'written': True}), 'J-INTERRUPTION-CANCELLED-STEP'),
    ('D2-cancellation-signal-vs-steps', lambda r, e: r['cancellation'].update(signal='SIGTERM'), 'J-INTERRUPTION-CANCELLED-STEP'),
    ('D3-rejected-step-carrying-result', lambda r, e: r['stepResults'].__setitem__(0, {'stepId': 0, 'outcome': 'rejected', 'attempts': [], 'result': copy.deepcopy(ANALYSIS), 'termination': {'class': 'request-rejected', 'errorCode': 'CONFIG.INVALID'}}), None),
    ('D4-projectId-dropped-from-envelope', lambda r, e: e.pop('projectId'), 'J-INTERRUPTION-CORRELATION'),
    ('D5-clientCorrelation-only-in-record', lambda r, e: r.update(clientCorrelationId='c'), 'J-INTERRUPTION-CORRELATION'),
    ('D6-exit-4-on-interrupted', lambda r, e: e.update(exitCode=4), 'J-INTERRUPTION-AGGREGATE'),
]:
    r, e = copy.deepcopy(pre), copy.deepcopy(env_for(pre)); mut(r, e)
    row(name, (shape(r, INV_ID), J(r, e)), None if want is None else (shape(r, INV_ID), want))
rows[-4]['note'] = 'non-completed step with a result is not refused unless kind mismatches; relies on StepResult admission'

# ================= E. preplanning
env_pp = env_for(pre); env_pp.pop('projectId')
ctx = {'stage': 'before-planning', 'requestId': RID, 'signal': 'SIGINT'}
PP = join.validate_preplanning_interruption
for name, c, e, want in [
    ('E1-accept', ctx, env_pp, 'accepted'),
    ('E2-extra-context-key', {**ctx, 'invocationAdmitted': False}, env_pp, 'J-INTERRUPTION-CONTEXT'),
    ('E3-stage-after-planning', {**ctx, 'stage': 'after-planning'}, env_pp, 'J-INTERRUPTION-CONTEXT'),
    ('E4-bad-requestId', {**ctx, 'requestId': 'req1_X'}, env_pp, 'J-INTERRUPTION-CONTEXT'),
    ('E5-envelope-projectId-not-in-context', ctx, env_for(pre), 'J-INTERRUPTION-CORRELATION'),
    ('E6-nonempty-errors', ctx, {**env_pp, 'errors': [CFG]}, 'J-INTERRUPTION-PREPLANNING-CARRIER'),
    ('E7-invocation-carrier', ctx, {**{k: v for k, v in env_pp.items() if k != 'errors'}, 'kind': 'invocation', 'invocation': pre}, 'J-INTERRUPTION-PREPLANNING-CARRIER'),
    ('E8-malformed-envelope', ctx, None, 'J-INTERRUPTION-INPUT'),
    ('E9-SIGKILL', {**ctx, 'signal': 'SIGKILL'}, env_pp, 'J-INTERRUPTION-SIGNAL'),
    ('E10-context-for-admitted-invocation-indistinguishable', ctx, env_pp, 'accepted'),
]:
    row(name, J(c, e, PP), want)
rows[-1]['note'] = 'same RequestId as an admitted invocation with a committed Run is still accepted: lifecycle exclusion is pure host custody'
row('E11-empty-orderedSteps-record', shape({**base(['render']), 'orderedSteps': [], 'stepResults': []}, INV_ID), False)

# ================= F. after-settle
af, _ = gen(SUCC, ['analysis', 'render'], None, 2)
row('F1-after-settle-model', (af['cancellation']['phase'], af['termination'], J(af, env_for(af))), ('after-settle', {'class': 'success', 'runId': 'run3:' + '1' * 64}, 'accepted'))
rc = env_for(af); rc.update(kind='failure', errors=[], exitCode=130, termination={'class': 'interrupted', 'signal': 'SIGINT'}); rc.pop('run')
row('F2-after-settle-reclassify', (shape(rc, ENV_ID), J(af, rc)), (True, 'J-INTERRUPTION-SETTLED'))
ao, _ = gen(SUCC, as_kinds[:2], as_reqs[:2], 1)
row('F3-optional-cancelled-after-required-settled', (ao['cancellation']['phase'], ao['termination'], J(ao, env_for(ao, 'invocation'))), ('after-settle', {'class': 'success'}, 'accepted'))
ex = env_for(af); ex['exitCode'] = 3
row('F4-settled-exit-mismatch-not-joined', J(af, ex), 'accepted', note='settled branch leaves exit/carrier to existing envelope admission')

print(json.dumps({'passed': not fails, 'failures': fails, 'rows': rows}, indent=1))
sys.exit(1 if fails else 0)
