from pathlib import Path
import os,json
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
f=Path(__file__).parent/'provider-spoken-r2';p=f/'report.json';raw=p.read_bytes();(f/'report-runtime-observation.json').write_bytes(raw);j=json.loads(raw);j.update(allPassed=False,testScopeValid=False,standing='INVALIDATED first-party buffered stdout harness attempt. Controlled child stops can themselves induce ProviderProtocol on EOF; runtime pass is not an identity/token substitution witness. Original runtime result retained separately.',originalRuntimeReport='report-runtime-observation.json',diagnosis='controlled-fixture-interruptions.json');p.write_text(json.dumps(j,indent=2)+'\n')
p=Path('crates/host/tests/factory_fixture.rs');s=p.read_text();s=s.replace('"identity", "tokens"','"identity", "tokens", "baseline"',1).replace('"providerReceived":[],','"providerReceived":[],"providerSent":[],',1)
a=s.index('            if output.write_all(&write_frame(&reply).unwrap())');b=s.index('\n        }',a)
s=s[:a]+'''            let bytes = write_frame(&reply).unwrap();
            if output.write_all(&bytes).and_then(|()| output.flush()).is_err() { return; }
            let mut record = audit.lock().unwrap();
            record.value["providerSent"].as_array_mut().unwrap().push(json!({"frameType":"HelloAck","wireHex":bytes.iter().map(|b|format!("{b:02x}")).collect::<String>()}));
            record.persist();
''' +s[b:]
# Baseline admits the unmodified HelloAck and waits for actual OpenUniverse,
# then deliberately refuses at the next boundary with a malformed payload.
x='''        } else if name == "OpenUniverse" && mode == "baseline" {
            let reply=Value::Map(vec![("protocolMajor".into(),Value::Unsigned(3)),("direction".into(),Value::Text("worker-to-host".into())),("sequence".into(),Value::Unsigned(1)),("frameType".into(),Value::Text("UniverseAccepted".into())),("payload".into(),Value::Map(vec![]))]);
            let bytes=write_frame(&reply).unwrap();
            if output.write_all(&bytes).and_then(|()|output.flush()).is_err(){return;}
'''
a=s.rindex('\n        }\n    }\n}');s=s[:a]+ '\n'+x+s[a:];p.write_text(s)
p=Path('crates/host/src/launch_recheck_tests.rs');s=p.read_text();s=s.replace('("tokens", Cause::ProviderProtocol),','("tokens", Cause::ProviderProtocol),\n        ("baseline", Cause::ProviderProtocol),',1)
a=s.index('            if matches!(mode, "identity" | "tokens") {');b=s.index('\n        });',a)
s=s[:a]+'''            if matches!(mode, "identity" | "tokens" | "baseline") {
                use opensip_components::provider_protocol::{read_frame, cbor::{Profile, Value}};
                assert!(frames.contains(&serde_json::json!("Hello")));
                let replies = observed["providerSent"].as_array().unwrap();
                assert_eq!(replies.len(), 1, "{mode}: a positive flushed HelloAck witness is required");
                let hex = replies[0]["wireHex"].as_str().unwrap();
                let bytes: Vec<u8> = (0..hex.len()).step_by(2).map(|i|u8::from_str_radix(&hex[i..i+2],16).unwrap()).collect();
                let reply = read_frame(&mut bytes.as_slice(), Profile::Rust3, 32, None).unwrap().unwrap();
                fn field<'a>(value: &'a Value, key: &str)->&'a Value {
                    let Value::Map(rows)=value else {panic!("map")};
                    &rows.iter().find(|(name,_)|name==key).unwrap().1
                }
                assert_eq!(field(reply.value(), "frameType"), &Value::Text("HelloAck".into()));
                let payload=field(reply.value(),"payload");
                if mode=="identity" {assert_eq!(field(payload,"providerBuildId"),&Value::Text("wrong-provider".into()));}
                if mode=="tokens" {assert_eq!(field(payload,"capabilities"),&Value::Array(vec![]));}
                assert_eq!(frames.contains(&serde_json::json!("OpenUniverse")), mode=="baseline", "{mode}: unmodified Ack alone must unlock the next metadata frame");
            }
''' +s[b:];p.write_text(s)
print('Invalidated externally stopped r2 attempt; require flushed reply bytes and a valid-HelloAck baseline progression witness.')
