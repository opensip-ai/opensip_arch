from pathlib import Path
import subprocess,os,json,tempfile,hashlib,re,difflib
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;W=Path('/Users/sb/code/opensip-ai/opensip-d3b2-takeover');O=F/'full-mutations-r2';O.mkdir();R='/opt/homebrew/Cellar/rust/1.95.0/bin/';T=Path(tempfile.mkdtemp(prefix='opensip-d3b2-full-mut-',dir=subprocess.check_output(['getconf','DARWIN_USER_TEMP_DIR'],text=True).strip()));T.chmod(0o700)
E=dict(os.environ,PATH='/opt/homebrew/bin:'+R+':/usr/bin:/bin',CARGO_HOME='/Users/sb/.cargo',CARGO_TARGET_DIR=str(F/'seam-r1/target'),CARGO=R+'cargo',RUSTC=R+'rustc',TMPDIR=str(T),CC='/usr/bin/cc',CXX='/usr/bin/c++',AR='/usr/bin/ar',SDKROOT=subprocess.check_output(['xcrun','--show-sdk-path'],text=True).strip());E.pop('RUST_TEST_THREADS',None)
base=json.loads((F/'complete-r3/report.json').read_text());assert all(x['exitCode']==0 for x in base['runs']);original={p:(W/p).read_bytes() for p in base['sourcePins']};assert all(hashlib.sha256(b).hexdigest()==base['sourcePins'][p] for p,b in original.items())
SUP='crates/components/src/supervisor.rs';TS='crates/components/src/provider_protocol/ts2/participant.rs';OP='crates/operability/src/kinds/registry.rs';source=original[SUP].decode()
inband='''inband: self
                    .stage1
                    .is_some_and(|s| s.evidence.inband == InbandCancel::Written),'''
grace='''        due.push((
            stage1.started + protocol.stage1_cancel_grace,
            BoundedWait::Stage1CancelGrace,
        ));'''
