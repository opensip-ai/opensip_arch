
"""Claude follow-up probe: which query operations reach the availability route."""
import argparse,importlib.util,json,sys
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
schema=json.loads((a.source/'docs/coop/design-corrections/workflows/schemas/evaluator3/graph-query.schema.json').read_text())
ops=schema['$defs']['Operation']['enum']
graph_ops=schema['$defs']['GraphOperation']['enum']
rows=[]
for op in ops:
    req=dict(base); req['operation']=op
    try:
        resp=Q.execute_graph_query(req,run,objects,blobs,host=K.host_obs(availability='purged'))
        rows.append({'operation':op,'inGraphOperationEnum':op in graph_ops,'outcome':'returned','exitCode':0})
    except Q.QueryRefusal as e:
        env=e.envelope();term=env['termination']
        rows.append({'operation':op,'inGraphOperationEnum':op in graph_ops,'outcome':'refused',
                     'exitCode':env['exitCode'],'class':term['class'],'errorCode':term.get('errorCode'),
                     'domainDetail':(term.get('domainDetail') or {}).get('code')})
retained=[]
for op in ['graph.neighbors','finding.show']:
    req=dict(base); req['operation']=op
    try:
        resp=Q.execute_graph_query(req,run,objects,blobs,host=K.host_obs(availability='retained'))
        retained.append({'operation':op,'availability':'retained','outcome':'returned','items':len(resp['items'])})
    except Q.QueryRefusal as e:
        env=e.envelope()
        retained.append({'operation':op,'availability':'retained','outcome':'refused','exitCode':env['exitCode'],
                         'errorCode':env['termination'].get('errorCode'),'domainDetail':(env['termination'].get('domainDetail') or {}).get('code')})
out={'standing':'CLAUDE follow-up observation of frozen candidate25 behavior; no route selected',
     'graphOperationEnum':graph_ops,'purgedHost':rows,'retainedControl':retained}
a.out.write_text(json.dumps(out,indent=2)+chr(10))
n4=sum(1 for r in rows if r.get('exitCode')==4)
print('operations tested',len(rows),'exit4',n4,'exit2',sum(1 for r in rows if r.get("exitCode")==2))
