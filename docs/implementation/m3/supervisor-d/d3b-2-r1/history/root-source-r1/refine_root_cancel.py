from pathlib import Path
W=Path('/Users/sb/code/opensip-ai/opensip-d3b2-takeover');p=W/'crates/components/src/supervisor.rs';s=p.read_text()
def one(a,b):
 global s
 assert s.count(a)==1,(a[:80],s.count(a));s=s.replace(a,b)
one('''        if self.state == State::Handshaking && now >= spawned + self.waits.handshake {''','''        if !self.handshake_done && (self.state == State::Handshaking || self.stage1_active()) && now >= spawned + self.waits.handshake {''')
one('''        if self.first_cause.is_none()
            && self.terminal.is_none()
            && now >= spawned + self.waits.wall_clock''','''        if (self.first_cause.is_none() || self.stage1_active())
            && self.terminal.is_none()
            && now >= spawned + self.waits.wall_clock''')
one('''        if self.state == State::Running && self.first_cause.is_none() {
            if let Some(due) = self.health_due''','''        if self.stage1_active() && self.health_due.is_some_and(|due| now >= due) {
            self.health_due = None;
            self.append(SupervisionEvent::WaitExpired(BoundedWait::LivenessWindow));
            self.append(SupervisionEvent::LivenessMissed(LivenessMiss::WindowExpired));
            self.trigger(Cause::Liveness);
        }
        if self.state == State::Running && self.first_cause.is_none() {
            if let Some(due) = self.health_due''')
one('''            if self.state == State::Handshaking {
                all.push(spawned + self.waits.handshake);
            }
            if self.first_cause.is_none() && self.terminal.is_none() {''','''            if !self.handshake_done && (self.state == State::Handshaking || self.stage1_active()) {
                all.push(spawned + self.waits.handshake);
            }
            if (self.first_cause.is_none() || self.stage1_active()) && self.terminal.is_none() {''')
one('''        if let Some(stage1) = self.stage1.filter(|s| s.active)
            && let Some(protocol) = self.protocol
        {
            all.push(stage1.started + protocol.stage1_cancel_grace);
        }''','''        if let Some(stage1) = self.stage1.filter(|s| s.active)
            && let Some(protocol) = self.protocol
        {
            all.push(stage1.started + protocol.stage1_cancel_grace);
            all.extend(self.health_due);
        }''')
# Every settlement has terminal cancellation evidence, even on unwind or
# an independently exiting child that never read a queued announcement.
one('''        self.ends = HostEnds::default();
        let output = self''','''        if self.cancel_control == Some(ControlCancel::Queued) {
            self.control_cancel(ControlCancel::Abandoned);
        }
        if self.stage1.is_some_and(|s| s.evidence.inband == InbandCancel::Queued) {
            if let Some(participant) = &mut self.participant { participant.abandon_input(); }
            self.inband_cancel(InbandCancel::Abandoned);
        }
        if let Some(stage1) = &mut self.stage1 { stage1.active = false; }
        self.deferred = None;
        self.control_out = PendingWrite::default();
        self.ends = HostEnds::default();
        let output = self''')
p.write_text(s)
p=W/'crates/components/tests/supervisor_fixture.rs';s=p.read_text();a='''                "cancel" if self.script == "cancel-cooperative" => {
                    if self.acked.send(()).is_err() {
                        return;
                    }
                }''';assert s.count(a)==1;s=s.replace(a,'''                "cancel" if self.script == "cancel-cooperative" && self.acked.send(()).is_err() => { return; }''');p.write_text(s)
