"""RESUMED INDEPENDENT DELTA REVIEW 07 probes: F1 prose, N1 attempt binding, capacity boundary (reference only)."""
import ast
import copy
import hashlib
import json
import re
import sys
import types
from pathlib import Path
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

S = Path(__file__).resolve().parent / 'subject'
M = {f['path']: f['sha256'] for f in json.loads((S.parent / 'manifest.json').read_bytes())['files']}


def verified(rel):
    data = (S / rel).read_bytes()
    assert hashlib.sha256(data).hexdigest() == M[rel], rel
    return data


PINS = {p['path']: p for p in json.loads(verified('input-pins.json'))['inputs']}
for rel, p in PINS.items():
    b = (S / rel).read_bytes()
    assert len(b) == p['bytes'] and hashlib.sha256(b).hexdigest() == p['sha256'], rel
ref = types.ModuleType('ref'); exec(compile(verified('inputs/canonical.py'), 'canonical.py', 'exec'), ref.__dict__)
docs = {}
for path in sorted((S / 'inputs/schemas').glob('*.json')):
    d = ref.parse(verified(str(path.relative_to(S)))); docs[d['$id']] = d
V6 = ref.parse(verified('command-envelope.v6.schema.json')); docs[V6['$id']] = V6
REG = Registry().with_resources((k, Resource(contents={a: v for a, v in d.items() if a != '$schema'}, specification=DRAFT202012)) for k, d in docs.items())
INV_ID, ENV_ID = 'urn:opensip:product-v1:workflows:evaluator3:invocation:3', V6['$id']
join = types.ModuleType('join'); exec(compile(verified('ledger_join.py'), 'ledger_join.py', 'exec'), join.__dict__)
inventory = json.loads(verified('inputs/inventory5.json'))
fx = json.loads(verified('inputs/report-fixtures04.json'))
rows, fails = [], []


def row(name, got, want=None, **kw):
    r = {'case': name, 'got': got, **kw}
    if want is not None:
        r['want'] = want; r['ok'] = got == want
        if got != want: fails.append(name)
    else:
        r['observation'] = True
    rows.append(r)


def shape(v, sid):
    try:
        ref.validate({'$ref': sid}, v, REG); return True
    except Exception as e:
        if type(e).__name__ not in ('ValidationError', 'AdmissionError'): raise
        return False


# ================= F1: all three prose spans against the pinned owner bytes
owner = verified('inputs/workflows-and-surfaces.md')
lines = owner.decode().splitlines()
ovs = json.loads(verified('passage-overrides.json'))['overrides']
spans = []
for i, ov in enumerate(ovs):
    s, e = ov['selector']['startLine'], ov['selector']['endLine']
    spans.append((s, e))
    row('F1a-before-image-%d-%d' % (s, e), (ov['sourceSha256'] == hashlib.sha256(owner).hexdigest(), '\n'.join(lines[s - 1:e]) == ov['before']), (True, True))
ordered = sorted(spans)
row('F1b-spans-disjoint', all(a[1] < b[0] for a, b in zip(ordered, ordered[1:])), True, spans=ordered)
# apply bottom-up to get the selected owner text
new_lines = list(lines)
for ov in sorted(ovs, key=lambda o: -o['selector']['startLine']):
    s, e = ov['selector']['startLine'], ov['selector']['endLine']
    new_lines[s - 1:e] = ov['after'].split('\n')
