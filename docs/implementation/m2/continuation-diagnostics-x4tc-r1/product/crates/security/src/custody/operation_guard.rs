// Law X4 r7 (unit X4a): the live security guards of one `ProjectOperation`.
// - Item 2: at the lease-free point the operation's one `FinalGate` and its
//   `FreshnessMonitor` are created first (`LeaseFree::create`), and X4T's
//   fenced admission runs as the monitor's first `read` (`first_read`).
// - Item 6: `OperationGuard` is built inside X2e's handoff, under the held
//   fence, from that gate, monitor and view, with the trust store's retained
//   handles. It is private, not Clone, never serialized, and lives only in a
//   `ProjectOperation`.
// - Items 2 and 5: one monitor history per operation behind one private
//   mutex, shared by the observer's ticks and every checkpoint; no read
//   resets it or the latch.
// - Item 5: one observer thread per guard, from the moment the guard moves
//   into `ProjectOperation` until it is dropped. Every 5 s it performs one
//   observation through the shared monitor, on its own per-observation
//   ledger. It never takes the fence and appends nothing.
// - Items 3 and 4: the authority checkpoint over a `JournalAppendHeld`
//   borrow (level 4 held): the mandatory guard rechecks, the final monitored
//   observation, the latch check, the admission-boundary check, then
//   `FinalGate::admit` (the one `AdmissionPermit`) or the effect's own intent
//   append. Any failure latches the gate.
// - Item 8: every stop names its existing row.
// Law X4 r8 S11.6 (unit X4-F3): the first-cause rule FC. Every latch of the
// gate after the guard's entry is a stop transition of the operation's stop
// handle: its latch and its cause's record are one critical section of the
// stop-cause lock, and the record is made only by the transition that set
// `LATCHED` (invariant I1). Readers only read. The guard's entry refuses a
// gate already latched (LD8-10).
// The crash matrix's `x4.*` points (law X9 r1 item 5 and G4) are placed
// here: `x4.observer.tick` (a `gate`, replacing the observer's timed wait when
// armed) and `x4.observer.after-observation`; `x4.checkpoint.before-
// observation`, `.after-observation` and `.before-admit`, inside the
// checkpoint's `x4.checkpoint` scope; `x4.gate.admit.after` and
// `.latch.after` sit in `commit_authority`. Without the test-only feature
// every point expands to nothing. Library only.
use super::first_registration::{ProjectWriteRefusal, recheck_registered_owners};
use super::installation_admission::{
    Chain, CustodyRefusal, DurableBarrierQualification, EndpointValues, GateRefusal, RequiredFile,
    observe_private_file,
};
use super::installation_routing::gate_refusal;
use super::namespace_lease::{HeldLease, Namespace, NamespaceSubject, recheck_namespace_at};
use super::operation_handoff::{OperationBinding, OperationRow};
use super::project_chain::ProjectChainPolicy;
use super::read_premise::ReceiptGuard;
use super::store_endpoint::SelectedStoreEndpoint;
use crate::InstallationTermination as T;
use crate::RootDetail;
use crate::commit_authority::{AdmissionPermit, AttemptState, OperationGate, StopObserver};
use crate::journal_store::{JournalAppendHeld, OperationCarrier};
use crate::revocation::{FreshnessMonitor, MonitorStop, Sample, StopReason, native_clock};
use crate::trust::{
    AdmittedCurrentTrust, LiveObservation, ObservationHook, Observed, RetainedTrustHandles,
    TrustRow,
};
use opensip_identity::ProjectRegistryEntry;
use opensip_platform::{DescriptorFilesystem, WorkFailure, WorkScope};
use std::collections::BTreeSet;
use std::sync::mpsc::{self, Receiver, RecvTimeoutError, Sender};
use std::sync::{Arc, Mutex, MutexGuard, PoisonError};
use std::thread::JoinHandle;
use std::time::Duration;

/// S6's observer period (law X4 r7 item 5).
pub(crate) const OBSERVER_PERIOD: Duration = Duration::from_secs(5);

/// The monitor's clock: the native awake clock in production, a script in
/// tests (every test uses scripted clocks; none qualifies native timing).
pub(crate) type MonitorClock = Box<dyn FnMut() -> Result<Sample, StopReason> + Send>;

/// When the observer ticks. Production: every `OBSERVER_PERIOD`. Tests: only
/// when the test sends a tick, so the cadence is controlled and no test
/// sleeps.
pub(crate) enum Cadence {
    Period(Duration),
    #[cfg(test)]
    Manual,
}
/// The guard's seam: the monitor's clock, the observer's cadence and the
/// observation's hook. Production passes `live()`.
pub(crate) struct GuardSeam {
    pub(crate) clock: MonitorClock,
    pub(crate) cadence: Cadence,
    pub(crate) hook: ObservationHook,
}
impl GuardSeam {
    pub(crate) fn live() -> Self {
        Self {
            clock: Box::new(native_clock),
            cadence: Cadence::Period(OBSERVER_PERIOD),
            hook: ObservationHook::live(),
        }
    }
}
impl std::fmt::Debug for GuardSeam {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("GuardSeam").finish_non_exhaustive()
    }
}

// ------------------------------------------------------------- stopping

