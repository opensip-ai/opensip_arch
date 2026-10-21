from pathlib import Path
import os,json,subprocess,tempfile,hashlib,re
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;B=F/'inherited-boundary-focused-r1';assert not B.exists();B.mkdir();W=Path('/Users/sb/code/opensip-ai/opensip-native-owner-patterns-takeover');R='/opt/homebrew/Cellar/rust/1.95.0/bin/'
T=Path(tempfile.mkdtemp(prefix='opensip-owner-boundary-',dir=subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR'],text=True).strip()));T.chmod(0o700)
E=dict(os.environ,PATH='/opt/homebrew/bin:'+R+':/usr/bin:/bin',CARGO_HOME='/Users/sb/.cargo',CARGO_TARGET_DIR=str(F/'registered-initial-r1/target'),TMPDIR=str(T),CC='/usr/bin/cc',CXX='/usr/bin/c++',AR='/usr/bin/ar',CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--show-sdk-path'],text=True).strip())
checks=[]
for name,args in [('identity',[R+'cargo','test','--locked','--offline','-p','opensip-identity']),('registered-host',[R+'cargo','test','--locked','--offline','-p','opensip-host','--lib','native_owner_registered']),('provider-paths',[R+'cargo','test','--locked','--offline','-p','opensip-components','--lib','native_owner_'])]:
 print(name,flush=True)
 r=subprocess.run(args,cwd=W,env=E,capture_output=True);raw=r.stdout+r.stderr;(B/(name+'.log')).write_bytes(raw);checks.append(dict(name=name,exitCode=r.returncode,summaries=re.findall(r'^test result:.*$',raw.decode(errors='replace'),re.M)))
report=dict(requiredFinding='OWNPAT-UNIT-R1-RF-1',checks=checks,allPassed=all(r['exitCode']==0 for r in checks),privateTMPDIR=str(T),TMPDIRMode='0700',sourcePins={r['path']:hashlib.sha256((W/r['path']).read_bytes()).hexdigest() for r in json.loads((F/'inherited-boundary-fix-r1/report.json').read_text())['changedPaths']},unitAccepted=False)
(B/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2));assert report['allPassed']
