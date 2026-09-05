#!/usr/bin/env python3
"""Deterministic fixture authoring recipe; expected outcomes are separately stated."""
import copy, hashlib, itertools, json, struct
from pathlib import Path
import cbor2
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];ART=ROOT/'docs/coop/artifacts'
SID='00000000-0000-4000-8000-000000000001';DIG='1'*64
TUPLE={'role':'semantic-provider','roleSubprotocol':'typescript','subprotocolVersion':1}
STATES=['AWAIT-HELLO','AWAIT-HELLO-ACK','AWAIT-SELECT','AWAIT-SELECT-ACK','STEADY','TEARDOWN','CLOSED','FAULTED']
PLATFORMS=['macos/arm64','macos/x86_64','linux/x86_64','linux/arm64']
cases=[]
def sha(b):return hashlib.sha256(b).hexdigest()
def frame(v):
 b=json.dumps(v,separators=(',',':'),ensure_ascii=False).encode();return len(b).to_bytes(4,'big')+b

def ctrl(t='ping',body=None,seq=1,major=1):return {'type':t,'seq':seq,'controlMajor':major,'body':{'nonce':'fixture-1'} if body is None else body}
def control(id,v,expected,covers,ctx=None,raw=None):
 cases.append({'id':id,'kind':'control','covers':covers,'bytesHex':(frame(v) if raw is None else raw).hex(),'context':ctx or {'state':'STEADY'},'expected':({'verdict':expected,'discardCandidates':True,'teardown':True} if isinstance(expected,str) else expected)})

def accept(t='ping',state='STEADY'):return {'verdict':'ACCEPT','type':t,'state':state}
# OQG21-4 deliberately envelope-level: no dependency on yet unapproved body schema.
ping=frame(ctrl())
mutants={'duplicate-member':b'{"type":"ping","type":"pong","seq":1,"controlMajor":1,"body":{}}','unknown-member':b'{"type":"ping","seq":1,"controlMajor":1,"body":{},"extra":0}','float':b'{"type":"ping","seq":1.0,"controlMajor":1,"body":{}}','negative':b'{"type":"ping","seq":1,"controlMajor":-1,"body":{}}','over-uint53':b'{"type":"ping","seq":1,"controlMajor":9007199254740992,"body":{}}','invalid-utf8':b'\x80','non-object':b'[]','nested-duplicate':b'{"type":"ping","seq":1,"controlMajor":1,"body":{"nonce":"a","nonce":"b"}}'}
for n,b in mutants.items():control('CC5.'+n,None,'RF-2',['CC-5','OQG21-4'],raw=len(b).to_bytes(4,'big')+b)
control('CC5.truncated',None,'RF-2',['CC-5'],raw=ping[:-1])
for bound in [65536,131072,16777216]:
 for n in [0,bound+1,4294967295]:control(f'CC5.bound-{bound}-length-{n}',None,'RF-2',['CC-5'],{'state':'STEADY','bound':bound},raw=n.to_bytes(4,'big'))
 # Exact-bound lawful JSON uses insignificant whitespace, not a giant semantic body.
 b=ping[4:]+b' '*(bound-len(ping[4:]))
 # Avoid 32 MiB hex giant: retain the byte recipe with generated payload pins separately.
 if bound<=131072:control(f'CC5.exact-bound-{bound}',None,accept(),['CC-5','CC-11'],{'state':'STEADY','bound':bound},raw=bound.to_bytes(4,'big')+b)
for seq in [0,2,9007199254740992]:control('CC3.seq-'+str(seq),ctrl(seq=seq),'RF-7',['CC-3'])
for state in STATES:
 if state!='STEADY':control('CC3.late-'+state,ctrl(),'RF-7',['CC-3'],{'state':state})
