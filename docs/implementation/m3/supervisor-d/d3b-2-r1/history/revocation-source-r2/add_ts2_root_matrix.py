from pathlib import Path
W=Path('/Users/sb/code/opensip-ai/opensip-d3b2-takeover');p=W/'crates/components/src/provider_protocol/ts2_send_tests.rs';s=p.read_text();s+='''
/// Real codec + native root loop, with only first-party generated wire data.
#[test]
fn d3b2_real_ts2_root_phase_matrix() {
    let table = Table::load(Protocol::Ts2).unwrap();
    for phase in ["handshake", "startup", "snapshot", "analysis", "terminal"] {
        let p = plan(); let r = build(&p); let c = context_of(&p, &r);
        let part = Ts2Participant::new(&table, c.clone(), r, Box::new(Memory::of(&p))).unwrap();
        let responses = m(&[
            ("mode", t(phase)),
            ("HelloAck", hello_ack(&c)),
            ("UniverseAccepted", universe_accepted(&c)),
            ("SnapshotAccepted", snapshot_accepted(&c)),
            ("NativeContextVerified", native_context_verified(&c)),
            ("analysis", Value::Array(vec![
                m(&[("kind", t("Coverage")), ("payload", coverage(&c,0))]),
                m(&[("kind", t("Coverage")), ("payload", coverage(&c,1))]),
                m(&[("kind", t("Complete")), ("payload", complete(&c,&[Vec::new(),Vec::new()],&[0,0]))]),
            ])),
        ]);
        crate::supervisor::tests::ts2_root_phase_control(part,responses,phase);
    }
}
''';p.write_text(s)
p=W/'crates/components/src/supervisor_tests.rs';s=p.read_text();s+='''
/// Bridge owned by the root tests: phase checks use the real participant's
/// public phase, without exposing production loop or descriptor internals.
pub(crate) fn ts2_root_phase_control(participant: crate::provider_protocol::ts2::Ts2Participant<'_>, bundle: Value, phase: &str) {
    let dir=test_dir();let bundle_path=dir.0.join("ts2-first-party-responses.cbor");
    std::fs::write(&bundle_path,write_frame(&bundle).unwrap()).unwrap();
    let script=format!("ts2-root:{}",bundle_path.display());
    let mut spec=spec_for(&fixture(),&script);
    spec.selection.tuple.role_subprotocol="typescript-semantic".to_owned();
    spec.selection.tuple.subprotocol_version=2;
    let mut supervision=Supervision::prepare(spec,participant).unwrap();
    let facts=Rc::new(RefCell::new(Vec::new()));let sink=Rc::clone(&facts);
    supervision.record_facts(Box::new(move |fact|sink.borrow_mut().push(fact)));
    let events:Events=Rc::default();let sink=Rc::clone(&events);
    supervision.observer=Some(Box::new(move|event|sink.borrow_mut().push((Instant::now(),event.clone()))));
    let mut root=root_in(&dir);supervision.start(&mut root).unwrap();let cap=Instant::now()+HANDSHAKE;
    loop {
        let at=match phase {
            "handshake"=>supervision.state==State::Handshaking,
            "startup"=>supervision.state==State::Running,
            "snapshot"=>supervision.participant.as_ref().unwrap().phase().contains("SNAPSHOT"),
            "analysis"=>supervision.participant.as_ref().unwrap().phase()=="ANALYZING",
            "terminal"=>supervision.terminal==Some(TerminalKind::Complete),
            _=>unreachable!(),
        };
        if at {break;}
        assert!(Instant::now()<cap,"phase {phase} never reached; actual {:?}, {:?}",supervision.state,supervision.participant.as_ref().unwrap().phase());
        assert_ne!(supervision.state,State::Settled,"premature settlement reaching {phase}: {:?}",events.borrow());
        supervision.turn();
    }
    assert!(supervision.handle().user_signal());
    while supervision.state!=State::Settled {assert!(Instant::now()<cap,"{phase} did not settle: {:?}",events.borrow());supervision.turn();}
    let mut settlement=supervision.take_settlement().unwrap();
    assert!(settlement.user_interrupted(),"{phase}");
    assert_eq!(settlement.exit(),ExitClass::Exited(0),"{phase}: {:?}",events.borrow());
    assert!(!settlement.later_causes().contains(&Cause::ProviderProtocol),"{phase}: {:?}",events.borrow());
    assert_eq!(records::settlement_route(&settlement),records::OwnerRoute::Interrupted);
    if phase=="terminal" {
        assert_eq!(settlement.first_cause(),Cause::Clean);
        assert!(settlement.stage1_evidence().is_none());
        assert!(!facts.borrow().iter().any(|f|matches!(f,records::RecordFact::CancelSent{..})));
    } else {
        assert_eq!(settlement.first_cause(),Cause::UserCancel,"{phase}: {:?}",events.borrow());
        assert_eq!(settlement.terminal(),Some(TerminalKind::Cancelled));
        assert_eq!(settlement.stage1_evidence(),Some(Stage1Evidence{inband:InbandCancel::Written,control:Some(ControlCancel::Written)}));
        assert!(!settlement.admissible());assert!(settlement.release().is_none());
        assert_eq!(facts.borrow().iter().filter(|f|matches!(f,records::RecordFact::CancelSent{inband:true,control_reason:opensip_operability::ControlCancelReason::User})).count(),1);
        assert!(!facts.borrow().iter().any(|f|matches!(f,records::RecordFact::CancelForced{..})));
    }
    assert_eq!(events.borrow().iter().filter(|(_,e)|matches!(e,SupervisionEvent::Settled(_))).count(),1);
    assert_eq!(settlement.scratch(),ScratchFate::Removed);
}
''';p.write_text(s)
p=W/'crates/components/tests/supervisor_fixture.rs';s=p.read_text();a='''"cancel" if self.script == "cancel-cooperative" && self.acked.send(()).is_err()''';assert s.count(a)==1;s=s.replace(a,'''"cancel" if (self.script == "cancel-cooperative" || self.script.starts_with("ts2-root:")) && self.acked.send(()).is_err()''')
a='''    std::thread::spawn(move || control.run(control_in));''';assert s.count(a)==1;s=s.replace(a,a+'''
    if let Some(bundle) = script.strip_prefix("ts2-root:") {
        ts2_root_data(&mut input, &mut data, &ack, bundle);
        return;
    }
''')
s+='''
fn cbor_member<'a>(value:&'a Value,key:&str)->&'a Value {
    if let Value::Map(pairs)=value {if let Some((_,v))=pairs.iter().find(|(k,_)|k==key){return v;}}
    panic!("first-party fixture value lacks {key}");
}
fn cbor_text(value:&Value)->&str {if let Value::Text(s)=value{s}else{panic!("first-party text")}}
fn ts2_reply(data:&mut Data,sequence:&mut u64,kind:&str,payload:Value) {
    let envelope=Value::Map(vec![("protocolMajor".to_owned(),Value::Unsigned(2)),("frameType".to_owned(),Value::Text(kind.to_owned())),
        ("sequence".to_owned(),Value::Unsigned(*sequence)),("payload".to_owned(),payload)]);
    *sequence+=1;
    data.out.as_mut().unwrap().write_all(&write_frame(&envelope).unwrap()).unwrap();
}
/// Responses are schema-valid payloads generated by the real codec's
/// first-party tests. Sequence and Cancel echo follow actual received bytes.
fn ts2_root_data(input:&mut File,data:&mut Data,ack:&mpsc::Receiver<()>,bundle_path:&str) {
    let bytes=std::fs::read(bundle_path).unwrap();
    let bundle=read_frame(&mut bytes.as_slice(),Profile::Rust3,16,None).unwrap().unwrap();
    let bundle=bundle.value();let mode=cbor_text(cbor_member(bundle,"mode"));
    let mut sequence=0;let mut observed="handshake";
    while let Some(frame)=read_frame(input,Profile::Ts2,opensip_components::provider_protocol::ts2::TS2_FRAME_MAX_DEPTH,None).unwrap() {
        let kind=cbor_text(cbor_member(frame.value(),"frameType"));
        match kind {
            "Hello" if !matches!(mode,"handshake"|"startup")=>ts2_reply(data,&mut sequence,"HelloAck",cbor_member(bundle,"HelloAck").clone()),
            "OpenUniverse"=>{observed="universe";ts2_reply(data,&mut sequence,"UniverseAccepted",cbor_member(bundle,"UniverseAccepted").clone());}
            "SnapshotManifest"=>observed="snapshot",
            "SnapshotSeal" if mode!="snapshot"=>{
                ts2_reply(data,&mut sequence,"SnapshotAccepted",cbor_member(bundle,"SnapshotAccepted").clone());
                ts2_reply(data,&mut sequence,"NativeContextVerified",cbor_member(bundle,"NativeContextVerified").clone());
            }
            "Analyze"=>{
                observed="analysis";
                if mode=="terminal" {
                    let Value::Array(replies)=cbor_member(bundle,"analysis") else {panic!("first-party replies")};
                    for reply in replies {ts2_reply(data,&mut sequence,cbor_text(cbor_member(reply,"kind")),cbor_member(reply,"payload").clone());}
                }
            }
            "Cancel"=>{
                let payload=cbor_member(frame.value(),"payload");
                let reply=Value::Map(vec![("executionId".to_owned(),cbor_member(payload,"executionId").clone()),
                    ("analysisOrdinal".to_owned(),cbor_member(payload,"analysisOrdinal").clone()),("observedPhase".to_owned(),Value::Text(observed.to_owned()))]);
                ts2_reply(data,&mut sequence,"Cancelled",reply);
            }
            _=>{}
        }
    }
    // Control cancel (or normal shutdown) is fully received before exit.
    assert!(ack.recv_timeout(Duration::from_secs(10)).is_ok());
}
''';p.write_text(s)
F=Path(__file__).parent;s=(F/'revocation_lane_r2.py').read_text().replace("'revocation-r2'","'matrix-r1'");s=s.replace("('review-rf-controls',[str(binary),'d3b2_review_']),", "('real-ts2-root-matrix',[str(binary),'d3b2_real_ts2_root_phase_matrix']),");(F/'matrix_lane_r1.py').write_text(s)
print('Five-phase native real TS2 codec matrix and first-party payload worker added')
