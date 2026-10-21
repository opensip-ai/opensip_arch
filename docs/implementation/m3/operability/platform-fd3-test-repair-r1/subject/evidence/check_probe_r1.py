from pathlib import Path
import os, sys, json, subprocess, tempfile, hashlib, resource
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK') == '1'
F = Path(__file__).parent
mode = sys.argv[1]
assert mode in ('red', 'green')
B = F / ('probe-' + mode + '-r1')
B.mkdir(exist_ok=False)
W = Path('/Users/sb/code/opensip-ai/opensip-platform-fd3-test-repair')
path = 'crates/platform/src/harness_descriptor.rs'
source = F / ('red-source' if mode == 'red' else 'candidate-source') / path
before = (W/path).read_bytes()
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=W,text=True).strip() == '82be07e21dedefb2bd928339ce22c88e97db21ff'
assert (W/path).read_bytes().split(b'#[cfg(test)]',1)[0] == (F/'parent'/path).read_bytes().split(b'#[cfg(test)]',1)[0]
(W/path).write_bytes(source.read_bytes())
R='/opt/homebrew/Cellar/rust/1.95.0/bin/'
T=Path(tempfile.mkdtemp(prefix='n-',dir=subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR'],text=True).strip()))
T.chmod(0o700)
os.setpriority(os.PRIO_PROCESS,0,10)
resource.setrlimit(resource.RLIMIT_CORE,(0,0))
E=dict(os.environ,CARGO_HOME='/Users/sb/.cargo',CARGO_TARGET_DIR=str(F/'target'),TMPDIR=str(T),CC='/usr/bin/cc',CXX='/usr/bin/c++',AR='/usr/bin/ar',CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--show-sdk-path'],text=True).strip())
r=subprocess.run([R+'rustfmt','--edition','2024',str(W/path)],cwd=W,env=E,capture_output=True)
(B/'format.log').write_bytes(r.stdout+r.stderr)
assert r.returncode==0
raw=(W/path).read_bytes()
assert raw.split(b'#[cfg(test)]',1)[0] == (F/'parent'/path).read_bytes().split(b'#[cfg(test)]',1)[0]
r=subprocess.run([R+'cargo','test','--locked','--offline','--no-run','--message-format=json','-p','opensip-platform','--lib'],cwd=W,env=E,capture_output=True)
(B/'build.log').write_bytes(r.stderr)
(B/'artifacts.jsonl').write_bytes(r.stdout)
assert r.returncode==0,'Compile failure is never a runtime witness'
rows=[j for l in r.stdout.splitlines()if l.startswith(b'{')and(j:=json.loads(l)).get('reason')=='compiler-artifact'and j.get('executable')and j['target']['name']=='opensip_platform']
assert len(rows)==1
row=rows[0]
assert not row['fresh']
binary=Path(row['executable'])
test='harness_descriptor::tests::an_ordinary_owned_descriptor_survives_fd3_checks'
r=subprocess.run([str(binary),'--exact',test],cwd=W,env=E,capture_output=True)
log=r.stdout+r.stderr
(B/'runtime.log').write_bytes(log)
red=r.returncode!=0 and b'an unrelated owned fd3 must retain its flags' in log and b'0 passed; 1 failed' in log
report=dict(standing='ACTUAL LEGACY FD3 OWNERSHIP RED IN ISOLATED PROBE' if mode=='red' else 'FIXED FD3 PROCESS ISOLATION FOCUSED GREEN; UNIT ACCEPTANCE OPEN',source=dict(path=path,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()),productionPrefixByteExact=True,
    compiled=True,freshCompilerArtifact=not row['fresh'],binary=dict(path=str(binary),sha256=hashlib.sha256(binary.read_bytes()).hexdigest()),test=test,runtimeExitCode=r.returncode,actualLegacyFlagCorruptionObserved=red,
    allPassed=red if mode=='red' else r.returncode==0 and b'1 passed; 0 failed' in log,productQualification=False,unitAccepted=False)
(B/'report.json').write_text(json.dumps(report,indent=2)+'\n')
assert report['allPassed'],log.decode()[-4000:]
print(mode.upper(),'FD3 owned-descriptor probe compiled and observed; production byte-exact')
