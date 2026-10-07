// Law X4T r5 (X4T-a): read-only admission of the installation's current
// trust. It composes the existing owners over one budget and grants nothing;
// it writes nothing (the floor write-ahead is X4T-b) and is not wired to a
// session or operation here (X4a consumes it). Unit X4-F1 (law X4T r11 item
// 6): an observer reread evaluates expiry and staleness at its instant, the
// handoff's tEval advanced by the elapsed monotonic time (`HandoffClock`).
// Unit X4-F2 (law X4T r12 item 6): the fenced read applies them at tEval, as
// its last decision; a refusal from that clock is not a view (`Admission`).
use super::super::admitted_revocations::verify_revocation;
use super::super::admitted_trust_records::{self as clock, Phase};
use super::super::current_event_trace::LocalTrace;
use super::super::current_record_bindings::{self, CurrentRecordBindings};
use super::super::effective_permission_policy::{self as policy, Context, Source};
use super::super::native_record_capture::{NativeStore, ReadCompletionError};
use super::super::{
    CURRENT_ENVELOPE_READER, ChainBudget, ChainError, EnvelopeKind, QuorumState,
    filter_envelope_revoked, verify_envelope,
};
use super::super::{incoming_recovery_quorums, retained_recovery_payload};
use super::super::{ordinary_bundle, ordinary_inventory, ordinary_metadata, ordinary_quorums};
use super::super::{ordinary_roots, recovery_catalog};
use super::{
    AuthenticationContext, ClockInputError, OrdinaryClockInput, RetainedRole, RootedError,
    ScopeContext, ScopeError, State, TimesError, prepare_authenticated_times,
};
use crate::custody::installation_fence::HeldFence;
use crate::trust::trust_record_shapes::{self as shapes, Definition};
use crate::trust_time::{RecordedObservation, TimeAdmission, TimeRefusal};
use opensip_identity::JsonValue as V;
use std::collections::BTreeSet;

const MIB: usize = 1 << 20;
/// Item 11: one view's ceiling (objects, edges, bytes).
pub(crate) const TRUST_VIEW_COST: (usize, usize, usize) = (128, 2048, 112 * MIB);
/// Item 11: the current descriptor's event bound; earlier publications are
/// never walked.
pub(crate) const MAX_VIEW_EVENTS: usize = 32;
/// Item 11: the closure's stored-bytes total, outside the chain's own bound.
pub(crate) const MAX_CLOSURE_BYTES: usize = 40 * MIB;
/// Items 3 and 11: the root chain budget.
const VIEW_CHAIN: ChainBudget = ChainBudget {
    max_links: 16,
    max_stored_bytes: 16 * MIB,
};
const ROLES: [&str; 6] = [
    "TR-BUNDLE",
    "TR-COMPONENT",
    "TR-CORE",
    "TR-INDEX",
    "TR-PROFILE",
    "TR-REPAIR",
];

