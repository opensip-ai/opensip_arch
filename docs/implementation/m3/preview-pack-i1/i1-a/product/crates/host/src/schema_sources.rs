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
    fn initialization_details_are_current_only_and_unknown_codes_still_refuse() {
        use opensip_contracts::generated::evidence::{
            Common1DomainDetailCode, Common3DomainDetailCode, Common4DomainDetailCode,
        };
        let registry = embedded_schema_registry().unwrap();
        let current = "urn:opensip:product-v1:workflows:evaluator3:common:4";
        for code in [
            "INSTALLATION.DURABILITY_NOT_CHECKED",
            "INSTALLATION.NOT_INITIALIZED",
            "CORE.NO_EMBEDDED_RELEASE",
            "INSTALLATION.ACCOUNT_REFUSED",
            "WORK.BUDGET_EXHAUSTED",
        ] {
            let raw = serde_json::to_vec(code).unwrap();
            assert!(
                registry
                    .schema(current, "/$defs/DomainDetailCode")
                    .unwrap()
                    .admit_json(&raw, 100_000)
                    .is_ok()
            );
            assert!(serde_json::from_slice::<Common4DomainDetailCode>(&raw).is_ok());
            for historical in [
                "urn:opensip:product-v1:workflows:common",
                "urn:opensip:product-v1:workflows:evaluator3:common:3",
            ] {
                assert!(matches!(
                    registry
                        .schema(historical, "/$defs/DomainDetailCode")
                        .unwrap()
                        .admit_json(&raw, 100_000),
                    Err(AdmissionError::Mismatch)
                ));
            }
            assert!(serde_json::from_slice::<Common1DomainDetailCode>(&raw).is_err());
            assert!(serde_json::from_slice::<Common3DomainDetailCode>(&raw).is_err());
        }
        let unknown = br#""INSTALLATION.UNREGISTERED""#;
        assert!(matches!(
            registry
                .schema(current, "/$defs/DomainDetailCode")
                .unwrap()
                .admit_json(unknown, 100_000),
            Err(AdmissionError::Mismatch)
        ));
        assert!(serde_json::from_slice::<Common4DomainDetailCode>(unknown).is_err());
    }
    // M3-I1 unit I1-a: the one additive operation member is admitted by the
    // current policy-document:2 and identity:v3 sources and their generated
    // enums, refused by policy-document:1, and no other spelling is admitted.
    // Evaluation still refuses the op (atoms.rs ATOM_OP) until unit I1-b2.
    #[test]
    fn cycle_representative_is_admitted_by_current_policy_and_identity_schemas_only() {
        use opensip_contracts::generated::evidence::{Policy1AtomOp, Policy2AtomOp};
        use opensip_contracts::generated::identity::{
            Identity3ProgramPredicateOperation, Identity3ProofBundlePredicateProofsItemOperation,
        };
        let registry = embedded_schema_registry().unwrap();
        let admits = |id: &str, selector: &str, raw: &str| match registry
            .schema(id, selector)
            .unwrap()
            .admit_json(raw.as_bytes(), 1_000_000)
        {
            Ok(_) => true,
            Err(AdmissionError::Mismatch) => false,
            Err(other) => panic!("{id}#{selector}: {other:?}"),
        };
        let hex = |c: char| c.to_string().repeat(64);
        let atom = |op: &str| {
            format!(
                r#"{{"op":"{op}","relation":"imports","minResolution":"resolved-target","filters":[]}}"#
            )
        };
        let program_predicate = |op: &str| {
            format!(
                r#"{{"schemaVersion":2,"ruleProgramDigest":"{}","ruleId":"module-import-cycle","predicateId":"p","operation":"{op}","nodeDigest":"{}"}}"#,
                hex('a'),
                hex('b')
            )
        };
        let proof_bundle = |op: &str| {
            format!(
                concat!(
                    r#"{{"schemaVersion":3,"planId":"plan2:{h}","executionPlanId":"exec-plan2:{h}","#,
                    r#""evaluatorClosure":"closure2:{h}","ruleProgramDigest":"{h}","evaluationInputRefs":[],"#,
                    r#""predicateProofs":[{{"ruleId":"module-import-cycle","subjectId":"subject3:{h}","#,
                    r#""predicateId":"p","operation":"{op}","inputRefs":[],"scopeIds":[],"value":"false","#,
                    r#""witnessDigest":"{h}"}}],"findingIds":[],"verdict":"pass","evaluationState":"evaluated","#,
                    r#""ruleResults":[],"waivedFindingIds":[],"executionDeficiencies":[],"executionInputsDigest":"{h}"}}"#
                ),
                h = hex('c'),
                op = op
            )
        };
        let policy2 = "urn:opensip:product-v1:policy-document:2";
        let policy1 = "urn:opensip:product-v1:workflows:policy-document";
        let identity3 = "urn:opensip:product-v1:identity:v3";
        // Controls: an existing member is admitted everywhere it was before.
        assert!(admits(policy2, "/$defs/Atom", &atom("exists")));
        assert!(admits(policy1, "/$defs/Atom", &atom("exists")));
        assert!(admits(
            identity3,
            "/$defs/program-predicate",
            &program_predicate("and")
        ));
        assert!(admits(
            identity3,
            "/$defs/proof-bundle",
            &proof_bundle("and")
        ));
        let op = "cycle-representative";
        assert!(admits(policy2, "/$defs/Atom", &atom(op)));
        assert!(admits(
            identity3,
            "/$defs/program-predicate",
            &program_predicate(op)
        ));
        assert!(admits(identity3, "/$defs/proof-bundle", &proof_bundle(op)));
        assert!(!admits(policy1, "/$defs/Atom", &atom(op)));
        let raw = serde_json::to_vec(op).unwrap();
        assert_eq!(
            serde_json::from_slice::<Policy2AtomOp>(&raw).unwrap(),
            Policy2AtomOp::CycleRepresentative
        );
        assert_eq!(
            serde_json::from_slice::<Identity3ProgramPredicateOperation>(&raw).unwrap(),
            Identity3ProgramPredicateOperation::CycleRepresentative
        );
        assert_eq!(
            serde_json::from_slice::<Identity3ProofBundlePredicateProofsItemOperation>(&raw)
                .unwrap(),
            Identity3ProofBundlePredicateProofsItemOperation::CycleRepresentative
        );
        assert!(serde_json::from_slice::<Policy1AtomOp>(&raw).is_err());
        assert_eq!(Policy2AtomOp::CycleRepresentative.to_string(), op);
        // No near spelling or case variant is admitted.
        for other in [
            "cycle_representative",
            "Cycle-Representative",
            "cycle-representatives",
            "cycle",
        ] {
            assert!(!admits(policy2, "/$defs/Atom", &atom(other)));
            assert!(!admits(
                identity3,
                "/$defs/program-predicate",
                &program_predicate(other)
            ));
            assert!(!admits(
                identity3,
                "/$defs/proof-bundle",
                &proof_bundle(other)
            ));
            let raw = serde_json::to_vec(other).unwrap();
            assert!(serde_json::from_slice::<Policy2AtomOp>(&raw).is_err());
            assert!(serde_json::from_slice::<Identity3ProgramPredicateOperation>(&raw).is_err());
            assert!(
                serde_json::from_slice::<Identity3ProofBundlePredicateProofsItemOperation>(&raw)
                    .is_err()
            );
        }
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

#[cfg(test)]
mod retained_input_tests {
    use opensip_identity::{
        IdentityCandidate, IdentityDomain, JsonValue, ObjectInput, RegisteredSchemas,
        RetainedInputError as Error, RetainedInputs, canonical_bytes, parse_json, raw_sha256,
    };
    use std::{collections::BTreeMap, string::String};
    use std::{format, vec};
    fn descriptor(raw: &str) -> JsonValue {
        parse_json(raw.as_bytes()).unwrap()
    }
    fn put(
        registry: &RegisteredSchemas,
        objects: &mut BTreeMap<String, ObjectInput>,
        domain: IdentityDomain,
        value: JsonValue,
    ) -> String {
        let raw = canonical_bytes(&value).unwrap();
        let key: String = IdentityCandidate::from_json(registry, domain, &raw, 1_000_000)
            .unwrap()
            .identifier()
            .into();
        objects.insert(
            key.clone(),
            ObjectInput {
                domain,
                descriptor: value,
            },
        );
        key
    }
    fn closure(kind: &str) -> JsonValue {
        descriptor(&format!(
            r#"{{"schemaVersion":2,"kind":"{kind}","manifestDigest":"{}","tree":[],"semanticVersion":"1.0.0","protocolMajor":3,"platform":"macos-aarch64"}}"#,
            "0".repeat(64)
        ))
    }
    fn import(producer: &str, adapter: &str) -> JsonValue {
        descriptor(&format!(
            r#"{{"schemaVersion":2,"kind":"runtime","payloadSchemaDigest":"{z}","payloadDigest":"{z}","sourceCorrespondenceDigest":"{z}","buildDigest":"{z}","producerClosure":"{producer}","adapterClosure":"{adapter}","blobs":[],"scopeDigest":"{z}","observationDigest":"{z}","completeness":"unknown","omissions":[]}}"#,
            z = "0".repeat(64)
        ))
    }
    #[test]
    fn missing_object_and_blob_are_distinct_from_changed_claimed_bytes() {
        let registry = crate::embedded_schema_registry().unwrap();
        let mut objects = BTreeMap::new();
        let mut blobs = BTreeMap::new();
        let missing = "closure2:missing";
        assert!(matches!(
            RetainedInputs::new(&registry, &objects, &blobs).object(
                missing,
                IdentityDomain::Closure,
                1_000_000
            ),
            Err(Error::MissingObject(_))
        ));
        assert!(matches!(
            RetainedInputs::new(&registry, &objects, &blobs).blob([0; 32]),
            Err(Error::MissingBlob(_))
        ));
        blobs.insert([0; 32], vec![1]);
        assert!(matches!(
            RetainedInputs::new(&registry, &objects, &blobs).blob([0; 32]),
            Err(Error::BlobDigest)
        ));
        let key = put(
            &registry,
            &mut objects,
            IdentityDomain::Closure,
            closure("provider"),
        );
        assert!(
            RetainedInputs::new(&registry, &objects, &blobs)
                .object(&key, IdentityDomain::Closure, 1_000_000)
                .is_ok()
        );
        assert!(matches!(
            RetainedInputs::new(&registry, &objects, &blobs).object(
                &key,
                IdentityDomain::Fact,
                1_000_000
            ),
            Err(Error::ObjectDomain)
        ));
        objects.get_mut(&key).unwrap().descriptor = closure("adapter");
        assert!(matches!(
            RetainedInputs::new(&registry, &objects, &blobs).object(
                &key,
                IdentityDomain::Closure,
                1_000_000
            ),
            Err(Error::ObjectIdentity)
        ));
    }
    #[test]
    fn hash_length_and_canonical_bytes_are_separate_checks() {
        let registry = crate::embedded_schema_registry().unwrap();
        let objects = BTreeMap::new();
        let mut blobs = BTreeMap::new();
        for raw in [b"{}".as_slice(), b"{ }", b"1.0", b""] {
            blobs.insert(raw_sha256(raw), raw.to_vec());
        }
        let inputs = RetainedInputs::new(&registry, &objects, &blobs);
        let blob = inputs.blob(raw_sha256(b"{}")).unwrap();
        assert_eq!(blob.bytes(), b"{}");
        assert_eq!(blob.digest(), raw_sha256(b"{}"));
        assert!(blob.require_length(2).is_ok());
        assert_eq!(blob.require_length(3), Err(Error::BlobLength));
        assert!(blob.canonical_record().is_ok());
        assert_eq!(
            inputs.blob(raw_sha256(b"{ }")).unwrap().canonical_record(),
            Err(Error::NoncanonicalRecord)
        );
        assert!(matches!(
            inputs.blob(raw_sha256(b"1.0")).unwrap().canonical_record(),
            Err(Error::Canonical(_))
        ));
        assert!(
            inputs
                .blob(raw_sha256(b""))
                .unwrap()
                .require_length(0)
                .is_ok()
        );
    }
    #[test]
    fn closure_identity_does_not_establish_its_role_or_payload_closure() {
        let registry = crate::embedded_schema_registry().unwrap();
        let mut objects = BTreeMap::new();
        let blobs = BTreeMap::new();
        let provider = put(
            &registry,
            &mut objects,
            IdentityDomain::Closure,
            closure("provider"),
        );
        let adapter = put(
            &registry,
            &mut objects,
            IdentityDomain::Closure,
            closure("adapter"),
        );
        let good = put(
            &registry,
            &mut objects,
            IdentityDomain::Import,
            import(&provider, &adapter),
        );
        let wrong = put(
            &registry,
            &mut objects,
            IdentityDomain::Import,
            import(&adapter, &provider),
        );
        let inputs = RetainedInputs::new(&registry, &objects, &blobs);
        assert!(
            inputs
                .object(&good, IdentityDomain::Import, 1_000_000)
                .is_ok()
        );
        assert!(matches!(
            inputs.object(&wrong, IdentityDomain::Import, 1_000_000),
            Err(Error::ClosureRole {
                field: "producerClosure",
                expected: "provider"
            })
        ));
        // Success above intentionally does not establish the absent payload bytes.
        assert!(matches!(inputs.blob([0; 32]), Err(Error::MissingBlob(_))));
        objects.remove(&adapter);
        assert!(matches!(
            RetainedInputs::new(&registry, &objects, &blobs).object(
                &good,
                IdentityDomain::Import,
                1_000_000
            ),
            Err(Error::MissingObject(_))
        ));
    }

    type StructureFixture = (
        RegisteredSchemas,
        BTreeMap<String, ObjectInput>,
        BTreeMap<[u8; 32], Vec<u8>>,
        String,
    );

    fn structure_fixture(length: u64) -> StructureFixture {
        let registry = crate::embedded_schema_registry().unwrap();
        let mut objects = BTreeMap::new();
        let manifest = b"manifest".to_vec();
        let member = b"source bytes".to_vec();
        let mut blobs = BTreeMap::new();
        blobs.insert(raw_sha256(&manifest), manifest.clone());
        blobs.insert(raw_sha256(&member), member.clone());
        let value = descriptor(&format!(
            r#"{{"schemaVersion":2,"kind":"provider","manifestDigest":"{}","tree":[{{"path":"src/a.rs","sha256":"{}","bytes":{length}}}],"semanticVersion":"1.0.0","protocolMajor":3,"platform":"macos-aarch64"}}"#,
            opensip_identity::digest_hex(&raw_sha256(&manifest)),
            opensip_identity::digest_hex(&raw_sha256(&member))
        ));
        let key = put(&registry, &mut objects, IdentityDomain::Closure, value);
        (registry, objects, blobs, key)
    }
    fn traversal_budget() -> opensip_identity::TraversalBudget {
        opensip_identity::TraversalBudget {
            steps: 10_000,
            depth: 64,
            descriptor_work: 1_000_000,
        }
    }
    #[test]
    fn local_walk_rehashes_manifest_members_and_checks_member_length() {
        let (registry, objects, blobs, key) = structure_fixture(12);
        let inputs = RetainedInputs::new(&registry, &objects, &blobs);
        let checked = inputs
            .inspect_local_structure(&key, IdentityDomain::Closure, traversal_budget())
            .unwrap();
        assert_eq!(checked.object_count(), 1);
        assert_eq!(checked.blob_count(), 2);
        assert_eq!(checked.record_count(), 0);
        let (registry, objects, blobs, key) = structure_fixture(13);
        assert!(matches!(
            RetainedInputs::new(&registry, &objects, &blobs).inspect_local_structure(
                &key,
                IdentityDomain::Closure,
                traversal_budget()
            ),
            Err(opensip_identity::GraphError::Input(Error::BlobLength))
        ));
    }
    #[test]
    fn local_walk_keeps_missing_corrupt_and_limit_distinct() {
        let (registry, objects, mut blobs, key) = structure_fixture(12);
        let member = raw_sha256(b"source bytes");
        blobs.remove(&member);
        assert!(matches!(
            RetainedInputs::new(&registry, &objects, &blobs).inspect_local_structure(
                &key,
                IdentityDomain::Closure,
                traversal_budget()
            ),
            Err(opensip_identity::GraphError::Input(Error::MissingBlob(_)))
        ));
        blobs.insert(member, b"different".to_vec());
        assert!(matches!(
            RetainedInputs::new(&registry, &objects, &blobs).inspect_local_structure(
                &key,
                IdentityDomain::Closure,
                traversal_budget()
            ),
            Err(opensip_identity::GraphError::Input(Error::BlobDigest))
        ));
        let budget = opensip_identity::TraversalBudget {
            steps: 0,
            ..traversal_budget()
        };
        assert!(matches!(
            RetainedInputs::new(&registry, &objects, &blobs).inspect_local_structure(
                &key,
                IdentityDomain::Closure,
                budget
            ),
            Err(opensip_identity::GraphError::Limit)
        ));
    }

    fn add_record(blobs: &mut BTreeMap<[u8; 32], Vec<u8>>, value: JsonValue) -> String {
        let raw = canonical_bytes(&value).unwrap();
        let hash = raw_sha256(&raw);
        blobs.insert(hash, raw);
        opensip_identity::digest_hex(&hash)
    }
    fn snapshot_structure(scope_path: &str) -> StructureFixture {
        let registry = crate::embedded_schema_registry().unwrap();
        let mut objects = BTreeMap::new();
        let mut blobs = BTreeMap::new();
        let inventory = add_record(&mut blobs, descriptor("[]"));
        let config = add_record(
            &mut blobs,
            descriptor(
                r#"{"analysis":{"profileId":"local","capabilities":[],"budget":{"unit":"work-units","limit":1}},"components":{"allowedScopes":["project","global"],"request":[{"stableId":"00000000-0000-0000-0000-000000000000","version":"1.0.0"},{"stableId":"ffffffff-ffff-ffff-ffff-ffffffffffff","version":"1.0.0"}]},"discovery":{},"policy":{},"evidence":{}}"#,
            ),
        );
        let scope = add_record(
            &mut blobs,
            descriptor(&format!(
                r#"{{"schemaVersion":2,"workspaceRoots":["{scope_path}"],"pathPrefixes":[],"excludedPathPrefixes":[]}}"#
            )),
        );
        let vcs = add_record(
            &mut blobs,
            descriptor(&format!(
                r#"{{"schemaVersion":2,"kind":"none","commitId":null,"dirty":false,"sourceInventoryDigest":"{inventory}"}}"#
            )),
        );
        let snapshot = descriptor(&format!(
            r#"{{"schemaVersion":2,"projectId":"prj1-{}","sourceInventory":[],"resolvedConfigDigest":"{config}","scopeDigest":"{scope}","vcsDigest":"{vcs}"}}"#,
            "0".repeat(64)
        ));
        let key = put(&registry, &mut objects, IdentityDomain::Snapshot, snapshot);
        (registry, objects, blobs, key)
    }
    #[test]
    fn local_records_follow_digest_annotations_and_preserve_configuration_sequences() {
        let (registry, objects, blobs, key) = snapshot_structure(".");
        let checked = RetainedInputs::new(&registry, &objects, &blobs)
            .inspect_local_structure(&key, IdentityDomain::Snapshot, traversal_budget())
            .unwrap();
        assert_eq!(checked.object_count(), 1);
        assert_eq!(checked.blob_count(), 4);
        assert_eq!(checked.record_count(), 4);
    }
    #[test]
    fn local_scope_dot_exception_does_not_admit_absolute_or_parent_paths() {
        for path in ["/bad", "a/../b"] {
            let (registry, objects, blobs, key) = snapshot_structure(path);
            assert!(matches!(
                RetainedInputs::new(&registry, &objects, &blobs).inspect_local_structure(
                    &key,
                    IdentityDomain::Snapshot,
                    traversal_budget()
                ),
                Err(opensip_identity::GraphError::Input(Error::Candidate(
                    opensip_identity::CandidateError::LogicalPath
                )))
            ));
        }
    }

    #[test]
    fn frame_candidate_is_current_shape_not_nested_blob_admission() {
        use opensip_identity::{GraphError, NativeFrameSet, hash_preimage};
        let registry = crate::embedded_schema_registry().unwrap();
        let objects = BTreeMap::new();
        let mut blobs = BTreeMap::new();
        let value = descriptor(&format!(
            r#"[{{"path":"dep/a.rs","contentSha256":"{}","byteLength":7}}]"#,
            "0".repeat(64)
        ));
        let raw = hash_preimage("native.dependency-file-manifest.v1", &value).unwrap();
        let sha = raw_sha256(&raw);
        blobs.insert(sha, raw);
        let inputs = RetainedInputs::new(&registry, &objects, &blobs);
        let candidate = inputs
            .frame_candidate(sha, NativeFrameSet::Nested, 1_000_000)
            .unwrap();
        assert_eq!(candidate.domain(), "native.dependency-file-manifest.v1");
        assert_eq!(candidate.descriptor(), &value);
        assert_eq!(
            candidate.schema().selector(),
            "/$defs/DependencyFileManifestV1"
        );
        // This deliberately valid frame names a missing member: shape alone
        // neither closes nested blobs nor grants native semantic authority.
        assert!(matches!(inputs.blob([0; 32]), Err(Error::MissingBlob(_))));
        assert!(matches!(
            inputs.frame_candidate(sha, NativeFrameSet::Context, 1_000_000),
            Err(GraphError::UnregisteredFrameDomain)
        ));
        assert!(matches!(
            inputs.frame_candidate(sha, NativeFrameSet::Nested, 0),
            Err(GraphError::Schema(
                opensip_identity::SchemaAdmissionError::Schema(
                    opensip_identity::SchemaError::Limit
                )
            ))
        ));
    }
    #[test]
    fn payload_schema_membership_is_narrower_than_available_sources() {
        use opensip_identity::GraphError;
        let registry = crate::embedded_schema_registry().unwrap();
        let objects = BTreeMap::new();
        let mut blobs = BTreeMap::new();
        let native = include_bytes!(concat!(
            env!("CARGO_MANIFEST_DIR"),
            "/../../schemas/sources/native-v2.schema.json"
        ));
        let identity = include_bytes!(concat!(
            env!("CARGO_MANIFEST_DIR"),
            "/../../schemas/sources/identity-v3.schema.json"
        ));
        let policy = include_bytes!(concat!(
            env!("CARGO_MANIFEST_DIR"),
            "/../../schemas/sources/policy-v2.schema.json"
        ));
        for raw in [native.as_slice(), identity.as_slice(), policy.as_slice()] {
            blobs.insert(raw_sha256(raw), raw.to_vec());
        }
        let inputs = RetainedInputs::new(&registry, &objects, &blobs);
        assert!(inputs.registered_schema_blob(raw_sha256(native)).is_ok());
        for raw in [identity.as_slice(), policy.as_slice()] {
            assert!(matches!(
                inputs.registered_schema_blob(raw_sha256(raw)),
                Err(GraphError::UnregisteredSchemaDocument)
            ));
        }
    }

    #[test]
    fn foundation_record_closes_a_record_in_another_current_document() {
        use opensip_identity::GraphError;
        let registry = crate::embedded_schema_registry().unwrap();
        let objects = BTreeMap::new();
        let mut blobs = BTreeMap::new();
        let policy = add_record(
            &mut blobs,
            descriptor(
                r####"{"gateSeverityAtLeast":"note","rules":[{"emitWhen":{"filters":[],"minResolution":"enumerated","op":"exists","relation":"a"},"enabled":false,"evidenceUse":[],"gate":false,"ruleId":"a","ruleProgramRef":{"contributionId":"a","programDigest":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","ruleStableId":"a","semanticsMajor":0},"severity":"note","subjectEnumeration":{"subjectKind":"file","universe":"a"}}],"schemaFamily":"opensip.product.policy","schemaMajor":2}"####,
            ),
        );
        let value = descriptor(&format!(
            r#"{{"schemaVersion":1,"policyDigest":"{policy}","rules":[]}}"#
        ));
        let raw = canonical_bytes(&value).unwrap();
        let sha = raw_sha256(&raw);
        blobs.insert(sha, raw);
        let inputs = RetainedInputs::new(&registry, &objects, &blobs);
        let checked = inputs
            .inspect_current_record(
                sha,
                "foundation/evaluator-emission-plan.schema.v1.json",
                "#",
                traversal_budget(),
            )
            .unwrap();
        assert_eq!(checked.record_count(), 2);
        assert_eq!(checked.blob_count(), 2);
        let missing=raw_sha256(&canonical_bytes(&descriptor(r####"{"gateSeverityAtLeast":"note","rules":[{"emitWhen":{"filters":[],"minResolution":"enumerated","op":"exists","relation":"a"},"enabled":false,"evidenceUse":[],"gate":false,"ruleId":"a","ruleProgramRef":{"contributionId":"a","programDigest":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","ruleStableId":"a","semanticsMajor":0},"severity":"note","subjectEnumeration":{"subjectKind":"file","universe":"a"}}],"schemaFamily":"opensip.product.policy","schemaMajor":2}"####)).unwrap());
        blobs.remove(&missing);
        let inputs = RetainedInputs::new(&registry, &objects, &blobs);
        assert!(
            matches!(inputs.inspect_current_record(sha,"foundation/evaluator-emission-plan.schema.v1.json","#",traversal_budget()),Err(GraphError::Input(Error::MissingBlob(h))) if h==missing)
        );
        blobs.insert(missing, b"wrong bytes".to_vec());
        let inputs = RetainedInputs::new(&registry, &objects, &blobs);
        assert!(matches!(
            inputs.inspect_current_record(
                sha,
                "foundation/evaluator-emission-plan.schema.v1.json",
                "#",
                traversal_budget()
            ),
            Err(GraphError::Input(Error::BlobDigest))
        ));
    }
    #[test]
    fn foreign_record_order_is_checked_before_digest_traversal() {
        use opensip_identity::GraphError;
        let registry = crate::embedded_schema_registry().unwrap();
        let objects = BTreeMap::new();
        let mut blobs = BTreeMap::new();
        let value = descriptor(r#"{"schemaVersion":1,"declaredBuildIds":["z","a"]}"#);
        let raw = canonical_bytes(&value).unwrap();
        let sha = raw_sha256(&raw);
        blobs.insert(sha, raw);
        let inputs = RetainedInputs::new(&registry, &objects, &blobs);
        assert!(matches!(
            inputs.inspect_current_record(
                sha,
                "foundation/import-source-context.schema.json",
                "#",
                traversal_budget()
            ),
            Err(GraphError::Schema(
                opensip_identity::SchemaAdmissionError::Mismatch
            ))
        ));
    }

    #[test]
    fn derived_recognition_hash_checks_inline_preimage_without_a_cas_frame() {
        use opensip_identity::{GraphError, digest_hex, hash_canonical_value};
        let registry = crate::embedded_schema_registry().unwrap();
        let objects = BTreeMap::new();
        let recognition = descriptor(
            r#"{"entryPoints":{"source":"explicit","state":"all"},"observedHints":[],"recognized":[],"schemaVersion":1}"#,
        );
        let derived =
            hash_canonical_value("native.framework-recognition.v1", &recognition).unwrap();
        for (correct, hash) in [(true, derived), (false, [0; 32])] {
            let mut blobs = BTreeMap::new();
            let row = descriptor(&format!(
                r#"{{"markerPath":"","recognition":{},"recognitionId":"sha256:{}","rootPath":"","unitOrdinal":0}}"#,
                core::str::from_utf8(&canonical_bytes(&recognition).unwrap()).unwrap(),
                digest_hex(&hash)
            ));
            let raw = canonical_bytes(&row).unwrap();
            let sha = raw_sha256(&raw);
            blobs.insert(sha, raw);
            let inputs = RetainedInputs::new(&registry, &objects, &blobs);
            let result = inputs.inspect_current_record(
                sha,
                "foundation/framework-recognition-plan.schema.v1.json",
                "#/$defs/UnitRecognitionV1",
                traversal_budget(),
            );
            if correct {
                let checked = result.unwrap();
                assert_eq!(checked.record_count(), 1);
                assert_eq!(checked.blob_count(), 1);
                assert!(matches!(inputs.blob(derived), Err(Error::MissingBlob(_))));
            } else {
                assert!(matches!(result, Err(GraphError::DerivedIdentity)));
            }
        }
    }

    #[test]
    fn stage_schema_owner_is_explicitly_pending_after_retained_blob_check() {
        use opensip_identity::GraphError;
        let registry = crate::embedded_schema_registry().unwrap();
        let mut objects = BTreeMap::new();
        let mut blobs = BTreeMap::new();
        let producer = put(
            &registry,
            &mut objects,
            IdentityDomain::Closure,
            closure("provider"),
        );
        let schema = add_record(&mut blobs, descriptor(r#"{"type":"object"}"#));
        let stage = descriptor(&format!(
            r#"{{"schemaVersion":2,"planId":"plan2:{}","producerClosure":"{producer}","operation":"derive-inventory-view","parameters":[],"outputDomains":["view"],"outputSchemaDigest":"{schema}"}}"#,
            "0".repeat(64)
        ));
        let raw = canonical_bytes(&stage).unwrap();
        let sha = raw_sha256(&raw);
        blobs.insert(sha, raw);
        let inputs = RetainedInputs::new(&registry, &objects, &blobs);
        assert!(matches!(
            inputs.inspect_identity_record(sha, "stage-spec", traversal_budget()),
            Err(GraphError::Unsupported("stage output schema owner join"))
        ));
        let schema_sha = raw_sha256(&canonical_bytes(&descriptor(r#"{"type":"object"}"#)).unwrap());
        blobs.remove(&schema_sha);
        let inputs = RetainedInputs::new(&registry, &objects, &blobs);
        assert!(
            matches!(inputs.inspect_identity_record(sha,"stage-spec",traversal_budget()),Err(GraphError::Input(Error::MissingBlob(h))) if h==schema_sha)
        );
    }

    #[test]
    fn parameter_payload_requires_exact_retained_registry_document() {
        use opensip_identity::{GraphError, digest_hex};
        let registry = crate::embedded_schema_registry().unwrap();
        let objects = BTreeMap::new();
        let mut blobs = BTreeMap::new();
        let source = include_bytes!(concat!(
            env!("CARGO_MANIFEST_DIR"),
            "/../../schemas/sources/import-source-context-v1.schema.json"
        ));
        let source_sha = raw_sha256(source);
        let schema = digest_hex(&source_sha);
        let payload = add_record(
            &mut blobs,
            descriptor(r#"{"schemaVersion":1,"declaredBuildIds":[]}"#),
        );
        let spec = descriptor(&format!(
            r#"{{"schemaVersion":2,"requestedCapabilities":[{{"capabilityId":"inventory","languageMode":"syntax-only","workspaceRoot":".","required":true}}],"policyPackIds":["fixture"],"parameters":[{{"schemaDigest":"{schema}","payloadDigest":"{payload}"}}]}}"#
        ));
        let raw = canonical_bytes(&spec).unwrap();
        let sha = raw_sha256(&raw);
        blobs.insert(sha, raw);
        let inputs = RetainedInputs::new(&registry, &objects, &blobs);
        assert!(
            matches!(inputs.inspect_identity_record(sha,"analysis-spec",traversal_budget()),Err(GraphError::Input(Error::MissingBlob(h))) if h==source_sha)
        );
        blobs.insert(source_sha, source.to_vec());
        let inputs = RetainedInputs::new(&registry, &objects, &blobs);
        assert!(
            inputs
                .inspect_identity_record(sha, "analysis-spec", traversal_budget())
                .is_ok()
        );
        blobs.insert(source_sha, b"altered document".to_vec());
        let inputs = RetainedInputs::new(&registry, &objects, &blobs);
        assert!(matches!(
            inputs.inspect_identity_record(sha, "analysis-spec", traversal_budget()),
            Err(GraphError::Input(Error::BlobDigest))
        ));
    }
    #[test]
    fn shared_parameter_payload_does_not_bypass_second_reference_row_selection() {
        use opensip_identity::{GraphError, digest_hex};
        let registry = crate::embedded_schema_registry().unwrap();
        let objects = BTreeMap::new();
        let mut blobs = BTreeMap::new();
        let source = include_bytes!(concat!(
            env!("CARGO_MANIFEST_DIR"),
            "/../../schemas/sources/import-source-context-v1.schema.json"
        ));
        let source_sha = raw_sha256(source);
        let schema = digest_hex(&source_sha);
        blobs.insert(source_sha, source.to_vec());
        let payload = add_record(
            &mut blobs,
            descriptor(r#"{"schemaVersion":1,"declaredBuildIds":[]}"#),
        );
        let spec = descriptor(&format!(
            r#"{{"schemaVersion":2,"requestedCapabilities":[{{"capabilityId":"inventory","languageMode":"syntax-only","workspaceRoot":".","required":true}}],"policyPackIds":["fixture"],"parameters":[{{"schemaDigest":"{schema}","payloadDigest":"{payload}"}},{{"schemaDigest":"{}","payloadDigest":"{payload}"}}]}}"#,
            "f".repeat(64)
        ));
        let raw = canonical_bytes(&spec).unwrap();
        let sha = raw_sha256(&raw);
        blobs.insert(sha, raw);
        let inputs = RetainedInputs::new(&registry, &objects, &blobs);
        assert!(matches!(
            inputs.inspect_identity_record(sha, "analysis-spec", traversal_budget()),
            Err(GraphError::PayloadRegistryRow)
        ));
    }

    #[test]
    fn coverage_payload_shape_and_document_selection_precede_missing_scope() {
        use opensip_identity::{GraphError, digest_hex};
        let registry = crate::embedded_schema_registry().unwrap();
        let source = include_bytes!(concat!(
            env!("CARGO_MANIFEST_DIR"),
            "/../../schemas/sources/native-v2.schema.json"
        ));
        let source_sha = raw_sha256(source);
        let scope = format!("scope2:{}", "0".repeat(64));
        // Schema-valid input only, not a claim of native semantic admission.
        for mode in 0..4 {
            let mut objects = BTreeMap::new();
            let mut blobs = BTreeMap::new();
            blobs.insert(source_sha, source.to_vec());
            let mut payload = descriptor(
                r####"{"entry":{"closedWorld":{"deadCodeRepairEligible":false,"dynamicDispatch":"resolved","entryPointsRecognized":"all","exportsClosed":"closed","externalConsumers":"none-declared","nonliteralLoading":"none","reasons":[]},"confidenceMillionths":0,"coverage":"complete","deficiency":"language-tier-unsupported","derivationKinds":[],"examinedUniverse":{"subjectCount":0,"subjectScopeCommitment":"sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"},"nativeCause":"body-language-owner-ambiguous","relation":"file","resolution":"enumerated","resolutionCompleteness":{"attempted":false,"examinedExhaustive":false,"stageTerminal":"complete","state":"complete","unresolvedEdgeClasses":[],"unresolvedEdgeCount":0}},"key":{"relation":"file","resolution":"enumerated","sourceUniverse":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","subjectScopeCommitment":"sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","targetUniverse":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"},"schemaVersion":3}"####,
            );
            if mode == 2 {
                payload = descriptor(r#"{"schemaVersion":3}"#);
            }
            if mode == 3
                && let JsonValue::Object(ref mut o) = payload
            {
                o.insert("schemaVersion".into(), descriptor("2"));
            }
            let payload = add_record(&mut blobs, payload);
            let claimed = if mode == 1 {
                "f".repeat(64)
            } else {
                digest_hex(&source_sha)
            };
            let value = descriptor(&format!(
                r#"{{"schemaVersion":2,"scopeId":"{scope}","payloadSchemaDigest":"{claimed}","payloadDigest":"{payload}"}}"#
            ));
            let key = put(&registry, &mut objects, IdentityDomain::Coverage, value);
            let inputs = RetainedInputs::new(&registry, &objects, &blobs);
            let result =
                inputs.inspect_local_structure(&key, IdentityDomain::Coverage, traversal_budget());
            match mode {
                0 => assert!(
                    matches!(result,Err(GraphError::Input(Error::MissingObject(ref key))) if key==&scope)
                ),
                1 => assert!(matches!(result, Err(GraphError::PayloadSchemaDocument))),
                2 => assert!(matches!(
                    result,
                    Err(GraphError::Schema(
                        opensip_identity::SchemaAdmissionError::Mismatch
                    ))
                )),
                _ => assert!(matches!(result, Err(GraphError::PayloadRegistryRow))),
            }
        }
    }

    #[test]
    fn relation_file_checks_owning_snapshot_and_retained_content_each_time() {
        use opensip_identity::{GraphError, digest_hex};
        let registry = crate::embedded_schema_registry().unwrap();
        let schema = include_bytes!(concat!(
            env!("CARGO_MANIFEST_DIR"),
            "/../../schemas/sources/relation-payload-v2.schema.json"
        ));
        let schema_sha = raw_sha256(schema);
        let source = b"source";
        let source_sha = raw_sha256(source);
        let mut blobs =
            BTreeMap::from([(schema_sha, schema.to_vec()), (source_sha, source.to_vec())]);
        let payload = descriptor(&format!(
            r#"{{"path":"src/a.ts","contentSha256":"{}","byteLength":6}}"#,
            digest_hex(&source_sha)
        ));
        let raw = canonical_bytes(&payload).unwrap();
        let payload_sha = raw_sha256(&raw);
        blobs.insert(payload_sha, raw);
        let mut objects = BTreeMap::new();
        let mut keys = Vec::new();
        for path in ["src/a.ts", "src/other.ts"] {
            let snapshot = descriptor(&format!(
                r#"{{"schemaVersion":2,"projectId":"prj1-{z}","sourceInventory":[{{"path":"{path}","sha256":"{sha}","bytes":6}}],"resolvedConfigDigest":"{z}","scopeDigest":"{z}","vcsDigest":"{z}"}}"#,
                z = "0".repeat(64),
                sha = digest_hex(&source_sha)
            ));
            keys.push(put(
                &registry,
                &mut objects,
                IdentityDomain::Snapshot,
                snapshot,
            ));
        }
        let fact = |snapshot: &str| {
            descriptor(&format!(
                r#"{{"relation":"file","resolution":"enumerated","anchors":[],"sourceUniverse":"a","targetUniverse":"a","snapshotId":"{snapshot}"}}"#
            ))
        };
        let inputs = RetainedInputs::new(&registry, &objects, &blobs);
        assert!(
            inputs
                .inspect_relation_sources(
                    payload_sha,
                    schema_sha,
                    &fact(&keys[0]),
                    traversal_budget()
                )
                .is_ok()
        );
        assert!(matches!(
            inputs.inspect_relation_sources(
                payload_sha,
                schema_sha,
                &fact(&keys[1]),
                traversal_budget()
            ),
            Err(GraphError::RelationRule("path not inventoried"))
        ));
        blobs.remove(&source_sha);
        let inputs = RetainedInputs::new(&registry, &objects, &blobs);
        assert!(matches!(
            inputs.inspect_relation_sources(
                payload_sha,
                schema_sha,
                &fact(&keys[0]),
                traversal_budget()
            ),
            Err(GraphError::Input(Error::MissingBlob(_)))
        ));
        blobs.insert(source_sha, b"changed".to_vec());
        let inputs = RetainedInputs::new(&registry, &objects, &blobs);
        assert!(matches!(
            inputs.inspect_relation_sources(
                payload_sha,
                schema_sha,
                &fact(&keys[0]),
                traversal_budget()
            ),
            Err(GraphError::Input(Error::BlobDigest))
        ));
    }
    #[test]
    fn relation_payload_checks_rung_anchor_nfc_and_exact_retained_schema() {
        use opensip_identity::GraphError;
        let registry = crate::embedded_schema_registry().unwrap();
        let schema = include_bytes!(concat!(
            env!("CARGO_MANIFEST_DIR"),
            "/../../schemas/sources/relation-payload-v2.schema.json"
        ));
        let schema_sha = raw_sha256(schema);
        let mut blobs = BTreeMap::from([(schema_sha, schema.to_vec())]);
        let objects = BTreeMap::new();
        let good = descriptor(r#"{"caller":"sym:a","calleeText":"é"}"#);
        let raw = canonical_bytes(&good).unwrap();
        let sha = raw_sha256(&raw);
        blobs.insert(sha, raw);
        let fact = descriptor(
            r#"{"relation":"calls","resolution":"syntactic-callee-name","anchors":[{}],"sourceUniverse":"a","targetUniverse":"b"}"#,
        );
        let inputs = RetainedInputs::new(&registry, &objects, &blobs);
        // admitted-target is not a same-only rule. This does NOT admit that target.
        assert!(
            inputs
                .inspect_relation_payload(sha, schema_sha, &fact, traversal_budget())
                .is_ok()
        );
        let mut changed = fact.clone();
        if let JsonValue::Object(ref mut o) = changed {
            o.insert("resolution".into(), descriptor("\"resolved-callee\""));
        }
        assert!(matches!(
            inputs.inspect_relation_payload(sha, schema_sha, &changed, traversal_budget()),
            Err(GraphError::RelationRule("required rung field"))
        ));
        let mut changed = fact.clone();
        if let JsonValue::Object(ref mut o) = changed {
            o.insert("anchors".into(), descriptor("[]"));
        }
        assert!(matches!(
            inputs.inspect_relation_payload(sha, schema_sha, &changed, traversal_budget()),
            Err(GraphError::RelationRule("anchor cardinality"))
        ));
        let bad = descriptor(r#"{"caller":"sym:a","calleeText":"e\u0301"}"#);
        let raw = canonical_bytes(&bad).unwrap();
        let bad_sha = raw_sha256(&raw);
        blobs.insert(bad_sha, raw);
        let inputs = RetainedInputs::new(&registry, &objects, &blobs);
        assert!(matches!(
            inputs.inspect_relation_payload(bad_sha, schema_sha, &fact, traversal_budget()),
            Err(GraphError::RelationRule("non-NFC string"))
        ));
        assert!(matches!(
            inputs.inspect_relation_payload(sha, [0; 32], &fact, traversal_budget()),
            Err(GraphError::PayloadSchemaDocument)
        ));
        blobs.remove(&schema_sha);
        let inputs = RetainedInputs::new(&registry, &objects, &blobs);
        assert!(matches!(
            inputs.inspect_relation_payload(sha, schema_sha, &fact, traversal_budget()),
            Err(GraphError::Input(Error::MissingBlob(_)))
        ));
    }
}
