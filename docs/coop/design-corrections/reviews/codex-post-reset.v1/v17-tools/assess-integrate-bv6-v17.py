"""Integrate exact mutually assessed architecture/reference source; fresh independent review owed."""
from pathlib import Path
import hashlib,json,shutil
root=Path.cwd();dc=root/'docs/coop/design-corrections';ev=dc/'reviews/codex-post-reset.v1';author=dc/'reviews/bv6-corrections-author.v6';work=Path('/tmp/opensip-design-corrections/bv6-corrections-author.v6/work')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();load=lambda p:json.loads(p.read_text())
def put(p,d):
 assert not p.exists(),str(p);p.write_text(json.dumps(d,indent=2)+'\n')
def ref(p):return {'path':str(p.relative_to(root)),'sha256':sha(p)}
# Written ONLY after root has actually read the completed v4 handoff/evidence and final bytes.
review=ev/'coauthor-assessment-bv6-v6.json';rv=load(review);assert rv['handoffReadInFull'] and rv['sourceDeltaReadInFull'] and rv['finalSourceAssent']
h=load(author/'handoff.json');assert h['technicalAssent']['value'] is True
assert sha(author/'handoff.json')==rv['handoffSha256'];assert load(author/'response.json')['is_error'] is False
custody=load(author/'custody.json')
for row in custody['files']:
 p=author/row['path'];assert sha(p)==row['sha256'] and p.stat().st_size==row['bytes'],str(p)
frozen=[]
for v,digest in [('v1','e7403b702d419f381be1cdbee7b886303fb43106b86985bc2f8ec63f5687a0ac'),('v16','ca5f36d421fb38d264f49fc6b2e1eeffee5bbe8182a7fe25bd50787244042ee9')]:
 mp=dc/('reviews/candidate-subject.'+v+'.json');assert sha(mp)==digest;m=load(mp)
 for row in m['files']:
  p=Path(m['snapshotRoot'])/row['path'];assert sha(p)==row['sha256'] and p.stat().st_size==row['bytes'],str(p)
 frozen.append({'version':v,'manifestSha256':digest,'filesVerified':len(m['files'])})
rows=[]
for r in h['changedSource']['files']:
 rel=r['path'];before=r['frozen16Sha256'];after=r['v6Sha256']
 assert sha(root/rel)==before and sha(work/rel)==after and sha(author/'work'/rel)==after,rel
 rows.append({'path':rel,'beforeSha256':before,'afterSha256':after,'coauthorSha256':after})
assert len(rows)==17
prior=dc/'reviews/bv6-corrections-author.v2/handoff.json';v2=load(prior);v3p=dc/'reviews/bv6-corrections-author.v3/handoff.json';v3=load(v3p);orig=load(dc/'reviews/consumer-b.v6/output/blind-review.json')
byid={x['id']:x for x in v2['originalFindingDispositions']}
notes={'MUST-1':'Native/imported per-requirement vocabularies, typed presence, per-kind consumer and explicit imported target projection/partial support are coherent. D9 enum remains unchanged; original evidence and authorization remain required.','MUST-2':'Every TypeScript configuration node has the deterministic config-file name; syntax-only and resolution-unit scope clarified without requiring the compiler for syntax-only.','SHOULD-1':'Command generic operations, admissible generic domain and per-step receipt operations are distinct; required receipt keys and lookup meanings are explicit, operational bindings do not grant permission.','SHOULD-2':'Inventory-relation totality is distinct from per-view scope disjointness, now enforced at retained Run closure including scopes without Coverage.'}
def finding(x):
 i=x['id'];return {'id':i,'originalSeverity':'MUST' if i.startswith('MUST') else 'SHOULD','status':'CORRECTED-PENDING-SUCCESSOR-REVIEW','basis':notes[i],'originalCoauthorDisposition':byid['CB6-'+i],'latestRootAssessment':ref(review)}
advice=[]
for x in orig['advisories']:
 i='CB6-'+x['id'];advice.append({'id':i,'originalId':x['id'],'originalSeverity':'ADVISORY','status':'ACCOUNTED-PENDING-SUCCESSOR-REVIEW','basis':byid[i]['disposition'],'rootAssessment':'Assessed against final source. Original severity retained; global native confidence rule is a selected law, not the reviewer\'s inferred types-only restriction. D9 future obligation remains unperformed.','sourceEvidence':ref(prior)})
