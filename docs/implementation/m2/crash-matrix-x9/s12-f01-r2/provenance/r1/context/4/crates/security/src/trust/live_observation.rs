// Law X4 r7 items 2, 4 and 5 (unit X4a) over law X4T r9 items 7 to 9: the
// operation's trust side.
// - `fenced_operation_read`: the fenced first read at the lease-free point,
//   X4T-b's `fenced_first_read` over the retained `state.v1` owner bound to
//   the write gate's one read, with the S4 observation the caller projects
//   from the monitor's own opening sample, and on F absent X4B-b's
//   acceptance and one confirming admission (`bootstrapping_first_read`).
//   It is the monitor's first `read`.
// - `RetainedTrustHandles`: `trust/stores/S`, its `events`, and `objects`,
//   `records` and `publications`, opened no-follow through the fence's I and
//   judged (identity, custody, filesystem) under the fence at the handoff.
// - `LiveObservation`: one unfenced observation through those handles only,
//   as one counter callback of the shared monitor: `state.v1` opened by name,
//   X4T's reread over the closure (each file opened by name through its
//   collection's retained handle), `state.v1` reopened, and once more when
//   its identity changed; then the floors against the start view and S6's
//   `observe_revocation` against the immutable start epoch and closure.
//   Unit X4-F1 (law X4T r11 item 6): the reread evaluates expiry and
//   staleness at the start view's tEval advanced by the monotonic time
//   elapsed to the monitored read's own opening sample.
// It never takes the fence, writes nothing and grants nothing.
use super::super::super::directory_record_capture as files;
use super::super::super::native_record_capture::{locator_components, reference_parts};
use super::super::super::retained_metadata_index::{self as M, Budget, Collection};
use super::floor_publication::RetainedCurrentTrust;
use super::trust_bootstrap::{BootstrapSource, bootstrapping_first_read};
use super::{
    AdmittedCurrentTrust, ReadMode, TrustRefusal, TrustRow, ViewInputs, admit_current_trust,
};
use crate::custody::directory_policy;
use crate::custody::installation_fence::HeldFence;
use crate::revocation::Sample;
use crate::trust::trust_record_reader::{Record, RecordKind};
use opensip_identity::{JsonInteger, JsonValue as V, digest_hex};
use opensip_platform::{
    DescriptorFilesystem, DescriptorMetadata, RetainedChildDirectory, RetainedDirectory, WorkCost,
    WorkFailure, WorkLedger, WorkScope,
};
use std::collections::BTreeSet;
use std::ffi::OsStr;
use std::os::unix::fs::MetadataExt;
use std::sync::Arc;

const CURRENT: &str = "state.v1";
const MIB: usize = 1 << 20;
/// Law X4 r7 item 5 (with X4T r9 item 11): one observation's ledger, two
/// views at `TRUST_VIEW_COST` each, for both attempts of one read.
pub(crate) const OBSERVATION_LEDGER: WorkCost = WorkCost {
    objects: 2 * super::TRUST_VIEW_COST.0,
    edges: 2 * super::TRUST_VIEW_COST.1,
    bytes: 2 * super::TRUST_VIEW_COST.2,
};
const _: () = assert!(OBSERVATION_LEDGER.bytes == 224 * MIB);

// ----------------------------------------------------------- invocation

/// The invocation identity the floor publication's `host-trust-admission`
/// operation records (law X4T r9 item 7): `req1_` and `exec1_` with 32
/// lowercase hex each, and a step id. Supplied by the operation's caller.
#[derive(Clone, Debug, PartialEq, Eq)]
pub(crate) struct TrustInvocation {
    request_id: String,
    execution_id: String,
    step_id: i64,
}
fn hex32(text: &str) -> bool {
    text.len() == 32
        && text
            .bytes()
            .all(|b| b.is_ascii_digit() || (b'a'..=b'f').contains(&b))
}
impl TrustInvocation {
    pub(crate) fn new(request_id: &str, execution_id: &str, step_id: i64) -> Option<Self> {
        let ok = request_id.strip_prefix("req1_").is_some_and(hex32)
            && execution_id.strip_prefix("exec1_").is_some_and(hex32)
            && step_id >= 0;
        ok.then(|| Self {
            request_id: request_id.to_owned(),
            execution_id: execution_id.to_owned(),
            step_id,
        })
    }
    fn value(&self) -> V {
        V::Object(
            [
                (
                    "executionId".to_owned(),
                    V::String(self.execution_id.clone()),
                ),
                ("requestId".to_owned(), V::String(self.request_id.clone())),
                (
                    "stepId".to_owned(),
                    V::Integer(JsonInteger::new(i128::from(self.step_id)).expect("i64")),
                ),
            ]
            .into(),
        )
    }
}

