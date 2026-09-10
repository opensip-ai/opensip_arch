"""Author closed successor bootstrap vectors; no security dependency mutation."""
import base64,copy,json
from pathlib import Path
P=Path(__file__).resolve().parent
rows=[]
def encoded(v):return base64.urlsafe_b64encode(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).rstrip(b'=').decode()
def add(id,value,accept=False):rows.append({'id':id,'encoded':encoded(value),'expected':'ACCEPT' if accept else 'STARTUP-FAILURE'})
root='/host-owned-operational-root/spawn/fixture/results'
handle={'effectClass':'HE-2','operationRef':'op-'+'2'*32,'authorizationRef':'ah:'+'1'*32,'commitClass':'REVERSIBLE'}
base={'bootstrapVersion':1,'handles':[handle],'resultScratchRoot':root}
add('shipped-empty',{'bootstrapVersion':1,'handles':[]},True);add('read-handle',base,True)
v=copy.deepcopy(base);v['handles'][0].update(effectClass='HE-1',commitClass='IRREVERSIBLE');add('write-irreversible',v,True)
v=copy.deepcopy(base);v['handles'][0]['effectClass']='HE-1';add('write-reversible',v,True)
v=copy.deepcopy(base);v['handles'].append({**handle,'authorizationRef':'ah:'+'3'*32});add('same-operation-two-grants',v,True)
for field in ['effectClass','operationRef','authorizationRef','commitClass']:
 v=copy.deepcopy(base);v['handles'][0].pop(field);add('missing-handle-'+field,v)
v=copy.deepcopy(base);v.pop('resultScratchRoot');add('missing-root-for-handles',v)
add('root-for-empty',{'bootstrapVersion':1,'handles':[],'resultScratchRoot':root})
for value,label in [('relative/path','relative'),('/','filesystem-root'),('/tmp/../results','dotdot'),('/tmp/./results','dot'),('/tmp//results','empty-segment'),('/tmp/results/','trailing-slash'),('/tmp/\x00/results','nul'),(False,'wrong-type'),('/'+'é'*2047+'a','utf8-exact-4096'),('/'+'é'*2048,'utf8-over-4096')]:
 v=copy.deepcopy(base);v['resultScratchRoot']=value;add('scratch-'+label,v,label=='utf8-exact-4096')
for key,val,label in [('effectClass','HE-3','effect-enum'),('commitClass','IRREVERSIBLE','read-irreversible'),('commitClass','REVERSIBLE\n','commit-newline'),('authorizationRef','ah:'+'A'*32,'upper-auth'),('operationRef','op-'+'2'*32+'\n','op-newline')]:
 v=copy.deepcopy(base);v['handles'][0][key]=val;add(label,v)
v=copy.deepcopy(base);v['handles'][0]['target']='/forbidden';add('unknown-entry-member',v)
v=copy.deepcopy(base);v['unknown']=1;add('unknown-top-member',v)
v=copy.deepcopy(base);v['handles']=[{**handle,'authorizationRef':'ah:'+str(i)*32} for i in range(4)];add('four-distinct-grants',v,True)
v['handles'].append({**handle,'authorizationRef':'ah:'+'4'*32});add('fifth-grant',v)
v=copy.deepcopy(base);v['handles']=[handle,handle];add('duplicate-grant',v)
# Old malformed encoded-byte probes retain exact bytes. Legacy valid nonempty
# shapes are explicitly refused by the new required metadata, not rewritten.
legacy=json.loads((P/'broker-bootstrap.cases.v1.json').read_text())['cases']
for c in legacy:
 if c['expected']=='STARTUP-FAILURE':rows.append({**c,'id':'retained-byte-negative/'+c['id']})
 elif c['id'] in ['empty-shipped-typescript','decoded-exact-12288','json-whitespace-member-order']:rows.append({**c,'id':'retained-empty-positive/'+c['id']})
 else:rows.append({**c,'id':'legacy-nonempty-needs-successor/'+c['id'],'expected':'STARTUP-FAILURE'})
(P/'broker-bootstrap-cases.v3.json').write_text(json.dumps({'standing':'PROPOSED-SUCCESSOR-DESIGN-EVIDENCE','cases':rows},sort_keys=True,indent=2)+'\n')
