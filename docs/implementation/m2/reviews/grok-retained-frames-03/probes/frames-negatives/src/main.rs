//! Independent review negatives. Not part of the frozen subject.
use opensip_identity::{
    GraphError, NativeFrameSet, ObjectInput, RegisteredSchemas, RetainedInputError, RetainedInputs,
    canonical_bytes, hash_preimage, parse_json, parse_hash_preimage, raw_sha256,
};
use std::{collections::BTreeMap, fs, path::PathBuf};

fn product() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../../copy/product")
}
fn arch() -> PathBuf {
    PathBuf::from("/Users/sb/code/opensip-ai/opensip_arch")
}
fn hex(d: &[u8; 32]) -> String {
    opensip_identity::digest_hex(d)
}
fn err_debug<T>(r: Result<T, GraphError>) -> String {
    match r {
        Ok(_) => "ok".into(),
        Err(e) => format!("{e:?}"),
    }
}

fn main() {
    let mut failures: Vec<String> = Vec::new();
    fn check(failures: &mut Vec<String>, name: &str, ok: bool, detail: String) {
        println!("{} {}", if ok { "PASS" } else { "FAIL" }, name);
        if !ok {
            failures.push(format!("{name}: {detail}"));
        }
    }

    let registry = opensip_host::embedded_schema_registry().expect("registry");
    let pins = RegisteredSchemas::source_requirements();
    check(&mut failures, 
        "source-pins-are-48",
        pins.len() == 48,
        format!("{}", pins.len()),
    );

    let mut blobs = BTreeMap::new();
    let objects: BTreeMap<String, ObjectInput> = BTreeMap::new();
    let mut pin_ok = 0usize;
    for pin in pins {
        let path = product().join(pin.source_path());
        let raw = fs::read(&path).unwrap_or_else(|_| panic!("read {}", path.display()));
        check(&mut failures, 
            &format!("pin-bytes:{}", pin.source_path()),
            raw.len() == pin.bytes() && raw_sha256(&raw) == pin.sha256(),
            format!("len {} vs {}", raw.len(), pin.bytes()),
        );
        blobs.insert(raw_sha256(&raw), raw);
        pin_ok += 1;
    }
    check(&mut failures, "read-all-48-pins", pin_ok == 48, format!("{pin_ok}"));

    let inputs = RetainedInputs::new(&registry, &objects, &blobs);
    let mut registered = Vec::new();
    let mut unregistered = Vec::new();
    for pin in pins {
        match inputs.registered_schema_blob(pin.sha256()) {
            Ok(_) => registered.push(pin.source_path()),
            Err(GraphError::UnregisteredSchemaDocument) => unregistered.push(pin.source_path()),
            Err(other) => failures.push(format!("unexpected {:?} for {}", other, pin.source_path())),
        }
    }
    check(&mut failures, 
        "exactly-9-of-48-are-payload-registry-members",
        registered.len() == 9 && unregistered.len() == 39,
        format!("ok={} unreg={}", registered.len(), unregistered.len()),
    );
    let expected_registered = [
        "schemas/sources/enumeration-plan-v1.schema.json",
        "schemas/sources/evaluator-emission-plan-v1.schema.json",
        "schemas/sources/framework-recognition-plan-v1.schema.json",
        "schemas/sources/import-source-context-v1.schema.json",
        "schemas/sources/imported-v1.schema.json",
        "schemas/sources/native-v2.schema.json",
        "schemas/sources/policy-v1.schema.json",
        "schemas/sources/relation-payload-v2.schema.json",
        "schemas/sources/test-execution-v1.schema.json",
    ];
    check(&mut failures, 
        "registered-set-is-payload-rows-not-caller-chosen",
        expected_registered.iter().all(|p| registered.contains(p)) && registered.len() == 9,
        format!("{registered:?}"),
    );
    check(&mut failures, 
        "identity-v3-is-available-but-not-payload-member",
        unregistered.contains(&"schemas/sources/identity-v3.schema.json"),
        format!("{unregistered:?}"),
    );
    check(&mut failures, 
        "policy-v2-is-available-but-not-payload-member",
        unregistered.contains(&"schemas/sources/policy-v2.schema.json"),
        format!("{unregistered:?}"),
    );

    let hist_native = fs::read(
        arch().join("docs/coop/design-corrections/native/native-evidence.schemas.v2.json"),
    )
    .unwrap();
    let hist_policy = fs::read(
        arch().join(
            "docs/coop/design-corrections/workflows/schemas/policy-document.v2.schema.json",
        ),
    )
    .unwrap();
    let hist_native_sha = raw_sha256(&hist_native);
    let hist_policy_sha = raw_sha256(&hist_policy);
    blobs.insert(hist_native_sha, hist_native);
    blobs.insert(hist_policy_sha, hist_policy);
    let inputs = RetainedInputs::new(&registry, &objects, &blobs);
    check(&mut failures, 
        "historical-native-same-id-is-not-current-member",
        matches!(
            inputs.registered_schema_blob(hist_native_sha),
            Err(GraphError::UnregisteredSchemaDocument)
        ) && hex(&hist_native_sha)
            == "2d37b810bd9ffed741d74241fc8a11051606862d8af2f152eed16b92bdc66043",
        hex(&hist_native_sha),
    );
    check(&mut failures, 
        "historical-policy-v2-same-id-is-not-current-member",
        matches!(
            inputs.registered_schema_blob(hist_policy_sha),
            Err(GraphError::UnregisteredSchemaDocument)
        ) && hex(&hist_policy_sha)
            == "c8b0a907a7b8019be4c6ed5b1d217ac7689bbbba2873679c42b86499280a3595",
        hex(&hist_policy_sha),
    );

    let missing = [0x11; 32];
    check(&mut failures, 
        "missing-schema-blob-is-unavailable-not-unregistered",
        matches!(
            inputs.registered_schema_blob(missing),
            Err(GraphError::Input(RetainedInputError::MissingBlob(_)))
        ),
        err_debug(inputs.registered_schema_blob(missing)),
    );
    blobs.insert(missing, b"not-the-digest".to_vec());
    let inputs = RetainedInputs::new(&registry, &objects, &blobs);
    check(&mut failures, 
        "corrupt-schema-blob-is-digest-invalid-not-missing",
        matches!(
            inputs.registered_schema_blob(missing),
            Err(GraphError::Input(RetainedInputError::BlobDigest))
        ),
        err_debug(inputs.registered_schema_blob(missing)),
    );

    let value = parse_json(
        format!(
            r#"[{{"path":"dep/a.rs","contentSha256":"{}","byteLength":7}}]"#,
            "0".repeat(64)
        )
        .as_bytes(),
    )
    .unwrap();
    let framed = hash_preimage("native.dependency-file-manifest.v1", &value).unwrap();
    let sha = raw_sha256(&framed);
    blobs.insert(sha, framed.clone());
    let inputs = RetainedInputs::new(&registry, &objects, &blobs);
    let candidate = inputs
        .frame_candidate(sha, NativeFrameSet::Nested, 1_000_000)
        .expect("nested frame");
    check(&mut failures, 
        "getters-are-read-only-shape-not-native-admit",
        candidate.domain() == "native.dependency-file-manifest.v1"
            && candidate.domain_set() == NativeFrameSet::Nested
            && candidate.digest() == sha
            && candidate.descriptor() == &value
            && candidate.schema().selector() == "/$defs/DependencyFileManifestV1",
        candidate.domain().into(),
    );
    check(&mut failures, 
        "reuses-parse-hash-preimage",
        parse_hash_preimage("native.dependency-file-manifest.v1", &framed).unwrap() == value,
        "unframe mismatch".into(),
    );
    check(&mut failures, 
        "wrong-set-is-unregistered-domain-not-ok",
        matches!(
            inputs.frame_candidate(sha, NativeFrameSet::Context, 1_000_000),
            Err(GraphError::UnregisteredFrameDomain)
        ),
        err_debug(inputs.frame_candidate(sha, NativeFrameSet::Context, 1_000_000)),
    );
    check(&mut failures, 
        "wrong-universe-set-is-unregistered-domain",
        matches!(
            inputs.frame_candidate(sha, NativeFrameSet::SemanticUniverse, 1_000_000),
            Err(GraphError::UnregisteredFrameDomain)
        ),
        "universe accepted nested domain".into(),
    );

    let raw_c = canonical_bytes(&value).unwrap();
    let c_sha = raw_sha256(&raw_c);
    blobs.insert(c_sha, raw_c.clone());
    let inputs = RetainedInputs::new(&registry, &objects, &blobs);
    check(&mut failures, 
        "raw-C-is-not-an-H-frame",
        matches!(
            inputs.frame_candidate(c_sha, NativeFrameSet::Nested, 1_000_000),
            Err(GraphError::Frame(opensip_identity::DigestError::FramePrefix))
        ) && parse_hash_preimage("native.dependency-file-manifest.v1", &raw_c).is_err(),
        err_debug(inputs.frame_candidate(c_sha, NativeFrameSet::Nested, 1_000_000)),
    );

    let short = framed[..10].to_vec();
    let short_sha = raw_sha256(&short);
    blobs.insert(short_sha, short);
    let inputs = RetainedInputs::new(&registry, &objects, &blobs);
    check(&mut failures, 
        "truncated-frame-is-invalid-not-unavailable",
        matches!(
            inputs.frame_candidate(short_sha, NativeFrameSet::Nested, 1_000_000),
            Err(GraphError::Frame(_))
        ),
        err_debug(inputs.frame_candidate(short_sha, NativeFrameSet::Nested, 1_000_000)),
    );

    let mut bad_len = framed.clone();
    let prefix = b"opensip.product.v1\0native.dependency-file-manifest.v1\0";
    bad_len.splice(prefix.len()..prefix.len() + 8, 0u64.to_be_bytes());
    let bad_sha = raw_sha256(&bad_len);
    blobs.insert(bad_sha, bad_len);
    let inputs = RetainedInputs::new(&registry, &objects, &blobs);
    check(&mut failures, 
        "declared-length-mismatch-is-frame-length",
        matches!(
            inputs.frame_candidate(bad_sha, NativeFrameSet::Nested, 1_000_000),
            Err(GraphError::Frame(opensip_identity::DigestError::FrameLength))
        ),
        err_debug(inputs.frame_candidate(bad_sha, NativeFrameSet::Nested, 1_000_000)),
    );

    let empty_objects = BTreeMap::new();
    let inputs = RetainedInputs::new(&registry, &empty_objects, &blobs);
    check(&mut failures, 
        "missing-frame-blob-is-unavailable",
        matches!(
            inputs.frame_candidate([0x22; 32], NativeFrameSet::Nested, 1_000_000),
            Err(GraphError::Input(RetainedInputError::MissingBlob(_)))
        ),
        "missing not distinct".into(),
    );

    // Registry row names outstanding joins; getters expose it without an ADMIT token.
    let inputs = RetainedInputs::new(&registry, &objects, &blobs);
    let candidate = inputs
        .frame_candidate(sha, NativeFrameSet::Nested, 1_000_000)
        .unwrap();
    let row = candidate.registry_row();
    check(&mut failures, 
        "registry-row-names-current-document-not-historical-alias",
        matches!(
            row,
            opensip_identity::JsonValue::Object(map)
                if map.get("document").and_then(|v| match v {
                    opensip_identity::JsonValue::String(s) => Some(s.as_str()),
                    _ => None
                }) == Some("native/native-evidence.schemas.v2.json")
        ),
        format!("{row:?}"),
    );

    if failures.is_empty() {
        println!("ALL_PASS {}", 1);
        std::process::exit(0);
    }
    println!("FAILURES {}", failures.len());
    for f in failures {
        println!("  {f}");
    }
    std::process::exit(1);
}
