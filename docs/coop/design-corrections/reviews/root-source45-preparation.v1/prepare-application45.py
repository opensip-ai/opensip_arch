from pathlib import Path
import json,hashlib,shutil,difflib
B=Path('/tmp/opensip-design-corrections');R=Path('/Users/sb/code/opensip-ai/opensip_arch');O=B/'application45-source-preparation.v1';assert not O.exists();O.mkdir();mp=R/'docs/coop/design-corrections/reviews/candidate-subject.v45.json';raw=mp.read_bytes();h=hashlib.sha256(raw).hexdigest();m=json.loads(raw);S=Path(m['snapshotRoot']);members={r['path']:r for r in m['files']};old=json.loads((B/'application44-source-preparation.v1/source-delta.reconciled.json').read_bytes());expected={r['path']:r['beforeSha256'] for r in old['files']};excluded={r['path'] for r in old['excludedPreservedFiles']};sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();rows=[];unexpected=[];exceptions=[];newly=[]
# First source45-only edits to formerly identical live paths need explicit read-only beforeimage review.
P=json.loads((R/'docs/coop/design-corrections/reviews/candidate-subject.v44.json').read_bytes());previous={r['path']:r for r in P['files']}
for rel,r in members.items():
 live=R/rel;before=sha(live) if live.is_file() else None
 if rel in excluded:exceptions.append({'path':rel,'liveSha256':before,'frozenSha256':r['sha256'],'standing':'Preserved navigation/history; separate conditional documentation draft handles navigation.'});continue
 if before==r['sha256']:continue
 if rel not in expected and before is not None:
  if rel in previous and before==previous[rel]['sha256']:
   newly.append({'path':rel,'beforeSha256':before,'standing':'Exact source44 byte equality measured; delta captured for root/independent assessment, not assumed accepted.'});expected[rel]=before
  else:unexpected.append({'path':rel,'observed':before,'expected':None})
 elif rel in expected and expected[rel]!=before:unexpected.append({'path':rel,'observed':before,'expected':expected[rel]})
 rows.append({'path':rel,'beforeSha256':before,'afterSha256':r['sha256'],'bytes':r['bytes'],'beforeimageAccount':'Guarded exact live beforeimage; inherited source44 delta or measured source44 equality' if before is not None else 'Absent live path; proposed addition'})
 if live.is_file():
  q=O/'before'/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(live.read_bytes())
  try:
   d=''.join(difflib.unified_diff(live.read_text().splitlines(True),(S/rel).read_text().splitlines(True),fromfile=rel,tofile=rel));q=O/'diffs'/(rel+'.diff');q.parent.mkdir(parents=True,exist_ok=True);q.write_text(d)
  except UnicodeError:pass
result={'standing':'Prospective source45 exact application delta only; no acceptance, assembly, grade or live source mutation. New source44-equal beforeimages are measured and captured; their semantic change still requires review.','designSubjectSha256':h,'files':rows,'unexpectedLiveDeltas':unexpected,'excludedPreservedFiles':exceptions,'newlyMeasuredSource44EqualBeforeimages':newly};(O/'source-delta.reconciled.json').write_text(json.dumps(result,indent=2)+'\n');assert not unexpected,unexpected
D=B/'application-draft.v27';assert not D.exists();shutil.copytree(B/'application-draft.v26',D);prop=json.loads((D/'documentation-proposal.json').read_bytes());assert len(prop['edits'])==17
for e in prop['edits']:assert sha(R/e['path'])==e['beforeSha256'] and sha(D/'files'/e['path'])==e['proposedSha256'],e['path']
prop['standing']=prop['standing'].replace('candidate44','candidate45');prop['prospectiveDesignSubjectSha256']=h;(D/'documentation-proposal.json').write_text(json.dumps(prop,indent=2)+'\n')
p=D/'readiness-row-map.proposed.json';j=json.loads(p.read_bytes());j['standing']=j['standing'].replace('Source44','Source45');pins=0;changed=0
for row in j['rows']:
 assert row['independentGrade']=='PENDING' and row['productQualified'] is False
 for r in row['productSuccessors']:n=members[r['path']]['sha256'];changed+=n!=r['sha256'];r['sha256']=n;pins+=1
p.write_text(json.dumps(j,indent=2)+'\n');assert len(j['rows'])==28
(O/'preparation.json').write_text(json.dumps({'standing':'Unapplied documentation/input preparation only. Independent design/blind/application prerequisites pending.','sourceManifestSha256':h,'sourceDeltaFiles':len(rows),'newlyMeasuredBeforeimages':len(newly),'documentationBeforeimagesVerified':17,'draft':str(D),'rows':28,'rowPins':pins,'changedPins':changed,'allIndependentGradesPending':True},indent=2)+'\n')
# Status is preparation metadata, not readiness or source activation.
p=B/'application-successor-root.v2/current-status.json';(O/'current-status.before.json').write_bytes(p.read_bytes());j=json.loads(p.read_bytes());j.update({'standing':'Source45 integrated correction preparation; original non-author independent45 review and blind reconstruction pending. No source assent, assembly, application or readiness.','readyForAssembly':False,'sourceAcceptance':False,'designSubjectSha256':h,'prospectiveSourceDeltaFiles':len(rows),'currentDraft':str(D),'prospectiveSourceDelta':str(O/'source-delta.reconciled.json'),'currentIndependentDesignReview':'docs/coop/design-corrections/reviews/claude-independent-design.v45/review.json','currentBlindContinuation':'consumer-b.v24-source45.v1','currentRootBlindAssent':False,'currentRootDesignAssent':None,'currentRootBlindAssessment':None,'currentDesignAdvisories':None,'pendingIndependentEvaluationResidualMap':True});p.write_text(json.dumps(j,indent=2)+'\n');print('Prospective delta',len(rows),'newly measured',len(newly),'draft27 rows28 pins',pins,'changed',changed)
