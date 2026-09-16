import json

W = ('/tmp/opensip-design-corrections/consumer-b.v17/subject/docs/coop/design-corrections/'
     'workflows/schemas/evaluator3/repair.schema.json')
d = json.load(open(W))
s = json.dumps(d, indent=1)
# the idempotency-key-per-step-kind law
for k, v in d.items():
    if k.startswith('x-'):
        print('==', k)
        print(json.dumps(v, indent=1)[:4000])
