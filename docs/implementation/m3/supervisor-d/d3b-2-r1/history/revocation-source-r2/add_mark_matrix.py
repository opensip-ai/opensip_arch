from pathlib import Path
W=Path('/Users/sb/code/opensip-ai/opensip-d3b2-takeover');p=W/'crates/components/tests/supervisor_fixture.rs';s=p.read_text();a='''    if let Value::Map(pairs) = value {
        if let Some((_, v)) = pairs.iter().find(|(k, _)| k == key) {
            return v;
        }
    }''';assert s.count(a)==1;s=s.replace(a,'''    if let Value::Map(pairs) = value && let Some((_, v)) = pairs.iter().find(|(k, _)| k == key) { return v; }''');p.write_text(s)
p=W/'crates/components/src/supervisor_tests.rs';s=p.read_text();s+='''
#[test]
fn d3b2_marks_each_timer_misses_before_completion_and_late_completion_is_silent() {
    use opensip_operability::RevocationMark as M;
    for mark in [M::ProtocolCancel,M::Sigterm,M::KillAndReap,M::ScratchCleanup] {
        let dir=test_dir();let(mut supervision,_)=prepared("cancel-ignore",FixtureParticipant::new(ProtocolWaits::TS2),None);
        let mut root=root_in(&dir);supervision.start(&mut root).unwrap();
        supervision.observer_trigger(Cause::Revoked,opensip_platform::observe_clock().unwrap());
        assert!(supervision.revocation.as_ref().unwrap().pending(mark));
        let read=d3b2_sample(&supervision.revocation.as_ref().unwrap().evidence.observation,revocation_bound(mark)+Duration::from_nanos(1));
        supervision.seams.revocation_reads.push_back(Ok(read));
        supervision.revocation.as_mut().unwrap().deadlines[mark as usize]=Some(Instant::now()-Duration::from_millis(1));
        supervision.timers();
        assert_eq!(supervision.revocation.as_ref().unwrap().evidence.state(mark),RevocationMarkState::Missed);
        let count=||supervision.seams.facts.borrow().iter().filter(|f|matches!(f,records::RecordFact::RevocationMissed{mark:m,..} if *m==mark)).count();
        assert_eq!(count(),1);
        let reads=supervision.seams.revocation_clock_reads;
        supervision.mark_completed(mark);
        assert_eq!(supervision.seams.revocation_clock_reads,reads,"late completion must not reread or revise a terminal mark");
        assert_eq!(supervision.seams.facts.borrow().iter().filter(|f|matches!(f,records::RecordFact::RevocationMissed{mark:m,..} if *m==mark)).count(),1);
        let cap=Instant::now()+HANDSHAKE;
        while supervision.state!=State::Settled {assert!(Instant::now()<cap);supervision.turn();}
        let settlement=supervision.take_settlement().unwrap();
        assert_eq!(settlement.revocation_evidence().unwrap().state(mark),RevocationMarkState::Missed);
        assert_eq!(settlement.scratch(),ScratchFate::Removed);
    }
}
fn d3b2_observer_on_snapshot()->Hook {
    let mut sent=false;Box::new(move|event,handle|{
        if !sent&&*event==SupervisionEvent::Progress(Progress::SnapshotAcknowledged){sent=true;assert!(handle.revoked(opensip_platform::observe_clock().unwrap()));}
    })
}
fn d3b2_scratch_miss(reason:ScratchRetained) {
    let dir=test_dir();let(mut supervision,events)=prepared("scratch-files",FixtureParticipant::new(ProtocolWaits::TS2),Some(d3b2_observer_on_snapshot()));
    match reason {
        ScratchRetained::IoFailure(errno)=>supervision.seams.removal_errno=Some(errno),
        ScratchRetained::WorkExhausted=>supervision.seams.removal_limits=Some(WorkCost{objects:16,edges:64,bytes:4096}),
        ScratchRetained::RootUnreaped=>supervision.seams.reap_blocked=true,
    }
    let out=finish(supervision,events,&dir);
    assert_eq!(out.settlement.scratch(),ScratchFate::Retained(reason));
    assert_eq!(out.settlement.revocation_evidence().unwrap().state(opensip_operability::RevocationMark::ScratchCleanup),RevocationMarkState::Missed);
    assert_eq!(out.facts.iter().filter(|f|matches!(f,records::RecordFact::RevocationMissed{mark:opensip_operability::RevocationMark::ScratchCleanup,..})).count(),1);
    assert!(out.settlement.revocation_evidence().unwrap().states.iter().all(|s|*s!=RevocationMarkState::Pending));
    if reason==ScratchRetained::RootUnreaped {
        assert_eq!(out.settlement.exit(),ExitClass::Unreaped);
        assert!(out.saw(&SupervisionEvent::WaitExpired(BoundedWait::ReapCeiling)));
        assert!(out.facts.contains(&records::RecordFact::WaitExpired{wait:opensip_operability::BoundedWait::ReapCeiling,limit:REAP_CEILING_REVOCATION}));
        assert_eq!(out.settlement.revocation_evidence().unwrap().state(opensip_operability::RevocationMark::KillAndReap),RevocationMarkState::Missed);
    }
}
#[test]
fn d3b2_marks_scratch_io_retention_is_an_immediate_single_miss(){d3b2_scratch_miss(ScratchRetained::IoFailure(13));}
#[test]
fn d3b2_marks_scratch_work_retention_is_an_immediate_single_miss(){d3b2_scratch_miss(ScratchRetained::WorkExhausted);}
#[test]
fn d3b2_marks_unreaped_root_uses_five_second_ceiling_and_retained_scratch_misses(){d3b2_scratch_miss(ScratchRetained::RootUnreaped);}
#[test]
fn d3b2_marks_failed_determinations_through_settlement_are_once_and_lower_bound() {
    for recover in [false,true] {
        let dir=test_dir();let(mut supervision,_)=prepared("cancel-ignore",FixtureParticipant::new(ProtocolWaits::TS2),None);
        let observed=opensip_platform::observe_clock().unwrap();
        supervision.seams.revocation_reads.push_back(Ok(d3b2_sample(&observed,Duration::ZERO)));
        supervision.seams.revocation_reads.push_back(Err(d3b2_clock_failure()));
        if !recover {for _ in 0..6 {supervision.seams.revocation_reads.push_back(Err(d3b2_clock_failure()));}}
        assert!(supervision.handle().revoked(observed));
        let mut root=root_in(&dir);supervision.start(&mut root).unwrap();let cap=Instant::now()+HANDSHAKE;
        while supervision.state!=State::Settled {assert!(Instant::now()<cap);supervision.turn();}
        let settlement=supervision.take_settlement().unwrap();let evidence=settlement.revocation_evidence().unwrap();
        assert!(evidence.states.iter().all(|s|*s!=RevocationMarkState::Pending));
        let facts=supervision.seams.facts.borrow();
        let misses:Vec<_>=facts.iter().filter_map(|f|match f{records::RecordFact::RevocationMissed{mark,measurement,..}=>Some((*mark,*measurement)),_=>None}).collect();
        assert_eq!(misses.len(),if recover{1}else{4});
        assert_eq!(evidence.determination_failures().len(),misses.len());
        for (index,(mark,measurement)) in misses.iter().enumerate(){
            assert!(matches!(measurement,records::RevocationMeasurement::LowerBound(_)));
            assert!(!misses[..index].iter().any(|(earlier,_)|earlier==mark));
        }
        if recover {assert_eq!(evidence.state(opensip_operability::RevocationMark::ScratchCleanup),RevocationMarkState::Satisfied);}
        else {assert_eq!(supervision.seams.revocation_clock_reads,5);}
    }
}
#[test]
fn d3b2_marks_non_user_faults_never_attempt_the_inband_cancel() {
    for cause in [Cause::HostFault,Cause::Deadline,Cause::Revoked,Cause::ObserverFailStop] {
        let dir=test_dir();let(mut supervision,events)=prepared("cancel-ignore",FixtureParticipant::new(ProtocolWaits::TS2),None);
        let mut root=root_in(&dir);supervision.start(&mut root).unwrap();let cap=Instant::now()+HANDSHAKE;
        while !supervision.participant.as_ref().unwrap().analyzed {assert!(Instant::now()<cap);supervision.turn();}
        if matches!(cause,Cause::Revoked|Cause::ObserverFailStop) {supervision.observer_trigger(cause,opensip_platform::observe_clock().unwrap());}
        else {supervision.trigger(cause);}
        assert!(!supervision.participant.as_ref().unwrap().cancel_requested,"{cause:?} attempted a user-only inband Cancel");
        while supervision.state!=State::Settled {assert!(Instant::now()<cap);supervision.turn();}
        assert!(!events.borrow().iter().any(|(_,e)|matches!(e,SupervisionEvent::InbandCancel(_))));
        assert_eq!(supervision.take_settlement().unwrap().first_cause(),cause);
    }
}
#[test]
fn d3b2_marks_rust_grace_second_signal_forces_at_once() {
    let mut sent=false;let hook:Hook=Box::new(move|event,handle|{
        if !sent&&*event==SupervisionEvent::Progress(Progress::SnapshotAcknowledged){sent=true;assert!(handle.user_signal());assert!(handle.user_signal());}
    });
    let dir=test_dir();let(supervision,events)=prepared("cancel-ignore",FixtureParticipant::new(ProtocolWaits{stage1_cancel_grace:Duration::from_millis(5000),normal_exit_grace:Duration::from_secs(5)}),Some(hook));
    let out=finish(supervision,events,&dir);
    let forces:Vec<_>=out.facts.iter().filter_map(|f|match f{records::RecordFact::CancelForced{trigger,grace}=>Some((*trigger,*grace)),_=>None}).collect();
    assert_eq!(forces.len(),1);assert_eq!(forces[0].0,opensip_operability::ForceTrigger::SecondSignal);assert!(forces[0].1<Duration::from_secs(5));
    assert!(!out.saw(&SupervisionEvent::WaitExpired(BoundedWait::Stage1CancelGrace)));nothing_left(&out);
}
#[test]
fn d3b2_marks_signal_close_race_accounts_for_every_signal_once() {
    let dir=test_dir();let(supervision,events)=prepared("cancel-cooperative",FixtureParticipant::new(ProtocolWaits::TS2),None);
    let handle=supervision.handle();let sending=handle.clone();
    let sender=std::thread::spawn(move||{for _ in 0..1000 {sending.user_signal();}});
    let out=finish(supervision,events,&dir);sender.join().unwrap();
    let consumed=out.events.iter().filter(|(_,e)|*e==SupervisionEvent::Trigger(Cause::UserCancel)).count() as u64;
    assert_eq!(consumed+out.settlement.extra_user_signals()+handle.gate.late(),1000);
    assert_eq!(out.events.iter().filter(|(_,e)|matches!(e,SupervisionEvent::Settled(_))).count(),1);
    assert!(!handle.user_signal());assert_eq!(consumed+out.settlement.extra_user_signals()+handle.gate.late(),1001);
}
''';p.write_text(s)
F=Path(__file__).parent;s=(F/'matrix_lane_r2.py').read_text().replace("'matrix-r2'","'marks-r1'");s=s.replace("('real-ts2-root-matrix',[str(binary),'d3b2_real_ts2_root_phase_matrix']),", "('new-mark-controls',[str(binary),'d3b2_marks_']),");(F/'marks_lane_r1.py').write_text(s)
print('8 mark/settlement/signal controls added, with real5s revocation ceiling')
