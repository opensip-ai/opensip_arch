// Law 463 (r3, amendment items 1-12 and r9): the executing core's identity for
// the initial creator, owner §1a step 3. The kernel-validated running image is
// joined to the entrypoint row of a release authenticated from the root
// embedded in that image. No argv, PATH, current_exe, listing or record from I.
use super::admitted_payload_paths as Paths;
use super::core_authentication::{EmbeddedRelease, ReleaseError, authenticate_embedded_release};
use super::core_inventory as Core;
use super::core_release_embedding::{
    AdmittedEmbedding, COMPILED_PLATFORM, EMBEDDED_CORE_RELEASE, EmbeddedCoreRelease,
    EmbeddingAbsent,
};
use super::retained_metadata_index::{self as M, Budget, Collection, ReadRequest};
use super::*;
use crate::custody::{CoreTreeKind, Refusal, check_core_tree_member};
use crate::initial_installation::InitialInstallationAttempt;
use opensip_identity::{JsonInteger, canonical_bytes, digest_hex, raw_sha256};
use opensip_platform::{
    DescriptorAclCapture, DescriptorAclCaptureError, DescriptorMetadata, RetainedDirectory,
    RetainedDirectoryPath, RunningImageError, RunningImageObservation, WorkCost, WorkFailure,
    WorkReadFailure, WorkScope,
};
use std::{ffi::OsStr, fs::File, io, os::unix::ffi::OsStrExt, sync::Arc};

/// The running image read bound. The security test binary exceeds it (item 11).
const MAX_IMAGE_BYTES: usize = 96 * 1024 * 1024;
/// One release file, and all bootstrap members together.
const MAX_FILE_BYTES: usize = 4 * 1024 * 1024;
const MAX_MEMBER_BYTES: usize = 16 * 1024 * 1024;
const MAX_MEMBERS: usize = 130;
const INVENTORY: [&str; 2] = ["inventory.json", "inventory.sig.json"];
const PAYLOAD: [&str; 2] = ["payload.json", "payload.sig.json"];
/// A status read with a buffer no smaller than the native `stat`.
const STATUS: WorkCost = WorkCost {
    objects: 0,
    edges: 1,
    bytes: 512,
};
/// Paths joined from the embedded values or a manifest row, each at most 4096 bytes.
const PATH_COST: WorkCost = WorkCost {
    objects: 1,
    edges: 0,
    bytes: 4096,
};

/// Which part of the core tree a refusal names.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum CoreMember {
    /// The tree root and the directories down to the entrypoint.
    Tree,
    Executable,
    Inventory,
    /// The bootstrap directories and any member subdirectory.
    Bootstrap,
    Payload,
    Member,
    /// The platform profile files and their directory (law 462 item 1).
    Platform,
}

#[derive(Debug)]
pub(crate) enum InitialCoreRefusal {
    EmbeddedRootAbsent,
    EmbeddedEntrypointAbsent,
    EmbeddedBootstrapAbsent,
    PlatformUnavailable,
    Image(RunningImageError),
    /// The executable or a tree directory is not the embedded entrypoint name.
    EntrypointName,
    /// The entrypoint has as many components as the kernel path, or more.
    TreeRootBound,
    Absent(CoreMember),
    Name(CoreMember),
    Native(CoreMember, io::Error),
    Acl(CoreMember, DescriptorAclCaptureError),
    Custody(CoreMember, Refusal),
    Read(CoreMember, WorkReadFailure),
    Size(CoreMember),
    Changed(CoreMember),
    BootstrapLocator,
    /// Law 463 item 9.
    BootstrapEnvelopeSet,
    Inventory(Core::Error),
    Anchor,
    Release(ReleaseError),
    BootstrapPath,
    EntrypointRow,
    EntrypointBytes,
    /// Law 463 item 8.
    ReleaseRevoked,
    CodeSigningFlags,
    StateWriter,
    WrongAttempt,
}
type Failure = WorkFailure<InitialCoreRefusal>;
use InitialCoreRefusal as R;

/// K (owner §1a step 3; law 463 item 6).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum StateWriter {
    Stage1,
    Stage2,
}

enum Image {
    Running(RunningImageObservation),
    #[cfg(any(test, feature = "crash-matrix", feature = "scenario-fixtures"))]
    Injected(tests::InjectedImage),
}
impl Image {
    fn status(&self) -> u32 {
        match self {
            Self::Running(o) => o.code_signing_status(),
            #[cfg(any(test, feature = "crash-matrix", feature = "scenario-fixtures"))]
            Self::Injected(i) => i.status,
        }
    }
    fn cdhash(&self) -> [u8; 20] {
        match self {
            Self::Running(o) => o.cdhash(),
            #[cfg(any(test, feature = "crash-matrix", feature = "scenario-fixtures"))]
            Self::Injected(i) => i.cdhash,
        }
    }
    fn parents(&self) -> &RetainedDirectoryPath {
        match self {
            Self::Running(o) => o.parents(),
            #[cfg(any(test, feature = "crash-matrix", feature = "scenario-fixtures"))]
            Self::Injected(i) => &i.parents,
        }
    }
    fn leaf(&self) -> &OsStr {
        match self {
            Self::Running(o) => o.leaf(),
            #[cfg(any(test, feature = "crash-matrix", feature = "scenario-fixtures"))]
            Self::Injected(i) => &i.leaf,
        }
    }
    fn sha256(&self) -> [u8; 32] {
        match self {
            Self::Running(o) => o.sha256(),
            #[cfg(any(test, feature = "crash-matrix", feature = "scenario-fixtures"))]
            Self::Injected(i) => i.sha256,
        }
    }
    fn length(&self) -> usize {
        match self {
            Self::Running(o) => o.length(),
            #[cfg(any(test, feature = "crash-matrix", feature = "scenario-fixtures"))]
            Self::Injected(i) => i.length,
        }
    }
    fn metadata(&self) -> &DescriptorMetadata {
        match self {
            Self::Running(o) => o.metadata(),
            #[cfg(any(test, feature = "crash-matrix", feature = "scenario-fixtures"))]
            Self::Injected(i) => &i.metadata,
        }
    }
    fn capture_file_acl(
        &self,
        work: &mut WorkScope<'_>,
    ) -> Result<DescriptorAclCapture, WorkFailure<DescriptorAclCaptureError>> {
        match self {
            Self::Running(o) => o.capture_file_acl(work),
            #[cfg(any(test, feature = "crash-matrix", feature = "scenario-fixtures"))]
            Self::Injected(i) => opensip_platform::capture_descriptor_acl_accounted(&i.file, work),
        }
    }
    fn leaf_name_matches_accounted(
        &self,
        work: &mut WorkScope<'_>,
    ) -> Result<bool, WorkFailure<RunningImageError>> {
        match self {
            Self::Running(o) => o.leaf_name_matches_accounted(work),
            #[cfg(any(test, feature = "crash-matrix", feature = "scenario-fixtures"))]
            Self::Injected(i) => i.leaf_name_matches_accounted(work),
        }
    }
    fn recheck(&self, work: &mut WorkScope<'_>) -> Result<(), WorkFailure<RunningImageError>> {
        match self {
            Self::Running(o) => o.recheck(work),
            #[cfg(any(test, feature = "crash-matrix", feature = "scenario-fixtures"))]
            Self::Injected(i) => i.recheck(work),
        }
    }
}

