"""Retain actual final checks and completed correction account; no independent acceptance."""
from pathlib import Path
import json,hashlib,shutil
root=Path.cwd();dc=root/'docs/coop/design-corrections';ev=dc/'reviews/codex-post-reset.v1';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();read=lambda p:json.loads(p.read_text())
a=read(ev/'coauthor-assessment-bv4-v3.json');assert a['finalSourceAssent'] is True
src=Path('/tmp/opensip-design-corrections/final-reference-v14-complete');report=read(src/'reference-checks.json');assert report['passed'] and len(report['commands'])==6 and all(r['exitCode']==0 for r in report['commands'])
dest=ev/'final-reference.v14';assert not dest.exists();shutil.copytree(src,dest)
editorial=read(ev/'publication-shorthand-v14/account.json')
for row in editorial['changes']:assert sha(root/row['path'])==row['afterSha256']
summary=read(dc/'validation-summary.v1.json');assert summary['native']['matrixCells']==66 and summary['claudeFinalReview']=='PENDING-FROZEN-V14'
rows=[]
for row in a['sourceDelta']:
 p=root/row['path'];rows.append({'path':row['path'],'beforeSha256':row['beforeSha256'],'coauthorSha256':row['afterSha256'],'finalSha256':sha(p)})
for rel in ['integration-fixtures.py','correction-crosswalk.proposed.json','foundation/source-pins.v1.json','security/source-pins.v1.json','native/source-pins.v2.json','workflows/source-pins.v1.json','validation-summary.v1.json']:
 p=dc/rel;rows.append({'path':str(p.relative_to(root)),'finalSha256':sha(p),'rootOwned':True})
(ev/'final-source-account.v14.json').write_text(json.dumps({'standing':'Exact coauthor integration plus mutually assessed root publication corrections, shared synthetic fixture and current recording/pins. Fresh independent acceptance pending.','files':rows,'publicationCorrectionAccount':{'path':str((ev/'publication-shorthand-v14/account.json').relative_to(root)),'sha256':sha(ev/'publication-shorthand-v14/account.json')},'actualFinalCommands':{'path':str((dest/'reference-checks.json').relative_to(root)),'sha256':sha(dest/'reference-checks.json')}},indent=2)+'\n')
body='''# Codex final v14 correction assessment

The Bv4 corrections and both remaining publication joins are completed in the candidate. This is Codex coauthor/integration assent to advance exact final source to fresh independent review; it is not independent acceptance, blind reconstructability, application acceptance or implementation readiness.

Actual Claude session77758b10-d7ba-4868-9d42-ae0b13e84cb6 completed the third coauthor pass using claude-opus-5. The full final handoff and public-tool custody are retained in ../bv4-corrections-author.v3/. The final source assessment, exact checkpoint feedback and independently written root probes are in coauthor-assessment-bv4-v3.json and bv4-v3-checkpoint1 through5. Original rejected source, failures, root harness errors and inaccurate intermediate claims remain available with additive corrections.

The substantive corrections preserve relation-specific anchor bounds, raw inventory digest/length/path ownership and per-universe totality; typed deficiency support and types-only derivation cause; actual clone body language; the matrix-fixed product default independently of installed availability; and existing unsupported-language precedence. Prior complete Run controls and their synthetic-input limitations remain explicitly cited, without pretending the current publication-only probes regrade unchanged paths.

The original invocation now carries a per-step collection of typed capability/mode/workspace absence notices. Two admitted1023request selections yield2046notices without truncation. Every analysis command declares the availability projection, including repair-verify, and missing required fields refuse instead of returning partial output. Candidate-only absences fabricate neither Coverage nor candidates and grant no repair/Control authority.

Actual guards normalize registered keys and values into origin-aware public termination and full schema-admitted failure envelopes. Four precise public detail codes join the existing registry. One selected host-invariant cause maps to the existing SYSTEM.OUTCOME.ILLEGAL_STATE while preserving historical D9 and all inherited mappings. Long diagnostic projection counts Unicode code points and hashes exact unnormalized UTF8 bytes. Root's24non-ASCII boundary controls admit and match independently computed projections; its initial950-versus949 expectation error is preserved separately.

Claude read and substantively agreed all three exact root-owned publication replacements. Root applied them with before-images: correct the helper leaf before adding stepId, name all five analysis commands in native1.4, and name the typed notice carrier in the native schema annotation. The omitted fifth command was a residual current-prose inconsistency, not an optional shorthand choice. These changes are complete before pins and final review; coauthor custody remains bound to the earlier submitted bytes, while the final-source account identifies these root changes.

The shared integration fixture is extracted through an explicit54-declaration interface from the final coauthor checker with its source hash, and copies construction data only, never independent expected verdicts. Current crosswalk/README/dispositions and43historical advisory accounts were updated before refreshing pins. The successor validation summary now measures66matrixcells; the stale60v13record remains immutable history. All32qualification gates remain unperformed.

All six actual final reference commands pass. Counts below are passing calls/reference cases, not exhaustive coverage, distinct tests or real platform qualification. Complete command source hashes, exits and logs are retained in final-reference.v14/. Final pin integrity must also pass after all recording and again on the copied frozen subject.

'''
body+='```json\n'+json.dumps({k:summary[k] for k in ['foundation','security','native','workflows','integration']},indent=2)+'\n```\n\n'
body+='Remaining: fresh independent Claude review of the newly frozen candidate with zero unresolved MUST/SHOULD; a NEW blind consumer on those accepted normative inputs; complete independently reviewed application/readiness reconciliation. No product implementation, commit or push is authorized.\n'
p=ev/'technical-review.v14.md';assert not p.exists();p.write_text(body)
helpers=['retain-bv4-corrections-author-v3.py','review-bv4-author-v3-checkpoint4.py','review-bv4-author-v3-checkpoint5.py','probe-bv4-v3-checkpoint5-unicode.py','assess-integrate-bv4-author-v3.py','adapt-integration-builder-v14.py','prepare-records-v14.py','reconcile-publication-shorthand-v14.py','refresh-pins-v6.py','run-final-v14.py','record-v14.py','record-technical-v14.py','launch-review-v14.py']
tool_dest=ev/'v14-tools';tool_dest.mkdir(exist_ok=False)
for name in helpers:
 p=Path(__file__).parent/name;q=tool_dest/name
 if q.exists():assert sha(p)==sha(q),name
 else:shutil.copy2(p,q)
print('Retained final six commands, exact final source account and completed technical assessment; independent review pending.')
