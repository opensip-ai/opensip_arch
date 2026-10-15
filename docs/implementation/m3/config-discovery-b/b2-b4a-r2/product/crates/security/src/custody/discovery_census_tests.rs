// Unit B2-b4a's controls (B2-b4 plan r2 sections 1.4 and 1.6). The soundness
// control walks every accepted walk vector, and every composed-workspace
// vector, natively on a fresh discovery ledger and asserts that the walker
// used no more objects and edges than tools/security/discovery_census.py's
// cost model predicts. The margin control classifies every censused T2 entry
// against the discovery profile's own limits. Every tree is a scratch tree
// under the APFS test premise; nothing reads the real home, a real repository
// or the T2 cache. The helpers repeat the closed walk tests' own
// (`discovery_walk_tests.rs`), which this unit does not modify.
use super::discovery_rule::MarkerCountBasis;
use super::discovery_scan::{
    DiscoveryInvocation, UnitSourceRequest, UpwardProvenance, VcsRecord, WalkRow,
};
use super::discovery_walk::discover_downward;
use super::project_chain::DiscoveryRoot;
use crate::grants::{AuthorizedGroups, ProjectOwnerWaiver};
use crate::initial_installation::InitialInstallationAttempt;
use crate::trust::AclOmissionPremise;
use opensip_identity::{JsonValue as V, parse_json, raw_sha256};
use opensip_platform::{RetainedDirectoryPath, WorkCost, WorkLedger};
use std::collections::BTreeSet;
use std::os::unix::fs::{MetadataExt, PermissionsExt};
use std::path::{Path, PathBuf};
use std::sync::atomic::AtomicBool;

const WALK_VECTORS: &[u8] = include_bytes!("discovery_walk_vectors.json");
const CENSUS_VECTORS: &[u8] = include_bytes!("discovery_census_vectors.json");
const CENSUS: &[u8] = include_bytes!("discovery_census.json");
/// The transitive cost closure the census pins (plan r2 section 1.3), as
/// the code is compiled.
const CLOSURE: [(&str, &[u8]); 15] = [
    (
        "crates/security/src/custody/discovery_walk.rs",
        include_bytes!("discovery_walk.rs"),
    ),
    (
        "crates/security/src/custody/project_admission.rs",
        include_bytes!("project_admission.rs"),
    ),
    (
        "crates/security/src/custody/project_chain.rs",
        include_bytes!("project_chain.rs"),
    ),
    (
        "crates/security/src/trust/initial_platform.rs",
        include_bytes!("../trust/initial_platform.rs"),
    ),
    (
        "crates/security/src/custody/discovery_scan.rs",
        include_bytes!("discovery_scan.rs"),
    ),
    (
        "crates/security/src/custody/discovery_rule.rs",
        include_bytes!("discovery_rule.rs"),
    ),
    (
        "crates/security/src/custody.rs",
        include_bytes!("../custody.rs"),
    ),
    (
        "crates/platform/src/filesystem/directory_open.rs",
        include_bytes!("../../../platform/src/filesystem/directory_open.rs"),
    ),
    (
        "crates/platform/src/filesystem/path_binding.rs",
        include_bytes!("../../../platform/src/filesystem/path_binding.rs"),
    ),
    (
        "crates/platform/src/filesystem.rs",
        include_bytes!("../../../platform/src/filesystem.rs"),
    ),
    (
        "crates/platform/src/filesystem/descriptor_acl_capture.rs",
        include_bytes!("../../../platform/src/filesystem/descriptor_acl_capture.rs"),
    ),
    (
        "crates/platform/src/filesystem/descriptor_filesystem.rs",
        include_bytes!("../../../platform/src/filesystem/descriptor_filesystem.rs"),
    ),
    (
        "crates/platform/src/filesystem/directory_entries.rs",
        include_bytes!("../../../platform/src/filesystem/directory_entries.rs"),
    ),
    (
        "crates/platform/src/work_reader.rs",
        include_bytes!("../../../platform/src/work_reader.rs"),
    ),
    (
        "crates/platform/src/work_ledger.rs",
        include_bytes!("../../../platform/src/work_ledger.rs"),
    ),
];
/// An invoking user who owns nothing in a scratch tree (`foreign` cases).
const FOREIGN_UID: u32 = 4242;
/// A group that authorizes nothing in a scratch tree (`groups: other`).
const OTHER_GID: u32 = 4243;

