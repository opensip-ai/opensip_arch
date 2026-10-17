// Unit C1a2's custody controls (C1a plan r4, C1a2): a private 0700 scratch
// directory per test stands in for J1's custody location.
use super::*;
use opensip_platform::WorkLedger;
use std::os::unix::fs::{MetadataExt, PermissionsExt};
use std::path::{Path, PathBuf};

struct Scratch(PathBuf);
impl Drop for Scratch {
    fn drop(&mut self) {
        let _ = std::process::Command::new("/bin/chmod")
            .args(["-R", "u+rwX"])
            .arg(&self.0)
            .stderr(std::process::Stdio::null())
            .status();
        let _ = std::fs::remove_dir_all(&self.0);
    }
}
fn scratch() -> (Scratch, PathBuf) {
    let nonce: String = opensip_platform::request_entropy()
        .unwrap()
        .iter()
        .map(|b| format!("{b:02x}"))
        .collect();
    let base = std::env::temp_dir().join(format!("opensip-c1a2-custody-{nonce}"));
    std::fs::create_dir(&base).unwrap();
    std::fs::set_permissions(&base, std::fs::Permissions::from_mode(0o700)).unwrap();
    let base = std::fs::canonicalize(&base).unwrap();
    let dir = base.join("custody");
    std::fs::create_dir(&dir).unwrap();
    std::fs::set_permissions(&dir, std::fs::Permissions::from_mode(0o700)).unwrap();
    (Scratch(base), dir)
}
fn retained(dir: &Path) -> RetainedDirectory {
    RetainedDirectory::from_retained_handle(File::open(dir).unwrap()).unwrap()
}
fn uid(dir: &Path) -> u32 {
    std::fs::metadata(dir).unwrap().uid()
}
fn custody(dir: &Path, work: &mut WorkScope<'_>) -> CandidateCustody {
    CandidateCustody::new(retained(dir), uid(dir), work).unwrap()
}
fn store(
    custody: &mut CandidateCustody,
    chunks: &[&[u8]],
    work: &mut WorkScope<'_>,
) -> Result<Custodied, CustodyFailure> {
    let total = chunks.iter().map(|c| c.len() as u64).sum();
    let mut pending = custody.begin(total, work)?;
    for chunk in chunks {
        pending.write(chunk, work)?;
    }
    pending.commit(work)
}
fn sha(bytes: &[u8]) -> [u8; 32] {
    RawSha256::new().update(bytes).unwrap().finish()
}
fn entries(dir: &Path) -> Vec<String> {
    let mut names: Vec<String> = std::fs::read_dir(dir)
        .unwrap()
        .map(|e| e.unwrap().file_name().into_string().unwrap())
        .collect();
    names.sort();
    names
}

#[test]
fn a_blob_is_committed_under_its_digest_hex_and_opened_verified() {
    let (_s, dir) = scratch();
    WorkLedger::discovery_profile()
        .scope(|work| {
            let mut custody = custody(&dir, work);
            let blob = store(&mut custody, &[b"hello ", b"world"], work).unwrap();
            assert_eq!(blob.sha256, sha(b"hello world"));
            assert_eq!((blob.bytes, blob.duplicate), (11, false));
            let hex = digest_hex(&blob.sha256);
            assert_eq!(entries(&dir), std::slice::from_ref(&hex));
            let meta = std::fs::symlink_metadata(dir.join(&hex)).unwrap();
            assert!(meta.file_type().is_file());
            assert_eq!(meta.mode() & 0o7777, 0o600);
            let mut buffer = vec![0; VERIFY_CHUNK];
            let mut file = custody.open(&blob.sha256, &mut buffer, work).unwrap();
            let mut bytes = Vec::new();
            file.read_to_end(&mut bytes).unwrap();
            assert_eq!(bytes, b"hello world");
            Ok::<_, CustodyFailure>(())
        })
        .unwrap();
}

#[test]
fn an_existing_digest_is_kept_and_a_duplicate_is_resolved_without_a_reread() {
    // LD-C1A-9: the second commit of the same bytes stores nothing new and
    // reads nothing. The committed file is made unreadable first, so any
    // read of it would fail the duplicate's commit.
    let (_s, dir) = scratch();
    WorkLedger::discovery_profile()
        .scope(|work| {
            let mut custody = custody(&dir, work);
            let first = store(&mut custody, &[b"same bytes"], work).unwrap();
            let hex = digest_hex(&first.sha256);
            let inode = std::fs::metadata(dir.join(&hex)).unwrap().ino();
            std::fs::set_permissions(dir.join(&hex), std::fs::Permissions::from_mode(0o000))
                .unwrap();
            let second = store(&mut custody, &[b"same ", b"bytes"], work).unwrap();
            assert_eq!(second.sha256, first.sha256);
            assert!(second.duplicate);
            assert_eq!(custody.blob_count(), 1);
            // The pending entry is gone and the original is untouched.
            assert_eq!(entries(&dir), std::slice::from_ref(&hex));
            std::fs::set_permissions(dir.join(&hex), std::fs::Permissions::from_mode(0o600))
                .unwrap();
            assert_eq!(std::fs::metadata(dir.join(&hex)).unwrap().ino(), inode);
            Ok::<_, CustodyFailure>(())
        })
        .unwrap();
}