/// Item 10: the public row a fenced admission refusal takes. 468c maps it.
#[derive(Clone, Debug, PartialEq, Eq)]
pub(crate) enum TrustRow {
    /// `CONFIG.CUSTODY_REFUSED`, subject `installation-incomplete`.
    Incomplete,
    /// `TRUST.NO_ADMITTED_TIME_CONTEXT` (F absent).
    NoAdmittedTimeContext,
    /// `CONTINUE-CORE-NOT-TRUSTED`, subject naming the role and its state
    /// and the existing clocked-expiry/revoked-closure continuation details.
    Continuation(String),
    /// X4T-c: stored index-role standing refuses with its registered detail.
    IndexContinuation(String),
    /// X4T-c: stored component-role standing refuses with its registered detail.
    ComponentContinuation(String),
    /// An S5 `ROOT.*` detail naming the link.
    Root(&'static str, String),
    /// `PAYLOAD-NOT-ADMISSIBLE`.
    PayloadNotAdmissible(&'static str),
    /// `CLOCK-EXCURSION-FORWARD`, subject `in-session` or `beyond-horizon`.
    ClockExcursion(&'static str),
    /// `STATE.SCHEMA_UNSUPPORTED`.
    StateSchemaUnsupported,
    /// The host I/O row.
    HostIo,
    /// `WORK.BUDGET_EXHAUSTED`.
    Budget,
    /// `CONFIG.CUSTODY_REFUSED`, subject `trust-rollback` (item 7, r8).
    Rollback,
    /// `CONFIG.CUSTODY_REFUSED`, subject `required-files-changed`: the
    /// retained `state.v1` changed other than by a confirmed publication
    /// (item 7, r8).
    RequiredFilesChanged,
    /// The existing host invariant row: operational-failed, exit 4,
    /// `SYSTEM.OUTCOME.ILLEGAL_STATE`, `host-invariant`, detail
    /// `HOST.INVARIANT_VIOLATED` (X4B r5 item 1 step 2.3: a second F absent
    /// after a confirmed acceptance, as X3d item 9 uses the row).
    Invariant,
}
impl TrustRow {
    pub(crate) fn code(&self) -> &'static str {
        match self {
            Self::Incomplete | Self::Rollback | Self::RequiredFilesChanged => {
                "CONFIG.CUSTODY_REFUSED"
            }
            Self::NoAdmittedTimeContext => "TRUST.NO_ADMITTED_TIME_CONTEXT",
            Self::Continuation(_) => "CONTINUE-CORE-NOT-TRUSTED",
            Self::IndexContinuation(_) => "CONTINUE-INDEX-NOT-TRUSTED",
            Self::ComponentContinuation(_) => "CONTINUE-COMPONENT-NOT-TRUSTED",
            Self::Root(code, _) => code,
            Self::PayloadNotAdmissible(_) => "PAYLOAD-NOT-ADMISSIBLE",
            Self::ClockExcursion(_) => "CLOCK-EXCURSION-FORWARD",
            Self::StateSchemaUnsupported => "STATE.SCHEMA_UNSUPPORTED",
            Self::HostIo => "HOST.IO_FAILURE",
            Self::Budget => "WORK.BUDGET_EXHAUSTED",
            Self::Invariant => "HOST.INVARIANT_VIOLATED",
        }
    }
    pub(crate) fn subject(&self) -> Option<String> {
        match self {
            Self::Incomplete => Some("installation-incomplete".into()),
            Self::Rollback => Some("trust-rollback".into()),
            Self::RequiredFilesChanged => Some("required-files-changed".into()),
            Self::Continuation(s)
            | Self::IndexContinuation(s)
            | Self::ComponentContinuation(s)
            | Self::Root(_, s) => Some(s.clone()),
            Self::PayloadNotAdmissible(s) | Self::ClockExcursion(s) => Some((*s).into()),
            _ => None,
        }
    }
}
/// A refusal: its row and, for diagnosis only, the internal cause.
#[derive(Debug, PartialEq, Eq)]
pub(crate) struct TrustRefusal {
    pub(crate) row: TrustRow,
    pub(crate) cause: String,
}
fn refuse<T>(row: TrustRow, cause: impl std::fmt::Debug) -> Result<T, TrustRefusal> {
    Err(TrustRefusal {
        row,
        cause: format!("{cause:?}"),
    })
}
/// Item 10: a limit of the view's ledger is the budget row; a read that is
/// absent, oversize (`Cap`, the owners' 4 MiB file cap), not its digest or
/// misreferenced is an incomplete installation, as is an undecodable record.
fn budget_row(error: &super::M::Error) -> TrustRow {
    use super::M::Error as E;
    match error {
        E::ObjectLimit | E::ByteLimit | E::EdgeLimit | E::Closed => TrustRow::Budget,
        _ => TrustRow::Incomplete,
    }
}

/// Item 1: the role standing the view carries when it is admitted.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub(crate) enum TrustStanding {
    ExistingOnly,
    InstallGateRequiredForNewProcess,
}
/// Item 1's S6 epoch.
#[derive(Clone, Debug, PartialEq, Eq)]
pub(crate) struct TrustEpoch {
    pub(crate) root_version: i64,
    pub(crate) index_snapshot_version: i64,
    pub(crate) revocation_version: i64,
    pub(crate) permission_policy_digest: [u8; 32],
}
/// Item 9: which read this is.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub(crate) enum ReadMode {
    /// The fenced first read: time is admitted. `report` is S4's
    /// report-only mode (read sessions and doctor): writes are proposed only.
    /// X4T-a never performs the write-ahead; that is X4T-b. Item 6 (r12,
    /// unit X4-F2): expiry and staleness are evaluated at tEval.
    Fenced { report: bool },
    /// An unfenced reread: items 2 to 5, with no time re-admission. Item 6
    /// (unit X4-F1): expiry and staleness are evaluated at `at`, in UTC
    /// seconds: the handoff's tEval advanced by the elapsed monotonic time
    /// (`HandoffClock::advanced`). No reread is made without its instant.
    Reread { at: i64 },
}
/// Item 1: the admitted current-trust view. Not Clone, not serializable.
#[derive(Debug)]
pub(crate) struct AdmittedCurrentTrust {
    roles: [(State, bool); 6],
    standing: TrustStanding,
    epoch: TrustEpoch,
    time: Option<TimeAdmission>,
    revoked_subjects: Vec<(String, String)>,
    /// Item 7: the admitted capsule's own floors.
    floors: Floors,
    /// Item 7 (X4T-b): the S4 proposal a fenced, not report-only read keeps
    /// for its write-ahead. Never kept on a reread or in report-only mode.
    pending: Option<PendingWrite>,
    /// Item 4's closure components, which the view's revocation was judged
    /// against: law X4 r7 item 2's closure subjects are taken from here.
    closure: ViewClosure,
    /// Item 4's admitted revocation list, for X4's S6 predicate.
    revocation: AdmittedRevocation,
    /// Item 6 (unit X4-F1): an admitted fenced read's clock, which the
    /// rereads of the operation it starts advance. `None` on a reread.
    handoff: Option<HandoffClock>,
}
/// Item 6 (unit X4-F1): the clock of an admitted fenced read. Its tEval, and
/// its S4 observation's sleep-inclusive monotonic seconds and boot. Observer
/// rereads do not re-admit time; they evaluate expiry and staleness at this
/// tEval advanced by the monotonic time elapsed on the same boot.
#[derive(Clone, Debug, PartialEq, Eq)]
pub(crate) struct HandoffClock {
    evaluation: i64,
    mono: i64,
    boot: String,
}
impl HandoffClock {
    /// Item 6: a reread's instant, from the reread's own S4 observation
    /// (`observation`, admitted by the same grammar as the fenced read's):
    /// tEval plus its monotonic seconds less the handoff's. Only the
    /// monotonic reading and the boot are used; the observation's wall clock
    /// is never consulted. Another boot is a stop (X4 r2 item 5), and a
    /// monotonic reading below the handoff's is not an elapsed time; neither
    /// has an instant.
    pub(crate) fn advanced(&self, observation: &V) -> Result<i64, &'static str> {
        let now = RecordedObservation::admit(observation).map_err(|_| "observation")?;
        if now.boot() != self.boot {
            return Err("boot");
        }
        now.mono()
            .checked_sub(self.mono)
            .filter(|elapsed| *elapsed >= 0)
            .and_then(|elapsed| self.evaluation.checked_add(elapsed))
            .ok_or("monotonic")
    }
}
/// Item 4's closure components as the view keeps them (law X4 r7 item 2).
#[derive(Clone, Debug, PartialEq, Eq)]
pub(crate) struct ViewClosure {
    pub(crate) release: String,
    pub(crate) signing_keys: BTreeSet<[u8; 32]>,
    pub(crate) namespaces: BTreeSet<String>,
    pub(crate) catalog_snapshot: i64,
}
/// The admitted revocation evidence, opaque outside the trust owner.
pub(crate) struct AdmittedRevocation(super::super::admitted_revocations::RevocationEvidence);
impl std::fmt::Debug for AdmittedRevocation {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("AdmittedRevocation")
            .field("version", &self.0.version())
            .finish_non_exhaustive()
    }
}
/// The fenced read's S4 proposal, kept only for item 7's write-ahead.
pub(super) struct PendingWrite(pub(super) crate::trust_time::OrdinaryClockProposal);
impl std::fmt::Debug for PendingWrite {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("PendingWrite").finish_non_exhaustive()
    }
}
/// Item 6 (r12, unit X4-F2): what an admission ends in. A fenced read whose
/// `EV-CLOCK` at tEval refuses is never a view. It keeps the read's floors,
/// its S4 outcome and its pending write-ahead only so that item 7 publishes
/// the floor before the refusal (item 7, r12). Both are boxed: their sizes
/// differ by hundreds of bytes.
#[derive(Debug)]
enum Admission {
    View(Box<AdmittedCurrentTrust>),
    Clocked(Box<ClockedRefusal>),
}
/// Item 10 (r12): the continuation row of a fenced read clocked at tEval.
#[derive(Debug)]
struct ClockedRefusal {
    refusal: TrustRefusal,
    floors: Floors,
    time: TimeAdmission,
    pending: Option<PendingWrite>,
}
impl Admission {
    /// The admitted capsule's floors (item 7's check 3).
    fn floors(&self) -> &Floors {
        match self {
            Self::View(view) => &view.floors,
            Self::Clocked(clocked) => &clocked.floors,
        }
    }
    /// The fenced read's S4 outcome; `None` on a reread.
    fn time(&self) -> Option<&TimeAdmission> {
        match self {
            Self::View(view) => view.time.as_ref(),
            Self::Clocked(clocked) => Some(&clocked.time),
        }
    }
    /// Item 7: the S4 proposal a fenced, not report-only read keeps.
    fn take_pending(&mut self) -> Option<PendingWrite> {
        match self {
            Self::View(view) => view.pending.take(),
            Self::Clocked(clocked) => clocked.pending.take(),
        }
    }
    /// The view, or the clocked refusal. Item 7's fenced read calls this
    /// only after its write-ahead or its closing rechecks; every other
    /// caller writes nothing.
    fn into_view(self) -> Result<AdmittedCurrentTrust, TrustRefusal> {
        match self {
            Self::View(view) => Ok(*view),
            Self::Clocked(clocked) => Err(clocked.refusal),
        }
    }
}
/// Item 7 (r8/r9): SC-TRUST floors as seconds and counters. A field is
/// `None` where the clock phase carries no such floor.
#[derive(Clone, Copy, Debug, Default, PartialEq, Eq)]
pub(crate) struct Floors {
    pub(crate) eval_high_water: Option<i64>,
    pub(crate) last_accepted: Option<i64>,
    pub(crate) root_version: Option<i64>,
    pub(crate) revocation_version: Option<i64>,
    pub(crate) index_snapshot_version: Option<i64>,
}
impl Floors {
    /// The floors of a clock phase object: all five for `retained`, F and L
    /// for `evaluated`, none for `unevaluated`.
    pub(crate) fn of_clock(clock: &V) -> Result<Self, TrustRefusal> {
        let stamp = |v: &V| match v {
            V::String(t) => crate::trust_time::timestamp_seconds(t)
                .map_or_else(|_| refuse(TrustRow::Incomplete, "timestamp"), Ok),
            _ => refuse(TrustRow::Incomplete, "timestamp"),
        };
        match field(clock, "phase")? {
            V::String(p) if p == "retained" => {
                let r = field(clock, "record")?;
                Ok(Self {
                    eval_high_water: Some(stamp(field(r, "evalHighWater")?)?),
                    last_accepted: Some(stamp(field(r, "lastAccepted")?)?),
                    root_version: Some(int(field(r, "rootVersion")?)?),
                    revocation_version: Some(int(field(r, "revocationVersion")?)?),
                    index_snapshot_version: Some(int(field(r, "indexSnapshotVersion")?)?),
                })
            }
            V::String(p) if p == "evaluated" => {
                let r = field(clock, "projection")?;
                Ok(Self {
                    eval_high_water: Some(stamp(field(r, "evalHighWater")?)?),
                    last_accepted: Some(stamp(field(r, "lastAccepted")?)?),
                    ..Self::default()
                })
            }
            V::String(p) if p == "unevaluated" => Ok(Self::default()),
            _ => refuse(TrustRow::Incomplete, "clock-phase"),
        }
    }
    /// Whether any floor here is below the same floor of `retained`; a floor
    /// either side lacks is not compared.
    pub(crate) fn below(&self, retained: &Self) -> bool {
        let lower = |a: Option<i64>, b: Option<i64>| matches!((a, b), (Some(a), Some(b)) if a < b);
        lower(self.eval_high_water, retained.eval_high_water)
            || lower(self.last_accepted, retained.last_accepted)
            || lower(self.root_version, retained.root_version)
            || lower(self.revocation_version, retained.revocation_version)
            || lower(self.index_snapshot_version, retained.index_snapshot_version)
    }
}
/// Item 7 checks 1 and 2 (r8): against the time evidence the view already
/// opened. Only an `s4-evaluation` input is compared; an S4.5 epoch input
/// records the one lawful floor-lowering act.
fn check_evidence_floors(floors: &Floors, evidence: &V) -> Result<(), TrustRefusal> {
    if field(evidence, "kind")? != &V::String("s4-evaluation".into()) {
        return Ok(());
    }
    if floors.below(&Floors::of_clock(field(evidence, "beforeClock")?)?) {
        return refuse(TrustRow::Rollback, "time-evidence-before-clock");
    }
    let wall = match field(field(evidence, "observation")?, "wall")? {
        V::String(t) => crate::trust_time::timestamp_seconds(t)
            .map_or_else(|_| refuse(TrustRow::Incomplete, "timestamp"), Ok)?,
        _ => return refuse(TrustRow::Incomplete, "timestamp"),
    };
    let observed = Floors {
        eval_high_water: Some(wall),
        ..Floors::default()
    };
    if floors.below(&observed) {
        return refuse(TrustRow::Rollback, "time-evidence-observation");
    }
    Ok(())
}
impl AdmittedCurrentTrust {
    /// Item 7: the admitted capsule's floors.
    pub(crate) fn floors(&self) -> &Floors {
        &self.floors
    }
    pub(crate) fn standing(&self) -> TrustStanding {
        self.standing
    }
    pub(crate) fn epoch(&self) -> &TrustEpoch {
        &self.epoch
    }
    /// The fenced read's S4 outcome; `None` on a reread.
    pub(crate) fn time(&self) -> Option<&TimeAdmission> {
        self.time.as_ref()
    }
    /// Each role's state, in `ROLES` order, as `EV-CLOCK` gives it at the
    /// read's instant (item 1, r12); the capsule's stored states are unchanged.
    pub(crate) fn role_states(&self) -> [(&'static str, &'static str); 6] {
        std::array::from_fn(|i| (ROLES[i], token(self.roles[i].0)))
    }
    /// The admitted revocation list's (subjectKind, subject) entries.
    pub(crate) fn revoked_subjects(&self) -> &[(String, String)] {
        &self.revoked_subjects
    }
    /// Item 4's closure components (law X4 r7 item 2's closure subjects).
    pub(crate) fn closure(&self) -> &ViewClosure {
        &self.closure
    }
    /// Item 6 (unit X4-F1): the fenced read's clock; `None` on a reread.
    pub(crate) fn handoff_clock(&self) -> Option<&HandoffClock> {
        self.handoff.as_ref()
    }
}
/// What the caller supplies besides the store: the S4 observation for a
/// fenced read, the project's policy body if one exists (item 5), and the
/// running core closure, which is the closure's release subject that the
/// revocation list is checked against (item 4). It is always required.
pub(crate) struct ViewInputs<'a> {
    pub(crate) mode: ReadMode,
    pub(crate) observation: Option<&'a V>,
    pub(crate) project_policy: Option<&'a V>,
    pub(crate) core_closure: &'a str,
}

