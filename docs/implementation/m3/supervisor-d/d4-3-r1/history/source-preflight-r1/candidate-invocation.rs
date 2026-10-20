//! Law M3-J1 r5 (unit J2a): the invocation model of the three M3 analysis
//! requests, pure. It holds:
//! - R1, the typed request (item 4), and R2's installation entry through
//!   `request.rs`'s exhaustive table;
//! - the step lists (item 5.1) and WS section 1's step-list rules, whose
//!   refusal is item 10's row 2 for a host-built list;
//! - the analysis step's join chain (item 5.2) as consumed tokens;
//! - the cancellation source and phase recording (items 8.2 and 8.3, with
//!   lead decision LD-r5-1);
//! - the output decision point, the final output section and settlement
//!   (items 5.3 and 8.4, under the bound successors S18 and S21).
//!
//! It does no I/O and has no process, filesystem, clock or signal effect.
//! No analysis word is wired in the binary (item 1), and nothing here is
//! public: J2b, J2c and J3d drive it. It never reads a home, profile or
//! release selector (X11:66).
use crate::outcomes::{
    AnalysisOutcome, EphemeralVerdict, Observation, RequestExcludedClass, StepResult, Termination,
    aggregate, project,
};
use crate::request::{InstallationEntry, InstallationEntryError, installation_entry};
use opensip_contracts::generated::evidence::{
    Common4D9Signal as Signal, Common4DomainDetailCode as Detail,
};
use opensip_contracts::generated::invocation::{
    Inventory3CommandName as Command, Invocation5StepKind as StepKind,
};
use opensip_security::InstallationTermination as Row;
use std::marker::PhantomData;
use std::path::PathBuf;

// ------------------------------------------------------- R1: the request

/// Item 1: the three M3 requests. `fit` and `audit` are not in the M3
/// request type, and `--ephemeral` is not accepted on the default command
/// (CINV `default`), so none of them is representable.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum AnalysisRequest {
    /// `opensip`, durable.
    Default,
    /// `opensip analyze`, durable.
    Analyze,
    /// `opensip analyze --ephemeral`.
    AnalyzeEphemeral,
}
/// Step 0's durability (`AnalysisParams.durability`).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum Durability {
    Authoritative,
    Ephemeral,
}
impl AnalysisRequest {
    /// The command-inventory row the request is.
    pub(crate) fn command(self) -> Command {
        match self {
            Self::Default => Command::Default,
            Self::Analyze | Self::AnalyzeEphemeral => Command::Analyze,
        }
    }
    pub(crate) fn durability(self) -> Durability {
        match self {
            Self::Default | Self::Analyze => Durability::Authoritative,
            Self::AnalyzeEphemeral => Durability::Ephemeral,
        }
    }
}

/// M3-B r2 item 3's one typed observation: `interactive` is computed once
/// by the entry's caller, never from the environment.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) struct InvocationModeV1 {
    pub(crate) interactive: bool,
}

/// Item 1: the M3 request carries one format, JSON (ENV7).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum OutputFormat {
    Json,
}

/// The parsed values of M3-B r2 item 23's flags that the command inventory
/// gives `default` and `analyze`, besides `--ephemeral`, which is the
/// request itself. R1 carries them typed; their owners admit them later
/// (B2-b, B1-a, B3-a), and nothing here grants what they name.
#[derive(Debug, Clone, Default, PartialEq, Eq)]
pub(crate) struct RequestFlags {
    /// `--project`: at most one explicit authority root.
    pub(crate) project: Option<PathBuf>,
    /// `--workspace-root`, repeatable, in the order given.
    pub(crate) workspace_roots: Vec<PathBuf>,
    /// `--trust-group <gid>`, repeatable, in the order given.
    pub(crate) trust_groups: Vec<u32>,
    /// `--trust-project-owner`.
    pub(crate) trust_project_owner: bool,
    /// `--allow-backup-custody`.
    pub(crate) allow_backup_custody: bool,
}