/// Why the operation stopped: the first stop's cause, recorded with its
/// latch and never replaced (law X4 r7 items 7 and 8; X4 r8 S11.6's rule
/// FC). X3d's end path reads it for its `REV`.
#[derive(Clone, Debug, PartialEq, Eq)]
pub(crate) enum StopCause {
    /// A revoking observation: `trust-revoked` or `policy`.
    Revoked { subject: &'static str },
    /// An observer or monitor fail-stop, with the stop reason.
    FailStop { subject: &'static str },
    /// A stale guard, with the failing guard's own row.
    Stale(OperationRow),
    /// Law X4 r8 LD8-7 (unit X4-F3): a certain refusal, X3d's
    /// (`OperationGuard::stop`) or the checkpoint's lock mismatch. X3d's
    /// `REV` reason for it stays `operation-stopped`; its row is the
    /// invariant row, which no checkpoint reaches.
    CertainRefusal,
}
/// A checkpoint refusal. Each names one row (`row`), and every one latched
/// the gate before it was returned.
#[derive(Clone, Debug, PartialEq, Eq)]
pub(crate) enum GuardRefusal {
    /// The first stop's recorded cause.
    Stopped(StopCause),
    /// The checkpoint was handed a level-4 borrow that is not this
    /// operation's append lock: a broken caller.
    Invariant,
}
impl StopCause {
    pub(crate) fn row(&self) -> OperationRow {
        match self {
            Self::Revoked { subject } => {
                OperationRow::Installation(T::RevokedDuringOperation { subject })
            }
            Self::FailStop { subject } => {
                OperationRow::Installation(T::ObserverFailStop { subject })
            }
            Self::Stale(row) => row.clone(),
            Self::CertainRefusal => OperationRow::Installation(T::Invariant),
        }
    }
}
impl GuardRefusal {
    pub(crate) fn row(&self) -> OperationRow {
        match self {
            Self::Stopped(cause) => cause.row(),
            Self::Invariant => OperationRow::Installation(T::Invariant),
        }
    }
}

/// Law X4 r8 S11.6 (unit X4-F3): the operation's stop handle, its gate's
/// stop observer bound to its one stop-cause record. From the guard's entry,
/// every latch of the gate is this handle's stop transition (LD8-6): the
/// observer's, the checkpoint's, the monitor's (`MonitorStop`) and X3d's
/// certain refusals. Never serialized; it lives in its guard and its
/// monitor.
#[derive(Clone)]
pub(crate) struct StopHandle(Arc<StopRecord>);
struct StopRecord {
    gate: StopObserver,
    /// The first stop's cause, recorded only by the stop transition that set
    /// `LATCHED` (invariant I1).
    cause: Mutex<Option<StopCause>>,
    /// Test seam (law X4 r8 W-8): run once after the next stop transition's
    /// release, outside its critical section.
    #[cfg(test)]
    after: Mutex<Option<Box<dyn FnOnce() + Send>>>,
}
/// What one stop transition did: the decoded state after it, whether it was
/// the operation's first stop, and the recorded cause, which is the first
/// stop's.
#[derive(Clone, Debug, PartialEq, Eq)]
pub(crate) struct Transition {
    pub(crate) state: AttemptState,
    pub(crate) first: bool,
    pub(crate) cause: Option<StopCause>,
}
impl Transition {
    /// The first stop's cause, as a checkpoint reports it. No cause after a
    /// stop transition would breach I1: the invariant row (LD8-8).
    fn refusal(self) -> GuardRefusal {
        self.cause
            .map_or(GuardRefusal::Invariant, GuardRefusal::Stopped)
    }
}
/// The stop-cause record's lock.
fn slot(cause: &Mutex<Option<StopCause>>) -> MutexGuard<'_, Option<StopCause>> {
    cause.lock().unwrap_or_else(PoisonError::into_inner)
}
impl StopHandle {
    /// The entry rule's step 1: the operation's record, holding no cause.
    fn new(gate: StopObserver) -> Self {
        Self(Arc::new(StopRecord {
            gate,
            cause: Mutex::new(None),
            #[cfg(test)]
            after: Mutex::new(None),
        }))
    }
    /// Law X4 r8 S11.6's stop transition (LD8-6), for every source after the
    /// guard's entry: (1) take the stop-cause lock; (2) the one fetch-OR of
    /// `LATCHED`; (3) record `cause` if, and only if, that fetch-OR set
    /// `LATCHED`; (4) read the recorded cause; (5) release the lock; then
    /// (6) `x4.gate.latch.after`, outside the lock (LD8-4). The section holds
    /// only the word's operation and the record's insert and read: no I/O,
    /// wait, callback or crash point, and never the monitor's mutex.
    pub(crate) fn stop(&self, cause: StopCause) -> Transition {
        let StopRecord {
            gate,
            cause: record,
            ..
        } = &*self.0;
        let transition = gate.latch_within(|latching| {
            let mut slot = slot(record);
            let latched = latching.fetch_latch();
            if latched.first {
                slot.get_or_insert(cause);
            }
            Transition {
                state: latched.state,
                first: latched.first,
                cause: slot.clone(),
            }
        });
        #[cfg(test)]
        {
            let after = slot_after(&self.0.after).take();
            if let Some(after) = after {
                after();
            }
        }
        transition
    }
    /// A reader that has seen `LATCHED` (S11.6; LD8-8): the first stop's
    /// recorded cause. It records nothing. None recorded would be a latch
    /// outside a stop transition after the guard's entry, a breach of I1:
    /// the invariant row.
    fn latched(&self) -> GuardRefusal {
        self.cause()
            .map_or(GuardRefusal::Invariant, GuardRefusal::Stopped)
    }
    /// The first stop's recorded cause, if any.
    fn cause(&self) -> Option<StopCause> {
        slot(&self.0.cause).clone()
    }
    /// The gate's decoded state (one load; no lock).
    fn observe(&self) -> AttemptState {
        self.0.gate.observe()
    }
    /// The entry rule's step 3: whether the gate's word has `LATCHED`, read
    /// under the record's lock.
    fn entry_latched(&self) -> bool {
        let _slot = slot(&self.0.cause);
        matches!(
            self.0.gate.observe(),
            AttemptState::LatchedBeforeAdmission | AttemptState::AdmittedThenLatched
        )
    }
}
#[cfg(test)]
fn slot_after(
    after: &Mutex<Option<Box<dyn FnOnce() + Send>>>,
) -> MutexGuard<'_, Option<Box<dyn FnOnce() + Send>>> {
    after.lock().unwrap_or_else(PoisonError::into_inner)
}
/// From the guard's entry the monitor latches only through the stop handle:
/// a failed read or boundary check with its caller's subject (sources 2 and
/// 3), and an unwind with `latched`, the subject the poisoned-mutex path
/// records (source 4).
impl MonitorStop for StopHandle {
    fn state(&self) -> AttemptState {
        self.observe()
    }
    fn fail(&self, subject: &'static str) {
        self.stop(StopCause::FailStop { subject });
    }
    fn unwound(&self) {
        self.stop(StopCause::FailStop { subject: "latched" });
    }
}
/// One observation's read, for the observer's tick and checkpoint step 2:
/// continue, with any drift; a revocation, the observer's stop transition
/// (source 1); or a failed read, whose stop transition the monitor made
/// (sources 2 and 4), or an earlier stop did, so its cause is read here and
/// never recorded.
fn observed(
    stop: &StopHandle,
    read: Result<Observed, StopReason>,
) -> Result<Option<&'static str>, GuardRefusal> {
    match read {
        Ok(Observed::Continue { drift }) => Ok(drift),
        Ok(Observed::Revoke { subject }) => {
            Err(stop.stop(StopCause::Revoked { subject }).refusal())
        }
        Err(_) => Err(stop.latched()),
    }
}
/// The shared monitor's lock. A poisoned mutex is source 5: the stop
/// transition with `FailStop { latched }`, today's subject.
fn lock_monitor<'a, M>(
    monitor: &'a Mutex<M>,
    stop: &StopHandle,
) -> Result<MutexGuard<'a, M>, GuardRefusal> {
    monitor.lock().map_err(|_| {
        stop.stop(StopCause::FailStop { subject: "latched" })
            .refusal()
    })
}
/// Checkpoint step 1's stale guard (source 6): its stop transition records
/// the failing guard's own row.
fn stale(stop: &StopHandle, row: OperationRow) -> GuardRefusal {
    stop.stop(StopCause::Stale(row)).refusal()
}
/// The checkpoint's trailing latch on every refusal (S11.6): a stop
/// transition whose cause is the refusal's own, or `CertainRefusal` for the
/// lock mismatch (source 7, LD8-7). It reports the first stop's cause; the
/// lock mismatch stays `GuardRefusal::Invariant`.
fn refuse(stop: &StopHandle, refusal: GuardRefusal) -> GuardRefusal {
    match refusal {
        GuardRefusal::Invariant => {
            stop.stop(StopCause::CertainRefusal);
            GuardRefusal::Invariant
        }
        GuardRefusal::Stopped(cause) => stop.stop(cause).refusal(),
    }
}

