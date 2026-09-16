//! Independent frozen-13 retention controls. Not part of the frozen subject.
use opensip_evaluator::{NativeRetentionError, NativeUniverseError, inspect_native_context, inspect_native_retention};
use opensip_identity::{
    GraphError, IdentityDomain, JsonValue as V, NativeFrameSet, ObjectInput, RetainedInputError,
    RetainedInputs, TraversalBudget, parse_json, raw_sha256,
};
use std::collections::BTreeMap;

fn object(v: &V) -> &BTreeMap<String, V> {
    let V::Object(o) = v else { panic!("object") };
    o
}
fn array(v: &V) -> &[V] {
    let V::Array(a) = v else { panic!("array") };
    a
}
fn string(v: &V) -> &str {
    let V::String(s) = v else { panic!("string") };
    s
}
fn bytes(s: &str) -> Vec<u8> {
    (0..s.len())
        .step_by(2)
        .map(|i| u8::from_str_radix(&s[i..i + 2], 16).unwrap())
        .collect()
}
fn objects(fixture: &V) -> BTreeMap<String, ObjectInput> {
    array(&object(fixture)["objects"])
        .iter()
        .map(|r| {
            let r = object(r);
            (
                string(&r["id"]).into(),
                ObjectInput {
                    domain: IdentityDomain::parse(string(&r["domain"])).unwrap(),
                    descriptor: r["descriptor"].clone(),
                },
            )
        })
        .collect()
}

fn main() {
    let mut failures = Vec::new();
    let check = |failures: &mut Vec<String>, name: &str, ok: bool, detail: String| {
        println!("{} {} {}", if ok { "PASS" } else { "FAIL" }, name, detail);
        if !ok {
            failures.push(format!("{name}: {detail}"));
        }
    };
    let registry = opensip_host::embedded_schema_registry().unwrap();
    let all = parse_json(include_bytes!(
        "../../../copy/product/crates/host/tests/fixtures/native-context-fixtures.json"
    ))
    .unwrap();
    let fixture = object(&all)["nativeRetention"].clone();
    let obs = objects(&fixture);
    let f = object(&fixture);
    let id: [u8; 32] = bytes(string(&f["digest"])).try_into().unwrap();
    let snapshot = string(&f["snapshotId"]).to_owned();
    let mut bs: BTreeMap<[u8; 32], Vec<u8>> = array(&f["blobs"])
        .iter()
        .map(|r| {
            let r = object(r);
            (
                bytes(string(&r["digest"])).try_into().unwrap(),
                bytes(string(&r["hex"])),
            )
        })
        .collect();
    let limits = TraversalBudget {
        steps: 100_000,
        depth: 96,
        descriptor_work: 10_000_000,
    };
    let golden = inspect_native_retention(
        &RetainedInputs::new(&registry, &obs, &bs),
        id,
        NativeFrameSet::SemanticUniverse,
        &snapshot,
        limits,
    )
    .unwrap();
    check(
        &mut failures,
        "golden-syntax-universe-counts",
        golden.frame_count() == 2 && golden.closure_count() == 1,
        format!("frames={} closures={}", golden.frame_count(), golden.closure_count()),
    );
    let extra = raw_sha256(b"unrelated extra retained artifact");
    bs.insert(extra, b"unrelated extra retained artifact".to_vec());
    let with_extra = inspect_native_retention(
        &RetainedInputs::new(&registry, &obs, &bs),
        id,
        NativeFrameSet::SemanticUniverse,
        &snapshot,
        limits,
    )
    .unwrap();
    check(
        &mut failures,
        "unrelated-blob-does-not-change-counts",
        with_extra.frame_count() == golden.frame_count()
            && with_extra.blob_count() == golden.blob_count()
            && with_extra.closure_count() == golden.closure_count(),
        format!(
            "frames={} blobs={} closures={}",
            with_extra.frame_count(),
            with_extra.blob_count(),
            with_extra.closure_count()
        ),
    );
    bs.remove(&extra);

    let u = opensip_identity::parse_hash_preimage("native.semantic-universe.syntax.v2", &bs[&id])
        .unwrap();
    let context_id: [u8; 32] = bytes(
        string(&object(&u)["nativeContextId"])
            .strip_prefix("sha256:")
            .unwrap(),
    )
    .try_into()
    .unwrap();
    let context =
        opensip_identity::parse_hash_preimage("native.context.syntax.v2", &bs[&context_id]).unwrap();
    let key = string(&object(&object(&context)["grammarBundle"])["closureId"]);
    let member = &array(&object(&obs[key].descriptor)["tree"])[0];
    let digest: [u8; 32] = bytes(string(&object(member)["sha256"])).try_into().unwrap();
    let original = bs.remove(&digest).unwrap();
    check(
        &mut failures,
        "context-owner-passes-without-grammar-bytes",
        inspect_native_context(&RetainedInputs::new(&registry, &obs, &bs), context_id, 10_000_000)
            .unwrap()
            .refusals()
            .is_empty(),
        "empty refusals".into(),
    );
    check(
        &mut failures,
        "retention-fails-missing-grammar-bytes",
        matches!(
            inspect_native_retention(
                &RetainedInputs::new(&registry, &obs, &bs),
                id,
                NativeFrameSet::SemanticUniverse,
                &snapshot,
                limits,
            ),
            Err(NativeRetentionError::Owner(NativeUniverseError::Frame(
                GraphError::Input(RetainedInputError::MissingBlob(_))
            )))
        ),
        "MissingBlob".into(),
    );
    bs.insert(digest, b"changed".to_vec());
    check(
        &mut failures,
        "retention-fails-corrupt-grammar-bytes",
        matches!(
            inspect_native_retention(
                &RetainedInputs::new(&registry, &obs, &bs),
                id,
                NativeFrameSet::SemanticUniverse,
                &snapshot,
                limits,
            ),
            Err(NativeRetentionError::Owner(NativeUniverseError::Frame(
                GraphError::Input(RetainedInputError::BlobDigest)
            )))
        ),
        "BlobDigest".into(),
    );
    bs.insert(digest, original);
    check(
        &mut failures,
        "steps-one-is-limit",
        matches!(
            inspect_native_retention(
                &RetainedInputs::new(&registry, &obs, &bs),
                id,
                NativeFrameSet::SemanticUniverse,
                &snapshot,
                TraversalBudget {
                    steps: 1,
                    ..limits
                },
            ),
            Err(NativeRetentionError::Limit)
        ),
        "Limit".into(),
    );
    check(
        &mut failures,
        "zero-budget-is-limit-before-walk",
        matches!(
            inspect_native_retention(
                &RetainedInputs::new(&registry, &obs, &bs),
                id,
                NativeFrameSet::SemanticUniverse,
                &snapshot,
                TraversalBudget {
                    steps: 0,
                    ..limits
                },
            ),
            Err(NativeRetentionError::Limit)
        ),
        "Limit".into(),
    );
    if failures.is_empty() {
        println!("retention-negatives: ALL_PASS");
    } else {
        println!("retention-negatives: FAILURES {}", failures.len());
        std::process::exit(1);
    }
}
