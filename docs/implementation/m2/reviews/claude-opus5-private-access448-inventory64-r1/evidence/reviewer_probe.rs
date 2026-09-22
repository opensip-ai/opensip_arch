
// Reviewer-authored native probe (actual Claude Opus 5.5). Appended ONLY to the
// review-directory copy of private_access.rs, run once, then removed. Real ACEs are
// installed with /bin/chmod +a on scratch objects under the review TMPDIR and read
// back through the reviewed capture and predicate. Prints states/decisions only;
// no uid, name or UUID is printed.
#[cfg(all(test, target_os = "macos"))]
mod reviewer_probe {
    use super::*;
    use opensip_platform::{WorkLedger, capture_descriptor_acl_accounted};
    use std::fs::{self, File};
    use std::os::unix::fs::{MetadataExt, OpenOptionsExt, PermissionsExt};
    use std::path::{Path, PathBuf};
    use std::process::Command;

    struct Root(PathBuf);
    impl Drop for Root {
        fn drop(&mut self) {
            let _ = Command::new("/bin/chmod").arg("-RN").arg(&self.0).status();
            let _ = fs::remove_dir_all(&self.0);
        }
    }
    fn chmod(args: &[&str], path: &Path) {
        let status = Command::new("/bin/chmod").args(args).arg(path).status().unwrap();
        assert!(status.success(), "chmod {args:?} failed");
    }
    type Got = (CapturedAclState, Result<(), PrivateAccessRefusal>);
    fn judge(case: &str, kind: PrivateObjectKind, file: &File, uid: u32) -> Got {
        let mut owner = WorkLedger::new();
        let sample = owner.scope(|w| capture_descriptor_acl_accounted(file, w)).unwrap();
        let got = (sample.acl_state(), assess_private_descendant_capture(kind, uid, &sample));
        println!("PROBE {{\"case\":\"{case}\",\"state\":\"{:?}\",\"decision\":\"{:?}\"}}", got.0, got.1);
        got
    }
    fn consistent(got: Got) -> bool {
        match got.0 {
            CapturedAclState::NotReturned => got.1 == Err(PrivateAccessRefusal::AclNotReturned),
            CapturedAclState::NoAclSentinel => got.1 == Err(PrivateAccessRefusal::AclSentinelUnqualified),
            CapturedAclState::Entries(_) => true,
        }
    }

    #[test]
    fn reviewer_probe_real_aces_through_capture() {
        use CapturedAclState::Entries;
        use PrivateAccessRefusal::{ForeignAclAccess, ModeShape};
        let nonce = opensip_platform::request_entropy().unwrap();
        let name: String = nonce.iter().map(|b| format!("{b:02x}")).collect();
        let root = Root(std::env::temp_dir().join(format!("reviewer-probe-{name}")));
        fs::create_dir(&root.0).unwrap();
        fs::set_permissions(&root.0, fs::Permissions::from_mode(0o700)).unwrap();
        let path = root.0.join("record");
        let file = fs::OpenOptions::new().read(true).write(true).create_new(true).mode(0o600).open(&path).unwrap();
        let uid = file.metadata().unwrap().uid();
        let me = String::from_utf8(Command::new("/usr/bin/id").arg("-un").output().unwrap().stdout).unwrap();
        let me = me.trim();
        let f = PrivateObjectKind::RegularFile;

        assert!(consistent(judge("F0 fresh 0600 file", f, &file, uid)));
        chmod(&["+a", "group:everyone deny delete"], &path);
        assert_eq!(judge("F1 everyone deny delete", f, &file, uid), (Entries(1), Ok(())));
        chmod(&["+a", "group:staff allow read"], &path);
        assert_eq!(judge("F2 plus group allow read", f, &file, uid), (Entries(2), Err(ForeignAclAccess)));
        chmod(&["-N"], &path);
        assert!(consistent(judge("F3 after chmod -N", f, &file, uid)));
        chmod(&["+a", &format!("user:{me} allow read,write")], &path);
        assert_eq!(judge("F4 invoking user allow read,write", f, &file, uid), (Entries(1), Ok(())));
        chmod(&["+a", "user:nobody allow read"], &path);
        assert_eq!(judge("F5 plus other user allow read", f, &file, uid), (Entries(2), Err(ForeignAclAccess)));
        chmod(&["-N"], &path);
        chmod(&["+a", "group:everyone allow readsecurity"], &path);
        assert_eq!(judge("F6 everyone allow readsecurity only", f, &file, uid), (Entries(1), Err(ForeignAclAccess)));
        chmod(&["-N"], &path);
        chmod(&["0640"], &path);
        chmod(&["+a", "group:everyone deny delete"], &path);
        assert_eq!(judge("F7 mode 0640 with present ACL", f, &file, uid), (Entries(1), Err(ModeShape)));
        chmod(&["0600"], &path);
        chmod(&["-N"], &path);

        let d = PrivateObjectKind::Directory;
        let dir = File::open(&root.0).unwrap();
        assert!(consistent(judge("D0 fresh 0700 directory", d, &dir, uid)));
        chmod(&["+a", "group:staff allow list,file_inherit,only_inherit"], &root.0);
        assert_eq!(judge("D1 group inherit-only allow list", d, &dir, uid), (Entries(1), Err(ForeignAclAccess)));
        chmod(&["-N"], &root.0);
        chmod(&["+a", &format!("user:{me} allow list,search,add_file")], &root.0);
        assert_eq!(judge("D2 invoking user allow list,search,add_file", d, &dir, uid), (Entries(1), Ok(())));
        chmod(&["-N"], &root.0);
        chmod(&["+a", "group:everyone deny delete_child"], &root.0);
        assert_eq!(judge("D3 everyone deny delete_child", d, &dir, uid), (Entries(1), Ok(())));
        assert_eq!(judge("D4 directory judged as regular file", f, &dir, uid), (Entries(1), Err(ModeShape)));
    }
}
