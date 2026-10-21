//! M3-D r5 items 20 to 22, unit D3a-3: the supervision's record facts and
//! its outcome route.
//!
//! **Record facts (LD-D3A3-1).** Each provider and supervision event the
//! registry holds (M3-D r5 item 21; `opensip_operability`'s
//! `provider.*`, `supervision.*` and `tool.*` events) needs minted values the
//! supervision cannot lawfully make: the attempt scope, the universe key's
//! digest (K9) and the process id (K11). So the supervision hands its caller
//! one typed, mint-free [`RecordFact`] per event, carrying every other field
//! as a host-held value, and the caller (J2b), which holds the minted scope,
//! universe and pid mint, builds the registry event and emits it. A fact
//! carries no stderr, `fault` or `refusal` text, no nonce, no environment
//! value and no path (item 21's "never recorded"): only counts, lengths,
//! durations and closed codes.
//!
//! **The route (LD-D3A-11).** Item 22 assigns no code: each settlement names
//! one row of its table, an [`OwnerRoute`], and J2 maps the route to J1's
//! codes. `userInterrupted` takes the interrupted row first (:712), and a
//! host-observed cause never takes the provider-protocol route (:731).
use super::{
    BoundedWait as Wait, ByteBound, Cause, ExitClass as Exit, LimitKind as Limit, LivenessMiss,
    PreSpawnRefusal, RunError, ScratchRetained, Settlement, SupervisorError,
};
use crate::control_protocol::RefusalFamily as Family;
use opensip_operability::{
    BoundedWait, ControlCancelReason, ExitClass, FaultSource, LimitKind, LimitUnit,
    LivenessMiss as Miss, ProtocolMajor, RefusalFamily, ScratchRetainedReason, TeardownCause,
};
use opensip_operability::{ChildSignal, ProviderReason, ProviderState, StageKind, StageTerminal};
use std::time::Duration;

