#!/usr/bin/env python3
"""Replay concrete conditional G15 joins; no OS qualification or shipping act."""
import argparse,copy,hashlib,importlib.util,json,subprocess,tempfile
from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parents[2]
s=importlib.util.spec_from_file_location('g15_check_model',P/'compatibility-selection-model.v5.py');M=importlib.util.module_from_spec(s);s.loader.exec_module(M)
def load(n):return json.loads((P/n).read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def stored(v):return (json.dumps(v,indent=2,ensure_ascii=False)+'\n').encode()
def mutate_doc(bundle,key,fn):
 value=json.loads(bytes.fromhex(bundle['documents'][key]));fn(value);bundle['documents'][key]=stored(value).hex();return value

def run(args):
 bundle=load('g15-conditional-bundle.v1.json');host=load('g15-conditional-host.v1.json');corpus=load('g15-conditional-cases.v2.json');goldens=load('g15-conditional-goldens.v1.json');variants=load('g15-conditional-variants.v1.json');matrix=load('g15-conditional-matrix.v2.json');results=[]
 def check(cid,observed,expected):results.append({'id':cid,'passed':observed==expected,'observed':observed,'expected':expected})
 for path,digest in corpus['sourcePins'].items():check('source/'+path,sha((ROOT/path).read_bytes()),digest)
 # Independently replay the retained v3 core's149 comparison/closure/sorting
 # regressions. Their observations are not relabelled signed catalog inputs.
 with tempfile.TemporaryDirectory() as td:
  report=Path(td)/'core.json';proc=subprocess.run([args.python,str(P/'compatibility-selection-model.v3.py'),'--report',str(report)],capture_output=True,text=True)
  check('selection-core/replay-exit',proc.returncode,0)
  if proc.returncode==0:
   legacy=json.loads(report.read_text());check('selection-core/149-retained', [legacy['passed'],legacy['total']],[149,149]);check('selection-core/retained-report-bytes',report.read_bytes()==(P/'compatibility-selection-report.v3.json').read_bytes(),True)
 before=sha(stored(bundle));frames=[]
 for case in corpus['cases']:
  x=case['resolutionInputs'];result=M.solve(bundle,x,host);check(case['id']+'/verified-selection',result.get('status'),'ACCEPT')
  if result['status']!='ACCEPT':continue
  check(case['id']+'/golden-lock',result,goldens[case['golden']])
  check(case['id']+'/two-components',len(result['resolved']),2)
  prior=case['environment']['priorSelection']
  if case['environment']['state']=='upgrade':
   previous=M.solve(load('g15-conditional-prior-bundle.v1.json'),prior['resolutionInputs'],load('g15-conditional-prior-host.v1.json'))
   check(case['id']+'/prior-verified',previous.get('status'),'ACCEPT')
   check(case['id']+'/prior-bytes',previous.get('lockBytesHex'),prior['lockBytesHex'])
   check(case['id']+'/prior-distinct',prior['lockPreimageSha256']!=result['lockPreimageSha256'],True)
   check(case['id']+'/prior-version',sorted(r['version'] for r in previous['resolved']),['0.9.0','1.0.0'])
  else:check(case['id']+'/no-prior',prior,None)
  cls=case['class'];lock=result['referenceLock'];raw=bytes.fromhex(result['lockBytesHex'])
  if cls=='TC-ACCEPT.5':observed=result['status']
  elif cls=='TC-SIG.C-LOCK':
   changed=copy.deepcopy(bundle);bad=variants['corruptedArtifact'];changed['artifacts'][bad['stableId']][bad['artifact']]=bad['bytesHex'];check(case['id']+'/positive-bytes',M.verify_lock_artifacts(lock,bundle),'ACCEPT');observed=M.verify_lock_artifacts(lock,changed)
  elif cls=='TC-SIG.C-ENVELOPE':
   bad=json.loads(bytes.fromhex(variants['wrongManifestPreimageEnvelopeHex']));sid=variants['corruptedArtifact']['stableId'];original=bytes.fromhex(bundle['documents']['manifest/'+sid]);root=json.loads(bytes.fromhex(bundle['documents']['root']));observed=M.SEC.verify_envelope(original,bad,root,'manifest','opensip')[0]
   authorized=M.SEC.root_keys_for_role(root,'TR-COMPONENT','opensip');count=sum(M.SEC.ed25519_verify(authorized[s['keyId']],M.SEC.envelope_message_hex(bad),s['signature']) for s in bad['signatures']);check(case['id']+'/wrong-preimage-is-signed',count,2)
  elif cls=='TC-BYTE-EXACT.C-CANON':
   good=True
   for sid,expected in variants['canonicalManifests'].items():
    value=json.loads(bytes.fromhex(bundle['documents']['manifest/'+sid]));canonical=M.SEC.canonical_bytes(value);independent=json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
    good=good and canonical.hex()==expected and canonical==independent
    envelope=json.loads(bytes.fromhex(bundle['documents']['manifest/'+sid+'.envelope']));check(case['id']+'/domain-preimage/'+sid,sha(b'opensip.metadata.manifest.1\0'+canonical),envelope['subject']['preimageSha256'])
   observed='ACCEPT' if good else 'CANONICAL-MISMATCH'
  else:
   independent=json.dumps(lock,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode();check(case['id']+'/second-serializer',independent,raw)
   check(case['id']+'/domain-preimage',sha(b'opensip.metadata.lock.1\0'+raw),result['lockPreimageSha256'])
   bad=variants['locks'][case['unit']];check(case['id']+'/noncanonical-refusal',M.verify_lock_bytes(bytes.fromhex(bad['noncanonicalBytesHex']),result['lockPreimageSha256'],x),'LOCK-NONCANONICAL');check(case['id']+'/wrong-digest-refusal',M.verify_lock_bytes(raw,bad['wrongPreimageSha256'],x),'LOCK-DIGEST')
   observed=M.verify_lock_bytes(raw,result['lockPreimageSha256'],x)
  check(case['id']+'/class-result',observed,case['expected']);check(case['id']+'/environment',case['environment']['network']=='DENIED' and not case['environment']['ambientPath'],True)
  frames.append({'id':case['id'],'result':observed,'lockPreimageSha256':result['lockPreimageSha256'],'platform':x['platform'],'state':case['environment']['state'],'productRun':False})
 check('input-immutability',sha(stored(bundle)),before)
 first=corpus['cases'][0]['resolutionInputs'];sid=variants['corruptedArtifact']['stableId']
 def probe(name,edit_bundle=None,edit_inputs=None,expected='REFUSE'):
  b=copy.deepcopy(bundle);x=copy.deepcopy(first)
  if edit_bundle:edit_bundle(b)
  if edit_inputs:edit_inputs(x,b)
  result=M.solve(b,x,host);check('supplementary/'+name,result['status'],expected)
  if expected=='REFUSE':
   check('supplementary/'+name+'/no-partial',result['resolved'],[])
   reasons={'stale-signed-catalog':'CATALOG-STALE','forged-view-recomputed-pin':'REGISTRY-VIEW-FORGED','cross-project-view':'REGISTRY-SCOPE','wrong-catalog-pin':'CATALOG-CUSTODY','wrong-registry-pin':'REGISTRY-VIEW-CUSTODY','missing-registry-pin':'INPUT-SCHEMA','wrong-scope-install':'REGISTRY-TRUST-JOIN','permission-policy-mismatch':'PERMISSION-POLICY-CUSTODY','compatibility-policy-mismatch':'COMPATIBILITY-POLICY-CUSTODY','missing-artifact':'RJ-4 MISSING-ARTIFACT:bin/entry','forged-manifest':'RJ-4 DIGEST_MISMATCH','duplicate-request':'SELECTION:DUPLICATE-REQUEST-ID','duplicate-pin-hold':'SELECTION:DUPLICATE-PIN-HOLD'}
   check('supplementary/'+name+'/typed-reason',result['reason'],reasons[name])
  return result
 probe('stale-signed-catalog',lambda b:b['documents'].update({'catalog':variants['staleCatalogHex'],'catalog.envelope':variants['staleCatalogEnvelopeHex']}))
 def forged(b):
  v=mutate_doc(b,'view',lambda v:v['entries'].pop());return v
 probe('forged-view-recomputed-pin',forged,lambda x,b:x.update({'registryViewDigest':M.digest(M.VIEW_DOMAIN,json.loads(bytes.fromhex(b['documents']['view'])))}))
 probe('cross-project-view',lambda b:b['documents'].update({'view':b['documents']['view/project-beta']}))
 def beta(x,b):
  v=json.loads(bytes.fromhex(b['documents']['view']));x.update({'scopeContext':v['scopeContext'],'registryViewDigest':M.digest(M.VIEW_DOMAIN,v)})
 result=probe('project-beta-positive',lambda b:b['documents'].update({'view':b['documents']['view/project-beta']}),beta,'ACCEPT');check('supplementary/project-beta-global',next(r['scope'] for r in result['resolved'] if r['stableId']==sid),'global')
 probe('wrong-catalog-pin',edit_inputs=lambda x,b:x.update({'indexDigest':'0'*64}));probe('wrong-registry-pin',edit_inputs=lambda x,b:x.update({'registryViewDigest':'0'*64}));probe('missing-registry-pin',edit_inputs=lambda x,b:x.pop('registryViewDigest'))
 probe('wrong-scope-install',edit_inputs=lambda x,b:x.update({'installId':'11111111-1111-4111-8111-111111111111'}))
 probe('permission-policy-mismatch',edit_inputs=lambda x,b:x.update({'permissionPolicyDigest':'0'*64}));probe('compatibility-policy-mismatch',edit_inputs=lambda x,b:x.update({'compatibilityPolicyDigest':'0'*64}))
 probe('duplicate-request',edit_inputs=lambda x,b:x['request'].append(copy.deepcopy(x['request'][0])))
 probe('duplicate-pin-hold',edit_inputs=lambda x,b:x.update({'pins':[{'stableId':sid,'version':'1.0.0'}],'holds':[{'stableId':sid,'version':'1.0.0'}]}))
 probe('missing-artifact',lambda b:b['artifacts'][sid].pop('bin/entry'));probe('forged-manifest',lambda b:mutate_doc(b,'manifest/'+sid,lambda m:m.update({'displayName':'forged'})))
 # G15-M1: freshness is independent of signature validity and version floors.
 freshness=load('g15-revocation-freshness-cases.v2.json')
 root=json.loads(bytes.fromhex(bundle['documents']['root']))
 for case in freshness['cases']:
  b=copy.deepcopy(bundle);b['documents']['revocation']=case['revocationHex'];b['documents']['revocation.envelope']=case['envelopeHex']
  outcome=M.SEC.verify_envelope(bytes.fromhex(case['revocationHex']),json.loads(bytes.fromhex(case['envelopeHex'])),root,'revocation','opensip')[0]
  check('freshness/'+case['id']+'/signature',outcome,'VERIFIED')
  result=M.solve(b,case['resolutionInputs'],case['host'])
  check('freshness/'+case['id']+'/status',result['status'],case['expectedStatus'])
  check('freshness/'+case['id']+'/reason',result.get('reason'),case['expectedReason'])
  if case['expectedStatus']=='REFUSE':
   check('freshness/'+case['id']+'/no-partial',result['resolved'],[])
   check('freshness/'+case['id']+'/no-lock','referenceLock' in result,False)
  else:
   check('freshness/'+case['id']+'/two-components',len(result['resolved']),2)
   check('freshness/'+case['id']+'/same-custody',result['lockBytesHex'],goldens[corpus['cases'][0]['golden']]['lockBytesHex'])
 probe_input=load('g15-stale-revocation-probe.v2.json');result=M.solve(probe_input['bundle'],probe_input['resolutionInputs'],probe_input['host'])
 check('freshness/exact-independent-probe/status',result['status'],'REFUSE');check('freshness/exact-independent-probe/reason',result.get('reason'),'REVOCATION-STALE');check('freshness/exact-independent-probe/no-partial',result['resolved'],[])
 # Every pre-existing key remains assigned its pinned concrete definition; only
 # five conditional keys receive new inputs. No slots are credited as OS runs.
 old=load('qualification-design-packaging.v1.json');old_definitions=load('qualification-design-schema-join.v1.json')['definitions'];newids={c['id']:c for c in corpus['cases']};slots=set();newcount=0
 for unit,previous in zip(matrix['matrix'],old['matrix']):
  check('matrix/'+unit['id']+'/80keys',set(unit['members']),set(previous['members']))
  for key,value in unit['members'].items():
   slots.add((unit['id'],key))
   if key in ['TC-ACCEPT.5','TC-SIG.C-LOCK','TC-SIG.C-ENVELOPE','TC-BYTE-EXACT.C-CANON','TC-BYTE-EXACT.C-LOCK']:
    newcount+=1;check('matrix/'+unit['id']+'/'+key,unit['id']+'/'+key in newids,True)
   else:
    check('matrix/'+unit['id']+'/'+key+'/retained',{k:v for k,v in value.items() if k in previous['members'][key]},previous['members'][key])
    if key in old_definitions:check('matrix/'+unit['id']+'/'+key+'/concrete','INTEGRATION-REQUIRED' not in old_definitions[key]['standing'],True)
 # Re-resolve every old byte pin, not only the JSON file containing its path.
 pending=[old,load('qualification-design-schema-join.v1.json')];pins={}
 while pending:
  item=pending.pop()
  if isinstance(item,dict):
   if isinstance(item.get('path'),str) and item['path'].startswith('docs/') and isinstance(item.get('sha256'),str):pins[item['path']]=item['sha256']
   pending.extend(item.values())
  elif isinstance(item,list):pending.extend(item)
 for path,value in pins.items():check('inherited-byte-pin/'+path,sha((ROOT/path).read_bytes()),value)
 for unit in matrix['matrix']:
  for key,member in unit['members'].items():
   pointer=member['designInput'];value=json.loads((ROOT/pointer['path']).read_text())
   for part in pointer['selector'].split('/')[1:]:
    part=part.replace('~1','/').replace('~0','~');value=value[int(part)] if isinstance(value,list) else value[part]
   check('matrix-pointer/'+unit['id']+'/'+key,value is not None,True)
 check('matrix/960slots',len(slots),960);check('matrix/60new',newcount,60);check('matrix/60executed-design-inputs',len(frames),60)
 files=['compatibility-selection-model.v5.py','component-lock-schema.completed.v3.json','g15-conditional-bundle.v1.json','g15-conditional-prior-bundle.v1.json','g15-conditional-host.v1.json','g15-conditional-prior-host.v1.json','g15-conditional-cases.v2.json','g15-conditional-goldens.v1.json','g15-conditional-variants.v1.json','g15-conditional-matrix.v2.json','check_g15_conditional_v2.py','g15-revocation-freshness-cases.v2.json','g15-stale-revocation-probe.v2.json']
 # JSON reports retain hashes rather than large byte/set values in comparison output.
 for row in results:
  for field in ['observed','expected']:
   if isinstance(row[field],bytes):row[field]={'bytesSha256':sha(row[field]),'length':len(row[field])}
   elif isinstance(row[field],set):row[field]=sorted(row[field])
 report={'status':'DESIGN-EVIDENCE-NOT-PRODUCT-QUALIFICATION','passed':sum(r['passed'] for r in results),'total':len(results),'results':results,'conditionalSlots':frames,'subjectPins':{n:sha((P/n).read_bytes()) for n in files},'qualification':{'nativeOSRuns':0,'conditionalDesignInputs':60,'matrixAssignedSlots':960},'limitations':['Synthetic TEST keys and archives are public design evidence; no shipping component or OS execution.','Prior0.9.0 generation is verified under its historical floor8 and retained immutably; current floor9 is never lowered.','Existing900matrix slots retain prior concrete design inputs and their documented limitations; assigning inputs is not product qualification.','Full host trust state transitions, persistent registry publication and process confinement remain their separately reviewed owners.']}
 Path(args.report).write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n');print(json.dumps({'passed':report['passed'],'total':report['total']}))
 if report['passed']!=report['total']:
  print(json.dumps([r for r in results if not r['passed']],indent=2));return 1
 return 0
if __name__=='__main__':
 import sys
 ap=argparse.ArgumentParser();ap.add_argument('--report',default=str(P/'g15-conditional-report.v2.json'));ap.add_argument('--python',default=sys.executable);raise SystemExit(run(ap.parse_args()))
