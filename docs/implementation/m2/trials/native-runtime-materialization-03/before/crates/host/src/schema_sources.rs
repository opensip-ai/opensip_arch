//! Host-owned exact raw schema sources. No runtime path lookup or ambient I/O.
use opensip_identity::{RegisteredSchemas, SchemaAdmissionError};
const SOURCES: &[&[u8]] = &[
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/dispatch-v1.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/enumeration-plan-v1.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/execution-inputs-v1.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/fact-batch-v3.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/framework-recognition-plan-v1.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/incoming-search-v1.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/occupancy-v1.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/handshake-v1.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/startup-v1.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/relation-payload-v2.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/subject-inventory-v1.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/target-attribution-v2.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/control-v3.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/evaluator-emission-plan-v1.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/identity-v3.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/import-source-context-v1.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/native-v2.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/policy-v2.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/configuration-disclosure-v1.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/explicit-history-panel-v1.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/explicit-history-v1.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/common-v1.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/baseline-v2.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/envelope-v3.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/envelope-v4.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/command-envelope-v7.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/inventory-v3.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/inventory-v4.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/command-inventory-v6.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/common-v3.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/common-v4.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/comparison-v2.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/detector-v1.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/graph-v3.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/graph-query-v4.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/invocation-v3.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/invocation-v5.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/policy-test-v2.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/repair-v2.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/report-v1.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/review-v2.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/sarif-v2.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/imported-v1.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/metadata-v1.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/policy-v1.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/policy-test-v1.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/presentation-catalog-v1.schema.json"
    )),
    include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../schemas/sources/test-execution-v1.schema.json"
    )),
];
/// Compile the selected shape registry. This does not admit semantic evidence.
pub fn embedded_schema_registry() -> Result<RegisteredSchemas, SchemaAdmissionError> {
    RegisteredSchemas::from_sources(SOURCES)
}
#[cfg(test)]
mod tests {
    use super::*;
    use opensip_identity::{
        JsonValue, SchemaAdmissionError as AdmissionError, SchemaError, raw_sha256,
    };
    fn sources() -> Vec<Vec<u8>> {
        SOURCES.iter().map(|raw| raw.to_vec()).collect()
    }
    fn build(sources: &[Vec<u8>]) -> Result<RegisteredSchemas, AdmissionError> {
        let refs: Vec<_> = sources.iter().map(Vec::as_slice).collect();
        RegisteredSchemas::from_sources(&refs)
    }
    const ID: &str = "urn:opensip:product-v1:workflows:metadata:1";
    #[test]
    fn complete_raw_registry_is_owned_and_selected_by_full_document_hash() {
        let mut supplied = sources();
        let registry = build(&supplied).unwrap();
        let row = RegisteredSchemas::source_requirements()
            .iter()
            .position(|p| p.schema_id() == ID)
            .unwrap();
        let expected = raw_sha256(&supplied[row]);
        for raw in &mut supplied {
            raw.fill(0);
        }
        drop(supplied);
        let handle = registry.schema(ID, "/$defs/HostRelease").unwrap();
        assert_eq!(handle.document_sha256(), expected);
        assert_eq!(handle.schema_id(), ID);
        assert_eq!(handle.selector(), "/$defs/HostRelease");
        let shape = handle
            .admit_json(br#""1.2.3-rc.1+build.01""#, 100_000)
            .unwrap();
        assert!(matches!(shape.value(),JsonValue::String(v) if v=="1.2.3-rc.1+build.01"));
        assert_eq!(shape.schema().document_sha256(), expected);
        let value = shape.into_value();
        assert!(matches!(value, JsonValue::String(_)));
    }
    #[test]
    fn missing_extra_reordered_changed_and_truncated_sources_refuse() {
        let originals = sources();
        assert!(matches!(
            build(&originals[..originals.len() - 1]),
            Err(AdmissionError::SourceSet)
        ));
        let mut altered = originals.clone();
        altered.push(originals[0].clone());
        assert!(matches!(build(&altered), Err(AdmissionError::SourceSet)));
        let mut altered = originals.clone();
        altered.swap(0, 1);
        assert!(matches!(build(&altered), Err(AdmissionError::SourceBytes)));
        let mut altered = originals.clone();
        altered.last_mut().unwrap()[0] = b' ';
        assert!(matches!(build(&altered), Err(AdmissionError::SourceBytes)));
        let mut altered = originals;
        altered.last_mut().unwrap().pop();
        assert!(matches!(build(&altered), Err(AdmissionError::SourceBytes)));
    }
    #[test]
    fn selectors_do_not_fallback_and_validation_failure_kinds_remain_distinct() {
        let registry = build(&sources()).unwrap();
        assert!(matches!(
            registry.schema("urn:opensip:product-v1:workflows:metadata:999", ""),
            Err(AdmissionError::SourceSet)
        ));
        assert!(matches!(
            registry.schema(ID, "/$defs/Missing"),
            Err(AdmissionError::Schema(SchemaError::UnselectedEntry))
        ));
        assert!(matches!(
            registry.schema(ID, "#/$defs/HostRelease"),
            Err(AdmissionError::Schema(SchemaError::UnselectedEntry))
        ));
        assert!(matches!(
            registry
                .schema(ID, "/$defs/HostRelease")
                .unwrap()
                .admit_json(br#""01.2.3""#, 100_000),
            Err(AdmissionError::Mismatch)
        ));
        assert!(matches!(
            registry
                .schema(ID, "/$defs/HostRelease")
                .unwrap()
                .admit_json(br#""1.2.3""#, 0),
            Err(AdmissionError::Schema(SchemaError::Limit))
        ));
        assert!(matches!(
            registry
                .schema(ID, "/$defs/HostRelease")
                .unwrap()
                .admit_json(b"1.0", 100_000),
            Err(AdmissionError::Schema(SchemaError::Json))
        ));
    }

    #[test]
    fn aliases_require_exact_current_bytes_and_report_root_requires_its_own_codec() {
        let registry = build(&sources()).unwrap();
        for (document, id) in [
            (
                "native/native-evidence.schemas.v2.json",
                "urn:opensip:product-v1:native:evidence-schemas:v2",
            ),
            (
                "workflows/schemas/policy-document.v2.schema.json",
                "urn:opensip:product-v1:policy-document:2",
            ),
            (
                "foundation/framework-recognition-plan.schema.v1.json",
                "opensip.product.framework-recognition-plan.1",
            ),
        ] {
            let digest = RegisteredSchemas::source_requirements()
                .iter()
                .find(|p| p.schema_id() == id)
                .unwrap()
                .sha256();
            assert_eq!(
                registry
                    .record_schema(document, digest, "")
                    .unwrap()
                    .document_sha256(),
                digest
            );
            assert!(matches!(
                registry.record_schema(document, [0; 32], ""),
                Err(AdmissionError::SourceBytes)
            ));
        }
        assert!(matches!(
            registry.record_schema("unknown", [0; 32], ""),
            Err(AdmissionError::SourceSet)
        ));
        assert!(matches!(
            registry.schema(
                "urn:opensip:product-v1:workflows:evaluator3:report-projection:1",
                ""
            ),
            Err(AdmissionError::UnsupportedCodec)
        ));
        assert!(
            registry
                .schema(
                    "urn:opensip:product-v1:workflows:evaluator3:report-projection:1",
                    "/$defs/ReportViewId"
                )
                .is_ok()
        );
    }

    #[test]
    fn candidate_refusals_preserve_json_shape_and_budget_distinctions() {
        use opensip_identity::{CandidateError, IdentityCandidate, IdentityDomain};
        let registry = embedded_schema_registry().unwrap();
        for raw in [
            b"{\"schemaVersion\":2,\"schemaVersion\":2}".as_slice(),
            b"1.0",
            b"-0",
            b"\xff",
        ] {
            assert!(matches!(
                IdentityCandidate::from_json(&registry, IdentityDomain::Fact, raw, 1_000_000),
                Err(CandidateError::Schema(AdmissionError::Schema(
                    SchemaError::Json
                )))
            ));
        }
        assert!(matches!(
            IdentityCandidate::from_json(&registry, IdentityDomain::Fact, b"{}", 1_000_000),
            Err(CandidateError::Schema(AdmissionError::Mismatch))
        ));
        assert!(matches!(
            IdentityCandidate::from_json(&registry, IdentityDomain::Fact, b"{}", 0),
            Err(CandidateError::Schema(AdmissionError::Schema(
                SchemaError::Limit
            )))
        ));
        assert_eq!(IdentityDomain::parse("fact2"), Err(CandidateError::Domain));
    }
}
