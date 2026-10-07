//! Law X3d r6 (unit X3d-2): storage's commit facade, the one way an
//! authoritative commit is published. It composes security's `CommitSession`
//! (X3d-1), the evaluator's opaque `ReplayedRun` and X3c's ledger and object
//! owners (X3c-1 and X3c-2):
//! - [`prepare_commit`] is item 3: the end-path reserve first (step 0,
//!   security's step), the binding of the replay to the session (step 1), the
//!   carrier's capacity (step 3, security's `seal_fits`), the store's
//!   directories and ledger, then attempt admission and the objects (steps 4
//!   to 6) drawn from one publication reserve (step 2);
//! - [`PreparedCommit::publish`] is item 4: the journal's level 3, the
//!   evidence ledger's level 3, then security's `seal_under_append_lock` with
//!   this module's private two-phase adapter, which stages the exact receipt,
//!   the thirteen-field association and the Run material after the durable
//!   `SEAL`, with the initial availability and the (empty) pin set on the
//!   Run's first commit in its store and namespace only (X3c r8: a re-commit
//!   of an already-committed Run stages neither), and whose one consuming
//!   method performs only the evidence `COMMIT`;
//! - [`PublishedCommit`] exists only after that `COMMIT` returned success.
//!
//! Storage holds no settlement reserve, mints no security type, accepts no
//! external adapter or `SealOutcome`, never calls lifecycle, never reads an
//! outcome back and never retries. Every outcome comes with the session's
//! `StoppedSession`, which the caller must finish (item 7). Library only: no
//! command commits.
use crate::availability::AvailabilityRecord;
use crate::ledger_store::{
    AdmittedAttempt, AdmittedLedger, CommitRows, DeclaredObject, LedgerCommitOutcome,
    ObjectDirectory, PreparedLedger, PreparedLedgerCommit, ProjectLedgerRefusal, ProjectLedgerRow,
    ProjectStoreLocation, ProjectStoreNames, PublishedObjects, StagingLimits, admit_attempt,
    admit_namespace_directory, admit_object_directory, attempt_and_objects_cost,
    begin_prepared_ledger, create_or_open_ledger, h_digest, publish_objects,
};
use crate::ledger_store::{AttemptKey, AttemptPhase, AttemptRecord};
use crate::pin_inventory::Inventory;
use crate::recovery::{AssociationCandidate, ReceiptCandidate};
use opensip_evaluator::ReplayedRun;
use opensip_identity::{
    JsonInteger, JsonValue as V, RegisteredSchemas, canonical_bytes, digest_hex, raw_sha256,
};
use opensip_platform::{WorkBudgetError, WorkCost, WorkFailure, WorkScope};
use opensip_security::{
    CarrierCapacityExhausted, CommitAdapter, CommitSession, EvidenceCommit,
    InstallationTermination as T, JournalSealBinding, RequestedBinding, SealOutcome, SealRefusal,
    SessionRefusal, StagedCommit, StoppedSession, begin_journal_txn, seal_under_append_lock,
};

/// The receipt's immutable assurance: the default authoritative profile
/// requires replayable retention at seal (identity-and-evidence, "Sealed
/// assurance"), and the commit publishes every frame and blob the replay read.
const SEALED_ASSURANCE: &str = "replayable";
/// The receipt's `signerKeyId`. No receipt signing key exists in M2
/// (identity-and-evidence leaves authenticated receipt signing to
/// implementation qualification), so the receipt names that it is held under
/// local custody and signed by no key.
const RECEIPT_SIGNER: &str = "local-custody-unsigned";
/// Staging's parse bound per record (the platform's per-record bound), and the
/// pin read bounds: the commit declares no pins and admits a Run with none.
const STAGING_LIMITS: StagingLimits = StagingLimits {
    per_record_work: 4 << 20,
    pin_rows: 0,
    pin_text_bytes: 0,
};

// ----------------------------------------------------------------- outcomes

