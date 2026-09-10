import json
from pathlib import Path
d=json.loads(Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/foundation/identity-schemas.v2.json').read_text())
HEX='^[0-9a-f]{64}(?![\\s\\S])'
missing=[];present=[]
def ishex(n):return isinstance(n,dict) and (n.get('pattern')==HEX or n.get('$ref')=='#/$defs/Hash')
def walk(n,path):
    if isinstance(n,dict):
        if ishex(n):
            (present if 'x-opensip-digest' in n else missing).append(path)
            return
        for k,v in n.items():
            walk(v,path if k in ('properties','items','$defs','oneOf','anyOf','additionalProperties') else path+'/'+k)
    elif isinstance(n,list):
        for v in n: walk(v,path)
for k,v in d['$defs'].items():
    if k=='Hash':continue
    walk(v,k)
print('annotated',len(present));print('MISSING',missing)
reps={}
def collect(n):
    if isinstance(n,dict):
        a=n.get('x-opensip-digest')
        if a:reps[a['representation']]=reps.get(a['representation'],0)+1
        for v in n.values():collect(v)
    elif isinstance(n,list):
        for v in n:collect(v)
collect(d['$defs'])
print('representations',reps)
