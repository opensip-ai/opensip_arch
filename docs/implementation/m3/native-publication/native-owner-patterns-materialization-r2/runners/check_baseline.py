from pathlib import Path
import os,subprocess,tempfile,json,hashlib,re
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;B=F/'baseline-r1';assert not B.exists();B.mkdir();P=Path('/Users/sb/code/opensip-ai/opensip');A=P.parent/'opensip_arch';R='/opt/homebrew/Cellar/rust/1.95.0/bin/';PY='/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'
T=Path(tempfile.mkdtemp(prefix='opensip-native-baseline-',dir=subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR'],text=True).strip()));T.chmod(0o700)
E=dict(os.environ,PATH='/opt/homebrew/bin:'+R+':/usr/bin:/bin',CARGO_HOME='/Users/sb/.cargo',CARGO_TARGET_DIR=str(B/'target'),TMPDIR=str(T),CC='/usr/bin/cc',CXX='/usr/bin/c++',AR='/usr/bin/ar',CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--show-sdk-path'],text=True).strip())
def git(*args):return subprocess.check_output(['/usr/bin/git',*args],cwd=P,text=True).strip()
head=git('rev-parse','HEAD');assert head=='19549dcb29c1e2c77f53419f18db8d0c451259aa' and not git('status','--porcelain')
report=dict(standing='ACTUAL UNCHANGED MAIN BASELINE; LIMITED HOST CONTROLS AND FULL STORAGE/EVALUATOR',head=head,privateTMPDIR=str(T),TMPDIRMode='0700',runs=[],productChanged=False)
steps=[('typescript-generator',[PY,'-I','-B','tools/check_typescript.py','--root',str(P),'--architecture',str(A),'--node','/tmp/opensip-implementation/d2b0b-materialization-r1/generation-r1/tool-node','--lane','generator']),('host-native',[R+'cargo','test','--locked','--offline','-p','opensip-host','--lib','native_owner_tests']),('host-fact',[R+'cargo','test','--locked','--offline','-p','opensip-host','--lib','fact_admission::tests']),('storage',[R+'cargo','test','--locked','--offline','-p','opensip-storage','--lib']),('evaluator',[R+'cargo','test','--locked','--offline','-p','opensip-evaluator','--lib'])]
for name,args in steps:
 print(name,flush=True)
 with (B/(name+'.log')).open('wb') as out:r=subprocess.run(args,cwd=P,env=E,stdout=out,stderr=subprocess.STDOUT)
 text=(B/(name+'.log')).read_text(errors='replace');report['runs'].append(dict(name=name,exitCode=r.returncode,summaries=re.findall(r'^test result:.*$',text,re.M),failedTests=re.findall(r'^test (\S+) \.\.\. FAILED$',text,re.M)));(B/'report.json').write_text(json.dumps(report,indent=2)+'\n')
assert git('rev-parse','HEAD')==head and not git('status','--porcelain')
report['mainUnchanged']=True;(B/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2),flush=True)
