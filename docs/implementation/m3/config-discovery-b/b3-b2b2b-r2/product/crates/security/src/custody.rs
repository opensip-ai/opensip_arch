//! Pure custody predicates over supplied OS-width observations. These values
//! are not lstat/ACL measurements, retained-handle checks or admission authority.
use std::collections::BTreeSet;
const MAX_CONFIG_BYTES: u64 = 4 * 1024 * 1024;
#[derive(Clone, Copy)]
enum EntryKind {
    Directory,
    Regular,
    Symlink,
    Other,
}
#[derive(Clone)]
enum Principal {
    User(u32),
    Group(u32),
    Unresolved,
}
#[derive(Clone)]
enum AclWrite {
    Unreadable,
    Known(Vec<Principal>),
}
struct EntryObservation {
    kind: EntryKind,
    uid: u32,
    gid: u32,
    mode: u32,
    links: u64,
    size: u64,
    acl: AclWrite,
}
#[derive(Clone, Copy)]
enum Scope {
    Directory,
    ConfigurationFile,
    OperationalFile,
}
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Refusal {
    Absent,
    Symlink,
    NotDirectory,
    NotRegular,
    ForeignOwner,
    OthersWrite,
    GroupWrite,
    AclUnreadable,
    AclWrite,
    HardLinked,
    Unlinked,
    TooLarge,
}
impl Refusal {
    fn code(self) -> &'static str {
        match self {
            Self::Absent => "ABSENT",
            Self::Symlink => "SYMLINK",
            Self::NotDirectory => "NOT_A_DIRECTORY",
            Self::NotRegular => "NOT_A_REGULAR_FILE",
            Self::ForeignOwner => "FOREIGN_OWNER",
            Self::OthersWrite => "WRITABLE_BY_OTHERS",
            Self::GroupWrite => "WRITABLE_BY_GROUP",
            Self::AclUnreadable => "ACL_UNREADABLE",
            Self::AclWrite => "WRITABLE_BY_ACL",
            Self::HardLinked => "HARD_LINKED",
            Self::Unlinked => "UNLINKED",
            Self::TooLarge => "TOO_LARGE",
        }
    }
}
fn check(
    entry: Option<&EntryObservation>,
    scope: Scope,
    invoking_uid: u32,
    authorized_groups: &BTreeSet<u32>,
    waive_owner: bool,
) -> Result<(), Refusal> {
    let e = entry.ok_or(Refusal::Absent)?;
    match e.kind {
        EntryKind::Symlink => return Err(Refusal::Symlink),
        EntryKind::Directory if matches!(scope, Scope::Directory) => {}
        EntryKind::Regular
            if matches!(scope, Scope::ConfigurationFile | Scope::OperationalFile) => {}
        _ => {
            return Err(if matches!(scope, Scope::Directory) {
                Refusal::NotDirectory
            } else {
                Refusal::NotRegular
            });
        }
    }
    if (!waive_owner || matches!(scope, Scope::OperationalFile))
        && e.uid != 0
        && e.uid != invoking_uid
    {
        return Err(Refusal::ForeignOwner);
    }
    if e.mode & 0o002 != 0 {
        return Err(Refusal::OthersWrite);
    }
    if e.mode & 0o020 != 0 && !authorized_groups.contains(&e.gid) {
        return Err(Refusal::GroupWrite);
    }
    match &e.acl {
        AclWrite::Unreadable => return Err(Refusal::AclUnreadable),
        AclWrite::Known(principals) => {
            for principal in principals {
                let trusted = match principal {
                    Principal::User(uid) => *uid == 0 || *uid == invoking_uid,
                    Principal::Group(gid) => authorized_groups.contains(gid),
                    Principal::Unresolved => false,
                };
                if !trusted {
                    return Err(Refusal::AclWrite);
                }
            }
        }
    }
    if matches!(scope, Scope::ConfigurationFile | Scope::OperationalFile) {
        // A last SQLite closer can unlink a sidecar while our old descriptor
        // remains open. Refusal is unavailable linkage, not a hardlink attack,
        // path absence or evidence of corruption. Do not retry here.
        if e.links == 0 && matches!(scope, Scope::OperationalFile) {
            return Err(Refusal::Unlinked);
        }
        if e.links != 1 {
            return Err(Refusal::HardLinked);
        }
        if matches!(scope, Scope::ConfigurationFile) && e.size > MAX_CONFIG_BYTES {
            return Err(Refusal::TooLarge);
        }
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use opensip_identity::JsonValue as V;
    fn object(v: &V) -> &std::collections::BTreeMap<String, V> {
        if let V::Object(o) = v {
            o
        } else {
            panic!("object")
        }
    }
    fn text(v: &V) -> &str {
        if let V::String(s) = v {
            s
        } else {
            panic!("string")
        }
    }
    fn number(v: &V) -> u64 {
        if let V::Integer(i) = v {
            u64::try_from(i.get()).unwrap()
        } else {
            panic!("integer")
        }
    }
    fn array(v: &V) -> &[V] {
        if let V::Array(a) = v {
            a
        } else {
            panic!("array")
        }
    }
    #[test]
    fn typed_custody_predicates_match_selected_os_width_reference_corpus() {
        let mut count = 0;
        let mut admitted = 0;
        for line in include_bytes!("../tests/fixtures/custody-predicate-cases.ndjson")
            .split(|b| *b == b'\n')
            .filter(|b| !b.is_empty())
        {
            let v = opensip_identity::parse_json(line).unwrap();
            let q = object(&v);
            let scope = if text(&q["scope"]) == "directory" {
                Scope::Directory
            } else {
                Scope::ConfigurationFile
            };
            let entry = if q["entry"] == V::Null {
                None
            } else {
                let e = object(&q["entry"]);
                let kind = match text(&e["kind"]) {
                    "dir" => EntryKind::Directory,
                    "file" => EntryKind::Regular,
                    "symlink" => EntryKind::Symlink,
                    _ => EntryKind::Other,
                };
                let acl = if e["aclUnreadable"] == V::Bool(true) {
                    AclWrite::Unreadable
                } else {
                    AclWrite::Known(
                        array(&e["aclWrite"])
                            .iter()
                            .map(|v| {
                                let p = text(v);
                                if let Some(uid) = p.strip_prefix("uid:") {
                                    Principal::User(uid.parse().unwrap())
                                } else if let Some(gid) = p.strip_prefix("group:") {
                                    Principal::Group(gid.parse().unwrap())
                                } else {
                                    Principal::Unresolved
                                }
                            })
                            .collect(),
                    )
                };
                Some(EntryObservation {
                    kind,
                    uid: u32::try_from(number(&e["uid"])).unwrap(),
                    gid: u32::try_from(number(&e["gid"])).unwrap(),
                    mode: u32::try_from(number(&e["mode"])).unwrap(),
                    links: number(&e["nlink"]),
                    size: number(&e["size"]),
                    acl,
                })
            };
            let groups = array(&q["groups"])
                .iter()
                .map(|v| u32::try_from(number(v)).unwrap())
                .collect();
            let result = check(
                entry.as_ref(),
                scope,
                u32::try_from(number(&q["invokingUid"])).unwrap(),
                &groups,
                q["waiveOwner"] == V::Bool(true),
            );
            let expected = if q["expected"] == V::Null {
                None
            } else {
                Some(text(&q["expected"]))
            };
            assert_eq!(result.err().map(Refusal::code), expected, "case {count}");
            count += 1;
            admitted += usize::from(result.is_ok());
        }
        assert_eq!((count, admitted), (18851, 5225));
    }
    #[test]
    fn unknown_acl_is_not_empty_and_owner_waiver_preserves_other_guards() {
        let mut e = EntryObservation {
            kind: EntryKind::Regular,
            uid: 1001,
            gid: 50,
            mode: 0o600,
            links: 1,
            size: 0,
            acl: AclWrite::Unreadable,
        };
        let groups = BTreeSet::new();
        assert_eq!(
            check(Some(&e), Scope::ConfigurationFile, 1000, &groups, true),
            Err(Refusal::AclUnreadable)
        );
        e.acl = AclWrite::Known(vec![]);
        assert_eq!(
            check(Some(&e), Scope::ConfigurationFile, 1000, &groups, true),
            Ok(())
        );
        e.links = 2;
        assert_eq!(
            check(Some(&e), Scope::ConfigurationFile, 1000, &groups, true),
            Err(Refusal::HardLinked)
        );
        e.mode = 0o602;
        assert_eq!(
            check(Some(&e), Scope::ConfigurationFile, 1000, &groups, true),
            Err(Refusal::OthersWrite)
        );
    }
}

/// Apply the pure predicates to an actual descriptor observation, while retaining
/// the distinction between a failed read and a policy refusal. The caller still
/// supplies identity/group/waiver scope; success is not a custody grant and does
/// not authenticate the path or its ancestors.
#[derive(Debug)]
pub enum NativeRefusal {
    Observation(opensip_platform::DescriptorObservationError),
    Predicate(Refusal),
}
fn check_retained_descriptor(
    file: &std::fs::File,
    scope: Scope,
    invoking_uid: u32,
    authorized_groups: &BTreeSet<u32>,
    waive_owner: bool,
) -> Result<opensip_platform::DescriptorObservation, NativeRefusal> {
    let observed =
        opensip_platform::observe_descriptor(file).map_err(NativeRefusal::Observation)?;
    check_descriptor_observation(
        &observed,
        scope,
        invoking_uid,
        authorized_groups,
        waive_owner,
    )
    .map_err(NativeRefusal::Predicate)?;
    Ok(observed)
}
fn check_descriptor_observation(
    observed: &opensip_platform::DescriptorObservation,
    scope: Scope,
    invoking_uid: u32,
    authorized_groups: &BTreeSet<u32>,
    waive_owner: bool,
) -> Result<(), Refusal> {
    let m = &observed.metadata;
    let entry = EntryObservation {
        kind: match m.mode & 0o170000 {
            0o040000 => EntryKind::Directory,
            0o100000 => EntryKind::Regular,
            0o120000 => EntryKind::Symlink,
            _ => EntryKind::Other,
        },
        uid: m.uid,
        gid: m.gid,
        mode: m.mode,
        links: m.links,
        size: m.size,
        // Law 461: an omitted ACL is unreadable, never "no writers". The
        // `check` arm order is unchanged, so earlier refusals still win.
        acl: match &observed.acl {
            opensip_platform::DescriptorAcl::Omitted => AclWrite::Unreadable,
            opensip_platform::DescriptorAcl::Present(writers) => AclWrite::Known(
                writers
                    .iter()
                    .map(|p| match p {
                        opensip_platform::AclWriter::User(uid) => Principal::User(*uid),
                        opensip_platform::AclWriter::Group(gid) => Principal::Group(*gid),
                        opensip_platform::AclWriter::Unresolved => Principal::Unresolved,
                    })
                    .collect(),
            ),
        },
    };
    check(
        Some(&entry),
        scope,
        invoking_uid,
        authorized_groups,
        waive_owner,
    )
}

/// Rights that cannot change a directory: list, search, read attributes, read
/// extended attributes, read security and synchronize. Every other bit,
/// including unknown and generic bits, is treated as a possible write.
const READ_ONLY_ACE_RIGHTS: u32 = (1 << 1) | (1 << 3) | (1 << 7) | (1 << 9) | (1 << 11) | (1 << 20);

/// Judge one existing external ancestor of I (H, `Library`, `Application
/// Support`) from a bounded ACL capture. The directory must be owned by the
/// invoking user or root and have no group or other write bit. Its ACL must be
/// present and grant no possible write to anyone except the invoking user or
/// root. Project trust groups never waive this. Omission and the NOACL
/// sentinel are unreadable, never an empty writer list. The captured state
/// fixes the entry count; `entry` only returns entries. This does not judge
/// the name binding, the path, or any child, and it grants no authority.
pub(crate) fn check_external_ancestor(
    metadata: &opensip_platform::DescriptorMetadata,
    state: opensip_platform::CapturedAclState,
    entry: impl Fn(usize) -> Option<opensip_platform::CapturedAclEntry>,
    invoking_uid: u32,
) -> Result<(), Refusal> {
    let observed = EntryObservation {
        kind: match metadata.mode & 0o170000 {
            0o040000 => EntryKind::Directory,
            0o100000 => EntryKind::Regular,
            0o120000 => EntryKind::Symlink,
            _ => EntryKind::Other,
        },
        uid: metadata.uid,
        gid: metadata.gid,
        mode: metadata.mode,
        links: metadata.links,
        size: metadata.size,
        // The ACL is judged below from the capture. An empty list does not
        // allocate and keeps the existing refusal order: ACL after mode.
        acl: AclWrite::Known(Vec::new()),
    };
    check(
        Some(&observed),
        Scope::Directory,
        invoking_uid,
        &BTreeSet::new(),
        false,
    )?;
    external_ancestor_acl(state, entry, invoking_uid)
}

fn external_ancestor_acl(
    state: opensip_platform::CapturedAclState,
    entry: impl Fn(usize) -> Option<opensip_platform::CapturedAclEntry>,
    invoking_uid: u32,
) -> Result<(), Refusal> {
    use crate::private_access::{ACE_DENY, ACE_KIND_MASK, ACE_PERMIT, KNOWN_ACE_FLAGS};
    use opensip_platform::{CapturedAclPrincipal, CapturedAclState};
    let CapturedAclState::Entries(count) = state else {
        return Err(Refusal::AclUnreadable);
    };
    for index in 0..count {
        let Some(e) = entry(index) else {
            return Err(Refusal::AclUnreadable);
        };
        // An entry this code cannot interpret is not evidence of no writer.
        if e.flags & !KNOWN_ACE_FLAGS != 0 {
            return Err(Refusal::AclUnreadable);
        }
        match e.flags & ACE_KIND_MASK {
            ACE_DENY => {}
            // Inheritance flags do not exempt an allow: it can still grant
            // this directory or pass the write to a new child.
            ACE_PERMIT if e.rights & !READ_ONLY_ACE_RIGHTS == 0 => {}
            ACE_PERMIT => match e.principal {
                CapturedAclPrincipal::User(uid) if uid == 0 || uid == invoking_uid => {}
                _ => return Err(Refusal::AclWrite),
            },
            _ => return Err(Refusal::AclUnreadable),
        }
    }
    Ok(())
}

/// A member of the executing core's tree (law 463, core-tree custody).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum CoreTreeKind {
    Directory,
    Regular,
}

