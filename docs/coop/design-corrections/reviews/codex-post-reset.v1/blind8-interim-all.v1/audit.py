from pathlib import Path
import json,sys,hashlib,importlib.util,base64
HERE=Path(__file__).parent
sys.path.insert(0,str(HERE/'work'))
import run_ts,run_rust,run_syntax,run_ts_config,osip
fx,A,rid={"ts":run_ts.build_run,"rust":run_rust.build_run,"syntax":run_syntax.build_run,"config":run_ts_config.build_run}[sys.argv[1]](*sys.argv[2:])
mp=Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v19.json')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(mp)=='312db9d904d0ec1f9c91d84137feb3277490b79b07bf3a6d5efc0380caa0f24b'
m=json.loads(mp.read_text());base=Path(m['snapshotRoot']);model=base/'docs/coop/design-corrections/foundation/identity-model.py'
spec=importlib.util.spec_from_file_location('root_v19',model);M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
objects={};bad=[]
for h,b in fx.s.blobs.items():
 if hashlib.sha256(b).hexdigest()!=h:bad.append(h)
 if b.startswith(osip.FRAME_PREFIX+b'\0'):
  dom,desc=osip.parse_frame(b)
  if dom in M.PREFIX:objects[M.PREFIX[dom]+':'+h]=(dom,desc)
report={'standing':'Preliminary root audit of graph computed from exact captured independent source. Not the eventual independently exported graph, no blindassent.','runId':rid,'blobs':len(fx.s.blobs),'typedObjects':len(objects),'badBlobHashes':bad,'parentSha256':sha(mp)}
try:
 assert not bad
 report['admittedRunId']=M.close_run(objects[rid][1],objects,fx.s.blobs);report['result']='ADMITTED'
except Exception as e:report.update(result='REFUSED',exception=type(e).__name__,detail=str(e))
(HERE/('result-'+ '-'.join(sys.argv[1:])+'.json')).write_text(json.dumps(report,indent=2)+'\n')
(HERE/('graph-'+ '-'.join(sys.argv[1:])+'.json')).write_text(json.dumps({'runId':rid,'objects':fx.objects,'blobs':{h:base64.b64encode(b).decode() for h,b in fx.s.blobs.items()}},indent=2)+'\n')
print(json.dumps(report,indent=2))