resolve=source[source.index('    fn resolve_revocation_mark('):source.index('    fn mark_completed(')]
arm_error=source[source.index('            Err(error) => {\n                tracking.evidence.arming_failure'):source.index('        let mut facts = Vec::new();\n        for mark in REVOCATION_MARKS',source.index('            Err(error) => {\n                tracking.evidence.arming_failure'))]
assert arm_error.endswith('        };\n')
new_arm='''            Err(_error) => {
                let observation = tracking.evidence.observation;
                let assumed = RevocationClockSample { after: observation.monotonic_before(), boot: observation.boot_id().to_owned() };
                return Self::arm(observation, tool, Ok(assumed), now, completed, impossible, prior);
            }
        };
'''
clean_block=source[source.index('        if self.clean_at.take().is_some()'):source.index('        if let Some(observed) = observed',source.index('        if self.clean_at.take().is_some()'))]
zero=original[TS].decode();zero=zero[zero.index('        if event == ProcessEvent::ZeroExit\n'):zero.index('        if !self.faulted() && self.receiver.process(event).is_err()',zero.index('        if event == ProcessEvent::ZeroExit\n'))]
# Each entry identifies the literal plan axis or a concrete review regression.
M=[]
def add(name,axis,path,pairs,control,package='opensip_components'):M.append(dict(name=name,axis=axis,path=path,pairs=pairs,control=control,package=package))
add('control-before-inband','1',SUP,[('self.inband_cancel(InbandCancel::Queued);','self.inband_cancel(InbandCancel::Queued); self.queue_control_cancel(CancelReason::User);')],'d3b2_root_cooperative_cancel')
add('non-user-inband','2',SUP,[('self.append(SupervisionEvent::Trigger(cause));\n        match self.first_cause','if cause != Cause::UserCancel { if let Some(p) = &mut self.participant { p.user_cancel(); } }\n        self.append(SupervisionEvent::Trigger(cause));\n        match self.first_cause')],'d3b2_marks_non_user_faults')
add('second-real-cancel','3',TS,[('&& !self.cancel_requested','&& true')],'d3b2_cancel_progress_follows_the_last_byte')
add('grace-at-write','4',SUP,[('self.inband_cancel(InbandCancel::Written);','self.inband_cancel(InbandCancel::Written); if let Some(s) = &mut self.stage1 { s.started = Instant::now(); }'),(grace,'if stage1.evidence.inband == InbandCancel::Written {\n'+grace+'\n}')],'d3b2_root_stalled_inband')
add('second-signal-refused','5',SUP,[('1 => self.second = Some(self.stamp()),','1 => return false,')],'d3b2_root_gate_keeps')
add('store-before-stamp','6',SUP,[('let stamp = self.minimum_stamp()?;','let stamp = self.queue.front().map(|entry| entry.stamp).or(self.first).or(self.second)?;')],'d3b2_root_named_interleavings')
add('interrupted-cleared','7',SUP,[('fn trigger_from(&mut self, cause: Cause, from_t2: bool) {','fn trigger_from(&mut self, cause: Cause, from_t2: bool) { if cause != Cause::UserCancel { self.user_interrupted = false; }')],'d3b2_root_named_interleavings')
add('ten-second-observer-ceiling','8',SUP,[('if self.observer_seen {\n            REAP_CEILING_REVOCATION','if self.observer_seen {\n            REAP_CEILING')],'d3b2_marks_unreaped_root')
add('miss-only-at-completion','9',SUP,[('        self.revocation_timers(now);','        // mutation: no independent mark timers')],'d3b2_marks_each_timer')
add('miss-twice','10',SUP,[(resolve,resolve.replace('self.fact(fact);','self.fact(fact); self.fact(fact);'))],'d3b2_marks_each_timer')
add('assumed-zero-failed-arm','11',SUP,[(arm_error,new_arm)],'d3b2_revocation_failed_arm_has_no_lag')
add('reset-reference-at-read','12',SUP,[('match read.and_then(|sample| self.validate(sample)) {','match read.and_then(|sample| self.validate(sample)).map(|_| Duration::ZERO) {')],'d3b2_revocation_later_failure')
add('lower-bound-as-measured','13',SUP,[('self.miss(mark, records::RevocationMeasurement::LowerBound(elapsed))','self.miss(mark, records::RevocationMeasurement::Measured(elapsed))')],'d3b2_revocation_repeated_failures_resolve')
add('elapsed-with-unavailable','14',OP,[('Self::Unavailable => (Code::from_enum(ElapsedStatus::Unavailable), None),','Self::Unavailable => (Code::from_enum(ElapsedStatus::Unavailable), Some(Elapsed::new(0))),')],'d3b2_revocation_measurement_shapes','opensip_operability')
add('cancel-fact-at-queue','15',SUP,[('self.control_cancel(ControlCancel::Queued);','self.control_cancel(ControlCancel::Queued); self.fact(records::RecordFact::CancelSent { inband: false, control_reason: opensip_operability::ControlCancelReason::User });')],'d3b2_root_control_write_failure')
add('inband-constant-false','16a',SUP,[(inband,'inband: false,')],'d3b2_root_cooperative_cancel')
add('inband-constant-true','16b',SUP,[(inband,'inband: true,')],'each_fact_carries_its_values')
add('normal-end-cancel-regression','ROOT-R1-RF1',SUP,[('if !normal_end_force {','if true {')],'d3b2_review_delayed_normal_shutdown')
add('late-grace-before-fault-regression','ROOT-R1-RF2',SUP,[('.min_by_key(|(at, wait)| (*at, usize::from(*wait == BoundedWait::Stage1CancelGrace)))','.max_by_key(|(at, wait)| (*at, usize::from(*wait == BoundedWait::Stage1CancelGrace)))')],'d3b2_review_older_')
add('clean-first-cause-regression','REV-R1-RF1',SUP,[('self.clean_at.get_or_insert_with(Instant::now);','self.first_cause = Some(Cause::Clean); self.clean_at.get_or_insert_with(Instant::now);'),(clean_block,'')],'d3b2_clean_reap_')
add('late-tool-clean-timer-regression','REV-R2-RF1',SUP,[('if self.clean_at.take().is_some() && self.ladder.is_none() && self.child.is_some() {','if cause != Cause::UserCancel && self.clean_at.take().is_some() && self.ladder.is_none() && self.child.is_some() {')],'d3b2_final_tool_signal_discards_late_clean')
add('ts2-cancelled-zero-exit-regression','REAL-TS2-ZEROEXIT',TS,[(zero,'')],'d3b2_real_ts2_root_phase_matrix')
pair='let read = self.revocation_clock();\n        let now = Instant::now();'
swap='let now = Instant::now();\n        let read = self.revocation_clock();'
arm_scope=source[source.index('    fn arm_revocation('):source.index('    fn resolve_revocation_mark(')]
assert arm_scope.count(pair)==1 and resolve.count(pair)==1
add('instant-before-arming-read','PLAN-R3-NBO1-ARM',SUP,[(arm_scope,arm_scope.replace(pair,swap))],'d3b2_final_delayed_clock_reads')
add('instant-before-failed-decision-read','PLAN-R3-NBO1-DECISION',SUP,[(resolve,resolve.replace(pair,swap))],'d3b2_final_delayed_clock_reads')
assert len(M)==24
for m in M:
 s=original[m['path']].decode()
 for before,after in m['pairs']:
  assert s.count(before)==1,(m['name'],'ambiguous edit',s.count(before),before[:70]);s=s.replace(before,after)
