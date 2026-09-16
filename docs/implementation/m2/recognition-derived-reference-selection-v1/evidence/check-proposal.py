from pathlib import Path
import ast,copy,hashlib,importlib.util,json,subprocess
A=Path('/Users/sb/code/opensip-ai/opensip_arch');B=Path('/tmp/opensip-implementation/m2-retained-graph-trial-04')
O=Path('/tmp/opensip-implementation/m2-grok-current-fixture-composition-01/review/archroot/docs/coop/design-corrections')
report=json.loads((A/'docs/implementation/m2/reviews/grok-current-fixture-composition-01/report.json').read_bytes())
for row in report['requiredCurrentOverlays']:
 raw=(O/row['overlayPath']).read_bytes();assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
s=importlib.util.spec_from_file_location('records_current_identity',O/'foundation/identity-model.v3.py');I=importlib.util.module_from_spec(s);s.loader.exec_module(I);C=I.C
F=Path('/tmp/opensip-implementation/m2-recognition-derived-fix-candidate-01/identity_model.proposed.v4.py');tree=ast.parse(F.read_text());names=['get','deref','branch_matches','carries_digest','walk','digest_field','blob','canonical_bytes','payload','foreign_payload']
parent=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='open_run_closure')
nodes=[n for n in parent.body if isinstance(n,ast.FunctionDef) and n.name in names];assert len(nodes)==10
ns={k:getattr(I,k) for k in ['C','copy','hashlib','SCHEMA','DIGESTS','DOMAIN_OF','PREFIX','ROOT_ORDER_PATH','identifier','ordered','admit_closure_field_kinds','EvidenceUnavailable','validate_registered_record','admit_foundation_digest_law','foundation_record_document','registered_schema_documents']}
exec(compile(ast.Module(body=nodes,type_ignores=[]),str(F),'exec'),ns)
class Unsupported(Exception):pass
original=ns['digest_field']
def digest_field(annotation,value,siblings):
 if annotation.get('retention') in ('fragment','owner-retained'):raise Unsupported()
 kind=annotation['representation']
 if kind=='capability-manifest-id' or (kind=='h-identity' and 'domain' not in annotation):raise Unsupported()
 if kind=='canonical-record' and 'payloadClass' in annotation['record']:raise Unsupported()
 return original(annotation,value,siblings)
def visit(key,domain):
 if key in ns['seen']:return
 value=ns['get'](key,domain);ns['seen'].add(key);ns['walk'](I.SCHEMA['$defs'][domain],value)
ns.update(digest_field=digest_field,visit=visit)
registry=json.loads((B/'product/schemas/admission-registry.json').read_bytes())
# Exact logical alias map is selected runtime input; do not infer by URI/major.
aliases=registry.get('documentAliases',registry.get('aliases'))
assert aliases is not None,registry.keys()
print('alias layout',type(aliases).__name__)
by_id={r['schemaId']:r['logicalDocument'] for r in aliases}
corpus=Path('/tmp/opensip-implementation/m2-schema-engine-trial-03/registered-cases.jsonl')
cases=[]
for i,line in enumerate(corpus.read_bytes().splitlines()):
 r=json.loads(line);sid,selector=r['ref'].split('#',1)
 if sid not in by_id:continue
 # All nine foundation aliases; a smaller representative foreign owner set.
 document=by_id[sid]
 if not document.startswith('foundation/') and selector not in ['/$defs/PolicyDocumentV2','/$defs/RuntimePayloadV1','/$defs/DependencyFileManifestV1']:continue
 raw=C.canonical(r['value']);sha=hashlib.sha256(raw).hexdigest()
 cases.append({'label':'schema:'+str(i),'mode':'record','document':document,'selector':'#'+selector,'digest':sha,'objects':[],'blobs':[{'digest':sha,'hex':raw.hex()}]})
for document in sorted(set(by_id.values())):
 if not document.startswith('foundation/'):continue
 for raw in [b'{ }',b'1.0',b'\xff',b'{"a":1,"a":1}']:
  sha=hashlib.sha256(raw).hexdigest();cases.append({'label':'noncanonical:'+document+':'+repr(raw),'mode':'record','document':document,'selector':'#','digest':sha,'objects':[],'blobs':[{'digest':sha,'hex':raw.hex()}]})
# Exact direct foreign-record regression and bounded law mutation controls.
q=next(q for q in cases if q['document']=='foundation/framework-recognition-plan.schema.v1.json' and q['selector']=='#/$defs/UnitRecognitionV1' and len(q['blobs'][0]['hex'])>100)
# Find a shape-valid UnitRecognitionV1, not the primitive adversaries.
for candidate in cases:
 if candidate['document']!=q['document'] or candidate['selector']!=q['selector']:continue
 value=C.parse(bytes.fromhex(candidate['blobs'][0]['hex']))
 try:I.validate_registered_record(candidate['document'],candidate['selector'],value)
 except C.AdmissionError:continue
 q=copy.deepcopy(candidate);break
value=C.parse(bytes.fromhex(q['blobs'][0]['hex']))
value['recognitionId']='sha256:'+C.identity('native.framework-recognition.v1',value['recognition'])
for label,v in [('correct-inline-identity',value),('mismatched-inline-identity',dict(value,recognitionId='sha256:'+'0'*64))]:
 raw=C.canonical(v);sha=hashlib.sha256(raw).hexdigest();qq=copy.deepcopy(q);qq.update(label=label,digest=sha,blobs=[{'digest':sha,'hex':raw.hex()}]);cases.append(qq)
expected=[];faults=[]
for q in cases:
 ns.update(objects={},blobs={r['digest']:bytes.fromhex(r['hex']) for r in q['blobs']},seen=set(),parsed={})
 try:ns['foreign_payload'](q['digest'],q['document'],q['selector']);out='ok'
 except Unsupported:out='unsupported'
 except I.EvidenceUnavailable:out='unavailable'
 except (C.AdmissionError,C.ValidationError):out='invalid'
 except Exception as e:faults.append({'label':q['label'],'exception':repr(e)});out='reference-fault'
 expected.append(out)
assert expected[-2:]==['ok','invalid'],expected[-2:]
assert not faults,faults
B=Path('/tmp/opensip-implementation/m2-recognition-derived-fix-candidate-01')
(B/'record-requests.ndjson').write_bytes(b''.join(C.canonical(q)+b'\n' for q in cases))
(B/'proposed-expected.txt').write_text('\n'.join(expected)+'\n')
result={'standing':'Proposed reference only, not accepted or installed','cases':len(cases),'outcomes':{x:expected.count(x) for x in sorted(set(expected))},'referenceFaults':faults,'inlineCorrectHash':'ok','inlineWrongHash':'invalid','fullRunTested':False}
(B/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
