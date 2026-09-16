import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_schema as S
import opensip_build as B

d = json.load(open(S.KIT + '/' + S.doc_path(B.EXEC_IN_DOC)))
for n in ('NativeCoverageAccountV1', 'CellProgramOutcomeV1', 'StageReceiptV1'):
    dd = d['$defs'][n]
    print('==', n, 'required:', dd.get('required'))
    for k, v in (dd.get('properties') or {}).items():
        print('  -', k, json.dumps({x: y for x, y in v.items()
                                    if x != 'description'})[:200])
        if v.get('description'):
            print('      DESC:', v['description'][:600])
    for key in ('allOf', 'oneOf', 'if', 'then'):
        if key in dd:
            print('   ', key, json.dumps(dd[key], indent=1)[:2200])
