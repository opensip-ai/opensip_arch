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

# Report/schema bounds are adopted by the completion successor, not inferred from fixtures.
S={'type':'string','minLength':1,'maxLength':4096};I={'type':'string','minLength':1,'maxLength':128};H={'type':'string','pattern':'^[0-9a-f]{64}$'};N={'type':'integer','minimum':0,'maximum':9007199254740991}
def ob(props,required=None,closed=False):return {'type':'object','properties':props,'required':list(props) if required is None else required,'additionalProperties':not closed}
nullable=lambda schema:{'anyOf':[schema,{'type':'null'}]}
arr=lambda item:{'type':'array','items':item,'maxItems':4096}
limschema=ob({'statement':S,'cause':I,'wouldBeResolvedBy':nullable(S)})
policy=nullable(ob({'authority':S|{'maxLength':512},'artifactPath':S|{'maxLength':512},'selector':S|{'maxLength':512},'digest':H},closed=True))
contractSchema=ob({'path':S,'version':N,'sha256':H},closed=True)
admissionSchema=ob({k:H if k=='digest' else S for k in ['authority','artifactPath','selector','digest','standing','scope']},closed=True)
platform={'enum':['macos-arm64','macos-x86_64','linux-arm64','linux-x86_64']}
deadline=ob({'kind':{'const':'DURATION-FROM-INVOCATION-START'},'value':N,'unit':{'const':'milliseconds'},'clockRule':{'const':'OBSERVATION-ONLY'}},closed=True)
scprops={'actor':{'const':'HOST-UNDER-INSTRUCTION'},'actionSubtype':nullable(I),'invocation':I,'checks':arr(I),'resources':arr(S),'targetIdentity':nullable({'type':'object'}),'observationDeadline':deadline,'byteCap':nullable({'type':'object'}),'endpointSet':nullable(arr(S)),'platform':platform,'policyProvenance':policy,'designContractRef':contractSchema,'productAdmissionRefs':arr(admissionSchema),'owners':arr(I),'auditIdentity':I}
scschema=ob(scprops,closed=True)
consentschema=ob({'id':I,'actionClass':{'enum':['CA-1','CA-2','CA-3','CA-4']},'permissionRef':{'const':{'reserved':True,'ridesOn':['DR-105']}},'scope':scschema,'endpoint':nullable({'anyOf':[S,arr(S)]}),'bytes':nullable({'type':'object'}),'authorization':{'enum':['requested','granted','denied']},'execution':{'enum':['enforced','disclosed-trusted-code','refused']},'result':{},'residualLimitation':limschema,'effectOutcome':{'enum':['COMPLETED','DEFINITELY_NOT_PERFORMED','INDETERMINATE']}})
subtypes={'CA-1':['SPAWN','IN_PROCESS'],'CA-2':[None],'CA-3':['OUT_OF_ROOT_READ','LOCAL_SOCKET_OR_PIPE','KEYCHAIN','PRIVILEGED_PLATFORM_FACILITY'],'CA-4':['PATH-TRUST-STATE-REFRESH','PATH-INDEX-REACH','PATH-DECLARED-EXTERNAL-SERVICE']}
consentschema['allOf']=[]
for action in subtypes:
 target=ob({'generation':I,'admittedManifestDigest':H},closed=True) if action=='CA-1' else ob({'toolIdentity':I},closed=True) if action=='CA-2' else {'type':'null'}
 cap=ob({'acceptFromTarget':N},closed=True) if action in ('CA-1','CA-2') else ob({'send':N,'receive':N},closed=True) if action=='CA-4' else {'type':'null'}
 ep=arr(S)|{'minItems':1} if action=='CA-4' else {'type':'null'}
 observedBytes=nullable(cap) if action in ('CA-1','CA-2','CA-4') else {'type':'null'}
 consentschema['allOf'].append({'if':{'properties':{'actionClass':{'const':action}}},'then':{'properties':{'scope':{'properties':{'actionSubtype':{'enum':subtypes[action]},'targetIdentity':target,'byteCap':cap,'endpointSet':ep}},'bytes':observedBytes}}})
