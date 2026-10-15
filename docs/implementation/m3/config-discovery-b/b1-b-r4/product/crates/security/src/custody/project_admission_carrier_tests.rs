// M3-B unit B1-b (X2 r9 item 3a; plan r3 section 2): the analysis path's
// configuration carriers, their absence observations and recheck, the
// legacy path's unchanged charges, the optional user-global carrier, FW-01
// and the hostile-environment control. Scratch installations only.

const PROJECT_JSON: &[u8] = b"{\"schemaVersion\":2,\"discovery\":{\"workspaceRoots\":[\"src\"]}}";
const LOCAL_JSON: &[u8] = b"{\"schemaVersion\":2,\"ui\":{\"color\":\"never\"}}";

fn analysis(
    fixture: &ReadFixture,
    project: &Path,
    local: LocalCarrierPolicy,
) -> (
    crate::custody::installation_read::ReadSession,
    Result<CarrierAdmission, ProjectSessionRefusal>,
) {
    let session = fixture.session(None).unwrap();
    let carriers = session.admit_project_carriers(project, None, &BTreeSet::new(), local);
    (session, carriers)
}
fn carrier_row<T: std::fmt::Debug>(
    result: Result<T, ProjectSessionRefusal>,
) -> ProjectAdmissionRow {
    match result {
        Err(ProjectSessionRefusal::Project(WorkFailure::Operation(refusal))) => refusal.row(),
        other => panic!("expected a project refusal, got {other:?}"),
    }
}
fn local_carrier(project: &Path, bytes: &[u8]) {
    let opensip = project.join(MARKER_DIRECTORY);
    if !opensip.exists() {
        directory(&opensip, 0o700);
    }
    file(&opensip.join(LOCAL_CONFIG_FILE), bytes, 0o644);
}

#[test]
fn the_analysis_path_captures_both_carriers_from_their_judged_descriptors() {
    churned(|| {
        let fixture = ReadFixture::new("b1b-capture");
        let project = fixture_project(&fixture);
        file(&project.join(CONFIG_FILE), PROJECT_JSON, 0o644);
        local_carrier(&project, LOCAL_JSON);
        let (session, carriers) = analysis(&fixture, &project, LocalCarrierPolicy::Interactive);
        let carriers = carriers.unwrap();
        let project_carrier = carriers.carriers().project().unwrap();
        assert_eq!(project_carrier.relative(), "opensip.json");
        assert_eq!(project_carrier.bytes(), PROJECT_JSON);
        let local = carriers.carriers().local().unwrap();
        assert_eq!(local.relative(), ".opensip/local.json");
        assert_eq!(local.bytes(), LOCAL_JSON);
        assert_eq!(carriers.selected().mode(), SelectionMode::Config);
        let admission = session
            .complete_project_admission(carriers, &BTreeSet::new())
            .unwrap();
        assert_eq!(
            admission.classification(),
            &Classification::FirstUseCandidate
        );
        assert_eq!(
            admission.carriers().unwrap().project().unwrap().bytes(),
            PROJECT_JSON
        );
    });
}

#[test]
fn ci_never_looks_up_the_local_carrier_and_hostile_local_bytes_never_refuse() {
    churned(|| {
        let fixture = ReadFixture::new("b1b-ci");
        let project = fixture_project(&fixture);
        let opensip = project.join(MARKER_DIRECTORY);
        directory(&opensip, 0o700);
        // A symlink, then an oversized file: each refuses interactively only.
        std::os::unix::fs::symlink("/etc/hosts", opensip.join(LOCAL_CONFIG_FILE)).unwrap();
        let (session, carriers) = analysis(&fixture, &project, LocalCarrierPolicy::NonInteractive);
        let carriers = carriers.unwrap();
        assert!(carriers.carriers().local().is_none());
        assert!(carriers.carriers().project().is_none());
        session
            .complete_project_admission(carriers, &BTreeSet::new())
            .unwrap();
        drop(session);
        let (_, interactive) = analysis(&fixture, &project, LocalCarrierPolicy::Interactive);
        assert_eq!(
            carrier_row(interactive),
            ProjectAdmissionRow::ConfigCustody("local-symlink")
        );
        fs::remove_file(opensip.join(LOCAL_CONFIG_FILE)).unwrap();
        file(
            &opensip.join(LOCAL_CONFIG_FILE),
            &vec![b' '; 4 * 1024 * 1024 + 1],
            0o644,
        );
        let (_, ci) = analysis(&fixture, &project, LocalCarrierPolicy::NonInteractive);
        assert!(ci.unwrap().carriers().local().is_none());
        let (_, interactive) = analysis(&fixture, &project, LocalCarrierPolicy::Interactive);
        assert_eq!(
            carrier_row(interactive),
            ProjectAdmissionRow::ConfigCustody("local-custody")
        );
    });
}

