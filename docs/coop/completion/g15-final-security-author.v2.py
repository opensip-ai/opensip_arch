#!/usr/bin/env python3
"""New fixtures against the receipt-pinned frozen security dependency; conditional design evidence only."""
import copy,hashlib,importlib.util,json
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
P=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('final_g15',P/'compatibility-selection-model.v7.py');M=importlib.util.module_from_spec(s);s.loader.exec_module(M)
def load(n):return json.loads((P/n).read_text())
def stored(v):return (json.dumps(v,indent=2,ensure_ascii=False)+'\n').encode()
def dump(n,v):(P/n).write_bytes(stored(v))
def setdoc(b,k,v):b['documents'][k]=stored(v).hex()
def sign_document(bundle,key,obj,kind):
 raw=stored(obj);domain,role=M.SEC.KIND_ROUTING[kind];env={'envelopeSchema':2,'subject':{'kind':kind,'domain':domain,'storedSha256':M.sha(raw),'preimageSha256':M.digest(domain,obj)},'role':role,'namespace':'opensip','signatures':[]};msg=bytes.fromhex(M.SEC.envelope_message_hex(env));records=[r for r in load('g15-conditional-test-keys.v1.json')['keys'] if ' '+role+' ' in r['label']];env['signatures']=sorted([{'keyId':r['keyId'],'alg':'ed25519','signature':Ed25519PrivateKey.from_private_bytes(bytes.fromhex(r['PUBLIC_TEST_SEED_HEX'])).sign(msg).hex()} for r in records[:2]],key=lambda r:r['keyId']);bundle['documents'][key]=raw.hex();setdoc(bundle,key+'.envelope',env);return M.sha(raw)

def policy_join(bundle,host,x,global_doc=None,project_doc=None,selected=True):
 b=copy.deepcopy(bundle);h=copy.deepcopy(host);x=copy.deepcopy(x)
 root=json.loads(bytes.fromhex(b['documents']['root']));root['kernelAttestationKeys']=[];h['trustedRootStoredSha256']=sign_document(b,'root',root,'root')
 compatibility_raw=(P/'compatibility-matrix.completed.v5.json').read_bytes();b['documents']['compatibility-policy']=compatibility_raw.hex();h['compatibilityPolicyDigest']=x['compatibilityPolicyDigest']=M.sha(compatibility_raw)
 if global_doc is None:
  global_doc=json.loads(bytes.fromhex(b['documents']['permission-policy']));global_doc['policyScope']='global'
 if selected and project_doc is None:
  project_doc=copy.deepcopy(global_doc);project_doc['policyScope']='project'
  if project_doc['grants']:project_doc['grants'][0]['scope']['pathPrefixes']=['src']
 setdoc(b,'permission-policy.global',global_doc)
 if selected:setdoc(b,'permission-policy.project',project_doc)
 else:b['documents'].pop('permission-policy.project',None)
 effective,errors=M.SEC.effective_policy_for_operation(global_doc,project_doc,selected)
 setdoc(b,'permission-policy',effective);h['policyPresence']={'global':'PRESENT','project':'PRESENT' if selected else 'NO-NAMESPACE'};h['permissionPolicySources']={'global':M.digest(M.SEC.DOMAIN_TAGS['policy'],global_doc),'project':M.digest(M.SEC.DOMAIN_TAGS['policy'],project_doc) if selected else None};h['projectPolicyMode']='SELECTED-PROJECT' if selected else 'GLOBAL-ONLY';h['permissionPolicyDigest']=x['permissionPolicyDigest']=M.SEC.effective_policy_digest(effective)
 return b,h,x,errors

