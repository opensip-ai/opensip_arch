import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_schema as S

d = json.load(open(S.KIT + '/' + S.doc_path(
    'docs/coop/design-corrections/foundation/enumeration-plan.schema.v1.json')))
print('x-keys:', [k for k in d if k.startswith('x-')])
for k in d:
    if k.startswith('x-'):
        print('==', k)
        print(json.dumps(d[k], indent=1)[:2500])
print('== defs:', sorted(d.get('$defs', {})))
for n in ('KindExtentV1', 'ProgramBindingV1', 'CellV1', 'EnumerationPlanV1'):
    if n in d.get('$defs', {}):
        print('==', n)
        print(json.dumps(d['$defs'][n], indent=1)[:1800])
