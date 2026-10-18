//! Admission, commit cells and finalization (S-OP-2 items 15 to 17; M3-O1 items 11 and 12).
//!
//! A featureless build admits no file sink and runs no writer. File projections
//! land in the pre-scope buffer and freeze as `unpersisted`. A settled runtime
//! does not sleep.

use std::sync::atomic::{AtomicBool, AtomicU8, AtomicU64, Ordering};
use std::sync::{Arc, Mutex, MutexGuard};
use std::time::{Duration, Instant};

use opensip_platform::{EntropyError, request_entropy};

use crate::constants::{
    FINALIZE_CANCEL_MS, FINALIZE_NORMAL_MS, LOSS_REASONS, Level, MAX_LINE, PER_NAME_BUDGET,
    loss_cell_index,
};
use crate::kinds::registry::CapabilitySet as IssuedSet;
use crate::sinks::{self, RecordBuffer};

const LEVELS: usize = Level::TEXT.len();
const DROP_CELLS: usize = LOSS_REASONS.len() * LEVELS;

const _: () = assert!(loss_cell_index(0, Level::Error) == 0);
const _: () = assert!(loss_cell_index(LOSS_REASONS.len() - 1, Level::Trace) == DROP_CELLS - 1);

const IDLE: u8 = 0;
const STARTING: u8 = 1;
const RUNNING: u8 = 2;
const UNAVAILABLE: u8 = 3;
const FINALIZING: u8 = 4;
const FROZEN: u8 = 5;

static PHASE: AtomicU8 = AtomicU8::new(IDLE);

/// Entropy failed or the compiled target has no selected operational platform.
/// No record is constructed and no summary is frozen.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct LoggingUnavailable;

/// The one capability set `start` returns to the owning host (M3-O1 item 8).
pub struct CapabilitySet {
    inner: IssuedSet,
}

impl CapabilitySet {
    pub fn process_id_mint(&self) -> &crate::kinds::ProcessIdMint {
        &self.inner.process_id
    }
    pub fn position_mint(&self) -> &crate::kinds::PositionMint {
        &self.inner.position
    }
    pub fn storage_owner(&self) -> &crate::kinds::registry::StorageCommitOwner {
        &self.inner.storage
    }

    pub fn path_ref_mint(&self) -> &crate::kinds::PathRefMint {
        &self.inner.path_ref
    }
    pub fn project_path_mint(&self) -> &crate::kinds::ProjectPathMint {
        &self.inner.project_path
    }
    pub fn snapshot_digest_mint(
        &self,
    ) -> &crate::kinds::IdentityDigestMint<crate::kinds::SnapshotDigest> {
        &self.inner.snapshot_digest
    }
    pub fn closure_digest_mint(
        &self,
    ) -> &crate::kinds::IdentityDigestMint<crate::kinds::ClosureDigest> {
        &self.inner.closure_digest
    }
    pub fn universe_digest_mint(
        &self,
    ) -> &crate::kinds::IdentityDigestMint<crate::kinds::UniverseDigest> {
        &self.inner.universe_digest
    }
    pub fn manifest_digest_mint(
        &self,
    ) -> &crate::kinds::IdentityDigestMint<crate::kinds::ManifestDigest> {
        &self.inner.manifest_digest
    }

    /// Retained by the bootstrap until the admitted policy owner is wired.
    pub fn rule_id_mint(&self) -> &crate::kinds::RuleIdMint {
        &self.inner.rule_id
    }

    /// Retained by the bootstrap until the declaration owner is wired.
    pub fn declared_name_mint(&self) -> &crate::kinds::DeclaredNameMint {
        &self.inner.declared_name
    }

    fn issue() -> Self {
        Self {
            inner: IssuedSet::issue(),
        }
    }

    fn prove_held(&self) {
        std::hint::black_box(&self.inner.process_id);
        std::hint::black_box(&self.inner.position);
        std::hint::black_box(&self.inner.storage);
    }

    /// Request scope. The set is the mint; the bytes are the fixed-width value.
    pub fn request_scope(&self, bytes: [u8; 16]) -> crate::scope::RequestScope {
        self.prove_held();
        crate::scope::RequestScope::minted(crate::scope::RequestId::minted(bytes))
    }

    pub fn project_scope(
        &self,
        request: crate::scope::RequestScope,
        project: [u8; 32],
    ) -> crate::scope::ProjectScope {
        self.prove_held();
        crate::scope::ProjectScope::minted(
            request.request(),
            crate::scope::ProjectId::minted(project),
        )
    }

    pub fn plan_scope(
        &self,
        project: crate::scope::ProjectScope,
        plan: [u8; 32],
    ) -> crate::scope::PlanScope {
        self.prove_held();
        crate::scope::PlanScope::minted(
            project.request(),
            project.project(),
            crate::scope::PlanId::minted(plan),
        )
    }

    pub fn attempt_scope(
        &self,
        project: crate::scope::ProjectScope,
        execution: [u8; 16],
    ) -> crate::scope::AttemptScope {
        self.prove_held();
        crate::scope::AttemptScope::minted(
            project.request(),
            project.project(),
            crate::scope::ExecutionId::minted(execution),
        )
    }

    pub fn plan_attempt_scope(
        &self,
        plan: crate::scope::PlanScope,
        execution: [u8; 16],
    ) -> crate::scope::PlanAttemptScope {
        self.prove_held();
        crate::scope::PlanAttemptScope::minted(
            plan.request(),
            plan.project(),
            plan.plan(),
            crate::scope::ExecutionId::minted(execution),
        )
    }

    pub fn committed_run_scope(
        &self,
        attempt: crate::scope::PlanAttemptScope,
        run: [u8; 32],
    ) -> crate::scope::CommittedRunScope {
        self.prove_held();
        crate::scope::CommittedRunScope::minted(
            attempt.request(),
            attempt.project(),
            attempt.plan(),
            attempt.execution(),
            crate::scope::RunId::minted(run),
        )
    }