/// Item 6: what `publish` returns beside the `StoppedSession`.
#[derive(Debug)]
pub enum CommitOutcome {
    /// The evidence `COMMIT` returned success (F13).
    Committed(PublishedCommit),
    /// The evidence `COMMIT` errored or the connection was lost, or an
    /// uncertain journal commit or barrier stopped `publish` (F12, F40): the
    /// ExecutionId is retained, there is no RunId and nothing is retried.
    CommitUndetermined { execution_id: String },
    /// A certain refusal before a permit was used, on its item 9 row.
    Refused(T),
}

/// Item 6: what `prepare_commit` returns, beside the `StoppedSession`, when
/// it prepares nothing.
#[derive(Debug)]
pub enum NotPrepared {
    /// Item 3 step 3 (F32): no SEAL fits after the proven tail. Not a
    /// refusal: the attempt ledger stays open for the end step's rollover.
    CarrierCapacityExhausted(CarrierCapacityExhausted),
    /// Item 3 step 5 (F34): an attempt with this exact ExecutionId exists.
    /// Nothing further was written. Law X6 r3 item 6: it stays on the
    /// invariant row in this invocation, which discloses `requested`, the
    /// binding this attempt was about to write (from its plan, never a
    /// read); a later read-entry invocation recovers it with that binding.
    ExistingAttempt {
        execution_id: String,
        /// Boxed so the refusal side of `prepare_commit` stays small.
        requested: Box<RequestedBinding>,
    },
    /// Item 3 step 4: the attempt-admission `COMMIT` was undetermined.
    CommitUndetermined { execution_id: String },
    /// A certain refusal, on its item 9 row.
    Refused(T),
}

/// Item 1's `PublishedCommit`: the exact committed receipt and its Run, after
/// the evidence `COMMIT` returned success. Private fields; not Clone, Default
/// or serializable; only this module's commit path builds one.
pub struct PublishedCommit {
    receipt: Vec<u8>,
    run_id: String,
    execution_id: String,
    commit_sequence: u64,
    grant_generation: i64,
    seal_seq: i64,
    latched_after_admission: bool,
}
impl std::fmt::Debug for PublishedCommit {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("PublishedCommit")
            .field("run_id", &self.run_id)
            .field("execution_id", &self.execution_id)
            .field("commit_sequence", &self.commit_sequence)
            .field("latched_after_admission", &self.latched_after_admission)
            .finish_non_exhaustive()
    }
}
impl PublishedCommit {
    /// The exact committed receipt bytes.
    pub fn receipt(&self) -> &[u8] {
        &self.receipt
    }
    pub fn run_id(&self) -> &str {
        &self.run_id
    }
    pub fn execution_id(&self) -> &str {
        &self.execution_id
    }
    /// The receipt counter allocated to this commit in (store, N).
    pub fn commit_sequence(&self) -> u64 {
        self.commit_sequence
    }
    /// The SEAL's grant generation and sequence on N's carrier.
    pub fn journal_seal(&self) -> (i64, i64) {
        (self.grant_generation, self.seal_seq)
    }
    /// Item 5 (F39): a latch took the gate from admitted to latched after the
    /// permit. The commit stands; required delivery reports
    /// `DELIVERY.REQUIRED_FAILED` (X7).
    pub fn latched_after_admission(&self) -> bool {
        self.latched_after_admission
    }
}

// -------------------------------------------------------------------- plan

/// What the session binds, read through its getters.
struct Bound {
    project: String,
    /// Law X3d r8 item 3 step 1: the session's core evaluator closure (EC1).
    evaluator_closure: String,
    namespace: String,
    store: String,
    generation: i64,
    schema: u8,
    carrier: String,
    execution: String,
    operation: String,
}
impl Bound {
    fn of(session: &CommitSession) -> Self {
        Self {
            project: session.project_id().to_owned(),
            evaluator_closure: session.core_evaluator_closure().to_owned(),
            namespace: session.namespace_id().to_owned(),
            store: session.store_instance().to_owned(),
            generation: session.store_generation(),
            schema: session.state_schema(),
            carrier: session.carrier_digest().to_owned(),
            execution: session.execution_id().to_owned(),
            operation: session.operation_ref().to_owned(),
        }
    }
}

