// Unit B2-b3b's controls (B2-b3 plan r2 section 3). Every tree is a scratch
// tree under the APFS test premise; nothing reads the real home or a real
// repository. The oracle cross-check builds each description of
// tools/security/discovery_walk_vectors.py natively, walks it, compares the
// population, its evidence and its custody inputs with the B2-b0 reference's,
// and runs the core over the native capture, with the scratch root spelled
// `/h/w`.
use super::*;
use crate::custody::discovery_rule::MarkerCountBasis;
use crate::custody::discovery_scan::{
    DiscoveryInvocation, ObservedAcl, UpwardProvenance, VcsRecord, WalkRow, boundary_inventory,
};
use crate::custody::project_admission::{GitdirStep, set_gitdir_hook};
use crate::grants::{AuthorizedGroups, ProjectOwnerWaiver};
use crate::initial_installation::InitialInstallationAttempt;
use opensip_identity::{JsonInteger, JsonValue as V, parse_json};
use opensip_platform::{CapturedAclPrincipal, RetainedDirectoryPath, WorkLedger};
use std::collections::BTreeMap;
use std::os::unix::fs::{MetadataExt, PermissionsExt};
use std::path::{Path, PathBuf};
use std::sync::atomic::AtomicBool;

const VECTORS: &[u8] = include_bytes!("discovery_walk_vectors.json");
/// An invoking user who owns nothing in a scratch tree (`foreign` cases).
const FOREIGN_UID: u32 = 4242;
/// A group that authorizes nothing in a scratch tree (`groups: other`).
const OTHER_GID: u32 = 4243;
const REFERENCE_ROOT: &str = "/h/w";

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
    let base = crate::test_scratch::temp_dir().join(format!("opensip-b2b3b-{nonce}"));
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
fn optional(value: &V) -> Option<String> {
    match value {
        V::Null => None,
        other => Some(text(other).to_owned()),
    }
}
fn flag(value: &V) -> bool {
    matches!(value, V::Bool(true))
}
fn string(s: &str) -> V {
    V::String(s.to_owned())
}
fn object(pairs: Vec<(&str, V)>) -> V {
    V::Object(pairs.into_iter().map(|(k, v)| (k.to_owned(), v)).collect())
}
fn integer(n: i128) -> V {
    V::Integer(JsonInteger::new(n).unwrap())
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
                // The system temp directory: the scratch parent's spelling is
                // too long. This thread holds the scratch lock, and the socket
                // leaves at once.
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

/// A native spelling under the scratch root as the reference's `/h/w`.
struct Spelling(String);
impl Spelling {
    fn map(&self, s: &str) -> String {
        s.replace(&self.0, REFERENCE_ROOT)
    }
}

/// A root-relative scope key spelled under the reference's `/h/w`.
fn reference_spelling(rel: &str) -> String {
    if rel.is_empty() {
        REFERENCE_ROOT.to_owned()
    } else {
        format!("{REFERENCE_ROOT}/{rel}")
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

/// The reference's file kind for a native status mode.
fn kind_name(mode: u32) -> &'static str {
    match mode & 0o170000 {
        0o040000 => "dir",
        0o100000 => "file",
        0o120000 => "symlink",
        0o010000 => "fifo",
        0o140000 => "socket",
        _ => "other",
    }
}
/// A captured ACL's write grants as the reference spells them: another
/// user is `uid:1001`, another group `group:70`; the invoking user, root
/// and authorized groups are trusted and not listed.
fn grants_of(acl: &ObservedAcl, owner: u32, trusted: &BTreeSet<u32>) -> Option<Vec<String>> {
    let ObservedAcl::Entries(entries) = acl else {
        return None;
    };
    let mut out = Vec::new();
    for e in entries {
        if e.flags & crate::private_access::ACE_KIND_MASK != crate::private_access::ACE_PERMIT
            || e.rights & !crate::custody::READ_ONLY_ACE_RIGHTS == 0
        {
            continue;
        }
        match e.principal {
            CapturedAclPrincipal::User(id) if id == 0 || id == owner => {}
            CapturedAclPrincipal::User(_) => out.push("uid:1001".to_owned()),
            CapturedAclPrincipal::Group(gid) if trusted.contains(&gid) => {}
            _ => out.push("group:70".to_owned()),
        }
    }
    Some(out)
}

fn units_json(p: &crate::custody::discovery_scan::DiscoveryProvenancePending, map: &Spelling) -> V {
    let strings = |v: &[String]| V::Array(v.iter().map(|s| string(&map.map(s))).collect());
    object(vec![
        ("selectedRoot", string(&map.map(&p.selected_root))),
        ("custodyWaiver", p.custody_waiver.map_or(V::Null, string)),
        ("nestedRepositories", strings(&p.nested_repositories)),
        ("nestedProjects", strings(&p.nested_projects)),
        ("unitSource", string(p.unit_source)),
        (
            "units",
            V::Array(
                p.units
                    .iter()
                    .map(|u| {
                        object(vec![
                            ("path", string(&map.map(&u.path))),
                            ("kind", string(u.kind)),
                            (
                                "markers",
                                V::Array(u.markers.iter().map(|m| string(m)).collect()),
                            ),
                        ])
                    })
                    .collect(),
            ),
        ),
        (
            "excludedUnits",
            V::Array(
                p.excluded_units
                    .iter()
                    .map(|u| {
                        object(vec![
                            ("path", string(&map.map(&u.path))),
                            ("reason", string(&u.reason)),
                        ])
                    })
                    .collect(),
            ),
        ),
        (
            "prunedTrees",
            V::Array(
                p.pruned_trees
                    .iter()
                    .map(|t| {
                        object(vec![
                            ("path", string(&map.map(&t.path))),
                            ("reason", string(t.reason.as_str())),
                            (
                                "markerCount",
                                t.marker_count.map_or(V::Null, |n| integer(n as i128)),
                            ),
                            ("markerCountBasis", string(t.basis.as_str())),
                        ])
                    })
                    .collect(),
            ),
        ),
        ("warnings", strings(&p.warnings)),
        ("memberRepositories", strings(&p.member_repositories)),
        ("memberConfigs", strings(&p.member_configs)),
    ])
}
fn expected_units_json(p: &V) -> V {
    let keys = [
        "selectedRoot",
        "custodyWaiver",
        "nestedRepositories",
        "nestedProjects",
        "unitSource",
        "units",
        "excludedUnits",
        "prunedTrees",
        "warnings",
        "memberRepositories",
        "memberConfigs",
    ];
    object(keys.iter().map(|k| (*k, field(p, k).clone())).collect())
}

/// One walk and core run over a built vector, on a fresh discovery ledger.
struct Run {
    scope: Result<ObservedScope, Failure>,
    result: Result<DiscoveryResultPending, Failure>,
    trace: Vec<(&'static str, String)>,
}
fn run_case(root: &Path, case: &V, ledger: Option<WorkCost>) -> Run {
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
    let source = source_of(case);
    let members = BTreeSet::new();
    let invocation = DiscoveryInvocation {
        invoking_uid: invoking,
        ci: false,
        groups: &groups,
        waiver: waiver.as_ref(),
        source: source.clone(),
        basis: MarkerCountBasis::NotEnumerated,
        member_roots: &members,
    };
    let new_ledger = || match ledger {
        Some(limits) => WorkLedger::with_limits(limits).unwrap(),
        None => WorkLedger::discovery_profile(),
    };
    take_trace();
    let request = WalkRequest {
        source: &source,
        invoking_uid: invoking,
        groups: &groups,
        waiver: waiver.as_ref(),
    };
    let scope = new_ledger().scope(|work| walk(&lent.root(), &request, work));
    take_trace();
    let upward = upward_of(field(case, "upward"));
    let result =
        new_ledger().scope(|work| discover_downward(&lent.root(), upward, &invocation, work));
    Run {
        scope,
        result,
        trace: take_trace(),
    }
}

// ---------------------------------------------------- the oracle cross-check

#[test]
fn every_walk_vector_matches_the_reference_population_evidence_and_records() {
    let body = parse_json(VECTORS).unwrap();
    let cases = items(field(&body, "cases"));
    assert!(cases.len() >= 40);
    for case in cases {
        let id = text(field(case, "id"));
        let (_s, root) = scratch();
        let links = root.parent().unwrap().join("links");
        materialize(&root, &links, items(field(case, "tree")));
        let map = Spelling(root.to_str().unwrap().to_owned());
        let run = run_case(&root, case, None);
        let scope = run.scope.unwrap_or_else(|e| panic!("{id}: {e:?}"));
        let foreign = flag(field(case, "foreign"));
        let trusted: BTreeSet<u32> = match field(case, "groups") {
            V::String(g) if g == "own" => [std::fs::metadata(&root).unwrap().gid()].into(),
            _ => BTreeSet::new(),
        };
        // The population: exactly the reference's paths, with their kinds.
        let V::Object(population) = field(case, "population") else {
            panic!("{id}")
        };
        // The scope is keyed by root-relative path (M3-B r6 item 12, unit
        // B2-b3d); the reference's population is spelled under `/h/w`.
        let native: BTreeMap<String, &ObservedEntry> = scope
            .entries
            .iter()
            .map(|(p, e)| (reference_spelling(p), e))
            .collect();
        assert_eq!(
            native.keys().collect::<Vec<_>>(),
            population.keys().collect::<Vec<_>>(),
            "{id}: population"
        );
        for (path, want) in population {
            let got = native[path];
            let kind = kind_name(got.metadata.mode);
            assert_eq!(kind, text(field(want, "kind")), "{id}: {path} kind");
            // Custody inputs (the r2 projection): kind, owner and mode for
            // every entry; links, size and the ACL only where captured.
            let owner = if foreign { 1001 } else { 1000 };
            assert_eq!(got.metadata.uid, uid(), "{id}: {path} owner");
            assert_eq!(
                i128::from(owner),
                match field(want, "uid") {
                    V::Integer(i) => i.get(),
                    _ => panic!(),
                }
            );
            if matches!(kind, "dir" | "file" | "fifo") {
                assert_eq!(
                    got.metadata.mode & 0o7777,
                    u32::from_str_radix(text(field(want, "mode")), 8).unwrap(),
                    "{id}: {path} mode"
                );
            }
            if got.acl != ObservedAcl::NotObserved {
                if kind == "file" {
                    assert_eq!(
                        i128::from(got.metadata.links as u32),
                        match field(want, "nlink") {
                            V::Integer(i) => i.get(),
                            _ => 1,
                        },
                        "{id}: {path} links"
                    );
                }
                let want_grants: Vec<String> = match field(want, "aclWrite") {
                    V::Array(g) => g.iter().map(|x| text(x).to_owned()).collect(),
                    _ => Vec::new(),
                };
                assert_eq!(
                    grants_of(&got.acl, uid(), &trusted),
                    Some(want_grants),
                    "{id}: {path} acl"
                );
            }
            // The evidence: VCS presence, kind and target on exactly the
            // probed directories.
            let want_vcs = match field(want, "vcs") {
                V::Null => None,
                v => Some((
                    text(field(v, "kind")).to_owned(),
                    optional(field(v, "target")),
                )),
            };
            let got_vcs = got.vcs.as_ref().map(|v| match v {
                ObservedVcs::Directory => ("directory".to_owned(), None),
                ObservedVcs::Indirection { target } => ("indirection".to_owned(), target.clone()),
            });
            assert_eq!(got_vcs, want_vcs, "{id}: {path} vcs");
            // A non-regular marker is never opened (r2, B2B3PLAN-2).
            if matches!(kind, "fifo" | "socket" | "symlink") {
                let native_path = path.replacen(REFERENCE_ROOT, &map.0, 1);
                assert!(
                    !run.trace
                        .iter()
                        .any(|(op, p)| *op == "open" && *p == native_path),
                    "{id}: {path} opened"
                );
            }
        }
        // The core over the native capture: the records, the refusal and
        // the boundary inventory.
        let result = run.result.unwrap_or_else(|e| panic!("{id}: {e:?}"));
        let expected = field(case, "expected");
        let (provenance, status) = match &result {
            DiscoveryResultPending::Accept(p) => (p, "ACCEPT"),
            DiscoveryResultPending::Refuse {
                refusal,
                path,
                detail,
                provenance,
            } => {
                assert_eq!(refusal.code(), text(field(expected, "refusal")), "{id}");
                assert_eq!(
                    path.as_ref().map(|p| map.map(p)),
                    optional(field(expected, "path")),
                    "{id}: path"
                );
                assert_eq!(map.map(detail), text(field(expected, "detail")), "{id}");
                // A join refused before custody (a crossing, a pruned tree,
                // the grammar) captures nothing (r3, Codex B2B3B-R2-RF-1).
                if detail.starts_with("JOIN_") {
                    assert!(
                        !run.trace.iter().any(|(op, _)| *op == "capture"),
                        "{id}: captured before a join refusal"
                    );
                }
                (provenance, "REFUSE")
            }
        };
        assert_eq!(status, text(field(expected, "status")), "{id}");
        assert_eq!(
            units_json(provenance, &map),
            expected_units_json(field(expected, "provenance")),
            "{id}: records"
        );
        match field(case, "inventory") {
            V::Null => assert!(boundary_inventory(&result).is_err(), "{id}"),
            want => {
                let got = boundary_inventory(&result).unwrap().to_json();
                let V::Object(mut got) = got else { panic!() };
                let selected = got.get("selectedRoot").map(|v| map.map(text(v))).unwrap();
                got.insert("selectedRoot".to_owned(), string(&selected));
                assert_eq!(&V::Object(got), want, "{id}: inventory");
            }
        }
    }
}

// ---------------------------------------------------------------- names

#[test]
fn listed_names_are_validated_as_logical_paths() {
    // An ordinary name, and the bounds of LD-B2B3-2 (r2) on the validator.
    assert!(listed_name("/w", "", b"package.json").is_ok());
    let at = |rel: &str, name: &[u8]| listed_name("/w", rel, name).is_ok();
    assert!(at("", "a".repeat(255).as_bytes()));
    assert!(!at("", "a".repeat(256).as_bytes()), "a 256-scalar segment");
    assert!(
        at("", "é".repeat(255).as_bytes()),
        "255 scalars in 510 bytes"
    );
    assert!(!at("", &[0x66, 0xff, 0x6f]), "not UTF-8");
    assert!(!at("", b"back\\slash"));
    assert!(!at("", b".opensip-stage-x"));
    assert!(!at("", b"has\0nul"));
    let long = vec!["a".repeat(255); 16].join("/");
    assert_eq!(long.chars().count(), 4095);
    assert!(at(&long[..long.len() - 1], b"b"), "a 4096-scalar path");
    assert!(!at(&long, b"b"), "a 4097-scalar path");
    // The refusal names the parent and the escaped bytes.
    let Err(WorkFailure::Operation(refusal)) = listed_name("/w/a", "a", &[0x66, 0xff, 0x3a]) else {
        panic!()
    };
    assert_eq!(
        refusal.discovery_refusal(),
        Some((
            DiscoveryRefusal::RootCustodyRefused,
            "NAME_UNREPRESENTABLE:/w/a:f%FF%3A".to_owned()
        ))
    );
}

fn automatic() -> V {
    object(vec![
        ("source", string("automatic")),
        ("roots", V::Array(Vec::new())),
        ("groups", V::Null),
        ("waive", V::Bool(false)),
        ("foreign", V::Bool(false)),
        (
            "upward",
            object(vec![
                ("mode", string("explicit")),
                ("configPath", V::Null),
                ("walked", V::Array(Vec::new())),
                ("stopReason", string("EXPLICIT")),
                ("vcs", V::Null),
                ("explicitPathWasSymlink", V::Bool(false)),
            ]),
        ),
    ])
}
fn refusal_detail(run: &Run) -> Option<String> {
    match &run.scope {
        Err(WorkFailure::Operation(refusal)) => refusal.discovery_refusal().map(|(_, d)| d),
        _ => None,
    }
}

#[test]
fn native_names_refuse_the_whole_walk_and_an_ordinary_listing_succeeds() {
    let (_s, root) = scratch();
    file(&root.join("package.json"), b"{}", 0o644);
    directory(&root.join("ok"), 0o755);
    let ok = run_case(&root, &automatic(), None);
    assert!(ok.scope.is_ok());
    assert!(ok.result.is_ok());
    for name in ["back\\slash", ".opensip-stage-x"] {
        let (_s, root) = scratch();
        directory(&root.join("a"), 0o755);
        file(&root.join("a").join(name), b"x", 0o644);
        let run = run_case(&root, &automatic(), None);
        let parent = root.join("a");
        assert_eq!(
            refusal_detail(&run),
            Some(format!(
                "NAME_UNREPRESENTABLE:{}:{}",
                parent.to_str().unwrap(),
                escaped(name.as_bytes())
            ))
        );
        assert!(run.result.is_err());
    }
    // A 255-scalar name is admitted natively.
    let (_s, root) = scratch();
    file(&root.join("a".repeat(255)), b"x", 0o644);
    assert!(run_case(&root, &automatic(), None).scope.is_ok());
}

/// Build `root/<segments...>/<leaf>` with relative steps, since the whole
/// spelling can exceed the platform's path bound.
fn build_long(root: &Path, segments: &[String], leaf: &str) {
    let mut script = String::from("set -e; cd \"$1\"");
    for s in segments {
        script.push_str(&format!("; mkdir {s}; cd {s}"));
    }
    script.push_str(&format!("; : > {leaf}"));
    let status = std::process::Command::new("/bin/sh")
        .args(["-c", &script, "sh"])
        .arg(root)
        .status()
        .unwrap();
    assert!(status.success());
}

#[test]
fn complete_paths_of_4096_scalars_are_walked_and_4097_refuse() {
    let mut segments = vec!["a".repeat(255); 15];
    segments.push("a".repeat(254));
    // 15 * 256 + 254 = 4094 scalars; one more segment of 1 is 4096, of 2 is 4097.
    let (_s, root) = scratch();
    build_long(&root, &segments, "b");
    assert!(run_case(&root, &automatic(), None).scope.is_ok());
    let (_s, root) = scratch();
    build_long(&root, &segments, "bb");
    let detail = refusal_detail(&run_case(&root, &automatic(), None)).unwrap();
    assert!(
        detail.starts_with("NAME_UNREPRESENTABLE:") && detail.ends_with(":bb"),
        "{detail}"
    );
}

// ---------------------------------------------------------------- traces

#[test]
fn the_ci_trace_touches_opensip_only_by_its_parents_observation() {
    let (_s, root) = scratch();
    file(&root.join("package.json"), b"{}", 0o644);
    directory(&root.join(".opensip"), 0o700);
    file(&root.join(".opensip").join("local.json"), b"{}", 0o600);
    directory(&root.join(".opensip").join("sub"), 0o700);
    let run = run_case(&root, &automatic(), None);
    run.scope.unwrap();
    let opensip = root.join(".opensip");
    let opensip = opensip.to_str().unwrap();
    let touching: Vec<_> = run
        .trace
        .iter()
        .filter(|(_, p)| p == opensip || p.starts_with(&format!("{opensip}/")))
        .collect();
    assert_eq!(touching, vec![&("observe", opensip.to_owned())]);
    // As a file, `.opensip` is an ordinary entry: never source, no row.
    let (_s, root) = scratch();
    file(&root.join(".opensip"), b"x", 0o644);
    let run = run_case(&root, &automatic(), None);
    let DiscoveryResultPending::Accept(p) = run.result.unwrap() else {
        panic!()
    };
    assert!(p.pruned_trees.is_empty() && p.units.is_empty());
}

#[test]
fn an_explicit_root_never_touches_a_large_sibling_and_needs_only_its_own_budget() {
    let (_s, root) = scratch();
    for dir in ["a", "a/u", "big"] {
        directory(&root.join(dir), 0o755);
    }
    file(&root.join("a/u/package.json"), b"{}", 0o644);
    for i in 0..300 {
        let d = root.join("big").join(format!("s{i}"));
        directory(&d, 0o755);
        file(&d.join("package.json"), b"{}", 0o644);
    }
    let mut explicit = automatic();
    let V::Object(fields) = &mut explicit else {
        panic!()
    };
    fields.insert("source".into(), string("explicit-joins"));
    fields.insert("roots".into(), V::Array(vec![string("a/u")]));
    let run = run_case(&root, &explicit, None);
    run.scope.unwrap();
    let big = root.join("big");
    let big = big.to_str().unwrap();
    assert!(
        !run.trace
            .iter()
            .any(|(_, p)| p.starts_with(&format!("{big}/"))),
        "the sibling's interior was touched"
    );
    // A ledger sized to the named root succeeds where automatic mode
    // exhausts.
    let mut ledger = WorkLedger::discovery_profile();
    let lent = Lent::new(&root);
    let groups = AuthorizedGroups::from_invocation(&[]).unwrap();
    let source = UnitSourceRequest::ExplicitJoins(vec!["a/u".into()]);
    ledger
        .scope(|work| {
            walk(
                &lent.root(),
                &WalkRequest {
                    source: &source,
                    invoking_uid: uid(),
                    groups: &groups,
                    waiver: None,
                },
                work,
            )
        })
        .unwrap();
    let used = ledger.used();
    let limits = WorkCost {
        objects: used.objects,
        edges: used.edges,
        bytes: used.bytes,
    };
    assert!(run_case(&root, &explicit, Some(limits)).scope.is_ok());
    assert!(matches!(
        run_case(&root, &automatic(), Some(limits)).scope,
        Err(WorkFailure::Budget(_))
    ));
}

// ---------------------------------------------------------------- swaps

#[test]
fn a_same_kind_swap_between_observation_and_open_refuses() {
    // A chain directory.
    let (_s, root) = scratch();
    directory(&root.join("a"), 0o755);
    directory(&root.join("a/u"), 0o755);
    file(&root.join("a/u/package.json"), b"{}", 0o644);
    let target = root.join("a");
    let moved = root.join("a-old");
    let swap = target.clone();
    let mut once = true;
    set_before_open(Some(Box::new(move |path: &str| {
        if once && Path::new(path) == swap {
            once = false;
            std::fs::rename(&swap, &moved).unwrap();
            std::fs::create_dir(&swap).unwrap();
        }
    })));
    let run = run_case(&root, &automatic(), None);
    set_before_open(None);
    assert!(
        matches!(run.scope, Err(WorkFailure::Operation(WalkRefusal::Changed(p))) if Path::new(&p) == target)
    );
    // A marker.
    let (_s, root) = scratch();
    directory(&root.join("u"), 0o755);
    file(&root.join("u/package.json"), b"{}", 0o644);
    let marker = root.join("u/package.json");
    let swap = marker.clone();
    let mut once = true;
    set_before_open(Some(Box::new(move |path: &str| {
        if once && Path::new(path) == swap {
            once = false;
            std::fs::remove_file(&swap).unwrap();
            std::fs::write(&swap, b"{}").unwrap();
        }
    })));
    let run = run_case(&root, &automatic(), None);
    set_before_open(None);
    assert!(
        matches!(run.scope, Err(WorkFailure::Operation(WalkRefusal::Changed(p))) if Path::new(&p) == marker)
    );
}

#[test]
fn a_gitdir_file_changed_after_its_opening_or_its_judgment_refuses() {
    // Codex B2B3A-R2-NBO-1: each full-metadata comparison in
    // `gitdir_target`, exercised by a race at its step.
    for step in [GitdirStep::Opened, GitdirStep::Judged] {
        let (_s, root) = scratch();
        directory(&root.join("r"), 0o755);
        let git = root.join("r/.git");
        file(&git, b"gitdir: /elsewhere\n", 0o644);
        let path = git.clone();
        set_gitdir_hook(Some(Box::new(move |at| {
            if at == step {
                use std::io::Write;
                let mut f = std::fs::OpenOptions::new()
                    .append(true)
                    .open(&path)
                    .unwrap();
                f.write_all(b"\n").unwrap();
            }
        })));
        let run = run_case(&root, &automatic(), None);
        set_gitdir_hook(None);
        assert!(
            matches!(
                run.scope,
                Err(WorkFailure::Operation(WalkRefusal::Evidence(
                    ProjectAdmissionRefusal::Changed
                )))
            ),
            "{step:?}: {:?}",
            run.scope
        );
    }
}

// ---------------------------------------------------------------- FW-01

#[test]
fn a_read_only_tree_gives_identical_records_and_a_canary_is_never_touched() {
    let build = |root: &Path| {
        for dir in ["a", "a/u", "n", "n/.git"] {
            directory(&root.join(dir), 0o755);
        }
        file(&root.join("package.json"), b"{}", 0o644);
        file(&root.join("a/u/package.json"), b"{}", 0o644);
        file(&root.join("a/canary"), b"canary", 0o644);
    };
    let (_s, writable) = scratch();
    build(&writable);
    let first = run_case(&writable, &automatic(), None);
    let (_s, readonly) = scratch();
    build(&readonly);
    let canary = readonly.join("a/canary");
    let before = std::fs::metadata(&canary).unwrap();
    let status = std::process::Command::new("/bin/chmod")
        .args(["-R", "a-w"])
        .arg(&readonly)
        .status()
        .unwrap();
    assert!(status.success());
    let second = run_case(&readonly, &automatic(), None);
    let after = std::fs::metadata(&canary).unwrap();
    assert_eq!(
        (before.mtime(), before.ctime(), before.len()),
        (after.mtime(), after.ctime(), after.len())
    );
    let canary = canary.to_str().unwrap();
    assert!(
        !second
            .trace
            .iter()
            .any(|(op, p)| *op == "open" && p == canary)
    );
    let records = |run: &Run, root: &Path| {
        let map = Spelling(root.to_str().unwrap().to_owned());
        match run.result.as_ref().unwrap() {
            DiscoveryResultPending::Accept(p) => units_json(p, &map),
            other => panic!("{other:?}"),
        }
    };
    assert_eq!(records(&first, &writable), records(&second, &readonly));
}

// ---------------------------------------------------------------- bounds

#[test]
fn exhaustion_refuses_as_budget_and_never_truncates() {
    let (_s, root) = scratch();
    for i in 0..20 {
        let d = root.join(format!("s{i}"));
        directory(&d, 0o755);
        file(&d.join("package.json"), b"{}", 0o644);
    }
    let mut ledger = WorkLedger::discovery_profile();
    let lent = Lent::new(&root);
    let groups = AuthorizedGroups::from_invocation(&[]).unwrap();
    let source = UnitSourceRequest::Automatic;
    let request = WalkRequest {
        source: &source,
        invoking_uid: uid(),
        groups: &groups,
        waiver: None,
    };
    ledger
        .scope(|work| walk(&lent.root(), &request, work))
        .unwrap();
    let used = ledger.used();
    for limits in [
        WorkCost {
            objects: used.objects - 1,
            ..used
        },
        WorkCost {
            edges: used.edges - 1,
            ..used
        },
        WorkCost {
            bytes: used.bytes - 1,
            ..used
        },
    ] {
        let mut short = WorkLedger::with_limits(limits).unwrap();
        assert!(matches!(
            short.scope(|work| walk(&lent.root(), &request, work)),
            Err(WorkFailure::Budget(_))
        ));
    }
}

#[test]
fn an_uncaptured_acl_the_core_reaches_is_an_instrument_fault() {
    // A unit chain directory handed over as NotObserved: the metadata-only
    // rejection passes, so the judgment needs the ACL (LD-B2B3-3).
    let (_s, root) = scratch();
    directory(&root.join("u"), 0o755);
    file(&root.join("u/package.json"), b"{}", 0o644);
    let lent = Lent::new(&root);
    let groups = AuthorizedGroups::from_invocation(&[]).unwrap();
    let source = UnitSourceRequest::Automatic;
    let mut ledger = WorkLedger::discovery_profile();
    let mut scope = ledger
        .scope(|work| {
            walk(
                &lent.root(),
                &WalkRequest {
                    source: &source,
                    invoking_uid: uid(),
                    groups: &groups,
                    waiver: None,
                },
                work,
            )
        })
        .unwrap();
    let unit = root.join("u");
    let unit = unit.to_str().unwrap();
    scope.entries.get_mut("u").unwrap().acl = ObservedAcl::NotObserved;
    let members = BTreeSet::new();
    let invocation = DiscoveryInvocation {
        invoking_uid: uid(),
        ci: false,
        groups: &groups,
        waiver: None,
        source,
        basis: MarkerCountBasis::NotEnumerated,
        member_roots: &members,
    };
    let upward = upward_of(field(&automatic(), "upward"));
    assert_eq!(
        discover_observed(&scope, root.to_str().unwrap(), upward.clone(), &invocation),
        Err(UnobservedAcl {
            path: unit.to_owned()
        })
    );
    // A metadata-only refusal needs no ACL: an other-writable directory.
    let mode = scope.entries.get("u").unwrap().metadata.mode;
    scope.entries.get_mut("u").unwrap().metadata.mode = mode | 0o002;
    let Ok(DiscoveryResultPending::Accept(p)) =
        discover_observed(&scope, root.to_str().unwrap(), upward, &invocation)
    else {
        panic!()
    };
    assert_eq!(
        p.excluded_units[0].reason,
        "DIRECTORY_CUSTODY:WRITABLE_BY_OTHERS"
    );
}

// ------------------------------------------------- r2: judgment-gated capture

fn captures(run: &Run) -> Vec<&str> {
    run.trace
        .iter()
        .filter(|(op, _)| *op == "capture")
        .map(|(_, p)| p.as_str())
        .collect()
}
fn opens(run: &Run) -> Vec<&str> {
    run.trace
        .iter()
        .filter(|(op, _)| *op == "open")
        .map(|(_, p)| p.as_str())
        .collect()
}
fn explicit(roots: &[&str], source: &str) -> V {
    let mut case = automatic();
    let V::Object(fields) = &mut case else {
        panic!()
    };
    fields.insert("source".into(), string(source));
    fields.insert(
        "roots".into(),
        V::Array(roots.iter().map(|r| string(r)).collect()),
    );
    case
}

#[test]
fn a_metadata_rejection_captures_nothing_past_it_and_opens_no_marker() {
    // Codex B2B3B-R1-RF-1: a 0777 unit directory is refused by its mode; it
    // is never captured and its marker is never opened.
    let (_s, root) = scratch();
    directory(&root.join("u"), 0o777);
    file(&root.join("u/package.json"), b"{}", 0o644);
    let run = run_case(&root, &automatic(), None);
    let u = root.join("u");
    assert!(captures(&run).is_empty(), "{:?}", captures(&run));
    assert!(
        !opens(&run)
            .iter()
            .any(|p| p.starts_with(u.to_str().unwrap()) && p.ends_with("package.json"))
    );
    let DiscoveryResultPending::Accept(p) = run.result.unwrap() else {
        panic!()
    };
    assert_eq!(
        p.excluded_units[0].reason,
        "DIRECTORY_CUSTODY:WRITABLE_BY_OTHERS"
    );
    // A foreign owner, unwaived, is refused the same way: nothing captured.
    let (_s, root) = scratch();
    directory(&root.join("u"), 0o755);
    file(&root.join("u/package.json"), b"{}", 0o644);
    let mut foreign = automatic();
    let V::Object(fields) = &mut foreign else {
        panic!()
    };
    fields.insert("foreign".into(), V::Bool(true));
    let run = run_case(&root, &foreign, None);
    assert!(captures(&run).is_empty());
    let DiscoveryResultPending::Accept(p) = run.result.unwrap() else {
        panic!()
    };
    assert_eq!(
        p.excluded_units[0].reason,
        "DIRECTORY_CUSTODY:FOREIGN_OWNER"
    );
    // A marker its own mode refuses is never opened, beside one that is.
    let (_s, root) = scratch();
    directory(&root.join("u"), 0o755);
    file(&root.join("u/package.json"), b"{}", 0o666);
    file(&root.join("u/Cargo.toml"), b"", 0o644);
    let run = run_case(&root, &automatic(), None);
    let bad = root.join("u/package.json");
    let good = root.join("u/Cargo.toml");
    assert!(!opens(&run).contains(&bad.to_str().unwrap()));
    assert!(opens(&run).contains(&good.to_str().unwrap()));
}

#[test]
fn an_ancestor_refused_by_its_acl_stops_the_chain_there() {
    // The ancestor's ACL must be captured to refuse it; nothing below it is.
    let (_s, root) = scratch();
    directory(&root.join("a"), 0o755);
    grant(&root.join("a"), "user", true);
    directory(&root.join("a/u"), 0o755);
    file(&root.join("a/u/package.json"), b"{}", 0o644);
    let run = run_case(&root, &automatic(), None);
    let a = root.join("a");
    assert_eq!(captures(&run), vec![a.to_str().unwrap()]);
    let DiscoveryResultPending::Accept(p) = run.result.unwrap() else {
        panic!()
    };
    assert_eq!(
        p.excluded_units[0].reason,
        "DIRECTORY_CUSTODY:WRITABLE_BY_ACL"
    );
}

#[test]
fn a_crossing_join_captures_nothing_and_later_joins_are_not_judged() {
    // A join through a nested repository refuses before any custody; the
    // core stops there, so the next join is walked but never captured.
    let (_s, root) = scratch();
    for dir in ["r", "r/.git", "r/x", "b"] {
        directory(&root.join(dir), 0o755);
    }
    file(&root.join("r/x/package.json"), b"{}", 0o644);
    file(&root.join("b/package.json"), b"{}", 0o644);
    let run = run_case(&root, &explicit(&["r/x", "b"], "explicit-joins"), None);
    assert!(captures(&run).is_empty(), "{:?}", captures(&run));
    let b = root.join("b");
    assert!(
        run.trace
            .contains(&("list", b.to_str().unwrap().to_owned()))
    );
    let DiscoveryResultPending::Refuse { detail, .. } = run.result.unwrap() else {
        panic!()
    };
    assert_eq!(detail, "JOIN_CROSSES_NESTED_REPOSITORY");
}

// ------------------------------------------------- r2: paths seen twice

#[test]
fn a_shared_prefix_replaced_between_named_roots_refuses() {
    // Codex B2B3B-R1-RF-2: roots a/u and a/v share `a`. Between the two
    // chains, `a` is replaced by a new directory holding the old children
    // (their identities kept); the second chain refuses, in both modes.
    for source in ["explicit-joins", "config-workspace-roots"] {
        let (_s, root) = scratch();
        for dir in ["a", "a/u", "a/v"] {
            directory(&root.join(dir), 0o755);
        }
        file(&root.join("a/u/package.json"), b"{}", 0o644);
        file(&root.join("a/v/package.json"), b"{}", 0o644);
        let a = root.join("a");
        let (swap, old) = (a.clone(), root.join("a-old"));
        // After the first chain is judged (its marker's open), before the
        // second chain observes `a` again.
        let trigger = root.join("a/u/package.json");
        let mut once = true;
        set_before_open(Some(Box::new(move |path: &str| {
            if once && Path::new(path) == trigger {
                once = false;
                std::fs::rename(&swap, &old).unwrap();
                std::fs::create_dir(&swap).unwrap();
                for child in ["u", "v"] {
                    std::fs::rename(old.join(child), swap.join(child)).unwrap();
                }
            }
        })));
        let run = run_case(&root, &explicit(&["a/u", "a/v"], source), None);
        set_before_open(None);
        assert!(
            matches!(&run.scope, Err(WorkFailure::Operation(WalkRefusal::Changed(p))) if Path::new(p) == a),
            "{source}: {:?}",
            run.scope
        );
    }
}

// ------------------------------------------------- r2: owned storage

fn walk_used(root: &Path, case: &V) -> WorkCost {
    let lent = Lent::new(root);
    let groups = AuthorizedGroups::from_invocation(&[]).unwrap();
    let source = source_of(case);
    let mut ledger = WorkLedger::discovery_profile();
    ledger
        .scope(|work| {
            walk(
                &lent.root(),
                &WalkRequest {
                    source: &source,
                    invoking_uid: uid(),
                    groups: &groups,
                    waiver: None,
                },
                work,
            )
        })
        .unwrap();
    ledger.used()
}

#[test]
fn owned_paths_are_charged_with_their_length_under_deep_prefixes() {
    // Codex B2B3B-R1-RF-3: each child's owned copies that carry its parent's
    // spelling are charged with their length. The marginal cost of 64 more
    // children, under an 8-level prefix of 100-byte names and under a short
    // one, differs by exactly three prefixes per child: its root-relative
    // path in the listing with the validator's copy of it (r3), and its
    // scope key. Unit B2-b3d (M3-B r6 item 12) keeps no absolute spelling of
    // a child, so the r3 count of four is now three.
    // Every per-directory cost cancels.
    let tree = |deep: bool, width: usize| {
        let (s, root) = scratch();
        let mut dir = root.clone();
        if deep {
            for i in 0..8 {
                dir = dir.join(format!("{i:0>100}"));
                directory(&dir, 0o755);
            }
        } else {
            for i in 0..8 {
                dir = dir.join(format!("{i}"));
                directory(&dir, 0o755);
            }
        }
        for i in 0..width {
            file(&dir.join(format!("f{i:0>3}")), b"", 0o644);
        }
        let used = walk_used(&root, &automatic());
        drop(s);
        used
    };
    let marginal = |deep: bool| tree(deep, 128).bytes - tree(deep, 64).bytes;
    // Eight levels, each name 99 bytes longer (`{i:0>100}` against `{i}`).
    let extra = 8 * 99;
    assert_eq!(marginal(true) - marginal(false), 64 * 3 * extra);
    // Explicit specs: 200 specs of 208 bytes against 200 of 8. Each spec's
    // copy, its normalized path and its chain key are charged with its
    // length: three copies per spec (unit B2-b3d drops the spelling under
    // the root), and the platform's by-name observation charges the name's
    // bytes once more.
    let (_s, root) = scratch();
    let long: Vec<String> = (0..200).map(|i| format!("missing-{i:0>200}")).collect();
    let short: Vec<String> = (0..200).map(|i| format!("m-{i:0>6}")).collect();
    let long: Vec<&str> = long.iter().map(String::as_str).collect();
    let short: Vec<&str> = short.iter().map(String::as_str).collect();
    let large = walk_used(&root, &explicit(&long, "explicit-joins"));
    let small = walk_used(&root, &explicit(&short, "explicit-joins"));
    // The first join is also classified whole before custody (r3); its
    // missing component ends the core's judgment, so no later join is.
    assert_eq!(large.bytes - small.bytes, 200 * 4 * (208 - 8) + (208 - 8));
}

#[test]
fn the_evidence_probe_is_traced_and_a_gitdir_target_is_never_followed() {
    // Codex B2B3B-R1-NBO-2: the probe's by-name observations, the `.git`
    // open, its capture and its read are in the trace; the target is not.
    let (_s, root) = scratch();
    directory(&root.join("r"), 0o755);
    file(&root.join("r/.git"), b"gitdir: /elsewhere/x\n", 0o644);
    let run = run_case(&root, &automatic(), None);
    let git = root.join("r/.git");
    let git = git.to_str().unwrap();
    for op in ["observe", "open", "capture", "read"] {
        assert!(run.trace.contains(&(op, git.to_owned())), "{op}");
    }
    assert!(!run.trace.iter().any(|(_, p)| p.starts_with("/elsewhere")));
}

#[test]
fn directory_and_pruned_children_charge_every_copy_of_their_paths() {
    // Codex B2B3B-R2-RF-2: the same marginal comparison for directory
    // children, ordinary and pruned. An ordinary (empty) directory child
    // carries six prefix copies: two in its parent's listing, its scope key,
    // its classification, its `opensip.json` key, and its listed-set entry.
    // A pruned child carries four: the listing's two, its scope key and its
    // classification, and nothing else. Unit B2-b3d (M3-B r6 item 12) keeps
    // no absolute spelling and moves the frame's path, so the r3 counts of
    // ten and five are now six and four.
    let tree = |deep: bool, width: usize, pruned: bool| {
        let (s, root) = scratch();
        let mut dir = root.clone();
        for i in 0..8 {
            dir = dir.join(if deep {
                format!("{i:0>100}")
            } else {
                format!("{i}")
            });
            directory(&dir, 0o755);
        }
        for i in 0..width {
            let child = dir.join(format!("c{i:0>3}"));
            directory(&child, 0o755);
            if pruned {
                directory(&child.join("node_modules"), 0o755);
            }
        }
        let used = walk_used(&root, &automatic());
        drop(s);
        used.bytes
    };
    let extra = 8 * 99;
    let ordinary = |deep: bool| tree(deep, 128, false) - tree(deep, 64, false);
    assert_eq!(ordinary(true) - ordinary(false), 64 * 6 * extra);
    let pruned = |deep: bool| tree(deep, 64, true) - tree(deep, 64, false);
    assert_eq!(pruned(true) - pruned(false), 64 * 4 * extra);
}

#[test]
fn a_named_root_beyond_the_listing_depth_is_never_listed() {
    // Codex B2B3B-R2-RF-3: a 257-segment named root shows only its marker
    // names; it is never listed, so an arbitrary child is never observed.
    let (_s, root) = scratch();
    let rel = vec!["d"; 257].join("/");
    let named = root.join(&rel);
    std::fs::create_dir_all(&named).unwrap();
    file(&named.join("package.json"), b"{}", 0o644);
    file(&named.join("unlisted.txt"), b"", 0o644);
    for source in ["explicit-joins", "config-workspace-roots"] {
        let run = run_case(&root, &explicit(&[rel.as_str()], source), None);
        let scope = run.scope.unwrap();
        let named_abs = named.to_str().unwrap();
        assert!(
            !run.trace.contains(&("list", named_abs.to_owned())),
            "{source}"
        );
        assert!(scope.entries.contains_key(&format!("{rel}/package.json")));
        assert!(!scope.entries.contains_key(&format!("{rel}/unlisted.txt")));
    }
}

// ------------------------------------- B2-b3d: one-pass listing conversion

/// Feed `names` through a `ListingConversion` on a fresh discovery ledger,
/// then finish it with `outcome`.
fn converted(
    names: &[&[u8]],
    outcome: Result<opensip_platform::DirectoryVisitSummary, DirectoryVisitError<Failure>>,
) -> Result<Vec<String>, Failure> {
    let mut ledger = WorkLedger::discovery_profile();
    ledger.scope(|work| {
        let mut conversion = ListingConversion::new();
        for name in names {
            conversion.accept("a", name, work)?;
        }
        conversion.finish(outcome, || "/w/a".to_owned())
    })
}
fn completed() -> Result<opensip_platform::DirectoryVisitSummary, DirectoryVisitError<Failure>> {
    let (_s, root) = scratch();
    let path = RetainedDirectoryPath::open_project_root(&root, 256).unwrap();
    path.directory()
        .visit_entry_names(8, 1024, |_| Ok::<(), Failure>(()))
}

#[test]
fn a_listing_failure_wins_over_an_earlier_unrepresentable_name() {
    // M3-B r6 item 12, unit B2-b3d (plan r2, Codex B2B3DPLAN-R1-RF-2): the
    // first invalid name is kept, the listing runs on, and its own failure
    // refuses first, as before the one-pass conversion.
    let bad: &[u8] = &[0x66, 0xff];
    let limit = converted(&[b".", bad, b"z"], Err(DirectoryVisitError::EntryLimit));
    assert!(matches!(
        limit,
        Err(WorkFailure::Operation(WalkRefusal::ListingBound))
    ));
    let bytes = converted(&[bad], Err(DirectoryVisitError::NameByteLimit));
    assert!(matches!(
        bytes,
        Err(WorkFailure::Operation(WalkRefusal::ListingBound))
    ));
    let native = converted(
        &[bad, b"z"],
        Err(DirectoryVisitError::Native(io::Error::other(
            "read or close",
        ))),
    );
    assert!(matches!(
        native,
        Err(WorkFailure::Operation(WalkRefusal::HostIo(_)))
    ));
}

#[test]
fn a_complete_listing_with_an_unrepresentable_name_refuses_as_before() {
    let refused = converted(&[b"ok", &[0x66, 0xff, 0x3a], b"later"], completed());
    let Err(WorkFailure::Operation(refusal)) = refused else {
        panic!("{refused:?}")
    };
    assert_eq!(
        refusal.discovery_refusal(),
        Some((
            DiscoveryRefusal::RootCustodyRefused,
            "NAME_UNREPRESENTABLE:/w/a:f%FF%3A".to_owned()
        ))
    );
    // A clean listing gives each child's one root-relative path, sorted,
    // without `.` and `..`.
    let paths = converted(&[b"z", b".", b"b", b".."], completed()).unwrap();
    assert_eq!(paths, ["a/b", "a/z"]);
}

#[test]
fn nothing_after_the_first_unrepresentable_name_is_converted() {
    // The conversion stops at the first invalid name: a later name costs its
    // visit only, never a copy.
    let used = |names: &[&[u8]]| {
        let mut ledger = WorkLedger::discovery_profile();
        ledger
            .scope(|work| {
                let mut conversion = ListingConversion::new();
                for name in names {
                    conversion.accept("a", name, work)?;
                }
                Ok::<_, Failure>(())
            })
            .unwrap();
        ledger.used()
    };
    let bad: &[u8] = &[0xff];
    let one = used(&[bad]);
    let more = used(&[bad, b"later-name"]);
    assert_eq!(more.objects, one.objects);
    assert_eq!(more.bytes, one.bytes);
    assert_eq!(more.edges, one.edges + 1);
}

/// One automatic walk of `root` under a byte limit, with its trace.
fn walk_under(root: &Path, bytes: usize) -> (bool, Vec<(&'static str, String)>) {
    let lent = Lent::new(root);
    let groups = AuthorizedGroups::from_invocation(&[]).unwrap();
    let source = UnitSourceRequest::Automatic;
    let mut ledger = WorkLedger::with_limits(WorkCost {
        objects: 65_536,
        edges: 131_072,
        bytes,
    })
    .unwrap();
    take_trace();
    let completed = ledger
        .scope(|work| {
            walk(
                &lent.root(),
                &WalkRequest {
                    source: &source,
                    invoking_uid: uid(),
                    groups: &groups,
                    waiver: None,
                },
                work,
            )
        })
        .is_ok();
    (completed, take_trace())
}

#[test]
fn the_observation_array_is_charged_before_it_is_reserved() {
    // r2 (Codex B2B3D-R1-RF-1): the parallel observation array is charged
    // whole, after the listing and before any child is observed or its slots
    // reserved. Under the largest byte limit that still refuses, the walk has
    // listed the root and observed no child: the refusing charge is that
    // allowance.
    let (_s, root) = scratch();
    for i in 0..512 {
        file(&root.join(format!("f{i:0>3}")), b"", 0o644);
    }
    let spelled = root.to_str().unwrap().to_owned();
    let child = format!("{spelled}/");
    let observes_a_child = |trace: &[(&'static str, String)]| {
        trace
            .iter()
            .any(|(op, p)| *op == "observe" && p.starts_with(&child))
    };
    // The smallest byte limit at which a child is observed.
    let (mut low, mut high) = (1, 1 << 24);
    assert!(observes_a_child(&walk_under(&root, high).1));
    while low < high {
        let mid = low + (high - low) / 2;
        if observes_a_child(&walk_under(&root, mid).1) {
            high = mid;
        } else {
            low = mid + 1;
        }
    }
    let (completed, trace) = walk_under(&root, low - 1);
    assert!(!completed);
    assert!(trace.contains(&("list", spelled.clone())));
    assert!(!observes_a_child(&trace));
    // That allowance is the whole array: at least one slot per child.
    let (_, at) = walk_under(&root, low);
    assert!(observes_a_child(&at));
    assert!(low > 512 * std::mem::size_of::<ChildObservation>());
}
