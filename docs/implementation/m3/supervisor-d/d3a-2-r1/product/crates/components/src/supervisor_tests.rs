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

/// The supervision's test seams.
#[derive(Debug, Default)]
pub(crate) struct Seams {
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
        };
        participant.host_frames();
        participant
    }
    fn status(&self) -> ParticipantStatus {
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
        if let ParticipantStatus::Terminal(kind) = self.status()
            && self.output.is_none()
        {
            // The fixture's frames carry no commitment: its terminal is
            // verified as soon as it is admitted.
            self.output = Some(TerminalOutput::mint(kind));
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
    fn report(&self, progress: Vec<Progress>, bytes: u64, eof: bool) -> ParticipantStep {
        ParticipantStep {
            status: self.status(),
            progress,
            admitted_payload_bytes: bytes,
            eof,
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
                        "SnapshotAccepted" => progress.push(Progress::SnapshotAcknowledged),
                        "FactBatch" => progress.push(Progress::FactBatch),
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

/// The test's waits: item 14's shape, shortened.
fn quick() -> Waits {
    Waits {
        handshake: Duration::from_millis(2_000),
        health_ping_interval: Duration::from_millis(50),
        liveness_window: Duration::from_millis(400),
        progress_absent_interval: Duration::from_millis(200),
        wall_clock: Duration::from_millis(4_000),
        term_to_kill: Duration::from_millis(300),
        reap_ceiling: Duration::from_millis(1_000),
        drain: Duration::from_millis(300),
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
    cap: Duration,
) -> Outcome {
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
    }
}

fn outcome(script: &str) -> Outcome {
    let dir = test_dir();
    let (supervision, events) = prepared(script, FixtureParticipant::new(FIXTURE_WAITS), None);
    finish(supervision, events, &dir, Duration::from_secs(20))
}

/// No child and no scratch left (D3-T3's killable, removable case).
fn nothing_left(out: &Outcome) {
    if let Some(pid) = out.process_id {
        assert_eq!(
            group_members(pid).expect("the group"),
            Vec::<i32>::new(),
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
        let out = outcome(script);
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
    let out = outcome("hang");
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
    let out = outcome("blocked");
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
    let out = outcome("slow");
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
    let out = finish(supervision, events, &dir, Duration::from_secs(20));
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
    let out = finish(supervision, events, &dir, Duration::from_secs(20));
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
            assert!(started.elapsed() < Duration::from_secs(10), "{at:?}");
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
            group_members(pid).expect("the group"),
            Vec::<i32>::new(),
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
#[test]
fn an_unreapable_root_and_an_exhausted_removal_are_disclosed() {
    // In the loop: the ladder's ceiling, then the abandon.
    let dir = test_dir();
    let (mut supervision, events) = prepared("fault", FixtureParticipant::new(FIXTURE_WAITS), None);
    supervision.seams.reap_blocked = true;
    let out = finish(supervision, events, &dir, Duration::from_secs(20));
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
    supervision.seams.reap_blocked = true;
    let mut root = root_in(&dir);
    supervision.start(&mut root).expect("spawned");
    let started = Instant::now();
    while supervision.state() != State::Running {
        assert!(started.elapsed() < Duration::from_secs(10), "never running");
        supervision.turn();
    }
    let started = Instant::now();
    drop(supervision);
    assert!(started.elapsed() < Duration::from_secs(5), "finite");
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
    let out = finish(supervision, events, &dir, Duration::from_secs(20));
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
    supervision.waits.drain = Duration::from_millis(50);
    let out = finish(supervision, events, &dir, Duration::from_secs(20));
    assert!(out.saw(&SupervisionEvent::WaitExpired(BoundedWait::Drain)));
    assert_eq!(
        out.settlement.first_cause(),
        Cause::Clean,
        "{:?}",
        out.events
    );
    // TERM to KILL: a group member survives SIGTERM, so the escalation's
    // wait expires and SIGKILL follows.
    let out = outcome("term-survivor");
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
        let out = finish(supervision, events, &dir, Duration::from_secs(30));
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
/// it does not settle within `limit`, so a starved loop cannot hang it.
fn threaded(script: &'static str, setup: Setup, limit: Duration) -> Outcome {
    let (done, finished) = mpsc::channel();
    std::thread::spawn(move || {
        let dir = test_dir();
        let (mut supervision, events) =
            prepared(script, FixtureParticipant::new(FIXTURE_WAITS), None);
        setup(&mut supervision);
        let out = finish(supervision, events, &dir, Duration::from_secs(25));
        done.send(out).ok();
    });
    finished
        .recv_timeout(limit)
        .unwrap_or_else(|_| panic!("{script}: no settlement within {limit:?}"))
}

/// r2 (Codex D3A1-R1-RF-1): an always-ready stderr (`/dev/zero`, never at
/// EOF) is serviced a bounded number of reads per turn, so the wall-clock
/// deadline, health and the ladder still advance and the child settles.
#[test]
fn an_always_ready_stderr_cannot_starve_the_loop() {
    let out = threaded(
        "hang",
        |s| s.seams.stderr_zero = true,
        Duration::from_secs(30),
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
    let out = threaded("control-storm", |_| {}, Duration::from_secs(30));
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
        let out = finish(supervision, events, &dir, Duration::from_secs(25));
        stop.store(true, Ordering::Release);
        spammer.join().ok();
        done.send(out).ok();
    });
    let out = finished
        .recv_timeout(Duration::from_secs(30))
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
        Duration::from_secs(20),
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
            s.waits.liveness_window = Duration::from_secs(5);
        },
        Duration::from_secs(30),
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
    let out = threaded(
        "normal",
        |s| s.seams.control_write_chunk = Some(1),
        Duration::from_secs(30),
    );
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
    assert_eq!(
        out.settlement.tree(),
        TreeReport::GroupKilledPlatformLimited
    );
    let out = threaded(
        "fault",
        |s| s.seams.extra_member = true,
        Duration::from_secs(20),
    );
    assert_eq!(out.settlement.tree(), TreeReport::Incomplete);
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
                assert!(started.elapsed() < Duration::from_secs(10), "{at:?}");
                supervision.turn();
            }
            drop(supervision);
            let settlement = unwound
                .recv_timeout(Duration::from_secs(1))
                .expect("the unwind's settlement");
            let want = if extra_member {
                TreeReport::Incomplete
            } else {
                TreeReport::GroupKilledPlatformLimited
            };
            assert_eq!(settlement.tree(), want, "{at:?}, extra {extra_member}");
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
        while !stopping.load(Ordering::Acquire) && started.elapsed() < Duration::from_secs(30) {
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
        let out = finish(supervision, events, &dir, Duration::from_secs(20));
        done.send(out).ok();
    });
    finished
        .recv_timeout(Duration::from_secs(30))
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
        Duration::from_secs(20),
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
    events: Vec<SupervisionEvent>,
    scratch: Option<PathBuf>,
    process_id: Option<i32>,
}
impl ToolOutcome {
    fn saw(&self, event: &SupervisionEvent) -> bool {
        self.events.contains(event)
    }
    fn nothing_left(&self) {
        if let Some(pid) = self.process_id {
            assert_eq!(group_members(pid).expect("the group"), Vec::<i32>::new());
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
    let (done, finished) = mpsc::channel();
    std::thread::spawn(move || {
        let dir = test_dir();
        let mut supervision =
            Supervision::prepare_tool_with(tool_spec_for(&fixture(), script), quick())
                .expect("prepared");
        setup(&mut supervision);
        let (sink, events) = mpsc::channel();
        supervision.observer = Some(Box::new(move |event| {
            sink.send(event.clone()).ok();
        }));
        let mut root = root_in(&dir);
        let started = Instant::now();
        supervision.start(&mut root).expect("spawned");
        while supervision.state() != State::Settled {
            assert!(started.elapsed() < Duration::from_secs(20), "no settlement");
            supervision.turn();
        }
        let settlement = supervision.take_settlement().expect("one settlement");
        let scratch = supervision.seams.scratch.clone();
        drop(supervision);
        let events: Vec<SupervisionEvent> = events.try_iter().collect();
        let process_id = events.iter().find_map(|e| match e {
            SupervisionEvent::Spawned { process_id } => Some(*process_id),
            _ => None,
        });
        done.send(ToolOutcome {
            settlement,
            events,
            scratch,
            process_id,
        })
        .ok();
    });
    finished
        .recv_timeout(Duration::from_secs(30))
        .unwrap_or_else(|_| panic!("{script}: no settlement within 30 s"))
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
#[test]
fn a_tools_wall_clock_and_held_output_end_it() {
    let out = tool_run("tool-hang", |_| {});
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
        Supervision::prepare_tool_with(tool_spec_for(&fixture(), "tool-hang"), quick())
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