/// R1's typed value: the request, its flags and mode, JSON, and the step
/// list the host built for it.
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) struct AdmittedRequest {
    request: AnalysisRequest,
    flags: RequestFlags,
    mode: InvocationModeV1,
    format: OutputFormat,
    steps: StepList,
}
impl AdmittedRequest {
    /// R1 (item 4): build the step list and check it under WS section 1. A
    /// host-built list that fails its own check is item 10's row 2, the
    /// host-generated internal layer (NE:3573), with its key in the
    /// operational record.
    pub(crate) fn admit(
        request: AnalysisRequest,
        flags: RequestFlags,
        mode: InvocationModeV1,
    ) -> Result<Self, Observation> {
        let steps = StepList::for_request(request);
        check_step_list(steps.specs()).map_err(StepListFault::observation)?;
        let admitted = Self {
            request,
            flags,
            mode,
            format: OutputFormat::Json,
            steps,
        };
        // D4-3: the opaque R1 token cannot leave admission before item 25
        // has classified it. No RequestId draw or durable entry occurs here.
        if let Some(first) = request_excluded_form(&admitted) {
            return Err(Observation::ExcludedRequest {
                first,
                rest: Vec::new(),
            });
        }
        Ok(admitted)
    }
    pub(crate) fn request(&self) -> AnalysisRequest {
        self.request
    }
    pub(crate) fn flags(&self) -> &RequestFlags {
        &self.flags
    }
    pub(crate) fn mode(&self) -> InvocationModeV1 {
        self.mode
    }
    pub(crate) fn format(&self) -> OutputFormat {
        self.format
    }
    pub(crate) fn steps(&self) -> &StepList {
        &self.steps
    }
    /// R2: `Creator` for a durable request, `Outside` for an ephemeral one,
    /// from `request.rs`'s exhaustive table.
    pub(crate) fn installation_entry(&self) -> Result<InstallationEntry, InstallationEntryError> {
        installation_entry(
            self.request.command(),
            self.request.durability() == Durability::Ephemeral,
        )
    }
}

/// M3-D r5 item 25 (D4-3): no M3 request carries EE-2, EE-4's request
/// part or EE-6a. D4-T2 is unrepresentable and row 57 is unreachable here.
/// A new request, flag, admitted field, mode or format must be reviewed
/// against item 25: these closed destructures and match have no wildcard.
/// The existing J1 request-class type is used, not a manifest's digest arm.
#[deny(unreachable_patterns)]
pub(crate) fn request_excluded_form(admitted: &AdmittedRequest) -> Option<RequestExcludedClass> {
    let AdmittedRequest {
        request,
        flags,
        mode,
        format,
        steps: _,
    } = admitted;
    let RequestFlags {
        project: _,
        workspace_roots: _,
        trust_groups: _,
        trust_project_owner: _,
        allow_backup_custody: _,
    } = flags;
    let InvocationModeV1 { interactive: _ } = mode;
    let OutputFormat::Json = format;
    match request {
        AnalysisRequest::Default => None,
        AnalysisRequest::Analyze => None,
        AnalysisRequest::AnalyzeEphemeral => None,
    }
}

// ------------------------------------------------ item 5.1: the step lists

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum Requirement {
    Required,
    Optional,
}
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum Gate {
    Completed,
    Terminal,
}
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum Retry {
    None,
    IdempotentRetry,
}
/// One step's DAG fields. Its StepId is its position.
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) struct StepSpec {
    pub(crate) kind: StepKind,
    pub(crate) requirement: Requirement,
    pub(crate) depends_on: Vec<usize>,
    pub(crate) gate: Gate,
    pub(crate) retry: Retry,
}
/// Step 0's snapshot source: the live worktree.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum SnapshotSource {
    LiveWorktree,
}
/// Step 0's parameters (5.1).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) struct AnalysisParams {
    pub(crate) durability: Durability,
    pub(crate) snapshot_source: SnapshotSource,
}
/// Step 1's parameters (5.1): JSON to the caller's output handle, required.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) struct RenderParams {
    pub(crate) format: OutputFormat,
    pub(crate) required: bool,
}
/// Item 5.1: `[analysis, render]`. No `import` step: M3 selects none.
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) struct StepList {
    specs: [StepSpec; 2],
    analysis: AnalysisParams,
    render: RenderParams,
}
impl StepList {
    /// WFC `default-analyze-render-success` (and `ephemeral-result-...` for
    /// the ephemeral request), except that retry is `none` (lead decision,
    /// 5.1).
    pub(crate) fn for_request(request: AnalysisRequest) -> Self {
        Self {
            specs: [
                StepSpec {
                    kind: StepKind::Analysis,
                    requirement: Requirement::Required,
                    depends_on: Vec::new(),
                    gate: Gate::Completed,
                    retry: Retry::None,
                },
                StepSpec {
                    kind: StepKind::Render,
                    requirement: Requirement::Required,
                    depends_on: vec![0],
                    gate: Gate::Terminal,
                    retry: Retry::None,
                },
            ],
            analysis: AnalysisParams {
                durability: request.durability(),
                snapshot_source: SnapshotSource::LiveWorktree,
            },
            render: RenderParams {
                format: OutputFormat::Json,
                required: true,
            },
        }
    }
    pub(crate) fn specs(&self) -> &[StepSpec] {
        &self.specs
    }
    pub(crate) fn analysis(&self) -> AnalysisParams {
        self.analysis
    }
    pub(crate) fn render(&self) -> RenderParams {
        self.render
    }
}

