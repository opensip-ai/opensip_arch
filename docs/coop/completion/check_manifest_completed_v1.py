#!/usr/bin/env python3
"""Full manifest structural/path/reference design checker, not shipping admission."""
import argparse,copy,hashlib,importlib.util,json,posixpath,re,unicodedata
from pathlib import Path
from jsonschema import Draft202012Validator
P=Path(__file__).resolve().parent;ROOT=P.parents[2]
SCHEMA=json.loads((P/'manifest-schema.completed.v1.json').read_text());VALIDATOR=Draft202012Validator(SCHEMA)
spec=importlib.util.spec_from_file_location('manifest_semver_dependency',P/'check_compatibility_design_v2.py');SEM=importlib.util.module_from_spec(spec);spec.loader.exec_module(SEM)
class Refuse(Exception):
 def __init__(self,code,datum):self.code=code;self.datum=datum

def no(code,datum):raise Refuse(code,datum)
def pairs(items):
 out={}
 for k,v in items:
  if k in out:no('RJ-6','DUPLICATE_JSON_KEY:'+k)
  out[k]=v
 return out

def parse(raw):
 if len(raw)>4194304:no('RJ-6','MANIFEST_BYTE_LIMIT')
 try:text=raw.decode('utf-8')
 except UnicodeError:no('RJ-6','UTF8')
 depth=0;quoted=False;escape=False
 for c in text:
  if quoted:
   if escape:escape=False
   elif c=='\\':escape=True
   elif c=='"':quoted=False
  elif c=='"':quoted=True
  elif c in '[{':
   depth+=1
   if depth>64:no('RJ-6','JSON_DEPTH_LIMIT')
  elif c in ']}':depth-=1
 try:v=json.loads(text,object_pairs_hook=pairs,parse_float=lambda _:no('RJ-6','FLOAT'),parse_constant=lambda _:no('RJ-6','CONSTANT'))
 except (ValueError,RecursionError):no('RJ-6','JSON_SYNTAX_OR_INTEGER_LIMIT')
 pending=[v]
 while pending:
  x=pending.pop()
  if isinstance(x,str):
   try:x.encode('utf-8')
   except UnicodeError:no('RJ-6','LONE_SURROGATE')
  elif isinstance(x,dict):pending.extend(x);pending.extend(x.values())
  elif isinstance(x,list):
   if len(x)>100000:no('RJ-6','ARRAY_LIMIT')
   pending.extend(x)
  elif type(x) is int and not -(2**63)<=x<2**63:no('RJ-6','INTEGER_LIMIT')
 return v

def path_ok(path):
 try:size=len(path.encode('utf-8'))
 except UnicodeError:no('RJ-3',path)
 parts=path.split('/')
 if size>1024 or not path or path.startswith('/') or re.match(r'^[A-Za-z]:',path) or '\\' in path or '\x00' in path or unicodedata.normalize('NFC',path)!=path or any(x in ['', '.', '..'] for x in parts):no('RJ-3',path)
 for segment in parts:
  stem=segment.split('.')[0].upper()
  if segment.endswith(('.', ' ')) or stem in {'CON','PRN','AUX','NUL',*[f'COM{i}' for i in range(1,10)],*[f'LPT{i}' for i in range(1,10)]}:no('RJ-3',path)

def interval(value):
 if isinstance(value,dict):
  order=SEM.compare(value['min'],value['max'])
  if order>0 or order==0 and not(value['includeMin'] and value['includeMax']):no('RJ-6','EMPTY_VERSION_INTERVAL')