// ---------------------------------------------------------- the monitor

/// One monitor history and its clock, behind the guard's one mutex. At the
/// lease-free point it latches the bare gate; from the guard's entry,
/// through the operation's stop handle.
struct MonitorCell<S = StopObserver> {
    monitor: FreshnessMonitor<S>,
    clock: MonitorClock,
}
/// Law X4 r7 item 2: what the lease-free point creates first, under the
/// fence and before any lease: the operation's one gate and its monitor.
pub(crate) struct LeaseFree {
    gate: OperationGate,
    stop: StopObserver,
    cell: MonitorCell,
}
/// The first read's refusal: the counter's own, or the monitor's (a clock
/// failure, a stall or a latch), which is the fail-stop row.
#[derive(Debug)]
pub(crate) enum FirstRead<E> {
    Counter(E),
    Monitor(StopReason),
}
impl LeaseFree {
    pub(crate) fn create(clock: MonitorClock) -> Self {
        let (gate, stop) = OperationGate::new();
        Self {
            gate,
            cell: MonitorCell {
                monitor: FreshnessMonitor::new(stop.clone()),
                clock,
            },
            stop,
        }
    }
    /// The monitor's first `read`: `counter` runs inside its bracket and
    /// receives the read's opening sample. Any failure latches the gate.
    pub(crate) fn first_read<R, E>(
        &mut self,
        counter: impl FnOnce(&Sample) -> Result<R, E>,
    ) -> Result<R, FirstRead<E>> {
        let mut refused = None;
        let MonitorCell { monitor, clock } = &mut self.cell;
        let read = monitor.read_sampled_with(
            clock,
            |sample| {
                counter(sample).map_err(|e| {
                    refused = Some(e);
                })
            },
            StopReason::subject,
        );
        match (read, refused) {
            (Ok(value), _) => Ok(value),
            (Err(_), Some(e)) => Err(FirstRead::Counter(e)),
            (Err(reason), None) => Err(FirstRead::Monitor(reason)),
        }
    }
    pub(crate) fn state(&self) -> AttemptState {
        self.gate.observe()
    }
    /// Test seam (law X4 r8 W-12): a bare latch on one of the lease-free
    /// point's three handles, outside any critical section.
    #[cfg(test)]
    pub(crate) fn latch_bare(&self, handle: BareHandle) -> AttemptState {
        match handle {
            BareHandle::Gate => self.gate.latch(),
            BareHandle::Stop => self.stop.latch(),
            BareHandle::Monitor => self.cell.monitor.stop().latch(),
        }
    }
}
/// The lease-free point's three handles that can latch the gate bare.
#[cfg(test)]
#[derive(Clone, Copy, Debug)]
pub(crate) enum BareHandle {
    Gate,
    Stop,
    Monitor,
}

