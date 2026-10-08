"""Synthetic canonical capacity counterexample, no snapshot/source admission."""
from pathlib import Path
import importlib.util,json,hashlib,sys
A=Path('/Users/sb/code/opensip-ai/opensip_arch')
sys.path.insert(0,'/tmp/opensip-implementation/c2a-protocol-major-panel/audit-deps')
spec=importlib.util.spec_from_file_location('selected_canonical',A/'docs/coop/design-corrections/foundation/canonical.py')
can=importlib.util.module_from_spec(spec);spec.loader.exec_module(can)
limit=can.MAX_BYTES
base={'schemaVersion':2,'projectId':'prj1-'+('0'*64),'sourceInventory':[],'resolvedConfigDigest':'0'*64,'scopeDigest':'0'*64,'vcsDigest':'0'*64}
# Shapes are symbolic. Digests do not stand for retained artifacts or source admission.
row={'path':'files/00000000.rs','sha256':'0'*64,'bytes':0}
base_len=len(json.dumps(base,sort_keys=True,separators=(',',':')).encode())
row_len=len(can.canonical(row))
count=(limit-base_len+1)//(row_len+1)
rows=[dict(row,path=f'files/{i:08d}.rs') for i in range(count)]
snapshot=dict(base,sourceInventory=rows)
raw=can.canonical(snapshot)
assert len(raw)<=limit
native=[{'path':r['path'],'contentSha256':r['sha256'],'byteLength':r['bytes']} for r in rows]
native_bytes=json.dumps(native,sort_keys=True,separators=(',',':')).encode()
assert len(native_bytes)>limit
try:can.canonical(native)
except can.AdmissionError as exc:assert str(exc)=='BYTE_LIMIT'
else:raise AssertionError('Required canonical refusal did not occur')
# Validate complete synthetic record/array shapes against selected schemas.
# Exact uniqueness is checked in linear time by canonical item bytes, keeping
# the original schema, order checks and all row validation unchanged.
from jsonschema import validators,ValidationError
foundation=json.loads((A/'docs/coop/design-corrections/foundation/identity-schemas.v3.json').read_text())
native_schema=json.loads((A/'docs/coop/design-corrections/native/native-evidence.schemas.v2.json').read_text())
def unique(validator,required,value,schema):
    if required and type(value) is list:
        seen=set()
        for item in value:
            key=can.canonical(item)
            if key in seen:
                yield ValidationError('duplicate canonical typed value')
                return
            seen.add(key)
AuditValidator=validators.extend(can.ExactValidator,validators={'uniqueItems':unique})
AuditValidator({'$ref':'#/$defs/snapshot','$defs':foundation['$defs']}).validate(snapshot)
AuditValidator({'$ref':'#/$defs/DependencyFileManifestV1','$defs':native_schema['$defs']}).validate(native)
assert [r['path'] for r in rows]==sorted({r['path'] for r in rows},key=lambda s:s.encode())
assert all(r['bytes']==0 and r['sha256']=='0'*64 for r in rows)
assert len(native_bytes)-len(can.canonical(rows))==12*count
report={'standing':'Synthetic canonical byte-capacity counterexample only; no actual snapshot/custody/source admission','rowCount':count,'canonicalLimitBytes':limit,'snapshotRecordCanonicalBytes':len(raw),'snapshotRecordSha256':hashlib.sha256(raw).hexdigest(),'snapshotBlobArrayBytes':len(can.canonical(rows)),'nativeProjectionBytes':len(native_bytes),'nativeProjectionSha256':hashlib.sha256(native_bytes).hexdigest(),'projectionExpansionBytes':12*count,'nativeProjectionRefusal':'BYTE_LIMIT','completeSyntheticSnapshotShapeValid':True,'completeSyntheticNativeArrayShapeValid':True,'actualSnapshotAdmitted':False,'sourceProfilePublished':False,'actualOwnerAdmission':False,'productQualification':False}
Path(__file__).with_name('path-capacity-report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