/// WS section 1: at most 64 steps, and at most 8 dependencies per step
/// (`invocation-v5` `StepSpec.dependsOn`).
pub(crate) const MAX_STEPS: usize = 64;
pub(crate) const MAX_DEPENDS_ON: usize = 8;

/// A step list that breaks WS section 1's rules. The key spells the
/// workflow refusal the reference model gives it; for a host-built list it
/// is an operational key, never a public detail (row 2).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum StepListFault {
    /// No steps, or more than 64.
    StepBound,
    /// A duplicate, unknown or excess dependency.
    DependencyInvalid { step: usize },
    /// A forward or self reference.
    DependencyCycle { step: usize },
    /// A required step depending on an optional one.
    RequiredDependsOnOptional { step: usize },
    /// `terminal` on a step other than `render` or `export-delivery`.
    GateNotApplicable { step: usize },
    /// `idempotent-retry` on a kind that is never retried.
    RetryNotApplicable { step: usize },
}
impl StepListFault {
    /// The operational key: the workflow refusal's spelling, then the step.
    pub(crate) fn key(self) -> String {
        let (code, step) = match self {
            Self::StepBound => (Detail::WorkflowStepBoundExceeded, None),
            Self::DependencyInvalid { step } => (Detail::WorkflowDependencyInvalid, Some(step)),
            Self::DependencyCycle { step } => (Detail::WorkflowDependencyCycle, Some(step)),
            Self::RequiredDependsOnOptional { step } => {
                (Detail::WorkflowRequiredDependsOnOptional, Some(step))
            }
            Self::GateNotApplicable { step } => (Detail::WorkflowGateNotApplicable, Some(step)),
            Self::RetryNotApplicable { step } => (Detail::WorkflowRetryBudgetExhausted, Some(step)),
        };
        match step {
            Some(step) => format!("{code}:{step}"),
            None => code.to_string(),
        }
    }
    /// Item 10's row 2 for a host-built list.
    pub(crate) fn observation(self) -> Observation {
        Observation::HostSpecInvalid { key: self.key() }
    }
}

/// WS section 1's step-list rules, in the reference model's order.
pub(crate) fn check_step_list(steps: &[StepSpec]) -> Result<(), StepListFault> {
    if steps.is_empty() || steps.len() > MAX_STEPS {
        return Err(StepListFault::StepBound);
    }
    for (step, spec) in steps.iter().enumerate() {
        if spec.depends_on.len() > MAX_DEPENDS_ON {
            return Err(StepListFault::DependencyInvalid { step });
        }
        for (at, dependency) in spec.depends_on.iter().enumerate() {
            if spec.depends_on[..at].contains(dependency) || *dependency >= steps.len() {
                return Err(StepListFault::DependencyInvalid { step });
            }
            if *dependency >= step {
                return Err(StepListFault::DependencyCycle { step });
            }
            if spec.requirement == Requirement::Required
                && steps[*dependency].requirement == Requirement::Optional
            {
                return Err(StepListFault::RequiredDependsOnOptional { step });
            }
        }
        if spec.gate == Gate::Terminal
            && !matches!(spec.kind, StepKind::Render | StepKind::ExportDelivery)
        {
            return Err(StepListFault::GateNotApplicable { step });
        }
        if spec.retry == Retry::IdempotentRetry && !retryable(spec.kind) {
            return Err(StepListFault::RetryNotApplicable { step });
        }
    }
    Ok(())
}
/// WS section 1: the kinds `idempotent-retry` is lawful for.
fn retryable(kind: StepKind) -> bool {
    match kind {
        StepKind::Analysis
        | StepKind::Verify
        | StepKind::Query
        | StepKind::Render
        | StepKind::ExportDelivery
        | StepKind::Doctor => true,
        StepKind::Comparison
        | StepKind::Import
        | StepKind::RepairPreview
        | StepKind::RepairApply
        | StepKind::TestExecution
        | StepKind::Mutation
        | StepKind::NativePreparation => false,
    }
}

