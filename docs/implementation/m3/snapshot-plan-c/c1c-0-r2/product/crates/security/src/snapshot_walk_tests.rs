// Unit C1a1's walk controls (C1a plan r4, C1a1): scratch trees under the APFS
// test premise, walked natively over a test root. Nothing reads the real
// home or a real repository; the visitor here stands in for the host's
// `snapshot.rs`, which alone reads content.
use super::*;
use crate::custody::project_chain::DiscoveryRoot;
use crate::discovery_export::CustodyExcludedUnit;
use crate::grants::AuthorizedGroups;
use crate::initial_installation::InitialInstallationAttempt;
use crate::snapshot_source::set_before_open;
use crate::snapshot_walk::set_before_observe;
use crate::trust::AclOmissionPremise;
use opensip_platform::{RetainedDirectoryPath, WorkLedger};
use std::io::Read;
use std::os::unix::fs::{MetadataExt, PermissionsExt};
use std::path::{Path, PathBuf};
use std::sync::atomic::AtomicBool;

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
    let base = crate::test_scratch::temp_dir().join(format!("opensip-c1a1-{nonce}"));
    std::fs::create_dir(&base).unwrap();
    std::fs::set_permissions(&base, std::fs::Permissions::from_mode(0o700)).unwrap();
    let base = std::fs::canonicalize(&base).unwrap();
    let root = base.join("w");
    dir(&root);
    (Scratch(base), root)
}
fn dir(path: &Path) {
    std::fs::create_dir_all(path).unwrap();
    std::fs::set_permissions(path, std::fs::Permissions::from_mode(0o755)).unwrap();
}
fn file(path: &Path, bytes: &[u8]) {
    if let Some(parent) = path.parent()
        && !parent.exists()
    {
        dir(parent);
    }
    std::fs::write(path, bytes).unwrap();
    std::fs::set_permissions(path, std::fs::Permissions::from_mode(0o644)).unwrap();
}
fn premise() -> AclOmissionPremise {
    let flag = Box::leak(Box::new(AtomicBool::new(false)));
    let attempt = InitialInstallationAttempt::for_tests(flag, None).unwrap();
    AclOmissionPremise::for_tests(&attempt, &[b"apfs"])
}
fn uid() -> u32 {
    std::fs::metadata(crate::test_scratch::temp_dir())
        .unwrap()
        .uid()
}

struct Lent {
    path: RetainedDirectoryPath,
    spelling: PathBuf,
    premise: AclOmissionPremise,
}
impl Lent {
    fn new(root: &Path) -> Self {
        Self {
            path: RetainedDirectoryPath::open_project_root(root, 256).unwrap(),
            spelling: root.to_path_buf(),
            premise: premise(),
        }
    }
    fn root(&self) -> SnapshotRoot<'_> {
        SnapshotRoot::for_tests(DiscoveryRoot::for_tests(
            self.path.directory(),
            &self.spelling,
            Some(&self.premise),
        ))
    }
}

/// An extent, its `ignorePaths` validation charged to a ledger of its own
/// (the walk's ledger then holds the walk alone).
fn extent_of<'a>(
    bounds: &'a AdmittedBoundaries,
    members: &'a BTreeSet<String>,
    ignore: &'a [String],
) -> Result<SnapshotExtent<'a>, WorkFailure<IgnorePathInvalid>> {
    WorkLedger::discovery_profile().scope(|work| SnapshotExtent::new(bounds, members, ignore, work))
}

fn boundaries(nested_repositories: &[&str], custody: &[(&str, &str)]) -> AdmittedBoundaries {
    AdmittedBoundaries::new(
        String::new(),
        nested_repositories
            .iter()
            .map(|s| (*s).to_owned())
            .collect(),
        Vec::new(),
        custody
            .iter()
            .map(|(p, r)| CustodyExcludedUnit {
                path: (*p).to_owned(),
                reason: (*r).to_owned(),
            })
            .collect(),
        Vec::new(),
        Vec::new(),
    )
}

/// What a walk handed the visitor: each path with its bytes (read here, as
/// the host would) and its observation's inode.
#[derive(Debug)]
struct Walked {
    files: Vec<(String, Vec<u8>, u64)>,
    report: SnapshotWalkReport,
}
fn walk_tree(root: &Path, ignore: &[&str], bounds: &AdmittedBoundaries) -> Result<Walked, String> {
    walk_members(root, ignore, bounds, &[])
}
fn walk_members(
    root: &Path,
    ignore: &[&str],
    bounds: &AdmittedBoundaries,
    members: &[&str],
) -> Result<Walked, String> {
    let lent = Lent::new(root);
    let groups = AuthorizedGroups::from_invocation(&[]).unwrap();
    let custody = SnapshotCustody::new(uid(), groups.as_set(), None);
    let members: BTreeSet<String> = members.iter().map(|m| (*m).to_owned()).collect();
    let ignore: Vec<String> = ignore.iter().map(|s| (*s).to_owned()).collect();
    let extent = extent_of(bounds, &members, &ignore).unwrap();
    let mut files = Vec::new();
    let mut visit = |mut source: SourceFile, _: &mut WorkScope<'_>| -> Result<(), String> {
        let mut bytes = Vec::new();
        source
            .file()
            .read_to_end(&mut bytes)
            .map_err(|e| e.to_string())?;
        files.push((source.path().to_owned(), bytes, source.observation().inode));
        Ok(())
    };
    let result = WorkLedger::discovery_profile()
        .scope(|work| walk_snapshot(&lent.root(), custody, &extent, &mut visit, work));
    match result {
        Ok(report) => Ok(Walked { files, report }),
        Err(WorkFailure::Operation(SnapshotStop::Refused(r))) => Err(format!("{r:?}")),
        Err(WorkFailure::Operation(SnapshotStop::Visitor(e))) => Err(e),
        Err(WorkFailure::Budget(b)) => Err(format!("budget {b:?}")),
    }
}
fn paths(walked: &Walked) -> Vec<&str> {
    walked.files.iter().map(|(p, _, _)| p.as_str()).collect()
}

// ------------------------------------------------------------------ the extent (item 2)

#[test]
fn the_extent_is_every_regular_file_outside_pruned_trees_boundaries_and_ignore_paths() {
    let (_s, root) = scratch();
    file(&root.join("a.txt"), b"a");
    file(&root.join("Cargo.toml"), b"[package]\n");
    file(&root.join("src/main.rs"), b"fn main() {}\n");
    // C1-T9: `target/` beside Cargo.toml is pruned; `packages/target/` is not.
    file(&root.join("target/debug/x.o"), b"obj");
    file(&root.join("packages/target/x.ts"), b"export {}\n");
    // Pruned dependency and VCS trees, and OpenSIP's own state (SX-1).
    file(&root.join("node_modules/p/index.js"), b"x");
    file(&root.join(".git/HEAD"), b"ref: refs/heads/main\n");
    file(&root.join(".opensip/project-id.v1"), b"prj1-x");
    // C1-T10: a nested repository's files are never read.
    file(&root.join("nested/repo/f.txt"), b"nested");
    file(&root.join("nested/repo/.git/HEAD"), b"x");
    // `ignorePaths`.
    file(&root.join("ignored/secret.txt"), b"s");
    file(&root.join("ignored-not/kept.txt"), b"k");
    // C1-T5 and C1-T6: a symlink and a FIFO, never opened.
    std::os::unix::fs::symlink(root.join("a.txt"), root.join("link")).unwrap();
    assert!(
        std::process::Command::new("/usr/bin/mkfifo")
            .arg(root.join("fifo"))
            .status()
            .unwrap()
            .success()
    );
    let bounds = boundaries(&["nested/repo"], &[]);
    let walked = walk_tree(&root, &["ignored"], &bounds).unwrap();
    let mut got = paths(&walked);
    got.sort();
    assert_eq!(
        got,
        [
            "Cargo.toml",
            "a.txt",
            "ignored-not/kept.txt",
            "packages/target/x.ts",
            "src/main.rs"
        ]
    );
    assert_eq!(walked.report.symlinks, ["link"]);
    assert_eq!(walked.report.special, ["fifo"]);
    // C1-T1's first half: the bytes handed are the file's bytes.
    let main = walked
        .files
        .iter()
        .find(|(p, _, _)| p == "src/main.rs")
        .unwrap();
    assert_eq!(main.1, b"fn main() {}\n");
}

