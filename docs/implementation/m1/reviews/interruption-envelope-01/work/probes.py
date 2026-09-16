"""Independent reviewer probes for the envelope6 pre-Run interruption proposal.

Runs against the reviewer's verified copy. Schema/reference trial only.
"""
import copy
import hashlib
import json
import sys
import types
from pathlib import Path
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

SUBJECT = Path(__file__).resolve().parent / 'subject'
TMP = Path(__file__).resolve().parent.parent / 'tmp'


def load_ref():
    pins = json.loads((SUBJECT / 'input-pins.json').read_bytes())['inputs']
    pinned = {}
    for pin in pins:
        data = (SUBJECT / pin['path']).read_bytes()
        assert len(data) == pin['bytes'] and hashlib.sha256(data).hexdigest() == pin['sha256'], pin['path']
        pinned[pin['path']] = data
    ref = types.ModuleType('reviewer_canonical')
    exec(compile(pinned['inputs/canonical.py'], 'canonical.py', 'exec'), ref.__dict__)
    return ref


ref = load_ref()
docs = {}
for path in sorted((SUBJECT / 'inputs/schemas').glob('*.json')):
    d = ref.parse(path.read_bytes())
    docs[d['$id']] = d
V5 = ref.parse((SUBJECT / 'inputs/envelope5.json').read_bytes())
V6 = ref.parse((SUBJECT / 'command-envelope.v6.schema.json').read_bytes())


def registry_with(v6doc):
    all_docs = dict(docs)
    all_docs[V5['$id']] = V5
    all_docs[v6doc['$id']] = v6doc
    return Registry().with_resources(
        (k, Resource(contents={a: b for a, b in d.items() if a != '$schema'}, specification=DRAFT202012))
        for k, d in all_docs.items())


REG = registry_with(V6)


def admits(value, sid, reg=REG):
    try:
        ref.validate({'$ref': sid}, value, reg)
        return True
    except Exception as e:  # noqa
        if type(e).__name__ not in ('ValidationError', 'AdmissionError'):
            raise
        return False


def a5(v):
    v = copy.deepcopy(v); v['schemaMajor'] = 5
    return admits(v, V5['$id'])


def a6(v, reg=REG):
    v = copy.deepcopy(v); v['schemaMajor'] = 6
    return admits(v, V6['$id'], reg)


results = []
failures = []


def case(name, value, want5, want6, note=''):
    g5, g6 = a5(value), a6(value)
    ok = (want5 is None or g5 == want5) and g6 == want6
    results.append({'case': name, 'major5': g5, 'major6': g6, 'ok': ok, **({'note': note} if note else {})})
    if not ok:
        failures.append(name)
    return g5, g6


RID = 'req1_' + '0123456789abcdef' * 2
BASE = {'schemaFamily': 'opensip.product.envelope', 'schemaMajor': 6, 'kind': 'failure', 'requestId': RID,
        'termination': {'class': 'interrupted', 'signal': 'SIGTERM'}, 'exitCode': 130, 'errors': []}


def w(**changes):
    v = copy.deepcopy(BASE)
    for k, val in changes.items():
        if val is DEL:
            del v[k]
        else:
            v[k] = val
    return v


DEL = object()

# ---- gap reproduction and new positive forms
for sig in ['SIGINT', 'SIGTERM', 'SIGHUP']:
    case('pos-preRun-' + sig, w(termination={'class': 'interrupted', 'signal': sig}), False, True)
case('pos-correlation-all-optional', w(clientCorrelationId='c' * 128, projectId='prj1-' + '0' * 64,
     projectRoot='.'), False, True, 'optional correlation fields admitted')
proj_ok = a6(w(projectId='prj1-' + '0' * 64))
results.append({'case': 'info-projectId-pattern-used', 'major6': proj_ok})

# ---- gap: is there any v5 carrier for a pre-Run interruption without invented detail?
common = docs['urn:opensip:product-v1:workflows:evaluator3:common:3']
codes = common['$defs']['DomainDetailCode']
code_list = codes.get('enum') or [x.get('const') for x in codes.get('oneOf', codes.get('anyOf', [])) if 'const' in x]
detail_admit = [c for c in code_list if a5(w(errors=[{'code': c, 'remedy': 'r'}]))]
results.append({'case': 'gap-v5-failure-interrupted-with-some-detail', 'domainDetailCodes': len(code_list),
                'codesShapeAdmittedWithInterrupted': len(detail_admit),
                'interruptionNamingCodes': [c for c in code_list if any(t in c.upper() for t in ('INTERR', 'CANCEL', 'SIGNAL', 'ABORT'))],
                'note': 'v5 admits kind=failure/interrupted only by attaching an arbitrary unrelated DomainDetail'})
