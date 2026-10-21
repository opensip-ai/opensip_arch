from pathlib import Path
import os,subprocess,tempfile,json,hashlib,re
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;B=F/'companion-focused-r2';assert not B.exists();B.mkdir();W=Path('/Users/sb/code/opensip-ai/opensip-native-owner-patterns-takeover');R='/opt/homebrew/Cellar/rust/1.95.0/bin/'
T=Path(tempfile.mkdtemp(prefix='opensip-companion-focus-',dir=subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR'],text=True).strip()));T.chmod(0o700)
E=dict(os.environ,CARGO_HOME='/Users/sb/.cargo',CARGO_TARGET_DIR=str(F/'registered-initial-r1/target'),TMPDIR=str(T),CC='/usr/bin/cc',CXX='/usr/bin/c++',AR='/usr/bin/ar',CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--show-sdk-path'],text=True).strip())
git=lambda *a:subprocess.check_output(['/usr/bin/git',*a],cwd=W,text=True).strip()
paths=git('diff','--name-only').splitlines()+git('ls-files','--others','--exclude-standard').splitlines();pins={p:hashlib.sha256((W/p).read_bytes()).hexdigest() for p in paths};assert len(paths)==40
report=dict(standing='FOCUSED ACTUAL COMPANION CONTROLS; COMPLETE UNIT ACCEPTANCE STILL REQUIRED',privateTMPDIR=str(T),TMPDIRMode='0700',sourcePins=pins,runs=[],allPassed=False,productQualification=False)
steps=[('host-execution','host','native_owner_tests::execution_inputs_recheck_retained_selection_and_capture_without_outputs'),('host-full-walk','host','native_owner_tests::full_retained_walk_checks_complete_inputs_faults_and_separate_limits'),('host-reconstruction','host','native_owner_tests::reconstructs_retained_evaluator_inputs_without_run_outputs')]
for name,pkg,pattern in steps:
 print(name,flush=True);args=[R+'cargo','test','--locked','--offline','-p','opensip-'+pkg,'--lib']
 if pattern:args += [pattern]
 with (B/(name+'.log')).open('wb') as out:r=subprocess.run(args,cwd=W,env=E,stdout=out,stderr=subprocess.STDOUT)
 text=(B/(name+'.log')).read_text(errors='replace');report['runs'].append(dict(name=name,exitCode=r.returncode,summaries=re.findall(r'^test result:.*$',text,re.M),failedTests=re.findall(r'^test (\S+) \.\.\. FAILED$',text,re.M)));(B/'report.json').write_text(json.dumps(report,indent=2)+'\n')
assert all(hashlib.sha256((W/p).read_bytes()).hexdigest()==h for p,h in pins.items())
report['allPassed']=all(r['exitCode']==0 for r in report['runs']);report['sourcePinsUnchanged']=True;(B/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(allPassed=report['allPassed'],failures=[r['name'] for r in report['runs'] if r['exitCode']]),indent=2),flush=True)
