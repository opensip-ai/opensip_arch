import json

SUB = '/tmp/opensip-design-corrections/consumer-b.v17/subject'
P = SUB + '/docs/coop/design-corrections/workflows/schemas/command-envelope.schema.json'
d = json.load(open(P))
print('=== allOf')
print(json.dumps(d['allOf'], indent=1)[:5000])
print('=== MutationReceiptProjection')
print(json.dumps(d['$defs']['MutationReceiptProjection'], indent=1)[:1500])
