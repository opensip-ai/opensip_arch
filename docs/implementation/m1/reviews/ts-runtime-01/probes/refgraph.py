import json,sys
root='/Users/sb/code/opensip-ai/opensip_arch/'
docs={}
for p in json.load(open(root+'docs/implementation/m1/metadata-v2/sources.json'))['schemas']:
    d=json.load(open(root+p['path'])); docs[d['$id']]=d
def get(ref,owner):
    i,_,f=ref.partition('#'); i=i or owner; v=docs[i]
    for s in f.split('/')[1:]: v=v[s.replace('~1','/').replace('~0','~')]
    return v,i,i+'#'+f
# edges: ref node -> refs reachable without consuming instance (allOf/anyOf/oneOf/not/if/then/else/$ref) vs consuming
NONCONS={'allOf','anyOf','oneOf','not','if','then','else'}
CONS_S={'additionalProperties','propertyNames','items','contains'}
def edges(s,owner,consuming,acc):
    if not isinstance(s,dict): return
    for k,v in s.items():
        if k=='$ref': acc.append((v,owner,consuming))
        elif k in ('properties','patternProperties'):
            for x in v.values(): edges(x,owner,True,acc)
        elif k in CONS_S: edges(v,owner,True,acc)
        elif k in ('not','if','then','else'): edges(v,owner,consuming,acc)
        elif k in ('allOf','anyOf','oneOf'):
            for x in v: edges(x,owner,consuming,acc)
refs=list(json.load(open('/tmp/opensip-implementation/m1-full-generator-trial-01/source-map.json'))['selectedTargets'])
graph={}; stack=[(r,'') for r in refs]
while stack:
    r,o=stack.pop(); v,i,key=get(r,o)
    if key in graph: continue
    acc=[]; edges(v,i,False,acc); graph[key]=[(get(t,oo)[2],c) for t,oo,c in acc]
    stack+= [(t,oo) for t,oo,c in acc]
print('closure nodes',len(graph))
# cycles through any edges
import itertools
sys.setrecursionlimit(10000)
color={};cyc=[];noncons=[]
def dfs(n,path,cons):
    color[n]=1
    for m,c in graph[n]:
        if color.get(m)==1:
            idx=[p for p,_ in path].index(m) if m in [p for p,_ in path] else 0
            cyc.append(m)
        elif m not in color: dfs(m,path+[(m,c)],cons)
    color[n]=2
for n in graph:
    if n not in color: dfs(n,[(n,False)],False)
print('back-edge targets (recursive schemas):',sorted(set(cyc))[:20])
