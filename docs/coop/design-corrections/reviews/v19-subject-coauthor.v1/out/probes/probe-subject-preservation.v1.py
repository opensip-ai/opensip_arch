"""Bounded probe for the workflow DomainDetail.subject loss root identified.

WHAT IS REAL HERE. `N.admit_plan_selection_cardinality`, `N.admit_requested_capability_cardinality`,
`N.unit_scope_descriptor` and `N.scope_refusal_termination` are invoked for real and raise real
exceptions; their ACTUAL typed fields are the observation supplied to `W.run_invocation`, and the
returned records are validated against the PUBLISHED pinned schemas.

WHAT IS SYNTHETIC. Every invocation record, requestId/projectId, step script and earlier committed
step result is a synthetic trusted fixture observation taken from `workflow-cases.v1.json`. Nothing
here closes an earlier Run, executes a provider, compiler, OS or filesystem, or qualifies a host.
`W.synthetic_execution_id` is the module's own declared fixture adapter. The 'earlier committed
result preserved' rows are about the invocation record the model returns, not about any Run.

The BEFORE and PROPOSED workflow models are loaded side by side from two shadow trees whose only
differing file is `workflows/workflows_model.v1.py`, so every comparison is that one edit.
"""
import copy
import hashlib
import importlib.util
import json
import pathlib
import sys

ROOT = pathlib.Path('/tmp/opensip-design-corrections/v19-subject-coauthor.v1')
NATIVE_WORK = pathlib.Path('/tmp/opensip-design-corrections/v19-native-coauthor.v1/work/docs/coop/design-corrections')
OUT = ROOT / 'out/evidence'
OUT.mkdir(parents=True, exist_ok=True)

results = []
def check(name, value, extra=None):
    row = {'id': name, 'passed': bool(value)}
    if extra is not None:
        row['observed'] = extra
    results.append(row)
    return bool(value)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


# N is READ-ONLY from the completed v19 native work; it is not part of this turn's delta.
N = load('probe_native', NATIVE_WORK / 'native/native_evidence_model.v2.py')
W_BEFORE = load('probe_wf_before', ROOT / 'out/disposable/dc-before/workflows/workflows_model.v1.py')
W_AFTER = load('probe_wf_after', ROOT / 'out/disposable/dc-proposed/workflows/workflows_model.v1.py')

CASES = json.loads((NATIVE_WORK / 'workflows/workflow-cases.v1.json').read_text())
CONST = CASES['constants']


def expand(v):
    if isinstance(v, str) and v.startswith('$'):
        return CONST[v[1:]]
    if isinstance(v, list):
        return [expand(x) for x in v]
    if isinstance(v, dict):
        return {k: expand(x) for k, x in v.items()}
    return v


BASE_CASE = expand(copy.deepcopy(CASES['invocationCases'][0]))
STEP = BASE_CASE['steps'][0]


def record_of(step_count=2):
    steps = [dict(stepId=i, kind=STEP['kind'], requirement=STEP['requirement'],
                  dependsOn=[] if i == 0 else [0], dependencyGate='completed',
                  retryPolicy=STEP['retry'], params=STEP['params']) for i in range(step_count)]
    return dict(schemaFamily='opensip.product.invocation', schemaMajor=1, requestId=CONST['REQ'],
                projectId=CONST['PRJ'], workflow={'kind': 'builtin', 'name': 'analyze'},
                mode=BASE_CASE['mode'], orderedSteps=steps)


# --------------------------------------------------------------------- the ACTUAL native refusals
def native_scope_termination(kind, field):
    """Invoke the real producer and project the real ScopeRefusal. No termination is hand-written."""
    if kind == 'plan':
        counts = {'semanticClosures': ('closure2:', 129), 'nativeContextDigests': ('', 129),
                  'importIds': ('import2:', 257)}
        prefix, count = counts[field]
        call = lambda: N.admit_plan_selection_cardinality(
            {field: [prefix + ('%064x' % i) for i in range(count)]})
    elif kind == 'requestedCapabilities':
        call = lambda: N.admit_requested_capability_cardinality(
            [{'capabilityId': 'references', 'languageMode': 'ts-tsconfig',
              'workspaceRoot': 'r%05d' % i, 'required': True}
             for i in range(N.requested_capability_bound() + 1)])
    elif kind == 'workspaceRoots':
        call = lambda: N.unit_scope_descriptor(
            [{'rootPath': 'r%05d' % i, 'languageMode': 'ts-tsconfig', 'languageFamily': 'tsjs'}
             for i in range(1025)], [])
    else:
        raise AssertionError(kind)
    try:
        call()
    except N.ScopeRefusal as exc:
        return exc, N.scope_refusal_termination(exc)
    raise AssertionError('expected a real ScopeRefusal for ' + kind + '/' + str(field))


