// Unit D3a-1's controls (D3a plan r4, §3): each drives the real loop over a
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
use std::sync::OnceLock;
use std::sync::atomic::{AtomicU64, Ordering};

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
                    bytes += frame.payload().len() as u64;
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

/// A prepared supervision over `script`, observed.
fn prepared(
    script: &str,
    participant: FixtureParticipant,
    hook: Option<Hook>,
) -> (Supervision<FixtureParticipant>, Events) {
    let mut supervision =
        Supervision::prepare_with(spec_for(&fixture(), script), participant, quick())
            .expect("prepared");
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
    scratch: Option<PathBuf>,
    process_id: Option<i32>,
}
impl Outcome {
    fn saw(&self, event: &SupervisionEvent) -> bool {
        self.events.iter().any(|(_, e)| e == event)
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
    supervision.start(&mut root);
    while supervision.state() != State::Settled {
        assert!(started.elapsed() < cap, "no settlement within {cap:?}");
        supervision.turn();
    }
    let settlement = supervision.take_settlement().expect("one settlement");
    assert!(supervision.take_settlement().is_none(), "taken once");
    let raw = std::mem::take(&mut supervision.participant.raw);
    let max_reads_per_turn = supervision.seams.max_reads_per_turn;
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
        assert_eq!(s.exit(), Some(ExitClass::Exited(0)), "{script}");
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
    assert_eq!(out.settlement.exit(), Some(ExitClass::Exited(3)));
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
            assert_eq!(out.settlement.exit(), Some(ExitClass::Signaled(SIGTERM)));
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

/// D3-T1: from `Prepared`, D4's two refusals settle with nothing spawned.
#[test]
fn prespawn_refusals_settle_with_nothing_spawned() {
    for (refusal, cause) in [
        (
            PreSpawnRefusal::ClosureRecheckFailed,
            Cause::ClosureRecheckFailed,
        ),
        (
            PreSpawnRefusal::SessionSpecInconsistent,
            Cause::SessionSpecInconsistent,
        ),
    ] {
        let (mut supervision, _) = prepared("normal", FixtureParticipant::new(FIXTURE_WAITS), None);
        supervision.decline(refusal);
        assert_eq!(supervision.state(), State::Settled);
        let s = supervision.take_settlement().expect("one");
        assert_eq!(s.first_cause(), cause);
        assert_eq!(s.exit(), None);
        assert_eq!(s.scratch(), ScratchFate::NoScratch);
    }
}

/// D3-T1: a spawn failure settles `spawn-failed`.
#[test]
fn a_spawn_failure_settles_spawn_failed() {
    let dir = test_dir();
    let missing = dir.0.join("no-such-fixture");
    let mut supervision = Supervision::prepare_with(
        spec_for(&missing, "normal"),
        FixtureParticipant::new(FIXTURE_WAITS),
        quick(),
    )
    .expect("prepared");
    let mut root = root_in(&dir);
    supervision.run(&mut root);
    let s = supervision.take_settlement().expect("one");
    assert_eq!(s.first_cause(), Cause::SpawnFailed);
    assert_eq!(s.exit(), None);
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
            assert_eq!(out.settlement.exit(), Some(ExitClass::Signaled(6)));
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
    assert!(out.saw(&SupervisionEvent::LivenessMissed));
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
    assert!(!out.saw(&SupervisionEvent::LivenessMissed));
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

/// LD-D3A-5 (NBO-1): a late event after settlement is counted and dropped,
/// the settlement is taken once, and `Drop` after the take changes nothing.
#[test]
fn a_late_event_and_a_drop_after_the_take_leave_one_settlement() {
    let dir = test_dir();
    let (mut supervision, events) =
        prepared("normal", FixtureParticipant::new(FIXTURE_WAITS), None);
    let mut root = root_in(&dir);
    supervision.run(&mut root);
    let handle = supervision.handle();
    assert!(handle.host_fault());
    supervision.turn();
    // The one transition into Settled is guarded: a second attempt mints
    // nothing.
    supervision.settle();
    assert!(supervision.take_settlement().is_some());
    assert!(supervision.take_settlement().is_none());
    drop(supervision);
    let events = events.borrow();
    let settled = events
        .iter()
        .filter(|(_, e)| matches!(e, SupervisionEvent::Settled(_)))
        .count();
    assert_eq!(settled, 1);
    assert!(
        events
            .iter()
            .any(|(_, e)| *e == SupervisionEvent::LateEvent)
    );
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
        supervision.start(&mut root);
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
    assert_eq!(out.settlement.exit(), Some(ExitClass::Unreaped));
    assert_eq!(out.settlement.scratch(), ScratchFate::KeptWithUnreapedRoot);
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
    supervision.start(&mut root);
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
        assert_eq!(supervision.protocol_waits(), waits);
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
        assert!(!out.saw(&SupervisionEvent::LivenessMissed), "{script}");
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