#[test]
fn a_corrupted_custody_file_is_refused_at_open() {
    for (case, damage) in [
        (
            "digest",
            &(|p: &Path| std::fs::write(p, b"HELLO").unwrap()) as &dyn Fn(&Path),
        ),
        ("length", &|p: &Path| std::fs::write(p, b"hell").unwrap()),
        ("kind, mode or owner", &|p: &Path| {
            std::fs::set_permissions(p, std::fs::Permissions::from_mode(0o644)).unwrap()
        }),
    ] {
        let (_s, dir) = scratch();
        let result = WorkLedger::discovery_profile().scope(|work| {
            let mut custody = custody(&dir, work);
            let blob = store(&mut custody, &[b"hello"], work).unwrap();
            damage(&dir.join(digest_hex(&blob.sha256)));
            let mut buffer = vec![0; VERIFY_CHUNK];
            custody.open(&blob.sha256, &mut buffer, work).map(drop)
        });
        match result {
            Err(WorkFailure::Operation(CustodyError::Corrupted(why))) => assert_eq!(why, case),
            other => panic!("{case}: {other:?}"),
        }
    }
}

#[test]
fn a_length_mismatch_refuses_at_the_write_or_the_commit() {
    let (_s, dir) = scratch();
    let short = WorkLedger::discovery_profile().scope(|work| {
        let mut custody = custody(&dir, work);
        let mut pending = custody.begin(5, work)?;
        pending.write(b"abc", work)?;
        pending.commit(work)
    });
    assert!(
        matches!(
            short,
            Err(WorkFailure::Operation(CustodyError::LengthMismatch {
                expected: 5,
                written: 3
            }))
        ),
        "{short:?}"
    );
    let (_s, dir) = scratch();
    let long = WorkLedger::discovery_profile().scope(|work| {
        let mut custody = custody(&dir, work);
        let mut pending = custody.begin(2, work)?;
        pending.write(b"abc", work)?;
        pending.commit(work)
    });
    assert!(
        matches!(
            long,
            Err(WorkFailure::Operation(CustodyError::LengthMismatch {
                expected: 2,
                written: 3
            }))
        ),
        "{long:?}"
    );
}

#[test]
fn the_custody_directory_must_be_a_private_empty_directory_of_the_user() {
    let (_s, dir) = scratch();
    std::fs::set_permissions(&dir, std::fs::Permissions::from_mode(0o755)).unwrap();
    let open = WorkLedger::discovery_profile()
        .scope(|work| CandidateCustody::new(retained(&dir), uid(&dir), work).map(drop));
    assert!(
        matches!(
            open,
            Err(WorkFailure::Operation(CustodyError::Directory(_)))
        ),
        "{open:?}"
    );
    std::fs::set_permissions(&dir, std::fs::Permissions::from_mode(0o700)).unwrap();
    let other = WorkLedger::discovery_profile()
        .scope(|work| CandidateCustody::new(retained(&dir), uid(&dir) + 1, work).map(drop));
    assert!(
        matches!(
            other,
            Err(WorkFailure::Operation(CustodyError::Directory(_)))
        ),
        "{other:?}"
    );
    std::fs::write(dir.join("left-over"), b"x").unwrap();
    let full = WorkLedger::discovery_profile()
        .scope(|work| CandidateCustody::new(retained(&dir), uid(&dir), work).map(drop));
    assert!(
        matches!(
            full,
            Err(WorkFailure::Operation(CustodyError::Directory("not empty")))
        ),
        "{full:?}"
    );
}

#[test]
fn a_digest_this_invocation_never_committed_is_not_opened() {
    let (_s, dir) = scratch();
    let result = WorkLedger::discovery_profile().scope(|work| {
        let custody = custody(&dir, work);
        let mut buffer = vec![0; VERIFY_CHUNK];
        custody.open(&sha(b"never"), &mut buffer, work).map(drop)
    });
    assert!(
        matches!(
            result,
            Err(WorkFailure::Operation(CustodyError::NotCommitted))
        ),
        "{result:?}"
    );
}
