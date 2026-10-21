from pathlib import Path
import os
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
p=Path('crates/host/src/launch_recheck_ts2_fixture.rs');s=p.read_text().replace('use opensip_identity::JsonValue as J;','use opensip_identity::{JsonValue as J, digest_hex as hex};');p.write_text(s)
p=Path('crates/host/tests/factory_fixture.rs');s=p.read_text();s=s.replace('//! Accepts only the factory\'s closed Rust3 launch argv.','//! Accepts only the factory\'s closed Rust3 or TS2 launch argv.');s=s.replace('struct Audit {','#[path = "support/factory_ts2.rs"]\nmod ts2_descriptors;\nstruct Audit {',1)
a=s.index('    if args.len() != 6');b=s.index('    let fixture = root',a)
s=s[:a]+'''    let (profile, major, root) = if args.len()==6 && args[1]=="--protocol-stdio-v2" && args[2]=="--toolchain-root" && args[4]=="--scratch-root" {
        (Profile::Rust3,3,PathBuf::from(&args[3]))
    } else if args.len()==5 && args[1]=="--no-addons" && args[2]=="--no-global-search-paths" && args[3].to_str().is_some_and(|s|s.starts_with("--openssl-config=")) {
        let provider = PathBuf::from(&args[4]);
        let root=provider.parent().unwrap().to_path_buf();
        assert_eq!(args[3],format!("--openssl-config={}",root.join("openssl.cnf").display()).as_str());
        assert!(fs::read(root.join("openssl.cnf")).unwrap().is_empty());
        (Profile::Ts2,2,root)
    } else {return;};
''' +s[b:];s=s.replace('"identity", "tokens", "baseline"','"identity", "tokens", "baseline", "providerdigest", "runtimedigest"',1)
s=s.replace('read_frame(&mut input, Profile::Rust3, 32, None)','read_frame(&mut input, profile, 32, None)',1)
a=s.index('            let Value::Map(mut fields)');b=s.index('            fields.push((',a)
s=s[:a]+'''            let mut fields = if major==3 {
                let Value::Map(fields)=field(payload,"expectedIdentity").clone()else{panic!("identity map")};fields
            } else {
                let mut fields:Vec<_>=ts2_descriptors::provider().into_iter().chain(ts2_descriptors::runtime()).collect();
                fields.push(("providerDescriptorSha256".into(),field(payload,"expectedProviderDescriptorSha256").clone()));
                fields.push(("runtimeDescriptorSha256".into(),field(payload,"expectedRuntimeDescriptorSha256").clone()));
                fields
            };
''' +s[b:]
a=s.index('            let reply = Value::Map(vec![',a);b=s.index('            let bytes = write_frame',a)
s=s[:a]+'''            for (mode_name, key) in [("providerdigest","providerDescriptorSha256"),("runtimedigest","runtimeDescriptorSha256")] {
                if mode==mode_name {fields.iter_mut().find(|(k,_)|k==key).unwrap().1=Value::Text("0".repeat(64));}
            }
            let mut envelope=vec![("protocolMajor".into(),Value::Unsigned(major)),("sequence".into(),Value::Unsigned(0)),("frameType".into(),Value::Text("HelloAck".into())),("payload".into(),Value::Map(fields))];
            if major==3 {envelope.push(("direction".into(),Value::Text("worker-to-host".into())));}
            let reply=Value::Map(envelope);
''' +s[b:]
a=s.index('            let reply = Value::Map(vec![',a);b=s.index('            let bytes = write_frame',a)
s=s[:a]+'''            let mut envelope=vec![("protocolMajor".into(),Value::Unsigned(major)),("sequence".into(),Value::Unsigned(1)),("frameType".into(),Value::Text("UniverseAccepted".into())),("payload".into(),Value::Map(vec![]))];
            if major==3 {envelope.push(("direction".into(),Value::Text("worker-to-host".into())));}
            let reply=Value::Map(envelope);
''' +s[b:];p.write_text(s)
p=Path('crates/host/src/launch_recheck_tests.rs');s=p.read_text();s+='''
impl opensip_components::provider_protocol::ts2::SnapshotSource for NoSource {
    fn read(&mut self,_:&str,_:u64,_:usize)->std::io::Result<Vec<u8>> {
        self.0.set(self.0.get()+1);Err(std::io::Error::other("source disclosure before acknowledgment"))
    }
}
'''
# Reuse the complete existing physical/supervisor witness assertions, changing
# the independent TS2 construction and both relevant descriptor digest modes.
a=s.index('#[test]\nfn actual_factory_spawned_peer_substitutions_refuse_before_source_or_analyze()');new=s[a:s.index('\nimpl opensip_components::provider_protocol::ts2::SnapshotSource',a)]
new=new.replace('fn actual_factory_spawned_peer_substitutions_refuse_before_source_or_analyze()', 'fn actual_ts2_factory_spawned_peer_substitutions_refuse_before_source_or_analyze()')
new=new.replace('rust3::Rust3Participant','ts2::Ts2Participant').replace('("tokens", Cause::ProviderProtocol),','("tokens", Cause::ProviderProtocol),\n        ("providerdigest", Cause::ProviderProtocol),\n        ("runtimedigest", Cause::ProviderProtocol),',1)
a=new.index('        let fixture = Fixture::with_provider');b=new.index('        fixture.opened',a)
new=new[:a]+'''        const JS:&[u8]=b"// first-party inert D4 provider fixture\\n";
        let fixture = Fixture::with_files(JS,Some(&binary),mode);
        let root=fixture.tree_path();let provider=root.join("provider");let node=root.join("node");let config=root.join("openssl.cnf");
        let bindings=[Binding{name:"entrypoint",tree:0,request:MemberRequest::Entrypoint},Binding{name:"node",tree:0,request:MemberRequest::File("node")},Binding{name:"openssl",tree:0,request:MemberRequest::File("openssl.cnf")},Binding{name:"provider",tree:0,request:MemberRequest::File("provider")}];
        let mut selection=selected(&fixture);selection.tuple.role_subprotocol="typescript-semantic".into();selection.tuple.subprotocol_version=2;
        let js_hash=digest_hex(&raw_sha256(JS));let node_hash=digest_hex(&raw_sha256(&binary));let config_hash=digest_hex(&raw_sha256(b""));
        let members=[
            MemberAuthority{member:NamedMember{name:"entrypoint",launch_path:&provider},kind:MemberKind::File,closure_member:"provider",file_sha256:Some(&js_hash)},
            MemberAuthority{member:NamedMember{name:"node",launch_path:&node},kind:MemberKind::File,closure_member:"node",file_sha256:Some(&node_hash)},
            MemberAuthority{member:NamedMember{name:"openssl",launch_path:&config},kind:MemberKind::File,closure_member:"openssl.cnf",file_sha256:Some(&config_hash)},
            MemberAuthority{member:NamedMember{name:"provider",launch_path:&provider},kind:MemberKind::File,closure_member:"provider",file_sha256:Some(&js_hash)},
        ];
        let input=ts2_fixture::typescript();
        let authority=Authorities{selection:&selection,capabilities:&input.capabilities,entrypoint:"entrypoint",members:&members,identity:IdentityAuthority::TypeScript{provider_sha256:&input.provider_digest,runtime_sha256:&input.runtime_digest,provider_fields:&input.provider_fields,runtime_fields:&input.runtime_fields}};
''' +new[b:]
new=new.replace('provider: codec,','provider: input.provider,',1).replace('launch: launch(&provider, &root),','launch: Launch::TypeScript{entrypoint:NamedMember{name:"entrypoint",launch_path:&provider},node:NamedMember{name:"node",launch_path:&node},openssl_config:NamedMember{name:"openssl",launch_path:&config},provider:NamedMember{name:"provider",launch_path:&provider},broker_context:"D4-first-party-fixture"},',1)
new=new.replace('assert_eq!(prepared.session.launch.spec().executable(), provider);','assert_eq!(prepared.session.launch.spec().executable(), node);\n            assert_eq!(prepared.session.launch.recheck().sha256,node_hash);',1).replace('let Provider::Rust { sender }','let Provider::TypeScript { sender, context }',1).replace('panic!("Rust peer")','panic!("TS2 peer")',1).replace('Table::load(Protocol::Rust3)','Table::load(Protocol::Ts2)',1).replace('Rust3Participant::from_sender(&table, sender, Box::new(NoSource(reads.clone())))','Ts2Participant::from_sender(&table, context, sender, Box::new(NoSource(reads.clone())))',1)
new=new.replace('evidence.join(format!("{mode}.json"))','evidence.join(format!("ts2-{mode}.json"))',1).replace('matches!(mode, "identity" | "tokens" | "baseline")','matches!(mode, "identity" | "tokens" | "baseline" | "providerdigest" | "runtimedigest")',1).replace('Profile::Rust3, 32','Profile::Ts2, 32',1)
a=new.index('                assert_eq!(\n                    frames.contains(&serde_json::json!("OpenUniverse"))');new=new[:a]+'''                if mode=="providerdigest" {assert_eq!(field(payload,"providerDescriptorSha256"),&Value::Text("0".repeat(64)));}
                if mode=="runtimedigest" {assert_eq!(field(payload,"runtimeDescriptorSha256"),&Value::Text("0".repeat(64)));}
''' +new[a:]
s+= '\n'+new;p.write_text(s)
print('Added nine actual TS2 factory/retained-tree/TestFixture/supervisor/real participant scenarios and dual-profile peer handling.')
