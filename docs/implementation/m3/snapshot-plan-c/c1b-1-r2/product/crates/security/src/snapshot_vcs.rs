// M3-C r8 item 4 (unit C1b-1; C1b plan r6): the snapshot's Git reads. The
// lending's own VCS subject (LD-C1B-1) names the repository: the innermost
// enclosing one, through its `RepositoryProof`, or, under the `NoRepository`
// proof, each D15 member of discovery's own record (LD-C1B-3, LD-C1B-5).
// For each, `HEAD` is resolved in its closed forms only (LD-C1B-2): `HEAD`
// itself, one loose ref reached segment by segment with no-follow opens, or
// `packed-refs`. Every object is opened from a retained descriptor and judged
// before any byte is read (LD-C1B-4), and every step is charged to the
// caller's ledger (LD-C1B-6). No Git object, index, log or environment is
// read; `dirty` is the sealer's constant, never computed here (LD-C1B-10).
use crate::custody::git_tracking::{
    self as git, Failure, INDEX_CAP, MAX_MEMBER_DEPTH, MemberCustody, MemberRefusal,
    RepositoryProof, TrackingRefusal,
};
use crate::custody::project_chain::{DiscoveryRoot, ProjectObject};
use crate::custody::workspace_declarations::MAX_MEMBERS;
use crate::discovery_export::AdmittedBoundaries;
use crate::snapshot_source::{SnapshotCustody, SnapshotRoot, VcsSubject, owned_record};
use opensip_platform::{RetainedDirectory, WorkCost, WorkFailure, WorkScope};
use std::fs::File;
use std::io;
use std::os::unix::ffi::OsStrExt;

/// A commit's object name: 40 lowercase hexadecimal digits. SHA-1 only,
/// because X2 refuses `extensions.*` (B-S2 LD-3).
#[derive(Clone, Copy, PartialEq, Eq)]
pub struct CommitId([u8; COMMIT_HEX]);
/// The object name's length.
pub const COMMIT_HEX: usize = 40;
impl CommitId {
    fn parse(raw: &[u8]) -> Option<Self> {
        let hex = |b: &u8| b.is_ascii_digit() || (b'a'..=b'f').contains(b);
        let mut id = [0u8; COMMIT_HEX];
        if raw.len() != COMMIT_HEX || !raw.iter().all(hex) {
            return None;
        }
        id.copy_from_slice(raw);
        Some(Self(id))
    }
    /// The 40 lowercase hexadecimal digits.
    pub fn as_str(&self) -> &str {
        std::str::from_utf8(&self.0).expect("hex digits are ASCII")
    }
}
impl std::fmt::Debug for CommitId {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.write_str(self.as_str())
    }
}

/// One admitted member's resolved `HEAD`, its path borrowed from
/// discovery's record.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct MemberCommit<'b> {
    path: &'b str,
    commit: CommitId,
}
impl<'b> MemberCommit<'b> {
    /// The member's root, relative to the project root (IDS `LogicalPath`).
    pub fn path(&self) -> &'b str {
        self.path
    }
    pub fn commit(&self) -> CommitId {
        self.commit
    }
}

/// What the VCS observation found (item 4; S4).
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum VcsObservation<'b> {
    /// No repository and no member: schema 2 `kind: none`.
    None,
    /// The innermost enclosing repository's `HEAD`: schema 2 `kind: git`.
    Git(CommitId),
    /// Each admitted member's `HEAD`, in the record's order: schema 3.
    Members(Vec<MemberCommit<'b>>),
    /// The lending carries no tracking observation: `VcsPending`.
    Unobserved,
}
impl VcsObservation<'_> {
    /// The canonical length of the `vcs-observation` record this
    /// observation seals into (C1b plan r6, R4-RF-1), `None` for
    /// `Unobserved`. Schema 2 is fixed: 154 bytes for `none` and 190 for
    /// `git` (B-S2's vectors). Schema 3 is 167 fixed bytes (the top level's
    /// keys and values, the single-digit `schemaVersion` and the 64-hex
    /// digest), 91 per member (its keys, 40-hex `commitId`, `true` and
    /// `"git"`) plus its path's escaped payload, and a comma between members.
    pub fn encoded_len(&self) -> Option<usize> {
        match self {
            Self::None => Some(154),
            Self::Git(_) => Some(190),
            Self::Members(members) => Some(
                members
                    .iter()
                    .map(|m| 91 + payload_len(m.path))
                    .sum::<usize>()
                    .saturating_add(167)
                    .saturating_add(members.len().saturating_sub(1)),
            ),
            Self::Unobserved => None,
        }
    }
}
/// A string's canonical payload, quotes excluded: 2 bytes for `"`, `\` and
/// each of `\b \f \n \r \t`, 6 for any other control below U+0020, raw
/// UTF-8 otherwise (identity `canonical.rs`, `Encoder::string`).
fn payload_len(text: &str) -> usize {
    text.chars()
        .map(|c| match c {
            '"' | '\\' | '\u{8}' | '\u{c}' | '\n' | '\r' | '\t' => 2,
            '\0'..='\u{1f}' => 6,
            c => c.len_utf8(),
        })
        .sum()
}

