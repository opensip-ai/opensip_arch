import json,os,difflib
S='/tmp/opensip-design-corrections/candidate-subject.v19'
D=json.load(open('/tmp/opensip-design-corrections/post-reset-review.v19/results/manifest-delta.json'))
print('changed under reviews/:',[p for p in D['changed'] if '/reviews/' in p])
sd=[d['path'] for d in json.load(open(os.path.join(S,'docs/coop/design-corrections/reviews/codex-post-reset.v1/successor-source-assessment.v19.json')))['sourceDelta']]
print('sourceDelta subset of changed+added:', set(sd) <= set(D['changed'])|set(D['added']))
print('changed NOT in sourceDelta:'); 
for p in D['changed']:
    if p not in sd: print('   ',p)
# leaf-by-leaf crosswalk diff v18 vs v19
def leaves(o,path=''):
    if isinstance(o,dict):
        for k,v in o.items():
            yield from leaves(v,path+'/'+k)
    elif isinstance(o,list):
        for i,v in enumerate(o): yield from leaves(v,path+'/'+str(i))
    else: yield path,o
B=os.path.join(S,'docs/coop/design-corrections/reviews/codex-post-reset.v1/crosswalk-before-v19.json')
A=os.path.join(S,'docs/coop/design-corrections/correction-crosswalk.proposed.json')
lb=dict(leaves(json.load(open(B)))); la=dict(leaves(json.load(open(A))))
chg={k:(lb[k],la[k]) for k in set(lb)&set(la) if lb[k]!=la[k]}
add=sorted(set(la)-set(lb)); rem=sorted(set(lb)-set(la))
import collections
def kind(p): return p.rsplit('/',1)[-1] if not p.rsplit('/',1)[-1].isdigit() else p.rsplit('/',2)[-2]
print('\nCROSSWALK leaf delta: changed',len(chg),'added',len(add),'removed',len(rem))
print('changed leaf kinds:',dict(collections.Counter(kind(k) for k in chg)))
print('added leaf paths (grouped):',dict(collections.Counter(k.split('/')[3] if len(k.split('/'))>3 else k for k in add)))
print('removed:',rem[:10])
STRUCT=('obligation','selector','owner','unit','contract','status','id','ownerRows')
print('structural leaves changed:',{k:v for k,v in chg.items() if kind(k) in STRUCT})
# README (D-372) diff
rb=open(os.path.join(S,'docs/coop/design-corrections/reviews/codex-post-reset.v1/corrections-readme-before-v19.md')).read().splitlines()
ra=open(os.path.join(S,'docs/coop/design-corrections/README.md')).read().splitlines()
print('\nREADME diff:')
for l in difflib.unified_diff(rb,ra,lineterm='',n=1): print('  ',l[:220])