evschema=ob({'kind':I,'observed':{},'bound':S,'provenance':{'type':'object'}},['kind','observed','bound'])
checkschema=ob({'id':I,'class':I,'status':{'enum':statuses},'title':S,'evidence':arr(evschema),'residualLimitation':nullable(limschema),'remediation':nullable({'type':'object'})},['id','class','status','title','evidence','residualLimitation'])
envschema=ob({'mode':{'enum':['core','project']},'modeSelectionReason':S,'installedGenerationRef':I,'platform':ob({'os':{'enum':['macos','linux']},'architecture':{'enum':['arm64','x86_64']}},closed=True),'configurationLayersResolved':arr(I),'offlinePosture':ob({'egressConsentNamed':{'type':'boolean'},'revocationIssuedAt':S,'metadataExpiresAt':S}),'generatedAt':S,'projectRootRef':nullable(S)})
schema=ob({'schemaVersion':{'const':1},'mode':{'enum':['core','project']},'outcome':{'enum':['OC-1','OC-2','OC-3','OC-4','OC-5']},'environment':envschema,'checks':arr(checkschema),'consentRecords':arr(consentschema),'residualLimitations':arr(limschema)})
schema.update({'$schema':'https://json-schema.org/draft/2020-12/schema','$id':'https://opensip.invalid/design/doctor-report.1','not':{'anyOf':[{'required':[k]} for k in ['ready','healthy','ok']]},'$defs':{'consent':consentschema,'limitation':limschema},'$comment':'UTF-8 byte caps, 16-MiB document cap and 32-container nesting cap are checked before semantic interpretation by the composed reader. OC4 allows empty checks; source-independent observation events govern OC4/5 verification.'})
arschema=ob({'id':I,'actor':{'const':'HOST-UNDER-INSTRUCTION'},'actionClass':{'enum':['CA-1-HOST-HEAD','CA-2','CA-3','CA-4-HOST']},'actionSubtype':nullable(I),'componentGenerationIdentity':nullable(I),'admittedManifestDigest':nullable(H),'designContractRef':contractSchema,'invocationId':I,'checkIds':arr(I),'resourceScope':arr(S),'toolIdentity':nullable(I),'endpointSet':nullable(arr(S)),'platform':platform,'consentCarrier':{'enum':['invocation-time-naming','pre-existing-policy']},'policyProvenance':policy,'productAdmissionRefs':arr(admissionSchema),'resolution':{'enum':['GRANTED','DENIED']},'owners':arr(I),'auditIdentity':I},closed=True)
schema['$defs']['authorization']=arschema
(P/'security-behavior-doctor-schema.v2.json').write_text(json.dumps(schema,indent=2)+'\n')

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
for c in CASES:
 if c['id']=='full-report-OC-4':c['input']['report']['checks']=[]
 if c['model']=='doctor-reader':
  rr=c['input']['report'];checks=rr.get('checks',[]) if isinstance(rr,dict) else []
  c['input']['events']={'checksExecuted':sum(z.get('status') in ('PASS','FAIL') for z in checks if isinstance(z,dict)) if isinstance(checks,list) else 0,'invocationRefusedBeforeChecks':c['id']=='full-report-OC-4','requiredConsentWriteFailed':c['id']=='full-report-OC-5'}
 if c['model']=='host-record':
  c['input']['recordedContext'].update({'contractRecorded':True,'admissionActive':True,'admittedClasses':{'CA-1':['SPAWN','IN_PROCESS'],'CA-2':[None],'CA-3':['OUT_OF_ROOT_READ'],'CA-4':['PATH-TRUST-STATE-REFRESH']}})
  c['input']['invocationConsent']=True
  aa=c['input']['authorization'];c['input']['actualAttempt']={'actor':'HOST-UNDER-INSTRUCTION','class':c['input']['consent']['actionClass'],'subtype':c['input']['consent']['scope'].get('actionSubtype'),'platform':aa.get('platform'),'generation':aa.get('componentGenerationIdentity'),'manifestDigest':aa.get('admittedManifestDigest'),'checks':aa.get('checkIds'),'resources':aa.get('resourceScope'),'toolIdentity':aa.get('toolIdentity'),'endpointSet':aa.get('endpointSet')}
  c['input']['boundAttempt']=copy.deepcopy(c['input']['actualAttempt'])
