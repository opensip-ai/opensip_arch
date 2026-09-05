#!/usr/bin/env python3
"""Build retained control schema and independently specified reference fixtures."""
import copy, hashlib, itertools, json
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];ART=ROOT/'docs/coop/artifacts'
def sha(b):return hashlib.sha256(b).hexdigest()
def obj(props,required=None):return {'type':'object','properties':props,'required':list(props) if required is None else required,'additionalProperties':False}
def string(n=1024):return {'type':'string','minLength':1,'maxLength':n,'x-maxUtf8Bytes':n}
uint={'type':'integer','minimum':0,'maximum':9007199254740991};pos={**uint,'minimum':1}
schema=json.loads((HERE/'control-message-schema.v1.json').read_text());schema['$id']='urn:opensip:design:control-schema:3';schema['title']='PROPOSED completed closed control major1 body schemas; independently reviewed application required'
bytype={x['properties']['type']['const']:x for x in schema['oneOf']}
# Retain the accepted hello/ack/select fields. Strings keep exact codepoints.
for name in ['hello','helloAck','select','selectAck']:
 def annotate(v):
  if isinstance(v,dict):
   if v.get('type')=='string':v['x-maxUtf8Bytes']=v.get('maxLength',1024)
   for x in v.values():annotate(x)
  elif isinstance(v,list):
   for x in v:annotate(x)
 annotate(bytype[name])
for name in ['ping','pong','health','healthReport']:bytype[name]['properties']['body']['properties']['nonce']=string(128)
for name in ['fault','refusal']:
 p=bytype[name]['properties']['body']['properties']['detail'];p['x-maxUtf8Bytes']=1024
refusal=obj({'family':{'enum':['RF-'+str(i) for i in range(1,9)]},'supportedControlMajors':{'type':'array','items':pos,'minItems':1,'maxItems':16,'uniqueItems':True},'decisionClass':{'enum':['PR-'+str(i) for i in range(1,10)]},'detail':{'type':'string','maxLength':1024,'x-maxUtf8Bytes':1024}},['family'])
refusal['allOf']=[{'if':{'properties':{'family':{'const':'RF-1'}}},'then':{'required':['supportedControlMajors']},'else':{'not':{'required':['supportedControlMajors']}}},{'if':{'properties':{'family':{'const':'RF-6'}}},'then':{'required':['decisionClass']},'else':{'not':{'required':['decisionClass']}}}]
bytype['refusal']['properties']['body']=refusal
bytype['effectRequest']['properties']['body']=obj({'effectClass':{'enum':['HE-1','HE-2']},'authorizationRef':string(1024),'operationRef':string(1024)})
bytype['effectResult']['properties']['body']=obj({'requestSeq':pos,'decisionSeq':pos,'outcomeSeq':pos,'commitClass':{'enum':['REVERSIBLE','IRREVERSIBLE']},'effectOutcome':{'enum':['COMPLETED','FAILED','INDETERMINATE']},'resultRef':string(1024)},['requestSeq','decisionSeq','outcomeSeq','commitClass','effectOutcome'])
assert schema==json.loads((HERE/'control-completion.schema.v3.json').read_text()), 'frozen schema drift'
SID='00000000-0000-4000-8000-000000000001';DIG='1'*64;TUPLE={'role':'semantic-provider','roleSubprotocol':'typescript','subprotocolVersion':1};PLATFORM={'os':'linux','arch':'x86_64'}
body={'hello':{'controlMajor':1,'expectedStableId':SID,'admittedManifestDigest':DIG,'platform':PLATFORM,'maxControlFrameBytesOffer':65536,'subprotocolOffers':[TUPLE]},'helloAck':{'controlMajor':1,'stableId':SID,'admittedManifestDigest':DIG,'maxControlFrameBytes':65536,'subprotocolConfirms':[TUPLE]},'select':TUPLE,'selectAck':TUPLE,'refusal':{'family':'RF-2'},'ping':{'nonce':'nonce-1'},'pong':{'nonce':'nonce-1'},'cancel':{'reason':'user'},'health':{'nonce':'nonce-1'},'healthReport':{'nonce':'nonce-1','status':'ready'},'resourceReport':{'residentBytes':0,'cpuNanoseconds':0,'openHandles':0},'fault':{'detail':'ordinary fault'},'effectRequest':{'effectClass':'HE-1','authorizationRef':'opaque-grant-record-fixture','operationRef':'opaque-operation-fixture'},'effectResult':{'requestSeq':12,'decisionSeq':40,'outcomeSeq':41,'commitClass':'REVERSIBLE','effectOutcome':'COMPLETED'},'shutdown':{'reason':'normal'},'shutdownAck':{}}
CTX={'state':'STEADY','direction':'host-to-component','helloSeen':True,'frameBound':65536,'frameOffer':65536,'nextSeq':1,'stableId':SID,'manifestDigest':DIG,'platform':PLATFORM,'manifestTuples':[TUPLE],'offeredTuples':[TUPLE],'confirmedTuples':[TUPLE],'selectedTuple':TUPLE,'pendingNonce':{'pong':'nonce-1','healthReport':'nonce-1'},'authorizationEvidence':{'authorized':True,**body['effectRequest'],'decisionClass':None,'bindingMismatchDecisionClass':'PR-4'},'effectOutcomeEvidence':{**body['effectResult'],'effectClass':'HE-1'}}
STATES=['AWAIT-HELLO','AWAIT-HELLO-ACK','AWAIT-SELECT','AWAIT-SELECT-ACK','STEADY','TEARDOWN','CLOSED','FAULTED'];H2C={'hello','select','refusal','ping','cancel','health','effectResult','shutdown'};C2H={'helloAck','selectAck','refusal','pong','healthReport','resourceReport','fault','effectRequest','shutdownAck'}
allowed={'AWAIT-HELLO':{'hello','refusal'},'AWAIT-HELLO-ACK':{'helloAck','refusal'},'AWAIT-SELECT':{'select','shutdown','refusal'},'AWAIT-SELECT-ACK':{'selectAck','refusal'},'STEADY':set(body)-{'hello','helloAck','select','selectAck','shutdownAck'},'TEARDOWN':{'shutdownAck','refusal'},'CLOSED':set(),'FAULTED':{'refusal'}}
nextstate={'hello':'AWAIT-HELLO-ACK','helloAck':'AWAIT-SELECT','select':'AWAIT-SELECT-ACK','selectAck':'STEADY','shutdown':'TEARDOWN','cancel':'TEARDOWN','shutdownAck':'CLOSED','fault':'FAULTED','refusal':'FAULTED'}
cases=[]
def envelope(t,b=None,seq=1,major=1):return {'type':t,'seq':seq,'controlMajor':major,'body':copy.deepcopy(body[t] if b is None else b)}
def frame(v):
 b=json.dumps(v,separators=(',',':'),ensure_ascii=False).encode();return len(b).to_bytes(4,'big')+b