// ------------------------------------------------------ the fenced read

/// Law X4T r11 items 7 to 9 and X4B r5 item 1 at the lease-free point, as
/// the operation monitor's first `read` call runs it: the retained
/// `state.v1` owner is bound to the gate's one read (its bytes and sample,
/// no new content read), X4T-b's fenced first read runs with its
/// write-ahead, and on F absent only X4B-b's acceptance from `bootstrap` and
/// the one confirming admission run, on the same observation. The view is
/// returned with every confirmed publication that advanced the owner, in
/// order, for the gate's own owner to follow, one by one
/// (`DurableInstallation::advance_current`).
#[allow(clippy::too_many_arguments)]
pub(crate) fn fenced_operation_read(
    work: &mut WorkScope<'_>,
    fence: &dyn HeldFence,
    raw: &[u8],
    sample: &DescriptorMetadata,
    observation: &V,
    core_closure: &str,
    invocation: &TrustInvocation,
    bootstrap: &BootstrapSource<'_>,
) -> Result<(AdmittedCurrentTrust, Vec<super::ConfirmedCurrent>), TrustRefusal> {
    let uid = fence.supplied_actor().0;
    let capsule = opensip_identity::parse_json(raw).map_err(|_| TrustRefusal {
        row: TrustRow::Incomplete,
        cause: "state.v1".into(),
    })?;
    let store = super::field(&capsule, "store")?.clone();
    let mut owner = RetainedCurrentTrust::bind(fence.directory(), uid, &store, raw, sample, work)?;
    let inputs = ViewInputs {
        mode: ReadMode::Fenced { report: false },
        observation: Some(observation),
        project_policy: None,
        core_closure,
    };
    let view = bootstrapping_first_read(
        work,
        fence,
        &mut owner,
        &inputs,
        &invocation.value(),
        bootstrap,
    )?;
    Ok((view, owner.confirmations().to_vec()))
}

// ---------------------------------------------------- retained handles

