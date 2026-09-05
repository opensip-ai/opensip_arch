"""Author fixture inputs and independent expectations; never imports the model."""
import copy, hashlib, itertools, json
from pathlib import Path
P=Path(__file__).parent
A=P.parent/'artifacts'
SOURCES=['permission-truth-tables.v9','host-effect-authorization.v25','doctor-contract.v4','doctor-actor-join-integration-contract.v8','signed-index-trust-contract.v14']
TOKENS=['PT-FS-READ-PROJECT','PT-FS-READ-COMPONENT','PT-FS-WRITE-HOST-STATE','PT-PROC-EXEC-DECLARED','PT-NET-EGRESS','PT-ENV-READ','PT-HOST-EFFECT-BROKERED']
CASES=[]
def add(id,model,inp,expected,classes,source,selector,properties=[]):
 CASES.append(dict(id=id,model=model,input=inp,expected=expected,classes=classes,source=source,selector=selector,properties=properties))
p='permission-truth-tables.v9'
h='host-effect-authorization.v25';d='doctor-contract.v4';j='doctor-actor-join-integration-contract.v8';t='signed-index-trust-contract.v14'
for token in TOKENS+['filesystem','network','env','subprocess','pt-env-read','PT-ENV-READ ',' PT-ENV-READ','PT-ENV-REAḊ']:
 add('vocabulary-'+str(len(CASES)),'permission',dict(token=token,declared=TOKENS,denied=[],admission=True),{'decision':'GRANTED' if token in TOKENS else 'PR-3','wire':None},['FX-1'],p,'$.permissionVocabulary.tokens')
for token in TOKENS:
 for label,extra,expect,cl in [('absent',{'declared':[]},'PR-1','FX-2A'),('deny',{'denied':[token]},'PR-2','FX-2A'),('revoked',{'revoked':True},'PR-5','FX-8'),('consent',{'consentRequired':True,'consent':False,'interactive':False},'PR-7','FX-9'),('scope',{'scopeMatches':False},'PR-4','R-9'),('exclusive',{'exclusiveHeld':True},'PR-9','R-4')]:
  add(token+'-'+label,'permission',dict(token=token,declared=TOKENS,denied=[],**{} )|extra,{'decision':expect,'wire':'RF-6','hostIntentCount':0,'promptAttempts':0},[cl],p,'$.refusalFamilies.families')
add('env-exact-case','environment',{'host':{'A':'allowed','B':'secret','a':'case','AA':'near','LANG':'C'},'granted':['A'],'structural':['LANG']},{'A':'allowed','LANG':'C'},['FX-3'],p,'$.acceptanceEvidenceFixtureClasses.classes[4]')
def W(typ,req=None,val=None):
 o={'op':'WRITE','type':typ}
 if req:o['request']=req
 if val:o['value']=val
 return [o,{'op':'SYNC'}]
traces=[('before-accept',W('REV')+W('RA','q'),{'initiated':[],'revoked':True},['FX-5','R-7']),('after-accept',W('RA','q')+W('REV')+W('RCI','q'),{'initiated':[],'revoked':True},['FX-5','R-1','R-2']),('irreversible-before',W('RA','q')+W('ICI','q')+[{'op':'EFFECT','request':'q'}]+W('ICO','q','COMPLETED')+W('REV'),{'initiated':['q'],'outcomes':{'q':'COMPLETED'}},['FX-5','R-3']),('irreversible-after',W('RA','q')+W('REV')+W('ICI','q'),{'initiated':[],'refusals':[{'request':'q','decision':'PR-8'}]},['FX-5','R-3']),('between-calls',W('RA','q')+W('RCI','q')+[{'op':'EFFECT','request':'q'}]+W('RCO','q','COMPLETED')+W('REV')+W('RA','q2'),{'initiated':['q'],'revoked':True},['FX-5']),('expiry',W('RA','q')+W('EXPIRY')+W('RCI','q'),{'initiated':[],'refusals':[{'request':'q','decision':'PR-5'}]},['R-10']),('indeterminate',W('RA','q')+W('ICI','q')+[{'op':'EFFECT','request':'q'},{'op':'CRASH'}],{'outcomes':{'q':'INDETERMINATE'},'revoked':True,'retryCount':0},['FX-11']),('duplicate',W('REV')+W('REV')+W('REV'),{'duplicateRevocations':2,'revokedAt':1},['FX-12','R-5']),('death-cleanup',W('RA','q')+W('RCI','q')+[{'op':'EFFECT','request':'q'}]+W('REV')+[{'op':'CRASH'},{'op':'CRASH'}],{'inverse':['q'],'cleanupClosed':True},['R-6','FX-12'])]
for name,schedule,expected,classes in traces:
 for clock in ('normal','backward','forward','frozen','transport-delayed'):
  add('journal-'+name+'-'+clock,'journal',{'schedule':schedule+[{'op':'CLEANUP'}],'clockPerturbation':clock},expected,classes+['FX-7'],p,'$.linearization; $.raceSemantics', ['journal-invariants'])
# All L-1..L-8 write and sync crash boundaries. Both OS labels are design axes, not executions there.
ladder=W('RA','q')+W('ICI','q')+W('ICO','q','COMPLETED')+W('REV')+W('CLN')+W('AUD')
reversible=W('RA','r')+W('RCI','r')+W('RCO','r','COMPLETED')+W('REV')+W('CLN')+W('AUD')
for platform,trace_name,trace in itertools.product(('macos','linux'),('irreversible','reversible'),(None,)):
 trace=ladder if trace_name=='irreversible' else reversible
 for cut in range(len(trace)+1):
  add(f'crash-{platform}-{trace_name}-{cut}','journal',{'schedule':trace[:cut]+[{'op':'CRASH'}],'platformAxis':platform}, {'retryCount':0},['FX-4'],p,'$.linearization.transitions',['journal-invariants'])
