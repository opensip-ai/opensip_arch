//! M3-D r5 item 10 (unit D2b-3b; A2-1): the TS2 participant the supervisor
//! drives (D3a's `Participant`, LD-D3A-3). It is the only reader of fd1 and
//! the only writer of fd0, and each call makes at most one non-blocking read
//! or write.
//!
//! - **Writes.** It writes exactly the sender's planned slots
//!   (HOST-SEND-SCHEDULE), each only when T2O admits it (the receiver's
//!   [`Ts2Receiver::admits`]). Each is recorded as sent state when the sender
//!   accepts it, before any byte is written.
//! - **Reads.** The worker's frames are read through D2b-1's accumulator and
//!   admitted by D2b-3a's receiver. Each admitted FactBatch, Coverage and
//!   terminal frame's received payload is spooled `CANDIDATE_ONLY` (item 20:
//!   "Everything is a candidate until settlement"; unit D2b-3c, LD-D2B3C-1)
//!   and moves into the terminal output when it is
//!   minted (item 20, D3a-3); a settlement that is not admissible discards
//!   both. The span boundaries (M3-L r1:400) are the manifest's acceptance,
//!   SnapshotAccepted, and NativeContextVerified or the pre-Analyze
//!   Unavailable.
//! - **Faults.**
//!   - A worker frame the receiver refuses, or a truncated stream, is `Fault`
//!     (`provider-protocol`).
//!   - A frame the host cannot supply (the sealed snapshot's bytes), a
//!     sender divergence, or a failed read or write of the host's own pipe
//!     end is `HostFault` (LD-D2B3B-1).
//!
//! The user's Cancel is [`Ts2Participant::cancel`]: D3b, which owns user
//! cancellation, adds its caller (LD-D2B3B-4).
use super::super::cbor::{self, Profile, Value};
use super::super::table::{Protocol, Table};
use super::super::{FrameAccumulator, ProcessEvent};
use super::carrier::field;
use super::send::{SnapshotSource, Ts2Request, Ts2Sender};
use super::{DispatchContext, HostFrame, TS2_FRAME_MAX_DEPTH, Ts2Receiver, Ts2Refusal};
use crate::supervisor::{
    Boundary, CancelProgress, Participant, ParticipantStatus, ParticipantStep, Progress,
    ProtocolWaits, Spool, TerminalKind, TerminalOutput,
};
use opensip_contracts::generated::protocol::Ts2FrameV2Payload as P;
use std::io::{self, Read, Write};

/// The frames whose received payloads are spooled for H (item 20; LD-D2B3C-1,
/// correcting D2b-3b's FactBatch-only spool): the candidates, every Coverage
/// frame, and the terminal, whose census and terminal Coverage H admits
/// (LD-D2B-16; MH item 4).
const SPOOLED: [&str; 5] = [
    "FactBatch",
    "Coverage",
    "Complete",
    "Unavailable",
    "BudgetExhausted",
];

/// The most fd1 bytes one read takes: D3a's service quantum for fd1 reads
/// (`supervisor.rs` `TOOL_READ_BUFFER`, LD-D3A1-8), not a bound of the law.
const READ_QUANTUM: usize = 65_536;

/// The TS2 participant for one session.
pub struct Ts2Participant<'t> {
    receiver: Ts2Receiver<'t>,
    sender: Ts2Sender,
    source: Box<dyn SnapshotSource>,
    accumulator: FrameAccumulator,
    pending: Vec<u8>,
    at: usize,
    closed: bool,
    cancel_requested: bool,
    pending_frame: Option<HostFrame>,
    cancel_progress: CancelProgress,
    protocol_fault: bool,
    host_fault: bool,
    output: Option<TerminalOutput>,
    minted: bool,
    /// Item 20's candidates (D3a-3): each admitted [`SPOOLED`] frame's payload
    /// bytes, as received, in admission order, moved into the terminal output
    /// when it is minted.
    spool: Spool,
    /// The span boundaries admitted since the last step (M3-L r1:400).
    boundaries: Vec<Boundary>,
}

impl std::fmt::Debug for Ts2Participant<'_> {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("Ts2Participant")
            .field("phase", &self.receiver.phase())
            .field("sender", &self.sender)
            .field("closed", &self.closed)
            .finish_non_exhaustive()
    }
}