/// The trust store's retained handles (law X4 r7 item 5): `trust/stores/S`,
/// its `events`, and the `objects`, `records` and `publications`
/// collections. Each is bound no-follow by exact name to its retained parent
/// and judged private and on H's filesystem when opened, under the fence.
/// Not Clone. After the release they are the observation's only way in.
pub(crate) struct RetainedTrustHandles {
    store: Arc<RetainedChildDirectory>,
    events: Arc<RetainedChildDirectory>,
    objects: Arc<RetainedChildDirectory>,
    records: Arc<RetainedChildDirectory>,
    publications: Arc<RetainedChildDirectory>,
    expected_store: V,
    sid: String,
    uid: u32,
    groups: BTreeSet<u32>,
}
impl std::fmt::Debug for RetainedTrustHandles {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("RetainedTrustHandles")
            .field("store", &self.sid)
            .finish_non_exhaustive()
    }
}
/// One handle's binding and judgment: the open, both descriptor samples
/// (parent and child) and both filesystem samples.
fn handle_cost(name: &str) -> WorkCost {
    let parts = [
        opensip_platform::open_child_directory_cost(OsStr::new(name)),
        opensip_platform::descriptor_acl_capture_cost(),
        opensip_platform::descriptor_acl_capture_cost(),
        opensip_platform::descriptor_filesystem_observation_cost(),
        opensip_platform::descriptor_filesystem_observation_cost(),
    ];
    parts
        .into_iter()
        .try_fold(WorkCost::default(), WorkCost::checked_add)
        .unwrap_or(WorkCost {
            objects: usize::MAX,
            edges: usize::MAX,
            bytes: usize::MAX,
        })
}
fn incomplete(cause: impl std::fmt::Debug) -> WorkFailure<TrustRefusal> {
    WorkFailure::Operation(TrustRefusal {
        row: TrustRow::Incomplete,
        cause: format!("{cause:?}"),
    })
}
impl RetainedTrustHandles {
    /// Open and judge the five handles through I, under the held fence, on
    /// the gate's ledger. A missing, misbound or foreign directory is an
    /// incomplete installation; it is never created here.
    pub(crate) fn open(
        i: &RetainedDirectory,
        uid: u32,
        expected_store: &V,
        home_filesystem: &dyn Fn(&DescriptorFilesystem) -> bool,
        work: &mut WorkScope<'_>,
    ) -> Result<Self, WorkFailure<TrustRefusal>> {
        let sid = match super::field(expected_store, "storeInstanceId") {
            Ok(V::String(sid)) if sid.len() == 32 => sid.clone(),
            _ => return Err(incomplete("store")),
        };
        let groups = BTreeSet::new();
        let bind = |parent: &RetainedDirectory, name: &str, work: &mut WorkScope<'_>| {
            work.run(handle_cost(name), |_| {
                let child = parent
                    .bind_child_directory(OsStr::new(name))
                    .map_err(|e| incomplete(("bind", name, e)))?;
                directory_policy::inspect(&child, uid, &groups)
                    .map_err(|e| incomplete(("custody", name, e)))?;
                let filesystems = child
                    .observe_filesystems()
                    .map_err(|e| incomplete(("filesystem", name, e)))?;
                if !filesystems.iter().all(home_filesystem) {
                    return Err(incomplete(("filesystem", name)));
                }
                Ok(Arc::new(child))
            })
        };
        let trust = bind(i, "trust", work)?;
        let stores = bind(trust.directory(), "stores", work)?;
        let store = bind(stores.directory(), &sid, work)?;
        let events = bind(store.directory(), "events", work)?;
        let objects = bind(trust.directory(), "objects", work)?;
        let records = bind(trust.directory(), "records", work)?;
        let publications = bind(trust.directory(), "publications", work)?;
        Ok(Self {
            store,
            events,
            objects,
            records,
            publications,
            expected_store: expected_store.clone(),
            sid,
            uid,
            groups,
        })
    }
    fn all(&self) -> [&Arc<RetainedChildDirectory>; 5] {
        [
            &self.store,
            &self.events,
            &self.objects,
            &self.records,
            &self.publications,
        ]
    }
}