for o in ('COMPLETED','FAILED','INDETERMINATE'):
 add('wording-'+o,'wording',{'outcome':o},{'machine':{'effectOutcome':o,'ordering':o+'-BEFORE-REVOCATION'},'human':o+'-BEFORE-REVOCATION\n','audit':{'ordering':o+'-BEFORE-REVOCATION','effectOutcome':o}},['FX-6'],p,'$.linearization.irreversibleBoundary',['no-undo-wording'])
# Actor split: concrete bindings use local labels, not authoritative Run/Execution identities.
bound={'invocation':'inv-local-1','generation':'g1','manifestDigest':'a'*64,'platform':'linux-x86_64','resource':'/etc/os-release','endpoint':'https://trust.example.invalid','check':'trust-read'}
base={'actor':'host','action':'CA-1','subtype':'SPAWN','contract':True,'admission':True,'consent':True,'bound':bound,'actual':bound}
for action,subtype,reason in [('CA-1','SPAWN',None),('CA-1','IN_PROCESS','INPROCESS-PREVIEW-EXCLUDED'),('CA-2',None,'CA2-PREVIEW-EXCLUDED'),('CA-3','KEYCHAIN','SUBTYPE-NOT-ADMITTED'),('CA-3','OUT_OF_ROOT_READ',None),('CA-4','PATH-TRUST-STATE-REFRESH',None),('CA-4','UNCLASSIFIED','SUBTYPE-NOT-ADMITTED'),('UNKNOWN',None,'UNNAMED-ACT')]:
 add(f'host-{action}-{subtype}','actor',base|{'action':action,'subtype':subtype},{'decision':'DENIED' if reason else 'GRANTED','reason':reason,'grantJournalWritten':False},['FC-JOIN-HOST-OUTSIDE-DR105','FC-JOIN-CA2-UNEXERCISABLE','FC-JOIN-CA1-INPROCESS-UNEXERCISABLE','FC-JOIN-CA3-KEYCHAIN-UNEXERCISABLE'],j,'$.joinFixtureClasses')
for field,reason,cls in [('contract','CONTRACT-NOT-RECORDED','FC-CONSENT-WITHOUT-CONTRACT'),('consent','CONSENT-REQUIRED','FC-CONTRACT-WITHOUT-CONSENT'),('admission','PRODUCT-NOT-ADMITTED','FC-CONSENT-CONTRACT-WITHOUT-PRODUCT-ADMISSION')]:
 add('host-no-'+field,'actor',base|{field:False},{'decision':'DENIED','reason':reason},[cls],h,'$.failClosed')
for field in bound:
 changed=bound|{field:'different'}
 add('host-mismatch-'+field,'actor',base|{'actual':changed},{'decision':'DENIED','reason':'BINDING-MISMATCH'},['FC-SCOPE-MISMATCH','FC-CROSS-GENERATION-REPLAY','FC-WRONG-MANIFEST'],h,'$.authorizationRecord')
for token in TOKENS:
 add('component-tail-'+token,'actor',{'actor':'component','token':token},{'authority':'DR-105','token':token,'hostConsentGrant':False},['FC-JOIN-COMPONENT-TAIL','FC-TAIL','FC-JOIN-INHERITED-PERM-RECITAL'],j,'$.extractedDecidedClauses')
add('customer-tool-tail','actor',{'actor':'customer-tool'},{'authority':'CUSTOMER-TOOL-TAIL','admitted':False},['FC-JOIN-CA2-TAIL','FC-HOST-CA4-NOT-TOOL-SOCKET'],j,'$.joinFixtureClasses')
add('reserved-permissionref','actor',base|{'permissionRef':'gj:1'},{'decision':'DENIED','reason':'RESERVED-FIELD'},['FC-JOIN-PERMISSIONREF-RESERVED'],j,'$.joinFixtureClasses')
for action,denied in itertools.product(('DEFAULT-READ','OPMETA-WRITE'),(False,True)):
 add('default-'+action+str(denied),'actor',{'actor':'host','action':action,'hostClassDenied':denied},{'authority':'HOST-DEFAULT','decision':'DENIED' if denied else 'GRANTED','grantJournalWritten':False},['FC-JOIN-HOST-DEFAULT-AND-OPMETA','FC-JOIN-DOCTOR-CONSENT-NOT-GRANT'],j,'$.joinFixtureClasses')
for boundary,complete,survivor in itertools.product(('before','during','after'),(False,True),(False,True)):
 exp={'standing':'UNEMITTED-CRASH'} if not survivor else {'effectOutcome':'DEFINITELY_NOT_PERFORMED' if boundary=='before' else 'COMPLETED' if complete else 'INDETERMINATE'}
 add('host-outcome-'+str(len(CASES)),'host-outcome',dict(boundary=boundary,knownCompleted=complete,survivingWriter=survivor),exp,['FC-OUTCOME','FC-CANCEL-BEFORE-COMMIT','FC-CANCEL-AFTER-COMMIT','FC-PROCESS-DEATH-INDETERMINATE','FC-CA4-RESOLVE-OR-CONNECT'],h,'$.effectCommit; $.outcomeVocabulary')
statuses=['PASS','FAIL','UNDETERMINED','NOT-APPLICABLE','CONSENT-REQUIRED']
for a,b in itertools.product(statuses,statuses):
 exp='OC-2' if 'FAIL' in (a,b) else 'OC-3' if any(s in ('UNDETERMINED','CONSENT-REQUIRED') for s in (a,b)) else 'OC-1'
 add('doctor-outcome-'+a+'-'+b,'doctor-outcome',{'statuses':[a,b]},exp,['FC-D9'],d,'$.outcomeStructure.derivationRule')
