//! M3-D r5 items 12 to 15, 17 and 19's normal end (unit D3a-1, D3a plan r4):
//! one supervised provider child, from its `VerifiedLaunch` to exactly one
//! `Settlement`.
//!
//! One thread owns the child's five host ends and its exit source, waits on
//! them with `poll(2)` (`opensip_platform::wait_ready`) and services them
//! non-blocking (item 12, :449; LD-D3A-13). The provider-side participant
//! is the only reader of fd1 and the only writer of fd0 (item 10, :379;
//! LD-D3A-3); this loop never touches a provider octet. It reads the
//! control channel itself (LD-D3A-4), drives the handshake through D2a's
//! `ControlSession`, joins EOF and exit for the participant (item 13), runs
//! the normal end (LD-D3A-15) and D3a's fault ladder (LD-D3A-6), and mints
//! one settlement (LD-D3A-5).
//!
//! Unit D3a-2 adds item 16: the sampled resident-memory ceiling, the process
//! count, TS2's aggregate response bound, the scratch measurement at
//! settlement, the zero-fit refusal, and the tool output and tool
//! materialization accounting (LD-D3A-16). It adds item 12's **tool class**
//! (:434): a first-party closure tool on fds 0 to 2, fd0 at EOF, with no
//! control plane, so it skips `Handshaking`; under the tool's wall clock
//! (item 14, :490), its process count (item 16, :533) and its output bound
//! on fd1 (:548), with stderr counted as every child's (item 17).
//!
//! Unit D3a-3 adds items 20 to 22: the admission gate
//! ([`Settlement::release`]) and the discard of every other settlement's
//! candidates, the record facts each registered event needs
//! ([`records::RecordFact`], LD-D3A3-1), and each settlement's one route
//! ([`records::OwnerRoute`], LD-D3A-11).
//!
//! **Not here.** The descendant step, user cancellation, revocation and
//! harness coexistence are D3b's; MC item 12's adapter, which builds the
//! tool's launch and reads its output, is C3b's; tool materialization's
//! writes are C3's; the records' emission, with the minted scope, universe
//! and pid, is J2b's.
use crate::control_protocol::{
    AdmittedSelection, Control3Root, ControlContext, ControlSession, ControlState, ControlVerdict,
    Direction, RefusalDetail, RefusalFamily, SubprotocolTuple, host_hello, host_select,
};
use crate::provider_protocol::table::Protocol;
use crate::provider_protocol::{ProcessEvent, ProcessFault};
use opensip_contracts::generated::evidence::FieldPresence;
use opensip_contracts::generated::protocol::{
    Control3RootVariant7Property0, Control3RootVariant7Property0Reason as CancelReason,
    Control3RootVariant8Property0, Control3RootVariant14Property0,
    Control3RootVariant14Property0Reason as ShutdownReason,
};
use opensip_platform::{
    DescriptorSet, LaunchError, ProcessChild as Child, ProcessExitStatus, Readiness, Reaped,
    ScratchRoot, VerifiedLaunch, WorkFailure, WorkLedger, group_members, resident_bytes, spawn,
    wait_ready,
};
use std::collections::VecDeque;
use std::fs::File;
use std::io::{self, Read, Write};
use std::num::NonZeroU64;
use std::os::fd::AsRawFd;
use std::sync::{Arc, Mutex, MutexGuard, PoisonError};
use std::time::{Duration, Instant};

// ------------------------------------------------------------------ item 14's release constants

/// Handshake, spawn to `selectAck`: 30 s provisional (item 14, :485).
pub const HANDSHAKE: Duration = Duration::from_secs(30);
/// The `health` interval in STEADY: 1 s (item 14, :486; item 15, :512).
pub const HEALTH_PING_INTERVAL: Duration = Duration::from_secs(1);
/// The liveness window: 5 s provisional (item 14, :487; OPP:237).
pub const LIVENESS_WINDOW: Duration = Duration::from_secs(5);
/// The progress-absent log interval: 30 s (item 14, :488; OPP:238).
pub const PROGRESS_ABSENT_INTERVAL: Duration = Duration::from_secs(30);
/// The provider's wall-clock deadline, spawn to the participant's
/// terminal: 1,800 s provisional, a host-safety backstop only (item 14,
/// :489; DLV:1163; RPP:601).
pub const WALL_CLOCK_PROVIDER: Duration = Duration::from_secs(1_800);
/// The tool's wall-clock deadline: 300 s provisional (item 14, :490).
pub const WALL_CLOCK_TOOL: Duration = Duration::from_secs(300);
/// TERM to KILL escalation: 1 s (item 14, :493; OPP:273).
pub const TERM_TO_KILL: Duration = Duration::from_secs(1);
/// The reap ceiling after KILL: 10 s (item 14, :494). Revocation's 5 s is
/// D3b's (item 19).
pub const REAP_CEILING: Duration = Duration::from_secs(10);
/// The drain deadline after death (J-3): 1 s (item 14, :495; CPC:481).
pub const DRAIN: Duration = Duration::from_secs(1);
/// stderr's truncation threshold, the protocol bound of 262,144 bytes
/// (item 16, :545; item 17, :565; NE:2967; RPP:117).
pub const STDERR_TRUNCATION_BYTES: u64 = 262_144;

/// The two protocol waits a participant supplies (LD-D3A-7): Rust3's are
/// its negotiated limits (RPP:119-120, agreed by exact equality in Hello,
/// item 14, :499), and D3 never substitutes its own; TS2's are the law's.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct ProtocolWaits {
    /// The stage-1 cancel grace (item 14, :492), D3b's user cancellation.
    pub stage1_cancel_grace: Duration,
    /// The normal-exit grace, terminal to exit, and the `shutdownAck` wait
    /// (item 14, :491 and :496).
    pub normal_exit_grace: Duration,
}
impl ProtocolWaits {
    /// TS2's provisional values: a 2 s stage-1 grace and a 5 s normal-exit
    /// grace (item 14, :491-492).
    pub const TS2: Self = Self {
        stage1_cancel_grace: Duration::from_secs(2),
        normal_exit_grace: Duration::from_secs(5),
    };
}

/// The host's own waits (item 14's table rows the host owns). Production
/// uses [`Waits::RELEASE`] only; a test may shorten them.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Waits {
    pub handshake: Duration,
    pub health_ping_interval: Duration,
    pub liveness_window: Duration,
    pub progress_absent_interval: Duration,
    pub wall_clock: Duration,
    pub term_to_kill: Duration,
    pub reap_ceiling: Duration,
    pub drain: Duration,
}
impl Waits {
    /// Item 14's release constants.
    pub const RELEASE: Self = Self {
        handshake: HANDSHAKE,
        health_ping_interval: HEALTH_PING_INTERVAL,
        liveness_window: LIVENESS_WINDOW,
        progress_absent_interval: PROGRESS_ABSENT_INTERVAL,
        wall_clock: WALL_CLOCK_PROVIDER,
        term_to_kill: TERM_TO_KILL,
        reap_ceiling: REAP_CEILING,
        drain: DRAIN,
    };
    /// A tool's: item 14's rows marked "all", and its own wall clock (:490).
    /// The provider-only waits never run for a tool, which has no control
    /// plane.
    pub const TOOL: Self = Self {
        wall_clock: WALL_CLOCK_TOOL,
        ..Self::RELEASE
    };
}

/// Item 14's bounded waits, each of which appends one typed event when it
/// expires (:481; SOP2:890). The health interval is a period, not a wait.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum BoundedWait {
    Handshake,
    LivenessWindow,
    ProgressAbsent,
    WallClock,
    NormalExitGrace,
    ShutdownAck,
    TermToKill,
    ReapCeiling,
    Drain,
}

// ------------------------------------------------------------------ item 16's ceilings and bounds (unit D3a-2)

/// The per-child-tree resident-memory ceiling: 8 GiB provisional, twice the
/// large-workload process-tree budget (item 16, :528; AQP:378).
pub const RESIDENT_MEMORY_CEILING: u64 = 8 * 1024 * 1024 * 1024;
/// The ceiling's sampling interval: 250 ms provisional (item 16, :529).
pub const MEMORY_SAMPLE_INTERVAL: Duration = Duration::from_millis(250);
/// A provider tree's processes: one (item 16, :533; DLV:1184; NE:2534-2535).
pub const PROVIDER_PROCESSES: usize = 1;
/// A tool tree's: at most 16, provisional (item 16, :533; NE:1788-1789), for
/// the tool supervision.
pub const TOOL_PROCESSES: usize = 16;
/// TS2's aggregate response bound: 1,073,741,824 B provisional, Rust3's
/// `maxResponsePayloadBytesTotal` (item 16, :544; RPP:114).
pub const TS2_RESPONSE_BYTES: u64 = 1_073_741_824;
/// Rust3's scratch: 2,147,483,648 B (item 16, :546; RPP:118; DRJ2:124).
pub const RUST3_SCRATCH_BYTES: u64 = 2_147_483_648;
/// TS2's scratch: 2 GiB provisional (item 16, :547).
pub const TS2_SCRATCH_BYTES: u64 = 2 * 1024 * 1024 * 1024;
/// A tool's output on fd1: 268,435,456 B provisional (item 16, :548).
pub const TOOL_OUTPUT_BYTES: u64 = 268_435_456;
/// Tool materialization's admitted candidate content: MC's acquisition
/// bound, 32 GiB (item 16, :549; LD-D3A-16).
pub const TOOL_MATERIALIZATION_CONTENT_BYTES: u64 = 34_359_738_368;
/// Its working space: 1 GiB (item 16, :549; LD-D3A-16).
pub const TOOL_MATERIALIZATION_WORKING_BYTES: u64 = 1_073_741_824;

/// The host's item 16 bounds as one supervision applies them. Production
/// uses [`Limits::RELEASE`] only; a test may shorten them.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Limits {
    pub resident_memory: u64,
    pub memory_sample_interval: Duration,
    pub ts2_response: u64,
    pub rust3_scratch: u64,
    pub ts2_scratch: u64,
    pub tool_output: u64,
}
impl Limits {
    /// Item 16's release values.
    pub const RELEASE: Self = Self {
        resident_memory: RESIDENT_MEMORY_CEILING,
        memory_sample_interval: MEMORY_SAMPLE_INTERVAL,
        ts2_response: TS2_RESPONSE_BYTES,
        rust3_scratch: RUST3_SCRATCH_BYTES,
        ts2_scratch: TS2_SCRATCH_BYTES,
        tool_output: TOOL_OUTPUT_BYTES,
    };
    /// The scratch limit for `protocol`.
    fn scratch(&self, protocol: Protocol) -> u64 {
        match protocol {
            Protocol::Rust3 => self.rust3_scratch,
            Protocol::Ts2 => self.ts2_scratch,
        }
    }
}

/// Item 16's breached bounds, as `supervision.limit.breached` names them.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum LimitKind {
    ResidentMemory,
    ProcessCount,
    Response,
    Scratch,
    ToolOutput,
}

/// A tool's materialization refused (item 16, :549; LD-D3A-16): the running
/// total that would result, and the limit. MC item 12's "D law's adapter
/// scratch bound", projected by J1.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct ToolScratchBound {
    pub observed: u64,
    pub limit: u64,
}
/// Tool materialization's accounting (LD-D3A-16): checked before each
/// whole admitted-copy write by C3's materializer, exact and never sampled.
/// A refusal changes nothing: no write is made and the total stands. It is
/// never the provider's scratch limit.
#[derive(Debug, Default)]
pub struct ToolMaterialization {
    total: u64,
}
impl ToolMaterialization {
    /// 32 GiB of admitted content plus 1 GiB of working space.
    pub const LIMIT: u64 = TOOL_MATERIALIZATION_CONTENT_BYTES + TOOL_MATERIALIZATION_WORKING_BYTES;
    pub fn new() -> Self {
        Self::default()
    }
    /// Charge `bytes` before writing them: refused exactly when the total
    /// would pass the limit.
    pub fn charge(&mut self, bytes: u64) -> Result<(), ToolScratchBound> {
        match self.total.checked_add(bytes) {
            Some(next) if next <= Self::LIMIT => {
                self.total = next;
                Ok(())
            }
            other => Err(ToolScratchBound {
                observed: other.unwrap_or(u64::MAX),
                limit: Self::LIMIT,
            }),
        }
    }
    pub fn total(&self) -> u64 {
        self.total
    }
}

/// A tool's output on fd1 over its bound (item 16, :548), projected by J1.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct ToolOutputBound {
    pub observed: u64,
    pub limit: u64,
}
/// A tool's output accounting (item 16, :548): each read's bytes charged
/// before they are kept, refused exactly past the bound. A refusal keeps
/// nothing and the total stands.
#[derive(Debug)]
pub struct ToolOutput {
    total: u64,
    limit: u64,
}
impl Default for ToolOutput {
    fn default() -> Self {
        Self::new()
    }
}
impl ToolOutput {
    pub const LIMIT: u64 = TOOL_OUTPUT_BYTES;
    pub fn new() -> Self {
        Self::with_limit(Self::LIMIT)
    }
    /// The supervision's, from its [`Limits`].
    fn with_limit(limit: u64) -> Self {
        Self { total: 0, limit }
    }
    pub fn charge(&mut self, bytes: u64) -> Result<(), ToolOutputBound> {
        match self.total.checked_add(bytes) {
            Some(total) if total <= self.limit => {
                self.total = total;
                Ok(())
            }
            other => Err(ToolOutputBound {
                observed: other.unwrap_or(u64::MAX),
                limit: self.limit,
            }),
        }
    }
    pub fn total(&self) -> u64 {
        self.total
    }
}