fn object(v: &V) -> Option<&std::collections::BTreeMap<String, V>> {
    super::super::object(v)
}
fn field<'v>(v: &'v V, k: &str) -> Result<&'v V, TrustRefusal> {
    object(v)
        .and_then(|o| o.get(k))
        .map_or_else(|| refuse(TrustRow::Incomplete, ("field", k)), Ok)
}
fn int(v: &V) -> Result<i64, TrustRefusal> {
    super::super::integer(v).map_or_else(|| refuse(TrustRow::Incomplete, "integer"), Ok)
}
fn state_of(token: &str) -> Option<State> {
    Some(match token {
        "ST-UNBOOTSTRAPPED" => State::Unbootstrapped,
        "ST-TRUSTED" => State::Trusted,
        "ST-EXPIRED" => State::Expired,
        "ST-STALE-REVOCATION" => State::StaleRevocation,
        "ST-QUORUM-LOST" => State::QuorumLost,
        "ST-REVOKED" => State::Revoked,
        "ST-RECOVERY" => State::Recovery,
        _ => return None,
    })
}
fn token(state: State) -> &'static str {
    match state {
        State::Unbootstrapped => "unbootstrapped",
        State::Trusted => "trusted",
        State::Expired => "expired",
        State::StaleRevocation => "stale-revocation",
        State::QuorumLost => "quorum-lost",
        State::Revoked => "revoked",
        State::Recovery => "recovery",
    }
}

/// Item 1: the P0 shape is F absent, refused before any read or join:
/// `heads` and `history` both null and every role `ST-UNBOOTSTRAPPED` with no
/// acceptance. Any other null head or history is an incomplete installation;
/// a capsule with neither null goes on to be bound.
fn is_p0(capsule: &V) -> Result<bool, TrustRefusal> {
    let c = object(capsule).map_or_else(|| refuse(TrustRow::Incomplete, "capsule"), Ok)?;
    let heads = c.get("heads") == Some(&V::Null);
    let history = c.get("history") == Some(&V::Null);
    if !heads && !history {
        return Ok(false);
    }
    let roles = field(capsule, "roles")?;
    let unbootstrapped = ROLES.iter().try_fold(true, |all, name| {
        let role = field(roles, name)?;
        Ok(all
            && field(role, "state")? == &V::String("ST-UNBOOTSTRAPPED".into())
            && field(role, "accepted")? == &V::Null)
    })?;
    if heads && history && unbootstrapped {
        Ok(true)
    } else {
        refuse(TrustRow::Incomplete, "pre-acceptance-shape")
    }
}
/// Item 11: the descriptor's event list is bounded before it is bound.
fn check_event_bound(descriptor: &V) -> Result<(), TrustRefusal> {
    match object(descriptor).and_then(|d| d.get("events")) {
        Some(V::Array(events)) if events.len() <= MAX_VIEW_EVENTS => Ok(()),
        Some(V::Array(events)) => refuse(TrustRow::Budget, ("events", events.len())),
        _ => refuse(TrustRow::Incomplete, "events"),
    }
}
fn bindings_row(e: &current_record_bindings::Error) -> TrustRow {
    use current_record_bindings::Error as E;
    match e {
        E::Budget(b) => budget_row(b),
        _ => TrustRow::Incomplete,
    }
}

