// Unit C1b-1's controls (C1b plan r6, section 4): scratch repositories built
// by hand under a scratch H, observed by X2 over their own retained chain,
// then lent with the subject X2's observation proves. Nothing reads the real
// home, a real repository's objects, or the environment.
use super::*;
use crate::custody::git_tracking::{NoRepository, TrackingInputs, observe_tracking};
use crate::custody::project_chain::{
    DiscoveryRoot, ProjectChain, ProjectChainPolicy, walk_project_chain,
};
use crate::initial_installation::InitialInstallationAttempt;
use crate::trust::AclOmissionPremise;
use opensip_platform::{DescriptorFilesystem, WorkCost, WorkLedger};
use std::collections::BTreeSet;
use std::ffi::OsString;
use std::os::unix::fs::{MetadataExt, PermissionsExt};
use std::path::{Path, PathBuf};
use std::sync::atomic::AtomicBool;

const A: &str = "0123456789abcdef0123456789abcdef01234567";
const B: &str = "89abcdef0123456789abcdef0123456789abcdef";
const C: &str = "fedcba9876543210fedcba9876543210fedcba98";
/// The default ledger's limits (`WorkLedger::new`), the base the budget
/// control lowers one component of.
const DEFAULT_LIMITS: WorkCost = WorkCost {
    objects: 65_536,
    edges: 131_072,
    bytes: 268_435_456,
};
const CONFIG: &[u8] = b"[core]\n\trepositoryformatversion = 0\n\tbare = false\n";

struct Scratch(PathBuf);
impl Drop for Scratch {
    fn drop(&mut self) {
        drop(
            std::process::Command::new("/bin/chmod")
                .args(["-R", "u+rwX"])
                .arg(&self.0)
                .stderr(std::process::Stdio::null())
                .status(),
        );
        drop(std::fs::remove_dir_all(&self.0));
    }
}
/// A 0700 scratch root holding H (`home`, 0700) and `home/code` (0755).
fn scratch() -> (Scratch, PathBuf) {
    let nonce: String = opensip_platform::request_entropy()
        .unwrap()
        .iter()
        .map(|b| format!("{b:02x}"))
        .collect();
    let base = crate::test_scratch::temp_dir().join(format!("opensip-c1b1-{nonce}"));
    std::fs::create_dir(&base).unwrap();
    std::fs::set_permissions(&base, std::fs::Permissions::from_mode(0o700)).unwrap();
    let base = std::fs::canonicalize(&base).unwrap();
    let home = base.join("home");
    std::fs::create_dir(&home).unwrap();
    std::fs::set_permissions(&home, std::fs::Permissions::from_mode(0o700)).unwrap();
    dir(&home.join("code"));
    (Scratch(base), home)
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
fn any_volume(_: &DescriptorFilesystem) -> bool {
    true
}

/// A hand-built repository at `at`: `.git` with X2's admitted config and no
/// index (so nothing is tracked), `HEAD`, the given loose refs and, when
/// given, `packed-refs`.
fn repository(at: &Path, head: &[u8], loose: &[(&str, &[u8])], packed: Option<&[u8]>) {
    let git = at.join(".git");
    dir(&git);
    file(&git.join("config"), CONFIG);
    file(&git.join("HEAD"), head);
    dir(&git.join("refs"));
    for (name, content) in loose {
        file(&git.join(name), content);
    }
    if let Some(packed) = packed {
        file(&git.join("packed-refs"), packed);
    }
}
fn loose(commit: &str) -> Vec<u8> {
    format!("{commit}\n").into_bytes()
}

/// X2's observation of `root` under `home`, over its own retained chain.
struct Observed {
    chain: ProjectChain,
    tracking: crate::custody::git_tracking::TrackingObservation,
    premise: AclOmissionPremise,
    groups: BTreeSet<u32>,
}
fn observe(home: &Path, root: &Path) -> Observed {
    let premise = premise();
    let groups = BTreeSet::new();
    let volume = any_volume;
    let policy = ProjectChainPolicy::new(Some(&premise), &volume, &groups);
    let environment = [(OsString::from("HOME"), home.as_os_str().to_owned())];
    let mut ledger = WorkLedger::new();
    let (chain, tracking) = ledger
        .scope(|work| {
            let chain = walk_project_chain(home, root, uid(), &policy, work)
                .map_err(|_| WorkFailure::Operation(TrackingRefusal::VcsUnsupported("chain")))?;
            let inputs = TrackingInputs {
                chain: &chain,
                uid: uid(),
                policy: &policy,
                home,
                environment: &environment,
                system_sources: &[],
            };
            let tracking = observe_tracking(&inputs, work)?;
            Ok::<_, Failure>((chain, tracking))
        })
        .unwrap_or_else(|e| panic!("X2 observation of {}: {e:?}", root.display()));
    Observed {
        chain,
        tracking,
        premise,
        groups,
    }
}
impl Observed {
    fn subject(&self) -> VcsSubject<'_> {
        if let Some(proof) = NoRepository::retained(&self.chain, &self.tracking) {
            VcsSubject::NoRepository(proof)
        } else {
            VcsSubject::Repository(
                RepositoryProof::retained(&self.chain, &self.tracking).expect("a repository"),
            )
        }
    }
    fn spelling(&self) -> String {
        self.chain.spelling().to_str().unwrap().to_owned()
    }
    /// The VCS observation on a fresh ledger (or one with `limits`), with
    /// its charge.
    fn vcs(
        &self,
        boundaries: Option<&AdmittedBoundaries>,
        limits: Option<WorkCost>,
    ) -> (Result<String, VcsFailure>, WorkCost) {
        let lent = DiscoveryRoot::for_tests(
            self.chain.root(),
            self.chain.spelling(),
            Some(&self.premise),
        );
        let root = SnapshotRoot::for_tests_with(lent, self.subject());
        let custody = SnapshotCustody::new(uid(), &self.groups, None);
        let mut ledger = match limits {
            Some(limits) => WorkLedger::with_limits(limits).unwrap(),
            None => WorkLedger::new(),
        };
        let result = ledger.scope(|work| {
            observe_vcs(&root, custody, boundaries, work).map(|observation| render(&observation))
        });
        (result, ledger.used())
    }
}
fn render(observation: &VcsObservation<'_>) -> String {
    match observation {
        VcsObservation::None => "none".to_owned(),
        VcsObservation::Git(commit) => format!("git:{}", commit.as_str()),
        VcsObservation::Members(members) => members
            .iter()
            .map(|m| format!("{}={}", m.path(), m.commit().as_str()))
            .collect::<Vec<_>>()
            .join(","),
        VcsObservation::Unobserved => "unobserved".to_owned(),
    }
}
fn subject_of(result: Result<String, VcsFailure>) -> String {
    match result {
        Ok(observed) => panic!("expected a refusal, observed {observed}"),
        Err(WorkFailure::Operation(refusal)) => {
            refusal.subject().unwrap_or_else(|| format!("{refusal:?}"))
        }
        Err(WorkFailure::Budget(budget)) => format!("budget:{budget:?}"),
    }
}
fn boundaries(selected_root: String, members: &[&str]) -> AdmittedBoundaries {
    AdmittedBoundaries::new(
        selected_root,
        Vec::new(),
        Vec::new(),
        Vec::new(),
        Vec::new(),
        members.iter().map(|m| (*m).to_owned()).collect(),
    )
}
/// A project root `home/code/<name>` holding one repository.
fn project(
    home: &Path,
    name: &str,
    head: &[u8],
    loose: &[(&str, &[u8])],
    packed: Option<&[u8]>,
) -> PathBuf {
    let root = home.join("code").join(name);
    dir(&root);
    repository(&root, head, loose, packed);
    root
}
fn resolved(home: &Path, root: &Path) -> Result<String, VcsFailure> {
    observe(home, root).vcs(None, None).0
}