// r2 (Codex C1A1-R1-RF-1): the exact `.opensip` anchors at the root and a D15
// member are never observed, so one that vanishes or changes after the
// listing cannot refuse the walk; an ordinary nested `.opensip` is walked.
#[test]
fn the_exact_opensip_anchors_are_never_observed_even_when_they_vanish_or_change() {
    let (_s, root) = scratch();
    file(&root.join(".opensip/project-id.v1"), b"prj1-x");
    file(&root.join("m/package.json"), b"{}");
    file(&root.join("m/.opensip/state"), b"s");
    file(&root.join("a/.opensip/kept.txt"), b"k");
    file(&root.join("z.txt"), b"z");
    let observed = std::rc::Rc::new(std::cell::RefCell::new(Vec::<String>::new()));
    let (log, swap_root) = (observed.clone(), root.clone());
    set_before_observe(Some(Box::new(move |rel: &str| {
        if log.borrow().is_empty() {
            // After the root's listing: the root's anchor vanishes (it could
            // no longer be observed) and the member's becomes a file.
            std::fs::remove_dir_all(swap_root.join(".opensip")).unwrap();
            std::fs::remove_dir_all(swap_root.join("m/.opensip")).unwrap();
            std::fs::write(swap_root.join("m/.opensip"), b"now a file").unwrap();
        }
        log.borrow_mut().push(rel.to_owned());
    })));
    let bounds = boundaries(&[], &[]);
    let walked = walk_members(&root, &[], &bounds, &["m"]);
    set_before_observe(None);
    let walked = walked.unwrap();
    let observed = observed.borrow();
    assert!(!observed.iter().any(|p| p == ".opensip"), "{observed:?}");
    assert!(!observed.iter().any(|p| p == "m/.opensip"), "{observed:?}");
    assert!(observed.iter().any(|p| p == "a/.opensip"), "{observed:?}");
    let mut got = paths(&walked);
    got.sort();
    assert_eq!(got, ["a/.opensip/kept.txt", "m/package.json", "z.txt"]);
}

// r2 (Codex C1A1-R1-RF-2): an admitted boundary excludes its path whatever the
// entry now is.
#[test]
fn a_boundary_that_is_now_a_file_a_link_or_a_fifo_is_never_handed_or_reported() {
    let (_s, root) = scratch();
    file(&root.join("r1"), b"was a nested repository");
    std::os::unix::fs::symlink(root.join("r1"), root.join("r2")).unwrap();
    assert!(
        std::process::Command::new("/usr/bin/mkfifo")
            .arg(root.join("r3"))
            .status()
            .unwrap()
            .success()
    );
    file(&root.join("c"), b"was a custody-excluded directory");
    file(&root.join("d/depth"), b"was below a depth exclusion");
    file(&root.join("kept.txt"), b"k");
    let bounds = boundaries(
        &["r1", "r2", "r3"],
        &[
            ("c", "DIRECTORY_CUSTODY:WRITABLE_BY_OTHERS"),
            ("d/depth", "DEPTH"),
        ],
    );
    let walked = walk_tree(&root, &[], &bounds).unwrap();
    assert_eq!(paths(&walked), ["kept.txt"]);
    assert!(walked.report.symlinks.is_empty(), "{:?}", walked.report);
    assert!(walked.report.special.is_empty(), "{:?}", walked.report);
}

#[test]
fn an_ignore_path_that_is_not_a_logical_path_is_refused() {
    let bounds = boundaries(&[], &[]);
    let members = BTreeSet::new();
    assert!(extent_of(&bounds, &members, &["../x".to_owned()]).is_err());
    assert!(extent_of(&bounds, &members, &["a//b".to_owned()]).is_err());
    // Each entry's validation is charged before the validator copies it.
    let ignore = ["ok/path".to_owned(), "also".to_owned()];
    let mut ledger = WorkLedger::discovery_profile();
    ledger
        .scope(|work| SnapshotExtent::new(&bounds, &members, &ignore, work).map(drop))
        .unwrap();
    let used = ledger.used();
    assert_eq!((used.objects, used.bytes), (2, 7 + 4 + 2 * 128));
}

// ------------------------------------------------------------------ custody (item 2)

#[test]
fn a_directory_failing_s3_custody_refuses_the_walk() {
    let (_s, root) = scratch();
    file(&root.join("open/f.txt"), b"x");
    std::fs::set_permissions(root.join("open"), std::fs::Permissions::from_mode(0o777)).unwrap();
    let bounds = boundaries(&[], &[]);
    let error = walk_tree(&root, &[], &bounds).unwrap_err();
    assert!(error.starts_with("Custody"), "{error}");
    assert!(error.contains("\"open\""), "{error}");
}

#[test]
fn a_marker_failing_config_file_custody_refuses_unless_a_marker_custody_row_excludes_it() {
    // C1-T8: a marker with link count 2.
    let (_s, root) = scratch();
    file(&root.join("pkg/package.json"), b"{}");
    std::fs::hard_link(root.join("pkg/package.json"), root.join("pkg/alias.json")).unwrap();
    let bounds = boundaries(&[], &[]);
    let error = walk_tree(&root, &[], &bounds).unwrap_err();
    assert!(error.starts_with("MarkerCustody"), "{error}");
    // B2's marker-custody row excludes exactly that marker; its hard-linked
    // sibling, not a marker, is ordinary source.
    let bounds = boundaries(&[], &[("pkg", "MARKER_CUSTODY:package.json:HARD_LINKED")]);
    let walked = walk_tree(&root, &[], &bounds).unwrap();
    assert_eq!(paths(&walked), ["pkg/alias.json"]);
}

#[test]
fn a_marker_over_four_mebibytes_refuses() {
    let (_s, root) = scratch();
    file(&root.join("Cargo.toml"), &vec![b'#'; 4 * 1024 * 1024 + 1]);
    let bounds = boundaries(&[], &[]);
    let error = walk_tree(&root, &[], &bounds).unwrap_err();
    assert!(error.starts_with("MarkerCustody"), "{error}");
}

// ------------------------------------------------------------------ names (C1-T7)