for flag,exp in [('fault','OC-5'),('refused','OC-4')]:add('doctor-'+flag,'doctor-outcome',{'statuses':[],flag:True},exp,['FC-D9'],d,'$.outcomeStructure.derivationRule')
for explicit,present,resolvable,expected in [('core',False,False,{'mode':'core','projectStatus':'NOT-APPLICABLE'}),('core',True,True,{'mode':'core','projectStatus':'NOT-APPLICABLE'}),('project',True,True,{'mode':'project','projectStatus':'PASS'}),('project',True,False,{'mode':'project','projectStatus':'UNDETERMINED'})]:add('doctor-mode-'+str(len(CASES)),'mode',dict(explicit=explicit,present=present,resolvable=resolvable),expected,['FC-MODE'],d,'$.modes')
secretbase={'secret':'s3cr3t-NEVER-OUTPUT','credentialPresent':True,'projectPath':'/private/user/project'}
for name,text,expected in [('url','https://bob:pass@host/p','https://[REDACTED]@host/p'),('bearer','Bearer AbC123.x','Bearer [REDACTED]'),('assignment','password=longsecret','password=[REDACTED]'),('ansi','\u001b[31mred\u001b[0m\u0001','red'),('unknown','f7c4D2qZ8wV9m3rL','f7c4D2qZ8wV9m3rL'),('long','Z'*10000000,'Z'*1008+'[TRUNCATED]')]:
 add('redact-'+name,'redact',secretbase|{'diagnostic':text},{'diagnostic':expected,'secret':'[REDACTED]','credentialPresent':True,'project':'<PROJECT>'},['FC-REDACT','FC-HOSTILE'],d,'$.redaction; $.acceptanceEvidenceFixtureClasses.FC-REDACT',['secret-noninterference'])
# Exhaustive 343 continuation triples: expectation expressed as a rank truth table independent of model branches.
states=['ST-UNBOOTSTRAPPED','ST-TRUSTED','ST-EXPIRED','ST-STALE-REVOCATION','ST-QUORUM-LOST','ST-RECOVERY','ST-REVOKED']
for ss in itertools.product(states,repeat=3):
 failures=[ss[0]!='ST-TRUSTED',ss[1] not in ['ST-TRUSTED','ST-EXPIRED','ST-STALE-REVOCATION'],ss[2]!='ST-TRUSTED']
 first=next((i for i,f in enumerate(failures) if f),None)
 reason=None if first is None else ['CONTINUE-CORE-NOT-TRUSTED','CONTINUE-INDEX-NOT-TRUSTED','CONTINUE-COMPONENT-NOT-TRUSTED'][first]
 add('continue-'+'-'.join(s[3:] for s in ss),'continuation',{'states':ss},{'alreadyRunning':first is None,'newProcess':all(s=='ST-TRUSTED' for s in ss),'reason':reason},['FC-CONTINUE','FC-CONTINUE-PRECEDENCE'],t,'$.offlineRunningPolicy.totalDecision')
# Explicit state transitions, including disjoint authenticated payload kind.
def tc(name,inp,to,reason=None,classes=[]):
 exp={'from':inp['state'],'to':to,'outcome':'refused' if reason else 'accepted'}
 if reason:exp['refusalReason']=reason
 add('trust-'+name,'trust',inp,exp,classes+['FC-REFUSAL-AUDIT'],t,'$.machine.transitions; $.machine.outcomeBranchDiscipline')
for s in states:
 for kind,active in itertools.product(('ordinary','recovery'),(False,True)):
  inp={'state':s,'event':'PRESENT','kind':kind,'active':active,'valid':True,'complete':True}
  reason='PAYLOAD-NOT-ADMISSIBLE' if kind=='recovery' and s=='ST-TRUSTED' or kind=='ordinary' and s in ('ST-RECOVERY','ST-REVOKED') else 'ENVELOPE-INACTIVE' if kind=='ordinary' and not active else None
  to='ST-TRUSTED' if kind=='ordinary' and active and s not in ('ST-RECOVERY','ST-REVOKED') else s
  tc(s+'-'+kind+'-'+str(active),inp,to,reason,['FC-PAYLOAD-KIND-DISJOINT','FC-ENVELOPE-INACTIVE'])
for s in states:
 tc('install-'+s,{'state':s,'event':'INSTALL','active':True,'valid':True},s,None if s=='ST-TRUSTED' else 'INSTALL-NOT-TRUSTED',['FC-TRUST-POLICY'])
for s in ['ST-TRUSTED','ST-STALE-REVOCATION','ST-RECOVERY']:
 tc('clock-'+s,{'state':s,'event':'CLOCK','eval':100,'expires':90,'revocationIssued':-90*86400},'ST-RECOVERY' if s=='ST-RECOVERY' else 'ST-EXPIRED',classes=['FC-EXPIRED','FC-EVENT-ORDER'])
tc('stale',{'state':'ST-TRUSTED','event':'CLOCK','eval':90*86400+1,'expires':365*86400,'revocationIssued':0},'ST-STALE-REVOCATION',classes=['FC-STALE-REV'])
for s in ['ST-TRUSTED','ST-RECOVERY','ST-REVOKED']:
 tc('revoke-'+s,{'state':s,'event':'REVOKE','newCounter':2,'oldCounter':1,'valid':True},'ST-REVOKED',classes=['FC-REPEATED-REVOKE','FC-EVENT-ORDER'])