# Independent FX4 oracle: durable-prefix table authored from L1-L8, not model execution.
for c in CASES:
 if c['id'].startswith('crash-'):
  irr='-irreversible-' in c['id'];req='q' if irr else 'r';n=sum(a['op']=='SYNC' for a in c['input']['schedule'])
  before=[{'seq':1,'type':'RA','request':req},{'seq':2,'type':'ICI' if irr else 'RCI','request':req},{'seq':3,'type':'ICO' if irr else 'RCO','request':req,'value':'COMPLETED'},{'seq':4,'type':'REV'},{'seq':5,'type':'CLN'},{'seq':6,'type':'AUD'}][:n]
  after=copy.deepcopy(before);outs={};inverse=[];rev=n>=4;revAt=4 if rev else None;closed=n>=5
  if n==1:outs={req:'CANCELED-BY-RECOVERY'}
  if n==2:
   if irr:
    after += [{'seq':3,'type':'ICO','request':req,'value':'INDETERMINATE'},{'seq':4,'type':'REV'},{'seq':5,'type':'CLN','value':'CLOSED'}];outs={req:'INDETERMINATE'};rev=True;revAt=4;closed=True
   else:after += [{'seq':3,'type':'RCO','request':req,'value':'CLEANED'}];outs={req:'CLEANED'};inverse=[req]
  if n>=3:outs={req:'COMPLETED'}
  if n==4:after += [{'seq':5,'type':'CLN','value':'CLOSED'}];closed=True
  if not irr and n>=4:inverse=[req]
  c['expectedDurableBeforeCrash']=before
  attempts=copy.deepcopy(inverse)
  if not irr and n==4 and any(a.get('type')=='CLN' for a in c['input']['schedule']):attempts=[req,req]
  c['expectedComplete']={'inverseAttempts':attempts,'journal':after,'initiated':[],'inverse':inverse,'outcomes':outs,'refusals':[],'revoked':rev,'revokedAt':revAt,'cleanupClosed':closed,'duplicateRevocations':0,'retryCount':0}
# Completed reversible outcome must retain its inverse through crash and cleanup.
add('completed-reversible-revocation-crash','journal',{'schedule':W('RA','q')+W('RCI','q')+[{'op':'EFFECT','request':'q'}]+W('RCO','q','COMPLETED')+W('REV')+[{'op':'CRASH'},{'op':'CLEANUP'}]},{'inverse':['q'],'outcomes':{'q':'COMPLETED'},'cleanupClosed':True},['FX-4','FX-12','R-6'],p,'$.linearization.transitions.L3/L7',['journal-invariants'])
# Independent invocation/report failure events, including no-emission OC5.
for event in ['outputSinkFailed','constructionFailed']:
 add('doctor-no-output-'+event,'doctor-execution',{'statuses':[],'events':{event:True,'checksExecuted':0}},{'outcome':'OC-5','reportEmitted':False,'environmentVerdict':False},['FC-D9','FC-RO'],d,'$.outcomeStructure.derivationRule')
for claim in ['OC-4','OC-5']:
 rr=copy.deepcopy(report);rr['outcome']=claim
 add('forged-outcome-'+claim,'doctor-reader',{'report':rr,'events':{'checksExecuted':1,'invocationRefusedBeforeChecks':False,'requiredConsentWriteFailed':False}},{'accepted':False},['FC-SCHEMA','FC-D9'],d,'$.outcomeStructure.derivationRule')
# Full-report path exercises every consent/scope field and closed nested addition.
full=next(c for c in CASES if c['id']=='full-doctor-consent-CA-1-SPAWN')['input']
for key in full['report']['consentRecords'][0]:
 xx=copy.deepcopy(full);del xx['report']['consentRecords'][0][key];add('full-consent-delete-'+key,'doctor-reader',xx,{'accepted':False},['FC-SCHEMA','FC-POSTREPORT'],d,'$.consentModel.mandatoryPostReport')
