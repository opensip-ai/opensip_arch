import json,hashlib,os,sys
MAN='/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v12.json'
m=json.load(open(MAN))
root=m['snapshotRoot']
declared={}
bad=[]
for e in m['files']:
    declared[e['path']]=e
tot=0
for p,e in declared.items():
    fp=os.path.join(root,p)
    if not os.path.exists(fp):
        bad.append(('MISSING',p)); continue
    b=open(fp,'rb').read()
    h=hashlib.sha256(b).hexdigest()
    if h!=e['sha256']: bad.append(('DIGEST',p,e['sha256'],h))
    if len(b)!=e['bytes']: bad.append(('LEN',p,e['bytes'],len(b)))
    tot+=len(b)
actual=set()
for dp,dns,fns in os.walk(root):
    for fn in fns:
        actual.add(os.path.relpath(os.path.join(dp,fn),root))
undecl=sorted(actual-set(declared))
missing=sorted(set(declared)-actual)
print('manifestSha256', hashlib.sha256(open(MAN,'rb').read()).hexdigest())
print('declaredCount',len(declared),'actualCount',len(actual))
print('declaredTotalBytes',m['totalBytes'],'computedTotalBytes',tot,'match',tot==m['totalBytes'])
print('mismatches',len(bad))
for x in bad[:40]: print('  ',x)
print('undeclared',len(undecl))
for x in undecl[:40]: print('  U',x)
print('missing',len(missing))
for x in missing[:40]: print('  M',x)
# aggregate digest over sorted (path,sha) for cheap re-verification later
agg=hashlib.sha256()
for p in sorted(declared): agg.update(p.encode()+b'\0'+declared[p]['sha256'].encode()+b'\n')
print('AGGREGATE_TREE_DIGEST',agg.hexdigest())