// ------------------------------------------ item 5.2: the analysis joins

/// The joins of step 0. Each is a token that only consuming the previous
/// join's token produces, so a join is never re-entered or skipped, and a
/// refusal at any join ends step 0. The durable chain is J-alpha to J-iota;
/// the ephemeral one has no J-gamma (handoff and session) and no J-iota
/// (finalization).
pub(crate) struct Join<P, J> {
    _at: PhantomData<fn() -> (P, J)>,
}
/// The durable path.
pub(crate) enum Durable {}
/// The ephemeral path.
pub(crate) enum Ephemeral {}
/// J-alpha: the request to the durable entry (R0-R3) or the ephemeral entry.
pub(crate) enum Alpha {}
/// J-beta: fence to project admission, configuration, pack, S3.1 and
/// component admission (R4-R10a; ER10a).
pub(crate) enum Beta {}
/// J-gamma: handoff to the open session (R11-R12). Durable only.
pub(crate) enum Gamma {}
/// J-delta: the capture session to the sealed `snapshot2`.
pub(crate) enum Delta {}
/// J-epsilon: the Plan.
pub(crate) enum Epsilon {}
/// J-zeta: the provider stages.
pub(crate) enum Zeta {}
/// J-eta: fact admission, then the full `admit_enumeration`.
pub(crate) enum Eta {}
/// J-theta: evaluation through `derive_evaluation`.
pub(crate) enum Theta {}
/// J-iota: replay, `prepare_commit`, `publish` and `finish`. Durable only.
pub(crate) enum Iota {}

/// Item 5.2's join labels, for records.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum JoinName {
    Alpha,
    Beta,
    Gamma,
    Delta,
    Epsilon,
    Zeta,
    Eta,
    Theta,
    Iota,
}
/// The marker's label.
pub(crate) trait Named {
    const NAME: JoinName;
}
impl Named for Alpha {
    const NAME: JoinName = JoinName::Alpha;
}
impl Named for Beta {
    const NAME: JoinName = JoinName::Beta;
}
impl Named for Gamma {
    const NAME: JoinName = JoinName::Gamma;
}
impl Named for Delta {
    const NAME: JoinName = JoinName::Delta;
}
impl Named for Epsilon {
    const NAME: JoinName = JoinName::Epsilon;
}
impl Named for Zeta {
    const NAME: JoinName = JoinName::Zeta;
}
impl Named for Eta {
    const NAME: JoinName = JoinName::Eta;
}
impl Named for Theta {
    const NAME: JoinName = JoinName::Theta;
}
impl Named for Iota {
    const NAME: JoinName = JoinName::Iota;
}