// ------------------------------------------------------------ C1-T15

#[test]
fn no_repository_and_no_member_is_none() {
    let (_s, home) = scratch();
    let root = home.join("code/w");
    dir(&root);
    let observed = observe(&home, &root);
    assert!(matches!(observed.subject(), VcsSubject::NoRepository(_)));
    let (result, used) = observed.vcs(None, None);
    assert_eq!(result.unwrap(), "none");
    assert_eq!(used, WorkCost::default());
    let record = boundaries(observed.spelling(), &[]);
    assert_eq!(observed.vcs(Some(&record), None).0.unwrap(), "none");
}

#[test]
fn head_through_a_loose_ref() {
    let (_s, home) = scratch();
    let a = loose(A);
    let root = project(
        &home,
        "p",
        b"ref: refs/heads/main\n",
        &[("refs/heads/main", &a)],
        None,
    );
    assert_eq!(resolved(&home, &root).unwrap(), format!("git:{A}"));
}

#[test]
fn head_through_packed_refs_with_and_without_the_header_and_with_peels() {
    let (_s, home) = scratch();
    let packed = format!(
        "# pack-refs with: peeled fully-peeled sorted \n{B} refs/heads/a\n{A} refs/heads/main\n{C} refs/tags/v1\n^{B}\n"
    );
    let root = project(
        &home,
        "h",
        b"ref: refs/heads/main\n",
        &[],
        Some(packed.as_bytes()),
    );
    assert_eq!(resolved(&home, &root).unwrap(), format!("git:{A}"));
    let bare = format!("{A} refs/heads/main\n^{B}\n{C} refs/tags/v1\n");
    let root = project(
        &home,
        "n",
        b"ref: refs/heads/main\n",
        &[],
        Some(bare.as_bytes()),
    );
    assert_eq!(resolved(&home, &root).unwrap(), format!("git:{A}"));
    // A peeled tag as the target resolves to the tag's own object name.
    let root = project(
        &home,
        "t",
        b"ref: refs/tags/v1\n",
        &[],
        Some(packed.as_bytes()),
    );
    assert_eq!(resolved(&home, &root).unwrap(), format!("git:{C}"));
}

#[test]
fn a_detached_head() {
    let (_s, home) = scratch();
    let root = project(&home, "d", &loose(B), &[], None);
    assert_eq!(resolved(&home, &root).unwrap(), format!("git:{B}"));
}

#[test]
fn an_unborn_head_refuses_unborn_head() {
    let (_s, home) = scratch();
    let root = project(&home, "u", b"ref: refs/heads/main\n", &[], None);
    assert_eq!(
        subject_of(resolved(&home, &root)),
        "vcs-unsupported:unborn-head"
    );
    let packed = format!("{A} refs/heads/other\n");
    let root = project(
        &home,
        "v",
        b"ref: refs/heads/main\n",
        &[],
        Some(packed.as_bytes()),
    );
    assert_eq!(
        subject_of(resolved(&home, &root)),
        "vcs-unsupported:unborn-head"
    );
}