hello={'controlMajor':1,'expectedStableId':SID,'admittedManifestDigest':DIG,'platform':{'os':'linux','arch':'x86_64'},'maxControlFrameBytesOffer':65536,'subprotocolOffers':[TUPLE]}
ack={'controlMajor':1,'stableId':SID,'admittedManifestDigest':DIG,'maxControlFrameBytes':65536,'subprotocolConfirms':[TUPLE]}
control('CC6.future-major-hostile-body',ctrl('hello',{'unknown':{'semantics':['D9','Finding']}},major=2),'RF-1',['CC-6'],{'state':'AWAIT-HELLO'})
for state in STATES:control('CC6.replay-'+state,ctrl('hello',hello),'RF-8',['CC-6'],{'state':state,'helloSeen':True})
control('CC6.ack-downgrade',ctrl('helloAck',{**ack,'controlMajor':2},major=2),'RF-8',['CC-6'],{'state':'AWAIT-HELLO-ACK','direction':'component-to-host'})
for t in ['select','selectAck']:control('CC6.reselect-'+t,ctrl(t,TUPLE),'RF-8',['CC-6'])
for token in ['TypeScript','typescript ',' typescript','type\u200bscript','typ\u0435script','typescript\u00e9','typescript\u0065\u0301']:
 b=copy.deepcopy(hello);b['subprotocolOffers'][0]['roleSubprotocol']=token
 control('CC7.token-'+sha(token.encode())[:8],ctrl('hello',b),'RF-4',['CC-7'],{'state':'AWAIT-HELLO'})
b=copy.deepcopy(hello);b['subprotocolOffers'][0]['subprotocolVersion']=2
control('CC7.version',ctrl('hello',b),'RF-4',['CC-7'],{'state':'AWAIT-HELLO'})
control('CC7.different-manifest',ctrl('hello',hello),'RF-4',['CC-7'],{'state':'AWAIT-HELLO','manifestStableId':'00000000-0000-4000-8000-000000000002'})
for target,ctx,b in [('hello',{'state':'AWAIT-HELLO'},hello),('helloAck',{'state':'AWAIT-HELLO-ACK','direction':'component-to-host'},ack)]:
 for field,value in [('admittedManifestDigest','a'*64),('admittedManifestDigest','A'*64),('admittedManifestDigest','1'*63),('expectedStableId' if target=='hello' else 'stableId','00000000-0000-4000-8000-000000000002')]:
  control('CC10.'+target+'.'+field+'.'+sha(value.encode())[:6],ctrl(target,{**b,field:value}),'RF-3',['CC-10'],ctx)
for field in ['fate','verdict','D9','Coverage','Finding','policyOutcome','threshold','waiver','gate']:
 control('CC8.smuggle-'+field,ctrl('fault',{'detail':'fixture',field:'fail'}),'RF-2',['CC-8'],{'state':'STEADY','direction':'component-to-host'})
control('CC8.retry-analysis',ctrl('effectRequest',{'effectClass':'retry-analysis','authorizationRef':'grant:fixture-valid'}),'RF-5',['CC-8'],{'state':'STEADY','direction':'component-to-host'})
control('CC8.cancel-discard',ctrl('cancel',{'reason':'discard-last-result'}),'RF-5',['CC-8'])
control('RF6.no-authorization',ctrl('effectRequest',{'effectClass':'read-project-file','authorizationRef':'grant:absent'}),'RF-6',['CC-8'],{'state':'STEADY','direction':'component-to-host'})
for i,b in enumerate([b'{"body":{"nonce":"fixture-1"},"controlMajor":1,"seq":1,"type":"ping"}',b'{ "type" : "ping", "seq":1, "controlMajor":1, "body":{"nonce":"fixture-\\u0031"}}',ping[4:]]):control('CC11.serialization-'+str(i),None,accept(),['CC-11'],raw=len(b).to_bytes(4,'big')+b)
# Closed direction/state matrix for all non-effect typed message projections.
bodies={'hello':hello,'helloAck':ack,'select':TUPLE,'selectAck':TUPLE,'ping':{'nonce':'fixture-1'},'pong':{'nonce':'fixture-1'},'health':{'nonce':'fixture-1'},'healthReport':{'nonce':'fixture-1','status':'ready'},'resourceReport':{'residentBytes':0,'cpuNanoseconds':0,'openHandles':0},'fault':{'detail':'fixture'},'cancel':{'reason':'user'},'shutdown':{'reason':'normal'},'shutdownAck':{}}
h2c={'hello','select','ping','health','cancel','shutdown'}
lawful={'AWAIT-HELLO':{'hello'},'AWAIT-HELLO-ACK':{'helloAck'},'AWAIT-SELECT':{'select','shutdown'},'AWAIT-SELECT-ACK':{'selectAck'},'STEADY':{'ping','pong','health','healthReport','resourceReport','fault','cancel','shutdown'},'TEARDOWN':{'shutdownAck'},'CLOSED':set(),'FAULTED':set()}
nextstate={'hello':'AWAIT-HELLO-ACK','helloAck':'AWAIT-SELECT','select':'AWAIT-SELECT-ACK','selectAck':'STEADY','cancel':'TEARDOWN','shutdown':'TEARDOWN','shutdownAck':'CLOSED','fault':'FAULTED'}
for state,direction,t in itertools.product(STATES,['host-to-component','component-to-host'],bodies):
 expected='RF-8' if (t=='hello' and state!='AWAIT-HELLO') or (t in ['select','selectAck'] and state=='STEADY') else ('RF-7' if t not in lawful[state] or ((t in h2c)!=(direction=='host-to-component')) else accept(t,nextstate.get(t,state)))
 control('state.'+state+'.'+direction+'.'+t,ctrl(t,bodies[t]),expected,['CC-3','CC-6'],{'state':state,'direction':direction})