#[test]
fn an_appearance_after_an_absent_observation_refuses_on_the_recheck() {
    churned(|| {
        // opensip.json absent at capture, then created: every mode.
        for local in [
            LocalCarrierPolicy::Interactive,
            LocalCarrierPolicy::NonInteractive,
        ] {
            let fixture = ReadFixture::new("b1b-appear-config");
            let project = fixture_project(&fixture);
            let (session, carriers) = analysis(&fixture, &project, local);
            let carriers = carriers.unwrap();
            file(&project.join(CONFIG_FILE), PROJECT_JSON, 0o644);
            assert_eq!(
                carrier_row(session.complete_project_admission(carriers, &BTreeSet::new())),
                ProjectAdmissionRow::ConfigCustody("opensip.json:appeared"),
                "{local:?}"
            );
        }
        // `.opensip` absent (interactive), then created holding `local.json`
        // but no marker: the ambiguous marker observation is not relied on.
        let fixture = ReadFixture::new("b1b-appear-directory");
        let project = fixture_project(&fixture);
        let (session, carriers) = analysis(&fixture, &project, LocalCarrierPolicy::Interactive);
        let carriers = carriers.unwrap();
        local_carrier(&project, LOCAL_JSON);
        assert_eq!(
            carrier_row(session.complete_project_admission(carriers, &BTreeSet::new())),
            ProjectAdmissionRow::ConfigCustody(".opensip:appeared")
        );
        // `local.json` absent under a present `.opensip` (interactive).
        let fixture = ReadFixture::new("b1b-appear-local");
        let project = fixture_project(&fixture);
        directory(&project.join(MARKER_DIRECTORY), 0o700);
        let (session, carriers) = analysis(&fixture, &project, LocalCarrierPolicy::Interactive);
        let carriers = carriers.unwrap();
        file(
            &project.join(MARKER_DIRECTORY).join(LOCAL_CONFIG_FILE),
            LOCAL_JSON,
            0o644,
        );
        assert_eq!(
            carrier_row(session.complete_project_admission(carriers, &BTreeSet::new())),
            ProjectAdmissionRow::ConfigCustody("local.json:appeared")
        );
    });
}

#[test]
fn in_ci_a_custody_valid_opensip_appearing_is_never_a_local_refusal_but_marker_custody_still_is() {
    churned(|| {
        // A custody-valid `.opensip` with no marker and a `local.json`,
        // appearing after a CI admission: no refusal attributable to it.
        let fixture = ReadFixture::new("b1b-ci-appear");
        let project = fixture_project(&fixture);
        let (session, carriers) = analysis(&fixture, &project, LocalCarrierPolicy::NonInteractive);
        let carriers = carriers.unwrap();
        local_carrier(&project, LOCAL_JSON);
        let admission = session
            .complete_project_admission(carriers, &BTreeSet::new())
            .unwrap();
        assert!(admission.carriers().unwrap().local().is_none());
        // Contrast: a `.opensip` with wrong custody still refuses through the
        // marker's own observation, in CI too.
        let fixture = ReadFixture::new("b1b-ci-marker");
        let project = fixture_project(&fixture);
        let opensip = project.join(MARKER_DIRECTORY);
        directory(&opensip, 0o777);
        let (_, carriers) = analysis(&fixture, &project, LocalCarrierPolicy::NonInteractive);
        assert_eq!(
            carrier_row(carriers),
            ProjectAdmissionRow::RootCustody("marker-directory-custody")
        );
    });
}