/// A member's refusal, with item 6b's subjects (`MemberRefusal`).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum MemberVcsRefusal {
    VcsUnsupported(&'static str),
    OutsideVolume,
}
impl MemberVcsRefusal {
    fn of(refusal: MemberRefusal) -> Self {
        match refusal {
            MemberRefusal::VcsUnsupported(reason) => Self::VcsUnsupported(reason),
            MemberRefusal::OutsideVolume => Self::OutsideVolume,
        }
    }
    pub fn subject(self) -> String {
        match self {
            Self::VcsUnsupported(reason) => MemberRefusal::VcsUnsupported(reason).subject(),
            Self::OutsideVolume => MemberRefusal::OutsideVolume.subject(),
        }
    }
}

/// Why the VCS observation refused (LD-C1B-8). Typed; the route is J2's.
#[derive(Debug)]
pub enum VcsRefusal {
    /// The enclosing repository outside the closed layout:
    /// `vcs-unsupported:<reason>`.
    Unsupported(&'static str),
    /// The member at `index` of the record's `memberRepositories`.
    Member {
        index: usize,
        refusal: MemberVcsRefusal,
    },
    /// Host I/O.
    Io(io::Error),
    /// A composition precondition failed (LD-C1B-3): never a refusal of
    /// the repository.
    Internal(&'static str),
}
impl VcsRefusal {
    /// The refusal's subject, X2's spelling; `None` for I/O and `Internal`.
    pub fn subject(&self) -> Option<String> {
        match self {
            Self::Unsupported(reason) => Some(format!("vcs-unsupported:{reason}")),
            Self::Member { refusal, .. } => Some(refusal.subject()),
            Self::Io(_) | Self::Internal(_) => None,
        }
    }
}
pub type VcsFailure = WorkFailure<VcsRefusal>;

/// The VCS observation of the lent root (item 4), on the caller's ledger.
/// `boundaries` is discovery's record for this very root (LD-C1B-3): its
/// `selectedRoot` must be the lent root's spelling, and a non-empty member
/// set needs the `NoRepository` subject. Either mismatch is `Internal`.
pub fn observe_vcs<'b>(
    root: &SnapshotRoot<'_>,
    custody: SnapshotCustody<'_>,
    boundaries: Option<&'b AdmittedBoundaries>,
    work: &mut WorkScope<'_>,
) -> Result<VcsObservation<'b>, VcsFailure> {
    let lent = root.lent();
    if let Some(record) = boundaries
        && record.selected_root().as_bytes() != lent.spelling().as_os_str().as_bytes()
    {
        return internal("cross-root-record");
    }
    let members: &'b [String] = boundaries.map_or(&[], AdmittedBoundaries::member_repositories);
    if members.len() > MAX_MEMBERS {
        return internal("members-over-limit");
    }
    let reader = Reader {
        lent,
        uid: custody.uid,
        custody: MemberCustody {
            trust_groups: custody.groups,
            premise: lent.premise(),
        },
    };
    match (root.vcs(), members.is_empty()) {
        (VcsSubject::Unobserved, true) => Ok(VcsObservation::Unobserved),
        (VcsSubject::NoRepository(_), true) => Ok(VcsObservation::None),
        (VcsSubject::Repository(proof), true) => reader
            .enclosing(proof, work)
            .map(VcsObservation::Git)
            .map_err(|failure| lift(failure, None)),
        (VcsSubject::NoRepository(proof), false) => {
            reader.members(proof.chain().root(), members, work)
        }
        (VcsSubject::Repository(_) | VcsSubject::Unobserved, false) => {
            internal("members-without-no-repository")
        }
    }
}