/// The store the observation's reads go through: each reference located by
/// the native readers' own locator, then opened by name under the retained
/// handle of its collection (and the collection's own subdirectories). Every
/// directory and file is charged through the budget, and the first native
/// failure is kept for completion, as `NativeStore` keeps it.
struct RetainedStore<'h> {
    handles: &'h RetainedTrustHandles,
    failure: Option<String>,
}
impl RetainedStore<'_> {
    fn base(
        &self,
        collection: Collection,
        components: &[String],
    ) -> Option<(&Arc<RetainedChildDirectory>, usize)> {
        let h = self.handles;
        match (collection, components.get(1).map(String::as_str)) {
            (Collection::Objects, Some("objects")) => Some((&h.objects, 2)),
            (Collection::Records, Some("records")) => Some((&h.records, 2)),
            (Collection::Publications, Some("publications")) => Some((&h.publications, 2)),
            (Collection::Events, Some("stores"))
                if components.get(2) == Some(&h.sid)
                    && components.get(3).map(String::as_str) == Some("events") =>
            {
                Some((&h.events, 4))
            }
            _ => None,
        }
    }
    fn read_at(&mut self, b: &mut Budget, r: &M::ReadRequest<'_>) -> Result<Arc<[u8]>, M::Error> {
        let components = locator_components(r.collection(), r.reference(), r.initial_store())
            .map_err(|_| M::Error::Reference)?;
        let (_, length) = reference_parts(r.collection(), r.reference(), r.initial_store())
            .map_err(|_| M::Error::Reference)?;
        let (base, skip) = self
            .base(r.collection(), &components)
            .ok_or(M::Error::Reference)?;
        let (leaf, parents) = components[skip..].split_last().ok_or(M::Error::Reference)?;
        let (uid, groups) = (self.handles.uid, &self.handles.groups);
        b.directory(Arc::clone(base))?;
        let mut directory = Arc::clone(base);
        for name in parents {
            b.edge(1)?;
            let child = directory
                .directory()
                .bind_child_directory(OsStr::new(name))
                .map_err(|e| self.fail(("bind", name, e)))?;
            directory_policy::inspect(&child, uid, groups)
                .map_err(|e| self.fail(("custody", e)))?;
            let child = Arc::new(child);
            b.directory(Arc::clone(&child))?;
            directory = child;
        }
        b.edge(1)?;
        let mut failure = None;
        let raw = b.capture(
            r.collection(),
            r.digest(),
            true,
            |cap| match files::read_one(&directory, leaf, cap.min(length), uid, groups, |_| {}) {
                Ok((_, raw, _)) => Ok(raw),
                Err(e) => {
                    failure = Some(format!("{e:?}"));
                    Err(())
                }
            },
        );
        let raw = match raw {
            Ok(raw) => raw,
            Err(e) => {
                if let Some(failure) = failure {
                    self.failure.get_or_insert(failure);
                }
                return Err(e);
            }
        };
        if raw.len() != length {
            return Err(M::Error::Digest);
        }
        Ok(raw)
    }
    fn fail(&mut self, cause: impl std::fmt::Debug) -> M::Error {
        self.failure.get_or_insert_with(|| format!("{cause:?}"));
        M::Error::Capture
    }
}
impl M::Store for RetainedStore<'_> {
    fn read(&mut self, b: &mut Budget, r: M::ReadRequest<'_>) -> Result<Arc<[u8]>, M::Error> {
        self.read_at(b, &r)
    }
}

// ---------------------------------------------------------- observation

/// What one observation found (law X4 r7 item 5).
#[derive(Clone, Debug, PartialEq, Eq)]
pub(crate) enum Observed {
    /// No revoking match: continue. `drift` is S6's recorded drift
    /// (`revocation-unrelated`, `policy-unrelated`, or both), if any.
    Continue { drift: Option<&'static str> },
    /// A revoking match: `trust-revoked` or `policy`.
    Revoke { subject: &'static str },
}
/// Why an observation failed. Each is a counter error of the monitored read,
/// which latches the gate as `OBSERVER.FAIL_STOP` with this subject.
#[derive(Clone, Debug, PartialEq, Eq)]
pub(crate) enum ObservationFailure {
    /// A record or `state.v1` absent, unreadable, misbound or changed.
    Unreadable(String),
    /// Both attempts saw `state.v1` replaced under them.
    Mixed,
    /// A signature, quorum, chain or payload refusal.
    Unauthenticated(String),
    /// A floor below the retained floors or the start view's.
    Rollback(String),
    /// The per-observation ledger refused.
    Budget(String),
    /// The view's role standing no longer continues.
    Standing(String),
    /// The observation has no instant (law X4T r11 item 6, unit X4-F1): its
    /// opening sample does not project, or names another boot or an earlier
    /// monotonic reading than the handoff's. The monitor's own `clock`
    /// subject (X4 r7 item 8: a boot change is a fail-stop).
    Clock(String),
}
impl ObservationFailure {
    pub(crate) fn subject(&self) -> &'static str {
        match self {
            Self::Unreadable(_) => "unreadable",
            Self::Mixed => "mixed",
            Self::Unauthenticated(_) => "unauthenticated",
            Self::Rollback(_) => "rollback",
            Self::Budget(_) => "budget",
            Self::Standing(_) => "standing",
            Self::Clock(_) => "clock",
        }
    }
}
/// The test seam at an observation's steps: which attempt, which step.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub(crate) enum ObservationPoint {
    /// Step 1 opened `state.v1` (attempt 1 or 2).
    Opened(u8),
    /// Step 3 admitted the view, before step 4's reopen.
    Admitted(u8),
}
/// A test hook run at each `ObservationPoint`; production passes `live()`.
#[derive(Clone, Default)]
pub(crate) struct ObservationHook {
    #[cfg(test)]
    pub(crate) at: Option<Arc<dyn Fn(ObservationPoint) + Send + Sync>>,
}
impl ObservationHook {
    pub(crate) fn live() -> Self {
        Self::default()
    }
    fn at(&self, _point: ObservationPoint) {
        #[cfg(test)]
        if let Some(hook) = &self.at {
            hook(_point);
        }
    }
}
impl std::fmt::Debug for ObservationHook {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("ObservationHook").finish_non_exhaustive()
    }
}

