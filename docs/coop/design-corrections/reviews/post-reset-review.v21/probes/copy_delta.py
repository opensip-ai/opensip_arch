import json,hashlib,os
MAN=json.load(open('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v21.json'))
m={f['path']:f['sha256'] for f in MAN['files']}
def scan(root,label):
    changed=[];added=[];removed=[]
    on=set()
    for dp,dn,fn in os.walk(root):
        for n in fn:
            p=os.path.join(dp,n); rel=os.path.relpath(p,root); on.add(rel)
            h=hashlib.sha256(open(p,'rb').read()).hexdigest()
            if rel not in m: added.append(rel)
            elif h!=m[rel]: changed.append({'path':rel,'frozenSha256':m[rel],'afterSha256':h,
                                            'afterBytes':os.path.getsize(p)})
    removed=sorted(set(m)-on)
    return {'label':label,'fileCount':len(on),'changed':changed,'added':sorted(added),'removed':removed}
out={'standing':'ACTUAL copy delta after executing the six canonical commands / after the single-law mutation. Frozen subject untouched.',
     'canonicalCopy':scan('/tmp/opensip-design-corrections/post-reset-review.v21/work/copy','six canonical commands executed'),
     'mutationCopy':scan('/tmp/opensip-design-corrections/post-reset-review.v21/work/mutation/tree','one law mutated + check-identity.py run')}
json.dump(out,open('/tmp/opensip-design-corrections/post-reset-review.v21/results/copy-delta.json','w'),indent=1)
for k in ('canonicalCopy','mutationCopy'):
    d=out[k]
    print('===',k,d['label'],'files',d['fileCount'])
    print('  changed:',len(d['changed']),'added:',len(d['added']),'removed:',len(d['removed']))
    for c in d['changed']: print('    CHANGED',c['path'],c['frozenSha256'][:12],'->',c['afterSha256'][:12])
    for a in d['added'][:10]: print('    ADDED',a)
