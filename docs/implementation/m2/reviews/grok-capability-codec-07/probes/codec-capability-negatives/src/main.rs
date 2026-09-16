//! Independent capability-codec-07 negatives. Not part of the frozen subject.
use opensip_evaluator::admit_capability_manifest;
use opensip_identity::{
    Cve1Error, GraphError, IdentityCandidate, IdentityDomain, JsonInteger, JsonValue, ObjectInput,
    RetainedInputs, TraversalBudget, decode_cve1, digest_hex, encode_cve1, parse_json, raw_sha256,
};
use std::collections::BTreeMap;
use unicode_normalization::UNICODE_VERSION;

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
    let raw = opensip_identity::canonical_bytes(&value).unwrap();
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
        "unicode16-pin",
        UNICODE_VERSION == (16, 0, 0),
        format!("{UNICODE_VERSION:?}"),
    );
    check(
        &mut failures,
        "cve1-integer-tags",
        encode_cve1(&JsonValue::Integer(JsonInteger::new(0).unwrap())).unwrap()
            == vec![3, 0, 0, 0, 0, 0, 0, 0, 0]
            && encode_cve1(&JsonValue::Integer(JsonInteger::new(-1).unwrap())).unwrap()
                == vec![7, 255, 255, 255, 255, 255, 255, 255, 255],
        "tag 3 vs 7".into(),
    );
    check(
        &mut failures,
        "cve1-nfc-refuses-decomposed",
        decode_cve1(&[4, 0, 0, 0, 3, b'e', 0xcc, 0x81]) == Err(Cve1Error::NotNfc)
            && decode_cve1(&[4, 0, 0, 0, 2, 0xc3, 0xa9]).unwrap()
                == JsonValue::String("é".into()),
        "NFC".into(),
    );
    check(
        &mut failures,
        "cve1-depth-64-ok-65-bound",
        {
            let mut d64 = Vec::new();
            for _ in 0..64 {
                d64.extend_from_slice(&[5, 0, 0, 0, 1]);
            }
            d64.push(0);
            let mut d65 = Vec::new();
            for _ in 0..65 {
                d65.extend_from_slice(&[5, 0, 0, 0, 1]);
            }
            d65.push(0);
            decode_cve1(&d64).is_ok() && decode_cve1(&d65) == Err(Cve1Error::DepthBound)
        },
        "CVE1 depth is 64, not JSON-C 32".into(),
    );
    check(
        &mut failures,
        "cve1-trailing-and-unknown-tag",
        decode_cve1(&[0, 0]) == Err(Cve1Error::TrailingBytes)
            && decode_cve1(&[255]) == Err(Cve1Error::Tag),
        "no repair".into(),
    );

    let golden = include_bytes!(concat!(
        env!("CARGO_MANIFEST_DIR"),
        "/../../subject/product/crates/evaluator/tests/fixtures/capability-manifest.golden.cve1"
    ));
    let admitted = admit_capability_manifest(golden).expect("golden");
    check(
        &mut failures,
        "golden-identity",
        digest_hex(&admitted.identity())
            == "508f24c718a0564c52fe18a1e6a5308d53bdd6012a50ad186ffbc208bb18881b",
        digest_hex(&admitted.identity()),
    );
    let mut value = decode_cve1(golden).unwrap();
    if let JsonValue::Object(ref mut o) = value {
        o.insert(
            "schemaVersion".into(),
            JsonValue::Integer(JsonInteger::new(99).unwrap()),
        );
        o.insert("profile".into(), JsonValue::String("not-a-product-promise".into()));
        if let JsonValue::Array(providers) = o.get_mut("providers").unwrap()
            && let JsonValue::Object(p) = &mut providers[0]
        {
            p.insert("language".into(), JsonValue::String("cobol".into()));
            p.insert(
                "platformIds".into(),
                JsonValue::Array(vec![JsonValue::String("windows-x86_64-msvc".into())]),
            );
        }
    }
    let open = admit_capability_manifest(&encode_cve1(&value).unwrap());
    check(
        &mut failures,
        "open-schemaversion-language-windows-not-custody",
        open.is_ok(),
        if open.is_ok() {
            "ok".into()
        } else {
            format!("refusals={:?}", open.err().unwrap().causes())
        },
    );
    if let JsonValue::Object(ref mut o) = value {
        o.insert("schemaVersion".into(), JsonValue::Bool(true));
    }
    let typed = admit_capability_manifest(&encode_cve1(&value).unwrap());
    check(
        &mut failures,
        "boolean-schemaversion-is-type-not-open",
        typed.as_ref().err().is_some_and(|e| {
            e.causes()
                .iter()
                .any(|c| c == "capability.adm-type:CapabilityManifestV1.schemaVersion")
        }),
        typed.err().map(|e| e.causes().join(",")).unwrap_or_default(),
    );

    let registry = opensip_host::embedded_schema_registry().unwrap();
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
    let walked = inputs.inspect_local_structure(&key, IdentityDomain::Fact, budget());
    check(
        &mut failures,
        "graph-relation-still-unsupported",
        matches!(
            walked,
            Err(GraphError::Unsupported("payload-class owner joins"))
        ),
        if let Err(GraphError::Unsupported(s)) = walked {
            s.into()
        } else {
            "not-unsupported".into()
        },
    );

    println!("failures={}", failures.len());
    if !failures.is_empty() {
        std::process::exit(1);
    }
    println!("ALL_PASS");
    let _ = raw_sha256(b"");
}
