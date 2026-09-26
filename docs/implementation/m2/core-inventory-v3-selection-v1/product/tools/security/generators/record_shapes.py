from pathlib import Path
import json,hashlib,sys,re
S=Path(sys.argv[1]);src=S/'inputs/trust-record-schema.json';raw=src.read_bytes();assert hashlib.sha256(raw).hexdigest()=='359345411d91585f76bbbad276b6bc2d774ba3e167aeb0bb2b70bfabb44d902f';schema=json.loads(raw);nodes=[];index={};locs={}
def key(v):return json.dumps(v,sort_keys=True,separators=(',',':'))
def collect(v,path):
 if key(v) in index:return index[key(v)]
 n=len(nodes);index[key(v)]=n;nodes.append(v);locs[n]=path
 if isinstance(v,bool):return n
 for k,x in v.items():
  if k in ['properties','$defs']:
   for name,y in x.items():collect(y,path+'/'+k+'/'+name)
  elif k in ['oneOf','allOf','anyOf']:
   for i,y in enumerate(x):collect(y,path+'/'+k+'/'+str(i))
  elif k in ['items','contains','if','then','else','not','propertyNames','additionalProperties'] and isinstance(x,(bool,dict)):collect(x,path+'/'+k)
 return n
collect(schema,'')
def call(v,arg='v'):return 'node_'+str(index[key(v)])+'('+arg+')'
def text(s):return json.dumps(s,ensure_ascii=False)
def const(v,arg='v'):
 if v is None:return 'matches!('+arg+', V::Null)'
 if isinstance(v,bool):return 'matches!('+arg+', V::Bool('+str(v).lower()+'))'
 if isinstance(v,str):return 'matches!('+arg+', V::String(s) if s == '+text(v)+')'
 if isinstance(v,int):return 'matches!('+arg+', V::Integer(n) if n.get() == '+str(v)+'_i128)'
 if isinstance(v,list):return 'matches!('+arg+', V::Array(a) if '+ ' && '.join(['a.len() == '+str(len(v))]+[const(x,'&a['+str(i)+']')for i,x in enumerate(v)])+')'
 if isinstance(v,dict):return 'matches!('+arg+', V::Object(o) if '+' && '.join(['o.len() == '+str(len(v))]+['o.get('+text(k)+').is_some_and(|v| '+const(x)+')'for k,x in v.items()])+')'
 raise AssertionError(v)
end=r'(?![\s\S])'
patterns={
 r'(^|/)\.\.?(/|$)':'dot_segment(s)',
 r'^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(-[0-9A-Za-z.-]+)?(\+[0-9A-Za-z.-]+)?'+end:'loose_version(s)',
 r'^(?!/)(?!.*(^|/)\.\.?(/|$))[^\u0000\\]+'+end:'logical_path_shape(s)',
 r'^(DISCLOSURE-ONLY|ENFORCED-BY-CONSTRUCTION|ENFORCED-AT-HOST-BROKER|ENFORCED-PLATFORM:[a-z0-9.-]+)'+end:'enforcement(s)',
 r'^/':"s.starts_with('/')",
 r'^P-(MACOS|LINUX)-(ARM64|X86_64)-[A-Z0-9]+-(APFS|EXT4)$':'platform(s)',
 r'^TRANSITION\.[A-Z_]+(:[^ ]+)?'+end:'transition(s)',
 r'^[0-7]{3,4}'+end:'mode(s)',
 r'^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z'+end:'timestamp(s)',
 r'^[^/\\\u0000]{1,255}(/[^/\\\u0000]{1,255})*'+end:'core_path_shape(s)',
 r'^[^/][^\x00]*$':'signed_path_shape(s)',
 r'^[a-z0-9][a-z0-9.-]*'+end:'token(s)'}
