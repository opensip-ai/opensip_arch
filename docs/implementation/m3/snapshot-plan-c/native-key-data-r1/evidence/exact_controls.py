from pathlib import Path
import shutil,subprocess,os,json
R=Path('/tmp/opensip-implementation/native-key-data-r1-authoring');W=Path('/Users/sb/code/opensip-ai/opensip-native-key-data');T=R/'bare';D=W/'target/debug/deps';U=R/'ui';U.mkdir(exist_ok=True)
for f in ['native_key_data.rs','native_key_data_tests.rs']:shutil.copyfile(W/'crates/host/src'/f,T/f)
x=T/'native_key_data/fixtures/golden.json';x.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(W/'crates/host/src/native_key_data/fixtures/golden.json',x)
sdk=subprocess.check_output(['/usr/bin/xcrun','--sdk','macosx','--show-sdk-path']).decode().strip();cmd=['/usr/bin/nice','-n','10','/opt/homebrew/Cellar/rust/1.95.0/bin/rustc','--edition=2024','--test',str(T/'lib.rs'),'-L','dependency='+str(D),'-C','linker=/usr/bin/cc','-o',str(T/'exact-controls')]
for crate in ['opensip_identity','serde_json']:cmd+=['--extern',crate+'='+str(next(D.glob('lib'+crate+'-*.rlib')))]
r=subprocess.run(cmd,env=dict(os.environ,SDKROOT=sdk),capture_output=True);(R/'exact-bare-compile.log').write_bytes(r.stdout+r.stderr);r.check_returncode();r=subprocess.run([str(T/'exact-controls')],capture_output=True);(R/'exact-bare-test.log').write_bytes(r.stdout+r.stderr);r.check_returncode();assert '6 passed; 0 failed' in r.stdout.decode()
m=max((p for p in D.glob('libopensip_host-*.rmeta')if p.stat().st_size>0),key=lambda p:p.stat().st_mtime_ns);out={}
for name,body,expected in [('positive','extern crate opensip_host;fn main(){let _=opensip_host::embedded_schema_registry;}','success'),('private','extern crate opensip_host;use opensip_host::native_key_data::KeyData;fn main(){let _:Option<KeyData>=None;}','E0603')]:
 p=U/(name+'.rs');p.write_text(body+'\n');r=subprocess.run(['/usr/bin/nice','-n','10','/opt/homebrew/Cellar/rust/1.95.0/bin/rustc','--edition=2024','--emit=metadata',str(p),'--extern','opensip_host='+str(m),'-L','dependency='+str(D),'-o',str(U/(name+'.rmeta'))],capture_output=True);(U/(name+'.log')).write_bytes(r.stdout+r.stderr);assert r.returncode==0 if expected=='success' else r.returncode!=0 and expected in r.stderr.decode();out[name]=dict(expected=expected,returncode=r.returncode,hostMetadata=str(m))
(U/'checks.json').write_text(json.dumps(out,indent=2)+'\n');print('Exact candidate bare6 and actual host metadata positive/E0603 pass.')
