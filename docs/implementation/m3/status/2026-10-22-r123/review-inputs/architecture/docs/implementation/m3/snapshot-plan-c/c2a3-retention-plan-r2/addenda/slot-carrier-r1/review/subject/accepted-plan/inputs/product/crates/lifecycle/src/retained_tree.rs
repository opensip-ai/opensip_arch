//! Law CI r5 items 6 and 7, with amendments CI-A2 and CI-A3 (units CI-3 and
//! CI-3L; component installation plan r3): the retained-tree capability
//! C2a-3 binds, its bounded verified-byte transfer, and its launch member,
//! the only operation that yields a path to spawn.
//!
//! `open_retained_tree` re-verifies everything, every time: the store's and
//! the generation's custody, the association of the generation with the
//! authenticated evidence and C2a-1's candidate, the pin, and the whole
//! tree's structure, installed modes, link targets and bytes. It trusts
//! nothing by existence, and repairs nothing. The capability it returns is
//! pinned (a shared `flock` on `pin.lock`) and holds the retained handles
//! and the shared read buffer, so a transfer re-reads a file from the
//! retained `tree/` handle, component by component, and hands the sink its
//! bytes only as verified at the end.
use crate::installation::{
    self as inst, ComponentStore, Evidence, Phase, READ, READ_CHUNK, TREE, Tree, TreeFault,
    charged_find, charged_sort, component_cmp, custody_cost, descend, descend_cost, envelope,
    index_buffer_cost, read_verified, search_comparisons, sort_comparisons, split,
};
use opensip_platform::component_tree::{
    self as ct, Access, EntryKind, PathStatus, PathStatusError, PinLock, PinMode, TreeOpenError,
};
use opensip_platform::{RetainedDirectory, WorkBudgetError, WorkCost, WorkFailure, WorkScope};
use opensip_security::archive_profile::RowKind;
use opensip_security::snapshot_source::{CustodyDirectoryRefusal, owned_record};
use opensip_security::{AuthenticatedComponent, ClosureCandidate, SelectedPlatform};
use std::ffi::CStr;
use std::io;
use std::marker::PhantomData;
use std::path::{Path, PathBuf};

/// D4-4's dependent-crate CI-T28 read-failure control. This exists only in
/// explicit fixture/debug builds, never in the ordinary or release surface.
#[cfg(all(debug_assertions, any(test, feature = "scenario-fixtures")))]
pub mod read_fixture {
    use std::{cell::Cell, marker::PhantomData, rc::Rc};
    thread_local! { static FAIL: Cell<bool> = const { Cell::new(false) }; }
    #[must_use = "retain the read fixture guard through the operation"]
    pub struct Guard {
        _same_thread: PhantomData<Rc<()>>,
    }
    pub fn fail_next_read() -> Guard {
        FAIL.with(|flag| {
            assert!(!flag.replace(true), "a read fixture is already armed");
        });
        Guard {
            _same_thread: PhantomData,
        }
    }
    impl Guard {
        pub fn was_triggered(&self) -> bool {
            FAIL.with(|flag| !flag.get())
        }
    }
    pub(crate) fn check() -> std::io::Result<()> {
        if FAIL.with(|flag| flag.replace(false)) {
            Err(std::io::Error::other("D4 fixture injected read failure"))
        } else {
            Ok(())
        }
    }
    impl Drop for Guard {
        fn drop(&mut self) {
            FAIL.with(|flag| flag.set(false));
        }
    }
}

/// Which fence the caller holds while it pins (LAW item 7): the durable
/// path's lifecycle fence, ER10a's read-session fence, or none for an
/// ephemeral read. The pin itself is the same shared `flock` in each.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum PinRequest {
    UnderFence,
    UnderReadSession,
    Ephemeral,
}

/// LAW item 6's typed failures. `NotInstalled` is the only absence of the
/// generation; every other failure but `Budget` and `Io` is a promised
/// tree's own corruption and keeps its cause (LAW item 8).
#[derive(Debug)]
pub enum TreeReadFailure {
    NotInstalled,
    Absent {
        row: u32,
    },
    Length {
        row: u32,
    },
    Digest {
        row: u32,
    },
    /// A row of the wrong type, or (`None`) a generation name that is not a
    /// directory.
    Type {
        row: Option<u32>,
    },
    Mode {
        row: Option<u32>,
    },
    LinkTarget {
        row: u32,
    },
    Extra {
        directory: Option<u32>,
    },
    Association,
    Pin,
    Custody(CustodyDirectoryRefusal),
    /// The composed launch path does not name the verified member (CI-A3-e):
    /// it is absent, a non-directory stands along it, its final component
    /// is a link or of another kind, or its `(device, inode)` differs.
    Binding,
    Budget(WorkBudgetError),
    Io {
        call: &'static str,
        error: io::Error,
    },
}
impl TreeReadFailure {
    fn of(e: WorkFailure<TreeFault>) -> Self {
        match e {
            WorkFailure::Budget(b) => Self::Budget(b),
            WorkFailure::Operation(fault) => match fault {
                TreeFault::Absent { row } => Self::Absent { row },
                TreeFault::Extra { directory } => Self::Extra { directory },
                TreeFault::Type { row } => Self::Type { row: Some(row) },
                TreeFault::Mode { row } => Self::Mode { row },
                TreeFault::LinkTarget { row } => Self::LinkTarget { row },
                TreeFault::Length { row } => Self::Length { row },
                TreeFault::Digest { row } => Self::Digest { row },
                TreeFault::Association => Self::Association,
                TreeFault::Pin => Self::Pin,
                TreeFault::Io { call, error } => Self::Io { call, error },
            },
        }
    }
}

