"""Distinguishing controls for the invocation step/result joins (audit area 5).

Each control starts from the ADMITTED multi-step invocation of envelopes/multi-step.json and
mutates one thing that a published clause of workflows-and-surfaces section 1 refuses. The
schema still admits most of them -- which is the point: "Schema shape and the normative
step/result joins are separate obligations."

Two POSITIVE contrasts are included so the checker is not merely refusing everything:
an OPTIONAL step that fails must NOT change the aggregate, and a retry attempt on the same
admitted inputs may bind the same exec-plan2 and Run.
"""
import copy
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_schema as S
import envelopes as EV

OUT = '/tmp/opensip-design-corrections/consumer-b.v22/output'


def load():
    d = json.load(open(OUT + '/envelopes/multi-step.json'))
    return d['envelope']['invocation'], set(
        r['result']['runId'] for r in d['envelope']['invocation']['stepResults']
        if 'runId' in (r.get('result') or {}))


def one_based(inv):
    for s in inv['orderedSteps']:
        s['stepId'] += 1
    for r in inv['stepResults']:
        r['stepId'] += 1
    for s in inv['orderedSteps']:
        s['dependsOn'] = [d + 1 for d in s['dependsOn']]


def forward_dep(inv):
    inv['orderedSteps'][0]['dependsOn'] = [2]


def required_on_optional(inv):
    inv['orderedSteps'][1]['requirement'] = 'optional'


def terminal_gate(inv):
    inv['orderedSteps'][0]['dependencyGate'] = 'terminal'


def retry_on_comparison(inv):
    inv['orderedSteps'][2]['retryPolicy'] = 'idempotent-retry'


def comparison_mints_a_run(inv):
    inv['stepResults'][2]['result'] = {'kind': 'analysis', 'authority': 'authoritative',
                                      'runId': inv['stepResults'][0]['result']['runId'],
                                      'planId': inv['stepResults'][0]['result']['planId'],
                                      'verdict': 'pass',
                                      'requiredCoverage': 'satisfied',
                                      'durability': 'committed', 'deficiency': 'none',
                                      'secondaryDeficiencies': []}


def drop_comparison_result(inv):
    inv['stepResults'] = [r for r in inv['stepResults'] if r['stepId'] != 2]


def drop_derivation(inv):
    for a in inv['stepResults'][0]['attempts']:
        a.pop('derivation', None)


def comparison_verdict_fail_but_success(inv):
    inv['stepResults'][2]['result']['verdict'] = 'fail'


def aggregate_hides_a_required_failure(inv):
    inv['stepResults'][1]['termination'] = {'class': 'policy-failed',
                                           'authority': 'authoritative',
                                           'runId': inv['stepResults'][1]['result']['runId']}


def duplicate_execution_id(inv):
    a = inv['stepResults'][0]['attempts'][0]
    inv['stepResults'][0]['attempts'] = [a, dict(a)]


def delegated_without_a_consumer(inv):
    inv['orderedSteps'] = inv['orderedSteps'][:2]
    inv['stepResults'] = [r for r in inv['stepResults'] if r['stepId'] != 2]


# ---- POSITIVE contrasts
def optional_step_failure_does_not_change_the_aggregate(inv):
    inv['orderedSteps'].append(
        {'stepId': 3, 'kind': 'render', 'requirement': 'optional', 'dependsOn': [0],
         'dependencyGate': 'terminal', 'retryPolicy': 'idempotent-retry',
         'params': {'kind': 'render', 'format': 'human', 'destination': 'stdout',
                    'sourceSteps': [0], 'required': False}})
    inv['stepResults'].append(
        {'stepId': 3, 'outcome': 'failed',
         'attempts': [{'executionId': 'exec1_' + '9f' * 16, 'outcome': 'failed',
                       'faultCause': 'output-serialization'}],
         'termination': {'class': 'operational-failed',
                         'errorCode': 'OUTPUT.SERIALIZATION_FAILED',
                         'faultCause': 'output-serialization'}})


