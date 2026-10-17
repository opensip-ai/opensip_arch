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
//! **Not here.** The memory and process-count ceilings, the byte bounds and
//! the zero-fit refusal are D3a-2's; records, discard and the admission gate
//! are D3a-3's; the descendant step, user cancellation, revocation and
//! harness coexistence are D3b's. The tool class (item 12's no-handshake
//! children) lands with D3a-2's tool output bound.
use crate::control_protocol::{
    AdmittedSelection, Control3Root, ControlContext, ControlSession, ControlState, ControlVerdict,
    Direction, RefusalFamily, SubprotocolTuple, host_hello, host_select,
};
use crate::provider_protocol::{ProcessEvent, ProcessFault};
use opensip_contracts::generated::protocol::{
    Control3RootVariant7Property0, Control3RootVariant7Property0Reason as CancelReason,
    Control3RootVariant8Property0, Control3RootVariant14Property0,
    Control3RootVariant14Property0Reason as ShutdownReason,
};
use opensip_platform::{
    ProcessChild as Child, ProcessExitStatus, Readiness, Reaped, ScratchRoot, VerifiedLaunch,
    WorkFailure, WorkLedger, group_members, spawn, wait_ready,
};
use std::fs::File;
use std::io::{self, Read, Write};
use std::num::NonZeroU64;
use std::os::fd::AsRawFd;
use std::sync::mpsc;
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

// ------------------------------------------------------------------ causes and settlement

/// The settlement's causes (item 12, :446). `user-cancel`, `revoked` and
/// `observer-fail-stop` are accepted in the table, but their ladders are
/// D3b's (LD-D3A-6). O7's `confinement-refused` is not at M3.
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
/// The one byte bound D3 itself enforces as a cause (item 16, :546): TS2's
/// aggregate response, `byte-bound(response)`. D3a-2 enforces it.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ByteBound {
    Response,
}

/// The two refusals D4 raises before any spawn (item 12, :425).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum PreSpawnRefusal {
    ClosureRecheckFailed,
    SessionSpecInconsistent,
}

/// How the child ended (item 12, :440); absent when nothing was spawned.
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
/// The scratch's fate (item 12 as amended by LD-D3A-17, :444). `Removed`
/// and `Retained` are the law's. `KeptWithUnreapedRoot` and `NoScratch`
/// are D3a-1's cases the law does not name (an abandoned root may still
/// run in its scratch; nothing was spawned), left for the lead and D3a-3.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ScratchFate {
    Removed,
    Retained(ScratchRetained),
    KeptWithUnreapedRoot,
    NoScratch,
}
/// Why a scratch was retained (LD-D3A-17): a failed call's actual errno,
/// or the removal walk's finite budget, with no errno.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ScratchRetained {
    IoFailure(i32),
    WorkExhausted,
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
/// verified every commitment. Item 20's gate (D3a-3) releases it from a
/// clean settlement or drops it; without one nothing is releasable.
#[derive(Debug)]
pub struct TerminalOutput {
    kind: TerminalKind,
}
impl TerminalOutput {
    /// For the participant only, after its terminal's commitments recompute.
    /// Its production callers are the codecs (D2b-3, D2b-4).
    #[cfg_attr(not(test), allow(dead_code))]
    pub(crate) fn mint(kind: TerminalKind) -> Self {
        Self { kind }
    }
    pub fn kind(&self) -> TerminalKind {
        self.kind
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
    exit: Option<ExitClass>,
    tree: TreeReport,
    stderr: StderrCount,
    rusage: Option<Rusage>,
    scratch: ScratchFate,
    terminal: Option<TerminalKind>,
    eof_observed: bool,
    output: Option<TerminalOutput>,
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
    pub fn exit(&self) -> Option<ExitClass> {
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
            && self.exit == Some(ExitClass::Exited(0))
            && self.eof_observed
            && self.output.is_some()
    }
    /// The terminal's output, for item 20's gate (D3a-3) to release or drop.
    pub fn take_output(&mut self) -> Option<TerminalOutput> {
        self.output.take()
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
}
impl ParticipantStep {
    pub fn status(status: ParticipantStatus) -> Self {
        Self {
            status,
            progress: Vec::new(),
            admitted_payload_bytes: 0,
            eof: false,
        }
    }
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
}

// ------------------------------------------------------------------ the supervision

/// Item 12's states (:423-431). Tools, which skip `Handshaking`, land with
/// D3a-2.
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
    LivenessMissed,
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
}

/// Why a supervision was not prepared.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum SupervisorError {
    /// The caller may need user cancellation, revocation or observer
    /// fail-stop, whose ladders are D3b's (LD-D3A-6).
    LadderUnavailable,
}