/// Judge one opened member of the executing core's tree from a bounded ACL
/// capture (law 463 r3, core-tree custody). The core tree is not an external
/// ancestor of I, so the owner may be any account or root. The member must be
/// the expected kind, with no group or other write bit, and a regular file must
/// have exactly one link. Its ACL must be present and grant no possible write
/// to anyone but its owner or root; inherit-only allows count. Omission and the
/// NOACL sentinel refuse. This judges no name or path and grants no authority.
pub(crate) fn check_core_tree_member(
    metadata: &opensip_platform::DescriptorMetadata,
    expected: CoreTreeKind,
    state: opensip_platform::CapturedAclState,
    entry: impl Fn(usize) -> Option<opensip_platform::CapturedAclEntry>,
) -> Result<(), Refusal> {
    match (metadata.mode & 0o170000, expected) {
        (0o120000, _) => return Err(Refusal::Symlink),
        (0o040000, CoreTreeKind::Directory) | (0o100000, CoreTreeKind::Regular) => {}
        (_, CoreTreeKind::Directory) => return Err(Refusal::NotDirectory),
        (_, CoreTreeKind::Regular) => return Err(Refusal::NotRegular),
    }
    if metadata.mode & 0o002 != 0 {
        return Err(Refusal::OthersWrite);
    }
    if metadata.mode & 0o020 != 0 {
        return Err(Refusal::GroupWrite);
    }
    if expected == CoreTreeKind::Regular {
        match metadata.links {
            0 => return Err(Refusal::Unlinked),
            1 => {}
            _ => return Err(Refusal::HardLinked),
        }
    }
    // The owner stands where the invoking user stands for external ancestors.
    external_ancestor_acl(state, entry, metadata.uid)
}

#[derive(Debug)]
pub(crate) enum AncestorRefusal {
    Capture(opensip_platform::DescriptorAclCaptureError),
    Predicate(Refusal),
}

/// Capture one retained external-ancestor directory with the bounded reader,
/// charged to `work`, and judge it with `check_external_ancestor`. The caller
/// still owes the name binding and rechecks. Nothing is created or changed.
pub(crate) fn observe_external_ancestor(
    directory: &std::fs::File,
    invoking_uid: u32,
    work: &mut opensip_platform::WorkScope<'_>,
) -> Result<opensip_platform::DescriptorAclCapture, opensip_platform::WorkFailure<AncestorRefusal>>
{
    use opensip_platform::WorkFailure;
    let sample =
        opensip_platform::capture_descriptor_acl_accounted(directory, work).map_err(|error| {
            match error {
                WorkFailure::Budget(budget) => WorkFailure::Budget(budget),
                WorkFailure::Operation(error) => {
                    WorkFailure::Operation(AncestorRefusal::Capture(error))
                }
            }
        })?;
    check_external_ancestor(
        sample.metadata(),
        sample.acl_state(),
        |index| sample.entry(index),
        invoking_uid,
    )
    .map_err(|refusal| WorkFailure::Operation(AncestorRefusal::Predicate(refusal)))?;
    Ok(sample)
}

#[cfg(test)]
mod external_ancestor_tests {
    use super::*;
    use crate::private_access::{ACE_DENY, ACE_PERMIT};
    use opensip_platform::{
        CapturedAclEntry, CapturedAclPrincipal, CapturedAclState, DescriptorMetadata,
    };
    const ME: u32 = 501;
    fn directory(uid: u32, permissions: u32) -> DescriptorMetadata {
        DescriptorMetadata {
            device: 1,
            inode: 2,
            mode: 0o040000 | permissions,
            uid,
            gid: 20,
            links: 3,
            size: 96,
            modified: (0, 0),
            changed: (0, 0),
            flags: 0,
        }
    }
    fn ace(
        kind: u32,
        extra_flags: u32,
        rights: u32,
        principal: CapturedAclPrincipal,
    ) -> CapturedAclEntry {
        CapturedAclEntry {
            flags: kind | extra_flags,
            rights,
            principal,
        }
    }
    fn judge(metadata: &DescriptorMetadata, entries: &[CapturedAclEntry]) -> Result<(), Refusal> {
        check_external_ancestor(
            metadata,
            CapturedAclState::Entries(entries.len()),
            |index| entries.get(index).copied(),
            ME,
        )
    }
    const OTHERS: [CapturedAclPrincipal; 4] = [
        CapturedAclPrincipal::Group(20),
        CapturedAclPrincipal::Group(0),
        CapturedAclPrincipal::User(502),
        CapturedAclPrincipal::Unresolved,
    ];

