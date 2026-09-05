#!/usr/bin/env python3
"""Closed control schema/framing/state reference checks, never a product harness."""
import argparse, copy, hashlib, json, re
from pathlib import Path
from jsonschema import Draft202012Validator
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
SCHEMA=json.loads((HERE/'control-completion.schema.v3.json').read_text())
SCHEMAS={s['properties']['type']['const']:s for s in SCHEMA['oneOf']}
VALIDATORS={k:Draft202012Validator(v) for k,v in SCHEMAS.items()}
STATES=['AWAIT-HELLO','AWAIT-HELLO-ACK','AWAIT-SELECT','AWAIT-SELECT-ACK','STEADY','TEARDOWN','CLOSED','FAULTED']
H2C={'hello','select','ping','health','cancel','shutdown','effectResult','refusal'}
C2H={'helloAck','selectAck','pong','healthReport','resourceReport','fault','shutdownAck','effectRequest','refusal'}
LAWFUL={'AWAIT-HELLO':{'hello','refusal'},'AWAIT-HELLO-ACK':{'helloAck','refusal'},'AWAIT-SELECT':{'select','shutdown','refusal'},'AWAIT-SELECT-ACK':{'selectAck','refusal'},'STEADY':{'ping','pong','health','healthReport','resourceReport','fault','cancel','shutdown','effectRequest','effectResult','refusal'},'TEARDOWN':{'shutdownAck','refusal'},'CLOSED':set(),'FAULTED':{'refusal'}}
NEXT={'hello':'AWAIT-HELLO-ACK','helloAck':'AWAIT-SELECT','select':'AWAIT-SELECT-ACK','selectAck':'STEADY','shutdown':'TEARDOWN','cancel':'TEARDOWN','shutdownAck':'CLOSED','fault':'FAULTED','refusal':'FAULTED'}
def sha(b):return hashlib.sha256(b).hexdigest()
class Refusal(Exception):
 def __init__(self,family,decision=None,body_read=False):self.family=family;self.decision=decision;self.body_read=body_read

def fail(family,decision=None):raise Refusal(family,decision,True)
def pairs(items):
 d={}
 for k,v in items:
  if k in d:fail('RF-2')
  d[k]=v
 return d

def utf8_bounds(value,schema):
 if isinstance(value,str):
  try:n=len(value.encode('utf-8'))
  except UnicodeEncodeError:fail('RF-2')
  if n>schema.get('x-maxUtf8Bytes',1024):fail('RF-2')
 if isinstance(value,dict):
  for k,v in value.items():utf8_bounds(v,schema.get('properties',{}).get(k,{}))
 if isinstance(value,list):
  for v in value:utf8_bounds(v,schema.get('items',{}))

class LargeInteger(str):
 """Lexical integer beyond any legal control integer; never converted to int."""
NUMBER=re.compile(r'-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?')

def iterative_json(text):
 """RFC8259 syntax parser with explicit container stack and exact integer tokens.

 The bounded frame limits input bytes; nesting consumes heap stack entries,
 never Python call stack. Unsupported-major body syntax is checked without
 imposing the known-major body's field, numeric or depth rules.
 """
 i=0;stack=[];root=None;done=False
 def put(value):
  nonlocal root,done
  if not stack:
   if done:fail('RF-2')
   root=value;done=True;return
  parent=stack[-1]
  if parent['kind']=='object':parent['value'][parent['key']]=value
  else:parent['value'].append(value)
  parent['phase']='separator'
 while True:
  while i<len(text) and text[i] in ' \t\r\n':i+=1
  if i==len(text):
   if stack or not done:fail('RF-2')
   return root
  if not stack and done:fail('RF-2')
  if stack:
   top=stack[-1];phase=top['phase'];kind=top['kind'];ch=text[i]
   if phase=='separator':
    if ch==(',' ):top['phase']='key' if kind=='object' else 'value';i+=1;continue
    if ch==('}' if kind=='object' else ']'):stack.pop();i+=1;continue
    fail('RF-2')
   if phase in ['first-key','key']:
    if phase=='first-key' and ch=='}':stack.pop();i+=1;continue
    if ch!='"':fail('RF-2')
    try:key,i=json.decoder.scanstring(text,i+1,True)
    except (ValueError,UnicodeError):fail('RF-2')
    if key in top['value']:fail('RF-2')
    top['key']=key;top['phase']='colon';continue
   if phase=='colon':
    if ch!=':':fail('RF-2')
    top['phase']='value';i+=1;continue
   if phase=='first-value' and ch==']':stack.pop();i+=1;continue
  ch=text[i]
  if ch in '{[':
   value={} if ch=='{' else [];put(value);stack.append({'kind':'object' if ch=='{' else 'array','value':value,'phase':'first-key' if ch=='{' else 'first-value'});i+=1;continue
  if ch=='"':
   try:value,i=json.decoder.scanstring(text,i+1,True)
   except (ValueError,UnicodeError):fail('RF-2')
   put(value);continue
  literal=next(((token,value) for token,value in [('true',True),('false',False),('null',None)] if text.startswith(token,i)),None)
  if literal:put(literal[1]);i+=len(literal[0]);continue
  match=NUMBER.match(text,i)
  if not match:fail('RF-2')
  token=match.group();i=match.end()
  if any(c in token for c in '.eE'):value=float(token)
  elif len(token.lstrip('-'))>16:value=LargeInteger(token)
  else:value=int(token)
  put(value)