fn internal<T>(reason: &'static str) -> Result<T, VcsFailure> {
    Err(WorkFailure::Operation(VcsRefusal::Internal(reason)))
}
fn unsupported<T>(reason: &'static str) -> Result<T, Failure> {
    Err(WorkFailure::Operation(TrackingRefusal::VcsUnsupported(
        reason,
    )))
}
fn io_error<T>(error: io::Error) -> Result<T, Failure> {
    Err(WorkFailure::Operation(TrackingRefusal::Io(error)))
}
/// X2's failure as this observation's: an enclosing repository's reason, or
/// the member's projection of it.
fn lift(failure: Failure, member: Option<usize>) -> VcsFailure {
    let refusal = match failure {
        WorkFailure::Budget(budget) => return WorkFailure::Budget(budget),
        WorkFailure::Operation(TrackingRefusal::VcsUnsupported(reason)) => match member {
            None => VcsRefusal::Unsupported(reason),
            Some(index) => VcsRefusal::Member {
                index,
                refusal: MemberVcsRefusal::VcsUnsupported(reason),
            },
        },
        WorkFailure::Operation(TrackingRefusal::Io(error)) => VcsRefusal::Io(error),
        WorkFailure::Operation(TrackingRefusal::MarkerTracked) => {
            VcsRefusal::Internal("marker-tracked")
        }
    };
    WorkFailure::Operation(refusal)
}

/// macOS `ENAMETOOLONG`.
const ENAMETOOLONG: i32 = 63;
/// A component the platform refuses (`InvalidInput`, over its component
/// bound) or the kernel refuses as too long (C1b plan r6, LD-C1B-2).
fn name_refused(error: &io::Error) -> bool {
    error.kind() == io::ErrorKind::InvalidInput || error.raw_os_error() == Some(ENAMETOOLONG)
}

/// One Git file's refusal reasons, X2's spellings.
struct GitFile {
    name: &'static str,
    not_file: &'static str,
    custody: &'static str,
    oversized: &'static str,
}
const HEAD: GitFile = GitFile {
    name: "HEAD",
    not_file: "head-not-file",
    custody: "head-custody",
    oversized: "head-oversized",
};
const PACKED_REFS: GitFile = GitFile {
    name: "packed-refs",
    not_file: "packed-refs-not-file",
    custody: "packed-refs-custody",
    oversized: "packed-refs-oversized",
};
const LOOSE_REF: GitFile = GitFile {
    name: "",
    not_file: "loose-ref-not-file",
    custody: "loose-ref-custody",
    oversized: "loose-ref-oversized",
};

/// The charged parse of `len` bytes read (LD-C1B-6): no allocation beyond
/// the charged buffer.
fn parse_cost(len: usize) -> WorkCost {
    WorkCost {
        objects: 1,
        edges: 1,
        bytes: len,
    }
}

