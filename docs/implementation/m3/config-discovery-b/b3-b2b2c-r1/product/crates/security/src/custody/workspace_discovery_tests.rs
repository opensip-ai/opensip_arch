// Unit B3-b2b2b's controls (M3-B r9 items 19 to 24; B3-b plan r2 amendment
// A3). Each vector of tools/security/workspace_discovery_vectors.py is built
// as a scratch tree under a scratch H, its members made real Git
// repositories by `git init` (and one configuration key where the case
// states item 6b's refusal); item 6a observes W's retained chain, the
// handoff's proof is built from it, and `discover_with_members` composes the
// readers, item 6b and the walk. The complete record and the link rows must
// equal B3-b0's, with W spelled `/h/w`.
use super::*;
use crate::custody::discovery_rule::MarkerCountBasis;
use crate::custody::discovery_scan::{VcsRecord, WalkRow};
use crate::custody::git_tracking::{
    MemberCustody, MemberInputs, NoRepository, TrackingInputs, observe_tracking,
};
use crate::custody::installation_read_fixture::churned;
use crate::custody::project_chain::{ProjectChainPolicy, walk_project_chain};
use crate::grants::AuthorizedGroups;
use crate::initial_installation::InitialInstallationAttempt;
use crate::trust::AclOmissionPremise;
use opensip_identity::{JsonValue as V, parse_json};
use opensip_platform::{DescriptorFilesystem, WorkLedger};
use std::ffi::OsString;
use std::os::unix::fs::{MetadataExt, PermissionsExt};
use std::path::{Path, PathBuf};
use std::process::Command;
use std::sync::atomic::AtomicBool;

const VECTORS: &[u8] = include_bytes!("workspace_discovery_vectors.json");
const REFERENCE_ROOT: &str = "/h/w";

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
fn optional_text(value: &V) -> Option<String> {
    match value {
        V::Null => None,
        other => Some(text(other).to_owned()),
    }
}