/// What D4's session factory hands over (item 12's `Prepared`, :425).
#[derive(Debug)]
pub struct SessionSpec {
    pub launch: VerifiedLaunch,
    pub selection: AdmittedSelection,
    /// Whether the caller may need a D3b ladder.
    pub needs_d3b_ladders: bool,
}

/// A cross-thread trigger (LD-D3A-5): appended through one bounded channel,
/// never applied to the state from another thread.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum Trigger {
    HostFault,
}
/// The one way another thread reaches a supervision.
#[derive(Debug, Clone)]
pub struct SupervisionHandle {
    sender: mpsc::SyncSender<Trigger>,
}
impl SupervisionHandle {
    /// The host's own fault (cause `host-fault`). `false` when the channel
    /// is full or the supervision is gone: a trigger is already pending or
    /// nothing is left to stop.
    pub fn host_fault(&self) -> bool {
        self.sender.try_send(Trigger::HostFault).is_ok()
    }
}
/// The bounded channel's capacity: one pending trigger per source.
const TRIGGER_CAPACITY: usize = 4;

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

/// The host's pending control write: the whole frame and its offset.
#[derive(Default)]
struct PendingWrite {
    bytes: Vec<u8>,
    at: usize,
}

/// D3a's fault ladder's progress (LD-D3A-6).
#[derive(Debug, Clone, Copy)]
struct Ladder {
    /// T-1 is done, or skipped: the normal end's grace expiry enters at T-2
    /// (LD-D3A-15).
    t1_done: bool,
    term_at: Option<Instant>,
    kill_at: Option<Instant>,
}

/// The two signals D3a's ladder sends to the group (item 19, :639-640),
/// by their POSIX numbers on both families.
const SIGTERM: i32 = 15;
const SIGKILL: i32 = 9;

/// stderr's fixed read buffer (item 17): bytes are read into it, counted
/// and overwritten; nothing else holds them.
const STDERR_BUFFER: usize = 4096;

/// A test's observer of the merged order.
type Observer = Box<dyn FnMut(&SupervisionEvent)>;