if not code_list:
    failures.append('could-not-enumerate-DomainDetailCode')
case('gap-v5-errors-absent', w(errors=DEL), False, False, 'allOf/3 requires errors on failure in both majors')
case('gap-v5-diagnostics-hack', w(diagnostics=['interrupted']), False, False,
     'diagnostic-only form still requires UNKNOWN_OPTION/exit2')
case('gap-v5-unknown-option-mislabel', w(termination={'class': 'request-rejected', 'errorCode': 'REQUEST.UNKNOWN_OPTION'},
     exitCode=2, diagnostics=['interrupted']), True, True, 'existing branch lies about the event; not a lawful substitute')
case('gap-kind-run-no-run', w(kind='run', errors=DEL, projectId='prj1-' + '0' * 64), False, False, 'kind=run requires run')
case('gap-kind-doctor-empty', w(kind='doctor', errors=DEL, doctor={}), False, False, 'doctor requires DoctorResult and is command-specific')

# ---- after-commit Run preservation (report04 golden, read-only import)
gold_path = TMP / 'run-interrupted-golden.json'
if gold_path.exists():
    gold = json.loads(gold_path.read_bytes())
    case('run-bearing-interrupted-golden', gold, True, True, 'report04 deliveryGoldens/24 envelope; unchanged')
    g = copy.deepcopy(gold); g['errors'] = []
    case('run-bearing-plus-empty-errors', g, False, False)
    g = copy.deepcopy(gold); g['kind'] = 'failure'; g.pop('run'); g['errors'] = []; g.pop('advisoryReport', None)
    case('committed-runId-on-new-form', g, False, False, 'new form cannot drop a committed Run while keeping runId')
    g.pop('availability', None); g.pop('findings', None)
    case('committed-runId-on-new-form-stripped', g, False, False, 'runId still refused after stripping all payloads')
    g['termination'].pop('runId')
    case('committed-run-erased-via-new-form', g, False, True,
         'SCHEMA CANNOT DETECT erasure of a committed Run; only host ledger/D9 admission can refuse (finding F2)')
else:
    failures.append('golden-missing')

# ---- negatives on the new form
for k in ['diagnostics', 'run', 'findings', 'advisoryReport', 'query', 'querySurface', 'queryResponse', 'queryRecord',
          'mutation', 'doctor', 'invocation', 'meta', 'retentionDisclosure', 'agentHints', 'availability']:
    case('neg-payload-' + k, w(**{k: {} if k not in ('diagnostics', 'findings', 'agentHints') else ['x']}), False, False)
case('neg-payload-diagnostics-empty-array', w(diagnostics=[]), False, False)
case('neg-unknown-top-key', w(cancelled=True), False, False)
for k, val in [('runId', 'run3:' + '0' * 64), ('executionId', 'x'), ('authority', 'ephemeral'), ('coverageId', 'x'),
               ('domainDetail', {'code': 'CONFIG.INVALID', 'remedy': 'r'}), ('errorCode', 'HOST.IO_FAILURE'), ('phase', 'before-settle')]:
    t = {'class': 'interrupted', 'signal': 'SIGINT', k: val}
    case('neg-termination-extra-' + k, w(termination=t), False, False)
for name, val in [('errors-null', None), ('errors-object', {}), ('errors-one', [{'code': 'CONFIG.INVALID', 'remedy': 'r'}]),
                  ]:
    case('neg-' + name, w(errors=val), False if name != 'errors-one' else None, False if name != 'errors-one' else True,
         'errors-one is the pre-existing detail-bearing failure shape (unrelated detail), still admitted' if name == 'errors-one' else '')
for name, changes in [
    ('clientCorrelationId-null', {'clientCorrelationId': None}), ('clientCorrelationId-empty', {'clientCorrelationId': ''}),
    ('clientCorrelationId-129', {'clientCorrelationId': 'c' * 129}), ('projectId-null', {'projectId': None}),
    ('requestId-null', {'requestId': None}), ('termination-null', {'termination': None}), ('exitCode-null', {'exitCode': None}),
    ('kind-absent', {'kind': DEL}), ('kind-null', {'kind': None}), ('schemaFamily-wrong', {'schemaFamily': 'x'}),
    ('signal-null', {'termination': {'class': 'interrupted', 'signal': None}}),
    ('termination-array', {'termination': [{'class': 'interrupted', 'signal': 'SIGINT'}]}),
    ('exit-130-with-unknown-option', {'termination': {'class': 'request-rejected', 'errorCode': 'REQUEST.UNKNOWN_OPTION'}, 'diagnostics': ['d']}),
    ('interrupted-exit2-with-diagnostics', {'exitCode': 2, 'diagnostics': ['d']}),
    ('interrupted-exit0', {'exitCode': 0}), ('interrupted-exit4', {'exitCode': 4}),
    ('success-class-with-signal', {'termination': {'class': 'success', 'signal': 'SIGINT'}}),
    ('success-exit130', {'termination': {'class': 'success'}}),
    ('opfailed-exit130', {'termination': {'class': 'operational-failed', 'errorCode': 'HOST.IO_FAILURE', 'faultCause': 'host-io'}}),
    ('policy-failed-ephemeral-exit130', {'termination': {'class': 'policy-failed', 'authority': 'ephemeral'}}),
    ('indeterminate-exit130', {'termination': {'class': 'indeterminate', 'reasonCodes': ['x']}}),
]:
    case('neg-' + name, w(**changes), False, False)