/// The sink of one verified transfer. It receives the expected digest and
/// length first, then the bytes, and is told only at the end whether the
/// stream verified; it must commit nothing unless `finish(true)` arrives.
/// Its own work is charged to its owner's ledger.
pub trait VerifiedSink {
    fn begin(&mut self, sha256: [u8; 32], length: u64);
    fn chunk(&mut self, bytes: &[u8]);
    fn finish(&mut self, verified: bool);
}

/// The opaque, pinned capability: the store's borrowed directory, the
/// generation's, `tree/`'s and `pin.lock`'s retained handles, the shared
/// read buffer, the borrowed TreeCommitment and its component-ordered index
/// (CI-A2-b). Only `open_retained_tree` constructs one; it never stands for
/// bytes present later on its own.
pub struct RetainedTree<'s, 'a> {
    #[allow(dead_code)]
    store: &'s ComponentStore,
    #[allow(dead_code)]
    generation: RetainedDirectory,
    tree_dir: RetainedDirectory,
    pin: PinLock,
    buffer: Vec<u8>,
    tree: Tree<'a>,
    order: Vec<u32>,
    /// The fence the caller declared it held while pinning (LAW item 7).
    request: PinRequest,
    /// The generation's name, `<closure2-hex>`, for the launch path.
    name: &'a str,
    /// The first failure of a transfer or a launch, after which every
    /// transfer and launch refuses with that cause (failure latching).
    latched: Option<Latched>,
}

/// A latched failure of `transfer` or `launch_member`, kept so every later
/// operation of the capability refuses with the same cause (CI-A3-a): the
/// call name and errno of an I/O failure, and a budget failure as the
/// ledger's own latch (`Closed`), on any scope.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum Latched {
    Association,
    Absent(u32),
    Type(Option<u32>),
    Mode(Option<u32>),
    Length(u32),
    Digest(u32),
    Binding,
    Budget,
    Io {
        call: &'static str,
        errno: Option<i32>,
    },
}
impl Latched {
    fn of(failure: &TreeReadFailure) -> Self {
        match failure {
            TreeReadFailure::Absent { row } => Self::Absent(*row),
            TreeReadFailure::Type { row } => Self::Type(*row),
            TreeReadFailure::Mode { row } => Self::Mode(*row),
            TreeReadFailure::Length { row } => Self::Length(*row),
            TreeReadFailure::Digest { row } => Self::Digest(*row),
            TreeReadFailure::Binding => Self::Binding,
            TreeReadFailure::Budget(_) => Self::Budget,
            TreeReadFailure::Io { call, error } => Self::Io {
                call,
                errno: error.raw_os_error(),
            },
            _ => Self::Association,
        }
    }
    fn failure(self) -> TreeReadFailure {
        match self {
            Self::Association => TreeReadFailure::Association,
            Self::Absent(row) => TreeReadFailure::Absent { row },
            Self::Type(row) => TreeReadFailure::Type { row },
            Self::Mode(row) => TreeReadFailure::Mode { row },
            Self::Length(row) => TreeReadFailure::Length { row },
            Self::Digest(row) => TreeReadFailure::Digest { row },
            Self::Binding => TreeReadFailure::Binding,
            Self::Budget => TreeReadFailure::Budget(WorkBudgetError::Closed),
            Self::Io { call, errno } => TreeReadFailure::Io {
                call,
                error: errno.map_or_else(
                    || io::Error::other("latched transfer failure"),
                    io::Error::from_raw_os_error,
                ),
            },
        }
    }
}

/// `CAP`: the capability record's size, a compile-time property of the
/// code.
pub(crate) fn capability_cost() -> WorkCost {
    WorkCost {
        objects: 1,
        edges: 0,
        bytes: size_of::<RetainedTree<'static, 'static>>(),
    }
}

