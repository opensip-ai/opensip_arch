"""Bounded exact-schema review of retained consumer CommandEnvelope records.
No consumer imports, reminting, mutation, whole workflow acceptance or host proof.
"""
from pathlib import Path
import argparse,json,hashlib,importlib.util
from referencing import Registry,Resource
from referencing.jsonschema import DRAFT202012
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--manifest',type=Path,required=True);p.add_argument('--manifest-sha256',required=True);p.add_argument('--runtime',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
sha=lambda b:hashlib.sha256(b).hexdigest()
assert (a.runtime/'process-completion.json').is_file()
assert not a.out.exists() and not a.out.resolve().is_relative_to(a.runtime.resolve()) and not a.out.resolve().is_relative_to(a.source.resolve())
raw=a.manifest.read_bytes();assert sha(raw)==a.manifest_sha256;mf=json.loads(raw)
for r in mf['files']:
 raw=(a.source/r['path']).read_bytes();assert len(raw)==r['bytes'] and sha(raw)==r['sha256'],r['path']
f=a.source/'docs/coop/design-corrections/foundation/canonical.py';spec=importlib.util.spec_from_file_location('root_envelope_canonical',f);C=importlib.util.module_from_spec(spec);spec.loader.exec_module(C)
wf=a.source/'docs/coop/design-corrections/workflows/schemas';e3=wf/'evaluator3';schemas={}
paths=list(sorted(e3.glob('*.schema.json')))+[wf/n for n in ['common.schema.json','imported-evidence.schema.json','policy-document.schema.json','policy-document.v2.schema.json','test-execution.schema.json']]
for f in paths:
 d=C.parse(f.read_bytes());assert d['$id'] not in schemas;schemas[d['$id']]=d
reg=Registry().with_resources([(k,Resource(contents=v,specification=DRAFT202012)) for k,v in schemas.items()])
schema=C.parse((e3/'command-envelope.schema.json').read_bytes());rows=[];inputs=[];a.out.mkdir()
def visit(v,loc,file,context):
 if isinstance(v,dict):
  context={**context,**{k:v[k] for k in ['label','case','classification','admitted','owningSchemaAdmitted'] if k in v}}
  if v.get('schemaFamily')=='opensip.product.envelope':
   errors=[]
   try:
    C.typed(v);C.ExactValidator(schema,registry=reg).validate(v)
   except Exception as exc:errors.append({'type':type(exc).__name__,'reason':str(exc)})
   rows.append({'file':file,'jsonPointer':loc,'context':context,'schemaAdmission':'REFUSE' if errors else 'ADMIT','errors':errors})
  for k,x in v.items():visit(x,loc+'/'+str(k).replace('~','~0').replace('/','~1'),file,context)
 elif isinstance(v,list):
  for i,x in enumerate(v):visit(x,loc+'/'+str(i),file,context)
for f in sorted((a.runtime/'output/envelopes').glob('*.json')):
 raw=f.read_bytes();d=C.parse(raw);dst=a.out/'exact-inputs'/f.name;dst.parent.mkdir(exist_ok=True);dst.write_bytes(raw);inputs.append({'path':str(f),'sha256':sha(raw),'bytes':len(raw)});visit(d,'',f.name,{})
contradictions=[r for r in rows if r['context'].get('owningSchemaAdmitted') is True and r['schemaAdmission']=='REFUSE']
report={'standing':'Exact retained CommandEnvelope records against frozen owning schema and canonical exact validator. Bounded schema checks only, no semantic response/projection/host conformance, no independent consumer assent or full charter assessment. Invalid controls may properly refuse.','manifestSha256':a.manifest_sha256,'sourceFilesVerified':len(mf['files']),'scriptSha256':sha(Path(__file__).read_bytes()),'inputs':inputs,'records':rows,'claimedSchemaAdmitContradictions':contradictions}
(a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'records':len(rows),'schemaAdmit':sum(r['schemaAdmission']=='ADMIT' for r in rows),'schemaRefuse':sum(r['schemaAdmission']=='REFUSE' for r in rows),'claimedSchemaAdmitContradictions':len(contradictions)}))