/// One registry event's host-held values (LD-D3A3-1). The caller adds the
/// minted `role`, `universe` and `pid` and emits the named event.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum RecordFact {
    /// `provider.process.spawned`: the raw pid, for the caller's K11 mint.
    ProcessSpawned {
        protocol: ProtocolMajor,
        raw_pid: u32,
    },
    /// `provider.process.ready`: spawn to the context's verification, and
    /// the snapshot transfer sub-span (M3-L r1:400).
    ProcessReady { start: Duration, transfer: Duration },
    /// `provider.stderr.reduced`: item 17's count, never a byte (K7).
    StderrReduced { bytes: u64, truncated: bool },
    /// `provider.fault.reduced`: a provider-spoken control `fault` or
    /// `refusal`, its detail reduced to its length.
    FaultReduced {
        source: FaultSource,
        refusal_family: Option<RefusalFamily>,
        detail_bytes: u64,
    },
    /// `provider.resources.reported`: `resourceReport`'s asserted values.
    ResourcesReported {
        resident: u64,
        cpu_nanos: u64,
        handles: u64,
    },
    /// `supervision.liveness.missed`: the configured window, and its
    /// reduced provenance (D3A1-R2-NBO-1).
    LivenessMissed {
        window: Duration,
        miss: Miss,
        refusal_family: Option<RefusalFamily>,
    },
    /// `supervision.limit.breached`: the value observed, in `unit`.
    LimitBreached {
        limit: LimitKind,
        observed: u64,
        unit: LimitUnit,
    },
    /// `supervision.sample.incomplete` (D3A2-R1-NBO-1): a sample the host
    /// could not complete, for a reason other than a member exiting.
    SampleIncomplete {
        listed: u64,
        unsampled: u64,
        listing_failed: bool,
    },
    /// A fully written control cancellation; `inband` says whether the
    /// provider Cancel completed before it. Ordinary fault T-1 is false.
    CancelSent {
        inband: bool,
        control_reason: ControlCancelReason,
    },
    CancelForced {
        trigger: opensip_operability::ForceTrigger,
        grace: Duration,
    },
    /// `supervision.wait.expired`: the wait and its configured bound.
    WaitExpired { wait: BoundedWait, limit: Duration },
    /// `supervision.teardown.started`.
    TeardownStarted { cause: TeardownCause },
    /// `supervision.scratch.retained`: the reason, and the errno exactly
    /// for `io-failure`.
    ScratchRetained {
        reason: ScratchRetainedReason,
        errno: Option<i32>,
    },
    /// `supervision.child.settled` (item 21's `supervision.settled`, in
    /// S-OP-2 item 2's three-segment grammar; LD-D3A3-11).
    Settled {
        cause: TeardownCause,
        admissible: bool,
        user_interrupted: bool,
    },
    /// `tool.process.spawned`.
    ToolSpawned { raw_pid: u32 },
    /// `tool.process.reaped`: macOS reports `ru_maxrss` in bytes, so the
    /// native value is the byte value (`rss_unit` `bytes`).
    ToolReaped {
        raw_pid: u32,
        exit: ExitClass,
        /// D3a-4: S-OP-2c's `ChildSignal`, only for `signaled` with a member.
        signal: Option<ChildSignal>,
        max_rss_bytes: u64,
        cpu: Duration,
    },
    /// D3a-4 (S-OP-2c item 23a): `provider.stage.changed`, the phase after a
    /// transition.
    StageChanged {
        stage: StageKind,
        state: ProviderState,
    },
    /// `provider.stage.terminal`: the terminal, its reason exactly for
    /// `unavailable`, the admitted frame counts and M3-L's analysis span.
    StageTerminal {
        stage: StageKind,
        terminal: StageTerminal,
        reason: Option<ProviderReason>,
        fact_frames: u64,
        coverage_frames: u64,
        analysis: Duration,
    },
    /// `provider.process.reaped`: the raw pid for the caller's mint, the
    /// exit, its signal member, the rusage and M3-L's teardown span.
    ProcessReaped {
        raw_pid: u32,
        exit: ExitClass,
        signal: Option<ChildSignal>,
        max_rss_bytes: u64,
        cpu: Duration,
        teardown: Duration,
    },
    /// `supervision.progress.absent`: measured since the last admitted
    /// transition.
    ProgressAbsent { stage: StageKind, since: Duration },
    /// r2 (Codex D3A3-R1-RF-1): a tool's own supervision records, each a
    /// Project-only `tool.*` event; a tool has no Plan, Execution, provider
    /// role or universe, so it never produces a `supervision.*` fact.
    /// `tool.limit.breached`.
    ToolLimitBreached {
        limit: LimitKind,
        observed: u64,
        unit: LimitUnit,
    },
    /// `tool.sample.incomplete`.
    ToolSampleIncomplete {
        listed: u64,
        unsampled: u64,
        listing_failed: bool,
    },
    /// `tool.wait.expired`.
    ToolWaitExpired { wait: BoundedWait, limit: Duration },
    /// `tool.teardown.started`.
    ToolTeardownStarted { cause: TeardownCause },
    /// `tool.scratch.retained`.
    ToolScratchRetained {
        reason: ScratchRetainedReason,
        errno: Option<i32>,
    },
    /// `tool.child.settled`.
    ToolSettled {
        cause: TeardownCause,
        user_interrupted: bool,
    },
    /// `supervision.tree.swept` (D3b-1; D3b plan r3, LD-D3B-5): `killed` is
    /// the count of distinct pids whose identity-checked kill was `Sent`,
    /// never a group delivery or a death; `unattributed` is Linux's notion,
    /// 0 on macOS; `platform_limited` is true on macOS. No orphan pid.
    TreeSwept {
        killed: u64,
        unattributed: u64,
        platform_limited: bool,
    },
    /// `tool.tree.swept` (D3b-1; LD-D3B-9).
    ToolTreeSwept {
        killed: u64,
        unattributed: u64,
        platform_limited: bool,
    },
}

/// The identities a fact's event requires (S-OP-2 item 23; M3-D r5 item 21,
/// :692): a provider's Project, Plan and Execution, or a tool's Project.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Requires {
    ProjectPlanExecution,
    Project,
}

