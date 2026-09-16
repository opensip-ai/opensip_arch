import json,copy,importlib.util,sys,collections,hashlib
from pathlib import Path
S=Path(sys.argv[1]); out=Path(sys.argv[2])
spec=importlib.util.spec_from_file_location('prep',S/'tools/contracts/prepare.py');P=importlib.util.module_from_spec(spec);spec.loader.exec_module(P)
docs={}
for p in sorted((S/'schemas/sources').glob('*.json')):
    d=json.loads(p.read_text()); docs[d['$id']]=d
opts=json.loads((S/'tools/contracts/options.json').read_text())
flat=P.flatten(docs,opts)
base=P.schema_map(copy.deepcopy(flat),P.rust)
named=P.name_variant_objects(copy.deepcopy(base))
changed=[n for n in base['definitions'] if base['definitions'][n]!=named['definitions'][n]]
print('definitions',len(base['definitions']),'changed by transform',changed)
# every inserted title, and whether it coincides with any definition name or pre-existing title
def titles(o,acc,path=''):
    if isinstance(o,dict):
        if isinstance(o.get('title'),str): acc.append((o['title'],path))
        for k,v in o.items(): titles(v,acc,path+'/'+k)
    elif isinstance(o,list):
        for i,v in enumerate(o): titles(v,acc,path+'/'+str(i))
tb=[];titles(base,tb);tn=[];titles(named,tn)
new=[t for t in tn if t not in tb]
print('new titles',len(new),'unique',len({t for t,_ in new}))
defs=set(base['definitions']); old={t for t,_ in tb}
print('collide with definition names',[t for t,_ in new if t in defs],'with existing titles',[t for t,_ in new if t in old])
print('prefix-collide with definitions',[d for d in defs for t,_ in new if d!=t and (d.startswith(t) or t.startswith(d)) and d!='Control3Root'][:10])
# residual Typify collision class: sibling union branches (oneOf/anyOf) anywhere, same property key, differing untitled non-trivial schemas
def needs_name(c):
    if not isinstance(c,dict) or '$ref' in c: return False
    return c.get('type')=='object' or 'enum' in c or any(k in c for k in ('oneOf','anyOf','allOf')) or c.get('type')=='array' or (c.get('type')=='string' and any(k in c for k in ('minLength','maxLength','const')))
res=[]
def walk(o,path,root):
    if isinstance(o,dict):
        for comb in ('oneOf','anyOf'):
            if isinstance(o.get(comb),list):
                g=collections.defaultdict(list)
                for i,b in enumerate(o[comb]):
                    if isinstance(b,dict):
                        for k,c in b.get('properties',{}).items():
                            if needs_name(c): g[k].append((i,c))
                for k,es in g.items():
                    shapes={json.dumps(c,sort_keys=True) for _,c in es}
                    ttl=[c.get('title') for _,c in es]
                    if len(shapes)>1 and len(set(ttl))<len(ttl):
                        res.append({'root':root,'path':path+'/'+comb,'key':k,'branches':[i for i,_ in es],'kinds':sorted({c.get('type') or ','.join(x for x in ('enum','oneOf','anyOf','allOf') if x in c) for _,c in es})})
        for k,v in o.items(): walk(v,path+'/'+k,root)
    elif isinstance(o,list):
        for i,v in enumerate(o): walk(v,path+'/'+str(i),root)
for label,proj in (('base',base),('named',named)):
    res=[]
    for n,d in proj['definitions'].items(): walk(d,'#/definitions/'+n,n)
    print(label,'residual same-key differing untitled union properties:',len(res))
    for r in res[:40]: print('  ',r)
out.write_text(json.dumps({'changed':changed,'newTitles':new},indent=1))
