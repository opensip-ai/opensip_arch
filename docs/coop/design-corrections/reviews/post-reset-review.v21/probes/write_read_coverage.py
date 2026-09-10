import json,hashlib,os
SNAP='/tmp/opensip-design-corrections/candidate-subject.v21'
MANI=json.load(open('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v21.json'))
m={f['path']:f for f in MANI['files']}
BASE='docs/v2/contracts/product-v1'
reads={
 'README.md':[[1,60]],
 'admission-and-qualification.md':[[1,304]],
 'identity-and-evidence.md':[[1,800],[801,1585]],
 'native-evidence.md':[[1,700],[701,1400],[1401,2100],[2101,2800],[2801,3435]],
 'security-and-lifecycle.md':[[1,600],[601,1176]],
 'workflows-and-surfaces.md':[[1,600],[601,1169]],
}
out={'subjectManifestSha256':'360c2758c0409ebc307966c7a385c385c2d7f580b4623dd760b7ba0e26bf18c1',
     'snapshotRoot':SNAP,'readTool':'Read (bounded consecutive, no skipped or truncated range)','files':[]}
allok=True
for n,rr in reads.items():
    rel=f'{BASE}/{n}'; fp=os.path.join(SNAP,rel)
    b=open(fp,'rb').read(); h=hashlib.sha256(b).hexdigest()
    total=b.decode('utf-8').count('\n')+(0 if b.endswith(b'\n') else 1)
    cov=[]; nxt=1; gaps=[]
    for a,z in rr:
        if a!=nxt: gaps.append([nxt,a-1])
        cov.append([a,z]); nxt=z+1
    if nxt-1!=total: gaps.append(['tail',nxt,total])
    ok=(not gaps)
    allok&=ok
    out['files'].append({'path':rel,'sha256':h,'manifestSha256':m[rel]['sha256'],
        'manifestAgrees':h==m[rel]['sha256'],'bytes':len(b),'totalLines':total,
        'observedReadRanges':cov,'contiguousFromLine1ToEnd':ok,'gaps':gaps})
out['allFilesFullyCovered']=allok
out['totalLinesRead']=sum(f['totalLines'] for f in out['files'])
json.dump(out,open('/tmp/opensip-design-corrections/post-reset-review.v21/contract-read-coverage.json','w'),indent=1)
print(json.dumps(out,indent=1))