for n in [32,64]:patterns[r'^[0-9a-f]{'+str(n)+'}'+end]='hex(s, '+str(n)+')'
for n in [64,128]:patterns[r'^[0-9a-f]{'+str(n)+'}$']='hex(dollar(s), '+str(n)+')'
for tag,n in [('closure2:',64),('exec1_',32),('prj1-',64),('receipt2:',64),('repairplan2:',64),('req1_',32),('run2:',64),('run3:',64),('snapshot2:',64)]:patterns['^'+tag+r'[0-9a-f]{'+str(n)+'}'+end]='tag_hex(s, '+text(tag)+', '+str(n)+')'
types={'string':'String(_)','integer':'Integer(_)','boolean':'Bool(_)','null':'Null','array':'Array(_)','object':'Object(_)'}
allowed={'$schema','$id','$comment','$defs','$ref','title','description','type','properties','required','additionalProperties','oneOf','allOf','anyOf','if','then','else','not','contains','const','enum','pattern','minimum','maximum','minLength','maxLength','minItems','maxItems','uniqueItems','items','propertyNames','minProperties','maxProperties','x-opensip-order','x-integration','x-installation-outcome-successor'}
# Validate the whole reference graph, not only currently exposed root entries.
def refs(v):
 if isinstance(v,dict):
  if '$ref'in v:yield v['$ref']
  for x in v.values():yield from refs(x)
 elif isinstance(v,list):
  for x in v:yield from refs(x)
deps={n:{r.removeprefix('#/$defs/')for r in refs(v)}for n,v in schema['$defs'].items()}
assert all(r.startswith('#/$defs/')and r.removeprefix('#/$defs/')in deps for r in refs(schema))
def visit(n,stack):
 assert n not in stack,('recursive schema',stack,n)
 for child in deps[n]:visit(child,stack+[n])
for n in deps:visit(n,[])
for i,n in enumerate(nodes):
 if isinstance(n,dict):assert not set(n)-allowed,(locs[i],set(n)-allowed)
