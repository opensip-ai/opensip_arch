from pathlib import Path
import os,json,subprocess,tempfile,hashlib,shutil
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;B=F/'receiver-mutations-r2';assert not B.exists();B.mkdir();W=Path('/Users/sb/code/opensip-ai/opensip-d2b4a-takeover');R='/opt/homebrew/Cellar/rust/1.95.0/bin/';own=json.loads((F/'repository-r2/report.json').read_text());assert own['allPassed'];pins=own['sourcePins'];assert len(pins)==20 and len({p['path']for p in pins})==20;baseline={p['path']:(W/p['path']).read_bytes()for p in pins}
def restored():
 for p in pins:assert hashlib.sha256((W/p['path']).read_bytes()).hexdigest()==p['sha256']
restored();T=Path(tempfile.mkdtemp(prefix='n-',dir=subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR'],text=True).strip()));T.chmod(0o700);os.setpriority(os.PRIO_PROCESS,0,10)
E=dict(os.environ,CARGO_HOME='/Users/sb/.cargo',CARGO_TARGET_DIR=str(F/'target'),TMPDIR=str(T),CC='/usr/bin/cc',CXX='/usr/bin/c++',AR='/usr/bin/ar',CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--show-sdk-path'],text=True).strip());RC='crates/components/src/provider_protocol/rust3/receive.rs';AC='crates/components/src/provider_protocol/rust3/accounting.rs';P='provider_protocol::rust3::receive::tests::'
cases=[
 dict(id='dispatch-fact-batch-stage-correlation-skipped',path=RC,old='if text_of(f, "stageId") != Some(binding.expected_stage_id.as_str())\n            || u64_of(f, "batchIndex")',new='if false && (text_of(f, "stageId") != Some(binding.expected_stage_id.as_str()))\n            || u64_of(f, "batchIndex")',test=P+'rust3_receive_misordered_stages_ordinals_and_batches_never_publish',witness='Err(Rust3Refusal::Admission(_))'),
 dict(id='hello-optional-token-echo-skipped',path=RC,old='field(f, "capabilities") != field(hello, "expectedCapabilities")',new='false && (field(f, "capabilities") != field(hello, "expectedCapabilities"))',test=P+'rust3_receive_optional_token_omission_is_an_exact_echo_failure',witness='offered optional token omission must refuse before disclosure'),
 dict(id='t016-batch-index-skipped',path=RC,old='u64_of(f, "batchIndex") != Some(live.batches)',new='false && (u64_of(f, "batchIndex") != Some(live.batches))',test=P+'rust3_receive_misordered_stages_ordinals_and_batches_never_publish',witness='Err(Rust3Refusal::Admission(_))'),
 dict(id='provider-fault-joint-window-skipped',path=RC,old='if !self.fault_window.matches(payload) {',new='if false && !self.fault_window.matches(payload) {',test=P+'rust3_receive_provider_fault_joint_window_is_wired_before_p3t',witness='joint worker observation must refuse'),
 dict(id='received-profile-proof-skipped',path=RC,old='if frame.profile() != cbor::Profile::Rust3 {',new='if false && frame.profile() != cbor::Profile::Rust3 {',test=P+'rust3_receive_raw_commitment_mismatch_and_wrong_profile_refuse',witness='Err(Rust3Refusal::Envelope(_))'),
 dict(id='received-commitment-parts-reencoded',path=RC,old="fn commit(domain: &str, parts: &[ReceivedBytes<'_>]) -> String {",new="""fn commit(domain: &str, parts: &[ReceivedBytes<'_>]) -> String {
    let owned: Vec<Vec<u8>> = parts.iter().map(|p| cbor::encode(&cbor::decode(p.as_bytes(), cbor::Profile::Rust3, RUST3_FRAME_MAX_DEPTH).unwrap())).collect();
    let reconstructed: Vec<ReceivedBytes<'_>> = owned.iter().map(|raw| ReceivedBytes(raw.as_slice())).collect();
    let parts = reconstructed.as_slice();""",test=P+'rust3_receive_commitments_use_only_retained_received_value_slices',witness='commitment input must belong to a retained received buffer'),
 dict(id='candidate-only-spool-precharge',path=AC,old='let size = entry_length(batch.analysis_ordinal, batch.stage_id, candidate)',new='let size = cbor::encoded_length(candidate)',test=P+'rust3_receive_full_published_response_boundaries_refuse_atomically_and_latch',witness='called `Result::unwrap_err()` on an `Ok` value'),
 dict(id='t020-current-stage-trigger-skipped',path=RC,old='text_of(f, "triggerStageId") != Some(binding.expected_stage_id.as_str())',new='false && (text_of(f, "triggerStageId") != Some(binding.expected_stage_id.as_str()))',test=P+'rust3_receive_budget_exhausted_matches_only_the_current_stage_and_exact_units',witness='T020 current-stage guard must refuse'),
 dict(id='cancelled-send-phase-skipped',path=RC,old='text_of(f, "observedPhase") != Some(phase.as_str())',new='false && (text_of(f, "observedPhase") != Some(phase.as_str()))',test=P+'rust3_receive_cancelled_echoes_exact_cancel_and_the_send_phase',witness='Err(Rust3Refusal::Admission(_))'),
 dict(id='universe-recursive-echo-skipped',path=RC,old='if field(open, name) != Some(value) {',new='if false && field(open, name) != Some(value) {',test=P+'rust3_receive_context_and_recursive_echo_never_substitute_a_different_identity',witness='recursive echo must compare the original resolved input value'),
]
for m in cases:assert baseline[m['path']].decode().count(m['old'])==1,m['id']
report=dict(standing='FULL RUST3 RECEIVER COMPILED RUNTIME MUTATIONS; NOT UNIT ACCEPTANCE/QUALIFICATION',baselineSourcePins=pins,owningReport=str(F/'repository-r2/report.json'),cargoTarget=str(F/'target'),cases=[],unitAccepted=False,productQualification=False)
def save():(B/'report.json').write_text(json.dumps(report,indent=2)+'\n')
def compile_binary(folder,require_fresh):
 folder.mkdir(parents=True,exist_ok=True);r=subprocess.run([R+'cargo','test','--locked','--offline','--no-run','--message-format=json','-p','opensip-components','--lib'],cwd=W,env=E,capture_output=True);(folder/'build.log').write_bytes(r.stderr);(folder/'artifacts.jsonl').write_bytes(r.stdout);assert r.returncode==0,'Compilation failure is never a runtime catch';rows=[j for l in r.stdout.splitlines()if l.startswith(b'{')and(j:=json.loads(l)).get('reason')=='compiler-artifact'and j.get('executable')and j['target']['name']=='opensip_components'];assert len(rows)==1;row=rows[0];assert row['target']['src_path']==str(W/'crates/components/src/lib.rs');assert not require_fresh or not row['fresh'];binary=Path(row['executable']);meta=dict(path=str(binary),bytes=binary.stat().st_size,sha256=hashlib.sha256(binary.read_bytes()).hexdigest(),freshCompilerArtifact=not row['fresh']);(folder/'binary.json').write_text(json.dumps(meta,indent=2)+'\n');return binary,meta
def execute(folder,binary,test,exact=True):
 r=subprocess.run([str(binary)]+(['--exact']if exact else[])+[test],cwd=W,env=E,capture_output=True);raw=r.stdout+r.stderr;(folder/'runtime.log').write_bytes(raw);return r.returncode,raw.decode(errors='replace')
binary,meta=compile_binary(B/'baseline',False);shutil.copyfile(binary,B/'positive-components');code,output=execute(B/'baseline',binary,'provider_protocol::rust3::',False);assert code==0 and '42 passed; 0 failed'in output;report['positiveBinary']=meta;report['baselineRust3Tests']=42;save()
for m in cases:
 restored();row=dict(m,caught=False,allSourcesRestored=False,restoredPositive=False);report['cases'].append(row);save();folder=B/m['id'];error=None
 try:
  (W/m['path']).write_text(baseline[m['path']].decode().replace(m['old'],m['new']));binary,meta=compile_binary(folder,True);code,output=execute(folder,binary,m['test']);row.update(binary=meta,runtimeExitCode=code,witnessObserved=m['witness']in output);assert code!=0 and '0 passed; 1 failed'in output and m['witness']in output,(m['id'],output[-3000:]);row['caught']=True
 except BaseException as ex:error=ex;row['error']=repr(ex)
 finally:
  for path,raw in baseline.items():
   if(W/path).read_bytes()!=raw:(W/path).write_bytes(raw)
  restored();row['allSourcesRestored']=True;save();binary,meta=compile_binary(folder/'restored-positive',True);code,output=execute(folder/'restored-positive',binary,m['test']);row.update(restoredPositive=code==0 and '1 passed; 0 failed'in output,restoredBinary=meta);save();assert row['restoredPositive'],m['id']
 if error:raise error
 print(m['id'],'compiled/runtime-caught/restored-positive',flush=True)
restored();report.update(allCaught=True,allRestored=True,compiledRuntimeMutants=len(cases));save();print('ALL10 RUST3 RECEIVER MUTANTS CAUGHT;20 SOURCE PINS RESTORED; UNIT REVIEW STILL REQUIRED',flush=True)
