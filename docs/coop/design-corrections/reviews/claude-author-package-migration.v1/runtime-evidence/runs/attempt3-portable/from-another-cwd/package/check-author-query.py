"""Author graph-query checks over the separately admitted TypeScript export."""
from pathlib import Path
import importlib.util,json,copy
import argparse
p=argparse.ArgumentParser()
p.add_argument('--source',type=Path,required=True)
p.add_argument('--package',type=Path,required=True)
p.add_argument('--out',type=Path,required=True)
a=p.parse_args()
ROOT=a.package.resolve()
for source_root in (ROOT,a.source.resolve()):
 if a.out.resolve().is_relative_to(source_root):raise ValueError('Output must be outside frozen source/package trees')
if a.out.exists():raise ValueError('Use a fresh output path; prior evidence must be preserved')
D=a.source/'docs/coop/design-corrections'
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
T=load('author_transport',ROOT/'check-export.v4.py');K=load('author_query_helpers',D/'workflows/check-query-projection.v3.py');Q=K.Q;M=Q.identity3()
claim=json.loads((ROOT/'checkpoint3/claims.json').read_text())[0];objects,blobs=T.decode_store((ROOT/'checkpoint3/ts.store.json').read_bytes(),M);rid=claim['runId'];run=objects[rid][1]
proof=objects[objects[run['evidenceId']][1]['proofBundleId']][1]
invref=next(r for r in proof['evaluationInputRefs'] if r['domain']=='subject-inventory' and json.loads(blobs[r['digest']])['kind']=='symbol');inv=json.loads(blobs[invref['digest']]);spec=json.loads(blobs[objects[run['planId']][1]['analysisSpecDigest']]);en=next(json.loads(blobs[p['payloadDigest']]) for p in spec['parameters'] if 'cells' in json.loads(blobs[p['payloadDigest']]) if isinstance(json.loads(blobs[p['payloadDigest']]),dict))
uni=en['cells'][inv['cellOrdinal']]['programBindings'][inv['programOrdinal']]['universe'];endpoint=K.ep(uni,'symbol','symbol:src/index.ts::x')
base={'relation':'imports','minResolution':'resolved-target','direction':'outgoing'}
out=a.out;out.mkdir();rows=[]
for label,op,params,view,host in [
 ('neighbors','graph.neighbors',dict(base,endpoint=endpoint),{'runId':rid},K.host_obs()),
 ('incoming','graph.neighbors',dict(base,direction='incoming',endpoint=endpoint),{'runId':rid},K.host_obs()),
 ('reach','graph.reach',dict(base,start=endpoint,maxDepth=8),{'runId':rid},K.host_obs()),
 ('historical','graph.neighbors',dict(base,endpoint=endpoint),{'runId':rid},K.host_obs(latestRunId='run3:'+'a'*64)),
 ('bounded','graph.reach',dict(base,start=endpoint,maxDepth=8),{'runId':rid},K.host_obs(testBounds={'maxVisitedNodes':1,'maxItemsPerOperation':1})),
 ('wrong-run','graph.neighbors',dict(base,endpoint=endpoint),{'runId':'run3:'+'a'*64},K.host_obs()),
 ('purged','graph.neighbors',dict(base,endpoint=endpoint),{'runId':rid},K.host_obs(availability='purged')),
]:
 request=K.request(op,run['projectId'],view,params);row={'name':label,'request':request,'host':host}
 try:row['response']=Q.execute_graph_query(request,run,objects,blobs,host=host);row['result']='returned'
 except Q.QueryRefusal as e:row.update(result='refused',code=e.error_code,detail=e.detail,envelope=e.envelope())
 rows.append(row);(out/(label+'.json')).write_text(json.dumps(row,indent=2)+'\n')
(out/'observations.json').write_text(json.dumps(rows,indent=2)+'\n')
for row in rows:
 res=row.get('response',{});print(json.dumps({'name':row['name'],'result':row['result'],'code':row.get('code'),'detail':row.get('detail'),'items':res.get('items'),'context':res.get('context'),'termination':res.get('termination')}))
