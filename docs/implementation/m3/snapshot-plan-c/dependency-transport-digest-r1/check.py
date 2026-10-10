from pathlib import Path
import json,hashlib,types,importlib.util,sys,copy
sys.path.insert(0,'/tmp/opensip-implementation/measurement-jsonschema-4.25.1')
B=Path(__file__).resolve().parent;A=Path('/Users/sb/code/opensip-ai/opensip_arch');V=B/'reference-encoders'
def load(path,name):m=types.ModuleType(name);m.__file__=str(path);exec(compile(path.read_text(),str(path),'exec'),m.__dict__);return m
E=load(V/'accounting.py','actual_encoder');I=load(V/'independent_host_codec.py','independent_encoder');mp=A/'docs/coop/design-corrections/native/native_evidence_model.v2.py';spec=importlib.util.spec_from_file_location('native_model',mp);M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
vectors=json.loads((B/'vectors.json').read_text())['vectors'];proposed=json.loads((B/'dependency-transport-digest.schemas.v1.json').read_text())['$defs'];controls=[]
for name,value in proposed.items():
 before=copy.deepcopy(M.SCHEMAS['$defs'][name]);after=copy.deepcopy(value);old=before['properties']['manifestSha256']['x-opensip-digest'].pop('artifact');new=after['properties']['manifestSha256']['x-opensip-digest'].pop('artifact');assert before==after and old!=new
for v in vectors:
 raw=E.encode(v['entries']);assert raw==I.encode(v['entries']);assert raw.hex()==v['cborHex'];assert hashlib.sha256(raw).hexdigest()==v['manifestSha256'];payload=dict(dependencySourceSetId='sha256:'+'a'*64,manifestSha256=v['manifestSha256'],entries=v['entries']);M.validate_native('DependencySourceManifestV3',payload)
 controls.append(dict(case='positive-'+v['name'],schemaPass=True,independentCborEqual=True,exactPreimageDigestPass=True))
base=vectors[-1]['entries'];original=hashlib.sha256(E.encode(base)).hexdigest()
for name,operation in [('package-key',lambda rows:rows[0].__setitem__('packageKey','pkg1-'+'c'*64)),('path',lambda rows:rows[0].__setitem__('path','src/other.rs')),('byte-length',lambda rows:rows[0].__setitem__('byteLength',1)),('content-digest',lambda rows:rows[0].__setitem__('contentSha256','c'*64)),('array-order',lambda rows:rows.reverse())]:
 rows=copy.deepcopy(base);operation(rows);assert hashlib.sha256(E.encode(rows)).hexdigest()!=original;controls.append(dict(case=name,completeArrayPreimageChanged=True))
payload=dict(dependencySourceSetId='sha256:'+'a'*64,manifestSha256=original,entries=base);other=dict(payload,dependencySourceSetId='sha256:'+'b'*64);assert hashlib.sha256(E.encode(payload)).hexdigest()!=hashlib.sha256(E.encode(other)).hexdigest();assert E.encode(payload['entries'])==E.encode(other['entries']);controls.append(dict(case='set-id-association',entriesDigestEqual=True,fullFramePayloadDigestDifferent=True,independentSetAssociationStillRequired=True))
for name,value in [('outer-object-with-digest',payload),('outer-object-without-digest',{k:v for k,v in payload.items() if k!='manifestSha256'}),('outer-object-zero-digest',dict(payload,manifestSha256='0'*64))]:
 assert hashlib.sha256(E.encode(value)).hexdigest()!=original;controls.append(dict(case=name,differentRecipeRefused=True))
for name,wrong in [('unknown-entry-field',dict(base[0],extra=True)),('bool-byte-length',dict(base[0],byteLength=True)),('negative-byte-length',dict(base[0],byteLength=-1)),('invalid-content-digest',dict(base[0],contentSha256='bad'))]:
 try:M.validate_native('DependencySourceManifestV3',dict(payload,entries=[wrong]))
 except (M.AdmissionError,M.C.ValidationError,ValueError):controls.append(dict(case=name,existingClosedSchemaRefuses=True))
 else:raise AssertionError(name)
result=dict(standing='SYNTHETIC DESIGN CONTROLS ONLY; NO DEPENDENCY TRANSFER IMPLEMENTATION OR SOURCE ADMISSION',controls=controls,positiveVectors=3,mutationAssociationAndMalformedControls=len(controls)-3,structuralSchemaInheritedByValue=True,onlyTwoDigestAnnotationsReplaced=True,repositoryCodeExecuted=False,sourceAdmission=False,fullSM=False,productQualification=False)
if '--write' in sys.argv:(B/'checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