for n in range(6):
 inp={'state':'ST-RECOVERY','event':'RECOVER-COMMIT','active':True,'valid':True,'authorizedSigners':['k'+str(i) for i in range(n)],'rootBinding':True,'oldRootNamed':True}
 tc('recover-signers-'+str(n),inp,'ST-TRUSTED' if n>=3 else 'ST-RECOVERY',None if n>=3 else 'RECOVERY-COMMIT-REFUSED',['FC-RECOVER','FC-RECOVERY-AUTHORITY'])
for flag in ['rootBinding','oldRootNamed','valid']:
 tc('recover-no-'+flag,inp|{flag:False},'ST-RECOVERY','RECOVERY-COMMIT-REFUSED',['FC-RECOVERY-AUTHORITY'])
for truths in [[],['ST-EXPIRED'],['ST-STALE-REVOCATION','ST-EXPIRED'],['ST-REVOKED','ST-QUORUM-LOST','ST-EXPIRED']]:
 exp=next((s for s in ['ST-REVOKED','ST-QUORUM-LOST','ST-EXPIRED','ST-STALE-REVOCATION'] if s in truths),'ST-UNBOOTSTRAPPED')
 tc('abort-'+str(len(CASES)),{'state':'ST-RECOVERY','event':'RECOVER-ABORT','stillTrue':truths},exp,classes=['FC-RECOVER-ABORT'])
for role,n in itertools.product(('ROOT','INDEX','RECOVERY'),range(6)):
 add('threshold-'+role+str(n),'policy-numbers',{'kind':'threshold','role':role,'validAuthorizedSigners':['k'+str(i) for i in range(n)]},{'accepted':n>=(3 if role=='RECOVERY' else 2)},['FC-QUORUM'],t,'$.namedOpenDecisions + security completion successor')
for days,renewals in itertools.product((29,30,31),(0,1,2)):
 add('waiver-'+str(days)+'-'+str(renewals),'policy-numbers',{'kind':'waiver','days':days,'renewals':renewals,'product':True,'release':True,'semanticOrTrustBlocker':False},{'allowed':days<=30 and renewals<=1},['WAIVER-BOUNDS'],t,'$.auditAndWaiver + security completion successor')
for exp in (90*86400,365*86400):
 add('time-rollback-'+str(exp),'policy-numbers',{'kind':'time','highwater':0,'observations':[exp-1,exp,1],'issued':0,'expires':exp},{'highwater':exp,'decisions':['FRESH','EXPIRED','EXPIRED']},['FC-EXPIRED','MONOTONIC-TIME'],t,'$.monotonicStore + pending security repair')
for delta in (86400,86401):
 add('future-'+str(delta),'policy-numbers',{'kind':'time','highwater':100,'observations':[100],'issued':100+delta,'expires':1000000},{'highwater':100,'decisions':['FRESH' if delta==86400 else 'FUTURE']},['FC-FUTURE'],t,'$.namedOpenDecisions + security completion successor')
for restored,anchor in itertools.product((False,True),(False,True)):
 add('restore-'+str(restored)+str(anchor),'policy-numbers',{'kind':'restore','restoreDetected':restored,'anchorMatches':anchor},{'admission':'REFUSED' if restored or not anchor else 'ALLOWED','networkFallback':False},['WHOLE-SET-RESTORE'],t,'$.monotonicStore + pending security repair')
# Complete report goldens and additive reader variants.
lim={'statement':'Observation is bounded.','cause':'observation-bounded','wouldBeResolvedBy':None}
report={'schemaVersion':1,'mode':'core','outcome':'OC-1','environment':{'mode':'core','modeSelectionReason':'Explicit core mode','installedGenerationRef':'install-generation-local-1','platform':{'os':'linux','architecture':'x86_64'},'configurationLayersResolved':['defaults'],'offlinePosture':{'egressConsentNamed':False,'revocationIssuedAt':'2026-09-01T00:00:00Z','metadataExpiresAt':'2026-12-01T00:00:00Z'},'generatedAt':'2026-09-04T00:00:00Z','projectRootRef':None},'checks':[{'id':'install-integrity','class':'INSTALL-INTEGRITY','status':'PASS','title':'Installed bytes match recorded inventory','evidence':[{'kind':'recorded-digest','observed':'a'*64,'bound':'Self-verification; independent host measurement not implied.'}],'residualLimitation':lim}],'consentRecords':[],'residualLimitations':[]}
for status in statuses:
 r=copy.deepcopy(report);r['checks'][0]['status']=status;r['checks'][0]['residualLimitation']=lim if status in ('UNDETERMINED','CONSENT-REQUIRED') else None;r['outcome']='OC-2' if status=='FAIL' else 'OC-3' if status in ('UNDETERMINED','CONSENT-REQUIRED') else 'OC-1'
 add('full-report-'+status,'doctor-reader',{'report':r},{'accepted':True,'outcome':r['outcome']},['FC-SCHEMA','FC-D9'],d,'$.stableMachineSchema; $.outcomeStructure')
for key,val in [('id','future-check-id'),('class','FUTURE-CHECK-CLASS'),('futureOptional',{'new':True})]:
 r=copy.deepcopy(report);r['checks'][0][key]=val
 add('report-additive-'+key,'doctor-reader',{'report':r},{'accepted':True,'outcome':'OC-1'},['FC-SCHEMA'],d,'$.stableMachineSchema.stabilityRules')
for key in report:
 r=copy.deepcopy(report);del r[key];add('report-delete-'+key,'doctor-reader',{'report':r},{'accepted':False},['FC-SCHEMA'],d,'$.stableMachineSchema.reportEnvelope')
for key in report['checks'][0]:
 r=copy.deepcopy(report);del r['checks'][0][key];add('check-delete-'+key,'doctor-reader',{'report':r},{'accepted':False},['FC-SCHEMA'],d,'$.stableMachineSchema.checkObject')