fn next<P, J>() -> Join<P, J> {
    Join { _at: PhantomData }
}
impl Join<Durable, Alpha> {
    /// The durable chain's first join.
    pub(crate) fn durable() -> Self {
        next()
    }
}
impl Join<Ephemeral, Alpha> {
    /// The ephemeral chain's first join.
    pub(crate) fn ephemeral() -> Self {
        next()
    }
}
impl<P, J: Named> Join<P, J> {
    /// The join this token stands at.
    pub(crate) fn name(&self) -> JoinName {
        J::NAME
    }
    /// A refusal at this join ends step 0 on its row (5.2).
    pub(crate) fn refused(self, refusal: Observation) -> AnalysisEnd {
        AnalysisEnd::Ended(refusal)
    }
    /// The deciding signal's cooperative stop at this join (phase A) ends
    /// step 0 with no outcome of its own.
    pub(crate) fn cancelled(self, by: Deciding) -> AnalysisEnd {
        AnalysisEnd::Cancelled(by)
    }
}
impl<P> Join<P, Alpha> {
    pub(crate) fn entered(self) -> Join<P, Beta> {
        next()
    }
}
impl Join<Durable, Beta> {
    pub(crate) fn admitted(self) -> Join<Durable, Gamma> {
        next()
    }
}
impl Join<Ephemeral, Beta> {
    /// ER10a has returned: the ephemeral attempt starts.
    pub(crate) fn admitted(self) -> Join<Ephemeral, Delta> {
        next()
    }
}
impl Join<Durable, Gamma> {
    /// R12: the session is open; its ExecutionId exists.
    pub(crate) fn opened(self) -> Join<Durable, Delta> {
        next()
    }
}
impl<P> Join<P, Delta> {
    pub(crate) fn captured(self) -> Join<P, Epsilon> {
        next()
    }
}
impl<P> Join<P, Epsilon> {
    pub(crate) fn planned(self) -> Join<P, Zeta> {
        next()
    }
}
impl<P> Join<P, Zeta> {
    pub(crate) fn provided(self) -> Join<P, Eta> {
        next()
    }
}
impl<P> Join<P, Eta> {
    pub(crate) fn admitted_facts(self) -> Join<P, Theta> {
        next()
    }
}
impl Join<Durable, Theta> {
    pub(crate) fn evaluated(self) -> Join<Durable, Iota> {
        next()
    }
}
impl Join<Ephemeral, Theta> {
    /// The ephemeral attempt ends when its evaluation result is held.
    pub(crate) fn evaluated(self, verdict: EphemeralVerdict) -> AnalysisEnd {
        AnalysisEnd::Ended(Observation::Analysis(AnalysisOutcome::Ephemeral(verdict)))
    }
}
impl Join<Durable, Iota> {
    /// The durable attempt ends when `finish` has returned, on the outcome
    /// X3d returned: a committed verdict, `LatchedAfterAdmission`,
    /// `CommitUndetermined`, or a refusal on its row.
    pub(crate) fn finished(self, outcome: Observation) -> AnalysisEnd {
        AnalysisEnd::Ended(outcome)
    }
}

/// How step 0 ended (5.3): on an observation's row, or cancelled before
/// any outcome by the deciding signal.
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) enum AnalysisEnd {
    Ended(Observation),
    Cancelled(Deciding),
}

// ------------------------------------ items 8.2 and 8.3: cancellation

/// SOP2's `CancelPhase` (A to E, OPP section 5.5) with S18's `O`.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum CancelPhase {
    A,
    B,
    C,
    D,
    O,
    E,
}

/// The operation's state when the host observes a signal (8.2). An
/// ephemeral request is `BeforeAttemptAdmission` up to its output decision
/// point, then `FinalOutput`, then `Settled`; it has no commit.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum OperationPoint {
    /// From R0 until `prepare_commit` returns with the attempt row
    /// committed: the entry, project admission, the analysis and replay.
    BeforeAttemptAdmission,
    /// From the committed attempt row until FinalGate admission.
    AttemptAdmitted,
    /// From FinalGate admission until `publish`'s sample.
    FinalGateAdmitted,
    /// LD-r5-1: `publish` returned `Refused`, `CommitUndetermined` or a
    /// latched `Committed`, before the output decision point. `admitted`
    /// is the window close's own sample: state 1 or 3.
    PublishReturned { admitted: bool },
    /// `publish` returned `Committed` unlatched, before the output
    /// decision point; it includes `finish` and step 1's projection.
    CommittedUnlatched,
    /// From the output decision point until the required output returns.
    FinalOutput,
    /// After the settlement point.
    Settled,
}
impl OperationPoint {
    /// 8.2's label. After a `publish` return that does not enter D, the
    /// last phase reached: C if FinalGate admission had succeeded, B
    /// otherwise (LD-r5-1).
    pub(crate) fn phase(self) -> CancelPhase {
        match self {
            Self::BeforeAttemptAdmission => CancelPhase::A,
            Self::AttemptAdmitted => CancelPhase::B,
            Self::FinalGateAdmitted => CancelPhase::C,
            Self::PublishReturned { admitted: true } => CancelPhase::C,
            Self::PublishReturned { admitted: false } => CancelPhase::B,
            Self::CommittedUnlatched => CancelPhase::D,
            Self::FinalOutput => CancelPhase::O,
            Self::Settled => CancelPhase::E,
        }
    }
}

