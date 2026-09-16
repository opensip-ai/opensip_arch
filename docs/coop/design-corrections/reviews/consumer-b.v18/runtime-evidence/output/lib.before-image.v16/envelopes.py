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


def write(rel, obj):
    p = ('/tmp/opensip-design-corrections/consumer-b.v16/output/' + rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w') as f:
        json.dump(obj, f, indent=1, default=str)
