// Law X4T r9 items 7 and 8 (unit X4T-b): the fenced first read with its S4
// write-ahead floor publication, the retained `state.v1` owner and its one
// advance path, and the handoff rollback check against this fence hold's own
// floors (item 7 check 3; checks 1 and 2 run in every admission). The
// publication protocol (`publish`) has one owner and is shared with X4B-a:
// dependencies through 467's private-file producer, each with its file and
// directory barriers, then the pointer through X3b's private file protocol
// (exclusive temporary name, F_FULLFSYNC, rename, directory barrier, reopen
// and confirm), then the confirming reread that advances the owner. Under the
// installation fence only, never under a lease; the caller holds no project
// lock. Nothing is retried or deleted. X4a's lease-free point runs it as
// the operation monitor's first read; on F absent, X4B-b's bootstrap
// (`trust_bootstrap::bootstrapping_first_read`) runs inside that same read.
use super::super::super::current_record_bindings;
use super::super::super::native_record_capture::{NativeStore, locator_components};
use super::super::super::proposed_time_input;
use super::super::super::retained_metadata_index::{Budget, Collection};
use super::super::super::successor_record_bindings;
use super::{
    AdmittedCurrentTrust, Floors, PendingWrite, ReadMode, TrustRefusal, TrustRow, ViewInputs,
    admit_current, complete, field, int, refuse,
};
use crate::custody::installation_admission::observe_private_file;
use crate::custody::installation_fence::HeldFence;
use crate::private_access::{create_private_directory, create_private_regular_file, observe_private_directory};
use crate::trust::trust_outcomes::reference;
use crate::trust::trust_record_reader::{Record, RecordKind};
use crate::trust::trust_record_shapes::{self as shapes, Definition};
use crate::trust_time::{TimeAdmission, format_timestamp};
use opensip_identity::{JsonInteger, JsonValue as V, canonical_bytes, digest_hex, raw_sha256};
use opensip_platform::{
    DescriptorMetadata, RetainedDirectory, WorkCost, WorkFailure, WorkScope,
    write_new_regular_accounted,
};
use std::collections::BTreeMap;
use std::ffi::OsStr;

const CURRENT: &str = "state.v1";

fn object(v: &V) -> Result<&BTreeMap<String, V>, TrustRefusal> {
    match v {
        V::Object(o) => Ok(o),
        _ => refuse(TrustRow::Incomplete, "object"),
    }
}
fn integer(n: i64) -> V {
    V::Integer(JsonInteger::new(i128::from(n)).expect("i64 is a JSON integer"))
}
fn s(text: &str) -> V {
    V::String(text.into())
}
fn obj<const N: usize>(pairs: [(&str, V); N]) -> V {
    V::Object(pairs.into_iter().map(|(k, v)| (k.to_owned(), v)).collect())
}
fn hex(raw: &[u8]) -> String {
    digest_hex(&raw_sha256(raw))
}
/// A refusal of the ledger is the budget row; everything else is `row`.
fn lift<E: std::fmt::Debug>(row: TrustRow) -> impl FnOnce(WorkFailure<E>) -> TrustRefusal {
    move |failure| match failure {
        WorkFailure::Budget(b) => TrustRefusal {
            row: TrustRow::Budget,
            cause: format!("{b:?}"),
        },
        WorkFailure::Operation(e) => TrustRefusal {
            row,
            cause: format!("{e:?}"),
        },
    }
}
fn gate_row(failure: WorkFailure<crate::custody::installation_admission::GateRefusal>) -> TrustRefusal {
    use crate::custody::installation_admission::{CustodyRefusal, GateRefusal};
    match failure {
        WorkFailure::Budget(b) => TrustRefusal {
            row: TrustRow::Budget,
            cause: format!("{b:?}"),
        },
        WorkFailure::Operation(GateRefusal::Incomplete(r)) => TrustRefusal {
            row: TrustRow::RequiredFilesChanged,
            cause: format!("{r:?}"),
        },
        WorkFailure::Operation(GateRefusal::Custody(CustodyRefusal::Changed)) => TrustRefusal {
            row: TrustRow::RequiredFilesChanged,
            cause: "changed".into(),
        },
        WorkFailure::Operation(other) => TrustRefusal {
            row: TrustRow::HostIo,
            cause: format!("{other:?}"),
        },
    }
}

/// Item 7 (r8): what a confirmed publication leaves for the gate: the new
/// `state.v1`'s path under I, its reread bytes and its post-rename full
/// sample. Only `publish` mints it; it grants nothing by itself.
#[derive(Clone, Debug, PartialEq, Eq)]
pub(crate) struct ConfirmedCurrent {
    relative: String,
    raw: Vec<u8>,
    metadata: DescriptorMetadata,
    predecessor: DescriptorMetadata,
}
impl ConfirmedCurrent {
    pub(crate) fn relative(&self) -> &str {
        &self.relative
    }
    pub(crate) fn raw(&self) -> &[u8] {
        &self.raw
    }
    pub(crate) fn metadata(&self) -> &DescriptorMetadata {
        &self.metadata
    }
    /// The sample of the `state.v1` this publication replaced, which the
    /// publication reconfirmed before its first effect.
    pub(crate) fn predecessor(&self) -> &DescriptorMetadata {
        &self.predecessor
    }
}

