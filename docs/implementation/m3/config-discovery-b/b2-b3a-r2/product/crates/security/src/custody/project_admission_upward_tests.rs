// M3-B unit B2-b3a (B2-b3 plan r2, LD-B2B3-1, LD-B2B3-7 and LD-B2B3-9): the
// analysis path's upward selection against the B2-b0 current reference, on
// scratch homes only. Each vector of tools/security/discovery_upward_vectors.py
// is a tree description: it is built here under a scratch home, selected over
// natively, and its rows, stop, VCS evidence and refusal compared with the
// reference's, with the scratch home spelled `/H`. The read session's release
// and its discovery root run on a published scratch installation.

const UPWARD_VECTORS: &[u8] = include_bytes!("discovery_upward_vectors.json");
const SCAN_VECTORS: &[u8] = include_bytes!("discovery_scan_vectors.json");
/// An invoking user who owns nothing in a scratch tree (the `foreign` cases).
const FOREIGN_UID: u32 = 4242;
/// A group that authorizes nothing in a scratch tree (`groups: other`).
const OTHER_GID: u32 = 4243;

fn upward_field<'v>(value: &'v V, key: &str) -> &'v V {
    let V::Object(fields) = value else {
        panic!("{value:?}")
    };
    fields.get(key).unwrap_or(&V::Null)
}
fn upward_text(value: &V) -> &str {
    let V::String(s) = value else {
        panic!("{value:?}")
    };
    s
}
fn upward_items(value: &V) -> &[V] {
    let V::Array(items) = value else {
        panic!("{value:?}")
    };
    items
}
fn upward_optional(value: &V) -> Option<String> {
    match value {
        V::Null => None,
        other => Some(upward_text(other).to_owned()),
    }
}
fn upward_flag(value: &V) -> bool {
    matches!(value, V::Bool(true))
}

/// A grant of a write right to another user or group, by `chmod +a`.
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

/// Build a vector's tree under `home`; hard links go to `links`, outside it.
fn materialize(home: &Path, links: &Path, tree: &[V]) {
    for (index, entry) in tree.iter().enumerate() {
        let path = home.join(upward_text(upward_field(entry, "path")));
        let mode = || u32::from_str_radix(upward_text(upward_field(entry, "mode")), 8).unwrap();
        match upward_text(upward_field(entry, "kind")) {
            "dir" => directory(&path, mode()),
            "file" => {
                let bytes = match upward_field(entry, "size") {
                    V::Integer(size) => vec![b' '; usize::try_from(size.get()).unwrap()],
                    _ => upward_text(upward_field(entry, "text")).as_bytes().to_vec(),
                };
                file(&path, &bytes, mode());
                if upward_flag(upward_field(entry, "hardlink")) {
                    fs::hard_link(&path, links.join(index.to_string())).unwrap();
                }
            }
            "symlink" => {
                std::os::unix::fs::symlink(upward_text(upward_field(entry, "target")), &path)
                    .unwrap();
            }
            "fifo" => {
                let status = std::process::Command::new("/usr/bin/mkfifo")
                    .arg("-m")
                    .arg(upward_text(upward_field(entry, "mode")))
                    .arg(&path)
                    .status()
                    .unwrap();
                assert!(status.success());
            }
            other => panic!("{other}"),
        }
        if let V::String(who) = upward_field(entry, "acl") {
            grant(
                &path,
                who,
                upward_text(upward_field(entry, "kind")) == "dir",
            );
        }
    }
}

/// The scratch home spelled as the reference's `/H`.
fn as_reference(home: &Path, path: &str) -> String {
    let home = home.to_str().unwrap();
    match path.strip_prefix(home) {
        Some(rest) if rest.is_empty() || rest.starts_with('/') => format!("/H{rest}"),
        _ => panic!("{path} is not under the scratch home"),
    }
}
fn reference_rows(
    home: &Path,
    record: &UpwardRecord,
) -> Vec<(String, String, String, Option<String>)> {
    record
        .rows()
        .unwrap()
        .into_iter()
        .map(|row| {
            (
                as_reference(home, &row.path),
                row.custody,
                row.candidate,
                row.boundary,
            )
        })
        .collect()
}
fn expected_rows(expected: &V) -> Vec<(String, String, String, Option<String>)> {
    upward_items(upward_field(expected, "walked"))
        .iter()
        .map(|row| {
            (
                upward_text(upward_field(row, "path")).to_owned(),
                upward_text(upward_field(row, "custody")).to_owned(),
                upward_text(upward_field(row, "candidate")).to_owned(),
                upward_optional(upward_field(row, "boundary")),
            )
        })
        .collect()
}