/// A retained directory below the tree root; `parent` indexes `directories`,
/// and None is the tree root.
struct HeldDirectory {
    parent: Option<usize>,
    name: String,
    directory: RetainedDirectory,
    metadata: DescriptorMetadata,
    member: CoreMember,
}
struct HeldFile {
    parent: Option<usize>,
    name: String,
    file: File,
    metadata: DescriptorMetadata,
    member: CoreMember,
}

/// Owner §1a step 3's receipt. Private, not Clone, bound to one attempt.
pub(crate) struct InitialCore {
    lineage: [u8; 16],
    image: Image,
    executable: DescriptorMetadata,
    root_index: usize,
    tree: Vec<DescriptorMetadata>,
    tree_root: RetainedDirectory,
    directories: Vec<HeldDirectory>,
    files: Vec<HeldFile>,
    release: EmbeddedRelease,
    platform: &'static str,
    state_writer: StateWriter,
    flags: u32,
    bootstrap: BootstrapDocuments,
}
impl std::fmt::Debug for InitialCore {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("InitialCore").finish_non_exhaustive()
    }
}
impl InitialCore {
    pub(crate) fn lineage(&self) -> [u8; 16] {
        self.lineage
    }
    /// The authenticated inventory's `closure2:` identity for this platform.
    pub(crate) fn closure(&self) -> &str {
        self.release.authentication().core().inventory().closure()
    }
    /// Contract successor EC1 (law X3d r8 item 13): the core evaluator
    /// closure, from the same authenticated inventory as `closure`, on the
    /// running and the injected arm alike. It differs from `closure` only by
    /// the descriptor's `kind`.
    pub(crate) fn evaluator_closure(&self) -> &str {
        self.release
            .authentication()
            .core()
            .inventory()
            .evaluator_closure()
    }
    /// CRC-1: identities from the already authenticated core inventory.
    /// These accessors do not grant field-use or semanticClosures admission.
    pub(crate) fn detector_closure(&self) -> &str {
        self.release
            .authentication()
            .core()
            .inventory()
            .detector_closure()
    }
    pub(crate) fn provider_closure(&self) -> &str {
        self.release
            .authentication()
            .core()
            .inventory()
            .provider_closure()
    }
    pub(crate) fn adapter_closure(&self) -> &str {
        self.release
            .authentication()
            .core()
            .inventory()
            .adapter_closure()
    }
    pub(crate) fn platform(&self) -> &'static str {
        self.platform
    }
    pub(crate) fn state_writer(&self) -> StateWriter {
        self.state_writer
    }
    pub(crate) fn cdhash(&self) -> [u8; 20] {
        self.image.cdhash()
    }
    /// Law 463 r9 item 2: the retained catalog pair and component-manifest
    /// pairs, for first trust acceptance (X4B r5 item 2). Raw bytes with
    /// their references; nothing here was verified, and nothing is granted.
    pub(crate) fn bootstrap_documents(&self) -> &BootstrapDocuments {
        &self.bootstrap
    }
    /// Law X4B r5 item 2 (unit X4B-a): the rest of the payload first trust
    /// acceptance reads, as the authenticated release retains it. The
    /// anchor's root binding (the embedded one), the bootstrap manifest and
    /// core inventory pairs, and the root chain's pairs in chain order. Raw
    /// bytes only; acceptance verifies them again and nothing is granted.
    pub(crate) fn bootstrap_release(&self) -> BootstrapRelease<'_> {
        let core = self.release.authentication().core();
        let pair = |name: &str| {
            let (body, envelope) = &core.initial()[name];
            (&body[..], &envelope[..])
        };
        BootstrapRelease {
            binding: &object(core.anchor().value()).expect("admitted anchor")["binding"],
            manifest: pair("bootstrapManifest"),
            inventory: pair("coreInventory"),
            chain: core
                .roots()
                .iter()
                .map(|p| (p.body(), p.envelope()))
                .collect(),
        }
    }
    /// Re-sample the image, every judged directory and every opened file on
    /// the attempt's ledger. A sample, not exclusion. Any refusal latches.
    pub(crate) fn recheck(&self, attempt: &mut InitialInstallationAttempt) -> Result<(), Failure> {
        if !attempt.require_lineage(self.lineage) {
            return Err(WorkFailure::Operation(R::WrongAttempt));
        }
        attempt.run(|work| self.recheck_in(work))
    }
    /// The same recheck on a borrowed scope, for a caller that has already
    /// checked the lineage (law 467 item 6: inside the rename's reservation).
    pub(crate) fn recheck_in(&self, work: &mut WorkScope<'_>) -> Result<(), Failure> {
        self.image.recheck(work).map_err(lift(R::Image))?;
        let mut tree = self.tree.iter();
        self.image.parents().visit_directories(|i, directory| {
            if i < self.root_index {
                return Ok(());
            }
            let capture = judge(
                directory.as_file(),
                CoreMember::Tree,
                CoreTreeKind::Directory,
                work,
            )?;
            same(capture.metadata(), tree.next(), CoreMember::Tree)
        })?;
        recheck_held(&self.tree_root, &self.directories, &self.files, work)?;
        let capture = self
            .image
            .capture_file_acl(work)
            .map_err(lift(|e| R::Acl(CoreMember::Executable, e)))?;
        judged(&capture, CoreMember::Executable, CoreTreeKind::Regular)?;
        same(
            capture.metadata(),
            Some(&self.executable),
            CoreMember::Executable,
        )
    }
    /// The final authenticated root (law 462 item 2).
    pub(super) fn final_root(&self) -> &ValidatedRootPayload {
        let authentication = self.release.authentication();
        authentication
            .chain()
            .links()
            .last()
            .map_or(authentication.anchor(), |link| link.root())
    }
    /// The revoked key set after law 463 item 5.
    pub(super) fn revoked(&self) -> &BTreeSet<[u8; 32]> {
        self.release.revoked()
    }
    /// The signed inventory's `platformProfileBinding.platformProfileSetBodyDigest`.
    pub(super) fn profile_pin(&self) -> Option<[u8; 32]> {
        object(self.release.authentication().core().inventory().inventory())
            .and_then(|o| o.get("platformProfileBinding"))
            .and_then(object)
            .and_then(|o| o.get("platformProfileSetBodyDigest"))
            .and_then(string)
            .and_then(|s| decode_hex32(s).ok())
    }
    /// This platform row's `file` tree entry at `path`: its sha256 and length.
    pub(super) fn tree_file(&self, path: &str) -> Option<([u8; 32], i64)> {
        let row = self
            .release
            .authentication()
            .core()
            .inventory()
            .files()
            .get(self.platform)?
            .get(path)
            .and_then(object)?;
        let sha256 = row.get("sha256").and_then(string)?;
        Some((
            decode_hex32(sha256).ok()?,
            row.get("length").and_then(integer)?,
        ))
    }
    /// Law 462 item 1: one fixed release file below the tree root, each
    /// directory and the file opened no-follow by exact name and judged by the
    /// core-tree predicate (463 item 7). The tree root is duplicated, so the
    /// file's recheck needs no InitialCore. Never a listing.
    pub(super) fn open_release_file(
        &self,
        path: &[&str],
        work: &mut WorkScope<'_>,
    ) -> Result<(ReleaseFile, Vec<u8>), Failure> {
        let member = CoreMember::Platform;
        let tree_root = duplicate(&self.tree_root, work)?;
        let root = judge(tree_root.as_file(), member, CoreTreeKind::Directory, work)?;
        let (leaf, walk) = path.split_last().expect("a fixed path has a leaf");
        let mut directories = Vec::new();
        let mut parent = None;
        for component in walk {
            parent = Some(judge_directory(
                parent,
                &mut directories,
                &tree_root,
                component,
                member,
                work,
            )?);
        }
        let directory = parent.map_or(&tree_root, |i| &directories[i].directory);
        let (file, metadata, raw) = judge_file(directory, leaf, member, MAX_FILE_BYTES, work)?;
        let name = work.run(PATH_COST, |_| Ok((*leaf).to_owned()))?;
        let file = ReleaseFile {
            root: root.metadata().clone(),
            tree_root,
            directories,
            files: [HeldFile {
                parent,
                name,
                file,
                metadata,
                member,
            }],
            sha256: raw_sha256(&raw),
            length: raw.len(),
        };
        Ok((file, raw))
    }
}

