from pathlib import Path
F=Path(__file__).parent;W=Path('/Users/sb/code/opensip-ai/opensip-d3b2-takeover');p=W/'crates/components/src/supervisor.rs';s=p.read_text()
def change(a,b):
 global s
 assert s.count(a)==1,(a[:100],s.count(a));s=s.replace(a,b)
# Reviewed core remains in existing product path; no file/module ownership changes.
core=(F/'gate-core-preflight-r1/gate_core.rs').read_text();core=core[core.index('#[derive(Debug, PartialEq, Eq)]'):core.index('#[cfg(test)]')]
start=s.index('#[derive(Debug)]\nstruct GateState');end=s.index('impl TriggerGate {',start);s=s[:start]+core+'type GateState = GateCore<Trigger>;\n'+s[end:]
change('''state: Mutex::new(GateState {
                closed: false,
                pending: VecDeque::with_capacity(TRIGGER_CAPACITY),
                late: 0,
            }),''','''state: Mutex::new(GateCore::new(TRIGGER_CAPACITY)),''')
change('gate.late += 1;','gate.late = gate.late.saturating_add(1);')
change('''        if gate.pending.len() >= TRIGGER_CAPACITY {
            return false;
        }
        gate.pending.push_back(trigger);
        true''','''        gate.push(trigger)''')
change('''    fn take(&self) -> Option<Trigger> {
        self.lock().pending.pop_front()
    }''','''    fn take(&self) -> Option<GateMessage<Trigger>> {
        self.lock().take()
    }
    fn user_signal(&self) -> bool {
        self.lock().signal()
    }
    fn take_extra_signals(&self) -> u64 {
        self.lock().take_extra_signals()
    }''')
change('''        let mut gate = self.lock();
        gate.closed = true;
        let drained = gate.pending.len();
        gate.pending.clear();
        gate.late += drained as u64;
        drained''','''        self.lock().close()''')
change('''    pub fn host_fault(&self) -> bool {
        self.gate.admit(Trigger::HostFault)
    }''','''    pub fn host_fault(&self) -> bool {
        self.gate.admit(Trigger::HostFault)
    }
    /// Called by J's signal-watch thread, never an async signal handler.
    /// The first two signals have independent slots; later signals are
    /// counted without stamps. Only a closed gate refuses a signal.
    pub fn user_signal(&self) -> bool {
        self.gate.user_signal()
    }''')
change('''        for _ in 0..TRIGGER_CAPACITY {
            match self.gate.take() {
                Some(Trigger::HostFault) => self.trigger(Cause::HostFault),
                None => break,
            }
        }
        self.timers();''','''        for _ in 0..TRIGGER_CAPACITY + 2 {
            match self.gate.take() {
                Some(GateMessage::Queued(Trigger::HostFault)) => self.trigger(Cause::HostFault),
                Some(GateMessage::FirstSignal) => self.user_signal(false),
                Some(GateMessage::SecondSignal) => self.user_signal(true),
                None => break,
            }
        }
        self.extra_user_signals = self.extra_user_signals.saturating_add(self.gate.take_extra_signals());
        self.timers();''')
change('''    NormalExitGrace,
    ShutdownAck,''','''    NormalExitGrace,
    Stage1CancelGrace,
    ShutdownAck,''')
change('''            BoundedWait::Handshake => self.waits.handshake,''','''            BoundedWait::Stage1CancelGrace => self.protocol.map_or(Duration::ZERO, |p| p.stage1_cancel_grace),
            BoundedWait::Handshake => self.waits.handshake,''')
# Typed final evidence has no fabricated control outcome before admission.
idx=s.index('/// One appended event of the merged order')
s=s[:idx]+'''/// D3b-2's in-band cancellation leg, kept through settlement.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum InbandCancel { NotLawful, Queued, Written, Abandoned }
/// The control leg is queued logically before it is serialized by its
/// session. Written is reported only after the frame's final byte.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ControlCancel { Queued, Written, Refused, Failed, Abandoned }
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Stage1Evidence {
    pub inband: InbandCancel,
    pub control: Option<ControlCancel>,
}
#[derive(Debug, Clone, Copy)]
struct Stage1 {
    started: Instant,
    active: bool,
    evidence: Stage1Evidence,
}

'''+s[idx:]
change('''    CancelAttempted,
    Signalled''','''    CancelAttempted,
    InbandCancel(InbandCancel),
    ControlCancel(ControlCancel),
    CancelForced { trigger: opensip_operability::ForceTrigger, grace: Duration },
    Signalled''')
change('''    user_interrupted: bool,
    exit: ExitClass,''','''    user_interrupted: bool,
    extra_user_signals: u64,
    stage1: Option<Stage1Evidence>,
    exit: ExitClass,''')