/// What `select` returns.
type Selection = Result<(Selected, Option<(File, DescriptorMetadata)>), Failure>;
/// One recorded analysis-path selection over a built vector: its result and
/// what it recorded.
fn select_vector(home: &Path, case: &V) -> (Selection, UpwardRecord) {
    let premise = premise();
    let own = fs::metadata(home).unwrap().gid();
    assert_ne!(own, OTHER_GID);
    let groups: BTreeSet<u32> = match upward_field(case, "groups") {
        V::String(g) if g == "own" => [own].into(),
        V::String(g) if g == "other" => [OTHER_GID].into(),
        _ => BTreeSet::new(),
    };
    let volume = any_volume;
    let policy = ProjectChainPolicy::new(Some(&premise), &volume, &groups);
    let invoking = if upward_flag(upward_field(case, "foreign")) {
        assert_ne!(uid(), FOREIGN_UID);
        FOREIGN_UID
    } else {
        uid()
    };
    let launch = match upward_text(upward_field(case, "launch")) {
        "" => home.to_path_buf(),
        rel => home.join(rel),
    };
    let explicit = upward_optional(upward_field(case, "explicit")).map(|rel| home.join(rel));
    let waiver = ProjectOwnerWaiver::from_invocation(
        upward_flag(upward_field(case, "waive")),
        explicit.as_deref(),
    )
    .unwrap();
    let mut record = UpwardRecord::default();
    let mut ledger = WorkLedger::new();
    let result = ledger.scope(|work| {
        super::select(
            &launch,
            explicit.as_deref(),
            home,
            invoking,
            &policy,
            true,
            waiver.as_ref(),
            Some(&mut record),
            work,
        )
    });
    (result, record)
}

#[test]
fn the_analysis_selection_reproduces_the_current_reference_on_native_trees() {
    let body = parse_json(UPWARD_VECTORS).unwrap();
    let cases = upward_items(upward_field(&body, "cases"));
    assert!(cases.len() >= 50);
    for case in cases {
        let id = upward_text(upward_field(case, "id"));
        let (_s, home) = scratch();
        let links = home.parent().unwrap().join("links");
        directory(&links, 0o700);
        materialize(&home, &links, upward_items(upward_field(case, "tree")));
        let expected = upward_field(case, "expected");
        let explicit = !matches!(upward_field(case, "explicit"), V::Null);
        let (result, record) = select_vector(&home, case);
        assert_eq!(
            reference_rows(&home, &record),
            expected_rows(expected),
            "{id}: rows"
        );
        match upward_text(upward_field(expected, "status")) {
            "ACCEPT" => {
                let (selected, _) = result.unwrap_or_else(|e| panic!("{id}: {e:?}"));
                let provenance = record.provenance(&selected).unwrap();
                assert_eq!(
                    as_reference(&home, selected.root().to_str().unwrap()),
                    upward_text(upward_field(expected, "selectedRoot")),
                    "{id}"
                );
                assert_eq!(
                    provenance.mode,
                    upward_text(upward_field(expected, "mode")),
                    "{id}"
                );
                assert_eq!(
                    provenance.config_path.map(|p| as_reference(&home, &p)),
                    upward_optional(upward_field(expected, "configPath")),
                    "{id}"
                );
                assert_eq!(
                    provenance.stop_reason,
                    upward_text(upward_field(expected, "stopReason")),
                    "{id}"
                );
                let vcs = upward_field(expected, "vcs");
                assert_eq!(
                    provenance.vcs.map(|v| (v.kind.to_owned(), v.target)),
                    match vcs {
                        V::Null => None,
                        _ => Some((
                            upward_text(upward_field(vcs, "kind")).to_owned(),
                            upward_optional(upward_field(vcs, "target")),
                        )),
                    },
                    "{id}: vcs"
                );
                assert_eq!(
                    provenance.explicit_path_was_symlink,
                    match upward_field(expected, "explicitPathWasSymlink") {
                        V::Bool(b) => Some(*b),
                        _ => None,
                    },
                    "{id}"
                );
                assert!(record.refused.is_none(), "{id}");
            }
            "REFUSE" => {
                let refusal = match result {
                    Err(WorkFailure::Operation(refusal)) => refusal,
                    other => panic!("{id}: {other:?}"),
                };
                let (code, detail, path) = record
                    .discovery_refusal(&refusal, explicit)
                    .unwrap_or_else(|| panic!("{id}: {refusal:?}"));
                assert_eq!(
                    code.code(),
                    upward_text(upward_field(expected, "refusal")),
                    "{id}"
                );
                assert_eq!(
                    detail,
                    upward_text(upward_field(expected, "detail")),
                    "{id}"
                );
                assert_eq!(
                    as_reference(&home, path.to_str().unwrap()),
                    upward_text(upward_field(expected, "path")),
                    "{id}: path"
                );
                assert_eq!(
                    upward_text(upward_field(expected, "mode")),
                    if explicit { "explicit" } else { "walk" },
                    "{id}"
                );
            }
            other => panic!("{other}"),
        }
    }
}

