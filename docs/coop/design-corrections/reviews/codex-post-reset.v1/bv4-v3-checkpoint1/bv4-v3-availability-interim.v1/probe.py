"""Root interim diagnostic of workspace ownership in the new public availability projection.
Synthetic selection inputs and actual pure reference projection; no host delivery claim.
"""
from pathlib import Path
import hashlib,importlib.util,json,shutil
base=Path('/tmp/opensip-design-corrections/bv4-corrections-author.v3');dc=base/'work/docs/coop/design-corrections'
p=dc/'native/native_evidence_model.v2.py';s=importlib.util.spec_from_file_location('root_v3_native',p);n=importlib.util.module_from_spec(s);s.loader.exec_module(n)
units=[{'rootPath':path,'languageMode':'ts-tsconfig','languageFamily':'tsjs'} for path in ['apps/a','apps/b']]
result=n.default_capability_selection(units,[])
inputs=[r for r in result['undeclaredCapabilities'] if r['capabilityId'] in ['clones-near','clones-cross-tsjs']]
outputs=n.release_absence_details(inputs)
assert len(inputs)==4 and len(outputs)==4
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
report={'standing':'Interim root source observation, not final-source assent or host/renderer execution. Two trusted synthetic unit descriptors stand in for admitted discovery. Actual new release_absence_details consumes selected absence rows.','sourceRoot':str(base/'work'),'sources':[{'path':str(p.relative_to(base/'work')),'sha256':sha(p)} for p in [p,dc/'native/native-evidence.schemas.v2.json',dc/'native/native-capability-matrix.v2.json']], 'inputRows':inputs,'projectedDetails':outputs,'distinctInputOwnershipTuples':len({(r['capabilityId'],r['languageMode'],r['workspaceRoot']) for r in inputs}),'distinctProjectedDetails':len({json.dumps(r,sort_keys=True) for r in outputs}),'observation':'Different workspaceRoot values become identical public details: the subject contains capabilityId and languageMode only. This leaves a consumer unable to attribute an absence to its requested unit from the published detail.'}
out=Path('/tmp/opensip-design-corrections/bv4-v3-availability-interim.v1');out.mkdir(exist_ok=False);(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');shutil.copyfile(__file__,out/'probe.py');print(json.dumps(report,indent=2))