/// One child's supervision (item 12).
pub struct Supervision<P: Participant> {
    state: State,
    launch: Option<VerifiedLaunch>,
    selection: AdmittedSelection,
    participant: P,
    waits: Waits,
    protocol: ProtocolWaits,
    child: Option<Child>,
    ends: HostEnds,
    control: ControlSession,
    reader: ControlReader,
    control_out: PendingWrite,
    close_fd3_after_write: bool,
    host_seq: u64,
    nonce_seq: u64,
    stderr_buf: [u8; STDERR_BUFFER],
    stderr: StderrCount,
    triggers: mpsc::Receiver<Trigger>,
    sender: mpsc::SyncSender<Trigger>,
    observer: Option<Observer>,
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
    #[cfg(test)]
    seams: tests::Seams,
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
        if spec.needs_d3b_ladders {
            return Err(SupervisorError::LadderUnavailable);
        }
        let control = ControlSession::new(ControlContext::for_session(&spec.selection));
        let bound = control.policy().frame_bound();
        let (sender, triggers) = mpsc::sync_channel(TRIGGER_CAPACITY);
        let protocol = participant.protocol_waits();
        Ok(Self {
            state: State::Prepared,
            launch: Some(spec.launch),
            selection: spec.selection,
            participant,
            waits,
            protocol,
            child: None,
            ends: HostEnds::default(),
            control,
            reader: ControlReader::new(bound),
            control_out: PendingWrite::default(),
            close_fd3_after_write: false,
            host_seq: 1,
            nonce_seq: 0,
            stderr_buf: [0; STDERR_BUFFER],
            stderr: StderrCount::default(),
            triggers,
            sender,
            observer: None,
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
            #[cfg(test)]
            seams: tests::Seams::default(),
        })
    }

    pub fn state(&self) -> State {
        self.state
    }
    /// The protocol waits in force: the participant's own (LD-D3A-7).
    pub fn protocol_waits(&self) -> ProtocolWaits {
        self.protocol
    }
    /// The cross-thread trigger channel (LD-D3A-5).
    pub fn handle(&self) -> SupervisionHandle {
        SupervisionHandle {
            sender: self.sender.clone(),
        }
    }
    /// How many events the merged order has appended.
    pub fn event_count(&self) -> u64 {
        self.events
    }
    /// The settlement, by value, once (LD-D3A-5).
    pub fn take_settlement(&mut self) -> Option<Settlement> {
        self.settlement.take()
    }

    /// D4's pre-spawn refusals (item 12, :425): settle with nothing spawned.
    pub fn decline(&mut self, refusal: PreSpawnRefusal) {
        if self.state != State::Prepared {
            return;
        }
        self.trigger(match refusal {
            PreSpawnRefusal::ClosureRecheckFailed => Cause::ClosureRecheckFailed,
            PreSpawnRefusal::SessionSpecInconsistent => Cause::SessionSpecInconsistent,
        });
        self.settle();
    }

    /// Spawn and supervise the child to its one settlement.
    pub fn run(&mut self, root: &mut ScratchRoot) {
        self.start(root);
        while self.state != State::Settled {
            self.turn();
        }
    }

    fn append(&mut self, event: SupervisionEvent) {
        self.events = self.events.saturating_add(1);
        if let Some(observer) = &mut self.observer {
            observer(&event);
        }
    }

    /// `Prepared` to `Spawning` to `Handshaking`, or to `Settled` on a
    /// spawn failure.
    fn start(&mut self, root: &mut ScratchRoot) {
        if self.state != State::Prepared {
            return;
        }
        self.state = State::Spawning;
        let Some(launch) = self.launch.take() else {
            return;
        };
        let mut child = match spawn(launch, root) {
            Ok(child) => child,
            Err(_) => {
                self.trigger(Cause::SpawnFailed);
                self.settle();
                return;
            }
        };
        let now = Instant::now();
        self.spawned_at = Some(now);
        self.append(SupervisionEvent::Spawned {
            process_id: child.process_id(),
        });
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
        }
        self.child = Some(child);
        self.state = State::Handshaking;
        // The host's hello (item 9), through the session only.
        if let Some(hello) = self.host_message(host_hello) {
            let sent = self.send_control(&hello);
            self.control.observations_mut().hello_seen = sent;
        }
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
        make(&self.selection, NonZeroU64::new(self.host_seq)?)
    }
    /// Send a host control frame through `ControlSession::send` (D2a r2),
    /// queued for fd3. False when the session refuses it or fd3 is closed.
    fn send_control(&mut self, message: &Control3Root) -> bool {
        if self.ends.fd3.is_none() || !self.control_out.bytes.is_empty() {
            return false;
        }
        match self.control.send(message) {
            Ok(frame) => {
                self.host_seq += 1;
                self.control_out = PendingWrite {
                    bytes: frame,
                    at: 0,
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
            // A late event is counted and dropped (LD-D3A-5).
            while self.triggers.try_recv().is_ok() {
                self.append(SupervisionEvent::LateEvent);
            }
            return;
        }
        while let Ok(trigger) = self.triggers.try_recv() {
            match trigger {
                Trigger::HostFault => self.trigger(Cause::HostFault),
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
                self.append(SupervisionEvent::LivenessMissed);
                self.trigger(Cause::Liveness);
            } else if self.health_due.is_none()
                && self.next_health.is_some_and(|at| now >= at)
                && self.control.state() == ControlState::Steady
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
            && now >= at + self.protocol.normal_exit_grace
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
        self.control.observations_mut().pending_health_report = Some(nonce);
        if self.send_control(&message) {
            self.health_due = Some(now + self.waits.liveness_window);
            self.next_health = None;
        }
    }

    /// The earliest pending deadline, for the wait's timeout.
    fn next_deadline(&self) -> Option<Instant> {
        let mut all: Vec<Instant> = Vec::new();
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
        {
            all.push(at + self.protocol.normal_exit_grace);
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
            && self.participant.wants_write()
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
            self.append(SupervisionEvent::ExitObserved);
            self.drained_check();
        }
    }

    /// The control channel: frames reassembled from any split, each decided
    /// by the session.
    fn service_control(&mut self) {
        let bound = self.control.policy().frame_bound();
        loop {
            let Some(fd) = &mut self.ends.fd4 else {
                return;
            };
            let read = match self.reader.read(fd, bound) {
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
                        let partial = self.reader.have;
                        let frame = self.reader.buf[..partial].to_vec();
                        self.receive_control(&frame);
                    }
                    self.ends.fd4 = None;
                    self.append(SupervisionEvent::ChannelEof(Channel::Control));
                    self.drained_check();
                    return;
                }
                ControlRead::OverBound => {
                    let prefix = self.reader.buf[..4].to_vec();
                    self.receive_control(&prefix);
                }
                ControlRead::Frame(len) => {
                    let frame = self.reader.buf[..len].to_vec();
                    self.receive_control(&frame);
                }
            }
            if self.state == State::Settled {
                return;
            }
        }
    }

    fn receive_control(&mut self, frame: &[u8]) {
        let step = self.control.receive(Direction::ComponentToHost, frame);
        match step.verdict {
            ControlVerdict::Refused(refused) => {
                self.trigger(Cause::ControlRefusal(refused.family));
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
                        self.control.observations_mut().confirmed_tuples = confirmed;
                        if let Some(select) = self.host_message(host_select) {
                            let tuple = self.selection.tuple.clone();
                            self.control.observations_mut().selected_tuple = Some(tuple);
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
                        self.control.observations_mut().pending_health_report = None;
                        self.health_due = None;
                        self.next_health = Some(Instant::now() + self.waits.health_ping_interval);
                    }
                    Control3Root::ShutdownAck { .. } => {
                        self.shutdown_ack = true;
                        self.check_clean();
                    }
                    Control3Root::Refusal { .. } => {
                        let family = accepted
                            .terminal_family
                            .as_deref()
                            .and_then(family_of)
                            .unwrap_or(RefusalFamily::Rf2);
                        self.trigger(Cause::ControlRefusal(family));
                    }
                    Control3Root::Fault { .. } => self.trigger(Cause::ProviderProtocol),
                    _ => {}
                }
            }
        }
    }

    /// stderr (item 17): read continuously into the fixed buffer, counted,
    /// overwritten; never held.
    fn service_stderr(&mut self) {
        loop {
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

    /// One participant read (the yield contract).
    fn service_data_read(&mut self) {
        let Some(fd) = &mut self.ends.fd1 else {
            return;
        };
        let step = self.participant.readable(fd);
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
        let Some(fd) = &mut self.ends.fd0 else {
            return;
        };
        let step = self.participant.writable(fd);
        self.apply_step(step);
    }

    fn service_control_write(&mut self) {
        let Some(fd) = &mut self.ends.fd3 else {
            return;
        };
        let pending = &mut self.control_out;
        match fd.write(&pending.bytes[pending.at..]) {
            Ok(n) => pending.at += n,
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
            self.control_out = PendingWrite::default();
            if self.close_fd3_after_write {
                // The normal end closes the protocol (DLV:567).
                self.ends.fd3 = None;
            }
        }
    }

    /// Deliver a process event to the participant and apply its step.
    fn deliver(&mut self, event: ProcessEvent) {
        if self.state == State::Settled {
            return;
        }
        self.append(SupervisionEvent::Delivered(event));
        let step = self.participant.process(event);
        self.apply_step(step);
    }

    fn apply_step(&mut self, step: ParticipantStep) {
        for progress in &step.progress {
            self.last_progress = Some(Instant::now());
            self.append(SupervisionEvent::Progress(*progress));
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
            ParticipantStatus::Done => self.check_clean(),
            _ => {}
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
        self.health_due = None;
        if let Some(seq) = NonZeroU64::new(self.host_seq) {
            let shutdown = Control3Root::Shutdown {
                body: Control3RootVariant14Property0 {
                    reason: ShutdownReason::Normal,
                },
                control_major: NonZeroU64::MIN,
                seq,
            };
            // A health exchange in flight is overtaken: the shutdown waits
            // for the pending write, then goes.
            self.flush_control_now();
            self.send_control(&shutdown);
        }
        self.participant.close_input();
        self.ends.fd0 = None;
        self.close_fd3_after_write = true;
        if self.control_out.bytes.is_empty() {
            self.ends.fd3 = None;
        }
    }

    /// Finish a pending control write before the next one, within one
    /// short bounded attempt; what does not go is dropped with fd3.
    fn flush_control_now(&mut self) {
        for _ in 0..64 {
            if self.control_out.bytes.is_empty() || self.ends.fd3.is_none() {
                return;
            }
            self.service_control_write();
        }
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
        if self.terminal.is_none() && self.first_cause.is_none() {
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
    /// channel at EOF and the death appended, with no cause.
    fn check_clean(&mut self) {
        if self.first_cause.is_none()
            && self.participant_status == ParticipantStatus::Done
            && self.shutdown_ack
            && self.death_appended
        {
            self.first_cause = Some(Cause::Clean);
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
                    self.ladder = Some(Ladder {
                        t1_done: from_t2,
                        term_at: None,
                        kill_at: None,
                    });
                }
            }
            Some(_) => self.later_causes.push(cause),
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
            if let Some(seq) = NonZeroU64::new(self.host_seq) {
                let cancel = Control3Root::Cancel {
                    body: Control3RootVariant7Property0 { reason },
                    control_major: NonZeroU64::MIN,
                    seq,
                };
                self.flush_control_now();
                self.send_control(&cancel);
                self.flush_control_now();
            }
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
        // The ceiling runs from the KILL; a clean end that cannot be reaped
        // gets a ladder's ceiling too.
        if let Some(kill) = self.ladder.and_then(|l| l.kill_at)
            && Instant::now() >= kill + self.waits.reap_ceiling
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
        let cause = self.first_cause.unwrap_or(Cause::Abandoned);
        let killed = self.ladder.is_some_and(|l| l.kill_at.is_some());
        self.tree = if !killed {
            TreeReport::NotKilled
        } else if self.root_alone() {
            TreeReport::GroupKilledPlatformLimited
        } else {
            TreeReport::Incomplete
        };
        let mut exit = None;
        let mut scratch = ScratchFate::NoScratch;
        if let Some(mut child) = self.child.take() {
            if child.is_reaped() {
                if let Some(status) = self.reaped.map(|r| r.status) {
                    exit = Some(exit_class(status));
                }
                scratch = match child.take_scratch() {
                    Some(dir) => self.remove_scratch(dir),
                    None => ScratchFate::NoScratch,
                };
                drop(child);
            } else {
                exit = Some(ExitClass::Unreaped);
                scratch = ScratchFate::KeptWithUnreapedRoot;
                drop(child.abandon());
                self.append(SupervisionEvent::Abandoned);
            }
        }
        self.ends = HostEnds::default();
        let output = self.participant.take_terminal_output();
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
        };
        self.state = State::Settled;
        self.settlement = Some(settlement);
        self.append(SupervisionEvent::Settled(cause));
    }

    /// Item 20's removal, within bounded work (LD-D3A-12: the discovery
    /// profile's caps), its failure retained (LD-D3A-17). The removal
    /// policy's records are D3a-3's.
    fn remove_scratch(&mut self, dir: opensip_platform::ChildScratch) -> ScratchFate {
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
        if self.state == State::Settled {
            return;
        }
        self.trigger(Cause::Abandoned);
        let unreaped = self.child.as_ref().is_some_and(|c| !c.is_reaped()) && self.reaped.is_none();
        if unreaped {
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
        if self.ladder.is_some_and(|l| l.kill_at.is_none())
            && let Some(ladder) = &mut self.ladder
        {
            ladder.kill_at = Some(Instant::now());
        }
        self.settle();
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

#[cfg(test)]
#[path = "supervisor_tests.rs"]
pub(crate) mod tests;
