from pathlib import Path
import json,hashlib
B=Path('/tmp/opensip-design-corrections');L=Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews');rt=B/'claude-independent32-reconciliation.v1';O=B/'root-independent32-reconciled-record-audit.v1';assert not O.exists();O.mkdir();sha=lambda b:hashlib.sha256(b).hexdigest();raw=(rt/'review.json').read_bytes();j=json.loads(raw);old=json.loads((B/'claude-independent-design.v31/review.json').read_bytes());m=json.loads((L/'candidate-subject.v32.json').read_bytes());p=json.loads((L/'candidate-subject.v31.json').read_bytes());files={r['path']:r for r in m['files']};before={r['path']:r for r in p['files']};findings=[];rows=[];families={'fDispositions':14,'evaluationResidualDispositions':30,'arDispositions':16,'fwDispositions':15,'inheritedResidualDispositions':27,'scopedReviewOwnerDispositions':5}
for k,count in families.items():
 group=j.get(k)
 if not isinstance(group,dict):findings.append({'family':k,'issue':'Expected individually keyed map absent or wrong shape'});continue
 if set(group)!=set(old[k]) or len(group)!=count:findings.append({'family':k,'issue':'Original required key population differs','keys':sorted(group)})
 for ident,r in group.items():
  owners=r.get('currentOwnerFiles',r.get('currentOwnerSelectors',r.get('owningSelectors',[])));actual=[]
  for rel in owners:
   path=rel.split('#')[0]
   if path in files:actual.append(path)
   else:findings.append({'family':k,'id':ident,'issue':'Owner path not a frozen source member','owner':rel})
  if k!='fDispositions' and not actual:findings.append({'family':k,'id':ident,'issue':'No actual current owning file supplied in the expected owner fields'})
  if k!='fDispositions':
   for flag in ['appliedByThisReview','finalApplicationOutcomeGranted']:
    if r.get(flag) is not False:findings.append({'family':k,'id':ident,'issue':'Design-only false flag missing or changed','flag':flag,'value':r.get(flag)})
  changed=[x for x in actual if before.get(x,{}).get('sha256')!=files[x]['sha256']]
  for field in ['ownerFilesChangedIn31to32','ownerFilesUnchangedIn31to32']:
   if field in r:
    want=set(changed) if 'Changed' in field else set(actual)-set(changed)
    if set(r[field])!=want:findings.append({'family':k,'id':ident,'issue':'Current changed-file account differs from measured hash delta','field':field,'claimed':r[field],'actual':sorted(want)})
  rows.append({'family':k,'id':ident,'owners':actual,'actualOwnerFilesChanged31to32':changed,'readingStanding':r.get('readingStanding'),'currentFields':{x:v for x,v in r.items() if x.startswith('current') or x in ['disposition','limits','sharedAssumption']}})
result={'standing':'Mechanical review-record scope/owner/hash account only; root substantive reading, exact custody and assessment required. No source acceptance or application grade.','reviewSha256':sha(raw),'subjectManifestSha256':sha((L/'candidate-subject.v32.json').read_bytes()),'claimedVerdict':j.get('verdict'),'claimedMustIssues':j.get('newMustIssues'),'claimedShouldIssues':j.get('newShouldIssues'),'rows':rows,'mechanicalFindings':findings};(O/'audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'rows':len(rows),'mechanicalFindings':findings},indent=2))