impl RecordFact {
    /// The registry event this fact feeds.
    pub fn event(&self) -> &'static str {
        use opensip_operability::Event;
        match self {
            Self::ProcessSpawned { .. } => opensip_operability::ProviderProcessSpawned::NAME,
            Self::ProcessReady { .. } => opensip_operability::ProviderProcessReady::NAME,
            Self::StderrReduced { .. } => opensip_operability::ProviderStderrReduced::NAME,
            Self::FaultReduced { .. } => opensip_operability::ProviderFaultReduced::NAME,
            Self::ResourcesReported { .. } => opensip_operability::ProviderResourcesReported::NAME,
            Self::LivenessMissed { .. } => opensip_operability::SupervisionLivenessMissed::NAME,
            Self::LimitBreached { .. } => opensip_operability::SupervisionLimitBreached::NAME,
            Self::SampleIncomplete { .. } => opensip_operability::SupervisionSampleIncomplete::NAME,
            Self::CancelSent { .. } => opensip_operability::SupervisionCancelSent::NAME,
            Self::CancelForced { .. } => opensip_operability::SupervisionCancelForced::NAME,
            Self::WaitExpired { .. } => opensip_operability::SupervisionWaitExpired::NAME,
            Self::TeardownStarted { .. } => opensip_operability::SupervisionTeardownStarted::NAME,
            Self::ScratchRetained { .. } => opensip_operability::SupervisionScratchRetained::NAME,
            Self::Settled { .. } => opensip_operability::SupervisionSettled::NAME,
            Self::ToolSpawned { .. } => opensip_operability::ToolProcessSpawned::NAME,
            Self::ToolReaped { .. } => opensip_operability::ToolProcessReaped::NAME,
            Self::ToolLimitBreached { .. } => opensip_operability::ToolLimitBreached::NAME,
            Self::ToolSampleIncomplete { .. } => opensip_operability::ToolSampleIncomplete::NAME,
            Self::ToolWaitExpired { .. } => opensip_operability::ToolWaitExpired::NAME,
            Self::ToolTeardownStarted { .. } => opensip_operability::ToolTeardownStarted::NAME,
            Self::ToolScratchRetained { .. } => opensip_operability::ToolScratchRetained::NAME,
            Self::ToolSettled { .. } => opensip_operability::ToolChildSettled::NAME,
            Self::StageChanged { .. } => opensip_operability::ProviderStageChanged::NAME,
            Self::StageTerminal { .. } => opensip_operability::ProviderStageTerminal::NAME,
            Self::ProcessReaped { .. } => opensip_operability::ProviderProcessReaped::NAME,
            Self::ProgressAbsent { .. } => opensip_operability::SupervisionProgressAbsent::NAME,
            Self::TreeSwept { .. } => opensip_operability::SupervisionTreeSwept::NAME,
            Self::ToolTreeSwept { .. } => opensip_operability::ToolTreeSwept::NAME,
        }
    }
    /// The event's field keys this fact supplies; the caller adds the
    /// minted ones (`role`, `universe`, `pid`). `inband` is carried by the
    /// cancel fact, and `rss_unit` is `bytes` on macOS.
    pub fn supplies(&self) -> &'static [&'static str] {
        match self {
            Self::ProcessSpawned { .. } => &["protocol"],
            Self::ProcessReady { .. } => &["start", "transfer"],
            Self::StderrReduced { .. } => &["stderr"],
            Self::FaultReduced { .. } => &[
                "source",
                "fault_kind",
                "refusal_family",
                "detail",
                "detail_code",
            ],
            Self::ResourcesReported { .. } => &["resident", "cpu", "handles"],
            Self::LivenessMissed { .. } => &["window", "miss", "refusal_family"],
            Self::LimitBreached { .. } => &["limit", "observed", "unit"],
            Self::SampleIncomplete { .. } => &["listed", "unsampled", "listing_failed"],
            Self::CancelSent { .. } => &["inband", "control_reason"],
            Self::CancelForced { .. } => &["trigger", "grace"],
            Self::WaitExpired { .. } => &["wait", "limit"],
            Self::TeardownStarted { .. } => &["cause"],
            Self::ScratchRetained { .. } => &["reason", "errno"],
            Self::Settled { .. } => &["cause", "admissible", "user_interrupted"],
            Self::ToolSpawned { .. } => &[],
            Self::ToolReaped { .. } => &[
                "exit_class",
                "signal",
                "max_rss_native",
                "rss_unit",
                "max_rss_bytes",
                "cpu",
            ],
            Self::ToolLimitBreached { .. } => &["limit", "observed", "unit"],
            Self::ToolSampleIncomplete { .. } => &["listed", "unsampled", "listing_failed"],
            Self::ToolWaitExpired { .. } => &["wait", "limit"],
            Self::ToolTeardownStarted { .. } => &["cause"],
            Self::ToolScratchRetained { .. } => &["reason", "errno"],
            Self::ToolSettled { .. } => &["cause", "user_interrupted"],
            Self::StageChanged { .. } => &["stage", "state"],
            Self::StageTerminal { .. } => &[
                "stage",
                "terminal",
                "reason",
                "fact_frames",
                "coverage_frames",
                "analysis",
            ],
            Self::ProcessReaped { .. } => &[
                "exit_class",
                "signal",
                "max_rss_native",
                "rss_unit",
                "max_rss_bytes",
                "cpu",
                "teardown",
            ],
            Self::ProgressAbsent { .. } => &["stage", "since"],
            Self::TreeSwept { .. } | Self::ToolTreeSwept { .. } => {
                &["killed", "unattributed", "platform_limited"]
            }
        }
    }
    /// The identities its event requires: J2b emits it on that scope only.
    pub fn requires(&self) -> Requires {
        match self {
            Self::ToolSpawned { .. }
            | Self::ToolReaped { .. }
            | Self::ToolLimitBreached { .. }
            | Self::ToolSampleIncomplete { .. }
            | Self::ToolWaitExpired { .. }
            | Self::ToolTeardownStarted { .. }
            | Self::ToolScratchRetained { .. }
            | Self::ToolSettled { .. }
            | Self::ToolTreeSwept { .. } => Requires::Project,
            _ => Requires::ProjectPlanExecution,
        }
    }
    /// A tool's record of a supervision fact (D3A3-R1-RF-1): the class-neutral
    /// supervision facts as their Project-only `tool.*` events. A provider
    /// fact (spawn, readiness, stderr, faults, resources, liveness, cancel)
    /// has no tool counterpart, because a tool has no protocol or control
    /// plane, so none is recorded for a tool.
    pub fn for_tool(self) -> Option<Self> {
        match self {
            Self::ToolSpawned { .. } | Self::ToolReaped { .. } | Self::ToolTreeSwept { .. } => {
                Some(self)
            }
            Self::TreeSwept {
                killed,
                unattributed,
                platform_limited,
            } => Some(Self::ToolTreeSwept {
                killed,
                unattributed,
                platform_limited,
            }),
            Self::LimitBreached {
                limit,
                observed,
                unit,
            } => Some(Self::ToolLimitBreached {
                limit,
                observed,
                unit,
            }),
            Self::SampleIncomplete {
                listed,
                unsampled,
                listing_failed,
            } => Some(Self::ToolSampleIncomplete {
                listed,
                unsampled,
                listing_failed,
            }),
            Self::WaitExpired { wait, limit } => Some(Self::ToolWaitExpired { wait, limit }),
            Self::TeardownStarted { cause } => Some(Self::ToolTeardownStarted { cause }),
            Self::ScratchRetained { reason, errno } => {
                Some(Self::ToolScratchRetained { reason, errno })
            }
            Self::Settled {
                cause,
                user_interrupted,
                ..
            } => Some(Self::ToolSettled {
                cause,
                user_interrupted,
            }),
            _ => None,
        }
    }
}

