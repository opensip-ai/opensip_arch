import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_schema as S
import opensip_build as B

reg = json.load(open(S.KIT + '/' + S.doc_path(B.NATIVE_DOC)))[
    'x-opensip-deficiency-cause-registry']
for k in ('nullIsNotAnEscape', 'noDeficiencyNoCause', 'multiCauseAndPrecedence',
          'selectedScalarCauseLimitation'):
    print('==', k)
    print(json.dumps(reg.get(k), indent=1)[:1400])
print('== full rows')
for k, v in sorted(reg['deficiencies'].items()):
    print('--', k)
    print(json.dumps(v, indent=1)[:700])
