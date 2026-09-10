import json,hashlib,os,sys
MAN='/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v5.json'
REQ='ccb2311ddbcaea7e8bd540030621c982fa6757792721095a505e4e47652c74cf'
def h(p):
    x=hashlib.sha256()
    with open(p,'rb') as f:
        for c in iter(lambda:f.read(1<<20),b''): x.update(c)
    return x.hexdigest()
mh=h(MAN)
m=json.load(open(MAN))
root=m['snapshotRoot']
res={'manifestSha256':mh,'manifestMatchesRequired':mh==REQ,'snapshotRoot':root,
     'declaredFileCount':m['fileCount'],'declaredTotalBytes':m['totalBytes']}
bad=[];missing=[];tot=0
declared=set()
for e in m['files']:
    fp=os.path.join(root,e['path']); declared.add(e['path'])
    if not os.path.isfile(fp): missing.append(e['path']); continue
    sz=os.path.getsize(fp); tot+=sz
    a=h(fp)
    if a!=e['sha256'] or sz!=e['bytes']:
        bad.append({'path':e['path'],'expect':e['sha256'],'actual':a,'expectBytes':e['bytes'],'actualBytes':sz})
onDisk=set()
for dp,dn,fn in os.walk(root):
    dn[:]=[d for d in dn if d!='.git']
    for f in fn:
        onDisk.add(os.path.relpath(os.path.join(dp,f),root))
res.update({'actualFileCount':len(m['files']),'verifiedBytes':tot,'bytesMatch':tot==m['totalBytes'],
  'mismatched':bad,'missing':missing,'extraOnDisk':sorted(onDisk-declared),'notOnDisk':sorted(declared-onDisk),
  'onDiskCount':len(onDisk)})
res['ALL_MATCH']= not bad and not missing and not (onDisk-declared) and mh==REQ and tot==m['totalBytes']
print(json.dumps(res,indent=1)[:4000])