/// `B_open` (LAW item 6, with CI-A2-b and CI-A2-d), with checked arithmetic.
pub(crate) fn open_bound(tree: &Tree<'_>, record: usize) -> Option<WorkCost> {
    let st = ct::status_read_cost();
    let fopen = ct::open_regular_no_follow_cost();
    let (n, d) = (tree.n, tree.dirs);
    let listing = n.checked_add(3usize.checked_mul(d.checked_add(1)?)?)?;
    let mut b = inst::Bound::default()
        .add(custody_cost())?
        .add(owned_record(inst::NAME_BYTES + 1))?
        .add(descend_cost(inst::NAME_BYTES))?
        .add(custody_cost())?
        .add(fopen)?
        .add(ct::NATIVE_CALL)?
        .add(owned_record(record))?
        .add(fopen)?
        .add_times(READ, usize::try_from(envelope(record as u64)).ok()?)?
        .add(inst::buffer_cost())?
        .add(descend_cost(TREE.len()))?
        .add(st)?
        // CI-A2-b: the component-ordered index, and the Blobs' association.
        .add_times(index_buffer_cost(n)?, 2)?
        .add_times(inst::COMPARISON, sort_comparisons(n)?)?
        .add_times(
            inst::COMPARISON,
            tree.files.checked_mul(search_comparisons(n))?,
        )?
        .add_times(READ, listing)?
        .add_times(st, n)?
        .add(capability_cost())?;
    for row in tree.rows() {
        let (_, name) = split(row.path);
        match row.kind {
            RowKind::File { length, .. } => {
                b = b
                    .add(fopen)?
                    .add_times(READ, usize::try_from(envelope(length)).ok()?)?;
            }
            RowKind::Dir => b = b.add(descend_cost(name.len()))?,
            RowKind::Symlink { .. } => {
                b = b.add(ct::NATIVE_CALL)?.add(owned_record(ct::LINK_BUFFER))?
            }
        }
    }
    Some(b.0)
}

/// `B_transfer(f)` (LAW item 6, with CI-A2-c): the path's lookup, the
/// parent chain's descents, the file's open and its read attempts.
pub fn transfer_bound(tree_rows: usize, path: &str, length: u64) -> Option<WorkCost> {
    let mut b = inst::Bound::default()
        .add_times(inst::COMPARISON, search_comparisons(tree_rows))?
        .add(ct::open_regular_no_follow_cost())?
        .add_times(READ, usize::try_from(envelope(length)).ok()?)?;
    let (parent, _) = split(path);
    if !parent.is_empty() {
        for segment in parent.split('/') {
            b = b.add(descend_cost(segment.len()))?;
        }
    }
    Some(b.0)
}

/// Open the pinned capability for C2a-1's candidate of `component` on
/// `platform` (LAW item 6). Every operation is charged before it is made,
/// at `B_open`'s prices; the work profile is the caller's.
pub fn open_retained_tree<'s, 'a>(
    store: &'s ComponentStore,
    component: &AuthenticatedComponent<'a>,
    candidate: &'a ClosureCandidate<'_>,
    platform: SelectedPlatform<'_>,
    pin: PinRequest,
    work: &mut WorkScope<'_>,
) -> Result<RetainedTree<'s, 'a>, TreeReadFailure> {
    let evidence =
        inst::evidence(component, candidate, platform).map_err(|_| TreeReadFailure::Association)?;
    open_with(store, &evidence, candidate, pin, work)
}

fn budget(e: WorkFailure<TreeFault>) -> TreeReadFailure {
    TreeReadFailure::of(e)
}

