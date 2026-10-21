from pathlib import Path
import os,json,hashlib,subprocess,tempfile,re
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;B=F/'factory-source-r1';B.mkdir(exist_ok=False);W=Path('/Users/sb/code/opensip-ai/opensip-d4factory-takeover');R='/opt/homebrew/Cellar/rust/1.95.0/bin/'
T=Path(tempfile.mkdtemp(prefix='n-',dir=subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR'],text=True).strip()));T.chmod(0o700);os.setpriority(os.PRIO_PROCESS,0,10)
E=dict(os.environ,PATH=R+':'+os.environ['PATH'],CARGO_HOME='/Users/sb/.cargo',CARGO_TARGET_DIR=str(F/'target'),TMPDIR=str(T),CC='/usr/bin/cc',CXX='/usr/bin/c++',AR='/usr/bin/ar',CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--show-sdk-path'],text=True).strip());E.pop('RUST_TEST_THREADS',None)
names=sorted(subprocess.check_output(['/usr/bin/git','ls-files','-m','-o','--exclude-standard'],cwd=W,text=True).splitlines())
def pins():return [dict(path=p,bytes=len((W/p).read_bytes()),sha256=hashlib.sha256((W/p).read_bytes()).hexdigest())for p in names]
before=pins();r=subprocess.run([R+'cargo','test','--locked','--offline','--no-run','--lib','--message-format=json','-p','opensip-components'],cwd=W,env=E,capture_output=True);(B/'build.log').write_bytes(r.stderr);(B/'artifacts.jsonl').write_bytes(r.stdout)
report=dict(standing='D4-4 factory source compilation and release constant source pin only; no complete unit/adapter acceptance.',buildExit=r.returncode,sourcePins=before,allPassed=False,productQualification=False)
(B/'report.json').write_text(json.dumps(report,indent=2)+'\n');assert r.returncode==0
rows=[j for line in r.stdout.splitlines()if line.startswith(b'{')and(j:=json.loads(line)).get('reason')=='compiler-artifact'and j.get('executable')and j['target']['name']=='opensip_components'];assert len(rows)==1;row=rows[0];binary=Path(row['executable'])
r=subprocess.run([str(binary),'provider_protocol::release_limits::tests'],cwd=W,env=E,capture_output=True);log=r.stdout+r.stderr;(B/'owning.log').write_bytes(log);report.update(exitCode=r.returncode,summaries=re.findall(r'^test result:.*$',log.decode(errors='replace'),re.M),failureSet=re.findall(r'^test (.+) \.\.\. FAILED$',log.decode(errors='replace'),re.M),binary=str(binary),binarySha256=hashlib.sha256(binary.read_bytes()).hexdigest(),compilerArtifactCached=row['fresh'],allPassed=r.returncode==0 and b'1 passed; 0 failed'in log)
(B/'report.json').write_text(json.dumps(report,indent=2)+'\n');assert report['allPassed']and pins()==before
print(json.dumps(report,indent=2))
