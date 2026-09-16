import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_schema as S
import opensip_build as B

d = json.load(open(S.KIT + '/' + S.doc_path(B.EXEC_IN_DOC)))
print('x-keys:', [k for k in d if k.startswith('x-')])
for k in d:
    if k.startswith('x-'):
        print('==', k)
        print(json.dumps(d[k], indent=1)[:4000])
print('== root required:', d.get('required'))
print('== defs:', sorted(d.get('$defs', {})))