def retry_binds_the_same_exec_plan_and_run(inv):
    a = inv['stepResults'][0]['attempts'][0]
    first = dict(a, executionId='exec1_' + '0e' * 16, outcome='failed',
                 faultCause='ledger-busy', retried=True)
    inv['stepResults'][0]['attempts'] = [first, a]


CASES = [
    ('step-ids-one-based-instead-of-zero-based', one_based,
     'STEP_ID_IS_THE_ZERO_BASED_POSITION',
     'workflows section 1: "`StepId` is the zero-based position."'),
    ('a-step-depends-on-a-higher-step-id', forward_dep, 'WORKFLOW.DEPENDENCY_CYCLE',
     '"`dependsOn` names lower StepIds only (a forward or self reference is '
     'WORKFLOW.DEPENDENCY_CYCLE)"'),
    ('a-required-step-depends-on-an-optional-step', required_on_optional,
     'WORKFLOW.REQUIRED_DEPENDS_ON_OPTIONAL',
     '"a required step may not depend on an optional step"'),
    ('dependency-gate-terminal-on-an-analysis-step', terminal_gate,
     'DEPENDENCY_GATE_TERMINAL_ONLY_FOR_RENDER_OR_EXPORT_DELIVERY',
     '"`terminal` ... lawful only for render/export-delivery"'),
    # both published halves of the retry law are violated by the same mutation; the FIRST
    # refusal this checker reaches is the kind-eligibility half, and it is named as observed
    # rather than relabelled to the half this row happened to cite first
    ('idempotent-retry-on-a-comparison-step', retry_on_comparison,
     'IDEMPOTENT_RETRY_NOT_LAWFUL_FOR_THIS_STEP_KIND',
     '"`mutation`, `import`, `repair-preview`, `repair-apply`, `comparison`, '
     '`native-preparation` and `test-execution` carry `retryPolicy=none` by schema"'),
    ('a-comparison-step-result-that-mints-a-run', comparison_mints_a_run,
     'ONLY_ANALYSIS_AND_VERIFY_MINT_OR_LINK_A_RUN',
     '"Only `analysis` and `verify` steps seal or link a content-derived `run3`" and "The '
     'comparison result is a distinct closed ComparisonStepResult, never a Run"'),
    ('the-comparison-step-has-no-result-at-all', drop_comparison_result,
     'EVERY_ORDERED_STEP_IS_ACCOUNTED_IN_STEP_RESULTS',
     'the terminal result of the WHOLE selected step list must be accounted'),
    ('an-analysis-attempt-with-no-derivation-binding', drop_derivation,
     'EVERY_ANALYSIS_OR_VERIFY_ATTEMPT_OWNS_ITS_DERIVATION_BINDING',
     '"Each analysis/verify attempt owns exactly one derivation DAG ... recorded in the '
     'attempt\'s `derivation` binding"'),
    ('comparison-verdict-fail-reported-as-a-success-termination',
     comparison_verdict_fail_but_success,
     'COMPARISON_STEP_TERMINATION_DERIVES_FROM_ITS_VERDICT',
     'ComparisonStepResult: "The step termination is derived from verdict: fail -> '
     'policy-failed ... Never defaults to success."'),
    ('aggregate-success-while-a-required-step-is-policy-failed',
     aggregate_hides_a_required_failure,
     'AGGREGATE_TERMINATION_IS_THE_D9_MAXIMUM_OVER_REQUIRED_STEPS',
     '"Over required steps only: operational-failed > request-rejected > policy-failed > '
     'indeterminate > success"'),
    ('two-attempts-sharing-one-execution-id', duplicate_execution_id,
     'EACH_ATTEMPT_RECEIVES_A_FRESH_EXECUTION_ID',
     '"Each admitted attempt of a step receives a fresh ExecutionId"'),
    ('delegated-verdict-gate-with-no-consuming-comparison-step',
     delegated_without_a_consumer,
     'DELEGATED_VERDICT_GATE_REQUIRES_A_CONSUMING_COMPARISON_STEP',
     '"`delegated` requires authoritative analysis and a consuming comparison step"'),
]