/// A release file another owner opened below the tree root (law 462 item 1).
/// Private, not Clone; it holds its own tree root and directories.
pub(super) struct ReleaseFile {
    root: DescriptorMetadata,
    tree_root: RetainedDirectory,
    directories: Vec<HeldDirectory>,
    files: [HeldFile; 1],
    sha256: [u8; 32],
    length: usize,
}
impl ReleaseFile {
    pub(super) fn sha256(&self) -> [u8; 32] {
        self.sha256
    }
    pub(super) fn length(&self) -> usize {
        self.length
    }
    /// Re-judge the tree root, then each directory and the file by identity,
    /// exact name and custody. A sample, not exclusion.
    pub(super) fn recheck(&self, work: &mut WorkScope<'_>) -> Result<(), Failure> {
        let member = CoreMember::Platform;
        let root = judge(
            self.tree_root.as_file(),
            member,
            CoreTreeKind::Directory,
            work,
        )?;
        same(root.metadata(), Some(&self.root), member)?;
        recheck_held(&self.tree_root, &self.directories, &self.files, work)
    }
}

/// One listed bootstrap body and the listed envelope whose carrier stored
/// digest equals it (law 463 r9 item 9). Unverified: InitialCore judges
/// neither its signatures, its quorum nor its role.
pub(crate) struct BootstrapPair {
    body: DocumentBytes,
    envelope: DocumentBytes,
}
impl BootstrapPair {
    pub(crate) fn body(&self) -> &DocumentBytes {
        &self.body
    }
    pub(crate) fn envelope(&self) -> &DocumentBytes {
        &self.envelope
    }
}
/// A retained member's manifest path (under the bootstrap directory), its raw
/// bytes and its reference: `bytes` is the length, `sha256` the raw digest,
/// which equals the manifest row's listed digest.
pub(crate) struct DocumentBytes {
    path: String,
    raw: Arc<[u8]>,
    sha256: [u8; 32],
}
impl DocumentBytes {
    pub(crate) fn path(&self) -> &str {
        &self.path
    }
    pub(crate) fn raw(&self) -> &[u8] {
        &self.raw
    }
    pub(crate) fn bytes(&self) -> usize {
        self.raw.len()
    }
    pub(crate) fn sha256(&self) -> [u8; 32] {
        self.sha256
    }
}
/// The catalog pair, present only when item 9 admitted its envelope, and the
/// component-manifest pairs in `members.manifests` order. Law X4B r5 item 2
/// (unit X4B-a): also the revocation pair's stored bytes, which item 5
/// verified, so first trust acceptance can write the bytes it verifies again.
pub(crate) struct BootstrapDocuments {
    catalog: Option<BootstrapPair>,
    manifests: Vec<BootstrapPair>,
    revocation: BootstrapPair,
}
impl BootstrapDocuments {
    pub(crate) fn revocation(&self) -> &BootstrapPair {
        &self.revocation
    }
    pub(crate) fn catalog(&self) -> Option<&BootstrapPair> {
        self.catalog.as_ref()
    }
    pub(crate) fn manifests(&self) -> &[BootstrapPair] {
        &self.manifests
    }
}