#[test]
fn a_carrier_changed_after_capture_refuses_on_the_recheck() {
    churned(|| {
        let fixture = ReadFixture::new("b1b-changed");
        let project = fixture_project(&fixture);
        file(&project.join(CONFIG_FILE), PROJECT_JSON, 0o644);
        local_carrier(&project, LOCAL_JSON);
        let (session, carriers) = analysis(&fixture, &project, LocalCarrierPolicy::Interactive);
        let carriers = carriers.unwrap();
        // Rewritten with other bytes: a different full sample.
        file(&project.join(CONFIG_FILE), b"{\"schemaVersion\":2}", 0o644);
        assert_eq!(
            carrier_row(session.complete_project_admission(carriers, &BTreeSet::new())),
            ProjectAdmissionRow::RequiredFilesChanged
        );
        let fixture = ReadFixture::new("b1b-changed-local");
        let project = fixture_project(&fixture);
        local_carrier(&project, LOCAL_JSON);
        let (session, carriers) = analysis(&fixture, &project, LocalCarrierPolicy::Interactive);
        let carriers = carriers.unwrap();
        fs::remove_file(project.join(MARKER_DIRECTORY).join(LOCAL_CONFIG_FILE)).unwrap();
        assert_eq!(
            carrier_row(session.complete_project_admission(carriers, &BTreeSet::new())),
            ProjectAdmissionRow::RequiredFilesChanged
        );
    });
}

#[test]
fn local_carrier_custody_refuses_config_custody_with_local_subjects() {
    churned(|| {
        let fixture = ReadFixture::new("b1b-local-custody");
        let project = fixture_project(&fixture);
        let opensip = project.join(MARKER_DIRECTORY);
        directory(&opensip, 0o700);
        // Others-writable local carrier.
        file(&opensip.join(LOCAL_CONFIG_FILE), LOCAL_JSON, 0o666);
        let (_, carriers) = analysis(&fixture, &project, LocalCarrierPolicy::Interactive);
        assert_eq!(
            carrier_row(carriers),
            ProjectAdmissionRow::ConfigCustody("local-custody")
        );
        // A directory where the file belongs.
        fs::remove_file(opensip.join(LOCAL_CONFIG_FILE)).unwrap();
        directory(&opensip.join(LOCAL_CONFIG_FILE), 0o700);
        let (_, carriers) = analysis(&fixture, &project, LocalCarrierPolicy::Interactive);
        assert_eq!(
            carrier_row(carriers),
            ProjectAdmissionRow::ConfigCustody("local-not-a-regular-file")
        );
    });
}

/// The legacy admission, on a fresh ledger, and what it spent.
fn legacy_spend(
    fixture: &ReadFixture,
    project: &Path,
) -> (ProjectRootAdmission, opensip_platform::WorkCost) {
    let premise = premise();
    let groups = BTreeSet::new();
    let volume = any_volume;
    let policy = ProjectChainPolicy::new(Some(&premise), &volume, &groups);
    let installation =
        RetainedDirectoryPath::open_project_root(&fixture.installation, 256).unwrap();
    let mut ledger = WorkLedger::new();
    let judged = ledger
        .scope(|work| {
            let file = installation.directory().open_regular(REGISTRY).unwrap();
            let sample = opensip_platform::capture_descriptor_acl_accounted(&file, work)?;
            Ok::<_, WorkFailure<opensip_platform::DescriptorAclCaptureError>>(RequiredFile::new(
                REGISTRY,
                sample.metadata().clone(),
            ))
        })
        .unwrap();
    let mut ledger = WorkLedger::new();
    let admission = ledger
        .scope(|work| {
            admit_project_root(
                &fixture.home,
                uid(),
                project,
                None,
                installation.directory(),
                &judged,
                &policy,
                work,
            )
        })
        .unwrap();
    (admission, ledger.used())
}