/// Items 1 and 11 (r8, X4T-a2): at most one `accepted.by` event per role is
/// opened by reference, so at most six.
pub(crate) const MAX_ACCEPTED_BY_READS: usize = ROLES.len();

/// Item 1 (r8): each accepted role's `accepted.by` names an accepted role
/// event of that role. One in the loaded chain is checked there; one outside
/// it is opened by its reference (one read, never its `previous`) and must be
/// a `role-event` of that role with outcome `accepted`, in this store, earlier
/// than the current publication. `history` is never walked.
fn check_accepted_by(
    b: &mut super::Budget,
    capsule: &V,
    descriptor: &V,
    trace: &LocalTrace,
    store: &mut impl super::M::Store,
) -> Result<[(State, bool); 6], TrustRefusal> {
    let roles = field(capsule, "roles")?;
    let sid = field(field(capsule, "store")?, "storeInstanceId")?.clone();
    // The current publication starts at its first listed event; a descriptor
    // listing none starts after `eventHead`.
    let before = match field(descriptor, "events")? {
        V::Array(events) if !events.is_empty() => {
            int(field(field(&events[0], "event")?, "sequence")?)?
        }
        V::Array(_) => match field(capsule, "eventHead")? {
            V::Null => 1,
            head => int(field(head, "sequence")?)?.saturating_add(1),
        },
        _ => return refuse(TrustRow::Incomplete, "events"),
    };
    let mut out = [(State::Unbootstrapped, false); 6];
    let mut opened = 0;
    for (i, name) in ROLES.iter().enumerate() {
        let role = field(roles, name)?;
        let state = match field(role, "state")? {
            V::String(s) => {
                state_of(s).map_or_else(|| refuse(TrustRow::Incomplete, "state"), Ok)?
            }
            _ => return refuse(TrustRow::Incomplete, "state"),
        };
        let accepted = field(role, "accepted")?;
        if *accepted != V::Null {
            let by = field(accepted, "by")?;
            let in_chain = trace.captures().iter().find(|c| c.reference() == by);
            let event = match in_chain {
                Some(c) => c.value().clone(),
                None => {
                    opened += 1;
                    if opened > MAX_ACCEPTED_BY_READS {
                        return refuse(TrustRow::Budget, "accepted.by");
                    }
                    let raw = b
                        .load_at(super::M::Collection::Events, by, None, store)
                        .or_else(|e| refuse(budget_row(&e), e))?;
                    let event = shapes::admit(Definition::TrustEventV1, &raw)
                        .or_else(|e| refuse(TrustRow::Incomplete, e))?;
                    let sequence = int(field(&event, "sequence")?)?;
                    if field(&event, "store")? != &sid
                        || field(by, "storeInstanceId")? != &sid
                        || int(field(by, "sequence")?)? != sequence
                        || sequence >= before
                    {
                        return refuse(TrustRow::Incomplete, ("accepted.by-earlier", name));
                    }
                    event
                }
            };
            let e = object(&event).map_or_else(|| refuse(TrustRow::Incomplete, "event"), Ok)?;
            let text = |k: &str| match e.get(k) {
                Some(V::String(s)) => Some(s.as_str()),
                _ => None,
            };
            if text("kind") != Some("role-event")
                || text("role") != Some(name)
                || text("outcome") != Some("accepted")
            {
                return refuse(TrustRow::Incomplete, ("accepted.by", name));
            }
        }
        out[i] = (state, *accepted != V::Null);
    }
    Ok(out)
}

/// The inventory and quorum owners carry a budget read's error as a typed
/// `Input` several owners deep. A failed read takes `budget_row`; only a
/// failure of the documents or quorums themselves is not admissible.
fn quorum_row(e: &ordinary_quorums::Error, subject: &'static str) -> TrustRow {
    use ordinary_quorums::Error as E;
    match e {
        E::Input(b) => budget_row(b),
        E::Retained(r) => inventory_row(r, subject),
        _ => TrustRow::PayloadNotAdmissible(subject),
    }
}
fn inventory_row(e: &ordinary_inventory::Error, subject: &'static str) -> TrustRow {
    use ordinary_inventory::Error as E;
    match e {
        E::Input(b) | E::Bundle(ordinary_bundle::Error::Input(b)) => budget_row(b),
        _ => TrustRow::PayloadNotAdmissible(subject),
    }
}
fn metadata_row(e: &ordinary_metadata::Error) -> TrustRow {
    use ordinary_metadata::{Error as E, catalog::Error as C};
    use recovery_catalog::Error as S;
    match e {
        E::Input(b) | E::Catalog(C::Input(b)) | E::Catalog(C::Schema(S::Input(b))) => budget_row(b),
        E::Catalog(C::Quorums(q)) => quorum_row(q, "inventory"),
        E::Catalog(C::Schema(S::Quorums(q))) => recovery_quorum_row(q),
        _ => TrustRow::PayloadNotAdmissible("inventory"),
    }
}
/// The catalog schema owner's quorums, which carry their own retained index.
fn recovery_quorum_row(e: &incoming_recovery_quorums::Error) -> TrustRow {
    use incoming_recovery_quorums::Error as E;
    use retained_recovery_payload::Error as R;
    match e {
        E::Input(b) | E::Retained(R::Input(b)) => budget_row(b),
        _ => TrustRow::PayloadNotAdmissible("inventory"),
    }
}
fn chain_row(e: &ChainError) -> TrustRow {
    let link = |i: &usize| format!("link:{i}");
    match e {
        ChainError::Limit => TrustRow::Budget,
        ChainError::Gap(i) => TrustRow::Root("ROOT.CHAIN_GAP", link(i)),
        ChainError::Backdated(i) => TrustRow::Root("ROOT.CHAIN_BACKDATED", link(i)),
        ChainError::OldThreshold(i) => TrustRow::Root("ROOT.CHAIN_OLD_THRESHOLD", link(i)),
        ChainError::NewThreshold(i) => TrustRow::Root("ROOT.CHAIN_NEW_THRESHOLD", link(i)),
        ChainError::FinalExpired => TrustRow::Root("ROOT.FINAL_EXPIRED", "final".into()),
        ChainError::FinalFuture => TrustRow::Root("ROOT.FINAL_FUTURE", "final".into()),
        ChainError::ExpiredNoChain => TrustRow::Root("ROOT.EXPIRED_NO_CHAIN", "final".into()),
        ChainError::StateInconsistent => TrustRow::Root("ROOT.STATE_INCONSISTENT", "chain".into()),
        ChainError::Unsupported(i) => TrustRow::Root("ROOT.SCHEMA_UNSUPPORTED", link(i)),
        ChainError::Payload(_) | ChainError::Envelope(_) => {
            TrustRow::PayloadNotAdmissible("root-chain")
        }
        ChainError::AnchorUnsupported | ChainError::Time => {
            TrustRow::Root("ROOT.SCHEMA_UNSUPPORTED", "anchor".into())
        }
    }
}
fn roots_row(e: &ordinary_roots::Error) -> TrustRow {
    use ordinary_roots::Error as E;
    match e {
        E::Input(b) => budget_row(b),
        E::Chain(c) => chain_row(c),
        E::Envelope | E::FirstQuorum => TrustRow::PayloadNotAdmissible("root"),
        E::Shared(q) => quorum_row(q, "shared"),
        // Item 10 (r10): a closure chain that is empty or does not end on
        // `heads.root.document` (`EmptyChain`, `FinalIdentity`) is incomplete.
        _ => TrustRow::Incomplete,
    }
}
fn clock_input_row(e: &ClockInputError) -> TrustRow {
    match e {
        ClockInputError::Input(b) => budget_row(b),
        ClockInputError::Head(h) => roots_row(h),
        ClockInputError::Times(TimesError::Input(b)) => budget_row(b),
        ClockInputError::Times(TimesError::Calendar) => TrustRow::Incomplete,
        ClockInputError::Times(TimesError::Rooted(RootedError::Input(b))) => budget_row(b),
        ClockInputError::Times(TimesError::Rooted(RootedError::Roots(r))) => roots_row(r),
        ClockInputError::Times(TimesError::Rooted(RootedError::Scope(s))) => match s {
            ScopeError::Input(b) => budget_row(b),
            ScopeError::ComponentEnvelope | ScopeError::ComponentQuorum => {
                TrustRow::PayloadNotAdmissible("component")
            }
            ScopeError::Inventory(i) => metadata_row(i),
            ScopeError::Context(_) => TrustRow::Incomplete,
        },
    }
}