/// Law X4 r8 S11.6's entry rule, steps 1 to 4 (unit X4-F3; LD8-10): the
/// operation's parts once its record exists and its monitor is rebound.
struct Entered {
    gate: OperationGate,
    stop: StopHandle,
    cell: MonitorCell<StopHandle>,
}
/// The entry rule. `Err` is a gate already latched before the guard exists
/// (by `StopOnUnwind` at the first read, or any lease-free handle): its parts
/// come back untouched, the latch kept, the monitor's history kept and
/// nothing recorded, and no guard is made.
fn enter(lease_free: LeaseFree) -> Result<Entered, Entered> {
    let LeaseFree { gate, stop, cell } = lease_free;
    // 1. The record: the operation's stop handle, holding no cause.
    let stop = StopHandle::new(stop);
    // 2. The rebind: the monitor latches through that handle from now on,
    // and its bare clone is consumed. No bare latch remains reachable
    // outside the guard's own stop transitions.
    let MonitorCell { monitor, clock } = cell;
    let cell = MonitorCell {
        monitor: monitor.rebind(stop.clone()),
        clock,
    };
    // 3. The check: the gate's word, under the record's lock.
    let latched = stop.entry_latched();
    let entered = Entered { gate, stop, cell };
    // 4. A latched gate gets no guard.
    if latched { Err(entered) } else { Ok(entered) }
}
/// Why `OperationGuard::start` made no guard.
#[derive(Debug)]
pub(crate) enum GuardStart {
    /// Law X4 r8 LD8-10 (unit X4-F3): the gate was latched before the
    /// guard's entry. The handoff's existing fail-stop row, subject
    /// `latched`.
    Latched,
    /// The observer thread could not be started: the host I/O row.
    Observer(std::io::Error),
}

// ------------------------------------------------------------ the guard

/// What the observer and the checkpoints share.
struct Shared {
    monitor: Mutex<MonitorCell<StopHandle>>,
    /// The operation's stop handle: `LeaseFree`'s stop observer, bound at the
    /// guard's entry to the operation's stop-cause record.
    stop: StopHandle,
    /// The start view: the immutable start epoch, closure and floors.
    start: AdmittedCurrentTrust,
    handles: RetainedTrustHandles,
    core_closure: String,
    hook: ObservationHook,
    drift: Mutex<BTreeSet<&'static str>>,
}
impl Shared {
    fn lock(&self) -> Result<MutexGuard<'_, MonitorCell<StopHandle>>, GuardRefusal> {
        lock_monitor(&self.monitor, &self.stop)
    }
    /// One observation through the shared monitor (law X4 r7 item 5): one
    /// `read` whose counter is the whole two-attempt observation. The read's
    /// own opening sample is the observation's clock (law X4T r11 item 6,
    /// unit X4-F1); no other sample is taken. A failed read's stop
    /// transition is the monitor's, with the observation's own failure
    /// subject, else the stop reason's (law X4 r8 S11.6, source 2).
    fn observe(&self, cell: &mut MonitorCell<StopHandle>) -> Result<(), GuardRefusal> {
        let failure = std::cell::Cell::new(None);
        let observation = LiveObservation {
            handles: &self.handles,
            start: &self.start,
            core_closure: &self.core_closure,
            hook: &self.hook,
        };
        let MonitorCell { monitor, clock } = cell;
        let read = monitor.read_sampled_with(
            clock,
            |opening| {
                observation.observe(opening).map_err(|f| {
                    failure.set(Some(f.subject()));
                })
            },
            |reason| failure.get().unwrap_or_else(|| reason.subject()),
        );
        if let Some(drift) = observed(&self.stop, read)? {
            self.drift
                .lock()
                .unwrap_or_else(|p| p.into_inner())
                .insert(drift);
        }
        Ok(())
    }
}

/// The observer's signals: stop, or (tests) one tick to run now.
enum Signal {
    Stop,
    #[cfg(test)]
    Tick(Sender<bool>),
}
/// The running observer thread. Dropping it stops and joins the thread.
struct Observer {
    signals: Sender<Signal>,
    thread: Option<JoinHandle<()>>,
}
impl Drop for Observer {
    fn drop(&mut self) {
        let _ = self.signals.send(Signal::Stop);
        if let Some(thread) = self.thread.take() {
            let _ = thread.join();
        }
    }
}
/// What ended the observer's wait.
enum Wake {
    /// The period elapsed (or, armed, the `x4.observer.tick` gate resumed).
    Tick,
    /// A test asked for one tick now.
    #[cfg(test)]
    TestTick(Sender<bool>),
    /// The guard is dropped or stopped.
    Stop,
}
fn wait(signals: &Receiver<Signal>, cadence: &Cadence) -> Wake {
    match cadence {
        Cadence::Period(period) => match signals.recv_timeout(*period) {
            Err(RecvTimeoutError::Timeout) => Wake::Tick,
            Ok(Signal::Stop) | Err(RecvTimeoutError::Disconnected) => Wake::Stop,
            #[cfg(test)]
            Ok(Signal::Tick(ack)) => Wake::TestTick(ack),
        },
        #[cfg(test)]
        Cadence::Manual => match signals.recv() {
            Ok(Signal::Tick(ack)) => Wake::TestTick(ack),
            Ok(Signal::Stop) | Err(_) => Wake::Stop,
        },
    }
}
fn observe_loop(shared: Arc<Shared>, signals: Receiver<Signal>, cadence: Cadence) {
    loop {
        // Law X9 r1 G4: the observer's period is a `gate` point. Unarmed, the
        // timed wait runs; armed, its rendezvous replaces it and a tick
        // happens exactly when the parent resumes it.
        let waited = std::cell::Cell::new(None);
        opensip_platform::crash_barrier!(
            "x4.observer",
            "tick",
            gate,
            waited.set(Some(wait(&signals, &cadence)))
        );
        let ack = match waited.into_inner().unwrap_or(Wake::Tick) {
            Wake::Tick => None,
            #[cfg(test)]
            Wake::TestTick(ack) => Some(ack),
            Wake::Stop => return,
        };
        let stopped = match shared.lock() {
            Ok(mut cell) => shared.observe(&mut cell).is_err(),
            Err(_) => true,
        };
        opensip_platform::crash_barrier!("x4.observer", "after-observation", step);
        #[cfg(test)]
        if let Some(ack) = ack {
            let _ = ack.send(!stopped);
        }
        #[cfg(not(test))]
        let _: Option<()> = ack;
        if stopped {
            return;
        }
    }
}

