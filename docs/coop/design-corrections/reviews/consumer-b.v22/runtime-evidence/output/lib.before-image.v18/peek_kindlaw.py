import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_schema as S

d = json.load(open(S.KIT + '/' + S.doc_path(
    'docs/coop/design-corrections/foundation/evaluator-projection-registry.v1.json')))
print('== kindApplicability')
print(json.dumps(d['kindApplicability'], indent=1))
print()
for rel, row in sorted(d['relations'].items()):
    print('%-18s src=%-28s tgt=%-28s endpointTarget=%-18s rungs=%s'
          % (rel,
             row.get('sourceSubjectKinds') or row.get('sourceSubjectKind'),
             row.get('targetKinds'),
             row.get('endpointTarget'),
             row.get('endpointTargetRungs')))
print()
print('== filters shape, per relation')
for rel, row in sorted(d['relations'].items()):
    f = row.get('filters') or {}
    print('--', rel)
    for k, v in f.items():
        print('     %-22s %s' % (k, json.dumps(v)[:150]))