selected = '\n'.join(new_lines)
flat = ' '.join(selected.split())
row('F1c-no-availability-ban-anywhere', [m.group(0) for m in re.finditer(r'[^.]{0,120}(Run-availability|no findings, advisoryReport or [^.]*availability)[^.]*', flat)], [])
duties = {
    'entry-points': 'validate_interruption_delivery',
    'preplanning-entry': 'validate_preplanning_delivery',
    'helpers-insufficient': 'narrower ledger and preplanning helpers alone do not satisfy delivery admission',
    'no-run-availability': 'its existence does not depend on a committed Run',
    'attempt': 'must have at least one recorded attempt and cannot be skipped',
    'skipped-term': '`{class: request-rejected, errorCode: REQUEST.PRECONDITION_FAILED}` with no composed detail',
    'completeness-custody': 'that completeness is a host custody duty, not inferred from a Run result',
    'profile-owner-addition': 'A profile containing an analysis or verify step has the same empty-collection duty',
    'preplanning-empty': 'Before planning, a host-resolved command whose inventory requires the parity field supplies the explicit empty account',
    'no-nonempty-preplanning': 'No nonempty account is legal before planning',
    'findings-still-banned': 'no findings or advisoryReport payload is carried',
}
row('F1d-selected-duties-present', {k: v in flat for k, v in duties.items()}, {k: True for k in duties})
# internal consistency of the selected document around the omission law
omission = re.search(r'an omission is a required-delivery operational fault[^.]*\.', flat)
row('F1e-omission-law-interaction', omission.group(0) if omission else None,
    note='existing law: omitting a required account is operational-failed delivery; for an interrupted invocation the join refuses the envelope, but which D9 class is delivered is not restated (observation O1)')
ser = 'OUTPUT.SERIALIZATION_FAILED' in V6['description']
row('F1f-envelope-overflow-law-present', ser, True, note='envelope description: output serialization overflow uses OUTPUT.SERIALIZATION_FAILED / output-serialization')

# ================= N1: attempt binding with owner-model ledgers
ntree = ast.parse(verified('inputs/native_evidence_model.v2.py'))
nn = [n for n in ntree.body if (isinstance(n, ast.FunctionDef) and n.name in ('release_absence_notices', 'invocation_availability'))
      or (isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'PUBLIC_ROUTE_REMEDIES' for t in n.targets))]
native = {}; exec(compile(ast.Module(body=nn, type_ignores=[]), 'native#extract', 'exec'), native)
PROJECT = native['invocation_availability']
succ = json.loads(verified('model-successor.json'))
wtext = verified('inputs/workflows_model.v1.py').decode().replace(succ['before'], succ['after'])
WANT = {'Refusal', 'terminate', 'analysis_termination', 'comparison_termination', 'exit_code', 'validate_dag', 'raw_sha', 'synthetic_execution_id', '_exec_id', 'run_invocation'}
wn = []
for n in ast.parse(wtext).body:
    if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name in WANT:
        wn.append(n)
    elif isinstance(n, ast.Assign):
        names = {x.id for x in n.targets if isinstance(x, ast.Name)}
        if names & WANT or (names and all(x.isupper() for x in names) and not any(isinstance(c, ast.Call) for c in ast.walk(n.value))):
            wn.append(n)
MODEL = types.ModuleType('owner'); MODEL.__dict__.update(hashlib=hashlib, json=json, canonical=ref)
exec(compile(ast.Module(body=wn, type_ignores=[]), 'workflows_model#extract', 'exec'), MODEL.__dict__)
gold = fx['deliveryGoldens'][24]['envelope']
ANALYSIS, RID, PID = gold['run'], gold['requestId'], gold['projectId']


def ledger(kinds, reqs, cut, over=None, workflow=None):
    steps = []
    for i, k in enumerate(kinds):
        if k == 'analysis':
            p = {'kind': k, 'profile': 'default', 'role': 'primary', 'durability': 'authoritative', 'snapshotSource': 'live-worktree'}
        else:
            p = {'kind': 'render', 'format': 'json', 'destination': 'stdout', 'sourceSteps': [j for j in range(i) if reqs[j] == 'required'], 'required': True}
        steps.append({'stepId': i, 'kind': k, 'requirement': reqs[i], 'dependsOn': [j for j in range(i) if reqs[j] == 'required' or reqs[i] == 'optional'],
                      'dependencyGate': 'terminal' if k == 'render' else 'completed', 'retryPolicy': 'none', 'params': p})
    wf = workflow or {'kind': 'builtin', 'name': 'default'}
    rec0 = {'schemaFamily': 'opensip.product.invocation', 'schemaMajor': 3, 'requestId': RID, 'projectId': PID, 'workflow': wf,
            'mode': {'interactive': False, 'ci': True, 'ephemeral': False}, 'orderedSteps': steps}
    sc = {}
    for i, k in enumerate(kinds):
        if k == 'analysis':
            r = copy.deepcopy(ANALYSIS); r['runId'] = 'run3:' + format(i + 1, 'x') * 64
            sc[str(i)] = [{'event': 'completed', 'result': r}]
        else:
            sc[str(i)] = [{'event': 'completed', 'result': {'kind': 'render', 'format': 'json', 'rendererVersion': 1, 'bytes': 7, 'truncation': False, 'written': True}}]
    sc.update(over or {})
    if cut is not None:
        sc['cancelAt'] = {'stepId': cut, 'signal': 'SIGINT'}
    return MODEL.run_invocation(rec0, sc)[0]


