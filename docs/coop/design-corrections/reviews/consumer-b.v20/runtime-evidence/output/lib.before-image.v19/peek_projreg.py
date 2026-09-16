import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_schema as S

d = json.load(open(S.KIT + '/' + S.doc_path(
    'docs/coop/design-corrections/foundation/evaluator-projection-registry.v1.json')))
print('keys:', list(d))
reg = d.get('relations') or d
for rel in ('imports', 'declares', 'clones', 'file', 'calls'):
    print('==', rel, json.dumps(reg.get(rel), indent=1)[:700])
print('capabilityForRelation:', json.dumps(d.get('capabilityForRelation'))[:400])
