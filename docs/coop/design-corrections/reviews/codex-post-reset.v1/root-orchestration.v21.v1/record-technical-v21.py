"""Retain final measured21 source/reference/environment evidence before freeze."""
from pathlib import Path
import json,hashlib,shutil,subprocess
root=Path('/Users/sb/code/opensip-ai/opensip_arch');dc=root/'docs/coop/design-corrections';own=dc/'reviews/codex-post-reset.v1';tmp=Path('/tmp/opensip-design-corrections');load=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();ref=lambda p:{'path':str(p.relative_to(root)),'sha256':sha(p)}
a=load(own/'successor-source-assessment.v21.json');assert a['finalSourceAssent'] and not a['independentAcceptance']
executed=tmp/'final-reference-v21-complete';commands=load(executed/'reference-checks.json');assert commands['passed'] and len(commands['commands'])==6 and all(x['exitCode']==0 for x in commands['commands'])
dest=own/'final-reference.v21';assert not dest.exists();shutil.copytree(executed,dest)
environment=subprocess.run(['/tmp/opensip-architecture-review-env/bin/python','-I','-B','-c',"import sys,unicodedata,importlib.metadata,json;print(json.dumps({'python':sys.version,'executable':sys.executable,'unicodeData':unicodedata.unidata_version,'jsonschema':importlib.metadata.version('jsonschema'),'referencing':importlib.metadata.version('referencing')}))"],capture_output=True,text=True,check=True)
env=json.loads(environment.stdout);assert env['unicodeData']=='15.0.0';(dest/'environment.json').write_text(json.dumps(env,indent=2)+'\n')
summary=load(dc/'validation-summary.v1.json');assert summary['claudeFinalReview']=='PENDING-FROZEN-V21' and summary['native']['qualifiedCells']==0
rows=[]
for row in a['sourceDelta']:
 p=root/row['path'];assert sha(p)==row['afterSha256'];rows.append({'path':row['path'],'beforeSha256':row['beforeSha256'],'finalSha256':sha(p)})
for rel in ['correction-crosswalk.proposed.json','foundation/source-pins.v1.json','security/source-pins.v1.json','native/source-pins.v2.json','workflows/source-pins.v1.json','validation-summary.v1.json']:
 p=dc/rel;rows.append({'path':str(p.relative_to(root)),'finalSha256':sha(p),'rootOwnedRecording':True})
p=own/'final-source-account.v21.json';assert not p.exists();p.write_text(json.dumps({'standing':'Exact mutually assessed three-file reference correction; six source-pinned commands passed. Independent21, NEWblind9 and complete application pending.','files':rows,'sourceAssessment':ref(own/'successor-source-assessment.v21.json'),'actualFinalCommands':ref(dest/'reference-checks.json'),'actualEnvironment':ref(dest/'environment.json')},indent=2)+'\n')
body='''# Codex source21 correction assessment

Actual Claude and Codex agree on the exact three-file reference correction. The scope-selection model's executable behavior is unchanged: the guard already refused ambiguity before payload matching. Five new controls now discriminate an unrelated but valid third scope document under zero, one and multiple selected parameters, and preserve successful binding when that document is selected. A pure guard-transposition mutation fails exactly two controls (1594passed/2failed); the final identity checker measures1596passed/0failed,1584distinct IDs and12historical duplicate extra instances. The redundant source-text-count assertion was removed while substantive public registry/carrier admission checks remain. Comments distinguish why the guard exists, why its position matters and the earlier canonicalization boundary.

The foundation launcher now catches child timeouts, decodes captured partial bytes and writes an explicit failed aggregate instead of leaving the prior success report as its apparent result. A timed-out entry declines attribution of any child report, even if old or partial bytes exist. The report extends the previous fields. Its fixed600second per-child reference budget is not product timeout or authorization law, and five child budgets do not bound whole-run wall time. Root's final orchestration permits3600seconds for this wrapper. The independent20 failure was an inner120second timeout; an outer600second preemption is a prospective risk, not an observed earlier event.

Root independently reproduced the final timeout path with a synthetic5second budget and locally repinned copied inputs: exit1, an explicit failed aggregate replaced the seeded success, the stale identity report remained but was not attributed, and the other four children completed. This failing synthetic run is separate from the full six-command final validation below. Claude's final peer reused earlier wrapper evidence on inspected executable equivalence and separately reexecuted the ordering mutation. All exact source variants, actual reports and failed environment/shell attempts are preserved.

The prior independent20 review remains CHANGES_REQUIRED0M1S3ADV. Root agrees with its real ordering-control weakness but qualifies its broader evidence: complete reading of all five contracts was not established; the purported direct registered-schema admission probe copied local logic rather than invoking actual closure; some mutation checks were blocked by stale pins. The fresh independent21 reviewer must read every complete contract and index first and assess the cumulative source20 laws, with actual executed boundaries distinguished from structural observations. No historical ACCEPT or count is rewritten. [The prior source20 assessment](technical-review.v20.md) remains historical context, with [root's independent20 assessment](review-assessment.v20.json) controlling its review-evidence limitations.

All31protected historical source files are unchanged and will be included in the new frozen21 inventory. Frozen20 contained10 and verified21others against live source; its scope is not retroactively expanded. The advisory account preserves76source20 records,3independent20 advisories and2final-peer advisories. The environment observation is narrow: the foundation README already specifies Python3.12/jsonschema4.25.1 and the native contract publishes UCD15.0.0; the launcher lacks its own environment field. This final root run records the actual interpreter and package versions separately. Claude used a distinct jsonschema4.26.0 environment, which is not conflated with root's documented environment. Incorrect earlier before-byte labels and two out-of-output Claude memory writes are retained and qualified by the final root peer assessment.

Measured reference results (finite calls/cases, not exhaustive coverage or product qualification):

```json
'''+json.dumps({k:summary[k] for k in ['foundation','security','native','workflows','integration']},indent=2)+'''
```

All four source-pin ledgers require a final after-recording seal and verification in the frozen copy. Fresh independent21 acceptance with zero unresolved MUST/SHOULD, NEWblind9 with complete semantic proof reconstruction, and complete separately independently reviewed application/readiness reconciliation remain required. D372 remains unapplied, all32qualification gates unperformed, condition5 NOT MET, and no implementation, commit or push is authorized.
'''
p=own/'technical-review.v21.md';assert not p.exists();p.write_text(body)
print(json.dumps({'retainedFinalCommands':6,'environment':env,'independentAcceptance':False}))