/// Everything the commit writes that the replay and the session fix, built
/// before any effect. Values only.
struct Planned {
    /// The selected schema registry the staging owners admit with, resolved
    /// here, before any lock, so that nothing compiles under level 4.
    schemas: &'static RegisteredSchemas,
    run_id: String,
    namespace: String,
    store: String,
    store_digest: String,
    carrier: String,
    execution: String,
    operation: String,
    manifest: Vec<u8>,
    inventory: Vec<u8>,
    inventory_digest: String,
}

/// Why the replay does not bind to the session (item 3 step 1), or cannot be
/// planned. Each is the invariant row: a broken caller, never a retry.
#[derive(Debug, PartialEq, Eq)]
enum PlanRefusal {
    /// The Run names another project (its target identity).
    Project,
    /// The replay's evaluator closure is not the session's core evaluator
    /// closure (law X3d r8; contract successor EC1).
    Closure,
    /// A retained frame is not its identity's H preimage, or a value has no
    /// canonical form.
    Material,
}

fn integer(n: i128) -> Option<V> {
    JsonInteger::new(n).ok().map(V::Integer)
}
fn text(s: &str) -> V {
    V::String(s.to_owned())
}
fn canonical(pairs: Vec<(&str, V)>) -> Option<Vec<u8>> {
    canonical_bytes(&V::Object(
        pairs.into_iter().map(|(k, v)| (k.to_owned(), v)).collect(),
    ))
    .ok()
}
fn sha256_hex(bytes: &[u8]) -> String {
    digest_hex(&raw_sha256(bytes))
}

/// Owner §8's `storeGenerationDigest`: raw SHA-256 over the canonical
/// five-member `StoreGenerationBindingV1` `{schemaVersion: 1, namespaceId,
/// storeInstanceId, storeGeneration, stateSchema}` (store-instance-lineage
/// v1's recipe; not a framed identity).
pub(crate) fn store_generation_digest(n: &str, s: &str, g: i64, k: u8) -> Option<String> {
    canonical(vec![
        ("schemaVersion", integer(1)?),
        ("namespaceId", text(n)),
        ("storeInstanceId", text(s)),
        ("storeGeneration", integer(g.into())?),
        ("stateSchema", integer(k.into())?),
    ])
    .map(|binding| sha256_hex(&binding))
}

/// Item 3 step 1 and the commit's values. The replay's Run must name the
/// session's project (its target identity) and its evaluator closure must be
/// the session's core evaluator closure (its producer selection; law X3d r8,
/// contract successor EC1), never its `kind: "core"` closure. Every
/// retained frame must be its identity's H preimage. The commit inventory
/// lists exactly the typed objects and raw blobs the replay retained, and
/// both are declared for publication: each frame under its H digest, each
/// blob under its raw digest (one CAS keyed by raw SHA-256).
fn plan(run: &ReplayedRun, bound: &Bound) -> Result<(Planned, Vec<DeclaredObject>), PlanRefusal> {
    let V::Object(descriptor) = run.run() else {
        return Err(PlanRefusal::Material);
    };
    if descriptor.get("projectId") != Some(&text(&bound.project)) {
        return Err(PlanRefusal::Project);
    }
    if run.evaluator_closure() != bound.evaluator_closure {
        return Err(PlanRefusal::Closure);
    }
    let evidence = run.retained_evidence();
    let mut declared = Vec::new();
    let mut digests = std::collections::BTreeSet::new();
    let mut objects = Vec::new();
    for (identity, frame) in evidence.object_frames() {
        let digest = raw_sha256(frame);
        if h_digest(identity) != Some(digest_hex(&digest).as_str()) {
            return Err(PlanRefusal::Material);
        }
        if digests.insert(digest) {
            declared.push(DeclaredObject::new(
                digest,
                frame.len() as u64,
                frame.clone(),
            ));
        }
        objects.push(text(identity));
    }
    let mut blobs = Vec::new();
    for (digest, bytes) in evidence.blobs() {
        if digests.insert(*digest) {
            declared.push(DeclaredObject::new(
                *digest,
                bytes.len() as u64,
                bytes.clone(),
            ));
        }
        blobs.push(text(&digest_hex(digest)));
    }
    let material = || PlanRefusal::Material;
    let manifest = canonical_bytes(run.run()).map_err(|_| material())?;
    let inventory = canonical(vec![
        ("schemaVersion", integer(2).ok_or_else(material)?),
        ("runId", text(run.run_id())),
        ("objects", V::Array(objects)),
        ("blobDigests", V::Array(blobs)),
    ])
    .ok_or_else(material)?;
    let store_digest = store_generation_digest(
        &bound.namespace,
        &bound.store,
        bound.generation,
        bound.schema,
    )
    .ok_or_else(material)?;
    let schemas = crate::schema_sources::registry().ok_or_else(material)?;
    Ok((
        Planned {
            schemas,
            run_id: run.run_id().to_owned(),
            namespace: bound.namespace.clone(),
            store: bound.store.clone(),
            store_digest,
            carrier: bound.carrier.clone(),
            execution: bound.execution.clone(),
            operation: bound.operation.clone(),
            inventory_digest: sha256_hex(&inventory),
            manifest,
            inventory,
        },
        declared,
    ))
}
/// The plan's charge: its in-memory work over the replay's retained bytes.
fn plan_cost(run: &ReplayedRun) -> WorkCost {
    let evidence = run.retained_evidence();
    let entries = evidence.object_frames().len() + evidence.blobs().len();
    WorkCost {
        objects: 1,
        edges: entries.saturating_add(4),
        bytes: evidence.byte_length().saturating_add(run.run_id().len()),
    }
}

