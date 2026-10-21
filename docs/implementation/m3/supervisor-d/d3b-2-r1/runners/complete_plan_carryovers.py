from pathlib import Path
W=Path('/Users/sb/code/opensip-ai/opensip-d3b2-takeover');p=W/'crates/components/src/supervisor.rs';s=p.read_text()
def one(a,b):
 global s
 assert s.count(a)==1,(a[:100],s.count(a));s=s.replace(a,b)
one('''    determination_failures: Vec<(opensip_operability::RevocationMark, RevocationClockFailure)>,''','''    determination_failures: Vec<(opensip_operability::RevocationMark, RevocationClockFailure)>,
    normal_shutdown_completed_before_arming: bool,
    control_input_open_at_arming: bool,''')
one('''    pub fn arming_failure(&self) -> Option<&RevocationClockFailure> {''','''    /// Q12: distinguish completed normal shutdown from an otherwise closed
    /// channel; this is settlement evidence, never a cancel-sent claim.
    pub fn normal_shutdown_completed_before_arming(&self) -> bool { self.normal_shutdown_completed_before_arming }
    pub fn control_input_open_at_arming(&self) -> bool { self.control_input_open_at_arming }
    pub fn arming_failure(&self) -> Option<&RevocationClockFailure> {''')
one('''                determination_failures: Vec::with_capacity(4),''','''                determination_failures: Vec::with_capacity(4),
                normal_shutdown_completed_before_arming: false,
                control_input_open_at_arming: false,''')
one('''    close_fd3_after_write: bool,
    host_seq:''','''    close_fd3_after_write: bool,
    normal_shutdown_completed: bool,
    host_seq:''')
one('''            close_fd3_after_write: false,
            host_seq:''','''            close_fd3_after_write: false,
            normal_shutdown_completed: false,
            host_seq:''')
one('''                // its shutdown itself is written.
                self.ends.fd3 = None;''','''                // its shutdown itself is written.
                self.normal_shutdown_completed = true;
                self.ends.fd3 = None;''')
one('''            self.seams.revocation_clock_reads += 1;
            if let Some(read) = self.seams.revocation_reads.pop_front() {''','''            self.seams.revocation_clock_reads += 1;
            if let Some(hook) = &mut self.seams.revocation_read_hook { return (hook.0)(); }
            if let Some(read) = self.seams.revocation_reads.pop_front() {''')
one('''        let (tracking, facts) = RevocationTracking::arm(''','''        let (mut tracking, facts) = RevocationTracking::arm(''')
one('''        self.revocation = Some(tracking);
        for fact in facts {''','''        tracking.evidence.normal_shutdown_completed_before_arming = self.normal_shutdown_completed;
        tracking.evidence.control_input_open_at_arming = self.ends.fd3.is_some();
        self.revocation = Some(tracking);
        for fact in facts {''')
# Pin the accepted clock-pair sampling order directly at both owner calls.
a='''        let read = self.revocation_clock();
        let now = Instant::now();''';assert s.count(a)==2;s=s.replace(a,'''        // D3BPLAN-R3-NBO-1: observe_clock finishes before this Instant;
        // otherwise a slow arming read would be counted twice in the lower bound.
        let read = self.revocation_clock();
        let now = Instant::now();''');p.write_text(s)
p=W/'crates/components/src/supervisor_tests.rs';s=p.read_text();a='''pub(crate) struct Seams {''';assert s.count(a)==1;s=s.replace(a,a+'''
    pub(super) revocation_read_hook: Option<RevocationReadHook>,''');idx=s.index('/// The supervision\'s test seams.');s=s[:idx]+'''pub(super) struct RevocationReadHook(pub(super) Box<dyn FnMut()->Result<RevocationClockSample,RevocationClockFailure>>);
impl std::fmt::Debug for RevocationReadHook {
    fn fmt(&self,f:&mut std::fmt::Formatter<'_>)->std::fmt::Result { f.write_str("first-party clock-read hook") }
}

'''+s[idx:];a='''    let is_tool = settlement.is_tool();
    assert_eq!(
        evidence.state(opensip_operability::RevocationMark::ProtocolCancel),''';assert s.count(a)==1;s=s.replace(a,'''    let is_tool = settlement.is_tool();
    assert_eq!(evidence.normal_shutdown_completed_before_arming(), !is_tool, "Q12 retains the actual fully written normal shutdown");
    assert!(!evidence.control_input_open_at_arming(), "no cancel was writable on the already closed host input");
    assert_eq!(
        evidence.state(opensip_operability::RevocationMark::ProtocolCancel),''')
s+='''
#[test]
fn d3b2_final_delayed_clock_reads_sample_instants_after_the_reads(){
    use std::cell::Cell;
    let(mut supervision,_)=prepared("normal",FixtureParticipant::new(ProtocolWaits::TS2),None);
    supervision.ends.fd3=Some(std::fs::OpenOptions::new().write(true).open("/dev/null").unwrap());
    let arm_done=Rc::new(Cell::new(None));let determine_done=Rc::new(Cell::new(None));
    let a=Rc::clone(&arm_done);let d=Rc::clone(&determine_done);let mut calls=0;
    supervision.seams.revocation_read_hook=Some(RevocationReadHook(Box::new(move||{
        std::thread::sleep(Duration::from_millis(20));calls+=1;
        if calls==1 {let read=RevocationClockSample::native();a.set(Some(Instant::now()));read}
        else {d.set(Some(Instant::now()));Err(d3b2_clock_failure())}
    })));
    let observed=opensip_platform::observe_clock().unwrap();supervision.observer_trigger(Cause::Revoked,observed);
    let tracking=supervision.revocation.as_ref().unwrap();let armed=tracking.evidence.armed_at.unwrap();let lag=tracking.evidence.arming_lag.unwrap();
    assert!(armed>=arm_done.get().unwrap(),"arming Instant before read would double-count the read interval");
    supervision.resolve_revocation_mark(opensip_operability::RevocationMark::ProtocolCancel,false);
    let after=Instant::now();
    let facts=supervision.seams.facts.borrow();let value=facts.iter().find_map(|f|match f{
        records::RecordFact::RevocationMissed{mark:opensip_operability::RevocationMark::ProtocolCancel,measurement:records::RevocationMeasurement::LowerBound(elapsed),..}=>Some(*elapsed),_=>None
    }).unwrap();
    assert!(value>=lag+determine_done.get().unwrap().duration_since(armed),"decision Instant must include the failed read interval");
    assert!(value<=lag+after.duration_since(armed),"no arming-read interval counted twice");
    assert_eq!(supervision.seams.revocation_clock_reads,2);
}
''';p.write_text(s)
F=Path(__file__).parent;s=(F/'complete_lane_r2.py').read_text().replace("'complete-r2'","'complete-r3'");(F/'complete_lane_r3.py').write_text(s)
print('Accepted Q12 shutdown evidence and NBO clock-pair-order delayed read control added')
