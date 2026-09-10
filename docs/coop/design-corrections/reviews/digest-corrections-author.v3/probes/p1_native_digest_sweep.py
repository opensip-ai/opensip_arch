"""Enumerate every 64-hex field in the native bundle and report annotation coverage."""
import json,sys
from pathlib import Path
P=Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/native/native-evidence.schemas.v2.json')
d=json.loads(P.read_text())
HEX='^[0-9a-f]{64}(?![\\s\\S])';TEXT='^sha256:[0-9a-f]{64}(?![\\s\\S])'
rows=[]
def hexish(n):
    if not isinstance(n,dict):return None
    if n.get('pattern')==HEX or n.get('$ref')=='#/$defs/DigestHex':return 'bare-hex'
    if n.get('pattern')==TEXT or n.get('$ref')=='#/$defs/Sha256Text':return 'sha256-text'
    return None
def walk(n,path):
    if isinstance(n,dict):
        kind=hexish(n)
        if kind:rows.append((path,kind,'x-opensip-digest' in n));return
        for k,v in n.items():walk(v,path if k in ('properties','items','$defs','oneOf','anyOf','additionalProperties') else path+'.'+k)
    elif isinstance(n,list):
        for v in n:walk(v,path)
for name,node in d['$defs'].items():
    if name in ('DigestHex','Sha256Text'):continue
    walk(node,name)
seen={}
for p,k,a in rows:seen.setdefault(p,(k,a))
print(json.dumps({'total':len(seen),'annotated':sum(1 for k,a in seen.values() if a),
 'unannotated':sorted(p for p,(k,a) in seen.items() if not a),
 'byForm':{'bare-hex':sum(1 for k,a in seen.values() if k=='bare-hex'),
           'sha256-text':sum(1 for k,a in seen.values() if k=='sha256-text')}},indent=1))