/// Law X6 r3 item 2: the binding this attempt was about to write, from its
/// plan: the digest of (N, S, G, K), N, the carrier digest and the operation
/// reference. Every member was built or checked by the plan, so a refusal
/// here is a broken composition.
fn requested_binding(planned: &Planned) -> Option<RequestedBinding> {
    RequestedBinding::checked(
        &planned.store_digest,
        &planned.namespace,
        &planned.carrier,
        &planned.operation,
    )
    .ok()
}

/// X3c item 3's `admitted` attempt row for this session.
fn attempt_record(planned: &Planned) -> AttemptRecord {
    AttemptRecord {
        key: AttemptKey {
            store: planned.store_digest.clone(),
            namespace: planned.namespace.clone(),
            execution: planned.execution.clone(),
        },
        operation: planned.operation.clone(),
        phase: AttemptPhase::Admitted,
    }
}

// ---------------------------------------------------------------- the store

/// The admitted per-(S, N) layout X3c-1 makes or admits: `projects/N`,
/// `objects/sha256` and the ledger.
struct Layout {
    objects: ObjectDirectory,
    ledger: AdmittedLedger,
}
fn admit_layout(location: &ProjectStoreLocation<'_>, work: &mut WorkScope<'_>) -> Refused<Layout> {
    let namespace = admit_namespace_directory(location, work)?;
    let objects = admit_object_directory(location, &namespace, work)?;
    let ledger = create_or_open_ledger(location, &namespace, work)?;
    Ok(Layout { objects, ledger })
}
/// Item 3 steps 2, 4 and 6 (step 5 is attempt admission's no-replace
/// refusal): the publication reserve, exactly what attempt admission and the
/// objects charge, taken before the attempt row; both then draw only from it.
/// A reserve the ledger cannot take refuses on the budget row before the
/// attempt row is written.
fn admit_and_publish(
    location: &ProjectStoreLocation<'_>,
    layout: &Layout,
    record: &AttemptRecord,
    declared: Vec<DeclaredObject>,
    work: &mut WorkScope<'_>,
    open_window: Box<dyn FnOnce() + '_>,
) -> Refused<(AdmittedAttempt, PublishedObjects)> {
    let reserve = attempt_and_objects_cost(&declared)
        .ok_or(WorkFailure::Budget(WorkBudgetError::Arithmetic))?;
    work.effect(WorkCost::default(), reserve, |reserved| {
        reserved.prepaid(reserve, |work| {
            let attempt = admit_attempt(location, &layout.ledger, record, work)?;
            open_window();
            let objects = publish_objects(&attempt, &layout.objects, declared, work)?;
            Ok((attempt, objects))
        })
    })
}
type Refused<T> = Result<T, WorkFailure<ProjectLedgerRefusal>>;