// ------------------------------------------------------------------ causes and settlement

/// The settlement's causes (item 12, :446). `user-cancel`, `revoked` and
/// `observer-fail-stop` are accepted in the table, but their ladders are
/// D3b's (LD-D3A-6). O7's `confinement-refused` is not at M3. The three
/// pre-spawn and spawn causes are carried by [`RunError`], since nothing
/// spawned yields no settlement (r2, Codex D3A1-R1-RF-5). `provider-protocol`
/// includes a component's accepted control `fault` report (LD-D3A-19).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Cause {
    Clean,
    ClosureRecheckFailed,
    SessionSpecInconsistent,
    SpawnFailed,
    HandshakeDeadline,
    ControlRefusal(RefusalFamily),
    ProviderProtocol,
    UnexpectedExit,
    Deadline,
    Liveness,
    MemoryCeiling,
    ProcessCount,
    ByteBound(ByteBound),
    ScratchBound,
    UserCancel,
    Revoked,
    ObserverFailStop,
    HostFault,
    Abandoned,
}
/// The byte bounds D3 itself enforces as a cause (item 16's table): TS2's
/// aggregate response, `byte-bound(response)` (:544); and a tool's output
/// on fd1, `byte-bound(tool-output)` (:548), whose settlement carries the
/// internal `ToolOutputBound` for J1 to project.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ByteBound {
    Response,
    ToolOutput,
}

/// The two refusals D4 raises before any spawn (item 12, :425).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum PreSpawnRefusal {
    ClosureRecheckFailed,
    SessionSpecInconsistent,
}

/// How the child ended (item 12, :440). A settlement exists only for a
/// spawned child, so it always has one (r2, RF-5).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ExitClass {
    Exited(i32),
    Signaled(i32),
    Unreaped,
}
/// Item 18's tree report, D3a's part (LD-D3A-6): D3a has no descendant
/// step, so a killed group is `GroupKilledPlatformLimited` only when the
/// group lists the zombie root alone, else `Incomplete`. D3b extends it.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum TreeReport {
    NotKilled,
    GroupKilledPlatformLimited,
    Incomplete,
}
/// stderr's count (item 17): bytes, saturating, and whether they passed the
/// truncation threshold. No byte is kept; D3a-3 reduces it to K7.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Default)]
pub struct StderrCount {
    pub bytes: u64,
    pub truncated: bool,
}
/// The reap's rusage (SOP2:910): CPU and the peak resident size, which
/// macOS reports in bytes.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Rusage {
    pub user_micros: u64,
    pub system_micros: u64,
    pub max_rss_bytes: u64,
}
/// The scratch's fate (item 12 as amended by LD-D3A-17 and, proposed with
/// this unit, LD-D3A-18, :444): removed, or retained with its reason.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ScratchFate {
    Removed,
    Retained(ScratchRetained),
}
/// Why a scratch was retained: a failed call's actual errno, or the
/// removal walk's finite budget, with no errno (LD-D3A-17); or the root was
/// abandoned at the reap ceiling and may still run in it, so it is held for
/// the process's life, with no errno (LD-D3A-18).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ScratchRetained {
    IoFailure(i32),
    WorkExhausted,
    RootUnreaped,
}

/// A participant's terminal (P3T and T2O's terminal law: the five kinds).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum TerminalKind {
    Complete,
    Unavailable,
    BudgetExhausted,
    ProviderFault,
    Cancelled,
}

/// The one-shot output of a verified terminal (LD-D3A-3, NBO-2): opaque,
/// not `Clone`, minted only inside this crate by the participant that
/// verified every commitment, holding the spool and the terminal's kind.
/// Item 20's gate ([`Settlement::release`], unit D3a-3) releases it from an
/// admissible settlement or drops it; without one nothing is releasable.
#[derive(Debug)]
pub struct TerminalOutput {
    kind: TerminalKind,
    spool: Spool,
}
impl TerminalOutput {
    /// For the participant only, after its terminal's commitments recompute.
    /// Its production callers are the codecs (D2b-3, D2b-4).
    #[cfg_attr(not(test), allow(dead_code))]
    pub(crate) fn mint(kind: TerminalKind, spool: Spool) -> Self {
        Self { kind, spool }
    }
    pub fn kind(&self) -> TerminalKind {
        self.kind
    }
    /// The candidates, for the admission owner (H) alone.
    pub fn into_spool(self) -> Spool {
        self.spool
    }
}
/// A participant's candidates, spooled `CANDIDATE_ONLY` (M3-D r5 item 20,
/// :667): opaque admitted frame payloads, never an iterator before
/// settlement. Not `Clone`: it moves into the one [`TerminalOutput`].
#[derive(Debug, Default)]
pub struct Spool {
    candidates: Vec<Vec<u8>>,
}
impl Spool {
    #[cfg_attr(not(test), allow(dead_code))]
    pub(crate) fn push(&mut self, candidate: Vec<u8>) {
        self.candidates.push(candidate);
    }
    pub fn len(&self) -> usize {
        self.candidates.len()
    }
    pub fn is_empty(&self) -> bool {
        self.candidates.is_empty()
    }
    /// The candidates, in admission order, for the admission owner.
    pub fn into_candidates(self) -> Vec<Vec<u8>> {
        self.candidates
    }
}

/// The one settlement (item 12, :435-446; LD-D3A-5). Its constructor is
/// private and called only by the one transition into `Settled`; it is not
/// `Clone`, and [`Supervision::take_settlement`] hands it out once.
#[derive(Debug)]
pub struct Settlement {
    first_cause: Cause,
    later_causes: Vec<Cause>,
    user_interrupted: bool,
    exit: ExitClass,
    tree: TreeReport,
    stderr: StderrCount,
    rusage: Option<Rusage>,
    scratch: ScratchFate,
    terminal: Option<TerminalKind>,
    eof_observed: bool,
    output: Option<TerminalOutput>,
    /// The tool class only: its output, and its bound's refusal.
    tool: Option<ToolResult>,
}
/// A tool's result (item 16, :548; item 22's tool row, :722): fd1's bytes
/// as read, never parsed here, and the `ToolOutputBound` refusal if fd1
/// passed its bound, when nothing past the bound was kept. MC item 12's
/// adapter (C3b) reads the output; J1 projects the refusal.
#[derive(Debug)]
struct ToolResult {
    /// Taken once.
    output: Option<Vec<u8>>,
    bound: Option<ToolOutputBound>,
}
impl Settlement {
    pub fn first_cause(&self) -> Cause {
        self.first_cause
    }
    /// Later triggers, appended and kept, never coalesced (item 12, :447).
    pub fn later_causes(&self) -> &[Cause] {
        &self.later_causes
    }
    pub fn user_interrupted(&self) -> bool {
        self.user_interrupted
    }
    pub fn exit(&self) -> ExitClass {
        self.exit
    }
    pub fn tree(&self) -> TreeReport {
        self.tree
    }
    pub fn stderr(&self) -> StderrCount {
        self.stderr
    }
    pub fn rusage(&self) -> Option<Rusage> {
        self.rusage
    }
    pub fn scratch(&self) -> ScratchFate {
        self.scratch
    }
    pub fn terminal(&self) -> Option<TerminalKind> {
        self.terminal
    }
    /// Item 20's admission condition: a clean cause, the participant's
    /// terminal, a zero exit, EOF observed, and the terminal's output
    /// (every commitment recomputed). The release is D3a-3's gate.
    pub fn admissible(&self) -> bool {
        self.first_cause == Cause::Clean
            && self.terminal.is_some()
            && self.exit == ExitClass::Exited(0)
            && self.eof_observed
            && self.output.is_some()
    }
    /// Item 20's gate (D3a-3): the terminal's output, once, only from an
    /// admissible settlement; from any other it is dropped here and nothing
    /// is released (DLV:1140-1143; RPP:597). There is no other way out.
    pub fn release(&mut self) -> Option<TerminalOutput> {
        let admissible = self.admissible();
        let output = self.output.take();
        if admissible { output } else { None }
    }
    /// Item 22's route (LD-D3A-11).
    pub fn route(&self) -> records::OwnerRoute {
        records::settlement_route(self)
    }
    /// Whether this is a tool's settlement (item 12, :434).
    pub fn is_tool(&self) -> bool {
        self.tool.is_some()
    }
    /// A tool's output bound refusal (item 16, :548), for J1 to project.
    pub fn tool_output_bound(&self) -> Option<ToolOutputBound> {
        self.tool.as_ref().and_then(|t| t.bound)
    }
    /// A tool's output, once, for MC item 12's adapter: only from a clean
    /// settlement whose tool exited zero with fd1 at EOF and within its
    /// bound. A failed tool (a nonzero exit or its own signal death) hands
    /// nothing; its exit is the adapter's to route (item 22's tool row,
    /// :722; NE:1789-1791).
    pub fn take_tool_output(&mut self) -> Option<Vec<u8>> {
        let complete = self.first_cause == Cause::Clean
            && self.exit == ExitClass::Exited(0)
            && self.eof_observed;
        match &mut self.tool {
            Some(tool) if complete && tool.bound.is_none() => tool.output.take(),
            _ => None,
        }
    }
}

// ------------------------------------------------------------------ the participant seam

/// What one participant call reports (LD-D3A-3): its status, the progress
/// transitions it admitted (item 15, :513), the payload bytes of the frames
/// it admitted (D3a-2's TS2 aggregate), and whether the read saw fd1's EOF
/// at a frame boundary. It carries no payload byte.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ParticipantStep {
    pub status: ParticipantStatus,
    pub progress: Vec<Progress>,
    pub admitted_payload_bytes: u64,
    /// fd1 read EOF at a frame boundary. EOF inside a frame is truncation:
    /// the participant reports `Fault` itself.
    pub eof: bool,
    /// M3-L r1:400's span boundaries the participant admitted, for
    /// `provider.process.ready` (unit D3a-3).
    pub boundaries: Vec<Boundary>,
}
impl ParticipantStep {
    pub fn status(status: ParticipantStatus) -> Self {
        Self {
            status,
            progress: Vec::new(),
            admitted_payload_bytes: 0,
            eof: false,
            boundaries: Vec::new(),
        }
    }
}
/// The provider-boundary span edges (M3-L r1:400): the snapshot transfer
/// sub-span's start and end, and the context's verification
/// (`NativeContextVerified`, or the pre-Analyze `Unavailable`) that ends
/// `start`.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Boundary {
    TransferStarted,
    TransferEnded,
    ContextVerified,
}
/// The participant's state as its table has it.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ParticipantStatus {
    Running,
    /// A terminal reached: the exit and EOF are still owed (WAIT_ZERO_EXIT,
    /// WAIT_EOF).
    Terminal(TerminalKind),
    /// DONE.
    Done,
    /// FAULT.
    Fault,
    /// The host's own failure on the participant's side (unit D2b-3b): its
    /// sealed snapshot cannot supply a frame, or its sender refused a
    /// divergence before writing. A host fault, never `provider-protocol`.
    HostFault,
}
/// Item 15's progress: only transitions the participant admitted (:513).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Progress {
    SnapshotAcknowledged,
    FactBatch,
    Coverage,
    StageChanged,
}

/// The provider-side participant (LD-D3A-3): the only reader of fd1 and the
/// only writer of fd0. The loop calls it synchronously, and each call makes
/// **at most one** non-blocking read or write and returns (the yield
/// contract), so the other descriptors, the exit and every timer run
/// between any two provider reads.
pub trait Participant {
    /// Its protocol waits (LD-D3A-7).
    fn protocol_waits(&self) -> ProtocolWaits;
    /// Its selected protocol (item 10): TS2's aggregate response bound and
    /// each protocol's scratch limit are chosen by it (item 16).
    fn protocol(&self) -> Protocol;
    /// Whether it has bytes pending for fd0.
    fn wants_write(&self) -> bool;
    /// fd1 is readable: one non-blocking read into its accumulator.
    fn readable(&mut self, fd1: &mut dyn Read) -> ParticipantStep;
    /// fd0 is writable and a write is pending: one non-blocking write from
    /// its pending buffer at its offset.
    fn writable(&mut self, fd0: &mut dyn Write) -> ParticipantStep;
    /// One of item 13's process events.
    fn process(&mut self, event: ProcessEvent) -> ParticipantStep;
    /// The normal end: no further input will be written (LD-D3A-15).
    fn close_input(&mut self);
    /// The verified terminal's output, once.
    fn take_terminal_output(&mut self) -> Option<TerminalOutput>;
    /// Item 20's discard: a settlement that is not admissible drops every
    /// candidate the participant still spools (DLV:1140-1143).
    fn discard(&mut self);
}

