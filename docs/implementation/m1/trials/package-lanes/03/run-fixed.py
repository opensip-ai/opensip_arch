from pathlib import Path
import subprocess,os,json,hashlib,time
ROOT=Path(__file__).resolve().parent;STORE=ROOT.parent/"m1-lane-trial-01/store";RESULTS=ROOT/"fixed-results";RESULTS.mkdir();rows=[]
def run(name,argv,cwd,negative=False):
 r=subprocess.run(argv,cwd=cwd,capture_output=True,env={**os.environ,"CI":"true"})
 for suffix,data in [("stdout",r.stdout),("stderr",r.stderr)]: (RESULTS/(name+"."+suffix)).write_bytes(data)
 rows.append({"name":name,"argv":argv,"cwd":str(cwd),"exitCode":r.returncode,"negativeControl":negative,"passed":r.returncode!=0 if negative else r.returncode==0,"stdoutSha256":hashlib.sha256(r.stdout).hexdigest(),"stderrSha256":hashlib.sha256(r.stderr).hexdigest()});print(name,r.returncode,flush=True)
for lane in ["provider","report"]:
 path=ROOT/lane
 run(lane+"-config",["pnpm","config","get","verify-deps-before-run"],path)
 run(lane+"-offline-install",["pnpm","install","--offline","--frozen-lockfile","--ignore-scripts","--ignore-pnpmfile","--store-dir",str(STORE),"--package-import-method","copy"],path)
 run(lane+"-build",["pnpm","--config.store-dir="+str(STORE),"run","build"],path)
 manifest=path/"package.json";before=manifest.read_bytes();d=json.loads(before);d["devDependencies"]["typescript"]="0.0.0";manifest.write_text(json.dumps(d)+"\n")
 run(lane+"-build-drift-refuses",["pnpm","--config.store-dir="+str(STORE),"run","build"],path,True)
 manifest.write_bytes(before)
(ROOT/"fixed-trial-results.json").write_text(json.dumps({"standing":"Bounded lane settings correction; complete isolation/policy choice still pending","commands":rows},indent=2)+"\n")
