from pathlib import Path
import json,hashlib,datetime
root=Path.cwd();ev=root/'docs/coop/design-corrections/reviews';b=ev/'post-reset-review.v14';out=ev/'codex-post-reset.v1/v14-final-review-read.json';assert not out.exists()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();r=json.loads((b/'review.json').read_text());response=json.loads((b/'response.json').read_text())
assert sha(b/'review.json')=='857b2e3a1342c79146bf09f4c598fcd31d26995e16b96b0faa3c4deab8bd84a1'
assert sha(b/'review.md')=='947c5ed547d5393cb01c9cd07301b3cf81c00e419aa432a3fc1b8ad77a87cd30'
assert response['is_error'] is False and response['session_id']=='46ea25c0-21fc-4be6-9b57-61e46c61d64d'
assert r['overallVerdict']=='ACCEPT' and r['newMustIssues']==r['newShouldIssues']==[]
copies=json.loads((b/'source-copy-accounts.json').read_text());assert set(copies)=={'work'};cp=copies['work'];assert cp['actualFiles']==len(cp['unchangedFiles'])==6047 and cp['changedFiles']==cp['addedFiles']==cp['deletedFiles']==[]
probes=[]
for name,reported in r['independentProbes'].items():
 p=b/'evidence'/name;d=json.loads(p.read_text());assert d['allHold'] is True and not d['failed'] and len(d['probes'])==reported['cases'] and all(x['holds'] is True for x in d['probes'])
 probes.append({'path':str(p.relative_to(root)),'sha256':sha(p),'finalCases':len(d['probes'])})
assert sum(p['finalCases'] for p in probes)==r['independentProbeCaseTotal']==212
for kind,count in [('arDispositions',16),('fwDispositions',15),('inheritedResidualDispositions',27),('scopedReviewOwnerDispositions',5)]:assert len(r[kind])==count
out.write_text(json.dumps({'standing':'Root full-read assessment of the actual completed independent v14 review. Its ACCEPT belongs only to frozen v14; successor source still requires fresh independent review.','recordedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'review':{'path':str((b/'review.json').relative_to(root)),'sha256':sha(b/'review.json'),'mdSha256':sha(b/'review.md'),'sessionId':response['session_id'],'actualVerdict':'ACCEPT','newMustIds':[],'newShouldIds':[],'newAdvisoryIds':['V14-ADV-1','V14-ADV-2']},'fullRead':True,'finalProbeAccount':probes,'frozenWorkCopyUnchangedFiles':6047,'precisionAndLimits':[
'The final212rows all hold. Earlier harness mistakes, unconstructible control-flow/literal payloads, and unreachable half-matching universe premises are retained, not silently counted as successful original cases.',
'Retained Run closure is demonstrated for the joined anchor/inventory and language cases; native coverage producer admission and retained closure are independently exercised for cause carriers. The headline wording is not interpreted as two-boundary execution for every one of the212rows.',
'p8_delivery.py H2 directly demonstrates pure renderer failure on missing parity; H4 inspects the mapper/code enum. That probe does not execute a host fault projection, commit a Run or demonstrate preservation in a real invocation. Inherited suite evidence and the normative required-output law retain their actual separate scope.',
'p4c_bounds.py demonstrates typed field retention and helper counts, equal schema bounds and forced schema refusals. It does not exercise the root-confirmed ordinary oversized default/explicit request boundary corrected after the v14 freeze.',
'V14-ADV-1 correctly identifies projection versus refusal scope. Its section13 citation is inaccurate: the four-code paragraph at2376 is within section10, under Admission and event routes; section13 Joins starts2750 in frozenv14. Original review stays unchanged. The clarification must use the actual subsection.',
'V14-ADV-2 correctly distinguishes mandatory producer enforcement from the retained-closure call site exhibited by the reference. No actual compiler/host/OS/storage/crypto/renderer qualification is inferred.',
'16AR and15FW carry-only with gradedByThisReviewfalse;27inherited and30evaluation preservation-only;5owners routing-only with gradedfalse. No application grade or readiness effect is inferred.',
'The independently confirmed root availability-mirror and pre-Plan selection issues were found after v14 freeze and already corrected in separate actual coauthor v4 source. They are not discoveries or closures attributed to this v14 reviewer. Therefore no design-assent.v14 or blind promotion on this older subject is issued.'
],'successorIndependentAcceptance':False,'blindAccepted':False,'applicationAccepted':False,'readinessChanged':False,'implementationAuthorized':False},indent=2)+'\n')
print(str(out))