/// Law X4 r7 item 6: one admitted writer operation's live authority. Built
/// only inside X2e's handoff, under the held fence, from the gate, monitor
/// and view the lease-free point created; moved into `ProjectOperation`
/// with X2e's other owners. Holds the monitor history, the gate and its
/// stop observer, the start view (immutable epoch, closure subjects and
/// floors; the required permission pairs of every M2 writer are empty), the
/// retained trust handles and the drift record. The receipt, lease, owners
/// and endpoint stay in `ProjectOperation`, which lends them to each
/// checkpoint. Not Clone; no serialized form.
pub(crate) struct OperationGuard {
    // Declaration order is drop order: the observer stops first.
    observer: Option<Observer>,
    gate: OperationGate,
    shared: Arc<Shared>,
    trust_groups: BTreeSet<u32>,
}
impl std::fmt::Debug for OperationGuard {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("OperationGuard")
            .field("state", &self.gate.observe())
            .finish_non_exhaustive()
    }
}
impl OperationGuard {
    /// Build the guard from the lease-free point's products and start its
    /// observer thread. Law X4 r8 S11.6's entry rule (unit X4-F3; LD8-10)
    /// comes first: the record, the monitor's rebind and the gate's check,
    /// and only then (step 5) the observer, so I1 holds at the guard's entry.
    /// A gate already latched gets no guard and no observer; a thread that
    /// cannot be started is the host I/O row.
    pub(crate) fn start(
        lease_free: LeaseFree,
        view: AdmittedCurrentTrust,
        handles: RetainedTrustHandles,
        core_closure: String,
        trust_groups: BTreeSet<u32>,
        cadence: Cadence,
        hook: ObservationHook,
    ) -> Result<Self, GuardStart> {
        let Entered { gate, stop, cell } = enter(lease_free).map_err(|_| GuardStart::Latched)?;
        let shared = Arc::new(Shared {
            monitor: Mutex::new(cell),
            stop,
            start: view,
            handles,
            core_closure,
            hook,
            drift: Mutex::new(BTreeSet::new()),
        });
        let (signals, receiver) = mpsc::channel();
        let thread = std::thread::Builder::new()
            .name("opensip-observer".into())
            .spawn({
                let shared = Arc::clone(&shared);
                move || observe_loop(shared, receiver, cadence)
            })
            .map_err(GuardStart::Observer)?;
        Ok(Self {
            observer: Some(Observer {
                signals,
                thread: Some(thread),
            }),
            gate,
            shared,
            trust_groups,
        })
    }
    /// The gate's state (law X4 r7 item 7).
    pub(crate) fn state(&self) -> AttemptState {
        self.gate.observe()
    }
    /// Law X3d r6 item 3 (unit X3d-1): a certain refusal stops the
    /// operation before admission, so its one gate latches (the fetch-OR
    /// `2`, X4 r7 item 7: `0` to `2`, and no `RA`, intent, commit or `SEAL`
    /// follows). Law X4 r8 S11.6 (unit X4-F3): it is the stop transition
    /// with X3d's `cause`, `CertainRefusal`, recorded only if it is the first
    /// stop; a stop already recorded stays. Never resets; after admission it
    /// is the `1` to `3` latch, which never relabels the admitted outcome.
    pub(crate) fn stop(&self, cause: StopCause) -> AttemptState {
        self.shared.stop.stop(cause).state
    }
    /// The first stop's recorded cause, if any.
    pub(crate) fn cause(&self) -> Option<StopCause> {
        self.shared.stop.cause()
    }
    /// S6's drift recorded under the operation.
    pub(crate) fn drift(&self) -> Vec<&'static str> {
        self.shared
            .drift
            .lock()
            .unwrap_or_else(|p| p.into_inner())
            .iter()
            .copied()
            .collect()
    }
    /// The start view the monitor's first read admitted.
    pub(crate) fn start_view(&self) -> &AdmittedCurrentTrust {
        &self.shared.start
    }
    /// Test seam: run one observer tick now and wait for it. True if the
    /// observation continued; false if it stopped the observer, or if the
    /// observer had already stopped.
    #[cfg(test)]
    pub(crate) fn tick(&self) -> bool {
        self.watch().tick()
    }
    /// Test seam: hold the shared monitor (as a checkpoint or tick does).
    #[cfg(test)]
    pub(crate) fn hold_monitor(&self) -> impl Drop + '_ {
        self.shared.monitor.lock().unwrap()
    }
    /// Test seam (law X4 r8 W-8): the guard as a test sees it after the
    /// operation has moved into a session.
    #[cfg(test)]
    pub(crate) fn watch(&self) -> Watch {
        Watch {
            signals: self
                .observer
                .as_ref()
                .map(|observer| observer.signals.clone()),
            stop: self.shared.stop.clone(),
        }
    }
    /// Test seam (law X4 r8 W-10 (c)): hold the stop-cause lock on a thread
    /// of its own, outside any stop transition, until the value is dropped.
    #[cfg(test)]
    pub(crate) fn hold_cause(&self) -> impl Drop + use<> {
        struct Held {
            release: Option<Sender<()>>,
            thread: Option<JoinHandle<()>>,
        }
        impl Drop for Held {
            fn drop(&mut self) {
                drop(self.release.take());
                if let Some(thread) = self.thread.take() {
                    let _ = thread.join();
                }
            }
        }
        let stop = self.shared.stop.clone();
        let (locked, held) = mpsc::channel();
        let (release, wait) = mpsc::channel::<()>();
        let thread = std::thread::spawn(move || {
            let _slot = slot(&stop.0.cause);
            let _ = locked.send(());
            let _ = wait.recv();
        });
        let _ = held.recv();
        Held {
            release: Some(release),
            thread: Some(thread),
        }
    }
}
/// Test seam (law X4 r8 W-8): one observer tick on request, the recorded
/// cause and the gate's state, and a hook after the next stop transition's
/// release. Reads only; it latches nothing.
#[cfg(test)]
pub(crate) struct Watch {
    signals: Option<Sender<Signal>>,
    stop: StopHandle,
}
#[cfg(test)]
impl Watch {
    /// Run one observer tick now and wait for it. True if the observation
    /// continued; false if it stopped the observer, or if the observer had
    /// already stopped.
    pub(crate) fn tick(&self) -> bool {
        let Some(signals) = &self.signals else {
            return false;
        };
        let (ack, done) = mpsc::channel();
        signals.send(Signal::Tick(ack)).is_ok() && done.recv().unwrap_or(false)
    }
    pub(crate) fn cause(&self) -> Option<StopCause> {
        self.stop.cause()
    }
    pub(crate) fn state(&self) -> AttemptState {
        self.stop.observe()
    }
    /// Run `hook` once, after the next stop transition's release.
    pub(crate) fn after_stop(&self, hook: impl FnOnce() + Send + 'static) {
        *slot_after(&self.stop.0.after) = Some(Box::new(hook));
    }
}

