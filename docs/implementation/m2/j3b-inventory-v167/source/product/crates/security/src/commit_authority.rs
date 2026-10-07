//! Private final-admission primitive, not a CommitSession constructor. Callers
//! must first establish custody, grants, generation, writer/journal guards and
//! evaluator-owned replay evidence. None of those authorities is supplied here.
use std::sync::{
    Arc,
    atomic::{AtomicU8, Ordering},
};
const ADMITTED: u8 = 1;
const LATCHED: u8 = 2;
const WINDOW_OPEN: u8 = 4;
const WINDOW_CLOSED: u8 = 8;
/// Result of the operation's one-use cancellation latch (X3d r9 S10.2).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum LatchOutcome {
    OutsideWindow,
    AlreadyStopped,
    BeforeAdmission,
    AfterAdmission,
}
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(super) enum AttemptState {
    Preparing,
    Admitted,
    LatchedBeforeAdmission,
    AdmittedThenLatched,
}
fn state(bits: u8) -> AttemptState {
    match bits & (ADMITTED | LATCHED) {
        0 => AttemptState::Preparing,
        1 => AttemptState::Admitted,
        2 => AttemptState::LatchedBeforeAdmission,
        3 => AttemptState::AdmittedThenLatched,
        _ => unreachable!("private two-bit state"),
    }
}
struct FinalGate(AtomicU8);
impl FinalGate {
    fn new() -> Self {
        Self(AtomicU8::new(0))
    }
    fn admit(&self) -> Result<(), AttemptState> {
        let mut word = self.0.load(Ordering::SeqCst);
        loop {
            if word & (ADMITTED | LATCHED) != 0 {
                return Err(state(word));
            }
            #[cfg(test)]
            tests::before_exchange(&self.0);
            match self
                .0
                .compare_exchange(word, word | ADMITTED, Ordering::SeqCst, Ordering::SeqCst)
            {
                Ok(_) => return Ok(()),
                Err(current) => word = current,
            }
        }
    }
    fn open_window(&self) {
        self.0.fetch_or(WINDOW_OPEN, Ordering::SeqCst);
    }
    fn close_window(&self) -> AttemptState {
        state(self.0.fetch_or(WINDOW_CLOSED, Ordering::SeqCst))
    }
    // Called only inside the operation's first-cause record lock. This method
    // neither records a cause nor runs the post-release crash barrier.
    fn cancel(&self) -> LatchOutcome {
        let mut word = self.0.load(Ordering::SeqCst);
        loop {
            if word & WINDOW_OPEN == 0 || word & WINDOW_CLOSED != 0 {
                return LatchOutcome::OutsideWindow;
            }
            if word & LATCHED != 0 {
                return LatchOutcome::AlreadyStopped;
            }
            #[cfg(test)]
            tests::before_exchange(&self.0);
            match self
                .0
                .compare_exchange(word, word | LATCHED, Ordering::SeqCst, Ordering::SeqCst)
            {
                Ok(_) => {
                    return if word & ADMITTED == 0 {
                        LatchOutcome::BeforeAdmission
                    } else {
                        LatchOutcome::AfterAdmission
                    };
                }
                Err(current) => word = current,
            }
        }
    }
    // Law X9 r1 G4, with law X4 r8 S11.6 and LD8-4 (unit X4-F3):
    // `x4.gate.latch.after` follows the existing latch's section. A stop
    // transition's section takes the operation's stop-cause lock, makes the
    // one fetch-OR, records and reads, and releases the lock before it
    // returns, so the point follows that release; a bare latch's section is
    // the fetch-OR alone. The point is reached once per call, set or not.
    fn latch_within<R>(&self, section: impl FnOnce(Latching<'_>) -> R) -> R {
        let result = section(Latching(self));
        opensip_platform::crash_barrier!("x4.gate", "latch.after", step);
        result
    }
    /// The bare latch: the fetch-OR alone, with no record.
    fn latch(&self) -> AttemptState {
        self.latch_within(|latching| latching.fetch_latch().state)
    }
    fn observe(&self) -> AttemptState {
        state(self.0.load(Ordering::SeqCst))
    }
}
/// Law X4 r8 S11.6 (unit X4-F3): the existing latch's one word operation,
/// lent once to a latch's section (`FinalGate::latch_within`).
pub(super) struct Latching<'a>(&'a FinalGate);
impl Latching<'_> {
    /// The one fetch-OR of `LATCHED` (S11.2): it only adds the bit.
    pub(super) fn fetch_latch(self) -> Latched {
        let prior = self.0.0.fetch_or(LATCHED, Ordering::SeqCst);
        Latched {
            state: state(prior | LATCHED),
            first: prior & LATCHED == 0,
        }
    }
}
/// What one fetch-OR of `LATCHED` did: the decoded state after it, and
/// whether it set the bit (the word it read had `LATCHED` clear), which
/// makes it the operation's first stop.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(super) struct Latched {
    pub(super) state: AttemptState,
    pub(super) first: bool,
}
#[derive(Clone)]
pub(super) struct StopObserver(Arc<FinalGate>);
impl StopObserver {
    pub(super) fn open_window(&self) {
        self.0.open_window();
    }
    pub(super) fn close_window(&self) -> AttemptState {
        self.0.close_window()
    }
    pub(super) fn cancel(&self) -> LatchOutcome {
        self.0.cancel()
    }
    /// The bare latch (law X4 r8 S11.6): at the lease-free point, before
    /// the guard's entry, and in tests. From the guard's entry, every latch
    /// of the operation's gate is a stop transition (`latch_within`).
    pub(super) fn latch(&self) -> AttemptState {
        self.0.latch()
    }
    /// Law X4 r8 S11.6 (unit X4-F3): the existing latch inside a stop
    /// transition's critical section; `x4.gate.latch.after` follows the
    /// section's return, after its lock is released.
    pub(super) fn latch_within<R>(&self, section: impl FnOnce(Latching<'_>) -> R) -> R {
        self.0.latch_within(section)
    }
    pub(super) fn observe(&self) -> AttemptState {
        self.0.observe()
    }
}
/// Exact owned prepared value for one attempt. Intentionally no Clone, reset,
/// unbound admission constructor or public operational authority API.
pub(super) struct PreparedAttempt<T> {
    gate: Arc<FinalGate>,
    prepared: T,
}
pub(super) struct AdmissionPermit<T> {
    _gate: Arc<FinalGate>,
    prepared: T,
}
impl<T> PreparedAttempt<T> {
    pub(super) fn new(prepared: T) -> (Self, StopObserver) {
        let gate = Arc::new(FinalGate::new());
        let observer = StopObserver(gate.clone());
        (Self { gate, prepared }, observer)
    }
    pub(super) fn admit(self) -> Result<AdmissionPermit<T>, AttemptState> {
        self.gate.admit()?;
        Ok(AdmissionPermit {
            _gate: self.gate,
            prepared: self.prepared,
        })
    }
}
/// Law X4 r7 items 2 and 3 (unit X4a): an operation's one `FinalGate`,
/// created first at the lease-free point, before any prepared value exists.
/// Not Clone and never reset. Its only admission is `admit`, at item 3 step
/// 4, which binds the prepared value and mints the one `AdmissionPermit`; a
/// second call is refused by the gate's own state (no second permit).
pub(crate) struct OperationGate(Arc<FinalGate>);
impl OperationGate {
    pub(crate) fn new() -> (Self, StopObserver) {
        let gate = Arc::new(FinalGate::new());
        let observer = StopObserver(gate.clone());
        (Self(gate), observer)
    }
    /// The compare-exchange `0 -> 1`; `x4.gate.admit.after` (law X9 r1 G4)
    /// follows a successful exchange.
    pub(crate) fn admit<T>(&self, prepared: T) -> Result<AdmissionPermit<T>, (T, AttemptState)> {
        match self.0.admit() {
            Ok(()) => {
                opensip_platform::crash_barrier!("x4.gate", "admit.after", step);
                Ok(AdmissionPermit {
                    _gate: self.0.clone(),
                    prepared,
                })
            }
            Err(state) => Err((prepared, state)),
        }
    }
    pub(crate) fn observe(&self) -> AttemptState {
        self.0.observe()
    }
    /// Test seam (law X4 r8 W-12): the bare fetch-OR `2` on the gate itself.
    /// In production nothing latches through the gate: from the guard's
    /// entry every latch is a stop transition (S11.6).
    #[cfg(test)]
    pub(crate) fn latch(&self) -> AttemptState {
        self.0.latch()
    }
}
impl<T> AdmissionPermit<T> {
    /// Consume once for the already prepared attempt. A later latch records a
    /// stop and does not cancel/relabel this result. Result/durability/reconciliation
    /// remain owned by the effect executor; this gate never invents a receipt.
    pub(super) fn consume<R>(self, effect: impl FnOnce(T) -> R) -> R {
        effect(self.prepared)
    }
}
/// Prepared binding only. An owned evaluator replay is necessary but does not
/// establish live custody, journal/writer guards, generation or durable commit.
/// Law X3d r6 item 4 step 3.3 (unit X3d-1): `seal_under_append_lock` binds
/// the `SEAL` it is about to append to the caller's replay through this, and
/// the replay stays the caller's (`&replayed`), so it borrows it.
pub(crate) struct PreparedJournalSeal<'r> {
    record: crate::journal_store::JournalRecord,
    replayed: &'r opensip_evaluator::ReplayedRun,
}
impl<'r> PreparedJournalSeal<'r> {
    pub(crate) fn bind(
        record: crate::journal_store::JournalRecord,
        replayed: &'r opensip_evaluator::ReplayedRun,
    ) -> Result<Self, crate::journal_store::JournalError> {
        if record.seal_run_id()? != replayed.run_id() {
            return Err(crate::journal_store::JournalError::RunMismatch);
        }
        Ok(Self { record, replayed })
    }
    pub(crate) fn run_id(&self) -> &str {
        self.replayed.run_id()
    }
    pub(crate) fn journal_body(&self) -> &[u8] {
        self.record.canonical()
    }
    pub(crate) fn journal_body_sha256(&self) -> [u8; 32] {
        self.record.body_sha256()
    }
}