    #[test]
    fn omission_and_sentinel_are_unreadable_whatever_entry_returns() {
        let good = directory(ME, 0o700);
        let foreign = ace(ACE_PERMIT, 0, 1 << 2, CapturedAclPrincipal::Group(20));
        for state in [
            CapturedAclState::NotReturned,
            CapturedAclState::NoAclSentinel,
        ] {
            assert_eq!(
                check_external_ancestor(&good, state, |_| None, ME),
                Err(Refusal::AclUnreadable)
            );
            assert_eq!(
                check_external_ancestor(&good, state, |_| Some(foreign), ME),
                Err(Refusal::AclUnreadable)
            );
        }
    }

    #[test]
    fn present_acl_admits_invoking_or_root_owner_and_other_read_search() {
        for (uid, permissions) in [
            (ME, 0o700),
            (ME, 0o750),
            (ME, 0o755),
            (0, 0o755),
            (0, 0o1755),
        ] {
            assert_eq!(judge(&directory(uid, permissions), &[]), Ok(()));
        }
        // The stock macOS home, Library and Application Support entry.
        let stock = ace(ACE_DENY, 0, 1 << 4, CapturedAclPrincipal::Group(12));
        assert_eq!(judge(&directory(ME, 0o700), &[stock]), Ok(()));
    }

    #[test]
    fn mode_and_owner_refusals_precede_the_acl() {
        let cases = [
            (directory(502, 0o700), Refusal::ForeignOwner),
            (directory(ME, 0o702), Refusal::OthersWrite),
            (directory(ME, 0o770), Refusal::GroupWrite),
            (directory(0, 0o775), Refusal::GroupWrite),
            (
                DescriptorMetadata {
                    mode: 0o100600,
                    ..directory(ME, 0o700)
                },
                Refusal::NotDirectory,
            ),
        ];
        for (metadata, expected) in cases {
            assert_eq!(judge(&metadata, &[]), Err(expected));
            assert_eq!(
                check_external_ancestor(&metadata, CapturedAclState::NotReturned, |_| None, ME),
                Err(expected)
            );
        }
    }

    #[test]
    fn deny_and_read_only_allow_pass_for_any_principal() {
        let read_only = [1 << 1, 1 << 3, 1 << 7, 1 << 9, 1 << 11, 1 << 20];
        for principal in OTHERS {
            assert_eq!(
                judge(
                    &directory(ME, 0o700),
                    &[ace(ACE_DENY, 0, u32::MAX, principal)]
                ),
                Ok(())
            );
            assert_eq!(
                judge(&directory(ME, 0o700), &[ace(ACE_PERMIT, 0, 0, principal)]),
                Ok(())
            );
            for right in read_only {
                assert_eq!(
                    judge(
                        &directory(ME, 0o700),
                        &[ace(ACE_PERMIT, 0, right, principal)]
                    ),
                    Ok(())
                );
            }
            assert_eq!(
                judge(
                    &directory(ME, 0o700),
                    &[ace(ACE_PERMIT, 0, read_only.iter().sum(), principal)]
                ),
                Ok(())
            );
        }
    }

    #[test]
    fn any_other_right_is_a_write_for_anyone_but_the_invoking_user_or_root() {
        // Known mutating rights, then an unknown bit, the four generic bits and bit 31.
        let writes = [
            1 << 2,
            1 << 4,
            1 << 5,
            1 << 6,
            1 << 8,
            1 << 10,
            1 << 12,
            1 << 13,
            1 << 14,
            1 << 21,
            1 << 22,
            1 << 23,
            1 << 24,
            1 << 31,
            1,
        ];
        for right in writes {
            for principal in OTHERS {
                assert_eq!(
                    judge(
                        &directory(ME, 0o700),
                        &[ace(ACE_PERMIT, 0, right | (1 << 1), principal)]
                    ),
                    Err(Refusal::AclWrite),
                    "right {right:#x}"
                );
            }
            for principal in [
                CapturedAclPrincipal::User(ME),
                CapturedAclPrincipal::User(0),
            ] {
                assert_eq!(
                    judge(
                        &directory(ME, 0o700),
                        &[ace(ACE_PERMIT, 0, right, principal)]
                    ),
                    Ok(())
                );
            }
        }
    }

    #[test]
    fn inheritance_flags_do_not_exempt_an_allow() {
        let group = CapturedAclPrincipal::Group(20);
        for flag in [1 << 4, 1 << 5, 1 << 6, 1 << 7, 1 << 8, (1 << 6) | (1 << 8)] {
            assert_eq!(
                judge(
                    &directory(ME, 0o700),
                    &[ace(ACE_PERMIT, flag, 1 << 2, group)]
                ),
                Err(Refusal::AclWrite)
            );
            assert_eq!(
                judge(&directory(ME, 0o700), &[ace(ACE_DENY, flag, 1 << 2, group)]),
                Ok(())
            );
        }
    }

    #[test]
    fn uninterpretable_or_missing_entries_are_unreadable() {
        let me = CapturedAclPrincipal::User(ME);
        for (flags, rights) in [(ACE_PERMIT | (1 << 11), 0), (3, 0), (0, 0), (0xf, 0)] {
            assert_eq!(
                judge(
                    &directory(ME, 0o700),
                    &[CapturedAclEntry {
                        flags,
                        rights,
                        principal: me
                    }]
                ),
                Err(Refusal::AclUnreadable)
            );
        }
        let one = [ace(ACE_DENY, 0, 1 << 4, CapturedAclPrincipal::Group(12))];
        assert_eq!(
            check_external_ancestor(
                &directory(ME, 0o700),
                CapturedAclState::Entries(2),
                |index| one.get(index).copied(),
                ME
            ),
            Err(Refusal::AclUnreadable)
        );
        // A later foreign writer is still found after an earlier harmless entry.
        let two = [
            one[0],
            ace(ACE_PERMIT, 0, 1 << 6, CapturedAclPrincipal::Group(20)),
        ];
        assert_eq!(judge(&directory(ME, 0o700), &two), Err(Refusal::AclWrite));
    }
}

#[cfg(all(test, target_os = "macos"))]
mod external_ancestor_native_tests {
    use super::*;
    use opensip_platform::{CapturedAclState, WorkFailure, WorkLedger};
    use std::os::unix::fs::{MetadataExt, PermissionsExt};
    struct Scratch(std::path::PathBuf);
    impl Drop for Scratch {
        fn drop(&mut self) {
            // A deny-delete fixture cannot be removed until its ACL is gone.
            let _ = std::process::Command::new("/bin/chmod")
                .args(["-R", "-N"])
                .arg(&self.0)
                .status();
            let _ = std::fs::remove_dir_all(&self.0);
        }
    }
    fn scratch() -> Scratch {
        let nonce = opensip_platform::request_entropy().unwrap();
        let name: String = nonce.iter().map(|b| format!("{b:02x}")).collect();
        let root = crate::test_scratch::temp_dir().join(format!("opensip-ancestor457-{name}"));
        std::fs::create_dir(&root).unwrap();
        Scratch(root)
    }
    fn fixture(
        root: &std::path::Path,
        name: &str,
        permissions: u32,
        acl: Option<&str>,
    ) -> std::fs::File {
        let path = root.join(name);
        std::fs::create_dir(&path).unwrap();
        std::fs::set_permissions(&path, std::fs::Permissions::from_mode(permissions)).unwrap();
        if let Some(acl) = acl {
            assert!(
                std::process::Command::new("/bin/chmod")
                    .args(["+a", acl, path.to_str().unwrap()])
                    .status()
                    .unwrap()
                    .success()
            );
        }
        std::fs::File::open(&path).unwrap()
    }
    fn observe(
        file: &std::fs::File,
        uid: u32,
    ) -> Result<CapturedAclState, WorkFailure<AncestorRefusal>> {
        let mut ledger = WorkLedger::new();
        let result = ledger
            .scope(|work| observe_external_ancestor(file, uid, work))
            .map(|sample| sample.acl_state());
        assert_eq!(
            ledger.used(),
            opensip_platform::descriptor_acl_capture_cost()
        );
        result
    }
    fn refusal(result: Result<CapturedAclState, WorkFailure<AncestorRefusal>>) -> Refusal {
        match result {
            Err(WorkFailure::Operation(AncestorRefusal::Predicate(refusal))) => refusal,
            other => panic!("expected a predicate refusal, got {other:?}"),
        }
    }