// The walk converts each listed name with the discovery walk's own
// `ListingConversion`, unchanged, so C1-T7's non-UTF-8 and 256-scalar cases,
// which APFS cannot create (EILSEQ, ENAMETOOLONG), are that conversion's
// controls (`discovery_walk_tests.rs`,
// `listed_names_are_validated_as_logical_paths`). The names APFS can hold are
// walked natively here.
#[test]
fn a_backslash_name_and_a_staging_name_refuse_the_whole_walk_with_the_parent() {
    for (name, escaped) in [
        ("back\\slash", "back\\\\slash"),
        (".opensip-stage-x", ".opensip-stage-x"),
    ] {
        let (_s, root) = scratch();
        file(&root.join("ok.txt"), b"x");
        file(&root.join("d").join(name), b"x");
        let bounds = boundaries(&[], &[]);
        let error = walk_tree(&root, &[], &bounds).unwrap_err();
        assert!(error.starts_with("Name"), "{name}: {error}");
        assert!(error.contains(escaped), "{name}: {error}");
        assert!(error.contains("/d"), "{name}: {error}");
    }
}

// ------------------------------------------------------------------ changes (C1-T4, C1A-T5)

#[test]
fn a_swap_between_the_observation_and_the_open_refuses_with_no_retry() {
    let (_s, root) = scratch();
    file(&root.join("src/main.rs"), b"one");
    let swap_root = root.clone();
    set_before_open(Some(Box::new(move |rel: &str| {
        if rel == "src/main.rs" {
            std::fs::remove_file(swap_root.join("src/main.rs")).unwrap();
            std::fs::write(swap_root.join("src/main.rs"), b"two").unwrap();
        }
    })));
    let bounds = boundaries(&[], &[]);
    let error = walk_tree(&root, &[], &bounds).unwrap_err();
    set_before_open(None);
    assert_eq!(error, "Changed(\"src/main.rs\")");
}

#[test]
fn a_directory_replaced_between_its_listing_and_its_open_refuses() {
    let (_s, root) = scratch();
    file(&root.join("a/f.txt"), b"one");
    let swap_root = root.clone();
    set_before_open(Some(Box::new(move |rel: &str| {
        if rel == "a" {
            std::fs::rename(swap_root.join("a"), swap_root.join("a.old")).unwrap();
            dir(&swap_root.join("a"));
        }
    })));
    let bounds = boundaries(&[], &[]);
    let error = walk_tree(&root, &[], &bounds).unwrap_err();
    set_before_open(None);
    assert_eq!(error, "Changed(\"a\")");
}

#[test]
fn an_ancestor_replaced_after_it_is_entered_never_redirects_the_walk() {
    // C1A-T5: the walk opens from its enumerating parent, so replacing an
    // entered ancestor by path cannot bring the replacement's bytes in.
    let (_s, root) = scratch();
    file(&root.join("a/b/f.txt"), b"original");
    let swap_root = root.clone();
    set_before_open(Some(Box::new(move |rel: &str| {
        if rel == "a/b/f.txt" {
            std::fs::rename(swap_root.join("a"), swap_root.join("a.old")).unwrap();
            file(&swap_root.join("a/b/f.txt"), b"replacement");
        }
    })));
    let bounds = boundaries(&[], &[]);
    let walked = walk_tree(&root, &[], &bounds).unwrap();
    set_before_open(None);
    let f = walked
        .files
        .iter()
        .find(|(p, _, _)| p == "a/b/f.txt")
        .unwrap();
    assert_eq!(f.1, b"original");
}

// ------------------------------------------------------------------ the pre-walk opener

#[test]
fn the_pre_walk_opener_judges_each_directory_and_matches_the_walks_observation() {
    let (_s, root) = scratch();
    file(&root.join("pkg/package.json"), b"{}");
    file(&root.join("pkg/src/i.ts"), b"x");
    let lent = Lent::new(&root);
    let groups = AuthorizedGroups::from_invocation(&[]).unwrap();
    let custody = SnapshotCustody::new(uid(), groups.as_set(), None);
    let captured = WorkLedger::discovery_profile()
        .scope(|work| lent.root().open("pkg/package.json", custody, work))
        .unwrap();
    assert!(captured.is_marker());
    let bounds = boundaries(&[], &[]);
    let walked = walk_tree(&root, &[], &bounds).unwrap();
    let walked_marker = walked
        .files
        .iter()
        .find(|(p, _, _)| p == "pkg/package.json")
        .unwrap();
    assert_eq!(walked_marker.2, captured.observation().inode);
    // A capture's ancestor replaced before the walk: the walk's observation
    // through its enumerating parent is another object (the host refuses).
    std::fs::rename(root.join("pkg"), root.join("pkg.old")).unwrap();
    file(&root.join("pkg/package.json"), b"{}");
    file(&root.join("pkg/src/i.ts"), b"x");
    let walked = walk_tree(&root, &[], &bounds).unwrap();
    let again = walked
        .files
        .iter()
        .find(|(p, _, _)| p == "pkg/package.json")
        .unwrap();
    assert_ne!(again.2, captured.observation().inode);
    // The opener refuses a symlinked component and a custody failure.
    std::os::unix::fs::symlink(root.join("pkg"), root.join("linked")).unwrap();
    let error = WorkLedger::discovery_profile()
        .scope(|work| lent.root().open("linked/package.json", custody, work))
        .unwrap_err();
    assert!(
        matches!(
            error,
            WorkFailure::Operation(SnapshotRefusal::NotARegularFile(_))
        ),
        "{error:?}"
    );
    std::fs::set_permissions(root.join("pkg"), std::fs::Permissions::from_mode(0o777)).unwrap();
    let error = WorkLedger::discovery_profile()
        .scope(|work| lent.root().open("pkg/package.json", custody, work))
        .unwrap_err();
    assert!(
        matches!(
            error,
            WorkFailure::Operation(SnapshotRefusal::Custody { .. })
        ),
        "{error:?}"
    );
}

// r2 (Codex C1A1-R1-RF-3): the opener judges the retained root itself before
// any traversal, for a root-level capture and a nested one, after the root's
// mode or ACL changes once it is lent.
#[test]
fn the_pre_walk_opener_judges_the_retained_root_before_any_capture() {
    let (_s, root) = scratch();
    file(&root.join("a.txt"), b"a");
    file(&root.join("src/main.rs"), b"fn main() {}\n");
    let lent = Lent::new(&root);
    let groups = AuthorizedGroups::from_invocation(&[]).unwrap();
    let custody = SnapshotCustody::new(uid(), groups.as_set(), None);
    let open = |path: &str| {
        WorkLedger::discovery_profile().scope(|work| lent.root().open(path, custody, work))
    };
    assert!(open("a.txt").is_ok());
    assert!(open("src/main.rs").is_ok());
    let refused_at_root = |result: Result<SourceFile, SnapshotFailure>| {
        matches!(
            result,
            Err(WorkFailure::Operation(SnapshotRefusal::Custody { ref path, .. })) if path.is_empty()
        )
    };
    std::fs::set_permissions(&root, std::fs::Permissions::from_mode(0o777)).unwrap();
    assert!(refused_at_root(open("a.txt")));
    assert!(refused_at_root(open("src/main.rs")));
    std::fs::set_permissions(&root, std::fs::Permissions::from_mode(0o755)).unwrap();
    assert!(open("a.txt").is_ok());
    assert!(
        std::process::Command::new("/bin/chmod")
            .args(["+a", "group:everyone allow add_file"])
            .arg(&root)
            .status()
            .unwrap()
            .success()
    );
    assert!(refused_at_root(open("a.txt")));
    assert!(refused_at_root(open("src/main.rs")));
}

