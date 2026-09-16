from pathlib import Path
import subprocess,os,json,hashlib,shutil,time
ROOT=Path(__file__).resolve().parent
STORE=ROOT/"store"
RESULTS=ROOT/"results";RESULTS.mkdir()
rows=[]
def run(name,argv,cwd,expected=0):
 t=time.time();r=subprocess.run(argv,cwd=cwd,capture_output=True,env={**os.environ,"CI":"true"})
 for suffix,data in [("stdout",r.stdout),("stderr",r.stderr)]: (RESULTS/(name+"."+suffix)).write_bytes(data)
 rows.append({"name":name,"argv":argv,"cwd":str(cwd),"exitCode":r.returncode,"expected":expected,"passed":r.returncode==0 if expected==0 else r.returncode!=0,"startedAt":t,"finishedAt":time.time(),"stdoutSha256":hashlib.sha256(r.stdout).hexdigest(),"stderrSha256":hashlib.sha256(r.stderr).hexdigest()})
 print(name,r.returncode,flush=True)
 return r.returncode==0
flags=["--ignore-workspace","--ignore-scripts","--ignore-pnpmfile","--store-dir",str(STORE),"--package-import-method","copy"]
for lane in ["provider","report"]:
 source=ROOT/"source"/lane
 if not run(lane+"-materialize",["pnpm","install","--no-frozen-lockfile",*flags],source):continue
 export=ROOT/("isolated-"+lane)
 shutil.copytree(source,export,ignore=shutil.ignore_patterns("node_modules","dist"))
 before=(export/"pnpm-lock.yaml").read_bytes()
 if run(lane+"-offline-install",["pnpm","install","--offline","--frozen-lockfile",*flags],export):
  run(lane+"-build",["pnpm","run","build"],export)
 assert (export/"pnpm-lock.yaml").read_bytes()==before
 assert not (export.parent/("isolated-"+("report" if lane=="provider" else "provider"))/"package.json").exists() if lane=="provider" else True
 # Deliberate declared-input drift must fail before regeneration.
 manifest=json.loads((export/"package.json").read_text());manifest["devDependencies"]["typescript"]="0.0.0"
 (export/"package.json").write_text(json.dumps(manifest)+"\n")
 run(lane+"-lock-drift",["pnpm","install","--offline","--frozen-lockfile",*flags],export,expected=1)
 shutil.copyfile(source/"package.json",export/"package.json")
(ROOT/"trial-results.json").write_text(json.dumps({"standing":"Per-lane package-manager trial only; not sealed toolchain or complete M1 build proof","pnpm":"11.10.0","node":"24.16.0","typescript":"7.0.2 trial-only","commands":rows},indent=2)+"\n")
