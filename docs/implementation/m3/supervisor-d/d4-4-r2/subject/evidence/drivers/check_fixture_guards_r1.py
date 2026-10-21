from pathlib import Path
import os,json,subprocess,tempfile,hashlib
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;B=F/'fixture-guards-r1';B.mkdir(exist_ok=False);W=Path('/Users/sb/code/opensip-ai/opensip-d4factory-takeover');R='/opt/homebrew/Cellar/rust/1.95.0/bin/'
T=Path(tempfile.mkdtemp(prefix='n-',dir=subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR'],text=True).strip()));T.chmod(0o700);os.setpriority(os.PRIO_PROCESS,0,10)
E=dict(os.environ,PATH=R+':'+os.environ['PATH'],CARGO_HOME='/Users/sb/.cargo',CARGO_TARGET_DIR=str(F/'target'),TMPDIR=str(T),CC='/usr/bin/cc',CXX='/usr/bin/c++',AR='/usr/bin/ar',CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--show-sdk-path'],text=True).strip())
for key in ['RUSTFLAGS','CARGO_ENCODED_RUSTFLAGS','RUSTC_WRAPPER','RUSTC_WORKSPACE_WRAPPER','CARGO_BUILD_RUSTFLAGS']:E.pop(key,None)
paths=sorted(subprocess.check_output(['/usr/bin/git','ls-files','-m','-o','--exclude-standard'],cwd=W,text=True).splitlines())
def pins():return [dict(path=p,bytes=len((W/p).read_bytes()),sha256=hashlib.sha256((W/p).read_bytes()).hexdigest())for p in paths]
before=pins();lib=(W/'crates/lifecycle/src/lib.rs').read_text();source=(W/'crates/lifecycle/src/retained_tree.rs').read_text()
assert '#[cfg(all(feature = "scenario-fixtures", not(debug_assertions)))]'in lib
assert '#[cfg(all(debug_assertions, any(test, feature = "scenario-fixtures")))]'in source
report=dict(standing='D4 native fixture helper default/release inaccessibility checks; no runtime/fullproject qualification.',sourcePins=before,allPassed=False,productQualification=False)
def save():(B/'report.json').write_text(json.dumps(report,indent=2)+'\n')
save();r=subprocess.run([R+'cargo','check','--locked','--offline','-p','opensip-host','--message-format=json'],cwd=W,env=E,capture_output=True);(B/'default-build.log').write_bytes(r.stderr);(B/'default-artifacts.jsonl').write_bytes(r.stdout);report['defaultExit']=r.returncode;save();assert r.returncode==0
rows=[j for line in r.stdout.splitlines()if line.startswith(b'{')and(j:=json.loads(line)).get('reason')=='compiler-artifact'and j['target']['name']=='opensip_lifecycle'];assert len(rows)==1;row=rows[0];assert 'scenario-fixtures'not in row['features']and 'crash-matrix'not in row['features'];report['defaultLifecycleArtifact']=row;save()
r=subprocess.run([R+'cargo','check','--locked','--offline','--release','-p','opensip-lifecycle','--features','scenario-fixtures'],cwd=W,env=E,capture_output=True);log=r.stdout+r.stderr;(B/'release-refusal.log').write_bytes(log);report.update(releaseExit=r.returncode,releaseFixtureRejected=r.returncode!=0 and b'scenario-fixtures'in log and(b'debug assertions'in log or b'debug_assertions'in log));save();assert report['releaseFixtureRejected'];assert pins()==before;report['allPassed']=True;save();print('DEFAULT HOST/LIFECYCLE HAS NO FIXTURE FEATURE; EXPLICIT RELEASE FIXTURE BUILD REJECTED; exact cfg guards pinned.')
