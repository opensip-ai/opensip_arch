import json,hashlib,os
MP='/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v21.json'
LIVE='/Users/sb/code/opensip-ai/opensip_arch'
d=json.load(open(MP)); root=d['snapshotRoot']
mani={f['path']:f['sha256'] for f in d['files']}
def sh(p):
    try: return hashlib.sha256(open(p,'rb').read()).hexdigest()
    except FileNotFoundError: return None
c=d['protectedHistoryCustody']
print('=== CUSTODY 31 ===')
print('n',len(c['files']),'presentInPredecessor true:',sum(1 for f in c['files'] if f['presentInPredecessor']))
bad=[];liveDrift=[]
for f in c['files']:
    p=f['path']
    if p not in mani: bad.append((p,'NOT-IN-MANIFEST')); continue
    if mani[p]!=f['sha256']: bad.append((p,'MANIFEST-HASH-DIFF',mani[p],f['sha256']))
    if sh(os.path.join(root,p))!=f['sha256']: bad.append((p,'SNAPSHOT-DIFF'))
    lv=sh(os.path.join(LIVE,p))
    if lv!=f['sha256']: liveDrift.append((p,f['sha256'],lv))
print('custody problems:',len(bad),bad)
print('live drift vs frozen custody:',len(liveDrift))
for x in liveDrift: print('   DRIFT',x[0])
sr=c['sourceRecord']
print('sourceRecord in manifest:',sr['path'] in mani, 'hash ok:', mani.get(sr['path'])==sr['sha256'],
      'snapshot ok:', sh(os.path.join(root,sr['path']))==sr['sha256'])

print()
print('=== FOUR LEDGERS ===')
LED=['docs/coop/design-corrections/foundation/source-pins.v1.json',
     'docs/coop/design-corrections/native/source-pins.v2.json',
     'docs/coop/design-corrections/security/source-pins.v1.json',
     'docs/coop/design-corrections/workflows/source-pins.v1.json']
for L in LED:
    j=json.load(open(os.path.join(root,L)))
    print('---',L,'ledgerSha',mani.get(L))
    print('   keys:',list(j.keys())[:12])
    # locate pin list
    ents=None
    for k in ('pins','files','sources','sourcePins'):
        if isinstance(j.get(k),list): ents=j[k];pk=k;break
    if ents is None:
        for k,v in j.items():
            if isinstance(v,list) and v and isinstance(v[0],dict) and 'sha256' in v[0]: ents=v;pk=k;break
    if ents is None: print('   !! no pin list found; dump:',json.dumps(j)[:800]); continue
    print('   pin list key=',pk,'n=',len(ents),'sample',json.dumps(ents[0])[:200])
    ok=snapbad=livebad=0
    sb_=[];lb=[]
    for e in ents:
        p=e.get('path') or e.get('file')
        h=e.get('sha256')
        s=sh(os.path.join(root,p)); l=sh(os.path.join(LIVE,p))
        if s==h: ok+=1
        else: snapbad+=1; sb_.append((p,h,s))
        if l!=h: livebad+=1; lb.append((p,h,l))
    print('   snapshot: ok',ok,'bad',snapbad, sb_[:5])
    print('   live    : bad',livebad, [x[0] for x in lb][:5])