BOUNDED = [('plan', 'semanticClosures'), ('plan', 'nativeContextDigests'), ('plan', 'importIds'),
           ('requestedCapabilities', 'requestedCapabilities'), ('workspaceRoots', 'workspaceRoots')]

rows = []
for kind, field in BOUNDED:
    refusal, termination = native_scope_termination(kind, field)
    detail = termination['domainDetail']
    observation = {'event': 'rejected', 'errorCode': termination['errorCode'],
                   'detail': detail['code'], 'subject': detail['subject'], 'remedy': detail['remedy']}
    record = record_of()
    script = {'0': BASE_CASE['script']['0'], '1': [observation]}

    before_result, before_exit = W_BEFORE.run_invocation(copy.deepcopy(record), copy.deepcopy(script))
    after_result, after_exit = W_AFTER.run_invocation(copy.deepcopy(record), copy.deepcopy(script))

    step_term = after_result['stepResults'][1]['termination']
    agg = after_result['termination']
    expected_subject = '%s:%d>%d' % (refusal.subject['field'], refusal.subject['count'],
                                     refusal.subject['limit'])

    # the exact subject the published scope refusal promises, per step AND in the aggregate
    check('exact-subject-retained-per-step.' + field,
          step_term['domainDetail'].get('subject') == detail['subject'] == expected_subject,
          {'subject': step_term['domainDetail'].get('subject')})
    check('exact-subject-retained-in-aggregate-termination.' + field,
          agg.get('domainDetail', {}).get('subject') == expected_subject)
    check('the-before-model-dropped-this-subject.' + field,
          'subject' not in before_result['stepResults'][1]['termination']['domainDetail'])
    # everything else about the envelope is unchanged
    check('exit-code-is-2-and-unchanged.' + field, after_exit == before_exit == 2,
          {'before': before_exit, 'after': after_exit})
    check('error-code-detail-and-remedy-unchanged.' + field,
          step_term['class'] == 'request-rejected' and
          step_term['errorCode'] == 'REQUEST.UNSATISFIABLE' == termination['errorCode'] and
          step_term['domainDetail']['code'] == 'PROJECT.SCOPE_LIMIT' == detail['code'] and
          step_term['domainDetail']['remedy'] == detail['remedy'])
    check('the-remedy-is-this-fields-own.' + field,
          detail['remedy'] == N.SCOPE_LIMIT_REMEDY[field])
    # the refused step mints nothing, and the earlier committed step keeps its result
    check('refused-step-has-no-result-or-derivation.' + field,
          'result' not in after_result['stepResults'][1] and
          all('derivation' not in a for a in after_result['stepResults'][1]['attempts']) and
          after_result['stepResults'][1]['outcome'] == 'rejected')
    check('earlier-committed-step-result-preserved.' + field,
          after_result['stepResults'][0]['result'] == BASE_CASE['script']['0'][0]['result'] ==
          before_result['stepResults'][0]['result'])
    # the ONLY difference between the two models' whole returned records is the subject
    stripped = copy.deepcopy(after_result)
    stripped['stepResults'][1]['termination']['domainDetail'].pop('subject')
    stripped['termination'] = dict(stripped['stepResults'][1]['termination'])
    check('the-edit-changes-exactly-one-field-of-the-whole-record.' + field,
          stripped == before_result,
          {'note': 'after-record with the subject removed equals the before-record byte for byte'})
    # PUBLISHED SCHEMAS, not a hand-written shape assertion
    schema_ok = True
    try:
        W_AFTER.validate_import_record('workflows/schemas/common.schema.json',
                                       '#/$defs/StepTermination', step_term)
        W_AFTER.validate_import_record('workflows/schemas/common.schema.json',
                                       '#/$defs/StepTermination', agg)
        W_AFTER.validate_import_record('workflows/schemas/common.schema.json',
                                       '#/$defs/DomainDetail', step_term['domainDetail'])
        W_AFTER.validate_import_record('workflows/schemas/invocation-record.schema.json',
                                       '', after_result)
    except Exception as exc:                                    # noqa: BLE001 - recorded, not hidden
        schema_ok = repr(exc)[:400]
    check('returned-termination-and-invocation-validate-against-published-schemas.' + field,
          schema_ok is True, {'error': None if schema_ok is True else schema_ok})

    rows.append({'kind': kind, 'field': field, 'nativeTermination': termination,
                 'beforeStepTermination': before_result['stepResults'][1]['termination'],
                 'afterStepTermination': step_term, 'afterAggregate': agg,
                 'exit': after_exit, 'expectedSubject': expected_subject})

