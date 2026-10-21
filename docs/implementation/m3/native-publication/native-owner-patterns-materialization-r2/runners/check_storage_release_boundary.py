"""Check unchanged production exclusion of the newly selected synthetic helper."""
from pathlib import Path
import os,subprocess,json,hashlib,tempfile
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;B=F/'storage-release-boundary-r1';assert not B.exists();B.mkdir()
W=Path('/Users/sb/code/opensip-ai/opensip-native-owner-patterns-takeover')
R='/opt/homebrew/Cellar/rust/1.95.0/bin/'
T=Path(tempfile.mkdtemp(prefix='opensip-storage-release-',dir=subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR'],text=True).strip()));T.chmod(0o700)
E=dict(os.environ,PATH='/opt/homebrew/bin:'+R+':/usr/bin:/bin',CARGO_HOME='/Users/sb/.cargo',CARGO_TARGET_DIR=str(F/'registered-initial-r1/target'),TMPDIR=str(T),CC='/usr/bin/cc',CXX='/usr/bin/c++',AR='/usr/bin/ar',CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--show-sdk-path'],text=True).strip())
checks=json.loads((F/'full-r4/report.json').read_text());assert checks['allPassed'] and checks['selectedGenerationInputsStillExact']==352
for p,h in checks['sourcePins'].items():assert hashlib.sha256((W/p).read_bytes()).hexdigest()==h
results=[]
for name,extra,success in [('normal-release',[],True),('crash-feature-release-refuses',['--features','crash-matrix'],False)]:
    args=[R+'cargo','check','--locked','--offline','--release','-p','opensip-storage',*extra]
    proc=subprocess.run(args,cwd=W,env=E,capture_output=True)
    output=(proc.stdout+proc.stderr).decode(errors='replace');(B/(name+'.log')).write_text(output)
    passed=proc.returncode==0 if success else proc.returncode!=0 and 'the crash-matrix feature is test-only' in output and 'refuses every build without debug assertions' in output
    results.append(dict(name=name,args=args,exitCode=proc.returncode,passed=passed,expectedRefusal=not success))
for p,h in checks['sourcePins'].items():assert hashlib.sha256((W/p).read_bytes()).hexdigest()==h
report=dict(standing='BOUNDED STORAGE RELEASE FEATURE BOUNDARY; NOT RELEASE QUALIFICATION',runs=results,allPassed=all(r['passed'] for r in results),sourcePinsUnchanged=True,privateTMPDIR=str(T),TMPDIRMode='0700',productQualification=False)
(B/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2));assert report['allPassed']