    #[test]
    fn native_ancestor_capture_refuses_omission_and_foreign_writers() {
        let scratch = scratch();
        let root = &scratch.0;
        let plain = fixture(root, "plain", 0o700, None);
        let uid = plain.metadata().unwrap().uid();
        assert_eq!(refusal(observe(&plain, uid)), Refusal::AclUnreadable);
        let stock = fixture(root, "stock", 0o700, Some("group:everyone deny delete"));
        assert_eq!(observe(&stock, uid).unwrap(), CapturedAclState::Entries(1));
        let readable = fixture(
            root,
            "readable",
            0o755,
            Some("group:everyone allow list,search,readattr"),
        );
        assert_eq!(
            observe(&readable, uid).unwrap(),
            CapturedAclState::Entries(1)
        );
        let root_writer = fixture(
            root,
            "root-writer",
            0o700,
            Some("user:root allow add_file,delete_child"),
        );
        assert_eq!(
            observe(&root_writer, uid).unwrap(),
            CapturedAclState::Entries(1)
        );
        for (name, acl) in [
            ("add-file", "group:everyone allow add_file"),
            ("subdirectory", "group:staff allow add_subdirectory"),
            ("delete-child", "group:everyone allow delete_child"),
            ("security", "group:everyone allow writesecurity"),
            (
                "inherit-only",
                "group:everyone allow add_file,directory_inherit,only_inherit",
            ),
        ] {
            let file = fixture(root, name, 0o700, Some(acl));
            assert_eq!(refusal(observe(&file, uid)), Refusal::AclWrite, "{name}");
        }
        let group_write = fixture(
            root,
            "group-write",
            0o770,
            Some("group:everyone deny delete"),
        );
        assert_eq!(refusal(observe(&group_write, uid)), Refusal::GroupWrite);
        assert_eq!(
            refusal(observe(&stock, uid.checked_add(1).unwrap())),
            Refusal::ForeignOwner
        );
    }

    #[test]
    fn native_ancestor_capture_that_cannot_be_paid_refuses_and_latches() {
        let scratch = scratch();
        let file = fixture(
            &scratch.0,
            "tight",
            0o700,
            Some("group:everyone deny delete"),
        );
        let uid = file.metadata().unwrap().uid();
        let mut cost = opensip_platform::descriptor_acl_capture_cost();
        cost.edges -= 1;
        let mut tight = WorkLedger::with_limits(cost).unwrap();
        let result = tight.scope(|work| observe_external_ancestor(&file, uid, work));
        assert!(matches!(result, Err(WorkFailure::Budget(_))));
        assert!(tight.is_failed());
    }
}
#[cfg(all(test, target_os = "macos"))]
mod native_tests {
    use super::*;
    use std::{
        fs,
        os::unix::fs::{MetadataExt, OpenOptionsExt, PermissionsExt},
    };
    #[test]
    fn actual_descriptor_metadata_reaches_custody_predicates() {
        let parent = crate::test_scratch::acl_scratch();
        let nonce = opensip_platform::request_entropy().unwrap();
        let name = nonce.iter().map(|b| format!("{b:02x}")).collect::<String>();
        let path = parent.join(format!("opensip-custody83-{name}"));
        let file = fs::OpenOptions::new()
            .read(true)
            .write(true)
            .create_new(true)
            .mode(0o600)
            .open(&path)
            .unwrap();
        struct Remove(std::path::PathBuf);
        impl Drop for Remove {
            fn drop(&mut self) {
                let _ = fs::remove_file(&self.0);
            }
        }
        let _cleanup = Remove(path.clone());
        let uid = file.metadata().unwrap().uid();
        let groups = BTreeSet::new();
        assert!(
            check_retained_descriptor(&file, Scope::ConfigurationFile, uid, &groups, false).is_ok()
        );
        file.set_permissions(fs::Permissions::from_mode(0o602))
            .unwrap();
        assert!(matches!(
            check_retained_descriptor(&file, Scope::ConfigurationFile, uid, &groups, true),
            Err(NativeRefusal::Predicate(Refusal::OthersWrite))
        ));
        file.set_permissions(fs::Permissions::from_mode(0o600))
            .unwrap();
        assert!(matches!(
            check_retained_descriptor(&file, Scope::Directory, uid, &groups, false),
            Err(NativeRefusal::Predicate(Refusal::NotDirectory))
        ));
        let link = path.with_extension("hard-link");
        fs::hard_link(&path, &link).unwrap();
        let _link_cleanup = Remove(link);
        assert!(matches!(
            check_retained_descriptor(&file, Scope::ConfigurationFile, uid, &groups, false),
            Err(NativeRefusal::Predicate(Refusal::HardLinked))
        ));
    }
}

/// Observed policy result only. Rechecks sample names; they do not exclude ABA,
/// concurrent permission changes, mount substitution or writes after return.
/// Host local-filesystem admission and exclusion through consumption remain owed.
#[derive(Debug)]
pub enum DirectoryPathRefusal {
    EmptyChain,
    NameObservation(std::io::Error),
    NameChanged,
    Descriptor(opensip_platform::DescriptorObservationError),
    Predicate { component: usize, refusal: Refusal },
}
/// Inspect a retained operational/store path after selection. This is not the
/// S3 project-discovery walk: it examines the entire chain to the filesystem
/// root, refuses any failed component, and grants no explicit-project owner
/// waiver. Discovery has its own stopping boundaries, ancestor fallback, and
/// --trust-project-owner rules; this function must not replace that walk.
/// Supplied UID/groups still require host admission. Success is only a sampled
/// predicate result, never exclusion or a permission to consume/write evidence.
pub(crate) fn inspect_directory_path(
    path: &opensip_platform::RetainedDirectoryPath,
    invoking_uid: u32,
    authorized_groups: &BTreeSet<u32>,
) -> Result<Vec<opensip_platform::DescriptorObservation>, DirectoryPathRefusal> {
    inspect_directory_path_with(path, invoking_uid, authorized_groups, || {})
}
fn inspect_directory_path_with(
    path: &opensip_platform::RetainedDirectoryPath,
    invoking_uid: u32,
    authorized_groups: &BTreeSet<u32>,
    after_observation: impl FnOnce(),
) -> Result<Vec<opensip_platform::DescriptorObservation>, DirectoryPathRefusal> {
    if !path
        .recheck_exact_names()
        .map_err(DirectoryPathRefusal::NameObservation)?
    {
        return Err(DirectoryPathRefusal::NameChanged);
    }
    let observations = path
        .observe_directories()
        .map_err(DirectoryPathRefusal::Descriptor)?;
    after_observation();
    if !path
        .recheck_exact_names()
        .map_err(DirectoryPathRefusal::NameObservation)?
    {
        return Err(DirectoryPathRefusal::NameChanged);
    }
    check_operational_chain_observations(&observations, invoking_uid, authorized_groups)?;
    Ok(observations)
}
// Pure sampled-policy join, shared by the actual descriptor path above and
// synthetic predicate tests. It cannot grant custody or manufacture OS evidence.
fn check_operational_chain_observations(
    observations: &[opensip_platform::DescriptorObservation],
    invoking_uid: u32,
    authorized_groups: &BTreeSet<u32>,
) -> Result<(), DirectoryPathRefusal> {
    if observations.is_empty() {
        return Err(DirectoryPathRefusal::EmptyChain);
    }
    for (component, observed) in observations.iter().enumerate() {
        // Test-only, opt-in per thread: the real system ancestors of an ACL
        // scratch base cannot carry an ACL (see `test_scratch::acl_scratch`).
        #[cfg(test)]
        if crate::test_scratch::above_acl_scratch(observed.metadata.device, observed.metadata.inode)
        {
            continue;
        }
        // No ownership waiver for a retained operational/store component.
        check_descriptor_observation(
            observed,
            Scope::Directory,
            invoking_uid,
            authorized_groups,
            false,
        )
        .map_err(|refusal| DirectoryPathRefusal::Predicate { component, refusal })?;
    }
    Ok(())
}