// ------------------------------------------------------- the checkpoint

/// What a checkpoint borrows from the operation: the guard and every owner
/// of law X4 r7 item 4's mandatory set. Lent by `ProjectOperation::journal`
/// only, inside the attempt ledger's charge, beside the started carrier.
pub(crate) struct Checkpoint<'a> {
    pub(super) guard: &'a OperationGuard,
    pub(super) receipt: &'a ReceiptGuard<'a>,
    pub(super) qualification: &'a dyn DurableBarrierQualification,
    pub(super) lease: &'a HeldLease,
    pub(super) namespace: &'a Namespace,
    pub(super) subject: &'a NamespaceSubject,
    pub(super) binding: &'a OperationBinding,
    pub(super) row: &'a ProjectRegistryEntry,
    pub(super) endpoint: &'a EndpointValues,
    pub(super) required: &'a [RequiredFile],
    pub(super) chain: &'a Chain,
    pub(super) uid: u32,
    pub(super) carrier: &'a OperationCarrier,
}
/// A passed checkpoint for a brokered effect request: the effect's own
/// intent append must follow at once. Not Clone, never serialized, not a
/// reusable token.
#[derive(Debug)]
pub(crate) struct EffectCheckpoint(());

fn project(refusal: ProjectWriteRefusal) -> OperationRow {
    OperationRow::Project(refusal.row())
}
impl Checkpoint<'_> {
    /// Steps 1 to 4 for a brokered effect request (and X3d's checkpoints
    /// before the SEAL, which admit nothing yet).
    pub(crate) fn effect(
        &self,
        held: &JournalAppendHeld<'_, '_>,
        work: &mut WorkScope<'_>,
    ) -> Result<EffectCheckpoint, GuardRefusal> {
        self.run(held, work, || Ok(EffectCheckpoint(())))
            .map_err(|(refusal, ())| refusal)
    }
    /// Steps 1 to 4 ending in `FinalGate::admit`, which binds `prepared` and
    /// mints the operation's one `AdmissionPermit`. On a refusal the prepared
    /// value is handed back with it, for the caller's stop order.
    pub(crate) fn admit<P>(
        &self,
        held: &JournalAppendHeld<'_, '_>,
        prepared: P,
        work: &mut WorkScope<'_>,
    ) -> Result<AdmissionPermit<P>, (GuardRefusal, P)> {
        let mut prepared = Some(prepared);
        let result = self.run(held, work, || {
            let value = prepared.take().expect("admitted once");
            self.guard.gate.admit(value).map_err(|(value, _)| {
                prepared = Some(value);
                self.guard.shared.stop.latched()
            })
        });
        result.map_err(|(refusal, ())| (refusal, prepared.take().expect("returned on refusal")))
    }
    /// The checkpoint inside its `x4.checkpoint` scope, so that the lease
    /// probe's lock primitive is named under it in a matrix run.
    fn run<R>(
        &self,
        held: &JournalAppendHeld<'_, '_>,
        work: &mut WorkScope<'_>,
        finish: impl FnOnce() -> Result<R, GuardRefusal>,
    ) -> Result<R, (GuardRefusal, ())> {
        opensip_platform::crash_scope!("x4.checkpoint", { self.steps(held, work, finish) })
    }
    fn steps<R>(
        &self,
        held: &JournalAppendHeld<'_, '_>,
        work: &mut WorkScope<'_>,
        finish: impl FnOnce() -> Result<R, GuardRefusal>,
    ) -> Result<R, (GuardRefusal, ())> {
        let shared = &self.guard.shared;
        // Every refusal ends with the trailing latch, a stop transition that
        // reports the first stop's cause (law X4 r8 S11.6).
        let stop = |refusal: GuardRefusal| Err((refuse(&shared.stop, refusal), ()));
        if !held.holds(self.carrier.lock()) {
            // Source 7: a broken caller, recorded as `CertainRefusal`.
            return stop(GuardRefusal::Invariant);
        }
        // Step 1: the guard rechecks, charged to the attempt ledger. They may
        // block; nothing observed before this checkpoint is authority.
        if let Err(row) = self.guards(work) {
            return stop(stale(&shared.stop, row));
        }
        opensip_platform::crash_barrier!("x4.checkpoint", "before-observation", step);
        // Steps 2 to 4 hold the shared monitor: no other read, wait or
        // callback runs between the final observation and admission.
        let mut cell = match shared.lock() {
            Ok(cell) => cell,
            Err(refusal) => return stop(refusal),
        };
        // Step 2: the final monitored observation and S6's predicate.
        if let Err(refusal) = shared.observe(&mut cell) {
            return stop(refusal);
        }
        opensip_platform::crash_barrier!("x4.checkpoint", "after-observation", step);
        // Step 3: the latch.
        match self.guard.gate.observe() {
            AttemptState::Preparing => {}
            // A checkpoint after this operation's admission (F41's second
            // admission): nothing has latched, so the trailing stop
            // transition is the first stop (1 to 3), with today's cause.
            AttemptState::Admitted => {
                return stop(GuardRefusal::Stopped(StopCause::FailStop {
                    subject: "latched",
                }));
            }
            // A stop came first: its recorded cause.
            AttemptState::LatchedBeforeAdmission | AttemptState::AdmittedThenLatched => {
                return stop(shared.stop.latched());
            }
        }
        opensip_platform::crash_barrier!("x4.checkpoint", "before-admit", step);
        // Step 4: one clock sample, no I/O, then admission at once. The
        // boundary's own failure is its stop transition (source 3); after it,
        // or after an `AlreadyStopped`, the trailing stop transition with
        // `admission-boundary` records nothing and reports the first cause.
        let MonitorCell { monitor, clock } = &mut *cell;
        if monitor.boundary_with(clock, "admission-boundary").is_err() {
            return stop(GuardRefusal::Stopped(StopCause::FailStop {
                subject: "admission-boundary",
            }));
        }
        let admitted = finish();
        drop(cell);
        match admitted {
            Ok(value) => Ok(value),
            Err(refusal) => stop(refusal),
        }
    }
    /// Law X4 r7 item 4's mandatory set after the fence's release, each by
    /// retained identity and full sample, charged to the attempt ledger:
    /// the write receipt, the held lease, the original owners, the
    /// namespace, the store endpoint and lineage owners, and the operation
    /// joins. The registry, the selection pair and `state.v1` are
    /// provenance and are not rechecked.
    fn guards(&self, work: &mut WorkScope<'_>) -> Result<(), OperationRow> {
        let uid = self.uid;
        self.receipt.recheck_in(work).map_err(|f| match f {
            WorkFailure::Budget(_) => OperationRow::BudgetExhausted,
            WorkFailure::Operation(row) => OperationRow::Installation(row),
        })?;
        self.lease
            .recheck_held(&self.namespace.directory, uid, work)
            .map_err(|f| project(ProjectWriteRefusal::Namespace(f)))?;
        let home_filesystem =
            |sample: &DescriptorFilesystem| self.qualification.is_home_filesystem(sample);
        let policy = ProjectChainPolicy::new(
            self.qualification.omission_premise(),
            &home_filesystem,
            &self.guard.trust_groups,
        );
        match self.subject {
            NamespaceSubject::Eligible { admission, .. } => admission
                .recheck_owners(uid, &policy, work)
                .map_err(|f| project(ProjectWriteRefusal::Project(f)))?,
            NamespaceSubject::Registered(registered) => {
                recheck_registered_owners(registered, uid, &policy, work)
                    .map_err(|f| project(ProjectWriteRefusal::Registration(f)))?
            }
        }
        let i = self.chain.installation();
        recheck_namespace_at(self.namespace, i, uid, work)
            .map_err(|f| project(ProjectWriteRefusal::Namespace(f)))?;
        let gate = |refusal: &GateRefusal| OperationRow::Installation(gate_refusal(refusal));
        for file in self.required.iter().filter(|file| {
            file.relative().starts_with("stores/") || file.relative().starts_with("transitions/")
        }) {
            let now = observe_private_file(i, file.relative(), uid, work).map_err(|f| match f {
                WorkFailure::Budget(_) => OperationRow::BudgetExhausted,
                WorkFailure::Operation(refusal) => gate(&refusal),
            })?;
            if &now != file.metadata() {
                return Err(gate(&GateRefusal::Custody(CustodyRefusal::Changed)));
            }
        }
        let endpoint = SelectedStoreEndpoint::new(self.endpoint);
        let n = self.namespace.id.as_str();
        if self.binding.namespace_id() != n
            || self.row.namespace_id() != n
            || self.carrier.lock().namespace_id() != n
            || self.binding.store_instance() != endpoint.store_instance()
            || self.binding.store_generation() != endpoint.store_generation()
            || self.binding.state_schema() != endpoint.state_schema()
        {
            return Err(OperationRow::Installation(T::Invariant));
        }
        Ok(())
    }
}