change('''    pub fn exit(&self) -> ExitClass {''','''    pub fn stage1_evidence(&self) -> Option<Stage1Evidence> { self.stage1 }
    /// Signals after the first two which were consumed before settlement.
    pub fn extra_user_signals(&self) -> u64 { self.extra_user_signals }
    pub fn exit(&self) -> ExitClass {''')
change('''    ladder: Option<Ladder>,
    grace_expired: bool,''','''    ladder: Option<Ladder>,
    user_interrupted: bool,
    extra_user_signals: u64,
    stage1: Option<Stage1>,
    normal_end_signal: Option<Instant>,
    handshake_done: bool,
    cancel_control: Option<ControlCancel>,
    grace_expired: bool,''')
change('''            ladder: None,
            grace_expired: false,''','''            ladder: None,
            user_interrupted: false,
            extra_user_signals: 0,
            stage1: None,
            normal_end_signal: None,
            handshake_done: false,
            cancel_control: None,
            grace_expired: false,''')
change('''            user_interrupted: false,
            exit,''','''            user_interrupted: self.user_interrupted,
            extra_user_signals: self.extra_user_signals,
            stage1: self.stage1.map(|s| s.evidence),
            exit,''')
change('''    t1_done: bool,
    term_at:''','''    t1_done: bool,
    reason: CancelReason,
    term_at:''')
change('''                        t1_done: from_t2 || self.class == Class::Tool,
                        term_at:''','''                        t1_done: from_t2 || self.class == Class::Tool,
                        reason: if cause == Cause::Deadline { CancelReason::Deadline } else { CancelReason::SupervisorFault },
                        term_at:''')
change('''            let reason = if self.first_cause == Some(Cause::Deadline) {
                CancelReason::Deadline
            } else {
                CancelReason::SupervisorFault
            };
            // Sent once any pending frame completes; T-2 does not wait.
            self.deferred = Some(Deferred::Cancel(reason));
            self.send_deferred();''','''            // Logical admission happens once, even if an earlier control
            // frame is still in flight. T-2 never waits for its write.
            self.queue_control_cancel(ladder.reason);''')
# Only an active first-signal grace permits provider writes while stopping.
change('''            && self.state == State::Running
            && self.participant.as_ref().is_some_and(|p| p.wants_write())''','''            && (self.state == State::Running || self.stage1_active())
            && self.handshake_done
            && self.participant.as_ref().is_some_and(|p| p.wants_write())''')
change('''                    Control3Root::SelectAck { .. } if self.state == State::Handshaking => {
                        let now = Instant::now();
                        self.state = State::Running;
                        self.absence.progress(now);
                        self.next_health = Some(now + self.waits.health_ping_interval);
                        self.append(SupervisionEvent::Running);
                    }''','''                    Control3Root::SelectAck { .. } => {
                        self.handshake_done = true;
                        if self.state == State::Handshaking {
                            let now = Instant::now();
                            self.state = State::Running;
                            self.absence.progress(now);
                            self.next_health = Some(now + self.waits.health_ping_interval);
                            self.append(SupervisionEvent::Running);
                        }
                    }''')
change('''                        if let Some(select) = self.host_message(host_select) {''','''                        if self.ladder.is_none() && let Some(select) = self.host_message(host_select) {''')
# Stop grace before ordinary timers. Wall/liveness faults on existing paths
# may escalate via trigger_from; they never emit CancelForced.
change('''        let now = Instant::now();
        let Some(spawned) = self.spawned_at else {''','''        let now = Instant::now();
        if let Some(stage1) = self.stage1.filter(|s| s.active)
            && let Some(protocol) = self.protocol
            && now >= stage1.started + protocol.stage1_cancel_grace {
            self.append(SupervisionEvent::WaitExpired(BoundedWait::Stage1CancelGrace));
            self.force_user_stage2(Some(opensip_operability::ForceTrigger::GraceExpired), CancelReason::User);
        }
        let Some(spawned) = self.spawned_at else {''')
change('''        all.extend(self.clean_at.map(|at| at + self.waits.reap_ceiling));''','''        if let Some(stage1) = self.stage1.filter(|s| s.active) && let Some(protocol) = self.protocol {
            all.push(stage1.started + protocol.stage1_cancel_grace);
        }
        all.extend(self.clean_at.map(|at| at + self.waits.reap_ceiling));''')
