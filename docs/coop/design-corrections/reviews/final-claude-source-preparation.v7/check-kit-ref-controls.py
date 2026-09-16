"""Exercise actual normative kit plus missing/conflicting reference counterexamples."""
from pathlib import Path
import copy
import json
from check_kit_schema_refs import validate_schema_references

root=Path('/tmp/opensip-design-corrections/consumer-b.v24-source38.v1/subject')
manifest=json.loads((root/'consumer-input-manifest.json').read_text())
docs={r['path']:json.loads((root/r['path']).read_text()) for r in manifest['files'] if r['path'].endswith('.json')}
positive=validate_schema_references(docs)
controls=[]
for name, ref in [('unknown-urn','urn:opensip:missing-owner:1'),('unknown-https','https://example.invalid/missing-schema.json'),('unknown-relative','missing.schema.json')]:
    changed=copy.deepcopy(docs)
    changed['counterexample.schema.json']={'$ref':ref}
    try:
        validate_schema_references(changed)
    except AssertionError as exc:
        controls.append({'name':name,'result':'REFUSE','reason':str(exc)})
    else:
        raise AssertionError('Missing dependency admitted: '+name)
changed=copy.deepcopy(docs)
changed['counterexample.schema.json']={'$id':'urn:opensip:design:journal-record:1','type':'null'}
try:
    validate_schema_references(changed)
except AssertionError as exc:
    controls.append({'name':'conflicting-schema-id','result':'REFUSE','reason':str(exc)})
else:
    raise AssertionError('Conflicting schema ID admitted')
result={'standing':'Prospective kit custody tool controls only; no product/schema/consumer acceptance. Original103-file kit unchanged.','actualKit':positive,'negativeControls':controls,'passed':len(controls)==4}
Path(__file__).with_name('kit-ref-controls.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
