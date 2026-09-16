"""Proposed joint mandatory report byte bounds, using the pinned owner's estimator.

Schema upper bounds are not evidence that a maximum-sized retained invocation is
codec-admissible (L01), nor a performance qualification. Source depth is separate.
"""
from pathlib import Path
import ast
import copy
import json
import math
import hashlib
import re
import types
HERE=Path(__file__).resolve().parent
PLANNING={'__file__':str(HERE/'planning_owner.py')}
exec(compile((HERE/'planning_owner.py').read_bytes(),str(HERE/'planning_owner.py'),'exec'),PLANNING)


def module(path,name):
    m=types.ModuleType(name);m.__file__=str(path)
    exec(compile(path.read_bytes(),str(path),'exec'),m.__dict__);return m

V=module(HERE/'check_model_carriers.py','carriers')
M=module(HERE/'models/report_model.py','model')
raw=V.read_unit('report-projection','build_owner.py')
names={'_resolve','_pattern_length','structural_max_bytes'}
nodes=[n for n in ast.parse(raw).body if isinstance(n,ast.FunctionDef) and n.name in names]
assert {n.name for n in nodes}==names
ns={'M':M,'re':re};exec(compile(ast.Module(body=nodes,type_ignores=[]),'pinned-report08-bound-estimator','exec'),ns)
bound=ns['structural_max_bytes']
report=copy.deepcopy(V.report);docs=copy.deepcopy(V.schemas);rid=report['$id']
planning=PLANNING['read']()


def maximum(node):
    result=bound(docs,rid,node)
    if type(result) is not int:raise ValueError('No finite structural bound: '+str(node)[:150])
    return result


def derive():
    budget=report['$defs']['BudgetProfileV1']['properties']
    # Conservative digit width breaks the budget's self-reference. All three
    # derived sizes must fit these Uint53 values before any source is emitted.
    for k in ['documentMaxBytes','rootMemberMaxBytes','ledgerMaxBytes']:
        budget[k]={'type':'integer','minimum':0,'maximum':9007199254740991}
    docs[rid]=report
    ledger=copy.deepcopy(report['$defs']['InvocationLedgerV1'])
    recorded=copy.deepcopy(report['$defs']['LedgerStepV1'])
    unrecorded=copy.deepcopy(recorded)
    unrecorded['properties']={k:v for k,v in unrecorded['properties'].items() if k in unrecorded['required']}
    unrecorded['properties']['recorded']={'const':False}
    unrecorded['properties']['attemptServiceTime']={'type':'object','additionalProperties':False,'properties':{
        'state':{'const':'not-finalized'},'reason':{'enum':['render-in-progress','step-result-not-recorded']}}}
    unrecorded.pop('allOf',None)
    recorded_size=maximum(recorded);unrecorded_size=maximum(unrecorded)
    per_command={}
    for command,variants in planning['commands'].items():
        bounds=[]
        for variant in variants:
            if variant['status']!='plannable':continue
            steps=variant['steps'];at=next(i for i,s in enumerate(steps) if s['kind']=='render')
            shape=copy.deepcopy(ledger)
            # At projection, only steps before this required render are recorded.
            shape['properties']['steps']={'const':[]}
            shape['properties']['missingChildren']['maxItems']=len(steps)
            size=maximum(shape)+(at*recorded_size+(len(steps)-at)*unrecorded_size)+max(len(steps)-1,0)
            bounds.append({'variant':variant['variant'],'recordedBeforeRender':at,'unrecordedFromRender':len(steps)-at,'ledgerMaxBytes':size})
        per_command[command]={'variants':bounds,'ledgerMaxBytes':max(v['ledgerMaxBytes'] for v in bounds)}
    root={}
    for key,node in report['properties'].items():
        if key in ['envelope','invocationLedger','panels']:continue
        candidates=[node]
        # Constraints common to every command: take maximum of each command's
        # constrained upper bound, never select just the smallest command.
        conditions=[c['then']['properties'].get(key) for c in report['allOf'] if c.get('if',{}).get('properties',{}).get('command',{}).get('const')]
        command_bounds=[bound(docs,rid,{'allOf':[node,c]}) for c in conditions if c is not None]
        value=bound(docs,rid,node)
        if len(command_bounds)==len(planning['commands']):value=min(value,max(command_bounds))
        if type(value) is not int:raise ValueError('Unbounded mandatory root '+key)
        root[key]=value
    ledger_max=max(c['ledgerMaxBytes'] for c in per_command.values())
    overhead=2+sum(len(M.canonical(k))+1 for k in report['properties'])+len(report['properties'])-1
    envelope=budget['envelopeMaxCanonicalBytes']['const'];exploration=budget['explorationMaxCanonicalBytes']['const']
    total=overhead+envelope+ledger_max+exploration+sum(root.values())
    assert all(v<=9007199254740991 for v in [total,ledger_max,sum(root.values())])
    return {'standing':'Proposed mandatory structural bounds only; no source selection, depth/profile/product/Claude qualification',
      'inputReportSha256':hashlib.sha256((HERE/'composed-sources/report-projection.proposed.schema.json').read_bytes()).hexdigest(),
      'recordedStepMaxBytes':recorded_size,'unrecordedStepMaxBytes':unrecorded_size,'perCommand':per_command,
      'rootKeyOverheadBytes':overhead,'rootMemberMaxBytes':root,'ledgerMaxBytes':ledger_max,'envelopeMaxCanonicalBytes':envelope,
      'explorationMaxCanonicalBytes':exploration,'documentMaxBytes':total,
      'formula':'root-key overhead + complete envelope cap + max per-command ledger + one shared exploration cap + other mandatory roots',
      'limitations':['L01 retained invocation codec capacity remains an owner decision','Depth and actual producer/consumer execution remain pending','L02 complete envelope representability/final output policy remains unaccepted','Finalized ledger is not a report-at-render ledger; these bounds apply only to the latter']}

if __name__=='__main__':
    result=derive();(HERE/'joint-budget-derivation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