for kind in ['run', 'query', 'mutation', 'invocation', 'doctor', 'meta']:
    case('neg-empty-errors-kind-' + kind, w(kind=kind), False, False)

# ---- old UNKNOWN_OPTION branch unchanged
UO = w(termination={'class': 'request-rejected', 'errorCode': 'REQUEST.UNKNOWN_OPTION'}, exitCode=2, diagnostics=['--bogus'])
case('old-unknown-option', UO, True, True)
for name, ch in [('no-diag', {'diagnostics': DEL}), ('empty-diag', {'diagnostics': []}), ('exit4', {'exitCode': 4}),
                 ('other-code', {'termination': {'class': 'request-rejected', 'errorCode': 'CONFIG.INVALID'}}),
                 ('with-signal', {'termination': {'class': 'request-rejected', 'errorCode': 'REQUEST.UNKNOWN_OPTION', 'signal': 'SIGINT'}})]:
    v = copy.deepcopy(UO)
    for k, val in ch.items():
        if val is DEL: v.pop(k)
        else: v[k] = val
    case('old-unknown-option-' + name, v, False, False)
v = copy.deepcopy(UO); v['run'] = {}
case('old-unknown-option-with-run', v, False, False)

# ---- byte-level admission (absence vs duplicate/float)
raw_dup = b'{"schemaFamily":"opensip.product.envelope","schemaMajor":6,"kind":"failure","requestId":"' + RID.encode() + \
    b'","termination":{"class":"interrupted","signal":"SIGINT"},"exitCode":130,"errors":[],"errors":[{"code":"CONFIG.INVALID","remedy":"r"}]}'
raw_float = raw_dup.replace(b',"errors":[{"code":"CONFIG.INVALID","remedy":"r"}]', b'').replace(b'130', b'130.0')
for name, raw in [('duplicate-errors-key', raw_dup), ('float-exit', raw_float)]:
    try:
        ref.parse(raw); got = 'parsed'
    except Exception as e:
        got = type(e).__name__
    results.append({'case': 'bytes-' + name, 'result': got, 'ok': got == 'AdmissionError'})
    if got != 'AdmissionError': failures.append('bytes-' + name)

# ---- superset: every v5-admitted value among all probes and 43 fixtures is v6-admitted; v6\\v5 is only the new form
fixtures = json.loads((SUBJECT / 'inputs/metadata-fixtures.json').read_bytes())['cases']
pop = [c['value'] for c in fixtures] + [BASE, UO]
if gold_path.exists():
    pop.append(gold)
superset_viol, new_only = [], []
for v in pop:
    g5, g6 = a5(v), a6(v)
    if g5 and not g6: superset_viol.append(v.get('kind'))
    if g6 and not g5: new_only.append((v.get('kind'), v.get('errors'), v.get('termination')))
results.append({'case': 'superset-population', 'size': len(pop), 'violations': superset_viol, 'v6OnlyCount': len(new_only)})
if superset_viol or any(n[0] != 'failure' or n[1] != [] or n[2].get('class') != 'interrupted' for n in new_only):
    failures.append('superset')
for r in results:
    if r.get('major6') and not r.get('major5') and r['case'] not in ('info-projectId-pattern-used',):
        t = r['case']
        if not (t.startswith('pos-') or t == 'committed-run-erased-via-new-form'):
            failures.append('unexpected-v6-only:' + t)

