import json

p = ('/tmp/opensip-design-corrections/consumer-b.v17/subject/docs/coop/design-corrections/'
     'foundation/target-attribution.schema.v2.json')
d = json.load(open(p))
for k, v in d['properties'].items():
    print('--', k, json.dumps(v)[:400])
print()
print('description tail:', str(d.get('description'))[900:2400])
