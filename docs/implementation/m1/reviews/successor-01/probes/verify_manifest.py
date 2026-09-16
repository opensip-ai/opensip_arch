import hashlib,json,os,sys
m=json.load(open('/tmp/opensip-implementation/m1-successor-subject-01.json'))
root=m['subjectRoot'];bad=0;listed=set()
for f in m['files']:
    p=os.path.join(root,f['path']);listed.add(f['path'])
    b=open(p,'rb').read()
    ok=hashlib.sha256(b).hexdigest()==f['sha256'] and len(b)==f['bytes']
    if not ok: bad+=1
    print('OK ' if ok else 'BAD',f['path'])
extra=[]
for d,_,fs in os.walk(root):
    for x in fs:
        r=os.path.relpath(os.path.join(d,x),root)
        if r not in listed: extra.append(r)
print('extra files:',extra)
print('RESULT', 'PASS' if bad==0 else 'FAIL', len(m['files']))
sys.exit(1 if bad else 0)
