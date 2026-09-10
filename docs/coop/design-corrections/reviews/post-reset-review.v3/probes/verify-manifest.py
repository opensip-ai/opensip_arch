import json,hashlib,os,sys
MAN='/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v3.json'
ROOT='/tmp/opensip-design-corrections/candidate-subject.v3'
h=hashlib.sha256(open(MAN,'rb').read()).hexdigest()
m=json.load(open(MAN))
ok=0;bad=[];missing=[];extra=[]
listed=set()
for f in m['files']:
    p=os.path.join(ROOT,f['path']); listed.add(f['path'])
    if not os.path.exists(p): missing.append(f['path']); continue
    d=open(p,'rb').read()
    if hashlib.sha256(d).hexdigest()==f['sha256'] and len(d)==f['bytes']: ok+=1
    else: bad.append(f['path'])
# extra files in snapshot
for dp,dn,fn in os.walk(ROOT):
    for n in fn:
        rel=os.path.relpath(os.path.join(dp,n),ROOT)
        if rel not in listed: extra.append(rel)
out={'manifestSha256':h,'manifestMatchesRequired':h=='e3365d6e64cb5b0260ec7261af5c3e554504c9ab9515456f680aeb01b31b76fd','fileCount':m['fileCount'],'verifiedOk':ok,'hashMismatch':bad,'missing':missing,'extraInSnapshot':extra,'totalBytesDeclared':m['totalBytes'],'totalBytesSum':sum(f['bytes'] for f in m['files'])}
print(json.dumps(out,indent=1))
json.dump(out,open('/tmp/opensip-design-corrections/post-reset-review.v3/probes/verify-manifest.before.json','w'),indent=1)
