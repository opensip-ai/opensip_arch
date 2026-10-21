//! The Rust3 D3a participant: one nonblocking pipe operation per step.
//! Table gates precede source disclosure; pending frames finish before Cancel.
//! Original admitted response buffers move only after DONE, never copied
//! before admission or published as facts by this codec.
use super::super::super::{
    FrameAccumulator, ProcessEvent,
    cbor::Profile,
    table::{Protocol, Table},
};
use super::super::{RUST3_FRAME_MAX_DEPTH, Rust3HostFrame, Rust3Receiver, Rust3Refusal};
use super::{
    request::Request,
    sender::{Sender, Source, host_frame},
};
use crate::supervisor::{
    Boundary, CancelProgress, Participant, ParticipantStatus, ParticipantStep, Progress,
    ProtocolWaits, Spool, TerminalKind, TerminalOutput,
};
use opensip_contracts::generated::protocol::Rust3ProviderFrameV3Payload as P;
use std::{
    io::{self, Read, Write},
    time::Duration,
};
const READ_QUANTUM: usize = 65_536;

pub struct Rust3Participant<'t> {
    receiver: Rust3Receiver<'t>,
    sender: Sender,
    source: Box<dyn Source>,
    accumulator: FrameAccumulator,
    remaining_frames: u64,
    pending: Vec<u8>,
    at: usize,
    pending_frame: Option<Rust3HostFrame>,
    closed: bool,
    cancel_requested: bool,
    cancel_progress: CancelProgress,
    protocol_fault: bool,
    host_fault: bool,
    discarded: bool,
    minted: bool,
    output: Option<TerminalOutput>,
    boundaries: Vec<Boundary>,
    waits: ProtocolWaits,
}
impl<'t> Rust3Participant<'t> {
    pub fn new(
        table: &'t Table,
        request: Request,
        source: Box<dyn Source>,
    ) -> Result<Self, Rust3Refusal> {
        // The receiver binds the selected scope before any source access.
        // Never strip signed selection tokens to force a historical branch.
        let receiver = Rust3Receiver::new(table, request.context.clone())?;
        let get = |key| {
            request
                .policy
                .limit(key)
                .map_err(|e| Rust3Refusal::Context(format!("{e:?}")))
        };
        let frames = get("maxResponseFrames")?;
        let payload = get("maxResponsePayloadBytesTotal")?;
        let waits = ProtocolWaits {
            stage1_cancel_grace: Duration::from_millis(get("cancellationGraceMilliseconds")?),
            normal_exit_grace: Duration::from_millis(get("normalExitGraceMilliseconds")?),
        };
        let sender = Sender::new(request)
            .map_err(|e| Rust3Refusal::Context(format!("host sender: {e:?}")))?;
        let mut p = Self {
            receiver,
            sender,
            source,
            accumulator: FrameAccumulator::new(
                Profile::Rust3,
                RUST3_FRAME_MAX_DEPTH,
                Some(payload),
            ),
            remaining_frames: frames,
            pending: Vec::new(),
            at: 0,
            pending_frame: None,
            closed: false,
            cancel_requested: false,
            cancel_progress: CancelProgress::default(),
            protocol_fault: false,
            host_fault: false,
            discarded: false,
            minted: false,
            output: None,
            boundaries: Vec::new(),
            waits,
        };
        p.pump();
        Ok(p)
    }
    pub fn phase(&self) -> &str {
        self.receiver.phase()
    }
    fn faulted(&self) -> bool {
        self.host_fault || self.protocol_fault
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
            _ => match self.receiver.terminal_kind() {
                Some(kind) => {
                    terminal_of(kind).map_or(ParticipantStatus::Fault, ParticipantStatus::Terminal)
                }
                None => ParticipantStatus::Running,
            },
        }
    }
    fn report(&mut self, progress: Vec<Progress>, bytes: u64, eof: bool) -> ParticipantStep {
        if self.faulted() || self.receiver.phase() == "FAULT" {
            self.output = None;
            self.receiver.discard_candidate_spool();
            self.pending.clear();
            self.pending_frame = None;
            self.at = 0;
        }
        ParticipantStep {
            status: self.status(),
            progress,
            admitted_payload_bytes: bytes,
            eof,
            boundaries: std::mem::take(&mut self.boundaries),
            cancel: std::mem::take(&mut self.cancel_progress),
        }
    }
    pub fn cancel(&mut self) -> bool {
        if self.closed
            || self.faulted()
            || self.discarded
            || self.cancel_requested
            || self.sender.cancel_payload().is_none()
            || !self.receiver.admits(&Rust3HostFrame::Cancel {
                execution_id: None,
                analysis_ordinal: None,
            })
        {
            return false;
        }
        self.cancel_requested = true;
        self.pump();
        true
    }
    fn pump(&mut self) {
        if self.closed || self.faulted() || self.discarded {
            return;
        }
        let sent = if self.cancel_requested {
            if self.sender.cancelled()
                || !self.receiver.admits(&Rust3HostFrame::Cancel {
                    execution_id: None,
                    analysis_ordinal: None,
                })
            {
                self.cancel_requested = false;
                return;
            }
            self.sender.cancel()
        } else {
            match self.sender.next_slot() {
                Some(slot) if self.receiver.admits(&host_frame(slot.frame)) => {
                    self.sender.send_next(self.source.as_mut())
                }
                _ => return,
            }
        };
        match sent {
            Ok(sent) => {
                if self.receiver.sent(sent.frame.clone()).is_err() {
                    self.host_fault = true;
                    return;
                }
                if sent.frame == Rust3HostFrame::SnapshotManifest {
                    self.boundaries.push(Boundary::TransferStarted);
                }
                self.pending_frame = Some(sent.frame);
                self.pending = sent.bytes;
                self.at = 0;
            }
            Err(_) => self.host_fault = true,
        }
    }
    fn mint(&mut self) {
        if self.minted || self.discarded || self.faulted() || self.receiver.phase() != "DONE" {
            return;
        }
        let Some(kind) = self.receiver.terminal_kind().and_then(terminal_of) else {
            return;
        };
        let mut spool = Spool::default();
        if kind != TerminalKind::Cancelled {
            let Some(frames) = self.receiver.take_candidate_spool() else {
                self.host_fault = true;
                return;
            };
            for bytes in frames {
                spool.push(bytes);
            }
        }
        self.minted = true;
        self.output = Some(TerminalOutput::mint(kind, spool));
    }
    fn received(&mut self, bytes: &[u8]) -> (Vec<Progress>, u64) {
        let mut at = 0;
        let mut admitted = 0_u64;
        let mut progress = Vec::new();
        while at < bytes.len() && !self.faulted() {
            if self.accumulator.at_boundary() {
                let Some(remaining) = self.remaining_frames.checked_sub(1) else {
                    self.protocol_fault = true;
                    break;
                };
                self.remaining_frames = remaining;
            }
            let n = self.accumulator.next_fragment_len().min(bytes.len() - at);
            if n == 0 {
                self.host_fault = true;
                break;
            }
            let pushed = self.accumulator.push(&bytes[at..at + n]);
            at += n;
            for frame in pushed.frames {
                let length = frame.payload().len() as u64;
                match self.receiver.receive(frame) {
                    Ok(admission) => {
                        let Some(next) = admitted.checked_add(length) else {
                            self.host_fault = true;
                            break;
                        };
                        admitted = next;
                        match admission.payload {
                            P::SnapshotAccepted(_) => {
                                progress.push(Progress::SnapshotAcknowledged);
                                self.boundaries.push(Boundary::TransferEnded);
                            }
                            P::NativeContextVerified(_) | P::Unavailable0(_) => {
                                self.boundaries.push(Boundary::ContextVerified)
                            }
                            P::FactBatch0(_) | P::FactBatch1(_) => {
                                progress.push(Progress::FactBatch)
                            }
                            P::CoverageV3(_) => {
                                progress.push(Progress::Coverage);
                                if self.receiver.phase() == "ANALYZING" {
                                    progress.push(Progress::StageChanged);
                                }
                            }
                            _ => {}
                        }
                    }
                    Err(_) => self.protocol_fault = true,
                }
            }
            if pushed.refusal.is_some() {
                self.protocol_fault = true;
            }
        }
        (progress, admitted)
    }
}
fn terminal_of(kind: &str) -> Option<TerminalKind> {
    match kind {
        "complete" => Some(TerminalKind::Complete),
        "unavailable" => Some(TerminalKind::Unavailable),
        "budget-exhausted" => Some(TerminalKind::BudgetExhausted),
        "cancelled" => Some(TerminalKind::Cancelled),
        _ => None,
    }
}
impl Participant for Rust3Participant<'_> {
    fn protocol_waits(&self) -> ProtocolWaits {
        self.waits
    }
    fn protocol(&self) -> Protocol {
        Protocol::Rust3
    }
    fn wants_write(&self) -> bool {
        !self.closed && !self.faulted() && !self.discarded && self.at < self.pending.len()
    }
    fn readable(&mut self, fd1: &mut dyn Read) -> ParticipantStep {
        if self.faulted() || self.discarded {
            return self.report(Vec::new(), 0, false);
        }
        let mut buf = vec![0; READ_QUANTUM];
        match fd1.read(&mut buf) {
            Ok(0) => {
                if self.accumulator.finish().is_err() {
                    self.protocol_fault = true;
                }
                self.report(Vec::new(), 0, true)
            }
            Ok(n) => {
                let (progress, admitted) = self.received(&buf[..n]);
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
                Ok(0) => self.host_fault = true,
                Ok(n) => {
                    if n > self.pending.len() - self.at {
                        self.host_fault = true;
                    } else {
                        self.at += n;
                        if self.at == self.pending.len() {
                            let cancel = matches!(
                                self.pending_frame.take(),
                                Some(Rust3HostFrame::Cancel { .. })
                            );
                            self.pending.clear();
                            self.at = 0;
                            if cancel {
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
        // The supervisor owns EOF/exit ordering: observed terminal EOF is
        // held until death, then ZeroExit and EOF are delivered in that order.
        if !self.faulted() && !self.discarded && self.receiver.process(event).is_err() {
            self.protocol_fault = true;
        }
        self.mint();
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
        self.output = None;
        self.discarded = true;
        self.close_input();
        self.receiver.discard_candidate_spool();
    }
}

#[cfg(test)]
#[path = "participant_tests.rs"]
mod tests;