out=['//! Generated exact private trust schema. Structural evidence only.','// SHA256 '+hashlib.sha256(raw).hexdigest(),'use super::*;','#[derive(Debug, Clone, Copy, PartialEq, Eq)]','pub(in super::super) enum Definition { '+', '.join(schema['$defs'])+' }','impl Definition {','#[cfg(test)] pub(super) fn named(s: &str) -> Option<Self> { match s {']
for n in schema['$defs']:out.append(text(n)+' => Some(Self::'+n+'),')
out+=['_ => None, } }','}','pub(super) fn shape(definition: Definition, v: &V) -> bool { match definition {']
for n,s in schema['$defs'].items():out.append('Definition::'+n+' => '+call(s)+',')
out+=['} }']
for i,n in enumerate(nodes):
 if isinstance(n,bool):out.append('fn node_'+str(i)+'(_v: &V) -> bool { '+str(n).lower()+' }');continue
 terms=[]
 if '$ref'in n:terms.append(call(schema['$defs'][n['$ref'].removeprefix('#/$defs/')]))
 if 'type'in n:
  ts=n['type']if isinstance(n['type'],list)else[n['type']];terms.append('matches!(v, '+' | '.join('V::'+types[t]for t in ts)+')')
 if 'const'in n:terms.append(const(n['const']))
 if 'enum'in n:terms.append(' || '.join(const(x)for x in n['enum']))
 if 'oneOf'in n:terms.append('('+' + '.join('usize::from('+call(x)+')'for x in n['oneOf'])+') == 1')
 for k,op in [('allOf',' && '),('anyOf',' || ')]:
  if k in n:terms.append(op.join(call(x)for x in n[k]))
 if 'not'in n:terms.append('!'+call(n['not']))
 if 'if'in n:terms.append('if '+call(n['if'])+' { '+(call(n['then'])if'then'in n else'true')+' } else { '+(call(n['else'])if'else'in n else'true')+' }')
 if any(k in n for k in ['minLength','maxLength','pattern']):
  checks=[]
  for k,op in [('minLength','>='),('maxLength','<=')]:
   if k in n:checks.append('s.chars().count() '+op+' '+str(n[k]))
  if 'pattern'in n:checks.append(patterns[n['pattern']])
  terms.append('match v { V::String(s) => '+' && '.join(checks)+', _=>true }')
 if any(k in n for k in ['minimum','maximum']):
  checks=[]
  for k,op in [('minimum','>='),('maximum','<=')]:
   if k in n:checks.append('n.get() '+op+' '+str(n[k])+'_i128')
  terms.append('match v { V::Integer(n) => '+' && '.join(checks)+', _=>true }')
 if any(k in n for k in ['minItems','maxItems','uniqueItems','items','contains','x-opensip-order']):
  checks=[]
  for k,op in [('minItems','>='),('maxItems','<=')]:
   if k in n:checks.append('a.len() '+op+' '+str(n[k]))
  if n.get('uniqueItems'):checks.append('unique(a)')
  if 'items'in n:checks.append('a.iter().all(|v| '+call(n['items'])+')')
  if 'contains'in n:checks.append('a.iter().any(|v| '+call(n['contains'])+')')
  if 'x-opensip-order'in n:
   order=n['x-opensip-order'];assert order in ['sequence','utf8','path']or order=={'by':['slot','path']}
   if order!='sequence':checks.append('ordered(a, &['+', '.join(text(k)for k in ([]if order=='utf8'else['path']if order=='path'else order['by']))+'])')
  terms.append('match v { V::Array(a) => '+(' && '.join(checks)or'true')+', _=>true }')
 if any(k in n for k in ['properties','required','additionalProperties','propertyNames','minProperties','maxProperties']):
  checks=[];props=n.get('properties',{});required=n.get('required',[])
  for k,s in props.items():checks.append('o.get('+text(k)+').'+('is_some_and'if k in required else'is_none_or')+'(|v| '+call(s)+')')
  checks+=['o.contains_key('+text(k)+')'for k in required if k not in props]
  if n.get('additionalProperties')is False:checks.append('o.keys().all(|k| ['+', '.join(text(k)for k in props)+'].contains(&k.as_str()))')
  if isinstance(n.get('additionalProperties'),dict):
   checks.append('o.iter().all(|(k,v)| ['+', '.join(text(k)for k in props)+'].contains(&k.as_str()) || '+call(n['additionalProperties'])+')')
  if 'propertyNames'in n:checks.append('o.keys().all(|k| '+call(n['propertyNames'],'&V::String(k.clone())')+')')
  for k,op in [('minProperties','>='),('maxProperties','<=')]:
   if k in n:checks.append('o.len() '+op+' '+str(n[k]))
  terms.append('match v { V::Object(o) => '+(' && '.join(checks)or'true')+', _=>true }')
 out.append('fn node_'+str(i)+'('+('v'if terms else'_v')+': &V) -> bool {\n    '+(terms[0]if len(terms)==1 else' &&\n    '.join('('+x+')'for x in terms)if terms else'true')+'\n}')
# Test every distinct fragment and every exact regex independently against original oracle.
out+=['pub(super) fn fragment(i: usize, v: &V) -> bool { match i {']+[str(i)+' => node_'+str(i)+'(v),'for i in range(len(nodes))]+['_ => false, } }']
out+=['#[cfg(test)] pub(super) fn pattern(i: usize, s: &str) -> bool { match i {']+[str(i)+' => '+code+','for i,(pattern,code)in enumerate(patterns.items())]+['_ => false, } }']
generated='\n'.join(out)+'\n';generated=re.sub(r'\|v\| (node_\d+)\(v\)',r'\1',generated);generated=generated.replace('a.len() >= 0 && ','').replace('a.len() >= 0','true').replace('a.len() >= 1','!a.is_empty()').replace('o.len() >= 1','!o.is_empty()')
(S/'product/crates/security/src/trust_record_shape_nodes.rs').write_text(generated)
(S/'schema-source.json').write_bytes(raw);(S/'schema-generation-report.json').write_text(json.dumps({'sha256':hashlib.sha256(raw).hexdigest(),'definitions':len(schema['$defs']),'nodes':len(nodes),'patterns':list(patterns),'nodeLocations':locs,'allKeywordsChecked':True,'referenceGraphAcyclic':True,'annotationOnly':['title','description','x-integration','x-installation-outcome-successor']},indent=2)+'\n');(S/'schema-fragments.json').write_text(json.dumps(nodes,indent=2)+'\n');print(len(nodes),'nodes',len(patterns),'patterns')