struct Reader<'r> {
    lent: &'r DiscoveryRoot<'r>,
    uid: u32,
    custody: MemberCustody<'r>,
}
impl Reader<'_> {
    /// The innermost enclosing repository (LD-C1B-1, LD-C1B-4): its `.git`
    /// reopened from the proof's chain directory, judged, and its metadata
    /// equal to X2's evidence sample.
    fn enclosing(
        &self,
        proof: &RepositoryProof<'_>,
        work: &mut WorkScope<'_>,
    ) -> Result<CommitId, Failure> {
        let dot_git = self.git_directory(proof.directory(), work)?;
        if git::snapshot_metadata(dot_git.as_file(), work)? != *proof.sample() {
            return unsupported("evidence-changed");
        }
        self.resolve(&dot_git, work)
    }

    /// Each admitted member (LD-C1B-5), in the record's order, reached from
    /// W, the `NoRepository` proof's own retained root.
    fn members<'b>(
        &self,
        w: &RetainedDirectory,
        members: &'b [String],
        work: &mut WorkScope<'_>,
    ) -> Result<VcsObservation<'b>, VcsFailure> {
        let device = git::snapshot_metadata(w.as_file(), work)
            .map_err(|failure| lift(failure, None))?
            .device;
        work.charge::<VcsRefusal>(owned_record(
            members
                .len()
                .saturating_mul(std::mem::size_of::<MemberCommit<'_>>()),
        ))?;
        let mut out = Vec::with_capacity(members.len());
        for (index, path) in members.iter().enumerate() {
            if !placement_path(path) {
                return internal("member-path");
            }
            match self
                .member(w, device, path, work)
                .map_err(|failure| lift(failure, Some(index)))?
            {
                Ok(commit) => out.push(MemberCommit { path, commit }),
                Err(refusal) => {
                    return Err(WorkFailure::Operation(VcsRefusal::Member {
                        index,
                        refusal: MemberVcsRefusal::of(refusal),
                    }));
                }
            }
        }
        Ok(VcsObservation::Members(out))
    }

    /// One member: reached from W (item 6b's placement), then its `.git`,
    /// on W's device, judged and resolved.
    fn member(
        &self,
        w: &RetainedDirectory,
        device: u64,
        path: &str,
        work: &mut WorkScope<'_>,
    ) -> Result<Result<CommitId, MemberRefusal>, Failure> {
        let directory = match git::reach_member(w, device, path, work)? {
            Ok(directory) => directory,
            Err(refusal) => return Ok(Err(refusal)),
        };
        let dot_git = self.git_directory(&directory, work)?;
        if git::snapshot_metadata(dot_git.as_file(), work)?.device != device {
            return Ok(Err(MemberRefusal::OutsideVolume));
        }
        self.resolve(&dot_git, work).map(Ok)
    }

    /// `parent/.git`, opened no-follow and judged as a directory on H's
    /// volume (X2's layout reasons).
    fn git_directory(
        &self,
        parent: &RetainedDirectory,
        work: &mut WorkScope<'_>,
    ) -> Result<RetainedDirectory, Failure> {
        let dot_git = match git::snapshot_open_directory(parent, ".git", work)? {
            Ok(dot_git) => dot_git,
            Err(error) if error.kind() == io::ErrorKind::NotFound => {
                return unsupported("evidence-changed");
            }
            Err(error) if git::snapshot_link_or_not_directory(&error) => {
                return unsupported("git-not-directory");
            }
            Err(error) => return io_error(error),
        };
        self.directory_custody(&dot_git, "repository-off-home-volume", "git-custody", work)?;
        Ok(dot_git)
    }

    fn directory_custody(
        &self,
        directory: &RetainedDirectory,
        off_volume: &'static str,
        reason: &'static str,
        work: &mut WorkScope<'_>,
    ) -> Result<(), Failure> {
        if !self
            .lent
            .is_home_filesystem(&git::snapshot_filesystem(directory.as_file(), work)?)
        {
            return unsupported(off_volume);
        }
        git::snapshot_judge(
            directory.as_file(),
            ProjectObject::Directory,
            self.uid,
            &self.custody,
            reason,
            work,
        )
    }

    /// One Git file under `directory`, judged before any byte is read and
    /// read under `INDEX_CAP`; `None` when it is absent.
    fn read_file(
        &self,
        directory: &RetainedDirectory,
        name: &str,
        reasons: &GitFile,
        work: &mut WorkScope<'_>,
    ) -> Result<Option<Vec<u8>>, Failure> {
        let file: File = match git::snapshot_open_file(directory, name, work)? {
            Ok(file) => file,
            Err(error) if error.kind() == io::ErrorKind::NotFound => return Ok(None),
            Err(error) if error.raw_os_error() == Some(ENAMETOOLONG) => {
                return unsupported("ref-name");
            }
            Err(error) if git::snapshot_link_or_not_directory(&error) => {
                return unsupported(reasons.not_file);
            }
            Err(error) => return io_error(error),
        };
        if !self
            .lent
            .is_home_filesystem(&git::snapshot_filesystem(&file, work)?)
        {
            return unsupported("evidence-off-home-volume");
        }
        git::snapshot_judge(
            &file,
            ProjectObject::ConfigurationFile,
            self.uid,
            &self.custody,
            reasons.custody,
            work,
        )?;
        let raw = git::snapshot_read(&file, INDEX_CAP, reasons.oversized, work)?;
        work.charge::<TrackingRefusal>(parse_cost(raw.len()))?;
        Ok(Some(raw))
    }

    /// `HEAD` in its closed forms (LD-C1B-2): detached, or one symbolic
    /// level through a loose ref, then `packed-refs`.
    fn resolve(
        &self,
        dot_git: &RetainedDirectory,
        work: &mut WorkScope<'_>,
    ) -> Result<CommitId, Failure> {
        let Some(head) = self.read_file(dot_git, HEAD.name, &HEAD, work)? else {
            return unsupported("head-missing");
        };
        let commit = match head_form(&head) {
            Err(reason) => return unsupported(reason),
            Ok(Head::Detached(commit)) => commit,
            Ok(Head::Symbolic(target)) => match self.loose(dot_git, target, work)? {
                Some(commit) => commit,
                None => self.packed(dot_git, target, work)?,
            },
        };
        // The retained commit (LD-C1B-6).
        work.charge::<TrackingRefusal>(owned_record(COMMIT_HEX))?;
        Ok(commit)
    }

    /// The loose ref, reached segment by segment from `.git` by no-follow
    /// opens, each directory judged; only the current directory is held.
    /// `None` when any segment is absent: `packed-refs` decides.
    fn loose(
        &self,
        dot_git: &RetainedDirectory,
        target: &str,
        work: &mut WorkScope<'_>,
    ) -> Result<Option<CommitId>, Failure> {
        let (directories, leaf) = target.rsplit_once('/').expect("a target begins refs/");
        let mut current: Option<RetainedDirectory> = None;
        for segment in directories.split('/') {
            let parent = current.as_ref().unwrap_or(dot_git);
            let child = match git::snapshot_open_directory(parent, segment, work)? {
                Ok(child) => child,
                Err(error) if error.kind() == io::ErrorKind::NotFound => return Ok(None),
                Err(error) if name_refused(&error) => return unsupported("ref-name"),
                Err(error) if git::snapshot_link_or_not_directory(&error) => {
                    return unsupported("ref-not-directory");
                }
                Err(error) => return io_error(error),
            };
            self.directory_custody(&child, "evidence-off-home-volume", "ref-custody", work)?;
            current = Some(child);
        }
        let parent = current.as_ref().unwrap_or(dot_git);
        let Some(raw) = self.read_file(parent, leaf, &LOOSE_REF, work)? else {
            return Ok(None);
        };
        if raw.len() == COMMIT_HEX + 1
            && raw[COMMIT_HEX] == b'\n'
            && let Some(commit) = CommitId::parse(&raw[..COMMIT_HEX])
        {
            return Ok(Some(commit));
        }
        if raw.starts_with(b"ref:") {
            return unsupported("symbolic-ref-chain");
        }
        unsupported("loose-ref-malformed")
    }

    /// `packed-refs` (LD-C1B-2): absent, or without the target, is an
    /// unborn `HEAD`.
    fn packed(
        &self,
        dot_git: &RetainedDirectory,
        target: &str,
        work: &mut WorkScope<'_>,
    ) -> Result<CommitId, Failure> {
        let Some(raw) = self.read_file(dot_git, PACKED_REFS.name, &PACKED_REFS, work)? else {
            return unsupported("unborn-head");
        };
        match packed_lookup(&raw, target.as_bytes()) {
            Ok(Some(commit)) => Ok(commit),
            Ok(None) => unsupported("unborn-head"),
            Err(reason) => unsupported(reason),
        }
    }
}

