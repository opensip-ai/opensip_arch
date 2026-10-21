import runpy,json
from pathlib import Path
F=Path(__file__).parent;m=runpy.run_path(str(F/'research_wire_depth_r1.py'));C,D,resolve=m['C'],m['D'],m['resolve'];memo={}
def weight(v):
 if isinstance(v,str):return 1+len(v.encode())
 if isinstance(v,list):return 1+sum(map(weight,v))
 if isinstance(v,dict):return 1+sum(len(k.encode())+weight(x)for k,x in v.items())
 return 1

def factor(s,owner,seen=()):
 if not isinstance(s,dict):return 1
 out=1
 if '$ref'in s:
  r=s['$ref'];key=(owner if r.startswith('#')else'')+r;assert key not in seen,key
  if key not in memo:
   node,base=resolve(r,owner);memo[key]=factor(node,base,seen+(key,))
  out+=memo[key]
 if 'const'in s:out+=1+weight(s['const'])
 for literal in s.get('enum',[]):out+=1+weight(literal)
 for k in ('allOf','anyOf','oneOf'):
  out+=sum(factor(x,owner,seen)for x in s.get(k,[]))
 for k in ('not','if','then','else'):
  if k in s:out+=factor(s[k],owner,seen)
 array=1+max([0]+[factor(x,owner,seen)for x in s.get('prefixItems',[])]+([factor(s['items'],owner,seen)]if'items'in s else[]))
 if 'contains'in s:array+=factor(s['contains'],owner,seen)
 if s.get('uniqueItems')is True:array+=33 # complete item weight + canonical bytes <=32*weight
 if 'x-opensip-order'in s:array+=1+weight(s['x-opensip-order'])
 obj=1+sum(1+len(k.encode())for k in s.get('required',[]))
 if 'propertyNames'in s:obj+=factor(s['propertyNames'],owner,seen)
 obj+=max([0]+[factor(x,owner,seen)for x in s.get('properties',{}).values()])
 obj+=sum(1+factor(x,owner,seen)for x in s.get('patternProperties',{}).values())
 if 'additionalProperties'in s:obj+=factor(s['additionalProperties'],owner,seen)
 return out+max(1,array,obj)
roots=set();visited=set()
def carrier(t):
 tag=t['t']
 if tag=='extern':roots.add(t['schemaRef'])
 elif tag in('array','nullable'):carrier(t['items']if tag=='array'else t['of'])
 elif tag=='ref':
  n=t['ref']
  if n in visited:return
  visited.add(n)
  if n in C['scalars']:carrier(C['scalars'][n]['type']);return
  r=C['records'][n]
  if r['kind']=='alias':carrier(r['target'])
  elif r['kind']=='record':
   for x in r['members']:carrier(x['type'])
  else:
   for v in r['variants'].values():
    for x in v.values():carrier(x)
 elif tag=='frame-payload':
  for f in C['protocols'][t['protocol']]['frames']:
   p=f['payload']
   for x in p.get('alternatives',{'':p}).values():carrier(x)
carrier({'t':'ref','ref':'Rust3ProviderFrameV3'})
# Piecewise item roots are also direct evaluator entries.
for definition,member in [('CoverageV3','entries'),('UnavailableV3','coverage'),('BudgetExhaustedV3','coverage')]:roots.add(D['opensip.product.provider-startup.1']['$defs'][definition]['properties'][member]['items']['$ref'])
rows=[]
for ref in sorted(roots):
 node,owner=resolve(ref,'');rows.append(dict(schemaRef=ref,evaluationFactor=factor(node,owner),completeAdmissionFactor=1+factor(node,owner)))
out=dict(standing='PROPOSED CONSERVATIVE METER-CREDIT UPPER BOUND; REQUIRES RUST IMPLEMENTATION AND INDEPENDENT REVIEW',sourcePins=m['pins'],roots=rows,maximumCompleteAdmissionFactor=max(x['completeAdmissionFactor']for x in rows),proof='For N=weight(value)>=1 (one per node plus UTF8 key/string bytes), evaluator cost <=C(schema)*N. Refs/branches add, array items use maximum child coefficient times total item weight, object named properties use maximum and pattern/propertyName/additional use summed conservative coefficients. Constants/required/order annotations are fixed costs amortized by N. uniqueItems canonical output <=32*item weight for exact JSON integers/model, and its extra value scan costs item weight. Full input precharge adds N. For strict byte-free deterministic CBOR, N<=encoded payload length. Failed parses/operational errors do not imply schema success. This bounds meter credits, not wall-clock time or allocations; original NFC/transport/depth/context gates remain required.')
(F/'schema-work-research-r1.json').write_text(json.dumps(out,indent=2)+'\n');print('maxFactor',out['maximumCompleteAdmissionFactor']);print(rows)