// ------------------------------------------------------------------ rows

/// Item 9 for X3c's rows, through 468c's `InstallationTermination`.
fn ledger_row(row: ProjectLedgerRow) -> T {
    match row {
        ProjectLedgerRow::Busy => T::Busy,
        ProjectLedgerRow::LedgerCorrupt => T::LedgerCorrupt,
        ProjectLedgerRow::HostIo => T::HostIo,
        ProjectLedgerRow::DurabilityCommitFailed => T::CommitUndetermined,
        ProjectLedgerRow::Invariant => T::Invariant,
        ProjectLedgerRow::Custody(subject) => T::Custody { subject },
    }
}
pub(crate) fn ledger_failure(failure: &WorkFailure<ProjectLedgerRefusal>) -> T {
    match failure {
        WorkFailure::Budget(_) => T::BudgetExhausted,
        WorkFailure::Operation(refusal) => ledger_row(refusal.row()),
    }
}
fn session_failure(failure: &WorkFailure<SessionRefusal>) -> T {
    match failure {
        WorkFailure::Budget(_) => T::BudgetExhausted,
        WorkFailure::Operation(refusal) => refusal.termination(),
    }
}

// ------------------------------------------------------------ prepare_commit

/// Item 1's `PreparedCommit`: both prerequisites, the exact binding, the
/// admitted attempt and ledger, and the published objects. Private fields;
/// not Clone, Default or serializable; only `prepare_commit` makes one, and
/// `publish` consumes it.
pub struct PreparedCommit {
    run: ReplayedRun,
    session: CommitSession,
    ledger: AdmittedLedger,
    attempt: AdmittedAttempt,
    objects: PublishedObjects,
    planned: Planned,
}
impl std::fmt::Debug for PreparedCommit {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("PreparedCommit")
            .field("run_id", &self.planned.run_id)
            .field("session", &self.session)
            .finish_non_exhaustive()
    }
}

