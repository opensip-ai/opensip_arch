/// S6's action outcome. Only a transition out of Pending can emit a miss.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum RevocationMarkState { Pending, Satisfied, Missed, Inapplicable }
/// Failed native or validity read; no invented boot identity or elapsed.
#[derive(Debug)]
pub enum RevocationClockFailure {
    Native(opensip_platform::ClockError),
    BootChanged,
    RegressedBeforeReference,
}
#[derive(Debug, Clone)]
struct RevocationClockSample { after: Duration, boot: String }
impl RevocationClockSample {
    fn native() -> Result<Self, RevocationClockFailure> {
        opensip_platform::observe_clock().map(|sample| Self {
            after: sample.monotonic_after(), boot: sample.boot_id().to_owned()
        }).map_err(RevocationClockFailure::Native)
    }
}
/// The original observer reference, mark states and measurement failures.
/// This is internal settlement evidence, never an operational record.
#[derive(Debug)]
pub struct RevocationEvidence {
    observation: opensip_platform::ClockObservation,
    states: [RevocationMarkState; 5],
    arming_lag: Option<Duration>,
    armed_at: Option<Instant>,
    arming_failure: Option<RevocationClockFailure>,
    determination_failures: Vec<(opensip_operability::RevocationMark, RevocationClockFailure)>,
}
impl RevocationEvidence {
    pub fn observation(&self) -> &opensip_platform::ClockObservation { &self.observation }
    pub fn state(&self, mark: opensip_operability::RevocationMark) -> RevocationMarkState { self.states[mark as usize] }
    pub fn arming_failure(&self) -> Option<&RevocationClockFailure> { self.arming_failure.as_ref() }
    pub fn determination_failures(&self) -> &[(opensip_operability::RevocationMark, RevocationClockFailure)] { &self.determination_failures }
}
const REVOCATION_MARKS: [opensip_operability::RevocationMark; 5] = {
    use opensip_operability::RevocationMark::*;
    [RequestsRefused, ProtocolCancel, Sigterm, KillAndReap, ScratchCleanup]
};
/// SL S6:492-494. These observe actions; scratch removal is never truncated.
fn revocation_bound(mark: opensip_operability::RevocationMark) -> Duration {
    use opensip_operability::RevocationMark::*;
    Duration::from_secs(match mark { RequestsRefused => 0, ProtocolCancel => 2,
        Sigterm => 3, KillAndReap => 5, ScratchCleanup => 10 })
}
struct RevocationTracking {
    evidence: RevocationEvidence,
    deadlines: [Option<Instant>; 5],
}
impl RevocationTracking {
    fn pending(&self, mark: opensip_operability::RevocationMark) -> bool {
        self.evidence.state(mark) == RevocationMarkState::Pending
    }
    fn validate(&self, sample: RevocationClockSample) -> Result<Duration, RevocationClockFailure> {
        if sample.boot != self.evidence.observation.boot_id() { return Err(RevocationClockFailure::BootChanged); }
        sample.after.checked_sub(self.evidence.observation.monotonic_before())
            .ok_or(RevocationClockFailure::RegressedBeforeReference)
    }
    fn arm(observation: opensip_platform::ClockObservation, tool: bool,
           read: Result<RevocationClockSample, RevocationClockFailure>, now: Instant,
           completed: &[bool; 5], impossible: &[bool; 5], prior: &[Option<RevocationClockSample>; 5])
           -> (Self, Vec<records::RecordFact>) {
        use opensip_operability::RevocationMark as M;
        let mut states = [RevocationMarkState::Pending; 5];
        states[M::RequestsRefused as usize] = RevocationMarkState::Satisfied;
        if tool { states[M::ProtocolCancel as usize] = RevocationMarkState::Inapplicable; }
        let mut tracking = Self { evidence: RevocationEvidence { observation, states,
            arming_lag: None, armed_at: None, arming_failure: None,
            determination_failures: Vec::with_capacity(4) }, deadlines: [None; 5] };
        let lag = match read.and_then(|sample| tracking.validate(sample)) {
            Ok(lag) => { tracking.evidence.arming_lag = Some(lag); tracking.evidence.armed_at = Some(now); lag },
            Err(error) => {
                tracking.evidence.arming_failure = Some(error);
                let mut facts = Vec::new();
                for mark in REVOCATION_MARKS {
                    if let Some(fact) = tracking.miss(mark, records::RevocationMeasurement::Unavailable) { facts.push(fact); }
                }
                return (tracking, facts);
            }
        };
        let mut facts = Vec::new();
        for mark in REVOCATION_MARKS {
            if !tracking.pending(mark) { continue; }
            let i = mark as usize; let bound = revocation_bound(mark);
            // Cached native completion is conservative: its later bracket
            // is after the successful action. Without it only the arm's
            // valid upper bound can establish timely completion.
            let prior_proves = prior[i].as_ref().is_some_and(|sample|
                sample.boot == tracking.evidence.observation.boot_id() &&
                sample.after.saturating_sub(tracking.evidence.observation.monotonic_before()) <= bound);
            if completed[i] && (prior_proves || lag <= bound) {
                tracking.evidence.states[i] = RevocationMarkState::Satisfied;
            } else if impossible[i] || lag >= bound {
                if let Some(fact) = tracking.miss(mark, records::RevocationMeasurement::Measured(lag)) { facts.push(fact); }
            } else { tracking.deadlines[i] = Some(now + (bound - lag)); }
        }
        (tracking, facts)
    }
    fn miss(&mut self, mark: opensip_operability::RevocationMark, measurement: records::RevocationMeasurement) -> Option<records::RecordFact> {
        if !self.pending(mark) { return None; }
        self.evidence.states[mark as usize] = RevocationMarkState::Missed;
        self.deadlines[mark as usize] = None;
        Some(records::RecordFact::RevocationMissed { mark, measurement, bound: revocation_bound(mark) })
    }
    fn determine(&mut self, mark: opensip_operability::RevocationMark, completed: bool,
                 read: Result<RevocationClockSample, RevocationClockFailure>, now: Instant) -> Option<records::RecordFact> {
        if !self.pending(mark) { return None; }
        match read.and_then(|sample| self.validate(sample)) {
            Ok(elapsed) if completed && elapsed <= revocation_bound(mark) => {
                self.evidence.states[mark as usize] = RevocationMarkState::Satisfied;
                self.deadlines[mark as usize] = None; None
            }
            Ok(elapsed) => self.miss(mark, records::RevocationMeasurement::Measured(elapsed)),
            Err(error) => {
                self.evidence.determination_failures.push((mark, error));
                // Only a successful arm can leave a pending mark.
                let lag = self.evidence.arming_lag.expect("pending after successful arm only");
                let armed = self.evidence.armed_at.expect("successful arming Instant");
                let elapsed = lag.saturating_add(now.saturating_duration_since(armed));
                self.miss(mark, records::RevocationMeasurement::LowerBound(elapsed))
            }
        }
    }
}
