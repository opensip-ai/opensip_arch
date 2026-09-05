#!/usr/bin/env python3
"""Author retained structural manifest design evidence; does not admit a release."""
import copy,hashlib,json
from pathlib import Path
P=Path(__file__).resolve().parent; ROOT=P.parents[2]
def write(n,v): (P/n).write_text(json.dumps(v,indent=2,ensure_ascii=True)+'\n')
def obj(p,r=None):return {'type':'object','properties':p,'required':list(p) if r is None else r,'additionalProperties':False}
def arr(item,**kw):return {'type':'array','items':item,**kw}
def ref(n):return {'$ref':'#/$defs/'+n}
S={'type':'string'};TEXT={'type':'string','minLength':1};UINT={'type':'integer','minimum':0,'maximum':9223372036854775807};POS={**UINT,'minimum':1};BOOL={'type':'boolean'}
NAME={'type':'string','pattern':'^[a-z0-9-]+(?![\\s\\S])'};FIELD={'type':'string','pattern':'^[a-z][a-zA-Z0-9_]*(?![\\s\\S])'}
UUID={'type':'string','pattern':'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}(?![\\s\\S])'}
HEX={'type':'string','pattern':'^[0-9a-f]{64}(?![\\s\\S])'};PATH={**TEXT,'x-maxUtf8Bytes':1024}
V=json.loads((P/'version-constraint-schema.completed.v2.json').read_text());V.pop('$id');V.pop('$schema');SEM=V['oneOf'][0]
D={};D['versionConstraint']=V;D['path']=PATH
D['reference']=obj({'path':ref('path'),'sha256':HEX});D['absence']=obj({'absent':{'const':True},'exceptionApprovalRef':TEXT,'typedAbsenceBehavior':{'enum':['RJ-'+str(n) for n in range(1,7)]}})
D['declaration']={'oneOf':[ref('reference'),ref('absence')]}
D['entry']={'oneOf':[obj({'path':ref('path'),'type':{'const':'file'},'mode':{'type':'string','pattern':'^0[0-7]{3}(?![\\s\\S])'},'length':UINT,'sha256':HEX}),obj({'path':ref('path'),'type':{'const':'dir'},'mode':{'type':'string','pattern':'^0[0-7]{3}(?![\\s\\S])'}}),obj({'path':ref('path'),'type':{'const':'symlink'},'mode':{'type':'string','pattern':'^0[0-7]{3}(?![\\s\\S])'},'target':ref('path')})]}
D['platform']=obj({'os':TEXT,'arch':TEXT,'tree':obj({'entries':arr(ref('entry'),minItems=1,maxItems=100000)}),'entrypoint':ref('path')})
D['option']=obj({'flag':{'type':'string','pattern':'^--[a-z][a-z0-9-]*(?![\\s\\S])'},'description':S,'valueKind':{'enum':['string','integer','boolean','path']},'repeatable':BOOL,'default':{'type':['string','integer','boolean','array']}},['flag','description','valueKind','repeatable'])
D['arg']=obj({'name':NAME,'description':S,'required':BOOL,'variadic':BOOL})
D['command']=obj({'name':NAME,'description':S,'aliases':arr(NAME,uniqueItems=True,maxItems=64),'parent':NAME,'visibility':{'enum':['public','internal']},'options':arr(ref('option')),'args':arr(ref('arg')),'scope':{'enum':['project','none']},'outputModes':arr({'enum':['human','json','sarif']},minItems=1,uniqueItems=True)},['name','description'])
REG={'typescript.imports':('imports','resolved-target'),'typescript.references':('references','resolved-binding'),'typescript.calls':('calls','resolved-callee'),'typescript.types':('types','checked'),'typescript.reachability':('reachability','from-resolved-calls')}
D['capability']={'oneOf':[obj({'capabilityId':{'const':k},'roleSubprotocol':{'const':'typescript'},'subprotocolVersion':{'const':1},'declarationData':obj({'relation':{'const':v[0]},'rung':{'const':v[1]}})}) for k,v in REG.items()]}
D['dependency']=obj({'stableId':UUID,'versionConstraint':ref('versionConstraint'),'reason':TEXT})
D['prerequisite']=obj({k:({'enum':['RJ-'+str(n) for n in range(1,7)]} if k.startswith('typed') else ref('path') if k=='doctorContract' else TEXT) for k in ['exceptionApprovalRef','ownership','trust','network','prerequisiteExpectations','doctorContract','typedAbsenceBehavior','typedFailureBehavior']})
D['configNode']={'oneOf':[obj({'type':{'const':'object'},'properties':{'type':'object','propertyNames':FIELD,'additionalProperties':ref('configNode')},'required':arr(FIELD,uniqueItems=True),'additionalProperties':{'const':False}}),obj({'type':{'const':'array'},'items':ref('configNode'),'minItems':UINT,'maxItems':UINT},['type','items']),obj({'type':{'const':'string'},'minLength':UINT,'maxLength':UINT,'enum':arr(S,minItems=1,uniqueItems=True)},['type']),obj({'type':{'const':'integer'},'minimum':{'type':'integer','minimum':-9223372036854775808,'maximum':9223372036854775807},'maximum':{'type':'integer','minimum':-9223372036854775808,'maximum':9223372036854775807}},['type']),obj({'type':{'enum':['boolean','null']}})]}
D['configuration']=obj({'namespace':NAME,'schema':ref('configNode'),'classifications':{'type':'object','propertyNames':FIELD,'additionalProperties':{'enum':['host.analysis.semantic','host.operability.nonsemantic']}}})
PERMS=['PT-FS-READ-PROJECT','PT-FS-READ-COMPONENT','PT-FS-WRITE-HOST-STATE','PT-PROC-EXEC-DECLARED','PT-NET-EGRESS','PT-ENV-READ','PT-HOST-EFFECT-BROKERED']
props={'manifestSchemaVersion':POS,'kind':{'const':'component'},'stableId':UUID,'name':NAME,'displayName':S,'aliases':arr(NAME,uniqueItems=True,maxItems=64),'version':SEM,'role':{'const':'analyzer'},'commands':arr(ref('command'),minItems=1,maxItems=4096),'capabilities':arr(ref('capability')),'platforms':arr(ref('platform'),minItems=1),'dependencies':arr(ref('dependency')),'prerequisites':arr(ref('prerequisite')),'declarations':obj({k:ref('declaration') for k in ['licenses','sbom','attestation','platformQualification','capabilityParityEvidence','performanceBaseline']}),'permissions':arr(obj({'permission':{'enum':PERMS},'reason':TEXT})),'configuration':ref('configuration'),'provenance':obj({'publisher':TEXT,'sourceClass':{'enum':['first-party','explicitly-trusted']}}),'stateMigration':{'const':{'reserved':True,'ridesOn':['DR-124','DR-106','DR-109','DR-113']}},'updateData':{'const':{'reserved':True,'ridesOn':['DR-110','DR-112']}},'compatibility':obj({'manifest':POS,'hostCore':ref('versionConstraint'),'control':POS,'providerProtocol':POS,'componentState':POS})}
SC={'$schema':'https://json-schema.org/draft/2020-12/schema','$id':'urn:opensip:completion:manifest:1','$comment':'Proposed closed structural manifest schema; cross-field/path/ref/host-policy checks are mandatory separate phases. No signature or product admission claim.',**obj(props,[k for k in props if k not in ['displayName','aliases','prerequisites','configuration']]),'$defs':D}
write('manifest-schema.completed.v1.json',SC)
full=json.loads((P/'security-fixtures.v2/typescript-analyzer.manifest.json').read_text());bases={'security-full':full}
minimal=copy.deepcopy(full);minimal['capabilities']=[];minimal['permissions']=[];minimal['platforms']=minimal['platforms'][:1];minimal.pop('displayName');bases['empty-capability']=minimal
maximum=copy.deepcopy(full);maximum['aliases']=['ts-analyzer'];maximum['commands'][0].update({'aliases':['tsa'],'visibility':'public','options':[{'flag':'--quiet','description':'Quiet','valueKind':'boolean','repeatable':False,'default':False}],'args':[{'name':'path','description':'Source path','required':False,'variadic':False}],'scope':'project','outputModes':['human','json','sarif']});maximum['commands'].append({'name':'inspect','parent':full['name'],'description':'Metadata inspection','visibility':'internal','scope':'none'});maximum['dependencies']=[{'stableId':'11111111-1111-4111-8111-111111111111','versionConstraint':'1.2.3-rc.1+build','reason':'Declared fixture dependency'}];maximum['configuration']={'namespace':full['name'],'schema':{'type':'object','properties':{'strictness':{'type':'boolean'},'display':{'type':'object','properties':{'color':{'type':'boolean'}},'required':[],'additionalProperties':False}},'required':['strictness'],'additionalProperties':False},'classifications':{'strictness':'host.analysis.semantic','display':'host.operability.nonsemantic'}};bases['maximal']=maximum
exception=copy.deepcopy(minimal);exception['prerequisites']=[{'exceptionApprovalRef':'CD-DR119-EXCEPTION-FIXTURE','ownership':'customer-owned fixture','trust':'explicit fixture authority','network':'none','prerequisiteExpectations':'customer-owned fixture service','doctorContract':'doctor/external-system.json','typedAbsenceBehavior':'RJ-5','typedFailureBehavior':'RJ-5'}];exception['declarations']['licenses']={'absent':True,'exceptionApprovalRef':'CD-DR119-EXCEPTION-FIXTURE','typedAbsenceBehavior':'RJ-5'};bases['approved-exception']=exception
# Complete synthetic bytes for reference checking; never claims shipping executables.
closure=copy.deepcopy(full);blobs={}
def blob(data):
 h=hashlib.sha256(data).hexdigest();blobs[h]=data.hex();return h