/// Law X4 r7 item 8 with X4T r9 item 10 (unit X4a): the fenced trust
/// admission's refusal rows at the lease-free point, as new variants of
/// 468c's closed vocabulary on existing details. Every match is exhaustive.
pub(crate) fn trust_termination(row: &TrustRow) -> T {
    match row {
        TrustRow::Incomplete => T::Incomplete,
        TrustRow::NoAdmittedTimeContext => T::TrustNoAdmittedTimeContext,
        TrustRow::Continuation(subject) => T::TrustContinuation {
            subject: subject.clone(),
        },
        TrustRow::IndexContinuation(subject) => T::TrustIndexContinuation {
            subject: subject.to_owned(),
        },
        TrustRow::ComponentContinuation(subject) => T::TrustComponentContinuation {
            subject: subject.to_owned(),
        },
        TrustRow::Root(code, subject) => match RootDetail::parse(code) {
            Some(detail) => T::TrustRoot {
                detail,
                subject: subject.clone(),
            },
            None => T::Invariant,
        },
        TrustRow::PayloadNotAdmissible(subject) => T::TrustPayloadNotAdmissible { subject },
        TrustRow::ClockExcursion(subject) => T::ClockExcursionForward { subject },
        TrustRow::StateSchemaUnsupported => T::StateSchemaUnsupported,
        TrustRow::HostIo => T::HostIo,
        TrustRow::Budget => T::BudgetExhausted,
        TrustRow::Rollback => T::Custody {
            subject: "trust-rollback",
        },
        TrustRow::RequiredFilesChanged => T::Custody {
            subject: "required-files-changed",
        },
        TrustRow::Invariant => T::Invariant,
    }
}