def carrier(rec, selections, include=True):
    t = rec['termination']
    kind = 'run' if t.get('runId') else ('failure' if t['class'] == 'interrupted' else 'invocation')
    e = {'schemaFamily': 'opensip.product.envelope', 'schemaMajor': 6, 'kind': kind, 'requestId': RID, 'projectId': PID,
         'termination': copy.deepcopy(t), 'exitCode': MODEL.exit_code(t)}
    if kind == 'run':
        e['run'] = copy.deepcopy(next(r['result'] for r in reversed(rec['stepResults']) if r.get('result', {}).get('runId') == t['runId']))
    elif kind == 'invocation':
        e['invocation'] = copy.deepcopy(rec)
    ds = [r['termination']['domainDetail'] for r in rec['stepResults'] if r['outcome'] not in ('cancelled', 'skipped')
          and r['termination']['class'] in ('request-rejected', 'operational-failed') and 'domainDetail' in r['termination']]
    if t['class'] == 'interrupted' and (ds or kind == 'failure'):
        e['errors'] = ds
    if include:
        e['availability'] = PROJECT([(s['stepId'], s['undeclared']) for s in selections])
    return e


def D(rec, env, sels):
    try:
        join.validate_interruption_delivery(rec, env, {'requestId': RID, 'workflow': copy.deepcopy(rec['workflow']), 'perStep': sels}, inventory, PROJECT)
        return 'accepted'
    except join.JoinRefusal as ex:
        return str(ex)


NOTICE = {'capabilityId': 'call-graph', 'languageMode': 'typescript', 'workspaceRoot': 'packages/a'}
SEL0 = [{'stepId': 0, 'undeclared': [NOTICE]}]
two = (['analysis', 'analysis', 'render'], ['optional', 'required', 'required'])
prof = {'kind': 'profile', 'contributionId': 'org.example.workflow', 'activationId': 'review', 'profileVersion': '1.0.0'}
cases = {}
# unstarted cancelled (owner model: signal before start)
r = ledger(['analysis', 'render'], ['required', 'required'], 0)
cases['model-unstarted-cancelled'] = (r, r['stepResults'][0]['attempts'], 'J-AVAILABILITY-SELECTION')
# started then cancelled mid-attempt (host record; model cannot emit this)
r = ledger(['analysis', 'render'], ['required', 'required'], 0)
r['stepResults'][0]['attempts'] = [{'executionId': 'exec1_' + '1' * 32, 'outcome': 'cancelled'}]
cases['started-then-cancelled'] = (r, r['stepResults'][0]['attempts'], 'accepted')
# model rejected attempt
r = ledger(*two, 1, over={'0': [{'event': 'rejected', 'errorCode': 'CONFIG.INVALID', 'detail': 'CONFIG.INVALID', 'remedy': 'fix'}]}, workflow=prof)
cases['model-rejected-with-attempt'] = (r, r['stepResults'][0]['attempts'], 'accepted')
# admission rejection without attempt (model ephemeral-authority style)
r2 = copy.deepcopy(r); r2['stepResults'][0]['attempts'] = []
cases['rejected-without-attempt'] = (r2, [], 'J-AVAILABILITY-SELECTION')
# model operational fault attempt
r = ledger(*two, 1, over={'0': [{'event': 'operational-fault', 'faultCause': 'host-io', 'detail': 'DELIVERY.CLOSURE_BYTES_CORRUPT', 'remedy': 'doctor'}]}, workflow=prof)
cases['model-failed-with-attempt'] = (r, r['stepResults'][0]['attempts'], 'accepted')
# model completed
r = ledger(['analysis', 'render'], ['required', 'required'], 1)
cases['model-completed'] = (r, r['stepResults'][0]['attempts'], 'accepted')
# model skipped (required analysis rejected, dependent analysis skipped, render cancelled)
r = ledger(['analysis', 'analysis', 'render'], ['required', 'required', 'required'], 2, over={'0': [{'event': 'rejected', 'errorCode': 'CONFIG.INVALID'}]}, workflow=prof)
cases['model-skipped'] = (r, r['stepResults'][1]['attempts'], 'J-AVAILABILITY-SELECTION')
for name, (rec, attempts, want) in cases.items():
    sid = 1 if name == 'model-skipped' else 0
    sels = [{'stepId': sid, 'undeclared': [NOTICE]}]
    env = carrier(rec, sels)
    got = (shape(rec, INV_ID), shape(env, ENV_ID), D(rec, env, sels))
    row('N1-' + name, {'outcome': rec['stepResults'][sid]['outcome'], 'attempts': len(attempts), 'result': got},
        {'outcome': rec['stepResults'][sid]['outcome'], 'attempts': len(attempts), 'result': (True, True, want)})