for label,changes in [('major',{'schemaVersion':2}),('boolean',{'ok':True}),('empty',{'checks':[]})]:
 add('report-invalid-'+label,'doctor-reader',{'report':report|changes},{'accepted':False},['FC-SCHEMA'],d,'$.stableMachineSchema.stabilityRules')
r=copy.deepcopy(report);r['checks'][0]['status']='SKIPPED';add('report-sixth-status','doctor-reader',{'report':r},{'accepted':False},['FC-SCHEMA'],d,'$.stableMachineSchema.checkObject.statusTokens')
# Full authorization and consent envelopes, nineteen-to-fifteen field mapping.
contract={'path':'docs/coop/artifacts/host-effect-authorization.v25.json','version':25,'sha256':hashlib.sha256((A/'host-effect-authorization.v25.json').read_bytes()).hexdigest()}
admission={'authority':'fixture-design','artifactPath':'docs/coop/completion/security-completion.v1.md','selector':'section 6','digest':'b'*64,'standing':'PROPOSED-INTEGRATION','scope':'preview'}
ars=[]
for action,sub in [('CA-1','SPAWN'),('CA-1','IN_PROCESS'),('CA-2',None),('CA-3','OUT_OF_ROOT_READ'),('CA-4','PATH-TRUST-STATE-REFRESH')]:
 ar={'id':'attempt-'+str(len(ars)),'actor':'HOST-UNDER-INSTRUCTION','actionClass':{'CA-1':'CA-1-HOST-HEAD','CA-4':'CA-4-HOST'}.get(action,action),'actionSubtype':sub,'componentGenerationIdentity':'component-generation-local-1' if action=='CA-1' else None,'admittedManifestDigest':'a'*64 if action=='CA-1' else None,'designContractRef':contract,'invocationId':'doctor-local-1','checkIds':['probe-health'],'resourceScope':['/etc/os-release'] if action=='CA-3' else [],'toolIdentity':'declared-tool-local-1' if action=='CA-2' else None,'endpointSet':['https://trust.example.invalid'] if action=='CA-4' else None,'platform':'linux-x86_64','consentCarrier':'invocation-time-naming','policyProvenance':None,'productAdmissionRefs':[admission],'resolution':'DENIED' if action=='CA-2' or sub=='IN_PROCESS' else 'GRANTED','owners':['Operability+security','Security+platform'],'auditIdentity':'separate-audit-handle-'+str(len(ars))}
 scope={'actor':ar['actor'],'actionSubtype':sub,'invocation':ar['invocationId'],'checks':ar['checkIds'],'resources':ar['resourceScope'],'targetIdentity':{'generation':ar['componentGenerationIdentity'],'admittedManifestDigest':ar['admittedManifestDigest']} if action=='CA-1' else {'toolIdentity':ar['toolIdentity']} if action=='CA-2' else None,'observationDeadline':{'kind':'DURATION-FROM-INVOCATION-START','value':1000,'unit':'milliseconds','clockRule':'OBSERVATION-ONLY'},'byteCap':{'acceptFromTarget':4096} if action in ('CA-1','CA-2') else {'send':4096,'receive':8192} if action=='CA-4' else None,'endpointSet':ar['endpointSet'],'platform':ar['platform'],'policyProvenance':ar['policyProvenance'],'designContractRef':ar['designContractRef'],'productAdmissionRefs':ar['productAdmissionRefs'],'owners':ar['owners'],'auditIdentity':ar['auditIdentity']}
 cr={'id':ar['id'],'actionClass':action,'permissionRef':{'reserved':True,'ridesOn':['DR-105']},'scope':scope,'endpoint':ar['endpointSet'] if action=='CA-4' else ar['resourceScope'] if action=='CA-3' else None,'bytes':{'send':17,'receive':31} if action=='CA-4' else {'acceptFromTarget':21} if action=='CA-1' and sub=='SPAWN' else None,'authorization':ar['resolution'].lower(),'execution':'refused' if ar['resolution']=='DENIED' else 'disclosed-trusted-code','result':{'observation':'not-performed' if ar['resolution']=='DENIED' else 'reference-probe-result'},'residualLimitation':{'statement':'Trusted code remains unconstrained. Null target, endpoint, or bytes mean not applicable. CA-3 byteCap null reason: NOT-APPLICABLE-NO-IO-BOUND.','cause':'observation-bounded','wouldBeResolvedBy':None},'effectOutcome':'DEFINITELY_NOT_PERFORMED' if ar['resolution']=='DENIED' else 'COMPLETED'}
 pair={'authorization':ar,'consent':cr};ars.append(pair)
 add('full-host-record-'+action+'-'+str(sub),'host-record',pair,{'accepted':True},['FC-ROUND-TRIP','FC-SCOPE-SHAPE','FC-BOUND-SHAPE','FC-SUBTYPE-CLASS','FC-POSTREPORT','FC-CONSENT'],h,'$.authorizationRecord.doctorV4FieldMapping; $.authorizationRecord.consentRecordsScopeShape')
 r=copy.deepcopy(report);r['consentRecords']=[cr];add('full-doctor-consent-'+action+'-'+str(sub),'doctor-reader',{'report':r},{'accepted':True},['FC-SCHEMA','FC-POSTREPORT'],d,'$.consentModel.mandatoryPostReport')
 for key in ar:
  pair=copy.deepcopy(ars[-1]);del pair['authorization'][key];add('ar-missing-'+str(len(CASES)),'host-record',pair,{'accepted':False},['FC-ROUND-TRIP'],h,'$.authorizationRecord.closedMembers')
 for key in scope:
  pair=copy.deepcopy(ars[-1]);del pair['consent']['scope'][key];add('scope-missing-'+str(len(CASES)),'host-record',pair,{'accepted':False},['FC-ROUND-TRIP','FC-SCOPE-SHAPE'],h,'$.authorizationRecord.consentRecordsScopeShape')
 for field in ('observationDeadline','byteCap','targetIdentity'):
  pair=copy.deepcopy(ars[-1]);pair['consent']['scope'][field]={};add('bound-empty-'+str(len(CASES)),'host-record',pair,{'accepted':False},['FC-BOUND-SHAPE'],h,'$.authorizationRecord.consentRecordsScopeShape')