// ------------------------------------------------------------------ the oracle cross-check

/// The extent against B2-b0, the bound discovery reference (contract
/// successor 164), through its accepted walk vectors: for every automatic case
/// the reference accepts, the snapshot walk over the same tree either hands
/// exactly the population's regular files outside every pruned tree,
/// boundary and marker-custody row, or refuses S3 custody at a directory the
/// tree gives a custody defect (the snapshot judges every directory it
/// enters; discovery judges unit chains only).
mod oracle {
    use super::*;
    use crate::custody::discovery_rule as rule;
    use crate::grants::ProjectOwnerWaiver;
    use opensip_identity::{JsonValue as V, parse_json};

    const VECTORS: &[u8] = include_bytes!("custody/discovery_walk_vectors.json");
    const FOREIGN_UID: u32 = 4242;
    const OTHER_GID: u32 = 4243;

    pub(super) fn field<'v>(value: &'v V, key: &str) -> &'v V {
        match value {
            V::Object(m) => m.get(key).unwrap_or_else(|| panic!("missing {key}")),
            _ => panic!("not an object"),
        }
    }
    pub(super) fn get<'v>(value: &'v V, key: &str) -> Option<&'v V> {
        match value {
            V::Object(m) => m.get(key),
            _ => None,
        }
    }
    pub(super) fn text(value: &V) -> &str {
        match value {
            V::String(s) => s,
            _ => panic!("not a string"),
        }
    }
    pub(super) fn items(value: &V) -> &[V] {
        match value {
            V::Array(a) => a,
            _ => panic!("not an array"),
        }
    }
    fn flag(value: &V) -> bool {
        matches!(value, V::Bool(true))
    }
    fn mode(entry: &V) -> u32 {
        u32::from_str_radix(text(field(entry, "mode")), 8).unwrap()
    }

    pub(super) fn materialize(root: &Path, links: &Path, tree: &[V]) {
        for (index, entry) in tree.iter().enumerate() {
            let path = root.join(text(field(entry, "path")));
            let kind = text(field(entry, "kind"));
            match kind {
                "dir" => {
                    std::fs::create_dir(&path).unwrap();
                    std::fs::set_permissions(&path, std::fs::Permissions::from_mode(mode(entry)))
                        .unwrap();
                }
                "file" => {
                    std::fs::write(&path, text(field(entry, "text")).as_bytes()).unwrap();
                    std::fs::set_permissions(&path, std::fs::Permissions::from_mode(mode(entry)))
                        .unwrap();
                    if get(entry, "hardlink").is_some_and(flag) {
                        std::fs::hard_link(&path, links.join(index.to_string())).unwrap();
                    }
                }
                "symlink" => {
                    std::os::unix::fs::symlink(text(field(entry, "target")), &path).unwrap()
                }
                "fifo" => assert!(
                    std::process::Command::new("/usr/bin/mkfifo")
                        .arg("-m")
                        .arg(text(field(entry, "mode")))
                        .arg(&path)
                        .status()
                        .unwrap()
                        .success()
                ),
                "socket" => {
                    let nonce: String = opensip_platform::request_entropy().unwrap()[..6]
                        .iter()
                        .map(|b| format!("{b:02x}"))
                        .collect();
                    let short = std::env::temp_dir().join(format!("s{nonce}"));
                    drop(std::os::unix::net::UnixListener::bind(&short).unwrap());
                    std::fs::rename(&short, &path).unwrap();
                }
                other => panic!("{other}"),
            }
            if let Some(V::String(who)) = get(entry, "acl") {
                let principal = if who == "user" {
                    "user:nobody"
                } else {
                    "group:everyone"
                };
                let right = if kind == "dir" { "add_file" } else { "write" };
                assert!(
                    std::process::Command::new("/bin/chmod")
                        .arg("+a")
                        .arg(format!("{principal} allow {right}"))
                        .arg(&path)
                        .status()
                        .unwrap()
                        .success()
                );
            }
        }
    }

    pub(super) fn strings(value: &V) -> Vec<String> {
        items(value).iter().map(|v| text(v).to_owned()).collect()
    }

    #[test]
    fn every_accepted_automatic_walk_vector_hands_exactly_its_reference_regular_files() {
        let body = parse_json(VECTORS).unwrap();
        let (mut exact, mut custody_refusals) = (0, 0);
        for case in items(field(&body, "cases")) {
            if text(field(case, "source")) != "automatic"
                || text(field(field(case, "expected"), "status")) != "ACCEPT"
            {
                continue;
            }
            let id = text(field(case, "id"));
            let (_s, root) = scratch();
            let links = root.parent().unwrap().join("links");
            dir(&links);
            materialize(&root, &links, items(field(case, "tree")));
            let inventory = field(case, "inventory");
            let bounds = AdmittedBoundaries::new(
                String::new(),
                strings(field(inventory, "nestedRepositories")),
                strings(field(inventory, "nestedProjects")),
                items(field(inventory, "custodyExcludedUnits"))
                    .iter()
                    .map(|row| CustodyExcludedUnit {
                        path: text(field(row, "path")).to_owned(),
                        reason: text(field(row, "reason")).to_owned(),
                    })
                    .collect(),
                Vec::new(),
                Vec::new(),
            );
            // The reference's regular files outside every exclusion.
            let population = match field(case, "population") {
                V::Object(m) => m,
                _ => panic!("population"),
            };
            let rel = |abs: &str| abs.strip_prefix("/h/w/").map(str::to_owned);
            let cargo_roots: BTreeSet<String> = population
                .iter()
                .filter_map(|(p, e)| {
                    let r = rel(p)?;
                    (text(field(e, "kind")) == "file" && super::last_segment(&r) == "Cargo.toml")
                        .then(|| {
                            r.rsplit_once('/')
                                .map_or(String::new(), |(d, _)| d.to_owned())
                        })
                })
                .chain(population.get("/h/w/Cargo.toml").map(|_| String::new()))
                .collect();
            let members = BTreeSet::new();
            let mut expected: Vec<String> = population
                .iter()
                .filter_map(|(p, e)| {
                    let r = rel(p)?;
                    if text(field(e, "kind")) != "file"
                        || rule::classify_path(&r, &cargo_roots, &members).is_some()
                        || bounds.is_boundary(&r)
                    {
                        return None;
                    }
                    let (parent, name) = r.rsplit_once('/').unwrap_or(("", r.as_str()));
                    let marker_row = super::is_marker_name(name)
                        && bounds
                            .boundary_hit(parent, Some(name))
                            .is_some_and(|(anchor, _)| anchor == parent);
                    (!marker_row).then_some(r)
                })
                .collect();
            expected.sort();
            // The native walk, as the reference's invocation.
            let lent = Lent::new(&root);
            let own = std::fs::metadata(&root).unwrap().gid();
            let gids: Vec<u32> = match get(case, "groups") {
                Some(V::String(g)) if g == "own" => vec![own],
                Some(V::String(g)) if g == "other" => vec![OTHER_GID],
                _ => Vec::new(),
            };
            let groups = AuthorizedGroups::from_invocation(&gids).unwrap();
            let waiver =
                ProjectOwnerWaiver::from_invocation(flag(field(case, "waive")), Some(&root))
                    .unwrap();
            let invoking = if flag(field(case, "foreign")) {
                FOREIGN_UID
            } else {
                uid()
            };
            let custody = SnapshotCustody::new(invoking, groups.as_set(), waiver.as_ref());
            let extent = extent_of(&bounds, &members, &[]).unwrap();
            let mut handed = Vec::new();
            let mut visit = |source: SourceFile, _: &mut WorkScope<'_>| -> Result<(), String> {
                handed.push(source.path().to_owned());
                Ok(())
            };
            let result = WorkLedger::discovery_profile()
                .scope(|work| walk_snapshot(&lent.root(), custody, &extent, &mut visit, work));
            match result {
                Ok(_) => {
                    handed.sort();
                    assert_eq!(handed, expected, "{id}");
                    exact += 1;
                }
                Err(WorkFailure::Operation(SnapshotStop::Refused(SnapshotRefusal::Custody {
                    path,
                    reason,
                }))) => {
                    // The refused directory must carry a custody defect in the tree.
                    let entry = items(field(case, "tree"))
                        .iter()
                        .find(|e| text(field(e, "path")) == path);
                    let defect = flag(field(case, "foreign"))
                        || entry.is_some_and(|e| mode(e) & 0o022 != 0 || get(e, "acl").is_some());
                    assert!(defect, "{id}: refused {path} ({reason}) without a defect");
                    custody_refusals += 1;
                }
                Err(other) => panic!("{id}: {other:?}"),
            }
        }
        eprintln!("oracle: {exact} exact, {custody_refusals} custody refusals");
        assert_eq!((exact, custody_refusals), (28, 0));
    }
}

