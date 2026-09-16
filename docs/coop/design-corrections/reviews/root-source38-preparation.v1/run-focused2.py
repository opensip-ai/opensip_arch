from pathlib import Path
import subprocess,time,json,hashlib,concurrent.futures
B=Path('/tmp/opensip-design-corrections');S=B/'termination-exclusivity-successor.v1/source';O=B/'root-source38-focused.v2';O.mkdir()
W=S/'docs/coop/design-corrections/workflows'
def run(name,script,args):
 cmd=['/tmp/opensip-architecture-review-env/bin/python','-I','-B',str(W/script),*args];t=time.time();r=subprocess.run(cmd,capture_output=True,text=True)
 (O/(name+'.stdout')).write_text(r.stdout);(O/(name+'.stderr')).write_text(r.stderr)
 out={'name':name,'command':cmd,'checkerSha256':hashlib.sha256((W/script).read_bytes()).hexdigest(),'exitCode':r.returncode,'elapsedSeconds':time.time()-t,'stdoutSha256':hashlib.sha256(r.stdout.encode()).hexdigest(),'stderrSha256':hashlib.sha256(r.stderr.encode()).hexdigest()}
 (O/(name+'-command.json')).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out),flush=True)
 if r.returncode:print(r.stderr[-1600:],flush=True)
 return out
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
 jobs=[pool.submit(run,'query','check-query-projection.v3.py',['--report',str(O/'query-report.json')]),pool.submit(run,'workflow','check-workflow-projection.v3.py',[])]
 results=[f.result() for f in jobs]
(O/'commands.json').write_text(json.dumps(results,indent=2)+'\n')