/// A reread refusal, as X4's callback sees it (law X4T r9 item 9). A
/// revoked closure component is the revoking observation (X4T item 10: during
/// an operation that refusal is X4's revoked-during-operation row); every
/// other refusal is a fail-stop.
fn classify(refusal: TrustRefusal) -> Result<Observed, ObservationFailure> {
    let cause = format!("{:?}: {}", refusal.row, refusal.cause);
    match refusal.row {
        TrustRow::Continuation(subject)
            if ["release:", "keyId:", "namespace:", "catalogSnapshot:"]
                .iter()
                .any(|kind| subject.starts_with(kind)) =>
        {
            Ok(Observed::Revoke {
                subject: "trust-revoked",
            })
        }
        TrustRow::Continuation(_)
        | TrustRow::IndexContinuation(_)
        | TrustRow::ComponentContinuation(_) => Err(ObservationFailure::Standing(cause)),
        TrustRow::Budget => Err(ObservationFailure::Budget(cause)),
        TrustRow::Rollback => Err(ObservationFailure::Rollback(cause)),
        TrustRow::Root(..) | TrustRow::PayloadNotAdmissible(_) | TrustRow::ClockExcursion(_) => {
            Err(ObservationFailure::Unauthenticated(cause))
        }
        TrustRow::Incomplete
        | TrustRow::NoAdmittedTimeContext
        | TrustRow::StateSchemaUnsupported
        | TrustRow::HostIo
        | TrustRow::RequiredFilesChanged
        | TrustRow::Invariant => Err(ObservationFailure::Unreadable(cause)),
    }
}
fn ledger_failure(budget: opensip_platform::WorkBudgetError) -> ObservationFailure {
    ObservationFailure::Budget(format!("{budget:?}"))
}

