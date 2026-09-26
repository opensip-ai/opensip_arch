from pathlib import Path
import json,hashlib,sys
from types import SimpleNamespace
S=Path(sys.argv[1]);base=S/'inputs';p=base/'reference-registry.json'
wire=json.loads(p.read_bytes());schema_raw=(base/'trust-record-schema.json').read_bytes()
assert wire['schemaVersion']==1 and hashlib.sha256(schema_raw).hexdigest()==wire['schemaSha256']=='359345411d91585f76bbbad276b6bc2d774ba3e167aeb0bb2b70bfabb44d902f'
def pointer(parts):
 return '/'+'/'.join(str(x).replace('~','~0').replace('/','~1')for x in parts)if parts else ''
registry={}
for ptr,row in wire['registry'].items():
 parts=[x.replace('~1','/').replace('~0','~')for x in ptr.split('/')[1:]]
 assert len(parts)>=2 and parts[0]=='$defs' and '/'+ '/'.join(x.replace('~','~0').replace('/','~1')for x in parts)==ptr
 key=(parts[1],tuple(parts[2:]));assert key not in registry;registry[key]=row
R=SimpleNamespace(D=json.loads(schema_raw)['$defs'],ROOTS=wire['roots'],TERMINALS=wire['terminals'],REGISTRY=registry,WIRE_REGISTRY=wire['registry'],pointer=pointer)
D=R.D
frags=json.loads((S/'schema-fragments.json').read_bytes());ids={json.dumps(n,sort_keys=True,separators=(',',':')):i for i,n in enumerate(frags)}
def idx(n):return ids[json.dumps(n,sort_keys=True,separators=(',',':'))]
def rs(s):return json.dumps(s,ensure_ascii=False)
roots=sorted(R.ROOTS);seen={};nodes=[];bindings={}
def add(n,owner,path):
 key=(owner,path)
 if key in seen:return seen[key]
 i=len(nodes);seen[key]=i;nodes.append(None);steps=[]
 if '$ref'in n:
  name=n['$ref'].removeprefix('#/$defs/')
  if name in R.TERMINALS:
   row=R.REGISTRY[(owner,path)];bindings[key]=row;nodes[i]=(n,owner,path,[('edge',row)]);return i
  steps.append(('ref',add(D[name],name,())))
 for union in ['oneOf','anyOf']:
  for j,child in enumerate(n.get(union,[])):
   if isinstance(child,dict):steps.append(('match',idx(child),add(child,owner,path+(union,str(j)))))
 for j,child in enumerate(n.get('allOf',[])):
  if isinstance(child,dict):steps.append(('all',add(child,owner,path+('allOf',str(j)))))
 if 'if'in n:
  branches=[add(n[b],owner,path+(b,))if b in n and isinstance(n[b],dict)else None for b in ['then','else']];steps.append(('if',idx(n['if']),*branches))
 for key,child in n.get('properties',{}).items():
  if isinstance(child,dict):steps.append(('property',key,add(child,owner,path+('properties',key))))
 if isinstance(n.get('items'),dict):steps.append(('items',add(n['items'],owner,path+('items',))))
 nodes[i]=(n,owner,path,steps);return i
entry={n:add(D[n],n,())for n in roots};assert bindings==R.REGISTRY,(len(bindings),len(R.REGISTRY));assert len(bindings)==136
# Static no-edge subtrees can be omitted; branch admission always uses the FULL
# generated shape validator, including predicates that themselves contain no refs.
useful={}
def effect(i):
 if i in useful:return useful[i]
 steps=nodes[i][3];value=False
 for step in steps:
  if step[0]=='edge':value=True
  elif step[0]in ['ref','all','items']:value|=effect(step[1])
  elif step[0]in ['match','property']:value|=effect(step[2])
  elif step[0]=='if':value|=any(effect(x)for x in step[2:]if x is not None)
 useful[i]=value;return value
for i in range(len(nodes)):effect(i)
mutability={}
def mutable(i):
 if i in mutability:return mutability[i]
 result=False
 for step in nodes[i][3]:
  tag=step[0]
  if tag=='property':result|=effect(step[2])
  elif tag=='items':result|=effect(step[1])
  elif tag in ['ref','all']:result|=mutable(step[1])
  elif tag=='match':result|=mutable(step[2])
  elif tag=='if':result|=any(mutable(x)for x in step[2:]if x is not None)
 mutability[i]=result;return result
