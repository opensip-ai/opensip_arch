// Units D3a-1's and D3a-2's controls (D3a plan r4, §3): each drives the real loop over a
// fixture child (`tests/supervisor_fixture.rs`, LD-D3A-9), located by the
// lane-written `supervisor_fixture.path` beside this test binary, and a
// fixture participant built from D2b-1's `FrameAccumulator` and D2b-2's
// table engine. It is a test double and never a codec: it runs P3T's rows on
// frame types alone and admits no payload.
use super::*;
use crate::control_protocol::Platform;
use crate::provider_protocol::cbor::{Profile, Value};
use crate::provider_protocol::table::{Event, Protocol, Run, Scalar, Table};
use crate::provider_protocol::{FrameAccumulator, write_frame};
use opensip_identity::{digest_hex, raw_sha256};
use opensip_platform::{
    ChildEnvironment, ClosureRecheck, DescriptorSet, LaunchSpec, ScratchRoot, VerifiedLaunch,
    WorkCost,
};
use std::cell::RefCell;
use std::ffi::OsStr;
use std::os::fd::{FromRawFd, IntoRawFd, OwnedFd};
use std::path::{Path, PathBuf};
use std::rc::Rc;
use std::sync::atomic::{AtomicBool, AtomicU64, Ordering};
use std::sync::{Barrier, OnceLock, mpsc};

/// D3b-1: where the descendant step calls a test's hook.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum TreeStep {
    /// Between the snapshot and the group SIGKILL (D5-T2b's pause).
    AfterSnapshot,
    /// Between the group SIGKILL and the identity-checked kills.
    AfterGroupKill,
}
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum TreeCallAttempt {
    Group,
    ByPid(i32),
}

/// D3b-1: a test's hook on the snapshot's targets.
type TreeHookAction = dyn FnMut(TreeStep, &mut Vec<ProcessIdentity>);
pub(crate) struct TreeHook(pub(crate) Box<TreeHookAction>);
impl std::fmt::Debug for TreeHook {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.write_str("TreeHook")
    }
}

/// The supervision's test seams.
#[derive(Debug, Default)]
pub(crate) struct Seams {
    /// D3b-1: the snapshot's child listing, the confirm's group listing and
    /// the group SIGKILL each fail; and the hook between steps.
    pub(crate) snapshot_listing_fails: bool,
    pub(crate) confirm_listing_fails: bool,
    pub(crate) group_kill_fails: bool,
    pub(crate) group_kill_errors: std::collections::VecDeque<i32>,
    pub(crate) tree_identity_error: Option<TreeCall>,
    pub(crate) tree_kill_result: Option<Result<KillOutcome, i32>>,
    pub(crate) confirm_exceeded_once: bool,
    pub(crate) tree_hook: Option<TreeHook>,
    pub(crate) tree_calls: Rc<RefCell<Vec<TreeCallAttempt>>>,
    /// The reap never succeeds: a root that survives the reap ceiling.
    pub(crate) reap_blocked: bool,
    /// The scratch removal's ledger, in place of the discovery profile.
    pub(crate) removal_limits: Option<WorkCost>,
    pub(crate) reads_this_turn: u32,
    /// The most participant reads in one turn (the yield contract: one).
    pub(crate) max_reads_per_turn: u32,
    /// The child's scratch path, for the no-scratch-left controls.
    pub(crate) scratch: Option<PathBuf>,
    /// r2 (RF-1): reads per turn, and stderr as an always-ready /dev/zero.
    pub(crate) control_reads_this_turn: usize,
    pub(crate) stderr_reads_this_turn: usize,
    pub(crate) max_control_reads_per_turn: usize,
    pub(crate) max_stderr_reads_per_turn: usize,
    pub(crate) stderr_zero: bool,
    /// r2 (RF-4): each control write at most this many bytes, and no write
    /// progress while `Running` before the terminal.
    pub(crate) control_write_chunk: Option<usize>,
    pub(crate) stall_control_writes_in_running: bool,
    /// r2 (RF-9): the confirmation sees a member the kill missed.
    pub(crate) extra_member: bool,
    /// r3 (RF-1): where an unwind (and so `Drop`) hands its settlement.
    pub(crate) unwound: Option<mpsc::Sender<Settlement>>,
    /// D3a-2: the process count unenforced, for D3a-1's controls whose
    /// fixtures spawn group members on purpose (LD-D3A2-4).
    pub(crate) process_count_off: bool,
    /// D3a-2: the scratch measurement's ledger, in place of the discovery
    /// profile (LD-D3A-12's exhaustion control).
    pub(crate) measure_limits: Option<WorkCost>,
    /// D3a-3: the group listing fails, or every member's resident sample
    /// fails with this errno (D3A2-R1-NBO-1); the scratch removal fails
    /// with this errno (D3-T24).
    pub(crate) listing_fails: bool,
    pub(crate) sample_errno: Option<i32>,
    pub(crate) removal_errno: Option<i32>,
    /// r2 (D3A3-R1-RF-2): no control write at all, and at most this many
    /// more control bytes written.
    pub(crate) stall_control_writes: bool,
    pub(crate) control_bytes_left: Option<usize>,
    /// r2 (D3A3-R1-RF-2): every control write fails with `EPIPE`.
    pub(crate) control_write_fails: bool,
    /// D3a-3: the record facts the public sink received.
    pub(crate) facts: Rc<RefCell<Vec<records::RecordFact>>>,
}

const SENTINEL: &str = "opensip-d3a-fixture";

// ------------------------------------------------------------------ the fixture participant

fn rust3() -> &'static Table {
    static TABLE: OnceLock<Table> = OnceLock::new();
    TABLE.get_or_init(|| Table::load(Protocol::Rust3).expect("P3T loads"))
}

/// The fixture participant: the host side of P3T over frame types alone.
pub(crate) struct FixtureParticipant {
    run: Run<'static>,
    accumulator: FrameAccumulator,
    pending: Vec<u8>,
    at: usize,
    closed: bool,
    /// Every byte read from fd1, in order (RF-6's raw control).
    raw: Vec<u8>,
    waits: ProtocolWaits,
    output: Option<TerminalOutput>,
    chunk: Option<usize>,
    reads: u64,
    /// D3a-2: the protocol it reports, and the payload bytes it claims for
    /// each admitted `FactBatch` in place of every frame's own (D3-T16's
    /// byte accounting).
    protocol: Protocol,
    fact_batch_claim: Option<u64>,
    /// D3a-3: the spooled candidates (each admitted `FactBatch`), the span
    /// boundaries owed to the next step, whether the settlement discarded,
    /// and a terminal whose commitment does not recompute (NBO-2).
    spool: Spool,
    spooled: u64,
    boundaries: Vec<Boundary>,
    discarded: bool,
    bad_commitment: bool,
    commitment_failed: bool,
    /// D3a-4 r2: whether `Analyze` was queued, which selects the
    /// `Unavailable` payload (D3A4-R1-NBO-1).
    analyzed: bool,
}
impl FixtureParticipant {
    fn new(waits: ProtocolWaits) -> Self {
        let mut participant = Self {
            run: rust3().start(),
            accumulator: FrameAccumulator::new(Profile::Rust3, 16, None),
            pending: Vec::new(),
            at: 0,
            closed: false,
            raw: Vec::new(),
            waits,
            output: None,
            chunk: None,
            reads: 0,
            protocol: Protocol::Rust3,
            fact_batch_claim: None,
            spool: Spool::default(),
            spooled: 0,
            boundaries: Vec::new(),
            discarded: false,
            bad_commitment: false,
            commitment_failed: false,
            analyzed: false,
        };
        participant.host_frames();
        participant
    }
    fn status(&self) -> ParticipantStatus {
        if self.commitment_failed {
            return ParticipantStatus::Fault;
        }
        match self.run.phase() {
            "FAULT" => ParticipantStatus::Fault,
            "DONE" => ParticipantStatus::Done,
            _ => match self.run.field("terminalKind") {
                Some(Scalar::Text(kind)) => ParticipantStatus::Terminal(terminal_of(kind)),
                _ => ParticipantStatus::Running,
            },
        }
    }
    fn step(&mut self, event: &Event) {
        self.run.step(event);
        // D3a-4: the phase after each transition (a supervision records
        // only a change).
        if let Some(state) = records::provider_state(self.run.phase()) {
            self.boundaries.push(Boundary::Phase(state));
        }
        if let ParticipantStatus::Terminal(kind) = self.status()
            && self.output.is_none()
        {
            if self.bad_commitment {
                // NBO-2: the terminal's commitment does not recompute, so
                // no output is minted and the participant faults.
                self.commitment_failed = true;
                return;
            }
            // The fixture's frames carry no commitment: its terminal is
            // verified as soon as it is admitted. Its `Unavailable` frame
            // carries no reason, so the double reports a fixed admitted one:
            // before Analyze, `PreAnalyzeUnavailableV1`'s only reason; after
            // it, one `UnavailableV3` admits.
            if kind == TerminalKind::Unavailable {
                self.boundaries
                    .push(Boundary::Unavailable(if self.analyzed {
                        opensip_operability::ProviderReason::CapabilityMissing
                    } else {
                        opensip_operability::ProviderReason::NativeContextMismatch
                    }));
            }
            self.output = Some(TerminalOutput::mint(kind, std::mem::take(&mut self.spool)));
        }
    }
    fn queue(&mut self, frame: &str) {
        let mut members = Vec::new();
        if frame == "SnapshotFileChunk"
            && let Some(size) = self.chunk
        {
            members.push(("data".to_owned(), Value::Bytes(vec![7; size])));
        }
        members.push(("type".to_owned(), Value::Text(frame.to_owned())));
        let bytes = write_frame(&Value::Map(members)).expect("a frame");
        self.pending.extend_from_slice(&bytes);
        let mut event = Event::frame(frame);
        if frame == "Analyze" {
            event.stage_count = 1;
            self.analyzed = true;
            self.boundaries.push(Boundary::AnalyzeSent);
        }
        self.step(&event);
    }
    /// The host frames each ready phase owes (P3T's host rows).
    fn host_frames(&mut self) {
        if self.closed {
            return;
        }
        match self.run.phase() {
            "START" => self.queue("Hello"),
            "READY_OPEN_UNIVERSE" => self.queue("OpenUniverse"),
            "READY_SNAPSHOT_MANIFEST" => {
                self.boundaries.push(Boundary::TransferStarted);
                self.queue("SnapshotManifest");
                if self.chunk.is_some() {
                    self.queue("SnapshotFileChunk");
                }
                self.queue("SnapshotSeal");
            }
            "READY_ANALYZE" => self.queue("Analyze"),
            _ => {}
        }
    }
    fn report(&mut self, progress: Vec<Progress>, bytes: u64, eof: bool) -> ParticipantStep {
        ParticipantStep {
            status: self.status(),
            progress,
            admitted_payload_bytes: bytes,
            eof,
            boundaries: std::mem::take(&mut self.boundaries),
        }
    }
}
fn terminal_of(kind: &str) -> TerminalKind {
    match kind {
        "complete" => TerminalKind::Complete,
        "unavailable" => TerminalKind::Unavailable,
        "budget-exhausted" => TerminalKind::BudgetExhausted,
        "provider-fault" => TerminalKind::ProviderFault,
        _ => TerminalKind::Cancelled,
    }
}
fn type_of(value: &Value) -> String {
    match value {
        Value::Map(members) => members
            .iter()
            .find(|(k, _)| k == "type")
            .and_then(|(_, v)| match v {
                Value::Text(t) => Some(t.clone()),
                _ => None,
            })
            .unwrap_or_default(),
        _ => String::new(),
    }
}
impl Participant for FixtureParticipant {
    fn protocol_waits(&self) -> ProtocolWaits {
        self.waits
    }
    fn protocol(&self) -> Protocol {
        self.protocol
    }
    fn wants_write(&self) -> bool {
        !self.closed && self.at < self.pending.len()
    }
    fn readable(&mut self, fd1: &mut dyn Read) -> ParticipantStep {
        self.reads += 1;
        let mut buf = [0u8; 512];
        match fd1.read(&mut buf) {
            Ok(0) => {
                if !self.accumulator.at_boundary() {
                    // EOF inside a frame: truncation, a protocol fault.
                    self.step(&Event::frame("truncated"));
                }
                self.report(Vec::new(), 0, true)
            }
            Ok(n) => {
                self.raw.extend_from_slice(&buf[..n]);
                let pushed = self.accumulator.push(&buf[..n]);
                let mut progress = Vec::new();
                let mut bytes = 0u64;
                for frame in &pushed.frames {
                    let ty = type_of(frame.value());
                    bytes += match self.fact_batch_claim {
                        Some(claim) if ty == "FactBatch" => claim,
                        Some(_) => 0,
                        None => frame.payload().len() as u64,
                    };
                    let mut event = Event::frame(&ty);
                    event.identity_negotiated = ty == "HelloAck";
                    self.step(&event);
                    match ty.as_str() {
                        "SnapshotAccepted" => {
                            progress.push(Progress::SnapshotAcknowledged);
                            self.boundaries.push(Boundary::TransferEnded);
                        }
                        "NativeContextVerified" => self.boundaries.push(Boundary::ContextVerified),
                        "FactBatch" => {
                            progress.push(Progress::FactBatch);
                            self.spool.push(frame.payload().to_vec());
                            self.spooled += 1;
                        }
                        "CoverageV3" => progress.push(Progress::Coverage),
                        _ => {}
                    }
                    self.host_frames();
                }
                if pushed.refusal.is_some() {
                    self.step(&Event::frame("refused"));
                }
                self.report(progress, bytes, false)
            }
            Err(e)
                if matches!(
                    e.kind(),
                    io::ErrorKind::WouldBlock | io::ErrorKind::Interrupted
                ) =>
            {
                self.report(Vec::new(), 0, false)
            }
            Err(_) => {
                self.step(&Event::frame("read-failed"));
                self.report(Vec::new(), 0, false)
            }
        }
    }
    fn writable(&mut self, fd0: &mut dyn Write) -> ParticipantStep {
        if self.wants_write() {
            match fd0.write(&self.pending[self.at..]) {
                Ok(n) => {
                    self.at += n;
                    if self.at == self.pending.len() {
                        self.pending.clear();
                        self.at = 0;
                    }
                }
                Err(e)
                    if matches!(
                        e.kind(),
                        io::ErrorKind::WouldBlock | io::ErrorKind::Interrupted
                    ) => {}
                Err(_) => self.step(&Event::frame("write-failed")),
            }
        }
        self.report(Vec::new(), 0, false)
    }
    fn process(&mut self, event: ProcessEvent) -> ParticipantStep {
        self.step(&event.table_event());
        self.report(Vec::new(), 0, false)
    }
    fn close_input(&mut self) {
        self.closed = true;
        self.pending.clear();
        self.at = 0;
    }
    fn take_terminal_output(&mut self) -> Option<TerminalOutput> {
        self.output.take()
    }
    fn discard(&mut self) {
        self.discarded = true;
        self.spool = Spool::default();
        self.output = None;
    }
}

// ------------------------------------------------------------------ the harness

/// The fixture's exact artifact, as this build reported it (LD-D3A-9 r4):
/// the lane writes its path and SHA-256 beside this test binary.
fn fixture() -> PathBuf {
    let exe = std::env::current_exe().expect("the test binary");
    let record = exe
        .parent()
        .expect("its directory")
        .join("supervisor_fixture.path");
    let text = std::fs::read_to_string(&record).unwrap_or_else(|_| {
        panic!(
            "{} is written by the lane (LD-D3A-9); this test runs only there",
            record.display()
        )
    });
    let mut fields = text.lines();
    let path = Path::new(fields.next().expect("the path")).to_path_buf();
    let sha = fields.next().expect("the digest");
    let bytes = std::fs::read(&path).expect("the fixture");
    assert_eq!(digest_hex(&raw_sha256(&bytes)), sha, "the fixture as built");
    path
}

fn selection() -> AdmittedSelection {
    AdmittedSelection {
        stable_id: "00000000-0000-4000-8000-000000000001".to_owned(),
        manifest_digest: "1".repeat(64),
        platform: Platform {
            os: "macos".to_owned(),
            arch: "arm64".to_owned(),
        },
        tuple: SubprotocolTuple {
            role: "analyzer".to_owned(),
            role_subprotocol: "rust-semantic".to_owned(),
            subprotocol_version: 3,
        },
    }
}

fn spec_for(exe: &Path, script: &str) -> SessionSpec {
    let argv: Vec<&OsStr> = vec![exe.as_os_str(), OsStr::new(SENTINEL), OsStr::new(script)];
    let launch = LaunchSpec::fixture(
        DescriptorSet::Provider,
        exe,
        &argv,
        ChildEnvironment::rust(),
    )
    .expect("a fixture spec");
    SessionSpec {
        launch: VerifiedLaunch::from_recheck(
            launch,
            ClosureRecheck {
                member: "supervisor-fixture".to_owned(),
                device: 0,
                inode: 0,
                sha256: "0".repeat(64),
            },
        ),
        selection: selection(),
        needs_d3b_ladders: false,
        memory_budget_bytes: RESIDENT_MEMORY_CEILING,
    }
}

/// D5-0: every ordinary control keeps item 14's release waits.
fn quick() -> Waits {
    Waits::RELEASE
}

/// Only the handshake expiry is shortened, in its named deadline control.
fn handshake_expiry_waits() -> Waits {
    Waits {
        handshake: Duration::from_millis(2_000),
        ..quick()
    }
}
/// Only the wall-clock expiry is shortened, to exercise a deadline's ladder.
fn wall_clock_expiry_waits() -> Waits {
    Waits {
        wall_clock: Duration::from_millis(4_000),
        ..quick()
    }
}
/// Only the missed-health window is shortened, in a liveness-expiry control.
fn liveness_expiry_waits() -> Waits {
    Waits {
        liveness_window: Duration::from_millis(400),
        ..quick()
    }
}
/// Only progress-absence reporting is shortened, in its measured-span controls.
fn progress_absence_waits() -> Waits {
    Waits {
        progress_absent_interval: Duration::from_millis(200),
        ..quick()
    }
}
/// Only the health period is shortened, to put a frame in flight before a terminal.
fn pending_health_waits() -> Waits {
    Waits {
        health_ping_interval: Duration::from_millis(50),
        ..quick()
    }
}
/// Only the drain expiry is shortened, in the held-descriptor control.
fn drain_expiry_waits() -> Waits {
    Waits {
        drain: Duration::from_millis(50),
        ..quick()
    }
}
/// Only the reap expiry is shortened, in controls holding the root unreaped.
fn reap_expiry_waits() -> Waits {
    Waits {
        reap_ceiling: Duration::from_millis(1_000),
        ..quick()
    }
}

/// D5-0's outer cap: the largest retained wait plus drain and reap ceilings.
fn control_cap(waits: Waits) -> Duration {
    [
        waits.handshake,
        waits.health_ping_interval,
        waits.liveness_window,
        waits.progress_absent_interval,
        waits.wall_clock,
        waits.term_to_kill,
        waits.reap_ceiling,
        waits.drain,
    ]
    .into_iter()
    .max()
    .expect("the wait set is nonempty")
        + waits.drain
        + waits.reap_ceiling
}

/// A regression to the old universal 2 s handshake fails without timing a child.
#[test]
fn ordinary_controls_keep_every_release_wait() {
    assert_eq!(quick(), Waits::RELEASE);
    assert_eq!(
        control_cap(quick()),
        WALL_CLOCK_PROVIDER + DRAIN + REAP_CEILING
    );
    assert_eq!(
        control_cap(Waits::TOOL),
        WALL_CLOCK_TOOL + DRAIN + REAP_CEILING
    );
    for (waits, field) in [
        (handshake_expiry_waits(), 0),
        (pending_health_waits(), 1),
        (liveness_expiry_waits(), 2),
        (progress_absence_waits(), 3),
        (wall_clock_expiry_waits(), 4),
        (reap_expiry_waits(), 6),
        (drain_expiry_waits(), 7),
    ] {
        let values = |w: Waits| {
            [
                w.handshake,
                w.health_ping_interval,
                w.liveness_window,
                w.progress_absent_interval,
                w.wall_clock,
                w.term_to_kill,
                w.reap_ceiling,
                w.drain,
            ]
        };
        for (index, (actual, release)) in values(waits).into_iter().zip(values(quick())).enumerate()
        {
            if index == field {
                assert!(actual < release);
            } else {
                assert_eq!(actual, release, "only the exercised wait changes");
            }
        }
    }
}

/// The fixture participant's protocol waits: not a codec's; its own.
const FIXTURE_WAITS: ProtocolWaits = ProtocolWaits {
    stage1_cancel_grace: Duration::from_millis(400),
    normal_exit_grace: Duration::from_millis(500),
};

struct TestDir(PathBuf);
impl Drop for TestDir {
    fn drop(&mut self) {
        // Best effort: an abandoned root's lock may still be held.
        std::fs::remove_dir_all(&self.0).ok();
    }
}
fn test_dir() -> TestDir {
    static NEXT: AtomicU64 = AtomicU64::new(0);
    let dir = std::env::temp_dir().join(format!(
        "opensip-d3a1-test-{}-{}",
        std::process::id(),
        NEXT.fetch_add(1, Ordering::Relaxed)
    ));
    std::fs::create_dir(&dir).expect("a test directory");
    TestDir(dir.canonicalize().expect("its path"))
}
fn root_in(dir: &TestDir) -> ScratchRoot {
    let file = File::open(&dir.0).expect("the directory");
    // SAFETY: the descriptor moves out of the File into the OwnedFd.
    let fd = unsafe { OwnedFd::from_raw_fd(file.into_raw_fd()) };
    ScratchRoot::create_in(fd).expect("a scratch root")
}

type Events = Rc<RefCell<Vec<(Instant, SupervisionEvent)>>>;
type Hook = Box<dyn FnMut(&SupervisionEvent, &SupervisionHandle)>;

/// D3a-1's fixtures that spawn group members on purpose, to drive a join or
/// a wait: a provider tree's process count (one, item 16, :533) would stop
/// each first, so it is not enforced for them (LD-D3A2-4). D3-T14 is its
/// own control.
const MEMBER_SCRIPTS: [&str; 4] = [
    "normal-exit-first",
    "early-exit-held",
    "early-exit-brief-hold",
    "term-survivor",
];