struct Scratch(PathBuf);
impl Drop for Scratch {
    fn drop(&mut self) {
        let _ = Command::new("/bin/chmod")
            .args(["-R", "u+rwX"])
            .arg(&self.0)
            .stderr(std::process::Stdio::null())
            .status();
        let _ = std::fs::remove_dir_all(&self.0);
    }
}
/// A scratch root holding a 0700 `home` (H) and a separate `githome`, the
/// HOME git runs with.
fn scratch() -> (Scratch, PathBuf, PathBuf) {
    let nonce: String = opensip_platform::request_entropy()
        .unwrap()
        .iter()
        .map(|b| format!("{b:02x}"))
        .collect();
    let root = crate::test_scratch::temp_dir().join(format!("opensip-b3b2b2b-{nonce}"));
    std::fs::create_dir(&root).unwrap();
    std::fs::set_permissions(&root, std::fs::Permissions::from_mode(0o700)).unwrap();
    let root = std::fs::canonicalize(&root).unwrap();
    let home = root.join("home");
    std::fs::create_dir(&home).unwrap();
    std::fs::set_permissions(&home, std::fs::Permissions::from_mode(0o700)).unwrap();
    let githome = root.join("githome");
    std::fs::create_dir(&githome).unwrap();
    (Scratch(root), home, githome)
}
fn git(githome: &Path, directory: &Path, args: &[&str]) {
    let output = Command::new("/usr/bin/git")
        .args([
            "-c",
            "init.defaultBranch=main",
            "-c",
            "core.hooksPath=/dev/null",
        ])
        .args(args)
        .current_dir(directory)
        .env_clear()
        .env("PATH", "/usr/bin:/bin")
        .env("HOME", githome)
        .env("GIT_CONFIG_NOSYSTEM", "1")
        .output()
        .unwrap();
    assert!(
        output.status.success(),
        "git {args:?}: {}",
        String::from_utf8_lossy(&output.stderr)
    );
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
fn any_volume(_: &DescriptorFilesystem) -> bool {
    true
}

/// Directories and files of a walk-vector description, under `root`.
fn materialize(root: &Path, tree: &[V]) {
    for entry in tree {
        let path = root.join(text(field(entry, "path")));
        let mode = u32::from_str_radix(text(field(entry, "mode")), 8).unwrap();
        match text(field(entry, "kind")) {
            "dir" => std::fs::create_dir(&path).unwrap(),
            "file" => {
                // `padTo`: spaces after the text, to that many bytes.
                let mut bytes = text(field(entry, "text")).as_bytes().to_vec();
                if let V::Integer(n) = field(entry, "padTo") {
                    bytes.resize(usize::try_from(n.get()).unwrap().max(bytes.len()), b' ');
                }
                std::fs::write(&path, bytes).unwrap();
            }
            other => panic!("{other}"),
        }
        std::fs::set_permissions(&path, std::fs::Permissions::from_mode(mode)).unwrap();
        // An ACL write grant, as the walk vectors' `acl` states it.
        if let V::String(who) = field(entry, "acl") {
            let principal = if who == "user" {
                "user:nobody"
            } else {
                "group:everyone"
            };
            let right = if text(field(entry, "kind")) == "dir" {
                "add_file"
            } else {
                "write"
            };
            let status = Command::new("/bin/chmod")
                .arg("+a")
                .arg(format!("{principal} allow {right}"))
                .arg(&path)
                .status()
                .unwrap();
            assert!(status.success());
        }
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
        config_path: optional_text(field(upward, "configPath")),
        walked: items(field(upward, "walked"))
            .iter()
            .map(|w| WalkRow {
                path: text(field(w, "path")).to_owned(),
                custody: text(field(w, "custody")).to_owned(),
                candidate: text(field(w, "candidate")).to_owned(),
                boundary: optional_text(field(w, "boundary")),
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
                target: optional_text(field(v, "target")),
            }),
        },
        explicit_path_was_symlink: match field(upward, "explicitPathWasSymlink") {
            V::Bool(b) => Some(*b),
            _ => None,
        },
    }
}
/// Every string with the native root's spelling as the reference's `/h/w`.
fn respell(value: V, native: &str) -> V {
    match value {
        V::String(s) => V::String(s.replace(native, REFERENCE_ROOT)),
        V::Array(items) => V::Array(items.into_iter().map(|v| respell(v, native)).collect()),
        V::Object(fields) => V::Object(
            fields
                .into_iter()
                .map(|(k, v)| (k, respell(v, native)))
                .collect(),
        ),
        other => other,
    }
}
fn link_json(l: &LinkRow) -> V {
    let mut pairs = vec![
        ("ecosystem", string(l.ecosystem)),
        ("packageName", string(&l.package_name)),
        ("providerMember", string(&l.provider_member)),
        ("packageDir", string(&l.package_dir)),
        ("providedVersion", string(&l.provided_version)),
        ("declaredBy", string(l.declared_by)),
    ];
    if let Some(source) = &l.cargo_patch_source {
        pairs.push(("cargoPatchSource", string(source)));
    }
    object(pairs)
}

/// Item 6a's chain walk or observation failed on a scratch tree.
fn invariant<E>(_: E) -> Failure {
    WorkFailure::Operation(WorkspaceRefusal::Invariant("item-6a"))
}

/// One vector: built, observed by item 6a, composed.
fn run(case: &V) -> (Result<WorkspaceDiscovery, Failure>, String) {
    run_with(case, |_, _| None)
}

/// A race control's hook, built over W and the git HOME once the tree is.
type Hook = super::super::workspace_observation::RaceHook;

