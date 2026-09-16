import json
root='/Users/sb/code/opensip-ai/opensip_arch/'
targets={"^.+$","(^|/)\\.\\.?(/|$)","^(?!/)(?!.*(^|/)\\.\\.?(/|$))[^\\u0000\\\\]*(?![\\s\\S])","^(?!/)(?!.*(^|/)\\.\\.?(/|$))[^\\u0000\\\\]+(?![\\s\\S])"}
def esc(k): return k.replace('~','~0').replace('/','~1')
for p in json.load(open(root+'docs/implementation/m1/metadata-v2/sources.json'))['schemas']:
    d=json.load(open(root+p['path']))
    def walk(v,ptr):
        if isinstance(v,dict):
            if isinstance(v.get('pattern'),str) and v['pattern'] in targets: print(d['$id']+'#'+ptr, repr(v['pattern']))
            for k,x in v.items(): walk(x,ptr+'/'+esc(k))
        elif isinstance(v,list):
            for i,x in enumerate(v): walk(x,ptr+'/'+str(i))
    walk(d,'')
