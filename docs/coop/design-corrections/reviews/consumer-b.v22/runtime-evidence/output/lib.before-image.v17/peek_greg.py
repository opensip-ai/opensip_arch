import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_schema as S
import opensip_build as B

g = json.load(open(S.KIT + '/' + S.doc_path(B.NATIVE_DOC)))[
    'x-opensip-grammar-capability-registry']
print(list(g))
print(json.dumps(g, indent=1)[:3000])