/// Items 7 and 8 (r8): the retained trust current owner of one fence hold.
/// It is the session's one read of `state.v1` (its bytes, the capsule decoded
/// from them and its full sample), with `trust/stores/S` bound to it by a
/// metadata recheck. Only a confirmed publication advances it. Not Clone.
pub(crate) struct RetainedCurrentTrust {
    store_dir: RetainedDirectory,
    expected_store: V,
    relative: String,
    raw: Vec<u8>,
    capsule: V,
    sample: DescriptorMetadata,
    /// Check 3: the floors of each capsule this hold retained before the
    /// current one, where its clock was evaluated or retained (r9).
    prior: Vec<Floors>,
    /// Every confirmed publication of this hold, in order (X4B-b: the
    /// acceptance, then any floor write of the confirming admission).
    confirmed: Vec<ConfirmedCurrent>,
}
impl std::fmt::Debug for RetainedCurrentTrust {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("RetainedCurrentTrust")
            .field("relative", &self.relative)
            .field("bytes", &self.raw.len())
            .field("prior", &self.prior.len())
            .finish_non_exhaustive()
    }
}
fn decode(raw: &[u8], expected_store: &V) -> Result<V, TrustRefusal> {
    if raw.is_empty() || raw.len() > super::super::super::native_current::CURRENT_STATE_CAP {
        return refuse(TrustRow::Incomplete, "state.v1-cap");
    }
    let record = Record::parse(RecordKind::TrustCapsuleV1, raw, 131072)
        .or_else(|e| refuse(TrustRow::Incomplete, e))?;
    if field(record.value(), "store")? != expected_store {
        return refuse(TrustRow::Incomplete, "state.v1-store");
    }
    Ok(record.value().clone())
}
fn open_private(
    parent: &RetainedDirectory,
    name: &str,
    uid: u32,
    work: &mut WorkScope<'_>,
) -> Result<Option<RetainedDirectory>, TrustRefusal> {
    let Some(dir) = parent
        .open_child_directory_if_present_accounted(OsStr::new(name), work)
        .map_err(lift(TrustRow::HostIo))?
    else {
        return Ok(None);
    };
    observe_private_directory(dir.as_file(), uid, work).map_err(lift(TrustRow::Incomplete))?;
    Ok(Some(dir))
}
impl RetainedCurrentTrust {
    /// Bind the owner to the session's one read of `state.v1` under I: its
    /// exact bytes and its full sample, as X3a's write gate retained them
    /// (`DurableInstallation::current_trust`). `trust/stores/S` is opened
    /// through I and judged private, and `state.v1` under it must carry the
    /// sample: a metadata recheck, not a content read.
    pub(crate) fn bind(
        i: &RetainedDirectory,
        uid: u32,
        expected_store: &V,
        raw: &[u8],
        sample: &DescriptorMetadata,
        work: &mut WorkScope<'_>,
    ) -> Result<Self, TrustRefusal> {
        let sid = match field(expected_store, "storeInstanceId")? {
            V::String(sid) if sid.len() == 32 => sid.clone(),
            _ => return refuse(TrustRow::Incomplete, "store"),
        };
        let capsule = decode(raw, expected_store)?;
        let mut dir = None;
        for name in ["trust", "stores", sid.as_str()] {
            let parent = dir.as_ref().unwrap_or(i);
            let child = open_private(parent, name, uid, work)?
                .map_or_else(|| refuse(TrustRow::Incomplete, ("missing", name)), Ok)?;
            dir = Some(child);
        }
        let owner = Self {
            store_dir: dir.expect("three components"),
            expected_store: expected_store.clone(),
            relative: format!("trust/stores/{sid}/{CURRENT}"),
            raw: raw.to_vec(),
            capsule,
            sample: sample.clone(),
            prior: Vec::new(),
            confirmed: Vec::new(),
        };
        owner.recheck(uid, work)?;
        Ok(owner)
    }
    /// The full-sample recheck every fenced recheck runs: any change but a
    /// confirmed publication is `required-files-changed`.
    pub(crate) fn recheck(&self, uid: u32, work: &mut WorkScope<'_>) -> Result<(), TrustRefusal> {
        let now = observe_private_file(&self.store_dir, CURRENT, uid, work).map_err(gate_row)?;
        if now != self.sample {
            return refuse(TrustRow::RequiredFilesChanged, "state.v1-sample");
        }
        Ok(())
    }
    pub(crate) fn capsule(&self) -> &V {
        &self.capsule
    }
    pub(crate) fn raw(&self) -> &[u8] {
        &self.raw
    }
    pub(crate) fn sample(&self) -> &DescriptorMetadata {
        &self.sample
    }
    /// The last confirmed publication of this hold, if any.
    pub(crate) fn confirmed(&self) -> Option<&ConfirmedCurrent> {
        self.confirmed.last()
    }
    /// Every confirmed publication of this hold, in the order the owner
    /// advanced through them; the gate's own owner follows each in turn
    /// (X4T-b judgment call 9).
    pub(crate) fn confirmations(&self) -> &[ConfirmedCurrent] {
        &self.confirmed
    }
    /// Check 3's floors: every capsule this hold retained before this one.
    pub(crate) fn prior_floors(&self) -> &[Floors] {
        &self.prior
    }
}

