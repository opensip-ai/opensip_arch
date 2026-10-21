from pathlib import Path
F=Path(__file__).parent;W=Path('/Users/sb/code/opensip-ai/opensip-d3b2-takeover');p=W/'crates/components/src/supervisor_records.rs';s=p.read_text();idx=s.index('/// The registry event') if False else s.index('#[derive(Debug, Clone, Copy, PartialEq, Eq)]')
s=s[:idx]+'''/// Three closed measurement shapes; elapsed exists exactly for the first two.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum RevocationMeasurement { Measured(Duration), LowerBound(Duration), Unavailable }
impl RevocationMeasurement {
    pub fn status(self) -> opensip_operability::ElapsedStatus {
        match self { Self::Measured(_) => opensip_operability::ElapsedStatus::Measured,
            Self::LowerBound(_) => opensip_operability::ElapsedStatus::LowerBound,
            Self::Unavailable => opensip_operability::ElapsedStatus::Unavailable }
    }
    pub fn elapsed(self) -> Option<Duration> {
        match self { Self::Measured(d) | Self::LowerBound(d) => Some(d), Self::Unavailable => None }
    }
}

'''+s[idx:];a='''    /// `supervision.wait.expired`: the wait and its configured bound.''';assert s.count(a)==1;s=s.replace(a,'''    RevocationMissed { mark: opensip_operability::RevocationMark, measurement: RevocationMeasurement, bound: Duration },
    ToolRevocationMissed { mark: opensip_operability::RevocationMark, measurement: RevocationMeasurement, bound: Duration },
'''+a);s=s.replace('''        match self {
            Self::ProcessSpawned''','''        match self {
            Self::RevocationMissed { .. } => opensip_operability::SupervisionRevocationMissed::NAME,
            Self::ToolRevocationMissed { .. } => opensip_operability::ToolRevocationMissed::NAME,
            Self::ProcessSpawned''',1);a='''            Self::CancelSent { .. } => &["inband", "control_reason"],''';assert s.count(a)==1;s=s.replace(a,a+'''
            Self::RevocationMissed { .. } | Self::ToolRevocationMissed { .. } => &["mark", "elapsed_status", "elapsed", "bound"],''');a='''            Self::ToolSpawned { .. }
            | Self::ToolReaped''';assert s.count(a)==1;s=s.replace(a,'''            Self::ToolRevocationMissed { .. }
            | Self::ToolSpawned { .. }
            | Self::ToolReaped''');a='''    pub fn for_tool(self) -> Option<Self> {
        match self {''';assert s.count(a)==1;s=s.replace(a,a+'''
            Self::RevocationMissed { mark, measurement, bound } => Some(Self::ToolRevocationMissed { mark, measurement, bound }),
            Self::ToolRevocationMissed { .. } => Some(self),''');p.write_text(s)
p=W/'crates/components/src/supervisor.rs';s=p.read_text()
def one(a,b):
 global s
 assert s.count(a)==1,(a[:100],s.count(a));s=s.replace(a,b)
one('''pub const REAP_CEILING: Duration = Duration::from_secs(10);''','''pub const REAP_CEILING: Duration = Duration::from_secs(10);
/// Item14:494, revocation/fail-stop's reap ceiling after KILL (PLAN-r3 LD-D3B-10).
pub const REAP_CEILING_REVOCATION: Duration = Duration::from_secs(5);''')
idx=s.index('/// A cross-thread trigger');s=s[:idx]+(F/'revocation_types.rs').read_text()+'\n'+s[idx:]
one('''#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum Trigger {
    HostFault,
}''','''#[derive(Debug)]
enum Trigger {
    HostFault,
    Revoked(opensip_platform::ClockObservation),
    ObserverFailStop(opensip_platform::ClockObservation),
}''')
one('''    pub fn user_signal(&self) -> bool {
        self.gate.user_signal()
    }''','''    pub fn user_signal(&self) -> bool {
        self.gate.user_signal()
    }
    pub fn revoked(&self, observed: opensip_platform::ClockObservation) -> bool { self.gate.admit(Trigger::Revoked(observed)) }
    pub fn observer_fail_stop(&self, observed: opensip_platform::ClockObservation) -> bool { self.gate.admit(Trigger::ObserverFailStop(observed)) }''')
one('''                Some(GateMessage::Queued(Trigger::HostFault)) => self.trigger(Cause::HostFault),''','''                Some(GateMessage::Queued(Trigger::HostFault)) => self.trigger(Cause::HostFault),
                Some(GateMessage::Queued(Trigger::Revoked(observed))) => self.observer_trigger(Cause::Revoked, observed),
                Some(GateMessage::Queued(Trigger::ObserverFailStop(observed))) => self.observer_trigger(Cause::ObserverFailStop, observed),''')
