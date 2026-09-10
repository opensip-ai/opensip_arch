import json,hashlib,os
S='/tmp/opensip-design-corrections/candidate-subject.v19'
R='docs/coop/design-corrections/reviews'
v18=json.load(open(os.path.join(S,R,'candidate-subject.v18.json')))
v19=json.load(open('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v19.json'))
a={f['path']:f['sha256'] for f in v18['files']}
b={f['path']:f['sha256'] for f in v19['files']}
changed=sorted(p for p in set(a)&set(b) if a[p]!=b[p])
added=sorted(set(b)-set(a)); removed=sorted(set(a)-set(b))
# owning documents of each governance group
OWN={'AR':['docs/coop/architecture-depth-review/REVIEW.md','docs/coop/design-corrections/correction-crosswalk.proposed.json'],
 'FW':['docs/coop/design-corrections/current-source-map.proposed.md'],
 'INHERITED':['docs/coop/design-corrections/inherited-residuals.proposed.md','docs/coop/design-corrections/inherited-row-sources.proposed.json'],
 'EVAL':['docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json'],
 'SCOPED':['docs/v2/architecture/08-decision-and-readiness-register.md'],
 'GATES':['docs/coop/design-corrections/qualification-gates.proposed.json'],
 'D372':['docs/coop/design-corrections/README.md','docs/coop/design-corrections/D-372-corrections.proposed.md']}
own={}
for g,ps in OWN.items():
    own[g]=[{'path':p,'inV18':p in a,'inV19':p in b,'byteIdentical':a.get(p)==b.get(p),'sha':b.get(p)} for p in ps]
# the five product contracts + index
cdir='docs/v2/contracts/product-v1/'
contracts=sorted(p for p in b if p.startswith(cdir))
out={'v18Count':v18['fileCount'],'v19Count':v19['fileCount'],
 'changedCount':len(changed),'addedCount':len(added),'removedCount':len(removed),
 'changed':changed,'added':added,'removed':removed,
 'owningDocs':own,'productContracts':[{'path':p,'changed':a.get(p)!=b.get(p),'newFile':p not in a} for p in contracts]}
json.dump(out,open('/tmp/opensip-design-corrections/post-reset-review.v19/results/manifest-delta.json','w'),indent=1)
print('v18',v18['fileCount'],'v19',v19['fileCount'])
print('changed',len(changed),'added',len(added),'removed',len(removed))
print('CHANGED (non-review-dir):');
for p in changed:
    if '/reviews/' not in p: print('  *',p)
print('CHANGED under reviews/:',sum(1 for p in changed if '/reviews/' in p))
print('ADDED (non-review-dir):')
for p in added:
    if '/reviews/' not in p: print('  +',p)
print('ADDED under reviews/:',sum(1 for p in added if '/reviews/' in p))
print('OWNING DOCS:');print(json.dumps(own,indent=1))
print('CONTRACTS:');print(json.dumps(out['productContracts'],indent=1))