/// Items 1 and 3: bind the root head, open its admission record, and
/// authenticate the accepted state through the existing retained-head
/// composition, at the view's chain budget: from the accepted root N, the
/// closure's first `rootChain` document, to the signing root M, `heads.root`
/// (r10, X4T-a3).
fn authenticate(
    b: &mut super::Budget,
    capsule: &V,
    descriptor: &V,
    roles: &[(State, bool); 6],
    store: &mut impl super::M::Store,
) -> Result<(OrdinaryClockInput, V), TrustRefusal> {
    let capsule_clock = clock::capsule_clock(b, capsule, descriptor, None)
        .or_else(|e| refuse(TrustRow::Incomplete, e))?;
    // The P0 shape was refused before any read; any other phase is misbound.
    if capsule_clock.phase() != Phase::Retained {
        return refuse(TrustRow::Incomplete, "phase");
    }
    let head = ordinary_roots::bind_retained_head(b, capsule_clock, store)
        .or_else(|e| refuse(roots_row(&e), e))?;
    // Item 1: the root admission record, which no binder opens.
    let raw = b
        .load(super::M::Collection::Records, head.admission(), store)
        .or_else(|e| refuse(budget_row(&e), e))?;
    let admission = shapes::admit(Definition::RootAdmissionNodeV1, &raw)
        .or_else(|e| refuse(TrustRow::Incomplete, e))?;
    if field(&admission, "root")? != head.document() {
        return refuse(TrustRow::Incomplete, "root-admission-root");
    }
    let closure_ref = field(&admission, "parent")?.clone();
    // Item 3 (r10, X4T-a3): `heads.root` is the signing root M. The accepted
    // root N is the closure's first `rootChain` document, and the chain must
    // end on exactly `heads.root.document`, or the installation is incomplete.
    let anchor = ordinary_roots::bind_chain_anchor(b, &closure_ref, &head, store)
        .or_else(|e| refuse(roots_row(&e), e))?;
    let signing_root_ref = head.document().clone();
    let retained = roles.map(|(state, established)| RetainedRole {
        state,
        established,
        recovery_revoked: None,
    });
    let times = {
        let signing_root = head.root();
        prepare_authenticated_times(
            b,
            &closure_ref,
            &signing_root_ref,
            signing_root,
            &std::collections::BTreeSet::new(),
            AuthenticationContext {
                roles: ScopeContext {
                    retained,
                    old_hits: [false; 6],
                    recovery: [None; 6],
                },
                roots: anchor.authentication_context(VIEW_CHAIN),
            },
            store,
        )
        .map_err(ClockInputError::Times)
        .or_else(|e| refuse(clock_input_row(&e), e))?
    };
    Ok((OrdinaryClockInput { head, times }, admission))
}

/// Items 1 and 4: the catalog and revocation heads, their admission records,
/// `history` and `timeEvidence`, each opened here by `Budget::load`.
struct Heads {
    time_evidence: V,
    revocation_version: i64,
    index_snapshot_version: i64,
    revoked_subjects: Vec<(String, String)>,
    catalog: super::super::EnvelopeEvidence,
    revocation: super::super::admitted_revocations::RevocationEvidence,
}
fn open_heads(
    b: &mut super::Budget,
    capsule: &V,
    input: &OrdinaryClockInput,
    root_admission_ref: &V,
    store: &mut impl super::M::Store,
) -> Result<Heads, TrustRefusal> {
    use super::M::Collection;
    let heads = field(capsule, "heads")?;
    let root = input.head.root();
    let mut load = |b: &mut super::Budget, c: Collection, r: &V| {
        b.load(c, r, store).or_else(|e| refuse(budget_row(&e), e))
    };
    let mut document =
        |b: &mut super::Budget, name: &str| -> Result<(Vec<u8>, V, V), TrustRefusal> {
            let head = field(heads, name)?;
            let doc = field(head, "document")?;
            let body = load(b, Collection::Objects, field(doc, "body")?)?;
            let envelope = load(b, Collection::Objects, field(doc, "envelope")?)?;
            let envelope = super::super::super::metadata::parse(&envelope)
                .or_else(|_| refuse(TrustRow::PayloadNotAdmissible("envelope"), name))?;
            let raw = load(b, Collection::Records, field(head, "admission")?)?;
            let admission = shapes::admit(Definition::MetadataAdmissionNodeV1, &raw)
                .or_else(|e| refuse(TrustRow::Incomplete, e))?;
            if field(&admission, "document")? != doc
                || field(&admission, "admittingRoot")? != root_admission_ref
            {
                return refuse(TrustRow::Incomplete, (name, "admission"));
            }
            Ok((body.to_vec(), envelope, head.clone()))
        };
    // The catalog: its envelope reverified against the accepted root. Its
    // quorum is judged in `admit_revocation`, with the current keyIds excluded.
    let (catalog_body, catalog_env, catalog_head) = document(b, "catalog")?;
    let catalog = verify_envelope(
        CURRENT_ENVELOPE_READER,
        root,
        &catalog_body,
        Some(&catalog_env),
        EnvelopeKind::Catalog,
        None,
    )
    .or_else(|e| refuse(TrustRow::PayloadNotAdmissible("catalog"), e))?;
    let catalog_value = super::super::super::metadata::parse(&catalog_body)
        .or_else(|_| refuse(TrustRow::PayloadNotAdmissible("catalog"), "body"))?;
    let index_snapshot_version = int(field(&catalog_value, "snapshotVersion")?)?;
    if int(field(&catalog_head, "version")?)? != index_snapshot_version {
        return refuse(TrustRow::Incomplete, "catalog-version");
    }
    // The revocation list: verify_revocation over exactly the loaded bytes,
    // with the keys revoked before it (none are walked: item 11).
    let (revocation_body, revocation_env, revocation_head) = document(b, "revocation")?;
    let empty = std::collections::BTreeSet::new();
    let revocation = verify_revocation(root, &revocation_body, &revocation_env, &empty)
        .or_else(|e| refuse(TrustRow::PayloadNotAdmissible("revocation"), e))?;
    if int(field(&revocation_head, "version")?)? != revocation.version() {
        return refuse(TrustRow::Incomplete, "revocation-version");
    }
    let mut revoked_subjects = Vec::new();
    if let Some(V::Array(entries)) =
        object(revocation.envelope().payload()).and_then(|o| o.get("entries"))
    {
        for entry in entries {
            if let (Some(V::String(kind)), Some(V::String(subject))) = (
                object(entry).and_then(|o| o.get("subjectKind")),
                object(entry).and_then(|o| o.get("subject")),
            ) {
                revoked_subjects.push((kind.clone(), subject.clone()));
            }
        }
    }
    // History and the clock's time evidence.
    let raw = load(b, Collection::Records, field(capsule, "history")?)?;
    let history = shapes::admit(Definition::RevocationHistoryNodeV1, &raw)
        .or_else(|e| refuse(TrustRow::Incomplete, e))?;
    if field(&history, "list")? != field(&revocation_head, "document")? {
        return refuse(TrustRow::Incomplete, "history-list");
    }
    let time = field(field(capsule, "clock")?, "timeEvidence")?;
    let raw = load(b, Collection::Records, time)?;
    let time_evidence = shapes::admit(Definition::TimeEvidenceV1, &raw)
        .or_else(|e| refuse(TrustRow::Incomplete, e))?;
    Ok(Heads {
        time_evidence,
        revocation_version: revocation.version(),
        index_snapshot_version,
        revoked_subjects,
        catalog,
        revocation,
    })
}

