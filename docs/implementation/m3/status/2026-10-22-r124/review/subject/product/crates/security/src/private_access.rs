//! Private-descendant access evidence over one already captured ACL sample.
//! A missing attribute and a NOACL sentinel stay unavailable. Neither is an
//! empty ACL, and neither result is creator authority or a profile qualification.
use opensip_platform::{
    CapturedAclEntry, CapturedAclPrincipal, CapturedAclState, DescriptorAclCapture,
    DescriptorMetadata,
};

const TYPE_MASK: u32 = 0o170000;
const DIRECTORY: u32 = 0o040000;
const REGULAR: u32 = 0o100000;
pub(crate) const ACE_KIND_MASK: u32 = 0xf;
pub(crate) const ACE_PERMIT: u32 = 1;
pub(crate) const ACE_DENY: u32 = 2;
/// Kind plus the inherit and audit flag bits defined by the macOS SDK.
pub(crate) const KNOWN_ACE_FLAGS: u32 =
    ACE_KIND_MASK | (1 << 4) | (1 << 5) | (1 << 6) | (1 << 7) | (1 << 8) | (1 << 9) | (1 << 10);

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum PrivateObjectKind {
    Directory,
    RegularFile,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum PrivateAccessRefusal {
    /// The sample omitted the ACL attribute. That is not an empty ACL.
    AclNotReturned,
    /// The sample carried the NOACL sentinel. Support is still unqualified.
    AclSentinelUnqualified,
    /// `Entries(n)` did not have exactly n readable entries.
    InconsistentCapture,
    ForeignOwner,
    /// Permission bits are not exactly `0700` for a directory or `0600` for a file.
    ModeShape,
    /// A regular file is not a single link.
    LinkCount,
    /// An allow ACE grants any right to someone other than the invoking user.
    ForeignAclAccess,
    UnknownAceKind,
    UnknownAceFlags,
}

/// Read `acl_state` before any entry. The state fixes the entry count, and
/// `entry` only returns entries, so omission cannot become privacy. Entries
/// are judged in place; nothing is copied outside the capture.
fn judge_private_descendant(
    kind: PrivateObjectKind,
    invoking_uid: u32,
    metadata: &DescriptorMetadata,
    state: CapturedAclState,
    entry: impl Fn(usize) -> Option<CapturedAclEntry>,
) -> Result<(), PrivateAccessRefusal> {
    let count = match state {
        CapturedAclState::NotReturned => return Err(PrivateAccessRefusal::AclNotReturned),
        CapturedAclState::NoAclSentinel => {
            return Err(PrivateAccessRefusal::AclSentinelUnqualified);
        }
        CapturedAclState::Entries(count) => count,
    };
    if (0..count).any(|index| entry(index).is_none()) {
        return Err(PrivateAccessRefusal::InconsistentCapture);
    }
    private_shape(kind, invoking_uid, metadata)?;
    for index in 0..count {
        let entry = entry(index).ok_or(PrivateAccessRefusal::InconsistentCapture)?;
        judge_ace(invoking_uid, &entry)?;
    }
    Ok(())
}

/// Test form over a supplied slice. A slice whose length differs from a
/// present state's count is inconsistent. Production uses the capture form.
#[cfg(test)]
fn assess_private_descendant(
    kind: PrivateObjectKind,
    invoking_uid: u32,
    metadata: &DescriptorMetadata,
    state: CapturedAclState,
    entries: &[CapturedAclEntry],
) -> Result<(), PrivateAccessRefusal> {
    if let CapturedAclState::Entries(count) = state
        && entries.len() != count
    {
        return Err(PrivateAccessRefusal::InconsistentCapture);
    }
    judge_private_descendant(kind, invoking_uid, metadata, state, |index| {
        entries.get(index).copied()
    })
}

fn private_shape(
    kind: PrivateObjectKind,
    invoking_uid: u32,
    metadata: &DescriptorMetadata,
) -> Result<(), PrivateAccessRefusal> {
    if metadata.uid != invoking_uid {
        return Err(PrivateAccessRefusal::ForeignOwner);
    }
    let file_type = metadata.mode & TYPE_MASK;
    let permissions = metadata.mode & 0o7777;
    match kind {
        PrivateObjectKind::Directory => {
            if file_type != DIRECTORY || permissions != 0o700 {
                return Err(PrivateAccessRefusal::ModeShape);
            }
        }
        PrivateObjectKind::RegularFile => {
            if file_type != REGULAR || permissions != 0o600 {
                return Err(PrivateAccessRefusal::ModeShape);
            }
            if metadata.links != 1 {
                return Err(PrivateAccessRefusal::LinkCount);
            }
        }
    }
    Ok(())
}

/// When the sample omitted the ACL and the object already has the private
/// shape, append one zero-rights owner allow and sample again. An existing
/// ACL is left unchanged and judged as it stands. If the append succeeds and
/// the later sample or predicate fails, that zero-rights allow remains. This
/// does not create the file and does not decide creator authority.
#[cfg(target_os = "macos")]
pub(crate) fn prepare_fresh_private_sample(
    kind: PrivateObjectKind,
    invoking_uid: u32,
    file: &std::fs::File,
    work: &mut opensip_platform::WorkScope<'_>,
) -> Result<
    opensip_platform::DescriptorAclCapture,
    opensip_platform::WorkFailure<PreparePrivateError>,
> {
    let follow = opensip_platform::descriptor_acl_capture_cost()
        .checked_add(opensip_platform::append_owner_zero_allow_cost())
        .and_then(|sum| sum.checked_add(opensip_platform::descriptor_acl_capture_cost()))
        .ok_or(opensip_platform::WorkFailure::Budget(
            opensip_platform::WorkBudgetError::Arithmetic,
        ))?;
    work.effect(opensip_platform::WorkCost::default(), follow, |post| {
        prepare_fresh_private_sample_reserved(kind, invoking_uid, file, post)
    })
}

/// One `openat` and one mode-setting call for a new regular file. This is an
/// outer allowance, not the later ACL sample or append.
#[cfg(target_os = "macos")]
fn create_private_regular_file_cost() -> opensip_platform::WorkCost {
    opensip_platform::WorkCost {
        objects: 1,
        edges: 2,
        bytes: 0,
    }
}

/// One `mkdirat`, one `openat`, one status read, one directory scan, and one
/// mode-setting call for a new directory.
#[cfg(target_os = "macos")]
fn create_private_directory_cost() -> opensip_platform::WorkCost {
    opensip_platform::WorkCost {
        objects: 1,
        edges: 5,
        bytes: 0,
    }
}

/// Create one new regular file at `parent`/`name` with mode `0600`, then
/// prepare its ACL. The ledger reserves the create and both samples and the
/// append before the file is created. `name` is a single component. A later
/// refusal can leave that file behind. This does not admit the parent, does
/// not create a directory, and is not the installation creator.
#[cfg(target_os = "macos")]
pub(crate) fn create_private_regular_file(
    parent: &opensip_platform::RetainedDirectory,
    name: &str,
    invoking_uid: u32,
    work: &mut opensip_platform::WorkScope<'_>,
) -> Result<
    (std::fs::File, opensip_platform::DescriptorAclCapture),
    opensip_platform::WorkFailure<PreparePrivateError>,
> {
    use opensip_platform::WorkFailure;
    reject_private_name(name)?;
    let follow = opensip_platform::descriptor_acl_capture_cost()
        .checked_add(opensip_platform::append_owner_zero_allow_cost())
        .and_then(|sum| sum.checked_add(opensip_platform::descriptor_acl_capture_cost()))
        .ok_or(WorkFailure::Budget(
            opensip_platform::WorkBudgetError::Arithmetic,
        ))?;
    work.effect(create_private_regular_file_cost(), follow, |post| {
        let file = parent
            .create_exclusive_regular(name)
            .map_err(|error| WorkFailure::Operation(PreparePrivateError::Create(error)))?;
        let sample = prepare_fresh_private_sample_reserved(
            PrivateObjectKind::RegularFile,
            invoking_uid,
            &file,
            post,
        )?;
        Ok((file, sample))
    })
}

/// Create one new directory at `parent`/`name` with mode `0700`, then prepare
/// its ACL. The same reservation rules as a private file apply. This does not
/// admit the parent and is not the installation creator.
#[cfg(target_os = "macos")]
pub(crate) fn create_private_directory(
    parent: &opensip_platform::RetainedDirectory,
    name: &str,
    invoking_uid: u32,
    work: &mut opensip_platform::WorkScope<'_>,
) -> Result<
    (std::fs::File, opensip_platform::DescriptorAclCapture),
    opensip_platform::WorkFailure<PreparePrivateError>,
> {
    use opensip_platform::WorkFailure;
    reject_private_name(name)?;
    let follow = opensip_platform::descriptor_acl_capture_cost()
        .checked_add(opensip_platform::append_owner_zero_allow_cost())
        .and_then(|sum| sum.checked_add(opensip_platform::descriptor_acl_capture_cost()))
        .ok_or(WorkFailure::Budget(
            opensip_platform::WorkBudgetError::Arithmetic,
        ))?;
    work.effect(create_private_directory_cost(), follow, |post| {
        let directory = parent
            .create_exclusive_directory(name)
            .map_err(|error| WorkFailure::Operation(PreparePrivateError::Create(error)))?;
        let sample = prepare_fresh_private_sample_reserved(
            PrivateObjectKind::Directory,
            invoking_uid,
            &directory,
            post,
        )?;
        Ok((directory, sample))
    })
}

/// Judge an existing directory object. An omitted ACL is a refusal, not
/// privacy. Contents, path resolution, and parent admission are not judged.
/// This does not create the directory or append an ACL.
#[cfg(target_os = "macos")]
pub(crate) fn observe_private_directory(
    directory: &std::fs::File,
    invoking_uid: u32,
    work: &mut opensip_platform::WorkScope<'_>,
) -> Result<
    opensip_platform::DescriptorAclCapture,
    opensip_platform::WorkFailure<PreparePrivateError>,
> {
    use opensip_platform::{WorkFailure, capture_descriptor_acl_accounted};
    let sample = capture_descriptor_acl_accounted(directory, work).map_err(lift_capture)?;
    assess_private_descendant_capture(PrivateObjectKind::Directory, invoking_uid, &sample)
        .map_err(|error| WorkFailure::Operation(PreparePrivateError::Access(error)))?;
    Ok(sample)
}

/// Create one private file inside a directory that observes as private.
/// The parent is judged first. A refusal creates nothing.
#[cfg(target_os = "macos")]
pub(crate) fn create_private_file_in_observed_directory(
    parent: &opensip_platform::RetainedDirectory,
    name: &str,
    invoking_uid: u32,
    work: &mut opensip_platform::WorkScope<'_>,
) -> Result<
    (std::fs::File, opensip_platform::DescriptorAclCapture),
    opensip_platform::WorkFailure<PreparePrivateError>,
> {
    reject_private_name(name)?;
    observe_private_directory(parent.as_file(), invoking_uid, work)?;
    create_private_regular_file(parent, name, invoking_uid, work)
}

/// `prepare_fresh_private_sample`, spending from an existing reservation:
/// the creator's `OpenSIP` step reserves it before `mkdirat` (law 465 item 6).
#[cfg(target_os = "macos")]
pub(crate) fn prepare_fresh_private_sample_reserved(
    kind: PrivateObjectKind,
    invoking_uid: u32,
    file: &std::fs::File,
    post: &mut opensip_platform::ReservedPostchecks<'_>,
) -> Result<
    opensip_platform::DescriptorAclCapture,
    opensip_platform::WorkFailure<PreparePrivateError>,
> {
    use opensip_platform::{
        CapturedAclState, WorkFailure, append_owner_zero_allow_reserved,
        capture_descriptor_acl_reserved,
    };
    let first = capture_descriptor_acl_reserved(file, post).map_err(lift_capture)?;
    if first.acl_state() == CapturedAclState::NotReturned {
        private_shape(kind, invoking_uid, first.metadata())
            .map_err(|error| WorkFailure::Operation(PreparePrivateError::Access(error)))?;
        append_owner_zero_allow_reserved(file, post).map_err(lift_append)?;
    }
    let sample = if first.acl_state() == CapturedAclState::NotReturned {
        capture_descriptor_acl_reserved(file, post).map_err(lift_capture)?
    } else {
        first
    };
    assess_private_descendant_capture(kind, invoking_uid, &sample)
        .map_err(|error| WorkFailure::Operation(PreparePrivateError::Access(error)))?;
    Ok(sample)
}

#[cfg(target_os = "macos")]
fn reject_private_name(
    name: &str,
) -> Result<(), opensip_platform::WorkFailure<PreparePrivateError>> {
    if name.is_empty() || name == "." || name == ".." || name.contains(['/', '\\', '\0']) {
        Err(opensip_platform::WorkFailure::Operation(
            PreparePrivateError::Name,
        ))
    } else {
        Ok(())
    }
}

#[cfg(target_os = "macos")]
fn lift_capture(
    error: opensip_platform::WorkFailure<opensip_platform::DescriptorAclCaptureError>,
) -> opensip_platform::WorkFailure<PreparePrivateError> {
    match error {
        opensip_platform::WorkFailure::Budget(budget) => {
            opensip_platform::WorkFailure::Budget(budget)
        }
        opensip_platform::WorkFailure::Operation(error) => {
            opensip_platform::WorkFailure::Operation(PreparePrivateError::Capture(
                opensip_platform::WorkFailure::Operation(error),
            ))
        }
    }
}

#[cfg(target_os = "macos")]
fn lift_append(
    error: opensip_platform::WorkFailure<std::io::Error>,
) -> opensip_platform::WorkFailure<PreparePrivateError> {
    match error {
        opensip_platform::WorkFailure::Budget(budget) => {
            opensip_platform::WorkFailure::Budget(budget)
        }
        opensip_platform::WorkFailure::Operation(error) => {
            opensip_platform::WorkFailure::Operation(PreparePrivateError::Append(
                opensip_platform::WorkFailure::Operation(error),
            ))
        }
    }
}

#[derive(Debug)]
pub(crate) enum PreparePrivateError {
    Capture(opensip_platform::WorkFailure<opensip_platform::DescriptorAclCaptureError>),
    Append(opensip_platform::WorkFailure<std::io::Error>),
    Create(std::io::Error),
    Name,
    Access(PrivateAccessRefusal),
}
impl From<opensip_platform::WorkFailure<opensip_platform::DescriptorAclCaptureError>>
    for PreparePrivateError
{
    fn from(
        error: opensip_platform::WorkFailure<opensip_platform::DescriptorAclCaptureError>,
    ) -> Self {
        Self::Capture(error)
    }
}
impl From<opensip_platform::WorkFailure<std::io::Error>> for PreparePrivateError {
    fn from(error: opensip_platform::WorkFailure<std::io::Error>) -> Self {
        Self::Append(error)
    }
}
impl From<PrivateAccessRefusal> for PreparePrivateError {
    fn from(error: PrivateAccessRefusal) -> Self {
        Self::Access(error)
    }
}

pub(crate) fn assess_private_descendant_capture(
    kind: PrivateObjectKind,
    invoking_uid: u32,
    capture: &DescriptorAclCapture,
) -> Result<(), PrivateAccessRefusal> {
    judge_private_descendant(
        kind,
        invoking_uid,
        capture.metadata(),
        capture.acl_state(),
        |index| capture.entry(index),
    )
}

fn judge_ace(invoking_uid: u32, entry: &CapturedAclEntry) -> Result<(), PrivateAccessRefusal> {
    if entry.flags & !KNOWN_ACE_FLAGS != 0 {
        return Err(PrivateAccessRefusal::UnknownAceFlags);
    }
    match entry.flags & ACE_KIND_MASK {
        ACE_DENY => Ok(()),
        ACE_PERMIT if entry.rights == 0 => Ok(()),
        ACE_PERMIT => match entry.principal {
            CapturedAclPrincipal::User(uid) if uid == invoking_uid => Ok(()),
            _ => Err(PrivateAccessRefusal::ForeignAclAccess),
        },
        _ => Err(PrivateAccessRefusal::UnknownAceKind),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn metadata(kind: PrivateObjectKind, uid: u32) -> DescriptorMetadata {
        DescriptorMetadata {
            device: 1,
            inode: 2,
            mode: match kind {
                PrivateObjectKind::Directory => DIRECTORY | 0o700,
                PrivateObjectKind::RegularFile => REGULAR | 0o600,
            },
            uid,
            gid: 3,
            links: 1,
            size: 0,
            modified: (0, 0),
            changed: (0, 0),
            flags: 0,
        }
    }

    fn allow(principal: CapturedAclPrincipal, rights: u32, flags: u32) -> CapturedAclEntry {
        CapturedAclEntry {
            flags: ACE_PERMIT | flags,
            rights,
            principal,
        }
    }

    #[test]
    fn omitted_and_sentinel_states_ignore_an_empty_entry_slice() {
        let metadata = metadata(PrivateObjectKind::Directory, 10);
        for state in [
            CapturedAclState::NotReturned,
            CapturedAclState::NoAclSentinel,
        ] {
            let result =
                assess_private_descendant(PrivateObjectKind::Directory, 10, &metadata, state, &[]);
            let want = match state {
                CapturedAclState::NotReturned => PrivateAccessRefusal::AclNotReturned,
                CapturedAclState::NoAclSentinel => PrivateAccessRefusal::AclSentinelUnqualified,
                CapturedAclState::Entries(_) => unreachable!(),
            };
            assert_eq!(result, Err(want));
        }
    }

    #[test]
    fn omitted_state_is_not_overridden_by_a_supplied_foreign_allow() {
        let metadata = metadata(PrivateObjectKind::RegularFile, 10);
        let foreign = allow(CapturedAclPrincipal::Group(9), 1 << 1, 0);
        assert_eq!(
            assess_private_descendant(
                PrivateObjectKind::RegularFile,
                10,
                &metadata,
                CapturedAclState::NotReturned,
                &[foreign],
            ),
            Err(PrivateAccessRefusal::AclNotReturned)
        );
    }

    #[test]
    fn present_empty_acl_accepts_exact_private_mode_and_owner() {
        for kind in [PrivateObjectKind::Directory, PrivateObjectKind::RegularFile] {
            let metadata = metadata(kind, 10);
            assert_eq!(
                assess_private_descendant(kind, 10, &metadata, CapturedAclState::Entries(0), &[]),
                Ok(())
            );
        }
    }

    #[test]
    fn group_or_other_mode_and_wrong_owner_refuse_after_a_present_acl() {
        let mut directory = metadata(PrivateObjectKind::Directory, 10);
        directory.mode = DIRECTORY | 0o750;
        assert_eq!(
            assess_private_descendant(
                PrivateObjectKind::Directory,
                10,
                &directory,
                CapturedAclState::Entries(0),
                &[],
            ),
            Err(PrivateAccessRefusal::ModeShape)
        );
        for permissions in [0o4600, 0o2700, 0o1700, 0o500] {
            directory.mode = DIRECTORY | permissions;
            assert_eq!(
                assess_private_descendant(
                    PrivateObjectKind::Directory,
                    10,
                    &directory,
                    CapturedAclState::Entries(0),
                    &[],
                ),
                Err(PrivateAccessRefusal::ModeShape)
            );
        }
        directory.mode = DIRECTORY | 0o705;
        assert_eq!(
            assess_private_descendant(
                PrivateObjectKind::Directory,
                10,
                &directory,
                CapturedAclState::Entries(0),
                &[],
            ),
            Err(PrivateAccessRefusal::ModeShape)
        );
        let mut file = metadata(PrivateObjectKind::RegularFile, 10);
        file.links = 2;
        assert_eq!(
            assess_private_descendant(
                PrivateObjectKind::RegularFile,
                10,
                &file,
                CapturedAclState::Entries(0),
                &[],
            ),
            Err(PrivateAccessRefusal::LinkCount)
        );
        assert_eq!(
            assess_private_descendant(
                PrivateObjectKind::Directory,
                11,
                &metadata(PrivateObjectKind::Directory, 10),
                CapturedAclState::Entries(0),
                &[],
            ),
            Err(PrivateAccessRefusal::ForeignOwner)
        );
        assert_eq!(
            assess_private_descendant(
                PrivateObjectKind::RegularFile,
                10,
                &metadata(PrivateObjectKind::Directory, 10),
                CapturedAclState::Entries(0),
                &[],
            ),
            Err(PrivateAccessRefusal::ModeShape)
        );
        assert_eq!(
            assess_private_descendant(
                PrivateObjectKind::Directory,
                10,
                &metadata(PrivateObjectKind::RegularFile, 10),
                CapturedAclState::Entries(0),
                &[],
            ),
            Err(PrivateAccessRefusal::ModeShape)
        );
    }

    #[test]
    fn foreign_allow_rights_refuse_and_deny_or_invoking_user_allow_do_not() {
        let metadata = metadata(PrivateObjectKind::Directory, 10);
        let read = 1 << 1;
        let cases = [
            (
                allow(CapturedAclPrincipal::User(99), read, 0),
                Err(PrivateAccessRefusal::ForeignAclAccess),
            ),
            (
                allow(CapturedAclPrincipal::Group(4), read, 0),
                Err(PrivateAccessRefusal::ForeignAclAccess),
            ),
            (
                allow(CapturedAclPrincipal::Unresolved, read, 0),
                Err(PrivateAccessRefusal::ForeignAclAccess),
            ),
            (
                allow(CapturedAclPrincipal::Group(4), read, 1 << 8),
                Err(PrivateAccessRefusal::ForeignAclAccess),
            ),
            (allow(CapturedAclPrincipal::User(10), read, 0), Ok(())),
            (allow(CapturedAclPrincipal::Group(4), 0, 0), Ok(())),
            (
                CapturedAclEntry {
                    flags: ACE_DENY,
                    rights: read,
                    principal: CapturedAclPrincipal::Group(4),
                },
                Ok(()),
            ),
            (allow(CapturedAclPrincipal::User(10), 1 << 31, 0), Ok(())),
            (
                CapturedAclEntry {
                    flags: 3,
                    rights: read,
                    principal: CapturedAclPrincipal::User(10),
                },
                Err(PrivateAccessRefusal::UnknownAceKind),
            ),
            (
                allow(CapturedAclPrincipal::User(10), read, 1 << 11),
                Err(PrivateAccessRefusal::UnknownAceFlags),
            ),
        ];
        for (entry, want) in cases {
            assert_eq!(
                assess_private_descendant(
                    PrivateObjectKind::Directory,
                    10,
                    &metadata,
                    CapturedAclState::Entries(1),
                    &[entry],
                ),
                want
            );
        }
    }

    #[test]
    fn entry_count_must_match_the_present_state() {
        let metadata = metadata(PrivateObjectKind::Directory, 10);
        assert_eq!(
            assess_private_descendant(
                PrivateObjectKind::Directory,
                10,
                &metadata,
                CapturedAclState::Entries(1),
                &[],
            ),
            Err(PrivateAccessRefusal::InconsistentCapture)
        );
    }

    #[test]
    fn type_mismatch_with_the_other_kinds_exact_permissions_refuses() {
        let directory_bits = 0o040000;
        let file_bits = 0o100000;
        assert_eq!(
            assess_private_descendant(
                PrivateObjectKind::Directory,
                10,
                &meta_mode(file_bits | 0o700),
                CapturedAclState::Entries(0),
                &[],
            ),
            Err(PrivateAccessRefusal::ModeShape)
        );
        assert_eq!(
            assess_private_descendant(
                PrivateObjectKind::RegularFile,
                10,
                &meta_mode(directory_bits | 0o600),
                CapturedAclState::Entries(0),
                &[],
            ),
            Err(PrivateAccessRefusal::ModeShape)
        );
    }

    #[test]
    fn file_mode_is_exact() {
        for permissions in [0o4600, 0o2600, 0o1600, 0o400] {
            assert_eq!(
                assess_private_descendant(
                    PrivateObjectKind::RegularFile,
                    10,
                    &meta_mode(0o100000 | permissions),
                    CapturedAclState::Entries(0),
                    &[],
                ),
                Err(PrivateAccessRefusal::ModeShape)
            );
        }
        assert_eq!(
            assess_private_descendant(
                PrivateObjectKind::RegularFile,
                10,
                &meta_mode(0o100000 | 0o600),
                CapturedAclState::Entries(0),
                &[],
            ),
            Ok(())
        );
    }

    fn meta_mode(mode: u32) -> DescriptorMetadata {
        DescriptorMetadata {
            device: 1,
            inode: 2,
            mode,
            uid: 10,
            gid: 3,
            links: 1,
            size: 0,
            modified: (0, 0),
            changed: (0, 0),
            flags: 0,
        }
    }

    #[cfg(target_os = "macos")]
    #[test]
    fn fresh_private_file_gains_a_zero_allow_and_a_loose_file_is_not_rewritten() {
        use opensip_platform::WorkLedger;
        use std::fs::OpenOptions;
        use std::os::unix::fs::{MetadataExt, OpenOptionsExt, PermissionsExt};
        struct Scratch(std::path::PathBuf);
        impl Drop for Scratch {
            fn drop(&mut self) {
                let _ = std::fs::remove_dir_all(&self.0);
            }
        }
        let nonce = opensip_platform::request_entropy().unwrap();
        let name: String = nonce.iter().map(|b| format!("{b:02x}")).collect();
        let scratch = Scratch(
            crate::test_scratch::temp_dir().join(format!("opensip-prepare-private-{name}")),
        );
        let root = &scratch.0;
        std::fs::create_dir(root).unwrap();
        let private_path = root.join("private");
        let loose_path = root.join("loose");
        let private_file = OpenOptions::new()
            .read(true)
            .write(true)
            .create_new(true)
            .mode(0o600)
            .open(&private_path)
            .unwrap();
        let uid = private_file.metadata().unwrap().uid();
        let mut owner = WorkLedger::new();
        let sample = owner
            .scope(|work| {
                prepare_fresh_private_sample(
                    PrivateObjectKind::RegularFile,
                    uid,
                    &private_file,
                    work,
                )
            })
            .unwrap();
        assert_eq!(sample.acl_state(), CapturedAclState::Entries(1));
        let directory_path = root.join("directory");
        std::fs::create_dir(&directory_path).unwrap();
        std::fs::set_permissions(&directory_path, std::fs::Permissions::from_mode(0o700)).unwrap();
        let directory = std::fs::File::open(&directory_path).unwrap();
        let mut directory_owner = WorkLedger::new();
        let directory_sample = directory_owner
            .scope(|work| {
                prepare_fresh_private_sample(PrivateObjectKind::Directory, uid, &directory, work)
            })
            .unwrap();
        assert_eq!(directory_sample.acl_state(), CapturedAclState::Entries(1));
        let mut again = WorkLedger::new();
        let second = again
            .scope(|work| {
                prepare_fresh_private_sample(
                    PrivateObjectKind::RegularFile,
                    uid,
                    &private_file,
                    work,
                )
            })
            .unwrap();
        assert_eq!(second.acl_state(), CapturedAclState::Entries(1));
        let mut recapture = WorkLedger::new();
        let reread = recapture
            .scope(|work| opensip_platform::capture_descriptor_acl_accounted(&private_file, work))
            .unwrap();
        assert_eq!(reread.acl_state(), CapturedAclState::Entries(1));
        let loose = OpenOptions::new()
            .read(true)
            .write(true)
            .create_new(true)
            .mode(0o644)
            .open(&loose_path)
            .unwrap();
        let mut loose_owner = WorkLedger::new();
        let refused = loose_owner.scope(|work| {
            prepare_fresh_private_sample(PrivateObjectKind::RegularFile, uid, &loose, work)
        });
        assert!(matches!(
            refused,
            Err(opensip_platform::WorkFailure::Operation(
                PreparePrivateError::Access(PrivateAccessRefusal::ModeShape)
            ))
        ));
        let mut check = WorkLedger::new();
        let after = check
            .scope(|work| opensip_platform::capture_descriptor_acl_accounted(&loose, work))
            .unwrap();
        assert_eq!(after.acl_state(), CapturedAclState::NotReturned);
        let limited = opensip_platform::descriptor_acl_capture_cost();
        let budget_path = root.join("budget");
        let budget_file = OpenOptions::new()
            .read(true)
            .write(true)
            .create_new(true)
            .mode(0o600)
            .open(&budget_path)
            .unwrap();
        let mut tight = WorkLedger::with_limits(limited).unwrap();
        let budget = tight.scope(|work| {
            prepare_fresh_private_sample(PrivateObjectKind::RegularFile, uid, &budget_file, work)
        });
        assert!(matches!(
            budget,
            Err(opensip_platform::WorkFailure::Budget(_))
        ));
        let mut budget_check = WorkLedger::new();
        let untouched = budget_check
            .scope(|work| opensip_platform::capture_descriptor_acl_accounted(&budget_file, work))
            .unwrap();
        assert_eq!(untouched.acl_state(), CapturedAclState::NotReturned);
        let foreign_path = root.join("foreign");
        let foreign = OpenOptions::new()
            .read(true)
            .write(true)
            .create_new(true)
            .mode(0o600)
            .open(&foreign_path)
            .unwrap();
        assert!(
            std::process::Command::new("/bin/chmod")
                .args([
                    "+a",
                    "group:everyone allow read",
                    foreign_path.to_str().unwrap()
                ])
                .status()
                .unwrap()
                .success()
        );
        let mut foreign_owner = WorkLedger::new();
        let foreign_result = foreign_owner.scope(|work| {
            prepare_fresh_private_sample(PrivateObjectKind::RegularFile, uid, &foreign, work)
        });
        assert!(matches!(
            foreign_result,
            Err(opensip_platform::WorkFailure::Operation(
                PreparePrivateError::Access(PrivateAccessRefusal::ForeignAclAccess)
            ))
        ));
        let mut foreign_check = WorkLedger::new();
        let foreign_after = foreign_check
            .scope(|work| opensip_platform::capture_descriptor_acl_accounted(&foreign, work))
            .unwrap();
        assert_eq!(foreign_after.acl_state(), CapturedAclState::Entries(1));
        assert_ne!(foreign_after.entry(0).unwrap().rights, 0);
        drop((private_file, loose, budget_file, foreign));
        let parent = opensip_platform::RetainedDirectory::from_retained_handle(
            std::fs::File::open(root).unwrap(),
        )
        .unwrap();
        let mut created_owner = WorkLedger::new();
        let (created, created_sample) = created_owner
            .scope(|work| create_private_regular_file(&parent, "created", uid, work))
            .unwrap();
        assert_eq!(created_sample.acl_state(), CapturedAclState::Entries(1));
        assert_eq!(created.metadata().unwrap().mode() & 0o777, 0o600);
        let (directory, directory_sample) = created_owner
            .scope(|work| create_private_directory(&parent, "nested", uid, work))
            .unwrap();
        assert_eq!(directory_sample.acl_state(), CapturedAclState::Entries(1));
        assert_eq!(directory.metadata().unwrap().mode() & 0o777, 0o700);
        let mut observed_owner = WorkLedger::new();
        let observed = observed_owner
            .scope(|work| observe_private_directory(&directory, uid, work))
            .unwrap();
        assert_eq!(observed.acl_state(), CapturedAclState::Entries(1));
        let child_parent = opensip_platform::RetainedDirectory::from_retained_handle(
            directory.try_clone().unwrap(),
        )
        .unwrap();
        let (child, child_sample) = observed_owner
            .scope(|work| {
                create_private_file_in_observed_directory(&child_parent, "inside", uid, work)
            })
            .unwrap();
        assert_eq!(child_sample.acl_state(), CapturedAclState::Entries(1));
        drop(child);
        let plain_parent = opensip_platform::RetainedDirectory::from_retained_handle(
            std::fs::File::open(root).unwrap(),
        )
        .unwrap();
        let mut blocked = WorkLedger::new();
        let blocked_result = blocked.scope(|work| {
            create_private_file_in_observed_directory(&plain_parent, "blocked", uid, work)
        });
        assert!(matches!(
            blocked_result,
            Err(opensip_platform::WorkFailure::Operation(
                PreparePrivateError::Access(PrivateAccessRefusal::AclNotReturned)
            ))
        ));
        assert!(!root.join("blocked").exists());
        for refused in ["", ".", "..", "a/b"] {
            let mut owner = WorkLedger::new();
            let result = owner.scope(|work| {
                create_private_file_in_observed_directory(&plain_parent, refused, uid, work)
            });
            assert!(
                matches!(
                    result,
                    Err(opensip_platform::WorkFailure::Operation(
                        PreparePrivateError::Name
                    ))
                ),
                "{refused}"
            );
            assert_eq!(owner.used(), opensip_platform::WorkCost::default());
        }
        let mut other_owner = WorkLedger::new();
        let other = other_owner.scope(|work| observe_private_directory(&directory, uid + 1, work));
        assert!(matches!(
            other,
            Err(opensip_platform::WorkFailure::Operation(
                PreparePrivateError::Access(PrivateAccessRefusal::ForeignOwner)
            ))
        ));
        let plain = root.join("plaindir");
        std::fs::create_dir(&plain).unwrap();
        std::fs::set_permissions(&plain, std::fs::Permissions::from_mode(0o700)).unwrap();
        let plain_file = std::fs::File::open(&plain).unwrap();
        let mut plain_owner = WorkLedger::new();
        let plain_result =
            plain_owner.scope(|work| observe_private_directory(&plain_file, uid, work));
        assert!(matches!(
            plain_result,
            Err(opensip_platform::WorkFailure::Operation(
                PreparePrivateError::Access(PrivateAccessRefusal::AclNotReturned)
            ))
        ));
        drop(directory);
        for refused in ["", ".", "..", "a/b"] {
            let mut owner = WorkLedger::new();
            let result = owner.scope(|work| create_private_directory(&parent, refused, uid, work));
            assert!(
                matches!(
                    result,
                    Err(opensip_platform::WorkFailure::Operation(
                        PreparePrivateError::Name
                    ))
                ),
                "{refused}"
            );
        }
        let mut tight = WorkLedger::with_limits(opensip_platform::WorkCost {
            objects: 1,
            edges: 1,
            bytes: 1,
        })
        .unwrap();
        let unpaid_dir =
            tight.scope(|work| create_private_directory(&parent, "unpaid-dir", uid, work));
        assert!(matches!(
            unpaid_dir,
            Err(opensip_platform::WorkFailure::Budget(_))
        ));
        assert!(!root.join("unpaid-dir").exists());
        let mut name_owner = WorkLedger::new();
        let bad_name =
            name_owner.scope(|work| create_private_regular_file(&parent, "a/b", uid, work));
        assert!(matches!(
            bad_name,
            Err(opensip_platform::WorkFailure::Operation(
                PreparePrivateError::Name
            ))
        ));
        for refused in ["", ".", ".."] {
            let mut owner = WorkLedger::new();
            let result =
                owner.scope(|work| create_private_regular_file(&parent, refused, uid, work));
            assert!(
                matches!(
                    result,
                    Err(opensip_platform::WorkFailure::Operation(
                        PreparePrivateError::Name
                    ))
                ),
                "{refused}"
            );
        }
        let mut tight = WorkLedger::with_limits(opensip_platform::WorkCost {
            objects: 1,
            edges: 1,
            bytes: 1,
        })
        .unwrap();
        let unpaid = tight.scope(|work| create_private_regular_file(&parent, "unpaid", uid, work));
        assert!(matches!(
            unpaid,
            Err(opensip_platform::WorkFailure::Budget(_))
        ));
        assert!(!root.join("unpaid").exists());
        let occupied = root.join("occupied");
        std::fs::write(&occupied, b"keep").unwrap();
        std::fs::set_permissions(&occupied, std::fs::Permissions::from_mode(0o644)).unwrap();
        let mut occupied_owner = WorkLedger::new();
        let occupied_result = occupied_owner
            .scope(|work| create_private_regular_file(&parent, "occupied", uid, work));
        assert!(matches!(
            occupied_result,
            Err(opensip_platform::WorkFailure::Operation(
                PreparePrivateError::Create(ref error)
            )) if error.kind() == std::io::ErrorKind::AlreadyExists
        ));
        assert_eq!(std::fs::read(&occupied).unwrap(), b"keep");
        assert_eq!(std::fs::metadata(&occupied).unwrap().mode() & 0o777, 0o644);
        drop(created);
    }

    #[cfg(target_os = "macos")]
    #[test]
    fn native_capture_feeds_state_before_entries() {
        use opensip_platform::{WorkLedger, capture_descriptor_acl_accounted};
        use std::fs::{self, File, Permissions};
        use std::os::unix::fs::{MetadataExt, OpenOptionsExt, PermissionsExt};
        struct Scratch(std::path::PathBuf);
        impl Drop for Scratch {
            fn drop(&mut self) {
                let _ = fs::remove_dir_all(&self.0);
            }
        }
        let nonce = opensip_platform::request_entropy().unwrap();
        let name: String = nonce.iter().map(|b| format!("{b:02x}")).collect();
        let scratch =
            Scratch(crate::test_scratch::temp_dir().join(format!("opensip-private-access-{name}")));
        let root = &scratch.0;
        fs::create_dir(root).unwrap();
        fs::set_permissions(root, Permissions::from_mode(0o700)).unwrap();
        let file_path = root.join("record");
        let file = std::fs::OpenOptions::new()
            .read(true)
            .write(true)
            .create_new(true)
            .mode(0o600)
            .open(&file_path)
            .unwrap();
        let uid = file.metadata().unwrap().uid();
        let mut owner = WorkLedger::new();
        let sample = owner
            .scope(|work| capture_descriptor_acl_accounted(&file, work))
            .unwrap();
        let decision =
            assess_private_descendant_capture(PrivateObjectKind::RegularFile, uid, &sample);
        match sample.acl_state() {
            CapturedAclState::NotReturned => {
                assert_eq!(decision, Err(PrivateAccessRefusal::AclNotReturned));
            }
            CapturedAclState::NoAclSentinel => {
                assert_eq!(decision, Err(PrivateAccessRefusal::AclSentinelUnqualified));
            }
            CapturedAclState::Entries(count) => {
                assert!(decision.is_err() || count == 0);
                if let Ok(()) = decision {
                    assert_eq!(count, 0);
                }
            }
        }
        drop(file);
        let _ = File::open(&file_path);
    }
}