/// The tool class's participant: none. A tool has no provider protocol, so
/// no participant exists for it and none of these calls can be made.
#[derive(Debug)]
pub enum NoProvider {}
impl Participant for NoProvider {
    fn protocol_waits(&self) -> ProtocolWaits {
        match *self {}
    }
    fn protocol(&self) -> Protocol {
        match *self {}
    }
    fn wants_write(&self) -> bool {
        match *self {}
    }
    fn readable(&mut self, _: &mut dyn Read) -> ParticipantStep {
        match *self {}
    }
    fn writable(&mut self, _: &mut dyn Write) -> ParticipantStep {
        match *self {}
    }
    fn process(&mut self, _: ProcessEvent) -> ParticipantStep {
        match *self {}
    }
    fn close_input(&mut self) {
        match *self {}
    }
    fn take_terminal_output(&mut self) -> Option<TerminalOutput> {
        match *self {}
    }
    fn discard(&mut self) {
        match *self {}
    }
}
/// A tool's supervision (item 12's tool class, :434).
pub type ToolSupervision = Supervision<NoProvider>;

// ------------------------------------------------------------------ the supervision

/// Item 12's states (:423-431). A tool skips `Handshaking` (:434).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum State {
    Prepared,
    Spawning,
    Handshaking,
    Running,
    Stopping(Cause),
    Killing,
    Reaping,
    Settled,
}

/// The host's supervision channels, for the merged order (item 12, :448).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Channel {
    Data,
    Stderr,
    Control,
}

/// One appended event of the merged order (item 12, :448): applied by the
/// joins, given to the observer, counted and dropped. D3a-3 maps them to
/// the registry's records.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum SupervisionEvent {
    Spawned {
        process_id: i32,
    },
    ControlSent(&'static str),
    ControlReceived(&'static str),
    Running,
    Progress(Progress),
    Terminal(TerminalKind),
    ChannelEof(Channel),
    ExitObserved,
    Delivered(ProcessEvent),
    WaitExpired(BoundedWait),
    /// An item 16 bound breached (`supervision.limit.breached`).
    LimitBreached(LimitKind),
    /// Item 15's liveness fault, with its reduced host-held provenance (r3,
    /// NBO-1).
    LivenessMissed(LivenessMiss),
    ProgressAbsent,
    Trigger(Cause),
    TeardownStarted(Cause),
    /// The ladder's T-1: control `cancel`, if the session takes it.
    CancelAttempted,
    Signalled {
        signal: i32,
    },
    Reaped,
    Abandoned,
    Settled(Cause),
    /// An event after settlement: counted and dropped (LD-D3A-5).
    LateEvent,
    /// A resource sample the host could not complete (D3A2-R1-NBO-1).
    SampleIncomplete,
}

/// Which of item 15's liveness faults (r3, NBO-1): the window expired with
/// no report, or a report's nonce mismatched and the control owner refused
/// it in `family`. A reduced discriminator only: no nonce, frame or detail
/// text is kept. D3a-3's record projection carries it onward.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum LivenessMiss {
    WindowExpired,
    NonceMismatch(RefusalFamily),
}

/// Why a supervision produced no settlement: it never spawned (r2, RF-5).
#[derive(Debug)]
pub enum RunError {
    /// D4's pre-spawn refusal (item 12, :425).
    Declined(PreSpawnRefusal),
    /// The spawn itself failed (`spawn-failed`, :426).
    SpawnFailed(LaunchError),
    /// `run` on a supervision that already ran.
    AlreadyRun,
}

/// Why a supervision was not prepared.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum SupervisorError {
    /// The caller may need user cancellation, revocation or observer
    /// fail-stop, whose ladders are D3b's (LD-D3A-6).
    LadderUnavailable,
    /// Zero fit (item 16, :534; OPP:277): the memory budget is below one
    /// ceiling, refused before any provider starts. J1 projects it.
    MemoryBudgetBelowCeiling { budget: u64, ceiling: u64 },
    /// The launch's descriptor set is not its class's (item 5, :274): a
    /// provider supervision takes fds 0 to 4, a tool's fds 0 to 2.
    DescriptorsMismatch,
}

/// What D4's session factory hands over (item 12's `Prepared`, :425).
#[derive(Debug)]
pub struct SessionSpec {
    pub launch: VerifiedLaunch,
    pub selection: AdmittedSelection,
    /// Whether the caller may need a D3b ladder.
    pub needs_d3b_ladders: bool,
    /// The invocation's memory budget (AQP §5.2), for the zero-fit refusal.
    pub memory_budget_bytes: u64,
}

/// What MC item 12's adapter hands over for a tool (item 1's `Tool` class,
/// :188): its verified launch, on fds 0 to 2 (item 5, :274), and the
/// invocation's memory budget. A tool has no selection and no control plane.
#[derive(Debug)]
pub struct ToolSpec {
    pub launch: VerifiedLaunch,
    /// Whether the caller may need a D3b ladder.
    pub needs_d3b_ladders: bool,
    pub memory_budget_bytes: u64,
}

/// A cross-thread trigger (LD-D3A-5): appended through one bounded gate,
/// never applied to the state from another thread.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum Trigger {
    HostFault,
}

/// The triggers' one linearization point (r3, RF-2): the closed check and
/// the append are one critical section, and so are the settlement's close
/// and its drain. A trigger is therefore either admitted before the close,
/// and then consumed by a turn or drained and counted by the close, or
/// refused after it and counted once by the refusal; none is queued
/// unaccounted. Each section is constant work on a queue of at most
/// [`TRIGGER_CAPACITY`], so admission never waits on the loop.
#[derive(Debug)]
struct TriggerGate {
    state: Mutex<GateState>,
    /// A test's pause between the closed check and the append.
    #[cfg(test)]
    pause: Option<Arc<(std::sync::Barrier, std::sync::Barrier)>>,
}
#[derive(Debug)]
struct GateState {
    closed: bool,
    pending: VecDeque<Trigger>,
    late: u64,
}
impl TriggerGate {
    fn new() -> Self {
        Self {
            state: Mutex::new(GateState {
                closed: false,
                pending: VecDeque::with_capacity(TRIGGER_CAPACITY),
                late: 0,
            }),
            #[cfg(test)]
            pause: None,
        }
    }
    /// A panic elsewhere cannot leave the state half-written: each section
    /// is complete or not begun, so a poisoned lock's state is used as is.
    fn lock(&self) -> MutexGuard<'_, GateState> {
        self.state.lock().unwrap_or_else(PoisonError::into_inner)
    }
    /// Admit `trigger`: `false` when the gate is closed (counted late) or a
    /// trigger per slot is already pending.
    fn admit(&self, trigger: Trigger) -> bool {
        let mut gate = self.lock();
        if gate.closed {
            gate.late += 1;
            return false;
        }
        #[cfg(test)]
        if let Some(pause) = &self.pause {
            pause.0.wait();
            pause.1.wait();
        }
        if gate.pending.len() >= TRIGGER_CAPACITY {
            return false;
        }
        gate.pending.push_back(trigger);
        true
    }
    fn take(&self) -> Option<Trigger> {
        self.lock().pending.pop_front()
    }
    /// Close admission and drain what was admitted before it, counting each
    /// as late; returns how many were drained.
    fn close(&self) -> usize {
        let mut gate = self.lock();
        gate.closed = true;
        let drained = gate.pending.len();
        gate.pending.clear();
        gate.late += drained as u64;
        drained
    }
    fn late(&self) -> u64 {
        self.lock().late
    }
}

/// The one way another thread reaches a supervision.
#[derive(Debug, Clone)]
pub struct SupervisionHandle {
    gate: Arc<TriggerGate>,
}
impl SupervisionHandle {
    /// The host's own fault (cause `host-fault`). `false` when it was not
    /// appended: a trigger is already pending, or the supervision has
    /// settled, when the request is counted as a late event and dropped
    /// (r2, NBO-1). Admission and the settlement's close are linearized by
    /// one gate (r3, RF-2).
    pub fn host_fault(&self) -> bool {
        self.gate.admit(Trigger::HostFault)
    }
}
/// The bounded channel's capacity: one pending trigger per source. It is
/// also the most triggers one turn consumes (r2, RF-1).
const TRIGGER_CAPACITY: usize = 4;
/// The most stderr reads, and control reads, one turn makes (r2, RF-1):
/// service quanta, not bounds of the law. Each read is at most the fixed
/// buffer or one frame's remainder, so a sustained producer cannot hold a
/// turn, and every other end, timer and teardown step is serviced between.
const STDERR_READS_PER_TURN: usize = 16;
const CONTROL_READS_PER_TURN: usize = 16;

/// The child's host ends, by slot; `None` once closed (item 5).
#[derive(Default)]
struct HostEnds {
    fd0: Option<File>,
    fd1: Option<File>,
    fd2: Option<File>,
    fd3: Option<File>,
    fd4: Option<File>,
}

/// LD-D3A-4's control acquisition: the 4-byte prefix first, judged against
/// the frame bound before any body byte is read; then exactly the body,
/// into one reused buffer of the bound plus four bytes. A read never goes
/// past the frame it is completing.
struct ControlReader {
    buf: Vec<u8>,
    have: usize,
    body: Option<usize>,
}
enum ControlRead {
    /// A whole frame, `buf[..len]`.
    Frame(usize),
    /// A prefix over the bound (or zero): `buf[..4]` alone, for D2a to
    /// refuse RF2 unbuffered.
    OverBound,
    Pending,
    /// EOF; `true` when a frame was cut short.
    Eof(bool),
}
impl ControlReader {
    fn new(bound: u32) -> Self {
        Self {
            buf: vec![0; bound as usize + 4],
            have: 0,
            body: None,
        }
    }
    fn read(&mut self, fd: &mut impl Read, bound: u32) -> io::Result<ControlRead> {
        let target = self.body.map_or(4, |n| 4 + n);
        match fd.read(&mut self.buf[self.have..target]) {
            Ok(0) => return Ok(ControlRead::Eof(self.have > 0)),
            Ok(n) => self.have += n,
            Err(e) if e.kind() == io::ErrorKind::WouldBlock => return Ok(ControlRead::Pending),
            Err(e) if e.kind() == io::ErrorKind::Interrupted => return Ok(ControlRead::Pending),
            Err(e) => return Err(e),
        }
        if self.body.is_none() && self.have == 4 {
            let n = u32::from_be_bytes([self.buf[0], self.buf[1], self.buf[2], self.buf[3]]);
            if n == 0 || n > bound {
                self.have = 0;
                return Ok(ControlRead::OverBound);
            }
            self.body = Some(n as usize);
        }
        match self.body {
            Some(n) if self.have == 4 + n => {
                self.have = 0;
                self.body = None;
                Ok(ControlRead::Frame(4 + n))
            }
            _ => Ok(ControlRead::Pending),
        }
    }
}

/// A host frame waiting for the pending write to finish (r2, RF-4): built
/// and sent through the session only once fd3 is free.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum Deferred {
    /// The normal end's `shutdown {reason: normal}`; fd3 closes after it.
    Shutdown,
    /// T-1's `cancel`.
    Cancel(CancelReason),
}

/// The host's pending control write: the whole frame and its offset, and
/// the record its full write makes (r2, D3A3-R1-RF-2: T-1's cancel is
/// recorded only as written, never as queued; a failed or abandoned write
/// drops it unrecorded).
#[derive(Default)]
struct PendingWrite {
    bytes: Vec<u8>,
    at: usize,
    written: Option<records::RecordFact>,
}

/// The supervised class (item 1, :186-188).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum Class {
    Provider,
    Tool,
}

/// A tool's fd1 (item 5, :274): read by the loop into one fixed buffer,
/// charged to the output bound before it is kept (item 16, :548). Past the
/// bound nothing more is kept and fd1 is closed: the tool is being torn
/// down. The bytes are never parsed here.
struct ToolCapture {
    buf: Box<[u8]>,
    output: Vec<u8>,
    accounting: ToolOutput,
    bound: Option<ToolOutputBound>,
}
/// The tool output read buffer, and the most fd1 reads one turn makes: a
/// service quantum as stderr's (LD-D3A1-8), not a bound of the law.
const TOOL_READ_BUFFER: usize = 65_536;
const TOOL_READS_PER_TURN: usize = 16;

/// D3a's fault ladder's progress (LD-D3A-6).
#[derive(Debug, Clone, Copy)]
struct Ladder {
    /// T-1 is done, or skipped: the normal end's grace expiry enters at T-2
    /// (LD-D3A-15).
    t1_done: bool,
    term_at: Option<Instant>,
    kill_at: Option<Instant>,
}

/// `ESRCH`: the process no longer exists (a member that exited).
const ESRCH: i32 = 3;

/// The two signals D3a's ladder sends to the group (item 19, :639-640),
/// by their POSIX numbers on both families.
const SIGTERM: i32 = 15;
const SIGKILL: i32 = 9;

/// stderr's fixed read buffer (item 17): bytes are read into it, counted
/// and overwritten; nothing else holds them.
const STDERR_BUFFER: usize = 4096;

/// A test's observer of the merged order.
type Observer = Box<dyn FnMut(&SupervisionEvent)>;
/// The caller's record sink (LD-D3A3-1): J2b builds and emits each fact's
/// registry event with its minted scope, universe and pid.
pub type FactSink = Box<dyn FnMut(records::RecordFact)>;

