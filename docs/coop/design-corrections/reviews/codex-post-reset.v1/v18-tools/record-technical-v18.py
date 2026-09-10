from pathlib import Path
import json,hashlib,shutil
root=Path.cwd();dc=root/'docs/coop/design-corrections';own=dc/'reviews/codex-post-reset.v1';tmp=Path('/tmp/opensip-design-corrections');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();load=lambda p:json.loads(p.read_text());ref=lambda p:{'path':str(p.relative_to(root)),'sha256':sha(p)}
a=load(own/'successor-source-assessment.v18.json');assert a['finalSourceAssent'] and a['independentAcceptance'] is False
src=tmp/'final-reference-v18-complete';commands=load(src/'reference-checks.json');assert commands['passed'] and len(commands['commands'])==6 and all(x['exitCode']==0 for x in commands['commands']);dest=own/'final-reference.v18';assert not dest.exists();shutil.copytree(src,dest)
summary=load(dc/'validation-summary.v1.json');assert summary['claudeFinalReview']=='PENDING-FROZEN-V18';assert summary['native']['qualifiedCells']==0
rows=[]
for row in a['sourceDelta']:
 p=root/row['path'];assert sha(p)==row['afterSha256'];rows.append({'path':row['path'],'beforeSha256':row['beforeSha256'],'finalSha256':sha(p)})
for rel in ['correction-crosswalk.proposed.json','foundation/source-pins.v1.json','security/source-pins.v1.json','native/source-pins.v2.json','workflows/source-pins.v1.json','validation-summary.v1.json']:
 p=dc/rel;rows.append({'path':str(p.relative_to(root)),'finalSha256':sha(p),'rootOwnedRecording':True})
p=own/'final-source-account.v18.json';assert not p.exists();p.write_text(json.dumps({'standing':'Exact mutually assessed checker correction and executedsixreferencecommands; freshindependent18pending.','files':rows,'sourceAssessment':ref(own/'successor-source-assessment.v18.json'),'priorIndependentRootAssessment':ref(own/'review-assessment.v17.json'),'actualFinalCommands':ref(dest/'reference-checks.json')},indent=2)+'\n')
body='''# Codex v18 correction assessment

Codex and actual Claude agree that the ten expected-refusal guards correctly repair the reference checker. An absent expected-refusal key now fails when an exception occurs; an explicit null-detail expectation still works. No product contract, schema, model or case expectation changes. [The source assessment](successor-source-assessment.v18.json) binds exact bytes and [the coauthor assessment](coauthor-assessment-v18-checker.v1.json) records evidence and report qualifications. This is source/coauthor assent, not independent acceptance or readiness.

The actual independent v17 reviewer preserved its ACCEPT with three advisories after substantive report corrections. Codex required correction of the demonstrated false-pass weakness before promotion; the actual source coauthor independently recommended SHOULD severity and assented to the exact proposal. Both original judgments remain intact. [The v17 root assessment](review-assessment.v17.json) explains the decision and remaining reporting limits.

Root executed the ten actual exception-handler bodies under five controlled outcomes each on both versions: 100 synthetic controls, ten old false passes and no proposed mismatches. A separate whole-AST comparison, after removing only the ten new guards, exactly reproduces the old AST. Actual Claude independently forced a real model refusal by removing the target from a synthetic evidence Run: the old checker passed the case, while the proposal failed exactly that case. Both versions pass the unchanged 1787-check corpus. All ten handlers execute in that corpus (46 line hits); reachability is distinct from discrimination. These are reference-model/checker controls, not production Run or host enforcement.

The coauthor ran the direct checker in explicitly partial disposable copies without exercising pin validation. Root subsequently updated routing and source pins and executed all six canonical commands below. The source assessment preserves the coauthor's null diagnostic observation as nonblocking reference convenience, with correct failure and case identity already present.

The new prospective advisory account preserves 58 individual original severities and histories. It explicitly labels the historical V14-ADV-2 source digest and binds the current document. Imported applicability is selected by registered relation key; its prose rule remains metadata. No silent schema patch changes accepted identities. The complete application review still must assess and apply these records.

Measured reference results, not exhaustive coverage or qualification:

'''
body+='```json\n'+json.dumps({k:summary[k] for k in ['foundation','security','native','workflows','integration']},indent=2)+'\n```\n\n'
body+='All31 protected historical files remain unchanged. Final live and copied source-pin verification after all recording is mandatory. Remaining work: fresh independent acceptance of frozen18, a NEW blind consumer on those normative bytes, and complete independently reviewed application/readiness reconciliation. All32 qualification gates remain unperformed; D372 and condition5 remain unapplied/not met. No implementation, commit or push is authorized.\n'
p=own/'technical-review.v18.md';assert not p.exists();p.write_text(body)
td=own/'v18-tools';td.mkdir(exist_ok=False)
for n in ['prepare-v18-checker-proposal.py','launch-v18-checker-coauthor.py','retain-review-clarification-v17.py','retain-v18-checker-coauthor.py','integrate-record-v18.py','refresh-pins-v6.py','run-final-v18.py','record-v18.py','record-technical-v18.py','freeze-next.py','launch-review-v18.py','launch-consumer-b-v7.py']:
 shutil.copyfile(tmp/'codex-post-reset.v1'/n,td/n)
print('Retained actual final18six-command evidence and technical assessment; fresh review pending.')
