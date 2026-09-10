"""Actual coauthor assessment of two narrowly scoped publication corrections; no live edits."""
from pathlib import Path
import json,hashlib,subprocess,datetime
root=Path.cwd();dc=root/'docs/coop/design-corrections';review=Path('/tmp/opensip-design-corrections/post-reset-review.v14/review.json')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
response=json.loads(review.with_name('response.json').read_text());assert response['is_error'] is False
rd=json.loads(review.read_text());assert rd['newMustIssues']==rd['newShouldIssues']==[]
assert {r['id'] for r in rd['newAdvisories']}=={'V14-ADV-1','V14-ADV-2'}
out=Path('/tmp/opensip-design-corrections/v14-advisory-clarification.v1');out.mkdir(exist_ok=False)
specs=[('V14-ADV-1','docs/v2/contracts/product-v1/native-evidence.md',
'`nativeCause`-carried rows. No new public code is added and none is needed.',
'`nativeCause`-carried rows. No new public code is added for this projection of a lawful entry\'s deficiency and cause. The refusal branches in section 13 separately add four public detail codes; those additions do not change this projection.'),
('V14-ADV-2','docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json',
'identity-model relation_payload_rules, on every owning fact, at the producer boundary and again at retained Run closure. It is checked before the relation\'s snapshot joins, so the cardinality fault is reported as itself rather than as a downstream join failure.',
'The producer must enforce this law on every owning fact, and the verifier must enforce it again at retained Run closure. The reference model exhibits the latter through identity-model relation_payload_rules inside open_run_closure; it does not exhibit a separate producer-boundary call site. Producer enforcement remains an implementation conformance obligation. At retained Run closure it is checked before the relation\'s snapshot joins, so the cardinality fault is reported as itself rather than as a downstream join failure.')]
rows=[]
for issue,rel,old,new in specs:
 p=root/rel;raw=p.read_text();assert raw.count(old)==1,rel
 before=out/'before'/rel;after=out/'proposed'/rel
 for q in [before,after]:q.parent.mkdir(parents=True,exist_ok=True)
 before.write_bytes(p.read_bytes());after.write_text(raw.replace(old,new))
 if rel.endswith('.json'):json.loads(after.read_text())
 rows.append({'id':issue,'path':rel,'beforeSha256':sha(before),'proposedSha256':sha(after),'old':old,'new':new})
(out/'proposal.json').write_text(json.dumps({'standing':'Root proposed publication clarification only; actual Claude technical assessment required before integration. Original two advisories retained at advisory severity.','reviewSha256':sha(review),'changes':rows},indent=2)+'\n')
prompt=f'''Resume as ACTUAL CLAUDE COAUTHOR, not independent reviewer. Your earlier v4 exact source was integrated without changes. A separate completed fresh independent v14 review {review} accepts its frozen subject with 0 MUST/SHOULD and two advisories. Read the exact review, especially V14-ADV-1/2, and {out}/proposal.json plus BOTH complete before/proposed files. Verify their hashes. Assess the two root-proposed wording corrections independently and substantively against their actual owning law and call sites in {root}/docs/coop/design-corrections/foundation/identity-model.py and public-detail-registry.v1.json. You may read root/coauthor v4 source assessment to distinguish current corrected source from v14 reviewed source. The proposal only scopes the already-existing public projection and distinguishes required producer enforcement from reference evidence of retained closure. It must not weaken producer obligation, invent a producer implementation, add a field/code/test, or alter admission semantics.
No source, pin, report, repository or frozen input edits. Write ONLY {out}/assessment.json and assessment.md (and any own inspection evidence under {out}). No subagents, product implementation, commits/pushes. No need to rerun the multi-minute whole suite for two non-executable strings; the successor final reference commands and NEW independent review will assess frozen bytes. If either exact proposal is wrong, explain and supply a precise alternative instead of assenting. Deliver technicalAssent boolean, proposalSha256, individually assessed changes with exact proposed file hashes and substantive rationale, requiredFollowup array, limitations. Preserve actual advisory severity; not design/independent/blind/application acceptance. Finish your bounded assessment now.'''
(out/'prompt.txt').write_text(prompt)
args=['/Users/sb/.local/bin/claude','-p','--resume','77758b10-d7ba-4868-9d42-ae0b13e84cb6','--model','opus','--effort','high','--permission-mode','dontAsk','--tools','Read,Grep,Glob,Write,Bash','--allowedTools','Read','Grep','Glob','Write','Bash','--strict-mcp-config','--output-format','json']
proc=subprocess.Popen(args,stdin=subprocess.PIPE,stdout=(out/'response.json').open('wb'),stderr=(out/'stderr.log').open('wb'),cwd=root,start_new_session=True);proc.stdin.write(prompt.encode());proc.stdin.close()
(out/'process.json').write_text(json.dumps({'pid':proc.pid,'startedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':args,'proposalSha256':sha(out/'proposal.json')},indent=2)+'\n');print(proc.pid)