/// One unfenced observation over the operation's retained handles, against
/// the immutable start view (law X4 r7 item 5).
pub(crate) struct LiveObservation<'a> {
    pub(crate) handles: &'a RetainedTrustHandles,
    pub(crate) start: &'a AdmittedCurrentTrust,
    pub(crate) core_closure: &'a str,
    pub(crate) hook: &'a ObservationHook,
}
/// One attempt's result: the admitted view (or the refusal X4's callback
/// classifies) and whether step 4's reopen found step 1's `state.v1`.
struct Attempt {
    view: Result<AdmittedCurrentTrust, TrustRefusal>,
    coherent: bool,
}
impl LiveObservation<'_> {
    /// Steps 1 to 4 once more if step 4's identity differs, then the floors
    /// and the S6 predicate, all charged to one fresh per-observation ledger
    /// (never the operation's). This is the body of one monitored read, and
    /// `opening` is that read's own opening sample: both attempts evaluate
    /// expiry and staleness at its instant (unit X4-F1).
    pub(crate) fn observe(&self, opening: &Sample) -> Result<Observed, ObservationFailure> {
        let at = self.instant(opening)?;
        let mut ledger = WorkLedger::with_limits(OBSERVATION_LEDGER)
            .map_err(|e| ObservationFailure::Budget(format!("{e:?}")))?;
        let first = self.attempt(&mut ledger, 1, at)?;
        let attempt = if first.coherent {
            first
        } else {
            let second = self.attempt(&mut ledger, 2, at)?;
            if !second.coherent {
                return Err(ObservationFailure::Mixed);
            }
            second
        };
        let view = match attempt.view {
            Ok(view) => view,
            Err(refusal) => return classify(refusal),
        };
        predicate(self.start, &view)
    }
    /// Law X4T r11 item 6 (unit X4-F1): the observation's instant. The
    /// opening sample is projected exactly as the first read's S4 observation
    /// is (`project_monitor_sample`), and the start view's handoff clock
    /// advances by its monotonic reading on the same boot; its wall reading
    /// is never used. No clock is sampled here, nothing is read or charged.
    fn instant(&self, opening: &Sample) -> Result<i64, ObservationFailure> {
        let observation = crate::clock_observation::project_monitor_sample(
            opening.wall_seconds,
            opening.wall_nanos,
            opening.before,
            opening.after,
            &opening.boot,
        )
        .map_err(|cause| ObservationFailure::Clock(cause.into()))?;
        let handoff = self
            .start
            .handoff_clock()
            .ok_or_else(|| ObservationFailure::Clock("handoff".into()))?;
        handoff
            .advanced(&observation)
            .map_err(|cause| ObservationFailure::Clock(cause.into()))
    }
    fn attempt(
        &self,
        ledger: &mut WorkLedger,
        n: u8,
        at: i64,
    ) -> Result<Attempt, ObservationFailure> {
        let h = self.handles;
        // A refused view is carried out here: its failed read has already
        // latched the per-observation ledger, so the scope itself returns
        // `Closed`. It is an error whatever step 4 would find (item 5).
        let mut refused = None;
        let result = ledger.scope(|work| {
            for handle in h.all() {
                directory_policy::inspect(handle, h.uid, &h.groups).map_err(|e| {
                    WorkFailure::Operation(ObservationFailure::Unreadable(format!("{e:?}")))
                })?;
            }
            // Step 1: `state.v1`, by name through the retained store handle.
            let mut held = None;
            let (raw, view) = {
                let mut b = Budget::borrowed(work);
                let opened = b.directory(Arc::clone(&h.store)).and_then(|()| {
                    b.capture_current(&h.store, |cap| {
                        match files::read_one(&h.store, CURRENT, cap, h.uid, &h.groups, |_| {}) {
                            Ok((file, raw, observation)) => {
                                held = Some((file, observation));
                                Ok(raw)
                            }
                            Err(_) => Err(()),
                        }
                    })
                });
                let raw = match opened {
                    Ok(raw) => raw,
                    Err(e) => {
                        return Err(WorkFailure::Operation(match e {
                            M::Error::ObjectLimit
                            | M::Error::EdgeLimit
                            | M::Error::ByteLimit
                            | M::Error::Closed => ObservationFailure::Budget(format!("{e:?}")),
                            e => ObservationFailure::Unreadable(format!("{e:?}")),
                        }));
                    }
                };
                self.hook.at(ObservationPoint::Opened(n));
                // Steps 2 and 3: X4T's reread over the closure, through the
                // retained collection handles.
                let capsule = Record::parse(RecordKind::TrustCapsuleV1, &raw, 131072)
                    .map(|record| record.value().clone())
                    .map_err(|e| TrustRefusal {
                        row: TrustRow::Incomplete,
                        cause: format!("{e:?}"),
                    });
                let view = capsule.and_then(|capsule| {
                    if super::field(&capsule, "store")? != &h.expected_store {
                        return Err(TrustRefusal {
                            row: TrustRow::Incomplete,
                            cause: "state.v1-store".into(),
                        });
                    }
                    let inputs = ViewInputs {
                        mode: ReadMode::Reread { at },
                        observation: None,
                        project_policy: None,
                        core_closure: self.core_closure,
                    };
                    let mut store = RetainedStore {
                        handles: h,
                        failure: None,
                    };
                    let admitted = admit_current_trust(
                        &mut b,
                        &h.expected_store,
                        &capsule,
                        &inputs,
                        &mut store,
                    );
                    match (admitted, store.failure) {
                        (Err(_), Some(failure)) => Err(TrustRefusal {
                            row: TrustRow::Incomplete,
                            cause: failure,
                        }),
                        (admitted, _) => admitted,
                    }
                });
                (raw, view)
            };
            drop(raw);
            let view = match view {
                Ok(view) => view,
                Err(refusal) => {
                    refused = Some(refusal);
                    return Err(WorkFailure::Operation(ObservationFailure::Unreadable(
                        "refused".into(),
                    )));
                }
            };
            self.hook.at(ObservationPoint::Admitted(n));
            // Step 4: `state.v1` reopened by name; the same file, unchanged.
            let (file, observation) = held.ok_or_else(|| {
                WorkFailure::Operation(ObservationFailure::Unreadable("state.v1".into()))
            })?;
            let reopen = WorkCost {
                bytes: 512,
                ..RetainedDirectory::open_regular_cost(CURRENT)
            };
            let coherent = work.run(reopen, |_| {
                let named = match h.store.directory().open_regular(CURRENT) {
                    Ok(named) => named,
                    Err(e) if e.kind() == std::io::ErrorKind::NotFound => return Ok(false),
                    Err(e) => {
                        return Err(WorkFailure::Operation(ObservationFailure::Unreadable(
                            format!("{e:?}"),
                        )));
                    }
                };
                let named = named.metadata().map_err(|e| {
                    WorkFailure::Operation(ObservationFailure::Unreadable(format!("{e:?}")))
                })?;
                // The step-1 descriptor's own sample, with no custody
                // predicate: an unlinked or changed original is a replaced
                // `state.v1` (retry), never an unreadable one.
                let original = opensip_platform::observe_descriptor(&file).map_err(|e| {
                    WorkFailure::Operation(ObservationFailure::Unreadable(format!("{e:?}")))
                })?;
                Ok((named.dev(), named.ino())
                    == (original.metadata.device, original.metadata.inode)
                    && original.metadata == observation.metadata
                    && original.acl == observation.acl
                    && named.nlink() == 1)
            })?;
            Ok(Attempt {
                view: Ok(view),
                coherent,
            })
        });
        if let Some(refusal) = refused {
            return Ok(Attempt {
                view: Err(refusal),
                coherent: true,
            });
        }
        result.map_err(|failure| match failure {
            WorkFailure::Operation(failure) => failure,
            WorkFailure::Budget(budget) => ledger_failure(budget),
        })
    }
}

