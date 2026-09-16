"""CommandEnvelope major 2 reconstruction, with the laws the envelope schema states in prose
implemented independently of stock JSON Schema:

  * exitCode DERIVES from termination.class by the fixed table; it is never stored twice with
    a second opinion, so a mismatch is refused rather than tolerated.
  * the D9 branch contract per class (success carries no error/reason/signal; policy-failed
    carries runId OR authority=ephemeral; request-rejected / operational-failed carry
    errorCode, and operational-failed also a non-none faultCause; indeterminate carries
    reasonCodes; interrupted carries signal, and runId only when a Run was committed).
  * `kind=failure` requires a NONEMPTY errors array, and where the step termination carries a
    domainDetail the envelope `errors` is EXACTLY that detail, so the two surfaces cannot
    disagree.
  * a D9 class is never reclassified after settle.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_core as K
import opensip_schema as S

# THE SELECTED COMPOSITION is evaluator3: its common document carries run3 RunIds, which the
# sealed Runs of this origin actually mint. The major-1 sibling documents are present in the
# kit and are NOT used for these envelopes; selecting them would have put a `run2:` pattern
# against a `run3:` identity, which is a composition-selection error rather than a schema one.
ENV_DOC = 'workflows/schemas/evaluator3/command-envelope.schema.json'
COMMON_DOC = 'workflows/schemas/evaluator3/common.schema.json'

EXIT_BY_CLASS = {'success': 0, 'policy-failed': 1, 'request-rejected': 2,
                 'indeterminate': 3, 'operational-failed': 4, 'interrupted': 130}


def branch_refusals(term):
    """The schema-enforced branch contract, applied independently."""
    ref = []
    cls = term['class']
    has = lambda k: term.get(k) is not None
    if cls == 'success':
        for k in ('errorCode', 'reasonCodes', 'signal'):
            if has(k):
                ref.append('SUCCESS_CARRIES_NO_' + k.upper())
    if cls == 'policy-failed':
        if not (has('runId') or term.get('authority') == 'ephemeral'):
            ref.append('POLICY_FAILED_CARRIES_RUNID_OR_AUTHORITY_EPHEMERAL')
    if cls in ('request-rejected', 'operational-failed') and not has('errorCode'):
        ref.append('THIS_CLASS_REQUIRES_AN_ERROR_CODE')
    if cls == 'operational-failed' and term.get('faultCause') in (None, 'none'):
        ref.append('OPERATIONAL_FAILED_REQUIRES_A_NON_NONE_FAULT_CAUSE')
    if cls == 'indeterminate' and not term.get('reasonCodes'):
        ref.append('INDETERMINATE_REQUIRES_REASON_CODES')
    if cls == 'interrupted' and not has('signal'):
        ref.append('INTERRUPTED_REQUIRES_A_SIGNAL')
    return ref


def admit(env, label, *, run_committed=False):
    """Returns a result row: stock+keyword schema admission, then the prose laws."""
    ok, err = True, None
    try:
        res = S.admit(ENV_DOC, '#', env, label)
        if not res['admitted']:
            ok = False
            err = {'stockSchemaErrors': res['stockSchemaErrors'],
                   'publishedKeywordRefusals': res['publishedKeywordRefusals']}
    except Exception as e:
        ok, err = False, '%s: %s' % (type(e).__name__, str(e)[:700])
    ref = []
    term = env.get('termination') or {}
    want_exit = EXIT_BY_CLASS.get(term.get('class'))
    if env.get('exitCode') != want_exit:
        ref.append({'check': 'EXIT_CODE_DERIVES_FROM_THE_TERMINATION_CLASS',
                    'detail': {'class': term.get('class'), 'declared': env.get('exitCode'),
                               'derived': want_exit}})
    for r in branch_refusals(term):
        ref.append({'check': 'D9_BRANCH_CONTRACT:' + r, 'detail': term})
    if env.get('kind') == 'failure':
        if not env.get('errors'):
            ref.append({'check': 'FAILURE_ENVELOPE_CARRIES_A_NONEMPTY_ERRORS_ARRAY',
                        'detail': None})
        elif term.get('domainDetail') is not None:
            if env['errors'] != [term['domainDetail']]:
                ref.append({'check': 'ERRORS_IS_EXACTLY_THE_STEP_DOMAIN_DETAIL',
                            'detail': {'errors': env['errors'],
                                       'stepDomainDetail': term['domainDetail']}})
    if term.get('class') == 'interrupted' and term.get('runId') and not run_committed:
        ref.append({'check': 'INTERRUPTED_CARRIES_RUNID_ONLY_WHEN_A_RUN_WAS_COMMITTED',
                    'detail': term.get('runId')})
    return {'label': label, 'owningSchemaAdmitted': ok, 'owningSchemaError': err,
            'prosaicLawRefusals': ref,
            'firstRefusal': (ref[0] if ref else
                             ({'check': 'OWNING_SCHEMA', 'detail': err} if not ok else None)),
            'admitted': ok and not ref, 'envelope': env}


RUN_SEALING_KINDS = ('analysis', 'verify')
NEVER_MINT_A_RUN = ('comparison', 'query', 'render', 'import', 'repair-preview',
                    'repair-apply', 'test-execution', 'native-preparation', 'mutation',
                    'export-delivery', 'doctor')
RETRYABLE_KINDS = ('analysis', 'verify', 'query', 'render', 'doctor', 'export-delivery')
NO_RETRY_KINDS = ('mutation', 'import', 'repair-preview', 'repair-apply', 'comparison',
                  'native-preparation', 'test-execution')
TERMINAL_GATE_KINDS = ('render', 'export-delivery')
D9_ORDER = ['success', 'indeterminate', 'policy-failed', 'request-rejected',
            'operational-failed']


def invocation_joins(inv, *, known_runs=None):
    """workflows-and-surfaces section 1 + invocation-record: the NORMATIVE step/result joins,
    which are a SEPARATE obligation from schema shape.

    Implemented from the clauses, not restated:
      * "`StepId` is the zero-based position" -- so orderedSteps[i].stepId == i;
      * "`dependsOn` names lower StepIds only (a forward or self reference is
        WORKFLOW.DEPENDENCY_CYCLE)";
      * "a required step may not depend on an optional step
        (WORKFLOW.REQUIRED_DEPENDS_ON_OPTIONAL)";
      * "`dependencyGate` ... `terminal` ... lawful only for render/export-delivery";
      * retryPolicy: idempotent-retry only for analysis/verify/query/render/doctor/
        export-delivery, and seven kinds carry `none` by schema;
      * "a step has at most 3 attempts" and "Each admitted attempt ... receives a fresh
        ExecutionId";
      * "Only `analysis` and `verify` steps seal or link a content-derived `run3`";
      * "Each analysis/verify attempt owns exactly one derivation DAG ... recorded in the
        attempt's `derivation` binding";
      * "`delegated` requires authoritative analysis and a consuming comparison step";
      * aggregate termination over REQUIRED steps only, D9 ordering
        operational-failed > request-rejected > policy-failed > indeterminate > success, and
        "An optional step's rejection or failure never changes the aggregate";
      * every ordered step is accounted in stepResults.

    HELPER OMISSION V17-D6 this closes: the v16 reconstruction built a schema-valid
    invocation whose stepIds were ONE-based, whose comparison step carried no result at all,
    and whose analysis attempts carried no derivation binding -- and then checked only that
    the envelope validated.
    """
    ref = []

    def bad(code, detail):
        ref.append({'check': code, 'detail': detail})

    steps = inv['orderedSteps']
    results = {r['stepId']: r for r in (inv.get('stepResults') or [])}
    if len(steps) > 64:
        bad('WORKFLOW.AT_MOST_64_STEPS', len(steps))
    by_id = {}
    for i, s in enumerate(steps):
        if s['stepId'] != i:
            bad('STEP_ID_IS_THE_ZERO_BASED_POSITION',
                {'position': i, 'stepId': s['stepId']})
        by_id[s['stepId']] = s
    for s in steps:
        for d in s.get('dependsOn') or []:
            if d >= s['stepId']:
                bad('WORKFLOW.DEPENDENCY_CYCLE',
                    {'stepId': s['stepId'], 'dependsOn': d,
                     'why': 'dependsOn names LOWER StepIds only'})
            elif s['requirement'] == 'required' and d in by_id \
                    and by_id[d]['requirement'] == 'optional':
                bad('WORKFLOW.REQUIRED_DEPENDS_ON_OPTIONAL',
                    {'stepId': s['stepId'], 'dependsOn': d})
        if s.get('dependencyGate') == 'terminal' and s['kind'] not in TERMINAL_GATE_KINDS:
            bad('DEPENDENCY_GATE_TERMINAL_ONLY_FOR_RENDER_OR_EXPORT_DELIVERY',
                {'stepId': s['stepId'], 'kind': s['kind']})
        if s.get('retryPolicy') == 'idempotent-retry' and s['kind'] not in RETRYABLE_KINDS:
            bad('IDEMPOTENT_RETRY_NOT_LAWFUL_FOR_THIS_STEP_KIND',
                {'stepId': s['stepId'], 'kind': s['kind']})
        if s['kind'] in NO_RETRY_KINDS and s.get('retryPolicy') != 'none':
            bad('THIS_STEP_KIND_CARRIES_RETRY_POLICY_NONE',
                {'stepId': s['stepId'], 'kind': s['kind'],
                 'retryPolicy': s.get('retryPolicy')})
        r = results.get(s['stepId'])
        if r is None:
            bad('EVERY_ORDERED_STEP_IS_ACCOUNTED_IN_STEP_RESULTS',
                {'stepId': s['stepId'], 'kind': s['kind']})
            continue
        atts = r.get('attempts') or []
        if len(atts) > 3:
            bad('AT_MOST_THREE_ATTEMPTS_PER_STEP', len(atts))
        ex = [a['executionId'] for a in atts]
        if len(set(ex)) != len(ex):
            bad('EACH_ATTEMPT_RECEIVES_A_FRESH_EXECUTION_ID', ex)
        dom = r.get('result') or {}
        if s['kind'] in RUN_SEALING_KINDS:
            for a in atts:
                if a.get('outcome') != 'completed':
                    continue
                d = a.get('derivation')
                if not d:
                    bad('EVERY_ANALYSIS_OR_VERIFY_ATTEMPT_OWNS_ITS_DERIVATION_BINDING',
                        {'stepId': s['stepId'], 'executionId': a.get('executionId')})
                else:
                    if d.get('stagesCompleted', 0) > d.get('stageCount', 0):
                        bad('DERIVATION_STAGES_COMPLETED_AT_MOST_STAGE_COUNT', d)
                    if dom.get('planId') and d.get('planId') != dom['planId']:
                        bad('ATTEMPT_DERIVATION_PLAN_EQUALS_THE_STEP_RESULT_PLAN',
                            {'attempt': d.get('planId'), 'result': dom.get('planId')})
        else:
            if 'runId' in dom:
                bad('ONLY_ANALYSIS_AND_VERIFY_MINT_OR_LINK_A_RUN',
                    {'stepId': s['stepId'], 'kind': s['kind'], 'runId': dom['runId']})
        if s['kind'] == 'comparison' and dom:
            if dom.get('kind') != 'comparison' or 'comparisonResultId' not in dom:
                bad('COMPARISON_RESULT_IS_A_COMPARISON_STEP_RESULT_NOT_A_RUN', dom)
            else:
                want = {'fail': 'policy-failed', 'indeterminate': 'indeterminate',
                        'pass': 'success'}[dom['verdict']]
                if (r['termination'] or {}).get('class') != want:
                    bad('COMPARISON_STEP_TERMINATION_DERIVES_FROM_ITS_VERDICT',
                        {'verdict': dom['verdict'], 'derived': want,
                         'declared': (r['termination'] or {}).get('class')})
        # verdictGate delegated requires an authoritative analysis AND a consuming comparison
        p = s.get('params') or {}
        if p.get('kind') == 'analysis' and p.get('verdictGate') == 'delegated':
            if p.get('durability') != 'authoritative':
                bad('DELEGATED_VERDICT_GATE_REQUIRES_AUTHORITATIVE_ANALYSIS',
                    {'stepId': s['stepId'], 'durability': p.get('durability')})
            consumers = [c for c in steps if c['kind'] == 'comparison'
                         and (c.get('params') or {}).get('currentStep') == s['stepId']]
            pivots = [c for c in steps if c['kind'] == 'comparison'
                      and (c.get('params') or {}).get('pivotStep') == s['stepId']]
            if not consumers and not pivots:
                bad('DELEGATED_VERDICT_GATE_REQUIRES_A_CONSUMING_COMPARISON_STEP',
                    {'stepId': s['stepId']})
        if known_runs is not None and dom.get('runId') \
                and dom['runId'] not in known_runs:
            bad('STEP_RESULT_RUN_ID_IS_AN_ACTUAL_ADMITTED_RUN_OF_THIS_ORIGIN',
                {'stepId': s['stepId'], 'runId': dom['runId'],
                 'admitted': sorted(known_runs)})
    # aggregate over REQUIRED steps only
    req = [s['stepId'] for s in steps if s['requirement'] == 'required']
    classes = [(results[i]['termination'] or {}).get('class')
               for i in req if i in results]
    agg = 'success'
    for c in classes:
        if c in D9_ORDER and D9_ORDER.index(c) > D9_ORDER.index(agg):
            agg = c
    declared = (inv.get('termination') or {}).get('class')
    if declared != agg:
        bad('AGGREGATE_TERMINATION_IS_THE_D9_MAXIMUM_OVER_REQUIRED_STEPS',
            {'requiredStepClasses': classes, 'derived': agg, 'declared': declared})
    return {'refusals': ref, 'derivedAggregate': agg,
            'requiredSteps': req,
            'optionalSteps': [s['stepId'] for s in steps
                              if s['requirement'] == 'optional'],
            'stepKinds': [s['kind'] for s in steps]}


def write(rel, obj):
    p = ('/tmp/opensip-design-corrections/consumer-b.v17/output/' + rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w') as f:
        json.dump(obj, f, indent=1, default=str)
