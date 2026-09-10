"""Does the at-most-one ambiguity guard really precede EVERYTHING for an ambiguous spec?

The proposed comment said: "Ambiguity is decidable without reading `scope` at all, so it is decided
first and every caller of an ambiguous spec is told the same one thing."
This probe tests that sentence against the actual frozen executable code.
"""
import importlib.util,json,sys
from pathlib import Path
ROOT=Path(sys.argv[1]).resolve()/'docs/coop/design-corrections'
def load(name,path):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
W=load('wf',ROOT/'workflows/workflows_model.v1.py')
sys.path.insert(0,str(ROOT/'foundation'))
import canonical as C

SCHEMA_DIGEST=W.raw_sha((ROOT/W.SCOPE_DOCUMENT_SCHEMA).read_bytes())
A={'schemaFamily':'opensip.product.scope','schemaMajor':1,'include':['src/**'],'exclude':[]}
B={'schemaFamily':'opensip.product.scope','schemaMajor':1,'include':['lib/**'],'exclude':[]}
def row(doc):return {'schemaDigest':SCHEMA_DIGEST,'payloadDigest':W.doc_digest(doc)}
def spec(rows):return {'schemaVersion':2,'policyPackIds':[],'requestedCapabilities':[],
                       'parameters':sorted(rows,key=C.canonical)}
AMBIGUOUS=spec([row(A),row(B)])

def outcome(doc,label):
    try:
        d=W.verify_scope_parameter_binding(AMBIGUOUS,doc)
        return {'case':label,'raised':None,'result':d}
    except W.Refusal as exc:
        return {'case':label,'raised':'Refusal','errorCode':exc.error_code,'detail':exc.detail}
    except Exception as exc:
        return {'case':label,'raised':type(exc).__name__,'message':str(exc)}

cases=[
 (A,'candidate-A (canonicalizable, IS a selected row)'),
 ({'schemaFamily':'opensip.product.scope','schemaMajor':1,'include':['other/**'],'exclude':[]},
  'non-candidate (canonicalizable, admitted shape)'),
 ({'schemaFamily':'opensip.product.scope','schemaMajor':1,'include':['x/**'],'exclude':[],'weight':1.5},
  'NON-CANONICALIZABLE float member'),
 ({'schemaFamily':'opensip.product.scope','schemaMajor':1,'include':['x/**'],'exclude':[],'n':-0.0},
  'NON-CANONICALIZABLE negative zero'),
 ({1:'x'},'NON-CANONICALIZABLE non-string key'),
]
out=[outcome(d,l) for d,l in cases]
print(json.dumps(out,indent=2))
same={json.dumps({k:v for k,v in o.items() if k!='case'},sort_keys=True) for o in out}
print('\nDISTINCT ANSWERS FOR ONE AMBIGUOUS SPEC:',len(same))
print('CLAIM "every caller of an ambiguous spec is told the same one thing" HOLDS:',len(same)==1)