#[test]
fn the_legacy_admission_reads_no_carrier_bytes_and_never_probes_local() {
    churned(|| {
        let fixture = ReadFixture::new("b1b-legacy");
        let project = fixture_project(&fixture);
        file(&project.join(CONFIG_FILE), b"{}", 0o644);
        let (small_admission, small) = legacy_spend(&fixture, &project);
        assert!(small_admission.carriers().is_none());
        // A larger `opensip.json` (the bytes are never read) and a present
        // `.opensip/local.json` (never looked up) spend exactly the same.
        file(&project.join(CONFIG_FILE), &vec![b' '; 1024 * 1024], 0o644);
        let (_, large) = legacy_spend(&fixture, &project);
        assert_eq!(small, large);
        let opensip = project.join(MARKER_DIRECTORY);
        directory(&opensip, 0o700);
        let (_, with_directory) = legacy_spend(&fixture, &project);
        file(&opensip.join(LOCAL_CONFIG_FILE), LOCAL_JSON, 0o644);
        let (_, with_local) = legacy_spend(&fixture, &project);
        assert_eq!(with_directory, with_local);
    });
}

#[test]
fn the_user_global_carrier_is_optional_rechecked_and_never_created() {
    churned(|| {
        let fixture = ReadFixture::new("b1b-global");
        // No `I/host`: no layer, recorded absent, and still absent.
        let session = fixture.session(None).unwrap();
        assert!(
            session
                .capture_optional(&["host"], "settings.json", 4 * 1024 * 1024)
                .unwrap()
                .is_none()
        );
        assert!(!fixture.installation.join("host").exists());
        session.recheck().unwrap();
        // It appears: the recheck refuses.
        fixture.write("host/settings.json", b"{\"schemaVersion\":2}");
        assert!(session.recheck().is_err());
        // `I/host` present, the file absent, then created.
        let fixture = ReadFixture::new("b1b-global-leaf");
        fixture.write("host/keep", b"x");
        let session = fixture.session(None).unwrap();
        assert!(
            session
                .capture_optional(&["host"], "settings.json", 4 * 1024 * 1024)
                .unwrap()
                .is_none()
        );
        fixture.write("host/settings.json", b"{\"schemaVersion\":2}");
        assert!(session.recheck().is_err());
        // Present: exactly a capture.
        let fixture = ReadFixture::new("b1b-global-present");
        fixture.write(
            "host/settings.json",
            b"{\"schemaVersion\":2,\"ui\":{\"color\":\"always\"}}",
        );
        let session = fixture.session(None).unwrap();
        let captured = session
            .capture_optional(&["host"], "settings.json", 4 * 1024 * 1024)
            .unwrap()
            .unwrap();
        assert_eq!(
            captured.raw(),
            b"{\"schemaVersion\":2,\"ui\":{\"color\":\"always\"}}"
        );
        session.recheck().unwrap();
    });
}

/// Every path under `root` with its kind, size and modification time.
fn tree(root: &Path) -> Vec<(PathBuf, bool, u64, i64, i64)> {
    let mut out = Vec::new();
    let mut stack = vec![root.to_path_buf()];
    while let Some(path) = stack.pop() {
        let meta = fs::symlink_metadata(&path).unwrap();
        out.push((
            path.clone(),
            meta.is_dir(),
            meta.len(),
            meta.mtime(),
            meta.mtime_nsec(),
        ));
        if meta.is_dir() {
            for entry in fs::read_dir(&path).unwrap() {
                stack.push(entry.unwrap().path());
            }
        }
    }
    out.sort();
    out
}