change('''    fn apply_step(&mut self, step: ParticipantStep) {
        for progress''','''    fn apply_step(&mut self, step: ParticipantStep) {
        if self.stage1_active() {
            if step.cancel.written && self.stage1.is_some_and(|s| s.evidence.inband == InbandCancel::Queued) {
                self.inband_cancel(InbandCancel::Written);
            }
            if step.cancel.request_closed && self.stage1.is_some_and(|s| s.evidence.inband == InbandCancel::Written) {
                self.ends.fd0 = None;
                self.queue_control_cancel(CancelReason::User);
            }
        }
        for progress''')
change('''        if self.first_cause.is_some() {
            return;
        }
        self.terminal_at = Some(Instant::now());''','''        if self.stage1_active() {
            if kind != TerminalKind::Cancelled { self.trigger(Cause::ProviderProtocol); }
            return;
        }
        if self.first_cause.is_some() {
            return;
        }
        self.terminal_at = Some(Instant::now());''')
change('''        if self.first_cause.is_none() && ended && self.death_appended {''','''        if self.stage1_active() && self.terminal == Some(TerminalKind::Cancelled)
            && self.participant_status == ParticipantStatus::Done && self.death_appended {
            if let Some(stage1) = &mut self.stage1 { stage1.active = false; }
            self.clean_at = Some(Instant::now());
            self.state = State::Reaping;
        }
        if self.first_cause.is_none() && ended && self.death_appended {''')
change('''            Some(_) => {}
        }
    }

    /// Teardown, reap''','''            Some(_) => {}
        }
        if self.stage1_active() && cause != Cause::UserCancel {
            let reason = if cause == Cause::Deadline { CancelReason::Deadline } else { CancelReason::SupervisorFault };
            self.force_user_stage2(None, reason);
        }
    }

    /// Teardown, reap''')
# Add main cancellation methods before trigger; caller controls ordering.
idx=s.index('    /// Append a teardown trigger')
s=s[:idx]+'''    fn stage1_active(&self) -> bool { self.stage1.is_some_and(|s| s.active) }
    fn inband_cancel(&mut self, outcome: InbandCancel) {
        if let Some(stage1) = &mut self.stage1 { stage1.evidence.inband = outcome; }
        self.append(SupervisionEvent::InbandCancel(outcome));
    }
    fn control_cancel(&mut self, outcome: ControlCancel) {
        self.cancel_control = Some(outcome);
        if let Some(stage1) = &mut self.stage1 { stage1.evidence.control = Some(outcome); }
        self.append(SupervisionEvent::ControlCancel(outcome));
    }
    fn queue_control_cancel(&mut self, reason: CancelReason) {
        if self.class == Class::Tool || self.cancel_control.is_some() { return; }
        self.control_cancel(ControlCancel::Queued);
        self.deferred = Some(Deferred::Cancel(reason));
        if self.ends.fd3.is_none() {
            self.deferred = None;
            self.control_cancel(ControlCancel::Abandoned);
            if self.stage1_active() { self.trigger(Cause::HostFault); }
        } else { self.send_deferred(); }
    }
    fn user_signal(&mut self, second: bool) {
        self.user_interrupted = true;
        if second {
            self.append(SupervisionEvent::Trigger(Cause::UserCancel));
            if self.stage1_active() || self.normal_end_signal.is_some() {
                self.force_user_stage2(Some(opensip_operability::ForceTrigger::SecondSignal), CancelReason::User);
            }
            return;
        }
        if self.first_cause.is_some() {
            self.trigger(Cause::UserCancel);
            return;
        }
        // During normal end the first signal adds no protocol message.
        if self.terminal.is_some() {
            self.normal_end_signal = Some(Instant::now());
            if !self.later_causes.contains(&Cause::UserCancel) { self.later_causes.push(Cause::UserCancel); }
            self.append(SupervisionEvent::Trigger(Cause::UserCancel));
            return;
        }
        if self.class == Class::Tool {
            self.trigger_from(Cause::UserCancel, true);
            self.ladder_step();
            return;
        }
        let now = Instant::now();
        self.first_cause = Some(Cause::UserCancel);
        self.teardown_from = Some(now);
        self.state = State::Stopping(Cause::UserCancel);
        self.stage1 = Some(Stage1 { started: now, active: true,
            evidence: Stage1Evidence { inband: InbandCancel::NotLawful, control: None } });
        self.append(SupervisionEvent::Trigger(Cause::UserCancel));
        self.append(SupervisionEvent::TeardownStarted(Cause::UserCancel));
        if self.participant.as_mut().is_some_and(|p| p.user_cancel()) {
            self.inband_cancel(InbandCancel::Queued);
        } else {
            self.inband_cancel(InbandCancel::NotLawful);
            self.queue_control_cancel(CancelReason::User);
        }
    }
    fn force_user_stage2(&mut self, forced: Option<opensip_operability::ForceTrigger>, reason: CancelReason) {
        if self.ladder.is_some() { return; }
        let started = self.stage1.map(|s| s.started).or(self.normal_end_signal);
        if let Some(stage1) = &mut self.stage1 { stage1.active = false; }
        self.normal_end_signal = None;
        if let Some(participant) = &mut self.participant { participant.abandon_input(); }
        self.ends.fd0 = None;
        if self.stage1.is_some_and(|s| s.evidence.inband == InbandCancel::Queued) {
            self.inband_cancel(InbandCancel::Abandoned);
        }
        // This is the last point at which a control cancellation can be
        // logically queued. A previously queued announcement may finish.
        self.queue_control_cancel(reason);
        if let (Some(trigger), Some(at)) = (forced, started) {
            let grace = Instant::now().saturating_duration_since(at);
            self.append(SupervisionEvent::CancelForced { trigger, grace });
            self.fact(records::RecordFact::CancelForced { trigger, grace });
        }
        self.first_cause.get_or_insert(Cause::UserCancel);
        self.state = State::Stopping(self.first_cause.unwrap());
        self.ladder = Some(Ladder { t1_done: true, reason, term_at: None, kill_at: None });
        self.ladder_step();
    }

'''+s[idx:]
# Control send/write evidence and fact are tied to actual full writes.
change('''            self.control_out.written = Some(records::RecordFact::CancelSent {
                control_reason:''','''            self.control_out.written = Some(records::RecordFact::CancelSent {
                inband: self.stage1.is_some_and(|s| s.evidence.inband == InbandCancel::Written),
                control_reason:''')
