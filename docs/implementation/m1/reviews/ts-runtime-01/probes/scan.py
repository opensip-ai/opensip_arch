import json, collections, re
root='/Users/sb/code/opensip-ai/opensip_arch/'
pins=json.load(open(root+'docs/implementation/m1/metadata-v2/sources.json'))['schemas']
docs={}
for p in pins:
    d=json.load(open(root+p['path'])); docs[d['$id']]=d
print('docs',len(docs), [k for k in docs if not k.startswith('urn:')])
kw=collections.Counter(); types=collections.Counter(); nested_ids=[]; refs=collections.Counter(); orders=[]; patterns=set(); bad=[]
MAPS={'$defs','definitions','properties','patternProperties'}; SING={'additionalProperties','propertyNames','items','not','if','then','else','contains'}; ARR={'allOf','anyOf','oneOf'}
def visit(s,path,top):
    if isinstance(s,bool): return
    if not isinstance(s,dict): bad.append(('node',path)); return
    for k,v in s.items():
        kw[k]+=1
        if k=='$id' and not top: nested_ids.append((path,v))
        if k=='$ref': refs[v]+=1
        if k=='type':
            for t in (v if isinstance(v,list) else [v]): types[t]+=1
        if k=='x-opensip-order': orders.append((path,v,s.get('items')))
        if k=='pattern': patterns.add(v)
        if k=='patternProperties': patterns.update(v)
        if k in ('minimum','maximum','minLength','maxLength','minItems','maxItems','minProperties','maxProperties') and type(v) is not int: bad.append((k,path,v))
        if k in ('enum','required','allOf','anyOf','oneOf') and type(v) is not list: bad.append((k,path,v))
        if k=='required' and any(type(x) is not str for x in v): bad.append((k,path))
        if k=='uniqueItems' and type(v) is not bool: bad.append((k,path))
        if k in ('pattern','$ref') and type(v) is not str: bad.append((k,path))
        if k in MAPS:
            for kk,vv in v.items(): visit(vv,path+'/'+k+'/'+kk,False)
        elif k in SING: visit(v,path+'/'+k,False)
        elif k in ARR:
            for i,vv in enumerate(v): visit(vv,path+'/'+k+'/'+str(i),False)
for i,d in docs.items(): visit(d,i+'#',True)
print('keywords',sorted(kw.items()))
print('types',types); print('nestedIds',nested_ids[:5],len(nested_ids)); print('bad',bad[:10])
print('refs with %:',[r for r in refs if '%' in r], 'relative non-exact:',sorted({r.split('#')[0] for r in refs if r.split('#')[0] and r.split('#')[0] not in docs}))
print('ref to arrays:',[r for r in refs if re.search(r'/(allOf|anyOf|oneOf|items)/\d',r)][:5])
print('orders',len(orders)); 
oc=collections.Counter(json.dumps(o[1]) for o in orders); print(oc)
print('patterns',len(patterns))
json.dump(sorted(patterns),open('/tmp/opensip-implementation/m1-ts-runtime-review-01/work/probes/patterns.json','w'),indent=1)
json.dump([[p,o,it] for p,o,it in orders],open('/tmp/opensip-implementation/m1-ts-runtime-review-01/work/probes/orders.json','w'),indent=1)