def command_checks(m,context):
 commands=m['commands'];roots=[i for i,c in enumerate(commands) if 'parent' not in c]
 if len(roots)!=1:no('RJ-2','MULTIPLE_ROOT_COMMANDS')
 root=roots[0]
 if commands[root]['name']!=m['name']:no('RJ-2','ROOT_COMMAND_NAME_MISMATCH')
 names={};scopes={}
 for i,c in enumerate(commands):
  names.setdefault(c['name'],[]).append(i)
  group=scopes.setdefault(c.get('parent'),set())
  for token in [c['name']]+c.get('aliases',[]):
   if token in group:no('RJ-2','PARENT_LINKAGE_COLLISION:'+token)
   group.add(token)
  options=c.get('options',[]);flags=[]
  for o in options:
   if o['flag'] in flags:no('RJ-6','DUPLICATE_OPTION')
   flags.append(o['flag'])
   if 'default' in o:
    value=o['default'];wanted={'boolean':bool,'integer':int,'string':str,'path':str}[o['valueKind']]
    values=value if o['repeatable'] and isinstance(value,list) else [value]
    if o['repeatable'] and not isinstance(value,list) or any(type(v) is not wanted for v in values):no('RJ-6','OPTION_DEFAULT_TYPE')
  args=c.get('args',[]);argnames=set();optional=False
  for j,a in enumerate(args):
   if a['name'] in argnames or a['variadic'] and j!=len(args)-1 or optional and a['required']:no('RJ-6','POSITIONAL_GRAMMAR')
   argnames.add(a['name']);optional=optional or not a['required']
 for i,c in enumerate(commands):
  seen=set();cur=i;depth=0
  while True:
   if cur in seen:no('RJ-2','PARENT_UNKNOWN_OR_CYCLIC')
   seen.add(cur);depth+=1
   if depth>32:no('RJ-6','COMMAND_DEPTH_LIMIT')
   parent=commands[cur].get('parent')
   if parent is None:break
   matches=names.get(parent,[])
   if len(matches)!=1:no('RJ-2','PARENT_UNKNOWN_OR_AMBIGUOUS')
   cur=matches[0]
 keys=[m['name']]+m.get('aliases',[])+commands[root].get('aliases',[])
 if len(keys)!=len(set(keys)):no('RJ-2','ALIAS_COLLISION')
 if set(keys)&set(context.get('reservedNames',[])):no('RJ-2','RESERVED_ROOT_COMMAND')
 for entry in context.get('liveNames',[]):
  if (entry['stableId'],entry['provenance'])!=(m['stableId'],m['provenance']) and set(keys)&set(entry['names']):no('RJ-2','LIVE_NAME_COLLISION')

def tree_checks(platform):
 entries=platform['tree']['entries'];by={};folded=set()
 for e in entries:
  p=e['path'];path_ok(p);fold=unicodedata.normalize('NFC',p.casefold())
  if p in by or fold in folded:no('RJ-3','DUPLICATE_PATH:'+p)
  by[p]=e;folded.add(fold)
  if e['type']=='symlink':path_ok(e['target'])
 for p,e in by.items():
  parent=posixpath.dirname(p)
  if parent and (parent not in by or by[parent]['type']!='dir'):no('RJ-3','UNDECLARED_OR_NONDIR_PARENT:'+p)
 def resolve(p):
  seen=set()
  while True:
   if p in seen:no('RJ-3','SYMLINK_CYCLE:'+p)
   seen.add(p)
   if p not in by:no('RJ-3','UNDECLARED_TARGET:'+p)
   e=by[p]
   if e['type']!='symlink':return e
   p=posixpath.join(posixpath.dirname(p),e['target'])
 for p,e in by.items():
  if e['type']=='symlink':resolve(p)
 path_ok(platform['entrypoint']);entry=resolve(platform['entrypoint'])
 if entry['type']!='file' or int(entry['mode'],8)&0o111==0:no('RJ-3','ENTRYPOINT_NOT_EXECUTABLE_FILE')

def config_checks(m,context):
 if 'configuration' not in m:return
 c=m['configuration'];node=c['schema']
 if c['namespace']!=m['name'] or node['type']!='object' or set(c['classifications'])!=set(node['properties']):no('RJ-6','SELF_CLASSIFIED_CONFIGURATION')
 if c['classifications']!=context.get('hostClassificationMap',{}):no('RJ-6','HOST_CLASSIFICATION_REVIEW_REQUIRED')
 pending=[node]
 while pending:
  n=pending.pop()
  if n['type']=='object':
   if not set(n['required'])<=set(n['properties']):no('RJ-6','UNDECLARED_CONFIG_REQUIRED_FIELD')
   pending.extend(n['properties'].values())
  elif n['type']=='array':pending.append(n['items'])
  for low,high in [('minimum','maximum'),('minItems','maxItems'),('minLength','maxLength')]:
   if low in n and high in n and n[low]>n[high]:no('RJ-6','EMPTY_CONFIG_RANGE')

