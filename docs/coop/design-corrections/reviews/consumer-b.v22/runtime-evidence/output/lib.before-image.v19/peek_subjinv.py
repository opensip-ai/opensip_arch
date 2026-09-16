import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_schema as S
import opensip_build as B

d = json.load(open(S.KIT + '/' + S.doc_path(B.SUBJ_INV_DOC)))
print('x-keys:', [k for k in d if k.startswith('x-')])
for k in d:
    if k.startswith('x-'):
        print('==', k)
        print(json.dumps(d[k], indent=1)[:3000])
print('== root required:', d.get('required'))
for k, v in (d.get('properties') or {}).items():
    print('  -', k, json.dumps({x: y for x, y in v.items() if x != 'description'})[:180])
    if v.get('description'):
        print('      DESC:', v['description'][:700])
for k in ('allOf', 'oneOf', 'anyOf', 'if', 'then'):
    if k in d:
        print('==', k)
        print(json.dumps(d[k], indent=1)[:3000])
