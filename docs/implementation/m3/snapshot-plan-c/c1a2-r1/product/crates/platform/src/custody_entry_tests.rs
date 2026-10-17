// Unit C1a2's controls for the custody entry primitives: the rename never
// replaces, and both are charged before any native call.
use super::*;
use crate::WorkLedger;
use std::fs::File;
use std::os::unix::fs::PermissionsExt;
use std::path::PathBuf;

struct Scratch(PathBuf);
impl Drop for Scratch {
    fn drop(&mut self) {
        let _ = std::fs::remove_dir_all(&self.0);
    }
}
fn scratch() -> (Scratch, RetainedDirectory) {
    let mut bytes = [0u8; 8];
    getrandom::fill(&mut bytes).unwrap();
    let hex: String = bytes.iter().map(|b| format!("{b:02x}")).collect();
    let dir = std::env::temp_dir().join(format!("opensip-custody-entry-{hex}"));
    std::fs::create_dir(&dir).unwrap();
    std::fs::set_permissions(&dir, std::fs::Permissions::from_mode(0o700)).unwrap();
    let retained = RetainedDirectory::from_retained_handle(File::open(&dir).unwrap()).unwrap();
    (Scratch(dir), retained)
}

#[test]
fn the_exclusive_rename_moves_to_a_free_name_and_never_replaces() {
    let (s, dir) = scratch();
    std::fs::write(s.0.join("pending-0"), b"new").unwrap();
    std::fs::write(s.0.join("taken"), b"old").unwrap();
    let mut ledger = WorkLedger::discovery_profile();
    let outcomes = ledger
        .scope(|work| {
            let onto_taken = dir.rename_exclusive_accounted("pending-0", "taken", work)?;
            let onto_free = dir.rename_exclusive_accounted("pending-0", "free", work)?;
            Ok::<_, WorkFailure<io::Error>>((onto_taken, onto_free))
        })
        .unwrap();
    assert_eq!(
        outcomes,
        (
            ExclusiveRenameOutcome::EntryExists,
            ExclusiveRenameOutcome::Renamed
        )
    );
    assert_eq!(std::fs::read(s.0.join("taken")).unwrap(), b"old");
    assert_eq!(std::fs::read(s.0.join("free")).unwrap(), b"new");
    assert!(!s.0.join("pending-0").exists());
    // Charged exactly twice, before each call.
    let one = rename_exclusive_cost("pending-0", "taken");
    let two = rename_exclusive_cost("pending-0", "free");
    let used = ledger.used();
    assert_eq!(
        (used.objects, used.edges, used.bytes),
        (
            one.objects + two.objects,
            one.edges + two.edges,
            one.bytes + two.bytes
        )
    );
}

#[test]
fn the_unlink_removes_one_entry_and_names_are_single_components() {
    let (s, dir) = scratch();
    std::fs::write(s.0.join("pending-1"), b"x").unwrap();
    WorkLedger::discovery_profile()
        .scope(|work| dir.unlink_entry_accounted("pending-1", work))
        .unwrap();
    assert!(!s.0.join("pending-1").exists());
    for bad in ["", ".", "..", "a/b", "a\\b"] {
        let renamed = WorkLedger::discovery_profile()
            .scope(|work| dir.rename_exclusive_accounted(bad, "x", work));
        assert!(renamed.is_err(), "{bad:?}");
        let unlinked =
            WorkLedger::discovery_profile().scope(|work| dir.unlink_entry_accounted(bad, work));
        assert!(unlinked.is_err(), "{bad:?}");
    }
    // An absent entry is an error, never a silent success.
    let absent =
        WorkLedger::discovery_profile().scope(|work| dir.unlink_entry_accounted("absent", work));
    assert!(absent.is_err());
}
