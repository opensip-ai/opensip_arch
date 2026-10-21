from pathlib import Path
import os
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
p=Path('crates/host/src/launch_recheck_tests.rs')
s=p.read_text()
a=s.index('#[test]\nfn actual_native_factory_recheck_corruption_never_returns_a_launch()')
b=s.index('\nstruct Boundary',a)
s=s[:a]+'''#[test]
fn actual_native_factory_preserves_corruption_and_read_io_routes() {
    // Each observation crosses the real installed-store adapter AND the
    // factory. An adapter-only error is not evidence for the factory route.
    for case in 0..6 {
        let fixture = Fixture::new();
        let root = fixture.tree_path();
        let provider = root.join("provider");
        let bindings = bindings();
        let selection = selected(&fixture);
        let hash = digest_hex(&raw_sha256(DATA));
        let members = members(&provider, &root, &hash);
        let (codec, identity, caps) = wire_fixture::rust();
        let authority = Authorities {
            selection: &selection,
            capabilities: &caps,
            entrypoint: "entrypoint",
            members: &members,
            identity: IdentityAuthority::Rust { expected_identity: &identity },
        };
        fixture.opened(|trees| {
            if case < 5 {
                fixture.change(|path| match case {
                    0 | 1 => {
                        fs::set_permissions(path, fs::Permissions::from_mode(0o600)).unwrap();
                        let mut bytes = DATA.to_vec();
                        if case == 0 { bytes[0] ^= 1; } else { bytes.pop(); }
                        fs::write(path, bytes).unwrap();
                        fs::set_permissions(path, fs::Permissions::from_mode(0o500)).unwrap();
                    }
                    2 => fs::set_permissions(path, fs::Permissions::from_mode(0o400)).unwrap(),
                    3 => { fs::remove_file(path).unwrap(); fs::create_dir(path).unwrap(); }
                    4 => fs::remove_file(path).unwrap(),
                    _ => unreachable!(),
                });
            }
            let read_guard = (case == 5).then(read_fixture::fail_next_read);
            let result = WorkLedger::snapshot_profile().scope(|work| {
                prepare_session(
                    SessionInput {
                        selection: selection.clone(), provider: codec,
                        launch: launch(&provider, &root), memory_budget_bytes: 1 << 30,
                    }, trees, &bindings, &authority, work,
                ).map_err(WorkFailure::Operation)
            });
            // Err is the only returned value: no launch escapes this boundary.
            let refusal = match result {
                Err(WorkFailure::Operation(refusal)) => refusal,
                _ => panic!("native refusal must survive factory composition, case {case}"),
            };
            use opensip_components::supervisor::records::OwnerRoute;
            if case == 5 {
                assert_eq!(refusal.route(), OwnerRoute::HostIo);
                assert!(matches!(refusal, FactoryRefusal::Recheck(RecheckFailure::Io { call: "read", error }) if error.kind() == std::io::ErrorKind::Other));
                assert!(read_guard.as_ref().unwrap().was_triggered());
            } else {
                let expected = [CorruptCause::Digest, CorruptCause::Length, CorruptCause::Mode, CorruptCause::Type, CorruptCause::Absent][case];
                assert_eq!(refusal.route(), OwnerRoute::ClosureBytesCorrupt);
                assert!(matches!(refusal, FactoryRefusal::Recheck(RecheckFailure::Corrupt(actual)) if actual == expected));
            }
        });
    }
}
''' +s[b:]
p.write_text(s)
print('Extended actual native factory controls to all five physical corruption causes and injected read-I/O, with owner-route assertions.')