/// One immutable trust file of a publication, located by its reference.
pub(crate) struct TrustWrite {
    collection: Collection,
    reference: V,
    initial_store: Option<V>,
    bytes: Vec<u8>,
}
impl TrustWrite {
    /// A file for the records or objects collection, named by its digest.
    pub(in crate::trust::root_payload) fn node(collection: Collection, bytes: Vec<u8>) -> Self {
        Self {
            collection,
            reference: reference(&bytes),
            initial_store: None,
            bytes,
        }
    }
    /// An event, by its full `EventRef`.
    pub(crate) fn event(reference: V, bytes: Vec<u8>) -> Self {
        Self {
            collection: Collection::Events,
            reference,
            initial_store: None,
            bytes,
        }
    }
    /// A publication descriptor, by its `PublicationRef`.
    pub(crate) fn publication(reference: V, bytes: Vec<u8>) -> Self {
        Self {
            collection: Collection::Publications,
            reference,
            initial_store: None,
            bytes,
        }
    }
    pub(in crate::trust::root_payload) fn collection(&self) -> Collection {
        self.collection
    }
    pub(crate) fn bytes(&self) -> &[u8] {
        &self.bytes
    }
    pub(crate) fn len(&self) -> usize {
        self.bytes.len()
    }
    /// The file's path under I, for a test that leaves it unreferenced.
    #[cfg(test)]
    pub(crate) fn path_for_tests(&self) -> Vec<String> {
        self.path().expect("a built file has a locator")
    }
    /// The file's path components under I (X4B-c: X4T-0 places the
    /// producer's files exactly where `publish` would).
    pub(in crate::trust::root_payload) fn path(&self) -> Result<Vec<String>, TrustRefusal> {
        locator_components(self.collection, &self.reference, self.initial_store.as_ref())
            .or_else(|e| refuse(TrustRow::Incomplete, e))
    }
}

// Item 11: the protocol's reserved work, summed from the platform's
// published cost functions. Each sum is an upper bound: a dependency's
// directories are charged as if each were opened, judged and created, and
// the file as if both the create and the existing-record path ran.
fn sum(costs: &[WorkCost]) -> WorkCost {
    costs
        .iter()
        .fold(WorkCost::default(), |a, c| a.checked_add(*c).unwrap_or(WorkCost {
            objects: usize::MAX,
            edges: usize::MAX,
            bytes: usize::MAX,
        }))
}
fn times(cost: WorkCost, n: usize) -> WorkCost {
    sum(&vec![cost; n])
}
/// `private_access`'s create of one private file or directory: the create
/// call, both ACL samples and the owner allow.
fn private_create(edges: usize) -> WorkCost {
    let capture = opensip_platform::descriptor_acl_capture_cost();
    sum(&[
        WorkCost {
            objects: 1,
            edges,
            bytes: 0,
        },
        capture,
        capture,
        opensip_platform::append_owner_zero_allow_cost(),
    ])
}
/// One exact-length reread of `len` bytes through `read_bounded_accounted`:
/// the platform's own `read_bounded_cost` (every requested growth to len+1),
/// with the read session's attempt bound (one per growth, the EOF read and
/// four spare). `len` is at least one byte and within the 4 MiB record cap.
fn exact_read(len: usize) -> Result<WorkCost, TrustRefusal> {
    opensip_platform::read_bounded_cost(len, crate::custody::installation_session::attempts(len))
        .or_else(|e| refuse(TrustRow::Incomplete, e))
}
/// Custody's `private_file` judgment of one name under a directory.
fn judged(name: &str) -> WorkCost {
    sum(&[
        RetainedDirectory::open_regular_cost(name),
        opensip_platform::descriptor_acl_capture_cost(),
    ])
}
fn directory_cost(name: &str) -> WorkCost {
    let barrier = opensip_platform::directory_barrier_cost();
    sum(&[
        opensip_platform::open_child_directory_cost(OsStr::new(name)),
        opensip_platform::descriptor_acl_capture_cost(),
        private_create(5),
        barrier,
        barrier,
    ])
}
fn file_cost(path: &[String], len: usize) -> Result<WorkCost, TrustRefusal> {
    let (leaf, parents) = path.split_last().expect("a locator has a leaf");
    let mut costs: Vec<WorkCost> = parents.iter().map(|n| directory_cost(n)).collect();
    costs.extend([
        opensip_platform::child_absence_observation_cost(OsStr::new(leaf)),
        private_create(2),
        opensip_platform::write_new_regular_cost(len),
        opensip_platform::directory_barrier_cost(),
        judged(leaf),
        RetainedDirectory::open_regular_cost(leaf),
        exact_read(len)?,
    ]);
    Ok(sum(&costs))
}
/// The pointer: X3b's protocol (temporary create, write with F_FULLFSYNC,
/// rename, directory barrier, reopen and confirm).
fn pointer_cost(len: usize) -> WorkCost {
    let temporary = format!("{CURRENT}.{}", "0".repeat(32));
    sum(&[
        private_create(2),
        opensip_platform::write_new_regular_cost(len),
        opensip_platform::rename_replace_cost(&temporary, CURRENT),
        opensip_platform::directory_barrier_cost(),
        WorkCost {
            objects: 2,
            edges: 4,
            bytes: len.saturating_add(1),
        },
    ])
}
/// The post-publication confirmation, reserved before the first effect: the
/// judged samples of `state.v1` before and after its exact reread (the second
/// is the owner's closing recheck), the reopen and the reread itself.
fn confirmation_cost(len: usize) -> Result<WorkCost, TrustRefusal> {
    Ok(sum(&[
        times(judged(CURRENT), 2),
        RetainedDirectory::open_regular_cost(CURRENT),
        exact_read(len)?,
    ]))
}
fn plus(costs: impl IntoIterator<Item = WorkCost>) -> Result<WorkCost, TrustRefusal> {
    costs
        .into_iter()
        .try_fold(WorkCost::default(), |sum, c| sum.checked_add(c))
        .map_or_else(|| refuse(TrustRow::Budget, "arithmetic"), Ok)
}