for key in full['report']['consentRecords'][0]['scope']:
 xx=copy.deepcopy(full);del xx['report']['consentRecords'][0]['scope'][key];add('full-scope-delete-'+key,'doctor-reader',xx,{'accepted':False},['FC-SCOPE-SHAPE'],h,'$.authorizationRecord.consentRecordsScopeShape')
for where in ['scope','observationDeadline','byteCap','targetIdentity']:
 xx=copy.deepcopy(full);sc=xx['report']['consentRecords'][0]['scope'];(sc if where=='scope' else sc[where])['unexpected']=True;add('full-nested-extra-'+where,'doctor-reader',xx,{'accepted':False},['FC-SCOPE-SHAPE','FC-BOUND-SHAPE'],h,'$.authorizationRecord.consentRecordsScopeShape')
for where in ['evidence','environment','consent']:
 xx=copy.deepcopy(full)
 target=xx['report']['checks'][0]['evidence'][0] if where=='evidence' else xx['report']['environment'] if where=='environment' else xx['report']['consentRecords'][0]
 target['futureOptional']={'description':'reader ignores optional field'};add('full-additive-'+where,'doctor-reader',xx,{'accepted':True},['FC-SCHEMA'],d,'$.stableMachineSchema.stabilityRules')
for bad in [None,[],17,'text',True]:
 xx=copy.deepcopy(full);xx['report']['environment']=bad;add('full-environment-type-'+str(len(CASES)),'doctor-reader',xx,{'accepted':False},['FC-SCHEMA'],d,'$.stableMachineSchema.environmentBlock')
for existing in [c for c in CASES if c['id'] in ('full-host-record-CA-1-IN_PROCESS','full-host-record-CA-2-None')]:
 xx=copy.deepcopy(existing['input']);xx['authorization']['resolution']='GRANTED';xx['consent'].update({'authorization':'granted','execution':'disclosed-trusted-code','effectOutcome':'COMPLETED'});add('coherent-forbidden-grant-'+existing['id'],'host-record',xx,{'accepted':False},['FC-NOT-SUFFICIENT','FC-CA1-IN-PROCESS-DENIED','FC-CA2-PREVIEW-DENIED'],h,'$.failClosed')
for key in ['result','residualLimitation','bytes','endpoint']:
 xx=copy.deepcopy(next(c for c in CASES if c['id']=='full-host-record-CA-4-PATH-TRUST-STATE-REFRESH')['input']);del xx['consent'][key];add('mandatory-record-delete-'+key,'host-record',xx,{'accepted':False},['FC-ROUND-TRIP','FC-OUTCOME'],h,'$.authorizationRecord.doctorV4FieldMapping')