    pub fn stored_run_scope(
        &self,
        project: crate::scope::ProjectScope,
        run: [u8; 32],
    ) -> crate::scope::StoredRunScope {
        self.prove_held();
        crate::scope::StoredRunScope::minted(
            project.request(),
            project.project(),
            crate::scope::RunId::minted(run),
        )
    }
}

/// Step 5's derived summary. Counts come from the commit cells read in step 4.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct FrozenSummary {
    pub in_flight_at_freeze: u64,
    pub file_admitted: bool,
    /// Per level, `E_pre − T` when no persistent sink was admitted.
    pub unpersisted: [u64; LEVELS],
    /// Per level, derived `drain-abandoned`.
    pub drain_abandoned: [u64; LEVELS],
    /// Per level, `written` outcomes of the file partition. No file writer means zeros.
    pub written: [u64; LEVELS],
    /// Development stderr outcomes. A featureless build leaves these zero.
    pub stderr_written: [u64; LEVELS],
    pub stderr_failed: [u64; LEVELS],
    pub stderr_abandoned: [u64; LEVELS],
    pub stderr_stopped: [u64; LEVELS],
    pub stderr_error: Option<crate::writer::CapturedError>,
    pub stderr_marker: Option<crate::marker::MarkerOutcome>,
    /// Harness descriptor outcomes, absent unless admission succeeded.
    pub harness_admitted: bool,
    pub harness_written: [u64; LEVELS],
    pub harness_failed: [u64; LEVELS],
    pub harness_abandoned: [u64; LEVELS],
    pub harness_stopped: [u64; LEVELS],
    pub harness_error: Option<crate::writer::CapturedError>,
    pub harness_marker: Option<crate::marker::MarkerOutcome>,
    /// Producer drop tallies, reason-major then level (`loss_cell_index`).
    pub drops: [u64; DROP_CELLS],
}

struct Frozen {
    summary: FrozenSummary,
    #[cfg(test)]
    deadline_ms: u64,
    #[cfg(test)]
    waited: bool,
}

const BUDGET_REQUESTS: usize = 8;
/// One per-name budget per event slot: O1's six (0 to 5), D3a-3's
/// twenty-three (6 to 28) and D3a-4's four (29 to 32, `emit.rs`'s
/// `registered_on!`).
const BUDGET_EVENTS: usize = 33;
const REASON_REFUSED: usize = 0;
const REASON_BUDGET: usize = 1;
const REASON_QUEUE_FULL: usize = 2;
const REASON_PRESCOPE_FULL: usize = 3;
const REASON_DRAIN_ABANDONED: usize = 7;

struct BudgetSlot {
    request: [u8; 16],
    live: bool,
    counts: [u64; BUDGET_EVENTS],
}

struct Budget {
    slots: [BudgetSlot; BUDGET_REQUESTS],
}

impl Budget {
    fn new() -> Self {
        Self {
            slots: std::array::from_fn(|_| BudgetSlot {
                request: [0; 16],
                live: false,
                counts: [0; BUDGET_EVENTS],
            }),
        }
    }

    fn try_take(&mut self, request: [u8; 16], event: usize) -> bool {
        let mut free = None;
        let mut index = 0;
        while index < self.slots.len() {
            if self.slots[index].live && self.slots[index].request == request {
                if self.slots[index].counts[event] >= PER_NAME_BUDGET as u64 {
                    return false;
                }
                self.slots[index].counts[event] += 1;
                return true;
            }
            if !self.slots[index].live && free.is_none() {
                free = Some(index);
            }
            index += 1;
        }
        let Some(index) = free else {
            return false;
        };
        self.slots[index].live = true;
        self.slots[index].request = request;
        self.slots[index].counts = [0; BUDGET_EVENTS];
        self.slots[index].counts[event] = 1;
        true
    }
}

struct Runtime {
    key: [u8; 32],
    admission_open: AtomicBool,
    enqueue_open: Arc<AtomicBool>,
    file_admitted: AtomicBool,
    in_flight: Arc<AtomicU64>,
    drops: Arc<[AtomicU64; DROP_CELLS]>,
    pre_scope_enqueued: [AtomicU64; LEVELS],
    post_freeze_drops: [AtomicU64; DROP_CELLS],
    post_freeze_sources: [AtomicU64; LEVELS],
    budget: Mutex<Budget>,
    pre_scope: Mutex<RecordBuffer>,
    ring: Mutex<RecordBuffer>,
    #[cfg(feature = "operability-dev-sinks")]
    stderr: Arc<crate::dev_writer::DevSink>,
    #[cfg(feature = "harness-instrumentation")]
    harness: Option<Arc<crate::harness_writer::HarnessSink>>,
    frozen: Option<Frozen>,
}

impl Runtime {
    fn new(mut key: [u8; 32]) -> Result<Self, LoggingUnavailable> {
        let enqueue_open = Arc::new(AtomicBool::new(true));
        let in_flight = Arc::new(AtomicU64::new(0));
        let drops = Arc::new(zero_cells());
        #[cfg(feature = "operability-dev-sinks")]
        let stderr = {
            let result = sinks::open_dev_stderr().and_then(|fd| {
                crate::dev_writer::DevSink::start(
                    fd,
                    Arc::clone(&enqueue_open),
                    Arc::clone(&drops),
                    Arc::clone(&in_flight),
                )
            });
            match result {
                Ok(sink) => sink,
                Err(_) => {
                    wipe(&mut key);
                    return Err(LoggingUnavailable);
                }
            }
        };
        #[cfg(feature = "harness-instrumentation")]
        let harness = match opensip_platform::admit_harness_descriptor() {
            Ok(output) => match crate::harness_writer::HarnessSink::start(
                output,
                Arc::clone(&enqueue_open),
                Arc::clone(&drops),
                Arc::clone(&in_flight),
            ) {
                Ok(sink) => Some(sink),
                Err(_) => {
                    wipe(&mut key);
                    return Err(LoggingUnavailable);
                }
            },
            Err(_) => None,
        };
        // The key is copied into its owning runtime; erase this local copy.
        let owned_key = key;
        wipe(&mut key);
        Ok(Self {
            key: owned_key,
            admission_open: AtomicBool::new(true),
            enqueue_open,
            file_admitted: AtomicBool::new(crate::constants::FILE_SINK_ADMITTED),
            in_flight,
            drops,
            pre_scope_enqueued: zero_levels(),
            post_freeze_drops: zero_cells(),
            post_freeze_sources: zero_levels(),
            budget: Mutex::new(Budget::new()),
            pre_scope: Mutex::new(sinks::pre_scope()),
            ring: Mutex::new(sinks::ring()),
            #[cfg(feature = "operability-dev-sinks")]
            stderr,
            #[cfg(feature = "harness-instrumentation")]
            harness,
            frozen: None,
        })
    }
}