/// A member path as placement admitted it (`MemberPath::new`'s rule),
/// checked in place: relative, canonical and at most 256 segments.
fn placement_path(path: &str) -> bool {
    !path.is_empty()
        && path.split('/').count() <= MAX_MEMBER_DEPTH
        && path
            .split('/')
            .all(|s| !s.is_empty() && s != "." && s != ".." && !s.contains('\0'))
}

enum Head<'h> {
    Detached(CommitId),
    Symbolic(&'h str),
}
/// `HEAD`'s two closed forms: `<40 lowercase hex>\n`, or `ref: refs/<name>\n`
/// with a name in the ref grammar.
fn head_form(raw: &[u8]) -> Result<Head<'_>, &'static str> {
    if raw.len() == COMMIT_HEX + 1
        && raw[COMMIT_HEX] == b'\n'
        && let Some(commit) = CommitId::parse(&raw[..COMMIT_HEX])
    {
        return Ok(Head::Detached(commit));
    }
    let Some(target) = raw
        .strip_prefix(b"ref: ")
        .and_then(|rest| rest.strip_suffix(b"\n"))
        .filter(|target| target.starts_with(b"refs/"))
    else {
        return Err("head-malformed");
    };
    if !ref_name(target) {
        return Err("ref-name");
    }
    std::str::from_utf8(target)
        .map(Head::Symbolic)
        .map_err(|_| "ref-name")
}

