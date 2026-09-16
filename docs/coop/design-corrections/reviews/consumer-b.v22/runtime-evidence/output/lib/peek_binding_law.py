import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_schema as S

d = json.load(open(S.KIT + '/' + S.doc_path(
    'docs/coop/design-corrections/foundation/enumeration-plan.schema.v1.json')))
for n in ('AvailableProgramBindingV1', 'UnavailableProgramBindingV1', 'EnumeratorRef',
          'SelectedEnumeratorRef', 'UnselectedEnumeratorRef', 'CellObligationV1'):
    dd = d['$defs'].get(n)
    if dd is None:
        print('==', n, 'ABSENT')
        continue
    print('==', n)
    print('required:', dd.get('required'))
    print('additionalProperties:', dd.get('additionalProperties'))
    for k, v in (dd.get('properties') or {}).items():
        desc = v.get('description')
        print('  -', k, json.dumps({x: y for x, y in v.items() if x != 'description'})[:140])
        if desc:
            print('      DESC:', desc[:900])
    for k in ('allOf', 'oneOf', 'anyOf', 'if', 'then', 'not'):
        if k in dd:
            print('  ', k, json.dumps(dd[k])[:700])