def numbers(value):
 pending=[value]
 while pending:
  current=pending.pop()
  if isinstance(current,LargeInteger) or type(current) is float:fail('RF-2')
  if type(current) is int and not 0<=current<=9007199254740991:fail('RF-2')
  if isinstance(current,dict):pending.extend(current.values())
  elif isinstance(current,list):pending.extend(current)

def parse(raw,context):
 if len(raw)<4:raise Refusal('RF-2',body_read=False)
 n=int.from_bytes(raw[:4],'big')
 if n==0 or n>context['frameBound']:raise Refusal('RF-2',body_read=False)
 if len(raw)!=4+n:raise Refusal('RF-2',body_read=True)
 try:v=iterative_json(raw[4:].decode('utf-8'))
 except (UnicodeError,json.JSONDecodeError):fail('RF-2')
 if not isinstance(v,dict) or set(v)!={'type','seq','controlMajor','body'}:fail('RF-2')
 if isinstance(v['seq'],LargeInteger):fail('RF-2' if v['seq'].startswith('-') else 'RF-7')
 if type(v['type']) is not str or type(v['controlMajor']) is not int or not 1<=v['controlMajor']<=9007199254740991 or type(v['seq']) is not int or v['seq']<0:fail('RF-2')
 if v['seq']==0 or v['seq']>9007199254740991:fail('RF-7')
 if not isinstance(v['body'],dict):fail('RF-2')
 if v['type']=='hello' and v['controlMajor']!=1:
  if context['direction']!='host-to-component':fail('RF-7')
  if context['helloSeen']:fail('RF-8')
  if context['state']!='AWAIT-HELLO' or v['seq']!=context['nextSeq']:fail('RF-7')
  # Frozen envelope selects the refusal without validating a future body schema.
  fail('RF-1')
 t=v['type'];b=v['body']
 if t not in VALIDATORS:fail('RF-2')
 numbers(v)
 validation_value={**v,'body':dict(b)}
 # Wrong string-valued identity echoes have the accepted specific RF3 class,
 # including digest case/truncation; all other schema faults remain RF2.
 if t in ['hello','helloAck']:
  identity_key='expectedStableId' if t=='hello' else 'stableId'
  if isinstance(b.get(identity_key),str):validation_value['body'][identity_key]=context['stableId']
  if isinstance(b.get('admittedManifestDigest'),str):validation_value['body']['admittedManifestDigest']=context['manifestDigest']
 try:valid=VALIDATORS[t].is_valid(validation_value)
 except RecursionError:
  # Known body shapes have fixed shallow structure; deeply nested supplied
  # values cannot match them. A validator's diagnostic repr may recurse.
  fail('RF-2')
 if not valid:fail('RF-2')
 utf8_bounds(v,SCHEMAS[t])
 direction=context['direction'];state=context['state']
 if t not in (H2C if direction=='host-to-component' else C2H):fail('RF-7')
 if t=='hello' and context['helloSeen']:fail('RF-8')
 if t=='helloAck' and (v['controlMajor']!=1 or b['controlMajor']!=1):fail('RF-8')
 if t in ['select','selectAck'] and state=='STEADY':fail('RF-8')
 if v['seq']!=context['nextSeq'] or t not in LAWFUL[state]:fail('RF-7')
 if v['controlMajor']!=(context.get('offeredControlMajor',1) if t=='refusal' else 1):fail('RF-7')
 if t=='hello' and b['controlMajor']!=v['controlMajor']:fail('RF-8')
 if t in ['hello','helloAck']:
  sid=b.get('expectedStableId',b.get('stableId'))
  if sid!=context['stableId'] or b['admittedManifestDigest']!=context['manifestDigest']:fail('RF-3')
  if t=='hello' and b['platform']!=context['platform']:fail('RF-3')
  tuples=b.get('subprotocolOffers',b.get('subprotocolConfirms'))
  if any(q not in context['manifestTuples'] for q in tuples):fail('RF-4')
  if t=='helloAck' and any(q not in context['offeredTuples'] for q in tuples):fail('RF-4')
  if t=='helloAck' and b['maxControlFrameBytes']>context['frameOffer']:fail('RF-2')
 if t in ['select','selectAck']:
  if b not in context['confirmedTuples']:fail('RF-4')
  if t=='selectAck' and b!=context['selectedTuple']:fail('RF-4')
 if t in ['pong','healthReport']:
  if b['nonce']!=context['pendingNonce'].get(t):fail('RF-7')
 if t=='effectRequest':
  auth=context['authorizationEvidence']
  if not auth['authorized']:fail('RF-6',auth['decisionClass'])
  if any(b[k]!=auth[k] for k in ['effectClass','authorizationRef','operationRef']):fail('RF-6',auth['bindingMismatchDecisionClass'])
 if t=='effectResult':
  pending=context['effectOutcomeEvidence']
  if b['outcomeSeq']<=b['decisionSeq'] or any(b[k]!=pending[k] for k in ['requestSeq','decisionSeq','outcomeSeq','commitClass','effectOutcome']):fail('RF-7')
  if pending['effectClass']=='HE-2' and b['commitClass']!='REVERSIBLE':fail('RF-7')
 out={'verdict':'ACCEPT','type':t,'nextState':NEXT.get(t,state),'bodyBuffered':True}
 if t=='refusal':out['terminalFamily']=b['family']
 return out