fn members(v: &Value) -> &[(String, Value)] {
    match v {
        Value::Map(m) => m,
        _ => &[],
    }
}
fn same(a: Option<&Value>, b: &Value) -> bool {
    a.is_some_and(|a| cbor::encode(a) == cbor::encode(b))
}
fn text(s: &str) -> Value {
    Value::Text(s.to_owned())
}

/// The context and the request describe one session (LD-D2B3B-5): every
/// value the receiver checks an echo against is the value the sender sends.
fn joins(c: &DispatchContext, r: &Ts2Request) -> Result<(), String> {
    let mismatch = |what: &str| Err(format!("the context and the request disagree: {what}"));
    let hello = members(r.hello());
    let texts = |items: &[String]| Value::Array(items.iter().map(|s| text(s)).collect());
    let numbers = |m: &std::collections::BTreeMap<String, u64>| {
        Value::Map(
            m.iter()
                .map(|(k, v)| (k.clone(), Value::Unsigned(*v)))
                .collect(),
        )
    };
    if !same(
        field(hello, "expectedCapabilities"),
        &texts(&c.capabilities),
    ) {
        return mismatch("expectedCapabilities");
    }
    if !same(
        field(hello, "identityVersions"),
        &numbers(&c.identity_versions),
    ) {
        return mismatch("identityVersions");
    }
    for (m, want) in [
        (
            "expectedProviderDescriptorSha256",
            &c.expected_provider_descriptor_sha256,
        ),
        (
            "expectedRuntimeDescriptorSha256",
            &c.expected_runtime_descriptor_sha256,
        ),
    ] {
        if !same(field(hello, m), &text(want)) {
            return mismatch(m);
        }
    }
    let open = members(r.open_universe());
    for (m, want) in [
        ("executionId", &c.execution_id),
        ("snapshotId", &c.snapshot_id),
        ("planId", &c.plan_id),
        ("universeKey", &c.universe_key),
    ] {
        if !same(field(open, m), &text(want)) {
            return mismatch(m);
        }
    }
    let manifest = members(r.manifest());
    if !same(field(manifest, "manifestSha256"), &text(&c.manifest_sha256)) {
        return mismatch("manifestSha256");
    }
    let files: std::collections::BTreeMap<String, (String, u64)> = match field(manifest, "entries")
    {
        Some(Value::Array(entries)) => entries
            .iter()
            .filter(|e| same(field(members(e), "kind"), &text("file")))
            .filter_map(|e| {
                let e = members(e);
                match (
                    field(e, "path"),
                    field(e, "contentSha256"),
                    field(e, "byteLength"),
                ) {
                    (Some(Value::Text(p)), Some(Value::Text(s)), Some(Value::Unsigned(n))) => {
                        Some((p.clone(), (s.clone(), *n)))
                    }
                    _ => None,
                }
            })
            .collect(),
        _ => return mismatch("entries"),
    };
    if files != c.manifest_files {
        return mismatch("the manifest's files");
    }
    let seal = members(r.seal());
    for (m, want) in [
        ("entryCount", c.entry_count),
        ("totalFileBytes", c.total_file_bytes),
        ("totalChunkCount", c.total_chunk_count),
    ] {
        if !same(field(seal, m), &Value::Unsigned(want)) {
            return mismatch(m);
        }
    }
    // The census request (LD-D2B-16): the context's is the Analyze's.
    let requested = match field(members(r.analyze()), "symbolCensus") {
        Some(Value::Map(m)) => match field(m, "enumeratorClosure") {
            Some(Value::Text(c)) => Some(c.clone()),
            _ => return mismatch("symbolCensus"),
        },
        _ => None,
    };
    if requested != c.symbol_census {
        return mismatch("symbolCensus");
    }
    let Some(Value::Array(stages)) = field(members(r.analyze()), "stageRequests") else {
        return mismatch("stageRequests");
    };
    if stages.len() != c.stages.len() {
        return mismatch("the stage count");
    }
    let build = c.provider_descriptor.get("providerBuildId");
    for (s, b) in stages.iter().zip(&c.stages) {
        let s = members(s);
        let domain = field(s, "requestedCoverageDomain")
            .map(members)
            .unwrap_or(&[]);
        let keys = Value::Array(
            b.keys
                .iter()
                .map(|k| {
                    Value::Map(vec![
                        ("relation".to_owned(), text(&k.relation)),
                        ("resolution".to_owned(), text(&k.resolution)),
                        ("sourceUniverseId".to_owned(), text(&k.source_universe_id)),
                        ("targetUniverseId".to_owned(), text(&k.target_universe_id)),
                        (
                            "subjectScopeCommitment".to_owned(),
                            text(&k.subject_scope_commitment),
                        ),
                        ("producer".to_owned(), text("typescript-semantic")),
                        (
                            "producerVersion".to_owned(),
                            build.cloned().unwrap_or(Value::Null),
                        ),
                        ("schemaVersion".to_owned(), Value::Unsigned(1)),
                    ])
                })
                .collect(),
        );
        if !(same(field(s, "stageId"), &text(&b.expected_stage_id))
            && same(field(s, "stageOrdinal"), &Value::Unsigned(b.stage_ordinal))
            && same(field(s, "relations"), &texts(&b.relations))
            && same(field(s, "budget"), &numbers(&b.budget))
            && same(field(domain, "keys"), &keys))
        {
            return mismatch(&format!("stage {}", b.expected_stage_id));
        }
    }
    Ok(())
}

