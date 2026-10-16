// Unit B2-b4a's controls (B2-b4 plan r2 sections 1.4 and 1.6). The soundness
// control walks every accepted walk vector, and every composed-workspace
// vector, natively on a fresh discovery ledger and asserts that the walker
// used no more objects and edges than tools/security/discovery_census.py's
// cost model predicts. The margin control classifies every censused T2 entry
// against the discovery profile's own limits, and every held-out row the
// census composes from the B2-b4c blind receipt by its per-mille margins
// (plan r6 section 2.5). Every tree is a scratch tree
// under the APFS test premise; nothing reads the real home, a real repository
// or the T2 cache. The helpers repeat the closed walk tests' own
// (`discovery_walk_tests.rs`), which this unit does not modify.
use super::discovery_rule::MarkerCountBasis;
use super::discovery_scan::{
    DiscoveryInvocation, ObservedEntry, UnitSourceRequest, UpwardProvenance, VcsRecord, WalkRow,
};
use super::discovery_walk::discover_downward;
use super::project_chain::DiscoveryRoot;
use crate::grants::{AuthorizedGroups, ProjectOwnerWaiver};
use crate::initial_installation::InitialInstallationAttempt;
use crate::trust::AclOmissionPremise;
use opensip_identity::{JsonValue as V, parse_json, raw_sha256};
use opensip_platform::{ChildObservation, RetainedDirectoryPath, WorkCost, WorkLedger};
use std::collections::BTreeSet;
use std::os::unix::fs::{MetadataExt, PermissionsExt};
use std::path::{Path, PathBuf};
use std::sync::atomic::AtomicBool;

const WALK_VECTORS: &[u8] = include_bytes!("discovery_walk_vectors.json");
const CENSUS_VECTORS: &[u8] = include_bytes!("discovery_census_vectors.json");
const CENSUS: &[u8] = include_bytes!("discovery_census.json");
/// Unit B3-b3c's companion record: the T2 workspaces' full ledgers.
const WORKSPACE_LEDGER: &[u8] = include_bytes!("discovery_workspace_ledger.json");
/// The reviewed T2 manifest the census is taken over (its SHA-256), and the
/// identities it gives the census record (r2, Codex B2B4C1-R1-RF-1): the
/// SHA-256 of the record's entry ids in manifest order, of its workspace ids,
/// and of its held-out entry ids, each list joined by newlines. Coverage is
/// checked against these, never against the record alone, so a duplicated,
/// foreign or substituted id, or a held-out status on another entry, fails.
/// A new manifest changes these under review.
const MANIFEST_SHA256: &str = "c8cc48e1549a05e9d563728fcac776ceca6c2ba63fa2004779385bd2fa4b7578";
const ENTRY_IDS_SHA256: &str = "cefb8f0394bb151eb3fb13e71c3ef767416c09597e09c75b1c24fafe9a6d8203";
const WORKSPACE_IDS_SHA256: &str =
    "f6ccde035daae0d8583c0b2802067b423baed6f2a5c92a9129eba22f165bc63c";
const HELD_OUT_IDS_SHA256: &str =
    "7a11ac53a4ed29d5abbb10a0f3d6aef4d677dfae51055d587112f2ebc1d76db6";
