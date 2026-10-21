from pathlib import Path
W=Path('/Users/sb/code/opensip-ai/opensip-d3b2-takeover');p=W/'crates/components/src/supervisor.rs';s=p.read_text()
a='''    /// The caller may need user cancellation, revocation or observer
    /// fail-stop, whose ladders are D3b's (LD-D3A-6).
    LadderUnavailable,
''';assert s.count(a)==1;s=s.replace(a,'');s=s.replace('''    /// Whether the caller may need a D3b ladder.
    pub needs_d3b_ladders: bool,
''','');s=s.replace('''    needs_d3b_ladders: bool,
''','');s=s.replace('''    if needs_d3b_ladders {
        return Err(SupervisorError::LadderUnavailable);
    }
''','');s=s.replace('''            spec.needs_d3b_ladders,
''','');s=s.replace('''        if cause != Cause::UserCancel
            && self.clean_at.take().is_some()''','''        if self.clean_at.take().is_some()''')
s=s.replace('''//! **Not here.** The descendant step, user cancellation, revocation and
//! harness coexistence are D3b's; MC item 12's adapter, which builds the
''','''//! D3b adds the descendant step, user cancellation, observer revocation
//! and fail-stop, with their typed settlement evidence. Linux harness
//! coexistence/qualification remains separate. MC item 12's adapter, which builds the
''');s=s.replace('''/// The settlement's causes (item 12, :446). `user-cancel`, `revoked` and
/// `observer-fail-stop` are accepted in the table, but their ladders are
/// D3b's (LD-D3A-6). O7's `confinement-refused` is not at M3.''','''/// The settlement's causes (item 12, :446). D3b supplies user-cancel,
/// revocation and observer-fail-stop. O7's `confinement-refused` is not at M3.''');s=s.replace('''/// a caller that may need a D3b ladder, a memory budget below one ceiling
/// (zero fit: the ceiling is never lowered silently), and a launch whose''','''/// a memory budget below one ceiling (zero fit: the ceiling is never
/// lowered silently), and a launch whose''');p.write_text(s)
p=W/'crates/components/src/supervisor_records.rs';s=p.read_text().replace('''        SupervisorError::LadderUnavailable | SupervisorError::DescriptorsMismatch => {''','''        SupervisorError::DescriptorsMismatch => {''');p.write_text(s)
p=W/'crates/components/src/supervisor_tests.rs';s=p.read_text().replace('''        needs_d3b_ladders: false,
''','');a='''/// LD-D3A-6: a caller that may need a D3b ladder is refused before spawn.
#[test]
fn a_caller_needing_a_d3b_ladder_is_refused() {
    let mut spec = spec_for(Path::new("/nonexistent"), "normal");
    spec.needs_d3b_ladders = true;
    assert!(matches!(
        Supervision::prepare(spec, FixtureParticipant::new(FIXTURE_WAITS)),
        Err(SupervisorError::LadderUnavailable)
    ));
}''';assert s.count(a)==1;s=s.replace(a,'''/// D3b-2 removes the temporary refusal. Both classes can prepare their
/// full supervisor without a prospective-ladder capability flag.
#[test]
fn d3b2_final_both_classes_prepare_without_a_ladder_gate() {
    let provider=Supervision::prepare(spec_for(Path::new("/nonexistent"),"normal"),FixtureParticipant::new(FIXTURE_WAITS)).unwrap();
    assert_eq!(provider.state(),State::Prepared);
    let tool=Supervision::prepare_tool(tool_spec_for(Path::new("/nonexistent"),"tool-ok")).unwrap();
    assert_eq!(tool.state(),State::Prepared);
}''');s+='''
fn d3b2_queue_kind(handle:&SupervisionHandle,kind:u8)->bool {
    match kind {
        0=>handle.user_signal(),
        1=>handle.user_signal()&&handle.user_signal(),
        2=>handle.revoked(opensip_platform::observe_clock().unwrap()),
        3=>handle.observer_fail_stop(opensip_platform::observe_clock().unwrap()),
        _=>unreachable!(),
    }
}
fn d3b2_state_case<P:Participant>(mut supervision:Supervision<P>,phase:&str,kind:u8) {
    let dir=test_dir();let events:Events=Rc::default();let sink=Rc::clone(&events);let handle=supervision.handle();
    let at_spawn=phase=="spawning";let spawned_handle=handle.clone();
    supervision.observer=Some(Box::new(move|event|{
        sink.borrow_mut().push((Instant::now(),event.clone()));
        if at_spawn&&matches!(event,SupervisionEvent::Spawned{..}){assert!(d3b2_queue_kind(&spawned_handle,kind));}
    }));
    let facts=Rc::clone(&supervision.seams.facts);let sink=Rc::clone(&facts);supervision.record_facts(Box::new(move|fact|sink.borrow_mut().push(fact)));
    if phase=="prepared"{assert!(d3b2_queue_kind(&handle,kind));}
    if phase=="reaping"{supervision.seams.reap_blocked=true;}
    let is_tool=supervision.class==Class::Tool;let mut root=root_in(&dir);supervision.start(&mut root).unwrap();let cap=Instant::now()+HANDSHAKE;
    if !matches!(phase,"prepared"|"spawning"|"handshaking") {
        if matches!(phase,"reaping"|"settled") {
            while if phase=="settled"{supervision.state!=State::Settled}else{!(supervision.state==State::Reaping&&supervision.clean_at.is_some()&&supervision.ladder.is_none())} {
                assert!(Instant::now()<cap,"{phase}, kind{kind}: {:?}",events.borrow());supervision.turn();
            }
        }else{
            while supervision.state!=State::Running{assert!(Instant::now()<cap);supervision.turn();}
            if matches!(phase,"stopping"|"killing"){
                supervision.trigger(Cause::HostFault);
                if phase=="killing"{
                    // A delayed turn after TERM: actual native KILL, before
                    // the separate exit source has been serviced.
                    supervision.ladder_step();
                    supervision.ladder.as_mut().unwrap().term_at=Some(Instant::now()-TERM_TO_KILL);
                    supervision.ladder_step();assert_eq!(supervision.state,State::Killing);
                }
            }
        }
    }
    if !matches!(phase,"prepared"|"spawning"){
        let accepted=d3b2_queue_kind(&handle,kind);assert_eq!(accepted,phase!="settled");
    }
    if phase=="settled"{
        assert_eq!(supervision.late_events(),if kind==1{1}else{1}); // second call short-circuits on refusal
    }else{
        supervision.turn();supervision.seams.reap_blocked=false;
        while supervision.state!=State::Settled{assert!(Instant::now()<cap,"{phase}, kind{kind}: {:?}",events.borrow());supervision.turn();}
    }
    let settlement=supervision.take_settlement().unwrap();
    let expected=if phase=="settled"{Cause::Clean}else if matches!(phase,"stopping"|"killing"){Cause::HostFault}
        else if phase=="reaping"&&!is_tool&&kind==0{Cause::Clean}else{match kind{0|1=>Cause::UserCancel,2=>Cause::Revoked,3=>Cause::ObserverFailStop,_=>unreachable!()}};
    assert_eq!(settlement.first_cause(),expected,"{phase}, kind{kind}: {:?}",events.borrow());
    assert_eq!(settlement.user_interrupted(),kind<2&&phase!="settled");
    if kind>=2&&phase!="settled"{
        let evidence=settlement.revocation_evidence().unwrap();assert!(evidence.states.iter().all(|s|*s!=RevocationMarkState::Pending));
        if is_tool{assert_eq!(evidence.state(opensip_operability::RevocationMark::ProtocolCancel),RevocationMarkState::Inapplicable);}
        assert!(!settlement.admissible());
    }
    assert_eq!(events.borrow().iter().filter(|(_,e)|matches!(e,SupervisionEvent::Settled(_))).count(),1);
    if is_tool||matches!(phase,"stopping"|"killing"|"settled"){
        assert!(!facts.borrow().iter().any(|f|matches!(f,records::RecordFact::CancelForced{..})));assert!(settlement.stage1_evidence().is_none());
    }
}
#[test]
fn d3b2_final_provider_trigger_state_matrix(){
    for phase in ["prepared","spawning","handshaking","running","stopping","killing","reaping","settled"]{
        for kind in 0..4{
            let script=if matches!(phase,"reaping"|"settled"){"normal"}else{"cancel-cooperative"};
            let(supervision,_)=prepared(script,FixtureParticipant::new(ProtocolWaits::TS2),None);d3b2_state_case(supervision,phase,kind);
        }
    }
}
#[test]
fn d3b2_final_tool_trigger_state_matrix(){
    for phase in ["prepared","spawning","running","stopping","killing","reaping","settled"]{
        for kind in 0..4{
            let script=if matches!(phase,"reaping"|"settled"){"tool-ok"}else{"tool-hang"};
            let supervision=Supervision::prepare_tool(tool_spec_for(&fixture(),script)).unwrap();d3b2_state_case(supervision,phase,kind);
        }
    }
}
#[test]
fn d3b2_final_cooperative_reap_observers_keep_user_cause_and_one_cancel(){
    for fail_stop in [false,true]{
        let dir=test_dir();let(mut supervision,events)=prepared("cancel-cooperative",FixtureParticipant::new(ProtocolWaits::TS2),Some(d3b2_signal_on_snapshot()));
        supervision.seams.reap_blocked=true;let mut root=root_in(&dir);supervision.start(&mut root).unwrap();let cap=Instant::now()+HANDSHAKE;
        while !(supervision.first_cause==Some(Cause::UserCancel)&&supervision.clean_at.is_some()&&supervision.state==State::Reaping){assert!(Instant::now()<cap);supervision.turn();}
        let observed=opensip_platform::observe_clock().unwrap();assert!(if fail_stop{supervision.handle().observer_fail_stop(observed)}else{supervision.handle().revoked(observed)});
        supervision.turn();assert!(supervision.ladder.is_some());assert!(supervision.clean_at.is_none());supervision.seams.reap_blocked=false;
        while supervision.state!=State::Settled{assert!(Instant::now()<cap);supervision.turn();}
        let settlement=supervision.take_settlement().unwrap();assert_eq!(settlement.first_cause(),Cause::UserCancel);assert!(settlement.user_interrupted());
        assert!(settlement.later_causes().contains(&if fail_stop{Cause::ObserverFailStop}else{Cause::Revoked}));
        assert!(!settlement.admissible());assert_eq!(records::settlement_route(&settlement),records::OwnerRoute::Interrupted);
        assert_eq!(supervision.seams.facts.borrow().iter().filter(|f|matches!(f,records::RecordFact::CancelSent{..})).count(),1);
        assert!(!supervision.seams.facts.borrow().iter().any(|f|matches!(f,records::RecordFact::CancelForced{..})));
        assert!(settlement.revocation_evidence().unwrap().states.iter().all(|s|*s!=RevocationMarkState::Pending));
        assert_eq!(events.borrow().iter().filter(|(_,e)|matches!(e,SupervisionEvent::Settled(_))).count(),1);
    }
}
#[test]
fn d3b2_final_session_refusal_misses_protocol_once_without_writing(){
    let(mut supervision,_)=prepared("normal",FixtureParticipant::new(ProtocolWaits::TS2),None);
    // The real session is still NEW and cannot admit Cancel before Hello.
    // A private sink witnesses no serialized frame, not a fake send result.
    supervision.ends.fd3=Some(std::fs::OpenOptions::new().write(true).open("/dev/null").unwrap());
    supervision.observer_trigger(Cause::Revoked,opensip_platform::observe_clock().unwrap());
    supervision.queue_control_cancel(CancelReason::SupervisorFault);
    assert_eq!(supervision.cancel_control,Some(ControlCancel::Refused));assert!(supervision.control_out.bytes.is_empty());
    let reads=supervision.seams.revocation_clock_reads;supervision.mark_impossible(opensip_operability::RevocationMark::ProtocolCancel);assert_eq!(supervision.seams.revocation_clock_reads,reads);
    assert_eq!(supervision.seams.facts.borrow().iter().filter(|f|matches!(f,records::RecordFact::RevocationMissed{mark:opensip_operability::RevocationMark::ProtocolCancel,..})).count(),1);
    assert!(!supervision.seams.facts.borrow().iter().any(|f|matches!(f,records::RecordFact::CancelSent{..})));
}
fn d3b2_control_failure_after_arm(reader_closes:bool){
    let dir=test_dir();let(mut supervision,_)=prepared("hang",FixtureParticipant::new(ProtocolWaits::TS2),None);
    let mut root=root_in(&dir);supervision.start(&mut root).unwrap();let cap=Instant::now()+HANDSHAKE;
    while supervision.state!=State::Running||!supervision.control_out.bytes.is_empty(){assert!(Instant::now()<cap);supervision.turn();}
    supervision.observer_trigger(Cause::Revoked,opensip_platform::observe_clock().unwrap());supervision.queue_control_cancel(CancelReason::SupervisorFault);
    assert_eq!(supervision.cancel_control,Some(ControlCancel::Queued));
    if reader_closes{
        let(writer,reader)=std::os::unix::net::UnixStream::pair().unwrap();let owned:OwnedFd=writer.into();supervision.ends.fd3=Some(File::from(owned));drop(reader);
    }else{supervision.seams.control_write_fails=true;}
    supervision.service_control_write();assert_eq!(supervision.cancel_control,Some(ControlCancel::Failed));
    assert_eq!(supervision.revocation.as_ref().unwrap().evidence.state(opensip_operability::RevocationMark::ProtocolCancel),RevocationMarkState::Missed);
    while supervision.state!=State::Settled{assert!(Instant::now()<cap);supervision.turn();}
    let settlement=supervision.take_settlement().unwrap();assert_eq!(settlement.first_cause(),Cause::Revoked);
    assert_eq!(supervision.seams.facts.borrow().iter().filter(|f|matches!(f,records::RecordFact::RevocationMissed{mark:opensip_operability::RevocationMark::ProtocolCancel,..})).count(),1);
    assert!(!supervision.seams.facts.borrow().iter().any(|f|matches!(f,records::RecordFact::CancelSent{..})));
}
#[test]
fn d3b2_final_control_reader_close_misses_protocol_immediately(){d3b2_control_failure_after_arm(true);}
#[test]
fn d3b2_final_control_write_failure_misses_protocol_immediately(){d3b2_control_failure_after_arm(false);}
''';p.write_text(s)
F=Path(__file__).parent;s=(F/'marks_lane_r2.py').read_text().replace("'marks-r2'","'complete-r1'");s=s.replace("('clean-reap-review-controls',[str(binary),'d3b2_clean_reap_']),", "('final-state-controls',[str(binary),'d3b2_final_']),");(F/'complete_lane_r1.py').write_text(s)
print('Final isolated candidate gate removed and full state/control failure matrix added; main untouched')