/// The reference's upward-only discovery cases (B2-b2's vectors list them)
/// are all here, except the two a scratch tree cannot hold, each covered by
/// its own control: a waiver without `--project` is unconstructible
/// (`grants_tests`), and an ACL that cannot be read is
/// `an_unreadable_acl_on_the_launch_refuses_custody`.
#[test]
fn every_upward_only_reference_case_a_scratch_tree_can_hold_is_a_vector() {
    let scan = parse_json(SCAN_VECTORS).unwrap();
    let upward_only: BTreeSet<&str> = upward_items(upward_field(&scan, "upwardOnly"))
        .iter()
        .map(upward_text)
        .collect();
    let body = parse_json(UPWARD_VECTORS).unwrap();
    let here: BTreeSet<&str> = upward_items(upward_field(&body, "cases"))
        .iter()
        .filter(|c| upward_flag(upward_field(c, "reference")))
        .map(|c| upward_text(upward_field(c, "id")))
        .collect();
    let elsewhere: BTreeSet<&str> = [
        "trust-project-owner-without-explicit-path-refuses",
        "unreadable-acl-on-cwd-refuses-custody-cannot-be-established",
    ]
    .into();
    assert_eq!(upward_only.len(), 19);
    assert_eq!(&upward_only - &elsewhere, here);
}

#[test]
fn an_unreadable_acl_on_the_launch_refuses_custody() {
    // With no premise, an omitted ACL cannot be judged: custody cannot be
    // established (SLM `aclUnreadable`).
    let (_s, home) = scratch();
    let launch = home.join("repo");
    directory(&launch, 0o755);
    let groups = BTreeSet::new();
    let volume = any_volume;
    let policy = ProjectChainPolicy::new(None, &volume, &groups);
    let mut record = UpwardRecord::default();
    let mut ledger = WorkLedger::new();
    let result = ledger.scope(|work| {
        super::select(
            &launch,
            None,
            &home,
            uid(),
            &policy,
            true,
            None,
            Some(&mut record),
            work,
        )
    });
    let Err(WorkFailure::Operation(refusal)) = result else {
        panic!("{result:?}")
    };
    assert_eq!(
        record.discovery_refusal(&refusal, false),
        Some((
            DiscoveryRefusal::RootCustodyRefused,
            "ACL_UNREADABLE",
            launch.as_path()
        ))
    );
    assert!(record.walked.is_empty());
}

#[test]
fn the_legacy_selection_records_nothing_and_selects_the_same_roots() {
    let body = parse_json(UPWARD_VECTORS).unwrap();
    for case in upward_items(upward_field(&body, "cases")) {
        let expected = upward_field(case, "expected");
        if upward_text(upward_field(expected, "status")) != "ACCEPT"
            || upward_flag(upward_field(case, "foreign"))
        {
            continue;
        }
        let id = upward_text(upward_field(case, "id"));
        let (_s, home) = scratch();
        let links = home.parent().unwrap().join("links");
        directory(&links, 0o700);
        materialize(&home, &links, upward_items(upward_field(case, "tree")));
        let (recorded, _) = select_vector(&home, case);
        let launch = match upward_text(upward_field(case, "launch")) {
            "" => home.clone(),
            rel => home.join(rel),
        };
        let explicit = upward_optional(upward_field(case, "explicit")).map(|rel| home.join(rel));
        let premise = premise();
        let own = fs::metadata(&home).unwrap().gid();
        let groups: BTreeSet<u32> = match upward_field(case, "groups") {
            V::String(g) if g == "own" => [own].into(),
            _ => BTreeSet::new(),
        };
        let volume = any_volume;
        let policy = ProjectChainPolicy::new(Some(&premise), &volume, &groups);
        let mut ledger = WorkLedger::new();
        let legacy = ledger
            .scope(|work| {
                select_project_root(&launch, explicit.as_deref(), &home, uid(), &policy, work)
            })
            .unwrap_or_else(|e| panic!("{id}: {e:?}"));
        assert_eq!(recorded.unwrap().0, legacy, "{id}");
    }
}

