from pathlib import Path
import hashlib,json
from jsonschema import Draft202012Validator
here=Path(__file__).resolve().parent;r=json.loads((here/'result.json').read_text())
for row in r['sourceImages']:assert hashlib.sha256((here/row['path']).read_bytes()).hexdigest()==row['sha256']
old=json.loads((here/'native-schema.v5.json').read_text());draft=json.loads((here/'native-schema.v6-draft.json').read_text())
path=r['hashDirectory']['value']['markerPath']
assert not list(Draft202012Validator(dict(old,**{'$ref':'#/$defs/CanonicalPath'})).iter_errors(path))
v=Draft202012Validator(dict(draft,**{'$ref':'#/$defs/SourceUnitOwnershipV1/properties/units/items'}))
assert not list(v.iter_errors(r['control']['value']))
errors=[{'path':'/'.join(map(str,e.absolute_path)),'validator':e.validator,'message':e.message} for e in v.iter_errors(r['hashDirectory']['value'])]
assert errors==r['hashDirectory']['errors']
print(json.dumps({'reproduced':True,'existingPathAdmitted':True,'controlAdmitted':True,'draftRefusalAt':'markerPath/pattern','fullRunClaim':False}))