/// What 8.2 prescribes for one observed signal.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum SignalEffect {
    /// A: cooperative. No new join starts, providers get `cancel`, and an
    /// open session ends through `refused()` and `finish`.
    Cooperate,
    /// B and C: the cancellation latch is attempted. After a `publish`
    /// return the window is closed and it changes nothing (8.1).
    Latch,
    /// D: no latch; `finish` runs to completion and step 1 is cancelled at
    /// the output decision point.
    CancelAtDecisionPoint,
    /// A later signal before the output decision point: the forced second
    /// stage (8.5).
    Force,
    /// O: deferred. It never changes the decided envelope.
    Defer,
    /// E: recorded only; nothing is reclassified.
    Record,
}

/// One `host.signal.received` record (SOP2:871): the signal, its ordinal
/// and its arrival phase, classified in memory.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) struct SignalRecord {
    pub(crate) signal: Signal,
    pub(crate) ordinal: u64,
    pub(crate) phase: CancelPhase,
}
/// The first signal observed before the output decision point, which
/// decides the termination (8.3).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) struct Deciding {
    pub(crate) signal: Signal,
    pub(crate) phase: CancelPhase,
}

/// The host cancellation source, in memory: it classifies each observed
/// signal by the operation's point and keeps the deciding one. It keeps no
/// list; each record is handed to the caller to record.
#[derive(Debug, Default)]
pub(crate) struct CancellationSource {
    observed: u64,
    deciding: Option<Deciding>,
}
impl CancellationSource {
    pub(crate) fn new() -> Self {
        Self::default()
    }
    /// Classify one signal observed at `point`.
    pub(crate) fn observe(
        &mut self,
        signal: Signal,
        point: OperationPoint,
    ) -> (SignalRecord, SignalEffect) {
        self.observed = self.observed.saturating_add(1);
        let phase = point.phase();
        let record = SignalRecord {
            signal,
            ordinal: self.observed,
            phase,
        };
        let effect = match phase {
            CancelPhase::O => SignalEffect::Defer,
            CancelPhase::E => SignalEffect::Record,
            CancelPhase::A | CancelPhase::B | CancelPhase::C | CancelPhase::D
                if self.deciding.is_some() =>
            {
                SignalEffect::Force
            }
            CancelPhase::A => SignalEffect::Cooperate,
            CancelPhase::B | CancelPhase::C => SignalEffect::Latch,
            CancelPhase::D => SignalEffect::CancelAtDecisionPoint,
        };
        if matches!(
            effect,
            SignalEffect::Cooperate | SignalEffect::Latch | SignalEffect::CancelAtDecisionPoint
        ) {
            self.deciding = Some(Deciding { signal, phase });
        }
        (record, effect)
    }
    /// The deciding signal, if one was observed before the decision point.
    pub(crate) fn deciding(&self) -> Option<Deciding> {
        self.deciding
    }
}

// ------------------------------------------- items 5.3 and 8.4: settlement

/// An uncertain step 0's disclosure (8.2 row O; S18): its ExecutionId and
/// namespace stay disclosed whichever termination is primary, and are never
/// the render attempt's or a Run's.
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) struct Uncertain {
    pub(crate) execution_id: String,
    pub(crate) namespace: String,
}

/// Step 1 at the output decision point.
#[derive(Debug, Clone, PartialEq, Eq)]
enum Step1 {
    /// Not terminal: it completes or fails when the required output
    /// returns.
    Rendering,
    /// Terminal at the decision point: cancelled for a termination output,
    /// or failed. Its envelope is still rendered and written in O.
    Terminal(StepResult),
}