#[test]
fn a_gitdir_file_is_judged_by_custody_and_a_change_or_exhaustion_is_never_a_null_target() {
    let (_s, home) = scratch();
    let wt = home.join("wt");
    directory(&wt, 0o755);
    file(&wt.join(".git"), b"gitdir: /elsewhere\n", 0o644);
    file(&wt.join("other"), b"gitdir: /other\n", 0o644);
    let retained = RetainedDirectoryPath::open_project_root(&wt, 256).unwrap();
    let directory = retained.directory();
    let premise = premise();
    let groups = BTreeSet::new();
    let volume = any_volume;
    let policy = ProjectChainPolicy::new(Some(&premise), &volume, &groups);
    let target = |observation: &opensip_platform::ChildObservation,
                  uid: u32,
                  policy: &ProjectChainPolicy<'_>| {
        let mut ledger = WorkLedger::new();
        ledger.scope(|work| gitdir_target(directory, observation, uid, policy, work))
    };
    // An identity change between the observation and the open refuses the
    // whole operation; it is never an unavailable target.
    let other = directory.observe_child(OsStr::new("other")).unwrap();
    let mut ledger = WorkLedger::new();
    let changed = ledger.scope(|work| gitdir_target(directory, &other, uid(), &policy, work));
    assert!(matches!(
        changed,
        Err(WorkFailure::Operation(ProjectAdmissionRefusal::Changed))
    ));
    let observed = directory.observe_child(OsStr::new(".git")).unwrap();
    // Custody (r2, Codex B2B3A-R1-RF-1): a foreign owner, and an omitted
    // ACL with no premise to admit it, keep the boundary with no target.
    assert_eq!(target(&observed, FOREIGN_UID, &policy).unwrap(), None);
    let unadmitted = ProjectChainPolicy::new(None, &volume, &groups);
    assert_eq!(target(&observed, uid(), &unadmitted).unwrap(), None);
    let mut ledger = WorkLedger::new();
    assert_eq!(
        ledger
            .scope(|work| gitdir_target(directory, &observed, uid(), &policy, work))
            .unwrap(),
        Some("/elsewhere".to_owned())
    );
    // A ledger too short for the read is the budget refusal.
    let used = ledger.used();
    let mut short = WorkLedger::with_limits(WorkCost {
        objects: used.objects,
        edges: used.edges,
        bytes: used.bytes - 1,
    })
    .unwrap();
    assert!(matches!(
        short.scope(|work| gitdir_target(directory, &observed, uid(), &policy, work)),
        Err(WorkFailure::Budget(_))
    ));
    // The same through the evidence probe.
    let mut short = WorkLedger::with_limits(WorkCost {
        objects: used.objects,
        edges: used.edges,
        bytes: used.bytes - 1,
    })
    .unwrap();
    assert!(matches!(
        short.scope(|work| vcs_evidence(directory, uid(), &policy, work)),
        Err(WorkFailure::Budget(_))
    ));
}

#[test]
fn the_owner_waiver_reaches_only_its_explicit_root() {
    let (_s, home) = scratch();
    let checkout = home.join("checkout");
    directory(&checkout, 0o755);
    let waiver = ProjectOwnerWaiver::from_invocation(true, Some(&checkout))
        .unwrap()
        .unwrap();
    assert!(applicable_waiver(Some(&waiver), &checkout).is_some());
    // Never normalized: another spelling of the same directory is not it.
    let respelled = home.join("./checkout");
    assert!(applicable_waiver(Some(&waiver), &respelled).is_none());
    assert!(applicable_waiver(Some(&waiver), &home).is_none());
    // The root's own judgment: a foreign owner passes only when waived; the
    // waiver never reaches the mode.
    let premise = premise();
    let groups = BTreeSet::new();
    let volume = any_volume;
    let policy = ProjectChainPolicy::new(Some(&premise), &volume, &groups);
    let retained = RetainedDirectoryPath::open_project_root(&checkout, 256).unwrap();
    let judge = |waiver: Option<&ProjectOwnerWaiver>| {
        let mut ledger = WorkLedger::new();
        ledger.scope(|work| passes(retained.directory(), FOREIGN_UID, &policy, waiver, work))
    };
    assert!(matches!(
        judge(None).unwrap(),
        Err(ProjectChainRefusal::Root(
            crate::custody::Refusal::ForeignOwner
        ))
    ));
    assert!(judge(Some(&waiver)).unwrap().is_ok());
    fs::set_permissions(&checkout, fs::Permissions::from_mode(0o777)).unwrap();
    assert!(matches!(
        judge(Some(&waiver)).unwrap(),
        Err(ProjectChainRefusal::Root(
            crate::custody::Refusal::OthersWrite
        ))
    ));
}

