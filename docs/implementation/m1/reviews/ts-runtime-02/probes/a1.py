import json,random,importlib.util
spec=importlib.util.spec_from_file_location('c','/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/foundation/canonical.py');c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
rng=random.Random(20260914)
orders=['utf8','numeric','canonical-set','canonical-order','path','ruleId','waiverId','predicate','ordinal','candidateOrdinal',{'by':['x']},{'by':['x','y']}]
fields=['x','y','path','ruleId','waiverId','subjectId','predicateId','ordinal','candidateOrdinal']
def scalar():
    return rng.choice([None,True,False,0,1,2,-1,2**64-1,-2**63,'','a','b','é','\U0001f600','￿','A',[],[0],['a'],{},{'a':1}])
def item(o):
    k=rng.random()
    if k<0.35: return scalar()
    d={}
    for f in fields:
        if rng.random()<0.6: d[f]=rng.choice([0,1,2,3,'a','b','c','',True,None,[1],'0'])
    return d
cases=[]
for o in orders:
    for _ in range(1500):
        n=rng.choice([0,1,2,2,3,4])
        base=rng.choice(['obj','str','int','mix'])
        arr=[]
        for i in range(n):
            if base=='str': arr.append(rng.choice(['a','b','c','é','\U0001f600','￿','A','']))
            elif base=='int': arr.append(rng.choice([0,1,2,3,-1,2**64-1]))
            elif base=='obj':
                d={f:rng.choice([i,rng.choice([0,1,2,3]),rng.choice(['a','b','c']),'0',True]) for f in fields if rng.random()<0.9}
                arr.append(d)
            else: arr.append(item(o))
        schema={'x-opensip-order':o}
        v=c.ExactValidator(schema).is_valid(arr)
        nv=c.ExactValidator({'not':schema}).is_valid(arr)
        cases.append(dict(order=o,value=arr,valid=v,notValid=nv))
open('a1-cases.json','w').write(json.dumps(cases))
print(len(cases),'cases',sum(x['valid'] for x in cases),'valid')