for platform in closure['platforms']:
 for e in platform['tree']['entries']:
  if e['type']=='file':
   data=('DESIGN-FIXTURE-ONLY '+e['path']+'\n').encode();e['length']=len(data);e['sha256']=blob(data)
notice=blob(b'Design fixture notice; no shipping product claim.\n')
for kind in closure['declarations']:
 value={'kind':kind,'designEvidenceOnly':True}
 if kind=='licenses':value.update({'licenseInventory':['Fixture-License'],'noticeInventory':[{'path':'notices/fixture.txt','sha256':notice}]})
 data=(json.dumps(value,sort_keys=True,separators=(',',':'))+'\n').encode();closure['declarations'][kind]['sha256']=blob(data)
bases['artifact-closure']=closure
write('manifest-bases.completed.v1.json',bases);write('manifest-artifact-blobs.completed.v1.json',blobs)
cases=[]
def case(i,base='security-full',ops=None,want='ACCEPT',context=None,**kw):cases.append({'id':i,'base':base,'operations':ops or [],'context':context or {},'expected':want,**kw})
def setv(path,value):return {'op':'set','path':path,'value':value}
def delete(path):return {'op':'delete','path':path}
def append(path,value):return {'op':'append','path':path,'value':value}
case('POS/full-security');case('POS/empty-capabilities','empty-capability');case('POS/maximal','maximal',context={'hostClassificationMap':maximum['configuration']['classifications']});case('POS/approved-exception','approved-exception',context={'approvedExceptions':['CD-DR119-EXCEPTION-FIXTURE']});case('POS/full-artifact-closure','artifact-closure',context={'verifyArtifacts':True})
case('POS/open-platform',ops=[setv(['platforms',0,'os'],'future-os'),setv(['platforms',0,'arch'],'future-arch')]);case('PROFILE/open-platform',ops=[setv(['platforms',0,'os'],'future-os')],want='RJ-6',context={'previewProfile':True});case('POS/preview-profile',context={'previewProfile':True})
# Every required top-level member and every direct closed object boundary.
for key in SC['required']:case('REQUIRED/'+key,ops=[delete([key])],want='RJ-6')
walk_targets=[[],['commands',0],['capabilities',0],['capabilities',0,'declarationData'],['platforms',0],['platforms',0,'tree'],['platforms',0,'tree','entries',0],['platforms',0,'tree','entries',1],['declarations'],['declarations','sbom'],['permissions',0],['provenance'],['compatibility'],['compatibility','hostCore']]
for path in walk_targets:case('CLOSED/'+('/'.join(map(str,path)) or 'root'),ops=[setv(path+['unknown'],True)],want='RJ-6')
for name,path,val in [('role',['role'],'builder'),('permission',['permissions',0,'permission'],'PT-INVENTED'),('capability',['capabilities',0,'capabilityId'],'typescript.parse-fidelity'),('rung',['capabilities',0,'declarationData','rung'],'checked'),('uuid',['stableId'],'UPPER-INVALID'),('version',['version'],'01.0.0'),('integer-bool',['manifestSchemaVersion'],True),('kind',['kind'],'tool'),('state-marker',['stateMigration','reserved'],False),('update-marker',['updateData','ridesOn'],[]),('dir-file-branch',['platforms',0,'tree','entries',0,'length'],1),('file-symlink-branch',['platforms',0,'tree','entries',1,'target'],'bin/entry'),('platform-empty',['platforms'],[]),('missing-cap-array',['capabilities'],None),('compat-field',['compatibility','control'],'1'),('float',['platforms',0,'tree','entries',1,'length'],1.0)]:case('TYPE/'+name,ops=[setv(path,val)],want='RJ-6')
for key in ['licenses','sbom','attestation','platformQualification','capabilityParityEvidence','performanceBaseline']:case('DECL/missing-'+key,ops=[delete(['declarations',key])],want='RJ-6')
for name,path in [('up','../entry'),('dot','bin/./entry'),('absolute','/entry'),('drive','C:/entry'),('backslash','bin\\entry'),('nul','bin/\0entry'),('empty-segment','bin//entry'),('nfc','bin/e\u0301'),('reserved','bin/CON.txt'),('trailing-dot','bin/entry.'),('trailing-space','bin/entry ')]:case('PATH/'+name,ops=[setv(['platforms',0,'tree','entries',1,'path'],path)],want='RJ-3')
case('PATH/non-ascii-1024',ops=[append(['platforms',0,'tree','entries'],{'path':'é'*512,'type':'dir','mode':'0755'})]);case('PATH/non-ascii-1026',ops=[append(['platforms',0,'tree','entries'],{'path':'é'*513,'type':'dir','mode':'0755'})],want='RJ-3')
for name,path in [('case','BIN'),('exact','bin')]:case('PATH/duplicate-'+name,ops=[append(['platforms',0,'tree','entries'],{'path':path,'type':'dir','mode':'0755'})],want='RJ-3')
case('PATH/missing-parent',ops=[append(['platforms',0,'tree','entries'],{'path':'missing/child','type':'dir','mode':'0755'})],want='RJ-3');case('PATH/file-parent',ops=[append(['platforms',0,'tree','entries'],{'path':'bin/entry/child','type':'dir','mode':'0755'})],want='RJ-3');case('PATH/missing-entrypoint',ops=[setv(['platforms',0,'entrypoint'],'bin/missing')],want='RJ-3')
symlink={'path':'bin/link','type':'symlink','mode':'0777','target':'entry'}
case('POS/symlink',ops=[append(['platforms',0,'tree','entries'],symlink)]);case('PATH/symlink-escape',ops=[append(['platforms',0,'tree','entries'],{**symlink,'target':'../entry'})],want='RJ-3');case('PATH/symlink-missing',ops=[append(['platforms',0,'tree','entries'],{**symlink,'target':'absent'})],want='RJ-3');case('PATH/symlink-cycle',ops=[append(['platforms',0,'tree','entries'],{**symlink,'target':'link'})],want='RJ-3')
case('TREE/dir-as-entrypoint',ops=[setv(['platforms',0,'entrypoint'],'bin')],want='RJ-3');case('TREE/non-executable-entrypoint',ops=[setv(['platforms',0,'tree','entries',1,'mode'],'0644')],want='RJ-3')
for name,ops in [('zero-root',[setv(['commands',0,'parent'],full['name'])]),('two-root',[append(['commands'],{'name':'second','description':'Second'})]),('root-name',[setv(['commands',0,'name'],'different')]),('unknown-parent',[append(['commands'],{'name':'child','parent':'missing','description':'Child'})]),('self-parent',[append(['commands'],{'name':'child','parent':'child','description':'Child'})]),('duplicate-pair',[append(['commands'],{'name':full['name'],'description':'Duplicate'})]),('alias-shadow',[setv(['aliases'],[full['name']])]),('reserved',[setv(['name'],'analyze'),setv(['commands',0,'name'],'analyze')])]:case('COMMAND/'+name,ops=ops,want='RJ-2',context={'reservedNames':['analyze']})
case('COMMAND/cycle',ops=[append(['commands'],{'name':'a','parent':'b','description':'A'}),append(['commands'],{'name':'b','parent':'a','description':'B'})],want='RJ-2')
for depth in [32,33]:
 commands=[{'name':full['name'],'description':'Root'}]+[{'name':'d'+str(i),'parent':full['name'] if i==1 else 'd'+str(i-1),'description':'Depth'} for i in range(1,depth)]
 case('LIMIT/command-depth-'+str(depth),ops=[setv(['commands'],commands)],want='ACCEPT' if depth==32 else 'RJ-6')
