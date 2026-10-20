from pathlib import Path
import os,subprocess,json,tempfile,hashlib,re
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
W=Path('/Users/sb/code/opensip-ai/opensip-d5-0-takeover');A=W.parent/'opensip_arch';F=Path(__file__).parent;O=F/'owning-r2';O.mkdir()
R='/opt/homebrew/Cellar/rust/1.95.0/bin/';P='/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'
tmp=Path(tempfile.mkdtemp(prefix='opensip-d5-owning-',dir=subprocess.check_output(['getconf','DARWIN_USER_TEMP_DIR'],text=True).strip()));tmp.chmod(0o700)
E=dict(os.environ,PATH='/opt/homebrew/bin:'+R+':/usr/bin:/bin',CARGO_HOME='/Users/sb/.cargo',CARGO_TARGET_DIR=str(F/'candidate-r3/target'),CARGO=R+'cargo',RUSTC=R+'rustc',TMPDIR=str(tmp),CC='/usr/bin/cc',CXX='/usr/bin/c++',AR='/usr/bin/ar',SDKROOT=subprocess.check_output(['xcrun','--show-sdk-path'],text=True).strip(),GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null')
for k in ['GIT_DIR','GIT_WORK_TREE','GIT_CONFIG_COUNT']:E.pop(k,None)
p=W/'crates/components/src/supervisor_tests.rs';raw=p.read_bytes();rows=[]
checks=[('clippy',[R+'cargo','clippy','--locked','--offline','-p','opensip-components','--all-targets','--','-D','warnings']),('doctests',[R+'cargo','test','--locked','--offline','--doc','-p','opensip-components']),('format',[R+'rustfmt','--edition','2024','--check',str(p)]),('environment',[P,'-I','-B','tools/tests/test_environment_exceptions.py','-v']),('operability-source',[P,'-I','-B','tools/check_operability.py','source','--repository',str(W)]),('operability-lock',[P,'-I','-B','tools/check_operability.py','lock','--repository',str(W)]),('design',[P,'-I','-B','tools/verify_design.py','--architecture',str(A),'--implementation',str(W)])]
for name,args in checks:
 with (O/(name+'.log')).open('wb') as f:r=subprocess.run(args,cwd=W,env=E,stdout=f,stderr=subprocess.STDOUT)
 rows.append(dict(name=name,exitCode=r.returncode));(O/'report.json').write_text(json.dumps(dict(sourceSha256=hashlib.sha256(raw).hexdigest(),checks=rows),indent=2)+'\n');print(name,r.returncode,flush=True)
assert p.read_bytes()==raw
assert all(x['exitCode']==0 for x in rows),rows
