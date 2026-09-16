"""Join invocation5 replay to envelope7 with the selected candidate-list owner laws.

This validates source dictionaries; it does not implement storage custody or a
query executor. A trusted caller must obtain the page from the exact request.
"""
from pathlib import Path
import ast
import hashlib
import json
import types

HERE=Path(__file__).resolve().parent
ENV='urn:opensip:product-v1:workflows:evaluator3:command-envelope:7'


def owner_summary(canonical):
    row=next(r for r in json.loads((HERE/'workflow-input-pins.json').read_text())['files'] if Path(r['path']).name=='query_surface_projection.v3.py')
    raw=Path(row['path']).read_bytes()
    assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
    names={'QuerySurfaceProjectionError','_equal','_join','_summary','command_surface_summary'}
    nodes=[n for n in ast.parse(raw).body if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name in names]
    assert {n.name for n in nodes}==names
    namespace={'canonical':canonical}
    exec(compile(ast.Module(body=nodes,type_ignores=[]),'pinned-query-owner#candidate-list','exec'),namespace)
    return namespace['command_surface_summary']


def admit_page(report,project_id,run_id,canonical,model,validate):
    validate(ENV+'#/$defs/FitAdvisoryReportV1',report)
    if report['state']!='sealed-run-first-page':raise ValueError('sealed candidate response required')
    record=report['candidateList'];context=record['context'];request=report['request']
    if request['projectId']!=project_id or request['view']!={'runId':run_id} or context['resolvedView']!={'runId':run_id}:
        raise ValueError('query response exact Run/project join')
    if record['includeSuppressed']!=request['params']['includeSuppressed']:
        raise ValueError('candidate suppression selection join')
    summary=owner_summary(canonical)('candidate-list',record,{'projectId':project_id})
    listed=len(record['candidates'])
    if listed>100 or context['truncated']!=(context['totalItems']>listed):raise ValueError('candidate page count join')
    if context['truncated']:
        if listed!=100 or context.get('nextCursor')!=model.fit_cursor(project_id,run_id,100):raise ValueError('candidate page continuation join')
    elif 'nextCursor' in context:raise ValueError('unexpected candidate continuation')
    parity={'runId':run_id,'candidates':record['candidates'],'evidenceLevels':record['evidenceLevels'],
            'candidatesTruncated':context['truncated'],'candidatesTotalItems':context['totalItems'],
            'candidatesNextCursor':context.get('nextCursor'),'candidatesAvailability':'sealed-run-first-page'}
    if not canonical.equal_typed(parity,report['parity']):raise ValueError('candidate parity join')
    return summary


def interruption_owner():
    pins=json.loads((HERE/'workflow-input-pins.json').read_text())['files']
    values={}
    for name in ['ledger_join.py','command-inventory.v5.json']:
        row=next(r for r in pins if Path(r['path']).name==name);raw=Path(row['path']).read_bytes()
        assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
        values[name]=raw
    owner=types.ModuleType('pinned_interruption07_joins')
    exec(compile(values['ledger_join.py'],'pinned-interruption07-ledger-joins','exec'),owner.__dict__)
    return owner,json.loads(values['command-inventory.v5.json'])


def interrupted(record,selection,completed_handle,canonical,model,fit,availability,validate):
    validate('urn:opensip:product-v1:workflows:evaluator3:invocation:5',record)
    if selection['requestId']!=record['requestId'] or not canonical.equal_typed(selection['workflow'],record['workflow']):
        raise ValueError('selection invocation join')
    # Selection completeness and original custody remain an upstream host duty.
    envelope=model.interruption_envelope(record,True,record['projectId'],availability,selection)
    if 'clientCorrelationId' in record:envelope['clientCorrelationId']=record['clientCorrelationId']
    admit=lambda page,pid,rid:admit_page(page,pid,rid,canonical,model,validate)
    envelope=fit.project_interrupted(record,envelope,completed_handle,admit,canonical.equal_typed)
    validate(ENV,envelope)
    owner,inventory=interruption_owner()
    owner.validate_interruption_delivery(record,envelope,selection,inventory,availability)
    return envelope