/// Directories a publication may create: the publications collection's
/// `by-predecessor` bucket and its predecessor directory, and (X4B-a) the
/// objects collection directory. Every other parent must exist (an
/// incomplete installation otherwise).
fn may_create(components: &[String], index: usize) -> bool {
    (index >= 2 && components[1] == "publications" && components[2] == "by-predecessor")
        // X4B-a: P0's closed tree (law 467) has no objects collection, so
        // the first acceptance creates `trust/objects` itself.
        || (index == 1 && components[1] == "objects")
}
fn parent_dir<'c>(
    cache: &'c mut BTreeMap<Vec<String>, RetainedDirectory>,
    i: &RetainedDirectory,
    parents: &[String],
    uid: u32,
    work: &mut WorkScope<'_>,
) -> Result<&'c RetainedDirectory, TrustRefusal> {
    for depth in 1..=parents.len() {
        let key = parents[..depth].to_vec();
        if cache.contains_key(&key) {
            continue;
        }
        let parent = if depth == 1 {
            i
        } else {
            &cache[&parents[..depth - 1]]
        };
        let name = &parents[depth - 1];
        let dir = match open_private(parent, name, uid, work)? {
            Some(dir) => dir,
            None if may_create(parents, depth - 1) => {
                let (created, _) = create_private_directory(parent, name, uid, work)
                    .map_err(lift(TrustRow::HostIo))?;
                let created = RetainedDirectory::from_retained_handle(created)
                    .or_else(|e| refuse(TrustRow::HostIo, e))?;
                created
                    .confirm_directory_barrier_accounted(work)
                    .map_err(lift(TrustRow::HostIo))?;
                parent
                    .confirm_directory_barrier_accounted(work)
                    .map_err(lift(TrustRow::HostIo))?;
                created
            }
            None => return refuse(TrustRow::Incomplete, ("missing", name.clone())),
        };
        cache.insert(key, dir);
    }
    Ok(&cache[parents])
}
/// One dependency: a fresh private file written with its file barrier and
/// then its directory barrier; or, at a content-addressed name already
/// present, the existing private file admitted only when its bytes are
/// exactly these (X4B item 6: equal bytes are equal names).
fn write_dependency(
    parent: &RetainedDirectory,
    leaf: &str,
    bytes: &[u8],
    uid: u32,
    work: &mut WorkScope<'_>,
) -> Result<(), TrustRefusal> {
    let absent = parent
        .observe_child_absent_accounted(OsStr::new(leaf), work)
        .map_err(lift(TrustRow::HostIo))?;
    if !absent {
        observe_private_file(parent, leaf, uid, work).map_err(gate_row_incomplete)?;
        let file = work
            .run(RetainedDirectory::open_regular_cost(leaf), |_| {
                parent.open_regular(leaf).map_err(WorkFailure::Operation)
            })
            .map_err(lift(TrustRow::HostIo))?;
        let existing = opensip_platform::read_bounded_accounted(&file, bytes.len(), work)
            .map_err(lift(TrustRow::Incomplete))?;
        if existing != bytes {
            return refuse(TrustRow::Incomplete, ("foreign", leaf.to_owned()));
        }
        return Ok(());
    }
    let (file, _) =
        create_private_regular_file(parent, leaf, uid, work).map_err(lift(TrustRow::HostIo))?;
    write_new_regular_accounted(&file, bytes, work).map_err(lift(TrustRow::HostIo))?;
    parent
        .confirm_directory_barrier_accounted(work)
        .map_err(lift(TrustRow::HostIo))?;
    Ok(())
}
/// An existing record that is not private, or not a regular file, is a
/// misbound trust record: an incomplete installation.
fn gate_row_incomplete(
    failure: WorkFailure<crate::custody::installation_admission::GateRefusal>,
) -> TrustRefusal {
    match failure {
        WorkFailure::Budget(b) => TrustRefusal {
            row: TrustRow::Budget,
            cause: format!("{b:?}"),
        },
        WorkFailure::Operation(e) => TrustRefusal {
            row: TrustRow::Incomplete,
            cause: format!("{e:?}"),
        },
    }
}

