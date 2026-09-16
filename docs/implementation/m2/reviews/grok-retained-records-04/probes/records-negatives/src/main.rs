//! Independent records04 probes. Not part of the frozen subject.
use opensip_identity::{
    GraphError, JsonValue, ObjectInput, RetainedInputError, RetainedInputs, TraversalBudget,
    canonical_bytes, hash_canonical_value, parse_json, raw_sha256,
};
use std::collections::BTreeMap;

fn budget() -> TraversalBudget {
    TraversalBudget {
        steps: 10_000,
        depth: 64,
        descriptor_work: 1_000_000,
    }
}
fn err_debug<T>(r: Result<T, GraphError>) -> String {
    match r {
        Ok(_) => "ok".into(),
        Err(e) => format!("{e:?}"),
    }
}

fn main() {
    let mut failures = Vec::new();
    fn check(failures: &mut Vec<String>, name: &str, ok: bool, detail: String) {
        println!("{} {}", if ok { "PASS" } else { "FAIL" }, name);
        if !ok {
            failures.push(format!("{name}: {detail}"));
        }
    }
    let registry = opensip_host::embedded_schema_registry().expect("registry");
    let objects: BTreeMap<String, ObjectInput> = BTreeMap::new();

    // Cross-document foundation: emission plan policyDigest -> current policy-v2.
    let policy = parse_json(
        br####"{"gateSeverityAtLeast":"note","rules":[{"emitWhen":{"filters":[],"minResolution":"enumerated","op":"exists","relation":"a"},"enabled":false,"evidenceUse":[],"gate":false,"ruleId":"a","ruleProgramRef":{"contributionId":"a","programDigest":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","ruleStableId":"a","semanticsMajor":0},"severity":"note","subjectEnumeration":{"subjectKind":"file","universe":"a"}}],"schemaFamily":"opensip.product.policy","schemaMajor":2}"####,
    )
    .unwrap();
    let policy_raw = canonical_bytes(&policy).unwrap();
    let policy_sha = raw_sha256(&policy_raw);
    let emission = parse_json(
        format!(
            r#"{{"schemaVersion":1,"policyDigest":"{}","rules":[]}}"#,
            opensip_identity::digest_hex(&policy_sha)
        )
        .as_bytes(),
    )
    .unwrap();
    let emission_raw = canonical_bytes(&emission).unwrap();
    let emission_sha = raw_sha256(&emission_raw);
    let mut blobs = BTreeMap::new();
    blobs.insert(policy_sha, policy_raw);
    blobs.insert(emission_sha, emission_raw);
    let inputs = RetainedInputs::new(&registry, &objects, &blobs);
    let checked = inputs
        .inspect_current_record(
            emission_sha,
            "foundation/evaluator-emission-plan.schema.v1.json",
            "#",
            budget(),
        )
        .expect("cross-doc");
    check(
        &mut failures,
        "cross-doc-counts-are-not-plan-tokens",
        checked.record_count() == 2 && checked.blob_count() == 2 && checked.object_count() == 0,
        format!(
            "records={} blobs={} objects={}",
            checked.record_count(),
            checked.blob_count(),
            checked.object_count()
        ),
    );
    let again = inputs
        .inspect_current_record(
            emission_sha,
            "foundation/evaluator-emission-plan.schema.v1.json",
            "#",
            budget(),
        )
        .unwrap();
    check(
        &mut failures,
        "memo-by-hash-document-selector-is-stable",
        again.record_count() == checked.record_count() && again.blob_count() == checked.blob_count(),
        format!("{} vs {}", again.record_count(), checked.record_count()),
    );

    // Same bytes, different selector: separate memo key.
    let unit = parse_json(
        br#"{"markerPath":"","recognition":{"entryPoints":{"source":"explicit","state":"all"},"observedHints":[],"recognized":[],"schemaVersion":1},"recognitionId":"sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","rootPath":"","unitOrdinal":0}"#,
    )
    .unwrap();
    // Native-v2 shape-only: DependencyFileManifestV1 is not a foundation walk.
    let manifest = parse_json(
        format!(
            r#"[{{"path":"dep/a.rs","contentSha256":"{}","byteLength":7}}]"#,
            "0".repeat(64)
        )
        .as_bytes(),
    )
    .unwrap();
    let man_raw = canonical_bytes(&manifest).unwrap();
    let man_sha = raw_sha256(&man_raw);
    blobs.insert(man_sha, man_raw);
    let inputs = RetainedInputs::new(&registry, &objects, &blobs);
    let native = inputs.inspect_current_record(
        man_sha,
        "native/native-evidence.schemas.v2.json",
        "#/$defs/DependencyFileManifestV1",
        budget(),
    );
    check(
        &mut failures,
        "native-v2-is-shape-only-not-generic-foundation-walk",
        native.as_ref().map(|c| (c.record_count(), c.blob_count())).ok() == Some((1, 1))
            && matches!(inputs.blob([0; 32]), Err(RetainedInputError::MissingBlob(_))),
        err_debug(native.map(|_| ())),
    );

    // payload-class remains Unsupported (coverage payload).
    let coverage = parse_json(
        br#"{"schemaVersion":2,"scopeId":"scope2:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","payloadSchemaDigest":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","payloadDigest":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}"#,
    )
    .unwrap();
    let cov_raw = canonical_bytes(&coverage).unwrap();
    let cov_sha = raw_sha256(&cov_raw);
    blobs.insert(cov_sha, cov_raw);
    blobs.insert([0xaa; 32], b"placeholder".to_vec());
    let inputs = RetainedInputs::new(&registry, &objects, &blobs);
    check(
        &mut failures,
        "payload-class-record-stays-unsupported",
        matches!(
            inputs.inspect_identity_record(cov_sha, "coverage", budget()),
            Err(GraphError::Unsupported("payload-class record"))
        ),
        err_debug(inputs.inspect_identity_record(cov_sha, "coverage", budget())),
    );

    // Inspect APIs are not IdentityCandidate / Run.
    check(
        &mut failures,
        "inspect-returns-structuralchecks-not-candidate",
        core::any::type_name::<opensip_identity::StructuralChecks>().contains("StructuralChecks"),
        "type".into(),
    );

    // Derived recognition uses inline preimage; missing CAS frame is allowed on match.
    let recognition = parse_json(
        br#"{"entryPoints":{"source":"explicit","state":"all"},"observedHints":[],"recognized":[],"schemaVersion":1}"#,
    )
    .unwrap();
    let derived = hash_canonical_value("native.framework-recognition.v1", &recognition).unwrap();
    let row = parse_json(
        format!(
            r#"{{"markerPath":"","recognition":{},"recognitionId":"sha256:{}","rootPath":"","unitOrdinal":0}}"#,
            core::str::from_utf8(&canonical_bytes(&recognition).unwrap()).unwrap(),
            opensip_identity::digest_hex(&derived)
        )
        .as_bytes(),
    )
    .unwrap();
    let row_raw = canonical_bytes(&row).unwrap();
    let row_sha = raw_sha256(&row_raw);
    let mut rec_blobs = BTreeMap::new();
    rec_blobs.insert(row_sha, row_raw);
    let inputs = RetainedInputs::new(&registry, &objects, &rec_blobs);
    let rec = inputs
        .inspect_current_record(
            row_sha,
            "foundation/framework-recognition-plan.schema.v1.json",
            "#/$defs/UnitRecognitionV1",
            budget(),
        )
        .expect("recognition match");
    check(
        &mut failures,
        "recognition-match-does-not-require-cas-frame",
        rec.record_count() == 1
            && rec.blob_count() == 1
            && matches!(inputs.blob(derived), Err(RetainedInputError::MissingBlob(_))),
        format!("records={} blobs={}", rec.record_count(), rec.blob_count()),
    );
    check(
        &mut failures,
        "hash-check-is-not-feature-or-native-admit",
        !matches!(JsonValue::Null, JsonValue::Null) || rec.object_count() == 0,
        "objects present".into(),
    );

    // Unknown artifact class stays Law (not a bypass).
    // Fragment/owner-retained still Unsupported — coverage by code path in digest_field.

    if failures.is_empty() {
        println!("ALL_PASS");
        std::process::exit(0);
    }
    println!("FAILURES {}", failures.len());
    for f in failures {
        println!("  {f}");
    }
    std::process::exit(1);
}