impl<'t> Ts2Participant<'t> {
    /// A participant over `table` (T2O), the session's immutable `context`
    /// (D4's) and the built `request` (C4's), whose sealed snapshot bytes
    /// `source` supplies. The two must describe one session.
    pub fn new(
        table: &'t Table,
        context: DispatchContext,
        request: Ts2Request,
        source: Box<dyn SnapshotSource>,
    ) -> Result<Self, Ts2Refusal> {
        Self::from_sender(table, context, Ts2Sender::new(request), source)
    }

    /// Consume the same fresh sender D4 compared with the independently
    /// admitted descriptor values; retain all ordinary participant joins.
    pub fn from_sender(
        table: &'t Table,
        context: DispatchContext,
        sender: Ts2Sender,
        source: Box<dyn SnapshotSource>,
    ) -> Result<Self, Ts2Refusal> {
        if !sender.is_pristine()
            || sender
                .next_slot()
                .is_none_or(|slot| slot.frame != super::send::SlotFrame::Hello)
        {
            return Err(Ts2Refusal::Context(
                "participant requires a fresh sender".into(),
            ));
        }
        joins(&context, sender.request()).map_err(Ts2Refusal::Context)?;
        let receiver = Ts2Receiver::new(table, context)?;
        let mut participant = Self {
            receiver,
            sender,
            source,
            accumulator: FrameAccumulator::new(Profile::Ts2, TS2_FRAME_MAX_DEPTH, None),
            pending: Vec::new(),
            at: 0,
            closed: false,
            cancel_requested: false,
            pending_frame: None,
            cancel_progress: CancelProgress::default(),
            protocol_fault: false,
            host_fault: false,
            output: None,
            minted: false,
            spool: Spool::default(),
            boundaries: Vec::new(),
        };
        participant.pump();
        Ok(participant)
    }

    /// The user interrupt (LD-D2B-7): one Cancel, the exact echo of what
    /// was sent, written once any frame in flight is whole. False when none
    /// can be sent: before the Hello slot, after a terminal, or once ended.
    pub fn cancel(&mut self) -> bool {
        let lawful = !self.closed
            && !self.cancel_requested
            && !self.faulted()
            && self.sender.cancel_payload().is_some()
            && self.receiver.admits(&HostFrame::Cancel {
                execution_id: None,
                analysis_ordinal: None,
            });
        if lawful {
            self.cancel_requested = true;
            self.pump();
        }
        lawful
    }

    /// The table's phase.
    pub fn phase(&self) -> &str {
        self.receiver.phase()
    }

    fn faulted(&self) -> bool {
        self.protocol_fault || self.host_fault
    }

