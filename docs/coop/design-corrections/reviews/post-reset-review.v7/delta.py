import json,sys
R='/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/'
a=json.load(open(R+'candidate-subject.v6.json'));b=json.load(open(R+'candidate-subject.v7.json'))
A={e['path']:e for e in a['files']};B={e['path']:e for e in b['files']}
added=sorted(set(B)-set(A));removed=sorted(set(A)-set(B))
changed=sorted(p for p in set(A)&set(B) if A[p]['sha256']!=B[p]['sha256'])
unchanged=sorted(p for p in set(A)&set(B) if A[p]['sha256']==B[p]['sha256'])
out={'v6ManifestSha':None,'added':added,'removed':removed,'changed':changed,
     'counts':{'added':len(added),'removed':len(removed),'changed':len(changed),'unchanged':len(unchanged)},
     'changedDetail':[{'path':p,'v6Bytes':A[p]['bytes'],'v7Bytes':B[p]['bytes']} for p in changed]}
json.dump(out,open('/tmp/opensip-design-corrections/post-reset-review.v7/delta-v6-v7.json','w'),indent=1)
print(json.dumps(out['counts']))
print('--- CHANGED ---')
for d in out['changedDetail']: print(' ',d['path'],d['v6Bytes'],'->',d['v7Bytes'])
print('--- ADDED (%d) ---'%len(added))
for p in added: print(' ',p)
print('--- REMOVED ---')
for p in removed: print(' ',p)
