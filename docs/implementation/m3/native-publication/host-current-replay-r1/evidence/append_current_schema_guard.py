from pathlib import Path
W=Path('/Users/sb/code/opensip-ai/opensip-host-current-corpus');P=W.parent/'opensip';p=W/'crates/host/src/schema_sources.rs';assert p.read_bytes()==(P/'crates/host/src/schema_sources.rs').read_bytes()
s=r'''

#[cfg(test)]
mod current_replay_schema_tests {
    use opensip_identity::{JsonValue, SchemaAdmissionError as AdmissionError, parse_json, raw_sha256};

    #[test]
    fn current_replay_selects_exact_native_bytes_and_refuses_the_retained_m1_document() {
        let registry = crate::embedded_schema_registry().unwrap();
        let current = include_bytes!("../../../schemas/sources/native-v2.schema.json");
        let document = "native/native-evidence.schemas.v2.json";
        assert_eq!(
            registry
                .record_schema(document, raw_sha256(current), "")
                .unwrap()
                .document_sha256(),
            raw_sha256(current)
        );
        let fixture = parse_json(include_bytes!("../tests/fixtures/replay-fixtures.json")).unwrap();
        let JsonValue::Object(root) = fixture else { panic!("fixture object") };
        let JsonValue::Object(pool) = &root["blobPool"] else { panic!("fixture blob pool") };
        let old = "e5834d37aebd96d77d352975878da349033f8633ecbd83322ad0fbea461f7773";
        let retained = pool.values().find_map(|row| {
            let JsonValue::Object(row) = row else { return None };
            let JsonValue::String(digest) = &row["digest"] else { return None };
            if digest != old { return None; }
            let JsonValue::String(hex) = &row["hex"] else { panic!("fixture hex") };
            Some(hex.as_bytes().chunks_exact(2).map(|pair| {
                u8::from_str_radix(std::str::from_utf8(pair).unwrap(), 16).unwrap()
            }).collect::<Vec<_>>())
        }).expect("exact retained M1 native schema");
        assert_ne!(retained.as_slice(), current);
        assert!(matches!(
            registry.record_schema(document, raw_sha256(&retained), ""),
            Err(AdmissionError::SourceBytes)
        ));
    }
}
'''
p.write_text(p.read_text()+s)