report={'standing':'FINAL ISOLATED CANDIDATE MUTATION PROOF; NO UNIT ACCEPTANCE OR QUALIFICATION','sourcePins':base['sourcePins'],'privateTMPDIR':str(T),'mutations':[],'restored':False,'plannedAxes':16,'plannedVariants':17,'reviewAndIntegrationRegressions':5,'clockPairOrderNegatives':2}
def save(): (O/'report.json').write_text(json.dumps(report,indent=2)+'\n')
def build(label,selected):
 r=subprocess.run([R+'cargo','test','--locked','--offline','--no-run','--message-format=json','-p','opensip-components','-p','opensip-operability'],cwd=W,env=E,capture_output=True);(O/(label+'-build.log')).write_bytes(r.stderr);(O/(label+'-artifacts.jsonl')).write_bytes(r.stdout)
 assert r.returncode==0,(label,'compile failures do not count',r.stderr[-3000:]);bins={};fresh={};fixture=None
 for line in r.stdout.splitlines():
  j=json.loads(line)
  if j.get('reason')!='compiler-artifact' or not j.get('executable'):continue
  name=j['target']['name']
  if name=='supervisor_fixture':fixture=Path(j['executable'])
  if name in ['opensip_components','opensip_operability'] and j['profile']['test']:
   crate='components' if name=='opensip_components' else 'operability';assert j['target']['src_path']==str(W/f'crates/{crate}/src/lib.rs');bins[name]=Path(j['executable']);fresh[name]=j['fresh']
 assert fixture and selected in bins and not fresh[selected]
 (bins['opensip_components'].parent/'supervisor_fixture.path').write_text(str(fixture)+'\n'+hashlib.sha256(fixture.read_bytes()).hexdigest()+'\n')
 return bins
try:
 for m in M:
  print(m['name'],flush=True);p=W/m['path'];s=original[m['path']].decode()
  for before,after in m['pairs']:s=s.replace(before,after)
  p.write_text(s);mutated=hashlib.sha256(p.read_bytes()).hexdigest();(O/(m['name']+'.diff')).write_text(''.join(difflib.unified_diff(original[m['path']].decode().splitlines(True),s.splitlines(True),fromfile=m['path'],tofile=m['path']+' (mutated)')))
  try:
   bins=build(m['name'],m['package']);binary=bins[m['package']]
   with (O/(m['name']+'.log')).open('wb') as log:r=subprocess.run([str(binary),m['control']],cwd=W,env=E,stdout=log,stderr=subprocess.STDOUT,timeout=90)
   out=(O/(m['name']+'.log')).read_text();assert r.returncode==101 and re.search(r'test result: FAILED\..* [1-9]\d* failed;',out),(m['name'],r.returncode,out[-3000:]);report['mutations'].append({'name':m['name'],'axis':m['axis'],'path':m['path'],'mutatedSha256':mutated,'binarySha256':hashlib.sha256(binary.read_bytes()).hexdigest(),'control':m['control'],'package':m['package'],'exitCode':r.returncode,'runtimeFailureObserved':True})
  finally:p.write_bytes(original[m['path']])
  save()
finally:
 for p,b in original.items():(W/p).write_bytes(b)
 assert all(hashlib.sha256((W/p).read_bytes()).hexdigest()==base['sourcePins'][p] for p in original);report['restored']=True;save()
bins=build('restored','opensip_components')
for package,control,expected in [('opensip_components','d3b2_',49),('opensip_operability','d3b2_',1)]:
 binary=bins[package]
 with (O/(package+'-restored.log')).open('wb') as log:r=subprocess.run([str(binary),control],cwd=W,env=E,stdout=log,stderr=subprocess.STDOUT,timeout=90)
 out=(O/(package+'-restored.log')).read_text();assert r.returncode==0 and f'{expected} passed; 0 failed' in out,(package,out[-3000:]);report[package+'RestoredPasses']=expected
report['all24Caught']=len(report['mutations'])==24;save();print('All24 runtime negatives caught; exact15-path restoration and50 targeted positives pass',flush=True)
