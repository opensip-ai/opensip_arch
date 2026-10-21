from pathlib import Path
import subprocess,os,json,tempfile,hashlib,re
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;O=F/'root-review-before-fix-r1';O.mkdir();W=Path('/Users/sb/code/opensip-ai/opensip-d3b2-takeover');R='/opt/homebrew/Cellar/rust/1.95.0/bin/';T=Path(tempfile.mkdtemp(prefix='opensip-d3b2-root-',dir=subprocess.check_output(['getconf','DARWIN_USER_TEMP_DIR'],text=True).strip()));T.chmod(0o700)
E=dict(os.environ,PATH='/opt/homebrew/bin:'+R+':/usr/bin:/bin',CARGO_HOME='/Users/sb/.cargo',CARGO_TARGET_DIR=str(F/'seam-r1/target'),CARGO=R+'cargo',RUSTC=R+'rustc',TMPDIR=str(T),CC='/usr/bin/cc',CXX='/usr/bin/c++',AR='/usr/bin/ar',SDKROOT=subprocess.check_output(['xcrun','--show-sdk-path'],text=True).strip());E.pop('RUST_TEST_THREADS',None)
import shutil
prior=json.loads((F/'revocation-r1/report.json').read_text())
for name in ['registry-events.json','registry-events.md']:
 shutil.copyfile(Path(prior['privateTMPDIR'])/name,W/'crates/operability'/name)
paths=subprocess.check_output(['git','diff','--name-only'],cwd=W,text=True).splitlines()
with (O/'format.log').open('wb') as log:r=subprocess.run([R+'rustfmt','--edition','2024',*[str(W/p) for p in paths if p.endswith('.rs')]],cwd=W,env=E,stdout=log,stderr=subprocess.STDOUT)
assert r.returncode==0
pins={p:hashlib.sha256((W/p).read_bytes()).hexdigest() for p in paths}
r=subprocess.run([R+'cargo','test','--locked','--offline','--no-run','--message-format=json','-p','opensip-components'],cwd=W,env=E,capture_output=True);(O/'build.log').write_bytes(r.stderr);(O/'artifacts.jsonl').write_bytes(r.stdout);assert r.returncode==0,r.stderr[-7000:]
binary=None;fixture=None
for line in r.stdout.splitlines():
 try:j=json.loads(line)
 except ValueError:continue
 if j.get('reason')!='compiler-artifact' or not j.get('executable'):continue
 if j['target']['name']=='supervisor_fixture':fixture=Path(j['executable'])
 if j['target']['name']=='opensip_components' and j['profile']['test']:
  assert j['target']['src_path']==str(W/'crates/components/src/lib.rs');binary=Path(j['executable'])
assert binary and fixture
(binary.parent/'supervisor_fixture.path').write_text(str(fixture)+'\n'+hashlib.sha256(fixture.read_bytes()).hexdigest()+'\n')
listing=subprocess.check_output([str(binary),'--list'],cwd=W,env=E,text=True);(O/'tests.log').write_text(listing)
report=dict(standing='PARTIAL D3b-2 ROOT CANCELLATION DRAFT; NO UNIT ACCEPTANCE OR GATE REMOVAL',sourcePins=pins,binary=str(binary),binarySha256=hashlib.sha256(binary.read_bytes()).hexdigest(),privateTMPDIR=str(T),runs=[])

with (O/'expected-failures.log').open('wb') as log:r=subprocess.run([str(binary),'d3b2_review_'],cwd=W,env=E,stdout=log,stderr=subprocess.STDOUT,timeout=90)
output=(O/'expected-failures.log').read_text();assert r.returncode==101 and '0 passed; 4 failed' in output,output[-4000:]
report['expectedFailedControls']=4;report['exitCode']=r.returncode;report['negativeReproduction']=True;(O/'report.json').write_text(json.dumps(report,indent=2)+'\n');print('Both RFs reproduced:4 runtime failures before correction',flush=True)
