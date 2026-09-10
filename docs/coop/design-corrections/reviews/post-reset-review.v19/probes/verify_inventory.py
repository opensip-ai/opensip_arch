import json,hashlib,os,sys
man=json.load(open('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v19.json'))
root=man['snapshotRoot']
files=man['files']
missing=[];hashmis=[];lenmis=[];total=0
seen=set()
for f in files:
    p=os.path.join(root,f['path']); seen.add(os.path.normpath(f['path']))
    if not os.path.isfile(p): missing.append(f['path']); continue
    b=open(p,'rb').read(); total+=len(b)
    if len(b)!=f['bytes']: lenmis.append((f['path'],len(b),f['bytes']))
    h=hashlib.sha256(b).hexdigest()
    if h!=f['sha256']: hashmis.append((f['path'],h,f['sha256']))
extra=[]
for dp,dn,fn in os.walk(root):
    dn[:] = [d for d in dn if d not in ('.git',)]
    for n in fn:
        rp=os.path.normpath(os.path.relpath(os.path.join(dp,n),root))
        if rp not in seen: extra.append(rp)
print(json.dumps({'declaredCount':man['fileCount'],'listLen':len(files),'declaredBytes':man['totalBytes'],
 'observedBytes':total,'missing':missing[:20],'missingCount':len(missing),
 'hashMismatch':hashmis[:20],'hashMismatchCount':len(hashmis),
 'lenMismatch':lenmis[:20],'lenMismatchCount':len(lenmis),
 'extraCount':len(extra),'extra':sorted(extra)[:20]},indent=1))
