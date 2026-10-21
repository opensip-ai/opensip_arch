from pathlib import Path
import os, subprocess, json, hashlib, tempfile, importlib.util, re
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;B=F/'repository-r2';B.mkdir(exist_ok=False)
W=Path('/Users/sb/code/opensip-ai/opensip-platform-fd3-test-repair');P=W.parent/'opensip';A=W.parent/'opensip_arch'
path='crates/platform/src/harness_descriptor.rs';raw=(W/path).read_bytes();assert hashlib.sha256(raw).hexdigest()==json.loads((F/'owning-r1/report.json').read_text())['source']['sha256']
ph=subprocess.check_output(['git','rev-parse','HEAD'],cwd=P,text=True).strip();subprocess.run(['git','checkout','--detach',ph],cwd=W,check=True);assert (W/path).read_bytes()==raw
spec=importlib.util.spec_from_file_location('check_op',W/'tools/check_operability.py');op=importlib.util.module_from_spec(spec);spec.loader.exec_module(op)
p='tools/operability/exceptions.json';old=json.loads((W/p).read_text());proposed=op.proposed_rows(W)
old_by={(r['path'],r['class']):r for r in old['rows']}; proposed_by={(r['path'],r['class']):r for r in proposed['rows']}
newrows=[r for key,r in proposed_by.items()if key not in old_by];removed=[r for key,r in old_by.items()if key not in proposed_by]
assert all(proposed_by[k]['count']==r['count']for k,r in old_by.items()), 'existing counts must stay exact; accepted explicit owners preserved'
assert newrows==[dict(path=path,**{'class':'process'},count=2,owner='platform custody owners')],newrows
assert not removed and proposed['mintAudit']['rows']==old['mintAudit']['rows']
new=dict(old,rows=sorted(old['rows']+newrows,key=lambda r:(r['path'],r['class'])));(W/p).write_text(json.dumps(new,indent=2)+'\n');assert len(old['rows'])==114 and len(new['rows'])==115 and len(new['mintAudit']['rows'])==453
(B/'census-delta.json').write_text(json.dumps(dict(added=newrows,removed=removed,oldRows=114,newRows=115,mintRows=453,mintAuditByteValueUnchanged=True,otherTopLevelFieldsUnchanged=True,scope='CommandExt import and Command::new in cfg(test) isolation helper; conservative lexical rows, no production process authority'),indent=2)+'\n')
R='/opt/homebrew/Cellar/rust/1.95.0/bin/';PY='/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'
T=Path(tempfile.mkdtemp(prefix='n-',dir=subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR'],text=True).strip()));T.chmod(0o700);os.setpriority(os.PRIO_PROCESS,0,10)
E=dict(os.environ,CARGO_HOME='/Users/sb/.cargo',CARGO_TARGET_DIR=str(F/'target'),TMPDIR=str(T),CC='/usr/bin/cc',CXX='/usr/bin/c++',AR='/usr/bin/ar',CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--show-sdk-path'],text=True).strip());E.pop('RUST_TEST_THREADS',None)
report=dict(parent=ph,standing='Unaccepted cfg(test)-only platform isolation and exact lexical census delta',runs=[],productQualification=False)
def run(name,args):
 with (B/(name+'.log')).open('wb')as out:r=subprocess.run(args,cwd=W,env=E,stdout=out,stderr=subprocess.STDOUT)
 report['runs'].append(dict(name=name,exitCode=r.returncode));assert r.returncode==0,name
run('cargo-metadata',[R+'cargo','metadata','--locked','--offline','--format-version','1']);(B/'metadata.json').write_bytes((B/'cargo-metadata.log').read_bytes())
run('package-edges',[PY,'-I','-B','tools/check_package_edges.py','--repository',str(W),'--metadata',str(B/'metadata.json'),'--inventory',str(A/'docs/implementation/m2/repository-file-inventory.v236.json'),'--lane','host','--architecture',str(A),'--lock',str(W/'design-lock.json'),'--package-policy',str(A/'docs/implementation/m3/operability/o1-package-policy-r1/package-policy.json')])
run('operability-source',[PY,'-I','-B','tools/check_operability.py','source','--repository',str(W)])
run('environment-exceptions',[PY,'-I','-B','tools/tests/test_environment_exceptions.py','-v'])
run('platform-test-fixture',[R+'cargo','test','--locked','--offline','-p','opensip-platform','--features','test-fixture'])
run('platform-clippy-test-fixture',[R+'cargo','clippy','--locked','--offline','-p','opensip-platform','--all-targets','--features','test-fixture','--','-D','warnings'])
run('verify-design',[PY,'-I','-B','tools/verify_design.py','--architecture',str(A)])
run('diff-check',['git','diff','--check'])
closure=set(re.findall(r"\('(crates/[^']+)', \d+, '[0-9a-f]{64}'\)",(W/'tools/security/discovery_census.py').read_text()));assert len(closure)>=10 and path not in closure
run('public-bindings',[PY,'-I','-B',str(A/'docs/implementation/m3/native-publication/native-owner-c1b-refresh-r1/evidence/freeze_c1b_refresh.py'),'--bindings',str(W),str(A),str(P)])
# Compare public receipt binding metadata only, never held-out rows.
bindings=json.loads((B/'public-bindings.log').read_text())
(B/'public-bindings.json').write_text(json.dumps(bindings,indent=2)+'\n')
assert (W/path).read_bytes()==raw
report.update(allPassed=True,sourcePins=[dict(path=p,bytes=(W/p).stat().st_size,sha256=hashlib.sha256((W/p).read_bytes()).hexdigest())for p in [path,'tools/operability/exceptions.json']],productionPrefixByteExact=raw.split(b'#[cfg(test)]')[0]==(P/path).read_bytes().split(b'#[cfg(test)]')[0],closureFilesUnchanged=True,realBlindInvocations=0)
assert report['productionPrefixByteExact']
(B/'report.json').write_text(json.dumps(report,indent=2)+'\n');print('REPOSITORY/FEATURE CHECKS PASS')
