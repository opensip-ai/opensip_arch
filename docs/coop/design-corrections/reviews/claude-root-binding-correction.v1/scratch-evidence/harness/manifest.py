import os,json,hashlib
S='/private/tmp/opensip-design-corrections/claude-root-binding-correction.v1/scratch'
OUT=S+'/output'; BASE=S+'/baseline25'; TREE=S+'/src25'
def sha(fp): return hashlib.sha256(open(fp,'rb').read()).hexdigest()
rows=[]
for dp,dn,fn in os.walk(OUT):
    for f in sorted(fn):
        fp=os.path.join(dp,f); rel=os.path.relpath(fp,OUT)
        if rel=='evidence-manifest.json': continue
        rows.append({'path':rel,'bytes':os.path.getsize(fp),'sha256':sha(fp)})
rows.sort(key=lambda r:r['path'])
changed=[]
for dp,dn,fn in os.walk(BASE):
    for f in fn:
        b=os.path.join(dp,f); rel=os.path.relpath(b,BASE); t=os.path.join(TREE,rel)
        if os.path.isfile(t) and sha(b)!=sha(t):
            changed.append({'path':rel,'beforeSha256':sha(b),'afterSha256':sha(t),
                            'beforeBytes':os.path.getsize(b),'afterBytes':os.path.getsize(t)})
changed.sort(key=lambda r:r['path'])
man={
 'standing':'AUTHORED bounded correction for F-04/Q-2 plus F-05/F-06 reference controls. Author-assisted reference work by a reviewer acting as author; NOT independent acceptance, NOT blind reconstruction, NOT product implementation or readiness authorization. Frozen candidate25 and the frozen author package are unmodified; every write is confined to this scratch directory.',
 'boundCandidateManifestSha256':'fa8cdc796c4dbab514c8b8a91a593b740e3f8e69d19574f4be11c6e00c3a536d',
 'boundAuthorPackageManifestSha256':'c533aa6ab8939e6ecf710d217233aea8818fd1783e770b0db5ba81e375d316c4',
 'frozenCandidateFilesVerified':12869,
 'frozenAuthorPackageFilesVerified':97,
 'frozenInputsModified':False,
 'changedSourceFiles':changed,
 'authoredEvidence':rows,
 'fileCount':len(rows)}
json.dump(man,open(OUT+'/evidence-manifest.json','w'),indent=1)
print('changed source files:',len(changed))
for c in changed: print('   ',c['path'])
print('authored evidence files:',len(rows))