/// Law X4B r5 item 2: borrowed views of the authenticated release's payload
/// documents (see `InitialCore::bootstrap_release`).
pub(crate) struct BootstrapRelease<'a> {
    pub(crate) binding: &'a V,
    pub(crate) manifest: (&'a [u8], &'a [u8]),
    pub(crate) inventory: (&'a [u8], &'a [u8]),
    pub(crate) chain: Vec<(&'a [u8], &'a [u8])>,
}

/// Reopen each held directory and file by name under its retained parent,
/// require the same object, its exact name and its custody.
fn recheck_held(
    tree_root: &RetainedDirectory,
    directories: &[HeldDirectory],
    files: &[HeldFile],
    work: &mut WorkScope<'_>,
) -> Result<(), Failure> {
    let parent = |index: Option<usize>| index.map_or(tree_root, |i| &directories[i].directory);
    for held in directories {
        let reopened = parent(held.parent)
            .open_child_directory_if_present_accounted(OsStr::new(&held.name), work)
            .map_err(lift(|e| opened(held.member, e)))?
            .ok_or(WorkFailure::Operation(R::Absent(held.member)))?;
        identical(reopened.as_file(), &held.metadata, held.member, work)?;
        name(held.directory.as_file(), &held.name, held.member, work)?;
        let capture = judge(
            held.directory.as_file(),
            held.member,
            CoreTreeKind::Directory,
            work,
        )?;
        same(capture.metadata(), Some(&held.metadata), held.member)?;
    }
    for held in files {
        let directory = parent(held.parent);
        let reopened = work.run(RetainedDirectory::open_regular_cost(&held.name), |_| {
            directory
                .open_regular(&held.name)
                .map_err(|e| WorkFailure::Operation(opened(held.member, e)))
        })?;
        identical(&reopened, &held.metadata, held.member, work)?;
        name(&held.file, &held.name, held.member, work)?;
        let capture = judge(&held.file, held.member, CoreTreeKind::Regular, work)?;
        same(capture.metadata(), Some(&held.metadata), held.member)?;
    }
    Ok(())
}

fn lift<E>(wrap: impl FnOnce(E) -> InitialCoreRefusal) -> impl FnOnce(WorkFailure<E>) -> Failure {
    move |failure| match failure {
        WorkFailure::Budget(budget) => WorkFailure::Budget(budget),
        WorkFailure::Operation(error) => WorkFailure::Operation(wrap(error)),
    }
}
/// A no-follow open that met a symlink is a custody refusal, and NotFound is absence.
fn opened(member: CoreMember, error: io::Error) -> InitialCoreRefusal {
    if error.raw_os_error() == Some(ELOOP) {
        R::Custody(member, Refusal::Symlink)
    } else if error.kind() == io::ErrorKind::NotFound {
        R::Absent(member)
    } else {
        R::Native(member, error)
    }
}
/// macOS `ELOOP`: an `O_NOFOLLOW` open of a symlink.
const ELOOP: i32 = 62;
fn operation<T>(ok: bool, value: T, refusal: InitialCoreRefusal) -> Result<T, Failure> {
    if ok {
        Ok(value)
    } else {
        Err(WorkFailure::Operation(refusal))
    }
}
/// Capture one descriptor's ACL and judge it as a core-tree member (items 7, 10).
fn judge(
    file: &File,
    member: CoreMember,
    kind: CoreTreeKind,
    work: &mut WorkScope<'_>,
) -> Result<DescriptorAclCapture, Failure> {
    let capture = opensip_platform::capture_descriptor_acl_accounted(file, work)
        .map_err(lift(|e| R::Acl(member, e)))?;
    judged(&capture, member, kind)?;
    Ok(capture)
}
fn judged(
    capture: &DescriptorAclCapture,
    member: CoreMember,
    kind: CoreTreeKind,
) -> Result<(), Failure> {
    check_core_tree_member(capture.metadata(), kind, capture.acl_state(), |i| {
        capture.entry(i)
    })
    .map_err(|refusal| WorkFailure::Operation(R::Custody(member, refusal)))
}
fn same(
    now: &DescriptorMetadata,
    then: Option<&DescriptorMetadata>,
    member: CoreMember,
) -> Result<(), Failure> {
    operation(then == Some(now), (), R::Changed(member))
}
/// The descriptor's on-disk name is exactly `expected` (APFS opens fold case).
fn name(
    file: &File,
    expected: &str,
    member: CoreMember,
    work: &mut WorkScope<'_>,
) -> Result<(), Failure> {
    let matches =
        opensip_platform::descriptor_name_matches_accounted(file, OsStr::new(expected), work)
            .map_err(lift(|e| R::Native(member, e)))?;
    operation(matches, (), R::Name(member))
}
/// A reopened handle names the held object: one status read.
fn identical(
    reopened: &File,
    held: &DescriptorMetadata,
    member: CoreMember,
    work: &mut WorkScope<'_>,
) -> Result<(), Failure> {
    use std::os::unix::fs::MetadataExt;
    work.run(STATUS, |_| {
        let now = reopened
            .metadata()
            .map_err(|e| WorkFailure::Operation(R::Native(member, e)))?;
        operation(
            now.dev() == held.device && now.ino() == held.inode,
            (),
            R::Changed(member),
        )
    })
}
/// One `dup` of a retained directory and its kind-check status read.
const DUP_COST: WorkCost = WorkCost {
    objects: 1,
    edges: 2,
    bytes: 512,
};
fn duplicate(
    directory: &RetainedDirectory,
    work: &mut WorkScope<'_>,
) -> Result<RetainedDirectory, Failure> {
    work.run(DUP_COST, |_| {
        directory
            .as_file()
            .try_clone()
            .and_then(RetainedDirectory::from_retained_handle)
            .map_err(|e| WorkFailure::Operation(R::Native(CoreMember::Tree, e)))
    })
}
/// Open, name, judge, bound, read and re-judge one release file under a
/// retained directory. `cap` bounds this file's size before its buffer.
fn judge_file(
    parent: &RetainedDirectory,
    leaf: &str,
    member: CoreMember,
    cap: usize,
    work: &mut WorkScope<'_>,
) -> Result<(File, DescriptorMetadata, Vec<u8>), Failure> {
    let file = work.run(RetainedDirectory::open_regular_cost(leaf), |_| {
        parent
            .open_regular(leaf)
            .map_err(|e| WorkFailure::Operation(opened(member, e)))
    })?;
    name(&file, leaf, member, work)?;
    let first = judge(&file, member, CoreTreeKind::Regular, work)?;
    let size = usize::try_from(first.metadata().size).unwrap_or(usize::MAX);
    if size == 0 || size > cap.min(MAX_FILE_BYTES) {
        return Err(WorkFailure::Operation(R::Size(member)));
    }
    let raw = opensip_platform::read_bounded_accounted(&file, size, work)
        .map_err(lift(|e| R::Read(member, e)))?;
    operation(raw.len() == size, (), R::Changed(member))?;
    let second = judge(&file, member, CoreTreeKind::Regular, work)?;
    same(second.metadata(), Some(first.metadata()), member)?;
    Ok((file, first.metadata().clone(), raw))
}
/// Open one child directory by its exact name and judge it (item 10).
fn judge_directory(
    parent: Option<usize>,
    directories: &mut Vec<HeldDirectory>,
    tree_root: &RetainedDirectory,
    leaf: &str,
    member: CoreMember,
    work: &mut WorkScope<'_>,
) -> Result<usize, Failure> {
    let held = work.run(PATH_COST, |_| Ok(leaf.to_owned()))?;
    let parent_directory = parent.map_or(tree_root, |i| &directories[i].directory);
    let directory = parent_directory
        .open_child_directory_if_present_accounted(OsStr::new(leaf), work)
        .map_err(lift(|e| opened(member, e)))?
        .ok_or(WorkFailure::Operation(R::Absent(member)))?;
    name(directory.as_file(), leaf, member, work)?;
    let capture = judge(directory.as_file(), member, CoreTreeKind::Directory, work)?;
    directories.push(HeldDirectory {
        parent,
        name: held,
        directory,
        metadata: capture.metadata().clone(),
        member,
    });
    Ok(directories.len() - 1)
}
/// A charged allowance for one parsed JSON value or projection built from
/// `bytes` of source. An allowance, not a proven allocator bound.
fn parse_cost(bytes: usize) -> WorkCost {
    WorkCost {
        objects: 1,
        edges: 1,
        bytes: bytes.saturating_mul(4),
    }
}