#[test]
fn the_chain_walk_remembers_a_waiver_only_for_its_root() {
    // The owner is the invoking user here, so the walk passes either way;
    // what it records decides whether its recheck may waive again.
    let (_s, home) = scratch();
    let project = home.join("project");
    directory(&project, 0o755);
    let premise = premise();
    let groups = BTreeSet::new();
    let volume = any_volume;
    let policy = ProjectChainPolicy::new(Some(&premise), &volume, &groups);
    let walk = |waiver: Option<&ProjectOwnerWaiver>| {
        let mut ledger = WorkLedger::new();
        ledger
            .scope(|work| {
                super::super::project_chain::walk_project_chain_waived(
                    &home,
                    &project,
                    uid(),
                    &policy,
                    waiver,
                    work,
                )
            })
            .unwrap()
    };
    let own = ProjectOwnerWaiver::from_invocation(true, Some(&project))
        .unwrap()
        .unwrap();
    let other = ProjectOwnerWaiver::from_invocation(true, Some(&home))
        .unwrap()
        .unwrap();
    let waived = walk(Some(&own));
    assert!(waived.owner_waived_for_tests());
    assert!(!walk(Some(&other)).owner_waived_for_tests());
    assert!(!walk(None).owner_waived_for_tests());
    let mut ledger = WorkLedger::new();
    ledger
        .scope(|work| waived.recheck_waived(uid(), &policy, Some(&own), work))
        .unwrap();
}

#[test]
fn a_released_read_session_frees_the_fence_and_lends_only_the_discovery_root() {
    churned(|| {
        let fixture = ReadFixture::new("b2b3a-release");
        let project = fixture_project(&fixture);
        directory(&project.join(".git"), 0o755);
        let session = fixture.session(None).unwrap();
        let mut upward = UpwardRecord::default();
        let carriers = session
            .admit_project_carriers(
                &project,
                None,
                &BTreeSet::new(),
                LocalCarrierPolicy::NonInteractive,
                None,
                &mut upward,
            )
            .unwrap();
        let admission = session
            .complete_project_admission(carriers, &BTreeSet::new(), None)
            .unwrap();
        let fence = fixture.installation.join("lifecycle.fence");
        let free = || {
            opensip_platform::FileLock::try_acquire(
                File::open(&fence).unwrap(),
                opensip_platform::LockMode::Exclusive,
            )
            .unwrap()
            .is_some()
        };
        assert!(!free());
        let released = session.release().unwrap();
        assert!(free());
        let root = released.discovery_root(&admission);
        assert_eq!(root.spelling(), project);
        assert_eq!(
            root.root().as_file().metadata().unwrap().ino(),
            fs::metadata(&project).unwrap().ino()
        );
        assert!(root.premise().is_some());
        // The selection's upward provenance came with the admission.
        let provenance = upward.provenance(admission.selected()).unwrap();
        assert_eq!(provenance.mode, "vcs-default");
        assert_eq!(provenance.stop_reason, "VCS");
        assert_eq!(provenance.vcs.unwrap().kind, "directory");
        assert_eq!(provenance.walked.len(), 1);
    });
}

#[test]
fn a_latched_read_session_still_releases_its_fence_and_lends_nothing() {
    churned(|| {
        let fixture = ReadFixture::new("b2b3a-latched");
        let session = fixture.session(None).unwrap();
        let launch = fixture.home.join("open");
        directory(&launch, 0o777);
        let mut upward = UpwardRecord::default();
        assert!(
            session
                .admit_project_carriers(
                    &launch,
                    None,
                    &BTreeSet::new(),
                    LocalCarrierPolicy::NonInteractive,
                    None,
                    &mut upward,
                )
                .is_err()
        );
        assert_eq!(upward.refused.as_deref(), Some(launch.as_path()));
        assert!(matches!(
            session.release(),
            Err(crate::custody::installation_session::SessionRefusal::Gate(
                crate::custody::installation_admission::GateRefusal::Latched
            ))
        ));
        let fence = fixture.installation.join("lifecycle.fence");
        assert!(
            opensip_platform::FileLock::try_acquire(
                File::open(&fence).unwrap(),
                opensip_platform::LockMode::Exclusive,
            )
            .unwrap()
            .is_some()
        );
    });
}

