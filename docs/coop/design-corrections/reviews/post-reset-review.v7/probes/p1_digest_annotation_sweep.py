# Independent sweep: every schema node whose pattern admits a 64-hex string
# (bare or prefixed). Checks x-opensip-digest coverage without importing the
# author's checker. Anchors in this bundle are (?![\s\S]), not $.
import json,re,sys
S='/tmp/opensip-design-corrections/candidate-subject.v7/docs/coop/design-corrections/'
sch=json.load(open(S+'foundation/identity-schemas.v2.json'))
BARE=re.compile(r'^\^\[0-9a-f\]\{64\}(\(\?!\[\\s\\S\]\)|\$)$')
def bare64(n): return isinstance(n,dict) and isinstance(n.get('pattern'),str) and BARE.match(n['pattern'])
def anyhex(n): return isinstance(n,dict) and isinstance(n.get('pattern'),str) and '[0-9a-f]{64}' in n['pattern']
bare=[];pref=[]
def walk(n,path):
    if isinstance(n,dict):
        if anyhex(n): (bare if bare64(n) else pref).append((path,n))
        for k,v in n.items(): walk(v,path+'/'+k)
    elif isinstance(n,list):
        for i,v in enumerate(n): walk(v,path+'/'+str(i))
walk(sch,'')
def rep(n): 
    a=n.get('x-opensip-digest'); return a if isinstance(a,dict) else None
unann=[p for p,n in bare if not rep(n)]
prefunann=[(p,n['pattern']) for p,n in pref if not rep(n)]
reps={};rets={}
for p,n in bare+pref:
    a=rep(n)
    if a:
        reps.setdefault(a.get('representation'),[]).append(p)
        rets.setdefault(a.get('retention','<absent>'),[]).append(p)
out={'bare64Fields':len(bare),'prefixedHexFields':len(pref),
     'bareUnannotated':unann,'prefixedUnannotated':prefunann,
     'representationCounts':{k:len(v) for k,v in reps.items()},
     'retentionCounts':{k:len(v) for k,v in rets.items()},
     'annotationKeysSeen':sorted({k for p,n in bare+pref if rep(n) for k in rep(n)})}
print(json.dumps(out,indent=1))
targets={'programPredicateDigest','parameterDigest','stageSpecDigest','outputSchemaDigest','inventoryDigest'}
print('\n=== NEW-MUST-1 FIELDS (all occurrences) ===')
for p,n in bare+pref:
    if p.rsplit('/',1)[-1] in targets:
        print(p); print('   ',json.dumps(rep(n)))
json.dump({'bare':[p for p,_ in bare],'pref':[p for p,_ in pref],'bareUnannotated':unann,'prefixedUnannotated':prefunann},open(sys.argv[1],'w'),indent=1)