/// A prepared supervision over `script`, observed.
fn prepared(
    script: &str,
    participant: FixtureParticipant,
    hook: Option<Hook>,
) -> (Supervision<FixtureParticipant>, Events) {
    let mut supervision =
        Supervision::prepare_with(spec_for(&fixture(), script), participant, quick())
            .expect("prepared");
    if MEMBER_SCRIPTS.contains(&script) {
        supervision.seams.process_count_off = true;
    }
    let events: Events = Rc::default();
    let sink = Rc::clone(&events);
    // D3a-3: every record fact, through the public sink (LD-D3A3-1).
    let facts = Rc::clone(&supervision.seams.facts);
    supervision.record_facts(Box::new(move |fact| facts.borrow_mut().push(fact)));
    let handle = supervision.handle();
    let mut hook = hook;
    supervision.observer = Some(Box::new(move |event| {
        sink.borrow_mut().push((Instant::now(), event.clone()));
        if let Some(hook) = &mut hook {
            hook(event, &handle);
        }
    }));
    (supervision, events)
}

/// One finished supervision: its settlement and what was observed.
struct Outcome {
    settlement: Settlement,
    events: Vec<(Instant, SupervisionEvent)>,
    raw: Vec<u8>,
    max_reads_per_turn: u32,
    max_control_reads_per_turn: usize,
    max_stderr_reads_per_turn: usize,
    scratch: Option<PathBuf>,
    process_id: Option<i32>,
    /// D3a-3: the record facts; the participant's spooled count, what it
    /// still spools, and whether the settlement discarded.
    facts: Vec<records::RecordFact>,
    spooled: u64,
    spool_left: usize,
    discarded: bool,
}
impl Outcome {
    fn saw(&self, event: &SupervisionEvent) -> bool {
        self.events.iter().any(|(_, e)| e == event)
    }
    /// Any liveness fault, of either provenance.
    fn missed(&self) -> bool {
        self.events
            .iter()
            .any(|(_, e)| matches!(e, SupervisionEvent::LivenessMissed(_)))
    }
    fn count(&self, event: &SupervisionEvent) -> usize {
        self.events.iter().filter(|(_, e)| e == event).count()
    }
    fn when(&self, event: &SupervisionEvent) -> Instant {
        self.events
            .iter()
            .find(|(_, e)| e == event)
            .map(|(t, _)| *t)
            .unwrap_or_else(|| panic!("{event:?} never appended"))
    }
    fn position(&self, event: &SupervisionEvent) -> usize {
        self.events
            .iter()
            .position(|(_, e)| e == event)
            .unwrap_or_else(|| panic!("{event:?} never appended"))
    }
}

/// Drive `supervision` to its settlement within `cap`; past it the test
/// fails (and `Drop` unwinds the child), so no mutation can hang a lane.
fn finish(
    mut supervision: Supervision<FixtureParticipant>,
    events: Events,
    dir: &TestDir,
) -> Outcome {
    let cap = control_cap(supervision.waits);
    let mut root = root_in(dir);
    let started = Instant::now();
    supervision.start(&mut root).expect("spawned");
    while supervision.state() != State::Settled {
        assert!(started.elapsed() < cap, "no settlement within {cap:?}");
        supervision.turn();
    }
    let settlement = supervision.take_settlement().expect("one settlement");
    assert!(supervision.take_settlement().is_none(), "taken once");
    let raw = std::mem::take(
        &mut supervision
            .participant
            .as_mut()
            .expect("a provider's participant")
            .raw,
    );
    let participant = supervision
        .participant
        .as_ref()
        .expect("a provider's participant");
    let (spooled, spool_left, discarded) = (
        participant.spooled,
        participant.spool.len(),
        participant.discarded,
    );
    let facts = supervision.seams.facts.borrow().clone();
    let max_reads_per_turn = supervision.seams.max_reads_per_turn;
    let max_control_reads_per_turn = supervision.seams.max_control_reads_per_turn;
    let max_stderr_reads_per_turn = supervision.seams.max_stderr_reads_per_turn;
    let scratch = supervision.seams.scratch.clone();
    drop(supervision);
    let events = events.borrow().clone();
    let process_id = events.iter().find_map(|(_, e)| match e {
        SupervisionEvent::Spawned { process_id } => Some(*process_id),
        _ => None,
    });
    Outcome {
        settlement,
        events,
        raw,
        max_reads_per_turn,
        max_control_reads_per_turn,
        max_stderr_reads_per_turn,
        scratch,
        process_id,
        facts,
        spooled,
        spool_left,
        discarded,
    }
}

fn outcome(script: &str) -> Outcome {
    outcome_with_waits(script, quick())
}
/// A control names the one wait it exercises instead of shortening every wait.
fn outcome_with_waits(script: &str, waits: Waits) -> Outcome {
    let dir = test_dir();
    let (mut supervision, events) = prepared(script, FixtureParticipant::new(FIXTURE_WAITS), None);
    supervision.waits = waits;
    finish(supervision, events, &dir)
}

/// No child and no scratch left (D3-T3's killable, removable case).
fn nothing_left(out: &Outcome) {
    if let Some(pid) = out.process_id {
        assert_eq!(
            group_members_bounded(pid, 64).expect("the group"),
            Listing::Complete(Vec::new()),
            "the group is gone"
        );
    }
    if let Some(scratch) = &out.scratch {
        assert!(!scratch.exists(), "{} removed", scratch.display());
    }
}

fn delivered(event: ProcessEvent) -> SupervisionEvent {
    SupervisionEvent::Delivered(event)
}

// ------------------------------------------------------------------ the normal end and the joins

/// D3-T4 and the normal end (LD-D3A-15): EOF before the exit and the exit
/// before EOF both settle `clean`. The host sends `shutdown {reason:
/// normal}` and receives `shutdownAck`; the participant gets `zero-exit`
/// and then the held `eof`. RF-6: fd1's raw bytes are exactly the
/// fixture's frames.
#[test]
fn a_normal_child_settles_clean_with_eof_before_or_after_the_exit() {
    let expected: Vec<u8> = [
        "HelloAck",
        "UniverseAccepted",
        "SnapshotAccepted",
        "NativeContextVerified",
        "FactBatch",
        "CoverageV3",
        "Complete",
    ]
    .iter()
    .flat_map(|t| {
        write_frame(&Value::Map(vec![(
            "type".to_owned(),
            Value::Text((*t).to_owned()),
        )]))
        .expect("a frame")
    })
    .collect();
    for script in ["normal", "normal-eof-first", "normal-exit-first"] {
        let out = outcome(script);
        let s = &out.settlement;
        assert_eq!(s.first_cause(), Cause::Clean, "{script}: {:?}", out.events);
        assert_eq!(s.exit(), ExitClass::Exited(0), "{script}");
        assert_eq!(s.terminal(), Some(TerminalKind::Complete), "{script}");
        assert_eq!(s.tree(), TreeReport::NotKilled, "{script}");
        assert_eq!(s.scratch(), ScratchFate::Removed, "{script}");
        assert!(s.admissible(), "{script}");
        assert!(
            out.saw(&SupervisionEvent::ControlSent("shutdown")),
            "{script}"
        );
        assert!(
            out.saw(&SupervisionEvent::ControlReceived("shutdownAck")),
            "{script}"
        );
        assert!(
            out.position(&delivered(ProcessEvent::ZeroExit))
                < out.position(&delivered(ProcessEvent::Eof)),
            "{script}: zero-exit, then the held eof"
        );
        assert_eq!(out.count(&delivered(ProcessEvent::ZeroExit)), 1, "{script}");
        assert!(!out.saw(&SupervisionEvent::CancelAttempted), "{script}");
        assert_eq!(out.raw, expected, "{script}: fd1's raw bytes");
        nothing_left(&out);
    }
}

/// LD-D3A-15: a nonzero exit faults the participant (`provider-protocol`).
#[test]
fn a_nonzero_exit_at_the_normal_end_is_provider_protocol() {
    let out = outcome("nonzero");
    assert_eq!(out.settlement.first_cause(), Cause::ProviderProtocol);
    assert_eq!(out.settlement.exit(), ExitClass::Exited(3));
    assert!(out.saw(&delivered(ProcessEvent::Fault(ProcessFault::NonzeroExit))));
    assert!(!out.settlement.admissible());
    nothing_left(&out);
}

/// LD-D3A-15: a missing `shutdownAck`, and no exit within the grace, each
/// deliver `deadline` (cause `deadline`, the expired wait named), and the
/// ladder runs from T-2: no cancel, `SIGTERM` at once. The grace is the
/// participant's own (D3-T8).
#[test]
fn a_missing_ack_or_exit_within_the_grace_is_deadline_from_t2() {
    for (script, wait) in [
        ("no-ack", BoundedWait::ShutdownAck),
        ("no-exit", BoundedWait::NormalExitGrace),
    ] {
        let out = outcome(script);
        assert_eq!(out.settlement.first_cause(), Cause::Deadline, "{script}");
        assert!(out.saw(&SupervisionEvent::WaitExpired(wait)), "{script}");
        assert!(out.saw(&delivered(ProcessEvent::Fault(ProcessFault::Deadline))));
        assert!(
            !out.saw(&SupervisionEvent::CancelAttempted),
            "{script}: from T-2"
        );
        let terminal = out.when(&SupervisionEvent::Terminal(TerminalKind::Complete));
        let expired = out.when(&SupervisionEvent::WaitExpired(wait));
        let grace = expired.duration_since(terminal);
        assert!(
            grace >= FIXTURE_WAITS.normal_exit_grace && grace < Duration::from_secs(4),
            "{script}: the participant's grace, {grace:?}"
        );
        if script == "no-exit" {
            assert!(out.saw(&SupervisionEvent::Signalled { signal: SIGTERM }));
            assert_eq!(out.settlement.exit(), ExitClass::Signaled(SIGTERM));
        }
        nothing_left(&out);
    }
}

/// D3-T5: EOF before the terminal faults; a frame cut short by EOF faults
/// as truncation.
#[test]
fn eof_before_the_terminal_or_inside_a_frame_faults() {
    for script in ["eof-early", "partial-frame"] {
        let out = outcome(script);
        assert_eq!(
            out.settlement.first_cause(),
            Cause::ProviderProtocol,
            "{script}: {:?}",
            out.events
        );
        assert!(
            out.saw(&SupervisionEvent::ChannelEof(Channel::Data)),
            "{script}"
        );
        assert!(
            out.saw(&SupervisionEvent::CancelAttempted),
            "{script}: from T-1"
        );
        nothing_left(&out);
    }
}

/// D3-T6: a held EOF whose exit never comes within the grace is `deadline`.
#[test]
fn a_held_eof_whose_exit_never_comes_is_deadline() {
    let out = outcome("held-eof-no-exit");
    assert_eq!(out.settlement.first_cause(), Cause::Deadline);
    assert!(out.saw(&SupervisionEvent::WaitExpired(BoundedWait::NormalExitGrace)));
    nothing_left(&out);
}

// ------------------------------------------------------------------ D3-T1's triggers

/// D3-T1 and r2 (Codex D3A1-R1-RF-5): from `Prepared`, D4's two refusals
/// consume the supervision with nothing spawned and no settlement; nothing
/// is settled on its drop either.
#[test]
fn prespawn_refusals_are_errors_with_no_settlement() {
    for refusal in [
        PreSpawnRefusal::ClosureRecheckFailed,
        PreSpawnRefusal::SessionSpecInconsistent,
    ] {
        let (supervision, events) =
            prepared("normal", FixtureParticipant::new(FIXTURE_WAITS), None);
        assert!(matches!(supervision.decline(refusal), RunError::Declined(r) if r == refusal));
        assert!(
            !events
                .borrow()
                .iter()
                .any(|(_, e)| matches!(e, SupervisionEvent::Settled(_)))
        );
    }
}

/// D3-T1 and r2 (RF-5): a spawn failure is an error, with no settlement,
/// and the supervision cannot run again.
#[test]
fn a_spawn_failure_is_an_error_with_no_settlement() {
    let dir = test_dir();
    let missing = dir.0.join("no-such-fixture");
    let mut supervision = Supervision::prepare_with(
        spec_for(&missing, "normal"),
        FixtureParticipant::new(FIXTURE_WAITS),
        quick(),
    )
    .expect("prepared");
    let mut root = root_in(&dir);
    assert!(matches!(
        supervision.run(&mut root),
        Err(RunError::SpawnFailed(_))
    ));
    assert!(supervision.take_settlement().is_none());
    assert!(matches!(
        supervision.run(&mut root),
        Err(RunError::AlreadyRun)
    ));
}

/// D3-T1: the handshake deadline, a control refusal (provider-spoken, a
/// malformed frame, and an over-bound prefix refused from the prefix
/// alone), a participant FAULT, and an early exit. J-3 appends the death
/// only after every channel's EOF, so a root that closes fd1 as it dies
/// before its terminal faults first on item 13's EOF (`provider-protocol`),
/// whether it exits or is signalled; a death while fd1 is still held,
/// appended at the drain's expiry, is `unexpected-exit`.
/// Only silent-handshake exercises a shortened handshake; every other trigger keeps release waits.
#[test]
fn each_trigger_yields_one_settlement_with_its_first_cause() {
    for (script, cause) in [
        ("silent-handshake", Cause::HandshakeDeadline),
        ("refuse", Cause::ControlRefusal(RefusalFamily::Rf2)),
        ("bad-control", Cause::ControlRefusal(RefusalFamily::Rf2)),
        ("over-bound", Cause::ControlRefusal(RefusalFamily::Rf2)),
        ("fault", Cause::ProviderProtocol),
        ("early-exit", Cause::ProviderProtocol),
        ("signal-death", Cause::ProviderProtocol),
        ("early-exit-held", Cause::UnexpectedExit),
    ] {
        let out = if script == "silent-handshake" {
            outcome_with_waits(script, handshake_expiry_waits())
        } else {
            outcome(script)
        };
        assert_eq!(
            out.settlement.first_cause(),
            cause,
            "{script}: {:?}",
            out.events
        );
        assert_eq!(out.count(&SupervisionEvent::Settled(cause)), 1, "{script}");
        if script == "silent-handshake" {
            assert!(out.saw(&SupervisionEvent::WaitExpired(BoundedWait::Handshake)));
        }
        if script == "signal-death" {
            assert_eq!(out.settlement.exit(), ExitClass::Signaled(6));
            assert!(out.saw(&delivered(ProcessEvent::Eof)));
        }
        if script == "early-exit-held" {
            assert!(out.saw(&SupervisionEvent::WaitExpired(BoundedWait::Drain)));
            assert!(out.saw(&delivered(ProcessEvent::ZeroExit)));
        }
        nothing_left(&out);
    }
}

/// D3-T1 and item 14: the wall-clock deadline delivers `deadline` and runs
/// the ladder from T-1 with `cancel {reason: deadline}`.
#[test]
fn the_wall_clock_deadline_delivers_deadline_and_cancels() {
    let out = outcome_with_waits("hang", wall_clock_expiry_waits());
    assert_eq!(out.settlement.first_cause(), Cause::Deadline);
    assert!(out.saw(&SupervisionEvent::WaitExpired(BoundedWait::WallClock)));
    assert!(out.saw(&delivered(ProcessEvent::Fault(ProcessFault::Deadline))));
    assert!(out.saw(&SupervisionEvent::CancelAttempted));
    assert!(out.saw(&SupervisionEvent::ControlSent("cancel")));
    nothing_left(&out);
}

/// D3-T11: a blocked provider, whose stderr keeps up traffic, gets a
/// liveness fault: traffic is not liveness (item 15, F8).
#[test]
fn a_blocked_provider_gets_a_liveness_fault_despite_its_traffic() {
    let out = outcome_with_waits("blocked", liveness_expiry_waits());
    assert_eq!(out.settlement.first_cause(), Cause::Liveness);
    assert!(out.saw(&SupervisionEvent::LivenessMissed(
        LivenessMiss::WindowExpired
    )));
    assert!(out.saw(&SupervisionEvent::WaitExpired(BoundedWait::LivenessWindow)));
    assert!(out.settlement.stderr().bytes > 0);
    nothing_left(&out);
}

/// D3-T10 and item 15: traffic with no admitted progress, while health
/// holds, is never faulted; the long phase logs absence and completes.
#[test]
fn absent_progress_is_logged_and_never_faulted() {
    let out = outcome_with_waits("slow", progress_absence_waits());
    assert_eq!(
        out.settlement.first_cause(),
        Cause::Clean,
        "{:?}",
        out.events
    );
    assert!(out.saw(&SupervisionEvent::ProgressAbsent));
    assert!(!out.missed());
    assert!(out.saw(&SupervisionEvent::Progress(Progress::FactBatch)));
    nothing_left(&out);
}

// ------------------------------------------------------------------ D3-T2 and NBO-1

/// D3-T2: concurrent triggers in both orders: the earlier is `firstCause`,
/// the later kept. The host's fault reaches the loop only through the
/// handle (LD-D3A-5), here from inside a join (NBO-1's re-entrant request).
#[test]
fn concurrent_triggers_keep_the_first_and_the_later() {
    // The host's fault first, at `Running`.
    let dir = test_dir();
    let hook: Hook = Box::new(|event, handle| {
        if *event == SupervisionEvent::Running {
            assert!(handle.host_fault());
        }
    });
    let (supervision, events) =
        prepared("hang", FixtureParticipant::new(FIXTURE_WAITS), Some(hook));
    let out = finish(supervision, events, &dir);
    assert_eq!(out.settlement.first_cause(), Cause::HostFault);
    assert!(
        out.settlement
            .later_causes()
            .contains(&Cause::ProviderProtocol),
        "{:?}",
        out.settlement.later_causes()
    );
    // The participant's fault first; the host's, appended from inside the
    // join that started the teardown, is kept.
    let dir = test_dir();
    let hook: Hook = Box::new(|event, handle| {
        if *event == SupervisionEvent::TeardownStarted(Cause::ProviderProtocol) {
            assert!(handle.host_fault());
        }
    });
    let (supervision, events) =
        prepared("fault", FixtureParticipant::new(FIXTURE_WAITS), Some(hook));
    let out = finish(supervision, events, &dir);
    assert_eq!(out.settlement.first_cause(), Cause::ProviderProtocol);
    assert!(out.settlement.later_causes().contains(&Cause::HostFault));
    assert_eq!(
        out.count(&SupervisionEvent::Settled(Cause::ProviderProtocol)),
        1
    );
}

/// LD-D3A-5 and r2 (NBO-1), through the public API: once `run` returns
/// settled, a trigger through the handle is counted as a late event and
/// dropped; the one transition into `Settled` is guarded, so a second
/// attempt mints nothing; the settlement is taken once; and `Drop` after the
/// take changes nothing.
#[test]
fn after_settlement_triggers_are_counted_and_dropped() {
    let dir = test_dir();
    let (mut supervision, events) =
        prepared("normal", FixtureParticipant::new(FIXTURE_WAITS), None);
    let handle = supervision.handle();
    let mut root = root_in(&dir);
    supervision.run(&mut root).expect("spawned");
    assert_eq!(supervision.state(), State::Settled);
    assert!(!handle.host_fault(), "dropped");
    assert!(!handle.host_fault(), "dropped");
    assert_eq!(supervision.late_events(), 2);
    supervision.settle();
    assert!(supervision.take_settlement().is_some());
    assert!(supervision.take_settlement().is_none());
    drop(supervision);
    assert!(!handle.host_fault());
    let events = events.borrow();
    let settled = events
        .iter()
        .filter(|(_, e)| matches!(e, SupervisionEvent::Settled(_)))
        .count();
    assert_eq!(settled, 1);
}

// ------------------------------------------------------------------ D3-T3: Drop

/// D3-T3 (r3, NBO-2): `Drop` in each state leaves no child and no scratch
/// for a killable, removable fixture, minting `abandoned`.
#[test]
fn drop_in_each_state_leaves_no_child_and_no_scratch() {
    for at in [
        State::Handshaking,
        State::Running,
        State::Stopping(Cause::ProviderProtocol),
    ] {
        let dir = test_dir();
        let script = if matches!(at, State::Stopping(_)) {
            "fault"
        } else {
            "hang"
        };
        let (mut supervision, events) =
            prepared(script, FixtureParticipant::new(FIXTURE_WAITS), None);
        let mut root = root_in(&dir);
        supervision.start(&mut root).expect("spawned");
        let started = Instant::now();
        while supervision.state() != at {
            assert!(started.elapsed() < control_cap(supervision.waits), "{at:?}");
            supervision.turn();
        }
        let scratch = supervision.seams.scratch.clone().expect("a scratch");
        drop(supervision);
        let events = events.borrow();
        let pid = events
            .iter()
            .find_map(|(_, e)| match e {
                SupervisionEvent::Spawned { process_id } => Some(*process_id),
                _ => None,
            })
            .expect("spawned");
        assert_eq!(
            group_members_bounded(pid, 64).expect("the group"),
            Listing::Complete(Vec::new()),
            "{at:?}"
        );
        assert!(!scratch.exists(), "{at:?}");
        let settled: Vec<&SupervisionEvent> = events
            .iter()
            .map(|(_, e)| e)
            .filter(|e| matches!(e, SupervisionEvent::Settled(_)))
            .collect();
        assert_eq!(settled.len(), 1, "{at:?}");
        assert!(
            events
                .iter()
                .any(|(_, e)| *e == SupervisionEvent::Trigger(Cause::Abandoned))
        );
    }
}

/// D3-T3 (r3, NBO-2): a root surviving the reap ceiling settles finitely
/// with `exit: unreaped`, its scratch kept with the root's hold, and no
/// signal after the one kill; a scratch exhausting its removal budget is
/// `retained {reason: work-exhausted}`.
/// Only the reap ceiling is shortened in the two unreapable-root cases.
#[test]
fn an_unreapable_root_and_an_exhausted_removal_are_disclosed() {
    // In the loop: the ladder's ceiling, then the abandon.
    let dir = test_dir();
    let (mut supervision, events) = prepared("fault", FixtureParticipant::new(FIXTURE_WAITS), None);
    supervision.waits = reap_expiry_waits();
    supervision.seams.reap_blocked = true;
    let out = finish(supervision, events, &dir);
    assert_eq!(out.settlement.exit(), ExitClass::Unreaped);
    assert_eq!(
        out.settlement.scratch(),
        ScratchFate::Retained(ScratchRetained::RootUnreaped)
    );
    assert!(out.saw(&SupervisionEvent::WaitExpired(BoundedWait::ReapCeiling)));
    assert!(out.saw(&SupervisionEvent::Abandoned));
    let abandoned = out.position(&SupervisionEvent::Abandoned);
    assert!(
        !out.events[abandoned..]
            .iter()
            .any(|(_, e)| matches!(e, SupervisionEvent::Signalled { .. })),
        "no signal after the abandon"
    );
    // On Drop: one kill, the reap polled to the ceiling, then the abandon.
    let dir = test_dir();
    let (mut supervision, events) = prepared("hang", FixtureParticipant::new(FIXTURE_WAITS), None);
    supervision.waits = reap_expiry_waits();
    supervision.seams.reap_blocked = true;
    let mut root = root_in(&dir);
    supervision.start(&mut root).expect("spawned");
    let started = Instant::now();
    while supervision.state() != State::Running {
        assert!(started.elapsed() < control_cap(quick()), "never running");
        supervision.turn();
    }
    let started = Instant::now();
    drop(supervision);
    assert!(
        started.elapsed() < control_cap(reap_expiry_waits()),
        "finite"
    );
    let events = events.borrow();
    let kills = events
        .iter()
        .filter(|(_, e)| matches!(e, SupervisionEvent::Signalled { .. }))
        .count();
    assert_eq!(kills, 1, "kill once");
    assert!(
        events
            .iter()
            .any(|(_, e)| *e == SupervisionEvent::Abandoned)
    );
    // The removal budget exhausted.
    let dir = test_dir();
    let (mut supervision, events) = prepared(
        "scratch-files",
        FixtureParticipant::new(FIXTURE_WAITS),
        None,
    );
    supervision.seams.removal_limits = Some(WorkCost {
        objects: 16,
        edges: 64,
        bytes: 4096,
    });
    let out = finish(supervision, events, &dir);
    assert_eq!(out.settlement.first_cause(), Cause::Clean);
    assert_eq!(
        out.settlement.scratch(),
        ScratchFate::Retained(ScratchRetained::WorkExhausted)
    );
    assert!(
        out.settlement.admissible(),
        "cleanup never changes admission"
    );
}