#[test]
fn fw01_capture_and_admission_write_nothing() {
    churned(|| {
        let fixture = ReadFixture::new("b1b-fw01");
        let project = fixture_project(&fixture);
        file(&project.join(CONFIG_FILE), PROJECT_JSON, 0o644);
        local_carrier(&project, LOCAL_JSON);
        let before = (tree(&project), tree(&fixture.installation));
        let (session, carriers) = analysis(&fixture, &project, LocalCarrierPolicy::Interactive);
        let admission = session
            .complete_project_admission(carriers.unwrap(), &BTreeSet::new())
            .unwrap();
        session
            .capture_optional(&["host"], "settings.json", 4 * 1024 * 1024)
            .unwrap();
        drop(admission);
        drop(session);
        assert_eq!(before.0, tree(&project));
        // The installation's own lifecycle files may be touched by the
        // session's fence; the project tree and I's member set must not grow.
        let after: Vec<PathBuf> = tree(&fixture.installation)
            .into_iter()
            .map(|row| row.0)
            .collect();
        let before_paths: Vec<PathBuf> = before.1.into_iter().map(|row| row.0).collect();
        assert_eq!(before_paths, after);
    });
}

/// A fresh test policy, as the selection tests build it.
macro_rules! test_policy {
    ($premise:ident, $groups:ident, $volume:ident, $policy:ident) => {
        let $premise = premise();
        let $groups = BTreeSet::new();
        let $volume = any_volume;
        let $policy = ProjectChainPolicy::new(Some(&$premise), &$volume, &$groups);
    };
}

#[test]
fn a_change_between_the_judgment_and_the_read_refuses_and_is_never_rebaselined() {
    // Codex B1B-R1-RF-01: the capture binds to the sample the custody
    // judgment passed on. A rewrite or a custody change interposed between
    // selection's judgment and the read refuses.
    for change in ["rewrite", "mode"] {
        let (_scratch, home) = scratch();
        let project = home.join("project");
        directory(&project, 0o755);
        file(&project.join(CONFIG_FILE), PROJECT_JSON, 0o644);
        test_policy!(premise, groups, volume, policy);
        let mut ledger = WorkLedger::new();
        let (selected, retained) = ledger
            .scope(|work| super::select(&project, None, &home, uid(), &policy, true, work))
            .unwrap();
        assert!(selected.config());
        let (file_handle, judged) = retained.unwrap();
        match change {
            "rewrite" => {
                fs::write(project.join(CONFIG_FILE), b"{\"schemaVersion\":2,\"x\":1}").unwrap()
            }
            _ => fs::set_permissions(project.join(CONFIG_FILE), fs::Permissions::from_mode(0o666))
                .unwrap(),
        }
        assert!(
            matches!(
                ledger.scope(|work| capture_carrier(&file_handle, &judged, CONFIG_FILE, work)),
                Err(WorkFailure::Operation(ProjectAdmissionRefusal::Changed))
            ),
            "{change}"
        );
    }
    // Unchanged: the judged bytes are captured.
    let (_scratch, home) = scratch();
    let project = home.join("project");
    directory(&project, 0o755);
    file(&project.join(CONFIG_FILE), PROJECT_JSON, 0o644);
    test_policy!(premise, groups, volume, policy);
    let mut ledger = WorkLedger::new();
    let (_, retained) = ledger
        .scope(|work| super::select(&project, None, &home, uid(), &policy, true, work))
        .unwrap();
    let (file_handle, judged) = retained.unwrap();
    let carrier = ledger
        .scope(|work| capture_carrier(&file_handle, &judged, CONFIG_FILE, work))
        .unwrap();
    assert_eq!(carrier.bytes(), PROJECT_JSON);
    // The local carrier: the same binding to its own judgment.
    for change in ["rewrite", "mode"] {
        let (_scratch, home) = scratch();
        let project = home.join("project");
        directory(&project, 0o755);
        local_carrier(&project, LOCAL_JSON);
        test_policy!(premise, groups, volume, policy);
        let root = RetainedDirectoryPath::open_project_root(&project, 256).unwrap();
        let mut ledger = WorkLedger::new();
        let directory_handle = ledger
            .scope(|work| local_directory(root.directory(), uid(), &policy, work))
            .unwrap()
            .unwrap();
        let (file_handle, judged) = ledger
            .scope(|work| judge_local(&directory_handle, uid(), &policy, work))
            .unwrap()
            .unwrap();
        let local = project.join(MARKER_DIRECTORY).join(LOCAL_CONFIG_FILE);
        match change {
            "rewrite" => fs::write(&local, b"{\"schemaVersion\":2}").unwrap(),
            _ => fs::set_permissions(&local, fs::Permissions::from_mode(0o666)).unwrap(),
        }
        assert!(
            matches!(
                ledger.scope(|work| capture_carrier(
                    &file_handle,
                    &judged,
                    ".opensip/local.json",
                    work
                )),
                Err(WorkFailure::Operation(ProjectAdmissionRefusal::Changed))
            ),
            "local {change}"
        );
    }
}

