from pathlib import Path
import os,json,hashlib,subprocess,tempfile,re,time
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;B=F/'mutants-r1';B.mkdir(exist_ok=False)
W=Path('/Users/sb/code/opensip-ai/opensip-rust3-send-takeover');R='/opt/homebrew/Cellar/rust/1.95.0/bin/'
own=json.loads((F/'mutation-owning-r2/report.json').read_text());assert own['allPassed'] and own['clippyExitCode']==0
pins=own['sourcePins'];original={p['path']:(W/p['path']).read_bytes()for p in pins}
assert all(hashlib.sha256(original[p['path']]).hexdigest()==p['sha256']for p in pins)
S='crates/components/src/provider_protocol/rust3/send/'
def test(module,name):return 'provider_protocol::rust3::send::'+module+'::tests::'+name
sender=test('sender','sender_slot_payload_sequence_and_lawful_alternative_chunking_diverge_before_sent_state')
final=test('sender','sender_final_digest_seals_and_defensive_request_counters_are_checked')
complete=test('participant','participant_complete_moves_original_raw_candidates_only_after_zero_exit_and_eof')
cancel=test('participant','participant_cancel_finishes_partial_hello_then_one_exact_cancel_without_source_read')
prefix=test('participant','participant_prefix_frame_count_and_payload_limits_precede_payload_allocation')
lifecycle=test('participant','participant_early_eof_late_fault_discard_and_successor_gate_never_publish_candidates')
cases=[]
def case(name,path,before,after,witness):
 assert before!=after and original[path].decode().count(before)==1,(name,'anchor not unique')
 cases.append(dict(name=name,path=path,before=before,after=after,witness=witness))
