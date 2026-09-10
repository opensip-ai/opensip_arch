"""Actual pure selection/collection diagnostic; no host execution or full Run claim."""
from pathlib import Path
import hashlib,json,importlib.util,shutil
b=Path('/tmp/opensip-design-corrections/bv4-corrections-author.v3/work')
dc=b/'docs/coop/design-corrections'
out=Path('/tmp/opensip-design-corrections/bv4-v3-multistep-interim.v1');out.mkdir(exist_ok=False)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rels=['native/native_evidence_model.v2.py','native/native-evidence.schemas.v2.json','native/native-capability-matrix.v2.json','workflows/workflows_model.v1.py','workflows/schemas/common.schema.json','workflows/schemas/command-envelope.schema.json','workflows/schemas/invocation-record.schema.json','foundation/identity-schemas.v2.json']
sources=[]
for rel in rels:
 p=dc/rel;q=out/'source'/rel;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q);sources.append({'path':'docs/coop/design-corrections/'+rel,'sha256':sha(q)})
s=importlib.util.spec_from_file_location('native_multistep',dc/'native/native_evidence_model.v2.py');N=importlib.util.module_from_spec(s);s.loader.exec_module(N)
s=importlib.util.spec_from_file_location('workflow_multistep',dc/'workflows/workflows_model.v1.py');W=importlib.util.module_from_spec(s);s.loader.exec_module(W)
selections=[]
for step in range(2):
 units=[{'rootPath':f'apps/s{step}/unit{i:03}','languageMode':'ts-tsconfig','languageFamily':'tsjs'} for i in range(93)]
 selections.append(N.default_capability_selection(units,[]))
def admission(x):
 try:W.validate_import_record('workflows/schemas/common.schema.json','#/$defs/CapabilityAvailabilityV1',x);return {'result':'ADMIT'}
 except Exception as e:return {'result':'REFUSE','error':str(e.__cause__ or e).split('\n')[0][:500]}
collections=[N.release_absence_notices(s['undeclaredCapabilities']) for s in selections]
combined=N.release_absence_notices([r for s in selections for r in s['undeclaredCapabilities']])
r={'standing':'Interim root composition diagnostic. Actual default_capability_selection validates each synthetic analysis-spec; release_absence_notices and actual workflow schema admission exercised. Trusted synthetic unit enumeration; no actual invocation execution or full Run admission. Combining disjoint rows probes the claimed invocation-wide no-truncation bound, not a claimed implemented host algorithm.',
 'sources':sources,'separateStepRequestedCounts':[len(s['analysisSpec']['requestedCapabilities']) for s in selections],
 'separateCollections':[admission(c) for c in collections],
 'combinedCount':combined['noticeCount'],'combinedAdmission':admission(combined),
 'observation':'Two individually admitted selections have1023requested rows each across186distinct units. A flat invocation collection needs2046unique notices, exceeding1024. Per-analysis-spec maximum is not a maximum over a multi-step invocation. Normative composition must specify bounded per-step carriers or an explicit bounded aggregate law that preserves admitted invocations and scope.'}
for row in sources:assert sha(b/row['path'])==row['sha256'],'Primary source changed during probe; retain failure and rerun on checkpoint'
(out/'report.json').write_text(json.dumps(r,indent=2)+'\n');shutil.copyfile(__file__,out/'probe.py')
print(json.dumps({k:v for k,v in r.items() if k not in ('sources','standing')},indent=2))