/// `run`, with the test-only hook a race control sets once the tree is
/// built (r2, Codex B3B2B2B-R1-RF-2 to RF-4).
fn run_with(
    case: &V,
    hook: impl FnOnce(&Path, &Path) -> Option<Hook>,
) -> (Result<WorkspaceDiscovery, Failure>, String) {
    let (_s, home, githome) = scratch();
    let w = home.join("w");
    std::fs::create_dir(&w).unwrap();
    std::fs::set_permissions(&w, std::fs::Permissions::from_mode(0o755)).unwrap();
    materialize(&w, items(field(case, "tree")));
    if matches!(field(case, "wRepository"), V::Bool(true)) {
        git(&githome, &w, &["init", "-q"]);
    }
    for member in items(field(case, "gitMembers")) {
        git(&githome, &w.join(text(member)), &["init", "-q"]);
    }
    // r2 (Codex B3B2B2B-R1-RF-1): an index gitlink at a populated directory
    // with no VCS marker, written into the member's index.
    for gitlink in items(field(case, "gitlinks")) {
        git(
            &githome,
            &w.join(text(field(gitlink, "member"))),
            &[
                "update-index",
                "--add",
                "--cacheinfo",
                &format!("160000,{},{}", "1".repeat(40), text(field(gitlink, "path"))),
            ],
        );
    }
    if let V::Object(_) = field(case, "gitConfig") {
        let config = field(case, "gitConfig");
        git(
            &githome,
            &w.join(text(field(config, "member"))),
            &[
                "config",
                text(field(config, "key")),
                text(field(config, "value")),
            ],
        );
    }
    let result = discover_at(
        &home,
        &w,
        &upward_of(field(case, "upward")),
        source_of(case),
        hook(&w, &githome),
    );
    (result, w.to_str().unwrap().to_owned())
}

/// Item 6a over W's retained chain, the handoff's proof from it, and
/// `discover_with_members` with `source` and the selection's `upward`
/// provenance, `hook` set for the run (unit B3-b2b2c: shared with the T2
/// link-map controls).
fn discover_at(
    home: &Path,
    w: &Path,
    upward: &UpwardProvenance,
    source: UnitSourceRequest,
    hook: Option<Hook>,
) -> Result<WorkspaceDiscovery, Failure> {
    super::super::workspace_observation::set_hook(hook);
    let premise = premise();
    let groups = BTreeSet::new();
    let authorized = AuthorizedGroups::from_invocation(&[]).unwrap();
    let volume = any_volume;
    let policy = ProjectChainPolicy::new(Some(&premise), &volume, &groups);
    let clean: Vec<(OsString, OsString)> = vec![(
        std::ffi::OsStr::new("HOME").to_os_string(),
        home.to_path_buf().into_os_string(),
    )];
    let none = BTreeSet::new();
    let invocation = DiscoveryInvocation {
        invoking_uid: uid(),
        ci: false,
        groups: &authorized,
        waiver: None,
        source,
        basis: MarkerCountBasis::NotEnumerated,
        member_roots: &none,
        gitlinks: &BTreeSet::new(),
    };
    let member_inputs = MemberInputs {
        uid: uid(),
        home,
        home_filesystem: &volume,
        environment: &clean,
        system_sources: &[],
        custody: MemberCustody {
            trust_groups: &groups,
            premise: Some(&premise),
        },
    };
    let result = WorkLedger::discovery_profile().scope(|work| {
        let chain = walk_project_chain(home, w, uid(), &policy, work).map_err(invariant)?;
        let inputs = TrackingInputs {
            chain: &chain,
            uid: uid(),
            policy: &policy,
            home,
            environment: &clean,
            system_sources: &[],
        };
        let observed = observe_tracking(&inputs, work).map_err(invariant)?;
        let members = NoRepository::retained(&chain, &observed).map(|proof| MemberObservation {
            inputs: &member_inputs,
            proof,
        });
        let root = DiscoveryRoot::for_tests(chain.root(), chain.spelling(), Some(&premise));
        discover_with_members(&root, upward, &invocation, members.as_ref(), work)
    });
    super::super::workspace_observation::set_hook(None);
    result
}

