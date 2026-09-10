"""Fresh public query boundary observations from an exact author-admitted Run."""
import argparse,importlib.util,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--package',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
def load(n,path):
 s=importlib.util.spec_from_file_location(n,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
T=load('audit_transport',a.package/'check-export.v4.py');K=load('audit_query',a.source/'docs/coop/design-corrections/workflows/check-query-projection.v3.py');Q=K.Q;M=Q.identity3()
claim=json.loads((a.package/'checkpoint3/claims.json').read_text())[0];objects,blobs=T.decode_store((a.package/'checkpoint3/ts.store.json').read_bytes(),M);run=objects[claim['runId']][1]
request=json.loads((a.package/'query-checks1/purged.json').read_text())['request'];rows=[]
for availability in ['retained','purged','expired','corrupt','unavailable']:
 try:
  response=Q.execute_graph_query(request,run,objects,blobs,host=K.host_obs(availability=availability));rows.append({'availability':availability,'outcome':'returned','termination':response['termination'],'itemCount':len(response['items'])})
 except Q.QueryRefusal as e:rows.append({'availability':availability,'outcome':'refused','envelope':e.envelope()})
assert rows[0]['outcome']=='returned'
assert all(r['envelope']['exitCode']==4 for r in rows[1:])
a.out.write_text(json.dumps({'standing':'AUTHOR observation of candidate25 behavior, not selection of a new public route','source':str(a.source),'runId':claim['runId'],'observations':rows},indent=2)+'\n');print('Retained control returned; four known unavailable states consistently returned exit 4.')
