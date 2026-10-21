from pathlib import Path
import os,subprocess,tempfile,json,hashlib,re
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;B=F/'registered-initial-r1';assert not B.exists();B.mkdir()
W=Path('/Users/sb/code/opensip-ai/opensip-native-owner-patterns-takeover');R='/opt/homebrew/Cellar/rust/1.95.0/bin/'
T=Path(tempfile.mkdtemp(prefix='opensip-native-registered-',dir=subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR'],text=True).strip()));T.chmod(0o700)
E=dict(os.environ,CARGO_HOME='/Users/sb/.cargo',CARGO_TARGET_DIR=str(B/'target'),TMPDIR=str(T),CC='/usr/bin/cc',CXX='/usr/bin/c++',AR='/usr/bin/ar',CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--show-sdk-path'],text=True).strip())
paths=subprocess.check_output(['/usr/bin/git','diff','--name-only'],cwd=W,text=True).splitlines();pins={p:hashlib.sha256((W/p).read_bytes()).hexdigest() for p in paths}
report=dict(standing='INITIAL ACTUAL REGISTERED CONSUMER CONTROLS; NO SELECTED GENERATION OR UNIT ACCEPTANCE',sourcePins=pins,privateTMPDIR=str(T),TMPDIRMode='0700',runs=[],productQualification=False)
for name,args in [('identity',[R+'cargo','test','--locked','--offline','-p','opensip-identity']),('host-registered',[R+'cargo','test','--locked','--offline','-p','opensip-host','--lib','native_owner_registered']),('startup-registered',[R+'cargo','test','--locked','--offline','-p','opensip-components','--lib','native_owner_registered_startup'])]:
 print(name,flush=True)
 with (B/(name+'.log')).open('wb') as out:r=subprocess.run(args,cwd=W,env=E,stdout=out,stderr=subprocess.STDOUT)
 text=(B/(name+'.log')).read_text(errors='replace');report['runs'].append(dict(name=name,exitCode=r.returncode,summaries=re.findall(r'^test result:.*$',text,re.M)));(B/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 assert r.returncode==0,(name,text[-6000:])
assert all(hashlib.sha256((W/p).read_bytes()).hexdigest()==h for p,h in pins.items())
report['allPassed']=True;(B/'report.json').write_text(json.dumps(report,indent=2)+'\n');print('REGISTERED CONSUMER CONTROLS PASS',flush=True)