#[test]
fn a_launch_beyond_the_retained_path_bound_refuses_at_its_open_with_no_row() {
    // X2 item 9 bounds the retained path from `/` at 256 components, so the
    // walk's own 256-level bound is reached only by a 256-component launch
    // outside H; a deeper launch refuses at its open, before any level.
    let (_s, home) = scratch();
    let mut launch = home.clone();
    while launch.components().count() <= super::super::project_chain::MAX_PROJECT_COMPONENTS + 1 {
        launch.push("d");
        directory(&launch, 0o755);
    }
    let premise = premise();
    let groups = BTreeSet::new();
    let volume = any_volume;
    let policy = ProjectChainPolicy::new(Some(&premise), &volume, &groups);
    let mut record = UpwardRecord::default();
    let mut ledger = WorkLedger::new();
    let result = ledger.scope(|work| {
        super::select(
            &launch,
            None,
            &home,
            uid(),
            &policy,
            true,
            None,
            Some(&mut record),
            work,
        )
    });
    assert!(matches!(
        result,
        Err(WorkFailure::Operation(ProjectAdmissionRefusal::Chain(
            ProjectChainRefusal::PathInvalid(_)
        )))
    ));
    assert!(record.walked.is_empty());
    assert_eq!(record.refused.as_deref(), Some(launch.as_path()));
    // The over-bound open is not discovery's refusal.
    assert_eq!(
        record.discovery_refusal(
            &ProjectAdmissionRefusal::Chain(ProjectChainRefusal::PathInvalid(io::Error::new(
                io::ErrorKind::InvalidInput,
                "over-bound"
            ))),
            false
        ),
        None
    );
    // The walk's own bound is the reference's depth refusal.
    let at = UpwardRecord {
        refused: Some(home.clone()),
        ..UpwardRecord::default()
    };
    assert_eq!(
        at.discovery_refusal(&ProjectAdmissionRefusal::WalkDepthExceeded, false),
        Some((
            DiscoveryRefusal::RootCustodyRefused,
            "WALK_DEPTH_EXCEEDED",
            home.as_path()
        ))
    );
}

#[test]
fn a_refusal_after_selection_is_never_mapped_as_a_selection_refusal() {
    // Codex B2B3A-R1-NBO-2: the chain walk can refuse with variants that
    // selection also uses; only a refusal whose object selection named maps.
    let missing = || {
        ProjectAdmissionRefusal::Chain(ProjectChainRefusal::PathInvalid(io::Error::from(
            io::ErrorKind::NotFound,
        )))
    };
    assert_eq!(
        UpwardRecord::default().discovery_refusal(&missing(), true),
        None
    );
    assert_eq!(
        UpwardRecord::default().discovery_refusal(
            &ProjectAdmissionRefusal::Chain(ProjectChainRefusal::Symlink),
            false
        ),
        None
    );
    // Selection accepts the home itself; the chain walk then refuses it as
    // not strictly below H, and the record names nothing.
    let (_s, home) = scratch();
    let premise = premise();
    let groups = BTreeSet::new();
    let volume = any_volume;
    let policy = ProjectChainPolicy::new(Some(&premise), &volume, &groups);
    let mut record = UpwardRecord::default();
    let mut ledger = WorkLedger::new();
    let result = ledger.scope(|work| {
        admit_project_root_for_analysis(
            &home,
            uid(),
            &home,
            None,
            None,
            LocalCarrierPolicy::NonInteractive,
            &policy,
            &mut record,
            work,
        )
    });
    let Err(WorkFailure::Operation(refusal)) = result else {
        panic!("{result:?}")
    };
    assert!(matches!(
        refusal,
        ProjectAdmissionRefusal::Chain(ProjectChainRefusal::OutsideHome)
    ));
    assert_eq!(record.walked.len(), 1);
    assert!(record.refused.is_none());
    assert_eq!(record.discovery_refusal(&refusal, false), None);
    let named = UpwardRecord {
        refused: Some(home.clone()),
        ..UpwardRecord::default()
    };
    assert_eq!(
        named.discovery_refusal(&missing(), true),
        Some((
            DiscoveryRefusal::ExplicitPathInvalid,
            "ABSENT",
            home.as_path()
        ))
    );
}