# ---- targeted mutations of the new alternative
KILL = {
    'diag': w(diagnostics=['d']), 'runId': w(termination={'class': 'interrupted', 'signal': 'SIGINT', 'runId': 'run3:' + '0' * 64}),
    'exit4': w(exitCode=4), 'sigkill': w(termination={'class': 'interrupted', 'signal': 'SIGKILL'}),
    'kind-invocation': w(kind='invocation'), 'uo-no-diag': {**UO, 'diagnostics': []},
    'errors-one-interrupted': None, 'success': w(termination={'class': 'success'}),
    'retention': w(retentionDisclosure={}), 'exec': w(termination={'class': 'interrupted', 'signal': 'SIGINT', 'executionId': 'x'}),
}
KILL.pop('errors-one-interrupted')


def mutate(label, fn):
    doc = copy.deepcopy(V6)
    fn(doc['allOf'][19]['then']['oneOf'])
    reg = registry_with(doc)
    killed_by = [k for k, v in KILL.items() if a6(v, reg)]
    pos = all(a6(w(termination={'class': 'interrupted', 'signal': s}), reg) for s in ['SIGINT', 'SIGTERM', 'SIGHUP']) and a6(UO, reg)
    return {'mutation': label, 'killedBy': killed_by, 'positivesStillAdmitted': pos}


def drop(path):
    def f(alts):
        node = alts
        for p in path[:-1]:
            node = node[p]
        del node[path[-1]]
    return f


def setv(path, val):
    def f(alts):
        node = alts
        for p in path[:-1]:
            node = node[p]
        node[path[-1]] = val
    return f


mutations = [
    mutate('drop alt2 not', drop([1, 'not'])),
    mutate('drop termination additionalProperties', drop([1, 'properties', 'termination', 'additionalProperties'])),
    mutate('drop exitCode const', drop([1, 'properties', 'exitCode'])),
    mutate('signal -> any string', setv([1, 'properties', 'termination', 'properties', 'signal'], {'type': 'string'})),
    mutate('drop kind const', drop([1, 'properties', 'kind'])),
    mutate('drop errors maxItems', drop([1, 'properties', 'errors'])),
    mutate('class const -> any D9Class', setv([1, 'properties', 'termination', 'properties', 'class'],
           {'$ref': 'urn:opensip:product-v1:workflows:evaluator3:common:3#/$defs/D9Class'})),
    mutate('drop termination required', drop([1, 'properties', 'termination', 'required'])),
    mutate('drop retentionDisclosure from not', lambda a: a[1]['not']['anyOf'].remove({'required': ['retentionDisclosure']})),
    mutate('alt1 diagnostics minItems 0', setv([0, 'properties', 'diagnostics', 'minItems'], 0)),
    mutate('drop alt2 entirely', lambda a: a.pop(1)),
]
mutations_json = []
for m in mutations:
    mutations_json.append(m)
# ---- real-payload `not` member discrimination: placeholder {} payloads fail their own
# schemas, so they cannot show the `not` clause is load-bearing. Use owner-valid payloads.
real = {}
if gold_path.exists():
    for k in ['run', 'availability', 'findings', 'advisoryReport']:
        real[k] = gold[k]
qpath = TMP / 'query-golden.json'
if qpath.exists():
    q = json.loads(qpath.read_bytes())
    for k in ['query', 'querySurface', 'queryRecord']:
        real[k] = q[k]
meta_case = next(c['value'] for c in fixtures if c['value'].get('kind') == 'meta' and a5(c['value']))
real['meta'] = meta_case['meta']
real['diagnostics'] = ['d']
not_members = []
for k, val in real.items():
    in_v6 = a6(w(**{k: val}))
    doc = copy.deepcopy(V6)
    doc['allOf'][19]['then']['oneOf'][1]['not']['anyOf'].remove({'required': [k]})
    in_mutant = a6(w(**{k: val}), registry_with(doc))
    not_members.append({'member': k, 'admittedByV6': in_v6, 'admittedWithoutNotMember': in_mutant,
                        'standing': 'load-bearing' if in_mutant else 'redundant (other existing constraint also refuses)'})
    if in_v6:
        failures.append('real-payload-admitted:' + k)
mutations_json.append({'notMemberDiscrimination': not_members})
# oneOf -> anyOf equivalence
doc = copy.deepcopy(V6); t = doc['allOf'][19]['then']; t['anyOf'] = t.pop('oneOf')
reg = registry_with(doc)
equiv = all(a6(v, reg) == a6(v) for v in pop + list(KILL.values()) + [w(termination={'class': 'interrupted', 'signal': s}) for s in ['SIGINT', 'SIGHUP']])
mutations_json.append({'mutation': 'oneOf -> anyOf', 'equivalentOnPopulation': equiv})

out = {'passed': not failures, 'failures': failures, 'caseCount': len(results), 'cases': results, 'mutations': mutations_json}
print(json.dumps(out, indent=2))
sys.exit(0 if not failures else 1)
