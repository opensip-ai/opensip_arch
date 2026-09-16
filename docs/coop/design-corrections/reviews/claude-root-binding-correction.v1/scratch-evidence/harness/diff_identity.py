import json
S='/private/tmp/opensip-design-corrections/claude-root-binding-correction.v1/scratch'
def load(t):
    return json.load(open(S+'/'+t+'/docs/coop/design-corrections/foundation/identity-report.json'))
a=load('baseline25'); b=load('src25')
print('keys',list(a.keys())[:12])
def rows(d):
    out={}
    for k,v in d.items():
        if isinstance(v,dict):
            for kk,vv in v.items(): out[k+'.'+kk]=vv
        elif isinstance(v,list) and v and isinstance(v[0],dict):
            for r in v:
                nm=r.get('check') or r.get('name')
                if nm is not None: out[nm]=r.get('passed',r)
    return out
ra,rb=rows(a),rows(b)
diff=[k for k in sorted(set(ra)|set(rb)) if ra.get(k)!=rb.get(k)]
print('differing entries:',len(diff))
for k in diff[:40]:
    print('  ',k)
    print('     baseline:',json.dumps(ra.get(k))[:220])
    print('     src25   :',json.dumps(rb.get(k))[:220])
