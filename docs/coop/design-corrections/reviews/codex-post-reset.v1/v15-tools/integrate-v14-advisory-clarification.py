"""Retain completed actual coauthor assessment; adopt its exact alternative and assented prose."""
from pathlib import Path
import json,hashlib,shutil,datetime,copy
root=Path.cwd();dc=root/'docs/coop/design-corrections';ev=dc/'reviews';own=ev/'codex-post-reset.v1';src=Path('/tmp/opensip-design-corrections/v14-advisory-clarification.v1');dest=ev/src.name
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();read=lambda p:json.loads(p.read_text())
response=read(src/'response.json');assert response['is_error'] is False and response['session_id']=='77758b10-d7ba-4868-9d42-ae0b13e84cb6'
a=read(src/'assessment.json');proposal=read(src/'proposal.json');assert a['proposalSha256']==sha(src/'proposal.json') and a['technicalAssent'] is False
assert a['perChangeAssent']=={'V14-ADV-1':False,'V14-ADV-2':True}
assert (src/'assessment.md').is_file()
changes={r['id']:r for r in a['changes']};choices=[('V14-ADV-1',src/changes['V14-ADV-1']['preciseAlternative']['exactProposedFile'],changes['V14-ADV-1']['preciseAlternative']['alternativeSha256'],'Root adopts the exact Claude-authored alternative after substantive review; the original root proposal was NOT assented.'),('V14-ADV-2',src/'proposed'/changes['V14-ADV-2']['path'],changes['V14-ADV-2']['proposedSha256'],'Root adopts the exact root proposal to which Claude explicitly assented.')]
for issue,p,digest,basis in choices:
 row=changes[issue];assert sha(p)==digest and sha(root/row['path'])==row['beforeSha256'];before=(root/row['path']).read_text()
 repl= row['preciseAlternative'] if issue=='V14-ADV-1' else next(r for r in proposal['changes'] if r['id']==issue)
 assert before.count(repl['old'])==1 and before.replace(repl['old'],repl['new']).encode()==p.read_bytes()
 if p.suffix=='.json':
  b=read(root/row['path']);c=read(p);b['x-opensip-relation-registry']['anchorLaw']['enforcedAt']=c['x-opensip-relation-registry']['anchorLaw']['enforcedAt'];assert b==c
assert not dest.exists();shutil.copytree(src,dest)
rows=[]
for p in sorted(src.rglob('*')):
 assert not p.is_symlink()
 if p.is_file():q=dest/p.relative_to(src);assert sha(q)==sha(p);rows.append({'path':str(p.relative_to(src)),'sha256':sha(p),'bytes':p.stat().st_size})
log=Path('/Users/sb/.claude/projects/-private-tmp-opensip-design-corrections-bv4-corrections-author-v1-work/77758b10-d7ba-4868-9d42-ae0b13e84cb6.jsonl');start=datetime.datetime.fromisoformat(read(src/'process.json')['startedAt']);blocks=[]
for line in log.read_text().split('\n'):
 if not line:continue
 d=json.loads(line)
 if not d.get('timestamp') or datetime.datetime.fromisoformat(d['timestamp'].replace('Z','+00:00'))<start:continue
 for v in d.get('message',{}).get('content',[]):
  if isinstance(v,dict) and v.get('type') in ('tool_use','tool_result'):blocks.append({'timestamp':d['timestamp'],'messageUuid':d.get('uuid'),'block':v})
assert blocks;(dest/'tool-calls.json').write_text(json.dumps(blocks,indent=2)+'\n')
(dest/'custody.json').write_text(json.dumps({'standing':'Exact completed actual coauthor follow-up retained. Partial before/proposed/alternative source files, not a complete candidate copy. No independent acceptance.','sessionId':response['session_id'],'files':rows,'publicToolBlocks':{'path':'tool-calls.json','sha256':sha(dest/'tool-calls.json'),'count':len(blocks),'selection':'Public tool_use/tool_result since this follow-up process.startedAt, LF-only JSONL parsing; no private thinking.'}},indent=2)+'\n')
def ref(p):return {'path':str(p.relative_to(root)),'sha256':sha(p)}
integrated=[]
for issue,p,digest,basis in choices:
 row=changes[issue];q=root/row['path'];assert sha(q)==row['beforeSha256'];q.write_bytes(p.read_bytes());assert sha(q)==digest
 integrated.append({'id':issue,'path':row['path'],'beforeSha256':row['beforeSha256'],'afterSha256':digest,'basis':basis,'retainedSource':ref(dest/p.relative_to(src))})
