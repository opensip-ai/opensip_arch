"""Replay the disclosed correspondence collision through full Run admission and comparison.

This measures owner behavior, not independent-consumer conformance. R2 property-name
inventory is deliberately not reproduced: nested owned carriers require actual admission.
"""
from pathlib import Path
import argparse, hashlib, importlib.util, json, sys
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
S=a.source.resolve();O=a.out.resolve();O.mkdir(parents=True,exist_ok=False);D=S/'docs/coop/design-corrections'
sys.path.insert(0,str(D/'foundation'))
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
P=load('root_collision_projection',D/'workflows/workflow_projection_model.v3.py')
RC=load('root_collision_replay',D/'foundation/check-replay.v3.py')
M=RC.M
def host(run_id,objects):
    closures={};majors=set();platform=None
    for key,(domain,value) in objects.items():
        if domain!='closure':continue
        closures[key]={'bytes':'ok','trust':'admitted','protocolMajor':value['protocolMajor'],'platform':value['platform']}
        majors.add(value['protocolMajor'])
        if value['kind']=='evaluator':platform=value['platform']
        elif platform is None and value['kind']=='detector' and value['platform']!='any':platform=value['platform']
    return {'closures':closures,'protocolMajors':sorted(majors),'platform':platform or 'linux','pivotRunId':run_id,'recipeMajors':[2]}
scope={'schemaFamily':'opensip.product.scope','schemaMajor':1,'include':['**'],'exclude':[]}
custody={'exportedAtUtc':'2026-09-08T00:00:00Z','exportedByHostRelease':'1.0.0'}
x1={'nativeSubjectId':'symbol:x1'}
x2={'nativeSubjectId':'symbol:x2','signatureTokens':['function','x','(','number',')']}
x3={'nativeSubjectId':'symbol:x3'}
rows=[]
for gate in [True,False]:
    base=RC.positive(symbol_rows=[x1,x2],scope_document=scope,gate=gate)
    cur=RC.positive(symbol_rows=[x1,x2,x3],scope_document=scope,gate=gate)
    base_id=M.close_run(*base);cur_id=M.close_run(*cur)
    baseline=P.adopt_admitted_baseline_v3(*base,custody)
    view=P.project_admitted_run_v3(*cur)
    result=P.compare_admitted_v3(baseline_artifact=baseline,current_run=cur[0],current_objects=cur[1],current_blobs=cur[2],host=host(base_id,base[1]),profile_name='code-regression')
    name='gating' if gate else 'nongating'
    (O/(name+'.comparison.json')).write_text(json.dumps(result,indent=2)+'\n')
    rows.append({'gate':gate,'baselineRunId':base_id,'currentRunId':cur_id,'bothFullReplayAdmitted':True,
                 'enumeration':view['ruleResults'][0]['enumeration']['state'],
                 'unmatched':[{'subject':o['finding']['subject'],'correspondence':o['finding']['correspondence']} for o in view['occurrences'] if not o['finding']['fingerprint']],
                 'entries':result['descriptor']['entries'],'verdict':result['descriptor']['verdict'],
                 'ruleDeficiencies':result['descriptor']['ruleDeficiencies']})
paths=['foundation/check-replay.v3.py','foundation/identity-model.v3.py','foundation/evaluator_graph_fixture.v3.py','workflows/workflow_projection_model.v3.py']
report={'standing':'Root reproduction of actual author-disclosed signature collision through full Run admission and public comparison owner. Capture only; exit0 is not acceptance.','source':str(S),
        'inputHashes':{p:hashlib.sha256((D/p).read_bytes()).hexdigest() for p in paths},'cases':rows}
(O/'report.json').write_text(json.dumps(report,indent=2)+'\n')
for row in rows:print(row['gate'],row['bothFullReplayAdmitted'],[(e['classification'],e.get('indeterminateReason')) for e in row['entries']],row['verdict'])