case('01-hello-limit-changed',S+'policy.rs','(k.clone(), Value::Unsigned(*v))','(k.clone(), Value::Unsigned(*v + u64::from(k == "maxScratchBytes")))',test('policy','selected_32_member_policy_and_hello_are_exact_not_defaulted'))
case('02-cancel-reserve-not-charged',S+'schedule.rs','payload_bytes: cancel_reserve_bytes,','payload_bytes: 0,',test('schedule','request_totals_include_one_reserved_cancel_and_refuse_before_retaining_a_slot'))
case('03-chunk-key-byte-undercharge',S+'schedule.rs','.and_then(|n| n.checked_add(6))','.and_then(|n| n.checked_add(5))',test('schedule','chunk_measurement_matches_real_encoding_at_all_heads_without_a_dummy_buffer'))
case('04-fixed-payload-digest-unchecked',S+'sender.rs','if raw_sha256(&cbor::encode(&payload)) != slot.payload_sha256 {','if false && raw_sha256(&cbor::encode(&payload)) != slot.payload_sha256 {',sender)
case('05-chunk-header-digest-unchecked',S+'sender.rs','if raw_sha256(&cbor::encode(&header)) != slot.payload_sha256 {','if false && raw_sha256(&cbor::encode(&header)) != slot.payload_sha256 {',sender)
case('06-final-entry-marker-unchecked',S+'sender.rs','|| slot.entry_content_sha256 != realized.final_digest','|| (false && slot.entry_content_sha256 != realized.final_digest)',final)
case('07-source-content-digest-unchecked',S+'sender.rs','if digest_hex(&digest.finish()) != *want {','if false && digest_hex(&digest.finish()) != *want {',test('sender','sender_bad_source_counts_hashes_and_reads_latch_once_before_the_bad_frame'))
case('08-running-payload-total-unchecked',S+'sender.rs','|| add(total, reserve)?','|| 0_u64 * add(total, reserve)?',final)
case('09-final-planned-totals-unchecked',S+'sender.rs','if next_slot == self.request.schedule.slots.len()','if false && next_slot == self.request.schedule.slots.len()',final)
case('10-wrong-host-envelope-major',S+'schedule.rs','("protocolMajor".into(), Value::Unsigned(3)),','("protocolMajor".into(), Value::Unsigned(4)),',test('sender','sender_independently_realizes_complete_greedy_transcripts_and_source_hashes'))
case('11-source-ack-gate-bypassed',S+'participant.rs','Some(slot) if self.receiver.admits(&host_frame(slot.frame)) => {','Some(_slot) => {',complete)
case('12-pending-write-gate-bypassed',S+'participant.rs','|| self.at < self.pending.len()','|| false',cancel)
case('13-duplicate-cancel-request-allowed',S+'participant.rs','|| self.cancel_requested\n','|| false\n',cancel)
case('14-response-frame-count-not-charged',S+'participant.rs','self.remaining_frames.checked_sub(1)','self.remaining_frames.checked_sub(0)',prefix)
case('15-coalesced-frame-boundary-bypassed',S+'participant.rs','let n = self.accumulator.next_fragment_len().min(bytes.len() - at);','let n = bytes.len() - at;',prefix)
case('16-terminal-minted-before-done',S+'participant.rs','|| self.receiver.phase() != "DONE"','|| false',complete)
case('17-original-buffer-handoff-copies','crates/components/src/provider_protocol/rust3/receive.rs','.map(|frame| frame.payload),','.map(|frame| frame.payload.clone()),',complete)
case('18-candidate-handoff-not-once','crates/components/src/provider_protocol/rust3/receive.rs','|| self.candidate_spool_taken\n','|| false\n','provider_protocol::rust3::receive::tests::rust3_terminal_spool_keeps_exact_envelopes_in_order_and_moves_only_once')
case('19-fault-keeps-minted-output',S+'participant.rs','if self.faulted() || self.receiver.phase() == "FAULT" {\n            self.output = None;','if self.faulted() || self.receiver.phase() == "FAULT" {\n            let _ = &self.output;',lifecycle)
case('20-reference-host-count-changed',S+'domain.rs','("subjectCount", Value::Unsigned(count)),','("subjectCount", Value::Unsigned(count+1)),',test('domain','reference_scope_preserves_the_same_subject_and_domain_commitments_without_inline_cap'))
case('21-reference-host-emits-inline',S+'request.rs','                reference,\n                recorder.sequence()','                false,\n                recorder.sequence()',test('request','request_reference_variant_is_selected_for_every_count_and_inline_cap_stays_closed'))
(B/'cases.json').write_text(json.dumps(cases,indent=2)+'\n')
T=Path(tempfile.mkdtemp(prefix='n-',dir=subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR'],text=True).strip()));T.chmod(0o700);os.setpriority(os.PRIO_PROCESS,0,10)
E=dict(os.environ,CARGO_HOME='/Users/sb/.cargo',CARGO_TARGET_DIR=str(F/'target'),TMPDIR=str(T),CC='/usr/bin/cc',CXX='/usr/bin/c++',AR='/usr/bin/ar',CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--show-sdk-path'],text=True).strip())
report=dict(standing='Compiled runtime weakening controls, not unit acceptance/qualification',sourcePins=pins,cases=[],productQualification=False,unitAccepted=False)
def save(): (B/'report.json').write_text(json.dumps(report,indent=2)+'\n')
def verify():assert all((W/path).read_bytes()==data for path,data in original.items())
def build(directory):
 r=subprocess.run([R+'cargo','test','--locked','--offline','-p','opensip-components','--lib','--no-run','--message-format=json'],cwd=W,env=E,capture_output=True,timeout=180)
 (directory/'compile.log').write_bytes(r.stderr);(directory/'artifacts.jsonl').write_bytes(r.stdout)
 assert r.returncode==0,'compile failure is not a mutation kill'
 rows=[j for line in r.stdout.splitlines()if line.startswith(b'{')and(j:=json.loads(line)).get('reason')=='compiler-artifact'and j.get('target',{}).get('name')=='opensip_components'and j.get('executable')]
 assert len(rows)==1 and rows[0]['fresh'] is False,'require fresh compiled components test executable'
 return rows[0],Path(rows[0]['executable'])
save()
for c in cases:
 verify();directory=B/c['name'];directory.mkdir();mutated=original[c['path']].decode().replace(c['before'],c['after'],1).encode()
 item=dict(name=c['name'],source=c['path'],witness=c['witness'],originalSha256=hashlib.sha256(original[c['path']]).hexdigest(),mutantSha256=hashlib.sha256(mutated).hexdigest(),mutantBytes=len(mutated),restored=False)
 report['cases'].append(item);save()
 try:
  (directory/'mutant-source.rs').write_bytes(mutated);(W/c['path']).write_bytes(mutated)
  row,binary=build(directory);item.update(compiled=True,compilerArtifactCached=row['fresh'],binary=str(binary),binarySha256=hashlib.sha256(binary.read_bytes()).hexdigest());save()
  start=time.monotonic();run=subprocess.run([str(binary),'--exact',c['witness'],'--nocapture'],cwd=W,env=E,capture_output=True,timeout=60);log=run.stdout+run.stderr;(directory/'runtime.log').write_bytes(log)
  decoded=log.decode(errors='replace');failure=re.findall(r'^test (.+) \.\.\. FAILED$',decoded,re.M)
  item.update(runtimeExitCode=run.returncode,runtimeSeconds=time.monotonic()-start,failureSet=failure,summaries=re.findall(r'^test result:.*$',decoded,re.M),killed=run.returncode==101 and failure==[c['witness']] and '0 passed; 1 failed;'in decoded);save()
  assert item['killed'],'mutant survived or failed without its named runtime witness'
 finally:
  (W/c['path']).write_bytes(original[c['path']]);verify();item['restored']=True;save()
 print(c['name']+' COMPILED/RUNTIME-KILLED/RESTORED',flush=True)
# Compile the restored source afresh, then execute all focused owning controls.
directory=B/'restored-positive';directory.mkdir();row,binary=build(directory)
run=subprocess.run([str(binary),'provider_protocol::rust3'],cwd=W,env=E,capture_output=True,timeout=120);log=run.stdout+run.stderr;(directory/'runtime.log').write_bytes(log)
report['restoredPositive']=dict(exitCode=run.returncode,binary=str(binary),binarySha256=hashlib.sha256(binary.read_bytes()).hexdigest(),compilerArtifactCached=row['fresh'],summaries=re.findall(r'^test result:.*$',log.decode(errors='replace'),re.M));save();assert run.returncode==0 and b'87 passed; 0 failed'in log
verify();report.update(allPassed=True,compiledRuntimeKills=len(cases),all23SourcesRestored=True);save();print('21 FRESH-COMPILED RUNTIME MUTANTS KILLED; EXACT23PINS RESTORED; FRESH87OWNING PASS',flush=True)
