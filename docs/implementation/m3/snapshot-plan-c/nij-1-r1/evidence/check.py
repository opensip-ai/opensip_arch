"""Proposal-only shape/identity algebra controls. No native acquisition/admission/replay."""
from pathlib import Path
import sys,json,copy,hashlib,importlib.util
sys.path.insert(0,'/tmp/opensip-implementation/c2a-protocol-major-panel/audit-deps')
from jsonschema import Draft202012Validator
D=Path(__file__).resolve().parents[1];A=Path('/Users/sb/code/opensip-ai/opensip_arch');base='docs/implementation/m1/source-selection-v2/schemas/sources/native.v2.schema.json';old=json.loads((A/base).read_text());new=json.loads((D/'completion/native.v2.schema.json').read_text());restored=copy.deepcopy(new);restored['$defs']['DependencySourcePayloadV1']['properties']['acquisitionSourcePath']=old['$defs']['DependencySourcePayloadV1']['properties']['acquisitionSourcePath'];assert restored==old
Draft202012Validator.check_schema(new)
def val(schema,value):
 v=copy.deepcopy(schema);v['$ref']='#/$defs/DependencySourcePayloadV1';return Draft202012Validator(v).is_valid(value)
setRecord=dict(schemaVersion=1,language='rust',lockfileIdentity=dict(path='Cargo.lock',contentSha256='a'*64,lockfileVersion=3),packages=[],completeness=dict(state='complete',missing=[]))
payload=dict(schemaVersion=1,payloadDomain='native.import-payload.dependency-source.v1',set=setRecord,tarballDigests=[],acquisitionSourcePath=None)
controls=[]
for label,value,oldValid,newValid in [('null',None,False,True),('historical-root','/one/root',True,True),('relocated-root','/different/root',True,True),('empty','',False,False),('length4096','a'*4096,True,True),('length4097','a'*4097,False,False),('bool',True,False,False),('number',1,False,False),('object',{},False,False),('array',[],False,False)]:
 p=copy.deepcopy(payload);p['acquisitionSourcePath']=value;assert val(old,p)==oldValid and val(new,p)==newValid,label;controls.append(dict(label=label,oldShape=oldValid,newShape=newValid,newM3PathPrecondition=value is None))
for label,change in [('absent',lambda p:p.pop('acquisitionSourcePath')),('extra-host-path',lambda p:p.update(hostSourcePath='/root')),('wrong-domain',lambda p:p.update(payloadDomain='other'))]:
 p=copy.deepcopy(payload);change(p);assert not val(old,p) and not val(new,p);controls.append(dict(label=label,oldShape=False,newShape=False))
spec=importlib.util.spec_from_file_location('nij_canonical',A/'docs/coop/design-corrections/foundation/canonical.py');C=importlib.util.module_from_spec(spec);spec.loader.exec_module(C)
def raw(v):return hashlib.sha256(C.canonical(v)).hexdigest()
oldA=copy.deepcopy(payload);oldA['acquisitionSourcePath']='/one/root';oldB=copy.deepcopy(oldA);oldB['acquisitionSourcePath']='/different/root';assert raw(oldA)!=raw(oldB)
# Independent hand-framing check of the existing H recipe, no synthetic admitted wrapper claim.
def framed(domain,value):
 b=C.canonical(value);return hashlib.sha256(b'opensip.product.v1\0'+domain.encode()+b'\0'+len(b).to_bytes(8,'big')+b).hexdigest()
probe=dict(payloadDigest=raw(payload),sourceCorrespondenceDigest=raw(dict(kind='exact-snapshot',snapshotId='snapshot2:'+'1'*64)))
assert C.identity('import',probe)==framed('import',probe)
relocated=copy.deepcopy(probe);assert C.identity('import',probe)==C.identity('import',relocated)
bodyEdited=copy.deepcopy(probe);bodyEdited['sourceCorrespondenceDigest']=raw(dict(kind='exact-snapshot',snapshotId='snapshot2:'+'2'*64));assert C.identity('import',probe)!=C.identity('import',bodyEdited)
changedSet=copy.deepcopy(setRecord);changedSet['lockfileIdentity']['contentSha256']='b'*64;assert C.identity('native.dependency-source-set.v1',setRecord)!=C.identity('native.dependency-source-set.v1',changedSet)
result=dict(standing='DESIGN SHAPE AND HASH ALGEBRA ONLY; no actual wrapper/schema admission, custody, parser, acquisition, Plan/Run closure or product qualification',schemaEqualExceptOneNamedAlternative=True,shapeControls=controls,historicalRawPathDigestDiffers=True,newNullPayloadIndependentOfAcquisitionArgument=True,snapshotCorrespondenceDigestMovesImportHashProbe=True,dependencySetContentChangeMovesIdentity=True,handFramingMatchesReference=True,actualImportWrappersAdmitted=0,nativeExecutions=0,productTestsRun=0,productQualification=False)
(D/'evidence/controls.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(shapeControls=len(controls),designAlgebraControls=5,productQualification=False)))