/// Item 4: what the admitted closure's components are, as the revocation
/// list's closed subject kinds name them.
struct ClosureComponents<'a> {
    /// `release`: the running core closure, which the installation's accepted
    /// core equals (X3a's endpoint join).
    release: &'a str,
    /// `keyId`: every key whose valid signature the closure's documents carry,
    /// before any revocation filter.
    signing_keys: BTreeSet<[u8; 32]>,
    /// `namespace`: the namespaces those envelopes are signed for.
    namespaces: BTreeSet<String>,
    /// `catalogSnapshot`: the admitted catalog's snapshot version.
    catalog_snapshot: i64,
}
/// The closure's signed documents: the root head, the catalog and revocation
/// heads, the payload manifest and each non-root document of its closure.
fn closure_components<'a>(
    input: &OrdinaryClockInput,
    heads: &Heads,
    release: &'a str,
) -> Result<ClosureComponents<'a>, TrustRefusal> {
    let root = input.head.root();
    let mut signing_keys = BTreeSet::new();
    let mut namespaces = BTreeSet::new();
    let mut verified = |kind, body: &[u8], envelope: &[u8], subject| {
        let envelope = super::super::super::metadata::parse(envelope)
            .or_else(|_| refuse(TrustRow::PayloadNotAdmissible(subject), "envelope"))?;
        let evidence = verify_envelope(
            CURRENT_ENVELOPE_READER,
            root,
            body,
            Some(&envelope),
            kind,
            None,
        )
        .or_else(|e| refuse(TrustRow::PayloadNotAdmissible(subject), e))?;
        signing_keys.extend(evidence.quorum().valid_before_revocation().iter().copied());
        namespaces.insert(evidence.quorum().namespace().to_owned());
        Ok(())
    };
    verified(
        EnvelopeKind::Root,
        input.head.body(),
        input.head.envelope(),
        "root",
    )?;
    let shared = input.times.proof.scoped.inventory.shared();
    for pair in shared.retained().pairs().values() {
        if pair.kind() != EnvelopeKind::Root {
            verified(pair.kind(), pair.body(), pair.envelope(), "inventory")?;
        }
    }
    for quorum in [
        shared.retained().bundle().proof().quorum(),
        heads.revocation.envelope().quorum(),
    ] {
        signing_keys.extend(quorum.valid().iter().copied());
        namespaces.insert(quorum.namespace().to_owned());
    }
    let catalog = heads.catalog.quorum();
    signing_keys.extend(catalog.valid_before_revocation().iter().copied());
    namespaces.insert(catalog.namespace().to_owned());
    Ok(ClosureComponents {
        release,
        signing_keys,
        namespaces,
        catalog_snapshot: heads.index_snapshot_version,
    })
}
/// The admitted revocation outcome the epoch and view carry.
struct Admitted {
    revocation_version: i64,
    index_snapshot_version: i64,
    revoked_subjects: Vec<(String, String)>,
    revocation: super::super::admitted_revocations::RevocationEvidence,
}
/// Item 4, after `verify_revocation`: an entry whose subject kind and subject
/// name a closure component refuses on the continuation row, subject that
/// component. The current list's keyIds are then excluded from the catalog's
/// and the list's own quorums, which must still be met. The keys revoked
/// before this list stay the empty set.
fn admit_revocation(
    heads: Heads,
    closure: &ClosureComponents<'_>,
) -> Result<Admitted, TrustRefusal> {
    let mut keys = BTreeSet::new();
    for (kind, subject) in &heads.revoked_subjects {
        let key = (kind == "keyId")
            .then(|| super::super::decode_hex32(subject))
            .transpose()
            .or_else(|_| refuse(TrustRow::PayloadNotAdmissible("revocation"), "keyId"))?;
        let named = match kind.as_str() {
            "release" => subject == closure.release,
            "keyId" => key.is_some_and(|k| closure.signing_keys.contains(&k)),
            "namespace" => closure.namespaces.contains(subject),
            "catalogSnapshot" => *subject == closure.catalog_snapshot.to_string(),
            _ => false,
        };
        if named {
            return refuse(
                TrustRow::Continuation(format!("{kind}:{subject}")),
                "revoked-component",
            );
        }
        keys.extend(key);
    }
    if filter_envelope_revoked(heads.catalog, &keys)
        .quorum()
        .state()
        != &QuorumState::Met
    {
        return refuse(TrustRow::PayloadNotAdmissible("catalog"), "quorum");
    }
    // The list does not exempt itself.
    if heads
        .revocation
        .envelope()
        .quorum()
        .filtered_again(&keys)
        .state()
        != &QuorumState::Met
    {
        return refuse(TrustRow::PayloadNotAdmissible("revocation"), "quorum");
    }
    Ok(Admitted {
        revocation_version: heads.revocation_version,
        index_snapshot_version: heads.index_snapshot_version,
        revoked_subjects: heads.revoked_subjects,
        revocation: heads.revocation,
    })
}

/// Item 11: the bytes the root chain retained on the view's ledger, which
/// `ChainBudget` bounds on its own: the recorded roots' bodies and envelopes,
/// each counted once, less the root head's, which is a closure member.
fn chain_bytes(input: &OrdinaryClockInput) -> usize {
    let shared = input.times.proof.scoped.inventory.shared();
    let head = [input.head.body(), input.head.envelope()].map(opensip_identity::raw_sha256);
    let mut seen = BTreeSet::new();
    shared
        .unresolved_roots()
        .iter()
        .filter_map(|path| shared.retained().pairs().get(path))
        .flat_map(|pair| [pair.body(), pair.envelope()])
        .filter(|raw| {
            let digest = opensip_identity::raw_sha256(raw);
            !head.contains(&digest) && seen.insert(digest)
        })
        .map(<[u8]>::len)
        .sum()
}

/// Item 11: the closure's own stored-bytes total, the chain's bytes excluded,
/// is at most 40 MiB. `retained` is all the view retained, chain included.
fn closure_total(retained: usize, chain: usize) -> Result<(), TrustRefusal> {
    let closure = retained.saturating_sub(chain);
    if closure > MAX_CLOSURE_BYTES {
        return refuse(TrustRow::Budget, ("closure-bytes", closure));
    }
    Ok(())
}

/// Item 1: the role standing, exactly the role machine's join over core,
/// index and component. Every state, Recovery included, goes through it; the
/// other three roles are not part of the join.
fn standing_of(roles: &[(State, bool); 6]) -> Result<TrustStanding, TrustRefusal> {
    use super::super::super::role_machine::{Standing, standing};
    let state = |name: &str| roles[ROLES.iter().position(|r| *r == name).unwrap()].0;
    let (core, index, component) = (state("TR-CORE"), state("TR-INDEX"), state("TR-COMPONENT"));
    match standing(core, index, component) {
        Standing::RefuseCore => refuse(
            TrustRow::Continuation(format!("core:{}", token(core))),
            core,
        ),
        Standing::RefuseIndex => refuse(
            TrustRow::IndexContinuation(format!("index:{}", token(index))),
            index,
        ),
        Standing::RefuseComponent => refuse(
            TrustRow::ComponentContinuation(format!("component:{}", token(component))),
            component,
        ),
        Standing::ExistingOnly => Ok(TrustStanding::ExistingOnly),
        Standing::InstallGateRequiredForNewProcess => {
            Ok(TrustStanding::InstallGateRequiredForNewProcess)
        }
    }
}

