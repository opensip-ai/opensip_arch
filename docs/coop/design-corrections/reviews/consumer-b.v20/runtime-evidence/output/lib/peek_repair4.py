import json

W = ('/tmp/opensip-design-corrections/consumer-b.v20/subject/docs/coop/design-corrections/'
     'workflows/schemas/evaluator3/repair.schema.json')
d = json.load(open(W))
m = d['x-opensip-mutation-operation-map']
for k in m:
    if k in ('standing', 'theConflationThisReplaces', 'emissionRule',
             'byCommandGenericMutationStep'):
        continue
    print('==', k)
    print(json.dumps(m[k], indent=1)[:3000])