fn zero_cells() -> [AtomicU64; DROP_CELLS] {
    std::array::from_fn(|_| AtomicU64::new(0))
}

fn zero_levels() -> [AtomicU64; LEVELS] {
    std::array::from_fn(|_| AtomicU64::new(0))
}

fn runtime_slot() -> &'static Mutex<Option<Runtime>> {
    static SLOT: Mutex<Option<Runtime>> = Mutex::new(None);
    &SLOT
}

fn lock_slot() -> MutexGuard<'static, Option<Runtime>> {
    runtime_slot()
        .lock()
        .unwrap_or_else(|poison| poison.into_inner())
}

fn wipe(bytes: &mut [u8]) {
    for byte in bytes.iter_mut() {
        *byte = 0;
    }
    std::sync::atomic::compiler_fence(Ordering::SeqCst);
    std::hint::black_box(bytes);
}

/// Copies the key under its ownership lock, hashes outside the lock, and wipes
/// the temporary copy. A frozen/unavailable runtime cannot issue new tags.
pub(crate) fn path_reference_tag(native: &[u8]) -> Option<[u8; 16]> {
    let mut key = {
        let slot = lock_slot();
        if PHASE.load(Ordering::Acquire) != RUNNING {
            return None;
        }
        slot.as_ref()?.key
    };
    let tag = crate::hmac::path_tag(&key, native);
    wipe(&mut key);
    Some(tag)
}

/// Two halves become the path key, or the partial key is wiped and logging stays unavailable.
pub(crate) fn key_from_halves(
    first: Result<[u8; 16], EntropyError>,
    second: Result<[u8; 16], EntropyError>,
) -> Result<[u8; 32], LoggingUnavailable> {
    let mut key = [0u8; 32];
    let mut first = match first {
        Ok(bytes) => bytes,
        Err(_) => return Err(LoggingUnavailable),
    };
    key[..16].copy_from_slice(&first);
    let mut second = match second {
        Ok(bytes) => bytes,
        Err(_) => {
            wipe(&mut first);
            wipe(&mut key);
            return Err(LoggingUnavailable);
        }
    };
    key[16..].copy_from_slice(&second);
    wipe(&mut first);
    wipe(&mut second);
    Ok(key)
}

fn draw_key() -> Result<[u8; 32], LoggingUnavailable> {
    let first = match request_entropy() {
        Ok(bytes) => bytes,
        Err(_) => return Err(LoggingUnavailable),
    };
    key_from_halves(Ok(first), request_entropy())
}

/// Once per process. `None` is a second call. `Some(Err)` is unavailable logging:
/// logging is disabled and no summary is frozen.
pub fn start() -> Option<Result<CapabilitySet, LoggingUnavailable>> {
    if PHASE
        .compare_exchange(IDLE, STARTING, Ordering::AcqRel, Ordering::Acquire)
        .is_err()
    {
        return None;
    }
    if crate::kinds::registry::Platform::compiled().is_none() {
        PHASE.store(UNAVAILABLE, Ordering::Release);
        return Some(Err(LoggingUnavailable));
    }
    let mut key = match draw_key() {
        Ok(key) => key,
        Err(error) => {
            PHASE.store(UNAVAILABLE, Ordering::Release);
            return Some(Err(error));
        }
    };
    let runtime = Runtime::new(key);
    wipe(&mut key);
    let runtime = match runtime {
        Ok(runtime) => runtime,
        Err(error) => {
            PHASE.store(UNAVAILABLE, Ordering::Release);
            return Some(Err(error));
        }
    };
    *lock_slot() = Some(runtime);
    PHASE.store(RUNNING, Ordering::Release);
    Some(Ok(CapabilitySet::issue()))
}

/// Start for an owning request, admitting its harness opening record before
/// any ordinary producer can enqueue on that sink.
pub fn start_for_request(
    scope: crate::scope::RequestScope,
) -> Option<Result<CapabilitySet, LoggingUnavailable>> {
    let result = start();
    #[cfg(feature = "harness-instrumentation")]
    if let Some(Ok(set)) = result.as_ref() {
        open_harness(scope, set);
    }
    #[cfg(not(feature = "harness-instrumentation"))]
    let _scope = scope;
    result
}

#[cfg(feature = "harness-instrumentation")]
fn open_harness(scope: crate::scope::RequestScope, set: &CapabilitySet) {
    use crate::kinds::registry::{Event, LogStreamOpened};
    let sink = {
        let slot = lock_slot();
        slot.as_ref().and_then(|runtime| runtime.harness.clone())
    };
    let Some(sink) = sink else {
        return;
    };
    if !sink.begin_opening() {
        return;
    }
    let Some(flight) = InFlightGuard::enter() else {
        return;
    };
    flight.armed();
    if !admission_is_open() {
        add_drop(REASON_DRAIN_ABANDONED, Level::Info);
        return;
    }
    if !take_budget(scope.request().bytes(), 3) {
        add_drop(REASON_BUDGET, Level::Info);
        return;
    }
    let Some(reservation) = sink.reserve_opening(LogStreamOpened::MAX_LINE) else {
        add_drop(REASON_QUEUE_FULL, Level::Info);
        return;
    };
    let record = set
        .process_id_mint()
        .pid(std::process::id())
        .and_then(|pid| crate::emit::encode_harness_opened(scope, pid));
    let Some(record) = record.filter(|record| record.bytes().len() <= LogStreamOpened::MAX_LINE)
    else {
        add_drop(REASON_REFUSED, Level::Info);
        return;
    };
    {
        let slot = lock_slot();
        let Some(runtime) = slot.as_ref() else {
            return;
        };
        if runtime.frozen.is_some() || !runtime.enqueue_open.load(Ordering::Acquire) {
            return;
        }
        sink.source_increment(scope.request(), Level::Info);
    }
    sink.push(record, reservation, Level::Info);
    sink.finish_opening();
}

