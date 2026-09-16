import json
import sys

SUB = '/tmp/opensip-design-corrections/consumer-b.v19/subject'
path = sys.argv[1]
name = sys.argv[2]
d = json.load(open(SUB + '/' + path))
node = d['$defs'][name]
for k in ('allOf', 'anyOf', 'oneOf', 'if', 'then', 'not', 'dependentRequired'):
    if k in node:
        print('==', k)
        print(json.dumps(node[k], indent=1)[:6000])