for field in ('generation','admittedManifestDigest','toolIdentity'):
 pair=copy.deepcopy(ars[0]);pair['consent']['scope'][field]='x';add('wrong-top-level-'+field,'host-record',pair,{'accepted':False},['FC-SCOPE-SHAPE'],h,'$.authorizationRecord.consentRecordsScopeShape')
for provenance,carrier,expected in [(None,'invocation-time-naming',True),({'authority':'product-security','artifactPath':'policy.json','selector':'$.policy','digest':'c'*64},'pre-existing-policy',True),('bad','pre-existing-policy',False),(None,'pre-existing-policy',False),({'authority':'x'},'invocation-time-naming',False)]:
 pair=copy.deepcopy(ars[0]);pair['authorization']['consentCarrier']=carrier;pair['authorization']['policyProvenance']=provenance;pair['consent']['scope']['policyProvenance']=provenance;add('carrier-'+str(len(CASES)),'host-record',pair,{'accepted':expected},['FC-CARRIER-SHAPE'],h,'$.authorizationRecord.consentCarrierPredicateDomain')
for i,pair0 in enumerate(ars):
 pair=copy.deepcopy(pair0);pair['consent']['scope']['actionSubtype']='WRONG';add('cross-subtype-'+str(i),'host-record',pair,{'accepted':False},['FC-SUBTYPE-CLASS'],h,'$.authorizationRecord.consentRecordsScopeShape')
for effect in ('COMPLETED','DEFINITELY_NOT_PERFORMED','INDETERMINATE'):
 pair=copy.deepcopy(ars[0]);pair['consent']['effectOutcome']=effect;add('full-effect-'+effect,'host-record',pair,{'accepted':True},['FC-OUTCOME'],h,'$.outcomeVocabulary')
# Retained degraded raw source bytes; source identities and before/after snapshots are explicit.
obs=[('inventory',{'kind':'inventory','source':'corrupt','expectedDigest':hashlib.sha256(b'original').hexdigest()},'FAIL'),('lock-truncated',{'kind':'lock','source':'{"components":['},'UNDETERMINED'),('lock-duplicate',{'kind':'lock','source':'{"components":[],"components":[]}'},'UNDETERMINED'),('lock-absent',{'kind':'lock','source':None},'UNDETERMINED'),('missing-component',{'kind':'lock','source':'{"components":["missing"]}','missingComponent':True},'FAIL'),('revoked',{'kind':'revocation','source':'recorded-revocation','revoked':True},'FAIL'),('clock',{'kind':'revocation','source':'recorded-revocation','timeUnestablished':True,'issuedAt':'2026-09-01T00:00:00Z','expiresAt':'2026-12-01T00:00:00Z'},'UNDETERMINED'),('changed',{'kind':'lock','source':'{"components":[]}','sourceAfter':'{"components":["x"]}'},'UNDETERMINED')]
for phase in ['PREPARE','COMMIT','ABORT','AMBIGUOUS']:obs.append(('migration-'+phase,{'kind':'migration','source':phase},'UNDETERMINED' if phase=='AMBIGUOUS' else 'PASS'))
for name,inp,status in obs:
 add('doctor-observe-'+name,'doctor-observe',inp,{'status':status,'writes':[],'locks':[],'network':[],'exec':[]},['FC-DEGRADED','FC-RO','FC-NC','FC-NN'],d,'$.degradedAndHostileInputs')
for days,minor,referenced in itertools.product((89,90,91),(0,1),(False,True)):
 closed=days>=90 and minor>=1;expected='WINDOW-CLOSED-ACTION-REQUIRED' if closed and referenced else 'UPDATE-PIN' if referenced else 'WINDOW-OPEN-NO-ACTION-REQUIRED'
 add('remediation-'+str(len(CASES)),'remediation',{'active':True,'daysElapsed':days,'minorCycles':minor,'referenced':referenced,'recordedWindow':{'deprecatedAtRelease':'0.1.0','deprecatedAtDate':'2026-06-01','windowEndsNoEarlierThan':{'date':'2026-08-30','minorCycles':1}}},{'remediationClass':expected,'appliedBy':'operator','mutations':[]},['FC-REMEDIATION'],d,'$.doctorRemediationRecord')

payload={'rootChain':[{'rootVersion':1,'roleKeys':['k1','k2','k3']}],'index':{'snapshotVersion':1,'entries':['typescript']} ,'revocation':{'version':1,'revoked':[]},'expiry':{'rootDays':365,'indexDays':90,'revocationFreshDays':90},'manifests':[{'fixturePath':'security-fixtures.v1/typescript-analyzer.manifest.json','sha256':hashlib.sha256((P/'security-fixtures.v1/typescript-analyzer.manifest.json').read_bytes()).hexdigest()}],'payloads':[{'name':'typescript','storedSha256':'a'*64}],'permissions':{'default':'deny'},'repairMaterial':{'absent':True,'ridesOn':'DR-110','stage':'REENTRY-REQUIRED'}}
basis={'payload':payload,'authenticated':True,'roleBinding':True,'namespaceAuthorized':True,'antiRollback':True,'envelopeMatches':True}
add('airgap-complete','airgap',basis,{'accepted':True,'network':[],'refresh':[],'lockMutation':False},['FC-AG-COMPLETE'],t,'$.airGapPayload')
for field in payload:
 inp=copy.deepcopy(basis);del inp['payload'][field];add('airgap-missing-'+field,'airgap',inp,{'accepted':False,'network':[],'refresh':[],'lockMutation':False},['FC-AG-MISSING'],t,'$.airGapPayload.mustCarry')