def expected_accept(t,state='STEADY',family='RF-2'):return {'verdict':'ACCEPT','type':t,'nextState':nextstate.get(t,state),'bodyBuffered':True,**({'terminalFamily':family} if t=='refusal' else {})}
def add(id,t,expected,ctx=None,v=None,raw=None,decision=None,buffered=True):
 context=copy.deepcopy(CTX);context.update(ctx or {})
 cases.append({'id':id,'messageType':t,'context':context,'frameHex':(raw if raw is not None else frame(v if v is not None else envelope(t))).hex(),'expected':({'verdict':expected,'nextState':'FAULTED','bodyBuffered':buffered,**({'decisionClass':decision} if decision else {})} if isinstance(expected,str) else expected)})
for t,state,direction in itertools.product(body,STATES,['host-to-component','component-to-host']):
 if t not in (H2C if direction=='host-to-component' else C2H):e='RF-7'
 elif t=='hello' and state!='AWAIT-HELLO':e='RF-8'
 elif t in ['select','selectAck'] and state=='STEADY':e='RF-8'
 elif t not in allowed[state]:e='RF-7'
 else:e=expected_accept(t,state)
 add('MATRIX/'+t+'/'+state+'/'+direction,t,e,{'state':state,'direction':direction,'helloSeen':state!='AWAIT-HELLO'})
# Closed schema missing/unknown fields are exercised for all sixteen types.
for t in body:
 state=next(s for s in STATES if t in allowed[s]);direction='host-to-component' if t in H2C else 'component-to-host';ctx={'state':state,'direction':direction,'helloSeen':False}
 add('SCHEMA/'+t+'/unknown',t,'RF-2',ctx,v=envelope(t,{**body[t],'unknown':0}))
 for field in body[t]:
  b=copy.deepcopy(body[t]);b.pop(field);add('SCHEMA/'+t+'/missing-'+field,t,'RF-2',ctx,v=envelope(t,b))
