import json

p = ('/tmp/opensip-design-corrections/consumer-b.v23/subject/docs/coop/design-corrections/'
     'workflows/schemas/evaluator3/common.schema.json')
d = json.load(open(p))
e = d['$defs']['DomainDetailCode']['enum']
for pref in ('CONFIG', 'HOST', 'PROVIDER', 'native', 'evidence', 'REQUEST', 'IMPORT',
             'PURGE', 'OUTPUT', 'DELIVERY'):
    print(pref, [x for x in e if x.startswith(pref)][:14])
print()
print('lowercase codes:', [x for x in e if x[:1].islower()][:40])
print()
print('reasonCodes:', d['$defs']['D9ReasonCode']['enum'])
print('faultCause:', d['$defs']['D9FaultCause']['enum'])