/// The output decision point (8.4): the one check after step 0 is
/// terminal and step 1's projection is done. It fixes the envelope the
/// final output section renders. It does not settle the invocation.
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) struct Decision {
    step0: StepResult,
    step1: Step1,
    envelope: Termination,
    uncertain: Option<Uncertain>,
    committed_run: Option<String>,
    replacement: bool,
}
/// What step 0's end says about the commit X3d returned: 8.3's precedence
/// and the committed evidence of a renderer failure in O are matched on it,
/// never on the gate's state. Exhaustive with no wildcard arm, so a new
/// observation must say which it is.
#[derive(Debug, Clone, PartialEq, Eq)]
enum CommitEvidence {
    /// Rule 1: any `CommitUndetermined`. Row 38's disclosure where the
    /// attempt carries it; security's bare row carries none.
    Undetermined(Option<Uncertain>),
    /// Rule 2: a `PublishedCommit` latched after admission.
    Latched { run_id: String },
    /// A `PublishedCommit` not latched (rule 3 when the signal is in D).
    Committed { run_id: String },
    /// No commit outcome: a refusal, a fault, an ephemeral result.
    None,
}
fn commit_evidence(observation: &Observation) -> CommitEvidence {
    use Observation as O;
    match observation {
        O::CommitUndetermined {
            execution_id,
            namespace,
        } => CommitEvidence::Undetermined(Some(Uncertain {
            execution_id: execution_id.clone(),
            namespace: namespace.clone(),
        })),
        O::Installation(row) => {
            if *row == Row::CommitUndetermined {
                CommitEvidence::Undetermined(None)
            } else {
                CommitEvidence::None
            }
        }
        O::LatchedAfterAdmission { run_id } => CommitEvidence::Latched {
            run_id: run_id.clone(),
        },
        O::Analysis(AnalysisOutcome::Committed { run_id, .. }) => CommitEvidence::Committed {
            run_id: run_id.clone(),
        },
        O::Analysis(AnalysisOutcome::Ephemeral(_))
        | O::HostSpecInvalid { .. }
        | O::CarrierCustody { .. }
        | O::ConfigurationInvalid { .. }
        | O::HostInvariant { .. }
        | O::PolicySelection(_)
        | O::WorkspaceUnitLimit { .. }
        | O::WorkBudgetExhausted
        | O::ScopeLimit { .. }
        | O::HostIo
        | O::ExplicitRootWithoutMarker { .. }
        | O::ExplicitPathInvalid { .. }
        | O::DiscoveryInventoryMismatch
        | O::Stale(_)
        | O::Native(_)
        | O::ClosureBytesCorrupt
        | O::ClosureUnspawnable
        | O::ProviderProtocol { .. }
        | O::OutputBoundExceeded
        | O::Replay(_)
        | O::ExistingAttempt { .. }
        | O::CarrierCapacityExhausted { .. }
        | O::RequiredDeliveryFailed { .. }
        | O::Interrupted { .. }
        | O::HostPanicBeforeAdmission
        | O::EphemeralCannotSupplyAuthority
        | O::NativeContextRefused { .. }
        | O::PrepareBoundExceeded
        | O::AmbientCargoConfig
        | O::ExcludedManifests { .. }
        | O::ExcludedRequest { .. }
        | O::TypescriptConfigUnresolved(_) => CommitEvidence::None,
    }
}
impl CommitEvidence {
    fn uncertain(&self) -> Option<Uncertain> {
        match self {
            Self::Undetermined(disclosure) => disclosure.clone(),
            Self::Latched { .. } | Self::Committed { .. } | Self::None => None,
        }
    }
    /// The committed evidence: a `PublishedCommit`'s runId, latched or not.
    fn committed_run(&self) -> Option<String> {
        match self {
            Self::Latched { run_id } | Self::Committed { run_id } => Some(run_id.clone()),
            Self::Undetermined(_) | Self::None => None,
        }
    }
}

