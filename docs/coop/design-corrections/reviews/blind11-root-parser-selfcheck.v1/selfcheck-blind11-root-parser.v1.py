"""Parser selfcheck only, author fixture never supplied to blind consumer."""
from pathlib import Path
import importlib.util,hashlib,json,base64,copy,subprocess
base=Path('/tmp/opensip-design-corrections');out=base/'blind11-root-parser-selfcheck.v1';out.mkdir(exist_ok=False);inp=out/'input';inp.mkdir();source=base/'candidate-subject.v24';f=source/'docs/coop/design-corrections/foundation'
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
S=load('root_parser_fixture',f/'evaluator_semantic_fixture.v3.py');R=load('root_parser_positive',f/'check-semantic-replay.v3.py');M=R.M
atom={'op':'none','relation':'references','minResolution':'resolved-binding','endpoint':'target','filters':[]};g=S.build_ts_semantic_graph(atom=atom,has_declares=False,has_references_fact=True,incoming_search=True,target_sidecar=True)
run,objects,blobs,actual=R.close_positive(g);rid=actual['runId'];objects=dict(objects);objects[rid]=('run',run);blobs=dict(blobs);table={}
for key,(domain,desc) in objects.items():
 body=M.C.canonical(desc);frame=b'opensip.product.v1\0'+domain.encode('ascii')+b'\0'+len(body).to_bytes(8,'big')+body;d=hashlib.sha256(frame).hexdigest();assert M.identifier(domain,desc)==key;blobs[d]=frame;table[key]={'id':key,'domain':domain,'descriptor':desc,'digest':d}
store={'objectTable':table,'blobs':{k:base64.b64encode(v).decode('ascii') for k,v in blobs.items()},'objectCount':len(table),'blobCount':len(blobs)};(inp/'positive.json').write_text(json.dumps(store,indent=2)+'\n')
mut=copy.deepcopy(store);mut['objectTable'][rid]['descriptor']['schemaVersion']=2;(inp/'table-mismatch.json').write_text(json.dumps(mut,indent=2)+'\n')
results=[]
for name,expected in [('positive',True),('table-mismatch',False)]:
 claims=out/(name+'-claims.json');claims.write_text(json.dumps([{'name':name,'path':name+'.json','runId':rid}])+'\n');dest=out/(name+'-result');command=['/tmp/opensip-architecture-review-env/bin/python','-I','-B',str(base/'check-blind11-exported-graphs.v1.py'),'--source',str(source),'--input',str(inp),'--claims',str(claims),'--out',str(dest)];r=subprocess.run(command,capture_output=True,text=True);(out/(name+'.log')).write_text(r.stdout+r.stderr);report=json.loads((dest/'report.json').read_text());assert report['passed']==expected and (r.returncode==0)==expected;results.append({'case':name,'expectedPass':expected,'actualPass':report['passed'],'check':report['checks'][0]})
summary={'standing':'Root parser selfcheck on an author reference fixture and mismatched table, not blind consumer evidence. No inputs or outcomes supplied to blind11.','passed':True,'results':results};(out/'assessment.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
