from pathlib import Path
import os,subprocess
R=Path('/tmp/opensip-implementation/source-attempt-r1-authoring');T=R/'bare';D=Path('/Users/sb/code/opensip-ai/opensip-source-attempt/target/debug/deps');env=dict(os.environ,SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--sdk','macosx','--show-sdk-path']).decode().strip());cmd=['/usr/bin/nice','-n','10','/opt/homebrew/Cellar/rust/1.95.0/bin/rustc','--edition=2024','--test',str(T/'lib.rs'),'-L','dependency='+str(D),'-C','linker=/usr/bin/cc','-o',str(T/'exact-controls')]
for crate in ['opensip_identity','miniz_oxide','serde_json']:cmd+=['--extern',crate+'='+str(next(D.glob('lib'+crate+'-*.rlib')))]
r=subprocess.run(cmd,env=env,capture_output=True);(R/'exact-bare-compile.log').write_bytes(r.stdout+r.stderr);r.check_returncode();r=subprocess.run([str(T/'exact-controls')],capture_output=True);(R/'exact-bare-test.log').write_bytes(r.stdout+r.stderr);print(r.stdout.decode().split('test result:')[-1]);r.check_returncode()
