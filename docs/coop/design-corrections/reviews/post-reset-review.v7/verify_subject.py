import json,hashlib,os,sys
MAN='/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v7.json'
raw=open(MAN,'rb').read()
man_sha=hashlib.sha256(raw).hexdigest()
m=json.loads(raw)
root=m['snapshotRoot']
res={'manifestSha256':man_sha,'manifestExpectedMatch':man_sha=='b5cfb5d316eb0101950476a37a2095ed0d9c5d51263408d3462f105d63165f7b',
     'snapshotRoot':root,'declaredCount':m['fileCount'],'declaredBytes':m['totalBytes']}
declared={}
mismatch=[];missing=[];dupes=[]
tot=0
for e in m['files']:
    p=e['path']
    if p in declared: dupes.append(p)
    declared[p]=e
    tot+=e['bytes']
res['sumOfDeclaredBytes']=tot
res['declaredBytesMatchesField']=tot==m['totalBytes']
res['declaredListLen']=len(m['files'])
res['duplicatePaths']=dupes
for p,e in declared.items():
    fp=os.path.join(root,p)
    if not os.path.isfile(fp):
        missing.append(p);continue
    b=open(fp,'rb').read()
    h=hashlib.sha256(b).hexdigest()
    if h!=e['sha256'] or len(b)!=e['bytes']:
        mismatch.append({'path':p,'expSha':e['sha256'],'gotSha':h,'expBytes':e['bytes'],'gotBytes':len(b)})
res['missing']=missing
res['hashOrLengthMismatch']=mismatch
onDisk=[]
for dp,dns,fns in os.walk(root):
    dns[:]=[d for d in dns]
    for fn in fns:
        rel=os.path.relpath(os.path.join(dp,fn),root)
        onDisk.append(rel)
res['onDiskCount']=len(onDisk)
res['undeclaredOnDisk']=sorted(set(onDisk)-set(declared))
res['symlinks']=[os.path.relpath(os.path.join(dp,n),root) for dp,dns,fns in os.walk(root) for n in list(dns)+list(fns) if os.path.islink(os.path.join(dp,n))]
res['emptyDirs']=[os.path.relpath(dp,root) for dp,dns,fns in os.walk(root) if not dns and not fns]
print(json.dumps(res,indent=1)[:4000])
json.dump(res,open(sys.argv[1],'w'),indent=1)
