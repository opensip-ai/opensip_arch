from pathlib import Path
W=Path('/Users/sb/code/opensip-ai/opensip-d3b2-takeover');p=W/'crates/components/src/supervisor_tests.rs';s=p.read_text();s+='''
fn d3b2_clock_failure() -> RevocationClockFailure {
    RevocationClockFailure::Native(opensip_platform::ClockError::InvalidObservation("first-party injected read failure"))
}
fn d3b2_sample(observed: &opensip_platform::ClockObservation, elapsed: Duration) -> RevocationClockSample {
    RevocationClockSample { after: observed.monotonic_before() + elapsed, boot: observed.boot_id().to_owned() }
}
fn d3b2_arm_tracking(tool: bool, lag: Duration) -> (RevocationTracking, Vec<records::RecordFact>) {
    let observed = opensip_platform::observe_clock().unwrap(); let read = d3b2_sample(&observed, lag);
    RevocationTracking::arm(observed, tool, Ok(read), Instant::now(), &[false;5], &[false;5], &std::array::from_fn(|_|None))
}
#[test]
fn d3b2_revocation_failed_arm_has_no_lag_timers_or_fabricated_elapsed() {
    for tool in [false,true] {
        let observed = opensip_platform::observe_clock().unwrap();
        let (tracking, facts) = RevocationTracking::arm(observed, tool, Err(d3b2_clock_failure()), Instant::now(),
            &[false;5], &[false;5], &std::array::from_fn(|_|None));
        assert_eq!(facts.len(), if tool {3} else {4});
        assert!(tracking.evidence.arming_lag.is_none()); assert!(tracking.evidence.armed_at.is_none());
        assert!(tracking.evidence.arming_failure().is_some());
        assert!(tracking.deadlines.iter().all(Option::is_none));
        assert!(tracking.evidence.states.iter().all(|s| *s != RevocationMarkState::Pending));
        for fact in facts { match fact {
            records::RecordFact::RevocationMissed { mark, measurement, bound } => {
                assert_ne!(mark, opensip_operability::RevocationMark::RequestsRefused);
                if tool { assert_ne!(mark, opensip_operability::RevocationMark::ProtocolCancel); }
                assert_eq!(measurement.status(), opensip_operability::ElapsedStatus::Unavailable);
                assert_eq!(measurement.elapsed(), None); assert_eq!(bound, revocation_bound(mark));
            }, _ => panic!("wrong fact")
        }}
    }
}
#[test]
fn d3b2_revocation_later_failure_is_lower_bound_and_recovery_never_resets_reference() {
    use opensip_operability::RevocationMark as M;
    let (mut tracking, facts) = d3b2_arm_tracking(false, Duration::from_millis(500)); assert!(facts.is_empty());
    let reference = tracking.evidence.observation.monotonic_before();
    let armed = tracking.evidence.armed_at.unwrap();
    let first_deadlines = tracking.deadlines;
    let fact = tracking.determine(M::ProtocolCancel, true, Err(d3b2_clock_failure()), armed + Duration::from_millis(250)).unwrap();
    assert!(matches!(fact, records::RecordFact::RevocationMissed { measurement: records::RevocationMeasurement::LowerBound(d), .. } if d == Duration::from_millis(750)));
    // A subsequent valid read is measured from the unchanged original
    // reference, not from arming or the failed determination.
    let read = d3b2_sample(&tracking.evidence.observation, Duration::from_secs(2));
    assert!(tracking.determine(M::Sigterm, true, Ok(read), armed + Duration::from_secs(1)).is_none());
    assert_eq!(tracking.evidence.state(M::Sigterm), RevocationMarkState::Satisfied);
    assert_eq!(tracking.evidence.state(M::ProtocolCancel), RevocationMarkState::Missed);
    assert_eq!(tracking.evidence.observation.monotonic_before(), reference);
    assert_eq!(tracking.deadlines[M::KillAndReap as usize], first_deadlines[M::KillAndReap as usize]);
    let read = d3b2_sample(&tracking.evidence.observation, Duration::from_secs(20));
    let fact = tracking.determine(M::ScratchCleanup, true, Ok(read), armed).unwrap();
    assert!(matches!(fact, records::RecordFact::RevocationMissed { measurement: records::RevocationMeasurement::Measured(d), .. } if d == Duration::from_secs(20)));
    let read = d3b2_sample(&tracking.evidence.observation, Duration::from_secs(21));
    assert!(tracking.determine(M::ProtocolCancel, true, Ok(read), armed).is_none());
}
#[test]
fn d3b2_revocation_invalid_reads_fail_closed_at_arm_and_determination() {
    use opensip_operability::RevocationMark as M;
    for invalid_boot in [false,true] {
        let observed = opensip_platform::observe_clock().unwrap();
        let mut read = d3b2_sample(&observed, Duration::ZERO);
        if invalid_boot { read.boot = "first-party different boot".to_owned(); }
        else { read.after = observed.monotonic_before() - Duration::from_nanos(1); }
        let (tracking, facts) = RevocationTracking::arm(observed, false, Ok(read), Instant::now(), &[false;5], &[false;5], &std::array::from_fn(|_|None));
        assert_eq!(facts.len(),4); assert!(tracking.evidence.arming_failure().is_some());
        assert!(tracking.deadlines.iter().all(Option::is_none));
        let (mut tracking, _) = d3b2_arm_tracking(false, Duration::from_millis(10));
        let mut read = d3b2_sample(&tracking.evidence.observation, Duration::ZERO);
        if invalid_boot { read.boot = "first-party different boot".to_owned(); }
        else { read.after = tracking.evidence.observation.monotonic_before() - Duration::from_nanos(1); }
        let at = tracking.evidence.armed_at.unwrap();
        assert!(matches!(tracking.determine(M::ProtocolCancel, true, Ok(read), at), Some(records::RecordFact::RevocationMissed { measurement: records::RevocationMeasurement::LowerBound(d), .. }) if d == Duration::from_millis(10)));
    }
}
#[test]
fn d3b2_revocation_repeated_failures_resolve_each_pending_mark_once() {
    let (mut tracking, _) = d3b2_arm_tracking(false, Duration::from_millis(1));
    let at = tracking.evidence.armed_at.unwrap(); let mut facts = Vec::new();
    for mark in REVOCATION_MARKS {
        if let Some(fact) = tracking.determine(mark, false, Err(d3b2_clock_failure()), at + Duration::from_millis(2)) { facts.push(fact); }
    }
    assert_eq!(facts.len(),4); assert_eq!(tracking.evidence.determination_failures.len(),4);
    for mark in REVOCATION_MARKS { assert!(tracking.determine(mark, true, Err(d3b2_clock_failure()), at).is_none()); }
    assert_eq!(tracking.evidence.determination_failures.len(),4);
    assert!(tracking.evidence.states.iter().all(|s| *s != RevocationMarkState::Pending));
    assert!(facts.iter().all(|f| matches!(f, records::RecordFact::RevocationMissed { measurement: records::RevocationMeasurement::LowerBound(d), .. } if *d == Duration::from_millis(3))));
}
#[test]
fn d3b2_revocation_lag_reduces_deadlines_and_prior_completion_needs_proof() {
    use opensip_operability::RevocationMark as M;
    let (tracking, facts) = d3b2_arm_tracking(false, Duration::from_secs(3));
    assert_eq!(facts.len(),2); //2s protocol and3s TERM already passed.
    let at = tracking.evidence.armed_at.unwrap();
    assert_eq!(tracking.deadlines[M::KillAndReap as usize], Some(at+Duration::from_secs(2)));
    assert_eq!(tracking.deadlines[M::ScratchCleanup as usize], Some(at+Duration::from_secs(7)));
    for valid_proof in [false,true] {
        let observed = opensip_platform::observe_clock().unwrap();
        let mut done = [false;5]; done[M::ProtocolCancel as usize] = true;
        let mut clocks = std::array::from_fn(|_|None);
        if valid_proof { clocks[M::ProtocolCancel as usize] = Some(d3b2_sample(&observed, Duration::from_secs(1))); }
        let read = d3b2_sample(&observed, Duration::from_secs(30));
        let (tracking, facts) = RevocationTracking::arm(observed,false,Ok(read),Instant::now(),&done,&[false;5],&clocks);
        assert_eq!(tracking.evidence.state(M::ProtocolCancel), if valid_proof {RevocationMarkState::Satisfied} else {RevocationMarkState::Missed});
        assert_eq!(facts.len(), if valid_proof {3} else {4});
    }
}
#[test]
fn d3b2_revocation_provider_triggers_have_distinct_routes_and_no_pending_marks() {
    for fail_stop in [false,true] {
        let mut sent = false;
        let hook: Hook = Box::new(move |event, handle| {
            if !sent && *event == SupervisionEvent::Progress(Progress::SnapshotAcknowledged) {
                sent=true; let observed=opensip_platform::observe_clock().unwrap();
                assert!(if fail_stop {handle.observer_fail_stop(observed)} else {handle.revoked(observed)});
            }
        });
        let dir=test_dir(); let (supervision, events)=prepared("cancel-ignore", FixtureParticipant::new(ProtocolWaits::TS2), Some(hook));
        let out=finish(supervision,events,&dir);
        assert_eq!(out.settlement.first_cause(),if fail_stop {Cause::ObserverFailStop} else {Cause::Revoked});
        assert_eq!(records::settlement_route(&out.settlement), if fail_stop {records::OwnerRoute::ObserverFailStop} else {records::OwnerRoute::Revoked});
        let evidence=out.settlement.revocation_evidence().unwrap();
        assert!(evidence.arming_failure().is_none());
        assert!(evidence.states.iter().all(|s| *s != RevocationMarkState::Pending));
        assert_eq!(evidence.state(opensip_operability::RevocationMark::RequestsRefused),RevocationMarkState::Satisfied);
        assert_eq!(evidence.state(opensip_operability::RevocationMark::ScratchCleanup),RevocationMarkState::Satisfied);
        assert!(!out.events.iter().any(|(_,e)| matches!(e,SupervisionEvent::InbandCancel(_))));
        nothing_left(&out);
    }
}
#[test]
fn d3b2_revocation_failed_arm_in_real_loop_performs_no_later_mark_reads() {
    let dir=test_dir(); let (mut supervision,events)=prepared("hang",FixtureParticipant::new(ProtocolWaits::TS2),None);
    supervision.seams.revocation_reads.push_back(Err(d3b2_clock_failure()));
    assert!(supervision.handle().revoked(opensip_platform::observe_clock().unwrap()));
    let mut root=root_in(&dir); supervision.start(&mut root).unwrap(); let cap=Instant::now()+HANDSHAKE;
    while supervision.state != State::Settled {assert!(Instant::now()<cap);supervision.turn();}
    assert_eq!(supervision.seams.revocation_clock_reads,1);
    assert_eq!(supervision.reap_ceiling(),REAP_CEILING_REVOCATION);
    let settlement=supervision.take_settlement().unwrap();
    assert_eq!(settlement.first_cause(),Cause::Revoked);
    assert!(settlement.revocation_evidence().unwrap().arming_failure().is_some());
    let facts=supervision.seams.facts.borrow();
    let misses:Vec<_>=facts.iter().filter_map(|f| match f {records::RecordFact::RevocationMissed {mark,measurement,..}=>Some((*mark,*measurement)),_=>None}).collect();
    assert_eq!(misses.len(),4);assert!(misses.iter().all(|(_,m)|*m==records::RevocationMeasurement::Unavailable));
    assert_eq!(events.borrow().iter().filter(|(_,e)| matches!(e,SupervisionEvent::Settled(_))).count(),1);
}
#[test]
fn d3b2_revocation_tool_protocol_mark_is_inapplicable_and_scope_is_project() {
    let out=tool_run_with("tool-hang",Box::new(|supervision| {
        supervision.seams.revocation_reads.push_back(Err(d3b2_clock_failure()));
        assert!(supervision.handle().observer_fail_stop(opensip_platform::observe_clock().unwrap()));
    }));
    assert_eq!(out.settlement.first_cause(),Cause::ObserverFailStop);
    let evidence=out.settlement.revocation_evidence().unwrap();
    assert_eq!(evidence.state(opensip_operability::RevocationMark::ProtocolCancel),RevocationMarkState::Inapplicable);
    let misses:Vec<_>=out.facts.iter().filter(|f|matches!(f,records::RecordFact::ToolRevocationMissed {..})).collect();
    assert_eq!(misses.len(),3);
    for fact in misses {assert_eq!(fact.requires(),records::Requires::Project);assert!(!fact.supplies().contains(&"role"));assert!(!fact.supplies().contains(&"universe"));}
    out.nothing_left();
}
#[test]
fn d3b2_revocation_during_stage1_preserves_interrupt_and_forces_without_forced_fact() {
    let mut sent=false;
    let hook:Hook=Box::new(move |event,handle| {
        if !sent && *event==SupervisionEvent::Progress(Progress::SnapshotAcknowledged) {
            sent=true;assert!(handle.user_signal());assert!(handle.revoked(opensip_platform::observe_clock().unwrap()));
        }
    });
    let dir=test_dir();let(supervision,events)=prepared("cancel-ignore",FixtureParticipant::new(ProtocolWaits::TS2),Some(hook));
    let out=finish(supervision,events,&dir);
    assert_eq!(out.settlement.first_cause(),Cause::UserCancel);assert!(out.settlement.user_interrupted());
    assert!(out.settlement.later_causes().contains(&Cause::Revoked));
    assert_eq!(records::settlement_route(&out.settlement),records::OwnerRoute::Interrupted);
    assert!(!out.facts.iter().any(|f|matches!(f,records::RecordFact::CancelForced{..})));
    assert_eq!(out.settlement.stage1_evidence().unwrap().inband,InbandCancel::Abandoned);
    assert!(out.settlement.revocation_evidence().unwrap().states.iter().all(|s|*s!=RevocationMarkState::Pending));
    nothing_left(&out);
}
''';p.write_text(s)
F=Path(__file__).parent;s=(F/'root_lane.py').read_text().replace("'root-r1'","'revocation-r1'").replace("'root-cancel-controls',[str(binary),'d3b2_root_']", "'revocation-controls',[str(binary),'d3b2_revocation_']");s=s.replace("('full-components',[str(binary)]),", "('full-components',[str(binary)]),('operability',[R+'cargo','test','--locked','--offline','-p','opensip-operability','--lib']),");s=s.replace("'-p','opensip-components','--all-targets'", "'-p','opensip-components','-p','opensip-operability','--all-targets'");(F/'revocation_lane_r1.py').write_text(s)
print('Nine revocation controls added; standalone/real-loop clock cases and route scopes')