/// Law X3d r6 item 3, under the writer lease the session holds:
/// 0. the end-path settlement reserve, through the session's own step, before
///    any check that can return a `StoppedSession`;
/// 1. the binding: the Run names the session's project, its evaluator closure
///    is the session's core evaluator closure (law X3d r8; EC1), and every
///    value the commit writes is built (the invariant row on a mismatch);
/// 3. the carrier's capacity (`CarrierCapacityExhausted`, the ledger open).
///
/// Then the store's directories and ledger (X3c-1), and, under one
/// publication reserve (step 2), attempt admission (step 4: a reused
/// ExecutionId is `ExistingAttempt`, step 5; an undetermined `COMMIT` is
/// `CommitUndetermined`) and the objects with their barriers (step 6).
///
/// Every refusal returns the session's `StoppedSession`: after step 0 it holds
/// the reserve, except after an undetermined attempt admission, which
/// forfeits it.
pub fn prepare_commit(
    run: ReplayedRun,
    session: CommitSession,
) -> Result<PreparedCommit, (NotPrepared, StoppedSession)> {
    // Step 0.
    let mut session = session
        .reserve_end_path()
        .map_err(|(refusal, stopped)| (NotPrepared::Refused(refusal.termination()), stopped))?;
    // Step 1, with every value the commit writes.
    let bound = Bound::of(&session);
    let planned = session.charge(|work| {
        work.run(plan_cost(&run), |_| {
            plan(&run, &bound).map_err(WorkFailure::Operation)
        })
    });
    let (planned, declared) = match planned {
        Ok(planned) => planned,
        Err(failure) => {
            let row = match failure {
                WorkFailure::Budget(_) => T::BudgetExhausted,
                WorkFailure::Operation(_) => T::Invariant,
            };
            return Err((NotPrepared::Refused(row), session.refused()));
        }
    };
    // Step 3: the ledger stays open on an exhausted generation.
    let mut session = session.capacity().map_err(|(exhausted, stopped)| {
        (NotPrepared::CarrierCapacityExhausted(exhausted), stopped)
    })?;
    // The selected store `I/stores/S`, then X3c-1's location and layout.
    let root = match session.store_root() {
        Ok(root) => root,
        Err(failure) => {
            let row = session_failure(&failure);
            return Err((NotPrepared::Refused(row), session.refused()));
        }
    };
    let Some(names) = ProjectStoreNames::new(&planned.store, &planned.namespace) else {
        return Err((NotPrepared::Refused(T::Invariant), session.refused()));
    };
    let location = ProjectStoreLocation::selected(
        root.directory(),
        root.path().to_path_buf(),
        names,
        root.uid(),
    );
    let layout = match session.charge(|work| admit_layout(&location, work)) {
        Ok(layout) => layout,
        Err(failure) => {
            let row = ledger_failure(&failure);
            return Err((NotPrepared::Refused(row), session.refused()));
        }
    };
    // Steps 2, 4, 5 and 6.
    let record = attempt_record(&planned);
    let admitted = session.charge_attempt(|work, open_window| {
        admit_and_publish(&location, &layout, &record, declared, work, open_window)
    });
    let (attempt, objects) = match admitted {
        Ok(admitted) => admitted,
        Err(WorkFailure::Operation(ProjectLedgerRefusal::ReusedExecution)) => {
            let Some(requested) = requested_binding(&planned) else {
                return Err((NotPrepared::Refused(T::Invariant), session.refused()));
            };
            let execution_id = planned.execution;
            return Err((
                NotPrepared::ExistingAttempt {
                    execution_id,
                    requested: Box::new(requested),
                },
                session.refused(),
            ));
        }
        Err(WorkFailure::Operation(ProjectLedgerRefusal::AttemptUndetermined)) => {
            let execution_id = planned.execution;
            return Err((
                NotPrepared::CommitUndetermined { execution_id },
                session.undetermined(),
            ));
        }
        Err(failure) => {
            let row = ledger_failure(&failure);
            return Err((NotPrepared::Refused(row), session.refused()));
        }
    };
    drop(location);
    Ok(PreparedCommit {
        run,
        session,
        ledger: layout.ledger,
        attempt,
        objects,
        planned,
    })
}

// ------------------------------------------------------------------ publish

impl PreparedCommit {
    /// Law X3d r6 item 4: the journal's level 3 (security), the evidence
    /// ledger's level 3 (never waiting; on failure, security's consuming
    /// abort), then security's `seal_under_append_lock` with this module's
    /// private adapter: after the durable `SEAL` and its `COMMITTED` witness
    /// the adapter stages every row in the open evidence transaction, and its
    /// one consuming method performs only the evidence `COMMIT`, inside the
    /// one `AdmissionPermit`. `PublishedCommit` is built only when that
    /// `COMMIT` returned success (`x3d.publish.published`).
    pub fn publish(self) -> (CommitOutcome, StoppedSession) {
        let PreparedCommit {
            run,
            session,
            ledger,
            attempt,
            objects,
            planned,
        } = self;
        // Step 1.
        let mut txn = match begin_journal_txn(session) {
            Ok(txn) => txn,
            Err((refusal, stopped)) => {
                return (CommitOutcome::Refused(refusal.termination()), stopped);
            }
        };
        // Step 2.
        let prepared = txn.charge(|work| begin_prepared_ledger(&ledger, &attempt, objects, work));
        let prepared = match prepared {
            Ok(prepared) => prepared,
            Err(failure) => {
                let row = ledger_failure(&failure);
                return (CommitOutcome::Refused(row), txn.abort());
            }
        };
        // Step 3, through security.
        let adapter = Stager {
            prepared,
            planned: &planned,
        };
        let (outcome, stopped) = seal_under_append_lock(txn, &run, adapter);
        let outcome = match outcome {
            SealOutcome::Committed {
                committed,
                binding,
                latched_after_admission,
            } => {
                let published = PublishedCommit {
                    receipt: committed.receipt,
                    run_id: binding.run_id().to_owned(),
                    execution_id: planned.execution.clone(),
                    commit_sequence: committed.sequence,
                    grant_generation: binding.grant_generation(),
                    seal_seq: binding.seal_seq(),
                    latched_after_admission,
                };
                opensip_platform::crash_barrier!("x3d.publish", "published", step);
                CommitOutcome::Committed(published)
            }
            SealOutcome::CommitUndetermined { execution_id } => {
                CommitOutcome::CommitUndetermined { execution_id }
            }
            SealOutcome::Refused(SealRefusal::Session(refusal)) => {
                CommitOutcome::Refused(refusal.termination())
            }
            SealOutcome::Refused(SealRefusal::Staging(refusal)) => {
                CommitOutcome::Refused(ledger_row(refusal.row()))
            }
        };
        (outcome, stopped)
    }
}