// ---------------------------------------------------------------- helpers

struct Scratch(PathBuf);
impl Drop for Scratch {
    fn drop(&mut self) {
        let _ = std::process::Command::new("/bin/chmod")
            .args(["-R", "-N"])
            .arg(&self.0)
            .stderr(std::process::Stdio::null())
            .status();
        let _ = std::process::Command::new("/bin/chmod")
            .args(["-R", "u+rwX"])
            .arg(&self.0)
            .stderr(std::process::Stdio::null())
            .status();
        let _ = std::fs::remove_dir_all(&self.0);
    }
}
/// A scratch directory holding the root `w` (0755) and a `links` directory
/// for hard links, on its canonical path.
fn scratch() -> (Scratch, PathBuf) {
    let nonce: String = opensip_platform::request_entropy()
        .unwrap()
        .iter()
        .map(|b| format!("{b:02x}"))
        .collect();
    let base = crate::test_scratch::temp_dir().join(format!("opensip-b2b4a-{nonce}"));
    std::fs::create_dir(&base).unwrap();
    std::fs::set_permissions(&base, std::fs::Permissions::from_mode(0o700)).unwrap();
    let base = std::fs::canonicalize(&base).unwrap();
    directory(&base.join("links"), 0o700);
    let root = base.join("w");
    directory(&root, 0o755);
    (Scratch(base), root)
}
fn directory(path: &Path, mode: u32) {
    std::fs::create_dir(path).unwrap();
    std::fs::set_permissions(path, std::fs::Permissions::from_mode(mode)).unwrap();
}
fn file(path: &Path, bytes: &[u8], mode: u32) {
    std::fs::write(path, bytes).unwrap();
    std::fs::set_permissions(path, std::fs::Permissions::from_mode(mode)).unwrap();
}
fn uid() -> u32 {
    std::fs::metadata(crate::test_scratch::temp_dir())
        .unwrap()
        .uid()
}
fn premise() -> AclOmissionPremise {
    let flag = Box::leak(Box::new(AtomicBool::new(false)));
    let attempt = InitialInstallationAttempt::for_tests(flag, None).unwrap();
    AclOmissionPremise::for_tests(&attempt, &[b"apfs"])
}
fn grant(path: &Path, who: &str, directory: bool) {
    let principal = if who == "user" {
        "user:nobody"
    } else {
        "group:everyone"
    };
    let right = if directory { "add_file" } else { "write" };
    let status = std::process::Command::new("/bin/chmod")
        .arg("+a")
        .arg(format!("{principal} allow {right}"))
        .arg(path)
        .status()
        .unwrap();
    assert!(status.success());
}

fn field<'v>(value: &'v V, key: &str) -> &'v V {
    let V::Object(fields) = value else {
        panic!("{value:?}")
    };
    fields.get(key).unwrap_or(&V::Null)
}
fn text(value: &V) -> &str {
    let V::String(s) = value else {
        panic!("{value:?}")
    };
    s
}
fn items(value: &V) -> &[V] {
    let V::Array(items) = value else {
        panic!("{value:?}")
    };
    items
}
fn number(value: &V) -> usize {
    let V::Integer(n) = value else {
        panic!("{value:?}")
    };
    usize::try_from(n.get()).unwrap()
}
fn optional(value: &V) -> Option<String> {
    match value {
        V::Null => None,
        other => Some(text(other).to_owned()),
    }
}
fn flag(value: &V) -> bool {
    matches!(value, V::Bool(true))
}

