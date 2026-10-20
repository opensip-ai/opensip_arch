from pathlib import Path
import subprocess,os,json,tempfile,hashlib
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
W=Path('/Users/sb/code/opensip-ai/opensip-d5-0-takeover');F=Path(__file__).parent;O=F/'mutation-r1';O.mkdir();R='/opt/homebrew/Cellar/rust/1.95.0/bin/'
T=Path(tempfile.mkdtemp(prefix='opensip-d5-mutation-',dir=subprocess.check_output(['getconf','DARWIN_USER_TEMP_DIR'],text=True).strip()));T.chmod(0o700)
E=dict(os.environ,PATH='/opt/homebrew/bin:'+R+':/usr/bin:/bin',CARGO_HOME='/Users/sb/.cargo',CARGO_TARGET_DIR=str(O/'target'),CARGO=R+'cargo',RUSTC=R+'rustc',TMPDIR=str(T),CC='/usr/bin/cc',CXX='/usr/bin/c++',AR='/usr/bin/ar',SDKROOT=subprocess.check_output(['xcrun','--show-sdk-path'],text=True).strip())
p=W/'crates/components/src/supervisor_tests.rs';raw=p.read_bytes();needle=b'fn quick() -> Waits {\n    Waits::RELEASE\n}';assert raw.count(needle)==1
args=[R+'cargo','test','--locked','--offline','-p','opensip-components','--lib','supervisor::tests::ordinary_controls_keep_every_release_wait','--','--exact','--nocapture']
try:
 p.write_bytes(raw.replace(needle,b'fn quick() -> Waits {\n    Waits { handshake: Duration::from_millis(2_000), ..Waits::RELEASE }\n}'))
 with (O/'negative.log').open('wb') as f:r=subprocess.run(args,cwd=W,env=E,stdout=f,stderr=subprocess.STDOUT)
 text=(O/'negative.log').read_text();caught=r.returncode==101 and '0 passed; 1 failed' in text and 'assertion `left == right` failed' in text
finally:
 p.write_bytes(raw)
assert p.read_bytes()==raw
with (O/'restored.log').open('wb') as f:positive=subprocess.run(args,cwd=W,env=E,stdout=f,stderr=subprocess.STDOUT)
report=dict(sourceSha256=hashlib.sha256(raw).hexdigest(),mutation='restore universal 2s handshake in quick()',negativeExit=r.returncode,runtimeFailureCaught=caught,restoredExit=positive.returncode,restoredSourceExact=p.read_bytes()==raw,positivePassed='1 passed; 0 failed' in (O/'restored.log').read_text())
(O/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report),flush=True);assert caught and positive.returncode==0 and report['positivePassed']