/// One child's supervision (item 12).
pub struct Supervision<P: Participant> {
    state: State,
    class: Class,
    launch: Option<VerifiedLaunch>,
    // The provider class only: its selection, participant, protocol waits,
    // control session and reader. A tool has none (item 12, :434).
    selection: Option<AdmittedSelection>,
    participant: Option<P>,
    waits: Waits,
    protocol: Option<ProtocolWaits>,
    child: Option<Child>,
    ends: HostEnds,
    control: Option<ControlSession>,
    reader: Option<ControlReader>,
    // The tool class only.
    tool: Option<ToolCapture>,
    control_out: PendingWrite,
    close_fd3_after_write: bool,
    host_seq: u64,
    nonce_seq: u64,
    stderr_buf: [u8; STDERR_BUFFER],
    stderr: StderrCount,
    gate: Arc<TriggerGate>,
    observer: Option<Observer>,
    facts: Option<FactSink>,
    spawned_pid: Option<u32>,
    // D3a-3: M3-L r1:400's spans, and the last incomplete sample.
    transfer_started: Option<Instant>,
    transfer_ended: Option<Instant>,
    ready_recorded: bool,
    last_incomplete: Option<(u64, u64, bool)>,
    events: u64,
    // Timing.
    spawned_at: Option<Instant>,
    last_progress: Option<Instant>,
    next_health: Option<Instant>,
    health_due: Option<Instant>,
    terminal_at: Option<Instant>,
    exit_at: Option<Instant>,
    // Joins.
    terminal: Option<TerminalKind>,
    participant_status: ParticipantStatus,
    fd1_eof: bool,
    held_eof: bool,
    eof_delivered: bool,
    shutdown_ack: bool,
    exit: Option<ProcessExitStatus>,
    death_appended: bool,
    reaped: Option<Reaped>,
    // Teardown.
    first_cause: Option<Cause>,
    later_causes: Vec<Cause>,
    ladder: Option<Ladder>,
    grace_expired: bool,
    tree: TreeReport,
    settlement: Option<Settlement>,
    // Item 16.
    limits: Limits,
    protocol_kind: Option<Protocol>,
    next_sample: Option<Instant>,
    asserted_resident: Option<u64>,
    memory_breached: bool,
    count_breached: bool,
    response_bytes: u64,
    response_breached: bool,
    // r2.
    control_refused: bool,
    clean_at: Option<Instant>,
    deferred: Option<Deferred>,
    exit_independent: bool,
    tree_confirmed: Option<TreeReport>,
    #[cfg(test)]
    seams: tests::Seams,
}

/// The provider class's parts, handed to [`Supervision::new`].
struct Provider<P> {
    selection: AdmittedSelection,
    participant: P,
    protocol: ProtocolWaits,
    protocol_kind: Protocol,
    control: ControlSession,
    reader: ControlReader,
}

/// The refusals before `Prepared` (LD-D3A-6; item 16, :534; item 5, :274):
/// a caller that may need a D3b ladder, a memory budget below one ceiling
/// (zero fit: the ceiling is never lowered silently), and a launch whose
/// descriptor set is not its class's.
fn admit_spec(
    launch: &VerifiedLaunch,
    descriptors: DescriptorSet,
    needs_d3b_ladders: bool,
    memory_budget_bytes: u64,
) -> Result<(), SupervisorError> {
    if needs_d3b_ladders {
        return Err(SupervisorError::LadderUnavailable);
    }
    if memory_budget_bytes < Limits::RELEASE.resident_memory {
        return Err(SupervisorError::MemoryBudgetBelowCeiling {
            budget: memory_budget_bytes,
            ceiling: Limits::RELEASE.resident_memory,
        });
    }
    if launch.spec().descriptors() != descriptors {
        return Err(SupervisorError::DescriptorsMismatch);
    }
    Ok(())
}

impl Supervision<NoProvider> {
    /// A prepared tool supervision (`Prepared`, :425; the tool class,
    /// :434): nothing is spawned.
    pub fn prepare_tool(spec: ToolSpec) -> Result<Self, SupervisorError> {
        Self::prepare_tool_with(spec, Waits::TOOL)
    }
    fn prepare_tool_with(spec: ToolSpec, waits: Waits) -> Result<Self, SupervisorError> {
        admit_spec(
            &spec.launch,
            DescriptorSet::Tool,
            spec.needs_d3b_ladders,
            spec.memory_budget_bytes,
        )?;
        Ok(Self::new(Class::Tool, spec.launch, waits, None))
    }
}

impl<P: Participant> Supervision<P> {
    /// A prepared supervision (`Prepared`, :425): nothing is spawned.
    pub fn prepare(spec: SessionSpec, participant: P) -> Result<Self, SupervisorError> {
        Self::prepare_with(spec, participant, Waits::RELEASE)
    }
    fn prepare_with(
        spec: SessionSpec,
        participant: P,
        waits: Waits,
    ) -> Result<Self, SupervisorError> {
        admit_spec(
            &spec.launch,
            DescriptorSet::Provider,
            spec.needs_d3b_ladders,
            spec.memory_budget_bytes,
        )?;
        let control = ControlSession::new(ControlContext::for_session(&spec.selection));
        let bound = control.policy().frame_bound();
        let protocol = participant.protocol_waits();
        let protocol_kind = participant.protocol();
        Ok(Self::new(
            Class::Provider,
            spec.launch,
            waits,
            Some(Provider {
                selection: spec.selection,
                participant,
                protocol,
                protocol_kind,
                control,
                reader: ControlReader::new(bound),
            }),
        ))
    }
    /// One supervision's starting state, nothing spawned.
    fn new(
        class: Class,
        launch: VerifiedLaunch,
        waits: Waits,
        provider: Option<Provider<P>>,
    ) -> Self {
        let limits = Limits::RELEASE;
        let (selection, participant, protocol, protocol_kind, control, reader) = match provider {
            Some(p) => (
                Some(p.selection),
                Some(p.participant),
                Some(p.protocol),
                Some(p.protocol_kind),
                Some(p.control),
                Some(p.reader),
            ),
            None => (None, None, None, None, None, None),
        };
        let tool = (class == Class::Tool).then(|| ToolCapture {
            buf: vec![0; TOOL_READ_BUFFER].into_boxed_slice(),
            output: Vec::new(),
            accounting: ToolOutput::with_limit(limits.tool_output),
            bound: None,
        });
        Self {
            state: State::Prepared,
            class,
            launch: Some(launch),
            selection,
            participant,
            waits,
            protocol,
            child: None,
            ends: HostEnds::default(),
            control,
            reader,
            tool,
            control_out: PendingWrite::default(),
            close_fd3_after_write: false,
            host_seq: 1,
            nonce_seq: 0,
            stderr_buf: [0; STDERR_BUFFER],
            stderr: StderrCount::default(),
            gate: Arc::new(TriggerGate::new()),
            observer: None,
            facts: None,
            spawned_pid: None,
            transfer_started: None,
            transfer_ended: None,
            ready_recorded: false,
            last_incomplete: None,
            events: 0,
            spawned_at: None,
            last_progress: None,
            next_health: None,
            health_due: None,
            terminal_at: None,
            exit_at: None,
            terminal: None,
            participant_status: ParticipantStatus::Running,
            fd1_eof: false,
            held_eof: false,
            eof_delivered: false,
            shutdown_ack: false,
            exit: None,
            death_appended: false,
            reaped: None,
            first_cause: None,
            later_causes: Vec::new(),
            ladder: None,
            grace_expired: false,
            tree: TreeReport::NotKilled,
            settlement: None,
            limits,
            protocol_kind,
            next_sample: None,
            asserted_resident: None,
            memory_breached: false,
            count_breached: false,
            response_bytes: 0,
            response_breached: false,
            control_refused: false,
            clean_at: None,
            deferred: None,
            exit_independent: false,
            tree_confirmed: None,
            #[cfg(test)]
            seams: tests::Seams::default(),
        }
    }

    pub fn state(&self) -> State {
        self.state
    }
    /// The protocol waits in force: the participant's own (LD-D3A-7). A
    /// tool has none.
    pub fn protocol_waits(&self) -> Option<ProtocolWaits> {
        self.protocol
    }
    /// The cross-thread trigger channel (LD-D3A-5).
    pub fn handle(&self) -> SupervisionHandle {
        SupervisionHandle {
            gate: Arc::clone(&self.gate),
        }
    }
    /// Triggers that arrived after settlement, counted and dropped (r2,
    /// NBO-1).
    pub fn late_events(&self) -> u64 {
        self.gate.late()
    }
    /// How many events the merged order has appended.
    pub fn event_count(&self) -> u64 {
        self.events
    }
    /// The settlement, by value, once (LD-D3A-5).
    pub fn take_settlement(&mut self) -> Option<Settlement> {
        self.settlement.take()
    }

    /// D4's pre-spawn refusals (item 12, :425): the supervision is consumed
    /// with nothing spawned, and no settlement exists (r2, RF-5).
    pub fn decline(self, refusal: PreSpawnRefusal) -> RunError {
        RunError::Declined(refusal)
    }

    /// Spawn and supervise the child to its one settlement, which
    /// [`take_settlement`](Self::take_settlement) then hands out. A spawn
    /// failure is an error, with no settlement (r2, RF-5).
    pub fn run(&mut self, root: &mut ScratchRoot) -> Result<(), RunError> {
        self.start(root)?;
        while self.state != State::Settled {
            self.turn();
        }
        Ok(())
    }

    fn append(&mut self, event: SupervisionEvent) {
        self.events = self.events.saturating_add(1);
        if let Some(observer) = &mut self.observer {
            observer(&event);
        }
        // Item 21's records of the events whose values the event holds.
        let fact = match event {
            SupervisionEvent::WaitExpired(wait) => Some(records::RecordFact::WaitExpired {
                wait: records::bounded_wait(wait),
                limit: self.wait_limit(wait),
            }),
            SupervisionEvent::TeardownStarted(cause) => {
                Some(records::RecordFact::TeardownStarted {
                    cause: records::teardown_cause(cause),
                })
            }
            SupervisionEvent::LivenessMissed(miss) => {
                let (miss, refusal_family) = records::liveness_miss(miss);
                Some(records::RecordFact::LivenessMissed {
                    window: self.waits.liveness_window,
                    miss,
                    refusal_family,
                })
            }
            _ => None,
        };
        if let Some(fact) = fact {
            self.fact(fact);
        }
    }

    /// Hand one record fact to the caller's sink (LD-D3A3-1).
    /// A tool's facts are its Project-only `tool.*` records (D3A3-R1-RF-1).
    fn fact(&mut self, fact: records::RecordFact) {
        let fact = match self.class {
            Class::Provider => Some(fact),
            Class::Tool => fact.for_tool(),
        };
        if let (Some(sink), Some(fact)) = (&mut self.facts, fact) {
            sink(fact);
        }
    }

    /// The caller's record sink (LD-D3A3-1): every record fact of this
    /// supervision, as it happens, including the unwind's.
    pub fn record_facts(&mut self, sink: FactSink) {
        self.facts = Some(sink);
    }

    /// A bounded wait's configured bound (`supervision.wait.expired`'s
    /// `limit`, SOP2:890).
    fn wait_limit(&self, wait: BoundedWait) -> Duration {
        let grace = self
            .protocol
            .map_or(Duration::ZERO, |p| p.normal_exit_grace);
        match wait {
            BoundedWait::Handshake => self.waits.handshake,
            BoundedWait::LivenessWindow => self.waits.liveness_window,
            BoundedWait::ProgressAbsent => self.waits.progress_absent_interval,
            BoundedWait::WallClock => self.waits.wall_clock,
            BoundedWait::NormalExitGrace | BoundedWait::ShutdownAck => grace,
            BoundedWait::TermToKill => self.waits.term_to_kill,
            BoundedWait::ReapCeiling => self.waits.reap_ceiling,
            BoundedWait::Drain => self.waits.drain,
        }
    }

    /// An item 16 bound breached, with the value observed in its unit.
    fn breached(&mut self, kind: LimitKind, observed: u64) {
        self.append(SupervisionEvent::LimitBreached(kind));
        let (limit, unit) = records::limit(kind);
        self.fact(records::RecordFact::LimitBreached {
            limit,
            observed,
            unit,
        });
    }