p=W/'crates/components/src/supervisor_tests.rs';s=p.read_text();s+='''
#[test]
fn d3b2_root_second_signal_during_normal_end_forces_once() {
    let hook: Hook = Box::new(|event, handle| {
        if *event == SupervisionEvent::Terminal(TerminalKind::Complete) {
            assert!(handle.user_signal()); assert!(handle.user_signal());
        }
    });
    let dir = test_dir();
    let (supervision, events) = prepared("no-exit", FixtureParticipant::new(FIXTURE_WAITS), Some(hook));
    let out = finish(supervision, events, &dir);
    assert!(out.settlement.user_interrupted());
    assert!(out.settlement.stage1_evidence().is_none());
    assert_eq!(out.facts.iter().filter(|f| matches!(f, records::RecordFact::CancelForced { trigger: opensip_operability::ForceTrigger::SecondSignal, .. })).count(), 1);
    assert!(!out.events.iter().any(|(_,e)| matches!(e, SupervisionEvent::InbandCancel(_))));
    assert!(out.saw(&SupervisionEvent::Signalled { signal: SIGTERM }));
    nothing_left(&out);
}

#[test]
fn d3b2_root_stalled_inband_does_not_extend_grace_or_complete_after_force() {
    let dir = test_dir();
    let (mut supervision, _) = prepared("cancel-ignore", FixtureParticipant::new(ProtocolWaits::TS2), None);
    let mut root = root_in(&dir);
    supervision.start(&mut root).unwrap();
    let cap = Instant::now() + HANDSHAKE;
    while supervision.participant.as_ref().unwrap().run.phase() != "ANALYZING" {
        assert!(Instant::now() < cap); supervision.turn();
        if supervision.participant.as_ref().unwrap().analyzed { break; }
    }
    assert!(supervision.handle().user_signal());
    // Consume exactly at the real turn's gate point; leave the fd0
    // deliberately unserviced until the protocol's own grace expires.
    assert_eq!(supervision.gate.take(), Some(GateMessage::FirstSignal));
    supervision.user_signal(false);
    assert!(supervision.stage1_active());
    assert_eq!(supervision.stage1.unwrap().evidence.inband, InbandCancel::Queued);
    let started = supervision.stage1.unwrap().started;
    while started.elapsed() < ProtocolWaits::TS2.stage1_cancel_grace { std::thread::yield_now(); }
    supervision.timers();
    assert!(!supervision.stage1_active());
    assert!(supervision.ends.fd0.is_none());
    assert!(!supervision.participant.as_ref().unwrap().wants_write());
    assert_eq!(supervision.stage1.unwrap().evidence.inband, InbandCancel::Abandoned);
    assert!(supervision.ladder.unwrap().term_at.is_some());
    assert!(supervision.seams.facts.borrow().iter().any(|f| matches!(f, records::RecordFact::CancelForced { trigger: opensip_operability::ForceTrigger::GraceExpired, grace } if *grace >= ProtocolWaits::TS2.stage1_cancel_grace)));
    // Continue the normal bounded loop to verify native cleanup, not Drop.
    while supervision.state != State::Settled { assert!(Instant::now() < cap); supervision.turn(); }
    let settlement = supervision.take_settlement().unwrap();
    assert_eq!(settlement.stage1_evidence().unwrap().inband, InbandCancel::Abandoned);
    assert!(settlement.user_interrupted());
}

#[test]
fn d3b2_root_control_write_failure_forces_fault_without_sent_or_forced_fact() {
    let dir = test_dir();
    let (mut supervision, _) = prepared("cancel-ignore", FixtureParticipant::new(ProtocolWaits::TS2), Some(d3b2_signal_on_snapshot()));
    let mut root = root_in(&dir); supervision.start(&mut root).unwrap();
    let cap = Instant::now() + HANDSHAKE;
    // Stop before servicing the cancellation's control bytes.
    loop {
        assert!(Instant::now() < cap);
        supervision.turn();
        if supervision.stage1.is_some_and(|s| s.evidence.inband == InbandCancel::Written) { break; }
    }
    assert_eq!(supervision.cancel_control, Some(ControlCancel::Queued));
    supervision.seams.control_write_fails = true;
    supervision.service_control_write();
    assert_eq!(supervision.cancel_control, Some(ControlCancel::Failed));
    assert!(!supervision.stage1_active());
    assert!(supervision.later_causes.contains(&Cause::HostFault));
    while supervision.state != State::Settled { assert!(Instant::now() < cap); supervision.turn(); }
    let settlement = supervision.take_settlement().unwrap();
    assert_eq!(settlement.first_cause(), Cause::UserCancel);
    assert_eq!(settlement.stage1_evidence().unwrap().control, Some(ControlCancel::Failed));
    assert!(!supervision.seams.facts.borrow().iter().any(|f| matches!(f, records::RecordFact::CancelSent { .. } | records::RecordFact::CancelForced { .. })));
}
''';p.write_text(s)
F=Path(__file__).parent;(F/'root_lane_r4.py').write_text((F/'root_lane.py').read_text().replace("'root-r1'","'root-r4'"))
print('Root timers and settlement evidence refined;3 edge controls added')
