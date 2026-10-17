// Unit C1a2's route controls (C1A-T2 and C1A-T3; C1a plan r2, RF-2, kept
// from C1a1 by Codex C1A1-R1-NBO-1): the snapshot's two lawful roots over
// one synthetic installation. The ephemeral route is a read session's
// equivalent release, I complete; the durable route is the writer handoff's
// operation. The visitor here reads each handed file, standing in for the
// host's `snapshot.rs`.
use super::*;
use crate::custody::installation_read_fixture::ReadFixture;
use crate::custody::namespace_lease::WriterLease;
use crate::discovery_export::AdmittedBoundaries;
use crate::snapshot_walk::{SnapshotExtent, SnapshotStop, walk_snapshot};
use opensip_identity::RawSha256;
use opensip_platform::{FileLock, LockMode, WorkLedger};
use std::io::Read;
use std::os::unix::fs::{MetadataExt, PermissionsExt};
use std::path::Path;

fn directory(path: &Path) {
    std::fs::create_dir_all(path).unwrap();
    std::fs::set_permissions(path, std::fs::Permissions::from_mode(0o755)).unwrap();
}
fn write(root: &Path, rel: &str, bytes: &[u8]) {
    let path = root.join(rel);
    directory(path.parent().unwrap());
    std::fs::write(&path, bytes).unwrap();
    std::fs::set_permissions(&path, std::fs::Permissions::from_mode(0o644)).unwrap();
}
fn fence_free(installation: &Path) -> bool {
    FileLock::try_acquire(
        std::fs::File::open(installation.join("lifecycle.fence")).unwrap(),
        LockMode::Exclusive,
    )
    .unwrap()
    .is_some()
}

/// The inventory a walk over `root` gives: each handed path, its raw
/// SHA-256 and length, in the order handed.
fn inventory(root: &SnapshotRoot<'_>, uid: u32) -> Vec<(String, [u8; 32], u64)> {
    let bounds = AdmittedBoundaries::new(
        String::new(),
        Vec::new(),
        Vec::new(),
        Vec::new(),
        Vec::new(),
        Vec::new(),
    );
    let members = BTreeSet::new();
    let extent = WorkLedger::discovery_profile()
        .scope(|work| SnapshotExtent::new(&bounds, &members, &[], work))
        .unwrap();
    let groups = BTreeSet::new();
    let custody = SnapshotCustody::new(uid, &groups, None);
    let mut rows = Vec::new();
    let mut visit = |mut source: SourceFile, _: &mut WorkScope<'_>| -> Result<(), String> {
        let mut bytes = Vec::new();
        source
            .file()
            .read_to_end(&mut bytes)
            .map_err(|e| e.to_string())?;
        let sha = RawSha256::new().update(&bytes).unwrap().finish();
        rows.push((source.path().to_owned(), sha, bytes.len() as u64));
        Ok(())
    };
    let walked = WorkLedger::discovery_profile()
        .scope(|work| walk_snapshot(root, custody, &extent, &mut visit, work));
    match walked {
        Ok(_) => rows,
        Err(WorkFailure::Operation(SnapshotStop::Refused(r))) => panic!("refused: {r:?}"),
        Err(WorkFailure::Operation(SnapshotStop::Visitor(e))) => panic!("visitor: {e}"),
        Err(WorkFailure::Budget(b)) => panic!("budget: {b:?}"),
    }
}

#[test]
fn the_ephemeral_and_durable_routes_walk_one_tree_to_one_inventory_and_the_ephemeral_holds_nothing()
{
    let fixture = ReadFixture::new("c1a2-routes");
    let at = fixture.at();
    at.install_accepted_trust(Vec::new(), 1, None).unwrap();
    let code = fixture.home.join("code");
    directory(&code);
    let project = code.join("project");
    directory(&project);
    write(&project, "package.json", b"{\"name\":\"p\"}");
    write(&project, "src/index.ts", b"export {};\n");
    write(&project, "node_modules/dep/index.js", b"pruned");
    write(&project, "README.md", b"# p\n");
    let uid = std::fs::metadata(&fixture.home).unwrap().uid();
    // The ephemeral route: a read session admits the root, then releases
    // its fence and installation handles, keeping only its read receipt.
    let session = fixture.session(None).unwrap();
    let admission = session
        .admit_project_root(&project, None, &BTreeSet::new())
        .unwrap();
    let released = session.release().unwrap();
    let ephemeral = SnapshotRoot::from_released_read(&released, &admission);
    // C1A-T3: the ephemeral route holds no fence, and no lease: with its
    // root lent and unwalked, a writer takes the fence and the APPEND_WRITE
    // lease, and hands off the durable route's operation.
    assert!(fence_free(&fixture.installation));
    let (operation, _trees) = at
        .operation(&project, WriterLease::AppendWrite)
        .unwrap_or_else(|t| panic!("durable operation: {t:?}"));
    assert!(fence_free(&fixture.installation));
    let durable = SnapshotRoot::from_operation(&operation);
    // C1A-T2: both routes walk the one tree to one inventory.
    let from_ephemeral = inventory(&ephemeral, uid);
    let from_durable = inventory(&durable, uid);
    assert_eq!(from_ephemeral, from_durable);
    let paths: Vec<&str> = from_durable.iter().map(|(p, _, _)| p.as_str()).collect();
    assert_eq!(paths, ["README.md", "package.json", "src/index.ts"]);
    // The registration's `.opensip/` marker, made by the durable route's
    // handoff, is never inventoried on either route.
    assert!(project.join(".opensip").exists());
}