    /// `Prepared` to `Spawning` to `Handshaking`; a spawn failure returns
    /// the supervision to nothing spawned.
    fn start(&mut self, root: &mut ScratchRoot) -> Result<(), RunError> {
        if self.state != State::Prepared {
            return Err(RunError::AlreadyRun);
        }
        self.state = State::Spawning;
        let Some(launch) = self.launch.take() else {
            return Err(RunError::AlreadyRun);
        };
        let mut child = match spawn(launch, root) {
            Ok(child) => child,
            Err(error) => return Err(RunError::SpawnFailed(error)),
        };
        let now = Instant::now();
        self.spawned_at = Some(now);
        self.next_sample = Some(now);
        self.append(SupervisionEvent::Spawned {
            process_id: child.process_id(),
        });
        let raw_pid = child.process_id() as u32;
        self.spawned_pid = Some(raw_pid);
        let fact = match self.protocol_kind {
            Some(protocol) => records::RecordFact::ProcessSpawned {
                protocol: records::protocol_major(protocol),
                raw_pid,
            },
            None => records::RecordFact::ToolSpawned { raw_pid },
        };
        self.fact(fact);
        self.ends = HostEnds {
            fd0: child.take_host_end(0),
            fd1: child.take_host_end(1),
            fd2: child.take_host_end(2),
            fd3: child.take_host_end(3),
            fd4: child.take_host_end(4),
        };
        #[cfg(test)]
        {
            self.seams.scratch = self.child_scratch_path(&child);
            // An always-ready stderr that never ends (r2, RF-1's control).
            if self.seams.stderr_zero {
                self.ends.fd2 = File::open("/dev/zero").ok();
            }
        }
        self.child = Some(child);
        if self.class == Class::Tool {
            // No control plane: a tool skips `Handshaking` (:434). Its fd0
            // is already at EOF (item 5, :274).
            self.state = State::Running;
            self.append(SupervisionEvent::Running);
            return Ok(());
        }
        self.state = State::Handshaking;
        // The host's hello (item 9), through the session only.
        if let Some(hello) = self.host_message(host_hello) {
            let sent = self.send_control(&hello);
            if let Some(control) = &mut self.control {
                control.observations_mut().hello_seen = sent;
            }
        }
        Ok(())
    }

    #[cfg(test)]
    fn child_scratch_path(&self, child: &Child) -> Option<std::path::PathBuf> {
        child.scratch().map(|s| s.path().to_path_buf())
    }

    /// The next host sequence's message, built by `make`.
    fn host_message(
        &mut self,
        make: impl FnOnce(&AdmittedSelection, NonZeroU64) -> Option<Control3Root>,
    ) -> Option<Control3Root> {
        make(self.selection.as_ref()?, NonZeroU64::new(self.host_seq)?)
    }
    /// Send a host control frame through `ControlSession::send` (D2a r2),
    /// queued for fd3. False when the session refuses it or fd3 is closed.
    fn send_control(&mut self, message: &Control3Root) -> bool {
        if self.ends.fd3.is_none() || !self.control_out.bytes.is_empty() {
            return false;
        }
        let Some(control) = &mut self.control else {
            return false;
        };
        match control.send(message) {
            Ok(frame) => {
                self.host_seq += 1;
                self.control_out = PendingWrite {
                    bytes: frame,
                    at: 0,
                    written: None,
                };
                self.append(SupervisionEvent::ControlSent(message_type(message)));
                true
            }
            Err(_) => false,
        }
    }

    /// One turn of the readiness loop: triggers, timers, one wait, then the
    /// ready descriptors in a fixed order, the participant at most once
    /// each way (the yield contract), then teardown, reap and settlement.
    fn turn(&mut self) {
        if self.state == State::Settled {
            // The gate is closed: a late request was counted and dropped by
            // its refusal (LD-D3A-5; r3, RF-2).
            return;
        }
        for _ in 0..TRIGGER_CAPACITY {
            match self.gate.take() {
                Some(Trigger::HostFault) => self.trigger(Cause::HostFault),
                None => break,
            }
        }
        self.timers();
        if self.state == State::Settled {
            return;
        }
        self.wait_and_service();
        self.advance();
    }

    /// Fire every expired wait (item 14), each appending its event.
    fn timers(&mut self) {
        let now = Instant::now();
        let Some(spawned) = self.spawned_at else {
            return;
        };
        if let Some(at) = self.next_sample
            && now >= at
        {
            self.next_sample = Some(now + self.limits.memory_sample_interval);
            self.sample_tree();
        }
        if self.state == State::Handshaking && now >= spawned + self.waits.handshake {
            self.append(SupervisionEvent::WaitExpired(BoundedWait::Handshake));
            self.trigger(Cause::HandshakeDeadline);
        }
        if self.first_cause.is_none()
            && self.terminal.is_none()
            && now >= spawned + self.waits.wall_clock
        {
            // The cause first: the participant's resulting FAULT is a later
            // trigger, never the first.
            self.append(SupervisionEvent::WaitExpired(BoundedWait::WallClock));
            self.trigger(Cause::Deadline);
            self.deliver(ProcessEvent::Fault(ProcessFault::Deadline));
        }
        if self.state == State::Running && self.first_cause.is_none() {
            if let Some(due) = self.health_due
                && now >= due
            {
                self.health_due = None;
                self.append(SupervisionEvent::WaitExpired(BoundedWait::LivenessWindow));
                self.append(SupervisionEvent::LivenessMissed(
                    LivenessMiss::WindowExpired,
                ));
                self.trigger(Cause::Liveness);
            } else if self.health_due.is_none()
                && self.next_health.is_some_and(|at| now >= at)
                && self
                    .control
                    .as_ref()
                    .is_some_and(|c| c.state() == ControlState::Steady)
                && self.terminal.is_none()
            {
                self.send_health(now);
            }
            if self.terminal.is_none()
                && let Some(last) = self.last_progress
                && now >= last + self.waits.progress_absent_interval
            {
                self.last_progress = Some(now);
                self.append(SupervisionEvent::WaitExpired(BoundedWait::ProgressAbsent));
                self.append(SupervisionEvent::ProgressAbsent);
            }
        }
        // The normal end's grace (LD-D3A-15): the exit, EOF and shutdownAck
        // are owed within it.
        if let Some(at) = self.terminal_at
            && !self.grace_expired
            && self.first_cause.is_none()
            && let Some(protocol) = self.protocol
            && now >= at + protocol.normal_exit_grace
        {
            self.grace_expired = true;
            let done = self.participant_status == ParticipantStatus::Done;
            if !(done && self.shutdown_ack) {
                let wait = if done {
                    BoundedWait::ShutdownAck
                } else {
                    BoundedWait::NormalExitGrace
                };
                self.append(SupervisionEvent::WaitExpired(wait));
                self.trigger_from(Cause::Deadline, true);
                self.deliver(ProcessEvent::Fault(ProcessFault::Deadline));
            }
        }
        // The drain after death (J-3).
        if let Some(at) = self.exit_at
            && !self.death_appended
            && now >= at + self.waits.drain
        {
            self.append(SupervisionEvent::WaitExpired(BoundedWait::Drain));
            self.append_death();
        }
    }

    fn send_health(&mut self, now: Instant) {
        self.nonce_seq += 1;
        let nonce = format!("h{}", self.nonce_seq);
        let Ok(parsed) = nonce.parse() else {
            return;
        };
        let Some(seq) = NonZeroU64::new(self.host_seq) else {
            return;
        };
        let message = Control3Root::Health {
            body: Control3RootVariant8Property0 { nonce: parsed },
            control_major: NonZeroU64::MIN,
            seq,
        };
        let Some(control) = &mut self.control else {
            return;
        };
        control.observations_mut().pending_health_report = Some(nonce);
        if self.send_control(&message) {
            self.health_due = Some(now + self.waits.liveness_window);
            self.next_health = None;
        }
    }

    /// Item 16's sample of the live tree: its members (the process count)
    /// and their summed resident bytes (the ceiling), the asserted value
    /// beside the observed one. Either above the ceiling is a breach, and an
    /// asserted value below it never clears an observed one (:531). Sampled
    /// while the root runs, before any teardown.
    fn sample_tree(&mut self) {
        if self.exit.is_some() || self.reaped.is_some() || self.first_cause.is_some() {
            self.next_sample = None;
            return;
        }
        let Some(pid) = self.child.as_ref().map(|c| c.process_id()) else {
            return;
        };
        #[cfg(test)]
        let listing = if self.seams.listing_fails {
            Err(())
        } else {
            group_members(pid).map_err(|_| ())
        };
        #[cfg(not(test))]
        let listing = group_members(pid).map_err(|_| ());
        let Ok(members) = listing else {
            // The group could not be listed: nothing was sampled.
            self.sample_incomplete(0, 0, true);
            return;
        };
        #[cfg(test)]
        let count_on = !self.seams.process_count_off;
        #[cfg(not(test))]
        let count_on = true;
        // A provider's tree is one process, a tool's at most 16 (:533).
        let most = match self.class {
            Class::Provider => PROVIDER_PROCESSES,
            Class::Tool => TOOL_PROCESSES,
        };
        if count_on && !self.count_breached && members.len() > most {
            self.count_breached = true;
            self.breached(LimitKind::ProcessCount, members.len() as u64);
            self.trigger(Cause::ProcessCount);
            return;
        }
        // A member gone between the listing and its sample (`ESRCH`)
        // contributes nothing, lawfully. Any other failure leaves the sum
        // partial: it is disclosed as incomplete, never as a complete
        // observed sum (D3A2-R1-NBO-1). A partial sum over the ceiling is
        // still a breach: it is a lower bound.
        let mut observed = 0u64;
        let mut unsampled = 0u64;
        for member in &members {
            match self.resident(*member) {
                Ok(bytes) => observed = observed.saturating_add(bytes),
                Err(Some(ESRCH)) => {}
                Err(_) => unsampled += 1,
            }
        }
        if unsampled > 0 {
            self.sample_incomplete(members.len() as u64, unsampled, false);
        } else {
            self.last_incomplete = None;
        }
        let asserted = self.asserted_resident.unwrap_or(0);
        if observed > self.limits.resident_memory || asserted > self.limits.resident_memory {
            self.memory_breach(observed.max(asserted));
        }
    }
    /// One member's resident bytes, or the failing call's errno.
    fn resident(&self, member: i32) -> Result<u64, Option<i32>> {
        #[cfg(test)]
        if let Some(errno) = self.seams.sample_errno {
            return Err(Some(errno));
        }
        resident_bytes(member).map_err(|error| match error {
            LaunchError::Io { error, .. } => error.raw_os_error(),
            _ => None,
        })
    }
    /// An incomplete sample, recorded when its shape changes (so a
    /// persistent failure is one record, not one per interval).
    fn sample_incomplete(&mut self, listed: u64, unsampled: u64, listing_failed: bool) {
        let shape = (listed, unsampled, listing_failed);
        if self.last_incomplete == Some(shape) {
            return;
        }
        self.last_incomplete = Some(shape);
        self.append(SupervisionEvent::SampleIncomplete);
        self.fact(records::RecordFact::SampleIncomplete {
            listed,
            unsampled,
            listing_failed,
        });
    }
    fn memory_breach(&mut self, observed: u64) {
        if self.memory_breached {
            return;
        }
        self.memory_breached = true;
        self.breached(LimitKind::ResidentMemory, observed);
        self.trigger(Cause::MemoryCeiling);
    }

    /// The earliest pending deadline, for the wait's timeout.
    fn next_deadline(&self) -> Option<Instant> {
        let mut all: Vec<Instant> = Vec::new();
        all.extend(self.next_sample);
        if let Some(spawned) = self.spawned_at {
            if self.state == State::Handshaking {
                all.push(spawned + self.waits.handshake);
            }
            if self.first_cause.is_none() && self.terminal.is_none() {
                all.push(spawned + self.waits.wall_clock);
            }
        }
        if self.state == State::Running && self.first_cause.is_none() {
            all.extend(self.health_due);
            if self.health_due.is_none() {
                all.extend(self.next_health);
            }
            if self.terminal.is_none() {
                all.extend(
                    self.last_progress
                        .map(|last| last + self.waits.progress_absent_interval),
                );
            }
        }
        if let Some(at) = self.terminal_at
            && !self.grace_expired
            && self.first_cause.is_none()
            && let Some(protocol) = self.protocol
        {
            all.push(at + protocol.normal_exit_grace);
        }
        if let Some(at) = self.exit_at
            && !self.death_appended
        {
            all.push(at + self.waits.drain);
        }
        if let Some(ladder) = self.ladder {
            if let Some(term) = ladder.term_at
                && ladder.kill_at.is_none()
            {
                all.push(term + self.waits.term_to_kill);
            }
            if let Some(kill) = ladder.kill_at {
                all.push(kill + self.waits.reap_ceiling);
            }
        }
        all.extend(self.clean_at.map(|at| at + self.waits.reap_ceiling));
        all.into_iter().min()
    }