pub(crate) struct SettleView {
    pub(crate) in_flight: Arc<AtomicU64>,
    #[cfg(feature = "operability-dev-sinks")]
    pub(crate) stderr: Arc<crate::dev_writer::DevSink>,
    #[cfg(feature = "harness-instrumentation")]
    pub(crate) harness: Option<Arc<crate::harness_writer::HarnessSink>>,
}
impl SettleView {
    fn from_runtime(runtime: &Runtime) -> Self {
        Self {
            in_flight: Arc::clone(&runtime.in_flight),
            #[cfg(feature = "operability-dev-sinks")]
            stderr: Arc::clone(&runtime.stderr),
            #[cfg(feature = "harness-instrumentation")]
            harness: runtime.harness.clone(),
        }
    }
    fn settled(&self) -> bool {
        if self.in_flight.load(Ordering::Acquire) != 0 {
            return false;
        }
        #[cfg(feature = "operability-dev-sinks")]
        if !self.stderr.settled() {
            return false;
        }
        #[cfg(feature = "harness-instrumentation")]
        if self.harness.as_ref().is_some_and(|sink| !sink.settled()) {
            return false;
        }
        true
    }
}

/// Poll owning atomics/snapshots without taking the runtime slot lock. This
/// absolute deadline is never restarted by a pending record or marker.
pub(crate) fn wait_for_settle(view: &SettleView, deadline: Instant) -> bool {
    if view.settled() {
        return false;
    }
    while !view.settled() {
        let remaining = deadline.saturating_duration_since(Instant::now());
        if remaining.is_zero() {
            break;
        }
        std::thread::sleep(remaining.min(Duration::from_millis(1)));
    }
    true
}

fn load_cells<const N: usize>(cells: &[AtomicU64; N]) -> [u64; N] {
    std::array::from_fn(|index| cells[index].load(Ordering::Acquire))
}

fn derive(runtime: &Runtime) -> FrozenSummary {
    // Step 4's read order: in-flight, file-admitted, snapshots, enqueue tallies, drop tallies.
    let in_flight_at_freeze = runtime.in_flight.load(Ordering::Acquire);
    let file_admitted = runtime.file_admitted.load(Ordering::Acquire);
    // The file writer has no snapshot. The development stderr snapshot is loaded
    // here, before the enqueue tallies and the producer drop tallies.
    let file_snapshot = crate::file_partition::FileSnapshot::default();
    #[cfg(feature = "operability-dev-sinks")]
    let stderr_snapshot = runtime.stderr.cell.load();
    #[cfg(not(feature = "operability-dev-sinks"))]
    let stderr_snapshot = crate::writer::Outcomes::default();
    #[cfg(feature = "harness-instrumentation")]
    let harness_snapshot = runtime
        .harness
        .as_ref()
        .map(|sink| sink.cell.load())
        .unwrap_or_default();
    #[cfg(not(feature = "harness-instrumentation"))]
    let harness_snapshot = crate::writer::Outcomes::default();
    #[cfg(feature = "harness-instrumentation")]
    let harness_enqueued = runtime
        .harness
        .as_ref()
        .map(|sink| sink.enqueued())
        .unwrap_or([0; LEVELS]);
    #[cfg(not(feature = "harness-instrumentation"))]
    let harness_enqueued = [0u64; LEVELS];
    #[cfg(feature = "operability-dev-sinks")]
    let stderr_enqueued = runtime.stderr.enqueued();
    #[cfg(not(feature = "operability-dev-sinks"))]
    let stderr_enqueued = [0u64; LEVELS];
    let enqueued = load_cells(&runtime.pre_scope_enqueued);
    let drops = load_cells(&runtime.drops);
    #[cfg(feature = "operability-dev-sinks")]
    let stderr_marker = Some(runtime.stderr.marker.freeze());
    #[cfg(not(feature = "operability-dev-sinks"))]
    let stderr_marker = None;
    #[cfg(feature = "harness-instrumentation")]
    let harness_marker = runtime.harness.as_ref().map(|sink| sink.marker.freeze());
    #[cfg(not(feature = "harness-instrumentation"))]
    let harness_marker = None;
    let harness_admitted = harness_marker.is_some();
    let harness_abandoned = std::array::from_fn(|index| {
        harness_enqueued[index].saturating_sub(
            harness_snapshot.written[index]
                .saturating_add(harness_snapshot.failed[index])
                .saturating_add(harness_snapshot.stopped[index]),
        )
    });
    let stderr_abandoned = std::array::from_fn(|index| {
        stderr_enqueued[index].saturating_sub(
            stderr_snapshot.written[index]
                .saturating_add(stderr_snapshot.failed[index])
                .saturating_add(stderr_snapshot.stopped[index]),
        )
    });
    // No file writer is admitted before S-OP-1. The C-7 stand-in uses
    // the same partition derivation with actual committed transfer snapshots.
    let file = crate::file_partition::derive(file_admitted, enqueued, [0; LEVELS], &file_snapshot);
    FrozenSummary {
        in_flight_at_freeze,
        file_admitted,
        unpersisted: file.unpersisted,
        drain_abandoned: file.abandoned,
        written: file.written,
        stderr_written: stderr_snapshot.written,
        stderr_failed: stderr_snapshot.failed,
        stderr_stopped: stderr_snapshot.stopped,
        stderr_error: stderr_snapshot.first_error,
        stderr_abandoned,
        stderr_marker,
        harness_admitted,
        harness_written: harness_snapshot.written,
        harness_failed: harness_snapshot.failed,
        harness_stopped: harness_snapshot.stopped,
        harness_error: harness_snapshot.first_error,
        harness_abandoned,
        harness_marker,
        drops,
    }
}