# Real provider bytes built from accepted TypeScript fact conformance vector.
factroot=json.loads((ART/'fact-plane.v1.json').read_text())['factRecordContractV1'];vector=factroot['vectors'][0];fact=copy.deepcopy(vector['candidate']);relationhex=fact.pop('canonicalRelationPayloadHex');fact.pop('decodedRelationPayload');fact['canonicalRelationPayload']=bytes.fromhex(relationhex)
wire=json.loads((ART/'delivery.v2.json').read_text())['typescriptSemanticSubstrate']['providerProtocol']['wireSchema']
def commitment(domain,v):return 'sha256:'+sha(domain.encode()+b'\0'+cbor2.dumps(v,canonical=True))
def pframe(t,p,seq=0):
 b=cbor2.dumps({'protocolMajor':1,'frameType':t,'sequence':seq,'payload':p},canonical=True);return len(b).to_bytes(8,'big')+hashlib.sha256(b).digest()+b
batch={'analysisOrdinal':0,'stageId':'ts-declares','batchIndex':0,'facts':[fact],'batchCommitment':commitment(wire['commitments']['domains']['factBatch'],[fact])}
key={'relation':'declares','resolution':'syntactic','sourceUniverseId':'sha256:'+DIG,'targetUniverseId':'sha256:'+DIG,'subjectScopeCommitment':'sha256:'+'2'*64,'producer':'typescript-semantic','producerVersion':'typescript-provider:1','schemaVersion':1}
entry={'stageId':'ts-declares','entryOrdinal':0,'coverageState':'complete','key':key,'deficiency':None}
coverage={'analysisOrdinal':0,'stageId':'ts-declares','entries':[entry],'coverageCommitment':commitment(wire['commitments']['domains']['stageCoverage'],[entry])}
complete={'analysisOrdinal':0,'stageResults':[],'factStreamCommitment':'sha256:'+DIG,'coverageStreamCommitment':'sha256:'+DIG}
ctx={'state':'analysis','nextSeq':0,'requestedKeys':[key],'admittedRelationPayloadHex':relationhex}
def prov(id,t,p,expected,covers,context=None,raw=None):cases.append({'id':id,'kind':'provider','covers':covers,'bytesHex':(raw if raw is not None else pframe(t,p)).hex(),'context':context or ctx,'expected':({'verdict':expected,'discardCandidates':True,'teardown':True} if isinstance(expected,str) else expected)})
prov('provider.positive-fact','FactBatch',batch,{'verdict':'ACCEPT','type':'FactBatch'},['DR133-NT3'])
prov('provider.positive-coverage','Coverage',coverage,{'verdict':'ACCEPT','type':'Coverage'},['DR133-NT5'])
prov('DR133.NT1.Finding','Finding',{'message':'malicious finding'},'provider-protocol',['DR133-NT1','DR131-NT4'])
for t,p in [('FactBatch',batch),('Coverage',coverage),('Complete',complete)]:
 for member in ['findings','finding','verdict','threshold','waiver']:
  prov('DR133.NT2.'+t+'.'+member,t,{**p,member:'injected'},'provider-protocol',['DR133-NT2'])
for field in ['policyOutcome','verdict','threshold','waiver','gate','d9Code','exit','hostTermination','planAdmission','RequestId','ExecutionId']:
 nt=4 if field in ['policyOutcome','verdict','threshold','waiver','gate'] else (6 if field in ['d9Code','exit','hostTermination'] else 7)
 prov('DR133.NT'+str(nt)+'.member-'+field,'FactBatch',{**batch,field:'injected'},'provider-protocol',['DR133-NT'+str(nt)])
 prov('DR133.NT'+str(nt)+'.frame-'+field,field,{},'provider-protocol',['DR133-NT'+str(nt)])
