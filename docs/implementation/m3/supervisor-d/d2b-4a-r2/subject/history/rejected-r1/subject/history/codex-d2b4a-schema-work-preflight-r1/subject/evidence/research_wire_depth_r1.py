from pathlib import Path
import json,re,hashlib
W=Path('/Users/sb/code/opensip-ai/opensip-d2b4a-takeover');F=Path(__file__).parent
names=re.findall(r'/../../(schemas/sources/[^"\n]+)',(W/'crates/components/src/schema_sources.rs').read_text());assert len(names)==52
D={};pins=[]
for name in names:
 raw=(W/name).read_bytes();d=json.loads(raw);D[d['$id']]=d;pins.append(dict(path=name,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
raw=(W/'schemas/wire/native-carriers-v1.json').read_bytes();C=json.loads(raw);pins.append(dict(path='schemas/wire/native-carriers-v1.json',bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
def resolve(ref,current):
 base,pointer=ref.split('#',1);base=base or current;node=D[base]
 for token in pointer.split('/')[1:]:node=node[token.replace('~1','/').replace('~0','~')]
 return node,base
# A structural upper bound. Branch correlations can make it conservative;
# no claim of deepest-valid reachability from this calculation alone.
def schema(s,current,seen=()):
 if not isinstance(s,dict):return 0
 best=0
 if '$ref'in s:
  ref=s['$ref'];key=(current if ref.startswith('#') else '')+ref;assert key not in seen,key
  node,base=resolve(ref,current);best=schema(node,base,seen+(key,))
 for k in ('allOf','anyOf','oneOf'):
  best=max([best]+[schema(v,current,seen) for v in s.get(k,[])])
 for k in ('if','then','else','not'):
  if k in s:best=max(best,schema(s[k],current,seen))
 types=s.get('type',[]);types=[types]if isinstance(types,str)else types
 if 'object'in types or any(k in s for k in ('properties','patternProperties','additionalProperties')):
  children=[v for k in ('properties','patternProperties')for v in s.get(k,{}).values()]
  if isinstance(s.get('additionalProperties'),dict):children.append(s['additionalProperties'])
  best=max(best,1+max([0]+[schema(v,current,seen)for v in children]))
 if 'array'in types or 'items'in s or 'prefixItems'in s:
  children=list(s.get('prefixItems',[]))
  if isinstance(s.get('items'),dict):children.append(s['items'])
  best=max(best,1+max([0]+[schema(v,current,seen)for v in children]))
 return best

def carrier(t,seen=()):
 tag=t['t']
 if tag in ('uint64','text','bytes','null','bool'):return 0
 if tag=='nullable':return carrier(t['of'],seen)
 if tag=='array':return 1+carrier(t['items'],seen)
 if tag=='extern':
  node,base=resolve(t['schemaRef'],'');return schema(node,base)
 if tag=='ref':
  name=t['ref'];assert name not in seen,name
  if name in C['scalars']:return carrier(C['scalars'][name]['type'],seen+(name,))
  r=C['records'][name]
  if r['kind']=='alias':return carrier(r['target'],seen+(name,))
  if r['kind']=='record':children=[m['type']for m in r['members']]
  else:children=[v for variant in r['variants'].values()for v in variant.values()]
  return 1+max([0]+[carrier(v,seen+(name,))for v in children])
 if tag=='frame-payload':
  children=[]
  for f in C['protocols'][t['protocol']]['frames']:
   p=f['payload'];children.extend(p.get('alternatives',{'':p}).values())
  return max(carrier(v,seen)for v in children)
 raise AssertionError(tag)
frames=[]
for f in C['protocols']['rust-semantic']['frames']:
 p=f['payload'];alts=p.get('alternatives',{'':p});frames.append(dict(frame=f['frameType'],direction=f['direction'],envelopeDepthUpperBound=1+max(carrier(v)for v in alts.values())))
result=dict(standing='STRUCTURAL RESEARCH ONLY; NO DEEPEST-VALID OR FULL SUCCESSOR CLOSURE CLAIM',sourcePins=pins,frames=frames,baseEnvelopeUpperBound=carrier({'t':'ref','ref':'Rust3ProviderFrameV3'}),pending=['Explicit FA2 and RUST3-LIM payload successor roots','Verify schemas with permissive unconstrained members cannot carry deeper legal values','A deepest-valid received envelope and a one-over strict-reader control','Separate embedded relation payload closure'])
(F/'wire-depth-research-r1.json').write_text(json.dumps(result,indent=2)+'\n');print('base envelope bound',result['baseEnvelopeUpperBound']);print('maximal frames',[x for x in frames if x['envelopeDepthUpperBound']==result['baseEnvelopeUpperBound']])