pub(crate) fn open_with<'s, 'a>(
    store: &'s ComponentStore,
    evidence: &Evidence<'a>,
    candidate: &ClosureCandidate<'_>,
    pin: PinRequest,
    work: &mut WorkScope<'_>,
) -> Result<RetainedTree<'s, 'a>, TreeReadFailure> {
    let request = pin;
    let tree = evidence.tree;
    // The store's custody.
    match store.custody::<TreeFault>(store.directory.as_file(), work) {
        Ok(Ok(())) => {}
        Ok(Err(refusal)) => return Err(TreeReadFailure::Custody(refusal)),
        Err(e) => return Err(budget(e)),
    }
    // Association: the candidate's Blobs are exactly the file rows
    // projected, found through the component-ordered index (CI-A2-b).
    let order = charged_sort::<TreeFault>(tree.n, work, |a, b| {
        component_cmp(tree.row(a).path, tree.row(b).path).is_lt()
    })
    .map_err(budget)?;
    let mut blobs = 0usize;
    for blob in candidate.blobs() {
        blobs += 1;
        let found = charged_find::<TreeFault>(&tree, &order, blob.path(), work).map_err(budget)?;
        let Some(index) = found else {
            return Err(TreeReadFailure::Association);
        };
        let RowKind::File { length, sha256 } = tree.row(index).kind else {
            return Err(TreeReadFailure::Association);
        };
        if length != blob.bytes() || &inst::hex64(&sha256)[..] != blob.sha256().as_bytes() {
            return Err(TreeReadFailure::Association);
        }
    }
    if blobs != tree.files {
        return Err(TreeReadFailure::Association);
    }
    // `<closure2-hex>`: its name's record and its descent, retained.
    work.charge(owned_record(inst::NAME_BYTES + 1))
        .map_err(budget)?;
    let generation = match descend(&store.directory, evidence.name, None, work) {
        Ok(level) => level.directory,
        Err(WorkFailure::Operation(TreeFault::Io { error, .. }))
            if error.kind() == io::ErrorKind::NotFound =>
        {
            return Err(TreeReadFailure::NotInstalled);
        }
        Err(WorkFailure::Operation(TreeFault::Io { error, .. }))
            if ct::is_not_directory(&error) =>
        {
            return Err(TreeReadFailure::Type { row: None });
        }
        Err(e) => return Err(budget(e)),
    };
    match store.custody::<TreeFault>(generation.as_file(), work) {
        Ok(Ok(())) => {}
        Ok(Err(refusal)) => return Err(TreeReadFailure::Custody(refusal)),
        Err(e) => return Err(budget(e)),
    }
    // The pin, before anything else of the generation is read: the existing
    // `pin.lock`, never created, a regular empty `0600` file, then one
    // shared `flock`. Busy (an exclusive GC probe) fails `Pin`, unretried.
    let pin_file = match ct::open_regular_no_follow(&generation, inst::PIN, Access::ReadOnly, work)
    {
        Ok(file) => file,
        Err(WorkFailure::Budget(b)) => return Err(TreeReadFailure::Budget(b)),
        Err(WorkFailure::Operation(TreeOpenError::Absent | TreeOpenError::NotRegular)) => {
            return Err(TreeReadFailure::Pin);
        }
        Err(WorkFailure::Operation(e)) => return Err(io_failure("openat", e)),
    };
    if pin_file.mode() != 0o600 || pin_file.length() != 0 {
        return Err(TreeReadFailure::Pin);
    }
    let pin = match ct::try_pin(pin_file, PinMode::Shared, work) {
        Ok(Ok(pin)) => pin,
        Ok(Err(_busy)) => return Err(TreeReadFailure::Pin),
        Err(WorkFailure::Budget(b)) => return Err(TreeReadFailure::Budget(b)),
        Err(WorkFailure::Operation(error)) => {
            return Err(TreeReadFailure::Io {
                call: "flock",
                error,
            });
        }
    };
    // `generation.json`: the owned expected record, compared byte for byte.
    work.charge(owned_record(evidence.record.length()))
        .map_err(budget)?;
    let expected = evidence.record.encode();
    work.charge(inst::buffer_cost()).map_err(budget)?;
    let mut buffer = vec![0u8; READ_CHUNK];
    inst::check_record(&generation, &expected, &mut buffer, work).map_err(TreeReadFailure::of)?;
    drop(expected);
    // `tree/`, retained as the capability's base, and its own mode.
    let tree_dir = descend(&generation, TREE, None, work)
        .map_err(TreeReadFailure::of)?
        .directory;
    inst::tree_root_mode(&generation, work).map_err(TreeReadFailure::of)?;
    // The structure, the installed modes, the link targets and every byte.
    inst::walk(&tree_dir, &tree, &order, Phase::Opened, &mut buffer, work)
        .map_err(TreeReadFailure::of)?;
    work.charge(capability_cost()).map_err(budget)?;
    Ok(RetainedTree {
        store,
        generation,
        tree_dir,
        pin,
        buffer,
        tree,
        order,
        request,
        name: evidence.name,
        latched: None,
    })
}

fn io_failure(call: &'static str, e: TreeOpenError) -> TreeReadFailure {
    match e {
        TreeOpenError::Io(error) => TreeReadFailure::Io { call, error },
        TreeOpenError::Absent => TreeReadFailure::Io {
            call,
            error: io::Error::new(io::ErrorKind::NotFound, "absent"),
        },
        other => TreeReadFailure::Io {
            call,
            error: io::Error::new(io::ErrorKind::InvalidInput, format!("{other:?}")),
        },
    }
}

impl RetainedTree<'_, '_> {
    /// The pin's mode: always shared.
    pub fn pin_mode(&self) -> PinMode {
        self.pin.mode()
    }
    /// The fence the caller declared it held while pinning.
    pub fn request(&self) -> PinRequest {
        self.request
    }
    /// Transfer the regular file at `path` to `sink`, verified (LAW item 6):
    /// its row found through the retained index (CI-A2-c), its parent chain
    /// resolved one no-follow component at a time from the retained `tree/`
    /// handle, its type, mode and length re-checked, then its bytes streamed
    /// through the retained buffer in charged attempts, hashed as they go.
    /// The sink is told at the end whether the stream verified.
    pub fn transfer(
        &mut self,
        path: &str,
        sink: &mut impl VerifiedSink,
        work: &mut WorkScope<'_>,
    ) -> Result<(), TreeReadFailure> {
        if let Some(latched) = self.latched {
            sink.finish(false);
            return Err(latched.failure());
        }
        let result = self.transfer_inner(path, sink, work);
        if let Err(failure) = &result {
            self.latched = Some(Latched::of(failure));
            sink.finish(false);
        }
        result
    }
    fn transfer_inner(
        &mut self,
        path: &str,
        sink: &mut impl VerifiedSink,
        work: &mut WorkScope<'_>,
    ) -> Result<(), TreeReadFailure> {
        let found =
            charged_find::<TreeFault>(&self.tree, &self.order, path, work).map_err(budget)?;
        let index = found.ok_or(TreeReadFailure::Association)?;
        let row = self.tree.row(index);
        let RowKind::File { length, sha256 } = row.kind else {
            return Err(TreeReadFailure::Association);
        };
        let (parent, name) = split(row.path);
        let mut chain: Vec<RetainedDirectory> = Vec::new();
        if !parent.is_empty() {
            for segment in parent.split('/') {
                let from = chain.last().unwrap_or(&self.tree_dir);
                let level = descend(from, segment, None, work).map_err(|e| match e {
                    WorkFailure::Operation(TreeFault::Io { error, .. })
                        if error.kind() == io::ErrorKind::NotFound =>
                    {
                        TreeReadFailure::Absent { row: index }
                    }
                    WorkFailure::Operation(TreeFault::Io { error, .. })
                        if ct::is_not_directory(&error) =>
                    {
                        TreeReadFailure::Type { row: Some(index) }
                    }
                    other => TreeReadFailure::of(other),
                })?;
                chain.push(level.directory);
            }
        }
        let directory = chain.last().unwrap_or(&self.tree_dir);
        let file = match ct::open_regular_no_follow(directory, name, Access::ReadOnly, work) {
            Ok(file) => file,
            Err(WorkFailure::Budget(b)) => return Err(TreeReadFailure::Budget(b)),
            Err(WorkFailure::Operation(TreeOpenError::Absent)) => {
                return Err(TreeReadFailure::Absent { row: index });
            }
            Err(WorkFailure::Operation(TreeOpenError::NotRegular)) => {
                return Err(TreeReadFailure::Type { row: Some(index) });
            }
            Err(WorkFailure::Operation(e)) => return Err(io_failure("openat", e)),
        };
        if file.mode() != inst::installed_mode(&row) {
            return Err(TreeReadFailure::Mode { row: Some(index) });
        }
        if file.length() != length {
            return Err(TreeReadFailure::Length { row: index });
        }
        sink.begin(sha256, length);
        read_verified(
            &file,
            index,
            length,
            sha256,
            &mut self.buffer,
            work,
            |bytes| sink.chunk(bytes),
        )
        .map_err(TreeReadFailure::of)?;
        sink.finish(true);
        Ok(())
    }
}

