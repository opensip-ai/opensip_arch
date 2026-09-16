import json

SUB = '/tmp/opensip-design-corrections/consumer-b.v17/subject'
W = SUB + '/docs/coop/design-corrections/workflows/schemas/evaluator3/repair.schema.json'
d = json.load(open(W))
print(json.dumps(d['x-opensip-evaluator3-repair-target-law'], indent=1)[:2500])
print('=== RepairPlanDescriptor')
print(json.dumps(d['$defs']['RepairPlanDescriptor'], indent=1)[:3000])