/// Scripted clocks and seams for the guard's tests: no test qualifies native
/// scheduling, and none sleeps.
#[cfg(test)]
pub(crate) mod scripted {
    use super::*;
    /// A boot id in the platform's grammar.
    pub(crate) const BOOT: &str = "00000000-0000-4000-8000-000000000001";
    /// The wall clock at the script's start, 2026-10-02T01:00:00Z: inside
    /// X4T-0's accepted store's time window.
    pub(crate) const WALL: i64 = 1_790_902_800;
    const START: Duration = Duration::from_secs(3600);
    struct State {
        now: Duration,
        boot: String,
        step: Duration,
    }
    /// A monotonic script: each sample is a point at `now`, and `now` moves
    /// on by `step` (1 ms) after it; `advance` is a pause of any length.
    #[derive(Clone)]
    pub(crate) struct Clock(Arc<Mutex<State>>);
    impl Clock {
        pub(crate) fn new() -> Self {
            Self(Arc::new(Mutex::new(State {
                now: START,
                boot: BOOT.to_owned(),
                step: Duration::from_millis(1),
            })))
        }
        pub(crate) fn advance(&self, by: Duration) {
            self.0.lock().unwrap().now += by;
        }
        /// Each later sample moves on by `step` instead.
        pub(crate) fn step_by(&self, step: Duration) {
            self.0.lock().unwrap().step = step;
        }
        pub(crate) fn reboot(&self, boot: &str) {
            self.0.lock().unwrap().boot = boot.to_owned();
        }
        pub(crate) fn sample(&self) -> Result<Sample, StopReason> {
            let mut state = self.0.lock().unwrap();
            let at = state.now;
            let step = state.step;
            state.now += step;
            let elapsed = i64::try_from(at.saturating_sub(START).as_secs()).unwrap();
            Ok(Sample {
                before: at,
                after: at,
                boot: state.boot.clone(),
                wall_seconds: WALL + elapsed,
                wall_nanos: 0,
            })
        }
        pub(crate) fn monitor(&self) -> MonitorClock {
            let clock = self.clone();
            Box::new(move || clock.sample())
        }
    }
    /// The test seam: this clock, ticks only on request, and `hook`.
    pub(crate) fn seam(clock: &Clock, hook: ObservationHook) -> GuardSeam {
        GuardSeam {
            clock: clock.monitor(),
            cadence: Cadence::Manual,
            hook,
        }
    }
    /// Run `f` in a destructor while its thread unwinds from an unrelated panic
    /// (`resume_unwind`, so no panic message is printed): whether the thread was
    /// panicking there, and `f`'s value. `f` must not panic.
    pub(crate) fn unwinding<R>(f: impl FnOnce() -> R) -> (bool, R) {
        struct OnDrop<F: FnOnce()>(Option<F>);
        impl<F: FnOnce()> Drop for OnDrop<F> {
            fn drop(&mut self) {
                if let Some(f) = self.0.take() {
                    f();
                }
            }
        }
        let mut out = None;
        let unwound = std::panic::catch_unwind::<_, ()>(std::panic::AssertUnwindSafe(|| {
            let _on_drop = OnDrop(Some(|| out = Some((std::thread::panicking(), f()))));
            std::panic::resume_unwind(Box::new("an unrelated panic"))
        }));
        assert!(unwound.is_err());
        out.expect("the destructor ran")
    }
    pub(crate) fn invocation() -> crate::trust::TrustInvocation {
        crate::trust::TrustInvocation::new(
            &format!("req1_{}", "a".repeat(32)),
            &format!("exec1_{}", "b".repeat(32)),
            0,
        )
        .unwrap()
    }
}

#[cfg(test)]
mod tests {
    include!("operation_guard_tests.rs");
}