for i in range(len(nodes)):mutable(i)
def call(i):return 'walk_'+str(i)+'(v, location, c)?;'if effect(i)else''
out=['//! Static visits generated from pinned current trust-record schema and registry.','use super::*;','#[derive(Clone, Copy, Debug, PartialEq, Eq, PartialOrd, Ord)]','pub(in super::super) enum RecordKind { '+', '.join(roots)+' }','impl RecordKind {','pub(super) fn definition(self)->Definition { match self {']+[f'Self::{n} => Definition::{n},'for n in roots]+['} }','pub(super) fn name(self)->&\'static str { match self {']+[f'Self::{n} => {rs(n)},'for n in roots]+['} }','#[cfg(test)] pub(super) fn named(name:&str)->Option<Self> {match name {']+[f'{rs(n)} => Some(Self::{n}),'for n in roots]+['_=>None,} }','}','pub(super) fn extract(kind:RecordKind,v:&V,location:&mut Vec<String>,c:&mut Collector)->Result<(),Error> { match kind {']
for n,i in entry.items():out.append('RecordKind::'+n+' => { '+call(i)+' },')
out+=['} Ok(()) }']
collections={'records':'Records','objects':'Objects','events':'Events','publications':'Publications'};rtypes={'NodeRef':'Node','BlobRef':'Blob','EventRef':'Event','PublicationRef':'Publication'}
for i,(n,owner,path,steps)in enumerate(nodes):
 if not effect(i):continue
 lines=[]
 # Exact reference LIFO visitation: preserve first row for overlapping constraints.
 for step in reversed(steps):
  tag=step[0]
  if tag=='edge':
   row=step[1];target=row['expectedDefinition'];assert target is None or target in roots
   ptr='/$defs/'+owner+R.pointer(path)
   lines.append('c.add(location, '+rs(ptr)+', Collection::'+collections[row['collection']]+', '+('None'if target is None else'Some(RecordKind::'+target+')')+', ReferenceType::'+rtypes[row['referenceType']]+', v)?;')
  elif tag in ['ref','all']:lines.append(call(step[1]))
  elif tag=='match':
   if effect(step[2]):lines.append('if shapes::fragment_matches('+str(step[1])+',v) { '+call(step[2])+' }')
  elif tag=='if':
   _,j,a,b=step
   if (a is not None and effect(a))or(b is not None and effect(b)):
    lines.append('if shapes::fragment_matches('+str(j)+',v) { '+(call(a)if a is not None else'')+' } else { '+(call(b)if b is not None else'')+' }')
  elif tag=='property':
   _,key,j=step
   if effect(j):lines.append('if let V::Object(o)=v && let Some(v)=o.get('+rs(key)+') { at(location, '+rs(key)+'.into(), |location| { '+call(j)+' Ok(()) })?; }')
  elif tag=='items':
   j=step[1]
   if effect(j):lines.append('if let V::Array(a)=v { for (i,v) in a.iter().enumerate().rev() { at(location,i.to_string(),|location| { '+call(j)+' Ok(()) })?; } }')
 out.append('fn walk_'+str(i)+'(v:&V,location:'+('&mut Vec<String>'if mutable(i)else'&[String]')+',c:&mut Collector)->Result<(),Error> { '+'\n'.join(lines)+'\nOk(()) }')
(S/'product/crates/security/src/trust_record_visit_nodes.rs').write_text('\n'.join(out)+'\n');(S/'reader-generation-report.json').write_text(json.dumps({'schemaSha256':hashlib.sha256((base/'trust-record-schema.json').read_bytes()).hexdigest(),'referenceSha256':wire['referenceSha256'],'roots':roots,'registryRows':len(bindings),'schemaVisitors':len(nodes),'edgeVisitors':sum(useful.values()),'registry':R.WIRE_REGISTRY,'exactReferenceLifoTraversal':True},indent=2)+'\n');print(len(nodes),sum(useful.values()),len(bindings))
