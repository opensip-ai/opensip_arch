#!/usr/bin/env python3
"""Actual metadata custody join around reviewed v3 selection; design evidence only."""
import copy,datetime,hashlib,importlib.util,json
from pathlib import Path
from jsonschema import Draft202012Validator
P=Path(__file__).resolve().parent

def module(name,path):
 s=importlib.util.spec_from_file_location(name,P/path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
CORE=module('g15_selection_core','compatibility-selection-model.v3.py')
SEC=module('g15_security','security_unit_lib_v2.py')
MAN=module('g15_manifest','check_manifest_completed_v1.py')
ARCH=module('g15_archive','check_qualification_design.py')
LOCK_SCHEMA=json.loads((P/'component-lock-schema.completed.v3.json').read_text())
INPUT=Draft202012Validator(LOCK_SCHEMA['properties']['resolutionInputs']);LOCK=Draft202012Validator(LOCK_SCHEMA)
REGISTRY_DOMAIN='opensip.metadata.registry.1';VIEW_DOMAIN='opensip.metadata.registry-view.1';LOCK_DOMAIN='opensip.metadata.lock.1'
class Failure(Exception):
 def __init__(self,reason):self.reason=reason

def require(ok,reason):
 if not ok:raise Failure(reason)
def sha(b):return hashlib.sha256(b).hexdigest()
def digest(domain,obj):return SEC.domain_digest(domain,obj)[0]
def schema(obj,name):
 require(Draft202012Validator(json.loads((P/('security-schemas.v2/'+name+'.schema.json')).read_text())).is_valid(obj),'SCHEMA-'+name)
def read(bundle,key):
 require(key in bundle['documents'],'MISSING-DOCUMENT:'+key)
 raw=bytes.fromhex(bundle['documents'][key]);return raw,SEC.load_json_strict(raw)
def envelope(bundle,key,root,kind,publisher='opensip'):
 raw,obj=read(bundle,key);_,env=read(bundle,key+'.envelope');outcome,_=SEC.verify_envelope(raw,env,root,kind,publisher)
 require(outcome=='VERIFIED',outcome);return raw,obj,env

def export_view(store,scope,exported_at):
 entries=[]
 for e in store['entries']:
  if e['scope'] not in scope['allowedScopes']:continue
  if e['scope']=='project' and e['projectKey']!=scope['projectKey']:continue
  entries.append(copy.deepcopy(e))
 live={'active','deprecated-alias-window'}
 for e in entries:
  e['shadowedBy']=None
  if e['scope']=='global' and e['status'] in live:
   matches=[p for p in entries if p['scope']=='project' and p['status'] in live and all(p[k]==e[k] for k in ['stableId','provenance','version'])]
   require(len(matches)<=1,'AMBIGUOUS-PROJECT-SHADOW')
   if matches:e['shadowedBy']={k:matches[0][k] for k in ['stableId','version','scope']}
 entries.sort(key=lambda e:(e['stableId'],e['version'],0 if e['scope']=='project' else 1,e['projectKey'] or ''))
 return {'registryViewSchema':1,'installId':store['installId'],'sourceStoreDigest':digest(REGISTRY_DOMAIN,store),'scopeContext':copy.deepcopy(scope),'exportedAt':exported_at,'entries':entries,'retiredIds':copy.deepcopy(store['retiredIds']),'reservedRootCommands':copy.deepcopy(store['reservedRootCommands']),'trustMetadata':copy.deepcopy(store['trustMetadata'])}

def verified_artifacts(bundle,manifest,platform):
 sid=manifest['stableId'];files=bundle['artifacts'].get(sid,{})
 def exact(path,expected):
  require(path in files,'RJ-4 MISSING-ARTIFACT:'+path);data=bytes.fromhex(files[path]);require(sha(data)==expected,'RJ-4 DIGEST_MISMATCH');return data
 # Every platform's committed tree is verified; the selected archive is decoded.
 for plat in manifest['platforms']:
  for entry in plat['tree']['entries']:
   if entry['type']=='file':require(len(exact(entry['path'],entry['sha256']))==entry['length'],'RJ-4 LENGTH_MISMATCH')
 for name,ref in manifest['declarations'].items():
  require('path' in ref,'FIXTURE-REQUIRES-DECLARED-EVIDENCE')
  data=exact(ref['path'],ref['sha256'])
  if name=='licenses':
   value=SEC.load_json_strict(data);require(isinstance(value.get('licenseInventory'),list) and isinstance(value.get('noticeInventory'),list),'LICENSE-INVENTORY')
   for notice in value['noticeInventory']:MAN.path_ok(notice['path']);exact(notice['path'],notice['sha256'])
 matching=[p for p in manifest['platforms'] if {k:p[k] for k in ['os','arch']}==platform];require(len(matching)==1,'PLATFORM-UNAVAILABLE')
 plat=matching[0];name='archive.'+platform['os']+'-'+platform['arch']+'.tar';require(name in files,'MISSING-ARCHIVE')
 tree=[]
 for e in plat['tree']['entries']:
  row={**e,'mode':int(e['mode'],8)}
  if e['type']=='file':row['bodyHex']=files[e['path']]
  tree.append(row)
 require(ARCH.admit_archive(bytes.fromhex(files[name]),tree)=='ACCEPT','ARCHIVE-PROFILE')
 wanted={'manifest.json','envelope.json',name}
 for e in plat['tree']['entries']:
  if e['type']=='file':wanted.add(e['path'])
 for key,ref in manifest['declarations'].items():
  wanted.add(ref['path'])
  if key=='licenses':wanted.update(x['path'] for x in SEC.load_json_strict(bytes.fromhex(files[ref['path']]))['noticeInventory'])
 require(wanted<=set(files),'MISSING-ARTIFACT')
 return len(plat['tree']['entries']),[{'artifact':name,'sha256':sha(bytes.fromhex(files[name]))} for name in sorted(wanted)]

def solve(bundle,x,host):
 """Host context is external trusted snapshot custody, never read from a lock."""
 try:
  require(INPUT.is_valid(x),'INPUT-SCHEMA')
  scope=x['scopeContext'];require(scope['allowedScopes'] in [['global'],['project','global']] and (scope['projectKey'] is None)==('project' not in scope['allowedScopes']),'SCOPE-CONTEXT')
  policy_raw,policy=read(bundle,'permission-policy');schema(policy,'permission-policy');compat_raw,_=read(bundle,'compatibility-policy')
  require(digest(SEC.DOMAIN_TAGS['policy'],policy)==x['permissionPolicyDigest']==host['permissionPolicyDigest'],'PERMISSION-POLICY-CUSTODY')
  require(sha(compat_raw)==x['compatibilityPolicyDigest']==host['compatibilityPolicyDigest'],'COMPATIBILITY-POLICY-CUSTODY')
  root_raw,root=read(bundle,'root');schema(root,'root');require(sha(root_raw)==host['trustedRootStoredSha256'],'ROOT-ANCHOR')
  now=host['now'];require(root['issuedAt']<=now<root['expiresAt'],'ROOT-EXPIRED')
  envelope(bundle,'root',root,'root')
  _,rev,_=envelope(bundle,'revocation',root,'revocation');schema(rev,'revocation')
  require(rev['rootVersion']==root['rootVersion'] and rev['revocationVersion']>=host['floors']['revocationVersion'] and rev['issuedAt']<=now,'REVOCATION-STALE')
  revoked={(e['subjectKind'],e['subject']) for e in rev['entries']}
  effective=copy.deepcopy(root)
  for role in effective['roles'].values():role['keys']=[k for k in role['keys'] if ('keyId',k) not in revoked]
  _,catalog,cat_env=envelope(bundle,'catalog',effective,'catalog');schema(catalog,'catalog')
  require(catalog['issuedAt']<=now<catalog['expiresAt'] and catalog['snapshotVersion']>=host['floors']['catalogSnapshotVersion'] and root['rootVersion']>=max(catalog['rootVersionRequired'],host['floors']['rootVersion']) and rev['revocationVersion']>=catalog['revocationVersionRequired'],'CATALOG-STALE')
  require(('catalogSnapshot',str(catalog['snapshotVersion'])) not in revoked and ('namespace','opensip') not in revoked,'CATALOG-REVOKED')
  require(x['indexDigest']==cat_env['subject']['preimageSha256'],'CATALOG-CUSTODY')
  _,store=read(bundle,'registry');schema(store,'registry')
  require(digest(REGISTRY_DOMAIN,store)==host['sourceStoreDigest'],'REGISTRY-STORE-CUSTODY')
  tuples=[(e['stableId'],e['version'],e['scope'],e['projectKey']) for e in store['entries']]
  require(len(tuples)==len(set(tuples)) and all((e['projectKey'] is None)==(e['scope']=='global') for e in store['entries']),'REGISTRY-SCOPE-KEYS')
  _,view=read(bundle,'view');schema(view,'registry-view')
  require(view['exportedAt']<=now,'REGISTRY-VIEW-FUTURE')
  require(view['scopeContext']==x['scopeContext'],'REGISTRY-SCOPE')
  require(view['sourceStoreDigest']==host['sourceStoreDigest'] and x['registryViewDigest']==digest(VIEW_DOMAIN,view),'REGISTRY-VIEW-CUSTODY')
  require(view==export_view(store,x['scopeContext'],view['exportedAt']),'REGISTRY-VIEW-FORGED')
  require(store['installId']==x['installId'] and store['trustMetadata']=={'rootVersion':root['rootVersion'],'catalogSnapshotVersion':catalog['snapshotVersion'],'revocationVersion':rev['revocationVersion']},'REGISTRY-TRUST-JOIN')
  require(store['reservedRootCommands']==catalog['reservedRootCommands'],'RESERVED-CATALOG-JOIN')
  releases=[];current={};catalog_ids=set()
  for release in catalog['releases']:
   key=(release['stableId'],release['publisher'],release['sourceClass'],release['version']);require(key not in catalog_ids,'DUPLICATE-CATALOG-RELEASE');catalog_ids.add(key)
  for e in view['entries']:
   if e['status'] not in ['active','deprecated-alias-window'] or e['shadowedBy'] is not None:continue
   require(not any(q['stableId']==e['stableId'] and q['provenance']!=e['provenance'] for q in store['retiredIds']),'RJ-1 RETIRED-IDENTITY')
   matches=[r for r in catalog['releases'] if r['stableId']==e['stableId'] and r['version']==e['version'] and (r['publisher'],r['sourceClass'])==(e['provenance']['publisher'],e['provenance']['sourceClass'])];require(len(matches)==1,'CATALOG-REGISTRY-RELEASE')
   release=matches[0];sid=e['stableId'];raw,m,env=envelope(bundle,'manifest/'+sid,effective,'manifest',e['provenance']['publisher'])
   MAN.validate(raw,{'previewProfile':True})
   require(all(m[k]==e[k] for k in ['stableId','version','provenance']),'MANIFEST-REGISTRY-IDENTITY')
   require(sha(raw)==e['manifestDigest']==release['manifestDigest'] and env['subject']['preimageSha256']==release['manifestPreimageSha256'],'MANIFEST-CUSTODY')
   env_raw,_=read(bundle,'manifest/'+sid+'.envelope')
   require(sha(env_raw)==e['signatureRef']==release['envelopeDigest'],'ENVELOPE-CUSTODY')
   require(e['catalogSnapshotVersion']==catalog['snapshotVersion'] and e['catalogPreimageSha256']==x['indexDigest'],'ADMISSION-CATALOG-CUSTODY')
   require(e['mountedRootCommand']==m['name'] and e['namesSnapshot']=={'name':m['name'],'aliases':m.get('aliases',[]),'mountedRootCommand':m['name']},'NAME-SNAPSHOT')
   require(bundle['artifacts'][sid]['manifest.json']==raw.hex() and bundle['artifacts'][sid]['envelope.json']==env_raw.hex(),'ARTIFACT-MANIFEST-CUSTODY')
   require(release['hostCoreConstraint']==m['compatibility']['hostCore'],'COMPATIBILITY-CATALOG-JOIN')
   count,artifacts=verified_artifacts(bundle,m,x['platform'])
   archive_name='archive.'+x['platform']['os']+'-'+x['platform']['arch']+'.tar';archive_sha=sha(bytes.fromhex(bundle['artifacts'][sid][archive_name]));matching=[a for a in release['artifacts'] if a['platform']==x['platform']['os']+'-'+x['platform']['arch']]
   require(len(matching)==1 and matching[0]['archiveProfileId']=='archive-profile.1' and matching[0]['archiveDigest']==archive_sha==matching[0]['sha256'],'CATALOG-ARCHIVE-CUSTODY')
   require(('release',sid+'@'+m['version']) not in revoked and ('namespace',m['provenance']['publisher']) not in revoked,'RELEASE-REVOKED')
   current.setdefault(sid,m['provenance']);require(current[sid]==m['provenance'],'CONFLICTING-PROVENANCE')
   ranges={k:[1,1] for k in ['coreState','root','index','manifest','lock','control','typescript','componentState']}
   releases.append({'stableId':sid,'version':m['version'],'scope':e['scope'],'projectKey':e['projectKey'],'provenance':m['provenance'],'manifestDigest':sha(raw),'admitted':True,'currentTrustPermits':True,'platforms':[{k:p[k] for k in ['os','arch']} for p in m['platforms']],'hostCoreConstraint':m['compatibility']['hostCore'],'surfaceRanges':ranges,'capabilities':[c['capabilityId'] for c in m['capabilities']],'dependencies':m['dependencies'],'platformTreeEntryCount':count,'artifactDigests':artifacts})
  # Private adapter input only: reviewed core still names its fixture observation
  # digest indexDigest. It never escapes as the external catalog custody pin.
  index={'custodyValid':True,'releases':releases,'currentProvenance':current};internal=copy.deepcopy(x);internal.pop('registryViewDigest');internal['indexDigest']=CORE.sha(CORE.fixture_bytes(index))
  result=CORE.solve({'resolutionInputs':internal,'index':index,'observedRequiredEdges':[]})
  require(result['status']=='ACCEPT','SELECTION:'+result.get('reason','UNKNOWN'))
  lock=result['referenceLock'];lock['resolutionInputs']=copy.deepcopy(x);require(LOCK.is_valid(lock),'LOCK-SCHEMA')
  raw=SEC.canonical_bytes(lock)
  return {'status':'ACCEPT','referenceLock':lock,'lockBytesHex':raw.hex(),'lockStoredSha256':sha(raw),'lockPreimageSha256':digest(LOCK_DOMAIN,lock),'resolved':result['resolved'],'admitted':False}
 except (Failure,MAN.Refuse,SEC.Reject) as e:return {'status':'REFUSE','reason':getattr(e,'reason',getattr(e,'code',str(e))),'resolved':[],'admitted':False}

def verify_lock_bytes(raw,expected_preimage,expected_inputs):
 try:
  lock=SEC.load_json_strict(raw);require(LOCK.is_valid(lock),'LOCK-SCHEMA');require(SEC.canonical_bytes(lock)==raw,'LOCK-NONCANONICAL');require(lock['resolutionInputs']==expected_inputs,'LOCK-INPUT-CUSTODY');require(digest(LOCK_DOMAIN,lock)==expected_preimage,'LOCK-DIGEST');return 'ACCEPT'
 except (Failure,SEC.Reject) as e:return getattr(e,'reason',str(e))

def verify_lock_artifacts(lock,bundle):
 for selected in lock['resolved']:
  files=bundle['artifacts'].get(selected['stableId'],{})
  for a in selected['artifactDigests']:
   if a['artifact'] not in files or sha(bytes.fromhex(files[a['artifact']]))!=a['sha256']:return 'RJ-4 DIGEST_MISMATCH'
 return 'ACCEPT'
