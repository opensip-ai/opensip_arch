from pathlib import Path
import json,types
HERE=Path(__file__).resolve().parent
def load(name):
 p=HERE/(name+'.py');m=types.ModuleType(name);m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m
I=load('check_identity_integration');P=load('identity_fixture');A=load('new_plan_admission')
with P.models(I.V,I.B) as (parent,succ):
 native=succ.load('new_plan_native',succ.root/I.B.DC/'native/native_evidence_model.v2.py')
 raw=succ.expected[I.B.DC+'native/native_evidence_model.v2.py']
 schema=I.V.schemas['urn:opensip:product-v1:native:evidence-schemas:v2']
 bound=A.bind(raw,native,succ.R.M,I.F,schema)
 _,_,blobs,graph=I.B.positive_run(succ.F,succ.R)
 spec=blobs[graph['inputs']['plan']['analysisSpecDigest']]
 print('TYPE',type(spec).__name__)
 print('SPEC',json.dumps(spec))
 print('SCHEMA_DEFS',[k for k in succ.R.M.SCHEMA['$defs'] if 'analysis' in k.lower()])
 print('CAPS',[r for r in native.CAPABILITY_MATRIX['cells'] if r['mode']=='ts-tsconfig'][:3] )
