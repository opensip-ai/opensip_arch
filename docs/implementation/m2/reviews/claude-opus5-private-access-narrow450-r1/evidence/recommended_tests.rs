
// Reviewer-authored recommended tests (actual Claude Opus 5.5). Appended ONLY to the
// review-directory copy to validate observation O1; never part of the subject.
// Type mismatches use the OTHER kind's exact permissions so only the type check refuses.
#[cfg(test)]
mod reviewer_recommended {
    use super::*;

    fn meta(mode: u32) -> DescriptorMetadata {
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

    fn judge(kind: PrivateObjectKind, mode: u32) -> Result<(), PrivateAccessRefusal> {
        assess_private_descendant(kind, 10, &meta(mode), CapturedAclState::Entries(0), &[])
    }

    #[test]
    fn reviewer_type_mismatch_with_matching_permissions_refuses() {
        assert_eq!(judge(PrivateObjectKind::Directory, REGULAR | 0o700), Err(PrivateAccessRefusal::ModeShape));
        assert_eq!(judge(PrivateObjectKind::RegularFile, DIRECTORY | 0o600), Err(PrivateAccessRefusal::ModeShape));
    }

    #[test]
    fn reviewer_file_mode_is_exact() {
        for permissions in [0o4600, 0o2600, 0o1600, 0o400] {
            assert_eq!(judge(PrivateObjectKind::RegularFile, REGULAR | permissions), Err(PrivateAccessRefusal::ModeShape));
        }
        assert_eq!(judge(PrivateObjectKind::RegularFile, REGULAR | 0o600), Ok(()));
    }
}