one('''    stage1: Option<Stage1Evidence>,
    exit: ExitClass,''','''    stage1: Option<Stage1Evidence>,
    revocation: Option<RevocationEvidence>,
    exit: ExitClass,''')
one('''    pub fn stage1_evidence(&self) -> Option<Stage1Evidence> {''','''    pub fn revocation_evidence(&self) -> Option<&RevocationEvidence> { self.revocation.as_ref() }
    pub fn stage1_evidence(&self) -> Option<Stage1Evidence> {''')
one('''    cancel_control: Option<ControlCancel>,
    grace_expired: bool,''','''    cancel_control: Option<ControlCancel>,
    observer_seen: bool,
    revocation: Option<RevocationTracking>,
    completed_actions: [bool; 5],
    impossible_actions: [bool; 5],
    action_clocks: [Option<RevocationClockSample>; 5],
    grace_expired: bool,''')
one('''            cancel_control: None,
            grace_expired: false,''','''            cancel_control: None,
            observer_seen: false,
            revocation: None,
            completed_actions: [false; 5],
            impossible_actions: [false; 5],
            action_clocks: std::array::from_fn(|_| None),
            grace_expired: false,''')
one('''            stage1: self.stage1.map(|s| s.evidence),
            exit,''','''            stage1: self.stage1.map(|s| s.evidence),
            revocation: self.revocation.take().map(|t| t.evidence),
            exit,''')
# All uses refer to the selected ceiling, never shortening S6 marks.
s=s.replace('self.waits.reap_ceiling','self.reap_ceiling()')
one('''    fn timers(&mut self) {
        let now = Instant::now();''','''    fn timers(&mut self) {
        let now = Instant::now();
        self.revocation_timers(now);''')
one('''        all.into_iter().min()
    }''','''        if let Some(tracking) = &self.revocation { all.extend(tracking.deadlines.iter().flatten().copied()); }
        all.into_iter().min()
    }''')
one('''    fn control_cancel(&mut self, outcome: ControlCancel) {
        self.cancel_control = Some(outcome);''','''    fn control_cancel(&mut self, outcome: ControlCancel) {
        self.cancel_control = Some(outcome);
        if outcome == ControlCancel::Written { self.mark_completed(opensip_operability::RevocationMark::ProtocolCancel); }
        else if matches!(outcome, ControlCancel::Refused | ControlCancel::Failed | ControlCancel::Abandoned) {
            self.mark_impossible(opensip_operability::RevocationMark::ProtocolCancel);
        }''')
# Keep one entry point for loop faults and observer observations; arm marks
# after cause/state bookkeeping, before immediate Stage1 fault escalation.
one('''    fn trigger_from(&mut self, cause: Cause, from_t2: bool) {
        if self.state == State::Settled''','''    fn trigger_from(&mut self, cause: Cause, from_t2: bool) { self.trigger_observed(cause, from_t2, None); }
    fn observer_trigger(&mut self, cause: Cause, observed: opensip_platform::ClockObservation) {
        self.trigger_observed(cause, false, Some(observed));
    }
    fn trigger_observed(&mut self, cause: Cause, from_t2: bool, observed: Option<opensip_platform::ClockObservation>) {
        if self.state == State::Settled''')
one('''        if self.stage1_active() && cause != Cause::UserCancel {''','''        if let Some(observed) = observed && !self.observer_seen {
            self.observer_seen = true;
            self.arm_revocation(observed);
        }
        if self.stage1_active() && cause != Cause::UserCancel {''')
one('''    fn signal(&self, signal: i32) -> bool {
        self.child
            .as_ref()
            .is_some_and(|child| child.signal_group(signal).is_ok())
    }''','''    fn signal(&mut self, signal: i32) -> bool {
        let sent = self.child.as_ref().is_some_and(|child| child.signal_group(signal).is_ok());
        if signal == SIGTERM {
            if sent { self.mark_completed(opensip_operability::RevocationMark::Sigterm); }
            else { self.mark_impossible(opensip_operability::RevocationMark::Sigterm); }
        }
        sent
    }''')
one('''                self.reaped = Some(reaped);
                self.append(SupervisionEvent::Reaped);''','''                self.reaped = Some(reaped);
                self.mark_completed(opensip_operability::RevocationMark::KillAndReap);
                self.append(SupervisionEvent::Reaped);''')
one('''        if self.cancel_control == Some(ControlCancel::Queued) {
            self.control_cancel(ControlCancel::Abandoned);
        }''','''        if exit == ExitClass::Unreaped { self.mark_impossible(opensip_operability::RevocationMark::KillAndReap); }
        if scratch == ScratchFate::Removed { self.mark_completed(opensip_operability::RevocationMark::ScratchCleanup); }
        else { self.mark_impossible(opensip_operability::RevocationMark::ScratchCleanup); }
        self.resolve_all_revocation_marks();
        if self.cancel_control == Some(ControlCancel::Queued) {
            self.control_cancel(ControlCancel::Abandoned);
        }''')