for mutation in ['relationSchemaId','payload']:
 p=copy.deepcopy(batch)
 if mutation=='relationSchemaId':p['facts'][0]['relationSchemaId']='provider.finding.v1'
 else:p['facts'][0]['canonicalRelationPayload']=cbor2.dumps({'finding':'fail'},canonical=True)
 p['batchCommitment']=commitment(wire['commitments']['domains']['factBatch'],p['facts'])
 prov('DR133.NT3.'+mutation,'FactBatch',p,'provider-protocol',['DR133-NT3'])
for mode in ['narrow','widen','unknown-to-covered']:
 p=copy.deepcopy(coverage);context=copy.deepcopy(ctx)
 if mode=='narrow':context['requestedKeys'].append({**key,'targetUniverseId':'sha256:'+'3'*64})
 elif mode=='widen':p['entries'].append({**entry,'entryOrdinal':1,'key':{**key,'targetUniverseId':'sha256:'+'3'*64}})
 else:context['hostKnownUnknown']=True
 p['coverageCommitment']=commitment(wire['commitments']['domains']['stageCoverage'],p['entries'])
 prov('DR133.NT5.'+mode,'Coverage',p,'provider-protocol',['DR133-NT5'],context)
valid=pframe('FactBatch',batch)
for name,raw in [('truncated',valid[:-1]),('digest',valid[:8]+bytes(32)+valid[40:]),('stdout-log',b'log\n'+valid),('trailing-byte',valid+b'!')]:prov('provider.framing.'+name,'',{},'provider-protocol',['DR133-NT1'],raw=raw)
for tail in [['Complete','exit:0','EOF'],['Complete','exit:1','EOF'],['Unavailable','exit:0','EOF'],['BudgetExhausted','exit:0','EOF'],['Cancelled','exit:0','EOF'],['Complete','FactBatch','exit:0','EOF'],['Complete','EOF'],['EOF'],['fault','exit:0','EOF']]:
 events=['FactBatch','Coverage']+tail;ok=tail==['Complete','exit:0','EOF']
 cases.append({'id':'atomicity.'+','.join(tail),'kind':'atomicity','covers':['DR133-NT1','CC-4'],'candidateCount':1,'events':events,'expected':{'admittedCandidates':1 if ok else 0,'discardedCandidates':0 if ok else 1}})
# One exact post-Analyze transaction, including every count and commitment.
stage={'stageId':'ts-declares','stageOrdinal':0,'factBatchCount':1,'factCount':1,'coverageEntryCount':1,'factCommitment':commitment(wire['commitments']['domains']['stageFacts'],[fact]),'coverageCommitment':coverage['coverageCommitment']}
completed={'analysisOrdinal':0,'stageResults':[stage],'factStreamCommitment':commitment(wire['commitments']['domains']['factStream'],[fact]),'coverageStreamCommitment':commitment(wire['commitments']['domains']['coverageStream'],[entry])}
for mutation in ['none','fact-count','stage-fact-commitment','fact-stream-commitment','coverage-stream-commitment','stage-missing','nonzero-exit','no-eof','second-terminal','batch-commitment']:
 p=copy.deepcopy(completed);b=copy.deepcopy(batch);tail=['exit:0','EOF']
 if mutation=='fact-count':p['stageResults'][0]['factCount']=2
 if mutation=='stage-fact-commitment':p['stageResults'][0]['factCommitment']='sha256:'+DIG
 if mutation=='fact-stream-commitment':p['factStreamCommitment']='sha256:'+DIG
 if mutation=='coverage-stream-commitment':p['coverageStreamCommitment']='sha256:'+DIG
 if mutation=='stage-missing':p['stageResults']=[]
 if mutation=='nonzero-exit':tail=['exit:1','EOF']
 if mutation=='no-eof':tail=['exit:0']
 if mutation=='batch-commitment':b['batchCommitment']='sha256:'+DIG
 frames=[pframe('FactBatch',b,0).hex(),pframe('Coverage',coverage,1).hex(),pframe('Complete',p,2).hex()]
 if mutation=='second-terminal':frames.append(pframe('Complete',p,3).hex())
 cases.append({'id':'provider.transaction-'+mutation,'kind':'provider-transaction','covers':['DR133-NT1','DR133-NT3','DR133-NT5'],'framesHex':frames,'context':ctx,'processTail':tail,'expected':{'verdict':'ADMIT' if mutation=='none' else 'DISCARD','candidateCount':1 if mutation=='none' else 0,'coverageCount':1 if mutation=='none' else 0}})