/// Steps 1 to 5. Idle, unavailable and a second call do nothing.
/// A runtime that is already settled does not sleep. The deadline is still recorded.
pub fn finalize(cancelled: bool) {
    let deadline_ms = if cancelled {
        FINALIZE_CANCEL_MS
    } else {
        FINALIZE_NORMAL_MS
    };
    let deadline = Instant::now() + Duration::from_millis(deadline_ms);
    if PHASE
        .compare_exchange(RUNNING, FINALIZING, Ordering::AcqRel, Ordering::Acquire)
        .is_err()
    {
        return;
    }
    let view = {
        let slot = lock_slot();
        let Some(runtime) = slot.as_ref() else {
            PHASE.store(FROZEN, Ordering::Release);
            return;
        };
        // 1. Cutoff. The settle wait does not hold this lock.
        runtime.admission_open.store(false, Ordering::Release);
        #[cfg(feature = "operability-dev-sinks")]
        runtime.stderr.begin_finalize(deadline);
        #[cfg(feature = "harness-instrumentation")]
        if let Some(sink) = runtime.harness.as_ref() {
            sink.begin_finalize(deadline);
        }
        SettleView::from_runtime(runtime)
    };
    // 2. Settle. Skip the wait when in-flight is already zero and no writer is admitted.
    let _waited = wait_for_settle(&view, deadline);
    let mut slot = lock_slot();
    let Some(runtime) = slot.as_mut() else {
        PHASE.store(FROZEN, Ordering::Release);
        return;
    };
    // 3. Close syscall admission, then enqueue. Already admitted residuals
    // belong to the writer; no join or ownership lock waits for their I/O.
    #[cfg(feature = "operability-dev-sinks")]
    runtime.stderr.gate.store(false, Ordering::Release);
    #[cfg(feature = "harness-instrumentation")]
    if let Some(sink) = runtime.harness.as_ref() {
        sink.gate.store(false, Ordering::Release);
    }
    runtime.enqueue_open.store(false, Ordering::Release);
    // 4 and 5. Read, derive, freeze.
    let summary = derive(runtime);
    wipe(&mut runtime.key);
    runtime.frozen = Some(Frozen {
        summary,
        #[cfg(test)]
        deadline_ms,
        #[cfg(test)]
        waited: _waited,
    });
    PHASE.store(FROZEN, Ordering::Release);
}

/// The carrier receives only this immutable frozen copy. Before successful
/// finalization, or when logging is unavailable, no summary exists.
pub fn frozen_summary() -> Option<FrozenSummary> {
    let slot = lock_slot();
    slot.as_ref()?.frozen.as_ref().map(|frozen| frozen.summary)
}

fn file_level_admits(level: Level) -> bool {
    level.index() <= Level::Info.index()
}

fn stderr_admits(level: Level) -> bool {
    cfg!(feature = "operability-dev-sinks") && level.index() <= Level::Debug.index()
}

fn any_sink_admits(level: Level) -> bool {
    // Featureless build: file and ring at info and above. Debug and trace match no sink.
    // The development feature adds stderr at debug and above.
    file_level_admits(level) || level.admits_ring() || stderr_admits(level)
}

fn saturating_increment(cell: &AtomicU64) {
    cell.fetch_update(Ordering::AcqRel, Ordering::Acquire, |value| {
        Some(value.saturating_add(1))
    })
    .unwrap_or_else(|value| value);
}

fn add_drop(reason: usize, level: Level) {
    #[cfg(test)]
    producer_tests::pause(producer_tests::Point::BeforeDrop);
    let slot = lock_slot();
    let Some(runtime) = slot.as_ref() else {
        return;
    };
    let cell = loss_cell_index(reason, level);
    // The slot lock serializes this commit with the ordered freeze reads.
    // A call paused before its drop cannot alter authoritative cells later.
    let cells = if runtime.frozen.is_some() {
        &runtime.post_freeze_drops
    } else {
        &*runtime.drops
    };
    saturating_increment(&cells[cell]);
}

fn add_post_freeze(level: Level) {
    let slot = lock_slot();
    let Some(runtime) = slot.as_ref() else {
        return;
    };
    let cell = loss_cell_index(REASON_DRAIN_ABANDONED, level);
    saturating_increment(&runtime.post_freeze_drops[cell]);
}

struct InFlightGuard;

impl InFlightGuard {
    fn enter() -> Option<Self> {
        let slot = lock_slot();
        let runtime = slot.as_ref()?;
        runtime.in_flight.fetch_add(1, Ordering::AcqRel);
        Some(Self)
    }

    fn armed(&self) {}
}

impl Drop for InFlightGuard {
    fn drop(&mut self) {
        let slot = lock_slot();
        let Some(runtime) = slot.as_ref() else {
            return;
        };
        runtime.in_flight.fetch_sub(1, Ordering::AcqRel);
    }
}

struct PrescopeHold {
    bytes: usize,
}

impl PrescopeHold {
    fn reserve(bytes: usize) -> Option<Self> {
        let slot = lock_slot();
        let runtime = slot.as_ref()?;
        let mut buffer = runtime
            .pre_scope
            .lock()
            .unwrap_or_else(|poison| poison.into_inner());
        if buffer.try_reserve(bytes) {
            Some(Self { bytes })
        } else {
            None
        }
    }