def run_case(case):
 if 'frameRecipe' in case:
  r=case['frameRecipe'];base=bytes.fromhex(r['baseHex']);raw=r['length'].to_bytes(4,'big')+base+b' '*(r['length']-len(base))
 else:raw=bytes.fromhex(case['frameHex'])
 try:return parse(raw,case['context'])
 except Refusal as e:
  return {'verdict':e.family,'nextState':'FAULTED','bodyBuffered':e.body_read,**({'decisionClass':e.decision} if e.decision else {})}

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--report',default=str(HERE/'control-completion.report.v3.json'));args=ap.parse_args()
 cases_path=HERE/'control-completion.cases.v3.json';corpus=json.loads(cases_path.read_text());results=[]
 Draft202012Validator.check_schema(SCHEMA)
 for p,digest in corpus['sourcePins'].items():results.append({'id':'source/'+p,'passed':sha((ROOT/p).read_bytes())==digest})
 for c in corpus['cases']:
  try:actual=run_case(c)
  except Exception as e:actual={'checkerError':repr(e)}
  results.append({'id':c['id'],'passed':actual==c['expected'],**({} if actual==c['expected'] else {'expected':c['expected'],'actual':actual})})
 matrix=[c for c in corpus['cases'] if c['id'].startswith('MATRIX/')]
 coordinates={(c['context']['state'],c['context']['direction'],c['messageType']) for c in matrix}
 results.append({'id':'coverage/16x8x2','passed':len(matrix)==len(coordinates)==256 and {x[2] for x in coordinates}==set(SCHEMAS)})
 proof=json.loads((HERE/'control-completion.rf5-proof.v2.json').read_text())
 results.append({'id':'coverage/RF5-unreachable-preview','passed':set(proof['messageFunctions'])==set(SCHEMAS) and proof['effectClasses']==['HE-1','HE-2'] and all(c['expected']['verdict']!='RF-5' for c in corpus['cases'])})
 report={'status':'DESIGN-EVIDENCE-NOT-PRODUCT-QUALIFICATION','total':len(results),'passed':sum(x['passed'] for x in results),'results':results,'subjectPins':{p.name:sha(p.read_bytes()) for p in [Path(__file__),HERE/'control-completion.schema.v3.json',cases_path,HERE/'control-completion.rf5-proof.v2.json']},'limits':corpus['limits']}
 Path(args.report).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'passed':report['passed'],'total':report['total']}))
 if report['passed']!=report['total']:
  print(json.dumps([x for x in results if not x['passed']],indent=2));raise SystemExit(1)
if __name__=='__main__':main()