#[cfg(all(test, target_os = "macos"))]
mod directory_path_tests {
    use super::*;
    use opensip_platform::RetainedDirectoryPath;
    use std::{
        fs,
        os::unix::fs::PermissionsExt,
        path::{Path, PathBuf},
    };
    // Test-only retries of actual transient metadata change, never policy/name
    // failures. No production retry or weakened custody observation is added.
    fn observe(path: &RetainedDirectoryPath) -> Vec<opensip_platform::DescriptorObservation> {
        for _ in 0..256 {
            match path.observe_directories() {
                Err(opensip_platform::DescriptorObservationError::ChangedDuringRead) => {
                    std::thread::sleep(std::time::Duration::from_millis(1))
                }
                result => return result.unwrap(),
            }
        }
        panic!("no stable test observation of shared ancestors");
    }
    fn inspect(
        mut call: impl FnMut() -> Result<
            Vec<opensip_platform::DescriptorObservation>,
            DirectoryPathRefusal,
        >,
    ) -> Result<Vec<opensip_platform::DescriptorObservation>, DirectoryPathRefusal> {
        for _ in 0..256 {
            match call() {
                Err(DirectoryPathRefusal::Descriptor(
                    opensip_platform::DescriptorObservationError::ChangedDuringRead,
                )) => std::thread::sleep(std::time::Duration::from_millis(1)),
                result => return result,
            }
        }
        panic!("no stable test observation of shared ancestors");
    }
    struct Fixture(PathBuf);
    impl Fixture {
        fn new() -> Self {
            let tag = opensip_platform::request_entropy()
                .unwrap()
                .iter()
                .map(|b| format!("{b:02x}"))
                .collect::<String>();
            let path = crate::test_scratch::acl_scratch()
                .join(format!("opensip-directory-custody191-{tag}"));
            fs::create_dir(&path).unwrap();
            fs::set_permissions(&path, fs::Permissions::from_mode(0o700)).unwrap();
            fs::create_dir(path.join("leaf")).unwrap();
            fs::set_permissions(path.join("leaf"), fs::Permissions::from_mode(0o700)).unwrap();
            Self(fs::canonicalize(path).unwrap())
        }
        fn capture(&self) -> RetainedDirectoryPath {
            RetainedDirectoryPath::open(&self.0.join("leaf"), 128).unwrap()
        }
    }
    impl Drop for Fixture {
        fn drop(&mut self) {
            let _ = fs::remove_dir_all(&self.0);
        }
    }
    #[test]
    fn exact_path_policy_rejects_case_alias_before_and_after_observation() {
        let f = Fixture::new();
        let path = f.capture();
        let groups = BTreeSet::new();
        let uid = observe(&path).last().unwrap().metadata.uid;
        fs::rename(f.0.join("leaf"), f.0.join("LEAF")).unwrap();
        assert!(matches!(
            inspect_directory_path_with(&path, uid, &groups, || panic!("alias passed precheck")),
            Err(DirectoryPathRefusal::NameChanged)
        ));
        fs::rename(f.0.join("LEAF"), f.0.join("leaf")).unwrap();
        let result = inspect(|| {
            inspect_directory_path_with(&path, uid, &groups, || {
                fs::rename(f.0.join("leaf"), f.0.join("LEAF")).unwrap();
            })
        });
        assert!(matches!(result, Err(DirectoryPathRefusal::NameChanged)));
    }
    #[test]
    fn actual_chain_forwards_invoking_uid_without_an_owner_waiver() {
        let f = Fixture::new();
        let path = f.capture();
        let samples = observe(&path);
        let uid = samples.last().unwrap().metadata.uid;
        assert_ne!(
            uid, 0,
            "this native regression requires an unprivileged runner"
        );
        assert!(inspect(|| inspect_directory_path(&path, uid, &BTreeSet::new())).is_ok());
        let wrong = if uid == u32::MAX { uid - 1 } else { uid + 1 };
        // The real system ancestors of the ACL scratch base are not judged
        // (law 461; see `test_scratch::acl_scratch`).
        let first = samples
            .iter()
            .position(|o| {
                !crate::test_scratch::above_acl_scratch(o.metadata.device, o.metadata.inode)
                    && o.metadata.uid != 0
                    && o.metadata.uid != wrong
            })
            .unwrap();
        assert!(
            matches!(inspect(|| inspect_directory_path(&path, wrong, &BTreeSet::new())),
            Err(DirectoryPathRefusal::Predicate { component, refusal: Refusal::ForeignOwner }) if component == first)
        );
    }
    #[test]
    fn actual_chain_forwards_authorized_groups_to_a_middle_ancestor() {
        let f = Fixture::new();
        let path = f.capture();
        let samples = observe(&path);
        let uid = samples.last().unwrap().metadata.uid;
        assert!(inspect(|| inspect_directory_path(&path, uid, &BTreeSet::new())).is_ok());
        fs::set_permissions(&f.0, fs::Permissions::from_mode(0o770)).unwrap();
        let samples = observe(&path);
        let index = samples.len() - 2;
        let gid = samples[index].metadata.gid;
        assert!(
            matches!(inspect(|| inspect_directory_path(&path, uid, &BTreeSet::new())),
            Err(DirectoryPathRefusal::Predicate { component, refusal: Refusal::GroupWrite }) if component == index)
        );
        assert!(inspect(|| inspect_directory_path(&path, uid, &BTreeSet::from([gid]))).is_ok());
    }
    /// Law 461: the real `/` omits its ACL on a stock Mac, so the whole-path
    /// walk refuses there, with no extra authority, as unreadable rather than
    /// "no writers". Earlier refusals would still win (item 2), but root-owned
    /// `/` passes them.
    #[test]
    fn root_only_observation_refuses_the_omitted_acl_of_root() {
        let root = RetainedDirectoryPath::open(Path::new("/"), 0).unwrap();
        let samples = observe(&root);
        assert_eq!(samples.len(), 1);
        assert_eq!(samples[0].metadata.uid, 0);
        assert_eq!(samples[0].metadata.mode & 0o170000, 0o040000);
        assert_eq!(samples[0].acl, opensip_platform::DescriptorAcl::Omitted);
        assert!(matches!(
            inspect(|| inspect_directory_path(&root, 0, &BTreeSet::new())),
            Err(DirectoryPathRefusal::Predicate {
                component: 0,
                refusal: Refusal::AclUnreadable
            })
        ));
    }
    #[test]
    fn a_private_leaf_cannot_hide_a_writable_ancestor() {
        let f = Fixture::new();
        fs::set_permissions(&f.0, fs::Permissions::from_mode(0o702)).unwrap();
        let path = f.capture();
        let observations = observe(&path);
        let leaf = &observations.last().unwrap().metadata;
        assert_eq!(leaf.mode & 0o777, 0o700);
        // No sticky-directory exception or owner waiver. An earlier shared temp
        // ancestor may refuse first; success must never follow from the safe leaf.
        let error =
            inspect(|| inspect_directory_path(&path, leaf.uid, &BTreeSet::new())).unwrap_err();
        assert!(
            matches!(error,DirectoryPathRefusal::Predicate{component,refusal:Refusal::OthersWrite} if component<observations.len()-1)
        );
    }
    #[test]
    fn changed_names_stop_before_descriptor_observation_and_after_it() {
        let f = Fixture::new();
        let path = f.capture();
        fs::rename(f.0.join("leaf"), f.0.join("moved")).unwrap();
        let result = inspect_directory_path_with(&path, 0, &BTreeSet::new(), || {
            panic!("read after precheck failure")
        });
        assert!(matches!(result, Err(DirectoryPathRefusal::NameChanged)));
        fs::rename(f.0.join("moved"), f.0.join("leaf")).unwrap();
        let result = inspect(|| {
            inspect_directory_path_with(&path, 0, &BTreeSet::new(), || {
                fs::rename(f.0.join("leaf"), f.0.join("moved")).unwrap();
                fs::create_dir(f.0.join("leaf")).unwrap();
            })
        });
        assert!(matches!(result, Err(DirectoryPathRefusal::NameChanged)));
    }
    #[test]
    fn denied_ancestor_search_is_observation_failure_not_policy_success() {
        let f = Fixture::new();
        let path = f.capture();
        let uid = observe(&path).last().unwrap().metadata.uid;
        if uid == 0 {
            return;
        }
        fs::set_permissions(&f.0, fs::Permissions::from_mode(0o0)).unwrap();
        let result = inspect_directory_path(&path, uid, &BTreeSet::new());
        fs::set_permissions(&f.0, fs::Permissions::from_mode(0o700)).unwrap();
        assert!(
            matches!(result,Err(DirectoryPathRefusal::NameObservation(e)) if e.kind()==std::io::ErrorKind::PermissionDenied)
        );
    }
}

