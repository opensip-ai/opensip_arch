import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_schema as S
import opensip_build as B

for doc in (B.NATIVE_DOC, B.IDENTITY_DOC):
    d = json.load(open(S.KIT + '/' + S.doc_path(doc)))
    law = d.get('x-opensip-digest-law') or {}
    print('==', S.doc_path(doc), 'keys:', list(law))
    print(json.dumps({k: v for k, v in law.items()
                      if k in ('siteCountLaw', 'sites')}, indent=1)[:1800])