# Frozen refusal conditionals, including every permission decision refinement.
for n in range(1,9):
 b={'family':'RF-'+str(n)}
 if n==1:b['supportedControlMajors']=[1]
 if n==6:b['decisionClass']='PR-1'
 add('REFUSAL/family-'+str(n),'refusal',expected_accept('refusal',family=b['family']),v=envelope('refusal',b))
for n in range(1,10):
 b={'family':'RF-6','decisionClass':'PR-'+str(n)};add('REFUSAL/permission-'+str(n),'refusal',expected_accept('refusal',family='RF-6'),v=envelope('refusal',b))
for label,b in [('rf1-missing',{'family':'RF-1'}),('rf1-empty',{'family':'RF-1','supportedControlMajors':[]}),('rf1-duplicate',{'family':'RF-1','supportedControlMajors':[1,1]}),('rf6-missing',{'family':'RF-6'}),('rf6-outside',{'family':'RF-6','decisionClass':'PR-10'}),('wrong-family-majors',{'family':'RF-2','supportedControlMajors':[1]}),('wrong-family-permission',{'family':'RF-7','decisionClass':'PR-1'})]:add('REFUSAL/'+label,'refusal','RF-2',v=envelope('refusal',b))
# Host decision records are external validated inputs, never fabricated grant carriers.
for n in range(1,10):
 evidence={**CTX['authorizationEvidence'],'authorized':False,'decisionClass':'PR-'+str(n)}
 add('EFFECT/request-denied-'+str(n),'effectRequest','RF-6',{'direction':'component-to-host','authorizationEvidence':evidence},decision='PR-'+str(n))
add('EFFECT/request-unknown-class','effectRequest','RF-2',{'direction':'component-to-host'},v=envelope('effectRequest',{**body['effectRequest'],'effectClass':'HE-3'}))
add('EFFECT/opaque-operation-reference','effectRequest',expected_accept('effectRequest'),{'direction':'component-to-host'})
add('EFFECT/wrong-direction','effectRequest','RF-7')
for field in ['authorizationRef','operationRef']:
 add('EFFECT/binding-'+field,'effectRequest','RF-6',{'direction':'component-to-host'},v=envelope('effectRequest',{**body['effectRequest'],field:'different'}),decision='PR-4')
for effect,commit,outcome in itertools.product(['HE-1','HE-2'],['REVERSIBLE','IRREVERSIBLE'],['COMPLETED','FAILED','INDETERMINATE']):
 b={**body['effectResult'],'commitClass':commit,'effectOutcome':outcome};evidence={**b,'effectClass':effect};e='RF-7' if effect=='HE-2' and commit=='IRREVERSIBLE' else expected_accept('effectResult')
 add('EFFECT/result-'+effect+'-'+commit+'-'+outcome,'effectResult',e,{'effectOutcomeEvidence':evidence},v=envelope('effectResult',b))
