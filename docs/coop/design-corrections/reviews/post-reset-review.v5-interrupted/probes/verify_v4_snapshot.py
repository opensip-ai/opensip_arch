import json,hashlib,os
B='/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v4.json'
m=json.load(open(B)); root=m['snapshotRoot']
def h(p):
    x=hashlib.sha256()
    with open(p,'rb') as f:
        for c in iter(lambda:f.read(1<<20),b''): x.update(c)
    return x.hexdigest()
bad=[]
for e in m['files']:
    fp=os.path.join(root,e['path'])
    if not os.path.isfile(fp) or h(fp)!=e['sha256']: bad.append(e['path'])
print('v4 root',root,'files',len(m['files']),'bad',len(bad),bad[:5])
