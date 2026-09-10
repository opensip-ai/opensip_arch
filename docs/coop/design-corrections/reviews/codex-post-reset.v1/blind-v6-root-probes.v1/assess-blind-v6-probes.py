"""Root post-completion evidence audit. Does not change or feed back blind sources."""
from pathlib import Path
import sys,json,hashlib,importlib.util,contextlib,io,datetime
root=Path('/Users/sb/code/opensip-ai/opensip_arch');rv=root/'docs/coop/design-corrections/reviews';out=rv/'codex-post-reset.v1/blind-v6-root-probes.v1';assert not out.exists();out.mkdir()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
c=json.loads((rv/'consumer-b.v6/custody.json').read_text())
for f in c['files']:
 p=rv/'consumer-b.v6'/f['path'];assert sha(p)==f['sha256'] and p.stat().st_size==f['bytes']
mf=rv/'candidate-subject.v16.json';assert sha(mf)=='ca5f36d421fb38d264f49fc6b2e1eeffee5bbe8182a7fe25bd50787244042ee9';m=json.loads(mf.read_text());snap=Path(m['snapshotRoot'])
for f in m['files']:
 p=snap/f['path'];assert sha(p)==f['sha256'] and p.stat().st_size==f['bytes']
m1=rv/'candidate-subject.v1.json';assert sha(m1)=='e7403b702d419f381be1cdbee7b886303fb43106b86985bc2f8ec63f5687a0ac'
for f in json.loads(m1.read_text())['files']:
 p=Path(json.loads(m1.read_text())['snapshotRoot'])/f['path'];assert sha(p)==f['sha256'] and p.stat().st_size==f['bytes']
spec=importlib.util.spec_from_file_location('root_v16_identity',snap/'docs/coop/design-corrections/foundation/identity-model.py');M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
sys.path.insert(0,str(rv/'consumer-b.v6/output/ref'));buf=io.StringIO()
with contextlib.redirect_stdout(buf):
 import build_ts,build_ts2,build_ts3,build_ts4,build_rust,build_rust2,build_syntax,build_workflow,build_suff,build_final
(out/'reconstruction-stdout.txt').write_text(buf.getvalue());S=build_ts.S
objects={};frames=[]
for digest,bb in S.cas.items():
 assert hashlib.sha256(bb).hexdigest()==digest
 if bb.startswith(M.FRAME_PREFIX):
  rest=bb[len(M.FRAME_PREFIX):];d,raw=rest.split(b'\0',1);domain=d.decode();assert int.from_bytes(raw[:8],'big')==len(raw[8:]);rec=json.loads(raw[8:]);frames.append((digest,domain,rec))
  if domain in M.PREFIX:objects[M.PREFIX[domain]+':'+digest]=(domain,rec)
checks=[]
for k,(dom,rec) in objects.items():
 if dom=='run':
  try:r=M.close_run(rec,objects,S.cas);checks.append({'runId':k,'result':'ADMITTED','return':str(r)})
  except Exception as exc:checks.append({'runId':k,'result':'REFUSED','exception':type(exc).__name__,'detail':str(exc)})
assert len(checks)==4
policies=[]
for digest,bb in S.cas.items():
 if not bb.startswith(b'{'):continue
 try:rec=json.loads(bb)
 except Exception:continue
 if not isinstance(rec,dict):continue
 if 'policyId' in rec and 'rules' in rec:selector='PolicyDocumentV1'
 elif 'waivers' in rec:selector='WaiverSetV1'
 else:continue
 try:M.validate_registered_record('workflows/schemas/policy-document.schema.json','#/$defs/'+selector,rec);result='ADMITTED';detail=''
 except Exception as exc:result='REFUSED';detail=str(exc)
 policies.append({'sha256':digest,'selector':selector,'keys':list(rec),'result':result,'detail':detail})
result={'standing':'Root audit AFTER completed blind; no modification or feedback to reviewer. Schema and closure refusals qualify claimed positive evidence; they do not erase independent normative findings. No product qualification.','at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'retentionFilesVerified':len(c['files']),'v16FilesVerified':len(m['files']),'v1FilesVerified':len(json.loads(m1.read_text())['files']),'casObjectsReconstructed':len(S.cas),'typedObjects':len(objects),'runClosureChecks':checks,'foreignPolicySchemaChecks':policies}
(out/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