case('COMMAND/option-default','maximal',[setv(['commands',0,'options',0,'default'],'wrong')],want='RJ-6',context={'hostClassificationMap':maximum['configuration']['classifications']})
case('COMMAND/arg-after-variadic','maximal',[setv(['commands',0,'args'],[{'name':'a','description':'a','required':False,'variadic':True},{'name':'b','description':'b','required':False,'variadic':False}])],want='RJ-6',context={'hostClassificationMap':maximum['configuration']['classifications']})
case('CONFIG/no-host-review','maximal',want='RJ-6');case('CONFIG/wrong-host-classification','maximal',context={'hostClassificationMap':{'strictness':'host.operability.nonsemantic','display':'host.operability.nonsemantic'}},want='RJ-6')
for name,path,val in [('namespace',['configuration','namespace'],'other'),('unknown-token',['configuration','classifications','strictness'],'my-token'),('unclosed',['configuration','schema','additionalProperties'],True),('hidden-ref',['configuration','schema','$ref'],'https://example.invalid/schema'),('missing-map',['configuration','classifications'],{}),('undeclared-required',['configuration','schema','required'],['absent'])]:case('CONFIG/'+name,'maximal',[setv(path,val)],want='RJ-6',context={'hostClassificationMap':maximum['configuration']['classifications']})
case('EXCEPTION/no-approval','approved-exception',want='RJ-6');case('EXCEPTION/no-prerequisite','approved-exception',[delete(['prerequisites'])],want='RJ-6',context={'approvedExceptions':['CD-DR119-EXCEPTION-FIXTURE']});case('EXCEPTION/mixed-ref-absence','approved-exception',[setv(['declarations','licenses','path'],'licenses')],want='RJ-6',context={'approvedExceptions':['CD-DR119-EXCEPTION-FIXTURE']})
case('CAP/duplicate',ops=[append(['capabilities'],full['capabilities'][0])],want='RJ-6');case('CAP/reachability-without-calls',ops=[setv(['capabilities'],[full['capabilities'][-1]])],want='RJ-6')
case('COMPAT/reversed-interval',ops=[setv(['compatibility','hostCore','min'],'0.3.0')],want='RJ-6');case('COMPAT/manifest-mismatch',ops=[setv(['compatibility','manifest'],2)],want='RJ-6');case('COMPAT/independent-state',ops=[setv(['compatibility','componentState'],2)]);case('COMPAT/unsupported-state-profile',ops=[setv(['compatibility','componentState'],2)],want='RJ-6',context={'previewProfile':True})
case('REF/digest-mismatch','artifact-closure',[setv(['declarations','sbom','sha256'],'0'*64)],want='RJ-4',context={'verifyArtifacts':True});case('REF/tree-digest-mismatch','artifact-closure',[setv(['platforms',0,'tree','entries',1,'length'],999)],want='RJ-4',context={'verifyArtifacts':True});case('REF/path-traversal',ops=[setv(['declarations','sbom','path'],'../sbom.json')],want='RJ-3');case('REF/missing-release-artifact','artifact-closure',want='RJ-4',context={'verifyArtifacts':True,'missingArtifacts':['declarations/sbom.json']})
case('LEX/duplicate-key',want='RJ-6',wireRecipe={'kind':'duplicate','key':'kind'});case('LEX/deep-65',want='RJ-6',wireRecipe={'kind':'nested','depth':65});case('LEX/huge-integer',want='RJ-6',wireRecipe={'kind':'huge-int','digits':5000});case('LIMIT/bytes-exact',wireRecipe={'kind':'padding','bytes':4194304});case('LIMIT/bytes-over',want='RJ-6',wireRecipe={'kind':'padding','bytes':4194305})
for n in [64,65]:case('LIMIT/aliases-'+str(n),ops=[setv(['aliases'],['alias'+str(i) for i in range(n)])],want='ACCEPT' if n==64 else 'RJ-6')
# Closed optional shapes and exact resource boundaries beyond the root sweep.
for path in [['commands',0,'options',0],['commands',0,'args',0],['dependencies',0],['configuration'],['configuration','schema'],['configuration','schema','properties','strictness']]:case('OPTIONAL-CLOSED/'+('/'.join(map(str,path))),'maximal',[setv(path+['unknown'],True)],want='RJ-6',context={'hostClassificationMap':maximum['configuration']['classifications']})
for path in [['prerequisites',0],['declarations','licenses']]:case('EXCEPTION-CLOSED/'+('/'.join(map(str,path))),'approved-exception',[setv(path+['unknown'],True)],want='RJ-6',context={'approvedExceptions':['CD-DR119-EXCEPTION-FIXTURE']})
for n in [1024,1025]:case('PATH/ascii-'+str(n),ops=[append(['platforms',0,'tree','entries'],{'path':'a'*n,'type':'dir','mode':'0755'})],want='ACCEPT' if n==1024 else 'RJ-3')
for n in [4096,4097]:
 commands=[{'name':full['name'],'description':'Root'}]+[{'name':'c'+str(i),'parent':full['name'],'description':'Child'} for i in range(1,n)]
 case('LIMIT/commands-'+str(n),ops=[setv(['commands'],commands)],want='ACCEPT' if n==4096 else 'RJ-6')
