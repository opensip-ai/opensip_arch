from pathlib import Path
import os,subprocess,json,hashlib
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
W=Path('/Users/sb/code/opensip-ai/opensip-native-owner-patterns-takeover');F=Path(__file__).parent
p=W/'crates/host/src/schema_sources.rs'
text=p.read_text();assert 'mod native_owner_registered_tests' not in text
text += r'''

/// The complete pinned source set exercises the selected owner through its
/// existing registered selectors. Shape admission is not path semantics.
#[cfg(test)]
mod native_owner_registered_tests {
    use opensip_identity::{RegisteredSchemas, SchemaAdmissionError, raw_sha256};

    #[test]
    fn native_owner_registered_paths_use_complete_input_and_exact_alias_pins() {
        let registry = super::embedded_schema_registry().unwrap();
        assert_eq!(RegisteredSchemas::source_requirements().len(), 52);
        for (id, selector, alias) in [
            ("urn:opensip:product-v1:native:evidence-schemas:v2", "/$defs/CanonicalPath", Some("native/native-evidence.schemas.v2.json")),
            ("opensip.product.relation-payload.2", "/$defs/CanonicalPath", Some("foundation/relation-payload-schemas.v2.json")),
            ("opensip.product.occupancy-companion.1", "/$defs/LogicalPath", None),
        ] {
            let handle = registry.schema(id, selector).unwrap();
            let pin = RegisteredSchemas::source_requirements().iter().find(|p| p.schema_id() == id).unwrap();
            assert_eq!(handle.document_sha256(), pin.sha256());
            for path in ["src/a.ts", "a/..\n", "a/..\r", "a/..\u{2028}", "a/..\u{2029}", "a\n/ok"] {
                let raw = serde_json::to_vec(path).unwrap();
                assert!(registry.schema(id, selector).unwrap().admit_json(&raw, 1_000_000).is_ok(), "{id} {path:?}");
                if let Some(alias) = alias {
                    assert!(registry.record_schema(alias, pin.sha256(), selector).unwrap().admit_json(&raw, 1_000_000).is_ok());
                }
            }
            for path in [".", "..", "/a", "a/.", "a/..", "a/../b", "a\n/../b", "a\r/../b", "a\u{2028}/../b", "a\u{2029}/../b"] {
                let raw = serde_json::to_vec(path).unwrap();
                assert!(matches!(registry.schema(id, selector).unwrap().admit_json(&raw, 1_000_000), Err(SchemaAdmissionError::Mismatch)), "{id} {path:?}");
            }
            if let Some(alias) = alias {
                assert!(matches!(registry.record_schema(alias, [0;32], selector), Err(SchemaAdmissionError::SourceBytes)));
            }
        }
    }

    #[test]
    fn native_owner_registered_guard_refuses_predecessor_patterns_and_same_length_substitution() {
        let requirements = RegisteredSchemas::source_requirements();
        for id in ["urn:opensip:product-v1:native:evidence-schemas:v2", "opensip.product.relation-payload.2"] {
            let index = requirements.iter().position(|p| p.schema_id()==id).unwrap();
            let original = super::SOURCES[index];
            assert_eq!(raw_sha256(original), requirements[index].sha256());
            for raw in [
                String::from_utf8(original.to_vec()).unwrap().replace(r"(?![\s\S]*", r"(?!.*").into_bytes(),
                { let mut value=original.to_vec(); let byte=value.iter_mut().find(|b| **b==b' ').unwrap(); *byte=b'\t'; value },
            ] {
                assert_ne!(raw, original);
                let mut supplied=super::SOURCES.to_vec(); supplied[index]=raw.as_slice();
                assert!(matches!(RegisteredSchemas::from_sources(&supplied), Err(SchemaAdmissionError::SourceBytes)));
            }
        }
    }
}
'''
p.write_text(text)
p=W/'crates/components/src/provider_protocol/ts2_send_tests.rs';text=p.read_text();assert 'fn native_owner_registered_startup' not in text
text+=r'''

/// The actual request builder reaches the native owner through the registered
/// startup schema. Keep line terminators as wire data; do not repair the frame.
#[test]
fn native_owner_registered_startup_preserves_non_dot_segments_and_refuses_late_dot_segments() {
    for path in ["a/..\n", "a/..\r", "a/..\u{2028}", "a/..\u{2029}"] {
        let mut p = plan();
        let J::Object(universe) = &mut p.universe else { unreachable!() };
        let J::Object(resolved) = universe.get_mut("resolvedInputs").unwrap() else { unreachable!() };
        for key in ["jsRootFiles", "programRootFiles"] {
            resolved.insert(key.to_owned(), J::Array(vec![J::String(path.to_owned())]));
        }
        let request = Ts2Request::build(&p).unwrap();
        assert_eq!(carrier::to_json(get(request.open_universe(), "universe")).unwrap(), p.universe);
    }
    for path in ["a/..", "a/../b", "a\n/../b", "a\r/../b", "a\u{2028}/../b", "a\u{2029}/../b"] {
        let mut p = plan();
        let J::Object(universe) = &mut p.universe else { unreachable!() };
        let J::Object(resolved) = universe.get_mut("resolvedInputs").unwrap() else { unreachable!() };
        resolved.insert("programRootFiles".to_owned(), J::Array(vec![J::String(path.to_owned())]));
        assert!(matches!(Ts2Request::build(&p), Err(PlanRefusal::HostInvariant(_))), "{path:?}");
    }
}
'''
p.write_text(text)
for rel in ['crates/host/src/schema_sources.rs','crates/components/src/provider_protocol/ts2_send_tests.rs']:
 subprocess.run(['/opt/homebrew/Cellar/rust/1.95.0/bin/rustfmt','--edition','2024',str(W/rel)],check=True)
print('added complete registered source/alias/guard and actual startup consumer controls')
