from pathlib import Path
P=Path('/tmp/opensip-implementation/o1b-authoring-r1/product')
p=P/'crates/operability/Cargo.toml';s=p.read_text();assert 'harness-instrumentation = 'not in s;s=s.replace('operability-dev-sinks = []','operability-dev-sinks = []\nharness-instrumentation = []');p.write_text(s)
for rel,dependency in [('crates/host/Cargo.toml','opensip-operability'),('apps/cli/Cargo.toml','opensip-host')]:
 p=P/rel;s=p.read_text();old=f'operability-dev-sinks = ["{dependency}/operability-dev-sinks"]';assert old in s;s=s.replace(old,old+f'\nharness-instrumentation = ["{dependency}/harness-instrumentation"]');p.write_text(s)
p=P/'Cargo.toml';s=p.read_text();assert '[profile.harness]'not in s;s+='\n# M3-O1 item13: optimized measured instrumentation with explicit assertions.\n[profile.harness]\ninherits = "release"\ndebug-assertions = true\noverflow-checks = false\n';p.write_text(s)
p=P/'crates/operability/src/lib.rs';s=p.read_text();s=s.replace('mod catalog;','''#[cfg(all(feature = "harness-instrumentation", not(debug_assertions)))]
compile_error!("the harness-instrumentation feature requires debug assertions (law S-OP-2b item2)");

#[cfg(any(test, feature = "operability-dev-sinks", feature = "harness-instrumentation"))]
mod phase_clock;
#[cfg(any(feature = "operability-dev-sinks", feature = "harness-instrumentation"))]
mod phase;
#[cfg(any(feature = "operability-dev-sinks", feature = "harness-instrumentation"))]
pub use phase::{PhaseError, PhaseSpan, RequestSpan};
#[cfg(any(feature = "operability-dev-sinks", feature = "harness-instrumentation"))]
pub use phase_clock::TimingError;

mod catalog;''',1);p.write_text(s)
p=P/'crates/operability/src/phase_clock.rs';s=p.read_text().replace('pub(crate) enum TimingError','pub enum TimingError');p.write_text(s)
p=P/'crates/operability/src/scope.rs';s=p.read_text();s=s.replace('pub struct RequestId([u8; 16]);','''pub struct RequestId(
    [u8; 16],
    #[cfg(any(feature = "operability-dev-sinks", feature = "harness-instrumentation"))]
    Option<crate::phase_clock::Observation>,
);''',1);old='''impl RequestId {
    pub(crate) fn minted(bytes: [u8; 16]) -> Self {
        Self(bytes)
    }''';assert old in s;s=s.replace(old,'''impl RequestId {
    pub(crate) fn minted(bytes: [u8; 16]) -> Self {
        #[cfg(any(feature = "operability-dev-sinks", feature = "harness-instrumentation"))]
        { Self(bytes, crate::phase_clock::Observation::capture().ok()) }
        #[cfg(not(any(feature = "operability-dev-sinks", feature = "harness-instrumentation")))]
        { Self(bytes) }
    }''',1)
