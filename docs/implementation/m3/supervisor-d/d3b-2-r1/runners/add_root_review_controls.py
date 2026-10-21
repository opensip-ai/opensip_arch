from pathlib import Path
W=Path('/Users/sb/code/opensip-ai/opensip-d3b2-takeover');p=W/'crates/components/src/supervisor_tests.rs';s=p.read_text();s=s.replace('pub(crate) revocation_reads:', 'pub(super) revocation_reads:').replace('pub(crate) revocation_clock_reads:', 'pub(super) revocation_clock_reads:')
s+='''
#[test]
fn d3b2_review_delayed_normal_shutdown_survives_two_signals_without_cancel() {
    let dir=test_dir();let(mut supervision,events)=prepared("no-exit",FixtureParticipant::new(FIXTURE_WAITS),None);
    let mut root=root_in(&dir);supervision.start(&mut root).unwrap();let cap=Instant::now()+HANDSHAKE;
    while supervision.state!=State::Running {assert!(Instant::now()<cap);supervision.turn();}
    supervision.send_health(Instant::now());
    assert!(!supervision.control_out.bytes.is_empty());
    supervision.seams.stall_control_writes=true;
    // Data completes normally while the older health frame remains unwritten.
    while supervision.terminal.is_none() {assert!(Instant::now()<cap);supervision.turn();}
    assert_eq!(supervision.terminal,Some(TerminalKind::Complete));
    assert_eq!(supervision.deferred,Some(Deferred::Shutdown));
    assert!(supervision.handle().user_signal());assert!(supervision.handle().user_signal());
    assert!(matches!(supervision.gate.take(),Some(GateMessage::FirstSignal)));supervision.user_signal(false);
    assert!(matches!(supervision.gate.take(),Some(GateMessage::SecondSignal)));supervision.user_signal(true);
    assert_eq!(supervision.deferred,Some(Deferred::Shutdown),"older shutdown must not be overwritten by a post-terminal cancel");
    assert!(supervision.cancel_control.is_none());
    assert!(!events.borrow().iter().any(|(_,e)|matches!(e,SupervisionEvent::ControlCancel(_))));
    assert_eq!(supervision.seams.facts.borrow().iter().filter(|f|matches!(f,records::RecordFact::CancelForced{trigger:opensip_operability::ForceTrigger::SecondSignal,..})).count(),1);
    assert!(!supervision.seams.facts.borrow().iter().any(|f|matches!(f,records::RecordFact::CancelSent{..})));
    supervision.seams.stall_control_writes=false;
    while supervision.state!=State::Settled {assert!(Instant::now()<cap);supervision.turn();}
    assert!(supervision.take_settlement().unwrap().user_interrupted());
}
fn d3b2_late_timer_fault(which:usize) {
    let dir=test_dir();let(mut supervision,events)=prepared("cancel-ignore",FixtureParticipant::new(ProtocolWaits::TS2),None);
    let mut root=root_in(&dir);supervision.start(&mut root).unwrap();
    supervision.user_signal(false);assert!(supervision.stage1_active());
    let now=Instant::now();
    // Both deadlines passed before the next inspected turn. The fault
    // precedes the Stage1 grace by one full second, without shortening waits.
    supervision.stage1.as_mut().unwrap().started=now-ProtocolWaits::TS2.stage1_cancel_grace-Duration::from_secs(1);
    supervision.next_sample=None;
    let (wait,cause)=match which {
        0=>{supervision.handshake_done=false;supervision.spawned_at=Some(now-supervision.waits.handshake-Duration::from_secs(2));(BoundedWait::Handshake,Cause::HandshakeDeadline)},
        1=>{supervision.handshake_done=true;supervision.spawned_at=Some(now-supervision.waits.wall_clock-Duration::from_secs(2));(BoundedWait::WallClock,Cause::Deadline)},
        2=>{supervision.handshake_done=true;supervision.health_due=Some(now-Duration::from_secs(2));(BoundedWait::LivenessWindow,Cause::Liveness)},
        _=>unreachable!(),
    };
    supervision.timers();
    assert_eq!(supervision.first_cause,Some(Cause::UserCancel));assert!(supervision.user_interrupted);
    assert!(supervision.later_causes.contains(&cause),"older {wait:?} fault suppressed by later grace");
    assert!(events.borrow().iter().any(|(_,e)|*e==SupervisionEvent::WaitExpired(wait)));
    assert!(!supervision.seams.facts.borrow().iter().any(|f|matches!(f,records::RecordFact::CancelForced{..})),"fault forces T2 without cancel.forced");
    assert!(supervision.ladder.unwrap().term_at.is_some());
    let cap=Instant::now()+HANDSHAKE;
    while supervision.state!=State::Settled {assert!(Instant::now()<cap);supervision.turn();}
    assert_eq!(supervision.take_settlement().unwrap().first_cause(),Cause::UserCancel);
}
#[test]
fn d3b2_review_older_handshake_deadline_precedes_later_grace() {d3b2_late_timer_fault(0);}
#[test]
fn d3b2_review_older_wall_deadline_precedes_later_grace() {d3b2_late_timer_fault(1);}
#[test]
fn d3b2_review_older_liveness_deadline_precedes_later_grace() {d3b2_late_timer_fault(2);}
''';p.write_text(s)
# The owner test already produced both exact rendered references in its
# private TMPDIR. Copy under the lane; subsequent owning test revalidates.
F=Path(__file__).parent;lane=(F/'root_lane.py').read_text();prefix=lane[:lane.index("for name,args in")].replace("'root-r1'","'root-review-before-fix-r1'");prefix=prefix.replace("paths=subprocess.check_output",'''import shutil
prior=json.loads((F/'revocation-r1/report.json').read_text())
for name in ['registry-events.json','registry-events.md']:
 shutil.copyfile(Path(prior['privateTMPDIR'])/name,W/'crates/operability'/name)
paths=subprocess.check_output''');suffix='''
with (O/'expected-failures.log').open('wb') as log:r=subprocess.run([str(binary),'d3b2_review_'],cwd=W,env=E,stdout=log,stderr=subprocess.STDOUT,timeout=90)
output=(O/'expected-failures.log').read_text();assert r.returncode==101 and '0 passed; 4 failed' in output,output[-4000:]
report['expectedFailedControls']=4;report['exitCode']=r.returncode;report['negativeReproduction']=True;(O/'report.json').write_text(json.dumps(report,indent=2)+'\\n');print('Both RFs reproduced:4 runtime failures before correction',flush=True)
''';(F/'root_review_before_fix.py').write_text(prefix+suffix)
print('4 review reproductions added; expected failures before correction')