/// The ref-name grammar (LD-C1B-2): a closed subset of `git-check-ref-format`.
/// The name begins `refs/` and is UTF-8. It has no `..`, no trailing `.`,
/// no component beginning with `.` or ending `.lock`, no byte below 0x20,
/// no DEL, no space, none of `~ ^ : ? * [ \`, no `@{`, is not `@`, and has
/// no empty component.
fn ref_name(name: &[u8]) -> bool {
    std::str::from_utf8(name).is_ok()
        && name.starts_with(b"refs/")
        && name != b"@"
        && !name.windows(2).any(|w| w == b".." || w == b"@{")
        && !name.ends_with(b".")
        && name
            .iter()
            .all(|&b| b > b' ' && b != 0x7f && !b"~^:?*[\\".contains(&b))
        && name
            .split(|b| *b == b'/')
            .all(|c| !c.is_empty() && !c.starts_with(b".") && !c.ends_with(b".lock"))
}

/// `packed-refs` (LD-C1B-2): an optional first line `# pack-refs with:` and
/// its traits, then `<40 hex> <refname>` lines, each optionally followed by
/// one `^<40 hex>` peel line; every line ends in LF. Names are in strictly
/// ascending byte order, as Git writes them (its `sorted` trait): that
/// refuses a duplicate with no per-line allocation (LD-C1B-6). Any other
/// line, an out-of-order or duplicate name, or an orphan peel refuses
/// `packed-refs-malformed`; a name outside the grammar refuses `ref-name`.
fn packed_lookup(raw: &[u8], target: &[u8]) -> Result<Option<CommitId>, &'static str> {
    const MALFORMED: &str = "packed-refs-malformed";
    let mut found = None;
    let mut previous: Option<&[u8]> = None;
    let mut peelable = false;
    let mut rest = raw;
    let mut first = true;
    while !rest.is_empty() {
        let Some(end) = rest.iter().position(|b| *b == b'\n') else {
            return Err(MALFORMED);
        };
        let line = &rest[..end];
        rest = &rest[end + 1..];
        if std::mem::replace(&mut first, false) && line.starts_with(b"# pack-refs with:") {
            if !line.iter().all(|b| (b' '..=b'~').contains(b)) {
                return Err(MALFORMED);
            }
            continue;
        }
        if let Some(peel) = line.strip_prefix(b"^") {
            if !std::mem::replace(&mut peelable, false) || CommitId::parse(peel).is_none() {
                return Err(MALFORMED);
            }
            continue;
        }
        if line.len() <= COMMIT_HEX + 1 || line[COMMIT_HEX] != b' ' {
            return Err(MALFORMED);
        }
        let Some(commit) = CommitId::parse(&line[..COMMIT_HEX]) else {
            return Err(MALFORMED);
        };
        let name = &line[COMMIT_HEX + 1..];
        if !ref_name(name) {
            return Err("ref-name");
        }
        if previous.is_some_and(|p| p >= name) {
            return Err(MALFORMED);
        }
        if name == target {
            found = Some(commit);
        }
        previous = Some(name);
        peelable = true;
    }
    Ok(found)
}

#[cfg(test)]
mod tests {
    include!("snapshot_vcs_tests.rs");
}