    fn wait_and_service(&mut self) {
        let running = matches!(
            self.state,
            State::Running | State::Stopping(_) | State::Killing | State::Reaping
        ) && self.child.is_some();
        let data_open = matches!(
            self.state,
            State::Running | State::Stopping(_) | State::Killing | State::Reaping
        ) || self.terminal.is_some();
        let mut set = Vec::with_capacity(6);
        let mut slots = Vec::with_capacity(6);
        if let Some(fd) = &self.ends.fd4 {
            set.push(Readiness::new(fd.as_raw_fd(), true, false));
            slots.push(4);
        }
        if let Some(fd) = &self.ends.fd2 {
            set.push(Readiness::new(fd.as_raw_fd(), true, false));
            slots.push(2);
        }
        if data_open && let Some(fd) = &self.ends.fd1 {
            set.push(Readiness::new(fd.as_raw_fd(), true, false));
            slots.push(1);
        }
        if running
            && self.state == State::Running
            && self.participant.as_ref().is_some_and(|p| p.wants_write())
            && let Some(fd) = &self.ends.fd0
        {
            set.push(Readiness::new(fd.as_raw_fd(), false, true));
            slots.push(0);
        }
        if !self.control_out.bytes.is_empty()
            && let Some(fd) = &self.ends.fd3
        {
            set.push(Readiness::new(fd.as_raw_fd(), false, true));
            slots.push(3);
        }
        if self.exit.is_none()
            && let Some(child) = &self.child
            && self.reaped.is_none()
        {
            set.push(Readiness::new(child.exit_source(), true, false));
            slots.push(5);
        }
        let now = Instant::now();
        // Bounded: every wait is finite, and a turn with nothing pending
        // still samples at the ladder's own deadlines.
        let timeout = self
            .next_deadline()
            .map_or(Duration::from_millis(100), |at| {
                at.saturating_duration_since(now)
            })
            .min(Duration::from_millis(100));
        if wait_ready(&mut set, timeout).is_err() {
            self.trigger(Cause::HostFault);
            return;
        }
        let ready = |slot: usize| {
            slots
                .iter()
                .zip(&set)
                .any(|(s, r)| *s == slot && (r.readable || r.writable))
        };
        if ready(5) {
            self.observe_exit();
        }
        if ready(4) {
            self.service_control();
        }
        if ready(2) {
            self.service_stderr();
        }
        if ready(1) {
            #[cfg(test)]
            {
                self.seams.reads_this_turn += 1;
                self.seams.max_reads_per_turn = self
                    .seams
                    .max_reads_per_turn
                    .max(self.seams.reads_this_turn);
            }
            self.service_data_read();
        }
        #[cfg(test)]
        {
            self.seams.reads_this_turn = 0;
            self.seams.max_control_reads_per_turn = self
                .seams
                .max_control_reads_per_turn
                .max(self.seams.control_reads_this_turn);
            self.seams.max_stderr_reads_per_turn = self
                .seams
                .max_stderr_reads_per_turn
                .max(self.seams.stderr_reads_this_turn);
            self.seams.control_reads_this_turn = 0;
            self.seams.stderr_reads_this_turn = 0;
        }
        if ready(0) {
            self.service_data_write();
        }
        if ready(3) {
            self.service_control_write();
        }
    }

    fn observe_exit(&mut self) {
        let Some(child) = &self.child else {
            return;
        };
        if let Ok(Some(status)) = child.wait_exit(Duration::ZERO) {
            self.exit = Some(status);
            self.exit_at = Some(Instant::now());
            // Observed before the host signalled the group: the death is the
            // child's own, not the ladder's (r2, RF-8).
            self.exit_independent = self.ladder.is_none_or(|l| l.term_at.is_none());
            self.append(SupervisionEvent::ExitObserved);
            self.drained_check();
        }
    }

    /// The control channel: frames reassembled from any split, each decided
    /// by the session.
    fn service_control(&mut self) {
        let Some(bound) = self.control.as_ref().map(|c| c.policy().frame_bound()) else {
            return;
        };
        for _ in 0..CONTROL_READS_PER_TURN {
            #[cfg(test)]
            {
                self.seams.control_reads_this_turn += 1;
            }
            let (Some(fd), Some(reader)) = (&mut self.ends.fd4, &mut self.reader) else {
                return;
            };
            let read = match reader.read(fd, bound) {
                Ok(read) => read,
                Err(_) => {
                    self.trigger(Cause::HostFault);
                    return;
                }
            };
            match read {
                ControlRead::Pending => return,
                ControlRead::Eof(cut) => {
                    if cut {
                        // A frame cut short at EOF: the session refuses the
                        // partial frame as RF2.
                        let frame = reader.buf[..reader.have].to_vec();
                        self.receive_control(&frame);
                    }
                    self.ends.fd4 = None;
                    self.append(SupervisionEvent::ChannelEof(Channel::Control));
                    self.drained_check();
                    return;
                }
                ControlRead::OverBound => {
                    let prefix = reader.buf[..4].to_vec();
                    self.receive_control(&prefix);
                }
                ControlRead::Frame(len) => {
                    let frame = reader.buf[..len].to_vec();
                    self.receive_control(&frame);
                }
            }
            if self.state == State::Settled {
                return;
            }
        }
    }

    fn receive_control(&mut self, frame: &[u8]) {
        let Some(control) = &mut self.control else {
            return;
        };
        let step = control.receive(Direction::ComponentToHost, frame);
        match step.verdict {
            // The first refusal is the trigger; the direction is stopped
            // after it, and later frames are drained, never re-triggered.
            ControlVerdict::Refused(_) if self.control_refused => {}
            ControlVerdict::Refused(refused) => {
                self.control_refused = true;
                if refused.detail == Some(RefusalDetail::HealthNonceMismatch) {
                    // Item 15: a mismatched report is a liveness fault (r2,
                    // RF-6). The refused frame is not kept; the event carries
                    // its reduced provenance, the mismatch and the control
                    // owner's family (r3, NBO-1).
                    self.health_due = None;
                    self.append(SupervisionEvent::LivenessMissed(
                        LivenessMiss::NonceMismatch(refused.family),
                    ));
                    self.trigger(Cause::Liveness);
                } else {
                    self.trigger(Cause::ControlRefusal(refused.family));
                }
            }
            ControlVerdict::Accepted(accepted) => {
                self.append(SupervisionEvent::ControlReceived(accepted.message_type));
                match &accepted.message {
                    Control3Root::HelloAck { body, .. } => {
                        let confirmed = body
                            .subprotocol_confirms
                            .iter()
                            .map(|c| SubprotocolTuple {
                                role: c.role.as_str().to_owned(),
                                role_subprotocol: c.role_subprotocol.as_str().to_owned(),
                                subprotocol_version: c.subprotocol_version.get() as i64,
                            })
                            .collect();
                        if let Some(control) = &mut self.control {
                            control.observations_mut().confirmed_tuples = confirmed;
                        }
                        if let Some(select) = self.host_message(host_select) {
                            let tuple = self.selection.as_ref().map(|s| s.tuple.clone());
                            if let Some(control) = &mut self.control {
                                control.observations_mut().selected_tuple = tuple;
                            }
                            self.send_control(&select);
                        }
                    }
                    Control3Root::SelectAck { .. } if self.state == State::Handshaking => {
                        let now = Instant::now();
                        self.state = State::Running;
                        self.last_progress = Some(now);
                        self.next_health = Some(now + self.waits.health_ping_interval);
                        self.append(SupervisionEvent::Running);
                    }
                    Control3Root::HealthReport { .. } => {
                        // Live, whatever its status (item 15, :512).
                        if let Some(control) = &mut self.control {
                            control.observations_mut().pending_health_report = None;
                        }
                        self.health_due = None;
                        self.next_health = Some(Instant::now() + self.waits.health_ping_interval);
                        // A shutdown waiting for this report now goes.
                        self.send_deferred();
                    }
                    Control3Root::ShutdownAck { .. } => {
                        self.shutdown_ack = true;
                        self.check_clean();
                    }
                    Control3Root::Refusal { body, .. } => {
                        let family = accepted
                            .terminal_family
                            .as_deref()
                            .and_then(family_of)
                            .unwrap_or(RefusalFamily::Rf2);
                        // Its detail is reduced to its length (SOP2:839).
                        let detail_bytes = match &body.detail {
                            FieldPresence::Present(Some(detail)) => detail.len() as u64,
                            _ => 0,
                        };
                        self.fact(records::RecordFact::FaultReduced {
                            source: opensip_operability::FaultSource::ControlRefusal,
                            refusal_family: Some(records::refusal_family(family)),
                            detail_bytes,
                        });
                        self.trigger(Cause::ControlRefusal(family));
                    }
                    Control3Root::Fault { body, .. } => {
                        let detail_bytes = body.detail.len() as u64;
                        self.fact(records::RecordFact::FaultReduced {
                            source: opensip_operability::FaultSource::ControlFault,
                            refusal_family: None,
                            detail_bytes,
                        });
                        self.trigger(Cause::ProviderProtocol);
                    }
                    // Asserted, logged as asserted (SOP2:842), and compared
                    // with the ceiling (item 16, :530).
                    Control3Root::ResourceReport { body, .. } => {
                        let asserted = body.resident_bytes.max(0) as u64;
                        let cpu_nanos = body.cpu_nanoseconds.max(0) as u64;
                        let handles = body.open_handles.max(0) as u64;
                        self.fact(records::RecordFact::ResourcesReported {
                            resident: asserted,
                            cpu_nanos,
                            handles,
                        });
                        self.asserted_resident = Some(asserted);
                        if asserted > self.limits.resident_memory {
                            self.memory_breach(asserted);
                        }
                    }
                    _ => {}
                }
            }
        }
    }

    /// stderr (item 17): read continuously into the fixed buffer, counted,
    /// overwritten; never held.
    fn service_stderr(&mut self) {
        for _ in 0..STDERR_READS_PER_TURN {
            #[cfg(test)]
            {
                self.seams.stderr_reads_this_turn += 1;
            }
            let Some(fd) = &mut self.ends.fd2 else {
                return;
            };
            match fd.read(&mut self.stderr_buf) {
                Ok(0) => {
                    self.ends.fd2 = None;
                    self.append(SupervisionEvent::ChannelEof(Channel::Stderr));
                    self.drained_check();
                    return;
                }
                Ok(n) => {
                    self.stderr.bytes = self.stderr.bytes.saturating_add(n as u64);
                    self.stderr.truncated = self.stderr.bytes > STDERR_TRUNCATION_BYTES;
                }
                Err(e) if e.kind() == io::ErrorKind::Interrupted => {}
                Err(_) => return,
            }
        }
    }

    /// One participant read (the yield contract); a tool's output instead.
    fn service_data_read(&mut self) {
        if self.class == Class::Tool {
            self.service_tool_output();
            return;
        }
        let (Some(fd), Some(participant)) = (&mut self.ends.fd1, &mut self.participant) else {
            return;
        };
        let step = participant.readable(fd);
        if step.eof {
            self.ends.fd1 = None;
            self.fd1_eof = true;
            self.append(SupervisionEvent::ChannelEof(Channel::Data));
        }
        self.apply_step(step);
        if self.fd1_eof && !self.eof_delivered && !self.held_eof {
            if self.terminal.is_some()
                && self.participant_status != ParticipantStatus::Fault
                && !self.death_appended
            {
                // Item 13: EOF after the terminal is held for the exit.
                self.held_eof = true;
            } else {
                // Before the terminal (item 13), or after the death was
                // already appended: delivered at once.
                self.eof_delivered = true;
                self.deliver(ProcessEvent::Eof);
            }
        }
        self.drained_check();
    }

    /// One participant write (the yield contract).
    fn service_data_write(&mut self) {
        let (Some(fd), Some(participant)) = (&mut self.ends.fd0, &mut self.participant) else {
            return;
        };
        let step = participant.writable(fd);
        self.apply_step(step);
    }

    /// A tool's fd1 (item 5, :274): a bounded number of reads into the fixed
    /// buffer, each read's bytes charged to the output bound before they are
    /// kept (item 16, :548). Past the bound the refusal is recorded, nothing
    /// more is kept, fd1 is closed and `byte-bound(tool-output)` starts the
    /// ladder. EOF is the tool's end of output; its death is then expected.
    fn service_tool_output(&mut self) {
        for _ in 0..TOOL_READS_PER_TURN {
            let (Some(fd), Some(tool)) = (&mut self.ends.fd1, &mut self.tool) else {
                return;
            };
            match fd.read(&mut tool.buf) {
                Ok(0) => {
                    self.ends.fd1 = None;
                    self.fd1_eof = true;
                    self.append(SupervisionEvent::ChannelEof(Channel::Data));
                    self.drained_check();
                    return;
                }
                Ok(n) => match tool.accounting.charge(n as u64) {
                    Ok(()) => tool.output.extend_from_slice(&tool.buf[..n]),
                    Err(bound) => {
                        tool.bound = Some(bound);
                        self.ends.fd1 = None;
                        self.breached(LimitKind::ToolOutput, bound.observed);
                        self.trigger(Cause::ByteBound(ByteBound::ToolOutput));
                        self.drained_check();
                        return;
                    }
                },
                Err(e) if e.kind() == io::ErrorKind::Interrupted => {}
                Err(_) => return,
            }
        }
    }

    fn service_control_write(&mut self) {
        #[cfg(test)]
        if (self.seams.stall_control_writes_in_running
            && self.state == State::Running
            && self.terminal.is_none())
            || self.seams.stall_control_writes
            || self.seams.control_bytes_left == Some(0)
        {
            return;
        }
        let Some(fd) = &mut self.ends.fd3 else {
            return;
        };
        let pending = &mut self.control_out;
        #[cfg(test)]
        let end = self
            .seams
            .control_write_chunk
            .map_or(pending.bytes.len(), |n| {
                (pending.at + n).min(pending.bytes.len())
            })
            .min(
                self.seams
                    .control_bytes_left
                    .map_or(usize::MAX, |left| pending.at + left),
            );
        #[cfg(not(test))]
        let end = pending.bytes.len();
        #[cfg(test)]
        let result = if self.seams.control_write_fails {
            Err(io::Error::from_raw_os_error(32))
        } else {
            fd.write(&pending.bytes[pending.at..end])
        };
        #[cfg(not(test))]
        let result = fd.write(&pending.bytes[pending.at..end]);
        match result {
            Ok(n) => {
                pending.at += n;
                #[cfg(test)]
                if let Some(left) = &mut self.seams.control_bytes_left {
                    *left -= n;
                }
            }
            Err(e)
                if matches!(
                    e.kind(),
                    io::ErrorKind::WouldBlock | io::ErrorKind::Interrupted
                ) => {}
            Err(_) => {
                // The child's control reader is gone: nothing more is sent.
                self.control_out = PendingWrite::default();
                self.ends.fd3 = None;
                return;
            }
        }
        if self.control_out.at == self.control_out.bytes.len() {
            // The frame is written whole: its record, if any, is made now.
            if let Some(fact) = std::mem::take(&mut self.control_out).written {
                self.fact(fact);
            }
            if self.close_fd3_after_write {
                // The normal end closes the protocol (DLV:567), only once
                // its shutdown itself is written.
                self.ends.fd3 = None;
                return;
            }
            self.send_deferred();
        }
    }