#[cfg(test)]
mod tests {
    // Gate-level only: deterministic interference with the real word, with
    // no guard or cause lock held. This seam does not exist in production.
    std::thread_local! {
        static EXCHANGES: std::cell::RefCell<(usize, std::collections::VecDeque<u8>)> = const {
            std::cell::RefCell::new((0, std::collections::VecDeque::new()))
        };
    }
    pub(super) fn before_exchange(word: &std::sync::atomic::AtomicU8) {
        EXCHANGES.with(|slot| {
            let mut probe = slot.borrow_mut();
            probe.0 += 1;
            if let Some(bits) = probe.1.pop_front() {
                word.fetch_or(bits, std::sync::atomic::Ordering::SeqCst);
            }
        });
    }
    fn interference(bits: &[u8]) {
        EXCHANGES.with(|slot| *slot.borrow_mut() = (0, bits.iter().copied().collect()));
    }
    fn exchanges() -> usize {
        EXCHANGES.with(|slot| slot.borrow().0)
    }
    use super::*;
    #[test]
    fn every_operation_on_every_four_bit_word_obeys_monotone_law() {
        for word in 0..16u8 {
            for operation in 0..6 {
                let gate = FinalGate(AtomicU8::new(word));
                let mut expected = word;
                match operation {
                    0 => {
                        let result = gate.admit();
                        if word & 3 == 0 {
                            expected |= ADMITTED;
                            assert_eq!(result, Ok(()));
                        } else {
                            assert_eq!(result, Err(state(word)));
                        }
                    }
                    1 => {
                        expected |= LATCHED;
                        assert_eq!(gate.latch(), state(expected));
                    }
                    2 => {
                        let expected_result =
                            if word & WINDOW_OPEN == 0 || word & WINDOW_CLOSED != 0 {
                                LatchOutcome::OutsideWindow
                            } else if word & LATCHED != 0 {
                                LatchOutcome::AlreadyStopped
                            } else {
                                expected |= LATCHED;
                                if word & ADMITTED == 0 {
                                    LatchOutcome::BeforeAdmission
                                } else {
                                    LatchOutcome::AfterAdmission
                                }
                            };
                        assert_eq!(gate.cancel(), expected_result);
                    }
                    3 => assert_eq!(gate.observe(), state(word)),
                    4 => {
                        gate.open_window();
                        expected |= WINDOW_OPEN;
                    }
                    5 => {
                        assert_eq!(gate.close_window(), state(word));
                        expected |= WINDOW_CLOSED;
                    }
                    _ => unreachable!(),
                }
                let actual = gate.0.load(Ordering::SeqCst);
                assert_eq!(actual, expected, "word {word}, operation {operation}");
                assert_eq!(actual & word, word);
                assert_eq!(gate.observe(), state(expected));
            }
        }
    }
    #[test]
    fn cancellation_window_precedes_state_and_close_samples_admission() {
        for window in [0, WINDOW_OPEN, WINDOW_CLOSED, WINDOW_OPEN | WINDOW_CLOSED] {
            for low in 0..4 {
                let gate = FinalGate(AtomicU8::new(window | low));
                assert_eq!(gate.observe(), state(low));
                let expected = if window != WINDOW_OPEN {
                    LatchOutcome::OutsideWindow
                } else if low & LATCHED != 0 {
                    LatchOutcome::AlreadyStopped
                } else if low & ADMITTED != 0 {
                    LatchOutcome::AfterAdmission
                } else {
                    LatchOutcome::BeforeAdmission
                };
                assert_eq!(gate.cancel(), expected);
                let current = gate.0.load(Ordering::SeqCst);
                assert_eq!(current & (WINDOW_OPEN | WINDOW_CLOSED), window);
                assert_eq!(gate.close_window(), state(current));
                assert_eq!(gate.cancel(), LatchOutcome::OutsideWindow);
                assert_eq!(gate.observe(), state(current));
            }
        }
    }
    #[test]
    fn admission_carries_every_window_combination_and_mints_once() {
        for window in [0, WINDOW_OPEN, WINDOW_CLOSED, WINDOW_OPEN | WINDOW_CLOSED] {
            let gate = FinalGate(AtomicU8::new(window));
            assert_eq!(gate.admit(), Ok(()));
            assert_eq!(gate.0.load(Ordering::SeqCst), window | ADMITTED);
            assert_eq!(gate.admit(), Err(AttemptState::Admitted));
            assert_eq!(gate.latch(), AttemptState::AdmittedThenLatched);
            assert_eq!(gate.0.load(Ordering::SeqCst), window | ADMITTED | LATCHED);
        }
    }
    #[test]
    fn window_interference_preserves_bits_and_bounds_real_exchanges() {
        for bits in [
            vec![WINDOW_OPEN],
            vec![WINDOW_CLOSED],
            vec![WINDOW_OPEN, WINDOW_CLOSED],
        ] {
            let gate = FinalGate::new();
            interference(&bits);
            assert_eq!(gate.admit(), Ok(()));
            assert_eq!(exchanges(), bits.len() + 1);
            assert!(exchanges() <= 3);
            assert_eq!(
                gate.0.load(Ordering::SeqCst),
                bits.into_iter().fold(ADMITTED, |word, bit| word | bit)
            );
        }
        let gate = FinalGate(AtomicU8::new(WINDOW_OPEN));
        interference(&[ADMITTED]);
        assert_eq!(gate.cancel(), LatchOutcome::AfterAdmission);
        assert_eq!(exchanges(), 2);
        assert_eq!(
            gate.0.load(Ordering::SeqCst),
            WINDOW_OPEN | ADMITTED | LATCHED
        );
        interference(&[]);
    }
    #[test]
    fn close_between_read_and_exchange_refuses_without_writing_a_stop() {
        for admission in [0, ADMITTED] {
            let gate = FinalGate(AtomicU8::new(WINDOW_OPEN | admission));
            interference(&[WINDOW_CLOSED]);
            assert_eq!(gate.cancel(), LatchOutcome::OutsideWindow);
            assert_eq!(exchanges(), 1);
            assert_eq!(
                gate.0.load(Ordering::SeqCst),
                WINDOW_OPEN | WINDOW_CLOSED | admission
            );
            assert_eq!(gate.close_window(), state(admission));
            let gate = FinalGate(AtomicU8::new(WINDOW_OPEN | admission));
            interference(&[]);
            assert_eq!(
                gate.cancel(),
                if admission == 0 {
                    LatchOutcome::BeforeAdmission
                } else {
                    LatchOutcome::AfterAdmission
                }
            );
            assert_eq!(gate.close_window(), state(admission | LATCHED));
            assert_eq!(gate.cancel(), LatchOutcome::OutsideWindow);
        }
        interference(&[]);
    }
    #[test]
    fn every_bounded_gate_trace_obeys_the_selected_two_bit_law() {
        // All 3^8 admit/latch/observe sequences. This is a direct exhaustive
        // contract-law check, not evidence of a native memory-model proof.
        for code in 0u32..3u32.pow(8) {
            let gate = FinalGate::new();
            let mut expected = 0;
            let mut actions = code;
            let mut successes = 0;
            for _ in 0..8 {
                match actions % 3 {
                    0 => {
                        let r = gate.admit();
                        if expected == 0 {
                            assert_eq!(r, Ok(()));
                            expected = 1;
                            successes += 1;
                        } else {
                            assert_eq!(r, Err(state(expected)));
                        }
                    }
                    1 => {
                        expected |= 2;
                        assert_eq!(gate.latch(), state(expected));
                    }
                    _ => assert_eq!(gate.observe(), state(expected)),
                }
                assert_eq!(gate.observe(), state(expected));
                actions /= 3;
            }
            assert!(successes <= 1);
        }
    }
    #[test]
    fn latch_before_admission_prevents_any_prepared_effect() {
        let (attempt, observer) = PreparedAttempt::new(String::from("prepared execution-A"));
        assert_eq!(observer.latch(), AttemptState::LatchedBeforeAdmission);
        assert!(matches!(
            attempt.admit(),
            Err(AttemptState::LatchedBeforeAdmission)
        ));
        assert_eq!(observer.observe(), AttemptState::LatchedBeforeAdmission);
    }
    #[test]
    fn late_latch_preserves_exact_owned_attempt_and_its_effect_result() {
        for result in [
            "committed receipt",
            "durability-undetermined",
            "failed-before-effect",
        ] {
            let (attempt, observer) = PreparedAttempt::new(("execution-A", vec![1, 2, 3]));
            let permit = attempt.admit().unwrap();
            assert_eq!(observer.latch(), AttemptState::AdmittedThenLatched);
            let observed = permit.consume(|prepared| {
                assert_eq!(prepared, ("execution-A", vec![1, 2, 3]));
                result
            });
            assert_eq!(observed, result);
            assert_eq!(observer.observe(), AttemptState::AdmittedThenLatched);
        }
    }
    #[test]
    fn dropped_permit_never_resets_or_reopens_admission() {
        let (attempt, observer) = PreparedAttempt::new(());
        let permit = attempt.admit().unwrap();
        drop(permit);
        assert_eq!(observer.observe(), AttemptState::Admitted);
        assert_eq!(observer.0.admit(), Err(AttemptState::Admitted));
        assert_eq!(observer.latch(), AttemptState::AdmittedThenLatched);
    }
    #[test]
    fn concurrent_stop_and_admission_never_lose_the_stop_or_duplicate_an_effect() {
        use std::sync::Barrier;
        for _ in 0..256 {
            let (attempt, observer) = PreparedAttempt::new("exact-prepared-value");
            let barrier = Barrier::new(2);
            std::thread::scope(|scope| {
                let stop = observer.clone();
                let barrier = &barrier;
                let handle = scope.spawn(move || {
                    barrier.wait();
                    stop.latch()
                });
                barrier.wait();
                let admitted = attempt.admit();
                let stop_state = handle.join().unwrap();
                match admitted {
                    Ok(permit) => {
                        assert_eq!(stop_state, AttemptState::AdmittedThenLatched);
                        assert_eq!(permit.consume(|value| value), "exact-prepared-value");
                        assert_eq!(observer.observe(), AttemptState::AdmittedThenLatched);
                    }
                    Err(s) => {
                        assert_eq!(s, AttemptState::LatchedBeforeAdmission);
                        assert_eq!(stop_state, s);
                        assert_eq!(observer.observe(), s);
                    }
                }
            });
        }
    }
}