change('''        if deferred == Deferred::Shutdown {''','''        if matches!(deferred, Deferred::Cancel(_)) && !sent {
            self.control_cancel(ControlCancel::Refused);
            if self.stage1_active() { self.trigger(Cause::HostFault); }
        }
        if deferred == Deferred::Shutdown {''')
change('''                self.control_out = PendingWrite::default();
                self.ends.fd3 = None;
                return;''','''                let cancel_pending = self.cancel_control == Some(ControlCancel::Queued);
                self.control_out = PendingWrite::default();
                self.ends.fd3 = None;
                self.deferred = None;
                if cancel_pending { self.control_cancel(ControlCancel::Failed); }
                if self.stage1_active() { self.trigger(Cause::HostFault); }
                return;''')
change('''                self.fact(fact);
            }
            if self.close_fd3_after_write {''','''                if matches!(fact, records::RecordFact::CancelSent { .. }) {
                    self.control_cancel(ControlCancel::Written);
                }
                self.fact(fact);
            }
            if self.close_fd3_after_write {''')
p.write_text(s)
# Correct the fact's shape and its scope mappings without registry changes.
p=W/'crates/components/src/supervisor_records.rs';s=p.read_text();s=s.replace('''    /// `supervision.cancel.sent`: T-1's in-band cancel, written.
    CancelSent { control_reason: ControlCancelReason },''','''    /// A fully written control cancellation; `inband` says whether the
    /// provider Cancel completed before it. Ordinary fault T-1 is false.
    CancelSent { inband: bool, control_reason: ControlCancelReason },
    CancelForced { trigger: opensip_operability::ForceTrigger, grace: Duration },''');s=s.replace('''            Self::CancelSent { .. } => opensip_operability::SupervisionCancelSent::NAME,''','''            Self::CancelSent { .. } => opensip_operability::SupervisionCancelSent::NAME,
            Self::CancelForced { .. } => opensip_operability::SupervisionCancelForced::NAME,''');s=s.replace('''            Self::CancelSent { .. } => &["inband", "control_reason"],''','''            Self::CancelSent { .. } => &["inband", "control_reason"],
            Self::CancelForced { .. } => &["trigger", "grace"],''');s=s.replace('''    /// minted ones (`role`, `universe`, `pid`). `inband` is always true for
    /// D3a's T-1 cancel, and `rss_unit` is `bytes` on macOS.''','''    /// minted ones (`role`, `universe`, `pid`). `inband` is carried by the
    /// cancel fact, and `rss_unit` is `bytes` on macOS.''');s=s.replace('''        Wait::NormalExitGrace => BoundedWait::NormalExitGrace,''','''        Wait::NormalExitGrace => BoundedWait::NormalExitGrace,
        Wait::Stage1CancelGrace => BoundedWait::Stage1CancelGrace,''');p.write_text(s)
# Existing constructors assert the previously missing false field explicitly.
p=W/'crates/components/src/supervisor_tests.rs';s=p.read_text();import re
s=re.sub(r'(RecordFact::CancelSent \{\n)(\s*)(control_reason:)',r'\1\2inband: false,\n\2\3',s)
p.write_text(s)
print('Root cancellation draft implemented; production admission gate retained')