#[cfg(test)]
mod operational_chain_policy_tests {
    use super::*;
    use opensip_platform::{AclWriter, DescriptorAcl, DescriptorMetadata, DescriptorObservation};
    #[test]
    fn missing_chain_observation_never_passes_policy() {
        assert!(matches!(
            check_operational_chain_observations(&[], 42, &BTreeSet::new()),
            Err(DirectoryPathRefusal::EmptyChain)
        ));
    }
    fn sample() -> DescriptorObservation {
        DescriptorObservation {
            metadata: DescriptorMetadata {
                device: 1,
                inode: 2,
                mode: 0o40700,
                uid: 42,
                gid: 7,
                links: 1,
                size: 0,
                modified: (0, 0),
                changed: (0, 0),
                flags: 0,
            },
            acl: DescriptorAcl::Present(vec![]),
        }
    }
    fn writers(s: &mut DescriptorObservation) -> &mut Vec<AclWriter> {
        match &mut s.acl {
            DescriptorAcl::Present(writers) => writers,
            DescriptorAcl::Omitted => panic!("the sample's ACL is present"),
        }
    }
    fn assert_refusal(samples: &[DescriptorObservation], index: usize, expected: Refusal) {
        assert!(
            matches!(check_operational_chain_observations(samples,42,&BTreeSet::new()),
            Err(DirectoryPathRefusal::Predicate { component, refusal }) if component == index && refusal == expected)
        );
    }
    #[test]
    fn every_component_including_root_and_leaf_must_pass_each_predicate() {
        for index in 0..3 {
            for expected in [
                Refusal::ForeignOwner,
                Refusal::OthersWrite,
                Refusal::GroupWrite,
                Refusal::AclWrite,
                Refusal::NotDirectory,
                Refusal::Symlink,
            ] {
                let mut samples = vec![sample(), sample(), sample()];
                assert!(
                    check_operational_chain_observations(&samples, 42, &BTreeSet::new()).is_ok()
                );
                let s = &mut samples[index];
                match expected {
                    Refusal::ForeignOwner => s.metadata.uid = 43,
                    Refusal::OthersWrite => s.metadata.mode |= 0o002,
                    Refusal::GroupWrite => s.metadata.mode |= 0o020,
                    Refusal::AclWrite => writers(s).push(AclWriter::Unresolved),
                    Refusal::NotDirectory => s.metadata.mode = 0o100600,
                    Refusal::Symlink => s.metadata.mode = 0o120700,
                    _ => unreachable!(),
                }
                assert_refusal(&samples, index, expected);
            }
        }
    }
    #[test]
    fn uid_and_group_authorization_are_applied_at_every_component() {
        for index in 0..3 {
            let mut samples = vec![sample(), sample(), sample()];
            samples[index].metadata.uid = 0;
            samples[index].acl =
                DescriptorAcl::Present(vec![AclWriter::User(0), AclWriter::User(42)]);
            assert!(check_operational_chain_observations(&samples, 42, &BTreeSet::new()).is_ok());
            samples[index].metadata.mode |= 0o020;
            assert_refusal(&samples, index, Refusal::GroupWrite);
            writers(&mut samples[index]).push(AclWriter::Group(7));
            assert!(
                check_operational_chain_observations(&samples, 42, &BTreeSet::from([7])).is_ok()
            );
            assert!(
                matches!(check_operational_chain_observations(&samples,42,&BTreeSet::from([8])),
                Err(DirectoryPathRefusal::Predicate { component, refusal: Refusal::GroupWrite }) if component == index)
            );
            samples[index].metadata.mode &= !0o020;
            assert_refusal(&samples, index, Refusal::AclWrite);
            samples[index].acl = DescriptorAcl::Present(vec![AclWriter::User(43)]);
            assert_refusal(&samples, index, Refusal::AclWrite);
        }
    }
    /// Law 461 item 6: an omitted ACL is unreadable at the choke point in
    /// every scope, whatever `waive_owner` is, and never "no writers".
    #[test]
    fn an_omitted_acl_refuses_in_every_scope_and_with_waive_owner() {
        for (scope, mode) in [
            (Scope::Directory, 0o40700),
            (Scope::ConfigurationFile, 0o100600),
            (Scope::OperationalFile, 0o100600),
        ] {
            for waive_owner in [false, true] {
                let mut observed = sample();
                observed.metadata.mode = mode;
                assert_eq!(
                    check_descriptor_observation(
                        &observed,
                        scope,
                        42,
                        &BTreeSet::new(),
                        waive_owner
                    ),
                    Ok(())
                );
                observed.acl = DescriptorAcl::Omitted;
                assert_eq!(
                    check_descriptor_observation(
                        &observed,
                        scope,
                        42,
                        &BTreeSet::new(),
                        waive_owner
                    ),
                    Err(Refusal::AclUnreadable)
                );
                // Root ownership and every authorized group change nothing.
                observed.metadata.uid = 0;
                assert_eq!(
                    check_descriptor_observation(
                        &observed,
                        scope,
                        42,
                        &BTreeSet::from([7]),
                        waive_owner
                    ),
                    Err(Refusal::AclUnreadable)
                );
            }
        }
    }
    /// Law 461 item 2: the ACL arm keeps its place, so the kind, owner, mode
    /// and group refusals still win over an omitted ACL.
    #[test]
    fn an_omitted_acl_keeps_the_refusal_order() {
        let base = || {
            let mut observed = sample();
            observed.acl = DescriptorAcl::Omitted;
            observed
        };
        let refusal = |observed: &DescriptorObservation| {
            check_descriptor_observation(observed, Scope::Directory, 42, &BTreeSet::new(), false)
        };
        let mut observed = base();
        observed.metadata.mode = 0o100600;
        assert_eq!(refusal(&observed), Err(Refusal::NotDirectory));
        let mut observed = base();
        observed.metadata.uid = 43;
        assert_eq!(refusal(&observed), Err(Refusal::ForeignOwner));
        let mut observed = base();
        observed.metadata.mode |= 0o002;
        assert_eq!(refusal(&observed), Err(Refusal::OthersWrite));
        let mut observed = base();
        observed.metadata.mode |= 0o020;
        assert_eq!(refusal(&observed), Err(Refusal::GroupWrite));
        assert_eq!(refusal(&base()), Err(Refusal::AclUnreadable));
    }
    /// The production text of this file: every item under a `cfg(test)`
    /// attribute is removed by matching its braces, skipping string literals.
    fn production_source() -> String {
        let source = include_str!("custody.rs");
        let bytes = source.as_bytes();
        let mut kept = String::new();
        let mut at = 0;
        while let Some(found) = source[at..].find("#[cfg(") {
            let attr = at + found;
            let line_end = attr + source[attr..].find('\n').unwrap();
            if !source[attr..line_end].contains("test") {
                kept.push_str(&source[at..line_end]);
                at = line_end;
                continue;
            }
            kept.push_str(&source[at..attr]);
            let open = attr + source[attr..].find('{').unwrap();
            let (mut depth, mut i, mut in_string) = (0usize, open, false);
            loop {
                match bytes[i] {
                    b'\\' if in_string => i += 1,
                    // A char literal, plain or escaped (a lifetime has no
                    // closing quote two or three bytes on).
                    b'\'' if !in_string && bytes[i + 2] == b'\'' => i += 2,
                    b'\'' if !in_string && bytes[i + 1] == b'\\' && bytes[i + 3] == b'\'' => i += 3,
                    b'"' => in_string = !in_string,
                    b'{' if !in_string => depth += 1,
                    b'}' if !in_string => {
                        depth -= 1;
                        if depth == 0 {
                            break;
                        }
                    }
                    _ => {}
                }
                i += 1;
            }
            at = i + 1;
        }
        kept.push_str(&source[at..]);
        kept
    }
    /// The body of the named production function.
    fn body<'a>(production: &'a str, name: &str) -> &'a str {
        let start = production.find(&format!("fn {name}(")).unwrap();
        let end = start + production[start..].find("\n}\n").unwrap();
        &production[start..end]
    }
    /// Law 461 item 6: `AclWrite::Known` is built from a platform observation
    /// only through `DescriptorAcl::Present` at the choke point. The one named
    /// exception is `check_external_ancestor`'s order placeholder, whose ACL is
    /// judged afterwards from its capture by `external_ancestor_acl`.
    #[test]
    fn known_acl_writes_come_only_from_a_present_acl() {
        let production = production_source();
        let choke = body(&production, "check_descriptor_observation");
        let ancestor = body(&production, "check_external_ancestor");
        assert!(choke.contains("opensip_platform::DescriptorAcl::Omitted => AclWrite::Unreadable"));
        assert!(
            choke.contains("opensip_platform::DescriptorAcl::Present(writers) => AclWrite::Known(")
        );
        assert_eq!(choke.matches("AclWrite::Known(").count(), 1);
        assert_eq!(ancestor.matches("AclWrite::Known(").count(), 1);
        assert!(ancestor.contains("acl: AclWrite::Known(Vec::new()),"));
        // Every other occurrence is the pattern that reads a `Known` value.
        let constructions = production.matches("AclWrite::Known(").count();
        let reads = production.matches("AclWrite::Known(principals) =>").count();
        assert_eq!(constructions, 2 + reads);
        assert!(!production.contains("possible_acl_writers"));
    }
    #[test]
    fn first_refusing_component_is_reported_without_skipping_root() {
        let mut samples = vec![sample(), sample(), sample()];
        samples[0].metadata.uid = 43;
        samples[1].metadata.mode |= 0o002;
        assert_refusal(&samples, 0, Refusal::ForeignOwner);
        samples[0] = sample();
        assert_refusal(&samples, 1, Refusal::OthersWrite);
    }
}

/// Actual operational-file observation with S7 predicates. No owner waiver or
/// configuration-only byte cap; a consuming role still enforces its read bounds.
/// Supplied actor/group provenance, retained names/ancestors, native filesystem
/// qualification and the consuming lease remain required. This observes our own
/// descriptor, not a descriptor secretly held by SQLite, and grants no authority.
pub fn inspect_operational_file(
    file: &std::fs::File,
    invoking_uid: u32,
    authorized_groups: &BTreeSet<u32>,
) -> Result<opensip_platform::DescriptorObservation, NativeRefusal> {
    check_retained_descriptor(
        file,
        Scope::OperationalFile,
        invoking_uid,
        authorized_groups,
        false,
    )
}

