from pathlib import Path
import os
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
p=Path('crates/host/src/launch_recheck_tests.rs')
s=p.read_text();assert 'actual_factory_spawned_peer_substitutions' not in s
s+=r'''
/// The lane builds the registered harness-free first-party target, pins its
/// bytes, then writes this sidecar beside the host test executable. This
/// cannot point to a repository member or unpinned executable silently.
fn compiled_factory_peer() -> Vec<u8> {
    let path = std::env::current_exe().unwrap().parent().unwrap().join("factory_fixture.json");
    let record: serde_json::Value = serde_json::from_slice(&fs::read(path).expect("lane must build and pin factory_fixture first")).unwrap();
    let binary = Path::new(record["path"].as_str().unwrap());
    let bytes = fs::read(binary).unwrap();
    assert_eq!(digest_hex(&raw_sha256(&bytes)), record["sha256"].as_str().unwrap());
    bytes
}

#[test]
fn actual_factory_spawned_peer_substitutions_refuse_before_source_or_analyze() {
    use opensip_components::{control_protocol::RefusalFamily as RF, supervisor::{Cause, Limits, Supervision, records::{OwnerRoute, settlement_route}}};
    use opensip_components::provider_protocol::{rust3::Rust3Participant, table::{Protocol, Table}};
    let binary = compiled_factory_peer();
    for (mode, expected) in [
        ("stable", Cause::ControlRefusal(RF::Rf3)),
        ("manifest", Cause::ControlRefusal(RF::Rf3)),
        ("tuple", Cause::ControlRefusal(RF::Rf4)),
        ("effect", Cause::ControlRefusal(RF::Rf6)),
        ("identity", Cause::ProviderProtocol),
        ("tokens", Cause::ProviderProtocol),
    ] {
        let fixture = Fixture::with_provider(&binary, mode);
        let root = fixture.tree_path();
        let provider = root.join("provider");
        let bindings = bindings();
        let selection = selected(&fixture);
        let hash = digest_hex(&raw_sha256(&binary));
        let members = members(&provider, &root, &hash);
        let (codec, identity, caps) = wire_fixture::rust();
        let authority = Authorities {
            selection: &selection, capabilities: &caps, entrypoint: "entrypoint", members: &members,
            identity: IdentityAuthority::Rust { expected_identity: &identity },
        };
        fixture.opened(|trees| {
            let prepared = WorkLedger::snapshot_profile().scope(|work| {
                prepare_session(SessionInput {
                    selection: selection.clone(), provider: codec, launch: launch(&provider, &root),
                    memory_budget_bytes: Limits::RELEASE.resident_memory,
                }, trees, &bindings, &authority, work).map_err(WorkFailure::Operation)
            }).unwrap();
            assert_eq!(prepared.session.launch.spec().executable(), provider);
            let Provider::Rust { sender } = prepared.provider else { panic!("Rust peer") };
            let table = Table::load(Protocol::Rust3).unwrap();
            let reads = Rc::new(Cell::new(0));
            let participant = Rust3Participant::from_sender(&table, sender, Box::new(NoSource(reads.clone()))).unwrap();
            let mut supervision = Supervision::prepare(prepared.session, participant).unwrap();
            let mut scratch = opensip_platform::ScratchRoot::create_in(File::open(&fixture.root).unwrap().into()).unwrap();
            // The operation's trees remain borrowed and alive until the
            // actual child has been supervised through its settlement.
            supervision.run(&mut scratch).unwrap();
            let settlement = supervision.take_settlement().unwrap();
            assert_eq!(settlement.first_cause(), expected, "{mode}: {settlement:?}");
            assert_eq!(settlement_route(&settlement), OwnerRoute::ProviderProtocol, "{mode}");
            assert_eq!(reads.get(), 0, "{mode}: immutable Source must never be consulted");
            let observed: serde_json::Value = serde_json::from_slice(&fs::read(fixture.root.join("peer-observation.json")).expect("actual child observation")).unwrap();
            assert_eq!(observed["sourceBytes"], 0, "{mode}: {observed}");
            assert_eq!(observed["analyze"], 0, "{mode}: {observed}");
            let frames = observed["providerReceived"].as_array().unwrap();
            assert!(frames.iter().all(|name| {
                let name = name.as_str().unwrap();
                !name.starts_with("Snapshot") && !name.starts_with("DependencySource") && name != "Analyze"
            }), "{mode}: {observed}");
            assert!(observed["controlSent"].as_array().unwrap().contains(&serde_json::json!("helloAck")), "{mode}: {observed}");
            if matches!(mode, "identity" | "tokens") {
                assert!(frames.contains(&serde_json::json!("Hello")), "{mode}: real provider Hello must precede the deliberate reply");
            }
        });
    }
}
'''
p.write_text(s)
print('Added actual factory/CI tree/supervisor/real Rust3 participant substitution controls, six modes.')
