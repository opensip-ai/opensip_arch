import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_schema as S

d = json.load(open(S.KIT + '/' + S.doc_path(
    'docs/coop/design-corrections/foundation/evaluator-projection-registry.v1.json')))
print(json.dumps(d['relations']['imports'], indent=1)[:2500])
print('=== kindApplicability')
print(json.dumps(d.get('kindApplicability'), indent=1)[:1200])