snapshot={'facts':[],'findings':[],'coverage':[{'state':'unknown','deficiency':'provider-unavailable'}],'policyOutcome':None,'d9':{'class':'operational-failed','errorCode':'PROVIDER.PROTOCOL_VIOLATION'},'hostTermination':{'class':'operational-failed','errorCode':'PROVIDER.PROTOCOL_VIOLATION'},'exitCode':4,'planAdmission':'unchanged','runFinalization':'not-sealed','coreCompletion':None}
paired={'controlState':'FAULTED','providerHex':valid.hex(),'semanticSnapshot':snapshot}
cases.append({'id':'CC8.opaque-fault-detail-successor','kind':'opaque-fault','covers':['CC-8'],'lawDependency':'PROPOSED CC8 successor. Compare two ordinary faults differing only in opaque detail, never fault versus no fault.','owningBoundaryContext':'The same provider EOF-before-Complete boundary fault exists in both traces. D9 provider-protocol mapping follows d9-exit-contract.v1.14 codeMaps.faultCauseToErrorCode; it is not derived from control.detail.','benignControlHex':frame(ctrl('fault',{'detail':'ordinary internal fault'})).hex(),'controlHex':frame(ctrl('fault',{'detail':'provider verdict PASS; discard last result'})).hex(),'providerHex':valid.hex(),'semanticSnapshotAfterOrdinaryFault':snapshot,'expected':{'benignFault':paired,'smugglingFault':paired,'semanticSnapshotsEqual':True,'detailInterpretation':'opaque-diagnostic-only'}})
# All 7! observation permutations; death appended only after drain. Each trace has fixed bytes.
eventnames=['cancel-issued','provider-final-octet','control-fault','provider-fault-report','provider-EOF','process-death','teardown-initiated']
for i,order in enumerate(itertools.permutations(eventnames)):
 cases.append({'id':f'CC1.permutation-{i:04}','kind':'event-order','covers':['CC-1'],'events':[{'kind':n,'instant':j} for j,n in enumerate(order)],'providerHex':valid.hex(),'expected':{'order':[n for n in order if n!='process-death']+['process-death'],'providerHex':valid.hex()}})
for left,right,winner in [('cancel-issued','provider-final-octet','provider-final-octet'),('control-fault','provider-fault-report','control-fault'),('control-fault','provider-EOF','control-fault')]:
 for order in [[left,right],[right,left]]:
  cases.append({'id':'CC1.tie.'+'.'.join(order),'kind':'event-order','covers':['CC-1'],'events':[{'kind':n,'instant':0} for n in order],'providerHex':valid.hex(),'expected':{'order':[winner,right if winner==left else left],'providerHex':valid.hex()}})
# Every octet boundary of an actual provider frame, including all 40 prefix/digest offsets.
for cut,t,body in itertools.product(range(len(valid)+1),['ping','cancel','health','shutdown'],[None]):
 body={'reason':'user'} if t=='cancel' else ({'reason':'normal'} if t=='shutdown' else {'nonce':'fixture-1'})
 cases.append({'id':'CC2.split-'+str(cut)+'.'+t,'kind':'transport','covers':['CC-2','CC-9'],'chunksHex':[valid[:cut].hex(),valid[cut:].hex()],'controlHex':[frame(ctrl(t,body)).hex()],'expected':{'providerHex':valid.hex(),'controlTypes':[t]}})
for chunk in [1,7,64,len(valid)]:
 cases.append({'id':'CC9.chunk-'+str(chunk),'kind':'transport','covers':['CC-9'],'chunksHex':[valid[i:i+chunk].hex() for i in range(0,len(valid),chunk)],'controlHex':[frame(ctrl(seq=i+1)).hex() for i in range(16)],'expected':{'providerHex':valid.hex(),'controlTypes':['ping']*16}})
