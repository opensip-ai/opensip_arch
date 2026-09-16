import json, hashlib
from pathlib import Path
from jsonschema import Draft202012Validator
from referencing import Registry, Resource
A=Path('/Users/sb/code/opensip-ai/opensip_arch')
paths=[A/'docs/coop/design-corrections/workflows/schemas/evaluator3/graph-query.schema.json',A/'docs/coop/design-corrections/workflows/schemas/evaluator3/common.schema.json',A/'docs/coop/design-corrections/workflows/query-projection-contract.v3.md']
pins=[{'path':str(p),'bytes':len(p.read_bytes()),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths]
query,common=[json.loads(p.read_bytes()) for p in paths[:2]]
registry=Registry().with_resources([(d['$id'],Resource.from_contents(d)) for d in [query,common]])
v=Draft202012Validator({'$ref':query['$id']+'#/$defs/GraphQueryResponseV1'},registry=registry)
print(common['$defs']['ProjectId'])
base={'schemaFamily':'opensip.product.query','schemaMajor':3,'operation':'run.show','context':{'projectId':'prj1-'+'2'*64,'resolvedView':{'runId':'run3:'+'1'*64},'coverage':'complete','availability':'retained','truncated':False,'totalItems':1,'advisory':False},'items':[{'unowned':'arbitrary run.show item'}]}
errors=[e.message for e in v.iter_errors(base)]
result={'schemaVersion':1,'pins':pins,'candidate':base,'shapeErrors':errors,'acceptedArbitraryRunShowItem':not errors,'scope':'Schema shape only, no execution or close_run admission. Query v3 section1 states graph selection law; section opening preserves non-graph owners. No typed run.show item appears in this selected schema. This refines HIS-F5 remediation: author explicit owned typed selection/result law rather than claim an existing typed adapter was invoked.'}
Path(__file__).with_name('result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
