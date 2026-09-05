#!/usr/bin/env python3
"""Author public TEST-key G15 metadata/lock fixtures; never release signing."""
import copy,hashlib,importlib.util,json
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding,PublicFormat
P=Path(__file__).resolve().parent;ROOT=P.parents[2]
s=importlib.util.spec_from_file_location('g15_author_model',P/'compatibility-selection-model.v4.py');M=importlib.util.module_from_spec(s);s.loader.exec_module(M);SEC=M.SEC

def store(v):return (json.dumps(v,indent=2,ensure_ascii=False)+'\n').encode()
def dump(name,obj):(P/name).write_bytes(store(obj))
def sha(b):return hashlib.sha256(b).hexdigest()
keys={};records=[]
for role in ['ROOT','TR-INDEX','TR-COMPONENT']:
 keys[role]=[]
 for i in range(3):
  label=f'OPENSiP PUBLIC G15 DESIGN TEST ONLY {role} {i}';seed=hashlib.sha256(label.encode()).digest();key=Ed25519PrivateKey.from_private_bytes(seed);pub=key.public_key().public_bytes(Encoding.Raw,PublicFormat.Raw);kid=sha(pub);keys[role].append((kid,key));records.append({'keyId':kid,'publicKey':pub.hex(),'label':label,'PUBLIC_TEST_SEED_HEX':seed.hex()})
root=json.loads((P/'security-fixtures.v2/root.example.json').read_text());root['keys'] += [{k:v for k,v in r.items() if k!='PUBLIC_TEST_SEED_HEX'} for r in records];root['rootKeys']=[kid for kid,_ in keys['ROOT']]
for role in ['TR-INDEX','TR-COMPONENT']:root['roles'][role]['keys']=[kid for kid,_ in keys[role]]
# Root is the fixed public test trust anchor, not a self-selected release trust root.
bundle={'documents':{},'artifacts':{}}
def document(key,obj):bundle['documents'][key]=store(obj).hex()
def sign(raw,kind,preimage=None):
 domain,role=SEC.KIND_ROUTING[kind];obj=SEC.load_json_strict(raw);env={'envelopeSchema':2,'subject':{'kind':kind,'domain':domain,'storedSha256':sha(raw),'preimageSha256':preimage or M.digest(domain,obj)},'role':role,'namespace':'opensip','signatures':[]};msg=bytes.fromhex(SEC.envelope_message_hex(env));env['signatures']=sorted([{'keyId':kid,'alg':'ed25519','signature':key.sign(msg).hex()} for kid,key in keys[role][:2]],key=lambda q:q['keyId']);return env

def signed(key,obj,kind):
 document(key,obj);document(key+'.envelope',sign(bytes.fromhex(bundle['documents'][key]),kind))
signed('root',root,'root')
rev=json.loads((P/'security-fixtures.v2/revocation.example.json').read_text());signed('revocation',rev,'revocation')
base=json.loads((P/'manifest-bases.completed.v1.json').read_text())['artifact-closure'];source_blobs=json.loads((P/'manifest-artifact-blobs.completed.v1.json').read_text());A=base['stableId'];B='11111111-1111-4111-8111-111111111111';manifests=[]
for sid,name,dependencies in [(A,'typescript-analyzer',[{'stableId':B,'versionConstraint':'1.0.0','reason':'Public non-shipping qualification twin dependency'}]),(B,'fixture-typescript-twin',[])]:
 m=copy.deepcopy(base);m.update({'stableId':sid,'name':name,'displayName':name+' café','dependencies':dependencies});m['commands'][0]['name']=name
 if sid==B:m['capabilities']=[]
 files={}
 for plat in m['platforms']:
  for entry in plat['tree']['entries']:
   if entry['type']=='file':files[entry['path']]=source_blobs[entry['sha256']]
 for kind,ref in m['declarations'].items():
  files[ref['path']]=source_blobs[ref['sha256']]
  if kind=='licenses':
   for notice in json.loads(bytes.fromhex(files[ref['path']]))['noticeInventory']:files[notice['path']]=source_blobs[notice['sha256']]
 signed('manifest/'+sid,m,'manifest');files['manifest.json']=bundle['documents']['manifest/'+sid];files['envelope.json']=bundle['documents']['manifest/'+sid+'.envelope']
 for plat in m['platforms']:
  tree=[]
  for e in plat['tree']['entries']:
   item={**e,'mode':int(e['mode'],8)}
   if e['type']=='file':item['bodyHex']=files[e['path']]
   tree.append(item)
  raw=M.ARCH.library_encode_fixed_vector(tree);files['archive.'+plat['os']+'-'+plat['arch']+'.tar']=raw.hex()
 bundle['artifacts'][sid]=files;manifests.append(m)