#[test]
fn optional_absence_is_observed_and_rechecked_under_judged_parents() {
    // Codex B1B-R1-RF-02. A wrong-custody existing `I/host` refuses, as a
    // capture would; it is never a vacuous absence.
    churned(|| {
        let fixture = ReadFixture::new("b1b-global-custody");
        fixture.write("host/keep", b"x");
        fs::set_permissions(
            fixture.installation.join("host"),
            fs::Permissions::from_mode(0o750),
        )
        .unwrap();
        let session = fixture.session(None).unwrap();
        assert!(
            session
                .capture_optional(&["host"], "settings.json", 4 * 1024 * 1024)
                .is_err()
        );
    });
    // After an absence under a judged `I/host`: a custody change, a
    // replacement and a detachment of the parent each refuse on recheck.
    for change in ["mode", "replace", "detach"] {
        churned(|| {
            let fixture = ReadFixture::new("b1b-global-parent");
            fixture.write("host/keep", b"x");
            let session = fixture.session(None).unwrap();
            assert!(
                session
                    .capture_optional(&["host"], "settings.json", 4 * 1024 * 1024)
                    .unwrap()
                    .is_none()
            );
            let host = fixture.installation.join("host");
            match change {
                "mode" => fs::set_permissions(&host, fs::Permissions::from_mode(0o750)).unwrap(),
                "replace" => {
                    fs::rename(&host, fixture.installation.join("host-old")).unwrap();
                    fixture.write("host/keep", b"x");
                }
                _ => fs::remove_dir_all(&host).unwrap(),
            }
            assert!(session.recheck().is_err(), "{change}");
        });
    }
}

/// The analysis path's first phase on a fresh ledger, and what it spent.
fn phase_one_spend(
    fixture: &ReadFixture,
    project: &Path,
    local: LocalCarrierPolicy,
) -> opensip_platform::WorkCost {
    test_policy!(premise, groups, volume, policy);
    let mut ledger = WorkLedger::new();
    ledger
        .scope(|work| {
            admit_project_root_for_analysis(
                &fixture.home,
                uid(),
                project,
                None,
                local,
                &policy,
                work,
            )
        })
        .unwrap();
    ledger.used()
}

#[test]
fn ci_makes_no_local_lookup_by_the_ledger_count() {
    // Every lookup is charged, so the ledger is the counter: in CI a present
    // `local.json` costs nothing; interactively it is looked up and read.
    churned(|| {
        let fixture = ReadFixture::new("b1b-ci-count");
        let project = fixture_project(&fixture);
        directory(&project.join(MARKER_DIRECTORY), 0o700);
        let without = phase_one_spend(&fixture, &project, LocalCarrierPolicy::NonInteractive);
        file(
            &project.join(MARKER_DIRECTORY).join(LOCAL_CONFIG_FILE),
            LOCAL_JSON,
            0o644,
        );
        let with = phase_one_spend(&fixture, &project, LocalCarrierPolicy::NonInteractive);
        assert_eq!(without, with);
        let interactive = phase_one_spend(&fixture, &project, LocalCarrierPolicy::Interactive);
        assert_ne!(interactive, with);
    });
}

