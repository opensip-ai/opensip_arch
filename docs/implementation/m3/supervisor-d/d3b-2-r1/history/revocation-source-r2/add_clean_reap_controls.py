from pathlib import Path
W=Path('/Users/sb/code/opensip-ai/opensip-d3b2-takeover');p=W/'crates/components/src/supervisor_tests.rs';s=p.read_text();s+='''
fn d3b2_clean_reap_observer<P:Participant>(mut supervision:Supervision<P>,fail_stop:bool) {
    let dir=test_dir();let events:Events=Rc::default();let sink=Rc::clone(&events);
    supervision.observer=Some(Box::new(move|event|sink.borrow_mut().push((Instant::now(),event.clone()))));
    let facts=Rc::clone(&supervision.seams.facts);let sink=Rc::clone(&facts);
    supervision.record_facts(Box::new(move|fact|sink.borrow_mut().push(fact)));
    supervision.seams.reap_blocked=true;
    let mut root=root_in(&dir);supervision.start(&mut root).unwrap();let cap=Instant::now()+HANDSHAKE;
    while !(supervision.state==State::Reaping && supervision.clean_at.is_some() && supervision.ladder.is_none()) {
        assert!(Instant::now()<cap,"clean Reaping never reached: {:?}",events.borrow());
        assert_ne!(supervision.state,State::Settled);supervision.turn();
    }
    let observed=opensip_platform::observe_clock().unwrap();
    assert!(if fail_stop{supervision.handle().observer_fail_stop(observed)}else{supervision.handle().revoked(observed)});
    supervision.turn();
    let cause=if fail_stop{Cause::ObserverFailStop}else{Cause::Revoked};
    let first=supervision.first_cause;
    let ladder=supervision.ladder;
    // If the regression assertion fails, Drop can still finish native
    // cleanup promptly; the seam never pins a negative control's root.
    supervision.seams.reap_blocked=false;
    assert_eq!(first,Some(cause),"observer was suppressed behind provisional Clean");
    assert!(ladder.is_some(),"observer in clean reap needs its fault ladder");
    assert!(ladder.unwrap().term_at.is_some(),"T2 attempted before reap");
    assert!(ladder.unwrap().kill_at.is_some(),"dead root's group/tree step before reap");
    while supervision.state!=State::Settled {assert!(Instant::now()<cap);supervision.turn();}
    let mut settlement=supervision.take_settlement().unwrap();
    assert_eq!(settlement.first_cause(),cause);
    assert!(!settlement.admissible());assert!(settlement.release().is_none());
    assert_eq!(settlement.exit(),ExitClass::Exited(0));
    let evidence=settlement.revocation_evidence().unwrap();
    assert!(evidence.states.iter().all(|s|*s!=RevocationMarkState::Pending));
    let is_tool=settlement.is_tool();
    assert_eq!(evidence.state(opensip_operability::RevocationMark::ProtocolCancel),if is_tool{RevocationMarkState::Inapplicable}else{RevocationMarkState::Missed});
    let list=facts.borrow();
    assert_eq!(list.iter().filter(|f|matches!(f,records::RecordFact::TreeSwept{..}|records::RecordFact::ToolTreeSwept{..})).count(),1);
    let mut marks=Vec::new();
    for fact in list.iter(){match fact{
        records::RecordFact::RevocationMissed{mark,..}|records::RecordFact::ToolRevocationMissed{mark,..}=>{assert!(!marks.contains(mark));marks.push(*mark);},_=>{}
    }}
    assert_eq!(events.borrow().iter().filter(|(_,e)|matches!(e,SupervisionEvent::Settled(_))).count(),1);
    assert_eq!(events.borrow().iter().filter(|(_,e)|*e==SupervisionEvent::CancelAttempted).count(),usize::from(!is_tool));
    assert_eq!(records::settlement_route(&settlement),if is_tool{records::OwnerRoute::Tool}else if fail_stop{records::OwnerRoute::ObserverFailStop}else{records::OwnerRoute::Revoked});
}
fn d3b2_clean_provider(fail_stop:bool){
    let(supervision,_)=prepared("normal",FixtureParticipant::new(FIXTURE_WAITS),None);d3b2_clean_reap_observer(supervision,fail_stop);
}
fn d3b2_clean_tool(fail_stop:bool){
    let supervision=Supervision::prepare_tool(tool_spec_for(&fixture(),"tool-ok")).unwrap();d3b2_clean_reap_observer(supervision,fail_stop);
}
#[test]
fn d3b2_clean_reap_provider_revoked_uses_observer_ladder(){d3b2_clean_provider(false);}
#[test]
fn d3b2_clean_reap_provider_fail_stop_uses_observer_ladder(){d3b2_clean_provider(true);}
#[test]
fn d3b2_clean_reap_tool_revoked_uses_observer_ladder(){d3b2_clean_tool(false);}
#[test]
fn d3b2_clean_reap_tool_fail_stop_uses_observer_ladder(){d3b2_clean_tool(true);}
''';p.write_text(s)
F=Path(__file__).parent;s=(F/'root_review_before_fix.py').read_text().replace("'root-review-before-fix-r1'","'clean-reap-before-fix-r1'");start=s.index('import shutil\nprior=');end=s.index('paths=subprocess.check_output',start);s=s[:start]+s[end:];s=s.replace("'d3b2_review_'", "'d3b2_clean_reap_'").replace('Both RFs reproduced:4 runtime failures before correction','Clean-reaping RF reproduced:4 runtime failures before correction');(F/'clean_reap_before_fix.py').write_text(s)
print('Held clean-reap observer controls added for both causes/classes')
