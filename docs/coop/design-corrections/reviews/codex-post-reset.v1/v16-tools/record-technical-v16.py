"""Retain measured final evidence and root's exact v16 source account after execution."""
from pathlib import Path
import hashlib,json,shutil
root=Path.cwd();dc=root/'docs/coop/design-corrections';ev=dc/'reviews/codex-post-reset.v1';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();load=lambda p:json.loads(p.read_text())
a=load(ev/'successor-source-assessment.v16.json');assert a['finalSourceAssent'] is True and a['independentAcceptance'] is False
src=Path('/tmp/opensip-design-corrections/final-reference-v16-complete');report=load(src/'reference-checks.json')
assert report['passed'] and len(report['commands'])==6 and all(x['exitCode']==0 for x in report['commands'])
dest=ev/'final-reference.v16';assert not dest.exists();shutil.copytree(src,dest)
summary=load(dc/'validation-summary.v1.json');assert summary['claudeFinalReview']=='PENDING-FROZEN-V16' and summary['native']['qualifiedCells']==0
rows=[]
for row in a['sourceDelta']:
 p=root/row['path'];assert sha(p)==row['afterSha256'];rows.append({'path':row['path'],'beforeSha256':row['beforeSha256'],'coauthorSha256':row.get('coauthorSha256',row['afterSha256']),'finalSha256':sha(p)})
for rel in ['integration-fixtures.py','correction-crosswalk.proposed.json','foundation/source-pins.v1.json','security/source-pins.v1.json','native/source-pins.v2.json','workflows/source-pins.v1.json','validation-summary.v1.json']:
 p=dc/rel;rows.append({'path':str(p.relative_to(root)),'finalSha256':sha(p),'rootOwnedRecording':True})
ref=lambda p:{'path':str(p.relative_to(root)),'sha256':sha(p)}
p=ev/'final-source-account.v16.json';assert not p.exists();p.write_text(json.dumps({'standing':'Exact corrected source and measured reference evidence; fresh independent acceptance pending.','files':rows,'sourceAssessment':ref(ev/'successor-source-assessment.v16.json'),'actualBlindRootAssessment':ref(ev/'blind-assessment.v5.json'),'actualFinalCommands':ref(dest/'reference-checks.json')},indent=2)+'\n')
body='''# Codex final v16 correction assessment

Codex assents to advancing these exact corrected architecture/design/reference bytes to fresh independent review. This is coauthor/integration assent, not independent acceptance, blind reconstructability, application acceptance or implementation readiness.

The completed actual-Claude blind v5 review found two MUST and two SHOULD issues after the earlier v15 design ACCEPT. Its original review, independently authored reconstruction and failed attempts remain unchanged. The [root blind assessment](blind-assessment.v5.json) records the substantive findings and precise limits of the reported counts, placeholders and synthetic evidence.

A fresh actual-Claude correction coauthor, session f6955666-0878-461a-a4e1-2ca2c4f5e824, proposed the exact source recorded in [the root source assessment](successor-source-assessment.v16.json). The [actual handoff](../bv5-corrections-author.v2/handoff.json), source-copy deltas and public tools retain its substantive assent and limitations. The first coauthor pass remains separately retained with root rejection; the actual same-session follow-up addresses the full-Run counterexamples and precise contract corrections. Root reviewed the exact changed bytes before integration; the source assessment owns every required/advisory disposition and any separately assessed follow-up.

The corrections explicitly select the scoped capability-manifest admission registry, define TypeScript library names' mapping to retained declaration components, state coverage applicability for registered relation/rung pairs, and define the repair descriptor's projection from original full native evidence. The projection cannot replace the original evidence prerequisite. Additional source assessment covers relation-specific coverage admission and contradictory not-applicable records at producer and retained Run closure, alongside the remaining root and coauthor findings. Accompanying advisory clarifications distinguish concrete digest representations from their selector, direct path-schema use from joined validation, inherited L0 length framing, the inherited platform vocabulary from selected product platforms, and cardinality-first request admission from the later schema stage. Every earlier finding retains its original severity and historical evidence.

The exact source account and handoff describe the actual changed files and controls; passing reference tests is not evidence of a real compiler, host, renderer, ledger, operating system, signature verification or supported-platform qualification. Schema-document edits change their byte digests where those digests are identity inputs; this is not a claim that changed source bytes have identical identities. Historical manifests and accepted source remain immutable.

Current routing, dispositions, README and advisory account were recorded before refreshing source pins. All six final source-pinned reference commands executed successfully. Values below are measured calls/cases and recorded scope, not exhaustive test coverage or product qualification. The separate freeze must still verify live and copied pins after all recording.

'''
body+='```json\n'+json.dumps({k:summary[k] for k in ['foundation','security','native','workflows','integration']},indent=2)+'\n```\n\n'
body+='Remaining: fresh independent Claude review of frozen v16 with zero unresolved MUST/SHOULD, a NEW blind consumer on those accepted normative bytes, and complete independently reviewed application/readiness reconciliation. All32 qualification gates remain unperformed. No implementation, commit or push is authorized.\n'
p=ev/'technical-review.v16.md';assert not p.exists();p.write_text(body)
td=ev/'v16-tools';assert not td.exists();td.mkdir()
names=['launch-bv5-corrections-author-v1.py','retain-bv5-corrections-author-v1.py','launch-bv5-corrections-author-v2.py','retain-bv5-corrections-author-v2.py','assess-bv5-author-v1.py','probe-bv5-rc1-full-run.py','assess-blind-v5.py','prepare-records-v16.py','refresh-pins-v6.py','run-final-v16.py','record-v16.py','record-technical-v16.py','freeze-next.py','launch-review-v16.py']
names += ['assess-integrate-bv5-v16.py','run-bv5-final-probes-v16.py','probe-bv5-resolved-classes.py','probe-bv5-scope-membership.py','probe-bv5-draft-rc1.py']
for name in names:shutil.copyfile(Path(__file__).parent/name,td/name)
print('Retained six executed commands and exact source/technical account; independent review pending.')
