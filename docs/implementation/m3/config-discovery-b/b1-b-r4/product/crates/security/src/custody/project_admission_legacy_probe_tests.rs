// M3-B unit B1-b (Codex B1B-R1-RF-04): the legacy admission's charges, for a
// comparison against the base product. It uses only APIs that exist at the
// base, so the check lane runs this same file there and here and requires
// equal lines. Ignored: run only by the lane, explicitly.
#[test]
#[ignore = "probe of the legacy admission's charges, run by the check lane"]
fn b1b_legacy_spend_probe() {
    churned(|| {
        let fixture = ReadFixture::new("b1b-legacy-probe");
        let project = fixture_project(&fixture);
        let premise = premise();
        let groups = BTreeSet::new();
        let volume = any_volume;
        let policy = ProjectChainPolicy::new(Some(&premise), &volume, &groups);
        let installation =
            RetainedDirectoryPath::open_project_root(&fixture.installation, 256).unwrap();
        let spend = |label: &str| {
            let mut ledger = WorkLedger::new();
            let judged = ledger
                .scope(|work| {
                    let file = installation.directory().open_regular(REGISTRY).unwrap();
                    let sample = opensip_platform::capture_descriptor_acl_accounted(&file, work)?;
                    Ok::<_, WorkFailure<opensip_platform::DescriptorAclCaptureError>>(
                        RequiredFile::new(REGISTRY, sample.metadata().clone()),
                    )
                })
                .unwrap();
            let mut ledger = WorkLedger::new();
            let admission = ledger
                .scope(|work| {
                    admit_project_root(
                        &fixture.home,
                        uid(),
                        &project,
                        None,
                        installation.directory(),
                        &judged,
                        &policy,
                        work,
                    )
                })
                .unwrap();
            let used = ledger.used();
            println!(
                "B1B-LEGACY:{label}:{}:{}:{}:{:?}",
                used.objects,
                used.edges,
                used.bytes,
                admission.classification()
            );
        };
        spend("no-config");
        file(&project.join("opensip.json"), b"{}", 0o644);
        spend("config-small");
        file(
            &project.join("opensip.json"),
            &vec![b' '; 1024 * 1024],
            0o644,
        );
        spend("config-large");
        let opensip = project.join(".opensip");
        directory(&opensip, 0o700);
        spend("opensip-directory");
        file(&opensip.join("local.json"), b"{}", 0o644);
        spend("local-present");
    });
}
