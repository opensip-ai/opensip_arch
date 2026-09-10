"""Retain measured final evidence and root's exact v17 source account after execution."""
from pathlib import Path
import hashlib,json,shutil
root=Path.cwd();dc=root/'docs/coop/design-corrections';ev=dc/'reviews/codex-post-reset.v1';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();load=lambda p:json.loads(p.read_text())
a=load(ev/'successor-source-assessment.v17.json');assert a['finalSourceAssent'] is True and a['independentAcceptance'] is False
src=Path('/tmp/opensip-design-corrections/final-reference-v17-complete');report=load(src/'reference-checks.json')
assert report['passed'] and len(report['commands'])==6 and all(x['exitCode']==0 for x in report['commands'])
dest=ev/'final-reference.v17';assert not dest.exists();shutil.copytree(src,dest)
summary=load(dc/'validation-summary.v1.json');assert summary['claudeFinalReview']=='PENDING-FROZEN-V17' and summary['native']['qualifiedCells']==0
rows=[]
for row in a['sourceDelta']:
 p=root/row['path'];assert sha(p)==row['afterSha256'];rows.append({'path':row['path'],'beforeSha256':row['beforeSha256'],'coauthorSha256':row.get('coauthorSha256',row['afterSha256']),'finalSha256':sha(p)})
for rel in ['integration-fixtures.py','correction-crosswalk.proposed.json','foundation/source-pins.v1.json','security/source-pins.v1.json','native/source-pins.v2.json','workflows/source-pins.v1.json','validation-summary.v1.json']:
 p=dc/rel;rows.append({'path':str(p.relative_to(root)),'finalSha256':sha(p),'rootOwnedRecording':True})
ref=lambda p:{'path':str(p.relative_to(root)),'sha256':sha(p)}
p=ev/'final-source-account.v17.json';assert not p.exists();p.write_text(json.dumps({'standing':'Exact corrected source and measured reference evidence; fresh independent acceptance pending.','files':rows,'sourceAssessment':ref(ev/'successor-source-assessment.v17.json'),'actualBlindRootAssessment':ref(ev/'blind-assessment.v6.json'),'actualFinalCommands':ref(dest/'reference-checks.json')},indent=2)+'\n')
body="""# Codex final v17 correction assessment

Codex assents to advancing these exact corrected architecture/design/reference bytes to fresh independent review. This is coauthor/integration assent, not independent acceptance, blind reconstructability, application acceptance or implementation readiness.

The completed actual-Claude blind v6 review found two MUST and two SHOULD issues after the earlier v16 design ACCEPT. Its original review, reconstruction and failed attempts remain unchanged. The [root blind assessment](blind-assessment.v6.json) records the substantive findings and the limits of the synthetic and incompletely closed fixtures.

Actual Claude correction coauthor session 4b48ccdd-92fb-4f92-9db2-ac8942f796d6 proposed the exact source recorded in [the root source assessment](successor-source-assessment.v17.json). That record names the released handoff, source-copy custody, root controls and every finding disposition. Earlier rejected coauthor passes and their claims remain historical evidence. Root read the final changed bytes and assessed the substantive evidence before integration; no agreement is inferred from a verdict alone.

The corrections separate native and imported per-requirement causes, define the TypeScript configuration-node name, publish command/step/receipt operation and key bindings, and enforce the existing per-view coverage-partition rule at retained Run closure. They also define how fingerprint repair targets project to imported subjects, the imported per-kind outcomes and partial-support semantics, and the owning receipt lookup and authorization boundaries. Additional clarifications preserve observation bounds, native closed-world prerequisites and original-run evidence. The source assessment owns the exact final dispositions, selected design clarifications and evidence limits; original finding severities remain unchanged.

Reference checks do not qualify a product host, compiler, ledger, runtime collector, renderer or platform. Helper/schema checks are distinguished from actual retained-Run closure controls. Editing a committed schema document changes its digest and may change fixture identities; historical manifests and their exact source remain immutable.

Current routing, dispositions, README and advisory account were recorded before refreshing source pins. All six final source-pinned reference commands executed successfully. The measured values below describe reference calls/cases, not exhaustive coverage or product qualification. A separate freeze must still verify live and copied pins after all recording.

"""
body+='```json\n'+json.dumps({k:summary[k] for k in ['foundation','security','native','workflows','integration']},indent=2)+'\n```\n\n'
body+='Remaining: fresh independent Claude review of frozen v17 with zero unresolved MUST/SHOULD, a NEW blind consumer on those accepted normative bytes, and complete independently reviewed application/readiness reconciliation. All32 qualification gates remain unperformed. No implementation, commit or push is authorized.\n'
p=ev/'technical-review.v17.md';assert not p.exists();p.write_text(body)
td=ev/'v17-tools';assert not td.exists();td.mkdir()
names=['prepare-records-v17.py','refresh-pins-v6.py','run-final-v17.py','record-v17.py','record-technical-v17.py','freeze-next.py','launch-review-v17.py','launch-consumer-b-v7.py','assess-integrate-bv6-v17.py','retain-bv6-corrections-author-v3.py','launch-bv6-corrections-author-v3.py','retain-bv6-corrections-author-v4.py','launch-bv6-corrections-author-v4.py','prepare-bv6-root-polish-v1.py','finalize-bv6-root-polish-v1.py','run-bv6-final-probes-v17.py','probe-bv6-final-v3-imported.py','launch-bv6-corrections-author-v5.py','retain-bv6-corrections-author-v5.py','launch-bv6-corrections-author-v6.py','retain-bv6-corrections-author-v6.py']
for name in names:shutil.copyfile(Path(__file__).parent/name,td/name)
print('Retained six executed commands and exact source/technical account; independent review pending.')