# Methods own the mark transaction with take/restore: no borrowed state
# crosses callbacks, and failed arm/past terminal marks make no later read.
idx=s.index('    fn stage1_active(&self)')
s=s[:idx]+'''    fn reap_ceiling(&self) -> Duration { if self.observer_seen { REAP_CEILING_REVOCATION } else { self.waits.reap_ceiling } }
    fn revocation_clock(&mut self) -> Result<RevocationClockSample, RevocationClockFailure> {
        #[cfg(test)] {
            self.seams.revocation_clock_reads += 1;
            if let Some(read) = self.seams.revocation_reads.pop_front() { return read; }
        }
        RevocationClockSample::native()
    }
    fn arm_revocation(&mut self, observed: opensip_platform::ClockObservation) {
        use opensip_operability::RevocationMark as M;
        if self.class == Class::Provider && self.ends.fd3.is_none() && self.cancel_control != Some(ControlCancel::Written) {
            self.impossible_actions[M::ProtocolCancel as usize] = true;
        }
        let read = self.revocation_clock(); let now = Instant::now();
        let (tracking, facts) = RevocationTracking::arm(observed, self.class == Class::Tool, read, now,
            &self.completed_actions, &self.impossible_actions, &self.action_clocks);
        self.revocation = Some(tracking);
        for fact in facts { self.fact(fact); }
    }
    fn resolve_revocation_mark(&mut self, mark: opensip_operability::RevocationMark, completed: bool) {
        if !self.revocation.as_ref().is_some_and(|t| t.pending(mark)) { return; }
        let read = self.revocation_clock(); let now = Instant::now();
        let fact = self.revocation.as_mut().unwrap().determine(mark, completed, read, now);
        if let Some(fact) = fact { self.fact(fact); }
    }
    fn mark_completed(&mut self, mark: opensip_operability::RevocationMark) {
        let i = mark as usize;
        if !self.completed_actions[i] {
            self.completed_actions[i] = true;
            // Only needed before the observer arms: an action already done
            // may predate its reference or its bound despite delayed delivery.
            if !self.observer_seen { self.action_clocks[i] = RevocationClockSample::native().ok(); }
        }
        self.resolve_revocation_mark(mark, true);
    }
    fn mark_impossible(&mut self, mark: opensip_operability::RevocationMark) {
        self.impossible_actions[mark as usize] = true;
        self.resolve_revocation_mark(mark, false);
    }
    fn revocation_timers(&mut self, now: Instant) {
        for mark in REVOCATION_MARKS {
            if self.revocation.as_ref().is_some_and(|t| t.deadlines[mark as usize].is_some_and(|at| now >= at)) {
                self.resolve_revocation_mark(mark, false);
            }
        }
    }
    fn resolve_all_revocation_marks(&mut self) {
        for mark in REVOCATION_MARKS { self.resolve_revocation_mark(mark, false); }
    }

'''+s[idx:];p.write_text(s)
# Test-only reduced clock seam; never construct a platform observation.
p=W/'crates/components/src/supervisor_tests.rs';s=p.read_text();a='''pub(crate) struct Seams {''';assert s.count(a)==1;s=s.replace(a,a+'''
    pub(crate) revocation_reads: VecDeque<Result<RevocationClockSample, RevocationClockFailure>>,
    pub(crate) revocation_clock_reads: u64,''');s=s.replace('''        stage1: None,
        exit: ExitClass::Exited(0),''','''        stage1: None,
        revocation: None,
        exit: ExitClass::Exited(0),''');# Generic message equality cannot require Eq on an owned native observation.
s=s.replace('''        assert_eq!(gate.take(), Some(GateMessage::Queued(Trigger::HostFault)));''','''        assert!(matches!(gate.take(), Some(GateMessage::Queued(Trigger::HostFault))));''');s=s.replace('assert_eq!(gate.take(), Some(GateMessage::FirstSignal));','assert!(matches!(gate.take(), Some(GateMessage::FirstSignal)));');s=s.replace('assert_eq!(gate.take(), Some(GateMessage::SecondSignal));','assert!(matches!(gate.take(), Some(GateMessage::SecondSignal)));');s=s.replace('assert_eq!(supervision.gate.take(), Some(GateMessage::FirstSignal));','assert!(matches!(supervision.gate.take(), Some(GateMessage::FirstSignal)));');p.write_text(s)
print('Observer handles and sleep-inclusive mark tracker wired; verification pending')
