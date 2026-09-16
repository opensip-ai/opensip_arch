//! Independent payloads05 negatives. Not part of the frozen subject.
use opensip_identity::{
    GraphError, IdentityCandidate, IdentityDomain, JsonValue, ObjectInput, RetainedInputError,
    RetainedInputs, TraversalBudget, canonical_bytes, digest_hex, parse_json, raw_sha256,
};
use std::collections::BTreeMap;

fn budget() -> TraversalBudget {
    TraversalBudget {
        steps: 10_000,
        depth: 64,
        descriptor_work: 1_000_000,
    }
}
fn descriptor(raw: &str) -> JsonValue {
    parse_json(raw.as_bytes()).unwrap()
}
fn put(
    registry: &opensip_identity::RegisteredSchemas,
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
fn add_record(blobs: &mut BTreeMap<[u8; 32], Vec<u8>>, value: JsonValue) -> String {
    let raw = canonical_bytes(&value).unwrap();
    let hash = raw_sha256(&raw);
    blobs.insert(hash, raw);
    digest_hex(&hash)
}
fn closure(kind: &str) -> JsonValue {
    descriptor(&format!(
        r#"{{"schemaVersion":2,"kind":"{kind}","manifestDigest":"{}","tree":[],"semanticVersion":"1.0.0","protocolMajor":3,"platform":"macos-aarch64"}}"#,
        "0".repeat(64)
    ))
}
fn err_name(r: &Result<opensip_identity::StructuralChecks, GraphError>) -> String {
    match r {
        Ok(_) => "ok".into(),
        Err(GraphError::Input(RetainedInputError::MissingBlob(_))) => "MissingBlob".into(),
        Err(GraphError::Input(RetainedInputError::MissingObject(_))) => "MissingObject".into(),
        Err(GraphError::Input(RetainedInputError::BlobDigest)) => "BlobDigest".into(),
        Err(e) => format!("{e:?}"),
    }
}

fn main() {
    let mut failures = Vec::new();
    let check = |failures: &mut Vec<String>, name: &str, ok: bool, detail: String| {
        println!("{} {} {}", if ok { "PASS" } else { "FAIL" }, name, detail);
        if !ok {
            failures.push(format!("{name}: {detail}"));
        }
    };
    let registry = opensip_host::embedded_schema_registry().expect("registry");
    let source = include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../subject/product/schemas/sources/import-source-context-v1.schema.json"
    ));
    let native = include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../subject/product/schemas/sources/native-v2.schema.json"
    ));
    let identity = include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../subject/product/schemas/sources/identity-v3.schema.json"
    ));
    let source_sha = raw_sha256(source);
    let native_sha = raw_sha256(native);
    let schema = digest_hex(&source_sha);
    let native_hex = digest_hex(&native_sha);

    // Full document SHA, not a canonicalized $defs subschema.
    let native_doc = parse_json(native).unwrap();
    let JsonValue::Object(root) = &native_doc else {
        panic!("native root");
    };
    let sub = root
        .get("$defs")
        .and_then(|d| if let JsonValue::Object(m) = d { m.get("CoverageResultV3") } else { None })
        .cloned()
        .expect("CoverageResultV3");
    let sub_sha = raw_sha256(&canonical_bytes(&sub).unwrap());
    check(
        &mut failures,
        "subschema-sha-is-not-document-sha",
        sub_sha != native_sha,
        format!("sub={} doc={}", digest_hex(&sub_sha), native_hex),
    );

    // Caller cannot assemble a private registry: pin length/bytes refuse.
    check(
        &mut failures,
        "no-caller-chosen-registry",
        matches!(
            opensip_identity::RegisteredSchemas::from_sources(&[b"{}" as &[u8]]),
            Err(opensip_identity::SchemaAdmissionError::SourceSet)
        ),
        "from_sources of a one-document set must refuse".into(),
    );

    let coverage_payload = descriptor(
        r####"{"entry":{"closedWorld":{"deadCodeRepairEligible":false,"dynamicDispatch":"resolved","entryPointsRecognized":"all","exportsClosed":"closed","externalConsumers":"none-declared","nonliteralLoading":"none","reasons":[]},"confidenceMillionths":0,"coverage":"complete","deficiency":"language-tier-unsupported","derivationKinds":[],"examinedUniverse":{"subjectCount":0,"subjectScopeCommitment":"sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"},"nativeCause":"body-language-owner-ambiguous","relation":"file","resolution":"enumerated","resolutionCompleteness":{"attempted":false,"examinedExhaustive":false,"stageTerminal":"complete","state":"complete","unresolvedEdgeClasses":[],"unresolvedEdgeCount":0}},"key":{"relation":"file","resolution":"enumerated","sourceUniverse":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","subjectScopeCommitment":"sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","targetUniverse":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"},"schemaVersion":3}"####,
    );

    // Parameter: exact retained full-document SHA, then foundation recurse.
    {
        let objects = BTreeMap::new();
        let mut blobs = BTreeMap::new();
        let payload = add_record(
            &mut blobs,
            descriptor(r#"{"schemaVersion":1,"declaredBuildIds":[]}"#),
        );
        let spec = descriptor(&format!(
            r#"{{"schemaVersion":2,"requestedCapabilities":[{{"capabilityId":"inventory","languageMode":"syntax-only","workspaceRoot":".","required":true}}],"policyPackIds":["fixture"],"parameters":[{{"schemaDigest":"{schema}","payloadDigest":"{payload}"}}]}}"#
        ));
        let raw = canonical_bytes(&spec).unwrap();
        let sha = raw_sha256(&raw);
        blobs.insert(sha, raw.clone());
        let inputs = RetainedInputs::new(&registry, &objects, &blobs);
        let missing = inputs.inspect_identity_record(sha, "analysis-spec", budget());
        check(
            &mut failures,
            "parameter-missing-schema-blob",
            matches!(missing, Err(GraphError::Input(RetainedInputError::MissingBlob(h))) if h == source_sha),
            err_name(&missing),
        );
        blobs.insert(source_sha, source.to_vec());
        let inputs = RetainedInputs::new(&registry, &objects, &blobs);
        let ok = inputs.inspect_identity_record(sha, "analysis-spec", budget());
        check(
            &mut failures,
            "parameter-retained-full-document",
            ok.is_ok(),
            match &ok {
                Ok(c) => format!(
                    "records={} blobs={} objects={}",
                    c.record_count(),
                    c.blob_count(),
                    c.object_count()
                ),
                Err(_) => err_name(&ok),
            },
        );
        // Counts are not Plan tokens; foundation parameter recurse visits the payload record.
        if let Ok(c) = &ok {
            check(
                &mut failures,
                "structural-checks-are-not-plan-tokens",
                c.record_count() >= 1 && c.blob_count() >= 2 && c.object_count() == 0,
                format!(
                    "records={} blobs={} objects={}",
                    c.record_count(),
                    c.blob_count(),
                    c.object_count()
                ),
            );
        }
        blobs.insert(source_sha, b"altered document".to_vec());
        let inputs = RetainedInputs::new(&registry, &objects, &blobs);
        let corrupt = inputs.inspect_identity_record(sha, "analysis-spec", budget());
        check(
            &mut failures,
            "parameter-corrupt-schema-blob",
            matches!(corrupt, Err(GraphError::Input(RetainedInputError::BlobDigest))),
            err_name(&corrupt),
        );
    }

    // Shared payload cannot authorize a second unregistered schema context.
    {
        let objects = BTreeMap::new();
        let mut blobs = BTreeMap::new();
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
        let second = inputs.inspect_identity_record(sha, "analysis-spec", budget());
        check(
            &mut failures,
            "no-memoized-second-context",
            matches!(second, Err(GraphError::PayloadRegistryRow)),
            err_name(&second),
        );
    }

    // Coverage: shape then missing scope; wrong document; subschema SHA; unregistered version.
    let scope = format!("scope2:{}", "0".repeat(64));
    let run_coverage = |claimed: &str, payload: JsonValue| {
        let mut objects = BTreeMap::new();
        let mut blobs = BTreeMap::new();
        blobs.insert(native_sha, native.to_vec());
        let p = add_record(&mut blobs, payload);
        let value = descriptor(&format!(
            r#"{{"schemaVersion":2,"scopeId":"{scope}","payloadSchemaDigest":"{claimed}","payloadDigest":"{p}"}}"#
        ));
        let key = put(&registry, &mut objects, IdentityDomain::Coverage, value);
        let inputs = RetainedInputs::new(&registry, &objects, &blobs);
        inputs.inspect_local_structure(&key, IdentityDomain::Coverage, budget())
    };
    let shape = run_coverage(&native_hex, coverage_payload.clone());
    check(
        &mut failures,
        "coverage-shape-then-missing-scope-not-native",
        matches!(shape, Err(GraphError::Input(RetainedInputError::MissingObject(ref k))) if k == &scope),
        err_name(&shape),
    );
    let wrong_doc = run_coverage(&digest_hex(&raw_sha256(identity)), coverage_payload.clone());
    check(
        &mut failures,
        "coverage-wrong-schema-document",
        matches!(wrong_doc, Err(GraphError::PayloadSchemaDocument)),
        err_name(&wrong_doc),
    );
    let subschema = run_coverage(&digest_hex(&sub_sha), coverage_payload.clone());
    check(
        &mut failures,
        "coverage-subschema-sha-refused",
        matches!(subschema, Err(GraphError::PayloadSchemaDocument)),
        err_name(&subschema),
    );
    let mut ver2 = coverage_payload.clone();
    if let JsonValue::Object(ref mut o) = ver2 {
        o.insert("schemaVersion".into(), descriptor("2"));
    }
    let unregistered = run_coverage(&native_hex, ver2);
    check(
        &mut failures,
        "coverage-unregistered-schemaversion",
        matches!(unregistered, Err(GraphError::PayloadRegistryRow)),
        err_name(&unregistered),
    );
    let mismatch = run_coverage(&native_hex, descriptor(r#"{"schemaVersion":3}"#));
    check(
        &mut failures,
        "coverage-shape-mismatch-before-scope",
        matches!(
            mismatch,
            Err(GraphError::Schema(
                opensip_identity::SchemaAdmissionError::Mismatch
            ))
        ),
        err_name(&mismatch),
    );

    // Relation payload class remains Unsupported; not ADMIT.
    {
        let mut objects = BTreeMap::new();
        let blobs = BTreeMap::new();
        let producer = put(
            &registry,
            &mut objects,
            IdentityDomain::Closure,
            closure("provider"),
        );
        let z = "0".repeat(64);
        let fact = descriptor(&format!(
            r#"{{"schemaVersion":2,"snapshotId":"snapshot2:{z}","relation":"file","resolution":"enumerated","sourceUniverse":"{z}","targetUniverse":"{z}","producerClosure":"{producer}","payloadSchemaDigest":"{z}","payloadDigest":"{z}","anchors":[],"confidenceMillionths":0}}"#
        ));
        let key = put(&registry, &mut objects, IdentityDomain::Fact, fact);
        let inputs = RetainedInputs::new(&registry, &objects, &blobs);
        let rel = inputs.inspect_local_structure(&key, IdentityDomain::Fact, budget());
        check(
            &mut failures,
            "relation-payload-unsupported",
            matches!(rel, Err(GraphError::Unsupported("payload-class owner joins"))),
            err_name(&rel),
        );
    }

    // Import candidate/role success does not retain or admit the payload.
    {
        let mut objects = BTreeMap::new();
        let blobs = BTreeMap::new();
        let producer = put(
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
        let z = "0".repeat(64);
        let import = descriptor(&format!(
            r#"{{"schemaVersion":2,"kind":"runtime","payloadSchemaDigest":"{z}","payloadDigest":"{z}","sourceCorrespondenceDigest":"{z}","buildDigest":"{z}","producerClosure":"{producer}","adapterClosure":"{adapter}","blobs":[],"scopeDigest":"{z}","observationDigest":"{z}","completeness":"unknown","omissions":[]}}"#
        ));
        let key = put(&registry, &mut objects, IdentityDomain::Import, import);
        let inputs = RetainedInputs::new(&registry, &objects, &blobs);
        check(
            &mut failures,
            "import-object-without-payload-is-not-admit",
            inputs.object(&key, IdentityDomain::Import, 1_000_000).is_ok()
                && matches!(inputs.blob([0; 32]), Err(RetainedInputError::MissingBlob(_))),
            "import object/role check must not imply retained payload bytes".into(),
        );
        let walked = inputs.inspect_local_structure(&key, IdentityDomain::Import, budget());
        check(
            &mut failures,
            "import-walk-does-not-ok-payload-class",
            !matches!(walked, Ok(_)),
            err_name(&walked),
        );
    }

    println!("failures={}", failures.len());
    if !failures.is_empty() {
        for f in &failures {
            eprintln!("FAIL {f}");
        }
        std::process::exit(1);
    }
    println!("ALL_PASS");
}