# Depth definition counts JSON object/array containers, including manifest root.
for target in [64,65]:
 node={'type':'boolean'}
 for _ in range(target-5):node={'type':'array','items':node}
 configuration={'namespace':full['name'],'schema':{'type':'object','properties':{'value':node},'required':[],'additionalProperties':False},'classifications':{'value':'host.analysis.semantic'}}
 case('LIMIT/valid-config-depth-'+str(target),ops=[setv(['configuration'],configuration)],context={'hostClassificationMap':configuration['classifications']},want='ACCEPT' if target==64 else 'RJ-6')
empty_config={'namespace':full['name'],'schema':{'type':'object','properties':{},'required':[],'additionalProperties':False},'classifications':{}}
case('POS/preview-empty-configuration',ops=[setv(['configuration'],empty_config)],context={'previewProfile':True})
case('PROFILE/nonempty-synthetic-configuration','maximal',context={'previewProfile':True,'hostClassificationMap':maximum['configuration']['classifications']},want='RJ-6')
case('TYPE/surrogate',ops=[setv(['displayName'],'\ud800')],want='RJ-6')
case('TYPE/huge-safe-integer-overflow',ops=[setv(['manifestSchemaVersion'],2**63)],want='RJ-6')
case('DEPENDENCY/duplicate','maximal',[append(['dependencies'],maximum['dependencies'][0])],want='RJ-6',context={'hostClassificationMap':maximum['configuration']['classifications']})
case('DEPENDENCY/self','maximal',[setv(['dependencies',0,'stableId'],full['stableId'])],want='RJ-6',context={'hostClassificationMap':maximum['configuration']['classifications']})
case('PERMISSION/duplicate',ops=[append(['permissions'],full['permissions'][0])],want='RJ-6')
case('PLATFORM/duplicate',ops=[append(['platforms'],full['platforms'][0])],want='RJ-6')
case('TREE/symlink-unknown-branch',ops=[append(['platforms',0,'tree','entries'],{**symlink,'sha256':'0'*64})],want='RJ-6')
case('EXCEPTION/doctor-path','approved-exception',[setv(['prerequisites',0,'doctorContract'],'../doctor')],want='RJ-3',context={'approvedExceptions':['CD-DR119-EXCEPTION-FIXTURE']})
case('CUSTODY/same-owner-name',context={'liveNames':[{'stableId':full['stableId'],'provenance':full['provenance'],'names':[full['name']]}]})
case('CUSTODY/different-owner-name',context={'liveNames':[{'stableId':'11111111-1111-4111-8111-111111111111','provenance':full['provenance'],'names':[full['name']]}]},want='RJ-2')
for case_value in cases:
 if case_value['id']=='LEX/duplicate-key':case_value['expectedDatum']='DUPLICATE_JSON_KEY:kind'
 if case_value['id'] in ['LEX/deep-65','LIMIT/valid-config-depth-65']:case_value['expectedDatum']='JSON_DEPTH_LIMIT'
 if case_value['id']=='LIMIT/bytes-over':case_value['expectedDatum']='MANIFEST_BYTE_LIMIT'
for path in [['commands',0],['capabilities',0],['capabilities',0,'declarationData'],['platforms',0],['platforms',0,'tree'],['platforms',0,'tree','entries',0],['platforms',0,'tree','entries',1],['declarations','sbom'],['permissions',0],['provenance'],['compatibility']]:
 node=full
 for key in path:node=node[key]
 for key in node:case('NESTED-REQUIRED/'+('/'.join(map(str,path+[key]))),ops=[delete(path+[key])],want='RJ-6')
write('manifest-cases.completed.v1.json',{'status':'PROPOSED-DESIGN-EVIDENCE','cases':cases,'sourcePins':{str(q.relative_to(ROOT)):hashlib.sha256(q.read_bytes()).hexdigest() for q in [ROOT/'docs/coop/artifacts/component-manifest-schemas.v11.json',ROOT/'docs/coop/artifacts/permission-truth-tables.v9.json',P/'version-constraint-schema.completed.v2.json',P/'security-fixtures.v2/typescript-analyzer.manifest.json']}})
print('Authored',len(cases),'manifest cases')