// ------------------------------------------------------------------ the charge model's soundness

/// C1a1's soundness control (C1a plan r5 section 2): every tree of
/// `snapshot_ledger_vectors.json` (the accepted automatic discovery walk
/// vectors and the generated worst-case shapes), walked natively on a fresh
/// ledger, uses no more objects, edges or bytes than the model predicts: an
/// upper bound, since the model charges each ACL capture at its dearer
/// branch. The cases the model marks `exact` (every capture there takes the
/// branch the model charges) must also be equal (r2, Codex C1A1-R1-NBO-2).
/// Each case's native and predicted triples are printed.
#[test]
fn the_native_walk_never_charges_more_than_the_model_predicts() {
    use opensip_identity::{JsonValue as V, parse_json};
    use oracle::{field, items, materialize, strings, text};
    const PREDICTIONS: &[u8] = include_bytes!("snapshot_ledger_vectors.json");
    let body = parse_json(PREDICTIONS).unwrap();
    let count = |v: &V| -> usize {
        match v {
            V::Integer(i) => usize::try_from(i.get()).unwrap(),
            _ => panic!("not an integer"),
        }
    };
    let (mut checked, mut exact_cases) = (0, 0);
    for case in items(field(&body, "cases")) {
        let id = text(field(case, "id"));
        let (_s, root) = scratch();
        let links = root.parent().unwrap().join("links");
        dir(&links);
        materialize(&root, &links, items(field(case, "tree")));
        let inventory = field(case, "inventory");
        let list = |key: &str| match inventory {
            V::Object(m) => m.get(key).map(strings).unwrap_or_default(),
            _ => Vec::new(),
        };
        let rows = match inventory {
            V::Object(m) => m
                .get("custodyExcludedUnits")
                .map(|v| {
                    items(v)
                        .iter()
                        .map(|row| CustodyExcludedUnit {
                            path: text(field(row, "path")).to_owned(),
                            reason: text(field(row, "reason")).to_owned(),
                        })
                        .collect()
                })
                .unwrap_or_default(),
            _ => Vec::new(),
        };
        let bounds = AdmittedBoundaries::new(
            String::new(),
            list("nestedRepositories"),
            list("nestedProjects"),
            rows,
            Vec::new(),
            Vec::new(),
        );
        let lent = Lent::new(&root);
        // The case's own invocation (the discovery vectors' groups, waiver
        // and foreign user; generated cases have none).
        let own = std::fs::metadata(&root).unwrap().gid();
        let key = |k: &str| match case {
            V::Object(m) => m.get(k).cloned(),
            _ => None,
        };
        let gids: Vec<u32> = match key("groups") {
            Some(V::String(g)) if g == "own" => vec![own],
            Some(V::String(g)) if g == "other" => vec![4243],
            _ => Vec::new(),
        };
        let groups = AuthorizedGroups::from_invocation(&gids).unwrap();
        let waive = matches!(key("waive"), Some(V::Bool(true)));
        let waiver =
            crate::grants::ProjectOwnerWaiver::from_invocation(waive, Some(&root)).unwrap();
        let invoking = if matches!(key("foreign"), Some(V::Bool(true))) {
            4242
        } else {
            uid()
        };
        let custody = SnapshotCustody::new(invoking, groups.as_set(), waiver.as_ref());
        let members: BTreeSet<String> = match case {
            V::Object(m) => m.get("members").map(strings).unwrap_or_default(),
            _ => Vec::new(),
        }
        .into_iter()
        .collect();
        let extent = extent_of(&bounds, &members, &[]).unwrap();
        let mut visit = |_: SourceFile, _: &mut WorkScope<'_>| -> Result<(), String> { Ok(()) };
        let mut ledger = WorkLedger::discovery_profile();
        let result =
            ledger.scope(|work| walk_snapshot(&lent.root(), custody, &extent, &mut visit, work));
        assert!(result.is_ok(), "{id}: {result:?}");
        let used = ledger.used();
        let predicted = field(case, "predicted");
        let (o, e, b) = (
            count(field(predicted, "objects")),
            count(field(predicted, "edges")),
            count(field(predicted, "bytes")),
        );
        let exact = matches!(key("exact"), Some(V::Bool(true)));
        eprintln!(
            "soundness {id}: native ({}, {}, {}) predicted ({o}, {e}, {b}){}",
            used.objects,
            used.edges,
            used.bytes,
            if exact { " exact" } else { "" }
        );
        assert!(
            used.objects <= o && used.edges <= e && used.bytes <= b,
            "{id}: native {used:?} over the model ({o}, {e}, {b})"
        );
        if exact {
            assert_eq!((used.objects, used.edges, used.bytes), (o, e, b), "{id}");
            exact_cases += 1;
        }
        checked += 1;
    }
    eprintln!("soundness: {checked} cases, {exact_cases} exact");
    assert_eq!(checked, 35);
}

