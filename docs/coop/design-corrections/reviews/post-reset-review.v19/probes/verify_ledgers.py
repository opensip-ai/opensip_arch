import json,hashlib,os
S='/tmp/opensip-design-corrections/candidate-subject.v19'
C=os.path.join(S,'docs/coop/design-corrections/reviews/codex-post-reset.v1')
def sh(rel):
    p=os.path.join(S,rel)
    return hashlib.sha256(open(p,'rb').read()).hexdigest() if os.path.isfile(p) else None
res={'declaredVsFrozen':[],'pinLedgers':{}}
acct=json.load(open(os.path.join(C,'final-source-account.v19.json')))
for f in acct['files']:
    o=sh(f['path']); res['declaredVsFrozen'].append({'path':f['path'],'declared':f['finalSha256'],'observed':o,'match':o==f['finalSha256']})
for k in ['sourceAssessment','priorIndependentRootAssessment','actualFinalCommands']:
    e=acct[k]; o=sh(e['path']); res['declaredVsFrozen'].append({'path':e['path'],'declared':e['sha256'],'observed':o,'match':o==e['sha256']})
sa=json.load(open(os.path.join(C,'successor-source-assessment.v19.json')))
for grp in ['actualCoauthorHandoffs','rootCoauthorAssessments','normativeInputAdditions','referenceEvidence']:
    for e in sa[grp]:
        o=sh(e['path']); res['declaredVsFrozen'].append({'grp':grp,'path':e['path'],'declared':e['sha256'],'observed':o,'match':o==e['sha256']})
for k in ['priorIndependentReview','priorRootAssessment','predecessorManifest','latestBlindClarification']:
    e=sa[k]; o=sh(e['path']); res['declaredVsFrozen'].append({'grp':k,'path':e['path'],'declared':e['sha256'],'observed':o,'match':o==e['sha256']})
w=sa['withdrawnFinding']
for k in ['evidence','rootAssessment']:
    e=w[k]; o=sh(e['path']); res['declaredVsFrozen'].append({'grp':'withdrawn/'+k,'path':e['path'],'declared':e['sha256'],'observed':o,'match':o==e['sha256']})
for d in sa['sourceDelta']:
    o=sh(d['path']); res['declaredVsFrozen'].append({'grp':'sourceDelta.after','path':d['path'],'declared':d['afterSha256'],'observed':o,'match':o==d['afterSha256']})
    p=sh(d['sourceProposal']); res['declaredVsFrozen'].append({'grp':'sourceDelta.proposalBytesEqualFinal','path':d['sourceProposal'],'declared':d['afterSha256'],'observed':p,'match':p==d['afterSha256']})
# pin ledgers
for name,rel in [('foundation','docs/coop/design-corrections/foundation/source-pins.v1.json'),
                 ('security','docs/coop/design-corrections/security/source-pins.v1.json'),
                 ('native','docs/coop/design-corrections/native/source-pins.v2.json'),
                 ('workflows','docs/coop/design-corrections/workflows/source-pins.v1.json')]:
    d=json.load(open(os.path.join(S,rel)))
    entries=d.get('files') or d.get('pins') or d
    mis=[];items=[]
    if isinstance(entries,list):
        for e in entries:
            pth=e.get('path'); dec=e.get('sha256') or e.get('finalSha256')
            o=sh(pth); items.append(pth)
            if o!=dec: mis.append({'path':pth,'declared':dec,'observed':o})
    res['pinLedgers'][name]={'ledgerSha':sh(rel),'keys':list(d.keys()) if isinstance(d,dict) else 'list',
      'count':len(items),'paths':items,'mismatches':mis}
bad=[x for x in res['declaredVsFrozen'] if not x['match']]
res['declaredMismatchCount']=len(bad); res['declaredMismatches']=bad
res['declaredCheckedCount']=len(res['declaredVsFrozen'])
json.dump(res,open('/tmp/opensip-design-corrections/post-reset-review.v19/results/ledger-verify.json','w'),indent=1)
print('checked',res['declaredCheckedCount'],'mismatch',len(bad))
for k,v in res['pinLedgers'].items(): print(k,'ledgerSha',v['ledgerSha'][:12],'count',v['count'],'mism',len(v['mismatches']))
print(json.dumps({k:v['paths'] for k,v in res['pinLedgers'].items()},indent=1))