def artifact_checks(m,context,bases,blobs):
 # The synthetic retained artifact bundle supplies the path->exact-byte custody
 # map. A claimed digest alone never selects which file bytes are checked.
 original=bases['artifact-closure'];missing=set(context.get('missingArtifacts',[]))
 refs={v['path']:v['sha256'] for v in original['declarations'].values()}
 notice_body=b'Design fixture notice; no shipping product claim.\n';refs['notices/fixture.txt']=hashlib.sha256(notice_body).hexdigest()
 def verify(ref,inventory):
  path=ref['path']
  if path in missing or path not in inventory:no('RJ-4','MISSING_ARTIFACT:'+path)
  expected=inventory[path]
  if expected not in blobs:no('RJ-4','MISSING_BYTES:'+path)
  data=bytes.fromhex(blobs[expected])
  if hashlib.sha256(data).hexdigest()!=ref['sha256']:no('RJ-4','DIGEST_MISMATCH:'+path)
  return data
 platforms={(v['os'],v['arch']):v for v in original['platforms']}
 for p in m['platforms']:
  source=platforms.get((p['os'],p['arch']))
  if source is None:no('RJ-4','NO_PLATFORM_ARTIFACT_BUNDLE')
  inventory={e['path']:e['sha256'] for e in source['tree']['entries'] if e['type']=='file'}
  for e in p['tree']['entries']:
   if e['type']=='file' and len(verify(e,inventory))!=e['length']:no('RJ-4','LENGTH_MISMATCH:'+e['path'])
 for kind,ref in m['declarations'].items():
  if 'absent' in ref:continue
  # References may point inside each platform tree, or to a sibling artifact.
  if ref['path'] in refs:data=verify(ref,refs)
  else:
   data=None
   for p in m['platforms']:
    source=platforms.get((p['os'],p['arch']),{'tree':{'entries':[]}})
    inventory={e['path']:e['sha256'] for e in source['tree']['entries'] if e['type']=='file'}
    data=verify(ref,inventory)
  if kind=='licenses':
   value=parse(data)
   if not isinstance(value,dict) or not isinstance(value.get('licenseInventory'),list) or not isinstance(value.get('noticeInventory'),list):no('RJ-6','LICENSE_NOTICE_INVENTORY_REQUIRED')
   for notice in value['noticeInventory']:
    if not isinstance(notice,dict) or set(notice)!={'path','sha256'}:no('RJ-6','NOTICE_REFERENCE_SHAPE')
    path_ok(notice['path']);verify(notice,refs)

def validate(raw,context=None,bases=None,blobs=None):
 context=context or {};m=parse(raw)
 if not VALIDATOR.is_valid(m):no('RJ-6','CLOSED_SCHEMA')
 command_checks(m,context)
 platforms=set()
 for p in m['platforms']:
  pair=(p['os'],p['arch'])
  if pair in platforms:no('RJ-6','DUPLICATE_PLATFORM')
  platforms.add(pair);tree_checks(p)
 caps=[c['capabilityId'] for c in m['capabilities']]
 if len(caps)!=len(set(caps)) or 'typescript.reachability' in caps and 'typescript.calls' not in caps:no('RJ-6','CAPABILITY_DUPLICATE_OR_PREREQUISITE')
 permissions=[x['permission'] for x in m['permissions']]
 if len(set(permissions))!=len(permissions):no('RJ-6','DUPLICATE_PERMISSION')
 deps=[d['stableId'] for d in m['dependencies']]
 if len(set(deps))!=len(deps) or m['stableId'] in deps:no('RJ-6','DUPLICATE_OR_SELF_DEPENDENCY')
 for d in m['dependencies']:interval(d['versionConstraint'])
 interval(m['compatibility']['hostCore'])
 if m['compatibility']['manifest']!=m['manifestSchemaVersion']:no('RJ-6','MANIFEST_VERSION_ECHO')
 approved=set(context.get('approvedExceptions',[]));prereqs={}
 for p in m.get('prerequisites',[]):
  path_ok(p['doctorContract'])
  if p['exceptionApprovalRef'] not in approved or p['exceptionApprovalRef'] in prereqs:no('RJ-6','UNAPPROVED_OR_DUPLICATE_EXCEPTION')
  prereqs[p['exceptionApprovalRef']]=p
 for ref in m['declarations'].values():
  if 'path' in ref:path_ok(ref['path'])
  elif ref['exceptionApprovalRef'] not in prereqs or ref['typedAbsenceBehavior']!=prereqs[ref['exceptionApprovalRef']]['typedAbsenceBehavior']:no('RJ-6','UNTYPED_OR_UNAPPROVED_ABSENCE')
 config_checks(m,context)
 if context.get('previewProfile'):
  allowed={('macos','arm64'),('macos','x86_64'),('linux','arm64'),('linux','x86_64')}
  if not platforms<=allowed or any(m['compatibility'][k]!=1 for k in ['manifest','control','providerProtocol','componentState']) or not SEM.satisfies('0.1.0',m['compatibility']['hostCore']):no('RJ-6','UNSUPPORTED_PREVIEW_PROFILE')
  if 'configuration' in m and m['configuration']['schema']['properties']:no('RJ-6','NO_SHIPPED_COMPONENT_SETTINGS')
 if context.get('verifyArtifacts'):artifact_checks(m,context,bases,blobs)
 return {'verdict':'ACCEPT','phase':'artifact-closure' if context.get('verifyArtifacts') else 'preview-profile' if context.get('previewProfile') else 'structural','admitted':False}

