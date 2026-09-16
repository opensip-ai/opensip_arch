import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_schema as S
import opensip_build as B

pairs = [
    ('foundation identity-schemas.v3', B.IDENTITY_DOC, ('ProjectId', 'RequestId')),
    ('workflows evaluator3 common', 'workflows/schemas/evaluator3/common.schema.json',
     ('ProjectId', 'RequestId', 'RunId')),
    ('workflows major-1 common', 'workflows/schemas/common.schema.json',
     ('ProjectId', 'RequestId', 'RunId')),
]
for label, doc, names in pairs:
    d = json.load(open(S.KIT + '/' + S.doc_path(doc)))
    print('==', label)
    for n in names:
        v = (d.get('$defs') or {}).get(n)
        print('  %-10s %s' % (n, json.dumps(v)[:220] if v else 'ABSENT'))