// ------------------------------------------------------------------ the tables, by member

/// Item 12's cause as the registry's `TeardownCause` (its family and kind
/// are other records' fields).
pub fn teardown_cause(cause: Cause) -> TeardownCause {
    use TeardownCause as T;
    match cause {
        Cause::Clean => T::Clean,
        Cause::ClosureRecheckFailed => T::ClosureRecheckFailed,
        Cause::SessionSpecInconsistent => T::SessionSpecInconsistent,
        Cause::SpawnFailed => T::SpawnFailed,
        Cause::HandshakeDeadline => T::HandshakeDeadline,
        Cause::ControlRefusal(_) => T::ControlRefusal,
        Cause::ProviderProtocol => T::ProviderProtocol,
        Cause::UnexpectedExit => T::UnexpectedExit,
        Cause::Deadline => T::Deadline,
        Cause::Liveness => T::Liveness,
        Cause::MemoryCeiling => T::MemoryCeiling,
        Cause::ProcessCount => T::ProcessCount,
        Cause::ByteBound(_) => T::ByteBound,
        Cause::ScratchBound => T::ScratchBound,
        Cause::UserCancel => T::UserCancel,
        Cause::Revoked => T::Revoked,
        Cause::ObserverFailStop => T::ObserverFailStop,
        Cause::HostFault => T::HostFault,
        Cause::Abandoned => T::Abandoned,
    }
}
pub fn bounded_wait(wait: Wait) -> BoundedWait {
    match wait {
        Wait::Handshake => BoundedWait::Handshake,
        Wait::LivenessWindow => BoundedWait::LivenessWindow,
        Wait::ProgressAbsent => BoundedWait::ProgressAbsent,
        Wait::WallClock => BoundedWait::WallClock,
        Wait::NormalExitGrace => BoundedWait::NormalExitGrace,
        Wait::Stage1CancelGrace => BoundedWait::Stage1CancelGrace,
        Wait::ShutdownAck => BoundedWait::ShutdownAck,
        Wait::TermToKill => BoundedWait::TermToKill,
        Wait::ReapCeiling => BoundedWait::ReapCeiling,
        Wait::Drain => BoundedWait::Drain,
    }
}
/// Item 16's bound and the unit its observed value is in.
pub fn limit(kind: Limit) -> (LimitKind, LimitUnit) {
    match kind {
        Limit::ResidentMemory => (LimitKind::ResidentMemory, LimitUnit::Bytes),
        Limit::ProcessCount => (LimitKind::ProcessCount, LimitUnit::Processes),
        Limit::Response => (LimitKind::Response, LimitUnit::Bytes),
        Limit::Scratch => (LimitKind::Scratch, LimitUnit::Bytes),
        Limit::ToolOutput => (LimitKind::ToolOutput, LimitUnit::Bytes),
    }
}
/// The participant's terminal as S-OP-2's `StageTerminal` (NE:2025).
pub fn stage_terminal(kind: super::TerminalKind) -> StageTerminal {
    use super::TerminalKind as K;
    match kind {
        K::Complete => StageTerminal::Complete,
        K::Unavailable => StageTerminal::Unavailable,
        K::BudgetExhausted => StageTerminal::BudgetExhausted,
        K::ProviderFault => StageTerminal::ProviderFault,
        K::Cancelled => StageTerminal::Cancelled,
    }
}
/// The platform's terminating signal as S-OP-2c's `ChildSignal`, member for
/// member (the platform matched the number by its `libc` constant).
pub fn child_signal(signal: opensip_platform::TerminatingSignal) -> ChildSignal {
    use opensip_platform::TerminatingSignal as T;
    match signal {
        T::Abrt => ChildSignal::Sigabrt,
        T::Alrm => ChildSignal::Sigalrm,
        T::Bus => ChildSignal::Sigbus,
        T::Fpe => ChildSignal::Sigfpe,
        T::Hup => ChildSignal::Sighup,
        T::Ill => ChildSignal::Sigill,
        T::Int => ChildSignal::Sigint,
        T::Kill => ChildSignal::Sigkill,
        T::Pipe => ChildSignal::Sigpipe,
        T::Prof => ChildSignal::Sigprof,
        T::Quit => ChildSignal::Sigquit,
        T::Segv => ChildSignal::Sigsegv,
        T::Sys => ChildSignal::Sigsys,
        T::Term => ChildSignal::Sigterm,
        T::Trap => ChildSignal::Sigtrap,
        T::Usr1 => ChildSignal::Sigusr1,
        T::Usr2 => ChildSignal::Sigusr2,
        T::Vtalrm => ChildSignal::Sigvtalrm,
        T::Xcpu => ChildSignal::Sigxcpu,
        T::Xfsz => ChildSignal::Sigxfsz,
    }
}
/// A P3T or T2O phase name as S-OP-2c's `ProviderState` (LD-OPT-2), for a
/// participant's `Boundary::Phase`; `None` for a name no table has.
pub fn provider_state(phase: &str) -> Option<ProviderState> {
    use ProviderState as S;
    Some(match phase {
        "START" => S::Start,
        "WAIT_HELLO_ACK" => S::WaitHelloAck,
        "READY_OPEN_UNIVERSE" => S::ReadyOpenUniverse,
        "WAIT_UNIVERSE_ACCEPTED" => S::WaitUniverseAccepted,
        "READY_SNAPSHOT_MANIFEST" => S::ReadySnapshotManifest,
        "RECEIVING_SNAPSHOT" => S::ReceivingSnapshot,
        "WAIT_SNAPSHOT_ACCEPTED" => S::WaitSnapshotAccepted,
        "READY_DEPENDENCY_MANIFEST" => S::ReadyDependencyManifest,
        "RECEIVING_DEPENDENCY" => S::ReceivingDependency,
        "WAIT_DEPENDENCY_ACCEPTED" => S::WaitDependencyAccepted,
        "READY_PREPARED_MANIFEST" => S::ReadyPreparedManifest,
        "RECEIVING_PREPARED" => S::ReceivingPrepared,
        "WAIT_PREPARED_ACCEPTED" => S::WaitPreparedAccepted,
        "WAIT_NATIVE_CONTEXT_VERIFIED" => S::WaitNativeContextVerified,
        "READY_ANALYZE" => S::ReadyAnalyze,
        "ANALYZING" => S::Analyzing,
        "READY_COMPLETE" => S::ReadyComplete,
        "WAIT_CANCELLED" => S::WaitCancelled,
        "WAIT_ZERO_EXIT" => S::WaitZeroExit,
        "WAIT_EOF" => S::WaitEof,
        "DONE" => S::Done,
        "FAULT" => S::Fault,
        _ => return None,
    })
}

