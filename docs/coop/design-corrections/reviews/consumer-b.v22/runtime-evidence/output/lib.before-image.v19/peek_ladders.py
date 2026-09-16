import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_schema as S
import opensip_build as B

r = json.load(open(S.KIT + '/' + S.doc_path(B.RELATION_DOC)))['x-opensip-relation-registry']
for k, v in sorted(r['relations'].items()):
    print('%-20s %s' % (k, v['ladder']))
print()
print(json.dumps(r.get('coveragePartitionLaw'), indent=1)[:800])