def main():
 old=load('g15-conditional-bundle.v1.json');host=load('g15-conditional-host.v1.json');cases=load('g15-conditional-cases.v2.json')['cases'];bundle,host,_,errors=policy_join(old,host,cases[0]['resolutionInputs']);assert not errors
 dump('g15-final-security-bundle.v2.json',bundle);dump('g15-final-security-host.v2.json',host)
 prior,prior_host,_,errors=policy_join(load('g15-conditional-prior-bundle.v1.json'),load('g15-conditional-prior-host.v1.json'),next(c['environment']['priorSelection']['resolutionInputs'] for c in cases if c['environment']['state']=='upgrade'));assert not errors
 dump('g15-final-security-prior-bundle.v2.json',prior);dump('g15-final-security-prior-host.v2.json',prior_host)
 goldens={}
 for c in cases:
  c['resolutionInputs']['permissionPolicyDigest']=host['permissionPolicyDigest'];c['resolutionInputs']['compatibilityPolicyDigest']=host['compatibilityPolicyDigest'];r=M.solve(bundle,c['resolutionInputs'],host);assert r['status']=='ACCEPT',r;goldens[c['golden']]=r
  if c['environment']['state']=='upgrade':
   prior_input=c['environment']['priorSelection']['resolutionInputs'];prior_input['permissionPolicyDigest']=prior_host['permissionPolicyDigest'];prior_input['compatibilityPolicyDigest']=prior_host['compatibilityPolicyDigest'];pr=M.solve(prior,prior_input,prior_host);assert pr['status']=='ACCEPT',pr;c['environment']['priorSelection']={**c['environment']['priorSelection'],**{k:pr[k] for k in ['lockBytesHex','lockPreimageSha256']}}
 dump('g15-final-security-cases.v2.json',{'standing':'CONDITIONAL-ON-INDEPENDENT-SECURITY-ACCEPTANCE','sourcePins':{v['path']:v['sha256'] for v in load('g15-final-security-inputs.v2.json')['sources']},'cases':cases});dump('g15-final-security-goldens.v2.json',goldens)
 x=copy.deepcopy(cases[0]['resolutionInputs']);variants=[]
 def add(id,b,h,xx,status='REFUSE',reason=None,grants=None):
  result=M.solve(b,xx,h)
  assert result['status']==status,(id,result)
  if reason:assert result['reason']==reason,(id,result)
  variants.append({'id':id,'documents':{k:v for k,v in b['documents'].items() if bundle['documents'].get(k)!=v},'removeDocuments':[k for k in bundle['documents'] if k not in b['documents']],'host':h,'resolutionInputs':xx,'expectedStatus':status,'expectedReason':reason,'expectedEffectiveGrantCount':grants,'expectedLock':result if status=='ACCEPT' else None})
 g=json.loads(bytes.fromhex(bundle['documents']['permission-policy.global']));p=json.loads(bytes.fromhex(bundle['documents']['permission-policy.project']))
 # Files absent under trusted no-follow observations become explicit empty
 # policy values, distinct from unexpected deletion of an expected source.
 empty_global={'policySchema':1,'policyScope':'global','grants':[],'denies':[],'consents':[]};empty_project=copy.deepcopy(M.SEC.EMPTY_PROJECT_POLICY)
 b,h,xx,e=policy_join(old,load('g15-conditional-host.v1.json'),x,empty_global,empty_project);b['documents'].pop('permission-policy.global');b['documents'].pop('permission-policy.project');h['policyPresence']={'global':'ABSENT','project':'ABSENT'};add('both-policy-files-absent-explicit-empty',b,h,xx,'ACCEPT',grants=0)
 b,h,xx,e=policy_join(old,load('g15-conditional-host.v1.json'),x,g,empty_project);b['documents'].pop('permission-policy.project');h['policyPresence']['project']='ABSENT';add('selected-project-file-absent-explicit-empty',b,h,xx,'ACCEPT',grants=0)
 b=copy.deepcopy(bundle);b['documents'].pop('permission-policy.global');add('expected-global-source-missing',b,host,x,reason='MISSING-DOCUMENT:permission-policy.global')

 empty=copy.deepcopy(M.SEC.EMPTY_PROJECT_POLICY);b,h,xx,e=policy_join(old,load('g15-conditional-host.v1.json'),x,g,empty);add('selected-project-empty-denies-by-absence',b,h,xx,'ACCEPT',grants=0)
 denied=copy.deepcopy(p);denied['denies']=[{k:v for k,v in denied['grants'][0].items() if k!='scope'}];b,h,xx,e=policy_join(old,load('g15-conditional-host.v1.json'),x,g,denied);add('project-deny-wins',b,h,xx,'ACCEPT',grants=0)
 b,h,xx,e=policy_join(old,load('g15-conditional-host.v1.json'),x,g,None,False)
 xx['scopeContext']={'projectKey':None,'allowedScopes':['global']};store=json.loads(bytes.fromhex(b['documents']['registry']));v=M.export_view(store,xx['scopeContext'],'2026-12-21T10:05:00Z');setdoc(b,'view',v);xx['registryViewDigest']=M.digest(M.VIEW_DOMAIN,v);add('global-only-no-project-policy',b,h,xx,'ACCEPT',grants=1)
 for id,key,mutation in [('global-source-changed','permission-policy.global',lambda q:q['grants'].clear()),('project-source-changed','permission-policy.project',lambda q:q['grants'].clear())]:
  b=copy.deepcopy(bundle);q=json.loads(bytes.fromhex(b['documents'][key]));mutation(q);setdoc(b,key,q);add(id,b,host,x,reason='POLICY-'+('GLOBAL' if 'global' in key else 'PROJECT')+'-CUSTODY')
 for id,fn in [('effective-grants-forged',lambda q:q['grants'].clear()),('effective-source-forged',lambda q:q['sources'].update(global_='a'*64))]:
  b=copy.deepcopy(bundle);q=json.loads(bytes.fromhex(b['documents']['permission-policy']));fn(q);setdoc(b,'permission-policy',q);hh=copy.deepcopy(host);xx=copy.deepcopy(x);hh['permissionPolicyDigest']=xx['permissionPolicyDigest']=M.SEC.effective_policy_digest(q);add(id,b,hh,xx,reason='EFFECTIVE-POLICY-FORGED' if id=='effective-grants-forged' else 'SCHEMA-effective-permission-policy')
 b=copy.deepcopy(bundle);b['documents'].pop('permission-policy.project');add('expected-project-source-missing',b,host,x,reason='MISSING-DOCUMENT:permission-policy.project')
 b=copy.deepcopy(bundle);q=copy.deepcopy(p);q['policyScope']='global';setdoc(b,'permission-policy.project',q);add('source-scope-swapped',b,host,x,reason='POLICY-PROJECT-SCOPE')
 broad=copy.deepcopy(p);broad['grants'][0]['scope']['pathPrefixes']=['private'];b,h,xx,e=policy_join(old,load('g15-conditional-host.v1.json'),x,g,broad);assert e;add('project-scope-widening',b,h,xx,reason='POLICY-MERGE-REFUSED:'+','.join(e))
 for id,mutate,reason in [('project-path-traversal',lambda q:q['grants'][0]['scope'].update(pathPrefixes=['src/../private']),'POLICY.PATH_PREFIX_NOT_NORMALIZED:PT-FS-READ-PROJECT:src/../private'),('project-duplicate-grant',lambda q:q['grants'].append(copy.deepcopy(q['grants'][0])),'POLICY.DUPLICATE_GRANT_PAIR')]:
  pp=copy.deepcopy(p);mutate(pp);b,h,xx,e=policy_join(old,load('g15-conditional-host.v1.json'),x,g,pp);assert reason in e;add(id,b,h,xx,reason='POLICY-MERGE-REFUSED:'+reason)
 # Raw source admission and scalar stateClass narrowing are composed through
 # the selector; independently call the merge boundary to retain zero grants.
 for label,global_scope,project_scope,status in [('stateclass-equal',{'stateClass':'SC-OPS'},{'stateClass':'SC-OPS'},'ACCEPT'),('stateclass-widening',{'stateClass':'SC-CACHE'},{'stateClass':'SC-OPS'},'REFUSE'),('stateclass-added-without-global',{}, {'stateClass':'SC-OPS'},'REFUSE')]:
  gg=copy.deepcopy(g);pp=copy.deepcopy(p)
  for policy,scope in [(gg,global_scope),(pp,project_scope)]:policy['grants']=[{'stableId':g['grants'][0]['stableId'],'token':'PT-FS-WRITE-HOST-STATE','scope':scope}]
  b,h,xx,e=policy_join(old,load('g15-conditional-host.v1.json'),x,gg,pp)
  add(label,b,h,xx,status,('POLICY-MERGE-REFUSED:'+','.join(e)) if e else None,1 if status=='ACCEPT' else None)
  eff,refusals=M.SEC.merge_policy(gg,pp);assert (not refusals) if status=='ACCEPT' else (refusals and eff['grants']==[])
  variants[-1]['rawPolicyMerge']={'global':gg,'project':pp,'expectedRefusals':refusals,'expectedGrantCount':len(eff['grants'])}
 for label,mutation in [('raw-policy-unknown-member',lambda q:q.update(unknownAuthority=True)),('raw-policy-string-prefixes',lambda q:q['grants'][0]['scope'].update(pathPrefixes='src')),('raw-policy-null-grants',lambda q:q.update(grants=None)),('raw-policy-missing-denies',lambda q:q.pop('denies'))]:
  pp=copy.deepcopy(p);mutation(pp);b=copy.deepcopy(bundle);setdoc(b,'permission-policy.project',pp)
  add(label,b,host,x,reason='SCHEMA-permission-policy')
  eff,refusals=M.SEC.merge_policy(g,pp);assert refusals==['POLICY.SHAPE'] and eff['grants']==[]
  variants[-1]['rawPolicyMerge']={'global':g,'project':pp,'expectedRefusals':['POLICY.SHAPE'],'expectedGrantCount':0}
 # Revocation removes counted signatures, not immutable admitted-root keys.
 current_catalog_envelope=json.loads(bytes.fromhex(bundle['documents']['catalog.envelope']));signed_ids={sig['keyId'] for sig in current_catalog_envelope['signatures']};root_doc=json.loads(bytes.fromhex(bundle['documents']['root']));role_ids=root_doc['roles']['TR-INDEX']['keys']
 for id,kid,status,reason in [('revoked-catalog-signer',next(iter(sorted(signed_ids))),'REFUSE','THRESHOLD-SHORTFALL'),('revoked-unused-catalog-key',next(k for k in role_ids if k not in signed_ids),'ACCEPT',None)]:
  b=copy.deepcopy(bundle);rev=json.loads(bytes.fromhex(b['documents']['revocation']));rev['entries'].append({'subjectKind':'keyId','subject':kid,'reason':'key-compromise','revokedAt':'2026-12-20T00:00:00Z'});sign_document(b,'revocation',rev,'revocation');add(id,b,host,x,status,reason,1 if status=='ACCEPT' else None)
 # Whole original envelope admission must precede the revoked-signature view.
 unused=next(k for k in role_ids if k not in signed_ids);base=copy.deepcopy(bundle);rev=json.loads(bytes.fromhex(base['documents']['revocation']));rev['entries'].append({'subjectKind':'keyId','subject':unused,'reason':'key-compromise','revokedAt':'2026-12-20T00:00:00Z'});sign_document(base,'revocation',rev,'revocation')
 env=json.loads(bytes.fromhex(base['documents']['catalog.envelope']));key=next(r for r in load('g15-conditional-test-keys.v1.json')['keys'] if r['keyId']==unused)
 valid_revoked={'keyId':unused,'alg':'ed25519','signature':Ed25519PrivateKey.from_private_bytes(bytes.fromhex(key['PUBLIC_TEST_SEED_HEX'])).sign(bytes.fromhex(M.SEC.envelope_message_hex(env))).hex()}
 env['signatures'].append(valid_revoked);setdoc(base,'catalog.envelope',env);add('valid-revoked-signature-in-original-envelope',base,host,x,'ACCEPT',grants=1)
 for label,mutation in [('malformed-revoked-signature',lambda e:e['signatures'].__setitem__(-1,{'keyId':unused,'alg':'not-an-algorithm','signature':'broken','extra':'forbidden'})),('duplicate-revoked-signature',lambda e:e['signatures'].append(copy.deepcopy(valid_revoked))),('original-envelope-over-16-signatures',lambda e:e.update(signatures=e['signatures'][:2]+[{**valid_revoked,'signature':format(i,'0128x')} for i in range(15)])),('original-envelope-float-schema',lambda e:e.update(envelopeSchema=2.0)),('original-envelope-unknown-member',lambda e:e.update(extraAuthority=True)),('original-envelope-unknown-subject',lambda e:e['subject'].update(extraAuthority=True))]:
  b=copy.deepcopy(base);bad=copy.deepcopy(env);mutation(bad);setdoc(b,'catalog.envelope',bad);add(label,b,host,x,reason='FLOAT_FORBIDDEN' if label=='original-envelope-float-schema' else 'RJ-4 UNSIGNED')
 xx=copy.deepcopy(x);xx['permissionPolicyDigest']='0'*64;add('stale-effective-lock-pin',bundle,host,xx,reason='PERMISSION-POLICY-CUSTODY')
 # Actual public TEST root signatures isolate semantic admission from signature/custody failure.
 records=load('g15-conditional-test-keys.v1.json')['keys'];rootkeys=[r for r in records if ' ROOT ' in r['label']]
 def signed_root(b,r):
  raw=stored(r);env={'envelopeSchema':2,'subject':{'kind':'root','domain':M.SEC.DOMAIN_TAGS['root'],'storedSha256':M.sha(raw),'preimageSha256':M.digest(M.SEC.DOMAIN_TAGS['root'],r)},'role':'ROOT','namespace':'opensip','signatures':[]};msg=bytes.fromhex(M.SEC.envelope_message_hex(env));env['signatures']=sorted([{'keyId':z['keyId'],'alg':'ed25519','signature':Ed25519PrivateKey.from_private_bytes(bytes.fromhex(z['PUBLIC_TEST_SEED_HEX'])).sign(msg).hex()} for z in rootkeys[:2]],key=lambda z:z['keyId']);b['documents']['root']=raw.hex();setdoc(b,'root.envelope',env);return M.sha(raw)
 root=json.loads(bytes.fromhex(bundle['documents']['root']))
 mutations=[('root-kernel-attestation-not-empty',lambda r:r.update(kernelAttestationKeys=json.loads(bytes.fromhex(old['documents']['root']))['kernelAttestationKeys'])),('root-weak-threshold',lambda r:r.update(rootThreshold=1)),('root-key-id-mismatch',lambda r:r['keys'][0].update(keyId='0'*64)),('root-recovery-overlap',lambda r:r['recoveryAuthority']['keys'].__setitem__(0,r['rootKeys'][0])),('root-role-overlap',lambda r:r['roles']['TR-COMPONENT']['keys'].__setitem__(0,r['roles']['TR-INDEX']['keys'][0])),('root-active-typed-absence',lambda r:r['roles']['TR-COMPONENT'].update(standing='typed-absence-DR-110')),('root-origin-previous',lambda r:r.update(previousRootVersion=1)),('root-expiry-before-issue',lambda r:r.update(expiresAt='2020-01-01T00:00:00Z'))]
 for id,mutate in mutations:
  b=copy.deepcopy(bundle);r=copy.deepcopy(root);mutate(r);h=copy.deepcopy(host);h['trustedRootStoredSha256']=signed_root(b,r)
  if id=='root-kernel-attestation-not-empty':assert b['documents']['root']==old['documents']['root'] and b['documents']['root.envelope']==old['documents']['root.envelope']
  add(id,b,h,x,reason='SCHEMA-root' if id in ['root-weak-threshold','root-kernel-attestation-not-empty'] else 'ROOT-NOT-ADMITTED')
 dump('g15-final-security-variants.v2.json',{'variants':variants})
if __name__=='__main__':main()