    fn commit(self, record: &crate::guard::SealedRecord) {
        let committed = {
            let slot = lock_slot();
            if let Some(runtime) = slot.as_ref() {
                let mut buffer = runtime
                    .pre_scope
                    .lock()
                    .unwrap_or_else(|poison| poison.into_inner());
                if runtime.enqueue_open.load(Ordering::Acquire)
                    && record.inspect().is_ok_and(crate::guard::Assessment::lawful)
                {
                    buffer.finish_reserve(self.bytes, record.bytes());
                } else {
                    // Already source-enqueued: no producer drop. With no file
                    // capability this unit remains unpersisted at the freeze.
                    buffer.release_reserve(self.bytes);
                }
                true
            } else {
                false
            }
        };
        if committed {
            std::mem::forget(self);
        }
    }
}

impl Drop for PrescopeHold {
    fn drop(&mut self) {
        let slot = lock_slot();
        let Some(runtime) = slot.as_ref() else {
            return;
        };
        let mut buffer = runtime
            .pre_scope
            .lock()
            .unwrap_or_else(|poison| poison.into_inner());
        buffer.release_reserve(self.bytes);
    }
}

fn admission_is_open() -> bool {
    let slot = lock_slot();
    slot.as_ref()
        .is_some_and(|runtime| runtime.admission_open.load(Ordering::Acquire))
}

fn enqueue_is_open() -> bool {
    let slot = lock_slot();
    slot.as_ref()
        .is_some_and(|runtime| runtime.enqueue_open.load(Ordering::Acquire))
}

fn file_is_admitted() -> bool {
    let slot = lock_slot();
    slot.as_ref()
        .is_some_and(|runtime| runtime.file_admitted.load(Ordering::Acquire))
}

fn take_budget(request: [u8; 16], event: usize) -> bool {
    let slot = lock_slot();
    let Some(runtime) = slot.as_ref() else {
        return false;
    };
    let mut budget = runtime
        .budget
        .lock()
        .unwrap_or_else(|poison| poison.into_inner());
    budget.try_take(request, event)
}

fn push_ring(record: &crate::guard::SealedRecord) {
    let slot = lock_slot();
    let Some(runtime) = slot.as_ref() else {
        return;
    };
    let mut ring = runtime
        .ring
        .lock()
        .unwrap_or_else(|poison| poison.into_inner());
    // A ring refusal has neither a source nor a loss tally.
    if runtime.enqueue_open.load(Ordering::Acquire)
        && record.inspect().is_ok_and(crate::guard::Assessment::lawful)
    {
        ring.push_overwrite(record.bytes());
    }
}

/// Level filter, per-name budget, reservation, then encoding, then the enqueue
/// increment before the push. The clock read happens with no lock held.
/// `encode` returns the file line (ceiling P2), the ring line (ceiling P1),
/// and the human stderr line.
pub(crate) fn produce(
    level: Level,
    event_slot: usize,
    request: crate::scope::RequestId,
    max_line: usize,
    encode: &dyn Fn() -> Option<crate::guard::ProjectedRecords>,
) {
    if !any_sink_admits(level) {
        return;
    }
    let phase = PHASE.load(Ordering::Acquire);
    if phase == FROZEN {
        add_post_freeze(level);
        return;
    }
    if phase != RUNNING && phase != FINALIZING {
        return;
    }
    let flight = match InFlightGuard::enter() {
        Some(guard) => guard,
        None => return,
    };
    flight.armed();
    if phase != RUNNING || !admission_is_open() {
        add_drop(REASON_DRAIN_ABANDONED, level);
        return;
    }
    if event_slot >= BUDGET_EVENTS {
        add_drop(REASON_REFUSED, level);
        return;
    }
    if !take_budget(request.bytes(), event_slot) {
        add_drop(REASON_BUDGET, level);
        return;
    }
    // One read of the file-admitted flag. This build never sets it, so the
    // direct queue is absent and a set flag is queue-full.
    if file_level_admits(level) && file_is_admitted() {
        add_drop(REASON_QUEUE_FULL, level);
        return;
    }
    let hold = if file_level_admits(level) {
        match PrescopeHold::reserve(max_line) {
            Some(hold) => Some(hold),
            None => {
                add_drop(REASON_PRESCOPE_FULL, level);
                return;
            }
        }
    } else {
        None
    };
    #[cfg(feature = "operability-dev-sinks")]
    let dev_hold = if stderr_admits(level) {
        let sink = {
            let slot = lock_slot();
            let Some(runtime) = slot.as_ref() else {
                return;
            };
            Arc::clone(&runtime.stderr)
        };
        let Some(reservation) = sink.reserve(max_line, level) else {
            add_drop(REASON_QUEUE_FULL, level);
            return;
        };
        Some((sink, reservation))
    } else {
        None
    };
    #[cfg(feature = "harness-instrumentation")]
    let harness_hold = if level.admits_ring() {
        let sink = {
            let slot = lock_slot();
            slot.as_ref().and_then(|runtime| runtime.harness.clone())
        };
        if let Some(sink) = sink {
            if !sink.opened() {
                add_drop(REASON_REFUSED, level);
                return;
            }
            let Some(reservation) = sink.reserve(max_line, level) else {
                add_drop(REASON_QUEUE_FULL, level);
                return;
            };
            Some((sink, reservation))
        } else {
            None
        }
    } else {
        None
    };
    let Some(records) = encode() else {
        add_drop(REASON_REFUSED, level);
        return;
    };
    if max_line > MAX_LINE
        || !records.lawful()
        || records.file.bytes().len() > max_line
        || records.human.bytes().len() > max_line
        || records
            .ring
            .as_ref()
            .is_some_and(|record| record.bytes().len() > max_line)
        || (level.admits_ring() && records.ring.is_none())
    {
        add_drop(REASON_REFUSED, level);
        return;
    }
    if !enqueue_is_open() {
        add_drop(REASON_DRAIN_ABANDONED, level);
        return;
    }
    // Every source increment precedes every push. Each commit is serialized
    // with the freeze; no ownership lock spans a test pause or any I/O.
    if hold.is_some() {
        let slot = lock_slot();
        let Some(runtime) = slot.as_ref() else {
            return;
        };
        let cells = if runtime.frozen.is_some() {
            &runtime.post_freeze_sources
        } else {
            &runtime.pre_scope_enqueued
        };
        saturating_increment(&cells[level.index()]);
    }
    #[cfg(test)]
    producer_tests::pause(producer_tests::Point::AfterFirstSource);
    #[cfg(feature = "operability-dev-sinks")]
    if let Some((sink, _)) = dev_hold.as_ref() {
        let slot = lock_slot();
        let Some(runtime) = slot.as_ref() else {
            return;
        };
        if runtime.frozen.is_some() {
            saturating_increment(&runtime.post_freeze_sources[level.index()]);
        } else {
            sink.source_increment(request, level);
        }
    }
    #[cfg(feature = "harness-instrumentation")]
    if let Some((sink, _)) = harness_hold.as_ref() {
        let slot = lock_slot();
        let Some(runtime) = slot.as_ref() else {
            return;
        };
        if runtime.frozen.is_some() {
            saturating_increment(&runtime.post_freeze_sources[level.index()]);
        } else {
            sink.source_increment(request, level);
        }
    }
    #[cfg(test)]
    producer_tests::pause(producer_tests::Point::BeforePush);
    if let Some(hold) = hold {
        hold.commit(&records.file);
    }
    if level.admits_ring()
        && let Some(record) = records.ring.as_ref()
    {
        push_ring(record);
    }
    #[cfg(feature = "operability-dev-sinks")]
    if let Some((sink, reservation)) = dev_hold {
        sink.push(records.human, reservation, level);
    }
    #[cfg(feature = "harness-instrumentation")]
    if let Some((sink, reservation)) = harness_hold
        && let Some(record) = records.ring
    {
        sink.push(record, reservation, level);
    }
}