/// Build a description under `root`; hard links go to `links`.
fn materialize(root: &Path, links: &Path, tree: &[V]) {
    for (index, entry) in tree.iter().enumerate() {
        let path = root.join(text(field(entry, "path")));
        let mode = || u32::from_str_radix(text(field(entry, "mode")), 8).unwrap();
        let kind = text(field(entry, "kind"));
        match kind {
            "dir" => directory(&path, mode()),
            "file" => {
                file(&path, text(field(entry, "text")).as_bytes(), mode());
                if flag(field(entry, "hardlink")) {
                    std::fs::hard_link(&path, links.join(index.to_string())).unwrap();
                }
            }
            "symlink" => std::os::unix::fs::symlink(text(field(entry, "target")), &path).unwrap(),
            "fifo" => {
                let status = std::process::Command::new("/usr/bin/mkfifo")
                    .arg("-m")
                    .arg(text(field(entry, "mode")))
                    .arg(&path)
                    .status()
                    .unwrap();
                assert!(status.success());
            }
            "socket" => {
                // Bound under a short name (a socket path has a 104-byte
                // bound), dropped, then renamed into place: the file stays.
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
        if let V::String(who) = field(entry, "acl") {
            grant(&path, who, kind == "dir");
        }
    }
}

/// The lent test root over a scratch directory.
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
    fn root(&self) -> DiscoveryRoot<'_> {
        DiscoveryRoot::for_tests(self.path.directory(), &self.spelling, Some(&self.premise))
    }
}

fn source_of(case: &V) -> UnitSourceRequest {
    let roots = || {
        items(field(case, "roots"))
            .iter()
            .map(|r| text(r).to_owned())
            .collect()
    };
    match text(field(case, "source")) {
        "explicit-joins" => UnitSourceRequest::ExplicitJoins(roots()),
        "config-workspace-roots" => UnitSourceRequest::ConfigWorkspaceRoots(roots()),
        _ => UnitSourceRequest::Automatic,
    }
}
fn upward_of(upward: &V) -> UpwardProvenance {
    UpwardProvenance {
        mode: text(field(upward, "mode")).to_owned(),
        config_path: optional(field(upward, "configPath")),
        walked: items(field(upward, "walked"))
            .iter()
            .map(|w| WalkRow {
                path: text(field(w, "path")).to_owned(),
                custody: text(field(w, "custody")).to_owned(),
                candidate: text(field(w, "candidate")).to_owned(),
                boundary: optional(field(w, "boundary")),
            })
            .collect(),
        stop_reason: text(field(upward, "stopReason")).to_owned(),
        vcs: match field(upward, "vcs") {
            V::Null => None,
            v => Some(VcsRecord {
                kind: if text(field(v, "kind")) == "directory" {
                    "directory"
                } else {
                    "indirection"
                },
                target: optional(field(v, "target")),
            }),
        },
        explicit_path_was_symlink: match field(upward, "explicitPathWasSymlink") {
            V::Bool(b) => Some(*b),
            _ => None,
        },
    }
}

/// One `discover_downward` over a built tree on a fresh ledger (the
/// discovery profile, or `limits`): whether it completed, and what the
/// ledger was charged. A typed discovery refusal is a completed result.
fn charged(root: &Path, case: &V, upward: &V, limits: Option<WorkCost>) -> (bool, WorkCost) {
    let lent = Lent::new(root);
    let own = std::fs::metadata(root).unwrap().gid();
    assert_ne!(own, OTHER_GID);
    let gids: Vec<u32> = match field(case, "groups") {
        V::String(g) if g == "own" => vec![own],
        V::String(g) if g == "other" => vec![OTHER_GID],
        _ => Vec::new(),
    };
    let groups = AuthorizedGroups::from_invocation(&gids).unwrap();
    let waiver =
        ProjectOwnerWaiver::from_invocation(flag(field(case, "waive")), Some(root)).unwrap();
    let invoking = if flag(field(case, "foreign")) {
        FOREIGN_UID
    } else {
        uid()
    };
    let members = BTreeSet::new();
    let invocation = DiscoveryInvocation {
        invoking_uid: invoking,
        ci: false,
        groups: &groups,
        waiver: waiver.as_ref(),
        source: source_of(case),
        basis: MarkerCountBasis::NotEnumerated,
        member_roots: &members,
    };
    let mut ledger = match limits {
        Some(limits) => WorkLedger::with_limits(limits).unwrap(),
        None => WorkLedger::discovery_profile(),
    };
    let completed = ledger
        .scope(|work| discover_downward(&lent.root(), upward_of(upward), &invocation, work))
        .is_ok();
    (completed, ledger.used())
}

