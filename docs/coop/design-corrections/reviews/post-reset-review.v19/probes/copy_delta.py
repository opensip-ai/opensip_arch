import json,hashlib,os
A='/tmp/opensip-design-corrections/candidate-subject.v19'
B='/tmp/opensip-design-corrections/post-reset-review.v19/copies/repro-v19'
def sh(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()
def scan(root):
    m={}
    for dp,dn,fn in os.walk(root):
        for n in fn:
            p=os.path.join(dp,n); m[os.path.relpath(p,root)]=p
    return m
a,b=scan(A),scan(B)
changed=[];added=sorted(set(b)-set(a));removed=sorted(set(a)-set(b))
for k in sorted(set(a)&set(b)):
    ha,hb=sh(a[k]),sh(b[k])
    if ha!=hb: changed.append({'path':k,'frozenSha':ha,'copySha':hb,'frozenBytes':os.path.getsize(a[k]),'copyBytes':os.path.getsize(b[k])})
out={'changedCount':len(changed),'changed':changed,'added':added,'removed':removed}
json.dump(out,open('/tmp/opensip-design-corrections/post-reset-review.v19/results/copy-delta.json','w'),indent=1)
print(json.dumps(out,indent=1)[:4000])
