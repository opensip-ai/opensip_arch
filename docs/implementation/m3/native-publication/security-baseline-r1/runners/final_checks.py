from pathlib import Path
import os,subprocess,json,hashlib,re,tempfile,difflib
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;W=Path('/Users/sb/code/opensip-ai/opensip-security-baseline-takeover');A=W.parent/'opensip_arch';O=F/'final-r1';O.mkdir();R='/opt/homebrew/Cellar/rust/1.95.0/bin/';PY='/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'
base=json.loads((F/'initial-r1/report.json').read_text());assert base['allRequiredChecksPassed'] and base['baselineFourteenReproduced'] and base['candidateFourteenResolved'];original={p:(W/p).read_bytes() for p in base['sourcePins']};assert all(hashlib.sha256(b).hexdigest()==base['sourcePins'][p] for p,b in original.items())
T=Path(tempfile.mkdtemp(prefix='opensip-security-final-',dir=subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR'],text=True).strip()));T.chmod(0o700)
E=dict(os.environ,PATH='/opt/homebrew/bin:'+R+':/usr/bin:/bin',CARGO_HOME='/Users/sb/.cargo',CARGO_TARGET_DIR=str(F/'initial-r1/candidate-target'),CARGO=R+'cargo',RUSTC=R+'rustc',TMPDIR=str(T),CC='/usr/bin/cc',CXX='/usr/bin/c++',AR='/usr/bin/ar',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--show-sdk-path'],text=True).strip());E.pop('RUST_TEST_THREADS',None)
J='crates/security/src/journal_store.rs';G='crates/security/src/custody/commit_session_tests.rs';s=original[J].decode();a=s.index('        // The historical journal cases remain immutable.');b=s.index('        let c = object(&f["case"]).unwrap();',a);replay=s[a:b];s=original[G].decode();a=s.index('        let helper_calls = |text: &str| {');b=s.index('        let own_calls = helper_calls(&source);',a);counter=s[a:b]
mutants=[('historical-replay-selected',J,replay,'        let f = fixture();\n        let f = object(&object(&f).unwrap()["replay"]).unwrap();\n',['commit_authority::seal_binding_tests::']),('unbounded-self-receiver',G,counter,'        let helper_calls = |text: &str| { text.lines().filter(|line| !line.trim_start().starts_with("//")).map(|line| line.matches("self.settle(").count()).sum::<usize>() };\n',['--exact','custody::operation_handoff::tests::session::the_settlement_reserve_has_one_production_caller_each'])]
report=dict(standing='COMPLETE TEST-ONLY REPAIR VERIFICATION; INDEPENDENT UNIT ACCEPTANCE STILL REQUIRED',sourcePins=base['sourcePins'],mutations=[],rows=[],restored=False,privateTMPDIR=str(T),unitAccepted=False,productQualification=False)
def save():(O/'report.json').write_text(json.dumps(report,indent=2)+'\n')
def build(label,changed):
 r=subprocess.run([R+'cargo','test','--locked','--offline','--no-run','--lib','--message-format=json','-p','opensip-security'],cwd=W,env=E,capture_output=True);(O/(label+'-build.log')).write_bytes(r.stderr);(O/(label+'-artifacts.jsonl')).write_bytes(r.stdout);assert r.returncode==0,(label,r.stderr[-5000:]);hits=[j for line in r.stdout.splitlines() if line.startswith(b'{') for j in [json.loads(line)] if j.get('reason')=='compiler-artifact' and j.get('target',{}).get('name')=='opensip_security' and j.get('profile',{}).get('test') and j.get('executable')];assert len(hits)==1 and hits[0]['target']['src_path']==str(W/'crates/security/src/lib.rs');assert not changed or hits[0]['fresh'] is False;return Path(hits[0]['executable'])
try:
 for name,path,before,after,args in mutants:
  try:
   source=original[path].decode();assert source.count(before)==1;(W/path).write_text(source.replace(before,after));(O/(name+'.diff')).write_text(''.join(difflib.unified_diff(source.splitlines(True),(W/path).read_text().splitlines(True),fromfile='before/'+path,tofile='mutated/'+path)))
   binary=build(name,True)
   with (O/(name+'.log')).open('wb') as log:r=subprocess.run([str(binary),*args],cwd=W,env=E,stdout=log,stderr=subprocess.STDOUT,timeout=120)
   out=(O/(name+'.log')).read_text();assert r.returncode==101 and 'test result: FAILED.' in out and re.search(r'[1-9]\d* failed;',out),(name,out[-5000:]);report['mutations'].append(dict(name=name,path=path,binarySha256=hashlib.sha256(binary.read_bytes()).hexdigest(),exitCode=r.returncode,compiledFresh=True,runtimeFailure=True,failed=sorted(set(re.findall(r'^test (\S+) \.\.\. FAILED$',out,re.M)))));save();print(name,'caught',flush=True)
  finally:(W/path).write_bytes(original[path])
finally:
 assert all((W/p).read_bytes()==b for p,b in original.items());report['restored']=True;save()
binary=build('restored',True)
with (O/'restored-fourteen.log').open('wb') as log:r=subprocess.run([str(binary),'--exact',*base['baselineFailures']],cwd=W,env=E,stdout=log,stderr=subprocess.STDOUT,timeout=120)
assert r.returncode==0 and '14 passed; 0 failed; 0 ignored;' in (O/'restored-fourteen.log').read_text();report['restoredFourteenPasses']=14
steps=[('workspace-check',[R+'cargo','check','--locked','--offline','--workspace','--all-targets']),('security-fixtures-check',[R+'cargo','check','--locked','--offline','-p','opensip-security','--all-targets','--features','scenario-fixtures,crash-matrix']),('environment',[PY,'-I','-B','tools/tests/test_environment_exceptions.py','-v']),('operability-source',[PY,'-I','-B','tools/check_operability.py','source','--repository',str(W)]),('operability-lock',[PY,'-I','-B','tools/check_operability.py','lock','--repository',str(W)]),('receipt-inputs-unchanged',[PY,'-I','-B','/tmp/opensip-implementation/ci3l-2026-10-20/receipt_inputs.py',str(W),str(O/'receipt-inputs.json')]),('design',[PY,'-I','-B','tools/verify_design.py','--architecture',str(A),'--implementation',str(W)])]
for name,args in steps:
 print(name,flush=True)
 with (O/(name+'.log')).open('wb') as log:r=subprocess.run(args,cwd=W,env=E,stdout=log,stderr=subprocess.STDOUT)
 report['rows'].append(dict(name=name,exitCode=r.returncode));save();assert r.returncode==0,(name,(O/(name+'.log')).read_text()[-4000:])
prep=json.loads((F/'PREPARATION.json').read_text())
for key in ['historicalJournalFixture','historicalHostFixture','acceptedCurrentHostFixture']:
 p=prep[key];assert hashlib.sha256((W/p['path']).read_bytes()).hexdigest()==p['sha256']
old=subprocess.check_output(['/usr/bin/git','show','HEAD:'+J],cwd=W);marker=b'#[cfg(test)]\npub(super) mod fixtures {';assert old.split(marker)[0]==(W/J).read_bytes().split(marker)[0];report['productionJournalPrefixUnchanged']=True;report['historicalFixturesUnchanged']=True;report['allRequiredChecksPassed']=True;report['allMutantsCaught']=len(report['mutations'])==2;assert all((W/p).read_bytes()==b for p,b in original.items());save();print('Final checks passed; source restored; full unit review and additive inventory still owed',flush=True)