for field,val in [('requestSeq',13),('decisionSeq',39),('outcomeSeq',40),('commitClass','IRREVERSIBLE'),('effectOutcome','FAILED')]:add('EFFECT/correlation-'+field,'effectResult','RF-7',v=envelope('effectResult',{**body['effectResult'],field:val}))
for forbidden in ['DEFINITELY_NOT_PERFORMED','COMPLETED-BEFORE-REVOCATION','REJECTED']:add('EFFECT/forbidden-'+forbidden,'effectResult','RF-2',v=envelope('effectResult',{**body['effectResult'],'effectOutcome':forbidden}))
# Independent UTF-8 byte limits; JSON Schema character max alone cannot pass these.
for t,field,bound in [('fault','detail',1024),('ping','nonce',128),('effectRequest','operationRef',1024),('effectRequest','authorizationRef',1024),('effectResult','resultRef',1024)]:
 for kind,value,ok in [('ascii-at','a'*bound,True),('ascii-over','a'*(bound+1),False),('utf8-at','é'*(bound//2),True),('utf8-over','é'*(bound//2)+'a',False)]:
  b={**body[t],field:value};ctx={'direction':'component-to-host' if t in ['fault','effectRequest'] else 'host-to-component'}
  if t=='effectRequest':ctx['authorizationEvidence']={**CTX['authorizationEvidence'],field:value}
  add('UTF8/'+t+'/'+field+'/'+kind,t,expected_accept(t) if ok else 'RF-2',ctx,v=envelope(t,b))
# Exact hello identity/body/tuple tests.
for t in ['hello','helloAck']:
 ctx={'state':'AWAIT-HELLO' if t=='hello' else 'AWAIT-HELLO-ACK','direction':'host-to-component' if t=='hello' else 'component-to-host','helloSeen':False}
 add('HELLO/'+t+'/identity',t,'RF-3',ctx,v=envelope(t,{**body[t],('expectedStableId' if t=='hello' else 'stableId'):'00000000-0000-4000-8000-000000000002'}))
 add('HELLO/'+t+'/digest',t,'RF-3',ctx,v=envelope(t,{**body[t],'admittedManifestDigest':'2'*64}))
 field='subprotocolOffers' if t=='hello' else 'subprotocolConfirms'
 add('HELLO/'+t+'/undeclared',t,'RF-4',ctx,v=envelope(t,{**body[t],field:[{**TUPLE,'roleSubprotocol':'TypeScript'}]}))
 add('HELLO/'+t+'/body-major',t,'RF-8',ctx,v=envelope(t,{**body[t],'controlMajor':2}))
add('HELLO/ack-over-offer','helloAck','RF-2',{'state':'AWAIT-HELLO-ACK','direction':'component-to-host'},v=envelope('helloAck',{**body['helloAck'],'maxControlFrameBytes':65537}))
add('HELLO/future-hostile-body','hello','RF-1',{'state':'AWAIT-HELLO','helloSeen':False},v=envelope('hello',{'unknownFutureMember':{'D9':'PASS','floatAllowedInFuture':1.25}},major=2))
for t in ['pong','healthReport']:add('CORRELATION/'+t,t,'RF-7',{'direction':'component-to-host'},v=envelope(t,{**body[t],'nonce':'unmatched'}))
for seq in [0,2,9007199254740992]:add('SEQUENCE/'+str(seq),'ping','RF-7',v=envelope('ping',seq=seq))
# No numeric forms other than JSON integer lexical forms; sequence overflow keeps RF7.
for name,b in [('float',b'{"type":"ping","seq":1.0,"controlMajor":1,"body":{"nonce":"nonce-1"}}'),('negative',b'{"type":"ping","seq":1,"controlMajor":-1,"body":{}}'),('duplicate',b'{"type":"ping","seq":1,"seq":1,"controlMajor":1,"body":{}}'),('unknown-envelope',b'{"type":"ping","seq":1,"controlMajor":1,"body":{},"extra":0}'),('invalid-utf8',b'\x80'),('non-object',b'[]')]:add('FRAMING/'+name,'ping','RF-2',raw=len(b).to_bytes(4,'big')+b)
raw=frame(envelope('ping'));add('FRAMING/truncated','ping','RF-2',raw=raw[:-1])
for bound in [65536,131072,16777216]:
 for length in [0,bound+1,4294967295]:add('FRAMING/bound-'+str(bound)+'-length-'+str(length),'ping','RF-2',{'frameBound':bound},raw=length.to_bytes(4,'big'),buffered=False)
 cases.append({'id':'FRAMING/exact-'+str(bound),'messageType':'ping','context':{**copy.deepcopy(CTX),'frameBound':bound},'frameRecipe':{'length':bound,'baseHex':frame(envelope('ping'))[4:].hex()},'expected':expected_accept('ping')})
for t in ['hello','helloAck']:
 ctx={'state':'AWAIT-HELLO' if t=='hello' else 'AWAIT-HELLO-ACK','direction':'host-to-component' if t=='hello' else 'component-to-host','helloSeen':False}
 for label,value in [('uppercase','A'*64),('truncated','1'*63)]:add('IDENTITY/'+t+'/'+label,t,'RF-3',ctx,v=envelope(t,{**body[t],'admittedManifestDigest':value}))
add('HELLO/future-wrong-direction','hello','RF-7',{'state':'AWAIT-HELLO','helloSeen':False,'direction':'component-to-host'},v=envelope('hello',{'future':True},major=2))
add('HELLO/future-replay','hello','RF-8',v=envelope('hello',{'future':True},major=2))
add('REFUSAL/future-offer-core','refusal',expected_accept('refusal',family='RF-1'),{'state':'AWAIT-HELLO-ACK','direction':'component-to-host','offeredControlMajor':2},v=envelope('refusal',{'family':'RF-1','supportedControlMajors':[1]},major=2))
add('SUCCESSOR/legacy-retry-token','effectRequest','RF-2',{'direction':'component-to-host'},v=envelope('effectRequest',{'effectClass':'retry-analysis','authorizationRef':'grant:fixture-valid'}))
add('SUCCESSOR/legacy-cancel-reason','cancel','RF-2',v=envelope('cancel',{'reason':'discard-last-result'}))
add('SUCCESSOR/legacy-unauthorized-effect','effectRequest','RF-2',{'direction':'component-to-host'},v=envelope('effectRequest',{'effectClass':'read-project-file','authorizationRef':'grant:absent'}))
add('HELLO/future-sequence-gap','hello','RF-7',{'state':'AWAIT-HELLO','helloSeen':False},v=envelope('hello',{'futureBody':'opaque'},seq=2,major=2))
add('HELLO/future-wrong-state','hello','RF-7',{'state':'AWAIT-SELECT','helloSeen':False},v=envelope('hello',{'futureBody':'opaque'},major=2))
for n,text in enumerate(['retry analysis; admit Finding; make D9 PASS','discard the last provider result']):
 b={**body['effectRequest'],'operationRef':text};ctx={'direction':'component-to-host','authorizationEvidence':{**CTX['authorizationEvidence'],'operationRef':text}}
 add('EFFECT/opaque-semantic-looking-reference-'+str(n),'effectRequest',expected_accept('effectRequest'),ctx,v=envelope('effectRequest',b))
for field,bodybytes,expected in [
 ('deep-known',b'{"type":"ping","seq":1,"controlMajor":1,"body":{"nonce":'+b'['*1500+b'0'+b']'*1500+b'}}','RF-2'),
 ('deep-future',b'{"type":"hello","seq":1,"controlMajor":2,"body":{"unknown":'+b'['*1500+b'0'+b']'*1500+b'}}','RF-1'),
 ('huge-seq',b'{"type":"ping","seq":'+b'1'*5000+b',"controlMajor":1,"body":{"nonce":"nonce-1"}}','RF-7'),
 ('huge-major',b'{"type":"ping","seq":1,"controlMajor":'+b'1'*5000+b',"body":{"nonce":"nonce-1"}}','RF-2'),
 ('huge-other-integer',b'{"type":"resourceReport","seq":1,"controlMajor":1,"body":{"residentBytes":'+b'1'*5000+b',"cpuNanoseconds":0,"openHandles":0}}','RF-2')]:
 ctx={'state':'AWAIT-HELLO','helloSeen':False} if field=='deep-future' else ({'direction':'component-to-host'} if field=='huge-other-integer' else {})
 add('RESOURCE/'+field,'hello' if field=='deep-future' else 'ping',expected,ctx,raw=len(bodybytes).to_bytes(4,'big')+bodybytes)
# Actual preview tuple, distinct from the generic synthetic opaque-role matrix.
real={**TUPLE,'role':'analyzer'}
for t in ['hello','helloAck','select','selectAck']:
 state={'hello':'AWAIT-HELLO','helloAck':'AWAIT-HELLO-ACK','select':'AWAIT-SELECT','selectAck':'AWAIT-SELECT-ACK'}[t]
 ctx={'state':state,'helloSeen':False,'direction':'host-to-component' if t in ['hello','select'] else 'component-to-host','manifestTuples':[real],'offeredTuples':[real],'confirmedTuples':[real],'selectedTuple':real}
 b=copy.deepcopy(body[t])
 if t=='hello':b['subprotocolOffers']=[real]
 elif t=='helloAck':b['subprotocolConfirms']=[real]
 else:b=real
 add('PREVIEW-HANDSHAKE/'+t,t,expected_accept(t,state),ctx,v=envelope(t,b))
# CCR-1: applicable structural faults outrank simultaneous sequence range faults.
add('PRECEDENCE/zero-seq-unknown-body','ping','RF-2',v=envelope('ping',{'nonce':'nonce-1','unknown':True},seq=0))
add('PRECEDENCE/overflow-seq-array-body','ping','RF-2',v=envelope('ping',[],seq=9007199254740992))
add('PRECEDENCE/zero-seq-unknown-type','not-a-type','RF-2',v={'type':'not-a-type','seq':0,'controlMajor':1,'body':{}})
add('PRECEDENCE/zero-seq-body-float','resourceReport','RF-2',{'direction':'component-to-host'},v=envelope('resourceReport',{**body['resourceReport'],'residentBytes':1.0},seq=0))
for name,b,expected in [
 ('huge-seq-string-major',b'{"type":"ping","seq":'+b'1'*5000+b',"controlMajor":"1","body":{"nonce":"nonce-1"}}','RF-2'),
 ('huge-seq-bad-body',b'{"type":"ping","seq":'+b'1'*5000+b',"controlMajor":1,"body":{"nonce":true}}','RF-2'),
 ('future-zero-opaque-body',b'{"type":"hello","seq":0,"controlMajor":2,"body":{"unknown":1.25}}','RF-7'),
 ('future-zero-array-body',b'{"type":"hello","seq":0,"controlMajor":2,"body":[]}','RF-2')]:
 ctx={'state':'AWAIT-HELLO','helloSeen':False} if name.startswith('future') else {}
 add('PRECEDENCE/'+name,'hello' if name.startswith('future') else 'ping',expected,ctx,raw=len(b).to_bytes(4,'big')+b)
# A real two-direction supervisor trace, not disconnected FAULTED contexts.
trace_frames=[
 {'direction':'host-to-component','frameHex':frame(envelope('ping',{'nonce':'nonce-1','unknown':True})).hex()},
 {'direction':'host-to-component','frameHex':frame(envelope('ping')).hex()},
 {'direction':'component-to-host','frameHex':frame(envelope('refusal',{'family':'RF-2'})).hex()},
 {'direction':'component-to-host','frameHex':frame(envelope('refusal',{'family':'RF-2'},seq=2)).hex()},
 {'direction':'host-to-component','frameHex':frame(envelope('ping')).hex()}]
steps=[]
for verdict,buffered,state,stopped,next_c in [
 ('RF-2',True,'FAULTED',['host-to-component'],1),
 ('RF-7',False,'FAULTED',['host-to-component'],1),
 ('ACCEPT',True,'CLOSED',['component-to-host','host-to-component'],2),
 ('RF-7',False,'CLOSED',['component-to-host','host-to-component'],2),
 ('RF-7',False,'CLOSED',['component-to-host','host-to-component'],2)]:steps.append({'verdict':verdict,'bodyBuffered':buffered,'state':state,'stoppedDirections':stopped,'nextSeq':{'host-to-component':1,'component-to-host':next_c}})
cases.append({'id':'TEARDOWN/two-direction-stopped-receiver','messageType':'session','context':copy.deepcopy(CTX),'sessionFrames':trace_frames,'expected':{'verdict':'TRACE','steps':steps}})
sources=['control-protocol-contract.v2.json','permission-truth-tables.v9.json'];pins={str((ART/n).relative_to(ROOT)):sha((ART/n).read_bytes()) for n in sources}
corpus={'status':'PROPOSED-DESIGN-EVIDENCE','sourcePins':pins,'contextPins':{'security-completion.v1.md':sha((HERE/'security-completion.v1.md').read_bytes()),'control-message-schema.v1.json':sha((HERE/'control-message-schema.v1.json').read_bytes())},'platformExecutionAliases':['macos/arm64','macos/x86_64','linux/x86_64','linux/arm64'],'cases':cases,'limits':['External authorization/outcomeEvidence fields are test-seam observations supplied by the host permission/journal owner, not a grant carrier or proof that an effect executed.','Pending security review SEC-M2/M5 must supply actual durable evidence and locator grammar; this package cannot activate effects alone.','Reference framing/schema/state execution is design evidence only; no shipping host or four-platform qualification.','Nonce and free-text limits are chosen design constants; UTF8 byte limits are independently checked after JSON decoding.','This complete state/direction successor resolves overlapping specific replay and wrong-direction rules: wrong direction RF7 precedes lawful-direction RF8 replay; refusal is receivable on a still-readable FAULTED channel but never CLOSED.']}
(HERE/'control-completion.cases.v4.json').write_text(json.dumps(corpus,indent=2,ensure_ascii=False)+'\n');print('Authored',len(cases),'control cases')