catalog=json.loads((P/'security-fixtures.v2/catalog.example.json').read_text());catalog['releases']=[]
for m in sorted(manifests,key=lambda q:q['stableId']):
 sid=m['stableId'];raw=bytes.fromhex(bundle['documents']['manifest/'+sid]);env=SEC.load_json_strict(bytes.fromhex(bundle['documents']['manifest/'+sid+'.envelope']));catalog['releases'].append({'stableId':sid,'publisher':m['provenance']['publisher'],'sourceClass':m['provenance']['sourceClass'],'version':m['version'],'manifestDigest':sha(raw),'manifestPreimageSha256':env['subject']['preimageSha256'],'envelopeDigest':sha(bytes.fromhex(bundle['documents']['manifest/'+sid+'.envelope'])),'hostCoreConstraint':m['compatibility']['hostCore'],'artifacts':[{'platform':plat['os']+'-'+plat['arch'],'archiveProfileId':'archive-profile.1','archiveDigest':sha(bytes.fromhex(bundle['artifacts'][sid]['archive.'+plat['os']+'-'+plat['arch']+'.tar'])),'sha256':sha(bytes.fromhex(bundle['artifacts'][sid]['archive.'+plat['os']+'-'+plat['arch']+'.tar']))} for plat in m['platforms']]})
signed('catalog',catalog,'catalog');catalog_digest=M.digest(SEC.DOMAIN_TAGS['catalog'],catalog)
store_obj=json.loads((P/'security-fixtures.v2/registry.example.json').read_text());store_obj['entries']=[];store_obj['retiredIds']=[];store_obj['reservedRootCommands']=catalog['reservedRootCommands'];store_obj['trustMetadata']={'rootVersion':1,'catalogSnapshotVersion':9,'revocationVersion':3}
for m in sorted(manifests,key=lambda q:q['stableId']):
 sid=m['stableId'];release=next(r for r in catalog['releases'] if r['stableId']==sid)
 for scope,project in [('global',None)]+([('project','project-alpha')] if sid==A else []):
  store_obj['entries'].append({'stableId':sid,'provenance':m['provenance'],'version':m['version'],'manifestDigest':release['manifestDigest'],'signatureRef':release['envelopeDigest'],'admittedAt':'2026-12-21T10:00:00Z','scope':scope,'projectKey':project,'mountedRootCommand':m['name'],'namesSnapshot':{'name':m['name'],'aliases':[],'mountedRootCommand':m['name']},'status':'active','deprecation':None,'ownershipTransfers':[],'catalogSnapshotVersion':9,'catalogPreimageSha256':catalog_digest})