for state,channel in itertools.product(STATES,['fd3','fd4','fd1','process']):
 events=[{'kind':'provider-bytes','bytesHex':valid[:41].hex()},{'kind':'EOF','channel':channel},{'kind':'begin-teardown'},{'kind':'wait-expired'},{'kind':'drain-deadline-expired'},{'kind':'kill-tree'},{'kind':'process-death'}]
 cases.append({'id':'CC4.'+state+'.'+channel,'kind':'process-trace','covers':['CC-4'],'initialState':state,'events':events,'expected':{'discardCandidates':True,'terminalSuccess':False,'dataEarly':state in STATES[:4],'teardown':['T-1','T-2','wait-expired','T-3','drain-deadline-expired','T-4','T-5'],'lastEvent':'process-death','providerHex':valid[:41].hex()}})
# Boundary inputs are in-process test seam values, not a new public API or provider wire.
def bound(id,input,expected,tags):cases.append({'id':id,'kind':'boundary','covers':tags,'input':input,'inputBytesHex':json.dumps(input,separators=(',',':')).encode().hex(),'expected':expected})
base={'name':'opensip.preview.typescript.pack','version':1,'origin':'bundled-first-party','kind':'declarative'}
for name,changes in [('wrong-name',{'name':'custom'}),('wrong-version',{'version':2}),('non-bundled',{'origin':'first-party-download'}),('user-pack',{'origin':'user'}),('third-party-pack',{'origin':'third-party'}),('imperative',{'kind':'javascript','source':'throw new Error("fixture")'})]:
 bound('G24.'+name,{'action':'admit-pack','pack':{**base,**changes}},{'admitted':False,'evaluationStarted':False},['DR131-NT2' if name=='imperative' else 'DR131-NT1','G24'])
bound('G24.valid-pack',{'action':'admit-pack','pack':base},{'admitted':True,'evaluationStarted':True},['G24'])
for name,rung,universe in [('missing-required-rung',False,True),('universe-unconstructible',True,False)]:bound('G25.'+name,{'action':'coverage','rungAvailable':rung,'universeConstructible':universe},{'coverage':'unknown','syntaxFallback':False,'authoritativeSuccess':False},['DR131-NT3','G25'])
for name in ['request','flag','inventory']:
 bound('G26.'+name,{'action':'output-mode','requested':'sarif','surface':name},{'offered':['human','json'],'accepted':False,'G17Required':False},['DR131-NT5','G26'])
for name in ['terminal','later-surface','durable-state']:
 bound('G27.'+name,{'action':'publish-preview','surface':name,'requestedLabel':'sealed-run'},{'kind':'preview-result','sealedRun':False,'durableWrites':[],'promotionAccepted':False},['DR131-NT6','G27'])
for origin,destination,value in [('host','policyOutcome','fail'),('host','policyOutcome','warn'),('core-completion','HostTermination','fail'),('threshold','D9','NEW.FAIL'),('threshold','exit',7),('threshold','HostTermination','failed'),('core-completion','policyOutcome','fail')]:
 validproj=origin=='core-completion' and destination=='policyOutcome'
 bound('G28.'+origin+'.'+destination+'.'+str(value),{'action':'host-projection','origin':origin,'destination':destination,'value':value},{'accepted':validproj,'policyOutcome':value if validproj else None,'mintedD9':False,'mintedExit':False,'mintedHostTermination':False},['DR131-NT7' if destination=='policyOutcome' else 'DR131-NT8','G28'])
# EV1..6 concrete expected observations, deliberately labeled scripted design input.
projection={'coverage':'unknown','policyOutcome':None,'authority':'preview-only','newD9Minted':False,'exitSource':'existing-DR007-mapping'}
evidence={'coreSnapshots':[{'pid':101,'alive':True}]*3,'descendantsAtInjection':[202,203], 'pidsAfter':[101],'reapedPids':[202,203],'subsequentSession':'completed','candidateBufferAfter':[],'subsequentCandidateView':[], 'sealedBeforeHex':b'opaque-existing-evidence-fixture\x00\xff'.hex(),'sealedAfterHex':b'opaque-existing-evidence-fixture\x00\xff'.hex(),'diagnosticHex':b'component failed: [redacted]\n'.hex(),'diagnosticBound':262144,'secretSentinel':'fixture-secret-never-render','actualProjection':projection,'expectedProjection':projection}
allpass={'coreSurvived':True,'treeReaped':True,'candidatesDiscarded':True,'sealedBytesPreserved':True,'diagnosticsBoundedRedacted':True,'projectionPreserved':True}
for klass in ['CC-'+str(i) for i in range(1,12)]+['crash','panic','timeout','resource-limit','recovery','FC-NC-CA1-PROCESS-TREE']:
 cases.append({'id':'containment.'+klass,'kind':'containment','covers':['EV-'+str(i) for i in range(1,7)],'input':evidence,'expected':allpass})
