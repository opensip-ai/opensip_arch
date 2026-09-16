"""Host foundation admission successor: configuration, policy and parser only.
Real fixture reads; no project discovery or OS acquisition implementation.

Not a production host, OS identity implementation, security authorization engine,
or measured filesystem/race qualification. Imports independently reviewed solver
and canonical policy functions for their narrow existing design contracts.
"""
import copy,hashlib,importlib.util,json,os,re,stat,tempfile
from pathlib import Path,PurePosixPath
from jsonschema import Draft202012Validator
# Explicit successor dependency; old model bytes stay frozen.
_cspec=importlib.util.spec_from_file_location('product_canonical',Path(__file__).with_name('canonical.py'))
CANONICAL=importlib.util.module_from_spec(_cspec);_cspec.loader.exec_module(CANONICAL)
Draft202012Validator=CANONICAL.ExactValidator

B=Path(__file__).resolve().parents[2]/'completion'
SCHEMA=json.loads((B/'preview-configuration.schema.v1.json').read_text())
POLICY_SCHEMA=json.loads((B/'security-schemas.v2/permission-policy.schema.json').read_text())
def module(name,path):
 s=importlib.util.spec_from_file_location(name,B/path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
SOLVER=module('foundation_solver','compatibility-selection-model.v3.py')
SECURITY=module('foundation_security','security_unit_lib_v2.py')
MAX_BYTES=4*1024*1024
MAX_DEPTH=32
CAPS=SOLVER.CAPS

class Refuse(ValueError):pass

def strict(raw):
 if len(raw)>MAX_BYTES:raise Refuse('byte-bound')
 def pairs(items):
  result={}
  for k,v in items:
   if k in result:raise Refuse('duplicate-key')
   result[k]=v
  return result
 def constant(_):raise Refuse('non-finite')
 def floating(_):raise Refuse('float-forbidden')
 def integer(raw):
  if raw=='-0':raise Refuse('negative-zero')
  value=int(raw)
  if not -(2**63)<=value<=2**64-1:raise Refuse('integer-range')
  return value
 try:value=json.loads(raw.decode('utf-8','strict'),object_pairs_hook=pairs,parse_constant=constant,parse_float=floating,parse_int=integer)
 except (ValueError,UnicodeError,RecursionError) as e:raise Refuse('strict-json') from e
 if not isinstance(value,dict):raise Refuse('object-required')
 def visit(v,depth):
  if isinstance(v,(dict,list)):
   if depth>MAX_DEPTH:raise Refuse('depth-bound')
   if isinstance(v,dict):
    for k,x in v.items():k.encode('utf-8','strict');visit(x,depth+1)
   else:
    for x in v:visit(x,depth+1)
  elif isinstance(v,str):v.encode('utf-8','strict')
  elif isinstance(v,float) and (v!=v or abs(v)==float('inf')):raise Refuse('non-finite')
 try:visit(value,1)
 except UnicodeError as e:raise Refuse('surrogate') from e
 return value

def validate(value,layer):
 try:CANONICAL.typed(value)
 except CANONICAL.AdmissionError as e:raise Refuse('carrier-schema') from e
 schema=copy.deepcopy(SCHEMA);schema.pop('anyOf');schema['$ref']='#/$defs/'+layer
 if not Draft202012Validator(schema).is_valid(value):raise Refuse('carrier-schema')

def flag_budget(raw):
 if not isinstance(raw,str) or not re.fullmatch(r'[1-9][0-9]*',raw) or len(raw)>16:raise Refuse('invalid-budget-flag')
 limit=int(raw)
 if limit>9007199254740991:raise Refuse('invalid-budget-flag')
 return {'analysis':{'budget':{'unit':'work-units','limit':limit}}}

def fixture_raw(spec):
 if 'rawHex' in spec:return bytes.fromhex(spec['rawHex'])
 if 'raw' in spec:return spec['raw'].encode('utf-8')
 if 'padToBytes' in spec:
  b=json.dumps(spec['json'],separators=(',',':')).encode();return b+b' '*(spec['padToBytes']-len(b))
 if 'nestedDepth' in spec:return ('{"x":'*(spec['nestedDepth']-1)+'{}'+'}'*(spec['nestedDepth']-1)).encode()
 return json.dumps(spec['json'],ensure_ascii=True,separators=(',',':')).encode()

class FixtureFS:
 """Temporary filesystem adapter with deterministic paths and actual read traces."""
 def __init__(self,root,files):
  self.root=Path(root);self.trace=[]
  for p,spec in files.items():
   target=self.path(p);target.parent.mkdir(parents=True,exist_ok=True)
   if 'symlink' in spec:target.symlink_to(spec['symlink'])
   elif spec.get('directory'):target.mkdir(exist_ok=True)
   else:target.write_bytes(fixture_raw(spec));target.chmod(spec.get('mode',0o600))
 def path(self,p):
  q=PurePosixPath(p)
  if q.is_absolute() or '..' in q.parts:raise ValueError('unsafe fixture path')
  return self.root/p
 def read(self,p,private=False):
  self.trace.append('lstat:'+p)
  try:s=self.path(p).lstat()
  except FileNotFoundError:return None
  if private and (not stat.S_ISREG(s.st_mode) or s.st_uid!=os.geteuid() or s.st_mode&0o077):raise Refuse('unsafe-policy')
  self.trace.append('open:'+p)
  try:
   fd=os.open(self.path(p),os.O_RDONLY|(os.O_NOFOLLOW if private else 0))
   with os.fdopen(fd,'rb') as f:
    self.trace.append('read:'+p);raw=f.read(MAX_BYTES+1)
   return strict(raw)
  except OSError as e:raise Refuse('carrier-io') from e

def configuration(x):
 with tempfile.TemporaryDirectory(prefix='opensip-foundation-') as td:
  fs=FixtureFS(td,x.get('files',{}));result={'status':'ACCEPT','semantic':{},'presentation':{},'provenance':{},'trace':fs.trace,'effects':[],'analysisAdmitted':False,'completionStage':'CONFIGURATION-ONLY','solverExecuted':False}
  layer='defaults'
  try:
   validate(x['defaults'],'defaults')
   layers=[('defaults',copy.deepcopy(x['defaults']))]
   # Read/admit each layer in precedence order; CI branch never asks about L4.
   for name,path in [('global','host/settings.json'),('project','project/opensip.json')]+([('local','project/.opensip/local.json')] if x.get('tty',False) and not x.get('ci',False) else []):
    layer=name;value=fs.read(path)
    if value is not None:validate(value,name)
    layers.append((name,value))
   layers.append(('environment',copy.deepcopy(x.get('hostEnvironment',{}))))
   layer='flags'
   flags=flag_budget(x['budgetFlag']) if 'budgetFlag' in x else copy.deepcopy(x.get('hostFlags',{}))
   layers.append(('flags',flags))
   for layer,value in layers:
    if value is None:continue
    validate(value,layer)
    fields=[]
    for k in ['profile','capabilities']:
     if k in value:fields.append((k,value[k],False))
    if 'budget' in value.get('analysis',{}):fields.append(('analysis.budget',value['analysis']['budget'],False))
    for k,v in value.get('components',{}).items():fields.append(('components.'+k,v,False))
    if 'color' in value.get('ui',{}):fields.append(('ui.color',value['ui']['color'],True))
    for key,v,presentation in fields:
     result['presentation' if presentation else 'semantic'][key]=copy.deepcopy(v)
     result['provenance'][key]={'decidingLayer':layer,'value':copy.deepcopy(v)}
   # Winning arrays remain untouched; resolver inputs have a distinct boundary.
   projection={}
   for k in ['request','pins','holds']:
    items=result['semantic']['components.'+k];ids=[v['stableId'] for v in items]
    if len(ids)!=len(set(ids)):
     layer=result['provenance']['components.'+k]['decidingLayer'];raise Refuse('duplicate-component-id')
    projection[k]=sorted(copy.deepcopy(items),key=lambda v:v['stableId'].encode('utf-8'))
   pins={v['stableId']:v['version'] for v in projection['pins']}
   if any(v['stableId'] in pins and v['version']!=pins[v['stableId']] for v in projection['holds']):
    layer='project';raise Refuse('pin-hold-conflict')
   projection['allowedScopes']=copy.deepcopy(result['semantic']['components.allowedScopes'])
   result['resolverProjection']=projection
   if 'solverFixtureId' in x:
    fixtures=json.loads((B/'compatibility-selection-cases.v3.json').read_text())['selections']
    data=copy.deepcopy(next(v['input'] for v in fixtures if v['id']==x['solverFixtureId']))
    for k in ['request','pins','holds']:data['resolutionInputs'][k]=projection[k]
    data['resolutionInputs']['scopeContext']['allowedScopes']=projection['allowedScopes']
    selected=SOLVER.solve(data);result['solverStatus']=selected['status'];result['solverExecuted']=True
    if selected['status']!='ACCEPT':
     layer='project';raise Refuse('resolver-refusal')
  except (Refuse,KeyError,TypeError) as e:
   # No semantic/provider request is admitted from a failed resolution.
   result['status']='HOST-INVARIANT-FAILURE' if layer in ['defaults','environment','flags'] and str(e)!='invalid-budget-flag' else 'CONFIG-INVALID'
   result['reason']=str(e);result['semantic']={};result['presentation']={};result['provenance']={};result.pop('resolverProjection',None)
  return result

def policy(x):
 with tempfile.TemporaryDirectory(prefix='opensip-policy-') as td:
  fs=FixtureFS(td,x['files']);result={'status':'ACCEPT','trace':fs.trace,'effects':[],'snapshots':[],'namespaceCreated':False,'grantsCreated':[]}
  try:
   if not x.get('hostFenceHeld',True):raise Refuse('lifecycle-fence-required')
   namespace=x.get('registeredNamespaceId')
   if namespace is not None and not re.fullmatch(r'[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}',namespace):raise Refuse('namespace-observation')
   paths=[('global','host/policies/permission-policy.json')]+([('project',f'host/projects/{namespace}/permission-policy.json')] if namespace is not None else [])
   for scope,path in paths:
    value=fs.read(path,private=True)
    if value is None:value={'policySchema':1,'policyScope':scope,'grants':[],'denies':[],'consents':[]}
    if not Draft202012Validator(POLICY_SCHEMA).is_valid(value) or value['policyScope']!=scope:raise Refuse('policy-schema')
    result['snapshots'].append({'scope':scope,'value':value,'canonicalHex':SECURITY.canonical_bytes(value).hex(),'digest':SECURITY.domain_digest(SECURITY.DOMAIN_TAGS['policy'],value)[0]})
   if 'replacement' in x:
    path=fs.path(paths[0][1]);before=path.stat();temp=path.with_name('replacement.tmp');temp.write_bytes(fixture_raw(x['replacement']));temp.chmod(0o600);os.replace(temp,path);os.utime(path,ns=(before.st_atime_ns,before.st_mtime_ns))
    value=fs.read(paths[0][1],private=True)
    if not Draft202012Validator(POLICY_SCHEMA).is_valid(value) or value['policyScope']!='global':raise Refuse('policy-schema')
    current=SECURITY.domain_digest(SECURITY.DOMAIN_TAGS['policy'],value)[0]
    result['nextOperation']={'sameMtime':path.stat().st_mtime_ns==before.st_mtime_ns,'digest':current,'changed':current!=result['snapshots'][0]['digest']}
  except (Refuse,SECURITY.Reject) as e:result['status']='REFUSE';result['reason']=str(e);result['snapshots']=[]
  return result

def evaluate(kind,x):
 if kind=='parser':
  try:v=strict(fixture_raw(x));return {'status':'ACCEPT','value':v}
  except Refuse as e:return {'status':'REFUSE','reason':str(e)}
 return {'configuration':configuration,'policy':policy}[kind](x)
