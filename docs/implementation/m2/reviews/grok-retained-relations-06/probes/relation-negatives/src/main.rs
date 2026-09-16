//! Independent relations06 negatives. Not part of the frozen subject.
use opensip_identity::{
    GraphError, IdentityCandidate, IdentityDomain, JsonValue, ObjectInput, RetainedInputError,
    RetainedInputs, TraversalBudget, canonical_bytes, digest_hex, parse_json, raw_sha256,
};
use std::collections::BTreeMap;
use unicode_normalization::{UNICODE_VERSION, is_nfc};

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
fn err_name(r: &Result<(), GraphError>) -> String {
    match r {
        Ok(()) => "ok".into(),
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
    check(
        &mut failures,
        "unicode-normalization-is-16-0-0",
        UNICODE_VERSION == (16, 0, 0),
        format!("{UNICODE_VERSION:?}"),
    );
    check(
        &mut failures,
        "nfc-composed-accepted-decomposed-rejected",
        is_nfc("é") && !is_nfc("e\u{0301}"),
        format!("composed={} decomposed={}", is_nfc("é"), is_nfc("e\u{0301}")),
    );
    check(
        &mut failures,
        "typed-json-1-is-not-true",
        parse_json(b"1").unwrap() != parse_json(b"true").unwrap(),
        "Integer(1) must not equal Bool(true)".into(),
    );

    let registry = opensip_host::embedded_schema_registry().expect("registry");
    let schema = include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../subject/product/schemas/sources/relation-payload-v2.schema.json"
    ));
    let schema_sha = raw_sha256(schema);
    check(
        &mut failures,
        "full-schema-document-sha",
        digest_hex(&schema_sha) == "53380a2455490e07028e1872557044fb1b69d062143deeeec0f44006f0b2be9a",
        digest_hex(&schema_sha),
    );

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
    let ok = inputs.inspect_relation_payload(sha, schema_sha, &fact, budget());
    check(
        &mut failures,
        "admitted-target-is-not-same-only-and-not-native",
        ok.is_ok(),
        err_name(&ok),
    );
    let mut empty = fact.clone();
    if let JsonValue::Object(ref mut o) = empty {
        o.insert("anchors".into(), descriptor("[]"));
    }
    let card = inputs.inspect_relation_payload(sha, schema_sha, &empty, budget());
    check(
        &mut failures,
        "anchor-cardinality",
        matches!(card, Err(GraphError::RelationRule("anchor cardinality"))),
        err_name(&card),
    );
    let wrong = inputs.inspect_relation_payload(sha, [0; 32], &fact, budget());
    check(
        &mut failures,
        "wrong-schema-digest-is-full-document-not-caller-schema",
        matches!(wrong, Err(GraphError::PayloadSchemaDocument)),
        err_name(&wrong),
    );

    // Owning snapshot identity is re-checked per fact; a second snapshot does not inherit.
    let source = b"source";
    let source_sha = raw_sha256(source);
    let mut blobs = BTreeMap::from([
        (schema_sha, schema.to_vec()),
        (source_sha, source.to_vec()),
    ]);
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
    let first = inputs.inspect_relation_sources(payload_sha, schema_sha, &fact(&keys[0]), budget());
    let second = inputs.inspect_relation_sources(payload_sha, schema_sha, &fact(&keys[1]), budget());
    check(
        &mut failures,
        "second-fact-different-snapshot-does-not-reuse-first",
        first.is_ok()
            && matches!(second, Err(GraphError::RelationRule("path not inventoried"))),
        format!("first={} second={}", err_name(&first), err_name(&second)),
    );

    // Body join remains explicit Unsupported.
    let clones = descriptor(&format!(
        r#"{{"bodyIdentity":"sha256:{}","normalisationLevel":"L0-verbatim","normalisationVersion":"{}"}}"#,
        digest_hex(&source_sha),
        digest_hex(&source_sha)
    ));
    let raw = canonical_bytes(&clones).unwrap();
    let clones_sha = raw_sha256(&raw);
    blobs.insert(clones_sha, raw);
    let clones_fact = descriptor(&format!(
        r#"{{"relation":"clones","resolution":"normalized-body-hash","anchors":[{{"path":"src/a.ts","blobDigest":"{}","startByte":0,"endByte":6}}],"sourceUniverse":"a","targetUniverse":"a","snapshotId":"{}"}}"#,
        digest_hex(&source_sha),
        keys[0]
    ));
    let inputs = RetainedInputs::new(&registry, &objects, &blobs);
    let body = inputs.inspect_relation_sources(clones_sha, schema_sha, &clones_fact, budget());
    check(
        &mut failures,
        "clones-body-join-unsupported",
        matches!(body, Err(GraphError::Unsupported("relation body identity owner"))),
        err_name(&body),
    );

    // General graph walk still refuses relation payload class.
    {
        let mut objects = BTreeMap::new();
        let blobs = BTreeMap::new();
        let producer = put(
            &registry,
            &mut objects,
            IdentityDomain::Closure,
            descriptor(&format!(
                r#"{{"schemaVersion":2,"kind":"provider","manifestDigest":"{}","tree":[],"semanticVersion":"1.0.0","protocolMajor":3,"platform":"macos-aarch64"}}"#,
                "0".repeat(64)
            )),
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
            "graph-relation-payload-class-still-unsupported",
            matches!(
                rel,
                Err(GraphError::Unsupported("payload-class owner joins"))
            ),
            match &rel {
                Ok(_) => "ok".into(),
                Err(e) => format!("{e:?}"),
            },
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
