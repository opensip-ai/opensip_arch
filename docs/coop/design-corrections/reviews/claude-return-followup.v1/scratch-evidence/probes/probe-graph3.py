
import argparse,importlib.util,json,sys,copy
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--package',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
def load(n,path):
    s=importlib.util.spec_from_file_location(n,path);m=importlib.util.module_from_spec(s);sys.modules[n]=m;s.loader.exec_module(m);return m
T=load('audit_transport',a.package/'check-export.v4.py')
K=load('audit_query',a.source/'docs/coop/design-corrections/workflows/check-query-projection.v3.py')
Q=K.Q;M=Q.identity3()
claim=json.loads((a.package/'checkpoint3/claims.json').read_text())[0]
objects,blobs=T.decode_store((a.package/'checkpoint3/ts.store.json').read_bytes(),M)
run=objects[claim['runId']][1]
base=json.loads((a.package/'query-checks1/purged.json').read_text())['request']
ep=base['params']['endpoint']
reqs={}
reqs['graph.neighbors']=copy.deepcopy(base['params'])
reqs['graph.path']={'relation':'imports','minResolution':'resolved-target','direction':'outgoing','start':ep,'target':ep,'maxDepth':4}
reqs['graph.reach']={'relation':'imports','minResolution':'resolved-target','direction':'outgoing','start':ep,'maxDepth':4}
rows=[]
for op,params in reqs.items():
    for avail in ['retained','purged','expired','corrupt','unavailable']:
        r=dict(base); r['operation']=op; r['params']=params
        try:
            resp=Q.execute_graph_query(r,run,objects,blobs,host=K.host_obs(availability=avail))
            rows.append({'operation':op,'availability':avail,'outcome':'returned','class':resp['termination']['class']})
        except Q.QueryRefusal as e:
            env=e.envelope();t=env['termination']
            rows.append({'operation':op,'availability':avail,'outcome':'refused','exitCode':env['exitCode'],'class':t['class'],'errorCode':t.get('errorCode'),'domainDetail':(t.get('domainDetail') or {}).get('code')})
a.out.write_text(json.dumps({'standing':'CLAUDE follow-up; frozen candidate25 observation','rows':rows},indent=2)+chr(10))
print('rows',len(rows))