fn paths(value: &V) -> BTreeSet<String> {
    items(value).iter().map(|p| text(p).to_owned()).collect()
}
fn under(path: &str, base: &str) -> bool {
    base.is_empty() || path == base || path.strip_prefix(base).is_some_and(|r| r.starts_with('/'))
}
/// The access control: the decision core requests only what B3-b0 looked up,
/// read or listed; the native observation touches only a requested path, an
/// ancestor of one, or a VCS marker of a directory whose markers were asked.
fn check_access(id: &str, case: &V, trace: &[(&'static str, String)]) {
    let (consulted, read, listed) = (
        paths(field(case, "consulted")),
        paths(field(case, "read")),
        paths(field(case, "listed")),
    );
    let mut requested = BTreeSet::new();
    let mut marker_dirs = BTreeSet::new();
    // (r3) B3-b0 r4 takes a gitlink as item 6b's report, as the core does, so
    // no representation allowance remains.
    for (op, path) in trace {
        let allowed = match *op {
            "request-entry" | "request-markers" | "request-custody" => consulted.contains(path),
            "request-children" => listed.contains(path),
            "request-bytes" => read.contains(path),
            "request-verdict" => consulted.contains(path),
            _ => continue,
        };
        assert!(
            allowed,
            "{id}: the core asked {op} {path}, which the reference never touched"
        );
        if *op == "request-markers" {
            marker_dirs.insert(path.clone());
        }
        requested.insert(path.clone());
    }
    for (op, path) in trace {
        let ok = match *op {
            "open-directory" => requested.iter().any(|r| under(r, path)),
            "observe" | "open-capture" | "read" | "list" => requested.contains(path),
            "lookup-marker" => marker_dirs
                .iter()
                .any(|d| path.rsplit_once('/').map_or(d.is_empty(), |(p, _)| p == d)),
            _ => continue,
        };
        assert!(
            ok,
            "{id}: the native observation made {op} {path}, which no request needed"
        );
    }
}

/// (r3, Codex B3B2B2B-R2-RF-1) No walk enters a member's gitlink: the walker
/// may probe the gitlink directory itself and look up its direct children
/// (its `opensip.json` and VCS markers), as it does at every boundary, but
/// never lists it, opens below it, or observes anything deeper.
fn check_gitlinks_not_entered(id: &str, case: &V, native: &str, walked: &[(&'static str, String)]) {
    for g in items(field(case, "gitlinks")) {
        let gitlink = format!(
            "{native}/{}/{}",
            text(field(g, "member")),
            text(field(g, "path"))
        );
        for (op, path) in walked {
            let Some(below) = path.strip_prefix(&gitlink) else {
                continue;
            };
            let entered = match below.strip_prefix('/') {
                None if below.is_empty() => *op == "list",
                None => false,
                Some(rest) => *op == "list" || *op == "open" || rest.contains('/'),
            };
            assert!(
                !entered,
                "{id}: the walk made {op} {path} inside gitlink {gitlink}"
            );
        }
    }
}

/// (r3, A4-2 step 1) The array gate refuses before any member decision: the
/// core requests no directory custody and no item-6b verdict.
fn gated(case: &V) -> bool {
    matches!(field(field(case, "expected"), "detail"),
        V::String(d) if d == "JOIN_PATH_GRAMMAR" || d.starts_with("TOO_MANY_"))
}
fn check_gate(id: &str, case: &V, trace: &[(&'static str, String)]) {
    if gated(case) {
        let decided: Vec<_> = trace
            .iter()
            .filter(|(op, _)| *op == "request-custody" || *op == "request-verdict")
            .collect();
        assert!(
            decided.is_empty(),
            "{id}: the gate's refusal came after {decided:?}"
        );
    }
}

#[test]
fn every_composition_vector_equals_the_reference_record_and_links() {
    churned(|| {
        let body = parse_json(VECTORS).unwrap();
        let cases = items(field(&body, "cases"));
        assert_eq!(cases.len(), 41);
        let (mut gitlinked, mut gates) = (0, 0);
        for case in cases {
            let id = text(field(case, "id"));
            super::super::workspace_observation::take_trace();
            crate::custody::discovery_walk::take_trace();
            let (result, native) = run(case);
            let trace = super::super::workspace_observation::take_trace();
            let walked = crate::custody::discovery_walk::take_trace();
            let discovery = result.unwrap_or_else(|e| panic!("{id}: {e:?}"));
            assert_eq!(
                &respell(discovery.result.to_json(), &native),
                field(case, "expected"),
                "{id}: record"
            );
            let links = V::Array(discovery.links.iter().map(link_json).collect());
            assert_eq!(
                &respell(links, &native),
                field(case, "links"),
                "{id}: links"
            );
            check_access(id, case, &trace);
            check_gitlinks_not_entered(id, case, &native, &walked);
            check_gate(id, case, &trace);
            gitlinked += (!items(field(case, "gitlinks")).is_empty()) as usize;
            gates += gated(case) as usize;
        }
        assert_eq!((gitlinked, gates), (11, 6));
    });
}

/// (r3) The paired control: without its gitlink, the unreadable directory
/// below `repos/a/sub` is listed by the walk and fails the discovery, so the
/// vector's acceptance shows the gitlink kept the walk out of it.
#[test]
fn without_its_gitlink_the_unlistable_subtree_fails_the_walk() {
    churned(|| {
        let mut case = vector("a-member-gitlink-subtree-unlistable-config-workspace-roots");
        let V::Object(fields) = &mut case else {
            panic!()
        };
        fields.insert("gitlinks".to_owned(), V::Array(Vec::new()));
        crate::custody::discovery_walk::take_trace();
        let (result, native) = run(&case);
        let walked = crate::custody::discovery_walk::take_trace();
        assert!(
            result.is_err(),
            "the walk lists the unreadable directory: {result:?}"
        );
        assert!(
            walked
                .iter()
                .any(|(op, path)| *op == "list" && path == &format!("{native}/repos/a/sub")),
            "the walk listed repos/a/sub"
        );
    });
}

// ------------------------------------------------- r2: the object bindings

fn vector(id: &str) -> V {
    let body = parse_json(VECTORS).unwrap();
    items(field(&body, "cases"))
        .iter()
        .find(|c| text(field(c, "id")) == id)
        .unwrap()
        .clone()
}
/// A hook that runs `act` once, at `point` for `path`.
fn once(point: &'static str, path: &'static str, act: impl FnOnce() + 'static) -> Option<Hook> {
    let mut act = Some(act);
    Some(Box::new(move |at: &str, rel: &str| {
        if at == point
            && rel == path
            && let Some(act) = act.take()
        {
            act();
        }
    }))
}
/// The discovery failed with a change of `path`, and no read reached
/// `unread`.
fn changed_without_read(result: Result<WorkspaceDiscovery, Failure>, unread: &str) {
    let trace = super::super::workspace_observation::take_trace();
    match result {
        Err(WorkFailure::Operation(WorkspaceRefusal::Walk(
            crate::custody::discovery_walk::WalkRefusal::Changed(_),
        ))) => {}
        other => panic!("expected a change, got {other:?}"),
    }
    assert!(
        !trace
            .iter()
            .any(|(op, path)| *op == "read" && path == unread),
        "{unread} was read"
    );
}
/// (r3, Codex B3B2B2B-R2-RF-2) The change was found inside item 6b's verdict
/// for `candidate`, before its admission: that verdict is the last request
/// the core made, and no walk listed anything. A change a later observer
/// catches is not enough.
fn changed_before_admission(
    result: Result<WorkspaceDiscovery, Failure>,
    candidate: &str,
    unread: &str,
) {
    let trace = super::super::workspace_observation::take_trace();
    let walked = crate::custody::discovery_walk::take_trace();
    match result {
        Err(WorkFailure::Operation(WorkspaceRefusal::Walk(
            crate::custody::discovery_walk::WalkRefusal::Changed(_),
        ))) => {}
        other => panic!("expected a change, got {other:?}"),
    }
    let last = trace
        .iter()
        .rev()
        .find(|(op, _)| op.starts_with("request-"));
    assert_eq!(
        last,
        Some(&("request-verdict", candidate.to_owned())),
        "the change was not found in item 6b's verdict"
    );
    assert!(
        !walked.iter().any(|(op, _)| *op == "list"),
        "a walk ran before the change was found"
    );
    assert!(
        !trace
            .iter()
            .any(|(op, path)| *op == "read" && path == unread),
        "{unread} was read"
    );
}
fn replace_with_repository(githome: &Path, at: &Path, crate_name: &str) {
    let aside = at.with_extension("replaced");
    std::fs::rename(at, &aside).unwrap();
    std::fs::create_dir_all(at).unwrap();
    git(githome, at, &["init", "-q"]);
    std::fs::write(
        at.join("Cargo.toml"),
        format!("[package]\nname = \"{crate_name}\"\nversion = \"1.0.0\"\n"),
    )
    .unwrap();
}

#[test]
fn a_directory_replaced_between_its_open_and_its_custody_is_a_change() {
    // `.cargo` A is opened and bound by the carrier probes; before its own
    // custody judgment it is made world-writable and moved aside, and B, a
    // passing directory, takes its name. Custody of B never authorizes a
    // read through A: the discovery fails with a change, and the carrier is
    // never read.
    churned(|| {
        super::super::workspace_observation::take_trace();
        let (result, _) = run_with(&vector("b-cargo-two-members"), |w, _| {
            let w = w.to_path_buf();
            once("before-custody", ".cargo", move || {
                let a = w.join(".cargo");
                std::fs::set_permissions(&a, std::fs::Permissions::from_mode(0o777)).unwrap();
                std::fs::rename(&a, w.join(".cargo-a")).unwrap();
                std::fs::create_dir(&a).unwrap();
                std::fs::write(a.join("config.toml"), b"[patch.crates-io]\n").unwrap();
            })
        });
        changed_without_read(result, ".cargo/config.toml");
    });
}

#[test]
fn a_reused_prefix_replaced_under_a_custody_judgment_is_a_change() {
    // `repos` is retained on the open stack; it is replaced before the
    // member custody of `repos/x` reuses it. The path is one object for the
    // whole discovery: the replacement is a change.
    churned(|| {
        super::super::workspace_observation::take_trace();
        let (result, _) = run_with(&vector("b-npm-literal-and-globs"), |w, githome| {
            let (w, githome) = (w.to_path_buf(), githome.to_path_buf());
            once("before-custody", "repos/x", move || {
                std::fs::rename(w.join("repos"), w.join("repos-a")).unwrap();
                std::fs::create_dir_all(w.join("repos/x")).unwrap();
                git(&githome, &w.join("repos/x"), &["init", "-q"]);
                std::fs::write(
                    w.join("repos/x/package.json"),
                    br#"{"name": "x", "version": "1.0.0"}"#,
                )
                .unwrap();
            })
        });
        changed_without_read(result, "repos/x/package.json");
    });
}

#[test]
fn a_member_replaced_after_the_walk_is_a_change() {
    // Branch A (r3, A4-2): the members are decided and the walk accepts with
    // `repos/a`; before the links, `repos/a` is replaced by another
    // conventional repository. The member decisions, the walk's result and
    // the links would otherwise describe different objects: the discovery
    // fails with a change.
    churned(|| {
        super::super::workspace_observation::take_trace();
        let (result, _) = run_with(&vector("a-roots-config-workspace-roots"), |w, githome| {
            let (w, githome) = (w.to_path_buf(), githome.to_path_buf());
            once("after-walk", "", move || {
                replace_with_repository(&githome, &w.join("repos/a"), "a")
            })
        });
        changed_without_read(result, "repos/a/crates/a/Cargo.toml");
    });
}

#[test]
fn an_ancestor_replaced_around_its_preserved_member_before_item_6b_is_a_change() {
    // r3 (Codex B3B2B2B-R2-RF-2): after the custody of `repos` and `repos/a`,
    // before item 6b, `repos` is moved aside, a world-writable `repos` takes
    // its name, and the original `repos/a` (its inode preserved) is moved
    // into it. Item 6b's chain passes through the unjudged ancestor: its
    // identity differs from the one custody bound, so the discovery fails
    // with a change before admission, in either branch.
    for id in ["a-roots-config-workspace-roots", "b-cargo-two-members"] {
        churned(|| {
            super::super::workspace_observation::take_trace();
            crate::custody::discovery_walk::take_trace();
            let (result, _) = run_with(&vector(id), |w, _| {
                let w = w.to_path_buf();
                once("before-verdict", "repos/a", move || {
                    let inode = std::fs::metadata(w.join("repos/a")).unwrap().ino();
                    std::fs::rename(w.join("repos"), w.join("repos-judged")).unwrap();
                    std::fs::create_dir(w.join("repos")).unwrap();
                    std::fs::set_permissions(
                        w.join("repos"),
                        std::fs::Permissions::from_mode(0o777),
                    )
                    .unwrap();
                    std::fs::rename(w.join("repos-judged/a"), w.join("repos/a")).unwrap();
                    assert_eq!(std::fs::metadata(w.join("repos/a")).unwrap().ino(), inode);
                })
            });
            changed_before_admission(result, "repos/a", "repos/a/crates/a/Cargo.toml");
        });
    }
}

#[test]
fn a_member_git_directory_replaced_before_item_6b_is_a_change() {
    // r3 (RF-2): `repos/a/.git`, bound when placement found the marker, is
    // replaced by a fresh repository's before item 6b opens it; `repos/a`
    // itself is preserved. The evidence item 6b reads is not the object the
    // decision bound: a change, in either branch.
    for id in ["a-roots-config-workspace-roots", "b-cargo-two-members"] {
        churned(|| {
            super::super::workspace_observation::take_trace();
            crate::custody::discovery_walk::take_trace();
            let (result, _) = run_with(&vector(id), |w, githome| {
                let (w, githome) = (w.to_path_buf(), githome.to_path_buf());
                once("before-verdict", "repos/a", move || {
                    let member = w.join("repos/a");
                    let inode = std::fs::metadata(&member).unwrap().ino();
                    std::fs::rename(member.join(".git"), w.join("repos/a-git-judged")).unwrap();
                    git(&githome, &member, &["init", "-q"]);
                    assert_eq!(std::fs::metadata(&member).unwrap().ino(), inode);
                })
            });
            changed_before_admission(result, "repos/a", "repos/a/crates/a/Cargo.toml");
        });
    }
}

#[test]
fn a_member_replaced_around_its_preserved_git_directory_before_item_6b_is_a_change() {
    // r3 (RF-2): only M changes. Before item 6b, `repos/a` is moved aside, a
    // new `repos/a` takes its name, and the original `repos/a/.git` (its
    // inode preserved) is moved into it. Its ancestors and Git evidence are
    // the bound objects; M is not. A change inside item 6b, in either branch.
    for id in ["a-roots-config-workspace-roots", "b-cargo-two-members"] {
        churned(|| {
            super::super::workspace_observation::take_trace();
            crate::custody::discovery_walk::take_trace();
            let (result, _) = run_with(&vector(id), |w, _| {
                let w = w.to_path_buf();
                once("before-verdict", "repos/a", move || {
                    let git_dir = w.join("repos/a/.git");
                    let inode = std::fs::metadata(&git_dir).unwrap().ino();
                    std::fs::rename(w.join("repos/a"), w.join("repos/a-judged")).unwrap();
                    std::fs::create_dir(w.join("repos/a")).unwrap();
                    std::fs::rename(w.join("repos/a-judged/.git"), &git_dir).unwrap();
                    assert_eq!(std::fs::metadata(&git_dir).unwrap().ino(), inode);
                })
            });
            changed_before_admission(result, "repos/a", "repos/a/crates/a/Cargo.toml");
        });
    }
}

#[test]
fn a_member_replaced_between_its_custody_and_item_6b_is_a_change() {
    // Branch B: `repos/a` passes directory custody; before item 6b observes
    // it, another conventional repository takes its name. The member item 6b
    // admits must be the one the decision judged: a change.
    churned(|| {
        super::super::workspace_observation::take_trace();
        crate::custody::discovery_walk::take_trace();
        let (result, _) = run_with(&vector("b-cargo-two-members"), |w, githome| {
            let (w, githome) = (w.to_path_buf(), githome.to_path_buf());
            once("before-verdict", "repos/a", move || {
                replace_with_repository(&githome, &w.join("repos/a"), "a")
            })
        });
        changed_before_admission(result, "repos/a", "repos/a/crates/a/Cargo.toml");
    });
}

#[test]
fn a_carrier_or_manifest_changed_around_its_read_is_a_change() {
    // The carrier's mode, its ACL, or its bytes during the read, and a
    // provider manifest's mode: each read is validated against the custody
    // capture of its own descriptor, so no stale verdict yields bytes.
    type Act = fn(&Path);
    let acts: [(&'static str, &'static str, Act); 4] = [
        ("before-read", "package.json", |p| {
            std::fs::set_permissions(p, std::fs::Permissions::from_mode(0o666)).unwrap()
        }),
        ("before-read", "package.json", |p| {
            let status = Command::new("/bin/chmod")
                .arg("+a")
                .arg("user:nobody allow write")
                .arg(p)
                .status()
                .unwrap();
            assert!(status.success());
        }),
        ("after-read", "package.json", |p| {
            use std::io::Write;
            std::fs::OpenOptions::new()
                .append(true)
                .open(p)
                .unwrap()
                .write_all(b" ")
                .unwrap();
        }),
        ("before-read", "repos/x/package.json", |p| {
            std::fs::set_permissions(p, std::fs::Permissions::from_mode(0o666)).unwrap()
        }),
    ];
    for (point, path, act) in acts {
        churned(|| {
            super::super::workspace_observation::take_trace();
            let (result, _) = run_with(&vector("b-npm-literal-and-globs"), |w, _| {
                let target = w.join(path);
                once(point, path, move || act(&target))
            });
            match result {
                Err(WorkFailure::Operation(WorkspaceRefusal::Walk(
                    crate::custody::discovery_walk::WalkRefusal::Changed(changed),
                ))) => assert_eq!(changed, path, "{point} {path}"),
                other => panic!("{point} {path}: expected a change, got {other:?}"),
            }
        });
    }
}

#[test]
fn a_directory_replaced_before_the_walk_is_a_change() {
    // Branch B: phase one observes `packages` for the glob classification;
    // before the walk it is replaced. The walk checks every entry it observes
    // against the decision's bindings: a change.
    churned(|| {
        super::super::workspace_observation::take_trace();
        let (result, _) = run_with(&vector("b-npm-literal-and-globs"), |w, _| {
            let w = w.to_path_buf();
            once("before-walk", "", move || {
                std::fs::rename(w.join("packages"), w.join("packages-a")).unwrap();
                std::fs::create_dir_all(w.join("packages/p")).unwrap();
                std::fs::write(w.join("packages/p/package.json"), br#"{"name": "p"}"#).unwrap();
            })
        });
        changed_without_read(result, "packages/p/package.json");
    });
}

#[test]
fn a_kept_read_is_copied_only_after_its_copy_is_charged() {
    // r3 (Codex B3B2B2B-R3-RF-1): a repeated request for a validated read is
    // a copy, charged on the discovery ledger first. A ledger that cannot
    // fund it refuses with nothing copied; one that can is charged exactly
    // the copy's owned record.
    use super::super::workspace_declarations::FileBytes;
    use super::super::workspace_observation::copy_kept;
    let kept = FileBytes::Read(vec![b'x'; 4096]);
    super::super::workspace_observation::take_trace();
    let mut tight = WorkLedger::with_limits(opensip_platform::WorkCost {
        objects: 8,
        edges: 8,
        bytes: 1024,
    })
    .unwrap();
    let refused = tight.scope(|work| copy_kept(&kept, work));
    assert!(
        matches!(refused, Err(WorkFailure::Budget(_))),
        "{refused:?}"
    );
    let trace = super::super::workspace_observation::take_trace();
    assert!(
        !trace.iter().any(|(op, _)| *op == "copy-kept"),
        "copied before its charge"
    );
    let mut ample = WorkLedger::new();
    let copy = ample.scope(|work| copy_kept(&kept, work)).unwrap();
    assert_eq!(copy, kept);
    let trace = super::super::workspace_observation::take_trace();
    assert!(trace.iter().any(|(op, _)| *op == "copy-kept"));
    assert_eq!(ample.used(), crate::custody::discovery_walk::owned(4096));
}
