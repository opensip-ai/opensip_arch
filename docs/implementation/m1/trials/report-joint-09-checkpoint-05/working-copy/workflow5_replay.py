"""Proposed invocation5 reference replay, not a live host/supervisor or store."""
from pathlib import Path
import ast
import copy
import hashlib
import json
import types

HERE=Path(__file__).resolve().parent


def owned_core(canonical):
    pins=json.loads((HERE/'workflow-input-pins.json').read_text())['files']
    values={}
    for row in pins:
        raw=Path(row['path']).read_bytes()
        assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
        values[Path(row['path']).name]=raw
    change=json.loads(values['model-successor.json'])
    raw=values['workflows_model.v1.py']
    assert hashlib.sha256(raw).hexdigest()==change['ownerSha256']
    source=raw.decode();assert source.count(change['before'])==1
    source=source.replace(change['before'],change['after'])
    wanted={'Refusal','terminate','dd','analysis_termination','comparison_termination','exit_code','validate_dag',
            'raw_sha','synthetic_execution_id','_exec_id','run_invocation'}
    nodes=[]
    for n in ast.parse(source).body:
        if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name in wanted:nodes.append(n)
        elif isinstance(n,ast.Assign):
            names={t.id for t in n.targets if isinstance(t,ast.Name)}
            if names & wanted or (names and all(k.isupper() for k in names) and not any(isinstance(x,ast.Call) for x in ast.walk(n.value))):nodes.append(n)
    module=types.ModuleType('joint_workflow_core')
    module.__dict__.update(hashlib=hashlib,json=json,canonical=canonical)
    exec(compile(ast.Module(body=nodes,type_ignores=[]),'pinned-workflow-owner#interruption07-successor','exec'),module.__dict__)
    native=[n for n in ast.parse(values['native_evidence_model.v2.py']).body
            if isinstance(n,ast.FunctionDef) and n.name in ('release_absence_notices','invocation_availability')
            or isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='PUBLIC_ROUTE_REMEDIES' for t in n.targets)]
    assert len(native)==3
    availability={};exec(compile(ast.Module(body=native,type_ignores=[]),'pinned-native-availability-projection','exec'),availability)
    return module,availability['invocation_availability']


def admit_fit_source_plan(base,validate):
    # The original DAG owner remains responsible for all ordinary dependency
    # and retry laws; these are the new sourceStep joins only.
    if base['workflow']=={'kind':'builtin','name':'fit'}:
        queries=[s for s in base['orderedSteps'] if s['kind']=='query']
        if len(queries)!=1:raise ValueError('fit requires exactly one source-bound query')
        validate('step-params',queries[0]['params'])
    for step in base['orderedSteps']:
        if step['kind']!='query' or 'sourceStep' not in step['params']:continue
        validate('step-params',step['params'])
        if base['workflow']!={'kind':'builtin','name':'fit'}:
            raise ValueError('fit source binding belongs only to the selected fit builtin')
        sid=step['params']['sourceStep']
        source=[s for s in base['orderedSteps'] if s['stepId']==sid and s['kind']=='analysis']
        if type(sid) is not int or len(source)!=1 or sid>=step['stepId'] or sid not in step['dependsOn'] or step['dependencyGate']!='completed':
            raise ValueError('invalid fit analysis source dependency')


def replay(base,script,canonical,timing,validate):
    """Use synthetic terminal domain observations as the unchanged owner does.

    Timing observations are private test inputs. Missing samples mean unavailable,
    not a measured zero. This routine has no journal, clock, subprocess or Run
    publisher. Validation after pure computation is not a durable transaction.
    """
    if base.get('schemaMajor')!=5:
        raise ValueError('invocation5 planning input required')
    validate('planned-steps',base['orderedSteps'])
    admit_fit_source_plan(base,validate)
    core,project_availability=owned_core(canonical)
    record,code=core.run_invocation(copy.deepcopy(base),copy.deepcopy(script))
    for result in record['stepResults']:
        observations=script.get(str(result['stepId']),[])
        for index,attempt in enumerate(result['attempts']):
            observation=observations[index] if index<len(observations) else {}
            clocks=observation.get('clockSamples',{'startNs':None,'endNs':None})
            if type(clocks) is not dict or set(clocks)!={'startNs','endNs'}:
                raise ValueError('closed private clock observation required')
            attempt['observedDuration']=timing.observe_terminal(attempt['outcome'],clocks['startNs'],clocks['endNs'])
    validate('invocation',record)
    return record,code,project_availability


def ledger(record,plan_roles,plan_variant,timing,report_model,ledger_schema):
    """Finalized record to report ledger; no claim this is an in-progress render ledger."""
    steps=[]
    for spec,result in zip(record['orderedSteps'],record['stepResults']):
        row={k:copy.deepcopy(spec[k]) for k in ['stepId','kind','requirement','dependsOn','dependencyGate']}
        row.update(planRole=plan_roles[spec['stepId']],recorded=True,outcome=result['outcome'],termination=copy.deepcopy(result['termination']))
        for key in ['skipReason']:
            if key in result:row[key]=result[key]
        attempts=[]
        for attempt in result['attempts']:
            projection=timing.project_attempt(record['schemaMajor'],attempt)
            for key in ['faultCause','retried']:
                if key in attempt:projection[key]=attempt[key]
            attempts.append(projection)
        row['attempts']=attempts
        row['attemptServiceTime']=timing.summarize_attempts([{k:v for k,v in a.items() if k not in ['faultCause','retried']} for a in attempts])
        if result.get('result',{}).get('runId'):row['analysisRunId']=result['result']['runId']
        steps.append(row)
    out={k:copy.deepcopy(record[k]) for k in ['requestId','workflow','mode']}
    out['steps']=steps
    out['cancellation']=copy.deepcopy(record['cancellation']) if record.get('cancellation',{}).get('requested') else {'requested':False,'phase':'none'}
    out['planVariant']=plan_variant
    out['missingChildren']=report_model.missing_children(steps)
    out['provenance']=copy.deepcopy(ledger_schema['properties']['provenance']['const'])
    return out