#[cfg(test)]
pub(crate) struct FreezeView {
    pub(crate) summary: FrozenSummary,
    pub(crate) deadline_ms: u64,
    pub(crate) waited: bool,
    pub(crate) key_wiped: bool,
    pub(crate) admission_open: bool,
    pub(crate) enqueue_open: bool,
    pub(crate) post_freeze: [u64; DROP_CELLS],
    pub(crate) post_freeze_sources: [u64; LEVELS],
    pub(crate) pre_scope_bytes: usize,
    pub(crate) pre_scope_records: usize,
    pub(crate) ring_bytes: usize,
    pub(crate) ring_records: usize,
    pub(crate) pre_scope_stored: usize,
    pub(crate) ring_stored: usize,
    pub(crate) buffers_empty: bool,
}

#[cfg(test)]
pub(crate) fn freeze_view() -> Option<FreezeView> {
    if PHASE.load(Ordering::Acquire) != FROZEN {
        return None;
    }
    let slot = lock_slot();
    let runtime = slot.as_ref()?;
    let frozen = runtime.frozen.as_ref()?;
    let pre_scope = runtime
        .pre_scope
        .lock()
        .unwrap_or_else(|poison| poison.into_inner());
    let ring = runtime
        .ring
        .lock()
        .unwrap_or_else(|poison| poison.into_inner());
    let key_wiped = runtime.key.iter().all(|byte| *byte == 0);
    Some(FreezeView {
        summary: frozen.summary,
        deadline_ms: frozen.deadline_ms,
        waited: frozen.waited,
        key_wiped,
        admission_open: runtime.admission_open.load(Ordering::Acquire),
        enqueue_open: runtime.enqueue_open.load(Ordering::Acquire),
        post_freeze: load_cells(&runtime.post_freeze_drops),
        post_freeze_sources: load_cells(&runtime.post_freeze_sources),
        pre_scope_bytes: pre_scope.capacity_bytes(),
        pre_scope_records: pre_scope.capacity_records(),
        ring_bytes: ring.capacity_bytes(),
        ring_records: ring.capacity_records(),
        pre_scope_stored: pre_scope.stored_count(),
        ring_stored: ring.stored_count(),
        buffers_empty: pre_scope.is_empty()
            && ring.is_empty()
            && pre_scope.memory_len() == pre_scope.capacity_bytes()
            && ring.memory_len() == ring.capacity_bytes(),
    })
}

#[cfg(test)]
fn copy_first(buffer_is_ring: bool) -> Option<Vec<u8>> {
    let slot = lock_slot();
    let runtime = slot.as_ref()?;
    let buffer = if buffer_is_ring {
        runtime
            .ring
            .lock()
            .unwrap_or_else(|poison| poison.into_inner())
    } else {
        runtime
            .pre_scope
            .lock()
            .unwrap_or_else(|poison| poison.into_inner())
    };
    buffer.first().map(|bytes| bytes.to_vec())
}

#[cfg(test)]
pub(crate) fn pre_scope_first() -> Option<Vec<u8>> {
    copy_first(false)
}

#[cfg(test)]
pub(crate) fn ring_first() -> Option<Vec<u8>> {
    copy_first(true)
}

#[cfg(test)]
pub(crate) fn buffers_contain(needle: &[u8]) -> (bool, bool) {
    let slot = lock_slot();
    let Some(runtime) = slot.as_ref() else {
        return (false, false);
    };
    let pre_scope = runtime
        .pre_scope
        .lock()
        .unwrap_or_else(|poison| poison.into_inner());
    let ring = runtime
        .ring
        .lock()
        .unwrap_or_else(|poison| poison.into_inner());
    (pre_scope.contains(needle), ring.contains(needle))
}

#[cfg(test)]
mod tests {
    use super::{
        DROP_CELLS, FINALIZE_NORMAL_MS, LEVELS, LoggingUnavailable, REASON_DRAIN_ABANDONED,
        buffers_contain, finalize, freeze_view, key_from_halves, pre_scope_first, ring_first,
        start,
    };
    use crate::constants::{
        Level, PRE_SCOPE_BYTES, PRE_SCOPE_RECORDS, RING_BYTES, RING_RECORDS, loss_cell_index,
    };
    use crate::emit::EmitOn;
    use crate::kinds::Code;
    use crate::kinds::registry::{HostRepairCompleted, RepairKind, RepairState};
    use opensip_platform::EntropyError;

