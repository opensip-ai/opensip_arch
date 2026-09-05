"""Executable reference design only. Host broker remains the authority."""
import base64, copy, importlib.util, json, re, secrets
from pathlib import Path
from types import MappingProxyType
from jsonschema import Draft202012Validator
HERE=Path(__file__).resolve().parent
KEY='OPENSIP_BROKER_CONTEXT'
FIXED={'LC_ALL':'C','LANG':'C','TZ':'UTC','UV_THREADPOOL_SIZE':'4'}
VALIDATOR=Draft202012Validator(json.loads((HERE/'broker-bootstrap.schema.v1.json').read_text()))
def load(name,path):
 s=importlib.util.spec_from_file_location(name,HERE/path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
SEC=load('broker_security_evidence','security-behavior-model.v2.py')
class StartupFailure(Exception):pass
class LocalHandleFailure(Exception):pass
def fail():raise StartupFailure('BROKER-BOOTSTRAP-INVALID')
def pairs(items):
 d={}
 for k,v in items:
  if k in d:fail()
  d[k]=v
 return d
def integer(s):
 if s!='1':fail()
 return 1
def reject_number(s):fail()
def encode(value):return base64.urlsafe_b64encode(json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).rstrip(b'=').decode('ascii')
def parse(value):
 if not isinstance(value,str) or not 0<len(value)<=16384 or re.fullmatch('[A-Za-z0-9_-]+',value) is None:fail()
 try:raw=base64.b64decode(value+'='*((-len(value))%4),altchars=b'-_',validate=True)
 except (ValueError,TypeError):fail()
 if len(raw)>12288 or base64.urlsafe_b64encode(raw).rstrip(b'=').decode()!=value:fail()
 try:text=raw.decode('utf-8')
 except UnicodeError:fail()
 # Admission scanner bounds containers before the recursive JSON implementation.
 depth=0;quoted=False;escape=False
 for c in text:
  if quoted:
   if escape:escape=False
   elif ord(c)==92:escape=True
   elif c=='"':quoted=False
  elif c=='"':quoted=True
  elif c in '[{':
   depth+=1
   if depth>8:fail()
  elif c in ']}':depth-=1
 try:v=json.loads(text,object_pairs_hook=pairs,parse_int=integer,parse_float=reject_number,parse_constant=reject_number)
 except (ValueError,TypeError,RecursionError):fail()
 pending=[v]
 while pending:
  x=pending.pop()
  if isinstance(x,str):
   try:x.encode('utf-8')
   except UnicodeError:fail()
  elif isinstance(x,dict):pending.extend(x.keys());pending.extend(x.values())
  elif isinstance(x,list):pending.extend(x)
 if not VALIDATOR.is_valid(v) or type(v['bootstrapVersion']) is not int:fail()
 handles=v['handles']
 for key in ('authorizationRef',):
  if len({h[key] for h in handles})!=len(handles):fail()
 return v
class Handle:
 __slots__=()
class SDK:
 def __init__(self,host_dispatch=None):self._consumed=False;self._registry={};self._dispatch=host_dispatch
 def consume(self,env):
  for key in list(env):
   if key not in FIXED and key!=KEY:del env[key]
  value=env.pop(KEY,None)
  if self._consumed:raise StartupFailure('BROKER-BOOTSTRAP-ALREADY-CONSUMED')
  self._consumed=True
  if value is None:raise StartupFailure('BROKER-BOOTSTRAP-MISSING')
  value=parse(value)
  for body in value['handles']:self._registry[Handle()]=MappingProxyType(dict(body))
  return tuple(self._registry)
 def requestEffect(self,handle):
  if type(handle) is not Handle or handle not in self._registry:raise LocalHandleFailure('UNKNOWN-LOCAL-HANDLE')
  if self._dispatch is None:raise LocalHandleFailure('SDK-DISPATCH-NOT-BOUND')
  return self._dispatch(dict(self._registry[handle]))
 def child_environment(self,env):return dict(FIXED)
def launch_environment(ambient,bootstrap):
 # Ambient is deliberately ignored, including alleged ENV grants in this profile.
 parse(bootstrap)
 return {**FIXED,KEY:bootstrap}
def launch_argv(node,config,entry):
 if not all(Path(p).is_absolute() for p in (node,config,entry)):raise ValueError('ABSOLUTE-ASSET-PATHS-REQUIRED')
 return [node,'--no-addons','--no-global-search-paths','--openssl-config='+config,entry]
class HostBroker:
 BINDINGS=('spawn','component','installGeneration','manifest','platform','policy','projectKey','grantGeneration','pid','bootUUID')
 def __init__(self,current,entropy=None):
  self.current=copy.deepcopy(current);self._entries={};self.schedule=[];self.started=False;self._entropy=entropy or (lambda:secrets.token_hex(16))
 def register(self,effect,operation,internal_locator,target,parameters):
  if self.started:raise ValueError('REGISTRATION-CLOSED-AFTER-BOOTSTRAP')
  if effect not in ('HE-1','HE-2') or re.fullmatch('op-[0-9a-f]{32}',operation) is None:raise ValueError('INVALID-OPERATION')
  if len(self._entries)>=4 or any(e['locator']==internal_locator for e in self._entries.values()):raise ValueError('OPERATION-REGISTRATION-BOUND')
  while True:
   suffix=self._entropy()
   if re.fullmatch('[0-9a-f]{32}',suffix) is None:raise ValueError('ENTROPY-SPELLING')
   ah='ah:'+suffix
   if ah not in self._entries:break
  body={'effectClass':effect,'operationRef':operation,'authorizationRef':ah}
  self.schedule.extend([{'op':'WRITE','type':'GRANT','request':ah},{'op':'SYNC'}])
  self._entries[ah]={'body':body,'locator':internal_locator,'target':target,'parameters':copy.deepcopy(parameters),'bindings':copy.deepcopy(self.current)}
  return copy.deepcopy(body)
 def bootstrap(self):
  self.started=True
  return encode({'bootstrapVersion':1,'handles':[copy.deepcopy(e['body']) for e in self._entries.values()]})
 def close(self):self._entries.clear()
 def revoke(self):self.schedule.extend([{'op':'WRITE','type':'REV'},{'op':'SYNC'}])
 def dispatch(self,body,process_context):
  entry=self._entries.get(body.get('authorizationRef')) if isinstance(body,dict) else None
  history=SEC.journal({'schedule':self.schedule})
  durable=entry is not None and any(r['type']=='GRANT' and r.get('request')==body.get('authorizationRef') for r in history['journal'])
  match=entry is not None and body==entry['body'] and entry['bindings']==self.current and all(process_context.get(k)==self.current.get(k) for k in self.BINDINGS) and durable
  token='PT-HOST-EFFECT-BROKERED'
  p=SEC.permission({'token':token,'declared':self.current['declared'],'denied':self.current['denied'],'revoked':history['revoked'],'scopeMatches':match})
  if p['decision']!='GRANTED':return {'wire':p['wire'],'decision':p['decision'],'initiated':[]}
  # Request admission only: downstream durable RA/RCI/ICI and witness protocol is
  # still required before an external effect. This model never performs one.
  return {'wire':None,'decision':'GRANTED','initiated':[],'registeredTarget':entry['target'],'registeredParameters':copy.deepcopy(entry['parameters'])}