#[test]
fn ci_never_looks_up_the_local_carrier_by_count() {
    // Codex B1B-R2-RF-02: the local-carrier lookups counted directly. A
    // charged lookup whose result is ignored would show here (the lane's
    // `ci-ignored-local-lookup` mutation).
    churned(|| {
        let fixture = ReadFixture::new("b1b-ci-lookups");
        let project = fixture_project(&fixture);
        local_carrier(&project, LOCAL_JSON);
        LOCAL_LOOKUPS.with(|count| count.set(0));
        let (session, carriers) = analysis(&fixture, &project, LocalCarrierPolicy::NonInteractive);
        session
            .complete_project_admission(carriers.unwrap(), &BTreeSet::new())
            .unwrap();
        drop(session);
        assert_eq!(LOCAL_LOOKUPS.with(std::cell::Cell::get), 0);
        let (session, carriers) = analysis(&fixture, &project, LocalCarrierPolicy::Interactive);
        session
            .complete_project_admission(carriers.unwrap(), &BTreeSet::new())
            .unwrap();
        // Capture, then the recheck under the fence.
        assert_eq!(LOCAL_LOOKUPS.with(std::cell::Cell::get), 2);
    });
}

#[test]
fn the_first_phase_reads_no_registry_and_has_no_effect() {
    churned(|| {
        let fixture = ReadFixture::new("b1b-order");
        let project = fixture_project(&fixture);
        file(&project.join(CONFIG_FILE), PROJECT_JSON, 0o644);
        // The registry's size does not change the first phase's charges, so
        // it reads no registry; item 5 is the second phase's.
        let small = phase_one_spend(&fixture, &project, LocalCarrierPolicy::Interactive);
        let rows = (1..=40)
            .map(|i| {
                entry(
                    i,
                    "ACTIVE",
                    format!("/elsewhere/{i}").as_bytes(),
                    &incarnation(1000 + u64::from(i)),
                )
            })
            .collect();
        fixture.write(REGISTRY, &document(rows));
        let large = phase_one_spend(&fixture, &project, LocalCarrierPolicy::Interactive);
        assert_eq!(small, large);
        // A refused pack: the first phase, then nothing. No member of I is
        // created or changed, and the fence is released for the next session.
        let before = tree(&fixture.installation);
        let session = fixture.session(None).unwrap();
        let carriers = session
            .admit_project_carriers(
                &project,
                None,
                &BTreeSet::new(),
                LocalCarrierPolicy::Interactive,
            )
            .unwrap();
        drop(carriers);
        drop(session);
        let after = tree(&fixture.installation);
        let unchanged = |rows: &[(PathBuf, bool, u64, i64, i64)]| -> Vec<(PathBuf, u64)> {
            rows.iter()
                .filter(|row| !row.1 && !row.0.ends_with("lifecycle.fence"))
                .map(|row| (row.0.clone(), row.2))
                .collect()
        };
        assert_eq!(unchanged(&before), unchanged(&after));
        assert_eq!(
            before.iter().map(|row| row.0.clone()).collect::<Vec<_>>(),
            after.iter().map(|row| row.0.clone()).collect::<Vec<_>>()
        );
        fixture.session(None).unwrap();
    });
}