key='scope!(RequestScope { request: RequestId });';assert key in s;s=s.replace(key,key+'''
#[cfg(any(feature = "operability-dev-sinks", feature = "harness-instrumentation"))]
impl RequestScope {
    pub(crate) fn creation_observation(self) -> Option<crate::phase_clock::Observation> {
        self.request.1
    }
}
''',1);p.write_text(s)
p=P/'crates/operability/src/emit.rs';s=p.read_text();s+='''
// A clock-unavailable phase is an actual known-event producer refusal, never
// a completed event with made-up zero timings. Reserve before this refusal.
#[cfg(any(feature = "operability-dev-sinks", feature = "harness-instrumentation"))]
pub(crate) fn refuse_phase(scope: RequestScope, started: bool) {
    let (slot,max_line)=if started {(4,HostPhaseStarted::MAX_LINE)}else{(5,HostPhaseCompleted::MAX_LINE)};
    crate::transport::produce(Level::Info,slot,scope.request(),max_line,&||None);
}
''';p.write_text(s)
p=P/'crates/operability/src/phase.rs';p.write_text('''//! O1-b scoped, actual phase observations. No span completes on Drop.
//! Provider component slots are wired by D3a, which owns their vocabulary.
use crate::emit::EmitOn;
use crate::kinds::{Code,Elapsed};
use crate::kinds::registry::{HostPhaseCompleted,HostPhaseStarted,Phase,PhaseOutcome};
use crate::phase_clock::{self,Observation,TimingError};
use crate::scope::RequestScope;

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum PhaseError {
    Clock(TimingError),
    InvalidPhase,
    InvalidOutcome,
    ComponentNotWired,
}

pub struct RequestSpan {
    scope: RequestScope,
    created: Observation,
}

pub struct PhaseSpan<'a> {
    request: &'a RequestSpan,
    phase: Phase,
    started: Observation,
}

fn child_phase(phase: Phase) -> Result<(),PhaseError> {
    match phase {
        Phase::Request => Err(PhaseError::InvalidPhase),
        Phase::Provider|Phase::ProviderStart|Phase::ProviderAnalysis|Phase::ProviderTeardown => Err(PhaseError::ComponentNotWired),
        _ => Ok(()),
    }
}
fn running_outcome(outcome: PhaseOutcome) -> Result<(),PhaseError> {
    if outcome==PhaseOutcome::NotApplicable { Err(PhaseError::InvalidOutcome) } else { Ok(()) }
}
fn observe(scope: RequestScope, started: bool) -> Result<Observation,PhaseError> {
    Observation::capture().map_err(|error| {
        crate::emit::refuse_phase(scope,started);
        PhaseError::Clock(error)
    })
}

impl RequestSpan {
    /// Starts at the actual request scope's creation observation, with `at` zero.
    pub fn begin(scope: RequestScope) -> Result<Self,PhaseError> {
        let created=scope.creation_observation().ok_or_else(|| {
            crate::emit::refuse_phase(scope,true);
            PhaseError::Clock(TimingError::ObservationUnavailable)
        })?;
        HostPhaseStarted::new(Phase::Request,Elapsed::new(0)).emit(scope);
        Ok(Self { scope,created })
    }
    pub fn start(&self, phase: Phase) -> Result<PhaseSpan<'_>,PhaseError> {
        child_phase(phase)?;
        let started=observe(self.scope,true)?;
        let at=phase_clock::at(self.created,started).map_err(|error| {
            crate::emit::refuse_phase(self.scope,true);
            PhaseError::Clock(error)
        })?;
        HostPhaseStarted::new(phase,Elapsed::new(at)).emit(self.scope);
        Ok(PhaseSpan { request:self,phase,started })
    }
    /// An owner that actually decides not to run its phase emits only completion.
    pub fn not_applicable(&self, phase: Phase) -> Result<(),PhaseError> {
        child_phase(phase)?;
        let observed=observe(self.scope,false)?;
        let at=phase_clock::at(self.created,observed).map_err(|error| {
            crate::emit::refuse_phase(self.scope,false);
            PhaseError::Clock(error)
        })?;
        HostPhaseCompleted::new(Code::from_enum(phase),Elapsed::new(0),Elapsed::new(0),Code::from_enum(PhaseOutcome::NotApplicable),Elapsed::new(at)).emit(self.scope);
        Ok(())
    }
    /// The request's final completion must precede the logging cutoff.
    pub fn finish(self, outcome: PhaseOutcome) -> Result<(),PhaseError> {
        running_outcome(outcome)?;
        self.finish_phase(Phase::Request,self.created,outcome)
    }
    fn finish_phase(&self, phase: Phase, started: Observation, outcome: PhaseOutcome) -> Result<(),PhaseError> {
        let ended=observe(self.scope,false)?;
        let sample=phase_clock::complete(self.created,started,ended).map_err(|error| {
            crate::emit::refuse_phase(self.scope,false);
            PhaseError::Clock(error)
        })?;
        HostPhaseCompleted::new(Code::from_enum(phase),Elapsed::new(sample.wall),Elapsed::new(sample.cpu),Code::from_enum(outcome),Elapsed::new(sample.at)).emit(self.scope);
        Ok(())
    }
}
impl PhaseSpan<'_> {
    pub fn finish(self, outcome: PhaseOutcome) -> Result<(),PhaseError> {
        running_outcome(outcome)?;
        self.request.finish_phase(self.phase,self.started,outcome)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn the_span_api_rejects_unowned_components_and_false_nonrunning_completion() {
        for phase in [Phase::Provider,Phase::ProviderStart,Phase::ProviderAnalysis,Phase::ProviderTeardown] {
            assert_eq!(child_phase(phase),Err(PhaseError::ComponentNotWired));
        }
        assert_eq!(child_phase(Phase::Request),Err(PhaseError::InvalidPhase));
        assert_eq!(child_phase(Phase::Delivery),Ok(()));
        assert_eq!(running_outcome(PhaseOutcome::NotApplicable),Err(PhaseError::InvalidOutcome));
        for outcome in [PhaseOutcome::Completed,PhaseOutcome::Failed,PhaseOutcome::Cancelled] {
            assert_eq!(running_outcome(outcome),Ok(()));
        }
    }
}
''')
print('O1-b clock-anchored span API prepared in isolated draft')