/// Item 7's publication protocol (r8: one owner, shared with X4B-a). Under
/// the held fence: the owner is rechecked; the whole protocol and its
/// post-publication confirmation are reserved before the first effect; each
/// dependency is written in order; `state.v1` is replaced last through X3b's
/// private file protocol; then `state.v1` is sampled, reread through an
/// exact-length cap and sampled again, the capsule is decoded from that
/// reread, and the owner advances to it. A failure before the rename leaves
/// the pointer unchanged (written records are unreferenced and harmless); a
/// failure from the rename on is durability-undetermined. Both are the host
/// I/O row; nothing is retried or deleted.
pub(crate) fn publish(
    fence: &dyn HeldFence,
    owner: &mut RetainedCurrentTrust,
    files: &[TrustWrite],
    capsule_raw: &[u8],
    work: &mut WorkScope<'_>,
) -> Result<(), TrustRefusal> {
    // X9: the protocol is `x4t.floor-publication` (law X9 r1 item 5).
    opensip_platform::crash_scope!("x4t.floor-publication", {
        publish_protocol(fence, owner, files, capsule_raw, work)
    })
}
/// Law X9 r1 item 6 and law X8 r3 items 4b and 5a (unit X9-1): the shared
/// fenced `state.v1` publisher, beside the trust owner's protocol and on the
/// shared fixture-gate site list. It has no production caller: without
/// `crash-matrix` or `scenario-fixtures` it is compiled only under
/// `cfg(test)`, and both support surfaces reach it only through the shared
/// installation fixture, which takes the fence by the write gate's walk.
///
/// Under that held fence it binds the retained `state.v1` owner to the
/// gate's one read, then runs `publish` itself over a generated store:
/// every immutable record first (content-addressed, so an existing name
/// must hold exactly these bytes), `state.v1` replaced last by X3b's private
/// file protocol, then the confirming reread. `files` are paths under I with
/// their bytes. The one named `trust/stores/<S>/state.v1` is the new capsule;
/// every other must be a records, objects, events or publications file whose
/// locator gives back exactly its path. It writes nothing else.
#[cfg(any(test, feature = "crash-matrix", feature = "scenario-fixtures"))]
pub(crate) fn publish_store_fenced(
    fence: &dyn HeldFence,
    current: &crate::custody::installation_admission::CurrentTrustRead<'_>,
    files: &[(String, Vec<u8>)],
    work: &mut WorkScope<'_>,
) -> Result<ConfirmedCurrent, TrustRefusal> {
    let Some(file) = current.file else {
        return refuse(TrustRow::Incomplete, "state.v1-unread");
    };
    let before =
        opensip_identity::parse_json(current.raw).or_else(|e| refuse(TrustRow::Incomplete, e))?;
    let expected_store = field(&before, "store")?.clone();
    let mut owner = RetainedCurrentTrust::bind(
        current.installation,
        current.uid,
        &expected_store,
        current.raw,
        file.metadata(),
        work,
    )?;
    let with = |bytes: &[u8], key: &str, value: V| -> Result<V, TrustRefusal> {
        let mut r = object(&reference(bytes))?.clone();
        r.insert(key.to_owned(), value);
        Ok(V::Object(r))
    };
    let mut writes = Vec::new();
    let mut capsule_raw = None;
    for (path, bytes) in files {
        let parts: Vec<&str> = path.split('/').collect();
        let write = match parts.as_slice() {
            ["trust", "stores", _, name] if *name == CURRENT => {
                capsule_raw = Some(bytes.as_slice());
                continue;
            }
            ["trust", "records", _] => TrustWrite::node(Collection::Records, bytes.clone()),
            ["trust", "objects", _] => TrustWrite::node(Collection::Objects, bytes.clone()),
            ["trust", "stores", sid, "events", leaf] => {
                let sequence = leaf
                    .split_once('-')
                    .and_then(|(n, _)| n.parse::<i64>().ok())
                    .map_or_else(|| refuse(TrustRow::Incomplete, ("event", path)), Ok)?;
                let reference = with(bytes, "storeInstanceId", s(sid))?;
                let mut r = object(&reference)?.clone();
                r.insert("sequence".into(), integer(sequence));
                TrustWrite::event(V::Object(r), bytes.clone())
            }
            ["trust", "publications", "by-predecessor", previous, _] => {
                TrustWrite::publication(with(bytes, "previousCapsule", s(previous))?, bytes.clone())
            }
            ["trust", "publications", "initial", sid, _] => TrustWrite {
                collection: Collection::Publications,
                reference: with(bytes, "previousCapsule", V::Null)?,
                initial_store: Some(s(sid)),
                bytes: bytes.clone(),
            },
            _ => return refuse(TrustRow::Incomplete, ("unaddressed", path)),
        };
        if write.path()? != parts {
            return refuse(TrustRow::Incomplete, ("locator", path));
        }
        writes.push(write);
    }
    let Some(capsule_raw) = capsule_raw else {
        return refuse(TrustRow::Incomplete, "no-capsule");
    };
    publish(fence, &mut owner, &writes, capsule_raw, work)?;
    owner
        .confirmed()
        .cloned()
        .map_or_else(|| refuse(TrustRow::HostIo, "unconfirmed"), Ok)
}
fn publish_protocol(
    fence: &dyn HeldFence,
    owner: &mut RetainedCurrentTrust,
    files: &[TrustWrite],
    capsule_raw: &[u8],
    work: &mut WorkScope<'_>,
) -> Result<(), TrustRefusal> {
    let uid = fence.supplied_actor().0;
    let i = fence.directory();
    fence.recheck().or_else(|e| refuse(TrustRow::HostIo, e))?;
    owner.recheck(uid, work)?;
    let new_capsule = decode(capsule_raw, &owner.expected_store)?;
    let paths = files.iter().map(TrustWrite::path).collect::<Result<Vec<_>, _>>()?;
    let mut costs = files
        .iter()
        .zip(&paths)
        .map(|(f, path)| file_cost(path, f.bytes.len()))
        .collect::<Result<Vec<_>, _>>()?;
    costs.push(pointer_cost(capsule_raw.len()));
    let writes = plus(costs)?;
    let confirm = confirmation_cost(capsule_raw.len())?;
    let reserve = plus([writes, confirm])?;
    let mut failure = None;
    let mut fail = |e: TrustRefusal| {
        failure.get_or_insert(e);
        WorkFailure::Operation(())
    };
    let store_dir = &owner.store_dir;
    let confirmed = work.effect(WorkCost::default(), reserve, |post| {
        post.prepaid(writes, |w| {
            let mut cache = BTreeMap::new();
            for (file, path) in files.iter().zip(&paths) {
                let (leaf, parents) = path.split_last().expect("a locator has a leaf");
                opensip_platform::crash_scope!("dependency", {
                    let parent = parent_dir(&mut cache, i, parents, uid, w).map_err(&mut fail)?;
                    write_dependency(parent, leaf, &file.bytes, uid, w).map_err(&mut fail)
                })?;
            }
            opensip_platform::crash_scope!("pointer", {
                crate::journal_store::publish_private_file(store_dir, CURRENT, capsule_raw, uid, w)
            })
            .map_err(lift(TrustRow::HostIo))
            .map_err(&mut fail)
        })?;
        post.prepaid(confirm, |w| {
            let before = observe_private_file(store_dir, CURRENT, uid, w)
                .map_err(gate_row)
                .map_err(&mut fail)?;
            let file = w
                .run(RetainedDirectory::open_regular_cost(CURRENT), |_| {
                    store_dir.open_regular(CURRENT).map_err(WorkFailure::Operation)
                })
                .map_err(lift(TrustRow::HostIo))
                .map_err(&mut fail)?;
            let reread = opensip_platform::read_bounded_accounted(&file, capsule_raw.len(), w)
                .map_err(lift(TrustRow::HostIo))
                .map_err(&mut fail)?;
            let after = observe_private_file(store_dir, CURRENT, uid, w)
                .map_err(gate_row)
                .map_err(&mut fail)?;
            if before != after || reread != capsule_raw {
                return Err(fail(TrustRefusal {
                    row: TrustRow::HostIo,
                    cause: "write-ahead-confirmation".into(),
                }));
            }
            Ok((reread, after))
        })
    });
    let (reread, metadata) = match confirmed {
        Ok(confirmed) => confirmed,
        Err(WorkFailure::Budget(b)) => {
            return Err(failure.unwrap_or(TrustRefusal {
                row: TrustRow::Budget,
                cause: format!("{b:?}"),
            }));
        }
        Err(WorkFailure::Operation(())) => {
            return Err(failure.unwrap_or(TrustRefusal {
                row: TrustRow::HostIo,
                cause: "publication".into(),
            }));
        }
    };
    let capsule = decode(&reread, &owner.expected_store)?;
    debug_assert_eq!(capsule, new_capsule);
    let previous = Floors::of_clock(field(&owner.capsule, "clock")?)?;
    if previous != Floors::default() {
        owner.prior.push(previous);
    }
    owner.confirmed.push(ConfirmedCurrent {
        relative: owner.relative.clone(),
        raw: reread.clone(),
        metadata: metadata.clone(),
        predecessor: owner.sample.clone(),
    });
    owner.raw = reread;
    owner.capsule = capsule;
    owner.sample = metadata;
    // The owner's closing recheck is the confirmation's second sample, taken
    // inside the reservation, so no charge follows the first effect.
    fence.recheck().or_else(|e| refuse(TrustRow::HostIo, e))
}
/// Item 7: the floor publication of one fenced admission, built in memory
/// and checked by the existing verifiers before any effect.
pub(crate) struct FloorPublication {
    files: Vec<TrustWrite>,
    capsule_raw: Vec<u8>,
}
impl FloorPublication {
    pub(crate) fn capsule_raw(&self) -> &[u8] {
        &self.capsule_raw
    }
}
fn encode(definition: Definition, value: &V) -> Result<Vec<u8>, TrustRefusal> {
    let raw = canonical_bytes(value).or_else(|_| refuse(TrustRow::Incomplete, "canonical"))?;
    shapes::admit(definition, &raw).or_else(|e| refuse(TrustRow::Incomplete, (definition, e)))?;
    Ok(raw)
}
fn stamp(seconds: i64) -> Result<V, TrustRefusal> {
    format_timestamp(seconds)
        .map(V::String)
        .or_else(|e| refuse(TrustRow::Incomplete, e))
}
/// Whether S4 proposes a write that changes the stored record: F rises, L
/// advances, or the anchor is rewritten to a different value (item 7). A
/// confirming admission on the same clock sample finds none (X4B item 1).
pub(crate) fn needs_write(capsule: &V, time: &TimeAdmission, observation: &V) -> Result<bool, TrustRefusal> {
    if time.report_only || time.refusal.is_some() {
        return Ok(false);
    }
    let Some(evaluation) = time.floor_write else {
        return Ok(false);
    };
    let record = field(field(capsule, "clock")?, "record")?;
    let floor = Floors::of_clock(field(capsule, "clock")?)?.eval_high_water;
    Ok(floor.is_none_or(|f| evaluation > f)
        || time.last_write.is_some()
        || (time.anchor_write && field(record, "anchor")? != observation))
}
/// Build item 7's floor publication over the owner's capsule: the before
/// image record, the S4EvaluationInputV2 from the existing assembler, the
/// `host-trust-admission` operation and its `continue` input for the running
/// core, the clock-write event, the descriptor and the successor capsule with
/// F := tEval, L and the anchor written as S4 proposed and every other field
/// unchanged. Verified by `successor_record_bindings::bind` (against the
/// actual before) and `current_record_bindings::bind` (which runs
/// `bind_trace`) over exactly these bytes before it is returned.
pub(crate) fn build_floor_publication(
    owner: &RetainedCurrentTrust,
    pending: &PendingWrite,
    time: &TimeAdmission,
    invocation: &V,
    core_closure: &str,
    work: &mut WorkScope<'_>,
) -> Result<FloorPublication, TrustRefusal> {
    let before = &owner.capsule;
    let b4 = object(before)?;
    let before_ref = reference(&owner.raw);
    let previous = hex(&owner.raw);
    let (evaluation, evaluation_ref) =
        proposed_time_input::assemble(&pending.0, before, &before_ref, invocation)
            .or_else(|e| refuse(TrustRow::Incomplete, e))?;
    let input = encode(
        Definition::TrustAdmissionInputV1,
        &obj([
            ("closure", s(core_closure)),
            ("inputSchema", integer(1)),
            ("kind", s("trust-admission-input")),
            ("purpose", s("continue")),
            ("surface", s("installed-component")),
        ]),
    )?;
    let operation = encode(
        Definition::OperationInputV1,
        &obj([
            ("action", s("host-trust-admission")),
            (
                "input",
                obj([("kind", s("trust-admission-input")), ("ref", reference(&input))]),
            ),
            ("invocation", invocation.clone()),
            ("operationSchema", integer(1)),
            ("store", b4["store"].clone()),
        ]),
    )?;
    let operation_ref = reference(&operation);
    let sid = field(&b4["store"], "storeInstanceId")?.clone();
    let head = b4["eventHead"].clone();
    let sequence = int(field(&head, "sequence")?)?
        .checked_add(1)
        .map_or_else(|| refuse(TrustRow::Incomplete, "sequence"), Ok)?;
    let evaluation_at = time
        .floor_write
        .map_or_else(|| refuse(TrustRow::Incomplete, "floor_write"), Ok)?;
    let mut writes = Vec::new();
    if time.anchor_write {
        writes.push(s("anchor"));
    }
    writes.push(s("evalHighWater"));
    if time.last_write.is_some() {
        writes.push(s("lastAccepted"));
    }
    let time_evidence = if time.last_write.is_some() {
        obj([("kind", s("new")), ("proof", evaluation_ref.clone())])
    } else {
        obj([("kind", s("kept"))])
    };
    let event = encode(
        Definition::TrustEventV1,
        &obj([
            ("eventSchema", integer(1)),
            ("store", sid.clone()),
            ("sequence", integer(sequence)),
            ("previous", head),
            ("operation", operation_ref.clone()),
            ("kind", s("clock-write")),
            ("source", s("s4")),
            ("evaluation", evaluation_ref.clone()),
            ("writes", V::Array(writes)),
            ("phaseBefore", s("retained")),
            ("phaseAfter", s("retained")),
            ("timeEvidence", time_evidence),
        ]),
    )?;
    let mut event_ref = object(&reference(&event))?.clone();
    event_ref.insert("storeInstanceId".into(), sid);
    event_ref.insert("sequence".into(), integer(sequence));
    let event_ref = V::Object(event_ref);

    // The successor projection: only F, L, the anchor and the time evidence
    // change in the clock, then the revision, predecessor and event head.
    let mut projection = b4.clone();
    projection.remove("publication");
    let mut clock = object(&projection["clock"])?.clone();
    let mut record = object(&clock["record"])?.clone();
    record.insert("evalHighWater".into(), stamp(evaluation_at)?);
    if let Some(last) = time.last_write {
        record.insert("lastAccepted".into(), stamp(last)?);
        clock.insert("timeEvidence".into(), evaluation_ref.clone());
    }
    if time.anchor_write {
        record.insert(
            "anchor".into(),
            pending.0.observation().document().clone(),
        );
    }
    clock.insert("record".into(), V::Object(record));
    projection.insert("clock".into(), V::Object(clock));
    let revision = int(&b4["revision"])?
        .checked_add(1)
        .map_or_else(|| refuse(TrustRow::Incomplete, "revision"), Ok)?;
    projection.insert("revision".into(), integer(revision));
    projection.insert("previous".into(), s(&previous));
    projection.insert("eventHead".into(), event_ref.clone());
    let projection = V::Object(projection);
    let descriptor = encode(
        Definition::PublicationDescriptorV1,
        &obj([
            ("afterProjection", projection.clone()),
            (
                "events",
                V::Array(vec![obj([("event", event_ref.clone()), ("roleChange", V::Null)])]),
            ),
            (
                "nativeBefore",
                obj([("revision", b4["revision"].clone()), ("sha256", s(&previous))]),
            ),
            ("operation", operation_ref),
            ("previousCapsule", s(&previous)),
            ("publicationSchema", integer(1)),
            ("revision", integer(revision)),
            ("store", b4["store"].clone()),
        ]),
    )?;
    let descriptor_ref = object(&reference(&descriptor))?.clone();
    let publication = obj([
        ("previousCapsule", s(&previous)),
        ("sha256", descriptor_ref["sha256"].clone()),
        ("bytes", descriptor_ref["bytes"].clone()),
    ]);
    let mut capsule = object(&projection)?.clone();
    capsule.insert("publication".into(), publication.clone());
    let capsule = V::Object(capsule);
    let capsule_raw = encode(Definition::TrustCapsuleV1, &capsule)?;
    let files = vec![
        TrustWrite::node(Collection::Records, owner.raw.clone()),
        TrustWrite::node(Collection::Records, evaluation.raw().to_vec()),
        TrustWrite::node(Collection::Records, input),
        TrustWrite::node(Collection::Records, operation),
        TrustWrite::event(event_ref, event),
        TrustWrite::publication(publication.clone(), descriptor.clone()),
    ];
    // The existing verifiers, over exactly these bytes.
    let held: BTreeMap<(Collection, [u8; 32]), Vec<u8>> = files
        .iter()
        .map(|f| ((f.collection, raw_sha256(&f.bytes)), f.bytes.clone()))
        .collect();
    let mut store = |c: Collection, h: [u8; 32], cap: usize| -> Result<Vec<u8>, ()> {
        let raw = held.get(&(c, h)).ok_or(())?;
        if raw.len() > cap {
            return Err(());
        }
        Ok(raw.clone())
    };
    let mut b = Budget::borrowed(work);
    successor_record_bindings::bind(&mut b, before, &publication, &mut store)
        .or_else(|e| refuse(TrustRow::Incomplete, ("successor", e)))?;
    let descriptor_value = opensip_identity::parse_json(&descriptor)
        .or_else(|_| refuse(TrustRow::Incomplete, "descriptor"))?;
    current_record_bindings::bind(
        &mut b,
        &owner.expected_store,
        &capsule,
        &descriptor_value,
        &mut store,
    )
    .or_else(|e| refuse(TrustRow::Incomplete, ("current", e)))?;
    Ok(FloorPublication { files, capsule_raw })
}

