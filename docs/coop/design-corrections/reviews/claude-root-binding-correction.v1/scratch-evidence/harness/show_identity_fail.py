import json
S='/private/tmp/opensip-design-corrections/claude-root-binding-correction.v1/scratch/output/evidence/suites/'
b=json.load(open(S+'reference-src25.json'))
for c in b['checks']:
    if c['script']=='check-identity.py':
        print('exitCode',c['exitCode'])
        print(c['stderr'][-3000:])