// --------------------------------------------------------------- the adapter

/// The SEAL binding's values, as security's `JournalSealBinding` reads them.
struct Sealed<'a> {
    carrier: &'a str,
    generation: i64,
    seq: i64,
    body: &'a str,
    operation: &'a str,
    run_id: &'a str,
}
impl<'a> Sealed<'a> {
    fn of(binding: &'a JournalSealBinding) -> Self {
        Self {
            carrier: binding.carrier_digest(),
            generation: binding.grant_generation(),
            seq: binding.seal_seq(),
            body: binding.body_sha256(),
            operation: binding.operation_ref(),
            run_id: binding.run_id(),
        }
    }
}

/// Item 1's private adapter implementation: the open evidence transaction
/// and the commit's values. Not Clone; staged at most once.
struct Stager<'a> {
    prepared: PreparedLedger,
    planned: &'a Planned,
}
impl CommitAdapter for Stager<'_> {
    type Staged = Staged;
    type Refusal = ProjectLedgerRefusal;
    fn stage(
        self,
        binding: &JournalSealBinding,
        work: &mut WorkScope<'_>,
    ) -> Result<Staged, WorkFailure<ProjectLedgerRefusal>> {
        stage(self.prepared, self.planned, &Sealed::of(binding), work)
    }
}

/// The staged commit: the prepared-commit adapter and the receipt it carries.
/// Its one consuming method performs only the evidence `COMMIT`.
struct Staged {
    commit: PreparedLedgerCommit,
    receipt: Vec<u8>,
    sequence: u64,
}
/// What a successful evidence `COMMIT` returns to `publish`.
struct Committed {
    receipt: Vec<u8>,
    sequence: u64,
}
impl StagedCommit for Staged {
    type Committed = Committed;
    fn commit(self) -> EvidenceCommit<Committed> {
        match self.commit.commit() {
            LedgerCommitOutcome::Committed { .. } => EvidenceCommit::Committed(Committed {
                receipt: self.receipt,
                sequence: self.sequence,
            }),
            LedgerCommitOutcome::Undetermined { .. } => EvidenceCommit::Undetermined,
        }
    }
}