/// Items 7 to 9: the fenced first read. Under the installation fence with no
/// project lock held and before any lease, it admits the retained owner's
/// capsule (items 2 to 6, with checks 1 and 2 of the rollback rule), applies
/// check 3 against this hold's own floors, and, unless report-only, performs
/// item 7's write-ahead before the view is returned: the floor publication is
/// built, verified and published, and the owner advances to the confirmed
/// `state.v1`. A confirming admission on the same clock sample writes nothing.
/// (r12, unit X4-F2) A refusal by item 6's clock at tEval is published where
/// the view would be returned: after check 3, and after the write-ahead or
/// the closing rechecks. It is never returned as a view.
pub(crate) fn fenced_first_read(
    work: &mut WorkScope<'_>,
    fence: &dyn HeldFence,
    owner: &mut RetainedCurrentTrust,
    inputs: &ViewInputs<'_>,
    invocation: &V,
) -> Result<AdmittedCurrentTrust, TrustRefusal> {
    if !matches!(inputs.mode, ReadMode::Fenced { .. }) {
        return refuse(TrustRow::HostIo, "fenced-read-mode");
    }
    let uid = fence.supplied_actor().0;
    fence.recheck().or_else(|e| refuse(TrustRow::HostIo, e))?;
    owner.recheck(uid, work)?;
    let mut admission = {
        let mut b = Budget::borrowed(work);
        let mut store = NativeStore::new(fence);
        let result = admit_current(
            &mut b,
            &owner.expected_store,
            &owner.capsule,
            inputs,
            &mut store,
        );
        complete(&mut store, result)?
    };
    // Check 3 (r9): this hold's own retained floors.
    if owner.prior.iter().any(|prior| admission.floors().below(prior)) {
        return refuse(TrustRow::Rollback, "fence-hold-floors");
    }
    if let Some(pending) = admission.take_pending() {
        let time = admission
            .time()
            .cloned()
            .map_or_else(|| refuse(TrustRow::HostIo, "time"), Ok)?;
        if needs_write(&owner.capsule, &time, pending.0.observation().document())? {
            let publication = build_floor_publication(
                owner,
                &pending,
                &time,
                invocation,
                inputs.core_closure,
                work,
            )?;
            // `publish` ends on its reserved confirmation, which is the
            // owner's recheck; nothing is charged after its first effect.
            publish(fence, owner, &publication.files, &publication.capsule_raw, work)?;
            // Item 7 (r12): a clocked refusal only after its write-ahead.
            return admission.into_view();
        }
    }
    fence.recheck().or_else(|e| refuse(TrustRow::HostIo, e))?;
    owner.recheck(uid, work)?;
    admission.into_view()
}

#[cfg(test)]
mod tests {
    include!("floor_publication_tests.rs");
}
