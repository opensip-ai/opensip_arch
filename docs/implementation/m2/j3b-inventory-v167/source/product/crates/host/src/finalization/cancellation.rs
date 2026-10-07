//! J3b's commit cancellation port; the pure J1 classifier stays in invocation.
use crate::invocation::{CancellationSource, OperationPoint, SignalEffect, SignalRecord};
use opensip_contracts::generated::evidence::Common4D9Signal as Signal;
use std::sync::Arc;

/// J3b's shared commit port wraps the existing J1 cancellation classifier.
/// It owns the sole token only from P3 to P4. The observer never gets a
/// session, gate reader or operational authority. Records are published only
/// after their arrival phase is known, outside the source and cause locks.
#[derive(Clone)]
pub(crate) struct CommitCancellationSource {
    state: Arc<std::sync::Mutex<CommitCancellationState>>,
    publish: Arc<dyn Fn(SignalRecord) + Send + Sync>,
}
struct CommitCancellationState {
    classifier: CancellationSource,
    point: OperationPoint,
    preparing: bool,
    token: Option<opensip_security::CancellationLatch>,
    pending: Vec<Signal>,
}
fn signal_to_security(signal: Signal) -> opensip_security::D9Signal {
    match signal {
        Signal::Sigint => opensip_security::D9Signal::Sigint,
        Signal::Sigterm => opensip_security::D9Signal::Sigterm,
        Signal::Sighup => opensip_security::D9Signal::Sighup,
    }
}
fn signal_from_security(signal: opensip_security::D9Signal) -> Signal {
    match signal {
        opensip_security::D9Signal::Sigint => Signal::Sigint,
        opensip_security::D9Signal::Sigterm => Signal::Sigterm,
        opensip_security::D9Signal::Sighup => Signal::Sighup,
    }
}
impl CommitCancellationState {
    fn flush_pending(&mut self) -> Vec<SignalRecord> {
        let pending = std::mem::take(&mut self.pending);
        pending
            .into_iter()
            .map(|signal| self.classifier.observe(signal, self.point).0)
            .collect()
    }
    fn first(&self) -> Option<Signal> {
        self.classifier
            .deciding()
            .map(|deciding| deciding.signal)
            .or_else(|| self.pending.first().copied())
    }
}
impl CommitCancellationSource {
    pub(crate) fn new(publish: impl Fn(SignalRecord) + Send + Sync + 'static) -> Self {
        Self {
            state: Arc::new(std::sync::Mutex::new(CommitCancellationState {
                classifier: CancellationSource::new(),
                point: OperationPoint::BeforeAttemptAdmission,
                preparing: false,
                token: None,
                pending: Vec::new(),
            })),
            publish: Arc::new(publish),
        }
    }
    fn records(&self, records: Vec<SignalRecord>) {
        for record in records {
            (self.publish)(record);
        }
    }
    /// The signal input's own thread calls this; return follows any latch.
    pub(crate) fn receive(&self, signal: opensip_security::D9Signal) -> SignalEffect {
        let signal_value = signal_from_security(signal);
        let (records, effect) = {
            let mut state = self
                .state
                .lock()
                .unwrap_or_else(std::sync::PoisonError::into_inner);
            let prior_signal = state.first().is_some();
            if state.preparing || !state.pending.is_empty() {
                state.pending.push(signal_value);
                (
                    Vec::new(),
                    if prior_signal {
                        SignalEffect::Force
                    } else {
                        SignalEffect::Cooperate
                    },
                )
            } else if let Some(token) = state.token.take() {
                match token.latch(signal) {
                    opensip_security::LatchOutcome::BeforeAdmission => {
                        state.point = OperationPoint::AttemptAdmitted
                    }
                    opensip_security::LatchOutcome::AfterAdmission => {
                        state.point = OperationPoint::FinalGateAdmitted
                    }
                    // Neither result discloses the state bits. The close's own
                    // sample at P4 resolves the label; no gate read substitutes.
                    opensip_security::LatchOutcome::AlreadyStopped
                    | opensip_security::LatchOutcome::OutsideWindow => {
                        state.pending.push(signal_value);
                        return if prior_signal {
                            SignalEffect::Force
                        } else {
                            SignalEffect::Latch
                        };
                    }
                }
                let point = state.point;
                let (record, effect) = state.classifier.observe(signal_value, point);
                (vec![record], effect)
            } else {
                let point = state.point;
                let (record, effect) = state.classifier.observe(signal_value, point);
                (vec![record], effect)
            }
        };
        self.records(records);
        effect
    }
}
impl crate::finalization::CancellationPort for CommitCancellationSource {
    fn observed(&mut self) -> Option<opensip_security::D9Signal> {
        let mut state = self
            .state
            .lock()
            .unwrap_or_else(std::sync::PoisonError::into_inner);
        let first = state.first().map(signal_to_security);
        if first.is_none() {
            state.preparing = true;
        }
        first
    }
    fn arm(&mut self, token: opensip_security::CancellationLatch) {
        let records = {
            let mut state = self
                .state
                .lock()
                .unwrap_or_else(std::sync::PoisonError::into_inner);
            state.preparing = false;
            state.point = OperationPoint::AttemptAdmitted;
            let first = state.first();
            let records = state.flush_pending();
            if let Some(signal) = first {
                let _ = token.latch(signal_to_security(signal));
            } else {
                state.token = Some(token);
            }
            records
        };
        self.records(records);
    }
    fn returned(&mut self, admitted_at_close: bool, enters_delivery: bool) {
        let records = {
            let mut state = self
                .state
                .lock()
                .unwrap_or_else(std::sync::PoisonError::into_inner);
            state.preparing = false;
            state.token = None;
            state.point = if enters_delivery {
                OperationPoint::CommittedUnlatched
            } else {
                OperationPoint::PublishReturned {
                    admitted: admitted_at_close,
                }
            };
            state.flush_pending()
        };
        self.records(records);
    }
    fn decide_output(&mut self) -> Option<opensip_security::D9Signal> {
        let (records, first) = {
            let mut state = self
                .state
                .lock()
                .unwrap_or_else(std::sync::PoisonError::into_inner);
            state.preparing = false;
            let records = state.flush_pending();
            let first = state.first().map(signal_to_security);
            state.point = OperationPoint::FinalOutput;
            (records, first)
        };
        self.records(records);
        first
    }
    fn settled(&mut self) {
        self.state
            .lock()
            .unwrap_or_else(std::sync::PoisonError::into_inner)
            .point = OperationPoint::Settled;
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::finalization::CancellationPort;
    use std::sync::Mutex;
    #[test]
    fn first_signal_is_kept_and_output_and_settlement_classify_later_signals() {
        let records = Arc::new(Mutex::new(Vec::new()));
        let out = records.clone();
        let mut source =
            CommitCancellationSource::new(move |record| out.lock().unwrap().push(record));
        assert_eq!(
            source.receive(opensip_security::D9Signal::Sigint),
            SignalEffect::Cooperate
        );
        assert_eq!(
            source.receive(opensip_security::D9Signal::Sigterm),
            SignalEffect::Force
        );
        assert_eq!(
            source.decide_output(),
            Some(opensip_security::D9Signal::Sigint)
        );
        assert_eq!(
            source.receive(opensip_security::D9Signal::Sighup),
            SignalEffect::Defer
        );
        source.settled();
        assert_eq!(
            source.receive(opensip_security::D9Signal::Sigterm),
            SignalEffect::Record
        );
        let records = records.lock().unwrap();
        assert_eq!(
            records.iter().map(|r| r.ordinal).collect::<Vec<_>>(),
            [1, 2, 3, 4]
        );
        assert_eq!(
            records.iter().map(|r| r.phase).collect::<Vec<_>>(),
            [
                crate::invocation::CancelPhase::A,
                crate::invocation::CancelPhase::A,
                crate::invocation::CancelPhase::O,
                crate::invocation::CancelPhase::E
            ]
        );
    }
    #[test]
    fn signal_after_publish_uses_close_sample_without_a_gate_reader() {
        for admitted in [false, true] {
            let records = Arc::new(Mutex::new(Vec::new()));
            let out = records.clone();
            let mut source =
                CommitCancellationSource::new(move |record| out.lock().unwrap().push(record));
            source.returned(admitted, false);
            assert_eq!(
                source.receive(opensip_security::D9Signal::Sigint),
                SignalEffect::Latch
            );
            assert_eq!(
                source.decide_output(),
                Some(opensip_security::D9Signal::Sigint)
            );
            assert_eq!(
                records.lock().unwrap()[0].phase,
                if admitted {
                    crate::invocation::CancelPhase::C
                } else {
                    crate::invocation::CancelPhase::B
                }
            );
        }
    }
    #[test]
    fn unlatched_commit_signal_is_d_and_never_attempts_a_latch() {
        let records = Arc::new(Mutex::new(Vec::new()));
        let out = records.clone();
        let mut source =
            CommitCancellationSource::new(move |record| out.lock().unwrap().push(record));
        source.returned(true, true);
        assert_eq!(
            source.receive(opensip_security::D9Signal::Sigint),
            SignalEffect::CancelAtDecisionPoint
        );
        assert_eq!(
            records.lock().unwrap()[0].phase,
            crate::invocation::CancelPhase::D
        );
    }
    #[test]
    fn prepare_error_keeps_pending_signal_in_a_and_decides_it_once() {
        let records = Arc::new(Mutex::new(Vec::new()));
        let out = records.clone();
        let mut source =
            CommitCancellationSource::new(move |record| out.lock().unwrap().push(record));
        assert_eq!(source.observed(), None);
        assert_eq!(
            source.receive(opensip_security::D9Signal::Sigint),
            SignalEffect::Cooperate
        );
        assert!(records.lock().unwrap().is_empty());
        assert_eq!(
            source.receive(opensip_security::D9Signal::Sigterm),
            SignalEffect::Force
        );
        assert_eq!(
            source.decide_output(),
            Some(opensip_security::D9Signal::Sigint)
        );
        let records = records.lock().unwrap();
        assert_eq!(records.len(), 2);
        assert!(
            records
                .iter()
                .all(|r| r.phase == crate::invocation::CancelPhase::A)
        );
    }
}