/// Law 463 item 2: exactly the anchor record, the inventory, payload and
/// index-0 root pairs, the later root-chain members, the revocation member
/// with its envelope, and (r9) the admitted catalog pair and every
/// component-manifest pair. Any other key is Missing.
struct MemoryStore(BTreeMap<(Collection, [u8; 32]), Arc<[u8]>>);
impl M::Store for MemoryStore {
    fn read(&mut self, _: &mut Budget, request: ReadRequest<'_>) -> Result<Arc<[u8]>, M::Error> {
        self.0
            .get(&(request.collection(), request.digest()))
            .cloned()
            .ok_or(M::Error::Missing)
    }
}
/// F8's rows, each a manifest path and its listed sha256.
struct Located {
    chain: Vec<(String, [u8; 32])>,
    revocation: (String, [u8; 32]),
    catalog: (String, [u8; 32]),
    manifests: Vec<(String, [u8; 32])>,
    envelopes: Vec<(String, [u8; 32])>,
}
/// F9's opens below the bootstrap directory: each subdirectory judged once,
/// every member within `MAX_MEMBER_BYTES` together.
struct MemberOpener {
    bootstrap: usize,
    memo: BTreeMap<String, usize>,
    remaining: usize,
    members: BTreeMap<String, Vec<u8>>,
}
impl MemberOpener {
    fn open(
        &mut self,
        path: &str,
        tree_root: &RetainedDirectory,
        directories: &mut Vec<HeldDirectory>,
        files: &mut Vec<HeldFile>,
        work: &mut WorkScope<'_>,
    ) -> Result<(), Failure> {
        if self.members.contains_key(path) {
            return Ok(());
        }
        let mut parent = self.bootstrap;
        let components: Vec<&str> = work.run(PATH_COST, |_| Ok(path.split('/').collect()))?;
        let (leaf, walk) = components
            .split_last()
            .expect("admitted path has a component");
        for (depth, component) in walk.iter().enumerate() {
            let prefix = work.run(PATH_COST, |_| Ok(walk[..=depth].join("/")))?;
            parent = match self.memo.get(&prefix) {
                Some(&index) => index,
                None => {
                    let index = judge_directory(
                        Some(parent),
                        directories,
                        tree_root,
                        component,
                        CoreMember::Bootstrap,
                        work,
                    )?;
                    self.memo.insert(prefix, index);
                    index
                }
            };
        }
        let (file, metadata, bytes) = judge_file(
            &directories[parent].directory,
            leaf,
            CoreMember::Member,
            self.remaining,
            work,
        )?;
        self.remaining -= bytes.len();
        files.push(HeldFile {
            parent: Some(parent),
            name: (*leaf).into(),
            file,
            metadata,
            member: CoreMember::Member,
        });
        self.members.insert(path.to_owned(), bytes);
        Ok(())
    }
}

/// One map node per stored key: the key, the shared pointer and tree links.
const STORE_ENTRY: WorkCost = WorkCost {
    objects: 1,
    edges: 0,
    bytes: 128,
};

/// Item 8: a release entry naming this closure refuses. Other kinds do not
/// apply to InitialCore; key entries were applied by the quorum re-filter.
fn refuse_revoked_release(entries: &[V], closure: &str) -> Result<(), InitialCoreRefusal> {
    let revoked = entries.iter().filter_map(object).any(|row| {
        row.get("subjectKind").and_then(string) == Some("release")
            && row.get("subject").and_then(string) == Some(closure)
    });
    if revoked {
        Err(R::ReleaseRevoked)
    } else {
        Ok(())
    }
}

