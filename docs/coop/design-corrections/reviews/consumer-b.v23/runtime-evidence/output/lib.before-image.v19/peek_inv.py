import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_schema as S

d = json.load(open(S.KIT + '/' + S.doc_path(
    'workflows/schemas/evaluator3/invocation-record.schema.json')))
print('defs:', sorted(d.get('$defs', {})))
print('x-keys:', [k for k in d if k.startswith('x-')])
print('top required:', d.get('required'))
print('top props:', sorted((d.get('properties') or {})))