# unstarted cancelled step contributes nothing, so the parity empty account is still accepted
r = cases['model-unstarted-cancelled'][0]
row('N1-unstarted-cancelled-empty-parity-account', D(r, carrier(r, []), []), 'accepted')
# attempt present but empty selection -> selected-empty step entry remains distinct from no selection
r = cases['model-completed'][0]
row('N1-selected-empty-vs-none', (D(r, carrier(r, [{'stepId': 0, 'undeclared': []}]), [{'stepId': 0, 'undeclared': []}]),
                                  D(r, carrier(r, []), [{'stepId': 0, 'undeclared': []}]),
                                  D(r, carrier(r, []), [])), ('accepted', 'J-AVAILABILITY-PROJECTION', 'accepted'))
# N2 stays a custody duty: omission of a completed analysis selection is still admitted
row('N2-completed-selection-omitted-is-custody-only', D(r, carrier(r, []), []), 'accepted', note='consistent with the published prose: the join cannot discover an unsupplied selection')
# attempts field type confusion is typed
r3 = copy.deepcopy(cases['model-completed'][0]); r3['stepResults'][0]['attempts'] = None
row('N1-attempts-null-typed', D(r3, carrier(r3, SEL0), SEL0), 'J-AVAILABILITY-INPUT')

# ================= N4 rename present in root result
rr = json.loads(verified('root-result.json'))
row('N4-renamed', ('invalid-availability-shape' in [p['case'] for p in rr['probes']], 'new-form-no-availability' in [p['case'] for p in rr['probes']]), (True, False))
bad = {'schemaFamily': 'opensip.product.envelope', 'schemaMajor': 6, 'kind': 'failure', 'requestId': RID, 'termination': {'class': 'interrupted', 'signal': 'SIGINT'}, 'exitCode': 130, 'errors': []}
row('N4-valid-empty-account-positive', (shape({**bad, 'availability': {}}, ENV_ID), shape({**bad, 'availability': PROJECT([])}, ENV_ID)), (False, True))

# ================= L02 boundary: capacity is outside this join
big = [{'stepId': 0, 'undeclared': [{'capabilityId': 'call-graph', 'languageMode': 'typescript', 'workspaceRoot': ('r%04d' % i) + 'w' * 4091} for i in range(995)]}]
r = cases['model-completed'][0]
env = carrier(r, big)
try:
    size = len(ref.canonical(env)); codec = 'ok'
except Exception as ex:
    size, codec = None, type(ex).__name__ + ':' + str(ex)
row('L02-single-step-995-notices-4096-roots', {'join': D(r, env, big), 'shape': shape(env, ENV_ID), 'canonical': codec, 'bytes': size},
    note='join and shape accept a required account that the 4 MiB canonical codec refuses; capacity/overflow precedence is a separate owner/integration duty (L02), not absorbed here')

print(json.dumps({'passed': not fails, 'failures': fails, 'rows': rows}, indent=1))
sys.exit(1 if fails else 0)