fn by_id<'v>(cases: &'v [V], id: &str) -> &'v V {
    let hits: Vec<&V> = cases
        .iter()
        .filter(|c| text(field(c, "id")) == id)
        .collect();
    assert_eq!(hits.len(), 1, "{id}");
    hits[0]
}
/// The soundness verdict for one native measurement (r2, Codex
/// B2B4A-R1-RF-3): a walk that stopped early measured nothing, so it never
/// passes, whatever it was charged.
fn soundness(
    id: &str,
    completed: bool,
    used: WorkCost,
    objects: usize,
    edges: usize,
) -> Result<(), String> {
    if !completed {
        return Err(format!("{id}: the native walk did not complete"));
    }
    if used.objects > objects || used.edges > edges {
        return Err(format!(
            "{id}: the walker used {} objects and {} edges; the model predicts {objects} and {edges}",
            used.objects, used.edges
        ));
    }
    Ok(())
}
fn hex(digest: &[u8; 32]) -> String {
    digest.iter().map(|b| format!("{b:02x}")).collect()
}

// ----------------------------------------------------- the soundness control

#[test]
fn the_cost_model_bounds_the_native_walker_on_every_walk_vector() {
    let walk = parse_json(WALK_VECTORS).unwrap();
    let census = parse_json(CENSUS_VECTORS).unwrap();
    // The predictions are for these exact vectors.
    let pinned = field(&census, "walkVectors");
    assert_eq!(number(field(pinned, "bytes")), WALK_VECTORS.len());
    assert_eq!(
        text(field(pinned, "sha256")),
        hex(&raw_sha256(WALK_VECTORS))
    );
    let cases = items(field(&walk, "cases"));
    let predictions = items(field(&census, "walkCases"));
    assert_eq!(cases.len(), predictions.len());
    for case in cases {
        let id = text(field(case, "id"));
        let predicted = by_id(predictions, id);
        let (_s, root) = scratch();
        let links = root.parent().unwrap().join("links");
        materialize(&root, &links, items(field(case, "tree")));
        let (completed, used) = charged(&root, case, field(case, "upward"), None);
        let (objects, edges) = (
            number(field(predicted, "objects")),
            number(field(predicted, "edges")),
        );
        soundness(id, completed, used, objects, edges).unwrap();
        // The tightness, for review (plan r2 section 1.4).
        println!(
            "census-soundness {id} used {} {} predicted {objects} {edges}",
            used.objects, used.edges
        );
    }
}

#[test]
fn the_cost_model_bounds_the_native_walker_on_composed_workspaces() {
    let walk = parse_json(WALK_VECTORS).unwrap();
    let census = parse_json(CENSUS_VECTORS).unwrap();
    // Every composed case is an automatic walk from the explicit root, as
    // the empty-root vector's upward record states it.
    let upward = field(by_id(items(field(&walk, "cases")), "empty-root"), "upward");
    let composed = items(field(&census, "composedCases"));
    assert!(composed.len() >= 4);
    for case in composed {
        let id = text(field(case, "id"));
        let (_s, root) = scratch();
        let links = root.parent().unwrap().join("links");
        materialize(&root, &links, items(field(case, "tree")));
        let (completed, used) = charged(&root, case, upward, None);
        let (objects, edges) = (number(field(case, "objects")), number(field(case, "edges")));
        soundness(id, completed, used, objects, edges).unwrap();
        // The tightness, for review (plan r2 section 1.4).
        println!(
            "census-soundness {id} used {} {} predicted {objects} {edges}",
            used.objects, used.edges
        );
    }
}

