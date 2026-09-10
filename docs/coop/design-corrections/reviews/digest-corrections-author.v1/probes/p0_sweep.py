import json,sys
from pathlib import Path
S=Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/foundation/identity-schemas.v2.json')
d=json.loads(S.read_text())
HEX='^[0-9a-f]{64}(?![\\s\\S])'
rows=[]
def is_hex(node):
    return isinstance(node,dict) and (node.get('pattern')==HEX or node.get('$ref')=='#/$defs/Hash')
def walk(node,path):
    if isinstance(node,dict):
        if is_hex(node):
            rows.append((path,'$ref' if node.get('$ref') else 'inline',sorted(k for k in node if k not in('type','pattern','$ref'))))
            return
        for k,v in node.items():
            walk(v,path+'/'+k if k not in('properties','items','$defs','oneOf','anyOf') else path)
    elif isinstance(node,list):
        for i,v in enumerate(node):walk(v,path)
for name,node in d['$defs'].items():
    walk(node,name)
for r in sorted(set((a,b,tuple(c)) for a,b,c in rows)):print(r[0],'|',r[1],'|',list(r[2]))
print('total distinct paths',len(set(r[0] for r in rows)))