/// Item 4 step 3.8 (X3c item 6): in the open evidence transaction, after the
/// durable `SEAL`, with nothing committed:
/// - the SEAL binding must join the commit: its RunId, carrier digest and
///   operationRef are the commit's own (otherwise the invariant row);
/// - the receipt counter is allocated by the ledger's one accessor;
/// - the exact receipt and the thirteen-field association are built from
///   the commit's values, the counter and the binding, and admitted by their
///   own parsers;
/// - X3c-2 stages them with the Run material, all or none. The initial
///   availability (generation 0, `retained`) and the empty pin set built here
///   are staged on the Run's first commit in (S, N) only: X3c r8 (unit
///   X3c-3) reads the Run's standing first, and a re-commit of an
///   already-committed Run stages neither (X3c r8 items 6a.2, 6a.4, 6a.5).
fn stage(
    prepared: PreparedLedger,
    planned: &Planned,
    sealed: &Sealed<'_>,
    work: &mut WorkScope<'_>,
) -> Refused<Staged> {
    let mismatch = || WorkFailure::Operation(ProjectLedgerRefusal::StagingMismatch);
    if sealed.run_id != planned.run_id
        || sealed.carrier != planned.carrier
        || sealed.operation != planned.operation
    {
        return Err(mismatch());
    }
    let schemas = planned.schemas;
    let sequence = prepared.next_commit_sequence(work)?;
    let receipt = receipt_bytes(planned, sequence).ok_or_else(mismatch)?;
    let association =
        association_bytes(planned, sequence, &receipt, sealed).ok_or_else(mismatch)?;
    let availability = availability(schemas, &planned.run_id).ok_or_else(mismatch)?;
    let receipt_candidate = ReceiptCandidate::parse(&receipt).map_err(|_| mismatch())?;
    let association = AssociationCandidate::parse(&association).map_err(|_| mismatch())?;
    let pins = Inventory::from_rows(planned.run_id.clone(), Vec::new()).map_err(|_| mismatch())?;
    let commit = prepared.stage(
        schemas,
        CommitRows {
            carrier: &planned.carrier,
            receipt: &receipt_candidate,
            association: &association,
            manifest: planned.manifest.clone(),
            inventory: planned.inventory.clone(),
            availability,
            pins: &pins,
        },
        STAGING_LIMITS,
        work,
    )?;
    Ok(Staged {
        commit,
        receipt,
        sequence,
    })
}

/// The exact commit receipt (`identity-schemas.v3#/$defs/commit-receipt`).
fn receipt_bytes(planned: &Planned, sequence: u64) -> Option<Vec<u8>> {
    canonical(vec![
        ("schemaVersion", integer(2)?),
        ("runId", text(&planned.run_id)),
        ("executionId", text(&planned.execution)),
        ("namespaceId", text(&planned.namespace)),
        ("commitSequence", integer(sequence.into())?),
        ("inventoryDigest", text(&planned.inventory_digest)),
        ("sealedAssurance", text(SEALED_ASSURANCE)),
        ("signerKeyId", text(RECEIPT_SIGNER)),
    ])
}
/// The private thirteen-field `CommitRecoveryAssociationV1`: the commit's
/// own values, the counter the receipt carries (as canonical decimal text),
/// the receipt's raw SHA-256 and the SEAL binding's journal values.
fn association_bytes(
    planned: &Planned,
    sequence: u64,
    receipt: &[u8],
    sealed: &Sealed<'_>,
) -> Option<Vec<u8>> {
    canonical(vec![
        ("recordSchema", integer(1)?),
        ("storeGenerationDigest", text(&planned.store_digest)),
        ("namespaceId", text(&planned.namespace)),
        ("executionId", text(&planned.execution)),
        ("runId", text(&planned.run_id)),
        ("inventoryDigest", text(&planned.inventory_digest)),
        ("commitSequence", text(&sequence.to_string())),
        ("receiptBytesSha256", text(&sha256_hex(receipt))),
        ("journalCarrierDigest", text(sealed.carrier)),
        ("grantGeneration", integer(sealed.generation.into())?),
        ("journalSeq", integer(sealed.seq.into())?),
        ("journalBodySha256", text(sealed.body)),
        ("operationRef", text(sealed.operation)),
    ])
}
/// The Run's initial availability: generation 0, `retained`, nothing
/// missing, observed at commit.
fn availability(schemas: &RegisteredSchemas, run_id: &str) -> Option<AvailabilityRecord> {
    let raw = canonical(vec![
        ("schemaVersion", integer(2)?),
        ("runId", text(run_id)),
        ("generation", integer(0)?),
        ("state", text("retained")),
        ("missingRefs", V::Array(Vec::new())),
        ("reason", text("observed")),
    ])?;
    AvailabilityRecord::parse(schemas, &raw, STAGING_LIMITS.per_record_work).ok()
}

#[cfg(test)]
#[path = "commit_tests.rs"]
mod tests;
