import json,importlib.util
from pathlib import Path
root=Path('/Users/sb/code/opensip-ai/opensip_arch')
spec=importlib.util.spec_from_file_location('meta',root/'docs/implementation/m1/metadata-v2/check_metadata.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
ref,registry,docs=m.load(root)
def esc(k): return k.replace('~','~0').replace('/','~1')
nodes=[]
def walk(v,ptr,did):
    if isinstance(v,dict):
        if 'x-opensip-order' in v and v['x-opensip-order']!='sequence': nodes.append((did+'#'+ptr,v['x-opensip-order']))
        for k,x in v.items():
            if k in ('const','enum','default'): continue
            walk(x,ptr+'/'+esc(k),did)
    elif isinstance(v,list):
        for i,x in enumerate(v): walk(x,ptr+'/'+str(i),did)
for i,d in docs.items(): walk(d,'',i)
def vals(o):
    fs=o['by'] if isinstance(o,dict) else {'predicate':['ruleId','subjectId','predicateId']}.get(o,[o])
    mk=lambda *xs:[{f:x for f in fs} for x in xs]
    return [[],[1,0],[0,1],['b','a'],['a','b'],[{},{}],[{}],[[],[]],[None,None],[True,False],['a',1],
            mk('a','b'),mk('b','a'),mk('a','a'),mk(0,1),mk(1,0),mk(['a'],['b']),mk(None,None),mk('a',1),mk(True,False)]
cases=[]
for ptr,o in nodes:
    v=ref.ExactValidator({'$ref':ptr},registry=registry)
    for i,x in enumerate(vals(o)):
        try: r=v.is_valid(x)
        except Exception as e: r='PYTHROW '+type(e).__name__
        cases.append(dict(ref=ptr,order=o,value=x,valid=r))
Path('order-cases.json').write_text(json.dumps(cases))
print(len(nodes),'nodes',len(cases),'cases')