document('registry',store_obj)
views={project:M.export_view(store_obj,{'projectKey':project,'allowedScopes':['project','global']},'2026-12-21T10:05:00Z') for project in ['project-alpha','project-beta']}
for project,view in views.items():document('view/'+project,view)
document('view',views['project-alpha'])
host={'trustedRootStoredSha256':sha(bytes.fromhex(bundle['documents']['root'])),'sourceStoreDigest':M.digest(M.REGISTRY_DOMAIN,store_obj),'now':'2026-12-21T10:10:00Z','floors':{'rootVersion':1,'catalogSnapshotVersion':9,'revocationVersion':3}}
x=copy.deepcopy(json.loads((P/'compatibility-selection-cases.v3.json').read_text())['selections'][0]['input']['resolutionInputs']);x.update({'installId':store_obj['installId'],'indexDigest':catalog_digest,'registryViewDigest':M.digest(M.VIEW_DOMAIN,views['project-alpha']),'scopeContext':views['project-alpha']['scopeContext'],'request':[{'stableId':A,'version':'1.0.0'}]})
policy=json.loads((P/'security-fixtures.v2/permission-policy.example.json').read_text());document('permission-policy',policy);x['permissionPolicyDigest']=M.digest(SEC.DOMAIN_TAGS['policy'],policy)
compat=json.loads((P/'compatibility-matrix.completed.v4.json').read_text());document('compatibility-policy',compat);x['compatibilityPolicyDigest']=sha(bytes.fromhex(bundle['documents']['compatibility-policy']))
host.update({k:x[k] for k in ['permissionPolicyDigest','compatibilityPolicyDigest']})
# Public policy inputs are digest pins only and confer no permission.
dump('g15-conditional-bundle.v1.json',bundle);dump('g15-conditional-test-keys.v1.json',{'warning':'PUBLIC TEST SEEDS; NEVER RELEASE KEYS','keys':records});dump('g15-conditional-host.v1.json',host)
# Wrong preimage carries cryptographically valid authorized TEST signatures.
wrong=copy.deepcopy(manifests[0]);wrong['version']='1.0.1';wrong_env=sign(bytes.fromhex(bundle['documents']['manifest/'+A]),'manifest',M.digest(SEC.DOMAIN_TAGS['manifest'],wrong))
variants={'wrongManifestPreimageEnvelopeHex':store(wrong_env).hex(),'corruptedArtifact':{'stableId':A,'artifact':'bin/entry','bytesHex':(b'X'+bytes.fromhex(bundle['artifacts'][A]['bin/entry'])[1:]).hex()},'locks':{},'canonicalManifests':{m['stableId']:SEC.canonical_bytes(m).hex() for m in manifests}}
# Freshly signed but below-floor catalog, to prove a valid signature cannot cure staleness.
stale=copy.deepcopy(catalog);stale['snapshotVersion']=8;stale_raw=store(stale);variants['staleCatalogHex']=stale_raw.hex();variants['staleCatalogEnvelopeHex']=store(sign(stale_raw,'catalog')).hex()
dump('g15-conditional-variants.v1.json',variants)
# An actual earlier immutable generation for upgrade-state preservation.
prior_bundle=copy.deepcopy(bundle);prior_manifest=copy.deepcopy(next(m for m in manifests if m['stableId']==A));prior_manifest['version']='0.9.0'
prior_raw=store(prior_manifest);prior_env_raw=store(sign(prior_raw,'manifest'))
prior_bundle['documents']['manifest/'+A]=prior_raw.hex();prior_bundle['documents']['manifest/'+A+'.envelope']=prior_env_raw.hex();prior_bundle['artifacts'][A]['manifest.json']=prior_raw.hex();prior_bundle['artifacts'][A]['envelope.json']=prior_env_raw.hex()
prior_catalog=copy.deepcopy(catalog);prior_catalog['snapshotVersion']=8
for r in prior_catalog['releases']:
 if r['stableId']==A:r.update({'version':'0.9.0','manifestDigest':sha(prior_raw),'manifestPreimageSha256':M.digest(SEC.DOMAIN_TAGS['manifest'],prior_manifest),'envelopeDigest':sha(prior_env_raw)})
prior_cat_raw=store(prior_catalog);prior_cat_digest=M.digest(SEC.DOMAIN_TAGS['catalog'],prior_catalog)
prior_bundle['documents']['catalog']=prior_cat_raw.hex();prior_bundle['documents']['catalog.envelope']=store(sign(prior_cat_raw,'catalog')).hex()
prior_store=copy.deepcopy(store_obj);prior_store['trustMetadata']['catalogSnapshotVersion']=8
for e in prior_store['entries']:
 e['catalogSnapshotVersion']=8;e['catalogPreimageSha256']=prior_cat_digest
 if e['stableId']==A:e.update({'version':'0.9.0','manifestDigest':sha(prior_raw),'signatureRef':sha(prior_env_raw)})