impl Decision {
    /// 8.3's rules, matched on the outcome X3d returned first, never on the
    /// gate's state:
    /// 1. any `CommitUndetermined` takes the durability row (row 38);
    /// 2. a latched `Committed` takes X7's F39 row (row 42);
    /// 3. an unlatched `Committed` with the signal observed in D is
    ///    `interrupted` with that runId (row 47);
    /// 4. otherwise a signal gives `interrupted` with no runId (row 46).
    ///
    /// With a signal, step 1 is cancelled for a termination output (WS:226
    /// as S21 states it). With none, step 1 renders the aggregate.
    pub(crate) fn decide(end: AnalysisEnd, deciding: Option<Deciding>) -> Self {
        let (observation, deciding) = match (end, deciding) {
            (AnalysisEnd::Ended(observation), None) => {
                return Self::unsignalled(observation);
            }
            (AnalysisEnd::Ended(observation), Some(deciding)) => (Some(observation), deciding),
            // The source's deciding signal is the first; a stop it caused
            // names the same one.
            (AnalysisEnd::Cancelled(by), deciding) => (None, deciding.unwrap_or(by)),
        };
        let evidence = observation
            .as_ref()
            .map_or(CommitEvidence::None, commit_evidence);
        let envelope = match (&observation, &evidence) {
            // Rules 1 and 2: the commit outcome governs (S21).
            (
                Some(observation),
                CommitEvidence::Undetermined(_) | CommitEvidence::Latched { .. },
            ) => project(observation),
            // Rule 3.
            (Some(_), CommitEvidence::Committed { run_id }) if deciding.phase == CancelPhase::D => {
                Termination::interrupted(deciding.signal, Some(run_id.clone()))
            }
            // Rule 4: otherwise.
            (Some(_), CommitEvidence::Committed { .. } | CommitEvidence::None)
            | (None, CommitEvidence::Undetermined(_))
            | (None, CommitEvidence::Latched { .. })
            | (None, CommitEvidence::Committed { .. })
            | (None, CommitEvidence::None) => Termination::interrupted(deciding.signal, None),
        };
        let step0 = StepResult::ended(match &observation {
            Some(observation) => project(observation),
            None => Termination::interrupted(deciding.signal, None),
        });
        Self {
            step0,
            step1: Step1::Terminal(StepResult::ended(Termination::interrupted(
                deciding.signal,
                None,
            ))),
            envelope,
            uncertain: evidence.uncertain(),
            committed_run: evidence.committed_run(),
            replacement: false,
        }
    }
    /// No signal before the decision point: step 1 renders the aggregate of
    /// step 0 and its own coming completion.
    fn unsignalled(observation: Observation) -> Self {
        let evidence = commit_evidence(&observation);
        let step0 = StepResult::ended(project(&observation));
        let envelope = aggregate(&[
            (Requirement::Required, &step0),
            (Requirement::Required, &StepResult::completed()),
        ]);
        Self {
            step0,
            step1: Step1::Rendering,
            envelope,
            uncertain: evidence.uncertain(),
            committed_run: evidence.committed_run(),
            replacement: false,
        }
    }
    /// The envelope the final output section renders.
    pub(crate) fn envelope(&self) -> &Termination {
        &self.envelope
    }
    pub(crate) fn step0(&self) -> &StepResult {
        &self.step0
    }
    /// Step 1's result when it is terminal at the decision point.
    pub(crate) fn step1_terminal(&self) -> Option<&StepResult> {
        match &self.step1 {
            Step1::Rendering => None,
            Step1::Terminal(step) => Some(step),
        }
    }
    pub(crate) fn uncertain(&self) -> Option<&Uncertain> {
        self.uncertain.as_ref()
    }
    /// A renderer failure in O before any byte of the decided envelope:
    /// step 1 fails, even where it was cancelled for a termination output,
    /// on the route the committed evidence chooses (row 43 with the runId,
    /// or row 44 without one), and the aggregate over both required steps
    /// replaces the envelope. A failure envelope that cannot itself be
    /// rendered ends the invocation undelivered.
    pub(crate) fn renderer_failed(self) -> Result<Self, Undelivered> {
        if self.replacement {
            return Err(Undelivered);
        }
        let failed = StepResult::ended(project(&Observation::RequiredDeliveryFailed {
            committed_run: self.committed_run.clone(),
        }));
        let envelope = aggregate(&[
            (Requirement::Required, &self.step0),
            (Requirement::Required, &failed),
        ]);
        Ok(Self {
            step1: Step1::Terminal(failed),
            envelope,
            replacement: true,
            ..self
        })
    }
    /// A failed write or flush of the envelope, whether or not a byte was
    /// written: exit 4, no replacement envelope (S18).
    pub(crate) fn output_failed(self) -> Undelivered {
        Undelivered
    }
    /// The required output returned: the settlement point (5.3). A step 1
    /// still rendering completes here.
    pub(crate) fn output_returned(self) -> Settled {
        let step1 = match self.step1 {
            Step1::Rendering => StepResult::completed(),
            Step1::Terminal(step) => step,
        };
        Settled {
            termination: self.envelope,
            uncertain: self.uncertain,
            steps: [self.step0, step1],
        }
    }
}

/// The invocation ended with no envelope delivered: exit 4 and one coded
/// standard-error line, which the output wiring writes.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) struct Undelivered;
impl Undelivered {
    pub(crate) fn exit(self) -> u8 {
        4
    }
}

/// The settled invocation. A signal observed after this is recorded only
/// (phase E); the settled class stands (WS:227-228, WS:1393).
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) struct Settled {
    pub(crate) termination: Termination,
    pub(crate) uncertain: Option<Uncertain>,
    pub(crate) steps: [StepResult; 2],
}
impl Settled {
    pub(crate) fn exit(&self) -> u8 {
        self.termination.exit()
    }
}

#[cfg(test)]
mod tests {
    include!("invocation_tests.rs");
}
