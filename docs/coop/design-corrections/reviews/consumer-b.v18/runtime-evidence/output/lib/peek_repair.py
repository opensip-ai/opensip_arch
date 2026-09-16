import json
import os
import sys

SUB = '/tmp/opensip-design-corrections/consumer-b.v18/subject'
W = SUB + '/docs/coop/design-corrections/workflows/schemas'
for p in ('repair.schema.json', 'evaluator3/repair.schema.json'):
    try:
        d = json.load(open(W + '/' + p))
    except Exception as e:
        print('==', p, 'ERR', e)
        continue
    print('==', p)
    print(' defs:', list(d.get('$defs', {})))
    print(' x-keys:', [k for k in d if k.startswith('x-')])
    print(' top:', {k: (v if isinstance(v, str) else type(v).__name__)
                    for k, v in d.items() if not k.startswith('$') and k != 'properties'})