// ------------------------------------------------------------------ waits, I/O and stderr

/// D3-T7: the waits the other controls do not reach: TERM to KILL, the
/// drain, and the ceiling's own expiry above.
#[test]
fn the_term_to_kill_and_drain_waits_expire_with_their_events() {
    // The drain: a group member holds fd1 past it after the root exits.
    let dir = test_dir();
    let (mut supervision, events) = prepared(
        "normal-exit-first",
        FixtureParticipant::new(FIXTURE_WAITS),
        None,
    );
    supervision.waits = drain_expiry_waits();
    let out = finish(supervision, events, &dir);
    assert!(out.saw(&SupervisionEvent::WaitExpired(BoundedWait::Drain)));
    assert_eq!(
        out.settlement.first_cause(),
        Cause::Clean,
        "{:?}",
        out.events
    );
    // TERM to KILL: a group member survives SIGTERM, so the escalation's
    // wait expires and SIGKILL follows.
    let out = outcome_with_waits("term-survivor", wall_clock_expiry_waits());
    assert!(out.saw(&SupervisionEvent::WaitExpired(BoundedWait::WallClock)));
    assert!(out.saw(&SupervisionEvent::Signalled { signal: SIGTERM }));
    assert!(out.saw(&SupervisionEvent::WaitExpired(BoundedWait::TermToKill)));
    assert!(out.saw(&SupervisionEvent::Signalled { signal: SIGKILL }));
    assert!(
        out.position(&SupervisionEvent::Signalled { signal: SIGTERM })
            < out.position(&SupervisionEvent::Signalled { signal: SIGKILL })
    );
}

/// D3-T8 and LD-D3A-7: the protocol waits are the participant's, Rust3's
/// 5,000 ms and TS2's 2 s each taken unchanged, never substituted.
#[test]
fn the_protocol_waits_are_the_participants_own() {
    let rust3 = ProtocolWaits {
        stage1_cancel_grace: Duration::from_millis(5_000),
        normal_exit_grace: Duration::from_millis(5_000),
    };
    for waits in [rust3, ProtocolWaits::TS2] {
        let (supervision, _) = prepared("normal", FixtureParticipant::new(waits), None);
        assert_eq!(supervision.protocol_waits(), Some(waits));
        drop(supervision);
    }
    assert_eq!(
        ProtocolWaits::TS2.stage1_cancel_grace,
        Duration::from_secs(2)
    );
    assert_ne!(
        rust3.stage1_cancel_grace,
        ProtocolWaits::TS2.stage1_cancel_grace
    );
}

/// Resumable provider I/O (RF-1): frames written a byte at a time and
/// coalesced, control frames a byte at a time, and a large host frame to a
/// slow reader resumed at its offset across short writes and `WouldBlock`,
/// with health serviced throughout; each turn calls the participant's read
/// once (the yield contract).
#[test]
fn split_and_coalesced_frames_and_blocked_writes_resume() {
    for script in ["split", "slow-reader"] {
        let dir = test_dir();
        let mut participant = FixtureParticipant::new(FIXTURE_WAITS);
        if script == "slow-reader" {
            participant.chunk = Some(300_000);
        }
        let (supervision, events) = prepared(script, participant, None);
        let out = finish(supervision, events, &dir);
        assert_eq!(
            out.settlement.first_cause(),
            Cause::Clean,
            "{script}: {:?}",
            out.events
        );
        assert!(!out.missed(), "{script}");
        assert_eq!(out.max_reads_per_turn, 1, "{script}: one read per turn");
        nothing_left(&out);
    }
}

/// Item 17 and OPP:431: a flood of ten times the bound is counted exactly,
/// truncated, never a fault; the producer is never blocked. No stderr byte
/// is held: the reader reads into one fixed buffer and keeps nothing.
#[test]
fn a_stderr_flood_is_counted_exactly_and_never_held() {
    let out = outcome("flood-stderr");
    assert_eq!(out.settlement.first_cause(), Cause::Clean);
    assert_eq!(
        out.settlement.stderr(),
        StderrCount {
            bytes: 10 * 262_144,
            truncated: true,
        }
    );
    let source = include_str!("supervisor.rs");
    let start = source.find("fn service_stderr").expect("the reader");
    let end = start + source[start..].find("\n    }\n").expect("its end");
    let body = &source[start..end];
    assert!(body.contains("fd.read(&mut self.stderr_buf)"));
    for kept in ["Vec", "to_vec", "extend", "push", "String", "clone"] {
        assert!(
            !body.contains(kept),
            "the stderr reader keeps no byte: {kept}"
        );
    }
    assert!(source.contains("stderr_buf: [u8; STDERR_BUFFER],"));
}

