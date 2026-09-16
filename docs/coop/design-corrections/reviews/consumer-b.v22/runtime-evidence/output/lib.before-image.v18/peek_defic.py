import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_schema as S
import opensip_build as B

d = json.load(open(S.KIT + '/' + S.doc_path(B.SUBJ_INV_DOC)))
for n in ('EnumerationDeficiencyV1', 'NativeCause', 'DeficiencyV2', 'InventoryRowV1'):
    dd = d['$defs'].get(n)
    print('==', n)
    print(json.dumps(dd, indent=1)[:1800] if dd else 'ABSENT')
nat = json.load(open(S.KIT + '/' + S.doc_path(B.NATIVE_DOC)))
reg = nat.get('x-opensip-deficiency-cause-registry')
print('== native x-opensip-deficiency-cause-registry keys:', list(reg))
print(json.dumps({k: v for k, v in reg.items() if k != 'deficiencies'}, indent=1)[:1500])
for k, v in sorted(reg['deficiencies'].items()):
    print('  %-28s %s' % (k, json.dumps(v)[:190]))