pub fn exit_class(exit: Exit) -> ExitClass {
    match exit {
        Exit::Exited(_) => ExitClass::Exited,
        Exit::Signaled(_) => ExitClass::Signaled,
        Exit::Unreaped => ExitClass::Unreaped,
    }
}
pub fn refusal_family(family: Family) -> RefusalFamily {
    match family {
        Family::Rf1 => RefusalFamily::Rf1,
        Family::Rf2 => RefusalFamily::Rf2,
        Family::Rf3 => RefusalFamily::Rf3,
        Family::Rf4 => RefusalFamily::Rf4,
        Family::Rf5 => RefusalFamily::Rf5,
        Family::Rf6 => RefusalFamily::Rf6,
        Family::Rf7 => RefusalFamily::Rf7,
        Family::Rf8 => RefusalFamily::Rf8,
    }
}
pub fn liveness_miss(miss: LivenessMiss) -> (Miss, Option<RefusalFamily>) {
    match miss {
        LivenessMiss::WindowExpired => (Miss::WindowExpired, None),
        LivenessMiss::NonceMismatch(family) => (Miss::NonceMismatch, Some(refusal_family(family))),
    }
}
pub fn scratch_retained(retained: ScratchRetained) -> (ScratchRetainedReason, Option<i32>) {
    match retained {
        ScratchRetained::IoFailure(errno) => (ScratchRetainedReason::IoFailure, Some(errno)),
        ScratchRetained::WorkExhausted => (ScratchRetainedReason::WorkExhausted, None),
        ScratchRetained::RootUnreaped => (ScratchRetainedReason::RootUnreaped, None),
    }
}