additional=[]
for x in v2['rootPointDispositions']:
 additional.append({'id':x['id'],'originalSeverity':x['severity'],'status':'CORRECTED-PENDING-SUCCESSOR-REVIEW','coauthorDisposition':x,'subsequentCorrectionEvidence':[ref(v3p),ref(author/'handoff.json')],'rootAssessment':'Final source assessed with all subsequent corrections and report qualifications; the historical v2 disposition alone does not establish final correction.'})
for x in v2['originalFindingDispositions']:
 if x['id'].startswith('CB6-NEW'):
  additional.append({'id':x['id'],'originalSeverity':x['severity'],'status':'ACCOUNTED-PENDING-SUCCESSOR-REVIEW','coauthorDisposition':x,'rootAssessment':{'CB6-NEW-1':'Four command renames comprise3generic and1dedicated preparation; original all-generic wording corrected.','CB6-NEW-2':'Only config-write remains unbound in current command/step inventory; import and preparation have required bound receipts.','CB6-NEW-3':'Deferral withdrawn; actual overlap guard implemented and controls assessed.','CB6-NEW-4':'Registered schema document edits change committed schema digests and measured fixture IDs; not a universal proof of all identity movements.'}[x['id']]})
for x in v3['rootPointDispositions']:
 additional.append({'id':x['id'],'originalSeverity':x['severity'],'status':'CORRECTED-PENDING-SUCCESSOR-REVIEW','coauthorDisposition':x,'finalRootAssessment':ref(review)})
v4p=dc/'reviews/bv6-corrections-author.v4/out/handoff.json'
for x in load(v4p)['changesRequired']:
 additional.append({'id':x['id'],'originalSeverity':x['severity'],'status':'CORRECTED-PENDING-SUCCESSOR-REVIEW','originalFinding':x,'sourceEvidence':ref(v4p),'finalRootAssessment':ref(review)})
v5p=dc/'reviews/bv6-corrections-author.v5/handoff.json'
for x in load(v5p)['changesRequired']:
 additional.append({'id':x['id'],'originalSeverity':x['severity'],'status':'CORRECTED-PENDING-SUCCESSOR-REVIEW','originalFinding':x,'sourceEvidence':ref(v5p),'finalRootAssessment':ref(review)})
a={'standing':'Codex substantive source/integration assent to exact17-file proposal, including actual Claude review of root\'s final5file clarification. Fresh independent, NEW blind and full application acceptance remain required.','finalSourceAssent':True,'independentAcceptance':False,'actualCoauthorHandoff':ref(author/'handoff.json'),'actualCoauthorCustody':ref(author/'custody.json'),'actualRootFinalReview':ref(review),'sourceDelta':rows,'frozenVerification':frozen,'findingDispositions':[finding(x) for x in orig['newMustIssues']+orig['newShouldIssues']],'advisoryDispositions':advice,'additionalFindingDispositions':additional,'rootFinalV3Assessment':ref(ev/'coauthor-assessment-bv6-v3.json'),'rootProbeExecution':ref(ev/'bv6-final-v3-root-probes.v1/execution.json'),'reportQualifications':rv['reportQualifications'],'implementationAuthorized':False,'readinessChanged':False,'productQualification':False}
put(ev/'successor-source-assessment.v17.json',a)
before=ev/'source-before-v17';assert not before.exists();before.mkdir()
for r in rows:
 p=root/r['path'];q=before/r['path'];q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q)
for r in rows:
 p=root/r['path'];assert sha(p)==r['beforeSha256'];shutil.copyfile(author/'work'/r['path'],p);assert sha(p)==r['afterSha256']
put(ev/'source-integration.v17.json',{'files':rows,'sourceAssessment':ref(ev/'successor-source-assessment.v17.json'),'beforeImages':str(before.relative_to(root)),'implementationAuthorized':False})
print(json.dumps({'integrated':len(rows),'sourceAssent':True,'independentAcceptance':False}))
