import os,shutil,hashlib,json,difflib
S='/private/tmp/opensip-design-corrections/claude-root-binding-correction.v1/scratch'
BASE=S+'/baseline25'; TREE=S+'/src25'; OUT=S+'/output'
FILES=OUT+'/files'; PATCHES=OUT+'/patches'
for d in [FILES,PATCHES]: os.makedirs(d,exist_ok=True)
def sha(fp): return hashlib.sha256(open(fp,'rb').read()).hexdigest()
pinfiles=['docs/coop/design-corrections/foundation/source-pins.v1.json',
          'docs/coop/design-corrections/foundation/evaluator3-source-pins.v1.json',
          'docs/coop/design-corrections/native/source-pins.v2.json',
          'docs/coop/design-corrections/security/source-pins.v1.json',
          'docs/coop/design-corrections/workflows/source-pins.v1.json']
changed=[]
for dp,dn,fn in os.walk(BASE):
    for f in fn:
        b=os.path.join(dp,f); rel=os.path.relpath(b,BASE); t=os.path.join(TREE,rel)
        if os.path.isfile(t) and sha(b)!=sha(t): changed.append(rel)
changed=sorted(changed)
GROUPS=[
 ('patch-01-f04-schema-internal-unit-root','normative',['docs/coop/design-corrections/native/native-evidence.schemas.v2.json']),
 ('patch-02-f04-native-model-order','normative',['docs/coop/design-corrections/native/native_evidence_model.v2.py']),
 ('patch-03-f04-enumeration-model-attribution','normative',['docs/coop/design-corrections/foundation/enumeration_model.v1.py']),
 ('patch-04-f04-native-evidence-contract-u0','normative',['docs/v2/contracts/product-v1/native-evidence.md']),
 ('patch-05-q2-execution-inputs-per-universe','normative',['docs/coop/design-corrections/foundation/execution-inputs-contract.v1.md']),
 ('patch-06-registered-schema-document-rebinding','consequential',['docs/coop/design-corrections/native/native-cases.v2.json']),
 ('patch-07-harness-canonical-set-positional-unpack','separable-harness-defect',['docs/coop/design-corrections/foundation/check-execution-inputs.v1.py']),
 ('patch-08-harness-canonical-set-substitution','separable-harness-defect',['docs/coop/design-corrections/security/check-analysis-seal-adapter.v1.py']),
 ('patch-09-source-pin-rebinding','scratch-only-rebinding',pinfiles),
]
covered=set()
index=[]
for name,kind,rels in GROUPS:
    lines=[]
    for rel in rels:
        covered.add(rel)
        a=open(os.path.join(BASE,rel),encoding='utf-8').read().splitlines(keepends=True)
        b=open(os.path.join(TREE,rel),encoding='utf-8').read().splitlines(keepends=True)
        lines.extend(difflib.unified_diff(a,b,fromfile='a/'+rel,tofile='b/'+rel,n=3))
    open(PATCHES+'/'+name+'.diff','w',encoding='utf-8').write(''.join(lines))
    index.append({'patch':name+'.diff','classification':kind,'files':rels,
                  'diffLines':len(lines),'sha256':sha(PATCHES+'/'+name+'.diff')})
    print(name,kind,'files',len(rels),'difflines',len(lines))
missing=[c for c in changed if c not in covered]
print('changed files not covered by a patch group:',missing)
for rel in changed:
    dst=os.path.join(FILES,'src25',rel); os.makedirs(os.path.dirname(dst),exist_ok=True)
    shutil.copy2(os.path.join(TREE,rel),dst)
print('changed full files copied:',len(changed))
json.dump({'patches':index,'changedFiles':changed,'uncovered':missing},open(OUT+'/patch-index.json','w'),indent=1)