// ------------------------------------------------------------------ item 22's route

/// Item 22's rows (:707-726), by owner route (LD-D3A-11). D3 assigns no
/// code: J2 maps each to J1's.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum OwnerRoute {
    /// `clean` and admissible: the admission owner's (H, J2).
    Admission,
    /// `userInterrupted` before FinalGate admission: `interrupted` 130.
    Interrupted,
    /// A provider-spoken or provider-caused fault: `operational-failed`,
    /// `PROVIDER.PROTOCOL_VIOLATION`.
    ProviderProtocol,
    /// D4's pre-spawn closure recheck: `DELIVERY.CLOSURE_BYTES_CORRUPT`.
    ClosureBytesCorrupt,
    /// The closure is unspawnable: `DELIVERY.CLOSURE_UNSPAWNABLE`.
    ClosureUnspawnable,
    /// A host-built spec that differs from the admission:
    /// `SYSTEM.OUTCOME.ILLEGAL_STATE`, `host-invariant`.
    HostInvariant,
    Revoked,
    ObserverFailStop,
    /// A host I/O failure: `HOST.IO_FAILURE`, `host-io`.
    HostIo,
    /// None manufactured: OPP §5.2's host-panic rows apply.
    Abandoned,
    /// MC item 12's route for the tool adapter.
    Tool,
    /// Refused before any provider starts, projected by J1 (SD-5b).
    MemoryBudgetBelowCeiling,
}