POSITIVES = [
    ('optional-step-failure-does-not-change-the-aggregate',
     optional_step_failure_does_not_change_the_aggregate,
     '"An optional step\'s rejection or failure never changes the aggregate."'),
    ('a-retry-attempt-may-bind-the-same-exec-plan-and-run',
     retry_binds_the_same_exec_plan_and_run,
     '"A retry on identical admitted inputs may bind the same exec-plan2 and the same Run; '
     'attempts remain separately auditable."'),
]


def run_case(label, mutate, expect, law, positive=False):
    inv, known = load()
    inv = copy.deepcopy(inv)
    mutate(inv)
    ok, err = True, None
    try:
        res = S.admit('workflows/schemas/evaluator3/invocation-record.schema.json', '#',
                      inv, label)
        if not res['admitted']:
            ok, err = False, {'stock': res['stockSchemaErrors'][:3]}
    except Exception as e:
        ok, err = False, '%s: %s' % (type(e).__name__, str(e)[:300])
    j = EV.invocation_joins(inv, known_runs=known)
    row = {'case': label, 'classification': 'valid' if positive else 'invalid',
           'owningLaw': law, 'schemaAdmitted': ok, 'schemaError': err,
           'jointRefusals': j['refusals'],
           'firstRefusal': (j['refusals'][0] if j['refusals']
                            else ({'check': 'OWNING_SCHEMA', 'detail': err}
                                  if not ok else None)),
           'derivedAggregate': j['derivedAggregate'],
           'refused': bool(j['refusals']) or not ok}
    if positive:
        row['mustAdmit'] = True
        row['admitted'] = ok and not j['refusals']
    else:
        row['expectedOwnerJoin'] = expect
        row['firstRefusalIsTheIntendedJoin'] = expect in json.dumps(row['firstRefusal'] or {})
        row['schemaAloneWouldHaveAdmittedIt'] = ok
    return row


def main():
    rows = [run_case(l, m, e, law) for l, m, e, law in CASES]
    rows += [run_case(l, m, None, law, positive=True) for l, m, law in POSITIVES]
    for r in rows:
        if r.get('mustAdmit'):
            print('%-56s POSITIVE admitted=%-5s aggregate=%s'
                  % (r['case'][:56], r['admitted'], r['derivedAggregate']))
        else:
            print('%-56s refused=%-5s intended=%-5s schemaAlone=%-5s first=%s'
                  % (r['case'][:56], r['refused'],
                     r['firstRefusalIsTheIntendedJoin'],
                     r['schemaAloneWouldHaveAdmittedIt'],
                     (r['firstRefusal'] or {}).get('check')))
    doc = {'standing': __doc__, 'controls': rows,
           'schemaVersusJoins': (
               'the `schemaAlone` column is the finding: %d of %d invalid records are ADMITTED'
               ' by the owning schema and are refused only by the normative step/result joins.'
               % (sum(1 for r in rows if r.get('schemaAloneWouldHaveAdmittedIt')),
                  len(CASES)))}
    EV.write('envelopes/invocation-join-negative-controls.json', doc)
    bad = [r['case'] for r in rows if not r.get('mustAdmit') and not r['refused']]
    bad += [r['case'] for r in rows if r.get('mustAdmit') and not r['admitted']]
    off = [r['case'] for r in rows
           if not r.get('mustAdmit') and not r['firstRefusalIsTheIntendedJoin']]
    print()
    print(doc['schemaVersusJoins'])
    if off:
        for r in rows:
            if r['case'] in off:
                print('NOT THE INTENDED JOIN:', r['case'], '->',
                      json.dumps(r['firstRefusal'], default=str)[:180])
    if bad:
        print('FAILED CONTROLS:', bad)
    assert not bad, bad
    print('all %d invocation controls behaved as required (%d negative, %d positive)'
          % (len(rows), len(CASES), len(POSITIVES)))


main()
