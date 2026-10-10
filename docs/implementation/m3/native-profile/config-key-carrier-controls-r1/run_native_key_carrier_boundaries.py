from pathlib import Path
import json,sys,hashlib,subprocess,copy
sys.path.insert(0,'/tmp/opensip-implementation/measurement-jsonschema-4.25.1')
from jsonschema import Draft202012Validator
b=Path('/tmp/opensip-implementation');r=b/'native-key-carrier-boundaries-2026-10-10';assert not r.exists();r.mkdir();p=Path('/Users/sb/code/opensip-ai/opensip/schemas/sources/native-v2.schema.json');a=Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/native/native-evidence.schemas.v2.json');current=json.loads(p.read_text());authority=json.loads(a.read_text());assert current['$defs']['CargoConfigProjectionV2']==authority['$defs']['CargoConfigProjectionV2'];schema=dict(current,**{'$ref':'#/$defs/CargoConfigProjectionV2'});v=Draft202012Validator(schema)
base=dict(schemaVersion=2,honoredKeys=[],strippedKeys=[],replacedSnapshotConfigs=[],rustflags=dict(honored=[],stripped=[],executableSelected=False),ancestorCarrierVerified=True,cargoHome='private-empty',environmentProjection='none',claimsCargoSwitch=False,projectionSha256='0'*64)
paths=[['a'*256],['a'*257],['é'*254],['é'*255],['\0'*42+'aa'],['\0'*42+'aaa'],['']];raw=json.dumps(paths).encode();notation=b/'native-config-key-notation-controls-2026-10-10/key_notation';keys=json.loads(subprocess.check_output([str(notation)],input=raw));assert [len(s) for s in keys]==[256,257,256,257,256,257,2]
rows=[]
def check(name,value,expected,keyword=None):
 errors=list(v.iter_errors(value));passed=not errors;assert passed==expected,(name,[(list(e.path),e.validator,e.message)for e in errors]);
 if keyword:assert any(e.validator==keyword for e in errors)
 rows.append(dict(case=name,expectedValid=expected,observedValid=passed,errors=[dict(path=list(e.path),validator=e.validator)for e in errors],record=value))
check('empty-complete-populations',base,True)
for field in ['honoredKeys','strippedKeys']:
 for n in [64,65]:
  x=copy.deepcopy(base);x[field]=[f'key{i:02}'for i in range(n)];check(field+'-'+str(n),x,n==64,None if n==64 else 'maxItems')
 for label,key,valid in zip(['ascii256','ascii257','quotedUnicode256','quotedUnicode257','escapedControls256','escapedControls257','emptyNamedSegment'],keys,[True,False,True,False,True,False,True]):
  x=copy.deepcopy(base);x[field]=[key];check(field+'-'+label,x,valid,None if valid else 'maxLength')
 x=copy.deepcopy(base);x[field]=['a','a'];check(field+'-duplicate',x,False,'uniqueItems')
 x=copy.deepcopy(base);x[field]=[''];check(field+'-raw-empty-record',x,False,'minLength')
# The structural schema does not itself enforce semantic set disjointness.
x=copy.deepcopy(base);x['honoredKeys']=['a'];x['strippedKeys']=['a'];check('cross-population-overlap-structurally-valid-needs-semantic-owner',x,True)
def pin(f):raw=f.read_bytes();return dict(path=str(f),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
(r/'cases.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False)+'\n');checks=dict(passed=True,cases=len(rows),currentCompiledSchema=pin(p),authoritySchema=pin(a),cargoProjectionDefinitionUnchanged=True,notationBinary=pin(notation),existingMaxItems=64,existingMaxLengthUnicodeScalars=256,quotedUnicodeExactBoundaryUtf8Bytes=len(keys[2].encode()),crossPopulationDisjointnessNotStructural=True,independentPythonSchemaReferenceOnly=True,actualFirstPartySchemaDecoderRun=False,actualKeyClassification=False,actualOwnedDiscovery=False,productCodeChanged=False,productQualification=False,entirePlanComplete=False);(r/'checks.json').write_text(json.dumps(checks,indent=2)+'\n');print(json.dumps(checks))