prior_bundle['documents']['registry']=store(prior_store).hex();prior_view=M.export_view(prior_store,x['scopeContext'],'2026-12-21T10:04:00Z');prior_bundle['documents']['view']=store(prior_view).hex()
prior_host=copy.deepcopy(host);prior_host['floors']['catalogSnapshotVersion']=8;prior_host['sourceStoreDigest']=M.digest(M.REGISTRY_DOMAIN,prior_store)
prior_inputs=copy.deepcopy(x);prior_inputs.update({'indexDigest':prior_cat_digest,'registryViewDigest':M.digest(M.VIEW_DOMAIN,prior_view),'request':[{'stableId':A,'version':'0.9.0'}]})
dump('g15-conditional-prior-bundle.v1.json',prior_bundle);dump('g15-conditional-prior-host.v1.json',prior_host)
old=json.loads((P/'qualification-design-packaging.v1.json').read_text());matrix=copy.deepcopy(old['matrix']);classes=['TC-ACCEPT.5','TC-SIG.C-LOCK','TC-SIG.C-ENVELOPE','TC-BYTE-EXACT.C-CANON','TC-BYTE-EXACT.C-LOCK'];cases=[];goldens={}
for unit in matrix:
 for key,member in unit['members'].items():
  if 'designInput' not in member:
   selector=('/atHalves/'+key) if key in old['atHalves'] else '/archiveCases/'+str(next(i for i,c in enumerate(old['archiveCases']) if c['id']==key))
   member['designInput']={'path':'docs/coop/completion/qualification-design-packaging.v1.json','selector':selector}
 platform_name,state=unit['id'].split('/');osname,arch=platform_name.split('-');osname={'macOS':'macos','Linux':'linux'}[osname]
 request=copy.deepcopy(x);request['platform']={'os':osname,'arch':arch};result=M.solve(bundle,request,host)
 assert result['status']=='ACCEPT',result
 assert len(result['resolved'])==2 and {r['stableId'] for r in result['resolved']}=={A,B}
 assert next(r for r in result['resolved'] if r['stableId']==A)['scope']=='project'
 assert next(r for r in result['resolved'] if r['stableId']==B)['scope']=='global'
 goldens[unit['id']]=result
 variants['locks'][unit['id']]={'noncanonicalBytesHex':(b' '+bytes.fromhex(result['lockBytesHex'])).hex(),'wrongPreimageSha256':'0'*64}
 prior=None
 if state=='upgrade':
  px=copy.deepcopy(prior_inputs);px['platform']=request['platform'];previous=M.solve(prior_bundle,px,prior_host);assert previous['status']=='ACCEPT',previous
  prior={'resolutionInputs':px,'lockBytesHex':previous['lockBytesHex'],'lockPreimageSha256':previous['lockPreimageSha256'],'historicalCatalogFloor':8,'currentCatalogFloor':9,'use':'retained prior operation only; not permission to dispatch under stale trust'}
 for cls in classes:
  cid=unit['id']+'/'+cls;expected='RJ-4 DIGEST_MISMATCH' if cls=='TC-SIG.C-LOCK' else 'RJ-4 ENVELOPE_MISMATCH' if cls=='TC-SIG.C-ENVELOPE' else 'ACCEPT'
  case={'id':cid,'unit':unit['id'],'class':cls,'resolutionInputs':request,'environment':{'platform':request['platform'],'state':state,'network':'DENIED','ambientPath':False,'priorSelection':prior},'expected':expected,'golden':unit['id']};cases.append(case)
  unit['members'][cls]={'definition':cls,'producerRequired':unit['members'][cls]['producerRequired'],'standing':'CONCRETE-DESIGN-INPUT-NOT-PRODUCT-RUN','requiredProductResult':'NOT-EXECUTED','designInput':{'path':'docs/coop/completion/g15-conditional-cases.v1.json','selector':'/cases/'+str(len(cases)-1)},'expectedDesign':expected}
source_names=['qualification-design-packaging.v1.json','qualification-design-schema-join.v1.json','manifest-freeze.completed.v1.json','compatibility-selection-freeze.v3.json','security_unit_lib_v2.py','security-schemas.v2/catalog.schema.json','security-schemas.v2/registry.schema.json','security-schemas.v2/registry-view.schema.json','security-schemas.v2/envelope.schema.json','security-schemas.v2/root.schema.json','security-schemas.v2/revocation.schema.json','compatibility-matrix.completed.v4.json','compatibility-selection-model.v3.py','compatibility-selection-cases.v3.json','compatibility-selection-report.v3.json','component-lock-schema.completed.v2.json','check_manifest_completed_v1.py','manifest-schema.completed.v1.json','check_compatibility_design_v2.py','version-constraint-schema.completed.v2.json','check_qualification_design.py','security-schemas.v2/permission-policy.schema.json','manifest-bases.completed.v1.json','manifest-artifact-blobs.completed.v1.json','security-fixtures.v2/root.example.json','security-fixtures.v2/catalog.example.json','security-fixtures.v2/revocation.example.json','security-fixtures.v2/registry.example.json','security-fixtures.v2/permission-policy.example.json']
dump('g15-conditional-cases.v1.json',{'status':'PROPOSED-DESIGN-EVIDENCE','sourcePins':{str((P/n).relative_to(ROOT)):sha((P/n).read_bytes()) for n in source_names},'cases':cases,'supplementary':['stale-signed-catalog','forged-view-recomputed-pin','cross-project-view','project-beta-positive','wrong-catalog-pin','wrong-registry-pin','missing-registry-pin','wrong-lock-serialization','wrong-lock-preimage','missing-artifact','forged-manifest','wrong-scope-install','permission-policy-mismatch','compatibility-policy-mismatch']})
dump('g15-conditional-variants.v1.json',variants);dump('g15-conditional-goldens.v1.json',goldens);dump('g15-conditional-matrix.v1.json',{'status':'PROPOSED-DESIGN-INPUT-COMPLETENESS-NOT-QUALIFICATION','matrix':matrix,'coverage':{'reports':12,'keysPerReport':80,'allSlots':960,'newConditionalSlots':60,'inheritedConcreteSlots':900,'productRuns':0}})
print('Authored',len(cases),'conditional slots and',len(matrix)*80,'matrix slots')
