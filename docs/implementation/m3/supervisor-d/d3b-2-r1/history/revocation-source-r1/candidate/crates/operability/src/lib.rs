//! Safe operational records: the event registry, typed fields, sinks and loss accounting.
//!
//! Law M3-O1 r2, units O1-a and O1-b. The only package edge is `opensip-platform`.
//! Instrumented hosts emit request and metadata delivery through owning scopes.
#![forbid(unsafe_code)]

#[cfg(all(feature = "operability-dev-sinks", not(debug_assertions)))]
compile_error!(
    "the operability-dev-sinks feature is development-only (law M3-O1 item 10) and refuses every build without debug assertions"
);

#[cfg(all(feature = "test-mints", not(debug_assertions)))]
compile_error!(
    "the test-mints feature is test-only (law M3-O1 item 7) and refuses every build without debug assertions"
);

#[cfg(all(feature = "harness-instrumentation", not(debug_assertions)))]
compile_error!("the harness-instrumentation feature requires debug assertions (law S-OP-2b item2)");

#[cfg(any(feature = "operability-dev-sinks", feature = "harness-instrumentation"))]
mod phase;
#[cfg(any(
    test,
    feature = "operability-dev-sinks",
    feature = "harness-instrumentation"
))]
mod phase_clock;
#[cfg(any(feature = "operability-dev-sinks", feature = "harness-instrumentation"))]
pub use phase::{PhaseError, PhaseSpan, RequestSpan};
#[cfg(any(feature = "operability-dev-sinks", feature = "harness-instrumentation"))]
pub use phase_clock::TimingError;

mod catalog;
#[cfg(any(
    test,
    feature = "operability-dev-sinks",
    feature = "harness-instrumentation"
))]
mod commit_cell;
mod constants;
mod credentials;
#[cfg(feature = "operability-dev-sinks")]
mod dev_writer;
mod emit;
mod file_partition;
mod guard;
#[cfg(feature = "harness-instrumentation")]
mod harness_writer;
mod hmac;
mod kinds;
mod marker;
#[cfg(any(
    test,
    feature = "operability-dev-sinks",
    feature = "harness-instrumentation"
))]
mod queue;
mod readback;
#[cfg(any(
    test,
    feature = "operability-dev-sinks",
    feature = "harness-instrumentation"
))]
mod reservation;
mod scope;
mod sinks;
mod transport;
mod wire;
mod writer;

pub use catalog::{ReleaseCatalogEntry, lookup as lookup_release_catalog_entry};
pub use kinds::registry::PathAnchor;
pub use kinds::{
    ClosureDigest, DigestKind, IdentityDigest, IdentityDigestMint, ManifestDigest, SnapshotDigest,
    UniverseDigest,
};
pub use kinds::{DeclaredName, DeclaredNameMint, RuleId, RuleIdMint};
pub use kinds::{PathRef, PathRefMint};
pub use kinds::{ProjectPath, ProjectPathMint};

pub use scope::{
    AttemptScope, CommittedRunScope, ExecutionId, PlanAttemptScope, PlanScope, ProjectScope,
    RequestScope, StoredRunScope,
};
#[cfg(any(test, feature = "test-mints"))]
pub use scope::{
    test_committed_run_scope, test_project_scope, test_request_scope, test_stored_run_scope,
};
pub use transport::{CapabilitySet, LoggingUnavailable, finalize, start, start_for_request};

// The public facade exposes only closed registry types and sealed traits.
// Encoder maps, queues, sink descriptors and mint issuers remain private.
pub use catalog::{MEMBER_SHA256, SOURCE_RECEIPTS, SourceReceipt};
pub use constants::Level;
pub use emit::EmitOn;
pub use kinds::registry::{
    BuildProfile, CodeEnum, CommitNotPublished, CounterTable, Event, HostPhaseCompleted,
    HostPhaseStarted, HostRepairCompleted, IdentitySet, IoErrorKind, LogStreamOpened, LossCell,
    Phase, PhaseOutcome, Platform, RepairKind, RepairState, Sink, StorageCommitNotPublished,
    StorageCommitOwner, StorageCommitPublished, TableRegistration,
};
// M3-D unit D3a-3: the supervision records (M3-D r5 item 21).
pub use kinds::registry::{
    BoundedWait, ControlCancelReason, ExitClass, FaultSource, ForceTrigger, LimitKind, LimitUnit,
    LivenessMiss, ProtocolMajor, ProviderFaultReduced, ProviderProcessReady,
    ProviderProcessSpawned, ProviderResourcesReported, ProviderRole, ProviderStderrReduced,
    RefusalFamily, RssUnit, RustDetailCode, RustFaultKind, ScratchRetainedReason,
    SupervisionCancelForced, SupervisionCancelSent, SupervisionLimitBreached,
    SupervisionLivenessMissed, SupervisionSampleIncomplete, SupervisionScratchRetained,
    SupervisionSettled, SupervisionTeardownStarted, SupervisionTreeSwept, SupervisionWaitExpired,
    TeardownCause, ToolProcessReaped, ToolProcessSpawned, Universe,
};
pub use kinds::registry::{
    ToolChildSettled, ToolLimitBreached, ToolSampleIncomplete, ToolScratchRetained,
    ToolTeardownStarted, ToolWaitExpired,
};
// M3-D unit D3a-4: the four events S-OP-2c unblocks, and their tables.
pub use kinds::registry::{
    ChildSignal, ProviderProcessReaped, ProviderReason, ProviderStageChanged,
    ProviderStageTerminal, ProviderState, ReapedExit, ReapedUsage, StageKind, StageTerminal,
    SupervisionProgressAbsent,
};
// M3-D unit D3b-1: a tool's tree sweep (D3b plan r3, LD-D3B-9).
pub use kinds::registry::ToolTreeSwept;
pub use kinds::{
    AdmittedId, Bytes, CaptureSummary, Code, Count, Counts, Elapsed, Errno, Flag, Form, Position,
    PositionMint, PrivacyClass, ProcessId, ProcessIdMint, Reduced, RegisteredCode, SafeField,
    Version,
};
pub use readback::{FieldDrops, Readmit, RecordDrops, readmit};
pub use scope::{HasExecution, HasPlan, HasProject, HasRun};

pub use marker::MarkerOutcome;
pub use transport::{FrozenSummary, frozen_summary};
pub use writer::CapturedError;

#[cfg(test)]
mod privacy_tests;

// D3b-2's S6 mark and measurement vocabulary and two scope-specific events.
pub use kinds::registry::{
    ElapsedStatus, RevocationElapsed, RevocationMark, SupervisionRevocationMissed,
    ToolRevocationMissed,
};
