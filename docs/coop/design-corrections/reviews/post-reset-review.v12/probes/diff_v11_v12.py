import json,hashlib,os
B='/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/'
m11=json.load(open(B+'candidate-subject.v11.json'))
m12=json.load(open(B+'candidate-subject.v12.json'))
r11,r12=m11['snapshotRoot'],m12['snapshotRoot']
d11={e['path']:e for e in m11['files']}
d12={e['path']:e for e in m12['files']}
# verify v11 snapshot integrity too
bad11=0
for p,e in d11.items():
    fp=os.path.join(r11,p)
    if not os.path.exists(fp): bad11+=1; continue
    if hashlib.sha256(open(fp,'rb').read()).hexdigest()!=e['sha256']: bad11+=1
print('v11 files',len(d11),'v11 mismatches',bad11)
added=sorted(set(d12)-set(d11)); removed=sorted(set(d11)-set(d12))
changed=sorted(p for p in set(d11)&set(d12) if d11[p]['sha256']!=d12[p]['sha256'])
print('ADDED',len(added),'REMOVED',len(removed),'CHANGED',len(changed))
print('--- CHANGED ---')
for p in changed: print(' C %+d bytes  %s'%(d12[p]['bytes']-d11[p]['bytes'],p))
print('--- REMOVED ---')
for p in removed: print(' R',p)
print('--- ADDED (top dirs) ---')
from collections import Counter
c=Counter(os.path.dirname(p) for p in added)
for k,v in sorted(c.items()): print('  %4d %s'%(v,k))
json.dump({'added':added,'removed':removed,'changed':changed},open('/tmp/opensip-design-corrections/post-reset-review.v12/probes/delta.json','w'),indent=1)
