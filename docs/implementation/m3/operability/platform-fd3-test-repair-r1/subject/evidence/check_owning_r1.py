from pathlib import Path
import os,json,hashlib,subprocess,tempfile,re,resource
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;B=F/'owning-r1';B.mkdir(exist_ok=False)
W=Path('/Users/sb/code/opensip-ai/opensip-platform-fd3-test-repair');R='/opt/homebrew/Cellar/rust/1.95.0/bin/'
T=Path(tempfile.mkdtemp(prefix='n-',dir=subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR'],text=True).strip()));T.chmod(0o700)
os.setpriority(os.PRIO_PROCESS,0,10);resource.setrlimit(resource.RLIMIT_CORE,(0,0))
E=dict(os.environ,CARGO_HOME='/Users/sb/.cargo',CARGO_TARGET_DIR=str(F/'target'),TMPDIR=str(T),CC='/usr/bin/cc',CXX='/usr/bin/c++',AR='/usr/bin/ar',CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--show-sdk-path'],text=True).strip())
E.pop('RUST_TEST_THREADS',None)
path='crates/platform/src/harness_descriptor.rs';raw=(W/path).read_bytes()
green=json.loads((F/'probe-green-r1/report.json').read_text());assert green['allPassed'] and hashlib.sha256(raw).hexdigest()==green['source']['sha256']
report=dict(standing='FD3 TEST PROCESS ISOLATION; NO UNIT ACCEPTANCE/QUALIFICATION',source=green['source'],productionPrefixByteExact=True,runs=[],mutants=[],productQualification=False)
def save():(B/'report.json').write_text(json.dumps(report,indent=2)+'\n')
def compile(folder,fresh=False):
 folder.mkdir(parents=True,exist_ok=True)
 r=subprocess.run([R+'cargo','test','--locked','--offline','--no-run','--message-format=json','-p','opensip-platform','--lib'],cwd=W,env=E,capture_output=True);(folder/'build.log').write_bytes(r.stderr);(folder/'artifacts.jsonl').write_bytes(r.stdout);assert r.returncode==0,'Compile failure never counts as catch'
 rows=[j for l in r.stdout.splitlines()if l.startswith(b'{')and(j:=json.loads(l)).get('reason')=='compiler-artifact'and j.get('executable')and j['target']['name']=='opensip_platform'];assert len(rows)==1;row=rows[0];assert not fresh or not row['fresh'];binary=Path(row['executable']);(folder/'binary.json').write_text(json.dumps(dict(path=str(binary),sha256=hashlib.sha256(binary.read_bytes()).hexdigest(),freshCompilerArtifact=not row['fresh']),indent=2)+'\n');return binary
binary=compile(B/'positive');save()
for trial in range(3):
 r=subprocess.run([str(binary)],cwd=W,env=E,capture_output=True);log=r.stdout+r.stderr;(B/f'platform-default-parallel-{trial+1}.log').write_bytes(log);report['runs'].append(dict(trial=trial+1,exitCode=r.returncode,summaries=re.findall(r'^test result:.*$',log.decode(),re.M),defaultParallel=True));save();assert r.returncode==0,log.decode()[-3500:]
with (B/'clippy.log').open('wb')as out:r=subprocess.run([R+'cargo','clippy','--locked','--offline','-p','opensip-platform','--all-targets','--','-D','warnings'],cwd=W,env=E,stdout=out,stderr=subprocess.STDOUT)
assert r.returncode==0,(B/'clippy.log').read_text()[-2500:]
test='harness_descriptor::tests::an_ordinary_owned_descriptor_survives_fd3_checks'
cases=[
 ('legacy-test-back-in-parent','if isolated_fd3_case(FD3_CASE, None) {','if false && isolated_fd3_case(FD3_CASE, None) {','an unrelated owned fd3 must retain its flags'),
 ('child-case-identity-not-checked','a[0] == "--exact" && a[1] == case','a[0] == "--exact"','an unrelated owned fd3 must retain its flags'),
 ('child-filter-selects-no-test','"--exact",\n            case,','"--exact",\n            "no-such-fd3-case",','isolated fd3 case'),
]
for name,old,new,witness in cases:
 assert raw.decode().count(old)==1,(name,old);(W/path).write_text(raw.decode().replace(old,new));error=None
 try:
  binary=compile(B/name,True);r=subprocess.run([str(binary),'--exact',test],cwd=W,env=E,capture_output=True);log=r.stdout+r.stderr;(B/name/'runtime.log').write_bytes(log);assert r.returncode!=0 and witness.encode()in log and b'0 passed; 1 failed'in log;report['mutants'].append(dict(id=name,compiled=True,caught=True,witness=witness,runtimeExitCode=r.returncode))
 except BaseException as ex:error=ex
 finally:
  (W/path).write_bytes(raw);assert hashlib.sha256((W/path).read_bytes()).hexdigest()==report['source']['sha256'];binary=compile(B/(name+'-restored-positive'),True);r=subprocess.run([str(binary),'--exact',test],cwd=W,env=E,capture_output=True);(B/(name+'-restored-positive')/'runtime.log').write_bytes(r.stdout+r.stderr);assert r.returncode==0;report['allRestored']=True;save()
 if error:raise error
report.update(allPassed=True,platformClippyPassed=True,wholePlatformDefaultParallelTrials=3,compiledRuntimeMutants=len(cases));save();print('THREE DEFAULT-PARALLEL PLATFORM SUITES PASS;3COMPILED RUNTIME MUTANTS CAUGHT/RESTORED; SOURCE CENSUS/UNIT REVIEW STILL REQUIRED')
