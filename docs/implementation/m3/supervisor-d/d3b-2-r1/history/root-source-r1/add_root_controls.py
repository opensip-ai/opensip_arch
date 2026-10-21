from pathlib import Path
W=Path('/Users/sb/code/opensip-ai/opensip-d3b2-takeover');p=W/'crates/components/src/supervisor_tests.rs';s=p.read_text();a='''        user_interrupted: false,
        exit: ExitClass::Exited(0),''';assert s.count(a)==1;s=s.replace(a,'''        user_interrupted: false,
        extra_user_signals: 0,
        stage1: None,
        exit: ExitClass::Exited(0),''')
s+='''
// D3b-2 root controls use only the first-party type-level fixture.
#[test]
fn d3b2_root_gate_keeps_capacity_signals_order_and_exact_close_counts() {
    let gate = TriggerGate::new();
    for _ in 0..TRIGGER_CAPACITY { assert!(gate.admit(Trigger::HostFault)); }
    assert!(!gate.admit(Trigger::HostFault));
    assert!(gate.user_signal()); assert!(gate.user_signal());
    for _ in 0..100 { assert!(gate.user_signal()); }
    assert_eq!(gate.take_extra_signals(), 0);
    for _ in 0..TRIGGER_CAPACITY {
        assert_eq!(gate.take(), Some(GateMessage::Queued(Trigger::HostFault)));
    }
    assert_eq!(gate.take(), Some(GateMessage::FirstSignal));
    assert_eq!(gate.take_extra_signals(), 0);
    assert_eq!(gate.take(), Some(GateMessage::SecondSignal));
    assert_eq!(gate.take_extra_signals(), 100);
    assert_eq!(gate.close(), 0); assert_eq!(gate.late(), 0);
    assert!(!gate.user_signal()); assert_eq!(gate.late(), 1);
    let gate = TriggerGate::new();
    assert!(gate.user_signal()); assert!(gate.admit(Trigger::HostFault));
    assert!(gate.user_signal()); assert!(gate.user_signal());
    assert_eq!(gate.close(), 3); assert_eq!(gate.late(), 4);
    assert_eq!(gate.close(), 0); assert_eq!(gate.late(), 4);
}

fn d3b2_signal_on_snapshot() -> Hook {
    let mut sent = false;
    Box::new(move |event, handle| {
        if !sent && *event == SupervisionEvent::Progress(Progress::SnapshotAcknowledged) {
            sent = true; assert!(handle.user_signal());
        }
    })
}

#[test]
fn d3b2_root_named_interleavings_keep_first_cause_and_forced_fact() {
    use records::RecordFact;
    for order in ["sfs", "fss", "ssf"] {
        let mut sent = false;
        let hook: Hook = Box::new(move |event, handle| {
            if !sent && *event == SupervisionEvent::Progress(Progress::SnapshotAcknowledged) {
                sent = true;
                for action in order.chars() {
                    assert!(if action == 's' { handle.user_signal() } else { handle.host_fault() });
                }
            }
        });
        let dir = test_dir();
        let (supervision, events) = prepared("cancel-ignore", FixtureParticipant::new(ProtocolWaits::TS2), Some(hook));
        let out = finish(supervision, events, &dir);
        assert!(out.settlement.user_interrupted(), "{order}");
        let first = if order == "fss" { Cause::HostFault } else { Cause::UserCancel };
        assert_eq!(out.settlement.first_cause(), first, "{order}");
        let later = if order == "fss" { Cause::UserCancel } else { Cause::HostFault };
        assert!(out.settlement.later_causes().contains(&later), "{order}");
        let forces: Vec<_> = out.facts.iter().filter_map(|f| match f {
            RecordFact::CancelForced { trigger, grace } => Some((*trigger, *grace)), _ => None
        }).collect();
        assert_eq!(forces.len(), usize::from(order == "ssf"), "{order}: {:?}", out.events);
        if let Some((trigger, grace)) = forces.first() {
            assert_eq!(*trigger, opensip_operability::ForceTrigger::SecondSignal);
            assert!(*grace < ProtocolWaits::TS2.stage1_cancel_grace);
        }
        assert_eq!(out.count(&SupervisionEvent::Settled(first)), 1);
        assert!(!out.settlement.admissible());
        if order == "fss" { assert!(out.settlement.stage1_evidence().is_none()); }
        else { assert_eq!(out.settlement.stage1_evidence().unwrap().inband, InbandCancel::Abandoned); }
        nothing_left(&out);
    }
}

#[test]
fn d3b2_root_cooperative_cancel_keeps_leg_order_and_discards_candidates() {
    use records::RecordFact;
    let dir = test_dir();
    let (supervision, events) = prepared("cancel-cooperative", FixtureParticipant::new(ProtocolWaits::TS2), Some(d3b2_signal_on_snapshot()));
    let out = finish(supervision, events, &dir);
    assert_eq!(out.settlement.first_cause(), Cause::UserCancel);
    assert!(out.settlement.user_interrupted());
    assert_eq!(out.settlement.exit(), ExitClass::Exited(0));
    assert_eq!(out.settlement.terminal(), Some(TerminalKind::Cancelled));
    assert_eq!(out.settlement.stage1_evidence(), Some(Stage1Evidence { inband: InbandCancel::Written, control: Some(ControlCancel::Written) }));
    assert!(out.position(&SupervisionEvent::InbandCancel(InbandCancel::Written)) < out.position(&SupervisionEvent::ControlCancel(ControlCancel::Queued)));
    assert!(out.position(&SupervisionEvent::ControlCancel(ControlCancel::Queued)) < out.position(&SupervisionEvent::ControlCancel(ControlCancel::Written)));
    assert_eq!(out.facts.iter().filter(|f| matches!(f, RecordFact::CancelSent { .. })).count(), 1);
    assert!(out.facts.contains(&RecordFact::CancelSent { inband: true, control_reason: opensip_operability::ControlCancelReason::User }));
    assert!(!out.facts.iter().any(|f| matches!(f, RecordFact::CancelForced { .. })));
    assert!(!out.saw(&SupervisionEvent::Signalled { signal: SIGTERM }));
    assert!(!out.saw(&SupervisionEvent::Signalled { signal: SIGKILL }));
    assert!(!out.settlement.admissible()); assert!(out.discarded);
    nothing_left(&out);
}

#[test]
fn d3b2_root_grace_uses_each_participants_full_protocol_wait() {
    for grace in [ProtocolWaits::TS2.stage1_cancel_grace, Duration::from_millis(5_000)] {
        let dir = test_dir();
        let waits = ProtocolWaits { stage1_cancel_grace: grace, normal_exit_grace: Duration::from_secs(5) };
        let (supervision, events) = prepared("cancel-ignore", FixtureParticipant::new(waits), Some(d3b2_signal_on_snapshot()));
        let out = finish(supervision, events, &dir);
        assert_eq!(out.settlement.first_cause(), Cause::UserCancel);
        assert!(out.saw(&SupervisionEvent::WaitExpired(BoundedWait::Stage1CancelGrace)));
        let forces: Vec<_> = out.facts.iter().filter_map(|f| match f {
            records::RecordFact::CancelForced { trigger, grace } => Some((*trigger, *grace)), _ => None
        }).collect();
        assert_eq!(forces.len(), 1);
        assert_eq!(forces[0].0, opensip_operability::ForceTrigger::GraceExpired);
        assert!(forces[0].1 >= grace);
        assert!(out.facts.contains(&records::RecordFact::WaitExpired { wait: opensip_operability::BoundedWait::Stage1CancelGrace, limit: grace }));
        assert_eq!(out.settlement.stage1_evidence().unwrap().inband, InbandCancel::Written);
        nothing_left(&out);
    }
}

#[test]
fn d3b2_root_first_signal_during_normal_end_sends_nothing() {
    let hook: Hook = Box::new(|event, handle| {
        if *event == SupervisionEvent::Terminal(TerminalKind::Complete) { assert!(handle.user_signal()); }
    });
    let dir = test_dir();
    let (supervision, events) = prepared("normal-eof-first", FixtureParticipant::new(FIXTURE_WAITS), Some(hook));
    let out = finish(supervision, events, &dir);
    assert_eq!(out.settlement.first_cause(), Cause::Clean);
    assert!(out.settlement.user_interrupted());
    assert!(out.settlement.later_causes().contains(&Cause::UserCancel));
    assert!(out.settlement.stage1_evidence().is_none());
    assert!(!out.facts.iter().any(|f| matches!(f, records::RecordFact::CancelSent { .. } | records::RecordFact::CancelForced { .. })));
    nothing_left(&out);
}

#[test]
fn d3b2_root_tool_first_signal_has_no_stage1_or_forced_fact() {
    let out = tool_run("tool-hang", Box::new(|supervision| { assert!(supervision.handle().user_signal()); }));
    assert_eq!(out.settlement.first_cause(), Cause::UserCancel);
    assert!(out.settlement.user_interrupted());
    assert!(out.settlement.stage1_evidence().is_none());
    assert!(out.saw(&SupervisionEvent::Signalled { signal: SIGTERM }));
    assert!(!out.facts.iter().any(|f| matches!(f, records::RecordFact::CancelForced { .. } | records::RecordFact::CancelSent { .. })));
}
'''
p.write_text(s)
p=W/'crates/components/tests/supervisor_fixture.rs';s=p.read_text();a='''                "shutdown" if self.script != "no-ack" => {''';assert s.count(a)==1;s=s.replace(a,'''                "cancel" if self.script == "cancel-cooperative" => {
                    if self.acked.send(()).is_err() { return; }
                }
'''+a);a='''            (_, "Analyze") => {''';assert s.count(a)==1;s=s.replace(a,'''            ("cancel-cooperative" | "cancel-ignore", "Analyze") => {}
            ("cancel-cooperative", "Cancel") => data.send(&["Cancelled"]),
            ("cancel-ignore", "Cancel") => hang(),
'''+a);p.write_text(s)
F=Path(__file__).parent;s=(F/'root_lane.py').read_text().replace("'root-r1'","'root-r2'");(F/'root_lane_r2.py').write_text(s)
print('Six root controls added; cooperative fixture remains type-only')