#[cfg(test)]
mod operational_file_tests {
    use super::*;
    fn sample() -> EntryObservation {
        EntryObservation {
            kind: EntryKind::Regular,
            uid: 42,
            gid: 7,
            mode: 0o600,
            links: 1,
            size: MAX_CONFIG_BYTES + 1,
            acl: AclWrite::Known(vec![]),
        }
    }
    #[test]
    fn operational_file_has_no_config_cap_but_never_an_owner_waiver() {
        let mut e = sample();
        let groups = BTreeSet::new();
        for size in [MAX_CONFIG_BYTES, MAX_CONFIG_BYTES + 1, u64::MAX] {
            e.size = size;
            assert_eq!(
                check(Some(&e), Scope::OperationalFile, 42, &groups, false),
                Ok(())
            );
            assert_eq!(
                check(Some(&e), Scope::ConfigurationFile, 42, &groups, false),
                if size > MAX_CONFIG_BYTES {
                    Err(Refusal::TooLarge)
                } else {
                    Ok(())
                }
            );
        }
        e.uid = 43;
        for waiver in [false, true] {
            assert_eq!(
                check(Some(&e), Scope::OperationalFile, 42, &groups, waiver),
                Err(Refusal::ForeignOwner)
            );
        }
        e.uid = 0;
        assert_eq!(
            check(Some(&e), Scope::OperationalFile, 42, &groups, false),
            Ok(())
        );
        assert_eq!(
            check(None, Scope::OperationalFile, 42, &groups, false),
            Err(Refusal::Absent)
        );
    }
    #[test]
    fn operational_file_preserves_all_non_size_custody_refusals() {
        let groups = BTreeSet::new();
        for (kind, want) in [
            (EntryKind::Directory, Refusal::NotRegular),
            (EntryKind::Other, Refusal::NotRegular),
            (EntryKind::Symlink, Refusal::Symlink),
        ] {
            let mut e = sample();
            e.kind = kind;
            assert_eq!(
                check(Some(&e), Scope::OperationalFile, 42, &groups, false),
                Err(want)
            );
        }
        for links in [0, 2, u64::MAX] {
            let mut e = sample();
            e.links = links;
            assert_eq!(
                check(Some(&e), Scope::OperationalFile, 42, &groups, false),
                Err(if links == 0 {
                    Refusal::Unlinked
                } else {
                    Refusal::HardLinked
                })
            );
        }
        for (mode, want) in [(0o602, Refusal::OthersWrite), (0o620, Refusal::GroupWrite)] {
            let mut e = sample();
            e.mode = mode;
            assert_eq!(
                check(Some(&e), Scope::OperationalFile, 42, &groups, false),
                Err(want)
            );
        }
        for (acl, want) in [
            (AclWrite::Unreadable, Refusal::AclUnreadable),
            (
                AclWrite::Known(vec![Principal::Unresolved]),
                Refusal::AclWrite,
            ),
            (
                AclWrite::Known(vec![Principal::User(43)]),
                Refusal::AclWrite,
            ),
            (
                AclWrite::Known(vec![Principal::Group(7)]),
                Refusal::AclWrite,
            ),
        ] {
            let mut e = sample();
            e.acl = acl;
            assert_eq!(
                check(Some(&e), Scope::OperationalFile, 42, &groups, false),
                Err(want)
            );
        }
        let mut e = sample();
        e.mode = 0o620;
        e.acl = AclWrite::Known(vec![
            Principal::User(0),
            Principal::User(42),
            Principal::Group(7),
        ]);
        assert_eq!(
            check(
                Some(&e),
                Scope::OperationalFile,
                42,
                &BTreeSet::from([7]),
                false
            ),
            Ok(())
        );
    }
    #[cfg(target_os = "macos")]
    #[test]
    fn actual_sparse_operational_file_keeps_link_owner_and_mode_checks() {
        use std::fs;
        use std::os::unix::fs::{MetadataExt, OpenOptionsExt, PermissionsExt};
        let tag = opensip_identity::digest_hex(&opensip_identity::raw_sha256(
            &opensip_platform::request_entropy().unwrap(),
        ));
        let path = crate::test_scratch::acl_scratch().join(format!("opensip-operational198-{tag}"));
        let file = fs::OpenOptions::new()
            .create_new(true)
            .read(true)
            .write(true)
            .mode(0o600)
            .open(&path)
            .unwrap();
        struct Cleanup(std::path::PathBuf);
        impl Drop for Cleanup {
            fn drop(&mut self) {
                let _ = fs::remove_file(&self.0);
            }
        }
        let _cleanup = Cleanup(path.clone());
        file.set_len(MAX_CONFIG_BYTES + 1).unwrap();
        let uid = file.metadata().unwrap().uid();
        assert_ne!(
            uid, 0,
            "native permission qualification requires an unprivileged process"
        );
        let groups = BTreeSet::new();
        let observed = inspect_operational_file(&file, uid, &groups).unwrap();
        assert_eq!(observed.metadata.size, MAX_CONFIG_BYTES + 1);
        assert!(matches!(
            check_retained_descriptor(&file, Scope::ConfigurationFile, uid, &groups, false),
            Err(NativeRefusal::Predicate(Refusal::TooLarge))
        ));
        assert!(matches!(
            inspect_operational_file(&file, uid.checked_add(1).unwrap(), &groups),
            Err(NativeRefusal::Predicate(Refusal::ForeignOwner))
        ));
        file.set_permissions(fs::Permissions::from_mode(0o602))
            .unwrap();
        assert!(matches!(
            inspect_operational_file(&file, uid, &groups),
            Err(NativeRefusal::Predicate(Refusal::OthersWrite))
        ));
        file.set_permissions(fs::Permissions::from_mode(0o600))
            .unwrap();
        let link = path.with_extension("link");
        fs::hard_link(&path, &link).unwrap();
        let _linked = Cleanup(link);
        assert!(matches!(
            inspect_operational_file(&file, uid, &groups),
            Err(NativeRefusal::Predicate(Refusal::HardLinked))
        ));
        fs::remove_file(&_linked.0).unwrap();
        fs::remove_file(&path).unwrap();
        assert!(matches!(
            inspect_operational_file(&file, uid, &groups),
            Err(NativeRefusal::Predicate(Refusal::Unlinked))
        ));
    }
    #[cfg(target_os = "macos")]
    #[test]
    fn retained_capture_checks_policy_on_the_read_file_not_a_replacement() {
        use std::{
            fs,
            os::unix::fs::{MetadataExt, PermissionsExt},
        };
        let tag = opensip_identity::digest_hex(&opensip_identity::raw_sha256(
            &opensip_platform::request_entropy().unwrap(),
        ));
        let path = crate::test_scratch::acl_scratch().join(format!("opensip-retained205-{tag}"));
        fs::create_dir(&path).unwrap();
        struct Cleanup(std::path::PathBuf);
        impl Drop for Cleanup {
            fn drop(&mut self) {
                let _ = fs::remove_dir_all(&self.0);
            }
        }
        let f = Cleanup(fs::canonicalize(path).unwrap());
        let original = f.0.join("witness");
        let moved = f.0.join("retained");
        fs::write(&original, b"observed original").unwrap();
        fs::set_permissions(&original, fs::Permissions::from_mode(0o600)).unwrap();
        let root = opensip_platform::RetainedDirectoryPath::open(&f.0, 128).unwrap();
        let crate::OperationalFileObservation::Present(captured) =
            crate::observe_bound_operational_file(&root, "witness", 128)
        else {
            panic!("capture required")
        };
        // Bounded capture consumed to EOF to decide that these are complete
        // bytes. Reopening in any outer wrapper would give offset zero instead.
        use std::io::Seek;
        let mut descriptor = captured.file();
        assert_eq!(
            descriptor.stream_position().unwrap(),
            captured.bytes().len() as u64
        );
        let uid = captured.file().metadata().unwrap().uid();
        assert_ne!(uid, 0);
        let groups = BTreeSet::new();
        crate::inspect_operational_file_policy(captured.file(), uid, &groups).unwrap();
        fs::rename(&original, &moved).unwrap();
        fs::write(&original, b"replacement").unwrap();
        fs::set_permissions(&original, fs::Permissions::from_mode(0o600)).unwrap();
        fs::set_permissions(&moved, fs::Permissions::from_mode(0o602)).unwrap();
        assert_eq!(captured.bytes(), b"observed original");
        assert!(matches!(
            crate::inspect_operational_file_policy(captured.file(), uid, &groups),
            Err(NativeRefusal::Predicate(Refusal::OthersWrite))
        ));
        let replacement = fs::File::open(&original).unwrap();
        inspect_operational_file(&replacement, uid, &groups).unwrap();
        assert_ne!(
            captured.file().metadata().unwrap().ino(),
            replacement.metadata().unwrap().ino()
        );
        fs::set_permissions(&moved, fs::Permissions::from_mode(0o600)).unwrap();
        fs::hard_link(&moved, f.0.join("second-link")).unwrap();
        assert!(matches!(
            crate::inspect_operational_file_policy(captured.file(), uid, &groups),
            Err(NativeRefusal::Predicate(Refusal::HardLinked))
        ));
        fs::remove_file(f.0.join("second-link")).unwrap();
        fs::remove_file(&moved).unwrap();
        assert!(matches!(
            crate::inspect_operational_file_policy(captured.file(), uid, &groups),
            Err(NativeRefusal::Predicate(Refusal::Unlinked))
        ));
        // The replacement is still readable and policy-admissible: reopening it
        // would have hidden all three refusals on the object that supplied bytes.
        inspect_operational_file(&replacement, uid, &groups).unwrap();
    }
}

pub(crate) mod directory_policy {
    include!("custody/directory_policy.rs");
}

pub(crate) mod installation_fence {
    include!("custody/installation_fence.rs");
}

pub(crate) mod initial_manifest {
    include!("custody/initial_manifest.rs");
}

