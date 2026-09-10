import json,hashlib,os,sys
MP='/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v21.json'
d=json.load(open(MP))
root=d['snapshotRoot']
files=d['files']
print('sample entry:',json.dumps(files[0],indent=1)[:600])
keys=set()
for f in files: keys|=set(f.keys())
print('entry keys union:',sorted(keys))
mism=[];missing=[];total=0
for f in files:
    rel=f.get('path')
    fp=os.path.join(root,rel)
    if not os.path.isfile(fp):
        missing.append(rel); continue
    b=open(fp,'rb').read()
    total+=len(b)
    h=hashlib.sha256(b).hexdigest()
    exp=f.get('sha256'); ln=f.get('bytes', f.get('length'))
    if exp and h!=exp: mism.append((rel,'sha',exp,h))
    if ln is not None and len(b)!=ln: mism.append((rel,'len',ln,len(b)))
print('missing:',len(missing),missing[:10])
print('mismatch:',len(mism),mism[:10])
print('totalBytes computed',total,'declared',d['totalBytes'],'match',total==d['totalBytes'])
# extra files in snapshot not in manifest
declared={f['path'] for f in files}
onk=set()
for dp,dn,fn in os.walk(root):
    for n in fn:
        onk.add(os.path.relpath(os.path.join(dp,n),root))
print('on-disk count',len(onk),'declared count',len(declared))
print('extra on disk:',len(onk-declared),sorted(onk-declared)[:10])
print('declared not on disk:',len(declared-onk),sorted(declared-onk)[:10])
