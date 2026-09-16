import json

SUB = '/tmp/opensip-design-corrections/consumer-b.v22/subject'
W = SUB + '/docs/coop/design-corrections/workflows/schemas'
d = json.load(open(W + '/imported-evidence.schema.json'))
print('x-keys:', [k for k in d if k.startswith('x-')])
law = d.get('x-opensip-imported-requirement-law')
print(json.dumps(law, indent=1)[:3000])
c = json.load(open(W + '/evaluator3/common.schema.json'))
for n in ('NativeSufficiencyDeficiency', 'ImportedRequirementDeficiency', 'Fingerprint',
          'RepairPlanId', 'GlobPattern'):
    print('--', n, json.dumps(c['$defs'].get(n))[:400])