#[cfg(target_os = "macos")]
pub(crate) mod installation_root {
    include!("custody/installation_root.rs");
}
#[cfg(target_os = "macos")]
pub(crate) mod installation_parent {
    include!("custody/installation_parent.rs");
}
#[cfg(target_os = "macos")]
pub(crate) mod installation_stage {
    include!("custody/installation_stage.rs");
}
#[cfg(target_os = "macos")]
pub(crate) mod installation_publication {
    include!("custody/installation_publication.rs");
}
#[cfg(target_os = "macos")]
pub(crate) mod installation_admission {
    include!("custody/installation_admission.rs");
}
#[cfg(target_os = "macos")]
pub(crate) mod installation_routing {
    include!("custody/installation_routing.rs");
}
#[cfg(target_os = "macos")]
pub(crate) mod read_premise {
    include!("custody/read_premise.rs");
}
#[cfg(target_os = "macos")]
pub(crate) mod ordinary_writer {
    include!("custody/ordinary_writer.rs");
}
#[cfg(target_os = "macos")]
pub(crate) mod installation_session {
    include!("custody/installation_session.rs");
}
#[cfg(target_os = "macos")]
pub(crate) mod installation_read {
    include!("custody/installation_read.rs");
}
#[cfg(target_os = "macos")]
pub(crate) mod installation_doctor {
    include!("custody/installation_doctor.rs");
}
#[cfg(target_os = "macos")]
pub(crate) mod store_endpoint {
    include!("custody/store_endpoint.rs");
}
#[cfg(target_os = "macos")]
pub(crate) mod project_chain {
    include!("custody/project_chain.rs");
}
#[cfg(target_os = "macos")]
pub(crate) mod project_admission {
    include!("custody/project_admission.rs");
}
#[cfg(target_os = "macos")]
pub(crate) mod git_tracking {
    include!("custody/git_tracking.rs");
}
#[cfg(target_os = "macos")]
pub(crate) mod first_registration {
    include!("custody/first_registration.rs");
}
#[cfg(target_os = "macos")]
pub(crate) mod namespace_lease {
    include!("custody/namespace_lease.rs");
}
#[cfg(target_os = "macos")]
pub(crate) mod operation_handoff {
    include!("custody/operation_handoff.rs");
}
#[cfg(target_os = "macos")]
pub(crate) mod operation_guard {
    include!("custody/operation_guard.rs");
}
#[cfg(target_os = "macos")]
pub(crate) mod commit_session {
    include!("custody/commit_session.rs");
}
#[cfg(target_os = "macos")]
pub(crate) mod recovery_admission {
    include!("custody/recovery_admission.rs");
}
#[cfg(target_os = "macos")]
pub(crate) mod settlement_sweep {
    include!("custody/settlement_sweep.rs");
}
// M3-B r5 items 13 and 14 (unit B2-a): the shared discovery rule, pure.
// No consumer yet: B2-b uses it in this crate, and B2-c exports it.
#[allow(dead_code)]
pub(crate) mod discovery_rule {
    include!("custody/discovery_rule.rs");
}
// M3-B r5 item 13 (unit B2-b2): the pure discovery core over an observed
// scope. No consumer yet: the walker (B2-b3) supplies its scope.
#[cfg(target_os = "macos")]
#[allow(dead_code)]
pub(crate) mod discovery_scan {
    include!("custody/discovery_scan.rs");
}
// M3-B r5 items 12 and 13 (unit B2-b3b): the S3 downward walker over a lent
// discovery root. No production caller yet: J1 composes it.
#[cfg(target_os = "macos")]
#[allow(dead_code)]
pub(crate) mod discovery_walk {
    include!("custody/discovery_walk.rs");
}
// M3-B r9 items 19 to 24 (unit B3-b2b1): the D15 readers and membership
// decision core. No consumer yet: B3-b2b2 composes it with the native
// observation.
#[cfg(target_os = "macos")]
#[allow(dead_code)]
pub(crate) mod workspace_declarations {
    include!("custody/workspace_declarations.rs");
}
// M3-B r9 items 19 to 24 (unit B3-b2b2b): the native workspace observation
// and the D15 discovery composition. No production caller yet: J1 composes
// it; the scenario path calls it.
#[cfg(target_os = "macos")]
#[allow(dead_code)]
pub(crate) mod workspace_observation {
    include!("custody/workspace_observation.rs");
}
#[cfg(target_os = "macos")]
#[allow(dead_code)]
pub(crate) mod workspace_discovery {
    include!("custody/workspace_discovery.rs");
}
// M3-B r5 item 12 (unit B2-b4a): the T2 census's soundness control and
// margin record (tools/security/discovery_census.py).
#[cfg(all(test, target_os = "macos"))]
mod discovery_census_tests {
    include!("custody/discovery_census_tests.rs");
}
#[cfg(all(
    any(test, feature = "crash-matrix", feature = "scenario-fixtures"),
    target_os = "macos"
))]
#[cfg_attr(not(test), allow(dead_code, unused_imports))]
pub(crate) mod installation_read_fixture {
    include!("custody/installation_read_fixture.rs");
}

#[cfg(test)]
mod core_tree_tests {
    use super::*;
    use crate::private_access::{ACE_DENY, ACE_PERMIT};
    use opensip_platform::{
        CapturedAclEntry, CapturedAclPrincipal, CapturedAclState, DescriptorMetadata,
    };
    const OWNER: u32 = 777;
    const WRITE: u32 = 1 << 2;
    const INHERIT_ONLY: u32 = 1 << 8;
    fn member(kind: u32, uid: u32, permissions: u32, links: u64) -> DescriptorMetadata {
        DescriptorMetadata {
            device: 1,
            inode: 2,
            mode: kind | permissions,
            uid,
            gid: 20,
            links,
            size: 96,
            modified: (0, 0),
            changed: (0, 0),
            flags: 0,
        }
    }
    fn dir(uid: u32, permissions: u32) -> DescriptorMetadata {
        member(0o040000, uid, permissions, 3)
    }
    fn file(uid: u32, permissions: u32, links: u64) -> DescriptorMetadata {
        member(0o100000, uid, permissions, links)
    }
    fn ace(
        kind: u32,
        flags: u32,
        rights: u32,
        principal: CapturedAclPrincipal,
    ) -> CapturedAclEntry {
        CapturedAclEntry {
            flags: kind | flags,
            rights,
            principal,
        }
    }
    fn judge(
        metadata: &DescriptorMetadata,
        kind: CoreTreeKind,
        entries: &[CapturedAclEntry],
    ) -> Result<(), Refusal> {
        check_core_tree_member(
            metadata,
            kind,
            CapturedAclState::Entries(entries.len()),
            |index| entries.get(index).copied(),
        )
    }

    #[test]
    fn any_owner_or_root_with_a_present_acl_is_admitted() {
        for uid in [OWNER, 0, 501] {
            assert_eq!(
                judge(&dir(uid, 0o755), CoreTreeKind::Directory, &[]),
                Ok(())
            );
            assert_eq!(
                judge(&file(uid, 0o755, 1), CoreTreeKind::Regular, &[]),
                Ok(())
            );
            // Explicit zero-rights and owner write grants do not refuse.
            let own = ace(ACE_PERMIT, 0, WRITE, CapturedAclPrincipal::User(uid));
            let root = ace(ACE_PERMIT, 0, WRITE, CapturedAclPrincipal::User(0));
            assert_eq!(
                judge(&dir(uid, 0o755), CoreTreeKind::Directory, &[own, root]),
                Ok(())
            );
        }
    }

    #[test]
    fn omission_and_sentinel_refuse() {
        for state in [
            CapturedAclState::NotReturned,
            CapturedAclState::NoAclSentinel,
        ] {
            for (metadata, kind) in [
                (dir(OWNER, 0o755), CoreTreeKind::Directory),
                (file(OWNER, 0o755, 1), CoreTreeKind::Regular),
            ] {
                assert_eq!(
                    check_core_tree_member(&metadata, kind, state, |_| None),
                    Err(Refusal::AclUnreadable)
                );
            }
        }
    }

    #[test]
    fn a_write_grant_to_anyone_else_refuses_including_inherit_only() {
        for principal in [
            CapturedAclPrincipal::User(502),
            CapturedAclPrincipal::Group(20),
            CapturedAclPrincipal::Group(0),
            CapturedAclPrincipal::Unresolved,
        ] {
            for flags in [0, INHERIT_ONLY] {
                let grant = ace(ACE_PERMIT, flags, WRITE, principal);
                assert_eq!(
                    judge(&dir(OWNER, 0o755), CoreTreeKind::Directory, &[grant]),
                    Err(Refusal::AclWrite)
                );
            }
            // Deny and read-only allows pass.
            let deny = ace(ACE_DENY, 0, WRITE, principal);
            let read = ace(ACE_PERMIT, 0, 1 << 1, principal);
            assert_eq!(
                judge(&file(OWNER, 0o755, 1), CoreTreeKind::Regular, &[deny, read]),
                Ok(())
            );
        }
    }

    #[test]
    fn kind_mode_and_links_refuse_before_the_acl() {
        let cases = [
            (
                dir(OWNER, 0o757),
                CoreTreeKind::Directory,
                Refusal::OthersWrite,
            ),
            (
                dir(OWNER, 0o775),
                CoreTreeKind::Directory,
                Refusal::GroupWrite,
            ),
            (
                file(OWNER, 0o775, 1),
                CoreTreeKind::Regular,
                Refusal::GroupWrite,
            ),
            (
                file(OWNER, 0o755, 2),
                CoreTreeKind::Regular,
                Refusal::HardLinked,
            ),
            (
                file(OWNER, 0o755, 0),
                CoreTreeKind::Regular,
                Refusal::Unlinked,
            ),
            (
                file(OWNER, 0o755, 1),
                CoreTreeKind::Directory,
                Refusal::NotDirectory,
            ),
            (
                dir(OWNER, 0o755),
                CoreTreeKind::Regular,
                Refusal::NotRegular,
            ),
            (
                member(0o120000, OWNER, 0o755, 1),
                CoreTreeKind::Regular,
                Refusal::Symlink,
            ),
            (
                member(0o120000, OWNER, 0o755, 1),
                CoreTreeKind::Directory,
                Refusal::Symlink,
            ),
        ];
        for (metadata, kind, expected) in cases {
            assert_eq!(
                check_core_tree_member(&metadata, kind, CapturedAclState::NotReturned, |_| None),
                Err(expected)
            );
        }
    }
}