def materialize(case,bases):
 v=copy.deepcopy(bases[case['base']])
 for op in case['operations']:
  target=v
  for key in op['path'][:-1]:target=target[key]
  if op['op']=='set':target[op['path'][-1]]=copy.deepcopy(op['value'])
  elif op['op']=='delete':del target[op['path'][-1]]
  else:
   target=v
   for key in op['path']:target=target[key]
   target.append(copy.deepcopy(op['value']))
 raw=json.dumps(v,ensure_ascii=True,separators=(',',':')).encode()
 recipe=case.get('wireRecipe',{});kind=recipe.get('kind')
 if kind=='padding':raw+=b' '*(recipe['bytes']-len(raw))
 elif kind=='duplicate':raw=raw[:-1]+b',"'+recipe['key'].encode()+b'":"component"}'
 elif kind=='nested':raw=b'['*recipe['depth']+b'0'+b']'*recipe['depth']
 elif kind=='huge-int':raw=raw.replace(b'"manifestSchemaVersion":1',b'"manifestSchemaVersion":'+b'9'*recipe['digits'])
 return raw

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--report',default=str(P/'manifest-report.completed.v1.json'));args=ap.parse_args()
 corpus=json.loads((P/'manifest-cases.completed.v1.json').read_text());bases=json.loads((P/'manifest-bases.completed.v1.json').read_text());blobs=json.loads((P/'manifest-artifact-blobs.completed.v1.json').read_text());results=[]
 Draft202012Validator.check_schema(SCHEMA)
 for name,h in corpus['sourcePins'].items():results.append({'id':'source/'+name,'passed':hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==h})
 for case in corpus['cases']:
  raw=materialize(case,bases)
  try:actual=validate(raw,case['context'],bases,blobs)
  except Refuse as e:actual={'verdict':e.code,'datum':e.datum,'admitted':False}
  except Exception as e:actual={'verdict':'CHECKER_ERROR','datum':repr(e)}
  results.append({'id':case['id'],'passed':actual['verdict']==case['expected'] and ('expectedDatum' not in case or actual.get('datum')==case['expectedDatum']),'wireSha256':hashlib.sha256(raw).hexdigest(),'wireLength':len(raw),'actual':actual})
 names=['manifest-schema.completed.v1.json','manifest-cases.completed.v1.json','manifest-bases.completed.v1.json','manifest-artifact-blobs.completed.v1.json','check_manifest_completed_v1.py','check_compatibility_design_v2.py','version-constraint-schema.completed.v2.json']
 report={'status':'DESIGN-EVIDENCE-NOT-PRODUCT-QUALIFICATION','passed':sum(r['passed'] for r in results),'total':len(results),'results':results,'subjectPins':{n:hashlib.sha256((P/n).read_bytes()).hexdigest() for n in names},'unicodeReferenceVersion':unicodedata.unidata_version,'limits':['Unicode casefold/NFC uses the reported interpreter database; production frozen Unicode15.1 integration remains separately required.','Structural validation does not verify signatures, trust, custody uniqueness, active dependency resolution or shipping runtime/tool availability.','Synthetic artifact closure checks only retained design bytes; latest security signatures and final G15 packaging join remain separate.']}
 Path(args.report).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'passed':report['passed'],'total':report['total']}))
 if report['passed']!=report['total']:
  print(json.dumps([r for r in results if not r['passed']],indent=2));raise SystemExit(1)
if __name__=='__main__':main()