    /// Queue the next frame when none is in flight and the table admits it.
    fn pump(&mut self) {
        if self.closed || self.faulted() || self.at < self.pending.len() {
            return;
        }
        let sent = if self.cancel_requested {
            let cancel = HostFrame::Cancel {
                execution_id: None,
                analysis_ordinal: None,
            };
            if self.sender.cancelled() || !self.receiver.admits(&cancel) {
                // Sent already, or a terminal arrived first: none is owed.
                self.cancel_requested = false;
                return;
            }
            self.sender.cancel()
        } else {
            match self.sender.next_slot() {
                Some(slot) if self.receiver.admits(&slot_frame(slot.frame)) => {
                    self.sender.send_next(self.source.as_mut())
                }
                _ => return,
            }
        };
        match sent {
            Ok(sent) => match self.receiver.sent(sent.frame.clone()) {
                Ok(_) => {
                    // The snapshot transfer starts with its manifest.
                    if sent.frame == HostFrame::SnapshotManifest {
                        self.boundaries.push(Boundary::TransferStarted);
                    }
                    self.pending_frame = Some(sent.frame);
                    self.pending = sent.bytes;
                    self.at = 0;
                }
                // The gate admitted it, so the table cannot refuse it.
                Err(_) => self.host_fault = true,
            },
            Err(_) => self.host_fault = true,
        }
    }

    fn status(&self) -> ParticipantStatus {
        if self.host_fault {
            return ParticipantStatus::HostFault;
        }
        if self.protocol_fault {
            return ParticipantStatus::Fault;
        }
        match self.receiver.phase() {
            "FAULT" => ParticipantStatus::Fault,
            "DONE" => ParticipantStatus::Done,
            _ => match self.receiver.terminal_kind().map(terminal_of) {
                Some(Some(kind)) => ParticipantStatus::Terminal(kind),
                Some(None) => ParticipantStatus::Fault,
                None => ParticipantStatus::Running,
            },
        }
    }

    fn report(&mut self, progress: Vec<Progress>, admitted: u64, eof: bool) -> ParticipantStep {
        ParticipantStep {
            status: self.status(),
            progress,
            admitted_payload_bytes: admitted,
            eof,
            boundaries: std::mem::take(&mut self.boundaries),
            cancel: std::mem::take(&mut self.cancel_progress),
        }
    }

    /// The verified terminal's output, minted once when its frame is
    /// admitted: the receiver recomputed every commitment it carries.
    fn mint(&mut self) {
        if !self.minted
            && let Some(Some(kind)) = self.receiver.terminal_kind().map(terminal_of)
        {
            self.minted = true;
            self.output = Some(TerminalOutput::mint(kind, std::mem::take(&mut self.spool)));
        }
    }
}

fn slot_frame(frame: super::send::SlotFrame) -> HostFrame {
    use super::send::SlotFrame as F;
    match frame {
        F::Hello => HostFrame::Hello,
        F::OpenUniverse => HostFrame::OpenUniverse,
        F::SnapshotManifest => HostFrame::SnapshotManifest,
        F::SnapshotFileChunk => HostFrame::SnapshotFileChunk,
        F::SnapshotSeal => HostFrame::SnapshotSeal,
        F::Analyze => HostFrame::Analyze,
    }
}

/// T2O's `terminal` values (its rows T2-10, T2-14 to T2-17 and T2-19).
fn terminal_of(kind: &str) -> Option<TerminalKind> {
    match kind {
        "complete" => Some(TerminalKind::Complete),
        "unavailable" => Some(TerminalKind::Unavailable),
        "budget-exhausted" => Some(TerminalKind::BudgetExhausted),
        "cancelled" => Some(TerminalKind::Cancelled),
        _ => None,
    }
}

