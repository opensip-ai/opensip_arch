"""Composed maximum container depth from schema structure and enforced owner caps.

Finite closed schema structure is used directly. Recursive owner material is
bounded only at an explicitly identified codec admission boundary. No boundary
is inferred merely from a $ref or an arbitrary schema ID.
"""
from pathlib import Path
import hashlib,json,types,math
HERE=Path(__file__).resolve().parent

def load(path,name):
 m=types.ModuleType(name);m.__file__=str(path);exec(compile(path.read_bytes(),str(path),'exec'),m.__dict__);return m
V=load(HERE/'check_model_carriers.py','v')
C='urn:opensip:product-v1:workflows:evaluator3:common:3#/$defs/'
I='urn:opensip:product-v1:workflows:evaluator3:invocation:5#/$defs/'
G=V.query_schema['$id']+'#/$defs/'
N='urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/'
P='urn:opensip:product-v1:policy-document:2#/$defs/'
# All these are checked by report08 embedded_owner_records and typed(value,
# nativeOffset). The additional history/config/catalogue projections below
# are structurally finite and do not receive an invented 32-depth assertion.
CAPS={'urn:opensip:product-v1:workflows:evaluator3:command-envelope:7':32,
 G+'GraphQueryRequestV1':32,G+'GraphQueryResponseV1':32,
 N+'CoverageResultV3':32,N+'ReleaseCapabilityRegistryV1':32,
 'urn:opensip:product-v1:workflows:evaluator3:comparison:2':32,
 I+'AnalysisResult':31,C+'StepTermination':29,C+'FindingSurface':30,P+'Rule':30}
seen_caps={};memo={}


def literal_depth(v):
 if isinstance(v,dict):return 1+max([literal_depth(x) for x in v.values()],default=0)
 if isinstance(v,list):return 1+max([literal_depth(x) for x in v],default=0)
 return 0


def resolve(base,ref):
 uri,sep,fragment=ref.partition('#');uri=uri or base;node=V.schemas[uri]
 if fragment:
  assert fragment.startswith('/')
  for token in fragment[1:].split('/'):node=node[token.replace('~1','/').replace('~0','~')]
 return uri,node,uri+('#'+fragment if sep else '')


def depth(base,node,stack=()):
 if node is False:return 0
 if not isinstance(node,dict):return math.inf
 candidates=[]
 if '$ref' in node:
  uri,target,key=resolve(base,node['$ref'])
  if key in stack:value=math.inf
  elif key in memo:value=memo[key]
  else:
   value=depth(uri,target,stack+(key,))
   # Cache only acyclic results; recursion context can change a provisional
   # infinity into a finite bound through an enclosing codec boundary.
   if math.isfinite(value):memo[key]=value
  if key in CAPS:
   seen_caps[key]={'nativeRemainingDepth':CAPS[key],'structuralDepth':value if math.isfinite(value) else 'unbounded-or-recursive'}
   value=min(value,CAPS[key])
  candidates.append(value)
 if 'const' in node:candidates.append(literal_depth(node['const']))
 if 'enum' in node:candidates.append(max((literal_depth(v) for v in node['enum']),default=0))
 for k in ['oneOf','anyOf']:
  if k in node:candidates.append(max((depth(base,v,stack) for v in node[k]),default=0))
 if 'allOf' in node:candidates.append(min((depth(base,v,stack) for v in node['allOf']),default=math.inf))
 types=node.get('type',[]);types=[types] if isinstance(types,str) else types
 if types:
  values=[]
  for kind in types:
   if kind in ['null','boolean','integer','number','string']:values.append(0)
   elif kind=='object':
    if node.get('additionalProperties') is not False:values.append(math.inf)
    else:
     children=list(node.get('properties',{}).values())+list(node.get('patternProperties',{}).values())
     values.append(1+max((depth(base,v,stack) for v in children),default=0))
   elif kind=='array':
    if node.get('maxItems')==0:values.append(1);continue
    children=list(node.get('prefixItems',[]))
    if node.get('items') is not False:children.append(node.get('items',True))
    values.append(1+max((depth(base,v,stack) for v in children),default=0))
   else:raise ValueError(kind)
  candidates.append(max(values))
 return min(candidates,default=math.inf)

if __name__=='__main__':
 report=V.report;root={name:depth(report['$id'],value) for name,value in report['properties'].items()}
 bound=depth(report['$id'],report)
 out={'standing':'Proposed schema/owner-codec depth derivation; boundary completeness and matching consumer enforcement still require verification',
      'inputReportSha256':hashlib.sha256((HERE/'composed-sources/report-projection.proposed.schema.json').read_bytes()).hexdigest(),
      'documentMaxContainerDepth':bound if math.isfinite(bound) else 'unbounded',
      'rootValueDepths':{k:v if math.isfinite(v) else 'unbounded' for k,v in root.items()},'appliedOwnerCaps':seen_caps,
      'currentProfileDepth':report['$defs']['BudgetProfileV1']['properties']['maxJsonDepth']['const']}
 (HERE/'joint-depth-derivation.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
 if not math.isfinite(bound):raise SystemExit(1)