    #[test]
    fn a_failed_half_does_not_return_a_key() {
        let first_failed = key_from_halves(Err(EntropyError), Ok([9; 16]));
        assert!(matches!(first_failed, Err(LoggingUnavailable)));
        let second_failed = key_from_halves(Ok([9; 16]), Err(EntropyError));
        assert!(matches!(second_failed, Err(LoggingUnavailable)));
        let key = key_from_halves(Ok([1; 16]), Ok([2; 16])).expect("two halves");
        assert_eq!(&key[..16], &[1; 16]);
        assert_eq!(&key[16..], &[2; 16]);
        assert_eq!(key.len(), 32);
    }

    #[test]
    fn start_once_then_one_info_record_is_unpersisted() {
        let set = match start() {
            Some(Ok(set)) => set,
            Some(Err(LoggingUnavailable)) => panic!("entropy failed"),
            None => panic!("start refused the first call"),
        };
        let request = set.request_scope([0xab; 16]);
        assert_eq!(
            &request.request().text()[5..],
            b"abababababababababababababababab"
        );
        let project = set.project_scope(request, [0x02; 32]);
        assert_eq!(&project.project().text()[..5], b"prj1-");
        let repair = HostRepairCompleted::new(
            Code::from_enum(RepairKind::Registration),
            Code::from_enum(RepairState::RwT3),
        );
        repair.emit(request);
        assert!(start().is_none());
        finalize(false);
        let view = freeze_view().expect("frozen summary");
        assert_eq!(view.deadline_ms, FINALIZE_NORMAL_MS);
        #[cfg(not(feature = "operability-dev-sinks"))]
        assert!(!view.waited);
        #[cfg(feature = "operability-dev-sinks")]
        std::hint::black_box(view.waited);
        assert!(view.key_wiped);
        assert!(!view.admission_open);
        assert!(!view.enqueue_open);
        assert_eq!(view.summary.in_flight_at_freeze, 0);
        assert!(!view.summary.file_admitted);
        let mut unpersisted = [0u64; LEVELS];
        unpersisted[Level::Info.index()] = 1;
        assert_eq!(view.summary.unpersisted, unpersisted);
        assert_eq!(view.summary.drain_abandoned, [0; LEVELS]);
        assert_eq!(view.summary.written, [0; LEVELS]);
        #[cfg(not(feature = "operability-dev-sinks"))]
        {
            assert_eq!(view.summary.stderr_written, [0; LEVELS]);
            assert_eq!(view.summary.stderr_failed, [0; LEVELS]);
            assert_eq!(view.summary.stderr_abandoned, [0; LEVELS]);
        }
        #[cfg(feature = "operability-dev-sinks")]
        {
            let mut stderr_written = [0u64; LEVELS];
            stderr_written[Level::Info.index()] = 1;
            assert_eq!(view.summary.stderr_written, stderr_written);
            assert_eq!(view.summary.stderr_failed, [0; LEVELS]);
            assert_eq!(view.summary.stderr_abandoned, [0; LEVELS]);
        }
        assert_eq!(view.summary.drops, [0; DROP_CELLS]);
        assert_eq!(view.post_freeze, [0; DROP_CELLS]);
        assert!(!view.buffers_empty);
        assert_eq!(view.pre_scope_stored, 1);
        assert_eq!(view.ring_stored, 1);
        assert_eq!(view.pre_scope_bytes, PRE_SCOPE_BYTES);
        assert_eq!(view.pre_scope_records, PRE_SCOPE_RECORDS);
        assert_eq!(view.ring_bytes, RING_BYTES);
        assert_eq!(view.ring_records, RING_RECORDS);
        let line = pre_scope_first().expect("pre-scope record");
        let ring = ring_first().expect("ring record");
        assert_eq!(line, ring);
        let (pre_has, ring_has) = buffers_contain(b"host.repair.completed");
        assert!(pre_has);
        assert!(ring_has);
        assert!(line.ends_with(b"\n"));
        assert_eq!(&line[..7], br#"{"ts":""#);
        let ts = &line[7..31];
        assert_eq!(ts.len(), 24);
        assert_eq!(ts[4], b'-');
        assert_eq!(ts[7], b'-');
        assert_eq!(ts[10], b'T');
        assert_eq!(ts[13], b':');
        assert_eq!(ts[16], b':');
        assert_eq!(ts[19], b'.');
        assert_eq!(ts[23], b'Z');
        assert!(
            line.windows(21)
                .any(|window| window == b"host.repair.completed")
        );
        assert!(line.windows(14).any(|window| window == b"\"registration\""));
        assert!(line.windows(7).any(|window| window == b"\"RW-T3\""));
        assert!(
            line.windows(37)
                .any(|window| window == b"req1_abababababababababababababababab")
        );
        assert!(
            line.windows(14)
                .any(|window| window == br#""level":"info""#)
        );
        assert!(!line.windows(9).any(|window| window == b"projectId"));
        assert!(!line.windows(7).any(|window| window == b"omitted"));
        assert!(!line.windows(9).any(|window| window == b"truncated"));
        let late = HostRepairCompleted::new(
            Code::from_enum(RepairKind::Registration),
            Code::from_enum(RepairState::RwT3),
        );
        late.emit(request);
        let again = freeze_view().expect("summary stays frozen");
        assert_eq!(again.summary, view.summary);
        assert_eq!(again.pre_scope_stored, 1);
        assert_eq!(again.ring_stored, 1);
        let mut post_freeze = [0u64; DROP_CELLS];
        post_freeze[loss_cell_index(REASON_DRAIN_ABANDONED, Level::Info)] = 1;
        assert_eq!(again.post_freeze, post_freeze);
        finalize(true);
        let stayed = freeze_view().expect("second finalize is a no-op");
        assert_eq!(stayed.summary, view.summary);
        assert_eq!(stayed.deadline_ms, FINALIZE_NORMAL_MS);
        assert_eq!(stayed.post_freeze, post_freeze);
        assert!(start().is_none());
    }
}

#[cfg(test)]
#[path = "producer_tests.rs"]
mod producer_tests;