/// A spawned settlement's one route.
pub fn settlement_route(settlement: &Settlement) -> OwnerRoute {
    if settlement.user_interrupted() {
        return OwnerRoute::Interrupted;
    }
    if settlement.is_tool() && settlement.first_cause() != Cause::Abandoned {
        return OwnerRoute::Tool;
    }
    cause_route(settlement.first_cause())
}

/// Each cause's one route (item 22): only a provider-spoken or
/// provider-caused cause takes `ProviderProtocol`.
pub fn cause_route(cause: Cause) -> OwnerRoute {
    match cause {
        Cause::Clean => OwnerRoute::Admission,
        Cause::ProviderProtocol
        | Cause::ControlRefusal(_)
        | Cause::UnexpectedExit
        | Cause::Deadline
        | Cause::Liveness
        | Cause::MemoryCeiling
        | Cause::ProcessCount
        | Cause::ByteBound(ByteBound::Response)
        | Cause::ScratchBound
        | Cause::HandshakeDeadline => OwnerRoute::ProviderProtocol,
        // A tool's output bound is MC item 12's, projected by J1.
        Cause::ByteBound(ByteBound::ToolOutput) => OwnerRoute::Tool,
        Cause::ClosureRecheckFailed => OwnerRoute::ClosureBytesCorrupt,
        Cause::SpawnFailed => OwnerRoute::ClosureUnspawnable,
        Cause::SessionSpecInconsistent => OwnerRoute::HostInvariant,
        Cause::UserCancel => OwnerRoute::Interrupted,
        Cause::Revoked => OwnerRoute::Revoked,
        Cause::ObserverFailStop => OwnerRoute::ObserverFailStop,
        Cause::HostFault => OwnerRoute::HostIo,
        Cause::Abandoned => OwnerRoute::Abandoned,
    }
}

/// A supervision that never spawned: its pre-spawn or spawn route.
/// A spawn failure is unspawnable only for the closure's own errors
/// (`ENOENT`, `EACCES`, `ENOEXEC`, item 22); any other is the host's I/O.
pub fn run_error_route(error: &RunError) -> OwnerRoute {
    match error {
        RunError::Declined(PreSpawnRefusal::ClosureRecheckFailed) => {
            OwnerRoute::ClosureBytesCorrupt
        }
        RunError::Declined(PreSpawnRefusal::SessionSpecInconsistent) => OwnerRoute::HostInvariant,
        RunError::SpawnFailed(error) => match error {
            opensip_platform::LaunchError::Io { error, .. }
                if matches!(error.raw_os_error(), Some(2 | 8 | 13)) =>
            {
                OwnerRoute::ClosureUnspawnable
            }
            _ => OwnerRoute::HostIo,
        },
        RunError::AlreadyRun => OwnerRoute::HostInvariant,
    }
}

/// A refusal before preparation.
pub fn supervisor_error_route(error: SupervisorError) -> OwnerRoute {
    match error {
        SupervisorError::MemoryBudgetBelowCeiling { .. } => OwnerRoute::MemoryBudgetBelowCeiling,
        // A host-built spec the supervision cannot run is the host's bug.
        SupervisorError::LadderUnavailable | SupervisorError::DescriptorsMismatch => {
            OwnerRoute::HostInvariant
        }
    }
}

/// The protocol a participant selected, as the registry's `ProtocolMajor`.
pub fn protocol_major(protocol: crate::provider_protocol::table::Protocol) -> ProtocolMajor {
    match protocol {
        crate::provider_protocol::table::Protocol::Ts2 => ProtocolMajor::TypescriptSemantic2,
        crate::provider_protocol::table::Protocol::Rust3 => ProtocolMajor::RustSemantic3,
    }
}
