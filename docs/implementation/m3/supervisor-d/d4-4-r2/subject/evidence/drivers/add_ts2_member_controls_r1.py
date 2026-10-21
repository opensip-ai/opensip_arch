from pathlib import Path
import os
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
p=Path('crates/host/src/launch_recheck_tests.rs');s=p.read_text();a=s.index('        const JS:',s.index('fn actual_ts2_factory_spawned'));b=s.index('        fixture.opened',a);setup=s[a:b].replace('mode);','"adapter");')
# The same independently projected three launch members are installed before
# opening the capability. Each corruption occurs AFTER it has been opened.
addition='''
#[test]
fn actual_ts2_factory_rechecks_each_distinct_native_file_before_launch() {
    let (binary, _) = compiled_factory_peer();
    for target in ["node", "openssl.cnf", "provider"] {
'''+setup+'''        fixture.opened(|trees| {
            fixture.change(|_| {
                let path=root.join(target);
                let original=fs::metadata(&path).unwrap().mode() & 0o777;
                fs::set_permissions(&path,fs::Permissions::from_mode(0o600)).unwrap();
                let mut bytes=fs::read(&path).unwrap();
                if bytes.is_empty(){bytes.push(1)}else{bytes[0]^=1;}
                fs::write(&path,bytes).unwrap();
                fs::set_permissions(&path,fs::Permissions::from_mode(original)).unwrap();
            });
            let result=WorkLedger::snapshot_profile().scope(|work|{
                prepare_session(SessionInput{
                    selection:selection.clone(),provider:input.provider,
                    launch:Launch::TypeScript{entrypoint:NamedMember{name:"entrypoint",launch_path:&provider},node:NamedMember{name:"node",launch_path:&node},openssl_config:NamedMember{name:"openssl",launch_path:&config},provider:NamedMember{name:"provider",launch_path:&provider},broker_context:"D4-first-party-fixture"},
                    memory_budget_bytes:1<<30,
                },trees,&bindings,&authority,work).map_err(WorkFailure::Operation)
            });
            let refusal=match result{Err(WorkFailure::Operation(error))=>error,_=>panic!("{target}: a changed member must refuse before any launch escapes")};
            let expected=if target=="openssl.cnf"{CorruptCause::Length}else{CorruptCause::Digest};
            assert_eq!(refusal.route(),opensip_components::supervisor::records::OwnerRoute::ClosureBytesCorrupt);
            assert!(matches!(refusal,FactoryRefusal::Recheck(RecheckFailure::Corrupt(actual))if actual==expected),"{target}");
            assert!(!fixture.root.join("peer-observation.json").exists());
        });
    }
}
'''
s+=addition;p.write_text(s)
print('Added post-open physical corruption controls for node, empty OpenSSL config, and provider through the actual TS2 factory.')