/// X4T r12 keeps a clocked-expiry refusal on the existing core detail.
/// The stored-state join alone selects X4T-c's role-specific public details.
fn clocked_standing_of(roles: &[(State, bool); 6]) -> Result<TrustStanding, TrustRefusal> {
    standing_of(roles).map_err(|mut refusal| {
        refusal.row = match refusal.row {
            TrustRow::IndexContinuation(subject) | TrustRow::ComponentContinuation(subject) => {
                TrustRow::Continuation(subject)
            }
            row => row,
        };
        refusal
    })
}

/// Item 6 (unit X4-F1): a reread's expiry and staleness applied to the
/// stored roles through the role machine's own `EV-CLOCK` (`clock`), on law
/// X4B r5 item 4's mapping of documents to roles, the one the law states:
/// the signing root's expiry to TR-BUNDLE, TR-COMPONENT and TR-CORE; the
/// root's or the catalog's to TR-INDEX; the list's staleness to all four.
/// TR-PROFILE and TR-REPAIR, which no payload carries and the standing's join
/// does not read, keep their stored states.
fn clock_roles(
    roles: [(State, bool); 6],
    (root, catalog, stale): (bool, bool, bool),
) -> [(State, bool); 6] {
    let mut out = roles;
    for (i, name) in ROLES.iter().enumerate() {
        let expired = match *name {
            "TR-BUNDLE" | "TR-COMPONENT" | "TR-CORE" => root,
            "TR-INDEX" => root || catalog,
            _ => continue,
        };
        out[i].0 = super::super::super::role_machine::clock(out[i].0, expired, stale);
    }
    out
}

/// Items 1 to 6 over a bound capsule. Shared by the in-memory path and the
/// native capture; `store` is the same store the binders used.
fn admit_bound(
    b: &mut super::Budget,
    capsule: &V,
    descriptor: &V,
    bindings: &CurrentRecordBindings,
    inputs: &ViewInputs<'_>,
    start_bytes: usize,
    store: &mut impl super::M::Store,
) -> Result<Admission, TrustRefusal> {
    let roles = check_accepted_by(b, capsule, descriptor, bindings.trace(), store)?;
    // Item 1: the join runs over the bound role states before authentication,
    // which needs a live ceremony's evidence for a role in Recovery. The
    // view's standing is the second join's, over the clocked states (r12).
    standing_of(&roles)?;
    let (input, root_admission) = authenticate(b, capsule, descriptor, &roles, store)?;
    // The root admission is the one `authenticate` opened and checked.
    let root_admission_ref = field(field(field(capsule, "heads")?, "root")?, "admission")?.clone();
    drop(root_admission);
    let heads = open_heads(b, capsule, &input, &root_admission_ref, store)?;
    closure_total(b.counters().2 - start_bytes, chain_bytes(&input))?;
    // Item 7 checks 1 and 2 (r8): on every read; a fenced refusal is the
    // `trust-rollback` row, a reread's is X4's callback error (item 9).
    let floors = Floors::of_clock(field(capsule, "clock")?)?;
    check_evidence_floors(&floors, &heads.time_evidence)?;
    // Item 4: no component of the admitted closure is revoked.
    let components = closure_components(&input, &heads, inputs.core_closure)?;
    let heads = admit_revocation(heads, &components)?;
    let closure = ViewClosure {
        release: components.release.to_owned(),
        signing_keys: components.signing_keys,
        namespaces: components.namespaces,
        catalog_snapshot: components.catalog_snapshot,
    };
    let root_version = int(field(input.head.root().value(), "rootVersion")?)?;
    // Item 5: the empty global policy in M2, and the project's if supplied.
    let effective = policy::merge(
        b,
        Source::Missing,
        match inputs.project_policy {
            Some(p) => Context::Project(Source::Body(p)),
            None => Context::Global,
        },
    )
    .or_else(|e| refuse(TrustRow::Incomplete, e))?;
    // Item 6: time is admitted on the fenced read only.
    let mut pending = None;
    let mut handoff = None;
    let (roles, standing, time) = match inputs.mode {
        // Item 6 (unit X4-F1): a reread re-admits no time and writes nothing.
        // It evaluates S4's expiry and staleness at its instant, applies them
        // to the stored roles through EV-CLOCK, and joins the standing again:
        // a continuation refusal is X4's callback error (item 9).
        ReadMode::Reread { at } => {
            let expired = crate::trust_time::evaluate_reread_expiry(&input, at)
                .or_else(|e| refuse(TrustRow::Incomplete, e))?;
            let roles = clock_roles(roles, expired);
            (roles, clocked_standing_of(&roles)?, None)
        }
        ReadMode::Fenced { report } => {
            let observation = inputs
                .observation
                .map_or_else(|| refuse(TrustRow::HostIo, "observation"), Ok)?;
            let observation =
                RecordedObservation::admit(observation).or_else(|e| refuse(TrustRow::HostIo, e))?;
            let (mono, boot) = (observation.mono(), observation.boot().to_owned());
            let proposal =
                crate::trust_time::evaluate_retained_ordinary(input, observation, report)
                    .or_else(|e| refuse(TrustRow::Incomplete, e))?;
            let admission = proposal.admission();
            if !report {
                pending = Some(PendingWrite(proposal));
            }
            if let Some(refusal) = admission.refusal {
                return refuse(
                    match refusal {
                        TimeRefusal::PayloadFuture | TimeRefusal::TimeRange => {
                            TrustRow::PayloadNotAdmissible("time")
                        }
                        TimeRefusal::NoContext => TrustRow::NoAdmittedTimeContext,
                        TimeRefusal::InSession => TrustRow::ClockExcursion("in-session"),
                        TimeRefusal::BeyondHorizon => TrustRow::ClockExcursion("beyond-horizon"),
                    },
                    refusal,
                );
            }
            // Item 6 (r12, unit X4-F2): EV-CLOCK at tEval, the admission's
            // last decision, after S4's own refusals. S4's three states at
            // tEval, which every admitted evaluation carries, go through the
            // reread's mapping and join. Nothing is recorded: the clocked
            // states live in the view only. A refusal is not a view; it keeps
            // the pending write-ahead, which item 7 performs before it.
            let expired = admission
                .expired
                .map_or_else(|| refuse(TrustRow::HostIo, "expiry"), Ok)?;
            let roles = clock_roles(roles, expired);
            let standing = match clocked_standing_of(&roles) {
                Ok(standing) => standing,
                Err(refusal) => {
                    return Ok(Admission::Clocked(Box::new(ClockedRefusal {
                        refusal,
                        floors,
                        time: admission,
                        pending,
                    })));
                }
            };
            // Item 6 (unit X4-F1): the clock the operation's rereads advance.
            handoff = admission.evaluation.map(|evaluation| HandoffClock {
                evaluation,
                mono,
                boot,
            });
            (roles, standing, Some(admission))
        }
    };
    Ok(Admission::View(Box::new(AdmittedCurrentTrust {
        roles,
        standing,
        epoch: TrustEpoch {
            root_version,
            index_snapshot_version: heads.index_snapshot_version,
            revocation_version: heads.revocation_version,
            permission_policy_digest: effective.digest(),
        },
        time,
        revoked_subjects: heads.revoked_subjects,
        floors,
        pending,
        closure,
        revocation: AdmittedRevocation(heads.revocation),
        handoff,
    })))
}

