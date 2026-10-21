"""Validate the narrow existing FA-2 dot-keyword owner route; no schema/mode changes."""
from pathlib import Path
import os,json,subprocess,tempfile,hashlib,re,shutil
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;B=F/'native-resume-r1/owning-r2';assert not B.exists();B.mkdir()
W=Path('/Users/sb/code/opensip-ai/opensip-d2b3c-native-resume');P=W.parent/'opensip';A=W.parent/'opensip_arch';R='/opt/homebrew/Cellar/rust/1.95.0/bin/';PY='/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'
def pin(root,p):
 raw=(root/p).read_bytes();return dict(path=p,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
prep=json.loads((F/'native-resume-r1/prepared.json').read_text());prior=json.loads((F/'native-resume-r1/owner-profile-r1/report.json').read_text());oldbin=Path(prior['binary']);assert hashlib.sha256(oldbin.read_bytes()).hexdigest()==prior['binarySha256'];shutil.copyfile(oldbin,B/'previous-failed-replay-binary')
git=lambda root,*args:subprocess.check_output(['/usr/bin/git',*args],cwd=root,text=True).strip()
assert git(W,'rev-parse','HEAD')==prep['productBase']==git(P,'rev-parse','HEAD') and not git(P,'status','--porcelain')
note=json.loads((F/'native-resume-r1/OWNER-PREFLIGHT-R1-LEAD-NOTE.json').read_text());assert note['limitedSourceRootAssent'] and not note['unitAccepted']
for row in note['sourcePaths']:assert pin(W,row['path'])==row
lint=F/'native-resume-r1/next-source/lint-correction.json';ld=json.loads(lint.read_text());assert not ld['applied']
target=W/ld['path'];assert hashlib.sha256(target.read_bytes()).hexdigest()==ld['beforeSha256']
replacement=(F/'native-resume-r1/next-source/ts2_census_tests.rs').read_bytes();assert hashlib.sha256(replacement).hexdigest()==ld['afterSha256'];target.write_bytes(replacement)
ld['applied']=True;ld['rootSourcePreflight']=note['subjectManifestSha256'];lint.write_text(json.dumps(ld,indent=2)+'\n')
subprocess.run([R+'rustfmt','--edition','2024',str(target)],cwd=W,check=True)
for row in note['sourcePaths']:assert pin(W,row['path'])==row

assert (W/'crates/identity/src/schema_patterns.rs').read_bytes()==(P/'crates/identity/src/schema_patterns.rs').read_bytes()
paths=[r['path'] for r in prep['candidatePins']]+['crates/identity/src/schema.rs','crates/identity/src/schema_tests.rs']
status=subprocess.check_output(['/usr/bin/git','status','--porcelain','--untracked-files=all'],cwd=W,text=True);assert sorted(line[3:] for line in status.splitlines())==sorted(paths)
T=Path(tempfile.mkdtemp(prefix='n-',dir=subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR'],text=True).strip()));T.chmod(0o700);os.setpriority(os.PRIO_PROCESS,0,10)
E=dict(os.environ,CARGO_HOME='/Users/sb/.cargo',CARGO_TARGET_DIR=str(F/'native-resume-r1/target'),TMPDIR=str(T),CC='/usr/bin/cc',CXX='/usr/bin/c++',AR='/usr/bin/ar',CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--show-sdk-path'],text=True).strip())
with (B/'format.log').open('wb') as out:r=subprocess.run([R+'rustfmt','--edition','2024',str(W/'crates/identity/src/schema.rs'),str(W/'crates/identity/src/schema_tests.rs')],cwd=W,env=E,stdout=out,stderr=subprocess.STDOUT)
assert r.returncode==0
pins=[pin(W,p) for p in paths];before=[pin(W,p) for p in ['crates/security/src/custody/discovery_census.json','crates/security/src/custody/discovery_census_held_out.json','crates/security/src/snapshot_ledger_census.json','crates/security/src/snapshot_ledger_census_held_out.json']]
report=dict(standing='FINAL RESUMED D2b3c OWNING CHECKS AFTER LIMITED OWNER PREFLIGHT AND TEST-ONLY LINT CORRECTION',productBase=prep['productBase'],sourcePins=pins,sharedPatternImplementationByteExact=True,previousFailureBinary=pin(B,'previous-failed-replay-binary'),runs=[],productQualification=False)
def run(name,args):
 print(name,flush=True)
 with (B/(name+'.log')).open('wb') as out:r=subprocess.run(args,cwd=W,env=E,stdout=out,stderr=subprocess.STDOUT)
 text=(B/(name+'.log')).read_text(errors='replace');summaries=re.findall(r'^test result:.*$',text,re.M);report['runs'].append(dict(name=name,exitCode=r.returncode,testSummaries=summaries));(B/'report.json').write_text(json.dumps(report,indent=2)+'\n');assert r.returncode==0,(name,text[-2500:]);return summaries
run('full-identity',[R+'cargo','test','--locked','--offline','-p','opensip-identity'])
r=subprocess.run([R+'cargo','test','--locked','--offline','--no-run','--message-format=json','-p','opensip-components'],cwd=W,env=E,capture_output=True);(B/'build.log').write_bytes(r.stderr);(B/'artifacts.jsonl').write_bytes(r.stdout);assert r.returncode==0
bins={j['target']['name']:j for l in r.stdout.splitlines() if l.startswith(b'{') and (j:=json.loads(l)).get('reason')=='compiler-artifact' and j.get('executable')};image=bins['opensip_components'];assert image['target']['src_path']==str(W/'crates/components/src/lib.rs') and not image['fresh'];binary=Path(image['executable']);fixture=Path(bins['supervisor_fixture']['executable']);(binary.parent/'supervisor_fixture.path').write_text(str(fixture)+'\n'+hashlib.sha256(fixture.read_bytes()).hexdigest()+'\n');report.update(binary=str(binary),binarySha256=hashlib.sha256(binary.read_bytes()).hexdigest(),freshCompilerArtifact=True)
for name,filter_ in [('accepted-native-startup','provider_protocol::ts2::tests::send::native_owner_registered_startup_preserves_non_dot_segments_and_refuses_late_dot_segments'),('formerly-blocked-path-replay','provider_protocol::ts2::tests::send::replay::replay_path_sites')]:
 summaries=run(name,[str(binary),'--exact',filter_]);assert any('1 passed; 0 failed' in s for s in summaries)
run('full-components',[str(binary)])
run('components-docs',[R+'cargo','test','--locked','--offline','-p','opensip-components','--doc'])
run('full-operability',[R+'cargo','test','--locked','--offline','-p','opensip-operability','--lib'])
run('clippy',[R+'cargo','clippy','--locked','--offline','-p','opensip-identity','-p','opensip-components','-p','opensip-operability','--all-targets','--','-D','warnings'])
run('workspace-check',[R+'cargo','check','--locked','--offline','--workspace','--all-targets'])
run('verify-design',[PY,'-I','-B','tools/verify_design.py','--architecture',str(A),'--implementation',str(W)])
helper=A/'docs/implementation/m3/native-publication/native-owner-c1b-refresh-r1/evidence/freeze_c1b_refresh.py';bindings=json.loads(subprocess.check_output([PY,'-I','-B',str(helper),'--bindings',str(W),str(A),str(P)],cwd=W,env=E));actual={n:json.loads((W/p).read_text())['bindings'] for n,p in [('discovery',before[1]['path']),('companion',before[3]['path'])]};assert bindings==actual
assert all(pin(W,r['path'])==r for r in pins+before)
report.update(allPassed=True,publicReceiptBindingsUnchanged=True,receiptAndCensusPinsUnchanged=before,realBlindInvocations=0);(B/'report.json').write_text(json.dumps(report,indent=2)+'\n');print('FA2 OWNER PROFILE AND RESUMED OWNING CHECKS PASS',flush=True)
