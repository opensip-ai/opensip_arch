"""Proposed fit binding/projection owner. Reference dictionaries model host custody."""
import copy


class BindingRefusal(ValueError):
    pass


class RequiredProjectionFailure(ValueError):
    """Map through the existing required-render failure owner; preserve settled data."""


def query_parts(record):
    if record['workflow'] != {'kind':'builtin','name':'fit'}:
        raise BindingRefusal('fit-workflow-required')
    queries = [s for s in record['orderedSteps'] if s['kind']=='query']
    if len(queries)!=1:
        raise BindingRefusal('one-fit-query-required')
    step = queries[0]
    params = step['params']
    if set(params)!={'kind','operation','sourceStep'} or params['kind']!='query' or params['operation']!='candidate.list':
        raise BindingRefusal('fit-source-params')
    source_id = params['sourceStep']
    if type(source_id) is not int or not 0 <= source_id < step['stepId']:
        raise BindingRefusal('earlier-source-step')
    if source_id not in step['dependsOn'] or step['dependencyGate']!='completed':
        raise BindingRefusal('completed-source-dependency')
    sources = [s for s in record['orderedSteps'] if s['stepId']==source_id and s['kind']=='analysis']
    if len(sources)!=1:
        raise BindingRefusal('analysis-source-required')
    results = {r['stepId']:r for r in record['stepResults']}
    if len(results)!=len(record['stepResults']):
        raise BindingRefusal('duplicate-step-results')
    return step, results[step['stepId']], results[source_id]


def resolved_request(record):
    _, _, source = query_parts(record)
    if source['outcome']!='completed' or source.get('result',{}).get('kind')!='analysis':
        raise BindingRefusal('source-analysis-not-completed')
    result = source['result']
    if result['authority']=='ephemeral':
        if 'runId' in result:
            raise BindingRefusal('ephemeral-run-forbidden')
        return None
    if result['authority']!='authoritative' or 'runId' not in result:
        raise BindingRefusal('committed-source-required')
    return {'schemaFamily':'opensip.product.query','schemaMajor':3,
            'projectId':record['projectId'],'view':{'runId':result['runId']},
            'operation':'candidate.list','params':{'includeSuppressed':False},
            'completeness':'best-effort','page':{'size':100}}


def _completed_attempt(query):
    attempts = query['attempts']
    if query['outcome']!='completed' or not attempts or attempts[-1]['outcome']!='completed':
        raise BindingRefusal('completed-query-attempt-required')
    return attempts[-1]['executionId']


def ephemeral_report():
    parity = dict.fromkeys(['runId','candidates','evidenceLevels','candidatesTruncated','candidatesTotalItems','candidatesNextCursor'])
    parity['candidatesAvailability']='unavailable-ephemeral-analysis'
    return {'state':'unavailable-ephemeral-analysis','parity':parity}


def capture_completed(record, report, admit_report_and_derive_summary, equal_typed):
    """Atomic step-completion boundary is a product duty; this validates its modeled output."""
    step, query, _ = query_parts(record)
    execution = _completed_attempt(query)
    request = resolved_request(record)
    if request is None:
        if not equal_typed(report,ephemeral_report()):
            raise BindingRefusal('ephemeral-advisory-form')
        summary = {'kind':'query','items':0,'truncated':False,'completenessMet':False,'advisory':True}
    else:
        if report.get('state')!='sealed-run-first-page' or not equal_typed(report.get('request'),request):
            raise BindingRefusal('exact-resolved-query-request')
        # Must admit complete shape, existing candidate/page/parity joins and
        # derive the actual owner summary. A product API cannot accept an
        # arbitrary caller callback as authority.
        summary = admit_report_and_derive_summary(report, record['projectId'],request['view']['runId'])
    if not equal_typed(query['result'],summary):
        raise BindingRefusal('query-summary-response-join')
    return {'requestId':record['requestId'],'stepId':step['stepId'],'executionId':execution,
            'report':copy.deepcopy(report)}


def project_interrupted(record, envelope, completed_handle, admit_report_and_derive_summary, equal_typed):
    """Parents first admit the full interruption record/envelope/availability joins."""
    if envelope['termination']['class']!='interrupted' or not equal_typed(envelope['termination'],record['termination']):
        raise BindingRefusal('interrupted-aggregate-required')
    if envelope['requestId']!=record['requestId'] or envelope.get('projectId')!=record['projectId']:
        raise BindingRefusal('envelope-request-project')
    out = copy.deepcopy(envelope)
    if out['kind']=='failure':
        if 'advisoryReport' in out or 'runId' in out['termination']:
            raise BindingRefusal('no-run-failure-carrier')
        return out
    if out['kind']!='run' or out['run']['authority']!='authoritative':
        raise BindingRefusal('authoritative-run-carrier-required')
    _, query, source = query_parts(record)
    if source['outcome']!='completed' or source['result'].get('runId')!=out['run']['runId']:
        raise BindingRefusal('same-producing-run-required')
    if query['outcome']=='completed':
        if completed_handle is None:
            raise RequiredProjectionFailure('completed-fit-response-not-retained')
        expected = capture_completed(record,completed_handle['report'],admit_report_and_derive_summary,equal_typed)
        if not equal_typed(expected,completed_handle):
            raise BindingRefusal('completed-response-custody-join')
        report = expected['report']
    elif query['outcome'] in ('cancelled','skipped','failed','rejected'):
        if completed_handle is not None:
            raise BindingRefusal('response-for-uncompleted-query')
        parity = dict.fromkeys(['candidates','evidenceLevels','candidatesTruncated','candidatesTotalItems','candidatesNextCursor'])
        parity.update(runId=out['run']['runId'],candidatesAvailability='unavailable-query-result')
        report = {'state':'unavailable-query-result','queryOutcome':query['outcome'],'parity':parity}
    else:
        # A recovered abandoned or malformed nonterminal query is outside
        # this live, admitted interrupted builtin path.
        raise RequiredProjectionFailure('fit-query-ended-without-advisory-response')
    if 'advisoryReport' in out and not equal_typed(out['advisoryReport'],report):
        raise BindingRefusal('existing-advisory-report-mismatch')
    out['advisoryReport']=copy.deepcopy(report)
    return out