for field in ['authenticated','roleBinding','namespaceAuthorized','antiRollback','envelopeMatches']:
 add('airgap-invalid-'+field,'airgap',basis|{field:False},{'accepted':False},['FC-TRUST-POLICY'],t,'$.trustPolicyShape')
for name,row in [('in-host-process','DR-105 / later product admission'),('replay','DR-113'),('repair','DR-110'),('keychain','DR-108'),('third-party','DR-128')]:
 add('typed-absence-'+name,'typed-absence',{'ridesOn':row},{'standing':'REENTRY-REQUIRED','ridesOn':row,'executionAllowed':False},['FX-10' if name=='in-host-process' else 'FC-REPLAY-NAMED' if name=='replay' else 'FC-REPAIR-NAMED' if name=='repair' else 'DEFERRED-EXERCISER'],p if name=='in-host-process' else t,'$.fixtureClasses / scope successor')
binding={'requestAttempt':'attempt-local-1','component':'typescript-fixture','installGenerationId':'generation-local-1','manifestDigest':'a'*64,'processInstance':'process-local-1','operation':'operation-local-1','grantGeneration':1,'grant':'grant-local-1','project':'project-local-1','scope':{'tokens':['PT-FS-READ-PROJECT'],'prefixes':['src/']},'expiry':{'observation':'explicit-journal-record'}}
records=[{'type':kind,'binding':binding} for kind in ['REQUESTED','GRANT','RA','RCI','RCO','AUD']]
add('grant-complete-binding','grant-binding',{'binding':binding,'records':records},{'accepted':True,'authoritativeIdentityMinted':False},['FX-13'],p,'$.acceptanceEvidenceFixtureClasses.classes.FX-13')
for field in binding:
 rr=copy.deepcopy(records);del rr[1]['binding'][field]
 add('grant-missing-binding-'+field,'grant-binding',{'binding':binding,'records':rr},{'accepted':False},['FX-13'],p,'$.acceptanceEvidenceFixtureClasses.classes.FX-13')
# Explicit old precondition inversions: FC-C1 now recorded under the completion successor;
# CA2 later admission and CA1 in-process exclusions still deny even when that condition is true.
for action,sub in [('CA-1','SPAWN'),('CA-1','IN_PROCESS'),('CA-2',None),('CA-3','OUT_OF_ROOT_READ'),('CA-4','PATH-TRUST-STATE-REFRESH')]:
 add('joint-contract-absent-'+str(len(CASES)),'actor',base|{'action':action,'subtype':sub,'contract':False},{'decision':'DENIED','reason':'CONTRACT-NOT-RECORDED'},['FC-JOIN-FAIL-CLOSED-UNRECORDED'],j,'$.joinFixtureClasses')
add('ca2-all-prerequisites-still-deny','actor',base|{'action':'CA-2','subtype':None},{'decision':'DENIED','reason':'CA2-PREVIEW-EXCLUDED'},['FC-JOIN-CA2-D000-GATE','FC-CA2-PREVIEW-DENIED','FC-NOT-SUFFICIENT'],j,'$.joinFixtureClasses')

# Reference report schema: extensible reader positions follow doctor v4's additive law.
S={'type':'string','maxLength':4096};N={'type':'integer','minimum':0,'maximum':9007199254740991}
def ob(props,required=None,closed=False):return {'type':'object','properties':props,'required':list(props) if required is None else required,'additionalProperties':not closed}
nullable=lambda schema:{'anyOf':[schema,{'type':'null'}]}
arr=lambda item:{'type':'array','items':item,'maxItems':100000}
limschema=ob({'statement':S,'cause':S,'wouldBeResolvedBy':nullable(S)})
evschema=ob({'kind':S,'observed':{},'bound':S,'provenance':{'type':'object'}},['kind','observed','bound'])
checkschema=ob({'id':S,'class':S,'status':{'enum':statuses},'title':S,'evidence':arr(evschema),'residualLimitation':nullable(limschema),'remediation':nullable({'type':'object'})},['id','class','status','title','evidence','residualLimitation'])
envschema=ob({'mode':{'enum':['core','project']},'modeSelectionReason':S,'installedGenerationRef':S,'platform':ob({'os':{'enum':['macos','linux']},'architecture':{'enum':['arm64','x86_64']}},closed=True),'configurationLayersResolved':arr(S),'offlinePosture':{'type':'object'},'generatedAt':S,'projectRootRef':nullable(S)})
consentschema=ob({'id':S,'actionClass':{'enum':['CA-1','CA-2','CA-3','CA-4']},'permissionRef':{'const':{'reserved':True,'ridesOn':['DR-105']}},'scope':{'type':'object'},'endpoint':nullable({'anyOf':[S,arr(S)]}),'bytes':nullable(ob({'acceptFromTarget':N,'send':N,'receive':N},[],True)),'authorization':{'enum':['requested','granted','denied']},'execution':{'enum':['enforced','disclosed-trusted-code','refused']},'result':{},'residualLimitation':limschema,'effectOutcome':{'enum':['COMPLETED','DEFINITELY_NOT_PERFORMED','INDETERMINATE']}})
schema=ob({'schemaVersion':{'const':1},'mode':{'enum':['core','project']},'outcome':{'enum':['OC-1','OC-2','OC-3','OC-4','OC-5']},'environment':envschema,'checks':arr(checkschema)|{'minItems':1},'consentRecords':arr(consentschema),'residualLimitations':arr(limschema)})
schema.update({'$schema':'https://json-schema.org/draft/2020-12/schema','$id':'https://opensip.invalid/design/doctor-report.1','not':{'anyOf':[{'required':[k]} for k in ['ready','healthy','ok']]},'$comment':'Structural reference schema. Host consent scope checked independently against host-effect v25; semantic outcome, evidence, bindings and additive laws checked by security-behavior model. Bound 4096 characters/100000 items are design validation ceilings pending adoption, not measured performance or qualification thresholds.'})
(P/'security-behavior-doctor-schema.v1.json').write_text(json.dumps(schema,indent=2)+'\n')