/// Owner §1a step 3 for this process. Every step runs on the attempt's one
/// ledger; any refusal latches the attempt.
pub(crate) fn produce_initial_core(
    attempt: &mut InitialInstallationAttempt,
) -> Result<InitialCore, Failure> {
    produce_with(attempt, &EMBEDDED_CORE_RELEASE, COMPILED_PLATFORM, |work| {
        opensip_platform::observe_running_image(MAX_IMAGE_BYTES, work)
            .map(Image::Running)
            .map_err(lift(R::Image))
    })
}
/// F0 before any native call, then the running-image observation (F1).
fn produce_with(
    attempt: &mut InitialInstallationAttempt,
    release: &EmbeddedCoreRelease,
    platform: Option<&'static str>,
    observe: impl FnOnce(&mut WorkScope<'_>) -> Result<Image, Failure>,
) -> Result<InitialCore, Failure> {
    let lineage = attempt.lineage();
    attempt.run(|work| {
        let embedding = release.admit().map_err(|absent| {
            WorkFailure::Operation(match absent {
                EmbeddingAbsent::Root => R::EmbeddedRootAbsent,
                EmbeddingAbsent::Entrypoint => R::EmbeddedEntrypointAbsent,
                EmbeddingAbsent::Bootstrap => R::EmbeddedBootstrapAbsent,
            })
        })?;
        // The two split component vectors admit() made; an absent value
        // allocates nothing, so a development build charges only the lineage.
        work.charge(WorkCost {
            objects: 2,
            edges: 0,
            bytes: 2 * 32 * std::mem::size_of::<&str>(),
        })?;
        let platform = platform.ok_or(WorkFailure::Operation(R::PlatformUnavailable))?;
        let image = observe(work)?;
        produce_in(work, lineage, &embedding, platform, image)
    })
}

fn produce_in(
    work: &mut WorkScope<'_>,
    lineage: [u8; 16],
    embedding: &AdmittedEmbedding,
    platform: &'static str,
    image: Image,
) -> Result<InitialCore, Failure> {
    let entrypoint = embedding.entrypoint();
    // F2: the kernel path's leaf is the embedded entrypoint's last component.
    let leaf = *entrypoint.last().expect("admitted path has a component");
    operation(
        image.leaf().as_bytes() == leaf.as_bytes(),
        (),
        R::EntrypointName,
    )?;
    let matches = image
        .leaf_name_matches_accounted(work)
        .map_err(lift(R::Image))?;
    operation(matches, (), R::EntrypointName)?;
    // F3: the tree root is n-1 retained parents above the executable's
    // directory (index C); it is never `/` (index 0).
    let n = entrypoint.len();
    let c = image.parents().component_count();
    operation(n <= c, (), R::TreeRootBound)?;
    let root_index = c - (n - 1);
    let mut tree = Vec::new();
    let mut tree_root = None;
    image.parents().visit_directories(|i, directory| {
        if i < root_index {
            return Ok(());
        }
        if i > root_index {
            let expected = OsStr::new(entrypoint[i - root_index - 1]);
            let matches = opensip_platform::descriptor_name_matches_accounted(
                directory.as_file(),
                expected,
                work,
            )
            .map_err(lift(|e| R::Native(CoreMember::Tree, e)))?;
            operation(matches, (), R::EntrypointName)?;
        }
        let capture = judge(
            directory.as_file(),
            CoreMember::Tree,
            CoreTreeKind::Directory,
            work,
        )?;
        tree.push(capture.metadata().clone());
        if i == root_index {
            tree_root = Some(duplicate(directory, work)?);
        }
        Ok(())
    })?;
    let tree_root = tree_root.expect("index r is visited");
    // F4: the executable, on the image's own retained descriptor.
    let capture = image
        .capture_file_acl(work)
        .map_err(lift(|e| R::Acl(CoreMember::Executable, e)))?;
    let held = image.metadata();
    operation(
        capture.metadata().device == held.device && capture.metadata().inode == held.inode,
        (),
        R::Changed(CoreMember::Executable),
    )?;
    judged(&capture, CoreMember::Executable, CoreTreeKind::Regular)?;
    let executable = capture.metadata().clone();
    let mut files = Vec::new();
    let mut raw = Vec::new();
    // F5: the two fixed names under the tree root (item 1).
    for leaf in INVENTORY {
        let (file, metadata, bytes) = judge_file(
            &tree_root,
            leaf,
            CoreMember::Inventory,
            MAX_FILE_BYTES,
            work,
        )?;
        files.push(HeldFile {
            parent: None,
            name: leaf.into(),
            file,
            metadata,
            member: CoreMember::Inventory,
        });
        raw.push(bytes);
    }
    // F6: the embedded bootstrap directory, component by component.
    let mut directories: Vec<HeldDirectory> = Vec::new();
    let mut bootstrap = None;
    for component in embedding.bootstrap() {
        bootstrap = Some(judge_directory(
            bootstrap,
            &mut directories,
            &tree_root,
            component,
            CoreMember::Bootstrap,
            work,
        )?);
    }
    let bootstrap = bootstrap.expect("admitted path has a component");
    // F7: the fixed payload pair under the bootstrap directory.
    for leaf in PAYLOAD {
        let (file, metadata, bytes) = judge_file(
            &directories[bootstrap].directory,
            leaf,
            CoreMember::Payload,
            MAX_FILE_BYTES,
            work,
        )?;
        files.push(HeldFile {
            parent: Some(bootstrap),
            name: leaf.into(),
            file,
            metadata,
            member: CoreMember::Payload,
        });
        raw.push(bytes);
    }
    let [inventory, inventory_env, payload, payload_env]: [Vec<u8>; 4] =
        raw.try_into().expect("four fixed files");
    // F8: the locator. Nothing here is authenticated yet. (r9) It also takes
    // `members.catalog` and `members.manifests`.
    let located = work.run(parse_cost(payload.len()), |_| {
        let manifest = super::super::metadata::parse(&payload)
            .map_err(|_| WorkFailure::Operation(R::BootstrapLocator))?;
        Paths::admit(&manifest).map_err(|_| WorkFailure::Operation(R::BootstrapLocator))?;
        let m = object(&object(&manifest).expect("admitted")["members"]).expect("admitted");
        let row = |v: &V| {
            let row = object(v).expect("admitted");
            let path = string(&row["path"]).expect("admitted").to_owned();
            (
                path,
                decode_hex32(string(&row["sha256"]).expect("admitted")).expect("admitted"),
            )
        };
        let rows =
            |key: &str| -> Vec<_> { array(&m[key]).expect("admitted").iter().map(row).collect() };
        let chain = rows("rootChain");
        let envelopes = rows("envelopes");
        let manifests = rows("manifests");
        operation(
            chain.len() + 1 + manifests.len() + envelopes.len() <= MAX_MEMBERS,
            Located {
                chain,
                revocation: row(&m["revocation"]),
                catalog: row(&m["catalog"]),
                manifests,
                envelopes,
            },
            R::BootstrapLocator,
        )
    })?;
    let Located {
        chain,
        revocation,
        catalog,
        manifests,
        envelopes,
    } = located;
    // F9: each member by no-follow opens under the bootstrap directory; its
    // subdirectories are judged once each. The listed envelopes are all
    // loaded before any selection (item 9).
    let mut opener = MemberOpener {
        bootstrap,
        memo: BTreeMap::new(),
        remaining: MAX_MEMBER_BYTES,
        members: BTreeMap::new(),
    };
    for (path, _) in chain.iter().chain([&revocation]).chain(&envelopes) {
        opener.open(path, &tree_root, &mut directories, &mut files, work)?;
    }
    // Item 9 (r9): the listed envelopes pair one-to-one, by carrier stored
    // digest, with the root-chain bodies, the revocation body, every
    // component-manifest body, and the catalog body only when one listed
    // envelope's stored digest equals it. Which role signed is not judged.
    let mut stored = Vec::new();
    for (path, _) in &envelopes {
        let raw = &opener.members[path];
        stored.push(work.run(parse_cost(raw.len()), |_| {
            let value = super::super::metadata::parse(raw)
                .map_err(|_| WorkFailure::Operation(R::BootstrapEnvelopeSet))?;
            verified_envelopes::parse_carrier(&value)
                .map(|carrier| carrier.stored_digest())
                .map_err(|_| WorkFailure::Operation(R::BootstrapEnvelopeSet))
        })?);
    }
    let catalog_admitted = stored.contains(&catalog.1);
    let mut bodies: BTreeSet<[u8; 32]> = chain.iter().map(|(_, d)| *d).collect();
    bodies.insert(revocation.1);
    bodies.extend(manifests.iter().map(|(_, d)| *d));
    if catalog_admitted {
        bodies.insert(catalog.1);
    }
    let listed = chain.len() + 1 + manifests.len() + usize::from(catalog_admitted);
    operation(
        bodies.len() == listed && envelopes.len() == bodies.len(),
        (),
        R::BootstrapEnvelopeSet,
    )?;
    // Each body digest's envelope, by index into `envelopes`.
    let mut paired: BTreeMap<[u8; 32], usize> = BTreeMap::new();
    for (index, digest) in stored.iter().enumerate() {
        operation(bodies.remove(digest), (), R::BootstrapEnvelopeSet)?;
        paired.insert(*digest, index);
    }
    // The admitted catalog body counts toward the same member bound. Under the
    // bijection F8's bound already implies it; it is stated here.
    operation(
        listed + envelopes.len() <= MAX_MEMBERS,
        (),
        R::BootstrapLocator,
    )?;
    // F9 (r9): the component-manifest bodies, then the admitted catalog body,
    // by the same opens, custody judgment and byte bound. An unadmitted
    // catalog is never opened.
    let catalog = catalog_admitted.then_some(catalog);
    for (path, _) in manifests.iter().chain(&catalog) {
        opener.open(path, &tree_root, &mut directories, &mut files, work)?;
    }
    let MemberOpener { mut members, .. } = opener;
    // A retained pair is keyed as the store keys it: each body and its
    // envelope hash to their listed digests.
    for (path, digest) in manifests.iter().chain(&catalog).chain(
        manifests
            .iter()
            .chain(&catalog)
            .map(|(_, body)| &envelopes[paired[body]]),
    ) {
        operation(
            raw_sha256(&members[path]) == *digest,
            (),
            R::BootstrapEnvelopeSet,
        )?;
    }
    let index_zero = &members[&envelopes[paired[&chain[0].1]].0];
    let root_body = &members[&chain[0].0];
    // F11: the anchor record from the retained raw pairs (items 2 and 3).
    let closure = work.run(parse_cost(inventory.len()), |_| {
        Core::project_v3(&inventory, platform)
            .map(|p| p.core().closure().to_owned())
            .map_err(|e| WorkFailure::Operation(R::Inventory(e)))
    })?;
    let root = embedding.root();
    let record = work.run(parse_cost(PATH_COST.bytes), |_| {
        let int = |n: i128| V::Integer(JsonInteger::new(n).expect("bounded"));
        let reference = |raw: &[u8]| {
            V::Object(BTreeMap::from([
                ("bytes".into(), int(raw.len() as i128)),
                ("sha256".into(), V::String(digest_hex(&raw_sha256(raw)))),
            ]))
        };
        let pair = |body: &[u8], envelope: &[u8]| {
            V::Object(BTreeMap::from([
                ("body".into(), reference(body)),
                ("envelope".into(), reference(envelope)),
            ]))
        };
        let node = V::Object(BTreeMap::from([
            ("admissionSchema".into(), int(1)),
            (
                "binding".into(),
                V::Object(BTreeMap::from([
                    ("rootDigest".into(), V::String(digest_hex(&root.digest()))),
                    ("rootSchema".into(), int(root.schema().into())),
                    ("rootVersion".into(), int(root.version().into())),
                ])),
            ),
            ("bootstrapManifest".into(), pair(&payload, &payload_env)),
            ("coreClosure".into(), V::String(closure)),
            ("coreInventory".into(), pair(&inventory, &inventory_env)),
            ("kind".into(), V::String("anchor".into())),
            ("platform".into(), V::String(platform.into())),
            ("root".into(), pair(root_body, index_zero)),
        ]));
        let record = canonical_bytes(&node).map_err(|_| WorkFailure::Operation(R::Anchor))?;
        Ok((reference(&record), record))
    })?;
    let (anchor_ref, record) = record;
    // F10: the in-memory store, item 2 exactly. The r9 pairs share their
    // stored bytes with the retained documents.
    let mut store = MemoryStore(BTreeMap::new());
    let mut insert = |collection: Collection, raw: Vec<u8>, work: &mut WorkScope<'_>| {
        work.run(
            WorkCost {
                bytes: STORE_ENTRY.bytes + raw.len(),
                ..STORE_ENTRY
            },
            |_| {
                let raw: Arc<[u8]> = Arc::from(raw);
                store.0.insert((collection, raw_sha256(&raw)), raw.clone());
                Ok(raw)
            },
        )
    };
    insert(Collection::Records, record, work)?;
    for raw in [inventory, inventory_env, payload, payload_env] {
        insert(Collection::Objects, raw, work)?;
    }
    let mut retained: BTreeMap<String, Arc<[u8]>> = BTreeMap::new();
    let r9_paths = manifests
        .iter()
        .chain(&catalog)
        .map(|(path, body)| (path, &envelopes[paired[body]].0));
    // X4B-a: the revocation pair is retained beside the r9 pairs.
    let revocation_paths = (&revocation.0, &envelopes[paired[&revocation.1]].0);
    let r9: BTreeSet<&String> = r9_paths
        .clone()
        .chain([revocation_paths])
        .flat_map(|(b, e)| [b, e])
        .collect();
    for (path, _) in chain
        .iter()
        .chain([&revocation])
        .chain(&envelopes)
        .chain(&manifests)
        .chain(&catalog)
    {
        if let Some(raw) = members.remove(path) {
            let raw = insert(Collection::Objects, raw, work)?;
            if r9.contains(path) {
                retained.insert(path.clone(), raw);
            }
        }
    }
    // The retained pairs: one vector, and two path copies per pair; the
    // revocation pair is the one beside the vector.
    let pairs = manifests.len() + usize::from(catalog.is_some()) + 1;
    let documents = work.run(
        WorkCost {
            objects: 1 + 2 * pairs,
            edges: 0,
            bytes: pairs * (std::mem::size_of::<BootstrapPair>() + 2 * PATH_COST.bytes),
        },
        |_| {
            let document = |path: &String| DocumentBytes {
                path: path.clone(),
                sha256: raw_sha256(&retained[path]),
                raw: retained[path].clone(),
            };
            let mut pairs: Vec<BootstrapPair> = r9_paths
                .map(|(body, envelope)| BootstrapPair {
                    body: document(body),
                    envelope: document(envelope),
                })
                .collect();
            let catalog = catalog
                .is_some()
                .then(|| pairs.pop().expect("chained last"));
            Ok(BootstrapDocuments {
                catalog,
                manifests: pairs,
                revocation: BootstrapPair {
                    body: document(revocation_paths.0),
                    envelope: document(revocation_paths.1),
                },
            })
        },
    )?;
    drop(retained);
    // F12: TR-CORE, TR-BUNDLE and the embedded revocation (items 4, 5).
    let release = {
        let mut budget = Budget::borrowed(work);
        authenticate_embedded_release(&mut budget, &anchor_ref, &mut store)
    }
    .map_err(|e| WorkFailure::Operation(R::Release(e)))?;
    drop(store);
    let core = release.authentication().core();
    let inventory = core.inventory();
    // F13: the authenticated bootstrap directory is the embedded one.
    let directory = &object(inventory.inventory()).expect("admitted")["embeddedBootstrap"];
    let bootstrap_path = work.run(PATH_COST, |_| Ok(embedding.bootstrap().join("/")))?;
    operation(
        object(directory)
            .and_then(|d| d.get("directory"))
            .and_then(string)
            == Some(bootstrap_path.as_str()),
        (),
        R::BootstrapPath,
    )?;
    // F14: K and the flags of this platform's row (item 6).
    let members = core
        .release()
        .ok_or(WorkFailure::Operation(R::StateWriter))?;
    let (writer, flags) = (
        members.state_writer(),
        members.required_code_signing_flags(),
    );
    // F15: the row's entrypoint is the embedded one, and commits to the image.
    let entry_path = work.run(PATH_COST, |_| Ok(entrypoint.join("/")))?;
    let row = array(&object(inventory.inventory()).expect("admitted")["platforms"])
        .expect("admitted")
        .iter()
        .filter_map(object)
        .find(|row| row.get("platform").and_then(string) == Some(platform))
        .ok_or(WorkFailure::Operation(R::EntrypointRow))?;
    operation(
        row.get("entrypoint").and_then(string) == Some(entry_path.as_str()),
        (),
        R::EntrypointRow,
    )?;
    let committed = inventory
        .files()
        .get(platform)
        .and_then(|files| files.get(&entry_path))
        .and_then(object)
        .ok_or(WorkFailure::Operation(R::EntrypointRow))?;
    operation(
        committed.get("sha256").and_then(string) == Some(digest_hex(&image.sha256()).as_str())
            && committed.get("length").and_then(integer) == i64::try_from(image.length()).ok(),
        (),
        R::EntrypointBytes,
    )?;
    // F17: item 8 on the embedded revocation's entries.
    let entries =
        array(&object(release.revocation().envelope().payload()).expect("admitted")["entries"])
            .expect("admitted");
    refuse_revoked_release(entries, inventory.closure()).map_err(WorkFailure::Operation)?;
    // F18, F19.
    operation(image.status() & flags == flags, (), R::CodeSigningFlags)?;
    let state_writer = match writer {
        1 => StateWriter::Stage1,
        2 => StateWriter::Stage2,
        _ => return Err(WorkFailure::Operation(R::StateWriter)),
    };
    // F20, F21.
    let core = InitialCore {
        lineage,
        image,
        executable,
        root_index,
        tree,
        tree_root,
        directories,
        files,
        release,
        platform,
        state_writer,
        flags,
        bootstrap: documents,
    };
    core.recheck_in(work)?;
    Ok(core)
}

#[cfg(any(test, feature = "crash-matrix", feature = "scenario-fixtures"))]
#[cfg_attr(not(test), allow(dead_code, unused_imports))]
pub(super) mod tests {
    include!("initial_core_tests.rs");
}