/// Items 2 and 11: the shared preamble. The store's schema, then the event
/// bound, before the capsule is bound.
fn preamble(descriptor: &V, expected_store: &V) -> Result<(), TrustRefusal> {
    let schema = field(expected_store, "stateSchema").and_then(int)?;
    if !(1..=2).contains(&schema) {
        return refuse(TrustRow::StateSchemaUnsupported, schema);
    }
    check_event_bound(descriptor)
}

/// The admission over a supplied store and an already-captured capsule, for
/// every caller but item 7's fenced first read: a clocked refusal (item 6,
/// r12) is returned as the refusal, and nothing is written here.
pub(super) fn admit_current_trust(
    b: &mut super::Budget,
    expected_store: &V,
    capsule: &V,
    inputs: &ViewInputs<'_>,
    store: &mut impl super::M::Store,
) -> Result<AdmittedCurrentTrust, TrustRefusal> {
    admit_current(b, expected_store, capsule, inputs, store)?.into_view()
}
/// The admission over a supplied store and an already-captured capsule (the
/// fenced first read takes X3a's retained capsule, item 8). The descriptor
/// is loaded through `store` by the capsule's reference.
fn admit_current(
    b: &mut super::Budget,
    expected_store: &V,
    capsule: &V,
    inputs: &ViewInputs<'_>,
    store: &mut impl super::M::Store,
) -> Result<Admission, TrustRefusal> {
    if is_p0(capsule)? {
        return refuse(TrustRow::NoAdmittedTimeContext, "pre-acceptance");
    }
    let start = b.counters().2;
    let publication = field(capsule, "publication")?;
    let initial = (field(publication, "previousCapsule")? == &V::Null)
        .then(|| field(field(capsule, "store").ok()?, "storeInstanceId").ok())
        .flatten();
    let raw = b
        .load_at(
            super::M::Collection::Publications,
            publication,
            initial,
            store,
        )
        .or_else(|e| refuse(budget_row(&e), e))?;
    let descriptor = shapes::admit(Definition::PublicationDescriptorV1, &raw)
        .or_else(|e| refuse(TrustRow::Incomplete, e))?;
    preamble(&descriptor, expected_store)?;
    let bindings = current_record_bindings::bind(b, expected_store, capsule, &descriptor, store)
        .or_else(|e| refuse(bindings_row(&e), e))?;
    admit_bound(b, capsule, &descriptor, &bindings, inputs, start, store)
}

/// Item 9's unfenced reread (and the native path generally): `capture_p2`
/// opens `state.v1` by name through the held fence's retained handles, then
/// the same admission runs over its native store; `state.v1` is rechecked
/// last (item 2 step 5). One attempt; no retry.
#[cfg(target_os = "macos")]
pub(super) fn admit_native(
    b: &mut super::Budget,
    fence: &dyn HeldFence,
    expected_store: &V,
    inputs: &ViewInputs<'_>,
) -> Result<AdmittedCurrentTrust, TrustRefusal> {
    let start = b.counters().2;
    let mut current = super::super::native_current::capture_p2(b, fence, expected_store)
        .or_else(|e| refuse(native_row(&e), e))?;
    let (capsule, descriptor, bindings, store) = current.parts_mut();
    let (capsule, descriptor) = (capsule.clone(), descriptor.clone());
    if is_p0(&capsule)? {
        return refuse(TrustRow::NoAdmittedTimeContext, "pre-acceptance");
    }
    preamble(&descriptor, expected_store)?;
    let result = admit_bound_native(b, &capsule, &descriptor, bindings, inputs, start, store);
    let admission = complete(store, result)?;
    current.recheck().or_else(|e| refuse(native_row(&e), e))?;
    admission.into_view()
}
#[cfg(target_os = "macos")]
fn admit_bound_native(
    b: &mut super::Budget,
    capsule: &V,
    descriptor: &V,
    bindings: &CurrentRecordBindings,
    inputs: &ViewInputs<'_>,
    start: usize,
    store: &mut NativeStore<'_>,
) -> Result<Admission, TrustRefusal> {
    admit_bound(b, capsule, descriptor, bindings, inputs, start, store)
}
#[cfg(target_os = "macos")]
fn complete<T>(
    store: &mut NativeStore<'_>,
    result: Result<T, TrustRefusal>,
) -> Result<T, TrustRefusal> {
    store.complete(result).map_err(|e| match e {
        ReadCompletionError::Native(source) => TrustRefusal {
            row: native_read_row(&source),
            cause: format!("{source:?}"),
        },
        ReadCompletionError::Logical(refusal) => refusal,
    })
}
/// A native read: a record that is absent, changed or not its digest is an
/// incomplete installation; a budget limit is the budget row; the rest is I/O.
#[cfg(target_os = "macos")]
fn native_read_row(e: &super::super::native_record_capture::Error) -> TrustRow {
    use super::super::native_record_capture::Error as E;
    match e {
        E::Budget(b) => budget_row(b),
        E::Native(_) | E::Fence(_) => TrustRow::HostIo,
        _ => TrustRow::Incomplete,
    }
}
#[cfg(target_os = "macos")]
fn native_row(e: &super::super::native_current::Error) -> TrustRow {
    use super::super::native_current::Error as E;
    match e {
        E::Budget(b) => budget_row(b),
        E::Bindings(b) => bindings_row(b),
        E::Immutable(n) => native_read_row(n),
        E::Native(_) | E::Fence(_) => TrustRow::HostIo,
        _ => TrustRow::Incomplete,
    }
}

/// A budget at exactly item 11's view ceiling.
pub(super) fn view_budget() -> super::Budget<'static, 'static> {
    super::Budget::new(TRUST_VIEW_COST.0, TRUST_VIEW_COST.1, TRUST_VIEW_COST.2)
        .expect("ceiling inside the budget's limits")
}

// Law X4T r9 items 7 and 8 (X4T-b): the fenced first read's write-ahead.
#[cfg(target_os = "macos")]
mod floor_publication {
    include!("floor_publication.rs");
}
#[cfg(target_os = "macos")]
pub(crate) use floor_publication::ConfirmedCurrent;
// The custody gate's own test of the owner advance (item 7) reaches these.
#[cfg(all(test, target_os = "macos"))]
pub(crate) use floor_publication::{RetainedCurrentTrust, publish};
// Law X9 r1 item 6 / X8 r3 item 4b: the shared fenced publisher.
#[cfg(all(
    any(test, feature = "crash-matrix", feature = "scenario-fixtures"),
    target_os = "macos"
))]
pub(crate) use floor_publication::publish_store_fenced;

// Law X4 r7 items 2 and 5 (unit X4a): the operation's retained trust
// handles, the unfenced observation through them and the S6 predicate.
#[cfg(target_os = "macos")]
mod live_observation {
    include!("live_observation.rs");
}
#[cfg(all(test, target_os = "macos"))]
pub(crate) use live_observation::ObservationPoint;
#[cfg(target_os = "macos")]
pub(crate) use live_observation::{
    LiveObservation, ObservationHook, Observed, RetainedTrustHandles, TrustInvocation,
    fenced_operation_read,
};

// Law X4B r5 items 2 to 6 (X4B-a): the first trust acceptance producer;
// item 1 (X4B-b): its F-absent branch inside the fenced first read, whose
// only payload source is the write receipt's running core. X4B-c: visible
// within `root_payload` so X4T-0 builds its accepted stores through it.
#[cfg(target_os = "macos")]
pub(in crate::trust::root_payload) mod trust_bootstrap {
    include!("trust_bootstrap.rs");
}
#[cfg(target_os = "macos")]
pub(crate) use trust_bootstrap::BootstrapSource;

#[cfg(test)]
mod tests {
    include!("current_trust_admission_tests.rs");
}