// ---- The launch member (CI-A3; unit CI-3L) ----

/// What `launch_member` resolves (CI-A3-a). The caller names a path; the
/// capability decides what it resolves to.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum MemberRequest<'r> {
    /// The selected platform row's `entrypoint`, taken from the same
    /// authenticated association the capability holds, never from the caller.
    Entrypoint,
    /// A regular-file row.
    File(&'r str),
    /// A `dir` row, or `""` for `tree/` itself.
    Directory(&'r str),
}
impl MemberRequest<'_> {
    fn wants_file(self) -> bool {
        !matches!(self, Self::Directory(_))
    }
    fn is_tree_root(self) -> bool {
        self == Self::Directory("")
    }
}

/// A launch member (CI-A3-a): the owned launch path, bound by its
/// re-observation to the verified member's `(device, inode)`, the row's
/// SHA-256 (files) and the row's index (`None` for `tree/` itself). Only
/// `launch_member` constructs one, and it borrows the capability, so it
/// cannot outlive the pin (CI-T27's lifetime probe):
/// ```compile_fail,E0505
/// use opensip_lifecycle::retained_tree::{MemberRequest, RetainedTree};
/// use opensip_platform::WorkScope;
/// fn outlives(mut tree: RetainedTree<'_, '_>, work: &mut WorkScope<'_>) {
///     let member = tree.launch_member(MemberRequest::Entrypoint, work).unwrap();
///     drop(tree);
///     assert!(member.path().is_absolute());
/// }
/// ```
/// The same use while the capability lives compiles:
/// ```no_run
/// use opensip_lifecycle::retained_tree::{MemberRequest, RetainedTree};
/// use opensip_platform::WorkScope;
/// fn within(mut tree: RetainedTree<'_, '_>, work: &mut WorkScope<'_>) {
///     let member = tree.launch_member(MemberRequest::Entrypoint, work).unwrap();
///     assert!(member.path().is_absolute());
///     drop(tree);
/// }
/// ```
#[derive(Debug)]
pub struct LaunchMember<'c> {
    path: PathBuf,
    /// Start of the resolved committed member in the already-bound path.
    /// The store prefix may contain arbitrary native bytes or `tree` names.
    member_offset: usize,
    device: u64,
    inode: u64,
    sha256: Option<[u8; 32]>,
    row: Option<u32>,
    capability: PhantomData<&'c ()>,
}
impl LaunchMember<'_> {
    /// The absolute launch path, which names no link at its final component.
    pub fn path(&self) -> &Path {
        &self.path
    }
    /// The actual resolved TreeCommitment member, not the caller's alias.
    /// Only the suffix copied from the validated UTF-8 row is interpreted.
    pub fn member(&self) -> Option<&str> {
        self.path
            .as_os_str()
            .as_encoded_bytes()
            .get(self.member_offset..)
            .and_then(|bytes| std::str::from_utf8(bytes).ok())
    }
    /// Move the funded bound spelling without copying its buffer. The
    /// operation must retain the capability through settlement (CI-A3-f),
    /// as it must for an owned/clonable D1a launch value.
    pub fn into_path(self) -> PathBuf {
        self.path
    }
    pub fn device(&self) -> u64 {
        self.device
    }
    pub fn inode(&self) -> u64 {
        self.inode
    }
    /// The verified file's SHA-256; `None` for a directory member.
    pub fn sha256(&self) -> Option<[u8; 32]> {
        self.sha256
    }
    /// The member's row in the TreeCommitment; `None` for `tree/` itself.
    pub fn row(&self) -> Option<u32> {
        self.row
    }
}

