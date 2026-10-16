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
            "file" => std::fs::write(&path, text(field(entry, "text")).as_bytes()).unwrap(),
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
    let premise = premise();
    let groups = BTreeSet::new();
    let authorized = AuthorizedGroups::from_invocation(&[]).unwrap();
    let volume = any_volume;
    let policy = ProjectChainPolicy::new(Some(&premise), &volume, &groups);
    let clean: Vec<(OsString, OsString)> = vec![(
        std::ffi::OsStr::new("HOME").to_os_string(),
        home.clone().into_os_string(),
    )];
    let upward = upward_of(field(case, "upward"));
    let none = BTreeSet::new();
    let invocation = DiscoveryInvocation {
        invoking_uid: uid(),
        ci: false,
        groups: &authorized,
        waiver: None,
        source: source_of(case),
        basis: MarkerCountBasis::NotEnumerated,
        member_roots: &none,
    };
    let member_inputs = MemberInputs {
        uid: uid(),
        home: &home,
        home_filesystem: &volume,
        environment: &clean,
        system_sources: &[],
        custody: MemberCustody {
            trust_groups: &groups,
            premise: Some(&premise),
        },
    };
    let result = WorkLedger::discovery_profile().scope(|work| {
        let chain = walk_project_chain(&home, &w, uid(), &policy, work).map_err(invariant)?;
        let inputs = TrackingInputs {
            chain: &chain,
            uid: uid(),
            policy: &policy,
            home: &home,
            environment: &clean,
            system_sources: &[],
        };
        let observed = observe_tracking(&inputs, work).map_err(invariant)?;
        let members = NoRepository::retained(&chain, &observed).map(|proof| MemberObservation {
            inputs: &member_inputs,
            proof,
        });
        let root = DiscoveryRoot::for_tests(chain.root(), chain.spelling(), Some(&premise));
        discover_with_members(&root, &upward, &invocation, members.as_ref(), work)
    });
    (result, w.to_str().unwrap().to_owned())
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
    for (op, path) in trace {
        let allowed = match *op {
            "request-entry" | "request-markers" => consulted.contains(path),
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

#[test]
fn every_composition_vector_equals_the_reference_record_and_links() {
    churned(|| {
        let body = parse_json(VECTORS).unwrap();
        let cases = items(field(&body, "cases"));
        assert_eq!(cases.len(), 19);
        for case in cases {
            let id = text(field(case, "id"));
            super::super::workspace_observation::take_trace();
            let (result, native) = run(case);
            let trace = super::super::workspace_observation::take_trace();
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
        }
    });
}
