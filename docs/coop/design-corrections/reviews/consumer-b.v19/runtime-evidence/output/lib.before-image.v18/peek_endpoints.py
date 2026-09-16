import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_schema as S
import opensip_build as B

r = json.load(open(S.KIT + '/' + S.doc_path(B.RELATION_DOC)))['x-opensip-relation-registry']
print('registry keys:', list(r))
for rel in ('imports', 'declares', 'clones', 'calls', 'references', 'file'):
    row = r['relations'][rel]
    print('==', rel, {k: v for k, v in row.items()
                      if k in ('ladder', 'subjectKindLaw', 'subjectKind', 'endpoints',
                               'sourceField', 'targetField', 'universeRule',
                               'occupancy', 'anchorLaw')})
print()
print('incoming search:', json.dumps(r.get('incomingSearch'), indent=1)[:600])
