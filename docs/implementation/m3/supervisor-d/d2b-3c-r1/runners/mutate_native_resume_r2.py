"""Fresh compiled runtime mutations, with exact thirteen-file restoration each time."""
from pathlib import Path
import os,json,subprocess,tempfile,hashlib,shutil,re
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;B=F/'native-resume-r1/mutations-r2';assert not B.exists();B.mkdir()
W=Path('/Users/sb/code/opensip-ai/opensip-d2b3c-native-resume');P=W.parent/'opensip';R='/opt/homebrew/Cellar/rust/1.95.0/bin/'
own=json.loads((F/'native-resume-r1/owning-r3-retry/report.json').read_text());assert own['allPassed'] and own['publicReceiptBindingsUnchanged'];pins=own['sourcePins'];baseline={r['path']:(W/r['path']).read_bytes() for r in pins}
def pin(root,p):
 raw=(root/p).read_bytes();return dict(path=p,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
def restored():
 for r in pins:assert pin(W,r['path'])==r
restored();oldbin=Path(own['binary']);assert hashlib.sha256(oldbin.read_bytes()).hexdigest()==own['binarySha256'];shutil.copyfile(oldbin,B/'owning-positive-binary')
T=Path(tempfile.mkdtemp(prefix='n-',dir=subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR'],text=True).strip()));T.chmod(0o700);os.setpriority(os.PRIO_PROCESS,0,10)
E=dict(os.environ,CARGO_HOME='/Users/sb/.cargo',CARGO_TARGET_DIR=str(F/'native-resume-r1/target'),TMPDIR=str(T),CC='/usr/bin/cc',CXX='/usr/bin/c++',AR='/usr/bin/ar',CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--show-sdk-path'],text=True).strip())
ID='crates/identity/src/schema.rs';RX='crates/components/src/provider_protocol/ts2.rs';TEST='crates/components/src/provider_protocol/ts2_census_tests.rs';PART='crates/components/src/provider_protocol/ts2/participant.rs';CP='provider_protocol::ts2::tests::send::census::'
probe_old='''    assert!(matches!(
        r.receive(frame("Complete", seq, v2)),
        Err(Ts2Refusal::Schema(_))
    ));'''
probe_new='''    let token_probe = r.receive(frame("Complete", seq, v2));
    assert!(
        matches!(&token_probe, Err(Ts2Refusal::Schema(_))),
        "token-mismatch probe: {token_probe:?}"
    );'''
mutants=[
 dict(id='census-owner-guard-removed',package='opensip-identity',test='schema_tests::symbol_census_dot_keyword_uses_ecma_end_only_in_the_pinned_owner_profile',path=ID,old='            && owner == "opensip.product.symbol-census.1"\n',new='',witness='assertion `left == right` failed'),
 dict(id='census-keyword-guard-removed',package='opensip-identity',test='schema_tests::symbol_census_profile_preserves_other_patterns_and_pattern_property_semantics',path=ID,old='            && pattern == r##"(^|/)\\.\\.?(/|$)"##\n',new='',witness='panicked'),
 dict(id='census-token-mismatch-accepted',package='opensip-components',test=CP+'a_census_payload_must_match_the_token',path=RX,old='_ if name == "Complete" && self.census => {',new='_ if name == "Complete" && (self.census || matches!(payload, Value::Map(f) if field(f, "symbolCensus").is_some())) => {',probe=True,witness='token-mismatch probe: Ok('),
 dict(id='census-null-request-join-unchecked',package='opensip-components',test=CP+'a_malformed_census_is_refused',path=RX,old='if (*census == Value::Null) == requested {',new='if false && (*census == Value::Null) == requested {',witness='a wrongly null census: Ok('),
 dict(id='census-row-examined-extent-unchecked',package='opensip-components',test=CP+'a_malformed_census_is_refused',path=RX,old='if !paths.contains(path) {',new='if false && !paths.contains(path) {',witness='a row off the examined extent: Ok('),
 dict(id='census-byte-bound-one-over-admitted',package='opensip-components',test=CP+'the_census_bounds_are_exact',path=RX,old='if bytes > CENSUS_MAX_BYTES {',new='if bytes > CENSUS_MAX_BYTES + 1 {',witness='4194305 bytes: Ok('),
 dict(id='census-terminal-not-handed-to-H',package='opensip-components',test=CP+'the_handoff_carries_the_received_census_and_entries',path=PART,old='    "Complete",\n',new='    "FactBatch",\n',witness='assertion `left == right` failed'),
 dict(id='census-late-signature-token-unchecked',package='opensip-components',test=CP+'wide_signature_token_rows_are_admitted_without_weakening_item_or_count_bounds',path=RX,old='for token in tokens.iter().skip(1) {',new='for token in tokens.iter().skip(tokens.len()) {',witness='late signature token over maxLength: Err(Admission'),
 dict(id='census-signature-token-count-unchecked',package='opensip-components',test=CP+'wide_signature_token_rows_are_admitted_without_weakening_item_or_count_bounds',path=RX,old='if tokens.len() as u64 > law.tokens_max {',new='if false && tokens.len() as u64 > law.tokens_max {',witness='signature token count above maxItems: Ok('),
]
for m in mutants:assert baseline[m['path']].decode().count(m['old'])==1,(m['id'],'ambiguous edit')
assert baseline[TEST].decode().count(probe_old)==1
report=dict(standing='COMPILED RUNTIME REGRESSION CONTROLS; NOT UNIT ACCEPTANCE',baselineSourcePins=pins,owningPositiveBinary=pin(B,'owning-positive-binary'),cases=[],allRestored=False,productQualification=False)
def save(): (B/'report.json').write_text(json.dumps(report,indent=2)+'\n')
def compile_case(folder,package):
 r=subprocess.run([R+'cargo','test','--locked','--offline','--no-run','--message-format=json','--lib','-p',package],cwd=W,env=E,capture_output=True);(folder/'build.log').write_bytes(r.stderr);(folder/'artifacts.jsonl').write_bytes(r.stdout)
 if r.returncode:raise RuntimeError('Rust compile failure is not a mutation kill: '+str(folder))
 name=package.replace('-','_');bins=[j for l in r.stdout.splitlines() if l.startswith(b'{') and (j:=json.loads(l)).get('reason')=='compiler-artifact' and j.get('executable') and j['target']['name']==name]
 assert len(bins)==1 and not bins[0]['fresh'],(folder,'not a fresh tested compiler artifact')
 binary=Path(bins[0]['executable']);return binary,dict(path=str(binary),bytes=binary.stat().st_size,sha256=hashlib.sha256(binary.read_bytes()).hexdigest(),freshCompilerArtifact=True)
def execute(folder,binary,test):
 r=subprocess.run([str(binary),'--exact',test],cwd=W,env=E,capture_output=True);raw=r.stdout+r.stderr;(folder/'runtime.log').write_bytes(raw);return r.returncode,raw.decode(errors='replace')
for m in mutants:
 restored();folder=B/m['id'];folder.mkdir();row=dict(id=m['id'],package=m['package'],test=m['test'],edit=dict(path=m['path'],before=m['old'],after=m['new']),caught=False,allSourceBytesRestored=False,restoredPositive=False);report['cases'].append(row);save();error=None
 try:
  if m.get('probe'):
   (W/TEST).write_text(baseline[TEST].decode().replace(probe_old,probe_new));pf=folder/'probe-positive';pf.mkdir();binary,bpin=compile_case(pf,m['package']);code,text=execute(pf,binary,m['test']);assert code==0 and '1 passed; 0 failed' in text
   row['diagnosticProbe']=dict(path=TEST,before=probe_old,after=probe_new,baselinePassed=True,binary=bpin)
  (W/m['path']).write_text(baseline[m['path']].decode().replace(m['old'],m['new']));binary,bpin=compile_case(folder,m['package']);code,text=execute(folder,binary,m['test']);row.update(binary=bpin,runtimeExitCode=code,evidenceMarker=m['witness'],evidenceMarkerObserved=m['witness'] in text)
  assert code!=0 and '0 passed; 1 failed' in text and m['witness'] in text,(m['id'],'no intended runtime witness',text[-2000:]);row['caught']=True
 except BaseException as ex:
  error=ex;row['error']=repr(ex)
 finally:
  for path,raw in baseline.items():
   if (W/path).read_bytes()!=raw:(W/path).write_bytes(raw)
  restored();row['allSourceBytesRestored']=True;save()
  pf=folder/'restored-positive';pf.mkdir();binary,bpin=compile_case(pf,m['package']);code,text=execute(pf,binary,m['test']);row.update(restoredPositive=code==0 and '1 passed; 0 failed' in text,restoredBinary=bpin);save();assert row['restoredPositive'],m['id']
 if error:raise error
 print(m['id'],'runtime-caught/restored-positive',flush=True)
restored();report.update(allRestored=True,allCaught=len(report['cases'])==len(mutants) and all(r['caught'] and r['restoredPositive'] for r in report['cases']),compiledRuntimeMutants=len(mutants),realBlindInvocations=0);save();print('ALL9COMPILED MUTANTS CAUGHT;13SOURCE PINS RESTORED',flush=True)