# -------------------------------------------------- BACKWARD EQUALITY where no subject is supplied
# Every existing invocation case, run through BOTH models. None of them carries a subject, so the
# proposed model must return byte-identical records; this is the regression surface of the edit.
same, differing = 0, []
for case in CASES['invocationCases']:
    case = expand(copy.deepcopy(case))
    steps = [dict(stepId=i, kind=s['kind'], requirement=s['requirement'],
                  dependsOn=s.get('dependsOn', [] if i == 0 else [i - 1]),
                  dependencyGate=s.get('dependencyGate', 'completed'), retryPolicy=s['retry'],
                  params=s['params']) for i, s in enumerate(case['steps'])]
    rec = dict(schemaFamily='opensip.product.invocation', schemaMajor=1, requestId=CONST['REQ'],
               projectId=CONST['PRJ'], workflow={'kind': 'builtin', 'name': 'analyze'},
               mode=case['mode'], orderedSteps=steps)
    try:
        b = W_BEFORE.run_invocation(copy.deepcopy(rec), copy.deepcopy(case['script']))
    except Exception as exc:                                    # noqa: BLE001
        b = ('raised', repr(exc)[:200])
    try:
        a = W_AFTER.run_invocation(copy.deepcopy(rec), copy.deepcopy(case['script']))
    except Exception as exc:                                    # noqa: BLE001
        a = ('raised', repr(exc)[:200])
    if a == b:
        same += 1
    else:
        differing.append(case.get('id', '?'))
check('every-existing-invocation-case-is-byte-identical-under-the-edit',
      not differing and same == len(CASES['invocationCases']),
      {'identical': same, 'total': len(CASES['invocationCases']), 'differing': differing})

# The other observation events that reach `dd`, each with NO subject: unchanged.
NO_SUBJECT = [
    {'event': 'rejected', 'errorCode': 'REQUEST.UNSATISFIABLE', 'detail': 'PROJECT.SCOPE_LIMIT',
     'remedy': 'narrow the selection'},
    {'event': 'rejected', 'errorCode': 'REQUEST.UNSATISFIABLE'},
    {'event': 'provider-unavailable', 'detail': 'native.capability-unavailable'},
    {'event': 'baseline-unsupported', 'detail': 'BASELINE.RECIPE_UNSUPPORTED'},
    {'event': 'query-completeness-unmet', 'detail': 'QUERY.COMPLETENESS_UNMET'},
    {'event': 'operational-fault', 'faultCause': 'host-io', 'detail': 'REPAIR.RECOVERY_BLOCKED'},
    {'event': 'completed-analysis', 'verdict': 'indeterminate', 'detail': 'PROJECT.SCOPE_LIMIT'},
]
check('every-dd-carrying-event-without-a-subject-is-unchanged',
      all(W_BEFORE.terminate(copy.deepcopy(o)) == W_AFTER.terminate(copy.deepcopy(o))
          for o in NO_SUBJECT))
check('a-detailless-observation-still-produces-no-domain-detail',
      'domainDetail' not in W_AFTER.terminate({'event': 'rejected', 'errorCode': 'REQUEST.UNSATISFIABLE'}))

# ------------------------------------------------- the two producers of one shape now agree
# `Refusal.termination()` already carried a subject onto the identical record. The edit uses the SAME
# truthiness test, so the two agree on present, absent and empty-string subjects alike.
for label, subject in (('present', 'importIds:257>256'), ('absent', None), ('empty', '')):
    ref = W_AFTER.Refusal('REQUEST.UNSATISFIABLE', 'PROJECT.SCOPE_LIMIT', 'narrow it',
                          subject).termination()
    obs = {'event': 'rejected', 'errorCode': 'REQUEST.UNSATISFIABLE', 'detail': 'PROJECT.SCOPE_LIMIT',
           'remedy': 'narrow it'}
    if subject is not None:
        obs['subject'] = subject
    check('the-two-producers-of-one-termination-now-agree.' + label,
          W_AFTER.terminate(obs) == ref, {'termination': W_AFTER.terminate(obs)})
check('the-before-model-disagreed-with-its-own-sibling-producer',
      W_BEFORE.terminate({'event': 'rejected', 'errorCode': 'REQUEST.UNSATISFIABLE',
                          'detail': 'PROJECT.SCOPE_LIMIT', 'remedy': 'narrow it',
                          'subject': 'importIds:257>256'}) !=
      W_BEFORE.Refusal('REQUEST.UNSATISFIABLE', 'PROJECT.SCOPE_LIMIT', 'narrow it',
                       'importIds:257>256').termination())