impl Participant for Ts2Participant<'_> {
    fn protocol_waits(&self) -> ProtocolWaits {
        ProtocolWaits::TS2
    }
    fn protocol(&self) -> Protocol {
        Protocol::Ts2
    }
    fn wants_write(&self) -> bool {
        !self.closed && !self.faulted() && self.at < self.pending.len()
    }
    fn readable(&mut self, fd1: &mut dyn Read) -> ParticipantStep {
        let mut buf = vec![0u8; READ_QUANTUM];
        match fd1.read(&mut buf) {
            Ok(0) => {
                if !self.accumulator.at_boundary() {
                    // EOF inside a frame: truncation.
                    self.protocol_fault = true;
                }
                self.report(Vec::new(), 0, true)
            }
            Ok(n) => {
                let pushed = self.accumulator.push(&buf[..n]);
                let mut progress = Vec::new();
                let mut admitted = 0u64;
                for frame in pushed.frames {
                    if self.faulted() {
                        break;
                    }
                    let bytes = frame.payload().len() as u64;
                    // A spooled frame's received payload is a candidate the
                    // spool keeps (item 20), once the frame is admitted.
                    let candidate = match field(members(frame.value()), "frameType") {
                        Some(Value::Text(kind)) => SPOOLED.contains(&kind.as_str()),
                        _ => false,
                    }
                    .then(|| frame.payload().to_vec());
                    match self.receiver.receive(frame) {
                        Ok(a) => {
                            admitted = admitted.saturating_add(bytes);
                            if let Some(c) = candidate {
                                self.spool.push(c);
                            }
                            match a.payload {
                                P::SnapshotAccepted(_) => {
                                    progress.push(Progress::SnapshotAcknowledged);
                                    self.boundaries.push(Boundary::TransferEnded);
                                }
                                P::NativeContextVerified(_) | P::Unavailable0(_) => {
                                    // The context's verification, or the
                                    // pre-Analyze Unavailable (M3-L r1:400).
                                    self.boundaries.push(Boundary::ContextVerified);
                                }
                                P::FactBatch0(_) | P::FactBatch1(_) => {
                                    progress.push(Progress::FactBatch)
                                }
                                P::Coverage(_) => {
                                    progress.push(Progress::Coverage);
                                    // The table moved to the next stage.
                                    if self.receiver.phase() == "ANALYZING" {
                                        progress.push(Progress::StageChanged);
                                    }
                                }
                                _ => {}
                            }
                            self.mint();
                        }
                        Err(_) => self.protocol_fault = true,
                    }
                }
                if pushed.refusal.is_some() {
                    self.protocol_fault = true;
                }
                self.pump();
                self.report(progress, admitted, false)
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
                self.host_fault = true;
                self.report(Vec::new(), 0, false)
            }
        }
    }
    fn writable(&mut self, fd0: &mut dyn Write) -> ParticipantStep {
        if self.wants_write() {
            match fd0.write(&self.pending[self.at..]) {
                // A pending frame that writes no byte is a failure, not
                // progress: the pipe cannot take it (std's `WriteZero`).
                Ok(0) => self.host_fault = true,
                Ok(n) => {
                    self.at += n;
                    if self.at == self.pending.len() {
                        let was_cancel =
                            matches!(self.pending_frame.take(), Some(HostFrame::Cancel { .. }));
                        self.pending.clear();
                        self.at = 0;
                        if was_cancel {
                            self.closed = true;
                            self.cancel_progress = CancelProgress {
                                written: true,
                                request_closed: true,
                            };
                        } else {
                            self.pump();
                        }
                    }
                }
                Err(e)
                    if matches!(
                        e.kind(),
                        io::ErrorKind::WouldBlock | io::ErrorKind::Interrupted
                    ) => {}
                Err(_) => self.host_fault = true,
            }
        }
        self.report(Vec::new(), 0, false)
    }
    fn process(&mut self, event: ProcessEvent) -> ParticipantStep {
        // T2-19 enters WAIT_EOF directly: cancellation's terminal law
        // owes only EOF, unlike T2-20's normal zero-exit transition. D3
        // still observes and records this successful death; it does not
        // manufacture an extra protocol transition after Cancelled.
        if event == ProcessEvent::ZeroExit
            && self.receiver.phase() == "WAIT_EOF"
            && self.receiver.terminal_kind() == Some("cancelled")
        {
            return self.report(Vec::new(), 0, false);
        }
        if !self.faulted() && self.receiver.process(event).is_err() {
            self.protocol_fault = true;
        }
        self.report(Vec::new(), 0, false)
    }
    fn close_input(&mut self) {
        self.closed = true;
        self.pending.clear();
        self.pending_frame = None;
        self.at = 0;
    }
    fn user_cancel(&mut self) -> bool {
        self.cancel()
    }
    fn abandon_input(&mut self) {
        self.close_input();
        self.cancel_progress = CancelProgress::default();
    }
    fn take_terminal_output(&mut self) -> Option<TerminalOutput> {
        self.output.take()
    }
    fn discard(&mut self) {
        self.spool = Spool::default();
        self.output = None;
    }
}
