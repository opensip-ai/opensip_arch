import json,hashlib,os,collections
S='/private/tmp/opensip-design-corrections/claude-root-binding-correction.v1/scratch'
BASE=S+'/baseline25'; TREE=S+'/src25'
def sha(fp): return hashlib.sha256(open(fp,'rb').read()).hexdigest()
def dumps_like(original_bytes, obj):
    import json as _j
    for ind in (1,2,3,4):
        for suf in ('\n',''):
            cand=(_j.dumps(_j.loads(original_bytes),indent=ind)+suf).encode('utf-8')
            if cand==original_bytes:
                return _j.dumps(obj,indent=ind)+suf
    return _j.dumps(obj,indent=1)+chr(10)
SCHEMA_REL='docs/coop/design-corrections/native/native-evidence.schemas.v2.json'
FIXTURE_REL='docs/coop/design-corrections/native/native-cases.v2.json'
delta=[]
# PASS 1: rebind the registered-schema-document declaration inside the native fixture
oldd=sha(os.path.join(BASE,SCHEMA_REL)); newd=sha(os.path.join(TREE,SCHEMA_REL))
raw=open(os.path.join(BASE,FIXTURE_REL),encoding='utf-8').read()
cnt=raw.count(oldd); raw2=raw.replace(oldd,newd)
open(os.path.join(TREE,FIXTURE_REL),'w',encoding='utf-8').write(raw2)
delta.append({'kind':'registered-schema-document-declaration','file':FIXTURE_REL,'occurrencesRebound':cnt,
              'beforeSha256':sha(os.path.join(BASE,FIXTURE_REL)),'afterSha256':sha(os.path.join(TREE,FIXTURE_REL)),
              'declaredDocumentDigestBefore':oldd,'declaredDocumentDigestAfter':newd})
print('PASS1 fixture occurrences rebound:',cnt)
# PASS 2: rebind every source pin for every file whose bytes now differ
# auto-detect every file whose bytes differ from the frozen baseline, EXCLUDING pin ledgers
pinfiles=['docs/coop/design-corrections/foundation/source-pins.v1.json',
          'docs/coop/design-corrections/foundation/evaluator3-source-pins.v1.json',
          'docs/coop/design-corrections/native/source-pins.v2.json',
          'docs/coop/design-corrections/security/source-pins.v1.json',
          'docs/coop/design-corrections/workflows/source-pins.v1.json']
changed=[]
for dp,dn,fn in os.walk(BASE):
    for f in fn:
        bfp=os.path.join(dp,f); rel=os.path.relpath(bfp,BASE)
        tfp=os.path.join(TREE,rel)
        if rel in pinfiles: continue
        if not os.path.isfile(tfp): continue
        if sha(bfp)!=sha(tfp): changed.append(rel)
changed=sorted(changed)
print('auto-detected changed files:',len(changed))
for c in changed: print('   ',c)
oldsha={}; newsha={}
for rel in changed:
    oldsha[rel]=sha(os.path.join(BASE,rel)); newsha[rel]=sha(os.path.join(TREE,rel))
for pf in pinfiles:
    bp=os.path.join(BASE,pf); tp=os.path.join(TREE,pf)
    d=json.loads(open(bp,'rb').read(),object_pairs_hook=collections.OrderedDict)
    key='pins' if 'pins' in d else 'files'
    n=0
    for row in d.get(key,[]):
        rel=row.get('path')
        if rel in oldsha and row.get('sha256')==oldsha[rel]:
            row['sha256']=newsha[rel]; n+=1
            delta.append({'kind':'source-pin','container':key,'pinFile':pf,'path':rel,
                          'beforeSha256':oldsha[rel],'afterSha256':newsha[rel]})
    out=dumps_like(open(bp,'rb').read(), d)
    open(tp,'w',encoding='utf-8').write(out)
    delta.append({'kind':'pin-file-identity','pinFile':pf,'rowsRebound':n,
                  'beforeSha256':sha(bp),'afterSha256':sha(tp)})
    print('PASS2',pf,'rows',n)
# PASS 3: pin ledgers pin each other; rebind the ledger hashes inside evaluator3-source-pins.v1.json
EV3='docs/coop/design-corrections/foundation/evaluator3-source-pins.v1.json'
ev3p=os.path.join(TREE,EV3)
d=json.loads(open(ev3p,'rb').read(),object_pairs_hook=collections.OrderedDict)
key='pins' if 'pins' in d else 'files'
n3=0
for row in d.get(key,[]):
    rel=row.get('path')
    if rel in pinfiles and rel!=EV3:
        cur=sha(os.path.join(TREE,rel))
        if row.get('sha256')!=cur:
            delta.append({'kind':'pin-ledger-cross-pin','pinFile':EV3,'path':rel,
                          'beforeSha256':row.get('sha256'),'afterSha256':cur})
            row['sha256']=cur; n3+=1
out=dumps_like(open(os.path.join(BASE,EV3),'rb').read(), d)
open(ev3p,'w',encoding='utf-8').write(out)
delta.append({'kind':'pin-file-identity-final','pinFile':EV3,'rowsRebound':n3,'afterSha256':sha(ev3p)})
print('PASS3 cross-pinned ledger rows rebound:',n3)
rep={'standing':'SCRATCH-ONLY rebinding for the authored F-04/Q-2 correction. Frozen candidate25 bytes are unchanged; this records exactly what an integrator must rebind.',
     'changedSourceFiles':[{'path':k,'beforeSha256':oldsha[k],'afterSha256':newsha[k]} for k in changed],
     'rebindings':delta}
json.dump(rep,open(S+'/output/evidence/source-pin-rebinding.json','w'),indent=1)
print('total delta rows',len(delta))
