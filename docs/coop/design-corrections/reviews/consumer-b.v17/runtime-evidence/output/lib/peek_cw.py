import json

W = ('/tmp/opensip-design-corrections/consumer-b.v17/subject/docs/coop/design-corrections/'
     'workflows/schemas/evaluator3/repair.schema.json')
d = json.load(open(W))
p = d['$defs']['RepairPlanDescriptor']['properties']
print(p['closedWorld']['description'])
print('\n=== evidenceRequirements')
print(json.dumps(p['evidenceRequirements'].get('description'), indent=1))
print('\n=== permittedEditScope')
print(json.dumps(p['permittedEditScope'].get('description'), indent=1))
print('\n=== applicable / unmetPreconditions / limitations / targets / edits')
for k in ('applicable', 'unmetPreconditions', 'limitations', 'targets', 'edits',
          'totalPostimageBytes', 'recipeTrust'):
    print('--', k, json.dumps(p[k].get('description'))[:700])
print('\n=== EvidenceRequirement full')
print(json.dumps(d['$defs']['EvidenceRequirement'], indent=1)[:2000])