/// LD-D3A-4: the control reader reassembles a frame split at every byte
/// offset, and two frames coalesced in one stream, the same; an over-bound
/// prefix is refused from its four bytes alone, with nothing more read.
#[test]
fn the_control_reader_reassembles_any_split_and_stops_at_an_over_bound_prefix() {
    /// A non-blocking source: at each cut it first reports `WouldBlock`.
    struct Pieces {
        data: Vec<u8>,
        cuts: Vec<usize>,
        at: usize,
        blocked_at: Option<usize>,
    }
    impl Read for Pieces {
        fn read(&mut self, buf: &mut [u8]) -> io::Result<usize> {
            if self.at == self.data.len() {
                return Ok(0);
            }
            if self.cuts.contains(&self.at) && self.blocked_at != Some(self.at) {
                self.blocked_at = Some(self.at);
                return Err(io::Error::new(io::ErrorKind::WouldBlock, "a cut"));
            }
            let next = self
                .cuts
                .iter()
                .copied()
                .find(|c| *c > self.at)
                .unwrap_or(self.data.len());
            let n = buf.len().min(next - self.at);
            buf[..n].copy_from_slice(&self.data[self.at..self.at + n]);
            self.at += n;
            Ok(n)
        }
    }
    let frame = |json: &str| {
        let mut f = (json.len() as u32).to_be_bytes().to_vec();
        f.extend_from_slice(json.as_bytes());
        f
    };
    let first = frame(r#"{"type":"shutdownAck","seq":1,"controlMajor":1,"body":{}}"#);
    let second = frame(
        r#"{"type":"healthReport","seq":2,"controlMajor":1,"body":{"nonce":"h1","status":"busy"}}"#,
    );
    let stream: Vec<u8> = first.iter().chain(&second).copied().collect();
    let frames_of = |cuts: Vec<usize>| {
        let mut reader = ControlReader::new(HOST_BOUND);
        let mut source = Pieces {
            data: stream.clone(),
            cuts,
            at: 0,
            blocked_at: None,
        };
        let mut frames = Vec::new();
        loop {
            match reader.read(&mut source, HOST_BOUND).expect("a read") {
                ControlRead::Frame(len) => frames.push(reader.buf[..len].to_vec()),
                ControlRead::Eof(cut) => {
                    assert!(!cut);
                    return frames;
                }
                ControlRead::Pending => {}
                ControlRead::OverBound => panic!("in bound"),
            }
        }
    };
    let whole = vec![first.clone(), second.clone()];
    for cut in 1..stream.len() {
        assert_eq!(frames_of(vec![cut]), whole, "split at {cut}");
    }
    assert_eq!(
        frames_of((1..stream.len()).collect()),
        whole,
        "byte at a time"
    );
    assert_eq!(frames_of(Vec::new()), whole, "coalesced");
    let mut over = (HOST_BOUND + 1).to_be_bytes().to_vec();
    over.extend_from_slice(&[b'x'; 100]);
    let mut source = Pieces {
        data: over,
        cuts: Vec::new(),
        at: 0,
        blocked_at: None,
    };
    let mut reader = ControlReader::new(HOST_BOUND);
    assert!(matches!(
        reader.read(&mut source, HOST_BOUND).expect("a read"),
        ControlRead::OverBound
    ));
    assert_eq!(source.at, 4, "nothing past the prefix is read");
}
const HOST_BOUND: u32 = crate::control_protocol::HOST_FRAME_BOUND;

/// LD-D3A-6: a caller that may need a D3b ladder is refused before spawn.
#[test]
fn a_caller_needing_a_d3b_ladder_is_refused() {
    let mut spec = spec_for(Path::new("/nonexistent"), "normal");
    spec.needs_d3b_ladders = true;
    assert!(matches!(
        Supervision::prepare(spec, FixtureParticipant::new(FIXTURE_WAITS)),
        Err(SupervisorError::LadderUnavailable)
    ));
}

// ------------------------------------------------------------------ round 2 (Codex codex-d3a-1-r1)

type Setup = fn(&mut Supervision<FixtureParticipant>);

/// Run `script` on its own thread, configured by `setup`; the test fails if
/// it does not settle within its wait-derived cap, so a starved loop cannot hang it.
fn threaded(script: &'static str, setup: Setup, waits: Waits) -> Outcome {
    let cap = control_cap(waits);
    let (done, finished) = mpsc::channel();
    std::thread::spawn(move || {
        let dir = test_dir();
        let (mut supervision, events) =
            prepared(script, FixtureParticipant::new(FIXTURE_WAITS), None);
        supervision.waits = waits;
        setup(&mut supervision);
        let out = finish(supervision, events, &dir);
        done.send(out).ok();
    });
    finished
        .recv_timeout(cap)
        .unwrap_or_else(|_| panic!("{script}: no settlement within {cap:?}"))
}

/// r2 (Codex D3A1-R1-RF-1): an always-ready stderr (`/dev/zero`, never at
/// EOF) is serviced a bounded number of reads per turn, so the wall-clock
/// deadline, health and the ladder still advance and the child settles.
#[test]
fn an_always_ready_stderr_cannot_starve_the_loop() {
    let out = threaded(
        "hang",
        |s| s.seams.stderr_zero = true,
        wall_clock_expiry_waits(),
    );
    assert_eq!(out.settlement.first_cause(), Cause::Deadline);
    assert!(out.saw(&SupervisionEvent::WaitExpired(BoundedWait::WallClock)));
    assert!(!out.missed(), "health serviced");
    assert!(out.settlement.stderr().truncated);
    assert!(out.max_stderr_reads_per_turn <= STDERR_READS_PER_TURN);
    assert!(out.max_stderr_reads_per_turn > 0);
}

/// r2 (RF-1): sustained control traffic (back-to-back resource reports, no
/// health answered) is serviced a bounded number of reads per turn; the
/// liveness window still expires: traffic is not liveness (item 15).
#[test]
fn sustained_control_traffic_cannot_starve_liveness() {
    let out = threaded("control-storm", |_| {}, liveness_expiry_waits());
    assert_eq!(out.settlement.first_cause(), Cause::Liveness);
    assert!(out.saw(&SupervisionEvent::LivenessMissed(
        LivenessMiss::WindowExpired
    )));
    assert!(out.max_control_reads_per_turn <= CONTROL_READS_PER_TURN);
    nothing_left(&out);
}

/// r2 (RF-1): a thread refilling the trigger channel without pause is
/// consumed a bounded number per turn; the supervision still settles.
#[test]
fn a_trigger_storm_is_consumed_a_bounded_number_per_turn() {
    let (done, finished) = mpsc::channel();
    std::thread::spawn(move || {
        let dir = test_dir();
        let (supervision, events) = prepared("hang", FixtureParticipant::new(FIXTURE_WAITS), None);
        let handle = supervision.handle();
        let stop = Arc::new(AtomicBool::new(false));
        let storm = Arc::clone(&stop);
        let spammer = std::thread::spawn(move || {
            while !storm.load(Ordering::Acquire) {
                handle.host_fault();
            }
        });
        let out = finish(supervision, events, &dir);
        stop.store(true, Ordering::Release);
        spammer.join().ok();
        done.send(out).ok();
    });
    let out = finished
        .recv_timeout(control_cap(quick()))
        .expect("settled under a trigger storm");
    assert_eq!(out.settlement.first_cause(), Cause::HostFault);
    nothing_left(&out);
}

/// r2 (RF-2): a fully joined clean end whose root cannot be reaped settles
/// at its own reap ceiling, once, `unreaped`, its scratch retained with the
/// root (LD-D3A-18) and nothing admissible.
#[test]
fn a_clean_end_that_cannot_be_reaped_settles_at_its_ceiling() {
    let out = threaded(
        "normal",
        |s| s.seams.reap_blocked = true,
        reap_expiry_waits(),
    );
    assert_eq!(out.settlement.first_cause(), Cause::Clean);
    assert_eq!(out.settlement.exit(), ExitClass::Unreaped);
    assert!(out.saw(&SupervisionEvent::WaitExpired(BoundedWait::ReapCeiling)));
    assert_eq!(
        out.settlement.scratch(),
        ScratchFate::Retained(ScratchRetained::RootUnreaped)
    );
    assert!(!out.settlement.admissible());
    assert_eq!(out.count(&SupervisionEvent::Settled(Cause::Clean)), 1);
}

/// r2 (RF-4): the terminal arrives while an older control frame (a health
/// request) is still pending: the shutdown waits for it, and for its report,
/// then goes exactly once, and the end is clean. Short writes (one byte each)
/// resume across turns too.
#[test]
fn the_shutdown_waits_for_a_pending_frame_and_goes_once() {
    let out = threaded(
        "slow",
        |s| {
            s.seams.stall_control_writes_in_running = true;
        },
        pending_health_waits(),
    );
    assert_eq!(
        out.settlement.first_cause(),
        Cause::Clean,
        "{:?}",
        out.events
    );
    assert_eq!(out.count(&SupervisionEvent::ControlSent("shutdown")), 1);
    assert!(
        out.position(&SupervisionEvent::ControlSent("health"))
            < out.position(&SupervisionEvent::ControlSent("shutdown"))
    );
    let out = threaded("normal", |s| s.seams.control_write_chunk = Some(1), quick());
    assert_eq!(
        out.settlement.first_cause(),
        Cause::Clean,
        "{:?}",
        out.events
    );
    assert_eq!(out.count(&SupervisionEvent::ControlSent("shutdown")), 1);
}

/// r2 (RF-6): a busy report is live; a report with the wrong nonce is a
/// liveness fault (D2a's typed RF7 detail), not a control refusal; an
/// unrelated RF7 (a sequence gap) stays a control refusal.
#[test]
fn health_report_nonce_mismatch_is_liveness_and_other_rf7_is_not() {
    let out = outcome("normal");
    assert_eq!(out.settlement.first_cause(), Cause::Clean);
    assert!(!out.missed(), "busy is live");
    let out = outcome("bad-nonce");
    assert_eq!(
        out.settlement.first_cause(),
        Cause::Liveness,
        "{:?}",
        out.events
    );
    // r3 (NBO-1): the reduced provenance, the mismatch and the control
    // owner's family, never the window's expiry.
    assert!(out.saw(&SupervisionEvent::LivenessMissed(
        LivenessMiss::NonceMismatch(RefusalFamily::Rf7)
    )));
    assert!(!out.saw(&SupervisionEvent::LivenessMissed(
        LivenessMiss::WindowExpired
    )));
    assert!(
        !out.settlement
            .later_causes()
            .contains(&Cause::ControlRefusal(RefusalFamily::Rf7))
    );
    let out = outcome("bad-seq");
    assert_eq!(
        out.settlement.first_cause(),
        Cause::ControlRefusal(RefusalFamily::Rf7),
        "{:?}",
        out.events
    );
    assert!(!out.missed());
    nothing_left(&out);
}

/// r2 (RF-7; LD-D3A-19): a component's accepted control `fault` report is
/// `provider-protocol`. The provider's bytes are delivered unchanged, and the
/// participant sees only the protocols' own process events: no deadline and
/// no invented event.
#[test]
fn an_accepted_control_fault_is_provider_protocol() {
    let out = outcome("control-fault");
    assert_eq!(
        out.settlement.first_cause(),
        Cause::ProviderProtocol,
        "{:?}",
        out.events
    );
    assert!(out.saw(&SupervisionEvent::ControlReceived("fault")));
    let hello_ack = write_frame(&Value::Map(vec![(
        "type".to_owned(),
        Value::Text("HelloAck".to_owned()),
    )]))
    .expect("a frame");
    assert_eq!(out.raw, hello_ack, "the provider's bytes, unchanged");
    for (_, event) in &out.events {
        if let SupervisionEvent::Delivered(delivered) = event {
            assert!(
                matches!(
                    delivered,
                    ProcessEvent::Eof | ProcessEvent::Fault(ProcessFault::SignalDeath)
                ),
                "{delivered:?}"
            );
        }
    }
    nothing_left(&out);
}

/// r2 (RF-8): a root that dies on its own before its terminal, with fd1
/// held briefly inside the drain, first faults on the EOF (`provider-
/// protocol`), and its independent death is kept as a later
/// `unexpected-exit`; a death the ladder caused is never one.
#[test]
fn an_independent_early_death_is_kept_after_the_eof_fault() {
    let out = outcome("early-exit-brief-hold");
    assert_eq!(
        out.settlement.first_cause(),
        Cause::ProviderProtocol,
        "{:?}",
        out.events
    );
    assert!(
        out.settlement
            .later_causes()
            .contains(&Cause::UnexpectedExit),
        "{:?}",
        out.settlement.later_causes()
    );
    let out = outcome("eof-early");
    assert_eq!(out.settlement.first_cause(), Cause::ProviderProtocol);
    assert!(
        !out.settlement
            .later_causes()
            .contains(&Cause::UnexpectedExit)
    );
}

/// r2 (RF-9): the killed group is confirmed against the zombie root before
/// the reap: a root alone is `group-killed, platform-limited`; a member the
/// kill missed leaves it `incomplete`.
#[test]
fn the_tree_is_confirmed_before_the_reap() {
    let out = outcome("fault");
    let e = out.settlement.tree_evidence().expect("kill evidence");
    assert_eq!(e.confirm, ConfirmOutcome::RootAlone);
    // macOS can refuse killpg on the held zombie with EPERM. A confirmed
    // singleton never turns that failed native send into a successful one.
    assert!(
        e.failures
            .iter()
            .all(|failure| failure.step == TreeCall::GroupKill)
    );
    let want = if e.group_kill_failures == 0 {
        TreeReport::GroupKilledPlatformLimited
    } else {
        TreeReport::IncompletePlatformLimited
    };
    assert_eq!(out.settlement.tree(), want, "{e:?}");
    let observed = out
        .events
        .iter()
        .position(|(_, event)| *event == SupervisionEvent::ExitObserved)
        .expect("exit observed");
    let reaped = out
        .events
        .iter()
        .position(|(_, event)| *event == SupervisionEvent::Reaped)
        .expect("reaped");
    assert!(observed < reaped);
    let out = threaded("fault", |s| s.seams.extra_member = true, quick());
    assert_eq!(out.settlement.tree(), TreeReport::IncompletePlatformLimited);
}

// ------------------------------------------------------------------ r3

/// r3 (Codex D3A1-R2-RF-1): an unwind (`Drop`) from Handshaking, Running and
/// Stopping marks its kill before the first reap attempt, so the group is
/// confirmed against the still-unreaped root: a root alone is
/// `group-killed, platform-limited`; a member the kill missed leaves it
/// `incomplete`. The settlement `Drop` makes is handed to the test.
#[test]
fn an_unwind_confirms_the_tree_before_its_reap() {
    for extra_member in [false, true] {
        for at in [
            State::Handshaking,
            State::Running,
            State::Stopping(Cause::ProviderProtocol),
        ] {
            let dir = test_dir();
            let script = if matches!(at, State::Stopping(_)) {
                "fault"
            } else {
                "hang"
            };
            let (mut supervision, _events) =
                prepared(script, FixtureParticipant::new(FIXTURE_WAITS), None);
            let (sink, unwound) = mpsc::channel();
            supervision.seams.unwound = Some(sink);
            supervision.seams.extra_member = extra_member;
            let mut root = root_in(&dir);
            supervision.start(&mut root).expect("spawned");
            let started = Instant::now();
            while supervision.state() != at {
                assert!(started.elapsed() < control_cap(supervision.waits), "{at:?}");
                supervision.turn();
            }
            drop(supervision);
            let settlement = unwound
                .recv_timeout(Duration::from_secs(1))
                .expect("the unwind's settlement");
            let e = settlement.tree_evidence().expect("kill evidence");
            assert!(
                e.failures
                    .iter()
                    .all(|failure| failure.step == TreeCall::GroupKill)
            );
            if !extra_member {
                assert_eq!(e.confirm, ConfirmOutcome::RootAlone);
            }
            let want = if extra_member || e.group_kill_failures > 0 {
                TreeReport::IncompletePlatformLimited
            } else {
                TreeReport::GroupKilledPlatformLimited
            };
            assert_eq!(
                settlement.tree(),
                want,
                "{at:?}, extra {extra_member}: {:?}",
                settlement.tree_evidence()
            );
            if !matches!(at, State::Stopping(_)) {
                assert!(
                    matches!(settlement.exit(), ExitClass::Signaled(9)),
                    "{at:?}: {:?}",
                    settlement.exit()
                );
            }
            assert!(unwound.try_recv().is_err(), "one settlement");
        }
    }
}

/// r3 (Codex D3A1-R2-RF-2): admission and the settlement's close are one
/// linearization. A sender paused between its closed check and its append
/// holds the close off; the close then drains and counts it, and nothing
/// is left queued unaccounted. A request after the close is refused and
/// counted exactly once, with no consumer turn.
#[test]
fn admission_and_the_close_are_one_linearization() {
    let pause = Arc::new((Barrier::new(2), Barrier::new(2)));
    let mut gate = TriggerGate::new();
    gate.pause = Some(Arc::clone(&pause));
    let gate = Arc::new(gate);
    let admitting = Arc::clone(&gate);
    let sender = std::thread::spawn(move || admitting.admit(Trigger::HostFault));
    // The sender has passed its closed check and not yet appended.
    pause.0.wait();
    let closing = Arc::clone(&gate);
    let (closed, close_done) = mpsc::channel();
    let closer = std::thread::spawn(move || {
        let drained = closing.close();
        closed.send(()).ok();
        drained
    });
    assert!(
        close_done.recv_timeout(Duration::from_millis(300)).is_err(),
        "the close completed between a sender's check and its append"
    );
    pause.1.wait();
    assert!(
        sender.join().expect("the sender"),
        "admitted before the close"
    );
    assert_eq!(
        closer.join().expect("the closer"),
        1,
        "drained by the close"
    );
    assert_eq!(gate.late(), 1, "counted by the close");
    assert!(gate.take().is_none(), "nothing queued unaccounted");

    // After the close: refused, counted once each, nothing queued.
    let gate = TriggerGate::new();
    assert_eq!(gate.close(), 0);
    assert!(!gate.admit(Trigger::HostFault));
    assert_eq!(gate.late(), 1);
    assert!(!gate.admit(Trigger::HostFault));
    assert_eq!(gate.late(), 2);
    assert!(gate.take().is_none());

    // Before the close: bounded, never blocking on a consumer.
    let gate = TriggerGate::new();
    for _ in 0..TRIGGER_CAPACITY {
        assert!(gate.admit(Trigger::HostFault));
    }
    assert!(!gate.admit(Trigger::HostFault), "full: not appended");
    assert_eq!(gate.late(), 0, "a full gate is not late");
    assert_eq!(gate.close(), TRIGGER_CAPACITY);
    assert_eq!(gate.late(), TRIGGER_CAPACITY as u64);
}

/// r3 (RF-2): through the public handle, from another thread, around the
/// real settlement: each request is either merged into the settlement as a
/// trigger, or drained at the close, or refused after it, and the counts
/// add up; none is lost.
#[test]
fn every_handle_request_is_merged_drained_or_refused() {
    let dir = test_dir();
    let (mut supervision, events) =
        prepared("normal", FixtureParticipant::new(FIXTURE_WAITS), None);
    let handle = supervision.handle();
    let stop = Arc::new(AtomicBool::new(false));
    let stopping = Arc::clone(&stop);
    let requester = std::thread::spawn(move || {
        let mut accepted = 0u64;
        let mut refused = 0u64;
        let mut sent = 0u64;
        let started = Instant::now();
        while !stopping.load(Ordering::Acquire) && started.elapsed() < control_cap(quick()) {
            sent += 1;
            if handle.host_fault() {
                accepted += 1;
            } else {
                refused += 1;
            }
            std::thread::yield_now();
        }
        // Past the close: every one refused and counted.
        for _ in 0..3 {
            sent += 1;
            if handle.host_fault() {
                accepted += 1;
            } else {
                refused += 1;
            }
        }
        (accepted, refused, sent)
    });
    let mut root = root_in(&dir);
    supervision.run(&mut root).expect("spawned");
    stop.store(true, Ordering::Release);
    let (accepted, _refused, sent) = requester.join().expect("the requester");
    assert!(sent > 0);
    let events = events.borrow();
    let merged = events
        .iter()
        .filter(|(_, e)| *e == SupervisionEvent::Trigger(Cause::HostFault))
        .count() as u64;
    let drained = events
        .iter()
        .filter(|(_, e)| *e == SupervisionEvent::LateEvent)
        .count() as u64;
    assert_eq!(accepted, merged + drained, "every admitted one accounted");
    assert!(supervision.late_events() >= drained + 3);
    assert!(supervision.take_settlement().is_some());
}

// ------------------------------------------------------------------ D3a-2: item 16 (D3-T13 to T16)

/// A provider supervision over `script` whose item 16 limits `limits`
/// adjusts, driven to its settlement on its own thread.
fn bounded(
    script: &'static str,
    participant: fn() -> FixtureParticipant,
    limits: fn(&mut Limits),
) -> Outcome {
    let (done, finished) = mpsc::channel();
    std::thread::spawn(move || {
        let dir = test_dir();
        let (mut supervision, events) = prepared(script, participant(), None);
        limits(&mut supervision.limits);
        let out = finish(supervision, events, &dir);
        done.send(out).ok();
    });
    finished
        .recv_timeout(control_cap(quick()))
        .unwrap_or_else(|_| panic!("{script}: no settlement"))
}
fn fixture_participant() -> FixtureParticipant {
    FixtureParticipant::new(FIXTURE_WAITS)
}
/// A resident-memory ceiling below the fixture's 96 MiB and above its own
/// baseline, sampled every 20 ms.
fn low_ceiling(limits: &mut Limits) {
    limits.resident_memory = 48 << 20;
    limits.memory_sample_interval = Duration::from_millis(20);
}

/// The item 16 constants, each as its row states it (:528-549).
#[test]
fn item_16s_constants_are_the_laws() {
    assert_eq!(RESIDENT_MEMORY_CEILING, 8_589_934_592);
    assert_eq!(MEMORY_SAMPLE_INTERVAL, Duration::from_millis(250));
    assert_eq!((PROVIDER_PROCESSES, TOOL_PROCESSES), (1, 16));
    assert_eq!(TS2_RESPONSE_BYTES, 1_073_741_824);
    assert_eq!(RUST3_SCRATCH_BYTES, 2_147_483_648);
    assert_eq!(TS2_SCRATCH_BYTES, 2_147_483_648);
    assert_eq!(TOOL_OUTPUT_BYTES, 268_435_456);
    assert_eq!(ToolMaterialization::LIMIT, 34_359_738_368 + 1_073_741_824);
    assert_eq!(WALL_CLOCK_TOOL, Duration::from_secs(300));
    assert_eq!(Waits::TOOL.wall_clock, WALL_CLOCK_TOOL);
    assert_eq!(
        Waits {
            wall_clock: WALL_CLOCK_PROVIDER,
            ..Waits::TOOL
        },
        Waits::RELEASE
    );
}

/// D3-T13: a fixture allocating past the ceiling is killed with
/// `memory-ceiling`; an asserted value above it is a breach; an asserted
/// value below it never clears an observed breach (item 16, :531).
#[test]
fn the_memory_ceiling_is_observed_or_asserted() {
    for script in ["allocate", "assert-small"] {
        let out = bounded(script, fixture_participant, low_ceiling);
        assert_eq!(
            out.settlement.first_cause(),
            Cause::MemoryCeiling,
            "{script}: {:?}",
            out.events
        );
        assert_eq!(
            out.count(&SupervisionEvent::LimitBreached(LimitKind::ResidentMemory)),
            1,
            "{script}"
        );
        assert_ne!(out.settlement.tree(), TreeReport::NotKilled, "{script}");
        nothing_left(&out);
    }
    let out = bounded("assert-large", fixture_participant, |_| {});
    assert_eq!(out.settlement.first_cause(), Cause::MemoryCeiling);
    nothing_left(&out);
    // Under the release ceiling the same fixture is never a breach.
    let out = bounded("normal", fixture_participant, |l| {
        l.memory_sample_interval = Duration::from_millis(20)
    });
    assert_eq!(out.settlement.first_cause(), Cause::Clean);
    assert!(!out.saw(&SupervisionEvent::LimitBreached(LimitKind::ResidentMemory)));
}

/// D3-T14: a second process in a provider's tree is `process-count`.
#[test]
fn a_second_process_in_a_provider_tree_is_process_count() {
    let out = bounded("fork", fixture_participant, |l| {
        l.memory_sample_interval = Duration::from_millis(20)
    });
    assert_eq!(
        out.settlement.first_cause(),
        Cause::ProcessCount,
        "{:?}",
        out.events
    );
    assert_eq!(
        out.count(&SupervisionEvent::LimitBreached(LimitKind::ProcessCount)),
        1
    );
    nothing_left(&out);
}

/// D3-T15: stderr exactly at its threshold is not truncated, one byte past
/// it is, and neither is a fault (item 16, :545; item 17).
#[test]
fn stderr_at_and_past_its_threshold() {
    for (script, truncated) in [("stderr-at", false), ("stderr-over", true)] {
        let out = outcome(script);
        assert_eq!(out.settlement.first_cause(), Cause::Clean, "{script}");
        assert_eq!(
            out.settlement.stderr(),
            StderrCount {
                bytes: if truncated { 262_145 } else { 262_144 },
                truncated
            },
            "{script}"
        );
    }
}

/// D3-T16 and D3-T15: a TS2 stream whose admitted payload bytes, counted
/// from the participant's accounting, pass 1 GiB is `byte-bound(response)`;
/// exactly 1 GiB is not. Rust3's totals are its codec's, so the same
/// accounting under Rust3 is never D3's bound.
#[test]
fn ts2s_response_bound_is_counted_from_the_participant() {
    fn ts2(claim: u64) -> FixtureParticipant {
        let mut participant = FixtureParticipant::new(FIXTURE_WAITS);
        participant.protocol = Protocol::Ts2;
        participant.fact_batch_claim = Some(claim);
        participant
    }
    let out = bounded("normal", || ts2(TS2_RESPONSE_BYTES), |_| {});
    assert_eq!(out.settlement.first_cause(), Cause::Clean);
    assert!(!out.saw(&SupervisionEvent::LimitBreached(LimitKind::Response)));
    let out = bounded("normal", || ts2(TS2_RESPONSE_BYTES + 1), |_| {});
    assert_eq!(
        out.settlement.first_cause(),
        Cause::ByteBound(ByteBound::Response),
        "{:?}",
        out.events
    );
    assert!(!out.settlement.admissible());
    nothing_left(&out);
    let out = bounded(
        "normal",
        || {
            let mut participant = ts2(TS2_RESPONSE_BYTES + 1);
            participant.protocol = Protocol::Rust3;
            participant
        },
        |_| {},
    );
    assert_eq!(out.settlement.first_cause(), Cause::Clean);
}

/// The zero-fit refusal (item 16, :534): a memory budget one byte below the
/// ceiling is refused before anything is spawned, and the ceiling is never
/// lowered; at the ceiling the supervision is prepared.
#[test]
fn a_budget_below_one_ceiling_is_refused_before_spawn() {
    let mut spec = spec_for(Path::new("/nonexistent"), "normal");
    spec.memory_budget_bytes = RESIDENT_MEMORY_CEILING - 1;
    assert!(matches!(
        Supervision::prepare(spec, FixtureParticipant::new(FIXTURE_WAITS)),
        Err(SupervisorError::MemoryBudgetBelowCeiling {
            budget,
            ceiling: RESIDENT_MEMORY_CEILING,
        }) if budget == RESIDENT_MEMORY_CEILING - 1
    ));
    let spec = spec_for(Path::new("/nonexistent"), "normal");
    let supervision =
        Supervision::prepare(spec, FixtureParticipant::new(FIXTURE_WAITS)).expect("at the ceiling");
    assert_eq!(supervision.limits.resident_memory, RESIDENT_MEMORY_CEILING);
    assert_eq!(supervision.state(), State::Prepared);
    let mut tool = tool_spec_for(Path::new("/nonexistent"), "tool-ok");
    tool.memory_budget_bytes = RESIDENT_MEMORY_CEILING - 1;
    assert!(matches!(
        Supervision::prepare_tool(tool),
        Err(SupervisorError::MemoryBudgetBelowCeiling { .. })
    ));
}

/// Item 16's scratch measurement at settlement (LD-D3A-12): the fixture's
/// 100 one-byte files exactly at the limit settle `clean`; one byte under
/// it, or the walk's ledger exhausted, is `scratch-bound`, which the clean
/// end becomes (DRJ2:125). The scratch is still removed.
#[test]
fn the_scratch_is_measured_at_settlement() {
    let out = bounded("scratch-files", fixture_participant, |l| {
        l.rust3_scratch = 100
    });
    assert_eq!(out.settlement.first_cause(), Cause::Clean);
    assert!(out.settlement.admissible());
    let out = bounded("scratch-files", fixture_participant, |l| {
        l.rust3_scratch = 99
    });
    assert_eq!(out.settlement.first_cause(), Cause::ScratchBound);
    assert!(out.saw(&SupervisionEvent::LimitBreached(LimitKind::Scratch)));
    assert!(!out.settlement.admissible());
    assert_eq!(out.settlement.scratch(), ScratchFate::Removed);
    let out = threaded(
        "scratch-files",
        |s| {
            s.seams.measure_limits = Some(WorkCost {
                objects: 16,
                edges: 64,
                bytes: 4096,
            })
        },
        quick(),
    );
    assert_eq!(out.settlement.first_cause(), Cause::ScratchBound);
    // TS2's limit is its own.
    let out = bounded(
        "scratch-files",
        || {
            let mut participant = FixtureParticipant::new(FIXTURE_WAITS);
            participant.protocol = Protocol::Ts2;
            participant
        },
        |l| {
            l.rust3_scratch = 99;
            l.ts2_scratch = 100;
        },
    );
    assert_eq!(out.settlement.first_cause(), Cause::Clean);
}

/// LD-D3A-16 (Codex D3A-plan RF-7): tool materialization's accounting.
/// Charges reaching exactly 32 GiB + 1 GiB admit; one byte more refuses
/// `ToolScratchBound` and changes nothing, so no write is made; the
/// provider's 2 GiB scratch limit is never applied (the wrong-limit
/// control).
#[test]
fn tool_materialization_is_charged_before_each_write() {
    let mut materialization = ToolMaterialization::new();
    for _ in 0..33 {
        materialization.charge(1 << 30).expect("within the limit");
    }
    assert_eq!(materialization.total(), ToolMaterialization::LIMIT);
    assert_eq!(
        materialization.charge(1),
        Err(ToolScratchBound {
            observed: ToolMaterialization::LIMIT + 1,
            limit: ToolMaterialization::LIMIT,
        })
    );
    assert_eq!(
        materialization.total(),
        ToolMaterialization::LIMIT,
        "nothing charged"
    );
    assert_eq!(
        materialization.charge(u64::MAX),
        Err(ToolScratchBound {
            observed: u64::MAX,
            limit: ToolMaterialization::LIMIT,
        })
    );
    assert_eq!(materialization.total(), ToolMaterialization::LIMIT);
    let mut materialization = ToolMaterialization::new();
    materialization
        .charge(RUST3_SCRATCH_BYTES + 1)
        .expect("past a provider's scratch limit, within the tool's");
    assert_ne!(ToolMaterialization::LIMIT, RUST3_SCRATCH_BYTES);
}

/// Item 16, :548: the tool output accounting at its release bound: exactly
/// 256 MiB admits, one byte more refuses `ToolOutputBound` with the total
/// unchanged.
#[test]
fn tool_output_is_charged_exactly_to_its_bound() {
    let mut output = ToolOutput::new();
    output.charge(TOOL_OUTPUT_BYTES).expect("at the bound");
    assert_eq!(
        output.charge(1),
        Err(ToolOutputBound {
            observed: TOOL_OUTPUT_BYTES + 1,
            limit: TOOL_OUTPUT_BYTES,
        })
    );
    assert_eq!(output.total(), TOOL_OUTPUT_BYTES);
}

// ------------------------------------------------------------------ D3a-2: the tool class (item 12, :434)

fn tool_spec_for(exe: &Path, script: &str) -> ToolSpec {
    let argv: Vec<&OsStr> = vec![exe.as_os_str(), OsStr::new(SENTINEL), OsStr::new(script)];
    let launch = LaunchSpec::fixture(DescriptorSet::Tool, exe, &argv, ChildEnvironment::rust())
        .expect("a fixture spec");
    ToolSpec {
        launch: VerifiedLaunch::from_recheck(
            launch,
            ClosureRecheck {
                member: "supervisor-fixture".to_owned(),
                device: 0,
                inode: 0,
                sha256: "0".repeat(64),
            },
        ),
        needs_d3b_ladders: false,
        memory_budget_bytes: RESIDENT_MEMORY_CEILING,
    }
}

/// The tool's outcome: its settlement and what was observed.
struct ToolOutcome {
    settlement: Settlement,
    tree_calls: Vec<TreeCallAttempt>,
    events: Vec<SupervisionEvent>,
    facts: Vec<RecordFact>,
    scratch: Option<PathBuf>,
    process_id: Option<i32>,
}
impl ToolOutcome {
    fn saw(&self, event: &SupervisionEvent) -> bool {
        self.events.contains(event)
    }
    fn nothing_left(&self) {
        if let Some(pid) = self.process_id {
            assert_eq!(
                group_members_bounded(pid, 64).expect("the group"),
                Listing::Complete(Vec::new())
            );
        }
        if let Some(scratch) = &self.scratch {
            assert!(!scratch.exists(), "{} removed", scratch.display());
        }
    }
}

type ToolSetup = fn(&mut ToolSupervision);

/// A tool supervision over `script`, set up by `setup`, driven to its
/// settlement on its own thread under a hard limit.
fn tool_run(script: &'static str, setup: ToolSetup) -> ToolOutcome {
    tool_run_with(script, Box::new(setup))
}
/// `tool_run` with a capturing setup (D3b-1's tree hooks).
fn tool_run_with(
    script: &'static str,
    setup: Box<dyn FnOnce(&mut ToolSupervision) + Send>,
) -> ToolOutcome {
    tool_run_waits(script, Waits::TOOL, setup)
}
/// Tree controls exercise the wall deadline to initiate their native teardown.
fn tool_deadline_run(script: &'static str, setup: ToolSetup) -> ToolOutcome {
    tool_deadline_run_with(script, Box::new(setup))
}
/// Capturing variant; all host waits except the exercised wall clock stay release waits.
fn tool_deadline_run_with(
    script: &'static str,
    setup: Box<dyn FnOnce(&mut ToolSupervision) + Send>,
) -> ToolOutcome {
    let out = tool_run_waits(script, wall_clock_expiry_waits(), setup);
    assert!(
        out.saw(&SupervisionEvent::WaitExpired(BoundedWait::WallClock)),
        "this control exercises the deadline's ladder"
    );
    out
}
fn tool_run_waits(
    script: &'static str,
    waits: Waits,
    setup: Box<dyn FnOnce(&mut ToolSupervision) + Send>,
) -> ToolOutcome {
    let cap = control_cap(waits);
    let (done, finished) = mpsc::channel();
    std::thread::spawn(move || {
        let dir = test_dir();
        let mut supervision =
            Supervision::prepare_tool_with(tool_spec_for(&fixture(), script), waits)
                .expect("prepared");
        setup(&mut supervision);
        let (fact_sink, facts) = mpsc::channel();
        supervision.record_facts(Box::new(move |fact| {
            fact_sink.send(fact).ok();
        }));
        let (sink, events) = mpsc::channel();
        supervision.observer = Some(Box::new(move |event| {
            sink.send(event.clone()).ok();
        }));
        let mut root = root_in(&dir);
        let started = Instant::now();
        supervision.start(&mut root).expect("spawned");
        while supervision.state() != State::Settled {
            assert!(started.elapsed() < cap, "no settlement");
            supervision.turn();
        }
        let settlement = supervision.take_settlement().expect("one settlement");
        let calls = Rc::clone(&supervision.seams.tree_calls);
        let before = calls.borrow().clone();
        for _ in 0..3 {
            supervision.turn();
        }
        let scratch = supervision.seams.scratch.clone();
        drop(supervision);
        assert_eq!(
            *calls.borrow(),
            before,
            "no native tree call after settlement or in settled Drop"
        );
        let tree_calls = calls.borrow().clone();
        let events: Vec<SupervisionEvent> = events.try_iter().collect();
        let process_id = events.iter().find_map(|e| match e {
            SupervisionEvent::Spawned { process_id } => Some(*process_id),
            _ => None,
        });
        let facts: Vec<RecordFact> = facts.try_iter().collect();
        done.send(ToolOutcome {
            settlement,
            tree_calls,
            events,
            facts,
            scratch,
            process_id,
        })
        .ok();
    });
    finished
        .recv_timeout(cap)
        .unwrap_or_else(|_| panic!("{script}: no settlement within {cap:?}"))
}

/// Item 12, :434: a tool skips `Handshaking` (no control frame, no health),
/// reads fd0 at EOF at once (item 5, :274), and settles `clean` with its
/// fd1 bytes exactly as written, handed out once; its stderr is counted,
/// never kept (item 17); its scratch is removed.
#[test]
fn a_tool_skips_the_handshake_and_hands_its_output_once() {
    let mut out = tool_run("tool-ok", |_| {});
    assert_eq!(
        out.settlement.first_cause(),
        Cause::Clean,
        "{:?}",
        out.events
    );
    assert_eq!(out.settlement.exit(), ExitClass::Exited(0));
    assert!(out.saw(&SupervisionEvent::Running));
    assert!(
        !out.events.iter().any(|e| matches!(
            e,
            SupervisionEvent::ControlSent(_) | SupervisionEvent::ControlReceived(_)
        )),
        "no control plane"
    );
    assert!(!out.settlement.admissible(), "never a provider admission");
    assert_eq!(out.settlement.stderr().bytes, 16);
    assert_eq!(out.settlement.tree(), TreeReport::NotKilled);
    assert_eq!(out.settlement.scratch(), ScratchFate::Removed);
    let output = out.settlement.take_tool_output().expect("the output");
    assert_eq!(output, b"tool output\n".repeat(1_000));
    assert!(out.settlement.take_tool_output().is_none(), "once");
    assert_eq!(out.settlement.tool_output_bound(), None);
    out.nothing_left();
    let mut out = tool_run("tool-stdin", |_| {});
    assert_eq!(out.settlement.first_cause(), Cause::Clean);
    assert_eq!(
        out.settlement.take_tool_output().as_deref(),
        Some(&b"stdin at eof\n"[..])
    );
}

/// Item 22's tool row (:722): a tool's own failure (a nonzero exit) is
/// settled with its exit for MC item 12's adapter to route; its output is
/// not handed out.
#[test]
fn a_failed_tool_hands_its_exit_not_its_output() {
    let mut out = tool_run("tool-fail", |_| {});
    assert_eq!(out.settlement.first_cause(), Cause::Clean);
    assert_eq!(out.settlement.exit(), ExitClass::Exited(101));
    assert!(out.settlement.take_tool_output().is_none());
    out.nothing_left();
}

/// Item 16, :548 (D3-T15 for the tool bound): fd1 exactly at the bound
/// settles `clean` with every byte; one byte past it refuses
/// `ToolOutputBound`, keeps nothing past the bound, and is
/// `byte-bound(tool-output)` with the ladder from T-2 (no control plane).
#[test]
fn a_tools_output_is_bounded_exactly() {
    fn at_one_mib(s: &mut ToolSupervision) {
        let limit = 1 << 20;
        s.limits.tool_output = limit;
        if let Some(tool) = &mut s.tool {
            tool.accounting = ToolOutput::with_limit(limit);
        }
    }
    let mut out = tool_run("tool-bytes-1048576", at_one_mib);
    assert_eq!(out.settlement.first_cause(), Cause::Clean);
    assert_eq!(
        out.settlement.take_tool_output().map(|o| o.len()),
        Some(1 << 20)
    );
    let mut out = tool_run("tool-bytes-1048577", at_one_mib);
    assert_eq!(
        out.settlement.first_cause(),
        Cause::ByteBound(ByteBound::ToolOutput),
        "{:?}",
        out.events
    );
    let bound = out.settlement.tool_output_bound().expect("the refusal");
    assert_eq!(bound.limit, 1 << 20);
    assert!(bound.observed > 1 << 20);
    assert!(out.saw(&SupervisionEvent::LimitBreached(LimitKind::ToolOutput)));
    assert!(!out.saw(&SupervisionEvent::CancelAttempted), "no T-1");
    assert!(out.settlement.take_tool_output().is_none());
    out.nothing_left();
}

/// Item 16, :533: a tool's tree may hold 16 processes; a 17th is
/// `process-count`.
#[test]
fn a_tools_tree_holds_at_most_sixteen() {
    fn sampled(s: &mut ToolSupervision) {
        s.limits.memory_sample_interval = Duration::from_millis(20);
    }
    let out = tool_run("tool-fork-15", sampled);
    assert_eq!(
        out.settlement.first_cause(),
        Cause::Clean,
        "{:?}",
        out.events
    );
    let out = tool_run("tool-fork-16", sampled);
    assert_eq!(
        out.settlement.first_cause(),
        Cause::ProcessCount,
        "{:?}",
        out.events
    );
    out.nothing_left();
}

/// Item 14, :490: the tool's wall clock is its own, and its expiry is
/// `deadline` with the ladder from T-2 (SIGTERM, then SIGKILL); a root that
/// exits while a member holds fd1 past the drain is `unexpected-exit`
/// (LD-D3A2-2).
/// Only the wall-clock deadline is shortened for the tool-hang case.
#[test]
fn a_tools_wall_clock_and_held_output_end_it() {
    let out = tool_deadline_run("tool-hang", |_| {});
    assert_eq!(out.settlement.first_cause(), Cause::Deadline);
    assert!(out.saw(&SupervisionEvent::WaitExpired(BoundedWait::WallClock)));
    assert!(!out.saw(&SupervisionEvent::CancelAttempted), "no T-1");
    assert!(out.saw(&SupervisionEvent::Signalled { signal: SIGTERM }));
    out.nothing_left();
    let out = tool_run("tool-held", |_| {});
    assert_eq!(
        out.settlement.first_cause(),
        Cause::UnexpectedExit,
        "{:?}",
        out.events
    );
    out.nothing_left();
    let supervision =
        Supervision::prepare_tool(tool_spec_for(Path::new("/nonexistent"), "tool-ok"))
            .expect("prepared");
    assert_eq!(supervision.waits, Waits::TOOL);
    assert_eq!(supervision.protocol_waits(), None);
}

/// Item 5, :274: each class takes only its own descriptor set.
#[test]
fn each_class_takes_its_own_descriptor_set() {
    let mut provider = spec_for(Path::new("/nonexistent"), "normal");
    provider.launch = tool_spec_for(Path::new("/nonexistent"), "tool-ok").launch;
    assert!(matches!(
        Supervision::prepare(provider, FixtureParticipant::new(FIXTURE_WAITS)),
        Err(SupervisorError::DescriptorsMismatch)
    ));
    let mut tool = tool_spec_for(Path::new("/nonexistent"), "tool-ok");
    tool.launch = spec_for(Path::new("/nonexistent"), "normal").launch;
    assert!(matches!(
        Supervision::prepare_tool(tool),
        Err(SupervisorError::DescriptorsMismatch)
    ));
}

/// D3-T3 for a tool: `Drop` while it runs kills its group once, reaps it,
/// removes its scratch, and mints `abandoned`, confirming the group against
/// the unreaped root first.
#[test]
fn dropping_a_running_tool_leaves_nothing() {
    let dir = test_dir();
    let mut supervision =
        Supervision::prepare_tool_with(tool_spec_for(&fixture(), "tool-hang"), Waits::TOOL)
            .expect("prepared");
    let (sink, unwound) = mpsc::channel();
    supervision.seams.unwound = Some(sink);
    let mut root = root_in(&dir);
    supervision.start(&mut root).expect("spawned");
    assert_eq!(supervision.state(), State::Running);
    supervision.turn();
    let scratch = supervision.seams.scratch.clone().expect("a scratch");
    drop(supervision);
    let settlement = unwound
        .recv_timeout(Duration::from_secs(1))
        .expect("the unwind's settlement");
    assert_eq!(settlement.first_cause(), Cause::Abandoned);
    assert_eq!(settlement.tree(), TreeReport::GroupKilledPlatformLimited);
    assert_eq!(settlement.exit(), ExitClass::Signaled(9));
    assert!(!scratch.exists());
}

// ------------------------------------------------------------------ D3a-3: items 20 to 22

use super::records::{OwnerRoute, RecordFact};

/// Item 20's gate: a clean, admissible settlement releases its terminal
/// output once, with the spooled candidates; nothing is discarded.
#[test]
fn an_admissible_settlement_releases_its_output_once() {
    let mut out = outcome("normal");
    assert!(out.settlement.admissible());
    let output = out.settlement.release().expect("released");
    assert_eq!(output.kind(), TerminalKind::Complete);
    assert_eq!(output.into_spool().len(), 1, "the one FactBatch");
    assert!(out.settlement.release().is_none(), "once");
    assert!(!out.discarded);
    assert_eq!(out.settlement.route(), OwnerRoute::Admission);
}

/// D3-T22: a fault after some `FactBatch` frames, at each kind (a protocol
/// fault, an early exit, the deadline), discards every candidate; the
/// admission owner receives nothing.
/// Only facts-then-hang shortens the wall deadline, exercising deadline-driven discard.
#[test]
fn a_fault_after_candidates_discards_every_one() {
    for script in ["facts-then-fault", "facts-then-exit", "facts-then-hang"] {
        let mut out = if script == "facts-then-hang" {
            let out = outcome_with_waits(script, wall_clock_expiry_waits());
            assert_eq!(out.settlement.first_cause(), Cause::Deadline);
            assert!(out.saw(&SupervisionEvent::WaitExpired(BoundedWait::WallClock)));
            out
        } else {
            outcome(script)
        };
        assert_ne!(out.settlement.first_cause(), Cause::Clean, "{script}");
        assert_eq!(out.spooled, 2, "{script}: candidates were spooled");
        assert!(out.discarded, "{script}");
        assert_eq!(out.spool_left, 0, "{script}");
        assert!(out.settlement.release().is_none(), "{script}");
        assert_eq!(
            out.settlement.route(),
            OwnerRoute::ProviderProtocol,
            "{script}"
        );
        nothing_left(&out);
    }
}

/// D3-T23: a clean `Complete` with a nonzero exit is discarded (DLV:1171):
/// its minted output is dropped by the gate.
#[test]
fn a_complete_terminal_with_a_nonzero_exit_is_discarded() {
    let mut out = outcome("nonzero");
    assert_eq!(out.settlement.terminal(), Some(TerminalKind::Complete));
    assert_eq!(out.settlement.exit(), ExitClass::Exited(3));
    assert!(!out.settlement.admissible());
    assert!(out.discarded);
    assert!(out.settlement.release().is_none());
}

/// D3-T24: an injected scratch-removal failure, and removal exhaustion,
/// leave the result unchanged: still clean, admissible and released, with
/// the scratch retained and recorded.
#[test]
fn a_scratch_removal_failure_never_changes_the_result() {
    let mut out = threaded("normal", |s| s.seams.removal_errno = Some(5), quick());
    assert_eq!(out.settlement.first_cause(), Cause::Clean);
    assert_eq!(
        out.settlement.scratch(),
        ScratchFate::Retained(ScratchRetained::IoFailure(5))
    );
    assert!(out.settlement.release().is_some());
    assert!(out.facts.contains(&RecordFact::ScratchRetained {
        reason: opensip_operability::ScratchRetainedReason::IoFailure,
        errno: Some(5),
    }));
    let mut out = threaded(
        "normal",
        |s| {
            s.seams.removal_limits = Some(WorkCost {
                objects: 1,
                edges: 1,
                bytes: 1,
            })
        },
        quick(),
    );
    assert_eq!(out.settlement.first_cause(), Cause::Clean);
    assert_eq!(
        out.settlement.scratch(),
        ScratchFate::Retained(ScratchRetained::WorkExhausted)
    );
    assert!(out.settlement.release().is_some());
    assert!(out.facts.contains(&RecordFact::ScratchRetained {
        reason: opensip_operability::ScratchRetainedReason::WorkExhausted,
        errno: None,
    }));
}

/// The bad-commitment gate (NBO-2): a terminal whose commitment does not
/// recompute mints no `TerminalOutput`; nothing is releasable.
#[test]
fn a_terminal_whose_commitment_fails_mints_nothing() {
    let dir = test_dir();
    let mut participant = FixtureParticipant::new(FIXTURE_WAITS);
    participant.bad_commitment = true;
    let (supervision, events) = prepared("normal", participant, None);
    let mut out = finish(supervision, events, &dir);
    assert_eq!(out.settlement.first_cause(), Cause::ProviderProtocol);
    assert!(!out.settlement.admissible());
    assert!(out.settlement.release().is_none());
    assert!(out.discarded);
}

/// LD-D3A3-1: a clean provider run's record facts, each naming a
/// registered event: spawned (Rust3), ready (with the transfer sub-span),
/// the stderr count, and the settlement.
#[test]
fn a_clean_run_records_its_facts() {
    let out = outcome("normal");
    let facts = &out.facts;
    assert!(facts.iter().any(|f| matches!(
        f,
        RecordFact::ProcessSpawned {
            protocol: opensip_operability::ProtocolMajor::RustSemantic3,
            raw_pid
        } if *raw_pid as i32 == out.process_id.expect("spawned")
    )));
    let ready = facts
        .iter()
        .find_map(|f| match f {
            RecordFact::ProcessReady { start, transfer } => Some((*start, *transfer)),
            _ => None,
        })
        .expect("ready");
    assert!(ready.0 > Duration::ZERO && ready.0 >= ready.1);
    assert_eq!(
        facts
            .iter()
            .filter(|f| matches!(f, RecordFact::ProcessReady { .. }))
            .count(),
        1
    );
    assert!(facts.contains(&RecordFact::StderrReduced {
        bytes: 0,
        truncated: false
    }));
    assert_eq!(
        facts.last(),
        Some(&RecordFact::Settled {
            cause: opensip_operability::TeardownCause::Clean,
            admissible: true,
            user_interrupted: false,
        })
    );
    assert!(
        !facts
            .iter()
            .any(|f| matches!(f, RecordFact::ScratchRetained { .. }))
    );
}

/// Each bound, wait and fault fact carries its host-held values: the
/// observed value in its unit, the wait's configured bound, the cancel as
/// sent, the liveness provenance, and the asserted resources.
/// The deadline and expired-health rows shorten only their named expiry, respectively.
#[test]
fn each_fact_carries_its_values() {
    let out = bounded("fork", fixture_participant, |l| {
        l.memory_sample_interval = Duration::from_millis(20)
    });
    assert!(out.facts.contains(&RecordFact::LimitBreached {
        limit: opensip_operability::LimitKind::ProcessCount,
        observed: 2,
        unit: opensip_operability::LimitUnit::Processes,
    }));
    assert!(out.facts.contains(&RecordFact::TeardownStarted {
        cause: opensip_operability::TeardownCause::ProcessCount
    }));
    let out = bounded("allocate", fixture_participant, low_ceiling);
    assert!(out.facts.iter().any(|f| matches!(
        f,
        RecordFact::LimitBreached {
            limit: opensip_operability::LimitKind::ResidentMemory,
            observed,
            unit: opensip_operability::LimitUnit::Bytes,
        } if *observed > 48 << 20
    )));
    let out = outcome_with_waits("hang", wall_clock_expiry_waits());
    assert!(out.facts.contains(&RecordFact::WaitExpired {
        wait: opensip_operability::BoundedWait::WallClock,
        limit: wall_clock_expiry_waits().wall_clock,
    }));
    assert!(out.facts.contains(&RecordFact::CancelSent {
        control_reason: opensip_operability::ControlCancelReason::Deadline,
    }));
    let out = outcome("bad-nonce");
    assert!(out.facts.contains(&RecordFact::LivenessMissed {
        window: quick().liveness_window,
        miss: opensip_operability::LivenessMiss::NonceMismatch,
        refusal_family: Some(opensip_operability::RefusalFamily::Rf7),
    }));
    let out = outcome_with_waits("blocked", liveness_expiry_waits());
    assert!(out.facts.contains(&RecordFact::LivenessMissed {
        window: liveness_expiry_waits().liveness_window,
        miss: opensip_operability::LivenessMiss::WindowExpired,
        refusal_family: None,
    }));
    let out = outcome("assert-large");
    assert!(out.facts.contains(&RecordFact::ResourcesReported {
        resident: 9_663_676_416,
        cpu_nanos: 0,
        handles: 0,
    }));
    assert!(
        !out.saw(&SupervisionEvent::Progress(Progress::FactBatch)),
        "asserted, never progress"
    );
}

/// D3A2-R1-NBO-1: a member's failed sample (not `ESRCH`), and a failed
/// listing, are each disclosed once as incomplete, never as a complete sum;
/// a member that exited (`ESRCH`) is lawful and records nothing.
/// Only the wall deadline is shortened, to settle each nonfatal sample-disclosure scenario.
#[test]
fn an_incomplete_sample_is_disclosed_once() {
    let out = threaded(
        "hang",
        |s| {
            s.seams.sample_errno = Some(1);
            s.limits.memory_sample_interval = Duration::from_millis(20);
        },
        wall_clock_expiry_waits(),
    );
    let incomplete: Vec<_> = out
        .facts
        .iter()
        .filter(|f| matches!(f, RecordFact::SampleIncomplete { .. }))
        .collect();
    assert_eq!(
        incomplete,
        [&RecordFact::SampleIncomplete {
            listed: 1,
            unsampled: 1,
            listing_failed: false
        }]
    );
    let out = threaded(
        "hang",
        |s| {
            s.seams.listing_fails = true;
            s.limits.memory_sample_interval = Duration::from_millis(20);
        },
        wall_clock_expiry_waits(),
    );
    assert_eq!(
        out.facts
            .iter()
            .filter(|f| matches!(f, RecordFact::SampleIncomplete { .. }))
            .collect::<Vec<_>>(),
        [&RecordFact::SampleIncomplete {
            listed: 0,
            unsampled: 0,
            listing_failed: true
        }]
    );
    let out = threaded(
        "hang",
        |s| {
            s.seams.sample_errno = Some(ESRCH);
            s.limits.memory_sample_interval = Duration::from_millis(20);
        },
        wall_clock_expiry_waits(),
    );
    assert!(out.saw(&SupervisionEvent::WaitExpired(BoundedWait::WallClock)));
    assert!(
        !out.facts
            .iter()
            .any(|f| matches!(f, RecordFact::SampleIncomplete { .. }))
    );
}

/// S-OP-2 C-4 with D3's fixture (item 21's "never recorded"): a canary in
/// the child's stderr and in a control `fault` detail reaches no fact, no
/// event and no settlement, nor does its SHA-256; the fault is reduced to
/// its length.
#[test]
fn a_canary_reaches_no_record() {
    const CANARY: &str = "OPENSIP-CANARY-q7Zx3mK9vB2nW5";
    let out = outcome("canary");
    assert!(out.facts.contains(&RecordFact::FaultReduced {
        source: opensip_operability::FaultSource::ControlFault,
        refusal_family: None,
        detail_bytes: CANARY.len() as u64,
    }));
    assert!(out.settlement.stderr().bytes >= CANARY.len() as u64);
    let digest = digest_hex(&raw_sha256(CANARY.as_bytes()));
    let seen = format!("{:?}{:?}{:?}", out.facts, out.events, out.settlement);
    for needle in [CANARY, "q7Zx3mK9vB2nW5", digest.as_str()] {
        assert!(!seen.contains(needle), "{needle} reached a record");
    }
}

/// A tool's facts: spawned and reaped (Project-only events), and the
/// settlement; no provider stderr record (item 21, :692).
#[test]
fn a_tool_records_its_spawn_and_reap() {
    let out = tool_run("tool-ok", |_| {});
    let pid = out.process_id.expect("spawned") as u32;
    assert_eq!(
        out.facts.first(),
        Some(&RecordFact::ToolSpawned { raw_pid: pid })
    );
    assert!(out.facts.iter().any(|f| matches!(
        f,
        RecordFact::ToolReaped {
            raw_pid,
            exit: opensip_operability::ExitClass::Exited,
            ..
        } if *raw_pid == pid
    )));
    assert!(
        !out.facts
            .iter()
            .any(|f| matches!(f, RecordFact::StderrReduced { .. }))
    );
    assert_eq!(out.settlement.route(), OwnerRoute::Tool);
}

/// S-OP-2 C-2's `protocol-enum` check, held here beside the generated
/// contracts: each registry table's members equal its pinned enum's.
#[test]
fn protocol_enum_tables_equal_their_schemas() {
    use opensip_contracts::generated::protocol::{
        Control3RootVariant7Property0Reason as Reason, Rust3ProviderFaultV2Field3Value as Kind,
    };
    use opensip_operability::CodeEnum;
    let families: Vec<&str> = [
        RefusalFamily::Rf1,
        RefusalFamily::Rf2,
        RefusalFamily::Rf3,
        RefusalFamily::Rf4,
        RefusalFamily::Rf5,
        RefusalFamily::Rf6,
        RefusalFamily::Rf7,
        RefusalFamily::Rf8,
    ]
    .iter()
    .map(|f| f.as_str())
    .collect();
    assert_eq!(
        opensip_operability::RefusalFamily::TEXT,
        families.as_slice()
    );
    // Each list is exhaustive: a new generated member fails to compile here.
    let reasons = [Reason::User, Reason::Deadline, Reason::SupervisorFault];
    for reason in reasons {
        match reason {
            Reason::User | Reason::Deadline | Reason::SupervisorFault => {}
        }
    }
    let texts: Vec<String> = reasons.iter().map(|r| r.to_string()).collect();
    assert_eq!(
        opensip_operability::ControlCancelReason::TEXT,
        texts.as_slice()
    );
    // The generated faultKind has exactly these three members, and their
    // spellings are the pinned carrier schema's (RPP:445): each `faultKind`
    // field's `enum` in `native-carriers-v1.json`.
    for kind in [
        Kind::CompilerCrash,
        Kind::InputRejected,
        Kind::InternalInvariant,
    ] {
        match kind {
            Kind::CompilerCrash | Kind::InputRejected | Kind::InternalInvariant => {}
        }
    }
    let schema = std::fs::read_to_string(
        Path::new(env!("CARGO_MANIFEST_DIR")).join("../../schemas/wire/native-carriers-v1.json"),
    )
    .expect("the pinned carriers");
    let mut texts: Vec<String> = Vec::new();
    for tail in schema.split("\"name\": \"faultKind\"").skip(1) {
        let list = tail
            .split_once("\"enum\": [")
            .and_then(|(_, rest)| rest.split_once(']'))
            .map(|(list, _)| list)
            .expect("a faultKind enum");
        for member in list.split(',') {
            let member = member.trim().trim_matches('"').to_owned();
            if !texts.contains(&member) {
                texts.push(member);
            }
        }
    }
    assert_eq!(opensip_operability::RustFaultKind::TEXT, texts.as_slice());
}

/// LD-D3A3-1's completeness: each fact names a registered event and
/// supplies exactly that event's fields but the minted ones (`role`,
/// `universe`, `pid`).
#[test]
fn each_fact_supplies_its_event_s_unminted_fields() {
    use opensip_operability as op;
    use opensip_operability::Event;
    let d = Duration::ZERO;
    let facts = [
        RecordFact::ProcessSpawned {
            protocol: op::ProtocolMajor::RustSemantic3,
            raw_pid: 1,
        },
        RecordFact::ProcessReady {
            start: d,
            transfer: d,
        },
        RecordFact::StderrReduced {
            bytes: 0,
            truncated: false,
        },
        RecordFact::FaultReduced {
            source: op::FaultSource::ControlFault,
            refusal_family: None,
            detail_bytes: 0,
        },
        RecordFact::ResourcesReported {
            resident: 0,
            cpu_nanos: 0,
            handles: 0,
        },
        RecordFact::LivenessMissed {
            window: d,
            miss: op::LivenessMiss::WindowExpired,
            refusal_family: None,
        },
        RecordFact::LimitBreached {
            limit: op::LimitKind::Scratch,
            observed: 0,
            unit: op::LimitUnit::Bytes,
        },
        RecordFact::SampleIncomplete {
            listed: 0,
            unsampled: 0,
            listing_failed: true,
        },
        RecordFact::CancelSent {
            control_reason: op::ControlCancelReason::Deadline,
        },
        RecordFact::WaitExpired {
            wait: op::BoundedWait::Drain,
            limit: d,
        },
        RecordFact::TeardownStarted {
            cause: op::TeardownCause::Deadline,
        },
        RecordFact::ScratchRetained {
            reason: op::ScratchRetainedReason::WorkExhausted,
            errno: None,
        },
        RecordFact::Settled {
            cause: op::TeardownCause::Clean,
            admissible: true,
            user_interrupted: false,
        },
        RecordFact::ToolSpawned { raw_pid: 1 },
        RecordFact::ToolReaped {
            raw_pid: 1,
            exit: op::ExitClass::Exited,
            signal: None,
            max_rss_bytes: 0,
            cpu: d,
        },
        RecordFact::ToolLimitBreached {
            limit: op::LimitKind::ToolOutput,
            observed: 0,
            unit: op::LimitUnit::Bytes,
        },
        RecordFact::ToolSampleIncomplete {
            listed: 0,
            unsampled: 0,
            listing_failed: true,
        },
        RecordFact::ToolWaitExpired {
            wait: op::BoundedWait::WallClock,
            limit: d,
        },
        RecordFact::ToolTeardownStarted {
            cause: op::TeardownCause::Deadline,
        },
        RecordFact::ToolScratchRetained {
            reason: op::ScratchRetainedReason::IoFailure,
            errno: Some(5),
        },
        RecordFact::ToolSettled {
            cause: op::TeardownCause::Clean,
            user_interrupted: false,
        },
        RecordFact::StageChanged {
            stage: op::StageKind::SemanticProvider,
            state: op::ProviderState::Analyzing,
        },
        RecordFact::StageTerminal {
            stage: op::StageKind::SemanticProvider,
            terminal: op::StageTerminal::Complete,
            reason: None,
            fact_frames: 0,
            coverage_frames: 0,
            analysis: d,
        },
        RecordFact::ProcessReaped {
            raw_pid: 1,
            exit: op::ExitClass::Exited,
            signal: None,
            max_rss_bytes: 0,
            cpu: d,
            teardown: d,
        },
        RecordFact::ProgressAbsent {
            stage: op::StageKind::SemanticProvider,
            since: d,
        },
        RecordFact::TreeSwept {
            killed: 0,
            unattributed: 0,
            platform_limited: true,
        },
        RecordFact::ToolTreeSwept {
            killed: 0,
            unattributed: 0,
            platform_limited: true,
        },
    ];
    fn keys<E: Event>() -> (&'static str, &'static [&'static str]) {
        (E::NAME, E::FIELD_KEYS)
    }
    let registered = [
        keys::<op::ProviderProcessSpawned>(),
        keys::<op::ProviderProcessReady>(),
        keys::<op::ProviderStderrReduced>(),
        keys::<op::ProviderFaultReduced>(),
        keys::<op::ProviderResourcesReported>(),
        keys::<op::SupervisionLivenessMissed>(),
        keys::<op::SupervisionLimitBreached>(),
        keys::<op::SupervisionSampleIncomplete>(),
        keys::<op::SupervisionCancelSent>(),
        keys::<op::SupervisionWaitExpired>(),
        keys::<op::SupervisionTeardownStarted>(),
        keys::<op::SupervisionScratchRetained>(),
        keys::<op::SupervisionSettled>(),
        keys::<op::ToolProcessSpawned>(),
        keys::<op::ToolProcessReaped>(),
        keys::<op::ToolLimitBreached>(),
        keys::<op::ToolSampleIncomplete>(),
        keys::<op::ToolWaitExpired>(),
        keys::<op::ToolTeardownStarted>(),
        keys::<op::ToolScratchRetained>(),
        keys::<op::ToolChildSettled>(),
        keys::<op::ProviderStageChanged>(),
        keys::<op::ProviderStageTerminal>(),
        keys::<op::ProviderProcessReaped>(),
        keys::<op::SupervisionProgressAbsent>(),
        keys::<op::SupervisionTreeSwept>(),
        keys::<op::ToolTreeSwept>(),
    ];
    assert_eq!(facts.len(), registered.len());
    for (fact, (name, fields)) in facts.iter().zip(registered) {
        assert_eq!(fact.event(), name);
        let mut supplied: Vec<&str> = fact.supplies().to_vec();
        supplied.extend(
            fields
                .iter()
                .copied()
                .filter(|k| ["role", "universe", "pid"].contains(k)),
        );
        supplied.sort_unstable();
        let mut wanted = fields.to_vec();
        wanted.sort_unstable();
        assert_eq!(supplied, wanted, "{name}");
    }
}

/// LD-D3A-11: every cause has exactly one route; a host-observed cause
/// never takes the provider-protocol route (item 22, :731);
/// `userInterrupted` takes the interrupted row first; the pre-spawn and
/// spawn refusals take theirs.
#[test]
fn every_cause_has_its_one_route() {
    let all = [
        Cause::Clean,
        Cause::ClosureRecheckFailed,
        Cause::SessionSpecInconsistent,
        Cause::SpawnFailed,
        Cause::HandshakeDeadline,
        Cause::ControlRefusal(RefusalFamily::Rf2),
        Cause::ProviderProtocol,
        Cause::UnexpectedExit,
        Cause::Deadline,
        Cause::Liveness,
        Cause::MemoryCeiling,
        Cause::ProcessCount,
        Cause::ByteBound(ByteBound::Response),
        Cause::ByteBound(ByteBound::ToolOutput),
        Cause::ScratchBound,
        Cause::UserCancel,
        Cause::Revoked,
        Cause::ObserverFailStop,
        Cause::HostFault,
        Cause::Abandoned,
    ];
    let host_observed = [
        Cause::ClosureRecheckFailed,
        Cause::SessionSpecInconsistent,
        Cause::SpawnFailed,
        Cause::HostFault,
        Cause::Abandoned,
        Cause::Revoked,
        Cause::ObserverFailStop,
        Cause::UserCancel,
    ];
    for cause in all {
        let route = records::cause_route(cause);
        assert_eq!(route, records::cause_route(cause), "deterministic");
        if host_observed.contains(&cause) {
            assert_ne!(route, OwnerRoute::ProviderProtocol, "{cause:?}");
        }
    }
    assert_eq!(records::cause_route(Cause::Clean), OwnerRoute::Admission);
    assert_eq!(records::cause_route(Cause::HostFault), OwnerRoute::HostIo);
    assert_eq!(
        records::cause_route(Cause::Liveness),
        OwnerRoute::ProviderProtocol
    );
    // userInterrupted takes the interrupted row first.
    let mut out = outcome("fault");
    out.settlement.user_interrupted = true;
    assert_eq!(out.settlement.route(), OwnerRoute::Interrupted);
    assert_eq!(
        records::run_error_route(&RunError::Declined(PreSpawnRefusal::ClosureRecheckFailed)),
        OwnerRoute::ClosureBytesCorrupt
    );
    assert_eq!(
        records::run_error_route(&RunError::Declined(
            PreSpawnRefusal::SessionSpecInconsistent
        )),
        OwnerRoute::HostInvariant
    );
    assert_eq!(
        records::supervisor_error_route(SupervisorError::MemoryBudgetBelowCeiling {
            budget: 0,
            ceiling: RESIDENT_MEMORY_CEILING
        }),
        OwnerRoute::MemoryBudgetBelowCeiling
    );
    let dir = test_dir();
    let missing = dir.0.join("no-such-fixture");
    let mut supervision = Supervision::prepare_with(
        spec_for(&missing, "normal"),
        FixtureParticipant::new(FIXTURE_WAITS),
        quick(),
    )
    .expect("prepared");
    let error = supervision
        .run(&mut root_in(&dir))
        .expect_err("unspawnable");
    assert_eq!(
        records::run_error_route(&error),
        OwnerRoute::ClosureUnspawnable
    );
}

/// Item 20 (NBO-2): admission requires the terminal's output; a settlement
/// that is clean, terminal, zero-exit and at EOF, but holds no
/// `TerminalOutput`, is not admissible and releases nothing.
#[test]
fn admission_requires_the_terminal_output() {
    let settlement = |output: Option<TerminalOutput>| Settlement {
        first_cause: Cause::Clean,
        later_causes: Vec::new(),
        user_interrupted: false,
        exit: ExitClass::Exited(0),
        tree: TreeReport::NotKilled,
        tree_evidence: None,
        stderr: StderrCount::default(),
        rusage: None,
        scratch: ScratchFate::Removed,
        terminal: Some(TerminalKind::Complete),
        eof_observed: true,
        output,
        tool: None,
    };
    let mut without = settlement(None);
    assert!(!without.admissible());
    assert!(without.release().is_none());
    let mut with = settlement(Some(TerminalOutput::mint(
        TerminalKind::Complete,
        Spool::default(),
    )));
    assert!(with.admissible());
    assert!(with.release().is_some());
}

// ------------------------------------------------------------------ D3a-3 r2 (Codex codex-d3a-3-r1)

/// The identities each registered event requires, by name.
fn registry_requires(name: &str) -> opensip_operability::IdentitySet {
    use opensip_operability as op;
    use opensip_operability::Event;
    fn of<E: Event>() -> (&'static str, op::IdentitySet) {
        (E::NAME, E::REQUIRES)
    }
    [
        of::<op::ProviderProcessSpawned>(),
        of::<op::ProviderProcessReady>(),
        of::<op::ProviderStderrReduced>(),
        of::<op::ProviderFaultReduced>(),
        of::<op::ProviderResourcesReported>(),
        of::<op::SupervisionLivenessMissed>(),
        of::<op::SupervisionLimitBreached>(),
        of::<op::SupervisionSampleIncomplete>(),
        of::<op::SupervisionCancelSent>(),
        of::<op::SupervisionWaitExpired>(),
        of::<op::SupervisionTeardownStarted>(),
        of::<op::SupervisionScratchRetained>(),
        of::<op::SupervisionSettled>(),
        of::<op::ToolProcessSpawned>(),
        of::<op::ToolProcessReaped>(),
        of::<op::ToolLimitBreached>(),
        of::<op::ToolSampleIncomplete>(),
        of::<op::ToolWaitExpired>(),
        of::<op::ToolTeardownStarted>(),
        of::<op::ToolScratchRetained>(),
        of::<op::ToolChildSettled>(),
        of::<op::ProviderStageChanged>(),
        of::<op::ProviderStageTerminal>(),
        of::<op::ProviderProcessReaped>(),
        of::<op::SupervisionProgressAbsent>(),
        of::<op::SupervisionTreeSwept>(),
        of::<op::ToolTreeSwept>(),
    ]
    .into_iter()
    .find(|(n, _)| *n == name)
    .map(|(_, requires)| requires)
    .unwrap_or_else(|| panic!("{name} is not registered"))
}

/// Codex D3A3-R1-RF-1: a tool has only a Project. Its normal, timed-out,
/// output-bound, sample-failing and scratch-retaining runs each produce
/// only facts whose registered events require exactly a Project; none
/// needs a Plan, an Execution, a provider role or a universe. A provider's
/// facts each require Project, Plan and Execution.
/// Only the timed-out rows shorten the wall deadline; their WaitExpired facts are part of this control.
#[test]
fn every_fact_matches_the_identities_its_class_has() {
    use opensip_operability::IdentitySet;
    fn at_one_mib(s: &mut ToolSupervision) {
        let limit = 1 << 20;
        s.limits.tool_output = limit;
        if let Some(tool) = &mut s.tool {
            tool.accounting = ToolOutput::with_limit(limit);
        }
    }
    fn sample_fails(s: &mut ToolSupervision) {
        s.seams.sample_errno = Some(1);
        s.limits.memory_sample_interval = Duration::from_millis(20);
    }
    fn removal_fails(s: &mut ToolSupervision) {
        s.seams.removal_errno = Some(5);
    }
    let runs: [(&'static str, ToolSetup); 5] = [
        ("tool-ok", |_| {}),
        ("tool-hang", |_| {}),
        ("tool-bytes-1048577", at_one_mib),
        ("tool-hang", sample_fails),
        ("tool-ok", removal_fails),
    ];
    let mut seen = std::collections::BTreeSet::new();
    for (script, setup) in runs {
        let out = if script == "tool-hang" {
            tool_deadline_run(script, setup)
        } else {
            tool_run(script, setup)
        };
        assert!(!out.facts.is_empty(), "{script}");
        for fact in &out.facts {
            assert_eq!(
                fact.requires(),
                records::Requires::Project,
                "{script}: {fact:?}"
            );
            assert_eq!(
                registry_requires(fact.event()),
                IdentitySet::Project,
                "{script}: {fact:?}"
            );
            seen.insert(fact.event());
        }
    }
    for event in [
        "tool.process.spawned",
        "tool.process.reaped",
        "tool.child.settled",
        "tool.wait.expired",
        "tool.teardown.started",
        "tool.limit.breached",
        "tool.sample.incomplete",
        "tool.scratch.retained",
    ] {
        assert!(seen.contains(event), "{event} never produced");
    }
    for script in ["normal", "hang", "fault"] {
        let out = if script == "hang" {
            let out = outcome_with_waits(script, wall_clock_expiry_waits());
            assert!(out.saw(&SupervisionEvent::WaitExpired(BoundedWait::WallClock)));
            out
        } else {
            outcome(script)
        };
        for fact in &out.facts {
            assert_eq!(
                fact.requires(),
                records::Requires::ProjectPlanExecution,
                "{script}"
            );
            assert_eq!(
                registry_requires(fact.event()),
                IdentitySet::ProjectPlanExecution,
                "{script}: {fact:?}"
            );
        }
    }
}

/// Codex D3A3-R1-RF-2: T-1's cancel is recorded only once its frame is
/// written whole: not while queued, not after a partial write, exactly once
/// on completion.
/// Only the wall-clock deadline is shortened to exercise deadline-triggered cancel writes.
#[test]
fn a_cancel_is_recorded_only_once_written() {
    let dir = test_dir();
    let (mut supervision, events) = prepared("hang", FixtureParticipant::new(FIXTURE_WAITS), None);
    supervision.waits = wall_clock_expiry_waits();
    let facts = Rc::clone(&supervision.seams.facts);
    let cancels = |facts: &Rc<RefCell<Vec<RecordFact>>>| {
        facts
            .borrow()
            .iter()
            .filter(|f| matches!(f, RecordFact::CancelSent { .. }))
            .count()
    };
    let mut root = root_in(&dir);
    let started = Instant::now();
    supervision.start(&mut root).expect("spawned");
    // Until the deadline queues T-1's cancel.
    while !events
        .borrow()
        .iter()
        .any(|(_, e)| *e == SupervisionEvent::ControlSent("cancel"))
    {
        assert!(
            started.elapsed() < control_cap(supervision.waits),
            "no cancel queued"
        );
        supervision.turn();
    }
    assert_eq!(cancels(&facts), 0, "queued, not written");
    // Three bytes of it, then no more.
    supervision.seams.control_bytes_left = Some(3);
    for _ in 0..5 {
        supervision.turn();
    }
    assert!(
        supervision.control_out.at > 0
            && supervision.control_out.at < supervision.control_out.bytes.len()
    );
    assert_eq!(cancels(&facts), 0, "partly written");
    supervision.seams.control_bytes_left = None;
    while supervision.state() != State::Settled {
        assert!(
            started.elapsed() < control_cap(supervision.waits),
            "no settlement"
        );
        supervision.turn();
    }
    assert_eq!(cancels(&facts), 1, "written whole, recorded once");
}

/// Codex D3A3-R1-RF-2: a queued cancel whose write fails (the child's
/// control reader gone, `EPIPE`) is never recorded as sent; and a child
/// whose control reader closes early records no cancel either.
/// Only the wall-clock deadline is shortened to exercise deadline-triggered cancel writes.
#[test]
fn a_cancel_whose_write_fails_is_not_recorded() {
    let dir = test_dir();
    let (mut supervision, events) = prepared("hang", FixtureParticipant::new(FIXTURE_WAITS), None);
    supervision.waits = wall_clock_expiry_waits();
    let facts = Rc::clone(&supervision.seams.facts);
    let mut root = root_in(&dir);
    let started = Instant::now();
    supervision.start(&mut root).expect("spawned");
    while !events
        .borrow()
        .iter()
        .any(|(_, e)| *e == SupervisionEvent::ControlSent("cancel"))
    {
        assert!(
            started.elapsed() < control_cap(supervision.waits),
            "no cancel queued"
        );
        supervision.turn();
    }
    supervision.seams.control_write_fails = true;
    while supervision.state() != State::Settled {
        assert!(
            started.elapsed() < control_cap(supervision.waits),
            "no settlement"
        );
        supervision.turn();
    }
    assert!(supervision.ends.fd3.is_none(), "the write failed");
    assert!(
        !facts
            .borrow()
            .iter()
            .any(|f| matches!(f, RecordFact::CancelSent { .. })),
        "{:?}",
        facts.borrow()
    );
    let out = outcome("close-control");
    assert_ne!(out.settlement.first_cause(), Cause::Clean);
    assert!(
        !out.facts
            .iter()
            .any(|f| matches!(f, RecordFact::CancelSent { .. }))
    );
}

// ------------------------------------------------------------------ D3a-4: the four unblocked events (S-OP-2c)

/// `provider.stage.changed`, `.stage.terminal` and `.process.reaped` on a
/// clean run: each phase change once (never a repeat), the terminal
/// `complete` with no reason and the admitted frame counts, and the reap
/// with no signal and M3-L's spans.
#[test]
fn a_clean_run_records_its_stages_terminal_and_reap() {
    use opensip_operability as op;
    let out = outcome("normal");
    let states: Vec<op::ProviderState> = out
        .facts
        .iter()
        .filter_map(|f| match f {
            RecordFact::StageChanged { state, .. } => Some(*state),
            _ => None,
        })
        .collect();
    assert!(states.windows(2).all(|w| w[0] != w[1]), "{states:?}");
    for state in [
        op::ProviderState::ReadyAnalyze,
        op::ProviderState::Analyzing,
        op::ProviderState::Done,
    ] {
        assert!(states.contains(&state), "{state:?} in {states:?}");
    }
    let terminals: Vec<&RecordFact> = out
        .facts
        .iter()
        .filter(|f| matches!(f, RecordFact::StageTerminal { .. }))
        .collect();
    assert_eq!(terminals.len(), 1, "{terminals:?}");
    assert!(
        matches!(
            terminals[0],
            RecordFact::StageTerminal {
                terminal: op::StageTerminal::Complete,
                reason: None,
                fact_frames: 1,
                coverage_frames: 1,
                analysis,
                ..
            } if *analysis > Duration::ZERO
        ),
        "{terminals:?}"
    );
    let pid = out.process_id.expect("spawned") as u32;
    assert!(
        out.facts.iter().any(|f| matches!(
            f,
            RecordFact::ProcessReaped {
                raw_pid,
                exit: op::ExitClass::Exited,
                signal: None,
                teardown,
                ..
            } if *raw_pid == pid && *teardown > Duration::ZERO
        )),
        "{:?}",
        out.facts
    );
}

/// `provider.stage.terminal`'s `reason` is present exactly for
/// `unavailable` (S-OP-2c item 23a).
#[test]
fn an_unavailable_terminal_records_its_reason() {
    use opensip_operability as op;
    let out = outcome("unavailable");
    assert_eq!(out.settlement.terminal(), Some(TerminalKind::Unavailable));
    assert!(
        out.facts.contains(&RecordFact::StageTerminal {
            stage: op::StageKind::SemanticProvider,
            terminal: op::StageTerminal::Unavailable,
            reason: Some(op::ProviderReason::CapabilityMissing),
            fact_frames: 0,
            coverage_frames: 0,
            analysis: match out.facts.iter().find_map(|f| match f {
                RecordFact::StageTerminal { analysis, .. } => Some(*analysis),
                _ => None,
            }) {
                Some(analysis) => analysis,
                None => panic!("no terminal record"),
            },
        }),
        "{:?}",
        out.facts
    );
}

/// A child's signal death names its `ChildSignal` member through the
/// platform's `libc` constant; a provider that analyzed and was killed
/// before any terminal records `crash`; a provider that died before Analyze
/// with no terminal records no stage terminal, and no `crash` is
/// synthesized for it.
#[test]
fn signal_deaths_and_crashes_are_recorded() {
    use opensip_operability as op;
    let out = outcome("signal-death");
    assert!(
        out.facts.iter().any(|f| matches!(
            f,
            RecordFact::ProcessReaped {
                exit: op::ExitClass::Signaled,
                signal: Some(op::ChildSignal::Sigabrt),
                ..
            }
        )),
        "{:?}",
        out.facts
    );
    assert!(
        !out.facts
            .iter()
            .any(|f| matches!(f, RecordFact::StageTerminal { .. }))
    );
    let out = outcome_with_waits("facts-then-hang", wall_clock_expiry_waits());
    assert!(out.saw(&SupervisionEvent::WaitExpired(BoundedWait::WallClock)));
    assert!(
        out.facts.iter().any(|f| matches!(
            f,
            RecordFact::StageTerminal {
                terminal: op::StageTerminal::Crash,
                reason: None,
                fact_frames: 2,
                ..
            }
        )),
        "{:?}",
        out.facts
    );
    assert!(
        out.facts.iter().any(|f| matches!(
            f,
            RecordFact::ProcessReaped {
                exit: op::ExitClass::Signaled,
                signal: Some(op::ChildSignal::Sigterm | op::ChildSignal::Sigkill),
                ..
            }
        )),
        "{:?}",
        out.facts
    );
}

/// `supervision.progress.absent`'s `since` is measured from the last
/// admitted transition (SOP2:906), so successive reports without one grow:
/// the k-th is at least k intervals (r2, D3A4-R1-RF-1).
/// Only progress-absence reporting is shortened; handshake, health and teardown waits are release waits.
#[test]
fn progress_absence_records_its_measured_span() {
    let interval = progress_absence_waits().progress_absent_interval;
    let out = outcome_with_waits("slow-long", progress_absence_waits());
    let since: Vec<Duration> = out
        .facts
        .iter()
        .filter_map(|f| match f {
            RecordFact::ProgressAbsent { since, .. } => Some(*since),
            _ => None,
        })
        .collect();
    assert!(since.len() >= 2, "{since:?}");
    for (k, span) in (1u32..).zip(&since) {
        assert!(*span >= interval * k, "report {k}: {since:?}");
    }
    assert!(since.windows(2).all(|w| w[0] < w[1]), "{since:?}");
}

/// r2 (the self-review's disclosure item): every participant terminal maps
/// to the `StageTerminal` member of its own spelling, including the three
/// the fixture never reaches (`budget-exhausted`, `provider-fault`,
/// `cancelled`).
#[test]
fn every_terminal_kind_maps_to_its_stage_terminal() {
    use opensip_operability::{CodeEnum, StageTerminal};
    for text in [
        "complete",
        "unavailable",
        "budget-exhausted",
        "provider-fault",
        "cancelled",
    ] {
        let member = records::stage_terminal(terminal_of(text));
        assert_eq!(StageTerminal::TEXT[member as usize], text);
    }
}

/// A pinned schema source, parsed (`opensip_identity`'s JSON).
fn pinned_json(relative: &str) -> opensip_identity::JsonValue {
    let raw = std::fs::read(
        Path::new(env!("CARGO_MANIFEST_DIR"))
            .join("../..")
            .join(relative),
    )
    .unwrap_or_else(|e| panic!("{relative}: {e}"));
    opensip_identity::parse_json(&raw).unwrap_or_else(|e| panic!("{relative}: {e:?}"))
}

/// The value at `path` (object keys, or array indexes as decimal text).
fn json_at<'a>(
    value: &'a opensip_identity::JsonValue,
    path: &[&str],
) -> &'a opensip_identity::JsonValue {
    use opensip_identity::JsonValue;
    path.iter().fold(value, |at, key| match at {
        JsonValue::Object(map) => map.get(*key).unwrap_or_else(|| panic!("no {key}")),
        JsonValue::Array(items) => key
            .parse::<usize>()
            .ok()
            .and_then(|i| items.get(i))
            .unwrap_or_else(|| panic!("no {key}")),
        _ => panic!("{key}: not a container"),
    })
}

/// A schema `enum`'s strings in order, or a `const`'s one.
fn json_members(value: &opensip_identity::JsonValue) -> Vec<String> {
    use opensip_identity::JsonValue;
    let JsonValue::Object(map) = value else {
        panic!("not a schema: {value:?}");
    };
    let text = |v: &JsonValue| match v {
        JsonValue::String(s) => s.clone(),
        other => panic!("not a string member: {other:?}"),
    };
    match (map.get("enum"), map.get("const")) {
        (Some(JsonValue::Array(items)), None) => items.iter().map(text).collect(),
        (None, Some(one)) => vec![text(one)],
        _ => panic!("neither an enum nor a const: {value:?}"),
    }
}

/// r2 (D3A4-R1-RF-3): C-2's source equality for D3a-4's three other
/// protocol-enum tables (S-OP-2c item 23a; `ProviderState` is
/// `every_table_phase_is_a_provider_state`'s), member for member and in
/// order, against the pinned sources, never a handwritten list:
/// - `StageKind`: the `operator` of TS2 `Ts2StageRequestV1` and Rust3
///   `Rust3C2PlanStageV3` in the pinned carriers (LD-OPT-1);
/// - `ProviderReason`: the union of `PreAnalyzeUnavailableV1`,
///   `TypeScriptUnavailableV2` and `UnavailableV3`'s `reason`, in S-OP-2c's
///   selected (sorted) order (LD-OPT-5);
/// - `StageTerminal`: NE's `StageTerminal` (SOP2:880).
///
/// Each generated enum's spellings are its schema's too, and each list
/// below is exhaustive, so an added generated member fails to compile here.
#[test]
fn the_stage_tables_equal_their_sources() {
    use opensip_contracts::generated::evidence::Native2StageTerminal as Terminal;
    use opensip_contracts::generated::protocol::{
        Rust3C2PlanStageV3Field5Value as RustOperator,
        Startup1TypeScriptUnavailableV2Reason as Ts2, Startup1UnavailableV3Reason as Rust3,
        Ts2StageRequestV1Field2Value as Ts2Operator,
    };
    use opensip_operability::{CodeEnum, ProviderReason, StageKind, StageTerminal};
    // StageKind.
    let carriers = pinned_json("schemas/wire/native-carriers-v1.json");
    let mut operators: Vec<String> = Vec::new();
    for record in ["Ts2StageRequestV1", "Rust3C2PlanStageV3"] {
        let opensip_identity::JsonValue::Array(members) =
            json_at(&carriers, &["records", record, "members"])
        else {
            panic!("{record}: no members");
        };
        let operator = members
            .iter()
            .find(|m| {
                json_at(m, &["name"]) == &opensip_identity::JsonValue::String("operator".into())
            })
            .unwrap_or_else(|| panic!("{record}: no operator"));
        for member in json_members(json_at(operator, &["type"])) {
            if !operators.contains(&member) {
                operators.push(member);
            }
        }
    }
    assert_eq!(StageKind::TEXT, operators.as_slice());
    for operator in [Ts2Operator::SemanticProvider] {
        match operator {
            Ts2Operator::SemanticProvider => {}
        }
    }
    for operator in [RustOperator::SemanticProvider] {
        match operator {
            RustOperator::SemanticProvider => {}
        }
    }
    // ProviderReason.
    let startup = pinned_json("schemas/sources/startup-v1.schema.json");
    let reasons =
        |def: &str| json_members(json_at(&startup, &["$defs", def, "properties", "reason"]));
    let pre_analyze = reasons("PreAnalyzeUnavailableV1");
    let ts2 = reasons("TypeScriptUnavailableV2");
    let rust3 = reasons("UnavailableV3");
    assert_eq!(pre_analyze, ["native-context-mismatch"]);
    let ts2_generated = [
        Ts2::CapabilityMissing,
        Ts2::IdentityVersionMismatch,
        Ts2::NodeModulesOutsideReadSet,
        Ts2::SemanticUniverseIncomplete,
        Ts2::SnapshotResolutionInputMissing,
        Ts2::UnsupportedCompilerMode,
    ];
    for reason in &ts2_generated {
        match reason {
            Ts2::CapabilityMissing
            | Ts2::IdentityVersionMismatch
            | Ts2::NodeModulesOutsideReadSet
            | Ts2::SemanticUniverseIncomplete
            | Ts2::SnapshotResolutionInputMissing
            | Ts2::UnsupportedCompilerMode => {}
        }
    }
    let ts2_texts: Vec<String> = ts2_generated.iter().map(|r| r.to_string()).collect();
    assert_eq!(ts2_texts, ts2);
    let rust3_generated = [
        Rust3::CapabilityMissing,
        Rust3::DependencySourceIncomplete,
        Rust3::GeneratedCfgUnavailable,
        Rust3::IdentityVersionMismatch,
        Rust3::PreparedOutputNotInert,
        Rust3::PreparedOutputStale,
        Rust3::SemanticUniverseIncomplete,
        Rust3::SnapshotResolutionInputMissing,
        Rust3::UnsupportedCompilerMode,
    ];
    for reason in &rust3_generated {
        match reason {
            Rust3::CapabilityMissing
            | Rust3::DependencySourceIncomplete
            | Rust3::GeneratedCfgUnavailable
            | Rust3::IdentityVersionMismatch
            | Rust3::PreparedOutputNotInert
            | Rust3::PreparedOutputStale
            | Rust3::SemanticUniverseIncomplete
            | Rust3::SnapshotResolutionInputMissing
            | Rust3::UnsupportedCompilerMode => {}
        }
    }
    let rust3_texts: Vec<String> = rust3_generated.iter().map(|r| r.to_string()).collect();
    assert_eq!(rust3_texts, rust3);
    let mut union: Vec<String> = pre_analyze.into_iter().chain(ts2).chain(rust3).collect();
    union.sort();
    union.dedup();
    assert_eq!(ProviderReason::TEXT, union.as_slice());
    // StageTerminal.
    let native = pinned_json("schemas/sources/native-v2.schema.json");
    let terminals = json_members(json_at(&native, &["$defs", "StageTerminal"]));
    assert_eq!(StageTerminal::TEXT, terminals.as_slice());
    let generated = [
        Terminal::Complete,
        Terminal::Unavailable,
        Terminal::BudgetExhausted,
        Terminal::ProviderFault,
        Terminal::Cancelled,
        Terminal::Crash,
    ];
    for terminal in &generated {
        match terminal {
            Terminal::Complete
            | Terminal::Unavailable
            | Terminal::BudgetExhausted
            | Terminal::ProviderFault
            | Terminal::Cancelled
            | Terminal::Crash => {}
        }
    }
    let generated: Vec<String> = generated.iter().map(|t| t.to_string()).collect();
    assert_eq!(generated, terminals);
}

/// r2 (D3A4-R1-RF-1): the absence clock, on fixed instants. A report
/// paces the next one an interval later but never moves the transition;
/// only a real transition resets both the span and the schedule.
#[test]
fn the_absence_clock_measures_from_the_transition() {
    let interval = Duration::from_millis(200);
    let t0 = Instant::now();
    let at = |ms: u64| t0 + Duration::from_millis(ms);
    let ms = Duration::from_millis;
    let mut clock = AbsenceClock::default();
    assert_eq!(clock.due(interval), None);
    clock.progress(t0);
    assert_eq!(clock.due(interval), Some(at(200)));
    assert_eq!(clock.report(at(200)), Some(ms(200)));
    assert_eq!(clock.due(interval), Some(at(400)));
    assert_eq!(clock.report(at(410)), Some(ms(410)));
    assert_eq!(clock.due(interval), Some(at(610)));
    assert_eq!(clock.report(at(610)), Some(ms(610)));
    clock.progress(at(700));
    assert_eq!(clock.due(interval), Some(at(900)));
    assert_eq!(clock.report(at(900)), Some(ms(200)));
    assert_eq!(clock.due(interval), Some(at(1_100)));
}

/// D3a-4 r2 (D3A4-R1-NBO-1): an admitted `Unavailable` before Analyze is a
/// real terminal: it records `unavailable` with `PreAnalyzeUnavailableV1`'s
/// reason, no frames and a zero analysis span (no Analyze was sent), and no
/// `crash` is synthesized.
#[test]
fn a_pre_analyze_unavailable_records_its_terminal() {
    use opensip_operability as op;
    let out = outcome("unavailable-early");
    assert_eq!(out.settlement.terminal(), Some(TerminalKind::Unavailable));
    let terminals: Vec<&RecordFact> = out
        .facts
        .iter()
        .filter(|f| matches!(f, RecordFact::StageTerminal { .. }))
        .collect();
    assert_eq!(
        terminals,
        [&RecordFact::StageTerminal {
            stage: op::StageKind::SemanticProvider,
            terminal: op::StageTerminal::Unavailable,
            reason: Some(op::ProviderReason::NativeContextMismatch),
            fact_frames: 0,
            coverage_frames: 0,
            analysis: Duration::ZERO,
        }],
        "{:?}",
        out.facts
    );
}

/// The time of a supervision event, which the test sink stamps as it is
/// appended.
fn event_at(out: &Outcome, wanted: &SupervisionEvent) -> Instant {
    out.events
        .iter()
        .find(|(_, e)| e == wanted)
        .map(|(at, _)| *at)
        .unwrap_or_else(|| panic!("no {wanted:?} in {:?}", out.events))
}

fn reaped_teardown(out: &Outcome) -> Duration {
    out.facts
        .iter()
        .find_map(|f| match f {
            RecordFact::ProcessReaped { teardown, .. } => Some(*teardown),
            _ => None,
        })
        .unwrap_or_else(|| panic!("no reap record in {:?}", out.facts))
}

/// A run whose host fault arrives at its first `FactBatch`, once.
fn faulted_at_the_first_fact(script: &str) -> Outcome {
    let dir = test_dir();
    let mut fired = false;
    let hook: Hook = Box::new(move |event, handle| {
        if !fired && *event == SupervisionEvent::Progress(Progress::FactBatch) {
            fired = true;
            assert!(handle.host_fault());
        }
    });
    let (supervision, events) =
        prepared(script, FixtureParticipant::new(FIXTURE_WAITS), Some(hook));
    finish(supervision, events, &dir)
}

/// r2 (D3A4-R1-RF-2): a terminal admitted after a teardown trigger still
/// starts the teardown span (M3-L r1:402), on fixed instants: the trigger a
/// known 150 ms before the terminal, which `reach_terminal` observes
/// although a cause exists. The normal end's grace does not start, the first
/// cause stays, and the one stage terminal is recorded.
#[test]
fn a_terminal_after_a_fault_starts_the_teardown_span() {
    use opensip_operability as op;
    let ms = Duration::from_millis;
    let (mut supervision, _events) =
        prepared("normal", FixtureParticipant::new(FIXTURE_WAITS), None);
    let triggered = Instant::now().checked_sub(ms(150)).expect("an instant");
    supervision.first_cause = Some(Cause::HostFault);
    supervision.teardown_from = Some(triggered);
    // No terminal yet: the trigger starts the span.
    assert_eq!(supervision.teardown_span(triggered + ms(400)), ms(400));
    supervision.reach_terminal(TerminalKind::Complete);
    let observed = supervision
        .terminal_observed
        .expect("the terminal is observed although a cause exists");
    assert!(observed.saturating_duration_since(triggered) >= ms(150));
    assert_eq!(supervision.teardown_span(observed + ms(250)), ms(250));
    assert!(supervision.terminal_at.is_none(), "no normal-end grace");
    assert_eq!(supervision.first_cause, Some(Cause::HostFault));
    let facts = supervision.seams.facts.borrow();
    assert!(
        matches!(
            facts.as_slice(),
            [RecordFact::StageTerminal {
                terminal: op::StageTerminal::Complete,
                ..
            }]
        ),
        "{facts:?}"
    );
}

/// r2 (D3A4-R1-RF-2): with no terminal, the teardown span starts at the
/// first teardown trigger: it covers the trigger to the reap, and `crash`
/// is the one stage terminal.
#[test]
fn a_fault_with_no_terminal_starts_the_teardown_span_at_its_trigger() {
    use opensip_operability as op;
    let out = faulted_at_the_first_fact("facts-then-hang");
    assert_eq!(out.settlement.first_cause(), Cause::HostFault);
    assert!(
        !out.events
            .iter()
            .any(|(_, e)| matches!(e, SupervisionEvent::Terminal(_)))
    );
    let triggered = event_at(&out, &SupervisionEvent::Trigger(Cause::HostFault));
    let started = event_at(&out, &SupervisionEvent::TeardownStarted(Cause::HostFault));
    let reaped = event_at(&out, &SupervisionEvent::Reaped);
    let settled = event_at(&out, &SupervisionEvent::Settled(Cause::HostFault));
    let teardown = reaped_teardown(&out);
    assert!(
        teardown >= reaped.saturating_duration_since(started),
        "{teardown:?} covers the trigger to the reap"
    );
    assert!(teardown <= settled.saturating_duration_since(triggered));
    let terminals: Vec<&RecordFact> = out
        .facts
        .iter()
        .filter(|f| matches!(f, RecordFact::StageTerminal { .. }))
        .collect();
    assert!(
        matches!(
            terminals.as_slice(),
            [RecordFact::StageTerminal {
                terminal: op::StageTerminal::Crash,
                ..
            }]
        ),
        "{terminals:?}"
    );
}

/// A tool's reap names its signal too (`tool.process.reaped`'s D3a-4
/// field).
/// Only the wall-clock deadline is shortened for the tool-hang case.
#[test]
fn a_killed_tool_records_its_signal() {
    use opensip_operability as op;
    let out = tool_deadline_run("tool-hang", |_| {});
    assert!(
        out.facts.iter().any(|f| matches!(
            f,
            RecordFact::ToolReaped {
                exit: op::ExitClass::Signaled,
                signal: Some(op::ChildSignal::Sigterm | op::ChildSignal::Sigkill),
                ..
            }
        )),
        "{:?}",
        out.facts
    );
}

/// Every P3T phase maps to its `ProviderState` member and back to the same
/// spelling; an unknown name maps to none.
#[test]
fn every_table_phase_is_a_provider_state() {
    use opensip_operability::CodeEnum;
    for (index, text) in opensip_operability::ProviderState::TEXT.iter().enumerate() {
        let state = records::provider_state(text).unwrap_or_else(|| panic!("{text}"));
        assert_eq!(state as usize, index, "{text}");
    }
    assert!(records::provider_state("NOT_A_PHASE").is_none());
    // The vendored P3T and T2O phase lists (S-OP-2c LD-OPT-2): P3T's is the
    // table exactly, in order, and T2O's a subset.
    let phases = |file: &str| -> Vec<String> {
        let text = std::fs::read_to_string(
            Path::new(env!("CARGO_MANIFEST_DIR"))
                .join("data")
                .join(file),
        )
        .expect("a vendored table");
        let (_, rest) = text.split_once("\"phases\": [").expect("phases");
        let (list, _) = rest.split_once(']').expect("the list");
        list.split(',')
            .map(|p| p.trim().trim_matches('"').to_owned())
            .collect()
    };
    let p3t = phases("protocol3-transitions.v1.json");
    assert_eq!(p3t, opensip_operability::ProviderState::TEXT);
    for phase in phases("typescript-protocol2-order.v1.json") {
        assert!(records::provider_state(&phase).is_some(), "{phase}");
    }
}

// ------------------------------------------------------------------ D3b-1: item 18's descendant step (macOS)

/// A per-test file for a tree fixture's pids, and the script naming it.
fn tree_script(kind: &str) -> (PathBuf, &'static str) {
    static NEXT: AtomicU64 = AtomicU64::new(0);
    let file = std::env::temp_dir().join(format!(
        "opensip-d3b1-pids-{}-{}",
        std::process::id(),
        NEXT.fetch_add(1, Ordering::Relaxed)
    ));
    let script: &'static str =
        Box::leak(format!("tool-tree-{kind}:{}", file.display()).into_boxed_str());
    (file, script)
}
/// The pids a tree fixture wrote.
fn tree_pids(file: &Path) -> Vec<i32> {
    let text = std::fs::read_to_string(file).expect("the fixture's pids");
    std::fs::remove_file(file).ok();
    text.split_whitespace()
        .map(|p| p.parse().expect("a pid"))
        .collect()
}
/// Whether `pid` has an identity: alive and not a zombie.
fn has_identity(pid: i32) -> bool {
    matches!(opensip_platform::process_identity(pid), Ok(Some(_)))
}
fn eventually_without_identity(pid: i32) -> bool {
    let started = Instant::now();
    while started.elapsed() < Duration::from_secs(5) {
        if !has_identity(pid) {
            return true;
        }
        std::thread::sleep(Duration::from_millis(25));
    }
    false
}
/// A test's out-of-band kill of a survivor macOS cannot reach.
fn kill_out_of_band(pid: i32) {
    let status = std::process::Command::new("/bin/kill")
        .args(["-9", &pid.to_string()])
        .status()
        .expect("kill");
    assert!(status.success(), "{pid}");
    assert!(eventually_without_identity(pid), "{pid} survived");
}
fn evidence(out: &ToolOutcome) -> &TreeEvidence {
    out.settlement.tree_evidence().expect("a kill's evidence")
}
fn tool_tree_swept(out: &ToolOutcome) -> Vec<(u64, u64, bool)> {
    out.facts
        .iter()
        .filter_map(|f| match f {
            RecordFact::ToolTreeSwept {
                killed,
                unattributed,
                platform_limited,
            } => Some((*killed, *unattributed, *platform_limited)),
            _ => None,
        })
        .collect()
}

/// D5-T1 (item 18, :617): a descendant in the group dies with it. The walk
/// finds it; it is left to the group's SIGKILL, never killed by pid; the
/// confirm sees the zombie root alone after its exit: `group-killed,
/// platform-limited`. `killed` counts by-pid sends only, so it is 0.
/// Only the wall deadline is shortened to exercise this tree-teardown scenario.
/// A recorded native killpg EPERM stays incomplete; no errno or failure is normalized away.
#[test]
fn an_in_group_descendant_dies_with_the_group() {
    let (file, script) = tree_script("ingroup");
    let out = tool_deadline_run(script, |_| {});
    let [member] = tree_pids(&file)[..] else {
        panic!("one member");
    };
    assert_eq!(out.settlement.first_cause(), Cause::Deadline);
    let e = evidence(&out);
    // The baseline native run also observed EPERM from killpg on a held
    // zombie. Keep that original failure and its incomplete report.
    assert!(
        e.failures.iter().all(|failure| {
            failure.step == TreeCall::GroupKill
                && matches!(&failure.error, LaunchError::Io { call, error }
                if *call == "killpg" && error.raw_os_error() == Some(1))
        }),
        "only the observed native killpg EPERM is allowed: {e:?}"
    );
    assert_eq!(e.group_kill_failures as usize, e.failures.len());
    let want = if e.group_kill_failures == 0 {
        TreeReport::GroupKilledPlatformLimited
    } else {
        TreeReport::IncompletePlatformLimited
    };
    assert_eq!(out.settlement.tree(), want, "{e:?}");
    assert_eq!(e.snapshot, SnapshotOutcome::Complete);
    assert_eq!((e.queued, e.inspected), (2, 2));
    assert_eq!(e.by_pid.in_group, 1);
    assert_eq!(e.by_pid.sent, 0);
    assert!(
        e.group_kills > e.group_kill_failures,
        "at least one successful native group signal"
    );
    assert_eq!(e.confirm, ConfirmOutcome::RootAlone);
    assert_eq!(tool_tree_swept(&out), [(0, 0, true)]);
    assert!(eventually_without_identity(member));
    out.nothing_left();
}

/// D5-T2 (:618): a descendant that left the group before the snapshot is
/// found by the walk and killed by pid on an equal identity: `killed` 1,
/// still `platform-limited`; the test confirms it gone out of band.
/// Only the wall deadline is shortened to exercise this tree-teardown scenario.
#[test]
fn an_escaped_descendant_is_killed_by_pid() {
    let (file, script) = tree_script("escape");
    let out = tool_deadline_run(script, |_| {});
    let [escapee] = tree_pids(&file)[..] else {
        panic!("one escapee");
    };
    let e = evidence(&out);
    assert_eq!(e.snapshot, SnapshotOutcome::Complete);
    assert_eq!((e.by_pid.sent, e.by_pid.in_group), (1, 0));
    assert_eq!(tool_tree_swept(&out), [(1, 0, true)]);
    assert!(eventually_without_identity(escapee));
}

/// D5-T2b: pause after the snapshot, then let a snapshotted member
/// fork a real child outside the group. The snapshot cannot target it.
/// Only the wall deadline is shortened to exercise this tree-teardown scenario.
#[test]
fn a_descendant_the_snapshot_missed_survives() {
    let (file, script) = tree_script("fork-after-snapshot");
    let gate = PathBuf::from(format!("{}.go", file.display()));
    let late = PathBuf::from(format!("{}.late", file.display()));
    let late_hook = late.clone();
    let out = tool_deadline_run_with(
        script,
        Box::new(move |s| {
            s.seams.tree_hook = Some(TreeHook(Box::new(move |step, _targets| {
                if step == TreeStep::AfterSnapshot {
                    std::fs::write(&gate, b"go").expect("release the member");
                    let started = Instant::now();
                    while !late_hook.exists() {
                        assert!(
                            started.elapsed() < Duration::from_secs(5),
                            "late child not created"
                        );
                        std::thread::sleep(Duration::from_millis(2));
                    }
                    std::fs::remove_file(&gate).ok();
                }
            })));
        }),
    );
    let members = tree_pids(&file);
    let late = tree_pids(&late);
    assert_eq!(evidence(&out).by_pid.sent, 0);
    assert_eq!(evidence(&out).queued, 2);
    assert_eq!(tool_tree_swept(&out), [(0, 0, true)]);
    for member in members {
        assert!(eventually_without_identity(member));
    }
    assert_eq!(late.len(), 1);
    assert!(has_identity(late[0]), "macOS cannot reach it");
    kill_out_of_band(late[0]);
}

/// RF-2: the same pid leaves its original group after the snapshot. Its
/// fresh pgid makes it eligible for an identity-checked by-pid send.
/// Only the wall deadline is shortened to exercise this tree-teardown scenario.
#[test]
fn a_snapshot_member_that_changes_group_is_targeted() {
    let (file, script) = tree_script("change-group");
    let gate = PathBuf::from(format!("{}.go", file.display()));
    let out = tool_deadline_run_with(
        script,
        Box::new(move |s| {
            s.seams.tree_hook = Some(TreeHook(Box::new(move |step, targets| {
                if step == TreeStep::AfterSnapshot {
                    assert_eq!(targets.len(), 1);
                    let target = targets[0];
                    assert_ne!(target.pgid(), target.process_id());
                    std::fs::write(&gate, b"go").expect("release the member");
                    let started = Instant::now();
                    loop {
                        if process_identity(target.process_id())
                            .expect("identity")
                            .is_some_and(|now| now.pgid() == target.process_id())
                        {
                            break;
                        }
                        assert!(
                            started.elapsed() < Duration::from_secs(5),
                            "member did not leave group"
                        );
                        std::thread::sleep(Duration::from_millis(2));
                    }
                    std::fs::remove_file(&gate).ok();
                }
            })));
        }),
    );
    let pids = tree_pids(&file);
    assert_eq!(evidence(&out).by_pid.sent, 1);
    assert_eq!(tool_tree_swept(&out), [(1, 0, true)]);
    for pid in pids {
        assert!(eventually_without_identity(pid));
    }
}

/// D5-T2c (:622) and Q3: an injected snapshot listing failure, an injected
/// confirm listing failure and an injected group-SIGKILL failure each leave
/// the tree `incomplete`, and each is in the evidence. A failed confirm
/// listing is latched: no later singleton clears it.
/// Only the wall deadline is shortened to exercise this tree-teardown scenario.
#[test]
fn a_failed_listing_or_group_kill_leaves_the_tree_incomplete() {
    let (file, script) = tree_script("ingroup");
    let out = tool_deadline_run(script, |s| s.seams.snapshot_listing_fails = true);
    let pids = tree_pids(&file);
    assert_eq!(out.settlement.tree(), TreeReport::IncompletePlatformLimited);
    assert_eq!(evidence(&out).snapshot, SnapshotOutcome::ListingFailed);
    pids.iter()
        .for_each(|p| assert!(eventually_without_identity(*p)));

    let (file, script) = tree_script("ingroup");
    let out = tool_deadline_run(script, |s| s.seams.confirm_listing_fails = true);
    let pids = tree_pids(&file);
    assert_eq!(out.settlement.tree(), TreeReport::IncompletePlatformLimited);
    assert_eq!(evidence(&out).confirm, ConfirmOutcome::ListingFailed);
    assert_eq!(evidence(&out).snapshot, SnapshotOutcome::Complete);
    pids.iter()
        .for_each(|p| assert!(eventually_without_identity(*p)));

    // All group SIGKILL attempts fail. The ignored SIGTERM leaves a live
    // root at abandonment; both it and the member are cleaned up out of band.
    let (file, script) = tree_script("ingroup");
    let out = tool_deadline_run(script, |s| {
        s.seams.group_kill_fails = true;
        s.seams.tree_hook = Some(TreeHook(Box::new(|step, targets| {
            if step == TreeStep::AfterSnapshot {
                assert!(
                    targets
                        .iter()
                        .all(|target| target.process_id() != target.pgid()),
                    "the owned root must not enter the by-pid target set"
                );
            }
        })));
    });
    let pids = tree_pids(&file);
    let e = evidence(&out);
    assert_eq!(out.settlement.tree(), TreeReport::IncompletePlatformLimited);
    assert!(e.group_kill_failures >= 1);
    let root = out.process_id.expect("root");
    let root_was_alive = has_identity(root);
    if root_was_alive {
        kill_out_of_band(root);
    }
    assert!(
        root_was_alive,
        "the ignored TERM and failed KILL leave a live root"
    );
    assert!(
        !has_identity(root),
        "out-of-band cleanup removed the live root"
    );
    assert_eq!(out.settlement.exit(), ExitClass::Unreaped);
    assert!(!out.saw(&SupervisionEvent::ExitObserved));
    assert_eq!(e.confirm, ConfirmOutcome::MembersListed);
    assert_eq!(e.by_pid.sent, 0);
    assert!(!out.tree_calls.contains(&TreeCallAttempt::ByPid(root)));
    assert_eq!(
        out.tree_calls
            .iter()
            .filter(|call| **call == TreeCallAttempt::Group)
            .count() as u64,
        e.group_kills
    );
    let ceiling = out
        .events
        .iter()
        .position(|event| *event == SupervisionEvent::WaitExpired(BoundedWait::ReapCeiling))
        .expect("ceiling");
    assert!(
        !out.events[ceiling..]
            .iter()
            .any(|event| matches!(event, SupervisionEvent::Signalled { .. }))
    );
    assert_eq!(e.failures.len() as u64, e.group_kill_failures);
    assert!(e.failures.iter().all(|f| f.step == TreeCall::GroupKill
        && matches!(&f.error, LaunchError::Io { call: "killpg", error }
            if error.raw_os_error() == Some(1))));
    for pid in pids {
        if has_identity(pid) {
            kill_out_of_band(pid);
        }
    }
}

/// RF-2 and Q10: a member the confirm keeps listing is a late joiner,
/// counted once however many confirms repeat; each repeat sends the group
/// SIGKILL again, and no target is counted twice; at the ceiling the tree
/// is `incomplete`.
/// Only the wall deadline is shortened to exercise this tree-teardown scenario.
#[test]
fn a_repeated_confirm_counts_a_late_joiner_once() {
    let (file, script) = tree_script("ingroup");
    let out = tool_deadline_run(script, |s| s.seams.extra_member = true);
    tree_pids(&file);
    let e = evidence(&out);
    assert_eq!(out.settlement.tree(), TreeReport::IncompletePlatformLimited);
    assert_eq!(e.confirm, ConfirmOutcome::MembersListed);
    assert_eq!(e.late_joiners, 1);
    assert!(e.group_kills >= 2, "{e:?}");
    // Each inspected pid lands in exactly one bucket, once.
    let b = e.by_pid;
    assert_eq!(
        b.sent
            + b.identity_changed
            + b.exited
            + b.refused
            + b.failed
            + b.in_group
            + e.identity_failed,
        e.inspected - 1,
        "{e:?}"
    );
    assert!(out.saw(&SupervisionEvent::WaitExpired(BoundedWait::ReapCeiling)));
}

/// RF-2: a target that exited between the snapshot and the identity-checked
/// kill is `exited`, never `sent`.
/// Only the wall deadline is shortened to exercise this tree-teardown scenario.
#[test]
fn a_target_gone_before_its_kill_is_not_counted_as_killed() {
    let (file, script) = tree_script("escape");
    let pidfile = file.clone();
    let out = tool_deadline_run_with(
        script,
        Box::new(move |s| {
            s.seams.tree_hook = Some(TreeHook(Box::new(move |step, targets| {
                if step == TreeStep::AfterGroupKill {
                    for target in targets.iter() {
                        let pid = target.process_id();
                        std::process::Command::new("/bin/kill")
                            .args(["-9", &pid.to_string()])
                            .status()
                            .ok();
                        let started = Instant::now();
                        while has_identity(pid) && started.elapsed() < Duration::from_secs(5) {
                            std::thread::sleep(Duration::from_millis(10));
                        }
                    }
                }
            })));
        }),
    );
    tree_pids(&pidfile);
    let e = evidence(&out);
    assert_eq!((e.by_pid.sent, e.by_pid.exited), (0, 1), "{e:?}");
    assert_eq!(tool_tree_swept(&out), [(0, 0, true)]);
}

/// D5-T3 (:623): a double-forked daemon orphaned to launchd before teardown
/// is unreachable on macOS: the walk cannot find it, the tree is still
/// `group-killed, platform-limited`, and the test observes it alive and
/// cleans it up.
/// Only the wall deadline is shortened to exercise this tree-teardown scenario.
#[test]
fn a_daemon_orphaned_before_teardown_survives() {
    let (file, script) = tree_script("daemon");
    let out = tool_deadline_run(script, |_| {});
    let [daemon] = tree_pids(&file)[..] else {
        panic!("one daemon");
    };
    let e = evidence(&out);
    assert_eq!((e.queued, e.by_pid.sent), (1, 0));
    assert_eq!(
        out.settlement.tree(),
        TreeReport::GroupKilledPlatformLimited,
        "{:?}",
        out.settlement.tree_evidence()
    );
    assert!(has_identity(daemon), "macOS cannot reach it");
    kill_out_of_band(daemon);
}

/// D5-T4 (:624): more descendants than the tool's walk bound (4 × 16 = 64)
/// reach the bound: `BoundReached` and `incomplete`, even though the
/// confirm later lists the root alone (Q3).
/// Only the wall deadline is shortened to exercise this tree-teardown scenario.
#[test]
fn a_fork_loop_reaches_the_walk_bound() {
    let (file, script) = tree_script("loop");
    let out = tool_deadline_run(script, |s| s.seams.process_count_off = true);
    let pids = tree_pids(&file);
    let e = evidence(&out);
    assert_eq!(e.snapshot, SnapshotOutcome::BoundReached);
    assert!(e.queued <= 64, "{e:?}");
    assert_eq!(out.settlement.tree(), TreeReport::IncompletePlatformLimited);
    for pid in pids {
        assert!(eventually_without_identity(pid), "{pid}");
    }
}

/// LD-D3B-3 bounds every visited pid, including the root: a tool's
/// snapshot can visit 64 total, not 64 descendants plus the root.
/// Only the wall deadline is shortened to exercise this tree-teardown scenario.
#[test]
fn the_snapshot_walk_bound_includes_its_root() {
    for (kind, children, expected) in [
        ("walk-exact", 63, SnapshotOutcome::Complete),
        ("walk-over", 64, SnapshotOutcome::BoundReached),
    ] {
        let (file, script) = tree_script(kind);
        let out = tool_deadline_run(script, |s| s.seams.process_count_off = true);
        let pids = tree_pids(&file);
        assert_eq!(pids.len(), children);
        let observed = evidence(&out);
        assert_eq!(observed.snapshot, expected, "{kind}: {observed:?}");
        assert!(
            observed.queued <= 64,
            "root also occupies a slot: {observed:?}"
        );
        if expected == SnapshotOutcome::Complete {
            assert_eq!((observed.queued, observed.inspected), (64, 64));
        }
        for pid in pids {
            assert!(eventually_without_identity(pid), "{kind}: {pid}");
        }
    }
}

/// D5-T5 (:625): a descendant that survives SIGTERM is killed by the group's
/// SIGKILL after the escalation's wait.
/// Only the wall deadline is shortened to exercise this tree-teardown scenario.
#[test]
fn a_sigterm_survivor_is_killed_after_the_escalation() {
    let (file, script) = tree_script("term-survivor");
    let out = tool_deadline_run(script, |_| {});
    let [survivor] = tree_pids(&file)[..] else {
        panic!("one survivor");
    };
    assert!(out.saw(&SupervisionEvent::Signalled { signal: SIGTERM }));
    assert!(out.saw(&SupervisionEvent::Signalled { signal: SIGKILL }));
    assert!(eventually_without_identity(survivor));
}

/// D3-T9 (item 4, :263): a root that exits on its own before teardown, its
/// group empty, is reaped with no signal at all; the tree is `NotKilled`
/// and no sweep evidence exists.
#[test]
fn a_root_that_exits_first_is_reaped_with_no_signal() {
    let out = tool_run("tool-ok", |_| {});
    assert!(
        !out.events
            .iter()
            .any(|e| matches!(e, SupervisionEvent::Signalled { .. })),
        "{:?}",
        out.events
    );
    assert_eq!(out.settlement.tree(), TreeReport::NotKilled);
    assert!(out.settlement.tree_evidence().is_none());
    assert!(tool_tree_swept(&out).is_empty());
}

/// Item 18's escalation sentence (:606): a root held unreaped past the
/// ceiling is `exit: unreaped`, and no group signal follows the ceiling.
/// Only the wall deadline is shortened to exercise this tree-teardown scenario.
#[test]
fn no_group_signal_follows_the_reap_ceiling() {
    let (file, script) = tree_script("ingroup");
    let out = tool_deadline_run(script, |s| s.seams.reap_blocked = true);
    let pids = tree_pids(&file);
    assert_eq!(out.settlement.exit(), ExitClass::Unreaped);
    assert!(
        out.saw(&SupervisionEvent::ExitObserved),
        "this control holds an exited root unreaped"
    );
    assert_eq!(evidence(&out).confirm, ConfirmOutcome::RootAlone);
    let ceiling = out
        .events
        .iter()
        .position(|e| *e == SupervisionEvent::WaitExpired(BoundedWait::ReapCeiling))
        .expect("the ceiling");
    assert!(
        !out.events[ceiling..]
            .iter()
            .any(|e| matches!(e, SupervisionEvent::Signalled { .. })),
        "{:?}",
        out.events
    );
    pids.iter()
        .for_each(|p| assert!(eventually_without_identity(*p)));
}

/// LD-D3B-12 (item 23, :737) is the lane's structural check over the
/// production sources; this pins the walk bound's arithmetic (:592).
#[test]
fn the_walk_bound_is_four_times_the_class_count() {
    assert_eq!(WALK_BOUND_FACTOR * PROVIDER_PROCESSES, 4);
    assert_eq!(WALK_BOUND_FACTOR * TOOL_PROCESSES, 64);
}

/// A named, unmodified native error for the descendant-step failure seams.
pub(crate) fn tree_io_error(call: &'static str, errno: i32) -> LaunchError {
    LaunchError::Io {
        call,
        error: std::io::Error::from_raw_os_error(errno),
    }
}

/// A later successful confirmation cannot erase an exceeded native list.
/// Only the wall deadline is shortened to exercise this tree-teardown scenario.
#[test]
fn an_exceeded_confirm_stays_incomplete_after_a_singleton() {
    let (file, script) = tree_script("ingroup");
    let out = tool_deadline_run(script, |s| s.seams.confirm_exceeded_once = true);
    let pids = tree_pids(&file);
    let e = evidence(&out);
    assert_eq!(e.confirm, ConfirmOutcome::RootAlone);
    assert!(e.confirm_exceeded);
    assert_eq!(out.settlement.tree(), TreeReport::IncompletePlatformLimited);
    for pid in pids {
        assert!(eventually_without_identity(pid));
    }
}

/// Failure counts do not discard earlier errno values or the native call.
/// Only the wall deadline is shortened to exercise this tree-teardown scenario.
#[test]
fn each_group_kill_failure_keeps_its_original_error() {
    let (file, script) = tree_script("ingroup");
    let out = tool_deadline_run(script, |s| {
        s.seams.extra_member = true;
        s.seams.group_kill_errors = [1, 5].into();
    });
    let pids = tree_pids(&file);
    let e = evidence(&out);
    assert!(e.group_kill_failures >= 2);
    assert!(e.group_kills > 2);
    let errors: Vec<_> = e
        .failures
        .iter()
        .map(|f| {
            assert_eq!(f.step, TreeCall::GroupKill);
            match &f.error {
                LaunchError::Io { call, error } => (*call, error.raw_os_error()),
                other => panic!("unexpected failure {other:?}"),
            }
        })
        .collect();
    assert_eq!(&errors[..2], [("killpg", Some(1)), ("killpg", Some(5))]);
    assert_eq!(errors.len() as u64, e.group_kill_failures);
    assert!(errors.iter().all(|(call, _)| *call == "killpg"));
    assert_eq!(out.settlement.tree(), TreeReport::IncompletePlatformLimited);
    for pid in pids {
        assert!(eventually_without_identity(pid));
    }
}

/// Both identity reads retain their errors, rather than counting them as
/// an exit or allowing a singleton confirm to grant a completed report.
/// Only the wall deadline is shortened to exercise this tree-teardown scenario.
#[test]
fn failed_tree_identity_reads_keep_their_step_and_errno() {
    for step in [TreeCall::SnapshotIdentity, TreeCall::PreKillIdentity] {
        let (file, script) = tree_script("escape");
        let out = tool_deadline_run_with(
            script,
            Box::new(move |s| s.seams.tree_identity_error = Some(step)),
        );
        let pids = tree_pids(&file);
        let e = evidence(&out);
        let failures = if step == TreeCall::SnapshotIdentity {
            2
        } else {
            1
        };
        assert_eq!(e.failures.len(), failures, "{e:?}");
        assert_eq!(e.failures[0].step, step);
        assert!(
            matches!(&e.failures[0].error, LaunchError::Io { call: "proc_pidinfo", error }
            if error.raw_os_error() == Some(5))
        );
        assert_eq!(e.by_pid.sent, 0);
        assert_eq!(e.by_pid.exited, 0);
        assert_eq!(out.settlement.tree(), TreeReport::IncompletePlatformLimited);
        for pid in pids {
            kill_out_of_band(pid);
        }
    }
}

/// The supervisor buckets the platform's typed outcomes without treating
/// a refused, changed-identity or failed send as an observed kill. The
/// platform's real identity/protection syscall controls are D3b-0's.
/// Only the wall deadline is shortened to exercise this tree-teardown scenario.
#[test]
fn unsent_by_pid_outcomes_are_not_reported_as_kills() {
    use opensip_platform::Protected;
    for result in [
        Ok(KillOutcome::IdentityChanged),
        Ok(KillOutcome::Refused(Protected::Host)),
        Err(1),
    ] {
        let (file, script) = tree_script("escape");
        let out = tool_deadline_run_with(
            script,
            Box::new(move |s| s.seams.tree_kill_result = Some(result)),
        );
        let pids = tree_pids(&file);
        let e = evidence(&out);
        assert_eq!(e.by_pid.sent, 0);
        match result {
            Ok(KillOutcome::IdentityChanged) => assert_eq!(e.by_pid.identity_changed, 1),
            Ok(KillOutcome::Refused(_)) => assert_eq!(e.by_pid.refused, 1),
            Err(errno) => {
                assert_eq!(e.by_pid.failed, 1);
                assert_eq!(e.failures.len(), 1);
                assert_eq!(e.failures[0].step, TreeCall::ByPidKill);
                assert!(
                    matches!(&e.failures[0].error, LaunchError::Io { call: "kill", error }
                    if error.raw_os_error() == Some(errno))
                );
            }
            _ => unreachable!(),
        }
        assert_eq!(tool_tree_swept(&out), [(0, 0, true)]);
        assert_eq!(out.settlement.tree(), TreeReport::IncompletePlatformLimited);
        for pid in pids {
            kill_out_of_band(pid);
        }
    }
}

/// LD-D3B-3's provider bound is exercised through the actual class
/// selection in snapshot, using a tool's fixture plumbing only to hold the
/// native process tree. Restore the real tool class before driving its
/// supervision; no provider protocol or qualification is inferred.
/// Only the tool fixture wall deadline is shortened to exercise its ordinary teardown after the explicit snapshot.
#[test]
fn the_provider_snapshot_bound_counts_its_root() {
    for (kind, children, expected) in [
        ("provider-exact", 3, SnapshotOutcome::Complete),
        ("provider-over", 4, SnapshotOutcome::BoundReached),
    ] {
        let (file, script) = tree_script(kind);
        let dir = test_dir();
        let mut supervision = Supervision::prepare_tool_with(
            tool_spec_for(&fixture(), script),
            wall_clock_expiry_waits(),
        )
        .expect("prepared");
        supervision.seams.process_count_off = true;
        let mut root = root_in(&dir);
        supervision.start(&mut root).expect("spawned");
        let started = Instant::now();
        while !file.exists() {
            assert!(
                started.elapsed() < Duration::from_secs(5),
                "fixture not ready"
            );
            std::thread::sleep(Duration::from_millis(2));
        }
        let pid = supervision.child.as_ref().expect("child").process_id();
        let mut kill = TreeKill {
            targets: Vec::new(),
            late: Vec::new(),
            next_confirm: Instant::now(),
            done: false,
            evidence: TreeEvidence::default(),
        };
        supervision.class = Class::Provider;
        assert_eq!(supervision.walk_bound(), 4);
        supervision.snapshot(pid, &mut kill);
        supervision.class = Class::Tool;
        // Complete the native child's ordinary teardown before asserting,
        // so a mutation of the snapshot cannot leak the fixture tree.
        while supervision.state() != State::Settled {
            assert!(
                started.elapsed() < control_cap(supervision.waits),
                "no settlement"
            );
            supervision.turn();
        }
        let settlement = supervision.take_settlement().expect("settlement");
        assert!(matches!(settlement.exit(), ExitClass::Signaled(9)));
        kill.evidence.confirm = settlement.tree_evidence().expect("native confirm").confirm;
        assert_eq!(kill.evidence.confirm, ConfirmOutcome::RootAlone);
        let want = if expected == SnapshotOutcome::Complete {
            TreeReport::GroupKilledPlatformLimited
        } else {
            TreeReport::IncompletePlatformLimited
        };
        assert_eq!(kill.report(), want);
        let pids = tree_pids(&file);
        for pid in &pids {
            assert!(eventually_without_identity(*pid));
        }
        assert_eq!(pids.len(), children);
        assert_eq!(
            kill.evidence.snapshot, expected,
            "{kind}: {:?}",
            kill.evidence
        );
        assert!(kill.evidence.queued <= 4);
        if expected == SnapshotOutcome::Complete {
            assert_eq!((kill.evidence.queued, kill.evidence.inspected), (4, 4));
        }
    }
}

/// RF-1: a root-only tree consumes and reports one queue/identity slot,
/// keeps its original identity, and never attempts a by-pid root signal.
/// Only the wall deadline is shortened to exercise this tree-teardown scenario.
#[test]
fn a_root_only_snapshot_records_the_owned_root() {
    let (file, script) = tree_script("root-only");
    let out = tool_deadline_run(script, |_| {});
    assert!(tree_pids(&file).is_empty());
    let e = evidence(&out);
    let root = out.process_id.expect("owned root");
    assert_eq!((e.queued, e.inspected), (1, 1));
    assert_eq!(
        e.root_identity.expect("live root identity").process_id(),
        root
    );
    assert!(!e.root_exited);
    assert_eq!(e.by_pid, ByPidOutcomes::default());
    assert!(!out.tree_calls.contains(&TreeCallAttempt::ByPid(root)));
    assert_eq!(
        out.settlement.tree(),
        TreeReport::GroupKilledPlatformLimited
    );
}