receipt=own/'advisory-integration.v15.json';assert not receipt.exists();receipt.write_text(json.dumps({'standing':'Root adopts the exact Claude alternative for ADV1 and explicitly assented proposal for ADV2. Original technicalAssent=false on the first combined proposal remains unchanged.','changes':integrated,'actualAssessment':ref(dest/'assessment.json'),'rootAssent':True,'followupDispositions':{'FU-1':'Addressed by exact Claude alternative; original rejected proposal retained.','FU-2':'Addressed in v14-final-review-read.json; original review citation retained verbatim.','FU-3':'Still REQUIRED BEFORE successor freeze: refresh four pin manifests and execute six reference commands. This source integration does not discharge it.','FU-4':'Observation only, no severity or behavioral finding. No additional heading change is part of this narrow amendment.'},'freshIndependentAcceptance':False,'readinessChanged':False,'implementationAuthorized':False},indent=2)+'\n')
v4=read(own/'coauthor-assessment-bv4-v4.json');manifest=read(ev/'candidate-subject.v14.json');base={r['path']:r for r in manifest['files']};combined={r['path']:copy.deepcopy(r) for r in v4['sourceDelta']}
for r in integrated:
 if r['path'] in combined:assert combined[r['path']]['afterSha256']==r['beforeSha256'];combined[r['path']]['intermediateV4Sha256']=r['beforeSha256']
 else:combined[r['path']]={'path':r['path'],'beforeSha256':base[r['path']]['sha256']}
 combined[r['path']]['afterSha256']=r['afterSha256']
for rel,r in combined.items():assert r['beforeSha256']==base[rel]['sha256'] and sha(root/rel)==r['afterSha256']
assert len(combined)==6
sp=own/'successor-source-assessment.v15.json';assert not sp.exists();sp.write_text(json.dumps({'standing':'Root cumulative source assent to advance SIX exact source files from frozen v14 to fresh independent review. Original v4 and advisory assessments retain their literal scope/verdict.','finalSourceAssent':True,'independentAcceptance':False,'sourceDelta':list(combined.values()),'v4SourceAssessment':ref(own/'coauthor-assessment-bv4-v4.json'),'advisoryIntegration':ref(receipt),'actualAdvisoryAssessment':ref(dest/'assessment.json'),'actualPredecessorReviewRead':ref(own/'v14-final-review-read.json'),'remaining':['FU-3 final pin refresh and six reference commands before freeze','NEW independent design review of exact successor','NEW blind consumer','complete independently reviewed application/readiness reconciliation'],'implementationAuthorized':False,'readinessChanged':False},indent=2)+'\n')
review=read(ev/'post-reset-review.v14/review.json');assert review['newMustIssues']==review['newShouldIssues']==[]
accounts=[]
for idx,item in enumerate(review['newAdvisories']):
 change=next(r for r in integrated if r['id']==item['id']);accounts.append({'id':item['id'],'reviewEvidence':{**ref(ev/'post-reset-review.v14/review.json'),'selector':'/newAdvisories/'+str(idx)},'disposition':('Clarify the lawful deficiency/cause projection versus the four refusal-code additions later in the SAME section10. Adopt exact Claude alternative and preserve the independent review original incorrect section13 citation as history.' if item['id']=='V14-ADV-1' else 'Retain mandatory producer and retained-verifier enforcement; explicitly limit exhibited reference evidence to relation_payload_rules inside open_run_closure. No second producer call site or product conformance is claimed.'),'originalSeverity':'advisory','sourceCorrection':ref(root/change['path']),'actualCoauthorAssessment':ref(dest/'assessment.json'),'rootIntegration':ref(receipt),'standing':'Source corrected at original advisory severity; pending fresh independent acceptance and application.'})
account=own/'v14-review-and-v15-correction-assessment.json';assert not account.exists();account.write_text(json.dumps({'standing':'Actual completed v14 review and cumulative successor correction account. No acceptance extended across changed bytes.','reviewSha256':sha(ev/'post-reset-review.v14/review.json'),'actualVerdict':'ACCEPT','fullReadAccount':ref(own/'v14-final-review-read.json'),'allRequiredAddressedByV15Source':True,'requiredScope':'Vacuous only: actual v14 has zero MUST and zero SHOULD. Root corrections below are independently established and are not attributed to the v14 reviewer.','independentRequiredDispositions':[],'newAdvisoryApplicationAccounts':accounts,'additionalRootCorrections':[{'id':'CX-V14-ADMISSION-AVAILABILITY-MIRROR','status':'CORRECTED-PENDING-SUCCESSOR-REVIEW','disposition':'Admission1.1, native schema operationalCarrier and legacy-helper description now agree with original-invocation typed per-step availability, complete ownership and fixed matrix defaults.','evidence':ref(own/'coauthor-assessment-bv4-v4.json')},{'id':'CX-V14-ANALYSIS-SELECTION-LIMIT','status':'CORRECTED-PENDING-SUCCESSOR-REVIEW','disposition':'Complete default and explicit pre-Plan specs use the conditional actual-array bound before schema and vocabulary;94TSunits/1034rows or explicit1025 produce existing typed PROJECT.SCOPE_LIMIT. Five malformed-shape failures corrected. No Plan/Run for refused step, earlier invocation outcomes survive. Raw previous ValidationError is reference evidence, not a demonstrated host-emitted payload.','evidence':ref(own/'coauthor-assessment-bv4-v4.json')}],'cumulativeSourceAssessment':ref(sp),'implementationAuthorized':False,'readinessChanged':False},indent=2)+'\n')
print(json.dumps({'retainedFiles':len(rows),'publicToolBlocks':len(blocks),'integratedAdvisories':[r['id'] for r in integrated],'cumulativeSourceFiles':len(combined),'independentAcceptance':False},indent=2))