    /// Send the deferred host frame once fd3 is free (r2, RF-4), through
    /// `ControlSession::send` only, with the session's next sequence.
    fn send_deferred(&mut self) {
        if !self.control_out.bytes.is_empty() || self.ends.fd3.is_none() {
            return;
        }
        if self.deferred == Some(Deferred::Shutdown)
            && self
                .control
                .as_mut()
                .is_some_and(|c| c.observations_mut().pending_health_report.is_some())
        {
            return;
        }
        let Some(deferred) = self.deferred.take() else {
            return;
        };
        let Some(seq) = NonZeroU64::new(self.host_seq) else {
            return;
        };
        let message = match deferred {
            Deferred::Shutdown => Control3Root::Shutdown {
                body: Control3RootVariant14Property0 {
                    reason: ShutdownReason::Normal,
                },
                control_major: NonZeroU64::MIN,
                seq,
            },
            Deferred::Cancel(reason) => Control3Root::Cancel {
                body: Control3RootVariant7Property0 { reason },
                control_major: NonZeroU64::MIN,
                seq,
            },
        };
        let sent = self.send_control(&message);
        if let (true, Deferred::Cancel(reason)) = (sent, deferred) {
            // Recorded once the frame is written whole (D3A3-R1-RF-2).
            self.control_out.written = Some(records::RecordFact::CancelSent {
                control_reason: match reason {
                    CancelReason::User => opensip_operability::ControlCancelReason::User,
                    CancelReason::Deadline => opensip_operability::ControlCancelReason::Deadline,
                    CancelReason::SupervisorFault => {
                        opensip_operability::ControlCancelReason::SupervisorFault
                    }
                },
            });
        }
        if deferred == Deferred::Shutdown {
            if sent {
                self.close_fd3_after_write = true;
            } else {
                // The session refused it: the protocol still closes.
                self.ends.fd3 = None;
            }
        }
    }

    /// Deliver a process event to the participant and apply its step.
    fn deliver(&mut self, event: ProcessEvent) {
        if self.state == State::Settled {
            return;
        }
        let Some(participant) = &mut self.participant else {
            return;
        };
        let step = participant.process(event);
        self.append(SupervisionEvent::Delivered(event));
        self.apply_step(step);
    }

    fn apply_step(&mut self, step: ParticipantStep) {
        for progress in &step.progress {
            self.last_progress = Some(Instant::now());
            self.append(SupervisionEvent::Progress(*progress));
        }
        // TS2's aggregate response bound, from the participant's typed
        // accounting (item 16, :544; LD-D3A-3). Rust3's totals are its own
        // limits, which its codec enforces (D2b).
        if self.protocol_kind == Some(Protocol::Ts2) {
            self.response_bytes = self
                .response_bytes
                .saturating_add(step.admitted_payload_bytes);
            if !self.response_breached && self.response_bytes > self.limits.ts2_response {
                self.response_breached = true;
                self.breached(LimitKind::Response, self.response_bytes);
                self.trigger(Cause::ByteBound(ByteBound::Response));
            }
        }
        for boundary in &step.boundaries {
            self.boundary(*boundary);
        }
        let before = self.participant_status;
        self.participant_status = step.status;
        match step.status {
            ParticipantStatus::Terminal(kind) if self.terminal.is_none() => {
                self.reach_terminal(kind);
            }
            // The transition into FAULT is the trigger, once.
            ParticipantStatus::Fault if before != ParticipantStatus::Fault => {
                self.trigger(Cause::ProviderProtocol);
            }
            ParticipantStatus::HostFault if before != ParticipantStatus::HostFault => {
                self.trigger(Cause::HostFault);
            }
            ParticipantStatus::Done => self.check_clean(),
            _ => {}
        }
    }

    /// M3-L r1:400's spans: `provider.process.ready` once, at the context's
    /// verification, with the transfer sub-span if the participant marked
    /// one (none transferred is a zero span).
    fn boundary(&mut self, boundary: Boundary) {
        let now = Instant::now();
        match boundary {
            Boundary::TransferStarted => self.transfer_started = Some(now),
            Boundary::TransferEnded => self.transfer_ended = Some(now),
            Boundary::ContextVerified if !self.ready_recorded => {
                self.ready_recorded = true;
                let start = self
                    .spawned_at
                    .map_or(Duration::ZERO, |at| now.saturating_duration_since(at));
                let transfer = match (self.transfer_started, self.transfer_ended) {
                    (Some(from), Some(to)) => to.saturating_duration_since(from),
                    _ => Duration::ZERO,
                };
                self.fact(records::RecordFact::ProcessReady { start, transfer });
            }
            Boundary::ContextVerified => {}
        }
    }

    /// The normal end begins (LD-D3A-15): `shutdown {reason: normal}`, the
    /// participant's input closed, fd3 closed once the shutdown is written,
    /// then the exit, EOF and `shutdownAck` within the normal-exit grace.
    fn reach_terminal(&mut self, kind: TerminalKind) {
        self.terminal = Some(kind);
        self.append(SupervisionEvent::Terminal(kind));
        if self.first_cause.is_some() {
            return;
        }
        self.terminal_at = Some(Instant::now());
        // A health exchange already in flight keeps its liveness window; no
        // new one starts after the terminal.
        if self
            .control
            .as_mut()
            .is_none_or(|c| c.observations_mut().pending_health_report.is_none())
        {
            self.health_due = None;
        }
        // The shutdown is tracked until it is written: if an older frame is
        // still pending, or a health report is owed, it goes once that frame
        // completes and the report arrives, so the report is not refused in
        // TEARDOWN (r2, RF-4).
        self.deferred = Some(Deferred::Shutdown);
        self.send_deferred();
        if let Some(participant) = &mut self.participant {
            participant.close_input();
        }
        self.ends.fd0 = None;
    }

    /// J-3: the death is appended once every channel reached EOF.
    fn drained_check(&mut self) {
        if self.exit.is_some()
            && !self.death_appended
            && self.ends.fd1.is_none()
            && self.ends.fd2.is_none()
            && self.ends.fd4.is_none()
        {
            self.append_death();
        }
    }

    /// The death event (item 13): the exit as the protocols name it, then
    /// the held EOF. A death before the terminal is `unexpected-exit`.
    fn append_death(&mut self) {
        if self.death_appended {
            return;
        }
        self.death_appended = true;
        let Some(status) = self.exit else {
            return;
        };
        let event = match (status.code(), status.signal()) {
            (Some(0), _) => ProcessEvent::ZeroExit,
            (_, Some(_)) => ProcessEvent::Fault(ProcessFault::SignalDeath),
            _ => ProcessEvent::Fault(ProcessFault::NonzeroExit),
        };
        // A death before the terminal that the host did not cause is
        // `unexpected-exit`: first, or appended after an earlier trigger
        // (r2, RF-8). A death the ladder caused is only its protocol event.
        // A tool has no terminal: its end of output is fd1's EOF, so its
        // death is unexpected only with fd1 still open at the drain's
        // expiry (LD-D3A2-2).
        let ended = match self.class {
            Class::Provider => self.terminal.is_some(),
            Class::Tool => self.fd1_eof || self.tool.as_ref().is_some_and(|t| t.bound.is_some()),
        };
        if !ended && self.exit_independent {
            self.trigger(Cause::UnexpectedExit);
        }
        self.deliver(event);
        if self.held_eof && !self.eof_delivered {
            self.eof_delivered = true;
            self.deliver(ProcessEvent::Eof);
        }
        if self.state != State::Settled
            && let State::Stopping(_) | State::Killing = self.state
        {
            self.state = State::Reaping;
        }
        self.check_clean();
    }

    /// A clean end: the participant at DONE, the `shutdownAck`, every
    /// channel at EOF and the death appended, with no cause. A tool's: its
    /// output at EOF and its death appended, with no cause, whatever its
    /// exit; a failed exit is MC item 12's to route (LD-D3A2-2).
    fn check_clean(&mut self) {
        let ended = match self.class {
            Class::Provider => {
                self.participant_status == ParticipantStatus::Done && self.shutdown_ack
            }
            Class::Tool => self.fd1_eof,
        };
        if self.first_cause.is_none() && ended && self.death_appended {
            self.first_cause = Some(Cause::Clean);
            self.clean_at = Some(Instant::now());
            self.state = State::Reaping;
        }
    }

    /// Append a teardown trigger (item 12, :447): the first starts the
    /// ladder; a later one is kept.
    fn trigger(&mut self, cause: Cause) {
        self.trigger_from(cause, false);
    }
    fn trigger_from(&mut self, cause: Cause, from_t2: bool) {
        if self.state == State::Settled {
            self.append(SupervisionEvent::LateEvent);
            return;
        }
        self.append(SupervisionEvent::Trigger(cause));
        match self.first_cause {
            None => {
                self.first_cause = Some(cause);
                self.append(SupervisionEvent::TeardownStarted(cause));
                if self.child.is_some() {
                    self.state = if self.death_appended {
                        State::Reaping
                    } else {
                        State::Stopping(cause)
                    };
                    // A tool has no control plane, so no T-1 (LD-D3A2-1).
                    self.ladder = Some(Ladder {
                        t1_done: from_t2 || self.class == Class::Tool,
                        term_at: None,
                        kill_at: None,
                    });
                }
            }
            // Kept, each cause once: the closed set bounds what is retained
            // (item 12, :448); every trigger is still appended to the order.
            Some(_) if !self.later_causes.contains(&cause) => self.later_causes.push(cause),
            Some(_) => {}
        }
    }

    /// Teardown, reap and settlement, as far as they can go this turn.
    fn advance(&mut self) {
        if self.state == State::Settled || self.first_cause.is_none() {
            return;
        }
        if self.ladder.is_some() {
            self.ladder_step();
        }
        if self.state == State::Settled {
            return;
        }
        self.reap_step();
    }

    /// LD-D3A-6's ladder: T-1 control cancel, T-2 SIGTERM at once, T-3
    /// SIGKILL after the escalation (sooner if the zombie root is alone).
    fn ladder_step(&mut self) {
        let Some(mut ladder) = self.ladder else {
            return;
        };
        let now = Instant::now();
        if !ladder.t1_done {
            ladder.t1_done = true;
            self.append(SupervisionEvent::CancelAttempted);
            let reason = if self.first_cause == Some(Cause::Deadline) {
                CancelReason::Deadline
            } else {
                CancelReason::SupervisorFault
            };
            // Sent once any pending frame completes; T-2 does not wait.
            self.deferred = Some(Deferred::Cancel(reason));
            self.send_deferred();
        }
        let unreaped = self.reaped.is_none();
        if ladder.term_at.is_none() {
            ladder.term_at = Some(now);
            if unreaped && self.signal(SIGTERM) {
                self.append(SupervisionEvent::Signalled { signal: SIGTERM });
            }
        }
        if ladder.kill_at.is_none()
            && let Some(term) = ladder.term_at
        {
            let alone = self.exit.is_some() && self.root_alone();
            if now >= term + self.waits.term_to_kill || alone {
                if now >= term + self.waits.term_to_kill && !alone {
                    self.append(SupervisionEvent::WaitExpired(BoundedWait::TermToKill));
                }
                ladder.kill_at = Some(now);
                if unreaped && self.signal(SIGKILL) {
                    self.append(SupervisionEvent::Signalled { signal: SIGKILL });
                }
                if !self.death_appended {
                    self.state = State::Killing;
                }
            }
        }
        self.ladder = Some(ladder);
    }

    /// Signal the child's group, while its root is unreaped (item 4's
    /// reap-last rule is the platform's).
    fn signal(&self, signal: i32) -> bool {
        self.child
            .as_ref()
            .is_some_and(|child| child.signal_group(signal).is_ok())
    }

    /// Item 18's confirmation, D3a's part (:595; LD-D3A-6): the killed group
    /// lists the zombie root alone, or it is incomplete.
    fn confirm_tree(&self) -> TreeReport {
        #[cfg(test)]
        if self.seams.extra_member {
            return TreeReport::Incomplete;
        }
        if self.root_alone() {
            TreeReport::GroupKilledPlatformLimited
        } else {
            TreeReport::Incomplete
        }
    }

