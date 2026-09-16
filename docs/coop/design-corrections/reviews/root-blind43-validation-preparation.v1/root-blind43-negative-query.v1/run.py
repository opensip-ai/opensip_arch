from pathlib import Path
import json,hashlib,copy,importlib.util,base64,shutil
B=Path('/tmp/opensip-design-corrections'); O=Path(__file__).parent; S=B/'candidate-subject.v43'; C=B/'consumer-b.v24-source43.v1/output'; L=Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews')
h=lambda raw:hashlib.sha256(raw).hexdigest()
def load(name,p):
 sp=importlib.util.spec_from_file_location(name,p); m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
mf=(L/'candidate-subject.v43.json').read_bytes();assert h(mf)=='db43ee76f91b08dc5076d152761ddef795a3645fafa690a3974d693bedaf897d'
for row in json.loads(mf)['files']:
 raw=(S/row['path']).read_bytes();assert len(raw)==row['bytes'] and h(raw)==row['sha256']
t=B/'root-blind39-transport-preparation.v1/check-export.py';assert h(t.read_bytes())=='6fa376bb59548bd9d52dbc52a3a35f27e0d12e4a963a6730624467c3a8f63074'
R=load('root_negative_transport42',t);Q=load('root_negative_query42',S/'docs/coop/design-corrections/workflows/query_projection_model.v3.py');M=Q.identity3()
raw=(C/'runs/cmp-code.store.json').read_bytes();vraw=(C/'vectors/graph-query.json').read_bytes();store=R.parse(raw);vectors=R.parse(vraw);objects,blobs,_=R.decode(raw,M);rid=vectors['runs']['cmp-code'];run=objects[rid][1];assert M.close_run(run,objects,blobs)==rid
victims=[k for k,v in store['blobLabels'].items() if v=='fact-payload:calls'];assert len(victims)>0;victim=victims[0];assert victim in blobs
rows=[]
for label,change in [('cmp-code~missing-bytes','delete'),('cmp-code~corrupt-bytes','xor-first-byte-1')]:
 cases=[x for x in vectors['vectors'] if x['run']==label];assert len(cases)==1;v=cases[0];mb=copy.deepcopy(blobs);mut=copy.deepcopy(store)
 if change=='delete':del mb[victim];del mut['blobs'][victim]
 else:
  b=bytearray(mb[victim]);b[0]^=1;mb[victim]=bytes(b);mut['blobs'][victim]=base64.b64encode(bytes(b)).decode()
 (O/(label+'.store.json')).write_text(json.dumps(mut,indent=2)+'\n')
 row={'vector':v['vector'],'runLabel':label,'baseFullRunAdmission':'ADMIT','mutation':change,'victim':victim,'request':v['request'],'hostObservations':v['hostObservations'],'consumerFailureEnvelope':v['failureEnvelope'],'standing':'Negative retained-byte mutation; never claimed an admitted Run or successful graph. Exact base objects retained; only declared blob mutation applied.'}
 try:R.decode(json.dumps(mut).encode(),M);row['mutatedTransport']='ADMIT'
 except Exception as e:row.update(mutatedTransport='REFUSE',transportException=type(e).__name__,transportReason=str(e))
 try:
  row['ownerResponse']=Q.execute_graph_query(copy.deepcopy(v['request']),copy.deepcopy(run),copy.deepcopy(objects),mb,host=copy.deepcopy(v['hostObservations']));row['ownerOutcome']='UNEXPECTED_RETURNED'
 except Q.QueryRefusal as e:row.update(ownerOutcome='REFUSED',ownerFailureEnvelope=e.envelope(host=copy.deepcopy(v['hostObservations'])))
 except Exception as e:row.update(ownerOutcome='UNEXPECTED_EXCEPTION',exceptionType=type(e).__name__,reason=str(e))
 rows.append(row)
assert h((C/'runs/cmp-code.store.json').read_bytes())==h(raw) and h((C/'vectors/graph-query.json').read_bytes())==h(vraw)
d={'standing':'Actual negative strong-query boundary measurements; not positive closure or whole charter assent. Mutated transport refusal and direct declared byte-loss/corruption call are separate boundaries. No repaired input or cursor translation.','sourceManifestSha256':h(mf),'exportSha256':h(raw),'vectorsSha256':h(vraw),'rows':rows,'rootBlindAssent':False}
(O/'report.json').write_text(json.dumps(d,indent=2)+'\n');shutil.copytree(O,L/O.name);print(json.dumps([{'vector':r['vector'],'outcome':r['ownerOutcome'],'transport':r['mutatedTransport'],'termination':r.get('ownerFailureEnvelope',{}).get('termination')} for r in rows],indent=2))