for key,changes,classes in [
 ('unknown',{'action':'UNKNOWN'},['FC-FAIL-CLOSED']),
 ('keychain',{'action':'CA-3','subtype':'KEYCHAIN'},['FC-KEYCHAIN']),
 ('unclassified-egress',{'action':'CA-4','subtype':'UNCLASSIFIED'},['FC-UNCLASSIFIED-EGRESS']),
 ('inprocess',{'action':'CA-1','subtype':'IN_PROCESS'},['FC-CA1-IN-PROCESS-DENIED'])]:
 add('host-final-'+key,'actor',base|changes,{'decision':'DENIED'},classes,h,'$.acceptanceEvidenceFixtureClasses')
for key in ('resourceScope','endpointSet','toolIdentity','checkIds'):
 pair=copy.deepcopy(ars[0]);pair['authorization'][key]=['*'];add('host-wildcard-'+key,'host-record',pair,{'accepted':False},['FC-WILDCARD-REFUSAL'],h,'$.authorizationRecord.wildcardRefusal')
for kind in ('contract','admission'):
 pair=copy.deepcopy(ars[0]);
 if kind=='contract':pair['authorization']['designContractRef']['sha256']='f'*64;pair['consent']['scope']['designContractRef']['sha256']='f'*64
 else:pair['authorization']['productAdmissionRefs'][0]['digest']='f'*64;pair['consent']['scope']['productAdmissionRefs'][0]['digest']='f'*64
 add('host-stale-'+kind,'host-record',pair,{'accepted':False},['FC-STALE-CONTRACT-REF'],h,'$.authorizationRecord.designContractRef')
for c in CASES:
 if c['model']=='host-record':
  c['input']['recordedContext']={'contract':contract,'admissions':[admission],'standing':'SYNTHETIC-RECORDED-CONTEXT-NOT-ADOPTION'}
  act=c['input']['consent']['actionClass']; sub=c['input']['consent']['scope'].get('actionSubtype')
  c['input']['observation']={'sendHex':(b'R'*17).hex(),'receiveHex':(b'S'*31).hex(),'endpoints':['https://trust.example.invalid']} if act=='CA-4' else {'acceptHex':(b'H'*21).hex()} if act=='CA-1' and sub=='SPAWN' else {'notApplicable':True}
tc('stale-boundary-equality',{'state':'ST-TRUSTED','event':'CLOCK','eval':90*86400,'expires':365*86400,'revocationIssued':0},'ST-TRUSTED',classes=['FC-STALE-REV'])

for c0 in list(CASES):
 if c0['id'].startswith('crash-'):
  for perturbation in ('backward','forward','frozen','transport-delayed'):
   c=copy.deepcopy(c0);c['id']+='-'+perturbation;c['input']['clockPerturbation']=perturbation;c['classes'].append('FX-7');CASES.append(c)
add('cleanup-bound-exhaustion','journal',{'schedule':W('RA','q')+W('RCI','q')+W('REV')+[{'op':'CRASH'},{'op':'CRASH'}],'cleanupFails':True},{'cleanupClosed':True,'inverse':['q'],'retryCount':0},['FX-12','R-6'],p,'$.raceSemantics.races',['journal-invariants'])
r=copy.deepcopy(report);r['mode']='project';r['environment']['mode']='project';r['environment']['modeSelectionReason']='Project requested';r['environment']['projectRootRef']='<PROJECT>';add('full-report-project','doctor-reader',{'report':r},{'accepted':True},['FC-SCHEMA','FC-MODE'],d,'$.stableMachineSchema')
for oc in ('OC-4','OC-5'):
 r=copy.deepcopy(report);r['outcome']=oc;r['checks'][0]['status']='UNDETERMINED';r['checks'][0]['evidence']=[];r['checks'][0]['residualLimitation']=lim;r['residualLimitations']=[lim];add('full-report-'+oc,'doctor-reader',{'report':r},{'accepted':True,'outcome':oc},['FC-SCHEMA','FC-D9'],d,'$.stableMachineSchema; $.outcomeStructure')
for token in TOKENS:
 bb=copy.deepcopy(binding);bb['scope']={'tokens':[token]};rr=[{'type':kind,'binding':bb} for kind in ['REQUESTED','GRANT','RA','RCI','RCO','AUD']];add('grant-bound-'+token,'grant-binding',{'binding':bb,'records':rr},{'accepted':True},['FX-13'],p,'$.acceptanceEvidenceFixtureClasses.classes.FX-13')
obj={'schemaVersion':1,'standing':'DESIGN-EVIDENCE-ONLY','sources':{s:hashlib.sha256((A/(s+'.json')).read_bytes()).hexdigest() for s in SOURCES},'cases':CASES}
(P/'security-behavior-cases.v1.json').write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
print(len(CASES))