/// Children of the hostile-environment controls (MB item 9; LD-B1B-4,
/// LD-B1B-5). Ignored: run only by the parents below, which invoke them
/// explicitly with a cleared environment, then with a hostile one.
#[test]
#[ignore = "child of the hostile-environment control"]
fn b1b_environment_child_capture() {
    churned(|| {
        let fixture = ReadFixture::new("b1b-env-child");
        let project = fixture_project(&fixture);
        file(&project.join(CONFIG_FILE), PROJECT_JSON, 0o644);
        local_carrier(&project, LOCAL_JSON);
        fixture.write(
            "host/settings.json",
            b"{\"schemaVersion\":2,\"ui\":{\"color\":\"always\"}}",
        );
        let (session, carriers) = analysis(&fixture, &project, LocalCarrierPolicy::Interactive);
        let admission = session
            .complete_project_admission(carriers.unwrap(), &BTreeSet::new())
            .unwrap();
        let global = session
            .capture_optional(&["host"], "settings.json", 4 * 1024 * 1024)
            .unwrap()
            .unwrap();
        let carriers = admission.carriers().unwrap();
        for carrier in [carriers.project().unwrap(), carriers.local().unwrap()] {
            println!(
                "B1B-ENV:{}:{}:{}",
                carrier.relative(),
                carrier.bytes().len(),
                hex(&opensip_identity::raw_sha256(carrier.bytes()))
            );
        }
        println!(
            "B1B-ENV:host/settings.json:{}:{}",
            global.raw().len(),
            hex(&opensip_identity::raw_sha256(global.raw()))
        );
        println!("B1B-ENV:classification:{:?}", admission.classification());
    });
}
#[test]
#[ignore = "child of the permitted Git environment refusal control"]
fn b1b_environment_child_tracking() {
    churned(|| {
        let fixture = ReadFixture::new("b1b-env-tracking");
        let project = fixture_project(&fixture);
        let session = fixture.session(None).unwrap();
        let admission = session
            .admit_project_root(&project, None, &BTreeSet::new())
            .unwrap();
        match session.observe_project_tracking(&admission, &BTreeSet::new()) {
            Ok(_) => println!("B1B-TRACK:ok"),
            Err(refusal) => println!("B1B-TRACK:refused:{refusal:?}"),
        }
    });
}

/// Run one ignored child with a cleared environment (only the private
/// TMPDIR kept, which the scratch tree needs), or with hostile values too.
fn child_lines(name: &str, marker: &str, hostile: bool) -> Vec<String> {
    let mut command = std::process::Command::new(std::env::current_exe().unwrap());
    command
        .args([
            "--ignored",
            "--exact",
            name,
            "--nocapture",
            "--test-threads=1",
        ])
        .env_clear()
        .env("TMPDIR", std::env::temp_dir());
    if hostile {
        command
            .env("HOME", "/nonexistent/opensip-hostile-home")
            .env("PATH", "/nonexistent/opensip-hostile-bin")
            .env("CI", "1")
            .env("TERM", "dumb")
            .env("NO_COLOR", "1")
            .env("XDG_CONFIG_HOME", "/nonexistent/opensip-hostile-xdg")
            .env("XDG_DATA_HOME", "/nonexistent/opensip-hostile-xdg-data")
            .env("XDG_CACHE_HOME", "/nonexistent/opensip-hostile-xdg-cache");
    }
    let output = command.output().unwrap();
    assert!(
        output.status.success(),
        "{}",
        String::from_utf8_lossy(&output.stderr)
    );
    String::from_utf8(output.stdout)
        .unwrap()
        .lines()
        .filter_map(|line| line.find(marker).map(|at| line[at..].to_owned()))
        .collect()
}

#[test]
fn the_carrier_capture_is_identical_under_a_hostile_environment() {
    let name = "custody::project_admission::tests::b1b_environment_child_capture";
    let clean = child_lines(name, "B1B-ENV:", false);
    assert_eq!(clean.len(), 4, "{clean:?}");
    assert_eq!(clean, child_lines(name, "B1B-ENV:", true));
}

#[test]
fn the_only_environment_effect_is_the_permitted_git_refusal() {
    // X2's refusal-only check reads the environment before any repository
    // discovery: with a cleared environment tracking proceeds; with a hostile
    // HOME or XDG_CONFIG_HOME it refuses, and that is its only effect.
    let name = "custody::project_admission::tests::b1b_environment_child_tracking";
    let clean = child_lines(name, "B1B-TRACK:", false);
    assert_eq!(clean, ["B1B-TRACK:ok"]);
    let hostile = child_lines(name, "B1B-TRACK:", true);
    assert_eq!(hostile.len(), 1);
    assert!(hostile[0].contains("environment-"), "{hostile:?}");
}