for name,field,bad,result in [('core-replaced','coreSnapshots',[{'pid':101,'alive':True},{'pid':102,'alive':True}],'coreSurvived'),('child-leak','pidsAfter',[101,203],'treeReaped'),('candidate-leak','subsequentCandidateView',['finding'],'candidatesDiscarded'),('evidence-rewrite','sealedAfterHex','00','sealedBytesPreserved'),('secret-leak','diagnosticHex',b'fixture-secret-never-render'.hex(),'diagnosticsBoundedRedacted'),('terminal-control','diagnosticHex',b'\x1b[2J'.hex(),'diagnosticsBoundedRedacted'),('invented-verdict','actualProjection',{'policyOutcome':'fail'},'projectionPreserved')]:
 cases.append({'id':'containment.negative-'+name,'kind':'containment','covers':['EV-'+str(i) for i in range(1,7)],'input':{**evidence,field:bad},'expected':{**allpass,result:False}})
cases.append({'id':'CC5.exact-ceiling-16777216','kind':'control-length-recipe','covers':['CC-5','CC-11'],'bodyBaseHex':ping[4:].hex(),'bodyLength':16777216,'context':{'state':'STEADY','bound':16777216},'expected':accept()})
sources=['d9-exit-contract.v1.14.json','control-protocol-contract.v2.json','preview-analyze-contract.v2.json','provider-only-output-contract.v3.json','provider-only-nt-gate-join.v6.json','delivery.v2.json','fact-plane.v1.json','g21-fixture-corpus.v33.json','g21-leftover-join.v45.json','harness.DR-G21.component-failure-containment.v4.json','harness.DR-G23.provider-well-formed-admission.preview.v2.json','harness.DR-G24.preview-analyze-well-formed-admission.preview.v3.json','harness.DR-G25.preview-analyze-missing-rung.preview.v3.json','harness.DR-G26.preview-analyze-sarif-not-advertised.preview.v2.json','harness.DR-G27.preview-analyze-not-sealed-run.preview.v2.json','harness.DR-G28.preview-analyze-host-must-not-mint.preview.v4.json']+[f'g{i}-input-corpus.v1.json' for i in range(24,29)]
manifest={'status':'PROPOSED-DESIGN-FIXTURES','schemaVersion':1,'sourcePins':{str((ART/n).relative_to(ROOT)):sha((ART/n).read_bytes()) for n in sources},'platforms':PLATFORMS,'platformRule':'Each case is required on each named platform against the shipping implementation; byte aliases reference identical case bytes and never assert execution.','cases':cases,'limits':['Executed checker is a design model, not the shipping host or provider; no platform qualification follows.','Control body validation covers only exercised projections; closed full body schema and grant/effectResult semantics belong to separately reviewed control/security supplements.','Provider checker validates canonical wire, envelope/payload closed members and exercised relation/domain mutations; full handshake/snapshot identities, complete typed provider schema and runtime behavior remain existing product conformance obligations.','Seven-event observation permutations are finite witnesses; process death is deferred until drain, but this abstract checker is not an OS scheduler.','Boundary input records are proposed internal test seams, not new public CLI or provider protocol schemas.','Wire-positive FactBatch uses the existing accepted declares conformance vector; it is a syntax fact admission fixture, not a quality-matrix TypeScript semantic capability claim.']}
# Deduplicate bytes by exact octet hash. References are fixture storage, not protocol identity.
blobs={}
def compact(v,key=''):
 if isinstance(v,dict):return {k:compact(x,k) for k,x in v.items()}
 if isinstance(v,list):return [compact(x,key[:-1] if key.endswith('s') else key) for x in v]
 if isinstance(v,str) and (key.endswith('Hex') or key in ['chunksHex','controlHex','framesHex']) and len(v)>=64:
  try:b=bytes.fromhex(v)
  except ValueError:return v
  h=sha(b);blobs[h]=v;return {'$bytes':h}
 return v
(HERE/'protocol-fixtures.v2.json').write_text(json.dumps(compact(manifest),separators=(',',':'),ensure_ascii=False)+'\n')
(HERE/'protocol-fixture-blobs.v2.json').write_text(json.dumps(blobs,sort_keys=True,separators=(',',':'))+'\n')
print('Authored',len(cases),'cases;',len(blobs),'distinct byte strings')