/// r3 (Codex C1A1-R2-RF-1): the pre-walk opener's charge, for a root-level
/// file, a nested one and a nested marker, equals the model's prediction
/// exactly: the validator's copy charged first and kept as the path, the
/// root's custody, and each component's key, observation, open and custody.
#[test]
fn the_pre_walk_opener_charges_exactly_the_models_prediction() {
    use opensip_identity::{JsonValue as V, parse_json};
    use oracle::{field, items, materialize, text};
    const PREDICTIONS: &[u8] = include_bytes!("snapshot_ledger_vectors.json");
    let body = parse_json(PREDICTIONS).unwrap();
    let count = |v: &V| -> usize {
        match v {
            V::Integer(i) => usize::try_from(i.get()).unwrap(),
            _ => panic!("not an integer"),
        }
    };
    let mut checked = 0;
    for case in items(field(&body, "openers")) {
        let (id, path) = (text(field(case, "id")), text(field(case, "path")));
        assert!(matches!(field(case, "exact"), V::Bool(true)), "{id}");
        let (_s, root) = scratch();
        let links = root.parent().unwrap().join("links");
        dir(&links);
        materialize(&root, &links, items(field(case, "tree")));
        let lent = Lent::new(&root);
        let groups = AuthorizedGroups::from_invocation(&[]).unwrap();
        let custody = SnapshotCustody::new(uid(), groups.as_set(), None);
        let mut ledger = WorkLedger::discovery_profile();
        let opened = ledger
            .scope(|work| lent.root().open(path, custody, work))
            .unwrap_or_else(|f| panic!("{id}: {f:?}"));
        assert_eq!(opened.path(), path);
        let used = ledger.used();
        let predicted = field(case, "predicted");
        let expected = (
            count(field(predicted, "objects")),
            count(field(predicted, "edges")),
            count(field(predicted, "bytes")),
        );
        eprintln!(
            "opener {id}: native ({}, {}, {}) predicted {expected:?}",
            used.objects, used.edges, used.bytes
        );
        assert_eq!((used.objects, used.edges, used.bytes), expected, "{id}");
        checked += 1;
    }
    assert_eq!(checked, 3);
}

/// B2-b's T2 census margin test, extended to the snapshot ledger's object,
/// edge and byte caps (M3-C r8 item 2 as M3-C r9 amends it; unit C1a4). Each
/// lead-readable entry of the companion census is classified again against
/// the compiled snapshot profile, at the 2x margin on its full ledger (the
/// walk, the session, sealing at its envelope and the leftover copy). Every
/// measured entry must pass: a failure returns the caps to the law. An
/// over-item-5 entry claims no margin. The census covers discovery's
/// manifest.
#[test]
fn the_snapshot_census_is_classified_against_the_snapshot_profile_and_every_measured_entry_passes()
{
    use opensip_identity::{JsonValue as V, parse_json};
    use oracle::{field, get, items, text};
    const CENSUS: &[u8] = include_bytes!("snapshot_ledger_census.json");
    const DISCOVERY: &[u8] = include_bytes!("custody/discovery_census.json");
    let body = parse_json(CENSUS).unwrap();
    let discovery = parse_json(DISCOVERY).unwrap();
    assert_eq!(
        text(field(field(&body, "manifest"), "sha256")),
        text(field(field(&discovery, "manifest"), "sha256"))
    );
    let count = |v: &V| -> usize {
        match v {
            V::Integer(i) => usize::try_from(i.get()).unwrap(),
            _ => panic!("not an integer"),
        }
    };
    let triple = |v: &V| {
        (
            count(field(v, "objects")),
            count(field(v, "edges")),
            count(field(v, "bytes")),
        )
    };
    // One fresh profile ledger charged exactly that, never the record's copy.
    let fits = |(objects, edges, bytes): (usize, usize, usize)| {
        WorkLedger::snapshot_profile()
            .charge::<()>(WorkCost {
                objects,
                edges,
                bytes,
            })
            .is_ok()
    };
    // The record's caps are the compiled profile's own.
    let (o, e, b) = triple(field(field(&body, "caps"), "snapshotProfile"));
    assert!(fits((o, e, b)));
    assert!(!fits((o + 1, 0, 0)) && !fits((0, e + 1, 0)) && !fits((0, 0, b + 1)));
    let (mut measured, mut over) = (0, 0);
    for list in ["entries", "workspaces"] {
        for row in items(field(&body, list)) {
            let id = text(field(row, "id"));
            let (fo, fe, fb) = triple(field(row, "fullLedger"));
            match text(field(row, "status")) {
                "measured" => {
                    let passes = fits((2 * fo, 2 * fe, 2 * fb));
                    let margin = field(field(row, "margins"), "snapshotProfile");
                    assert!(
                        matches!(field(margin, "passes2x"), V::Bool(p) if *p == passes),
                        "{id}"
                    );
                    assert!(passes, "{id}: fails the snapshot profile's 2x margin");
                    measured += 1;
                }
                "over-item-5" => {
                    assert!(get(row, "margins").is_none(), "{id}");
                    over += 1;
                }
                other => panic!("{id}: {other}"),
            }
        }
    }
    let counts = field(&body, "counts");
    assert_eq!(measured, count(field(counts, "measured")));
    assert_eq!(over, count(field(counts, "overItem5")));
    assert!(measured > 0);
    // Unit C1a4-blind (Codex C1A4-R1-NBO-2): the record's coverage is checked
    // against discovery's compiled record, not its own counts. Its
    // lead-readable ids are unique and are exactly discovery's lead-readable
    // repository rows and workspaces, in order; its held-out ids are exactly
    // discovery's held-out rows, in order.
    let ids = |rows: &[V]| -> Vec<String> {
        rows.iter()
            .map(|row| text(field(row, "id")).to_owned())
            .collect()
    };
    let held_out = |row: &V| matches!(get(row, "status"), Some(V::String(_)));
    let discovery_entries = items(field(&discovery, "entries"));
    let mut readable = ids(items(field(&body, "entries")));
    readable.extend(ids(items(field(&body, "workspaces"))));
    let mut expected: Vec<String> = discovery_entries
        .iter()
        .filter(|row| !held_out(row))
        .map(|row| text(field(row, "id")).to_owned())
        .collect();
    expected.extend(ids(items(field(&discovery, "workspaces"))));
    let unique: std::collections::BTreeSet<&String> = readable.iter().collect();
    assert_eq!(unique.len(), readable.len(), "a duplicated id");
    assert_eq!(readable, expected);
    let held_rows = items(field(&body, "heldOutEntries"));
    let held_expected: Vec<String> = discovery_entries
        .iter()
        .filter(|row| held_out(row))
        .map(|row| text(field(row, "id")).to_owned())
        .collect();
    assert!(!held_expected.is_empty());
    assert_eq!(ids(held_rows), held_expected);
    assert_eq!(held_rows.len(), count(field(counts, "heldOut")));
    // The held-out rows, composed from the companion blind receipt only while
    // it is current: all outstanding, or all the receipt's closed rows, with
    // the record's state the receipt's.
    let failing: Vec<&str> = items(field(field(&body, "failing2x"), "snapshotProfile"))
        .iter()
        .map(text)
        .collect();
    let (mut blind, mut errors, mut blind_failing) = (0, 0, 0);
    for row in held_rows {
        let id = text(field(row, "id"));
        match text(field(row, "status")) {
            "outstanding: held-out" | "outstanding: held-out (blind receipt stale)" => {}
            "blind-census" => {
                blind += 1;
                let result = field(row, "result");
                let V::Object(fields) = result else {
                    panic!("{id}")
                };
                let mut keys: Vec<&str> = fields.keys().map(String::as_str).collect();
                keys.sort_unstable();
                match text(field(result, "status")) {
                    "measured" => {
                        assert_eq!(
                            keys,
                            [
                                "integrity",
                                "marginPermille",
                                "passes2x",
                                "population",
                                "status"
                            ],
                            "{id}"
                        );
                        assert!(matches!(field(result, "integrity"), V::Bool(true)), "{id}");
                        assert!(matches!(field(result, "population"), V::Bool(true)), "{id}");
                        let margins = field(result, "marginPermille");
                        let V::Object(dimensions) = margins else {
                            panic!("{id}")
                        };
                        assert_eq!(dimensions.len(), 3, "{id}");
                        let passes = ["objects", "edges", "bytes"]
                            .iter()
                            .all(|d| count(field(margins, d)) >= 2000);
                        assert!(
                            matches!(field(result, "passes2x"), V::Bool(b) if *b == passes),
                            "{id}"
                        );
                        assert_eq!(failing.contains(&id), !passes, "{id}");
                        if !passes {
                            blind_failing += 1;
                        }
                    }
                    "over-item-5" => {
                        assert_eq!(keys, ["integrity", "population", "status"], "{id}");
                    }
                    "error" => {
                        assert_eq!(keys, ["errorClass", "status"], "{id}");
                        assert!(
                            ["INTEGRITY", "POPULATION", "MODEL", "IO"]
                                .contains(&text(field(result, "errorClass"))),
                            "{id}"
                        );
                        errors += 1;
                    }
                    other => panic!("{id}: {other}"),
                }
            }
            other => panic!("{id}: {other}"),
        }
    }
    let state = text(field(&body, "heldOutMargin"));
    if blind == 0 {
        assert_eq!(state, "outstanding");
    } else {
        assert_eq!(blind, held_rows.len(), "a partly composed receipt");
        let derived = if errors > 0 {
            "incomplete (blind census)"
        } else if blind_failing > 0 {
            "fails (blind census)"
        } else {
            "holds (blind census)"
        };
        assert_eq!(state, derived);
    }
    assert_eq!(
        text(field(&body, "capsStatus")),
        if failing.is_empty() {
            "recorded-margin-holds"
        } else {
            "returned-to-law"
        }
    );
}

