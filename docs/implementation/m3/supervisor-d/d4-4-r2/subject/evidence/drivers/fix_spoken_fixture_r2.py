from pathlib import Path
import os
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
p=Path('crates/host/tests/factory_fixture.rs');s=p.read_text();a='if output.write_all(&write_frame(&reply).unwrap()).is_err() {';assert s.count(a)==1;s=s.replace(a,'if output.write_all(&write_frame(&reply).unwrap()).and_then(|()| output.flush()).is_err() {');p.write_text(s)
p=Path('crates/host/src/launch_recheck_tests.rs');s=p.read_text();s=s.replace('fn compiled_factory_peer() -> Vec<u8> {','fn compiled_factory_peer() -> (Vec<u8>, PathBuf) {')
s=s.replace('    bytes\n}\n\n#[test]\nfn actual_factory_spawned_peer_substitutions','    (bytes, PathBuf::from(record["evidenceDirectory"].as_str().unwrap()))\n}\n\n#[test]\nfn actual_factory_spawned_peer_substitutions',1)
s=s.replace('let binary = compiled_factory_peer();','let (binary, evidence) = compiled_factory_peer();',1)
a=s.index('            assert_eq!(settlement.first_cause()') if '            assert_eq!(settlement.first_cause()' in s else s.index('            assert_eq!(\n                settlement.first_cause()')
b=s.index('            let observed:',a);e=s.index('            assert_eq!(observed["sourceBytes"]',b)
assertions=s[a:b];observation=s[b:e]
s=s[:a]+observation+'''            fs::write(evidence.join(format!("{mode}.json")), serde_json::to_vec_pretty(&serde_json::json!({
                "mode":mode, "firstCause":format!("{:?}",settlement.first_cause()),
                "ownerRoute":format!("{:?}",settlement_route(&settlement)),
                "sourceReads":reads.get(), "peer":observed,
            })).unwrap()).unwrap();
'''+assertions+s[e:];p.write_text(s)
print('Fixed explicit peer stdout flush and added per-mode retained child observations before verdict assertions.')