xx=copy.deepcopy(next(c for c in CASES if c['id']=='full-host-record-CA-4-PATH-TRUST-STATE-REFRESH')['input']);xx['authorization']['endpointSet']={'host':'wrong'};xx['consent']['scope']['endpointSet']={'host':'wrong'};add('object-endpoint-set','host-record',xx,{'accepted':False},['FC-SCOPE-SHAPE'],h,'$.authorizationRecord.closedMembers.endpointSet')
xx=copy.deepcopy(next(c for c in CASES if c['id']=='full-host-record-CA-1-SPAWN')['input']);xx['consent']['id']='distinct-consent-id';xx['consent']['residualLimitation']['authorizationRecordId']=xx['authorization']['id'];add('distinct-consent-record-id','host-record',xx,{'accepted':True},['FC-ROUND-TRIP'],h,'$.authorizationRecord.doctorV4FieldMapping.destinations.id')
# D006 bounds: independently compute encoded byte lengths, include non-ASCII equality/+1.
for key,cap in [('title',4096),('id',128),('diagnostic',1024)]:
 for size in [0,1,cap,cap+1]:
  for unicode in [False,True]:
   value=('é'*(size//2)+'x'*(size%2)) if unicode else 'x'*size
   add('byte-bound-'+key+'-'+str(size)+'-'+str(unicode),'bound-probe',{'value':{key:value}},{'accepted':size<=cap},['FC-HOSTILE','FC-SCHEMA'],d,'completion successor doctor bounds')
for count in [0,1,4096,4097]:add('collection-bound-'+str(count),'bound-probe',{'value':[None]*count},{'accepted':count<=4096},['FC-HOSTILE','FC-SCHEMA'],d,'completion successor doctor bounds')
for depth in [1,32,33]:
 v=None
 for unused in range(depth):v=[v]
 add('depth-bound-'+str(depth),'bound-probe',{'value':v},{'accepted':depth<=32},['FC-HOSTILE','FC-SCHEMA'],d,'completion successor doctor bounds')
# 16MiB separate from string/collection limits: distribute strings over 4096 slots.
# JSON array overhead = 4096 comma/quote groups + brackets; no field exceeds 4096 bytes.
for delta in [-1,0,1]:
 target=16*1024*1024+delta;v=['x'*4093]*4096
 current=len(json.dumps(v,separators=(',',':')).encode());remaining=target-current
 # At most 3 added bytes per string; preserve every per-string and array bound.
 for i in range(4096):
  n=min(3,max(0,remaining));v[i]+='x'*n;remaining-=n
 if remaining<0:v[-1]=v[-1][:remaining]
 assert len(json.dumps(v,separators=(',',':')).encode())==target
 add('whole-document-'+str(delta),'bound-probe',{'value':v},{'accepted':delta<=0,'encodedBytes':target},['FC-HOSTILE','FC-SCHEMA'],d,'completion successor doctor bounds')


for field in ['platform','generation','manifestDigest','resources','endpointSet']:
 xx=copy.deepcopy(next(c for c in CASES if c['id']=='full-host-record-CA-1-SPAWN')['input']);xx['actualAttempt'][field]='DIFFERENT';add('actual-binding-mismatch-'+field,'host-record',xx,{'accepted':False},['FC-SCOPE-MISMATCH'],h,'$.authorizationRecord.scopeMismatch')
for field in ['contractRecorded','admissionActive']:
 xx=copy.deepcopy(next(c for c in CASES if c['id']=='full-host-record-CA-1-SPAWN')['input']);xx['recordedContext'][field]=False;add('context-absent-'+field,'host-record',xx,{'accepted':False},['FC-NOT-SUFFICIENT'],h,'$.failClosed')
xx=copy.deepcopy(next(c for c in CASES if c['id']=='full-host-record-CA-1-SPAWN')['input']);xx['invocationConsent']=False;add('full-record-no-consent','host-record',xx,{'accepted':False},['FC-CONTRACT-WITHOUT-CONSENT'],h,'$.failClosed')
for size in [1,512,513]:
 for uni in [False,True]:
  xx=copy.deepcopy(next(c for c in CASES if c['id']=='full-host-record-CA-1-SPAWN')['input']);value=('é'*(size//2)+'x'*(size%2)) if uni else 'x'*size
  pol={'authority':value,'artifactPath':'policy.json','selector':'$.policy','digest':'c'*64};xx['authorization']['consentCarrier']='pre-existing-policy';xx['authorization']['policyProvenance']=pol;xx['consent']['scope']['policyProvenance']=pol
  add('source-identity-bound-'+str(size)+str(uni),'host-record',xx,{'accepted':size<=512},['FC-CARRIER-SHAPE'],h,'$.authorizationRecord.policyProvenance')
add('death-after-inverse-before-cleanup-sync','journal',{'schedule':W('RA','q')+W('RCI','q')+W('RCO','q','COMPLETED')+W('REV')+[{'op':'WRITE','type':'CLN'},{'op':'CRASH'}]},{'inverse':['q'],'inverseAttempts':['q','q'],'outcomes':{'q':'COMPLETED'},'cleanupClosed':True},['FX-4','FX-12','R-6'],p,'$.raceSemantics.R6',['journal-invariants'])
obj={'schemaVersion':1,'standing':'DESIGN-EVIDENCE-ONLY','sources':{s:hashlib.sha256((A/(s+'.json')).read_bytes()).hexdigest() for s in SOURCES},'cases':CASES}
(P/'security-behavior-cases.v2.json').write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
print(len(CASES))