#[test]
fn the_innermost_of_nested_enclosing_repositories() {
    let (_s, home) = scratch();
    let a = loose(A);
    let b = loose(B);
    let outer = project(
        &home,
        "outer",
        b"ref: refs/heads/main\n",
        &[("refs/heads/main", &a)],
        None,
    );
    let inner = outer.join("inner");
    dir(&inner);
    repository(
        &inner,
        b"ref: refs/heads/main\n",
        &[("refs/heads/main", &b)],
        None,
    );
    let root = inner.join("src");
    dir(&root);
    assert_eq!(resolved(&home, &root).unwrap(), format!("git:{B}"));
    assert_eq!(resolved(&home, &inner).unwrap(), format!("git:{B}"));
}

#[test]
fn a_loose_ref_wins_over_packed_refs() {
    let (_s, home) = scratch();
    let a = loose(A);
    let packed = format!("{B} refs/heads/main\n");
    let root = project(
        &home,
        "w",
        b"ref: refs/heads/main\n",
        &[("refs/heads/main", &a)],
        Some(packed.as_bytes()),
    );
    assert_eq!(resolved(&home, &root).unwrap(), format!("git:{A}"));
}

// ------------------------------------------------------------ LD-C1B-2's refusals

/// (name, HEAD, loose refs, packed-refs, the refusal's reason).
type RefusalCase = (
    &'static str,
    Vec<u8>,
    Vec<(&'static str, Vec<u8>)>,
    Option<Vec<u8>>,
    &'static str,
);

#[test]
fn each_closed_form_refusal() {
    let (_s, home) = scratch();
    let cases: Vec<RefusalCase> = vec![
        (
            "crlf",
            format!("{A}\r\n").into_bytes(),
            vec![],
            None,
            "head-malformed",
        ),
        (
            "upper",
            format!("{}\n", A.to_uppercase()).into_bytes(),
            vec![],
            None,
            "head-malformed",
        ),
        (
            "no-lf",
            b"ref: refs/heads/main".to_vec(),
            vec![],
            None,
            "head-malformed",
        ),
        (
            "not-refs",
            b"ref: heads/main\n".to_vec(),
            vec![],
            None,
            "head-malformed",
        ),
        (
            "lone-at",
            b"ref: @\n".to_vec(),
            vec![],
            None,
            "head-malformed",
        ),
        (
            "leading-slash",
            b"ref: /refs/heads/main\n".to_vec(),
            vec![],
            None,
            "head-malformed",
        ),
        ("empty", Vec::new(), vec![], None, "head-malformed"),
        (
            "chain",
            b"ref: refs/heads/main\n".to_vec(),
            vec![("refs/heads/main", b"ref: refs/heads/other\n".to_vec())],
            None,
            "symbolic-ref-chain",
        ),
        (
            "loose-malformed",
            b"ref: refs/heads/main\n".to_vec(),
            vec![("refs/heads/main", format!("{A}\n\n").into_bytes())],
            None,
            "loose-ref-malformed",
        ),
        (
            "packed-garbage",
            b"ref: refs/heads/main\n".to_vec(),
            vec![],
            Some(b"garbage\n".to_vec()),
            "packed-refs-malformed",
        ),
        (
            "packed-duplicate",
            b"ref: refs/heads/main\n".to_vec(),
            vec![],
            Some(format!("{A} refs/heads/main\n{B} refs/heads/main\n").into_bytes()),
            "packed-refs-malformed",
        ),
        (
            "packed-unsorted",
            b"ref: refs/heads/main\n".to_vec(),
            vec![],
            Some(format!("{A} refs/heads/z\n{B} refs/heads/main\n").into_bytes()),
            "packed-refs-malformed",
        ),
        (
            "packed-orphan-peel",
            b"ref: refs/heads/main\n".to_vec(),
            vec![],
            Some(format!("^{A}\n{B} refs/heads/main\n").into_bytes()),
            "packed-refs-malformed",
        ),
        (
            "packed-double-peel",
            b"ref: refs/heads/main\n".to_vec(),
            vec![],
            Some(format!("{B} refs/heads/main\n^{A}\n^{A}\n").into_bytes()),
            "packed-refs-malformed",
        ),
        (
            "packed-no-final-lf",
            b"ref: refs/heads/main\n".to_vec(),
            vec![],
            Some(format!("{B} refs/heads/main").into_bytes()),
            "packed-refs-malformed",
        ),
        (
            "packed-header-not-first",
            b"ref: refs/heads/main\n".to_vec(),
            vec![],
            Some(format!("{B} refs/heads/main\n# pack-refs with: sorted\n").into_bytes()),
            "packed-refs-malformed",
        ),
        ("head-missing", Vec::new(), vec![], None, "head-missing"),
    ];
    for (index, (name, head, refs, packed, reason)) in cases.into_iter().enumerate() {
        let refs: Vec<(&str, &[u8])> = refs.iter().map(|(n, c)| (*n, c.as_slice())).collect();
        let root = project(&home, &format!("r{index}"), &head, &refs, packed.as_deref());
        if name == "head-missing" {
            std::fs::remove_file(root.join(".git/HEAD")).unwrap();
        }
        assert_eq!(
            subject_of(resolved(&home, &root)),
            format!("vcs-unsupported:{reason}"),
            "{name}"
        );
    }
}

/// One control per grammar rule (r2, RF-2), as `HEAD`'s target and as a
/// `packed-refs` name; each refuses `ref-name`, never `unborn-head`.
#[test]
fn every_ref_name_rule_refuses_ref_name_in_head_and_in_packed_refs() {
    let (_s, home) = scratch();
    let mut names: Vec<Vec<u8>> = [
        "refs/heads/a..b",
        "refs/heads/topic.",
        "refs/heads/.hidden",
        "refs/heads/x.lock",
        "refs/heads/a\u{1}b",
        "refs/heads/a\u{7f}b",
        "refs/heads/a b",
        "refs/heads/a~b",
        "refs/heads/a^b",
        "refs/heads/a:b",
        "refs/heads/a?b",
        "refs/heads/a*b",
        "refs/heads/a[b",
        "refs/heads/a\\b",
        "refs/heads/a@{b",
        "refs/heads/",
        "refs//heads/main",
    ]
    .iter()
    .map(|n| n.as_bytes().to_vec())
    .collect();
    names.push(b"refs/heads/\xff".to_vec());
    for (index, name) in names.iter().enumerate() {
        let mut head = b"ref: ".to_vec();
        head.extend_from_slice(name);
        head.push(b'\n');
        let root = project(&home, &format!("h{index}"), &head, &[], None);
        assert_eq!(
            subject_of(resolved(&home, &root)),
            "vcs-unsupported:ref-name",
            "HEAD {}",
            String::from_utf8_lossy(name)
        );
        let mut packed = format!("{A} ").into_bytes();
        packed.extend_from_slice(name);
        packed.push(b'\n');
        let root = project(
            &home,
            &format!("k{index}"),
            b"ref: refs/heads/main\n",
            &[],
            Some(&packed),
        );
        assert_eq!(
            subject_of(resolved(&home, &root)),
            "vcs-unsupported:ref-name",
            "packed {}",
            String::from_utf8_lossy(name)
        );
    }
    // The lone `@` and a leading `/` are not `refs/` names: in packed-refs
    // they refuse `ref-name`; as `HEAD`'s target, `head-malformed` (above).
    for (index, name) in ["@", "/refs/heads/main"].iter().enumerate() {
        let packed = format!("{A} {name}\n");
        let root = project(
            &home,
            &format!("q{index}"),
            b"ref: refs/heads/main\n",
            &[],
            Some(packed.as_bytes()),
        );
        assert_eq!(
            subject_of(resolved(&home, &root)),
            "vcs-unsupported:ref-name",
            "{name}"
        );
    }
}

/// r6: a component the kernel refuses as too long (`ENAMETOOLONG`) or the
/// platform refuses over its 1,023-byte bound (`InvalidInput`) refuses
/// `ref-name`, never absent and never a custody reason.
#[test]
fn a_too_long_target_component_refuses_ref_name() {
    let (_s, home) = scratch();
    for (index, (length, leaf)) in [(300, false), (1100, false), (300, true)]
        .iter()
        .enumerate()
    {
        let long = "a".repeat(*length);
        let target = if *leaf {
            format!("refs/heads/{long}")
        } else {
            format!("refs/heads/{long}/x")
        };
        let head = format!("ref: {target}\n");
        let root = project(&home, &format!("l{index}"), head.as_bytes(), &[], None);
        dir(&root.join(".git/refs/heads"));
        assert_eq!(
            subject_of(resolved(&home, &root)),
            "vcs-unsupported:ref-name",
            "{length} {leaf}"
        );
    }
}

#[test]
fn a_fifo_as_head_refuses_head_not_file() {
    let (_s, home) = scratch();
    let root = project(&home, "f", b"ref: refs/heads/main\n", &[], None);
    let head = root.join(".git/HEAD");
    std::fs::remove_file(&head).unwrap();
    assert!(
        std::process::Command::new("/usr/bin/mkfifo")
            .arg(&head)
            .status()
            .unwrap()
            .success()
    );
    std::fs::set_permissions(&head, std::fs::Permissions::from_mode(0o644)).unwrap();
    assert_eq!(
        subject_of(resolved(&home, &root)),
        "vcs-unsupported:head-not-file"
    );
}

// ------------------------------------------------------------ custody (LD-C1B-4)

#[test]
fn custody_refusals() {
    let (_s, home) = scratch();
    let a = loose(A);
    // A group-writable HEAD.
    let root = project(
        &home,
        "g",
        b"ref: refs/heads/main\n",
        &[("refs/heads/main", &a)],
        None,
    );
    std::fs::set_permissions(
        root.join(".git/HEAD"),
        std::fs::Permissions::from_mode(0o664),
    )
    .unwrap();
    assert_eq!(
        subject_of(resolved(&home, &root)),
        "vcs-unsupported:head-custody"
    );
    // A hard-linked packed-refs.
    let packed = format!("{A} refs/heads/main\n");
    let root = project(
        &home,
        "l",
        b"ref: refs/heads/main\n",
        &[],
        Some(packed.as_bytes()),
    );
    std::fs::hard_link(root.join(".git/packed-refs"), root.join("second-name")).unwrap();
    assert_eq!(
        subject_of(resolved(&home, &root)),
        "vcs-unsupported:packed-refs-custody"
    );
    // A symlinked refs directory, and a symlinked ref segment.
    let root = project(&home, "s", b"ref: refs/heads/main\n", &[], None);
    let elsewhere = home.join("code/elsewhere");
    dir(&elsewhere.join("heads"));
    file(&elsewhere.join("heads/main"), &a);
    std::fs::remove_dir(root.join(".git/refs")).unwrap();
    std::os::unix::fs::symlink(&elsewhere, root.join(".git/refs")).unwrap();
    assert_eq!(
        subject_of(resolved(&home, &root)),
        "vcs-unsupported:ref-not-directory"
    );
    let root = project(&home, "t", b"ref: refs/heads/main\n", &[], None);
    std::os::unix::fs::symlink(elsewhere.join("heads"), root.join(".git/refs/heads")).unwrap();
    assert_eq!(
        subject_of(resolved(&home, &root)),
        "vcs-unsupported:ref-not-directory"
    );
    // A symlinked loose ref.
    let root = project(&home, "u", b"ref: refs/heads/main\n", &[], None);
    dir(&root.join(".git/refs/heads"));
    std::os::unix::fs::symlink(
        elsewhere.join("heads/main"),
        root.join(".git/refs/heads/main"),
    )
    .unwrap();
    assert_eq!(
        subject_of(resolved(&home, &root)),
        "vcs-unsupported:loose-ref-not-file"
    );
    // A group-writable ref directory.
    let root = project(
        &home,
        "v",
        b"ref: refs/heads/main\n",
        &[("refs/heads/main", &a)],
        None,
    );
    std::fs::set_permissions(
        root.join(".git/refs/heads"),
        std::fs::Permissions::from_mode(0o775),
    )
    .unwrap();
    assert_eq!(
        subject_of(resolved(&home, &root)),
        "vcs-unsupported:ref-custody"
    );
}

#[test]
fn evidence_changed_when_dot_git_is_replaced() {
    let (_s, home) = scratch();
    let a = loose(A);
    let root = project(
        &home,
        "e",
        b"ref: refs/heads/main\n",
        &[("refs/heads/main", &a)],
        None,
    );
    let observed = observe(&home, &root);
    std::fs::rename(root.join(".git"), root.join("old-git")).unwrap();
    repository(
        &root,
        b"ref: refs/heads/main\n",
        &[("refs/heads/main", &a)],
        None,
    );
    assert_eq!(
        subject_of(observed.vcs(None, None).0),
        "vcs-unsupported:evidence-changed"
    );
}

// ------------------------------------------------------------ the caps (Q1)

#[test]
fn each_git_file_at_exactly_the_cap_is_read_and_one_over_refuses() {
    let (_s, home) = scratch();
    // packed-refs at exactly 4 MiB resolves; one byte more refuses.
    let tail = format!("{A} refs/heads/main\n");
    let header = |len: usize| {
        let mut h = b"# pack-refs with: sorted".to_vec();
        h.resize(len - tail.len() - 1, b' ');
        h.push(b'\n');
        h.extend_from_slice(tail.as_bytes());
        h
    };
    let exact = header(INDEX_CAP);
    assert_eq!(exact.len(), INDEX_CAP);
    let root = project(&home, "p0", b"ref: refs/heads/main\n", &[], Some(&exact));
    assert_eq!(resolved(&home, &root).unwrap(), format!("git:{A}"));
    let over = header(INDEX_CAP + 1);
    let root = project(&home, "p1", b"ref: refs/heads/main\n", &[], Some(&over));
    // One byte over: S3 config-file custody's 4 MiB size rule refuses it
    // before any byte is read; the read cap is the same 4 MiB.
    assert_eq!(
        subject_of(resolved(&home, &root)),
        "vcs-unsupported:packed-refs-custody"
    );
    // HEAD and a loose ref at exactly 4 MiB are read (and refuse their form);
    // one byte more refuses custody's size rule.
    let big = vec![b'x'; INDEX_CAP];
    let bigger = vec![b'x'; INDEX_CAP + 1];
    let root = project(&home, "h0", &big, &[], None);
    assert_eq!(
        subject_of(resolved(&home, &root)),
        "vcs-unsupported:head-malformed"
    );
    let root = project(&home, "h1", &bigger, &[], None);
    assert_eq!(
        subject_of(resolved(&home, &root)),
        "vcs-unsupported:head-custody"
    );
    let root = project(
        &home,
        "l0",
        b"ref: refs/heads/main\n",
        &[("refs/heads/main", &big)],
        None,
    );
    assert_eq!(
        subject_of(resolved(&home, &root)),
        "vcs-unsupported:loose-ref-malformed"
    );
    let root = project(
        &home,
        "l1",
        b"ref: refs/heads/main\n",
        &[("refs/heads/main", &bigger)],
        None,
    );
    assert_eq!(
        subject_of(resolved(&home, &root)),
        "vcs-unsupported:loose-ref-custody"
    );
}

/// r4: work past the ledger's remaining allowance refuses with the budget,
/// typed, with no partial observation and never `unborn-head`.
#[test]
fn a_deep_target_past_the_remaining_budget_refuses_budget() {
    let (_s, home) = scratch();
    let segments: Vec<String> = (0..40).map(|k| format!("d{k:02}")).collect();
    let target = format!("refs/{}/main", segments.join("/"));
    let head = format!("ref: {target}\n");
    let a = loose(A);
    let root = project(&home, "deep", head.as_bytes(), &[(&target, &a)], None);
    let observed = observe(&home, &root);
    let (result, used) = observed.vcs(None, None);
    assert_eq!(result.unwrap(), format!("git:{A}"));
    for short in [
        WorkCost {
            edges: used.edges - 1,
            ..DEFAULT_LIMITS
        },
        WorkCost {
            objects: used.objects - 1,
            ..DEFAULT_LIMITS
        },
        WorkCost {
            bytes: used.bytes - 1,
            ..DEFAULT_LIMITS
        },
    ] {
        let (result, _) = observed.vcs(None, Some(short));
        assert!(
            matches!(result, Err(WorkFailure::Budget(_))),
            "{short:?}: {result:?}"
        );
    }
    let (result, _) = observed.vcs(None, Some(used));
    assert_eq!(result.unwrap(), format!("git:{A}"));
}

// ------------------------------------------------------------ the join (LD-C1B-3)

#[test]
fn a_cross_root_record_and_members_under_a_repository_refuse_internal() {
    let (_s, home) = scratch();
    let a = loose(A);
    let w = home.join("code/w");
    dir(&w);
    let member = w.join("m");
    dir(&member);
    repository(
        &member,
        b"ref: refs/heads/main\n",
        &[("refs/heads/main", &a)],
        None,
    );
    let observed = observe(&home, &w);
    let other = boundaries("/elsewhere/w".to_owned(), &["m"]);
    assert!(matches!(
        observed.vcs(Some(&other), None).0,
        Err(WorkFailure::Operation(VcsRefusal::Internal(
            "cross-root-record"
        )))
    ));
    let inside = project(
        &home,
        "r",
        b"ref: refs/heads/main\n",
        &[("refs/heads/main", &a)],
        None,
    );
    dir(&inside.join("m"));
    repository(
        &inside.join("m"),
        b"ref: refs/heads/main\n",
        &[("refs/heads/main", &a)],
        None,
    );
    let observed = observe(&home, &inside);
    let record = boundaries(observed.spelling(), &["m"]);
    assert!(matches!(
        observed.vcs(Some(&record), None).0,
        Err(WorkFailure::Operation(VcsRefusal::Internal(
            "members-without-no-repository"
        )))
    ));
}

// ------------------------------------------------------------ members (LD-C1B-5)

#[test]
fn two_members_resolve_one_loose_and_one_packed() {
    let (_s, home) = scratch();
    let a = loose(A);
    let w = home.join("code/w");
    dir(&w);
    dir(&w.join("crates/one"));
    repository(
        &w.join("crates/one"),
        b"ref: refs/heads/main\n",
        &[("refs/heads/main", &a)],
        None,
    );
    dir(&w.join("two"));
    let packed = format!("{B} refs/heads/main\n");
    repository(
        &w.join("two"),
        b"ref: refs/heads/main\n",
        &[],
        Some(packed.as_bytes()),
    );
    let observed = observe(&home, &w);
    let record = boundaries(observed.spelling(), &["crates/one", "two"]);
    assert_eq!(
        observed.vcs(Some(&record), None).0.unwrap(),
        format!("crates/one={A},two={B}")
    );
    // A member whose placement changed refuses with its MemberRefusal subject.
    std::fs::rename(w.join("two/.git"), w.join("two/moved")).unwrap();
    match observed.vcs(Some(&record), None).0 {
        Err(WorkFailure::Operation(refusal @ VcsRefusal::Member { index: 1, .. })) => {
            assert_eq!(
                refusal.subject().unwrap(),
                "member-vcs-unsupported:evidence-changed"
            );
        }
        other => panic!("{other:?}"),
    }
    // A marker between W and M is item 6b's `vcs-other`.
    dir(&w.join("crates/.hg"));
    match observed.vcs(Some(&record), None).0 {
        Err(WorkFailure::Operation(refusal @ VcsRefusal::Member { index: 0, .. })) => {
            assert_eq!(
                refusal.subject().unwrap(),
                "member-vcs-unsupported:vcs-other"
            );
        }
        other => panic!("{other:?}"),
    }
}

#[test]
fn a_members_refusals_keep_the_member_projection() {
    let (_s, home) = scratch();
    let w = home.join("code/w");
    dir(&w);
    dir(&w.join("m"));
    repository(&w.join("m"), b"ref: refs/heads/main\n", &[], None);
    let observed = observe(&home, &w);
    let record = boundaries(observed.spelling(), &["m"]);
    assert_eq!(
        subject_of(observed.vcs(Some(&record), None).0),
        "member-vcs-unsupported:unborn-head"
    );
    let long = format!("ref: refs/heads/{}/x\n", "a".repeat(300));
    file(&w.join("m/.git/HEAD"), long.as_bytes());
    dir(&w.join("m/.git/refs/heads"));
    assert_eq!(
        subject_of(observed.vcs(Some(&record), None).0),
        "member-vcs-unsupported:ref-name"
    );
}

/// r6 (R5-RF-1): a member reached through a multibyte path of 256
/// segments, each of 15 or 16 four-byte scalars (the review's
/// counterexample), resolves; its charge is checked against the model in
/// `the_observation_charges_exactly_the_models_vcs_term`.
#[test]
fn a_member_reached_through_a_deep_multibyte_path() {
    let (_s, home) = scratch();
    let w = home.join("code/w");
    dir(&w);
    let member = deep_multibyte_member(&w);
    let observed = observe(&home, &w);
    let record = boundaries(observed.spelling(), &[&member]);
    assert_eq!(
        observed.vcs(Some(&record), None).0.unwrap(),
        format!("{member}={A}")
    );
}
/// The review's 256-segment path, with a member repository at M.
fn deep_multibyte_member(w: &Path) -> String {
    let wide = '\u{10000}';
    let mut segments: Vec<String> = (0..255)
        .map(|_| std::iter::repeat_n(wide, 15).collect())
        .collect();
    segments.push(std::iter::repeat_n(wide, 16).collect());
    let at = segments.join("/");
    let stage = w.with_file_name("stage-deep");
    dir(&stage);
    let a = loose(A);
    repository(
        &stage,
        b"ref: refs/heads/main\n",
        &[("refs/heads/main", &a)],
        None,
    );
    place(w, &at, &stage.join(".git"));
    at
}

// ------------------------------------------------------------ the record (R4-RF-1)

/// The record-length function equals the identity crate's canonical encoder
/// for paths with every escape class, DEL, C1 and 2-, 3- and 4-byte UTF-8,
/// and at the maximal record.
#[test]
fn the_record_length_equals_the_canonical_encoding() {
    use opensip_identity::{JsonInteger, JsonValue as V, canonical_bytes};
    let commit = CommitId::parse(A.as_bytes()).unwrap();
    let digest = "f".repeat(64);
    let obj = |fields: Vec<(&str, V)>| {
        V::Object(fields.into_iter().map(|(k, v)| (k.to_owned(), v)).collect())
    };
    let int = |n: i128| V::Integer(JsonInteger::new(n).unwrap());
    let s = |x: &str| V::String(x.to_owned());
    let none = obj(vec![
        ("schemaVersion", int(2)),
        ("kind", s("none")),
        ("commitId", V::Null),
        ("dirty", V::Bool(false)),
        ("sourceInventoryDigest", s(&digest)),
    ]);
    let git2 = obj(vec![
        ("schemaVersion", int(2)),
        ("kind", s("git")),
        ("commitId", s(A)),
        ("dirty", V::Bool(true)),
        ("sourceInventoryDigest", s(&digest)),
    ]);
    assert_eq!(
        VcsObservation::None.encoded_len().unwrap(),
        canonical_bytes(&none).unwrap().len()
    );
    assert_eq!(
        VcsObservation::Git(commit).encoded_len().unwrap(),
        canonical_bytes(&git2).unwrap().len()
    );
    assert_eq!(VcsObservation::Unobserved.encoded_len(), None);
    let schema3 = |paths: &[String]| {
        let members = paths
            .iter()
            .map(|p| {
                obj(vec![
                    ("commitId", s(A)),
                    ("dirty", V::Bool(true)),
                    ("kind", s("git")),
                    ("path", s(p)),
                ])
            })
            .collect();
        obj(vec![
            ("schemaVersion", int(3)),
            ("kind", s("none")),
            ("commitId", V::Null),
            ("dirty", V::Bool(false)),
            ("sourceInventoryDigest", s(&digest)),
            ("members", V::Array(members)),
        ])
    };
    let six: Vec<char> = (1u8..0x20)
        .map(char::from)
        .filter(|c| !matches!(c, '\u{8}' | '\u{c}' | '\n' | '\r' | '\t'))
        .collect();
    let mut maximal: Vec<String> = (0..64)
        .map(|i| {
            let fill = six[i % six.len()];
            let mark = six[(i / six.len()) % six.len()];
            let mut parts: Vec<String> = (0..15)
                .map(|_| std::iter::repeat_n(fill, 255).collect())
                .collect();
            parts.push(
                std::iter::once(mark)
                    .chain(std::iter::repeat_n(fill, 127))
                    .collect(),
            );
            parts.push(std::iter::repeat_n(fill, 127).collect());
            parts.join("/")
        })
        .collect();
    maximal.sort();
    let cases: Vec<Vec<String>> = vec![
        vec!["a".to_owned()],
        vec!["crates/a".to_owned(), "crates/b\"q".to_owned()],
        vec![
            "x\u{8}\u{c}\n\r\t".to_owned(),
            "y\u{1}\u{1f}\u{7f}\u{85}".to_owned(),
            "z/é/日本/𝄞".to_owned(),
        ],
        maximal,
    ];
    for paths in &cases {
        let observation = VcsObservation::Members(
            paths
                .iter()
                .map(|path| MemberCommit { path, commit })
                .collect(),
        );
        let expected = canonical_bytes(&schema3(paths)).unwrap().len();
        assert_eq!(
            observation.encoded_len().unwrap(),
            expected,
            "{} members",
            paths.len()
        );
    }
    assert_eq!(
        VcsObservation::Members(
            cases[3]
                .iter()
                .map(|path| MemberCommit { path, commit })
                .collect()
        )
        .encoded_len()
        .unwrap(),
        1_573_798
    );
}

// ------------------------------------------------------------ source pins

/// No environment read (item 4's forbidden substitutes), and the model's
/// record size.
#[test]
fn the_module_reads_no_environment() {
    let source = include_str!("snapshot_vcs.rs");
    for forbidden in ["env::", "var_os", "vars_os", "HOME", "getenv"] {
        assert!(!source.contains(forbidden), "{forbidden}");
    }
    assert_eq!(std::mem::size_of::<MemberCommit<'_>>(), 56);
}

// ------------------------------------------------------------ the model (LD-C1B-6)

/// Each repository of `snapshot_vcs_vectors.json` built and observed
/// natively on a fresh ledger: the observation is the case's, and its charge
/// equals the model's exactly (C1a2's method). Then the reach pricing
/// control: the model's reach over multibyte paths equals the platform's own
/// cost functions over their segments (C1b plan r6, R5-RF-1).
#[test]
fn the_observation_charges_exactly_the_models_vcs_term() {
    use opensip_identity::{JsonValue as V, parse_json};
    const VECTORS: &[u8] = include_bytes!("snapshot_vcs_vectors.json");
    let field = |v: &V, k: &str| -> V {
        match v {
            V::Object(m) => m.get(k).cloned().unwrap_or(V::Null),
            _ => V::Null,
        }
    };
    let text = |v: V| match v {
        V::String(s) => s,
        other => panic!("not a string: {other:?}"),
    };
    let count = |v: V| match v {
        V::Integer(i) => usize::try_from(i.get()).unwrap(),
        other => panic!("not an integer: {other:?}"),
    };
    let items = |v: V| match v {
        V::Array(a) => a,
        other => panic!("not an array: {other:?}"),
    };
    let cost = |v: V| WorkCost {
        objects: count(field(&v, "objects")),
        edges: count(field(&v, "edges")),
        bytes: count(field(&v, "bytes")),
    };
    let doc = parse_json(VECTORS).unwrap();
    let (_s, home) = scratch();
    let cases = items(field(&doc, "cases"));
    assert_eq!(cases.len(), 9);
    for (index, case) in cases.iter().enumerate() {
        let id = text(field(case, "id"));
        let repos = items(field(case, "repos"));
        let spec = |repo: &V| {
            let loose: Vec<(String, Vec<u8>)> = match field(repo, "loose") {
                V::Object(m) => m
                    .iter()
                    .map(|(k, v)| (k.clone(), text(v.clone()).into_bytes()))
                    .collect(),
                _ => Vec::new(),
            };
            let packed = match field(repo, "packed") {
                V::Null => None,
                v => Some(text(v).into_bytes()),
            };
            (text(field(repo, "head")).into_bytes(), loose, packed)
        };
        let root = home.join("code").join(format!("m{index}"));
        dir(&root);
        let mut paths = Vec::new();
        if text(field(case, "kind")) == "enclosing" {
            let (head, loose, packed) = spec(&repos[0]);
            let loose: Vec<(&str, &[u8])> = loose
                .iter()
                .map(|(n, c)| (n.as_str(), c.as_slice()))
                .collect();
            repository(&root, &head, &loose, packed.as_deref());
        } else {
            for (k, repo) in repos.iter().enumerate() {
                let at = text(field(repo, "at"));
                let stage = home.join("code").join(format!("stage-{index}-{k}"));
                dir(&stage);
                let (head, loose, packed) = spec(repo);
                let loose: Vec<(&str, &[u8])> = loose
                    .iter()
                    .map(|(n, c)| (n.as_str(), c.as_slice()))
                    .collect();
                repository(&stage, &head, &loose, packed.as_deref());
                place(&root, &at, &stage.join(".git"));
                paths.push(at);
            }
        }
        let observed = observe(&home, &root);
        let names: Vec<&str> = paths.iter().map(String::as_str).collect();
        let record = boundaries(observed.spelling(), &names);
        let with = if names.is_empty() {
            None
        } else {
            Some(&record)
        };
        let (result, used) = observed.vcs(with, None);
        assert_eq!(result.unwrap(), text(field(case, "expect")), "{id}");
        assert_eq!(used, cost(field(case, "predicted")), "{id}");
    }
    // The reach pricing control.
    let status = {
        let mut ledger = WorkLedger::new();
        ledger
            .scope(|work| git::snapshot_metadata(&std::fs::File::open(&home).unwrap(), work))
            .unwrap();
        ledger.used()
    };
    for reach in items(field(&doc, "reach")) {
        let path = text(field(&reach, "path"));
        let mut native = WorkCost::default();
        let mut add = |c: WorkCost| {
            native = WorkCost {
                objects: native.objects + c.objects,
                edges: native.edges + c.edges,
                bytes: native.bytes + c.bytes,
            }
        };
        for segment in path.split('/') {
            add(opensip_platform::open_child_directory_cost(
                std::ffi::OsStr::new(segment),
            ));
            add(status);
            for marker in [".git", ".hg", ".svn", ".jj"] {
                add(opensip_platform::child_absence_observation_cost(
                    std::ffi::OsStr::new(marker),
                ));
            }
        }
        assert_eq!(
            native,
            cost(field(&reach, "predicted")),
            "{} scalars",
            path.chars().count()
        );
    }
}
/// Make the member path `at` below `w` one relative step at a time (a deep
/// path's absolute spelling exceeds PATH_MAX) and move the staged `.git`
/// into it.
fn place(w: &Path, at: &str, staged: &Path) {
    let mut script = String::from("set -e\numask 022\n");
    for segment in at.split('/') {
        script.push_str(&format!("mkdir '{segment}'\ncd '{segment}'\n"));
    }
    script.push_str("mv \"$1\" .git\n");
    let status = std::process::Command::new("/bin/sh")
        .arg("-c")
        .arg(&script)
        .arg("sh")
        .arg(staged)
        .current_dir(w)
        .env_clear()
        .env("PATH", "/usr/bin:/bin")
        .status()
        .unwrap();
    assert!(status.success());
}
