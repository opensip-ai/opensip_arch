import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_schema as S
import opensip_build as B

d = json.load(open(S.KIT + '/' + S.doc_path(B.NATIVE_DOC)))
u = d['$defs']['TypeScriptUniverseV2ResolvedInputs']['properties']
print(json.dumps(u['synthesizedOptions'], indent=1)[:1500])
print('--- synthesizerVersion')
print(json.dumps(u['synthesizerVersion'], indent=1)[:400])
