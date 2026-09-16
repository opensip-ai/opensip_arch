from pathlib import Path
import json,hashlib,shutil,difflib
B=Path('/tmp/opensip-design-corrections');R=Path('/Users/sb/code/opensip-ai/opensip_arch');O=B/'application30-source-preparation.v1';O.mkdir();mp=R/'docs/coop/design-corrections/reviews/candidate-subject.v30.json';raw=mp.read_bytes();h=hashlib.sha256(raw).hexdigest();m=json.loads(raw);S=Path(m['snapshotRoot']);members={r['path']:r for r in m['files']};old=json.loads((B/'application28-source-preparation.v1/source-delta.reconciled.json').read_text());expected={r['path']:r['beforeSha256'] for r in old['files']};excluded={r['path'] for r in old['excludedPreservedFiles']};sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();rows=[];unexpected=[];exceptions=[]
for rel,r in members.items():
 live=R/rel;before=sha(live) if live.is_file() else None
 if rel in excluded:exceptions.append({'path':rel,'liveSha256':before,'frozenSha256':r['sha256'],'standing':'Preserved navigation/history; separate conditional documentation draft handles navigation.'});continue
 if before==r['sha256']:continue
 if rel in expected and expected[rel]!=before or rel not in expected and before is not None:unexpected.append({'path':rel,'observed':before,'expected':expected.get(rel)})
 rows.append({'path':rel,'beforeSha256':before,'afterSha256':r['sha256'],'bytes':r['bytes'],'beforeimageAccount':'Previously examined source28 application beforeimage unchanged' if rel in expected else 'Absent live path; new normative input layer'})
 if live.is_file():
  q=O/'before'/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(live.read_bytes())
  try:
   diff=''.join(difflib.unified_diff(live.read_text().splitlines(True),(S/rel).read_text().splitlines(True),fromfile=rel,tofile=rel));q=O/'diffs'/(rel+'.diff');q.parent.mkdir(parents=True,exist_ok=True);q.write_text(diff)
  except UnicodeError:pass
result={'standing':'Prospective source30 exact delta only. No acceptance, assembly, grade or live source mutation. Source28 beforeimages preserved; source28 order/source29 catalog/source30 fixture corrections require independent review.','designSubjectSha256':h,'files':rows,'unexpectedLiveDeltas':unexpected,'excludedPreservedFiles':exceptions,'additionalExaminedBeforeimages':{'path':str(O/'before'),'standing':'Exact unchanged observed live bytes; differences retained for review.'}}
(O/'source-delta.reconciled.json').write_text(json.dumps(result,indent=2)+'\n');assert not unexpected,unexpected
D=B/'application-draft.v11';assert not D.exists();shutil.copytree(B/'application-draft.v10',D);prop=json.loads((D/'documentation-proposal.json').read_text());assert len(prop['edits'])==17
for e in prop['edits']:
 assert sha(R/e['path'])==e['beforeSha256'],e['path'];assert sha(D/'files'/e['path'])==e['proposedSha256'],e['path']
prop['standing']=prop['standing'].replace('candidate28','candidate30');prop['prospectiveDesignSubjectSha256']=h;(D/'documentation-proposal.json').write_text(json.dumps(prop,indent=2)+'\n')
p=D/'readiness-row-map.proposed.json';j=json.loads(p.read_text());j['standing']=j['standing'].replace('Source28','Source30');pins=0;changed=0
for row in j['rows']:
 assert row['independentGrade']=='PENDING' and row['productQualified'] is False
 for r in row['productSuccessors']:
  n=members[r['path']]['sha256'];changed+=n!=r['sha256'];r['sha256']=n;pins+=1
p.write_text(json.dumps(j,indent=2)+'\n');assert len(j['rows'])==28
(O/'preparation.json').write_text(json.dumps({'standing':'Unapplied documentation/input prep only. Actual design/blind/application prerequisites remain pending.','sourceManifestSha256':h,'sourceDeltaFiles':len(rows),'unexpectedLiveDeltas':unexpected,'documentationBeforeimagesVerified':17,'draft':str(D),'rows':len(j['rows']),'rowPins':pins,'changedPins':changed,'allIndependentGradesPending':True},indent=2)+'\n')
status=B/'application-successor-root.v2/current-status.json';(O/'current-status.before.json').write_bytes(status.read_bytes());j=json.loads(status.read_text());j.update({'standing':'Frozen30 order/catalog/fixture corrections pending actual Claude successor review after active27; blind16 active on byte-identical normative kit29. No current acceptance, binding, assembly or application.','readyForAssembly':False,'sourceAcceptance':False,'designSubjectSha256':h,'prospectiveSourceDeltaFiles':len(rows),'currentDraft':str(D),'prospectiveConsumerVersion':'v16','currentBlindKitSha256':'6aad82e65623c7204008c19fdbea0aee84c302c0ef225c57647cd3e75e4a3cc6','prospectiveSourceDelta':str(O/'source-delta.reconciled.json'),'currentIndependentDesignReview':'docs/coop/design-corrections/reviews/claude-independent-design.v30/review.json','currentBlindContinuation':'consumer-b.v16','currentRootBlindAssent':False,'currentRootDesignAssent':None,'currentRootBlindAssessment':None,'currentDesignAdvisories':None,'pendingIndependentEvaluationResidualMap':True,'currentCompletionRunbook':str(B/'application-completion-runbook.source30.v1.md')});status.write_text(json.dumps(j,indent=2)+'\n');print('Delta',len(rows),'draft17 rows28 pins',pins,'changed',changed)