// ------------------------------------------------------------------ unit C1c-0 (M3-C r8 item 3)

fn custody_now() -> (SnapshotCustody<'static>, &'static AuthorizedGroups) {
    let groups: &'static AuthorizedGroups =
        Box::leak(Box::new(AuthorizedGroups::from_invocation(&[]).unwrap()));
    (SnapshotCustody::new(uid(), groups.as_set(), None), groups)
}

/// Open `path` with the pruned-tree opener over `root`, with `members`.
fn open_pruned_at(root: &Path, path: &str, members: &[&str]) -> Result<String, String> {
    let lent = Lent::new(root);
    let (custody, _) = custody_now();
    let bounds = boundaries(&[], &[]);
    let members: BTreeSet<String> = members.iter().map(|m| (*m).to_owned()).collect();
    let extent = extent_of(&bounds, &members, &[]).unwrap();
    WorkLedger::discovery_profile()
        .scope(|work| {
            crate::snapshot_read_set::open_pruned(&lent.root(), path, &extent, custody, work)
        })
        .map(|source| source.path().to_owned())
        .map_err(|f| format!("{f:?}"))
}

/// Unit C1c-0 (C1c plan r4, LD-C1C-2): the pruned-tree opener's charge, for
/// an installed manifest at the root's dependency tree, one under a
/// first-party directory and a nested package's, equals the model's
/// prediction exactly: custody judged only above the dependency anchor, and
/// no marker custody below it.
#[test]
fn the_pruned_tree_opener_charges_exactly_the_models_prediction() {
    use opensip_identity::{JsonValue as V, parse_json};
    use oracle::{field, items, materialize, text};
    const PREDICTIONS: &[u8] = include_bytes!("snapshot_ledger_vectors.json");
    let body = parse_json(PREDICTIONS).unwrap();
    let count = |v: &V| -> usize {
        match v {
            V::Integer(i) => usize::try_from(i.get()).unwrap(),
            _ => panic!("not an integer"),
        }
    };
    let mut checked = 0;
    for case in items(field(&body, "prunedOpeners")) {
        let (id, path) = (text(field(case, "id")), text(field(case, "path")));
        assert!(matches!(field(case, "exact"), V::Bool(true)), "{id}");
        let (_s, root) = scratch();
        let links = root.parent().unwrap().join("links");
        dir(&links);
        materialize(&root, &links, items(field(case, "tree")));
        let lent = Lent::new(&root);
        let (custody, _) = custody_now();
        let bounds = boundaries(&[], &[]);
        let members = BTreeSet::new();
        let extent = extent_of(&bounds, &members, &[]).unwrap();
        let mut ledger = WorkLedger::discovery_profile();
        let opened = ledger
            .scope(|work| {
                crate::snapshot_read_set::open_pruned(&lent.root(), path, &extent, custody, work)
            })
            .unwrap_or_else(|f| panic!("{id}: {f:?}"));
        assert_eq!(opened.path(), path);
        assert!(
            !opened.is_marker(),
            "{id}: no marker custody below the anchor"
        );
        let used = ledger.used();
        let predicted = field(case, "predicted");
        let expected = (
            count(field(predicted, "objects")),
            count(field(predicted, "edges")),
            count(field(predicted, "bytes")),
        );
        eprintln!(
            "pruned opener {id}: native ({}, {}, {}) predicted {expected:?}",
            used.objects, used.edges, used.bytes
        );
        assert_eq!((used.objects, used.edges, used.bytes), expected, "{id}");
        checked += 1;
    }
    assert_eq!(checked, 3);
}

/// Unit C1c-0 (LD-C1C-2; SL:266): S3 directory custody holds above the
/// dependency anchor and is not judged at or below it. A group-writable
/// first-party directory refuses; a group-writable installed package is read.
#[test]
fn the_pruned_tree_opener_judges_custody_above_the_anchor_only() {
    let (_s, root) = scratch();
    file(&root.join("node_modules/a/package.json"), b"{}");
    std::fs::set_permissions(
        root.join("node_modules/a"),
        std::fs::Permissions::from_mode(0o775),
    )
    .unwrap();
    assert_eq!(
        open_pruned_at(&root, "node_modules/a/package.json", &[]).unwrap(),
        "node_modules/a/package.json"
    );
    file(&root.join("web/node_modules/b/package.json"), b"{}");
    std::fs::set_permissions(root.join("web"), std::fs::Permissions::from_mode(0o775)).unwrap();
    let refused = open_pruned_at(&root, "web/node_modules/b/package.json", &[]).unwrap_err();
    assert!(
        refused.contains("Custody") && refused.contains("\"web\""),
        "{refused}"
    );
}

