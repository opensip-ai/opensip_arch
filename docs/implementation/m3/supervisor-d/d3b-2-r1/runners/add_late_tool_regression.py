from pathlib import Path
W=Path('/Users/sb/code/opensip-ai/opensip-d3b2-takeover');p=W/'crates/components/src/supervisor_tests.rs';s=p.read_text();s=s.replace('''        1 => handle.user_signal() && handle.user_signal(),''','''        1 => { let first=handle.user_signal(); let second=handle.user_signal(); first&&second },''');s=s.replace('''        assert_eq!(supervision.late_events(), if kind == 1 { 1 } else { 1 }); // second call short-circuits on refusal''','''        assert_eq!(supervision.late_events(), if kind == 1 { 2 } else { 1 });''')
s+='''
struct D3b2OwnedSurvivor(ProcessIdentity);
impl Drop for D3b2OwnedSurvivor {
    fn drop(&mut self){
        // Test-only cleanup is restricted to this first-party identity.
        if matches!(process_identity(self.0.process_id()),Ok(Some(now)) if now==self.0){
            let _=std::process::Command::new("/bin/kill").args(["-9",&self.0.process_id().to_string()]).status();
        }
    }
}
#[test]
fn d3b2_final_tool_signal_discards_late_clean_ceiling_before_kill(){
    let dir=test_dir();let file=dir.0.join("clean-tool-survivor.pid");let script=format!("tool-clean-survivor:{}",file.display());
    let mut supervision=Supervision::prepare_tool(tool_spec_for(&fixture(),&script)).unwrap();supervision.seams.reap_blocked=true;
    let facts=Rc::clone(&supervision.seams.facts);let sink=Rc::clone(&facts);supervision.record_facts(Box::new(move|fact|sink.borrow_mut().push(fact)));
    let mut root=root_in(&dir);supervision.start(&mut root).unwrap();let cap=Instant::now()+HANDSHAKE;
    while !(supervision.state==State::Reaping&&supervision.clean_at.is_some()&&supervision.ladder.is_none()) {assert!(Instant::now()<cap);supervision.turn();}
    let pids=tree_pids(&file);assert_eq!(pids.len(),1);let identity=process_identity(pids[0]).unwrap().expect("owned survivor is alive");let _cleanup=D3b2OwnedSurvivor(identity);
    assert!(!supervision.group_alone());
    supervision.clean_at=Some(Instant::now()-(REAP_CEILING-Duration::from_millis(100)));
    assert!(supervision.handle().user_signal());supervision.turn();
    assert!(supervision.clean_at.is_none(),"old clean deadline must not preempt tool Stage2");
    assert_ne!(supervision.state,State::Settled,"no settlement before T3/tree step");
    assert!(has_identity(pids[0]),"survivor ignores TERM until KILL");
    supervision.seams.reap_blocked=false;
    while supervision.state!=State::Settled{assert!(Instant::now()<cap);supervision.turn();}
    let ladder=supervision.ladder.unwrap();assert!(ladder.kill_at.unwrap().duration_since(ladder.term_at.unwrap())>=TERM_TO_KILL);
    let settlement=supervision.take_settlement().unwrap();assert_eq!(settlement.first_cause(),Cause::UserCancel);assert!(settlement.user_interrupted());
    assert_eq!(records::settlement_route(&settlement),records::OwnerRoute::Interrupted);assert!(settlement.tree_evidence().is_some());
    assert_eq!(facts.borrow().iter().filter(|f|matches!(f,records::RecordFact::ToolTreeSwept{..})).count(),1);
    assert!(!facts.borrow().iter().any(|f|matches!(f,records::RecordFact::CancelForced{..})));
    assert!(eventually_without_identity(pids[0]),"native group KILL removed the actual survivor");
}
''';p.write_text(s)
p=W/'crates/components/tests/supervisor_fixture.rs';s=p.read_text();a='''    if let Some(n) = script.strip_prefix("tool-bytes-") {''';assert s.count(a)==1;s=s.replace(a,'''    if let Some(file)=script.strip_prefix("tool-clean-survivor:"){
        let marker=format!("{file}.ready");let exe=std::env::current_exe().unwrap();
        let child=std::process::Command::new("/bin/sh")
            .args(["-c","trap '' TERM; : > \\"$1\\"; exec \\"$2\\" \\"$3\\" hold-tree","first-party-survivor"])
            .arg(&marker).arg(exe).arg(SENTINEL)
            .stdin(std::process::Stdio::null()).stdout(std::process::Stdio::null()).stderr(std::process::Stdio::null()).spawn().unwrap();
        let cap=std::time::Instant::now()+Duration::from_secs(10);
        while !std::path::Path::new(&marker).exists(){assert!(std::time::Instant::now()<cap);std::thread::sleep(Duration::from_millis(1));}
        write_pids(file,&[child.id()]);std::process::exit(0);
    }
'''+a);p.write_text(s)
F=Path(__file__).parent;s=(F/'complete_lane_r1.py').read_text().replace("'complete-r1'","'complete-r2'");(F/'complete_lane_r2.py').write_text(s)
print('Late clean tool regression added; two refused signals are each actually attempted')