/// The transitive cost closure the census pins (plan r2 section 1.3), as
/// the code is compiled.
const CLOSURE: [(&str, &[u8]); 19] = [
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
    // B3-b3a1 (plan amendment A5): the D15 member producer, readers,
    // native observation and composition.
    (
        "crates/security/src/custody/git_tracking.rs",
        include_bytes!("git_tracking.rs"),
    ),
    (
        "crates/security/src/custody/workspace_declarations.rs",
        include_bytes!("workspace_declarations.rs"),
    ),
    (
        "crates/security/src/custody/workspace_observation.rs",
        include_bytes!("workspace_observation.rs"),
    ),
    (
        "crates/security/src/custody/workspace_discovery.rs",
        include_bytes!("workspace_discovery.rs"),
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
        gitlinks: &BTreeSet::new(),
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
fn soundness(id: &str, completed: bool, used: WorkCost, predicted: WorkCost) -> Result<(), String> {
    if !completed {
        return Err(format!("{id}: the native walk did not complete"));
    }
    if used.objects > predicted.objects
        || used.edges > predicted.edges
        || used.bytes > predicted.bytes
    {
        return Err(format!(
            "{id}: the walker used {used:?}; the model predicts {predicted:?}"
        ));
    }
    Ok(())
}
/// A prediction at the built root: bytes are affine in the root spelling's
/// length (plan r4 section 2.1), evaluated at the scratch root's own.
fn predicted_at(case: &V, root: &Path) -> WorkCost {
    WorkCost {
        objects: number(field(case, "objects")),
        edges: number(field(case, "edges")),
        bytes: number(field(case, "bytes"))
            + number(field(case, "bytesPerRootByte")) * root.to_str().unwrap().len(),
    }
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
        let predicted = predicted_at(predicted, &root);
        soundness(id, completed, used, predicted).unwrap();
        // The tightness, for review (plan r2 section 1.4).
        println!(
            "census-soundness {id} used {} {} {} predicted {} {} {}",
            used.objects,
            used.edges,
            used.bytes,
            predicted.objects,
            predicted.edges,
            predicted.bytes
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
        let predicted = predicted_at(case, &root);
        soundness(id, completed, used, predicted).unwrap();
        // The tightness, for review (plan r2 section 1.4).
        println!(
            "census-soundness {id} used {} {} {} predicted {} {} {}",
            used.objects,
            used.edges,
            used.bytes,
            predicted.objects,
            predicted.edges,
            predicted.bytes
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
    let predicted = predicted_at(predicted, &root);
    assert!(!completed);
    assert!(
        used.objects <= predicted.objects
            && used.edges <= predicted.edges
            && used.bytes <= predicted.bytes
    );
    assert!(soundness("aborted", completed, used, predicted).is_err());
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

/// Whether a charge fits the discovery profile's own limits: one fresh
/// ledger charged exactly that, never the record's copy.
fn admits(objects: usize, edges: usize, bytes: usize) -> bool {
    WorkLedger::discovery_profile()
        .charge::<()>(WorkCost {
            objects,
            edges,
            bytes,
        })
        .is_ok()
}

/// The compile-time sizes the byte model names (plan r4 section 2.1, RF-1):
/// the inventory is exactly these, and each equals the build's. The `libc`
/// types are asserted by the platform's own test
/// (`crates/platform/tests/discovery_census_sizes_tests.rs`).
#[test]
fn the_census_size_inventory_matches_the_build() {
    let here = [
        ("usize", std::mem::size_of::<usize>()),
        (
            "std::fs::Metadata",
            std::mem::size_of::<std::fs::Metadata>(),
        ),
        ("ObservedEntry", std::mem::size_of::<ObservedEntry>()),
        ("ChildObservation", std::mem::size_of::<ChildObservation>()),
        (
            "opensip_platform::CapturedAclEntry",
            std::mem::size_of::<opensip_platform::CapturedAclEntry>(),
        ),
        (
            "DescriptorAclCapture",
            std::mem::size_of::<opensip_platform::DescriptorAclCapture>(),
        ),
        (
            "DescriptorFilesystem",
            std::mem::size_of::<opensip_platform::DescriptorFilesystem>(),
        ),
        // B3-b3a1: the D15 records.
        (
            "DescriptorMetadata",
            std::mem::size_of::<opensip_platform::DescriptorMetadata>(),
        ),
        (
            "(Vec<u8>, DescriptorMetadata)",
            std::mem::size_of::<(Vec<u8>, opensip_platform::DescriptorMetadata)>(),
        ),
    ];
    let platform = ["libc::stat", "libc::attrlist", "libc::statfs"];
    for body in [CENSUS_VECTORS, CENSUS] {
        let body = parse_json(body).unwrap();
        let V::Object(sizes) = field(&body, "sizes") else {
            panic!("no size inventory")
        };
        let mut names: Vec<&str> = here.iter().map(|(n, _)| *n).chain(platform).collect();
        names.sort_unstable();
        let mut recorded: Vec<&str> = sizes.keys().map(String::as_str).collect();
        recorded.sort_unstable();
        assert_eq!(recorded, names);
        for (name, size) in here {
            assert_eq!(number(&sizes[name]), size, "{name}");
        }
    }
}

/// A held-out row as the census composes it from the blind receipt (unit
/// B2-b4c, plan r6 section 2.5): `Some(passes)` for a measured row, whose
/// margin is its per-mille margins at 2000 or more in every dimension, and
/// `None` for an error row. Each is in its closed format.
fn blind_result(id: &str, result: &V) -> Option<bool> {
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
                .all(|d| number(field(margins, d)) >= 2000);
            assert!(
                matches!(field(result, "passes2x"), V::Bool(b) if *b == passes),
                "{id}"
            );
            Some(passes)
        }
        "error" => {
            assert_eq!(keys, ["errorClass", "status"], "{id}");
            assert!(
                ["INTEGRITY", "POPULATION", "MODEL", "IO"]
                    .contains(&text(field(result, "errorClass"))),
                "{id}"
            );
            None
        }
        other => panic!("{id}: {other}"),
    }
}

#[test]
fn the_census_margin_is_classified_against_the_profile_limits_and_never_claimed_for_a_failing_entry()
 {
    let body = parse_json(CENSUS).unwrap();
    let mut failing = Vec::new();
    let mut lead_failing = Vec::new();
    let (mut outstanding, mut stale, mut measured, mut errors) = (0, 0, 0, 0);
    let mut held_ids = Vec::new();
    assert_eq!(
        text(field(field(&body, "manifest"), "sha256")),
        MANIFEST_SHA256
    );
    for (list, expected) in [
        ("entries", ENTRY_IDS_SHA256),
        ("workspaces", WORKSPACE_IDS_SHA256),
    ] {
        let ids: Vec<&str> = items(field(&body, list))
            .iter()
            .map(|row| text(field(row, "id")))
            .collect();
        assert_eq!(
            hex(&raw_sha256(ids.join("\n").as_bytes())),
            expected,
            "{list}"
        );
    }
    for list in ["entries", "workspaces"] {
        for row in items(field(&body, list)) {
            let id = text(field(row, "id")).to_owned();
            if let V::String(status) = field(row, "status") {
                // No workspace is held out: every workspace row is measured.
                if list == "entries" {
                    held_ids.push(id.clone());
                }
                match (list, status.as_str()) {
                    ("entries", "outstanding: held-out") => outstanding += 1,
                    ("entries", "outstanding: held-out (blind receipt stale)") => stale += 1,
                    ("entries", "blind-census") => match blind_result(&id, field(row, "result")) {
                        Some(passes) => {
                            measured += 1;
                            if !passes {
                                failing.push(id);
                            }
                        }
                        None => errors += 1,
                    },
                    _ => panic!("{id}: {status}"),
                }
                continue;
            }
            // The margin, in every dimension, with bytes at the largest
            // root spelling (M3-B r6 and r7 item 12; unit B2-b4b3).
            let bytes = field(row, "bytes");
            let widest = items(field(&body, "rootLengths"))
                .iter()
                .map(number)
                .max()
                .unwrap();
            let fits = admits(
                2 * number(field(row, "objects")),
                2 * number(field(row, "edges")),
                2 * (number(field(bytes, "base")) + number(field(bytes, "perRootByte")) * widest),
            );
            assert_eq!(flag(field(row, "passes2x")), fits, "{id}");
            if list == "workspaces" {
                assert!(
                    text(field(row, "fullLedgerMargin")).starts_with("outstanding"),
                    "{id}"
                );
            }
            // Bytes are reported, and classified, at each root length.
            for r in items(field(&body, "rootLengths")) {
                let r = number(r);
                let at = number(field(bytes, "base")) + number(field(bytes, "perRootByte")) * r;
                let key = r.to_string();
                assert_eq!(number(field(field(bytes, "at"), &key)), at, "{id}");
                assert_eq!(
                    flag(field(field(bytes, "fitsTwiceAt"), &key)),
                    admits(0, 0, 2 * at),
                    "{id} at {r}"
                );
            }
            // B3-b3a1 (plan r2 section 4.2): a repository entry's full
            // ledger is its walker cost plus its reader, member and descent
            // terms, classified the same way; a failure there fails the entry.
            let mut full_fits = true;
            if let V::Object(_) = field(row, "d15") {
                let d15 = field(row, "d15");
                let full = field(d15, "fullLedger");
                let total = |key: &str| {
                    ["reader", "member", "descent"]
                        .iter()
                        .map(|t| number(field(field(field(d15, "terms"), t), key)))
                        .sum::<usize>()
                };
                let objects = number(field(row, "objects")) + total("objects");
                let edges = number(field(row, "edges")) + total("edges");
                let base = number(field(bytes, "base")) + total("bytes");
                let per = number(field(bytes, "perRootByte")) + total("bytesPerRootByte");
                assert_eq!(number(field(full, "objects")), objects, "{id}");
                assert_eq!(number(field(full, "edges")), edges, "{id}");
                assert_eq!(number(field(field(full, "bytes"), "base")), base, "{id}");
                assert_eq!(
                    number(field(field(full, "bytes"), "perRootByte")),
                    per,
                    "{id}"
                );
                full_fits = admits(2 * objects, 2 * edges, 2 * (base + per * widest));
                assert_eq!(flag(field(full, "passes2x")), full_fits, "{id}");
            } else {
                assert!(
                    list == "workspaces",
                    "{id}: a repository entry without its D15 terms"
                );
            }
            if !fits || !full_fits {
                failing.push(id.clone());
                lead_failing.push(id);
            }
        }
    }
    // Coverage: exactly the manifest's ten held-out entries carry a held-out
    // status, and they are all outstanding (no receipt), all stale, or all
    // composed from one current receipt.
    assert_eq!(
        hex(&raw_sha256(held_ids.join("\n").as_bytes())),
        HELD_OUT_IDS_SHA256
    );
    let blind = measured + errors;
    assert_eq!(outstanding + stale + blind, 10);
    assert!(
        [outstanding, stale, blind]
            .iter()
            .filter(|n| **n == 10)
            .count()
            == 1,
        "{outstanding} {stale} {blind}"
    );
    let recorded: Vec<String> = items(field(&body, "failingEntries"))
        .iter()
        .map(|v| text(v).to_owned())
        .collect();
    assert_eq!(recorded, failing);
    // The full claim (M3-B r7 item 12; unit B2-b4b3): under the recorded
    // caps no lead-readable entry fails the margin. Workspace rows are
    // walker-only (above).
    assert!(lead_failing.is_empty(), "{lead_failing:?}");
    let caps = if failing.is_empty() {
        "recorded-margin-holds"
    } else {
        "returned-to-law"
    };
    assert_eq!(text(field(&body, "caps")), caps);
    // The held-out state (plan r6 section 2.5): any error leaves it
    // incomplete, any failing margin fails it, and only every held-out entry
    // measured and passing holds, which alone meets the gate.
    let state = if blind < 10 {
        "outstanding"
    } else if errors > 0 {
        "incomplete (blind census)"
    } else if failing.is_empty() {
        "holds (blind census)"
    } else {
        "fails (blind census)"
    };
    assert_eq!(text(field(&body, "heldOutMargin")), state);
    let gate = state == "holds (blind census)";
    assert_eq!(gate, measured == 10 && failing.is_empty());
    // The record's limits are the profile's: exactly the largest charge a
    // fresh discovery ledger admits.
    let limits = field(&body, "limits");
    let (objects, edges, bytes) = (
        number(field(limits, "objects")),
        number(field(limits, "edges")),
        number(field(limits, "bytes")),
    );
    assert!(admits(objects, edges, bytes));
    assert!(!admits(objects + 1, 0, 0));
    assert!(!admits(0, edges + 1, 0));
    assert!(!admits(0, 0, bytes + 1));
}

/// Unit B3-b3c (B3-b plan r2 section 4.3): each T2 workspace's full ledger,
/// the walker with its members entered plus the D15 reader, member and
/// descent terms, under both declaration branches (automatic, and every
/// member mount as a configured root), classified against the profile's
/// limits at the 2x margin. The record is the census's companion: the same
/// manifest, closure, sizes, limits and root lengths, and the same workspaces
/// with the same members.
#[test]
fn every_t2_workspace_full_ledger_is_classified_against_the_profile_limits() {
    let census = parse_json(CENSUS).unwrap();
    let body = parse_json(WORKSPACE_LEDGER).unwrap();
    for key in ["manifest", "closure", "sizes", "limits", "rootLengths"] {
        assert_eq!(field(&body, key), field(&census, key), "{key}");
    }
    let widest = items(field(&body, "rootLengths"))
        .iter()
        .map(number)
        .max()
        .unwrap();
    let rows = items(field(&body, "workspaces"));
    let walker_rows = items(field(&census, "workspaces"));
    assert_eq!(rows.len(), walker_rows.len());
    let mut failing = Vec::new();
    for (row, walker_row) in rows.iter().zip(walker_rows) {
        let id = text(field(row, "id"));
        // No workspace is held out: every row is measured.
        assert_eq!(id, text(field(walker_row, "id")));
        assert_eq!(field(row, "members"), field(walker_row, "members"), "{id}");
        let members: Vec<&str> = items(field(row, "members")).iter().map(text).collect();
        assert!(!members.is_empty(), "{id}");
        let mut passes = true;
        for (key, every_member) in [("automatic", false), ("configWorkspaceRoots", true)] {
            let branch = field(field(row, "branches"), key);
            let admitted: Vec<&str> = items(field(branch, "admitted")).iter().map(text).collect();
            assert!(admitted.iter().all(|m| members.contains(m)), "{id} {key}");
            if every_member {
                // Item 6b at the workspace's member count.
                assert_eq!(admitted, members, "{id} {key}");
            }
            let walker = field(branch, "walker");
            let terms = field(branch, "terms");
            let total = |k: &str| {
                number(field(walker, k))
                    + ["reader", "member", "descent"]
                        .iter()
                        .map(|t| number(field(field(terms, t), k)))
                        .sum::<usize>()
            };
            let (objects, edges) = (total("objects"), total("edges"));
            let (base, per) = (total("bytes"), total("bytesPerRootByte"));
            let full = field(branch, "fullLedger");
            assert_eq!(number(field(full, "objects")), objects, "{id} {key}");
            assert_eq!(number(field(full, "edges")), edges, "{id} {key}");
            assert_eq!(
                number(field(field(full, "bytes"), "base")),
                base,
                "{id} {key}"
            );
            assert_eq!(
                number(field(field(full, "bytes"), "perRootByte")),
                per,
                "{id} {key}"
            );
            let fits = admits(2 * objects, 2 * edges, 2 * (base + per * widest));
            assert_eq!(flag(field(full, "passes2x")), fits, "{id} {key}");
            passes &= fits;
        }
        assert_eq!(flag(field(row, "passes2x")), passes, "{id}");
        if !passes {
            failing.push(id.to_owned());
        }
    }
    let recorded: Vec<String> = items(field(&body, "failingWorkspaces"))
        .iter()
        .map(|v| text(v).to_owned())
        .collect();
    assert_eq!(recorded, failing);
    let caps = if failing.is_empty() {
        "recorded-margin-holds"
    } else {
        "returned-to-law"
    };
    assert_eq!(text(field(&body, "caps")), caps);
    // The full claim (M3-B r9 item 12): under the recorded caps every T2
    // workspace holds the 2x margin on its full ledger. A failure would return
    // the caps to the law, and this test refuses until the law revises them.
    assert!(failing.is_empty(), "{failing:?}");
    assert_eq!(text(field(&census, "caps")), "recorded-margin-holds");
}
