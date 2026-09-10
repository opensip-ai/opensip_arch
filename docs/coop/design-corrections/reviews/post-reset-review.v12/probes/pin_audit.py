import json,hashlib,os,sys
ROOT='/tmp/opensip-design-corrections/candidate-subject.v12'
LEDGERS=['docs/coop/design-corrections/foundation/source-pins.v1.json',
 'docs/coop/design-corrections/security/source-pins.v1.json',
 'docs/coop/design-corrections/workflows/source-pins.v1.json',
 'docs/coop/design-corrections/native/source-pins.v2.json']
def sha(p):
    try: return hashlib.sha256(open(p,'rb').read()).hexdigest()
    except FileNotFoundError: return None
total=0;stale=[];missing=[]
for L in LEDGERS:
    d=json.load(open(os.path.join(ROOT,L)))
    # find pin entries generically
    n=0
    def walk(o,path=''):
        global n,total
        if isinstance(o,dict):
            if 'sha256' in o and ('path' in o or 'file' in o) and isinstance(o.get('sha256'),str):
                rel=o.get('path') or o.get('file')
                n+=1; total+=1
                fp=os.path.join(ROOT,rel)
                a=sha(fp)
                if a is None: missing.append((L,rel))
                elif a!=o['sha256']: stale.append((L,rel,o['sha256'],a))
            for k,v in o.items(): walk(v,path+'/'+k)
        elif isinstance(o,list):
            for i,v in enumerate(o): walk(v,path+'/%d'%i)
    walk(d)
    print('%-70s pins=%d'%(L.split('design-corrections/')[1],n))
print('TOTAL PINS',total)
print('STALE',len(stale))
for s in stale: print('  STALE',s)
print('MISSING',len(missing))
for s in missing: print('  MISSING',s)