#[cfg(test)]
mod seal_binding_tests {
    use super::*;
    use crate::journal_store::{JournalError, fixtures};
    #[test]
    fn seal_binds_real_replayed_evidence_after_original_arenas_are_dropped() {
        let replayed = fixtures::replay();
        let id = replayed.run_id().to_owned();
        let record = fixtures::record("SEAL", Some(&id));
        let expected = record.body_sha256();
        let bound =
            PreparedJournalSeal::bind(record, &replayed).unwrap_or_else(|e| panic!("{e:?}"));
        assert_eq!(bound.run_id(), id);
        assert_eq!(bound.journal_body_sha256(), expected);
        assert!(!bound.journal_body().is_empty());
        // The final gate keeps this exact prepared binding through a later stop.
        let (attempt, observer) = PreparedAttempt::new(bound);
        let permit = attempt.admit().unwrap();
        observer.latch();
        assert_eq!(permit.consume(|bound| bound.run_id().to_owned()), id);
    }
    #[test]
    fn seal_rejects_wrong_type_absence_fixture_and_mismatched_run() {
        for (kind, claimed, expected) in [
            ("REV", None, JournalError::SealType),
            ("SEAL", None, JournalError::SealRunRequired),
            (
                "SEAL",
                Some(format!("run3:{}", "0".repeat(64))),
                JournalError::FixtureRun,
            ),
            (
                "SEAL",
                Some(format!("run3:{}", "f".repeat(64))),
                JournalError::RunMismatch,
            ),
        ] {
            let replayed = fixtures::replay();
            let r =
                PreparedJournalSeal::bind(fixtures::record(kind, claimed.as_deref()), &replayed);
            let actual = match r {
                Err(e) => e,
                Ok(_) => panic!("invalid seal admitted"),
            };
            assert_eq!(actual, expected);
        }
    }
}