/// An owned temporary or buffer of `bytes` bytes: objects 1, bytes `bytes`
/// (CI-A3-b's hop temporaries and launch-path buffer).
pub(crate) fn heap(bytes: usize) -> WorkCost {
    WorkCost {
        objects: 1,
        edges: 0,
        bytes,
    }
}

/// `LM`: the result record's size, a compile-time property of the code.
pub(crate) fn launch_member_cost() -> WorkCost {
    heap(size_of::<LaunchMember<'static>>())
}

/// `<storePath>/<closure2-hex>/tree`'s length beyond `L`: `1 + 64 + 1 + 4`.
const GENERATION_TREE: usize = 1 + inst::NAME_BYTES + 1 + TREE.len();

/// `P`: the launch path's length without its terminator (CI-A3-b).
pub(crate) fn launch_path_length(store: usize, member: usize) -> Option<usize> {
    let base = store.checked_add(GENERATION_TREE)?;
    if member == 0 {
        Some(base)
    } else {
        base.checked_add(1)?.checked_add(member)
    }
}

/// A hop's joined path: the link's parent path, `/` unless the parent is
/// the root, and the target text (the security owner's rule,
/// `component_manifest.rs`'s `resolve`).
fn joined_length_parts(parent: usize, target: usize) -> Result<usize, TreeReadFailure> {
    let length = if parent == 0 {
        Some(target)
    } else {
        parent.checked_add(1).and_then(|n| n.checked_add(target))
    };
    length.ok_or(TreeReadFailure::Budget(WorkBudgetError::Arithmetic))
}
fn joined_length(link: &str, target: &str) -> Result<usize, TreeReadFailure> {
    let (parent, _) = split(link);
    joined_length_parts(parent.len(), target.len())
}

/// The largest segment of `path`.
fn longest_segment(path: &str) -> usize {
    path.split('/').map(str::len).max().unwrap_or(0)
}

/// `k`: a member path's component count (`0` for `tree/` itself).
fn components(path: &str) -> usize {
    if path.is_empty() {
        0
    } else {
        inst::depth(path)
    }
}

/// `B̂_launch(request)` (CI-A3-b), with checked arithmetic: every
/// member-dependent quantity replaced by its maximum over the TreeCommitment
/// (`0` over an empty set). It funds a request in advance; it is never
/// charged in place of the actual charges.
pub(crate) fn launch_pre_bound(
    tree: &Tree<'_>,
    store: usize,
    request: MemberRequest<'_>,
) -> Option<WorkCost> {
    let st = ct::status_read_cost();
    let tail = |p: usize| -> Option<inst::Bound> {
        inst::Bound::default()
            .add(heap(launch_path_length(store, p)?.checked_add(1)?))?
            .add(st)?
            .add(launch_member_cost())
    };
    if request.is_tree_root() {
        return Some(tail(0)?.add(st)?.0);
    }
    let kind = inst::Bound::default().add(inst::COMPARISON)?;
    let count = if request.wants_file() {
        tree.files
    } else {
        tree.dirs
    };
    if count == 0 {
        return Some(kind.0);
    }
    let (mut q, mut p, mut k, mut seg, mut c) = (0usize, 0usize, 0usize, 0usize, 0u64);
    for row in tree.rows() {
        match row.kind {
            RowKind::Symlink { target } => {
                q = q.max(joined_length(row.path, target).ok()?);
                continue;
            }
            RowKind::File { length, .. } if request.wants_file() => c = c.max(length),
            RowKind::Dir if !request.wants_file() => {}
            _ => continue,
        }
        p = p.max(row.path.len());
        k = k.max(components(row.path));
        seg = seg.max(longest_segment(row.path));
    }
    let s = tree.links;
    let mut b = kind
        .add_times(
            inst::COMPARISON,
            s.checked_add(1)?.checked_mul(search_comparisons(tree.n))?,
        )?
        .add_times(heap(q), s)?;
    if request.wants_file() {
        b = b
            .add_times(descend_cost(seg), k.saturating_sub(1))?
            .add(ct::open_regular_no_follow_cost())?
            .add_times(READ, usize::try_from(envelope(c)).ok()?)?;
    } else {
        b = b.add_times(descend_cost(seg), k)?.add(st)?;
    }
    Some(b.add(tail(p)?.0)?.0)
}

/// The binding's observation, with CI-T28's partition seam under test: a
/// hook's error replaces a successful observation's result, as the native
/// call's own error would.
fn observe_path(
    path: &CStr,
    work: &mut WorkScope<'_>,
) -> Result<PathStatus, WorkFailure<PathStatusError>> {
    let status = ct::path_status_no_follow(path, work);
    // The seam marks a native call made: not a budget refusal.
    if !matches!(status, Err(WorkFailure::Budget(_))) {
        path_seam()?;
    }
    status
}
#[cfg(test)]
fn path_seam() -> Result<(), WorkFailure<PathStatusError>> {
    inst::seams::at("lstat").map_err(|error| {
        WorkFailure::Operation(if error.kind() == io::ErrorKind::NotFound {
            PathStatusError::Absent
        } else if error.kind() == io::ErrorKind::NotADirectory || ct::is_not_directory(&error) {
            PathStatusError::NotDirectory
        } else {
            PathStatusError::Io(error)
        })
    })
}
#[cfg(not(test))]
fn path_seam() -> Result<(), WorkFailure<PathStatusError>> {
    Ok(())
}

/// Lexical resolution over the retained index (CI-A3-a): at most
/// `S + 1` lookups, each hop's joined path an owned temporary, charged
/// before it is allocated and dropped after the lookup it funds. The
/// final row must be of the requested kind.
pub(crate) fn resolve(
    tree: &Tree<'_>,
    order: &[u32],
    request: MemberRequest<'_>,
    work: &mut WorkScope<'_>,
) -> Result<u32, TreeReadFailure> {
    let path = match request {
        MemberRequest::Entrypoint => tree.entrypoint.ok_or(TreeReadFailure::Association)?,
        MemberRequest::File(path) | MemberRequest::Directory(path) => path,
    };
    let mut hop: Option<String> = None;
    let mut lookups = 0usize;
    loop {
        if lookups == tree.links.saturating_add(1) {
            return Err(TreeReadFailure::Association);
        }
        lookups += 1;
        let wanted = hop.as_deref().unwrap_or(path);
        let found = charged_find::<TreeFault>(tree, order, wanted, work).map_err(budget)?;
        drop(hop.take());
        let index = found.ok_or(TreeReadFailure::Association)?;
        let row = tree.row(index);
        match row.kind {
            RowKind::Symlink { target } => {
                // The last permitted lookup may establish a cycle or an
                // overlong chain, but cannot fund an (S + 1)th hop temporary.
                // Refused prefixes obey the same S-hop pre-bound as success.
                if lookups > tree.links {
                    return Err(TreeReadFailure::Association);
                }
                let length = joined_length(row.path, target)?;
                let (parent, _) = split(row.path);
                work.charge(heap(length)).map_err(budget)?;
                let mut joined = String::with_capacity(length);
                if !parent.is_empty() {
                    joined.push_str(parent);
                    joined.push('/');
                }
                joined.push_str(target);
                hop = Some(joined);
            }
            RowKind::File { .. } if request.wants_file() => return Ok(index),
            RowKind::Dir if !request.wants_file() => return Ok(index),
            _ => return Err(TreeReadFailure::Association),
        }
    }
}

impl RetainedTree<'_, '_> {
    /// `B̂_launch(request)` for this capability's TreeCommitment and store
    /// path (CI-A3-b), for a caller funding the launch in advance.
    pub fn launch_pre_bound(&self, request: MemberRequest<'_>) -> Option<WorkCost> {
        launch_pre_bound(&self.tree, self.store.path.as_os_str().len(), request)
    }

    /// The launch member (CI-A3-a): resolve `request` lexically over the
    /// TreeCommitment, re-observe the member from the retained `tree/`
    /// handle, compose its launch path once and bind it by a no-follow
    /// re-observation. Every charge is made immediately before its
    /// operation, at its actual count (`E_launch`). On a latched capability
    /// it refuses with the latched cause before any charge or observation;
    /// its own first failure of any kind, `Budget` included, latches it.
    pub fn launch_member(
        &mut self,
        request: MemberRequest<'_>,
        work: &mut WorkScope<'_>,
    ) -> Result<LaunchMember<'_>, TreeReadFailure> {
        if let Some(latched) = self.latched {
            return Err(latched.failure());
        }
        let result = self.launch_inner(request, work);
        if let Err(failure) = &result {
            self.latched = Some(Latched::of(failure));
        }
        result
    }

    /// The launch itself; its result borrows nothing until `launch_member`
    /// ties it to the capability.
    fn launch_inner(
        &mut self,
        request: MemberRequest<'_>,
        work: &mut WorkScope<'_>,
    ) -> Result<LaunchMember<'static>, TreeReadFailure> {
        // The kind check (r4): one charged comparison of the held count of
        // the requested kind against zero, before any lookup, hop or
        // allocation. `tree/` itself always exists.
        let index = if request.is_tree_root() {
            None
        } else {
            work.charge(inst::COMPARISON).map_err(budget)?;
            let count = if request.wants_file() {
                self.tree.files
            } else {
                self.tree.dirs
            };
            if count == 0 {
                return Err(TreeReadFailure::Association);
            }
            Some(resolve(&self.tree, &self.order, request, work)?)
        };
        let row = index.map(|i| self.tree.row(i));
        let member = row.map_or("", |row| row.path);
        // Observation from the retained base: the parent chain, one no-follow
        // component at a time (the final descent too, for a directory), then
        // the member itself.
        let descents = if request.wants_file() {
            components(member).saturating_sub(1)
        } else {
            components(member)
        };
        let mut level: Option<RetainedDirectory> = None;
        for segment in member.split('/').take(descents) {
            let from = level.as_ref().unwrap_or(&self.tree_dir);
            let next = descend(from, segment, index, work).map_err(TreeReadFailure::of)?;
            level = Some(next.directory);
        }
        let directory = level.as_ref().unwrap_or(&self.tree_dir);
        let (device, inode, sha256) = match (row, index) {
            (Some(row), Some(index)) if request.wants_file() => {
                let RowKind::File { length, sha256 } = row.kind else {
                    return Err(TreeReadFailure::Association);
                };
                let (_, name) = split(row.path);
                let file = match ct::open_regular_no_follow(directory, name, Access::ReadOnly, work)
                {
                    Ok(file) => file,
                    Err(WorkFailure::Budget(b)) => return Err(TreeReadFailure::Budget(b)),
                    Err(WorkFailure::Operation(TreeOpenError::Absent)) => {
                        return Err(TreeReadFailure::Absent { row: index });
                    }
                    Err(WorkFailure::Operation(TreeOpenError::NotRegular)) => {
                        return Err(TreeReadFailure::Type { row: Some(index) });
                    }
                    // A committed path is at most 100 bytes (CI-T5), so the
                    // stack name never refuses one.
                    Err(WorkFailure::Operation(TreeOpenError::Name)) => {
                        return Err(TreeReadFailure::Association);
                    }
                    Err(WorkFailure::Operation(e)) => return Err(io_failure("openat", e)),
                };
                if file.mode() != inst::installed_mode(&row) {
                    return Err(TreeReadFailure::Mode { row: Some(index) });
                }
                if file.length() != length {
                    return Err(TreeReadFailure::Length { row: index });
                }
                read_verified(&file, index, length, sha256, &mut self.buffer, work, |_| {})
                    .map_err(TreeReadFailure::of)?;
                let identity = file.identity();
                (identity.device, identity.inode, Some(sha256))
            }
            _ => {
                let status = ct::directory_identity(directory, work).map_err(|e| match e {
                    WorkFailure::Budget(b) => TreeReadFailure::Budget(b),
                    WorkFailure::Operation(error) => TreeReadFailure::Io {
                        call: "fstat",
                        error,
                    },
                })?;
                if status.kind != EntryKind::Directory {
                    return Err(TreeReadFailure::Type { row: index });
                }
                // LD-CI-10: a directory inside `tree/`, and `tree/` itself, `0500`.
                let mode = row.map_or(0o500, |row| inst::installed_mode(&row));
                if status.mode != mode {
                    return Err(TreeReadFailure::Mode { row: index });
                }
                (status.device, status.inode, None)
            }
        };
        drop(level);
        // The path binding: one owned NUL-terminated buffer of `P + 1` bytes,
        // composed once, re-observed no-follow, then the result's path.
        let store: &[u8] = {
            use std::os::unix::ffi::OsStrExt;
            self.store.path.as_os_str().as_bytes()
        };
        let length = launch_path_length(store.len(), member.len())
            .and_then(|p| p.checked_add(1))
            .ok_or(TreeReadFailure::Budget(WorkBudgetError::Arithmetic))?;
        work.charge(heap(length)).map_err(budget)?;
        let mut bytes = Vec::with_capacity(length);
        bytes.extend_from_slice(store);
        bytes.push(b'/');
        bytes.extend_from_slice(self.name.as_bytes());
        bytes.push(b'/');
        bytes.extend_from_slice(TREE.as_bytes());
        if !member.is_empty() {
            bytes.push(b'/');
            bytes.extend_from_slice(member.as_bytes());
        }
        bytes.push(0);
        // The store path and a committed row hold no NUL, so this never
        // refuses; if it did, the path would not name the member.
        let spelling = CStr::from_bytes_with_nul(&bytes).map_err(|_| TreeReadFailure::Binding)?;
        let observed = match observe_path(spelling, work) {
            Ok(status) => status,
            Err(WorkFailure::Budget(b)) => return Err(TreeReadFailure::Budget(b)),
            Err(WorkFailure::Operation(
                PathStatusError::Absent | PathStatusError::NotDirectory,
            )) => {
                return Err(TreeReadFailure::Binding);
            }
            Err(WorkFailure::Operation(PathStatusError::Io(error))) => {
                return Err(TreeReadFailure::Io {
                    call: "lstat",
                    error,
                });
            }
        };
        let kind = if request.wants_file() {
            EntryKind::File
        } else {
            EntryKind::Directory
        };
        if observed.kind != kind || (observed.device, observed.inode) != (device, inode) {
            return Err(TreeReadFailure::Binding);
        }
        // The NUL is dropped in place: the buffer becomes the path unmoved.
        bytes.pop();
        let path = {
            use std::os::unix::ffi::OsStringExt;
            PathBuf::from(std::ffi::OsString::from_vec(bytes))
        };
        work.charge(launch_member_cost()).map_err(budget)?;
        let member_offset = path
            .as_os_str()
            .len()
            .checked_sub(member.len())
            .ok_or(TreeReadFailure::Association)?;
        Ok(LaunchMember {
            path,
            member_offset,
            device,
            inode,
            sha256,
            row: index,
            capability: PhantomData,
        })
    }
}

#[cfg(test)]
#[path = "retained_tree_tests.rs"]
mod tests;