# ------------------------------------------------------- honest limits, asserted rather than implied
# The edit COPIES; it does not admit. A malformed trusted observation still yields a record the
# published schema refuses, and this probe states that rather than claiming otherwise.
bad = W_AFTER.terminate({'event': 'rejected', 'errorCode': 'REQUEST.UNSATISFIABLE',
                         'detail': 'PROJECT.SCOPE_LIMIT', 'remedy': 'r', 'subject': 'x' * 2000})
refused = False
try:
    W_AFTER.validate_import_record('workflows/schemas/common.schema.json', '#/$defs/DomainDetail',
                                   bad['domainDetail'])
except Exception:                                               # noqa: BLE001
    refused = True
check('an-over-length-subject-from-a-malformed-observation-is-still-refused-by-the-schema-not-by-this-edit',
      refused and len(bad['domainDetail']['subject']) == 2000)

# ------------------------------------------------------- META: the schema validator is LIVE here
# A validation control that never refuses anything proves nothing, so the validator used above is
# shown to admit a well-formed record and to refuse an unregistered code, a wrong-typed subject, an
# over-length subject, an undeclared property and a non-record at the invocation root selector.
def _validates(doc, sel, val):
    try:
        W_AFTER.validate_import_record(doc, sel, val)
        return 'ADMIT'
    except Exception:                                           # noqa: BLE001
        return 'REFUSE'


_CS = 'workflows/schemas/common.schema.json'
_DD = '#/$defs/DomainDetail'
_meta = {
    'well-formed-detail': _validates(_CS, _DD, {'code': 'PROJECT.SCOPE_LIMIT', 'remedy': 'r',
                                                'subject': 'importIds:257>256'}),
    'unregistered-code': _validates(_CS, _DD, {'code': 'NOT.A.REGISTERED_CODE', 'remedy': 'r'}),
    'subject-wrong-type': _validates(_CS, _DD, {'code': 'PROJECT.SCOPE_LIMIT', 'remedy': 'r',
                                                'subject': 7}),
    'subject-over-length': _validates(_CS, _DD, {'code': 'PROJECT.SCOPE_LIMIT', 'remedy': 'r',
                                                 'subject': 'x' * 2000}),
    'undeclared-property': _validates(_CS, _DD, {'code': 'PROJECT.SCOPE_LIMIT', 'remedy': 'r',
                                                 'notAField': 1}),
    'invocation-root-selector-on-a-non-record':
        _validates('workflows/schemas/invocation-record.schema.json', '', {'nope': 1}),
}
check('the-schema-validator-used-above-is-live-and-discriminating',
      _meta['well-formed-detail'] == 'ADMIT' and
      all(v == 'REFUSE' for k, v in _meta.items() if k != 'well-formed-detail'), _meta)

report = {
    'probe': 'v19-subject-coauthor.v1 subject preservation',
    'standing': ('Actual reference composition. The native cardinality producers raise real '
                 'exceptions and their real typed fields are the observation; the returned records '
                 'are validated against the published pinned schemas. Invocation records, IDs, step '
                 'scripts and the earlier committed step result are SYNTHETIC trusted fixture '
                 'observations from workflow-cases.v1.json. No product host, no earlier Run closure, '
                 'no provider, compiler, OS or filesystem execution, and no qualification.'),
    'syntheticAdapters': ['W.synthetic_execution_id (the module\'s own declared fixture adapter)',
                          'workflow-cases.v1.json constants REQ/PRJ and step scripts',
                          'the earlier completed step result, supplied by the case script'],
    'sourceHashes': {
        'workflow.before.py': hashlib.sha256((ROOT / 'workflow.before.py').read_bytes()).hexdigest(),
        'workflow.proposed.py': hashlib.sha256((ROOT / 'workflow.proposed.py').read_bytes()).hexdigest(),
        'native_evidence_model.v2.py (read-only, from the completed v19 work)':
            hashlib.sha256((NATIVE_WORK / 'native/native_evidence_model.v2.py').read_bytes()).hexdigest(),
    },
    'passed': sum(1 for r in results if r['passed']),
    'failed': [r for r in results if not r['passed']],
    'checks': results,
    'boundedFieldRows': rows,
}
(OUT / 'probe-result.json').write_text(json.dumps(report, indent=1) + '\n', encoding='utf-8')
print(json.dumps({'passed': report['passed'], 'failed': len(report['failed']),
                  'failedIds': [r['id'] for r in report['failed']]}, indent=1))