#[test]
fn an_aborted_native_measurement_never_passes_as_soundness() {
    // r2 (Codex B2B4A-R1-RF-3): a walk stopped by a small ledger is charged
    // less than the prediction, and is still refused.
    let walk = parse_json(WALK_VECTORS).unwrap();
    let census = parse_json(CENSUS_VECTORS).unwrap();
    let case = by_id(items(field(&walk, "cases")), "units-at-root-and-below");
    let predicted = by_id(
        items(field(&census, "walkCases")),
        "units-at-root-and-below",
    );
    let (_s, root) = scratch();
    let links = root.parent().unwrap().join("links");
    materialize(&root, &links, items(field(case, "tree")));
    let small = WorkCost {
        objects: 10,
        edges: 10,
        bytes: 1 << 20,
    };
    let (completed, used) = charged(&root, case, field(case, "upward"), Some(small));
    let (objects, edges) = (
        number(field(predicted, "objects")),
        number(field(predicted, "edges")),
    );
    assert!(!completed);
    assert!(used.objects <= objects && used.edges <= edges);
    assert!(soundness("aborted", completed, used, objects, edges).is_err());
}

// ----------------------------------------------------- the census record

#[test]
fn the_census_pins_the_cost_closure_as_compiled() {
    for body in [CENSUS_VECTORS, CENSUS] {
        let body = parse_json(body).unwrap();
        let rows = items(field(&body, "closure"));
        assert_eq!(rows.len(), CLOSURE.len());
        for (row, (path, bytes)) in rows.iter().zip(CLOSURE) {
            assert_eq!(text(field(row, "path")), path);
            assert_eq!(number(field(row, "bytes")), bytes.len(), "{path}");
            assert_eq!(
                text(field(row, "sha256")),
                hex(&raw_sha256(bytes)),
                "{path}"
            );
        }
    }
}

/// Whether twice an entry's cost fits the discovery profile's own limits:
/// one fresh ledger charged exactly that, never the record's copy.
fn fits_twice(objects: usize, edges: usize) -> bool {
    WorkLedger::discovery_profile()
        .charge::<()>(WorkCost {
            objects: 2 * objects,
            edges: 2 * edges,
            bytes: 0,
        })
        .is_ok()
}

#[test]
fn the_census_margin_is_classified_against_the_profile_limits_and_never_claimed_for_a_failing_entry()
 {
    let body = parse_json(CENSUS).unwrap();
    let mut failing = Vec::new();
    let mut held_out = 0;
    for list in ["entries", "workspaces"] {
        for row in items(field(&body, list)) {
            let id = text(field(row, "id")).to_owned();
            if let V::String(status) = field(row, "status") {
                assert_eq!(status, "outstanding: held-out", "{id}");
                held_out += 1;
                continue;
            }
            let fits = fits_twice(number(field(row, "objects")), number(field(row, "edges")));
            assert_eq!(flag(field(row, "passes2x")), fits, "{id}");
            if !fits {
                failing.push(id);
            }
        }
    }
    assert_eq!(held_out, 10);
    let recorded: Vec<String> = items(field(&body, "failingEntries"))
        .iter()
        .map(|v| text(v).to_owned())
        .collect();
    assert_eq!(recorded, failing);
    // A failing entry returns the caps to the law (M3-B r5 item 12): the
    // record never claims the margin.
    let caps = text(field(&body, "caps"));
    if failing.is_empty() {
        assert_eq!(caps, "margin-holds-for-lead-readable-entries");
    } else {
        assert_eq!(caps, "returned-to-law");
    }
    assert_eq!(text(field(&body, "heldOutMargin")), "outstanding");
    // The record's limits are the profile's: exactly the largest charge a
    // fresh discovery ledger admits.
    let limits = field(&body, "limits");
    let (objects, edges) = (
        number(field(limits, "objects")),
        number(field(limits, "edges")),
    );
    let admits = |o, e| {
        WorkLedger::discovery_profile()
            .charge::<()>(WorkCost {
                objects: o,
                edges: e,
                bytes: 0,
            })
            .is_ok()
    };
    assert!(admits(objects, edges));
    assert!(!admits(objects + 1, 0));
    assert!(!admits(0, edges + 1));
}