    /// Whether the group lists the zombie root alone (item 18's confirm
    /// rule, :595, D3a's part).
    fn root_alone(&self) -> bool {
        let Some(child) = &self.child else {
            return true;
        };
        let pid = child.process_id();
        matches!(group_members(pid).as_deref(), Ok([only]) if *only == pid)
    }

    /// The reap (T-5): non-blocking after the death, abandoning at the
    /// ceiling; then the settlement.
    fn reap_step(&mut self) {
        let ladder_done = self.ladder.is_none_or(|l| l.kill_at.is_some())
            || self.first_cause == Some(Cause::Clean);
        if self.death_appended && ladder_done && self.try_reap() {
            self.settle();
            return;
        }
        // The ceiling runs from the KILL, or for a clean end from its join
        // (r2, RF-2); at it the root is abandoned, never signalled again.
        let since = self.ladder.and_then(|l| l.kill_at).or(self.clean_at);
        if let Some(at) = since
            && Instant::now() >= at + self.waits.reap_ceiling
        {
            self.append(SupervisionEvent::WaitExpired(BoundedWait::ReapCeiling));
            self.settle();
        }
    }

    /// `Child::try_reap` (D3a-0), never blocking.
    fn try_reap(&mut self) -> bool {
        #[cfg(test)]
        if self.seams.reap_blocked {
            return false;
        }
        // The group is confirmed against the still-unreaped root, before the
        // reap that would empty it (r2, RF-9).
        if self.ladder.is_some_and(|l| l.kill_at.is_some()) && self.reaped.is_none() {
            self.tree_confirmed = Some(self.confirm_tree());
        }
        let Some(child) = &mut self.child else {
            return true;
        };
        if child.is_reaped() {
            return true;
        }
        match child.try_reap() {
            Ok(Some(reaped)) => {
                self.reaped = Some(reaped);
                self.append(SupervisionEvent::Reaped);
                true
            }
            _ => false,
        }
    }

    /// The one transition into `Settled` (LD-D3A-5): the tree report, the
    /// scratch's removal, the terminal's output, and the one settlement.
    fn settle(&mut self) {
        if self.state == State::Settled {
            return;
        }
        let mut cause = self.first_cause.unwrap_or(Cause::Abandoned);
        let killed = self.ladder.is_some_and(|l| l.kill_at.is_some());
        self.tree = if !killed {
            TreeReport::NotKilled
        } else {
            // Captured before the reap; an unreaped root is confirmed now,
            // still held (r2, RF-9). A reaped root is never confirmed by pid
            // after its reap: without a capture it is incomplete (r3, RF-1).
            match self.tree_confirmed {
                Some(tree) => tree,
                None if self.reaped.is_none() => self.confirm_tree(),
                None => TreeReport::Incomplete,
            }
        };
        // Only a spawned child is settled (r2, RF-5).
        let Some(mut child) = self.child.take() else {
            return;
        };
        let reaped = self.reaped.filter(|_| child.is_reaped());
        let (exit, scratch) = match reaped {
            Some(reaped) => {
                // A spawned child's scratch stays attached until here; if it
                // were gone, nothing would be left to remove.
                let fate = match child.take_scratch() {
                    Some(dir) => {
                        // Item 16: an exact bounded walk before removal; past
                        // the limit, or at the ledger's exhaustion, is
                        // `scratch-bound` (LD-D3A-12), which a clean end
                        // becomes (DRJ2:125). A provider's only: a tool's
                        // materialization is charged before each write, and
                        // the provider walk never stands in for it
                        // (LD-D3A-16).
                        if let Some(over) = self.scratch_over(&dir) {
                            match over {
                                Some(observed) => self.breached(LimitKind::Scratch, observed),
                                // Exhausted or failed: no observed value
                                // exists, so only the event and the cause
                                // record it (LD-D3A3-6).
                                None => {
                                    self.append(SupervisionEvent::LimitBreached(LimitKind::Scratch))
                                }
                            }
                            if cause == Cause::Clean {
                                cause = Cause::ScratchBound;
                            } else if !self.later_causes.contains(&Cause::ScratchBound) {
                                self.later_causes.push(Cause::ScratchBound);
                            }
                        }
                        self.remove_scratch(dir)
                    }
                    None => ScratchFate::Removed,
                };
                drop(child);
                (exit_class(reaped.status), fate)
            }
            None => {
                // The root may still run in its scratch: both are held for
                // the process's life (LD-D3A-18).
                drop(child.abandon());
                self.append(SupervisionEvent::Abandoned);
                (
                    ExitClass::Unreaped,
                    ScratchFate::Retained(ScratchRetained::RootUnreaped),
                )
            }
        };
        self.ends = HostEnds::default();
        let output = self
            .participant
            .as_mut()
            .and_then(|p| p.take_terminal_output());
        let tool = self.tool.take().map(|t| ToolResult {
            output: Some(t.output),
            bound: t.bound,
        });
        let settlement = Settlement {
            first_cause: cause,
            later_causes: std::mem::take(&mut self.later_causes),
            user_interrupted: false,
            exit,
            tree: self.tree,
            stderr: self.stderr,
            rusage: self.reaped.map(|r| Rusage {
                user_micros: r.user_micros,
                system_micros: r.system_micros,
                max_rss_bytes: r.max_resident_bytes,
            }),
            scratch,
            terminal: self.terminal,
            eof_observed: self.fd1_eof,
            output,
            tool,
        };
        // Item 20: a settlement that is not admissible discards every
        // candidate the participant still spools; its terminal output, if
        // any, is dropped by the gate (`Settlement::release`).
        let admissible = settlement.admissible();
        if !admissible && let Some(participant) = &mut self.participant {
            participant.discard();
        }
        self.settle_records(&settlement, admissible);
        self.state = State::Settled;
        self.settlement = Some(settlement);
        self.append(SupervisionEvent::Settled(cause));
        // Admission closes with the drain, in one section (r3, RF-2): later
        // requests are refused and counted by the gate, and any admitted
        // before the close are counted here.
        for _ in 0..self.gate.close() {
            self.append(SupervisionEvent::LateEvent);
        }
    }

    /// Item 21's settlement records: the stderr count, a retained scratch,
    /// a tool's reap, and the settlement itself.
    fn settle_records(&mut self, settlement: &Settlement, admissible: bool) {
        if self.class == Class::Provider {
            self.fact(records::RecordFact::StderrReduced {
                bytes: settlement.stderr.bytes,
                truncated: settlement.stderr.truncated,
            });
        }
        if let ScratchFate::Retained(retained) = settlement.scratch {
            let (reason, errno) = records::scratch_retained(retained);
            self.fact(records::RecordFact::ScratchRetained { reason, errno });
        }
        if self.class == Class::Tool
            && let (Some(reaped), Some(raw_pid)) = (self.reaped, self.spawned_pid)
        {
            self.fact(records::RecordFact::ToolReaped {
                raw_pid,
                exit: records::exit_class(settlement.exit),
                max_rss_bytes: reaped.max_resident_bytes,
                cpu: Duration::from_micros(reaped.user_micros.saturating_add(reaped.system_micros)),
            });
        }
        self.fact(records::RecordFact::Settled {
            cause: records::teardown_cause(settlement.first_cause),
            admissible,
            user_interrupted: settlement.user_interrupted,
        });
    }

    /// Item 16's measurement at settlement (LD-D3A-12): D3a-0's bounded walk
    /// on the discovery profile's ledger, stopping one past the protocol's
    /// limit. An I/O failure cannot show the scratch within its limit, so it
    /// counts as past it.
    ///
    /// `None` within the limit; `Some(Some(bytes))` past it, where the walk
    /// stopped; `Some(None)` when the walk could not show it within (its
    /// ledger exhausted, or an I/O failure). A tool's scratch is never
    /// walked here (LD-D3A-16).
    fn scratch_over(&mut self, dir: &opensip_platform::ChildScratch) -> Option<Option<u64>> {
        if self.class != Class::Provider {
            return None;
        }
        let limit = self.limits.scratch(self.protocol_kind?);
        #[cfg(test)]
        let mut ledger = match self.seams.measure_limits {
            Some(limits) => WorkLedger::with_limits(limits).unwrap_or_else(|_| WorkLedger::new()),
            None => WorkLedger::discovery_profile(),
        };
        #[cfg(not(test))]
        let mut ledger = WorkLedger::discovery_profile();
        match ledger.scope(|work| dir.measure(limit, work)) {
            Ok(bytes) if bytes <= limit => None,
            Ok(bytes) => Some(Some(bytes)),
            Err(_) => Some(None),
        }
    }

    /// Item 20's removal, within bounded work (LD-D3A-12: the discovery
    /// profile's caps), its failure retained (LD-D3A-17). The removal
    /// policy's records are D3a-3's.
    fn remove_scratch(&mut self, dir: opensip_platform::ChildScratch) -> ScratchFate {
        #[cfg(test)]
        if let Some(errno) = self.seams.removal_errno {
            // D3-T24's injected removal failure.
            drop(dir);
            return ScratchFate::Retained(ScratchRetained::IoFailure(errno));
        }
        #[cfg(test)]
        let mut ledger = match self.seams.removal_limits {
            Some(limits) => WorkLedger::with_limits(limits).unwrap_or_else(|_| WorkLedger::new()),
            None => WorkLedger::discovery_profile(),
        };
        #[cfg(not(test))]
        let mut ledger = WorkLedger::discovery_profile();
        match ledger.scope(|work| dir.remove_bounded(work)) {
            Ok(()) => ScratchFate::Removed,
            Err(WorkFailure::Budget(_)) => ScratchFate::Retained(ScratchRetained::WorkExhausted),
            Err(WorkFailure::Operation(error)) => match error {
                opensip_platform::LaunchError::Io { error, .. } => match error.raw_os_error() {
                    Some(errno) => ScratchFate::Retained(ScratchRetained::IoFailure(errno)),
                    None => ScratchFate::Retained(ScratchRetained::WorkExhausted),
                },
                _ => ScratchFate::Retained(ScratchRetained::WorkExhausted),
            },
        }
    }

    /// Host unwinding (item 12, :436; LD-D3A-14): kill the group once if
    /// the root is unreaped, poll the non-blocking reap to the ceiling,
    /// then abandon; remove the scratch; mint `abandoned`.
    fn unwind(&mut self) {
        // Settled, or never spawned: there is nothing to settle (r2, RF-5).
        if self.state == State::Settled || self.child.is_none() {
            return;
        }
        self.trigger(Cause::Abandoned);
        let unreaped = self.child.as_ref().is_some_and(|c| !c.is_reaped()) && self.reaped.is_none();
        if unreaped {
            // The kill is marked before the first reap attempt, so each
            // attempt captures the confirmation against the still-unreaped
            // root, and settlement reuses the last one (r3, RF-1).
            if let Some(ladder) = &mut self.ladder
                && ladder.kill_at.is_none()
            {
                ladder.kill_at = Some(Instant::now());
            }
            if self.signal(SIGKILL) {
                self.append(SupervisionEvent::Signalled { signal: SIGKILL });
            }
            let ceiling = Instant::now() + self.waits.reap_ceiling;
            while Instant::now() < ceiling {
                if self.try_reap() {
                    break;
                }
                std::thread::sleep(Duration::from_millis(10));
            }
        }
        self.settle();
        #[cfg(test)]
        if let Some(sink) = &self.seams.unwound
            && let Some(settlement) = self.settlement.take()
        {
            sink.send(settlement).ok();
        }
    }
}

impl<P: Participant> Drop for Supervision<P> {
    fn drop(&mut self) {
        self.unwind();
    }
}

fn exit_class(status: ProcessExitStatus) -> ExitClass {
    match (status.code(), status.signal()) {
        (Some(code), _) => ExitClass::Exited(code),
        (_, Some(signal)) => ExitClass::Signaled(signal),
        _ => ExitClass::Exited(-1),
    }
}

fn family_of(text: &str) -> Option<RefusalFamily> {
    use RefusalFamily as F;
    [
        F::Rf1,
        F::Rf2,
        F::Rf3,
        F::Rf4,
        F::Rf5,
        F::Rf6,
        F::Rf7,
        F::Rf8,
    ]
    .into_iter()
    .find(|f| f.as_str() == text)
}

fn message_type(message: &Control3Root) -> &'static str {
    match message {
        Control3Root::Hello { .. } => "hello",
        Control3Root::HelloAck { .. } => "helloAck",
        Control3Root::Select { .. } => "select",
        Control3Root::SelectAck { .. } => "selectAck",
        Control3Root::Refusal { .. } => "refusal",
        Control3Root::Ping { .. } => "ping",
        Control3Root::Pong { .. } => "pong",
        Control3Root::Cancel { .. } => "cancel",
        Control3Root::Health { .. } => "health",
        Control3Root::HealthReport { .. } => "healthReport",
        Control3Root::ResourceReport { .. } => "resourceReport",
        Control3Root::Fault { .. } => "fault",
        Control3Root::EffectRequest { .. } => "effectRequest",
        Control3Root::EffectResult { .. } => "effectResult",
        Control3Root::Shutdown { .. } => "shutdown",
        Control3Root::ShutdownAck { .. } => "shutdownAck",
    }
}

#[path = "supervisor_records.rs"]
pub mod records;

#[cfg(test)]
#[path = "supervisor_tests.rs"]
pub(crate) mod tests;