/// Unit C1c-0: the opener places its path by the shared rule before any
/// open. A first-party path is outside; a VCS segment or the root's or a
/// member's `.opensip` anchor excludes; a symlinked component below the
/// anchor is never followed.
#[test]
fn the_pruned_tree_opener_refuses_paths_the_read_set_may_not_reach() {
    let (_s, root) = scratch();
    file(&root.join("packages/a/package.json"), b"{}");
    file(&root.join("node_modules/a/.git/package.json"), b"{}");
    file(&root.join("m/.opensip/node_modules/a/package.json"), b"{}");
    file(&root.join("real/package.json"), b"{}");
    dir(&root.join("node_modules"));
    std::os::unix::fs::symlink(root.join("real"), root.join("node_modules/link")).unwrap();
    for (path, expected) in [
        ("packages/a/package.json", "outside-dependency-tree"),
        ("node_modules/a/.git/package.json", "vcs-tree"),
        (
            "m/.opensip/node_modules/a/package.json",
            "opensip-custody-state",
        ),
    ] {
        let refused = open_pruned_at(&root, path, &["m"]).unwrap_err();
        assert!(refused.contains(expected), "{path}: {refused}");
    }
    let refused = open_pruned_at(&root, "node_modules/link/package.json", &[]).unwrap_err();
    assert!(refused.contains("NotARegularFile"), "{refused}");
}

/// Unit C1c-0: the descriptor discipline below the anchor. A manifest
/// replaced between its observation and its open refuses `Changed`, never
/// retried.
#[test]
fn a_pruned_tree_manifest_replaced_before_its_open_refuses() {
    let (_s, root) = scratch();
    file(&root.join("node_modules/a/package.json"), b"{}");
    let swap_root = root.clone();
    set_before_open(Some(Box::new(move |rel: &str| {
        if rel == "node_modules/a/package.json" {
            let target = swap_root.join("node_modules/a/package.json");
            std::fs::remove_file(&target).unwrap();
            std::fs::write(&target, b"{\"x\":1}").unwrap();
        }
    })));
    let refused = open_pruned_at(&root, "node_modules/a/package.json", &[]).unwrap_err();
    set_before_open(None);
    assert!(refused.contains("Changed"), "{refused}");
}

/// Unit C1c-0 (LD-C1C-13): the walk's evidence. Every first-party Cargo root
/// the walk derived is kept, siblings' included, and the admitted member
/// roots are copied; the walk's handed files are those `walk_snapshot`
/// hands, and its charge is the same.
#[test]
fn the_walk_keeps_every_first_party_cargo_root_and_copies_the_member_roots() {
    let (_s, root) = scratch();
    file(&root.join("Cargo.toml"), b"[workspace]\n");
    file(&root.join("a/Cargo.toml"), b"[package]\n");
    file(&root.join("a/src/lib.rs"), b"");
    file(&root.join("b/Cargo.toml"), b"[package]\n");
    file(&root.join("b/target/x"), b"x");
    file(&root.join("m/package.json"), b"{}");
    let lent = Lent::new(&root);
    let (custody, _) = custody_now();
    let bounds = boundaries(&[], &[]);
    let members: BTreeSet<String> = ["m".to_owned()].into_iter().collect();
    let extent = extent_of(&bounds, &members, &[]).unwrap();
    let mut handed = Vec::new();
    let mut visit = |source: SourceFile, _: &mut WorkScope<'_>| -> Result<(), String> {
        handed.push(source.path().to_owned());
        Ok(())
    };
    let mut retaining = WorkLedger::discovery_profile();
    let (_, evidence) = retaining
        .scope(|work| walk_snapshot_retaining(&lent.root(), custody, &extent, &mut visit, work))
        .unwrap();
    let roots: Vec<&str> = evidence.cargo_roots().iter().map(String::as_str).collect();
    assert_eq!(roots, ["", "a", "b"]);
    assert_eq!(evidence.member_roots(), &members);
    assert!(!handed.iter().any(|p| p.starts_with("b/target")));
    let mut plain_visit = |_: SourceFile, _: &mut WorkScope<'_>| -> Result<(), String> { Ok(()) };
    let mut plain = WorkLedger::discovery_profile();
    plain
        .scope(|work| walk_snapshot(&lent.root(), custody, &extent, &mut plain_visit, work))
        .unwrap();
    assert_eq!(retaining.used(), plain.used());
}

/// Unit C1c-0 (LD-C1C-13): the dependency-tree Cargo marker observation. A
/// regular `Cargo.toml` in a dependency tree makes a root; a symlinked one,
/// none, or one outside a dependency tree does not; nothing is read.
#[test]
fn a_dependency_tree_cargo_root_is_observed_without_a_read() {
    let (_s, root) = scratch();
    file(&root.join("node_modules/a/Cargo.toml"), b"[package]\n");
    file(&root.join("node_modules/b/x"), b"");
    file(&root.join("node_modules/c/real.toml"), b"");
    std::os::unix::fs::symlink(
        root.join("node_modules/c/real.toml"),
        root.join("node_modules/c/Cargo.toml"),
    )
    .unwrap();
    file(&root.join("crates/d/Cargo.toml"), b"[package]\n");
    let observe = |rel: &str| {
        let held = RetainedDirectoryPath::open_project_root(&root.join(rel), 256).unwrap();
        WorkLedger::discovery_profile()
            .scope(|work| {
                crate::snapshot_read_set::observes_dependency_cargo_root(
                    held.directory(),
                    rel,
                    work,
                )
            })
            .unwrap()
    };
    assert!(observe("node_modules/a"));
    assert!(!observe("node_modules/b"));
    assert!(!observe("node_modules/c"));
    assert!(!observe("crates/d"));
}

/// Unit C1c-0 (LD-C1C-5): the read set's authorization is the shared rule's
/// over the walk's own evidence, charged exactly its published cost.
#[test]
fn the_read_set_authorization_uses_the_walks_evidence_and_charges_its_cost() {
    use crate::snapshot_read_set::{ReadAuthorization, authorize_read, read_set_path_cost};
    let (_s, root) = scratch();
    file(&root.join("Cargo.toml"), b"[workspace]\n");
    file(&root.join("m/package.json"), b"{}");
    let lent = Lent::new(&root);
    let (custody, _) = custody_now();
    let bounds = boundaries(&[], &[]);
    let members: BTreeSet<String> = ["m".to_owned()].into_iter().collect();
    let extent = extent_of(&bounds, &members, &[]).unwrap();
    let mut visit = |_: SourceFile, _: &mut WorkScope<'_>| -> Result<(), String> { Ok(()) };
    let (_, evidence) = WorkLedger::discovery_profile()
        .scope(|work| walk_snapshot_retaining(&lent.root(), custody, &extent, &mut visit, work))
        .unwrap();
    let dependency = BTreeSet::new();
    for (authorized, relative, expected) in [
        ("node_modules/a", "lib/x.ts", ReadAuthorization::Admitted),
        (
            "target/node_modules/a",
            "x.js",
            ReadAuthorization::Excluded("cargo-build-output"),
        ),
        (
            "m/.opensip/node_modules/a",
            "x.js",
            ReadAuthorization::Excluded("opensip-custody-state"),
        ),
    ] {
        let mut ledger = WorkLedger::discovery_profile();
        let got = ledger
            .scope(|work| authorize_read(authorized, relative, &evidence, &dependency, work))
            .unwrap();
        assert_eq!(got, expected, "{authorized} {relative}");
        let cost = read_set_path_cost(authorized, relative);
        assert_eq!(
            (
                ledger.used().objects,
                ledger.used().edges,
                ledger.used().bytes
            ),
            (cost.objects, cost.edges, cost.bytes)
        );
    }
}
