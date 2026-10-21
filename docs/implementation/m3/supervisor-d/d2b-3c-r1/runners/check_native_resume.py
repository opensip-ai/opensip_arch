"""First fresh owning run after accepted native shapes/current receipts; no acceptance."""
from pathlib import Path
import os,subprocess,json,tempfile,hashlib,re
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;B=F/'native-resume-r1/owning-r1';assert not B.exists();B.mkdir()
W=Path('/Users/sb/code/opensip-ai/opensip-d2b3c-native-resume');P=W.parent/'opensip';A=W.parent/'opensip_arch';R='/opt/homebrew/Cellar/rust/1.95.0/bin/';PY='/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'
prep=json.loads((F/'native-resume-r1/prepared.json').read_text());base=prep['productBase'];paths=[r['path'] for r in prep['candidatePins']]
def git(root,*args):return subprocess.check_output(['/usr/bin/git',*args],cwd=root,text=True).strip()
def pin(root,path):
 raw=(root/path).read_bytes();return dict(path=path,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
assert git(P,'rev-parse','HEAD')==base==git(W,'rev-parse','HEAD') and not git(P,'status','--porcelain')
for r in prep['candidatePins']:assert pin(W,r['path'])==r
authorities=['docs/implementation/m3/supervisor-d/d2b/PLAN-r3.md','docs/implementation/m3/supervisor-d/d2b/PLAN-r3-A1.md','docs/implementation/m3/supervisor-d/d2b/PLAN-r3-A2.md','docs/implementation/m3/supervisor-d/d2b-3a-r1-unit.json','docs/implementation/m3/supervisor-d/d2b-3b-r2-unit.json','docs/implementation/m3/native-publication/native-owner-patterns-materialization-r2-unit.json','docs/implementation/m3/native-publication/native-owner-c1b-refresh-run-r1-unit.json']
authority_pins=[pin(A,p) for p in authorities]
a2=json.loads((A/authorities[3]).read_text())['acceptedAmendment'];assert pin(A,a2['planAmendment']['path'])==a2['planAmendment'] and pin(A,a2['amends']['path'])==a2['amends']
T=Path(tempfile.mkdtemp(prefix='n-',dir=subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR'],text=True).strip()));T.chmod(0o700);os.setpriority(os.PRIO_PROCESS,0,10)
E=dict(os.environ,CARGO_HOME='/Users/sb/.cargo',CARGO_TARGET_DIR=str(F/'native-resume-r1/target'),TMPDIR=str(T),CC='/usr/bin/cc',CXX='/usr/bin/c++',AR='/usr/bin/ar',CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--show-sdk-path'],text=True).strip())
with (B/'format.log').open('wb') as out:r=subprocess.run([R+'rustfmt','--edition','2024',*[str(W/p) for p in paths if p.endswith('.rs')]],cwd=W,env=E,stdout=out,stderr=subprocess.STDOUT)
assert r.returncode==0
status=subprocess.check_output(['/usr/bin/git','status','--porcelain','--untracked-files=all'],cwd=W,text=True);assert sorted(line[3:] for line in status.splitlines())==sorted(paths)
target='crates/components/src/provider_protocol/ts2_send_tests.rs';oldbase=subprocess.check_output(['/usr/bin/git','show',prep['originalRecoveredBase']+':'+target],cwd=P);accepted_append=(P/target).read_bytes()[len(oldbase):]
assert hashlib.sha256(accepted_append).hexdigest()==prep['acceptedNativeAppend']['sha256'] and accepted_append in (W/target).read_bytes()
pins=[pin(W,p) for p in paths]
source=json.loads((W/'crates/components/tests/data/trial07-admission-vectors.v1.json').read_text());selected=json.loads((W/'crates/components/tests/data/trial07-integer-replay.v1.json').read_text());excluded=selected['deferredVectors'];assert len(excluded)==1
for rule,vs in source['vectors'].items():
 expected=[v for v in vs if not (rule==excluded[0]['rule'] and v['id']==excluded[0]['id'])]
 assert selected['vectors'][rule]==expected
assert sum(map(len,source['vectors'].values()))==353 and sum(map(len,selected['vectors'].values()))==352
assert any(v==json.loads(excluded[0]['originalVectorJson']) for v in source['vectors'][excluded[0]['rule']])
r=subprocess.run([R+'cargo','test','--locked','--offline','--no-run','--message-format=json','-p','opensip-components'],cwd=W,env=E,capture_output=True);(B/'build.log').write_bytes(r.stderr);(B/'artifacts.jsonl').write_bytes(r.stdout);assert r.returncode==0
artifacts=[json.loads(l) for l in r.stdout.splitlines() if l.startswith(b'{')];bins={j['target']['name']:j for j in artifacts if j.get('reason')=='compiler-artifact' and j.get('executable')};image=bins['opensip_components'];assert image['target']['src_path']==str(W/'crates/components/src/lib.rs') and not image['fresh'];binary=Path(image['executable']);fixture=Path(bins['supervisor_fixture']['executable']);(binary.parent/'supervisor_fixture.path').write_text(str(fixture)+'\n'+hashlib.sha256(fixture.read_bytes()).hexdigest()+'\n')
report=dict(standing='FRESH RESUMED D2b3c OWNING CHECKS; UNACCEPTED DRAFT',productBase=base,architectureHeadAtStart=git(A,'rev-parse','HEAD'),sourcePins=pins,authorities=authority_pins,original353Preserved=True,selected352EqualByValue=True,deferredRust3RawFloatVector=excluded,acceptedNativeControlPreserved=True,binary=str(binary),binarySha256=hashlib.sha256(binary.read_bytes()).hexdigest(),freshCompilerArtifact=True,privateTMPDIR=str(T),TMPDIRMode='0700',runs=[],productQualification=False)
steps=[('accepted-native-startup',[str(binary),'--exact','provider_protocol::ts2::tests::send::native_owner_registered_startup_preserves_non_dot_segments_and_refuses_late_dot_segments']),('corrected-hello',[str(binary),'--exact','provider_protocol::ts2::tests::send::the_hello_is_the_selection_and_the_schema_constants']),('formerly-blocked-path-replay',[str(binary),'--exact','provider_protocol::ts2::tests::send::replay::replay_path_sites']),('full-components',[str(binary)]),('components-docs',[R+'cargo','test','--locked','--offline','-p','opensip-components','--doc']),('full-operability',[R+'cargo','test','--locked','--offline','-p','opensip-operability','--lib']),('clippy',[R+'cargo','clippy','--locked','--offline','-p','opensip-components','-p','opensip-operability','--all-targets','--','-D','warnings']),('workspace-check',[R+'cargo','check','--locked','--offline','--workspace','--all-targets']),('verify-design',[PY,'-I','-B','tools/verify_design.py','--architecture',str(A),'--implementation',str(W)])]
for name,args in steps:
 print(name,flush=True)
 with (B/(name+'.log')).open('wb') as out:r=subprocess.run(args,cwd=W,env=E,stdout=out,stderr=subprocess.STDOUT)
 text=(B/(name+'.log')).read_text(errors='replace');summaries=re.findall(r'^test result:.*$',text,re.M)
 report['runs'].append(dict(name=name,exitCode=r.returncode,testSummaries=summaries));(B/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 assert r.returncode==0,(name,text[-3000:])
 if name in ['accepted-native-startup','corrected-hello','formerly-blocked-path-replay']:assert any('1 passed; 0 failed' in s for s in summaries),name
assert all(pin(W,r['path'])==r for r in pins) and all(pin(A,r['path'])==r for r in authority_pins)
report.update(allPassed=True,architectureHeadAtEnd=git(A,'rev-parse','HEAD'));(B/'report.json').write_text(json.dumps(report,indent=2)+'\n');print('FRESH RESUMED OWNING CHECKS PASS',flush=True)
