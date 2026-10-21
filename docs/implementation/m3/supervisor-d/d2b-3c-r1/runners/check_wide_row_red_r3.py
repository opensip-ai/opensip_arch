from pathlib import Path
import os,subprocess,tempfile,json,hashlib
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;B=F/'native-resume-r1/wide-row-red-r3';assert not B.exists();B.mkdir();W=Path('/Users/sb/code/opensip-ai/opensip-d2b3c-native-resume');R='/opt/homebrew/Cellar/rust/1.95.0/bin/'
T=Path(tempfile.mkdtemp(prefix='n-',dir=subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR'],text=True).strip()));T.chmod(0o700);os.setpriority(os.PRIO_PROCESS,0,10)
E=dict(os.environ,CARGO_HOME='/Users/sb/.cargo',CARGO_TARGET_DIR=str(F/'native-resume-r1/target'),TMPDIR=str(T),CC='/usr/bin/cc',CXX='/usr/bin/c++',AR='/usr/bin/ar',CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--show-sdk-path'],text=True).strip())
p=W/'crates/components/src/provider_protocol/ts2_census_tests.rs';subprocess.run([R+'rustfmt','--edition','2024',str(p)],cwd=W,env=E,check=True)
name='provider_protocol::ts2::tests::send::census::wide_signature_token_rows_are_admitted_without_weakening_item_or_count_bounds'
r=subprocess.run([R+'cargo','test','--locked','--offline','-p','opensip-components','--lib',name,'--','--exact'],cwd=W,env=E,capture_output=True);raw=r.stdout+r.stderr;(B/'runtime.log').write_bytes(raw);text=raw.decode(errors='replace')
report=dict(exitCode=r.returncode,expectedRedRuntimeFailure=r.returncode!=0 and '0 passed; 1 failed' in text and 'wide signature tokens: Err(Schema(' in text,test=name,testSourceSha256=hashlib.sha256(p.read_bytes()).hexdigest(),productionSourceSha256=hashlib.sha256((W/'crates/components/src/provider_protocol/ts2.rs').read_bytes()).hexdigest(),rustCompileFailureCounted=False,productQualification=False)
(B/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2));assert report['expectedRedRuntimeFailure'],text[-3000:]
