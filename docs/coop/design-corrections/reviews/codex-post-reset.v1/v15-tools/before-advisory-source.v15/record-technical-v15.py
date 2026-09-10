"""Prepared only: retain actual final checks and completed source account; no independent acceptance."""
from pathlib import Path
import json,hashlib,shutil
root=Path.cwd();dc=root/'docs/coop/design-corrections';ev=dc/'reviews/codex-post-reset.v1';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();read=lambda p:json.loads(p.read_text())
a=read(ev/'coauthor-assessment-bv4-v4.json');assert a['finalSourceAssent'] is True
src=Path('/tmp/opensip-design-corrections/final-reference-v15-complete');report=read(src/'reference-checks.json');assert report['passed'] and len(report['commands'])==6 and all(r['exitCode']==0 for r in report['commands']);dest=ev/'final-reference.v15';assert not dest.exists();shutil.copytree(src,dest)
summary=read(dc/'validation-summary.v1.json');assert summary['native']['matrixCells']==66 and summary['claudeFinalReview']=='PENDING-FROZEN-V15'
rows=[]
for row in a['sourceDelta']:
 p=root/row['path'];assert sha(p)==row['afterSha256'];rows.append({'path':row['path'],'beforeSha256':row['beforeSha256'],'coauthorSha256':row['afterSha256'],'finalSha256':sha(p)})
for rel in ['integration-fixtures.py','correction-crosswalk.proposed.json','foundation/source-pins.v1.json','security/source-pins.v1.json','native/source-pins.v2.json','workflows/source-pins.v1.json','validation-summary.v1.json']:
 p=dc/rel;rows.append({'path':str(p.relative_to(root)),'finalSha256':sha(p),'rootOwned':True})
def ref(p):return {'path':str(p.relative_to(root)),'sha256':sha(p)}
p=ev/'final-source-account.v15.json';assert not p.exists();p.write_text(json.dumps({'standing':'Exact coauthor integration, source-bound shared construction fixture and current recording/pins. Fresh independent acceptance pending.','files':rows,'sourceAssessment':ref(ev/'coauthor-assessment-bv4-v4.json'),'actualPredecessorReviewAssessment':ref(ev/'v14-review-and-v15-correction-assessment.json'),'actualFinalCommands':ref(dest/'reference-checks.json')},indent=2)+'\n')
body='''# Codex final v15 correction assessment

Codex assents to advancing the exact corrected design/reference source to fresh independent review. This is coauthor/integration assent, not independent acceptance, blind reconstructability, application acceptance or implementation readiness.

Actual Claude session77758b10-d7ba-4868-9d42-ae0b13e84cb6 completed the fourth coauthor pass using claude-opus-5. Its full final handoff, numbered checkpoints, failed attempts, source-copy accounts and public-tool custody are retained in ../bv4-corrections-author.v4/. Codex's exact source assessment and independent boundary probes are linked in coauthor-assessment-bv4-v4.json. Original rejected source, initial test failures and later corrections remain distinguishable.

The admission paragraph, native route annotation and legacy-helper description now agree on the original invocation's per-step typed capability-availability account. Generic environment details cannot substitute for that complete account. The release registry describes availability; the capability matrix fixes the full-product default, and explicit overrides retain their provenance.

The complete pre-Plan analysis-spec boundary covers both default and explicit selections. Actual arrays over the published bound receive the existing PROJECT.SCOPE_LIMIT refusal, with field/count/limit, request-rejected classification and a schema-admitted complete failure envelope. Other shapes retain schema validation; a string is not counted as a capability array. The meaning explicitly covers four bounded fields across two record families. Existing defaults and bounds remain fixed, with explicit narrowing as the remedy. No Plan/Run is minted for the refused analysis step; request/invocation attribution and any earlier committed outcomes remain. Retained Run payload validation keeps its existing admission order and authority.

These are executable design-reference controls with synthetic input and schema composition. They do not demonstrate a real host, renderer, compiler, operating system, storage or cryptographic implementation. The exact failed and corrected malformed-input cases and valid boundary controls are accounted in the source assessment. The inherited Bv4 anchor/inventory, body-language, cause-carrier and public projection evidence keeps its original measured scope; carrying it is not a claim to have re-executed every prior probe.

The current correction crosswalk, dispositions, advisory accounts and README were updated before the reference pins. The shared integration fixture retains its exact source digest and an explicit construction-only declaration interface; it provides no independent expected verdict. The completed predecessor review and every finding/advisory are individually accounted in v14-review-and-v15-correction-assessment.json. No prior review is extended to these successor bytes by inference.

All six final source-pinned reference commands pass. The following values are actual passing calls/cases and reported counts, not exhaustive coverage or product qualification. Full exits and logs are retained in final-reference.v15/. Final live and copied pins must also verify after all recording.

'''
body+='```json\n'+json.dumps({k:summary[k] for k in ['foundation','security','native','workflows','integration']},indent=2)+'\n```\n\n'
body+='Remaining: fresh independent Claude review of frozen v15 with zero unresolved MUST/SHOULD; a NEW blind consumer on those accepted normative inputs; complete independently reviewed application and readiness reconciliation. All32 product qualification gates remain undemonstrated. No implementation, commit or push is authorized.\n'
p=ev/'technical-review.v15.md';assert not p.exists();p.write_text(body)
helpers=['retain-bv4-corrections-author-v4.py','probe-bv4-v4-preflight.py','review-bv4-v4-checkpoint1.py','review-bv4-v4-checkpoint2.py','review-bv4-v4-checkpoint3.py','recover-bv4-v4-checkpoint3-metadata.py','review-bv4-v4-checkpoint3-final.py','record-bv4-v4-final-handoff-read.py','assess-integrate-bv4-author-v4.py','adapt-integration-builder-v15.py','prepare-records-v15.py','refresh-pins-v6.py','run-final-v15.py','record-v15.py','record-technical-v15.py','launch-review-v15.py']
td=ev/'v15-tools';td.mkdir(exist_ok=False)
for name in helpers:shutil.copy2(Path(__file__).parent/name,td/name)
print('Retained final six commands, exact source account and technical assessment; independent review pending.')
