import json
B='/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/'
v4={e['path']:e for e in json.load(open(B+'candidate-subject.v4.json'))['files']}
v5={e['path']:e for e in json.load(open(B+'candidate-subject.v5.json'))['files']}
add=sorted(set(v5)-set(v4)); rem=sorted(set(v4)-set(v5))
mod=sorted(p for p in set(v4)&set(v5) if v4[p]['sha256']!=v5[p]['sha256'])
print('v4 files',len(v4),'v5 files',len(v5))
print('ADDED',len(add));[print('  +',p,v5[p]['bytes']) for p in add]
print('REMOVED',len(rem));[print('  -',p) for p in rem]
print('MODIFIED',len(mod));[print('  M',p,v4[p]['bytes'],'->',v5[p]['bytes']) for p in mod]
print('UNCHANGED',len(set(v4)&set(v5))-len(mod))
json.dump({'added':add,'removed':rem,'modified':mod},open('/tmp/opensip-design-corrections/post-reset-review.v5/probes/delta.json','w'),indent=1)