/// The floors, then S6's selected predicate (law X4 r7 item 5). A view
/// below the start view's floors or counters is a rollback and never reaches
/// the predicate (a lower counter never revokes). The predicate runs against
/// the immutable start epoch and closure; the required permission pairs of
/// every M2 writer are empty, so a policy change is drift only.
fn predicate(
    start: &AdmittedCurrentTrust,
    current: &AdmittedCurrentTrust,
) -> Result<Observed, ObservationFailure> {
    let (s, c) = (start.epoch(), current.epoch());
    if current.floors().below(start.floors())
        || c.root_version < s.root_version
        || c.index_snapshot_version < s.index_snapshot_version
        || c.revocation_version < s.revocation_version
    {
        return Err(ObservationFailure::Rollback("below-start".into()));
    }
    use super::super::super::{ClosureSubjects, EpochAtStart, RevocationAction};
    let closure = start.closure();
    let subjects = ClosureSubjects {
        releases: BTreeSet::from([closure.release.clone()]),
        signing_keys: closure.signing_keys.iter().map(digest_hex).collect(),
        namespaces: closure.namespaces.clone(),
        catalog_snapshot: Some(closure.catalog_snapshot),
    };
    let epoch = EpochAtStart {
        revocation_version: s.revocation_version,
        permission_policy_digest: s.permission_policy_digest,
    };
    let observed = super::super::super::observe_revocation(
        &current.revocation.0,
        &epoch,
        &subjects,
        c.permission_policy_digest,
        &BTreeSet::new(),
        Some(&[]),
    );
    Ok(match observed.action {
        RevocationAction::Revoke => Observed::Revoke {
            subject: if observed.reason == "policy" {
                "policy"
            } else {
                "trust-revoked"
            },
        },
        RevocationAction::Continue => Observed::Continue {
            drift: (observed.reason != "no-change").then_some(observed.reason),
        },
    })
}

#[cfg(test)]
mod tests {
    include!("live_observation_tests.rs");
}
