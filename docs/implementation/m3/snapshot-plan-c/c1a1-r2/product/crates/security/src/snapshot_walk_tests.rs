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
    let extent = SnapshotExtent::new(bounds, &members, &ignore).unwrap();
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
    assert!(SnapshotExtent::new(&bounds, &members, &["../x".to_owned()]).is_err());
    assert!(SnapshotExtent::new(&bounds, &members, &["a//b".to_owned()]).is_err());
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
            let extent = SnapshotExtent::new(&bounds, &members, &[]).unwrap();
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
        let extent = SnapshotExtent::new(&bounds, &members, &[]).unwrap();
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
