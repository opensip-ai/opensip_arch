"""Root transport-adapter controls using already admitted author fixture, never blind input."""
from pathlib import Path
import base64,copy,hashlib,json,subprocess
b=Path('/tmp/opensip-design-corrections');out=b/'blind12-root-parser-selfcheck.v1';assert not out.exists();out.mkdir();inp=out/'input';inp.mkdir()
old=json.loads((b/'blind11-root-parser-selfcheck.v1/input/positive.json').read_text());blobs=old['blobs'];table={d:{'kind':'raw-artifact','label':'root-known-control','bytes':len(base64.b64decode(raw))} for d,raw in blobs.items()}
for key,obj in old['objectTable'].items():
 d=obj['digest'];typed=key if not key.startswith('sha256:') else None
 meta={'kind':'h-identity','domain':obj['domain'],'digest':d,'typedId':typed,'sha256Text':'sha256:'+d,'label':'root-known-control','bytes':len(base64.b64decode(blobs[d]))};table[d]=meta
 if typed:table[typed]=meta
store={'objectTable':table,'blobs':blobs,'blobCount':len(blobs)};rid=next(k for k in table if k.startswith('run3:'));rows=[]
for case in ['positive','wrong-typed-metadata','missing-required-schema']:
 x=copy.deepcopy(store)
 if case=='wrong-typed-metadata':
  d=rid.split(':')[1];x['objectTable'][d]['typedId']='run3:'+'0'*64
 elif case=='missing-required-schema':
  d='a87331bca7545468a266d74776d785a9903f93563220ac7f6267b6d749b82257';assert d in x['blobs'];del x['blobs'][d];del x['objectTable'][d];x['blobCount']=len(x['blobs'])
 path=inp/(case+'.json');path.write_text(json.dumps(x,indent=2)+'\n');claims=out/(case+'.claims.json');claims.write_text(json.dumps([{'name':case,'path':path.name,'runId':rid}])+'\n')
 r=subprocess.run(['/tmp/opensip-architecture-review-env/bin/python','-I','-B',str(b/'check-blind12-exported-graphs.v1.py'),'--input',str(inp),'--claims',str(claims),'--source',str(b/'candidate-subject.v24'),'--out',str(out/(case+'.result'))],capture_output=True,text=True);(out/(case+'.log')).write_text(r.stdout+r.stderr);report=json.loads((out/(case+'.result/report.json')).read_text());row=report['checks'][0]
 expected=(row['ownerAdmission']=='ADMIT' and row['semanticAdmission']=='ADMIT') if case=='positive' else (not row['passed'])
 if case=='missing-required-schema':expected=expected and row['ownerAdmission']=='REFUSE' and row['reason']=='EVIDENCE_UNAVAILABLE:'+d
 rows.append({'case':case,'exitCode':r.returncode,'ownerAdmission':row['ownerAdmission'],'semanticAdmission':row['semanticAdmission'],'reason':row.get('reason'),'passed':expected})
result={'standing':'Parser controls only on known author fixture transformed to transport format; never provided to blind12 or claimed as blind reconstruction. No repair of actual consumer outputs.','checks':rows,'passed':all(r['passed'] for r in rows)};(out/'assessment.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));raise SystemExit(not result['passed'])
