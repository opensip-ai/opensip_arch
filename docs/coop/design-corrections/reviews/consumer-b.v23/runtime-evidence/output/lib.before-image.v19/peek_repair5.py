import json

W = ('/tmp/opensip-design-corrections/consumer-b.v19/subject/docs/coop/design-corrections/'
     'workflows/schemas/evaluator3/repair.schema.json')
d = json.load(open(W))
m = d['x-opensip-mutation-operation-map']
print('keys:', list(m))
print(json.dumps(m.get('receiptIdempotencyKeyByStepKind'), indent=1)[:4000])
